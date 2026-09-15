from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from libs.application.mappers.request_json__mapper import RequestJsonMapper
from libs.common.clock import iso
from libs.common.enums import BackendKind, BlockedOn, Confirmer, JobState, PauseReason, PreparingStep
from libs.domain.entities.generation_job__entity import GenerationJobEntity, TransitionRecord
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao

CREATED_REASON: str = "created"


class JobMapper:
    """GenerationJobEntity ↔ JobDao. Columns the entity does not own (credits_charged, idempotency_key,
    created_at, drama_rel) are carried over from the stored row so a save never clobbers another writer's data."""

    def __init__(self, requests: RequestJsonMapper) -> None:
        self._requests: RequestJsonMapper = requests

    def to_entity(self, dao: JobDao, transitions: Sequence[JobTransitionDao]) -> GenerationJobEntity:
        extra: dict[str, Any] = json.loads(dao.extra_json)
        frozen: FrozenRequest | None = (
            None if dao.frozen_request_json is None else self._requests.frozen_from_dict(json.loads(dao.frozen_request_json))
        )
        confirmation: dict[str, Any] | None = extra.get("confirmation")
        return GenerationJobEntity(
            dao.job_id,
            dao.batch_id,
            BackendKind(dao.backend),
            self._request(dao, extra, frozen),
            Fingerprint(dao.fingerprint),
            attempt=dao.attempt,
            state=JobState(dao.state),
            blocked_on=BlockedOn(dao.blocked_on) if dao.blocked_on else BlockedOn.NONE,
            current_step=PreparingStep(dao.preparing_step) if dao.preparing_step else None,
            pause_reason=_reason(extra.get("pause_reason")),
            paused_from=JobState(extra["paused_from"]) if extra.get("paused_from") else None,
            failure_reason=_reason(extra.get("failure_reason")),
            confirmation=None if confirmation is None else BatchConfirmation(
                batch_id=dao.batch_id,
                confirmed_at=RequestJsonMapper.parse_iso(confirmation["confirmed_at"]),
                confirmer=Confirmer(confirmation["confirmer"]),
            ),
            frozen_request=frozen,
            platform_task_id=dao.platform_task_id,
            cancel_requested=dao.cancel_requested,
            credits_spent=dao.credits_spent,
            page_estimated_credits=dao.credits_estimated_page,
            approved_credits=extra.get("approved_credits"),
            transitions=[
                TransitionRecord(JobState(t.from_state), JobState(t.to_state), RequestJsonMapper.parse_iso(t.at), t.reason)
                for t in transitions
                if t.from_state is not None
            ],
        )

    def to_dao(self, job: GenerationJobEntity, existing: JobDao | None, drama_rel: str | None, now: datetime) -> JobDao:
        frozen: FrozenRequest | None = job.frozen_request
        extra: dict[str, Any] = {} if existing is None else json.loads(existing.extra_json)
        extra.update(
            {
                "confirmation": None if job.confirmation is None else {
                    "confirmed_at": iso(job.confirmation.confirmed_at),
                    "confirmer": job.confirmation.confirmer.value,
                },
                "pause_reason": _value(job.pause_reason),
                "paused_from": _value(job.paused_from),
                "failure_reason": _value(job.failure_reason),
                "approved_credits": job.approved_credits,
            }
        )
        if frozen is not None and frozen.request == job.request:
            extra.pop("request", None)
        else:
            extra["request"] = self._requests.request_to_dict(job.request)
        reason: PauseReason | None = job.pause_reason or job.failure_reason
        return JobDao(
            job_id=job.job_id,
            batch_id=job.batch_id,
            kind=job.request.kind.value,
            backend=job.backend.value,
            source_type=job.request.source.type.value,
            source_path=job.request.source.path,
            drama_rel=drama_rel if existing is None else (existing.drama_rel or drama_rel),
            output_slot=job.request.output_slot,
            state=job.state.value,
            reason=_value(reason),
            blocked_on=job.blocked_on.value,
            preparing_step=_value(job.current_step),
            fingerprint=job.fingerprint.value,
            idempotency_key=None if existing is None else existing.idempotency_key,
            attempt=job.attempt,
            confirmed=job.confirmed,
            cancel_requested=job.cancel_requested,
            credits_spent=job.credits_spent,
            platform_task_id=job.platform_task_id,
            credits_estimated_static=frozen.credits_estimated if frozen is not None else None,
            credits_estimated_page=job.page_estimated_credits,
            credits_charged=None if existing is None else existing.credits_charged,
            frozen_request_json=None if frozen is None else _dumps(self._requests.frozen_to_dict(frozen)),
            extra_json=_dumps(extra),
            created_at=iso(now) if existing is None else existing.created_at,
            updated_at=iso(now),
        )

    def new_transitions(
        self, job: GenerationJobEntity, persisted: Sequence[JobTransitionDao], now: datetime
    ) -> list[JobTransitionDao]:
        recorded: int = sum(1 for row in persisted if row.from_state is not None)
        rows: list[JobTransitionDao] = []
        history: tuple[TransitionRecord, ...] = job.transitions
        if not persisted:
            first: JobState = history[0].from_state if history else job.state
            rows.append(JobTransitionDao(job.job_id, None, first.value, CREATED_REASON, iso(now)))
        rows.extend(
            JobTransitionDao(job.job_id, record.from_state.value, record.to_state.value, record.reason, iso(record.at))
            for record in history[recorded:]
        )
        return rows

    def _request(self, dao: JobDao, extra: dict[str, Any], frozen: FrozenRequest | None) -> GenerationRequest:
        stored: dict[str, Any] | None = extra.get("request")
        if stored is not None:
            return self._requests.request_from_dict(stored)
        if frozen is None:
            raise ValueError(f"作业 {dao.job_id} 的存储记录既没有请求也没有冻结请求")
        return frozen.request


def _reason(value: str | None) -> PauseReason | None:
    return None if value is None else PauseReason(value)


def _value(member: JobState | PauseReason | PreparingStep | None) -> str | None:
    return None if member is None else member.value


def _dumps(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True)
