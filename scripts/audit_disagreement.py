"""Per-claim disagreement audit between arg-aware and flat-RAG predictions.

For every test claim, categorise the (arg-aware, flat-RAG) prediction pair
relative to the gold label and write a human-readable report plus a CSV.

Categories:
  both_correct          both pipelines hit the gold label
  both_wrong_same       both miss, but agree with each other (no signal)
  both_wrong_different  both miss, disagree (LLM noise / hard claim)
  arg_only_right        arg-aware correct, flat-RAG wrong (the argument-
                        aware advantage cases)
  flat_only_right       flat-RAG correct, arg-aware wrong (where role
                        targeting actively hurt)
  off_by_one            both close but off by one bucket on the scale

Usage:
    python scripts/audit_disagreement.py
    python scripts/audit_disagreement.py --results-dir outputs/results
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

LABEL_ORDER = ["True", "Mostly-true", "Half-true",
               "Barely-true", "False", "Pants-fire"]
LABEL_INDEX = {lab: i for i, lab in enumerate(LABEL_ORDER)}


def _label_distance(a: str, b: str) -> int | None:
    """Bucket distance between two labels on the 6-point scale, or None."""
    if a not in LABEL_INDEX or b not in LABEL_INDEX:
        return None
    return abs(LABEL_INDEX[a] - LABEL_INDEX[b])


def _categorise(gold: str, arg: str, flat: str) -> str:
    arg_right = arg == gold
    flat_right = flat == gold
    if arg_right and flat_right:
        return "both_correct"
    if arg_right and not flat_right:
        return "arg_only_right"
    if flat_right and not arg_right:
        return "flat_only_right"
    if arg == flat:
        return "both_wrong_same"
    return "both_wrong_different"


def _is_off_by_one(gold: str, pred: str) -> bool:
    d = _label_distance(gold, pred)
    return d is not None and d == 1


def _load(path: Path) -> dict[int, dict]:
    out = {}
    with open(path) as f:
        for line in f:
            d = json.loads(line)
            out[d["row_id"]] = d
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir",
                    default=str(PROJECT_ROOT / "outputs" / "results"))
    ap.add_argument("--max-shown-per-category", type=int, default=4)
    args = ap.parse_args()

    arg_path = Path(args.results_dir) / "predictions.jsonl"
    flat_path = Path(args.results_dir) / "predictions_flat.jsonl"
    if not arg_path.exists() or not flat_path.exists():
        print(f"Missing predictions files in {args.results_dir}")
        print(f"  arg-aware: {arg_path.exists()} | flat: {flat_path.exists()}")
        return 1

    arg = _load(arg_path)
    flat = _load(flat_path)
    shared = sorted(set(arg) & set(flat))
    print(f"[audit] {len(shared)} shared claims")

    # ---- categorise each claim
    rows: list[dict] = []
    for rid in shared:
        a = arg[rid]
        f = flat[rid]
        gold = a["gold_label"]
        cat = _categorise(gold, a["predicted_label"], f["predicted_label"])
        rows.append({
            "row_id": rid,
            "gold": gold,
            "arg_pred": a["predicted_label"],
            "flat_pred": f["predicted_label"],
            "category": cat,
            "arg_dist": _label_distance(gold, a["predicted_label"]),
            "flat_dist": _label_distance(gold, f["predicted_label"]),
            "statement": a["statement"],
            "n_queries_arg": len(a.get("queries", [])),
            "arg_rationale": a.get("rationale", ""),
            "flat_rationale": f.get("rationale", ""),
        })

    # ---- summary
    cats = Counter(r["category"] for r in rows)
    n = len(rows)
    print()
    print("=" * 60)
    print("CATEGORY SUMMARY")
    print("=" * 60)
    for c in ("both_correct", "arg_only_right", "flat_only_right",
              "both_wrong_same", "both_wrong_different"):
        share = cats[c] / n if n else 0
        print(f"  {c:24s} {cats[c]:3d}  ({share:.0%})")

    arg_correct = cats["both_correct"] + cats["arg_only_right"]
    flat_correct = cats["both_correct"] + cats["flat_only_right"]
    print(f"\n  arg-aware accuracy:  {arg_correct}/{n} = {arg_correct/n:.2%}")
    print(f"  flat-RAG  accuracy:  {flat_correct}/{n} = {flat_correct/n:.2%}")
    print(f"  net arg-aware lift:  {(arg_correct - flat_correct)/n:+.2%}")

    # ---- off-by-one analysis (where the pipelines are "close")
    arg_off1 = sum(1 for r in rows if r["arg_dist"] == 1)
    flat_off1 = sum(1 for r in rows if r["flat_dist"] == 1)
    arg_within1 = sum(1 for r in rows if r["arg_dist"] is not None and r["arg_dist"] <= 1)
    flat_within1 = sum(1 for r in rows if r["flat_dist"] is not None and r["flat_dist"] <= 1)
    print(f"\n  arg-aware off-by-one count:     {arg_off1}")
    print(f"  flat-RAG  off-by-one count:     {flat_off1}")
    print(f"  arg-aware within-1 accuracy:    {arg_within1}/{n} = {arg_within1/n:.2%}")
    print(f"  flat-RAG  within-1 accuracy:    {flat_within1}/{n} = {flat_within1/n:.2%}")

    # ---- prediction distributions
    print("\n  prediction distributions:")
    arg_dist = Counter(r["arg_pred"] for r in rows)
    flat_dist = Counter(r["flat_pred"] for r in rows)
    gold_dist = Counter(r["gold"] for r in rows)
    print(f"    {'label':14s}  gold   arg   flat")
    for lab in LABEL_ORDER:
        print(f"    {lab:14s}  {gold_dist[lab]:4d}  {arg_dist[lab]:4d}  {flat_dist[lab]:4d}")

    # ---- show example claims for each disagreement category
    print()
    print("=" * 60)
    print("DISAGREEMENT EXAMPLES")
    print("=" * 60)
    for category in ("arg_only_right", "flat_only_right",
                     "both_wrong_different"):
        examples = [r for r in rows if r["category"] == category]
        print(f"\n--- {category} ({len(examples)} total) ---")
        for r in examples[:args.max_shown_per_category]:
            print(f"\n  id={r['row_id']}  gold={r['gold']}")
            print(f"    arg={r['arg_pred']}   flat={r['flat_pred']}")
            print(f"    claim: {r['statement'][:160]}"
                  f"{'...' if len(r['statement']) > 160 else ''}")
            if category == "arg_only_right" and r["arg_rationale"]:
                rat = r["arg_rationale"].replace("\n", " ")
                print(f"    arg-rationale: {rat[:200]}"
                      f"{'...' if len(rat) > 200 else ''}")
            elif category == "flat_only_right" and r["flat_rationale"]:
                rat = r["flat_rationale"].replace("\n", " ")
                print(f"    flat-rationale: {rat[:200]}"
                      f"{'...' if len(rat) > 200 else ''}")

    # ---- write CSV
    out_csv = Path(args.results_dir) / "audit.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "row_id", "gold", "arg_pred", "flat_pred", "category",
            "arg_dist", "flat_dist", "n_queries_arg", "statement",
        ])
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in w.fieldnames})

    # ---- write a focused Markdown report of the most interesting cases
    out_md = Path(args.results_dir) / "audit.md"
    with open(out_md, "w") as f:
        f.write("# Disagreement audit\n\n")
        f.write(f"- Claims compared: {n}\n")
        f.write(f"- arg-aware accuracy: {arg_correct}/{n} ({arg_correct/n:.0%})\n")
        f.write(f"- flat-RAG accuracy:  {flat_correct}/{n} ({flat_correct/n:.0%})\n")
        f.write(f"- net arg-aware lift: {(arg_correct - flat_correct)/n:+.0%}\n\n")
        f.write("## Category breakdown\n\n")
        for c in ("both_correct", "arg_only_right", "flat_only_right",
                  "both_wrong_same", "both_wrong_different"):
            f.write(f"- **{c}**: {cats[c]}\n")
        f.write("\n## Cases where arg-aware wins\n\n")
        for r in (rr for rr in rows if rr["category"] == "arg_only_right"):
            f.write(f"### id={r['row_id']} — gold *{r['gold']}*\n")
            f.write(f"- arg-aware predicted **{r['arg_pred']}** ✓\n")
            f.write(f"- flat-RAG predicted **{r['flat_pred']}**\n")
            f.write(f"- claim: {r['statement']}\n")
            if r["arg_rationale"]:
                f.write(f"- arg-rationale: {r['arg_rationale']}\n")
            f.write("\n")
        f.write("## Cases where flat-RAG wins\n\n")
        for r in (rr for rr in rows if rr["category"] == "flat_only_right"):
            f.write(f"### id={r['row_id']} — gold *{r['gold']}*\n")
            f.write(f"- arg-aware predicted **{r['arg_pred']}**\n")
            f.write(f"- flat-RAG predicted **{r['flat_pred']}** ✓\n")
            f.write(f"- claim: {r['statement']}\n")
            if r["flat_rationale"]:
                f.write(f"- flat-rationale: {r['flat_rationale']}\n")
            f.write("\n")

    print(f"\n[audit] wrote {out_csv}")
    print(f"[audit] wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
