from typing import Protocol

from libs.common.enums import BatchState
from libs.domain.entities.batch__entity import BatchEntity


class BatchRepository(Protocol):
    def get(self, batch_id: str) -> BatchEntity | None: ...

    def save(self, batch: BatchEntity) -> None: ...

    def save_if_state(self, batch: BatchEntity, expected_state: BatchState) -> bool: ...
