from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequestLogQdto:
    logs: list[dict[str, Any]]
    entries: list[dict[str, Any]]
    total: int

    def to_payload(self) -> dict[str, Any]:
        return {"logs": self.logs, "entries": self.entries, "total": self.total}
