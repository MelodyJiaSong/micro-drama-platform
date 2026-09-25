# -*- coding: utf-8 -*-
"""场景俯视布局图（floor plan）—— 把「一张画」变成「一组有坐标、有尺寸的东西」。

用法（仓库根目录）：
    python tools/build_floorplan.py ai_videos/shengji_zhilu/2_世界观人设/scenes/eastern_kingdoms/elwynn_forest/bg1_北郡山谷
    python tools/build_floorplan.py <scene 目录> --check     # 只机检，不写盘

输入：`{scene}/planning/blocks.toml` —— **本场景的几何唯一出处**。
产物（同目录）：
    {bg}_floorplan.png   俯视图：地面 + 水系 + 道路 + 建筑组方块 + 朝向 + 比例尺
    {bg}_blocks.md       同一批数字的表（名字 / 位置 / 尺寸 / 朝向 / 来源 / 是否建 prop）

## 它和 `shot_plan.py`（原 `shot_floorplan.py`）的分工

| | `shot_plan.py`（rule 4j） | 本工具 |
|---|---|---|
| 回答 | **镜头怎么走**（航线、航点、离地物多远） | **这个地方有什么**（有哪些东西、各在哪、多大） |
| 输入 | `previz_config.toml` 的 `[[机位]]` | `blocks.toml` |
| 下游 | previz 的机位关键帧 | **props 卡 与 .blend 建模** |

两者共用同一套世界坐标，**但产物不同，不要互相替代**。

## 三条硬约束

1. **几何只有一个出处**（rule 4i ①）：位置与尺寸只写在 `blocks.toml`；图与表都是派生。
   改布局 ＝ 改 toml 重跑，**不手改 PNG、不手改 md**。
2. **每个 block 必须写 `src`（来源）**——`原典方位` / `坐标表` / `地图量取` / `推定`。
   **`推定` 的块在图上画成虚线**，让看图的人一眼分清「有据」与「我编的」。
3. **本图是示意，不是几何真相**：真几何在 `.blend`。方块只回答「有什么、在哪、多大」。
"""
from __future__ import annotations

import argparse
import io
import math
import os
import re
import sys
import tomllib

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.previz import planschema  # noqa: E402
from tools.previz.planstyle import (  # noqa: E402
    BG_KEY, BG_NONE, GRASS, GRID, INK, PAPER, ROAD, ROCK, SOFT, SRC_STYLE, WATER,
    BADGE_R, badge, font, halo, index_panel, index_panel_height,
    legend_row, footer, north_arrow, scale_bar, title_block,
)

GUESS = SRC_STYLE["推定"]

# 超过这个块数就不在图上写名字了，只留编号、名字进侧栏（planstyle 编号索引栏的注释解释了为什么）。
# 十几个块时内嵌名字更好读，所以默认 auto；`[meta] label_mode` 可显式写死 "inline" / "number"。
DENSE_N = 15


def numbered(cfg: dict) -> list[tuple[int, dict, float]]:
    """按面积降序编号。

    降序而非空间顺序，是因为这套图要回答的问题里有一条是「大概的面积对比」——
    编号跟着面积走，侧栏的面积条就单调递减，整栏本身即是一张面积对比图。
    面积一律按 `size` 的外接矩形算，与 `rot` 无关（旋转不改变面积）。
    """
    items = [(b, b["size"][0] * b["size"][1]) for b in cfg.get("block", [])]
    items.sort(key=lambda q: -q[1])
    return [(i + 1, b, a) for i, (b, a) in enumerate(items)]


def load(scene: str) -> tuple[dict, str]:
    p = os.path.join(scene, "planning", "blocks.toml")
    if not os.path.exists(p):
        raise SystemExit(f"没有 {p} —— 这是本场景几何的唯一出处，先写它")
    with open(p, "rb") as fh:
        return tomllib.load(fh), p


def bg_dirs(scene: str) -> dict[str, str]:
    """兄弟目录里所有 `bg{N}_{名}` → 键。bg 归属键必须指向一个**真实存在的主体目录**。"""
    parent = os.path.dirname(os.path.abspath(scene))
    out: dict[str, str] = {}
    for n in os.listdir(parent):
        if os.path.isdir(os.path.join(parent, n)) and re.match(r"^bg\d+_", n):
            out[n.split("_", 1)[0]] = n
    return out


def check(cfg: dict, scene: str) -> list[str]:
    """schema 判据住在 `tools/previz/planschema.py`（bpy-free，与场景引擎共用同一份）。

    本函数只是薄壳：**判据不许在这里再写一遍**，否则平面图与 `.blend` 会对同一份 toml
    给出两套「合格」的定义，而两边都不会报错（CLAUDE.md § 一个名字只有一处定义）。
    """
    return planschema.check(cfg, scene, known_bg=bg_dirs(scene))


def own_key(b: dict, meta: dict) -> str:
    """块归哪个 bg 主体卡。**没写就归本图自己**——详图里的每一块本来就是这张卡的组成部分，
    逼作者把 `bg = "bg2"` 抄 13 遍只会制造副本。显式写了、且与本图不同的才印出来
    （那是「这块地另有主人，去看那张卡」）。"""
    k = (b.get("bg") or "").strip()
    return "" if not k or k == meta.get("bg") else k


def draw_site(d: ImageDraw.ImageDraw, cfg: dict, P, PX: float, W: int, H: int, inline: bool) -> None:
    """场地本身：地面 / 山 / 水 / 路 / 网格 / 建筑组方块 / 名字 / 圆牌。
    场地平面图与镜头平面图（`tools/shot_overhead.py`）共用这一份画法——两张图的底子不许各画各的。"""
    meta = cfg["meta"]
    Wm, Hm = meta["size_m"]
    rows = numbered(cfg)
    # 地面
    d.rectangle([P(0, 0), P(Wm, Hm)], fill=GRASS)
    # 山体（围合）
    for r in cfg.get("ridge", []):
        pts = [P(*p) for p in r["poly"]]
        d.polygon(pts, fill=ROCK)
        for i in range(0, len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(120, 108, 92), width=2)
    # 水系
    for w in cfg.get("water", []):
        pts = [P(*p) for p in w["path"]]
        d.line(pts, fill=WATER, width=int(w.get("width_m", 6) * PX), joint="curve")
    # 道路
    road_boxes: list[tuple[float, float, float, float]] = []
    for r in cfg.get("road", []):
        pts = [P(*p) for p in r["path"]]
        d.line(pts, fill=ROAD, width=int(r.get("width_m", 4) * PX), joint="curve")
        if r.get("name"):
            mx, my = pts[len(pts) // 2]
            halo(d, (mx, my - 14), r["name"], font(19), SOFT)
            rw = d.textlength(r["name"], font=font(19))
            road_boxes.append((mx - rw / 2, my - 32, mx + rw / 2, my + 4))
    # 山 / 水 / 路只画在场地框里：多边形与宽线会伸出框外（实测 bg186 的湖面盖到了左边距），
    # 把四条边距刷回纸色。标题 / 索引 / 图例都在后面才画，不受影响。
    x0, y0 = P(0, 0)
    x1, y1 = P(Wm, Hm)
    for bx0, by0, bx1, by1 in ((0, 0, W, y0), (0, y1, W, H), (0, y0, x0, y1), (x1, y0, W, y1)):
        # 镜头平面图会把视野裁在场地内部，场地边就落到画布外——钳进画布，空矩形跳过
        bx0, bx1 = max(0, bx0), min(W, bx1)
        by0, by1 = max(0, by0), min(H, by1)
        if bx1 > bx0 and by1 > by0:
            d.rectangle((bx0, by0, bx1, by1), fill=PAPER)
    # 网格（默认 20 m；整区级的图写 `[meta] grid_m = 200`，否则 3 km 的场地上 20 m 网格是一片噪声）
    grid = int(meta.get("grid_m", 20))
    for gx in range(0, int(Wm) + 1, grid):
        d.line([P(gx, 0), P(gx, Hm)], fill=GRID, width=1)
    for gy in range(0, int(Hm) + 1, grid):
        d.line([P(0, gy), P(Wm, gy)], fill=GRID, width=1)
    d.rectangle([P(0, 0), P(Wm, Hm)], outline=INK, width=3)

    # 建筑组方块
    f_b, f_s = font(20), font(15)
    pending: list[tuple[float, float, str, str, float]] = []
    badges: list[tuple[float, float, int, tuple]] = []
    for no, b, area in rows:
        x, y = b["xy"]
        sx, sy = b["size"]
        rot = b.get("rot", 0)
        col = SRC_STYLE[b["src"]]
        cx, cy = P(x, y)
        hw, hh = sx * PX / 2, sy * PX / 2
        cs, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        corners = [(cx + (dx * cs - dy * sn), cy + (dx * sn + dy * cs))
                   for dx, dy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
        # 填充深浅 ＝ 高度。**主厅 h=15 和内院空场 h=0 以前渲成同一个灰盒子**，
        # 而 h_m 是航线图唯一算不出来的那个数（今天它靠开一次 Blender 射线扫描 90 秒、
        # 再手抄成 `alt_floor=((340.0, 75.0, 9.5),)`，屋顶一改就过期且没人知道）。
        h_m = float(b.get("h_m", 0) or 0)
        if h_m <= 0:            # 贴地板块（草坪 / 石板地 / 空场）：只描边，画斜线示意
            d.polygon(corners, fill=(col[0], col[1], col[2], 18))
            x0 = min(p[0] for p in corners)
            x1 = max(p[0] for p in corners)
            y0 = min(p[1] for p in corners)
            y1 = max(p[1] for p in corners)
            step = 13
            for k in range(int((x1 - x0 + y1 - y0) / step) + 1):
                ax, ay = x0 + k * step, y0
                bx2, by2 = x0, y0 + k * step
                if ax > x1:
                    ay, ax = ay + (ax - x1), x1
                if by2 > y1:
                    bx2, by2 = bx2 + (by2 - y1), y1
                d.line([ax, ay, bx2, by2], fill=(col[0], col[1], col[2], 46), width=1)
        else:
            a = 46 + int(min(h_m, 20.0) / 20.0 * 104)   # 0–20 m 映射到 46–150
            d.polygon(corners, fill=(col[0], col[1], col[2], a))
        for i in range(4):
            a, bb = corners[i], corners[(i + 1) % 4]
            if b["src"] == "推定":  # 推定＝虚线，一眼分清有据与我编的
                n = max(4, int(math.dist(a, bb) / 9))
                for s in range(0, n, 2):
                    t0, t1 = s / n, min(1.0, (s + 1) / n)
                    d.line([a[0] + (bb[0] - a[0]) * t0, a[1] + (bb[1] - a[1]) * t0,
                            a[0] + (bb[0] - a[0]) * t1, a[1] + (bb[1] - a[1]) * t1], fill=col, width=2)
            else:
                d.line([a, bb], fill=col, width=3)
        # 编号圆牌钉在方块左上角（跟着 rot 一起转）。**够大才往里钉**——
        # 圆牌比小块还宽时往里钉会整个盖住块和它的名字（祭台 3.2×1.6 m 就是这种），
        # 所以小块一律钉到角外，宁可占一点空地也不遮内容。
        diag = math.hypot(hw, hh) or 1.0
        t = (BADGE_R + 9) / diag if diag >= BADGE_R * 2 + 14 else -(BADGE_R + 6) / diag
        badges.append((corners[0][0] + (cx - corners[0][0]) * t,
                       corners[0][1] + (cy - corners[0][1]) * t, no, col))
        # 稀疏图才在方块上写名字；密集图 pending 为空，下面的避让循环自然空转
        if inline:
            key = own_key(b, meta)
            pending.append((cx, cy, f"{key} {b['name']}" if key else b["name"],
                            f"{sx:g}×{sy:g}m h{h_m:g}" + ("  ▣prop" if b.get("make_prop") else ""),
                            max(hw, hh), bool(key)))

    # 标签统一避让后再画——建筑组密集处（修道院那一簇）不避让必糊成一团
    # 圆牌先占位：标签避让必须把圆牌算进去，否则小块的名字会被它自己的编号盖住
    taken: list[tuple[float, float, float, float]] = [
        (bx - BADGE_R - 3, by - BADGE_R - 3, bx + BADGE_R + 3, by + BADGE_R + 3)
        for bx, by, _, _ in badges
    ] + road_boxes
    for cx, cy, nm, tag, rad, has_key in sorted(pending, key=lambda q: -q[4]):
        tw = max(d.textlength(nm, font=f_b), d.textlength(tag, font=f_s)) + 10
        th = 42
        for dx, dy in ((0, 0), (0, -rad - 26), (0, rad + 26), (-rad - tw / 2 - 8, 0),
                       (rad + tw / 2 + 8, 0), (0, -rad - 54), (0, rad + 54),
                       (-rad - tw / 2 - 8, -rad - 30), (rad + tw / 2 + 8, -rad - 30),
                       (-rad - tw / 2 - 8, rad + 30), (rad + tw / 2 + 8, rad + 30),
                       (0, -rad - 84), (0, rad + 84)):
            box = (cx + dx - tw / 2, cy + dy - th / 2, cx + dx + tw / 2, cy + dy + th / 2)
            if any(not (box[2] < q[0] or box[0] > q[2] or box[3] < q[1] or box[1] > q[3]) for q in taken):
                continue
            taken.append(box)
            if dx or dy:  # 挪开了就拉一根细引线回到方块
                d.line([cx, cy, cx + dx, cy + dy], fill=SOFT, width=1)
            halo(d, (cx + dx, cy + dy - 10), nm, f_b, BG_KEY if has_key else INK)
            halo(d, (cx + dx, cy + dy + 12),
                 tag if has_key else tag, f_s,
                 SOFT if has_key else BG_NONE)
            break

    # 编号圆牌最后画、压在标签之上——它是查图的索引锚点，被任何东西盖住这张图就查不了
    for bx, by, no, col in badges:
        badge(d, bx, by, no, col)



def render(cfg: dict, scene: str) -> str:
    meta = cfg["meta"]
    Wm, Hm = meta["size_m"]
    PX = meta.get("px_per_m", 3.0)
    pad, top = 110, 200
    rows = numbered(cfg)
    mode = meta.get("label_mode", "auto")
    inline = mode == "inline" or (mode == "auto" and len(rows) <= DENSE_N)

    plan_w, plan_h = int(Wm * PX), int(Hm * PX)
    PANEL_W, GAP = 430, 46
    W = pad + plan_w + GAP + PANEL_W + pad
    H = top + max(plan_h, index_panel_height(len(rows))) + 180

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    def P(x: float, y: float) -> tuple[float, float]:
        return pad + x * PX, top + y * PX

    draw_site(d, cfg, P, PX, W, H, inline)

    # 索引栏里带上 **稳定 id**：圆牌号是按面积降序生成的，**把一块加宽 2 m 就会让一半的号重排**，
    # 于是所有引用它的航线 / 闸门 / 批注静默指到别的建筑上，而且不报错。
    # 所以「圆牌号」只用来看图，「id」才是可以被引用的键（rule 4k）。
    index_panel(d, pad + plan_w + GAP, top, PANEL_W, [
        (no, b["name"],
         f"{b.get('id', '??')}  {b['size'][0]:g}×{b['size'][1]:g} m  h{float(b.get('h_m', 0) or 0):g}"
         + ("  ▣prop" if b.get("make_prop") else ""),
         area, SRC_STYLE[b["src"]], own_key(b, meta))
        for no, b, area in rows
    ])

    # 图面构件全部走 tools/previz/planstyle —— 与航线图同一套规范
    # 「体块合计」不叫「建筑占地」：院墙 / 空场 / 石板地也在 block 里，叫建筑会虚报。
    total = sum(a for _, _, a in rows)
    north_arrow(d, pad + plan_w - 46, top + 40)
    scale_bar(d, pad, H - 96, PX, meters=50)
    covers = meta.get("covers") or []
    cov = ("　管辖 " + "、".join(
        (c.get("dir") if isinstance(c, dict) else str(c)) for c in covers)) if covers else ""
    title_block(
        d, pad, 44,
        f"{meta['name_zh']} · 场地平面图（floor plan）",
        f"{meta['bg']} ｜ 场地 {Wm:g} × {Hm:g} m ｜ {len(rows)} 个建筑组 ｜ "
        f"体块合计 {total:,.0f} m²（占场地 {total / (Wm * Hm) * 100:.0f}%）{cov}",
        ("圆牌 = 看图编号（按面积降序，会随尺寸变动重排，**不可引用**）；可引用的键是右栏的 id；"
         "填充深浅 = 高度，斜线 = 贴地（h0）；虚线 = 推定"),
    )
    legend_row(d, pad, H - 56, SRC_STYLE.items())
    # 尺度来源不是「注记」，是**图上第一位的诚实机制**：bg1 的场地 260×300 m 自己都写着
    # 「这个换算没有一手出处」，而图以前照样把它印成事实。推定的必须挂一枚 ⚠，且不设抑制开关。
    if meta.get("scale_src") == "推定":
        wx, wy = pad + 300, H - 92
        d.polygon([(wx, wy + 9), (wx + 9, wy - 8), (wx + 18, wy + 9)], outline=(176, 60, 44), width=2)
        d.line([wx + 9, wy - 3, wx + 9, wy + 3], fill=(176, 60, 44), width=2)
        d.point((wx + 9, wy + 6), fill=(176, 60, 44))
        halo(d, (wx + 26, wy), "尺度为推定，未经一手核实", font(19), (176, 60, 44), anchor="lm")
    footer(d, pad, H - 22,
           f"本图为示意，真几何在 .blend · 由 tools/build_floorplan.py 从 blocks.toml 生成"
           f" · 尺度来源 {meta.get('scale_src', '?')} · blocks.toml@{planschema.sha(scene)}")

    out = os.path.join(scene, "planning", f"{meta['bg']}_floorplan.png")
    img.save(out)
    return out


def write_table(cfg: dict, scene: str) -> str:
    meta = cfg["meta"]
    # 表按 toml 原序（作者是按「围合 / 主体 / 附属」成组写的，打乱反而难改），
    # 靠 `#` 列与图上的圆牌对号 —— 圆牌是面积降序，两种顺序各有各的用处。
    idx = {b["name"]: (no, a) for no, b, a in numbered(cfg)}
    rows = "\n".join(
        f"| {b.get('id', '??')} | {idx[b['name']][0]} | {(b.get('bg') or '').strip() or '—'} | "
        f"{b['name']} | {b['xy'][0]:g}, {b['xy'][1]:g} | "
        f"{b['size'][0]:g} × {b['size'][1]:g} | {float(b.get('h_m', 0) or 0):g} | {idx[b['name']][1]:,.0f} | "
        f"{b.get('rot', 0):g}° | {b['src']} | {'✅' if b.get('make_prop') else ''} | {b.get('note', '')} |"
        for b in cfg.get("block", []))
    absent = meta.get("absent") or []
    absent_md = ("\n## 这里**没有**什么（喂负面词，rule 4k）\n\n"
                 + "\n".join(f"- ❌ {a}" for a in absent) + "\n"
                 ) if absent else ""
    total = sum(a for _, _, a in numbered(cfg))
    out = os.path.join(scene, "planning", f"{meta['bg']}_blocks.md")
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        f"""# {meta['name_zh']} · 建筑组清单

> **本文件是生成物**（`tools/build_floorplan.py`），几何唯一出处是同目录 `blocks.toml`。改布局 ＝ 改 toml 重跑。
> 场地 **{meta['size_m'][0]:g} × {meta['size_m'][1]:g} m**。{meta['scale_note']}
>
> 共 **{len(idx)} 个建筑组**，体块合计 **{total:,.0f} m²**，占场地 **{total / (meta['size_m'][0] * meta['size_m'][1]) * 100:.0f}%**。
> 尺度来源 **{meta.get('scale_src', '?')}** ｜ 收据 `blocks.toml@{planschema.sha(scene)}`
>
> **`id` 是可引用的键**（航线、闸门、批注一律引 id）；`#` 只是图上的看图圆牌，
> **按面积降序生成，改一块尺寸就会重排**，所以任何地方都不要引 `#`（rule 4k）。

| id | # | bg | 名字 | 中心 (x, y) m | 尺寸 m | 高 m | 面积 m² | 旋转 | 来源 | 建 prop | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
{rows}
{absent_md}

## 来源口径

- **原典方位**：任务文本 / wiki 原文写死的方位关系（东西南北、过不过河），**最可信**。
- **坐标表**：世界树的 `coords`（游戏内地图百分比）。⚠ w02 核验已指出北郡这张表**方位与坐标打架**，只作提示。
- **地图量取**：从 `refs/` 的 c60 原图上量的。
- **推定**：以上都没有，按空间逻辑推的。**图上画成虚线。**

## 下游

- 标 `建 prop` 的块 → `props/p{{N}}_{{名}}/` 出 object 卡（rule 4d 图先行五步）。
- 全表 → `_blender/blender_build.md` 的建模依据（rule 4e ⑥：`.blend` 是图的下游）。
""")
    return out


def audit(root: str, strict: bool) -> int:
    """全仓覆盖率。**默认只报告、退出 0**——「必备」是靠下游消费者跑不起来来咬人的，
    不是靠一次全仓盘点去点名旧剧（CLAUDE.md 2026-09-06 不回溯）。`--strict` 才判错。"""
    rows = planschema.audit(root)
    owns = [r for r in rows if r[1] == "owns"]
    pts = [r for r in rows if r[1] == "points"]
    miss = [r for r in rows if r[1] == "missing"]
    print(f"{root}：{len(rows)} 个 bg 目录 —— 自有图 {len(owns)} · 指向别人 {len(pts)} · 未解析 {len(miss)}")
    for dp, _s, note in pts:
        print(f"  → {os.path.relpath(dp)}  ⇒ {note}")
    for dp, _s, _n in miss:
        print(f"  ⬜ {os.path.relpath(dp)}")
    return 1 if (strict and miss) else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--audit", action="store_true", help="把 scene 当成根目录，扫覆盖率")
    ap.add_argument("--strict", action="store_true", help="--audit 时，有未解析的就退出 1")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if args.audit:
        return audit(args.scene, args.strict)

    cfg, p = load(args.scene)
    errs = check(cfg, args.scene)
    for e in errs:
        print("  ❌", e)
    if errs:
        print(f"\n{len(errs)} 条 blocker，未出图。")
        return 1
    n = len(cfg.get("block", []))
    props = sum(1 for b in cfg.get("block", []) if b.get("make_prop"))
    guess = sum(1 for b in cfg.get("block", []) if b["src"] == "推定")
    nokey = [b["name"] for b in cfg.get("block", [])
             if (b.get("bg") or "").strip() and (b.get("bg") or "").strip() != cfg["meta"]["bg"]]
    print(f"{cfg['meta']['name_zh']}：{n} 个建筑组（{props} 个要建 prop，{guess} 个是推定，"
          f"{n - len(nokey)} 个已挂 bg 主体卡）")
    if nokey:
        print(f"  归属别的主体卡（{len(nokey)}）：{'、'.join(nokey)}")
    if args.check:
        return 0
    print("  →", os.path.relpath(render(cfg, args.scene)))
    print("  →", os.path.relpath(write_table(cfg, args.scene)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
