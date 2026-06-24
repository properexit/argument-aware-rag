"""YAML config loader for Phase 2.

Loads a YAML file into a Phase2Config dataclass. Round-trips cleanly
because the schema dataclasses use simple types (str / int / float /
list[str]) — no custom serialisation needed.
"""
from __future__ import annotations

from pathlib import Path

from .schema import (
    Phase2Config, DatasetConfig, TeacherConfig, StudentConfig,
)


def load_phase2_config(path: str | Path) -> Phase2Config:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("Install PyYAML: pip install pyyaml") from e

    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    dataset = DatasetConfig(**(raw.get("dataset") or {}))
    teacher = TeacherConfig(**(raw.get("teacher") or {}))
    student = StudentConfig(**(raw.get("student") or {}))
    return Phase2Config(
        dataset=dataset,
        teacher=teacher,
        student=student,
        student_output_dir=raw.get("student_output_dir", "phase2_student_model"),
        run_name=raw.get("run_name", "phase2"),
    )


def dump_phase2_config(cfg: Phase2Config, path: str | Path) -> None:
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("Install PyYAML: pip install pyyaml") from e
    with open(path, "w") as f:
        yaml.safe_dump(cfg.to_dict(), f, sort_keys=False)
