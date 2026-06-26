"""Merge a partial-re-run predictions.jsonl back into a previous full run.

Use case (Phase 2-α): yesterday's run_pipeline produced verdicts for all 425
test rows, but 56 of those used the parser's defensive single-claim fallback
(missing or empty parser predictions). After backfilling the parser
predictions for those 56 rows and re-running Phase 1 with
`--restrict-row-ids` on just those 56, this script:

  1. Loads the OLD predictions.jsonl + predictions_flat.jsonl (425 rows each)
  2. Loads the NEW predictions.jsonl + predictions_flat.jsonl (56 rows each)
  3. Replaces the 56 rows in OLD with the NEW values
  4. Writes merged JSONL files (predictions_merged.jsonl,
     predictions_flat_merged.jsonl)
  5. Calls compute_metrics on the merged files and prints clean metrics

PipelineResult schema in each line (from src/pipeline.py):
    row_id, gold_label, predicted_label, ... (plus other fields)

Usage:
    python scripts/merge_phase2alpha_predictions.py \
        --old-dir outputs/results_phase2alpha_llama70b \
        --new-dir outputs/results_phase2alpha_llama70b_backfill
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluate import compute_metrics


def read_predictions(path: Path) -> dict[int, dict]:
    """Return {row_id: prediction_dict} from a predictions JSONL."""
    out: dict[int, dict] = {}
    if not path.exists():
        return out
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            out[int(rec["row_id"])] = rec
    return out


def merge_and_write(old_path: Path, new_path: Path, out_path: Path) -> dict[int, dict]:
    old = read_predictions(old_path)
    new = read_predictions(new_path)
    print(f"[merge] {old_path.name}: old={len(old)}  new={len(new)}")

    overlap = set(old) & set(new)
    only_new = set(new) - set(old)
    if only_new:
        print(f"  + {len(only_new)} row_ids in new but not in old (added)")
    print(f"  + {len(overlap)} row_ids overlap (replaced by new values)")

    merged = dict(old)
    for rid, rec in new.items():
        merged[rid] = rec

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for rid in sorted(merged):
            f.write(json.dumps(merged[rid], ensure_ascii=False) + "\n")
    print(f"  → wrote {len(merged)} rows to {out_path.name}")
    return merged


def metrics_from(records: dict[int, dict], label: str) -> None:
    """Compute and print metrics from a {row_id: prediction_dict} map."""
    if not records:
        print(f"[metrics:{label}] no records, skipping")
        return
    y_true = []
    y_pred = []
    for rid in sorted(records):
        rec = records[rid]
        if "gold_label" not in rec or "predicted_label" not in rec:
            print(f"  [warning] row {rid} missing gold/predicted label, skipping")
            continue
        y_true.append(rec["gold_label"])
        y_pred.append(rec["predicted_label"])

    m = compute_metrics(y_true, y_pred)
    print()
    print(f"=== {label} (n={len(y_true)}) ===")
    print(f"  6-way macro-F1:   {m['macro_f1']:.3f}")
    print(f"  6-way acc:        {m['accuracy']:.3f}")
    print(f"  within-1 acc:     {m['within_1_accuracy']:.3f}")
    print(f"  MAE on 0..5:      {m['mae_on_scale']:.3f}")
    print(f"  3-way macro-F1:   {m['threeway']['macro_f1']:.3f}")
    print(f"  3-way acc:        {m['threeway']['accuracy']:.3f}")
    print(f"  extreme F1:       {m['extreme_macro_f1']:.3f}  "
          f"within-1: {m['extreme_within_1_accuracy']:.3f}")
    print(f"  intermediate F1:  {m['intermediate_macro_f1']:.3f}  "
          f"within-1: {m['intermediate_within_1_accuracy']:.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old-dir", required=True,
                    help="Directory with yesterday's predictions.jsonl + "
                         "predictions_flat.jsonl (full 425-row run).")
    ap.add_argument("--new-dir", required=True,
                    help="Directory with today's partial-re-run files "
                         "(produced by run_pipeline --restrict-row-ids).")
    ap.add_argument("--out-dir", default="",
                    help="Where to write the merged files. Defaults to "
                         "<old-dir>/merged/.")
    args = ap.parse_args()

    old_dir = Path(args.old_dir)
    new_dir = Path(args.new_dir)
    out_dir = Path(args.out_dir) if args.out_dir else old_dir / "merged"
    out_dir.mkdir(parents=True, exist_ok=True)

    # arg-aware
    merged_arg = merge_and_write(
        old_dir / "predictions.jsonl",
        new_dir / "predictions.jsonl",
        out_dir / "predictions.jsonl",
    )
    # flat-RAG (may be skipped if --skip-flat was used)
    merged_flat = merge_and_write(
        old_dir / "predictions_flat.jsonl",
        new_dir / "predictions_flat.jsonl",
        out_dir / "predictions_flat.jsonl",
    )

    metrics_from(merged_arg, "arg-aware (Phase 2-α merged)")
    metrics_from(merged_flat, "flat-RAG (merged)")


if __name__ == "__main__":
    main()
