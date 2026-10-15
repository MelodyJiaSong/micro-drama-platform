from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GlobalWorkflowQdto:
    groups: list[dict[str, str]]
    sources: list[dict[str, Any]]
    categories: list[dict[str, str]] = field(default_factory=list)
    formats: list[dict[str, str]] = field(default_factory=list)
