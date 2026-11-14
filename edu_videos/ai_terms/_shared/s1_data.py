"""第 1 季前半共用的示意数据：十二趟打车（距离 km、车费 元）。

真值：起步价 10 元、每公里 2.5 元，加一点随机波动（堵车、绕路）。示意数据，画面标「示意」。
各期 `scenes/data.py` 用 `from s1_data import RIDES` 或读 s1_data.json；本文件不要改（改了五期都要重算）。
"""
import json
from pathlib import Path

import numpy as np

TRUE_BASE, TRUE_PER_KM = 10.0, 2.5
rng = np.random.default_rng(2026_1109)
km = np.array([1.2, 2.0, 2.8, 3.5, 4.1, 5.0, 6.3, 7.0, 8.4, 9.5, 11.0, 12.6])
fare = np.round(TRUE_BASE + TRUE_PER_KM * km + rng.normal(0, 1.6, km.size), 1)
RIDES = [{"km": float(k), "fare": float(f)} for k, f in zip(km, fare)]

# 最小二乘的最佳旋钮（t11 地形图最低点、t04 下山终点都应落在这里）
A = np.c_[np.ones_like(km), km]
best_base, best_per_km = np.linalg.lstsq(A, fare, rcond=None)[0]
best_loss = float(np.mean((A @ [best_base, best_per_km] - fare) ** 2))
assert abs(best_base - TRUE_BASE) < 2.5 and abs(best_per_km - TRUE_PER_KM) < 0.4

if __name__ == "__main__":
    out = {"note": __doc__.strip(), "rides": RIDES, "true": {"base": TRUE_BASE, "per_km": TRUE_PER_KM},
           "best": {"base": round(float(best_base), 3), "per_km": round(float(best_per_km), 3), "mse": round(best_loss, 3)}}
    Path(__file__).with_suffix(".json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["best"]), [r["fare"] for r in RIDES])
