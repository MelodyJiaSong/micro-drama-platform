"""Drama-wide 定版: lock every episode's takes in one pass.

The per-episode `EpisodeTakesSelector` copies each shot's newest `renders/` mp4
to a stable `shot{NN}.mp4`. This walks every shot tree of a drama
(`drama_layout.shot_tree_roots` — an `episodes/ep{NN}/` per episode, or the
single one a single-piece drama keeps at `shots/`) and delegates to that same
selector per tree, so the drama-wide lock can NEVER drift from the single-episode one.

A single episode failing (no shots, no render mp4) is reported, not fatal — the
other episodes still lock. The whole call only raises on a bad drama path.
"""
from __future__ import annotations

from libs.common import drama_ref

from dataclasses import dataclass
from pathlib import Path

from libs.common import drama_layout
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.episode__error import EpisodeDomainError
from libs.domain.errors.subtitle__error import InvalidBatchScopeError
from libs.infrastructure.writers.episode_takes__writer import (
    EpisodeTakesSelector,
    SelectTakesResult,
)

@dataclass(frozen=True)
class EpisodeTakesOutcome:
    episode: str                 # ep folder name, e.g. "ep04"
    episode_rel: str             # repo-relative ep folder path
    ok: bool
    selected: int                # shots locked (ok only)
    skipped: int                 # shots skipped for lack of a render (ok only)
    reason: str | None = None    # failure kind (ok=False only)


@dataclass(frozen=True)
class DramaTakesResult:
    drama_rel: str
    outcomes: tuple[EpisodeTakesOutcome, ...]


class DramaTakesSelector:
    def __init__(
        self,
        exposed: ExposedTree,
        resolver: SafeResolver,
        episode_selector: EpisodeTakesSelector,
    ) -> None:
        self._exposed = exposed
        self._resolver = resolver
        self._episode_selector = episode_selector

    def select_all(self, rel: str) -> DramaTakesResult:
        drama_root = self._drama_root(rel)
        outcomes: list[EpisodeTakesOutcome] = []
        for ep_dir in drama_layout.shot_tree_roots(drama_root):
            ep_rel = self._rel(ep_dir)
            try:
                result: SelectTakesResult = self._episode_selector.select(ep_rel)
            except EpisodeDomainError as exc:
                outcomes.append(
                    EpisodeTakesOutcome(
                        drama_layout.shot_tree_slug(ep_dir, drama_root),
                        ep_rel, False, 0, 0, type(exc).__name__,
                    )
                )
                continue
            outcomes.append(
                EpisodeTakesOutcome(
                    drama_layout.shot_tree_slug(ep_dir, drama_root),
                    ep_rel, True, len(result.selected), len(result.skipped),
                )
            )
        return DramaTakesResult(self._rel(drama_root), tuple(outcomes))

    def _drama_root(self, rel: str) -> Path:
        if not isinstance(rel, str) or rel == "":
            raise InvalidBatchScopeError("path is empty")
        if not self._exposed.is_inside(rel):
            raise InvalidBatchScopeError("path outside sandbox")
        parts = rel.split("/")
        depth = drama_ref.drama_depth(self._resolver.root, parts)
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
    def _episode_dirs(drama_root: Path) -> list[Path]:
        episodes_dir = drama_layout.episodes_dir(drama_root)
        if not episodes_dir.is_dir():
            return []
        try:
            entries = sorted(episodes_dir.iterdir(), key=lambda p: p.name)
        except OSError:
            return []
        return [
            e for e in entries
            if e.is_dir() and not e.is_symlink() and _EP_DIR_RE.match(e.name)
        ]

    def _rel(self, p: Path) -> str:
        try:
            return p.resolve().relative_to(self._resolver.root).as_posix()
        except (OSError, ValueError):
            return p.as_posix()
