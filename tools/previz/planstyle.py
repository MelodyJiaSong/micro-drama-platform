# -*- coding: utf-8 -*-
"""俯视平面图的共用画法 —— 一套图面规范只有一处定义。

背景（2026-09-22 用户定调「统一 flight plan 的规范」）：同一族俯视图长期是两套视觉语言 ——
`shot_plan.py` 的航线图（米白底 / 细北针 / 左上标题 / 单段比例尺）与 `build_floorplan.py`
的场地图（深褐画布 / 红圆章北针 / 居中大标题 / 分段比例尺 / 底部色块图例）。
两者回答的问题不同（rule 4j：一个答「镜头怎么走」，一个答「这地方有什么」），
**但画出来应当像同一套图** —— 否则读图的人每换一张就要重新建立一次视觉索引，
而这些图存在的全部理由就是「读图比读散文快两个数量级」。

本模块是图面规范的**唯一出处**：配色 / 字体 / 标题块 / 北针 / 比例尺 / 图例 / 光晕文字。
改规范 ＝ 改本文件，两个工具一起变；任何一方自己再写一份字面量，就是 CLAUDE.md
「一个名字只有一处定义」说的那种静默漂移。

**名字不在本模块的管辖内**（rule 4j 已定）：机位在世界里飞的叫航线图 flight plan
（`{shot}_flightplan.png`），地面镜的机位与走位叫走位平面图 ground plan
（`{shot}_groundplan.png`），场景的场地布局叫 floor plan（`{bg}_floorplan.png`）——
最后这个保留 floor plan 一词是对的：它在影视工业里本来就指室内 / 场地平面图，
rule 4j 退役的是「拿它称呼一条一公里多的空中航线」那种用法。
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import ImageDraw, ImageFont

# ── 配色 ──────────────────────────────────────────────────────────────────
# 统一走米白纸底：比深褐画布更接近真实的工程图，打印与投屏都不糊，
# 也让红色航线与蓝色水系在同一张图上保持同样的对比度。
PAPER = (250, 248, 243)
INK = (34, 34, 34)
MUTED = (140, 140, 140)
SOFT = (120, 108, 90)

WATER = (120, 176, 196)
WATER_FILL = (198, 226, 232)
WALL = (156, 132, 100)
WALL_FILL = (238, 230, 214)
STREET = (198, 190, 176)
ROAD = (198, 176, 138)
GRASS = (214, 222, 190)
ROCK = (196, 188, 170)
GRID = (226, 221, 211)

ACCENT = (208, 62, 44)           # 航线 / 主体线：全族共用的唯一强调色
ACCENT_GHOST = (232, 168, 158)
PANEL_BG = (243, 240, 233)
HALO_BG = (246, 243, 236)
LABEL_BG = (255, 255, 255, 216)
LEG_LABEL_BG = (255, 255, 255, 232)

# bg 归属键：青色自成一档，与建筑名（墨色）分开——一眼能扫出哪些块已有主体卡。
# 没有键的块显式写「无专属 bg」而不是留白：留白读者要问一次「是漏标还是本来就没有」，
# 而这张图的下游用途之一正是「哪些反复入画的建筑还欠一张主体卡」（rule 4j ④）。
BG_KEY = (26, 116, 140)
BG_KEY_BG = (214, 236, 242, 236)
BG_NONE = (150, 146, 138)

# 来源分档（场地图用）。颜色取自同一张色盘，不另起一套。
SRC_STYLE = {
    "原典方位": INK,
    "坐标表": (70, 90, 130),
    "地图量取": (60, 110, 80),
    "推定": ACCENT,
}

MARGIN = 130

# ── 字体 ──────────────────────────────────────────────────────────────────
# 按候选名查找，不写死 C:/Windows/Fonts 下的某一个文件：换机器 / 换系统时
# 硬编码路径会直接抛 OSError，而平面图是「随时重跑」的产物。
_FONT_DIRS = (Path("C:/Windows/Fonts"), Path("/usr/share/fonts"), Path("/Library/Fonts"))
_REGULAR = ("msyh.ttc", "simhei.ttf", "simsun.ttc", "msjh.ttc", "NotoSansCJK-Regular.ttc")
_BOLD = ("msyhbd.ttc", "simhei.ttf", *_REGULAR)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for name in (_BOLD if bold else _REGULAR):
        for d in _FONT_DIRS:
            p = d / name
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


# ── 文字 ──────────────────────────────────────────────────────────────────
def halo(d: ImageDraw.ImageDraw, xy, text: str, f, fill=INK, anchor: str = "mm") -> None:
    """描边文字。图上标签压在地块 / 水系上时，没有描边一律读不出来。"""
    x, y = xy
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)):
        d.text((x + dx, y + dy), text, font=f, fill=HALO_BG, anchor=anchor)
    d.text((x, y), text, font=f, fill=fill, anchor=anchor)


# ── 图面构件 ───────────────────────────────────────────────────────────────
def title_block(d: ImageDraw.ImageDraw, x: int, y: int, title: str,
                subtitle: str = "", hint: str = "") -> None:
    """左上角标题块。统一靠左，不居中——右侧要留给侧栏，居中标题会和侧栏打架。"""
    d.text((x, y), title, font=font(46, bold=True), fill=INK)
    if subtitle:
        d.text((x, y + 62), subtitle, font=font(21), fill=MUTED)
    if hint:
        d.text((x, y + 96), hint, font=font(19), fill=MUTED)


def north_arrow(d: ImageDraw.ImageDraw, x: int, y: int, size: int = 74) -> None:
    """细箭头 + N。不用红三角圆章：那是地图装饰，会和强调色抢注意力。"""
    d.line((x, y + size, x, y), fill=INK, width=5)
    d.polygon([(x, y - 16), (x - 13, y + 8), (x + 13, y + 8)], fill=INK)
    d.text((x, y + size + 8), "N", font=font(24), fill=INK, anchor="mt")


def nice_span(raw: float) -> float:
    """把任意长度收成 1 / 2 / 5 × 10^n 的整值——比例尺上只出现好读的数。"""
    e = 10 ** math.floor(math.log10(max(raw, 1e-6)))
    for m in (1, 2, 5, 10):
        if raw <= m * e:
            return m * e
    return 10 * e


def scale_bar(d: ImageDraw.ImageDraw, x: int, y: int, px_per_m: float,
              meters: float | None = None, segments: int = 5) -> None:
    """分段刻度比例尺。分段比单段好读——不用拿尺子换算就能估中间距离。"""
    if meters is None:
        meters = nice_span(220 / px_per_m)
    bar = meters * px_per_m
    d.line((x, y, x + bar, y), fill=INK, width=5)
    for i in range(segments + 1):
        tx = x + bar * i / segments
        d.line((tx, y - 11, tx, y + 11), fill=INK, width=3 if i % segments else 5)
    halo(d, (x + bar / 2, y - 26), f"{meters:g} m", font(22), INK, "mm")


def legend_row(d: ImageDraw.ImageDraw, x: int, y: int, items, box: int = 18) -> None:
    """底部色块图例。比把图例塞进副标题好——副标题那一行读者只会扫一次。"""
    f = font(18)
    for text, col in items:
        d.rectangle([x, y, x + box, y + box], outline=col, width=3)
        halo(d, (x + box + 10, y + box / 2), text, f, SOFT, "lm")
        x += box + 10 + d.textlength(text, font=f) + 30


def footer(d: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    halo(d, (x, y), text, font(17), MUTED, "lm")


# ── 编号索引栏 ─────────────────────────────────────────────────────────────
# 2026-09-22 用户定调：「一张图看到整个 X 有多少个建筑、布局在哪里、大概的面积对比」。
# 把名字写在方块上只在十几个块时成立；到了城区尺度（暴风城光 POI 就近百个）必然叠成一团。
# 解法是**图上只留编号、名字进侧栏**，侧栏同时承载面积条——面积对比靠眼睛比读数字快得多。
ROW_H = 46
BADGE_R = 13


def badge(d: ImageDraw.ImageDraw, x: float, y: float, no: int, col, r: int = BADGE_R) -> None:
    """编号圆牌。实心填充 + 白字：压在任何底色的方块上都读得出。"""
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=PAPER, width=2)
    d.text((x, y + 1), str(no), font=font(int(r * 1.25), bold=True), fill=PAPER, anchor="mm")


def index_panel_height(n: int, title: bool = True) -> int:
    return (54 if title else 0) + n * ROW_H


def index_panel(d: ImageDraw.ImageDraw, x: int, y: int, w: int, rows,
                title: str = "编号索引 · 按面积降序") -> int:
    """右侧编号索引栏。`rows` = (no, name, dims_text, area_m2, color, bg_key) 的序列。

    **面积条按本栏最大值归一**——它回答的是「这些东西彼此差多少倍」，不是绝对面积；
    绝对值就写在条子左边，两者各管各的。排序由调用方决定（默认面积降序，
    这样条子单调递减，一眼就是面积对比图）。

    `bg_key` 是该块的 **bg 归属键**（`bg2` / `bg17` …），空字符串表示还没有主体卡。
    两种情形都显式写出来：有键的写键，没键的写「无专属 bg」——**留白会让读者
    分不清「漏标」与「本来就没有」**，而这张图的下游用途之一正是盘点缺口。
    """
    rows = list(rows)
    if not rows:
        return 0
    y0 = y
    if title:
        d.text((x, y), title, font=font(22, bold=True), fill=INK)
        d.line((x, y + 34, x + w, y + 34), fill=GRID, width=2)
        y += 54

    peak = max(r[3] for r in rows) or 1.0
    bar_w = max(70, int(w * 0.3))
    bar_x = x + w - bar_w
    f_key = font(15, bold=True)

    for row in rows:
        no, name, dims, area, col = row[:5]
        key = (row[5] if len(row) > 5 else "") or ""
        badge(d, x + BADGE_R, y + 15, no, col)
        tx = x + BADGE_R * 2 + 10
        if key:
            d.text((tx, y + 6), key, font=f_key, fill=BG_KEY)
            tx += d.textlength(key, font=f_key) + 8
        d.text((tx, y + 4), name, font=font(19), fill=INK)
        tail = f"{dims}   {area:,.0f} m²" if key else f"{dims}   {area:,.0f} m²   无专属 bg"
        d.text((x + BADGE_R * 2 + 10, y + 25), tail,
               font=font(15), fill=MUTED if key else BG_NONE)
        # 面积条
        d.rectangle([bar_x, y + 12, bar_x + bar_w, y + 24], fill=PANEL_BG)
        run = max(2, int(bar_w * area / peak))
        d.rectangle([bar_x, y + 12, bar_x + run, y + 24],
                    fill=(col[0], col[1], col[2], 150))
        y += ROW_H

    return y - y0
