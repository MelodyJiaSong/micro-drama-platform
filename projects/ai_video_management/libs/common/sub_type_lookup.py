"""Sub_type detection for ai_video projects.

Heuristic (does not look outside `ai_videos/{name}/`):

- If the episodes tree exists with at least one `epNN/` child → `novel`.
- Else if `script.md`, `shotlist.md`, or a flat `shots/shotNN/` tree exists → `short`.
- Else → `None` (project shape not yet recognisable).

Every path is resolved through `drama_layout`, so both the legacy flat root and
the staged pipeline (`4_剧本/`, `5_6_分镜与prompt/`) are recognised.

Trade-off: a novel project mid-creation without any episode folders yet would
mis-detect as short. Acceptable; user can fix downstream by adding the first
`epNN/` placeholder.
"""
from __future__ import annotations

from dataclasses import dataclass
from libs.common import drama_layout
from pathlib import Path
from typing import Literal

import re

SubType = Literal["novel", "short"]

_EPISODE_DIR_RE = re.compile(r"^ep\d+$")
_SHOT_DIR_RE = re.compile(r"^shot\d+$")


@dataclass(frozen=True)
class ProjectMeta:
    sub_type: SubType | None
    shot_count: int | None
    episode_count: int | None


def lookup(repo_root: Path, project_name: str) -> ProjectMeta:
    project_dir = repo_root / "ai_videos" / project_name
    if not project_dir.is_dir():
        return ProjectMeta(sub_type=None, shot_count=None, episode_count=None)
    episode_count = _count_episodes(project_dir)
    sub_type: SubType | None
    if episode_count is not None and episode_count > 0:
        sub_type = "novel"
    elif _looks_like_short(project_dir):
        sub_type = "short"
    else:
        sub_type = None
    shot_count = _count_shots(project_dir)
    return ProjectMeta(sub_type=sub_type, shot_count=shot_count, episode_count=episode_count)


def _count_episodes(project_dir: Path) -> int | None:
    episodes_dir = drama_layout.episodes_dir(project_dir)
    if not episodes_dir.is_dir():
        return None
    count = sum(1 for p in episodes_dir.iterdir() if p.is_dir() and _EPISODE_DIR_RE.match(p.name))
    return count


def _looks_like_short(project_dir: Path) -> bool:
    """Short layout: script.md / shotlist.md / a flat shots tree, no episodes/.
    Each of the three is resolved through `drama_layout`, so the staged pipeline
    (`4_剧本/script.md`, `5_6_分镜与prompt/{shotlist.md, shots/}`) counts as well
    as the legacy flat root."""
    if drama_layout.shotlist_md(project_dir).is_file():
        return True
    if drama_layout.script_md(project_dir).is_file():
        return True
    return _has_flat_shots(project_dir)


def _has_flat_shots(project_dir: Path) -> bool:
    shots = drama_layout.shots_dir(project_dir)
    if not shots.is_dir():
        return False
    return any(p.is_dir() and _SHOT_DIR_RE.match(p.name) for p in shots.iterdir())


def _count_shots(project_dir: Path) -> int | None:
    shotlist = drama_layout.shotlist_md(project_dir)
    if not shotlist.is_file():
        return None
    try:
        text = shotlist.read_text(encoding="utf-8")
    except OSError:
        return None
    pattern = re.compile(r"^\|\s*`?(shot\d+)`?\s*\|", re.MULTILINE)
    shots = set(pattern.findall(text))
    return len(shots) if shots else None
