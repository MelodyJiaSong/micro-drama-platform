# -*- coding: utf-8 -*-
"""items_def.py → data.json（保留已存在的 image / image_credit / image_focus / image_alt*），并写 _build/content/NN_<slug>.md。
python _build/build.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import ITEMS, INSIGHTS, R  # noqa: E402

CONT = {"CN": "Asia", "FR": "Europe", "US": "North America", "SE": "Europe", "HR": "Europe", "DE": "Europe",
        "GB": "Europe", "IT": "Europe"}
KEEP = ("image", "image_credit", "image_focus", "image_alt", "image_alt_credit", "image_risk", "image_note")

old = {}
if (EP / "data.json").exists():
    for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]:
        old[it["name"]] = it

items = sorted(ITEMS, key=lambda d: -d["kmh"])
out = []
prev_val, prev_rank = None, 0
for n, d in enumerate(items, 1):
    rank = prev_rank if d["kmh"] == prev_val else n
    prev_val, prev_rank = d["kmh"], rank
    verified = d["kind"] == "V"
    badge = "VERIFIED" if verified else "CLAIMED"
    if d.get("badge_new"):
        badge = f"{d['badge_new']} · {badge}"
    tags = []
    if d.get("tags"):
        tags = [{"icon": i, "text": t} for i, t in d["tags"]]
    elif verified:
        second = ("ruler", d["two_way"]) if d.get("two_way") else d.get("extra_tag")
        if second:
            tags.append({"icon": second[0], "text": second[1]})
        tags.append({"icon": "calendar", "text": f"{d['year']} run"})
    else:
        tags.append({"icon": "calendar", "text": d["year"]})
        tags.append({"icon": "users", "text": d["built"]})
    for t in tags:
        assert len(t["text"]) <= 24, t
    assert len(badge) <= 22, badge
    cross_val = d["cross"][2] if len(d["cross"]) > 2 else None
    item = {
        "rank": rank,
        "name": d["name"],
        "subtitle": d.get("venue", "") if verified else "",
        "country_iso2": d["iso"],
        "country_name": d["country"],
        "continent": CONT[d["iso"]],
        "value": d["kmh"],
        "value_display": f"{round(d['kmh']):,} km/h",
        "secondary_display": d["mph_disp"],
        "badge": badge,
        "tags": tags,
        "image": f"assets/img/{rank:02d}_{d['slug']}.jpg",
        "image_credit": "",
        "image_hint": d["hint"],
        "source": {"name": d["src"][0], "url": d["src"][1], "retrieved_at": R},
        "cross_check": {"name": d["cross"][0], "url": d["cross"][1], "value": cross_val,
                        "diff_pct": round(abs(d["kmh"] - cross_val) / d["kmh"] * 100, 1) if cross_val else None},
        "notes": d["notes"],
        "measure": "verified" if verified else "claimed",
    }
    o = old.get(d["name"])
    if o:
        for k in KEEP:
            if k in o:
                item[k] = o[k]
    out.append(item)

N = len(out)
data = {
    "episode": "ep18_fastest_cars",
    "title": "Fastest Production Cars in the World",
    "kicker": f"TOP {N}",
    "metric_label": "Top speed · VERIFIED one-way run or maker CLAIM",
    "unit": "km/h",
    "period_label": "Data as of Nov 2026",
    "source_line": "Sources: maker releases, independent timing (Racelogic, TÜV), press",
    "theme": "velocity",
    "tally": {"by": "country", "title": "Cars by brand country"},
    "items": out,
    "insights": [{"after_rank": a, "text": t} for a, t in INSIGHTS],
    "scope_note": ("Ranking: fastest one-way run timed by an independent body (VERIFIED: Racelogic, TUV, Guinness, FMSCI) or the maker's own figure (CLAIMED). "
                   "The official Guinness-style two-way record is the SSC Tuatara's 455 km/h (2021); two-way averages are shown on the cards. "
                   "Design targets and simulations are not counted. Cars: street-legal series production, 10+ built, deliveries started by Nov 2026; one card per model. "
                   "Country = brand origin."),
    "layout": {"card_w": 800, "focus": [0.5, 0.55], "intro_hold": 2.5,
               "image_prefer": "the exact model and version, whole car visible, three-quarter front or side view, sharp, outdoor, real photograph (no renders, no CGI, no configurator images); landscape is fine"},
}
for ins in data["insights"]:
    assert len(ins["text"]) <= 90, (len(ins["text"]), ins["text"])
assert len(data["scope_note"]) <= 600, len(data["scope_note"])
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
if not (EP / "assets.json").exists():
    (EP / "assets.json").write_text("[]", encoding="utf-8")

# ── 第一步：每项内容落盘（follow-up 016）──
cdir = HERE / "content"
cdir.mkdir(exist_ok=True)
for it, d in zip(out, items):
    md = f"""# #{it['rank']} {d['name']}

- 品牌国 / 国旗：{d['country']}（{d['iso']}）
- 口径：{'VERIFIED（独立计时实测，单向最高）' if d['kind'] == 'V' else 'CLAIMED（厂方数字）'}；主值 {d['kmh']} km/h（{d['mph_disp']}）
- 年份：{d['year']}；产量：{d['built']}；动力：{d['power']}
- 主源：[{d['src'][0]}]({d['src'][1]})
- 交叉核对：[{d['cross'][0]}]({d['cross'][1]})

## 它是什么 / 记录细节
{d['notes']}

## 长什么样（辨认特征）
{d['look']}

## 易混淆对象（找图要排除）
{d['confuse']}

## 最佳画面
全车可见，四分之三前侧或正侧，室外自然光；真实照片，不要渲染图、官方 CG 或配置器图。车展灯下的整车照可作备选。

## 给找图用的 image_hint
{d['hint']}
"""
    (cdir / f"{it['rank']:02d}_{d['slug']}.md").write_text(md, encoding="utf-8")

from collections import Counter  # noqa: E402
print(N, "items;", Counter(i["country_name"] for i in out).most_common())
print("verified", sum(i["measure"] == "verified" for i in out), "claimed", sum(i["measure"] == "claimed" for i in out))
for i in out:
    print(i["rank"], i["name"], i["value_display"], i["badge"], [t["text"] for t in i["tags"]])
