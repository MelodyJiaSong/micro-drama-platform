from __future__ import annotations

import os
from datetime import datetime, timedelta

from libs.application.mappers.request__mapper import MappedItem
from libs.application.mappers.request_json__mapper import RequestJsonMapper
from libs.common.enums import JobState
from libs.common.paths import RepoSandbox
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.domain.value_objects.precheck_context__valueobject import EntitySnapshotFacts, PrecheckContext
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.store_record__reader import EntitySnapshotReader

_STATES_WITHOUT_RESULT: frozenset[str] = frozenset({JobState.FAILED.value, JobState.CANCELLED.value})


class RequestContextMapper:
    """Collects the I/O facts FR-11 needs (snapshot, writability, fingerprint hit) into a pure PrecheckContext."""

    def __init__(self, sandbox: RepoSandbox, snapshots: EntitySnapshotReader, jobs: JobReader) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._snapshots: EntitySnapshotReader = snapshots
        self._jobs: JobReader = jobs

    def snapshot(self) -> EntitySnapshotFacts:
        synced_at: str | None = self._snapshots.last_synced_at()
        return EntitySnapshotFacts(
            names=frozenset(record.name for record in self._snapshots.all()),
            synced_at=None if synced_at is None else RequestJsonMapper.parse_iso(synced_at),
        )

    def context(
        self, item: MappedItem, global_config: GlobalConfig, snapshot: EntitySnapshotFacts, now: datetime
    ) -> PrecheckContext:
        config = item.settings.config
        return PrecheckContext(
            backend=item.backend,
            limits=global_config.model_limits,
            price_table=global_config.price_table,
            prompt_max_chars=config.precheck.prompt_max_chars,
            entity_name_max_chars=config.precheck.entity_name_max_chars,
            negative_prompt_strategy=config.video.negative_prompt,
            snapshot=snapshot,
            snapshot_stale_after=timedelta(hours=global_config.entities.snapshot_stale_h),
            now=now,
            output_dir_writable=item.output_dir is None or self._writable(item.output_dir),
            reference_issues=item.references.issues,
            legacy_reference_fragments=item.references.legacy,
            fingerprint_hit_job_id=self.fingerprint_hit(Fingerprint.of(item.request)),
            reroll=item.reroll,
            entity_card_dirs=item.references.entity_card_dirs,
        )

    def fingerprint_hit(self, fingerprint: Fingerprint) -> str | None:
        live = [job for job in self._jobs.find_by_fingerprint(fingerprint.value) if job.state not in _STATES_WITHOUT_RESULT]
        return live[-1].job_id if live else None

    def _writable(self, rel: str) -> bool:
        verdict = self._sandbox.check_write(rel)
        if not verdict.ok or verdict.path is None:
            return False
        probe = verdict.path
        while not probe.exists() and probe.parent != probe:
            probe = probe.parent
        return probe.is_dir() and os.access(probe, os.W_OK)
