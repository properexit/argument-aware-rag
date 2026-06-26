"""Phase 2-β training orchestrator.

Loads the unified-corpus JSONLs from phase2_data/unified/, excludes any
sources you pass via --exclude (default: liararg, since LIARArg is the
held-out integration target), then runs HFTrainer on the rest.

Different from train_student.py: that script reads {output_dir}/gold.jsonl
and {output_dir}/silver.jsonl. This one reads the unified directory
directly — which is how Phase 2-β data is organised (one JSONL per
source × split).

Usage:
    python -m scripts.phase2.train_phase2_beta \\
        --config configs/phase2_beta_qwen1.5b.yaml

To include LIARArg train (e.g. for a Phase 2-β-v2 ablation):
        --exclude  (pass empty)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.phase2.config import load_phase2_config
from src.phase2.dataset import load_unified_corpus
from src.phase2.student import build_student


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--exclude", default="liararg",
                   help="Comma-separated source names to exclude from training. "
                        "Default: 'liararg' (it's the held-out integration target).")
    p.add_argument("--unified-dir", default="",
                   help="Override the unified-corpus directory. Defaults to "
                        "the config's dataset.output_dir.")
    args = p.parse_args()

    cfg = load_phase2_config(args.config)
    exclude = tuple(s.strip() for s in args.exclude.split(",") if s.strip())
    unified_dir = args.unified_dir or cfg.dataset.output_dir
    print(f"[train-β] config: {args.config}")
    print(f"[train-β] unified dir: {unified_dir}")
    print(f"[train-β] excluding sources: {exclude or '(none)'}")

    records = load_unified_corpus(unified_dir, exclude_sources=exclude)
    if not records:
        raise RuntimeError(
            f"No records loaded from {unified_dir}. "
            f"Run the dataset-loader notebook cells first.")

    # Quick split summary
    from collections import Counter
    by_split = Counter(r.get("split", "?") for r in records)
    print(f"[train-β] split distribution: {dict(by_split)}")

    if by_split.get("train", 0) == 0:
        raise RuntimeError("No 'train' records found — check JSONL split labels.")

    print(f"[train-β] building student: {cfg.student.backend} "
          f"({cfg.student.base_model})")
    student = build_student(cfg.student)
    out = student.train(records, cfg.student_output_dir)
    print(f"[train-β] saved student to {out}")


if __name__ == "__main__":
    main()
