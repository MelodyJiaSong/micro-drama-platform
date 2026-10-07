from __future__ import annotations

from typing import Any, Literal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from apps.api.container import Container
from libs.application.commands.episode_workflow__command import EpisodeWorkflowCommand
from libs.application.dtos.episode_workflow__dto import EpisodeWorkflowCdto, EpisodeWorkflowQdto
from libs.application.queries.episode_workflow__query import EpisodeWorkflowQuery

router = APIRouter()


class ChangeBody(BaseModel):
    episode_path: str
    module: Literal["story", "filming", "prompts"]
    operation: Literal["save", "approve", "compile"]
    expected: str
    source: str | None = None
    content: dict[str, Any] | None = None


@router.get("/api/episode-workflow")
@inject
def read_workflow(episode_path: str = Query(...),
                  query: EpisodeWorkflowQuery = Depends(Provide[Container.episode_workflow_query])) -> EpisodeWorkflowQdto:
    return query.read(episode_path)


@router.post("/api/episode-workflow")
@inject
def change_workflow(body: ChangeBody,
                    command: EpisodeWorkflowCommand = Depends(Provide[Container.episode_workflow_command])) -> EpisodeWorkflowCdto:
    return command.change(body.episode_path, body.module, body.operation, body.expected, body.source, body.content)
