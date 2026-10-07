from __future__ import annotations

from typing import Any

from libs.application.dtos.story_runs__dto import StoryRunsQdto
from libs.common.story_runs import StoryRunsError
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader
from libs.infrastructure.readers.story_selection__reader import StorySelectionReader
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.domain.entities.episode_workflow__entity import EpisodeWorkflowEntity
from libs.domain.entities.story_selection__entity import StorySelectionEntity
from libs.common.episode_workflow import fingerprint


class StoryRunsQuery:
    def __init__(self, reader: StoryRunsReader, selections: StorySelectionReader, workflows: EpisodeWorkflowReader) -> None:
        self.reader = reader
        self.selections = selections
        self.workflows = workflows

    def read(self, episode_path: str) -> StoryRunsQdto:
        try:
            dao = self.reader.read(episode_path)
            stored = self.selections.read(episode_path)
            selection = None
            if stored is not None:
                workflow = EpisodeWorkflowEntity(self.workflows.read(episode_path).documents)
                selected_run = next((run for run in dao.runs if run["run_id"] == stored["run_id"]), None)
                selection = {**stored, "status": StorySelectionEntity(stored).status(workflow, selected_run)}
            _, entries = self.reader.index(episode_path)
            paths = {entry["run_id"]: entry["audit_path"] for entry in entries}
        except FileNotFoundError as exc:
            raise StoryRunsError("找不到创作记录", 404) from exc
        except (ValueError, OSError) as exc:
            raise StoryRunsError("创作记录格式无效，请检查索引和日志") from exc
        summaries = [{"run_id": run["run_id"], "created_at": run["created_at"], "status": run["status"],
                      "participant_count": len(run["participants"]), "proposal_count": len(run["proposals"]),
                      "input_hash": run["input"]["input_hash"], "rules_hash": fingerprint(run["input"]["rules"]),
                      "title": run["candidate"].get("title") or run["candidate"]["brief"],
                      "audit_path": paths[run["run_id"]], "audit_folder": paths[run["run_id"]].rsplit("/", 1)[0],
                      "selected": selection is not None and selection["status"] == "selected" and selection["run_id"] == run["run_id"]}
                     for run in dao.runs]
        return StoryRunsQdto(dao.episode_path, summaries, selection)

    def detail(self, episode_path: str, run_id: str) -> dict[str, Any]:
        try:
            run = self.reader.detail(episode_path, run_id)
            return {**run, "io": self.reader.describe(run)}
        except FileNotFoundError as exc:
            raise StoryRunsError("找不到创作记录", 404) from exc
        except (ValueError, OSError) as exc:
            raise StoryRunsError("创作记录格式无效，请检查索引和日志") from exc
