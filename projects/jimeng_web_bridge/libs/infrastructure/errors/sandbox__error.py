from __future__ import annotations


class SandboxError(Exception):
    """A path failed the repo sandbox. The message carries only the repo-relative form."""

    def __init__(self, reason: str, rel: str | None) -> None:
        super().__init__(f"path rejected ({reason}): {rel if rel is not None else '<input>'}")
        self.reason: str = reason
        self.rel: str | None = rel


class LinkRejectedError(SandboxError):
    """A `*.link.json` is malformed, chained, escapes `ai_videos/`, or targets a non-file."""
