from __future__ import annotations

from dataclasses import replace
from datetime import timedelta

from libs.application.dtos.batch__dto import ShotItemInput
from libs.common.enums import JobState, PauseReason, PreparingStep
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from tests.libs.application.batch.support import HY3, SHOT02, T0, BatchEnv


def _view(job: GenerationJobEntity) -> tuple[object, ...]:
    return (
        job.job_id, job.batch_id, job.backend, job.request, job.fingerprint, job.attempt, job.state, job.blocked_on,
        job.current_step, job.pause_reason, job.paused_from, job.failure_reason, job.confirmation, job.frozen_request,
        job.platform_task_id, job.cancel_requested, job.credits_spent, job.page_estimated_credits,
        job.approved_credits, job.transitions,
    )


def _confirmed_job_id(env: BatchEnv) -> tuple[str, str]:
    batch_id = env.command.precheck([ShotItemInput(SHOT02)], None).batch_id
    token = env.query.confirmation(batch_id).token
    return batch_id, env.command.confirm(batch_id, token, "ui_human").job_ids[0]


def test_round_trip_appends_only_new_transitions_and_keeps_foreign_columns(env: BatchEnv) -> None:
    batch_id, job_id = _confirmed_job_id(env)
    job = env.jobs.get(job_id)
    assert job is not None
    job.start_preparing(T0 + timedelta(minutes=1))
    job.advance_step(PreparingStep.UPLOAD)
    env.jobs.save(job)
    row = env.job_reader.get(job_id)
    assert row is not None
    env.job_writer.save(replace(row, credits_charged=440, idempotency_key="k1"), [])

    reloaded = env.jobs.get(job_id)
    assert reloaded is not None
    reloaded.pause(PauseReason.STEP_FAILED, T0 + timedelta(minutes=2))
    env.jobs.save(reloaded)

    final = env.jobs.get(job_id)
    assert final is not None and _view(final) == _view(reloaded)
    assert [(t.from_state, t.to_state, t.reason) for t in env.job_reader.transitions(job_id)] == [
        (None, "queued", "created"),
        ("queued", "preparing", None),
        ("preparing", "paused_needs_human", "step_failed"),
    ]
    stored = env.job_reader.get(job_id)
    assert stored is not None
    assert (stored.credits_charged, stored.idempotency_key, stored.reason, stored.drama_rel) == (440, "k1", "step_failed", HY3)
    assert [job.job_id for job in env.jobs.list_by_batch(batch_id)] == [job_id]
    assert [job.job_id for job in env.jobs.list_in_states(frozenset({JobState.PAUSED_NEEDS_HUMAN}))] == [job_id]
    assert env.jobs.list_in_states(frozenset()) == []
    assert [job.job_id for job in env.jobs.find_by_fingerprint(final.fingerprint)] == [job_id]


def test_unconfirmed_job_round_trips_its_request_without_a_frozen_copy(env: BatchEnv) -> None:
    batch_id = env.command.precheck([ShotItemInput(SHOT02)], None).batch_id
    stored = env.batches.get_stored(batch_id)
    assert stored is not None
    item = stored.entity.items[0]
    job = GenerationJobEntity("job_unconfirmed", batch_id, stored.metas[0].backend, item.request, item.fingerprint)

    env.jobs.save(job)

    loaded = env.jobs.get("job_unconfirmed")
    assert loaded is not None and _view(loaded) == _view(job)
    row = env.job_reader.get("job_unconfirmed")
    assert row is not None and row.frozen_request_json is None and row.drama_rel == HY3 and not row.confirmed
