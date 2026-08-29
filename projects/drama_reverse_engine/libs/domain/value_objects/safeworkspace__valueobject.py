from __future__ import annotations

import posixpath
from dataclasses import dataclass
from pathlib import PurePath

from libs.domain.errors.workspace__error import PathEscapeError


@dataclass(frozen=True)
class SafeWorkspace:
    """Path sandbox: every artifact path is resolved through this single resolver
    (SEC-05). Pure path math — no filesystem access."""

    root: str

    def resolve(self, rel_path: str) -> str:
        return str(PurePath(self.root) / PurePath(self._safe_norm(rel_path)))

    def within(self, base_rel: str, rel_path: str) -> bool:
        """True iff rel_path normalizes to a location inside base_rel (both workspace-
        relative). Enforces sub-tree scope beyond the workspace sandbox (SEC edit guard)."""
        base = self._safe_norm(base_rel)
        target = self._safe_norm(rel_path)
        return target == base or target.startswith(base + "/")

    @staticmethod
    def _safe_norm(rel_path: str) -> str:
        norm = posixpath.normpath(PurePath(rel_path).as_posix())
        if norm.startswith("/") or norm == ".." or norm.startswith("../") or ":" in norm:
            raise PathEscapeError(f"path escapes workspace: {rel_path!r}")
        return norm
