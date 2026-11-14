# -*- coding: utf-8 -*-
"""ep21 大米：由 items_draft.json（研究稿）+ 本文件的卡面文字生成 data.json 与 _build/tiles/<key>/content.*。
已有 data.json 时保留其中的 image / image_credit / image_focus 等图片字段（tile_images.py apply 写入），只刷新文字。
本期约定（follow-up 056/057）：poster 版式；卡片只拍米本身（生米粒或一碗白饭），不用配菜；大字写粒型。"""
import json
import re
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
draft = json.loads((EP / "_build/items_draft.json").read_text(encoding="utf-8"))
# rank: (value_display 大字, secondary 小字, badge <=22, [(icon, tag <=24) x2], subtitle)
CARD = {
    1: ("Short grain", "soft & glossy", "JAPAN'S TOP RICE", [("sparkles", "Mild, sweet taste"), ("calendar", "Most planted since 1979")], "Niigata, Japan"),
    2: ("Bold grain", "for sake, not the table", "KING OF SAKE RICE", [("glass-full", "Brewed into sake"), ("calendar", "Bred in 1923")], "Hyogo, Japan"),
    3: ("Glutinous", "stretchy & chewy", "POUNDED INTO MOCHI", [("droplet", "Almost no amylose"), ("hand-stop", "Steamed, then pounded")], "Japan"),
    4: ("Short grain", "soft & fragrant", "EU-PROTECTED GI", [("sparkles", "Aromatic"), ("globe", "EU-China GI deal 2020")], "Heilongjiang, China"),
    5: ("Extra-long", "light & springy", "'SILK SEEDLING'", [("ruler", "3.5x longer than wide"), ("sparkles", "Aromatic")], "Guangdong, China"),
    6: ("Round grain", "fluffy & fragrant", "'FRAGRANT PANDAN'", [("sparkles", "Pandan-leaf scent"), ("calendar", "Named variety 2004")], "West Java, Indonesia"),
    7: ("Broken grain", "soft", "SAIGON STREET STAPLE", [("ruler", "Cracked in milling"), ("droplet", "Absorbs sauces")], "Mekong Delta, Vietnam"),
    8: ("Glutinous", "eaten by hand", "STEAMED IN A BASKET", [("hand-stop", "Rolled into balls"), ("droplet", "Chewy & sticky")], "Laos"),
    9: ("Long grain", "soft & floral", "WORLD'S BEST RICE 2021", [("sparkles", "Thai jasmine rice"), ("trophy", "First Thai EU GI (2013)")], "Northeast Thailand"),
    10: ("Whole grain", "purple & nutty", "PURPLE x JASMINE", [("sparkles", "Deep purple bran"), ("calendar", "Bred from 2002")], "Kasetsart University, Thailand"),
    11: ("Plump grain", "fluffy, grows long", "WORLD'S BEST RICE 2011", [("ruler", "Lengthens when cooked"), ("sparkles", "Aromatic")], "Ayeyarwady Delta, Myanmar"),
    12: ("Black rice", "sticky, cooks purple", "FEAST-DAY KHEER", [("sparkles", "Black, turns purple"), ("droplet", "Glutinous")], "Manipur, India"),
    13: ("Tiny grain", "buttery aroma", "TEMPLE OFFERING RICE", [("sparkles", "Buttery scent"), ("ruler", "Very short & round")], "West Bengal, India"),
    14: ("Bold grain", "red & earthy", "SOLD PARBOILED", [("sparkles", "Red bran left on"), ("droplet", "Long soak & cook")], "Kerala, India"),
    15: ("Red rice", "firm & nutty", "HIGHEST RICE ON EARTH", [("mountain", "Grown near 3,000 m"), ("sparkles", "Red grain")], "Jumla, Nepal"),
    16: ("Extra-long", "dry & fluffy", "12 mm WHEN COOKED", [("ruler", "Doubles in length"), ("sparkles", "Nutty aroma")], "Punjab, India & Pakistan"),
    17: ("Ribbed grain", "firm", "THE PLOV RICE", [("sparkles", "Pinkish tint"), ("trophy", "GI-listed plov (2026)")], "Fergana Valley, Uzbekistan"),
    18: ("Long grain", "fluffy & fragrant", "FOR CHELOW & TAHDIG", [("sparkles", "Fragrant"), ("ruler", "Long & slender")], "Gilan, Iran"),
    19: ("Medium grain", "tender, for pilav", "FIT FOR THE SULTAN", [("sparkles", "Aromatic"), ("trophy", "Turkish PDO (2017)")], "Kastamonu, Türkiye"),
    20: ("Large grain", "creamy, firm core", "RISOTTO FAVOURITE", [("calendar", "Created in 1945"), ("droplet", "Stays al dente")], "Vercelli & Pavia, Italy"),
    21: ("Red rice", "chewy & nutty", "FIRST HARVEST 1988", [("sparkles", "Wholegrain red"), ("trophy", "Camargue PGI rice")], "Rhône Delta, France"),
    22: ("Round grain", "absorbent", "DO SINCE 1986", [("droplet", "Soaks up broth"), ("mountain", "Mountain-grown")], "Calasparra, Spain"),
    23: ("Medium grain", "creamy in broth", "PORTUGAL'S FAVOURITE", [("users", "16 kg/person a year"), ("droplet", "Soaks up broth")], "Ribatejo, Portugal"),
    24: ("Short grain", "soft & slightly sticky", "AFRICA'S JAPONICA", [("droplet", "Soft & sticky"), ("sparkles", "Stuffed into mahshi")], "Nile Delta, Egypt"),
    25: ("Unpolished", "firm, swells up", "BRAN LEFT ON", [("sparkles", "Strong aroma"), ("droplet", "Firm & chewy")], "Ogun State, Nigeria"),
    26: ("Own species", "red bran, nutty", "DOMESTICATED IN AFRICA", [("calendar", "~3,000 years ago"), ("sparkles", "Oryza glaberrima")], "Inner Niger Delta, Mali"),
    27: ("Long & thin", "loose & separate", "70% FROM ONE STATE", [("ruler", "'Little needle'"), ("sparkles", "For arroz e feijão")], "Rio Grande do Sul, Brazil"),
    28: ("Large grain", "soft, holds sauce", "DENOMINATION 2012", [("sparkles", "Chalky 'white belly'"), ("droplet", "For arroz rojo")], "Morelos, Mexico"),
    29: ("Long grain", "tender & creamy", "REVIVED IN 1986", [("sparkles", "Golden hull"), ("calendar", "From 14 lb of seed")], "South Carolina, USA"),
    30: ("Aquatic grass", "chewy", "NOT TRUE RICE", [("ruler", "Long needle seeds"), ("trophy", "Minnesota state grain")], "Great Lakes, USA & Canada"),
}
# ── v2（第 1 轮独立审片 qc.md 后，follow-up 060）：大字统一粒长四档（USDA 口径：short ≤5.5 mm、medium 5.51–6.6、long ≥6.61；
#    extra-long 指 basmati 类 ≥7 mm 细长粒），副字统一口感，标签 1 = 颜色 / 香气，特殊身份与看点放徽章；未核实的说法已换掉。
# rank: (value_display, secondary, badge <=22, [(icon, tag <=24)...], subtitle)
CARD = {
    1: ("Short grain", "soft & sticky", "JAPAN'S TOP RICE", [("sparkles", "White · mild & sweet"), ("calendar", "Most planted since 1979")], "Niigata, Japan"),
    2: ("Short grain", "brewed, not eaten", "KING OF SAKE RICE", [("sparkles", "White, opaque core"), ("glass-full", "Brewed into sake")], "Hyogo, Japan"),
    3: ("Short grain", "very sticky & chewy", "GLUTINOUS · FOR MOCHI", [("sparkles", "Opaque white"), ("droplet", "Almost no amylose")], "Japan"),
    4: ("Short grain", "soft & glossy", "EU-PROTECTED GI", [("sparkles", "White · aromatic"), ("globe", "EU-China GI deal 2020")], "Heilongjiang, China"),
    5: ("Extra-long", "light & springy", "'SILK SEEDLING'", [("sparkles", "White · aromatic"), ("ruler", "3.5x+ longer than wide")], "Guangdong, China"),
    6: ("Medium grain", "fluffy, a little sticky", "'FRAGRANT PANDAN'", [("sparkles", "White · pandan scent"), ("calendar", "Named variety 2004")], "West Java, Indonesia"),
    7: ("Broken grain", "soft, soaks up sauce", "SAIGON STREET STAPLE", [("sparkles", "White · cracked bits"), ("droplet", "Absorbs sauces")], "Mekong Delta, Vietnam"),
    8: ("Long grain", "sticky, eaten by hand", "GLUTINOUS · STEAMED", [("sparkles", "Opaque white"), ("hand-stop", "Rolled into balls")], "Laos"),
    9: ("Long grain", "soft & clingy", "'BEST RICE' 2020+2021", [("sparkles", "White · jasmine scent"), ("trophy", "First Thai EU GI (2013)")], "Northeast Thailand"),
    10: ("Long grain", "soft but chewy", "PURPLE x JASMINE", [("sparkles", "Purple · whole grain"), ("calendar", "Bred from 2002")], "Kasetsart University, Thailand"),
    11: ("Short grain", "fluffy, grows long", "MYANMAR'S PEARL RICE", [("sparkles", "White · aromatic"), ("ruler", "Lengthens when cooked")], "Ayeyarwady Delta, Myanmar"),
    12: ("Medium grain", "sticky & soft", "GLUTINOUS BLACK RICE", [("sparkles", "Black, cooks purple"), ("trophy", "Indian GI tag (2020)")], "Manipur, India"),
    13: ("Short grain", "soft, a little sticky", "TEMPLE OFFERING RICE", [("sparkles", "White · buttery aroma"), ("trophy", "Indian GI tag (2017)")], "West Bengal, India"),
    14: ("Medium grain", "firm & chunky", "PARBOILED RED RICE", [("sparkles", "Red bran left on"), ("droplet", "Long soak & cook")], "Kerala, India"),
    15: ("Medium grain", "firm & nutty", "GROWN NEAR 3,000 m", [("sparkles", "Red grain"), ("mountain", "High-altitude rice")], "Jumla, Nepal"),
    16: ("Extra-long", "dry & fluffy", "12 mm WHEN COOKED", [("sparkles", "White · nutty aroma"), ("ruler", "Grows 1.7x+ longer")], "Punjab, India & Pakistan"),
    17: ("Medium grain", "firm & separate", "THE PLOV RICE", [("trophy", "GI-listed plov (2026)")], "Fergana Valley, Uzbekistan"),
    18: ("Long grain", "fluffy & separate", "IRAN'S CASPIAN RICE", [("sparkles", "White · fragrant"), ("ruler", "Long & slender")], "Gilan, Iran"),
    19: ("Medium grain", "tender & separate", "FIT FOR THE SULTAN", [("sparkles", "White · aromatic"), ("trophy", "Turkish PDO (2017)")], "Kastamonu, Türkiye"),
    20: ("Long grain", "creamy, firm core", "RISOTTO FAVOURITE", [("sparkles", "Pearly white core"), ("calendar", "Created in 1945")], "Vercelli & Pavia, Italy"),
    21: ("Medium grain", "chewy & nutty", "FIRST HARVEST 1988", [("sparkles", "Red · whole grain"), ("trophy", "Camargue PGI rice")], "Rhône Delta, France"),
    22: ("Short grain", "absorbent, stays whole", "DO SINCE 1986", [("sparkles", "Pearly white"), ("droplet", "Soaks up broth")], "Calasparra, Spain"),
    23: ("Medium grain", "creamy in broth", "EU PGI SINCE 2008", [("sparkles", "White japonica"), ("droplet", "Soaks up broth")], "Ribatejo, Portugal"),
    24: ("Short grain", "soft, a little sticky", "AFRICA'S JAPONICA", [("sparkles", "White japonica"), ("droplet", "Stuffed into mahshi")], "Nile Delta, Egypt"),
    25: ("Medium grain", "firm, swells up", "UNPOLISHED, BRAN ON", [("sparkles", "Brown-red · aromatic")], "Ogun State, Nigeria"),
    26: ("Medium grain", "firm & nutty", "A SEPARATE SPECIES", [("sparkles", "Oryza glaberrima"), ("calendar", "~3,000 years ago")], "Inner Niger Delta, Mali"),
    27: ("Long grain", "loose & separate", "70% FROM ONE STATE", [("sparkles", "For arroz e feijão")], "Rio Grande do Sul, Brazil"),
    28: ("Extra-long", "soft, holds sauce", "MEXICAN DO SINCE 2012", [("sparkles", "Chalky 'white belly'"), ("droplet", "For arroz rojo")], "Morelos, Mexico"),
    29: ("Long grain", "tender & creamy", "REVIVED IN 1986", [("sparkles", "Golden hull"), ("calendar", "From 14 lb of seed")], "South Carolina, USA"),
    30: ("Extra-long", "chewy, splits open", "NOT TRUE RICE", [("sparkles", "Dark · a water grass"), ("trophy", "Minnesota state grain")], "Great Lakes, USA & Canada"),
}
NAME = {27: "Brazilian Long-Grain"}          # 「Agulhinha」市场名无来源（qc M3）
FLAG = {16: ("in-pk", "India / Pakistan"), 30: ("us-ca", "USA / Canada")}   # 两国共有：双旗（qc M2 / m6）
CORNER = {**{r: "EAST ASIA" for r in range(1, 6)}, **{r: "SE ASIA" for r in range(6, 12)},
          **{r: "SOUTH ASIA" for r in range(12, 17)}, 17: "CENTRAL ASIA", 18: "WEST ASIA", 19: "WEST ASIA",
          **{r: "EUROPE" for r in range(20, 24)}, 24: "NORTH AFRICA", 25: "WEST AFRICA", 26: "WEST AFRICA",
          27: "S. AMERICA", 28: "N. AMERICA", 29: "N. AMERICA", 30: "N. AMERICA"}

# 画面描述（找图 / 出图共用）：只拍米本身
LOOK = {
    1: "short, plump, translucent white japonica grains; cooked: glossy white rice in a plain bowl",
    2: "large bold white grains with an opaque white heart (shinpaku); often shown highly polished, almost round",
    3: "opaque chalky-white short round glutinous grains; cooked: very sticky glossy mass",
    4: "short-medium translucent white japonica grains; cooked: glossy, slightly sticky white rice",
    5: "extra-long very slender translucent white indica grains; cooked: separate, springy, long grains",
    6: "medium-bold roundish white grains (javanica bulu type); cooked: fluffy, slightly sticky",
    7: "white broken rice fragments (1/2-1/3 length pieces) of long-grain rice; cooked: soft heap of small broken grains",
    8: "opaque white long glutinous grains; cooked: sticky rice in a woven bamboo basket (tip khao)",
    9: "long slender translucent white grains (Thai jasmine); cooked: soft, slightly clingy white rice",
    10: "long slender deep purple-black whole grains; cooked: dark purple rice",
    11: "short plump white grains; cooked: grains elongate, fluffy white rice",
    12: "black glutinous whole grains; cooked: deep purple, sticky",
    13: "very small short round white grains; cooked: tiny fragrant white rice",
    14: "bold coarse grains with reddish bran, parboiled, pink-red streaks; cooked: chunky red-brown rice",
    15: "short-medium red rice grains; cooked: firm red rice",
    16: "extra-long slender white grains; cooked: very long, dry, separate grains",
    17: "medium ribbed grains with a pinkish-red tint and a visible furrow; cooked: separate grains holding shape",
    18: "long slender white Iranian grains; cooked: fluffy white rice (chelow), separate grains",
    19: "medium white grains; cooked: tender separate white rice (pilav), plain",
    20: "large pearly-white medium-long grains with an opaque white core; raw close-up",
    21: "short-medium red-brown wholegrain rice; cooked: chewy red rice",
    22: "short round pearly-white grains; raw close-up or plain cooked",
    23: "medium-long white japonica grains; raw close-up",
    24: "short-medium white japonica grains (Egyptian rice); raw close-up or plain cooked",
    25: "unpolished short-medium grains, mixed brown, reddish and cream colours, slightly irregular; raw close-up",
    26: "medium grains with reddish-brown bran (Oryza glaberrima); raw close-up",
    27: "long thin white grains; cooked: loose separate white rice, plain",
    28: "large extra-long white grains with a chalky white belly; raw close-up",
    29: "long white grains (heirloom Carolina Gold); raw close-up; optionally golden hulls",
    30: "very long needle-like dark brown to black seeds of wild rice (Zizania); raw close-up; cooked: some split open showing white inside",
}
INSIGHTS = [
    (3, "IRRI's genebank in the Philippines stores over 127,000 rice samples, the largest on Earth."),
    (8, "Glutinous rice is gluten-free: 'glutinous' means glue-like sticky, not gluten."),
    (13, "Sticky or fluffy? It's the starch: low-amylose rice clings, high-amylose rice stays apart."),
    (19, "Rice is the staple food for nearly half of the world's people."),
    (23, "Senegal's ceebu jën, UNESCO-listed in 2021, is made with fish and broken rice."),
    (28, "2004 World Food Prize: Yuan Longping (hybrid rice) and Monty Jones (NERICA, for Africa)."),
]
KEEP = ("image", "image_credit", "image_focus", "image_risk", "image_note", "image_alt", "image_alt_credit")


def tile_key(i: int, name: str) -> str:
    return f"{i:02d}_" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def main() -> None:
    old = {}
    if (EP / "data.json").exists():
        old = {it["rank"]: it for it in json.loads((EP / "data.json").read_text(encoding="utf-8"))["items"]}
    items = []
    for x in draft:
        r = x["rank"]
        vd, sec, badge, tags, sub = CARD[r]
        assert len(badge) <= 22, badge
        for _, t in tags:
            assert len(t) <= 24, t
        iso, cname = FLAG.get(r, (x["country_iso2"], x["country_name"]))
        it = {"rank": r, "name": NAME.get(r, x["name"]), "subtitle": sub, "country_iso2": iso,
              "country_name": cname, "continent": x["continent"],
              "value": 0, "value_display": vd, "secondary_display": sec, "badge": badge,
              "corner": CORNER[r],
              "tags": [{"icon": i, "text": t} for i, t in tags], "source": x["source"],
              "notes": (f"Fact: {x['fact']} | Local name: {x.get('local_name') or '-'} | Grain: {x['grain']}; "
                        f"colour {x['colour']}; texture {x['texture']}. {x.get('notes') or ''}")}
        for k in KEEP:
            if k in old.get(r, {}):
                it[k] = old[r][k]
        items.append(it)
    d = {"episode": "ep21_rice_varieties", "mode": "list", "title": "30 Kinds of Rice Around the World",
         "youtube_title": "30 Kinds of Rice Around the World", "kicker": "30 KINDS OF RICE",
         "metric_label": "Grain length", "unit": "", "period_label": "From sticky to fluffy, white to black",
         "source_line": "Sources: GI registers, FAO, IRRI, journals · Images: AI-generated",
         "theme": "savanna", "tally": {"by": "continent", "title": "Rice by continent"},
         "layout": {"card_w": 720, "focus": [0.5, 0.5], "intro_hold": 2.5, "card_style": "poster"},
         "scope_note": ("30 rice varieties and rice types, one per kind, ordered as a journey from East Asia west to the "
                        "Americas. Not a ranking. Each card shows grain length (USDA classes: short, medium, long; extra-long "
                        "= basmati-type slender grains), texture, colour and aroma. Flags show the growing country; basmati "
                        "(India & Pakistan) and wild rice (USA & Canada) show both. All rice images are AI-generated illustrations. Wild rice is included as a famous "
                        "'rice' that is actually a different grass. Per-item sources are listed in the replies under the pinned comment."),
         "insights": [{"after_rank": a, "text": t} for a, t in INSIGHTS],
         "items": items}
    for _, t in INSIGHTS:
        assert len(t) <= 90, t
    (EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not (EP / "assets.json").exists():
        (EP / "assets.json").write_text("[]\n", encoding="utf-8")
    for i, (x, it) in enumerate(zip(draft, items)):
        td = EP / "_build/tiles" / tile_key(i, x["name"])
        td.mkdir(parents=True, exist_ok=True)
        desc = f"{x['grain']} rice, {x['colour'].lower()}, from {it['subtitle']}"
        (td / "content.json").write_text(json.dumps({"description": desc, "wiki_url": "", "coords": None, "ref_image": None,
                                                     "extract": ""}, ensure_ascii=False, indent=1), encoding="utf-8")
        md = [f"# #{x['rank']} {x['name']} ({x.get('local_name') or ''})", "",
              f"- Card: {x['name']} — {it['subtitle']}, {it['country_name']}; big text '{it['value_display']}'",
              f"- Grain: {x['grain']} · colour: {x['colour']} · aroma: {x['aroma']} · texture: {x['texture']}",
              f"- Fact: {x['fact']}", f"- Source: {x['source']['url']}",
              (f"- What the photo must show (episode rule, user 2026-11-06): ONLY the rice itself — {LOOK[x['rank']]}. "
               "No side dishes, curries, toppings, meat, sushi, garnish-heavy plates. Raw grains close-up, or a plain "
               "bowl / heap of plain cooked rice."),
              f"- Search hints: {x.get('image_query_grain') or ''}", f"- Notes: {x.get('notes') or ''}"]
        (td / "content.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("data.json:", len(items), "items")


if __name__ == "__main__":
    main()
