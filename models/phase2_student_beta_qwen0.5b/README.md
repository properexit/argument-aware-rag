---
license: apache-2.0
base_model: Qwen/Qwen2.5-0.5B-Instruct
library_name: transformers
tags: [argument-mining, fact-checking, qwen]
language: [en]
pipeline_tag: text-generation
---

# ArgParser-v1

Baseline for the ArgParser series. Full fine-tune of Qwen-0.5B on four
argument-mining corpora (AbstRCT, Microtext, CDCP, PERSPECTRUM), 1,494
records total, 3 epochs, fp16, Adafactor. About 1.5 hours on a
GTX 1080 Ti.

Held-out component-F1 averaged across the four domains: **0.108**.
Best on CDCP claim extraction (0.501). Worst on PERSPECTRUM (91%
empty rate -- the debate-text format defeats extractive parsing here).

This is the smallest useful reference point. Kept up mostly for
reproducibility of the ablation series. If you want to actually use
one of these, use [ArgParser-v4](https://huggingface.co/properexit/ArgParser-v4) -- same repo family, gets a
real Phase 1 integration F1 of 0.217 versus this baseline's near-zero
usefulness on that task.

## Config

- Base: `Qwen/Qwen2.5-0.5B-Instruct`
- Method: full fine-tune, 494M trainable params
- Data: 4 gold argument-mining corpora, 1,494 records
- Epochs: 3
- Wall clock: 1.5 h on GTX 1080 Ti

## License

Apache 2.0.
