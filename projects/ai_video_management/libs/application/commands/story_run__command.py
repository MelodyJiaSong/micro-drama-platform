from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from libs.domain.entities.story_run__entity import StoryRunEntity
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader
from libs.infrastructure.writers.story_runs__writer import StoryRunsWriter
from libs.common.story_runs import StoryRunsError
from libs.common.episode_workflow import fingerprint
from libs.domain.entities.episode_workflow__entity import EpisodeWorkflowEntity
from libs.domain.entities.story_selection__entity import StorySelectionEntity
from libs.infrastructure.readers.story_selection__reader import StorySelectionReader
from libs.infrastructure.readers.story_input__reader import StoryInputReader
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader


class StoryRunCommand:
    def __init__(self, reader: StoryRunsReader, writer: StoryRunsWriter,
                 inputs: StoryInputReader, selections: StorySelectionReader,
                 workflows: EpisodeWorkflowReader) -> None:
        self.reader = reader
        self.writer = writer
        self.inputs = inputs
        self.selections = selections
        self.workflows = workflows

    def begin_from_file(self, episode_path: str, file_path: str) -> dict[str, Any]:
        try:
            value = self.inputs.read_file(episode_path, file_path)
        except FileNotFoundError as exc:
            raise StoryRunsError("找不到显式创作输入或规则文件", 404) from exc
        except (ValueError, OSError) as exc:
            raise StoryRunsError("显式创作输入或规则文件无效") from exc
        return self.begin(episode_path, value)

    def promote(self, episode_path: str, run_id: str) -> dict[str, Any]:
        try:
            with self.writer.episode_lock(episode_path):
                run = self.reader.detail(episode_path, run_id)
                workflow = self.workflows.read(episode_path)
                entity = EpisodeWorkflowEntity(workflow.documents)
                expected = fingerprint(workflow.documents["story"])
                selection = StorySelectionEntity(self.selections.read(episode_path)).promote(
                    run, entity, datetime.now(timezone.utc).isoformat())
                self.writer.promote(workflow.episode_path, entity.documents["story"], selection, expected)
                return {**selection, "status": "selected", "story_status": "draft"}
        except FileNotFoundError as exc:
            raise StoryRunsError("找不到本集的候选run", 404) from exc
        except (ValueError, OSError) as exc:
            raise StoryRunsError("无法载入故事候选，请检查故事、run和选择记录") from exc

    def begin(self, episode_path: str, input_dict: dict[str, Any]) -> dict[str, Any]:
        entity = StoryRunEntity.from_input(input_dict)
        try:
            canonical, _ = self.reader.index(episode_path)
            now = datetime.now(timezone.utc)
            run_id = f"story-run-{now.strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"
            run = entity.begin(run_id, canonical, now.isoformat())
            audit_path = self.writer.begin(run)
        except FileNotFoundError as exc:
            raise StoryRunsError("找不到剧集或创作索引", 404) from exc
        except (ValueError, OSError) as exc:
            raise StoryRunsError("无法创建独立创作记录，请检查路径和索引") from exc
        return {**run, "audit_path": audit_path}
