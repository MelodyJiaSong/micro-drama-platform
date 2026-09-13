"""List a drama's episodes for the main-page production console.

Walks every shot tree the drama has (`drama_layout.shot_tree_roots` — an
`episodes/ep{NN}/` per episode, or the single one a single-piece drama keeps at
`shots/`) and reports each one's shot count, how many shots are already 定版-locked
(`shot{NN}.mp4` present), and whether the stitched master exists —
enough for the dashboard to render a per-episode 拼接成片 row with status.

Read-only: no copies, no mutation.
"""
from __future__ import annotations

from libs.common import drama_ref

import re
from dataclasses import dataclass
from pathlib import Path

from libs.common import drama_layout
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.subtitle__error import InvalidBatchScopeError

_SHOT_DIR_RE = re.compile(r"^shot\d+$", re.IGNORECASE)
_MP4_EXT = ".mp4"


@dataclass(frozen=True)
class EpisodeInfo:
    episode: str         # shot-tree slug: "ep04", or the drama name (single-piece)
    episode_rel: str     # repo-relative ep folder path (concat target)
    shots: int           # shot{NN} subfolders
    locked: int          # shots with a 定版 shot{NN}.mp4
    has_master: bool     # stitched {slug}.mp4 exists


@dataclass(frozen=True)
class DramaEpisodesResult:
    drama_rel: str
    episodes: tuple[EpisodeInfo, ...]

    def to_payload(self) -> dict[str, object]:
        return {
            "drama": self.drama_rel,
            "episodes": [
                {
                    "episode": e.episode,
                    "episode_rel": e.episode_rel,
                    "shots": e.shots,
                    "locked": e.locked,
                    "has_master": e.has_master,
                }
                for e in self.episodes
            ],
        }


class DramaEpisodesReader:
    def __init__(self, exposed: ExposedTree, resolver: SafeResolver) -> None:
        self._exposed = exposed
        self._resolver = resolver

    def list(self, rel: str) -> DramaEpisodesResult:
        drama_root = self._drama_root(rel)
        episodes: list[EpisodeInfo] = []
        for ep_dir in drama_layout.shot_tree_roots(drama_root):
            slug = drama_layout.shot_tree_slug(ep_dir, drama_root)
            shots = self._shot_dirs(ep_dir / drama_layout.SHOTS_DIR_NAME)
            locked = sum(1 for s in shots if (s / f"{s.name}{_MP4_EXT}").is_file())
            master = ep_dir / f"{slug}{_MP4_EXT}"
            episodes.append(
                EpisodeInfo(
                    slug,
                    self._rel(ep_dir),
                    len(shots),
                    locked,
                    master.is_file() and not master.is_symlink(),
                )
            )
        return DramaEpisodesResult(self._rel(drama_root), tuple(episodes))

    def _drama_root(self, rel: str) -> Path:
        if not isinstance(rel, str) or rel == "":
            raise InvalidBatchScopeError("path is empty")
        if not self._exposed.is_inside(rel):
            raise InvalidBatchScopeError("path outside sandbox")
        parts = rel.split("/")
        depth = drama_ref.drama_depth(self._exposed.root, parts)
        if depth is None:
            raise InvalidBatchScopeError("path is not under ai_videos/{drama}/")
        resolved = self._resolver.resolve("/".join(parts[:depth]))
        if resolved is None:
            raise InvalidBatchScopeError("path failed sandbox resolution")
        if resolved.is_symlink():
            raise InvalidBatchScopeError("symlink is not allowed")
        if not resolved.is_dir():
            raise InvalidBatchScopeError("drama folder does not exist")
        return resolved

    @staticmethod
    def _shot_dirs(shots_dir: Path) -> list[Path]:
        if not shots_dir.is_dir():
            return []
        try:
            entries = sorted(shots_dir.iterdir(), key=lambda p: p.name)
        except OSError:
            return []
        return [
            e for e in entries
            if e.is_dir() and not e.is_symlink() and _SHOT_DIR_RE.match(e.name)
        ]

    def _rel(self, p: Path) -> str:
        try:
            return p.resolve().relative_to(self._resolver.root).as_posix()
        except (OSError, ValueError):
            return p.as_posix()
