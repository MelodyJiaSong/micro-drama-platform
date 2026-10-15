"""Downloads that stop mid-file still open with a plausible duration; only a full decode catches them
(2026-10-11: s2 st8 / st12 / st16 were truncated on download and recorded as takes). Needs ffmpeg on PATH."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from tools import shot_take

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None, reason="needs ffmpeg")


def clip(folder: Path, seconds: int = 2) -> Path:
    out = folder / "full.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc=size=320x180:rate=24:duration={seconds}",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)
    return out


def truncated(full: Path, folder: Path) -> Path:
    cut = folder / "cut.mp4"
    data = full.read_bytes()
    cut.write_bytes(data[: int(len(data) * 0.6)])
    return cut


def test_media_problem_passes_a_whole_file_and_flags_a_cut_one(tmp_path: Path) -> None:
    full = clip(tmp_path)
    assert shot_take.media_problem(full, 2) == ""
    assert shot_take.media_problem(truncated(full, tmp_path), 2) != ""
    assert "时长" in shot_take.media_problem(full, 5)


def test_a_truncated_download_is_fetched_again_before_the_take_is_made(tmp_path: Path, monkeypatch) -> None:
    full = clip(tmp_path)
    cut = truncated(full, tmp_path)
    served = iter([cut, full])
    made: list[Path] = []

    def fake_query(ep_dir, sid, download_dir):
        if download_dir is None:
            return {"gen_status": "success"}
        shutil.copyfile(next(served), Path(download_dir) / "video_1.mp4")
        return {"gen_status": "success"}

    def fake_make_take(ep_dir, key, sid, video, credits, model, sent):
        made.append(tmp_path / "kept.mp4")
        shutil.copyfile(video, made[-1])
        return shot_take.REPO / "take"

    monkeypatch.setattr(shot_take, "query", fake_query)
    monkeypatch.setattr(shot_take, "make_take", fake_make_take)
    monkeypatch.setattr(shot_take, "pending_file", lambda ep_dir, key, sid: tmp_path / "pending.json")
    monkeypatch.setattr(shot_take.time, "sleep", lambda s: None)
    rc = shot_take.wait_and_record(tmp_path, "ep1_s2_st1", "abcdef12", None, None, 0, 1, ("ep1_s2_st1\n时长：2秒\n", {}))
    assert rc == 0 and len(made) == 1
    assert shot_take.media_problem(made[0], 2) == ""
