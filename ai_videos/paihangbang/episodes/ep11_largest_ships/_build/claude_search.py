# -*- coding: utf-8 -*-
"""第二步（follow-up 023）：Claude 自己找图 —— Flickr 搜索（只收可商用 CC 许可），按内容里的船名逐一搜，
标题/描述必须含该船级某艘船的名字才收；再打开照片页取 >=1600 px 的尺寸与页面许可。
输出 reselect/claude_<tag>.json（与 codex 同 schema）。用法：python claude_search.py <tag> [key ...]
"""
import json
import re
import sys
from pathlib import Path

B = Path(__file__).parent
EP = B.parent
sys.path.insert(0, str(B))
import flickr_search as fs  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_tools"))
from image_reselect import item_key  # noqa: E402

Q = {
    "pioneering_spirit": ["Pioneering Spirit"],
    "icon": ["Icon of the Seas", "Star of the Seas", "Legend of the Seas"],
    "cma_seine": ["CMA CGM Seine", "CMA CGM Notre Dame", "CMA CGM Pantheon", "CMA CGM Vendome", "CMA CGM Grand Palais", "CMA CGM Saint Germain", "CMA CGM Orsay"],
    "ever_a": ["Ever Ace", "Ever Alot", "Ever Aim", "Ever Act", "Ever Alp", "Ever Arm", "Ever Art", "Ever Apex", "Ever Atop", "Ever Aria", "Ever Acme", "Ever Aeon", "Ever Ally"],
    "cma_saade": ["CMA CGM Jacques Saade", "CMA CGM Champs Elysees", "CMA CGM Palais Royal", "CMA CGM Louvre", "CMA CGM Rivoli", "CMA CGM Montmartre", "CMA CGM Concorde", "CMA CGM Trocadero", "CMA CGM Sorbonne"],
    "oasis": ["Utopia of the Seas", "Wonder of the Seas", "Symphony of the Seas", "Harmony of the Seas", "Oasis of the Seas", "Allure of the Seas"],
    "msc_irina": ["MSC Irina", "MSC Loreto", "MSC Tessa", "MSC Gemma", "MSC Mariella", "MSC Micol", "MSC Michel Cappellini", "MSC Celestino Maresca", "MSC Nicola Mastro", "MSC Claude Girardet", "MSC Raya", "MSC Mette", "MSC Turkiye"],
    "oocl_spain": ["OOCL Spain", "OOCL Piraeus", "OOCL Felixstowe", "OOCL Zeebrugge", "OOCL Gdynia", "OOCL Valencia", "OOCL Abu Dhabi", "OOCL Sweden", "OOCL Finland", "OOCL Portugal", "OOCL Turkiye"],
    "one_innovation": ["ONE Innovation", "ONE Infinity", "ONE Integrity", "ONE Inspiration", "ONE Ingenuity", "ONE Intelligence"],
    "oocl_wisdom": ["OOCL Wisdom", "OOCL Grace"],
    "msc_gulsun": ["MSC Gulsun", "MSC Samar", "MSC Leni", "MSC Mia", "MSC Febe", "MSC Ambra", "MSC Mina", "MSC Isabella", "MSC Arina", "MSC Nela", "MSC Sixin", "MSC Apolline", "MSC Amelia", "MSC Diletta", "MSC Michelle", "MSC Allegra"],
    "hmm_algeciras": ["HMM Algeciras", "HMM Oslo", "HMM Copenhagen", "HMM Dublin", "HMM Gdansk", "HMM Hamburg", "HMM Helsinki", "HMM Le Havre", "HMM Rotterdam", "HMM Southampton", "HMM Stockholm", "HMM St Petersburg"],
    "berlin_express": ["Berlin Express", "Manila Express", "Hanoi Express", "Busan Express", "Singapore Express", "Damietta Express", "Rotterdam Express", "Gdansk Express", "Bangkok Express", "Genova Express", "Wilhelmshaven Express"],
    "ever_g": ["Ever Given", "Ever Glory", "Ever Globe", "Ever Golden", "Ever Goods", "Ever Genius", "Ever Gifted", "Ever Grade", "Ever Gentle", "Ever Govern", "Ever Greet"],
    "cma_antoine": ["CMA CGM Antoine de Saint Exupery", "CMA CGM Jean Mermoz", "CMA CGM Louis Bleriot"],
    "msc_world": ["MSC World Europa", "MSC World America", "MSC World Asia"],
    "cosco_universe": ["COSCO Shipping Universe", "COSCO Shipping Nebula", "COSCO Shipping Galaxy", "COSCO Shipping Solar", "COSCO Shipping Star", "COSCO Shipping Planet"],
    "madrid_maersk": ["Madrid Maersk", "Munich Maersk", "Moscow Maersk", "Milan Maersk", "Monaco Maersk", "Marseille Maersk", "Manchester Maersk", "Murcia Maersk", "Manila Maersk", "Mumbai Maersk", "Maastricht Maersk"],
    "mol_triumph": ["MOL Triumph", "ONE Triumph", "MOL Trust", "ONE Trust", "MOL Tribute", "ONE Tribute", "MOL Tradition", "ONE Tradition", "MOL Truth", "ONE Truth", "MOL Treasure", "ONE Treasure"],
    "oocl_hk": ["OOCL Hong Kong", "OOCL Germany", "OOCL Japan", "OOCL United Kingdom", "OOCL Scandinavia", "OOCL Indonesia"],
    "disney_adventure": ["Disney Adventure"],
    "valemax": ["Valemax", "Vale Brasil", "Vale Rio de Janeiro", "Vale Beijing", "Vale China", "Ore Brasil", "Pacific Unity", "Yuan He Hai", "Sohar Max", "Berge Everest", "Sea Tubarao", "Ore Tianjin"],
    "cosco_aries": ["COSCO Shipping Aries", "COSCO Shipping Leo", "COSCO Shipping Taurus", "COSCO Shipping Pisces", "COSCO Shipping Scorpio", "COSCO Shipping Gemini", "COSCO Shipping Virgo", "COSCO Shipping Libra", "COSCO Shipping Sagittarius", "COSCO Shipping Aquarius", "COSCO Shipping Capricorn"],
    "barzan": ["Barzan", "Al Muraykh", "Al Nefud", "Al Zubara", "Al Dahna Express", "Al Dahna", "Tihama", "Umm Salal", "Al Jmeliyah"],
    "triple_e": ["Maersk Mc-Kinney Moller", "Majestic Maersk", "Mary Maersk", "Marie Maersk", "Madison Maersk", "Magleby Maersk", "Maribo Maersk", "Marstal Maersk", "Matz Maersk", "Mayview Maersk", "Merete Maersk", "Mette Maersk", "Marchen Maersk", "Margrethe Maersk", "Mogens Maersk", "Munkebo Maersk", "Maren Maersk", "Morten Maersk", "Marit Maersk", "Mathilde Maersk"],
    "msc_oscar": ["MSC Oscar", "MSC Oliver", "MSC Zoe", "MSC Maya", "MSC Sveva", "MSC Clara", "MSC Jade", "MSC Reef", "MSC Mirja", "MSC Erica", "MSC Tina", "MSC Ditte", "MSC Diana", "MSC Ingy", "MSC Eloane", "MSC Mirjam", "MSC Rifaya", "MSC Leanne", "MSC Anna", "MSC Viviana"],
    "cscl_globe": ["CSCL Globe", "CSCL Pacific Ocean", "CSCL Indian Ocean", "CSCL Atlantic Ocean", "CSCL Arctic Ocean"],
    "excel": ["Costa Toscana", "Costa Smeralda", "Arvia", "Iona", "AIDAnova", "AIDAcosma", "Carnival Celebration", "Carnival Jubilee", "Mardi Gras"],
    "meraviglia_plus": ["MSC Euribia", "MSC Grandiosa", "MSC Virtuosa"],
    "beijing_maersk": ["Beijing Maersk", "Berlin Maersk", "Bangkok Maersk", "Brussels Maersk", "Brisbane Maersk", "Barcelona Maersk"],
    "cma_franklin": ["CMA CGM Benjamin Franklin", "CMA CGM Vasco de Gama", "CMA CGM Zheng He"],
    "sphere": ["Sun Princess", "Star Princess"],
    "cma_bougainville": ["CMA CGM Bougainville", "CMA CGM Kerguelen", "CMA CGM Georg Forster"],
    "cma_explorer": ["CMA CGM Marco Polo", "CMA CGM Alexander von Humboldt", "CMA CGM Jules Verne"],
    "msc_london": ["MSC London", "MSC New York", "MSC Amsterdam", "MSC Istanbul", "MSC Hamburg", "MSC Venice"],
    "winning": ["Winning Ambition", "Winning Brave", "Winning Creation", "Winning Devotion"],
    "guaibamax": ["Guaibamax", "Sea Guaiba", "Sea Shanghai", "Ore Shantou", "BOKM Tubarao", "Wooyang Moria", "SAO Grace", "HL Mercury", "Nansha Glory", "Haizhu Flourish", "Grand Pioneer", "Sea Victoria"],
    "ever_e": ["Ever Eon", "Ever Eco", "Ever Echo", "Ever Edit", "Ever Even", "Ever Emit", "Ever Eclat", "Ever Edify"],
    "ane_maersk": ["Ane Maersk", "Astrid Maersk", "Axel Maersk", "Arthur Maersk", "Albert Maersk", "Alva Maersk", "Alexandra Maersk", "Alette Maersk", "Antonia Maersk", "Angelica Maersk", "Adrian Maersk"],
    "meraviglia": ["MSC Meraviglia", "MSC Bellissima"],
    "emma_maersk": ["Emma Maersk", "Estelle Maersk", "Eleonora Maersk", "Evelyn Maersk", "Ebba Maersk", "Elly Maersk", "Edith Maersk", "Eugen Maersk"],
}
# 名字短、易误配的：文字里还须含这些词之一
NEED = {"excel": ["ship", "cruise", "costa", "carnival", "aida", "p&o", "p o"], "sphere": ["princess cruise", "cruise"],
        "barzan": ["container", "ship", "hapag", "uasc"], "valemax": ["ship", "carrier", "bulk", "vloc", "freighter", "vessel"]}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("ü", "u").replace("ø", "o").replace("æ", "ae"))


def page_best(c):
    t = fs.get(c["page_url"], "p_" + c["id"] + ".html")
    dec = json.JSONDecoder()
    for m in re.finditer(r'\{"_flickrModelRegistry":"photo-models"', t):
        try:
            o, _ = dec.raw_decode(t, m.start())
        except Exception:  # noqa: BLE001
            continue
        if str(o.get("id")) != c["id"]:
            continue
        sz = (o.get("sizes") or {}).get("data") or {}
        for k in ("k", "h", "3k", "4k", "o", "l"):
            s = (sz.get(k) or {}).get("data")
            if s and s.get("url"):
                u = s["url"]
                c["image_url"] = "https:" + u if u.startswith("//") else u
                c["w"], c["h"] = s.get("width"), s.get("height")
                break
        dm = re.search(r'"dateTaken":"(\d{4})[^"]*","datePosted":"(\d+)","id":"%s"' % c["id"], t)
        if dm:
            import datetime
            c["taken_year"] = int(dm.group(1))
            c["posted_year"] = datetime.datetime.utcfromtimestamp(int(dm.group(2))).year
        lic = o.get("license")
        if lic is not None:
            c["license"] = int(lic)
            c["licence"] = fs.LIC.get(int(lic), f"flickr-license-{lic}")
        return c
    return c


YEARS = {}
for _c in json.loads((B / "classes_computed.json").read_text(encoding="utf-8")):
    for _m in _c["members"]:
        YEARS[re.sub(r"[^a-z0-9]", "", _m[1].lower())] = int(_m[2])


def ship_year(nm, key):
    n = norm(nm)
    for k, y in YEARS.items():
        if k.endswith(n[-10:]) or n.endswith(k[-10:]):
            return y
    return None


def collect(it, per=10):
    cands = {}
    for nm in Q[it["key"]]:
        for x in fs.search(nm):                 # 引号 + 许可过滤组合会让 Flickr 返回 apiFailed，改不加引号，靠标题/描述含船名过滤
            low = (x["title"] + " " + x["description"]).lower()
            if norm(nm) not in norm(low):
                continue
            if it["key"] in NEED and not any(w in low for w in NEED[it["key"]]):
                continue
            if any(w in low for w in ("summit", "conference", "booth")):
                continue
            if x["license"] not in fs.LIC:
                continue
            x["matched"] = nm
            cands.setdefault(x["id"], x)
        if len(cands) >= 40:
            break
    lst = sorted(cands.values(), key=lambda x: -(x["w"] or 0))
    by_author = {}
    for x in lst:
        by_author.setdefault(x["author"], []).append(x)
    order = []
    while any(by_author.values()):
        for a in list(by_author):
            if by_author[a]:
                order.append(by_author[a].pop(0))
    imgs = []
    for c in order[:30]:
        if len(imgs) >= per:
            break
        c = page_best(c)
        if c.get("license") not in fs.LIC:
            continue
        y = ship_year(c["matched"], it["key"]) or it.get("first_year")
        yr = max(c.get("taken_year") or 0, c.get("posted_year") or 0)
        if y and yr and yr < y - 1:
            continue                      # 同名旧船（如 1995 年的 Legend of the Seas）
        imgs.append({"image_url": c["image_url"], "page_url": c["page_url"], "source": "Flickr", "author": c["author"],
                     "licence": c["licence"], "why": f"Flickr '{c['title'][:80]}' - matches {c['matched']}; {c.get('w')}x{c.get('h')}"})
    return len(cands), imgs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    tag = sys.argv[1]
    only = set(sys.argv[2:])
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    (EP / "_build" / "reselect").mkdir(parents=True, exist_ok=True)
    for i, it in enumerate(data["items"]):
        if only and it["key"] not in only:
            continue
        one = EP / "_build" / "reselect" / f"claude_{tag}_{i:02d}.json"
        if one.exists():
            continue
        n, imgs = collect(it)
        print(f"{i:02d} {it['key']}: {n} matches, kept {len(imgs)}", flush=True)
        one.write_text(json.dumps({"items": [{"key": item_key(i, it), "images": imgs}]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("done", flush=True)


if __name__ == "__main__":
    main()
