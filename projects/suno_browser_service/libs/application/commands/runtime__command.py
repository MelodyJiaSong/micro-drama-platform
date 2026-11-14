import threading
import time
from pathlib import Path

from projects.suno_browser_service.libs.application.mappers.job__mapper import JobMapper
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.domain.entities.job__entity import JobEntity
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.browser__client import BrowserClient
from projects.suno_browser_service.libs.infrastructure.clients.database__client import DatabaseClient
from projects.suno_browser_service.libs.infrastructure.clients.lock__client import LockClient
from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient
from projects.suno_browser_service.libs.infrastructure.readers.job__reader import JobReader
from projects.suno_browser_service.libs.infrastructure.writers.audio__writer import AudioWriter
from projects.suno_browser_service.libs.infrastructure.writers.job__writer import JobWriter
from projects.suno_browser_service.libs.infrastructure.writers.private_directory__writer import PrivateDirectoryWriter
from projects.suno_browser_service.libs.infrastructure.writers.runtime__writer import RuntimeWriter
from projects.suno_browser_service.libs.infrastructure.readers.runtime__reader import RuntimeReader
from projects.suno_browser_service.libs.common.generation import GenerationRequest
from projects.suno_browser_service.libs.infrastructure.clients.asset__client import AssetClient
from projects.suno_browser_service.libs.infrastructure.clients.form__client import FormClient
from projects.suno_browser_service.libs.infrastructure.clients.manual_browser__client import ManualBrowserClient, window_open

# Failures of the window itself, not of Suno or the request; retried while nothing was submitted.
# ui_changed is included: a throttled tab can render the form later than the control wait; a real Suno change still
# ends as needs_attention after the retries.
TRANSIENT_CODES = {"TimeoutError", "TargetClosedError", "Error", "window_not_open", "browser_unavailable", "ui_changed"}
TRANSIENT_RETRIES = 3


class RuntimeCommand:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        PrivateDirectoryWriter.ensure(settings.data_dir)
        db = DatabaseClient(settings.data_dir / "jobs.sqlite3")
        self.reader, self.writer = JobReader(db), JobWriter(db)
        self.browser = BrowserClient(settings)
        self.lock = LockClient(settings.data_dir / "browser.lock")
        self.stop_event = threading.Event()
        self.thread: threading.Thread | None = None
        self.failure: str | None = None
        self._reopened_at = float("-inf")

    def start(self) -> None:
        self.lock.acquire()
        try:
            self.recover()
            RuntimeWriter(self.settings.data_dir).begin(self.settings.port)
            self.thread = threading.Thread(target=self.run, name="suno-worker", daemon=True)
            self.thread.start()
        except BaseException:
            self.lock.release()
            raise

    def shutdown_requested(self) -> bool:
        return RuntimeReader(self.settings.data_dir).shutdown_requested()

    def automation_paused(self) -> bool:
        return RuntimeReader(self.settings.data_dir).automation_paused()

    def stop(self) -> None:
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=10)
        if self.thread is None or not self.thread.is_alive():
            self.lock.release()

    def recover(self) -> None:
        for status in ("preparing", "submitting", "waiting", "downloading"):
            for dao in self.reader.list(status):
                job = JobMapper.entity(dao)
                if status == "submitting" or status == "waiting" and not job.payload.get("song_urls"):
                    self.change(job, "uncertain", error={"code": "interrupted_submission", "message": "上次提交结果未知；提供歌曲地址恢复，禁止重复生成"})
                else:
                    self.change(job, "queued")

    def change(self, job: JobEntity, status: str | None = None, **fields: object) -> None:
        if status:
            job.transition(status, **fields)
        else:
            job.payload.update(fields)
        self.writer.save(JobMapper.dao(job))
        job.version += 1

    def run(self) -> None:
        try:
            while not self.stop_event.is_set():
                if self.automation_paused():
                    self.stop_event.wait(1)
                    continue
                pending = self.reader.list("queued")
                if pending and self.settings.attached and not window_open(self.settings):
                    # Jobs stay queued (nothing is marked failed) while the service reopens its window itself.
                    self.reopen_window()
                    self.stop_event.wait(3)
                    continue
                if pending:
                    self.process(JobMapper.entity(pending[0]))
                else:
                    self.stop_event.wait(1)
        except Exception as exc:
            self.failure = type(exc).__name__
        finally:
            self.browser.close()
            self.lock.release()

    def reopen_window(self) -> None:
        """Queued jobs and no window: open the service's window again, at most once a minute. A Chrome that still holds
        the service profile but no longer answers on its port (seen 2026-11-03) is ended first; only processes started
        on the service's own profile are touched, never the person's other Chrome windows."""
        if not self.settings.window_auto_open or time.monotonic() - self._reopened_at < 60:
            return
        self._reopened_at = time.monotonic()
        self.browser.close()
        manual = ManualBrowserClient(self.settings)
        try:
            audit = AuditClient(self.settings.data_dir)
            if manual.profile_in_use():
                audit.call("window_stuck_end", {"profile": "service dedicated", "reason": "profile locked, port closed"},
                           manual.end_profile_processes)
            manual.open_window(audit)
        except Exception:
            pass  # tried again in a minute; the jobs stay queued

    def process(self, job: JobEntity) -> None:
        p = job.payload
        has_songs = bool(p.get("song_urls"))
        self.change(job, "downloading" if has_songs else "preparing")
        audit = AuditClient(Path(p["target"]))
        try:
            with self.browser.session(audit) as context:
                page = self.browser.page(context)
                ui = SunoClient(page, audit, self.settings.data_dir / "selectors.json")
                if self.settings.attached:
                    ui.renew_page = lambda: self.browser.renew_page(context)
                if self.settings.attached or not self.settings.headless and not self.settings.endpoint:
                    ui.challenge_wait = self.settings.challenge_wait
                    ui.on_challenge = lambda action: self.change(job, human_action=action)
                if self.settings.attached:
                    ui.login_hint = "在常驻 Suno 窗口里登录后恢复任务（窗口没开就运行 open-window.ps1）"
                if not has_songs:
                    self.recollect(job, ui) if p.get("recollect") else self.generate(job, ui)
                writer = AudioWriter(ui, self.settings.data_dir / "outputs" / job.id,
                                     capture=self.browser.capture_download if self.settings.attached else None)
                for url in p["song_urls"]:
                    if self.stop_event.is_set():
                        self.change(job, "queued")
                        return
                    existing = next((f for f in p["files"] if f["song_url"] == url), None)
                    if existing:
                        file = writer.output / existing["name"]
                        if file.exists() and writer.metadata(file, url) == existing:
                            continue
                        p["files"].remove(existing)
                    result = writer.download(url, p["format"])
                    self.change(job, files=[*p["files"], result])
                self.change(job, "completed", error=None)
        except Exception as exc:
            code = exc.code if isinstance(exc, ServiceError) else type(exc).__name__
            message = str(exc) if isinstance(exc, ServiceError) else "执行中断；检查本机 request_log.md，修复后恢复任务"
            status = "uncertain" if job.status in {"submitting", "waiting"} else (
                "needs_login" if code == "needs_login" else "needs_attention")
            if job.status == "completed":
                return
            retries = int(p.get("transient_retries", 0))
            if (self.settings.attached and job.status in {"preparing", "downloading"} and code in TRANSIENT_CODES
                    and retries < TRANSIENT_RETRIES and not self.stop_event.is_set()):
                # Nothing was submitted yet (or only a download failed): the window broke, so the job simply runs again.
                self.change(job, "queued", transient_retries=retries + 1, error={"code": code, "message": message})
                self.browser.close()
                self.stop_event.wait(5)
                return
            self.change(job, status, error={"code": code, "message": message})
            if code in {"challenge", "quota_exhausted"}:
                # quota: 2026-11-04 Suno showed "Out of Downloads"; more Creates would spend credits on songs that cannot be fetched.
                RuntimeWriter(self.settings.data_dir).pause_automation(job.id, code)

    def generate(self, job: JobEntity, ui: SunoClient) -> None:
        p = job.payload
        title = ((p["title"] + " · ") if p.get("title") else "") + "suno-job-" + job.id
        ui.navigate()
        if p.get("mode") or p.get("options") or p.get("references"):
            request = GenerationRequest.model_validate({k: p[k] for k in GenerationRequest.model_fields if k in p})
            baseline = FormClient(ui).prepare(request, title, AssetClient(self.settings))
        else:
            baseline = ui.prepare(p["prompt"], title, p["instrumental"], p.get("lyrics"))
        if self.stop_event.is_set():
            raise ServiceError("stopping", "服务正在停止，未提交生成")
        self.change(job, "submitting", submitted=True, baseline=baseline, title=title, applied_options=ui.applied_options, title_field=ui.title_field)
        ui.submit(title)
        self.change(job, "waiting")
        self.claim(job, ui, title, baseline, appear_wait=self.settings.clip_appear_wait, refresh=True)

    def recollect(self, job: JobEntity, ui: SunoClient) -> None:
        """Find an already submitted job's clips again; never fills the form or clicks Create."""
        p = job.payload
        ui.title_field = p.get("title_field", p.get("mode") != "sounds")
        ui.match_prompt = None if ui.title_field else p["prompt"]
        ui.navigate()
        self.change(job, "waiting", recollect=False)
        ui.search(p["title"] if ui.title_field else p["prompt"])
        # The clips already exist; a short look is enough before reporting them missing.
        self.claim(job, ui, p["title"], p.get("baseline", []), timeout=90)

    def claim(self, job: JobEntity, ui: SunoClient, title: str, baseline: list[str], timeout: float | None = None,
              appear_wait: float | None = None, refresh: bool = False) -> None:
        """Wait for this job's two clips. Time a person spends on a verification or login does not count.

        refresh (after Create only): the two clip ids in Suno's answer to Create are used directly when present;
        otherwise, once that answer arrived, the work tab is reloaded every refresh_seconds, since its clip list
        does not show new clips by itself. It is never reloaded before, which would abort the Create. appear_wait (after Create only, off by default): no clip row at all by then means Create most likely did not take
        effect (e.g. a verification closed unsolved), so the job is reported uncertain early instead of
        waiting out the whole generation timeout.
        """
        started = last_refresh = time.monotonic()
        limit = timeout or self.settings.generation_timeout
        seen = False
        while True:
            if refresh:
                direct = ui.created_songs()
                if len(direct) == 2:
                    self.change(job, "downloading", song_urls=direct)
                    return
                # Reloading before Suno sent its generate request would abort the Create.
                # Without Suno's answer to Create the tab is not reloaded (that aborted a pending Create), but only for
                # so long: 2026-11-03 ep13 was created, its answer was never seen and the list never refreshed.
                sent = ui.create_sent() or time.monotonic() - started >= self.settings.unanswered_create_wait
                if sent and time.monotonic() - last_refresh >= self.settings.refresh_seconds:
                    ui.refresh()
                    last_refresh = time.monotonic()
            songs = ui.collect(title, baseline)
            if len(songs) == 2:
                self.change(job, "downloading", song_urls=songs)
                return
            seen = seen or bool(songs)
            since = time.monotonic() - max(started, ui.human_cleared_at)
            if appear_wait and not seen and since >= appear_wait:
                raise ServiceError("no_clip_seen", f"Create 后 {int(appear_wait)} 秒内没有出现本任务的歌曲行，生成很可能没有开始"
                                   "（例如验证码没完成就关了）；在窗口里确认没生成后再用新键重提，有歌曲则 resume 认领")
            if since >= limit or self.stop_event.wait(self.settings.poll_seconds):
                break
        raise ServiceError("generation_timeout", "尚未确认两首属于本任务的歌曲；请查 Suno 后提供歌曲地址恢复")
