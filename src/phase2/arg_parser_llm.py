"""ArgParserLLM — Phase 1 integration adapter.

Wraps a trained student (or a dummy) and exposes the same parse()
interface that Phase 1's GoldArgParser does, so swapping is a one-line
change in Phase 1's pipeline construction.

Two parse methods:
  - parse(row_id)        : Phase 1 compatibility — looks up text from
                           a LIARArg-style row registry, runs the student,
                           returns the typed Phase 1 ArgStructure.
  - parse_text(text)     : cross-domain / standalone — useful for ARIES
                           rows during evaluation.

Conversion ArgStructureDict (JSON shape) → ArgStructure (typed) happens
here. Lookup tables fill in source_text/target_text on relations because
Phase 1's ArgRelation carries the resolved text alongside the IDs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

# Phase 1 types — imported lazily inside methods to avoid hard
# coupling at import time (the scaffold needs to be importable from a
# clean checkout even before Phase 1 wiring is rebuilt).
from .schema import ArgStructureDict
from .student import StudentTrainerBase


@dataclass
class ArgParserLLMConfig:
    # If True, when the student predicts no components at all, fall back
    # to treating the entire input as one claim (no premises). This
    # prevents downstream NaN F1 on inputs the student can't parse.
    fallback_to_single_claim: bool = True

    # If True, drop relations whose src or tgt don't appear in the
    # predicted component set (the student sometimes hallucinates IDs).
    drop_dangling_relations: bool = True


class ArgParserLLM:
    """Adapter from a trained Student to Phase 1's ArgStructure interface."""

    def __init__(
        self,
        student: StudentTrainerBase,
        row_to_text: Optional[Callable[[int], str]] = None,
        row_to_statement: Optional[Callable[[int], str]] = None,
        cfg: Optional[ArgParserLLMConfig] = None,
    ):
        """
        Args:
            student: a trained (or dummy) StudentTrainerBase.
                     Must have .load() already called if it's a real HF model.
            row_to_text: callable that returns the text passed to the student
                         given a row_id. For LIARArg this is typically
                         `statement + " " + justification`.
            row_to_statement: callable that returns the bare statement string
                              (used as ArgStructure.statement). Defaults to
                              row_to_text if not provided.
            cfg: ArgParserLLMConfig (defensive parsing options).
        """
        self.student = student
        self.row_to_text = row_to_text
        self.row_to_statement = row_to_statement or row_to_text
        self.cfg = cfg or ArgParserLLMConfig()

    # ─────────── Phase 1 compatibility ───────────
    def parse(self, row_id: int):
        """Same signature as GoldArgParser.parse(row_id)."""
        if self.row_to_text is None:
            raise RuntimeError(
                "ArgParserLLM.parse(row_id) needs row_to_text wired up. "
                "Either pass row_to_text= at construction, or call "
                "parse_text(text) directly.")
        text = self.row_to_text(row_id)
        statement = (self.row_to_statement(row_id)
                     if self.row_to_statement else text)
        return self._parse_text_with_statement(text, statement)

    # ─────────── Standalone / cross-domain ───────────
    def parse_text(self, text: str, statement: Optional[str] = None):
        """Parse arbitrary text. Useful for ARIES held-out evaluation."""
        return self._parse_text_with_statement(text, statement or text)

    # ─────────── Internal: dict → Phase 1 typed ───────────
    def _parse_text_with_statement(self, text: str, statement: str):
        structure_dict, _reasoning = self.student.predict(text)
        return self._dict_to_typed(structure_dict, statement)

    def _dict_to_typed(self, d: ArgStructureDict, statement: str):
        """Convert ArgStructureDict → Phase 1's ArgStructure dataclass."""
        # Lazy import — Phase 1 path; matches current repo layout.
        from src.arg_parser import (
            ArgStructure, ArgComponent, ArgRelation,
        )

        claims    = [self._mk_component(c, "claim",    ArgComponent)
                     for c in d.get("claim_components", [])]
        premises  = [self._mk_component(c, "premise",  ArgComponent)
                     for c in d.get("premise_components", [])]
        citations = [self._mk_component(c, "citation", ArgComponent)
                     for c in d.get("citation_components", [])]

        # Empty-prediction fallback
        if (not claims and not premises and not citations
                and self.cfg.fallback_to_single_claim):
            claims = [ArgComponent(id=1, text=statement[:500], kind="claim")]

        # Build text lookup for relations
        all_comps = {c.id: c for c in claims + premises + citations}

        relations = []
        for r in d.get("relations", []):
            src_id, tgt_id = r.get("src"), r.get("tgt")
            role = r.get("type", "support")
            if self.cfg.drop_dangling_relations:
                if src_id not in all_comps or tgt_id not in all_comps:
                    continue
            src_text = all_comps[src_id].text if src_id in all_comps else ""
            tgt_text = all_comps[tgt_id].text if tgt_id in all_comps else ""
            relations.append(ArgRelation(
                source_id=src_id, target_id=tgt_id, role=role,
                source_text=src_text, target_text=tgt_text,
            ))

        return ArgStructure(
            statement=statement,
            claim_components=claims,
            premise_components=premises,
            citation_components=citations,
            relations=relations,
        )

    @staticmethod
    def _mk_component(c: dict, default_kind: str, ArgComponentCls):
        return ArgComponentCls(
            id=int(c.get("id", 0)),
            text=str(c.get("text", "")),
            kind=c.get("type", default_kind),
        )


# ════════════════════════════════════════════════════════════════════════════
# FrozenArgParserLLM — drop-in for GoldArgParser, but reads pre-computed
# predictions instead of dereferencing CSV columns.
#
# Workflow:
#   1. Run scripts/phase2/parse_test_with_teacher.py on the GPU server to
#      produce a predictions JSONL: one line per row_id, with the predicted
#      ArgStructureDict from whatever teacher/student backend you choose.
#   2. Download the JSONL to the Mac.
#   3. In scripts/run_pipeline.py, swap GoldArgParser → FrozenArgParserLLM
#      and pass the JSONL path.
#   4. Phase 1's verifier (Ollama-hosted Qwen-14B) consumes the learned
#      argument structure exactly as it consumed gold.
#
# This separates the GPU-heavy parser inference (uni server) from the
# Ollama-heavy verifier inference (Mac), and makes the parser stage
# reproducible: re-running Phase 1 doesn't re-invoke the LLM.
# ════════════════════════════════════════════════════════════════════════════

import json as _json
from pathlib import Path as _Path


class FrozenArgParserLLM:
    """Same .parse(row_id) -> ArgStructure interface as GoldArgParser, but
    backed by a JSONL of pre-computed predictions.

    Each line of the JSONL must be:
        {"row_id": <int>,
         "prediction": {"claim_components": [...],
                        "premise_components": [...],
                        "citation_components": [...],
                        "relations": [...]}}

    Missing keys default to []; rows not in the JSONL fall back to a
    single-claim ArgStructure built from the row's statement (defensive,
    so a missing prediction doesn't crash the whole pipeline).
    """

    def __init__(
        self,
        rows_by_id: dict,                   # dict[int, LIARArgRow] from Phase 1
        predictions_path: str | _Path,
        cfg: ArgParserLLMConfig | None = None,
    ):
        self.rows_by_id = rows_by_id
        self.cfg = cfg or ArgParserLLMConfig()
        self.predictions_path = str(predictions_path)
        self.preds: dict[int, dict] = {}
        self._load()

    def _load(self) -> None:
        path = _Path(self.predictions_path)
        if not path.exists():
            raise FileNotFoundError(
                f"frozen predictions not found: {self.predictions_path}")
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = _json.loads(line)
                    self.preds[int(rec["row_id"])] = rec["prediction"]
                except (KeyError, ValueError, _json.JSONDecodeError):
                    continue
        print(f"[FrozenArgParserLLM] loaded {len(self.preds)} predictions "
              f"from {self.predictions_path}")

    def parse(self, row_id: int):
        from src.arg_parser import ArgStructure, ArgComponent, ArgRelation

        if row_id not in self.rows_by_id:
            raise KeyError(f"Unknown row id {row_id}")
        row = self.rows_by_id[row_id]
        statement = getattr(row, "statement", "")

        pred = self.preds.get(int(row_id))
        if pred is None:
            # Defensive fallback: single-claim structure from the statement.
            # Better than crashing — lets the verifier degrade gracefully.
            if self.cfg.fallback_to_single_claim:
                return ArgStructure(
                    statement=statement,
                    claim_components=[ArgComponent(id=1, text=statement[:500],
                                                   kind="claim")],
                    premise_components=[],
                    citation_components=[],
                    relations=[],
                )
            return ArgStructure(
                statement=statement,
                claim_components=[], premise_components=[],
                citation_components=[], relations=[],
            )

        # Reuse the dict→typed conversion from ArgParserLLM
        adapter = ArgParserLLM(student=None, cfg=self.cfg)  # student unused here
        return adapter._dict_to_typed(pred, statement)

