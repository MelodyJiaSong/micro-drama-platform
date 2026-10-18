# -*- coding: utf-8 -*-
"""六模块剧：overhead.toml → 绿幕小人偶 previz 配置（previz/previz_config.toml），再交 `tools/previz/build_previz.py` 出 MP4。

    python tools/overhead_previz.py <镜头目录>                 # 写配置（previz.json 判「要」的镜才写；--force 免判也写）
    python tools/overhead_previz.py <镜头目录> --stills        # 写配置 + 出关键时刻静帧拼图（十几秒，先看这张）
    python tools/overhead_previz.py <镜头目录> --render        # 写配置 + 渲整条 MP4（几分钟）
    python tools/overhead_previz.py --all <集目录> [--stills|--render]   # 本集所有「要 previz」的镜

previz 只有绿幕、纯色小人偶（颜色＝剧 workflow.json 的 figure_colors，与 overhead 圆点同色）、人偶带着的东西
（overhead [[carry]] 与 [[actor]] shield：锤、盾、剑……在手里跟着 [[pose]] 的握法，背着就斜背在身后）和灰色方块物件：
它只回答「机位怎么走、谁站在哪、朝哪、几秒走到哪、几秒做什么姿势」；长相、服装、场景、光线、表情、特效都交给 Seedance。
位置与时刻只写在 overhead.toml（位置唯一出处）：改走位＝改 overhead 重跑本工具，previz_config.toml 不手改。
坐标：overhead 是场地平面图坐标（米，x 向东、y 向南）；previz 世界坐标原点在场地中心、y 向北。
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from tools import episode_shots as es  # noqa: E402
from tools import shot_overhead as so  # noqa: E402
from tools.blender_exe import BLENDER  # noqa: E402
from tools.previz import planschema  # noqa: E402

FPS = 24
RES = (1280, 720)        # Seedance 参考视频下限 409600 像素（tools/previz/seedance_ref.py）
AIM_Z = 1.4              # overhead 的 look 只有平面坐标；瞄点取成人胸口高
OBJ_H = 1.0              # [[object]] 没写 h 时的高


def _toml(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return "%g" % round(float(v), 3)
    if isinstance(v, str):
        return '"%s"' % v.replace('"', "'")
    return "[" + ", ".join(_toml(x) for x in v) + "]"


def _yaw(dx: float, dy: float) -> float:
    """面朝方向（previz 世界 XY）→ build_previz 的「朝向」度数：人偶 0° 面朝 -Y。"""
    return round(math.degrees(math.atan2(dx, -dy)), 1)


def _moved(a: tuple, b: tuple) -> bool:
    return abs(a[1] - b[1]) > 0.05 or abs(a[2] - b[2]) > 0.05


def config(shot_dir: Path) -> str:
    ov = so.load(shot_dir)
    info = es.episode_shot(shot_dir)
    drama = es.drama_root(shot_dir)
    secs = float(info["shot"]["duration"])
    owner, _ = planschema.resolve(str(so._bg_dir(so._scenes_root(drama), ov["meta"]["scene"])))
    W, H = planschema.load(owner)["meta"]["size_m"]

    def xy(x: float, y: float) -> tuple[float, float]:
        return float(x) - W / 2, H / 2 - float(y)

    actors = ov.get("actor", [])
    colors = es.figure_colors(drama, [a["key"].split("_", 1)[0] for a in actors])
    cams = ov["camera"]
    first = cams[0]
    subj = next((a for a in actors if a["key"] == first.get("subject")), actors[0] if actors else None)
    frac = 0.5
    if subj:
        lens = float(first.get("lens", 35))
        vfov = 2 * math.atan((so.SENSOR_W * 9 / 16) / (2 * lens))
        dist = max(0.5, math.dist(first["xy"], so._pos_at(subj["path"], float(first["t"]))))
        frac = round(min(3.0, so.SUBJ_H / (2 * dist * math.tan(vfov / 2))), 3)
    L = ["# 由 tools/overhead_previz.py 从 planning/overhead.toml 生成；不手改（改走位＝改 overhead 重跑）。", "",
         '["全局"]', "shot = %s" % _toml(shot_dir.name), "\"项目\" = %s" % _toml(drama.name), "\"绿幕\" = true",
         "fps = %d" % FPS, "total_sec = %s" % _toml(secs), "\"分辨率\" = %s" % _toml(list(RES)),
         "", '["机位"]', "\"焦距\" = %s" % _toml(first.get("lens", 35)), "\"占画高\" = %s" % _toml(frac)]
    if subj:
        L.append("\"基准主体\" = %s" % _toml(subj.get("label", subj["key"])))
    for c in cams:
        cx, cy = xy(*c["xy"])
        lx, ly = xy(*c.get("look", c["xy"]))
        L += ["", '[["机位"."路点"]]', "t = %s" % _toml(c["t"]), "\"位置\" = %s" % _toml([cx, cy, c.get("h", 1.6)]),
              "\"瞄\" = %s" % _toml([lx, ly, c.get("aim_h", AIM_Z)]), "\"焦距\" = %s" % _toml(c.get("lens", 35))]
        if c.get("cut"):
            L.append("\"切\" = true")
    poses = ov.get("pose", [])
    heights = es.settings(drama).get("figure_heights", {})
    for a0 in actors:
        for a in _crowd(a0):
            L += _actor(a, a0, colors[a0["key"].split("_", 1)[0]], _height(a0, heights), poses, xy)
            for c in carry_segments(ov, a, a0, secs):
                L += ['[["角色"."持物"]]'] + ["\"%s\" = %s" % (k, _toml(v)) for k, v in c.items()]
    for h in hit_checks(ov):
        L += ["", '[["命中"]]'] + ["\"%s\" = %s" % (k, _toml(v)) if k != "t" else "t = %s" % _toml(v) for k, v in h.items()]
    for o in ov.get("object", []):
        ox, oy = xy(*o["xy"])
        w, d = o.get("size", [0.6, 0.6])
        L += ["", '[["道具"]]', "\"名\" = %s" % _toml(o["label"]), "\"色\" = \"灰\"",
              "\"尺寸\" = %s" % _toml([w, d, o.get("h", OBJ_H)]), "\"位置\" = %s" % _toml([ox, oy, 0.0])]
        if o.get("rot"):
            L.append("\"朝向\" = %s" % _toml(-float(o["rot"])))
    for pr in ov.get("prop", []):        # 会动的道具（推车之类）：路点逐个打帧；出场前、gone 之后缩成一点
        w, d = pr.get("size", [0.4, 0.4])
        ph = float(pr.get("h", 0.3))
        pts = [(float(q[0]),) + tuple(xy(float(q[1]), float(q[2]))) for q in pr["path"]]
        keys = [(0.0, pts[0][1], pts[0][2], 1e-3), (max(0.0, pts[0][0] - 0.05), pts[0][1], pts[0][2], 1e-3)] if pts[0][0] > 0.05 else []
        keys += [(t, x, y, 1.0) for t, x, y in pts]
        if pr.get("gone") is not None:
            gx, gy = xy(*so.prop_pos(dict(pr, gone=None), float(pr["gone"])))
            keys += [(float(pr["gone"]), gx, gy, 1.0), (float(pr["gone"]) + 0.05, gx, gy, 1e-3)]
        L += ["", '[["道具"]]', "\"名\" = %s" % _toml(pr["label"]), "\"色\" = \"灰\"", "\"尺寸\" = %s" % _toml([w, d, ph]),
              "\"位置\" = %s" % _toml([pts[0][1], pts[0][2], 0.0])]
        for t, x, y, sc in sorted(keys):
            L += ["", '[["道具"."关键帧"]]', "t = %s" % _toml(round(t, 3)), "\"位置\" = %s" % _toml([x, y, 0.0]),
                  "\"尺寸\" = %s" % _toml([w * sc, d * sc, ph * sc])]
    return "\n".join(L) + "\n"


CROWD_GAP = 0.7      # 同卡一群（count = N）在 previz 里排成一列：前后间距（m），左右错开一半


def _crowd(a: dict) -> list[dict]:
    """overhead 里 count = N 的一群：第一只沿用原 label，其余 label 加序号、沿同一条路线跟在后面一列。"""
    n = int(a.get("count", 1))
    if n <= 1:
        return [a]
    p0 = a["path"][0]
    p1 = next((q for q in a["path"][1:] if math.dist(q[1:3], p0[1:3]) > 0.05), None)
    hx, hy = ((p1[1] - p0[1], p1[2] - p0[2]) if p1 is not None else (p0[3] - p0[1], p0[4] - p0[2]) if len(p0) >= 5 else (0.0, -1.0))
    nrm = math.hypot(hx, hy) or 1.0
    hx, hy = hx / nrm, hy / nrm
    out = [a]
    for i in range(1, n):
        back, lat = CROWD_GAP * ((i + 1) // 2), CROWD_GAP / 2 * (1 if i % 2 else -1)
        dx, dy = -hx * back - hy * lat, -hy * back + hx * lat
        path = [[q[0], q[1] + dx, q[2] + dy] + ([q[3] + dx, q[4] + dy] if len(q) >= 5 else []) for q in a["path"]]
        out.append(dict(a, label="%s%d" % (a.get("label", a["key"]), i + 1), path=path, count=1))
    return out


def _height(a: dict, heights: dict) -> float:
    """身高：剧 workflow.json 的 figure_heights（人物卡号 → 米）；没登记的按 1.75 m。"""
    return float(heights.get(a["key"].split("_", 1)[0], 1.75))


def _actor(a: dict, base: dict, col: str, h: float, poses: list[dict], xy) -> list[str]:
    """一个 [[角色]]：路点换成关键帧。站着的路点沿用此前 [[pose]] 给的姿势（不再一律写回「站」），走动时写「行走」。"""
    who = (base["key"], base.get("label"), a.get("label"))
    mine = sorted((float(p["t"]), p["pose"]) for p in poses if p["who"] in who)
    path = [(float(p[0]), *xy(p[1], p[2]), p) for p in a["path"]]
    keys: dict[float, dict] = {}
    yaw = 0.0
    for i, (t, x, y, p) in enumerate(path):
        nxt = path[i + 1] if i + 1 < len(path) else None
        moving = nxt is not None and _moved(nxt, path[i])
        if len(p) >= 5:
            fx, fy = xy(p[3], p[4])
            yaw = _yaw(fx - x, fy - y)
        elif moving:
            yaw = _yaw(nxt[1] - x, nxt[2] - y)
        k = {"t": t, "位置": [x, y, 0.0], "朝向": yaw}
        if moving:
            k["姿态"] = "行走"
        elif i == 0 or _moved(path[i - 1], path[i]):
            k["姿态"] = next((pose for pt, pose in reversed(mine) if pt <= t + 1e-6), "站")
        keys[t] = k
    for t, pose in mine:
        if t not in keys:          # 姿态时刻不在路点上：位置与朝向按路线插值补一帧
            x, y = xy(*so._pos_at(a["path"], t))
            keys[t] = {"t": t, "位置": [x, y, 0.0],
                       "朝向": keys[max(k for k in keys if k <= t)]["朝向"] if any(k <= t for k in keys) else yaw}
        keys[t]["姿态"] = pose
    L = ["", '[["角色"]]', "\"名\" = %s" % _toml(a.get("label", a["key"])), "\"色\" = %s" % _toml(col),
         "\"身高\" = %s" % _toml(h)]
    if so.QUADRUPED.search(base.get("label", "") + base["key"]) or base["key"].endswith("_Wolf"):
        L.append("\"四足\" = true")       # 狼之类：四足人偶，不是直立小人
    if a.get("gone") is not None:
        L.append("\"离场\" = %s" % _toml(float(a["gone"])))
    if a.get("enter") is not None:
        L.append("\"入场\" = %s" % _toml(float(a["enter"])))
    for t in sorted(keys):
        L += ['[["角色"."关键帧"]]'] + ["\"%s\" = %s" % (k, _toml(v)) for k, v in keys[t].items()]
    return L


def _grip_at(mine: list[tuple[float, str]], t: float, grips: tuple, default: str) -> str:
    """t 这一刻生效的 [[pose]]（最后一条 ≤ t）里写的持物姿态；没写就用缺省握法。"""
    pose = next((p for pt, p in reversed(mine) if pt <= t + 1e-6), "")
    return next((g for g in pose.split("+") if g.strip() in grips), default).strip()


def _windows(t0: float, t1: float, cuts: list[float], grip_at) -> list[tuple[float, float, str]]:
    """[t0, t1] 按姿态时刻切段，相邻同握法的段并起来。"""
    marks = [t0] + sorted(t for t in set(cuts) if t0 + 1e-6 < t < t1 - 1e-6) + [t1]
    out: list[tuple[float, float, str]] = []
    for a, b in zip(marks, marks[1:]):
        g = grip_at(a)
        if out and out[-1][2] == g:
            out[-1] = (out[-1][0], b, g)
        else:
            out.append((a, b, g))
    return out


def carry_segments(ov: dict, a: dict, base: dict, secs: float) -> list[dict]:
    """一个人偶的 [[角色.持物]]（follow-up 262）：[[carry]] 与 [[actor]] shield 换成引擎的件、姿（握法）、长、起 / 止。
    在手里：握法跟着这一刻 [[pose]] 里写的持物姿态（双手低握 → 前砸 → …），没写取 grip / 该件的缺省；
    背着：盾「背盾」（件也叫背盾，命中检查按「{人}_背盾」找），其余「斜背」。整镜都在时不写起 / 止。"""
    who = {base["key"], base.get("label"), a.get("label")}
    mine = sorted((float(p["t"]), p["pose"]) for p in ov.get("pose", []) if p["who"] in who)
    cuts = [t for t, _ in mine]
    wins: list[tuple[float, float, str, str, dict]] = []      # (起, 止, 件, 姿, 源)
    if base.get("shield"):
        if base["shield"] != "左":
            raise so.Bad("%s 的 shield = %s：previz 只有左手盾" % (base.get("label", base["key"]), base["shield"]))
        t0, t1 = (float(x) for x in base.get("shield_t", [0.0, secs]))
        wins += [(a0, a1, "盾", g, {}) for a0, a1, g in
                 _windows(t0, t1, cuts, lambda t: _grip_at(mine, t, planschema.SHIELD_GRIPS, planschema.CARRY_KINDS["盾"][1]))]
    for c in ov.get("carry", []):
        if c["who"] not in who:
            continue
        what, t0, t1 = c["what"], float(c.get("t0", 0.0)), float(c.get("t1", secs))
        if c["on"] == "背":
            back = planschema.BACK_GRIPS.get(what, planschema.SLUNG)
            wins.append((t0, t1, back if what == "盾" else what, back, c))
            continue
        grips = planschema.SHIELD_GRIPS if what == "盾" else planschema.HAND_GRIPS
        dflt = c.get("grip") or planschema.CARRY_KINDS[what][1]
        wins += [(a0, a1, what, g, c) for a0, a1, g in _windows(t0, t1, cuts, lambda t: _grip_at(mine, t, grips, dflt))]
    out = []
    for a0, a1, item, grip, c in sorted(wins, key=lambda w: w[0]):
        kind = "盾" if "盾" in item else item
        seg = {"件": item, "姿": grip, "长": float(c.get("len", planschema.CARRY_KINDS[kind][0]))}
        if c.get("shape"):
            seg["形"] = c["shape"]
        if a0 > 1e-6:
            seg["起"] = a0
        if a1 < secs - 1e-6:
            seg["止"] = a1
        out.append(seg)
    return out


def _label(ov: dict, ref: str) -> str:
    a = so._actor(ov, ref)
    return a.get("label", a["key"]) if a else ref


def hit_checks(ov: dict) -> list[dict]:
    """overhead [[hit]] 里用兵器、不落空的那几下 → previz [[命中]]：渲染时查兵器件真的贴到目标（或目标身上的盾）。
    身体出手（咬、撞、拳）与扔出去的（投、光）不抄：平面图已按距离查过，previz 的色块身体量不出更多。"""
    out = []
    for h in ov.get("hit", []):
        if h.get("miss") or h.get("with") not in planschema.HIT_OBJ:
            continue
        who = _label(ov, h["who"])
        d = {"t": h["t"], "谁": who, "物件": h.get("obj") or "%s_%s" % (who, planschema.HIT_OBJ[h["with"]]),
             "目标": _label(ov, h["target"])}
        part = planschema.hit_part_obj(h.get("part", ""))
        if part:
            d["部位"] = part
        out.append(d)
    return out


def needs_previz(shot_dir: Path) -> bool:
    p = shot_dir / "planning" / "previz.json"
    if not p.is_file():
        raise es.ShotError("%s 还没有 planning/previz.json——先跑 python tools/shot_overhead.py %s" % (shot_dir, shot_dir))
    return bool(json.loads(p.read_text(encoding="utf-8"))["previz"])


def run(shot_dir: Path, stills: bool, render: bool, force: bool) -> int:
    if not force and not needs_previz(shot_dir):
        print("  · %s 免 previz（overhead 图直接当运动参考）" % shot_dir.relative_to(REPO).as_posix())
        return 0
    cfg = shot_dir / "previz" / "previz_config.toml"
    cfg.parent.mkdir(exist_ok=True)
    cfg.write_text(config(shot_dir), encoding="utf-8", newline="\n")
    print("  → %s" % cfg.relative_to(REPO).as_posix())
    if stills:
        return subprocess.run([sys.executable, str(REPO / "tools" / "previz" / "review.py"), str(cfg)]).returncode
    if render:
        r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", str(REPO / "tools" / "previz" / "build_previz.py"),
                            "--", str(cfg)])
        if r.returncode == 0:
            print("  → %s" % (cfg.parent / ("%s_previz.mp4" % shot_dir.name)).relative_to(REPO).as_posix())
        return r.returncode
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="overhead → 绿幕小人偶 previz")
    ap.add_argument("target", type=Path, help="镜头目录；--all 时是集目录")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--stills", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--force", action="store_true", help="免 previz 的镜也写配置")
    a = ap.parse_args()
    targets = es.episode_shot_dirs(a.target.resolve()) if a.all else [a.target.resolve()]
    rc = 0
    for sd in targets:
        try:
            rc |= run(sd, a.stills, a.render, a.force)
        except (es.ShotError, so.Bad) as e:
            print("  ✗ %s" % e)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
