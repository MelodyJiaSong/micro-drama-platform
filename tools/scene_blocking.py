# -*- coding: utf-8 -*-
"""一场的**走位图**（blocking diagram）：把本场每个镜头的 overhead 叠成一张俯视简图，给人看站位与相互位置
（ai_video_management follow-up 271）。

数据唯一出处是各镜 `planning/overhead.toml`（与 `tools/shot_overhead.py` 同一份，不另存坐标）：
- 底图＝场地平面图的简笔画（坡、河、路、地块），与 Seedance 版 overhead 同一套画法（`shot_overhead.sketch_site`）；
- 人＝彩色圆（颜色与 overhead、previz 人偶同一张 workflow.json `figure_colors`），怪物与匪徒（m 卡）＝三角，
  物件与道具＝橙色方块；
- 镜内移动＝带箭头的虚线，旁边标镜号（本场镜头的播放顺序 1、2、3…）；不画机位（机位看各镜 overhead）。
同一场里不同镜用了不同场地平面图时，按平面图分块画在同一张图里。

产物：`scenes/sN/planning/sN_blocking.png`；管理 UI 的影视改编场页面显示它。
`tools/shot_overhead.py` 画完一镜（或 `--all` 画完整集）会顺带重画所在场的走位图。

用法：
    python tools/scene_blocking.py <场目录 scenes/sN>
    python tools/scene_blocking.py --all <集目录 episodes/epNN>
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import shot_overhead as so  # noqa: E402
from tools.previz import planschema  # noqa: E402
from tools.previz.planstyle import INK, MUTED, PAPER, PANEL_BG, SOFT, badge, font, halo, north_arrow, scale_bar  # noqa: E402

MAP_W, MAP_H_MAX, MAP_H_MIN = 1400, 1000, 520
PANEL_W, PAD, HEAD = 600, 60, 130
MOVE_MIN_M = 0.3            # 镜内位移小于这个算原地不动，不画轨迹
SAME_SPOT_M = 0.5           # 两镜起点相距小于这个算同一个站位，只画一个记号、镜号合在一起
MARGIN_M = 3.0


def out_path(scene_dir: Path) -> Path:
    return scene_dir / "planning" / ("%s_blocking.png" % scene_dir.name)


def _scene(scene_dir: Path) -> dict:
    ep_dir = scene_dir.parent.parent
    doc = json.loads((ep_dir / "filming.json").read_text(encoding="utf-8"))
    for sc in doc["content"]["scenes"]:
        if sc["id"] == scene_dir.name:
            return sc
    raise so.Bad("filming.json 里没有场次 %s" % scene_dir.name)


def _entity_ids(cfg: dict) -> list[str]:
    """同一镜里同卡多人（两名卫兵、两个匪徒）用 key+label 区分，其余只用 key——跨镜认出是同一个人。"""
    keys = [a["key"] for a in cfg.get("actor", [])]
    return [a["key"] + ("|" + a.get("label", "") if keys.count(a["key"]) > 1 else "") for a in cfg.get("actor", [])]


def _shape(d: ImageDraw.ImageDraw, p, kind: str, col, r: float, filled: bool = True) -> None:
    fill = col if filled else (255, 255, 255)
    if kind == "triangle":
        pts = [(p[0], p[1] - r * 1.2), (p[0] + r * 1.1, p[1] + r * 0.8), (p[0] - r * 1.1, p[1] + r * 0.8)]
        d.polygon(pts, fill=fill, outline=col if not filled else (255, 255, 255), width=3)
    elif kind == "square":
        d.rectangle([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill, outline=col if not filled else (255, 255, 255), width=3)
    else:
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill, outline=col if not filled else (255, 255, 255), width=3)


def _dashed_path(d: ImageDraw.ImageDraw, pts: list, col, w: int = 4) -> None:
    for a, b in zip(pts, pts[1:]):
        if math.dist(a, b) > 1:
            so._dashed(d, a, b, col, w, 14)
    # 箭头画在最后一段真正有长度的线段上
    segs = [(a, b) for a, b in zip(pts, pts[1:]) if math.dist(a, b) > 1]
    if segs:
        a, b = segs[-1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (-1, 1):
            d.line([b, (b[0] - 22 * math.cos(ang + s * 0.45), b[1] - 22 * math.sin(ang + s * 0.45))], fill=col, width=w + 1)


def _path_mid(pts: list):
    total = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    run = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        if run + seg >= total / 2 and seg > 0:
            t = (total / 2 - run) / seg
            return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        run += seg
    return pts[0]


def _ranges(ks: list[int]) -> str:
    """[3, 4, 5, 8] → 「3–5·8」：一个站位出现在很多镜时不把镜号排成一长串。"""
    out, run = [], [ks[0]]
    for k in ks[1:]:
        if k == run[-1] + 1:
            run.append(k)
        else:
            out.append(run); run = [k]
    out.append(run)
    return "·".join(("%d–%d" % (r[0], r[-1])) if len(r) > 2 else "·".join(map(str, r)) for r in out)


def render_scene(scene_dir: Path) -> Path | None:
    """画一场的走位图；本场一镜 overhead 都没有就不出图（返回 None）。"""
    scene_dir = scene_dir.resolve()
    sc = _scene(scene_dir)
    drama = so._drama_root(scene_dir)
    shots, missing = [], []
    for k, st in enumerate(sc["shots"], 1):
        sd = scene_dir / "shots" / st["id"]
        if not (sd / "planning" / "overhead.toml").is_file():
            missing.append(st["id"])
            continue
        cfg = so.load(sd)
        owner, _ = planschema.resolve(str(so._bg_dir(so._scenes_root(drama), cfg["meta"]["scene"])))
        shots.append({"k": k, "st": st, "dir": sd, "cfg": cfg, "owner": owner, "colors": so.actor_colors(cfg, sd)})
    if not shots:
        return None

    groups: dict[str, list[dict]] = {}
    for s in shots:
        groups.setdefault(s["owner"], []).append(s)

    # 每个平面图一块：先算尺寸
    panels = []
    for owner, items in groups.items():
        site = planschema.with_derived(planschema.load(owner))
        pts = [(float(p[1]), float(p[2])) for s in items for a in s["cfg"].get("actor", []) for p in a["path"]]
        pts += [tuple(o["xy"]) for s in items for o in s["cfg"].get("object", [])]
        pts += [(float(q[1]), float(q[2])) for s in items for pr in s["cfg"].get("prop", []) for q in pr["path"]]
        x0, x1 = min(p[0] for p in pts) - MARGIN_M, max(p[0] for p in pts) + MARGIN_M
        y0, y1 = min(p[1] for p in pts) - MARGIN_M, max(p[1] for p in pts) + MARGIN_M
        if x1 - x0 < 12:
            cx = (x0 + x1) / 2; x0, x1 = cx - 6, cx + 6
        if y1 - y0 < 8:
            cy = (y0 + y1) / 2; y0, y1 = cy - 4, cy + 4
        PX = min(MAP_W / (x1 - x0), MAP_H_MAX / (y1 - y0))
        w, h = MAP_W, max(MAP_H_MIN, int((y1 - y0) * PX))
        # 撑满面板：按面板宽高重新取米范围，内容居中
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        x0, x1 = cx - w / PX / 2, cx + w / PX / 2
        y0, y1 = cy - h / PX / 2, cy + h / PX / 2
        name = site["meta"].get("name_zh", "") or Path(owner).name
        panels.append({"site": site, "items": items, "view": (x0, y0, x1, y1), "PX": PX, "w": w, "h": h, "name": name})

    sub_h = 46 if len(panels) > 1 else 0
    H = HEAD + sum(p["h"] + sub_h + 30 for p in panels) + 90
    W = PAD + MAP_W + 40 + PANEL_W + PAD
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    entities: dict[str, dict] = {}       # id → {name, color, shape}
    y_top = HEAD
    for pan in panels:
        if sub_h:
            halo(d, (PAD, y_top + 20), "场地：%s（镜 %s）" % (pan["name"], "、".join(str(s["k"]) for s in pan["items"])),
                 font(24, bold=True), INK, anchor="lm")
        top = y_top + sub_h
        x0, y0, x1, y1 = pan["view"]
        PX = pan["PX"]

        def P(x: float, y: float, _x0=x0, _y0=y0, _top=top) -> tuple[float, float]:
            return PAD + (x - _x0) * PX, _top + (y - _y0) * PX

        box = (PAD, top, PAD + pan["w"], top + pan["h"])
        layer = Image.new("RGB", (W, H), so.GRASS_REF)
        ld = ImageDraw.Draw(layer, "RGBA")
        labels = so.sketch_site(ld, pan["site"], P, PX, box, name_size=22)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rectangle(box, fill=255)
        img.paste(layer, (0, 0), mask)
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle(box, outline=INK, width=3)
        taken: list = []

        # 物件与道具（橙色方块），同名只画一次
        seen_obj: set[str] = set()
        for s in pan["items"]:
            for o in s["cfg"].get("object", []):
                if so._short(o["label"]) in seen_obj:
                    continue
                seen_obj.add(so._short(o["label"]))
                p = P(*o["xy"])
                _shape(d, p, "square", so.OBJ_COL, 12)
                taken.append((p[0] - 14, p[1] - 14, p[0] + 14, p[1] + 14))
                labels.append((p, so._short(o["label"]), font(20), so.OBJ_COL, 22))
            for pr in s["cfg"].get("prop", []):
                pts = [P(float(q[1]), float(q[2])) for q in pr["path"]]
                if len(pts) > 1 and math.dist(pts[0], pts[-1]) > 1:
                    _dashed_path(d, pts, so.OBJ_COL + (230,), 3)
                    mx, my = _path_mid(pts)
                    badge(d, mx, my, s["k"], so.OBJ_COL, 13)
                _shape(d, pts[0], "square", so.OBJ_COL, 10)
                if so._short(pr["label"]) not in seen_obj:
                    seen_obj.add(so._short(pr["label"]))
                    labels.append((pts[0], so._short(pr["label"]), font(20), so.OBJ_COL, 22))

        # 人：每镜起点记号（同一站位合并镜号）+ 镜内移动虚线
        spots: dict[str, list[dict]] = {}   # 实体 → [{p, ks}]
        for s in pan["items"]:
            for a, eid in zip(s["cfg"].get("actor", []), _entity_ids(s["cfg"])):
                col = s["colors"][a["key"]]
                kind = "triangle" if a["key"].startswith("m") else "circle"
                entities.setdefault(eid, {"name": so._short(a.get("label", a["key"])), "color": col, "shape": kind})
                pts = [P(float(q[1]), float(q[2])) for q in a["path"]]
                start = pts[0]
                lst = spots.setdefault(eid, [])
                hit = next((sp for sp in lst if math.dist(sp["p"], start) <= SAME_SPOT_M * PX), None)
                if hit:
                    hit["ks"].append(s["k"])
                else:
                    lst.append({"p": start, "ks": [s["k"]], "col": col, "kind": kind, "name": entities[eid]["name"]})
                moved = max(math.dist(start, q) for q in pts) > MOVE_MIN_M * PX
                if moved:
                    _dashed_path(d, pts, col + (235,), 5)
                    _shape(d, pts[-1], kind, col, 11, filled=False)
                    mx, my = _path_mid(pts)
                    badge(d, mx, my, s["k"], col, 15)
                    taken.append((mx - 17, my - 17, mx + 17, my + 17))
        for eid, lst in spots.items():
            for j, sp in enumerate(lst):
                p = sp["p"]
                _shape(d, p, sp["kind"], sp["col"], 17)
                taken.append((p[0] - 20, p[1] - 20, p[0] + 20, p[1] + 20))
                tag = ("%s " % sp["name"] if j == 0 else "") + _ranges(sorted(sp["ks"]))
                labels.append((p, tag, font(22, bold=(j == 0)), sp["col"], 26))
        for anchor, txt, f, col, gap in labels:
            so._place(d, taken, anchor, txt, f, col, gap, W, H)
        north_arrow(d, PAD + pan["w"] - 50, top + 44, 56)
        scale_bar(d, PAD + 20, top + pan["h"] - 36, PX, meters=so._nice(x1 - x0))
        y_top = top + pan["h"] + 30

    # 标题
    halo(d, (PAD, 44), "%s · %s · 走位图" % (sc["id"], sc["location"]), font(34, bold=True), INK, anchor="lm")
    halo(d, (PAD, 92), "%s ｜ 编号＝本场镜头顺序；虚线箭头＝这一镜里的移动；人名旁的数字＝在这个位置出现的镜"
         % sc["time"], font(20), SOFT, anchor="lm")

    # 右栏：图例 + 镜头表
    x0p = PAD + MAP_W + 40
    d.rectangle([x0p, HEAD, x0p + PANEL_W, H - 90], fill=PANEL_BG)
    x, y = x0p + 24, HEAD + 22
    halo(d, (x, y), "人与物", font(24, bold=True), INK, anchor="lm")
    y += 40
    for e in entities.values():
        _shape(d, (x + 14, y), e["shape"], e["color"], 12)
        d.text((x + 40, y), e["name"], font=font(22), fill=INK, anchor="lm")
        y += 36
    if any(s["cfg"].get("object") or s["cfg"].get("prop") for s in shots):
        _shape(d, (x + 14, y), "square", so.OBJ_COL, 11)
        d.text((x + 40, y), "物件 / 道具", font=font(22), fill=INK, anchor="lm")
        y += 36
    d.text((x, y), "○ 圆＝主要人物　△ 三角＝卫兵、匪徒、怪物（群演卡）　□ 方块＝物件", font=font(18), fill=SOFT, anchor="lm")
    y += 30
    d.text((x, y), "空心记号＝这一镜结束时的位置", font=font(18), fill=SOFT, anchor="lm")
    y += 46
    halo(d, (x, y), "镜头", font(24, bold=True), INK, anchor="lm")
    y += 38
    for k, st in enumerate(sc["shots"], 1):
        drawn = any(s["k"] == k for s in shots)
        brief = st.get("camera", "").split("：")[0].split("，")[0]
        head = "%d  %s · %g 秒 · %s%s" % (k, st["id"], float(st["duration"]), brief, "" if drawn else "（未画 overhead）")
        d.text((x, y), so._wrap(d, head, font(19), PANEL_W - 50)[0], font=font(19), fill=INK if drawn else MUTED, anchor="lm")
        y += 30

    foot = "由 tools/scene_blocking.py 从各镜 planning/overhead.toml 生成；机位看各镜 overhead"
    if missing:
        foot += " ｜ 未画 overhead：" + "、".join(missing)
    d.text((PAD, H - 50), foot, font=font(18), fill=MUTED, anchor="lm")

    out = out_path(scene_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def render_episode(ep_dir: Path) -> list[Path]:
    doc = json.loads((ep_dir / "filming.json").read_text(encoding="utf-8"))
    outs = []
    for sc in doc["content"]["scenes"]:
        out = render_scene(ep_dir / "scenes" / sc["id"])
        if out:
            outs.append(out)
    return outs


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="一场的走位图（blocking diagram）")
    ap.add_argument("target", type=Path, help="场目录 scenes/sN；--all 时是集目录")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    try:
        outs = render_episode(a.target.resolve()) if a.all else [render_scene(a.target)]
    except so.Bad as e:
        print("  ✗ " + str(e))
        return 1
    for out in outs:
        print("  → " + (str(out.relative_to(REPO)) if out else "本场还没有 overhead，未出图"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
