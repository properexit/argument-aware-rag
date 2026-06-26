"""Multi-source dataset assembler for Phase 2.

This module takes raw inputs from each source dataset and emits a unified
JSONL of `TrainRecord`s with a consistent argument structure schema. The
schema decisions are deliberate:

  - 'claim', 'premise', 'citation' as component kinds — same as Phase 1
  - 'support' / 'attack' / 'psupport' / 'pattack' as relations
  - psupport and pattack are PRESERVED (not merged into support/attack)
    because Phase 1's verifier uses them as separate calibration signals
  - Components that don't fit (e.g. AAEC's MajorClaim) are mapped to the
    closest kind with the original kind recorded in `extra`.

Real loaders for AAEC, AbstRCT and LIARArg live in subroutines that can
be implemented or stubbed independently. The default behaviour without
any source paths set is to emit a tiny synthetic corpus useful for
end-to-end testing without external data.
"""
from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Iterable

from .schema import (
    TrainRecord, ArgStructureDict, ComponentDict, RelationDict,
    DatasetConfig,
)


# ────────────────────────────────────────────────────────────────────────────
# Source loaders — stubs for now, populate when real data is available.
# ────────────────────────────────────────────────────────────────────────────

def _stub_loader_warning(source: str) -> None:
    print(f"[dataset] {source} path not configured — skipping. "
          f"Set {source}_path in DatasetConfig to ingest.")


def load_aaec(path: str) -> Iterable[TrainRecord]:
    """Stub. Real impl parses brat .ann files into TrainRecords."""
    if not path:
        _stub_loader_warning("aaec")
        return []
    raise NotImplementedError("AAEC loader stub — implement when ready")


def load_abstrct(path: str) -> Iterable[TrainRecord]:
    """Stub. Real impl parses BIO + relation TSVs into TrainRecords."""
    if not path:
        _stub_loader_warning("abstrct")
        return []
    raise NotImplementedError("AbstRCT loader stub — implement when ready")


def load_liararg(path: str) -> list[TrainRecord]:
    """Load LIARArg into TrainRecords.

    `path` can be either:
      - a directory containing train.jsonl / val.jsonl / test.jsonl
        (the pre-parsed LIARArg splits from Phase 1)
      - a single .jsonl file (treated as the train split)

    The pre-parsed JSONL schema is:
        id, label, statement, speaker, full_text, summary,
        claim_ids/texts, premise_ids/texts, citation_ids/texts,
        support_relations, attack_relations, psupport_relations,
        pattack_relations    (each: list[[src_id, tgt_id]])

    The split label is preserved (we do NOT re-shuffle) so LIAR's
    canonical test set stays intact — important for direct comparison
    with Phase 1's gold-parser numbers.
    """
    if not path:
        _stub_loader_warning("liararg")
        return []
    p = Path(path)
    if p.is_dir():
        sources = [
            (p / "train.jsonl", "train"),
            (p / "val.jsonl",   "val"),
            (p / "test.jsonl",  "test"),
        ]
        sources = [(f, s) for f, s in sources if f.exists()]
    elif p.is_file():
        sources = [(p, "train")]
    else:
        raise FileNotFoundError(f"liararg path not found: {path}")

    INSTRUCTION = ("Extract all argument components and relations from "
                   "the text. Output strict JSON with claim_components, "
                   "premise_components, citation_components, and relations.")

    records: list[TrainRecord] = []
    for file_path, split in sources:
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                records.append(_liararg_row_to_record(row, split, INSTRUCTION))
    print(f"[dataset] liararg: loaded {len(records)} records from {path}")
    return records


def _liararg_row_to_record(
    row: dict, split: str, instruction: str,
) -> TrainRecord:
    """Convert one parsed LIARArg JSONL row to a TrainRecord."""
    def _zip_components(ids, texts, kind):
        out = []
        for cid, ctext in zip(ids or [], texts or []):
            out.append({"id": int(cid), "type": kind, "text": str(ctext)})
        return out

    claims    = _zip_components(row.get("claim_ids"),    row.get("claim_texts"),    "claim")
    premises  = _zip_components(row.get("premise_ids"),  row.get("premise_texts"),  "premise")
    citations = _zip_components(row.get("citation_ids"), row.get("citation_texts"), "citation")

    relations = []
    for rel_type in ("support", "attack", "psupport", "pattack"):
        key = f"{rel_type}_relations"
        for pair in (row.get(key) or []):
            if len(pair) >= 2:
                relations.append({
                    "src": int(pair[0]),
                    "tgt": int(pair[1]),
                    "type": rel_type,
                })

    # Input text: prefer full_text but truncate so we don't blow up the
    # student's max_input_len. Most articles are <5K chars; longer ones
    # we accept some loss on gold span coverage.
    input_text = row.get("full_text") or row.get("summary") or row.get("statement", "")

    return {
        "instruction": instruction,
        "input": str(input_text),
        "reasoning": "",
        "output": {
            "claim_components": claims,
            "premise_components": premises,
            "citation_components": citations,
            "relations": relations,
        },
        "source_dataset": "liararg",
        "label_kind": "gold",
        "split": split,
        "domain": "politics",
    }


def load_aries_for_silver(
    csv_path: str,
    silver_sources: list[str],
    samples_per_source: int,
    seed: int,
) -> list[dict]:
    """Return rows from ARIES CSV that need silver annotation.

    Each dict has keys {`text`, `source`}. Caller passes these to the
    teacher in teacher.py to generate the silver `output`/`reasoning`.
    """
    if not csv_path:
        _stub_loader_warning("aries_clean")
        return []
    try:
        import pandas as pd
    except ImportError:
        raise RuntimeError("pandas required for ARIES loading")
    df = pd.read_csv(csv_path)
    rng = random.Random(seed)
    rows: list[dict] = []
    for source, group in df.groupby("data_source"):
        if source not in silver_sources:
            continue
        group = group.drop_duplicates("argument").reset_index(drop=True)
        sampled_idx = rng.sample(
            range(len(group)),
            min(len(group), samples_per_source),
        )
        for i in sampled_idx:
            rows.append({
                "text": str(group.iloc[i]["argument"]),
                "source": str(source),
            })
    return rows


# ────────────────────────────────────────────────────────────────────────────
# Synthetic corpus — used when no real datasets are configured.
# Lets you run the entire Phase 2 pipeline end-to-end on zero real data.
# ────────────────────────────────────────────────────────────────────────────

_SYNTHETIC_EXAMPLES: list[TrainRecord] = [
    {
        "instruction": "Extract the argument structure as JSON.",
        "input": ("Capital punishment is not a solution. The judicial process "
                  "may make mistakes. The state needs the death penalty as a "
                  "deterrent to horrific crimes."),
        "reasoning": "",
        "output": {
            "claim_components": [
                {"id": 1, "type": "claim",
                 "text": "Capital punishment is not a solution"},
                {"id": 3, "type": "claim",
                 "text": "the state needs the death penalty as a deterrent"},
            ],
            "premise_components": [
                {"id": 2, "type": "premise",
                 "text": "the judicial process may make mistakes"},
            ],
            "citation_components": [],
            "relations": [
                {"src": 2, "tgt": 1, "type": "support"},
                {"src": 3, "tgt": 1, "type": "attack"},
            ],
        },
        "source_dataset": "synthetic",
        "label_kind": "gold",
        "split": "train",
        "domain": "ethics",
    },
    {
        "instruction": "Extract the argument structure as JSON.",
        "input": ("Online learning is the future. Studies show students retain "
                  "more from interactive video. Critics say it lacks "
                  "interpersonal contact, which is essential."),
        "reasoning": "",
        "output": {
            "claim_components": [
                {"id": 1, "type": "claim",
                 "text": "Online learning is the future"},
            ],
            "premise_components": [
                {"id": 2, "type": "premise",
                 "text": "students retain more from interactive video"},
                {"id": 3, "type": "premise",
                 "text": "it lacks interpersonal contact"},
            ],
            "citation_components": [],
            "relations": [
                {"src": 2, "tgt": 1, "type": "support"},
                {"src": 3, "tgt": 1, "type": "attack"},
            ],
        },
        "source_dataset": "synthetic",
        "label_kind": "gold",
        "split": "val",
        "domain": "education",
    },
]


def synthetic_corpus(n: int = 50) -> list[TrainRecord]:
    """Replicate the two synthetic examples enough times to be useful for
    smoke-testing. Strips the split field so assemble_corpus's stratifier
    can assign train/val/test fractions cleanly."""
    out: list[TrainRecord] = []
    for i in range(n):
        rec = dict(_SYNTHETIC_EXAMPLES[i % len(_SYNTHETIC_EXAMPLES)])  # type: ignore
        rec.pop("split", None)
        out.append(rec)
    return out


# ────────────────────────────────────────────────────────────────────────────
# Top-level entry point
# ────────────────────────────────────────────────────────────────────────────

def assemble_corpus(cfg: DatasetConfig) -> list[TrainRecord]:
    """Build the full Phase 2 training corpus from all configured sources.

    Returns a list of TrainRecords. Caller is responsible for writing to
    disk (see write_jsonl) and for invoking the teacher on unannotated
    silver rows.
    """
    records: list[TrainRecord] = []
    # Gold sources
    records.extend(load_aaec(cfg.aaec_path))
    records.extend(load_abstrct(cfg.abstrct_path))
    records.extend(load_liararg(cfg.liararg_path))

    if not records:
        print("[dataset] no real sources configured — using synthetic corpus.")
        records = synthetic_corpus()

    # Stratified-by-source train/val/test split.
    # IMPORTANT: records that already have a canonical split (e.g. LIARArg's
    # train/val/test from the pre-parsed JSONLs, which align with LIAR-test)
    # are preserved as-is. We only assign splits for sources that arrived
    # without one (synthetic, or any source whose loader didn't set it).
    rng = random.Random(cfg.seed)
    by_source: dict[str, list[TrainRecord]] = {}
    for r in records:
        by_source.setdefault(r["source_dataset"], []).append(r)
    out: list[TrainRecord] = []
    for source, rs in by_source.items():
        if all(r.get("split") in ("train", "val", "test") for r in rs):
            # All rows already carry a canonical split — keep it.
            out.extend(rs)
            continue
        # Otherwise re-shuffle and assign splits per cfg fractions.
        rng.shuffle(rs)
        n = len(rs)
        n_test = int(n * cfg.test_frac)
        n_val = int(n * cfg.val_frac)
        for i, r in enumerate(rs):
            if i < n_test:
                r["split"] = "test"
            elif i < n_test + n_val:
                r["split"] = "val"
            else:
                r["split"] = "train"
            out.append(r)

    print(f"[dataset] assembled {len(out)} records "
          f"from {len(by_source)} source(s)")
    return out


def write_jsonl(records: list[TrainRecord], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[dataset] wrote {len(records)} records to {path}")


def read_jsonl(path: str | Path) -> list[TrainRecord]:
    out: list[TrainRecord] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


# ────────────────────────────────────────────────────────────────────────────
# Phase 2-β unified-corpus loader
# ────────────────────────────────────────────────────────────────────────────

def load_unified_corpus(
    unified_dir: str | Path,
    exclude_sources: tuple[str, ...] = (),
    include_silver: bool = True,
    splits: tuple[str, ...] = ("train", "val", "test"),
) -> list[TrainRecord]:
    """Load all unified JSONLs from a directory and combine them.

    Expects filename pattern <source>_<split>.jsonl (e.g. abstrct_train.jsonl).
    Skips sources in `exclude_sources` — typically used to keep LIARArg
    out of training while still letting it sit in the unified directory
    for the integration evaluation.

    Returns one combined list, with each record's "split" field already
    populated by the loaders. Caller can filter by record["split"].
    """
    unified_dir = Path(unified_dir)
    if not unified_dir.is_dir():
        raise FileNotFoundError(f"unified_dir not found: {unified_dir}")

    out: list[TrainRecord] = []
    by_source: dict[str, int] = {}
    for jsonl_path in sorted(unified_dir.glob("*.jsonl")):
        # Filename: <source>_<split>.jsonl — split out the trailing _split
        stem = jsonl_path.stem
        if "_" not in stem:
            continue
        source, split = stem.rsplit("_", 1)
        if source in exclude_sources or split not in splits:
            continue
        recs = read_jsonl(jsonl_path)
        if not include_silver:
            recs = [r for r in recs if r.get("label_kind", "gold") == "gold"]
        out.extend(recs)
        by_source[source] = by_source.get(source, 0) + len(recs)

    print(f"[unified] loaded {len(out)} records across {len(by_source)} source(s):")
    for src in sorted(by_source):
        print(f"  {src}: {by_source[src]}")
    return out
