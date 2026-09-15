import pytest

from libs.common.enums import (
    PREPARING_STEP_ORDER, PREPARING_STEPS_BY_BACKEND, TERMINAL_JOB_STATES, BackendKind, BatchState, Confirmer,
    JobState, PauseReason, PreparingStep, RefKind,
)


def test_job_states_match_fr17() -> None:
    assert {s.value for s in JobState} == {
        "queued", "preparing", "submitting", "generating", "downloading", "done", "paused_needs_human", "failed", "cancelled",
    }


def test_terminal_states() -> None:
    assert TERMINAL_JOB_STATES == {JobState.DONE, JobState.FAILED, JobState.CANCELLED}


def test_preparing_step_order() -> None:
    assert PREPARING_STEP_ORDER == tuple(PreparingStep)
    assert [s.value for s in PREPARING_STEP_ORDER] == ["set_params", "upload", "fill", "preview", "verify"]


def test_preparing_steps_by_backend() -> None:
    assert PREPARING_STEPS_BY_BACKEND[BackendKind.WEB] == PREPARING_STEP_ORDER
    assert PREPARING_STEPS_BY_BACKEND[BackendKind.CLI] == (PreparingStep.VERIFY,)
    assert all(steps[-1] is PreparingStep.VERIFY for steps in PREPARING_STEPS_BY_BACKEND.values())
    with pytest.raises(TypeError):
        PREPARING_STEPS_BY_BACKEND[BackendKind.CLI] = ()  # type: ignore[index]


def test_confirmer_has_only_ui_human() -> None:
    assert [c.value for c in Confirmer] == ["ui_human"]


def test_batch_states() -> None:
    assert {s.value for s in BatchState} == {"awaiting_confirm", "confirmed", "expired", "rejected"}


def test_ref_kinds() -> None:
    assert {k.value for k in RefKind} == {"image", "video", "audio", "entity", "first_frame"}


def test_pause_reasons_cover_fr17_and_fr21() -> None:
    assert len(PauseReason) == 20
