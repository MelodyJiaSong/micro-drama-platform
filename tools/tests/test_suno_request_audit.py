import json
from pathlib import Path

from tools import service_request
from tools.service_request import RequestLog


def test_standalone_service_request_scope(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(service_request, "__file__", str(tmp_path / "tools" / "service_request.py"))
    target = tmp_path / ".audit" / "service_requests" / "suno_browser_service" / "job-1"
    log = RequestLog(target)
    assert log.path == target.parent / "request_log.md"
    called = []

    def action() -> dict:
        assert '"event": "request"' in log.path.read_text(encoding="utf-8")
        called.append(True)
        return {"saved": True}

    assert log.invoke("suno-browser", "test-local-callback", {"prompt": "完整提示词"}, action) == {"saved": True}
    assert called == [True]
    body = log.path.read_text(encoding="utf-8")
    assert "完整提示词" in body and '"event": "result"' in body


def test_websocket_secrets_are_redacted() -> None:
    value = RequestLog.sanitize({"error": "Cannot connect to wss://user:pass@example.test/chromium/playwright?token=super-secret-123&keep=yes"})
    body = json.dumps(value)
    assert "super-secret-123" not in body and "user:pass" not in body
    assert "keep=yes" in body
