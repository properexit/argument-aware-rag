"""Shared utilities for baseline runs.

All baselines write to a uniquely-named output directory containing:
  - predictions.jsonl   (same schema as the main pipeline)
  - run_config.json     (timestamp, model, prompts, seed, sample size, etc.)
  - prompts_used.txt    (the actual system/user prompts after templating)
  - metrics.json        (computed at the end of the run via evaluate.py)

The directory naming convention is:
  outputs/baselines/<name>_<YYYYMMDD_HHMM>/
which guarantees no run ever overwrites another.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_split, LIARArgRow
from src.evaluate import compute_metrics


# Canonical 6-way labels.
LABELS = ["True", "Mostly-true", "Half-true",
          "Barely-true", "False", "Pants-fire"]


def make_run_dir(name: str, root: Path | None = None) -> Path:
    """Create outputs/baselines/<name>_<timestamp>/ and return its path."""
    root = root or (PROJECT_ROOT / "outputs" / "baselines")
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    out = root / f"{name}_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def normalise_label(raw: str) -> str:
    """Coerce a model's free-form output into one of the 6 canonical labels.

    Tries direct match, then JSON `{"label": ...}`, then loose alias match.
    Returns "" if nothing recognisable comes out.
    """
    if not raw:
        return ""
    s = raw.strip()

    # Try JSON first
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            label = str(obj.get("label", "")).strip()
            if label:
                return _canonicalise(label)
        except json.JSONDecodeError:
            pass

    # Try direct first-line lookup
    first_line = s.splitlines()[0].strip().strip(".,:;\"'")
    canonical = _canonicalise(first_line)
    if canonical:
        return canonical

    # Substring match over the whole response (last resort)
    for lab in LABELS:
        if re.search(rf"\b{re.escape(lab)}\b", s, re.IGNORECASE):
            return lab
    return ""


def _canonicalise(s: str) -> str:
    """Map common variants to the canonical label form."""
    s_norm = s.strip().lower().replace("_", "-").replace(" ", "-")
    canonical = {l.lower(): l for l in LABELS}
    if s_norm in canonical:
        return canonical[s_norm]
    aliases = {
        "pants-on-fire": "Pants-fire", "pants-fire": "Pants-fire",
        "mostly-true": "Mostly-true", "mostly_true": "Mostly-true",
        "half-true": "Half-true", "barely-true": "Barely-true",
        "mostly-false": "Barely-true",  # some models emit this
    }
    return aliases.get(s_norm, "")


@dataclass
class BaselineRunConfig:
    name: str
    description: str
    backend: str                # "ollama" or "openai"
    model: str
    test_data_path: str
    n_claims_total: int
    n_claims_evaluated: int
    seed: int
    started_at: str
    finished_at: str = ""
    elapsed_seconds: float = 0.0
    extra: dict = field(default_factory=dict)


def load_test_rows(data_dir: str) -> list[LIARArgRow]:
    """Load the test split from a prepared split directory."""
    split = load_split(data_dir)
    if "test" not in split:
        raise RuntimeError(f"No test.jsonl in {data_dir}")
    return split["test"]


def write_prediction(f, row: LIARArgRow, predicted_label: str,
                     raw_response: str, mode: str) -> None:
    """Append one prediction row to the open JSONL file. Same schema as
    the main pipeline's predictions.jsonl, so existing scripts work."""
    f.write(json.dumps({
        "row_id": row.id,
        "statement": row.statement,
        "gold_label": row.label,
        "predicted_label": predicted_label,
        "rationale": raw_response[:800],   # truncate to keep file small
        "mode": mode,
        "queries": [],
        "role_evidence": {},
    }) + "\n")


def run_baseline(
    name: str,
    description: str,
    backend: str,
    model: str,
    data_dir: str,
    n: int | None,
    seed: int,
    prompt_for_row: Callable[[LIARArgRow], tuple[str, str]],   # (system, user)
    call_model: Callable[[str, str], str],                     # (system, user) -> raw text
    system_prompt_label: str,
    out_root: Path | None = None,
) -> Path:
    """Generic baseline runner. Returns the path of the run directory.

    Args:
        name: short identifier (e.g. "qwen_zeroshot")
        description: free-text description for the run_config.json
        backend: "ollama" or "openai"
        model: model id (e.g. "qwen2.5:14b-instruct")
        data_dir: path containing test.jsonl (e.g. "data_liar")
        n: number of test claims to score (None = all)
        seed: stratified-sampling seed
        prompt_for_row: function that builds (system, user) prompts per claim
        call_model: function that calls the LLM and returns raw text
        system_prompt_label: short tag stored in run_config.extra
        out_root: optional override of outputs/baselines/
    """
    run_dir = make_run_dir(name, out_root)
    print(f"[baseline:{name}] run dir: {run_dir}")

    rows = load_test_rows(data_dir)
    if n is not None and n < len(rows):
        # Same stratified sampler the main pipeline uses, so the comparison
        # is on the same claims.
        import random
        by_label: dict[str, list] = {}
        for r in rows:
            by_label.setdefault(r.label, []).append(r)
        rng = random.Random(seed)
        per_label = max(1, n // len(by_label))
        sample: list = []
        for lab, rs in by_label.items():
            rng.shuffle(rs)
            sample.extend(rs[:per_label])
        extras = [r for r in rows if r not in sample]
        rng.shuffle(extras)
        while len(sample) < n and extras:
            sample.append(extras.pop())
        rows_to_run = sample[:n]
    else:
        rows_to_run = rows

    started_at = datetime.now().isoformat(timespec="seconds")
    t0 = time.time()
    preds_path = run_dir / "predictions.jsonl"
    prompts_path = run_dir / "prompts_used.txt"

    # Capture the prompt template once at the top of prompts_used.txt
    if rows_to_run:
        s0, u0 = prompt_for_row(rows_to_run[0])
        with open(prompts_path, "w") as pf:
            pf.write("=== SYSTEM PROMPT (first claim) ===\n\n")
            pf.write(s0 + "\n\n")
            pf.write("=== USER PROMPT (first claim) ===\n\n")
            pf.write(u0 + "\n")

    y_true: list[str] = []
    y_pred: list[str] = []
    with open(preds_path, "w") as pf:
        for i, row in enumerate(rows_to_run, 1):
            system_prompt, user_prompt = prompt_for_row(row)
            raw = call_model(system_prompt, user_prompt)
            label = normalise_label(raw)
            write_prediction(pf, row, label, raw, mode=name)
            y_true.append(row.label)
            y_pred.append(label or "UNKNOWN")
            if i % 25 == 0 or i == len(rows_to_run):
                print(f"  [{i}/{len(rows_to_run)}] elapsed {time.time()-t0:.1f}s")

    elapsed = time.time() - t0
    finished_at = datetime.now().isoformat(timespec="seconds")

    # Compute metrics
    metrics = compute_metrics(y_true, y_pred)
    with open(run_dir / "metrics.json", "w") as f:
        json.dump({name: metrics}, f, indent=2)

    cfg = BaselineRunConfig(
        name=name,
        description=description,
        backend=backend,
        model=model,
        test_data_path=str(data_dir),
        n_claims_total=len(rows),
        n_claims_evaluated=len(rows_to_run),
        seed=seed,
        started_at=started_at,
        finished_at=finished_at,
        elapsed_seconds=round(elapsed, 1),
        extra={"system_prompt_label": system_prompt_label},
    )
    with open(run_dir / "run_config.json", "w") as f:
        json.dump(asdict(cfg), f, indent=2)

    print(f"\n[baseline:{name}] complete in {elapsed/60:.1f} min")
    print(f"  6-way macro-F1 : {metrics['macro_f1']:.3f}")
    print(f"  6-way accuracy : {metrics['accuracy']:.3f}")
    print(f"  within-1 acc.  : {metrics['within_1_accuracy']:.3f}")
    print(f"  3-way macro-F1 : {metrics['threeway']['macro_f1']:.3f}")
    print(f"  3-way accuracy : {metrics['threeway']['accuracy']:.3f}")
    print(f"\n  output dir: {run_dir}")
    return run_dir
