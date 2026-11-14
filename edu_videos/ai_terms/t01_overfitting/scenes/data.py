# -*- coding: utf-8 -*-
"""t01 过拟合的全部实验数据：numpy 算出、断言讲稿里的说法，写成 scenes/data.json 给网页场景用。

    python edu_videos/ai_terms/t01_overfitting/scenes/data.py
讲稿说「训练误差为零」「二十多倍」「四个数字」「十个数字、十个点」「重复三百次」，都由下面的断言守住；数据变了先改讲稿。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def truth(x):
    return 1.2 * np.sin(1.3 * x) + 0.25 * x


def make_data(seed: int = 99):
    rng = np.random.default_rng(seed)
    xtr = np.linspace(-2.8, 2.8, 10) + rng.uniform(-0.12, 0.12, 10)
    ytr = truth(xtr) + rng.normal(0, 0.35, 10)
    xte = np.linspace(-2.5, 2.5, 6) + rng.uniform(-0.1, 0.1, 6)
    yte = truth(xte) + rng.normal(0, 0.3, 6)
    return xtr, ytr, xte, yte


def error_curves(runs: int = 300):
    rng = np.random.default_rng(0)
    tr, te = np.zeros((runs, 9)), np.zeros((runs, 9))
    for k in range(runs):
        xtr = np.linspace(-2.8, 2.8, 10) + rng.uniform(-0.12, 0.12, 10)
        ytr = truth(xtr) + rng.normal(0, 0.35, 10)
        xte = rng.uniform(-2.8, 2.8, 50)          # 与训练点同一范围（审稿：范围不同会让测试误差在低次时反常偏低）
        yte = truth(xte) + rng.normal(0, 0.35, 50)
        for d in range(1, 10):
            c = np.polyfit(xtr, ytr, d)
            tr[k, d - 1] = np.mean((np.polyval(c, xtr) - ytr) ** 2)
            te[k, d - 1] = np.mean((np.polyval(c, xte) - yte) ** 2)
    return np.median(tr, axis=0), np.median(te, axis=0)


def main() -> None:
    xtr, ytr, xte, yte = make_data()
    xs = np.linspace(-2.95, 2.95, 300)
    fits = {d: np.polyfit(xtr, ytr, d) for d in (1, 3, 9)}
    mse = {d: (float(np.mean((np.polyval(c, xtr) - ytr) ** 2)), float(np.mean((np.polyval(c, xte) - yte) ** 2)))
           for d, c in fits.items()}
    ratio = mse[9][1] / mse[3][1]
    assert mse[9][0] < 1e-6 and 20 <= ratio < 30, "讲稿说「训练误差为零」「二十多倍」"
    assert len(fits[3]) == 4 and len(fits[9]) == len(xtr) == 10, "讲稿说「四个数字」「十个数字、十个点」"
    tr, te = error_curves()
    assert np.all(np.diff(tr) <= 1e-9), "讲稿说训练误差一路往下走"
    best = int(np.argmin(te))
    assert 0 < best < 8 and te[-1] > 2 * te[best], "讲稿说测试误差先降后升"
    rng = np.random.default_rng(3)
    mx = np.sort(rng.uniform(-2.8, 2.8, 40))
    my = truth(mx) + rng.normal(0, 0.35, 40)
    more = np.polyfit(mx, my, 9)
    v = np.vander(xtr / 3, 10, increasing=True)
    w = np.linalg.solve(v.T @ v + 0.01 * np.eye(10), v.T @ ytr)
    ridge = np.vander(xs / 3, 10, increasing=True) @ w
    clip = lambda a: np.clip(a, -3.2, 3.2).round(4).tolist()
    out = {
        "note": "由 data.py 生成，勿手改",
        "xs": xs.round(4).tolist(), "truth": clip(truth(xs)),
        "train": np.c_[xtr, ytr].round(4).tolist(), "test": np.c_[xte, yte].round(4).tolist(),
        "fits": {str(d): clip(np.polyval(c, xs)) for d, c in fits.items()},
        "coef": {str(d): c.round(4).tolist() for d, c in fits.items()},
        "mse": {str(d): [round(a, 4), round(b, 4)] for d, (a, b) in mse.items()},
        "ratio": round(ratio, 2),
        "curves": {"train": tr.round(4).tolist(), "test": te.round(4).tolist(), "runs": 300, "best_degree": best + 1},
        "more": {"points": np.c_[mx, my].round(4).tolist(), "fit": clip(np.polyval(more, xs))},
        "ridge": clip(ridge),
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"data.json：25 倍={ratio:.1f}，最佳次数 {best + 1}，训练误差 {mse[9][0]:.1e}")


if __name__ == "__main__":
    main()
