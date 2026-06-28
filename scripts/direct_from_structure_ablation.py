"""Direct-from-parsed-structure ablation (Mac-runnable).

Skip Phase 1's retriever-reranker entirely. For each LIARArg test row:
  - Read Phase 2-α's parser predictions (already downloaded to Mac)
  - Group the parser's premises by their support/attack role toward
    the claim components
  - Pass that structure directly to the Ollama Qwen-14B verifier
  - Compare predicted label to gold

If the resulting 6-way macro-F1 matches/beats Phase 1's 0.254 (which
includes retrieval), retrieval was doing little real work on LIARArg.

Resumable via the output JSONL — re-running picks up at the first
unprocessed row.

Usage (from repo root):
    python scripts/direct_from_structure_ablation.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


# ────────────────────── paths ──────────────────────

PARSER_PREDS = Path.home() / "Downloads" / "parser_preds_llama70b.jsonl"
GOLD_PATH    = REPO / "data" / "test.jsonl"
OUT_DIR      = REPO / "outputs" / "results_direct_from_structure"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT          = OUT_DIR / "predictions.jsonl"
LOG          = OUT_DIR / "run.log"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "qwen2.5:14b-instruct"
TIMEOUT    = 240  # seconds per verifier call (Mac Ollama can be slow)


# ────────────────────── prompt ──────────────────────

LIAR_LABELS = ["True", "Mostly-true", "Half-true",
               "Barely-true", "False", "Pants-fire"]

PROMPT_TMPL = """You are a political fact-checker. Classify the truth of the claim using EXACTLY one of these labels:
True, Mostly-true, Half-true, Barely-true, False, Pants-fire.

CLAIM: {claim}

Supporting evidence extracted from the article:
{supporting}

Attacking evidence extracted from the article:
{attacking}

Now output a single line in this exact format and nothing else:
VERDICT: <one of the six labels>"""


def collect_evidence(prediction: dict) -> tuple[list[str], list[str]]:
    """Group parser's premises/citations by their support/attack role
    toward any claim component, using the parser's own relation tags."""
    supporting, attacking = [], []
    by_id: dict[int, str] = {}
    for c in prediction.get("claim_components", []):
        by_id[c["id"]] = c.get("text", "")
    for p in prediction.get("premise_components", []):
        by_id[p["id"]] = p.get("text", "")
    for c in prediction.get("citation_components", []):
        by_id[c["id"]] = c.get("text", "")
    for rel in prediction.get("relations", []):
        src_text = by_id.get(rel.get("src"), "")
        if not src_text:
            continue
        rtype = rel.get("type", "")
        if rtype in ("support", "psupport"):
            supporting.append(src_text)
        elif rtype in ("attack", "pattack"):
            attacking.append(src_text)
    return supporting, attacking


_VERDICT_RE = re.compile(r"VERDICT:\s*([A-Za-z\-\s]+)", re.IGNORECASE)


def parse_verdict(raw: str) -> str:
    m = _VERDICT_RE.search(raw)
    candidate = (m.group(1).strip() if m else raw.strip()).split("\n")[0]
    candidate = candidate.lower()
    for lab in LIAR_LABELS:
        if lab.lower() in candidate:
            return lab
    return "Half-true"


def main():
    # Load gold
    gold: dict[int, dict] = {}
    with open(GOLD_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            gold[int(row["id"])] = {
                "label": row["label"],
                "statement": row["statement"],
            }
    print(f"[ablation] loaded {len(gold)} gold rows", flush=True)

    # Load parser predictions
    if not PARSER_PREDS.exists():
        raise FileNotFoundError(
            f"Phase 2-α parser predictions not found at {PARSER_PREDS}.\n"
            "Download phase2_data_liar/parser_preds_llama70b.jsonl from the "
            "server to ~/Downloads/.")
    preds: dict[int, dict] = {}
    with open(PARSER_PREDS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            preds[int(rec["row_id"])] = rec["prediction"]
    print(f"[ablation] loaded {len(preds)} parser predictions", flush=True)

    # Resume
    done: set[int] = set()
    if OUT.exists():
        with open(OUT) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    done.add(int(json.loads(line)["row_id"]))
                except Exception:
                    continue
    if done:
        print(f"[ablation] resuming — {len(done)} verifications already done",
              flush=True)

    todo = [rid for rid in sorted(gold) if rid not in done and rid in preds]
    print(f"[ablation] {len(todo)} rows to do (of {len(gold)} total)",
          flush=True)

    # Ollama warmup ping — Mac Ollama cold-loads slowly the first time
    print("[ablation] warmup ping to Ollama...", flush=True)
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL, "prompt": "warmup", "stream": False,
            "options": {"num_predict": 1},
        }, timeout=120)
        print(f"  warmup OK ({r.status_code})", flush=True)
    except Exception as e:
        print(f"  warmup FAILED: {e}", flush=True)
        print("  Make sure `ollama serve` is running and the model is pulled.",
              flush=True)
        return

    # Main loop
    t0 = time.time()
    n_done = 0
    with open(OUT, "a") as fout:
        for row_id in todo:
            g = gold[row_id]
            supporting, attacking = collect_evidence(preds[row_id])
            prompt = PROMPT_TMPL.format(
                claim=g["statement"],
                supporting=("\n".join(f"- {s}" for s in supporting[:8])
                            or "(none)"),
                attacking=("\n".join(f"- {s}" for s in attacking[:8])
                           or "(none)"),
            )
            try:
                r = requests.post(OLLAMA_URL, json={
                    "model": MODEL, "prompt": prompt, "stream": False,
                    "options": {"temperature": 0.0, "num_predict": 30},
                }, timeout=TIMEOUT)
                raw = r.json().get("response", "")
                verdict = parse_verdict(raw)
            except Exception as e:
                print(f"  row {row_id} ERROR: {e}", flush=True)
                verdict = "Half-true"
                raw = f"[error: {e}]"

            fout.write(json.dumps({
                "row_id": row_id,
                "gold_label": g["label"],
                "predicted_label": verdict,
                "raw": raw[:200],
                "n_supporting": len(supporting),
                "n_attacking": len(attacking),
            }, ensure_ascii=False) + "\n")
            fout.flush()
            os.fsync(fout.fileno())

            n_done += 1
            if n_done % 10 == 0:
                elapsed = time.time() - t0
                rate = n_done / max(elapsed, 1e-6)
                eta = (len(todo) - n_done) / max(rate, 1e-6) / 60
                print(f"  {n_done}/{len(todo)}  "
                      f"({elapsed:.0f}s, {rate:.2f}/s, ETA {eta:.1f} min)",
                      flush=True)

    # Compute F1
    try:
        from src.evaluate import compute_metrics
    except Exception:
        print("[ablation] src.evaluate not importable — printing raw counts",
              flush=True)
        return

    y_true, y_pred = [], []
    with open(OUT) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            y_true.append(r["gold_label"])
            y_pred.append(r["predicted_label"])
    m = compute_metrics(y_true, y_pred)

    print("\n=== DIRECT-FROM-STRUCTURE ABLATION RESULT ===", flush=True)
    print(f"  n = {len(y_true)}", flush=True)
    print(f"  6-way macro-F1:    {m['macro_f1']:.3f}", flush=True)
    print(f"  6-way accuracy:    {m['accuracy']:.3f}", flush=True)
    print(f"  within-1:          {m['within_1_accuracy']:.3f}", flush=True)
    print(f"  3-way macro-F1:    {m['threeway']['macro_f1']:.3f}", flush=True)
    print(f"\n  vs Phase 1 with retrieval (gpt-oss-120b parser): 0.254",
          flush=True)
    print(f"  vs flat-RAG (no parser):                          0.114",
          flush=True)


if __name__ == "__main__":
    main()
