"""Repo file sandbox (spec v2 NFR 安全, FR-10).

Checks return a `PathVerdict` instead of raising because `common` may not
import the infrastructure error types; callers raise their own error.
Containment is decided component-wise on the resolved path, never by string
prefix, so `ai_videos_backup/` can never pass as `ai_videos/`.
"""
from __future__ import annotations

import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path

AI_VIDEOS_DIR_NAME: str = "ai_videos"

_RESERVED_STEM_RE = re.compile(
    r"^(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9¹²³]|LPT[1-9¹²³])$", re.IGNORECASE
)
_PERCENT_ESCAPE_RE = re.compile(r"%[0-9A-Fa-f]{2}")
_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_DEVICE_PREFIXES: tuple[str, ...] = ("\\\\?\\", "\\\\.\\", "\\??\\", "//?/", "//./")
_INVALID_CHARS: frozenset[str] = frozenset('<>"|?*\\')


@dataclass(frozen=True)
class PathVerdict:
    rel: str | None
    path: Path | None
    violation: str | None

    @property
    def ok(self) -> bool:
        return self.violation is None


def segment_violation(segment: str) -> str | None:
    if segment == "":
        return "empty_segment"
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in segment):
        return "control_char"
    if segment in (".", ".."):
        return "traversal"
    if ":" in segment:
        return "alternate_data_stream"
    if segment[-1] in ". ":
        return "trailing_dot_or_space"
    if any(char in _INVALID_CHARS for char in segment):
        return "invalid_char"
    if _PERCENT_ESCAPE_RE.search(segment):
        return "percent_escape"
    if _RESERVED_STEM_RE.match(segment.split(".", 1)[0].rstrip(" ")):
        return "reserved_name"
    return None


def lexical_violation(raw: str) -> str | None:
    if raw == "":
        return "empty"
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in raw):
        return "control_char"
    if raw.startswith(_DEVICE_PREFIXES):
        return "device_path"
    unified = raw.replace("\\", "/")
    if unified.startswith("//"):
        return "unc_path"
    if unified.startswith("/"):
        return "absolute_path"
    if _DRIVE_RE.match(unified):
        return "drive_path"
    for segment in unified.split("/"):
        violation = segment_violation(segment)
        if violation is not None:
            return violation
    return None


def is_reparse_point(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except ValueError:
        return True
    except OSError:
        return False
    if stat.S_ISLNK(info.st_mode):
        return True
    return bool(getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def is_within(path: Path, root: Path) -> bool:
    path_parts = [os.path.normcase(part) for part in path.parts]
    root_parts = [os.path.normcase(part) for part in root.parts]
    return path_parts[: len(root_parts)] == root_parts


class RepoSandbox:
    """Reads confined to `ai_videos/`; writes to `ai_videos/` plus `extra_write_roots` (`.data/`)."""

    def __init__(self, repo_root: Path, extra_write_roots: tuple[Path, ...] = ()) -> None:
        self._repo_root: Path = repo_root.resolve()
        self._read_root: Path = self._repo_root / AI_VIDEOS_DIR_NAME
        self._write_roots: tuple[Path, ...] = (
            self._read_root,
            *(root.resolve() for root in extra_write_roots),
        )

    @property
    def repo_root(self) -> Path:
        return self._repo_root

    @property
    def read_root(self) -> Path:
        return self._read_root

    def check_read(self, raw: str) -> PathVerdict:
        return self._check_relative(raw, (self._read_root,), allow_root=True)

    def check_write(self, raw: str) -> PathVerdict:
        return self._check_relative(raw, self._write_roots, allow_root=False)

    def check_write_path(self, path: Path) -> PathVerdict:
        # Segments are checked on the raw parts: `os.path.abspath` would silently strip trailing dots/spaces.
        if not path.is_absolute():
            return PathVerdict(None, None, "relative_path")
        for root in self._write_roots:
            if is_within(path, root) and len(path.parts) > len(root.parts):
                if is_reparse_point(root):
                    return PathVerdict(None, None, "reparse_point")
                return self._contain(root, list(path.parts[len(root.parts):]), (root,), allow_root=False)
        return PathVerdict(None, None, "outside_sandbox")

    def rel(self, path: Path) -> str | None:
        if not is_within(path, self._repo_root):
            return None
        return "/".join(path.parts[len(self._repo_root.parts):])

    def _check_relative(self, raw: str, roots: tuple[Path, ...], allow_root: bool) -> PathVerdict:
        violation = lexical_violation(raw)
        if violation is not None:
            return PathVerdict(None, None, violation)
        return self._contain(self._repo_root, raw.replace("\\", "/").split("/"), roots, allow_root)

    def _contain(
        self, base: Path, segments: list[str], roots: tuple[Path, ...], allow_root: bool
    ) -> PathVerdict:
        given = "/".join(segments)
        for segment in segments:
            violation = segment_violation(segment)
            if violation is not None:
                return PathVerdict(None, None, violation)
        current = base
        for segment in segments:
            current = current / segment
            if is_reparse_point(current):
                return PathVerdict(given, None, "reparse_point")
        resolved = current.resolve(strict=False)
        for root in roots:
            if is_within(resolved, root) and (allow_root or len(resolved.parts) > len(root.parts)):
                return PathVerdict(self.rel(resolved) or given, resolved, None)
        return PathVerdict(given, None, "outside_sandbox")
