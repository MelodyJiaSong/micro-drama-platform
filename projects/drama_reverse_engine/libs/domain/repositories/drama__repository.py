from __future__ import annotations

from typing import Protocol

from libs.common.types import DramaId
from libs.domain.entities.drama__entity import DramaEntity


class DramaRepository(Protocol):
    def get(self, drama_id: DramaId) -> DramaEntity | None: ...

    def save(self, drama: DramaEntity) -> None: ...

    def list_all(self) -> list[DramaEntity]: ...
