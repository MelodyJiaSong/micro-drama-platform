"""Resolve a drama's asset locations across the two on-disk layouts.

Two structures coexist under `ai_videos/{drama}/`:

* **legacy / flat** — `casting.md`, `characters/`, `scenes/`, `episodes/`
  directly at the drama root.
* **staged pipeline** (`全流程编排`) — assets live under numbered stage
  folders: `2_世界观人设/{casting.md, characters/, scenes/}`, script
  episodes under `4_剧本/episodes/`, and the shot/render episodes (the
  `episodes/{ep}/shots/shot{NN}/` tree the downloads-import, bgm-cue scan
  and episode-compose all operate on) under `5_6_分镜与prompt/episodes/`.

Every consumer (casting assign, downloads import, sub-type lookup, bgm-cue
scan, …) must work for both. These helpers take the drama root dir and return
the *actual* location — preferring whichever exists, falling back to the flat
root so first-time `create` still lands somewhere sane.
"""
from __future__ import annotations

import re
from pathlib import Path

EP_DIR_RE = re.compile(r"^ep\d+$", re.IGNORECASE)
SHOTS_DIR_NAME: str = "shots"
EPISODES_DIR_NAME: str = "episodes"

WORLD_STAGE: str = "2_世界观人设"
SCRIPT_STAGE: str = "4_剧本"
SHOTS_STAGE: str = "5_6_分镜与prompt"


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


def scenes_dir(drama_dir: Path) -> Path:
    return _first_existing_dir(
        drama_dir / "scenes", drama_dir / WORLD_STAGE / "scenes"
    )


def props_dir(drama_dir: Path) -> Path:
    """`props/` — flat root or `2_世界观人设/`. Resolved on its own rather than
    as `characters_dir(...).parent / "props"`: that derivation only found the
    staged props when a `characters/` sibling also existed, so a drama with
    props but no character folder silently fell back to the flat root."""
    return _first_existing_dir(
        drama_dir / "props", drama_dir / WORLD_STAGE / "props"
    )


def episodes_dir(drama_dir: Path) -> Path:
    """The episodes tree the render-side consumers walk (downloads import,
    episode compose, bgm-cue scan). The staged pipeline puts the shot/render
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
