from __future__ import annotations

import json
from collections.abc import Callable, Sequence

from libs.application.dtos.job__dto import (
    AllowedActionQdto, JobDetailQdto, JobPageQdto, JobRuntimeQdto, JobSummaryQdto, TransitionQdto,
)
from libs.application.errors.lifecycle__error import InvalidQueryFilterError
from libs.common.enums import TERMINAL_JOB_STATES, JobState, PauseReason, ResumeAllowance
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.domain.value_objects.pause_reason__valueobject import PauseReasonPolicy
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao
from libs.infrastructure.readers.job__reader import JobReader

RUNTIME_KEY: str = "runtime"


class JobQuery:
    """Read side for jobs (DAO → Qdto; no aggregate load, development.md §3 carve-out)."""

    def __init__(self, reader: JobReader, global_config_provider: Callable[[], GlobalConfig]) -> None:
        self._reader = reader
        self._global_config_provider = global_config_provider

    def list(
        self,
        states: Sequence[str] | None = None,
        batch_id: str | None = None,
        drama_rel: str | None = None,
        updated_after: str | None = None,
        page: int = 1,
        page_size: int | None = None,
    ) -> JobPageQdto:
        api = self._global_config_provider().api
        size = api.page_size_default if page_size is None else max(1, min(page_size, api.page_size_max))
        number = max(1, page)
        wanted = [_state(value).value for value in states] if states else None
        rows, total = self._reader.list(wanted, batch_id, drama_rel, updated_after, size, (number - 1) * size)
        cursor = max((row.updated_at for row in rows), default=updated_after)
        return JobPageQdto(tuple(job_summary(row) for row in rows), total, number, size, cursor)

    def get(self, job_id: str) -> JobDetailQdto | None:
        dao = self._reader.get(job_id)
        if dao is None:
            return None
        transitions = self._reader.transitions(job_id)
        state = JobState(dao.state)
        reason = _pause_reason(dao) if state is JobState.PAUSED_NEEDS_HUMAN else None
        rule = None if reason is None else PauseReasonPolicy.rule(reason)
        return JobDetailQdto(
            job=job_summary(dao),
            transitions=tuple(TransitionQdto(t.from_state, t.to_state, t.reason, t.at) for t in transitions),
            pause_reason=None if reason is None else reason.value,
            pause_tier=None if rule is None else rule.tier.value,
            resume_allowance=None if rule is None else rule.resume.value,
            allowed_actions=_allowed_actions(dao, reason, _paused_from(transitions)),
            runtime=runtime_facts(dao.extra_json),
            credits_not_refundable=dao.credits_spent or dao.platform_task_id is not None,
        )


def job_summary(dao: JobDao) -> JobSummaryQdto:
    return JobSummaryQdto(
        job_id=dao.job_id, batch_id=dao.batch_id, kind=dao.kind, backend=dao.backend, source_type=dao.source_type,
        source_path=dao.source_path, drama_rel=dao.drama_rel, output_slot=dao.output_slot, state=dao.state,
        reason=dao.reason, blocked_on=dao.blocked_on, preparing_step=dao.preparing_step, attempt=dao.attempt,
        confirmed=dao.confirmed, cancel_requested=dao.cancel_requested, credits_spent=dao.credits_spent,
        platform_task_id=dao.platform_task_id, credits_estimated_static=dao.credits_estimated_static,
        credits_estimated_page=dao.credits_estimated_page, credits_charged=dao.credits_charged,
        created_at=dao.created_at, updated_at=dao.updated_at,
    )


def runtime_facts(extra_json: str | None) -> JobRuntimeQdto:
    try:
        extra = json.loads(extra_json) if extra_json else {}
    except ValueError:
        extra = {}
    bucket = extra.get(RUNTIME_KEY) if isinstance(extra, dict) else None
    facts: dict[str, object] = bucket if isinstance(bucket, dict) else {}
    progress = facts.get("progress_pct")
    last_error = facts.get("last_error")
    return JobRuntimeQdto(
        screenshots=_strings(facts.get("screenshots")),
        outputs=_strings(facts.get("outputs")),
        progress_pct=progress if isinstance(progress, int) and not isinstance(progress, bool) else None,
        last_error=last_error if isinstance(last_error, str) else None,
        sidecar_missing=facts.get("sidecar_missing") is True,
    )


def _allowed_actions(dao: JobDao, reason: PauseReason | None, paused_from: JobState | None) -> tuple[AllowedActionQdto, ...]:
    state = JobState(dao.state)
    if state in TERMINAL_JOB_STATES:
        return ()
    if state is JobState.PAUSED_NEEDS_HUMAN:
        if reason is None:
            return ()
        if PauseReasonPolicy.requires_adjudication(reason, paused_from, dao.platform_task_id is not None):
            return (AllowedActionQdto("adjudicate", True),)
        if reason is PauseReason.ESTIMATE_EXCEEDS_CONFIRMED:
            first = AllowedActionQdto("approve_estimate", True)
        elif PauseReasonPolicy.rule(reason).resume is ResumeAllowance.NEVER:
            first = AllowedActionQdto("reprecheck", False)
        else:
            first = AllowedActionQdto("resume", False)
        return (first, AllowedActionQdto("cancel", False))
    actions = [AllowedActionQdto("cancel", False)]
    if state is JobState.QUEUED:
        actions.append(AllowedActionQdto("steps", False))
        if dao.confirmed:
            actions.append(AllowedActionQdto("step_submit", True))
    return tuple(actions)


def _pause_reason(dao: JobDao) -> PauseReason | None:
    try:
        return None if dao.reason is None else PauseReason(dao.reason)
    except ValueError:
        return None


def _paused_from(transitions: Sequence[JobTransitionDao]) -> JobState | None:
    for transition in reversed(transitions):
        if transition.to_state == JobState.PAUSED_NEEDS_HUMAN.value:
            return None if transition.from_state is None else JobState(transition.from_state)
    return None


def _state(value: str) -> JobState:
    try:
        return JobState(value)
    except ValueError as error:
        raise InvalidQueryFilterError(f"未知作业状态 {value!r}") from error


def _strings(value: object) -> tuple[str, ...]:
    return tuple(item for item in value if isinstance(item, str)) if isinstance(value, list) else ()
