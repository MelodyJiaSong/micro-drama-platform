"""Eval-center routes: read-only verdict/rubric views + rubric/config editing.

Eval runs are triggered from the ai_video_eval CLI only — there is deliberately
no run-trigger endpoint here.
"""
from __future__ import annotations

from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from apps.api.container import Container
from libs.application.commands.eval_center__command import EvalCenterCommand
from libs.application.queries.eval_center__query import EvalCenterQuery
from libs.infrastructure.readers.eval_center__reader import EvalCenterError

router = APIRouter()


def _error(exc: EvalCenterError) -> Response:
    status = 404 if exc.kind == "not_found" else 400
    return JSONResponse(
        status_code=status, content={"detail": {"kind": exc.kind, "message": str(exc)}}
    )


class RubricFileBody(BaseModel):
    name: str
    content: str


class ConfigBody(BaseModel):
    content: str


@router.get("/api/eval/overview")
@inject
def eval_overview(
    query: EvalCenterQuery = Depends(Provide[Container.eval_center_query]),
) -> Any:
    try:
        return query.overview()
    except EvalCenterError as exc:
        return _error(exc)


@router.get("/api/eval/rubric-file")
@inject
def eval_rubric_file(
    name: str, query: EvalCenterQuery = Depends(Provide[Container.eval_center_query])
) -> Any:
    try:
        return query.rubric_file(name)
    except EvalCenterError as exc:
        return _error(exc)


@router.put("/api/eval/rubric-file")
@inject
def eval_save_rubric_file(
    body: RubricFileBody,
    command: EvalCenterCommand = Depends(Provide[Container.eval_center_command]),
) -> Any:
    try:
        return command.save_rubric_file(body.name, body.content)
    except EvalCenterError as exc:
        return _error(exc)


@router.get("/api/eval/config")
@inject
def eval_config(
    query: EvalCenterQuery = Depends(Provide[Container.eval_center_query]),
) -> Any:
    try:
        return query.config()
    except EvalCenterError as exc:
        return _error(exc)


@router.put("/api/eval/config")
@inject
def eval_save_config(
    body: ConfigBody,
    command: EvalCenterCommand = Depends(Provide[Container.eval_center_command]),
) -> Any:
    try:
        return command.save_config(body.content)
    except EvalCenterError as exc:
        return _error(exc)


@router.get("/api/eval/runs")
@inject
def eval_runs(
    query: EvalCenterQuery = Depends(Provide[Container.eval_center_query]),
) -> Any:
    try:
        return query.runs()
    except EvalCenterError as exc:
        return _error(exc)


@router.get("/api/eval/run/{run_id}")
@inject
def eval_run_detail(
    run_id: str, query: EvalCenterQuery = Depends(Provide[Container.eval_center_query])
) -> Any:
    try:
        return query.run_detail(run_id)
    except EvalCenterError as exc:
        return _error(exc)


@router.get("/api/eval/run/{run_id}/report")
@inject
def eval_run_report(
    run_id: str, query: EvalCenterQuery = Depends(Provide[Container.eval_center_query])
) -> Any:
    try:
        return query.report(run_id)
    except EvalCenterError as exc:
        return _error(exc)


@router.get("/api/eval/run/{run_id}/unit")
@inject
def eval_unit_results(
    run_id: str,
    unit: str,
    query: EvalCenterQuery = Depends(Provide[Container.eval_center_query]),
) -> Any:
    try:
        return query.unit_results(run_id, unit)
    except EvalCenterError as exc:
        return _error(exc)


@router.get("/api/eval/run/{run_id}/raw")
@inject
def eval_raw_judgments(
    run_id: str,
    unit: str,
    dim: str,
    query: EvalCenterQuery = Depends(Provide[Container.eval_center_query]),
) -> Any:
    try:
        return query.raw_judgments(run_id, unit, dim)
    except EvalCenterError as exc:
        return _error(exc)
