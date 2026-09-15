from __future__ import annotations

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from libs.infrastructure.middleware.request_class__middleware import (
    REQUEST_CLASS_KEY,
    UI_SESSION_COOKIE,
    RequestClassMiddleware,
    RequestGatePolicy,
)
from libs.infrastructure.middleware.security_headers__middleware import SecurityHeadersMiddleware

PORT = 8790
TOKEN = "t" * 40
SESSION = "s" * 43
BASE = f"http://127.0.0.1:{PORT}"
SAME_ORIGIN = {"sec-fetch-site": "same-origin"}


async def _echo(request: Request) -> JSONResponse:
    return JSONResponse({"class": request.scope["state"][REQUEST_CLASS_KEY]})


def _client() -> TestClient:
    routes = [
        Route(path, _echo, methods=["GET", "POST", "PUT"])
        for path in ("/", "/api/health", "/api/jobs", "/ui-api/batches/b1/confirm", "/mcp", "/assets/app.js")
    ]
    app = SecurityHeadersMiddleware(
        RequestClassMiddleware(Starlette(routes=routes), RequestGatePolicy.for_local(PORT, TOKEN, SESSION))
    )
    return TestClient(app, base_url=BASE)


def _ui_cookie(client: TestClient, value: str = SESSION) -> None:
    client.cookies.set(UI_SESSION_COOKIE, value)


def test_unknown_host_is_rejected_even_with_valid_token() -> None:
    client = _client()
    response = client.get("/api/jobs", headers={"host": "evil.example:8790", "authorization": f"Bearer {TOKEN}"})
    assert response.status_code == 403


def test_forwarded_headers_do_not_change_the_host_check() -> None:
    client = _client()
    response = client.get(
        "/api/jobs",
        headers={"host": "evil.example", "x-forwarded-host": f"127.0.0.1:{PORT}", "authorization": f"Bearer {TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.parametrize("path", ["/", "/api/health", "/assets/app.js"])
def test_public_get_paths_need_no_credentials(path: str) -> None:
    response = _client().get(path)
    assert response.status_code == 200
    assert response.json() == {"class": "public"}


def test_public_paths_do_not_accept_writes_without_identity() -> None:
    assert _client().post("/").status_code == 403


def test_spa_deep_link_get_is_public_but_api_prefixes_are_not() -> None:
    routes = [Route(path, _echo, methods=["GET"]) for path in ("/queue", "/batches/b1", "/api/jobs", "/ui-api/x", "/mcp")]
    client = TestClient(
        RequestClassMiddleware(Starlette(routes=routes), RequestGatePolicy.for_local(PORT, TOKEN, SESSION)), base_url=BASE
    )
    assert client.get("/queue").json() == {"class": "public"}
    assert client.get("/batches/b1").json() == {"class": "public"}
    for protected in ("/api/jobs", "/ui-api/x", "/mcp"):
        assert client.get(protected).status_code == 403


def test_valid_bearer_is_classified_bearer() -> None:
    response = _client().get("/api/jobs", headers={"authorization": f"Bearer {TOKEN}"})
    assert response.json() == {"class": "bearer"}


@pytest.mark.parametrize("header", [f"Bearer {'x' * 40}", "Bearer ", f"Basic {TOKEN}", TOKEN])
def test_malformed_or_wrong_bearer_is_rejected(header: str) -> None:
    assert _client().get("/api/jobs", headers={"authorization": header}).status_code == 403


def test_bearer_can_never_reach_ui_api_even_with_browser_signals() -> None:
    client = _client()
    _ui_cookie(client)
    response = client.post(
        "/ui-api/batches/b1/confirm",
        headers={"authorization": f"Bearer {TOKEN}", "origin": BASE, **SAME_ORIGIN},
    )
    assert response.status_code == 403


def test_mcp_accepts_bearer() -> None:
    response = _client().post("/mcp", headers={"authorization": f"Bearer {TOKEN}"})
    assert response.json() == {"class": "bearer"}


def test_mcp_rejects_browser_identity() -> None:
    client = _client()
    _ui_cookie(client)
    assert client.post("/mcp", headers={"origin": BASE, **SAME_ORIGIN}).status_code == 403


def test_browser_read_with_session_cookie_is_ui() -> None:
    client = _client()
    _ui_cookie(client)
    response = client.get("/api/jobs", headers=SAME_ORIGIN)
    assert response.json() == {"class": "ui"}


def test_browser_confirm_with_cookie_and_origin_is_ui() -> None:
    client = _client()
    _ui_cookie(client)
    response = client.post("/ui-api/batches/b1/confirm", headers={"origin": BASE, **SAME_ORIGIN})
    assert response.json() == {"class": "ui"}


@pytest.mark.parametrize(
    ("cookie", "headers"),
    [
        (None, {"origin": BASE, **SAME_ORIGIN}),
        ("wrong", {"origin": BASE, **SAME_ORIGIN}),
        (SESSION, {"origin": BASE}),
        (SESSION, {"origin": BASE, "sec-fetch-site": "cross-site"}),
        (SESSION, {"origin": "http://evil.example", **SAME_ORIGIN}),
        (SESSION, SAME_ORIGIN),
    ],
)
def test_ui_write_requires_cookie_same_origin_fetch_and_origin(cookie: str | None, headers: dict[str, str]) -> None:
    client = _client()
    if cookie is not None:
        _ui_cookie(client, cookie)
    assert client.post("/ui-api/batches/b1/confirm", headers=headers).status_code == 403


def test_denial_body_does_not_echo_the_token() -> None:
    response = _client().get("/api/jobs", headers={"authorization": f"Bearer {'y' * 40}"})
    assert TOKEN not in response.text and "y" * 40 not in response.text


def test_security_headers_are_attached() -> None:
    response = _client().get("/api/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
