from __future__ import annotations

import re
from decimal import ROUND_HALF_UP, Decimal

RATIO_FIELD: str = "比例"
DURATION_FIELD: str = "时长"

_FIELD_RE = re.compile(r"^[\s`*\-]*([A-Za-z_一-鿿]{1,12})[`*]*\s*[:：](.*)$")
_FIELD_SEPARATOR_RE = re.compile(r"[｜|]")
_RATIO_RE = re.compile(r"(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)")
_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


class PromptFieldReader:
    """`名称: 值` fields at a line start or after a `｜` separator (`比例: 9:16 ｜ 时长: 9秒`)."""

    def fields(self, content: str) -> tuple[tuple[str, str], ...]:
        found: list[tuple[str, str]] = []
        for line in content.split("\n"):
            for part in _FIELD_SEPARATOR_RE.split(line):
                match = _FIELD_RE.match(part)
                if match is not None:
                    found.append((match.group(1), match.group(2).strip().strip("`").strip()))
        return tuple(found)

    def names(self, fields: tuple[tuple[str, str], ...]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(f"{name}:" for name, _ in fields))

    def ratio(self, fields: tuple[tuple[str, str], ...]) -> tuple[str | None, str | None]:
        raw = _first_value(fields, RATIO_FIELD)
        if raw is None:
            return None, None
        # Decimal-aware on purpose: a plain `\d+:\d+` would read `2.35:1` as `35:1`.
        match = _RATIO_RE.search(raw)
        return (None if match is None else f"{match.group(1)}:{match.group(2)}"), raw

    def duration(self, fields: tuple[tuple[str, str], ...]) -> tuple[int | None, str | None]:
        raw = _first_value(fields, DURATION_FIELD)
        if raw is None:
            return None, None
        match = _NUMBER_RE.search(raw)
        if match is None:
            return None, raw
        return int(Decimal(match.group(0)).quantize(Decimal(1), rounding=ROUND_HALF_UP)), raw


def _first_value(fields: tuple[tuple[str, str], ...], name: str) -> str | None:
    return next((value for field_name, value in fields if field_name == name), None)
