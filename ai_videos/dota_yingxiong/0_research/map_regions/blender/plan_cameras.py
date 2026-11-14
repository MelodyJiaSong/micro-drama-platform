# -*- coding: utf-8 -*-
"""为每个拍摄区（S1 用手调机位，除外）自动布远景 / 正面 / 侧面三台相机。

目标点取本区主题点（营地刷新点、肉山、神符、商店、中路一塔、遗迹等，见 TARGETS）。
每台相机在 16 个方位里挑：相机落脚格不在树或禁行格里、到目标的视线被树冠/地形挡得最少，
并偏向太阳一侧（傍晚低日从西南偏西来，相机站在西南偏西看过去是顺光）。

    python plan_cameras.py   → region_cameras.json（region_blockout.py 读取并渲染同机位布局图）
"""
from __future__ import annotations

import base64
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MAP = HERE.parent
UPM = json.loads((HERE / "common.json").read_text("utf8"))["units_per_m"]
LEVEL_M = json.loads((HERE / "common.json").read_text("utf8"))["level_height_m"]
TREE_TOP_M = 15.0
SUN_SIDE = math.radians(202.5)  # 相机相对目标的理想方位：西南偏西
SPOT = {"wide": (2200, 55, 24), "front": (640, 4, 24), "side": (640, 6, 28)}
BIG = {"wide": (3200, 80, 24), "front": (1100, 6, 20), "side": (1100, 10, 24)}
OVERVIEW = {"wide": (4500, 150, 24), "front": (2600, 60, 24), "side": (2600, 60, 24)}

grid = json.loads((MAP / "navigation" / "grid.json").read_text("utf8"))
cells = np.frombuffer(base64.b64decode(grid["cells_base64"]), np.uint8).reshape(512, 512)
layers = np.frombuffer(base64.b64decode(grid["height_layers_base64"]), np.uint8).reshape(512, 512)
bit = {k: 1 << i for i, k in enumerate(grid["bits"])}
features = json.loads((MAP / "map_features.json").read_text("utf8"))
regions = json.loads((MAP / "map_regions.json").read_text("utf8"))["regions"]


def cell(x: float, y: float) -> tuple[int, int]:
    return min(511, max(0, int((8192 - y) / 32))), min(511, max(0, int((x + 8192) / 32)))


def ground_m(x: float, y: float) -> float:
    return (int(layers[cell(x, y)]) - 10) * LEVEL_M


def occlusion(cam: tuple[float, float, float], tgt: tuple[float, float, float]) -> float:
    (cx, cy, cz), (tx, ty, tz) = cam, tgt
    steps = max(2, int(math.hypot(tx - cx, ty - cy) / 32))
    hit = 0.0
    for k in range(2, steps - 1):
        t = k / steps
        x, y, z = cx + (tx - cx) * t, cy + (ty - cy) * t, cz + (tz - cz) * t
        g = ground_m(x, y)
        if g > z:
            hit += 3
        elif cells[cell(x, y)] & bit["trees"] and z < g + TREE_TOP_M:
            hit += 1
    return hit


def place(target: tuple[float, float], spec: tuple[float, float, float], avoid: float | None = None, low: bool = True, allowed: list[float] | None = None) -> dict:
    """先在规定距离找空地；找不到就换距离，再不行把相机升到树冠以上（记 raised）。"""
    dist, h, lens = spec
    options = []
    for d, hh, need_free, penalty in ((dist, h, low, 0), (dist * 0.75, h, low, 5), (dist * 1.4, h, low, 5), (dist, 24, False, 15)):
        got = _place(target, (d, hh, lens), avoid, low, need_free, allowed)
        if got:
            got["raised"] = low and not need_free
            options.append((got["occlusion_score"] + penalty, got))
    assert options, target
    return min(options, key=lambda o: o[0])[1]


def _place(target, spec, avoid, low, need_free, allowed=None):
    dist, h, lens = spec
    tx, ty = target
    tz = ground_m(tx, ty) + 2
    best = None
    for k in range(16):
        a = 2 * math.pi * k / 16
        if avoid is not None and not (math.radians(60) <= abs((a - avoid + math.pi) % (2 * math.pi) - math.pi) <= math.radians(130)):
            continue
        if allowed is not None and min(abs((a - math.radians(b) + math.pi) % (2 * math.pi) - math.pi) for b in allowed) > math.radians(25):
            continue
        x, y = tx + dist * math.cos(a), ty + dist * math.sin(a)
        if abs(x) > 7900 or abs(y) > 7900:
            continue
        c = cells[cell(x, y)]
        if need_free and (c & bit["trees"] or c & bit["blocked"]):
            continue
        z = ground_m(x, y) + h
        sun = abs((a - SUN_SIDE + math.pi) % (2 * math.pi) - math.pi)
        score = (occlusion((x, y, z), (tx, ty, tz)) if low else 0) * 10 + math.degrees(sun) / 10
        if best is None or score < best[0]:
            best = (score, a, [round(x), round(y), h])
    if not best:
        return None
    return {"pos": best[2], "look": [round(tx), round(ty), 2 if low else 0], "lens_mm": lens, "azimuth_deg": round(math.degrees(best[1]) % 360, 1),
            "occlusion_score": round(best[0], 1)}


def targets() -> dict[str, tuple[str, tuple[float, float]]]:
    camps = {c["id"]: c for c in features["camps"]}
    shops = {s["id"]: s for s in features["shops"]}
    towers = {t["id"]: t for t in features["towers"]}
    runes = {r["id"]: r for r in features["runes"]}
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    center = lambda ids: (float(np.mean([camps[i]["spawn"][0] for i in ids])), float(np.mean([camps[i]["spawn"][1] for i in ids])))
    out = {cid: ("spot", tuple(c["spawn"])) for cid, c in camps.items()}
    out.update({
        "R4": ("spot", tuple(features["roshan"]["spawn"])), "R1": ("spot", tuple(runes["rune_top"]["spawn"])), "R3": ("spot", tuple(runes["rune_bottom"]["spawn"])),
        "J2": ("spot", tuple(shops["secret_shop_sentinel"]["spawn"])), "K2": ("spot", tuple(shops["secret_shop_scourge"]["spawn"])),
        "T1": ("spot", mid(shops["side_shop_top_u00Z"]["spawn"], shops["side_shop_top_u010"]["spawn"])),
        "B1": ("spot", mid(shops["side_shop_bottom_u00Z"]["spawn"], shops["side_shop_bottom_u010"]["spawn"])),
        "M1": ("spot", tuple(towers["tower_sentinel_mid_t1"]["spawn"])), "M2": ("spot", tuple(towers["tower_scourge_mid_t1"]["spawn"])),
        "R2": ("spot", (-328, -164)), "S2": ("big", (-5632, -6144)), "D2": ("big", (5184, 4864)), "D1": ("big", (6450, 6200)),
        "J1": ("overview", center(["J4", "J5", "J6", "J7", "J8"])), "K1": ("overview", center(["K3", "K4", "K5", "K6", "K7"])),
    })
    return out


def main() -> None:
    plan = {}
    for rid, (kind, target) in targets().items():
        spec = {"spot": SPOT, "big": BIG, "overview": OVERVIEW}[kind]
        wide = place(target, spec["wide"], low=False)
        front = place(target, spec["front"], low=kind != "overview")
        side = place(target, spec["side"], avoid=math.radians(front["azimuth_deg"]), low=kind != "overview")
        plan[rid] = {"kind": kind, "target": [round(target[0]), round(target[1])],
                     "cameras": [{"id": f"{rid}_{v}", "type": "persp", "res": [1600, 900], **c} for v, c in (("wide", wide), ("front", front), ("side", side))]}
    # D1 是 S1 的天灾镜像：手调三机位（前庭看泉水与商店、西南坡道一侧看台地、西南高空看东北）
    plan["D1"]["cameras"] = [
        {"id": "D1_wide", "type": "persp", "res": [1600, 900], "pos": [5300, 5600, 70], "look": [6500, 6150, 0], "lens_mm": 24, "hand": True},
        {"id": "D1_front", "type": "persp", "res": [1600, 900], "pos": [6150, 6230, 5], "look": [6900, 6050, 2], "lens_mm": 20, "hand": True},
        {"id": "D1_side", "type": "persp", "res": [1600, 900], "pos": [5750, 5500, 14], "look": [6550, 6250, 2], "lens_mm": 22, "hand": True}]
    # 边路商店两家沿南北排开：正面从东西方向横看，侧面从斜向看，两家都左右分开而不是前后重叠
    for rid in ("T1", "B1"):
        t = tuple(plan[rid]["target"])
        front = place(t, SPOT["front"], allowed=[0, 180])
        side = place(t, SPOT["side"], allowed=[45, 135, 225, 315], avoid=math.radians(front["azimuth_deg"]))
        plan[rid]["cameras"][1:] = [{"id": f"{rid}_{v}", "type": "persp", "res": [1600, 900], **c} for v, c in (("front", front), ("side", side))]
    assert set(plan) == {r["id"] for r in regions} - {"S1"}, set(plan) ^ ({r["id"] for r in regions} - {"S1"})
    (HERE / "region_cameras.json").write_text(json.dumps({"units_per_m": UPM, "regions": plan}, ensure_ascii=False, indent=1) + "\n", "utf8")
    for rid, p in plan.items():
        print(rid, p["kind"], [(c["id"].split("_")[1], c.get("azimuth_deg", "hand"), c.get("occlusion_score", "-")) for c in p["cameras"]])


main()
