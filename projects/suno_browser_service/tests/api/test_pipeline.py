"""真实 HTTP/API/worker/SQLite/Chrome；仅外部 Suno 网页替换为离线 HTTP fixture。"""

import hashlib
import io
import json
import socket
import sqlite3
import threading
import time
import wave
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

import httpx
import pytest
import uvicorn
from playwright.sync_api import BrowserContext, Route

from projects.suno_browser_service.apps.api.app_factory import create_app
from projects.suno_browser_service.apps.api.container import Container
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.browser__client import BrowserClient
from projects.suno_browser_service.tests.libs.test_browser import FORM, SONG, SONG_IDS


TOKEN = "offline-pipeline-test-token-long-enough"


@dataclass
class PipelineSite:
    audio: bytes
    base_url: str = ""
    fail_second_once: bool = False
    submissions: list[dict] = field(default_factory=list)
    downloads: dict[str, int] = field(default_factory=dict)


@pytest.fixture
def pipeline_site() -> Iterator[PipelineSite]:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as audio:
        audio.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
        audio.writeframes(b"\0\0" * 800)
    site = PipelineSite(buffer.getvalue())

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args: object) -> None:
            pass

        def respond(self, body: bytes, mime: str, download: bool = False) -> None:
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            if download:
                self.send_header("Content-Disposition", 'attachment; filename="offline-fixture.wav"')
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path.startswith("/audio/"):
                song_id = self.path.rsplit("/", 1)[-1].removesuffix(".wav")
                site.downloads[song_id] = site.downloads.get(song_id, 0) + 1
                failing = site.fail_second_once and song_id == SONG_IDS[1] and site.downloads[song_id] == 1
                body = b"<html>Fixture export failed</html>" if failing else site.audio
                self.respond(body, "application/octet-stream", download=True)
            elif self.path.startswith("/song/"):
                song_id = self.path.rsplit("/", 1)[-1]
                page = SONG.replace("/audio/fixture.wav", f"/audio/{song_id}.wav")
                self.respond(page.encode(), "text/html; charset=utf-8")
            else:
                self.respond(FORM.encode(), "text/html; charset=utf-8")

        def do_POST(self) -> None:
            assert self.path == "/created"
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            site.submissions.append(payload)
            songs = [{"id": song_id, "title": payload["title"]} for song_id in SONG_IDS[:2]]
            self.respond(json.dumps(songs).encode(), "application/json")

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    site.base_url = f"http://127.0.0.1:{server.server_port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield site
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


class FixtureBrowserClient(BrowserClient):
    def __init__(self, settings: Settings, site: PipelineSite) -> None:
        super().__init__(settings)
        self.site = site

    @contextmanager
    def session(self, audit: AuditClient, *, headed: bool = False) -> Iterator[BrowserContext]:
        with super().session(audit, headed=headed) as context:
            def offline(route: Route) -> None:
                requested = urlsplit(route.request.url)
                if requested.hostname == "suno.com":
                    response = route.fetch(url=self.site.base_url + requested.path)
                    route.fulfill(response=response)
                else:
                    route.abort("blockedbyclient")
            context.route("**/*", offline)
            yield context


@pytest.fixture
def live_pipeline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, pipeline_site: PipelineSite):
    monkeypatch.setenv("SUNO_SERVICE_TOKEN", TOKEN)
    settings = Settings(tmp_path / "ai_videos" / "offline_pipeline", poll_seconds=0.05, generation_timeout=10)
    container = Container()
    container.settings.override(settings)
    runtime = container.runtime()
    runtime.browser = FixtureBrowserClient(settings, pipeline_site)
    app = create_app(container, worker=True)
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", log_level="error", lifespan="on"))
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    thread = threading.Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 15
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.05)
        assert server.started, "真实 uvicorn HTTP 服务未启动"
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10) as client:
            assert client.get("/health").json() == {"status": "ok", "worker": True, "automation_paused": False, "browser_window": "not_used"}
            yield client, settings, pipeline_site
    finally:
        server.should_exit = True
        thread.join(timeout=20)
        listener.close()
        container.unwire()
        assert not thread.is_alive(), "测试启动的 uvicorn 未退出"
        assert runtime.thread is None or not runtime.thread.is_alive(), "测试启动的 worker 未退出"


def wait_for_job(client: httpx.Client, job_id: str, expected: str) -> dict:
    deadline = time.monotonic() + 25
    while time.monotonic() < deadline:
        response = client.get(f"/v1/jobs/{job_id}")
        assert response.status_code == 200
        job = response.json()
        if job["status"] == expected:
            return job
        assert job["status"] not in {"needs_attention", "needs_login", "uncertain", "completed", "failed"}, job
        time.sleep(0.05)
    pytest.fail(f"任务未达到 {expected}: {job}")


def submit_job(client: httpx.Client, key: str) -> str:
    response = client.post("/v1/jobs", headers={"Idempotency-Key": key}, json={
        "prompt": "离线测试：温暖钢琴\nGentle strings", "format": "wav", "instrumental": True,
    })
    assert response.status_code == 202, response.text
    return response.json()["id"]


def assert_delivered(client: httpx.Client, settings: Settings, site: PipelineSite, job: dict) -> None:
    expected_urls = [f"https://suno.com/song/{song_id}" for song_id in SONG_IDS[:2]]
    assert job["status"] == "completed" and job["song_urls"] == expected_urls
    assert len(job["files"]) == 2 and job["error"] is None
    output = settings.data_dir / "outputs" / job["id"]
    assert not list(output.glob("*.part"))
    assert len(list(output.glob("*.wav"))) == 2
    for file in job["files"]:
        response = client.get(f"/v1/jobs/{job['id']}/files/{file['name']}")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("audio/wav")
        assert response.content == (output / file["name"]).read_bytes() == site.audio
        assert len(response.content) == file["bytes"]
        assert hashlib.sha256(response.content).hexdigest() == file["sha256"]
    with sqlite3.connect(settings.data_dir / "jobs.sqlite3") as connection:
        status, payload = connection.execute("SELECT status,payload FROM jobs WHERE id=?", (job["id"],)).fetchone()
        assert status == "completed"
        assert json.loads(payload)["files"] == job["files"]
    assert len(site.submissions) == 1
    assert site.submissions[0] == {
        "style": job["prompt"], "title": "suno-job-" + job["id"], "lyrics": "", "instrumental": True,
    }


def test_http_worker_chrome_sqlite_to_two_downloaded_files(live_pipeline) -> None:
    client, settings, site = live_pipeline
    job_id = submit_job(client, "offline-complete")
    job = wait_for_job(client, job_id, "completed")
    assert_delivered(client, settings, site, job)
    assert site.downloads == {SONG_IDS[0]: 1, SONG_IDS[1]: 1}
    assert submit_job(client, "offline-complete") == job_id
    assert len(site.submissions) == 1


def test_second_download_failure_resume_only_collects_missing_file(live_pipeline) -> None:
    client, settings, site = live_pipeline
    site.fail_second_once = True
    job_id = submit_job(client, "offline-recovery")
    paused = wait_for_job(client, job_id, "needs_attention")
    assert paused["error"]["code"] == "invalid_audio"
    assert len(paused["files"]) == 1
    first = paused["files"][0]
    first_path = settings.data_dir / "outputs" / job_id / first["name"]
    first_mtime = first_path.stat().st_mtime_ns
    assert client.get(f"/v1/jobs/{job_id}/files/{SONG_IDS[1]}.wav").status_code == 404
    assert client.get(f"/v1/jobs/{job_id}/files/{SONG_IDS[1]}.wav.part").status_code == 404
    assert site.downloads == {SONG_IDS[0]: 1, SONG_IDS[1]: 1}
    resumed = client.post(f"/v1/jobs/{job_id}/resume", json={})
    assert resumed.status_code == 202, resumed.text
    job = wait_for_job(client, job_id, "completed")
    assert_delivered(client, settings, site, job)
    assert job["files"][0] == first
    assert first_path.stat().st_mtime_ns == first_mtime
    assert site.downloads == {SONG_IDS[0]: 1, SONG_IDS[1]: 2}
