
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse

from libs.application.commands.export__command import ExportCommand
from libs.domain.errors.export__error import ExportArtifactMissingError, UnknownExportSelectionError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace

router = APIRouter()


@router.get("/api/episodes/export-artifacts")
@inject
def export_artifacts(
    episode_rel_dir: str,
    artifacts: str,
    format: str = "md",
    command: ExportCommand = Depends(Provide["export_command"]),
    workspace: SafeWorkspace = Depends(Provide["workspace"]),
):
    try:
        result = command.export_artifacts(episode_rel_dir, [a for a in artifacts.split(",") if a], format)
    except UnknownExportSelectionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ExportArtifactMissingError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return FileResponse(workspace.resolve(result.rel_path), filename=result.filename,
                        media_type=result.media_type)


@router.post("/api/dramas/{drama_id}/export")
@inject
def export_drama(
    drama_id: str,
    command: ExportCommand = Depends(Provide["export_command"]),
    workspace: SafeWorkspace = Depends(Provide["workspace"]),
):
    rel = command.export_drama(drama_id, f"{drama_id}/export/{drama_id}_deliverable.zip")
    return FileResponse(workspace.resolve(rel), filename=f"{drama_id}_deliverable.zip")
