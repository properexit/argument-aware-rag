# phase2_student_liar

Early full fine-tune experiment. Not part of the four v1--v4 variants that
we published on HuggingFace as `ArgParser-vN`.

This was a first attempt at training a student directly on LIAR-style
inputs (see `train.log`, `eval.log`, `phase2_metrics.json`) before we
converged on the extractive gold + silver + CoT recipe that produced v4.
Weights are not preserved in the repo. Metadata is kept for the record.

If you are looking for the recommended distilled parser, use
[ArgParser-v4](https://huggingface.co/properexit/ArgParser-v4).
