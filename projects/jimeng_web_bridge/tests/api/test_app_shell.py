from __future__ import annotations

from pathlib import Path

import pytest
from starlette.testclient import TestClient

from apps.api.app_factory import create_app
from apps.api.container import Container
from libs.application.queries.app_settings__query import AppSettingsQuery
from libs.common.app_settings import StartupConfigError
from libs.infrastructure.readers.env_file__reader import EnvFileReader
from tests.api.support import write_test_global_toml

TOKEN = "z" * 40


def _project(tmp_path: Path, with_ui: bool = True) -> Path:
    project = tmp_path / "repo" / "projects" / "jimeng_web_bridge"
    (project / "config").mkdir(parents=True)
    write_test_global_toml(project / "config" / "global.toml")
    if with_ui:
        (project / "apps" / "api" / "static" / "assets").mkdir(parents=True)
        (project / "apps" / "api" / "static" / "index.html").write_text("<!doctype html><title>即梦桥接</title>", encoding="utf-8")
        (project / "apps" / "api" / "static" / "assets" / "app.js").write_text("console.log(1)", encoding="utf-8")
    return project


def _environ(tmp_path: Path, **extra: str) -> dict[str, str]:
    return {"JWB_TEST_MODE": "1", "JIMENG_BRIDGE_TOKEN": TOKEN, "JIMENG_BRIDGE_DATA_DIR": str(tmp_path / "data"), **extra}


def _client(tmp_path: Path, with_ui: bool = True) -> TestClient:
    settings = AppSettingsQuery(EnvFileReader()).load(_project(tmp_path, with_ui), _environ(tmp_path))
    container = Container(settings=settings)
    container.wire()
    return TestClient(create_app(settings, container), base_url=f"http://127.0.0.1:{settings.port}")


def test_boot_health_is_public_and_has_security_headers(tmp_path: Path) -> None:
    response = _client(tmp_path).get("/api/health")
    assert response.status_code == 200 and response.json() == {"ok": True}
    assert response.headers["x-content-type-options"] == "nosniff"


@pytest.mark.parametrize("path", ["/", "/queue", "/batches/b-1"])
def test_shell_serves_index_and_sets_strict_http_only_session_cookie(tmp_path: Path, path: str) -> None:
    response = _client(tmp_path).get(path)
    assert response.status_code == 200 and "即梦桥接" in response.text
    cookie = response.headers["set-cookie"].lower()
    assert "jwb_ui=" in cookie and "httponly" in cookie and "samesite=strict" in cookie


def test_static_assets_are_served(tmp_path: Path) -> None:
    assert _client(tmp_path).get("/assets/app.js").status_code == 200


def test_missing_ui_build_returns_actionable_503_not_blank(tmp_path: Path) -> None:
    response = _client(tmp_path, with_ui=False).get("/")
    assert response.status_code == 503 and response.json()["hint"] == "运行 make ui-build"


def test_unknown_api_path_is_gated_then_404_for_bearer(tmp_path: Path) -> None:
    client = _client(tmp_path)
    assert client.get("/api/nope").status_code == 403
    assert client.get("/api/nope", headers={"authorization": f"Bearer {TOKEN}"}).status_code == 404


def test_session_cookie_from_shell_grants_ui_identity_for_same_origin_reads(tmp_path: Path) -> None:
    client = _client(tmp_path)
    client.get("/")
    assert client.get("/api/health", headers={"sec-fetch-site": "same-origin"}).status_code == 200
    assert client.get("/api/nope", headers={"sec-fetch-site": "same-origin"}).status_code == 404


def test_startup_fails_closed_without_strong_token(tmp_path: Path) -> None:
    project = _project(tmp_path)
    with pytest.raises(StartupConfigError):
        AppSettingsQuery(EnvFileReader()).load(project, {"JWB_TEST_MODE": "1", "JIMENG_BRIDGE_TOKEN": "short"})


def test_test_mode_ignores_repo_root_env_file(tmp_path: Path) -> None:
    project = _project(tmp_path)
    (tmp_path / "repo" / ".env").write_text(f"JIMENG_BRIDGE_TOKEN={'r' * 40}\n", encoding="utf-8")
    with pytest.raises(StartupConfigError):
        AppSettingsQuery(EnvFileReader()).load(project, {"JWB_TEST_MODE": "1"})
    settings = AppSettingsQuery(EnvFileReader()).load(project, {})
    assert settings.bearer_token == "r" * 40 and not settings.test_mode


def test_settings_repr_never_contains_secrets(tmp_path: Path) -> None:
    settings = AppSettingsQuery(EnvFileReader()).load(_project(tmp_path), _environ(tmp_path))
    assert TOKEN not in repr(settings) and settings.ui_session not in repr(settings)
