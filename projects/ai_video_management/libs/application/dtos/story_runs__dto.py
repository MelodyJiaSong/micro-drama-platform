from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StoryRunsQdto:
    episode_path: str
    runs: list[dict[str, Any]]
    selection: dict[str, Any] | None
