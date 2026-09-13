"""Errors raised while muxing an uploaded video with an uploaded BGM track."""
from __future__ import annotations


class MuxError(Exception):
    """Base for BGM-mux failures. `kind` maps to the HTTP status in the route."""

    def __init__(self, kind: str, message: str) -> None:
        super().__init__(message)
        self.kind = kind


class UnsupportedMediaError(MuxError):
    """Upload rejected at the boundary: bad extension or out-of-range option."""

    def __init__(self, message: str) -> None:
        super().__init__("unsupported_media", message)


class MuxFailedError(MuxError):
    """ffmpeg ran but produced no output."""

    def __init__(self, message: str) -> None:
        super().__init__("mux_failed", message)
