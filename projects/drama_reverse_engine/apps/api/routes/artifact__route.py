
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query

from libs.application.queries.artifact__query import ArtifactQuery
from libs.domain.errors.workspace__error import PathEscapeError

router = APIRouter()


@router.get("/api/artifacts")
@inject
def read_artifact(rel_path: str = Query(...), query: ArtifactQuery = Depends(Provide["artifact_query"])):
    try:
        content = query.read_text(rel_path)
    except PathEscapeError:
        raise HTTPException(status_code=400, detail="path escapes workspace")
    if content is None:
        raise HTTPException(status_code=404, detail="artifact not found or not a text type")
    return {"rel_path": rel_path, "content": content}


@router.get("/api/episodes/shot-files")
@inject
def shot_files(episode_rel_dir: str = Query(...), query: ArtifactQuery = Depends(Provide["artifact_query"])):
    return {"episode_rel_dir": episode_rel_dir, "shot_files": query.shot_files(episode_rel_dir)}
