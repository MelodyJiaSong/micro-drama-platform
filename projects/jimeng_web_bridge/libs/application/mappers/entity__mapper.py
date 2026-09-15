from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from datetime import datetime, timedelta

from libs.application.dtos.drama_config__dto import DramaEntitiesQdto
from libs.application.dtos.entity__dto import (
    DramaConfigIssueQdto,
    EntitySnapshotEntryCdto,
    EntityUsageQdto,
    ReconcileQdto,
    ReconcileRowQdto,
    UnnamedCardQdto,
)
from libs.common.clock import iso
from libs.common.enums import EntityReconcileState
from libs.domain.value_objects.precheck_context__valueobject import EntitySnapshotFacts
from libs.infrastructure.daos.store_record__dao import EntitySnapshotDao

_STATE_ORDER: dict[str, int] = {
    EntityReconcileState.MAPPED.value: 0,
    EntityReconcileState.MISSING_ON_PLATFORM.value: 1,
    EntityReconcileState.UNMAPPED_ON_PLATFORM.value: 2,
}


class EntityMapper:
    def snapshot_records(self, entries: Sequence[EntitySnapshotEntryCdto], synced_at: str) -> list[EntitySnapshotDao]:
        seen: set[str] = set()
        records: list[EntitySnapshotDao] = []
        for entry in entries:
            if not entry.name or entry.name in seen:
                continue
            seen.add(entry.name)
            records.append(EntitySnapshotDao(entry.name, entry.thumbnail_url, entry.modified_at, synced_at))
        return records

    def snapshot_facts(self, synced_at: str | None, names: Iterable[str]) -> EntitySnapshotFacts:
        return EntitySnapshotFacts(
            names=frozenset(names), synced_at=None if synced_at is None else datetime.fromisoformat(synced_at)
        )

    def reconcile(
        self,
        drama_rel: str | None,
        dramas: Sequence[DramaEntitiesQdto],
        records: Sequence[EntitySnapshotDao],
        facts: EntitySnapshotFacts,
        now: datetime,
        stale_after: timedelta,
    ) -> ReconcileQdto:
        usages: dict[str, list[EntityUsageQdto]] = {}
        unnamed: list[UnnamedCardQdto] = []
        issues: list[DramaConfigIssueQdto] = []
        for drama in dramas:
            in_scope = drama_rel is None or drama.drama_rel == drama_rel
            if in_scope and drama.config_error is not None:
                issues.append(DramaConfigIssueQdto(drama_rel=drama.drama_rel, error=drama.config_error))
            for card in drama.entities:
                if card.entity_name is None:
                    if in_scope:
                        unnamed.append(
                            UnnamedCardQdto(
                                drama_rel=drama.drama_rel, character_dir=card.character_dir, card_rel=card.card_rel,
                                error_code=card.error_code or "entity_name_unavailable", config_key=card.config_key,
                            )
                        )
                    continue
                usages.setdefault(card.entity_name, []).append(
                    EntityUsageQdto(drama.drama_rel, card.character_dir, card.card_rel, card.source_drama_rel, "card")
                )
            for name in drama.reference_entity_names:
                usages.setdefault(name, []).append(
                    EntityUsageQdto(drama.drama_rel, None, None, None, "reference_override")
                )
        rows = [*self._expected_rows(drama_rel, usages, records), *self._unmapped_rows(usages, records)]
        rows.sort(key=lambda row: (_STATE_ORDER[row.state], row.name))
        counts = Counter(row.state for row in rows)
        synced_at = facts.synced_at
        return ReconcileQdto(
            drama_rel=drama_rel,
            snapshot_synced_at=None if synced_at is None else iso(synced_at),
            snapshot_age_h=None if synced_at is None else round((now - synced_at).total_seconds() / 3600, 2),
            stale=facts.is_stale(now, stale_after),
            never_synced=facts.never_synced,
            mapped_count=counts[EntityReconcileState.MAPPED.value],
            missing_count=counts[EntityReconcileState.MISSING_ON_PLATFORM.value],
            unmapped_count=counts[EntityReconcileState.UNMAPPED_ON_PLATFORM.value],
            rows=tuple(rows),
            unnamed_cards=tuple(unnamed),
            config_issues=tuple(issues),
        )

    def _expected_rows(
        self, drama_rel: str | None, usages: dict[str, list[EntityUsageQdto]], records: Sequence[EntitySnapshotDao]
    ) -> list[ReconcileRowQdto]:
        by_name = {record.name: record for record in records}
        rows: list[ReconcileRowQdto] = []
        for name, found in usages.items():
            scoped = tuple(usage for usage in found if drama_rel is None or usage.drama_rel == drama_rel)
            if not scoped:
                continue
            record = by_name.get(name)
            state = EntityReconcileState.MAPPED if record is not None else EntityReconcileState.MISSING_ON_PLATFORM
            rows.append(
                ReconcileRowQdto(
                    name=name, state=state.value, usages=scoped,
                    thumbnail_url=None if record is None else record.thumbnail_url,
                    modified_at=None if record is None else record.modified_at,
                )
            )
        return rows

    def _unmapped_rows(
        self, usages: dict[str, list[EntityUsageQdto]], records: Sequence[EntitySnapshotDao]
    ) -> list[ReconcileRowQdto]:
        return [
            ReconcileRowQdto(
                name=record.name, state=EntityReconcileState.UNMAPPED_ON_PLATFORM.value, usages=(),
                thumbnail_url=record.thumbnail_url, modified_at=record.modified_at,
            )
            for record in records
            if record.name not in usages
        ]
