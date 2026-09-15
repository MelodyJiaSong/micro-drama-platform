"""Pure fill planning and editor verification (FR-31): split a prompt at its `=>@` markers, build the expected
editor snapshot, and compare it with what the page's editor actually holds."""
from __future__ import annotations

import re
from collections.abc import Sequence

from libs.infrastructure.daos.jimeng_page__dao import EditorSnapshotDao, FillSegmentDao, MentionMarkerDao
from libs.infrastructure.errors.jimeng_browser__error import FillPlanError

MENTION_MARKER: str = "=>@"
PROMPT_PREFIX_CHARS: int = 24
_INVISIBLE = re.compile("[" + "".join(chr(code) for code in (0x200B, 0x200C, 0x200D, 0xFEFF)) + "]")
_NEWLINE_RUNS = re.compile(r"\n{2,}")


def build_fill_segments(prompt: str, markers: Sequence[MentionMarkerDao]) -> tuple[FillSegmentDao, ...]:
    """Text segments are typed as-is; at each reference's `@` a mention chip for `marker.mention` is picked.

    Markers are consumed in order, each after the previous one; any other `@` stays literal text.
    """
    segments: list[FillSegmentDao] = []
    cursor = 0
    for marker in markers:
        token = f"{marker.name}({marker.label}){MENTION_MARKER}" if marker.label else f"{marker.name}{MENTION_MARKER}"
        index = prompt.find(token, cursor)
        if index < 0:
            raise FillPlanError(f"prompt 里在第 {cursor} 个字符之后找不到参考项标记 {token}")
        at = index + len(token) - 1
        segments.append(FillSegmentDao(prompt[cursor:at]))
        segments.append(FillSegmentDao("", mention=marker.mention))
        cursor = at + 1
    segments.append(FillSegmentDao(prompt[cursor:]))
    return tuple(segment for segment in segments if segment.mention is not None or segment.text)


def normalize_editor_text(text: str) -> str:
    """Whitespace normalisation shared by both sides of the comparison.

    CR/CRLF → LF, NBSP → space, zero-width characters removed, blank-line runs collapsed to one line break
    (contenteditable renders an empty paragraph as a bogus `<br>`), outer line breaks and trailing spaces
    stripped. Runs of spaces and U+3000 are kept: the prompt is sent byte-for-byte.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace(chr(0xA0), " ")
    text = _NEWLINE_RUNS.sub("\n", _INVISIBLE.sub("", text))
    return text.strip("\n").rstrip(" ")


def expected_snapshot(segments: Sequence[FillSegmentDao]) -> EditorSnapshotDao:
    text = "".join(segment.mention if segment.mention is not None else segment.text for segment in segments)
    return EditorSnapshotDao(
        text=normalize_editor_text(text),
        mentions=tuple(segment.mention for segment in segments if segment.mention is not None),
    )


def compare_snapshot(expected: EditorSnapshotDao, actual: EditorSnapshotDao) -> str | None:
    problems: list[str] = []
    actual_text = normalize_editor_text(actual.text)
    if actual_text != expected.text:
        index = next(
            (i for i, (a, b) in enumerate(zip(expected.text, actual_text)) if a != b),
            min(len(expected.text), len(actual_text)),
        )
        problems.append(
            f"纯文本在第 {index} 个字符处不一致：期望 {expected.text[index:index + 24]!r}，编辑器 {actual_text[index:index + 24]!r}"
            f"（期望 {len(expected.text)} 字，实际 {len(actual_text)} 字）"
        )
    if tuple(actual.mentions) != tuple(expected.mentions):
        problems.append(f"mention 序列不一致：期望 {list(expected.mentions)}，编辑器 {list(actual.mentions)}")
    return "；".join(problems) or None


def prompt_prefix(expected: EditorSnapshotDao, chars: int = PROMPT_PREFIX_CHARS) -> str:
    return re.sub(r"\s+", " ", expected.text).strip()[:chars]
