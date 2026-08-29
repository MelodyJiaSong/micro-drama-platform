from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LockedDescriptor:
    """锁定中文描述符 — must be re-pasted byte-identically in every shot prompt
    that names the character."""

    character_name: str
    text: str

    def matches(self, candidate: str) -> bool:
        return self.text == candidate
