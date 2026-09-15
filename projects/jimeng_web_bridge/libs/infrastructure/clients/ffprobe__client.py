from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from libs.infrastructure.daos.output__dao import MediaProbeDao
from libs.infrastructure.errors.output__error import FfprobeFailedError, FfprobeUnavailableError

_NO_WINDOW: int = getattr(subprocess, "CREATE_NO_WINDOW", 0)
_STDERR_TAIL: int = 400


class FfprobeClient:
    """Reads duration and display size of a media file with `ffprobe` (argv list, never a shell)."""

    def __init__(self, executable: str | None = None, timeout_s: float = 60.0) -> None:
        self._executable = executable
        self._timeout_s = timeout_s

    def probe(self, path: Path) -> MediaProbeDao:
        argv = [self._resolve(), "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)]
        try:
            done = subprocess.run(argv, capture_output=True, timeout=self._timeout_s, check=False, creationflags=_NO_WINDOW)
        except FileNotFoundError as error:
            raise FfprobeUnavailableError(f"ffprobe 无法启动：{error}") from error
        except subprocess.TimeoutExpired as error:
            raise FfprobeFailedError(f"ffprobe 超时（{self._timeout_s:g} s）") from error
        if done.returncode != 0:
            tail = done.stderr.decode("utf-8", "replace")[-_STDERR_TAIL:].strip()
            raise FfprobeFailedError(f"ffprobe 读取失败（退出码 {done.returncode}）：{tail}")
        try:
            data = json.loads(done.stdout.decode("utf-8", "replace"))
        except ValueError as error:
            raise FfprobeFailedError("ffprobe 输出不是 JSON") from error
        stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
        if stream is None or not stream.get("width") or not stream.get("height"):
            raise FfprobeFailedError("文件里没有可读的画面流")
        width, height = int(stream["width"]), int(stream["height"])
        if abs(_rotation(stream)) % 180 == 90:
            width, height = height, width
        return MediaProbeDao(duration_s=_duration(data.get("format", {})), width=width, height=height)

    def _resolve(self) -> str:
        if self._executable is not None:
            if not Path(self._executable).is_file():
                raise FfprobeUnavailableError(f"ffprobe 不存在：{self._executable}")
            return self._executable
        found = shutil.which("ffprobe")
        if found is None:
            raise FfprobeUnavailableError("ffprobe 不在 PATH 上，无法校验下载结果")
        return found


def _duration(fmt: dict[str, object]) -> float | None:
    try:
        value = float(str(fmt.get("duration")))
    except ValueError:
        return None
    return value if value > 0 else None


def _rotation(stream: dict[str, object]) -> int:
    tags = stream.get("tags")
    if isinstance(tags, dict) and str(tags.get("rotate", "")).lstrip("-").isdigit():
        return int(str(tags["rotate"]))
    for side in stream.get("side_data_list", []) or []:
        if isinstance(side, dict) and "rotation" in side:
            try:
                return int(float(str(side["rotation"])))
            except ValueError:
                return 0
    return 0
