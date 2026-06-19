# Phase 1: Argument-Aware RAG Pipeline

Implementation of Phase 1 of the project *"Can argument structure improve evidence retrieval for automated fact-checking?"*

## What this is

An argument-aware retrieval-augmented generation pipeline for political fact-checking, evaluated on **LIARArg** (Wang, Cabrio & Villata 2025a). Instead of retrieving evidence by topical similarity alone, the pipeline issues **role-targeted queries** (one per support/attack/psupport/pattack relation in the claim's gold argument structure), retrieves with a **hybrid BM25 + dense** index, **re-ranks** by argumentative role using an NLI cross-encoder, and synthesises a 6-way truthfulness verdict using an LLM guided by a **probabilistic structural prior**.

A **flat-RAG baseline** (single topical query, no role re-ranking, no structural prior) is included for direct in-pipeline comparison.

## Pipeline (5 stages)

```
[claim + gold annotations]
        |
        v
1. Argument parser          ->  {claim, premises[], support_rels[], attack_rels[], ...}
        |
        v
2. Role-targeted query gen  ->  one query per argument relation
        |
        v
3. Hybrid retriever         ->  BM25 + dense (MiniLM) fused via RRF, top-k per query
        |
        v
4. Role-aware NLI re-ranker ->  passages re-scored by role-fit (entailment/contradiction)
        |
        v
5. LLM verdict synthesiser  ->  Qwen-14B + probabilistic 6-label structural prior
                                -> {True, Mostly-true, Half-true, Barely-true, False, Pants-fire}
```

## Headline results (n=952, LIAR's official test split intersected with LIARArg quality-filtered)

```
Method                           3-way F1    6-way F1    within-1    mixed F1
─────────────────────────────────────────────────────────────────────────────
Flat-RAG baseline (this work)     0.219       0.127       0.489       0.184
Arg-aware (this work, main)       0.599       0.388       0.754       0.534
                                  +0.380      +0.260      +0.265      +0.350
```

For comparison, Wang et al. (2025a, KGB+RC supervised joint training): 6-way macro-F1 = 0.42 on 10-fold CV over full LIARArg. Per-label, our method beats their best supervised approach on the top half of the scale (True / Mostly-true / Half-true) while their supervised classifier dominates on the rare Pants-fire label.

## Folder layout

```
phase1_argrag/
├── README.md, NEXT_STEPS.md, LICENSE, requirements.txt, config.yaml
├── src/
│   ├── data_loader.py    # Load LIARArg CSV, parse argument annotations
│   ├── arg_parser.py     # Phase-1 GoldArgParser (Phase-2 will be ArgParserLLM)
│   ├── query_gen.py      # Role-targeted query generator
│   ├── retriever.py      # Hybrid BM25 + dense + RRF
│   ├── reranker.py       # NLI cross-encoder role-aware re-ranker
│   ├── verifier.py       # LLM verdict with probabilistic structural prior
│   ├── pipeline.py       # 5-stage orchestrator
│   └── evaluate.py       # 6-way + 3-way + within-1 + MAE metrics
├── scripts/
│   ├── prepare_data.py             # filter, split (random or LIAR-aligned)
│   ├── build_index.py              # build BM25 + dense index
│   ├── run_pipeline.py             # run the main pipeline
│   ├── audit_disagreement.py       # per-claim arg-aware vs flat-RAG analysis
│   ├── recompute_metrics.py        # re-score existing predictions
│   ├── build_comparison_table.py   # aggregate every run into one table
│   └── baselines/                  # LLM-only baselines (zero-shot, oracle, etc.)
│       ├── _common.py
│       ├── qwen_zeroshot.py
│       ├── qwen_oracle_justification.py
│       └── groq_zeroshot.py        # free Groq tier for the 70B comparison row
└── outputs/
    ├── results_liar/               # main pipeline run
    └── baselines/                  # one timestamped subdir per baseline run
```

## Quick start (full reproduction)

### 0. Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 1. Get the data

Download LIARArg (`data.csv`) from the original dataset release and place it at `data/data.csv`. Then download LIAR's canonical split for fair comparison:

```bash
mkdir -p /tmp/liar
curl -sL https://www.cs.ucsb.edu/~william/data/liar_dataset.zip -o /tmp/liar/liar.zip
unzip -o -d /tmp/liar /tmp/liar/liar.zip
```

### 2. Prepare splits (LIAR-aligned, for paper-comparable evaluation)

```bash
python scripts/prepare_data.py --csv data/data.csv \
    --liar-split --liar-dir /tmp/liar --out-dir data_liar
```

Produces `data_liar/{train,val,test}.jsonl`. Train ≈ 1,858; val = 0 (LIARArg covers none of LIAR-valid); test = 952.

### 3. Build the retrieval index

```bash
python scripts/build_index.py --data-dir data_liar --out-dir outputs/index_liar
```

~3 minutes on M3. Indexes ~38k paragraphs from LIAR-train justifications.

### 4. Pull the LLM and run the main pipeline

```bash
ollama pull qwen2.5:14b-instruct

caffeinate -i python -u scripts/run_pipeline.py \
    --n 952 --data-dir data_liar \
    --index-dir outputs/index_liar \
    --out-dir outputs/results_liar \
    --verifier ollama --ollama-model qwen2.5:14b-instruct \
    --device mps --prior-mode probabilistic
```

~9–12 hours overnight on M3. For a smoke test, use `--n 25` (~5 minutes).

### 5. Score and audit

```bash
python scripts/recompute_metrics.py --results-dir outputs/results_liar
python scripts/audit_disagreement.py --results-dir outputs/results_liar
```

## Baselines (all free, no paid APIs)

The `scripts/baselines/` directory holds LLM-only baselines that share the same data, prompts skeleton, and evaluation harness as the main pipeline. Each run lands in `outputs/baselines/<name>_<timestamp>/` and never overwrites.

### Local Ollama baselines (free, no internet after model pull)

```bash
# Same LLM as main pipeline, isolates retrieval + prior contribution
python scripts/baselines/qwen_zeroshot.py                                # ~45 min on M3

# Oracle upper bound: claim + gold fact-checker article
python scripts/baselines/qwen_oracle_justification.py                    # ~60 min

# Cross-family LLM checks: same script, different --ollama-model
ollama pull llama3.1:8b
python scripts/baselines/qwen_zeroshot.py --ollama-model llama3.1:8b     # ~30 min

ollama pull gemma2:9b
python scripts/baselines/qwen_zeroshot.py --ollama-model gemma2:9b       # ~40 min
```

### Cloud baseline (free Groq tier, no card required)

For the "strong / larger LLM" comparison row, Groq's free tier serves Llama-3.x-70B:

```bash
# Sign up free at https://groq.com (no credit card)
# Get a key at https://console.groq.com/keys
pip install groq
export GROQ_API_KEY=gsk_...

python scripts/baselines/groq_zeroshot.py                                # ~32 min
python scripts/baselines/groq_zeroshot.py --model llama-3.3-70b-versatile
```

Rate-limited to 28 requests/min (under Groq's free 30 rpm cap). 952 claims finish in roughly 32 minutes at no cost.

### Build the comparison table

After running any subset of baselines, aggregate everything:

```bash
python scripts/build_comparison_table.py --markdown
python scripts/build_comparison_table.py --csv outputs/comparison_table.csv
```

Walks `outputs/results_liar/` and every `outputs/baselines/*/` directory, recomputes metrics consistently, and prints / saves a sortable comparison table.

## What gets saved (per run)

Every pipeline run and baseline run writes a self-contained directory:

```
outputs/{results_liar | baselines/<name>_<timestamp>}/
├── predictions.jsonl   # one row per claim, same schema across all runs
├── metrics.json        # 6-way + 3-way + within-1 + MAE + per-bucket + per-label
├── run_config.json     # model, timestamp, seed, sample size, prompt label
├── prompts_used.txt    # exact system + user prompts (first claim, for reproducibility)
├── worked_example.md   # one claim end-to-end (main pipeline only)
└── audit.csv / audit.md  # generated by audit_disagreement.py
```

Naming convention: `<name>_<YYYYMMDD_HHMM>/`. Two runs of the same baseline produce two separate directories, never an overwrite.

## Determinism

Pinned via `temperature=0`, `top_p=1`, `seed=42` on every LLM call (Ollama and Groq alike). Stratified sampling uses `seed=42` by default. Reruns are bit-identical on Ollama and effectively-identical on Groq (which has minor server-side noise).

## Phase 2 hand-off

The argument parser in `src/arg_parser.py` exposes a single `parse(row_id) -> ArgStructure` interface that Phase 2's learned `ArgParserLLM` will eventually return. Swapping the parser is a single-file change; the rest of the pipeline is unchanged.

## Data

LIARArg is *not* included in this repo. Obtain it from Wang, Cabrio & Villata (2025a). LIAR (Wang 2017) is available at https://www.cs.ucsb.edu/~william/data/liar_dataset.zip.
