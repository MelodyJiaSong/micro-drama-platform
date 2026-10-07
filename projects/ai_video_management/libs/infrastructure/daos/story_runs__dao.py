from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StoryRunsDao:
    episode_path: str
    runs: list[dict[str, Any]]
