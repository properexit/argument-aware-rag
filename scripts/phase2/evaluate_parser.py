"""Evaluate the trained student on the test split.

Loads the trained model, runs predict() on every test record, computes
component-level and relation-level F1, writes metrics to disk.

Usage:
    python -m scripts.phase2.evaluate_parser --config configs/phase2_dummy.yaml
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.phase2.config import load_phase2_config
from src.phase2.dataset import read_jsonl
from src.phase2.student import build_student
from src.phase2.evaluate import evaluate_corpus


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--threshold", type=float, default=0.5,
                   help="Token-overlap threshold for component matching.")
    args = p.parse_args()

    cfg = load_phase2_config(args.config)
    data_dir = Path(cfg.dataset.output_dir)

    records = []
    for fname in ("gold.jsonl", "silver.jsonl"):
        path = data_dir / fname
        if path.exists() and path.stat().st_size > 0:
            records.extend(read_jsonl(path))
    test_recs = [r for r in records if r.get("split") == "test"]
    if not test_recs:
        raise RuntimeError(f"No test-split records in {data_dir}.")

    print(f"[eval] running student on {len(test_recs)} test records")
    student = build_student(cfg.student)
    student.load(cfg.student_output_dir)

    preds = []
    for i, r in enumerate(test_recs, 1):
        pred, _ = student.predict(r["input"])
        preds.append(pred)
        if i % 25 == 0:
            print(f"  [eval] {i}/{len(test_recs)}")

    metrics = evaluate_corpus(test_recs, preds, threshold=args.threshold)
    out_path = Path(cfg.student_output_dir) / "phase2_metrics.json"
    out_path.write_text(json.dumps(metrics, indent=2))

    print(f"[eval] component macro-F1: {metrics['macro_component_f1']:.3f}")
    print(f"[eval] relation F1:        {metrics['relation_f1']['f1']:.3f}")
    print(f"[eval] by domain:")
    for d, s in metrics["by_domain"].items():
        print(f"  - {d}: n={s['n']}, relation-F1={s['macro_relation_f1']:.3f}")
    print(f"[eval] saved metrics to {out_path}")


if __name__ == "__main__":
    main()
