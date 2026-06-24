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
# Factory
# ────────────────────────────────────────────────────────────────────────────

def build_teacher(cfg: TeacherConfig) -> AnnotatorBase:
    if cfg.backend == "dummy":
        return DummyTeacher(cfg)
    if cfg.backend == "groq":
        return GroqTeacher(cfg)
    # Hooks for future backends — kept as explicit raises so config typos
    # don't silently fall through to dummy.
    if cfg.backend == "openai":
        raise NotImplementedError("OpenAI teacher: implement in teacher.py")
    if cfg.backend == "anthropic":
        raise NotImplementedError("Anthropic teacher: implement in teacher.py")
    raise ValueError(f"Unknown teacher backend: {cfg.backend}")
