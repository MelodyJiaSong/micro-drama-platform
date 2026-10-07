from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EpisodeWorkflowQdto:
    episode_path: str
    modules: list[dict[str, Any]]
    shot_keys: dict[str, dict[str, str]]


@dataclass(frozen=True)
class EpisodeWorkflowCdto:
    module: str
