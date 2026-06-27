"""Batched parser-level eval for Phase 2-β trained students.

Designed to run identically against v1 (Qwen-0.5B full FT) and v2
(Qwen-1.5B + LoRA) so the numbers are directly comparable. Reads
config via --config, model output dir via cfg.student_output_dir.

Uses HFTrainer.predict_batch — much higher GPU util than the per-row
loop used in v1 eval (which sat at 14% util / 60+ min wall).

Usage:
    python -m scripts.phase2.eval_phase2beta_v2 \\
        --config configs/phase2_beta_qwen1.5b_lora.yaml \\
        --cap-per-domain 50 \\
        --batch-size 4
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.phase2.config import load_phase2_config
from src.phase2.student import build_student
from src.phase2.dataset import read_jsonl
from src.phase2.evaluate import evaluate_corpus


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--cap-per-domain", type=int, default=50,
                   help="Max records per held-out test split (0 = all).")
    p.add_argument("--batch-size", type=int, default=4,
                   help="Inference batch size for predict_batch.")
    p.add_argument("--domains", default="microtext,cdcp,abstrct,perspectrum",
                   help="Comma-separated domains to eval. Faster domains first.")
    p.add_argument("--threshold", type=float, default=0.5,
                   help="Token-overlap threshold for component matching.")
    p.add_argument("--out-json", default="",
                   help="Optional path to write summary metrics JSON.")
    args = p.parse_args()

    cfg = load_phase2_config(args.config)
    print(f"[eval-v2] config: {args.config}", flush=True)
    print(f"[eval-v2] model dir: {cfg.student_output_dir}", flush=True)
    print(f"[eval-v2] cap={args.cap_per_domain}  batch={args.batch_size}",
          flush=True)

    student = build_student(cfg.student)
    student.load(cfg.student_output_dir)
    print(f"[eval-v2] loaded student.  use_cache="
          f"{student._model.config.use_cache}", flush=True)

    domains = [d.strip() for d in args.domains.split(",") if d.strip()]
    summary = {}

    for dom in domains:
        path = Path(f"phase2_data/unified/{dom}_test.jsonl")
        if not path.exists():
            print(f"  {dom}: missing test file ({path}), skipping", flush=True)
            continue
        recs = read_jsonl(path)
        if args.cap_per_domain > 0:
            recs = recs[: args.cap_per_domain]
        if not recs:
            continue

        t0 = time.time()
        preds = []
        empty = 0
        for i in range(0, len(recs), args.batch_size):
            batch = recs[i : i + args.batch_size]
            texts = [r["input"] for r in batch]
            try:
                batch_preds = student.predict_batch(texts)
                # predict_batch returns list of (ArgStructureDict, reasoning)
                batch_preds = [p[0] if isinstance(p, tuple) else p
                               for p in batch_preds]
            except Exception as e:
                print(f"  {dom} batch @ {i}: ERROR {e}", flush=True)
                batch_preds = [{"claim_components": [], "premise_components": [],
                                "citation_components": [], "relations": []}
                               for _ in batch]
            for p in batch_preds:
                if (len(p["claim_components"]) == 0
                        and len(p["premise_components"]) == 0):
                    empty += 1
            preds.extend(batch_preds)
            done = min(i + args.batch_size, len(recs))
            print(f"  {dom} {done}/{len(recs)}  "
                  f"({time.time()-t0:.0f}s, empty={empty})", flush=True)

        m = evaluate_corpus(recs, preds, threshold=args.threshold)
        elapsed = time.time() - t0
        print(f"\n  ── {dom} ── n={len(recs)}  empty={empty} "
              f"({100*empty/len(recs):.0f}%)  ({elapsed:.0f}s)", flush=True)
        print(f"     component macro-F1: {m['macro_component_f1']:.3f}", flush=True)
        print(f"     relation F1:        {m['relation_f1']['f1']:.3f}", flush=True)
        print(f"     claim F1:           {m['component_f1']['claim']['f1']:.3f}", flush=True)
        print(f"     premise F1:         {m['component_f1']['premise']['f1']:.3f}", flush=True)
        print(f"     citation F1:        {m['component_f1']['citation']['f1']:.3f}\n",
              flush=True)
        summary[dom] = {
            "n": len(recs),
            "empty": empty,
            "comp_f1": m["macro_component_f1"],
            "rel_f1": m["relation_f1"]["f1"],
            "claim_f1": m["component_f1"]["claim"]["f1"],
            "premise_f1": m["component_f1"]["premise"]["f1"],
            "citation_f1": m["component_f1"]["citation"]["f1"],
            "wall_sec": elapsed,
        }

    print("\n=== SUMMARY ===", flush=True)
    for dom, s in summary.items():
        print(f"  {dom:14s} comp-F1={s['comp_f1']:.3f}  "
              f"rel-F1={s['rel_f1']:.3f}  "
              f"empty={s['empty']}/{s['n']}", flush=True)
    if summary:
        avg = sum(s["comp_f1"] for s in summary.values()) / len(summary)
        print(f"  {'average':14s} comp-F1={avg:.3f}", flush=True)

    if args.out_json:
        out_path = Path(args.out_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps({
            "config": args.config,
            "model_dir": cfg.student_output_dir,
            "cap_per_domain": args.cap_per_domain,
            "batch_size": args.batch_size,
            "per_domain": summary,
        }, indent=2))
        print(f"\n[eval-v2] summary → {out_path}", flush=True)


if __name__ == "__main__":
    main()
