from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from datetime import datetime, timedelta
from pathlib import Path, PurePosixPath

from libs.application.dtos.job__dto import (
    DownloadPlanCdto, DownloadWorkCdto, RecoveredJobCdto, RecoveryCdto, StepWorkCdto, SubmitWorkCdto, TickCdto,
)
from libs.application.executors.backend__executor import JOB_MUTATION_LOCK, BackendExecutor, ExecutorResult
from libs.application.queries.job__query import RUNTIME_KEY
from libs.common.clock import Clock, iso
from libs.common.enums import (
    PREPARING_STEP_ORDER, PREPARING_STEPS_BY_BACKEND, BackendKind, BlockedOn, GenerationKind, JobState,
    NegativePromptStrategy, PauseReason, PauseTier, PreparingStep, QueueState, RemoteStatus, SourceType,
)
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.repositories.generation_backend__repository import (
    BackendHealth, DownloadedFile, GenerationBackend, PollResult, PrepareResult, SubmitOutcome,
)
from libs.domain.repositories.job__repository import JobRepository
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.domain.value_objects.pause_reason__valueobject import PauseReasonPolicy
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.clients.toast__client import ToastClient
from libs.infrastructure.daos.output__dao import FinalizedOutputDao, OutputExpectationDao
from libs.infrastructure.daos.store_record__dao import QueueStateDao
from libs.infrastructure.errors.output__error import OutputError, SidecarWriteError
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.store_record__reader import QueueStateReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.job__writer import JobWriter
from libs.infrastructure.writers.output__writer import OutputWriter, timestamp_label
from libs.infrastructure.writers.store_record__writer import QueueStateWriter

S = JobState
R = PauseReason
POLL_INTERVAL_S: float = 5.0
PRE_CLICK_RETRY_S: float = 5.0
UNHEALTHY_RECHECK_S: float = 60.0
PRUNE_INTERVAL: timedelta = timedelta(hours=24)
NOT_NOW_PREFIX: str = "not_now:"
_ACTIVE: frozenset[JobState] = frozenset({S.QUEUED, S.PREPARING, S.SUBMITTING, S.GENERATING, S.DOWNLOADING})
_NON_TERMINAL: frozenset[JobState] = _ACTIVE | {S.PAUSED_NEEDS_HUMAN}
_REMOTE: frozenset[JobState] = frozenset({S.SUBMITTING, S.GENERATING})
_STEP_RETRY_FIELDS: Mapping[PreparingStep, str] = {
    PreparingStep.SET_PARAMS: "set_params", PreparingStep.UPLOAD: "upload", PreparingStep.FILL: "fill",
}
_NO_OBSERVATION: frozenset[str] = frozenset({R.LOGIN_EXPIRED.value, R.BROWSER_LOST.value, R.CLI_LOGIN_REQUIRED.value})
_LOG_KEYS: tuple[str, ...] = ("dispatched", "paused_jobs", "failed_jobs", "done_jobs", "paused_queues")
_MESSAGE_LIMIT: int = 500


class SchedulerCommand:
    """Moves confirmed jobs through preparing → submitting → generating → downloading → done (FR-17..FR-22).

    `tick` never blocks on a backend: every backend call runs on the `BackendExecutor` lane of its backend and its
    result is applied on a later tick. Gates, in order: queue running (per backend) → one work item per lane →
    account slot (`submitting` + `generating` + `preparing` < `concurrency.max_remote_rendering`, all backends) →
    `pacing.min_submit_interval_s` since the last submit (all backends). `submitting` is persisted inside the submit
    work item, after the final verify and before `backend.submit`, so a crash can never lose a click.
    """

    def __init__(
        self,
        jobs: JobRepository,
        queue_states: tuple[QueueStateReader, QueueStateWriter],
        backends: Mapping[BackendKind, GenerationBackend],
        executor: BackendExecutor,
        global_config_provider: Callable[[], GlobalConfig],
        drama_config_provider: Callable[[str], DramaConfig],
        output_writer: OutputWriter,
        artifact_writer: ArtifactWriter,
        toast: ToastClient,
        clock: Clock,
        job_reader: JobReader,
        job_writer: JobWriter,
    ) -> None:
        self._jobs = jobs
        self._queue_reader, self._queue_writer = queue_states
        self._backends = backends
        self._executor = executor
        self._global_config_provider = global_config_provider
        self._drama_config_provider = drama_config_provider
        self._output_writer = output_writer
        self._artifact_writer = artifact_writer
        self._toast = toast
        self._clock = clock
        self._job_reader = job_reader
        self._job_writer = job_writer
        self._inflight: dict[str, str] = {}
        self._retry_at: dict[str, datetime] = {}
        self._last_submit_at: datetime | None = None
        self._submit_inflight: bool = False
        self._last_poll_at: dict[str, datetime] = {}
        self._step_failures: dict[str, int] = {}
        self._download_failures: dict[str, int] = {}
        self._health_inflight: set[BackendKind] = set()
        self._health_checked_at: dict[BackendKind, datetime] = {}
        self._health_ok_at: dict[BackendKind, datetime] = {}
        self._healthy: dict[BackendKind, bool] = {}
        self._versions: dict[BackendKind, str | None] = {}
        self._last_prune_at: datetime | None = None

    def recover(self, now: datetime) -> RecoveryCdto:
        cfg = self._global_config_provider()
        recovered: list[RecoveredJobCdto] = []
        polling: list[str] = []
        downloads: list[str] = []
        with JOB_MUTATION_LOCK:
            for job in self._jobs.list_in_states(_NON_TERMINAL):
                before = job.state
                if job.recover_after_restart(now):
                    self._jobs.save(job)
                    recovered.append(RecoveredJobCdto(job.job_id, before.value, job.state.value, _value(job.pause_reason)))
                    if job.state is S.PAUSED_NEEDS_HUMAN:
                        self._notify_job(job, cfg)
                elif job.state is S.GENERATING:
                    polling.append(job.job_id)
                elif job.state is S.DOWNLOADING:
                    downloads.append(job.job_id)
            for state in (self._inflight, self._retry_at, self._last_poll_at, self._step_failures, self._download_failures):
                state.clear()
            for health in (self._health_checked_at, self._health_ok_at, self._healthy, self._versions):
                health.clear()
            self._health_inflight.clear()
            self._submit_inflight = False
            self._last_submit_at = now
            pruned = self._prune(now, cfg)
        return RecoveryCdto(tuple(recovered), tuple(polling), tuple(downloads), pruned)

    def tick(self, now: datetime) -> TickCdto:
        cfg = self._global_config_provider()
        log: dict[str, list[str]] = {key: [] for key in _LOG_KEYS}
        with JOB_MUTATION_LOCK:
            applied = sum(1 for result in self._executor.poll_done() if self._apply(result, now, cfg, log))
            if self._last_prune_at is None or now - self._last_prune_at >= PRUNE_INTERVAL:
                self._prune(now, cfg)
            jobs = self._jobs.list_in_states(_ACTIVE)
            self._expire_waits(jobs, now, cfg, log)
            jobs = [job for job in jobs if job.state in _ACTIVE]
            queues = self._queue_states()
            remote = sum(1 for job in jobs if job.state in _REMOTE)
            reserved = remote + sum(1 for job in jobs if job.state is S.PREPARING)
            for kind, backend in self._backends.items():
                reserved = self._dispatch(kind, backend, jobs, queues.get(kind), reserved, remote, now, cfg, log)
        return TickCdto(applied, *(tuple(log[key]) for key in _LOG_KEYS), remote_rendering=remote)

    # ---- applying finished work -------------------------------------------------------------------------------

    def _apply(self, result: ExecutorResult, now: datetime, cfg: GlobalConfig, log: dict[str, list[str]]) -> bool:
        parts = result.key.split(":", 2)
        if parts[0] == "health":
            self._health_inflight.discard(result.backend)
            self._apply_health(result, now, cfg, log)
            return True
        if parts[0] != "job" or len(parts) != 3:
            return False
        job_id, phase = parts[1], parts[2]
        if self._inflight.get(job_id) == result.key:
            del self._inflight[job_id]
        if phase == "final":
            self._submit_inflight = False
        job = self._jobs.get(job_id)
        if job is None:
            return True
        if phase.startswith("step:"):
            self._apply_step(job, PreparingStep(phase.removeprefix("step:")), result, now, cfg, log)
        elif phase == "final":
            self._apply_final(job, result, now, cfg, log)
        elif phase == "poll":
            self._apply_poll(job, result, now, cfg, log)
        elif phase == "download":
            self._apply_download(job, result, now, cfg, log)
        return True

    def _apply_step(self, job: GenerationJobEntity, step: PreparingStep, result: ExecutorResult, now: datetime,
                    cfg: GlobalConfig, log: dict[str, list[str]]) -> None:
        if job.state is not S.PREPARING or job.current_step is not step:
            return
        if result.error is not None:
            self._step_failed(job, step, _describe(result.error), now, cfg, log)
            return
        work = result.value
        assert isinstance(work, StepWorkCdto)
        if work.changed_references:
            self._pause(job, R.INPUTS_CHANGED, "确认后参考文件已变化：" + "、".join(work.changed_references), now, cfg, log)
            return
        assert work.prepare is not None
        if not self._prepared(job, step, work.prepare, now, cfg, log):
            return
        if step is PreparingStep.PREVIEW:
            page = work.prepare.page_estimated_credits
            if page is None:
                self._step_failed(job, step, "预演没有读到页面预计积分", now, cfg, log)
                return
            assert job.frozen_request is not None
            tolerance = job.frozen_request.estimate_tolerance_pct
            if job.record_page_estimate(page, self._pause_if_unestimated(job), now):
                self._jobs.save(job)
                self._after_pause(job, f"页面预计 {page} 积分超出已确认的预计（容差 {tolerance}%）", now, cfg, log)
                return
        steps = job.preparing_steps
        job.advance_step(steps[steps.index(step) + 1])
        self._jobs.save(job)

    def _apply_final(self, job: GenerationJobEntity, result: ExecutorResult, now: datetime, cfg: GlobalConfig,
                     log: dict[str, list[str]]) -> None:
        if job.state is S.PREPARING:
            last = job.preparing_steps[-1]
            if job.current_step is not last:
                return
            if result.error is not None:
                self._step_failed(job, last, _describe(result.error), now, cfg, log)
                return
            work = result.value
            assert isinstance(work, SubmitWorkCdto)
            if work.changed_references:
                self._pause(job, R.INPUTS_CHANGED, "确认后参考文件已变化：" + "、".join(work.changed_references), now, cfg, log)
            elif work.prepare is not None and not self._prepared(job, last, work.prepare, now, cfg, log):
                return
            elif work.pre_click is not None:
                if work.pre_click.rejection is not None:
                    self._apply_reason(job, work.pre_click.rejection, work.pre_click.message, now, cfg, log)
                else:
                    self._retry_at[job.job_id] = now + timedelta(seconds=PRE_CLICK_RETRY_S)
                    self._record_facts(job.job_id, now, {"last_error": _clip(work.pre_click.message)})
            elif work.aborted_reason is not None:
                reason = _queue_reason(work.aborted_reason)
                if reason is not None and job.yield_to_queue_pause(reason, now):
                    self._jobs.save(job)
            return
        if job.state is not S.SUBMITTING:
            return
        self._retry_at.pop(job.job_id, None)
        if result.error is not None:
            self._pause(job, R.SUBMIT_UNCONFIRMED, f"点击后结果不明：{_describe(result.error)}", now, cfg, log)
            return
        work = result.value
        assert isinstance(work, SubmitWorkCdto) and work.outcome is not None
        self._apply_submit_outcome(job, work.outcome, now, cfg, log)

    def _apply_submit_outcome(self, job: GenerationJobEntity, outcome: SubmitOutcome, now: datetime, cfg: GlobalConfig,
                              log: dict[str, list[str]]) -> None:
        if outcome.accepted:
            assert outcome.platform_task_id is not None
            job.mark_generating(outcome.platform_task_id, now)
            self._jobs.save(job)
            self._last_poll_at[job.job_id] = now
            if job.is_terminal:
                self._notify_batch_if_finished(job, cfg)
            return
        reason = outcome.rejection
        if reason is None:
            not_clicked = (outcome.message or "").startswith(NOT_NOW_PREFIX)
            self._pause(job, R.SUBMIT_REJECTED if not_clicked else R.SUBMIT_UNCONFIRMED, outcome.message, now, cfg, log)
            return
        rule = PauseReasonPolicy.rule(reason)
        if rule.tier is PauseTier.JOB and S.SUBMITTING in rule.from_states and rule.applies_to(job.backend):
            self._apply_reason(job, reason, outcome.message, now, cfg, log)
            return
        if rule.tier is PauseTier.QUEUE:
            self._pause_queue(job.backend, reason.value, outcome.message, now, cfg, log)
        self._pause(job, R.SUBMIT_REJECTED, f"未点击（{reason.value}）：{outcome.message or ''}", now, cfg, log)

    def _apply_poll(self, job: GenerationJobEntity, result: ExecutorResult, now: datetime, cfg: GlobalConfig,
                    log: dict[str, list[str]]) -> None:
        self._last_poll_at[job.job_id] = now
        if job.state is not S.GENERATING:
            return
        if result.error is not None:
            self._record_facts(job.job_id, now, {"last_error": _describe(result.error)})
            return
        poll = result.value
        assert isinstance(poll, PollResult)
        if poll.status is RemoteStatus.SUCCEEDED:
            job.mark_downloading(now)
            self._jobs.save(job)
            self._record_facts(job.job_id, now, {"progress_pct": 100})
            return
        if poll.failure is not None and PauseReasonPolicy.rule(poll.failure).tier is PauseTier.QUEUE:
            self._pause_queue(job.backend, poll.failure.value, poll.message, now, cfg, log)
            return
        if poll.status is RemoteStatus.FAILED or poll.failure is not None:
            fallback = R.CLI_ERROR if job.backend is BackendKind.CLI else R.MODERATION_REJECT
            self._apply_reason(job, poll.failure or fallback, poll.message or "平台报告生成失败", now, cfg, log)
            return
        self._record_facts(job.job_id, now, {"progress_pct": poll.progress_pct})

    def _apply_download(self, job: GenerationJobEntity, result: ExecutorResult, now: datetime, cfg: GlobalConfig,
                        log: dict[str, list[str]]) -> None:
        if job.state is not S.DOWNLOADING:
            return
        if result.error is not None:
            self._download_failed(job, result.error, now, cfg, log)
            return
        work = result.value
        assert isinstance(work, DownloadWorkCdto)
        if work.skipped:
            return
        self._download_failures.pop(job.job_id, None)
        facts: dict[str, object] = {"outputs": list(work.outputs), "sidecar_missing": work.sidecar_missing, "last_error": work.note}
        self._record_facts(job.job_id, now, facts, credits_charged=work.credits_charged)
        job.mark_done(now)
        self._jobs.save(job)
        log["done_jobs"].append(job.job_id)
        self._notify_batch_if_finished(job, cfg)

    def _apply_health(self, result: ExecutorResult, now: datetime, cfg: GlobalConfig, log: dict[str, list[str]]) -> None:
        kind = result.backend
        self._health_checked_at[kind] = now
        if result.error is not None:
            health = BackendHealth(False, (f"health_error: {_describe(result.error)}",), None, None)
        else:
            assert isinstance(result.value, BackendHealth)
            health = result.value
        if health.version:
            self._versions[kind] = health.version
        self._healthy[kind] = health.ok
        if health.ok:
            self._health_ok_at[kind] = now
            return
        reason = health.pause_reason or (R.PAGE_CONTRACT_BROKEN if kind is BackendKind.WEB else None)
        if reason is not None and PauseReasonPolicy.rule(reason).tier is PauseTier.QUEUE:
            self._pause_queue(kind, reason.value, "；".join(health.failed_checks), now, cfg, log)

    # ---- state changes shared by the apply paths --------------------------------------------------------------

    def _prepared(self, job: GenerationJobEntity, step: PreparingStep, prepare: PrepareResult, now: datetime,
                  cfg: GlobalConfig, log: dict[str, list[str]]) -> bool:
        facts: dict[str, object] = {}
        if prepare.screenshot_names:
            facts["screenshots"] = list(prepare.screenshot_names)
        reported_sent = getattr(prepare, "negative_prompt_sent", None)
        if isinstance(reported_sent, bool):
            facts["negative_prompt_sent"] = reported_sent
        if facts:
            self._record_facts(job.job_id, now, facts)
        if prepare.pause_reason is not None:
            self._apply_reason(job, prepare.pause_reason, prepare.message, now, cfg, log)
            return False
        if _order(prepare.reached_step) < _order(step):
            self._step_failed(job, step, prepare.message or f"{step} 未完成", now, cfg, log)
            return False
        self._step_failures.pop(job.job_id, None)
        return True

    def _apply_reason(self, job: GenerationJobEntity, reason: PauseReason, message: str | None, now: datetime,
                      cfg: GlobalConfig, log: dict[str, list[str]]) -> None:
        rule = PauseReasonPolicy.rule(reason)
        if rule.tier is PauseTier.QUEUE:
            self._pause_queue(job.backend, reason.value, message, now, cfg, log)
            if job.state is S.PREPARING:
                if job.yield_to_queue_pause(reason, now):
                    self._jobs.save(job)
                else:
                    self._pause(job, R.STEP_FAILED, f"{reason.value}: {message or ''}", now, cfg, log)
            return
        if job.state in rule.from_states and rule.applies_to(job.backend):
            if rule.is_failure:
                job.fail(reason, now)
                self._jobs.save(job)
                self._record_facts(job.job_id, now, {"last_error": _clip(message)})
                log["failed_jobs"].append(job.job_id)
                self._notify_batch_if_finished(job, cfg)
            else:
                self._pause(job, reason, message, now, cfg, log)
            return
        fallback = {S.PREPARING: R.STEP_FAILED, S.SUBMITTING: R.SUBMIT_REJECTED, S.DOWNLOADING: R.DOWNLOAD_FAILED}.get(job.state)
        detail = f"{reason.value}: {message or ''}"
        if fallback is None:
            self._record_facts(job.job_id, now, {"last_error": _clip(detail)})
        else:
            self._pause(job, fallback, detail, now, cfg, log)

    def _step_failed(self, job: GenerationJobEntity, step: PreparingStep, message: str, now: datetime, cfg: GlobalConfig,
                     log: dict[str, list[str]]) -> None:
        count = self._step_failures.get(job.job_id, 0) + 1
        field = _STEP_RETRY_FIELDS.get(step)
        budget = 0 if field is None else int(getattr(cfg.retries, field))
        self._record_facts(job.job_id, now, {"last_error": _clip(message)})
        if count > budget:
            self._step_failures.pop(job.job_id, None)
            self._pause(job, R.STEP_FAILED, f"{step} 失败（已重试 {budget} 次）：{message}", now, cfg, log)
        else:
            self._step_failures[job.job_id] = count

    def _download_failed(self, job: GenerationJobEntity, error: BaseException, now: datetime, cfg: GlobalConfig,
                         log: dict[str, list[str]]) -> None:
        message = _describe(error)
        reason = getattr(error, "reason", None)
        retryable = getattr(error, "retryable", True) is not False
        if isinstance(reason, PauseReason) and not retryable:
            self._download_failures.pop(job.job_id, None)
            if reason is R.DOWNLOAD_FAILED:
                self._pause(job, R.DOWNLOAD_FAILED, message, now, cfg, log)
            elif PauseReasonPolicy.rule(reason).tier is PauseTier.QUEUE:
                self._pause_queue(job.backend, reason.value, message, now, cfg, log)
                self._record_facts(job.job_id, now, {"last_error": message})
            else:
                self._apply_reason(job, reason, message, now, cfg, log)
            return
        count = self._download_failures.get(job.job_id, 0) + 1
        self._record_facts(job.job_id, now, {"last_error": message})
        if count > cfg.retries.download:
            self._download_failures.pop(job.job_id, None)
            self._pause(job, R.DOWNLOAD_FAILED, f"下载失败（已重试 {cfg.retries.download} 次）：{message}", now, cfg, log)
        else:
            self._download_failures[job.job_id] = count

    def _pause(self, job: GenerationJobEntity, reason: PauseReason, message: str | None, now: datetime, cfg: GlobalConfig,
               log: dict[str, list[str]]) -> None:
        job.pause(reason, now)
        self._jobs.save(job)
        if job.state is S.PAUSED_NEEDS_HUMAN:
            self._after_pause(job, message, now, cfg, log)
        else:
            self._notify_batch_if_finished(job, cfg)

    def _after_pause(self, job: GenerationJobEntity, message: str | None, now: datetime, cfg: GlobalConfig,
                     log: dict[str, list[str]]) -> None:
        if message:
            self._record_facts(job.job_id, now, {"last_error": _clip(message)})
        log["paused_jobs"].append(job.job_id)
        self._notify_job(job, cfg)

    def _pause_queue(self, kind: BackendKind, reason: str, message: str | None, now: datetime, cfg: GlobalConfig,
                     log: dict[str, list[str]]) -> None:
        current = self._queue_states().get(kind)
        if current is not None and current[0] is QueueState.PAUSED and current[1] == reason:
            return
        self._queue_writer.set(QueueStateDao(kind.value, QueueState.PAUSED.value, reason, iso(now)))
        log["paused_queues"].append(f"{kind.value}:{reason}")
        detail = f"（{_clip(message, 120)}）" if message else ""
        self._toast.notify("队列已暂停", f"{kind.value} 队列：{reason}{detail}", self._ui_url(cfg, "/queue"))

    def _expire_waits(self, jobs: Sequence[GenerationJobEntity], now: datetime, cfg: GlobalConfig,
                      log: dict[str, list[str]]) -> None:
        limit = timedelta(hours=cfg.wait.timeout_h)
        for job in jobs:
            if job.state is S.GENERATING and job.job_id not in self._inflight:
                since = _entered_at(job, S.GENERATING)
                if since is not None and now - since > limit:
                    self._pause(job, R.WAIT_TIMEOUT, f"生成超过 {cfg.wait.timeout_h} h 仍未结束", now, cfg, log)

    # ---- dispatching new work ---------------------------------------------------------------------------------

    def _dispatch(self, kind: BackendKind, backend: GenerationBackend, jobs: Sequence[GenerationJobEntity],
                  queue: tuple[QueueState, str | None, datetime | None] | None, reserved: int, remote: int,
                  now: datetime, cfg: GlobalConfig, log: dict[str, list[str]]) -> int:
        mine = [job for job in jobs if job.backend is kind and job.request.kind is not GenerationKind.ENTITY]
        state, queue_reason, changed_at = queue or (QueueState.RUNNING, None, None)
        paused = state is QueueState.PAUSED
        if paused:
            self._block((job for job in mine if job.state is S.QUEUED), BlockedOn.QUEUE_PAUSED)
        if self._executor.busy(kind) or kind in self._health_inflight:
            return reserved
        if self._health_due(kind, mine, paused, changed_at, now, cfg):
            self._dispatch_health(kind, backend, log)
            return reserved
        healthy = self._healthy.get(kind, False)
        holding = False
        for job in [job for job in mine if job.state is S.PREPARING]:
            if job.job_id in self._inflight:
                return reserved
            if paused:
                reason = _queue_reason(queue_reason)
                if reason is not None and job.yield_to_queue_pause(reason, now):
                    self._jobs.save(job)
                    reserved -= 1
                else:
                    holding = True
                continue
            if not healthy:
                holding = True
                continue
            if job.current_step is job.preparing_steps[-1]:
                if self._retry_at.get(job.job_id, now) > now or not self._may_submit(now, remote, cfg):
                    holding = True
                    continue
                self._dispatch_final(kind, backend, job, log)
                return reserved
            self._dispatch_step(kind, backend, job, log)
            return reserved
        if not paused and healthy and not holding:
            download = next((job for job in mine if job.state is S.DOWNLOADING and job.job_id not in self._inflight), None)
            if download is not None:
                self._dispatch_download(kind, backend, download, cfg, log)
                return reserved
        observable = kind in self._health_checked_at and (healthy or (paused and queue_reason not in _NO_OBSERVATION))
        poll = self._next_poll(mine, now) if observable else None
        if poll is not None:
            self._dispatch_poll(kind, backend, poll, log)
            return reserved
        if paused or not healthy or any(job.state is S.PREPARING for job in mine):
            return reserved
        queued = sorted((job for job in mine if job.state is S.QUEUED and job.confirmed and job.job_id not in self._inflight), key=_fifo)
        if not queued:
            return reserved
        if reserved >= cfg.concurrency.max_remote_rendering:
            self._block(queued, BlockedOn.SLOT)
            return reserved
        if not self._interval_elapsed(now, cfg):
            self._block(queued, BlockedOn.INTERVAL)
            return reserved
        job = queued[0]
        confirmation = job.confirmation
        ok_at = self._health_ok_at.get(kind)
        if confirmation is not None and (ok_at is None or ok_at < confirmation.confirmed_at):
            self._dispatch_health(kind, backend, log)
            return reserved
        self._block(queued[1:], BlockedOn.NONE)
        job.start_preparing(now)
        self._jobs.save(job)
        if job.current_step is not job.preparing_steps[-1]:
            self._dispatch_step(kind, backend, job, log)
        elif self._may_submit(now, remote, cfg):
            self._dispatch_final(kind, backend, job, log)
        return reserved + 1

    def _health_due(self, kind: BackendKind, mine: Sequence[GenerationJobEntity], paused: bool,
                    changed_at: datetime | None, now: datetime, cfg: GlobalConfig) -> bool:
        last = self._health_checked_at.get(kind)
        if last is None:
            return True
        if paused or any(job.state is S.PREPARING for job in mine):
            return False
        if not self._healthy.get(kind, False):
            return (changed_at is not None and changed_at > last) or now - last >= timedelta(seconds=UNHEALTHY_RECHECK_S)
        return now - last >= timedelta(minutes=cfg.canary.interval_min)

    def _may_submit(self, now: datetime, remote: int, cfg: GlobalConfig) -> bool:
        return not self._submit_inflight and remote < cfg.concurrency.max_remote_rendering and self._interval_elapsed(now, cfg)

    def _interval_elapsed(self, now: datetime, cfg: GlobalConfig) -> bool:
        last = self._last_submit_at
        return last is None or (now - last).total_seconds() >= cfg.pacing.min_submit_interval_s

    def _next_poll(self, mine: Sequence[GenerationJobEntity], now: datetime) -> GenerationJobEntity | None:
        due = [
            job for job in mine
            if job.state is S.GENERATING and job.job_id not in self._inflight
            and (job.job_id not in self._last_poll_at or (now - self._last_poll_at[job.job_id]).total_seconds() >= POLL_INTERVAL_S)
        ]
        return min(due, key=lambda job: self._last_poll_at.get(job.job_id, datetime.min.replace(tzinfo=now.tzinfo)), default=None)

    def _block(self, jobs: object, blocked_on: BlockedOn) -> None:
        for job in jobs:  # type: ignore[attr-defined]
            if job.state is S.QUEUED and job.blocked_on is not blocked_on:
                job.set_blocked_on(blocked_on)
                self._jobs.save(job)

    def _dispatch_health(self, kind: BackendKind, backend: GenerationBackend, log: dict[str, list[str]]) -> None:
        key = f"health:{kind.value}"
        self._health_inflight.add(kind)
        self._executor.submit(kind, key, backend.health)
        log["dispatched"].append(key)

    def _dispatch_step(self, kind: BackendKind, backend: GenerationBackend, job: GenerationJobEntity,
                       log: dict[str, list[str]]) -> None:
        step = job.current_step
        frozen = job.frozen_request
        assert step is not None and frozen is not None
        rehash = step is _rehash_step(kind)
        job_id = job.job_id
        self._submit_work(kind, job_id, f"job:{job_id}:step:{step.value}", lambda: self._work_step(backend, job_id, frozen, step, rehash), log)

    def _dispatch_final(self, kind: BackendKind, backend: GenerationBackend, job: GenerationJobEntity,
                        log: dict[str, list[str]]) -> None:
        frozen = job.frozen_request
        assert frozen is not None
        rehash = job.current_step is _rehash_step(kind)
        job_id = job.job_id
        self._submit_inflight = True
        self._submit_work(kind, job_id, f"job:{job_id}:final", lambda: self._work_final(kind, backend, job_id, frozen, rehash), log)

    def _dispatch_poll(self, kind: BackendKind, backend: GenerationBackend, job: GenerationJobEntity,
                       log: dict[str, list[str]]) -> None:
        task_id = job.platform_task_id
        assert task_id is not None
        self._submit_work(kind, job.job_id, f"job:{job.job_id}:poll", lambda: backend.poll(task_id), log)

    def _dispatch_download(self, kind: BackendKind, backend: GenerationBackend, job: GenerationJobEntity,
                           cfg: GlobalConfig, log: dict[str, list[str]]) -> None:
        task_id = job.platform_task_id
        assert task_id is not None
        plan = self._download_plan(job, cfg)
        job_id = job.job_id
        self._submit_work(kind, job_id, f"job:{job_id}:download", lambda: self._work_download(backend, job_id, task_id, plan), log)

    def _submit_work(self, kind: BackendKind, job_id: str, key: str, fn: Callable[[], object], log: dict[str, list[str]]) -> None:
        self._inflight[job_id] = key
        log["dispatched"].append(key)
        self._executor.submit(kind, key, fn)

    # ---- work items (run on executor threads) -----------------------------------------------------------------

    def _work_step(self, backend: GenerationBackend, job_id: str, frozen: FrozenRequest, step: PreparingStep,
                   rehash: bool) -> StepWorkCdto:
        if rehash:
            changed = self._changed_references(frozen)
            if changed:
                return StepWorkCdto(None, changed)
        return StepWorkCdto(backend.prepare(job_id, frozen, step), ())

    def _work_final(self, kind: BackendKind, backend: GenerationBackend, job_id: str, frozen: FrozenRequest,
                    rehash: bool) -> SubmitWorkCdto:
        if rehash:
            changed = self._changed_references(frozen)
            if changed:
                return SubmitWorkCdto(changed, None, None, False, None, None)
        last = PREPARING_STEPS_BY_BACKEND[kind][-1]
        prepare: PrepareResult | None = None
        check = getattr(backend, "check_before_submit", None)
        if callable(check):
            pre_click = check(job_id, frozen)
            if pre_click is not None:
                return SubmitWorkCdto((), None, pre_click, False, None, None)
        else:
            prepare = backend.prepare(job_id, frozen, last)
            if prepare.pause_reason is not None or _order(prepare.reached_step) < _order(last):
                return SubmitWorkCdto((), prepare, None, False, None, None)
        with JOB_MUTATION_LOCK:
            job = self._jobs.get(job_id)
            if job is None or job.state is not S.PREPARING or job.current_step is not last:
                return SubmitWorkCdto((), prepare, None, False, None, "job_changed")
            queue_state, queue_reason, _ = self._queue_states().get(kind, (QueueState.RUNNING, None, None))
            if queue_state is QueueState.PAUSED:
                return SubmitWorkCdto((), prepare, None, False, None, queue_reason or "queue_paused")
            at = self._clock.now()
            job.mark_submitting(at)
            self._jobs.save(job)
            self._last_submit_at = at
        return SubmitWorkCdto((), prepare, None, True, backend.submit(job_id, frozen), None)

    def _work_download(self, backend: GenerationBackend, job_id: str, task_id: str, plan: DownloadPlanCdto) -> DownloadWorkCdto:
        download_all = getattr(backend, "download_all", None)
        if plan.count > 1 and callable(download_all):
            downloaded = download_all(job_id, task_id)
            files: tuple[DownloadedFile, ...] = tuple(downloaded.files)
            charged: int | None = downloaded.credits_charged
        else:
            single = backend.download(job_id, task_id)
            files, charged = (single,), single.credits_charged
        with JOB_MUTATION_LOCK:
            current = self._jobs.get(job_id)
            still_downloading = current is not None and current.state is S.DOWNLOADING
        if not still_downloading:
            for file in files:
                Path(file.temp_path).unlink(missing_ok=True)
            return DownloadWorkCdto(True, (), (), charged, False, None)
        finished = self._clock.now()
        label = timestamp_label(finished, plan.timezone)
        numbered = plan.count > 1 or len(files) > 1
        outputs: list[str] = []
        sidecars: list[str] = []
        skipped: list[str] = []
        sidecar_missing = False
        for index, file in enumerate(files, start=1):
            name = _file_name(plan, label, f"_{index}" if numbered else "", file.temp_path)
            expected = OutputExpectationDao(file.size, file.sha256, plan.duration_s, plan.ratio, plan.duration_tolerance_s)
            try:
                placed: FinalizedOutputDao = self._output_writer.finalize(
                    Path(file.temp_path), plan.target_dir_rel, name, expected, _final_sidecar(plan, file, finished)
                )
            except SidecarWriteError as error:
                placed, sidecar_missing = error.output, True
            except OutputError as error:
                if not outputs:
                    for rest in files[index:]:
                        Path(rest.temp_path).unlink(missing_ok=True)
                    raise
                skipped.append(f"{name}：{error.message}")
                continue
            outputs.append(placed.path_rel)
            if placed.sidecar_rel is not None:
                sidecars.append(placed.sidecar_rel)
        note = ("以下文件未通过校验，已跳过：" + "；".join(skipped)) if skipped else None
        return DownloadWorkCdto(False, tuple(outputs), tuple(sidecars), charged, sidecar_missing, note)

    # ---- helpers ----------------------------------------------------------------------------------------------

    def _download_plan(self, job: GenerationJobEntity, cfg: GlobalConfig) -> DownloadPlanCdto:
        request = job.request
        params = request.params
        drama = self._drama_config(job)
        slot, _, key = request.output_slot.partition("#")
        default_extension: str | None = ".mp4" if request.kind is GenerationKind.VIDEO else ".png"
        if key:
            target = f"{slot}/{drama.outputs.image_candidates_dir.format(key=key)}"
            template, fields = "{ts}{suffix}", {}
        elif request.kind is GenerationKind.VIDEO:
            target = f"{slot}/renders" if request.source.type is SourceType.SHOT else slot
            template, fields, default_extension = drama.outputs.video_name, {"shot": PurePosixPath(slot).name}, None
        else:
            target, template, fields = slot, "{ts}{suffix}", {}
        duration = float(params.duration_s) if request.kind is GenerationKind.VIDEO and params and params.duration_s is not None else None
        return DownloadPlanCdto(
            target_dir_rel=target, name_template=template, name_fields=fields, default_extension=default_extension,
            count=params.count if params else 1, duration_s=duration, ratio=params.ratio if params else None,
            duration_tolerance_s=cfg.download.duration_tolerance_s, timezone=cfg.time.timezone,
            downloading_at=_entered_at(job, S.DOWNLOADING), sidecar=self._sidecar_base(job, drama, cfg),
        )

    def _sidecar_base(self, job: GenerationJobEntity, drama: DramaConfig, cfg: GlobalConfig) -> dict[str, object]:
        frozen, confirmation = job.frozen_request, job.confirmation
        assert frozen is not None and confirmation is not None
        request = frozen.request
        preparing, submitting = _entered_at(job, S.PREPARING), _entered_at(job, S.SUBMITTING)
        generating, downloading = _entered_at(job, S.GENERATING), _entered_at(job, S.DOWNLOADING)
        dao = self._job_reader.get(job.job_id)
        reported_sent = _runtime_bucket(None if dao is None else dao.extra_json)[1].get("negative_prompt_sent")
        return {
            "job_id": job.job_id,
            "batch_id": job.batch_id,
            "attempt": job.attempt,
            "backend": job.backend.value,
            "source": {"type": request.source.type.value, "path": request.source.path, "block_key": request.source.block_key},
            "prompt_sha256": request.prompt_sha256(),
            "negative_prompt_sha256": request.negative_prompt_sha256(),
            "negative_prompt_sent": reported_sent if isinstance(reported_sent, bool) else _negative_prompt_sent(job, drama, cfg),
            "references": [_reference(ref) for ref in request.references],
            "params": None if request.params is None else request.params.canonical(),
            "platform_task_id": job.platform_task_id,
            "credits_estimated": {"static": frozen.credits_estimated, "page": job.page_estimated_credits},
            "credits_charged": None,
            "confirmed_at": iso(confirmation.confirmed_at),
            "confirmer": confirmation.confirmer.value,
            "submitted_at": None if submitting is None else iso(submitting),
            "finished_at": None,
            "durations": {
                "prepare_s": _seconds(preparing, submitting),
                "queue_wait_s": _seconds(confirmation.confirmed_at, preparing),
                "render_s": _seconds(generating, downloading),
                "download_s": None,
            },
            ("web_version" if job.backend is BackendKind.WEB else "cli_version"): self._versions.get(job.backend),
            "browser_version": None,
        }

    def _changed_references(self, frozen: FrozenRequest) -> tuple[str, ...]:
        current = {
            ref.resolved_path: self._output_writer.current_sha256(ref.resolved_path)
            for ref in frozen.request.upload_references if ref.resolved_path is not None
        }
        return tuple(ref.name for ref in frozen.changed_references(current))

    def _pause_if_unestimated(self, job: GenerationJobEntity) -> bool:
        return not any(
            other.approved_credits is not None for other in self._jobs.list_by_batch(job.batch_id) if other.job_id != job.job_id
        )

    def _drama_config(self, job: GenerationJobEntity) -> DramaConfig:
        return self._drama_config_provider(job.request.output_slot.partition("#")[0])

    def _record_facts(self, job_id: str, now: datetime, runtime: Mapping[str, object],
                      credits_charged: int | None = None) -> None:
        dao = self._job_reader.get(job_id)
        if dao is None:
            return
        extra, bucket = _runtime_bucket(dao.extra_json)
        for key, value in runtime.items():
            if key == "screenshots" and isinstance(value, list):
                previous = bucket.get("screenshots")
                value = list(dict.fromkeys([*(previous if isinstance(previous, list) else []), *value]))
            bucket[key] = value
        extra[RUNTIME_KEY] = bucket
        extra_json = json.dumps(extra, ensure_ascii=False, sort_keys=True)
        charged = dao.credits_charged if credits_charged is None else credits_charged
        if extra_json == dao.extra_json and charged == dao.credits_charged:
            return
        self._job_writer.save(replace(dao, extra_json=extra_json, credits_charged=charged, updated_at=iso(now)), [])

    def _queue_states(self) -> dict[BackendKind, tuple[QueueState, str | None, datetime | None]]:
        states: dict[BackendKind, tuple[QueueState, str | None, datetime | None]] = {}
        known = {kind.value: kind for kind in BackendKind}
        for record in self._queue_reader.all():
            if record.backend in known:
                states[known[record.backend]] = (QueueState(record.state), record.reason, _parse_time(record.updated_at))
        return states

    def _notify_job(self, job: GenerationJobEntity, cfg: GlobalConfig) -> None:
        self._toast.notify("作业待人工处理", f"{job.job_id}：{_value(job.pause_reason)}", self._ui_url(cfg, f"/jobs/{job.job_id}"))

    def _notify_batch_if_finished(self, job: GenerationJobEntity, cfg: GlobalConfig) -> None:
        if all(other.is_terminal for other in self._jobs.list_by_batch(job.batch_id)):
            self._toast.notify("批次已全部结束", job.batch_id, self._ui_url(cfg, f"/batches/{job.batch_id}"))

    def _prune(self, now: datetime, cfg: GlobalConfig) -> int:
        self._last_prune_at = now
        return self._artifact_writer.prune_previews(cfg.artifacts.preview_retention_days, now.timestamp())

    @staticmethod
    def _ui_url(cfg: GlobalConfig, path: str) -> str:
        return f"http://127.0.0.1:{cfg.server.port}{path}"


def _runtime_bucket(extra_json: str | None) -> tuple[dict[str, object], dict[str, object]]:
    try:
        extra = json.loads(extra_json) if extra_json else {}
    except ValueError:
        extra = {}
    if not isinstance(extra, dict):
        extra = {}
    bucket = extra.get(RUNTIME_KEY)
    return extra, dict(bucket) if isinstance(bucket, dict) else {}


def _file_name(plan: DownloadPlanCdto, label: str, suffix: str, temp_path: str) -> str:
    name = plan.name_template.format(**plan.name_fields, ts=label, suffix=suffix)
    if plan.default_extension is None:
        return name
    return name + (Path(temp_path).suffix.lower() or plan.default_extension)


def _final_sidecar(plan: DownloadPlanCdto, file: DownloadedFile, finished: datetime) -> dict[str, object]:
    body = dict(plan.sidecar)
    durations = dict(body.get("durations") or {})  # type: ignore[call-overload]
    durations["download_s"] = _seconds(plan.downloading_at, finished)
    body["durations"] = durations
    body["credits_charged"] = file.credits_charged
    body["finished_at"] = iso(finished)
    return body


def _negative_prompt_sent(job: GenerationJobEntity, drama: DramaConfig, cfg: GlobalConfig) -> bool:
    request = job.request
    if request.negative_prompt is None or request.params is None or job.backend is not BackendKind.WEB:
        return False
    if drama.video.negative_prompt is NegativePromptStrategy.OMIT:
        return False
    capability = cfg.model_limits.find(request.params.model)
    return capability is not None and capability.negative_prompt_field


def _reference(ref: ReferenceItem) -> dict[str, object]:
    if ref.is_entity:
        return {"name": ref.name, "kind": ref.kind.value, "entity": ref.entity_name}
    return {"name": ref.name, "kind": ref.kind.value, "path": ref.resolved_path, "sha256": ref.sha256}


def _rehash_step(kind: BackendKind) -> PreparingStep:
    return next(step for step in PREPARING_STEPS_BY_BACKEND[kind] if _order(step) >= _order(PreparingStep.UPLOAD))


def _order(step: PreparingStep) -> int:
    return PREPARING_STEP_ORDER.index(step)


def _entered_at(job: GenerationJobEntity, state: JobState) -> datetime | None:
    for transition in reversed(job.transitions):
        if transition.to_state is state:
            return transition.at
    return None


def _seconds(start: datetime | None, end: datetime | None) -> float | None:
    return None if start is None or end is None else round((end - start).total_seconds(), 3)


def _fifo(job: GenerationJobEntity) -> tuple[datetime, str, str]:
    confirmation = job.confirmation
    assert confirmation is not None
    return confirmation.confirmed_at, job.batch_id, job.job_id


def _queue_reason(value: str | None) -> PauseReason | None:
    try:
        reason = None if value is None else PauseReason(value)
    except ValueError:
        return None
    return reason if reason is not None and PauseReasonPolicy.rule(reason).tier is PauseTier.QUEUE else None


def _parse_time(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _value(reason: PauseReason | None) -> str | None:
    return None if reason is None else reason.value


def _describe(error: BaseException) -> str:
    message = getattr(error, "message", None) or str(error) or type(error).__name__
    return _clip(str(message)) or type(error).__name__


def _clip(message: str | None, limit: int = _MESSAGE_LIMIT) -> str | None:
    return None if message is None else message[:limit]
