from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EpisodeWorkflowDao:
    episode_path: str
    documents: dict[str, dict[str, Any]]
