"""Resolve each shot's prompt references from the drama's files (follow-up 227).

Same lookup rules as `tools/episode_shots.py` (the production tools that draw overheads and previz):
- cast key `c1-1` → costume stage three-view sheet `characters/[{group}/]c1_*/c1-1_*/c1-1_views.png`; `c14` →
  `characters/c14_*/views/c14_*_views.png` (follow-up 228: the user requires three-view sheets for identity consistency).
- name: first Chinese segment of the character card's H1 (`Aaron · 亚伦 · …` → 亚伦), overridable in workflow.json `names`.
- voice: `views/{card}_audio.mp3` when the card has one (follow-up 228); a local who never speaks or speaks one line has none (chuanyue_yiri follow-up 036, bible §2.1).
  `speaks` (a dialogue line's speaker matches the name) decides whether the compiler attaches it (v13).
- appearance: the card's `## Shot prompt 外观` text block; scene description: the background card's `## Shot prompt 场景` block.
- figure colour: workflow.json `figure_colors` (card number → colour name), shared with overhead dots and previz figures.
- scene image: `background/**/bgN_*/bgN_*.png`.
  A shot may name its own view with `background` (follow-up 261); its image and 场景 block replace the scene's for that shot.
- props (follow-up 231): shot `props: ["p475"]` → `props/p475_*/p475_*.png` (the anchor image; the front view
  `p475-1_正面.png` when a prop has only views), name from the card's H1, description from its `## Shot prompt 外观` block.
- motion: `planning/previz.json` (written by tools/shot_overhead.py) decides; complex shots use `previz/{stN}_previz.mp4`,
  the rest use `planning/{stN}_overhead_ref.png`. Every shot must have an overhead.
- first frame (follow-up 276): `planning/{stN}_first_frame.png` when present — an approved opening still.
"""
from __future__ import annotations

import dataclasses
import json
import re
import tomllib
from pathlib import Path
from typing import Any

from libs.common import prop_key
from libs.common.asset_group import character_dirs, grouped_dirs, character_weapon_keys
from libs.common.drama_ref import split_drama_rel
from libs.common.episode_workflow import GROUP_BOARD_FILE
from libs.common.production_key import GROUPS_DIR_NAME, SCENES_DIR_NAME, group_key, shot_key
from libs.domain.value_objects.shot_materials__valueobject import CastMember, PromptSettings, PropItem, ShotMaterials

SETTINGS_DIR = "2_世界观人设"
KEY_RE = re.compile(r"([cm])(\d+)(?:-(\d+))?\Z")
FALLBACK_COLORS = ("蓝", "黄", "红", "橙", "紫", "青", "粉", "白", "褐")
KNOWN_COLORS = {*FALLBACK_COLORS, "绿", "灰"}
LOOK_SECTION = "Shot prompt 外观"
SCENE_SECTION = "Shot prompt 场景"


class ShotMaterialsReader:
    def __init__(self, repo_root: Path) -> None:
        self.root = repo_root

    def read(self, episode_path: str, filming: dict[str, Any]) -> tuple[PromptSettings, dict[str, ShotMaterials]]:
        split = split_drama_rel(self.root, episode_path)
        if not split:
            raise FileNotFoundError("找不到剧集")
        drama = self.root / split[0]
        episode = self.root / episode_path
        config = self._settings(drama)
        prompt = config.get("prompt", {}) if isinstance(config.get("prompt"), dict) else {}
        settings = PromptSettings(style=str(prompt.get("style", "")), ratio=str(prompt.get("ratio", "16:9")),
                                  negatives=str(prompt.get("negatives", "")))
        materials: dict[str, ShotMaterials] = {}
        for scene in filming["scenes"]:
            scene_image, scene_text, scene_errors = self._scene_image(drama, scene["background"])
            scene_key = Path(scene_image).parent.name if scene_image else ""
            for shot in scene["shots"]:
                key = shot_key(episode.name, scene["id"], shot["id"]).value
                view = (scene_image, scene_text, scene_errors, scene_key)
                if shot.get("background"):
                    image, text, view_errors = self._scene_image(drama, shot["background"])
                    view = (image, text, view_errors, Path(image).parent.name if image else "")
                shot_image, shot_text, shot_errors, shot_scene_key = view
                errors = list(shot_errors)
                motion_kind, motion = self._motion(episode / "scenes" / scene["id"] / "shots" / shot["id"], errors)
                cast = self._counted(self._cast(drama, config, shot, errors),
                                     episode / "scenes" / scene["id"] / "shots" / shot["id"])
                prop_keys = list(shot.get("props", []))
                for cast_key in shot["cast"]:
                    card = self._card(drama, cast_key)
                    if card:
                        try:
                            prop_keys.extend(character_weapon_keys((card / f"{card.name}.md").read_text(encoding="utf-8")))
                        except ValueError as exc:
                            errors.append(f"{cast_key}：{exc}")
                props = self._props(drama, list(dict.fromkeys(prop_keys)), errors)
                first = episode / "scenes" / scene["id"] / "shots" / shot["id"] / "planning" / f"{shot['id']}_first_frame.png"
                materials[key] = ShotMaterials(motion_kind, motion, cast, shot_image, tuple(errors), shot_text, shot_scene_key, props,
                                               self._rel(first) if first.is_file() else "")
        return settings, materials

    def boards(self, episode_path: str, filming: dict[str, Any]) -> dict[str, str]:
        """Each 镜组's board (follow-up 331): `scenes/{sN}/groups/{gN}/board.png`, keyed `ep1_s1_g2`; absent boards are left out."""
        episode = self.root / episode_path
        out: dict[str, str] = {}
        for scene in filming["scenes"]:
            for group in scene.get("groups", []):
                board = episode / SCENES_DIR_NAME / scene["id"] / GROUPS_DIR_NAME / group["id"] / GROUP_BOARD_FILE
                if board.is_file():
                    out[group_key(episode.name, scene["id"], group["id"])] = self._rel(board)
        return out

    def _settings(self, drama: Path) -> dict[str, Any]:
        data = json.loads((drama / "workflow.json").read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}

    def _rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def _scene_image(self, drama: Path, bg: str) -> tuple[str, str, list[str]]:
        if not bg:
            return "", "", ["场次没有绑定环境资产：每镜都要上传背景图"]
        root = drama / SETTINGS_DIR / "background"
        for folder in sorted(root.rglob(bg + "_*")) if root.is_dir() else []:
            image, md = folder / (folder.name + ".png"), folder / (folder.name + ".md")
            if folder.is_dir() and md.is_file():
                errors = [] if image.is_file() else [f"环境资产 {bg} 没有场景图 {image.name}"]
                text = self._section(md, SCENE_SECTION)
                if not text:
                    errors.append(f"环境资产 {bg} 的卡里没有「{SCENE_SECTION}」一节")
                return (self._rel(image) if image.is_file() else ""), text, errors
        return "", "", [f"找不到环境资产 {bg}"]

    @staticmethod
    def _section(md: Path, head: str) -> str:
        """The first ```text block under `## {head}` — prompt-ready text only, never the card's tables or notes."""
        text = md.read_text(encoding="utf-8").replace("\r\n", "\n")
        match = re.search(r"^## " + re.escape(head) + r"\n(?:(?!^## ).)*?```text\n(.*?)\n```", text, re.S | re.M)
        return match.group(1).strip() if match else ""

    def _motion(self, shot_dir: Path, errors: list[str]) -> tuple[str, str]:
        decision = shot_dir / "planning" / "previz.json"
        if not decision.is_file():
            errors.append("还没有 overhead（先写 planning/overhead.toml 并运行 tools/shot_overhead.py）")
            return "", ""
        if json.loads(decision.read_text(encoding="utf-8")).get("previz"):
            video = shot_dir / "previz" / f"{shot_dir.name}_previz.mp4"
            if video.is_file():
                return "video", self._rel(video)
            errors.append("复杂镜要 previz 视频，还没渲（tools/overhead_previz.py --render）")
            return "", ""
        image = shot_dir / "planning" / f"{shot_dir.name}_overhead_ref.png"
        if image.is_file():
            return "image", self._rel(image)
        errors.append("缺给模型的 overhead 图（重跑 tools/shot_overhead.py）")
        return "", ""

    def _card(self, drama: Path, key: str) -> Path | None:
        match = KEY_RE.match(key)
        root = drama / SETTINGS_DIR / "characters"
        if not match or not root.is_dir():
            return None
        hits = [d for d in character_dirs(root) if d.name.startswith(f"{match[1]}{match[2]}_")]
        return hits[0] if len(hits) == 1 else None

    def _cast(self, drama: Path, config: dict[str, Any], shot: dict[str, Any], errors: list[str]) -> tuple[CastMember, ...]:
        table = config.get("figure_colors", {}) if isinstance(config.get("figure_colors"), dict) else {}
        names = config.get("names", {}) if isinstance(config.get("names"), dict) else {}
        speakers = {line.split("：", 1)[0].strip() for line in shot["dialogue"].splitlines() if "：" in line}
        used: dict[str, str] = {}
        out: list[CastMember] = []
        for key in shot["cast"]:
            card = self._card(drama, key)
            if card is None:
                errors.append(f"找不到人物卡 {key}")
                continue
            number = card.name.split("_", 1)[0]
            folder = card
            if "-" in key:
                stages = [d for d in card.iterdir() if d.is_dir() and d.name.startswith(key + "_")]
                if len(stages) != 1:
                    errors.append(f"人物卡 {card.name} 下找不到换装阶段 {key}")
                    continue
                folder = stages[0]
            image = folder / f"{key}_views.png" if "-" in key else card / "views" / f"{card.name}_views.png"
            if not image.is_file():
                errors.append(f"{key} 没有三视图 {image.name}")
                continue
            voice = card / "views" / f"{card.name}_audio.mp3"
            # 声样有就挂；没有不再报错（chuanyue_yiri follow-up 036）：bible §2.1 不开口或只说一句的当地人不做声样，
            # 由那一镜直接生成。已有声样的人物编译结果不变，所以不升编译器版本。
            has_voice = voice.is_file()
            look = self._section(card / f"{card.name}.md", LOOK_SECTION)
            if "-" in key:      # 换装阶段卡有自己的「Shot prompt 外观」就用它（长相照本人、衣服换掉），
                # 否则人物卡外观段里的本人造型会和换装三视图打架（chuanyue_yiri follow-up 068：浴场裹布）
                stage_card = folder / f"{folder.name}.md"
                look = (self._section(stage_card, LOOK_SECTION) if stage_card.is_file() else "") or look
            if not look:
                errors.append(f"人物卡 {card.name} 里没有「{LOOK_SECTION}」一节")
            name = names.get(number) or self._name(card)
            color = table.get(number) or next((c for c in FALLBACK_COLORS if c not in used.values()), "灰")
            if color not in KNOWN_COLORS:
                errors.append(f"workflow.json figure_colors 的 {number}＝{color} 不是可用颜色")
            if color in used.values():      # 不同框的人可以共用一色；同框撞色读不出谁是谁
                errors.append(f"{key} 与同镜另一人共用人偶颜色 {color}，在 workflow.json figure_colors 里换色")
            used[number] = color
            speaks = any(who and (who in name or name in who) for who in speakers)    # 台词写「萨缪尔」，人物名是「萨缪尔修士」
            out.append(CastMember(key, name, self._rel(image), color, self._rel(voice) if has_voice else "", look, speaks,
                                  folder.name, voice.stem))
        return tuple(out)

    @staticmethod
    def _counted(cast: tuple[CastMember, ...], shot_dir: Path) -> tuple[CastMember, ...]:
        """How many people each card stands for, counted from the overhead's [[actor]]s (card number before the first
        `_`, times `count`): two gate guards drawn from one card become 「北郡门卫 ×2」 in the prompt (follow-up 274)."""
        plan = shot_dir / "planning" / "overhead.toml"
        if not plan.is_file():
            return cast
        counts: dict[str, int] = {}
        for actor in tomllib.loads(plan.read_text(encoding="utf-8")).get("actor", []):
            number = str(actor.get("key", "")).split("_", 1)[0]
            counts[number] = counts.get(number, 0) + int(actor.get("count", 1))
        return tuple(dataclasses.replace(m, count=counts[m.key.split("-", 1)[0]]) if counts.get(m.key.split("-", 1)[0], 1) > 1
                     else m for m in cast)

    def _props(self, drama: Path, keys: list[str], errors: list[str]) -> tuple[PropItem, ...]:
        root = drama / SETTINGS_DIR / "props"
        out: list[PropItem] = []
        for key in keys:
            hits = [d for d in grouped_dirs(root, prop_key.is_folder_name) if d.name.startswith(key + "_")]
            if len(hits) != 1:
                errors.append(f"找不到道具卡 {key}")
                continue
            folder = hits[0]
            image = next((f for f in (folder / f"{folder.name}.png", folder / f"{key}-1_正面.png") if f.is_file()), None)
            if image is None:
                errors.append(f"道具 {key} 没有锚点图 {folder.name}.png")
                continue
            look = self._section(folder / f"{folder.name}.md", LOOK_SECTION)
            if not look:
                errors.append(f"道具卡 {folder.name} 里没有「{LOOK_SECTION}」一节")
            out.append(PropItem(key, self._name(folder), self._rel(image), folder.name, look))
        return tuple(out)

    @staticmethod
    def _name(card: Path) -> str:
        md = card / f"{card.name}.md"
        lines = md.read_text(encoding="utf-8").splitlines() if md.is_file() else []
        title = next((line[2:] for line in lines if line.startswith("# ")), card.name)
        return next((part.strip() for part in title.split("·") if re.search(r"[一-鿿]", part)), card.name)
