from __future__ import annotations

from datetime import timedelta

from libs.application.dtos.entity__dto import ReconcileQdto
from libs.application.mappers.entity__mapper import EntityMapper
from libs.application.queries.drama_config__query import DramaConfigQuery
from libs.common.clock import Clock
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.store_record__reader import EntitySnapshotReader


class EntityQuery:
    def __init__(
        self,
        configs: DramaConfigQuery,
        snapshot_reader: EntitySnapshotReader,
        global_reader: GlobalConfigReader,
        clock: Clock,
        mapper: EntityMapper,
        test_mode: bool,
    ) -> None:
        self._configs = configs
        self._snapshots = snapshot_reader
        self._global = global_reader
        self._clock = clock
        self._mapper = mapper
        self._test_mode = test_mode

    def reconcile(self, drama_rel: str | None = None) -> ReconcileQdto:
        """FR-48. `drama_rel` narrows mapped/missing rows; `unmapped_on_platform` is always computed over every drama."""
        target = None if drama_rel is None else self._configs.drama_root(drama_rel)
        stale_h = GlobalConfig.from_dict(self._global.read().data, self._test_mode).entities.snapshot_stale_h
        records = self._snapshots.all()
        facts = self._mapper.snapshot_facts(self._snapshots.last_synced_at(), (record.name for record in records))
        return self._mapper.reconcile(
            target, self._configs.all_card_entities(), records, facts, self._clock.now(), timedelta(hours=stale_h)
        )
