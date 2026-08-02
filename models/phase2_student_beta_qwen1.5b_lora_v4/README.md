---
license: apache-2.0
base_model: Qwen/Qwen2.5-1.5B-Instruct
library_name: peft
tags:
  - argument-mining
  - fact-checking
  - lora
  - qwen
  - distillation
language: [en]
pipeline_tag: text-generation
---

# ArgParser-v4

A Qwen-1.5B LoRA that extracts argument structure -- claims, premises,
citations, and support/attack relations -- from political claims and
argumentative prose. This is the fourth iteration of a distillation
project, and the one that actually works well enough to plug into a
real fact-checking pipeline.

## Where this came from

I built an argument-aware retrieval pipeline for Politifact-style
fact-checking. Given a claim like "Politician X said Y," it retrieves
evidence using argument-role-targeted queries and returns a 6-way truth
verdict. When the parser was reading gold argument annotations from the
LIARArg dataset, this pipeline hit 0.422 6-way F1 versus 0.114 for a
flat-RAG baseline. The 0.308 gap was the whole reason to build it.

But that gap only means something if a real parser can slot in at
inference time. Gold annotations aren't available for actual incoming
claims. So the question became: what parser closes that gap?

First cut, Phase 2-α, was `gpt-oss-120b` running zero-shot on Cerebras.
It closed about 45% of the gap (integration F1 0.254). Real, useful,
but calling a 120B cloud model per claim isn't practical for anything
resembling deployment.

Phase 2-β was the distillation project. Four iterations. Can a small
local model preserve most of the gain?

## The four iterations

**v1** was Qwen-0.5B, full fine-tune on four argument-mining corpora
(AbstRCT, Microtext, CDCP, PERSPECTRUM), 1,494 records, 3 epochs. The
smallest reasonable baseline. In-domain comp-F1 averaged 0.108 across
the four held-out test sets. High empty rates on some domains
(PERSPECTRUM: 91% empty). The point was to get the pipeline plumbing
right, not to publish a number.

**v2** kept the same data but moved to Qwen-1.5B with LoRA r=16
(α=32, dropout 0.05, target `q_proj,k_proj,v_proj,o_proj`). 3 epochs.
In-domain comp-F1: 0.219, roughly double v1. Microtext premise F1
jumped from 0.000 to 0.680. AbstRCT empty rate 75% → 50%. Scale +
LoRA + longer training context are the dominant levers here.

**v3** was v2's adapter continued for one more epoch after adding a
fifth corpus (AAEC, 402 persuasive essays). Marginal in-domain
improvement (0.229). PERSPECTRUM actually regressed slightly, which
was the first sign that adding more of the same kind of extractive
gold hits diminishing returns quickly. Then I tried v3 on the actual
LIARArg parse and hit 83% empty rate on the first 64 rows. Killed
that run. The lesson was clear: extractive gold from academic
argument-mining corpora doesn't teach a small student to handle
Politifact-style claims. The distribution gap is too wide.

**v4** is this model. Two changes from v3:

1. Fresh adapter, not continual. Clean A/B against v3.
2. I generated 2,123 silver labels on LIARArg train articles using
   `gpt-oss-120b` via Cerebras. Both the extracted argument structure
   and the model's Chain-of-Thought reasoning came back (the CoT was
   in `message.reasoning`, which I captured almost by accident). The
   training code's target-formatter passes reasoning through as
   `<think>...</think>{json}` when present, so v4 accidentally
   became CoT-aware for LIARArg-style inputs -- while staying purely
   extractive on the gold in-domain corpora (where reasoning was empty).

This wasn't planned. It just happened, and it turned out to be exactly
what was missing.

Training details: 3,617 records total, 3 epochs, fresh LoRA adapter,
fp16, Adafactor, gradient checkpointing. Batch 1, grad accum 32.
About 29 hours on a single GTX 1080 Ti.

## What v4 actually does

The load-bearing number is Phase 1 integration on LIARArg -- the whole
reason to build any of this:

| Metric | v4 | Phase 2-α teacher (120B) | Teacher retention |
|---|---|---|---|
| 6-way F1 | 0.217 | 0.254 | 85% |
| 3-way F1 | 0.457 | 0.461 | 99% |
| within-1 accuracy | 0.605 | 0.616 | 98% |

Flat-RAG baseline for reference: 0.114. v4 beats it by 0.103 and
closes 33% of the gold-parser gap using a locally-runnable 1.5B model.

LIARArg parse empty rate went from v3's 83% down to 23%. Silver + CoT
was the missing piece.

In-domain retention is modest -- 0.192 comp-F1 averaged across the five
training corpora, slightly regressed from v3's 0.229. That's the cost
of a fresh 3-epoch run versus v3's effective 4 epochs. The trade was
worth it for the cross-domain transfer.

## OOD probes

To characterize where v4 stops transferring, I ran three unseen-domain
probes:

**AMPERSAND** (Chakrabarty et al. 2019, Reddit ChangeMyView). Binary
is-argumentative F1 = 0.819 with recall 0.970 on 150 balanced
sentences. v4 catches essentially all argumentative content in Reddit
debate. The 30% false-positive rate comes from over-flagging fragments
and borderline sentences; some of those are arguably right and just
disagree with the annotator.

**PERSUADE 2.0** (Kaggle Feedback Prize, student argumentative essays).
Component F1 macro = 0.193 with 45.7% extraction rate on 25 essays.
Claim F1 = 0.351, premise F1 = 0.034. v4 finds about half of
PERSUADE's argumentative spans and labels claim-like content
reasonably. Premise F1 collapses because PERSUADE's Evidence and
Rebuttal categories are much narrower than v4's premise concept.

**ECHR** (European Court of Human Rights case briefs). Component F1
= 0.074 with 9.7% extraction rate against a proxy gold derived from
ECHR's agent labels. Legal reasoning is structurally distant from
anything v4 saw in training.

Ordering (Reddit > essays > legal) tracks discourse-register proximity
to v4's training data. Predictable, but useful to have quantified.

## Usage

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch, re, json

base_id    = "Qwen/Qwen2.5-1.5B-Instruct"
adapter_id = "properexit/ArgParser-v4"

tok = AutoTokenizer.from_pretrained(base_id)
base = AutoModelForCausalLM.from_pretrained(
    base_id, torch_dtype=torch.float16, device_map="auto"
)
model = PeftModel.from_pretrained(base, adapter_id)

INSTR = ("Extract all argument components and relations from the text. "
         "Output strict JSON with claim_components, premise_components, "
         "citation_components, and relations.")

def parse(text, max_new_tokens=1024):
    prompt = tok.apply_chat_template(
        [{"role": "user", "content": f"{INSTR}\n\nTEXT:\n{text}"}],
        tokenize=False, add_generation_prompt=True,
    )
    enc = tok(prompt, return_tensors="pt", truncation=True,
              max_length=2048).to(model.device)
    out = model.generate(**enc, max_new_tokens=max_new_tokens,
                         do_sample=False,
                         pad_token_id=tok.pad_token_id,
                         eos_token_id=tok.eos_token_id)
    raw = tok.decode(out[0, enc["input_ids"].shape[-1]:],
                     skip_special_tokens=True)
    cleaned = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)
    m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    return (json.loads(m.group()) if m else None), raw

pred, raw = parse(
    "The Obama administration is putting Border Patrol agents in a chokehold."
)
print(pred)
```

## Things worth knowing before using this

The model emits `<think>...</think>` blocks on political and
opinionated inputs (that's where it saw CoT during training). On
formal or structured text -- legal writing, some scientific abstracts
 -- it goes straight to JSON. Neither is a bug, it just needs handling
if you're stripping the raw generation.

Long inputs can trigger a relation-generation loop that leaves the JSON
unclosed. What happens: the model emits valid `claim_components` and
`premise_components` early, then gets stuck emitting
`{"src": N, "tgt": M, "type": "support"}` tuples in a repeating
pattern until it hits `max_new_tokens`. You never see the closing `}`
so strict JSON parsing rejects everything. The workaround is either
setting `max_new_tokens` conservatively, or using a lenient parser
that pulls each valid `{...}` object out of each section
independently and dedupes relations. I use the second approach in
the training repo.

v4 systematically over-predicts spans on OOD text -- precision runs
lower than recall in every probe. On borderline sentences it defaults
to labeling as claim. Something to keep in mind if downstream
consumers care about precision.

Fine-grained annotation schemas map imperfectly to v4's binary
claim/premise split. PERSUADE's Evidence/Rebuttal distinction and
ECHR's Court/Applicant/State agent labels don't translate directly.
v4 knows a claim from a premise; it doesn't know PERSUADE's Evidence
from PERSUADE's Rebuttal.

## Training summary

- Base: `Qwen/Qwen2.5-1.5B-Instruct`
- LoRA: r=16, α=32, dropout 0.05, on `q_proj,k_proj,v_proj,o_proj`
- Training records: 3,617 (5 gold corpora + 2,123 LIARArg silver)
- Epochs: 3, fresh adapter
- Optimizer: Adafactor, fp16, gradient checkpointing
- Hardware: single NVIDIA GTX 1080 Ti
- Wall clock: ~29 h

## License

Apache 2.0. Base model (Qwen 2.5) is also Apache 2.0. Use however you
want, no warranty.
