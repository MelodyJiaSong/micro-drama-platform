from __future__ import annotations

from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.markdown__dao import MarkdownDocumentDao, MarkdownFenceDao
from libs.infrastructure.daos.shot_prompt__dao import ShotPromptDao
from libs.infrastructure.errors.shot_parse__error import MarkdownParseError, ShotParseError
from libs.infrastructure.readers.markdown__reader import TEXT_FENCE_INFO, MarkdownReader
from libs.infrastructure.readers.prompt_field__reader import PromptFieldReader
from libs.infrastructure.readers.reference_line__reader import ReferenceLineReader

PROMPT_HEADING_PREFIX: str = "视频 prompt"
NEGATIVE_MARK: str = "反向提示词"


class ShotPromptReader:
    def __init__(self, sandbox: RepoSandbox) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._markdown: MarkdownReader = MarkdownReader()
        self._fields: PromptFieldReader = PromptFieldReader()
        self._references: ReferenceLineReader = ReferenceLineReader()

    def read(self, rel: str) -> ShotPromptDao:
        source_rel, data = self._markdown.load(self._sandbox, rel)
        return self.parse_bytes(data, source_rel)

    def parse_bytes(self, data: bytes, source_rel: str) -> ShotPromptDao:
        try:
            text = self._markdown.decode(data, source_rel)
        except MarkdownParseError as error:
            raise ShotParseError(error.code, source_rel) from error
        document = self._markdown.parse(text)
        fence, close_line = _prompt_fence(document, source_rel)
        fields = self._fields.fields(fence.content)
        ratio, ratio_raw = self._fields.ratio(fields)
        duration_s, duration_raw = self._fields.duration(fields)
        return ShotPromptDao(
            source_rel=source_rel,
            prompt=fence.content,
            negative_prompt=_negative_prompt(document, close_line + 1),
            ratio=ratio,
            ratio_raw=ratio_raw,
            duration_s=duration_s,
            duration_raw=duration_raw,
            references=self._references.parse(fence.content),
        )


def _prompt_fence(document: MarkdownDocumentDao, source_rel: str) -> tuple[MarkdownFenceDao, int]:
    heading = next(
        (h for h in document.headings if h.level == 2 and h.text.startswith(PROMPT_HEADING_PREFIX)),
        None,
    )
    if heading is None:
        raise ShotParseError("prompt_heading_missing", source_rel)
    section_end = next(
        (h.line for h in document.headings if h.line > heading.line and h.level <= 2),
        len(document.lines),
    )
    fence = next(
        (f for f in document.fences if heading.line < f.open_line < section_end and f.info == TEXT_FENCE_INFO),
        None,
    )
    if fence is None:
        raise ShotParseError("prompt_fence_missing", source_rel)
    if fence.close_line is None:
        raise ShotParseError("prompt_fence_unterminated", source_rel)
    return fence, fence.close_line


def _negative_prompt(document: MarkdownDocumentDao, start: int) -> str | None:
    # `## 反向提示词` is itself a level-2 heading, so only headings without the mark end the search.
    end = min(
        (h.line for h in document.headings if h.line >= start and h.level <= 2 and NEGATIVE_MARK not in h.text),
        default=len(document.lines),
    )
    fence = next(
        (f for f in document.fences if start <= f.open_line < end and f.info == TEXT_FENCE_INFO),
        None,
    )
    if fence is None:
        return None
    preceding = next(
        (document.lines[i].strip() for i in range(fence.open_line - 1, -1, -1) if document.lines[i].strip()),
        "",
    )
    if NEGATIVE_MARK in preceding and preceding.startswith(("#", ">")):
        return fence.content
    return None
