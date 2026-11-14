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
from libs.common.production_key import BACKGROUND_DIR_NAME, GROUP_ID_RE, GROUPS_DIR_NAME, SCENES_DIR_NAME, first_shot_key, group_key, shot_key
from libs.common.scene_cut import CUT_FILE_PATTERN, CUT_STAGES, EDIT_DIR, EPISODE_CUT, POST_CUT, POST_DIR, POST_FILE_PATTERN
from urllib.parse import quote, urlencode
from libs.common.exposed_tree import ExposedTree, TREE_VISIBLE_EXTENSIONS
from libs.domain.errors.file__error import FileNotInSandboxError
from libs.domain.errors.media__error import NotUnderAiVideosError
from libs.infrastructure.readers.scene_registry__reader import SceneRegistryReader
from libs.infrastructure.readers.shared_library_tree__reader import SharedLibraryTreeReader

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
# Series-level new-drama development framework (xihuan follow-up 001); the UI route lives in lib/devPreview.ts.
DEV_FRAMEWORK_DIR = "framework"
DEV_DOCS_DIR = "0_开发"
DEV_PREVIEW_ROUTE = "/dev-preview"


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
# Lazy tree (follow-up 280): how many real folder levels the first load expands
# below each navigation node. Deeper folders arrive as `lazy` stubs (no
# children) and are fetched with `subtree()` when opened. A drama walks two
# levels so `2_世界观人设/{characters,background,…}` are listed; a shot folder one
# level so `planning/` `renders/` `资料包/` are listed.
LAZY_DRAMA_DEPTH: int = 2
LAZY_SHOT_DEPTH: int = 1

# 教学视频一节（follow-up 357）：系列 → 课程表的季 → 期。课程表格式见 edu_videos/ai_terms/课程表.md。
EDU_VIDEOS_DIR = "edu_videos"
EDU_SECTION_NAME = "教学视频"
EDU_SYLLABUS_FILE = "课程表.md"
EDU_SYLLABUS_NODE = "syllabus"   # 季与期是虚拟节点，路径挂在系列下这个名字里，不对应真实目录
EDU_TOPIC_DIR_RE = re.compile(r"(t\d+)_.+")
EDU_SEASON_RE = re.compile(r"^###\s*第\s*(\d+)\s*季\s*(.*)$")
EDU_ROW_RE = re.compile(r"^\|\s*(\d+-\d+)\s*\|\s*(t\d+)\s*(✅)?\s*\|\s*([^|]+?)\s*\|")
EDU_TOPIC_FILE_EXTENSIONS: frozenset[str] = frozenset({".md", ".json"})


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

    def build(self, lazy: bool = False) -> dict[str, Any]:
        """The whole tree, or with `lazy` only the navigation skeleton plus the
        first real folder levels (follow-up 280: the full walk is ~47k nodes /
        8.8 MB / 10 s and grew with every generated take)."""
        return {
            "type": "section",
            "name": "root",
            "path": "",
            "children": [self._ai_videos_section(lazy), *self._edu_videos_section()],
        }

    def subtree(self, rel_path: str, depth: int | None = 1) -> dict[str, Any]:
        """One real folder under `ai_videos/` for a lazy stub: its children,
        `depth` folder levels deep (None = everything below). Only `children`
        is meant to replace the stub's; the stub keeps its own labels."""
        rel = rel_path.strip().strip("/")
        parts = rel.split("/") if rel else []
        if not parts or parts[0] != "ai_videos" or any(part in {"", ".", ".."} for part in parts):
            raise NotUnderAiVideosError(rel_path)
        target = self._root.joinpath(*parts)
        if not target.is_dir() or target.is_symlink() or any(part in self._exposed.excluded_dirs() for part in parts):
            raise FileNotInSandboxError(rel_path)
        children = self._walk_filtered(target, self._is_allowed_leaf, depth=None if depth is None else depth - 1)
        if target.name == "2_世界观人设":
            self._label_world_assets(children)
        node: dict[str, Any] = {"type": "directory", "name": target.name, "path": self._rel(target), "children": children}
        _mark_obsolete(node, _obsolete_note(children))
        return node

    @staticmethod
    def _label_world_assets(children: list[dict[str, Any]]) -> None:
        for asset in children:
            if asset["name"] == WORLD_FACTS_FILE:
                asset["display_name"] = "世界规则"
            elif asset["name"] == BACKGROUND_DIR_NAME:
                asset["display_name"] = "background · 环境资产"

    def _ai_videos_section(self, lazy: bool = False) -> dict[str, Any]:
        ai_videos_root = self._root / "ai_videos"
        children: list[dict[str, Any]] = []
        deleted_child: dict[str, Any] | None = None
        if ai_videos_root.is_dir():
            for project_dir in sorted(p for p in ai_videos_root.iterdir() if p.is_dir()):
                if project_dir.name in self._exposed.excluded_dirs():
                    continue
                if drama_ref.is_series_dir(project_dir):
                    series_node = self._walk_series(project_dir, lazy)
                    if series_node is not None:
                        children.append(series_node)
                    continue
                project_node = self._walk_project(project_dir, lazy=lazy)
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

    def _edu_videos_section(self) -> list[dict[str, Any]]:
        """教学视频（follow-up 357）：`edu_videos/` 每个系列一个节点。

        系列有 `课程表.md` 时按它列「第 N 季 → 季-集 词」：有知识点目录的期点开单集预览、
        展开看讲稿等文件；还没目录的期只显示「规划」。没有课程表的系列直接列知识点目录。
        只读、不懒加载（每个系列只有几十个节点）。没有 `edu_videos/` 时不出这一节。
        """
        edu_root = self._root / EDU_VIDEOS_DIR
        if not edu_root.is_dir() or edu_root.is_symlink():
            return []
        series_nodes = []
        for series_dir in sorted(p for p in edu_root.iterdir() if p.is_dir() and not p.is_symlink()):
            if series_dir.name.startswith(("_", ".")) or series_dir.name in self._exposed.excluded_dirs():
                continue
            series_nodes.append(self._edu_series(series_dir))
        return [{"type": "section", "name": EDU_SECTION_NAME, "path": EDU_VIDEOS_DIR, "children": series_nodes}]

    def _edu_series(self, series_dir: Path) -> dict[str, Any]:
        rel = self._rel(series_dir)
        topics = {m.group(1): d for d in series_dir.iterdir()
                  if d.is_dir() and not d.is_symlink() and (m := EDU_TOPIC_DIR_RE.fullmatch(d.name))}
        readme, syllabus = series_dir / "README.md", series_dir / EDU_SYLLABUS_FILE
        title = self._edu_title(readme) or series_dir.name
        children: list[dict[str, Any]] = []
        node: dict[str, Any] = {"type": "directory", "name": series_dir.name, "display_name": title,
                                "path": rel, "children": children}
        if syllabus.is_file() and not syllabus.is_symlink():
            node["navigation_href"] = "/file/" + quote(self._rel(syllabus), safe="")
            children.append({"type": "file", "name": syllabus.name, "display_name": "课程表", "path": self._rel(syllabus)})
        if readme.is_file() and not readme.is_symlink():
            children.append({"type": "file", "name": readme.name, "display_name": "系列说明", "path": self._rel(readme)})
        seasons = self._edu_seasons(syllabus) if syllabus.is_file() and not syllabus.is_symlink() else []
        listed: set[str] = set()
        for number, season_title, rows in seasons:
            episodes = []
            for code, topic_id, word in rows:
                listed.add(topic_id)
                episodes.append(self._edu_episode(f"{rel}/{EDU_SYLLABUS_NODE}/{code}", f"{code} {word}", topics.get(topic_id),
                                                   syllabus_href=node["navigation_href"] + "?" + urlencode({"ep": code})))
            children.append({"type": "directory", "name": f"s{number}", "display_name": season_title,
                             "path": f"{rel}/{EDU_SYLLABUS_NODE}/s{number}", "children": episodes})
        rest = sorted((t for t in topics if t not in listed), key=_natural)
        if rest and seasons:
            children.append({"type": "directory", "name": "_unlisted", "display_name": "未排进课程表",
                             "path": f"{rel}/{EDU_SYLLABUS_NODE}/_unlisted",
                             "children": [self._edu_episode(self._rel(topics[t]), topics[t].name, topics[t]) for t in rest]})
        elif rest:
            children.extend(self._edu_episode(self._rel(topics[t]), topics[t].name, topics[t]) for t in rest)
        return node

    @staticmethod
    def _edu_title(readme: Path) -> str | None:
        if not readme.is_file() or readme.is_symlink():
            return None
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return re.sub(r"[（(][^）)]*[）)]\s*$", "", line[2:]).strip() or None
        return None

    @staticmethod
    def _edu_seasons(syllabus: Path) -> list[tuple[str, str, list[tuple[str, str, str]]]]:
        """`### 第 N 季 · 名（M 期）` 起一季，其下 `| 季-集 | tNN ✅ | 词 | …` 每行一期。"""
        seasons: list[tuple[str, str, list[tuple[str, str, str]]]] = []
        for line in syllabus.read_text(encoding="utf-8").splitlines():
            if (m := EDU_SEASON_RE.match(line)):
                seasons.append((m.group(1), f"第 {m.group(1)} 季 {m.group(2).strip()}".strip(), []))
            elif seasons and (m := EDU_ROW_RE.match(line)):
                seasons[-1][2].append((m.group(1), m.group(2), m.group(4).strip()))
        return seasons

    def _edu_episode(self, path: str, label: str, topic: Path | None, syllabus_href: str | None = None) -> dict[str, Any]:
        if topic is None:   # 还没目录：点开课程表（带 ?ep= 只为高亮这一行，阅读页不看它）
            node = {"type": "directory", "name": label, "display_name": f"{label} · 规划", "path": path, "children": []}
            if syllabus_href:
                node["navigation_href"] = syllabus_href
            return node
        files = [self._leaf_for(f) for f in sorted(topic.iterdir(), key=lambda f: _natural(f.name))
                 if f.is_file() and not f.is_symlink() and f.suffix.lower() in EDU_TOPIC_FILE_EXTENSIONS]
        done = any((topic / "final").glob("*.mp4")) if (topic / "final").is_dir() else False
        node: dict[str, Any] = {"type": "directory", "name": topic.name,
                                "display_name": label + (" ✅" if done else " · 制作中"),
                                "path": path, "children": files}
        if (topic / "preview.json").is_file():
            node["navigation_href"] = "/episode-preview?" + urlencode({"path": self._rel(topic)})
        return node

    def _walk_project(self, project_dir: Path, series_note: str | None = None, lazy: bool = False) -> dict[str, Any] | None:
        sub = self._walk_filtered(project_dir, self._is_allowed_leaf, depth=LAZY_DRAMA_DEPTH if lazy else None)
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
                        self._label_world_assets(child.get("children", []))
                        # 点名字开资产总览，点箭头照常展开（follow-up 294）
                        child["navigation_href"] = "/assets?" + urlencode({"drama": node["path"]})
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
                                output["children"] = self._workflow_scenes(node["path"], episode.name, module, scenes, lazy)
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
                    stage_outputs = []
                    for episode in episodes:
                        output = {"type": "workflow", "name": episode.name, "display_name": f"EP{int(episode.name[2:])}",
                                  "path": f"{node['path']}/episodes/{episode.name}/{stage}",
                                  "drama_path": node["path"], "workflow_module": stage, "workflow_episode": episode.name}
                        cut_scenes = self._edit_scenes(node["path"], episode) if stage == "edit" else []
                        if cut_scenes:   # 剪辑（follow-up 269）：列出已有剪辑的场次，每场分草稿剪辑 / 正片剪辑
                            output.update(type="directory", navigation_href=self._workflow_url(node["path"], episode.name, stage),
                                          children=cut_scenes)
                        stage_outputs.append(output)
                    node["children"].append({
                        "type": "directory", "name": stage, "display_name": MODULE_NAV_LABELS[stage],
                        "path": f"{node['path']}/stages/{stage}",
                        "children": stage_outputs,
                    })
            for key, title, route in [("base_layout", "基地布局", "/base-layout"), ("map_regions", "地图资产", "/map-regions")]:
                layout = config.get(key)
                if isinstance(layout, str) and layout.endswith(".json") and "\\" not in layout and ":" not in layout:
                    parts = layout.split("/")
                    if all(part not in {"", ".", ".."} for part in parts):
                        target = project_dir.joinpath(*parts)
                        if target.is_file() and not any(p.is_symlink() for p in [target, *target.parents]):
                            node["children"].insert(2, {
                                "type": "file", "name": key, "display_name": title,
                                "path": f"{node['path']}/stages/{key}", "navigation_href": route + "?" + urlencode({"path": self._rel(target)}),
                            })
        zh_title = _SYSTEM_FOLDER_LABELS_ZH.get(project_dir.name) or self._project_zh_title(project_dir)
        if zh_title:
            node["display_name"] = zh_title
        return node

    @staticmethod
    def _workflow_url(drama: str, episode: str, module: str, scene: str = "", shot: str = "", cut: str = "") -> str:
        params = {"drama": drama, "episode": episode, "module": module}
        if scene:
            params["scene"] = scene
        if shot:
            params["shot"] = shot
        if cut:
            params["cut"] = cut
        return "/drama?" + urlencode(params)

    def _edit_scenes(self, drama: str, episode: Path) -> list[dict]:
        """剪辑导航（follow-up 269）：有剪辑决定的场次，按分镜顺序；每场下面是草稿剪辑 / 正片剪辑（最新版本号）。"""
        located: dict[str, str] = {}
        filming = episode / "filming.json"
        if filming.is_file() and not filming.is_symlink():
            try:
                located = {str(item["id"]): str(item.get("location", "")) for item in json.loads(filming.read_text(encoding="utf-8"))["content"]["scenes"]}
            except (ValueError, KeyError, TypeError, AttributeError):
                located = {}
        order = list(located)
        scenes_root = episode / "scenes"
        found = [p.name for p in scenes_root.iterdir() if p.is_dir() and not p.is_symlink()] if scenes_root.is_dir() else []
        nodes = []
        whole = []   # 集级剪辑（follow-up 278）：`{集}/edit/{阶段}/cut_v{N}.json` 把各场接起来，导航里排在各场前面
        for stage in CUT_STAGES:
            folder = episode / EDIT_DIR / stage
            versions = [int(m.group(1)) for f in folder.iterdir() if (m := re.fullmatch(CUT_FILE_PATTERN, f.name)) and f.is_file()]                 if folder.is_dir() and not folder.is_symlink() else []
            if versions:
                whole.append({"type": "directory", "name": stage,
                              "display_name": f"{'草稿剪辑' if stage == 'draft' else '正片剪辑'} · v{max(versions)}",
                              "path": f"{drama}/episodes/{episode.name}/edit/episode/{stage}",
                              "navigation_href": self._workflow_url(drama, episode.name, "edit", EPISODE_CUT, cut=stage), "children": []})
        if whole:
            nodes.append({"type": "directory", "name": EPISODE_CUT, "display_name": "整集（场与场接起来、转场）",
                          "path": f"{drama}/episodes/{episode.name}/edit/episode",
                          "navigation_href": self._workflow_url(drama, episode.name, "edit", EPISODE_CUT), "children": whole})
        post = episode / POST_DIR   # 后期试做（follow-up 290）：排在整集后面
        posts = [int(m.group(1)) for f in post.iterdir() if (m := re.fullmatch(POST_FILE_PATTERN, f.name)) and f.is_file()]             if post.is_dir() and not post.is_symlink() else []
        if posts:
            nodes.append({"type": "directory", "name": POST_CUT, "display_name": f"后期试做（声音、字幕、字卡） · v{max(posts)}",
                          "path": f"{drama}/episodes/{episode.name}/edit/post",
                          "navigation_href": self._workflow_url(drama, episode.name, "edit", POST_CUT), "children": []})
        for sid in sorted(found, key=lambda s: (order.index(s) if s in order else len(order), _natural(s))):
            stages = []
            for stage in CUT_STAGES:
                folder = scenes_root / sid / EDIT_DIR / stage
                versions = [int(m.group(1)) for f in folder.iterdir() if (m := re.fullmatch(CUT_FILE_PATTERN, f.name)) and f.is_file()] \
                    if folder.is_dir() and not folder.is_symlink() else []
                if versions:
                    stages.append({"type": "directory", "name": stage,
                                   "display_name": f"{'草稿剪辑' if stage == 'draft' else '正片剪辑'} · v{max(versions)}",
                                   "path": f"{drama}/episodes/{episode.name}/edit/scenes/{sid}/{stage}",
                                   "navigation_href": self._workflow_url(drama, episode.name, "edit", sid, cut=stage), "children": []})
            if stages:
                nodes.append({"type": "directory", "name": sid, "display_name": f"{sid} · {located.get(sid) or '场次'}",
                              "path": f"{drama}/episodes/{episode.name}/edit/scenes/{sid}",
                              "navigation_href": self._workflow_url(drama, episode.name, "edit", sid), "children": stages})
        return nodes

    def _workflow_scenes(self, drama: str, episode: str, module: str, scenes: list[dict], lazy: bool = False) -> list[dict]:
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
        filming_durations: dict[str, dict[str, int]] = {}
        if module == "prompts" and filming.is_file() and not filming.is_symlink():
            try:
                filming_durations = {item["id"]: {s["id"]: s["duration"] for s in item["shots"] if isinstance(s.get("duration"), int)}
                                     for item in json.loads(filming.read_text(encoding="utf-8"))["content"]["scenes"]}
            except (ValueError, KeyError, TypeError):
                filming_durations = {}
        for scene in scenes:
            path = f"{base}/{module}.json/scenes/{scene['id']}"
            shot_nodes: dict[str, dict] = {}
            durations: dict[str, int] = {}
            for shot in scene["shots"]:
                key = shot_key(episode, scene["id"], shot["id"]) if module == "filming" else first_shot_key(shot["id"])
                if key is None:
                    continue
                folder = key.folder(self._root / base)
                durations[f"st{key.shot}"] = shot.get("duration") if isinstance(shot.get("duration"), int) else 0
                shot_nodes[f"st{key.shot}"] = {"type": "directory", "name": f"st{key.shot}", "display_name": key.value,
                                               "path": f"{path}/shots/st{key.shot}",
                                               "navigation_href": self._workflow_url(drama, episode, module, scene["id"], key.value),
                                               "children": self._walk_filtered(folder, self._is_allowed_leaf, depth=LAZY_SHOT_DEPTH if lazy else None)
                                               if folder.is_dir() and not folder.is_symlink() else []}
            if module == "prompts":     # compiled shots carry no duration; take it from filming
                durations.update(filming_durations.get(scene["id"], {}))
            # 场 → 镜组 → 镜头 (follow-up 331): every shot sits under a group; a shot not listed in `groups` is a one-shot
            # group of its own. A written group opens its preview page; its board, pack and takes live there, not in the nav.
            grouped: dict[str, tuple[str, list[str]]] = {}
            for group in scene.get("groups", []):
                gid = group["id"].rsplit("_", 1)[-1]
                members = [m.rsplit("_", 1)[-1] for m in group.get("shots", [])]
                if GROUP_ID_RE.fullmatch(gid) and members:
                    for member in members:
                        grouped[member] = (gid, members)
            children = []
            done: set[str] = set()
            for sid, shot_node in shot_nodes.items():
                if sid in done:
                    continue
                if sid not in grouped:
                    done.add(sid)
                    children.append({"type": "directory", "name": sid,
                                     "display_name": f"单镜 {sid}" + (f" · {durations[sid]} 秒" if durations.get(sid) else ""),
                                     "path": f"{path}/groups/{sid}", "navigation_href": shot_node["navigation_href"],
                                     "children": [shot_node]})
                    continue
                gid, members = grouped[sid]
                done.update(members)
                folder = self._root / base / SCENES_DIR_NAME / scene["id"] / GROUPS_DIR_NAME / gid
                total = sum(durations.get(m, 0) for m in members)
                children.append({"type": "directory", "name": gid,
                                 "display_name": f"镜组 {group_key(episode, scene['id'], gid)} · {members[0]}–{members[-1]}"
                                 + (f" · {total} 秒" if total else ""),
                                 "path": f"{path}/groups/{gid}",
                                 "navigation_href": "/group-preview?" + urlencode({"path": self._rel(folder)}),
                                 "children": [shot_nodes[m] for m in members if m in shot_nodes]})
            # 场故事板 (follow-up 336): the scene's panels left to right, for review; first under the scene.
            board = self._root / base / SCENES_DIR_NAME / scene["id"] / "board" / "scene_board.json"
            if board.is_file() and not board.is_symlink():
                children.insert(0, {"type": "directory", "name": "board", "display_name": "场故事板",
                                    "path": f"{path}/board",
                                    "navigation_href": "/scene-preview?" + urlencode({"path": self._rel(board.parent.parent)}),
                                    "children": []})
            # Scene-level decision record (follow-up 225): purpose, coverage, why each shot, cited guidelines.
            decision = self._root / base / "scenes" / scene["id"] / "decisions.md"
            if module == "filming" and decision.is_file() and not decision.is_symlink():
                children.insert(0, {"type": "file", "name": decision.name, "display_name": "决策记录", "path": self._rel(decision)})
            nodes.append({"type": "directory", "name": scene["id"],
                          "display_name": f"{scene['id']} · {scene.get('location') or locations.get(scene['id']) or '场次'}", "path": path,
                          "navigation_href": self._workflow_url(drama, episode, module, scene["id"]), "children": children})
        return nodes

    def _walk_series(self, series_dir: Path, lazy: bool = False) -> dict[str, Any] | None:
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
            if entry.name == DEV_FRAMEWORK_DIR and (entry / "README.md").is_file() and (entry / "templates").is_dir():
                shared.append(self._dev_framework_node(entry))
                continue
            node = self._walk_project(entry, series_note=note, lazy=lazy)
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
        library = self._series_library(series_dir, lazy)
        if library is not None:
            series["navigation_href"] = library["navigation_href"]
            series["children"].insert(0, library)
        _mark_obsolete(series, note)
        return series

    def _dev_framework_node(self, framework: Path) -> dict[str, Any]:
        """Series-level new-drama development framework (xihuan follow-up 001): the framework page
        plus one entry per dev-doc folder (worked examples, and each member drama's `0_开发`)."""
        folders = sorted(p for p in (framework / "examples").glob("*") if (p / "01_主题.md").is_file())
        folders += sorted(p / DEV_DOCS_DIR for p in framework.parent.iterdir()
                          if p.is_dir() and (p / DEV_DOCS_DIR / "01_主题.md").is_file())
        children = [{"type": "directory", "name": f.name if f.name != DEV_DOCS_DIR else f.parent.name,
                     "display_name": (f"试套 · {self._h1_zh(f / '01_主题.md') or f.name}" if f.parent.name == "examples"
                                      else f"开发稿 · {self._project_zh_title(f.parent) or f.parent.name}"),
                     "path": self._rel(f), "navigation_href": DEV_PREVIEW_ROUTE + "?" + urlencode({"path": self._rel(f)}),
                     "children": []} for f in folders]
        return {"type": "directory", "name": framework.name, "display_name": "新剧开发框架", "path": self._rel(framework),
                "navigation_href": DEV_PREVIEW_ROUTE + "?" + urlencode({"path": self._rel(framework)}), "children": children}

    def _series_library(self, series_dir: Path, lazy: bool) -> dict[str, Any] | None:
        try:
            config = json.loads((series_dir / drama_ref.SERIES_MARKER_NAME).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        rel = config.get("shared_library")
        if not isinstance(rel, str) or not self._exposed.is_inside(rel):
            return None
        library = self._root / rel
        if library.is_symlink() or not (library / "library.json").is_file():
            return None
        return {"type": "directory", "name": "shared_library", "display_name": "公用资产",
                "path": self._rel(library), "navigation_href": "/assets?" + urlencode({"library": self._rel(library)}),
                "children": SharedLibraryTreeReader().read(library, self._rel(library))}

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
        self, directory: Path, leaf_predicate: Any, dirs: bool = True, depth: int | None = None
    ) -> list[dict[str, Any]]:
        """`dirs=False` emits only the directory's own files — used for a series
        folder, whose sub-directories are walked as drama nodes instead.

        `depth` (follow-up 280) is how many sub-folder levels to expand; a folder
        past it becomes a `lazy` stub — listed only when something visible lies
        inside, labelled as usual, with no children. None walks everything."""
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
            if is_dir and depth is not None and depth <= 0:
                if self._has_visible(entry, leaf_predicate):
                    stub: dict[str, Any] = {"type": "directory", "name": name, "path": self._rel(entry),
                                            "children": [], "lazy": True}
                    zh_label = self._sidecar_zh_label(entry)
                    if zh_label:
                        stub["display_name"] = zh_label
                    marker = entry / OBSOLETE_MARKER_NAME
                    if marker.is_file() and not marker.is_symlink():
                        _mark_obsolete(stub, self._rel(marker))
                    children.append(stub)
            elif is_dir:
                sub = self._walk_filtered(entry, leaf_predicate, depth=None if depth is None else depth - 1)
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

    def _has_visible(self, directory: Path, leaf_predicate: Any) -> bool:
        """Whether a full walk would list this folder: something visible lies
        somewhere inside (same skips as `_walk_filtered`). Stops at the first hit."""
        excluded = self._exposed.excluded_dirs()
        try:
            with os.scandir(directory) as it:
                entries = list(it)
        except OSError:
            return False
        later: list[Path] = []
        for e in entries:
            if e.is_symlink() or e.name in excluded:
                continue
            if e.is_dir(follow_symlinks=False):
                if e.name not in _HIDDEN_DIR_NAMES:
                    later.append(Path(e.path))
            elif e.is_file(follow_symlinks=False):
                entry = Path(e.path)
                if (asset_link.is_link_file(entry) and self._link_leaf(entry) is not None) or leaf_predicate(entry):
                    return True
        return any(self._has_visible(sub, leaf_predicate) for sub in later)

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
