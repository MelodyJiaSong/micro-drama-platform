from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractResultCdto:
    episode_rel_dir: str
    shot_count: int
    dialogue_line_count: int
    flagged_line_count: int
    degradations: list[str]
    skipped: bool = False
