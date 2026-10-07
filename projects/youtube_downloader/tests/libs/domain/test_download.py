from pathlib import Path
from threading import Event

import pytest

from apps.desktop.container import Container
from libs.domain.errors.download__error import DownloadError
from libs.domain.value_objects.download__valueobject import Download


@pytest.mark.parametrize("url", [
    "https://www.youtube.com/watch?v=YE7VzlLtp-4&list=PL123",
    "https://youtu.be/YE7VzlLtp-4?t=20",
    "https://m.youtube.com/shorts/YE7VzlLtp-4",
    "https://youtube.com/live/YE7VzlLtp-4",
    " https://youtube.com/embed/YE7VzlLtp-4/ ",
])
def test_normalizes_only_requested_video(url: str) -> None:
    assert Download(url, "downloads").url == "https://www.youtube.com/watch?v=YE7VzlLtp-4"


@pytest.mark.parametrize("url", [
    "https://youtube.com.evil.example/watch?v=YE7VzlLtp-4",
    "https://youtube.com@evil.example/watch?v=YE7VzlLtp-4",
    "https://user:pass@youtube.com/watch?v=YE7VzlLtp-4",
    "ftp://youtube.com/watch?v=YE7VzlLtp-4",
    "file:///video.mp4",
    "https://youtube.com/playlist?list=PL123",
    "https://youtube.com/@blender",
    "https://youtube.com/watch?v=short",
    "https://youtube.com/watch?v=YE7VzlLtp-4&v=AAAAAAAAAAA",
    "https://youtube.com:443/watch?v=YE7VzlLtp-4",
    "https://youtube.com/watch?v=YE7VzlLtp%24",
])
def test_invalid_input_rejected_before_writer(url: str, tmp_path: Path) -> None:
    class ForbiddenWriter:
        def download(self, *args: object) -> None:
            pytest.fail("Invalid URL reached the external download boundary")

    container = Container()
    with container.writer.override(ForbiddenWriter()):
        with pytest.raises(DownloadError):
            container.command().download(url, str(tmp_path), "video", 1080, "", Event(), print)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("mode,height,browser,directory", [
    ("video", 999, "", "downloads"), ("exe", 1080, "", "downloads"),
    ("mp3", 1080, "arbitrary-browser", "downloads"), ("video", 1080, "", " "),
])
def test_invalid_options(mode: str, height: int, browser: str, directory: str) -> None:
    with pytest.raises(DownloadError):
        Download("https://youtu.be/YE7VzlLtp-4", directory, mode, height, browser)
