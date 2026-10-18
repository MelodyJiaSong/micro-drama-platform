"""草稿条的用户审核（follow-up 265）：POST 写入「通过 / 不通过」，通过的草稿才能用来出正式条。"""
from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.api.container import Container
from libs.application.commands.shot_take__command import ShotTakeCommand

router = APIRouter()


class VerdictBody(BaseModel):
    take_path: str
    verdict: str


@router.post("/api/shot-take/verdict")
@inject
def take_verdict(body: VerdictBody, command: ShotTakeCommand = Depends(Provide[Container.shot_take_command])) -> dict[str, str]:
    return {"take_path": body.take_path, "review_status": command.verdict(body.take_path, body.verdict)}
