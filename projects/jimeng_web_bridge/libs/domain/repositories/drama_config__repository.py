from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class StoredDramaConfig:
    data: Mapping[str, object]
    content_hash: str


class DramaConfigRepository(Protocol):
    def read(self, drama_root: str) -> StoredDramaConfig | None: ...

    def write(self, drama_root: str, data: Mapping[str, object], expected_hash: str | None) -> str: ...
