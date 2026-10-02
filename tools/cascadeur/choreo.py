# -*- coding: utf-8 -*-
"""镜头人体动作表 → Cascadeur 逐键数据 → 两段式出 FBX（follow-up 032：攻防镜的人体动作用 Cascadeur 做）。

位置与朝向只从 `planning/overhead.toml` 读（rule 4j：位置只写一次）；`cascadeur/choreo.toml` 只写逐拍用哪些姿势部件，
部件本身在共享库 `tools/cascadeur/poses.toml`（本镜独有的才写进镜头自己的 [parts]）。

    python tools/cascadeur/choreo.py <shot 目录>             # 写 cascadeur/keys.json 并打印每个角色要跑的 Cascadeur 命令
    python tools/cascadeur/choreo.py <shot 目录> --build     # 逐角色驱动在跑的 Cascadeur：建动画 → 导 FBX → 拷回 cascadeur/

Cascadeur 读不了中文路径（ai_videos__cascadeur动作 §2），FBX 先导到 ASCII 临时目录再拷回。
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
import shot_overhead  # noqa: E402

LIBRARY = REPO / "tools" / "cascadeur" / "poses.toml"   # 共享姿势库：部件与步频只写在这里一处
PART_KEYS = {"armL", "armR", "elbowL", "elbowR", "hipL", "hipR", "kneeL", "kneeR", "lean", "twist", "head",
             "drop", "lift", "ground"}


def _face_keys(path: list) -> list[tuple[float, float]]:
    out = []
    for i, p in enumerate(path):
        t, x, y = float(p[0]), float(p[1]), float(p[2])
        if len(p) == 5:
            v = (float(p[3]) - x, float(p[4]) - y)
        else:
            nb = path[i + 1] if i + 1 < len(path) else None
            pv = path[i - 1] if i else None
            if nb and math.dist((x, y), (nb[1], nb[2])) > 0.05:
                v = (nb[1] - x, nb[2] - y)
            elif pv and math.dist((x, y), (pv[1], pv[2])) > 0.05:
                v = (x - pv[1], y - pv[2])
            else:
                continue
        out.append((t, math.atan2(v[0], v[1])))
    if not out:
        raise SystemExit("路点里既没写面朝、也没有移动，推不出朝向")
    return out


def face_at(path: list, t: float) -> tuple[float, float]:
    ks = _face_keys(path)
    if t <= ks[0][0]:
        a = ks[0][1]
    elif t >= ks[-1][0]:
        a = ks[-1][1]
    else:
        for (t0, a0), (t1, a1) in zip(ks, ks[1:]):
            if t0 <= t <= t1:
                d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
                a = a0 + d * ((t - t0) / (t1 - t0) if t1 > t0 else 1.0)
                break
    return math.sin(a), math.cos(a)


FIGHT_PARTS = ("shield_guard", "shield_brace", "shield_shove")
HEAD_DOWN_MAX = 6.0       # 打斗姿态里「头角 + 0.6 × 前倾」超过这么多＝低着头（用户 2026-10-01：S11 杜克全程低头像傻子）
HEADUP_LEGACY = {"shot02", "shot10", "shot13", "shot14", "shot15", "shot16", "shot17", "shot18", "shot19", "shot20", "shot21", "shot22", "shot24", "shot25"}   # 已出片 / 暂不动，只减不增
_CUR_SHOT = ""


def pose_of(expr: str, parts: dict) -> dict:
    out: dict = {}
    for name in expr.split("+"):
        if name not in parts:
            raise SystemExit("姿态部件「%s」没在 [parts] 里定义" % name)
        bad = set(parts[name]) - PART_KEYS
        if bad:
            raise SystemExit("部件 %s 有未知关节键 %s（合法：%s）" % (name, sorted(bad), sorted(PART_KEYS)))
        out.update(parts[name])
    if any(n in FIGHT_PARTS for n in expr.split("+")) and _CUR_SHOT not in HEADUP_LEGACY:
        eff = float(out.get("head", 0.0)) + 0.6 * float(out.get("lean", 0.0))
        if eff > HEAD_DOWN_MAX:
            raise SystemExit("打斗姿态「%s」头低着（head %.0f + 0.6×lean %.0f = %.1f > %.0f）——加一个抬头部件（head 取负值）让他盯着对手" % (expr, out.get("head", 0.0), out.get("lean", 0.0), eff, HEAD_DOWN_MAX))
    return out


# ── 活人层（follow-up 067）──
HOLD_MAX_S = 0.6          # 任一关节一动不动超过这么久＝定格（机器人感）
MICRO_STEP_S = 0.45       # 定住的段落里每隔这么久插一个微动键
BREATH_S = 3.6            # 一次呼吸
BREATH = {"lean": 1.2, "head": 1.6}                 # 呼吸幅度（度）：胸口一起一伏、头跟着轻点
MICRO = {"armL": 2.5, "armR": 2.5, "elbowL": 3.0, "elbowR": 3.0, "twist": 1.5, "head": 2.0}   # 定住时的微动幅度
LEAD = {"lean": 0.65, "twist": 0.65, "head": 0.6, "drop": 0.6, "lift": 0.6,      # 大动作中段：躯干、头先到位六成多，
        "armL": 0.45, "armR": 0.45, "hipL": 0.5, "hipR": 0.5,                     # 上臂、髋跟到一半，
        "elbowL": 0.3, "elbowR": 0.3, "kneeL": 0.35, "kneeR": 0.35}               # 肘、膝最后跟上
BIG_DEG = 35.0            # 关节变化超过这么多算大动作，加中间键
JOINT_DPS_MAX = 900.0     # 关节角速度上限（度 / 秒），快过它不是人


def _vec(v) -> list[float]:
    return list(v) if isinstance(v, (list, tuple)) else [float(v)]


def _blend(a: dict, b: dict, w: dict | float) -> dict:
    out = {}
    for k in set(a) | set(b):
        if k == "ground":
            out[k] = b.get(k, a.get(k))
            continue
        va, vb = _vec(a.get(k, [0.0] * len(_vec(b.get(k, 0.0))))), _vec(b.get(k, [0.0] * len(_vec(a.get(k, 0.0)))))
        n = max(len(va), len(vb))
        va, vb = va + [0.0] * (n - len(va)), vb + [0.0] * (n - len(vb))
        ww = w.get(k, 0.5) if isinstance(w, dict) else w
        r = [x + (y - x) * ww for x, y in zip(va, vb)]
        out[k] = r if n > 1 else r[0]
    return out


def _add(p: dict, k: str, d: float, idx: int = 0) -> None:
    v = _vec(p.get(k, 0.0))
    if k in ("armL", "armR"):
        v = (v + [0.0, 0.0, 0.0])[:3]
    v[idx] += d
    p[k] = v if len(v) > 1 or k in ("armL", "armR") else v[0]


def _dist(a: dict, b: dict) -> float:
    m = 0.0
    for k in (set(a) | set(b)) - {"ground", "drop", "lift"}:
        va, vb = _vec(a.get(k, 0.0)), _vec(b.get(k, 0.0))
        n = max(len(va), len(vb))
        m = max([m] + [abs(x - y) for x, y in zip(va + [0.0] * (n - len(va)), vb + [0.0] * (n - len(vb)))])
    return m


def life_layer(rows: list[dict], fps: int, salt: float) -> list[dict]:
    """关键姿势 → 加了动作先后、定住微动、呼吸的键（位置与朝向照旧按时刻从平面图取）。"""
    out: list[dict] = []
    for i, r in enumerate(rows):
        out.append(r)
        if i + 1 == len(rows):
            break
        n = rows[i + 1]
        dt = n["t"] - r["t"]
        if _dist(r["pose"], n["pose"]) >= BIG_DEG and dt >= 0.2:          # 大动作：中段一键，躯干先走、肘膝后跟
            out.append({**r, "t": r["t"] + dt * 0.45, "expr": n["expr"] + "~lead", "pose": _blend(r["pose"], n["pose"], LEAD)})
        elif _dist(r["pose"], n["pose"]) < 1.0 and dt > HOLD_MAX_S:     # 定住：每 MICRO_STEP_S 一个微动键
            k = 1
            while r["t"] + k * MICRO_STEP_S < n["t"] - 0.15:
                t = r["t"] + k * MICRO_STEP_S
                p = {kk: (list(v) if isinstance(v, list) else v) for kk, v in r["pose"].items()}
                for j, (kk, amp) in enumerate(MICRO.items()):
                    _add(p, kk, amp * math.sin(1.7 * t + 2.1 * j + salt))
                out.append({**r, "t": t, "expr": r["expr"] + "~%d" % k, "pose": p})
                k += 1
    for r in out:                                                       # 呼吸叠在每一键上
        p = {kk: (list(v) if isinstance(v, list) else v) for kk, v in r["pose"].items()}
        for j, (kk, amp) in enumerate(BREATH.items()):
            _add(p, kk, amp * math.sin(2 * math.pi * r["t"] / BREATH_S + 0.8 * j + salt))
        r["pose"] = p
        r["f"] = round(r["t"] * fps)
    out.sort(key=lambda r: r["t"])
    seen: set[int] = set()
    return [r for r in out if not (r["f"] in seen or seen.add(r["f"]))]


UPPER = ("armL", "armR", "elbowL", "elbowR", "lean", "twist", "head")   # 机器人感看上半身：脚站着不动是正常的


def life_errors(label: str, rows: list[dict]) -> list[str]:
    """活人层闸门：上半身（臂、肘、胸、头）一起一动不动超过 HOLD_MAX_S；或两键之间关节角速度快过 JOINT_DPS_MAX。"""
    bad: list[str] = []
    up = lambda r: {k: r["pose"].get(k, 0.0) for k in UPPER}
    start = 0
    for i in range(1, len(rows)):
        if _dist(up(rows[start]), up(rows[i])) > 0.5:
            start = i
        elif rows[i]["t"] - rows[start]["t"] > HOLD_MAX_S + 1e-6:
            bad.append("%s 上半身在 %g–%gs 一动不动（> %gs，机器人感，follow-up 067）" % (label, rows[start]["t"], rows[i]["t"], HOLD_MAX_S))
            start = i
    for a, b in zip(rows, rows[1:]):
        d = _dist(a["pose"], b["pose"])
        if b["t"] > a["t"] and d / (b["t"] - a["t"]) > JOINT_DPS_MAX:
            bad.append("%s 在 %g–%gs 关节转得太快（%.0f°/s > %g）" % (label, a["t"], b["t"], d / (b["t"] - a["t"]), JOINT_DPS_MAX))
    return bad


def build_keys(shot_dir: Path) -> dict:
    global _CUR_SHOT
    _CUR_SHOT = shot_dir.name
    ov = shot_overhead.load(shot_dir)
    ch = tomllib.loads((shot_dir / "cascadeur" / "choreo.toml").read_text(encoding="utf-8"))
    fps = int(ch["meta"].get("fps", 30))
    lib = tomllib.loads(LIBRARY.read_text(encoding="utf-8"))
    own = ch.get("parts", {})
    clash = sorted(set(own) & set(lib["parts"]))
    if clash:
        raise SystemExit("镜头 [parts] 与共享库 %s 重名：%s —— 本镜独有的部件另起名，改库就改库" % (LIBRARY.name, clash))
    parts = {**lib["parts"], **own}
    gait_step = lib["gait"]
    secs = max(float(p[0]) for a in ov.get("actor", []) for p in a["path"])
    out = {"origin": ch["meta"]["origin"], "fps": fps, "last": round(secs * fps), "actors": {}}
    for label, spec in ch["actor"].items():
        act = next((a for a in ov.get("actor", []) if a.get("label") == label), None)
        if act is None:
            raise SystemExit("overhead.toml 里没有 label ＝ %s 的 actor" % label)
        keys: dict[int, dict] = {}
        for t0, t1, kind, upper in spec.get("gait", []):
            n = 0
            t = float(t0)
            while t <= float(t1) + 1e-6:
                keys[round(t * fps)] = {"t": t, "expr": "%s_%s+%s" % (kind, "ab"[n % 2], upper)}
                n += 1
                t += float(gait_step[kind])
        for t, expr in spec.get("keys", []):
            keys[round(float(t) * fps)] = {"t": float(t), "expr": expr}
        rows = []
        for fr in sorted(keys):
            k = keys[fr]
            x, y = shot_overhead._pos_at(act["path"], k["t"])
            rows.append({"f": fr, "t": k["t"], "expr": k["expr"], "pose": pose_of(k["expr"], parts),
                         "x": x, "y": y, "face": face_at(act["path"], k["t"])})
        if rows[-1]["f"] > out["last"]:
            raise SystemExit("%s 的末键 %gs 超出镜长" % (label, rows[-1]["t"]))
        if ch["meta"].get("life"):
            rows = life_layer(rows, fps, salt=len(out["actors"]) * 1.3)
            for r in rows:
                r["x"], r["y"] = shot_overhead._pos_at(act["path"], r["t"])
                r["face"] = face_at(act["path"], r["t"])
            bad = life_errors(label, rows)
            if bad:
                raise SystemExit("活人层闸门：" + chr(10) + "  " + (chr(10) + "  ").join(bad))
        out["actors"][label] = rows
    return out


SLOW_S = 0.6   # ≥ 这么长的键间隔一律 LINEAR：慢过渡用 Bezier 会把后面的快动作提前拉进来（shot20 加瑞克举斧前就弯腰 32°）
JUMP_MPS = shot_overhead.SPEED_MAX["c"]   # 两键之间根位移快过人冲刺 ＝ 镜内硬切换位置（与平面图瞬移闸门同一个数）

RUNNER = r'''
import json
LIB = r"{repo}\tools\cascadeur\casc_lib.py"
FK = r"{repo}\tools\cascadeur\casc_fk.py"
exec(open(LIB, encoding="utf-8").read())
REST_FRESH = {fresh}
if REST_FRESH:
    reload_scene(r"C:\Program Files\Cascadeur\samples\Cascy.casc")
    exec(open(LIB, encoding="utf-8").read())
exec(open(FK, encoding="utf-8").read())
D = json.load(open(r"{keys}", encoding="utf-8"))
rows = D["actors"][{label!r}]
if {fresh}:
    set_anim_size(D["last"] + 1)
    set_visible_range(0, D["last"])
for r in rows[{a}:{b}]:
    key_pose(r["f"], r["pose"], r["x"], r["y"], r["face"], D["origin"], "choreo " + r["expr"])
print("keyed", {a}, min({b}, len(rows)), "of", len(rows))
'''

FINISH = r'''
import json
LIB = r"{repo}\tools\cascadeur\casc_lib.py"
FK = r"{repo}\tools\cascadeur\casc_fk.py"
exec(open(LIB, encoding="utf-8").read())
exec(open(FK, encoding="utf-8").read())
D = json.load(open(r"{keys}", encoding="utf-8"))
rows = D["actors"][{label!r}]
frames = [r["f"] for r in rows]
print(set_interpolation(POINTS, frames, "BEZIER"))
# 保持段一律 LINEAR（Bezier 会把下一段的大动作提前拉进来）：姿势相同就算保持，挪几步也是保持——
# 原先还要求位移 < 0.3 m，shot05 亚伦 8–11.8s 同一个架势挪了 0.46 m 被判成 Bezier，烘出来弯腰低头 73°（follow-up 042）
holds = [a["f"] for a, b in zip(rows, rows[1:]) if a["expr"] == b["expr"] or b["t"] - a["t"] >= {slow}]
# 镜内硬切人换位置（根位移快过 {jump} m/s）：跳变那一段和前后两段一律 LINEAR——Bezier 会把十几米的跳变甩出去，
# 切点后人先冲出场地十几米再折回来（052 shot11：25s 切到洞口，骨盆被甩到洞外 16 m、previz 贴地找不到地面）
for i, (a, b) in enumerate(zip(rows, rows[1:])):
    if ((b["x"] - a["x"]) ** 2 + (b["y"] - a["y"]) ** 2) ** 0.5 > {jump} * max(b["t"] - a["t"], 1e-6):
        holds += [r["f"] for r in rows[max(0, i - 1):i + 3]]
print(set_interpolation(POINTS, sorted(set(holds)), "LINEAR"))
set_visible_range(0, D["last"])
for fr in range(0, D["last"] + 1, 30):
    goto(fr)
goto(0)
print(export_fbx(r"{fbx}"))
'''


def _run(code: str) -> None:
    r = subprocess.run([sys.executable, str(REPO / "tools" / "cascadeur" / "casc_run.py"), "-c", code],
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    print(r.stdout.strip()[-600:])
    if r.returncode:
        raise SystemExit("Cascadeur 脚本失败：\n" + r.stderr[-2000:])


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("shot_dir")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--only", default="", help="只建这个 label 的角色")
    ap.add_argument("--batch", type=int, default=12)
    args = ap.parse_args()
    shot_dir = Path(args.shot_dir).resolve()
    data = build_keys(shot_dir)
    out = shot_dir / "cascadeur" / "keys.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    for label, rows in data["actors"].items():
        print("%s：%d 键，%s" % (label, len(rows), "、".join("%gs %s" % (r["t"], r["expr"]) for r in rows[:4]) + " …"))
    if not args.build:
        return 0
    tmp = Path(tempfile.gettempdir()) / "casc_choreo"
    tmp.mkdir(exist_ok=True)
    keys_ascii = tmp / "keys.json"
    shutil.copyfile(out, keys_ascii)
    for i, (label, rows) in enumerate(data["actors"].items()):
        if args.only and label != args.only:
            continue
        stem = "%s_body%d" % (shot_dir.name, i + 1)
        for a in range(0, len(rows), args.batch):
            _run(RUNNER.format(repo=REPO, keys=keys_ascii, label=label, fresh=a == 0, a=a, b=a + args.batch))
        fbx = tmp / (stem + ".fbx")
        _run(FINISH.format(repo=REPO, keys=keys_ascii, label=label, fbx=fbx, slow=SLOW_S, jump=JUMP_MPS))
        dst = shot_dir / "cascadeur" / (stem + ".fbx")
        shutil.copyfile(fbx, dst)
        print("→ %s（%s）" % (dst.relative_to(REPO), label))
        # RUNNER 每个角色 fresh 新建一个场景：不关就越堆越多（2026-09-30 实测 21 个场景、12 GB，脚本开始 idle 超时）
        _run(CLOSE_OTHERS)
    return 0


CLOSE_OTHERS = r'''
import csc
sm = csc.app.get_application().get_scene_manager()
cur = sm.current_scene()
for s in [s for s in sm.scenes() if s != cur]:
    sm.remove_application_scene(s)
print("scenes left", len(list(sm.scenes())))
'''


if __name__ == "__main__":
    raise SystemExit(main())
