"""Baseline: Qwen-2.5-14B zero-shot, claim-only.

Tests how well the LLM does on its own — no retrieval, no evidence, no
argument structure. Isolates the contribution of the LLM's pretrained
knowledge from everything else in the pipeline.

Usage:
    python scripts/baselines/qwen_zeroshot.py
    python scripts/baselines/qwen_zeroshot.py --n 200   # smoke test
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.baselines._common import run_baseline


SYSTEM_PROMPT = """You are a PolitiFact-style fact-checking analyst. Classify the truthfulness of a single political claim using only your background knowledge — no external evidence is provided.

Reply with a strict JSON object on a single line:
{"label": "<one of: True, Mostly-true, Half-true, Barely-true, False, Pants-fire>"}

Distribution sanity check: across PolitiFact, claims are roughly evenly distributed across the 6 labels. Do not collapse everything to False or Half-true.
"""


def prompt_for_row(row):
    return SYSTEM_PROMPT, f"CLAIM: {row.statement}\n\nReply with the JSON only."


def call_ollama(model: str, base_url: str):
    import requests
    def _call(system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": 0.0, "seed": 42, "top_p": 1.0},
        }
        try:
            r = requests.post(f"{base_url.rstrip('/')}/api/chat",
                              json=payload, timeout=120)
            r.raise_for_status()
            return r.json().get("message", {}).get("content", "")
        except Exception as e:
            return f'[ollama error: {e}]'
    return _call


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(PROJECT_ROOT / "data_liar"))
    ap.add_argument("--n", type=int, default=None,
                    help="Limit to first N test claims (default: all)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ollama-base-url", default="http://localhost:11434")
    ap.add_argument("--ollama-model", default="qwen2.5:14b-instruct")
    args = ap.parse_args()

    # Derive the run name from the model so different Ollama models land
    # in clearly-named directories (not all under "qwen14b_zeroshot_*").
    safe_model = (args.ollama_model
                  .replace(":", "_")
                  .replace(".", "_")
                  .replace("-", "_")
                  .replace("/", "_"))
    run_name = f"{safe_model}_zeroshot"

    run_baseline(
        name=run_name,
        description=(
            f"{args.ollama_model} zero-shot, claim-only. No retrieval, no "
            "evidence, no argument structure. Tests the contribution of the "
            "LLM's pretrained knowledge alone."
        ),
        backend="ollama",
        model=args.ollama_model,
        data_dir=args.data_dir,
        n=args.n,
        seed=args.seed,
        prompt_for_row=prompt_for_row,
        call_model=call_ollama(args.ollama_model, args.ollama_base_url),
        system_prompt_label="zeroshot_claim_only_v1",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
