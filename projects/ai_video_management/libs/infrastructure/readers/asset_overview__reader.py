"""资产总览（follow-up 293）：一部剧的人物、背景、道具，每个资产目录一格。只读。

人物与道具是 `{characters|props}/[{分组}/]{键}_{名}/`（`asset_group`），背景是 `background/` 下任意深度的
`bg{N}_{主体}/`（`series_shared.scene_subject_dirs`）；系列成员连同 `_series/` 共享资产一起列。每格读目录顶层的
图片、视频，与 `{目录}.md` 开头：首个 `# ` 行是名字，它前面的 `> ` 引用行是键与状态。形态 / 换装子目录、`ref/`、
`skills/` 等不列（人物的技能在预览里另取 `GET /api/character-reel`）。
"""
from __future__ import annotations

import re
from pathlib import Path

from libs.common import drama_layout, drama_ref, series_shared
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.drama__error import DramaNotFoundError, InvalidDramaPathError
from libs.infrastructure.daos.asset_overview__dao import AssetFolderDao

IMAGE_EXTS = frozenset({".png", ".jpg", ".jpeg", ".webp", ".gif"})
VIDEO_EXTS = frozenset({".mp4", ".mov", ".webm", ".m4v"})
TITLE_RE = re.compile(r"^# (.+)$", re.M)
HEAD_CHARS = 6000

LAYOUTS = (("characters", drama_layout.characters_dir), ("props", drama_layout.props_dir))


class AssetOverviewReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root
        self.resolver = SafeResolver(repo_root)

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def drama_dir(self, rel: str) -> tuple[Path, str]:
        """(剧目录, 规范化的仓库相对路径)；不是 `ai_videos/{剧}` 或系列成员根抛 InvalidDramaPathError。"""
        norm = rel.strip().replace("\\", "/").strip("/")
        parts = norm.split("/")
        if not norm or drama_ref.drama_depth(self.root, parts) != len(parts):
            raise InvalidDramaPathError(f"不是剧目录：{rel}")
        resolved = self.resolver.resolve(norm)
        if resolved is None:
            raise InvalidDramaPathError(f"不是剧目录：{rel}")
        if not resolved.is_dir():
            raise DramaNotFoundError(f"剧目录不存在：{rel}")
        return resolved, norm

    def read(self, rel: str) -> tuple[str, dict[str, list[AssetFolderDao]], list[str]]:
        """(剧路径, {种类: 资产目录}, 要盯的目录)。"""
        drama, norm = self.drama_dir(rel)
        roots = series_shared.asset_roots(drama)
        out: dict[str, list[AssetFolderDao]] = {}
        for kind, layout in LAYOUTS:
            out[kind] = [self._folder(kind, d, layout(root), root is not drama)
                         for root in roots for d in series_shared.layout_children(layout, root)
                         if (d / f"{d.name}.md").is_file() or self._has_media(d)]
        out["background"] = [self._folder("background", d, self._background_root(d, roots), self._shared(d, drama))
                             for d in series_shared.scene_subject_dirs(drama)]
        watch = sorted({self._rel(layout(root)) for root in roots
                        for layout in (drama_layout.characters_dir, drama_layout.props_dir, drama_layout.background_dir)
                        if layout(root).is_dir()})
        return norm, out, watch

    @staticmethod
    def _background_root(folder: Path, roots: list[Path]) -> Path:
        for root in roots:
            base = drama_layout.background_dir(root)
            if base in folder.parents:
                return base
        return folder.parent

    @staticmethod
    def _shared(folder: Path, drama: Path) -> bool:
        return drama not in folder.parents

    @staticmethod
    def _has_media(folder: Path) -> bool:
        try:
            return any(p.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS for p in folder.iterdir() if p.is_file())
        except OSError:
            return False

    def _folder(self, kind: str, folder: Path, base: Path, shared: bool) -> AssetFolderDao:
        try:
            group_parts = list(folder.parent.relative_to(base).parts)
        except ValueError:
            group_parts = []
        group = "/".join(([drama_ref.SERIES_SHARED_DIR_NAME] if shared else []) + group_parts)
        card = folder / f"{folder.name}.md"
        title, meta = "", []
        if card.is_file() and not card.is_symlink():
            try:
                with card.open(encoding="utf-8", errors="replace") as fh:
                    head = fh.read(HEAD_CHARS)
            except OSError:
                head = ""
            found = TITLE_RE.search(head)
            title = found.group(1).strip() if found else ""
            before = head[: found.start()] if found else ""
            meta = [line[1:].strip() for line in before.splitlines() if line.startswith(">") and line[1:].strip()]
        images: list[str] = []
        videos: list[tuple[str, float]] = []
        try:
            entries = sorted(folder.iterdir())
        except OSError:
            entries = []
        for entry in entries:
            if not entry.is_file() or entry.is_symlink():
                continue
            ext = entry.suffix.lower()
            if ext in IMAGE_EXTS:
                images.append(self._rel(entry))
            elif ext in VIDEO_EXTS:
                videos.append((self._rel(entry), entry.stat().st_mtime))
        return AssetFolderDao(kind, folder.name, self._rel(folder), group,
                              self._rel(card) if card.is_file() else "", title, meta, images, videos)
