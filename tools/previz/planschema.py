# -*- coding: utf-8 -*-
"""场地平面图（floor plan）的 **schema + 解析 + 校验**——`ai_video.md` rule 4k 的可执行版。

**本模块不 import bpy**，所以平面图生成器、Blender 场景引擎、以及任何 shot 层工具
都能 import 同一份判据（`一个名字只有一处定义`）。
凡是需要「先起一个 Blender」才能跑的检查一律不放这里——那种检查会被跳过，
而**被跳过的检查比没有更糟，因为它会被当成跑过了**。

## 一张图挂在哪一级：挂在**一个坐标系**上

一个 floor plan ＝ 一个原点 + 一套米制 + 一组footprint。
**每个 `bg{N}_*` 目录都必须能解析到恰好一份图，但不必自己拥有一份。**
四问，按顺序问，只看目录名就能答：

1. 动了 A 里的一堵墙，B 里的同一堵墙要不要跟着动？ → 要 → **同一份图**
2. A 与 B 只差机位 / 镜头 / 光 / 天气 / 时辰？ → **同一份图**，B 什么都不拥有
3. A 与 B 差在「哪些结构存在」？ → **同一份图** + `[meta] states` + 每块 `state_in`
4. A 与 B 是同一批 footprint 的不同**分辨率**（山谷 260×300 vs 修道院 90×90）？
   → **两份图**，子图声明 `[meta] parent`

**拥有的判据是文件系统级的**：目录下有 `planning/blocks.toml` ＝ 拥有。
否则必须有一份三行的 `planning/plan.toml`（`plan = "<相对路径>"` + `state=` 或 `anchor=`），
解析不到就报错。这样「每个 bg 都有 floor plan」在文件系统上字面成立，而**几何只有一份**。

**反面写死，免得日后重新争论**：给「原始 / 骨架 / 覆顶中」开三份 toml 是**禁止**的——
台地边缘、林线、坑位会被录三遍；谁挪了一根柱子，三张图就开始各说各话**而且三张看上去都对**；
到 shot 层的症状就是那条自己把自己填回去的沟（rule 16 ③ / 16.10，两条都是本仓库真实事故）。

## 必填是刻意压到最少的

一份没人写得起的标准比没有标准更糟。所以：
**基础必填 6 个 meta + 5 个 block 字段**，其余一律「下游需要时才声明」。
**零个 `[[block]]` 是合法的**——全仓一大半 bg 是没有建筑的自然场景（林中列柱 / 冰湖 / 溪谷 /
巷道），图的内容是 `[[ridge]]` / `[[water]]` / `[[road]]` 与自然类 block。
硬要它们「标出所有建筑物」，作者只会**编出建筑**或者**干脆不画**。
"""
from __future__ import annotations

import hashlib
import math
import os
import re
import tomllib

# 尺度来源。与 block 的 src 共享词汇，只是少了「原典方位」（方位不构成尺度）、
# 多了「实测」（在客户端/现场量过）。**推定的在图上挂 ⚠，且不设抑制开关。**
SCALE_SRC: tuple[str, ...] = ("实测", "原典", "坐标表", "地图量取", "推定")
SRC: tuple[str, ...] = ("原典方位", "坐标表", "地图量取", "推定")
ID_RE = re.compile(r"^b\d{2,3}$")
BG_DIR_RE = re.compile(r"^bg\d+_")

PLAN_FILE = os.path.join("planning", "blocks.toml")
POINTER_FILE = os.path.join("planning", "plan.toml")


class Unresolved(Exception):
    pass


def is_bg_dir(path: str) -> bool:
    return os.path.isdir(path) and bool(BG_DIR_RE.match(os.path.basename(path)))


def owns_plan(bg_dir: str) -> bool:
    return os.path.isfile(os.path.join(bg_dir, PLAN_FILE))


def resolve(bg_dir: str) -> tuple[str, dict]:
    """`bg_dir` → (拥有图的目录, 指针里的附加声明)。自己拥有就返回自己。

    **解析不到就抛**——这是「每个 bg 必备」真正咬人的地方：
    下游（`build_scene` / previz / shot_plan）跑不起来，而不是靠一次全仓盘点去点名。
    这样**新活被挡住、没动过的旧剧一个都不扫**（CLAUDE.md 2026-09-06）。
    """
    bg_dir = os.path.abspath(bg_dir)
    if owns_plan(bg_dir):
        return bg_dir, {}
    ptr = os.path.join(bg_dir, POINTER_FILE)
    if not os.path.isfile(ptr):
        raise Unresolved(
            "%s 既没有 planning/blocks.toml（＝自己拥有一份图），"
            "也没有 planning/plan.toml（＝指向拥有它的那个目录）。\n"
            "二选一：① 这是一个独立坐标系 → 写 blocks.toml；"
            "② 它与别的 bg 是同一块地 → 写三行 plan.toml：\n"
            '  plan = "../bg1_xxx"\n  state = "骨架"      # 或 anchor = "bg1-2_xxx"'
            % os.path.relpath(bg_dir))
    with open(ptr, "rb") as f:
        p = tomllib.load(f)
    target = p.get("plan")
    if not target:
        raise Unresolved("%s 缺 `plan = \"<相对路径>\"`" % os.path.relpath(ptr))
    owner = os.path.abspath(os.path.join(bg_dir, target))
    if not owns_plan(owner):
        raise Unresolved("%s 指向 %s，但那里没有 planning/blocks.toml"
                         % (os.path.relpath(ptr), target))
    return owner, p


def load(owner_dir: str) -> dict:
    with open(os.path.join(owner_dir, PLAN_FILE), "rb") as f:
        return tomllib.load(f)


def sha(owner_dir: str) -> str:
    """图的收据。PNG 页脚与 md 抬头各印一份，**看图的人才知道自己批的是哪一版**。"""
    with open(os.path.join(owner_dir, PLAN_FILE), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


def corners(b: dict) -> list[tuple[float, float]]:
    x, y = b["xy"]
    sx, sy = b["size"]
    r = math.radians(float(b.get("rot", 0)))
    c, s = math.cos(r), math.sin(r)
    return [(x + dx * c - dy * s, y + dx * s + dy * c)
            for dx, dy in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2))]


def check(cfg: dict, scene_dir: str, known_bg: dict[str, str] | None = None) -> list[str]:
    """返回 blocker 列表（空 ＝ 过）。**只查能从这一份文件里查出来的事。**"""
    errs: list[str] = []
    meta = cfg.get("meta", {})

    for k in ("bg", "name_zh", "size_m", "scale_note", "scale_src"):
        if k not in meta:
            errs.append("[meta] 缺 `%s`" % k)
    if meta.get("scale_src") and meta["scale_src"] not in SCALE_SRC:
        errs.append("[meta] scale_src 越界：%s（只许 %s）"
                    % (meta["scale_src"], " / ".join(SCALE_SRC)))
    W, H = (meta.get("size_m") or [0, 0])[:2]

    states = meta.get("states") or []
    if meta.get("covers") and not states and any(
            (c.get("state") if isinstance(c, dict) else None) for c in meta["covers"]):
        errs.append("[meta] covers 里出现了 state，但没有 [meta] states 列出它们的顺序")

    parent = os.path.dirname(os.path.abspath(scene_dir))
    siblings = {n.split("_", 1)[0]: n for n in os.listdir(parent)
                if is_bg_dir(os.path.join(parent, n))} if os.path.isdir(parent) else {}
    known = known_bg if known_bg is not None else siblings

    claimed: set[str] = set()
    for c in meta.get("covers", []):
        d = c.get("dir") if isinstance(c, dict) else c
        if not d:
            errs.append("[meta] covers 有一项没写 dir")
            continue
        if not os.path.isdir(os.path.join(parent, d)):
            errs.append("[meta] covers 指向不存在的目录：%s" % d)
        if d in claimed:
            errs.append("[meta] covers 重复认领同一个目录：%s" % d)
        claimed.add(d)
        st = c.get("state") if isinstance(c, dict) else None
        if st and states and st not in states:
            errs.append("[meta] covers 里的 state「%s」不在 [meta] states 里" % st)

    seen_id: set[str] = set()
    seen_name: set[str] = set()
    for b in cfg.get("block", []):
        n = b.get("name", "?")
        for k in ("id", "name", "xy", "size", "src", "h_m"):
            if k not in b:
                errs.append("block「%s」缺 `%s`" % (n, k))
        if n in seen_name:
            errs.append("block 名字重复：%s" % n)
        seen_name.add(n)

        bid = b.get("id", "")
        if bid:
            if not ID_RE.match(bid):
                errs.append("block「%s」的 id=%s 不合式（要 b + 2~3 位数字，如 b01）" % (n, bid))
            if bid in seen_id:
                errs.append("block id 重复：%s（%s）" % (bid, n))
            seen_id.add(bid)

        if b.get("src") not in SRC:
            errs.append("block「%s」的 src 越界：%s（只许 %s）" % (n, b.get("src"), " / ".join(SRC)))

        h = b.get("h_m")
        if h is not None and (not isinstance(h, (int, float)) or h < 0):
            errs.append("block「%s」的 h_m=%r 不是 ≥0 的数（0 是合法值：草坪 / 石板地）" % (n, h))

        key = (b.get("bg") or "").strip()
        if key and key not in known:
            errs.append("block「%s」的 bg 键 %s 在同级目录下没有对应的 bg 目录（现有：%s）"
                        % (n, key, " ".join(sorted(known)) or "无"))

        if "xy" in b and "size" in b and W and H:
            out = [p for p in corners(b) if not (-1e-6 <= p[0] <= W + 1e-6 and -1e-6 <= p[1] <= H + 1e-6)]
            if out:
                # 只测中心的旧版会漏掉「rot=90 的长墙有一半在场地外」这种，
                # 而图上看它就是贴着边，完全看不出来。
                errs.append("block「%s」旋转后有 %d 个角超出场地 %g×%g（如 %.1f, %.1f）"
                            % (n, len(out), W, H, out[0][0], out[0][1]))

        st = b.get("state_in")
        if st and not states:
            errs.append("block「%s」写了 state_in，但 [meta] 没有 states" % n)
        for s in (st or []):
            if s not in states:
                errs.append("block「%s」的 state_in 含未声明的 state：%s" % (n, s))

    return errs


def audit(root: str) -> list[tuple[str, str, str]]:
    """全仓覆盖率：每个 bg 目录 → (目录, 状态, 说明)。**只报告，不判错。**"""
    rows: list[tuple[str, str, str]] = []
    for dp, dirs, _files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("_deleted", "renders", "previz", "frames", "__pycache__")]
        if not is_bg_dir(dp):
            continue
        try:
            owner, ptr = resolve(dp)
            if owner == os.path.abspath(dp):
                rows.append((dp, "owns", ""))
            else:
                tag = ptr.get("state") or ptr.get("anchor") or ""
                rows.append((dp, "points", "%s%s" % (os.path.basename(owner), " · " + tag if tag else "")))
        except Unresolved:
            rows.append((dp, "missing", ""))
    return rows
