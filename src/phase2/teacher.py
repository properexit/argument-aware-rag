"""Teacher annotator for Phase 2.

The teacher's job: given a raw argumentative text, emit a structured
ArgStructureDict + a CoT reasoning trace. Used to convert un-annotated
ARIES rows (the "silver" sources) into TrainRecords.

Interface:
    AnnotatorBase.annotate(text, source) -> (ArgStructureDict, reasoning)

Implementations:
    DummyTeacher  — returns a hard-coded structure. Runs in microseconds.
    GroqTeacher   — Llama-3.3-70B via Groq free tier. Uses the resilient
                    rate-limit-aware patterns from
                    scripts/baselines/groq_zeroshot.py.

To add a new backend (Claude, OpenAI, vLLM-hosted, etc.):
    1. Subclass AnnotatorBase
    2. Implement annotate()
    3. Register in `build_teacher(cfg)`
"""
from __future__ import annotations

import abc
import json
import os
import re
import time
from pathlib import Path
from typing import Iterable

from .schema import ArgStructureDict, TeacherConfig, TrainRecord


# ────────────────────────────────────────────────────────────────────────────
# System prompt — adapted from the Wang-style prompt used in your friend's
# prototype, with our Phase 1 schema (citations included, partials preserved).
# ────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert argument mining annotator.

Before producing the JSON, reason inside <think>...</think> tags about:
- Which sentence is the main conclusion (claim)?
- Which sentences provide evidence, reasons, or examples (premises)?
- Are any segments external references / citations?
- What is the direction (support/attack) and strength (full/partial) of each relation?

Extract the minimal argumentative structure. Conservative is better than over-extraction.

COMPONENT TYPES:
- claim     — central conclusion(s) or clear sub-conclusion(s)
- premise   — reason, evidence, example, statistic, or explanation
- citation  — a clearly-marked external reference, source, or quoted authority

RELATION TYPES (always from premise/citation TO claim):
- support           — premise gives a reason FOR the claim
- attack            — premise contradicts the claim
- psupport          — partial / qualified support
- pattack           — partial / qualified attack

OUTPUT SCHEMA (strict JSON):
{
  "claim_components":   [{"id": int, "type": "claim",    "text": str}, ...],
  "premise_components": [{"id": int, "type": "premise",  "text": str}, ...],
  "citation_components":[{"id": int, "type": "citation", "text": str}, ...],
  "relations": [{"src": int, "tgt": int, "type": "support|attack|psupport|pattack"}, ...]
}

Rules:
1. IDs are unique integers across all components in this example.
2. If no clear argument structure is present, return all-empty arrays.
3. Do not invent claims that aren't in the input.
4. Skip filler, fragments, citations of authors without a full statement.
"""


def _build_user_prompt(text: str, source: str, max_chars: int) -> str:
    return (f"SOURCE: {source}\n\nTEXT:\n{text[:max_chars]}\n\n"
            "Reason inside <think>...</think> then output the JSON only.")


def _extract_json(raw: str) -> ArgStructureDict:
    """Strip CoT, find first JSON object, parse safely."""
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not m:
        return _empty_structure()
    try:
        parsed = json.loads(m.group())
    except json.JSONDecodeError:
        return _empty_structure()
    # Defensive fill-ins for missing arrays
    return {
        "claim_components":    parsed.get("claim_components",    []) or [],
        "premise_components":  parsed.get("premise_components",  []) or [],
        "citation_components": parsed.get("citation_components", []) or [],
        "relations":           parsed.get("relations",           []) or [],
    }


def _extract_cot(raw: str) -> str:
    m = re.search(r"<think>(.*?)</think>", raw, flags=re.DOTALL)
    return m.group(1).strip() if m else ""


def _empty_structure() -> ArgStructureDict:
    return {
        "claim_components": [],
        "premise_components": [],
        "citation_components": [],
        "relations": [],
    }


# ────────────────────────────────────────────────────────────────────────────
# Abstract base
# ────────────────────────────────────────────────────────────────────────────

class AnnotatorBase(abc.ABC):
    """Subclass and implement `annotate`."""
    name: str = "base"

    def __init__(self, cfg: TeacherConfig):
        self.cfg = cfg

    @abc.abstractmethod
    def annotate(self, text: str, source: str) -> tuple[ArgStructureDict, str]:
        """Return (structure, cot_reasoning). cot may be empty string."""
        ...

    def annotate_all(
        self,
        rows: Iterable[dict],
        out_jsonl: str | Path,
        resume: bool = True,
    ) -> list[TrainRecord]:
        """Annotate a list of {text, source} dicts. Resumable.

        Writes each record to disk as soon as it's produced, fsync'd.
        Re-running the same command picks up where it stopped — useful when
        the real teacher hits API rate limits mid-run.
        """
        out_jsonl = Path(out_jsonl)
        out_jsonl.parent.mkdir(parents=True, exist_ok=True)

        done_inputs: set[str] = set()
        if resume and out_jsonl.exists():
            with open(out_jsonl) as f:
                for line in f:
                    try:
                        done_inputs.add(json.loads(line)["input"])
                    except (json.JSONDecodeError, KeyError):
                        continue
            if done_inputs:
                print(f"[teacher:{self.name}] resuming — "
                      f"{len(done_inputs)} already done")

        all_recs: list[TrainRecord] = []
        with open(out_jsonl, "a") as f:
            for i, row in enumerate(rows, 1):
                text = row["text"]
                source = row["source"]
                if text in done_inputs:
                    continue
                structure, cot = self.annotate(text, source)
                rec: TrainRecord = {
                    "instruction": "Extract the argument structure as JSON.",
                    "input": text,
                    "reasoning": cot,
                    "output": structure,
                    "source_dataset": source,
                    "label_kind": "silver",
                    "split": "train",          # caller can re-split later
                    "domain": source,
                }
                all_recs.append(rec)
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
                if i % 10 == 0:
                    print(f"  [teacher:{self.name}] {i} processed this session")
        return all_recs


# ────────────────────────────────────────────────────────────────────────────
# DummyTeacher — instant, no API
# ────────────────────────────────────────────────────────────────────────────

class DummyTeacher(AnnotatorBase):
    """Returns a fixed minimal structure. For smoke-testing the pipeline.

    The structure it returns is intentionally trivial but valid — one
    claim, one premise, one support relation — so downstream code that
    expects non-empty arrays sees something it can process.
    """
    name = "dummy"

    def annotate(self, text: str, source: str) -> tuple[ArgStructureDict, str]:
        sentences = [s.strip() for s in re.split(r"\[SEP\]|[.!?]\s", text)
                     if s.strip()]
        if len(sentences) < 2:
            return _empty_structure(), ""
        first, *rest = sentences
        structure: ArgStructureDict = {
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
        }
        cot = (f"Dummy reasoning: first sentence is the claim; the next "
               f"{len(structure['premise_components'])} sentences are premises "
               f"that I'll mark as 'support' by default.")
        return structure, cot


# ────────────────────────────────────────────────────────────────────────────
# GroqTeacher — real implementation, free tier
# ────────────────────────────────────────────────────────────────────────────

class GroqTeacher(AnnotatorBase):
    """Llama-3.3-70B via Groq free tier. Rate-limit aware.

    Mirrors the resilience patterns from scripts/baselines/groq_zeroshot.py:
      - per-minute throttle (rpm_cap)
      - per-day cap (max_requests_per_day)
      - 429 backoff with retries
      - empty-result fallback on persistent failures
    """
    name = "groq"

    def __init__(self, cfg: TeacherConfig):
        super().__init__(cfg)
        if not os.environ.get("GROQ_API_KEY"):
            raise RuntimeError(
                "GROQ_API_KEY not set. Free tier at https://groq.com")
        try:
            from groq import Groq
        except ImportError as e:
            raise RuntimeError("pip install groq first") from e
        self._client = Groq()
        self._sleep_between = 60.0 / max(cfg.rpm_cap, 1)
        self._last_call = 0.0
        self._n_today = 0

    def annotate(self, text: str, source: str) -> tuple[ArgStructureDict, str]:
        # Daily-cap guard
        if self._n_today >= self.cfg.max_requests_per_day:
            return _empty_structure(), "[teacher: daily cap reached]"

        # RPM throttle
        elapsed = time.time() - self._last_call
        if elapsed < self._sleep_between:
            time.sleep(self._sleep_between - elapsed)

        from groq import RateLimitError
        prompt = _build_user_prompt(text, source, self.cfg.max_input_chars)
        for attempt in range(self.cfg.retries_per_call + 1):
            try:
                resp = self._client.chat.completions.create(
                    model=self.cfg.model or "llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user",   "content": prompt},
                    ],
                    temperature=0.0,
                    seed=self.cfg.seed,
                    max_tokens=self.cfg.max_output_tokens,
                )
                self._last_call = time.time()
                self._n_today += 1
                raw = resp.choices[0].message.content or ""
                return _extract_json(raw), _extract_cot(raw)
            except RateLimitError as e:
                if attempt == self.cfg.retries_per_call:
                    return _empty_structure(), f"[teacher rate-limit: {e}]"
                backoff = 2 ** attempt * 5
                print(f"  [teacher:groq 429 — sleeping {backoff}s]")
                time.sleep(backoff)
            except Exception as e:
                if attempt == self.cfg.retries_per_call:
                    return _empty_structure(), f"[teacher error: {e}]"
                time.sleep(2)
        return _empty_structure(), "[teacher: max retries]"


# ────────────────────────────────────────────────────────────────────────────
# HFInferenceTeacher — HuggingFace Inference Providers (free tier)
# ────────────────────────────────────────────────────────────────────────────

class HFInferenceTeacher(AnnotatorBase):
    """Calls a model hosted via HuggingFace's Inference Providers
    (the free tier of huggingface_hub.InferenceClient, which routes to
    backends like Cerebras / SambaNova / Together).

    Requires env var HF_TOKEN. Llama-3.3-70B-Instruct and
    Qwen/Qwen2.5-72B-Instruct are both available on the free tier
    with a daily request budget (set max_requests_per_day to your cap).

    Uses the same rate-limit-aware patterns as GroqTeacher.
    """
    name = "hf_inference"

    def __init__(self, cfg: TeacherConfig):
        super().__init__(cfg)
        token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
        if not token:
            raise RuntimeError(
                "HF_TOKEN env var not set. Get a free token from "
                "https://huggingface.co/settings/tokens (Read access "
                "is enough for the Inference API).")
        try:
            from huggingface_hub import InferenceClient
        except ImportError as e:
            raise RuntimeError("pip install huggingface_hub") from e
        model = cfg.model or "meta-llama/Llama-3.3-70B-Instruct"
        self._client = InferenceClient(model=model, token=token)
        self._model = model
        self._sleep_between = 60.0 / max(cfg.rpm_cap, 1)
        self._last_call = 0.0
        self._n_today = 0

    def annotate(self, text: str, source: str) -> tuple[ArgStructureDict, str]:
        if self._n_today >= self.cfg.max_requests_per_day:
            return _empty_structure(), "[teacher: daily cap reached]"

        elapsed = time.time() - self._last_call
        if elapsed < self._sleep_between:
            time.sleep(self._sleep_between - elapsed)

        prompt = _build_user_prompt(text, source, self.cfg.max_input_chars)
        for attempt in range(self.cfg.retries_per_call + 1):
            try:
                resp = self._client.chat_completion(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user",   "content": prompt},
                    ],
                    temperature=0.0,
                    seed=self.cfg.seed,
                    max_tokens=self.cfg.max_output_tokens,
                )
                self._last_call = time.time()
                self._n_today += 1
                raw = resp.choices[0].message.content or ""
                return _extract_json(raw), _extract_cot(raw)
            except Exception as e:
                msg = str(e).lower()
                if "rate" in msg or "429" in msg or "quota" in msg:
                    if attempt == self.cfg.retries_per_call:
                        return _empty_structure(), f"[teacher rate-limit: {e}]"
                    backoff = 2 ** attempt * 5
                    print(f"  [teacher:hf_inference {e.__class__.__name__} — "
                          f"sleeping {backoff}s]")
                    time.sleep(backoff)
                elif attempt == self.cfg.retries_per_call:
                    return _empty_structure(), f"[teacher error: {e}]"
                else:
                    time.sleep(2)
        return _empty_structure(), "[teacher: max retries]"


# ────────────────────────────────────────────────────────────────────────────
# LocalHFTeacher — runs a small/medium model on the local GPU
# ────────────────────────────────────────────────────────────────────────────

class LocalHFTeacher(AnnotatorBase):
    """Runs a HuggingFace causal LM locally — no API, no rate limit.

    For an 11 GB GPU (GTX 1080 Ti), recommended defaults:
      - Qwen/Qwen2.5-3B-Instruct in fp16 (no quantization needed; ~6 GB)
      - meta-llama/Llama-3.2-3B-Instruct in fp16 (~6 GB)
      - Qwen/Qwen2.5-7B-Instruct + 4-bit quantization (~4.5 GB,
        requires bitsandbytes; Pascal support via bnb≥0.42)

    Trade-off: a 3-7B teacher is weaker than a 70B teacher, so silver
    label quality is lower. Defensible if (a) you can't get API
    budget, or (b) you spot-check silver against held-out gold.

    Important: this loads a model into GPU memory. Free it (call
    `release()`) before training the student so they don't compete.
    """
    name = "local_hf"

    def __init__(self, cfg: TeacherConfig):
        super().__init__(cfg)
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
        except ImportError as e:
            raise RuntimeError(
                "pip install torch transformers (already in our deps)") from e

        model_name = cfg.model or "Qwen/Qwen2.5-3B-Instruct"
        print(f"[teacher:local_hf] loading {model_name} "
              f"(quant={cfg.quantization})")

        load_kwargs: dict = {"torch_dtype": torch.float16}
        if cfg.quantization in ("4bit", "8bit"):
            try:
                from transformers import BitsAndBytesConfig
                load_kwargs["quantization_config"] = BitsAndBytesConfig(
                    load_in_4bit=(cfg.quantization == "4bit"),
                    load_in_8bit=(cfg.quantization == "8bit"),
                    bnb_4bit_compute_dtype=torch.float16,
                )
            except ImportError as e:
                raise RuntimeError(
                    "pip install bitsandbytes for quantization") from e

        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Many causal LMs lack a pad token by default — use EOS.
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        self._model = AutoModelForCausalLM.from_pretrained(
            model_name, **load_kwargs,
        )
        # device_map="auto" would also work, but we pin to a single device
        # so memory is predictable on a single-GPU machine.
        device = cfg.device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        if cfg.quantization == "none":
            self._model.to(device)
        self._device = device
        self._model.eval()
        self._torch = torch
        self._n_today = 0
        print(f"[teacher:local_hf] ready on {device}")

    def annotate(self, text: str, source: str) -> tuple[ArgStructureDict, str]:
        if self._n_today >= self.cfg.max_requests_per_day:
            return _empty_structure(), "[teacher: daily cap reached]"

        prompt_user = _build_user_prompt(text, source, self.cfg.max_input_chars)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt_user},
        ]

        # Canonical Qwen/Llama-3 chat pattern:
        #   1) apply_chat_template(..., tokenize=False) → str
        #   2) tokenizer([str], return_tensors="pt") → BatchEncoding with
        #      proper [batch, seq] shapes AND attention_mask
        #   3) model.generate(**inputs) — uses attention_mask, no shape bugs
        # Previous shortcut returned a 1-D tensor on some tokenizers, which
        # silently broke generate() on certain transformers versions.
        try:
            try:
                prompt_str = self._tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True,
                )
            except Exception:
                prompt_str = SYSTEM_PROMPT + "\n\n" + prompt_user

            inputs = self._tokenizer(
                [prompt_str],
                return_tensors="pt",
                truncation=True,
                max_length=4096,
            ).to(self._device)

            with self._torch.no_grad():
                out = self._model.generate(
                    **inputs,
                    max_new_tokens=self.cfg.max_output_tokens,
                    do_sample=False,
                    pad_token_id=self._tokenizer.pad_token_id,
                    eos_token_id=self._tokenizer.eos_token_id,
                )
            input_len = inputs["input_ids"].shape[-1]
            new_tokens = out[0][input_len:]
            raw = self._tokenizer.decode(new_tokens, skip_special_tokens=True)
            self._n_today += 1
            return _extract_json(raw), _extract_cot(raw)
        except Exception as e:
            # Surface the real error: previous silent except hid the cause.
            # We print once per failure so the log shows what's actually
            # wrong instead of just `[teacher error: ]`.
            import traceback as _tb
            err_str = f"{type(e).__name__}: {e}"
            # Print only the first ~3 frames so the log doesn't explode
            tb_short = "".join(_tb.format_exception(type(e), e, e.__traceback__))[-1500:]
            print(f"[teacher:local_hf] ERROR — {err_str}\n{tb_short}",
                  flush=True)
            return _empty_structure(), f"[teacher error: {err_str}]"

    def release(self) -> None:
        """Free GPU memory before student training takes the GPU."""
        try:
            del self._model
            self._torch.cuda.empty_cache()
            print("[teacher:local_hf] released GPU memory")
        except Exception:
            pass


# ────────────────────────────────────────────────────────────────────────────
# Factory
# ────────────────────────────────────────────────────────────────────────────

def build_teacher(cfg: TeacherConfig) -> AnnotatorBase:
    if cfg.backend == "dummy":
        return DummyTeacher(cfg)
    if cfg.backend == "groq":
        return GroqTeacher(cfg)
    if cfg.backend == "hf_inference":
        return HFInferenceTeacher(cfg)
    if cfg.backend == "local_hf":
        return LocalHFTeacher(cfg)
    # Hooks for future backends — kept as explicit raises so config typos
    # don't silently fall through to dummy.
    if cfg.backend == "openai":
        raise NotImplementedError("OpenAI teacher: implement in teacher.py")
    if cfg.backend == "anthropic":
        raise NotImplementedError("Anthropic teacher: implement in teacher.py")
    raise ValueError(f"Unknown teacher backend: {cfg.backend}")
