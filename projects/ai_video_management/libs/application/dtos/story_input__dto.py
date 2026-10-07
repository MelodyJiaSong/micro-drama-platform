from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StoryInputQdto:
    episode_path: str
    selected_profile: str
    profile_id: str
    profiles: list[dict[str, Any]]
    input: dict[str, Any]
