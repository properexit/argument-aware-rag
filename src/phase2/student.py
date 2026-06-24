"""Student trainer for Phase 2.

The student is a smaller model (Flan-T5-large, Llama-3.1-8B, Qwen-7B, ...)
fine-tuned on the combined gold+silver corpus to predict ArgStructureDict
JSON given source text.

Interface:
    StudentTrainerBase.train(records, out_dir) -> trained_model_path
    StudentTrainerBase.predict(text) -> (ArgStructureDict, reasoning)

Implementations:
    DummyTrainer   — copies a fixed model artifact, returns canned predictions.
                     Runs in seconds. Used for end-to-end pipeline tests.
    HFTrainer      — HuggingFace Transformers fine-tune. Real implementation
                     for university GPU infra. Configurable base model.

The HFTrainer code is intentionally complete enough to copy onto a GPU
machine and run; it only requires the appropriate packages to be importable.
"""
from __future__ import annotations

import abc
import json
import os
import re
from pathlib import Path

from .schema import ArgStructureDict, StudentConfig, TrainRecord


# ────────────────────────────────────────────────────────────────────────────
# Shared utilities
# ────────────────────────────────────────────────────────────────────────────

INSTRUCTION = ("Extract all argument components and relations from the text. "
               "Output strict JSON with claim_components, premise_components, "
               "citation_components, and relations.")


def _format_input(text: str) -> str:
    return f"{INSTRUCTION}\n\nTEXT:\n{text}"


def _format_target(structure: ArgStructureDict, reasoning: str = "") -> str:
    payload = json.dumps(structure, ensure_ascii=False)
    if reasoning:
        return f"<think>\n{reasoning.strip()}\n</think>\n{payload}"
    return payload


def _parse_output(raw: str) -> tuple[ArgStructureDict, str]:
    cot_m = re.search(r"<think>(.*?)</think>", raw, flags=re.DOTALL)
    reasoning = cot_m.group(1).strip() if cot_m else ""
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    json_m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not json_m:
        return _empty(), reasoning
    try:
        parsed = json.loads(json_m.group())
    except json.JSONDecodeError:
        return _empty(), reasoning
    return {
        "claim_components":    parsed.get("claim_components",    []) or [],
        "premise_components":  parsed.get("premise_components",  []) or [],
        "citation_components": parsed.get("citation_components", []) or [],
        "relations":           parsed.get("relations",           []) or [],
    }, reasoning


def _empty() -> ArgStructureDict:
    return {
        "claim_components": [],
        "premise_components": [],
        "citation_components": [],
        "relations": [],
    }


# ────────────────────────────────────────────────────────────────────────────
# Abstract base
# ────────────────────────────────────────────────────────────────────────────

class StudentTrainerBase(abc.ABC):
    name: str = "base"

    def __init__(self, cfg: StudentConfig):
        self.cfg = cfg
        self.model_path: str | None = None

    @abc.abstractmethod
    def train(self, records: list[TrainRecord], out_dir: str | Path) -> str:
        """Train the student. Returns the directory it was saved to."""
        ...

    @abc.abstractmethod
    def load(self, model_path: str | Path) -> None:
        """Prepare for inference by loading a saved model."""
        ...

    @abc.abstractmethod
    def predict(self, text: str) -> tuple[ArgStructureDict, str]:
        """Run inference on a single text. Returns (structure, reasoning)."""
        ...


# ────────────────────────────────────────────────────────────────────────────
# DummyTrainer — instant, no GPU
# ────────────────────────────────────────────────────────────────────────────

class DummyTrainer(StudentTrainerBase):
    """No-op trainer. Saves a small JSON marker file and predicts a fixed
    minimal structure. Useful for end-to-end pipeline tests without GPU.
    """
    name = "dummy"

    def train(self, records: list[TrainRecord], out_dir: str | Path) -> str:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        marker = out_dir / "dummy_student.json"
        with open(marker, "w") as f:
            json.dump({
                "backend": "dummy",
                "n_train_records": len(records),
                "config": self.cfg.__dict__,
            }, f, indent=2)
        self.model_path = str(out_dir)
        print(f"[student:dummy] saved marker to {marker} "
              f"(would have trained on {len(records)} records)")
        return self.model_path

    def load(self, model_path: str | Path) -> None:
        self.model_path = str(model_path)

    def predict(self, text: str) -> tuple[ArgStructureDict, str]:
        # Same trivial heuristic as DummyTeacher so the pipeline gets
        # consistent output across both dummy components.
        sentences = [s.strip() for s in re.split(r"\[SEP\]|[.!?]\s", text)
                     if s.strip()]
        if len(sentences) < 2:
            return _empty(), ""
        first, *rest = sentences
        return ({
            "claim_components": [{"id": 1, "type": "claim", "text": first[:200]}],
            "premise_components": [
                {"id": 2 + i, "type": "premise", "text": s[:200]}
                for i, s in enumerate(rest[:3])
            ],
            "citation_components": [],
            "relations": [
                {"src": 2 + i, "tgt": 1, "type": "support"}
                for i in range(min(3, len(rest)))
            ],
        }, "Dummy student prediction.")


# ────────────────────────────────────────────────────────────────────────────
# HFTrainer — HuggingFace fine-tune, GPU-required
# ────────────────────────────────────────────────────────────────────────────

class HFTrainer(StudentTrainerBase):
    """Generic HuggingFace seq2seq / causal-LM fine-tuner.

    Default base model is google/flan-t5-large because it fits on a T4
    and excels at structured output. Swap to a Llama / Qwen / Mistral
    decoder by changing StudentConfig.base_model — the code will switch
    between AutoModelForSeq2SeqLM and AutoModelForCausalLM automatically.

    Intentionally not invoked during DummyTrainer pipeline tests; this
    code is for the GPU infra hand-off only.
    """
    name = "hf"

    def __init__(self, cfg: StudentConfig):
        super().__init__(cfg)
        self._tokenizer = None
        self._model = None
        self._is_seq2seq: bool | None = None
        self._device = None

    def _import_hf(self):
        try:
            import torch
            from transformers import (
                AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM,
                Trainer, TrainingArguments, DataCollatorForSeq2Seq,
            )
            return torch, AutoTokenizer, AutoModelForSeq2SeqLM, \
                   AutoModelForCausalLM, Trainer, TrainingArguments, \
                   DataCollatorForSeq2Seq
        except ImportError as e:
            raise RuntimeError(
                "Install: pip install torch transformers datasets accelerate"
            ) from e

    def _is_seq2seq_model(self, base_model: str) -> bool:
        name = base_model.lower()
        return any(t in name for t in ["t5", "bart", "pegasus", "mbart"])

    def train(self, records: list[TrainRecord], out_dir: str | Path) -> str:
        (torch, AutoTokenizer, S2SLM, CausalLM, Trainer, TrainingArguments,
         DataCollatorForSeq2Seq) = self._import_hf()

        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        is_seq2seq = self._is_seq2seq_model(self.cfg.base_model)
        self._is_seq2seq = is_seq2seq
        print(f"[student:hf] base_model={self.cfg.base_model} "
              f"(seq2seq={is_seq2seq})")

        tokenizer = AutoTokenizer.from_pretrained(self.cfg.base_model)
        ModelCls = S2SLM if is_seq2seq else CausalLM
        # IMPORTANT: load weights in fp32 even if we want fp16 training.
        # AMP (enabled via TrainingArguments.fp16=True) maintains fp32
        # master weights and casts to fp16 only for forward/backward.
        # Loading directly in fp16 conflicts with AMP's gradient scaler
        # ("Attempting to unscale FP16 gradients" — torch raises that
        # because there are no fp32 grads to unscale).
        model = ModelCls.from_pretrained(self.cfg.base_model)
        if self.cfg.gradient_checkpointing:
            model.gradient_checkpointing_enable()
            # For T5: gradient checkpointing requires use_cache=False
            if hasattr(model.config, "use_cache"):
                model.config.use_cache = False

        # Build the train/val split from records
        train_recs = [r for r in records if r.get("split") == "train"]
        val_recs   = [r for r in records if r.get("split") == "val"]
        if not val_recs and train_recs:
            split = max(1, int(0.1 * len(train_recs)))
            val_recs = train_recs[-split:]
            train_recs = train_recs[:-split]

        def encode(rec: TrainRecord):
            inp = _format_input(rec["input"])
            tgt = _format_target(rec["output"], rec.get("reasoning", ""))
            ids = tokenizer(inp, max_length=self.cfg.max_input_len,
                            truncation=True, padding="max_length",
                            return_tensors="pt")
            labels = tokenizer(tgt, max_length=self.cfg.max_target_len,
                               truncation=True, padding="max_length",
                               return_tensors="pt")["input_ids"]
            labels[labels == tokenizer.pad_token_id] = -100
            return {
                "input_ids":      ids["input_ids"].squeeze(),
                "attention_mask": ids["attention_mask"].squeeze(),
                "labels":         labels.squeeze(),
            }

        train_ds = [encode(r) for r in train_recs]
        val_ds   = [encode(r) for r in val_recs] if val_recs else None

        args = TrainingArguments(
            output_dir=str(out_dir),
            num_train_epochs=self.cfg.num_epochs,
            per_device_train_batch_size=self.cfg.batch_size,
            per_device_eval_batch_size=self.cfg.batch_size,
            gradient_accumulation_steps=self.cfg.grad_accum,
            learning_rate=self.cfg.learning_rate,
            weight_decay=self.cfg.weight_decay,
            warmup_ratio=self.cfg.warmup_ratio,
            fp16=self.cfg.fp16,
            optim=self.cfg.optim,
            eval_strategy="epoch" if val_ds else "no",
            save_strategy="epoch",
            save_total_limit=2,
            load_best_model_at_end=bool(val_ds),
            seed=self.cfg.seed,
            report_to="none",
            logging_steps=50,
        )

        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            data_collator=(DataCollatorForSeq2Seq(tokenizer, model=model)
                           if is_seq2seq else None),
        )
        trainer.train()
        trainer.save_model(str(out_dir))
        tokenizer.save_pretrained(str(out_dir))

        self.model_path = str(out_dir)
        return self.model_path

    def load(self, model_path: str | Path) -> None:
        (torch, AutoTokenizer, S2SLM, CausalLM, *_rest) = self._import_hf()
        model_path = str(model_path)
        is_seq2seq = self._is_seq2seq_model(self.cfg.base_model)
        self._is_seq2seq = is_seq2seq
        self._tokenizer = AutoTokenizer.from_pretrained(model_path)
        ModelCls = S2SLM if is_seq2seq else CausalLM
        self._model = ModelCls.from_pretrained(model_path)
        self._device = "cuda" if torch.cuda.is_available() else (
            "mps" if torch.backends.mps.is_available() else "cpu")
        self._model.to(self._device)
        self._model.eval()
        self.model_path = model_path

    def predict(self, text: str) -> tuple[ArgStructureDict, str]:
        if self._model is None:
            raise RuntimeError("HFTrainer not loaded — call .load() first")
        (torch, *_rest) = self._import_hf()
        inp = _format_input(text)
        enc = self._tokenizer(inp, max_length=self.cfg.max_input_len,
                              truncation=True, return_tensors="pt").to(self._device)
        with torch.no_grad():
            out = self._model.generate(
                **enc,
                max_new_tokens=self.cfg.max_target_len,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3,
            )
        raw = self._tokenizer.decode(out[0], skip_special_tokens=True)
        return _parse_output(raw)


# ────────────────────────────────────────────────────────────────────────────
# Factory
# ────────────────────────────────────────────────────────────────────────────

def build_student(cfg: StudentConfig) -> StudentTrainerBase:
    if cfg.backend == "dummy":
        return DummyTrainer(cfg)
    if cfg.backend == "hf":
        return HFTrainer(cfg)
    raise ValueError(f"Unknown student backend: {cfg.backend}")
