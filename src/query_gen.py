"""Role-targeted query generator.

For each argumentative relation in the parsed structure we emit one retrieval
query that explicitly seeks evidence playing that role:

  - support relation: query asks for passages CONFIRMING the claim
  - attack relation:  query asks for passages CHALLENGING the claim
  - psupport / pattack: same intent, weaker phrasing ("partially")

The premise text itself is the strongest signal we have for what the
fact-checker actually had to verify, so each query is anchored on the
premise (with the claim included for topical context). A flat-RAG baseline
generator is also provided.
"""
from __future__ import annotations

from dataclasses import dataclass

from .arg_parser import ArgStructure, ArgRelation


@dataclass
class TargetedQuery:
    role: str                  # "support" | "attack" | "psupport" | "pattack" | "flat"
    query_text: str            # text issued to the retriever
    claim_text: str            # the claim being verified
    premise_text: str          # the gold premise this query addresses (empty for flat)
    relation: ArgRelation | None = None


# Role-specific intent prefixes; the retriever sees these as plain text.
_INTENT = {
    "support": "Evidence confirming that",
    "attack": "Evidence contradicting or refuting that",
    "psupport": "Evidence partially confirming or qualifying support that",
    "pattack": "Evidence partially refuting or qualifying that",
}


def _normalise(text: str) -> str:
    return " ".join(str(text).split())


def generate_targeted_queries(struct: ArgStructure) -> list[TargetedQuery]:
    """Generate one query per argumentative relation."""
    queries: list[TargetedQuery] = []
    claim_text = struct.statement or (
        struct.claim_components[0].text if struct.claim_components else ""
    )
    claim_text = _normalise(claim_text)

    for rel in struct.relations:
        intent = _INTENT.get(rel.role, "Evidence about")
        premise = _normalise(rel.source_text)
        # Targeted query: intent + premise (the specific point) + claim (topical anchor)
        # The premise is what the fact-checker actually needed to verify;
        # the claim keeps the retrieval on-topic.
        if premise:
            qtext = f"{intent}: {premise}. Context claim: {claim_text}"
        else:
            qtext = f"{intent} the claim: {claim_text}"
        queries.append(TargetedQuery(
            role=rel.role,
            query_text=qtext,
            claim_text=claim_text,
            premise_text=premise,
            relation=rel,
        ))

    # Edge case: a claim with no annotated relations falls back to a flat query
    # so the pipeline still has something to retrieve.
    if not queries:
        queries.append(TargetedQuery(
            role="flat",
            query_text=claim_text,
            claim_text=claim_text,
            premise_text="",
            relation=None,
        ))
    return queries


def generate_flat_query(struct: ArgStructure) -> TargetedQuery:
    """Flat-RAG baseline: a single topic-similarity query."""
    claim_text = struct.statement or (
        struct.claim_components[0].text if struct.claim_components else ""
    )
    return TargetedQuery(
        role="flat",
        query_text=_normalise(claim_text),
        claim_text=_normalise(claim_text),
        premise_text="",
        relation=None,
    )
