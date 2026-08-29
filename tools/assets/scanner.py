"""Walk `ai_videos/` and hash the media files that belong in the remote store.

Syncable = a media extension, NOT tracked by git (git is the source of truth for
everything it holds — the `0_原作资料/_refs/` reference images stay versioned and
are never duplicated into R2), and not under a skip prefix.

Hashing 7 GB on every invocation is slow, so sha256 is cached by
(size, mtime_ns) in a gitignored sidecar. A file whose size and mtime are
unchanged is not re-read.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from tools.assets.manifest import AssetEntry

MEDIA_EXTENSIONS: frozenset[str] = frozenset(
    {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp",
     ".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v",
     ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac",
     ".pdf"}
)
# `_deleted/` is the webapp's recycle bin — its whole point is that the bytes are
# on their way out. `previz/frames/` is recomputable from previz_config.toml.
_SKIP_TOP_LEVEL: frozenset[str] = frozenset({"_deleted"})
_CACHE_NAME: str = ".assets_cache.json"
_CHUNK: int = 1 << 20


@dataclass(frozen=True)
class ScanResult:
    entries: dict[str, AssetEntry]
    skipped_tracked: int


def _git_tracked(repo_root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "ai_videos"],
        cwd=repo_root, capture_output=True, check=True,
    )
    return {p for p in result.stdout.decode("utf-8").split("\0") if p}


def is_syncable(rel: PurePosixPath) -> bool:
    if rel.suffix.lower() not in MEDIA_EXTENSIONS:
        return False
    parts = rel.parts
    if parts and parts[0] in _SKIP_TOP_LEVEL:
        return False
    return not any(parts[i] == "previz" and parts[i + 1] == "frames" for i in range(len(parts) - 1))


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def scan(repo_root: Path) -> ScanResult:
    media_root = repo_root / "ai_videos"
    tracked = _git_tracked(repo_root)
    cache_path = repo_root / _CACHE_NAME
    cache: dict[str, dict[str, object]] = (
        json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.is_file() else {}
    )
    entries: dict[str, AssetEntry] = {}
    fresh: dict[str, dict[str, object]] = {}
    skipped = 0
    for path in sorted(media_root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = PurePosixPath(path.relative_to(media_root).as_posix())
        if not is_syncable(rel):
            continue
        if f"ai_videos/{rel}" in tracked:
            skipped += 1
            continue
        stat = path.stat()
        hit = cache.get(str(rel))
        if hit and hit.get("size") == stat.st_size and hit.get("mtime_ns") == stat.st_mtime_ns:
            digest = str(hit["sha256"])
        else:
            digest = sha256_of(path)
        entries[str(rel)] = AssetEntry(sha256=digest, size=stat.st_size)
        fresh[str(rel)] = {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns, "sha256": digest}
    cache_path.write_text(json.dumps(fresh, ensure_ascii=False), encoding="utf-8")
    return ScanResult(entries=entries, skipped_tracked=skipped)
