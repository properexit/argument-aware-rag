"""Prepare the LIARArg dataset: filter, parse, split, save.

Two split modes:
  - Default: stratified random split of quality-filtered LIARArg
        python scripts/prepare_data.py --csv data/data.csv

  - LIAR-standard split: align with the canonical LIAR train/valid/test
    partitions (Wang 2017) by intersecting LIARArg's quality-filtered rows
    with each LIAR split's row IDs. Required for fair comparison with
    prior LIAR-benchmark literature.
        # First download LIAR TSVs once:
        # curl -sL https://www.cs.ucsb.edu/~william/data/liar_dataset.zip \
        #   -o /tmp/liar/liar.zip
        # unzip -d /tmp/liar /tmp/liar/liar.zip
        python scripts/prepare_data.py --csv data/data.csv \\
            --liar-split --liar-dir /tmp/liar \\
            --out-dir data_liar
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


LIAR_COLS = [
    "id", "label", "statement", "subject", "speaker", "speaker_job",
    "state", "party", "barely_true_cnt", "false_cnt", "half_true_cnt",
    "mostly_true_cnt", "pants_fire_cnt", "context", "justification",
]


def _liar_split_ids(liar_dir: str) -> dict[str, set[int]]:
    """Return {'train': {ids}, 'val': {ids}, 'test': {ids}} from LIAR TSVs."""
    import pandas as pd
    out: dict[str, set[int]] = {}
    for name, fname in (("train", "train.tsv"),
                        ("val",   "valid.tsv"),
                        ("test",  "test.tsv")):
        path = Path(liar_dir) / fname
        if not path.exists():
            raise FileNotFoundError(
                f"LIAR file not found: {path}. "
                f"Download from https://www.cs.ucsb.edu/~william/data/liar_dataset.zip"
            )
        df = pd.read_csv(path, sep="\t", header=None,
                         names=LIAR_COLS, on_bad_lines="skip")
        # LIAR IDs look like "9433.json" — strip the suffix and cast.
        ids = df["id"].astype(str).str.replace(".json", "", regex=False)
        out[name] = set(int(i) for i in ids if i.isdigit())
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--csv", required=True, help="Path to data.csv")
    ap.add_argument("--out-dir", default=str(PROJECT_ROOT / "data"))
    ap.add_argument("--test-frac", type=float, default=0.15,
                    help="(default mode only) test fraction")
    ap.add_argument("--val-frac", type=float, default=0.10,
                    help="(default mode only) val fraction")
    ap.add_argument("--seed", type=int, default=42,
                    help="(default mode only) random seed")
    ap.add_argument("--keep-low-quality", action="store_true",
                    help="Skip the quality filter (default: drop noisy rows)")
    ap.add_argument("--liar-split", action="store_true",
                    help="Use LIAR's canonical train/valid/test split "
                         "instead of a stratified random split. Requires "
                         "--liar-dir.")
    ap.add_argument("--liar-dir", default="/tmp/liar",
                    help="Directory containing train.tsv, valid.tsv, test.tsv "
                         "from the LIAR dataset (default: /tmp/liar).")
    args = ap.parse_args()

    print(f"[prepare_data] loading {args.csv}")
    rows = load_liararg(args.csv, filter_low_quality=not args.keep_low_quality)
    print(f"[prepare_data] kept {len(rows)} rows after quality filter")

    if args.liar_split:
        # ------------------------------------------------------------
        # LIAR-standard split: intersect quality-filtered LIARArg rows
        # with LIAR's official train/valid/test partitions.
        # ------------------------------------------------------------
        print(f"[prepare_data] loading LIAR splits from {args.liar_dir}")
        liar_ids = _liar_split_ids(args.liar_dir)
        for name in ("train", "val", "test"):
            print(f"[prepare_data]   LIAR {name}: {len(liar_ids[name])} ids")

        split: dict[str, list] = {"train": [], "val": [], "test": []}
        for r in rows:
            for name in ("train", "val", "test"):
                if r.id in liar_ids[name]:
                    split[name].append(r)
                    break  # row goes to exactly one split
        for name, rs in split.items():
            print(f"[prepare_data] LIAR-aligned {name}: {len(rs)} rows")
    else:
        # ------------------------------------------------------------
        # Default: stratified random split (Phase 1 development mode).
        # ------------------------------------------------------------
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
