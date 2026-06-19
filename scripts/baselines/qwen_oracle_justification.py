"""Baseline: Qwen-2.5-14B with the LIARArg gold justification text.

Tests the upper bound on evidence-aided performance when the LLM is
handed the fact-checker's full justification as input. This is an
oracle baseline — it cheats by using the article that explains the
verdict — and tells us the ceiling of single-LLM reasoning given
perfect evidence. Our method should approach this ceiling without
needing the oracle.

Usage:
    python scripts/baselines/qwen_oracle_justification.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.baselines._common import run_baseline


SYSTEM_PROMPT = """You are a PolitiFact-style fact-checking analyst. Classify the truthfulness of a single political claim using the fact-checker's article provided below.

Reply with a strict JSON object on a single line:
{"label": "<one of: True, Mostly-true, Half-true, Barely-true, False, Pants-fire>"}

Distribution sanity check: across PolitiFact, claims are roughly evenly distributed across the 6 labels. Do not collapse everything to False or Half-true.
"""

# Cap to keep input under typical context limits and avoid swamping the
# LLM with massive articles. 4000 chars ≈ 800 tokens, plenty for the
# substantive content of most LIARArg justifications.
MAX_JUSTIFICATION_CHARS = 4000


def prompt_for_row(row):
    justification = (row.full_text or "")[:MAX_JUSTIFICATION_CHARS]
    user = (f"CLAIM: {row.statement}\n\n"
            f"FACT-CHECKER ARTICLE:\n{justification}\n\n"
            f"Reply with the JSON only.")
    return SYSTEM_PROMPT, user


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
                              json=payload, timeout=180)
            r.raise_for_status()
            return r.json().get("message", {}).get("content", "")
        except Exception as e:
            return f'[ollama error: {e}]'
    return _call


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(PROJECT_ROOT / "data_liar"))
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ollama-base-url", default="http://localhost:11434")
    ap.add_argument("--ollama-model", default="qwen2.5:14b-instruct")
    args = ap.parse_args()

    run_baseline(
        name="qwen14b_oracle_justification",
        description=(
            "Qwen-2.5-14B with the LIARArg gold fact-checker article as "
            "input. Oracle upper bound on single-LLM reasoning with "
            "perfect evidence."
        ),
        backend="ollama",
        model=args.ollama_model,
        data_dir=args.data_dir,
        n=args.n,
        seed=args.seed,
        prompt_for_row=prompt_for_row,
        call_model=call_ollama(args.ollama_model, args.ollama_base_url),
        system_prompt_label="oracle_justification_v1",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
