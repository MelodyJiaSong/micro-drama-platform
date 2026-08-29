from __future__ import annotations

import re
from dataclasses import dataclass

from libs.common.constants import PROMPT_CHAR_LIMIT

_WHITESPACE = re.compile(r"\s+")


def visible_char_count(block: str) -> int:
    """全字符 count per repo contract: trim the block, drop ALL whitespace, count
    UTF-16 code units (matches the PowerShell reference `.Trim() -replace '\\s',''`
    `.Length` — astral-plane chars like emoji count as 2)."""
    stripped = _WHITESPACE.sub("", block.strip())
    return sum(2 if ord(ch) > 0xFFFF else 1 for ch in stripped)


@dataclass(frozen=True)
class PromptBudget:
    count: int
    limit: int

    @property
    def ok(self) -> bool:
        return self.count <= self.limit


def check_prompt_budget(block: str, limit: int = PROMPT_CHAR_LIMIT) -> PromptBudget:
    return PromptBudget(count=visible_char_count(block), limit=limit)
