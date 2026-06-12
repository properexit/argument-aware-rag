"""Recompute metrics on existing predictions.jsonl / predictions_flat.jsonl
without re-running the pipeline.

Use after extending src/evaluate.py with new metrics (e.g. 3-way collapse).

Usage:
    python scripts/recompute_metrics.py
"""
import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluate import compute_metrics


def _load_pairs(path: Path) -> tuple[list[str], list[str]]:
    y_true, y_pred = [], []
    with open(path) as f:
        for line in f:
            d = json.loads(line)
            y_true.append(d["gold_label"])
            y_pred.append(d["predicted_label"])
    return y_true, y_pred


def _print_block(m: dict, name: str) -> None:
    tw = m["threeway"]
    print(f"\n[{name}]  n = {m['n']}")
    print(f"  6-way:  macro-F1 = {m['macro_f1']:.3f}   "
          f"acc = {m['accuracy']:.3f}   "
          f"within-1 = {m['within_1_accuracy']:.3f}   "
          f"MAE = {m['mae_on_scale']:.2f}")
    print(f"  3-way:  macro-F1 = {tw['macro_f1']:.3f}   "
          f"acc = {tw['accuracy']:.3f}")
    print(f"          per-bucket F1:  "
          f"true-leaning = {tw['per_bucket']['true-leaning']['f1']:.3f}   "
          f"mixed = {tw['per_bucket']['mixed']['f1']:.3f}   "
          f"false-leaning = {tw['per_bucket']['false-leaning']['f1']:.3f}")
    print(f"  extreme:      F1 = {m['extreme_macro_f1']:.3f}   "
          f"within-1 = {m['extreme_within_1_accuracy']:.3f}")
    print(f"  intermediate: F1 = {m['intermediate_macro_f1']:.3f}   "
          f"within-1 = {m['intermediate_within_1_accuracy']:.3f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir",
                    default=str(PROJECT_ROOT / "outputs" / "results"))
    args = ap.parse_args()

    arg_path = Path(args.results_dir) / "predictions.jsonl"
    flat_path = Path(args.results_dir) / "predictions_flat.jsonl"
    if not arg_path.exists():
        print(f"missing: {arg_path}")
        return 1

    y_true_a, y_pred_a = _load_pairs(arg_path)
    arg_m = compute_metrics(y_true_a, y_pred_a)
    _print_block(arg_m, "arg-aware")

    out = {"arg_aware": arg_m}
    if flat_path.exists():
        y_true_f, y_pred_f = _load_pairs(flat_path)
        flat_m = compute_metrics(y_true_f, y_pred_f)
        _print_block(flat_m, "flat-RAG")
        out["flat"] = flat_m

        print("\n[deltas: arg-aware − flat-RAG]")
        print(f"  6-way macro-F1 : {arg_m['macro_f1'] - flat_m['macro_f1']:+.3f}")
        print(f"  6-way accuracy : {arg_m['accuracy'] - flat_m['accuracy']:+.3f}")
        print(f"  within-1       : {arg_m['within_1_accuracy'] - flat_m['within_1_accuracy']:+.3f}")
        print(f"  3-way macro-F1 : {arg_m['threeway']['macro_f1'] - flat_m['threeway']['macro_f1']:+.3f}")
        print(f"  3-way accuracy : {arg_m['threeway']['accuracy'] - flat_m['threeway']['accuracy']:+.3f}")

    metrics_path = Path(args.results_dir) / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {metrics_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
