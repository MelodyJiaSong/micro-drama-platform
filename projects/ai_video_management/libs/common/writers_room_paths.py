from __future__ import annotations

from pathlib import Path
import re


def story_path(root: Path, slug: str) -> Path:
    if not re.fullmatch(r"[a-z0-9_]{1,80}", slug):
        raise ValueError("剧目标识只能包含小写字母、数字、下划线。")
    path = (root / "ai_videos" / slug).resolve()
    if not path.is_relative_to((root / "ai_videos").resolve()):
        raise ValueError("剧目路径超出工作区。")
    return path


def room_path(root: Path, slug: str) -> Path:
    return story_path(root, slug) / "4_剧本" / "writers_room"


def bible_path(root: Path, slug: str) -> Path:
    return story_path(root, slug) / "2_世界观人设" / "writers_room"
