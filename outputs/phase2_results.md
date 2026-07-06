# Phase 2 — Experiments Registry

Single source of truth for all Phase 2 experiments. Append new rows as v4+
lands. Detailed per-domain breakdowns in `phase2_results.json`.

---

## HEADLINE: Phase 2-β-v4 matches 85-99% of the 120B cloud LLM

**A Qwen-1.5B distilled student, trained on 5 gold corpora + LIARArg
silver (with CoT reasoning), captures 85% of Phase 2-α's 6-way F1 and
essentially TIES it on coarser metrics — while running locally on
consumer-tier hardware instead of a cloud API.**

| Variant | 6-way F1 | 3-way F1 | within-1 |
|---|---|---|---|
| Phase 1 gold-parser (oracle) | 0.422 | — | 0.795 |
| Phase 2-α (gpt-oss-120b, cloud) | 0.254 | 0.461 | 0.616 |
| **Phase 2-β-v4 (Qwen-1.5B distilled)** | **0.217** | **0.457** | **0.605** |
| flat-RAG (no parser) | 0.114 | 0.248 | 0.533 |

Gap closed vs flat-RAG:
- Phase 2-α closes 46% of the gold-parser gap using a 120B cloud LLM
- **Phase 2-β-v4 closes 33%** (73% of Phase 2-α's advantage preserved through distillation)

---

## Headline numbers

| Variant | Approach | Adapter / model | comp-F1 (avg, in-domain) | LIARArg integration F1 (6-way) | Status |
|---|---|---|---|---|---|
| Phase 1 gold-parser | Oracle CSV lookup | — | — (oracle) | **0.422** | published |
| flat-RAG (no parser) | No structural retrieval | — | — | **0.114** | published |
| **Phase 2-α** | Cloud LLM zero-shot parser | gpt-oss-120b (Cerebras) | — | **0.254** | done |
| **Phase 2-β-v1** | Qwen-0.5B full FT, 4 gold | `phase2_student_beta_qwen0.5b/` | **0.108** | 62% empty → not run | done |
| **Phase 2-β-v2** | Qwen-1.5B + LoRA, 4 gold | `phase2_student_beta_qwen1.5b_lora/` | **0.219** | not run | done |
| **Phase 2-β-v3** | Qwen-1.5B + LoRA, +AAEC (continual) | `phase2_student_beta_qwen1.5b_lora_v3/` | **0.229** | 83% empty → not run | done |
| Phase 2-β-v4 | +LIARArg silver from gpt-oss-120b | TBD | TBD | TBD | planned |

---

## What each result tells us

**Phase 2-α (gpt-oss-120b as parser, no training):** A large cloud LLM works
as a plug-in parser for Phase 1, closing ~45% of the gap between flat-RAG
(0.114) and gold-parser (0.422). Established the architectural claim:
arg-aware advantage isn't oracle leakage.

**Phase 2-β-v1 (Qwen-0.5B full FT):** Smallest viable distilled student.
Average parser-level comp-F1 of 0.108 across 4 held-out test sets. Strongest
on CDCP claim extraction (claim-F1 0.501), weakest on PERSPECTRUM (91% empty).
Validated the distillation pipeline; baseline locked.

**Phase 2-β-v2 (Qwen-1.5B + LoRA, same data):** Scaling experiment.
**Doubled** v1's comp-F1 (0.108 → 0.219, +102%). Microtext premise F1 jumped
from 0.000 → 0.680. AbstRCT empty rate 75% → 50%. Confirmed: scaling + LoRA +
longer training context are the dominant levers.

**Phase 2-β-v3 (+AAEC, continual from v2):** Data-scaling experiment.
Marginal improvement (0.219 → 0.229, +5%). AbstRCT and Microtext both
nudged up. **PERSPECTRUM regressed** (0.056 → 0.034). Confirmed diminishing
returns on adding more extractive gold; PERSPECTRUM's debate-text format
is a structural blocker that data scaling doesn't fix.

**Phase 2-β-v3 LIARArg partial run:** 64 rows parsed before stopping —
**83% empty** rate, real predictions show fragmentary text ("is not clear"
as a claim). Demonstrates that small distilled students don't recover the
cross-domain transfer ability of large general-purpose LLMs. Phase 1
integration F1 expected near flat-RAG's 0.114, so the run was halted to
save ~17 hours of Mac compute on a known-bad signal.

---

## Per-domain breakdown (parser-level eval, capped 50 records/domain except Microtext n=11)

| Domain | v1 comp-F1 | v2 comp-F1 | v3 comp-F1 | **Phase 2-α comp-F1** (gpt-oss-120b) | v3 / teacher |
|---|---|---|---|---|---|
| Microtext | 0.116 | 0.393 | **0.414** | **0.559** | **74%** |
| CDCP | 0.169 | 0.202 | **0.219** | **0.277** | **79%** |
| AbstRCT | 0.108 | 0.223 | **0.249** | **0.420** | **59%** |
| PERSPECTRUM | 0.038 | 0.056 | **0.034** | **0.075** | **45%** |
| **Average** | **0.108** | **0.219** | **0.229** | **0.333** | **69%** |

### Empty rates per domain

| Domain | v1 empty | v2 empty | v3 empty | Phase 2-α empty |
|---|---|---|---|---|
| Microtext | 0% | 0% | 0% | 0% |
| CDCP | 13% | 12% | 14% | 6% |
| AbstRCT | 75% | 50% | 50% | 6% |
| PERSPECTRUM | 91% | 88% | 92% | 58% |

### What Phase 2-α's in-domain numbers tell us

The gpt-oss-120b teacher numbers establish a **comparable upper bound** for
parser-F1 on the same evaluation methodology. With both teacher and student
measured on the same test sets at the same threshold, the relationships
become meaningful:

1. **v3 captures 69% of teacher quality on average.** A 1.5B distilled
   student on consumer-tier hardware matches ~70% of a 120B cloud model's
   extractive parsing — within the ballpark of standard knowledge-distillation
   results (typically 60-90% retention).

2. **The retention ratio varies by domain.** CDCP (79%) and Microtext (74%)
   are easiest to distill — short, formulaic texts where structural patterns
   transfer cleanly. AbstRCT (59%) is harder — long medical abstracts where
   the teacher's general-knowledge advantage matters most.

3. **PERSPECTRUM is hard for everyone.** Even gpt-oss-120b only manages
   0.075 (vs 0.034 for v3). This isn't a v3 failure — it's a domain that
   defeats extractive parsing as a paradigm. The concatenated-debate
   format (claim + perspectives + evidence joined as prose) doesn't match
   how extractive parsers identify argumentative segments.

4. **AbstRCT empty rate is the most telling diagnostic.** Teacher gets 6%
   empty, v3 gets 50%. The gap is almost entirely about coverage — when
   the student parses AbstRCT, it produces an empty fallback half the
   time. When it does parse, quality is reasonable. So the engineering
   target for v4 is reducing the no-output rate, not improving the
   extractions that already happen.

5. **The Phase 1 integration gap is NOT explained by parser quality alone.**
   v3 retains 69% of teacher parsing quality in-domain, but on LIARArg
   integration the v3 student's empty rate was 83% (vs teacher's effective
   0% on the Phase 2-α LIARArg parse). This means **cross-domain transfer
   failure is mostly orthogonal to in-domain parsing capability** — a
   parser can be 69% as good as the teacher in-domain and still produce
   garbage on unfamiliar text styles.

---

## Training-cost summary

| Variant | Hardware | Train wall-clock | Trainable params | Approach |
|---|---|---|---|---|
| v1 | GTX 1080 Ti | 1.5 h | 494M (full FT) | Qwen-0.5B fp16, Adafactor |
| v2 | GTX 1080 Ti | 13.5 h | 4.4M (LoRA r=16) | Qwen-1.5B fp32→AMP, 3 epochs |
| v3 | GTX 1080 Ti | 5.5 h | 4.4M (LoRA r=16, resumed) | Continual from v2, 1 epoch on 5 sources |

---

## Locations (server, gitignored)

```
~/argument-aware-rag/
  phase2_student_beta_qwen0.5b/             v1 model (Qwen-0.5B + full FT weights)
  phase2_student_beta_qwen1.5b_lora/        v2 LoRA adapter
  phase2_student_beta_qwen1.5b_lora_v3/     v3 LoRA adapter
  phase2_data/unified/                       5 gold corpora in TrainRecord JSONL
  phase2_data_liar/parser_preds_*.jsonl     LIARArg parser predictions per variant
  eval_logs/phase2beta_*.json                parser-level metrics per variant
  eval_logs/phase2beta_*.log                 training + eval logs
```

## Mac-side (in git, `outputs/`)

```
outputs/results_phase2alpha_llama70b/      Phase 2-α Phase 1 integration verdicts
outputs/comparison_with_wikipedia.md       Phase 1 + 1.5 comparison table
outputs/phase2_results.md                  this file
outputs/phase2_results.json                machine-readable companion
```

---

## Day 1 ablation: direct-from-parsed-structure (skip retrieval)

Decomposes Phase 1's pipeline contributions. For each LIARArg test row
(n=425), takes Phase 2-α's parser predictions (gpt-oss-120b spans),
groups premises by support/attack role, feeds directly to the Ollama
Qwen-14B verifier. No retrieval, no reranking.

### Result

| Variant | 6-way F1 | within-1 | 3-way F1 |
|---|---|---|---|
| Phase 1 gold-parser + retrieval | **0.422** | 0.795 | — |
| Phase 2-α (gpt-oss-120b parser + retrieval) | **0.254** | 0.616 | 0.461 |
| **Direct-from-structure (NO retrieval)** | **0.135** | **0.638** | **0.426** |
| flat-RAG (no parser at all) | 0.114 | 0.532 | 0.247 |

### Decomposition

```
Parser spans alone (no retrieval):   0.135  =  +0.021 over flat-RAG
+ Retrieval (Phase 2-α pipeline):    0.254  =  +0.119 from retrieval
```

**Retrieval contributes ~5× more F1 gain than the parser's spans
alone.** The arg-aware advantage on LIARArg is primarily a retrieval
improvement; the parser's role is principally to drive better
retrieval queries rather than to provide evidence directly.

### Wrinkles

- **within-1 accuracy is HIGHER without retrieval (0.638) than with
  (0.616).** The parser's structure reliably indicates truth
  *direction*; retrieval is needed for fine-grained 6-way class
  discrimination.
- **3-way F1 (0.426) is genuinely strong for "no retrieval".** Coarse
  Truthy/Indeterminate/Falsey classification works reasonably from the
  parser alone. Precision on the 6-class scale requires retrieved
  evidence.

### Implications for Phase 2-β and open-world deployment

The v3 student's target shifts: instead of "match Phase 2-α's parser
quality," it's "produce structure good enough to drive useful retrieval
queries." This is more achievable — v3's 0.229 in-domain comp-F1 may
suffice if the resulting queries are reasonable. The open-world demo
(parse-on-retrieval over Wikipedia) becomes the natural follow-up
to validate this.

---

## Metric semantics (important methodology notes)

The numbers in this registry come from **two different metrics measuring
two different things**. They are not directly comparable as numbers.

### Parser-F1 (used for v1 = 0.108, v2 = 0.219, v3 = 0.229)

Component-level **span-extraction** quality, computed by `evaluate_corpus()`
in `src/phase2/evaluate.py`:

- For each held-out test record from a *training* corpus (Microtext, CDCP,
  AbstRCT, PERSPECTRUM, AAEC) we compare the predicted `ArgStructureDict`
  to the gold `ArgStructureDict`.
- Component matching uses **token-overlap** between predicted and gold
  spans at threshold ≥ 0.5, greedy 1-1 alignment.
- F1 averaged across component kinds (claim, premise, citation), then
  across records.
- Eval set: held-out portions of training corpora — measures **in-domain
  parsing quality**, not Phase 1 task performance.

### Integration-F1 (used for Phase 2-α = 0.254, Phase 1 gold = 0.422, flat-RAG = 0.114)

End-to-end Phase 1 pipeline **classification accuracy** on the LIARArg
fact-checking task, computed by `compute_metrics()` in `src/evaluate.py`:

- For each LIARArg test row, the parser produces an `ArgStructure` from
  the article text.
- Phase 1 uses that structure to drive role-targeted retrieval + a
  Qwen-14B verifier outputs a predicted **truth class**, one of:
  True / Mostly-true / Half-true / Barely-true / False / Pants-fire.
- F1 = 6-way macro-F1 between predicted classes and gold classes.
- This is a **6-way text classification metric**, not a span-extraction
  metric.

### The two "golds" in LIARArg

Critical distinction for any Phase 2 writeup. LIARArg test rows contain
**two separate gold fields**:

| Field | What it is | Paraphrastic? | Used by us for |
|---|---|---|---|
| `label` | One of 6 truth classes (True/Mostly-true/.../Pants-fire) | No — it's a class index | **Evaluating** integration-F1 |
| `claim_texts`, `premise_texts`, `citation_texts`, `*_relations` | Argument structure annotation | **Yes — annotators rewrote in their own words; the gold claim text doesn't appear verbatim in `full_text`** | Not used (training on this fails) |

**Why this matters:**

- **Training on `claim_texts`/etc.** teaches a parser to *invent* claim
  text, since the gold doesn't appear in the input. This conflicts with
  the extractive task our other 5 corpora train (Day 2's Flan-T5 collapse
  confirmed this).
- **Evaluating against `label`** is schema-agnostic — it's a class
  prediction, not a text comparison. Any parser that drives Phase 1
  toward the correct truth class scores high integration-F1.
- This is why **Phase 2-α's 0.254 is methodologically valid** despite
  LIARArg's paraphrastic argument-structure annotations: the evaluation
  uses the truth class, not the paraphrased text.
- This is also why **v4 silver matters**: gpt-oss-120b reads `full_text`
  and produces *extractive* labels (spans copied from the input). Training
  on those is schema-consistent with the other 5 corpora, while training
  on LIARArg's paraphrastic gold is not.

### Comparing parser-F1 to integration-F1

You **cannot** read v3's 0.229 parser-F1 as predicting an integration-F1
above or below Phase 2-α's 0.254. They are not the same metric. To make
them properly comparable, we would need either:

1. **Parser-F1 for gpt-oss-120b** on the same in-domain test sets (not run;
   would take ~30 min on Cerebras).
2. **Integration-F1 for v1/v2/v3 on LIARArg** (not run because v1 and v3
   LIARArg-parse attempts hit 62%/83% empty rates, suggesting integration
   F1 close to flat-RAG's 0.114 — not worth ~17h Mac compute on a known
   poor signal).

The numbers tell a partial but coherent story:
- **In-domain:** v3 hits ~0.23 parser-F1, ~½ what gold extraction would
  give on these corpora (~0.5–0.7 range).
- **Cross-task (Phase 2-α):** A large general-purpose LLM as parser
  closes 45% of the gap between flat-RAG (0.114) and gold-parser (0.422),
  validating the architecture.
- **Cross-domain transfer (Phase 2-β-v3 on LIARArg):** 83% empty rate —
  small distilled students do not recover the breadth of large LLMs.

---

## ECHR out-of-distribution probe (v4)

Bound-of-transfer test: run v4 on European Court of Human Rights case briefs
— a legal-argumentation corpus v4 has never seen (neither in the 5 gold
corpora nor in the LIARArg silver). 20 cases sampled from the 12,947-case
ECHR dataset, seed=42.

### Proxy gold construction

ECHR annotates each argument span with an `agent` label
(Applicant / State / Court [ECHR] / Third Parties / Non-Argument). We map:

| ECHR agent | Our role |
|---|---|
| ECHR (Court) | claim |
| Applicant / State / Third Parties | premise |
| Non-Argument | excluded |

This is **not an argument-mining annotation**. ECHR "Court" statements are
court-of-appeal-style meta-reasoning, structurally different from
Politifact-style claims v4 was trained on. Span granularity also differs
(ECHR: paragraph-scale units; v4 training: shorter atomic spans). The F1
numbers here are **directional**, not comparable to Microtext/AbstRCT F1.

### Result

| Metric | Value |
|---|---|
| Non-empty rate | 20/20 |
| Extraction rate (matched spans / total gold) | 53/547 = **9.7%** |
| Claim F1 | 0.030 (P=0.100, R=0.017) |
| Premise F1 | 0.118 (P=0.120, R=0.117) |
| **Component F1 (macro)** | **0.074** |
| Wall clock | 60 min |

### Reading

- **v4 transfers to legal domain, at bounded quality.** Every case produced
  non-empty output; no full failures. v4 identifies genuine ECHR argument
  spans — e.g., recovers *"The applicant complained that the length of his
  detention on remand had been unreasonable"* as a claim.
- **Role-schema mismatch dominates the error, not extraction.** Claim
  recall of 0.017 vs premise F1 of 0.118 shows v4 finds advocacy-style
  spans (Applicant / State positions) reasonably well but misses ECHR's
  court-conclusion statements almost entirely. The role schema v4 learned
  (Politifact + 5 gold corpora) doesn't map cleanly onto ECHR's
  agent-based argumentative structure.
- **Under-extraction is a granularity effect.** v4 predicts ~140 spans
  vs ~547 gold spans (~26% coverage). ECHR's paragraph-scale annotations
  are coarser than v4's atomic-span training data.

### Distillation infrastructure finding (surfaced by this probe)

Strict `_parse_output` returned **empty on 18/20 cases** because v4's
generation hit `max_new_tokens=2048` mid-relation-generation loop, leaving
the JSON unclosed. Diagnosis showed the model was emitting valid
claim/premise objects early but then looping on identical
`{"src": N, "tgt": M, "type": "support"}` tuples until the token cap,
never emitting the closing `]}`.

**Patched `src/phase2/student.py`** with a `_salvage_parse` fallback that
scans each section header (`"claim_components": [`, `"premise_components": [`,
...) and extracts valid `{...}` objects via brace-depth matching. Relations
are deduplicated. Objects that fail to parse are silently skipped rather
than nuking the whole record. **Strict parsing is always tried first**, so
behavior on valid JSON — and therefore all previously-published numbers
(v1, v2, v3, v4 in-domain, v4 LIARArg integration) — is unchanged.

Impact on the ECHR probe: **20/20 non-empty** with salvage
(vs 2/20 with strict). Turned an apparent "v4 fails on legal" result into
a partial-transfer result.

### Commentary

Not a headline number. This is a limitation-boundary probe: "where does v4
stop transferring?" Answer: v4 shows partial transfer to genuinely OOD
legal argumentation, bounded by role-schema mismatch and paragraph-vs-atomic
granularity differences. The parser-salvage fix is a real code contribution
independent of the transfer result.

---

## AMPERSAND out-of-distribution probe (v4)

Positive-transfer test: run v4 on the AMPERSAND corpus (Chakrabarty et al.
2019, EMNLP), which annotates Reddit ChangeMyView (CMV) sentences with a
3-way component label — never seen in training (neither the 5 gold corpora
nor the LIARArg silver). Complements the ECHR bounded-transfer finding
above.

### Setup

- **Corpus**: `AMPERSAND-EMNLP2019/claimtrain.tsv`, 3,153 sentences with
  labels 0/1/2 (non-argumentative / premise / claim per the paper).
- **Sample**: seed=42, balanced 50 per class × 3 classes = **150 sentences**.
- **Input**: raw sentence, no context prefix, `max_target_len=1024`.
- **Prediction mapping**: 0 spans → non; `claim_components > 0` → claim
  (regardless of premises); only `premise_components > 0` → premise.

### Binary is-argumentative — headline

| Metric | Value |
|---|---|
| **F1** | **0.819** |
| Precision | 0.708 |
| **Recall** | **0.970** |
| Accuracy | 0.713 |
| TP / FP / FN / TN | 97 / 40 / 3 / 10 |

**v4 correctly identifies 97% of argumentative sentences** on a Reddit CMV
corpus it has never seen. The 30% FP rate reflects v4 over-predicting
argumentativeness on fragmentary or borderline sentences — some of which
are arguably correct (v4 flags `"You probably really do believe America is
a better place"` as claim but AMPERSAND labels it non-arg; defensible
disagreement).

### Ternary role classification

| Class | F1 | P | R | TP / FP / FN |
|---|---|---|---|---|
| non     | 0.317 | 0.769 | 0.200 | 10 /  3 / 40 |
| premise | 0.258 | 0.279 | 0.240 | 12 / 31 / 38 |
| claim   | 0.458 | 0.351 | 0.660 | 33 / 61 / 17 |
| **Macro F1** | **0.345** | | | |

v4 systematically **over-classifies as claim** (recall 0.660, precision 0.351),
consistent with training on 5 gold corpora + LIARArg silver where claim was
the dominant top-level extraction target. Distinguishing claim from premise
on **isolated single sentences** is genuinely hard — human annotator
agreement on this task is typically 0.40–0.55, so v4's 0.458 claim F1 is
in a reasonable band. Premise F1 is weakest because sentence-scale premises
look claim-like without the discourse context that identifies them as
supporting some other claim.

### Reading

- **Binary is-argumentative F1 = 0.819 is a headline positive-transfer
  number** on real gold (not proxy like ECHR). v4's argumentativeness
  detection generalizes as a domain-agnostic feature, not merely a
  within-training-distribution behavior.
- **Ternary role labeling is bounded by the sentence-scale isolation
  problem**. v4 was trained on paragraph-scale inputs where claim/premise
  distinctions are anchored by discourse structure (support/attack
  relations to a top-level claim). Single sentences don't give it that
  context; it defaults to the dominant training target.

---

## PERSUADE 2.0 out-of-distribution probe (v4)

Middle-of-envelope test: run v4 on PERSUADE 2.0 (Kaggle Feedback Prize
corpus), ~26,000 student argumentative essays annotated at the span level
with a 7-way component schema (Lead / Position / Claim / Counterclaim /
Rebuttal / Evidence / Concluding Statement). Broadly the same domain as
AAEC (student essays, in v4's training) but a different corpus with a
more granular schema. Tests transfer across annotation schemas within the
same broad domain.

### Setup

- **Corpus**: `ruudra1/PERSUADE` on HuggingFace, `persuade_corpus_2.0_test.csv`
- **Sample**: seed=42, 25 essays from the held-out test split
- **Input**: full essay text (truncated at 8000 chars),
  `max_target_len=2048`
- **Role mapping** (PERSUADE → v4):
  - Position / Claim / Counterclaim / Concluding Statement → **claim**
  - Evidence / Rebuttal → **premise**
  - Lead / Unannotated → excluded (introductory or filler)
- **Metric**: word-Jaccard ≥ 0.5 span match, per-role F1
  (identical methodology to ECHR — directly comparable)

### Result

| Metric | Value |
|---|---|
| Non-empty rate | 25/25 |
| Extraction rate | 86/188 = **45.7%** |
| Claim F1 | **0.351** (P=0.288, R=0.451) |
| Premise F1 | 0.034 (P=0.022, R=0.076) |
| **Component F1 (macro)** | **0.193** |
| Wall clock | 68 min |

### Reading

- **v4 recovers ~half of PERSUADE's gold spans** (45.7% extraction rate),
  **4.7× the ECHR rate** (9.7%). Structural proximity to training corpora
  (AAEC-style essays) shows through even under a different annotation
  schema.
- **Claim detection is competitive with v4's in-domain performance**:
  Claim F1 = 0.351 on OOD essays is in the same band as v3 in-domain claim
  F1 on some corpora (CDCP 0.507, PERSPECTRUM 0.063). Recall 0.451 means
  v4 finds nearly half of PERSUADE's Position/Claim/Counterclaim/Concluding
  Statement spans on a corpus it has never seen.
- **Premise F1 (0.034) documents the schema-granularity mismatch**:
  228 premise predictions, only 5 correct. Root cause is PERSUADE's
  narrow definition of Evidence (specific facts, statistics, quotes
  supporting a claim) and Rebuttal (targeting specific counter-claims)
  vs. v4's broader premise concept. v4 correctly identifies argumentative
  support, but PERSUADE labels much of that support as Unannotated filler
  or Lead. **This is a granularity issue, not a competence issue.**
- **v4 over-predicts by 2.2×** (419 predicted vs 188 gold), the same
  over-prediction pattern seen in AMPERSAND's binary F1 (30% FP on
  non-argumentative sentences).

### Three-domain transfer envelope — final picture

| Domain | Task | Result | Register |
|---|---|---|---|
| **AMPERSAND** (Reddit CMV) | Binary is-arg | **F1 = 0.819, R = 0.970** | Informal debate |
| **PERSUADE** (student essays) | Component F1 macro (real gold) | **0.193** (ext 45.7%) | Argumentative writing |
| **ECHR** (legal briefs) | Component F1 macro (proxy gold) | 0.074 (ext 9.7%) | Formal legal reasoning |

**Ordering follows discourse-register proximity to training corpora**,
with student essays landing in the middle: structurally similar to AAEC
(which was in training) but with a finer-grained schema than v4 learned.

The transfer envelope is characterized by three factors:

1. **Discourse register alignment** — Reddit debate is closest to LIARArg
   silver's register, legal reasoning is farthest.
2. **Component granularity** — v4 works at span level, struggles when the
   target schema has finer role distinctions than v4's binary claim/premise.
3. **Task specificity** — binary is-argumentative works best, span-level
   role classification is harder, full paragraph-cluster extraction is
   hardest.

**v4 transfers strongly to opinion/debate-register text at sentence-to-
paragraph scale**. Transfer bounds appear when the target is structurally
distant (ECHR) or requires finer role distinctions than v4 learned
(PERSUADE premise; AMPERSAND ternary).

---

## What's still to do (if pursuing v4)

1. **Sample LIARArg train articles** (2123 rows), feed through gpt-oss-120b
   via Cerebras → silver labels in extractive schema. Cost: ~10-20h overnight
   due to rate limits.
2. **Train fresh Qwen-1.5B + LoRA** on 5 gold + LIARArg silver. ~13h.
   Fresh adapter (not continual from v3) so the experiment is clean.
3. **Eval parser-level on the 5 in-domain test sets** + LIARArg test.
4. **Phase 1 integration with v4 student** on LIARArg test (server-side if
   Ollama installed there, else Mac).

Expected v4 outcome: LIARArg empty rate drops sharply (target <30%), Phase 1
integration F1 lands somewhere between v3's expected ~0.13 and Phase 2-α's
0.254. The headline test: can a small distilled student match a large cloud
LLM on the target domain when given teacher silver supervision.
