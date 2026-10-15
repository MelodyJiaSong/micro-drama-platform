"""Character-video aggregate writer: extract a character turntable's three
views (front / side / back PNG) + audio (mp3) + first-2s trim into `views/`.

Used by the 🖼 extraction buttons, the character gallery's one-click batch, and
`apps.cli.extract_views` (which `tools/char_assets.py` runs per drama). The
old per-character 2-second truncation and per-shot character reel (prompts/
shotNN/shotNN.md) were removed with the old pipeline (follow-up 233).

ffmpeg binary supplied by `imageio-ffmpeg` — no system install required.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import imageio_ffmpeg

from libs.common import drama_ref
from libs.common.character_dir import CHARACTER_DIR_RE as _CHARACTER_DIR_RE
from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.domain.value_objects.character_video__valueobject import (
    CANONICAL_VIEWS,
    TRIM_DURATION_S,
    audio_output_filename,
    trim_output_filename,
    view_output_filename,
)
from libs.domain.errors.character_video__error import (
    CharacterVideoDomainError,
    CharacterVideoNotFoundError,
    FfmpegMissingForCharacterVideoError,
    InvalidCharacterVideoPathError,
    InvalidCharactersDirError,
    NotCharacterVideoError,
    ViewExtractFailedError,
)


VIDEO_EXTENSIONS: frozenset[str] = frozenset(
    {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"}
)

# A 2-second `video.mp4` reel the removed truncate button used to write into a
# character folder. Old folders may still hold one; it is never a turntable source.
_LEGACY_REEL_NAME: str = "video.mp4"

# Path shape: ai_videos / {drama} / characters / {cN_xxx} / {filename}.{ext}
# (`{drama}` is one OR two segments — a series member is `{series}/{drama}`.)


def is_under_character_folder(root: Path, rel: str) -> bool:
    """True when `rel` points inside `…/characters/{cN_xxx}/`.

    Needs `root` because the owning folder is **two or three** segments
    depending on whether the second one is a series folder, and that question is
    only answerable against the filesystem (`libs.common.drama_ref` — the single
    place allowed to resolve it; CLAUDE.md forbids re-deriving it from depth).

    `asset_root_depth`, not `drama_depth`: a character shared by several
    episodes lives in `ai_videos/{series}/_series/characters/`, which is not a
    drama, so `drama_depth` answers None for it and every extraction on a shared
    character's turntable video came back `not_a_character_video`.

    Module-level on purpose: the previous shape — a `@staticmethod` whose body
    reached for `self._resolver.root` — raised `NameError: name 'self' is not
    defined` on every call, which took out extract-views / extract-all for
    **every** drama (regression in 8907992, the series-nesting refactor).
    """
    parts = rel.split("/")
    depth = drama_ref.asset_root_depth(root, parts)
    if depth is None:
        return False
    # `characters/` sits at the drama root (legacy) or under a stage folder
    # (staged pipeline `2_世界观人设/characters/`) — so exactly `depth` or
    # `depth + 1`. Anywhere deeper is some other folder that happens to be
    # named `characters`, and must not pass.
    for ci in (depth, depth + 1):
        if ci < len(parts) and parts[ci] == "characters":
            return ci + 1 < len(parts) and bool(_CHARACTER_DIR_RE.match(parts[ci + 1]))
    return False


# --- View + audio extraction (Feature 3, per follow-up 093) -----------------


_VIEW_FFMPEG_TIMEOUT_S: int = 30
_AUDIO_FFMPEG_TIMEOUT_S: int = 60
_TRIM_FFMPEG_TIMEOUT_S: int = 60
_VIEWS_SUBDIR: str = "views"
_AUDIO_MP3_QUALITY: str = "4"  # libmp3lame VBR ~165 kbps — small, transparent for speech


@dataclass(frozen=True)
class ViewResult:
    timestamp: float
    role: str
    out_rel: str

    def to_payload(self) -> dict[str, object]:
        return {"timestamp": self.timestamp, "role": self.role, "path": self.out_rel}


@dataclass(frozen=True)
class AudioResult:
    out_rel: str

    def to_payload(self) -> dict[str, object]:
        return {"path": self.out_rel}


@dataclass(frozen=True)
class TrimResult:
    out_rel: str
    duration_seconds: float

    def to_payload(self) -> dict[str, object]:
        return {"path": self.out_rel, "duration_seconds": self.duration_seconds}


@dataclass(frozen=True)
class ViewExtractResult:
    src_rel: str
    views: tuple[ViewResult, ...]
    audio: AudioResult | None
    trim: TrimResult | None
    failures: tuple[tuple[str, str], ...]  # (target, error_msg) where target is "front"/"side"/"back"/"audio"/"trim"

    def to_payload(self) -> dict[str, object]:
        return {
            "src": self.src_rel,
            "views": [v.to_payload() for v in self.views],
            "audio": self.audio.to_payload() if self.audio is not None else None,
            "trim": self.trim.to_payload() if self.trim is not None else None,
            "failures": [{"target": t, "error": e} for (t, e) in self.failures],
        }


@dataclass(frozen=True)
class BatchViewItem:
    """One character folder's outcome in a batch (extract-all) run."""

    folder: str  # character folder name, e.g. "c1_裴知秋"
    status: str  # "ok" | "skipped" | "error"
    result: ViewExtractResult | None
    reason: str  # "" for ok; explanation for skipped/error

    def to_payload(self) -> dict[str, object]:
        return {
            "folder": self.folder,
            "status": self.status,
            "result": self.result.to_payload() if self.result is not None else None,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class BatchViewExtractResult:
    characters_rel: str
    items: tuple[BatchViewItem, ...]

    def to_payload(self) -> dict[str, object]:
        return {
            "characters_dir": self.characters_rel,
            "items": [i.to_payload() for i in self.items],
        }


class CharacterViewExtractor:
    """Extracts 3 angle PNGs (front/side/back) + the full audio (mp3) + a
    first-`TRIM_DURATION_S`-seconds trimmed mp4 from a character turntable mp4
    — 5 outputs in one click. They land in `{src.parent}/views/` with
    `{src.parent.name}_{role}.png` + `{src.parent.name}_audio.mp3` +
    `{src.parent.name}_trim{N}s.mp4` naming so re-extraction in the same
    character folder overwrites the same outputs regardless of mp4 stem (the
    latest extraction is the single source of truth in `views/`).

    Source selection: the request may point at any video in the character
    folder, but extraction always runs on the **newest original turntable mp4
    by mtime** (per 2026-06-27 follow-up '多个原始视频选最新') — the truncated
    `video.mp4` reel and the `views/` outputs are never candidates.

    Per follow-up 093 (3 views + audio); the trimmed mp4 was added so the same
    button yields all 5 reference files. The 3 timestamps live in
    `libs/domain/value_objects/character_video__valueobject.py` and are
    pinned to rule #12.5 v10.2's camera path.
    """

    def __init__(self, exposed: ExposedTree, resolver: SafeResolver) -> None:
        self._exposed = exposed
        self._resolver = resolver

    def _latest_video_in(self, folder: Path) -> Path | None:
        """Newest original turntable mp4 directly in `folder` by mtime, or None.

        Per 2026-06-27 follow-up '多个原始视频选最新': when the folder holds
        several downloaded turntable videos, extraction runs on the latest by
        mtime. Candidates are video files directly in the folder, excluding the
        truncated `video.mp4` reel (a generated artifact); `views/` outputs live
        in a subfolder and are never enumerated here.
        """
        try:
            entries = list(folder.iterdir())
        except OSError:
            return None
        candidates = [
            entry
            for entry in entries
            if entry.is_file()
            and not entry.is_symlink()
            and entry.suffix.lower() in VIDEO_EXTENSIONS
            and entry.name != _LEGACY_REEL_NAME
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda p: p.stat().st_mtime)

    def _resolve_latest_source(self, validated_src: Path) -> Path:
        """Newest original turntable mp4 in the character folder, falling back
        to the validated source when no other candidate exists."""
        return self._latest_video_in(validated_src.parent) or validated_src

    def extract(self, rel: str) -> ViewExtractResult:
        src = self._resolve_latest_source(self._validate_character_video_source(rel))
        return self._extract_source(src)

    def _extract_source(self, src: Path) -> ViewExtractResult:
        try:
            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception as exc:
            raise FfmpegMissingForCharacterVideoError(str(exc)) from exc
        prefix = src.parent.name
        out_dir = src.parent / _VIEWS_SUBDIR
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise ViewExtractFailedError(f"could not create views dir: {exc}") from exc
        self._sweep_outputs(out_dir)
        views: list[ViewResult] = []
        failures: list[tuple[str, str]] = []
        for spec in CANONICAL_VIEWS:
            out_path = out_dir / view_output_filename(prefix, spec)
            ok, err = self._run_view(ffmpeg, src, spec.timestamp, out_path)
            if ok:
                views.append(
                    ViewResult(
                        timestamp=spec.timestamp,
                        role=spec.role,
                        out_rel=self._rel(out_path),
                    )
                )
            else:
                failures.append((spec.role, err))
        audio_path = out_dir / audio_output_filename(prefix)
        audio: AudioResult | None
        ok, err = self._run_audio(ffmpeg, src, audio_path)
        if ok:
            audio = AudioResult(out_rel=self._rel(audio_path))
        else:
            audio = None
            failures.append(("audio", err))
        trim_path = out_dir / trim_output_filename(prefix)
        trim: TrimResult | None
        ok, err = self._run_trim(ffmpeg, src, trim_path)
        if ok:
            trim = TrimResult(out_rel=self._rel(trim_path), duration_seconds=TRIM_DURATION_S)
        else:
            trim = None
            failures.append(("trim", err))
        if not views and audio is None and trim is None:
            joined = "; ".join(f"{tgt}: {e}" for (tgt, e) in failures)
            raise ViewExtractFailedError(joined or "no outputs produced")
        return ViewExtractResult(
            src_rel=self._rel(src),
            views=tuple(views),
            audio=audio,
            trim=trim,
            failures=tuple(failures),
        )

    def _run_view(
        self,
        ffmpeg: str,
        src: Path,
        timestamp: float,
        out_path: Path,
    ) -> tuple[bool, str]:
        cmd = [
            ffmpeg,
            "-y",
            "-ss", f"{timestamp}",
            "-i", str(src),
            "-frames:v", "1",
            "-q:v", "1",
            "-loglevel", "error",
            str(out_path),
        ]
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                timeout=_VIEW_FFMPEG_TIMEOUT_S,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, "ffmpeg_timeout"
        if completed.returncode != 0 or not out_path.is_file():
            err = completed.stderr.decode("utf-8", errors="replace").strip()[:200]
            return False, err or "ffmpeg_failed"
        return True, ""

    def _run_audio(
        self,
        ffmpeg: str,
        src: Path,
        out_path: Path,
    ) -> tuple[bool, str]:
        cmd = [
            ffmpeg,
            "-y",
            "-i", str(src),
            "-vn",
            "-c:a", "libmp3lame",
            "-q:a", _AUDIO_MP3_QUALITY,
            "-loglevel", "error",
            str(out_path),
        ]
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                timeout=_AUDIO_FFMPEG_TIMEOUT_S,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, "ffmpeg_timeout"
        if completed.returncode != 0 or not out_path.is_file():
            err = completed.stderr.decode("utf-8", errors="replace").strip()[:200]
            return False, err or "ffmpeg_failed"
        return True, ""

    def _run_trim(
        self,
        ffmpeg: str,
        src: Path,
        out_path: Path,
    ) -> tuple[bool, str]:
        cmd = [
            ffmpeg,
            "-y",
            "-i", str(src),
            "-t", str(TRIM_DURATION_S),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-movflags", "+faststart",
            "-loglevel", "error",
            str(out_path),
        ]
        try:
            completed = subprocess.run(
                cmd,
                capture_output=True,
                timeout=_TRIM_FFMPEG_TIMEOUT_S,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, "ffmpeg_timeout"
        if completed.returncode != 0 or not out_path.is_file():
            err = completed.stderr.decode("utf-8", errors="replace").strip()[:200]
            return False, err or "ffmpeg_failed"
        return True, ""

    def _sweep_outputs(self, views_dir: Path) -> None:
        try:
            entries = list(views_dir.iterdir())
        except OSError:
            return
        for entry in entries:
            if entry.is_symlink() or not entry.is_file():
                continue
            suffix = entry.suffix.lower()
            if suffix not in (".png", ".mp3", ".mp4"):
                continue
            try:
                entry.unlink()
            except OSError:
                continue

    def _validate_character_video_source(self, rel: str) -> Path:
        if not isinstance(rel, str) or rel == "":
            raise InvalidCharacterVideoPathError("path is empty")
        if not self._exposed.is_inside(rel):
            raise InvalidCharacterVideoPathError("path outside sandbox")
        ext = Path(rel).suffix.lower()
        if ext not in VIDEO_EXTENSIONS:
            raise NotCharacterVideoError("extension is not a video type")
        if not is_under_character_folder(self._resolver.root, rel):
            raise NotCharacterVideoError(
                "path must be under ai_videos/{drama}/characters/{cN_xxx|mN_xxx}/"
            )
        resolved = self._resolver.resolve(rel)
        if resolved is None:
            raise InvalidCharacterVideoPathError("path failed sandbox resolution")
        if resolved.is_symlink():
            raise InvalidCharacterVideoPathError("symlink is not allowed")
        if not resolved.is_file():
            raise CharacterVideoNotFoundError("file does not exist")
        return resolved

    def _rel(self, p: Path) -> str:
        try:
            return p.resolve().relative_to(self._resolver.root).as_posix()
        except (OSError, ValueError):
            return p.as_posix()

    # --- Batch extract-all (one click → every character) --------------------

    def extract_all(self, characters_rel: str) -> BatchViewExtractResult:
        """Run view/audio/trim extraction for every `cN_*` character folder
        under a drama's `characters/` dir, each on its newest turntable mp4.

        Folders with no turntable video are reported `skipped`; per-folder
        ffmpeg/validation failures are reported `error` (the run never aborts
        on one bad folder). Per 2026-06-27 follow-up: a single click on the
        character gallery regenerates every character's 3 views + audio + trim.
        """
        chars_dir = self._validate_characters_dir(characters_rel)
        items: list[BatchViewItem] = []
        for sub in sorted(chars_dir.iterdir(), key=lambda p: p.name):
            if not sub.is_dir() or sub.is_symlink():
                continue
            if not _CHARACTER_DIR_RE.match(sub.name):
                continue
            src = self._latest_video_in(sub)
            if src is None:
                items.append(BatchViewItem(sub.name, "skipped", None, "no turntable video"))
                continue
            try:
                result = self._extract_source(src)
                items.append(BatchViewItem(sub.name, "ok", result, ""))
            except CharacterVideoDomainError as exc:
                items.append(
                    BatchViewItem(sub.name, "error", None, str(exc) or type(exc).__name__)
                )
        return BatchViewExtractResult(
            characters_rel=self._rel(chars_dir),
            items=tuple(items),
        )

    def _validate_characters_dir(self, rel: str) -> Path:
        if not isinstance(rel, str) or rel == "":
            raise InvalidCharactersDirError("path is empty")
        if not self._exposed.is_inside(rel):
            raise InvalidCharactersDirError("path outside sandbox")
        parts = rel.split("/")
        # `asset_root_depth`: a series' shared `_series/characters/` owns the
        # characters its episodes reuse, and is not a drama.
        depth = drama_ref.asset_root_depth(self._resolver.root, parts)
        if depth is None or len(parts) < depth + 1:
            raise InvalidCharactersDirError("path must be ai_videos/{drama}/.../characters/")
        if parts[-1] != "characters":
            raise InvalidCharactersDirError("path must end in characters/")
        resolved = self._resolver.resolve(rel)
        if resolved is None:
            raise InvalidCharactersDirError("path failed sandbox resolution")
        if resolved.is_symlink():
            raise InvalidCharactersDirError("symlink is not allowed")
        if not resolved.is_dir():
            raise InvalidCharactersDirError("characters dir does not exist")
        return resolved
