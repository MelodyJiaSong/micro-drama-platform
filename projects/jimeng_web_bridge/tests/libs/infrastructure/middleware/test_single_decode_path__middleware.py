from __future__ import annotations

import asyncio

import pytest
from starlette.types import Message, Receive, Scope, Send

from libs.infrastructure.middleware.single_decode_path__middleware import SingleDecodePathMiddleware


def _seen_path(scope: Scope) -> str:
    seen: list[str] = []

    async def app(inner: Scope, receive: Receive, send: Send) -> None:
        seen.append(inner["path"])

    async def receive() -> Message:
        return {"type": "http.request"}

    async def send(message: Message) -> None:
        return None

    asyncio.run(SingleDecodePathMiddleware(app)(scope, receive, send))
    return seen[0]


@pytest.mark.parametrize(
    ("raw_path", "transport_path", "expected"),
    [
        (b"/api/dramas/a%2Fb/config", "/api/dramas/a/b/config", "/api/dramas/a/b/config"),
        (b"/api/dramas/a%252Fb/config", "/api/dramas/a/b/config", "/api/dramas/a%2Fb/config"),
        (b"/api/thumbs?path=%252F", "/api/thumbs", "/api/thumbs"),
        (b"/api/dramas/%E9%BB%84/config", "/api/dramas/黄/config", "/api/dramas/黄/config"),
    ],
)
def test_path_is_exactly_one_decode_of_raw_path(raw_path: bytes, transport_path: str, expected: str) -> None:
    assert _seen_path({"type": "http", "path": transport_path, "raw_path": raw_path}) == expected


def test_scopes_without_raw_path_are_left_alone() -> None:
    assert _seen_path({"type": "http", "path": "/api/health"}) == "/api/health"
