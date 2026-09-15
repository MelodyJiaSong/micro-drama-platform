from __future__ import annotations

import re

from libs.infrastructure.daos.shot_prompt__dao import (
    LegacyReferenceDao,
    ReferenceItemDao,
    ReferenceLineDao,
)

MENTION_MARKER: str = "=>@"
_ARROW_RE = re.compile(r"=>(?:@(\d*))?")
_LINE_PREFIXES: tuple[str, ...] = ("参考:", "参考：")
_EDGE_CHARS: str = " \t`,，、;；"
_ITEM_BREAK_CHARS: str = "`,，、;；"
_NONE_DECLARATIONS: frozenset[str] = frozenset({"无", "none"})


class ReferenceLineReader:
    """Splits `参考:` lines on `=>` boundaries (spec v2 FR-8); never yields a silent empty result."""

    def parse(self, content: str) -> ReferenceLineDao:
        lines = [line.strip() for line in content.split("\n") if line.strip().startswith(_LINE_PREFIXES)]
        items: list[ReferenceItemDao] = []
        legacy: list[LegacyReferenceDao] = []
        unrecognized: list[str] = []
        declares_none = False
        for line in lines:
            body = line[len(_LINE_PREFIXES[0]):]
            if body.strip(_EDGE_CHARS).lower() in _NONE_DECLARATIONS:
                declares_none = True
                continue
            before = len(items) + len(legacy) + len(unrecognized)
            cursor = 0
            for arrow in _ARROW_RE.finditer(body):
                _classify(body[cursor : arrow.start()], arrow, items, legacy, unrecognized)
                cursor = arrow.end()
            tail = body[cursor:].strip(_EDGE_CHARS)
            if tail:
                unrecognized.append(tail)
            if len(items) + len(legacy) + len(unrecognized) == before:
                unrecognized.append(line)
        return ReferenceLineDao(
            line_count=len(lines),
            items=tuple(items),
            legacy=tuple(legacy),
            unrecognized=tuple(unrecognized),
            marker_count=content.count(MENTION_MARKER),
            declares_none=declares_none,
        )


def _classify(
    segment: str,
    arrow: re.Match[str],
    items: list[ReferenceItemDao],
    legacy: list[LegacyReferenceDao],
    unrecognized: list[str],
) -> None:
    text = segment.rstrip(" \t`")
    label: str | None = None
    head = text
    if text.endswith(")"):
        opening = _matching_open_paren(text)
        if opening is not None:
            label = text[opening + 1 : -1]
            head = text[:opening]
    cut = max(head.rfind(char) for char in _ITEM_BREAK_CHARS)
    junk = head[: cut + 1].strip(_EDGE_CHARS)
    if junk:
        unrecognized.append(junk)
    name_part = head[cut + 1 :]
    name = name_part.strip()
    token = text[cut + 1 + len(name_part) - len(name_part.lstrip()) :] + arrow.group(0)
    if not name or label == "":
        unrecognized.append(token)
        return
    kinds = tuple(
        kind
        for kind, applies in (
            ("no_at", arrow.group(1) is None),
            ("slot_number", bool(arrow.group(1))),
            ("no_paren", label is None),
        )
        if applies
    )
    if kinds:
        legacy.append(LegacyReferenceDao(kinds, token))
    elif label is not None:
        items.append(ReferenceItemDao(name, label, token))


def _matching_open_paren(text: str) -> int | None:
    depth = 0
    for index in range(len(text) - 1, -1, -1):
        if text[index] == ")":
            depth += 1
        elif text[index] == "(":
            depth -= 1
            if depth == 0:
                return index
    return None
