import sys
from typing import Callable

from libs.common.types import Auth
from libs.infrastructure.clients.process__client import ProcessClient

_BASE = [sys.executable, "-m", "yt_dlp", "--ignore-config", "--no-warnings", "--no-playlist"]


class YtdlpClient:
    def __init__(self, process: ProcessClient) -> None:
        self._process = process

    def capture(self, arguments: list[str], auth: Auth) -> str:
        return self._process.capture("yt-dlp", _BASE + auth.arguments() + arguments)

    def stream(self, arguments: list[str], auth: Auth, notify: Callable[[str], None]) -> None:
        self._process.stream("yt-dlp", _BASE + ["--newline"] + auth.arguments() + arguments, notify)
