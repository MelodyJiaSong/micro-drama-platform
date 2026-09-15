from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownFenceDao:
    open_line: int
    close_line: int | None
    info: str
    content: str


@dataclass(frozen=True)
class MarkdownHeadingDao:
    line: int
    level: int
    text: str


@dataclass(frozen=True)
class MarkdownDocumentDao:
    lines: tuple[str, ...]
    fences: tuple[MarkdownFenceDao, ...]
    headings: tuple[MarkdownHeadingDao, ...]
