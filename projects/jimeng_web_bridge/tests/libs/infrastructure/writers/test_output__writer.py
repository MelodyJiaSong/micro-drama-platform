from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

import libs.infrastructure.writers.output__writer as output_module
from libs.common.paths import RepoSandbox
from libs.infrastructure.clients.ffprobe__client import FfprobeClient
from libs.infrastructure.daos.output__dao import MediaProbeDao, OutputExpectationDao
from libs.infrastructure.errors.output__error import (
    DownloadShaMismatchError, DownloadSizeMismatchError, FfprobeFailedError, FfprobeUnavailableError,
    MediaMismatchError, OutputPathRejectedError, SidecarWriteError,
)
from libs.infrastructure.writers.output__writer import OutputWriter, timestamp_label, whitelist_sidecar

RENDERS = "ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/renders"


class Prober:
    def __init__(self, duration_s: float | None = 22.0, width: int = 1280, height: int = 720) -> None:
        self.result = MediaProbeDao(duration_s, width, height)

    def probe(self, path: Path) -> MediaProbeDao:
        return self.result


def make(tmp_path: Path, prober: object | None = None) -> tuple[Path, OutputWriter]:
    root = tmp_path / "repo"
    (root / "ai_videos").mkdir(parents=True)
    return root, OutputWriter(RepoSandbox(root, (root / ".data",)), prober or Prober())  # type: ignore[arg-type]


def temp(root: Path, data: bytes = b"video bytes", name: str = "download.mp4") -> tuple[Path, OutputExpectationDao]:
    path = root / ".data" / "tmp" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path, OutputExpectationDao(len(data), hashlib.sha256(data).hexdigest(), 22.0, "16:9", 0.5)


def listing(directory: Path) -> list[str]:
    return sorted(p.name for p in directory.iterdir()) if directory.exists() else []


def test_finalize_places_bytes_unchanged_and_writes_whitelisted_sidecar_after(tmp_path: Path) -> None:
    root, writer = make(tmp_path)
    source, expected = temp(root)
    sidecar = {"job_id": "job-1", "cookie": "sid=1", "token": "t", "source": {"type": "shot", "path": "p", "extra": 1}, "backend": "web"}
    placed = writer.finalize(source, RENDERS, "shot02_20260913-181500.mp4", expected, sidecar)
    target = root / placed.path_rel
    assert target.read_bytes() == b"video bytes" and not source.exists()
    body = json.loads((root / (placed.sidecar_rel or "")).read_text(encoding="utf-8"))
    assert list(body) == ["job_id", "backend", "source", "output"]
    assert body["source"] == {"type": "shot", "path": "p"} and body["output"]["sha256"] == expected.sha256
    assert listing(root / RENDERS) == ["shot02_20260913-181500.mp4", "shot02_20260913-181500.mp4.jimeng.json"]


def test_size_and_sha_mismatch_reject_without_touching_the_target(tmp_path: Path) -> None:
    root, writer = make(tmp_path)
    source, expected = temp(root)
    with pytest.raises(DownloadSizeMismatchError):
        writer.finalize(source, RENDERS, "a.mp4", OutputExpectationDao(1, expected.sha256, None, None, 0.5), {})
    assert not source.exists() and listing(root / RENDERS) == []
    source, expected = temp(root)
    with pytest.raises(DownloadShaMismatchError):
        writer.finalize(source, RENDERS, "a.mp4", OutputExpectationDao(expected.size, "0" * 64, None, None, 0.5), {})
    assert listing(root / RENDERS) == []


@pytest.mark.parametrize(("probe", "message"), [(Prober(duration_s=4.0), "时长"), (Prober(width=720, height=1280), "比例"), (Prober(duration_s=None), "时长")])
def test_media_mismatch_rejects(tmp_path: Path, probe: Prober, message: str) -> None:
    root, writer = make(tmp_path, probe)
    source, expected = temp(root)
    with pytest.raises(MediaMismatchError, match=message):
        writer.finalize(source, RENDERS, "a.mp4", expected, {})
    assert listing(root / RENDERS) == []


def test_duration_within_tolerance_and_approximate_ratio_pass(tmp_path: Path) -> None:
    root, writer = make(tmp_path, Prober(duration_s=22.4, width=854, height=480))
    source, expected = temp(root)
    assert writer.finalize(source, RENDERS, "a.mp4", expected, {}).width == 854


def test_existing_names_are_never_overwritten(tmp_path: Path) -> None:
    root, writer = make(tmp_path)
    (root / RENDERS).mkdir(parents=True)
    (root / RENDERS / "shot02_x.mp4").write_bytes(b"earlier render")
    (root / RENDERS / "shot02_x_dup2.mp4.jimeng.json").write_text("{}", encoding="utf-8")
    source, expected = temp(root)
    placed = writer.finalize(source, RENDERS, "shot02_x.mp4", expected, {})
    assert placed.path_rel.endswith("shot02_x_dup3.mp4")
    assert (root / RENDERS / "shot02_x.mp4").read_bytes() == b"earlier render"


def test_cross_volume_staging_leaves_nothing_behind_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, writer = make(tmp_path)
    source, expected = temp(root)
    (root / RENDERS).mkdir(parents=True)
    monkeypatch.setattr(output_module, "_same_volume", lambda source, target: False)

    def refuse(source: Path, target: Path) -> None:
        raise PermissionError("target locked")

    monkeypatch.setattr(output_module, "_move_new", refuse)
    with pytest.raises(PermissionError):
        writer.finalize(source, RENDERS, "a.mp4", expected, {})
    assert listing(root / RENDERS) == [] and source.exists()


def test_cross_volume_copy_is_verified_and_placed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, writer = make(tmp_path)
    source, expected = temp(root)
    monkeypatch.setattr(output_module, "_same_volume", lambda source, target: False)
    placed = writer.finalize(source, RENDERS, "a.mp4", expected, {})
    assert (root / placed.path_rel).read_bytes() == b"video bytes" and not source.exists()
    assert listing(root / RENDERS) == ["a.mp4", "a.mp4.jimeng.json"]


def test_sidecar_failure_keeps_the_verified_media(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, writer = make(tmp_path)
    source, expected = temp(root)

    def broken(path: Path, body: object) -> None:
        raise OSError("read-only directory")

    monkeypatch.setattr(writer, "_write_sidecar", broken)
    with pytest.raises(SidecarWriteError) as caught:
        writer.finalize(source, RENDERS, "a.mp4", expected, {})
    assert (root / caught.value.output.path_rel).read_bytes() == b"video bytes"


@pytest.mark.parametrize("target", ["ai_videos/../elsewhere", "ai_videos/_deleted/x", ".data/tmp", "//server/share", "ai_videos/a:b"])
def test_targets_outside_the_output_sandbox_are_rejected(tmp_path: Path, target: str) -> None:
    root, writer = make(tmp_path)
    source, expected = temp(root)
    with pytest.raises(OutputPathRejectedError):
        writer.finalize(source, target, "a.mp4", expected, {})


@pytest.mark.parametrize("name", ["../a.mp4", "sub/a.mp4", "CON.mp4", "a.mp4 "])
def test_file_names_must_be_single_safe_segments(tmp_path: Path, name: str) -> None:
    root, writer = make(tmp_path)
    source, expected = temp(root)
    with pytest.raises(OutputPathRejectedError):
        writer.finalize(source, RENDERS, name, expected, {})


def test_missing_ffprobe_is_a_distinct_error_and_nothing_is_placed(tmp_path: Path) -> None:
    root, writer = make(tmp_path, FfprobeClient(executable=str(tmp_path / "missing" / "ffprobe.exe")))
    source, expected = temp(root)
    with pytest.raises(FfprobeUnavailableError):
        writer.finalize(source, RENDERS, "a.mp4", expected, {})
    assert listing(root / RENDERS) == []


def test_current_sha256_and_timestamp_label(tmp_path: Path) -> None:
    root, writer = make(tmp_path)
    (root / "ai_videos" / "ref.png").write_bytes(b"ref")
    assert writer.current_sha256("ai_videos/ref.png") == hashlib.sha256(b"ref").hexdigest()
    assert writer.current_sha256("ai_videos/missing.png") is None and writer.current_sha256("../x") is None
    assert timestamp_label(datetime(2026, 9, 13, 10, 15, 0, tzinfo=timezone.utc), "Asia/Shanghai") == "20260913-181500"
    assert whitelist_sidecar({"references": [{"name": "a", "cookie": "x", "sha256": "s"}]}) == {"references": [{"name": "a", "sha256": "s"}]}


# ---- real ffprobe ------------------------------------------------------------------------------------------------

def _require_media_tools() -> None:
    if shutil.which("ffprobe") and shutil.which("ffmpeg"):
        return
    if os.environ.get("JWB_REQUIRE_FFPROBE") == "1":
        pytest.fail("ffprobe/ffmpeg not on PATH")
    pytest.skip("ffprobe/ffmpeg not on PATH")


@pytest.fixture(scope="module")
def sample_mp4(tmp_path_factory: pytest.TempPathFactory) -> bytes:
    _require_media_tools()
    out = tmp_path_factory.mktemp("media") / "tiny_16x9_2s.mp4"
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=gray:s=320x180:d=2:r=25",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-y", str(out)],
        check=True, capture_output=True,
    )
    return out.read_bytes()


@pytest.mark.requires_ffprobe
def test_real_probe_accepts_matching_media(tmp_path: Path, sample_mp4: bytes) -> None:
    root, writer = make(tmp_path, FfprobeClient())
    source, expected = temp(root, sample_mp4)
    placed = writer.finalize(source, RENDERS, "shot02.mp4", replace_expectation(expected, 2.0, "16:9"), {})
    assert (placed.width, placed.height) == (320, 180) and placed.duration_s is not None and abs(placed.duration_s - 2.0) <= 0.1
    assert hashlib.sha256((root / placed.path_rel).read_bytes()).hexdigest() == hashlib.sha256(sample_mp4).hexdigest()


@pytest.mark.requires_ffprobe
@pytest.mark.parametrize(("duration", "ratio"), [(22.0, "16:9"), (2.0, "9:16")])
def test_real_probe_rejects_mismatching_media(tmp_path: Path, sample_mp4: bytes, duration: float, ratio: str) -> None:
    root, writer = make(tmp_path, FfprobeClient())
    source, expected = temp(root, sample_mp4)
    with pytest.raises(MediaMismatchError):
        writer.finalize(source, RENDERS, "shot02.mp4", replace_expectation(expected, duration, ratio), {})
    assert listing(root / RENDERS) == []


@pytest.mark.requires_ffprobe
def test_real_probe_rejects_a_truncated_file(tmp_path: Path, sample_mp4: bytes) -> None:
    root, writer = make(tmp_path, FfprobeClient())
    source, expected = temp(root, sample_mp4[: len(sample_mp4) // 3])
    with pytest.raises(FfprobeFailedError):
        writer.finalize(source, RENDERS, "shot02.mp4", replace_expectation(expected, 2.0, "16:9"), {})
    assert listing(root / RENDERS) == []


def replace_expectation(expected: OutputExpectationDao, duration: float, ratio: str) -> OutputExpectationDao:
    return OutputExpectationDao(expected.size, expected.sha256, duration, ratio, 0.5)
