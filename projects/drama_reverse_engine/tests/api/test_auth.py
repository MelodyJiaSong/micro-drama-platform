from __future__ import annotations

from pathlib import Path

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient

from apps.api.app_factory import create_app
from apps.api.container import Container
from apps.api.routes import GUARDED_ROUTES
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


@pytest.fixture()
def secured_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("DRE_API_TOKEN", "secret-token")
    container = Container()
    container.workspace.override(providers.Object(SafeWorkspace(root=str(tmp_path))))
    return TestClient(create_app(serve_static=False, container=container))


def test_health_stays_public(secured_client: TestClient) -> None:
    assert secured_client.get("/api/health").status_code == 200


def test_all_guarded_routes_refuse_without_token(secured_client: TestClient) -> None:
    for method, path in GUARDED_ROUTES:
        concrete = path.replace("{drama_id}", "d1")
        resp = secured_client.request(method, concrete)
        assert resp.status_code == 401, f"{method} {concrete} -> {resp.status_code}"
        assert "secret-token" not in resp.text


def test_wrong_token_refused_right_token_passes_auth(secured_client: TestClient) -> None:
    assert secured_client.get("/api/dramas", headers={"x-api-token": "nope"}).status_code == 401
    assert secured_client.get("/api/dramas", headers={"x-api-token": "secret-token"}).status_code == 200
