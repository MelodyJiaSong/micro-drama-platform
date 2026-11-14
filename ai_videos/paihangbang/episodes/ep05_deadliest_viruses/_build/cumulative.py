# -*- coding: utf-8 -*-
"""ep05 累计死亡推算（sources.md §2 的口径）：年度锚点之间线性插值，窗口两端按最近锚点持平，逐年相加。
锚点只取同一来源体系（GBD 系列 / WHO 系列）；推算值一律标 est.，屏上取 2 位有效数字。"""
import json

def cum(anchors: dict[int, float], start: int, end: int) -> float:
    ys = sorted(anchors)
    def at(y):
        if y <= ys[0]: return anchors[ys[0]]
        if y >= ys[-1]: return anchors[ys[-1]]
        for a, b in zip(ys, ys[1:]):
            if a <= y <= b:
                return anchors[a] + (anchors[b] - anchors[a]) * (y - a) / (b - a)
    return sum(at(y) for y in range(start, end + 1))

SERIES = {
  # key: (start, end, {year: deaths}, 说明)
  "measles":   (1980, 2024, {1980: 2_600_000, 2000: 780_000, 2019: 207_500, 2022: 136_200, 2023: 107_500, 2024: 95_000}, "WHO/CDC 全球估计"),
  "hbv":       (1990, 2024, {1990: 524_000, 2019: 555_000}, "GBD 2019（1990 值由 2019 值与 +5.9% 反推）"),
  "rotavirus": (1990, 2024, {1990: 659_053, 2019: 235_331, 2021: 170_000}, "GBD 2019 / GBD 2021"),
  "hpv":       (1990, 2024, {1990: 184_527, 2019: 280_479, 2021: 296_667, 2024: 279_583}, "GBD 宫颈癌 + GLOBOCAN 2024"),
  "hcv":       (2013, 2024, {2013: 700_000, 2019: 536_833}, "GBD 2013（Stanaway 2016）/ GBD 2019（Ou 2024）"),
  "norovirus": (1990, 2024, {1990: 242_996, 2019: 135_798}, "GBD 2019"),
  "rsv":       (1990, 2024, {1990: 139_762, 2019: 94_918, 2021: 31_525}, "GBD 2021"),
  "ebv":       (2010, 2024, {2010: 142_979, 2017: 164_000, 2020: 173_300}, "归因癌症死亡：Khan 2014 / Khan 2020 / Wong 2022（区间中点）"),
  "hav":       (1990, 2024, {1990: 107_920, 2019: 39_280, 2023: 35_569}, "GBD 2019 + WHO 2023"),
  "dengue":    (1990, 2024, {1990: 14_315, 2019: 36_055, 2021: 29_075}, "GBD 2021"),
  "yellow_fever": (2013, 2024, {2013: 78_000, 2018: 51_000}, "Garske 2014 / Gaythorpe 2021"),
  "rabies":    (1990, 2024, {1990: 21_806, 2019: 13_743, 2021: 10_084}, "GBD 2019 / GBD 2021"),
  "varicella": (1990, 2024, {1990: 15_633, 2019: 14_553, 2021: 13_931}, "GBD 2019 / GBD 2021"),
  "kshv":      (2020, 2024, {2020: 15_086, 2024: 10_727}, "Kaposi 肉瘤死亡：Fu 2023 / GLOBOCAN 2024"),
  "hev":       (2021, 2024, {2021: 3_450, 2023: 4_431}, "GBD 2021 / WHO 2023"),
}
out = {k: {"start": s, "end": e, "anchors": a, "basis": b, "value": round(cum(a, s, e))} for k, (s, e, a, b) in SERIES.items()}
json.dump(out, open("cumulative.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in sorted(out.items(), key=lambda kv: -kv[1]["value"]):
    print(f"{k:13s} {v['start']}-{v['end']}  {v['value']:>12,}")
