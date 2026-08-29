import json
import os


class RunReader:
    def __init__(self, runs_dir: str) -> None:
        self._runs_dir = runs_dir

    def latest_pointer(self, project: str) -> dict | None:
        path = os.path.join(self._runs_dir, "latest", f"{project}.json")
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def manifest(self, run_id: str) -> dict | None:
        path = os.path.join(self._runs_dir, run_id, "manifest.json")
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def verdicts(self, run_id: str) -> dict | None:
        path = os.path.join(self._runs_dir, run_id, "verdicts.json")
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def findings(self, run_id: str) -> list[dict]:
        path = os.path.join(self._runs_dir, run_id, "findings.json")
        if not os.path.isfile(path):
            return []
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def list_runs(self, project: str | None = None) -> list[dict]:
        if not os.path.isdir(self._runs_dir):
            return []
        manifests = []
        for name in sorted(os.listdir(self._runs_dir)):
            if name == "latest":
                continue
            manifest = self.manifest(name)
            if manifest and (project is None or manifest.get("project") == project):
                manifests.append(manifest)
        return manifests
