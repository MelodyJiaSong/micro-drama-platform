# -*- coding: utf-8 -*-
"""艾泽拉斯地图渲染器 —— 从地理树出羊皮纸风格的 PNG。

用法（仓库根目录）：
    python tools/render_wow_maps.py                      # 全部
    python tools/render_wow_maps.py --zone elwynn_forest # 单区
    python tools/render_wow_maps.py --min-points 4       # 放宽出图门槛

产物（写在 `{drama}/0_research/map/images/`）：
    zones/{zone_id}.png     单区图：点位画在**真实的游戏内地图坐标**上
    eastern_kingdoms.png    大陆示意图：按 lore 分区南北排列 + 邻接连线
    kalimdor.png            同上

设计依据
--------
· **数据只有一个出处**：`world_tree.json`（它本身又是 `g*.yaml` 的派生）。本脚本**不自编任何坐标**，
  `coords` 为空的节点就是不画——**错误的地图比没有地图更糟**，下游会照着它选景、排动线。
· **单区图是可信的**：`coords` 存的是魔兽的区域地图百分比坐标（玩家鼠标悬停看到的那一组），
  x 左→右 0–100、y 上→下 0–100，直接线性映射到画布即可。
· **大陆图是示意的**：树里没有 zone 的多边形与大陆坐标，所以大陆图按
  **lore 分区的南北次序 + 邻接关系**排布，图上写明「示意 · 非地理精确」。
  按次序排不是凭空编——东部王国自北向南＝洛丹伦 → 卡兹莫丹 → 暴风王国 → 荆棘谷，这是考据里的定论。
· 纯 **Pillow**，不引新依赖（`pillow` 本来就在 `pyproject.toml` 里）。
"""
from __future__ import annotations

import argparse
import io
import json
import math
import os
import random
import sys
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DRAMA = os.path.join(REPO, "ai_videos", "shengji_zhilu")
SRC = os.path.join(DRAMA, "0_research", "map", "world_tree.json")
OUT = os.path.join(DRAMA, "0_research", "map", "images")

FONT_DIR = "C:/Windows/Fonts"
F_LABEL = os.path.join(FONT_DIR, "simkai.ttf")   # 楷体：标注，接近手写地名的味道
F_UI = os.path.join(FONT_DIR, "simhei.ttf")      # 黑体：图框、图例、页脚

# 羊皮纸色（自然色名口径：暖米黄底 / 深褐墨 / 赭红点缀）
PARCHMENT = (214, 191, 152)
INK = (58, 40, 24)
INK_SOFT = (104, 80, 52)
ACCENT = (140, 52, 38)
GOLD = (168, 130, 62)

# 各类型的画法：(标记, 半径, 是否给标签, 字号档)
STYLE: dict[str, tuple[str, int, bool, int]] = {
    "city": ("keep", 13, True, 0),
    "district": ("square", 8, True, 1),
    "settlement": ("house", 9, True, 1),
    "dungeon": ("arch", 10, True, 1),
    "raid": ("arch", 11, True, 0),
    "battleground": ("cross", 9, True, 1),
    "subzone": ("dot", 5, True, 2),
    "poi": ("dot", 4, True, 2),
    "transport": ("wing", 7, False, 2),
}
FACTION_TINT = {"alliance": (44, 74, 132), "horde": (132, 44, 38), "neutral": (96, 84, 56)}


@dataclass(frozen=True)
class Node:
    nid: str
    parent: str | None
    ntype: str
    subtype: str
    zh: str
    en: str
    level: str
    faction: str
    xy: tuple[float, float] | None
    adjacent: tuple[str, ...]
    look: str
    verified: str


def load() -> tuple[dict[str, Node], dict[str, list[str]]]:
    raw = json.load(io.open(SRC, encoding="utf-8"))
    nodes: dict[str, Node] = {}
    for n in raw["nodes"]:
        c = (n.get("coords") or "").strip()
        xy = None
        if c.startswith("[") and "," in c:
            try:
                a, b = c.strip("[]").split(",")[:2]
                xy = (float(a), float(b))
            except ValueError:
                xy = None
        nodes[n["id"]] = Node(
            n["id"], n.get("parent"), n.get("type", ""), n.get("subtype", ""),
            n.get("name_zh", ""), n.get("name_en", ""), n.get("level", ""),
            n.get("faction", ""), xy, tuple(n.get("adjacent") or []),
            n.get("look_zh", ""), n.get("verified_by", ""))
    kids: dict[str, list[str]] = {}
    for n in nodes.values():
        if n.parent:
            kids.setdefault(n.parent, []).append(n.nid)
    return nodes, kids


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def parchment(w: int, h: int, seed: int) -> Image.Image:
    """程序化羊皮纸：底色 + 多尺度噪声 + 四边烧灼感。"""
    rnd = random.Random(seed)
    base = Image.new("RGB", (w, h), PARCHMENT)
    for scale, amp in ((6, 16), (24, 11), (96, 7)):
        sw, sh = max(2, w // scale), max(2, h // scale)
        noise = Image.new("L", (sw, sh))
        noise.putdata([128 + rnd.randint(-amp, amp) for _ in range(sw * sh)])
        noise = noise.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))
        base = Image.blend(base, Image.merge("RGB", (noise, noise, noise)), 0.10)
    # 四边由外向内的暖褐渐暗（烧灼/老化）
    vig = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vig)
    edge = int(min(w, h) * 0.16)
    for i in range(edge):
        v = int(150 * (1 - i / edge) ** 2)
        vd.rectangle([i, i, w - 1 - i, h - 1 - i], outline=v)
    burn = Image.new("RGB", (w, h), (120, 88, 50))
    base = Image.composite(burn, base, vig.filter(ImageFilter.GaussianBlur(edge / 3)))
    return base


def frame(d: ImageDraw.ImageDraw, w: int, h: int) -> None:
    d.rectangle([14, 14, w - 15, h - 15], outline=INK, width=5)
    d.rectangle([26, 26, w - 27, h - 27], outline=GOLD, width=2)
    for cx, cy in ((26, 26), (w - 27, 26), (26, h - 27), (w - 27, h - 27)):
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=GOLD, outline=INK, width=2)


def cartouche(img: Image.Image, d: ImageDraw.ImageDraw, w: int, title: str, sub: str) -> None:
    f1, f2 = font(F_UI, 44), font(F_UI, 20)
    tw = d.textlength(title, font=f1)
    bx0, bx1 = w / 2 - tw / 2 - 46, w / 2 + tw / 2 + 46
    d.rounded_rectangle([bx0, 40, bx1, 118], radius=10, fill=(198, 172, 128), outline=INK, width=3)
    d.rounded_rectangle([bx0 + 7, 47, bx1 - 7, 111], radius=7, outline=GOLD, width=1)
    d.text((w / 2, 66), title, font=f1, fill=INK, anchor="mm")
    d.text((w / 2, 100), sub, font=f2, fill=INK_SOFT, anchor="mm")


def marker(d: ImageDraw.ImageDraw, x: float, y: float, kind: str, r: int, col: tuple[int, int, int]) -> None:
    if kind == "dot":
        d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=INK, width=2)
    elif kind == "square":
        d.rectangle([x - r, y - r, x + r, y + r], fill=col, outline=INK, width=2)
    elif kind == "house":
        d.rectangle([x - r, y - r * 0.3, x + r, y + r], fill=col, outline=INK, width=2)
        d.polygon([(x - r * 1.25, y - r * 0.3), (x, y - r * 1.4), (x + r * 1.25, y - r * 0.3)],
                  fill=col, outline=INK)
    elif kind == "keep":  # 主城：带雉堞的方塔
        d.rectangle([x - r, y - r * 0.55, x + r, y + r], fill=col, outline=INK, width=3)
        step = r * 2 / 5
        for i in range(3):
            bx = x - r + step * (i * 2)
            d.rectangle([bx, y - r * 1.15, bx + step, y - r * 0.55], fill=col, outline=INK, width=2)
    elif kind == "arch":  # 副本：拱门
        d.arc([x - r, y - r, x + r, y + r * 0.9], 180, 360, fill=INK, width=4)
        d.line([x - r, y + r * 0.9, x - r, y], fill=INK, width=4)
        d.line([x + r, y + r * 0.9, x + r, y], fill=INK, width=4)
        d.ellipse([x - r * 0.3, y - r * 0.15, x + r * 0.3, y + r * 0.45], fill=ACCENT)
    elif kind == "cross":
        d.line([x - r, y - r, x + r, y + r], fill=ACCENT, width=4)
        d.line([x - r, y + r, x + r, y - r], fill=ACCENT, width=4)
    elif kind == "wing":  # 飞行点
        d.arc([x - r * 1.6, y - r, x, y + r], 300, 60, fill=INK, width=3)
        d.arc([x, y - r, x + r * 1.6, y + r], 120, 240, fill=INK, width=3)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=INK)


def halo_text(img: Image.Image, d: ImageDraw.ImageDraw, xy: tuple[float, float], s: str,
              f: ImageFont.FreeTypeFont, fill: tuple[int, int, int], anchor: str = "lm") -> None:
    """给标注描一圈羊皮纸色的光晕，压住底纹保证可读。"""
    x, y = xy
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)):
        d.text((x + dx, y + dy), s, font=f, fill=(226, 206, 172), anchor=anchor)
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def place_labels(d: ImageDraw.ImageDraw, pts: list[tuple[float, float, str, int]],
                 w: int, h: int) -> list[tuple[float, float, str, str, int]]:
    """贪心避让：每个点试八个方位，挑不与已放标签重叠的那个；放不下就丢掉标签（点仍在）。

    **宽度必须用 `textlength` 实测**——初版用 `len(s) * size * 0.62` 估，
    那是拉丁字母的比例；中文字宽≈字号，于是每个框都比真实小 40%，
    重叠检测形同虚设，闪金镇那一簇当场糊成一团。
    """
    taken: list[tuple[float, float, float, float]] = []
    out = []
    for x, y, s, size in sorted(pts, key=lambda p: p[3]):
        f = font(F_LABEL, size)
        tw, th = d.textlength(s, font=f) + 6, size * 1.2
        for dx, dy, anc in ((14, 0, "lm"), (-14, 0, "rm"), (0, -16, "md"), (0, 17, "ma"),
                            (12, -13, "lm"), (-12, -13, "rm"), (12, 14, "lm"), (-12, 14, "rm")):
            lx, ly = x + dx, y + dy
            x0 = lx if anc == "lm" else (lx - tw if anc == "rm" else lx - tw / 2)
            y0 = ly - th / 2
            box = (x0, y0, x0 + tw, y0 + th)
            if box[0] < 34 or box[2] > w - 34 or box[1] < 130 or box[3] > h - 96:
                continue
            if any(not (box[2] < t[0] or box[0] > t[2] or box[3] < t[1] or box[1] > t[3]) for t in taken):
                continue
            taken.append(box)
            out.append((lx, ly, s, anc, size))
            break
    return out


def legend(d: ImageDraw.ImageDraw, w: int, h: int, items: list[tuple[str, str]]) -> None:
    f = font(F_UI, 17)
    bw, bh = 196, 30 + len(items) * 27
    x0, y0 = w - bw - 40, h - bh - 46
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=8, fill=(204, 180, 138), outline=INK, width=2)
    for i, (kind, name) in enumerate(items):
        cy = y0 + 26 + i * 27
        marker(d, x0 + 26, cy, kind, 7, (198, 172, 128))
        d.text((x0 + 50, cy), name, font=f, fill=INK, anchor="lm")


def footer(d: ImageDraw.ImageDraw, w: int, h: int, note: str) -> None:
    d.text((40, h - 46), note, font=font(F_UI, 15), fill=INK_SOFT, anchor="lm")


def zone_of(nodes: dict[str, Node], nid: str) -> str | None:
    cur = nodes[nid].parent
    while cur and cur in nodes:
        if nodes[cur].ntype in ("zone", "city"):
            return cur
        cur = nodes[cur].parent
    return None


def render_zone(nodes: dict[str, Node], kids: dict[str, list[str]], zid: str, min_pts: int) -> str | None:
    z = nodes[zid]
    members = [n for n in nodes.values() if zone_of(nodes, n.nid) == zid and n.xy]
    if z.xy:
        members.append(z)
    if len(members) < min_pts:
        return None

    W, H = 1600, 1180
    img = parchment(W, H, seed=abs(hash(zid)) % 9999)
    d = ImageDraw.Draw(img)

    # 绘图区：把 0–100 的地图百分比映射进来
    m_l, m_t, m_r, m_b = 70, 138, 70, 104
    pw, ph = W - m_l - m_r, H - m_t - m_b
    def px(c: tuple[float, float]) -> tuple[float, float]:
        return m_l + c[0] / 100 * pw, m_t + c[1] / 100 * ph

    d.rectangle([m_l, m_t, W - m_r, H - m_b], outline=(150, 124, 86), width=2)
    for i in range(1, 10):  # 极淡的十分格，只为读坐标
        gx, gy = m_l + pw * i / 10, m_t + ph * i / 10
        d.line([gx, m_t, gx, H - m_b], fill=(198, 176, 140), width=1)
        d.line([m_l, gy, W - m_r, gy], fill=(198, 176, 140), width=1)

    labels = []
    for n in members:
        kind, r, lab, sz = STYLE.get(n.ntype, ("dot", 4, True, 2))
        x, y = px(n.xy)
        col = FACTION_TINT.get(n.faction or z.faction, (198, 172, 128))
        col = tuple(int(c * 0.35 + 198 * 0.65) for c in col)
        marker(d, x, y, kind, r, col)
        if lab and n.zh:
            labels.append((x, y, n.zh, (19, 17, 15)[sz]))
    for lx, ly, s, anc, size in place_labels(d, labels, W, H):
        halo_text(img, d, (lx, ly), s, font(F_LABEL, size), INK, anc)

    frame(d, W, H)
    lvl = f"  ·  {z.level} 级" if z.level else ""
    fac = {"alliance": "联盟", "horde": "部落", "contested": "争夺", "neutral": "中立"}.get(z.faction, "")
    cartouche(img, d, W, z.zh, f"{z.en}{lvl}{('  ·  ' + fac) if fac else ''}  ·  {len(members)} 个点位")
    legend(d, W, H, [("keep", "主城"), ("house", "聚居点"), ("arch", "副本"), ("dot", "子区域 / 地标"), ("wing", "飞行点")])
    footer(d, W, H,
           f"点位＝游戏内地图百分比坐标（x 左→右 / y 上→下）· 共 {len(members)} 点 · "
           f"由 tools/render_wow_maps.py 从 world_tree.json 生成，不要手改")

    os.makedirs(os.path.join(OUT, "zones"), exist_ok=True)
    p = os.path.join(OUT, "zones", zid + ".png")
    img.save(p)
    return p


REGION_ORDER = {
    "eastern_kingdoms": ["quel_thalas", "lordaeron", "khaz_modan", "kingdom_of_stormwind",
                         "azeroth_continent", "stranglethorn"],
    "kalimdor": ["northern_kalimdor", "central_kalimdor", "southern_kalimdor"],
}


def render_continent(nodes: dict[str, Node], kids: dict[str, list[str]], cid: str) -> str | None:
    if cid not in nodes:
        return None
    # 收集该大陆下所有 zone/city，按「直接拥有它的分区」归组
    groups: list[tuple[str, list[Node]]] = []

    def walk(rid: str) -> None:
        own = [nodes[k] for k in kids.get(rid, []) if nodes[k].ntype in ("zone", "city")]
        if own:
            groups.append((nodes[rid].zh or rid, own))
        for k in kids.get(rid, []):
            if nodes[k].ntype == "region":
                walk(k)

    walk(cid)
    if not groups:
        return None

    W = 1700
    rows = sum(math.ceil(len(g[1]) / 4) for g in groups)
    H = 230 + rows * 128 + len(groups) * 46
    img = parchment(W, H, seed=abs(hash(cid)) % 9999)
    d = ImageDraw.Draw(img)

    pos: dict[str, tuple[float, float]] = {}
    y = 176
    f_reg, f_z, f_en = font(F_UI, 23), font(F_LABEL, 24), font(F_UI, 14)
    for rname, zs in groups:
        d.line([60, y, W - 60, y], fill=(168, 142, 104), width=2)
        halo_text(img, d, (66, y - 17), rname, f_reg, ACCENT, "lm")
        y += 26
        for i, z in enumerate(sorted(zs, key=lambda n: (n.level or "zz"))):
            col, row = i % 4, i // 4
            cx, cy = 150 + col * ((W - 300) / 3), y + row * 128 + 44
            pos[z.nid] = (cx, cy)
            kind = "keep" if z.ntype == "city" else "house"
            tint = FACTION_TINT.get(z.faction, (96, 84, 56))
            marker(d, cx, cy, kind, 15, tuple(int(c * 0.3 + 198 * 0.7) for c in tint))
            halo_text(img, d, (cx, cy + 34), z.zh, f_z, INK, "ma")
            tag = z.level or ({"alliance": "联盟", "horde": "部落"}.get(z.faction, ""))
            if tag:
                halo_text(img, d, (cx, cy + 62), tag, f_en, INK_SOFT, "ma")
        y += math.ceil(len(zs) / 4) * 128 + 20

    # 邻接连线（画在标记之间，细虚线感）
    drawn = set()
    for z in nodes.values():
        if z.nid not in pos:
            continue
        for a in z.adjacent:
            if a in pos and (a, z.nid) not in drawn:
                drawn.add((z.nid, a))
                x1, y1 = pos[z.nid]
                x2, y2 = pos[a]
                steps = max(6, int(math.hypot(x2 - x1, y2 - y1) / 14))
                for s in range(0, steps, 2):
                    t0, t1 = s / steps, min(1.0, (s + 1) / steps)
                    d.line([x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0,
                            x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1], fill=(150, 124, 86), width=2)

    frame(d, W, H)
    cartouche(img, d, W, nodes[cid].zh, f"{nodes[cid].en}  ·  {len(pos)} 个地区与主城  ·  按 lore 分区排列")
    footer(d, W, H,
           "⚠ 本图为**示意**：树里没有地区的多边形与大陆坐标，故按 lore 分区分组、虚线表示接壤，"
           "**不是地理精确的位置**。精确点位见 zones/ 下各单区图。")
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, cid + ".png")
    img.save(p)
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zone")
    ap.add_argument("--min-points", type=int, default=5)
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    nodes, kids = load()
    os.makedirs(OUT, exist_ok=True)

    targets = [args.zone] if args.zone else [n.nid for n in nodes.values() if n.ntype in ("zone", "city")]
    made, skipped = [], []
    for zid in sorted(targets):
        if zid not in nodes:
            print("没有这个区：", zid)
            return 1
        p = render_zone(nodes, kids, zid, args.min_points)
        (made if p else skipped).append(zid)
        if p:
            print(f"  ✔ {nodes[zid].zh:<14} → {os.path.relpath(p, REPO)}")

    if not args.zone:
        for cid in ("eastern_kingdoms", "kalimdor"):
            p = render_continent(nodes, kids, cid)
            if p:
                print(f"  ✔ {nodes[cid].zh:<14} → {os.path.relpath(p, REPO)}")

    print(f"\n出图 {len(made)} 张单区图；{len(skipped)} 个区坐标不足 {args.min_points} 点、跳过。")
    if skipped:
        print("  坐标不足的区：" + "、".join(nodes[z].zh for z in skipped[:18]) +
              ("…" if len(skipped) > 18 else ""))
        print("  —— 补坐标就能出图：去 map/g*.yaml 填 `coords: \"[x, y]\"`（游戏内地图百分比），重跑本脚本。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
