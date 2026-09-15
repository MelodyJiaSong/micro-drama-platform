from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timedelta
from pathlib import Path

from libs.application.dtos.batch__dto import BatchConfirmCdto, BatchItemInput, BatchPrecheckCdto
from libs.application.errors.batch__error import (
    BatchItemRejectedError,
    BatchNotFoundError,
    BatchTooLargeError,
    IdempotencyKeyReusedError,
)
from libs.application.mappers.batch__mapper import BatchItemMeta, BatchMapper, StoredBatch
from libs.application.mappers.job__mapper import JobMapper
from libs.application.mappers.request__mapper import MappedItem, RequestMapper
from libs.application.mappers.request_context__mapper import RequestContextMapper
from libs.application.mappers.request_input__mapper import RequestInputMapper
from libs.application.repositories.batch__repository import SqliteBatchRepository
from libs.common.canonical_json import canonical_sha256
from libs.common.clock import Clock, iso
from libs.common.enums import BatchState, Confirmer, GenerationKind
from libs.common.ids import new_id
from libs.domain.entities.batch__entity import BatchEntity
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.errors.batch__error import (
    BatchAlreadyConfirmedError,
    BatchError,
    BatchNotAwaitingConfirmError,
    EmptyBatchError,
    InvalidConfirmerError,
    TokenDigestMismatchError,
)
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.batch_item__valueobject import BatchItem
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.domain.value_objects.precheck__valueobject import run_precheck
from libs.domain.value_objects.precheck_context__valueobject import EntitySnapshotFacts
from libs.domain.value_objects.precheck_result__valueobject import PrecheckResult
from libs.infrastructure.daos.config_file__dao import ConfigFileDao
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao
from libs.infrastructure.daos.store_record__dao import IdempotencyDao
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.store_record__reader import IdempotencyReader
from libs.infrastructure.writers.batch_confirmation__writer import BatchConfirmationWriter
from libs.infrastructure.writers.secret_key__writer import SecretKeyWriter
from libs.infrastructure.writers.store_record__writer import IdempotencyWriter

ENTITY_REUSED_CODE: str = "entity_will_be_reused"
IdFactory = Callable[[str, datetime | None], str]
JobRow = tuple[JobDao, list[JobTransitionDao]]


class BatchCommand:
    def __init__(
        self,
        global_config_reader: GlobalConfigReader,
        requests: RequestMapper,
        inputs: RequestInputMapper,
        contexts: RequestContextMapper,
        batches: BatchMapper,
        jobs: JobMapper,
        batch_repository: SqliteBatchRepository,
        job_reader: JobReader,
        confirmation_writer: BatchConfirmationWriter,
        idempotency_reader: IdempotencyReader,
        idempotency_writer: IdempotencyWriter,
        secret_key_writer: SecretKeyWriter,
        secret_key_path: Path,
        clock: Clock,
        test_mode: bool = False,
        id_factory: IdFactory = new_id,
    ) -> None:
        self._global_config_reader = global_config_reader
        self._requests = requests
        self._inputs = inputs
        self._contexts = contexts
        self._batches = batches
        self._jobs = jobs
        self._batch_repository = batch_repository
        self._job_reader = job_reader
        self._confirmation_writer = confirmation_writer
        self._idempotency_reader = idempotency_reader
        self._idempotency_writer = idempotency_writer
        self._secret_key_writer = secret_key_writer
        self._secret_key_path = secret_key_path
        self._clock = clock
        self._test_mode = test_mode
        self._new_id = id_factory

    def precheck(self, items: Sequence[BatchItemInput], idempotency_key: str | None) -> BatchPrecheckCdto:
        now: datetime = self._clock.now()
        global_file, global_config = self._global_config()
        if not items:
            raise EmptyBatchError("批次至少要有一条")
        limit: int = global_config.api.max_batch_items
        if len(items) > limit:
            raise BatchTooLargeError(f"一次最多预检 {limit} 条，实际 {len(items)} 条", "api.max_batch_items")
        if idempotency_key is None:
            return self._create(items, global_file, global_config, now, None)
        body_sha256: str = canonical_sha256([self._inputs.to_dict(item) for item in items])
        retention = timedelta(hours=global_config.idempotency.retention_h)
        self._idempotency_writer.purge_created_before(iso(now - retention))
        previous: IdempotencyDao | None = self._idempotency_reader.get(idempotency_key)
        if previous is not None:
            return self._replay(previous, body_sha256)
        created: BatchPrecheckCdto = self._create(items, global_file, global_config, now, idempotency_key)
        record = IdempotencyDao(idempotency_key, body_sha256, self._batches.precheck_cdto_to_json(created), iso(now))
        return self._replay(self._idempotency_writer.put_if_absent(record), body_sha256)

    def reprecheck(
        self,
        batch_id: str,
        drop_error_items: bool,
        item_overrides: Mapping[int, BatchItemInput] | None = None,
    ) -> BatchPrecheckCdto:
        stored: StoredBatch = self._stored(batch_id)
        overrides: Mapping[int, BatchItemInput] = item_overrides or {}
        unknown: list[int] = sorted(index for index in overrides if not 0 <= index < len(stored.metas))
        if unknown:
            raise BatchItemRejectedError("item_index_invalid", f"批次 {batch_id} 没有第 {unknown[0]} 条", unknown[0])
        inputs: list[BatchItemInput] = [
            overrides[item.index] if item.index in overrides else self._inputs.from_dict(meta.input)
            for item, meta in zip(stored.entity.items, stored.metas, strict=True)
            if item.index in overrides or not (drop_error_items and item.precheck.has_errors)
        ]
        if not inputs:
            raise EmptyBatchError("剔除错误项之后批次为空，没有可以重新预检的条目")
        result: BatchPrecheckCdto = self.precheck(inputs, None)
        self._retire(stored.entity)
        return result

    def confirm(self, batch_id: str, token: str, confirmer: str, now: datetime | None = None) -> BatchConfirmCdto:
        at: datetime = now or self._clock.now()
        if confirmer != Confirmer.UI_HUMAN.value:
            raise InvalidConfirmerError("只有本地管理网页里的人可以确认批次")
        stored: StoredBatch = self._stored(batch_id)
        confirmation: BatchConfirmation = self._confirm_batch(stored.entity, token, at)
        global_file, global_config = self._global_config()
        self._require_unchanged(stored, global_file, global_config)
        job_ids, rows = self._jobs_for(stored, confirmation, at)
        dao = self._batches.to_dao(stored.entity, stored.metas, stored.idempotency_key, at)
        if not self._confirmation_writer.confirm(dao, stored.entity.content_digest, rows):
            raise self._lost_race(batch_id)
        return BatchConfirmCdto(batch_id=batch_id, job_ids=tuple(job_ids), confirmed_at=iso(at))

    def _create(
        self,
        items: Sequence[BatchItemInput],
        global_file: ConfigFileDao,
        global_config: GlobalConfig,
        now: datetime,
        idempotency_key: str | None,
    ) -> BatchPrecheckCdto:
        mapped: list[MappedItem] = self._requests.map_all(items, global_config, global_file.sha256)
        snapshot: EntitySnapshotFacts = self._contexts.snapshot()
        batch_items: list[BatchItem] = []
        metas: list[BatchItemMeta] = []
        for index, item in enumerate(mapped):
            result: PrecheckResult = run_precheck(item.request, self._contexts.context(item, global_config, snapshot, now))
            with_notices = PrecheckResult((*result.items, *item.settings.notices), result.estimate, result.existing_job_id)
            batch_items.append(BatchItem.of(index, item.request, with_notices))
            metas.append(
                BatchItemMeta(
                    backend=item.backend,
                    config_digest=item.config_digest,
                    estimate_tolerance_pct=item.settings.config.precheck.estimate_tolerance_pct,
                    drama_rel=item.drama_rel,
                    reroll=item.reroll,
                    input=item.input,
                )
            )
        batch = BatchEntity(self._new_id("batch", now), batch_items, now)
        self._batch_repository.create(batch, metas, idempotency_key)
        return self._batches.precheck_cdto(batch)

    def _replay(self, record: IdempotencyDao, body_sha256: str) -> BatchPrecheckCdto:
        if record.content_sha256 != body_sha256:
            raise IdempotencyKeyReusedError(f"idempotency_key {record.key} 已用于不同内容的预检")
        return self._batches.precheck_cdto_from_json(record.response_json)

    def _confirm_batch(self, batch: BatchEntity, token: str, at: datetime) -> BatchConfirmation:
        key: bytes = self._secret_key_writer.read(self._secret_key_path)
        return batch.confirm(token, key, Confirmer.UI_HUMAN, at)

    def _require_unchanged(self, stored: StoredBatch, global_file: ConfigFileDao, global_config: GlobalConfig) -> None:
        inputs: list[BatchItemInput] = [self._inputs.from_dict(meta.input) for meta in stored.metas]
        try:
            current: list[MappedItem] = self._requests.map_all(inputs, global_config, global_file.sha256)
        except BatchItemRejectedError as error:
            raise TokenDigestMismatchError(f"预检之后输入已变化（{error.message}），请重新预检") from error
        changed: list[str] = [
            str(item.index + 1)
            for item, fresh in zip(stored.entity.items, current, strict=True)
            if Fingerprint.of(fresh.request) != item.fingerprint
        ]
        if changed:
            raise TokenDigestMismatchError(f"第 {'、'.join(changed)} 条的 shot、参考文件或 config 在预检之后被改动，请重新预检")

    def _jobs_for(
        self, stored: StoredBatch, confirmation: BatchConfirmation, at: datetime
    ) -> tuple[list[str], list[JobRow]]:
        job_ids: list[str] = []
        rows: list[JobRow] = []
        for item, meta in zip(stored.entity.items, stored.metas, strict=True):
            if item.precheck.existing_job_id is not None:
                job_ids.append(item.precheck.existing_job_id)
                continue
            if _reuses_entity(item):
                continue
            job: GenerationJobEntity = self._confirmed_job(item, meta, confirmation, at)
            job_ids.append(job.job_id)
            rows.append((self._jobs.to_dao(job, None, meta.drama_rel, at), self._jobs.new_transitions(job, (), at)))
        return job_ids, rows

    def _confirmed_job(
        self, item: BatchItem, meta: BatchItemMeta, confirmation: BatchConfirmation, at: datetime
    ) -> GenerationJobEntity:
        job = GenerationJobEntity(
            self._new_id("job", at),
            confirmation.batch_id,
            meta.backend,
            item.request,
            item.fingerprint,
            attempt=self._next_attempt(item.fingerprint),
        )
        frozen = FrozenRequest.from_item(item, meta.backend, meta.config_digest, meta.estimate_tolerance_pct)
        job.confirm(confirmation, frozen, item)
        return job

    def _next_attempt(self, fingerprint: Fingerprint) -> int:
        return max((job.attempt for job in self._job_reader.find_by_fingerprint(fingerprint.value)), default=0) + 1

    def _lost_race(self, batch_id: str) -> BatchError:
        current: BatchEntity | None = self._batch_repository.get(batch_id)
        if current is not None and current.state is BatchState.CONFIRMED:
            return BatchAlreadyConfirmedError("该批次已确认，token 只能使用一次")
        state: str = "unknown" if current is None else current.state.value
        return BatchNotAwaitingConfirmError(f"批次处于 {state}，不能确认")

    def _retire(self, batch: BatchEntity) -> None:
        if batch.state is not BatchState.AWAITING_CONFIRM:
            return
        batch.reject()
        self._batch_repository.save_if_state(batch, BatchState.AWAITING_CONFIRM)

    def _stored(self, batch_id: str) -> StoredBatch:
        stored: StoredBatch | None = self._batch_repository.get_stored(batch_id)
        if stored is None:
            raise BatchNotFoundError(f"批次 {batch_id} 不存在")
        return stored

    def _global_config(self) -> tuple[ConfigFileDao, GlobalConfig]:
        global_file: ConfigFileDao = self._global_config_reader.read()
        return global_file, GlobalConfig.from_dict(global_file.data, self._test_mode)


def _reuses_entity(item: BatchItem) -> bool:
    return item.request.kind is GenerationKind.ENTITY and any(
        check.error_code == ENTITY_REUSED_CODE for check in item.precheck.items
    )
