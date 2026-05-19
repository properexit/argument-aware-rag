"""LLM verdict synthesiser.

Takes role-labelled, re-ranked evidence and produces a 6-way truthfulness
verdict in {True, Mostly-true, Half-true, Barely-true, False, Pants-fire}.

Three backends are supported:
  - "stub":      rule-based, no LLM. Computes a role-balance signal from the
                 role_fit scores and maps it to a label. Useful for fast iteration
                 and as a debuggable lower bound.
  - "ollama":    POST to a local Ollama server (e.g. llama3.1:8b-instruct).
  - "anthropic": (optional) call the Anthropic API via ANTHROPIC_API_KEY.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Literal

from .reranker import RerankedPassage
from .query_gen import TargetedQuery


LABELS = ["True", "Mostly-true", "Half-true", "Barely-true", "False", "Pants-fire"]


@dataclass
class Verdict:
    label: str
    rationale: str
    evidence_used: list[dict]


# ---------------------------------------------------------------------------
# Stub backend (rule-based)
# ---------------------------------------------------------------------------

def _stub_verdict(role_evidence: dict[str, list[RerankedPassage]]) -> Verdict:
    """Map role-balance to a label without calling an LLM.

    Uses two complementary signals so the result is robust to whatever
    `role_fit` magnitudes the upstream re-ranker (or its absence) produces:

    1. **Structural balance** — the counts of support vs attack passages.
       This is independent of raw score magnitude.
    2. **Mean role-fit** — for whichever side has more passages, how strong
       are they on average. Used as a tie-breaker.

    The 6-way label is selected by a logit derived from these signals.
    """
    sup_evs = role_evidence.get("support", []) + role_evidence.get("psupport", [])
    atk_evs = role_evidence.get("attack", []) + role_evidence.get("pattack", [])

    n_sup, n_atk = len(sup_evs), len(atk_evs)
    total = n_sup + n_atk

    if total == 0:
        # No structural evidence at all: fall back to flat passages, if any
        flat_evs = role_evidence.get("flat", [])
        # With no signal, predict the dataset's mode-ish middle label.
        label = "Half-true" if flat_evs else "Barely-true"
        rationale = f"Stub verdict (no argumentative evidence). n_flat={len(flat_evs)}."
        evidence: list[dict] = []
        for role, evs in role_evidence.items():
            for ev in evs:
                evidence.append({
                    "role": role,
                    "passage_id": ev.retrieved.passage.passage_id,
                    "text": ev.retrieved.passage.text,
                    "role_fit": ev.role_fit,
                    "nli_label": ev.nli_label,
                })
        return Verdict(label=label, rationale=rationale, evidence_used=evidence)

    # Signal 1: structural balance in [-1, 1]
    balance = (n_sup - n_atk) / total

    # Signal 2: mean role_fit per side (after per-side min-max normalisation)
    def _mean_norm(evs):
        if not evs:
            return 0.0
        scores = [ev.role_fit for ev in evs]
        lo, hi = min(scores), max(scores)
        rng = (hi - lo) or 1.0
        return sum((s - lo) / rng for s in scores) / len(scores)

    sup_strength = _mean_norm(sup_evs)
    atk_strength = _mean_norm(atk_evs)
    strength_diff = sup_strength - atk_strength            # in [-1, 1]

    # Combine: 0.7 weight on structural balance, 0.3 on strength
    signal = 0.7 * balance + 0.3 * strength_diff           # in [-1, 1]

    # Bucket into the 6-way scale
    if signal > 0.6:
        label = "True"
    elif signal > 0.2:
        label = "Mostly-true"
    elif signal > 0.0:
        label = "Half-true"
    elif signal > -0.2:
        label = "Barely-true"
    elif signal > -0.6:
        label = "False"
    else:
        label = "Pants-fire"

    evidence = []
    for role, evs in role_evidence.items():
        for ev in evs:
            evidence.append({
                "role": role,
                "passage_id": ev.retrieved.passage.passage_id,
                "text": ev.retrieved.passage.text,
                "role_fit": ev.role_fit,
                "nli_label": ev.nli_label,
            })
    rationale = (
        f"Stub verdict. n_support={n_sup} n_attack={n_atk} "
        f"balance={balance:+.2f} strength_diff={strength_diff:+.2f} "
        f"signal={signal:+.2f}."
    )
    return Verdict(label=label, rationale=rationale, evidence_used=evidence)


# ---------------------------------------------------------------------------
# Ollama backend
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are a PolitiFact-style fact-checking analyst. You will receive:
- A CLAIM being fact-checked
- A set of EVIDENCE passages, each tagged with its argumentative ROLE
  (support / attack / partial_support / partial_attack / topical)
- Optionally, a STRUCTURAL_PRIOR — the label that would follow purely from
  counting support vs attack relations. Treat this as a strong prior. Override
  it only if the evidence text clearly contradicts the structural balance.

Your task: assign exactly one label from this 6-point scale:
  True, Mostly-true, Half-true, Barely-true, False, Pants-fire

LABEL RUBRIC — read carefully:
  True         Evidence overwhelmingly supports the claim. No meaningful
               contradictions. Use this when support evidence dominates and
               attacks are absent or trivial.
  Mostly-true  Claim is accurate but needs minor clarification or omits a
               small qualifier. Support clearly outweighs attack.
  Half-true    Claim is partially accurate but leaves out important details
               or takes things out of context. Roughly balanced evidence.
  Barely-true  Claim contains an element of truth but ignores critical facts
               that change the impression. Attack outweighs support.
  False        Claim is not accurate. Attack evidence strongly dominates.
  Pants-fire   Claim is not accurate AND makes a ridiculous or fabricated
               assertion (e.g. invented quotes, impossible numbers,
               misattributed statements).

CRITICAL — READ TWICE:
The "attack" tag on a passage does NOT mean the claim is false. It
means the fact-checker recorded a caveat, qualification, or correction.
A claim that is **directionally correct with minor caveats** should be
labelled **Mostly-true**, NOT False. A claim that is roughly accurate
but missing important context should be **Half-true**, NOT False.

Reserve **False** for claims that are *substantively wrong* — wrong
direction, wrong magnitude by a lot, or contradicted by the evidence
on the central point. Reserve **Pants-fire** for fabricated quotes,
invented statistics, or impossible assertions.

Distribution sanity check: across PolitiFact, claims are roughly
evenly distributed across the 6 labels. If you find yourself wanting
to output "False" for most claims, you are over-correcting.

DECISION HEURISTIC:
  1. What does the claim's CENTRAL assertion say?
  2. Does the evidence confirm that central assertion?
       - Yes, fully and cleanly                       -> True
       - Yes, but with minor qualification or detail  -> Mostly-true
       - Partly — important details omitted/twisted   -> Half-true
       - Element of truth but misleads overall        -> Barely-true
       - Central assertion is wrong                   -> False
       - Central assertion is wrong AND absurd        -> Pants-fire
  3. Only after answering steps 1 and 2 should you tally support vs
     attack counts. The counts inform the verdict; they do not dictate
     it.

FEW-SHOT EXAMPLES (cover all six labels):

Example 1 — TRUE (one-sided support)
CLAIM: "Obama has more czars than the Romanovs"
EVIDENCE: Support passages enumerate ~28 Obama "czars" and ~18 Romanov
tsars. No contradicting evidence.
{"label": "True", "rationale": "Support evidence numerically confirms the comparison; no contradiction."}

Example 2 — MOSTLY-TRUE (correct direction with minor caveat)
CLAIM: "Wisconsin is dead last in the Midwest for job creation"
EVIDENCE: Several attack passages noting Wisconsin was tied for 9th of
10 in the relevant quarter, not strictly last. Other passages confirm
it was at or near the bottom.
{"label": "Mostly-true", "rationale": "Direction is correct; the caveat is minor (tied for last vs. strictly last)."}

Example 3 — HALF-TRUE (partial accuracy, omits important context)
CLAIM: "The Democratic Congress created over 500,000 new jobs this year"
EVIDENCE: Job-creation figure is roughly correct, but multiple
passages note Democrats deserve only partial credit and the recovery
was partly driven by prior-administration policies and broader trends.
{"label": "Half-true", "rationale": "Number is roughly accurate but credit-assignment is misleading; important context is omitted."}

Example 4 — BARELY-TRUE (kernel of truth, misleads overall)
CLAIM: "Bush 'borrowed' $1.37 trillion of Social Security surplus to
pay for tax cuts and the Iraq war"
EVIDENCE: Social Security surplus was indeed used for general
government spending under Bush, but this is standard practice under
every president since 1935 and the bonds are legally obligated to be
repaid — characterising it as "borrowed to pay for tax cuts" misleads.
{"label": "Barely-true", "rationale": "Element of truth (surplus was used), but framing implies wrongdoing where it was standard practice."}

Example 5 — FALSE (central assertion is wrong)
CLAIM: "New carbon regulations will kill 244,000 jobs a year and cost
average families $1,200 a year"
EVIDENCE: Multiple attack passages debunk the underlying study's
methodology, show the job number is overstated, and show the $1,200
figure was misattributed.
{"label": "False", "rationale": "Both central numerical claims are refuted by the underlying study's own author and by the agency cited."}

Example 6 — PANTS-FIRE (fabricated)
CLAIM: "Hillary Clinton told the Des Moines Register: 'I will get the
NRA shut down for good if I become president'"
EVIDENCE: Multiple passages confirm the quote is fabricated — Clinton
never said this; prior fact-checks rated identical claims Pants-on-Fire.
{"label": "Pants-fire", "rationale": "Quote is invented; no record exists. Previously rated Pants on Fire."}

OUTPUT FORMAT:
Reply with a strict JSON object on a single line:
{"label": "<one of the six>", "rationale": "<one or two sentences>"}
"""


def _build_user_prompt(
    claim: str,
    role_evidence: dict[str, list[RerankedPassage]],
    max_per_role: int = 3,
    structural_prior: str | None = None,
) -> str:
    lines = [f"CLAIM: {claim}\n"]
    if structural_prior:
        lines.append(f"STRUCTURAL_PRIOR: {structural_prior}")
        lines.append("(This label follows from counting support vs attack "
                     "relations. Use it as a strong starting point.)\n")
    lines.append("EVIDENCE:")
    role_display = {
        "support": "support",
        "attack": "attack",
        "psupport": "partial_support",
        "pattack": "partial_attack",
        "flat": "topical",
    }
    # Count for the prompt header so the LLM can see the balance at a glance
    n_sup = len(role_evidence.get("support", [])) + len(role_evidence.get("psupport", []))
    n_atk = len(role_evidence.get("attack", [])) + len(role_evidence.get("pattack", []))
    lines.append(f"(structural balance: {n_sup} support passages, "
                 f"{n_atk} attack passages)")
    for role, evs in role_evidence.items():
        for ev in evs[:max_per_role]:
            tag = role_display.get(role, role)
            lines.append(f"[{tag} | role_fit={ev.role_fit:.2f}] {ev.retrieved.passage.text}")
    lines.append('\nReply ONLY with a single-line JSON object: '
                 '{"label": "<one of: True, Mostly-true, Half-true, '
                 'Barely-true, False, Pants-fire>", "rationale": "..."}.')
    return "\n".join(lines)


def _parse_llm_json(raw: str) -> tuple[str, str]:
    """Robustly pull {label, rationale} out of an LLM response."""
    # Try direct JSON
    try:
        obj = json.loads(raw)
        return str(obj.get("label", "")).strip(), str(obj.get("rationale", "")).strip()
    except json.JSONDecodeError:
        pass
    # Try to extract first {...} block
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            return str(obj.get("label", "")).strip(), str(obj.get("rationale", "")).strip()
        except json.JSONDecodeError:
            pass
    # Fall back: search for one of the labels in the text
    for lab in LABELS:
        if lab.lower() in raw.lower():
            return lab, raw.strip()
    return "", raw.strip()


def _normalise_label(raw: str) -> str:
    """Map various LLM phrasings to the canonical 6-label scheme."""
    s = raw.strip().lower().replace("_", "-").replace(" ", "-")
    canonical = {l.lower(): l for l in LABELS}
    if s in canonical:
        return canonical[s]
    # Common aliases
    aliases = {
        "pants-on-fire": "Pants-fire", "pants on fire": "Pants-fire",
        "true.": "True", "false.": "False",
        "mostly true": "Mostly-true", "half true": "Half-true",
        "barely true": "Barely-true", "mostly-false": "Barely-true",
    }
    for k, v in aliases.items():
        if k in s:
            return v
    return ""


def _ollama_verdict(
    claim: str,
    role_evidence: dict[str, list[RerankedPassage]],
    base_url: str,
    model: str,
    max_evidence_per_role: int,
    use_structural_prior: bool = True,
) -> Verdict:
    import requests
    structural_prior = None
    if use_structural_prior:
        structural_prior = _stub_verdict(role_evidence).label
    prompt = _build_user_prompt(
        claim, role_evidence, max_evidence_per_role,
        structural_prior=structural_prior,
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        # temperature=0 picks the argmax token; seed pins any remaining
        # GPU/floating-point nondeterminism so reruns are bit-identical.
        "options": {"temperature": 0.0, "seed": 42, "top_p": 1.0},
    }
    try:
        resp = requests.post(
            f"{base_url.rstrip('/')}/api/chat",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        body = resp.json()
        content = body.get("message", {}).get("content", "")
    except Exception as e:
        # Fail-safe: fall back to stub if the local server is unreachable
        v = _stub_verdict(role_evidence)
        v.rationale = f"[ollama unreachable: {e}] {v.rationale}"
        return v

    raw_label, rationale = _parse_llm_json(content)
    label = _normalise_label(raw_label) or _stub_verdict(role_evidence).label

    evidence = []
    for role, evs in role_evidence.items():
        for ev in evs[:max_evidence_per_role]:
            evidence.append({
                "role": role,
                "passage_id": ev.retrieved.passage.passage_id,
                "text": ev.retrieved.passage.text,
                "role_fit": ev.role_fit,
                "nli_label": ev.nli_label,
            })
    return Verdict(label=label, rationale=rationale or content, evidence_used=evidence)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class VerdictSynthesiser:

    def __init__(
        self,
        backend: Literal["stub", "ollama", "anthropic"] = "stub",
        ollama_base_url: str = "http://localhost:11434",
        ollama_model: str = "llama3.1:8b-instruct",
        max_evidence_per_role: int = 3,
        use_structural_prior: bool = True,
    ):
        self.backend = backend
        self.ollama_base_url = ollama_base_url
        self.ollama_model = ollama_model
        self.max_evidence_per_role = max_evidence_per_role
        self.use_structural_prior = use_structural_prior

    def verdict(
        self,
        claim: str,
        role_evidence: dict[str, list[RerankedPassage]],
    ) -> Verdict:
        if self.backend == "stub":
            return _stub_verdict(role_evidence)
        if self.backend == "ollama":
            return _ollama_verdict(
                claim, role_evidence,
                base_url=self.ollama_base_url,
                model=self.ollama_model,
                max_evidence_per_role=self.max_evidence_per_role,
                use_structural_prior=self.use_structural_prior,
            )
        # Anthropic backend stub: requires user to add their key/handler
        raise NotImplementedError(f"backend {self.backend} not implemented")
