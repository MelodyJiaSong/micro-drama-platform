# -*- coding: utf-8 -*-
"""合并 UN Tourism 数据库（2025-12 批量下载）与三组本国官方调研（research/*.json）→ candidates.json + 打印候选排序。
用法：python -I _build/merge.py"""
import json
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"

DB_NAMES = {  # UN Tourism 名 → 本期屏上英文短名
    "United States of America": "United States", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong", "China, Macao Special Administrative Region": "Macao",
    "Republic of Korea": "South Korea", "Taiwan Province of China": "Taiwan", "Netherlands (Kingdom of the)": "Netherlands",
    "Viet Nam": "Vietnam", "Russian Federation": "Russia", "Iran (Islamic Republic of)": "Iran",
}


def db() -> dict:
    wb = openpyxl.load_workbook(RAW / "UN_Tourism_inbound_arrivals_12_2025.xlsx", read_only=True)
    rows = list(wb["Data"].iter_rows(values_only=True))
    hdr = rows[0]
    out: dict = {}
    for r in rows[1:]:
        r = dict(zip(hdr, r))
        if r["partner_area_label"] != "World" or not str(r["indicator_code"]).endswith(("TOTL_TOUR", "TOTL_VSTR")):
            continue
        name = DB_NAMES.get(r["reporter_area_label"], r["reporter_area_label"])
        kind = "TOUR" if r["indicator_code"].endswith("TOUR") else "VSTR"
        try:
            out.setdefault(name, {})[f"{kind}{r['year']}"] = round(float(r["value"]) / 1000, 4)
        except (TypeError, ValueError):
            pass
    return out


def main() -> None:
    d = db()
    research = {}
    for g in ("europe", "asia", "africa_americas"):
        p = HERE / "research" / f"{g}.json"
        if p.exists():
            for r in json.loads(p.read_text(encoding="utf-8")):
                research[DB_NAMES.get(r["country"], r["country"])] = {**r, "group": g}
    names = set(research) | {k for k, v in d.items() if (v.get("TOUR2024") or 0) >= 3.5}
    cands = []
    for n in sorted(names):
        r, v = research.get(n, {}), d.get(n, {})
        v24 = v.get("TOUR2024") or r.get("v2024")
        cands.append({"name": n, "v2024": v24, "db_tour2024": v.get("TOUR2024"), "res_v2024": r.get("v2024"),
                      "v2023": v.get("TOUR2023") or r.get("v2023"), "db_tour2019": v.get("TOUR2019"), "db_vstr2019": v.get("VSTR2019"),
                      "res_v2019": r.get("v2019"), "res": r})
    cands.sort(key=lambda c: -(c["v2024"] or 0))
    (HERE / "candidates.json").write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    for i, c in enumerate(cands, 1):
        print(f"{i:>3} {c['name']:<22} 2024={c['v2024']!s:<9} db={c['db_tour2024']!s:<9} res={c['res_v2024']!s:<9} "
              f"2023={c['v2023']!s:<9} 2019db={c['db_tour2019']!s:<8} 2019res={c['res_v2019']!s:<8}")


if __name__ == "__main__":
    main()
