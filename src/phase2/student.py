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
        # Causal LMs often lack a pad token — use EOS as pad
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        ModelCls = S2SLM if is_seq2seq else CausalLM
        # IMPORTANT: explicitly force fp32 loading. Without this kwarg,
        # from_pretrained() inherits the checkpoint's stored dtype — bf16
        # for Qwen 2.5, fp16 for some others. AMP's grad scaler then can't
        # unscale non-fp32 gradients ("_amp_foreach_non_finite_check_and_unscale_cuda
        # not implemented for 'BFloat16'") — same class of footgun as the
        # T5+fp16 NaN cascade.
        # The right pattern is always: load fp32 master, let AMP cast to fp16
        # during forward/backward via TrainingArguments.fp16=True.
        try:
            model = ModelCls.from_pretrained(self.cfg.base_model,
                                             dtype=torch.float32)
        except TypeError:
            # Older transformers used torch_dtype= kwarg
            model = ModelCls.from_pretrained(self.cfg.base_model,
                                             torch_dtype=torch.float32)

        # ── LoRA wrap ──
        # Phase 2-β-v2: train low-rank adapters on attention projections
        # instead of the full model. Cuts gradient + optimizer memory to
        # near-zero, so Qwen-1.5B+ fits on 11 GB Pascal.
        # Phase 2-β-v3: when resume_from_adapter is set, load that adapter
        # and continue training instead of starting fresh — saves ~10 hours.
        if self.cfg.use_lora:
            try:
                from peft import LoraConfig, get_peft_model, TaskType, PeftModel
            except ImportError as e:
                raise RuntimeError("pip install peft for LoRA support") from e

            if self.cfg.resume_from_adapter:
                resume_path = Path(self.cfg.resume_from_adapter)
                if not (resume_path / "adapter_config.json").exists():
                    raise FileNotFoundError(
                        f"resume_from_adapter set but no adapter_config.json at "
                        f"{resume_path}")
                # is_trainable=True so the loaded adapter weights remain
                # learnable (default is to freeze them for inference)
                model = PeftModel.from_pretrained(model, str(resume_path),
                                                   is_trainable=True)
                print(f"[student:hf:lora] RESUMING from adapter at "
                      f"{resume_path} (Phase 2-β-v3 continual training)")
            else:
                target_modules = [m.strip() for m in
                                  self.cfg.lora_target_modules.split(",")
                                  if m.strip()]
                lora_cfg = LoraConfig(
                    r=self.cfg.lora_r,
                    lora_alpha=self.cfg.lora_alpha,
                    lora_dropout=self.cfg.lora_dropout,
                    target_modules=target_modules,
                    bias="none",
                    task_type=TaskType.SEQ_2_SEQ_LM if is_seq2seq
                              else TaskType.CAUSAL_LM,
                )
                model = get_peft_model(model, lora_cfg)
                print(f"[student:hf:lora] FRESH adapter "
                      f"(r={self.cfg.lora_r}, targets={target_modules})")

            trainable, total = 0, 0
            for p in model.parameters():
                total += p.numel()
                if p.requires_grad:
                    trainable += p.numel()
            print(f"[student:hf:lora] trainable={trainable/1e6:.1f}M / "
                  f"{total/1e6:.1f}M ({100*trainable/total:.2f}%)")
        if self.cfg.gradient_checkpointing:
            model.gradient_checkpointing_enable()
            if hasattr(model.config, "use_cache"):
                model.config.use_cache = False

        # Build the train/val split from records
        train_recs = [r for r in records if r.get("split") == "train"]
        val_recs   = [r for r in records if r.get("split") == "val"]
        if not val_recs and train_recs:
            split = max(1, int(0.1 * len(train_recs)))
            val_recs = train_recs[-split:]
            train_recs = train_recs[:-split]

        def encode_seq2seq(rec: TrainRecord):
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

        def encode_causal(rec: TrainRecord):
            """Causal-LM encoding: concatenate prompt + target into one
            sequence, mask the prompt portion in labels so we only train
            on the target tokens. Uses the tokenizer's chat template so
            instruction-tuned models (Qwen, Llama-3.x) format input the
            way they expect."""
            inp = _format_input(rec["input"])
            tgt = _format_target(rec["output"], rec.get("reasoning", ""))
            # Try chat template; fall back to plain concat for tokenizers
            # without one (e.g. base/non-instruct models)
            try:
                prompt_str = tokenizer.apply_chat_template(
                    [
                        {"role": "user",      "content": inp},
                    ],
                    tokenize=False,
                    add_generation_prompt=True,
                )
                full_str = prompt_str + tgt + tokenizer.eos_token
            except Exception:
                prompt_str = inp + "\n\n"
                full_str = prompt_str + tgt + tokenizer.eos_token

            max_total = self.cfg.max_input_len + self.cfg.max_target_len
            full = tokenizer(full_str, max_length=max_total,
                             truncation=True, padding="max_length",
                             return_tensors="pt")
            # Find where the target tokens start (= length of the prompt-only
            # tokenisation, capped at max_total)
            prompt_ids = tokenizer(prompt_str, truncation=True,
                                   max_length=max_total, return_tensors="pt")
            prompt_len = min(prompt_ids["input_ids"].shape[1], max_total)

            labels = full["input_ids"].clone()
            labels[0, :prompt_len] = -100                              # mask prompt
            labels[labels == tokenizer.pad_token_id] = -100            # mask pad
            return {
                "input_ids":      full["input_ids"].squeeze(),
                "attention_mask": full["attention_mask"].squeeze(),
                "labels":         labels.squeeze(),
            }

        encode = encode_seq2seq if is_seq2seq else encode_causal
        print(f"[student:hf] encoding {len(train_recs)} train + "
              f"{len(val_recs)} val records "
              f"({'seq2seq' if is_seq2seq else 'causal'} format)")
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

        # Detect whether the saved dir is a full model checkpoint or just a
        # LoRA adapter (which contains adapter_config.json + adapter_model.*).
        adapter_path = Path(model_path) / "adapter_config.json"
        is_lora_adapter = adapter_path.exists()

        if is_lora_adapter:
            # Load tokenizer from the saved dir (we save it there too),
            # then load the BASE model + apply the adapter on top
            self._tokenizer = AutoTokenizer.from_pretrained(model_path)
            ModelCls = S2SLM if is_seq2seq else CausalLM
            try:
                from peft import PeftModel
            except ImportError as e:
                raise RuntimeError("pip install peft to load LoRA adapters") from e
            base = ModelCls.from_pretrained(self.cfg.base_model)
            self._model = PeftModel.from_pretrained(base, model_path)
            print(f"[student:hf:load] base={self.cfg.base_model} + "
                  f"LoRA adapter from {model_path}")
        else:
            self._tokenizer = AutoTokenizer.from_pretrained(model_path)
            ModelCls = S2SLM if is_seq2seq else CausalLM
            self._model = ModelCls.from_pretrained(model_path)
            print(f"[student:hf:load] full model from {model_path}")

        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        # CRITICAL: re-enable KV cache for inference. Training sets
        # use_cache=False as a hard requirement of gradient_checkpointing,
        # and this setting is persisted in the checkpoint's config. Loading
        # the model carries the False forward into inference, where it
        # makes every generated token re-run the full forward pass over
        # the entire context → ~150× slower decoding on long inputs.
        if hasattr(self._model.config, "use_cache"):
            self._model.config.use_cache = True
        # Also disable any inherited gradient_checkpointing flag (inference
        # doesn't compute grads anyway, but the flag can still trigger
        # checkpoint-wrapped forwards).
        if hasattr(self._model, "gradient_checkpointing_disable"):
            try:
                self._model.gradient_checkpointing_disable()
            except Exception:
                pass

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

        # Use the chat template at inference IFF it was used at training (i.e.
        # causal LM trained via encode_causal). Without this, the model gets
        # raw text input but was trained on chat-formatted input → format
        # mismatch → garbage output → our parser returns empty fallback.
        # (This was a silent bug that made a perfectly-trained Qwen look like
        # it had collapsed.)
        if not self._is_seq2seq:
            try:
                prompt_str = self._tokenizer.apply_chat_template(
                    [{"role": "user", "content": inp}],
                    tokenize=False,
                    add_generation_prompt=True,
                )
            except Exception:
                prompt_str = inp + "\n\n"
            enc = self._tokenizer(
                [prompt_str],
                return_tensors="pt",
                truncation=True,
                max_length=self.cfg.max_input_len,
            ).to(self._device)
        else:
            enc = self._tokenizer(inp, max_length=self.cfg.max_input_len,
                                  truncation=True, return_tensors="pt").to(self._device)

        with torch.no_grad():
            # Greedy decoding for causal LMs (no_repeat_ngram_size=3 + beam
            # search was distorting JSON structure — beams can avoid the
            # closing brace because they "look like" a repeated trigram).
            gen_kwargs = dict(
                max_new_tokens=self.cfg.max_target_len,
                pad_token_id=self._tokenizer.pad_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
                do_sample=False,
            )
            if self._is_seq2seq:
                gen_kwargs.update(num_beams=4, early_stopping=True)
            out = self._model.generate(**enc, **gen_kwargs)

        if self._is_seq2seq:
            raw = self._tokenizer.decode(out[0], skip_special_tokens=True)
        else:
            # Strip the prompt portion — only decode the newly-generated tokens
            input_len = enc["input_ids"].shape[-1]
            raw = self._tokenizer.decode(out[0][input_len:], skip_special_tokens=True)
        return _parse_output(raw)

    # ────────────────────────────────────────────────────────────────────
    # Batched inference (Phase 2-β-v2)
    # ────────────────────────────────────────────────────────────────────

    def predict_batch(self, texts: list[str]
                      ) -> list[tuple[ArgStructureDict, str]]:
        """Run inference on a list of inputs in one batched generate() call.

        ~3-5× faster than calling predict() in a loop because the GPU
        stays fed (vs Python overhead dominating between single-row calls).

        For causal LMs, we LEFT-pad the inputs so all rows have their
        content ending at the same position — generation then continues
        from that aligned position for every row.
        """
        if self._model is None:
            raise RuntimeError("HFTrainer not loaded — call .load() first")
        if not texts:
            return []
        (torch, *_rest) = self._import_hf()
        tok = self._tokenizer
        model = self._model

        # Build prompts (chat template for causal, raw for seq2seq)
        prompts = []
        for text in texts:
            inp = _format_input(text)
            if not self._is_seq2seq:
                try:
                    p = tok.apply_chat_template(
                        [{"role": "user", "content": inp}],
                        tokenize=False, add_generation_prompt=True,
                    )
                except Exception:
                    p = inp + "\n\n"
            else:
                p = inp
            prompts.append(p)

        # LEFT-pad causal LM inputs — required for batched generation
        old_side = tok.padding_side
        if not self._is_seq2seq:
            tok.padding_side = "left"
        try:
            enc = tok(prompts, return_tensors="pt", truncation=True,
                      max_length=self.cfg.max_input_len, padding=True
                      ).to(self._device)
        finally:
            tok.padding_side = old_side

        gen_kwargs = dict(
            max_new_tokens=self.cfg.max_target_len,
            pad_token_id=tok.pad_token_id,
            eos_token_id=tok.eos_token_id,
            do_sample=False,
        )
        if self._is_seq2seq:
            gen_kwargs.update(num_beams=4, early_stopping=True)

        with torch.no_grad():
            out = model.generate(**enc, **gen_kwargs)

        # Strip the prompt portion from each row
        input_len = enc["input_ids"].shape[-1]
        results = []
        for i in range(out.shape[0]):
            if self._is_seq2seq:
                raw = tok.decode(out[i], skip_special_tokens=True)
            else:
                raw = tok.decode(out[i][input_len:], skip_special_tokens=True)
            results.append(_parse_output(raw))
        return results


# ────────────────────────────────────────────────────────────────────────────
# Factory
# ────────────────────────────────────────────────────────────────────────────

def build_student(cfg: StudentConfig) -> StudentTrainerBase:
    if cfg.backend == "dummy":
        return DummyTrainer(cfg)
    if cfg.backend == "hf":
        return HFTrainer(cfg)
    raise ValueError(f"Unknown student backend: {cfg.backend}")
