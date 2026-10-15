from __future__ import annotations

from pathlib import Path

from libs.common import drama_ref

TEXT_EXTENSIONS: frozenset[str] = frozenset(
    {".md", ".json", ".yaml", ".yml", ".jsonl", ".txt", ".toml"}
)
ALLOWED_EXTENSIONS: frozenset[str] = TEXT_EXTENSIONS | {".png", ".jpg"}
# Media files (per follow-up 005): visible in sidebar tree; served via /api/media
# (raw FileResponse, bypasses MAX_FILE_BYTES). User-rendered turntable mp4 / scene
# ref png / shot output video etc. — gitignored, but webapp displays inline.
# `.pdf` rides the same path (reference decks a user drops into a drama folder);
# it stays OUT of ALLOWED_EXTENSIONS so /api/file never tries to decode it as text.
# `.glb` / `.gltf` likewise: white-model meshes handed back by image-to-3D, previewed
# in-browser so the user can judge a mesh without opening Blender.
MEDIA_EXTENSIONS: frozenset[str] = frozenset(
    {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp",
     ".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v",
     ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac",
     ".pdf", ".glb", ".gltf"}
)
# Listed in the tree and served by /api/media as a plain download, but NOT media:
# the downloads import and the rename pass both key off MEDIA_EXTENSIONS, and a
# `.blend` is a script-built scene file (`_blender/{bg}.blend`) neither may touch.
DOWNLOAD_ONLY_EXTENSIONS: frozenset[str] = frozenset({".blend"})
TREE_VISIBLE_EXTENSIONS: frozenset[str] = ALLOWED_EXTENSIONS | MEDIA_EXTENSIONS | DOWNLOAD_ONLY_EXTENSIONS
MAX_FILE_BYTES: int = 1_048_576

_EXCLUDED_DIRS: frozenset[str] = frozenset(
    {"node_modules", ".git", ".audit", "__pycache__", ".pytest_cache", "dist", "build", ".vite"}
)


_ALLOWED_TOP_LEVEL: frozenset[str] = frozenset({"ai_videos"})


class ExposedTree:
    """The webapp's read/write tree exposes one root: ai_videos/**.

    Follow-ups 096 / 113 had added `downloaded_novels/` and `my_novel/` beside it;
    follow-up 233 took both out again with the novel browsing (their data stays
    on disk, outside the sandbox). Same security controls throughout (extension
    allowlist, _EXCLUDED_DIRS filter, traversal hardening).
    """

    def __init__(self, repo_root: Path) -> None:
        self._root = repo_root.resolve()

    @property
    def root(self) -> Path:
        return self._root

    def ai_video_dirs(self) -> list[Path]:
        """Leaf drama folders — flat ones plus every member of a series folder.

        A series (`ai_videos/{s}/series.json`) is never itself a drama, so it is
        replaced here by its member dramas; see `libs.common.drama_ref`.
        """
        return drama_ref.drama_dirs(self._root)

    def is_inside(self, rel: str) -> bool:
        if not rel or rel.startswith("/") or "\\" in rel or "\x00" in rel:
            return False
        candidate = (self._root / rel).resolve(strict=False)
        if not (candidate == self._root or self._root in candidate.parents):
            return False
        try:
            relative = candidate.relative_to(self._root)
        except ValueError:
            return False
        parts = relative.parts
        if not parts:
            return False
        first = parts[0]
        if first in _ALLOWED_TOP_LEVEL:
            for seg in parts:
                if seg in _EXCLUDED_DIRS:
                    return False
            return True
        return False

    def excluded_dirs(self) -> frozenset[str]:
        return _EXCLUDED_DIRS
