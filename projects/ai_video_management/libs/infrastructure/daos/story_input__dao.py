from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StoryInputDao:
    episode_path: str
    selected_profile: str
    profiles: list[dict[str, Any]]
    inputs: dict[str, dict[str, Any]]
