"""Runs the fake 即梦 site on 127.0.0.1 (page port + separate control port) in background threads.

Usage in a conftest:  `from tests.fixtures.fake_jimeng_site.server import fake_jimeng_site  # noqa: F401`
"""
from __future__ import annotations

import json
import socket
import threading
import time
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
import uvicorn
from starlette.applications import Starlette

from tests.fixtures.fake_jimeng_site.control import FakeControlEndpoints
from tests.fixtures.fake_jimeng_site.endpoints import FakePageEndpoints
from tests.fixtures.fake_jimeng_site.media import FixtureVideo, make_video
from tests.fixtures.fake_jimeng_site.state import FakeSiteState

LOOPBACK: str = "127.0.0.1"
CONTROL_ATTEMPTS: int = 3
LOCAL_OPENER: urllib.request.OpenerDirector = urllib.request.build_opener(urllib.request.ProxyHandler({}))
"""Loopback calls must never be routed through a proxy picked up from the environment."""


class _ThreadedServer:
    def __init__(self, app: Starlette) -> None:
        self._server = uvicorn.Server(
            uvicorn.Config(app, log_level="warning", access_log=False, lifespan="off", loop="asyncio")
        )
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((LOOPBACK, 0))
        self.port: int = self._socket.getsockname()[1]
        self._thread = threading.Thread(target=self._server.run, kwargs={"sockets": [self._socket]}, daemon=True)

    def start(self, timeout_s: float = 10.0) -> None:
        self._thread.start()
        deadline = time.monotonic() + timeout_s
        while not self._server.started:
            if time.monotonic() > deadline:
                raise RuntimeError("fake site server did not start")
            time.sleep(0.02)

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=10)
        self._socket.close()


class FakeJimengSite:
    def __init__(self, video: FixtureVideo) -> None:
        self.video = video
        self.state = FakeSiteState(video.data)
        self._page = _ThreadedServer(Starlette(routes=FakePageEndpoints(self.state).routes()))
        self._control = _ThreadedServer(Starlette(routes=FakeControlEndpoints(self.state).routes()))

    @property
    def origin(self) -> str:
        return f"http://{LOOPBACK}:{self._page.port}"

    @property
    def generate_url(self) -> str:
        return f"{self.origin}/ai-tool/generate?type=video&workspace=0"

    @property
    def elements_url(self) -> str:
        return f"{self.origin}/ai-tool/elements"

    @property
    def control_url(self) -> str:
        return f"http://{LOOPBACK}:{self._control.port}/__fake__"

    def start(self) -> None:
        self._page.start()
        self._control.start()

    def stop(self) -> None:
        self._page.stop()
        self._control.stop()

    def reset(self) -> None:
        self.state.reset()

    def inject(self, name: str, times: int = 1, **params: object) -> None:
        self.state.inject(name, times, **params)

    def clear_fault(self, name: str) -> None:
        self.state.clear_fault(name)

    def hold(self, gate: str) -> None:
        self.state.hold(gate)

    def release(self, gate: str) -> None:
        self.state.release(gate)

    def counts(self) -> dict[str, int]:
        with self.state.lock:
            return self.state.ledger.counts()

    def control(self, action: str, payload: dict[str, object] | None = None) -> dict[str, object]:
        """Same operations over HTTP, for harnesses running the service in another process."""
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.control_url}/{action}", data=data, method="GET" if payload is None else "POST",
            headers={"content-type": "application/json"},
        )
        for attempt in range(CONTROL_ATTEMPTS):
            try:
                with LOCAL_OPENER.open(request, timeout=10) as response:
                    return json.loads(response.read().decode("utf-8"))
            except (ConnectionResetError, ConnectionAbortedError):
                if attempt == CONTROL_ATTEMPTS - 1:
                    raise
                time.sleep(0.2)
        raise AssertionError("unreachable")


@contextmanager
def running_fake_site(media_cache: Path) -> Iterator[FakeJimengSite]:
    site = FakeJimengSite(make_video(media_cache))
    site.start()
    try:
        yield site
    finally:
        site.stop()


@pytest.fixture(scope="session")
def fake_jimeng_site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[FakeJimengSite]:
    with running_fake_site(tmp_path_factory.mktemp("fake_jimeng_media")) as site:
        yield site
