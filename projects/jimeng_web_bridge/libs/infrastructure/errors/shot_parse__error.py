from __future__ import annotations


class MarkdownParseError(Exception):
    def __init__(self, code: str, source_rel: str) -> None:
        super().__init__(f"{code}: {source_rel}")
        self.code: str = code
        self.source_rel: str = source_rel


class ShotParseError(MarkdownParseError):
    """Codes: `not_utf8`, `prompt_heading_missing`, `prompt_fence_missing`, `prompt_fence_unterminated`."""
