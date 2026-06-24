"""Prepare the Phase 2 training corpus.

Reads source datasets (gold), runs them through the unified-schema
assembler, and writes a JSONL where each row is a TrainRecord.

Silver annotation (LLM-labeled) happens in annotate_silver.py.

Usage:
    python -m scripts.phase2.prepare_datasets --config configs/phase2_dummy.yaml
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make repo root importable when called as `python -m scripts.phase2.prepare_datasets`
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.phase2.config import load_phase2_config
from src.phase2.dataset import assemble_corpus, write_jsonl


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()

    cfg = load_phase2_config(args.config)
    out_dir = Path(cfg.dataset.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    records = assemble_corpus(cfg.dataset)
    gold_path = out_dir / "gold.jsonl"
    write_jsonl(records, gold_path)

    # Quick summary
    by_source = {}
    by_split = {}
    for r in records:
        by_source[r["source_dataset"]] = by_source.get(r["source_dataset"], 0) + 1
        by_split[r["split"]] = by_split.get(r["split"], 0) + 1
    print(f"[prepare] by_source: {by_source}")
    print(f"[prepare] by_split:  {by_split}")
    print(f"[prepare] wrote {gold_path}")


if __name__ == "__main__":
    main()
