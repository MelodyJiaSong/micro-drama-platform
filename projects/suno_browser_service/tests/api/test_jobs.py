import hashlib
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from projects.suno_browser_service.apps.api.app_factory import create_app
from projects.suno_browser_service.apps.api.container import Container
from projects.suno_browser_service.libs.common.settings import Settings


TOKEN = "isolated-test-token-32-characters-long"
SONG_ID = "12345678-1234-1234-1234-123456789abc"
SONG_URL = f"https://suno.com/song/{SONG_ID}"


@pytest.fixture
def api(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SUNO_SERVICE_TOKEN", TOKEN)
    container = Container()
    container.settings.override(Settings(tmp_path))
    with TestClient(create_app(container, worker=False)) as client:
        yield client, container, tmp_path
    container.unwire()


def headers(key: str | None = None) -> dict[str, str]:
    result = {"Authorization": f"Bearer {TOKEN}"}
    if key is not None:
        result["Idempotency-Key"] = key
    return result


def submit(client: TestClient, key: str = "unique", **body: object):
    return client.post("/v1/jobs", headers=headers(key), json={"prompt": "安静的钢琴\n无歌词", **body})


def update_job(container: Container, job_id: str, status: str, **fields: object) -> None:
    command = container.command()
    dao = command.reader.get(job_id)
    assert dao is not None
    command.writer.save(replace(dao, status=status, payload={**dao.payload, **fields}))


def test_http_submit_query_list_consumer_contract(api):
    client, container, data_dir = api
    assert client.get("/health").status_code == 200
    response = submit(client)
    assert response.status_code == 202
    job = response.json()
    assert job["status"] == "queued"
    assert job["prompt"] == "安静的钢琴\n无歌词"
    assert job["format"] == "mp3" and job["instrumental"] is True
    assert job["files"] == job["song_urls"] == []
    assert job["error"] is None and job["created_at"] and job["updated_at"]
    assert client.get(f"/v1/jobs/{job['id']}", headers=headers()).json() == job
    assert client.get("/v1/jobs", headers=headers()).json() == [job]
    assert (data_dir / "jobs.sqlite3").is_file()
    assert container.runtime().thread is None


@pytest.mark.parametrize("auth", [None, "Bearer wrong", "Basic abc"])
@pytest.mark.parametrize("method,path,body", [
    ("post", "/v1/jobs", {"prompt": "music"}),
    ("get", "/v1/jobs", None),
    ("get", "/v1/jobs/missing", None),
    ("post", "/v1/jobs/missing/resume", {}),
    ("get", f"/v1/jobs/missing/files/{SONG_ID}.mp3", None),
])
def test_all_business_routes_require_auth(api, auth, method, path, body):
    client, _, _ = api
    request_headers = {"Idempotency-Key": "unauthorized"}
    if auth:
        request_headers["Authorization"] = auth
    response = client.request(method, path, headers=request_headers, json=body)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"
    assert client.get("/v1/jobs", headers=headers()).json() == []


def test_empty_persisted_token_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("SUNO_SERVICE_TOKEN", raising=False)
    (tmp_path / "service-token.txt").write_text("\n", encoding="utf-8")
    container = Container()
    container.settings.override(Settings(tmp_path))
    try:
        with TestClient(create_app(container, worker=False)) as client:
            response = client.post("/v1/jobs", headers={"Idempotency-Key": "no-auth"}, json={"prompt": "music"})
            assert response.status_code == 401, "空持久 token 不能使无 Authorization 的业务请求通过"
    except ValueError:
        pass
    finally:
        container.unwire()


def test_concurrent_same_key_is_one_persisted_job(api):
    client, _, _ = api
    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(lambda _: submit(client, "concurrent"), range(16)))
    assert {response.status_code for response in responses} == {202}
    assert len({response.json()["id"] for response in responses}) == 1
    assert len(client.get("/v1/jobs", headers=headers()).json()) == 1


@pytest.mark.parametrize("changed", [{"prompt": "different"}, {"format": "wav"}, {"instrumental": False, "lyrics": "Hello"}])
def test_same_key_different_payload_conflicts(api, changed):
    client, _, _ = api
    original = submit(client, "conflict").json()
    response = submit(client, "conflict", **changed)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "idempotency_conflict"
    assert client.get(f"/v1/jobs/{original['id']}", headers=headers()).json() == original


@pytest.mark.parametrize("body", [
    {"prompt": ""}, {"prompt": "   "}, {"prompt": "a" * 2001}, {"format": "flac"},
    {"instrumental": False}, {"instrumental": False, "lyrics": " "},
    {"lyrics": "a" * 5001}, {"unexpected": 1}, {"target": "../outside"},
    {"target": "ai_videos"}, {"target": "ai_videos_nonexistent/project"},
    {"target": "edu_videos"}, {"target": "edu_videos/nonexistent_series/t99"},
])
def test_invalid_create_inputs_rejected_without_job(api, body):
    client, _, _ = api
    assert submit(client, **body).status_code == 422
    assert client.get("/v1/jobs", headers=headers()).json() == []


@pytest.mark.parametrize("key", [None, "bad/key", "a" * 129])
def test_idempotency_key_required_and_validated(api, key):
    client, _, _ = api
    response = client.post("/v1/jobs", headers=headers(key), json={"prompt": "music"})
    assert response.status_code == 422


def test_unknown_jobs_are_404(api):
    client, _, _ = api
    assert client.get("/v1/jobs/unknown", headers=headers()).status_code == 404
    assert client.post("/v1/jobs/unknown/resume", headers=headers(), json={}).status_code == 404


def test_resume_unknown_submission_requires_songs_and_preserves_completed_file(api):
    client, container, _ = api
    job_id = submit(client).json()["id"]
    existing = {"name": f"{SONG_ID}.mp3", "bytes": 200, "sha256": "persisted", "song_url": SONG_URL}
    update_job(container, job_id, "uncertain", submitted=True, files=[existing])
    url = f"/v1/jobs/{job_id}/resume"
    rejected = client.post(url, headers=headers(), json={})
    assert rejected.status_code == 409
    assert rejected.json()["error"]["code"] == "song_urls_required"
    resumed = client.post(url, headers=headers(), json={"song_urls": [SONG_URL]})
    assert resumed.status_code == 202
    assert resumed.json()["status"] == "queued"
    assert resumed.json()["song_urls"] == [SONG_URL]
    assert resumed.json()["files"] == [existing]
    assert container.command().reader.get(job_id).payload["submitted"] is True
    assert client.post(url, headers=headers(), json={"song_urls": [SONG_URL]}).status_code == 409
    assert submit(client).json()["id"] == job_id


@pytest.mark.parametrize("song_urls", [
    ["http://127.0.0.1/"], ["file:///C:/secrets"], ["https://suno.com.evil.test/song/x"],
    ["https://suno.com@evil.test/song/x"], [SONG_URL + "?token=secret"], [SONG_URL, SONG_URL],
])
def test_resume_rejects_untrusted_song_urls(api, song_urls):
    client, container, _ = api
    job_id = submit(client).json()["id"]
    update_job(container, job_id, "uncertain", submitted=True)
    response = client.post(f"/v1/jobs/{job_id}/resume", headers=headers(), json={"song_urls": song_urls})
    assert response.status_code == 422
    assert client.get(f"/v1/jobs/{job_id}", headers=headers()).json()["status"] == "uncertain"


@pytest.mark.parametrize("status", ["queued", "preparing", "submitting", "waiting", "downloading", "completed"])
def test_resume_cannot_requeue_active_or_completed_job(api, status):
    client, container, _ = api
    job_id = submit(client).json()["id"]
    update_job(container, job_id, status, submitted=True, song_urls=[SONG_URL])
    response = client.post(f"/v1/jobs/{job_id}/resume", headers=headers(), json={"song_urls": [SONG_URL]})
    assert response.status_code == 409
    assert client.get(f"/v1/jobs/{job_id}", headers=headers()).json()["status"] == status


def test_file_download_uses_registered_job_metadata(api):
    client, container, data_dir = api
    job_id = submit(client).json()["id"]
    other_id = submit(client, "other").json()["id"]
    name = f"{SONG_ID}.mp3"
    output = data_dir / "outputs" / job_id
    output.mkdir(parents=True)
    audio = b"ID3" + b"audio" * 100
    (output / name).write_bytes(audio)
    metadata = {"name": name, "bytes": len(audio), "sha256": hashlib.sha256(audio).hexdigest(), "song_url": SONG_URL}
    update_job(container, job_id, "completed", submitted=True, song_urls=[SONG_URL], files=[metadata])
    job = client.get(f"/v1/jobs/{job_id}", headers=headers()).json()
    for file in job["files"]:
        response = client.get(f"/v1/jobs/{job['id']}/files/{file['name']}", headers=headers())
        assert response.status_code == 200
        assert len(response.content) == file["bytes"]
        assert hashlib.sha256(response.content).hexdigest() == file["sha256"]
        assert response.headers["content-type"].startswith("audio/mpeg")
    assert client.get(f"/v1/jobs/{other_id}/files/{name}", headers=headers()).status_code == 404
    unregistered = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.mp3"
    (output / unregistered).write_bytes(audio)
    assert client.get(f"/v1/jobs/{job_id}/files/{unregistered}", headers=headers()).status_code == 404


@pytest.mark.parametrize("name", ["..%2Fsecret", "..%5Csecret", "C:%5Csecret", "safe.mp3:secret", "%5C%5Cserver%5Cshare"])
def test_file_path_inputs_cannot_escape(api, name):
    client, _, _ = api
    job_id = submit(client).json()["id"]
    response = client.get(f"/v1/jobs/{job_id}/files/{name}", headers=headers())
    assert response.status_code == 404


@pytest.mark.parametrize("link_type", ["symlink", "junction"])
def test_job_output_directory_link_cannot_escape(api, link_type):
    client, container, data_dir = api
    job_id = submit(client).json()["id"]
    name = f"{SONG_ID}.mp3"
    outside = data_dir / "outside-output-root"
    outside.mkdir()
    (outside / name).write_bytes(b"private outside file")
    output = data_dir / "outputs"
    output.mkdir()
    link = output / job_id
    if link_type == "junction":
        if os.name != "nt":
            pytest.skip("Windows junction test")
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True, timeout=10)
        assert result.returncode == 0, result.stderr
    else:
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            pytest.skip(f"Windows symlink permission unavailable: {exc}")
    update_job(container, job_id, "completed", files=[{"name": name}])
    try:
        response = client.get(f"/v1/jobs/{job_id}/files/{name}", headers=headers())
        assert response.status_code == 404, "整个 job 目录链接到 outputs 根外时必须拒绝读取"
    finally:
        if link_type == "junction":
            link.rmdir()
