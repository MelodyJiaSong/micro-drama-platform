# -*- coding: utf-8 -*-
"""t04 梯度下降的全部实验数据：numpy 算出、断言讲稿里的说法，写成 scenes/data.json 给网页场景用。

    python edu_videos/ai_terms/t04_gradient_descent/scenes/data.py

数据：第 1 季共用的十二趟打车（_shared/s1_data.py，示意）。模型：车费 = 起步价 + 每公里 × 距离，两个旋钮。
分数（损失）：均方误差（误差平方再平均），与 t11 损失函数同一种打分、同一张地形图（横轴起步价 0–20，纵轴每公里；本期纵向放宽到 0–5）。
起点：t11 的第一组拧法 A（起步价 5、每公里 2，七十八分）。
梯度下降：每一步算两个旋钮各自的坡度（分数对旋钮的变化率），两个旋钮一起往下坡拧「学习率 × 坡度」那么多。
讲稿里的说法（试拧一下看分数怎么变、走多少步到谷底、学习率太大越跳越高、太小走不动、一小批数据也能走到谷底附近）
都由下面的断言守住；数据变了先改讲稿。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_shared"))
from s1_data import RIDES, best_base, best_per_km, best_loss  # noqa: E402

KM = np.array([r["km"] for r in RIDES])
FARE = np.array([r["fare"] for r in RIDES])
BASE_RANGE, PER_KM_RANGE = (0.0, 20.0), (0.0, 5.0)      # 网格比 t11 宽；画面上 s0/s3/s5 照 t11 只显示 1–4，第 03 章小图显示 0–5（来回跳才看得见）
NX, NY = 161, 161
LEVELS = [2.5, 5, 10, 20, 40, 80, 160, 320]           # 与 t11 同一组等高线
START = np.array([5.0, 2.0])                           # t11 第一组拧法 A
LR_GOOD, LR_SMALL, LR_BIG = 0.005, 0.0005, 0.021
N_STEPS = 1200                                         # 三种学习率都比同样的步数
BATCH = 3                                              # 随机梯度下降：每步随机抽 3 趟
NUDGE = {"base": 0.1, "per_km": 0.1}                   # 「试拧一下」：两个旋钮各拧一毛钱


def loss(p) -> float:
    return float(np.mean((p[0] + p[1] * KM - FARE) ** 2))


def grad(p, idx=None) -> np.ndarray:
    k, f = (KM, FARE) if idx is None else (KM[idx], FARE[idx])
    r = p[0] + p[1] * k - f
    return np.array([2 * r.mean(), 2 * (r * k).mean()])


def descend(lr: float, n: int, start=START, rng=None, stop=1e5):
    """梯度下降 n 步；rng 给了就每步只用随机抽的 BATCH 趟算坡度（随机梯度下降）。分数超过 stop 就停（已经飞出地图）。"""
    p, path, ls = start.astype(float).copy(), [start.astype(float).copy()], [loss(start)]
    for _ in range(n):
        idx = None if rng is None else rng.choice(KM.size, BATCH, replace=False)
        p = p - lr * grad(p, idx)
        path.append(p.copy()); ls.append(loss(p))
        if ls[-1] > stop:
            break
    return np.array(path), np.array(ls)


def main() -> None:
    # 0) 地形图：两个旋钮所有拧法的分数（与 t11 同一张）
    bx, my = np.linspace(*BASE_RANGE, NX), np.linspace(*PER_KM_RANGE, NY)
    B, M = np.meshgrid(bx, my)
    Z = np.mean((B[..., None] + M[..., None] * KM - FARE) ** 2, axis=-1)
    i = np.unravel_index(np.argmin(Z), Z.shape)
    assert abs(B[i] - best_base) < 0.2 and abs(M[i] - best_per_km) < 0.03, "网格最低点就是共用数据的最好拧法"
    assert round(best_base, 1) == 10.2 and round(best_per_km, 2) == 2.54 and round(best_loss, 2) == 1.97, "讲稿：最低点 10.2 / 2.54 / 1.97"
    assert round(loss(START)) == 78, "起点就是 t11 的第一组拧法，七十八分"

    # 1) 试拧一下：每个旋钮单独往两边各拧一点，看分数怎么变（坡度的直观意思）
    l0 = loss(START)
    nudge = {
        "base_up": loss(START + [NUDGE["base"], 0]) - l0, "base_dn": loss(START - [NUDGE["base"], 0]) - l0,
        "km_up": loss(START + [0, NUDGE["per_km"]]) - l0, "km_dn": loss(START - [0, NUDGE["per_km"]]) - l0,
    }
    assert nudge["base_up"] < 0 < nudge["base_dn"], "起步价往高拧，分数降"
    assert nudge["km_up"] < 0 < nudge["km_dn"], "每公里往高拧，分数降"
    assert abs(nudge["km_up"]) > 5 * abs(nudge["base_up"]), "同样拧一毛，每公里那个旋钮让分数降得多得多（坡更陡）"
    g0 = grad(START)
    assert g0[0] < 0 and g0[1] < 0, "坡度说：两个旋钮都往高拧"
    assert abs(g0[1]) > 5 * abs(g0[0]), "每公里旋钮的坡度大得多，所以第一步主要拧它"

    # 2) 合适的学习率：一步步走到谷底
    P, Lg = descend(LR_GOOD, N_STEPS)
    assert len(P) == N_STEPS + 1
    assert np.all(np.diff(Lg) < 0), "合适的学习率：每一步分数都在降"
    step1 = float(np.linalg.norm(P[1] - P[0])); step_late = float(np.linalg.norm(P[-1] - P[-2]))
    assert step1 > 20 * step_late, "坡陡时一步迈得远，快到谷底坡缓了，步子自己变小"
    assert Lg[4] < 10, "头几步就从七十八分掉到十分以下（先下到谷里）"
    k10 = int(np.argmax(Lg < 10)); k2 = int(np.argmax(Lg <= 2.0))
    assert k10 <= 5 and 1000 <= k2 <= 1100, "先几步掉进谷里，再沿着谷底走一千多步才到最低点附近（分数 2.0）"
    assert round(float(Lg[-1]), 1) == 2.0 and abs(P[-1][0] - best_base) < 0.3 and abs(P[-1][1] - best_per_km) < 0.04, \
        "走完：分数 2.0，旋钮约 10 和 2.5，就在最低点旁边"
    assert np.all(np.diff(P[:, 0]) > -1e-9) and P[10, 1] > 3.1 and np.all(np.diff(P[10:, 1]) < 0), \
        "头几步主要把每公里拧到 3 以上（掉进谷里），之后起步价一路往高拧、每公里往回拧（沿着谷底走）"

    # 3) 学习率太小：走同样多步，还在半路
    Ps, Ls = descend(LR_SMALL, N_STEPS)
    assert len(Ps) == N_STEPS + 1 and np.all(np.diff(Ls) < 0)
    assert Ls[-1] > 2.5 * best_loss and Ps[-1][0] < best_base - 3, "太小：走同样多步，分数还高、离最低点还远"

    # 4) 学习率太大：来回跳，越跳越高，几步就飞出地图
    Pb, Lb = descend(LR_BIG, N_STEPS)
    assert Lb[1] > Lb[0] and np.all(np.diff(Lb) > 0), "太大：第一步分数就变高，之后越跳越高"
    side = np.sign(Pb[1:6, 1] - (np.mean(KM * FARE) - Pb[1:6, 0] * KM.mean()) / np.mean(KM ** 2))   # 在谷底的哪一侧
    assert np.all(side[1:] != side[:-1]), "太大：每一步都跳到山谷对面（来回跳）"
    out_k = int(np.argmax(~((Pb[:, 1] >= PER_KM_RANGE[0]) & (Pb[:, 1] <= PER_KM_RANGE[1]))))
    floor = (np.mean(KM * FARE) - Pb[:out_k + 1, 0] * KM.mean()) / np.mean(KM ** 2)   # 同一起步价下，每公里拧到哪分最低（谷底）
    assert 4 <= out_k <= 6 and np.all(np.diff(np.abs(Pb[:out_k + 1, 1] - floor)) > 0), "太大：来回跳、一次比一次离谷底远，几步就跳出了地图"
    assert LR_BIG / LR_GOOD < 5 and LR_GOOD / LR_SMALL == 10

    # 5) 随机梯度下降：每步只随机抽 3 趟算坡度，路歪歪扭扭，也走到谷底附近
    rng = np.random.default_rng(2026_1109)
    Pr, Lr = descend(LR_GOOD, N_STEPS, rng=rng)
    wob = float(np.max(np.linalg.norm(Pr[:200] - P[:200], axis=1)))
    assert wob > 0.15, "示意：小批量的路明显歪扭，不跟全量那条重合"
    assert np.mean(Lr[-100:]) < 1.3 * best_loss + 0.6 and np.linalg.norm(Pr[-1] - [best_base, best_per_km]) < 1.2, \
        "示意：最后也在谷底附近晃"
    assert BATCH / KM.size == 0.25

    # 6) GPT-3（Brown 等 2020，表 2.1）：每一步一批 320 万个词元，总共训练 3000 亿个词元 → 每步约十万分之一
    frac = 3.2e6 / 300e9
    assert 0.9e-5 < frac < 1.2e-5, "讲稿：每一步只看大约十万分之一的训练数据"

    def thin(path, ls, keep):
        """路径点太多：前 keep 步全留，之后每 10 步留一个，末点必留。"""
        ix = sorted(set(list(range(min(keep, len(path)))) + list(range(keep, len(path), 10)) + [len(path) - 1]))
        return {"k": ix, "p": np.round(path[ix], 4).tolist(), "loss": np.round(ls[ix], 3).tolist()}

    out = {
        "note": "由 data.py 生成，勿手改",
        "rides": RIDES,
        "best": {"base": round(float(best_base), 2), "per_km": round(float(best_per_km), 2), "mse": round(float(best_loss), 2)},
        "land": {"base": list(BASE_RANGE), "per_km": list(PER_KM_RANGE), "nx": NX, "ny": NY,
                 "z": Z.round(2).ravel().tolist(), "levels": LEVELS},
        "start": START.tolist(), "start_loss": round(l0, 1),
        "nudge": {k: round(v, 1) for k, v in nudge.items()}, "nudge_size": NUDGE, "g0": np.round(g0, 2).tolist(),
        "lr": {"good": LR_GOOD, "small": LR_SMALL, "big": LR_BIG}, "n_steps": N_STEPS, "k_valley": k10, "k_two": k2,
        "good": thin(P, Lg, 40), "small": thin(Ps, Ls, 40), "big": thin(Pb, Lb, 40), "sgd": thin(Pr, Lr, 40),
        "big_out": out_k, "batch": BATCH, "gpt3_frac": frac,
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print("起点", START.tolist(), round(l0, 2), "试拧", {k: round(v, 2) for k, v in nudge.items()}, "坡度", g0.round(2))
    print("合适", LR_GOOD, "头几步分数", Lg[:6].round(1), "掉进谷", k10, "到 2.0 第", k2, "步；终点", P[-1].round(2), round(Lg[-1], 3))
    print("太小", LR_SMALL, "终点", Ps[-1].round(2), round(Ls[-1], 2), "| 太大", LR_BIG, "分数", Lb[:8].round(0), "出图第", out_k, "步")
    print("小批量 终点", Pr[-1].round(2), "末百步平均分", round(float(np.mean(Lr[-100:])), 2), "最大偏离", round(wob, 2), "| GPT-3 每步", frac)


if __name__ == "__main__":
    main()
