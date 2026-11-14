from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ReviewRunQdto:
    runs: list[dict[str, Any]]

    def to_payload(self) -> dict[str, Any]:
        return {"runs": self.runs}
