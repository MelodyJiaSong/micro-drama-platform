"""Resolve a drama's asset locations.

Assets live under `ai_videos/{drama}/2_世界观人设/` (`characters/`,
`background/`, `props/`, `equipment/`); a few older dramas keep the same
folders directly at the drama root, and `scenes/` is still accepted as the
legacy name of `background/`. These helpers take the drama root dir and return
the *actual* location — preferring whichever exists, falling back to the flat
root so first-time `create` still lands somewhere sane.

Shot folders are the six-module layout only: `episodes/epNN/scenes/sN/shots/stN/`
(ordered by the compiled `prompts.json` when present). The old 0–7 stage
layouts (`5_6_分镜与prompt/`, `4_剧本/`, `shots/shotNN/`, `prompts/shotNN/`,
single-piece `shots/`) and their helpers were removed in follow-up 233.
"""
from __future__ import annotations

import json
from pathlib import Path
from libs.common.production_key import BACKGROUND_DIR_NAME, SCENES_DIR_NAME, SCENE_ID_RE, SHOT_ID_RE, first_shot_key

SHOTS_DIR_NAME: str = "shots"
EPISODES_DIR_NAME: str = "episodes"

WORLD_STAGE: str = "2_世界观人设"

EQUIPMENT_DIR_NAME: str = "equipment"
# Per-character loadout tables beside the category / slot folders — never an item.
EQUIPMENT_LOADOUTS_DIR_NAME: str = "loadouts"


def is_equipment_tool_dir(name: str) -> bool:
    """A folder under `equipment/` that holds no items, at any depth: `loadouts/`,
    and anything `_`- or `.`-prefixed. Every other unkeyed folder (a category
    `板甲/`, a slot `胸/` — per-drama, any nesting) is walked through to its items."""
    return name == EQUIPMENT_LOADOUTS_DIR_NAME or name.startswith((".", "_"))


def _first_existing_dir(*candidates: Path) -> Path:
    for c in candidates:
        if c.is_dir():
            return c
    return candidates[0]


def characters_dir(drama_dir: Path) -> Path:
    return _first_existing_dir(
        drama_dir / "characters", drama_dir / WORLD_STAGE / "characters"
    )


def background_dir(drama_dir: Path) -> Path:
    """Environment assets; the legacy scenes path is accepted for other dramas."""
    return _first_existing_dir(
        drama_dir / BACKGROUND_DIR_NAME, drama_dir / WORLD_STAGE / BACKGROUND_DIR_NAME,
        drama_dir / "scenes", drama_dir / WORLD_STAGE / "scenes"
    )


scenes_dir = background_dir


def episode_shot_dirs(episode: Path) -> list[Path]:
    """The episode's shot folders `scenes/sN/shots/stN/`, in compiled order when
    `prompts.json` exists (only folders already on disk), else scene then shot
    number. Empty for anything else."""
    compiled = episode / "prompts.json"
    if compiled.is_file() and not compiled.is_symlink():
        data = json.loads(compiled.read_text(encoding="utf-8"))
        scenes = data.get("content", {}).get("scenes")
        if isinstance(scenes, list):
            folders = []
            seen = set()
            for scene in scenes:
                for shot in scene["shots"]:
                    key = first_shot_key(shot["id"])
                    if (key is None or key.value != shot["id"] or key.episode != int(episode.name[2:])
                            or scene["id"] != f"s{key.scene}" or key.value in seen):
                        raise ValueError("编译镜头key重复或与所属集、场不一致")
                    seen.add(key.value)
                    path = key.folder(episode)
                    if path.is_dir() and not any(p.is_symlink() for p in (path, *path.parents)):
                        folders.append(path)
            return folders
    scenes_root = episode / SCENES_DIR_NAME
    if scenes_root.is_dir() and not scenes_root.is_symlink():
        folders = []
        for scene in sorted(scenes_root.iterdir(), key=lambda p: int(SCENE_ID_RE.fullmatch(p.name)[1]) if SCENE_ID_RE.fullmatch(p.name) else 0):
            if not scene.is_dir() or scene.is_symlink() or not SCENE_ID_RE.fullmatch(scene.name):
                continue
            shots = scene / SHOTS_DIR_NAME
            if shots.is_dir() and not shots.is_symlink():
                folders.extend(sorted((p for p in shots.iterdir() if p.is_dir() and not p.is_symlink() and SHOT_ID_RE.fullmatch(p.name)),
                                      key=lambda p: int(SHOT_ID_RE.fullmatch(p.name)[1])))
        return folders
    return []


def props_dir(drama_dir: Path) -> Path:
    """`props/` — flat root or `2_世界观人设/`. Resolved on its own rather than
    as `characters_dir(...).parent / "props"`: that derivation only found the
    staged props when a `characters/` sibling also existed, so a drama with
    props but no character folder silently fell back to the flat root."""
    return _first_existing_dir(
        drama_dir / "props", drama_dir / WORLD_STAGE / "props"
    )


def equipment_dir(drama_dir: Path) -> Path:
    """`equipment/` — flat root or `2_世界观人设/`, resolved on its own like `props_dir`."""
    return _first_existing_dir(
        drama_dir / EQUIPMENT_DIR_NAME, drama_dir / WORLD_STAGE / EQUIPMENT_DIR_NAME
    )


def episodes_dir(drama_dir: Path) -> Path:
    """`episodes/` at the drama root — the tree the downloads import walks
    (`episodes/epNN/scenes/sN/shots/stN/renders/`)."""
    return drama_dir / EPISODES_DIR_NAME
