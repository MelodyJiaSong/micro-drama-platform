from __future__ import annotations

from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from libs.application.dtos.batch__dto import BatchConfirmationQdto, BatchQdto
from libs.application.errors.batch__error import BatchNotFoundError
from libs.application.mappers.batch__mapper import BatchMapper, StoredBatch
from libs.application.repositories.batch__repository import SqliteBatchRepository
from libs.common.clock import Clock, iso
from libs.common.enums import BatchState
from libs.domain.entities.batch__entity import BatchEntity
from libs.domain.errors.batch__error import BatchExpiredError, BatchNotAwaitingConfirmError
from libs.domain.value_objects.confirmation_token__valueobject import ConfirmationToken
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.global_config__reader import GlobalConfigReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.writers.secret_key__writer import SecretKeyWriter

# SQLite treats a negative LIMIT as "no limit".
_ALL_ROWS: int = -1


class BatchQuery:
    def __init__(
        self,
        global_config_reader: GlobalConfigReader,
        batch_repository: SqliteBatchRepository,
        batches: BatchMapper,
        batch_reader: BatchReader,
        job_reader: JobReader,
        secret_key_writer: SecretKeyWriter,
        secret_key_path: Path,
        clock: Clock,
        test_mode: bool = False,
    ) -> None:
        self._global_config_reader = global_config_reader
        self._batch_repository = batch_repository
        self._batches = batches
        self._batch_reader = batch_reader
        self._job_reader = job_reader
        self._secret_key_writer = secret_key_writer
        self._secret_key_path = secret_key_path
        self._clock = clock
        self._test_mode = test_mode

    def get(self, batch_id: str, page: int, page_size: int) -> BatchQdto:
        stored: StoredBatch = self._stored(batch_id)
        size: int = min(max(page_size, 1), self._global_config().api.page_size_max)
        stored.entity.expire(self._clock.now())
        jobs, _ = self._job_reader.list(None, batch_id, None, None, _ALL_ROWS, 0)
        return self._batches.batch_qdto(stored, sorted(job.job_id for job in jobs), max(page, 1), size)

    def confirmation(self, batch_id: str) -> BatchConfirmationQdto:
        """UI-only: issues the batch's token on first call; the expiry is fixed then, so reopening cannot extend it."""
        now: datetime = self._clock.now()
        config: GlobalConfig = self._global_config()
        batch: BatchEntity = self._stored(batch_id).entity
        token: ConfirmationToken = self._issue(batch, config.confirm.token_ttl_min, now)
        day_start, day_end = _day_bounds(now, config.time.timezone)
        return BatchConfirmationQdto(
            batch_id=batch.batch_id,
            token=token.encode(),
            expires_at=iso(token.expires_at),
            seconds_left=max(0, int((token.expires_at - now).total_seconds())),
            estimated_credits=batch.estimated_credits,
            today_confirmed_credits=self._batch_reader.confirmed_credits_between(iso(day_start), iso(day_end)),
        )

    def _issue(self, batch: BatchEntity, ttl_min: int, now: datetime) -> ConfirmationToken:
        if batch.expire(now):
            self._batch_repository.save_if_state(batch, BatchState.AWAITING_CONFIRM)
            raise BatchExpiredError("确认 token 已过期，请重新预检")
        first_issue: bool = batch.token_expires_at is None
        expires_at: datetime = batch.token_expires_at or ConfirmationToken.expiry(now, ttl_min).astimezone(timezone.utc)
        key: bytes = self._secret_key_writer.read(self._secret_key_path)
        token = ConfirmationToken.issue(batch.batch_id, batch.content_digest, batch.estimated_credits, expires_at, key)
        batch.issue_confirmation(token, now)
        if first_issue and not self._batch_repository.save_if_state(batch, BatchState.AWAITING_CONFIRM):
            raise BatchNotAwaitingConfirmError(f"批次 {batch.batch_id} 已不在待确认状态")
        return token

    def _stored(self, batch_id: str) -> StoredBatch:
        stored: StoredBatch | None = self._batch_repository.get_stored(batch_id)
        if stored is None:
            raise BatchNotFoundError(f"批次 {batch_id} 不存在")
        return stored

    def _global_config(self) -> GlobalConfig:
        return GlobalConfig.from_dict(self._global_config_reader.read().data, self._test_mode)


def _day_bounds(now: datetime, zone_name: str) -> tuple[datetime, datetime]:
    start = now.astimezone(_zone(zone_name)).replace(hour=0, minute=0, second=0, microsecond=0)
    return start, start + timedelta(days=1)


def _zone(name: str) -> tzinfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        # Windows ships no IANA database and `tzdata` is not a project dependency yet; see the impl-03 report.
        return timezone.utc
