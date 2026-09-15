from __future__ import annotations

import io
import json
import os
import time
from pathlib import Path

import pytest
from PIL import Image

from libs.infrastructure.clients.toast__client import ToastClient
from libs.infrastructure.errors.artifact__error import (
    ArtifactTooLargeError,
    InvalidArtifactNameError,
    UnsupportedThumbnailSourceError,
)
from libs.infrastructure.readers.thumbnail__reader import ThumbnailReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter


def _png(width: int, height: int, noisy: bool = False) -> bytes:
    image = Image.effect_noise((width, height), 90).convert("RGB") if noisy else Image.new("RGB", (width, height), (120, 130, 140))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_thumbnail_bounds_long_edge_and_caches(tmp_path: Path) -> None:
    source = tmp_path / "bg11-1.png"
    source.write_bytes(_png(1600, 900))
    reader = ThumbnailReader(tmp_path / "cache")
    first = reader.thumbnail(source, max_edge=320)
    assert (first.width, first.height) == (320, 180) and first.content_type == "image/jpeg"
    mtime = first.path.stat().st_mtime_ns
    second = reader.thumbnail(source, max_edge=320)
    assert second.path == first.path and second.path.stat().st_mtime_ns == mtime


def test_thumbnail_rejects_video_and_garbage(tmp_path: Path) -> None:
    reader = ThumbnailReader(tmp_path / "cache")
    video = tmp_path / "shot01_previz.mp4"
    video.write_bytes(b"\x00\x00\x00\x18ftypisom")
    with pytest.raises(UnsupportedThumbnailSourceError):
        reader.thumbnail(video, 320)
    fake_png = tmp_path / "broken.png"
    fake_png.write_bytes(b"not an image")
    with pytest.raises(UnsupportedThumbnailSourceError):
        reader.thumbnail(fake_png, 320)


def test_preview_is_compressed_under_budget(tmp_path: Path) -> None:
    writer = ArtifactWriter(tmp_path / "artifacts")
    artifact = writer.save_preview("job-001", "composer", _png(1536, 864, noisy=True), max_bytes=150_000)
    assert artifact.size_bytes <= 150_000 and artifact.path.suffix == ".jpg"
    assert artifact.path.parent.name == "job-001"


def test_preview_that_can_never_fit_raises(tmp_path: Path) -> None:
    with pytest.raises(ArtifactTooLargeError):
        ArtifactWriter(tmp_path).save_preview("job-001", "full", _png(640, 480, noisy=True), max_bytes=500)


@pytest.mark.parametrize("bad", ["..", "../x", "a/b", "a\\b", "", "x" * 65, "C:", "con.png", "_hidden", "job-1\n", "job\t1"])
def test_artifact_names_cannot_escape(tmp_path: Path, bad: str) -> None:
    writer = ArtifactWriter(tmp_path / "artifacts")
    with pytest.raises(InvalidArtifactNameError):
        writer.save_preview(bad, "ok", _png(10, 10), 10_000)
    with pytest.raises(InvalidArtifactNameError):
        writer.save_preview("job-1", bad, _png(10, 10), 10_000)


def test_dom_snapshots_go_to_a_private_subfolder(tmp_path: Path) -> None:
    path = ArtifactWriter(tmp_path).save_failure_dom("job-1", "fill", "<html></html>")
    assert path.parent.name == "private"


def test_prune_removes_only_old_previews(tmp_path: Path) -> None:
    writer = ArtifactWriter(tmp_path)
    old = writer.save_preview("job-old", "p", _png(10, 10), 10_000).path
    fresh = writer.save_preview("job-new", "p", _png(10, 10), 10_000).path
    failure = writer.save_failure_screenshot("job-old", "f", _png(10, 10)).path
    past = time.time() - 40 * 86400
    os.utime(old, (past, past))
    os.utime(failure, (past, past))
    assert writer.prune_previews(older_than_days=30) == 1
    assert not old.exists() and fresh.exists() and failure.exists()


def test_toast_sink_records_instead_of_showing(tmp_path: Path) -> None:
    sink = tmp_path / "toasts.jsonl"
    assert ToastClient(enabled=True, sink_path=sink).notify("队列已暂停", "登录失效", "http://127.0.0.1:8790/queue")
    assert json.loads(sink.read_text(encoding="utf-8"))["title"] == "队列已暂停"


def test_disabled_toast_does_nothing(tmp_path: Path) -> None:
    sink = tmp_path / "toasts.jsonl"
    assert not ToastClient(enabled=False, sink_path=sink).notify("t", "b", None)
    assert not sink.exists()


def test_thumbnail_rejects_truncated_image(tmp_path: Path) -> None:
    source = tmp_path / "bg1-1.png"
    source.write_bytes(_png(400, 400, noisy=True)[:200])
    with pytest.raises(UnsupportedThumbnailSourceError):
        ThumbnailReader(tmp_path / "cache").thumbnail(source, 320)
