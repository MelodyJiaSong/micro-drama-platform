# -*- coding: utf-8 -*-
"""t09 拉格朗日乘子的全部实验数据：numpy 算出、断言讲稿里的说法，写成 scenes/data.json 给网页场景用。

    python edu_videos/ai_terms/t09_lagrange/scenes/data.py

实验：一座山 f(p) = 10 − |p − c|²（山顶 c 在 (2.4, 1.8)，离营地中心 3），只许在营地围栏 |p| ≤ 1.5 里找最高点。
拉格朗日的办法：拆掉围栏，改成「离中心每远一步扣 λ 分」，即找 f(p) − λ|p| 的最高点（与 f − λ(|p| − r) 只差常数）。
讲稿说「λ=0 奔山顶、λ 涨到三刚好停在围栏上、价再高就躲进圈里」「自动调价：越界多少涨多少」「围栏放大 0.1，最高点多 0.29，约等于 3×0.1」
「最优点上等高线贴着围栏」「山顶在圈里时 λ 为零」，都由下面的断言守住；数据变了先改讲稿。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C = np.array([2.4, 1.8])          # 山顶
R = 1.5                           # 围栏半径
H = 10.0                          # 山顶高度
GRID = np.linspace(-2.2, 4.3, 1301), np.linspace(-2.0, 3.0, 1001)


def height(x, y):
    return H - ((x - C[0]) ** 2 + (y - C[1]) ** 2)


def best_with_toll(lam: float) -> np.ndarray:
    """数值求 f(p) − λ|p| 在网格上的最高点（不用解析式，眼见为实）。"""
    xx, yy = np.meshgrid(*GRID)
    score = height(xx, yy) - lam * np.hypot(xx, yy)
    i = np.unravel_index(np.argmax(score), score.shape)
    return np.array([xx[i], yy[i]])


def best_in_fence(r: float) -> float:
    """有围栏时的最高点高度（网格上直接找圈内最高）。"""
    xx, yy = np.meshgrid(*GRID)
    inside = np.hypot(xx, yy) <= r
    return float(height(xx, yy)[inside].max())


def main() -> None:
    dist = float(np.hypot(*C))
    assert abs(dist - 3.0) < 1e-9, "讲稿说山顶离营地中心三"
    assert dist > R, "讲稿说山顶在围栏外"

    # 1) 几个价格下，扣分版的最高点落在哪
    probe = {}
    for lam in (0, 1.5, 3, 4):
        p = best_with_toll(lam)
        probe[str(lam)] = {"p": p.round(4).tolist(), "r": round(float(np.hypot(*p)), 3)}
    assert abs(probe["0"]["r"] - 3.0) < 0.01, "λ=0 直奔山顶"
    assert probe["1.5"]["r"] > R + 0.3, "λ=1.5 还在圈外"
    assert abs(probe["3"]["r"] - R) < 0.01, "λ=3 刚好停在围栏上"
    assert probe["4"]["r"] < R - 0.3, "λ=4 躲进圈里，太保守"

    # 2) 自动调价：λ ← λ + (离中心距离 − 半径)，越界多少涨多少，没走到边就降
    lam, steps = 0.0, []
    for _ in range(12):
        p = best_with_toll(lam)
        steps.append({"lam": round(lam, 3), "p": p.round(4).tolist(), "r": round(float(np.hypot(*p)), 3)})
        lam = max(0.0, lam + (float(np.hypot(*p)) - R))
    assert steps[1]["lam"] == 1.5 and steps[1]["r"] > R, "第一次涨到 1.5，还在圈外"
    assert abs(steps[-1]["lam"] - 3.0) < 0.01, "自动调价收在 3"
    lam_star = 3.0

    # 3) 有围栏时的真最高点，和 λ=3 的扣分版是同一个点
    xx, yy = np.meshgrid(*GRID)
    inside = np.hypot(xx, yy) <= R
    hh = np.where(inside, height(xx, yy), -np.inf)
    i = np.unravel_index(np.argmax(hh), hh.shape)
    p_fence = np.array([xx[i], yy[i]])
    assert np.linalg.norm(p_fence - np.array(probe["3"]["p"])) < 0.02, "λ=3 的点就是有围栏时的最高点"
    top = best_in_fence(R)
    assert abs(top - 7.75) < 0.01

    # 4) 相切：最优点上，山坡往上的方向与围栏往外的方向同向，坡度大小正好是 λ
    grad = -2 * (p_fence - C)
    out_dir = p_fence / np.linalg.norm(p_fence)
    cos = float(grad @ out_dir / np.linalg.norm(grad))
    assert cos > 0.9999, "最优点上，往高处的方向正对着围栏外（等高线贴着围栏）"
    assert abs(np.linalg.norm(grad) - lam_star) < 0.02, "坡度大小等于 λ"

    # 5) 影子价格：围栏放大 0.1，最高点多 0.29 ≈ 3 × 0.1
    top2 = best_in_fence(R + 0.1)
    gain = top2 - top
    assert abs(top2 - 8.04) < 0.01 and abs(gain - 0.29) < 0.01, "讲稿说 7.75 → 8.04，多 0.29"
    assert abs(gain - lam_star * 0.1) < 0.02, "≈ λ × 0.1"

    # 6) 山顶本来在圈里：λ 为零（规矩没挡着）
    c_in = np.array([0.6, 0.45])
    lam_in, _ = 0.0, None
    for _ in range(12):
        sc = H - ((xx - c_in[0]) ** 2 + (yy - c_in[1]) ** 2) - lam_in * np.hypot(xx, yy)
        j = np.unravel_index(np.argmax(sc), sc.shape)
        lam_in = max(0.0, lam_in + (float(np.hypot(xx[j], yy[j])) - R))
    assert lam_in == 0.0, "山顶在圈里时 λ 为零"

    # 7) Safe RLHF 画面用的「示意」曲线：玩具模拟，不是论文数据（画面标「示意」）。
    #    模型只有一个旋钮 b（越放得开越有用、也越可能有害）：有用 = b，有害 = b²，底线 0.25。
    #    每步：b 往「有用 − λ×有害」变大的方向走一步；λ ← λ + α(有害 − 底线)，超标涨、守住降（不低于 0）。
    b, lam_t, harm, lams = 0.15, 0.0, [], []
    for _ in range(240):
        b = b + 0.04 * (1 - 2 * lam_t * b)
        lam_t = max(0.0, lam_t + 0.35 * (b * b - 0.25))
        harm.append(b * b); lams.append(lam_t)
    harm, lams = np.array(harm), np.array(lams)
    k_up = int(np.argmax(harm > 0.25))
    assert harm.max() > 0.3 and abs(harm[-1] - 0.25) < 0.01, "示意：先超标、最后贴着底线"
    assert lams[k_up + 5] > lams[k_up] and np.any(np.diff(lams) < 0), "示意：超标时 λ 涨，守住后 λ 降"

    out = {
        "note": "由 data.py 生成，勿手改",
        "toy": {"harm": harm.round(4).tolist(), "lam": lams.round(4).tolist(), "limit": 0.25},
        "peak": C.tolist(), "R": R, "H": H, "lam_star": lam_star,
        "domain": {"x": [-2.2, 4.3], "y": [-2.0, 3.0]},
        "levels": [2, 4, 6, 8],
        "probe": probe, "steps": steps,
        "p_star": p_fence.round(4).tolist(), "top": round(top, 2), "top2": round(top2, 2), "gain": round(gain, 2),
        "peak_in": c_in.tolist(),
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print("data.json：λ 序列", [s["lam"] for s in steps[:7]], "最高点", round(top, 2), "→", round(top2, 2), "多", round(gain, 2))


if __name__ == "__main__":
    main()
