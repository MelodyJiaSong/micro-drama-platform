"""审片串联的落盘（follow-up 260）：ffmpeg 把每条重编码成同一规格的中间件（按文件缓存），再无损接起来。

每条先统一成 1280×720（等比缩放加黑边）、30fps、yuv420p、AAC 48k 立体声，缺音轨补静音，按源画面长度截断；规格一致后用 concat
分路器接视频（不重编码），音频再编一次。中间件按「源路径 + 大小 + 修改时间」命名，换了一条只重编码那一条。
半写的文件（正在下载）ffmpeg 打不开，返回 None，由调用方退用上一条。ffmpeg 来自 imageio-ffmpeg，不需系统安装。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import threading
from pathlib import Path
from typing import Any

import imageio_ffmpeg

from libs.common.review_reel import AUDIO_RATE, FPS, HEIGHT, REEL_FORMAT, SEGMENTS_DIR, WIDTH

_VIDEO_FILTER = (f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
                 f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps={FPS},format=yuv420p")
_AUDIO_FILTER = f"aresample={AUDIO_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,apad"
_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
_DURATION = re.compile(r"Duration: (\d+):(\d+):([\d.]+)")


class ReviewReelWriter:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        self._lock = threading.Lock()
        self._running: set[str] = set()

    # ── 同一份串联同一时间只跑一个 ──
    def claim(self, job: str) -> bool:
        with self._lock:
            if job in self._running:
                return False
            self._running.add(job)
            return True

    def release(self, job: str) -> None:
        with self._lock:
            self._running.discard(job)

    def only(self, job: str) -> bool:
        with self._lock:
            return self._running == {job}

    def _run(self, args: list[str], timeout: float = 1800) -> subprocess.CompletedProcess[str]:
        return subprocess.run([self.ffmpeg, "-hide_banner", *args], capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout, creationflags=_NO_WINDOW)

    def _has_audio(self, src: Path) -> bool:
        return "Audio:" in self._run(["-i", str(src)], timeout=60).stderr

    def duration(self, path: Path) -> float:
        """段的容器时长：concat 按它累加下一段的起点，章节起止也按它算才对得上（画面帧数算的会每段差几十毫秒）。"""
        found = _DURATION.search(self._run(["-i", str(path)], timeout=60).stderr)
        if not found:
            raise RuntimeError(f"读不出时长：{path.name}")
        hours, minutes, seconds = found.groups()
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

    def segment(self, folder: Path, clip: dict[str, Any]) -> tuple[Path, float] | None:
        """一条生成 → (中间件, 秒数)；读不出返回 None。"""
        ident = f"{REEL_FORMAT}|{clip['video']}|{clip['size']}|{clip['mtime_ns']}"
        seg = folder / SEGMENTS_DIR / f"{hashlib.sha1(ident.encode('utf-8')).hexdigest()[:20]}.mp4"
        if seg.is_file():
            try:
                return seg, self.duration(seg)
            except (RuntimeError, OSError):
                seg.unlink(missing_ok=True)
        src = self.root / clip["video"]
        seg.parent.mkdir(parents=True, exist_ok=True)
        part = seg.with_name(seg.stem + ".part.mp4")
        try:   # 按源画面的长度截断：-shortest 配 apad 在高码率素材上会让音轨超出 10 秒以上（s2 实测 7 秒画面出 19 秒的段）
            _, picture = imageio_ffmpeg.count_frames_and_secs(str(src))
        except (RuntimeError, OSError):
            return None   # 打不开（半写的文件）
        if picture <= 0:
            return None
        audio = self._has_audio(src)
        args = ["-y", "-v", "error", "-i", str(src)]
        if audio:
            args += ["-map", "0:v:0", "-map", "0:a:0", "-af", _AUDIO_FILTER]
        else:
            args += ["-f", "lavfi", "-i", f"anullsrc=channel_layout=stereo:sample_rate={AUDIO_RATE}", "-map", "0:v:0", "-map", "1:a:0"]
        args += ["-vf", _VIDEO_FILTER, "-t", f"{picture:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                 "-c:a", "aac", "-b:a", "160k", "-ar", str(AUDIO_RATE), "-ac", "2", "-movflags", "+faststart", str(part)]
        try:
            done = self._run(args)
            seconds = self.duration(part) if done.returncode == 0 and part.is_file() else 0.0
        except (RuntimeError, OSError, subprocess.TimeoutExpired):
            seconds = 0.0
        if seconds <= 0:
            part.unlink(missing_ok=True)
            return None
        part.replace(seg)
        return seg, seconds

    def concat(self, segments: list[Path], out: Path) -> None:
        out.parent.mkdir(parents=True, exist_ok=True)
        listing = out.with_name(out.stem + ".concat.txt")
        listing.write_text("".join("file '" + p.resolve().as_posix().replace("'", r"'\''") + "'\n" for p in segments), encoding="utf-8")
        part = out.with_name(out.stem + ".part.mp4")
        try:
            done = self._run(["-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-c:v", "copy",
                              "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(part)])
            if done.returncode != 0 or not part.is_file():
                raise RuntimeError(done.stderr.strip()[-500:] or "ffmpeg 拼接失败")
            part.replace(out)
        finally:
            listing.unlink(missing_ok=True)
            part.unlink(missing_ok=True)

    def save(self, path: Path, data: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(path)

    def prune(self, folder: Path, keep: set[str]) -> None:
        """删掉没有任何串联清单再用到的中间件。"""
        for seg in (folder / SEGMENTS_DIR).glob("*.mp4"):
            if seg.name not in keep and not seg.name.endswith(".part.mp4"):
                seg.unlink(missing_ok=True)
