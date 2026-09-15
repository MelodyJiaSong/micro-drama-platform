from typing import Protocol

from libs.domain.entities.operation__entity import OperationEntity


class OperationRepository(Protocol):
    def get(self, operation_id: str) -> OperationEntity | None: ...

    def save(self, operation: OperationEntity) -> None: ...

    def list_unfinished(self) -> list[OperationEntity]: ...
