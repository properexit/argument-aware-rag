"""Macro-F1 + accuracy metrics + within-1 graded accuracy, split by
extreme vs intermediate labels.

`within_1_accuracy` treats predictions that are off by at most one bucket
on the 6-point LIARArg scale as correct. This is the more forgiving and
arguably more honest metric for this dataset, since PolitiFact's gold
labels are themselves noisy at adjacent-bucket distinctions (e.g.
Mostly-true vs Half-true).
"""
from __future__ import annotations

from collections import defaultdict
from typing import Sequence

from sklearn.metrics import (
    classification_report,
    f1_score,
    accuracy_score,
    confusion_matrix,
)

LABELS = ["True", "Mostly-true", "Half-true", "Barely-true", "False", "Pants-fire"]
EXTREME = ["True", "False", "Pants-fire"]
INTERMEDIATE = ["Mostly-true", "Half-true", "Barely-true"]

# Position on the 6-point truthfulness scale (True=0 ... Pants-fire=5)
LABEL_INDEX = {lab: i for i, lab in enumerate(LABELS)}

# ---------------------------------------------------------------------------
# 3-way collapsed scheme (LIAR-literature standard).
# Used for direct comparison against prior work that collapses LIAR's
# 6-point scale into truth-leaning / mixed / false-leaning buckets.
# ---------------------------------------------------------------------------
THREEWAY_LABELS = ["true-leaning", "mixed", "false-leaning"]
LABEL_TO_3WAY = {
    "True":         "true-leaning",
    "Mostly-true":  "true-leaning",
    "Half-true":    "mixed",
    "Barely-true":  "mixed",
    "False":        "false-leaning",
    "Pants-fire":   "false-leaning",
}


def to_3way(label: str) -> str:
    """Collapse a 6-way label to its 3-way bucket. Pass-through if unknown."""
    return LABEL_TO_3WAY.get(label, label)


def _bucket_distance(a: str, b: str) -> int | None:
    """Distance between two labels on the 6-point scale, or None if either
    label is outside the canonical set."""
    if a not in LABEL_INDEX or b not in LABEL_INDEX:
        return None
    return abs(LABEL_INDEX[a] - LABEL_INDEX[b])


def _within_k_accuracy(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    k: int,
) -> float:
    if not y_true:
        return 0.0
    n_ok = 0
    for t, p in zip(y_true, y_pred):
        d = _bucket_distance(t, p)
        if d is not None and d <= k:
            n_ok += 1
    return n_ok / len(y_true)


def compute_metrics(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    labels: Sequence[str] = LABELS,
) -> dict:
    # Replace empty preds with a sentinel so sklearn doesn't choke
    y_pred = [p if p else "UNKNOWN" for p in y_pred]
    label_set = list(labels) + (["UNKNOWN"] if "UNKNOWN" in y_pred else [])

    macro_f1 = f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)
    within_1 = _within_k_accuracy(y_true, y_pred, k=1)

    # Extreme / intermediate splits (both strict F1 and within-1 accuracy)
    def _subset_indices(target):
        return [i for i, t in enumerate(y_true) if t in target]

    def _subset_f1(target):
        idx = _subset_indices(target)
        if not idx:
            return None
        ys = [y_true[i] for i in idx]
        ps = [y_pred[i] for i in idx]
        return f1_score(ys, ps, labels=target, average="macro", zero_division=0)

    def _subset_within_1(target):
        idx = _subset_indices(target)
        if not idx:
            return None
        ys = [y_true[i] for i in idx]
        ps = [y_pred[i] for i in idx]
        return _within_k_accuracy(ys, ps, k=1)

    extreme_f1 = _subset_f1(EXTREME)
    intermediate_f1 = _subset_f1(INTERMEDIATE)
    extreme_within_1 = _subset_within_1(EXTREME)
    intermediate_within_1 = _subset_within_1(INTERMEDIATE)

    report = classification_report(
        y_true, y_pred, labels=labels, zero_division=0, output_dict=True
    )
    cm = confusion_matrix(y_true, y_pred, labels=label_set).tolist()

    # Mean Absolute Error on the 6-point scale (lower is better, max=5)
    distances = [_bucket_distance(t, p) for t, p in zip(y_true, y_pred)]
    distances = [d for d in distances if d is not None]
    mae = (sum(distances) / len(distances)) if distances else None

    # ---- 3-way collapsed metrics (LIAR-standard comparison) ---------------
    y_true_3w = [to_3way(t) for t in y_true]
    y_pred_3w = [to_3way(p) for p in y_pred]
    acc_3way = accuracy_score(y_true_3w, y_pred_3w)
    macro_f1_3way = f1_score(
        y_true_3w, y_pred_3w,
        labels=THREEWAY_LABELS, average="macro", zero_division=0,
    )
    report_3w = classification_report(
        y_true_3w, y_pred_3w,
        labels=THREEWAY_LABELS, zero_division=0, output_dict=True,
    )
    cm_3way = confusion_matrix(
        y_true_3w, y_pred_3w, labels=THREEWAY_LABELS,
    ).tolist()

    return {
        "n": len(y_true),
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "within_1_accuracy": within_1,
        "mae_on_scale": mae,
        "extreme_macro_f1": extreme_f1,
        "intermediate_macro_f1": intermediate_f1,
        "extreme_within_1_accuracy": extreme_within_1,
        "intermediate_within_1_accuracy": intermediate_within_1,
        "per_label": {
            lab: {
                "precision": report[lab]["precision"],
                "recall": report[lab]["recall"],
                "f1": report[lab]["f1-score"],
                "support": report[lab]["support"],
            }
            for lab in labels if lab in report
        },
        "labels": label_set,
        "confusion_matrix": cm,
        # 3-way collapsed view
        "threeway": {
            "accuracy": acc_3way,
            "macro_f1": macro_f1_3way,
            "per_bucket": {
                lab: {
                    "precision": report_3w[lab]["precision"],
                    "recall": report_3w[lab]["recall"],
                    "f1": report_3w[lab]["f1-score"],
                    "support": report_3w[lab]["support"],
                }
                for lab in THREEWAY_LABELS if lab in report_3w
            },
            "labels": THREEWAY_LABELS,
            "confusion_matrix": cm_3way,
        },
    }
