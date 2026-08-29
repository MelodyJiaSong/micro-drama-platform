from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UnderstandResultCdto:
    episode_rel_dir: str
    shot_count: int
    low_confidence_count: int
    speaker_low_confidence_count: int
    skipped: bool = False
