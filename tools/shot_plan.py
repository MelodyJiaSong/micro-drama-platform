# -*- coding: utf-8 -*-
"""一个 shot 的**镜头平面图** —— 给「这条路线对不对」做快速对账。

名字（2026-09-21 follow-up 028 用户定调）：机位在世界里飞的叫**航线图 flight plan**，
产物 `shotNN_flightplan.png`；地面镜的机位与人物走位叫**走位平面图 ground plan**，
产物 `shotNN_groundplan.png`。`floor plan` 一词退役——它在影视工业里指室内 / 场地平面图，
拿来称呼一条 1.2 km 的空中航线是错的（旧剧已出的 `*_floorplan.png` 不回溯改名）。

存在的理由（follow-up：用户 2026-09-20「交流少了，先给我一个 floor plan」）：
shot 的 `镜头:` 是一段散文，previz 是 751 个关键帧，两者都不能让人一眼看出
「从哪飞到哪、途经什么、离河多远」。**读图比读散文快两个数量级**，而错一条航线
的代价是一次 30 秒的重渲。所以先出图、用户点头、再渲。

输入（两边都是既有的唯一出处，本脚本不自编任何坐标）：
  · `previz_config.toml` 的 `[[机位]]` —— 航线本身（世界坐标，逐帧）。
  · W11 §2.8 全城坐标表 —— 城墙 / 城门 / 河道 / 街 / 地标，经 `tools/previz/city_layout`
    乘同一个 `CITY_SCALE`。**尺度必须与 builder 同源**，否则图上城市与航线错位，
    而且看上去毫无破绽。

输出（写进 shot 目录下的 `planning/`）：
  · `{shot}_flightplan.png`  俯视图：城市 + 航线 + ①②③④ 航点（地面镜为 `_groundplan.png`）
  · `{shot}_route.md`        同一批数字的文字版（航点表 + 逐航点离河距离与航向差）

用法：
  python tools/shot_plan.py ai_videos/shikong_lvxing/sk1/5_6_分镜与prompt/shots/shot01
  python tools/shot_plan.py <shot 目录> --waypoints 0,8,16,30
  python tools/shot_plan.py <shot 目录> --kind ground     # 地面镜：走位平面图
  python tools/shot_plan.py <shot 目录> --coverage        # 这一镜到底拍到了哪些主体
  python tools/shot_plan.py --city <scenes/{world} 目录>  # 全城 bg 分布图
"""
from __future__ import annotations

import argparse
import importlib
import math
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.previz.city_layout import CITY_SCALE, read_w11  # noqa: E402
from tools.previz.planstyle import (  # noqa: E402
    ACCENT, ACCENT_GHOST, BG_KEY, BG_KEY_BG, BG_NONE, GRID, INK, LEG_LABEL_BG,
    MARGIN, MUTED, PANEL_BG, PAPER, STREET, WALL, WALL_FILL, WATER, WATER_FILL,
    font, north_arrow, scale_bar,
)

# 世界地理坐标表（W11 §2.8 那种）。有就画城墙/河/城门/地标，没有就只画
# blocks.toml + 航线——**没有坐标表不是错误**，别的剧可能根本没有这一层。
LAYOUT_REL = ("0_research", "parts", "w11_city_layout.md")


def find_layout(start: Path) -> Path | None:
    for d in (start, *start.parents):
        cand = d.joinpath(*LAYOUT_REL)
        if cand.is_file():
            return cand
        if d.name == "ai_videos":
            break
    return None

sys.stdout.reconfigure(encoding="utf-8")

MAP_W, MAP_H = 1560, 1900       # 左侧俯视图
PANEL_W = 700                   # 右侧航点说明栏（详情不压地图，怎么挤都读得清）
W, H = MAP_W + PANEL_W, MAP_H
PROFILE_H = 430                 # 下方高度剖面条
CITY_W, CITY_H = 2260, 2500     # 全城 bg 分布图（没有右栏，地图自己占满）
PAD_M = 160.0                   # 航线外扩多少米才收边

# 配色与字体走 tools/previz/planstyle —— 与场地平面图同一套规范，改那一处两张图一起变
BG = PAPER
PATH = ACCENT
PATH_GHOST = ACCENT_GHOST
CONE = (*ACCENT, 46)


@dataclass(frozen=True)
class Cam:
    t: float
    pos: tuple[float, float, float]
    look: tuple[float, float, float]
    lens: float


# 没有 per-shot `previz_config.toml` 的剧：机位表在别处。值是模块名，模块导出
# `SHOTS: {shot_id: (时长, 焦距mm, [(t, 机位xyz, 看向xyz)])}`，坐标已是世界米。
PATH_TABLES: dict[str, str] = {"sk2": "tools.previz.sk2_gate_paths"}


def external_path(shot_dir: Path) -> list[Cam] | None:
    drama = next((d.name for d in shot_dir.parents if d.name in PATH_TABLES), None)
    if drama is None:
        return None
    entry = importlib.import_module(PATH_TABLES[drama]).SHOTS.get(
        shot_dir.name.replace("shot", "S"))
    if entry is None:
        return None
    _dur, lens, keys = entry
    return [Cam(float(t), tuple(map(float, pos)), tuple(map(float, look)), float(lens))
            for t, pos, look in keys]


def handoff_tail(shot_dir: Path, refs: tuple[list, ...], seen: frozenset[str]) -> Cam:
    """`["承接", "shotNN"]` → 被承接那一镜的末帧机位。"""
    names = {r[1] for r in refs if r[0] == "承接"}
    if len(names) != 1:
        raise SystemExit(f"{shot_dir.name} 的承接引用指向多个 shot：{sorted(names)}")
    name = names.pop()
    if name in seen:
        raise SystemExit(f"承接成环：{' → '.join([*sorted(seen), name])}")
    src = shot_dir.parent / name
    if not src.is_dir():
        raise SystemExit(f"{shot_dir.name} 承接 {name}，但 {src} 不存在")
    return load_path(src, seen | {shot_dir.name})[-1]


def load_path(shot_dir: Path, seen: frozenset[str] = frozenset()) -> list[Cam]:
    cfg_path = shot_dir / "previz_config.toml"
    if not cfg_path.is_file():
        ext = external_path(shot_dir)
        if ext is not None:
            return sorted(ext, key=lambda c: c.t)
        raise SystemExit(f"没有 {cfg_path} —— 这个 shot 还没有 previz 航线，先出 previz_config")
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    cams = cfg.get("机位") or []
    if not cams:
        raise SystemExit(f"{cfg_path} 里没有 [[机位]]")
    if isinstance(cams, dict):
        # 另一种 previz 写法：`["机位"]` 单表 + 基准主体/占画高/方位角，机位是**相对某个主体**
        # 摆的，整条航线里没有一个世界坐标。俯视图画的是「在世界里从哪飞到哪」，这种镜没有这回事。
        raise SystemExit(
            f"{cfg_path} 用的是相对机位（`[\"机位\"]` 单表 + 基准主体/占画高/方位角），"
            "没有世界坐标航线，画不出俯视图。"
            "俯视图只适用于 `[[机位]]` 逐帧世界坐标的走动镜（航拍 / 穿行 / 跨地点）。"
        )
    out: list[Cam] = []
    for c in cams:
        pos, look = c["位置"], c["看向"]
        if "承接" in (pos[0], look[0]):
            tail = handoff_tail(shot_dir, (pos, look), seen)
            pos = ["世界", *tail.pos] if pos[0] == "承接" else pos
            look = ["世界", *tail.look] if look[0] == "承接" else look
        if pos[0] != "世界" or look[0] != "世界":
            raise SystemExit(
                f"t={c['t']} 的机位不是世界坐标（{pos[0]} / {look[0]}）——"
                "俯视图只画世界坐标，Place 局部坐标要先转换"
            )
        out.append(Cam(float(c["t"]), tuple(map(float, pos[1:4])),
                       tuple(map(float, look[1:4])), float(c.get("焦距", 24.0))))
    return sorted(out, key=lambda c: c.t)


def seg_dist(p, a, b) -> tuple[float, float]:
    """(点到线段的距离, 线段航向°)。"""
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.dist(p, (ax + t * dx, ay + t * dy)), math.degrees(math.atan2(dy, dx)) % 360


def nearest_on(poly: list[tuple[float, float]], p: tuple[float, float]) -> tuple[float, float]:
    """(到折线的最近距离, 该段走向°)。折线为空时调用方自己处理，不在这里造数。"""
    best = (float("inf"), 0.0)
    for a, b in zip(poly, poly[1:]):
        d, h = seg_dist(p, a, b)
        if d < best[0]:
            best = (d, h)
    return best


def heading_at(cams: list[Cam], i: int) -> float:
    j = min(i + 1, len(cams) - 1)
    k = i if j > i else max(0, i - 1)
    a, b = cams[k].pos, cams[j].pos
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360


def speed_at(cams: list[Cam], i: int) -> float:
    j = min(i + 1, len(cams) - 1)
    k = i if j > i else max(0, i - 1)
    dt = cams[j].t - cams[k].t
    return 0.0 if dt <= 0 else math.dist(cams[k].pos, cams[j].pos) / dt


class Plan:
    """世界米 → 画布像素。北在上：世界 +Y 向上，+X 向右。"""

    def __init__(self, pts: list[tuple[float, float]], w: int, h: int, margin: int) -> None:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, x1 = min(xs) - PAD_M, max(xs) + PAD_M
        y0, y1 = min(ys) - PAD_M, max(ys) + PAD_M
        sx = (w - 2 * margin) / max(x1 - x0, 1e-6)
        sy = (h - 2 * margin) / max(y1 - y0, 1e-6)
        self.k = min(sx, sy)
        self.cx, self.cy = (x0 + x1) / 2, (y0 + y1) / 2
        self.w, self.h = w, h

    def __call__(self, x: float, y: float) -> tuple[float, float]:
        return (self.w / 2 + (x - self.cx) * self.k,
                self.h / 2 - (y - self.cy) * self.k)

    def inside(self, x: float, y: float, pad: int = 60) -> bool:
        px, py = self(x, y)
        return -pad <= px <= self.w + pad and -pad <= py <= self.h + pad


# 已画出的标签框。门名 / 地标 / 建筑组 / 航段牌全挤在门洞那一小块地方，
# 不记账就会互相盖住——整张图最先失去可读性的就是这里。
_PLACED: list[tuple[float, float, float, float]] = []


def _hits(box) -> bool:
    l, t_, r, b = box
    return any(not (r < pl_ or l > pr or b < pt or t_ > pb) for pl_, pt, pr, pb in _PLACED)


def place_label(d: ImageDraw.ImageDraw, px: float, py: float, text, f, fill=INK,
                bg=(255, 255, 255, 216), offsets=((14, -11),)) -> None:
    """挑第一个不与已有标签相撞的位置；全撞就用最后一个（宁可叠，不要不画）。"""
    for i, (dx, dy) in enumerate(offsets):
        x, y = px + dx, py + dy
        l, t_, r, b = d.textbbox((x, y), text, font=f, anchor="lt")
        if not _hits((l - 7, t_ - 4, r + 7, b + 4)) or i == len(offsets) - 1:
            label(d, (x, y), text, f, fill=fill, bg=bg)
            return


def label(d: ImageDraw.ImageDraw, xy, text, f, fill=INK, bg=(255, 255, 255, 216), anchor="lt"):
    """带底色的文字块。Pillow 的 anchor 不支持多行，所以多行走左上角对齐。"""
    x, y = xy
    if "\n" in text:
        l, t, r, b = d.multiline_textbbox((x, y), text, font=f, spacing=6)
        d.rounded_rectangle((l - 9, t - 6, r + 9, b + 6), radius=6, fill=bg)
        d.multiline_text((x, y), text, font=f, fill=fill, spacing=6)
        _PLACED.append((l - 9, t - 6, r + 9, b + 6))
        return
    l, t, r, b = d.textbbox((x, y), text, font=f, anchor=anchor)
    d.rounded_rectangle((l - 7, t - 4, r + 7, b + 4), radius=5, fill=bg)
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)
    _PLACED.append((l - 7, t - 4, r + 7, b + 4))


BLOCK_STYLE = {
    "house": ((222, 210, 190), (168, 148, 118)),
    "wall":  ((206, 186, 150), (128, 104, 70)),
    "wharf": ((214, 200, 168), (150, 124, 82)),
    "water": (WATER_FILL, WATER),
}


def load_blocks(shot_dir: Path) -> list[dict]:
    """`planning/blocks.toml` 的建筑组示意块。没有就不画——本脚本不自编建筑位置。"""
    f = shot_dir / "planning" / "blocks.toml"
    if not f.is_file():
        return []
    return tomllib.loads(f.read_text(encoding="utf-8")).get("block", [])


def draw_blocks(d: ImageDraw.ImageDraw, pl: Plan, blocks: list[dict], f_s, f_xs) -> None:
    f_xs_g = (f_xs,)
    for b in blocks:
        cx, cy = b["xy"]
        L, Wd = b["size"]
        a = math.radians(float(b.get("rot", 0.0)))
        ca, sa = math.cos(a), math.sin(a)
        corners = []
        for dx, dy in ((-L / 2, -Wd / 2), (L / 2, -Wd / 2), (L / 2, Wd / 2), (-L / 2, Wd / 2)):
            corners.append(pl(cx + dx * ca - dy * sa, cy + dx * sa + dy * ca))
        fill, line = BLOCK_STYLE.get(b.get("kind", "house"), BLOCK_STYLE["house"])
        d.polygon(corners, fill=fill, outline=line, width=4)
        bx, by = pl(cx, cy)
        key = (b.get("bg") or "").strip()
        text = f"{key}  {b['name']}" if key else b["name"]
        wpx = d.textlength(text, font=f_s)
        place_label(d, bx, by, text, f_s, fill=(72, 58, 40), bg=(255, 255, 255, 206),
                    offsets=((-wpx / 2, -18), (-wpx / 2, -70), (-wpx / 2, 34),
                             (-wpx - 26, -18), (26, -18)))
        if not key:
            # 没有主体卡的块也要说出来——否则「为什么这块没标 bg」要问一次
            place_label(d, bx, by + 30, "无专属 bg", f_xs_g[0], fill=BG_NONE,
                        bg=(255, 255, 255, 176),
                        offsets=((-30, 0), (-30, 34), (-30, -60)))


def arrow(d: ImageDraw.ImageDraw, at, heading_px: float, size: int, fill) -> None:
    """航向箭头。俯视图上「往哪飞」必须画出来——光有一条线，两头都说得通。"""
    x, y = at
    a = math.radians(heading_px)
    tip = (x + size * math.cos(a), y + size * math.sin(a))
    for s in (140, -140):
        b = a + math.radians(s)
        d.line([tip, (tip[0] + size * 0.92 * math.cos(b), tip[1] + size * 0.92 * math.sin(b))],
               fill=fill, width=7)


def sk2_layout(shot_dir: Path):
    """sk2 没有 W11 §2.8 那种坐标表，城市层取 `build_stormwind` 用的同一份纯几何。"""
    if not any(dd.name == "sk2" for dd in shot_dir.parents):
        return None
    return importlib.import_module("tools.previz.stormwind_layout")


def rot_rect(pl: Plan, cx: float, cy: float, w: float, dp: float, ang: float):
    """绕 Z 转 ang 的矩形足迹 → 画布四点。长边 w 沿街切向，与 blender 的 box+rotation_euler 一致。"""
    c, s_ = math.cos(ang), math.sin(ang)
    return [pl(cx + dx * c - dy * s_, cy + dx * s_ + dy * c)
            for dx, dy in ((-w / 2, -dp / 2), (w / 2, -dp / 2), (w / 2, dp / 2), (-w / 2, dp / 2))]


def draw_city_sk2(d: ImageDraw.ImageDraw, pl: Plan, L, f_s, f_xs) -> None:
    """暴风城：城墙 → 运河 → 填充体块 → 逐栋街墙建筑 → 地标 → 锚点名。"""
    x0, y0, x1, y1 = L.wall_bounds()
    d.polygon([pl(x0, y0), pl(x1, y0), pl(x1, y1), pl(x0, y1)],
              fill=WALL_FILL, outline=WALL, width=5)
    d.line([pl(*L.ANCHORS[k][:2]) for k in L.CANAL],
           fill=WATER_FILL, width=max(5, int(L.CANAL_W * pl.k)), joint="curve")

    fill, edge = BLOCK_STYLE["house"]
    faint = (232, 224, 208)
    for x, y, w, dp, _h in L.infill_footprints():
        d.rectangle([pl(x - w / 2, y + dp / 2), pl(x + w / 2, y - dp / 2)], fill=faint)
    for nm, names, _r, g in L.CORRIDORS:
        for bx, by, w, dp, ang, _h, roof in L.corridor_footprints(nm, L.polyline(names), g):
            d.polygon(rot_rect(pl, bx, by, w, dp, ang), fill=fill,
                      outline=edge if roof else None)

    lm, lm_edge = BLOCK_STYLE["wall"]
    for nm, x, y, sx, sy, _h in L.landmark_boxes():
        d.rectangle([pl(x - sx / 2, y + sy / 2), pl(x + sx / 2, y - sy / 2)],
                    fill=lm, outline=lm_edge, width=4)
        if pl.inside(x, y, pad=-10):
            lx, ly = pl(x, y + sy / 2)
            label(d, (lx, ly - 30), nm, f_s, INK, LEG_LABEL_BG)
    for nm, (x, y, _z) in L.ANCHORS.items():
        if not pl.inside(x, y, pad=-10):
            continue
        px, py = pl(x, y)
        d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=BG_NONE)
        label(d, (px + 12, py - 13), nm.replace("_", " "), f_xs, BG_NONE, None)


def draw_city(d: ImageDraw.ImageDraw, pl: Plan, w11: dict) -> None:
    for wall in w11["wall"]:
        pts = [pl(*p) for p in wall["points"]]
        if len(pts) >= 3:
            d.polygon(pts, fill=WALL_FILL, outline=WALL, width=5)
    for rv in w11["river"]:
        pts = [pl(*p) for p in rv["points"]]
        if len(pts) >= 2:
            d.line(pts, fill=WATER_FILL, width=max(8, int(56 * pl.k)), joint="curve")


def _dodge(px: float, py: float, avoid: list[tuple[float, float]], reach: int) -> tuple[float, float]:
    """把标签推到离所有航点圆圈最远的那一侧 —— 城门名被编号盖住，图就白画了。"""
    cands = [(px + reach, py - 11), (px - reach * 4, py - 11),
             (px + 14, py - reach - 26), (px + 14, py + reach)]
    if not avoid:
        return cands[0]
    return max(cands, key=lambda c: min(math.dist(c, a) for a in avoid))


def draw_places(d: ImageDraw.ImageDraw, pl: Plan, w11: dict, f_s, f_xs,
                avoid: list[tuple[float, float]] | None = None,
                named: set[str] | None = None) -> None:
    """W11 的城门与地标。`named` 里已被示意块标注过的名字不再重复标——
    「东水门」同时出现在方块标签和门标记上，只会挤成一团。"""
    avoid, named = avoid or [], named or set()
    for g in w11["gate"]:
        x, y = g["xy"]
        if not pl.inside(x, y, pad=-20) or any(g["name"] in n for n in named):
            continue
        px, py = pl(x, y)
        d.rectangle((px - 11, py - 11, px + 11, py + 11), fill=(255, 255, 255), outline=WALL, width=5)
        place_label(d, px, py, g["name"], f_s, fill=(96, 74, 48),
                    offsets=((20, -13), (20, -66), (20, 36), (-190, -13)))
    for lm in w11["landmark"]:
        x, y = lm["xy"]
        if not pl.inside(x, y, pad=-20) or any(lm["name"] in n or n in lm["name"] for n in named):
            continue
        px, py = pl(x, y)
        d.ellipse((px - 6, py - 6, px + 6, py + 6), fill=MUTED)
        place_label(d, px, py, lm["name"], f_xs, fill=(92, 92, 92), bg=(255, 255, 255, 176),
                    offsets=((16, -11), (16, -54), (16, 30), (-170, -11)))


def draw_panel(d: ImageDraw.ImageDraw, rows, river_name: str, f_h, f_m, f_s, f_xs) -> None:
    """右栏：逐航点的数字。离河距离与航向差单独一行——判断「这条航线跟不跟着河走」
    全靠这两个数，埋在句子里就没人看。"""
    x0 = MAP_W
    d.rectangle((x0, 0, W, MAP_H), fill=PANEL_BG)
    d.line((x0, 0, x0, MAP_H), fill=(214, 208, 196), width=3)
    x = x0 + 44
    d.text((x, 48), "航点", font=f_h, fill=INK)
    d.text((x, 104), f"「离{river_name}」＝到河道中线的水平距离", font=f_xs, fill=MUTED)
    d.text((x, 136), "「河道夹角」＝航向与该处河道走向之差", font=f_xs, fill=MUTED)
    y = 190
    for n, c, hd, v, dist, rh, look in rows:
        up = (rh + 180) % 360
        delta = (hd - up + 180) % 360 - 180
        d.ellipse((x, y, x + 52, y + 52), fill=PATH, outline=(255, 255, 255), width=4)
        d.text((x + 26, y + 27), str(n), font=f_m, fill=(255, 255, 255), anchor="mm")
        d.text((x + 72, y - 2), f"t = {c.t:g} s", font=f_h, fill=INK)
        d.text((x + 72, y + 46), f"高 {c.pos[2]:.0f} m ｜ {v:.0f} m/s ｜ {c.lens:.0f} mm",
               font=f_m, fill=(70, 70, 70))
        if river_name:
            far = dist > 60
            d.text((x + 72, y + 86), f"离{river_name} {dist:.0f} m ｜ 河道夹角 {delta:+.0f}°",
                   font=f_m, fill=PATH if far else (70, 120, 80))
        else:
            d.text((x + 72, y + 86), "（本剧没有世界坐标表，不算离河距离）", font=f_m, fill=MUTED)
        d.line((x, y + 132, W - 44, y + 132), fill=(224, 218, 206), width=2)
        y += 168


def draw_scale_bar(d: ImageDraw.ImageDraw, pl: Plan, f_s) -> None:
    for nice in (2000, 1000, 500, 200, 100, 50):
        if nice * pl.k <= 420:
            break
    scale_bar(d, MARGIN, pl.h - MARGIN + 60, pl.k, meters=nice)
    north_arrow(d, pl.w - MARGIN, MARGIN - 40)


def resolve_anchor(w11: dict, a: dict) -> tuple[float, float]:
    """`bg_anchors.toml` 的一条 anchor → 世界坐标。坐标只从 W11 取，这里不写死任何数。"""
    kind = a.get("kind")
    if kind in ("gate", "landmark"):
        for row in w11[kind]:
            if row["name"] == a["name"]:
                return tuple(row["xy"])
        raise SystemExit(f"W11 [[{kind}]] 里没有「{a['name']}」——名字要与 W11 §2.8 逐字一致")
    if kind == "river_offset":
        river = next((r for r in w11["river"] if r["name"].startswith(a["river"])), None)
        gate = next((g for g in w11["gate"] if g["name"] == a["gate"]), None)
        if river is None or gate is None:
            raise SystemExit(f"river_offset 认不出河「{a['river']}」或门「{a['gate']}」")
        poly = [tuple(p) for p in river["points"]]
        i = min(range(len(poly)), key=lambda j: math.dist(poly[j], tuple(gate["xy"])))
        # upstream_m 为负 ＝ 顺流下行（门外）。城门外的主体（关厢、草市）同样要挂在河上，
        # 而它们离门的距离是「出门多少米」，不是「上溯多少米」——一个符号就够，不必再发明一种 kind。
        rem, cur = abs(float(a["upstream_m"])), list(gate["xy"])
        step = 1 if float(a["upstream_m"]) < 0 else -1
        while rem > 0 and 0 <= i + step < len(poly):
            nxt = poly[i + step]
            seg = math.dist(cur, nxt)
            if seg >= rem:
                f = rem / seg
                return (cur[0] + (nxt[0] - cur[0]) * f, cur[1] + (nxt[1] - cur[1]) * f)
            rem -= seg
            cur = list(nxt)
            i += step
        return tuple(cur)
    raise SystemExit(f"不认识的 anchor.kind：{kind}")


def coverage(shot: str, shot_dir: Path, cams: list[Cam], out_dir: Path, near: float = 900.0) -> None:
    """逐帧视锥统计：这一镜到底拍到了哪些 W11 条目、各入画多少秒、最近到多少米。

    为什么要有它（2026-09-21 follow-up 028）：「航线图上标着无专属 bg 的建筑」是一张缺口清单，
    而这张清单第一次是手算的，改一次航线就作废。补卡的优先级只该由两个数决定——
    **入画多久、离镜头多近**——所以这两个数必须能一条命令重算。

    判据：水平视场由焦距得出（Super-35 24.89 mm 宽），条目中心落在视锥内即算「这一帧在画面里」；
    只算水平角，不做遮挡判断——遮挡要靠 blend 里的射线，这里只回答「镜头朝没朝它」。
    """
    layout = find_layout(shot_dir)
    if layout is None:
        raise SystemExit("本剧没有世界坐标表（W11 §2.8），算不了覆盖率")
    w11 = read_w11(layout)
    anchors = ([("gate", g["name"], tuple(g["xy"])) for g in w11["gate"]]
               + [("landmark", lm["name"], tuple(lm["xy"])) for lm in w11["landmark"]])
    scene = next((d for d in (shot_dir.parents[2] / "2_世界观人设" / "scenes").glob("*")
                  if (d / "bg_anchors.toml").is_file()), None)
    have: dict[str, str] = {}
    if scene:
        cfg = tomllib.loads((scene / "bg_anchors.toml").read_text(encoding="utf-8"))
        for b in cfg.get("bg", []) + cfg.get("todo", []):
            a = b.get("anchor") or {}
            if a.get("name"):
                have[a["name"]] = b["key"]

    dt = (cams[-1].t - cams[0].t) / max(1, len(cams) - 1)
    stat: dict[str, list] = {}
    for c in cams:
        hfov = 2.0 * math.degrees(math.atan(24.89 / (2.0 * c.lens)))
        look = math.degrees(math.atan2(c.look[1] - c.pos[1], c.look[0] - c.pos[0]))
        for kind, name, (x, y) in anchors:
            ang = math.degrees(math.atan2(y - c.pos[1], x - c.pos[0]))
            if abs((ang - look + 180) % 360 - 180) > hfov / 2:
                continue
            d = math.dist((x, y), (c.pos[0], c.pos[1]))
            row = stat.setdefault(name, [0.0, 1e9, kind, c.t, c.t])
            row[0] += dt
            row[1] = min(row[1], d)
            row[4] = c.t
    # 只留「真的看得见」的：默认 900 m 以内（走廊 r_far=600 m 之外没有肌理，
    # 再远的条目在画面里只是天际线上的一两个像素，不构成补卡理由）。塔另算：
    # 76 m 的繁塔两公里外仍是天际线主角，所以高耸地标放宽到 2.5 km。
    TALL = ("塔",)
    rows = [(n, v) for n, v in stat.items()
            if v[1] <= (2500.0 if any(t in n for t in TALL) else near) and v[0] >= 1.0]
    rows.sort(key=lambda kv: (-kv[1][0], kv[1][1]))
    lines = [f"# {shot} · 入画主体覆盖表", "",
             "由 `python tools/shot_plan.py <shot 目录> --coverage` 从 `previz_config.toml` 的逐帧机位 "
             "+ W11 §2.8 算出：**入画** ＝ 条目中心落在该帧水平视锥内的总秒数，**最近** ＝ 全程最近距离。"
             f"只算镜头朝没朝它，不做遮挡判断；只列 **{near:.0f} m 以内**（高耸的塔放宽到 2.5 km）、"
             "入画 ≥ 1 s 的条目——更远的在画面里只是天际线上的一两个像素，不构成补卡理由。", "",
             "**「主体卡」列为空 ＝ 这一镜反复拍到它、而 `scenes/` 里没有它的主体卡**，"
             "出图只能借世界锚点的长相（`bg_anchors.toml` 的 `[[todo]]` 就是这么来的）。", "",
             "| 入画 | 最近 | 类型 | W11 条目 | 主体卡 |", "|---|---|---|---|---|"]
    print(f"{shot}：视锥里出现过 {len(rows)} 个 W11 条目")
    for name, (sec, dmin, kind, t0, t1) in rows:
        key = have.get(name, "")
        lines.append(f"| {sec:.1f}s | {dmin:.0f} m | {kind} | {name} | "
                     + (f"`{key}`" if key else "**无**") + " |")
        print(f"   {sec:5.1f}s  {dmin:6.0f} m  {kind:8} {name}  {key or '← 无主体卡'}")
    out_dir.mkdir(parents=True, exist_ok=True)
    md = out_dir / f"{shot}_coverage.md"
    md.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
    print(f"✅ {md}")


def city_main(scene_dir: Path, out: Path | None) -> None:
    """全城俯视图：标出每个 bg 主体在城里的位置。没有航线、没有方向箭头。"""
    cfg_path = scene_dir / "bg_anchors.toml"
    if not cfg_path.is_file():
        raise SystemExit(f"没有 {cfg_path} —— 全城图的 bg 点位表，见 shot01/planning 的同名做法")
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8"))
    w11 = read_w11()
    placed = [(b, resolve_anchor(w11, b["anchor"])) for b in cfg.get("bg", [])]
    unplaced = cfg.get("unplaced", [])

    # 同一处地点的多个主体（州桥的 bg4 御街 / bg17 夜市 / bg9 今日遗址 是同一个点的
    # 不同时辰与时代）合成一个点、一条标签——三个点画在同一像素上只会叠成糊的一团。
    groups: dict[tuple[int, int], list[dict]] = {}
    for b, xy in placed:
        groups.setdefault((round(xy[0] / 30), round(xy[1] / 30)), []).append({**b, "_xy": xy})

    # 底部说明条先算高度，地图画在剩下的部分里：地图若占满整张画布，
    # 比例尺和最边上那个点（虹桥）会被说明条压掉。
    bh = 58 + 40 * len(unplaced) + 24 if unplaced else 0
    map_h = CITY_H - bh
    pts = [xy for _, xy in placed]
    for wall in w11["wall"]:
        pts += [tuple(p) for p in wall["points"]]
    # 边距放大：最外侧的点（虹桥）标签朝右伸出去，130 的边距装不下。
    pl = Plan(pts, CITY_W, map_h, 300)
    img = Image.new("RGB", (CITY_W, CITY_H), BG)
    map_img = Image.new("RGB", (CITY_W, map_h), BG)
    d = ImageDraw.Draw(map_img, "RGBA")
    f_t, f_h, f_m, f_s, f_xs = font(54, True), font(34, True), font(28), font(25), font(22)
    _PLACED.clear()

    draw_city(d, pl, w11)
    for g in w11["gate"]:
        gx, gy = pl(*g["xy"])
        d.rectangle((gx - 7, gy - 7, gx + 7, gy + 7), fill=(255, 255, 255), outline=WALL, width=3)

    for members in sorted(groups.values(), key=lambda g: g[0]["_xy"][1], reverse=True):
        x, y = members[0]["_xy"]
        px, py = pl(x, y)
        d.ellipse((px - 15, py - 15, px + 15, py + 15), fill=BG_KEY, outline=(255, 255, 255), width=4)
        keys = " / ".join(m["key"] for m in members)
        names = " · ".join(m["name"] for m in members)
        txt = f"{keys}  {names}"
        place_label(d, px, py, txt, f_s, fill=BG_KEY, bg=BG_KEY_BG,
                    offsets=((24, -15), (24, -58), (24, 28), (24, 70),
                             (-d.textlength(txt, font=f_s) - 30, -15)))

    d.text((MARGIN, 48), "汴京 · 全城 bg 主体分布图", font=f_t, fill=INK)
    d.text((MARGIN, 112), f"城市坐标 ×CITY_SCALE={CITY_SCALE:g}，来自 W11 §2.8 全城坐标表", font=f_s, fill=MUTED)
    d.text((MARGIN, 150), "● ＝ 一个 bg 场景主体 ｜ □ ＝ 外城/里城/宫城城门 ｜ 蓝带 ＝ 河道", font=f_s, fill=MUTED)
    draw_scale_bar(d, pl, f_s)

    img.paste(map_img, (0, 0))
    if unplaced:
        db = ImageDraw.Draw(img, "RGBA")
        db.rectangle((0, map_h, CITY_W, CITY_H), fill=PANEL_BG)
        db.line((0, map_h, CITY_W, map_h), fill=(214, 208, 196), width=3)
        db.text((MARGIN, map_h + 16), "没有点位的主体（不是漏标，逐条有原因）", font=f_h, fill=INK)
        yy = map_h + 62
        for u in unplaced:
            db.text((MARGIN, yy), f"{u['key']}  {u['name']}", font=f_xs, fill=BG_KEY)
            db.text((MARGIN + 250, yy), u["why"], font=f_xs, fill=MUTED)
            yy += 40

    out_dir = (out or scene_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{scene_dir.name}_bg_map.png"   # 全城分布图既不是航线也不是走位，叫「分布图 map」
    img.save(png)

    lines = ["# 汴京 · 全城 bg 主体分布", "",
             "由 `python tools/shot_plan.py --city <scenes/bianjing>` 生成；"
             "点位全部来自 W11 §2.8（`bg_anchors.toml` 只声明「挂在哪一条」，不写坐标）。", "",
             "| bg | 主体 | 世界坐标 | 挂在 W11 的哪一条 | 备注 |", "|---|---|---|---|---|"]
    for b, (x, y) in placed:
        a = b["anchor"]
        src = (f"{a['kind']} · {a.get('name', '')}" if a["kind"] != "river_offset"
               else f"river_offset · {a['river']} 自{a['gate']}"
                    + (f"下行 {abs(a['upstream_m']):g} m" if a["upstream_m"] < 0
                       else f"上溯 {a['upstream_m']:g} m"))
        lines.append(f"| `{b['key']}` | {b['name']} | {x:.0f}, {y:.0f} | {src} | {b.get('note', '')} |")
    lines += ["", "## 没有点位的主体（不是漏标）", "", "| bg | 主体 | 为什么 |", "|---|---|---|"]
    for u in unplaced:
        lines.append(f"| `{u['key']}` | {u['name']} | {u['why']} |")
    md = out_dir / "bg_index.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ {png}")
    print(f"✅ {md}")
    print(f"   已标 {len(placed)} 个 bg，未标 {len(unplaced)} 个（见表末，都有原因）")


def main() -> None:
    ap = argparse.ArgumentParser(description="航线俯视图 / 全城 bg 分布图")
    ap.add_argument("shot_dir", type=Path, help="shot 目录；--city 时是 scenes/{world} 目录")
    ap.add_argument("--city", action="store_true",
                    help="画全城 bg 主体分布图（无航线、无方向箭头），读该目录的 bg_anchors.toml")
    ap.add_argument("--kind", default="flight", choices=("flight", "ground"),
                    help="flight ＝ 走动镜的航线图（默认）；ground ＝ 地面镜的走位平面图")
    ap.add_argument("--near", type=float, default=900.0,
                    help="--coverage 只列这个距离以内的条目（米，默认 900 ＝ 走廊 r_far 再加余量）")
    ap.add_argument("--coverage", action="store_true",
                    help="不出图，改算「这一镜逐帧视锥里都有谁」：每个 W11 条目的入画秒数与最近距离")
    ap.add_argument("--waypoints", default="", help="逗号分隔的秒数；默认按拐点自动挑 4 个")
    ap.add_argument("--out", type=Path, default=None, help="输出目录，默认 {shot_dir}/planning")
    args = ap.parse_args()
    if args.city:
        city_main(args.shot_dir.resolve(), args.out)
        return

    shot_dir = args.shot_dir.resolve()
    if not shot_dir.is_dir():
        raise SystemExit(f"没有这个目录：{shot_dir}")
    shot = shot_dir.name
    kind_zh = "航线图" if args.kind == "flight" else "走位平面图"
    kind_en = "flight plan" if args.kind == "flight" else "ground plan"
    cams = load_path(shot_dir)
    if args.coverage:
        coverage(shot, shot_dir, cams, out_dir=(args.out or shot_dir / "planning").resolve(),
                 near=args.near)
        return
    blocks = load_blocks(shot_dir)
    layout = find_layout(shot_dir)
    w11 = read_w11(layout) if layout else None
    out_dir = (args.out or shot_dir / "planning").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.waypoints.strip():
        want = [float(s) for s in args.waypoints.split(",")]
    else:
        T = cams[-1].t
        want = [0.0, T * 0.27, T * 0.5, T * 0.73, T]
    idx: list[int] = []
    for t in want:
        i = min(range(len(cams)), key=lambda j: abs(cams[j].t - t))
        if i not in idx:
            idx.append(i)

    # 没有世界坐标表的剧：不画城市层，`离河` 一列也就无从算起，留空而不是编一个数。
    main_river, main_pts = ("", [])
    if w11:
        rivers = {r["name"]: [tuple(p) for p in r["points"]] for r in w11["river"]}
        main_river, main_pts = next(iter(rivers.items()))

    sk2 = sk2_layout(shot_dir) if not w11 else None
    fit = [(c.pos[0], c.pos[1]) for c in cams]
    if sk2:
        # 航线只有几百米、城却有七百米见方：只按航线收边会把城墙外的建筑全切掉，
        # 而「每栋楼摆在哪」正是这张图要回答的。取景按城墙四至 ∪ 航线。
        wx0, wy0, wx1, wy1 = sk2.wall_bounds()
        fit += [(wx0, wy0), (wx1, wy1)]
    pl = Plan(fit, MAP_W, MAP_H, MARGIN)
    img = Image.new("RGB", (W, H + PROFILE_H), BG)
    # 地图画在自己的画布上再贴进去：城墙多边形与河道折线远远伸出取景框，
    # 直接画在总画布上会盖住下方的高度剖面（实测第一版就是这样）。
    map_img = Image.new("RGB", (MAP_W, MAP_H), BG)
    md_ = ImageDraw.Draw(map_img, "RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    f_t, f_h, f_m, f_s, f_xs = font(54, True), font(38, True), font(29), font(25), font(22)

    if w11:
        draw_city(md_, pl, w11)
    elif sk2:
        draw_city_sk2(md_, pl, sk2, f_s, f_xs)
    draw_blocks(md_, pl, blocks, f_s, f_xs)
    wp_px = [pl(cams[i].pos[0], cams[i].pos[1]) for i in idx]
    if w11:
        draw_places(md_, pl, w11, f_s, f_xs, avoid=wp_px,
                    named={b["name"] for b in blocks})

    pts = [pl(c.pos[0], c.pos[1]) for c in cams]
    md_.line(pts, fill=PATH, width=11, joint="curve")
    # 每段航线中点一个大箭头 + 段号：一条线看不出往哪飞，箭头是方向标记。
    legs_todo: list[tuple[float, float, str]] = []
    for leg, (a, b) in enumerate(zip(idx, idx[1:]), 1):
        seg = pts[a:b + 1]
        if len(seg) < 2:
            continue
        for frac in (0.3, 0.7):
            j = max(1, int(len(seg) * frac))
            hx, hy = seg[j][0] - seg[j - 1][0], seg[j][1] - seg[j - 1][1]
            arrow(md_, seg[j], math.degrees(math.atan2(hy, hx)), 26, PATH)
        # 航段牌挂在航线旁边（沿法线推开），不做成第二种编号圆圈——
        # 与航点圆圈同形状只会让人分不清「第3段」和「航点3」。
        j = len(seg) // 2
        k = max(1, j)
        nx, ny = seg[k][1] - seg[k - 1][1], -(seg[k][0] - seg[k - 1][0])
        nl = math.hypot(nx, ny) or 1.0
        mx, my = seg[j][0] + nx / nl * 62, seg[j][1] + ny / nl * 62
        legs_todo.append((mx, my, f"航段 {leg}"))

    for mx, my, txt in legs_todo:
        wtx = md_.textlength(txt, font=f_m)
        place_label(md_, mx, my, txt, f_m, fill=PATH, bg=LEG_LABEL_BG,
                    offsets=((-wtx / 2, -20), (-wtx / 2, -74), (-wtx / 2, 38),
                             (-wtx - 30, -20), (30, -20)))

    # 地图上只落编号圆点；数字全部进右栏，永远不会互相压住。
    rows = []
    for n, i in enumerate(idx, 1):
        c = cams[i]
        px, py = pl(c.pos[0], c.pos[1])
        hd = heading_at(cams, i)
        v = speed_at(cams, i)
        dist, rh = nearest_on(main_pts, (c.pos[0], c.pos[1])) if main_pts else (float("nan"), 0.0)
        look_dir = math.degrees(math.atan2(c.look[1] - c.pos[1], c.look[0] - c.pos[0])) % 360
        md_.ellipse((px - 31, py - 31, px + 31, py + 31), fill=PATH, outline=(255, 255, 255), width=5)
        md_.text((px, py + 1), str(n), font=f_h, fill=(255, 255, 255), anchor="mm")
        rows.append((n, c, hd, v, dist, rh, look_dir))

    total = sum(math.dist(cams[i - 1].pos, cams[i].pos) for i in range(1, len(cams)))
    md_.text((MARGIN, 48), f"{shot} · {kind_zh}（{kind_en}）", font=f_t, fill=INK)
    md_.text((MARGIN, 112),
             f"全程 {total:.0f} m / {cams[-1].t:g} s ｜ 平均 {total / max(cams[-1].t, 1e-6):.1f} m/s",
             font=f_s, fill=MUTED)
    md_.text((MARGIN, 152),
             "红线＝航线，箭头＝飞行方向，●＝航点 ｜ 灰块＝建筑组示意（非几何真相，可改 blocks.toml）",
             font=f_s, fill=MUTED)
    draw_scale_bar(md_, pl, f_s)
    img.paste(map_img, (0, 0))
    draw_panel(d, rows, main_river, f_h, f_m, f_s, f_xs)

    # ── 高度剖面：横轴＝累计里程，纵轴＝高度 ────────────────────────────────
    top = MAP_H + 70
    ph = PROFILE_H - 150
    cum, acc = [0.0], 0.0
    for i in range(1, len(cams)):
        acc += math.dist(cams[i - 1].pos, cams[i].pos)
        cum.append(acc)
    zmax = max(c.pos[2] for c in cams)
    d.text((MARGIN, MAP_H + 12), "高度剖面（横轴＝累计里程，纵轴＝离地高度）", font=f_m, fill=MUTED)
    d.line((MARGIN, top + ph, W - MARGIN, top + ph), fill=MUTED, width=3)
    prof = [(MARGIN + (W - 2 * MARGIN) * (s / max(acc, 1e-6)),
             top + ph - ph * (c.pos[2] / max(zmax * 1.15, 1e-6)))
            for s, c in zip(cum, cams)]
    d.line(prof, fill=PATH, width=6, joint="curve")
    for n, i in enumerate(idx, 1):
        x, y = prof[i]
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=PATH, outline=(255, 255, 255), width=4)
        d.text((x, y), str(n), font=f_m, fill=(255, 255, 255), anchor="mm")
        d.text((x, y - 34), f"{cams[i].pos[2]:.0f} m", font=f_s, fill=INK, anchor="mb")

    png = out_dir / f"{shot}_{args.kind}plan.png"
    img.save(png)

    src = (f"从 `previz_config.toml` + W11 §2.8 生成，城市坐标乘 `CITY_SCALE={CITY_SCALE:g}`。"
           "改航线 ＝ 改 previz_config 重跑本脚本。"
           if (shot_dir / "previz_config.toml").is_file() else
           f"从 `{PATH_TABLES[next(d.name for d in shot_dir.parents if d.name in PATH_TABLES)]}` "
           "的 `SHOTS` 生成（世界米，1:1 不缩放；本剧没有 W11 坐标表，故不画城市层、不算离河距离）。"
           "改航线 ＝ 改那张表重跑本脚本。")
    lines = [f"# {shot} · {kind_zh}航点表", "",
             f"由 `tools/shot_plan.py` {src}", "",
             f"全程 **{total:.0f} m / {cams[-1].t:g} s**，平均 {total / max(cams[-1].t, 1e-6):.1f} m/s。", "",
             ("| # | t (s) | 世界坐标 x, y | 高度 | 速度 | 焦距 | 航向 | 视线 | "
              + (f"离{main_river}中线 | 与河道夹角 |" if main_pts else "离河中线 | 与河道夹角 |")),
             "|---|---|---|---|---|---|---|---|---|---|"]
    for n, c, hd, v, dist, rh, look in rows:
        up = (rh + 180) % 360
        delta = (hd - up + 180) % 360 - 180
        lines.append(
            f"| {n} | {c.t:g} | {c.pos[0]:.0f}, {c.pos[1]:.0f} | {c.pos[2]:.0f} m | {v:.0f} m/s "
            f"| {c.lens:.0f}mm | {hd:.0f}° | {look:.0f}° | "
            + (f"**{dist:.0f} m** | {delta:+.0f}° |" if main_pts else "— | — |"))
    md = out_dir / f"{shot}_route.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"✅ {png.relative_to(Path.cwd()) if png.is_relative_to(Path.cwd()) else png}")
    print(f"✅ {md.relative_to(Path.cwd()) if md.is_relative_to(Path.cwd()) else md}")
    for n, c, hd, v, dist, rh, look in rows:
        up = (rh + 180) % 360
        river = (f"  离河 {dist:6.1f} m  航向差 {((hd - up + 180) % 360 - 180):+5.0f}°"
                 if main_pts else "")
        print(f"   ⑨{n} t={c.t:5g}s  z={c.pos[2]:5.1f}m  v={v:4.0f}m/s{river}")


if __name__ == "__main__":
    main()
