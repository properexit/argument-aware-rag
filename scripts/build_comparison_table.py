"""Aggregate every results directory into one comparison table.

Walks outputs/results_liar/ and outputs/baselines/* (and any other
directory containing both predictions.jsonl and run_config.json or
metrics.json), recomputes metrics, and prints a comparison table that
can be pasted straight into the paper.

Usage:
    python scripts/build_comparison_table.py
    python scripts/build_comparison_table.py --markdown    # markdown out
    python scripts/build_comparison_table.py --csv out.csv # CSV out
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluate import compute_metrics


def _derive_label(run_dir: Path, cfg: dict) -> str:
    """Build a human-readable label from the actual model name in the
    config, falling back to the directory name. Filters out the
    'qwen14b_zeroshot' hardcoded name (was a script bug that affected
    early runs of llama3.1:8b and mistral on the same script)."""
    model = cfg.get("model", "")
    name = cfg.get("name", "")
    dir_name = run_dir.name

    # Prefer model id when it's specific
    if model:
        # Determine the run flavour from name/dir
        if "oracle" in name.lower() or "oracle" in dir_name.lower():
            flavour = " + oracle justification"
        elif "zeroshot" in name.lower() or "zeroshot" in dir_name.lower():
            flavour = " zero-shot"
        else:
            flavour = ""
        return f"{model}{flavour}"

    # Fallbacks for main pipeline runs (which don't write a run_config.json)
    if "results_liar" in dir_name:
        return "arg-aware (main, LIAR-aligned)"
    if "results" in dir_name and "liar" not in dir_name:
        return "arg-aware (main, stratified)"
    return dir_name


def _is_excluded(run_dir: Path) -> bool:
    """Skip snapshots and smoke tests for the final table."""
    name = run_dir.name.lower()
    return ("_final" in name or "snapshot" in name or
            "smoketest" in name or "smoke_test" in name)


def _load_run(run_dir: Path, preds_filename: str = "predictions.jsonl") -> dict | None:
    """Load one run's predictions + config + recompute metrics."""
    preds_path = run_dir / preds_filename
    if not preds_path.exists():
        return None
    if _is_excluded(run_dir):
        return None

    y_true, y_pred = [], []
    with open(preds_path) as f:
        for line in f:
            d = json.loads(line)
            y_true.append(d["gold_label"])
            y_pred.append(d["predicted_label"] or "UNKNOWN")

    m = compute_metrics(y_true, y_pred)

    cfg_path = run_dir / "run_config.json"
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
    label = _derive_label(run_dir, cfg)

    # Flat-RAG predictions live alongside arg-aware predictions in the
    # main pipeline run; rename the row so the comparison is legible.
    if preds_filename == "predictions_flat.jsonl":
        if "LIAR-aligned" in label:
            label = "flat-RAG (baseline, LIAR-aligned)"
        elif "stratified" in label:
            label = "flat-RAG (baseline, stratified)"
        else:
            label = f"flat-RAG: {label}"

    return {
        "label": label,
        "n": m["n"],
        "model": cfg.get("model", "—"),
        "backend": cfg.get("backend", "—"),
        "acc_6w": m["accuracy"],
        "macro_f1_6w": m["macro_f1"],
        "within_1": m["within_1_accuracy"],
        "mae": m["mae_on_scale"],
        "acc_3w": m["threeway"]["accuracy"],
        "macro_f1_3w": m["threeway"]["macro_f1"],
        "mixed_f1": m["threeway"]["per_bucket"]["mixed"]["f1"],
        "run_dir": str(run_dir.relative_to(PROJECT_ROOT)),
    }


def _walk_runs(base: Path) -> list[tuple[Path, str]]:
    """Find directories with predictions files.

    Returns a list of (run_dir, predictions_filename) so we can score
    both `predictions.jsonl` (arg-aware) and `predictions_flat.jsonl`
    (flat-RAG baseline) as separate rows from the same run directory.
    """
    found: list[tuple[Path, str]] = []
    for p in base.rglob("predictions.jsonl"):
        found.append((p.parent, "predictions.jsonl"))
    for p in base.rglob("predictions_flat.jsonl"):
        found.append((p.parent, "predictions_flat.jsonl"))
    return sorted(found, key=lambda t: (str(t[0]), t[1]))


def _print_table(rows: list[dict], markdown: bool = False) -> None:
    cols = [
        ("label",       "Method",            42),
        ("n",           "n",                  4),
        ("backend",     "Backend",            8),
        ("acc_6w",      "6w-acc",             7),
        ("macro_f1_6w", "6w-F1",              7),
        ("within_1",    "within-1",           9),
        ("mae",         "MAE",                5),
        ("acc_3w",      "3w-acc",             7),
        ("macro_f1_3w", "3w-F1",              7),
        ("mixed_f1",    "mixed-F1",           8),
    ]
    sep = " | " if markdown else "  "
    if markdown:
        print(sep.join(f"{h}" for _, h, _ in cols))
        print(sep.join("---" for _ in cols))
    else:
        print(sep.join(f"{h:<{w}}" for _, h, w in cols))
        print(sep.join("-" * w for _, _, w in cols))
    for r in rows:
        def _fmt(key, w):
            v = r[key]
            if v is None:
                return f"{'—':<{w}}" if not markdown else "—"
            if isinstance(v, float):
                s = f"{v:.3f}"
            else:
                s = str(v)
            return f"{s:<{w}}" if not markdown else s
        print(sep.join(_fmt(k, w) for k, _, w in cols))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs-root", default=str(PROJECT_ROOT / "outputs"))
    ap.add_argument("--markdown", action="store_true",
                    help="Print as Markdown table")
    ap.add_argument("--csv", default=None,
                    help="Also save the table as CSV at this path")
    args = ap.parse_args()

    base = Path(args.outputs_root)
    run_targets = _walk_runs(base)
    rows = [_load_run(d, fn) for d, fn in run_targets]
    rows = [r for r in rows if r is not None]
    # Sort: main pipeline runs first (heuristic: directory name contains
    # "results_liar"), then baselines, both by 6-way F1 descending
    def _sort_key(r):
        is_main = "results_liar" in r["run_dir"] and "baseline" not in r["run_dir"]
        return (not is_main, -r["macro_f1_6w"])
    rows.sort(key=_sort_key)

    print(f"\nComparison table over {len(rows)} runs:\n")
    _print_table(rows, markdown=args.markdown)

    if args.csv:
        import csv
        out = Path(args.csv)
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"\nWrote CSV to {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
