# -*- coding: utf-8 -*-
"""区级物件规划 `{区}/_plan/plan.toml` → 每个 bg 的 blocks.toml（kind / asset / face / count + 校验机位）→ blend（follow-up 007 / 013）。

物件本身住本剧 `props/p{N}_{名}/`（`tools/props_lib.py`）；区里只留这份布局规划。
plan.toml（区级规划 agent 写；本脚本只读）：
    [[asset]]  key / name_zh / size_m / queries / prompt_en / brief     —— 新物件（key 先用 props_lib 领号；props 里已有的直接引用，不必重列）
    [[use]]    bg = "bg11" / block = "b01" / asset = "{key}" 或 kind = "yard" / face / count
               或 parts = [{asset = "{key}", at = [x, y], yaw = 0}, …] —— 一个块里有几样东西（长桌 + 长凳），
               每样一个单物体资产，由 build_scene 摆在一起；**GLB 只装单个物体**（2026-09-25）
本脚本做四件事，全部确定性、可重跑：
    ① plan 里新物件在 props/ 下建目录 + asset.toml（卡由写卡 agent 写，`gen_bg_assets.py check` 管它齐不齐）
    ② 把 [[use]] 写进各 bg 的 blocks.toml（只动 kind / asset / face / count / may_overlap 这几个键；其余字段一字不动）
    ③ 没有 [[anchor]] 的 bg 补一个默认校验机位（场地南缘朝北、避开所有体块）
    ④ `--build`：逐个开 Blender 跑 build_scene.py。**布局闸门以引擎为唯一判据**——它报「平面重叠 / 落在山脊里 /
       坐在河道上 / 眼位落在体块内部」，本脚本按消息写显式声明（may_overlap / into_ridge / over_water / 挪机位）
       再重跑，最多三轮；每一条自动声明都记进 `_plan/apply_report.md`，不静默。

用法（仓库根目录）：
    python tools/apply_asset_plan.py <区目录> [--build]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parent.parent
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from blender_exe import BLENDER as _BLENDER_EXE  # noqa: E402  Blender 路径唯一出处
BLENDER = Path(_BLENDER_EXE)
GROUND = ("lawn", "plaza", "yard", "graveyard", "vineyard")
BLOCK_KEYS = ("kind", "asset", "parts", "face", "count", "layout", "may_overlap", "into_ridge", "over_water")
LEGACY = {"bg1", "bg2", "bg3", "bg17", "bg18", "bg19", "bg20", "bg21", "bg22"}
PLAN_DIR = "_plan"      # 区级只留布局规划；物件本身住本剧 props/（follow-up 013）
sys.path.insert(0, str(REPO))
from tools import props_lib  # noqa: E402


def kinds() -> set[str]:
    """kind 名单只有一处定义：build_scene.py 的 KINDS 字典（它 import bpy，所以这里读源码）。"""
    src = (REPO / "tools" / "build_scene.py").read_text(encoding="utf-8")
    body = src[src.index("KINDS = {"):]
    body = body[:body.index("}")]
    return set(re.findall(r'"([a-z_]+)"\s*:', body))


def q(v) -> str:
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def tv(v) -> str:
    """TOML 行内值：parts 是 inline table 数组，别的键是标量。"""
    if v is True or v is False:
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{v:g}" if isinstance(v, float) else str(v)
    if isinstance(v, list):
        return "[" + ", ".join(tv(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k} = {tv(x)}" for k, x in v.items()) + "}"
    return q(v)


def bg_dirs(zone: Path) -> dict[str, Path]:
    """区里的成员 bg。**区级主体（全境 / 全城）不算**：它的 blocks.toml 由 gen_world_scenes_szzl.py 从
    terrain.toml 重写，写进去的 kind / asset 下次 `--zone` 就没了。"""
    with open(zone.parent.parent / "registry.toml", "rb") as f:
        whole = {r["dir"] for r in tomllib.load(f)["bg"] if r.get("kind") == "zone_whole"}
    return {d.name.split("_", 1)[0]: d for d in zone.iterdir()
            if d.is_dir() and re.match(r"^bg\d+_[^_]+$", d.name) and d.name not in whole
            and (d / "planning" / "blocks.toml").is_file()}


def split_sections(text: str) -> list[list[str]]:
    secs: list[list[str]] = [[]]
    for ln in text.split("\n"):
        if re.match(r"^\[\[?[A-Za-z_]", ln):     # 表头（[meta] / [[block]]）；多行数组的续行是 `[12, 3],`，不算
            secs.append([ln])
        else:
            secs[-1].append(ln)
    return secs


def set_block_keys(toml_p: Path, updates: dict[str, dict[str, object]]) -> int:
    """updates: block id → {key: value}；None 值 ＝ 删掉该键。只改这几个键，块里其余行原样保留。"""
    secs = split_sections(toml_p.read_text(encoding="utf-8"))
    n = 0
    for sec in secs:
        if not sec or sec[0].strip() != "[[block]]":
            continue
        bid = next((re.match(r'^id = "(b\d+)"', l).group(1) for l in sec if re.match(r'^id = "(b\d+)"', l)), None)
        if bid not in updates:
            continue
        upd = updates[bid]
        keep = [l for l in sec if not any(re.match(rf"^{k}\s*=", l) for k in upd)]
        idx = next(i for i, l in enumerate(keep) if l.startswith("id ="))
        new = []
        for k, v in upd.items():
            if v is None:
                continue
            new.append(f"{k} = {tv(v)}")
        sec[:] = keep[:idx + 1] + new + keep[idx + 1:]
        n += 1
    text = "\n".join("\n".join(s) for s in secs)
    tomllib.loads(text)
    toml_p.write_text(text, encoding="utf-8", newline="\n")
    return n


def default_anchor(cfg: dict, bg: str) -> str:
    W, H = cfg["meta"]["size_m"]
    boxes = []
    for b in cfg.get("block", []):
        if b.get("kind") in GROUND:
            continue
        (x, y), (sx, sy) = b["xy"], b["size"]
        r = max(sx, sy) / 2.0 + 2.0
        boxes.append((x - r, y - r, x + r, y + r))
    for fx, fy in ((0.5, 0.92), (0.5, 0.08), (0.08, 0.5), (0.92, 0.5), (0.25, 0.9), (0.75, 0.9)):
        ex, ey = W * fx, H * fy
        if not any(x0 < ex < x1 and y0 < ey < y1 for x0, y0, x1, y1 in boxes):
            eye_h = 1.65 if max(W, H) < 400 else round(max(W, H) / 30.0, 1)
            return (f'\n# 默认校验机位（tools/apply_asset_plan.py，follow-up 007）\n[[anchor]]\nkey = "{bg}-c1"\n'
                    f"eye = [{ex:.0f}, {ey:.0f}]\ntarget = [{W / 2:.0f}, {H / 2:.0f}]\neye_h = {eye_h}\nlens_mm = 28\n"
                    f'note = "场地边缘朝场地中心；自动生成，排镜时按需改"\n')
    # 找不到空地（建筑占满场地，如大教堂）：机位放进室内南端朝北，显式声明 inside
    return (f'\n# 默认校验机位（tools/apply_asset_plan.py，follow-up 007）：场地被体块占满，放在室内\n[[anchor]]\nkey = "{bg}-c1"\n'
            f"eye = [{W / 2:.0f}, {H * 0.85:.0f}]\ntarget = [{W / 2:.0f}, {H * 0.2:.0f}]\neye_h = 1.65\nlens_mm = 24\ninside = true\n"
            f'note = "室内南端朝北；自动生成，排镜时按需改"\n')


def plan_path(zone: Path) -> Path:
    return zone / PLAN_DIR / "plan.toml"


def have_props(zone: Path) -> dict[str, Path]:
    return {d.name.split("_", 1)[0]: d for d in props_lib.scene_objects(zone)}


def make_props(zone: Path, plan: dict, have: dict[str, Path]) -> int:
    """plan 的 [[asset]] ＝ 新物件：键必须是 props/registry.toml 里登记过的 p{N}（`python tools/props_lib.py new …` 领号）。
    已有目录的跳过；只建 `props/p{N}_{名}/asset.toml`，卡由写卡 agent 写。"""
    made = 0
    for a in plan.get("asset", []):
        if a["key"] in have:
            continue
        d = props_lib.props_root(zone) / f"{a['key']}_{a['name_zh']}"
        d.mkdir(parents=True, exist_ok=True)
        lines = ["[asset]", f"key = {q(a['key'])}", f"name_zh = {q(a['name_zh'])}",
                 f"size_m = [{', '.join(f'{float(v):g}' for v in a['size_m'])}]",
                 "queries = [" + ", ".join(q(s) for s in a["queries"]) + "]", f"prompt_en = {q(a['prompt_en'])}",
                 "yaw_deg = 0", f"brief = {q(a.get('brief', ''))}"]
        (d / "asset.toml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        have[a["key"]] = d
        made += 1
    return made


def apply(zone: Path, report: list[str]) -> list[Path]:
    with open(plan_path(zone), "rb") as f:
        plan = tomllib.load(f)
    K = kinds()
    have = have_props(zone)
    make_props(zone, plan, have)
    bgs = bg_dirs(zone)
    per: dict[str, dict[str, dict[str, object]]] = {}
    for u in plan.get("use", []):
        # 旧 v3 卡（LEGACY）的 md 不动；它们的 blocks.toml 只要 plan 里点名了就照写（ep01 的六个场景，2026-09-25）
        if u["bg"] not in bgs:
            continue
        upd: dict[str, object] = {}
        if u.get("parts"):
            bad = [p["asset"] for p in u["parts"] if p["asset"] not in have]
            if bad:
                report.append(f"- ❌ {u['bg']}·{u['block']}：parts 里的资产 {bad} 不在库里也不在 plan 里，跳过")
                continue
            upd = {"kind": "asset", "asset": None, "parts": u["parts"], "face": u.get("face"), "count": None}
        elif u.get("asset"):
            if u["asset"] not in have:
                report.append(f"- ❌ {u['bg']}·{u['block']}：资产 {u['asset']} 不在库里也不在 plan 里，跳过")
                continue
            upd = {"kind": "asset", "asset": u["asset"], "parts": None, "face": u.get("face"),
                   "count": int(u["count"]) if int(u.get("count", 1)) > 1 else None, "layout": u.get("layout")}
        elif u.get("kind") in K:
            upd = {"kind": u["kind"], "asset": None, "parts": None, "face": u.get("face"),
                   "count": int(u["count"]) if u.get("count") else None}
            if u["kind"] in GROUND:
                upd["may_overlap"] = True
        else:
            report.append(f"- ❌ {u['bg']}·{u['block']}：kind={u.get('kind')} 未登记，跳过")
            continue
        per.setdefault(u["bg"], {})[u["block"]] = upd
    touched = []
    for bg, upd in per.items():
        tp = bgs[bg] / "planning" / "blocks.toml"
        set_block_keys(tp, upd)
        cfg = tomllib.loads(tp.read_text(encoding="utf-8"))
        missing = [b["id"] for b in cfg.get("block", []) if "kind" not in b]
        if missing:
            set_block_keys(tp, {m: {"kind": "proxy"} for m in missing})
            report.append(f"- ⚠ {bg}：这些块 plan 里没给判定，先写 kind = \"proxy\"（方盒）：{missing}")
        if not cfg.get("anchor"):
            anc = default_anchor(cfg, bg)
            if anc:
                tp.write_text(tp.read_text(encoding="utf-8").rstrip("\n") + "\n" + anc, encoding="utf-8", newline="\n")
        subprocess.run([sys.executable, str(REPO / "tools" / "build_floorplan.py"), str(bgs[bg])], capture_output=True)
        touched.append(bgs[bg])
    return touched


FIXES = (
    (re.compile(r"「(.+?)」与「(.+?)」平面重叠"), lambda m: [(m.group(2), "may_overlap")]),
    (re.compile(r"「(.+?)」的外廓点 .*?落在山脊里"), lambda m: [(m.group(1), "into_ridge")]),
    (re.compile(r"「(.+?)」坐在河道上"), lambda m: [(m.group(1), "over_water")]),
)


def build(bg_dir: Path, report: list[str]) -> bool:
    tp = bg_dir / "planning" / "blocks.toml"
    for rnd in range(3):
        r = subprocess.run([str(BLENDER), "-b", "--factory-startup", "--python", str(REPO / "tools" / "build_scene.py"),
                            "--", str(bg_dir)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
        out = r.stdout + r.stderr
        if "已存" in out and r.returncode == 0:
            n_proxy = out.count("用方盒占位")
            report.append(f"- ✓ {bg_dir.name}：blend 已建（占位 {n_proxy} 件）")
            return True
        cfg = tomllib.loads(tp.read_text(encoding="utf-8"))
        by_name = {b["name"]: b["id"] for b in cfg.get("block", [])}
        upd: dict[str, dict[str, object]] = {}
        for rx, f in FIXES:
            for m in rx.finditer(out):
                for name, key in f(m):
                    if name in by_name:
                        upd.setdefault(by_name[name], {})[key] = True
                        report.append(f"- ⚙ {bg_dir.name}·{by_name[name]}「{name}」：引擎报错，自动声明 {key} = true")
        eye = re.search(r"机位「(.+?)」的眼位", out)
        if eye:
            text = tp.read_text(encoding="utf-8")
            text = re.sub(r'(\[\[anchor\]\]\nkey = "' + re.escape(eye.group(1)) + r'"\n)', r"\1inside = true\n", text)
            tp.write_text(text, encoding="utf-8", newline="\n")
            report.append(f"- ⚙ {bg_dir.name}：机位 {eye.group(1)} 落在体块内，声明 inside = true")
        if upd:
            set_block_keys(tp, upd)
        if not upd and not eye:
            tail = [l for l in out.splitlines() if l.strip()][-6:]
            report.append(f"- ❌ {bg_dir.name}：build 失败且无法自动处理：{' / '.join(tail)[:400]}")
            return False
    report.append(f"- ❌ {bg_dir.name}：三轮自动处理后仍未建成")
    return False


def check_plan(zone: Path) -> list[str]:
    """plan.toml 覆盖与合法性：每个非旧卡 bg 的每个块都要有且只有一条 [[use]]。"""
    with open(plan_path(zone), "rb") as f:
        plan = tomllib.load(f)
    K = kinds()
    registered = {r["key"] for r in props_lib.registry(zone)}
    keys = set(have_props(zone)) | {a["key"] for a in plan.get("asset", [])}
    errs, seen = [], {}
    for a in plan.get("asset", []):
        for k in ("key", "name_zh", "size_m", "queries", "prompt_en", "brief"):
            if k not in a:
                errs.append(f"asset {a.get('key')} 缺 {k}")
        if a.get("key") not in registered:
            errs.append(f"asset {a.get('key')} 没在 props/registry.toml 登记——用 `python tools/props_lib.py new <剧目录> <名>` 领号")
        if "_" in a.get("name_zh", "") or "/" in a.get("name_zh", ""):
            errs.append(f"asset {a['key']} 的 name_zh 不能含 _ 或 /（它是目录名的一部分）")
    for u in plan.get("use", []):
        k = (u["bg"], u["block"])
        if k in seen:
            errs.append(f"{u['bg']}·{u['block']} 在 [[use]] 里出现两次")
        seen[k] = u
        if u.get("asset") and u["asset"] not in keys:
            errs.append(f"{u['bg']}·{u['block']} 引用的资产 {u['asset']} 不存在")
        if u.get("asset") and u.get("parts"):
            errs.append(f"{u['bg']}·{u['block']} 同时写了 asset 与 parts，只能二选一")
        for p in u.get("parts", []):
            if p.get("asset") not in keys:
                errs.append(f"{u['bg']}·{u['block']} 的 parts 引用的资产 {p.get('asset')} 不存在")
        if not u.get("asset") and not u.get("parts") and u.get("kind") not in K:
            errs.append(f"{u['bg']}·{u['block']} 的 kind={u.get('kind')} 未登记（已有：{' / '.join(sorted(K))}）")
    for bg, d in bg_dirs(zone).items():
        if bg in LEGACY:
            continue
        cfg = tomllib.loads((d / "planning" / "blocks.toml").read_text(encoding="utf-8"))
        miss = [b["id"] for b in cfg.get("block", []) if (bg, b["id"]) not in seen]
        if miss:
            errs.append(f"{bg} 有 {len(miss)} 个块 plan 里没给判定：{miss}")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--build", action="store_true", help="逐个开 Blender 建 blend（串行，rule 4h ⑥）")
    ap.add_argument("--only", nargs="*", default=None, help="只处理这些 bg 键")
    ap.add_argument("--check-plan", action="store_true", help="只核对 plan.toml 的覆盖与合法性，不写盘")
    ap.add_argument("--dirs-only", action="store_true", help="只按 plan 建资产目录 + asset.toml，不动 blocks.toml")
    args = ap.parse_args()
    zone = Path(args.zone).resolve()
    if args.check_plan or args.dirs_only:
        errs = check_plan(zone)
        for e in errs:
            print(f"  ❌ {e}")
        print(f"[{zone.name}] plan.toml：{len(errs)} 处问题")
        if errs or args.check_plan:
            return 1 if errs else 0
        with open(plan_path(zone), "rb") as f:
            plan = tomllib.load(f)
        print(f"[{zone.name}] 新建 prop 目录 {make_props(zone, plan, have_props(zone))} 个")
        return 0
    report: list[str] = [f"# 资产落地报告 · {zone.name}", ""]
    touched = apply(zone, report)
    if args.only:
        touched = [d for d in touched if d.name.split("_", 1)[0] in args.only]
    print(f"[{zone.name}] blocks.toml 已写 {len(touched)} 个 bg")
    if args.build:
        ok = sum(build(d, report) for d in touched)
        print(f"[{zone.name}] blend 建成 {ok} / {len(touched)}")
        for d in touched:          # 自动声明改了 toml → 平面图要重出，W7 才不判过期
            subprocess.run([sys.executable, str(REPO / "tools" / "build_floorplan.py"), str(d)], capture_output=True)
    (zone / PLAN_DIR / "apply_report.md").write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")
    for ln in report[2:]:
        print(ln)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
