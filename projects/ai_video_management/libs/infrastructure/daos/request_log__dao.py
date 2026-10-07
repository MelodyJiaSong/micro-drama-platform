from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequestLogDao:
    logs: list[dict[str, Any]]
    entries: list[dict[str, Any]]
    total: int
