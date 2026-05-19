# Phase 1 — first-pass results and next steps

## What is built

A complete five-stage argument-aware RAG pipeline (`src/`), runnable with three scripts (`scripts/`), evaluated on a stratified split of LIARArg.

```
data_loader.py      Parses LIARArg's stringified-list columns, filters low-quality rows,
                    stratified split (2123 train / 284 val / 425 test from 2832 clean rows).
arg_parser.py       Returns an ArgStructure (claims, premises, relations) from the gold
                    LIARArg annotations. Phase 2 will swap GoldArgParser for ArgParserLLM.
query_gen.py        Emits one role-targeted query per relation (support/attack/psupport/
                    pattack), plus a flat-query baseline.
retriever.py        Hybrid BM25 + dense (sentence-transformers) fused with RRF, over a
                    50,065-paragraph corpus built from the fact-checker articles.
                    Same-row exclusion prevents trivial leakage at evaluation time.
reranker.py         NLI cross-encoder (deberta-v3-small) re-scores each retrieved passage
                    by how well it plays the requested argumentative role.
verifier.py         Three backends: rule-based stub, local Ollama, Anthropic stub.
pipeline.py         Orchestrates the 5 stages; also exposes a flat-RAG run for comparison.
evaluate.py         Macro-F1 (overall, extreme labels, intermediate labels), per-label
                    P/R/F1, confusion matrix.
```

## First-pass numbers (sanity check)

Run: `n=25 test claims, BM25-only retrieval, no NLI re-ranker, stub verifier`
(this is the runtime-permitted configuration in the sandbox; full setup needs
sentence-transformers + a local LLM to be installed).

```
                         macro-F1   extreme   intermediate   accuracy
arg-aware (stub)         0.309      0.515     0.222          0.36
flat-RAG  (stub)         0.046      0.000     0.157          0.16
```

The flat-RAG baseline collapses to predicting "Half-true" for every claim
(because the stub can only differentiate when it has role labels). The
argument-aware path uses all six labels and is correct on 9/25 claims.

These are *lower-bound* numbers. The next two steps should push them up
substantially:

1. **Turn on the dense retriever and NLI re-ranker.** The hybrid retriever
   was implemented and unit-buildable but sentence-transformers / torch were
   not pre-installed in the sandbox. On a real machine:
   ```bash
   pip install sentence-transformers
   python scripts/build_index.py            # now produces BM25 + dense
   python scripts/run_pipeline.py --n 50    # NLI re-ranker on by default
   ```
   Expected lift: re-ranking by NLI role-fit will surface passages that
   genuinely entail/contradict the premise (rather than just share keywords),
   which is precisely the signal the proposal hypothesises is missing in
   flat retrieval.

2. **Swap the stub verifier for a local LLM.** The proposal's design needs
   an LLM to synthesise the final verdict from role-labelled evidence; the
   stub is a coarse rule that only sees the support/attack balance. Run
   `ollama pull llama3.1:8b-instruct` then:
   ```bash
   python scripts/run_pipeline.py --n 50 --verifier ollama \
       --ollama-model llama3.1:8b-instruct
   ```

## Worked example (now produced automatically)

`outputs/results/worked_example.md` contains the test-set claim with the most
gold annotations from this run:

> *"U.S. global AIDS spending helped reduce 'political instability and
> violence' by '40 percent' in recipient nations."*
>
> Gold: **Barely-true** · Predicted: **False** (one bucket off)

The file shows all 8 role-targeted queries (7 attack, 1 partial-support),
each tied to a specific premise from the gold structure, with the retrieved
passages tagged by role — the same "argument map" the proposal describes
for the Lamar Smith illustration.

## Open issues / next steps

1. **LLM centrist bias (addressed in v2 of the prompt).** Small open LLMs
   (Llama-3.1-8B in particular) refuse to predict True / Pants-fire and
   cluster everything around Half-true / Barely-true. Two mitigations are
   now wired in:
   - The system prompt includes an explicit anti-hedging rubric and 5
     few-shot examples covering all 6 labels.
   - The stub's structural prediction is injected into the LLM prompt as a
     `STRUCTURAL_PRIOR`. Disable with `--no-structural-prior` to ablate.

2. **Model upgrade for M3 (11.8 GB Metal VRAM).** Llama-3.1-8B is too small
   for the 6-way verdict task. Try a 13–14B class model at Q4_K_M, which
   fits comfortably:
   ```bash
   ollama pull qwen2.5:14b-instruct           # ~8.5 GB, strong reasoner
   # or
   ollama pull mistral-small:24b-instruct     # ~13 GB, tight but works
   # or stay on Llama but go higher quant
   ollama pull llama3.1:8b-instruct-q8_0      # ~8.5 GB, same model better quant
   ```
   Run with:
   ```bash
   python scripts/run_pipeline.py --n 25 --verifier ollama \
       --ollama-model qwen2.5:14b-instruct --device mps
   ```

3. **Larger-sample evaluation.** With the full stack and an LLM verifier
   each claim takes ~20-30s on M3. Plan ~3 hours to score the full
   425-row test set; ~10 minutes for n=25.

4. **Per-relation-type analysis.** `predictions.jsonl` logs every query,
   role, and retrieved passage. A short notebook should answer: which
   relation types (support vs attack vs partial) contribute most to
   correct predictions, and which LLM hedging patterns dominate the
   error cases? This will inform Phase 2 priorities.

5. **Phase 2 hand-off.** `GoldArgParser` and `ArgParserLLM` share the same
   `parse(...) -> ArgStructure` interface. Replacing the parser is a
   one-file change; the rest of the pipeline is untouched.

## How to reproduce

```bash
pip install -r requirements.txt
python scripts/prepare_data.py --csv /path/to/data.csv
python scripts/build_index.py
python scripts/run_pipeline.py --n 50 --verifier stub
# For the full configuration:
ollama pull llama3.1:8b-instruct
python scripts/run_pipeline.py --n 50 --verifier ollama
```
