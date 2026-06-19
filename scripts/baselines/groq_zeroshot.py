"""Baseline: Llama-3.x-70B zero-shot via Groq's free API tier.

Provides the "stronger / larger LLM" comparison row without any cost.
Built to be resilient against Groq's free-tier rate limits:

  * Llama-3.3-70B-versatile: 30 RPM, **1,000 RPD**, 12K TPM, 100K TPD
  * Llama-3.1-8B-instant:    30 RPM, **14,400 RPD**, 6K TPM, 500K TPD

For 952 test claims, the 70B model is tight (95% of daily quota with no
margin). This script defends against that:

  1. **Incremental append-mode JSONL** — every successful prediction is
     written and flushed immediately. If the script crashes or hits a
     daily limit mid-run, no progress is lost.

  2. **Resumable** — rerunning checks the existing predictions.jsonl,
     skips already-completed claims, continues from where it stopped.
     Uses a FIXED (non-timestamped) directory per model so resumption
     works.

  3. **429 handling with exponential backoff** — respects the
     `retry-after` header from Groq when rate-limited. Caps at 3
     consecutive 429s before exiting gracefully.

  4. **Daily-quota awareness** — tracks requests sent this session and
     stops at `--max-requests` (default: leave 5% headroom under the
     daily cap). Tells you exactly when to resume.

  5. **Proactive RPM throttling** — sleeps between requests to stay
     under the per-minute cap.

Setup (one-time):
  1. Sign up free at https://groq.com (no credit card required)
  2. Get an API key at https://console.groq.com/keys
  3. `pip install groq`
  4. `export GROQ_API_KEY=gsk_...`

Usage:
    # Run with safe defaults on llama-3.3-70b (950 max for safety margin)
    python scripts/baselines/groq_zeroshot.py

    # Smoke test (10 claims, ~30s)
    python scripts/baselines/groq_zeroshot.py --n 10

    # Use the much more generous 8B model (14,400 RPD)
    python scripts/baselines/groq_zeroshot.py --model llama-3.1-8b-instant \\
        --max-requests 999999

    # Resume an interrupted run (just rerun the same command — it picks
    # up where it left off automatically)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.baselines._common import (
    BaselineRunConfig,
    load_test_rows,
    normalise_label,
)
from src.evaluate import compute_metrics


SYSTEM_PROMPT = """You are a PolitiFact-style fact-checking analyst. Classify the truthfulness of a single political claim using only your background knowledge — no external evidence is provided.

Reply with a strict JSON object on a single line:
{"label": "<one of: True, Mostly-true, Half-true, Barely-true, False, Pants-fire>"}

Distribution sanity check: across PolitiFact, claims are roughly evenly distributed across the 6 labels. Do not collapse everything to False or Half-true.
"""

# Groq daily limits per model.
# In practice TPD (tokens per day) is often the binding constraint
# before RPD (requests per day). For ~180-token requests:
#   model                    TPD       max claims per day
#   llama-3.3-70b-versatile  100K      ~560     ← TPD-limited
#   openai/gpt-oss-120b      200K      ~1,100   ← TPD-limited
#   llama-4-scout-17b        500K      ~2,700   ← RPD-limited (1K)
#   llama-3.1-8b-instant     500K      ~14,400  ← RPM-limited
KNOWN_RPD = {
    "llama-3.3-70b-versatile":  1000,
    "llama-3.1-70b-versatile":  1000,
    "llama-3.1-8b-instant":     14400,
    "qwen/qwen3-32b":           1000,
    "openai/gpt-oss-120b":      1000,
    "openai/gpt-oss-20b":       1000,
    "meta-llama/llama-4-scout-17b-16e-instruct": 1000,
}
KNOWN_TPD = {
    "llama-3.3-70b-versatile":  100_000,
    "llama-3.1-70b-versatile":  100_000,
    "llama-3.1-8b-instant":     500_000,
    "qwen/qwen3-32b":           500_000,
    "openai/gpt-oss-120b":      200_000,
    "openai/gpt-oss-20b":       200_000,
    "meta-llama/llama-4-scout-17b-16e-instruct": 500_000,
}
EST_TOKENS_PER_REQUEST = 200   # safe overestimate; lets us pre-budget


def _user_prompt(claim: str) -> str:
    return f"CLAIM: {claim}\n\nReply with the JSON only."


def _load_done_ids(preds_path: Path) -> set[int]:
    """Return the row_ids already present in an existing predictions.jsonl."""
    if not preds_path.exists():
        return set()
    ids: set[int] = set()
    with open(preds_path) as f:
        for line in f:
            try:
                ids.add(int(json.loads(line)["row_id"]))
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    return ids


def _safe_groq_call(client, model: str, system_prompt: str,
                    user_prompt: str, max_retries: int = 3) -> tuple[str, bool]:
    """Call Groq with retry-on-429 using exponential backoff.

    Returns (raw_response_text, hit_daily_limit).
    `hit_daily_limit` is True if the response indicated we exhausted RPD.
    """
    from groq import RateLimitError, APIError

    for attempt in range(max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.0,
                seed=42,
                max_tokens=80,         # short JSON output — keeps TPM usage low
            )
            return resp.choices[0].message.content or "", False

        except RateLimitError as e:
            # Look for daily-limit signal in the error message.
            msg = str(e).lower()
            is_daily = "per day" in msg or "rpd" in msg or "daily" in msg

            # Try to extract retry-after seconds from the error if present.
            wait = 30  # default
            for token in msg.replace(",", " ").split():
                if token.endswith("s") and token[:-1].replace(".", "").isdigit():
                    try:
                        wait = max(wait, int(float(token[:-1])) + 2)
                        break
                    except ValueError:
                        pass

            if is_daily or attempt == max_retries:
                return f"[groq rate-limit error: {e}]", is_daily

            # Exponential backoff for per-minute / per-second limits
            backoff = max(wait, 2 ** attempt * 5)
            print(f"  [429 — sleeping {backoff}s before retry {attempt+1}/{max_retries}]")
            time.sleep(backoff)

        except APIError as e:
            if attempt == max_retries:
                return f"[groq api error: {e}]", False
            print(f"  [api error — retry {attempt+1}/{max_retries} in 5s]: {e}")
            time.sleep(5)

        except Exception as e:
            return f"[groq error: {e}]", False

    return "[groq: max retries exceeded]", False


def main() -> int:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    ap.add_argument("--data-dir", default=str(PROJECT_ROOT / "data_liar"))
    ap.add_argument("--n", type=int, default=None,
                    help="Limit to first N test claims (default: all 952)")
    ap.add_argument("--model", default="llama-3.3-70b-versatile",
                    help="Groq model id (default: llama-3.3-70b-versatile)")
    ap.add_argument("--rpm", type=int, default=25,
                    help="Requests-per-minute cap on our side (default: 25, "
                         "well under Groq's 30 rpm limit)")
    ap.add_argument("--max-requests", type=int, default=None,
                    help="Hard cap on total requests this run. Default: "
                         "95%% of the model's known RPD (~950 for 70B). "
                         "Use 999999 for unlimited.")
    args = ap.parse_args()

    # ---- API key check ----
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not set.\n"
              "  1. Sign up at https://groq.com (no card needed)\n"
              "  2. Create a key at https://console.groq.com/keys\n"
              "  3. export GROQ_API_KEY=gsk_...")
        return 1
    try:
        from groq import Groq
    except ImportError:
        print("ERROR: groq SDK not installed. Run `pip install groq` first.")
        return 1
    client = Groq()

    # ---- Decide max-requests budget ----
    # TPD (token daily) is usually the binding constraint, not RPD.
    # Pick whichever cap implies fewer requests.
    if args.max_requests is None:
        rpd = KNOWN_RPD.get(args.model, 1000)
        tpd = KNOWN_TPD.get(args.model, 100_000)
        rpd_cap = int(rpd * 0.95)
        tpd_cap = int(tpd * 0.95 / EST_TOKENS_PER_REQUEST)
        args.max_requests = min(rpd_cap, tpd_cap)
        binding = "TPD" if tpd_cap < rpd_cap else "RPD"
        print(f"[groq:{args.model}] using max-requests = {args.max_requests} "
              f"({binding}-limited; RPD-cap={rpd_cap}, "
              f"TPD-cap={tpd_cap} at est {EST_TOKENS_PER_REQUEST} tok/req)")

    # ---- Output directory: FIXED per-model so we can resume ----
    safe_name = (args.model
                 .replace(":", "_").replace("/", "_")
                 .replace(".", "_").replace("-", "_"))
    out_dir = (PROJECT_ROOT / "outputs" / "baselines"
               / f"groq_{safe_name}_zeroshot")
    out_dir.mkdir(parents=True, exist_ok=True)
    preds_path = out_dir / "predictions.jsonl"
    print(f"[groq:{args.model}] output dir: {out_dir}")

    # ---- Resume: skip already-completed row IDs ----
    done_ids = _load_done_ids(preds_path)
    if done_ids:
        print(f"[groq:{args.model}] resuming: {len(done_ids)} claims already done")

    # ---- Load test rows, filter to remaining work ----
    all_rows = load_test_rows(args.data_dir)
    todo = [r for r in all_rows if r.id not in done_ids]
    if args.n is not None:
        # Apply --n to total target across all sessions, not per run
        n_already = len(done_ids)
        remaining_target = max(0, args.n - n_already)
        todo = todo[:remaining_target]
    print(f"[groq:{args.model}] test set: {len(all_rows)} total, "
          f"{len(done_ids)} done, {len(todo)} to do this run")

    if not todo:
        print(f"[groq:{args.model}] nothing to do. Run complete.")
        _emit_metrics(preds_path, out_dir, args)
        return 0

    # ---- Run, respecting RPM, with incremental flushed writes ----
    started_at = datetime.now().isoformat(timespec="seconds")
    t0 = time.time()
    sleep_between = 60.0 / max(args.rpm, 1)
    consecutive_429 = 0
    last_call = 0.0
    n_succeeded = 0

    with open(preds_path, "a") as pf:
        for i, row in enumerate(todo, 1):
            # Stop if THIS SESSION would exceed today's daily-quota guard.
            # done_ids may have been processed yesterday or on a different
            # key, so they don't count against today's API budget. Only
            # n_succeeded (this session's new requests) does.
            if n_succeeded >= args.max_requests:
                print(f"\n[groq:{args.model}] hit this-session max-requests "
                      f"budget ({args.max_requests}). Stopping cleanly. "
                      f"Rerun this command tomorrow (or with a fresh key) "
                      f"to continue.")
                break

            # Proactive RPM throttle
            elapsed = time.time() - last_call
            if elapsed < sleep_between:
                time.sleep(sleep_between - elapsed)

            raw, hit_daily = _safe_groq_call(
                client, args.model,
                SYSTEM_PROMPT, _user_prompt(row.statement),
            )
            last_call = time.time()

            label = normalise_label(raw)

            # Track 429 streak to bail early if Groq is unhealthy
            is_error = raw.startswith("[groq")
            if is_error and "rate" in raw.lower():
                consecutive_429 += 1
                if hit_daily:
                    print(f"\n[groq:{args.model}] daily quota exhausted at "
                          f"{n_succeeded} new + {len(done_ids)} prior = "
                          f"{n_succeeded + len(done_ids)} claims.")
                    print(f"Rerun this command tomorrow to continue.")
                    break
                if consecutive_429 >= 3:
                    print(f"\n[groq:{args.model}] 3 consecutive rate-limit "
                          f"errors. Stopping. Rerun later to resume.")
                    break
                # Don't write a junk prediction; skip and try next claim later
                continue
            else:
                consecutive_429 = 0

            # Append + flush immediately so a crash doesn't lose progress
            pf.write(json.dumps({
                "row_id": row.id,
                "statement": row.statement,
                "gold_label": row.label,
                "predicted_label": label,
                "rationale": raw[:800],
                "mode": f"groq_{args.model}_zeroshot",
                "queries": [],
                "role_evidence": {},
            }) + "\n")
            pf.flush()
            os.fsync(pf.fileno())   # belt-and-braces: hit the disk
            n_succeeded += 1

            if i % 25 == 0 or i == len(todo):
                print(f"  [{i}/{len(todo)}] (+{n_succeeded} new) "
                      f"elapsed {time.time()-t0:.1f}s")

    finished_at = datetime.now().isoformat(timespec="seconds")
    elapsed = time.time() - t0

    print(f"\n[groq:{args.model}] session done: +{n_succeeded} new predictions "
          f"in {elapsed/60:.1f} min")
    total_done = len(_load_done_ids(preds_path))
    print(f"  total predictions on disk: {total_done}/{len(all_rows)}")

    # ---- Save run_config and compute metrics ----
    cfg = BaselineRunConfig(
        name=f"groq_{safe_name}_zeroshot",
        description=(
            f"{args.model} zero-shot via Groq free-tier API. Rate-limit "
            "aware, resumable, incrementally-flushed predictions."
        ),
        backend="groq",
        model=args.model,
        test_data_path=str(args.data_dir),
        n_claims_total=len(all_rows),
        n_claims_evaluated=total_done,
        seed=42,
        started_at=started_at,
        finished_at=finished_at,
        elapsed_seconds=round(elapsed, 1),
        extra={
            "rpm_cap": args.rpm,
            "max_requests_budget": args.max_requests,
            "this_session_succeeded": n_succeeded,
            "total_on_disk": total_done,
        },
    )
    with open(out_dir / "run_config.json", "w") as f:
        json.dump(asdict(cfg), f, indent=2)

    _emit_metrics(preds_path, out_dir, args)
    return 0


def _emit_metrics(preds_path: Path, out_dir: Path, args) -> None:
    if not preds_path.exists():
        return
    y_true, y_pred = [], []
    with open(preds_path) as f:
        for line in f:
            d = json.loads(line)
            y_true.append(d["gold_label"])
            y_pred.append(d["predicted_label"] or "UNKNOWN")
    if not y_true:
        return
    m = compute_metrics(y_true, y_pred)
    name = f"groq_{args.model}_zeroshot"
    with open(out_dir / "metrics.json", "w") as f:
        json.dump({name: m}, f, indent=2)
    print(f"  6-way macro-F1 : {m['macro_f1']:.3f}")
    print(f"  6-way accuracy : {m['accuracy']:.3f}")
    print(f"  within-1 acc.  : {m['within_1_accuracy']:.3f}")
    print(f"  3-way macro-F1 : {m['threeway']['macro_f1']:.3f}")
    print(f"  3-way accuracy : {m['threeway']['accuracy']:.3f}")


if __name__ == "__main__":
    raise SystemExit(main())
