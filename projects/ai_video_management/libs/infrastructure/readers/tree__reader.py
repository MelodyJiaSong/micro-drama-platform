from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from libs.common import asset_link, drama_ref
from libs.common.exposed_tree import ExposedTree, TREE_VISIBLE_EXTENSIONS
from libs.common.sub_type_lookup import lookup as sub_type_lookup
from libs.domain.value_objects.bgm__valueobject import CATEGORY_LABELS_ZH as BGM_CATEGORY_LABELS_ZH
from libs.domain.value_objects.novel__valueobject import CANONICAL_NOVELS, categories as novel_categories

_IMAGE_EXTENSIONS: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"})
_VIDEO_EXTENSIONS: frozenset[str] = frozenset({".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"})
_AUDIO_EXTENSIONS: frozenset[str] = frozenset({".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"})
_PDF_EXTENSIONS: frozenset[str] = frozenset({".pdf"})
# White-model meshes (image-to-3D output / `tools/whitemodel_normalize.py` input).
# Their own node type so the sidebar marks them and the UI knows to preview them
# in <model-viewer> rather than treat them as an opaque download.
_MODEL_EXTENSIONS: frozenset[str] = frozenset({".glb", ".gltf"})
_CJK_RE = re.compile("[\u4e00-\u9fff]")
_ACTOR_FOLDER_RE = re.compile(r"^actor_\d{4,}$")
_VOICE_FOLDER_RE = re.compile(r"^voice_\d{4,}$")
# Chinese display labels for the shared system folders under `ai_videos/` (they
# carry no README/concept H1 to derive a title from). Each of these is its own
# "library" main page in the UI.
_SYSTEM_FOLDER_LABELS_ZH: dict[str, str] = {
    "_actors": "演员库",
    "_bgm": "背景音乐库",
    "_research": "选题调研",
}


class TreeReader:
    """Walks the EXPOSED_TREE root and emits the recursive TreeNode shape.

    Single section: "AI Videos".
    """

    def __init__(self, exposed: ExposedTree) -> None:
        self._exposed = exposed
        self._root = exposed.root
        self._root_prefix = str(self._root).rstrip(os.sep) + os.sep

    def build(self) -> dict[str, Any]:
        return {
            "type": "section",
            "name": "root",
            "path": "",
            "children": [
                self._ai_videos_section(),
                self._downloaded_novels_section(),
                self._my_novel_section(),
            ],
        }

    def _ai_videos_section(self) -> dict[str, Any]:
        ai_videos_root = self._root / "ai_videos"
        children: list[dict[str, Any]] = []
        deleted_child: dict[str, Any] | None = None
        if ai_videos_root.is_dir():
            for project_dir in sorted(p for p in ai_videos_root.iterdir() if p.is_dir()):
                if project_dir.name in self._exposed.excluded_dirs():
                    continue
                if drama_ref.is_series_dir(project_dir):
                    series_node = self._walk_series(project_dir)
                    if series_node is not None:
                        children.append(series_node)
                    continue
                project_node = self._walk_project(project_dir)
                if project_node is None:
                    continue
                if project_dir.name == "_deleted":
                    deleted_child = project_node
                else:
                    children.append(project_node)
        if deleted_child is not None:
            children.append(deleted_child)
        return {
            "type": "section",
            "name": "AI Videos",
            "path": "",
            "children": children,
        }

    def _downloaded_novels_section(self) -> dict[str, Any]:
        """Scraped baseline corpus, organized as `downloaded_novels/{category}/{slug}/`.
        Filters to novels whose `_meta.json.complete == True` (per follow-up 104).
        """
        root = self._root / "downloaded_novels"
        children: list[dict[str, Any]] = []
        if root.is_dir():
            category_zh = dict(novel_categories())
            slug_to_title: dict[str, str] = {s.slug: s.title_zh for s in CANONICAL_NOVELS}
            slug_order: dict[str, int] = {s.slug: i for i, s in enumerate(CANONICAL_NOVELS)}
            cat_order: dict[str, int] = {c: i for i, (c, _) in enumerate(novel_categories())}
            for cat_dir in sorted(
                (p for p in root.iterdir() if p.is_dir() and not p.is_symlink()),
                key=lambda p: cat_order.get(p.name, 9999),
            ):
                if cat_dir.name in self._exposed.excluded_dirs():
                    continue
                novel_nodes: list[dict[str, Any]] = []
                for novel_dir in sorted(
                    (p for p in cat_dir.iterdir() if p.is_dir() and not p.is_symlink()),
                    key=lambda p: slug_order.get(p.name, 9999),
                ):
                    if novel_dir.name in self._exposed.excluded_dirs():
                        continue
                    if not self._novel_is_complete(novel_dir):
                        continue
                    sub = self._walk_filtered(novel_dir, self._is_allowed_leaf)
                    novel_nodes.append(
                        {
                            "type": "directory",
                            "name": novel_dir.name,
                            "display_name": slug_to_title.get(novel_dir.name, novel_dir.name),
                            "path": self._rel(novel_dir),
                            "children": sub,
                        }
                    )
                if not novel_nodes:
                    continue
                children.append(
                    {
                        "type": "directory",
                        "name": cat_dir.name,
                        "display_name": category_zh.get(cat_dir.name, cat_dir.name),
                        "path": self._rel(cat_dir),
                        "children": novel_nodes,
                    }
                )
            for entry in sorted(
                (p for p in root.iterdir() if p.is_file() and not p.is_symlink()),
                key=lambda p: p.name.lower(),
            ):
                if self._is_allowed_leaf(entry):
                    children.append(self._leaf_for(entry))
        return {
            "type": "section",
            "name": "Downloaded Novels",
            "path": "",
            "children": children,
        }

    def _my_novel_section(self) -> dict[str, Any]:
        """Original manuscripts authored for AI-short-drama production. No
        canonical-slug ordering and no completeness filter — every subdir of
        `my_novel/` surfaces verbatim, walked with the same leaf-allowlist as
        the rest of the tree.
        """
        root = self._root / "my_novel"
        children: list[dict[str, Any]] = []
        if root.is_dir():
            for project_dir in sorted(
                (p for p in root.iterdir() if p.is_dir() and not p.is_symlink()),
                key=lambda p: p.name.lower(),
            ):
                if project_dir.name in self._exposed.excluded_dirs():
                    continue
                sub = self._walk_filtered(project_dir, self._is_allowed_leaf)
                node: dict[str, Any] = {
                    "type": "directory",
                    "name": project_dir.name,
                    "path": self._rel(project_dir),
                    "children": sub,
                }
                zh_title = self._project_zh_title(project_dir)
                if zh_title:
                    node["display_name"] = zh_title
                children.append(node)
            for entry in sorted(
                (p for p in root.iterdir() if p.is_file() and not p.is_symlink()),
                key=lambda p: p.name.lower(),
            ):
                if self._is_allowed_leaf(entry):
                    children.append(self._leaf_for(entry))
        return {
            "type": "section",
            "name": "My Novel",
            "path": "",
            "children": children,
        }

    def _novel_is_complete(self, novel_dir: Path) -> bool:
        """Per follow-up 104: the Novels section only surfaces novels whose
        `_meta.json.complete == True`. In-progress downloads stay on disk
        (resume checkpoint preserved) but are filtered out of the sidebar.
        """
        meta_path = novel_dir / "_meta.json"
        if not meta_path.is_file():
            return False
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return False
        return bool(data.get("complete", False))

    def _walk_project(self, project_dir: Path) -> dict[str, Any] | None:
        sub = self._walk_filtered(project_dir, self._is_allowed_leaf)
        drama_key = self._rel(project_dir).split("/", 1)[1]
        meta = sub_type_lookup(self._root, drama_key)
        project_meta_payload: dict[str, Any] | None = None
        if meta.sub_type is not None or meta.shot_count is not None or meta.episode_count is not None:
            project_meta_payload = {
                "sub_type": meta.sub_type,
                "shot_count": meta.shot_count,
                "episode_count": meta.episode_count,
            }
        node: dict[str, Any] = {
            "type": "directory",
            "name": project_dir.name,
            "path": self._rel(project_dir),
            "children": sub,
            "project_meta": project_meta_payload,
        }
        # `is_drama` is the UI's only way to know where a drama root sits — a flat
        # drama is 2 segments, a series member 3. Nothing downstream may re-derive
        # that from path depth.
        if not project_dir.name.startswith("_"):
            node["is_drama"] = True
        zh_title = _SYSTEM_FOLDER_LABELS_ZH.get(project_dir.name) or self._project_zh_title(project_dir)
        if zh_title:
            node["display_name"] = zh_title
        return node

    def _walk_series(self, series_dir: Path) -> dict[str, Any] | None:
        """A series folder (`series.json`) renders as one collapsible node whose
        children are its member dramas, plus any `_`-prefixed shared folder
        (`_series/` — the series bible and cross-episode locked assets)."""
        members: list[dict[str, Any]] = []
        shared: list[dict[str, Any]] = []
        for entry in sorted(p for p in series_dir.iterdir() if p.is_dir()):
            if entry.name in self._exposed.excluded_dirs():
                continue
            node = self._walk_project(entry)
            if node is None:
                continue
            if entry.name.startswith("_"):
                node.pop("is_drama", None)
                node.pop("project_meta", None)
                if entry.name == drama_ref.SERIES_SHARED_DIR_NAME:
                    node["display_name"] = "系列共用"
                shared.append(node)
            else:
                members.append(node)
        loose = self._walk_filtered(series_dir, self._is_allowed_leaf, dirs=False)
        return {
            "type": "series",
            "name": series_dir.name,
            "display_name": self._series_zh_title(series_dir),
            "path": self._rel(series_dir),
            "children": shared + members + loose,
        }

    def _series_zh_title(self, series_dir: Path) -> str:
        try:
            data = json.loads((series_dir / drama_ref.SERIES_MARKER_NAME).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return series_dir.name
        name = data.get("name_zh")
        return name if isinstance(name, str) and name else series_dir.name

    def _project_zh_title(self, project_dir: Path) -> str | None:
        """Chinese display title for a drama folder (pinyin / English on disk).

        Legacy: `ai_videos/{name}/README.md` first H1 `# 《<title>》— …`.
        Staged pipeline (no top-level README): the title lives in
        `1_立项/concept.md`'s H1, shape `# 立项策划单 · 武神觉醒` → 武神觉醒.
        Also reused by `my_novel/{name}/README.md`.
        """
        title = self._h1_zh(project_dir / "README.md")
        if title:
            return title
        return self._h1_zh(project_dir / "1_立项" / "concept.md")

    def _h1_zh(self, md_path: Path) -> str | None:
        """Extract a Chinese display title from a markdown file's first H1.
        Priority: 《…》 → （…） → text after a middle-dot separator (· / ・) →
        the whole H1 text. None when the file is missing or has no H1.

        The （…） rule only fires when the text before the parenthesis has no
        CJK — `pinyin（中文）` means the parenthetical IS the title, but
        `热血高校（预告片）` means it is a qualifier, so it is dropped and the
        head keeps flowing through the middle-dot rule.
        """
        if not md_path.is_file():
            return None
        try:
            with md_path.open(encoding="utf-8") as fh:
                for line in fh:
                    stripped = line.strip()
                    if stripped.startswith("# "):
                        head = stripped[2:].strip()
                        m = re.search(r"《([^》]+)》", head)
                        if m:
                            return m.group(1)
                        m = re.search(r"[（(]([^）)]+)[）)]", head)
                        if m:
                            before = head[: m.start()].strip()
                            if _CJK_RE.search(before):
                                head = before
                            else:
                                return m.group(1)
                        tail = re.split(r"\s*[·・]\s*", head)[-1].strip()
                        return tail or head or None
        except OSError:
            return None
        return None

    def _sidecar_zh_label(self, directory: Path) -> str | None:
        """Chinese display label for a nested pinyin-named directory.

        1) Performance-library emotion folders (`_performances/{emotion}/`) hold
           the Chinese name in `_emotion.md`'s H1 (`# 压抑隐忍（yayi_yinren）`) —
           return the head, dropping the trailing `（pinyin）` annotation.
        2) Scene folders (staged pipeline `…/scenes/{pinyin}/`) hold the Chinese
           name in `{pinyin}.md`'s H1 (`# zhenbei_wangfu_zhengting（镇北王府正厅）`)
           — return the `（中文）` group.
        3) BGM emotion-category folders (`_bgm/{category}/`) have no sidecar; the
           Chinese label comes from the closed `BGM_CATEGORY_LABELS_ZH` enum
           (`suspense` → 悬疑).
        None when no recognizable sidecar.
        """
        emotion = directory / "_emotion.md"
        if emotion.is_file():
            try:
                with emotion.open(encoding="utf-8") as fh:
                    for line in fh:
                        stripped = line.strip()
                        if stripped.startswith("# "):
                            title = stripped[2:].strip()
                            head = re.split(r"[（(]", title, maxsplit=1)[0].strip()
                            if head:
                                return head
                            break
                        if stripped:
                            break
            except OSError:
                pass
        if directory.parent.name == "scenes":
            label = self._h1_zh(directory / f"{directory.name}.md")
            if label:
                return label
        if directory.parent.name == "_bgm":
            label = BGM_CATEGORY_LABELS_ZH.get(directory.name)
            if label:
                return label
        return None

    def _walk_filtered(
        self, directory: Path, leaf_predicate: Any, dirs: bool = True
    ) -> list[dict[str, Any]]:
        """`dirs=False` emits only the directory's own files — used for a series
        folder, whose sub-directories are walked as drama nodes instead."""
        children: list[dict[str, Any]] = []
        excluded = self._exposed.excluded_dirs()
        # `os.scandir` rather than `Path.iterdir`: on Windows the directory
        # enumeration already carries is_dir / is_file / is_symlink, so reading
        # them off the DirEntry costs nothing, while the `Path` form issued five
        # separate `nt.stat` calls per entry — 106,926 of them (5.1s) across this
        # tree. `is_dir` is asked once here and passed down as a plain bool.
        try:
            with os.scandir(directory) as it:
                scanned = [(Path(e.path), e.name, e.is_dir(follow_symlinks=False),
                            e.is_file(follow_symlinks=False), e.is_symlink())
                           for e in it]
        except OSError:
            return children
        scanned.sort(key=lambda row: (not row[2], row[1].lower()))
        for entry, name, is_dir, is_file, is_symlink in scanned:
            if is_symlink:
                continue
            if name in excluded:
                continue
            if is_dir and not dirs:
                continue
            if is_dir:
                collapsed = self._collapsed_actor_leaf(entry)
                if collapsed is not None:
                    children.append(collapsed)
                    continue
                voice_collapsed = self._collapsed_voice_leaf(entry)
                if voice_collapsed is not None:
                    children.append(voice_collapsed)
                    continue
                sub = self._walk_filtered(entry, leaf_predicate)
                if sub:
                    dir_node: dict[str, Any] = {
                        "type": "directory",
                        "name": name,
                        "path": self._rel(entry),
                        "children": sub,
                    }
                    zh_label = self._sidecar_zh_label(entry)
                    if zh_label:
                        dir_node["display_name"] = zh_label
                    children.append(dir_node)
            elif is_file:
                if asset_link.is_link_file(entry):
                    link_node = self._link_leaf(entry)
                    if link_node is not None:
                        children.append(link_node)
                        continue
                    # 解析不了就按普通 json 显示，让用户看得见、改得了
                if leaf_predicate(entry):
                    children.append(self._leaf_for(entry))
        return children

    def _link_leaf(self, link_file: Path) -> dict[str, Any] | None:
        """A `*.link.json` renders as the asset it points at — the node carries the
        **target's** path, so /api/media and preview work with no media-layer
        change; `is_link` is what tells the UI it is a shortcut, not a copy."""
        link = asset_link.read(self._root, link_file)
        if link is None:
            return None
        node = self._leaf_for(self._root / link.target_rel)
        node["name"] = link.display_name
        node["is_link"] = True
        node["link_at"] = self._rel(link_file)
        if link.note:
            node["link_note"] = link.note
        return node

    def _is_allowed_leaf(self, p: Path) -> bool:
        return p.suffix.lower() in TREE_VISIBLE_EXTENSIONS

    def _collapsed_actor_leaf(self, entry: Path) -> dict[str, Any] | None:
        if not _ACTOR_FOLDER_RE.match(entry.name):
            return None
        try:
            rel_parts = entry.resolve().relative_to(self._root).parts
        except (OSError, ValueError):
            return None
        if len(rel_parts) != 3 or rel_parts[0] != "ai_videos" or rel_parts[1] != "_actors":
            return None
        sidecar = entry / f"{entry.name}.md"
        if not sidecar.is_file():
            return None
        return {
            "type": "actor",
            "name": entry.name,
            "path": self._rel(sidecar),
            "face_path": self._first_face_image(entry),
            "children": [],
        }

    def _first_face_image(self, folder: Path) -> str | None:
        try:
            entries = sorted(folder.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            return None
        for p in entries:
            if p.is_symlink() or not p.is_file():
                continue
            if p.suffix.lower() in _IMAGE_EXTENSIONS:
                return self._rel(p)
        return None

    def _collapsed_voice_leaf(self, entry: Path) -> dict[str, Any] | None:
        """Voice profile folders under `ai_videos/_voices/` collapse to a
        single leaf node (parallel to `_collapsed_actor_leaf` — follow-up 115).
        """
        if not _VOICE_FOLDER_RE.match(entry.name):
            return None
        try:
            rel_parts = entry.resolve().relative_to(self._root).parts
        except (OSError, ValueError):
            return None
        if len(rel_parts) != 3 or rel_parts[0] != "ai_videos" or rel_parts[1] != "_voices":
            return None
        sidecar = entry / f"{entry.name}.md"
        if not sidecar.is_file():
            return None
        return {
            "type": "voice",
            "name": entry.name,
            "path": self._rel(sidecar),
            "audio_path": self._first_audio_sample(entry),
            "children": [],
        }

    def _first_audio_sample(self, folder: Path) -> str | None:
        try:
            entries = sorted(folder.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            return None
        for p in entries:
            if p.is_symlink() or not p.is_file():
                continue
            if p.suffix.lower() in _AUDIO_EXTENSIONS:
                return self._rel(p)
        return None

    def _leaf_for(self, f: Path) -> dict[str, Any]:
        ext = f.suffix.lower()
        if ext in _VIDEO_EXTENSIONS:
            node_type = "video"
        elif ext in _IMAGE_EXTENSIONS:
            node_type = "image"
        elif ext in _AUDIO_EXTENSIONS:
            node_type = "audio"
        elif ext in _PDF_EXTENSIONS:
            node_type = "pdf"
        elif ext in _MODEL_EXTENSIONS:
            node_type = "model"
        else:
            node_type = "file"
        node: dict[str, Any] = {"type": node_type, "name": f.name, "path": self._rel(f)}
        # A scene's main sidecar `.md` (`…/scenes/{pinyin}/{pinyin}.md`) is shown
        # in Chinese in the nav (from its H1 `（中文）`), mirroring the scene
        # folder's display_name. Only the display label changes — `name`/`path`
        # stay pinyin, so import routing / download / open are unaffected.
        if (
            f.suffix.lower() == ".md"
            and f.stem == f.parent.name
            and f.parent.parent.name == "scenes"
        ):
            zh = self._h1_zh(f)
            if zh:
                node["display_name"] = zh
        return node

    def _rel(self, p: Path) -> str:
        """Path relative to the exposed root, POSIX-separated.

        Sliced off the string rather than computed with `resolve()` +
        `relative_to()`. The two are equivalent here — `ExposedTree` resolves the
        root in its constructor, and every path reaching this method was built by
        descending from that root with symlinks skipped, so there is nothing left
        for `resolve()` to normalize. They are not equivalent in cost: profiling
        the 20,573-node tree put `_rel` at 68% of the whole walk (42,034
        `nt._getfinalpathname` calls for 9.5s, plus 8.3s inside `relative_to`),
        which is what made `/api/tree` take 42s and the dev-server proxy give up.

        The resolve-based form stays as the fallback for a path that is not under
        the root, which is the only case where slicing cannot answer.
        """
        s = str(p)
        if s.startswith(self._root_prefix):
            return s[len(self._root_prefix):].replace(os.sep, "/")
        try:
            return p.resolve().relative_to(self._root).as_posix()
        except ValueError:
            return p.as_posix()
