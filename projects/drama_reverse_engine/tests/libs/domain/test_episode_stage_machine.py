from __future__ import annotations

import pytest

from libs.common.enums import PipelineStage
from libs.domain.entities.episode__entity import EpisodeEntity
from libs.domain.errors.episode__error import InvalidStageTransitionError


def _ep() -> EpisodeEntity:
    return EpisodeEntity(entity_id="ep01", drama_id="d1", index=1, source_rel_path="d1/ep01/source.mp4")


def test_full_forward_walk_reaches_done() -> None:
    ep = _ep()
    seen = [ep.stage]
    while ep.stage is not PipelineStage.DONE:
        seen.append(ep.advance())
    assert seen[0] is PipelineStage.INGEST
    assert seen[-1] is PipelineStage.DONE
    assert len(seen) == 8  # ingest→extract→assets→understand→compose→gate_a→gate_b→done


def test_advance_past_done_rejected() -> None:
    ep = _ep()
    while ep.stage is not PipelineStage.DONE:
        ep.advance()
    with pytest.raises(InvalidStageTransitionError):
        ep.advance()


def test_gate_hold_blocks_advance_until_release() -> None:
    ep = _ep()
    while ep.stage is not PipelineStage.GATE_A:
        ep.advance()
    ep.hold_at_gate()
    with pytest.raises(InvalidStageTransitionError):
        ep.advance()
    ep.release_gate()
    assert ep.advance() is PipelineStage.GATE_B


def test_hold_at_non_gate_stage_rejected() -> None:
    ep = _ep()
    with pytest.raises(InvalidStageTransitionError):
        ep.hold_at_gate()


@pytest.mark.parametrize("steps", range(8))
def test_fail_and_retry_pinned_at_every_stage(steps: int) -> None:
    ep = _ep()
    for _ in range(steps):
        ep.advance()
    ep.fail("boom")
    assert ep.is_failed
    if ep.stage is not PipelineStage.DONE:
        with pytest.raises(InvalidStageTransitionError):
            ep.advance()
    ep.retry()
    assert not ep.is_failed


def test_failed_episode_cannot_advance_until_retry() -> None:
    ep = _ep()
    ep.fail("boom")
    with pytest.raises(InvalidStageTransitionError):
        ep.advance()
    ep.retry()
    assert ep.advance() is PipelineStage.EXTRACT
