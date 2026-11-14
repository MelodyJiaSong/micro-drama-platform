# -*- coding: utf-8 -*-
"""ep16 build：_build/items_def.py（人工核定的条目）→ data.json；保留已有的图片字段（image / image_credit / image_alt …）。

    python _build/build.py          # 写 data.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parent
EP = B.parent
sys.path.insert(0, str(B))
from items_def import EPISODE, ITEMS, INSIGHTS  # noqa: E402
from img_queries import Q  # noqa: E402

KEEP = ("image", "image_credit", "image_alt", "image_alt_credit", "image_risk", "image_note", "image_focus")


def ranks(values: list[float]) -> list[int]:
    """标准竞赛排名（1,1,3）：同容量同名次。"""
    out, prev, r = [], None, 0
    for i, v in enumerate(values, 1):
        if v != prev:
            r, prev = i, v
        out.append(r)
    return out


def main() -> None:
    old = {}
    if (EP / "data.json").exists():
        for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]:
            old[it["slug"]] = it
    items = sorted(ITEMS, key=lambda d: (-d["value"], d["name"]))
    out = []
    for r, d in zip(ranks([d["value"] for d in items]), items):
        it = {"rank": r, "slug": d["slug"], "name": d["name"], "subtitle": d["subtitle"],
              "country_iso2": d["iso2"], "country_name": d["country"], "continent": d["continent"],
              "value": d["value"], "value_display": f"{d['value']:,}", "secondary_display": "seats, est." if d.get("badge") == "ESTIMATE" else "seats"}
        if d.get("badge"):
            it["badge"] = d["badge"]
        it["tags"] = d["tags"]
        it["image"] = f"assets/img/{r:02d}_{d['slug']}.jpg"
        prev = old.get(d["slug"], {})
        for k in KEEP:
            if k in prev:
                it[k] = prev[k]
        if prev.get("image") and Path(prev["image"]).name.split("_", 1)[1] != Path(it["image"]).name.split("_", 1)[1]:
            pass
        if d.get("fop_risk") and "image_risk" not in it:
            it["image_risk"] = d["fop_risk"]
        it["image_hint"] = Q[d["slug"]][0]
        if d.get("image_focus") and "image_focus" not in it:
            it["image_focus"] = d["image_focus"]
        if d.get("thumb"):
            it["thumb"] = True
        it["source"] = d["source"]
        it["cross_check"] = d["cross_check"]
        it["notes"] = d.get("notes", "")
        it["opened"] = d.get("opened")
        it["use"] = d.get("use", "")
        out.append(it)
    data = dict(EPISODE)
    data["items"] = out
    data["insights"] = INSIGHTS
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(out)} items; ranks {out[0]['rank']}..{out[-1]['rank']}; last value {out[-1]['value']:,}")


if __name__ == "__main__":
    main()
