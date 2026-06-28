# Phase 2 — Experiments Registry

Single source of truth for all Phase 2 experiments. Append new rows as v4+
lands. Detailed per-domain breakdowns in `phase2_results.json`.

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

| Domain | v1 comp-F1 | v2 comp-F1 | v3 comp-F1 | v1 empty | v2 empty | v3 empty |
|---|---|---|---|---|---|---|
| Microtext | 0.116 | 0.393 | **0.414** | 0% | 0% | 0% |
| CDCP | 0.169 | 0.202 | **0.219** | 13% | 12% | 14% |
| AbstRCT | 0.108 | 0.223 | **0.249** | 75% | 50% | 50% |
| PERSPECTRUM | 0.038 | 0.056 | **0.034** | 91% | 88% | 92% |
| **Average** | **0.108** | **0.219** | **0.229** | — | — | — |

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
