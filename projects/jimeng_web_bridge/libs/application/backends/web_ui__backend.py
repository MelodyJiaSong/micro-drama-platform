"""`GenerationBackend` port over the logged-in 即梦 web page (spec v2 FR-18, FR-25..FR-37, §8 divergence 6).

Blocking facade: every call holds the BrowserActor's exclusive lock for its whole UI sequence and is meant to
run on an executor thread. Beyond the port it offers `check_before_submit` (pre-click checks, no click),
`recover_browser` (FR-37 rebuild + canary) and `negative_prompt_entered` (sidecar input).

`submit` outcome contract (U4 report):
- `platform_task_id` set → clicked and accepted.
- `rejection in POST_CLICK_REJECTIONS` → clicked; never click again (FR-33). An unknown result is
  `SUBMIT_UNCONFIRMED`.
- any other `rejection` → NOT clicked (queue-level reason, fill_mismatch, inputs_changed, …).
- `platform_task_id is None and rejection is None` → NOT clicked, wait and retry; `message` starts `not_now:`.

`prepare` success `message` carries the negative prompt side channel: `NEGATIVE_ENTERED`, `NEGATIVE_OMITTED`,
or None when the request has no negative prompt.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from libs.common.enums import PREPARING_STEPS_BY_BACKEND, BackendKind, GenerationKind, PauseReason, PreparingStep, RemoteStatus
from libs.common.paths import RepoSandbox, is_reparse_point, segment_violation
from libs.domain.repositories.generation_backend__repository import (
    BackendHealth,
    DownloadedFile,
    PollResult,
    PrepareResult,
    SubmitOutcome,
)
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.clients.jimeng_browser__client import BrowserSession, JimengBrowserClient
from libs.infrastructure.clients.jimeng_page__map import (
    MODEL_DISPLAY_NAMES,
    OMNI_REFERENCE_MODE,
    VIDEO_CREATION_TYPE,
    JimengPageMap,
)
from libs.infrastructure.clients.jimeng_page__steps import detect_blocker
from libs.infrastructure.clients.jimeng_page_canary__steps import run_canary
from libs.infrastructure.clients.jimeng_page_fill__steps import fill_editor, fill_negative, read_editor
from libs.infrastructure.clients.jimeng_page_params__steps import params_diff, read_params, reset_composer, set_params
from libs.infrastructure.clients.jimeng_page_record__steps import download_record, reload_history_view
from libs.infrastructure.clients.jimeng_page_submit__steps import capture_preview, click_generate, pre_click_state
from libs.infrastructure.clients.jimeng_page_upload__steps import remove_upload, upload_file, uploads_mismatch
from libs.infrastructure.clients.jimeng_page_verify__steps import (
    build_fill_segments,
    compare_snapshot,
    expected_snapshot,
    prompt_prefix,
)
from libs.infrastructure.daos.jimeng_history__dao import HistoryRecordDao, ParseOutcome
from libs.infrastructure.daos.jimeng_page__dao import (
    ComposerParamsDao,
    EditorSnapshotDao,
    FillSegmentDao,
    MentionMarkerDao,
    SubmitCaptureDao,
    UploadItemDao,
)
from libs.infrastructure.errors.jimeng_browser__error import (
    BrowserCommandTimeoutError,
    BrowserLaunchError,
    BrowserLostError,
    BrowserNotStartedError,
    FillPlanError,
    PageStepError,
    StepFailureKind,
    WebBackendError,
)
from libs.infrastructure.readers.jimeng_history__reader import STATUS_KEYS, JimengHistoryReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter

NOT_NOW_PREFIX: str = "not_now:"
CONCURRENCY_LIMIT_PRE_CLICK: str = f"{NOT_NOW_PREFIX}concurrency_limit_pre_click"
GENERATE_DISABLED_PRE_CLICK: str = f"{NOT_NOW_PREFIX}generate_button_disabled"
NEGATIVE_ENTERED: str = "negative_prompt=entered"
NEGATIVE_OMITTED: str = "negative_prompt=omitted_no_field"
POST_CLICK_REJECTIONS: frozenset[PauseReason] = frozenset(
    {PauseReason.SUBMIT_REJECTED, PauseReason.SUBMIT_UNCONFIRMED, PauseReason.MODERATION_REJECT, PauseReason.REAL_FACE_REJECTED}
)
STEP_REASONS: dict[StepFailureKind, PauseReason] = {
    StepFailureKind.CAPTCHA_OR_RISK: PauseReason.CAPTCHA_OR_RISK_POPUP,
    StepFailureKind.LOGIN_REQUIRED: PauseReason.LOGIN_EXPIRED,
    StepFailureKind.INSUFFICIENT_CREDIT: PauseReason.INSUFFICIENT_CREDIT,
    StepFailureKind.SELECTOR_MISSING: PauseReason.PAGE_CONTRACT_BROKEN,
    StepFailureKind.PAGE_ERROR: PauseReason.PAGE_CONTRACT_BROKEN,
    StepFailureKind.RESPONSE_TIMEOUT: PauseReason.PAGE_CONTRACT_BROKEN,
    StepFailureKind.UPLOAD_REJECTED: PauseReason.UPLOAD_REJECTED,
    StepFailureKind.REAL_FACE_REJECTED: PauseReason.REAL_FACE_REJECTED,
    StepFailureKind.UPLOAD_TIMEOUT: PauseReason.STEP_FAILED,
    StepFailureKind.READBACK_MISMATCH: PauseReason.STEP_FAILED,
    StepFailureKind.ENTITY_FORM_FAILED: PauseReason.STEP_FAILED,
    StepFailureKind.RECORD_NOT_FOUND: PauseReason.DOWNLOAD_FAILED,
    StepFailureKind.DOWNLOAD_FAILED: PauseReason.DOWNLOAD_FAILED,
}
_BLOCKER_CAN_EXPLAIN: frozenset[PauseReason] = frozenset(
    {PauseReason.PAGE_CONTRACT_BROKEN, PauseReason.STEP_FAILED, PauseReason.FILL_MISMATCH}
)
_BROWSER_FAILURES = (PageStepError, BrowserLostError, BrowserNotStartedError, BrowserCommandTimeoutError)
_MODERATION = re.compile(r"审核|违规|社区规范")
_REAL_FACE = re.compile(r"真人人脸")
_HASH_CHUNK: int = 1 << 20
_INFLIGHT_FRESH_S: float = 10.0
_WEB_STEPS: tuple[PreparingStep, ...] = PREPARING_STEPS_BY_BACKEND[BackendKind.WEB]


@dataclass(frozen=True)
class _ComposerPlan:
    params: ComposerParamsDao
    segments: tuple[FillSegmentDao, ...]
    expected: EditorSnapshotDao
    prefix: str
    upload_names: tuple[str, ...]


@dataclass
class _Composer:
    job_id: str
    fingerprint: str
    epoch: int
    done: set[PreparingStep] = field(default_factory=set)
    estimate: int | None = None
    screenshots: tuple[str, ...] = ()
    negative: str | None = None


@dataclass
class _TaskView:
    status: RemoteStatus | None = None
    progress_pct: int | None = None
    fail_msg: str = ""
    prompt_text: str | None = None
    video_size: int | None = None
    observed_at: float = 0.0


class _StepStop(Exception):
    def __init__(self, reason: PauseReason, message: str) -> None:
        super().__init__(message)
        self.reason = reason
        self.message = message


class WebUiBackend:
    def __init__(
        self,
        client: JimengBrowserClient,
        artifacts: ArtifactWriter,
        config: GlobalConfig,
        repo_root: Path,
        tmp_dir: Path,
        reader: JimengHistoryReader | None = None,
        poll_stale_s: float = 30.0,
        poll_wait_s: float = 10.0,
        status_fresh_s: float = 15.0,
    ) -> None:
        self._client = client
        self._artifacts = artifacts
        self._config = config
        self._sandbox = RepoSandbox(repo_root)
        self._tmp_dir = tmp_dir
        self._reader = reader or JimengHistoryReader()
        self._poll_stale_s = poll_stale_s
        self._poll_wait_s = poll_wait_s
        self._status_fresh_s = status_fresh_s
        self._composer: _Composer | None = None
        self._negatives: dict[str, str | None] = {}
        self._status_lock = threading.Lock()
        self._status_cursor = 0
        self._parse_failures: dict[str, int] = {}
        self._login_error = False
        self._inflight: tuple[int, int | None, float] | None = None
        self._tasks: dict[str, _TaskView] = {}
        self._prefixes: dict[str, str] = {}

    @property
    def kind(self) -> BackendKind:
        return BackendKind.WEB

    def health(self) -> BackendHealth:
        if not self._client.is_started or self._client.is_lost:
            return self._lost_health()
        with self._client.exclusive():
            try:
                report = self._client.run(lambda session: run_canary(session, self._reader, self._status_fresh_s))
            except (BrowserLostError, BrowserNotStartedError):
                return self._lost_health()
            except (PageStepError, BrowserCommandTimeoutError) as error:
                return BackendHealth(False, (f"canary: {error}",), self._client.web_version, PauseReason.PAGE_CONTRACT_BROKEN)
        failed = report.failed
        reason: PauseReason | None = None
        if report.blocker is not None:
            reason = STEP_REASONS[StepFailureKind(report.blocker)]
            failed = (*failed, report.blocker)
        elif self._ingest_status() is PauseReason.LOGIN_EXPIRED:
            reason, failed = PauseReason.LOGIN_EXPIRED, (*failed, "login_error_response")
        elif failed:
            reason = PauseReason.PAGE_CONTRACT_BROKEN
        return BackendHealth(not failed, failed, self._client.web_version, reason)

    def recover_browser(self) -> BackendHealth:
        with self._client.exclusive():
            self._composer = None
            try:
                self._client.restart()
            except BrowserLaunchError as error:
                return BackendHealth(False, (f"launch_{error.kind.value}",), None, PauseReason.BROWSER_LOST)
        return self.health()

    def prepare(self, job_id: str, request: FrozenRequest, until: PreparingStep) -> PrepareResult:
        plan = self._plan(request)
        if isinstance(plan, PrepareResult):
            return plan
        with self._client.exclusive():
            return self._prepare_locked(job_id, request, plan, until)

    def negative_prompt_entered(self, job_id: str) -> bool | None:
        """True / False once the job's fill ran with a negative prompt; None when it had none (or never filled)."""
        status = self._negatives.get(job_id)
        return None if status is None else status == NEGATIVE_ENTERED

    def check_before_submit(self, job_id: str, request: FrozenRequest) -> SubmitOutcome | None:
        plan = self._plan(request)
        if isinstance(plan, PrepareResult):
            return SubmitOutcome(None, plan.pause_reason, f"pre_click: {plan.message}")
        with self._client.exclusive():
            return self._pre_click_locked(job_id, request, plan)

    def submit(self, job_id: str, request: FrozenRequest) -> SubmitOutcome:
        plan = self._plan(request)
        if isinstance(plan, PrepareResult):
            return SubmitOutcome(None, plan.pause_reason, f"pre_click: {plan.message}")
        with self._client.exclusive():
            blocked = self._pre_click_locked(job_id, request, plan)
            if blocked is not None:
                return blocked
            dispatched = threading.Event()

            async def command(session: BrowserSession) -> SubmitCaptureDao:
                dispatched.set()
                return await click_generate(session, plan.prefix, self._reader)

            try:
                capture = self._client.run(command)
            except _BROWSER_FAILURES as error:
                self._composer = None
                if isinstance(error, PageStepError) and error.step == "generate_button":
                    return SubmitOutcome(None, STEP_REASONS[error.kind], f"pre_click: {error}")
                if not dispatched.is_set():
                    return SubmitOutcome(None, PauseReason.BROWSER_LOST, f"pre_click: {error}")
                return SubmitOutcome(None, PauseReason.SUBMIT_UNCONFIRMED, f"点击后结果不明：{error}")
            self._composer = None
            return self._submit_outcome(capture, plan)

    def poll(self, platform_task_id: str) -> PollResult:
        if not self._client.is_started or self._client.is_lost:
            return PollResult(RemoteStatus.UNKNOWN, None, PauseReason.BROWSER_LOST, self._client.lost_reason)
        problem = self._ingest_status()
        if problem is not None:
            return PollResult(RemoteStatus.UNKNOWN, None, problem, "状态响应异常")
        view = self._tasks.get(platform_task_id)
        final = view is not None and view.status in (RemoteStatus.SUCCEEDED, RemoteStatus.FAILED)
        if not final and (view is None or time.monotonic() - view.observed_at > self._poll_stale_s):
            refreshed = self._refresh_history(platform_task_id)
            if refreshed is not None:
                return refreshed
            view = self._tasks.get(platform_task_id)
        if view is None or view.status is None:
            return PollResult(RemoteStatus.UNKNOWN, None, None, "尚未观察到该任务的状态响应")
        if view.status is RemoteStatus.FAILED:
            failure = PauseReason.REAL_FACE_REJECTED if _REAL_FACE.search(view.fail_msg) else (
                PauseReason.MODERATION_REJECT if _MODERATION.search(view.fail_msg) else None
            )
            return PollResult(RemoteStatus.FAILED, view.progress_pct, failure, view.fail_msg or None)
        progress = 100 if view.status is RemoteStatus.SUCCEEDED else view.progress_pct
        return PollResult(view.status, progress)

    def download(self, job_id: str, platform_task_id: str) -> DownloadedFile:
        """One attempt; `WebBackendError.retryable` tells the caller whether `retries.download` applies."""
        work_dir = self._job_dir(job_id) / "download"
        prefix = self._prefix_for(platform_task_id)
        if prefix is None:
            raise WebBackendError(PauseReason.DOWNLOAD_FAILED, True, f"不知道任务 {platform_task_id} 的 prompt，无法定位记录")
        view = self._tasks.get(platform_task_id)
        part = work_dir / f"{_safe_name(platform_task_id)}.mp4.part"
        final = part.with_suffix("")
        with self._client.exclusive():
            shutil.rmtree(work_dir, ignore_errors=True)
            try:
                capture = self._client.run(lambda session: download_record(session, prefix, part))
            except PageStepError as error:
                reason = STEP_REASONS[error.kind]
                raise WebBackendError(reason, reason is PauseReason.DOWNLOAD_FAILED, str(error)) from error
            except (BrowserLostError, BrowserNotStartedError) as error:
                raise WebBackendError(PauseReason.BROWSER_LOST, False, str(error)) from error
            except BrowserCommandTimeoutError as error:
                raise WebBackendError(PauseReason.DOWNLOAD_FAILED, True, str(error)) from error
        size, digest = _hash_file(part)
        if view is not None and view.video_size is not None and size != view.video_size:
            part.unlink(missing_ok=True)
            raise WebBackendError(PauseReason.DOWNLOAD_FAILED, True, f"下载大小 {size} 与平台记录 {view.video_size} 不一致")
        os.replace(part, final)
        return DownloadedFile(temp_path=str(final), size=size, sha256=digest, credits_charged=capture.credits_charged)

    def _prepare_locked(self, job_id: str, request: FrozenRequest, plan: _ComposerPlan, until: PreparingStep) -> PrepareResult:
        composer = self._owned_composer(job_id, request)
        for step in _WEB_STEPS[: _WEB_STEPS.index(until) + 1]:
            if step in composer.done and step is not PreparingStep.VERIFY:
                continue
            try:
                self._run_step(step, job_id, request, plan, composer)
            except _StepStop as stop:
                return self._stopped(step, composer, stop.reason, stop.message)
            except PageStepError as error:
                return self._stopped(step, composer, STEP_REASONS[error.kind], str(error))
            except (BrowserLostError, BrowserNotStartedError) as error:
                return self._stopped(step, composer, PauseReason.BROWSER_LOST, str(error))
            except BrowserCommandTimeoutError as error:
                return self._stopped(step, composer, PauseReason.STEP_FAILED, str(error))
            composer.done.add(step)
            composer.epoch = self._client.navigation_epoch
            self._composer = composer
        return PrepareResult(until, composer.estimate, composer.screenshots, None, composer.negative)

    def _stopped(self, step: PreparingStep, composer: _Composer, reason: PauseReason, message: str) -> PrepareResult:
        """A captcha / login / credit overlay explains most step failures; the queue-level reason wins."""
        self._composer = None
        if reason in _BLOCKER_CAN_EXPLAIN and not self._client.is_lost:
            blocker = self._blocker_reason()
            if blocker is not None:
                reason, message = blocker, f"{message}（页面出现阻断：{blocker.value}）"
        return PrepareResult(step, composer.estimate, composer.screenshots, reason, message)

    def _blocker_reason(self) -> PauseReason | None:
        try:
            kind = self._client.run(detect_blocker)
        except _BROWSER_FAILURES:
            return None
        return None if kind is None else STEP_REASONS[kind]

    def _run_step(self, step: PreparingStep, job_id: str, request: FrozenRequest, plan: _ComposerPlan, composer: _Composer) -> None:
        if step is PreparingStep.SET_PARAMS:
            self._set_params(plan)
        elif step is PreparingStep.UPLOAD:
            self._upload(job_id, request)
        elif step is PreparingStep.FILL:
            self._fill(request, plan, composer)
            self._negatives[job_id] = composer.negative
        elif step is PreparingStep.PREVIEW:
            self._preview(job_id, composer)
        else:
            self._verify(plan)

    def _set_params(self, plan: _ComposerPlan) -> None:
        self._client.run(reset_composer)
        diff: tuple[str, ...] = ()
        for _ in range(1 + self._config.retries.set_params):
            readback = self._client.run(lambda session: set_params(session, plan.params))
            diff = params_diff(plan.params, readback)
            if not diff:
                return
        raise _StepStop(PauseReason.STEP_FAILED, "参数读回不一致：" + "；".join(diff))

    def _upload(self, job_id: str, request: FrozenRequest) -> None:
        references = request.request.upload_references
        current = {ref.resolved_path: self._repo_sha256(ref.resolved_path) for ref in references if ref.resolved_path}
        changed = request.changed_references(current)
        if changed:
            raise _StepStop(PauseReason.INPUTS_CHANGED, "确认后参考文件已变化：" + "、".join(ref.name for ref in changed))
        for ref in references:
            self._upload_one(self._stage_upload(job_id, ref.name, ref.resolved_path or ""))

    def _upload_one(self, item: UploadItemDao) -> None:
        last: PageStepError | None = None
        for _ in range(1 + self._config.retries.upload):
            try:
                self._client.run(lambda session: upload_file(session, item))
                return
            except PageStepError as error:
                if error.kind not in (StepFailureKind.UPLOAD_REJECTED, StepFailureKind.UPLOAD_TIMEOUT):
                    raise
                last = error
                self._client.run(lambda session: remove_upload(session, item.name))
        assert last is not None
        raise _StepStop(STEP_REASONS[last.kind], f"{item.name} 上传失败（已重试 {self._config.retries.upload} 次）：{last.detail}")

    def _fill(self, request: FrozenRequest, plan: _ComposerPlan, composer: _Composer) -> None:
        problem: str | None = None
        for _ in range(1 + self._config.retries.fill):
            self._client.run(lambda session: fill_editor(session, plan.segments))
            problem = compare_snapshot(plan.expected, self._client.run(read_editor))
            if problem is None:
                break
        if problem is not None:
            raise _StepStop(PauseReason.FILL_MISMATCH, problem)
        negative = request.request.negative_prompt
        composer.negative = None
        if negative:
            entered = self._client.run(lambda session: fill_negative(session, negative))
            composer.negative = NEGATIVE_ENTERED if entered else NEGATIVE_OMITTED

    def _preview(self, job_id: str, composer: _Composer) -> None:
        capture = self._client.run(capture_preview)
        limit = self._config.artifacts.preview_max_bytes
        page = self._artifacts.save_preview(job_id, "page", capture.page_png, limit)
        region = self._artifacts.save_preview(job_id, "composer", capture.composer_png, limit)
        composer.screenshots = (page.path.name, region.path.name)
        composer.estimate = capture.estimated_credits

    def _verify(self, plan: _ComposerPlan) -> None:
        diff = params_diff(plan.params, self._client.run(read_params))
        if diff:
            raise _StepStop(PauseReason.STEP_FAILED, "提交前参数读回不一致：" + "；".join(diff))
        uploads = self._client.run(lambda session: uploads_mismatch(session, plan.upload_names))
        if uploads is not None:
            raise _StepStop(PauseReason.STEP_FAILED, uploads)
        problem = compare_snapshot(plan.expected, self._client.run(read_editor))
        if problem is not None:
            raise _StepStop(PauseReason.FILL_MISMATCH, problem)

    def _pre_click_locked(self, job_id: str, request: FrozenRequest, plan: _ComposerPlan) -> SubmitOutcome | None:
        prepared = self._prepare_locked(job_id, request, plan, PreparingStep.VERIFY)
        if prepared.pause_reason is not None:
            return SubmitOutcome(None, prepared.pause_reason, f"pre_click: {prepared.message}")
        try:
            blocker = self._client.run(detect_blocker)
            state = self._client.run(pre_click_state)
        except _BROWSER_FAILURES as error:
            self._composer = None
            return SubmitOutcome(None, PauseReason.BROWSER_LOST, f"pre_click: {error}")
        if blocker is not None:
            return SubmitOutcome(None, STEP_REASONS[blocker], "pre_click: blocking page UI is showing")
        self._ingest_status()
        limit = self._config.concurrency.max_remote_rendering
        if state.inflight_limit is not None:
            limit = min(limit, state.inflight_limit)
        observed = self._inflight
        fresh_running = observed[0] if observed and time.monotonic() - observed[2] <= _INFLIGHT_FRESH_S else None
        if observed and observed[1] is not None and fresh_running is not None:
            limit = min(limit, observed[1])
        running = max(value for value in (state.inflight, fresh_running, 0) if value is not None)
        if state.parallel_notice or running >= limit:
            return SubmitOutcome(None, None, f"{CONCURRENCY_LIMIT_PRE_CLICK}（平台在途 {running} / 上限 {limit}）")
        if not state.send_enabled:
            return SubmitOutcome(None, None, GENERATE_DISABLED_PRE_CLICK)
        return None

    def _submit_outcome(self, capture: SubmitCaptureDao, plan: _ComposerPlan) -> SubmitOutcome:
        if capture.task_id is not None:
            self._prefixes[capture.task_id] = plan.prefix
            return SubmitOutcome(capture.task_id, None, f"任务标识来自 {capture.via}")
        text = capture.rejection_text or ""
        if capture.login_error:
            return SubmitOutcome(None, PauseReason.SUBMIT_REJECTED, f"点击后平台返回未登录：{text}")
        if text:
            if _REAL_FACE.search(text):
                return SubmitOutcome(None, PauseReason.REAL_FACE_REJECTED, text)
            if _MODERATION.search(text):
                return SubmitOutcome(None, PauseReason.MODERATION_REJECT, text)
            return SubmitOutcome(None, PauseReason.SUBMIT_REJECTED, text)
        detail = f"出现 {capture.blocker}" if capture.blocker else f"未截获提交响应（{capture.via}），历史记录也对不上"
        return SubmitOutcome(None, PauseReason.SUBMIT_UNCONFIRMED, f"点击后结果不明：{detail}")

    def _refresh_history(self, task_id: str) -> PollResult | None:
        with self._client.exclusive():
            self._composer = None
            try:
                self._client.run(reload_history_view)
            except (BrowserLostError, BrowserNotStartedError) as error:
                return PollResult(RemoteStatus.UNKNOWN, None, PauseReason.BROWSER_LOST, str(error))
            except (PageStepError, BrowserCommandTimeoutError) as error:
                return PollResult(RemoteStatus.UNKNOWN, None, PauseReason.PAGE_CONTRACT_BROKEN, str(error))
        started = time.monotonic()
        while time.monotonic() < started + self._poll_wait_s:
            problem = self._ingest_status()
            if problem is not None:
                return PollResult(RemoteStatus.UNKNOWN, None, problem, "状态响应异常")
            view = self._tasks.get(task_id)
            if view is not None and view.observed_at >= started:
                return None
            time.sleep(0.1)
        return None

    def _ingest_status(self) -> PauseReason | None:
        with self._status_lock:
            observed = sorted(
                (item for key in STATUS_KEYS for item in self._client.observations(key, self._status_cursor)),
                key=lambda item: item.seq,
            )
            for item in observed:
                self._status_cursor = max(self._status_cursor, item.seq)
                parsed = self._reader.status_body(item.key, item.body)
                if parsed.outcome is ParseOutcome.OK:
                    self._parse_failures[item.key] = 0
                    self._login_error = False
                    for record in parsed.records:
                        self._merge(record, item.observed_at)
                    if parsed.running_count is not None:
                        self._inflight = (parsed.running_count, parsed.running_limit, item.observed_at)
                elif parsed.outcome is ParseOutcome.LOGIN_ERROR:
                    self._login_error = True
                else:
                    self._parse_failures[item.key] = self._parse_failures.get(item.key, 0) + 1
            if max(self._parse_failures.values(), default=0) >= self._config.status.parse_failure_threshold:
                return PauseReason.PAGE_CONTRACT_BROKEN
            return PauseReason.LOGIN_EXPIRED if self._login_error else None

    def _merge(self, record: HistoryRecordDao, observed_at: float) -> None:
        view = self._tasks.setdefault(record.record_id, _TaskView())
        if record.status is not None:
            view.status = record.status
        if record.progress_pct is not None:
            view.progress_pct = record.progress_pct
        if record.fail_msg:
            view.fail_msg = record.fail_msg
        if record.prompt_text is not None:
            view.prompt_text = record.prompt_text
        if record.video_size is not None:
            view.video_size = record.video_size
        view.observed_at = observed_at

    def _prefix_for(self, task_id: str) -> str | None:
        self._ingest_status()
        view = self._tasks.get(task_id)
        if view is not None and view.prompt_text:
            return prompt_prefix(EditorSnapshotDao(view.prompt_text, ()))
        return self._prefixes.get(task_id)

    def _lost_health(self) -> BackendHealth:
        return BackendHealth(False, ("browser_lost",), self._client.web_version, PauseReason.BROWSER_LOST)

    def _owned_composer(self, job_id: str, request: FrozenRequest) -> _Composer:
        composer = self._composer
        fingerprint = request.fingerprint.value
        if (
            composer is None
            or composer.job_id != job_id
            or composer.fingerprint != fingerprint
            or composer.epoch != self._client.navigation_epoch
            or self._client.is_lost
        ):
            composer = _Composer(job_id, fingerprint, self._client.navigation_epoch)
        return composer

    def _plan(self, request: FrozenRequest) -> _ComposerPlan | PrepareResult:
        generation = request.request
        params = generation.params
        if generation.kind is not GenerationKind.VIDEO or params is None:
            return PrepareResult(PreparingStep.SET_PARAMS, None, (), PauseReason.STEP_FAILED, "网页通道只处理视频请求")
        if params.model not in MODEL_DISPLAY_NAMES:
            return PrepareResult(PreparingStep.SET_PARAMS, None, (), PauseReason.STEP_FAILED, f"PageMap 没有模型 {params.model} 的显示名")
        if params.reference_mode not in (None, "omni", OMNI_REFERENCE_MODE):
            return PrepareResult(PreparingStep.SET_PARAMS, None, (), PauseReason.STEP_FAILED, f"v1 只支持全能参考，收到 {params.reference_mode}")
        markers = tuple(
            MentionMarkerDao(ref.name, ref.label, ref.entity_name if ref.entity_name is not None else ref.name)
            for ref in generation.references
        )
        try:
            segments = build_fill_segments(generation.prompt, markers)
        except FillPlanError as error:
            return PrepareResult(PreparingStep.FILL, None, (), PauseReason.FILL_MISMATCH, str(error))
        expected = expected_snapshot(segments)
        composer_params = ComposerParamsDao(
            creation_type=VIDEO_CREATION_TYPE,
            model=JimengPageMap.model_display(params.model),
            reference_mode=OMNI_REFERENCE_MODE,
            ratio=params.ratio,
            resolution=JimengPageMap.resolution_display(params.resolution),
            count=params.count,
            duration_s=params.duration_s,
        )
        return _ComposerPlan(
            params=composer_params,
            segments=segments,
            expected=expected,
            prefix=prompt_prefix(expected),
            upload_names=tuple(ref.name for ref in generation.upload_references),
        )

    def _repo_sha256(self, rel: str) -> str | None:
        verdict = self._sandbox.check_read(rel)
        if not verdict.ok or verdict.path is None or not verdict.path.is_file():
            return None
        return _hash_file(verdict.path)[1]

    def _stage_upload(self, job_id: str, name: str, rel: str) -> UploadItemDao:
        verdict = self._sandbox.check_read(rel)
        if not verdict.ok or verdict.path is None:
            raise _StepStop(PauseReason.INPUTS_CHANGED, f"参考文件 {rel} 不在沙箱内或不可读（{verdict.violation}）")
        if "/" in name or "\\" in name or segment_violation(name) is not None:
            raise _StepStop(PauseReason.STEP_FAILED, f"参考项名 {name!r} 不能用作上传文件名")
        target = self._job_dir(job_id) / "upload" / f"{name}{verdict.path.suffix.lower()}"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(verdict.path, target)
        return UploadItemDao(name=name, path=target)

    def _job_dir(self, job_id: str) -> Path:
        violation = "separator" if "/" in job_id or "\\" in job_id else segment_violation(job_id)
        if violation is not None:
            raise WebBackendError(PauseReason.STEP_FAILED, False, f"job_id 不能用作临时目录名（{violation}）")
        target = self._tmp_dir / job_id
        if is_reparse_point(target):
            raise WebBackendError(PauseReason.STEP_FAILED, False, f"临时目录 {target.name} 是链接，拒绝使用")
        target.mkdir(parents=True, exist_ok=True)
        return target


def _hash_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(_HASH_CHUNK):
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]", "_", value)[:80] or "task"
