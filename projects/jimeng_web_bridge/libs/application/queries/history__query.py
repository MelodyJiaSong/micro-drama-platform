from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import date, datetime, timedelta
from datetime import time as day_start
from pathlib import PurePosixPath

from libs.application.dtos.history__dto import (
    BatchBalanceQdto, DailyTotalQdto, DailyTotalsQdto, DurationsQdto, HistoryItemQdto, HistoryPageQdto,
)
from libs.application.errors.lifecycle__error import InvalidQueryFilterError
from libs.application.queries.job__query import runtime_facts
from libs.common.clock import Clock, iso
from libs.common.enums import JobState, SourceType
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.writers.output__writer import CANDIDATES_DIR_NAME, zone_for

HISTORY_SCAN_LIMIT: int = 50_000
MAX_DAYS: int = 366
_FINISHED: frozenset[str] = frozenset({JobState.DONE.value, JobState.FAILED.value, JobState.CANCELLED.value})
_ONE_TICK: timedelta = timedelta(microseconds=1)


class HistoryQuery:
    """Generation history and daily credit totals (FR-46). Days are cut in `time.timezone`."""

    def __init__(
        self,
        job_reader: JobReader,
        batch_reader: BatchReader,
        global_config_provider: Callable[[], GlobalConfig],
        clock: Clock,
    ) -> None:
        self._jobs = job_reader
        self._batches = batch_reader
        self._global_config_provider = global_config_provider
        self._clock = clock

    def list(
        self,
        drama_rel: str | None = None,
        shot: str | None = None,
        subject: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        page: int = 1,
        page_size: int | None = None,
    ) -> HistoryPageQdto:
        cfg = self._global_config_provider()
        zone = zone_for(cfg.time.timezone)
        start = None if date_from is None else datetime.combine(_date(date_from), day_start.min, zone)
        end = None if date_to is None else datetime.combine(_date(date_to) + timedelta(days=1), day_start.min, zone)
        rows = [
            row for row in self._scan(drama_rel, start)
            if (shot is None or _shot(row) == shot)
            and (subject is None or subject in _subject(row))
            and (start is None or _parse(row.created_at) >= start)
            and (end is None or _parse(row.created_at) < end)
        ]
        rows.sort(key=lambda row: (row.created_at, row.job_id), reverse=True)
        size = cfg.api.page_size_default if page_size is None else max(1, min(page_size, cfg.api.page_size_max))
        number = max(1, page)
        chunk = rows[(number - 1) * size: number * size]
        items = tuple(self._item(row) for row in chunk)
        batches = tuple(self._balance(batch_id) for batch_id in dict.fromkeys(row.batch_id for row in chunk))
        return HistoryPageQdto(items, len(rows), number, size, batches)

    def daily_totals(self, days: int = 7, timezone: str | None = None) -> DailyTotalsQdto:
        cfg = self._global_config_provider()
        zone_name = timezone or cfg.time.timezone
        zone = zone_for(zone_name)
        span = max(1, min(days, MAX_DAYS))
        today = self._clock.now().astimezone(zone).date()
        first = today - timedelta(days=span - 1)
        totals: dict[date, list[int]] = {first + timedelta(days=i): [0, 0, 0, 0, 0, 0] for i in range(span)}
        for row in self._scan(None, datetime.combine(first, day_start.min, zone)):
            bucket = totals.get(_parse(row.created_at).astimezone(zone).date())
            if bucket is None:
                continue
            bucket[0] += 1
            bucket[1] += row.state == JobState.DONE.value
            bucket[2] += row.state == JobState.FAILED.value
            bucket[3] += row.credits_estimated_static or 0
            bucket[4] += row.credits_estimated_page or 0
            bucket[5] += row.credits_charged or 0
        return DailyTotalsQdto(
            zone_name,
            tuple(DailyTotalQdto(day.isoformat(), *values) for day, values in totals.items()),
        )

    def _scan(self, drama_rel: str | None, since: datetime | None) -> list[JobDao]:
        updated_after = None if since is None else iso(since - _ONE_TICK)
        rows, _ = self._jobs.list(None, None, drama_rel, updated_after, HISTORY_SCAN_LIMIT, 0)
        return rows

    def _item(self, row: JobDao) -> HistoryItemQdto:
        transitions = self._jobs.transitions(row.job_id)
        outputs = runtime_facts(row.extra_json).outputs
        slot, _, block_key = row.output_slot.partition("#")
        return HistoryItemQdto(
            job_id=row.job_id, batch_id=row.batch_id, kind=row.kind, backend=row.backend, state=row.state,
            reason=row.reason, drama_rel=row.drama_rel, shot=_shot(row),
            subject=PurePosixPath(slot).name if block_key else None, block_key=block_key or None,
            source_path=row.source_path, output_slot=row.output_slot, attempt=row.attempt,
            credits_estimated_static=row.credits_estimated_static, credits_estimated_page=row.credits_estimated_page,
            credits_charged=row.credits_charged, created_at=row.created_at,
            finished_at=_last_at(transitions, *_FINISHED), durations=_durations(row, transitions), outputs=outputs,
            candidates=tuple(path for path in outputs if f"/{CANDIDATES_DIR_NAME}/" in path),
        )

    def _balance(self, batch_id: str) -> BatchBalanceQdto:
        batch = self._batches.get(batch_id)
        return BatchBalanceQdto(batch_id, None if batch is None else batch.balance_start, None if batch is None else batch.balance_end)


def _durations(row: JobDao, transitions: Sequence[JobTransitionDao]) -> DurationsQdto:
    preparing = _last_at(transitions, JobState.PREPARING.value)
    submitting = _last_at(transitions, JobState.SUBMITTING.value)
    generating = _last_at(transitions, JobState.GENERATING.value)
    downloading = _last_at(transitions, JobState.DOWNLOADING.value)
    done = _last_at(transitions, JobState.DONE.value)
    return DurationsQdto(
        queue_wait_s=_seconds(row.created_at, preparing),
        prepare_s=_seconds(preparing, submitting),
        render_s=_seconds(generating, downloading),
        download_s=_seconds(downloading, done),
    )


def _shot(row: JobDao) -> str | None:
    return PurePosixPath(row.output_slot).name if row.source_type == SourceType.SHOT.value else None


def _subject(row: JobDao) -> tuple[str, ...]:
    slot, _, block_key = row.output_slot.partition("#")
    return (PurePosixPath(slot).name, block_key) if block_key else ()


def _last_at(transitions: Sequence[JobTransitionDao], *states: str) -> str | None:
    for transition in reversed(transitions):
        if transition.to_state in states:
            return transition.at
    return None


def _seconds(start: str | None, end: str | None) -> float | None:
    if start is None or end is None:
        return None
    return round((_parse(end) - _parse(start)).total_seconds(), 3)


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise InvalidQueryFilterError(f"日期必须是 YYYY-MM-DD，收到 {value!r}") from error
