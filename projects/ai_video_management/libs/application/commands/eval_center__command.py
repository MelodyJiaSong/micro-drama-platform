"""Eval-center commands: save rubric files (validated + rollback) and config."""
from __future__ import annotations

from libs.infrastructure.writers.eval_center__writer import EvalCenterWriter


class EvalCenterCommand:
    def __init__(self, writer: EvalCenterWriter) -> None:
        self._writer = writer

    def save_rubric_file(self, name: str, content: str) -> dict[str, object]:
        return self._writer.save_rubric_file(name, content)

    def save_config(self, content: str) -> dict[str, object]:
        return self._writer.save_config(content)
