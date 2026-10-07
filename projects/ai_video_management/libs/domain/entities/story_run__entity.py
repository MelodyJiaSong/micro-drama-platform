from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from libs.common.episode_workflow import fingerprint
from libs.common.story_runs import STORY_FRAME_FIELDS, STORY_RUN_SCHEMA_VERSION, StoryRunsError


@dataclass
class StoryRunEntity:
    input: dict[str, Any]

    @classmethod
    def from_input(cls, value: dict[str, Any]) -> StoryRunEntity:
        try:
            snapshot = json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False))
        except (ValueError, TypeError, OverflowError, RecursionError) as exc:
            raise StoryRunsError("创作输入必须是可序列化JSON") from exc
        if not isinstance(snapshot, dict):
            raise StoryRunsError("创作输入必须是对象")
        frame = snapshot.get("frame")
        if not isinstance(frame, dict) or not all(isinstance(frame.get(key), str) and frame[key].strip() for key in STORY_FRAME_FIELDS):
            raise StoryRunsError("故事六问who/what/why/when/where/how必须完整填写")
        if not isinstance(snapshot.get("brief"), str):
            raise StoryRunsError("故事方向brief必须是字符串")
        for key in ("assumptions", "sources", "rules"):
            if not isinstance(snapshot.get(key), list):
                raise StoryRunsError(f"创作输入{key}必须是列表")
        if not isinstance(snapshot.get("independence"), dict):
            raise StoryRunsError("必须明确记录本run的independence输入边界")
        snapshot.pop("input_hash", None)
        snapshot["input_hash"] = fingerprint(snapshot)
        return cls(snapshot)

    def begin(self, run_id: str, episode_path: str, created_at: str) -> dict[str, Any]:
        return {"schema_version": STORY_RUN_SCHEMA_VERSION, "run_id": run_id, "episode_path": episode_path,
                "created_at": created_at, "status": "started", "input": self.input,
                "participants": [], "events": [], "proposals": [], "artifacts": [],
                "candidate": {"frame": dict(self.input["frame"]), "brief": self.input["brief"], "text": "", "state_changes": []}}
