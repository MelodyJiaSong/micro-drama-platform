"""Test support for the job lifecycle: inline executor, in-memory repositories, scriptable backends, harness."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from libs.application.commands.job__command import JobCommand
from libs.application.commands.scheduler__command import SchedulerCommand
from libs.application.dtos.job__dto import TickCdto
from libs.application.executors.backend__executor import ExecutorResult
from libs.common.clock import FrozenClock, iso
from libs.common.enums import (
    BackendKind, Confirmer, GenerationKind, JobState, PreparingStep, QueueState, RefKind, RemoteStatus, SourceType,
)
from libs.common.paths import RepoSandbox
from libs.domain.entities.generation_job__entity import GenerationJobEntity
from libs.domain.entities.operation__entity import OperationEntity
from libs.domain.repositories.generation_backend__repository import (
    BackendHealth, DownloadedFile, PollResult, PrepareResult, SubmitOutcome,
)
from libs.domain.value_objects.batch_confirmation__valueobject import BatchConfirmation
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.fingerprint__valueobject import Fingerprint
from libs.domain.value_objects.frozen_request__valueobject import FrozenRequest
from libs.domain.value_objects.generation_params__valueobject import GenerationParams
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.clients.sqlite__client import SqliteClient
from libs.infrastructure.clients.toast__client import ToastClient
from libs.infrastructure.daos.job__dao import JobDao, JobTransitionDao
from libs.infrastructure.daos.output__dao import MediaProbeDao
from libs.infrastructure.daos.store_record__dao import QueueStateDao
from libs.infrastructure.readers.job__reader import JobReader
from libs.infrastructure.readers.store_record__reader import QueueStateReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.job__writer import JobWriter
from libs.infrastructure.writers.output__writer import OutputWriter
from libs.infrastructure.writers.store_record__writer import QueueStateWriter
from tests.libs.domain.builders import TOLERANCE_PCT, T0, confirmed_item, global_data, rehydrate

DRAMA_REL = "ai_videos/huangye_shenghuo/hy3"
SHOTS_REL = f"{DRAMA_REL}/5_6_分镜与prompt/shots"
CARD_REL = f"{DRAMA_REL}/2_世界观人设/characters/c1_砌炉的老人"


class InlineExecutor:
    """Runs work synchronously at submit (or on `run_pending` when manual); results surface on the next poll."""

    def __init__(self, manual: bool = False) -> None:
        self.manual = manual
        self.submitted: list[tuple[BackendKind, str]] = []
        self._pending: list[tuple[BackendKind, str, Callable[[], object]]] = []
        self._done: list[ExecutorResult] = []

    def submit(self, backend: BackendKind, key: str, fn: Callable[[], object]) -> None:
        self.submitted.append((backend, key))
        if self.manual:
            self._pending.append((backend, key, fn))
        else:
            self._run(backend, key, fn)

    def run_pending(self) -> int:
        pending, self._pending = self._pending, []
        for backend, key, fn in pending:
            self._run(backend, key, fn)
        return len(pending)

    def busy(self, backend: BackendKind) -> bool:
        return any(b is backend for b, _, _ in self._pending) or any(r.backend is backend for r in self._done)

    def poll_done(self) -> list[ExecutorResult]:
        done, self._done = self._done, []
        return done

    def shutdown(self) -> None:
        self._pending.clear()

    def _run(self, backend: BackendKind, key: str, fn: Callable[[], object]) -> None:
        try:
            self._done.append(ExecutorResult(backend, key, fn(), None))
        except Exception as error:
            self._done.append(ExecutorResult(backend, key, None, error))


class FakeJobRepository:
    """In-memory `JobRepository` that also mirrors each save into the SQLite `jobs` rows the read side uses.

    Like the real adapter must, it preserves the columns the entity does not carry (`credits_charged`, `extra_json`).
    """

    def __init__(self, client: SqliteClient, drama_rel: str | None = DRAMA_REL) -> None:
        self._jobs: dict[str, GenerationJobEntity] = {}
        self._reader = JobReader(client)
        self._writer = JobWriter(client)
        self._drama_rel = drama_rel
        self.saves = 0

    def get(self, job_id: str) -> GenerationJobEntity | None:
        job = self._jobs.get(job_id)
        return None if job is None else rehydrate(job)

    def save(self, job: GenerationJobEntity) -> None:
        previous = self._jobs.get(job.job_id)
        known = 0 if previous is None else len(previous.transitions)
        self._jobs[job.job_id] = rehydrate(job)
        existing = self._reader.get(job.job_id)
        created = existing.created_at if existing else iso(job.transitions[0].at if job.transitions else T0)
        updated = iso(job.transitions[-1].at) if job.transitions else created
        if existing is not None and existing.updated_at > updated:
            updated = existing.updated_at
        reason = job.pause_reason or job.failure_reason
        frozen = job.frozen_request
        dao = JobDao(
            job_id=job.job_id, batch_id=job.batch_id, kind=job.request.kind.value, backend=job.backend.value,
            source_type=job.request.source.type.value, source_path=job.request.source.path, drama_rel=self._drama_rel,
            output_slot=job.request.output_slot, state=job.state.value, reason=None if reason is None else reason.value,
            blocked_on=job.blocked_on.value, preparing_step=None if job.current_step is None else job.current_step.value,
            fingerprint=job.fingerprint.value, idempotency_key=None, attempt=job.attempt, confirmed=job.confirmed,
            cancel_requested=job.cancel_requested, credits_spent=job.credits_spent, platform_task_id=job.platform_task_id,
            credits_estimated_static=None if frozen is None else frozen.credits_estimated,
            credits_estimated_page=job.page_estimated_credits,
            credits_charged=None if existing is None else existing.credits_charged,
            frozen_request_json="{}", extra_json="{}" if existing is None else existing.extra_json,
            created_at=created, updated_at=updated,
        )
        transitions = [
            JobTransitionDao(job.job_id, t.from_state.value, t.to_state.value, t.reason, iso(t.at))
            for t in job.transitions[known:]
        ]
        self._writer.save(dao, transitions)
        self.saves += 1

    def list_by_batch(self, batch_id: str) -> list[GenerationJobEntity]:
        return [rehydrate(job) for _, job in sorted(self._jobs.items()) if job.batch_id == batch_id]

    def list_in_states(self, states: frozenset[JobState]) -> list[GenerationJobEntity]:
        return [rehydrate(job) for _, job in sorted(self._jobs.items()) if job.state in states]

    def find_by_fingerprint(self, fingerprint: Fingerprint) -> list[GenerationJobEntity]:
        return [rehydrate(job) for _, job in sorted(self._jobs.items()) if job.fingerprint == fingerprint]


class FakeOperationRepository:
    def __init__(self) -> None:
        self._operations: dict[str, OperationEntity] = {}

    def get(self, operation_id: str) -> OperationEntity | None:
        operation = self._operations.get(operation_id)
        return None if operation is None else _copy_operation(operation)

    def save(self, operation: OperationEntity) -> None:
        self._operations[operation.operation_id] = _copy_operation(operation)

    def list_unfinished(self) -> list[OperationEntity]:
        return [_copy_operation(op) for op in self._operations.values() if not op.is_finished]


def _copy_operation(operation: OperationEntity) -> OperationEntity:
    return OperationEntity(
        operation.operation_id, operation.kind, operation.created_at, operation.subject_id, state=operation.state,
        started_at=operation.started_at, finished_at=operation.finished_at, result=operation.result,
        error_code=operation.error_code, error_message=operation.error_message,
    )


@dataclass(frozen=True)
class PrepareResultWithNegative(PrepareResult):
    negative_prompt_sent: bool = False


@dataclass(frozen=True)
class FakeDownloadSet:
    submit_id: str
    files: tuple[DownloadedFile, ...]
    credits_charged: int | None


Scripted = PrepareResult | SubmitOutcome | PollResult | DownloadedFile | BackendHealth | Exception


class FakeBackend:
    """Scriptable `GenerationBackend`. Unscripted calls succeed; scripts are consumed front to back."""

    def __init__(self, kind: BackendKind, tmp_dir: Path, jobs: FakeJobRepository, clock: FrozenClock) -> None:
        self._kind = kind
        self._tmp_dir = tmp_dir
        self._jobs = jobs
        self._clock = clock
        self.calls: list[tuple[str, str]] = []
        self.health_script: list[BackendHealth | Exception] = []
        self.prepare_script: dict[tuple[str, PreparingStep], list[PrepareResult | Exception]] = {}
        self.submit_script: dict[str, list[SubmitOutcome | Exception]] = {}
        self.poll_script: dict[str, list[PollResult | Exception]] = {}
        self.download_script: dict[str, list[DownloadedFile | Exception]] = {}
        self.on_submit: Callable[[str], None] | None = None
        self.page_estimate: int | None = 440
        self.polls_to_finish: int = 0
        self.submit_states: list[JobState | None] = []
        self.submit_times: list[datetime] = []
        self.active_tasks: set[str] = set()
        self._polls: dict[str, int] = {}
        self._downloads = 0

    @property
    def kind(self) -> BackendKind:
        return self._kind

    def count(self, method: str) -> int:
        return sum(1 for name, _ in self.calls if name == method)

    def health(self) -> BackendHealth:
        self.calls.append(("health", ""))
        return _take(self.health_script, BackendHealth(True, (), f"{self._kind.value}-1.0"))  # type: ignore[return-value]

    def prepare(self, job_id: str, request: FrozenRequest, until: PreparingStep) -> PrepareResult:
        self.calls.append(("prepare", f"{job_id}:{until.value}"))
        default = PrepareResult(until, self.page_estimate if until is PreparingStep.PREVIEW else None, ())
        return _take(self.prepare_script.get((job_id, until), []), default)  # type: ignore[return-value]

    def submit(self, job_id: str, request: FrozenRequest) -> SubmitOutcome:
        self.calls.append(("submit", job_id))
        stored = self._jobs.get(job_id)
        self.submit_states.append(None if stored is None else stored.state)
        self.submit_times.append(self._clock.now())
        if self.on_submit is not None:
            self.on_submit(job_id)
        task = f"task-{job_id}-{self.count('submit')}"
        outcome = _take(self.submit_script.get(job_id, []), SubmitOutcome(task))
        assert isinstance(outcome, SubmitOutcome)
        if outcome.accepted:
            self.active_tasks.add(outcome.platform_task_id or task)
        return outcome

    def poll(self, platform_task_id: str) -> PollResult:
        self.calls.append(("poll", platform_task_id))
        scripted = self.poll_script.get(platform_task_id, [])
        if scripted:
            return _take(scripted, PollResult(RemoteStatus.GENERATING, None))  # type: ignore[return-value]
        seen = self._polls.get(platform_task_id, 0)
        self._polls[platform_task_id] = seen + 1
        if seen < self.polls_to_finish:
            return PollResult(RemoteStatus.GENERATING, int(100 * seen / max(self.polls_to_finish, 1)))
        self.active_tasks.discard(platform_task_id)
        return PollResult(RemoteStatus.SUCCEEDED, 100)

    def download(self, job_id: str, platform_task_id: str) -> DownloadedFile:
        self.calls.append(("download", job_id))
        scripted = self.download_script.get(job_id, [])
        if scripted:
            return _take(scripted, None)  # type: ignore[return-value]
        return self._file(job_id, ".mp4" if self._kind is BackendKind.WEB else ".png", 440)

    def _file(self, job_id: str, ext: str, credits: int | None) -> DownloadedFile:
        self._downloads += 1
        self._tmp_dir.mkdir(parents=True, exist_ok=True)
        path = self._tmp_dir / f"{job_id}-{self._downloads}{ext}"
        data = f"bytes-of-{job_id}-{self._downloads}".encode()
        path.write_bytes(data)
        return DownloadedFile(str(path), len(data), hashlib.sha256(data).hexdigest(), credits)


class FakeCliBackend(FakeBackend):
    """Adds the CLI adapter's `download_all` side channel (multi-image tasks)."""

    def download_all(self, job_id: str, platform_task_id: str) -> FakeDownloadSet:
        self.calls.append(("download_all", job_id))
        stored = self._jobs.get(job_id)
        count = 1 if stored is None or stored.request.params is None else stored.request.params.count
        files = tuple(self._file(job_id, ".png", 4 if index == 0 else None) for index in range(count))
        return FakeDownloadSet(platform_task_id, files, 4)


class FakeWebBackend(FakeBackend):
    """Adds the web adapter's `check_before_submit` side channel."""

    def __init__(self, tmp_dir: Path, jobs: FakeJobRepository, clock: FrozenClock) -> None:
        super().__init__(BackendKind.WEB, tmp_dir, jobs, clock)
        self.pre_click_script: list[SubmitOutcome | None] = []

    def check_before_submit(self, job_id: str, request: FrozenRequest) -> SubmitOutcome | None:
        self.calls.append(("check_before_submit", job_id))
        return self.pre_click_script.pop(0) if self.pre_click_script else None


class StubProber:
    def __init__(self, duration_s: float = 22.0, video_size: tuple[int, int] = (1280, 720), image_size: tuple[int, int] = (1536, 2048)) -> None:
        self.duration_s = duration_s
        self.video_size = video_size
        self.image_size = image_size
        self.calls = 0

    def probe(self, path: Path) -> MediaProbeDao:
        self.calls += 1
        if path.suffix.lower() == ".mp4":
            return MediaProbeDao(self.duration_s, *self.video_size)
        return MediaProbeDao(None, *self.image_size)


def _take(script: list[Scripted], default: object) -> object:
    item = script.pop(0) if script else default
    if isinstance(item, Exception):
        raise item
    return item


def video_request(slot_name: str, duration: int = 22, ratio: str = "16:9", count: int = 1,
                  refs: Sequence[ReferenceItem] = (), negative: str | None = None) -> GenerationRequest:
    slot = f"{SHOTS_REL}/{slot_name}"
    return GenerationRequest(
        kind=GenerationKind.VIDEO, prompt=f"{slot_name} prompt", negative_prompt=negative, references=tuple(refs),
        params=GenerationParams(model="seedance2.5", ratio=ratio, resolution="720p", count=count, duration_s=duration),
        output_slot=slot, source=RequestSource(type=SourceType.SHOT, path=f"{slot}/{slot_name}.md"),
    )


def image_request(key: str, count: int = 1) -> GenerationRequest:
    return GenerationRequest(
        kind=GenerationKind.IMAGE, prompt=f"{key}_砌炉的老人立绘", negative_prompt=None, references=(),
        params=GenerationParams(model="seedream5.0", ratio="3:4", resolution="2k", count=count),
        output_slot=f"{CARD_REL}#{key}",
        source=RequestSource(type=SourceType.ASSET_IMAGE, path=f"{CARD_REL}/c1_砌炉的老人.md", block_key=key),
    )


def confirmed_job(job_id: str, request: GenerationRequest, backend: BackendKind = BackendKind.WEB,
                  batch_id: str = "batch-1", credits: int | None = 440, confirmed_at: datetime = T0) -> GenerationJobEntity:
    job = GenerationJobEntity(job_id, batch_id, backend, request, Fingerprint.of(request))
    item = confirmed_item(request, credits)
    job.confirm(
        BatchConfirmation(batch_id=batch_id, confirmed_at=confirmed_at, confirmer=Confirmer.UI_HUMAN),
        FrozenRequest.from_item(item, backend, "cfg-digest", TOLERANCE_PCT),
        item,
    )
    return job


@dataclass
class Harness:
    root: Path
    client: SqliteClient
    clock: FrozenClock
    jobs: FakeJobRepository
    queue_reader: QueueStateReader
    queue_writer: QueueStateWriter
    executor: InlineExecutor
    web: FakeBackend
    cli: FakeCliBackend
    prober: StubProber
    output_writer: OutputWriter
    toast_sink: Path
    config_data: dict[str, object]
    scheduler: SchedulerCommand = field(init=False)
    job_command: JobCommand = field(init=False)

    def __post_init__(self) -> None:
        drama = DramaConfig.from_dict(DramaConfig.defaults("hy3"), self.cfg().model_limits)
        self.scheduler = SchedulerCommand(
            jobs=self.jobs, queue_states=(self.queue_reader, self.queue_writer),
            backends={BackendKind.WEB: self.web, BackendKind.CLI: self.cli}, executor=self.executor,  # type: ignore[arg-type]
            global_config_provider=self.cfg, drama_config_provider=lambda rel: drama, output_writer=self.output_writer,
            artifact_writer=ArtifactWriter(self.root / ".data" / "artifacts"), toast=ToastClient(True, self.toast_sink),
            clock=self.clock, job_reader=JobReader(self.client), job_writer=JobWriter(self.client),
        )
        self.job_command = JobCommand(self.jobs, (self.queue_reader, self.queue_writer), self.clock)

    def cfg(self) -> GlobalConfig:
        return GlobalConfig.from_dict(self.config_data)

    def set_config(self, section: str, key: str, value: object) -> None:
        table = self.config_data[section]
        assert isinstance(table, dict)
        table[key] = value

    def add(self, job: GenerationJobEntity) -> GenerationJobEntity:
        self.jobs.save(job)
        return job

    def tick(self, seconds: float = 1.0) -> TickCdto:
        self.clock.advance(timedelta(seconds=seconds))
        return self.scheduler.tick(self.clock.now())

    def run(self, ticks: int, seconds: float = 1.0, check: Callable[[], None] | None = None) -> None:
        for _ in range(ticks):
            self.tick(seconds)
            if check is not None:
                check()

    def run_until(self, predicate: Callable[[], bool], limit: int = 500, seconds: float = 1.0) -> int:
        for index in range(limit):
            if predicate():
                return index
            self.tick(seconds)
        raise AssertionError("condition not reached")

    def state(self, job_id: str) -> JobState:
        job = self.jobs.get(job_id)
        assert job is not None
        return job.state

    def job(self, job_id: str) -> GenerationJobEntity:
        job = self.jobs.get(job_id)
        assert job is not None
        return job

    def remote_count(self) -> int:
        return sum(1 for job in self.jobs.list_in_states(frozenset({JobState.SUBMITTING, JobState.GENERATING})))

    def pause_queue(self, kind: BackendKind, reason: str) -> None:
        self.queue_writer.set(QueueStateDao(kind.value, QueueState.PAUSED.value, reason, iso(self.clock.now())))

    def queue(self, kind: BackendKind) -> tuple[str, str | None]:
        rows = {row.backend: row for row in self.queue_reader.all()}
        row = rows.get(kind.value)
        return ("running", None) if row is None else (row.state, row.reason)

    def toasts(self) -> list[dict[str, str]]:
        if not self.toast_sink.is_file():
            return []
        return [json.loads(line) for line in self.toast_sink.read_text(encoding="utf-8").splitlines()]

    def runtime(self, job_id: str) -> dict[str, object]:
        dao = JobReader(self.client).get(job_id)
        assert dao is not None
        return json.loads(dao.extra_json).get("runtime", {})

    def abs(self, rel: str) -> Path:
        return self.root / rel


def make_harness(tmp_path: Path, manual: bool = False, pre_click: bool = False) -> Harness:
    root = tmp_path / "repo"
    (root / "ai_videos").mkdir(parents=True)
    client = SqliteClient(tmp_path / "bridge.db")
    clock = FrozenClock(T0)
    jobs = FakeJobRepository(client)
    tmp_dir = root / ".data" / "tmp"
    web: FakeBackend = FakeWebBackend(tmp_dir / "web", jobs, clock) if pre_click else FakeBackend(BackendKind.WEB, tmp_dir / "web", jobs, clock)
    prober = StubProber()
    return Harness(
        root=root, client=client, clock=clock, jobs=jobs, queue_reader=QueueStateReader(client),
        queue_writer=QueueStateWriter(client), executor=InlineExecutor(manual), web=web,
        cli=FakeCliBackend(BackendKind.CLI, tmp_dir / "cli", jobs, clock), prober=prober,
        output_writer=OutputWriter(RepoSandbox(root, (root / ".data",)), prober),  # type: ignore[arg-type]
        toast_sink=tmp_path / "toasts.jsonl", config_data=global_data(),
    )


def advance(job: GenerationJobEntity, state: JobState, at: datetime = T0, task_id: str | None = None) -> GenerationJobEntity:
    """Walks a queued, confirmed job forward to `state` (preparing / submitting / generating / downloading / done)."""
    if state is JobState.QUEUED:
        return job
    job.start_preparing(at)
    if state is JobState.PREPARING:
        return job
    for step in job.preparing_steps[1:]:
        job.advance_step(step)
    if job.backend is BackendKind.WEB and job.request.kind is not GenerationKind.ENTITY:
        job.record_page_estimate(440, False, at)
    job.mark_submitting(at)
    if state is JobState.SUBMITTING:
        return job
    job.mark_generating(task_id or f"task-{job.job_id}", at)
    if state is JobState.GENERATING:
        return job
    job.mark_downloading(at)
    if state is JobState.DOWNLOADING:
        return job
    job.mark_done(at)
    return job


def reference_file(harness: Harness, name: str, content: bytes) -> ReferenceItem:
    rel = f"{DRAMA_REL}/2_世界观人设/scenes/bg11_崖脚洼地/{name}.png"
    path = harness.abs(rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return ReferenceItem(name=name, label="场景参考图", kind=RefKind.IMAGE, resolved_path=rel, sha256=hashlib.sha256(content).hexdigest())
