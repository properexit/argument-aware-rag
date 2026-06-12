# Supervisor meeting — Phase 1 progress

**Time budget:** 10 minutes (~7 minutes of slides, 3 minutes for discussion).
**Goal:** confirm Phase 1 direction is right and surface three decision-shaped questions.

---

## Slide 1 — Title (10 s)

> **Argument-Aware Retrieval for Fact-Checking**
> Phase 1 progress · n=200 evaluation on LIARArg

Say: *"Quick update on Phase 1 plus three things I'd like your input on."*

---

## Slide 2 — Problem & question (60 s)

**Bullets on slide:**
- RAG-for-fact-checking retrieves by *topical* similarity.
- Wang et al. (2025a) showed argumentation helps verification — but their retrieval is still topical.
- Topical relevance ≠ argumentative relevance: a passage can mention the right subject without supporting or attacking the actual premises a fact-checker needs to verify.

**Research question:** *"Can using the argumentative structure of a claim guide evidence retrieval, and does that improve fact-checking accuracy and explainability over standard RAG?"*

Say: *"My anchor example is the AIDS-spending claim — gold structure has 7 attack relations from the fact-checker. Standard retrieval finds AIDS-funding paragraphs; role-targeted retrieval finds the specific paragraphs that address each attacking premise."*

---

## Slide 3 — Architecture (60 s) [show the architecture diagram]

Bullets on slide:
- Five stages. Two are novel (Stages 2 + 4).
- Stages 1, 3, 5 are shared infrastructure with standard RAG.
- Flat-RAG baseline = pipeline without Stages 2 + 4.

Say: *"Phase 1 uses the gold argument parser. Phase 2 replaces it with a learned cross-domain parser. Everything downstream is the same."*

---

## Slide 4 — Setup (40 s)

**On slide:**
- Dataset: LIARArg, 2,832 filtered claims, stratified split 2123 / 284 / 425.
- Retrieval corpus: ~50k paragraph passages from LIARArg justifications, same-row exclusion at query time.
- Retriever: BM25 + sentence-transformers (MiniLM), RRF fusion.
- Re-ranker: NLI cross-encoder (deberta-v3-small).
- Verifier: Qwen-2.5-14B-instruct via Ollama, local on M3.
- Metrics: macro-F1, within-1 accuracy, MAE, per-label P/R.

---

## Slide 5 — Headline results, n=200 (120 s) ★ key slide

| Metric                     | arg-aware  | flat-RAG  | gap         |
|----------------------------|------------|-----------|-------------|
| Accuracy                   | **33.5 %** | 20.0 %    | **+13.5 pt**|
| Macro-F1                   | **0.296**  | 0.128     | **+0.168**  |
| Within-1 accuracy          | **66.5 %** | 60.0 %    | +6.5 pt     |
| MAE on 6-point scale       | **1.23**   | 1.49      | −0.26       |
| **Extreme F1**             | **0.536**  | 0.195     | **+0.341**  |
| **Extreme within-1**       | **85.9 %** | 57.6 %    | **+28.3 pt**|
| Intermediate within-1      | 47.5 %     | 62.4 %    | −14.9 pt    |

Say: *"Headline is +13.5 points accuracy. But the more useful number is the extreme-label split: arg-aware gets 86 % within-1 on True / False / Pants-fire vs 58 % for flat-RAG. The retrieval is doing exactly what we hypothesised."*

**Significance note (have ready if asked):** with n=200, SE on accuracy ≈ 3.3 pts → 13.5-point gap is ~4 SE apart. Solid signal.

---

## Slide 6 — Where it wins, where it loses (90 s)

**Where it wins (60 / 200 cases unique to arg-aware):**
- Pants-fire (fabricated claims, invented quotes, impossible figures).
- True / Mostly-true (claims with clean support evidence — flat-RAG hedges).
- Mechanism: role-targeted retrieval + structural prior give the LLM confidence to commit to the right extreme.

**Where it loses (33 / 200 cases unique to flat-RAG):**
- Two failure modes:
  - False → Pants-fire overshoot (~21 cases): one-bucket over-commitment.
  - Half-true / Mostly-true → False/Pants-fire overshoot (~10 cases): multi-bucket overshoot when gold structure is attack-heavy but verdict is intermediate.
- Wisconsin "dead last in the Midwest for job creation" case (gold = Mostly-true, predicted = False) is the canonical example.

---

## Slide 7 — The methodological finding (75 s)

**On slide:**
- **Argument-component balance ≠ truthfulness balance.**
- In LIARArg, fact-checkers annotate any qualification or caveat as an *attack* on the claim's literal wording. But many attack-heavy claims still receive intermediate verdicts (Mostly-true, Half-true) because the central assertion is roughly correct.
- The structural prior reinforces this: one-sided attack structure → LLM predicts False or Pants-fire → over-shoots the gold intermediate label.
- This is a clean methodological observation that I think is publishable on its own.

Say: *"This is the part I'm most excited about — it's not just a numbers improvement, it's a finding about how argument structure relates to verdict polarity in this dataset."*

---

## Slide 8 — What's done, what's next (60 s)

**Done:**
- Five-stage pipeline implemented; reproducible on a single laptop.
- n=25 prompt iteration; n=200 evaluation with seeded determinism.
- Per-claim audit script comparing arg-aware vs flat-RAG.
- Code on GitHub: `github.com/properexit/argument-aware-rag`.

**This week:**
- Full test set n=425 evaluation (~4.5 h overnight run) → headline number.
- Variance estimate via second seed → robustness bound.
- Soft-prior ablation (apply prior only when |n_sup − n_atk| ≥ 3) → test whether the False-overshoot drops.

**Phase 2 (the bigger contribution):**
- Train ArgParserLLM on ARIES benchmark (teacher-student CoT distillation).
- Drop into Phase 1 pipeline; measure gold-vs-learned F1 gap.

---

## Slide 9 — Three decisions I'd like your input on (90 s) ★ ask slide

1. **Scope.** Submit Phase 1 to a workshop now (ArgMining @ ACL/EMNLP) or wait and combine with Phase 2 for a fuller submission?

2. **Open-corpus extension.** Should I run a Phase 1 experiment on a non-LIARArg corpus (Wikipedia / news passages) to show the method isn't dataset-specific? This adds ~2 weeks but strengthens the contribution.

3. **Methodological framing.** I've been thinking about reframing the central contribution as **premise-level verification** rather than claim-level — predicting a verdict for each premise and aggregating to a claim verdict via the argument graph. New task definition, new evaluation metric, native explainability. Worth pursuing or scope creep?

---

## Backup slides (have these ready, do not pre-show)

**B1 — Worked example.** AIDS-spending claim flowing through all 5 stages, with concrete intermediate outputs.

**B2 — Confusion matrices.** Side-by-side for arg-aware and flat-RAG. The Barely-true row is empty in both — paper-worthy finding.

**B3 — Prompt evolution.** Stub → Llama 8B (centrist bias) → Qwen 14B + new rubric (mostly fixed). One slide of the lessons.

**B4 — Phase 2 plan.** ArgParserLLM distillation pipeline + ARIES eval plan.

---

## Practical notes for delivery

- Lead each slide with the bottom-line one-liner before walking through bullets.
- For Slide 5, do **not** read the table — point at the 13.5 and the 86%, then move on.
- For Slide 7 (the methodological finding), this is where you sound most like a researcher. Pause, look up from the screen, deliver it.
- For Slide 9, write the three questions on a sticky note or notebook so you can refer to them during the discussion that follows.
- If you run short on time, drop Slide 6 first, then Slide 4. Never drop Slide 5 or Slide 9.

## Possible questions and prepared answers

- *"How big is the noise floor?"* → n=200, SE ~3 pts on accuracy. The 13.5 gap is ~4 SE. Second seed run is queued.
- *"What about prior work?"* → Wang et al. 2025a does claim-level RAG with argumentation. Ours adds role-targeted queries and role-aware re-ranking. Premise-level framing is a further differentiator.
- *"Why Qwen-14B and not GPT-4?"* → Reproducibility, cost, runs on a laptop. Numbers are LLM-agnostic in trend; GPT-4 would shift the level not the gradient.
- *"What's the failure mode you most worry about?"* → Argument-balance vs verdict-polarity decoupling (Slide 7). Soft-prior ablation tests one hypothesis.
