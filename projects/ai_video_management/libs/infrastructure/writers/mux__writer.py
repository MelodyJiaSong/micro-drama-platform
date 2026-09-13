"""Mux an uploaded video with an uploaded audio track into a BGM'd cut.

Both inputs arrive as browser uploads, so nothing here touches the repo tree:
the uploads land in a per-request temp workdir that is swept as soon as ffmpeg
is done. That is why this feature needs no hole in the EXPOSED_TREE path
sandbox — it never names a repo path at all.

The RESULT, by contrast, is durable and has an address the user can go open: it
is written to the same folder the downloads-importer watches (env
`AI_VIDEO_MGMT_DOWNLOADS_DIR`, else `~/Downloads`), so a muxed shot cut is
already sitting where the drama-row import button will file it. Re-running never
overwrites — a taken name gets a `_1`, `_2`, … suffix.

The ffmpeg work is NOT reimplemented. `tools/mux_av.py` (the tested CLI) is
loaded as a module off the sandbox root and its `main()` is called with the
same argv the terminal takes, so the button and the CLI produce identical
output and only have to be fixed once.
"""
from __future__ import annotations

import importlib.util
import os
import re
import shutil
import tempfile
from pathlib import Path
from types import ModuleType
from typing import BinaryIO

from libs.application.dtos.mux__dto import MuxOptions, MuxResult
from libs.infrastructure.errors.mux__error import MuxFailedError, UnsupportedMediaError

VIDEO_EXTENSIONS = frozenset({".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"})
# Deliberately wide: generators hand out audio under whatever extension they
# like (an opus/webm stream saved as `.m4a` is routine) and ffmpeg sniffs the
# real container from the bytes, so the extension is a sanity check, not a
# format claim.
AUDIO_EXTENSIONS = frozenset(
    {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".opus", ".webm", ".mp4"}
)
_UNSAFE_STEM = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff._-]+")


# Shared with the downloads importer so the mux output lands where the drama-row
# import button already looks.
OUTPUT_DIR_ENV_VAR = "AI_VIDEO_MGMT_DOWNLOADS_DIR"


class BgmMuxer:
    def __init__(self, repo_root: Path, output_dir: Path | None = None) -> None:
        self._root = repo_root
        self._output_dir = (output_dir or self._resolve_default_output_dir()).resolve()

    def add_bgm(
        self,
        video_name: str,
        video_stream: BinaryIO,
        audio_name: str,
        audio_stream: BinaryIO,
        options: MuxOptions,
    ) -> MuxResult:
        video_ext = self._checked_ext(video_name, VIDEO_EXTENSIONS, "video")
        audio_ext = self._checked_ext(audio_name, AUDIO_EXTENSIONS, "audio")
        if not 0.0 <= options.bgm_volume <= 1.0:
            raise UnsupportedMediaError(f"bgm_volume out of range: {options.bgm_volume}")
        if not 0.0 <= options.source_volume <= 1.0:
            raise UnsupportedMediaError(
                f"source_volume out of range: {options.source_volume}"
            )
        workdir = Path(tempfile.mkdtemp(prefix="mux_bgm_"))
        out_path = self._unique_output(self._download_name(video_name))
        try:
            # Upload filenames are caller-controlled; keep the extension only and
            # name the temp files ourselves, so no upload can steer the path.
            video_path = workdir / f"in_video{video_ext}"
            audio_path = workdir / f"in_audio{audio_ext}"
            self._spill(video_stream, video_path)
            self._spill(audio_stream, audio_path)
            argv = [
                "--video", str(video_path),
                "--bgm", str(audio_path),
                "--out", str(out_path),
                "--bgm-volume", str(options.bgm_volume),
                "--bgm-start", str(options.bgm_start),
                "--fade-in", str(options.fade_in),
                "--fade-out", str(options.fade_out),
            ]
            if options.no_loop:
                argv.append("--no-loop")
            if options.keep_source_audio:
                argv += ["--keep-source-audio", "--source-volume", str(options.source_volume)]
                if options.duck_source:
                    argv.append("--duck-source")
            code = int(self._load_mux_av(self._root).main(argv))
            if code != 0 or not out_path.is_file():
                # Don't leave a half-written cut sitting in the output folder
                # under a name that looks like a finished render.
                out_path.unlink(missing_ok=True)
                raise MuxFailedError(f"mux_av.py exited {code}")
            return MuxResult(output=out_path, download_name=out_path.name)
        except Exception:
            out_path.unlink(missing_ok=True)
            raise
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    @staticmethod
    def _resolve_default_output_dir() -> Path:
        override = os.environ.get(OUTPUT_DIR_ENV_VAR, "").strip()
        return Path(override) if override else Path.home() / "Downloads"

    def _unique_output(self, name: str) -> Path:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        candidate = self._output_dir / name
        stem, ext = Path(name).stem, Path(name).suffix
        n = 1
        while candidate.exists():
            candidate = self._output_dir / f"{stem}_{n}{ext}"
            n += 1
        return candidate

    @staticmethod
    def _checked_ext(name: str, allowed: frozenset[str], label: str) -> str:
        ext = Path(name).suffix.lower()
        if ext not in allowed:
            raise UnsupportedMediaError(f"unsupported {label} type: {ext or name!r}")
        return ext

    @staticmethod
    def _spill(stream: BinaryIO, dst: Path) -> None:
        """Stream the upload to disk. `copyfileobj`, never `.read()`: a cut can be
        hundreds of MB and must not be held in memory."""
        stream.seek(0)
        with dst.open("wb") as fh:
            shutil.copyfileobj(stream, fh)

    @staticmethod
    def _download_name(video_name: str) -> str:
        stem = _UNSAFE_STEM.sub("_", Path(video_name).stem).strip("_")
        return f"{stem or 'video'}_bgm.mp4"

    @staticmethod
    def _load_mux_av(root: Path) -> ModuleType:
        path = root / "tools" / "mux_av.py"
        spec = importlib.util.spec_from_file_location("mux_av_tool", path)
        if spec is None or spec.loader is None:
            raise MuxFailedError(f"mux_av tool not found at {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
