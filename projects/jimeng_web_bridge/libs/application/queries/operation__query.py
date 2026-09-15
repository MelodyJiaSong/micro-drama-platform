from __future__ import annotations

from libs.application.dtos.operation__dto import OperationQdto
from libs.application.mappers.operation__mapper import OperationMapper
from libs.infrastructure.readers.operation__reader import OperationReader


class OperationQuery:
    def __init__(self, reader: OperationReader) -> None:
        self._reader = reader

    def get(self, operation_id: str) -> OperationQdto | None:
        dao = self._reader.get(operation_id)
        return None if dao is None else OperationMapper.to_qdto(dao)
