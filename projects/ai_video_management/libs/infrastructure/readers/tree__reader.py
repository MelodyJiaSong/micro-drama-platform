from __future__ import annotations

import json
import os
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from libs.common import asset_link, drama_ref, equipment_key, prop_key, scene_key
from libs.common.drama_layout import EQUIPMENT_DIR_NAME, is_equipment_tool_dir
from libs.common.episode_workflow import MODULE_NAV_LABELS, MODULES, PLACEHOLDER_STAGES, WORLD_FACTS_FILE, WORKFLOW_ID, WORKFLOW_MARKER
from libs.common.production_key import BACKGROUND_DIR_NAME, SCENES_DIR_NAME, first_shot_key, shot_key
from urllib.parse import urlencode
from libs.common.exposed_tree import ExposedTree, TREE_VISIBLE_EXTENSIONS
from libs.infrastructure.readers.scene_registry__reader import SceneRegistryReader

_IMAGE_EXTENSIONS: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"})
_VIDEO_EXTENSIONS: frozenset[str] = frozenset({".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"})
_AUDIO_EXTENSIONS: frozenset[str] = frozenset({".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"})
_PDF_EXTENSIONS: frozenset[str] = frozenset({".pdf"})
# White-model meshes (image-to-3D output / `tools/whitemodel_normalize.py` input).
# Their own node type so the sidebar marks them and the UI knows to preview them
# in <model-viewer> rather than treat them as an opaque download.
_MODEL_EXTENSIONS: frozenset[str] = frozenset({".glb", ".gltf"})
_CJK_RE = re.compile("[\u4e00-\u9fff]")
_DIGITS_RE = re.compile(r"(\d+)")


def _natural(name: str) -> list[str | int]:
    """Sort key that orders embedded numbers by value (p9 < p10, bg2 < bg10)."""
    return [int(t) if t.isdigit() else t for t in _DIGITS_RE.split(name.lower())]
# Chinese display labels for the shared system folders under `ai_videos/` (they
# carry no README H1 to derive a title from). Each of these is its own
# "library" main page in the UI.
_SYSTEM_FOLDER_LABELS_ZH: dict[str, str] = {
    "_research": "选题调研",
}
# A folder holding this file is marked obsolete (`"obsolete": true`, plus
# `"obsolete_note"` = the marker's path): content made with, or only serving, the
# removed 0–7 stage pipeline, kept for reference until it is redone with the
# six-module workflow (follow-up 233). A drama inherits the mark from its series
# folder — the only `ai_videos/` ancestor a drama root can have — and its own
# marker, if any, wins as the note.
OBSOLETE_MARKER_NAME: str = "OBSOLETE.md"
PROPS_DIR_NAME: str = "props"
# Asset trees whose keyed entries are labelled by their grammar alone
# (`p15 两层石木旅店`, `e12 蓝_维里甘之拳`); an unkeyed name — an equipment
# category / slot folder, `item.toml`, `registry.toml` — keeps its own.
_KEY_LABELS: dict[str, Callable[[str], str | None]] = {
    PROPS_DIR_NAME: prop_key.label,
    EQUIPMENT_DIR_NAME: equipment_key.label,
}
# The asset trees whose entries are labelled `{key} {rest}` (follow-ups 173 / 174).
_KEYED_TREES: frozenset[str] = frozenset({SCENES_DIR_NAME, BACKGROUND_DIR_NAME, *_KEY_LABELS})
# Tool-owned folders inside a scenes tree, labelled because their names say
# nothing to a reader (follow-up 173): a subject's script-built 3D scene, and a
# subject's per-block links into `props/`.
_SCENE_DIR_LABELS_ZH: dict[str, str] = {
    "_blender": "3D 场景",
    "assets": "本场景资产",
}
# A zone's layout input (`scenes/{大陆}/{区}/_plan/plan.toml` + apply report) is
# tool state, not an asset library — never shown (follow-up 174).
_HIDDEN_DIR_NAMES: frozenset[str] = frozenset({"_plan"})


def _obsolete_note(children: list[dict[str, Any]]) -> str | None:
    """Path of the folder's own `OBSOLETE.md` among its walked children, else None."""
    return next((c["path"] for c in children
                 if c["type"] == "file" and c["name"] == OBSOLETE_MARKER_NAME and not c.get("is_link")), None)


def _mark_obsolete(node: dict[str, Any], note: str | None) -> None:
    if note:
        node["obsolete"] = True
        node["obsolete_note"] = note


class TreeReader:
    """Walks the EXPOSED_TREE root and emits the recursive TreeNode shape.

    Single section: "AI Videos". (The Downloaded Novels / My Novel sections
    went with follow-up 233.)
    """

    def __init__(self, exposed: ExposedTree, scene_registry: SceneRegistryReader | None = None) -> None:
        self._exposed = exposed
        self._root = exposed.root
        self._root_prefix = str(self._root).rstrip(os.sep) + os.sep
        self._scene_registry = scene_registry or SceneRegistryReader()

    def build(self) -> dict[str, Any]:
        return {
            "type": "section",
            "name": "root",
            "path": "",
            "children": [self._ai_videos_section()],
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

    def _walk_project(self, project_dir: Path, series_note: str | None = None) -> dict[str, Any] | None:
        sub = self._walk_filtered(project_dir, self._is_allowed_leaf)
        node: dict[str, Any] = {
            "type": "directory",
            "name": project_dir.name,
            "path": self._rel(project_dir),
            "children": sub,
        }
        # Read before the six-module branch below narrows `children`.
        _mark_obsolete(node, _obsolete_note(sub) or series_note)
        # `is_drama` is the UI's only way to know where a drama root sits — a flat
        # drama is 2 segments, a series member 3. Nothing downstream may re-derive
        # that from path depth.
        if not project_dir.name.startswith("_"):
            node["is_drama"] = True
        marker = project_dir / WORKFLOW_MARKER
        if marker.is_file():
            config = json.loads(marker.read_text(encoding="utf-8"))
            if config.get("workflow") == WORKFLOW_ID:
                node["workflow"] = WORKFLOW_ID
                node["children"] = [child for child in sub if child["name"] in {"0_research", "2_世界观人设"}]
                for child in node["children"]:
                    child["display_name"] = "0_research" if child["name"] == "0_research" else "1_资产库"
                    child["lifetime"] = "persistent"
                    if child["name"] == "2_世界观人设":
                        for asset in child.get("children", []):
                            if asset["name"] == WORLD_FACTS_FILE:
                                asset["display_name"] = "世界规则"
                            elif asset["name"] == BACKGROUND_DIR_NAME:
                                asset["display_name"] = "background · 环境资产"
                episodes_root = project_dir / "episodes"
                episodes = sorted((p for p in episodes_root.iterdir() if p.is_dir() and not p.is_symlink()
                                   and re.fullmatch(r"ep\d+", p.name)), key=lambda p: _natural(p.name)) if episodes_root.is_dir() else []
                for module in MODULES:
                    outputs = []
                    for episode in episodes:
                        output = {"type": "workflow", "name": episode.name,
                                  "display_name": f"EP{int(episode.name[2:])}",
                                  "path": f"{node['path']}/episodes/{episode.name}/{module}.json",
                                  "drama_path": node["path"], "workflow_module": module,
                                  "workflow_episode": episode.name}
                        file = episode / f"{module}.json"
                        if file.is_file() and not file.is_symlink():
                            content = json.loads(file.read_text(encoding="utf-8"))["content"]
                            scenes = content.get("scenes", [])
                            if scenes:
                                output["type"] = "directory"
                                output["navigation_href"] = self._workflow_url(node["path"], episode.name, module)
                                output["children"] = self._workflow_scenes(node["path"], episode.name, module, scenes)
                        # Episode-level decision record (follow-up 225): why these scenes / sequences, which guideline.
                        decision = episode / "decisions" / f"{module}.md"
                        if decision.is_file() and not decision.is_symlink():
                            output["type"] = "directory"
                            output["navigation_href"] = self._workflow_url(node["path"], episode.name, module)
                            output["children"] = [{"type": "file", "name": decision.name, "display_name": "决策记录（本集）",
                                                   "path": self._rel(decision)}, *output.get("children", [])]
                        outputs.append(output)
                    node["children"].append({
                        "type": "directory", "name": module, "display_name": MODULE_NAV_LABELS[module],
                        "path": f"{node['path']}/stages/{module}",
                        "children": outputs,
                    })
                for stage in PLACEHOLDER_STAGES:
                    node["children"].append({
                        "type": "directory", "name": stage, "display_name": MODULE_NAV_LABELS[stage],
                        "path": f"{node['path']}/stages/{stage}",
                        "children": [{"type": "workflow", "name": episode.name, "display_name": f"EP{int(episode.name[2:])}",
                                      "path": f"{node['path']}/episodes/{episode.name}/{stage}",
                                      "drama_path": node["path"], "workflow_module": stage, "workflow_episode": episode.name}
                                     for episode in episodes],
                    })
        zh_title = _SYSTEM_FOLDER_LABELS_ZH.get(project_dir.name) or self._project_zh_title(project_dir)
        if zh_title:
            node["display_name"] = zh_title
        return node

    @staticmethod
    def _workflow_url(drama: str, episode: str, module: str, scene: str = "", shot: str = "") -> str:
        params = {"drama": drama, "episode": episode, "module": module}
        if scene:
            params["scene"] = scene
        if shot:
            params["shot"] = shot
        return "/drama?" + urlencode(params)

    def _workflow_scenes(self, drama: str, episode: str, module: str, scenes: list[dict]) -> list[dict]:
        nodes = []
        base = f"{drama}/episodes/{episode}"
        # Compiled scenes carry no location; name them after the filming scene they came from (follow-up 226).
        locations: dict[str, str] = {}
        filming = self._root / base / "filming.json"
        if module == "prompts" and filming.is_file() and not filming.is_symlink():
            try:
                locations = {item["id"]: item.get("location", "") for item in json.loads(filming.read_text(encoding="utf-8"))["content"]["scenes"]}
            except (ValueError, KeyError, TypeError):
                locations = {}
        for scene in scenes:
            path = f"{base}/{module}.json/scenes/{scene['id']}"
            children = []
            for shot in scene["shots"]:
                key = shot_key(episode, scene["id"], shot["id"]) if module == "filming" else first_shot_key(shot["id"])
                if key is None:
                    continue
                folder = key.folder(self._root / base)
                children.append({"type": "directory", "name": f"st{key.shot}", "display_name": key.value,
                                 "path": f"{path}/shots/st{key.shot}",
                                 "navigation_href": self._workflow_url(drama, episode, module, scene["id"], key.value),
                                 "children": self._walk_filtered(folder, self._is_allowed_leaf) if folder.is_dir() and not folder.is_symlink() else []})
            # Scene-level decision record (follow-up 225): purpose, coverage, why each shot, cited guidelines.
            decision = self._root / base / "scenes" / scene["id"] / "decisions.md"
            if module == "filming" and decision.is_file() and not decision.is_symlink():
                children.insert(0, {"type": "file", "name": decision.name, "display_name": "决策记录", "path": self._rel(decision)})
            nodes.append({"type": "directory", "name": scene["id"],
                          "display_name": f"{scene['id']} · {scene.get('location') or locations.get(scene['id']) or '场次'}", "path": path,
                          "navigation_href": self._workflow_url(drama, episode, module, scene["id"]), "children": children})
        return nodes

    def _walk_series(self, series_dir: Path) -> dict[str, Any] | None:
        """A series folder (`series.json`) renders as one collapsible node whose
        children are its member dramas, plus any `_`-prefixed shared folder
        (`_series/` — the series bible and cross-episode locked assets)."""
        members: list[dict[str, Any]] = []
        shared: list[dict[str, Any]] = []
        loose = self._walk_filtered(series_dir, self._is_allowed_leaf, dirs=False)
        note = _obsolete_note(loose)
        for entry in sorted(p for p in series_dir.iterdir() if p.is_dir()):
            if entry.name in self._exposed.excluded_dirs():
                continue
            node = self._walk_project(entry, series_note=note)
            if node is None:
                continue
            if entry.name.startswith("_"):
                node.pop("is_drama", None)
                if entry.name == drama_ref.SERIES_SHARED_DIR_NAME:
                    node["display_name"] = "系列共用"
                shared.append(node)
            else:
                members.append(node)
        series: dict[str, Any] = {
            "type": "series",
            "name": series_dir.name,
            "display_name": self._series_zh_title(series_dir),
            "path": self._rel(series_dir),
            "children": shared + members + loose,
        }
        _mark_obsolete(series, note)
        return series

    def _series_zh_title(self, series_dir: Path) -> str:
        try:
            data = json.loads((series_dir / drama_ref.SERIES_MARKER_NAME).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return series_dir.name
        name = data.get("name_zh")
        return name if isinstance(name, str) and name else series_dir.name

    def _project_zh_title(self, project_dir: Path) -> str | None:
        """Chinese display title for a drama folder (pinyin / English on disk):
        the first H1 of `ai_videos/{name}/README.md`, e.g. `# 《<title>》— …`."""
        return self._h1_zh(project_dir / "README.md")

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

        Anything under `scenes/` / `background/` — key-prefixed label, see
        `_scene_dir_label` (an unkeyed pinyin folder still reads its `{pinyin}.md`
        H1 `# zhenbei_wangfu_zhengting（镇北王府正厅）` → the `（中文）` group).
        A keyed folder under `props/` / `equipment/` likewise:
        `p15_两层石木旅店` → `p15 两层石木旅店`, `e12_蓝_维里甘之拳` → `e12 蓝_维里甘之拳`.
        None when no recognizable sidecar.
        """
        tree = self._keyed_tree(directory)
        if tree is not None:
            kind, tree_root, inner = tree
            label = (self._scene_dir_label(directory, tree_root) if kind in {SCENES_DIR_NAME, BACKGROUND_DIR_NAME}
                     else self._key_label(kind, directory.name, inner))
            if label:
                return label
        return None

    def _keyed_tree(self, p: Path) -> tuple[str, Path, tuple[str, ...]] | None:
        """(`scenes` | `props` | `equipment`, that folder, the folder names
        between it and `p`) for the nearest such folder above `p`, or None
        outside all of them."""
        parts = self._rel(p).split("/")[:-1]
        for i in range(len(parts) - 1, -1, -1):
            if parts[i] in _KEYED_TREES:
                if parts[i] == SCENES_DIR_NAME and "episodes" in parts[:i]:
                    continue
                return parts[i], self._root.joinpath(*parts[: i + 1]), tuple(parts[i + 1:])
        return None

    @staticmethod
    def _key_label(kind: str, name: str, inner: tuple[str, ...]) -> str | None:
        """`{key} {rest}` for a keyed name under `props/` / `equipment/`. An
        equipment item is found by its name at any depth (`equipment/板甲/胸/e79_…`
        or `equipment/主手/e12_…`), so nesting never matters — except that nothing
        inside a tool-owned folder (`loadouts/`, `_*`, `.*`) is an item, a card or
        a view."""
        if kind == EQUIPMENT_DIR_NAME and any(map(is_equipment_tool_dir, inner)):
            return None
        return _KEY_LABELS[kind](name)

    def _scene_dir_label(self, directory: Path, scenes_root: Path) -> str | None:
        """Every scenes-tree label opens with its routing key (follow-up 173).

        A keyed name is labelled from the name itself — `bg1-1 谷心_北望修道院` —
        never from its md's H1: a subject H1 reads `广场 · Seedance 主体` and a
        view H1 is a prompt title, so the name is the only label that is always
        right. An unkeyed folder (continent / zone / legacy pinyin scene) keeps
        its `{dir}.md` H1; a zone gets its zone-level subject's key in front.
        """
        name = directory.name
        fixed = _SCENE_DIR_LABELS_ZH.get(name)
        if fixed:
            return fixed
        keyed = scene_key.label(name)
        if keyed:
            return keyed
        h1 = self._h1_zh(directory / f"{name}.md")
        if h1 is None:
            return None
        zone = self._scene_registry.zone_key(scenes_root, directory)
        return scene_key.prefixed(zone, h1) if zone else h1

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
        # 数字按数值排：p9 在 p10 前、bg2 在 bg10 前（p1–p463 / bg1–bg804 按字面排会乱成 p1, p10, p100 …）
        scanned.sort(key=lambda row: (not row[2], _natural(row[1])))
        for entry, name, is_dir, is_file, is_symlink in scanned:
            if is_symlink:
                continue
            if name in excluded:
                continue
            if is_dir and (not dirs or name in _HIDDEN_DIR_NAMES):
                continue
            if is_dir:
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
                    _mark_obsolete(dir_node, _obsolete_note(sub))
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
        # Scenes / props / equipment leaves: a keyed file shows `{key} {rest}`
        # (`bg1-1 谷心.png`, `p15-1 正面.png`, `e12-1 正面.png`); in a scenes
        # tree an unkeyed folder's main sidecar `.md` mirrors its folder's
        # label. Only the label changes —
        # `name`/`path` stay as on disk, so import routing / download / open are
        # unaffected.
        tree = self._keyed_tree(f)
        if tree is not None:
            kind, tree_root, inner = tree
            if kind in {SCENES_DIR_NAME, BACKGROUND_DIR_NAME}:
                label = scene_key.label(f.name)
                if label is None and ext == ".md" and f.stem == f.parent.name:
                    label = self._scene_dir_label(f.parent, tree_root)
            else:
                label = self._key_label(kind, f.name, inner)
            if label:
                node["display_name"] = label
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
