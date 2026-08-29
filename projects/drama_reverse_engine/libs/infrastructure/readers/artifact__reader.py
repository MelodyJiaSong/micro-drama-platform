from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


class ArtifactReader:
    def __init__(self, workspace: SafeWorkspace) -> None:
        self._workspace = workspace

    def exists(self, rel_path: str) -> bool:
        return Path(self._workspace.resolve(rel_path)).exists()

    def read_json(self, rel_path: str) -> Any:
        return json.loads(Path(self._workspace.resolve(rel_path)).read_text(encoding="utf-8"))

    def read_text(self, rel_path: str) -> str:
        return Path(self._workspace.resolve(rel_path)).read_text(encoding="utf-8")
