# -*- coding: utf-8 -*-
"""t13 反向传播的全部实验数据：numpy 算出、断言讲稿里的说法，写成 scenes/data.json 给网页场景用。

    python edu_videos/ai_terms/t13_backprop/scenes/data.py

实验（两层小网络，七个旋钮）：输入一趟车的距离（第一季共用打车数据里 5 公里、实付 23 元那一趟），
第一层两个小单元 A、B，各带「每公里」「起步」两个旋钮（和 t10 的打车模型同一个样子），过一道「负数归零」；
第二层把 A、B 各乘一个旋钮再加一个起步旋钮，得出猜的车费。
讲稿说「猜二十九，实际二十三，多猜六块」「倒着走一趟，每个旋钮分到自己的数」「挨个试拧要正着算八遍，反向传播正着一遍、倒着一趟，
两边算出来一模一样」「按这七个数拧一小步，猜得更准」「十亿个旋钮：挨个试十亿零一遍，一遍一秒要三十多年；反向传播约三遍的工夫」，
都由下面的断言守住；数据变了先改讲稿。
错误分用 ½ ×（猜的 − 实际）²：½ 只为让「坡度 = 传到这儿的错误 × 放大倍数」不多出一个 2；和平方误差只差常数倍，往哪拧完全一样。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_shared"))
from s1_data import RIDES  # noqa: E402  第一季共用打车数据（示意）

RIDE = next(r for r in RIDES if r["km"] == 5.0)
X, Y = RIDE["km"], RIDE["fare"]
NAMES = ["wA", "bA", "wB", "bB", "vA", "vB", "c"]       # 第一层 A、B 各两个；第二层三个
KNOBS = np.array([1.0, 1.0, 0.4, 2.0, 2.0, 1.0, 13.0])
FORWARD_CALLS = 0


def forward(k: np.ndarray, x: float = X) -> dict:
    """正着算一遍：输入 → 第一层 → 第二层 → 猜的车费。每调用一次记一遍。"""
    global FORWARD_CALLS
    FORWARD_CALLS += 1
    wA, bA, wB, bB, vA, vB, c = k
    zA, zB = wA * x + bA, wB * x + bB
    hA, hB = max(zA, 0.0), max(zB, 0.0)
    pred = vA * hA + vB * hB + c
    return {"zA": zA, "zB": zB, "hA": hA, "hB": hB, "pred": pred}


def loss(k: np.ndarray) -> float:
    return 0.5 * (forward(k)["pred"] - Y) ** 2


def backward(k: np.ndarray, f: dict) -> dict:
    """倒着走一趟：错误从输出往回传，每到一处乘上那里的放大倍数（链式法则），不再正着重算。"""
    wA, bA, wB, bB, vA, vB, c = k
    err = f["pred"] - Y                       # 输出处的错误（多猜了几块）
    g = {"c": err, "vA": err * f["hA"], "vB": err * f["hB"]}   # 第二层：错误 × 送进来的数
    dA = err * vA * (1.0 if f["zA"] > 0 else 0.0)              # 传回单元 A：错误 × 连着它的旋钮
    dB = err * vB * (1.0 if f["zB"] > 0 else 0.0)
    g |= {"wA": dA * X, "bA": dA, "wB": dB * X, "bB": dB}       # 第一层：收到的 × 送进来的数（距离 / 1）
    return {"err": err, "toA": dA, "toB": dB, "grad": np.array([g[n] for n in NAMES])}


def mlp_mults(sizes: list[int]) -> tuple[int, int, int]:
    """全连接网络（每层 n_in×n_out 个旋钮）一次正着、一次倒着的乘法次数；倒着要算两样：
    旋钮的坡度（n_in×n_out 次）和往前一层传的错误（n_in×n_out 次，第一层不用再往输入传）。"""
    pairs = list(zip(sizes[:-1], sizes[1:]))
    n_knobs = sum(a * b + b for a, b in pairs)
    fwd = sum(a * b for a, b in pairs)
    bwd = sum(a * b for a, b in pairs) + sum(a * b for a, b in pairs[1:])
    return n_knobs, fwd, bwd


def main() -> None:
    global FORWARD_CALLS
    assert (X, Y) == (5.0, 23.0), "讲稿说这一趟五公里、实际二十三块"

    # 1) 正着算一遍
    FORWARD_CALLS = 0
    f = forward(KNOBS)
    assert (f["hA"], f["hB"]) == (6.0, 4.0) and f["pred"] == 29.0, "A 出 6、B 出 4，猜二十九"
    assert f["zA"] > 0 and f["zB"] > 0, "两个单元这一趟都在出力（没被归零）"

    # 2) 倒着走一趟
    b = backward(KNOBS, f)
    passes_bp = {"forward": FORWARD_CALLS, "backward": 1}
    assert b["err"] == 6.0, "多猜了六块"
    grad = dict(zip(NAMES, b["grad"].tolist()))
    assert (b["toA"], b["toB"]) == (12.0, 6.0), "传回 A：6×2=12；传回 B：6×1=6"
    assert grad == {"wA": 60.0, "bA": 12.0, "wB": 30.0, "bB": 6.0, "vA": 36.0, "vB": 24.0, "c": 6.0}
    assert passes_bp == {"forward": 1, "backward": 1}, "反向传播：正着一遍、倒着一趟"
    assert all(v > 0 for v in grad.values()), "猜多了：七个旋钮都该往小拧，只是多少不同"

    # 3) 挨个旋钮试拧一下：每个旋钮拧一点点，从头重算一遍，看错误分变了多少
    FORWARD_CALLS = 0
    h = 1e-4
    base = loss(KNOBS)
    fd = []
    for i in range(len(KNOBS)):
        k2 = KNOBS.copy(); k2[i] += h
        fd.append((loss(k2) - base) / h)
    fd = np.array(fd)
    passes_fd = FORWARD_CALLS
    assert passes_fd == len(KNOBS) + 1 == 8, "七个旋钮：正着算八遍"
    assert np.allclose(fd, b["grad"], atol=0.01), "两种办法算出的坡度一模一样（试拧只差一点舍入）"

    # 4) 按这七个数各拧一小步，再猜一遍：更准了
    lr = 0.005
    k_new = KNOBS - lr * b["grad"]
    pred_new = forward(k_new)["pred"]
    assert abs(pred_new - Y) < 1.0 and abs(pred_new - Y) < abs(f["pred"] - Y), "拧一步，猜得更准"

    # 5) 换大一点的网络真跑一遍：挨个试的遍数 = 旋钮数 + 1；反向传播仍是一遍 + 一趟，坡度一致
    rng = np.random.default_rng(13)
    sizes = [1, 32, 32, 1]
    Ws = [rng.normal(0, 1 / np.sqrt(a), (a, b2)) for a, b2 in zip(sizes[:-1], sizes[1:])]
    Bs = [np.zeros(b2) for b2 in sizes[1:]]
    xs = np.array([r["km"] for r in RIDES])[:, None] / 10
    ys = np.array([r["fare"] for r in RIDES])[:, None] / 10
    calls = {"n": 0}

    def net(Ws, Bs):
        calls["n"] += 1
        a, acts = xs, [xs]
        for j, (W, B) in enumerate(zip(Ws, Bs)):
            z = a @ W + B
            a = np.maximum(z, 0) if j < len(Ws) - 1 else z
            acts.append(a)
        return acts

    def L(Ws, Bs):
        return float(0.5 * np.mean((net(Ws, Bs)[-1] - ys) ** 2))

    acts = net(Ws, Bs)
    d = (acts[-1] - ys) / len(xs)
    gW, gB = [None] * len(Ws), [None] * len(Ws)
    for j in reversed(range(len(Ws))):
        gW[j], gB[j] = acts[j].T @ d, d.sum(0)
        if j:
            d = (d @ Ws[j].T) * (acts[j] > 0)
    n_mid = sum(W.size + B.size for W, B in zip(Ws, Bs))
    calls["n"] = 0
    base = L(Ws, Bs)
    fd_mid = []
    for j, W in enumerate(Ws):
        for idx in np.ndindex(W.shape):
            W2 = [w.copy() for w in Ws]; W2[j][idx] += 1e-6
            fd_mid.append((L(W2, Bs) - base) / 1e-6)
    for j, B in enumerate(Bs):
        for idx in np.ndindex(B.shape):
            B2 = [x.copy() for x in Bs]; B2[j][idx] += 1e-6
            fd_mid.append((L(Ws, B2) - base) / 1e-6)
    assert calls["n"] == n_mid + 1, "挨个试：旋钮数 + 1 遍"
    bp_all = np.concatenate([g.ravel() for g in gW] + [g.ravel() for g in gB])
    assert np.allclose(np.array(fd_mid), bp_all, atol=1e-4), "大一点的网络：两种办法坡度一致"
    mid = {"knobs": n_mid, "fd_passes": calls["n"], "bp": "1 + 1"}

    # 6) 倒着那一趟的工夫：数乘法次数，约是正着的两倍 → 反向传播合计约三遍正着的工夫
    n_big, fwd_m, bwd_m = mlp_mults([1024] * 10)
    ratio = (fwd_m + bwd_m) / fwd_m
    assert 2.8 < ratio <= 3.0, "正着一遍 + 倒着一趟 ≈ 三遍正着的工夫"

    # 7) 放大到十亿个旋钮
    N = 10 ** 9
    fd_big = N + 1
    years = fd_big * 1.0 / (365.25 * 24 * 3600)      # 假设正着算一遍要一秒
    assert 31 < years < 32, "一遍一秒，十亿零一遍要三十多年"

    # 8) 齿轮比方：前一个转一格，后一个转两格；再往后转三格 → 一路乘起来六格
    gears = [2, 3]
    assert np.prod(gears) == 6

    out = {
        "note": "由 data.py 生成，勿手改",
        "ride": RIDE, "names": NAMES, "knobs": KNOBS.tolist(),
        "fwd": {k: float(v) for k, v in f.items()},
        "err": b["err"], "toA": b["toA"], "toB": b["toB"], "grad": grad,
        "fd": dict(zip(NAMES, np.round(fd, 3).tolist())), "passes_fd": passes_fd, "passes_bp": passes_bp,
        "lr": lr, "knobs_new": np.round(k_new, 3).tolist(), "pred_new": round(pred_new, 2),
        "mid": mid, "ratio": round(ratio, 2), "big": {"N": N, "fd_passes": fd_big, "years": round(years, 1)},
        "gears": gears,
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("猜", f["pred"], "实际", Y, "错", b["err"], "坡度", grad, "试拧", passes_fd, "遍；拧一步后猜", round(pred_new, 2),
          "；中号网络", mid, "；倍数", round(ratio, 2), "；十亿", round(years, 1), "年")


if __name__ == "__main__":
    main()
