"""Error raised by the research reader when the research surface is absent or malformed."""
from __future__ import annotations


class ResearchError(Exception):
    def __init__(self, kind: str, message: str) -> None:
        super().__init__(message)
        self.kind = kind
