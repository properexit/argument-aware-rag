# Phase 1: Argument-Aware RAG Pipeline

Implementation of Phase 1 of the project "Can argument structure improve evidence retrieval for automated fact-checking?"

## What this is

An argument-aware retrieval-augmented generation pipeline for political fact-checking, evaluated on **LIARArg** (Wang et al., 2025a). Instead of retrieving evidence by topical similarity alone, the pipeline issues **role-targeted queries** (one per support/attack/psupport/pattack relation in the claim's gold argument structure), retrieves with a **hybrid BM25 + dense** index, **re-ranks** by argumentative role using an NLI model, and synthesises a 6-way truthfulness verdict.

A **flat-RAG baseline** (no argument structure, single query, no role re-ranking) is included for direct comparison.

## Pipeline (5 stages)

```
[claim + gold annotations]
        |
        v
1. Argument parser  --->  {claim, premises[], support_rels[], attack_rels[], ...}
        |
        v
2. Role-targeted query generator  --->  [(role, query_text), ...]
        |
        v
3. Hybrid retriever (BM25 + dense, RRF fusion)  --->  top-k passages per query
        |
        v
4. Role-aware re-ranker (NLI cross-encoder)  --->  passages re-scored by role-fit
        |
        v
5. LLM verdict synthesiser  --->  one of {True, Mostly-true, Half-true, Barely-true, False, Pants-fire}
```

## Folder layout

```
phase1_argrag/
├── README.md
├── requirements.txt
├── config.yaml
├── data/                 # (CSV gets copied here on first run)
├── src/
│   ├── data_loader.py    # Load and split LIARArg
│   ├── arg_parser.py     # Phase-1 parser uses gold annotations
│   ├── query_gen.py      # Role-targeted query generator
│   ├── retriever.py      # Hybrid BM25 + dense + RRF
│   ├── reranker.py       # NLI-based role-aware re-ranker
│   ├── verifier.py       # LLM verdict (Ollama / HF / stub)
│   ├── pipeline.py       # 5-stage orchestrator
│   └── evaluate.py       # Macro-F1 metrics
├── scripts/
│   ├── prepare_data.py
│   ├── build_index.py
│   └── run_pipeline.py
└── outputs/
    └── results/
```

## Quick start

```bash
# 1. Install deps
pip install -r requirements.txt --break-system-packages

# 2. Prepare data (creates train/val/test split, filters low-quality rows)
python scripts/prepare_data.py --csv ../../uploads/data.csv

# 3. Build retrieval index over the LIARArg corpus
python scripts/build_index.py

# 4. Run pipeline on a sample of the test set (default 50 claims)
python scripts/run_pipeline.py --n 50 --verifier stub

# Optional: with a local LLM via Ollama
ollama pull llama3.1:8b-instruct
python scripts/run_pipeline.py --n 50 --verifier ollama --ollama_model llama3.1:8b-instruct
```

## What gets reported

`outputs/results/` will contain:

- `predictions.jsonl` — per-claim prediction with full retrieved evidence trace
- `metrics.json` — macro-F1 (overall, extreme labels, intermediate labels), accuracy, per-label F1
- `worked_example.md` — a single claim shown end-to-end (analogue of the Lamar Smith illustration in the proposal)

## Phase 2 hand-off

The argument parser in `src/arg_parser.py` exposes a single `parse(claim_text, justification_text) -> ArgStructure` interface. Replacing the gold-annotation parser with the trained ArgParserLLM model from Phase 2 is a single-file swap; the rest of the pipeline is unchanged.
