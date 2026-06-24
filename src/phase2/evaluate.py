"""Phase 2 evaluation — parser-level metrics.

Two evaluation regimes:

1. Component-level F1: did the student detect the right text spans as
   claims / premises / citations? Uses a soft text-overlap match (a
   predicted component matches a gold one if their normalised text
   shares ≥ overlap_threshold of unigrams).

2. Relation-level F1: did the student identify the right
   (src_kind, tgt_kind, type) triples? Components are first matched
   1-1 between pred and gold via greedy text overlap, then relations
   are evaluated on the matched ID space.

This is the standalone metric. Integration F1 — measuring the gap
between gold-parser and learned-parser Phase 1 macro-F1 — is computed
by running the full Phase 1 pipeline with each parser and comparing
the existing Phase 1 metrics; that lives outside this module.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Sequence

from .schema import ArgStructureDict, TrainRecord


# ────────────────────────────────────────────────────────────────────────────
# Text matching utilities
# ────────────────────────────────────────────────────────────────────────────

_WORD = re.compile(r"\w+")


def _tokens(s: str) -> Counter:
    return Counter(w.lower() for w in _WORD.findall(s or ""))


def _overlap(a: str, b: str) -> float:
    """Symmetric token-overlap ratio in [0, 1]."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    inter = sum((ta & tb).values())
    return inter / max(sum(ta.values()), sum(tb.values()))


def _greedy_match(
    pred: Sequence[dict], gold: Sequence[dict], threshold: float
) -> list[tuple[int, int]]:
    """Greedy 1-1 matching by highest overlap above threshold.

    Returns list of (pred_idx, gold_idx). Unmatched predictions/golds
    are not included.
    """
    if not pred or not gold:
        return []
    pairs: list[tuple[float, int, int]] = []
    for i, p in enumerate(pred):
        for j, g in enumerate(gold):
            o = _overlap(p.get("text", ""), g.get("text", ""))
            if o >= threshold:
                pairs.append((o, i, j))
    pairs.sort(reverse=True)
    used_p, used_g, matches = set(), set(), []
    for _, i, j in pairs:
        if i in used_p or j in used_g:
            continue
        used_p.add(i)
        used_g.add(j)
        matches.append((i, j))
    return matches


# ────────────────────────────────────────────────────────────────────────────
# Component-level F1
# ────────────────────────────────────────────────────────────────────────────

def component_prf(
    pred: ArgStructureDict, gold: ArgStructureDict, threshold: float = 0.5
) -> dict[str, dict[str, float]]:
    """Per-kind precision/recall/F1 over the three component types."""
    out: dict[str, dict[str, float]] = {}
    for kind in ("claim", "premise", "citation"):
        key = f"{kind}_components"
        p_items = pred.get(key, []) or []
        g_items = gold.get(key, []) or []
        matched = len(_greedy_match(p_items, g_items, threshold))
        precision = matched / len(p_items) if p_items else 0.0
        recall    = matched / len(g_items) if g_items else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) else 0.0)
        out[kind] = {"precision": precision, "recall": recall, "f1": f1,
                     "support_pred": len(p_items),
                     "support_gold": len(g_items),
                     "matched": matched}
    return out


# ────────────────────────────────────────────────────────────────────────────
# Relation-level F1 (conditional on component alignment)
# ────────────────────────────────────────────────────────────────────────────

def relation_prf(
    pred: ArgStructureDict, gold: ArgStructureDict, threshold: float = 0.5
) -> dict[str, float]:
    """F1 over (src_id, tgt_id, type) after greedy ID alignment.

    A predicted relation is correct iff its (matched_src_id_in_gold,
    matched_tgt_id_in_gold, type) exists in gold's relations.
    """
    # Build pred → gold id mapping per kind, then merge
    id_map: dict[int, int] = {}
    for kind in ("claim", "premise", "citation"):
        key = f"{kind}_components"
        p_items = pred.get(key, []) or []
        g_items = gold.get(key, []) or []
        for i, j in _greedy_match(p_items, g_items, threshold):
            id_map[int(p_items[i]["id"])] = int(g_items[j]["id"])

    def to_triple(r: dict) -> tuple:
        return (r.get("src"), r.get("tgt"), r.get("type", "support"))

    gold_triples = {to_triple(r) for r in (gold.get("relations") or [])}

    matched = 0
    pred_rels = pred.get("relations") or []
    for r in pred_rels:
        s = id_map.get(r.get("src"))
        t = id_map.get(r.get("tgt"))
        if s is None or t is None:
            continue
        if (s, t, r.get("type", "support")) in gold_triples:
            matched += 1

    precision = matched / len(pred_rels) if pred_rels else 0.0
    recall    = matched / len(gold_triples) if gold_triples else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) else 0.0)
    return {"precision": precision, "recall": recall, "f1": f1,
            "support_pred": len(pred_rels),
            "support_gold": len(gold_triples),
            "matched": matched}


# ────────────────────────────────────────────────────────────────────────────
# Corpus-level aggregation
# ────────────────────────────────────────────────────────────────────────────

def evaluate_corpus(
    records: list[TrainRecord],
    predictions: list[ArgStructureDict],
    threshold: float = 0.5,
) -> dict:
    """Aggregate component- and relation-level F1 across a corpus.

    Returns a dict suitable to dump to metrics.json. Per-domain
    breakdowns let you spot domains the student struggles on without
    retraining.
    """
    assert len(records) == len(predictions), "len mismatch"

    # Macro-averages, accumulated then divided
    comp_acc = {k: {"precision": 0.0, "recall": 0.0, "f1": 0.0}
                for k in ("claim", "premise", "citation")}
    rel_acc = {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    per_domain: dict[str, list[float]] = {}

    for rec, pred in zip(records, predictions):
        gold = rec["output"]
        comp = component_prf(pred, gold, threshold)
        rel = relation_prf(pred, gold, threshold)
        for k in comp:
            for m in ("precision", "recall", "f1"):
                comp_acc[k][m] += comp[k][m]
        for m in ("precision", "recall", "f1"):
            rel_acc[m] += rel[m]
        per_domain.setdefault(rec.get("domain", "unknown"), []).append(rel["f1"])

    n = max(len(records), 1)
    for k in comp_acc:
        for m in comp_acc[k]:
            comp_acc[k][m] /= n
    for m in rel_acc:
        rel_acc[m] /= n

    domain_summary = {
        d: {"n": len(scores), "macro_relation_f1": sum(scores) / len(scores)}
        for d, scores in per_domain.items()
    }

    return {
        "n": len(records),
        "threshold": threshold,
        "component_f1": comp_acc,
        "relation_f1": rel_acc,
        "macro_component_f1": sum(comp_acc[k]["f1"] for k in comp_acc) / 3,
        "by_domain": domain_summary,
    }
