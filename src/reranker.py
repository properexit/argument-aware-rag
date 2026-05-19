"""Role-aware re-ranker.

After retrieval, each candidate passage carries a generic relevance score
(BM25 / dense / RRF) — i.e. *topical* similarity. The re-ranker re-scores
each passage by how well it fulfils the argumentative role we asked for:

  - For a `support` query, a good passage should ENTAIL the premise.
  - For an `attack` query, a good passage should CONTRADICT the premise.
  - Partial variants get a softer threshold.

We use an off-the-shelf NLI cross-encoder (`cross-encoder/nli-deberta-v3-small`)
which scores each (passage, premise) pair with [entailment, neutral, contradiction]
probabilities. The role-fit score is then a function of these probabilities.
"""
from __future__ import annotations

from dataclasses import dataclass

from .retriever import RetrievedPassage
from .query_gen import TargetedQuery


@dataclass
class RerankedPassage:
    retrieved: RetrievedPassage
    role_fit: float          # 0..1, how well the passage plays its target role
    final_score: float       # weighted combination of role_fit and original score
    nli_label: str           # "entailment" | "contradiction" | "neutral"


class RoleAwareReranker:
    """NLI-driven re-ranker."""

    NLI_LABELS = ["contradiction", "neutral", "entailment"]   # deberta-v3 NLI order

    def __init__(
        self,
        model_name: str = "cross-encoder/nli-deberta-v3-small",
        device: str = "cpu",
        role_weight: float = 0.7,
        rrf_weight: float = 0.3,
    ):
        self.model_name = model_name
        self.device = device
        self.role_weight = role_weight
        self.rrf_weight = rrf_weight
        self._model = None

    def _ensure_model(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name, device=self.device)

    @staticmethod
    def _role_fit(probs: dict[str, float], role: str) -> tuple[float, str]:
        """Translate NLI probs into a role-fit score in [0,1] and a label tag."""
        ent = probs["entailment"]
        con = probs["contradiction"]
        neu = probs["neutral"]

        if role in ("support", "psupport"):
            # We want entailment, penalise contradiction
            fit = ent - 0.5 * con
            soft = 0.5 if role == "psupport" else 1.0  # partial counts less
            fit = max(0.0, min(1.0, (fit + 0.5))) * soft
        elif role in ("attack", "pattack"):
            fit = con - 0.5 * ent
            soft = 0.5 if role == "pattack" else 1.0
            fit = max(0.0, min(1.0, (fit + 0.5))) * soft
        else:  # "flat" or unknown: rely on non-neutrality
            fit = max(ent, con) * (1.0 - neu)
        # Pick the label tag for transparency in outputs
        label = max(probs, key=probs.get)
        return float(fit), label

    def rerank(
        self,
        query: TargetedQuery,
        passages: list[RetrievedPassage],
    ) -> list[RerankedPassage]:
        if not passages:
            return []
        self._ensure_model()

        # Premise is the hypothesis the passage must (dis)prove. If no premise
        # is available (flat fallback), use the claim itself.
        hypothesis = query.premise_text or query.claim_text
        pairs = [(rp.passage.text, hypothesis) for rp in passages]

        # CrossEncoder returns raw logits for the 3 NLI classes
        import numpy as np
        scores = self._model.predict(pairs, convert_to_numpy=True)
        # Convert to probabilities
        e_x = np.exp(scores - scores.max(axis=1, keepdims=True))
        probs = e_x / e_x.sum(axis=1, keepdims=True)

        out: list[RerankedPassage] = []
        # Normalise original retrieval scores into a 0..1 range
        raw = [rp.score for rp in passages]
        rmin, rmax = (min(raw), max(raw)) if raw else (0.0, 1.0)
        rng = (rmax - rmin) or 1.0

        for i, rp in enumerate(passages):
            p = {lbl: float(probs[i][j]) for j, lbl in enumerate(self.NLI_LABELS)}
            fit, label = self._role_fit(p, query.role)
            norm = (rp.score - rmin) / rng
            final = self.role_weight * fit + self.rrf_weight * norm
            out.append(RerankedPassage(
                retrieved=rp, role_fit=fit, final_score=float(final),
                nli_label=label,
            ))

        out.sort(key=lambda x: -x.final_score)
        return out
