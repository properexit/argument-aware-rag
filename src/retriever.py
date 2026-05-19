"""Hybrid retriever: BM25 + dense embeddings fused with Reciprocal Rank Fusion.

The retrieval corpus is the union of paragraph-level passages drawn from
LIARArg justifications. Each passage is tagged with the source claim id so
we can exclude same-claim passages from retrieval (avoiding trivial leakage
of the gold justification at evaluation time).
"""
from __future__ import annotations

import ast
import json
import os
import re
from dataclasses import dataclass, asdict
from typing import Iterable

import numpy as np
from rank_bm25 import BM25Okapi


# ---------------------------------------------------------------------------
# Passage representation
# ---------------------------------------------------------------------------

@dataclass
class Passage:
    passage_id: str          # "<row_id>::<paragraph_index>"
    source_row_id: int       # LIARArg row this paragraph came from
    paragraph_index: int
    text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RetrievedPassage:
    passage: Passage
    score: float
    rank: int
    retriever: str           # "bm25" | "dense" | "rrf"


# ---------------------------------------------------------------------------
# Corpus building
# ---------------------------------------------------------------------------

_PARA_PATTERN = re.compile(r"\n+")
_WORD_RE = re.compile(r"[A-Za-z0-9']+")


def _split_paragraphs(text: str) -> list[str]:
    if not text:
        return []
    parts = [p.strip() for p in _PARA_PATTERN.split(str(text)) if p.strip()]
    # Drop very short paragraphs (likely headers/noise)
    return [p for p in parts if len(p.split()) >= 6]


def build_corpus_from_rows(rows: Iterable) -> list[Passage]:
    """Build a paragraph-level passage corpus.

    Each row's `paragraph_based_content` is a list of paragraphs (the fact-
    checker's article body). We index every paragraph and tag it with the
    originating row id so we can exclude same-claim paragraphs at query time.
    """
    passages: list[Passage] = []
    for r in rows:
        # `r` may be a LIARArgRow or a plain dict
        row_id = getattr(r, "id", None) or r.get("id")
        full_text = getattr(r, "full_text", "") or r.get("full_text", "")
        paragraphs = _split_paragraphs(full_text)
        for j, p in enumerate(paragraphs):
            passages.append(Passage(
                passage_id=f"{row_id}::{j}",
                source_row_id=int(row_id),
                paragraph_index=j,
                text=p,
            ))
    return passages


def build_corpus_from_dataframe(df) -> list[Passage]:
    """Build the corpus directly from the raw CSV dataframe.

    Used when we want the retrieval pool to span the whole dataset (train +
    val + test) but with a per-query exclusion of same-row passages.
    """
    passages: list[Passage] = []
    for _, row in df.iterrows():
        row_id = int(row["id"])
        paras = row.get("paragraph_based_content", "")
        try:
            parts = ast.literal_eval(paras) if isinstance(paras, str) else paras
            if not isinstance(parts, list):
                parts = _split_paragraphs(str(paras))
        except (ValueError, SyntaxError):
            parts = _split_paragraphs(str(paras))
        for j, p in enumerate(parts):
            text = str(p).strip()
            if len(text.split()) < 6:
                continue
            passages.append(Passage(
                passage_id=f"{row_id}::{j}",
                source_row_id=row_id,
                paragraph_index=j,
                text=text,
            ))
    return passages


# ---------------------------------------------------------------------------
# Tokeniser
# ---------------------------------------------------------------------------

def _tokenise(text: str) -> list[str]:
    return [t.lower() for t in _WORD_RE.findall(text or "")]


# ---------------------------------------------------------------------------
# Hybrid retriever
# ---------------------------------------------------------------------------

class HybridRetriever:
    """BM25 + dense retriever fused with Reciprocal Rank Fusion."""

    def __init__(
        self,
        passages: list[Passage],
        dense_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str = "cpu",
        use_bm25: bool = True,
        use_dense: bool = True,
        rrf_k: int = 60,
    ):
        self.passages = passages
        self.use_bm25 = use_bm25
        self.use_dense = use_dense
        self.rrf_k = rrf_k

        self._bm25 = None
        self._dense_model = None
        self._dense_emb = None
        self._dense_model_name = dense_model_name
        self._device = device

        self._tokenised: list[list[str]] | None = None
        self._passage_id_to_idx = {p.passage_id: i for i, p in enumerate(passages)}

    # -- index build -------------------------------------------------------

    def build(self, dense_batch_size: int = 64, verbose: bool = True) -> None:
        if self.use_bm25:
            if verbose:
                print(f"[retriever] building BM25 over {len(self.passages)} passages")
            self._tokenised = [_tokenise(p.text) for p in self.passages]
            self._bm25 = BM25Okapi(self._tokenised)

        if self.use_dense:
            from sentence_transformers import SentenceTransformer
            if verbose:
                print(f"[retriever] loading dense model {self._dense_model_name}")
            self._dense_model = SentenceTransformer(self._dense_model_name, device=self._device)
            if verbose:
                print(f"[retriever] encoding {len(self.passages)} passages")
            texts = [p.text for p in self.passages]
            self._dense_emb = self._dense_model.encode(
                texts,
                batch_size=dense_batch_size,
                show_progress_bar=verbose,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )

    # -- single-retriever search ------------------------------------------

    def _bm25_search(self, query: str, top_k: int) -> list[tuple[int, float]]:
        scores = self._bm25.get_scores(_tokenise(query))
        idx = np.argsort(-scores)[:top_k]
        return [(int(i), float(scores[i])) for i in idx]

    def _dense_search(self, query: str, top_k: int) -> list[tuple[int, float]]:
        qv = self._dense_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]
        sims = self._dense_emb @ qv
        idx = np.argsort(-sims)[:top_k]
        return [(int(i), float(sims[i])) for i in idx]

    # -- fusion ------------------------------------------------------------

    def _rrf(
        self,
        bm25_hits: list[tuple[int, float]],
        dense_hits: list[tuple[int, float]],
    ) -> list[tuple[int, float]]:
        scores: dict[int, float] = {}
        for rank, (idx, _) in enumerate(bm25_hits):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (self.rrf_k + rank + 1)
        for rank, (idx, _) in enumerate(dense_hits):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (self.rrf_k + rank + 1)
        return sorted(scores.items(), key=lambda x: -x[1])

    # -- public API --------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 20,
        exclude_row_ids: set[int] | None = None,
        per_retriever_pool: int = 50,
    ) -> list[RetrievedPassage]:
        exclude = exclude_row_ids or set()

        bm25_hits: list[tuple[int, float]] = []
        dense_hits: list[tuple[int, float]] = []
        if self.use_bm25:
            bm25_hits = self._bm25_search(query, per_retriever_pool)
        if self.use_dense:
            dense_hits = self._dense_search(query, per_retriever_pool)

        if self.use_bm25 and self.use_dense:
            fused = self._rrf(bm25_hits, dense_hits)
            retriever_tag = "rrf"
        elif self.use_bm25:
            fused = bm25_hits
            retriever_tag = "bm25"
        else:
            fused = dense_hits
            retriever_tag = "dense"

        out: list[RetrievedPassage] = []
        for idx, score in fused:
            p = self.passages[idx]
            if p.source_row_id in exclude:
                continue
            out.append(RetrievedPassage(
                passage=p, score=float(score),
                rank=len(out) + 1, retriever=retriever_tag,
            ))
            if len(out) >= top_k:
                break
        return out

    # -- persistence -------------------------------------------------------

    def save(self, out_dir: str) -> None:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "passages.jsonl"), "w") as f:
            for p in self.passages:
                f.write(json.dumps(p.to_dict()) + "\n")
        if self._dense_emb is not None:
            np.save(os.path.join(out_dir, "dense.npy"), self._dense_emb)
        meta = {
            "dense_model_name": self._dense_model_name,
            "use_bm25": self.use_bm25,
            "use_dense": self.use_dense,
            "rrf_k": self.rrf_k,
            "n_passages": len(self.passages),
        }
        with open(os.path.join(out_dir, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)

    @classmethod
    def load(cls, in_dir: str, device: str = "cpu") -> "HybridRetriever":
        with open(os.path.join(in_dir, "meta.json")) as f:
            meta = json.load(f)
        passages = []
        with open(os.path.join(in_dir, "passages.jsonl")) as f:
            for line in f:
                passages.append(Passage(**json.loads(line)))
        ret = cls(
            passages=passages,
            dense_model_name=meta["dense_model_name"],
            device=device,
            use_bm25=meta["use_bm25"],
            use_dense=meta["use_dense"],
            rrf_k=meta["rrf_k"],
        )
        if ret.use_bm25:
            ret._tokenised = [_tokenise(p.text) for p in passages]
            ret._bm25 = BM25Okapi(ret._tokenised)
        if ret.use_dense:
            from sentence_transformers import SentenceTransformer
            ret._dense_model = SentenceTransformer(meta["dense_model_name"], device=device)
            ret._dense_emb = np.load(os.path.join(in_dir, "dense.npy"))
        return ret
