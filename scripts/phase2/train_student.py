"""Train the Phase 2 student on combined gold+silver data.

Reads {output_dir}/gold.jsonl and {output_dir}/silver.jsonl, merges
them, runs the configured trainer (dummy or HF), saves the model to
student_output_dir.

Usage:
    python -m scripts.phase2.train_student --config configs/phase2_dummy.yaml
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.phase2.config import load_phase2_config
from src.phase2.dataset import read_jsonl
from src.phase2.student import build_student


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()

    cfg = load_phase2_config(args.config)
    data_dir = Path(cfg.dataset.output_dir)
    gold_path = data_dir / "gold.jsonl"
    silver_path = data_dir / "silver.jsonl"

    records = []
    if gold_path.exists():
        records.extend(read_jsonl(gold_path))
    if silver_path.exists() and silver_path.stat().st_size > 0:
        records.extend(read_jsonl(silver_path))
    if not records:
        raise RuntimeError(
            f"No training data found in {data_dir}. "
            "Run prepare_datasets.py and annotate_silver.py first.")

    print(f"[train] loaded {len(records)} records "
          f"(student={cfg.student.backend}, base={cfg.student.base_model})")

    student = build_student(cfg.student)
    out = student.train(records, cfg.student_output_dir)
    print(f"[train] saved student to {out}")


if __name__ == "__main__":
    main()
