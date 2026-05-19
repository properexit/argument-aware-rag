"""Load LIARArg CSV, parse list-encoded columns, build train/val/test splits.

The LIARArg dataset stores most argument structure as stringified Python lists,
e.g.  premise   = "['p1', 'p2', ...]"
      attack_relation = "[premise_id_a, claim_id_b, premise_id_c, claim_id_b, ...]"

Relation lists are *flat* lists of (source_id, target_id) pairs. They are
re-shaped here into list[tuple[int,int]] for downstream use.
"""
from __future__ import annotations

import ast
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split


LIST_COLUMNS = [
    "claim", "premise", "citation", "leaking", "summary",
    "claim_id", "premise_id", "citation_id",
    "leaking_claim_id", "leaking_premise_id",
    "claim_position", "premise_position", "citation_position",
    "leaking_claim_position", "leaking_premise_position",
    "support_relation", "attack_relation",
    "psupport_relation", "pattack_relation",
]


def _safe_literal_eval(x: Any) -> Any:
    """ast.literal_eval but tolerant of NaN/empty/already-decoded values."""
    if x is None:
        return []
    if isinstance(x, (list, dict)):
        return x
    if not isinstance(x, str):
        # NaN floats end up here
        try:
            if pd.isna(x):
                return []
        except (TypeError, ValueError):
            pass
        return []
    s = x.strip()
    if not s:
        return []
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        # Fall back to splitting on commas inside brackets, else empty
        return []


def _pair_up(flat: list[int]) -> list[tuple[int, int]]:
    """Convert flat [s1, t1, s2, t2, ...] into [(s1,t1), (s2,t2), ...]."""
    if not flat:
        return []
    if len(flat) % 2 != 0:
        # Defensive: truncate trailing element
        flat = flat[: len(flat) - 1]
    return [(int(flat[i]), int(flat[i + 1])) for i in range(0, len(flat), 2)]


@dataclass
class LIARArgRow:
    """Parsed view of one LIARArg row."""

    id: int
    label: str
    statement: str                       # the raw claim text being fact-checked
    speaker: str
    claim_texts: list[str]               # gold claim spans inside the justification
    claim_ids: list[int]
    premise_texts: list[str]
    premise_ids: list[int]
    citation_texts: list[str]
    citation_ids: list[int]
    support_relations: list[tuple[int, int]]   # (premise_id, claim_id)
    attack_relations: list[tuple[int, int]]
    psupport_relations: list[tuple[int, int]]
    pattack_relations: list[tuple[int, int]]
    full_text: str                       # the fact-checker's justification
    summary: list[str]
    quality: str | float | None

    @property
    def n_support(self) -> int:
        return len(self.support_relations) + len(self.psupport_relations)

    @property
    def n_attack(self) -> int:
        return len(self.attack_relations) + len(self.pattack_relations)

    def to_dict(self) -> dict:
        return asdict(self)


def parse_row(raw: pd.Series) -> LIARArgRow:
    """Convert one raw CSV row into a typed LIARArgRow."""
    parsed = {col: _safe_literal_eval(raw.get(col)) for col in LIST_COLUMNS}

    return LIARArgRow(
        id=int(raw["id"]),
        label=str(raw["label"]),
        statement=str(raw.get("statement", "")),
        speaker=str(raw.get("speaker", "")),
        claim_texts=list(parsed["claim"] or []),
        claim_ids=[int(x) for x in (parsed["claim_id"] or [])],
        premise_texts=list(parsed["premise"] or []),
        premise_ids=[int(x) for x in (parsed["premise_id"] or [])],
        citation_texts=list(parsed["citation"] or []),
        citation_ids=[int(x) for x in (parsed["citation_id"] or [])],
        support_relations=_pair_up(parsed["support_relation"] or []),
        attack_relations=_pair_up(parsed["attack_relation"] or []),
        psupport_relations=_pair_up(parsed["psupport_relation"] or []),
        pattack_relations=_pair_up(parsed["pattack_relation"] or []),
        full_text=str(raw.get("fullText_based_content", "") or raw.get("whole_text", "")),
        summary=list(parsed["summary"] or []),
        quality=raw.get("quality"),
    )


def load_liararg(
    csv_path: str,
    filter_low_quality: bool = True,
) -> list[LIARArgRow]:
    """Load LIARArg and return a list of typed rows."""
    df = pd.read_csv(csv_path)
    if filter_low_quality:
        # In the CSV, well-formed rows have NaN quality; bad rows have a string.
        df = df[df["quality"].isna()].copy()
    rows = [parse_row(r) for _, r in df.iterrows()]
    return rows


def stratified_split(
    rows: list[LIARArgRow],
    test_frac: float = 0.15,
    val_frac: float = 0.10,
    random_state: int = 42,
) -> dict[str, list[LIARArgRow]]:
    """Stratified split on label."""
    labels = [r.label for r in rows]
    idx = list(range(len(rows)))

    train_val_idx, test_idx = train_test_split(
        idx,
        test_size=test_frac,
        stratify=labels,
        random_state=random_state,
    )
    # val fraction is relative to original size; scale to remaining set
    remaining_val_frac = val_frac / (1 - test_frac)
    train_val_labels = [labels[i] for i in train_val_idx]
    train_idx, val_idx = train_test_split(
        train_val_idx,
        test_size=remaining_val_frac,
        stratify=train_val_labels,
        random_state=random_state,
    )
    return {
        "train": [rows[i] for i in train_idx],
        "val": [rows[i] for i in val_idx],
        "test": [rows[i] for i in test_idx],
    }


def save_split(split: dict[str, list[LIARArgRow]], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for name, rs in split.items():
        path = os.path.join(out_dir, f"{name}.jsonl")
        with open(path, "w") as f:
            for r in rs:
                f.write(json.dumps(r.to_dict()) + "\n")


def load_split(out_dir: str) -> dict[str, list[LIARArgRow]]:
    split: dict[str, list[LIARArgRow]] = {}
    for name in ("train", "val", "test"):
        path = os.path.join(out_dir, f"{name}.jsonl")
        if not os.path.exists(path):
            continue
        split[name] = []
        with open(path) as f:
            for line in f:
                d = json.loads(line)
                # Re-tuple relations
                for k in ("support_relations", "attack_relations",
                          "psupport_relations", "pattack_relations"):
                    d[k] = [tuple(x) for x in d.get(k, [])]
                split[name].append(LIARArgRow(**d))
    return split
