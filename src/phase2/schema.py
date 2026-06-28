"""Type definitions for Phase 2.

Two key schemas:

  - `TrainRecord` is the canonical row of the training corpus. Same shape
    for gold (from AAEC/AbstRCT/LIARArg) and silver (LLM-annotated from
    other ARIES datasets). Stored as JSONL on disk; `output` is the
    serialised `ArgStructure`.

  - `ArgStructureDict` is the JSON-serialisable form of Phase 1's
    `ArgStructure`. This is what teacher LLMs emit and what students
    learn to predict. Conversion to/from Phase 1's typed `ArgStructure`
    lives in arg_parser_llm.py.

Configs are dataclasses (not yaml-only) so they round-trip cleanly and
type-check in editors.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal, TypedDict

# Re-export Phase 1's relation roles for consistency
RelationRole = Literal["support", "attack", "psupport", "pattack"]
ComponentKind = Literal["claim", "premise", "citation"]


class ComponentDict(TypedDict):
    id: int
    type: ComponentKind
    text: str


class RelationDict(TypedDict):
    src: int            # component id of the source (usually premise/citation)
    tgt: int            # component id of the target (usually claim)
    type: RelationRole


class ArgStructureDict(TypedDict, total=False):
    """JSON-serialisable form of an ArgStructure.

    Compatible across datasets that may or may not include citations —
    `citation_components` is optional and defaults to [].
    """
    claim_components: list[ComponentDict]
    premise_components: list[ComponentDict]
    citation_components: list[ComponentDict]
    relations: list[RelationDict]


class TrainRecord(TypedDict, total=False):
    """One row of the Phase 2 training corpus."""
    instruction: str           # Task description (constant across rows)
    input: str                 # Source text the student reads
    reasoning: str             # CoT trace (silver only; empty for gold)
    output: ArgStructureDict   # Target structure
    source_dataset: str        # 'aaec' | 'abstrct' | 'liararg' | 'cdcp' | ...
    label_kind: Literal["gold", "silver"]
    split: Literal["train", "val", "test"]
    domain: str                # Free-form domain tag for cross-domain eval


# ────────────────────────────────────────────────────────────────────────────
# Component / Trainer configs
# ────────────────────────────────────────────────────────────────────────────

@dataclass
class TeacherConfig:
    backend: Literal[
        "dummy", "groq", "openai", "anthropic",
        "hf_inference", "local_hf", "together", "cerebras",
    ] = "dummy"
    model: str = ""                   # e.g. "llama-3.3-70b-versatile"
    api_base_url: str = ""            # optional override
    max_input_chars: int = 4000
    max_output_tokens: int = 800
    rpm_cap: int = 25
    max_requests_per_day: int = 950
    seed: int = 42
    include_cot: bool = True          # request <think>...</think> from teacher
    retries_per_call: int = 3
    # Only used by local_hf backend:
    quantization: Literal["none", "4bit", "8bit"] = "none"
    device: str = "auto"              # "auto" / "cuda" / "cuda:0" / "cpu"


@dataclass
class StudentConfig:
    backend: Literal["dummy", "hf"] = "dummy"
    base_model: str = "google/flan-t5-large"   # alt: "meta-llama/Llama-3.1-8B"
    max_input_len: int = 512
    max_target_len: int = 512
    batch_size: int = 4
    grad_accum: int = 8
    learning_rate: float = 3e-4
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    num_epochs: int = 5
    fp16: bool = True                 # AMP — gives ~30% speedup on Volta+
    gradient_checkpointing: bool = True
    # Optimizer choice. "adafactor" is the canonical choice for T5
    # (low memory footprint, Google's own choice for T5 fine-tuning) and
    # is what lets Flan-T5-Large fit in 11 GB VRAM with Adam-class
    # state savings of ~4 GB. Use "adamw_torch" for non-T5 models.
    optim: Literal["adafactor", "adamw_torch", "adamw_torch_fused", "adamw_bnb_8bit"] = "adafactor"
    seed: int = 42
    eval_every_steps: int = 0          # 0 = epoch-level eval
    # ────────────────────────────────────────────────────────────────────
    # LoRA (Phase 2-β-v2): when use_lora=True, freeze the base model and
    # train low-rank adapter matrices on the attention projections instead.
    # Lets us run Qwen-1.5B+ on 11 GB Pascal (gradients + optimizer state
    # drop from ~6 GB to ~10 MB; only the adapter trains).
    # ────────────────────────────────────────────────────────────────────
    use_lora: bool = False
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: str = "q_proj,k_proj,v_proj,o_proj"
    # When set, load this adapter and continue training instead of starting
    # fresh. Used for Phase 2-β-v3: resume from v2's adapter, train 1 more
    # epoch on the expanded 5-source gold pool. Saves ~10 hours vs from-scratch.
    resume_from_adapter: str = ""


@dataclass
class DatasetConfig:
    """Where each source dataset lives and which split goes where."""
    aaec_path: str = ""               # if set, ingested as gold
    abstrct_path: str = ""            # if set, ingested as gold
    liararg_path: str = ""            # if set, ingested as gold
    aries_clean_path: str = ""        # CSV with `data_source, argument` cols
    silver_sources: list[str] = field(default_factory=lambda: [
        "US2016", "US2016R1", "CDCP", "Microtext", "Cuties", "ACSP",
    ])
    samples_per_silver_source: int = 200   # cap for teacher annotation
    val_frac: float = 0.10
    test_frac: float = 0.10
    seed: int = 42
    output_dir: str = "phase2_data"


@dataclass
class Phase2Config:
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    teacher: TeacherConfig = field(default_factory=TeacherConfig)
    student: StudentConfig = field(default_factory=StudentConfig)
    student_output_dir: str = "phase2_student_model"
    run_name: str = "phase2"

    def to_dict(self) -> dict:
        return asdict(self)
