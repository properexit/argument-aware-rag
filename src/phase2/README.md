# Phase 2 — ArgParserLLM (learned cross-domain argument parser)

This subsystem replaces Phase 1's `GoldArgParser` with a learned parser
that works on arbitrary text (not just LIARArg rows). The design goal is
that Phase 1 doesn't need to know which parser is plugged in — same
`.parse()` interface, same `ArgStructure` output type.

## What's in here

```
src/phase2/
├── schema.py            TrainRecord, ArgStructureDict, configs
├── dataset.py           Multi-source assembler + JSONL I/O
├── teacher.py           AnnotatorBase + DummyTeacher + GroqTeacher
├── student.py           StudentTrainerBase + DummyTrainer + HFTrainer
├── arg_parser_llm.py    Adapter: student.predict() → Phase 1 ArgStructure
├── evaluate.py          Component-F1 + relation-F1
├── config.py            YAML loader
└── README.md            this file

configs/
├── phase2_dummy.yaml         all dummies — CPU, ~30 seconds
├── phase2_groq_flan.yaml     Groq Llama-70B teacher (~100K tok/day cap)
├── phase2_hfinf_flan.yaml    HF Inference Llama-70B (free, ~1000 req/day)
└── phase2_local7b_flan.yaml  fully offline Qwen-7B (4-bit) on local GPU
                              (unlimited, no API key, ~5 GB VRAM)

scripts/phase2/
├── prepare_datasets.py       assemble gold corpus
├── annotate_silver.py        teacher-annotate silver corpus
├── train_student.py          fine-tune student
└── evaluate_parser.py        parser-level F1 on test split
```

## Pluggability

Two interfaces are the swap seams:

- **`AnnotatorBase`** (`teacher.py`) — `annotate(text, source)` returns
  `(ArgStructureDict, reasoning)`. Ships with four backends:
  `DummyTeacher`, `GroqTeacher` (Llama-70B via Groq, 100K tok/day cap),
  `HFInferenceTeacher` (Llama-70B / Qwen-72B via HuggingFace's free
  Inference Providers, ~1000 req/day), and `LocalHFTeacher` (Qwen-3B
  or Llama-3B running locally on the same GPU, no API needed).
  Add new ones (OpenAI, Anthropic, vLLM-hosted) by subclassing.

- **`StudentTrainerBase`** (`student.py`) — `train(records, out_dir)`
  + `load(path)` + `predict(text)`. Add a new student backend (PEFT
  LoRA, accelerate-distributed, etc.) by subclassing and registering
  in `build_student`.

Both have `Dummy*` and real implementations. Dummies let you smoke-test
the full pipeline (data → annotate → train → eval → Phase 1 integration)
in seconds, with no GPU and no API key.

## Quick start — dummy smoke test (laptop)

```bash
# from repo root, with .venv activated
python -m scripts.phase2.prepare_datasets --config configs/phase2_dummy.yaml
python -m scripts.phase2.annotate_silver  --config configs/phase2_dummy.yaml
python -m scripts.phase2.train_student    --config configs/phase2_dummy.yaml
python -m scripts.phase2.evaluate_parser  --config configs/phase2_dummy.yaml
```

Total runtime: <30 seconds. The synthetic two-example corpus is used,
the dummy student "trains" by writing a marker JSON, the dummy
predictor returns trivial structures. The point is to confirm all
files import cleanly and the metrics pipeline produces a JSON.

## Real run — GPU server

1. **Env setup** (on the JupyterHub notebook, one-time):
   ```bash
   git clone https://github.com/properexit/argument-aware-rag.git
   cd argument-aware-rag
   python3 -m venv .venv && source .venv/bin/activate
   # PyTorch with CUDA 12.1 wheels (works on driver ≥ 525)
   pip install torch==2.4.1 torchvision==0.19.1 \
       --index-url https://download.pytorch.org/whl/cu121
   pip install -r requirements.txt
   pip install transformers datasets accelerate peft sentencepiece
   # Only needed for local_hf teacher (4-bit / 8-bit):
   pip install bitsandbytes>=0.42
   # Set whichever teacher key you'll actually use:
   export HF_TOKEN=hf_...        # for hf_inference backend
   export GROQ_API_KEY=gsk_...   # for groq backend
   # (no env var needed for local_hf)
   ```

2. **Edit `configs/phase2_groq_flan.yaml`** to point `liararg_path` and
   `aries_clean_path` at the data files on the server.

3. **Run the four scripts** in order:
   ```bash
   python -m scripts.phase2.prepare_datasets --config configs/phase2_groq_flan.yaml
   python -m scripts.phase2.annotate_silver  --config configs/phase2_groq_flan.yaml
   python -m scripts.phase2.train_student    --config configs/phase2_groq_flan.yaml
   python -m scripts.phase2.evaluate_parser  --config configs/phase2_groq_flan.yaml
   ```

   `annotate_silver` is rate-limited (≤30 requests/min on Groq free
   tier). `train_student` is the GPU-heavy step. Both are resumable.

## Phase 1 integration

Once you have a trained student, drop it into the Phase 1 pipeline:

```python
from src.phase2.student import build_student
from src.phase2.config import load_phase2_config
from src.phase2.arg_parser_llm import ArgParserLLM
from src.pipeline import ArgAwareRAGPipeline   # Phase 1

cfg = load_phase2_config("configs/phase2_groq_flan.yaml")
student = build_student(cfg.student)
student.load(cfg.student_output_dir)

# Use the same row→text wiring Phase 1 uses internally
parser = ArgParserLLM(
    student=student,
    row_to_text=lambda i: liararg_rows[i].statement + " " + liararg_rows[i].justification,
    row_to_statement=lambda i: liararg_rows[i].statement,
)

pipeline = ArgAwareRAGPipeline(arg_parser=parser, ...)  # rest as Phase 1
```

The gap between gold-parser and learned-parser Phase 1 macro-F1 is
the headline number — that's what we report.

## Datasets

- **AAEC** (Stab & Gurevych, 2014) — student essays, argument graphs
- **AbstRCT** (Mayer et al., 2020) — RCT abstracts, evidence/claim
- **LIARArg** (Wang et al., 2025a) — political claims, our anchor
- **ARIES sources** (Cuties, US2016, Microtext, CDCP, ACSP, ...)
  — un-annotated, used for silver labels

Loaders for the gold sources are currently stubs in `dataset.py` —
implement them when the data is in hand. The synthetic corpus fallback
covers smoke testing in the meantime.

## What this scaffold deliberately defers

- Real loaders for AAEC/AbstRCT/LIARArg (stubs raise NotImplementedError
  with a clear message — fill in when needed)
- LoRA / QLoRA configuration in HFTrainer (full fine-tune only for now;
  add `peft.LoraConfig` wiring when 8B+ models become viable)
- Distributed training (single-GPU only)
- Per-source class weighting for imbalanced silver labels
- Active learning over teacher annotations
