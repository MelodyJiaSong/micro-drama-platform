# -*- coding: utf-8 -*-
"""t01 美国全国停飞：网页场景用的全部数据，写成 scenes/data.json。

    python edu_videos/redian_xiangying/t01_faa_ground_stop/scenes/data.py

画面上的每个数字、日期、引语都从 claims.json 与 research/archive/ 的原文取，并在这里断言：
台账或存档一改、和画面对不上，就在这里报错，先改画面再出片。
示意性的东西（美国轮廓、航路中心的大致位置、设施散点、在空飞机点、绿色「改动」格子、散落的进度表）
用固定随机种子生成，画面上都标「示意」，不代表真实位置或数量比例。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOPIC = HERE.parent
CLAIMS = {c["id"]: c for c in json.loads((TOPIC / "claims.json").read_text(encoding="utf-8"))["claims"]}
ARCHIVE = TOPIC / "research" / "archive"


def claim(cid: str, *needles: str) -> dict:
    """取一条台账，并断言 claim / quote / note / verified 里出现了画面要用的字样。"""
    c = CLAIMS[cid]
    text = " ".join(str(c.get(k) or "") for k in ("claim", "quote", "note", "verified", "via", "source"))
    for n in needles:
        assert n in text, f"{cid} 里找不到画面要用的「{n}」"
    return c


# ---------- 1. 停飞公告原文（ATCSCC Advisory 111，存档）----------
def advisory() -> dict:
    raw = (ARCHIVE / "atcscc_adv111_20261113233522.txt").read_text(encoding="utf-8")
    msg = raw.split("MESSAGE:", 1)[1].split("EFFECTIVE TIME:", 1)[0]
    lines = [re.sub(r"\s+", " ", x).strip() for x in msg.strip().splitlines() if x.strip()]
    assert lines[0] == "EVENT TIME: 13/2053 - 14/0400", lines[0]
    assert lines[1] == "DUE TO EXTRAORDINARY CIRCUMSTANCES AND FOR REASONS OF SAFETY.", lines[1]
    body = " ".join(lines)
    for s in ("ALL AIRPORTS ARE GROUND STOPPED", "UNTIL FURTHER NOTICE", "CASE BY CASE BASIS"):
        assert s in body, s
    assert "26/11/13 20:54" in raw and "NATIONAL GROUND STOP" in raw and "111" in raw
    c1, c2 = claim("C01", "20:54 UTC", "15:54"), claim("C02")
    assert c1["quote"] in body and c2["quote"].replace("  ", " ") in body, "台账引语与存档原文不一致"
    # 与 FAA 美东时间对应：20:54 UTC = 15:54 EST（11 月已是标准时间，UTC−5）
    assert (20 * 60 + 54) - 5 * 60 == 15 * 60 + 54
    return {"head": ["ATCSCC ADVZY 111 DCC 11/13/2026", "NATIONAL GROUND STOP"], "lines": lines,
            "stamp": "ATCSCC Advisory 111 · 2026-11-13 20:54 UTC"}


# ---------- 2. FAA 声明原文（存档）----------
def statement() -> str:
    raw = (ARCHIVE / "faa_statement_20261114024408.txt").read_text(encoding="utf-8")
    q = CLAIMS["C41"]["quote"]
    assert re.sub(r"\s+", " ", q) in re.sub(r"\s+", " ", raw), "C41 引语不在 FAA 声明存档里"
    assert "multiple Air Route Traffic Control Centers" in q and "technicians are investigating" in q
    return q


# ---------- 3. 数字（全部对台账断言）----------
def numbers() -> dict:
    c3 = claim("C03", "8:15", "4 小时 21 分钟", "15:54")
    mins = (20 * 60 + 15) - (15 * 60 + 54)
    assert divmod(mins, 60) == (4, 21), "停飞时长 15:54 → 20:15 = 4 小时 21 分"
    claim("C04", "3,500", "all safely landed")
    claim("C06", "4,467", "10,079", "FlightAware")
    claim("C31", "second since 9/11")
    assert CLAIMS["C31"]["status"] == "有争议"
    claim("C10", "multiple", "all Air Route Traffic Control Centers", "22")
    claim("C25", "4,400", "L3Harris")
    claim("C18", "$50 billion")
    claim("C11", "update", "reboot", "crash")
    assert CLAIMS["C11"]["status"] == "有争议" and CLAIMS["C11"]["via"] == "匿名信源"
    claim("C15", "new equipment and new technology was overwhelming the older system")
    claim("C35", "129", "21", "820", "5 小时", "CC-2010-012", "Harris", "OPIP", "copied")
    claim("C45", "492", "476", "software upgrade", "memory")
    claim("C34", "deleted files")
    claim("C33", "over 30 years old", "GAO-25-108162")
    claim("C22", "138", "51", "54", "GAO-24-107001")
    claim("C28", "50 years", "Bedford")
    claim("C27", "Verizon", "AT&T", "Aug. 11", "2023")
    claim("C26", "150-200 new network paths each month")
    claim("C37", "two cut fiber optic cables", "L3 Harris")
    claim("C38", "backup line had been cut")
    claim("C46", "crashed within a minute", "reboot")
    claim("C23", "11,389", "GAO-26-107992", "lifecycle cost estimate")
    return {
        "stop": {"from": "15:54", "to": "20:15", "h": 4, "m": 21},
        "airborne": 3500, "cancel": 4467, "delay": 10079,
        "artcc": 22, "facilities": 4400, "ask_bn": 50,
        "fti2009": {"should": 21, "hit": 129, "hours": 5, "delayed": 820},
        "eram2015": {"delay": 492, "cancel": 476},
        "notam_years": 30,
        "gao": {"total": 138, "red": 51, "yellow": 54},
        "paths_month": [150, 200],
        "schedules": 11389,
    }


# ---------- 4. 美国示意地图 ----------
# 本土 48 州的粗略轮廓（经纬度，手写约 90 个点；示意，不追求精确）
OUTLINE = [
    (-124.7, 48.4), (-123.0, 49.0), (-110.0, 49.0), (-95.2, 49.0), (-95.2, 49.4), (-94.8, 48.7), (-91.5, 48.1),
    (-89.6, 48.0), (-88.4, 48.3), (-84.8, 46.8), (-84.4, 46.5), (-83.6, 46.1), (-82.4, 45.3), (-82.5, 43.0),
    (-83.1, 42.0), (-81.2, 42.6), (-79.0, 42.9), (-79.2, 43.4), (-76.8, 43.6), (-76.2, 44.2), (-74.8, 45.0),
    (-71.5, 45.0), (-70.6, 45.6), (-70.0, 46.7), (-69.2, 47.45), (-68.2, 47.35), (-67.8, 47.1), (-67.8, 45.7),
    (-67.0, 44.8), (-68.8, 44.3), (-70.2, 43.6), (-70.8, 42.9), (-70.6, 42.6), (-71.0, 42.2), (-70.0, 41.8),
    (-70.6, 41.5), (-71.9, 41.3), (-73.6, 41.0), (-74.0, 40.6), (-74.1, 39.8), (-74.9, 38.9), (-75.1, 38.4),
    (-75.9, 37.6), (-76.0, 37.0), (-75.7, 36.0), (-75.5, 35.3), (-76.5, 34.7), (-77.9, 33.9), (-78.6, 33.8),
    (-79.9, 32.7), (-80.9, 32.0), (-81.4, 30.7), (-81.2, 29.6), (-80.6, 28.4), (-80.1, 26.9), (-80.1, 25.8),
    (-80.4, 25.2), (-81.1, 25.1), (-81.8, 26.1), (-82.6, 27.4), (-82.7, 27.9), (-82.8, 28.9), (-83.6, 29.9),
    (-84.3, 30.0), (-85.4, 29.7), (-86.5, 30.4), (-87.6, 30.3), (-88.4, 30.4), (-89.6, 30.2), (-89.2, 29.2),
    (-90.2, 29.1), (-91.0, 29.3), (-92.3, 29.6), (-93.8, 29.7), (-94.8, 29.3), (-96.0, 28.6), (-97.2, 27.7),
    (-97.4, 26.0), (-99.1, 26.4), (-99.5, 27.5), (-100.3, 28.3), (-101.4, 29.8), (-102.4, 29.8), (-103.1, 29.0),
    (-104.5, 29.6), (-106.5, 31.8), (-108.2, 31.8), (-108.2, 31.3), (-111.1, 31.3), (-114.8, 32.5),
    (-117.1, 32.5), (-117.3, 33.2), (-118.5, 34.0), (-119.6, 34.4), (-120.6, 34.6), (-120.9, 35.4),
    (-121.9, 36.6), (-122.5, 37.8), (-123.0, 38.3), (-123.8, 39.4), (-124.4, 40.4), (-124.2, 42.0),
    (-124.5, 43.0), (-124.0, 46.2), (-124.7, 48.4),
]
# 22 个航路管制中心（ARTCC）：本土 20 个 + 安克雷奇、檀香山；位置取所在城市附近，示意
ARTCC = [
    ("ZSE", -122.2, 47.3), ("ZOA", -122.0, 37.5), ("ZLA", -118.1, 34.6), ("ZLC", -111.9, 40.8), ("ZAB", -106.6, 35.1),
    ("ZDV", -105.1, 40.2), ("ZMP", -93.1, 44.6), ("ZKC", -94.8, 38.9), ("ZFW", -97.3, 32.8), ("ZHU", -95.3, 30.0),
    ("ZME", -89.9, 35.1), ("ZAU", -88.3, 41.8), ("ZID", -86.3, 39.7), ("ZOB", -82.2, 41.3), ("ZTL", -84.3, 33.4),
    ("ZJX", -81.9, 30.7), ("ZMA", -80.3, 25.8), ("ZDC", -77.5, 39.1), ("ZNY", -74.4, 41.1), ("ZBW", -71.5, 42.8),
]
INSETS = [("ZAN", 0.06, 0.80), ("ZHN", 0.17, 0.90)]       # 归一化坐标：放在加州外海的空白处（示意小框）


def inside(px: np.ndarray, py: np.ndarray, poly: np.ndarray) -> np.ndarray:
    """射线法判断点是否在多边形内（向量化）。"""
    res = np.zeros(px.shape, bool)
    x, y = poly[:, 0], poly[:, 1]
    j = len(poly) - 1
    for i in range(len(poly)):
        cond = ((y[i] > py) != (y[j] > py)) & (px < (x[j] - x[i]) * (py - y[i]) / (y[j] - y[i] + 1e-12) + x[i])
        res ^= cond
        j = i
    return res


def usmap() -> dict:
    lat0 = 38.0
    k = np.cos(np.radians(lat0))
    proj = lambda lon, lat: ((lon + 125.0) * k, (49.6 - lat))          # 等距投影，x 按纬度压缩
    pts = np.array([proj(*p) for p in OUTLINE])
    x0, y0 = pts.min(0)
    span = pts.max(0) - pts.min(0)
    s = 1.0 / span[0]
    norm = lambda p: ((p[0] - x0) * s, (p[1] - y0) * s)
    outline = np.array([norm(p) for p in pts])
    aspect = float(span[1] / span[0])
    centers = [{"id": c, "x": round(norm(proj(lon, lat))[0], 4), "y": round(norm(proj(lon, lat))[1], 4)} for c, lon, lat in ARTCC]
    for c in centers:
        assert inside(np.array([c["x"]]), np.array([c["y"]]), outline)[0], f"{c['id']} 落在轮廓外"
    centers += [{"id": c, "x": x, "y": round(y * aspect, 4), "inset": True} for c, x, y in INSETS]
    assert len(centers) == 22, "讲稿说 22 个航路管制中心"
    # 网：每个本土中心连最近的 3 个（去重）；两个外岛中心用虚线连到西海岸
    P = np.array([[c["x"], c["y"]] for c in centers[:20]])
    edges = set()
    for i in range(20):
        d = np.hypot(*(P - P[i]).T)
        for j in np.argsort(d)[1:4]:
            edges.add(tuple(sorted((i, int(j)))))
    edges = sorted(edges)
    ids = [c["id"] for c in centers]
    links = [[ids.index("ZAN"), ids.index("ZSE")], [ids.index("ZHN"), ids.index("ZOA")]]
    # 设施散点（示意 4,400 多个设施，只画 360 个）与在空飞机点（示意，只画 300 个）
    rng = np.random.default_rng(20261113)

    def scatter(n: int) -> list:
        out = []
        while len(out) < n:
            px, py = rng.random(4000), rng.random(4000) * aspect
            ok = inside(px, py, outline)
            out += [[round(float(a), 4), round(float(b), 4)] for a, b in zip(px[ok], py[ok])]
        return out[:n]

    fac, planes = scatter(360), scatter(300)
    order = rng.permutation(len(planes)).tolist()          # 落地的先后（示意）
    return {"aspect": round(aspect, 4), "outline": outline.round(4).tolist(), "centers": centers,
            "edges": [list(e) for e in edges], "links": links, "fac": fac, "planes": planes, "land_order": order}


# ---------- 5. 示意格子 ----------
def gao_grid(n: dict) -> list:
    g = n["gao"]
    cells = ["red"] * g["red"] + ["yellow"] * g["yellow"] + ["grey"] * (g["total"] - g["red"] - g["yellow"])
    assert len(cells) == 138 and cells.count("red") == 51 and cells.count("yellow") == 54
    assert round(51 / 138 * 100) == 37 and round(54 / 138 * 100) == 39, "GAO：37% 与 39%"
    return cells


def changes_grid() -> dict:
    """「每月 150–200 条新线路，绝大多数没出事」：200 个绿格里 4 个红点。示意，不是真实比例。"""
    cols, rows = 25, 8
    rng = np.random.default_rng(7)
    red = sorted(rng.choice(cols * rows, 4, replace=False).tolist())
    return {"cols": cols, "rows": rows, "red": red}


def sheets() -> list:
    """「11,389 份进度表，互不整合」：散落的表格（示意 72 张）。"""
    rng = np.random.default_rng(11389)
    out = []
    for i in range(72):
        out.append({"x": round(float(rng.random()), 3), "y": round(float(rng.random()), 3),
                    "r": round(float(rng.normal(0, 14)), 1), "d": round(float(rng.random()), 3)})
    return out


def main() -> None:
    n = numbers()
    out = {
        "note": "由 data.py 生成，勿手改；数字对 claims.json 与 research/archive 断言过",
        "advisory": advisory(),
        "statement": statement(),
        "bedford": CLAIMS["C28"]["quote"],
        "n": n,
        "map": usmap(),
        "gao": gao_grid(n),
        "changes": changes_grid(),
        "sheets": sheets(),
    }
    (HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    m = out["map"]
    print(f"data.json：公告 {len(out['advisory']['lines'])} 行 · 地图 {len(m['outline'])} 点 / {len(m['centers'])} 中心 / {len(m['edges'])} 条网线"
          f" · GAO 格 {len(out['gao'])} · 停飞 {n['stop']['h']}:{n['stop']['m']:02d}")


if __name__ == "__main__":
    main()
