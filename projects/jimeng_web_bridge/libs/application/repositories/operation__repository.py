from __future__ import annotations

from libs.application.mappers.operation__mapper import OperationMapper
from libs.common.enums import OperationState
from libs.domain.entities.operation__entity import OperationEntity
from libs.infrastructure.readers.operation__reader import OperationReader
from libs.infrastructure.writers.operation__writer import OperationWriter

_UNFINISHED: tuple[str, ...] = (OperationState.PENDING.value, OperationState.RUNNING.value)


class SqliteOperationRepository:
    """`OperationRepository` over the SQLite store (spec v2 §8 divergence 6: application-layer adapter)."""

    def __init__(self, reader: OperationReader, writer: OperationWriter) -> None:
        self._reader = reader
        self._writer = writer

    def get(self, operation_id: str) -> OperationEntity | None:
        dao = self._reader.get(operation_id)
        return None if dao is None else OperationMapper.to_entity(dao)

    def save(self, operation: OperationEntity) -> None:
        self._writer.save(OperationMapper.to_dao(operation))

    def list_unfinished(self) -> list[OperationEntity]:
        return [OperationMapper.to_entity(dao) for dao in self._reader.in_states(_UNFINISHED)]
