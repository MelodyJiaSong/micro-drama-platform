from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from apps.api.container import Container
from libs.application.commands.character_interview__command import CharacterInterviewCommand
from libs.application.queries.writers_room__query import WritersRoomQuery

router = APIRouter(prefix="/api/writers-room")


class AnswerBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    character: str
    question_id: str
    choice: str
    note: str = Field(default="", max_length=5000)
    expected_revision: int = Field(ge=0)


@router.get("")
@inject
def list_rooms(query: WritersRoomQuery = Depends(Provide[Container.writers_room_query])) -> list[dict]:
    return query.list()


@router.get("/{slug}")
@inject
def detail(slug: str, query: WritersRoomQuery = Depends(Provide[Container.writers_room_query])) -> dict:
    return query.detail(slug)


@router.put("/{slug}/answers")
@inject
def answer(slug: str, body: AnswerBody, command: CharacterInterviewCommand = Depends(Provide[Container.character_interview_command])) -> dict:
    return command.answer(slug, body.character, body.question_id, {"choice": body.choice, "note": body.note}, body.expected_revision)
