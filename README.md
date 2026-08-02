# Argument Aware Retrieval for Automated Fact Checking

Codebase for the project *"Can argument structure improve evidence retrieval
for automated fact checking?"* Two phases:

- **Phase 1:** an argument aware retrieval pipeline that beats flat RAG by
  0.26 6-way macro F1 on LIARArg and sits within 0.017 of an oracle upper
  bound.
- **Phase 2:** distilling the parser that Phase 1 needs at inference into
  a Qwen 1.5B LoRA that retains 85% of a 120B cloud teacher's target task
  performance.

Write-up and full per-run outputs are hosted separately (see Data setup).

## Pipeline (five stages)

```
[claim + supporting article]
        |
        v
1. Argument parser          ->  {claims, premises, support/attack relations}
        |
        v
2. Role-targeted query gen  ->  one query per argument relation
        |
        v
3. Hybrid retriever         ->  BM25 + dense (MiniLM) fused via RRF
        |
        v
4. NLI reranker             ->  role-fit scoring via DeBERTa-v3-small
        |
        v
5. LLM verdict synthesiser  ->  Qwen-14B + probabilistic 6-label prior
                                -> {True, Mostly-true, Half-true,
                                    Barely-true, False, Pants-fire}
```

Stage 1 is the parser. Phase 1 uses gold LIARArg annotations; Phase 2
replaces stage 1 with a distilled learned parser
(`ArgParser-v4` on HuggingFace). Stages 2 through 5 do not change between
phases.

## Headline results

**Phase 1 on LIAR canonical test split intersected with LIARArg
quality-filtered rows (n=952):**

| Method | 6-way F1 | 3-way F1 | within-1 |
|---|---|---|---|
| Flat-RAG baseline | 0.127 | 0.219 | 0.489 |
| Qwen-14B zero-shot (no retrieval) | 0.166 | 0.346 | 0.592 |
| Mistral 7B zero-shot | 0.210 | 0.412 | 0.641 |
| Llama-3.1-8B zero-shot | 0.239 | 0.434 | 0.675 |
| Llama-3.3-70B zero-shot (Groq) | 0.267 | 0.455 | 0.680 |
| **Arg-aware (this work)** | **0.388** | **0.599** | **0.754** |
| Qwen-14B + oracle article | 0.405 | 0.686 | 0.855 |
| Wang et al. (2025a) COTP20 prompt-based | 0.380 | -- | -- |
| Wang et al. (2025a) KGB+RC supervised | 0.420 | -- | -- |

**Phase 2 distilled parser (ArgParser-v4) integrated into the pipeline,
stratified n=425:**

| Method | 6-way F1 | 3-way F1 | within-1 |
|---|---|---|---|
| Flat-RAG | 0.114 | 0.248 | 0.532 |
| Phase 2-beta v4 (1.5B local) | 0.217 | 0.457 | 0.605 |
| Phase 2-alpha (gpt-oss-120b cloud) | 0.254 | 0.461 | 0.616 |
| Retention vs teacher | 85% | 99% | 98% |

## Repository layout

```
phase1_argrag/
├── README.md                          # this file
├── requirements.txt
│
├── src/                               # library
│   ├── data_loader.py, arg_parser.py, query_gen.py,
│   ├── retriever.py, reranker.py, verifier.py,
│   ├── pipeline.py, evaluate.py
│   └── phase2/                        # Phase 2 distillation code
│       ├── student.py                 # includes salvage parser
│       ├── teacher.py                 # Cerebras / HF Inference clients
│       ├── dataset.py, config.py, schema.py
│       ├── arg_parser_llm.py          # inference-time parser (plugs into stage 1)
│       └── evaluate.py                # component-F1 metrics
│
├── scripts/                           # entry points
│   ├── prepare_data.py, build_index.py, build_wikipedia_index.py
│   ├── run_pipeline.py, recompute_metrics.py, audit_disagreement.py
│   ├── build_comparison_table.py, direct_from_structure_ablation.py
│   ├── merge_phase2alpha_predictions.py
│   ├── baselines/
│   │   ├── qwen_zeroshot.py, qwen_oracle_justification.py, groq_zeroshot.py
│   └── phase2/
│       ├── annotate_silver.py         # silver-label generation
│       ├── train_phase2_beta.py       # main training
│       ├── train_student.py           # student model wrapper
│       ├── parse_test_with_teacher.py # Phase 2-alpha
│       ├── evaluate_parser.py, eval_phase2beta_v2.py
│       └── prepare_datasets.py
│
├── configs/                           # YAML configs for training and eval
│
├── data/, data/liar_splits/                  # LIAR raw + splits
│
├── phase2_data/                       # everything Phase 2-beta needs
│   ├── silver/liararg_train_silver.jsonl  # 22 MB, teacher CoT + parses
│   ├── unified/*.jsonl                # training input format (5 corpora + silver)
│   ├── raw/                           # small gold arg-mining corpora
│   └── phase2alpha_indomain_preds/    # Phase 2-alpha in-domain predictions
│
├── phase2_data_liar/                  # Phase 2-alpha and v3/v4 parser predictions
│   └── parser_preds_*.jsonl, gold.jsonl, *.log
│
├── models/                            # model metadata only; weights on HuggingFace
│   ├── phase2_student_beta_qwen0.5b/       -> ArgParser-v1 on HF
│   ├── phase2_student_beta_qwen1.5b_lora/  -> ArgParser-v2 on HF
│   ├── phase2_student_beta_qwen1.5b_lora_v3/  -> ArgParser-v3
│   ├── phase2_student_beta_qwen1.5b_lora_v4/  -> ArgParser-v4 (recommended)
│   └── phase2_student_liar/           # early full-FT experiment (metadata only)
│
├── eval_logs/                         # training + OOD probe logs
│   ├── phase2beta_v4_train.log        # v4 training run
│   ├── phase2beta_v4_eval_full.log    # v4 in-domain eval
│   ├── ampersand_v4.log, persuade_v4.log, echr_v4_salvage.log
│   └── ...
│
├── notebooks/                         # curated Jupyter notebooks
│   ├── phase2/                        # silver gen, training, in-domain eval
│   └── ood_probes/                    # v4 AMPERSAND / PERSUADE / ECHR probes
│
└── fixtures/                          # tiny CI test data
    └── data_dummy/, student_dummy/, student_liar_dummy/
```

The full `outputs/` directory (per-run predictions, audits, comparison
tables, `phase2_results.{md,json}`) and the project report are hosted
on Google Drive rather than in this repo. See "Data setup" below.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

For Phase 1 pipeline evaluation you also need Ollama with a local model:

```bash
ollama pull qwen2.5:14b-instruct   # ~8.5 GB, main verifier
```

For Phase 2-alpha silver generation you need a Cerebras API key
(https://cloud.cerebras.ai, free tier). For the Groq baseline you need a
Groq API key (https://console.groq.com, free tier, no credit card).

## Data setup

Data and full per-run outputs are on Google Drive rather than in this
repo (LIARArg and the gold argument mining corpora each come with
their own licenses; the bundle is also large):

**Download:** https://drive.google.com/drive/folders/1kAXs4eatGyDtPZvCP0adAeQ8WyYjhKzM

Contents (~200 MB):

- `data/` -- LIAR raw CSV, LIAR splits, LIAR-aligned splits
  (`data/liar_splits/{train,val,test}.jsonl`)
- `phase2_data/raw/` -- 5 gold argument mining corpora (AAEC, AbstRCT,
  arg-microtext, CDCP, PERSPECTRUM) plus OOD probe corpora (AMPERSAND,
  PERSUADE 2.0, AURC, ECHR)
- `phase2_data/unified/` -- the 5 gold corpora + LIARArg silver
  serialised as JSONL training records (this is what
  `train_phase2_beta.py` reads)
- `phase2_data/silver/liararg_train_silver.jsonl` -- 2,123 LIARArg
  training articles annotated by gpt-oss-120b via Cerebras, including
  Chain of Thought reasoning (~22 MB, expensive to regenerate)
- `phase2_data_liar/` -- LIARArg gold annotations and parser
  predictions from each Phase 2 variant (v3, v4, Phase 2-alpha)
- `outputs/results_*/` -- full per-run outputs: `predictions.jsonl`
  (per-claim receipts with retrieved passages and verdicts) and
  `audit.{csv,md}` (disagreement analyses)

Extract the archive into the repo root so it merges with the tracked
directories:

```bash
# Assuming the archive downloads to ~/Downloads/argrag_data_bundle.zip
cd /path/to/phase1_argrag
unzip ~/Downloads/argrag_data_bundle.zip
```

After extraction, every notebook and script should run against the
same paths used in the paper.

**Model weights** for the four distilled adapters
(`ArgParser-v1` through `v4`) live on HuggingFace under
`properexit/` and download automatically the first time you load
them (see the reproduction table for usage).

**Retrieval indexes** (`outputs/index_liar/`,
`outputs/index_wikipedia_50k/`) are not included; rebuild them via
the "Rebuilding retrieval indexes" section below (~3 minutes for
LIAR, ~15 minutes for Wikipedia).

**What stays in this repo** even though data is external: the
aggregation summaries the paper directly cites
(`outputs/comparison_table_FINAL.md`,
`outputs/comparison_with_wikipedia.md`,
`outputs/phase2_results.md`, `outputs/phase2_results.json`), all
training and OOD probe logs in `eval_logs/`, and model metadata
under `models/` (config, tokenizer, training log for each variant).

## Reproducing every experiment in the paper

Each row below maps a paper result to the exact command or notebook and
the output directory that contains predictions, metrics, and audit
files.

| Paper result | Command / notebook | Output |
|---|---|---|
| Phase 1 headline (n=952) | `python scripts/run_pipeline.py --n 952 --data-dir data/liar_splits --index-dir outputs/index_liar --out-dir outputs/results_liar_n952_FINAL_20260618 --verifier ollama --ollama-model qwen2.5:14b-instruct --device mps --prior-mode probabilistic` | `outputs/results_liar_n952_FINAL_20260618/` |
| Zero-shot LLM baselines | `python scripts/baselines/qwen_zeroshot.py`, `qwen_oracle_justification.py`, `groq_zeroshot.py --model llama-3.3-70b-versatile` | `outputs/baselines/<name>_<ts>/` |
| Stratified n=425 evaluation | `python scripts/run_pipeline.py --n 425 --stratified ...` | `outputs/results_n425_probprior_FINAL/` |
| Per-example disagreement audit | `python scripts/audit_disagreement.py --results-dir outputs/results_n425_probprior_FINAL` | `outputs/results_n425_probprior_FINAL/audit.md` |
| Wikipedia open-corpus probe | `python scripts/build_wikipedia_index.py --n 50000 --out-dir outputs/index_wikipedia_50k`, then `python scripts/run_pipeline.py --index-dir outputs/index_wikipedia_50k --n 200 --out-dir outputs/results_liar_wikipedia_n200` | `outputs/results_liar_wikipedia_n200/` |
| Phase 2-alpha parser | `python scripts/phase2/parse_test_with_teacher.py --config configs/phase2_parse_test_cerebras_llama70b.yaml` | `outputs/results_phase2alpha_llama70b/` |
| Phase 2-alpha in-domain eval | `notebooks/phase2/phase2alpha_indomain_eval.ipynb` | `phase2_data/phase2alpha_indomain_preds/` |
| Direct-from-structure ablation | `python scripts/direct_from_structure_ablation.py` | `outputs/results_direct_from_structure/` |
| Phase 2 data assembly (5 gold corpora) | `notebooks/phase2/data_gathering.ipynb` | `phase2_data/unified/*.jsonl`, `phase2_data/raw/` |
| OOD dataset downloads (AMPERSAND, PERSUADE, AURC) | `notebooks/phase2/data_gathering_ood.ipynb` | `phase2_data/raw/{AMPERSAND-EMNLP2019, persuade, aurc, ukp_sentential}/` |
| Phase 2-beta silver generation | `notebooks/phase2/silver_generation.ipynb` (uses Cerebras key) | `phase2_data/silver/liararg_train_silver.jsonl` |
| Phase 2-beta v1 (Qwen-0.5B full FT) eval | `notebooks/phase2/v1_indomain_eval.ipynb` | `phase2_data_liar/parser_preds_phase2beta_qwen0.5b.jsonl` |
| Phase 2-beta v2 training | `notebooks/phase2/v2_training.ipynb` (uses `configs/phase2_beta_qwen1.5b_lora.yaml`) | model on HF (`ArgParser-v2`), logs in `eval_logs/phase2beta_v2_train.log` |
| Phase 2-beta v3 continual training | `notebooks/phase2/v3_training.ipynb` (uses `configs/phase2_beta_qwen1.5b_lora_v3.yaml`) | model on HF (`ArgParser-v3`), logs in `eval_logs/phase2beta_v3_train.log` |
| Phase 2-beta v3 LIARArg parse (the 83% empty finding) | `notebooks/phase2/v3_liar_parse.ipynb` | `phase2_data_liar/parser_preds_phase2beta_v3.jsonl` |
| Phase 2-beta v4 training | `notebooks/phase2/v4_training.ipynb` (uses `configs/phase2_beta_qwen1.5b_lora_v4.yaml`) | model on HF (`ArgParser-v4`), logs in `eval_logs/phase2beta_v4_train.log` |
| Phase 2-beta v4 in-domain eval | `notebooks/phase2/v4_indomain_eval.ipynb` | `eval_logs/phase2beta_v4_eval_full.{log,json}` |
| Phase 2-beta v4 LIARArg parse | `notebooks/phase2/v4_liar_parse.ipynb` | `phase2_data_liar/parser_preds_v4.jsonl` |
| Phase 2-beta v4 Phase 1 integration | Run `scripts/run_pipeline.py` with the v4 adapter loaded via HF Transformers + PEFT | `outputs/results_phase2beta_v4_integration/` |
| Qwen-1.5B non-LoRA baseline (early experiment) | `notebooks/phase2/qwen1.5b_base_training.ipynb` (uses `configs/phase2_beta_qwen1.5b.yaml`) | `models/phase2_student_beta_qwen1.5b/train.log` |
| Publish adapters to HuggingFace | `notebooks/phase2/models_upload_hf.ipynb` | `ArgParser-v1..v4` on HuggingFace |
| OOD probe: AMPERSAND | `notebooks/ood_probes/v4_ood_ampersand.ipynb` | `eval_logs/ampersand_v4.log` |
| OOD probe: PERSUADE 2.0 | `notebooks/ood_probes/v4_ood_persuade.ipynb` | `eval_logs/persuade_v4.log` |
| OOD probe: ECHR | `notebooks/ood_probes/v4_ood_echr.ipynb` | `eval_logs/echr_v4_salvage.log` |
| Comparison table across runs | `python scripts/build_comparison_table.py --markdown` | `outputs/comparison_table_FINAL.md` |

## Rebuilding retrieval indexes

Retrieval indexes are excluded from this repo (roughly 570 MB combined,
rebuildable in minutes). Rebuild:

```bash
# LIAR closed-corpus index (~3 min): 38k paragraphs from LIAR-train justifications
python scripts/build_index.py --data-dir data/liar_splits --out-dir outputs/index_liar

# Wikipedia open-corpus index (~15 min for 50k passages)
python scripts/build_wikipedia_index.py --n 50000 --out-dir outputs/index_wikipedia_50k
```

## Model artifacts on HuggingFace

All four Phase 2-beta adapters are published as separate repos:

- `properexit/ArgParser-v1` -- Qwen-0.5B full fine-tune baseline
- `properexit/ArgParser-v2` -- Qwen-1.5B + LoRA r=16 on 4 gold corpora
- `properexit/ArgParser-v3` -- v2 + AAEC continual training
- `properexit/ArgParser-v4` -- Qwen-1.5B + LoRA on 5 gold + LIARArg silver + CoT (recommended)

Load with:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
tok  = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = PeftModel.from_pretrained(base, "properexit/ArgParser-v4")
```

The local `models/` directory holds the training metadata (config,
tokenizer, `train.log`, `phase2_metrics.json`) for each variant. The
weights themselves live on HuggingFace to keep the repo small.

## Determinism

Every LLM call uses `temperature=0`, `top_p=1`. Sampling seeds are `42`
throughout (splits, OOD probe sampling, all training). Ollama runs are
bit-identical across reruns; Cerebras and Groq have small server-side
variation but the aggregate metrics are stable.

## Salvage parser (Phase 2-beta inference)

`src/phase2/student.py` includes a lenient JSON salvage fallback in
`_parse_output`. On long inputs the distilled parser sometimes hits
`max_new_tokens` mid relation-generation loop, leaving JSON unclosed.
Strict parsing rejects this; the salvage fallback scans each section
header and extracts valid `{...}` objects individually, deduping
relations. Strict path is tried first, so behaviour on well-formed
output is unchanged and all reported numbers stand.

Effect on the ECHR probe: 2/20 non-empty went to 20/20 non-empty
without changing the model.

## Data

LIARArg is **not** included in this repo. Obtain from
Wang, Cabrio & Villata (2025a).

LIAR canonical dataset (Wang 2017) is at
https://www.cs.ucsb.edu/~william/data/liar_dataset.zip.

Gold argument mining corpora used for Phase 2-beta training:
AAEC (Stab & Gurevych 2017), AbstRCT (Mayer et al. 2020),
arg-microtext (Peldszus & Stede 2015), CDCP (Park & Cardie 2018),
PERSPECTRUM (Chen et al. 2019). We ship the raw files we used in
`phase2_data/raw/` for a subset; the full ECHR / PERSPECTRUM raw
corpora were too large to include and can be re-downloaded from their
original sources (see `phase2_data/raw/README.md` if present).

OOD probe corpora: AMPERSAND (Chakrabarty et al. 2019, GitHub),
PERSUADE 2.0 (Kaggle Feedback Prize competition, via HuggingFace
`ruudra1/PERSUADE`), ECHR argumentation corpus (Poudyal et al. 2020).

## Citation

If you use this codebase or the distilled adapters, please cite the
paper in `project_report/acl_latex.pdf`.

## License

To be determined before public release.
