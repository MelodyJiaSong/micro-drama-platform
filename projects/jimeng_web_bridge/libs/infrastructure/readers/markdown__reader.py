from __future__ import annotations

import re

from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.markdown__dao import (
    MarkdownDocumentDao,
    MarkdownFenceDao,
    MarkdownHeadingDao,
)
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.errors.shot_parse__error import MarkdownParseError

TEXT_FENCE_INFO: str = "text"
MARKDOWN_SUFFIX: str = ".md"
MAX_MARKDOWN_BYTES: int = 2 * 1024 * 1024
_FENCE_MARK: str = "```"
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


class MarkdownReader:
    def load(self, sandbox: RepoSandbox, rel: str) -> tuple[str, bytes]:
        """Sandboxed read of a shot/card md: suffix, file type and size are checked before any byte is loaded."""
        verdict = sandbox.check_read(rel)
        if verdict.path is None or verdict.rel is None:
            raise SandboxError(verdict.violation or "rejected", verdict.rel)
        if not verdict.rel.casefold().endswith(MARKDOWN_SUFFIX):
            raise SandboxError("unsupported_type", verdict.rel)
        try:
            if not verdict.path.is_file():
                raise SandboxError("not_a_file", verdict.rel)
            if verdict.path.stat().st_size > MAX_MARKDOWN_BYTES:
                raise SandboxError("too_large", verdict.rel)
            return verdict.rel, verdict.path.read_bytes()
        except OSError as error:
            raise SandboxError("unreadable", verdict.rel) from error

    def decode(self, data: bytes, source_rel: str) -> str:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise MarkdownParseError("not_utf8", source_rel) from error
        return text.removeprefix("﻿").replace("\r\n", "\n").replace("\r", "\n")

    def parse(self, text: str) -> MarkdownDocumentDao:
        lines = tuple(text.split("\n"))
        fences: list[MarkdownFenceDao] = []
        headings: list[MarkdownHeadingDao] = []
        index = 0
        while index < len(lines):
            stripped = lines[index].strip()
            if stripped.startswith(_FENCE_MARK):
                close = next(
                    (j for j in range(index + 1, len(lines)) if lines[j].strip() == _FENCE_MARK),
                    None,
                )
                end = len(lines) if close is None else close
                content = "\n".join(lines[index + 1 : end]).rstrip("\n")
                fences.append(MarkdownFenceDao(index, close, stripped[len(_FENCE_MARK):].strip(), content))
                index = end + 1
                continue
            match = _HEADING_RE.match(lines[index])
            if match is not None:
                headings.append(MarkdownHeadingDao(index, len(match.group(1)), match.group(2)))
            index += 1
        return MarkdownDocumentDao(lines, tuple(fences), tuple(headings))
