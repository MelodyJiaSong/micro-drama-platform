from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProbeResultCdto:
    name: str
    status: str  # ok | failed | skipped
    detail: str
    data: dict[str, str] = field(default_factory=dict)
