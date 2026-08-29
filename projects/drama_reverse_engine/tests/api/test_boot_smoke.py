from __future__ import annotations

from fastapi.testclient import TestClient

from apps.api.app_factory import create_app


def test_health_returns_200_and_service_name() -> None:
    client = TestClient(create_app(serve_static=False))
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["service"] == "drama_reverse_engine"


def test_openapi_schema_served() -> None:
    client = TestClient(create_app(serve_static=False))
    assert client.get("/api/openapi.json").status_code == 200
