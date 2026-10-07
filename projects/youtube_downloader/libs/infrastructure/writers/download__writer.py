from collections import deque
import json
from pathlib import Path
import shutil
import sys
from threading import Event
from typing import Callable

from libs.common.options import FILE_PREFIX, PROGRESS_PREFIX
from libs.infrastructure.clients.process__client import ProcessClient
from libs.infrastructure.daos.download__dao import DownloadDao
from libs.infrastructure.errors.download__error import DownloadFailedError


class DownloadWriter:
    def __init__(self, client: ProcessClient) -> None:
        self.client = client

    def download(self, request: DownloadDao, cancel: Event, notify: Callable[[str], None]) -> tuple[str, ...]:
        missing = [name for name in ("ffmpeg", "ffprobe") if not shutil.which(name)]
        if missing:
            raise DownloadFailedError("缺少 " + ", ".join(missing) + "，请安装 FFmpeg 并加入 PATH。")
        if not shutil.which("deno") and not shutil.which("node"):
            raise DownloadFailedError("缺少 JavaScript 运行时，请安装 Deno（推荐）。")
        directory = Path(request.directory).expanduser().resolve()
        directory.mkdir(parents=True, exist_ok=True)
        args = [sys.executable, "-m", "yt_dlp", "--ignore-config", "--no-playlist",
                "--no-overwrites", "--continue", "--part", "--newline", "--no-colors",
                "--encoding", "utf-8", "--socket-timeout", "20", "--retries", "3",
                "--fragment-retries", "3", "--windows-filenames", "--trim-filenames", "180",
                "--progress-delta", "0.3", "--progress-template",
                f"download:{PROGRESS_PREFIX}%(progress._percent_str)s|%(progress._speed_str)s|%(progress._eta_str)s",
                "--print", f"after_move:{FILE_PREFIX}%(filepath)j", "--no-simulate", "--no-quiet", "--progress",
                "-P", str(directory)]
        if not shutil.which("deno"):
            args.extend(["--js-runtimes", "node"])
        if request.mode == "mp3":
            args.extend(["-f", "ba/b", "-x", "--audio-format", "mp3", "--audio-quality", "0",
                         "-o", "%(title).120s [%(id)s].%(ext)s"])
        else:
            limit = f"[height<={request.height}]" if request.height else ""
            args.extend(["-f", f"bv*{limit}+ba/b{limit}", "--merge-output-format", "mp4",
                         "--remux-video", "mp4", "-o",
                         "%(title).120s [%(id)s] [%(height)sp].%(ext)s"])
        if request.browser:
            args.extend(["--cookies-from-browser", request.browser])
        args.extend(["--", request.url])
        paths: list[str] = []
        tail: deque[str] = deque(maxlen=12)

        def receive(line: str) -> None:
            if line.startswith(FILE_PREFIX):
                paths.append(json.loads(line[len(FILE_PREFIX):]))
            elif not line.startswith(PROGRESS_PREFIX):
                tail.append(line)
            notify(line)

        code = self.client.run(args, cancel, receive)
        if code != 0:
            raise DownloadFailedError("\n".join(tail) or f"下载进程退出，状态码 {code}。")
        if not paths or not all(Path(path).is_file() for path in paths):
            raise DownloadFailedError("下载进程没有返回可用的最终文件，请查看日志。")
        return tuple(paths)
