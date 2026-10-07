from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
from threading import Event, Thread
from typing import Iterator

import pytest

from libs.common.options import FILE_PREFIX, PROGRESS_PREFIX
from libs.infrastructure.clients.process__client import ProcessClient
from libs.infrastructure.daos.download__dao import DownloadDao
from libs.infrastructure.errors.download__error import DownloadFailedError
from libs.infrastructure.writers.download__writer import DownloadWriter


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def run_media(arguments: list[str], directory: Path) -> None:
    result = subprocess.run(arguments, cwd=directory, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr


@pytest.fixture(scope="module")
def media_server(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    missing = [name for name in ("ffmpeg", "ffprobe") if not shutil.which(name)]
    if missing:
        pytest.skip("真实媒体集成缺少依赖：" + ", ".join(missing))
    if not shutil.which("deno") and not shutil.which("node"):
        pytest.skip("DownloadWriter 需要真实 Deno 或 Node")
    root = tmp_path_factory.mktemp("http-media")
    source = root / "fixture.mp4"
    run_media([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=10",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100",
        "-t", "2", "-c:v", "libx264", "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", "-c:a", "aac", str(source),
    ], root)
    run_media([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-map", "0:v", "-map", "0:v", "-map", "0:a",
        "-c:v", "libx264", "-preset", "ultrafast", "-g", "10",
        "-filter:v:0", "scale=640:360", "-filter:v:1", "scale=1280:720",
        "-b:v:0", "400k", "-b:v:1", "800k", "-c:a", "aac",
        "-f", "dash", "-seg_duration", "1", "-use_template", "1",
        "-use_timeline", "1", "-adaptation_sets", "id=0,streams=v id=1,streams=a",
        "split.mpd",
    ], root)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(root)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def download(url: str, destination: Path, mode: str = "video", height: int = 0) -> tuple[Path, list[str]]:
    logs: list[str] = []
    paths = DownloadWriter(ProcessClient()).download(
        DownloadDao(url, str(destination), mode, height, ""), Event(), logs.append,
    )
    assert len(paths) == 1, logs
    path = Path(paths[0])
    assert path.is_file(), logs
    assert path.parent == destination.resolve()
    assert any(line.startswith(FILE_PREFIX) for line in logs), logs
    return path, logs


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, timeout=20,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_mp4_contains_readable_video_and_audio(media_server: str, tmp_path: Path) -> None:
    path, logs = download(f"{media_server}/fixture.mp4", tmp_path / "中文 目录")
    info = probe(path)
    assert path.suffix == ".mp4"
    assert "mp4" in info["format"]["format_name"].split(",")
    assert {stream["codec_type"] for stream in info["streams"]} == {"video", "audio"}
    assert float(info["format"]["duration"]) >= 1.9
    assert any(line.startswith(PROGRESS_PREFIX) for line in logs), logs


def test_mp3_conversion_returns_audio_only(media_server: str, tmp_path: Path) -> None:
    path, logs = download(f"{media_server}/fixture.mp4", tmp_path, "mp3")
    info = probe(path)
    assert path.suffix == ".mp3"
    assert info["format"]["format_name"] == "mp3"
    assert len(info["streams"]) == 1
    assert info["streams"][0]["codec_type"] == "audio"
    assert info["streams"][0]["codec_name"] == "mp3"
    assert any("[ExtractAudio]" in line for line in logs), logs
    assert not list(tmp_path.glob("*.mp4"))


def test_existing_complete_file_is_unchanged(media_server: str, tmp_path: Path) -> None:
    path, _ = download(f"{media_server}/fixture.mp4", tmp_path)
    original_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    original_size = path.stat().st_size
    original_mtime = path.stat().st_mtime_ns
    repeated_path, logs = download(f"{media_server}/fixture.mp4", tmp_path)
    assert repeated_path == path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == original_hash
    assert path.stat().st_size == original_size
    assert path.stat().st_mtime_ns == original_mtime
    assert any("already been downloaded" in line for line in logs), logs


def test_http_failure_preserves_existing_files(media_server: str, tmp_path: Path) -> None:
    protected = tmp_path / "existing.mp4"
    protected.write_bytes(b"existing user file")
    original_hash = hashlib.sha256(protected.read_bytes()).hexdigest()
    logs: list[str] = []
    with pytest.raises(DownloadFailedError, match="404"):
        DownloadWriter(ProcessClient()).download(
            DownloadDao(f"{media_server}/missing.mp4", str(tmp_path), "video", 0, ""),
            Event(), logs.append,
        )
    assert not any(line.startswith(FILE_PREFIX) for line in logs), logs
    assert hashlib.sha256(protected.read_bytes()).hexdigest() == original_hash
    assert list(tmp_path.iterdir()) == [protected]


@pytest.mark.parametrize("height", [360, 720])
def test_split_streams_merge_with_height_limit(media_server: str, tmp_path: Path, height: int) -> None:
    path, logs = download(f"{media_server}/split.mpd", tmp_path, height=height)
    info = probe(path)
    video = [stream for stream in info["streams"] if stream["codec_type"] == "video"]
    audio = [stream for stream in info["streams"] if stream["codec_type"] == "audio"]
    assert len(video) == len(audio) == 1
    assert video[0]["height"] == height
    assert path.suffix == ".mp4"
    assert any("[Merger]" in line for line in logs), logs


def test_unavailable_height_fails_without_larger_fallback(media_server: str, tmp_path: Path) -> None:
    logs: list[str] = []
    with pytest.raises(DownloadFailedError, match="Requested format is not available"):
        DownloadWriter(ProcessClient()).download(
            DownloadDao(f"{media_server}/split.mpd", str(tmp_path), "video", 280, ""),
            Event(), logs.append,
        )
    assert not any(line.startswith(FILE_PREFIX) for line in logs), logs
    assert not list(tmp_path.iterdir())


def test_missing_final_file_is_failure(media_server: str, tmp_path: Path) -> None:
    removed: list[Path] = []

    def remove_final_file(line: str) -> None:
        if line.startswith(FILE_PREFIX):
            path = Path(json.loads(line[len(FILE_PREFIX):]))
            assert path.parent == tmp_path.resolve()
            assert path.is_file()
            path.unlink()
            removed.append(path)

    with pytest.raises(DownloadFailedError, match="没有返回可用的最终文件"):
        DownloadWriter(ProcessClient()).download(
            DownloadDao(f"{media_server}/fixture.mp4", str(tmp_path), "video", 0, ""),
            Event(), remove_final_file,
        )
    assert len(removed) == 1
    assert not list(tmp_path.iterdir())
