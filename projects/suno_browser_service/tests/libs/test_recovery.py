import subprocess
import sys
import json
import re
import threading
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

import pytest

from projects.suno_browser_service.libs.application.commands.job__command import JobCommand
from projects.suno_browser_service.libs.application.commands.runtime__command import RuntimeCommand
from projects.suno_browser_service.libs.application.dtos.job__dto import JobCdto
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import REPO_ROOT, Settings
from projects.suno_browser_service.libs.infrastructure.clients.lock__client import LockClient
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.application.mappers.job__mapper import JobMapper
from projects.suno_browser_service.libs.infrastructure.clients.suno__client import SunoClient
from projects.suno_browser_service.libs.infrastructure.writers.runtime__writer import RuntimeWriter


SONG_URL = "https://suno.com/song/12345678-1234-1234-1234-123456789abc"


@pytest.mark.parametrize("status,songs,submitted,expected", [
    ("preparing", [], False, "queued"),
    ("submitting", [], True, "uncertain"),
    ("submitting", [SONG_URL], True, "uncertain"),
    ("waiting", [], True, "uncertain"),
    ("waiting", [SONG_URL], True, "queued"),
    ("downloading", [SONG_URL], True, "queued"),
    ("completed", [SONG_URL], True, "completed"),
    ("needs_login", [], False, "needs_login"),
])
def test_recovery_preserves_submission_and_download_evidence(tmp_path: Path, status, songs, submitted, expected):
    settings = Settings(tmp_path)
    command = JobCommand(settings)
    job = command.submit("recover", JobCdto("quiet piano"))
    original = command.reader.get(job.id)
    baseline = ["https://suno.com/song/00000000-0000-0000-0000-000000000000"]
    files = [{"name": "persisted.mp3", "sha256": "known", "bytes": 128, "song_url": SONG_URL}]
    command.writer.save(replace(original, status=status, payload={
        **original.payload, "submitted": submitted, "song_urls": songs, "baseline": baseline, "files": files,
    }))
    runtime = RuntimeCommand(settings)
    runtime.recover()
    recovered = command.reader.get(job.id)
    assert recovered.status == expected
    assert recovered.payload["submitted"] is submitted
    assert recovered.payload["song_urls"] == songs
    assert recovered.payload["baseline"] == baseline
    assert recovered.payload["files"] == files
    assert runtime.thread is None
    if expected == "uncertain":
        assert recovered.payload["error"]["code"] == "interrupted_submission"
        if not songs:
            with pytest.raises(ServiceError, match="只恢复下载"):
                command.resume(job.id, [])
            assert command.reader.get(job.id).status == "uncertain"
    assert JobCommand(settings).submit("recover", JobCdto("quiet piano")).id == job.id
    assert len(command.reader.list()) == 1


def test_idempotency_survives_new_command_instance(tmp_path: Path):
    settings = Settings(tmp_path)
    first = JobCommand(settings).submit("restart", JobCdto("slow cello"))
    second = JobCommand(settings).submit("restart", JobCdto("slow cello"))
    assert second.id == first.id
    with pytest.raises(ServiceError) as exc:
        JobCommand(settings).submit("restart", JobCdto("different"))
    assert exc.value.code == "idempotency_conflict"


def test_optimistic_update_does_not_overwrite_newer_job(tmp_path: Path):
    command = JobCommand(Settings(tmp_path))
    job = command.submit("versioned", JobCdto("music"))
    stale = command.reader.get(job.id)
    command.writer.save(replace(stale, status="preparing"))
    with pytest.raises(ServiceError) as exc:
        command.writer.save(replace(stale, status="queued"))
    assert exc.value.code == "job_changed"
    assert command.reader.get(job.id).status == "preparing"


def test_lock_excludes_other_process_and_releases(tmp_path: Path):
    lock_path = tmp_path / "browser.lock"
    lock = LockClient(lock_path)
    script = """
import sys
from pathlib import Path
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.infrastructure.clients.lock__client import LockClient
lock = LockClient(Path(sys.argv[1]))
try:
    lock.acquire()
except ServiceError as exc:
    print(exc.code)
else:
    print('acquired')
    lock.release()
"""
    lock.acquire()
    try:
        blocked = subprocess.run([sys.executable, "-c", script, str(lock_path)], cwd=REPO_ROOT, capture_output=True, text=True, timeout=15)
        assert blocked.returncode == 0, blocked.stderr
        assert blocked.stdout.strip() == "browser_busy"
    finally:
        lock.release()
    released = subprocess.run([sys.executable, "-c", script, str(lock_path)], cwd=REPO_ROOT, capture_output=True, text=True, timeout=15)
    assert released.returncode == 0, released.stderr
    assert released.stdout.strip() == "acquired"


def test_real_request_log_is_persisted_before_local_action(tmp_path: Path):
    audit = AuditClient(tmp_path / "ai_videos" / "isolated_test")
    observed = []

    def local_action():
        events = [json.loads(body) for body in re.findall(r"```json\n(.*?)\n```", audit.log.path.read_text(encoding="utf-8"), re.S)]
        assert len(events) == 1 and events[0]["event"] == "request"
        observed.append(events[0]["request_id"])
        return {"local_only": True}

    assert audit.call("test_local_no_external_request", {"prompt": "local fixture", "authorization": "private-test-token"}, local_action) == {"local_only": True}
    text = audit.log.path.read_text(encoding="utf-8")
    events = [json.loads(body) for body in re.findall(r"```json\n(.*?)\n```", text, re.S)]
    assert [event["event"] for event in events] == ["request", "result"]
    assert {event["request_id"] for event in events} == set(observed)
    assert "private-test-token" not in text


def test_request_log_write_failure_prevents_local_action(tmp_path: Path):
    audit = AuditClient(tmp_path / "ai_videos" / "isolated_test")
    audit.log.path.parent.mkdir(parents=True)
    audit.log.path.mkdir()
    called = []
    with pytest.raises(OSError):
        audit.call("test_local_no_external_request", {}, lambda: called.append(True))
    assert called == []


def test_challenge_pauses_remaining_queue_across_restart(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    settings = Settings(tmp_path / "ai_videos" / "challenge_fixture")
    settings.data_dir.mkdir(parents=True)
    command = JobCommand(settings)
    first = command.submit("challenge", JobCdto("first cue"))
    second = command.submit("later", JobCdto("second cue"))
    runtime = RuntimeCommand(settings)

    @contextmanager
    def session(_audit):
        class Context:
            pages = [object()]
        yield Context()

    def challenge(_ui):
        raise ServiceError("challenge", "fixture human verification")

    monkeypatch.setattr(runtime.browser, "session", session)
    monkeypatch.setattr(SunoClient, "navigate", challenge)
    runtime.process(JobMapper.entity(command.reader.get(first.id)))
    assert command.reader.get(first.id).payload["error"]["code"] == "challenge"
    restarted = RuntimeCommand(settings)
    assert restarted.automation_paused()
    processed = []
    monkeypatch.setattr(restarted, "process", lambda job: processed.append(job.id))
    thread = threading.Thread(target=restarted.run)
    thread.start()
    try:
        assert not restarted.stop_event.wait(1.1)
    finally:
        restarted.stop_event.set()
        thread.join(timeout=3)
    assert processed == []
    assert command.reader.get(second.id).status == "queued"
    RuntimeWriter(settings.data_dir).clear_automation_pause()
    assert not restarted.automation_paused()


def test_recollect_only_requeues_submitted_jobs_without_files():
    from projects.suno_browser_service.libs.common.errors import ServiceError
    from projects.suno_browser_service.libs.domain.entities.job__entity import JobEntity
    job = JobEntity("j", "k", "f", "uncertain", {"submitted": True, "song_urls": ["https://suno.com/song/x"], "files": []})
    job.resume([], recollect=True)
    assert job.status == "queued" and job.payload["recollect"] is True and job.payload["song_urls"] == []
    for payload in ({"submitted": False, "files": []}, {"submitted": True, "files": [{"name": "a.wav"}]}):
        with pytest.raises(ServiceError):
            JobEntity("j", "k", "f", "uncertain", payload).resume([], recollect=True)
    with pytest.raises(ServiceError):
        JobEntity("j", "k", "f", "uncertain", {"submitted": True, "files": []}).resume(["https://suno.com/song/y"], recollect=True)


def test_cancel_only_withdraws_unsubmitted_jobs():
    from projects.suno_browser_service.libs.common.errors import ServiceError
    from projects.suno_browser_service.libs.domain.entities.job__entity import JobEntity
    job = JobEntity("j", "k", "f", "queued", {"submitted": False})
    job.cancel()
    assert job.status == "cancelled"
    for status, payload in (("queued", {"submitted": True}), ("waiting", {"submitted": False}), ("uncertain", {"submitted": True})):
        with pytest.raises(ServiceError):
            JobEntity("j", "k", "f", status, payload).cancel()
