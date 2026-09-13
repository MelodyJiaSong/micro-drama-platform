"""DramaPath value object — `ai_videos/{drama}` or `ai_videos/{series}/{drama}`.

Shape validation only: this layer has no filesystem access, so it cannot tell a
series folder from a flat drama (that is `libs.common.drama_ref`'s job). It
accepts 2 or 3 segments and exposes the last one as `drama_name`; whoever
resolves the path against disk rejects a series folder handed in as a drama.
"""
from __future__ import annotations

from dataclasses import dataclass

from libs.domain.errors.casting__error import InvalidDramaPathError


@dataclass(frozen=True)
class DramaPath:
    rel: str

    def __post_init__(self) -> None:
        if not isinstance(self.rel, str) or self.rel == "":
            raise InvalidDramaPathError("path is empty")
        normalized = self.rel.rstrip("/")
        parts = normalized.split("/")
        if not (2 <= len(parts) <= 3) or parts[0] != "ai_videos" or any(p == "" for p in parts[1:]):
            raise InvalidDramaPathError(
                "path must be 'ai_videos/{drama}' or 'ai_videos/{series}/{drama}'"
            )
        object.__setattr__(self, "rel", normalized)

    @property
    def drama_name(self) -> str:
        """Leaf folder name — the drama itself, series prefix stripped."""
        return self.rel.rsplit("/", 1)[1]

    @property
    def series_name(self) -> str | None:
        parts = self.rel.split("/")
        return parts[1] if len(parts) == 3 else None
