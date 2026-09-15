from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigFileDao:
    location: str
    exists: bool
    data: dict[str, object]
    sha256: str | None
    raw_text: str | None
