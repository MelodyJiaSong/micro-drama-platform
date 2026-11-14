import hashlib
import io
import json
import wave
from pathlib import Path

import pytest

from projects.suno_browser_service.tests.api.test_jobs import api, headers, submit
from projects.suno_browser_service.libs.application.commands.job__command import JobCommand
from projects.suno_browser_service.libs.application.dtos.job__dto import JobCdto
from projects.suno_browser_service.libs.common.settings import Settings


def audio() -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as stream:
        stream.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
        stream.writeframes(b"\0\0" * 8000)
    return buffer.getvalue()


def test_asset_plan_submit_preserves_requested_controls(api):
    client, container, root = api
    payload = audio()
    response = client.post("/v1/assets", headers=headers(), files={"file": ("我的参考.wav", payload)}, data={"rights_confirmed": "true"})
    assert response.status_code == 201, response.text
    asset = response.json()
    assert asset["id"] == hashlib.sha256(payload).hexdigest()
    assert asset["rights_confirmed"] and asset["storage_scope"] == "local"
    request = {"prompt": "Soft strings", "options": {"model": "v6-wild", "variety": 0, "style_influence": 70, "audio_influence": 35, "max_mode": False},
               "references": [{"asset_id": asset["id"]}]}
    plan = client.post("/v1/plan", headers=headers(), json=request)
    assert plan.status_code == 200 and plan.json()["browser_called"] is False
    assert client.get("/v1/jobs", headers=headers()).json() == []
    job = client.post("/v1/jobs", headers=headers("options-1"), json=request)
    assert job.status_code == 202, job.text
    assert job.json()["request"]["options"] == request["options"]
    same = client.post("/v1/jobs", headers=headers("options-1"), json=request)
    assert same.json()["id"] == job.json()["id"]
    request["options"]["variety"] = 10
    assert client.post("/v1/jobs", headers=headers("options-1"), json=request).status_code == 409
    (root / "assets" / asset["stored_name"]).write_bytes(b"changed")
    assert client.post("/v1/jobs", headers=headers("changed-asset"), json=request).json()["error"]["code"] == "asset_changed"


@pytest.mark.parametrize("body", [
    {"mode": "unknown"}, {"options": {"typo": 5}}, {"options": {"weirdness": 101}},
    {"options": {"style_influence": -1}}, {"options": {"duration_seconds": 481}},
    {"options": {"audio_influence": 20}}, {"options": {"vocal_gender": "male"}},
    {"mode": "sounds", "options": {"model": "v6"}}, {"mode": "sounds", "instrumental": False},
    {"mode": "sounds", "options": {"duration_seconds": 5}}, {"mode": "sounds", "prompt": "x" * 501},
    {"mode": "simple", "lyrics": "hello"}, {"options": {"bpm": 120}},
    {"references": [{"url": "https://evil.invalid/song/1"}]}, {"references": [{}]},
    {"references": [{"asset_id": "a"*64, "url": "https://suno.com/song/00000000-0000-4000-8000-000000000001"}]},
])
def test_conflicting_or_unknown_options_never_queue(api, body):
    client, _, _ = api
    assert submit(client, **body).status_code == 422
    assert client.get("/v1/jobs", headers=headers()).json() == []


@pytest.mark.parametrize("body", [
    {"mode": "simple", "instrumental": False},
    {"mode": "sounds", "options": {"sound_type": "loop", "bpm": 80}},
    {"options": {"weirdness": 0, "style_influence": 100, "max_mode": False}},
])
def test_supported_request_shapes(api, body):
    assert submit(api[0], **body).status_code == 202


@pytest.mark.parametrize("name,content", [("bad.exe", b"MZ"), ("fake.wav", b"hello"), ("../outside.wav", b"RIFF"), ("empty.wav", b"")])
def test_upload_validation(api, name, content):
    client, _, _ = api
    assert client.post("/v1/assets", headers=headers(), files={"file": (name, content)}).status_code == 422


def test_mislabeled_image_is_not_accepted(api):
    assert api[0].post("/v1/assets", headers=headers(), files={"file": ("fake.png", audio())}).status_code == 422


@pytest.mark.parametrize("method,path", [("get", "/v1/capabilities"), ("post", "/v1/plan"), ("post", "/v1/assets"), ("get", "/v1/assets/" + "a"*64)])
def test_new_routes_require_auth(api, method, path):
    assert api[0].request(method, path, json={"prompt": "music"}).status_code == 401


def test_old_job_fingerprint_is_compatible_with_new_defaults(api):
    client, container, _ = api
    job = submit(client, key="legacy").json()
    dao = container.command().reader.get(job["id"])
    original_payload = {"prompt": job["prompt"], "format": "mp3", "instrumental": True, "target": str(api[2]), "lyrics": None}
    fingerprint = hashlib.sha256(json.dumps(original_payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    assert dao.fingerprint == fingerprint
    assert submit(client, key="legacy", mode="advanced", options={}, references=[]).json()["id"] == job["id"]


def test_capabilities_advertise_live_gaps_and_schema(api):
    data = api[0].get("/v1/capabilities", headers=headers()).json()
    assert set(data["modes"]) == {"advanced", "simple", "sounds"}
    assert not any(m["live_verified"] for m in data["modes"].values())
    assert "references" in data["request_schema"]["properties"]
