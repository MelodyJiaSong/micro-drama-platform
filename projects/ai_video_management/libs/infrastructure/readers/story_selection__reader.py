from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.common.story_runs import STORY_RUN_ID_RE, STORY_RUN_SCHEMA_VERSION, STORY_SELECTION_FILE
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader


class StorySelectionReader:
    def __init__(self, repo_root: Path) -> None:
        self.episodes = EpisodeWorkflowReader(repo_root)

    def read(self, episode_path: str) -> dict[str, Any] | None:
        self.episodes.resolve(episode_path)
        path = self.episodes.resolver.resolve(f"{episode_path}/{STORY_SELECTION_FILE}")
        if path is None:
            raise ValueError("故事选择路径无效")
        if not path.exists():
            return None
        document = json.loads(path.read_text(encoding="utf-8"))
        fields = ("run_id", "candidate_hash", "input_hash", "story_revision", "promoted_at")
        if not isinstance(document, dict) or type(document.get("schema_version")) is not int or document["schema_version"] != STORY_RUN_SCHEMA_VERSION:
            raise ValueError("故事选择格式无效")
        history = document.get("history")
        if not isinstance(history, list) or not history:
            raise ValueError("故事选择缺少有序历史")
        for entry in [document, *history]:
            if not isinstance(entry, dict) or not all(isinstance(entry.get(field), str) for field in fields) or not STORY_RUN_ID_RE.fullmatch(entry["run_id"]):
                raise ValueError("故事选择记录无效")
        if any(document[key] != history[-1][key] for key in fields):
            raise ValueError("故事选择与最后历史记录不一致")
        return document
