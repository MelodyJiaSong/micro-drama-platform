# -*- coding: utf-8 -*-
"""汴京全城坐标表的读取与拍摄尺度缩放 —— `tools/build_bianjing.py` 与
`tools/shot_plan.py` 共用的唯一出处。

为什么单独成模块：`build_bianjing.py` 顶上就 `import bpy`，只能在 Blender 里跑；
而航线俯视图要在普通 Python 里几秒出图。把 W11 的解析与 `CITY_SCALE` 抄一份到
第二个脚本里，是 CLAUDE.md §General coding rules「一个名字只有一处定义」点名的那种
坑——**尺度漂了不会报错，只会让俯视图上的航线与城市错位，而且看上去很合理**。

本模块不依赖 bpy。
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SK1 = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "2_世界观人设"
W11_LAYOUT = SK1.parent / "0_research" / "parts" / "w11_city_layout.md"

REQUIRED_SECTIONS = ("wall", "gate", "river", "street", "landmark", "place_anchor", "waypoint")

# ── 拍摄用尺度（follow-up 017，2026-09-18 用户定调「城市面积可以缩小，只需要够拍」）──
# W11 的**坐标**统一乘 CITY_SCALE，**尺寸不乘**：街还是 25 m 宽、房还是 11 m 面宽、墙还是 8.7 m 高，
# 变的只是「两处地点之间有多远」。为什么这是对的取舍：
#   · 一镜到底的航线原本 4 km / 60 s ＝ 67 m/s 平均、城内汴河那段要 95 m/s，比真无人机快一倍；
#     压到 0.5 之后全程 33–45 m/s，**速度问题从根上消失，而且不用切镜**（follow-up 010 的一镜到底照旧）。
#   · 全片没有俯视全城的镜头了（follow-up 014 把末段爬升取消），观众无从对照城的总尺寸；
#     能看出比例的只有「街多宽、房多高、门洞多大」——这些保持 1:1。
# 代价（已登记 divergence #28）：几何不再与「外城周长五十里」这类**距离类**史料对得上。
# 几何只服务 previz，不进 prompt；口播里的里程数照旧引 W11，不引 blend。
CITY_SCALE = 0.5
# 压缩后个别 Place 的 1:1 足迹会压到河/街上（足迹不缩、中心距缩）。逐个挪开，只挪不在航线上的：
#   开封府（Place F）——压缩后汴河从它足迹里穿过（实测 k≤0.7 起冲突）。它是地面镜地点、不在一镜到底的
#   航线上，往北挪 70 m 即让出河道；相对州桥的方位不变（仍在州桥西北），地面镜的取景不受影响。
SCALE_NUDGE: dict[str, tuple[float, float]] = {"开封府": (0.0, 70.0)}
_SCALE_XY = {"gate": ("xy",), "landmark": ("xy",), "place_anchor": ("xy",)}
_SCALE_PTS = {"wall": ("points",), "river": ("points",), "street": ("points",)}


class CityLayoutError(RuntimeError):
    """W11 §2.8 读不出来或缺节——照 blender_build.md §7：解析失败直接 raise、不猜。"""


def scale_w11(cfg: dict) -> dict:
    """只缩坐标：xy / points / waypoint 的 pos 与 look_at。宽度、高度、足迹尺寸原样。"""
    k = CITY_SCALE
    if k == 1.0:
        return cfg
    for sec, fields in _SCALE_XY.items():
        for row in cfg.get(sec, []):
            for f in fields:
                row[f] = [float(v) * k for v in row[f]]
    for sec, fields in _SCALE_PTS.items():
        for row in cfg.get(sec, []):
            for f in fields:
                row[f] = [[float(a) * k, float(b) * k] for a, b in row[f]]
    for row in cfg.get("waypoint", []):
        for f in ("pos", "look_at"):
            if f in row:
                v = [float(x) for x in row[f]]
                row[f] = [v[0] * k, v[1] * k] + v[2:]          # z 是高度，不缩
    for row in cfg.get("landmark", []):
        for name, (dx, dy) in SCALE_NUDGE.items():
            if row["name"].startswith(name):
                row["xy"] = [row["xy"][0] + dx, row["xy"][1] + dy]
    return cfg


def read_w11(path: Path | None = None) -> dict:
    """W11 §2.8 的 TOML 块，已乘 CITY_SCALE —— 与 blend 里的世界坐标同一套数。"""
    md = (path or W11_LAYOUT).read_text(encoding="utf-8")
    sec = md.split("### 2.8", 1)
    m = re.search(r"```toml\n(.*?)```", sec[1] if len(sec) == 2 else "", re.S)
    if not m:
        raise CityLayoutError("w11_city_layout.md §2.8 缺 toml 块")
    cfg = scale_w11(tomllib.loads(m.group(1)))
    for key in REQUIRED_SECTIONS:
        if not cfg.get(key):
            raise CityLayoutError(f"W11 TOML 缺 [[{key}]]")
    return cfg
