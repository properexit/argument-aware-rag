---
license: apache-2.0
base_model: Qwen/Qwen2.5-1.5B-Instruct
library_name: peft
tags: [argument-mining, fact-checking, lora, qwen]
language: [en]
pipeline_tag: text-generation
---

# ArgParser-v2

Same training data as v1 (four argument-mining corpora, 1,494 records)
but a larger base and LoRA instead of full fine-tune. Qwen-1.5B with
LoRA r=16 (α=32, dropout 0.05, target `q_proj,k_proj,v_proj,o_proj`).
3 epochs, about 13.5 hours on a GTX 1080 Ti.

Held-out component-F1: **0.219** -- roughly double v1. Microtext premise
F1 went from 0.000 to 0.680. AbstRCT empty rate 75% → 50%. Scale plus
LoRA plus longer training context are the dominant levers, and this
was the run that made that obvious.

Not the best model in the series. For actual use pick
[ArgParser-v4](https://huggingface.co/properexit/ArgParser-v4) instead -- it adds cross-domain transfer to
LIARArg-style political claims, which is what most people probably
care about.

## Config

- Base: `Qwen/Qwen2.5-1.5B-Instruct`
- Method: LoRA r=16 (4.4M trainable params)
- Data: 4 gold corpora, 1,494 records
- Epochs: 3
- Wall clock: 13.5 h

## Usage

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM
base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = PeftModel.from_pretrained(base, "properexit/ArgParser-v2")
```

## License

Apache 2.0.
