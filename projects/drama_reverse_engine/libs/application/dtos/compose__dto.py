from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComposeResultCdto:
    episode_rel_dir: str
    shot_files: list[str]
    script_rel_path: str
    novel_rel_path: str
    degradations: list[str]
    skipped: bool = False
