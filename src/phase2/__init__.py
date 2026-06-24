"""Phase 2: ArgParserLLM — learned cross-domain argument parser.

Scaffold-first design: every component has a Dummy implementation that
runs end-to-end on a laptop in seconds, and a Real implementation that
needs API keys or GPU. The Dummy variants let you test the whole
plumbing (data → teacher → student → ArgParserLLM → Phase 1 integration)
without external dependencies. Real variants drop in by config change.

Interfaces:
  - TeacherBase       (teacher.py)     annotate() -> dict
  - StudentTrainerBase(student.py)     train(data, cfg) -> model_path
  - ArgParserLLM      (arg_parser_llm.py) parse() -> ArgStructure

Phase 1 doesn't need to know any of this exists. Plug ArgParserLLM into
src/arg_parser/__init__.py exactly the same way GoldArgParser is plugged
in today — one-file swap.
"""
