# -*- coding: utf-8 -*-
"""t10 模型与参数的全部实验数据：numpy 算出、断言讲稿里的说法，写成 scenes/data.json 给网页场景用。

    python edu_videos/ai_terms/t10_model_params/scenes/data.py

模型：车费 = 起步价旋钮 + 每公里旋钮 × 公里数（两个旋钮 = 两个参数）。数据：第 1 季共用的十二趟打车（_shared/s1_data.py，示意）。
讲稿说的「起步价拧到十、每公里拧到二，五公里就猜二十」「先随便拧：每趟都猜少了」「起步价往上拧，直线整体抬高，远的还差得多」
「每公里拧过头，远的又猜多了」「拧到约十块二、两块五，直线贴着点走」「八公里猜三十块五」「GPT-3 一千七百五十亿个旋钮，一秒念一个要念五千五百多年」
都由下面的断言守住；数据变了先改讲稿。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_shared"))
from s1_data import RIDES, best_base, best_per_km  # noqa: E402

KM = np.array([r["km"] for r in RIDES])
FARE = np.array([r["fare"] for r in RIDES])
assert KM.size == 12, "讲稿说十二趟"


def predict(base: float, per_km: float, km):
    return base + per_km * np.asarray(km)


def main() -> None:
    # 1) 机器怎么算：起步价 10、每公里 2，跑 5 公里 → 20 元
    demo = {"base": 10, "per_km": 2, "km": 5}
    demo["fare"] = float(predict(demo["base"], demo["per_km"], demo["km"]))
    assert demo["fare"] == 20.0, "讲稿说五公里猜二十块"

    # 2) 拧旋钮的几步（画面上直线跟着动；竖线 = 每趟猜的跟实际差多少）
    best = {"base": round(float(best_base), 1), "per_km": round(float(best_per_km), 2)}
    assert best == {"base": 10.2, "per_km": 2.54}, "讲稿说拧到约十块二、两块五"
    steps = {
        "start": {"base": 0.0, "per_km": 1.0},     # 随便拧
        "up": {"base": 10.0, "per_km": 1.0},       # 起步价往上拧：直线整体抬高
        "steep": {"base": 10.0, "per_km": 3.5},    # 每公里拧过头：远的猜多了
        "best": best,                              # 拧到合适
    }
    gaps = {}
    for k, s in steps.items():
        g = predict(s["base"], s["per_km"], KM) - FARE
        gaps[k] = g.round(2).tolist()
        s["max_gap"] = round(float(np.abs(g).max()), 1)
    g = {k: np.array(v) for k, v in gaps.items()}
    assert (g["start"] < 0).all(), "随便拧：十二趟全都猜少了"
    assert (g["up"] < 0).all() and abs(g["up"][-1]) > 3 * abs(g["up"][0]), "起步价拧上去：近的差得少，远的还差得多"
    assert (g["steep"][-4:] > 0).all() and g["steep"][-1] > 8, "每公里拧过头：远的那几趟都猜多了"
    assert np.abs(g["best"]).max() < 3.5 and np.abs(g["best"]).mean() < 1.2, "拧到合适：竖线都很短"
    for k in ("start", "up", "steep"):
        assert np.abs(g["best"]).mean() < np.abs(g[k]).mean() / 2, f"拧到合适比 {k} 贴得多"

    # 3) 学会以后拿来用：八公里多少钱（用屏幕上的读数算，口播「三十块五左右」）
    ask_km = 8
    ask = round(float(predict(best["base"], best["per_km"], ask_km)), 1)
    assert ask == 30.5, "讲稿说八公里猜三十块五"
    assert ask_km not in KM.tolist(), "八公里这趟不在十二趟记录里（是新问题）"

    # 4) GPT-3：1750 亿参数（Brown et al. 2020）；一秒念一个读数，要念多少年
    gpt3 = 175_000_000_000
    years = gpt3 / (365.25 * 24 * 3600)
    assert 5500 < years < 5600, "讲稿说五千五百多年"
    ratio = gpt3 / 2

    out = {
        "note": "由 data.py 生成，勿手改；打车数据为示意（_shared/s1_data.py）",
        "rides": [{"km": float(k), "fare": float(f)} for k, f in zip(KM, FARE)],
        "demo": demo, "steps": steps, "gaps": gaps, "ask": {"km": ask_km, "fare": ask},
        "knobs": {"base": {"min": 0, "max": 20}, "per_km": {"min": 0, "max": 5}},
        "domain": {"km": [0, 14], "fare": [0, 50]},
        "gpt3": {"params": gpt3, "years": round(years), "ratio": ratio},
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print("best", best, "max_gap", {k: s["max_gap"] for k, s in steps.items()}, "8km", ask, "years", round(years, 1))


if __name__ == "__main__":
    main()
