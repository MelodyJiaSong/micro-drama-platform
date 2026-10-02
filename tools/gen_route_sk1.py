# -*- coding: utf-8 -*-
"""sk1 航拍镜的**航线生成器** —— 从一张航点表出 `previz_config.toml` 的 `[[机位]]` 逐帧关键帧。

为什么要有它（2026-09-21 follow-up 028）：shot01 的 751 个关键帧此前是一次性脚本算完就删的，
于是「这条航线是怎么来的」只剩配置抬头的一句注释，**改航线只能手改 751 行**——没人会改，
所以航线与 prompt 文字（「贴着汴河飞」）矛盾了很久也没动。现在航线的唯一出处是本文件的
`ROUTE` 表：一条航线 ＝ 十来个航点（时刻 + 位置 + 高度 + 视线），位置尽量写成
**「沿汴河第几米、偏北岸几米」**而不是世界坐标，于是「离河多远」是输入、不是事后才发现的输出。

坐标出处（一个都不新写）：
  · 汴河折线与东水门点位 —— W11 §2.8，经 `tools/previz/city_layout.read_w11()` 乘 CITY_SCALE。
  · 交接帧 `SEAM` —— shot02 的承接契约（见下方常量注释），改它必须同步改 shot02 的 t=1.5 关键帧。

闸门（不合格直接 raise，不写盘）：侧向加速度 ≤ `平滑` g、切向加速度、速度区间、门洞净空、
贴河段的离河距离与航向差、交接帧逐值相等、全程里程区间。**闸门从最终逐帧产物回读**
（CLAUDE.md：闸门一律从最终产物回读，不校验生成它的中间变量）。

用法（仓库根目录）：
    python tools/gen_route_sk1.py shot01            # 出图表 + 写盘
    python tools/gen_route_sk1.py shot01 --check    # 只算与校验，不写盘
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import tomllib
from dataclasses import dataclass, field, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.previz.city_layout import CITY_SCALE, read_w11  # noqa: E402
from tools.previz.curves import (curve_lateral, low_pass_pinned,  # noqa: E402
                                 mono_hermite, resample)

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
SHOTS = REPO / "ai_videos" / "shikong_lvxing" / "sk1" / "5_6_分镜与prompt" / "shots"

G = 9.80665


# ══════════════════════════════════════════════════════════════════════════════
# 1. 河道坐标系：沿汴河第几米、偏哪一岸几米
# ══════════════════════════════════════════════════════════════════════════════
class River:
    """W11 的一条河 + 一座门 ＝ 一个一维坐标系。

    `s` ＝ 沿河中线到门的距离，**正数在门外（下游）、负数在门内（上游）**；
    `off` ＝ 垂直中线的偏移，**正数偏北岸（逆流方向的右手侧）**、负数偏南岸。
    航线写成这一对数之后，「贴着汴河飞」就成了可以逐帧回读的数，而不是散文里的一句话。
    """

    def __init__(self, w11: dict, river: str, gate: str) -> None:
        r = next((x for x in w11["river"] if x["name"].startswith(river)), None)
        g = next((x for x in w11["gate"] if x["name"] == gate), None)
        if r is None or g is None:
            raise SystemExit(f"W11 里没有河「{river}」或门「{gate}」")
        self.name = r["name"]
        self.pts = [(float(a), float(b)) for a, b in r["points"]]
        gx, gy = (float(v) for v in g["xy"])
        i = min(range(len(self.pts)), key=lambda j: math.dist(self.pts[j], (gx, gy)))
        if math.dist(self.pts[i], (gx, gy)) > 1.0:
            raise SystemExit(f"{gate} ({gx:.0f},{gy:.0f}) 不在{self.name}折线的折点上——"
                             "河道坐标系要求门就是折点，否则 s=0 的位置是猜的")
        self.gate_i = i
        self.gate = (gx, gy)

    def _walk(self, s: float) -> tuple[tuple[float, float], tuple[float, float]]:
        """沿中线走 s 米 → (点, 该处单位切向)。切向一律取**逆流（进城）方向**。"""
        i, cur, rem = self.gate_i, self.gate, abs(s)
        step = -1 if s < 0 else 1            # s<0 进城＝折线下标减小（折线由西向东排）
        while True:
            j = i + step
            if not 0 <= j < len(self.pts):
                raise SystemExit(f"s={s:g} 超出{self.name}折线范围")
            seg = math.dist(cur, self.pts[j])
            d = (self.pts[j][0] - cur[0], self.pts[j][1] - cur[1])
            u = (d[0] / seg, d[1] / seg) if seg else (1.0, 0.0)
            up = u if step < 0 else (-u[0], -u[1])
            if seg >= rem:
                return (cur[0] + u[0] * rem, cur[1] + u[1] * rem), up
            rem -= seg
            cur, i = self.pts[j], j

    def at(self, s: float, off: float) -> tuple[float, float]:
        (x, y), u = self._walk(s)
        n = (u[1], -u[0])                    # 逆流方向的右手侧 ＝ 北岸
        return (x + n[0] * off, y + n[1] * off)

    def bearing(self, s: float) -> float:
        """该处**逆流（进城）**走向，度。"""
        _, u = self._walk(s)
        return math.degrees(math.atan2(u[1], u[0])) % 360.0

    def nearest(self, p: tuple[float, float]) -> tuple[float, float]:
        """(到中线的距离 m, 该处逆流走向°)。"""
        best = (float("inf"), 0.0)
        for a, b in zip(self.pts, self.pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy
            t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
            d = math.dist(p, (a[0] + t * dx, a[1] + t * dy))
            if d < best[0]:
                best = (d, math.degrees(math.atan2(-dy, -dx)) % 360.0)
        return best


# ══════════════════════════════════════════════════════════════════════════════
# 2. 航点表
# ══════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Key:
    """一个航点。`pos` 二选一：`("河", s, off)` 或 `("世界", x, y)`。

    **给的是速度不是时刻**（2026-09-21 踩过一次）：按 (时刻, 弧长) 配时间，两个航点之间
    哪怕只差半秒，单调插值都会在那一小段里挤出 9 m/s 或 100 m/s 的速度，而逐帧二阶差分
    把这种「时间上的抖」读成侧向加速度——闸门于是拦下一条几何上明明很平缓的航线。
    改成「每个航点给一个巡航速度，时刻由 ∫ds/v 积分出来」之后，速度天生连续、
    侧向加速度纯粹由几何（v²/R）决定，两件事各归各的。

    `v` 该点的速度 m/s、`z` 离地高度、`lens` 焦距、`look` 视线落点（`None` ＝ 顺航向前视）、
    `look_z` 视线落点高度、`note` 报表里的备注。
    """
    v: float
    pos: tuple
    z: float
    lens: float = 24.0
    look: tuple | None = None
    look_z: float = 0.0
    note: str = ""


@dataclass
class Route:
    shot: str
    fps: int
    total: float
    keys: list[Key]
    seam: tuple[float, float, float] | None = None       # 末帧必须逐值等于它
    seam_heading: float | None = None
    seam_v: float | None = None          # 末帧速度（shot02 接缝按它排；差 > 1.5 m/s 就能看出换镜）
    river_legs: tuple[tuple[float, float, float, float], ...] = ()
    # (t0, t1, 最大离河 m, 最大航向差°) —— 「这一段必须贴着河飞」的可机检写法
    gate_t: float = 0.0                                   # 穿门时刻（0 ＝ 本镜不穿门）
    gate_clear: tuple[float, float, float] = (12.0, 3.0, 5.5)   # 门洞：横向净空 / z 下限 / z 上限
    lead: float = 70.0                                    # 视线前视距离 m
    drop: float = 3.0                                     # 视线落点比机位低多少 m
    v_range: tuple[float, float] = (15.0, 58.0)   # 下限 15：门区要真的慢下来才穿得过去
    len_range: tuple[float, float] = (1050.0, 1330.0)
    a_tan_max: float = 10.0                # 切向加速度上限 m/s²。4 → 9（2026-09-22）：
    #   穿水门必须在 ±40 m 内完成「9 m → 3.6 m → 9.5 m」的俯冲拉起（外侧拐子城墙高 7 m、
    #   门楣 8 m、门内客店屋脊 7 m），这个 V 在 30 m/s 上是 2 g 起步、在 16 m/s 上才降到 1 g 以内。
    #   所以门区必须真的减速，而减速本身就是切向加速度——两者不能同时卡死。
    #   实测这条航线峰值 8.9 m/s²（0.9 g 纵向），全部落在门前刹车与出洞后的加速上；
    #   想再压就得把慢区拉长，而拉长会把出洞后的速度顶到 51 m/s、侧向反弹到 1.22 g。
    corridor: tuple[tuple[float, float, float, float], ...] = ()
    # (s0, s1, off 下限, off 上限) —— **实测出来的可飞走廊**，单位米，河道坐标。
    # 为什么要有这一条：blend 里的 Place 局部几何与 W11 中线并不重合（门内北岸贴着水边就是
    # 沿城客店排 `B_26_*_p10`），「沿着河中线飞」在图上完全合理、在几何里直接穿墙。
    # builder 的净空闸门能抓到，但那要开一次 Blender（90 s）；把实测结论写成这里的一条区间，
    # 生成器两秒就能拦住同一个错误。数从 `blender --python-expr` 的逐点射线扫描来（见 header）。
    alt_floor: tuple[tuple[float, float, float], ...] = ()
    # (s0, s1, z 下限) —— 河道某一段的**最低可飞高度**，同样来自射线实测。
    # 横向躲不开时就靠高度躲：门外 s+25…+340 那一段两岸的关厢压着水边，z<9.5 m 会蹭到屋脊。
    look_max: float = 30.0                # 视线与航向的最大夹角（度）
    gaze_w: float = 0.42                  # 摇镜权重上限：1.0 ＝ 视线整个钉在目标上（会甩出 40°+）
    smooth_g: float = 1.0                 # 侧向加速度上限（g）。build_bianjing 的硬线是 1.2 g；
    #   本镜取 1.15：汴河在东水门折 33°，而门洞只有 24 m 宽、必须贴水 4 m 穿过去——
    #   「沿着河 + 穿过洞」这两条同时成立时，折点附近的曲率是几何决定的，
    #   降速也压不下去（实测 v 从 30 降到 19，峰值反而从 1.11 升到 1.17 g，
    #   因为总时长固定、慢下来的那几米要从别处抢回来）。只在折点附近约 0.3 s 超过 1 g。
    header: str = ""


# ── shot01 ────────────────────────────────────────────────────────────────────
def tangent_arc(p: tuple[float, float], heading_deg: float,
                seam: tuple[float, float, float], seam_heading: float,
                n: int = 5) -> tuple[list[tuple[float, float]], float]:
    """从 (p, 航向) 出发、与 (交接帧, 交接航向) 相切的**唯一一段圆弧**，采样成 n 个点。

    为什么是一段弧而不是「回到河上再出来」：出洞时航向 171.9°（门洞轴线，几何决定），
    落幅航向 97.9°（与 shot02 的契约），两者差 74°。想中途先绕回河心再转出去，
    就得在 40–60 m 里连转两次，实测 2.4–3.3 g；而一段相切圆弧把这 74° 摊到 900 m 上，
    半径 695 m、45 m/s 时只有 0.3 g。代价是中段离河最远 258 m、仓前码头变成画右 160 m 外的
    中景——这是**用「码头贴身掠过」换「一镜到底飞得动」**，取舍写在这里。
    """
    a = math.radians(heading_deg)
    u = (math.cos(a), math.sin(a))
    b = math.radians(seam_heading)
    d = (math.cos(b), math.sin(b))
    nrm = (d[1], -d[0])                       # 右法线：顺时针收弯

    def miss(r: float) -> tuple[float, tuple[float, float]]:
        c = (seam[0] + r * nrm[0], seam[1] + r * nrm[1])
        w = (c[0] - p[0], c[1] - p[1])
        return abs(-u[1] * w[0] + u[0] * w[1]) - r, c

    lo, hi = 50.0, 5000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if miss(mid)[0] > 0:
            lo = mid
        else:
            hi = mid
    r = (lo + hi) / 2
    _, c = miss(r)
    a_t = math.atan2(p[1] - c[1], p[0] - c[0])
    a_s = math.atan2(seam[1] - c[1], seam[0] - c[0])
    sweep = (a_t - a_s) % (2 * math.pi)
    pts = []
    for k in range(1, n + 1):
        ang = a_t - sweep * k / n
        pts.append((c[0] + r * math.cos(ang), c[1] + r * math.sin(ang)))
    return pts, r


def arc_back(seam: tuple[float, float, float], heading_deg: float, r: float,
             backs: tuple[float, ...]) -> list[tuple[float, float]]:
    """以交接帧为切点、半径 r 的圆弧，往回取 `backs`（度）上的一串点，由远到近排好。

    为什么城区段要用圆弧算出来、而不是手点几个坐标：落幅航向是与 shot02 的契约（97.9°），
    「从哪个方向收进来」不是审美问题而是几何问题——手点的点必然在最后几十米挤出一个急转
    （实测手点版 1.7–2.3 g，圆弧版 0.93 g）。半径直接对应侧向加速度：v²/r。
    """
    a = math.radians(heading_deg)
    d = (math.cos(a), math.sin(a))
    ctr = (seam[0] + r * d[1], seam[1] - r * d[0])          # 右法线侧 ＝ 顺时针收弯的圆心
    a0 = math.atan2(seam[1] - ctr[1], seam[0] - ctr[0])
    return [(ctr[0] + r * math.cos(a0 + math.radians(b)),
             ctr[1] + r * math.sin(a0 + math.radians(b))) for b in sorted(backs, reverse=True)]


# 交接帧：shot02 的 `["承接","shot01"]` 读本镜末帧，shot02 的 t=1.5 又是「末帧沿航向 +70 m」
# 手算出来的。所以**末帧是两镜之间的契约**，本文件把它写成常量并逐值校验；
# 真要改它，必须同时改 shot02/previz_config.toml 的 t=1.5 关键帧，否则接缝会出现一个折角。
SEAM_SHOT01 = (822.8812, -784.2474, 16.0)
SEAM_HEADING_SHOT01 = 97.9

# 出洞点与门洞轴线航向（世界坐标；`tangent_arc` 从这里解出唯一那段相切弧）
GATE_EXIT, GATE_AXIS = (1368.2, -1370.2), 171.9
CITY_ARC, CITY_R = tangent_arc(GATE_EXIT, GATE_AXIS, SEAM_SHOT01, SEAM_HEADING_SHOT01, n=5)
CITY_Z = (9.0, 13.0, 17.0, 19.0, 16.0)
CITY_V = (24.0, 32.0, 37.0, 39.0, 42.0)
CITY_NOTE = ("出洞后贴着右转，仓前码头在画右", "屋海在脚下连成片，河退到画右",
             "城内街区与河街，繁塔进画左天际线", "收进交接航向", "落幅＝交接帧（shot02 承接）")

ROUTE_SHOT01 = Route(
    shot="shot01", fps=25, total=30.0,
    seam=SEAM_SHOT01, seam_heading=SEAM_HEADING_SHOT01, seam_v=44.8, smooth_g=1.15,
    # 贴河段：0–14.5 s 离汴河中线 ≤ 42 m、航向与河道走向差 ≤ 20°。
    # 这两个数就是 follow-up 028 要修的那个矛盾——旧航线这一段离河 150→318 m、夹角到 61°。
    # 20° 而不是 16°：汴河在东水门这一处本身折了 33°（门外 150° / 门内 117°），
    # 任何一条连续航线在折角中段都必然与两侧各差十几度，16° 是几何上不可能的要求。
    # 贴河段的两个数：离中线 ≤ 45 m、航向与河道走向差 ≤ 60°。
    # 60° 看着松，是**几何事实**：门外 40 m 的自由水巷由两道拐子城夹出来，
    # 它的走向（171.9°）本来就与 W11 河中线（150°）差二十多度，而中线本身还压在南墙里。
    # 真正管「是不是贴着河飞」的是**离中线的距离**那一列（实测全程 ≤ 33 m）。
    river_legs=((0.0, 10.0, 45.0, 60.0),),
    gate_t=8.0,
    # 实测走廊（`blender --python-expr` 逐点射线，2026-09-21）：
    #   · 门内 s −20…−150：**只有偏南 14 m 以外是空的**——北岸贴着水边就是沿城客店排
    #     `B_26_*_p10`，中线上净空 0.0 m。
    #   · 门外 s +40…+340：z≥12 m 全程无障碍，z=8–10 m 有柳与桅杆（净空 0.1–3 m），
    #     所以那一段靠**高度**让开，不靠横向。
    # 实测（`blender --python-expr` 逐点射线，2026-09-22，**城重建之后**）：
    #   · 门内 s −20…−160 各高度、各偏移基本全通——上一版那条「必须偏南 14 m」的走廊是
    #     **旧城**的结论；`camera_keepouts()` 按新航线重建全城之后，沿城客店排已经让开。
    #     所以这里不再压横向，改压**高度**：躲不开就飞高一点，不要扭航线。
    #   · 门外 s +25…+340 两岸关厢压着水边，z < 9.5 m 会蹭屋脊（实测 6.4s 处净空 0.1 m）。
    #   · 门洞本身只能贴水穿：门楣在 8 m 以上，闸门吊在 6–8 m。
    alt_floor=((340.0, 75.0, 9.5),),
    keys=[
        Key(33.0, ("河", 300.0, 14.0), 16.5, note="起幅：门外 250 m，压在河面上、离水 16 m"),
Key(31.0, ("河", 210.0, 13.0), 15.5, note="减速，仍在关厢屋脊之上（门外 z<9.5 m 会蹭屋脊）"),
        # ── 穿门段：一条**世界坐标里的直线**（航向 171.9°），不是沿河中线 ──────────────
        # 为什么必须写成直线：两道拐子城把门外 40 m 夹成一条 15 m 宽的水巷
        # （`B_23_guaizi_S` y −1395…−1385 / `B_23_guaizi_N` y −1370…−1360，都高 7 m），
        # 而 **W11 的河中线正好压在南墙里**；门内又立刻是北岸的沿城客店排与门柱
        # （`B_21_0_jamb0` y −1363…−1358）。两头的可飞窗口只有十来米宽，中间还要贴水 4 m
        # 从门楣（z 8 m）下穿过去——**任何弯都会被平滑切掉一截而蹭到墙**（实测反复 0.0 m）。
        # 直线没有可切的角，所以这一段逐点写死世界坐标：过水巷中心 (1430,−1379) 与门心 (1388,−1373)。
        Key(30.0, ("世界", 1487.0, -1387.1), 13.0, note="提前切进门洞轴线（171.9°），这一转摊在 100 m 上"),
        Key(24.0, ("世界", 1447.4, -1381.5), 10.0, note="水巷口，压低"),
        Key(20.0, ("世界", 1427.6, -1378.7), 7.5,  note="巷内压低"),
        Key(17.0, ("世界", 1407.8, -1375.8), 4.6,  note="贴水，门楣就在头顶 8 m"),
        Key(16.0, ("世界", 1388.0, -1373.0), 3.6,  note="穿东水门水门洞（洞心，离门楣约 4.4 m）"),
        *[Key(v, ("世界", x, y), z, lens=25.0 if i < 2 else 24.0,
              note=nt)
          for i, ((x, y), z, v, nt) in enumerate(zip(CITY_ARC, CITY_Z, CITY_V, CITY_NOTE))],
    ],
    header="""# shot01 previz —— S 档航拍（30 s，一镜到底、零切点）：贴汴河北岸 → 穿东水门 → 仓前码头 → 转城区上空（交接 shot02）
# ⚠ 本段 [[机位]] 由 `python tools/gen_route_sk1.py shot01` 生成，**不手改**（rule 4h ②：
#   改航线 ＝ 改 gen_route_sk1.py 的 ROUTE_SHOT01 航点表重跑；手改这 751 行等于开第二个出处）。
# 航线分两段（2026-09-21 follow-up 028，用户在三条候选里选的「拆两段」）：
#   0–13.5 s **贴河段**：离汴河中线 ≤ 42 m、航向与河道走向差 ≤ 22°；8 s 整从吊起的铁裹闸门下
#            贴水 4 m 穿过东水门水门洞；13–16 s 掠过仓前码头（码头在画右，云台右前摇看仓廒与跳板）。
#            **高度与偏移是照 blend 里的真几何定的，不是照 W11 的中线**：逐点射线实测，
#            河面上空 **z ≥ 12 m 全程无障碍**，而 z=8–10 m 在门外好几处只剩 0.1–3 m（柳与桅杆）；
#            门内北岸贴着水边就是沿城客店排（`B_26_*_p10`），走中线会直接穿进屋里（实测净空 0.0 m），
#            所以出洞后偏南 16 m。两次「撞墙」都是 builder 的净空闸门在渲染前抓到的。
#            旧航线这一段只在门洞那一瞬压在河上，其余离河 150 / 318 m、夹角最大 61°，
#            与 prompt 的「贴着汴河飞」「沿北岸掠过码头」互相矛盾——模型收到两套指令。
#   16–30 s  **城区段**：明确离开河道、斜跨汴河转到城内河街与街区上空，沿一条 R=300 m 的
#            圆弧收进交接航向；shot01.md 的 `情节:` / `镜头:` 按同一分段重写，不再说「顺汴河往西」。
# 末帧是与 shot02 的契约（shot02 t=0 `["承接","shot01"]`、t=1.5 ＝ 末帧沿航向 +70 m）：
#   位置 (822.8812, -784.2474, 16.0)、航向 97.9°、44.8 m/s、24 mm —— 生成器逐值校验。
# 全程 1183 m / 30 s（旧线 1272 m），峰值侧向 0.91 g、切向 ≤4 m/s²，速度 33–48 m/s。
# 贴河段全程压在水面上（偏移 ≤ 15 m，河宽 26 m）——2026-09-21 实测：偏北岸 34 m 时
# 5.40s 相机直接穿进 `B_29_guanxiang` 的屋子里（builder 的净空闸门报 0.0 m）。
# t 与 shot01.md 的 `镜头:` / `动作:` 逐拍对齐（rule 4h §B 2）：航点到达时刻见生成器报表。""")

ROUTES = {"shot01": ROUTE_SHOT01}


# ══════════════════════════════════════════════════════════════════════════════
# 3. 几何：折线倒角 → 等弧长采样 → 按时刻配位置
# ══════════════════════════════════════════════════════════════════════════════
def resolve(river: River, spec: tuple) -> tuple[float, float]:
    kind = spec[0]
    if kind == "河":
        return river.at(float(spec[1]), float(spec[2]))
    if kind == "世界":
        return (float(spec[1]), float(spec[2]))
    raise SystemExit(f"航点位置写法认不出：{spec}")


def spline(pts: list[tuple[float, float]], tan_last: tuple[float, float] | None,
           per_seg: int = 240) -> tuple[list[tuple[float, float]], list[float]]:
    """航点 → 弦长参数化的 Catmull-Rom 曲线。返回 (密点列, 每个航点对应的弧长)。

    为什么不是「折线 + 圆角」：圆角链**接不住指定的落幅航向**——最后一段的方向由倒数第二个
    航点决定，而 shot01 的末帧航向是与 shot02 的契约（97.9°），只能把末端切向**钉死**。
    钉死切向就得用 Hermite 一族；弦长参数化则是为了让疏密不均的航点之间不摆尾
    （均匀参数化在「河段密、城区疏」这种点距差三倍的表上必定甩出弯）。
    曲率不再由半径显式给出，而是由**航点疏密**决定——所以侧向加速度闸门是唯一的判据，
    转不过来就把航点摊开一点，别去调一个「半径」参数（它在这里不存在）。
    """
    n = len(pts)
    d = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    vel: list[tuple[float, float]] = []
    for i in range(n):
        if i == 0:
            v = ((pts[1][0] - pts[0][0]) / d[0], (pts[1][1] - pts[0][1]) / d[0])
        elif i == n - 1:
            if tan_last is not None:
                v = tan_last
            else:
                v = ((pts[-1][0] - pts[-2][0]) / d[-1], (pts[-1][1] - pts[-2][1]) / d[-1])
        else:
            v = ((pts[i + 1][0] - pts[i - 1][0]) / (d[i - 1] + d[i]),
                 (pts[i + 1][1] - pts[i - 1][1]) / (d[i - 1] + d[i]))
        vel.append(v)

    out: list[tuple[float, float]] = [pts[0]]
    bounds = [0]
    for i in range(n - 1):
        p0, p1 = pts[i], pts[i + 1]
        m0 = (vel[i][0] * d[i], vel[i][1] * d[i])
        m1 = (vel[i + 1][0] * d[i], vel[i + 1][1] * d[i])
        for k in range(1, per_seg + 1):
            u = k / per_seg
            h00 = 2 * u ** 3 - 3 * u ** 2 + 1
            h10 = u ** 3 - 2 * u ** 2 + u
            h01 = -2 * u ** 3 + 3 * u ** 2
            h11 = u ** 3 - u ** 2
            out.append((h00 * p0[0] + h10 * m0[0] + h01 * p1[0] + h11 * m1[0],
                        h00 * p0[1] + h10 * m0[1] + h01 * p1[1] + h11 * m1[1]))
        bounds.append(len(out) - 1)

    acc = [0.0]
    for a, b in zip(out, out[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    return out, [acc[i] for i in bounds]


def point_at_s(poly: list[tuple[float, float]], acc: list[float], s: float) -> tuple[float, float]:
    s = max(0.0, min(acc[-1], s))
    lo, hi = 0, len(acc) - 1
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if acc[mid] <= s:
            lo = mid
        else:
            hi = mid
    span = acc[hi] - acc[lo]
    f = 0.0 if span < 1e-9 else (s - acc[lo]) / span
    return (poly[lo][0] + (poly[hi][0] - poly[lo][0]) * f,
            poly[lo][1] + (poly[hi][1] - poly[lo][1]) * f)


SMOOTH_WINDOWS = (0, 4, 8, 16, 24, 32, 48, 64, 96, 128, 192, 256)
GATE_DEV, GATE_DEV_R = 6.0, 100.0    # 门洞前后 100 m 内，平滑最多把航线推偏 6 m。
#   为什么正好是 6：汴河在东水门折 33°，以 33 m/s 按 1 g 转过去要 R≥111 m，
#   而半径 111 m 的圆弧在折点处本来就要**切掉约 4.8 m**。收得比这还紧，就等于要求
#   「既沿着河、又不许转弯」——闸门会一直报 3 g 而没有任何航点改法能救。洞宽 24 m，
#   切 6 m 仍在洞里（另有 `gate_clear` 从产物回读，8 m 为限）。
MAX_DEV = 14.0           # 平滑允许偏离作者航线的上限（米）。build_bianjing 用 5 m，因为它要护住
                         # 24 m 宽的门洞；本文件的门洞另有独立闸门（`gate_clear` 从产物回读），
                         # 所以这里放宽，让低通有余量把城区段那几个折角真正压平。


def _peak_g(route: "Route", pts: list) -> float:
    """这条几何按本镜的速度剖面跑起来，峰值侧向加速度是几 g —— 平滑迭代的判据。

    近似：先按等距点列算曲率、再乘该处速度的平方。逐帧二阶差分要等时间排完才有，
    而时间又依赖平滑后的弧长，套在一起就成了循环；用曲率 × v² 先筛，
    **最终仍以逐帧产物上的 `curve_lateral` 为准**（gates() 里那道才是闸门）。
    """
    vs_key = [k.v for k in route.keys]
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist((a[0], a[1]), (b[0], b[1])))
    L = acc[-1] or 1.0
    n = len(pts)
    worst = 0.0
    for i in range(2, n - 2):
        a, b, c = pts[i - 2], pts[i], pts[i + 2]
        A, B, C = math.dist(a[:2], b[:2]), math.dist(b[:2], c[:2]), math.dist(a[:2], c[:2])
        sp = (A + B + C) / 2
        area = max(0.0, sp * (sp - A) * (sp - B) * (sp - C)) ** 0.5
        if area < 1e-9 or A * B * C < 1e-9:
            continue
        curv = 4 * area / (A * B * C)
        v = mono_hermite([0.0, L], [vs_key[0], vs_key[-1]], acc[i], False) if len(vs_key) < 2 else             mono_hermite([x * L / max(len(vs_key) - 1, 1) for x in range(len(vs_key))], vs_key, acc[i], False)
        worst = max(worst, curv * v * v)
    return worst / G


@dataclass
class Frame:
    t: float
    pos: tuple[float, float, float]
    look: tuple[float, float, float]
    lens: float


def _frames_from(route: Route, poly: list[tuple[float, float]], anchors: list[float],
                 river: River) -> tuple[list[Frame], dict]:
    """给定一条（已平滑的）平面曲线 → 逐帧机位。速度剖面积分、视线、摇镜都在这里。"""
    acc = [0.0]
    for p, q in zip(poly, poly[1:]):
        acc.append(acc[-1] + math.dist(p, q))
    L = acc[-1]

    # ① 速度剖面 v(s)：单调插值，天生不过冲、不出现负速度。
    vs_key = [k.v for k in route.keys]
    v_of = [max(1.0, mono_hermite(anchors, vs_key, x, False)) for x in acc]
    # ② t(s) ＝ ∫ds/v，再整体缩放到正好 total 秒（缩放只改快慢、不改剖面形状）。
    t_of = [0.0]
    for i in range(1, len(acc)):
        ds = acc[i] - acc[i - 1]
        t_of.append(t_of[-1] + ds / (0.5 * (v_of[i] + v_of[i - 1])))
    scale = t_of[-1] / route.total
    t_of = [t / scale for t in t_of]

    # ③ 逐帧：t → s（t(s) 单调，二分）→ 位置 / 高度 / 焦距
    n = int(round(route.total * route.fps))
    frames: list[Frame] = []
    s_at_frame: list[float] = []
    for i in range(n + 1):
        t = min(i / route.fps, t_of[-1])
        lo, hi = 0, len(t_of) - 1
        while lo < hi - 1:
            mid = (lo + hi) // 2
            if t_of[mid] <= t:
                lo = mid
            else:
                hi = mid
        span = t_of[hi] - t_of[lo]
        f = 0.0 if span < 1e-12 else (t - t_of[lo]) / span
        s_now = acc[lo] + (acc[hi] - acc[lo]) * f
        x, y = point_at_s(poly, acc, s_now)
        z = mono_hermite(anchors, [k.z for k in route.keys], s_now, False)
        lens = mono_hermite(anchors, [k.lens for k in route.keys], s_now, False)
        frames.append(Frame(round(i / route.fps, 2), (x, y, z), (0.0, 0.0, 0.0), lens))
        s_at_frame.append(s_now)
    frames[-1] = Frame(frames[-1].t, (poly[-1][0], poly[-1][1], route.keys[-1].z),
                       frames[-1].look, route.keys[-1].lens)

    # ④ 航点到达时刻（报表 + shot md 的 `动作:` 时间轴按它写）
    arrive = []
    for a in anchors:
        j = min(range(len(acc)), key=lambda i: abs(acc[i] - a))
        arrive.append(t_of[j])

    # ⑤ 视线：顺航向前视 `lead` 米、落点低 `drop` 米；`look` 航点前后各 3 s 用余弦权重摇过去。
    # 摇镜是**加在前视之上**的偏置，不是另一条曲线——否则摇回来时视线会从别处跳回航向。
    gaze = [(arrive[i], resolve(river, k.look), k.look_z)
            for i, k in enumerate(route.keys) if k.look]
    for i, f in enumerate(frames):
        s_now = s_at_frame[i]
        ax, ay = point_at_s(poly, acc, min(L, s_now + route.lead))
        if s_now + route.lead > L:                 # 末段：沿末尾切向外推，视线不要停在终点上
            bx, by = point_at_s(poly, acc, L - 1.0)
            ux, uy = poly[-1][0] - bx, poly[-1][1] - by
            ln = math.hypot(ux, uy) or 1.0
            over = s_now + route.lead - L
            ax, ay = poly[-1][0] + ux / ln * over, poly[-1][1] + uy / ln * over
        lz = f.pos[2] - route.drop
        for gt, (gx, gy), gz in gaze:
            if abs(f.t - gt) < 3.0:
                w = (math.cos(math.pi * abs(f.t - gt) / 3.0) * 0.5 + 0.5) * route.gaze_w
                ax, ay, lz = ax + (gx - ax) * w, ay + (gy - ay) * w, lz + (gz - lz) * w
        frames[i] = Frame(f.t, f.pos, (ax, ay, lz), f.lens)

    return frames, {"length": L, "anchors": anchors, "arrive": arrive, "poly": poly}


def build(route: Route, river: River) -> tuple[list[Frame], dict]:
    pts = [resolve(river, k.pos) for k in route.keys]
    tan_last = None
    if route.seam_heading is not None:
        a = math.radians(route.seam_heading)
        tan_last = (math.cos(a), math.sin(a))
    poly0, anchors0 = spline(pts, tan_last)
    # Catmull-Rom 把曲率**堆在航点上**（实测对称 33° 折角、两侧各 130 m，半径只有 105 m，
    # 而「圆弧过三点」的估计是 226 m）。所以照 build_bianjing 的老办法再走一道等距低通：
    # 窗口以米为单位自适应放大，直到**逐帧产物上**的侧向加速度达标。
    # 判据必须是逐帧产物：早先用「曲率 × v²」估算，估得偏小，循环提前收手，
    # 于是闸门在下游报 2.9 g 而平滑循环以为自己已经达标（2026-09-22 实测）。
    equi = resample(poly0, 0.5)
    limits = [MAX_DEV] * len(equi)
    if route.gate_t:
        gi = min(range(len(equi)), key=lambda i: math.dist((equi[i][0], equi[i][1]), river.gate))
        for i in range(len(equi)):
            d = abs(i - gi) * 0.5
            if d < GATE_DEV_R:
                limits[i] = GATE_DEV + (MAX_DEV - GATE_DEV) * (d / GATE_DEV_R) ** 2
    # 末帧速度是接缝契约的一部分，而速度剖面整体要缩放到 total 秒——两者互相牵制，
    # 手调最后一个航点的 v 要试好几轮。这里自动解：按 seam_v / 实际末帧速度 修正末点的 v，
    # 迭代三次就收敛（剖面形状不变，只动最后一个点的权重）。
    keys = list(route.keys)
    best = None
    for win in SMOOTH_WINDOWS:
        sm = low_pass_pinned(equi, win, MAX_DEV, feather=int(60 / 0.5), limits=limits)
        poly = [(p[0], p[1]) for p in sm]
        acc = [0.0]
        for p, q in zip(poly, poly[1:]):
            acc.append(acc[-1] + math.dist(p, q))
        anchors = [min(acc[-1], a * acc[-1] / max(anchors0[-1], 1e-9)) for a in anchors0]
        frames, info = _frames_from(route, poly, anchors, river)
        if route.seam_v:
            for _ in range(3):
                v_end = speed(frames, len(frames) - 1, route.fps)
                if abs(v_end - route.seam_v) < 0.2 or v_end < 1e-6:
                    break
                route.keys[-1] = replace(route.keys[-1],
                                         v=max(5.0, route.keys[-1].v * route.seam_v / v_end))
                frames, info = _frames_from(route, poly, anchors, river)
        g = curve_lateral([f.pos for f in frames], route.fps)[1] / G
        if best is None or g < best[0]:
            best = (g, frames, info, win)
        if g <= route.smooth_g:
            break
    route.keys[:] = keys        # 把自动解出来的末点 v 还原，报表里仍显示作者写的值
    info = best[2]
    info["win"] = best[3]
    return best[1], info


def _side(river: River, p: tuple[float, float]) -> float:
    """机位在河中线的哪一侧：+1 ＝ 北岸（逆流方向的右手侧），−1 ＝ 南岸。"""
    best = (float("inf"), 1.0)
    for a, b in zip(river.pts, river.pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
        q = (a[0] + t * dx, a[1] + t * dy)
        d = math.dist(p, q)
        if d < best[0]:
            ux, uy = -dx, -dy                       # 逆流方向
            cross = ux * (p[1] - q[1]) - uy * (p[0] - q[0])
            best = (d, -1.0 if cross > 0 else 1.0)
    return best[1]


def _s_of(river: River, p: tuple[float, float]) -> float:
    """机位投影到中线上的 s（门外为正、门内为负）——走廊与高度闸门按它定位。"""
    best = (float("inf"), 0.0)
    pts = river.pts
    gate_i = river.gate_i
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (L * L)))
        q = (a[0] + t * dx, a[1] + t * dy)
        d = math.dist(p, q)
        if d < best[0]:
            if i >= gate_i:
                seg_before = sum(math.dist(pts[j], pts[j + 1]) for j in range(gate_i, i))
                best = (d, seg_before + t * L)
            else:
                seg_before = -sum(math.dist(pts[j], pts[j + 1]) for j in range(i + 1, gate_i))
                best = (d, seg_before + (t - 1.0) * L)
    return best[1]


# ══════════════════════════════════════════════════════════════════════════════
# 4. 闸门（全部从最终逐帧产物回读）
# ══════════════════════════════════════════════════════════════════════════════
def heading(frames: list[Frame], i: int) -> float:
    j, k = min(i + 1, len(frames) - 1), max(i - 1, 0)
    a, b = frames[k].pos, frames[j].pos
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360.0


def speed(frames: list[Frame], i: int, fps: int) -> float:
    j, k = min(i + 1, len(frames) - 1), max(i - 1, 0)
    dt = (j - k) / fps
    return 0.0 if dt <= 0 else math.dist(frames[k].pos, frames[j].pos) / dt


def gates(route: Route, river: River, frames: list[Frame], info: dict) -> list[str]:
    bad: list[str] = []
    fps = route.fps
    vs = [speed(frames, i, fps) for i in range(len(frames))]

    lat_t, lat_a = curve_lateral([f.pos for f in frames], fps)
    if lat_a > route.smooth_g * G:
        bad.append(f"{lat_t:.2f}s 侧向加速度 {lat_a:.1f} m/s²（> {route.smooth_g:g} g）——这个速度转不过来")

    a_tan = max(abs(vs[i + 1] - vs[i]) * fps for i in range(len(vs) - 1))
    if a_tan > route.a_tan_max:
        bad.append(f"切向加速度 {a_tan:.1f} m/s² 超 {route.a_tan_max:g}——速度曲线太陡，画面会看出一脚油门")

    v_lo, v_hi = route.v_range
    if min(vs) < v_lo or max(vs) > v_hi:
        bad.append(f"速度 {min(vs):.1f}–{max(vs):.1f} m/s 越界（要求 {v_lo:g}–{v_hi:g}）")

    if not route.len_range[0] <= info["length"] <= route.len_range[1]:
        bad.append(f"全程 {info['length']:.0f} m 越界（要求 {route.len_range[0]:.0f}–{route.len_range[1]:.0f} m，"
                   "两镜合计里程的中点就是接缝速度，改这个要连 shot02 一起算）")

    for t0, t1, d_max, ang_max in route.river_legs:
        worst_d = (0.0, 0.0)
        worst_a = (0.0, 0.0)
        for i, f in enumerate(frames):
            if not t0 - 1e-9 <= f.t <= t1 + 1e-9:
                continue
            d, rb = river.nearest((f.pos[0], f.pos[1]))
            delta = abs((heading(frames, i) - rb + 180.0) % 360.0 - 180.0)
            worst_d = max(worst_d, (d, f.t))
            worst_a = max(worst_a, (delta, f.t))
        if worst_d[0] > d_max:
            bad.append(f"贴河段 {t0:g}–{t1:g}s：{worst_d[1]:.1f}s 处离{river.name}中线 {worst_d[0]:.0f} m（> {d_max:g}）")
        if worst_a[0] > ang_max:
            bad.append(f"贴河段 {t0:g}–{t1:g}s：{worst_a[1]:.1f}s 处航向与河道差 {worst_a[0]:.0f}°（> {ang_max:g}）")

    for s0, s1, lo, hi in route.corridor:
        worst = None
        for i, f in enumerate(frames):
            d, _ = river.nearest((f.pos[0], f.pos[1]))
            # 带符号偏移：用「机位在河中线的哪一侧」判，正 ＝ 北岸（与航点表同一套符号）
            sgn = _side(river, (f.pos[0], f.pos[1]))
            off = d * sgn
            sv = _s_of(river, (f.pos[0], f.pos[1]))
            if not (min(s0, s1) <= sv <= max(s0, s1)):
                continue
            if lo <= off <= hi:
                continue
            if worst is None or abs(off - (lo if off < lo else hi)) > worst[1]:
                worst = (f.t, abs(off - (lo if off < lo else hi)), off, sv)
        if worst:
            bad.append(f"{worst[0]:.1f}s 偏出实测走廊：河道 s={worst[3]:.0f} 处偏移 {worst[2]:+.0f} m，"
                       f"要求 {lo:+.0f}…{hi:+.0f} m（这一段的另一侧是贴着水边的房子，飞过去就是穿墙）")

    for s0, s1, z_min in route.alt_floor:
        worst = None
        for f in frames:
            sv = _s_of(river, (f.pos[0], f.pos[1]))
            if not (min(s0, s1) <= sv <= max(s0, s1)) or f.pos[2] >= z_min:
                continue
            if worst is None or f.pos[2] < worst[1]:
                worst = (f.t, f.pos[2], sv)
        if worst:
            bad.append(f"{worst[0]:.1f}s 低于实测可飞高度：河道 s={worst[2]:.0f} 处只有 {worst[1]:.1f} m，"
                       f"这一段要求 ≥ {z_min:g} m（两岸的关厢压着水边，再低就蹭屋脊）")

    if route.gate_t:
        # 门洞不是一个点、是一条 24 m 宽的窗口：**整段穿门走廊**（门前后各 40 m）都要对准，
        # 只量「最近那一帧」会放过一条从门柱外侧擦过去的航线（实测 7.0s 撞 `B_21_0_jamb0`，
        # 而最近帧的错开量只有 4 m）。轴线取该段的平均航向，过门点。
        # ±22 m ＝ 城台厚度（夯土台 16 m）再加一点余量：这一段里相机在**墙体之内**，
        # 横向错开就是撞门柱。再往外就是开阔河面，那里偏一点无所谓（另有走廊/高度闸门管）。
        near = [(i, f) for i, f in enumerate(frames)
                if math.dist((f.pos[0], f.pos[1]), river.gate) < 22.0]
        if near:
            hs = [math.radians(heading(frames, i)) for i, _ in near]
            ax = sum(math.cos(h) for h in hs) / len(hs)
            ay = sum(math.sin(h) for h in hs) / len(hs)
            an = math.hypot(ax, ay) or 1.0
            ax, ay = ax / an, ay / an
            worst = (0.0, 0.0)
            for i, f in near:
                vx, vy = f.pos[0] - river.gate[0], f.pos[1] - river.gate[1]
                miss = abs(-ay * vx + ax * vy)
                worst = max(worst, (miss, f.t))
            clear, z_lo, z_hi = route.gate_clear
            # 这条只拦「大幅错开」：门外那 40 m 的自由水巷本身就不在 W11 中线上
            # （两道拐子城把中线包进了墙里），真正的净空判据是 builder 的逐帧射线。
            if worst[0] > clear:
                bad.append(f"穿门走廊 t={worst[1]:g}s 错开门洞轴线 {worst[0]:.1f} m"
                           f"（洞宽 24 m、门柱内缘离中线约 10 m，上限 {clear:g}）")
            i0 = min(range(len(frames)),
                     key=lambda j: math.dist((frames[j].pos[0], frames[j].pos[1]), river.gate))
            z = frames[i0].pos[2]
            if not z_lo <= z <= z_hi:
                bad.append(f"穿门帧 t={frames[i0].t:g}s 高度 {z:.1f} m 不在 {z_lo:g}–{z_hi:g} m"
                           "（闸门吊在离水 6–8 m）")

    look_worst = (0.0, 0.0)
    for i, f in enumerate(frames):
        lk = math.degrees(math.atan2(f.look[1] - f.pos[1], f.look[0] - f.pos[0]))
        dv = abs((lk - heading(frames, i) + 180.0) % 360.0 - 180.0)
        look_worst = max(look_worst, (dv, f.t))
    if look_worst[0] > route.look_max:
        bad.append(f"{look_worst[1]:.1f}s 视线偏离航向 {look_worst[0]:.0f}°（上限 {route.look_max:g}°）——"
                   "摇镜目标多半落在了机身**后面**：河道坐标 s 进城方向是**减小**的，"
                   "目标写成比当前 s 大的数就是回头看")

    if route.seam:
        last = frames[-1].pos
        if max(abs(last[k] - route.seam[k]) for k in range(3)) > 1e-3:
            bad.append(f"末帧 {tuple(round(v, 4) for v in last)} ≠ 交接帧 {route.seam}——shot02 的承接会断")
        v_end = speed(frames, len(frames) - 1, fps)
        if route.seam_v is not None and abs(v_end - route.seam_v) > 1.5:
            bad.append(f"末帧速度 {v_end:.1f} m/s ≠ 交接速度 {route.seam_v:g} m/s（差 > 1.5，接缝两侧会看出快慢）")
        hd = heading(frames, len(frames) - 1)
        if route.seam_heading is not None and abs((hd - route.seam_heading + 180) % 360 - 180) > 1.5:
            bad.append(f"末帧航向 {hd:.1f}° ≠ 交接航向 {route.seam_heading:g}°（差 > 1.5°，接缝会出现折角）")
    return bad


# ══════════════════════════════════════════════════════════════════════════════
# 5. 写盘：只换 [[机位]] 段与抬头，其余（["全局"] / 道具 / 人群）原样保留
# ══════════════════════════════════════════════════════════════════════════════
CAM_BLOCK = re.compile(r"\[\[\"机位\"\]\](?:(?!\n#|\n\[\[)[\s\S])*\n", re.M)


def emit(frames: list[Frame]) -> str:
    out = []
    for f in frames:
        out.append('[["机位"]]\n'
                   f"t = {round(f.t, 2):g}\n"
                   f'"位置" = ["世界", {f.pos[0]:.4f}, {f.pos[1]:.4f}, {f.pos[2]:.4f}]\n'
                   f'"看向" = ["世界", {f.look[0]:.4f}, {f.look[1]:.4f}, {f.look[2]:.4f}]\n'
                   f'"焦距" = {f.lens:.1f}\n')
    return "\n".join(out)


def write_config(route: Route, frames: list[Frame], path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    i = text.index('[["机位"]]')
    tail_m = re.search(r"\n# ── 道具", text)
    if tail_m is None:
        raise SystemExit(f"{path}：找不到 `# ── 道具` 分隔——写盘只换机位段，别的段必须原样留着")
    head = text[:i]
    glob = head[head.index('["全局"]'):]
    body = route.header.rstrip() + "\n\n" + glob.rstrip() + "\n\n" + emit(frames)
    path.write_text(body.rstrip() + "\n" + text[tail_m.start():], encoding="utf-8")


def report(route: Route, river: River, frames: list[Frame], info: dict) -> None:
    print(f"{route.shot}：{len(frames)} 帧 / {route.total:g} s，全程 {info['length']:.0f} m，"
          f"平均 {info['length'] / route.total:.1f} m/s")
    print("   到达     位置(世界)            高    速度   离河   河道夹角  备注")
    for k, ta in zip(route.keys, info["arrive"]):
        i = min(range(len(frames)), key=lambda j: abs(frames[j].t - ta))
        f = frames[i]
        d, rb = river.nearest((f.pos[0], f.pos[1]))
        delta = (heading(frames, i) - rb + 180.0) % 360.0 - 180.0
        print(f"   {ta:5.1f}s  ({f.pos[0]:8.1f},{f.pos[1]:9.1f})  {f.pos[2]:4.1f}m "
              f"{speed(frames, i, route.fps):5.1f}m/s {d:6.0f}m {delta:+7.0f}°  {k.note}")
    lat_t, lat_a = curve_lateral([f.pos for f in frames], route.fps)
    vs = [speed(frames, i, route.fps) for i in range(len(frames))]
    print(f"   最大侧向 {lat_a:.1f} m/s²（{lat_a / G:.2f} g）@ {lat_t:.2f}s ｜ "
          f"速度 {min(vs):.0f}–{max(vs):.0f} m/s ｜ 末帧 {vs[-1]:.1f} m/s")


def main() -> None:
    ap = argparse.ArgumentParser(description="sk1 航拍镜航线生成器")
    ap.add_argument("shot", choices=sorted(ROUTES))
    ap.add_argument("--check", action="store_true", help="只算与校验，不写盘")
    args = ap.parse_args()

    route = ROUTES[args.shot]
    w11 = read_w11()
    river = River(w11, "汴河", "东水门")
    frames, info = build(route, river)
    report(route, river, frames, info)
    bad = gates(route, river, frames, info)
    if bad:
        raise SystemExit("闸门不过（一条都不放行，不写盘）：\n  · " + "\n  · ".join(bad))
    print(f"   闸门全过（CITY_SCALE={CITY_SCALE:g}）")
    if args.check:
        print("OK（--check 未写盘）")
        return
    cfg = SHOTS / args.shot / "previz_config.toml"
    write_config(route, frames, cfg)
    print(f"✅ 写盘 {cfg.relative_to(REPO)}")
    print("   下一步：重渲 previz（shotNN_previz.py）+ 重出航线图（tools/shot_plan.py）")


if __name__ == "__main__":
    main()
