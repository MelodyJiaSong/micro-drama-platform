# -*- coding: utf-8 -*-
"""follow-up 016 第一步：每项照片题材的文字内容落盘 content/NN_<slug>.md（Wikipedia 文字，仅作描述参考）。"""
import json, time, urllib.parse, urllib.request
from pathlib import Path
B = Path(__file__).parent
EP = B.parent
WIKI = {
 "RU": "Lake Baikal", "CA": "Moraine Lake", "US": "Grand Canyon", "CN": "Li River", "BR": "Lençóis Maranhenses National Park",
 "AU": "Uluru", "IN": "Kangchenjunga", "AR": "Perito Moreno Glacier", "KZ": "Charyn Canyon", "DZ": "Tassili n'Ajjer",
 "CD": "Mount Nyiragongo", "SA": "Elephant Rock (Saudi Arabia)", "MX": "Copper Canyon", "ID": "Mount Bromo", "SD": "Meroë",
 "LY": "Ubari Lakes", "IR": "Lut Desert", "MN": "Orkhon Valley", "PE": "Machu Picchu", "TD": "Ennedi Plateau",
 "NE": "Aïr Mountains", "AO": "Kalandula Falls", "ML": "Bandiagara Escarpment", "ZA": "Table Mountain", "CO": "Cocora Valley",
 "ET": "Simien Mountains National Park", "BO": "Salar de Uyuni", "MR": "Adrar Plateau", "EG": "White Desert National Park",
 "TZ": "Mount Kilimanjaro", "VE": "Angel Falls", "NG": "Zuma Rock", "NA": "Deadvlei", "MZ": "Bazaruto Archipelago",
 "PK": "Saiful Muluk", "TR": "Cappadocia", "CL": "Torres del Paine National Park", "ZM": "Victoria Falls", "MM": "Bagan",
 "SS": "Imatong Mountains", "AF": "Band-e Amir National Park", "SO": "Geography of Somalia", "CF": "Dzanga-Sangha Special Reserve",
 "UA": "Chornohora", "KE": "Maasai Mara", "MG": "Avenue of the Baobabs", "BW": "Okavango Delta", "FR": "Étretat",
 "YE": "Socotra", "TH": "Phang Nga Bay",
}
UA = {"User-Agent": "paihangbang-ep12-content/1.0 (research; contact via repo)"}
data = json.load(open(EP / "data.json", encoding="utf-8"))
for it in data["items"]:
    iso = it["country_iso2"]
    out = B / "content" / (Path(it["image"]).stem + ".md")
    if out.exists():
        continue
    title = WIKI[iso]
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts|pageprops", "explaintext": 1, "exsectionformat": "plain",
                                "titles": title, "redirects": 1, "format": "json", "exintro": 1})
    text, rt = None, title
    for attempt in range(6):
        try:
            d = json.loads(urllib.request.urlopen(urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers=UA), timeout=60).read())
            page = next(iter(d["query"]["pages"].values()))
            text = page.get("extract") or "(no extract)"
            rt = page.get("title", title)
            break
        except Exception as e:  # 429：退避重试
            text = f"(fetch failed: {e})"
            time.sleep(15 * (attempt + 1))
    out.write_text(f"# #{it['rank']} {it['name']} · photo subject: {it['subtitle']}\n\n"
                   f"- Wikipedia: https://en.wikipedia.org/wiki/{urllib.parse.quote(rt.replace(' ', '_'))} (text only, retrieved 2026-11-03)\n"
                   f"- image_hint (draft): {it['image_hint']}\n\n## Wikipedia extract (intro)\n\n{text}\n", encoding="utf-8")
    print(out.name, rt, len(text))
    time.sleep(4)
