from __future__ import annotations

from pathlib import Path

from libs.application.commands.ingest__command import IngestCommand
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.daos.media__dao import MediaInfoDao
from libs.infrastructure.writers.artifact__writer import ArtifactWriter


class _FakeFfmpeg:
    def __init__(self, duration_s: float = 120.0, decodable: bool = True) -> None:
        self._duration_s = duration_s
        self._decodable = decodable
        self.cut_calls: list[tuple[float, float, str]] = []

    def probe(self, path: str) -> MediaInfoDao:
        return MediaInfoDao(self._duration_s, 720, 1280, self._decodable, "" if self._decodable else "moov atom not found")

    def black_ranges(self, path: str, min_black_s: float = 0.3) -> list[tuple[float, float]]:
        return [(118.0, 119.0), (239.5, 240.5)] if self._duration_s > 300 else []

    def cut_clip(self, path: str, start_s: float, end_s: float, out_path: str) -> None:
        self.cut_calls.append((start_s, end_s, out_path))
        Path(out_path).write_bytes(b"clip")


def _cmd(tmp_path: Path, ffmpeg: _FakeFfmpeg) -> tuple[IngestCommand, ArtifactWriter]:
    writer = ArtifactWriter(SafeWorkspace(root=str(tmp_path)))
    return IngestCommand(ffmpeg=ffmpeg, writer=writer), writer  # type: ignore[arg-type]


def test_undecodable_file_rejected_with_reason(tmp_path: Path) -> None:
    cmd, writer = _cmd(tmp_path, _FakeFfmpeg(decodable=False))
    writer.write_text("d1/upload.mp4", "x")
    result = cmd.validate_media("d1/upload.mp4", size_bytes=100)
    assert not result.ok and "undecodable" in result.reason


def test_oversize_file_rejected_before_probe(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path, _FakeFfmpeg())
    result = cmd.validate_media("d1/upload.mp4", size_bytes=3 * 1024**3)
    assert not result.ok and "2GB" in result.reason


def test_single_episode_file_copied_not_cut(tmp_path: Path) -> None:
    ffmpeg = _FakeFfmpeg(duration_s=120.0)
    cmd, writer = _cmd(tmp_path, ffmpeg)
    writer.write_text("d1/upload.mp4", "source-bytes")
    result = cmd.split_episodes("d1", "d1/upload.mp4")
    assert result.episode_rel_paths == ["d1/ep01/source.mp4"]
    assert ffmpeg.cut_calls == []
    assert (tmp_path / "d1" / "episodes.json").exists()


def test_append_upload_numbers_after_existing_episodes(tmp_path: Path) -> None:
    """2026-07-18 regression: appending a file to a drama with existing ep01 must land
    at ep02 — numbering from ep01 overwrote the prior episode's source and its
    reset state silently reprocessed it."""
    ffmpeg = _FakeFfmpeg(duration_s=120.0)
    cmd, writer = _cmd(tmp_path, ffmpeg)
    writer.write_text("d1/ep01/source.mp4", "original-episode")
    writer.write_json("d1/episodes.json", [
        {"rel_path": "d1/ep01/source.mp4", "start_s": 0.0, "end_s": 90.0, "confidence": "high"},
    ])
    writer.write_text("d1/upload2.mp4", "second-episode")
    result = cmd.split_episodes("d1", "d1/upload2.mp4")
    assert result.episode_rel_paths == ["d1/ep02/source.mp4"]
    assert (tmp_path / "d1/ep01/source.mp4").read_text(encoding="utf-8") == "original-episode"
    import json as _json

    index = _json.loads((tmp_path / "d1/episodes.json").read_text(encoding="utf-8"))
    assert [e["rel_path"] for e in index] == ["d1/ep01/source.mp4", "d1/ep02/source.mp4"]


def test_long_file_cut_at_black_gaps(tmp_path: Path) -> None:
    ffmpeg = _FakeFfmpeg(duration_s=360.0)
    cmd, writer = _cmd(tmp_path, ffmpeg)
    writer.write_text("d1/upload.mp4", "source-bytes")
    result = cmd.split_episodes("d1", "d1/upload.mp4")
    assert len(result.episode_rel_paths) == 3
    assert len(ffmpeg.cut_calls) == 3
    assert result.confidences == ["medium", "medium", "medium"]
