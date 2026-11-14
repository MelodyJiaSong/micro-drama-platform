from typing import Annotated, Literal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field

from projects.suno_browser_service.apps.api.container import Container
from projects.suno_browser_service.libs.application.commands.job__command import JobCommand
from projects.suno_browser_service.libs.application.dtos.job__dto import JobCdto, JobQdto
from projects.suno_browser_service.libs.application.queries.auth__query import AuthQuery
from projects.suno_browser_service.libs.application.queries.job__query import JobQuery
from projects.suno_browser_service.libs.application.queries.capability__query import CapabilityQuery
from projects.suno_browser_service.libs.application.commands.asset__command import AssetCommand
from projects.suno_browser_service.libs.common.generation import GenerationRequest

bearer = HTTPBearer(auto_error=False, description="本机服务访问令牌（不是 Suno 密码）。start.ps1 初始化；MCP/CLI 自动读取，HTTP 用 Authorization: Bearer <token>。")


@inject
def authorize(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
              auth: Annotated[AuthQuery, Depends(Provide[Container.auth])]) -> None:
    auth.verify(f"Bearer {credentials.credentials}" if credentials else None)


router = APIRouter(prefix="/v1", dependencies=[Depends(authorize)], responses={
    401: {"description": "服务令牌缺失或错误；不操作 Suno。"},
    409: {"description": '业务冲突，返回 {"error":{"code":"...","message":"..."}}；读取 code 后处理，不能盲目换键重试。'},
    422: {"description": "参数错误：schema 错误返回 detail 数组，业务校验返回 error.code/message。修正后先 plan。"},
})


CreateBody = GenerationRequest


class ResumeBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    song_urls: list[str] = Field(default_factory=list, max_length=2, description="最多两条已确认属于本任务的 Suno 歌曲 URL。未知提交必填；已有链接或确定尚未提交可为空。", examples=[["https://suno.com/song/00000000-0000-4000-8000-000000000001"]])
    recollect: bool = Field(default=False, description="已提交但结果未知或认领有误的任务：只到库里按标题 / Sounds prompt 重新认领两条，不填表、不点 Create、不收费；不能与 song_urls 同用。")


@router.post("/jobs", response_model=JobQdto, status_code=202, tags=["任务"], summary="排队生成与官方下载（可能收费）")
@inject
def submit(body: CreateBody, idempotency_key: Annotated[str, Header(description="同一次生成的固定键，1–128 位 ASCII 字母、数字或 _.:-。同键同请求返回原任务，不重复 Create；不同参数返回 409。")],
           command: Annotated[JobCommand, Depends(Provide[Container.command])]) -> JobQdto:
    """先 capabilities → plan，再提交。202 仅表示已接受，轮询返回 id，直到 completed 或需处理状态。

    执行时使用付费 Suno 账号，上传参考并消耗生成/下载额度。网络超时沿用原键。
    全局暂停时仍可排队，但不会执行；不要为结果未知的任务另建新键。
    """
    return command.submit(idempotency_key, JobCdto(**body.model_dump(exclude_none=True)))


@router.get("/capabilities", tags=["发现与预检"], summary="发现参数、上传限制与实测边界")
@inject
def capabilities(query: Annotated[CapabilityQuery, Depends(Provide[Container.capabilities])]) -> dict:
    """只读本机，返回 request_schema、modes、options、uploads、automation_paused 和 evidence。implemented 不等于 live_verified；不访问 Suno。"""
    return query.get()


@router.post("/plan", tags=["发现与预检"], summary="预检请求（不生成、不收费）")
@inject
def plan(body: GenerationRequest, query: Annotated[CapabilityQuery, Depends(Provide[Container.capabilities])]) -> dict:
    """校验请求 schema 和本机参考哈希，返回 schema_valid、request、references、warnings、暂停状态。不会创建 Job 或打开浏览器；目标目录和媒体模式组合在提交时仍校验。"""
    return query.plan(body)


@router.post("/assets", status_code=201, tags=["参考素材"], summary="保存本机参考文件", responses={413: {"description": "单文件超过 64 MiB，未保存资产。"}})
@inject
def upload_asset(command: Annotated[AssetCommand, Depends(Provide[Container.assets])],
                 file: UploadFile = File(..., description="音频、图片或视频，最大 64 MiB；扩展名见 capabilities，ffprobe 校验真实媒体。"), rights_confirmed: bool = Form(False, description="明确有权使用时设 true；否则 Suno 要求权利确认时暂停。")) -> dict:
    """返回 id（SHA256）、name、kind、bytes、duration_seconds、rights_confirmed 等元信息。

    将 id 放入 references[].asset_id。此步只存本机，不上传 Suno；相同内容复用同一资产。
    """
    return command.upload(file.filename or "", file.file, rights_confirmed)


@router.get("/assets/{asset_id}", tags=["参考素材"], summary="查询参考元信息并核对哈希", responses={404: {"description": "资产未上传或不存在。"}})
@inject
def asset(asset_id: str, command: Annotated[AssetCommand, Depends(Provide[Container.assets])]) -> dict:
    """asset_id 是上传返回的 64 位 SHA256；返回元信息，不返回媒体文件。内容改变时返回 409 asset_changed。"""
    return command.get(asset_id)


@router.get("/jobs", response_model=list[JobQdto], tags=["任务"], summary="列出最近 100 个本机任务")
@inject
def list_jobs(query: Annotated[JobQuery, Depends(Provide[Container.query])]) -> list[JobQdto]:
    """直接返回 Job 数组，包含暂停/未知任务；从本机数据库读取，不刷新 Suno 歌曲库。"""
    return query.list()


@router.get("/jobs/{job_id}", response_model=JobQdto, tags=["任务"], summary="查询任务进度、结果与下一步", responses={404: {"description": "任务不存在。"}})
@inject
def get_job(job_id: str, query: Annotated[JobQuery, Depends(Provide[Container.query])]) -> JobQdto:
    """Job 包含 status、request、applied_options（网页已读回选项）、next_action、error、song_urls、files。

    files 每项有 name/bytes/sha256/song_url；created_at/updated_at 为 UTC ISO 时间。
    queued/preparing/submitting/waiting/downloading 时继续轮询；completed 后取文件。
    needs_login/needs_attention/uncertain 时读 error 与 next_action，勿另建任务。
    """
    return query.get(job_id)


@router.post("/jobs/{job_id}/cancel", response_model=JobQdto, tags=["任务"], summary="取消尚未提交的任务（不访问 Suno）", responses={404: {"description": "任务不存在。"}})
@inject
def cancel(job_id: str, command: Annotated[JobCommand, Depends(Provide[Container.command])]) -> JobQdto:
    """只允许 queued/needs_login/needs_attention 且从未点过 Create 的任务；已提交任务返回 409 job_active。"""
    return command.cancel(job_id)


@router.post("/jobs/{job_id}/resume", response_model=JobQdto, status_code=202, tags=["任务"], summary="修复原因后恢复原任务", responses={404: {"description": "任务不存在。"}})
@inject
def resume(job_id: str, body: ResumeBody,
           command: Annotated[JobCommand, Depends(Provide[Container.command])]) -> JobQdto:
    """仅允许 needs_login/needs_attention/uncertain。未知提交必须提供确认的 song_urls，只补下载。

    确定尚未提交的任务恢复后会首次 Create，可能收费。已知歌曲的下载失败可传空数组。
    此接口不清除验证码暂停；执行中或 completed 返回 409 job_active。
    """
    return command.resume(job_id, body.song_urls, body.recollect)


@router.get("/jobs/{job_id}/files/{name}", tags=["任务"], summary="下载本机已登记音频（不再次访问 Suno）", responses={200: {"content": {"audio/mpeg": {"schema": {"type": "string", "format": "binary"}}, "audio/wav": {"schema": {"type": "string", "format": "binary"}}}, "description": "二进制音频；将大小/SHA256 与 Job.files 元信息核对。"}, 404: {"description": "任务、已登记文件或实际文件不存在。"}}, response_class=FileResponse)
@inject
def file(job_id: str, name: str, query: Annotated[JobQuery, Depends(Provide[Container.query])]) -> FileResponse:
    """name 必须原样取自 Job.files[].name，不能传本机路径。所有下载同样需要 Bearer token。"""
    path = query.file(job_id, name)
    return FileResponse(path, filename=name, media_type="audio/wav" if name.endswith(".wav") else "audio/mpeg")
