"""LLM-only baselines for fair comparison with the main pipeline.

Each baseline runs on the same LIAR-aligned test set as the main method
and writes predictions in the same JSONL format, so the existing
`recompute_metrics.py` and `audit_disagreement.py` scripts can score
them without modification.
"""
