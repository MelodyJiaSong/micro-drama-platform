from __future__ import annotations

import importlib.util
import io
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("service_request", Path(__file__).parents[1] / "service_request.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
RequestLog = MODULE.RequestLog


def events(path: Path) -> list[dict]:
    return [json.loads(x) for x in re.findall(r"```json\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S)]


@pytest.mark.parametrize("tail, expected", [
    ("2_世界观人设/characters/c1_A/a.png", "2_世界观人设/characters/request_log.md"),
    ("2_世界观人设/scenes/bg1/a.glb", "2_世界观人设/scenes/request_log.md"),
    ("2_世界观人设/background/bg1/a.png", "2_世界观人设/background/request_log.md"),
    ("episodes/ep01/scenes/s1/shots/st1/a.mp4", "episodes/ep01/request_log.md"),
    ("2_世界观人设/equipment/e1/a.png", "2_世界观人设/equipment/request_log.md"),
    ("5_6_分镜与prompt/episodes/ep01/shots/shot02/a.wav", "5_6_分镜与prompt/episodes/ep01/request_log.md"),
])
def test_scope_shares_by_episode_or_asset_group(tmp_path, tail, expected):
    root = tmp_path / "ai_videos" / "demo"
    assert RequestLog(root / tail).path == root / expected


def test_complete_request_precedes_call_and_secrets_are_redacted(tmp_path, monkeypatch):
    log = RequestLog(tmp_path / "ai_videos/demo/characters/c1/a.png")
    secret = "secret_test_value_123"
    monkeypatch.setenv("ELEVENLABS_API_KEY", secret)
    prompt = "完整台词\n" * 3000
    request = {"prompt": prompt, "headers": {"xi-api-key": secret}, "url": "https://example.com/file?signature=abc&format=png"}
    def call():
        first = events(log.path)
        assert len(first) == 1 and first[0]["request"]["prompt"] == prompt
        assert secret not in log.path.read_text(encoding="utf-8")
        return {"submit_id": "task-123", "consumed": 4}
    result = log.invoke("elevenlabs", "POST image", request, call)
    assert result["submit_id"] == "task-123"
    rows = events(log.path)
    assert rows[0]["request_id"] == rows[1]["request_id"]
    assert rows[1]["response"]["consumed"] == 4
    assert "abc" not in rows[0]["request"]["url"]


def test_errors_are_logged_without_retry(tmp_path):
    log = RequestLog(tmp_path / "ai_videos/demo/props/p1/a.glb")
    calls = []
    def call():
        calls.append(1)
        raise TimeoutError("submission outcome unknown")
    with pytest.raises(TimeoutError):
        log.invoke("hyper3d", "POST rodin", {"prompt": "box"}, call)
    assert len(calls) == 1
    assert [x["event"] for x in events(log.path)] == ["request", "error"]


def test_unwritable_log_prevents_paid_call(tmp_path, monkeypatch):
    log = RequestLog(tmp_path / "ai_videos/demo/characters/c1/a.png")
    calls = []
    monkeypatch.setattr(log, "append", lambda _: (_ for _ in ()).throw(OSError("disk full")))
    with pytest.raises(OSError):
        log.invoke("dreamina", "text2image", {}, lambda: calls.append(1))
    assert not calls
    with pytest.raises(ValueError):
        RequestLog(tmp_path / "no_owner.png")


def test_concurrent_append_keeps_all_requests_and_results(tmp_path):
    target = tmp_path / "ai_videos/demo/characters/c1/a.png"
    def call(n):
        return RequestLog(target).invoke("test", "query", {"n": n}, lambda: {"n": n})
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(call, range(16)))
    rows = events(RequestLog(target).path)
    assert len(rows) == 32
    assert len({x["request_id"] for x in rows}) == 16


def test_series_shared_assets_and_binary_reference_digest(tmp_path):
    root = tmp_path / "ai_videos/series"
    root.mkdir(parents=True)
    (root / "series.json").write_text("{}")
    image = root / "_series/characters/c1/a.png"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"ref-image")
    log = RequestLog(image)
    assert log.path == root / "_series/characters/request_log.md"
    assert log.sanitize(image)["bytes"] == 9
    assert log.sanitize({"content_base64": "cmVmLWltYWdl"})["content_base64"]["bytes"] == 9


def test_multipart_file_hash_preserves_stream_position():
    stream = io.BytesIO(b"inline-reference")
    stream.seek(3)
    result = RequestLog.sanitize(stream)
    assert result["bytes"] == 16 and stream.tell() == 3


def test_cli_stdout_embedded_signed_url_and_json_credentials_are_redacted():
    stdout = json.dumps({"url": "https://example.com/result?signature=signed-secret&format=png",
                         "access_token": "oauth-secret"})
    clean = RequestLog.sanitize(stdout)
    assert "signed-secret" not in clean and "oauth-secret" not in clean
    assert "format=png" in clean


def test_download_logs_each_attempt_and_digest_before_return(tmp_path, monkeypatch):
    output = tmp_path / "ai_videos/demo/characters/c1/video.part.mp4"
    log = RequestLog(output)
    class Response(io.BytesIO):
        status = 200
        headers = {}
    def get(request, **kwargs):
        assert events(log.path)[0]["request"]["attempt"] == 2
        assert "signature=abc" not in log.path.read_text(encoding="utf-8")
        return Response(b"video-bytes")
    monkeypatch.setattr(MODULE.urllib.request, "urlopen", get)
    assert log.download("dreamina", "https://example.com/file?signature=abc", output, timeout=300, attempt=2) == 11
    assert output.read_bytes() == b"video-bytes"
    assert events(log.path)[1]["response"]["file"]["bytes"] == 11
