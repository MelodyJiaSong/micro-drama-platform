
from typing import Callable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from libs.application.commands.gate__command import GateCommand
from libs.application.commands.pipeline__command import PipelineCommand
from libs.domain.errors.episode__error import InvalidStageTransitionError
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter

router = APIRouter()


class StepBody(BaseModel):
    drama_id: str
    episode_rel_dir: str


class RerunBody(StepBody):
    stage: str


class EditBody(BaseModel):
    episode_rel_dir: str
    artifact_rel_path: str
    content: str


def _locked(states: PipelineStateWriter, episode_rel_dir: str, fn: Callable[[], dict]) -> dict:
    """API-triggered runs contend with workers for the same per-episode lock — without
    it, a UI「自动跑完」racing a worker double-executes stages (observed: compose read
    understanding.json mid-write)."""
    if not states.try_claim(episode_rel_dir, "api"):
        raise HTTPException(status_code=409, detail="episode busy: another runner (worker/API) holds the lock; retry shortly")
    try:
        return fn()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    finally:
        states.release(episode_rel_dir)


@router.post("/api/episodes/step")
@inject
def step(body: StepBody, pipeline: PipelineCommand = Depends(Provide["pipeline_command"]),
         states: PipelineStateWriter = Depends(Provide["state_writer"])):
    return _locked(states, body.episode_rel_dir, lambda: pipeline.step(body.drama_id, body.episode_rel_dir))


@router.post("/api/episodes/run")
@inject
def run_to_completion(body: StepBody, pipeline: PipelineCommand = Depends(Provide["pipeline_command"]),
                      states: PipelineStateWriter = Depends(Provide["state_writer"])):
    return _locked(states, body.episode_rel_dir,
                   lambda: pipeline.run_to_completion(body.drama_id, body.episode_rel_dir))


@router.post("/api/episodes/rerun-stage")
@inject
def rerun_stage(body: RerunBody, pipeline: PipelineCommand = Depends(Provide["pipeline_command"]),
                states: PipelineStateWriter = Depends(Provide["state_writer"])):
    try:
        return _locked(states, body.episode_rel_dir,
                       lambda: pipeline.rerun_stage(body.drama_id, body.episode_rel_dir, body.stage))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"invalid stage: {exc}")


@router.post("/api/episodes/gate/release")
@inject
def release_gate(body: StepBody, gate: GateCommand = Depends(Provide["gate_command"])):
    try:
        return gate.release(body.episode_rel_dir)
    except InvalidStageTransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.post("/api/episodes/edit-artifact")
@inject
def edit_artifact(body: EditBody, gate: GateCommand = Depends(Provide["gate_command"])):
    try:
        return gate.edit_artifact(body.episode_rel_dir, body.artifact_rel_path, body.content)
    except InvalidStageTransitionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
