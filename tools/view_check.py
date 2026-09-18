# -*- coding: utf-8 -*-
"""机检「三视图塌成一个轴」——把只有人眼能发现的缺陷变成一条可跑的判据。

为什么要有这个文件
------------------
2026-09-17 这个缺陷出现了**两次**，两次都是靠人眼盯出来的：
  · 第一次 p22 素木床榻（宽1.1 × 长2.0 × 高0.6）——用户报的「object 长得和图片不是一个东西」。
    模型把 2.0 m 的长边当成了正面，接着「侧面」又画了一次长边。
  · 第二次 p12 漕船（宽4.5 × 长18 × 高3）——改完 prompt 之后我自己抽查才发现，
    「正面」仍然是和侧面一模一样的舷侧视图。
三张图落在同一个轴上，喂进 image-to-3D 等于只给了一个方向的信息，出来的网格和图不是一个东西。
而这件事**是可量的**：每张图里主体的外轮廓宽高比，应该和卡里声明的那一面对得上。
`whitemodel_normalize` 的包围盒检查抓的是「网格对不对」，抓不到「输入的图本来就错了」——
错在更上游，闸门只能看见它的下游结果（而且还会被 vendor 的压方行为混淆）。本文件补的是上游那一关。

怎么量
------
正交三视图的背景是**纯中性浅灰**（`gen_object_cards.ORTHO` 写死的），所以主体 ＝ 与四角中位色
差得够远的像素。取这些像素的包围盒，得到实测宽高比，与 `object_inventory.toml` 的尺寸算出的
应有宽高比比对。判据只看**比值的比值**，对裁切边距、分辨率、主体在画面里占多大都免疫。

两条判据（都可证伪）：
  ① **各视图自身**：实测宽高比 ÷ 声明宽高比 落在 [1/TOL, TOL] 内。
  ② **视图之间**：声明里差得多的两张（比值 ≥ DIFF），实测也必须差得多。
     这一条才是真正抓「塌成一个轴」的——①有时会被主体自带的附件（桅杆、伞柄）糊过去。

用法（仓库根目录）：
    python tools/view_check.py                # 查全部已出图的物件
    python tools/view_check.py --only p12,p22
    python tools/view_check.py --json         # 给 CI / 生成器当闸门用
退出码 1 ＝ 有物件没过，可以直接挂进出图流程。
"""
from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SK1 = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "2_世界观人设"
PROPS = SK1 / "props"

TOL = 1.45        # 判据①（warning）：单张实测 ÷ 声明 的容许倍数
DIFF = 1.8        # 判据②（硬失败）：声明宽高比差到这个倍数以上，实测也必须看得出来
#
# DIFF 为什么正好是 1.8：它是**判得动**与**判不动**之间那条线，由实测四例定的，不是拍的。
#   p12 漕船   声明差 4.00 倍  —— 塌陷，必须抓到
#   p27 挑担货筐 声明差 4.00 倍  —— 塌陷，必须抓到
#   p22 素木床榻 声明差 1.82 倍  —— 用户报的那一个，必须抓到 → 所以 DIFF 不能 > 1.82
#   p25 插柳暖轿 声明差 1.60 倍  —— **没塌**（正视图门帘、侧视图窗），腐蚀后核心 0.68 vs 0.80
#                                 仍分不开；声明本身就只差 1.6 倍，这一档量不动 → 让它退出判定
# 也就是说：声明宽高比差不到 1.8 倍的两个面，本工具**不声称**能分辨，不报也不背书。
SIM = 0.80        # 判据②的第二个信号：两张主体裁切图的相似度 ≥ 它才算"真的没转"
SEP = 1.35        # ……看得出来的下限（实测差异 ≥ 它才算两张不同的视图）

# 为什么①只报 warning：**声明尺寸量的是主体，剪影量的是主体＋附件。**
# 实测两例（都确认图本身是对的）：p25 插柳暖轿轿身 1.0 × 1.7、但两根抬杆左右伸出去，
# 剪影成了 1.02:1；p12 漕船侧视图船体约 6:1、但竖着的桅杆把剪影高度抬到 2.49:1。
# 把①判死就会把这两张正确的图毙掉。真正要抓的缺陷是②——三张图塌到同一个轴上，
# 那是 image-to-3D 拿不到第二个方向信息的根因，而它对附件免疫（附件在三张里都在）。

# 视图 n → (水平方向取 size 的哪一项, 垂直方向取哪一项)；与 gen_object_cards.VIEWS 同一张表。
# 第三张可以是背面（与正面同轴）或俯视（清单里 `view3 = "俯视"`），两者量的轴不同。
AXES = {1: (0, 2), 2: (1, 2), 3: (0, 2)}
AXES_TOP = {1: (0, 2), 2: (1, 2), 3: (0, 1)}


def _subject(png: Path) -> tuple[float, np.ndarray, float | None] | None:
    """(外轮廓宽÷高, 主体裁切归一到 96×96 的灰度图, 腐蚀掉附件后的核心宽÷高)。背景＝四角中位色。"""
    im = Image.open(png).convert("L")
    a = np.asarray(im, dtype=np.int16)
    h, w = a.shape
    k = max(4, min(h, w) // 40)
    corners = np.concatenate([a[:k, :k].ravel(), a[:k, -k:].ravel(),
                              a[-k:, :k].ravel(), a[-k:, -k:].ravel()])
    bg = float(np.median(corners))
    mask = np.abs(a - bg) > 12
    if mask.sum() < (h * w) * 0.005:          # 几乎全是背景：这张图没主体
        return None
    ys, xs = np.where(mask)
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    if y1 <= y0 or x1 <= x0:
        return None
    crop = Image.fromarray(np.asarray(im)[y0:y1, x0:x1]).resize((96, 96), Image.BILINEAR)
    return (x1 - x0) / (y1 - y0), np.asarray(crop, dtype=np.float32), core_aspect(mask)


def core_aspect(mask: np.ndarray) -> float | None:
    """**腐蚀掉细附件之后**的主体核心 宽÷高。判据②量的就是它。

    为什么不用整张剪影：声明尺寸量的是**主体**，剪影量的是**主体＋附件**，两者口径不同。
    实测三例：p25 插柳暖轿的两根抬杆在正/侧两张里都横着伸出去（剪影都成 0.93:1，
    可轿身明明转了——一张门帘一张窗）；p12 漕船竖着的桅杆把侧视图剪影从 6:1 压到 2.49:1；
    p14 油纸伞的伞柄同理。腐蚀核按短边的百分比取，比细杆粗、比主体细，一刀砍掉附件。

    腐蚀是**可分离**的（先按行取最小、再按列取最小），所以是 O(k) 两遍、不是 O(k²)：
    PIL 的 MinFilter 在 1024² 上用 46 的核要跑好几分钟，这里毫秒级。
    """
    def erode1(a: np.ndarray, k: int, axis: int) -> np.ndarray:
        a = np.moveaxis(a, axis, -1)
        pad = np.pad(a, ((0, 0), (k // 2, k // 2)), constant_values=True)
        w = np.lib.stride_tricks.sliding_window_view(pad, k, axis=-1)
        return np.moveaxis(w.min(axis=-1), -1, axis)

    h, w = mask.shape
    k = max(3, (min(h, w) // 22) | 1)            # 奇数；约短边的 4.5%
    er = erode1(erode1(mask, k, 1), k, 0)
    if er.sum() < mask.sum() * 0.05:             # 腐蚀过头（主体本身就细）——退回整张剪影
        er = mask
    ys, xs = np.where(er)
    dy, dx = int(ys.max() - ys.min()) + 1, int(xs.max() - xs.min()) + 1
    return dx / dy if dy else None


def subject_aspect(png: Path) -> float | None:
    s = _subject(png)
    return None if s is None else s[0]


def look_alike(a: np.ndarray, b: np.ndarray) -> float:
    """两张主体裁切图的相似度 0..1（1 ＝ 一模一样）。归一到同一尺寸后比皮尔逊相关。

    为什么需要它：剪影宽高比**会被附件主导**。p25 插柳暖轿的两根抬杆在正视图与侧视图里
    都横着伸出去，于是两张的外轮廓都是 0.93:1 —— 光看剪影像是"塌成了一个轴"，
    可轿身明明转了（一张是门帘、一张是窗）。真正的塌陷（p12 最初的 -1 与 -2）是
    **两张图几乎一模一样**。所以判死要两个信号同时成立：剪影没差 ∧ 画面也没差。
    """
    x, y = a.ravel() - a.mean(), b.ravel() - b.mean()
    d = float(np.linalg.norm(x) * np.linalg.norm(y))
    return 0.0 if d < 1e-6 else float(np.dot(x, y) / d)


def check(o: dict) -> dict:
    key, size = o["key"], [float(v) for v in o["size"]]
    fold = next(iter(sorted(PROPS.glob(f"{key}_*"))), None)
    out: dict = {"key": key, "name": o["name"], "views": {}, "problems": [], "warnings": []}
    crops: dict[int, np.ndarray] = {}
    if fold is None:
        out["problems"].append("没有物件目录")
        return out
    for n, (hi, vi) in (AXES_TOP if o.get("view3") == "俯视" else AXES).items():
        png = fold / f"{key}-{n}.png"
        if not png.is_file():
            continue
        s = _subject(png)
        got = None if s is None else s[0]
        want = size[hi] / size[vi]
        out["views"][n] = {"want": round(want, 3), "got": None if got is None else round(got, 3)}
        if s is not None:
            crops[n] = s[1]
            out["views"][n]["core"] = None if s[2] is None else round(s[2], 3)
        if got is None:
            out["problems"].append(f"视图{n} 抠不出主体（整张接近背景色）")
            continue
        r = got / want
        if not (1 / TOL <= r <= TOL):
            out["warnings"].append(
                f"视图{n} 宽高比 {got:.2f} 与声明 {want:.2f} 差 {max(r, 1 / r):.2f} 倍"
                f"（这一面应当是 {size[hi]:g} × {size[vi]:g} m）")
    # 判据②：声明里差得多的两张，实测也得差得多
    for a, b in ((1, 2), (2, 3)):
        va, vb = out["views"].get(a), out["views"].get(b)
        if not (va and vb and va["got"] and vb["got"]):
            continue
        want_d = max(va["want"] / vb["want"], vb["want"] / va["want"])
        ca, cb = va.get("core") or va["got"], vb.get("core") or vb["got"]
        got_d = max(ca / cb, cb / ca)
        if want_d < DIFF or got_d >= SEP:
            continue
        sim = look_alike(crops[a], crops[b]) if a in crops and b in crops else 1.0
        msg = (f"视图{a} 与 视图{b}：声明宽高比差 {want_d:.1f} 倍"
               f"（{va['want']:.2f} vs {vb['want']:.2f}），实测只差 {got_d:.2f} 倍"
               f"（核心 {ca:.2f} vs {cb:.2f}），画面相似度 {sim:.2f}")
        if sim >= SIM:
            out["problems"].append("塌成了同一个轴 —— " + msg)
        else:
            out["warnings"].append("剪影被附件主导（画面确实转了）—— " + msg)
    out["ok"] = not out["problems"]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    objs = tomllib.loads((SK1 / "object_inventory.toml").read_text(encoding="utf-8"))["object"]
    rows = [check(o) for o in objs if not only or o["key"] in only]
    rows = [r for r in rows if r["views"]]
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    else:
        for r in rows:
            mark = "✓" if r["ok"] else "✗"
            seen = "  ".join(f"视图{n} {v['got']}/{v['want']}"
                             for n, v in sorted(r["views"].items()) if v["got"])
            print(f"{mark} {r['key']:5}{r['name']:14}{seen}")
            for p in r["problems"]:
                print(f"    ✗ {p}")
            for p in r["warnings"]:
                print(f"    ! {p}（剪影含附件时这条会误报，见抬头）")
        bad = [r["key"] for r in rows if not r["ok"]]
        print(f"\n{len(rows) - len(bad)}/{len(rows)} 过；不过的：{bad or '无'}")
    sys.exit(1 if any(not r["ok"] for r in rows) else 0)


if __name__ == "__main__":
    main()
