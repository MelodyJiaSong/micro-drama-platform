# -*- coding: utf-8 -*-
"""t12 神经网络与深度学习的全部实验数据：numpy 真训练、断言讲稿里的说法，写成 scenes/data.json 给网页场景用。

    python edu_videos/ai_terms/t12_neural_networks/scenes/data.py

主例子（示意数据）：同样跑五公里，一天里不同时刻出发的车费。白天的价从第 1 季共用数据 `_shared/s1_data.py` 学出的
两个旋钮算（起步价 + 每公里 × 5），早晚高峰加价、深夜加价，所以车费随时刻是弯的。
1) 两个旋钮的直线（车费 = 旋钮 1 + 旋钮 2 × 时刻）最好也只能平平地穿过去：最小二乘的最优直线，损失（均方误差）约 11.5。
2) 神经网络：输入 1 个（出发时刻）→ 第一层 12 个小单元（每个 2 个旋钮：w、b；输出 max(0, w·x + b)，小于零就当零，是一条折线）
   → 第二层 1 个单元把 12 条折线各乘一个旋钮再加一个旋钮（12 + 1）。共 12×2 + 13 = 37 个旋钮。
   用梯度下降（带动量）拧 1 万步，损失压到 0.3 以下；把曲线拆开，正好是 12 条折线之和。
3) 为什么要叠深（构造的例子）：每层两个单元能把一段斜线「对折」一次（帐篷形）；一层叠一层，折线的段数每层翻一倍。
   同样 10 个单元：并排一层最多 11 段；叠成 5 层是 32 段。
讲稿里的数字都由下面的断言守住；数据变了先改讲稿。t13 反向传播参照这里的网络结构（见本期 README）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_shared"))
import s1_data  # noqa: E402  第 1 季共用打车数据（只读）

KM = 5.0
DAY = float(s1_data.best_base + s1_data.best_per_km * KM)   # 两旋钮模型说的「白天五公里」车费
H_UNITS = 12
SEED, LR, MOM, STEPS = 0, 0.05, 0.9, 10000
SNAPS = [0, 30, 100, 250, 600, 1500, 4000, 10000]   # 训练过程中存下曲线的步数（画面上曲线一步步弯过去）


def fare_rule(h):
    """示意的「真实」车费：白天价 ×（1 + 早高峰 + 晚高峰 + 深夜加价）。"""
    g = lambda c, w: np.exp(-0.5 * ((h - c) / w) ** 2)
    night = 1 / (1 + np.exp(-(h - 23) * 3)) + 1 / (1 + np.exp((h - 5) * 3))
    return DAY * (1 + 0.40 * g(8.2, 0.9) + 0.50 * g(18.3, 1.1) + 0.25 * night)


def rides():
    rng = np.random.default_rng(1205)
    h = np.sort((np.arange(48) + rng.uniform(0, 1, 48)) / 2)       # 每半小时一趟，时刻略有前后
    y = np.round(fare_rule(h) + rng.normal(0, 0.6, h.size), 1)
    return h, y


# 网络内部用缩放后的数：x = (时刻 − 12) / 12 ∈ [−1, 1]，t = (车费 − 30) / 10
sx = lambda h: (h - 12) / 12
sy = lambda y: (y - 30) / 10
uy = lambda t: t * 10 + 30


def forward(P, x):
    W1, b1, W2, b2 = P
    z = np.outer(x, W1) + b1
    a = np.maximum(z, 0)
    return z, a, a @ W2 + b2


def train(h, y):
    r = np.random.default_rng(SEED)
    W1 = r.choice([-1, 1], H_UNITS) * r.uniform(1, 2, H_UNITS)
    b1 = -W1 * (np.linspace(-1, 1, H_UNITS) + r.uniform(-.05, .05, H_UNITS))   # 折点起初均匀撒在一天里
    W2 = r.normal(0, 0.2, H_UNITS)
    P = [W1, b1, W2, np.array(0.0)]
    V = [np.zeros_like(q) for q in P]
    x, t = sx(h), sy(y)
    hist, snaps = [], {}
    for it in range(STEPS + 1):
        z, a, p = forward(P, x)
        e = p - t
        loss = float(np.mean((uy(p) - uy(t)) ** 2))   # 用「元²」报损失，和直线的损失同一把尺
        hist.append(loss)
        if it in SNAPS:
            snaps[it] = [q.copy() for q in P]
        if it == STEPS:
            break
        gp = 2 * e / len(x)                            # 坡度（这里用反向传播算，片中留到下一期讲）
        gz = np.outer(gp, P[2]) * (z > 0)
        G = [(gz * x[:, None]).sum(0), gz.sum(0), a.T @ gp, np.array(gp.sum())]
        for i in range(4):
            V[i] = MOM * V[i] - LR * G[i]
            P[i] = P[i] + V[i]
    return P, hist, snaps


def pieces(f, xs):
    """数一条折线有几段（相邻斜率明显变了就算新的一段）。"""
    s = np.diff(f(xs)) / np.diff(xs)
    return int(1 + np.sum(np.abs(np.diff(s)) > 1e-6))


def main() -> None:
    h, y = rides()
    assert len(h) == 48
    day = (h > 10) & (h < 16)
    assert abs(np.mean(y[day]) - DAY) < 0.6, "白天就是两旋钮模型说的价"
    assert y[(h > 7.5) & (h < 9)].mean() > DAY * 1.3 and y[(h > 17.5) & (h < 19)].mean() > DAY * 1.35, "早晚高峰贵"
    assert y[(h < 4) | (h > 23.5)].mean() > DAY * 1.15, "深夜也贵"

    # 1) 两个旋钮的直线：最小二乘最优
    A = np.c_[np.ones_like(h), h]
    k = np.linalg.lstsq(A, y, rcond=None)[0]
    line_loss = float(np.mean((A @ k - y) ** 2))
    assert 10 < line_loss < 13, line_loss
    assert abs(k[1]) < 0.15, "最好的直线几乎是平的"
    # 再怎么拧都不行：在一大片拧法里找，都不比最优直线好
    gb, gk = np.meshgrid(np.linspace(15, 40, 251), np.linspace(-1, 1, 201))
    grid_loss = ((gb[..., None] + gk[..., None] * h - y) ** 2).mean(-1)
    assert grid_loss.min() >= line_loss - 1e-6

    # 2) 神经网络 1 → 12 → 1
    P, hist, snaps = train(h, y)
    n_knobs = sum(q.size for q in P)
    assert n_knobs == 37, n_knobs
    net_loss = hist[-1]
    assert net_loss < 0.3, net_loss
    assert net_loss < line_loss / 30, "网络的损失比直线小一个数量级以上"
    sl = [hist[s] for s in SNAPS]
    assert sl[0] > line_loss and all(u >= v for u, v in zip(sl, sl[1:])), "训练前比直线还差，越训越好"
    hh = np.linspace(0, 24, 241)
    z, a, p = forward(P, sx(hh))
    parts = a * P[2]                                   # 每个单元的贡献：一条折线
    assert np.allclose(parts.sum(1) + P[3], p), "曲线 = 12 条折线之和 + 一个常数"
    alive = int(np.sum(np.any(a > 0, axis=0)))
    kinks = sorted(float(12 - 12 * b / w) for w, b in zip(P[0], P[1]) if 0 < 12 - 12 * b / w < 24)
    # 高峰、深夜都抓住了：网络在这些时刻的预测贴着数据
    pred = uy(forward(P, sx(h))[2])
    for lo, hi in ((7.5, 9), (17.5, 19), (0, 4), (10, 16)):
        m = (h > lo) & (h < hi)
        assert np.abs(pred[m] - y[m]).mean() < 1.0, (lo, hi)
    # 直线平平地穿过去：高峰说便宜了、白天说贵了，各差三块钱以上
    for lo, hi, sign in ((7.5, 9, -1), (17.5, 19, -1), (10, 16, 1)):
        m = (h > lo) & (h < hi)
        assert sign * ((A @ k)[m] - y[m]).mean() > 3.0, ("直线在这里差得远", lo, hi)

    # 单元示意：一个单元 = 直线 + 「小于零就当零」→ 折线（折点在 w、b 定的位置）
    demo_w, demo_b = 1.6, -0.4                          # 缩放后的旋钮读数；折点 x = 0.25 → 15 点
    demo = {"w": demo_w, "b": demo_b, "kink_h": 12 + 12 * (-demo_b / demo_w)}
    assert abs(demo["kink_h"] - 15) < 1e-9
    # 三条折线加成一个鼓包（示意）：在 6 点、8 点、10 点各拐一次，斜率 +s、−2s、+s
    hb = np.linspace(0, 24, 97)
    s_ = 3.0
    bump_parts = [s_ * np.maximum(0, hb - 6), -2 * s_ * np.maximum(0, hb - 8), s_ * np.maximum(0, hb - 10)]
    bump = sum(bump_parts)
    assert np.allclose(bump[(hb <= 6) | (hb >= 10)], 0) and abs(bump.max() - 2 * s_) < 1e-9 and hb[np.argmax(bump)] == 8, "三条折线 → 8 点一个鼓包"
    demo["bump"] = {"h": hb.round(2).tolist(), "parts": [q.round(3).tolist() for q in bump_parts], "sum": bump.round(3).tolist()}

    # 3) 为什么叠深：每层两个单元 u1 = max(0, 2x)、u2 = max(0, 4x − 2)，输出 u1 − u2 是「帐篷」（在 [0,1] 上对折一次）
    tent = lambda v: np.maximum(0, 2 * v) - np.maximum(0, 4 * v - 2)
    xs = np.linspace(0, 1, 2 ** 12 + 1)
    deep = {}
    f = xs.copy()
    for L in range(1, 6):
        f = tent(f)
        deep[L] = f.copy()
        assert pieces(lambda v, L=L: _compose(tent, v, L), xs) == 2 ** L, L
    # 并排：同样 10 个单元摆成一层，每个单元只在自己的折点 −b/w 处拐一次，所以最多 10 个折点、11 段
    # （随机试很多组：折点落在 [0,1] 里的个数 + 1 从不超过 11；折点挑成均匀分布时正好 11 段）
    rng = np.random.default_rng(7)
    best_wide = 0
    for _ in range(2000):
        w, b = rng.normal(size=10), rng.normal(size=10)
        best_wide = max(best_wide, 1 + int(np.sum((-b / w > 0) & (-b / w < 1))))
    w = np.ones(10); b = -np.arange(1, 11) / 16; v = np.where(np.arange(10) % 2, -2.0, 2.0)
    assert pieces(lambda q: np.maximum(0, np.outer(q, w) + b) @ v, xs) == 11
    assert best_wide <= 11 and pieces(lambda v: _compose(tent, v, 5), xs) == 32

    step_ids = [s for s in SNAPS]
    curves = {str(s): np.round(uy(forward(snaps[s], sx(hh))[2]), 2).tolist() for s in step_ids}
    out = {
        "note": "由 data.py 生成，勿手改",
        "km": KM, "day": round(DAY, 2),
        "rides": [{"h": round(float(a_), 2), "fare": float(b_)} for a_, b_ in zip(h, y)],
        "line": {"b": round(float(k[0]), 3), "k": round(float(k[1]), 4), "loss": round(line_loss, 1)},
        "net": {"units": H_UNITS, "knobs": n_knobs, "loss": round(net_loss, 2), "steps": STEPS, "lr": LR, "momentum": MOM,
                "alive": alive, "kinks": [round(v, 2) for v in kinks],
                "W1": np.round(P[0], 4).tolist(), "b1": np.round(P[1], 4).tolist(), "W2": np.round(P[2], 4).tolist(), "b2": round(float(P[3]), 4)},
        "hh": hh.round(2).tolist(),
        "fit": np.round(uy(p), 2).tolist(),
        "parts": np.round(parts * 10, 2).T.tolist(),          # 12 条折线（元），加上 base 即曲线
        "base": round(float(uy(P[3])), 2),
        "train": {"steps": step_ids, "loss": [round(hist[s], 2) for s in step_ids], "curves": curves,
                  "knobs": [np.round(np.concatenate([np.ravel(q) for q in snaps[s]]), 3).tolist() for s in step_ids]},
        "s1": {"rides": s1_data.RIDES, "base": round(float(s1_data.best_base), 2), "per_km": round(float(s1_data.best_per_km), 3)},
        "kink_pts": [[round(v, 2), round(float(uy(forward(P, sx(np.array([v])))[2][0])), 2)] for v in kinks],
        "demo": demo,
        "deep": {"x": xs[::32].round(4).tolist(), "layers": {str(L): deep[L][::32].round(4).tolist() for L in deep},
                 "pieces": {str(L): 2 ** L for L in deep}, "wide10": 11, "deep10": 32,
                 "wide_curve": np.round(np.maximum(0, np.outer(xs[::32], w) + b) @ v, 4).tolist()},
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"白天五公里 {DAY:.2f} 元；直线 {k.round(3)} 损失 {line_loss:.2f}；网络 {n_knobs} 个旋钮 损失 {net_loss:.3f}（活单元 {alive}）")
    print("训练损失", [round(hist[s], 2) for s in SNAPS], "折点", [round(v, 1) for v in kinks])
    print("叠深：每层段数", [2 ** L for L in deep], "并排 10 个最多", best_wide)


def _compose(f, v, n):
    for _ in range(n):
        v = f(v)
    return v


if __name__ == "__main__":
    main()
