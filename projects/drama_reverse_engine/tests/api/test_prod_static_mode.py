from __future__ import annotations

from pathlib import Path

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient

import apps.api.app_factory as app_factory
from apps.api.container import Container
from apps.api.routes import GUARDED_ROUTES
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


@pytest.fixture()
def prod_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """serve_static=True with a real dist dir: the static mount at '/' must never
    shadow a state-changing API route into a 405 (development.md move 1)."""
    monkeypatch.delenv("DRE_API_TOKEN", raising=False)
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html><body>ui</body></html>", encoding="utf-8")
    monkeypatch.setattr(app_factory, "_UI_DIST", dist)
    container = Container()
    container.workspace.override(providers.Object(SafeWorkspace(root=str(tmp_path / "ws"))))
    return TestClient(app_factory.create_app(serve_static=True, container=container))


def test_static_index_served(prod_client: TestClient) -> None:
    resp = prod_client.get("/")
    assert resp.status_code == 200 and "ui" in resp.text


def test_no_guarded_route_returns_405_under_static_mount(prod_client: TestClient) -> None:
    for method, path in GUARDED_ROUTES:
        concrete = path.replace("{drama_id}", "d1")
        resp = prod_client.request(method, concrete)
        assert resp.status_code != 405, f"{method} {concrete} shadowed by static mount (405)"


def test_openapi_covers_every_guarded_route(prod_client: TestClient) -> None:
    """Sweep-completeness self-check: GUARDED_ROUTES must list every state-changing
    route in the OpenAPI schema (so new routes can't dodge the sweep)."""
    schema = prod_client.get("/api/openapi.json").json()
    mutating = {
        (method.upper(), path)
        for path, methods in schema["paths"].items()
        for method in methods
        if method.upper() in ("POST", "PUT", "DELETE", "PATCH")
    }
    assert mutating == set(GUARDED_ROUTES)
