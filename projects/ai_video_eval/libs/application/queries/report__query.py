import os

from libs.domain.errors.eval__error import ArtifactError
from libs.infrastructure.readers.run__reader import RunReader


class ReportQuery:
    def __init__(self, runs_dir: str, run_reader: RunReader) -> None:
        self._runs_dir = runs_dir
        self._run_reader = run_reader

    def latest_report(self, project: str) -> str:
        pointer = self._run_reader.latest_pointer(project)
        if pointer is None:
            raise ArtifactError(f"no runs recorded for project {project}")
        path = os.path.join(self._runs_dir, pointer["report_path"])
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()

    def report_for(self, run_id: str) -> str:
        path = os.path.join(self._runs_dir, run_id, "report.md")
        if not os.path.isfile(path):
            raise ArtifactError(f"report not found for run {run_id}")
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
