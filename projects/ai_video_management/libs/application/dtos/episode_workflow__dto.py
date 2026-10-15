from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EpisodeWorkflowQdto:
    episode_path: str
    modules: list[dict[str, Any]]
    shot_keys: dict[str, dict[str, str]]
    packs: dict[str, dict[str, Any]] = field(default_factory=dict)   # shot key -> 资料包 status and files (follow-up 229)
    renders: dict[str, list[dict[str, Any]]] = field(default_factory=dict)   # shot key -> generations, newest first (follow-up 230)


@dataclass(frozen=True)
class EpisodeWorkflowCdto:
    module: str
