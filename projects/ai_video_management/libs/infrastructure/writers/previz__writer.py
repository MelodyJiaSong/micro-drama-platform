"""Render a Blender previz `.blend` to an MP4, detached, with pollable progress.

**Why this exists as its own step.** Authoring the previz (`build_previz.py`
rebuilds the `.blend` from the scene master) and rendering it are two
independent concerns with wildly different costs: the build is ~15 seconds and
gets re-run many times while the shot is being tuned, the render is 15–30
minutes and is only worth paying once the `.blend` is right. Coupling them
would mean every tweak costs half an hour. So the build stays a script the
author runs freely, and the render is triggered on demand — from the UI button
this class backs, or by hand with the two commands in the previz README.

**Pipeline.** `blender -b <blend> --python-expr` to read `frame_end` (also a
cheap validity check on the file) → `blender -b <blend> -a` writing a PNG
sequence into `frames/` → ffmpeg assembling `{stem}.mp4` beside the `.blend`.

Blender's own build often ships without FFMPEG compiled in (the `file_format`
enum simply has no `FFMPEG` member), so direct-to-MP4 output is not reliable;
the PNG sequence + `imageio-ffmpeg` path always works and is what
`build_previz.py` configures the scene for.

**One job at a time, process-wide.** Blender saturates every core; a second
concurrent render makes both crawl and the progress numbers meaningless.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

import imageio_ffmpeg

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.previz__error import (
    BlenderMissingError,
    InvalidPrevizPathError,
    PrevizBlendNotFoundError,
    PrevizRenderBusyError,
    PrevizRenderFailedError,
)
from libs.domain.value_objects.previz__valueobject import (
    STATE_BUILDING,
    STATE_CANCELLED,
    STATE_IDLE,
    STATE_DONE,
    STATE_FAILED,
    STATE_MUXING,
    STATE_PROBING,
    STATE_RENDERING,
    PrevizJobSnapshot,
)

PREVIZ_DIR_NAME: str = "previz"
BUILD_SCRIPT_NAME: str = "build_previz.py"
CONFIG_NAME: str = "previz_config.toml"
_SCENE_MASTER_RE = re.compile(r'^SCENE_MASTER\s*=\s*[ru]*["\']([^"\']+)["\']', re.M)
_BUILD_TIMEOUT_S: int = 600
FRAMES_SUBDIR: str = "frames"
FRAME_PREFIX: str = "f"
DEFAULT_FPS: int = 24
_PROBE_TIMEOUT_S: int = 120
_MUX_TIMEOUT_S: int = 600
_POLL_INTERVAL_S: float = 1.0
_PROBE_RE = re.compile(r"PREVIZ_FRAME_END=(\d+)")
_PROBE_EXPR: str = (
    "import bpy;print('PREVIZ_FRAME_END=%d' % bpy.context.scene.frame_end);"
    "print('PREVIZ_FPS=%d' % bpy.context.scene.render.fps)"
)
_PROBE_FPS_RE = re.compile(r"PREVIZ_FPS=(\d+)")

# Checked in order; first hit wins. `BLENDER_EXE` overrides everything.
_BLENDER_CANDIDATES: tuple[str, ...] = (
    r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe",
    r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
    r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
    "/usr/bin/blender",
    "/usr/local/bin/blender",
    "/Applications/Blender.app/Contents/MacOS/Blender",
)


def find_blender() -> str:
    """Absolute path to a Blender executable, or raise.

    `BLENDER_EXE` wins so a machine with a non-standard install needs one line
    in `apps/api/.env` rather than a code change.
    """
    override = os.environ.get("BLENDER_EXE", "").strip()
    if override:
        if Path(override).is_file():
            return override
        raise BlenderMissingError(f"BLENDER_EXE points at a missing file: {override}")
    on_path = shutil.which("blender")
    if on_path:
        return on_path
    for candidate in _BLENDER_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    raise BlenderMissingError(
        "no Blender executable found — set BLENDER_EXE in apps/api/.env"
    )


class PrevizRenderer:
    def __init__(self, exposed: ExposedTree, resolver: SafeResolver) -> None:
        self._exposed = exposed
        self._resolver = resolver
        self._lock = threading.Lock()
        self._job: PrevizJobSnapshot | None = None
        self._cancel = threading.Event()
        self._proc: subprocess.Popen[bytes] | None = None

    # ------------------------------------------------------------------ public

    def locate_blend(self, rel: str) -> Path:
        """Resolve any path inside a `previz/` folder to the single `.blend` in it.

        Accepts the folder itself, the `.blend`, or a sibling (README, the build
        script) — so the UI can pass whatever the user currently has open.
        """
        if not isinstance(rel, str) or rel == "":
            raise InvalidPrevizPathError("path is empty")
        if not self._exposed.is_inside(rel):
            raise InvalidPrevizPathError("path outside sandbox")
        resolved = self._resolver.resolve(rel)
        if resolved is None:
            raise InvalidPrevizPathError("path does not resolve")
        folder = resolved if resolved.is_dir() else resolved.parent
        if folder.name != PREVIZ_DIR_NAME:
            raise InvalidPrevizPathError(f"not inside a {PREVIZ_DIR_NAME}/ folder")
        blends = sorted(p for p in folder.glob("*.blend") if p.is_file())
        if not blends:
            raise PrevizBlendNotFoundError(f"no .blend in {folder.name}/")
        if len(blends) > 1:
            raise PrevizBlendNotFoundError(
                f"{len(blends)} .blend files in {folder.name}/ — expected exactly one"
            )
        return blends[0]

    def status(self, rel: str) -> PrevizJobSnapshot:
        blend = self.locate_blend(rel)
        with self._lock:
            job = self._job
        if job is not None and job.blend_rel == self._rel(blend):
            return job
        return self._idle_snapshot(blend)

    def start(self, rel: str) -> PrevizJobSnapshot:
        blend = self.locate_blend(rel)
        blender = find_blender()  # fail fast, before claiming the slot
        with self._lock:
            if self._job is not None and not self._job.is_terminal:
                raise PrevizRenderBusyError(
                    f"a render is already running: {self._job.blend_rel}"
                )
            self._cancel.clear()
            self._job = PrevizJobSnapshot(
                blend_rel=self._rel(blend),
                state=STATE_BUILDING,
                rendered_frames=0,
                total_frames=0,
                started_at=time.time(),
                finished_at=None,
                message="按 previz_config.toml 重建 .blend",
                mp4_rel=None,
            )
            snapshot = self._job
        threading.Thread(
            target=self._run, args=(blend, blender), name="previz-render", daemon=True
        ).start()
        return snapshot

    def cancel(self, rel: str) -> PrevizJobSnapshot:
        blend = self.locate_blend(rel)
        self._cancel.set()
        with self._lock:
            proc = self._proc
        if proc is not None and proc.poll() is None:
            proc.terminate()
        with self._lock:
            job = self._job
        return job if job is not None else self._idle_snapshot(blend)

    # ----------------------------------------------------------------- private

    def _run(self, blend: Path, blender: str) -> None:
        try:
            self._rebuild(blend, blender)
            if self._cancel.is_set():
                self._finish(STATE_CANCELLED, "已取消", None)
                return
            self._update(state=STATE_PROBING, message="读取 .blend 帧范围")
            total, fps = self._probe(blend, blender)
            self._update(state=STATE_RENDERING, total_frames=total, message="渲染帧序列")
            frames_dir = blend.parent / FRAMES_SUBDIR
            self._wipe_frames(frames_dir)
            self._render_frames(blend, frames_dir, blender)
            if self._cancel.is_set():
                self._finish(STATE_CANCELLED, "已取消", None)
                return
            self._update(state=STATE_MUXING, message="合成 MP4")
            mp4 = self._mux(blend, frames_dir, fps)
            self._finish(STATE_DONE, f"完成 · {total} 帧 · {total / fps:.2f}s", self._rel(mp4))
        except Exception as exc:  # any failure must land in the snapshot, not vanish
            if self._cancel.is_set():
                self._finish(STATE_CANCELLED, "已取消", None)
            else:
                self._finish(STATE_FAILED, str(exc)[:300], None)
        finally:
            with self._lock:
                self._proc = None

    def _rebuild(self, blend: Path, blender: str) -> None:
        """Rebuild the `.blend` from the scene master + config before rendering.

        User contract (follow-up 058): editing `previz_config.toml` and hitting
        出片 must be enough — no manual `cp` + `blender -b … --python` step. The
        build script declares its scene master via a `SCENE_MASTER = "…"`
        repo-relative constant; we re-copy that master over the `.blend` (the
        build script is only idempotent from a fresh copy) and run the script,
        which reads the config. Folders without a build script or without the
        constant keep the old behaviour: render the `.blend` as-is.
        """
        script = blend.parent / BUILD_SCRIPT_NAME
        if not script.is_file():
            return
        master_match = _SCENE_MASTER_RE.search(script.read_text(encoding="utf-8"))
        if master_match is None:
            return
        master = self._resolver.resolve(master_match.group(1).replace("\\", "/"))
        if master is None or not master.is_file():
            raise PrevizRenderFailedError(
                f"SCENE_MASTER 不存在: {master_match.group(1)}"
            )
        shutil.copyfile(master, blend)
        completed = subprocess.run(
            [blender, "-b", str(blend), "--python", str(script)],
            capture_output=True,
            timeout=_BUILD_TIMEOUT_S,
            check=False,
        )
        out = completed.stdout.decode("utf-8", errors="replace")
        if "PREVIZ OK" not in out:
            err = completed.stderr.decode("utf-8", errors="replace").strip()
            tail = (err or out).strip().splitlines()[-8:]
            raise PrevizRenderFailedError("重建 .blend 失败: " + " / ".join(tail)[:280])

    def _probe(self, blend: Path, blender: str) -> tuple[int, int]:
        completed = subprocess.run(
            [blender, "-b", str(blend), "--python-expr", _PROBE_EXPR],
            capture_output=True,
            timeout=_PROBE_TIMEOUT_S,
            check=False,
        )
        out = completed.stdout.decode("utf-8", errors="replace")
        frame_match = _PROBE_RE.search(out)
        if frame_match is None:
            err = completed.stderr.decode("utf-8", errors="replace").strip()[:200]
            raise PrevizRenderFailedError(f"无法读取 .blend 帧范围: {err or 'blender 无输出'}")
        fps_match = _PROBE_FPS_RE.search(out)
        return int(frame_match.group(1)), int(fps_match.group(1)) if fps_match else DEFAULT_FPS

    def _render_frames(self, blend: Path, frames_dir: Path, blender: str) -> None:
        """Run Blender and report progress by counting the PNGs it has written.

        Parsing Blender's stdout looks like the obvious source of progress, but
        it does not work: the per-frame progress is printed with a carriage
        return so the stream carries no newlines to iterate on, and stdio
        block-buffers into a pipe anyway — measured live, the frame counter sat
        at 0 for a full minute while frames were landing on disk. Counting
        files is immune to both. It is exact here because `_wipe_frames` has
        just emptied the directory, so nothing but this run's output is in it.

        stdout goes to the void (it is only the progress spam we cannot use);
        stderr goes to a temp file rather than a pipe so a chatty failure can
        never deadlock on a full pipe buffer.
        """
        with tempfile.TemporaryFile() as err_file:
            proc = subprocess.Popen(
                [blender, "-b", str(blend), "-a"],
                stdout=subprocess.DEVNULL,
                stderr=err_file,
            )
            with self._lock:
                self._proc = proc
            while proc.poll() is None:
                if self._cancel.is_set():
                    proc.terminate()
                    break
                self._update(rendered_frames=self._count_frames(frames_dir))
                time.sleep(_POLL_INTERVAL_S)
            proc.wait()
            if self._cancel.is_set():
                return
            self._update(rendered_frames=self._count_frames(frames_dir))
            if proc.returncode != 0:
                err_file.seek(0)
                tail = err_file.read().decode("utf-8", errors="replace").strip()[-200:]
                raise PrevizRenderFailedError(
                    f"blender 渲染失败 (exit {proc.returncode}) {tail}".strip()
                )

    def _count_frames(self, frames_dir: Path) -> int:
        try:
            return sum(1 for p in frames_dir.glob(f"{FRAME_PREFIX}*.png") if p.is_file())
        except OSError:
            return 0

    def _mux(self, blend: Path, frames_dir: Path, fps: int) -> Path:
        frames = sorted(frames_dir.glob(f"{FRAME_PREFIX}*.png"))
        if not frames:
            raise PrevizRenderFailedError("渲染结束但 frames/ 里没有 PNG")
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        out = blend.with_suffix(".mp4")
        pattern = str(frames_dir / f"{FRAME_PREFIX}%04d.png")
        cmd = [
            ffmpeg,
            "-y",
            "-framerate", str(fps),
            "-start_number", str(self._first_index(frames[0])),
            "-i", pattern,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-movflags", "+faststart",
            "-loglevel", "error",
            str(out),
        ]
        completed = subprocess.run(
            cmd, capture_output=True, timeout=_MUX_TIMEOUT_S, check=False
        )
        if completed.returncode != 0 or not out.is_file():
            err = completed.stderr.decode("utf-8", errors="replace").strip()[:200]
            raise PrevizRenderFailedError(f"ffmpeg 合成失败: {err or 'unknown'}")
        return out

    def _first_index(self, first: Path) -> int:
        digits = first.stem[len(FRAME_PREFIX):]
        return int(digits) if digits.isdigit() else 1

    def _wipe_frames(self, frames_dir: Path) -> None:
        """A shortened re-render must not leave the previous run's tail behind —
        ffmpeg would splice stale frames onto the end of the new MP4."""
        if not frames_dir.is_dir():
            frames_dir.mkdir(parents=True, exist_ok=True)
            return
        for entry in frames_dir.iterdir():
            if entry.is_file() and not entry.is_symlink() and entry.suffix.lower() == ".png":
                entry.unlink()

    def _update(self, **fields: object) -> None:
        with self._lock:
            if self._job is None:
                return
            self._job = PrevizJobSnapshot(
                blend_rel=self._job.blend_rel,
                state=str(fields.get("state", self._job.state)),
                rendered_frames=int(
                    fields.get("rendered_frames", self._job.rendered_frames)  # type: ignore[arg-type]
                ),
                total_frames=int(
                    fields.get("total_frames", self._job.total_frames)  # type: ignore[arg-type]
                ),
                started_at=self._job.started_at,
                finished_at=self._job.finished_at,
                message=str(fields.get("message", self._job.message)),
                mp4_rel=self._job.mp4_rel,
            )

    def _finish(self, state: str, message: str, mp4_rel: str | None) -> None:
        with self._lock:
            if self._job is None:
                return
            self._job = PrevizJobSnapshot(
                blend_rel=self._job.blend_rel,
                state=state,
                rendered_frames=self._job.rendered_frames,
                total_frames=self._job.total_frames,
                started_at=self._job.started_at,
                finished_at=time.time(),
                message=message,
                mp4_rel=mp4_rel,
            )

    def _idle_snapshot(self, blend: Path) -> PrevizJobSnapshot:
        mp4 = blend.with_suffix(".mp4")
        return PrevizJobSnapshot(
            blend_rel=self._rel(blend),
            state=STATE_IDLE,
            rendered_frames=0,
            total_frames=0,
            started_at=0.0,
            finished_at=None,
            message="",
            mp4_rel=self._rel(mp4) if mp4.is_file() else None,
        )

    def _rel(self, p: Path) -> str:
        try:
            return p.resolve().relative_to(self._resolver.root).as_posix()
        except (OSError, ValueError):
            return p.as_posix()
