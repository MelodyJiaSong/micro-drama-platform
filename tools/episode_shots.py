# -*- coding: utf-8 -*-
"""六模块剧（workflow.json: three-module-v1）的镜头查询：镜头目录 ↔ filming.json 的场与镜、出场人物 ↔ 人物卡、人偶颜色。

不 import bpy，overhead / previz / 资料包工具与 Blender 侧共用（一个名字只在这里定义一次）。

镜头目录：`{剧}/episodes/epNN/scenes/sN/shots/stN/`；镜头 key：`ep1_s4_st2`（集号不补零）。
出场人物 `cast` 写资产键：换装阶段 `c1-1`（人物卡 c1_Aaron 下的 c1-1_*）或人物卡本身 `c14`；怪物 `m7`。
人偶颜色：剧 `workflow.json` 的 `figure_colors`（人物卡号 → 颜色名，如 {"c1": "蓝"}）；overhead 图、previz 人偶与 prompt 的
颜色说明都读这一张表，所以同一个人在所有镜、所有参考里颜色一样。没登记的按卡号从 FALLBACK 里顺延。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = "workflow.json"
SETTINGS = "2_世界观人设"
KEY_RE = re.compile(r"^([cm])(\d+)(?:-(\d+))?$")          # c1、c1-1、m7

# 颜色名 → RGB（0–255）。名字与 tools/previz/build_previz.py 的 COLORS 同名同色，previz 人偶与 overhead 圆点一致。
# 绿幕前不用绿色人偶：与背景同色，读不出轮廓（previz 背景就是绿幕）。
FIGURE_RGB = {
    "蓝": (26, 77, 230), "黄": (230, 204, 26), "红": (217, 26, 26), "橙": (242, 115, 13), "紫": (140, 38, 217),
    "青": (26, 204, 204), "粉": (242, 115, 166), "白": (230, 230, 230), "褐": (102, 66, 33), "灰": (89, 89, 97),
    "绿": (26, 191, 38),
}
FALLBACK = ("蓝", "黄", "红", "橙", "紫", "青", "粉", "白", "褐")


class ShotError(Exception):
    pass


def drama_root(path: Path) -> Path:
    for d in (path, *path.parents):
        if (d / WORKFLOW).is_file() and (d / SETTINGS).is_dir():
            return d
    raise ShotError("%s 往上找不到六模块剧目录（没有 workflow.json + 2_世界观人设/）" % path)


def is_episode_shot(shot_dir: Path) -> bool:
    """新布局：…/episodes/epNN/scenes/sN/shots/stN。"""
    p = shot_dir.resolve()
    return (re.fullmatch(r"st\d+", p.name) is not None and p.parent.name == "shots"
            and re.fullmatch(r"s\d+", p.parent.parent.name) is not None and p.parents[2].name == "scenes"
            and re.fullmatch(r"ep\d+", p.parents[3].name) is not None)


def settings(drama: Path) -> dict:
    data = json.loads((drama / WORKFLOW).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def episode_shot(shot_dir: Path) -> dict:
    """{key, ep_dir, scene, shot}：scene / shot 是 filming.json 里那一场、那一镜的原样字典。"""
    p = shot_dir.resolve()
    if not is_episode_shot(p):
        raise ShotError("%s 不是 episodes/epNN/scenes/sN/shots/stN 镜头目录" % p)
    ep_dir = p.parents[3]
    doc = json.loads((ep_dir / "filming.json").read_text(encoding="utf-8"))
    for scene in doc["content"]["scenes"]:
        if scene["id"] != p.parent.parent.name:
            continue
        for shot in scene["shots"]:
            if shot["id"] == p.name:
                key = "ep%d_%s_%s" % (int(ep_dir.name[2:]), scene["id"], shot["id"])
                return {"key": key, "ep_dir": ep_dir, "scene": scene, "shot": shot}
    raise ShotError("filming.json 里没有 %s/%s" % (p.parent.parent.name, p.name))


def episode_shot_dirs(ep_dir: Path) -> list[Path]:
    """按 filming.json 的播放顺序列出本集每个镜头目录（目录不存在也列出，由调用方报缺）。"""
    doc = json.loads((ep_dir / "filming.json").read_text(encoding="utf-8"))
    return [ep_dir / "scenes" / sc["id"] / "shots" / st["id"] for sc in doc["content"]["scenes"] for st in sc["shots"]]


def _child(parent: Path, prefix: str) -> Path | None:
    hits = sorted(d for d in parent.iterdir() if d.is_dir() and d.name.startswith(prefix + "_")) if parent.is_dir() else []
    return hits[0] if len(hits) == 1 else None


def card_dir(drama: Path, asset_key: str) -> Path:
    """`c1-1` / `c1` / `m7` → 人物卡目录（c1_Aaron）。"""
    m = KEY_RE.match(asset_key)
    if not m:
        raise ShotError("出场人物键 %s 不是 c1 / c1-1 / m7 这样的资产键" % asset_key)
    root = drama / SETTINGS / "characters"           # 人物 c* 与怪物 m* 的卡都在 characters/
    card = _child(root, "%s%s" % (m.group(1), m.group(2)))
    if card is None:
        raise ShotError("找不到人物卡 %s%s_*（在 %s）" % (m.group(1), m.group(2), root.relative_to(drama)))
    return card


def asset_dir(drama: Path, asset_key: str) -> Path:
    """`c1-1` → 换装阶段目录；`c14` → 人物卡目录。"""
    card = card_dir(drama, asset_key)
    if "-" not in asset_key:
        return card
    sub = _child(card, asset_key)
    if sub is None:
        raise ShotError("人物卡 %s 下找不到换装阶段 %s_*" % (card.name, asset_key))
    return sub


def front_image(drama: Path, asset_key: str) -> Path:
    """人物参考图：正面全身单人图（不用三视图合图——模型会把合图读成几个人）。"""
    d = asset_dir(drama, asset_key)
    for p in (d / ("%s_front.png" % asset_key), d / "views" / ("%s_front.png" % d.name)):
        if p.is_file():
            return p
    raise ShotError("%s 没有正面全身图（%s_front.png 或 views/%s_front.png）" % (asset_key, asset_key, d.name))


def voice_sample(drama: Path, asset_key: str) -> Path | None:
    card = card_dir(drama, asset_key)
    p = card / "views" / ("%s_audio.mp3" % card.name)
    return p if p.is_file() else None


def display_name(drama: Path, asset_key: str) -> str:
    """人物卡 H1 里第一个中文名段：「Aaron · 亚伦 · 人类圣骑士学徒」→ 亚伦。workflow.json `names` 可覆盖。"""
    card = card_dir(drama, asset_key)
    override = settings(drama).get("names", {}).get(card.name.split("_", 1)[0])
    if override:
        return override
    md = card / ("%s.md" % card.name)
    h1 = next((ln[2:] for ln in md.read_text(encoding="utf-8").splitlines() if ln.startswith("# ")), card.name)
    return next((part.strip() for part in h1.split("·") if re.search(r"[一-鿿]", part)), card.name)


def card_number(asset_key: str) -> str:
    """`c1-1` → `c1`。"""
    m = KEY_RE.match(asset_key)
    if not m:
        raise ShotError("出场人物键 %s 不是 c1 / c1-1 / m7 这样的资产键" % asset_key)
    return "%s%s" % (m.group(1), m.group(2))


def figure_colors(drama: Path, keys: list[str]) -> dict[str, str]:
    """人物卡号（c1）→ 颜色名。登记过的用登记色；没登记的按出现顺序取 FALLBACK 里同镜没用过的色。"""
    table = settings(drama).get("figure_colors", {})
    out: dict[str, str] = {}
    for k in keys:
        n = card_number(k)
        if n in table:
            if table[n] not in FIGURE_RGB:
                raise ShotError("workflow.json figure_colors 的 %s＝%s 不在可用颜色 %s" % (n, table[n], "、".join(FIGURE_RGB)))
            out[n] = table[n]
    for k in keys:
        n = card_number(k)
        if n not in out:
            out[n] = next((c for c in FALLBACK if c not in out.values()), "灰")
    clash = sorted({c for c in out.values() if list(out.values()).count(c) > 1})
    if clash:     # 登记表里允许从不同框的人共用一色；同框撞色读不出谁是谁
        raise ShotError("同一镜里 %s 用了同一个人偶颜色 %s——在 workflow.json figure_colors 里给其中一人换色"
                        % ("、".join(n for n, c in out.items() if c in clash), "、".join(clash)))
    return out


def background_dir(drama: Path, bg: str) -> Path:
    for p in sorted((drama / SETTINGS / "background").rglob(bg + "_*")):
        if p.is_dir() and (p / (p.name + ".md")).is_file():
            return p
    raise ShotError("环境资产 %s 在 2_世界观人设/background 下找不到" % bg)


def background_image(drama: Path, bg: str) -> Path:
    d = background_dir(drama, bg)
    p = d / (d.name + ".png")
    if not p.is_file():
        raise ShotError("环境资产 %s 没有场景图 %s" % (bg, p.name))
    return p
