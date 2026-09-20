# -*- coding: utf-8 -*-
"""xj1 的相机路径数据：一条连续曲线，按镜切段。

坐标读自 `_series/scenes/余杭客栈/_blender/blender_build.md`。路径是：
李逍遥房（东，x 7.20–10.50 / y 9.00–12.00）→ 房门（y 9.00）→ 二层回廊向西（y 中线 8.25）
→ 楼梯（x 0–1.20，自 y 8.25 下行）→ 大堂（y 1.50–7.50）。

**shot01 没有 previz**：它前 19 秒在梦境乱石坡，那个场景没有几何（rule 4g：环境永不走
image-to-3D，要建须另写 builder）；后半段复用 shot02 的起幅。故本表自 shot02 起。

Run (repo root):
  python tools/gen_previz_xj1.py --check                                  # 不开 Blender，只验曲线
  blender -b --factory-startup --python tools/gen_previz_xj1.py -- --stills
  blender -b --factory-startup --python tools/gen_previz_xj1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from xj_previz_engine import DRAMA, Envelope, Key, ShotPath, run

BLEND = DRAMA / "_series" / "scenes" / "余杭客栈" / "_blender" / "余杭客栈.blend"
ENV = Envelope(x=(-0.30, 10.80), y=(-0.60, 11.90), z=(0.30, 6.20))

PATHS: tuple[ShotPath, ...] = (
    ShotPath(2, 28, (
        Key(0,  (9.90, 10.20, 5.05), (8.90, 11.30, 4.45)),
        Key(14, (9.30,  9.85, 5.20), (8.90, 11.20, 4.55)),
        Key(28, (8.85,  9.55, 5.30), (9.00, 11.10, 4.65)),
    )),
    ShotPath(3, 30, (
        Key(0,  (8.85, 9.55, 5.30), (9.00, 11.10, 4.65)),
        Key(22, (8.85, 9.95, 5.30), (9.05, 11.05, 4.80)),
        Key(30, (8.85, 9.90, 5.30), (9.05, 11.05, 4.80)),
    )),
    ShotPath(4, 30, (
        Key(0,  (8.85, 9.90, 5.30), (9.05, 11.05, 4.80)),
        Key(12, (8.85, 9.70, 5.30), (8.60, 11.00, 4.70)),
        Key(20, (8.85, 9.60, 5.00), (9.60, 11.40, 4.10)),
        Key(30, (8.85, 9.50, 5.35), (8.85, 10.60, 4.90)),
    )),
    ShotPath(5, 28, (
        Key(0,  (8.85, 9.50, 5.35), (8.85, 10.60, 4.90)),
        Key(4,  (8.85, 8.60, 5.35), (8.20,  8.25, 5.00)),
        Key(12, (6.20, 8.30, 5.35), (3.60,  8.25, 5.00)),
        Key(16, (4.60, 8.30, 5.35), (4.20,  6.60, 4.30)),
        Key(20, (2.40, 8.30, 5.35), (0.90,  8.00, 4.90)),
        Key(25, (0.60, 6.10, 3.20), (0.60,  4.20, 1.80)),
        Key(28, (0.70, 3.60, 1.65), (3.40,  3.30, 1.60)),
    )),
    ShotPath(6, 26, (
        Key(0,  (0.70, 3.60, 1.65), (3.40, 3.30, 1.60)),
        Key(26, (1.80, 3.45, 1.62), (4.60, 3.25, 1.45)),
    )),
    ShotPath(7, 30, (
        Key(0,  (1.80, 3.45, 1.62), (4.60, 3.25, 1.45)),
        Key(20, (3.10, 3.35, 1.55), (5.10, 3.20, 1.30), 42.0),
        Key(30, (3.90, 3.30, 1.45), (5.25, 3.15, 1.15), 50.0),
    )),
)


if __name__ == "__main__":
    raise SystemExit(run("xj1", BLEND, PATHS, ENV))
