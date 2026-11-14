# -*- coding: utf-8 -*-
"""t11 损失函数的全部实验数据：numpy 算出、断言讲稿里的说法，写成 scenes/data.json 给网页场景用。

    python edu_videos/ai_terms/t11_loss_function/scenes/data.py

数据：第 1 季共用的十二趟打车（edu_videos/ai_terms/_shared/s1_data.py，示意数据，不改它）。
模型：车费 = 起步价 + 每公里 × 距离，两个旋钮。
损失：每趟「猜的 − 实际」= 误差 → 平方 → 十二趟平均（均方误差）。
实验：三组拧法逐个算分；再把两个旋钮的全部拧法算成一张「分数地形图」，最低点 = s1_data 的 best。
讲稿里的数字（六十四、七十八、十三点四、负零点三、二点一九、一点九七、十点二、二点五四）都由下面的断言守住；数据变了先改讲稿。

地形图画法（t04 梯度下降接着用，务必一致）：
    横轴 = 起步价旋钮 BASE_RANGE（元），纵轴 = 每公里旋钮 PER_KM_RANGE（元/公里）；
    颜色 = 分数（均方误差），越高颜色越深（琥珀），等高线取 LEVELS；最低点用绿色标出。
    网格值在 data.json 的 land.z（行 = 每公里，列 = 起步价），d3.contours 直接用。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SHARED = HERE.parents[1] / "_shared"
sys.path.insert(0, str(SHARED))
from s1_data import RIDES, best_base, best_loss, best_per_km  # noqa: E402

KM = np.array([r["km"] for r in RIDES])
FARE = np.array([r["fare"] for r in RIDES])

# 三组拧法（起步价, 每公里）
SETTINGS = {
    "A": (5.0, 2.0),    # 整条线偏低：每趟都猜少了
    "B": (4.0, 3.5),    # 太陡：短途猜少、长途猜多，正负几乎抵消
    "C": (10.0, 2.5),   # 差不多
}
BASE_RANGE = (0.0, 20.0)
PER_KM_RANGE = (1.0, 4.0)
NX, NY = 161, 121
LEVELS = [2.5, 5, 10, 20, 40, 80, 160, 320]


def errors(base: float, per_km: float) -> np.ndarray:
    """每趟的误差：模型猜的 − 实际车费（元）。"""
    return base + per_km * KM - FARE


def score(base: float, per_km: float) -> float:
    """损失：误差平方的平均。"""
    return float(np.mean(errors(base, per_km) ** 2))


def main() -> None:
    assert len(RIDES) == 12, "讲稿说十二趟"

    sets = {}
    for k, (b, m) in SETTINGS.items():
        e = errors(b, m)
        sets[k] = {"base": b, "per_km": m, "err": e.round(2).tolist(), "sq": (e ** 2).round(2).tolist(),
                   "mean_err": round(float(e.mean()), 2), "mse": round(score(b, m), 2)}

    # 第一组：拿 5 公里那趟细算——实际 23 元，模型猜 15 元，差 8 元，平方 64
    i5 = int(np.where(KM == 5.0)[0][0])
    assert FARE[i5] == 23.0 and 5.0 + 2.0 * 5.0 == 15.0, "讲稿：五公里、实际二十三、猜十五"
    assert abs(sets["A"]["err"][i5] + 8.0) < 1e-9 and abs(sets["A"]["sq"][i5] - 64.0) < 1e-9, "差八元，平方六十四"
    assert all(e < 0 for e in sets["A"]["err"]), "第一组每趟都猜少了"
    assert abs(sets["A"]["mse"] - 77.96) < 0.01, "第一组得分约七十八"

    # 第二组：短途猜少、长途猜多；直接平均误差几乎是零（正负抵消），平方后得分 13.4
    eB = np.array(sets["B"]["err"])
    assert eB[0] < -5 and eB[-1] > 5, "短途猜少、长途猜多"
    assert abs(sets["B"]["mean_err"] + 0.33) < 0.005, "直接平均误差 ≈ −0.33，看着像没错"
    assert abs(sets["B"]["mse"] - 13.39) < 0.01, "平方再平均：十三点四"
    # 平方让大错更吃亏：第二组最大的一个误差（8.3 元）在总分里占的份额远大于它在误差里的份额
    share_abs = np.abs(eB).max() / np.abs(eB).sum()
    share_sq = (eB ** 2).max() / (eB ** 2).sum()
    assert share_sq > 1.5 * share_abs, "平方后，差得多的那趟罚得更重"

    # 讲稿「差两块只罚四，差八块就罚六十四」；视角段「宁可每趟都差一点，也不愿意有一趟差很多」：
    # 同样一共差 8 元，四趟各差 2 元 → 罚 4×4 = 16；一趟差 8 元 → 罚 64
    spread, lump = np.array([2.0, 2.0, 2.0, 2.0]), np.array([8.0, 0.0, 0.0, 0.0])
    assert spread.sum() == lump.sum() and (spread ** 2).sum() == 16 and (lump ** 2).sum() == 64

    # 第一章「拧一下，分低了就是拧对了，分高了就拧回来」「一遍遍拧，把分压下去」的演示：起步价固定 10，只拧每公里
    demo_m = [2.0, 2.2, 3.0, 2.2, 2.3, 2.4, 2.5]
    demo = [{"m": m, "mse": round(score(10.0, m), 2)} for m in demo_m]
    assert demo[1]["mse"] < demo[0]["mse"] and demo[2]["mse"] > demo[1]["mse"], "先拧对（分降）、再拧过头（分升）"
    assert all(demo[i + 1]["mse"] < demo[i]["mse"] for i in range(3, 6)), "一遍遍拧，分一路往下"

    # 第三组：二点一九，三组里最低
    assert abs(sets["C"]["mse"] - 2.19) < 0.01
    assert sets["C"]["mse"] < sets["B"]["mse"] < sets["A"]["mse"], "第三组最好、第一组最差"

    # 地形图：两个旋钮的全部拧法
    bx = np.linspace(*BASE_RANGE, NX)
    my = np.linspace(*PER_KM_RANGE, NY)
    BB, MM = np.meshgrid(bx, my)
    Z = np.mean((BB[..., None] + MM[..., None] * KM - FARE) ** 2, axis=-1)
    j = np.unravel_index(np.argmin(Z), Z.shape)
    g_base, g_per = float(BB[j]), float(MM[j])
    # 网格最低点就是最小二乘解（s1_data 的 best）
    assert abs(g_base - best_base) < 0.2 and abs(g_per - best_per_km) < 0.03, "地形图最低点 = s1_data best"
    assert abs(best_base - 10.2) < 0.005 and abs(best_per_km - 2.54) < 0.005 and abs(best_loss - 1.97) < 0.005, "讲稿：十点二、二点五四、一点九七"
    assert best_loss > 1.5, "最低点也不是零：打车费有随机波动，一条直线不可能每趟都猜中"
    assert best_loss < sets["C"]["mse"], "最低点比第三组还低一点"
    for k, (b, m) in SETTINGS.items():
        assert BASE_RANGE[0] <= b <= BASE_RANGE[1] and PER_KM_RANGE[0] <= m <= PER_KM_RANGE[1], f"{k} 在地图范围里"
    assert Z.max() > LEVELS[-1], "最高一圈等高线在图内"

    # 大模型「猜下一个词」的打分（交叉熵，只点名字）：给正确的词 90% 把握 vs 10% 把握，罚分 = −ln(把握)
    ce = {"p_hi": 0.9, "p_lo": 0.1, "pen_hi": round(-np.log(0.9), 2), "pen_lo": round(-np.log(0.1), 2)}
    assert ce["pen_lo"] > 20 * ce["pen_hi"], "把握越小，罚得越多"

    # Llama 2 训练损失「示意」曲线：形状示意（一路往下、越来越缓、到最后还在降），不是论文数据
    t = np.linspace(0, 1, 120)
    curve = 1.75 + 1.6 / (1 + 14 * t) ** 0.55
    assert np.all(np.diff(curve) < 0), "示意：一路往下降"

    out = {
        "note": "由 data.py 生成，勿手改",
        "rides": RIDES, "sets": sets, "i5": i5, "demo": demo,
        "best": {"base": round(float(best_base), 2), "per_km": round(float(best_per_km), 2), "mse": round(float(best_loss), 2)},
        "land": {"base": list(BASE_RANGE), "per_km": list(PER_KM_RANGE), "nx": NX, "ny": NY,
                 "z": Z.round(2).ravel().tolist(), "levels": LEVELS},
        "ce": ce, "curve": curve.round(4).tolist(),
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print("data.json：得分", {k: v["mse"] for k, v in sets.items()}, "第二组平均误差", sets["B"]["mean_err"],
          "最低点", out["best"], "Z 范围", round(float(Z.min()), 2), round(float(Z.max()), 1))


if __name__ == "__main__":
    main()
