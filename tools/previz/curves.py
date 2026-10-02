# -*- coding: utf-8 -*-
"""航线曲线数学 —— `build_bianjing.py`（Blender 内）与 `gen_route_sk1.py`（普通 Python）共用。

为什么单独成模块：与 `city_layout.py` 同一个理由（CLAUDE.md §General coding rules
「一个名字只有一处定义」）。单调插值与侧向加速度这两件事，**航线生成端**要用它判断
「这条航线转得过来吗」、**previz 求解端**要用它判断「这条航线转不过来就 raise」。
两处各写一份的后果不是报错，是两端的判据悄悄分岔——生成时算合格、渲染时被拦下，
或者更糟：生成时算合格、渲染时也没拦，因为两边的公式本来就不一样。

本模块不依赖 bpy；点列用「可索引的三元组」即可（`tuple` 与 `mathutils.Vector` 都行）。
"""
from __future__ import annotations

import math
from typing import Sequence

Pt3 = Sequence[float]


def mono_hermite(ts: list[float], vs: list[float], t: float, ease_in: bool) -> float:
    """Fritsch–Carlson 单调三次插值：关键帧之间不过冲；相邻两帧同值＝悬停（速度归零）。"""
    n = len(ts)
    if n == 1 or t <= ts[0]:
        return vs[0]
    if t >= ts[-1]:
        return vs[-1]
    d = [(vs[i + 1] - vs[i]) / (ts[i + 1] - ts[i]) for i in range(n - 1)]
    m = [d[0]] + [0.0 if d[i - 1] * d[i] <= 0 else (d[i - 1] + d[i]) / 2 for i in range(1, n - 1)] + [d[-1]]
    if ease_in:
        m[0] = 0.0
    for i in range(n - 1):
        if d[i] == 0.0:
            m[i] = m[i + 1] = 0.0
            continue
        a0, b0 = max(0.0, m[i] / d[i]), max(0.0, m[i + 1] / d[i])
        m[i], m[i + 1] = a0 * d[i], b0 * d[i]
        if a0 * a0 + b0 * b0 > 9.0:
            tau = 3.0 / math.sqrt(a0 * a0 + b0 * b0)
            m[i], m[i + 1] = tau * a0 * d[i], tau * b0 * d[i]
    i = max(k for k in range(n - 1) if ts[k] <= t)
    h = ts[i + 1] - ts[i]
    u = (t - ts[i]) / h
    return ((2 * u ** 3 - 3 * u ** 2 + 1) * vs[i] + (u ** 3 - 2 * u ** 2 + u) * h * m[i]
            + (-2 * u ** 3 + 3 * u ** 2) * vs[i + 1] + (u ** 3 - u ** 2) * h * m[i + 1])


def curve_lateral(pts: Sequence[Pt3], fps: int) -> tuple[float, float]:
    """逐帧位置 → 最大侧向加速度 (t, a)：二阶差分取加速度，再取垂直于速度的分量。

    为什么是这个量：相机就是**按帧**被 key 的，帧率下的二阶差分就是它真实经历的加速度；
    而「相邻速度夹角 ÷ dt」随采样间隔漂移（密采样上任何抖动都读成几十 g，闸门失灵），
    三点外接圆半径在近共线时又会数值退化 —— 两个都试过，都不能用（2026-09-18）。
    """
    worst = (0.0, 0.0)
    for i in range(1, len(pts) - 1):
        a_, b_, c_ = pts[i - 1], pts[i], pts[i + 1]
        v = [(c_[k] - a_[k]) * (fps / 2.0) for k in range(3)]
        vl = math.sqrt(sum(x * x for x in v))
        if vl < 1.0:                             # 近乎悬停：侧向加速度无意义
            continue
        a = [(c_[k] - 2.0 * b_[k] + a_[k]) * (fps * fps) for k in range(3)]
        u = [x / vl for x in v]
        dot = sum(a[k] * u[k] for k in range(3))
        a_lat = math.sqrt(sum((a[k] - u[k] * dot) ** 2 for k in range(3)))
        if a_lat > worst[1]:
            worst = ((i + 1) / fps, a_lat)
    return worst


def resample(pts: Sequence[Pt3], step_m: float) -> list[tuple[float, ...]]:
    """折线 → 等弧长点列。**先等距、再滤波**：按时间采样得到的点空间上疏密不均，
    在那种点列上做滑动平均等于变频滤波，会造出新的折角（build_bianjing 2026-09-18 踩过）。"""
    dim = len(pts[0])
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a[:dim], b[:dim]))
    L = acc[-1] or 1.0
    n = max(8, int(L / step_m))
    out, j = [], 1
    for i in range(n + 1):
        target = L * i / n
        while j < len(acc) - 1 and acc[j] < target:
            j += 1
        a0, a1 = acc[j - 1], acc[j]
        r = 0.0 if a1 - a0 < 1e-9 else (target - a0) / (a1 - a0)
        out.append(tuple(pts[j - 1][k] + (pts[j][k] - pts[j - 1][k]) * r for k in range(dim)))
    return out


def low_pass(pts: Sequence[Pt3], win: int) -> list[tuple[float, ...]]:
    """等距点列的箱式低通。两端**沿切向延长补齐**——否则窗口在端点被截断、端点附近等于
    没滤，起飞后一秒就会留下一个 1.5 g 的折角（2026-09-18 实测 1.36s 处 14.3 m/s²）。"""
    if win <= 0:
        return [tuple(p) for p in pts]
    dim = len(pts[0])
    head = [pts[1][k] - pts[0][k] for k in range(dim)]
    tail = [pts[-1][k] - pts[-2][k] for k in range(dim)]
    ext = ([tuple(pts[0][k] - head[k] * (win - i) for k in range(dim)) for i in range(win)]
           + [tuple(p) for p in pts]
           + [tuple(pts[-1][k] + tail[k] * (i + 1) for k in range(dim)) for i in range(win)])
    out = []
    for i in range(win, win + len(pts)):
        w = ext[i - win:i + win + 1]
        out.append(tuple(sum(q[k] for q in w) / len(w) for k in range(dim)))
    return out


def low_pass_pinned(pts: Sequence[Pt3], win: int, max_dev: float, feather: int,
                    limits: Sequence[float] | None = None) -> list[tuple[float, ...]]:
    """低通 + 三条约束：偏离原线不超过上限、首末点逐值钉回原处、上限可以**逐点不同**。

    为什么要逐点不同：门洞只有 24 m 宽，低通把航线推偏两三米就贴墙；而城区段恰恰需要
    大窗口才压得平那几个折角。一个全局系数满足不了两边——门口收紧则城区压不平，
    城区放开则门口被推出洞外（两种都实测过）。做法是给每个点一个上限，
    按 `min(1, 上限/偏移)` 算逐点回blend系数，**再把这个系数本身低通一遍**：
    系数变化平缓，两条光滑曲线的插值就仍然光滑，不会像硬截断那样留下折角。
    """
    dim = len(pts[0])
    sm = low_pass(pts, win)
    devs = [math.sqrt(sum((a[k] - b[k]) ** 2 for k in range(dim))) for a, b in zip(sm, pts)]
    if limits is None:
        # 默认：**整条线一个系数**（全局 blend）。逐点截断会在「刚好顶到上限」的那一帧
        # 留下折角，而整条回blend 是两条光滑曲线的线性插值，仍然光滑。
        peak = max(devs) or 1.0
        alpha = [1.0 if peak <= max_dev else max_dev / peak] * len(pts)
    else:
        alpha = [1.0 if d <= 1e-9 else min(1.0, limits[i] / d) for i, d in enumerate(devs)]
        # 固定窗口（不随 win 变大）：用 win 去平滑系数，等于把门洞那一点的严格上限
        # 摊到上百米以外，收紧就失效了——实测门洞被推偏 12.8 m。
        aw = 40
        pad = [alpha[0]] * aw + alpha + [alpha[-1]] * aw
        alpha = [sum(pad[i - aw:i + aw + 1]) / (2 * aw + 1) for i in range(aw, aw + len(alpha))]
    out = [tuple(b[k] + (a[k] - b[k]) * alpha[i] for k in range(dim))
           for i, (a, b) in enumerate(zip(sm, pts))]
    # 两端羽化回原线：**整段渐回原曲线**，不只是把端点平移回去。
    # 只平移端点会保住位置、保不住**切向**——实测末帧航向差 2.2°，而末帧航向是接缝契约
    # 的一部分（下一镜按它排头 70 m 的直线平飞），2° 就够在缝后看出一次轻微的摆头。
    n = len(out)
    for end in (0, n - 1):
        for j in range(min(feather, n)):
            i = j if end == 0 else n - 1 - j
            w = 0.5 * (1.0 + math.cos(math.pi * j / max(1, feather)))
            out[i] = tuple(out[i][k] * (1.0 - w) + pts[i][k] * w for k in range(dim))
    return out
