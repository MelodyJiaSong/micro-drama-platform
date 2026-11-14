# -*- coding: utf-8 -*-
"""ep04 第一步「内容」：从 research/batch_*.json + 本文件的取舍与补充 → ../data.json、../sources.md。
用法：python -I <本目录>/build.py
改数据只改本文件（SELECT / EXTRA / OVERRIDE / INSIGHTS），不手改 data.json 的数据字段（图片字段由找图工具写入，重跑会保留）。
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
R = {}
for b in "ABC":
    for s in json.loads((HERE / "research" / f"batch_{b}.json").read_text(encoding="utf-8"))["species"]:
        R[s["common_name"]] = s

LABEL = {"Javan rhinoceros": "Only in Indonesia", "Sumatran rhinoceros": "Only in Indonesia"}   # 独立审片 m5
IUCN_BADGE = {"NT": "NEAR THREATENED", "VU": "VULNERABLE", "EN": "ENDANGERED", "CR": "CRITICALLY ENDANGERED"}
M49 = {"BW": "Africa", "GA": "Africa", "ZA": "Africa", "ZM": "Africa", "KE": "Africa", "TZ": "Africa", "CF": "Africa",
       "NA": "Africa", "IN": "Asia", "ID": "Asia", "CN": "Asia", "KH": "Asia", "US": "North America", "CA": "North America",
       "PL": "Europe", "RU": "Europe", "EC": "South America"}
COUNTRY = {"BW": "Botswana", "GA": "Gabon", "ZA": "South Africa", "ZM": "Zambia", "KE": "Kenya", "TZ": "Tanzania",
           "CF": "Central African Rep.", "NA": "Namibia", "IN": "India", "ID": "Indonesia", "CN": "China", "KH": "Cambodia",
           "US": "United States", "CA": "Canada", "PL": "Poland", "RU": "Russia", "EC": "Ecuador"}

# 物种 → 屏上名、分布（info 行 map-pin）、找图辨认要点。顺序无关，按体重排序。
SELECT = {
    "African bush elephant": ("African Bush Elephant", "Sub-Saharan Africa",
        "adult bull African bush (savanna) elephant in the wild, big fan-shaped ears, long tusks, full body on open savanna; NOT an Asian elephant, NOT a forest elephant"),
    "Asian elephant": ("Asian Elephant", "South & Southeast Asia",
        "adult male Asian elephant (tusker) in the wild, small rounded ears, twin-domed head, full body; NOT an African elephant; no riders, no chains, no temple decorations"),
    "White rhinoceros": ("White Rhinoceros", "Southern & East Africa",
        "adult white (square-lipped) rhinoceros in the wild, wide square mouth, large shoulder hump, two horns, full body on grassland; NOT a black rhino"),
    "Greater one-horned rhinoceros": ("Indian Rhinoceros", "India & Nepal",
        "greater one-horned (Indian) rhinoceros in the wild, armour-plated skin folds, single horn, full body in tall grass or wetland (e.g. Kaziranga, Chitwan)"),
    "African forest elephant": ("African Forest Elephant", "Central & West Africa",
        "African forest elephant in the wild, rounder oval ears, straight downward-pointing tusks, in a rainforest clearing (bai) e.g. Dzanga Bai; NOT a savanna elephant"),
    "Common hippopotamus": ("Hippopotamus", "Sub-Saharan Africa",
        "adult common hippopotamus in the wild, whole body visible (on land or riverbank), ideally mouth open showing tusks; NOT a pygmy hippo"),
    "Javan rhinoceros": ("Javan Rhinoceros", "Ujung Kulon, Indonesia",
        "Javan rhinoceros (Rhinoceros sondaicus) — extremely rare, photos come from Ujung Kulon National Park (camera traps or wallow photos); NOT an Indian rhino; accept the best real photo available"),
    "Giraffe": ("Giraffe", "Sub-Saharan Africa",
        "adult bull giraffe in the wild, the whole animal from hooves to ossicones visible, on savanna"),
    "Black rhinoceros": ("Black Rhinoceros", "Southern & East Africa",
        "black (hook-lipped) rhinoceros in the wild, pointed prehensile upper lip, two horns, full body; NOT a white rhino"),
    "Gaur": ("Gaur", "South & Southeast Asia",
        "adult bull gaur (Indian bison) in the wild, massive muscular dorsal ridge, white 'stockings' on the legs, full body in Indian forest; NOT domestic cattle, NOT gayal/mithun"),
    "Wild yak": ("Wild Yak", "Tibetan Plateau",
        "WILD yak (Bos mutus) on the Tibetan plateau / Chang Tang, uniformly blackish-brown, long skirt of hair, wild herd — NOT a domestic yak (no white patches, no saddles, no ropes, no herders)"),
    "Wild water buffalo": ("Wild Water Buffalo", "India, Nepal & Thailand",
        "WILD water buffalo (Bubalus arnee) bull, huge wide-sweeping horns, in Kaziranga / Manas / Koshi Tappu; NOT domestic water buffalo (no ropes, no farm, no people)"),
    "American bison": ("American Bison", "North America",
        "adult bull American bison in the wild (Yellowstone etc.), full body with shaggy shoulder hump; NOT European wisent"),
    "Sumatran rhinoceros": ("Sumatran Rhinoceros", "Sumatra & Borneo",
        "Sumatran rhinoceros (hairy, two horns, small reddish-brown rhino), e.g. Way Kambas sanctuary; NOT a Javan or Indian rhino"),
    "African buffalo": ("African Buffalo", "Sub-Saharan Africa",
        "adult bull Cape buffalo in the wild, heavy fused horn boss, full body on savanna"),
    "Banteng": ("Banteng", "Southeast Asia",
        "wild banteng (Bos javanicus) BULL — dark blackish-chestnut coat with white rump patch and white stockings, in forest/grassland (Java Baluran, Borneo); NOT Bali cattle on a farm"),
    "Giant eland": ("Giant Eland", "Central & West Africa",
        "giant (Lord Derby's) eland bull with spiralled horns, black neck with white stripes on the body, full body; NOT a common eland"),
    "European bison (wisent)": ("European Bison", "Poland, Belarus & Russia",
        "European bison (wisent) bull in Białowieża forest or similar, full body; NOT an American bison"),
    "Common eland": ("Common Eland", "East & Southern Africa",
        "common eland bull in the wild, tawny coat, dewlap, short spiralled horns, full body on savanna; NOT a giant eland"),
    "Moose": ("Moose", "Northern forests worldwide",
        "adult bull moose with broad palmate antlers in the wild, full body in boreal forest or wetland"),
    "Polar bear": ("Polar Bear", "The Arctic",
        "adult polar bear in the wild on sea ice or tundra, full body, sharp; not a zoo enclosure"),
    "Grévy's zebra": ("Grévy's Zebra", "Kenya & Ethiopia",
        "Grévy's zebra in the wild (Samburu etc.), narrow dense stripes, white belly, large rounded ears, full body; NOT a plains zebra"),
    "Kiang": ("Kiang", "Tibetan Plateau",
        "kiang (Tibetan wild ass), chestnut-red body with white belly and legs, on the Tibetan plateau / Ladakh, full body"),
    "Wapiti / Elk": ("Elk (Wapiti)", "North America & East Asia",
        "bull elk (wapiti) with big many-tined antlers in the wild (Yellowstone, Rocky Mountains), full body; NOT a moose (Eurasian 'elk'), NOT a red deer"),
    "Takin": ("Takin", "Eastern Himalaya & China",
        "takin (Budorcas taxicolor), golden or Mishmi/Bhutan takin, thick-horned goat-antelope, full body"),
    "Muskox": ("Muskox", "Arctic Canada & Greenland",
        "muskox bull in the Arctic, long shaggy coat, heavy horn boss, full body on tundra"),
    "Plains zebra": ("Plains Zebra", "East & Southern Africa",
        "plains zebra in the wild, broad stripes with shadow stripes, full body on savanna; NOT Grévy's or mountain zebra"),
    "Brown bear": ("Brown Bear", "Northern Eurasia & N. America",
        "adult male brown bear / grizzly in the wild (Alaska, Kamchatka, Finland, Yellowstone), full body, sharp; NOT a black bear, NOT a zoo"),
}

# 研究批次之外补查的物种（主会话 WebSearch，2026-11-03）
EXTRA = [
    {"common_name": "Bongo", "scientific_name": "Tragelaphus eurycerus", "class": "mammal",
     "iucn": {"category": "NT", "assessed_year": 2016, "population_trend": "decreasing", "url": None},
     "male_mass_kg": {"value": 300, "kind": "mean", "range_low": 240, "range_high": 405,
                      "text": "Britannica: males weigh on average 300 kg, up to 400 kg; HMW (via Plazi): males 240–405 kg",
                      "source_name": "Encyclopaedia Britannica, 'bongo'", "source_url": "https://www.britannica.com/print/article/73016", "tier": "secondary"},
     "mass_cross_check": {"value": 322, "source_name": "Handbook of the Mammals of the World via Plazi (240–405 kg midpoint)",
                          "source_url": "https://tb.plazi.org/GgServer/html/03F50713996EFFD606D4FE81FB19F2FD"},
     "max_mass_kg": None,
     "wild_population": {"value": 20000, "display": "15,000–25,000 adults", "unit": "mature individuals", "year": 2016,
                         "source_name": "World Land Trust species data (citing IUCN)", "source_url": "https://www.worldlandtrust.org/?p=41099"},
     "stronghold": {"iso2": "GA", "country": "Gabon", "evidence": "没有分国数量；按分布与保护地面积推断，Gabon / Rep. Congo / CAR 为主要分布国", "source_url": None, "confidence": "low"},
     "notes": "主会话补查：雄性典型体重来源只有百科级（Britannica、HMW 转载）；stronghold 无分国数据，low。"},
    {"common_name": "Mountain zebra", "scientific_name": "Equus zebra", "class": "mammal",
     "iucn": {"category": "VU", "assessed_year": 2019, "population_trend": "increasing", "url": None},
     "male_mass_kg": {"value": 298, "kind": "mean", "range_low": None, "range_high": None,
                      "text": "ADW Equus zebra: stallions average 298 kg, mares 276 kg (Hartmann's)",
                      "source_name": "Animal Diversity Web, Equus zebra", "source_url": "https://animaldiversity.org/accounts/Equus_zebra/", "tier": "primary"},
     "mass_cross_check": {"value": 298, "source_name": "southafrica.co.za (Hartmann's males average 298 kg)", "source_url": "https://southafrica.co.za/hartmanns-mountain-zebra.html"},
     "max_mass_kg": {"value": 343, "text": "Hartmann's stallions ≥7 years mean 343 kg (age-class mean, not a single record)", "source_name": "krugerpark.co.za", "source_url": "https://krugerpark.co.za/africa_hartmans_mountain_zebra.html"},
     "wild_population": None,
     "stronghold": {"iso2": "NA", "country": "Namibia", "evidence": "Hartmann's subspecies ~25,000 in Namibia (Novellie et al. 2002, 1998 data); Cape subspecies only a few thousand in South Africa", "source_url": "https://conservationnamibia.com/articles/2019nam-zebra.php", "confidence": "high"},
     "notes": "Cape 亚种雄性只有 250–260 kg；298 kg 是 Hartmann's 亚种（占全种绝大多数）。IUCN 全种评估年份未直接核到（SANBI 区域评估 VU）。"},
]
SELECT["Bongo"] = ("Bongo", "Central & West Africa",
                   "bongo antelope bull in the wild or a natural forest setting, chestnut coat with 10–15 thin white stripes, spiralled horns, full body")
SELECT["Mountain zebra"] = ("Mountain Zebra", "Namibia & South Africa",
                            "Hartmann's or Cape mountain zebra, small dewlap, stripes NOT reaching the white belly, grid-iron rump pattern, rocky hills; NOT a plains zebra")

# 主会话对研究批次的改动（每条都写原因）
OVERRIDE = {
    "Wapiti / Elk": {"male_mass_kg": {"value": 331, "kind": "mean", "range_low": 178, "range_high": 497,
                     "text": "EOL: males 178–497 kg, averaging 331 kg", "source_name": "Encyclopedia of Life, Cervus canadensis",
                     "source_url": "https://api.eol.org/pages/328649/articles", "tier": "secondary"},
                     "_why": "批次 C 用 WorldAtlas（内容站）340；改用 EOL 均值 331，原 340 作交叉核对"},
    "Gaur": {"male_mass_kg": {"value": 1044, "kind": "range midpoint", "range_low": 588, "range_high": 1500,
             "text": "Walker's Mammals of the World: adult males 588-1,500 kg, females 440-1,000 kg (male-specific; read via Wikipedia 'Gaur')",
             "source_name": "Nowak 1999, Walker's Mammals of the World (male range, via Wikipedia)",
             "source_url": "https://en.wikipedia.org/wiki/Gaur", "tier": "secondary"},
             "mass_cross_check": {"value": 825, "source_name": "Handbook of the Mammals of the World vol. 2 (650-1000 kg, sexes not separated; midpoint)",
                                  "source_url": "https://tb.plazi.org/GgServer/html/03F507139949FFF2037DFDC2F79AF289"},
             "_why": "复审 N2：HMW 650–1000 不分性别（中点 825 低估雄性）；改回唯一能找到的雄性专属范围（Walker's 588–1500，经维基读取，tier=secondary），HMW 作交叉核对（-21%）。差异 > 10% 已记"},
    "African buffalo": {"male_mass_kg": {"value": 700, "kind": "range midpoint", "range_low": 500, "range_high": 900,
                        "text": "HMW: weight 500-900 kg (males), 350-620 kg (females)",
                        "source_name": "Handbook of the Mammals of the World vol. 2 (via Plazi treatment)",
                        "source_url": "https://treatment.plazi.org/id/03F507139945FFFF0375F62EF68AF855", "tier": "primary"},
                        "_why": "独立审片 M1：原主值 775 出自维基；改用 HMW 雄性 500–900 中点 700（与班腾牛同值并列）"},
    "Brown bear": {"male_mass_kg": {"value": 340, "kind": "range midpoint", "range_low": 130, "range_high": 550,
                   "text": "SDZWA fact sheet: males 130-550 kg (287-1213 lb); females 80-250 kg",
                   "source_name": "San Diego Zoo Wildlife Alliance Library, brown bear fact sheet",
                   "source_url": "https://ielc.libguides.com/sdzg/factsheets/brownbear/characteristics", "tier": "secondary"},
                   "_why": "独立审片 M2：口径统一为「全物种雄性范围取中点」，棕熊按 SDZ 130–550 中点 340 入榜（原按物种常见值约 200 落选，与其他物种取法不一致）"},
    "American bison": {"stronghold": {"iso2": "US", "country": "United States",
                       "evidence": "约 25 群平原野牛在美国公园与保护区，约 16,000 头；加拿大林地野牛 5,000+（加平原群仍少于美国）",
                       "source_url": "https://ielc.libguides.com/sdzg/factsheets/americanbison/population", "confidence": "medium"},
                       "_why": "批次 B 给 CA（low）；按圣地亚哥动物园资料库的保护群数量改 US"},
}
for k, ov in OVERRIDE.items():
    ov = dict(ov)
    why = ov.pop("_why")
    old = {f: R[k].get(f) for f in ov}
    if "male_mass_kg" in ov and "mass_cross_check" not in ov:
        R[k]["mass_cross_check"] = {"value": old["male_mass_kg"]["value"], "source_name": old["male_mass_kg"]["source_name"],
                                    "source_url": old["male_mass_kg"]["source_url"]}
    R[k].update(ov)
    R[k]["notes"] = (R[k].get("notes") or "") + f" ｜主会话改动：{why}"
for e in EXTRA:
    R[e["common_name"]] = e

INSIGHTS = [
    (30, "Each flag marks the country where most of that species lives in the wild."),
    (26, "Just missed the cut at #31: the Galápagos giant tortoise, at about 295 kg."),
    (22, "Saltwater crocodiles (males ~460 kg) would rank here, but we count crocodiles as aquatic."),
    (15, "The kouprey (~750 kg) would rank near here, but none has been confirmed alive in decades."),
    (12, "From here on, every typical adult male weighs a tonne or more."),
    (8, "Giraffe experts now recognise 4 species; the IUCN Red List still lists just one."),
]


def fmt_kg(v: float) -> str:
    r = round(v / 50) * 50 if v >= 1000 else round(v)   # 千公斤以下照出处原值（中点也照写），避免取整后相邻两名显示相同
    return f"{r:,.0f} kg"


def fmt_lb(v: float) -> str:
    lb = v * 2.20462
    r = round(lb / 100) * 100 if lb >= 2000 else round(lb / 10) * 10
    return f"{r:,.0f} lb"


def pop_tag(s: dict) -> dict | None:
    p = s.get("wild_population") or {}
    disp = {"African bush elephant": "350,000+ in the wild", "African forest elephant": "~136,000 in the wild",
            "Asian elephant": "<50,000 in the wild", "White rhinoceros": "~15,750 in the wild",
            "Greater one-horned rhinoceros": "~4,075 in the wild", "Black rhinoceros": "~6,790 in the wild",
            "Javan rhinoceros": "only ~50 left", "Sumatran rhinoceros": "only 34–47 left",
            "Common hippopotamus": "115,000–130,000 wild", "Giraffe": "~140,000 in the wild",
            "Gaur": "up to 21,000 adults", "Wild yak": "<10,000 adults", "Wild water buffalo": "<4,000 in the wild",
            "American bison": "11,000–13,000 adults", "African buffalo": "~400,000 adults",
            "Banteng": "~3,300 in the wild", "Giant eland": None, "European bison (wisent)": "~9,800 free-living",
            "Common eland": "~100,000 adults", "Moose": "~3 million", "Polar bear": "~26,000 in the wild",
            "Grévy's zebra": "~2,800 in the wild", "Kiang": "60,000–70,000", "Takin": None, "Muskox": "~170,000",
            "Plains zebra": "500,000+", "Brown bear": "200,000+ in the wild", "Bongo": "15,000–25,000 adults",
            "Western Santa Cruz giant tortoise (largest-bodied Galápagos tortoise candidate)": "~3,400 in the wild"}
    t = disp.get(s["common_name"]) if p else None
    return {"icon": "users", "text": t} if t else None


def max_tag(s: dict) -> dict | None:
    m = s.get("max_mass_kg") or {}
    v = m.get("value")
    if not v or s["common_name"] in ("Mountain zebra",):     # 343 是年龄组均值，不是个体记录
        return None
    return {"icon": "trophy", "text": f"Up to ~{round(v):,} kg"}   # 独立审片 M6：多为范围上限 / 估计，不叫 Record


def build() -> None:
    import sys; sys.stdout.reconfigure(encoding="utf-8")
    rows = []
    for key, (name, rng, hint) in SELECT.items():
        s = R[key]
        mm = s["male_mass_kg"]
        st = s["stronghold"]
        iso = st["iso2"]
        iu = (s.get("iucn") or {}).get("category")
        tags = [t for t in (pop_tag(s), max_tag(s)) if t]
        if key == "African forest elephant":                 # 独立审片 M8：没有实测称重，主值为推算
            tags = [{"icon": "ruler", "text": "Estimate: none weighed"}] + [t for t in tags if t["icon"] != "trophy"][:1]
        if key == "Gaur":                                    # 第 3 轮审片 R3-M1：雄性体重无一手出处，标明是估计区间
            tags = [{"icon": "ruler", "text": "Estimates: 650–1,500 kg"}] + [t for t in tags if t["icon"] != "trophy"][:1]
            s = {**s, "notes": (s.get("notes") or "") + " ｜第 3 轮审片 R3-M1：未找到雄性体重的一手出处（Ahrestani 2018 原文取不到），"
                 "保留中点 1,044 并在卡上首位标「Estimates: 650–1,500 kg」，描述框口径说明写明是估计值"}
        rows.append({
            "rank": 0, "name": name, "subtitle": rng, "scientific_name": s["scientific_name"],
            "country_iso2": iso, "country_name": LABEL.get(key, f"Most in {COUNTRY[iso]}"), "stronghold_country": COUNTRY[iso],
            "continent": M49[iso],
            "value": float(mm["value"]), "value_display": fmt_kg(mm["value"]), "secondary_display": fmt_lb(mm["value"]),
            **({"badge": IUCN_BADGE[iu]} if iu in IUCN_BADGE else {}),
            "tags": tags[:2],
            "source": {"name": mm["source_name"], "url": mm["source_url"], "kind": mm.get("kind"), "tier": mm.get("tier"),
                       "text": mm.get("text"), "retrieved_at": "2026-11-03"},
            "cross_check": s.get("mass_cross_check"),
            "iucn": s.get("iucn"), "stronghold": st, "wild_population": s.get("wild_population"), "max_mass": s.get("max_mass_kg"),
            "image_hint": hint, "notes": s.get("notes") or "", "_key": key,
        })
    rows.sort(key=lambda r: -r["value"])
    assert len(rows) == 30, len(rows)
    for i, r in enumerate(rows, 1):                      # 同值同名次（1,1,3 式）
        r["rank"] = rows[i - 2]["rank"] if i > 1 and r["value"] == rows[i - 2]["value"] else i
    # 保留找图工具已写入的图片字段
    old = {}
    if (EP / "data.json").exists():
        for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]:
            old[it["name"]] = {k: it[k] for k in ("image", "image_credit", "image_focus", "image_risk", "image_note", "image_alt", "image_alt_credit", "thumb") if k in it}
    for r in rows:
        r.pop("_key")
        r.update(old.get(r["name"], {}))
    data = {
        "episode": "ep04_largest_land_animals",
        "title": "Largest Land Animals in the World",
        "kicker": "TOP 30",
        "metric_label": "Typical adult male weight · wild species only",
        "unit": "kg",
        "period_label": "Data as of Nov 2026",
        "source_line": "Sources: IUCN Red List, peer-reviewed studies, zoo & reference works",
        "theme": "savanna",
        "tally": {"by": "continent", "title": "Giants by continent"},
        "layout": {"card_w": 720, "focus": [0.5, 0.45], "intro_hold": 2.5,
                   "image_prefer": ("the whole animal clearly visible (adult, ideally a male), in its natural wild habitat, sharp, eye-level, "
                                    "strong natural light (golden hour or clear day); a wild animal rather than a zoo enclosure; "
                                    "the CORRECT species, not a domestic form or a look-alike relative; landscape or portrait both fine")},
        "music_credit": "Music: original instrumental generated for this channel with Suno (job 101bce70, clips 11cce2f0 + b2fcbabf).",
        "scope_note": ("Ranked by typical adult male weight of living wild species (IUCN taxonomy); where sources give a range, "
                       "we use its midpoint. Excluded: domestic animals, marine mammals, crocodilians, and wild Bactrian camels "
                       "(no published weights separate wild males from domestic ones). Hippos and polar bears are included. "
                       "Flags mark the country with the largest wild population; continents follow UN M49. Ranks within ~5% "
                       "are effectively ties. Forest elephant (2–4.5 t) and gaur (0.65–1.5 t) weights are estimates. "
                       "Low-confidence flags: giraffe, giant eland, bongo, common eland, European bison."),
        "items": rows,
        "insights": [{"after_rank": a, "text": t} for a, t in INSIGHTS],
    }
    for a, t in INSIGHTS:
        assert len(t) <= 90, (len(t), t)
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not (EP / "assets.json").exists():
        (EP / "assets.json").write_text("[]\n", encoding="utf-8")
    for r in rows:
        print(f"{r['rank']:>2} {r['name']:<26} {r['value_display']:>9} {r['secondary_display']:>10}  {r['country_iso2']} {r['continent']:<14} "
              f"{r.get('badge',''):<22} {' · '.join(t['text'] for t in r['tags'])}")


if __name__ == "__main__":
    build()
