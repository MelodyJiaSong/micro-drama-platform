"""Eval-center queries: read-only views over ai_video_eval's rubric / config / runs."""
from __future__ import annotations

from libs.infrastructure.readers.eval_center__reader import EvalCenterReader


class EvalCenterQuery:
    def __init__(self, reader: EvalCenterReader) -> None:
        self._reader = reader

    def overview(self) -> dict[str, object]:
        return self._reader.overview()

    def rubric_file(self, name: str) -> dict[str, object]:
        return self._reader.rubric_file(name)

    def config(self) -> dict[str, object]:
        return self._reader.config()

    def runs(self) -> dict[str, object]:
        return self._reader.runs()

    def run_detail(self, run_id: str) -> dict[str, object]:
        return self._reader.run_detail(run_id)

    def report(self, run_id: str) -> dict[str, object]:
        return self._reader.report(run_id)

    def unit_results(self, run_id: str, unit_id: str) -> dict[str, object]:
        return self._reader.unit_results(run_id, unit_id)

    def raw_judgments(self, run_id: str, unit_id: str, dim_id: str) -> dict[str, object]:
        return self._reader.raw_judgments(run_id, unit_id, dim_id)
