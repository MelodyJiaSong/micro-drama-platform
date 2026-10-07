"""Resolve a drama's asset locations across the two on-disk layouts.

Two structures coexist under `ai_videos/{drama}/`:

* **legacy / flat** — `casting.md`, `characters/`, `scenes/`, `episodes/`
  directly at the drama root.
* **staged pipeline** (`全流程编排`) — assets live under numbered stage
  folders: `2_世界观人设/{casting.md, characters/, scenes/}`, script
  episodes under `4_剧本/episodes/`, and the shot/render episodes (the
  `episodes/{ep}/shots/shot{NN}/` tree the downloads-import, render scan
  and episode-compose all operate on) under `5_6_分镜与prompt/episodes/`.

Every consumer (casting assign, downloads import, sub-type lookup, render
scan, …) must work for both. These helpers take the drama root dir and return
the *actual* location — preferring whichever exists, falling back to the flat
root so first-time `create` still lands somewhere sane.
"""
from __future__ import annotations

import re
import json
from pathlib import Path
from libs.common.production_key import BACKGROUND_DIR_NAME, SCENES_DIR_NAME, SCENE_ID_RE, SHOT_ID_RE, first_shot_key

EP_DIR_RE = re.compile(r"^ep\d+$", re.IGNORECASE)
SHOTS_DIR_NAME: str = "shots"
EPISODES_DIR_NAME: str = "episodes"

WORLD_STAGE: str = "2_世界观人设"
SCRIPT_STAGE: str = "4_剧本"
SHOTS_STAGE: str = "5_6_分镜与prompt"

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


def _first_existing_file(*candidates: Path) -> Path:
    for c in candidates:
        if c.is_file():
            return c
    return candidates[0]


def casting_md(drama_dir: Path) -> Path:
    """`casting.md` — flat root or `2_世界观人设/`. Falls back to flat root."""
    return _first_existing_file(
        drama_dir / "casting.md", drama_dir / WORLD_STAGE / "casting.md"
    )


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
    """Current ordered scene shots, or legacy episode/flat shot folders."""
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
    shots = episode / SHOTS_DIR_NAME
    if not shots.is_dir():
        shots = episode / "prompts"
    if not shots.is_dir() or shots.is_symlink():
        return []
    return sorted((p for p in shots.iterdir() if p.is_dir() and not p.is_symlink() and re.fullmatch(r"shot\d+", p.name, re.I)),
                  key=lambda p: int(re.search(r"\d+", p.name)[0]))


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
    """The episodes tree the render-side consumers walk (downloads import,
    episode compose, render scan). The staged pipeline puts the shot/render
    episodes — `episodes/{ep}/shots/shot{NN}/` — under `5_6_分镜与prompt/`, so
    that stage is preferred over the script-only `4_剧本/episodes/` (which has
    no `shots/` and previously caused shot renders to misroute). Legacy flat
    `episodes/` still wins when present."""
    return _first_existing_dir(
        drama_dir / "episodes",
        drama_dir / SHOTS_STAGE / "episodes",
        drama_dir / SCRIPT_STAGE / "episodes",
    )


def script_md(drama_dir: Path) -> Path:
    """Single-piece `script.md` — flat root or `4_剧本/`."""
    return _first_existing_file(
        drama_dir / "script.md", drama_dir / SCRIPT_STAGE / "script.md"
    )


def shotlist_md(drama_dir: Path) -> Path:
    """Single-piece `shotlist.md` — flat root or `5_6_分镜与prompt/`."""
    return _first_existing_file(
        drama_dir / "shotlist.md", drama_dir / SHOTS_STAGE / "shotlist.md"
    )


def shots_dir(drama_dir: Path) -> Path:
    """The single-piece `shots/` tree — flat root or `5_6_分镜与prompt/`.
    Multi-episode dramas keep their shots under `episodes/{ep}/shots/` instead
    (see `episodes_dir`), so this resolving to a real dir is itself evidence of
    a single-piece project."""
    return _first_existing_dir(
        drama_dir / "shots", drama_dir / SHOTS_STAGE / "shots"
    )


def shot_tree_roots(drama_dir: Path) -> list[Path]:
    """Every dir that directly owns a `shots/shot{NN}/` tree.

    Multi-episode dramas have one per `episodes/ep{NN}/`; a **single-piece**
    drama (`sub_type=short` — no `episodes/` layer at all, shots sit at
    `shots/` under the drama root or the `5_6_分镜与prompt/` stage) has exactly
    one, the dir holding that `shots/`.

    This is the single source of truth for "where are this drama's shot trees".
    Every drama-wide walker (episode listing, 全局定版, 全剧烧字幕) must use it
    rather than globbing `episodes/` itself — that duplication is what made all
    three silently no-op on single-piece dramas.
    """
    episodes = episodes_dir(drama_dir)
    if episodes.is_dir():
        try:
            eps = [
                e for e in sorted(episodes.iterdir(), key=lambda p: p.name)
                if e.is_dir() and not e.is_symlink() and EP_DIR_RE.match(e.name)
            ]
        except OSError:
            eps = []
        if eps:
            return eps
    single = shots_dir(drama_dir)
    return [single.parent] if single.is_dir() else []


def is_episode_root(root: Path) -> bool:
    return bool(EP_DIR_RE.match(root.name))


def shot_tree_slug(root: Path, drama_dir: Path) -> str:
    """Stable name for a shot tree — the ep folder name, or the drama name for a
    single-piece drama. Doubles as the stitched master's stem
    (`ep04.mp4` / `{drama}.mp4`)."""
    return root.name.lower() if is_episode_root(root) else drama_dir.name


def shot_tree_for(
    drama_dir: Path, rel_parts: list[str], drama_depth: int = 2
) -> tuple[Path, str] | None:
    """Which shot tree does a repo-relative path under this drama belong to?

    Returns `(root_dir, slug)`, or `None` when the path is under neither an
    `episodes/ep{NN}/` nor a single-piece shot tree. Callers keep doing their own
    sandbox resolution; this only answers the layout question.

    `drama_depth` is how many leading segments of `rel_parts` name the drama root
    (2 flat, 3 inside a series — see `libs.common.drama_ref`); everything after it
    is the path *within* the drama.
    """
    for i in range(drama_depth - 1, len(rel_parts) - 1):
        if rel_parts[i] == EPISODES_DIR_NAME and EP_DIR_RE.match(rel_parts[i + 1]):
            root = drama_dir.joinpath(*rel_parts[drama_depth : i + 2])
            return root, rel_parts[i + 1].lower()
    roots = shot_tree_roots(drama_dir)
    if len(roots) == 1 and not is_episode_root(roots[0]):
        return roots[0], shot_tree_slug(roots[0], drama_dir)
    return None
