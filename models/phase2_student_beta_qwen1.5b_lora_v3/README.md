---
license: apache-2.0
base_model: Qwen/Qwen2.5-1.5B-Instruct
library_name: peft
tags: [argument-mining, fact-checking, lora, qwen]
language: [en]
pipeline_tag: text-generation
---

# ArgParser-v3

v2's adapter continued for one more epoch after adding a fifth corpus:
AAEC (402 persuasive essays, ~6000 argument components). ~5.5 hours
on the same GTX 1080 Ti.

Held-out component-F1: **0.229**, a marginal improvement over v2's
0.219. Microtext and AbstRCT nudged up; PERSPECTRUM slightly regressed
(0.056 → 0.034). Adding more of the same kind of extractive academic
gold hits diminishing returns pretty quickly.

I also tried v3 on the actual LIARArg parse -- the whole point of the
project -- and hit an **83% empty rate** on the first 64 rows. Real
outputs were fragmentary ("is not clear" as a claim). Killed the run
after that; it was obvious this variant couldn't do cross-domain
transfer to Politifact-style claims. The five academic argument-mining
corpora aren't enough on their own to bridge that gap.

That result motivated [v4](https://huggingface.co/properexit/ArgParser-v4) -- adding silver labels from a large
teacher (`gpt-oss-120b`) on 2,123 LIARArg training articles, with
Chain-of-Thought reasoning traces preserved through training. v4 gets
Phase 1 integration F1 = 0.217, closes 33% of the gold-parser gap.

For actual use, go to v4. This one exists for the ablation record.

## Config

- Base: `Qwen/Qwen2.5-1.5B-Instruct`
- Method: LoRA r=16, continual from v2
- Data: 5 gold corpora (AAEC added), 1,823 records
- Epochs: 1 continual (~4 epochs of learning total including v2)
- Wall clock: 5.5 h

## Usage

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM
base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = PeftModel.from_pretrained(base, "properexit/ArgParser-v3")
```

## License

Apache 2.0.
