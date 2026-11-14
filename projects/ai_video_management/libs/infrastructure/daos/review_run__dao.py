from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ReviewRunDao:
    runs: list[dict[str, Any]]
