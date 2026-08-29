from libs.application.dtos.eval__dto import TrendsQdto
from libs.infrastructure.readers.run__reader import RunReader


class TrendsQuery:
    def __init__(self, run_reader: RunReader) -> None:
        self._run_reader = run_reader

    def compute(self, project: str) -> TrendsQdto:
        manifests = self._run_reader.list_runs(project)
        runs: list[dict] = []
        latest_run_id: str | None = None
        for manifest in manifests:
            run_id = manifest["run_id"]
            verdicts = self._run_reader.verdicts(run_id)
            if not verdicts:
                continue
            latest_run_id = run_id
            project_verdict = verdicts["project_verdict"]
            runs.append(
                {
                    "run_id": run_id,
                    "ts": manifest.get("ts"),
                    "tier": project_verdict["tier"],
                    "composite": project_verdict["composite"],
                    "dimensions": project_verdict["dimension_composites"],
                    "unit_count": project_verdict["unit_count"],
                }
            )
        recurring: dict[str, dict] = {}
        if latest_run_id:
            for finding in self._run_reader.findings(latest_run_id):
                entry = recurring.setdefault(
                    finding["field_id"],
                    {
                        "field_id": finding["field_id"],
                        "field_name_cn": finding["field_name_cn"],
                        "dim_id": finding["dim_id"],
                        "count": 0,
                        "blockers": 0,
                    },
                )
                entry["count"] += 1
                if finding["severity"] == "blocker":
                    entry["blockers"] += 1
        top = sorted(recurring.values(), key=lambda e: (-e["blockers"], -e["count"]))[:15]
        return TrendsQdto(project=project, runs=tuple(runs), recurring_fields=tuple(top))
