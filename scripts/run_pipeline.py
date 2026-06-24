"""Run the Phase 1 pipeline on a sample of the test set.

Reports macro-F1 for both the argument-aware pipeline and the flat-RAG baseline.

Usage:
    python scripts/run_pipeline.py --n 50 --verifier stub
    python scripts/run_pipeline.py --n 50 --verifier ollama --ollama-model llama3.1:8b-instruct
"""
import argparse
import json
import os
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_split
from src.arg_parser import GoldArgParser
from src.retriever import HybridRetriever
from src.reranker import RoleAwareReranker
from src.verifier import VerdictSynthesiser
from src.pipeline import ArgAwareRAGPipeline
from src.evaluate import compute_metrics


def _stratified_sample(rows, n, seed=42):
    """Stratified-by-label sample so the small eval keeps all 6 labels represented."""
    by_label = {}
    for r in rows:
        by_label.setdefault(r.label, []).append(r)
    rng = random.Random(seed)
    out = []
    if n >= len(rows):
        return list(rows)
    per_label = max(1, n // len(by_label))
    for lab, rs in by_label.items():
        rng.shuffle(rs)
        out.extend(rs[:per_label])
    # Top up to exactly n if we under-sampled
    extras = [r for r in rows if r not in out]
    rng.shuffle(extras)
    while len(out) < n and extras:
        out.append(extras.pop())
    return out[:n]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(PROJECT_ROOT / "data"))
    ap.add_argument("--index-dir", default=str(PROJECT_ROOT / "outputs" / "index"))
    ap.add_argument("--out-dir", default=str(PROJECT_ROOT / "outputs" / "results"))
    ap.add_argument("--n", type=int, default=50, help="Number of test claims to score")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--verifier", default="stub", choices=["stub", "ollama"])
    ap.add_argument("--ollama-base-url", default="http://localhost:11434")
    ap.add_argument("--ollama-model", default="llama3.1:8b-instruct")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--no-reranker", action="store_true")
    ap.add_argument("--top-k-per-query", type=int, default=20)
    ap.add_argument("--final-top-k-per-role", type=int, default=5)
    ap.add_argument("--skip-flat", action="store_true",
                    help="Skip the flat-RAG baseline run (faster)")
    ap.add_argument("--no-structural-prior", action="store_true",
                    help="Disable passing the stub-derived structural prior "
                         "to the LLM (default: pass it)")
    ap.add_argument("--soft-prior-threshold", type=int, default=3,
                    help="Inject a discrete structural prior only when "
                         "|n_sup - n_atk| >= this threshold. Set to 0 for "
                         "the old hard-prior behaviour, or to 99 to disable "
                         "the discrete prior entirely (default: 3).")
    ap.add_argument("--prior-mode", default="discrete",
                    choices=["discrete", "probabilistic", "none"],
                    help="How to express the structural prior to the LLM. "
                         "'discrete' = single label (or 'uncertain'); "
                         "'probabilistic' = 6-label probability distribution "
                         "from role-fit scores; 'none' = no prior at all.")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    print("[run_pipeline] loading split")
    split = load_split(args.data_dir)
    test_rows = split["test"]
    sample = _stratified_sample(test_rows, args.n, seed=args.seed)
    print(f"[run_pipeline] evaluating on {len(sample)} test claims")

    print("[run_pipeline] loading retrieval index")
    retriever = HybridRetriever.load(args.index_dir, device=args.device)

    reranker = None
    if not args.no_reranker:
        print("[run_pipeline] loading re-ranker")
        reranker = RoleAwareReranker(device=args.device)

    verifier = VerdictSynthesiser(
        backend=args.verifier,
        ollama_base_url=args.ollama_base_url,
        ollama_model=args.ollama_model,
        use_structural_prior=not args.no_structural_prior,
        soft_prior_threshold=args.soft_prior_threshold,
        prior_mode=args.prior_mode,
    )

    # Parser needs lookup over ALL rows (train+val+test) so it can dereference
    # any row id.
    all_rows = {r.id: r for rs in split.values() for r in rs}
    parser = GoldArgParser(all_rows)

    pipeline = ArgAwareRAGPipeline(
        parser=parser,
        retriever=retriever,
        reranker=reranker,
        verifier=verifier,
        top_k_per_query=args.top_k_per_query,
        final_top_k_per_role=args.final_top_k_per_role,
    )

    arg_aware_preds = []
    flat_preds = []
    arg_results = []
    flat_results = []
    y_true = []

    # ── Incremental save: skip already-done claims on resume and write
    #    each prediction to disk immediately so a crash never loses progress.
    pred_path = os.path.join(args.out_dir, "predictions.jsonl")
    flat_path = os.path.join(args.out_dir, "predictions_flat.jsonl")
    done_ids: set[int] = set()
    if os.path.exists(pred_path):
        with open(pred_path) as f:
            for line in f:
                try:
                    done_ids.add(int(json.loads(line)["row_id"]))
                except (json.JSONDecodeError, KeyError, ValueError):
                    pass
        if done_ids:
            print(f"[run_pipeline] resuming: {len(done_ids)} claims already done "
                  f"in {pred_path}")
        # Load existing results so end-of-run metrics span the full union
        with open(pred_path) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    arg_results.append(r)
                    arg_aware_preds.append(r["predicted_label"])
                    y_true.append(r["gold_label"])
                except (json.JSONDecodeError, KeyError):
                    pass
        if not args.skip_flat and os.path.exists(flat_path):
            with open(flat_path) as f:
                for line in f:
                    try:
                        r = json.loads(line)
                        flat_results.append(r)
                        flat_preds.append(r["predicted_label"])
                    except (json.JSONDecodeError, KeyError):
                        pass

    # Open for APPEND, never overwrite existing partial work
    pred_f = open(pred_path, "a")
    flat_f = open(flat_path, "a") if not args.skip_flat else None

    t0 = time.time()
    n_done_this_session = 0
    for i, row in enumerate(sample, 1):
        if row.id in done_ids:
            continue                                # skip on resume
        y_true.append(row.label)
        res = pipeline.run(row)
        arg_aware_preds.append(res.predicted_label)
        d = asdict(res)
        arg_results.append(d)
        pred_f.write(json.dumps(d) + "\n")          # incremental flush
        pred_f.flush()
        os.fsync(pred_f.fileno())

        if not args.skip_flat:
            res_f = pipeline.run_flat(row)
            flat_preds.append(res_f.predicted_label)
            df = asdict(res_f)
            flat_results.append(df)
            flat_f.write(json.dumps(df) + "\n")
            flat_f.flush()
            os.fsync(flat_f.fileno())

        n_done_this_session += 1
        if i % 5 == 0 or i == len(sample):
            elapsed = time.time() - t0
            print(f"  [{i}/{len(sample)}] (+{n_done_this_session} new) "
                  f"elapsed {elapsed:.1f}s")

    pred_f.close()
    if flat_f is not None:
        flat_f.close()

    # Metrics
    arg_metrics = compute_metrics(y_true, arg_aware_preds)
    out_metrics = {
        "config": vars(args),
        "arg_aware": arg_metrics,
    }
    if not args.skip_flat:
        flat_metrics = compute_metrics(y_true, flat_preds)
        out_metrics["flat"] = flat_metrics

    metrics_path = os.path.join(args.out_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(out_metrics, f, indent=2)
    def _fmt(m: dict, name: str) -> str:
        tw = m["threeway"]
        return (
            f"[run_pipeline] {name:10s}"
            f"  6-way macro-F1 = {m['macro_f1']:.3f}"
            f"  acc = {m['accuracy']:.3f}"
            f"  within-1 = {m['within_1_accuracy']:.3f}"
            f"  MAE = {m['mae_on_scale']:.2f}"
            f"\n             "
            f"  3-way:        macro-F1={tw['macro_f1']:.3f}"
            f"  acc={tw['accuracy']:.3f}"
            f"\n             "
            f"  extreme:      F1={m['extreme_macro_f1']:.3f}"
            f"  within-1={m['extreme_within_1_accuracy']:.3f}"
            f"\n             "
            f"  intermediate: F1={m['intermediate_macro_f1']:.3f}"
            f"  within-1={m['intermediate_within_1_accuracy']:.3f}"
        )

    print()
    print(_fmt(arg_metrics, "arg-aware"))
    if not args.skip_flat:
        print(_fmt(flat_metrics, "flat-RAG"))
        # Side-by-side deltas
        d_w1 = arg_metrics["within_1_accuracy"] - flat_metrics["within_1_accuracy"]
        d_3w = arg_metrics["threeway"]["macro_f1"] - flat_metrics["threeway"]["macro_f1"]
        d_3a = arg_metrics["threeway"]["accuracy"] - flat_metrics["threeway"]["accuracy"]
        print(f"\n[run_pipeline] arg-aware vs flat:"
              f"  within-1 lift {d_w1:+.3f}"
              f"  ·  3-way F1 lift {d_3w:+.3f}"
              f"  ·  3-way acc lift {d_3a:+.3f}")
    print(f"[run_pipeline] wrote {pred_path}")
    print(f"[run_pipeline] wrote {metrics_path}")

    # Worked example: the test row with the most argument relations
    best = max(sample, key=lambda r: r.n_support + r.n_attack)
    if best.n_support + best.n_attack > 0:
        ex = next(r for r in arg_results if r["row_id"] == best.id)
        we_path = os.path.join(args.out_dir, "worked_example.md")
        with open(we_path, "w") as f:
            f.write(_format_worked_example(ex, best.label))
        print(f"[run_pipeline] wrote worked example to {we_path}")
    return 0


def _format_worked_example(ex: dict, gold: str) -> str:
    lines = ["# Worked example\n"]
    lines.append(f"**Claim** ({ex['statement']!r})\n")
    lines.append(f"- Gold label: **{gold}**")
    lines.append(f"- Predicted label: **{ex['predicted_label']}**")
    lines.append(f"- Rationale: {ex['rationale']}\n")
    lines.append("## Role-targeted queries\n")
    for q in ex["queries"]:
        lines.append(f"- **{q['role']}** (kept {q['n_kept']}/{q['n_retrieved']}): "
                     f"premise = {q['premise_text']!r}")
        lines.append(f"  - query: {q['query_text']}")
    lines.append("\n## Evidence by role\n")
    for role, evs in ex["role_evidence"].items():
        lines.append(f"### {role} ({len(evs)} passages)\n")
        for ev in evs:
            lines.append(f"- role_fit={ev['role_fit']:.2f} nli={ev['nli_label']} "
                         f"pid={ev['passage_id']}")
            lines.append(f"  > {ev['text'][:400]}{'...' if len(ev['text'])>400 else ''}\n")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
