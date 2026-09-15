from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from libs.application.dtos.batch__dto import BatchPrecheckCdto, EntityCreateItemInput
from libs.application.dtos.entity__dto import EntitySnapshotEntryCdto
from libs.application.mappers.entity__mapper import EntityMapper
from libs.application.queries.drama_config__query import DramaConfigQuery
from libs.common.clock import Clock, iso
from libs.common.paths import segment_violation
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.writers.store_record__writer import EntitySnapshotWriter


class BatchPrecheckPort(Protocol):
    """The slice of `BatchCommand` this command needs; creation only ever enters through a batch (FR-49)."""

    def precheck(self, items: Sequence[EntityCreateItemInput], idempotency_key: str | None) -> BatchPrecheckCdto: ...


class EntityCommand:
    def __init__(
        self,
        configs: DramaConfigQuery,
        batches: BatchPrecheckPort,
        snapshot_writer: EntitySnapshotWriter,
        clock: Clock,
        mapper: EntityMapper,
    ) -> None:
        self._configs = configs
        self._batches = batches
        self._snapshot_writer = snapshot_writer
        self._clock = clock
        self._mapper = mapper

    def request_create(self, drama_rel: str, character_dir: str, description: str | None = None) -> BatchPrecheckCdto:
        """`character_dir` is the card directory name (`c2_獾`). Nothing is created here — the batch awaits UI confirmation."""
        root = self._configs.drama_root(drama_rel)
        if "\\" in character_dir or "/" in character_dir:
            raise SandboxError("not_a_directory_name", None)
        violation = segment_violation(character_dir)
        if violation is not None:
            raise SandboxError(violation, None)
        item = EntityCreateItemInput(drama_rel=root, character_dir=character_dir, description=description)
        return self._batches.precheck([item], None)

    def record_snapshot(self, entries: Sequence[EntitySnapshotEntryCdto]) -> None:
        """Replaces the whole snapshot (FR-47); called by the entity-sync operation with what the page reported."""
        synced_at = iso(self._clock.now())
        self._snapshot_writer.replace_all(self._mapper.snapshot_records(entries, synced_at), synced_at=synced_at)
