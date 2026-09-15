from __future__ import annotations

from collections.abc import Sequence

from libs.application.errors.batch__error import BatchNotFoundError
from libs.application.mappers.batch__mapper import BatchItemMeta, BatchMapper, StoredBatch
from libs.common.clock import Clock
from libs.common.enums import BatchState
from libs.domain.entities.batch__entity import BatchEntity
from libs.infrastructure.daos.batch__dao import BatchDao
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.writers.batch__writer import BatchWriter


class SqliteBatchRepository:
    """Implements domain `BatchRepository`; `create` / `get_stored` add the per-item metadata only BatchCommand uses."""

    def __init__(self, reader: BatchReader, writer: BatchWriter, mapper: BatchMapper, clock: Clock) -> None:
        self._reader: BatchReader = reader
        self._writer: BatchWriter = writer
        self._mapper: BatchMapper = mapper
        self._clock: Clock = clock

    def get(self, batch_id: str) -> BatchEntity | None:
        stored: StoredBatch | None = self.get_stored(batch_id)
        return None if stored is None else stored.entity

    def get_stored(self, batch_id: str) -> StoredBatch | None:
        dao: BatchDao | None = self._reader.get(batch_id)
        return None if dao is None else self._mapper.to_stored(dao)

    def create(self, batch: BatchEntity, metas: Sequence[BatchItemMeta], idempotency_key: str | None) -> None:
        self._writer.save(self._mapper.to_dao(batch, metas, idempotency_key, self._clock.now()))

    def save(self, batch: BatchEntity) -> None:
        stored: StoredBatch | None = self.get_stored(batch.batch_id)
        if stored is None:
            raise BatchNotFoundError(f"批次 {batch.batch_id} 不存在")
        self._writer.save(self._mapper.to_dao(batch, stored.metas, stored.idempotency_key, self._clock.now()))

    def save_if_state(self, batch: BatchEntity, expected_state: BatchState) -> bool:
        stored: StoredBatch | None = self.get_stored(batch.batch_id)
        if stored is None or stored.entity.state is not expected_state:
            return False
        dao: BatchDao = self._mapper.to_dao(batch, stored.metas, stored.idempotency_key, self._clock.now())
        if expected_state is BatchState.AWAITING_CONFIRM:
            return self._writer.save_if_token_unused(dao, stored.entity.content_digest)
        self._writer.save(dao)
        return True
