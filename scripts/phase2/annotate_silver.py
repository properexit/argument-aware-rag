"""Run the teacher on un-annotated ARIES rows to produce silver labels.

Reads aries_clean_path, samples N rows per source, sends each to the
teacher (dummy or Groq), writes a silver.jsonl alongside gold.jsonl.

The teacher's annotate_all() is resumable — Ctrl+C and re-run picks
up exactly where it left off.

Usage:
    python -m scripts.phase2.annotate_silver --config configs/phase2_dummy.yaml
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.phase2.config import load_phase2_config
from src.phase2.dataset import load_aries_for_silver
from src.phase2.teacher import build_teacher


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()

    cfg = load_phase2_config(args.config)
    out_dir = Path(cfg.dataset.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    silver_path = out_dir / "silver.jsonl"

    rows = load_aries_for_silver(
        cfg.dataset.aries_clean_path,
        cfg.dataset.silver_sources,
        cfg.dataset.samples_per_silver_source,
        cfg.dataset.seed,
    )
    if not rows:
        print("[annotate] no rows to annotate (aries_clean_path empty or "
              "silver_sources empty). Skipping.")
        # Write empty silver so downstream scripts find a valid file
        silver_path.touch()
        return

    print(f"[annotate] {len(rows)} rows × teacher={cfg.teacher.backend} → {silver_path}")
    teacher = build_teacher(cfg.teacher)
    teacher.annotate_all(rows, silver_path, resume=True)
    # Release GPU memory if the teacher held any (LocalHFTeacher) so
    # train_student.py can take the GPU cleanly afterwards.
    if hasattr(teacher, "release"):
        teacher.release()
    print(f"[annotate] done. silver written to {silver_path}")


if __name__ == "__main__":
    main()
