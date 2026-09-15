from __future__ import annotations

import asyncio
import socket
import threading
import time
from collections.abc import Iterator
from pathlib import Path

import httpx2
import pytest
import uvicorn
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

from apps.api.app_factory import create_app
from apps.api.container import Container
from libs.application.queries.app_settings__query import AppSettingsQuery
from libs.infrastructure.readers.env_file__reader import EnvFileReader
from tests.api.support import write_test_global_toml

TOKEN = "m" * 40


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture(scope="module")
def server_url(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    root = tmp_path_factory.mktemp("mcp")
    project = root / "repo" / "projects" / "jimeng_web_bridge"
    (project / "config").mkdir(parents=True)
    port = _free_port()
    write_test_global_toml(project / "config" / "global.toml", port)
    settings = AppSettingsQuery(EnvFileReader()).load(
        project, {"JWB_TEST_MODE": "1", "JIMENG_BRIDGE_TOKEN": TOKEN, "JIMENG_BRIDGE_DATA_DIR": str(root / "data")}
    )
    container = Container(settings=settings)
    container.wire()
    server = uvicorn.Server(
        uvicorn.Config(create_app(settings, container), host="127.0.0.1", port=port, log_level="warning", proxy_headers=False)
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 15
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.05)
    assert server.started, "uvicorn did not start"
    yield f"http://127.0.0.1:{port}/mcp"
    server.should_exit = True
    thread.join(timeout=10)


async def _with_session(url: str, token: str | None):  # type: ignore[no-untyped-def]
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    async with httpx2.AsyncClient(headers=headers, timeout=20) as http:
        async with streamable_http_client(url, http_client=http) as transport:
            async with ClientSession(*transport) if isinstance(transport, tuple) else ClientSession(transport) as session:
                initialize = getattr(session, "initialize", None)
                if initialize is not None:
                    await initialize()
                tools = await session.list_tools()
                result = await session.call_tool("session_status", {})
                return tools, result


def test_mcp_lists_and_calls_tools_with_bearer(server_url: str) -> None:
    tools, result = asyncio.run(_with_session(server_url, TOKEN))
    names = {tool.name for tool in tools.tools}
    assert "session_status" in names
    assert not result.is_error
    assert set(result.structured_content or {}) >= {"web", "cli", "queues", "today_confirmed_credits", "test_mode"}
    assert not any(name in names for name in ("confirm_batch", "submit", "browser_submit"))


def test_mcp_without_bearer_is_refused(server_url: str) -> None:
    with pytest.raises(BaseException):
        asyncio.run(_with_session(server_url, None))


def test_mcp_rejects_browser_style_request_without_token(server_url: str) -> None:
    response = httpx2.post(
        server_url,
        headers={"Origin": server_url.rsplit("/mcp", 1)[0], "Sec-Fetch-Site": "same-origin", "Content-Type": "application/json"},
        content=b'{"jsonrpc":"2.0","id":1,"method":"tools/list"}',
    )
    assert response.status_code == 403
