from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import sys
from threading import Event, Thread

import pytest

from libs.infrastructure.clients.process__client import ProcessClient
from libs.infrastructure.daos.download__dao import DownloadDao
from libs.infrastructure.writers.download__writer import DownloadWriter


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def test_writer_ignores_executable_user_config_and_preserves_literal_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not all(shutil.which(name) for name in ("ffmpeg", "ffprobe")):
        pytest.skip("Real security integration needs FFmpeg/ffprobe")
    if not shutil.which("deno") and not shutil.which("node"):
        pytest.skip("Real writer integration needs a JS runtime")
    for name in ("HOME", "USERPROFILE", "APPDATA", "XDG_CONFIG_HOME"):
        path = tmp_path / name.lower()
        path.mkdir()
        monkeypatch.setenv(name, str(path))
    config = tmp_path / "appdata" / "yt-dlp" / "config"
    config.parent.mkdir()
    config.write_text('--yes-playlist\n--exec "before_dl:echo CONFIG_EXECUTED>configuration.marker"\n',
                      encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "fixture.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "color=c=black:s=32x32:r=5", "-t", "0.4", "-c:v", "libx264", str(source)],
                   check=True, capture_output=True, timeout=15)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(tmp_path)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    marker = tmp_path / "configuration.marker"
    try:
        url = f"http://127.0.0.1:{server.server_port}/fixture.mp4"
        logs: list[str] = []
        code = ProcessClient().run([sys.executable, "-m", "yt_dlp", "--no-simulate",
                                   "-P", str(tmp_path / "control"), "-o", "control.%(ext)s", "--", url],
                                  Event(), logs.append)
        assert code == 0, logs
        assert marker.is_file(), "Control did not prove that this user config was loaded"
        assert (tmp_path / "control" / "control.mp4").is_file(), logs
        marker.unlink()
        destination = tmp_path / "保存 & $(literal)"
        paths = DownloadWriter(ProcessClient()).download(
            DownloadDao(url, str(destination), "video", 0, ""), Event(), logs.append,
        )
        assert len(paths) == 1
        assert Path(paths[0]).is_file() and Path(paths[0]).parent == destination.resolve()
        assert not marker.exists(), "User config command executed despite isolation"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
