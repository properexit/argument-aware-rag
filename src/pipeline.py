"""End-to-end orchestration of the 5 pipeline stages.

Stage 1: parse argument structure (gold in Phase 1).
Stage 2: generate role-targeted queries.
Stage 3: hybrid retrieve per query.
Stage 4: role-aware re-rank per query.
Stage 5: synthesise the verdict.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional

from .arg_parser import GoldArgParser, ArgStructure
from .data_loader import LIARArgRow
from .query_gen import (
    TargetedQuery,
    generate_targeted_queries,
    generate_flat_query,
)
from .retriever import HybridRetriever, RetrievedPassage
from .reranker import RoleAwareReranker, RerankedPassage
from .verifier import VerdictSynthesiser, Verdict


@dataclass
class PipelineResult:
    row_id: int
    statement: str
    gold_label: str
    predicted_label: str
    rationale: str
    mode: str                    # "arg_aware" | "flat"
    queries: list[dict]
    role_evidence: dict[str, list[dict]]


class ArgAwareRAGPipeline:

    def __init__(
        self,
        parser: GoldArgParser,
        retriever: HybridRetriever,
        reranker: Optional[RoleAwareReranker],
        verifier: VerdictSynthesiser,
        top_k_per_query: int = 20,
        final_top_k_per_role: int = 5,
    ):
        self.parser = parser
        self.retriever = retriever
        self.reranker = reranker
        self.verifier = verifier
        self.top_k_per_query = top_k_per_query
        self.final_top_k_per_role = final_top_k_per_role

    # ------------------------------------------------------------------
    # Argument-aware mode
    # ------------------------------------------------------------------

    def run(self, row: LIARArgRow) -> PipelineResult:
        struct: ArgStructure = self.parser.parse(row.id)
        queries: list[TargetedQuery] = generate_targeted_queries(struct)

        role_evidence: dict[str, list[RerankedPassage]] = {
            "support": [], "attack": [], "psupport": [], "pattack": [], "flat": []
        }
        queries_log = []
        seen_passages: set[str] = set()

        for q in queries:
            retrieved = self.retriever.search(
                q.query_text,
                top_k=self.top_k_per_query,
                exclude_row_ids={row.id},   # don't retrieve from the same article
            )
            if self.reranker is not None:
                reranked = self.reranker.rerank(q, retrieved)
            else:
                # Wrap raw retrieval as RerankedPassage with role_fit=score
                reranked = [
                    RerankedPassage(
                        retrieved=rp, role_fit=rp.score, final_score=rp.score,
                        nli_label="neutral",
                    )
                    for rp in retrieved
                ]
            # Keep best K and dedupe by passage id across queries for this row
            kept: list[RerankedPassage] = []
            for rp in reranked:
                pid = rp.retrieved.passage.passage_id
                if pid in seen_passages:
                    continue
                seen_passages.add(pid)
                kept.append(rp)
                if len(kept) >= self.final_top_k_per_role:
                    break
            role_evidence.setdefault(q.role, []).extend(kept)

            queries_log.append({
                "role": q.role,
                "query_text": q.query_text,
                "premise_text": q.premise_text,
                "n_retrieved": len(retrieved),
                "n_kept": len(kept),
            })

        verdict = self.verifier.verdict(struct.statement, role_evidence)

        return PipelineResult(
            row_id=row.id,
            statement=struct.statement,
            gold_label=row.label,
            predicted_label=verdict.label,
            rationale=verdict.rationale,
            mode="arg_aware",
            queries=queries_log,
            role_evidence={
                role: [
                    {
                        "passage_id": ev.retrieved.passage.passage_id,
                        "text": ev.retrieved.passage.text,
                        "role_fit": ev.role_fit,
                        "final_score": ev.final_score,
                        "nli_label": ev.nli_label,
                    }
                    for ev in evs
                ]
                for role, evs in role_evidence.items() if evs
            },
        )

    # ------------------------------------------------------------------
    # Flat-RAG baseline (single topical query, no role re-ranking)
    # ------------------------------------------------------------------

    def run_flat(self, row: LIARArgRow) -> PipelineResult:
        struct: ArgStructure = self.parser.parse(row.id)
        q = generate_flat_query(struct)
        retrieved = self.retriever.search(
            q.query_text,
            top_k=self.top_k_per_query,
            exclude_row_ids={row.id},
        )
        # No role re-ranking; treat all as "flat" and rely on the verifier
        reranked = [
            RerankedPassage(
                retrieved=rp, role_fit=rp.score, final_score=rp.score,
                nli_label="neutral",
            )
            for rp in retrieved[: self.final_top_k_per_role]
        ]
        role_evidence = {"flat": reranked}
        verdict = self.verifier.verdict(struct.statement, role_evidence)
        return PipelineResult(
            row_id=row.id,
            statement=struct.statement,
            gold_label=row.label,
            predicted_label=verdict.label,
            rationale=verdict.rationale,
            mode="flat",
            queries=[{"role": "flat", "query_text": q.query_text, "premise_text": "",
                      "n_retrieved": len(retrieved), "n_kept": len(reranked)}],
            role_evidence={
                "flat": [
                    {
                        "passage_id": ev.retrieved.passage.passage_id,
                        "text": ev.retrieved.passage.text,
                        "role_fit": ev.role_fit,
                        "final_score": ev.final_score,
                        "nli_label": ev.nli_label,
                    }
                    for ev in reranked
                ]
            },
        )
