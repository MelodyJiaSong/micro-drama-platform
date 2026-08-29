from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MediaValidationCdto:
    ok: bool
    duration_s: float
    width: int
    height: int
    reason: str = ""


@dataclass(frozen=True)
class EpisodeSplitCdto:
    episode_rel_paths: list[str]
    confidences: list[str]
