"""Run a teacher backend (LocalHFTeacher, HFInferenceTeacher, GroqTeacher,
DummyTeacher) on the LIARArg test split and save the predicted argument
structure per row_id, so it can be plugged into Phase 1's pipeline
without re-invoking the LLM.

Output JSONL schema (one line per row):
    {"row_id": int, "prediction": ArgStructureDict, "reasoning": str}

Resumable: re-running picks up where it stopped, useful when the teacher
hits rate limits mid-run.

Usage:
    python -m scripts.phase2.parse_test_with_teacher \\
        --config configs/phase2_parse_test_qwen7b.yaml \\
        --split test \\
        --output phase2_data_liar/parser_preds_qwen7b.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.phase2.config import load_phase2_config
from src.phase2.dataset import read_jsonl
from src.phase2.teacher import build_teacher


def _input_text_from_row(row: dict) -> str:
    """Choose the text passed to the parser. We prioritise the full article
    (more context for the parser) but fall back to summary then statement."""
    return (
        row.get("full_text")
        or row.get("summary")
        or row.get("statement")
        or ""
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True,
                   help="Phase 2 YAML with the teacher backend configured.")
    p.add_argument("--split", choices=("train", "val", "test"), default="test",
                   help="Which LIARArg split to annotate (default: test).")
    p.add_argument("--output", required=True,
                   help="Output JSONL path. Will be created or resumed.")
    p.add_argument("--max-rows", type=int, default=0,
                   help="Cap rows for quick smoke tests; 0 = no cap.")
    args = p.parse_args()

    cfg = load_phase2_config(args.config)

    # Load the requested split
    data_dir = Path(cfg.dataset.liararg_path)
    if not data_dir.is_dir():
        raise FileNotFoundError(
            f"liararg_path is not a directory: {cfg.dataset.liararg_path}")
    split_path = data_dir / f"{args.split}.jsonl"
    if not split_path.exists():
        raise FileNotFoundError(f"split file not found: {split_path}")
    rows = read_jsonl(split_path)
    if args.max_rows > 0:
        rows = rows[: args.max_rows]
    print(f"[parse] loaded {len(rows)} rows from {split_path}")

    # Resumable: skip rows already in the output
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done_ids: set[int] = set()
    if out_path.exists():
        with open(out_path) as f:
            for line in f:
                try:
                    done_ids.add(int(json.loads(line)["row_id"]))
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
        print(f"[parse] resuming — {len(done_ids)} predictions already done")

    teacher = build_teacher(cfg.teacher)
    print(f"[parse] teacher: {teacher.name} ({cfg.teacher.model or 'default model'})")

    t0 = time.time()
    n_done = 0
    n_failed = 0
    with open(out_path, "a") as fout:
        for i, row in enumerate(rows, 1):
            row_id = int(row.get("id", 0))
            if row_id in done_ids:
                continue
            text = _input_text_from_row(row)
            if not text:
                n_failed += 1
                continue

            structure, reasoning = teacher.annotate(text, source="liararg")
            fout.write(json.dumps({
                "row_id": row_id,
                "prediction": structure,
                "reasoning": reasoning,
            }, ensure_ascii=False) + "\n")
            fout.flush()
            os.fsync(fout.fileno())
            n_done += 1

            if i % 10 == 0:
                elapsed = time.time() - t0
                rate = n_done / max(elapsed, 1)
                eta = (len(rows) - i) / max(rate, 1e-6) / 60
                print(f"  [parse] {i}/{len(rows)}  "
                      f"({n_done} this session, {elapsed:.0f}s, "
                      f"~{rate:.2f}/s, ETA {eta:.1f} min)")

    # Free the GPU (LocalHFTeacher only)
    if hasattr(teacher, "release"):
        teacher.release()

    print(f"[parse] done. {n_done} new predictions written to {out_path} "
          f"({n_failed} skipped for empty text)")


if __name__ == "__main__":
    main()
