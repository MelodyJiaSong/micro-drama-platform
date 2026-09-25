# -*- coding: utf-8 -*-
"""一个 shot 的**镜头平面图（overhead）** —— 分层出片的第二层（ai_video.md rule 4j，2026-09-25 修订）。

    ① 场景层  scene blend + 场地平面图 floor plan（`tools/build_floorplan.py`）—— 静态的地方
    ② 本工具  每镜一张 overhead：镜头怎么走、每个人怎么走、建筑与物件在哪——**不管动作细节与形状**
    ③ shot blend + previz MP4：真实动作、走位细节、物件形状、镜头远近变化（从②的同一份数据读，不重填坐标）
    ④ Seedance：色彩、表情、特效、质感
每一层只解决它最擅长、最便宜的那件事；越往下改一次越贵，所以错误要在越上面的层拦住。

输入（唯一出处）：`{shot 目录}/planning/overhead.toml`
    [meta]      scene = "bg19"（挂在哪张场地平面图的坐标系上）· view = [x0, y0, x1, y1]（可选，米）· note ·
                walkable = ["b08"]（本镜机位允许站进的地块 id，只给类型泛用的地块用）
    [[camera]]  t · xy · h（离地米）· look（瞄准点）· lens（mm）· tag（机位标签，可选）·
                subject（这一刻景别量谁，人物卡键；缺省＝第一个 actor）· cut（true＝硬切到这里，不是运镜走过来）· note
    [[actor]]   key（人物卡目录名）· label · count（群体数，默认 1）· path = [[t, x, y], …]
                （路点可写 [t, x, y, fx, fy]：fx/fy ＝ 此刻面朝的点）· note
    [[object]]  label · xy · size · rot · key（物件卡目录名，可选）· note —— 场地图里没有、本镜才出现的东西
    [[beat]]    t0 · t1 · text —— 时间轴提要（与剧本【a–bs】对齐）
坐标一律用场地平面图的坐标系（米；x 向东、y 向南，与 floor plan 同一张网格）。

产物：`{shot 目录}/planning/{shot}_overhead.png`；`--all` 另写 `{ep 目录}/overheads.md` 索引。

构建闸门（blocker 不写图）：键名白名单 · 场景能解析 · 时刻落在镜长内且不倒退 ·
**入画人物与 shot md 的 `角色:` 行双向一致**（prompt 说谁在画面里，这张图就得给谁站位）。
提示（warning，印在图上）：机位落在有高度的体块里 · 起幅 / 落幅的机位距离与 `景别档` 按焦距反算的距离差太多。

用法：
    python tools/shot_overhead.py <shot 目录>
    python tools/shot_overhead.py --all <ep 目录>        # 整集，外加 overheads.md 索引
    python tools/shot_overhead.py --all <ep 目录> --check
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys
import tomllib
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import build_floorplan  # noqa: E402
from tools.previz import planschema  # noqa: E402
from tools.previz.planstyle import (  # noqa: E402
    ACCENT, INK, MUTED, PAPER, PANEL_BG, SOFT, font, halo, badge, north_arrow, scale_bar, title_block, footer,
)

KEYS = {
    "meta": {"scene", "view", "note", "walkable"},
    "camera": {"t", "xy", "h", "look", "lens", "tag", "subject", "cut", "note"},
    "actor": {"key", "label", "count", "path", "note"},
    "object": {"label", "xy", "size", "rot", "key", "note"},
    "beat": {"t0", "t1", "text"},
}
ACTOR_COLORS = [(38, 110, 196), (40, 150, 80), (150, 70, 170), (200, 130, 20), (20, 150, 150),
                (120, 90, 60), (200, 60, 130), (90, 90, 90)]
OBJ_COL = (214, 120, 30)
# 本身就是「人能站进去」的地块：机位落在里面不算扎进体块（内景壳、巷道、藤垄行间、桥面、门洞…）。
# 类型泛用的地块（kind = asset 的营地之类）不在此列——由各镜 `[meta] walkable = ["b08"]` 显式放行。
WALKABLE = {"hall_shell", "chamber", "tunnel", "vineyard", "graveyard", "arch_bridge", "mine_portal",
            "plaza", "yard", "lawn", "tables"}
SENSOR_W = 36.0          # 全画幅；16:9 横向视角由它与焦距算
FRAC = {"远景": 0.12, "全景": 0.3, "中景": 0.6, "近景": 0.9, "特写": 1.3}
SUBJ_H = 1.72
MAP_MAX = (1500, 1250)


class Bad(Exception):
    pass


def _drama_root(shot_dir: Path) -> Path:
    for d in (shot_dir, *shot_dir.parents):
        if (d / "2_世界观人设").is_dir():
            return d
    raise Bad("%s 往上找不到剧目录（没有 2_世界观人设/）" % shot_dir)


def _bg_dir(scenes: Path, bg: str) -> Path:
    for dirpath, dirs, _ in os.walk(scenes):
        for d in dirs:
            if d.startswith(bg + "_") and (Path(dirpath) / d / (d + ".md")).is_file():
                return Path(dirpath) / d
    raise Bad("场景主体 %s 在 %s 下找不到" % (bg, scenes))


def _shot_md(shot_dir: Path) -> tuple[str, float, str, set[str]]:
    f = shot_dir / (shot_dir.name + ".md")
    if not f.is_file():
        raise Bad("没有 %s —— overhead 的时长与入画人物都从它读" % f.name)
    text = f.read_text(encoding="utf-8")
    title = (re.search(r"^title:\s*(.+)$", text, re.M) or [None, ""])[1]
    secs = float(re.search(r"^duration_s:\s*([0-9.]+)", text, re.M).group(1))
    jb = (re.search(r"\*\*景别档\*\*:\s*(.+)$", text, re.M) or [None, ""])[1]
    role = (re.search(r"^角色: (.*)$", text, re.M) or [None, ""])[1]
    chars = set(re.findall(r"(?:^|；)([cm]\d+_[^＝；]+)＝", role))
    return title, secs, jb, chars


def load(shot_dir: Path) -> dict:
    p = shot_dir / "planning" / "overhead.toml"
    if not p.is_file():
        raise Bad("没有 %s" % p.relative_to(REPO))
    with open(p, "rb") as fh:
        cfg = tomllib.load(fh)
    for sec, body in cfg.items():
        if sec not in KEYS:
            raise Bad("overhead.toml：未知段 [%s]" % sec)
        for item in (body if isinstance(body, list) else [body]):
            bad = set(item) - KEYS[sec]
            if bad:
                raise Bad("overhead.toml [%s] 未知键 %s（拼错不静默忽略）" % (sec, sorted(bad)))
    return cfg


def _inside(b: dict, x: float, y: float) -> bool:
    cs = planschema.corners(b)
    sign = None
    for i in range(4):
        (ax, ay), (bx, by) = cs[i], cs[(i + 1) % 4]
        cr = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        s = cr >= 0
        if sign is None:
            sign = s
        elif s != sign:
            return False
    return True


def gate(cfg: dict, site: dict, secs: float, chars: set[str], jb: str) -> tuple[list[str], list[str]]:
    bad: list[str] = []
    warn: list[str] = []
    cams = cfg.get("camera", [])
    if not cams:
        bad.append("没有 [[camera]] 路点")
    ts = [float(c["t"]) for c in cams]
    if ts != sorted(ts) or (ts and (ts[0] < 0 or ts[-1] > secs + 1e-6)):
        bad.append("机位时刻 %s 须不减且落在 0–%gs" % (ts, secs))
    keys: set[str] = set()
    for a in cfg.get("actor", []):
        keys.add(a["key"])
        pt = [float(p[0]) for p in a["path"]]
        if pt != sorted(pt) or pt[0] < 0 or pt[-1] > secs + 1e-6:
            bad.append("%s 的路点时刻 %s 须不减且落在 0–%gs" % (a["key"], pt, secs))
        for p in a["path"]:
            if len(p) not in (3, 5):
                bad.append("%s 的路点 %s 须是 [t,x,y] 或 [t,x,y,fx,fy]" % (a["key"], p))
    if chars - keys:
        bad.append("shot md 的 `角色:` 里有、平面图没给站位：%s" % "、".join(sorted(chars - keys)))
    if keys - chars:
        bad.append("平面图里有、shot md 的 `角色:` 没有：%s" % "、".join(sorted(keys - chars)))
    Wm, Hm = site["meta"]["size_m"]
    open_ids = set(cfg["meta"].get("walkable", []))
    for c in cams:
        x, y = c["xy"]
        if not (-5 <= x <= Wm + 5 and -5 <= y <= Hm + 5):
            bad.append("机位 t=%gs 落在场地外 %s（场地 %g×%g m）" % (c["t"], c["xy"], Wm, Hm))
        for b in site.get("block", []):
            h = float(b.get("h_m", 0) or 0)
            if h > float(c.get("h", 1.6)) and b.get("kind") not in WALKABLE \
                    and b.get("id") not in open_ids and _inside(b, x, y):
                warn.append("机位 t=%gs 在「%s」(h%g m) 里面" % (c["t"], b["name"], h))
    # 起幅 / 落幅：按景别档的人占画高与焦距反算机位距离，与图上距离比一下
    m = re.findall(r"(远景|全景|中景|近景|特写)([0-9.]+)", jb)
    acts = {a["key"]: a for a in cfg.get("actor", [])}
    first = next(iter(acts), None)
    for c in cams:
        if c.get("subject") and c["subject"] not in acts:
            bad.append("机位 t=%gs 的 subject %s 不是本镜的 actor" % (c["t"], c["subject"]))
    if m and first and cams:
        for (name, v), c in ((m[0], cams[0]), (m[-1], cams[-1])):
            subj = acts.get(c.get("subject", first), acts[first])
            frac = float(v)
            lens = float(c.get("lens", 35))
            vfov = 2 * math.atan((SENSOR_W * 9 / 16) / (2 * lens))
            want = SUBJ_H / frac / (2 * math.tan(vfov / 2))
            p = _pos_at(subj["path"], float(c["t"]))
            got = math.dist(c["xy"], p)
            if got and not 0.4 <= got / want <= 2.5:
                warn.append("t=%gs %s%s：按 %gmm 该离主体约 %.1fm，图上是 %.1fm" % (
                    c["t"], name, v, lens, want, got))
    return bad, warn


def _pos_at(path: list, t: float) -> tuple[float, float]:
    pts = [(float(p[0]), float(p[1]), float(p[2])) for p in path]
    if t <= pts[0][0]:
        return pts[0][1], pts[0][2]
    for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            k = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    return pts[-1][1], pts[-1][2]


def _dashed(d: ImageDraw.ImageDraw, a, b, col, w: int = 2, dash: int = 12) -> None:
    n = max(1, int(math.dist(a, b) / dash))
    for k in range(0, n, 2):
        t0, t1 = k / n, min(1.0, (k + 1) / n)
        d.line([a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0,
                a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1], fill=col, width=w)


def _arrow(d: ImageDraw.ImageDraw, a, b, col, w: int = 4, head: int = 16) -> None:
    d.line([a, b], fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (-1, 1):
        d.line([b, (b[0] - head * math.cos(ang + s * 0.45), b[1] - head * math.sin(ang + s * 0.45))],
               fill=col, width=w)


def render(shot_dir: Path) -> tuple[Path | None, list[str], list[str]]:
    cfg = load(shot_dir)
    drama = _drama_root(shot_dir)
    bg = cfg["meta"]["scene"]
    bg_dir = _bg_dir(drama / "2_世界观人设" / "scenes", bg)
    owner, _ptr = planschema.resolve(str(bg_dir))
    site = planschema.load(owner)
    title, secs, jb, chars = _shot_md(shot_dir)
    bad, warn = gate(cfg, site, secs, chars, jb)
    if bad:
        return None, bad, warn

    Wm, Hm = site["meta"]["size_m"]
    vx0, vy0, vx1, vy1 = cfg["meta"].get("view", [0, 0, Wm, Hm])
    PX = min(MAP_MAX[0] / (vx1 - vx0), MAP_MAX[1] / (vy1 - vy0))
    map_w, map_h = int((vx1 - vx0) * PX), int((vy1 - vy0) * PX)
    pad, top, panel_w, gap = 90, 210, 660, 40
    W = pad + map_w + gap + panel_w + pad
    H = top + max(map_h, 1180) + 170
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    def P(x: float, y: float) -> tuple[float, float]:
        return pad + (x - vx0) * PX, top + (y - vy0) * PX

    build_floorplan.draw_site(d, site, P, PX, W, H, inline=True)
    for box in ((0, 0, W, top), (0, top + map_h, W, H), (0, top, pad, top + map_h),
                (pad + map_w, top, W, top + map_h)):
        d.rectangle(box, fill=PAPER)
    d.rectangle([pad, top, pad + map_w, top + map_h], outline=INK, width=3)

    f_s, f_m, f_b = font(17), font(20), font(22, bold=True)
    # 本镜物件
    for o in cfg.get("object", []):
        b = {"xy": o["xy"], "size": o.get("size", [0.6, 0.6]), "rot": o.get("rot", 0)}
        cs = [P(*p) for p in planschema.corners(b)]
        d.polygon(cs, fill=OBJ_COL + (90,), outline=OBJ_COL)
        cx, cy = P(*o["xy"])
        halo(d, (cx, cy - 16), "◆" + o["label"], f_s, OBJ_COL)
    # 人物走位
    for i, a in enumerate(cfg.get("actor", [])):
        col = ACTOR_COLORS[i % len(ACTOR_COLORS)]
        pts = [P(float(p[1]), float(p[2])) for p in a["path"]]
        n = int(a.get("count", 1))
        if len(pts) > 1:
            for j in range(len(pts) - 1):
                if pts[j] == pts[j + 1]:
                    continue
                # 切点瞬间换位置（Δt ≤ 0.2s）是镜内硬切的时间压缩，不是真的走过去——画虚线
                if float(a["path"][j + 1][0]) - float(a["path"][j][0]) <= 0.2:
                    _dashed(d, pts[j], pts[j + 1], col + (120,))
                else:
                    _arrow(d, pts[j], pts[j + 1], col + (220,), 4, 14)
        for j, (p, raw) in enumerate(zip(pts, a["path"])):
            r = 9 if j == 0 else 6
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col, outline=(255, 255, 255))
            if n > 1 and j == 0:
                for k in range(1, min(n, 6)):
                    ang = k * 2 * math.pi / min(n, 6)
                    q = (p[0] + 18 * math.cos(ang), p[1] + 18 * math.sin(ang))
                    d.ellipse([q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6], fill=col + (170,))
            if len(raw) == 5:
                fx, fy = P(float(raw[3]), float(raw[4]))
                ang = math.atan2(fy - p[1], fx - p[0])
                d.line([p, (p[0] + 26 * math.cos(ang), p[1] + 26 * math.sin(ang))], fill=col, width=3)
            halo(d, (p[0] + 14, p[1] + 14), "%gs" % float(raw[0]), f_s, col, anchor="lm")
        name = a.get("label", a["key"]) + (" ×%d" % n if n > 1 else "")
        halo(d, (pts[0][0], pts[0][1] - 22), name, f_m, col)
    # 机位
    cams = cfg["camera"]
    cp = [P(*c["xy"]) for c in cams]
    for j in range(len(cp) - 1):
        if cp[j] == cp[j + 1]:
            continue
        if cams[j + 1].get("cut"):          # 硬切：机位不是走过去的
            _dashed(d, cp[j], cp[j + 1], ACCENT + (110,))
            mx, my = (cp[j][0] + cp[j + 1][0]) / 2, (cp[j][1] + cp[j + 1][1]) / 2
            halo(d, (mx, my), "切", f_s, ACCENT)
        else:
            _arrow(d, cp[j], cp[j + 1], ACCENT, 6, 20)
    for j, (c, p) in enumerate(zip(cams, cp)):
        lens = float(c.get("lens", 35))
        hf = 2 * math.atan(SENSOR_W / 2 / lens)
        lk = P(*c.get("look", c["xy"]))
        ang = math.atan2(lk[1] - p[1], lk[0] - p[0])
        # 扇形只示意朝向与视角宽窄：长度封顶，否则广角镜的扇形会盖住半张图
        L = max(50.0, min(math.dist(p, lk), 130.0))
        wedge = [p, (p[0] + L * math.cos(ang - hf / 2), p[1] + L * math.sin(ang - hf / 2)),
                 (p[0] + L * math.cos(ang + hf / 2), p[1] + L * math.sin(ang + hf / 2))]
        d.polygon(wedge, fill=ACCENT + (16,), outline=ACCENT + (90,))
        d.line([p, (p[0] + L * math.cos(ang), p[1] + L * math.sin(ang))], fill=ACCENT + (150,), width=2)
    for j, (c, p) in enumerate(zip(cams, cp)):
        # 同一位置的路点（静止段）只标一次，免得圆牌叠圆牌
        if j and cp[j - 1] == p:
            continue
        badge(d, p[0], p[1], j + 1, ACCENT)
        halo(d, (p[0] + 20, p[1] - 20), "%gs" % float(c["t"]), f_m, ACCENT, anchor="lm")

    # 右栏
    x0, y = pad + map_w + gap, top
    d.rectangle([x0, y, x0 + panel_w, H - 150], fill=PANEL_BG)
    x, y = x0 + 22, y + 18

    def line(txt: str, f=f_s, col=INK, dy: int = 26) -> None:
        nonlocal y
        for chunk in _wrap(d, txt, f, panel_w - 44):
            d.text((x, y), chunk, font=f, fill=col)
            y += dy

    line("机位（红）", f_b, ACCENT, 32)
    for j, c in enumerate(cams, 1):
        line("%d  %gs  %s  h%gm  %gmm  %s" % (j, float(c["t"]), _xy(c["xy"]), float(c.get("h", 1.6)),
                                               float(c.get("lens", 35)), c.get("tag", "")), f_s, INK)
        if c.get("note"):
            line("    " + c["note"], f_s, SOFT)
    y += 10
    line("人物走位", f_b, INK, 32)
    for i, a in enumerate(cfg.get("actor", [])):
        col = ACTOR_COLORS[i % len(ACTOR_COLORS)]
        line("● %s（%s）%s" % (a.get("label", a["key"]), a["key"],
                               " ×%d" % int(a.get("count", 1)) if int(a.get("count", 1)) > 1 else ""), f_m, col, 28)
        line("    " + " → ".join("%gs%s" % (float(p[0]), _xy(p[1:3])) for p in a["path"]), f_s, SOFT)
        if a.get("note"):
            line("    " + a["note"], f_s, SOFT)
    if cfg.get("object"):
        y += 10
        line("本镜物件（橙）", f_b, OBJ_COL, 32)
        for o in cfg["object"]:
            line("◆ %s %s%s" % (o["label"], _xy(o["xy"]), ("  " + o["key"]) if o.get("key") else ""), f_s, INK)
    if cfg.get("beat"):
        y += 10
        line("时间轴", f_b, INK, 32)
        for b in cfg["beat"]:
            line("%g–%gs  %s" % (float(b["t0"]), float(b["t1"]), b["text"]), f_s, INK)
    if warn:
        y += 10
        line("⚠ 提示", f_b, (176, 60, 44), 32)
        for w_ in warn:
            line("· " + w_, f_s, (176, 60, 44))

    north_arrow(d, pad + map_w - 50, top + 44)
    scale_bar(d, pad, H - 118, PX, meters=_nice(vx1 - vx0))
    title_block(d, pad, 40, "%s《%s》 · 镜头平面图（overhead）" % (shot_dir.name, title),
                "%gs ｜ %s（%s）｜ 景别档 %s" % (secs, site["meta"].get("name_zh", bg), bg, jb or "—"),
                cfg["meta"].get("note", ""))
    halo(d, (pad, H - 72), "红＝机位（实线箭头＝运镜、虚线「切」＝硬切；圆牌号＝路点顺序、旁边是秒数，扇形＝朝向与视角）"
         "　彩色＝人物走位（点旁数字＝秒，短线＝面朝）　橙＝本镜物件", f_s, MUTED, anchor="lm")
    footer(d, pad, H - 40, "由 tools/shot_overhead.py 从 planning/overhead.toml 生成 · 位置的唯一出处，shot blend 从同一份读"
           " · 底图＝%s 场地平面图 blocks.toml@%s" % (bg, planschema.sha(owner)))
    out = shot_dir / "planning" / ("%s_overhead.png" % shot_dir.name)
    img.save(out)
    return out, bad, warn


def _xy(p) -> str:
    return "(%g,%g)" % (float(p[0]), float(p[1]))


def _nice(span: float) -> int:
    for m in (1, 2, 5, 10, 20, 50, 100, 200):
        if m >= span / 6:
            return m
    return 500


def _wrap(d: ImageDraw.ImageDraw, txt: str, f, width: int) -> list[str]:
    out, cur = [], ""
    for ch in txt:
        if d.textlength(cur + ch, font=f) > width:
            out.append(cur)
            cur = "    " + ch
        else:
            cur += ch
    return out + [cur]


def run_all(ep_dir: Path, check_only: bool) -> int:
    shots = sorted(p for p in (ep_dir / "shots").iterdir() if p.is_dir())
    rows, nbad = [], 0
    for sd in shots:
        try:
            if check_only:
                cfg = load(sd)
                drama = _drama_root(sd)
                owner, _ = planschema.resolve(str(_bg_dir(drama / "2_世界观人设" / "scenes", cfg["meta"]["scene"])))
                title, secs, jb, chars = _shot_md(sd)
                bad, warn = gate(cfg, planschema.load(owner), secs, chars, jb)
                out = None
            else:
                out, bad, warn = render(sd)
        except Bad as e:
            bad, warn, out = [str(e)], [], None
        nbad += len(bad)
        for b in bad:
            print("  ✗ %s: %s" % (sd.name, b))
        for w_ in warn:
            print("  ⚠ %s: %s" % (sd.name, w_))
        rows.append((sd.name, out, bad, warn))
    if not check_only:
        md = ["# %s 镜头平面图（overhead）索引" % ep_dir.name, "",
              "> 生成物：`python tools/shot_overhead.py --all %s`。改走位 ＝ 改各镜 `planning/overhead.toml` 重跑。"
              % ep_dir.relative_to(REPO).as_posix(),
              "> 这一层只定「镜头与人各自在哪、往哪走、几秒到」；动作细节与形状在 shot blend 层。**这里点头之后才做 shot blend。**", "",
              "| 镜 | 状态 | 图 |", "|---|---|---|"]
        for name, out, bad, warn in rows:
            st = "❌ %d" % len(bad) if bad else ("⚠ %d" % len(warn) if warn else "✅")
            md.append("| %s | %s | %s |" % (name, st, "[%s](shots/%s/planning/%s)" % (out.name, name, out.name)
                                              if out else "—"))
        (ep_dir / "overheads.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("%d 镜 · blocker %d · warning %d" % (len(rows), nbad, sum(len(r[3]) for r in rows)))
    return 1 if nbad else 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="镜头平面图（overhead）")
    ap.add_argument("target", type=Path, help="shot 目录；--all 时是 ep 目录")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true", help="只跑闸门，不画图")
    a = ap.parse_args()
    target = a.target.resolve()
    if a.all:
        return run_all(target, a.check)
    try:
        out, bad, warn = render(target)
    except Bad as e:
        print("  ✗ " + str(e))
        return 1
    for b in bad:
        print("  ✗ " + b)
    for w_ in warn:
        print("  ⚠ " + w_)
    if out:
        print("  → " + str(out.relative_to(REPO)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
