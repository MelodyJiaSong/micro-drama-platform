"""Frozen request → CLI invocation, and CLI output → port value objects, for `DreaminaCliBackend`.

Also holds the backend's side-channel results (`DreaminaHealthReport`, `DreaminaDownloadSet`) and
`DreaminaBackendError`, which `download()` raises because the port's return type has no error slot.
"""
from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from libs.application.mappers.dreamina__mapper import DreaminaMapper
from libs.common.enums import BackendKind, GenerationKind, PauseReason, PreparingStep, RefKind
from libs.common.paths import RepoSandbox, is_reparse_point
from libs.domain.repositories.generation_backend__repository import BackendHealth, DownloadedFile
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.daos.dreamina_result__dao import DreaminaResultDao, DreaminaTaskDao

IMAGE_EXTS: tuple[str, ...] = (".png", ".jpg", ".jpeg", ".webp")
MAX_REFERENCE_IMAGES: int = 10
MAX_DOWNLOAD_FILES: int = 10
_HASH_CHUNK: int = 1 << 20


class DreaminaBackendError(Exception):
    """`retryable` tells the application whether `retries.download` applies before pausing with `reason`."""

    def __init__(self, reason: PauseReason, retryable: bool, message: str) -> None:
        super().__init__(f"{reason.value}: {message}")
        self.reason = reason
        self.retryable = retryable
        self.message = message


@dataclass(frozen=True)
class DreaminaHealthReport:
    health: BackendHealth
    logged_in: bool | None
    balance: int | None
    vip_level: str | None
    version_warning: bool


@dataclass(frozen=True)
class DreaminaDownloadSet:
    """Every image of one task, name-sorted. Only `files[0]` carries `credits_charged` (a task total, never per file)."""

    submit_id: str
    files: tuple[DownloadedFile, ...]
    credits_charged: int | None


@dataclass(frozen=True)
class CliInvocation:
    prompt: str
    model_version: str
    ratio: str
    resolution_type: str
    images: tuple[Path, ...]


@dataclass(frozen=True)
class PlanRejection:
    step: PreparingStep
    reason: PauseReason
    message: str


def plan_invocation(frozen: FrozenRequest, sandbox: RepoSandbox, verify_hashes: bool) -> CliInvocation | PlanRejection:
    """Checks run in preparing-step order, so the first rejection names the earliest failing step."""
    request = frozen.request
    params = request.params
    if frozen.backend is not BackendKind.CLI or request.kind is not GenerationKind.IMAGE or params is None:
        return _cli_error(PreparingStep.SET_PARAMS, f"dreamina 只执行路由到 cli 的图片请求，实际为 {request.kind}/{frozen.backend}")
    if request.entity_references:
        names = "、".join(ref.name for ref in request.entity_references)
        return _cli_error(PreparingStep.SET_PARAMS, f"cli 图片请求不能带主体参考：{names}")
    model_version = DreaminaMapper.model_version(params.model)
    ratio = DreaminaMapper.ratio(params.ratio)
    resolution_type = DreaminaMapper.resolution_type(params.resolution)
    if model_version is None or ratio is None or resolution_type is None:
        return _cli_error(
            PreparingStep.SET_PARAMS,
            f"参数无法映射到 dreamina：model={params.model!r} ratio={params.ratio!r} resolution={params.resolution!r}",
        )
    references = request.upload_references
    if len(references) > MAX_REFERENCE_IMAGES:
        return _cli_error(PreparingStep.UPLOAD, f"image2image 最多 {MAX_REFERENCE_IMAGES} 张参考图，实际 {len(references)} 张")
    images: list[Path] = []
    for ref in references:
        located = _locate(ref, sandbox, verify_hashes)
        if isinstance(located, PlanRejection):
            return located
        images.append(located)
    if "\x00" in request.prompt:
        return _cli_error(PreparingStep.FILL, "prompt 含 NUL 字符，无法作为命令行参数传递")
    return CliInvocation(request.prompt, model_version, ratio, resolution_type, tuple(images))


def vet_downloads(result: DreaminaResultDao, download_dir: Path) -> tuple[Path, ...]:
    """The job dir is emptied before `query_result`, so every entry in it came from this call."""
    irregular = sorted(entry.name for entry in download_dir.iterdir() if is_reparse_point(entry) or not entry.is_file())
    if irregular:
        raise DreaminaBackendError(PauseReason.CLI_ERROR, False, "下载目录里出现非普通文件：" + "、".join(irregular[:5]))
    files = tuple(path for path in result.downloaded_files if path.parent == download_dir)
    if not files:
        raise DreaminaBackendError(
            PauseReason.DOWNLOAD_FAILED, True, f"query_result 没有下载到文件（gen_status={result.gen_status!r}）"
        )
    if len(files) > MAX_DOWNLOAD_FILES:
        raise DreaminaBackendError(PauseReason.CLI_ERROR, False, f"下载到 {len(files)} 个文件，超过上限 {MAX_DOWNLOAD_FILES}")
    foreign = [path.name for path in files if path.suffix.lower() not in IMAGE_EXTS]
    if foreign:
        raise DreaminaBackendError(PauseReason.CLI_ERROR, False, "下载到非图片文件：" + "、".join(foreign[:5]))
    return files


def describe_file(path: Path, credits_charged: int | None) -> DownloadedFile:
    size, digest = hash_file(path)
    return DownloadedFile(temp_path=str(path), size=size, sha256=digest, credits_charged=credits_charged)


def hash_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_HASH_CHUNK), b""):
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


def find_task(tasks: Sequence[DreaminaTaskDao], submit_id: str) -> DreaminaTaskDao | None:
    return next((task for task in tasks if task.submit_id == submit_id), None)


def _locate(ref: ReferenceItem, sandbox: RepoSandbox, verify_hash: bool) -> Path | PlanRejection:
    if ref.kind is not RefKind.IMAGE:
        return _cli_error(PreparingStep.UPLOAD, f"参考项 {ref.name} 的类型是 {ref.kind}，dreamina 只接受图片")
    verdict = sandbox.check_read(ref.resolved_path or "")
    if not verdict.ok or verdict.path is None:
        return _cli_error(PreparingStep.UPLOAD, f"参考项 {ref.name} 的路径被沙箱拒绝（{verdict.violation}）")
    path = verdict.path
    if not path.is_file():
        return PlanRejection(PreparingStep.UPLOAD, PauseReason.INPUTS_CHANGED, f"参考项 {ref.name} 的文件已不存在：{ref.resolved_path}")
    if path.suffix.lower() not in IMAGE_EXTS or "," in str(path):
        return _cli_error(PreparingStep.UPLOAD, f"参考项 {ref.name} 无法经 --images 传递（须为图片且路径不含逗号）：{ref.resolved_path}")
    if verify_hash and _sha256_or_none(path) != ref.sha256:
        return PlanRejection(PreparingStep.UPLOAD, PauseReason.INPUTS_CHANGED, f"参考项 {ref.name} 在确认后被改动：{ref.resolved_path}")
    return path


def _sha256_or_none(path: Path) -> str | None:
    try:
        return hash_file(path)[1]
    except OSError:
        return None


def _cli_error(step: PreparingStep, message: str) -> PlanRejection:
    return PlanRejection(step, PauseReason.CLI_ERROR, message)
