from __future__ import annotations

import ast
import importlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Console(io.StringIO):
    def reconfigure(self, **kwargs):
        pass


def load(name, monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, "stdout", Console())
        m.syspath_prepend(str(ROOT))
        return importlib.import_module(name)


def events(path):
    return [json.loads(x) for x in re.findall(r"```json\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S)]


def test_eleven_image_records_payload_and_reference_before_post(tmp_path, monkeypatch):
    adapter = load("tools.image_fetch", monkeypatch)
    output = tmp_path / "ai_videos/demo/scenes/bg1/view.png"
    ref = tmp_path / "ref.png"
    ref.write_bytes(b"reference")
    log = adapter.RequestLog(output).path
    def post(method, path, key, payload, **kwargs):
        row = events(log)[0]["request"]
        assert row["body"]["prompt"] == "完整画面描述"
        assert row["body"]["images"][0]["content_base64"]["bytes"] == 9
        assert row["files"][0]["path"] == str(ref)
        assert "secret" not in log.read_text(encoding="utf-8")
        return {"id": "image-id"}
    monkeypatch.setattr(adapter, "_api_once", post)
    assert adapter.create("secret", "完整画面描述", model="gpt-image-2", quality="medium",
        aspect="16:9", resolution="2K", refs=[adapter.inline(ref)], target=output) == "image-id"
    assert events(log)[1]["response"]["id"] == "image-id"


def test_hyper3d_multipart_and_poll_are_logged_without_network(tmp_path, monkeypatch):
    adapter = load("tools.hyper3d_fetch", monkeypatch)
    output = tmp_path / "ai_videos/demo/props/p1/raw.glb"
    log = adapter.RequestLog(output).path
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self): return b'{"uuid":"rodin-id","jobs":{"subscription_key":"job-key"}}'
    def post(request, **kwargs):
        body = events(log)[0]["request"]["body"]
        assert body["prompt"] == "wooden cart" and body["bbox_condition"] == "[100, 50, 25]"
        assert b"wooden cart" in request.data
        return Response()
    monkeypatch.setattr(adapter.urllib.request, "urlopen", post)
    result = adapter.create_job("secret", "wooden cart", [], [4, 2, 1], "Sketch", "Raw", target=output)
    assert result["uuid"] == "rodin-id"
    monkeypatch.setattr(adapter, "_post_json_once", lambda *args: {"jobs": [{"status": "Done"}]})
    adapter.wait("secret", "job-key", 600, target=output)
    assert events(log)[2]["request"]["body"]["subscription_key"] == "job-key"


def test_generator_submission_callers_provide_log_scope():
    names = {"create", "create_job", "_dm_submit", "wait"}
    receivers = {"el", "rodin", "gba", "ba"}
    for path in (ROOT / "tools").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id in receivers and node.func.attr in names:
                    assert any(k.arg == "target" for k in node.keywords), f"{path.name}:{node.lineno}"


def test_unknown_submission_does_not_match_upload_retry(tmp_path, monkeypatch):
    adapter = load("tools.gen_bg_images", monkeypatch)
    for error in ("即梦没回 JSON、list_task 里也按 prompt 找不到（可能已提交扣费）：upload failed",
                  "即梦任务超时（积分已扣）：upload timeout", "即梦生成失败：upload failed", "connection timeout"):
        assert not adapter.RETRYABLE.search(error)
    assert adapter.RETRYABLE.search("upload failed before submission")
