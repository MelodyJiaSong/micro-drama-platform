"""Media bytes for the fake site: a tiny 22 s 16:9 mp4 (via ffmpeg when present) and small upload PNGs."""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

STUB_VIDEO: bytes = b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00isomiso2" + b"fake-jimeng-stub-video" * 64


@dataclass(frozen=True)
class FixtureVideo:
    data: bytes
    is_real_mp4: bool


def make_video(cache_dir: Path, duration_s: int = 22) -> FixtureVideo:
    target = cache_dir / f"fake_result_{duration_s}s.mp4"
    if target.is_file():
        return FixtureVideo(target.read_bytes(), True)
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return FixtureVideo(STUB_VIDEO, False)
    cache_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            ffmpeg, "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", f"color=c=gray:s=320x180:r=5:d={duration_s}",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
            "-t", str(duration_s), "-c:v", "libx264", "-preset", "ultrafast", "-crf", "45", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "16k", "-shortest", str(target),
        ],
        capture_output=True,
        check=False,
        timeout=120,
    )
    if completed.returncode != 0 or not target.is_file():
        return FixtureVideo(STUB_VIDEO, False)
    return FixtureVideo(target.read_bytes(), True)


def make_png(path: Path, color: tuple[int, int, int], size: int = 64) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (size, size), color).save(path, format="PNG")
    return path
