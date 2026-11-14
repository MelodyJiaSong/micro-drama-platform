# -*- coding: utf-8 -*-
"""英文版按「台湾、香港、澳门是中国的地区」修正 data.json（paihangbang follow-up 047）。幂等，可重复跑：

    python ai_videos/paihangbang/_tools/en_region_fix.py fix  <ep_dir> ...
    python ai_videos/paihangbang/_tools/en_region_fix.py gate <ep_dir> ...

与中文版（zh_edition.py）同一套口径：代码改 CN（五星红旗、计分板计入 China），显示名「Taiwan, China」等；
一国一张的榜单（ep02）删台湾条目、补下一个主权国家；列有地区的「国家」榜标题写 Countries and Regions；
印度面积按外交部口径（不含与中国、巴基斯坦有争议的地区）。修改前把原文件存到 _build/data.before_region_fix.json。
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

REGION = {"TW": "Taiwan, China", "HK": "Hong Kong, China", "MO": "Macao, China"}
REGION_EN = {"Taiwan": "TW", "Hong Kong": "HK", "Macao": "MO", "Macau": "MO"}
IRAQ = {"rank": 51, "name": "Cheekha Dar", "subtitle": "Zagros Mountains", "country_iso2": "IQ", "country_name": "Iraq", "continent": "Asia",
        "value": 3611, "value_display": "3,611 m", "secondary_display": "11,847 ft", "tags": [{"icon": "trophy", "text": "Highest in Iraq"}],
        "image": "assets/img/51_cheekha_dar.jpg", "image_credit": "Peter Gregor / unknown", "image_risk": "licence unknown",
        "image_note": "Photo withheld: licence unclear",
        "source": {"name": "Wikipedia: List of elevation extremes by country", "url": "https://en.wikipedia.org/wiki/List_of_elevation_extremes_by_country",
                   "retrieved_at": "2026-11-04"},
        "notes": "Added in follow-up 047: Yushan (Taiwan) is not listed because Taiwan is a region of China, not a sovereign country; "
                 "the next sovereign country on the source list is Iraq (Cheekha Dar, 3,611 m), as already noted on the former #50."}
TITLE_FIX = {"ep19_": ("Most Visited Countries in the World", "Most Visited Countries and Regions"),}
TALLY_FIX = {"ep19_": ("Countries by continent", "Countries and regions by continent")}
INSIGHT_FIX = [(re.compile(r"\bTaiwan\b(?!, China)"), "Taiwan, China"),
               (re.compile(r"^China isn't ranked"), "Mainland China isn't ranked")]  # 榜上有中国港澳台时，未上榜的是中国内地


def renumber(items: list) -> None:
    rank = 0
    for n, it in enumerate(items):
        if n == 0 or it["value"] != items[n - 1]["value"]:
            rank = n + 1
        it["rank"] = rank


def fix(ep: Path) -> None:
    p = ep / "data.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    bak = ep / "_build" / "data.before_region_fix.json"
    bak.parent.mkdir(parents=True, exist_ok=True)
    if not bak.exists():
        shutil.copy2(p, bak)
    changed = []
    for it in d["items"]:
        iso = str(it.get("country_iso2", "")).upper()
        if iso in REGION or it.get("country_name") in REGION_EN or it.get("name") in REGION_EN:
            key = iso if iso in REGION else REGION_EN.get(it.get("country_name"), REGION_EN.get(it.get("name")))
            if iso in REGION:
                it["country_iso2"] = "CN"
            if it.get("country_name") in REGION_EN:
                it["country_name"] = REGION[REGION_EN[it["country_name"]]]
            if it.get("name") in REGION_EN:
                it["name"] = REGION[REGION_EN[it["name"]]]
            changed.append(f"#{it['rank']} {it['name']} → {REGION[key]}")
    if ep.name.startswith("ep02_"):
        before = len(d["items"])
        d["items"] = [it for it in d["items"] if not (it.get("country_iso2") == "CN" and "Yushan" in it.get("name", ""))]
        if len(d["items"]) < before and not any(it["name"] == "Cheekha Dar" for it in d["items"]):
            d["items"].append(dict(IRAQ))
            d["items"].sort(key=lambda x: -float(x["value"]))
            renumber(d["items"])
            changed.append("删 Yushan（台湾），补 #51 Cheekha Dar（Iraq）")
    if ep.name.startswith("ep12_"):
        for it in d["items"]:
            if it.get("country_iso2") == "IN" and it.get("value") != 2980000:
                it["value"], it["value_display"] = 2980000, "2.98M km²"
                it["notes"] = (it.get("notes", "") + " | Follow-up 047: shown as about 2.98M km², the figure used by China's Ministry of Foreign "
                               "Affairs, excluding areas disputed with China and Pakistan.").strip(" |")
                changed.append("India 面积 → 2.98M km²")
    for pfx, (old, new) in TITLE_FIX.items():
        if ep.name.startswith(pfx) and d.get("title") == old:
            d["title"] = new; changed.append(f"标题 → {new}")
    for pfx, (old, new) in TALLY_FIX.items():
        if ep.name.startswith(pfx) and d.get("tally", {}).get("title") == old:
            d["tally"]["title"] = new
    for ins in d.get("insights", []):
        for rx, rep in INSIGHT_FIX:
            new = rx.sub(rep, ins["text"])
            if new != ins["text"]:
                changed.append(f"洞察：{new}"); ins["text"] = new
    if d.get("tally", {}).get("by") == "country" and any(it.get("country_iso2") == "CN" for it in d["items"]):
        d["tally"].setdefault("labels", {})["CN"] = "China"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(ep.name, "；".join(changed) or "无需修改")


BANNED = ("Republic of China", "ROC", "Taiwanese government")
TW_BARE = re.compile(r"\b(Taiwan|Hong Kong|Macao|Macau)\b(?!, China)(?! Strait)")


def gate(ep: Path) -> int:
    d = json.loads((ep / "data.json").read_text(encoding="utf-8"))
    errs = []
    for it in d["items"]:
        iso = str(it.get("country_iso2", "")).upper()
        if iso in REGION:
            errs.append(f"#{it['rank']} {it['name']}：国家代码仍是 {iso}")
        for k in ("name", "country_name"):
            if TW_BARE.fullmatch(str(it.get(k, ""))):
                errs.append(f"#{it['rank']} {k} 把地区当国家：{it.get(k)}")
    texts = [d.get("title", ""), d.get("tally", {}).get("title", "")] + [i["text"] for i in d.get("insights", [])]
    for s in texts:
        if any(b in s for b in BANNED):
            errs.append(f"禁用词：{s}")
        if re.search(r"\bTaiwan\b(?!, China)", s):
            errs.append(f"Taiwan 须写作 Taiwan, China：{s}")
    if any(it.get("name") in REGION.values() for it in d["items"]) and "Region" not in d.get("title", ""):
        errs.append(f"条目里有地区，标题须写 Countries and Regions：{d.get('title')}")
    labels = d.get("tally", {}).get("labels") or {}
    if d.get("tally", {}).get("by") == "country" and any(it.get("country_iso2") == "CN" for it in d["items"]) and labels.get("CN") != "China":
        errs.append("计分板 CN 的显示名须为 China")
    for e in errs:
        print("  ✗", e)
    print(f"{ep.name}：{'闸门通过' if not errs else f'{len(errs)} 处不合规'}")
    return 1 if errs else 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("fix", "gate"))
    ap.add_argument("ep", nargs="+")
    a = ap.parse_args()
    rc = 0
    for e in a.ep:
        ep = Path(e).resolve()
        if a.step == "fix":
            fix(ep)
        else:
            rc |= gate(ep)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
