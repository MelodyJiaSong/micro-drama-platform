import json
import os


def sanitize_unit_id(unit_id: str) -> str:
    return unit_id.replace("/", "__")


class RunWriter:
    def __init__(self, runs_dir: str) -> None:
        self._runs_dir = runs_dir

    def run_dir(self, run_id: str) -> str:
        return os.path.join(self._runs_dir, run_id)

    def init_run(self, run_id: str, manifest: dict) -> str:
        run_dir = self.run_dir(run_id)
        os.makedirs(os.path.join(run_dir, "raw"), exist_ok=True)
        os.makedirs(os.path.join(run_dir, "results"), exist_ok=True)
        self.write_manifest(run_id, manifest)
        return run_dir

    def write_manifest(self, run_id: str, manifest: dict) -> None:
        self._write_json(os.path.join(self.run_dir(run_id), "manifest.json"), manifest)

    def write_raw(self, run_id: str, unit_id: str, dim_id: str, payload: dict) -> None:
        unit_dir = os.path.join(self.run_dir(run_id), "raw", sanitize_unit_id(unit_id))
        os.makedirs(unit_dir, exist_ok=True)
        self._write_json(os.path.join(unit_dir, f"{dim_id}.json"), payload)

    def write_unit_results(self, run_id: str, unit_id: str, results: dict) -> None:
        path = os.path.join(
            self.run_dir(run_id), "results", f"{sanitize_unit_id(unit_id)}.json"
        )
        self._write_json(path, results)

    def write_verdicts(self, run_id: str, verdicts: dict) -> None:
        self._write_json(os.path.join(self.run_dir(run_id), "verdicts.json"), verdicts)

    def write_findings(self, run_id: str, findings: list[dict]) -> None:
        self._write_json(os.path.join(self.run_dir(run_id), "findings.json"), findings)

    def write_report(self, run_id: str, text: str) -> str:
        path = os.path.join(self.run_dir(run_id), "report.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def write_latest_pointer(self, project: str, pointer: dict) -> None:
        latest_dir = os.path.join(self._runs_dir, "latest")
        os.makedirs(latest_dir, exist_ok=True)
        self._write_json(os.path.join(latest_dir, f"{project}.json"), pointer)

    @staticmethod
    def _write_json(path: str, data: object) -> None:
        tmp = f"{path}.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
