"""Argument parser interface.

Phase 1 uses gold annotations from LIARArg directly: this module simply
reshapes the already-parsed `LIARArgRow` into an `ArgStructure` view that
matches what a learned parser (Phase 2 ArgParserLLM) will eventually return.

Keeping a single `ArgStructure` interface makes the parser swap trivial: only
this file needs to change in Phase 2.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .data_loader import LIARArgRow


Role = Literal["support", "attack", "psupport", "pattack"]


@dataclass
class ArgComponent:
    """A single argumentative component (claim, premise, or citation)."""
    id: int
    text: str
    kind: Literal["claim", "premise", "citation"]


@dataclass
class ArgRelation:
    """A directed argumentative relation between two components."""
    source_id: int       # premise/citation supplying the argument
    target_id: int       # claim being supported/attacked
    role: Role
    source_text: str
    target_text: str


@dataclass
class ArgStructure:
    """The full parsed argument structure for one claim."""
    statement: str
    claim_components: list[ArgComponent] = field(default_factory=list)
    premise_components: list[ArgComponent] = field(default_factory=list)
    citation_components: list[ArgComponent] = field(default_factory=list)
    relations: list[ArgRelation] = field(default_factory=list)

    @property
    def support_relations(self) -> list[ArgRelation]:
        return [r for r in self.relations if r.role in ("support", "psupport")]

    @property
    def attack_relations(self) -> list[ArgRelation]:
        return [r for r in self.relations if r.role in ("attack", "pattack")]

    def relations_by_role(self) -> dict[str, list[ArgRelation]]:
        out: dict[str, list[ArgRelation]] = {
            "support": [], "attack": [], "psupport": [], "pattack": []
        }
        for r in self.relations:
            out[r.role].append(r)
        return out


def parse_gold(row: LIARArgRow) -> ArgStructure:
    """Build an ArgStructure from gold LIARArg annotations."""
    id2text: dict[int, str] = {}

    claims = []
    for cid, ctext in zip(row.claim_ids, row.claim_texts):
        id2text[cid] = ctext
        claims.append(ArgComponent(id=cid, text=ctext, kind="claim"))

    premises = []
    for pid, ptext in zip(row.premise_ids, row.premise_texts):
        id2text[pid] = ptext
        premises.append(ArgComponent(id=pid, text=ptext, kind="premise"))

    citations = []
    for cid, ctext in zip(row.citation_ids, row.citation_texts):
        id2text[cid] = ctext
        citations.append(ArgComponent(id=cid, text=ctext, kind="citation"))

    def build_relations(pairs, role: Role) -> list[ArgRelation]:
        out = []
        for src, tgt in pairs:
            out.append(ArgRelation(
                source_id=src,
                target_id=tgt,
                role=role,
                source_text=id2text.get(src, ""),
                target_text=id2text.get(tgt, ""),
            ))
        return out

    relations: list[ArgRelation] = []
    relations += build_relations(row.support_relations, "support")
    relations += build_relations(row.attack_relations, "attack")
    relations += build_relations(row.psupport_relations, "psupport")
    relations += build_relations(row.pattack_relations, "pattack")

    return ArgStructure(
        statement=row.statement,
        claim_components=claims,
        premise_components=premises,
        citation_components=citations,
        relations=relations,
    )


class GoldArgParser:
    """Phase-1 parser: returns the gold ArgStructure for a LIARArg row.

    The `parse` method takes a row identifier so Phase-1 evaluation can run
    without ever touching free text. In Phase 2 this class is replaced by
    `ArgParserLLM`, which will accept raw text and predict the same structure.
    """

    def __init__(self, rows_by_id: dict[int, LIARArgRow]):
        self.rows_by_id = rows_by_id

    def parse(self, row_id: int) -> ArgStructure:
        if row_id not in self.rows_by_id:
            raise KeyError(f"Unknown row id {row_id}")
        return parse_gold(self.rows_by_id[row_id])
