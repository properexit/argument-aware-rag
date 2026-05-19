"""Prepare the LIARArg dataset: filter, parse, split, save.

Run once before anything else:
    python scripts/prepare_data.py --csv ../../uploads/data.csv
"""
import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import (
    load_liararg,
    stratified_split,
    save_split,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to data.csv")
    ap.add_argument("--out-dir", default=str(PROJECT_ROOT / "data"))
    ap.add_argument("--test-frac", type=float, default=0.15)
    ap.add_argument("--val-frac", type=float, default=0.10)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--keep-low-quality", action="store_true",
                    help="Skip the quality filter (default: drop noisy rows)")
    args = ap.parse_args()

    print(f"[prepare_data] loading {args.csv}")
    rows = load_liararg(args.csv, filter_low_quality=not args.keep_low_quality)
    print(f"[prepare_data] kept {len(rows)} rows")

    split = stratified_split(
        rows,
        test_frac=args.test_frac,
        val_frac=args.val_frac,
        random_state=args.seed,
    )
    for name, rs in split.items():
        print(f"[prepare_data] {name}: {len(rs)} rows")

    os.makedirs(args.out_dir, exist_ok=True)
    save_split(split, args.out_dir)
    print(f"[prepare_data] wrote splits to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
