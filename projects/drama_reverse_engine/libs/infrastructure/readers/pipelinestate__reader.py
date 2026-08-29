from __future__ import annotations

import json
from pathlib import Path

from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


class PipelineStateReader:
    def __init__(self, workspace: SafeWorkspace) -> None:
        self._workspace = workspace

    def read(self, episode_rel_dir: str) -> dict | None:
        path = Path(self._workspace.resolve(f"{episode_rel_dir}/pipeline_state.json"))
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_episode_dirs(self, drama_id: str) -> list[str]:
        root = Path(self._workspace.resolve(drama_id))
        if not root.is_dir():
            return []
        return sorted(
            f"{drama_id}/{p.name}" for p in root.iterdir()
            if p.is_dir() and p.name.startswith("ep") and (p / "pipeline_state.json").exists()
        )

    def list_drama_ids(self) -> list[str]:
        root = Path(self._workspace.resolve("."))
        if not root.is_dir():
            return []
        return sorted(p.name for p in root.iterdir() if p.is_dir() and (p / "drama.json").exists())
