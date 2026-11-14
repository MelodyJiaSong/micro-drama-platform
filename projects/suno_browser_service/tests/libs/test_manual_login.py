from pathlib import Path

import pytest

from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import Settings
from projects.suno_browser_service.libs.infrastructure.clients.audit__client import AuditClient
from projects.suno_browser_service.libs.infrastructure.clients.manual_browser__client import ManualBrowserClient


def test_unwritable_audit_prevents_manual_browser_launch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    client = ManualBrowserClient(Settings(data_dir=tmp_path / "browser"))
    audit = AuditClient(tmp_path / "ai_videos" / "fixture")
    monkeypatch.setattr(client, "executable", lambda: Path("chrome.exe"))

    def fail(_event: dict) -> None:
        raise OSError("audit unavailable")

    def forbidden(*_args, **_kwargs):
        pytest.fail("browser launched before a durable request log")

    monkeypatch.setattr(audit.log, "append", fail)
    monkeypatch.setattr("projects.suno_browser_service.libs.infrastructure.clients.manual_browser__client.subprocess.Popen", forbidden)
    with pytest.raises(OSError, match="audit unavailable"):
        client.login(audit)


def test_remote_configuration_cannot_open_a_local_login_profile(tmp_path: Path) -> None:
    client = ManualBrowserClient(Settings(data_dir=tmp_path / "browser", endpoint="wss://example.invalid/playwright"))
    with pytest.raises(ServiceError) as error:
        client.login(AuditClient(tmp_path / "ai_videos" / "fixture"))
    assert error.value.code == "remote_login"
    assert not client.settings.profile_dir.exists()
