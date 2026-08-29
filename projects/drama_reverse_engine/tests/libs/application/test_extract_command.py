from __future__ import annotations

import json
from pathlib import Path

from libs.application.commands.extract__command import ExtractCommand
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.daos.media__dao import MediaInfoDao
from libs.infrastructure.daos.shotspan__dao import ShotSpanDao
from libs.infrastructure.daos.subtitleline__dao import SubtitleLineDao
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter


class _FakeFfmpeg:
    def probe(self, path: str) -> MediaInfoDao:
        return MediaInfoDao(10.0, 720, 1280, True)


class _FakeDetector:
    def detect(self, video_path: str, duration_s: float) -> list[ShotSpanDao]:
        return [ShotSpanDao(0.0, 2.8), ShotSpanDao(2.8, 6.0), ShotSpanDao(6.0, duration_s)]


class _FakeOcr:
    available = True

    def extract(self, video_path: str) -> list[SubtitleLineDao]:
        return [SubtitleLineDao("你还敢回来？", 0.5, 2.0, "ocr"), SubtitleLineDao("我回来拿东西", 3.0, 4.5, "ocr")]


class _FakeAsr:
    available = True

    def transcribe(self, video_path: str) -> list[SubtitleLineDao]:
        return [SubtitleLineDao("你还敢回来？", 0.55, 2.0, "asr"), SubtitleLineDao("我回来拿冬西", 3.1, 4.4, "asr")]


class _Null:
    available = False

    def extract(self, video_path: str) -> list[SubtitleLineDao]:
        return []

    def transcribe(self, video_path: str) -> list[SubtitleLineDao]:
        return []


def _cmd(tmp_path: Path, ocr: object, asr: object) -> tuple[ExtractCommand, Path]:
    ws = SafeWorkspace(root=str(tmp_path))
    writer = ArtifactWriter(ws)
    writer.write_text("d1/ep01/source.mp4", "fake")
    cmd = ExtractCommand(
        ffmpeg=_FakeFfmpeg(), detector=_FakeDetector(), subtitles=ocr, asr=asr,  # type: ignore[arg-type]
        reader=ArtifactReader(ws), writer=writer,
    )
    return cmd, tmp_path


def test_shots_and_dialogue_written_with_flags(tmp_path: Path) -> None:
    cmd, root = _cmd(tmp_path, _FakeOcr(), _FakeAsr())
    result = cmd.run("d1/ep01")
    assert result.shot_count == 3
    assert result.dialogue_line_count == 2
    assert result.flagged_line_count == 1  # 拿东西 vs 拿冬西 mismatch
    shots = json.loads((root / "d1/ep01/shots.json").read_text(encoding="utf-8"))
    assert shots[0]["duration_s"] == 2.8
    lines = json.loads((root / "d1/ep01/dialogue_raw.json").read_text(encoding="utf-8"))["lines"]
    assert lines[0]["speaker"] is None and lines[0]["attribution"] == "pending"


def test_no_backends_degrades_with_explicit_flags(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path, _Null(), _Null())
    result = cmd.run("d1/ep01")
    assert "ocr_backend_unavailable" in result.degradations
    assert "asr_backend_unavailable" in result.degradations
    assert result.dialogue_line_count == 0


def test_asr_only_marks_fidelity_degraded_without_per_line_flags(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path, _Null(), _FakeAsr())
    result = cmd.run("d1/ep01")
    assert "asr_only_fidelity_degraded" in result.degradations
    assert result.dialogue_line_count == 2
    assert result.flagged_line_count == 0


def test_second_run_is_idempotent_skip(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path, _FakeOcr(), _FakeAsr())
    first = cmd.run("d1/ep01")
    second = cmd.run("d1/ep01")
    assert not first.skipped and second.skipped
    assert second.shot_count == first.shot_count


def test_force_rerun_recomputes(tmp_path: Path) -> None:
    cmd, _ = _cmd(tmp_path, _FakeOcr(), _FakeAsr())
    cmd.run("d1/ep01")
    third = cmd.run("d1/ep01", force=True)
    assert not third.skipped
