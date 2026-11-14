from pathlib import Path

from libs.infrastructure.clients.process__client import ProcessClient


class FfmpegClient:
    def __init__(self, process: ProcessClient) -> None:
        self._process = process

    def run(self, arguments: list[str], output: Path) -> None:
        self._process.capture("ffmpeg", ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                                         *arguments, output.name], cwd=output.parent)
