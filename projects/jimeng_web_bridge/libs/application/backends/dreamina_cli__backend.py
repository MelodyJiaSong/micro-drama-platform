from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from libs.application.backends.dreamina_cli_mapping import (
    CliInvocation,
    DreaminaBackendError,
    DreaminaDownloadSet,
    DreaminaHealthReport,
    PlanRejection,
    describe_file,
    find_task,
    plan_invocation,
    vet_downloads,
)
from libs.application.mappers.dreamina__mapper import DreaminaMapper
from libs.common.enums import PREPARING_STEP_ORDER, BackendKind, PauseReason, PreparingStep, RemoteStatus
from libs.common.paths import RepoSandbox, is_reparse_point, segment_violation
from libs.domain.repositories.generation_backend__repository import (
    BackendHealth,
    DownloadedFile,
    PollResult,
    PrepareResult,
    SubmitOutcome,
)
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.infrastructure.clients.dreamina_cli__client import DreaminaCliClient
from libs.infrastructure.daos.dreamina_result__dao import DreaminaSubmitDao
from libs.infrastructure.errors.dreamina_cli__error import DreaminaCliError

CHECK_UNAVAILABLE: str = "cli_unavailable"
CHECK_VERSION_FAILED: str = "cli_version_failed"
CHECK_VERSION_UNKNOWN: str = "cli_version_unknown"
CHECK_VERSION_BELOW_MIN: str = "cli_version_below_min"
CHECK_NOT_LOGGED_IN: str = "cli_not_logged_in"
CHECK_COMPLIANCE_REQUIRED: str = "cli_compliance_confirmation_required"
CHECK_CREDIT_FAILED: str = "cli_credit_failed"
WARNING_CHECKS: frozenset[str] = frozenset({CHECK_VERSION_UNKNOWN, CHECK_VERSION_BELOW_MIN})
LIST_TASK_LIMIT: int = 5

_QUEUE_CHECKS: dict[PauseReason, str] = {
    PauseReason.CLI_LOGIN_REQUIRED: CHECK_NOT_LOGGED_IN,
    PauseReason.COMPLIANCE_CONFIRMATION_REQUIRED: CHECK_COMPLIANCE_REQUIRED,
}
_T = TypeVar("_T")


class DreaminaCliBackend:
    """`GenerationBackend` port over the official `dreamina` CLI (spec v2 FR-38..FR-41, §8 divergence 6).

    Blocking like the client it wraps: the application calls it from its executor threads. It never
    retries; retry policy (zero retries for submit) belongs to the application. Beyond the port it
    offers `inspect()` (login / balance / version warning) and `download_all()` (multi-image tasks).
    """

    def __init__(self, client: DreaminaCliClient, sandbox: RepoSandbox, tmp_dir: Path, min_version: str) -> None:
        self._client = client
        self._sandbox = sandbox
        self._tmp_dir = tmp_dir
        self._min_version = min_version

    @property
    def kind(self) -> BackendKind:
        return BackendKind.CLI

    def health(self) -> BackendHealth:
        return self.inspect().health

    def inspect(self) -> DreaminaHealthReport:
        checks: list[str] = []
        reasons: list[PauseReason] = []
        version = _probe(self._client.version, checks, reasons, CHECK_VERSION_FAILED)
        credit = _probe(self._client.user_credit, checks, reasons, CHECK_CREDIT_FAILED)
        if version is not None:
            below = DreaminaMapper.version_below(version.version, self._min_version)
            if below is not False:
                checks.append(CHECK_VERSION_UNKNOWN if below is None else CHECK_VERSION_BELOW_MIN)
        unique = tuple(dict.fromkeys(checks))
        pause_reason = reasons[0] if reasons else None
        health = BackendHealth(
            ok=all(check in WARNING_CHECKS for check in unique),
            failed_checks=unique,
            version=None if version is None else (version.version or None),
            pause_reason=pause_reason,
        )
        if credit is not None:
            logged_in: bool | None = True
        else:
            logged_in = False if pause_reason is PauseReason.CLI_LOGIN_REQUIRED else None
        return DreaminaHealthReport(
            health=health,
            logged_in=logged_in,
            balance=None if credit is None else credit.total_credit,
            vip_level=None if credit is None else credit.vip_level,
            version_warning=any(check in WARNING_CHECKS for check in unique),
        )

    def prepare(self, job_id: str, request: FrozenRequest, until: PreparingStep) -> PrepareResult:
        verify = _order(until) >= _order(PreparingStep.UPLOAD)
        plan = plan_invocation(request, self._sandbox, verify_hashes=verify)
        if isinstance(plan, PlanRejection) and _order(plan.step) <= _order(until):
            return PrepareResult(plan.step, None, (), plan.reason, plan.message)
        return PrepareResult(reached_step=until, page_estimated_credits=None, screenshot_names=())

    def submit(self, job_id: str, request: FrozenRequest) -> SubmitOutcome:
        plan = plan_invocation(request, self._sandbox, verify_hashes=False)
        if isinstance(plan, PlanRejection):
            return SubmitOutcome(None, PauseReason.CLI_ERROR, plan.message)
        try:
            submitted = self._generate(plan)
        except DreaminaCliError as error:
            if DreaminaMapper.is_transient(error.kind):
                return SubmitOutcome(None, PauseReason.SUBMIT_UNCONFIRMED, _describe(error))
            return SubmitOutcome(None, DreaminaMapper.failure_reason(error.kind), _describe(error))
        except OSError as error:
            return SubmitOutcome(None, PauseReason.CLI_ERROR, f"无法启动 dreamina：{error}")
        return SubmitOutcome(platform_task_id=submitted.submit_id)

    def poll(self, platform_task_id: str) -> PollResult:
        try:
            tasks = self._client.list_task(limit=LIST_TASK_LIMIT, submit_id=platform_task_id)
        except DreaminaCliError as error:
            failure = None if DreaminaMapper.is_transient(error.kind) else DreaminaMapper.failure_reason(error.kind)
            return PollResult(RemoteStatus.UNKNOWN, None, failure, _describe(error))
        except OSError as error:
            return PollResult(RemoteStatus.UNKNOWN, None, PauseReason.CLI_ERROR, f"无法启动 dreamina：{error}")
        task = find_task(tasks, platform_task_id)
        if task is None:
            return PollResult(RemoteStatus.GENERATING, None, None, f"list_task 没有 submit_id={platform_task_id} 的记录，按生成中处理")
        status = DreaminaMapper.remote_status(task.gen_status)
        if status is RemoteStatus.FAILED:
            return PollResult(status, None, PauseReason.CLI_ERROR, task.fail_reason or "dreamina 报告任务失败（无 fail_reason）")
        if DreaminaMapper.is_known_status(task.gen_status):
            return PollResult(status, None)
        return PollResult(status, None, None, f"未识别的 gen_status={task.gen_status!r}，按生成中处理")

    def download(self, job_id: str, platform_task_id: str) -> DownloadedFile:
        return self.download_all(job_id, platform_task_id).files[0]

    def download_all(self, job_id: str, platform_task_id: str) -> DreaminaDownloadSet:
        download_dir = self._fresh_download_dir(job_id)
        try:
            result = self._client.query_result(platform_task_id, download_dir)
        except DreaminaCliError as error:
            transient = DreaminaMapper.is_transient(error.kind)
            reason = PauseReason.DOWNLOAD_FAILED if transient else DreaminaMapper.failure_reason(error.kind)
            raise DreaminaBackendError(reason, transient, _describe(error)) from error
        except OSError as error:
            raise DreaminaBackendError(PauseReason.DOWNLOAD_FAILED, True, f"query_result 执行失败：{error}") from error
        if DreaminaMapper.remote_status(result.gen_status) is RemoteStatus.FAILED:
            raise DreaminaBackendError(PauseReason.CLI_ERROR, False, result.fail_reason or "dreamina 报告任务失败（无 fail_reason）")
        paths = vet_downloads(result, download_dir)
        credits_charged = self._credits_charged(platform_task_id)
        try:
            files = tuple(describe_file(path, credits_charged if index == 0 else None) for index, path in enumerate(paths))
        except OSError as error:
            raise DreaminaBackendError(PauseReason.DOWNLOAD_FAILED, True, f"读取下载文件失败：{error}") from error
        return DreaminaDownloadSet(submit_id=platform_task_id, files=files, credits_charged=credits_charged)

    def _generate(self, plan: CliInvocation) -> DreaminaSubmitDao:
        if plan.images:
            return self._client.image2image(plan.images, plan.prompt, plan.model_version, plan.ratio, plan.resolution_type)
        return self._client.text2image(plan.prompt, plan.model_version, plan.ratio, plan.resolution_type)

    def _credits_charged(self, submit_id: str) -> int | None:
        try:
            task = find_task(self._client.list_task(limit=LIST_TASK_LIMIT, submit_id=submit_id), submit_id)
        except (DreaminaCliError, OSError):
            return None
        return None if task is None else task.credit_count

    def _fresh_download_dir(self, job_id: str) -> Path:
        violation = "separator" if "/" in job_id or "\\" in job_id else segment_violation(job_id)
        if violation is not None:
            raise DreaminaBackendError(PauseReason.CLI_ERROR, False, f"job_id 不能用作临时目录名（{violation}）")
        target = self._tmp_dir / job_id
        if is_reparse_point(target):
            raise DreaminaBackendError(PauseReason.CLI_ERROR, False, f"临时目录 {target.name} 是链接，拒绝使用")
        try:
            if target.exists():
                shutil.rmtree(target)
            target.mkdir(parents=True)
        except OSError as error:
            raise DreaminaBackendError(PauseReason.DOWNLOAD_FAILED, True, f"无法准备临时目录：{error}") from error
        return target


def _probe(call: Callable[[], _T], checks: list[str], reasons: list[PauseReason], fallback: str) -> _T | None:
    try:
        return call()
    except DreaminaCliError as error:
        reason = DreaminaMapper.queue_reason(error.kind)
        if reason is None:
            checks.append(fallback)
        else:
            reasons.append(reason)
            checks.append(_QUEUE_CHECKS[reason])
    except OSError:
        checks.append(CHECK_UNAVAILABLE)
    except (ValueError, TypeError):
        checks.append(fallback)
    return None


def _describe(error: DreaminaCliError) -> str:
    tail = error.output_tail.strip()
    return f"{error}：{tail}" if tail else str(error)


def _order(step: PreparingStep) -> int:
    return PREPARING_STEP_ORDER.index(step)
