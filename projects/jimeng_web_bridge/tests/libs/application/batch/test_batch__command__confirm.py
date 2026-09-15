from __future__ import annotations

import threading
from dataclasses import replace
from datetime import timedelta

import pytest

from libs.application.dtos.batch__dto import BatchConfirmCdto, BatchItemInput, EntityCreateItemInput, ShotItemInput
from libs.application.errors.batch__error import BatchItemRejectedError
from libs.common.clock import iso
from libs.common.enums import BackendKind, BatchState, Confirmer, JobState
from libs.domain.errors.batch__error import (
    BatchAlreadyConfirmedError,
    BatchError,
    BatchHasErrorsError,
    BatchNotAwaitingConfirmError,
    InvalidConfirmerError,
    TokenDigestMismatchError,
    TokenExpiredError,
    TokenInvalidError,
)
from tests.libs.application.batch.support import (
    C1_DIR_NAME,
    HY3,
    P2,
    REXUE_SHOT01,
    SHOT02,
    SHOT02_DIR,
    T0,
    BatchEnv,
)


def _prechecked(env: BatchEnv, *items: BatchItemInput) -> tuple[str, str]:
    batch_id = env.command.precheck(list(items), None).batch_id
    return batch_id, env.query.confirmation(batch_id).token


def _state(env: BatchEnv, batch_id: str) -> BatchState:
    batch = env.batches.get(batch_id)
    assert batch is not None
    return batch.state


def test_confirm_creates_queued_jobs_with_frozen_requests(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))

    result = env.command.confirm(batch_id, token, "ui_human")

    assert result.batch_id == batch_id and len(result.job_ids) == 1 and result.confirmed_at == iso(T0)
    stored = env.batches.get_stored(batch_id)
    assert stored is not None
    assert stored.entity.state is BatchState.CONFIRMED and stored.entity.confirmer is Confirmer.UI_HUMAN
    assert stored.entity.confirmed_at == T0
    job = env.jobs.get(result.job_ids[0])
    assert job is not None
    assert (job.state, job.backend, job.attempt, job.confirmed) == (JobState.QUEUED, BackendKind.WEB, 1, True)
    frozen = job.frozen_request
    assert frozen is not None
    assert frozen.request == stored.entity.items[0].request
    assert frozen.credits_estimated == 440 and frozen.entity_names == ("hy3_主角",)
    assert frozen.estimate_tolerance_pct == 20
    assert frozen.config_digest == stored.metas[0].config_digest and len(frozen.config_digest) == 64
    row = env.job_reader.get(job.job_id)
    assert row is not None
    assert (row.drama_rel, row.source_path, row.output_slot, row.credits_estimated_static) == (HY3, SHOT02, SHOT02_DIR, 440)
    assert [(t.from_state, t.to_state) for t in env.job_reader.transitions(job.job_id)] == [(None, "queued")]


def test_replayed_token_is_rejected_and_creates_nothing(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))
    env.command.confirm(batch_id, token, "ui_human")

    with pytest.raises(BatchAlreadyConfirmedError):
        env.command.confirm(batch_id, token, "ui_human")

    assert env.job_count() == 1


def test_expired_token_is_rejected_and_reprecheck_builds_a_new_batch(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))
    env.clock.advance(timedelta(minutes=31))

    with pytest.raises(TokenExpiredError):
        env.command.confirm(batch_id, token, "ui_human")
    assert env.job_count() == 0

    renewed = env.command.reprecheck(batch_id, drop_error_items=False)
    assert renewed.batch_id != batch_id and renewed.estimated_credits == 440
    assert _state(env, batch_id) is BatchState.REJECTED
    new_token = env.query.confirmation(renewed.batch_id).token
    assert len(env.command.confirm(renewed.batch_id, new_token, "ui_human").job_ids) == 1


def test_inputs_changed_after_precheck_reject_the_confirmation(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))
    with (env.repo / P2).open("ab") as handle:
        handle.write(b"\x00")

    with pytest.raises(TokenDigestMismatchError):
        env.command.confirm(batch_id, token, "ui_human")

    assert env.job_count() == 0 and _state(env, batch_id) is BatchState.AWAITING_CONFIRM


def test_batch_with_error_items_is_rejected_until_errors_are_dropped(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02), ShotItemInput(REXUE_SHOT01))

    with pytest.raises(BatchHasErrorsError):
        env.command.confirm(batch_id, token, "ui_human")
    assert env.job_count() == 0

    cleaned = env.command.reprecheck(batch_id, drop_error_items=True)
    stored = env.batches.get_stored(cleaned.batch_id)
    assert stored is not None and [item.request.source.path for item in stored.entity.items] == [SHOT02]
    assert cleaned.error_count == 0


@pytest.mark.parametrize("confirmer", ["mcp", "http_auto", "UI_HUMAN", ""])
def test_only_ui_human_can_confirm(env: BatchEnv, confirmer: str) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))

    with pytest.raises(InvalidConfirmerError):
        env.command.confirm(batch_id, token, confirmer)

    assert env.job_count() == 0 and _state(env, batch_id) is BatchState.AWAITING_CONFIRM


def test_tampered_or_foreign_tokens_are_rejected(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))
    other_id, other_token = _prechecked(env, ShotItemInput(SHOT02, reroll=True))
    flipped = token[:-1] + ("0" if token[-1] != "0" else "1")

    with pytest.raises(TokenInvalidError):
        env.command.confirm(batch_id, flipped, "ui_human")
    with pytest.raises((TokenDigestMismatchError, TokenInvalidError)):
        env.command.confirm(batch_id, other_token, "ui_human")

    assert env.job_count() == 0 and other_id != batch_id


def test_concurrent_double_confirm_has_exactly_one_winner(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))
    barrier = threading.Barrier(2)
    outcomes: list[BatchConfirmCdto | BatchError] = []
    lock = threading.Lock()

    def attempt() -> None:
        barrier.wait()
        try:
            outcome: BatchConfirmCdto | BatchError = env.command.confirm(batch_id, token, "ui_human")
        except BatchError as error:
            outcome = error
        with lock:
            outcomes.append(outcome)

    threads = [threading.Thread(target=attempt) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(outcomes) == 2
    assert sum(isinstance(outcome, BatchConfirmCdto) for outcome in outcomes) == 1
    assert all(
        isinstance(outcome, (BatchConfirmCdto, BatchAlreadyConfirmedError, BatchNotAwaitingConfirmError))
        for outcome in outcomes
    )
    assert env.job_count() == 1


def test_fingerprint_hit_reuses_the_job_unless_reroll(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, ShotItemInput(SHOT02))
    (first_job,) = env.command.confirm(batch_id, token, "ui_human").job_ids

    again = env.command.precheck([ShotItemInput(SHOT02)], None)
    assert again.existing_job_ids == (first_job,) and again.estimated_credits == 0
    again_token = env.query.confirmation(again.batch_id).token
    assert env.command.confirm(again.batch_id, again_token, "ui_human").job_ids == (first_job,)
    assert env.job_count() == 1

    reroll_id, reroll_token = _prechecked(env, ShotItemInput(SHOT02, reroll=True))
    (second_job,) = env.command.confirm(reroll_id, reroll_token, "ui_human").job_ids
    second = env.jobs.get(second_job)
    assert second_job != first_job and second is not None and second.attempt == 2
    assert env.job_count() == 2

    for job_id in (first_job, second_job):
        row = env.job_reader.get(job_id)
        assert row is not None
        env.job_writer.save(replace(row, state="cancelled"), [])
    after_cancel = env.command.precheck([ShotItemInput(SHOT02)], None)
    assert after_cancel.existing_job_ids == () and after_cancel.estimated_credits == 440


def test_entity_reuse_item_confirms_without_a_job(env: BatchEnv) -> None:
    batch_id, token = _prechecked(env, EntityCreateItemInput(HY3, C1_DIR_NAME))

    assert env.command.confirm(batch_id, token, "ui_human").job_ids == ()
    assert env.job_count() == 0 and _state(env, batch_id) is BatchState.CONFIRMED


def test_description_edit_goes_through_reprecheck_with_an_item_override(env: BatchEnv) -> None:
    env.write_drama_config(HY3)
    batch_id, _ = _prechecked(env, EntityCreateItemInput(HY3, C1_DIR_NAME))

    edited = env.command.reprecheck(batch_id, False, {0: EntityCreateItemInput(HY3, C1_DIR_NAME, "页面上改过的描述")})

    stored = env.batches.get_stored(edited.batch_id)
    assert stored is not None and stored.entity.items[0].request.prompt == "页面上改过的描述"
    assert _state(env, batch_id) is BatchState.REJECTED
    token = env.query.confirmation(edited.batch_id).token
    (job_id,) = env.command.confirm(edited.batch_id, token, "ui_human").job_ids
    job = env.jobs.get(job_id)
    assert job is not None and job.frozen_request is not None
    assert job.frozen_request.request.prompt == "页面上改过的描述" and job.backend is BackendKind.WEB
    with pytest.raises(BatchItemRejectedError):
        env.command.reprecheck(edited.batch_id, False, {5: EntityCreateItemInput(HY3, C1_DIR_NAME)})
