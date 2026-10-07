from __future__ import annotations

import json
import os
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from libs.common import asset_link, drama_ref, equipment_key, prop_key, scene_key
from libs.common.drama_layout import EQUIPMENT_DIR_NAME, is_equipment_tool_dir
from libs.common.episode_workflow import MODULE_NAV_LABELS, MODULES, WORLD_FACTS_FILE, WORKFLOW_ID, WORKFLOW_MARKER
from libs.common.production_key import BACKGROUND_DIR_NAME, SCENES_DIR_NAME, first_shot_key, shot_key
from urllib.parse import urlencode
from libs.common.exposed_tree import ExposedTree, TREE_VISIBLE_EXTENSIONS
from libs.common.story_runs import STORY_INPUT_FILE, STORY_INPUT_NODE_TYPE, STORY_RUNS_FILE, STORY_RUNS_NODE_TYPE, STORY_RUN_VIEWS, STORY_RUN_DOCUMENT_FILES
from libs.common.sub_type_lookup import lookup as sub_type_lookup
from libs.domain.value_objects.novel__valueobject import CANONICAL_NOVELS, categories as novel_categories
from libs.infrastructure.readers.scene_registry__reader import SceneRegistryReader
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader
from libs.infrastructure.readers.story_selection__reader import StorySelectionReader

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
_DIGITS_RE = re.compile(r"(\d+)")


def _natural(name: str) -> list[str | int]:
    """Sort key that orders embedded numbers by value (p9 < p10, bg2 < bg10)."""
    return [int(t) if t.isdigit() else t for t in _DIGITS_RE.split(name.lower())]
# Chinese display labels for the shared system folders under `ai_videos/` (they
# carry no README/concept H1 to derive a title from). Each of these is its own
# "library" main page in the UI.
_SYSTEM_FOLDER_LABELS_ZH: dict[str, str] = {
    "_actors": "演员库",
    "_research": "选题调研",
}
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


class TreeReader:
    """Walks the EXPOSED_TREE root and emits the recursive TreeNode shape.

    Single section: "AI Videos".
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
                        if module == "story":
                            output["display_name"] = "故事正文"
                            output["lifetime"] = "workspace"
                            episode_path = f"{node['path']}/episodes/{episode.name}"
                            children = []
                            shared_input = episode / STORY_INPUT_FILE
                            if shared_input.is_file() and not shared_input.is_symlink():
                                inputs = [{"type": STORY_INPUT_NODE_TYPE, "name": view,
                                           "display_name": label, "path": f"{episode_path}/{file}",
                                           "episode_path": episode_path, "story_input_view": view,
                                           "lifetime": "persistent"}
                                          for view, label, file in (("input", "创作输入", STORY_INPUT_FILE),
                                                                    ("rules", "创作规则", "shared/rules-view.json"))]
                                children.append({"type": "directory", "name": "shared", "display_name": "共享配置 · Persistent",
                                                 "path": f"{episode_path}/shared", "lifetime": "persistent", "children": inputs})
                            runs = episode / STORY_RUNS_FILE
                            run_tree = None
                            if runs.is_file() and not runs.is_symlink():
                                run_tree = self._story_runs_node(episode_path)
                            children.append(self._story_current_link(episode_path, int(episode.name[2:]), run_tree))
                            if run_tree is not None:
                                children.append(run_tree)
                            outputs.append({"type": "directory", "name": episode.name,
                                            "display_name": f"EP{int(episode.name[2:])}",
                                            "path": f"{node['path']}/stages/{module}/{episode.name}", "children": children})
                        else:
                            file = episode / f"{module}.json"
                            if file.is_file() and not file.is_symlink():
                                content = json.loads(file.read_text(encoding="utf-8"))["content"]
                                scenes = content.get("scenes", [])
                                if scenes:
                                    output["type"] = "directory"
                                    output["navigation_href"] = self._workflow_url(node["path"], episode.name, module)
                                    output["children"] = self._workflow_scenes(node["path"], episode.name, module, scenes)
                            outputs.append(output)
                    node["children"].append({
                        "type": "directory", "name": module, "display_name": MODULE_NAV_LABELS[module],
                        "path": f"{node['path']}/stages/{module}",
                        "children": outputs,
                    })
        zh_title = _SYSTEM_FOLDER_LABELS_ZH.get(project_dir.name) or self._project_zh_title(project_dir)
        if zh_title:
            node["display_name"] = zh_title
        return node

    def _story_current_link(self, episode_path: str, number: int, runs: dict[str, Any] | None) -> dict[str, Any]:
        node: dict[str, Any] = {"type": "directory", "name": "current", "display_name": f"当前 EP{number} · 未选用",
                                "path": f"{episode_path}/current", "children": []}
        selection = StorySelectionReader(self._root).read(episode_path)
        if selection is None or runs is None:
            return node
        target = next((run for run in runs["children"] if run["story_run_id"] == selection["run_id"]), None)
        if target is None or target.get("story_run_status") == "unavailable":
            node["display_name"] = f"当前 EP{number} · 目标不可用"
            return node
        node.pop("children")
        node.update(type=STORY_RUNS_NODE_TYPE, display_name=f"当前 EP{number} → {target['display_name']}",
                    is_link=True, link_note="指向当前选用的 run，文档统一保存在 runs 下",
                    episode_path=episode_path, story_run_id=selection["run_id"], story_run_view="output",
                    story_run_source=f"{target['audit_folder']}/{STORY_RUN_DOCUMENT_FILES['output']}")
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
            nodes.append({"type": "directory", "name": scene["id"],
                          "display_name": f"{scene['id']} · {scene.get('location', '场次')}", "path": path,
                          "navigation_href": self._workflow_url(drama, episode, module, scene["id"]), "children": children})
        return nodes

    def _story_runs_node(self, episode_path: str) -> dict[str, Any]:
        reader = StoryRunsReader(self._root)
        _, entries = reader.index(episode_path)
        runs = []
        for index, entry in enumerate(entries, 1):
            run_id = entry["run_id"]
            path = f"{episode_path}/runs/{run_id}"
            documents = [{"type": STORY_RUNS_NODE_TYPE, "name": view, "display_name": label,
                          "path": f"{path}/{view}.json", "episode_path": episode_path,
                          "story_run_id": run_id, "story_run_view": view,
                          "lifetime": "transient",
                          "story_run_source": f"{entry['audit_path'].rsplit('/', 1)[0]}/{STORY_RUN_DOCUMENT_FILES[view]}"}
                         for view, label in STORY_RUN_VIEWS.items()]
            run_node = {"type": "directory", "name": run_id, "display_name": f"run{index}",
                        "path": path, "episode_path": episode_path, "story_run_id": run_id,
                        "lifetime": "transient", "audit_folder": entry["audit_path"].rsplit("/", 1)[0],
                        "children": [{"type": "directory", "name": "inputs", "display_name": "输入与规则",
                                      "path": f"{path}/inputs", "lifetime": "transient", "children": [documents[2]]},
                                     {"type": "directory", "name": "outputs", "display_name": "产出",
                                      "path": f"{path}/outputs", "lifetime": "transient", "children": documents[:2]},
                                     {"type": "directory", "name": "process_documents", "display_name": "过程",
                                      "path": f"{path}/process_documents", "lifetime": "transient", "children": [documents[3]]}]}
            try:
                run = reader.detail(episode_path, run_id)
                run_node["story_run_title"] = run["candidate"].get("title") or run["candidate"]["brief"]
                run_node["story_run_status"] = run["status"]
                io = reader.describe(run)
                links: dict[str, list[dict[str, Any]]] = {}
                for item in io["items"]:
                    links.setdefault(item["group"], []).append({
                        "type": STORY_RUNS_NODE_TYPE, "name": item["id"], "display_name": item["name"],
                        "path": f"{path}/links/{item['id']}.json", "episode_path": episode_path,
                        "story_run_id": run_id, "story_run_view": "item", "story_run_item_id": item["id"],
                        "story_run_source": item["target"], "is_link": True, "lifetime": "transient",
                        "link_note": "关联本次运行记录的实际版本"})
                input_groups = [{"type": "directory", "name": group, "display_name": label,
                                 "path": f"{path}/inputs/{group}", "children": links.get(group, [])}
                                for group, label in (("settings", "故事设定"), ("sources", "背景与事实来源"),
                                                     ("rules", "流程规则"), ("tasks", "实际任务指令"), ("runtime", "运行与模型设置"))]
                run_node["children"] = [
                    {"type": "directory", "name": "inputs", "display_name": "输入与规则",
                     "path": f"{path}/inputs", "lifetime": "transient", "children": [documents[2], *input_groups]},
                    {"type": "directory", "name": "outputs", "display_name": "产出",
                     "path": f"{path}/outputs", "lifetime": "transient", "children": [*documents[:2], *links.get("outputs", [])]},
                    {"type": "directory", "name": "process_documents", "display_name": "过程",
                     "path": f"{path}/process_documents", "lifetime": "transient", "children": [documents[3], *links.get("process", [])]}]
            except (ValueError, FileNotFoundError, OSError):
                run_node["story_run_status"] = "unavailable"
            runs.append(run_node)
        return {"type": "directory", "name": "runs", "display_name": "runs · Transient",
                "path": f"{episode_path}/runs", "lifetime": "transient", "children": runs}

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
        2) Anything under `scenes/` — key-prefixed label, see `_scene_dir_label`
           (an unkeyed pinyin folder still reads its `{pinyin}.md` H1
           `# zhenbei_wangfu_zhengting（镇北王府正厅）` → the `（中文）` group).
           A keyed folder under `props/` / `equipment/` likewise:
           `p15_两层石木旅店` → `p15 两层石木旅店`, `e12_蓝_维里甘之拳` → `e12 蓝_维里甘之拳`.
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
