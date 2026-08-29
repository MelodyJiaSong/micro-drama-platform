from __future__ import annotations

import re
import subprocess

from libs.infrastructure.daos.media__dao import MediaInfoDao
from libs.infrastructure.errors.ffmpeg__error import FfmpegError

_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)")
_SIZE_RE = re.compile(r",\s*(\d{2,5})x(\d{2,5})[\s,]")
_SCENE_PTS_RE = re.compile(r"pts_time:(\d+\.?\d*)")
_BLACK_RE = re.compile(r"black_start:(\d+\.?\d*)\s+black_end:(\d+\.?\d*)")


def _ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


class FfmpegClient:
    def __init__(self, timeout_s: float = 600.0) -> None:
        self._exe = _ffmpeg_exe()
        self._timeout_s = timeout_s

    def _run(self, args: list[str]) -> tuple[int, str]:
        proc = subprocess.run(
            [self._exe, "-hide_banner", *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=self._timeout_s,
        )
        return proc.returncode, (proc.stderr or "") + (proc.stdout or "")

    def _run_or_raise(self, args: list[str]) -> str:
        rc, out = self._run(args)
        if rc != 0:
            raise FfmpegError(" ".join(args[:4]), rc, out[-300:])
        return out

    def probe(self, path: str) -> MediaInfoDao:
        decode_rc, decode_out = self._run(["-v", "error", "-t", "1", "-i", path, "-f", "null", "-"])
        _, info = self._run(["-i", path])  # bare -i always exits 1; only the parse matters
        dur = _DURATION_RE.search(info)
        size = _SIZE_RE.search(info)
        duration = (int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3))) if dur else 0.0
        decodable = decode_rc == 0 and dur is not None
        return MediaInfoDao(
            duration_s=duration,
            width=int(size.group(1)) if size else 0,
            height=int(size.group(2)) if size else 0,
            decodable=decodable,
            detail="" if decodable else decode_out[-300:],
        )

    def scene_change_times(self, path: str, threshold: float = 0.4) -> list[float]:
        out = self._run_or_raise(["-i", path, "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"])
        return [float(m.group(1)) for m in _SCENE_PTS_RE.finditer(out)]

    def black_ranges(self, path: str, min_black_s: float = 0.3) -> list[tuple[float, float]]:
        out = self._run_or_raise(["-i", path, "-vf", f"blackdetect=d={min_black_s}", "-an", "-f", "null", "-"])
        return [(float(m.group(1)), float(m.group(2))) for m in _BLACK_RE.finditer(out)]

    def extract_frame(self, path: str, at_s: float, out_path: str) -> None:
        self._run_or_raise(["-y", "-ss", f"{at_s:.3f}", "-i", path, "-frames:v", "1", out_path])

    def cut_clip(self, path: str, start_s: float, end_s: float, out_path: str) -> None:
        # -ss before -i is fast but keyframe-snapped; episode boundaries get a human
        # review pass (FR-1.4), so copy-mode speed wins over frame accuracy here.
        self._run_or_raise(["-y", "-ss", f"{start_s:.3f}", "-to", f"{end_s:.3f}", "-i", path, "-c", "copy", out_path])

    def trim_to(self, path: str, seconds: float, out_path: str) -> None:
        # frame-accurate head-aligned trim (FR-7.3 裁剪回原长) — re-encode, drop audio
        # (v1 carve-out: 成片无对白音轨)
        self._run_or_raise(["-y", "-i", path, "-t", f"{seconds:.3f}",
                            "-c:v", "libx264", "-preset", "veryfast", "-an", out_path])

    def concat(self, paths: list[str], list_file_path: str, out_path: str) -> None:
        from pathlib import Path

        listing = "\n".join(f"file '{p}'" for p in paths)
        Path(list_file_path).write_text(listing, encoding="utf-8")
        self._run_or_raise(["-y", "-f", "concat", "-safe", "0", "-i", list_file_path, "-c", "copy", out_path])

    def last_frame(self, path: str, out_path: str) -> None:
        self._run_or_raise(["-y", "-sseof", "-0.05", "-i", path, "-frames:v", "1", out_path])
