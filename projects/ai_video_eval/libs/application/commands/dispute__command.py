import json
import os
from datetime import datetime, timezone

from libs.domain.errors.eval__error import ArtifactError
from libs.infrastructure.daos.config__dao import EvalConfigDao
from libs.infrastructure.readers.run__reader import RunReader


class DisputeCommand:
    def __init__(self, config: EvalConfigDao, run_reader: RunReader) -> None:
        self._config = config
        self._run_reader = run_reader

    def record(self, project: str, finding_id: str, because: str, run_id: str | None = None) -> str:
        if run_id is None:
            pointer = self._run_reader.latest_pointer(project)
            if pointer is None:
                raise ArtifactError(f"no runs recorded for project {project}")
            run_id = pointer["run_id"]
        findings = self._run_reader.findings(run_id)
        finding = next((f for f in findings if f["finding_id"] == finding_id), None)
        if finding is None:
            raise ArtifactError(f"finding {finding_id} not found in run {run_id}")

        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        record = {
            "ts": ts,
            "run_id": run_id,
            "project": project,
            "finding": finding,
            "user_verdict": because,
        }
        os.makedirs(self._config.disputes_dir, exist_ok=True)
        dispute_path = os.path.join(self._config.disputes_dir, f"{ts}_{finding_id}.json")
        with open(dispute_path, "w", encoding="utf-8") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=1)

        os.makedirs(self._config.golden_dir, exist_ok=True)
        golden_path = os.path.join(self._config.golden_dir, "golden.jsonl")
        with open(golden_path, "a", encoding="utf-8") as fh:
            fh.write(
                json.dumps(
                    {
                        "unit_id": finding["unit_id"],
                        "field_id": finding["field_id"],
                        "eval_grade": finding["grade"],
                        "user_verdict": because,
                        "run_id": run_id,
                        "rubric_note": "dispute",
                        "ts": ts,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        return dispute_path
