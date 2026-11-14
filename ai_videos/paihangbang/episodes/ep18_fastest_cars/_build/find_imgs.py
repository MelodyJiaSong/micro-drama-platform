# -*- coding: utf-8 -*-
"""Claude 自己找图（follow-up 023）：逐项在 Flickr（仅可商用 CC：BY/BY-SA 2.0/4.0、CC0、PDM）与 Pexels 站内搜索，
解析结果页里的照片元数据，按车型关键词过滤，存 _build/find/NN_<slug>.json；再出缩略图拼图供人眼挑选。
不调用任何收费服务。用法：
  python _build/find_imgs.py search [idx ...]     # 抓候选元数据（可续跑，已有的跳过；--force 重抓）
  python _build/find_imgs.py sheet  [idx ...]     # 下载小图出拼图 _build/find/sheet_NN.jpg
"""
import json
import re
import sys
import time
import html as H
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
FIND = HERE / "find"
FIND.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36",
      "Accept-Language": "en"}
PEXELS_DEAD = [False]
SHEET_SUFFIX = [""]
FNS = [None]
FLICKR_LIC = {4: "CC BY 2.0", 5: "CC BY-SA 2.0", 9: "CC0 1.0", 10: "Public Domain Mark 1.0", 11: "CC BY 4.0", 12: "CC BY-SA 4.0"}

# 每项：搜索词列表、标题必须包含的关键词（全部，小写，任一组满足即可）、排除词
Q = {
 "yangwang_u9_xtreme": (["Yangwang U9 Xtreme", "Yangwang U9", "BYD Yangwang U9"], [["u9"]], ["u8", "u7"]),
 "bugatti_chiron_super_sport_300": (["Bugatti Chiron Super Sport 300+", "Chiron Super Sport 300", "Bugatti Chiron Super Sport"], [["chiron", "super sport"], ["chiron", "300"]], ["pur sport", "lego"]),
 "ssc_tuatara": (["SSC Tuatara"], [["tuatara"]], ["aggressor", "lizard", "reptile"]),
 "koenigsegg_agera_rs": (["Koenigsegg Agera RS"], [["agera", "rs"], ["agera rs"]], ["one:1", "regera"]),
 "bugatti_w16_mistral": (["Bugatti W16 Mistral", "Bugatti Mistral"], [["mistral"]], ["wind", "lego"]),
 "czinger_21c": (["Czinger 21C"], [["czinger"]], ["hyper gt"]),
 "hennessey_venom_f5": (["Hennessey Venom F5"], [["venom", "f5"]], []),
 "hennessey_venom_gt": (["Hennessey Venom GT"], [["venom gt"], ["venom", "hennessey"]], ["f5"]),
 "bugatti_veyron_super_sport": (["Bugatti Veyron Super Sport", "Veyron Super Sport"], [["veyron", "super sport"]], ["lego"]),
 "rimac_nevera_r": (["Rimac Nevera R", "Rimac Nevera"], [["nevera"]], []),
 "ssc_ultimate_aero_tt": (["SSC Ultimate Aero", "Shelby SuperCars Ultimate Aero"], [["ultimate aero"], ["ssc", "aero"]], ["tuatara"]),
 "koenigsegg_regera": (["Koenigsegg Regera"], [["regera"]], []),
 "dauer_962_le_mans": (["Dauer 962 Le Mans", "Dauer 962", "Porsche 962 road car"], [["dauer"], ["962", "road"], ["962", "strassen"]], []),
 "mclaren_speedtail": (["McLaren Speedtail"], [["speedtail"]], []),
 "saleen_s7_twin_turbo": (["Saleen S7 Twin Turbo", "Saleen S7"], [["saleen", "s7"]], ["s7-r", "s7r", "lego"]),
 "mclaren_f1": (["McLaren F1 road car", "McLaren F1 1994", "McLaren F1 LM"], [["mclaren f1"]], ["gtr", "formula", "racing", "grand prix", "mp4", "mcl", "f1 team", "f1 car"]),
 "koenigsegg_ccr": (["Koenigsegg CCR"], [["ccr"]], ["ccx", "ccxr"]),
 "bugatti_divo": (["Bugatti Divo"], [["divo"]], []),
 "bugatti_centodieci": (["Bugatti Centodieci"], [["centodieci"]], []),
 "chevrolet_corvette_zr1": (["Corvette ZR1 2025", "C8 Corvette ZR1", "2025 Chevrolet Corvette ZR1"], [["zr1"]], ["c7", "c6", "2019", "2010", "2011", "2012", "2013", "1990", "c4"]),
 "noble_m600": (["Noble M600"], [["m600"]], []),
 "pininfarina_battista": (["Pininfarina Battista"], [["battista"]], []),
 "lamborghini_countach_lpi_800_4": (["Lamborghini Countach LPI 800-4", "Countach LPI 800"], [["800-4"], ["lpi", "countach"], ["countach", "2022"], ["countach", "2021"]], ["lp400", "5000", "qv", "25th"]),
 "lamborghini_aventador_ultimae": (["Lamborghini Aventador Ultimae", "Aventador LP780-4 Ultimae", "Lamborghini Aventador SVJ"], [["ultimae"], ["aventador", "svj"]], ["roadster"]),
 "bugatti_eb110_super_sport": (["Bugatti EB110 Super Sport", "Bugatti EB110 SS", "Bugatti EB110"], [["eb110"], ["eb 110"]], ["centodieci", "lego"]),
 "aston_martin_one_77": (["Aston Martin One-77", "Aston Martin One 77"], [["one-77"], ["one 77"], ["one77"]], []),
 "mercedes_amg_one": (["Mercedes-AMG One", "Mercedes AMG One hypercar"], [["amg one"], ["amg-one"], ["project one"]], ["gt"]),
 "porsche_918_spyder": (["Porsche 918 Spyder"], [["918"]], ["lego"]),
 "koenigsegg_ccx": (["Koenigsegg CCX", "Koenigsegg CCX 2006", "CCX Koenigsegg"], [["ccx"]], ["ccxr", "lego"]),
 "koenigsegg_jesko_absolut": (["Koenigsegg Jesko Absolut", "Koenigsegg Jesko", "Jesko Absolut"], [["jesko"]], ["lego", "jesko von"]),
}
Q3 = {
 "yangwang_u9_xtreme": (["Yangwang U9", "Yangwang U9 Xtreme", "BYD Yangwang U9 supercar", "仰望U9", "Yangwang U9 Goodwood", "Yangwang U9 Munich"], [["u9"], ["yangwang"], ["仰望"]], ["u8", "u7", "lego"]),
 "rimac_nevera_r": (["Rimac Nevera R", "Nevera R", "Rimac Nevera", "Rimac Nevera Goodwood", "Rimac Nevera Monterey"], [["nevera"]], ["lego", "hot wheels"]),
 "dauer_962_le_mans": (["Dauer 962", "Porsche Dauer 962", "Dauer 962 LM road", "Dauer Porsche 962 LM"], [["dauer"]], []),
 "bugatti_centodieci": (["Bugatti Centodieci", "Centodieci"], [["centodieci"]], ["lego"]),
}


# 第二轮：更宽的搜索词 / 过滤（写 find/<key>_r2.json）
Q2 = {
 "yangwang_u9_xtreme": (["Yangwang", "仰望U9", "仰望 U9", "BYD U9", "Yangwang U9 Goodwood", "Yangwang U9 Track"], [["u9"], ["yangwang"], ["仰望"]], ["u8", "u7"]),
 "czinger_21c": (["Czinger", "Czinger 21C Goodwood", "Czinger 21C Monterey", "Czinger hypercar"], [["czinger"], ["21c"]], ["hyper gt", "chassis"]),
 "rimac_nevera_r": (["Nevera R", "Rimac Nevera R Goodwood", "Rimac Nevera Goodwood", "Rimac Nevera Monterey"], [["nevera"]], ["hot wheels", "lego", "moc"]),
 "dauer_962_le_mans": (["Dauer 962 road", "Dauer 962 street", "Dauer Porsche 962 road car", "Porsche 962 street legal", "Dauer 962 LM strassenversion"], [["dauer"], ["962"]], []),
 "mclaren_f1": (["McLaren F1", "McLaren F1 supercar", "McLaren F1 road car 1995", "McLaren F1 Goodwood"], [["mclaren f1"], ["mclaren", "f1"]], ["gtr", "formula 1", "grand prix", "mp4", "mcl3", "mcl6", "f1 team", "lego", "senna", "p1", "gp"]),
 "bugatti_centodieci": (["Centodieci", "Bugatti Centodieci 110", "Bugatti 110 ans"], [["centodieci"]], ["lego"]),
 "chevrolet_corvette_zr1": (["2025 Corvette ZR1", "Corvette ZR1 C8", "C8 ZR1", "Corvette ZR1 2026", "ZR1X"], [["zr1"]], ["c7", "c6", "2019", "2010", "2011", "2012", "2013", "1990", "c4", "lego"]),
 "bugatti_w16_mistral": (["Bugatti Mistral Goodwood", "Bugatti Mistral Monterey", "W16 Mistral roadster"], [["mistral"]], ["lego"]),
 "hennessey_venom_f5": (["Venom F5", "Hennessey F5 Roadster", "Venom F5 Revolution"], [["f5"]], []),
 "ssc_tuatara": (["Tuatara hypercar", "SSC Tuatara 2020"], [["tuatara"]], ["aggressor", "lizard", "reptile"]),
 "bugatti_divo": (["Divo Bugatti", "Bugatti Divo Goodwood"], [["divo"]], ["lego"]),
 "koenigsegg_ccr": (["Koenigsegg CCR 2005", "CCR Koenigsegg"], [["ccr"]], ["ccx", "ccxr"]),
 "mercedes_amg_one": (["AMG ONE", "Mercedes AMG ONE Goodwood"], [["amg one"], ["amg-one"]], ["gt", "lego"]),
}


def get(url: str, timeout=40) -> str:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read().decode("utf-8", "replace")


def flickr(q: str) -> list[dict]:
    url = "https://www.flickr.com/search/?" + urllib.parse.urlencode({"text": q, "license": "4,5,9,10,11,12", "sort": "relevance"})
    s = get(url)
    out = []
    for m in re.finditer(r'\{"data":\{"_flickrModelRegistry":"photo-lite-models",(.*?)"exportMetaType":"model"', s):
        blob = m.group(1)
        def f(k):
            mm = re.search(r'"%s":("(?:[^"\\]|\\.)*"|\d+)' % k, blob)
            return json.loads(mm.group(1)) if mm else None
        lic = f("license")
        if lic not in FLICKR_LIC:
            continue
        sizes = {}
        for sm in re.finditer(r'"(\w+)":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)', blob):
            sizes[sm.group(1)] = ("https:" + sm.group(2).replace("\\/", "/"), int(sm.group(3)), int(sm.group(4)))
        best = max(sizes.values(), key=lambda v: v[1] * v[2]) if sizes else None
        thumb = sizes.get("n") or sizes.get("m") or best
        pid = re.search(r'"id":"(\d+)"', blob)
        owner = f("ownerNsid")
        if not best or not pid:
            continue
        out.append({"image_url": best[0], "w": best[1], "h": best[2], "thumb": thumb[0] if thumb else best[0],
                    "page_url": f"https://www.flickr.com/photos/{owner}/{pid.group(1)}/", "source": "Flickr",
                    "author": (f("realname") or f("username") or "").strip(), "licence": FLICKR_LIC[lic],
                    "title": f("title") or "", "desc": (f("description") or "")[:300]})
    return out


def pexels(q: str) -> list[dict]:
    s = get("https://www.pexels.com/search/" + urllib.parse.quote(q) + "/")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    out = []
    if not m:
        return out
    d = json.loads(m.group(1))
    for row in d["props"]["pageProps"].get("initialData", {}).get("data", []):
        a = row.get("attributes", {})
        if not a.get("id"):
            continue
        u = a.get("user") or {}
        pid = a["id"]
        out.append({"image_url": f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg", "w": a.get("width"), "h": a.get("height"),
                    "thumb": f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&w=400",
                    "page_url": f"https://www.pexels.com/photo/{a.get('slug','')}-{pid}/", "source": "Pexels",
                    "author": f"{u.get('first_name','')}{u.get('last_name','')}".strip(), "licence": "Pexels License",
                    "title": a.get("title") or "", "desc": (a.get("description") or "")[:300]})
    return out


def pexels_curl(q: str) -> list[dict]:
    import subprocess
    r = subprocess.run(["curl", "-sL", "-m", "40", "-A", UA["User-Agent"], "-H", "Accept-Language: en",
                        "https://www.pexels.com/search/" + urllib.parse.quote(q) + "/"], capture_output=True)
    s = r.stdout.decode("utf-8", "replace")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    out = []
    if not m:
        raise RuntimeError("pexels no data, len %d" % len(s))
    d = json.loads(m.group(1))
    for row in d["props"]["pageProps"].get("initialData", {}).get("data", []):
        a = row.get("attributes", {})
        if not a.get("id"):
            continue
        u = a.get("user") or {}
        pid = a["id"]
        out.append({"image_url": f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg", "w": a.get("width"), "h": a.get("height"),
                    "thumb": f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&w=400",
                    "page_url": f"https://www.pexels.com/photo/{a.get('slug','')}-{pid}/", "source": "Pexels",
                    "author": f"{u.get('first_name','')} {u.get('last_name','')}".strip(), "licence": "Pexels License",
                    "title": a.get("title") or "", "desc": (a.get("description") or "")[:300]})
    return out


def flickr_any(q: str) -> list[dict]:
    """全部许可（含 All rights reserved）——只用于风险版候选。"""
    url = "https://www.flickr.com/search/?" + urllib.parse.urlencode({"text": q, "sort": "relevance"})
    s = get(url)
    out = []
    names = {0: "All rights reserved", 1: "CC BY-NC-SA 2.0", 2: "CC BY-NC 2.0", 3: "CC BY-NC-ND 2.0", 6: "CC BY-ND 2.0",
             7: "No known copyright restrictions", 13: "CC BY-ND 4.0", 14: "CC BY-NC 4.0", 15: "CC BY-NC-SA 4.0", 16: "CC BY-NC-ND 4.0", **FLICKR_LIC}
    for m in re.finditer(r'\{"data":\{"_flickrModelRegistry":"photo-lite-models",(.*?)"exportMetaType":"model"', s):
        blob = m.group(1)
        def f(k):
            mm = re.search(r'"%s":("(?:[^"\\]|\\.)*"|\d+)' % k, blob)
            return json.loads(mm.group(1)) if mm else None
        lic = f("license")
        sizes = {}
        for sm in re.finditer(r'"(\w+)":\{"data":\{"displayUrl":"([^"]+)","width":(\d+),"height":(\d+)', blob):
            sizes[sm.group(1)] = ("https:" + sm.group(2).replace("\\/", "/"), int(sm.group(3)), int(sm.group(4)))
        best = max(sizes.values(), key=lambda v: v[1] * v[2]) if sizes else None
        thumb = sizes.get("n") or sizes.get("m") or best
        pid = re.search(r'"id":"(\d+)"', blob)
        owner = f("ownerNsid")
        if not best or not pid:
            continue
        out.append({"image_url": best[0], "w": best[1], "h": best[2], "thumb": thumb[0] if thumb else best[0],
                    "page_url": f"https://www.flickr.com/photos/{owner}/{pid.group(1)}/", "source": "Flickr",
                    "author": (f("realname") or f("username") or "").strip(), "licence": names.get(lic, f"flickr licence {lic}"),
                    "title": f("title") or "", "desc": (f("description") or "")[:300]})
    return out


def matches(c: dict, groups, excl) -> bool:
    t = (c["title"] + " " + c["desc"]).lower()
    if any(x in t for x in excl):
        return False
    return any(all(k in t for k in g) for g in groups)


def items():
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    for i, it in enumerate(data["items"]):
        slug = Path(it["image"]).stem[3:]
        yield i, it, slug, f"{i:02d}_{Path(it['image']).stem}"


def cmd_search(sel, force, table=None, suffix=""):
    for i, it, slug, key in items():
        if sel and i not in sel:
            continue
        table = table or Q
        if slug not in table:
            continue
        f = FIND / f"{key}{suffix}.json"
        if f.exists() and not force:
            continue
        qs, groups, excl = table[slug]
        cands, seen = [], set()
        for q in qs:
            for fn in FNS[0]:
                if fn is pexels and PEXELS_DEAD[0]:
                    continue
                try:
                    rows = fn(q)
                except Exception as e:  # noqa: BLE001
                    print(" ", key, fn.__name__, q, "ERR", e)
                    if fn is pexels and "403" in str(e):
                        PEXELS_DEAD[0] = True
                    rows = []
                for c in rows:
                    if c["image_url"] in seen or not matches(c, groups, excl):
                        continue
                    seen.add(c["image_url"])
                    c["query"] = q
                    cands.append(c)
                time.sleep(1.0)
        f.write_text(json.dumps({"key": key, "name": it["name"], "cands": cands}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(key, len(cands), "candidates", flush=True)


def cmd_sheet(sel):
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    import io
    fnt = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
    for i, it, slug, key in items():
        if sel and i not in sel:
            continue
        suffix = SHEET_SUFFIX[0]
        f = FIND / f"{key}{suffix}.json"
        if not f.exists():
            continue
        cands = json.loads(f.read_text(encoding="utf-8"))["cands"][:24]
        if not cands:
            continue
        TW, TH, cols = 300, 200, 6
        rows = (len(cands) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (TW + 6) + 6, rows * (TH + 40) + 30), (20, 20, 24))
        dr = ImageDraw.Draw(sheet)
        dr.text((6, 6), f"{key}  {it['name']}", font=ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 16), fill=(255, 255, 255))
        from concurrent.futures import ThreadPoolExecutor

        def fetch(c):
            try:
                return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(c["thumb"], headers=UA), timeout=30).read()))
            except Exception:  # noqa: BLE001
                return None
        with ThreadPoolExecutor(8) as ex:
            ims = list(ex.map(fetch, cands))
        for n, c in enumerate(cands):
            x, y = 6 + (n % cols) * (TW + 6), 30 + (n // cols) * (TH + 40)
            im = ims[n]
            if im is not None:
                sheet.paste(ImageOps.contain(im.convert("RGB"), (TW, TH)), (x, y))
            else:
                dr.text((x + 5, y + 5), "下载失败", font=fnt, fill=(255, 80, 80))
            dr.text((x, y + TH + 2), f"#{n} {c['w']}x{c['h']} {c['source'][:6]} {c['licence'][:12]}", font=fnt, fill=(220, 220, 220))
            dr.text((x, y + TH + 19), c["title"][:44], font=fnt, fill=(160, 160, 170))
        sheet.save(FIND / f"sheet_{key}{suffix}.jpg", quality=85)
        print("sheet", key, len(cands), flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    force = "--force" in args
    sel = {int(a) for a in args[1:] if a.isdigit()}
    FNS[0] = (flickr, pexels)
    if args[0] == "search3":          # Pexels（curl）全部项
        FNS[0] = (pexels_curl,)
        cmd_search(sel, force, Q, "_px")
    elif args[0] == "searchrisk":     # Flickr 全许可（风险版）
        FNS[0] = (flickr_any,)
        cmd_search(sel, force, Q2, "_any")
    elif args[0] in ("sheet3", "sheetrisk"):
        SHEET_SUFFIX[0] = "_px" if args[0] == "sheet3" else "_any"
        cmd_sheet(sel)
    elif args[0] == "search4":
        PEXELS_DEAD[0] = True
        cmd_search(sel, force, Q3, "_r3")
    elif args[0] == "sheet4":
        SHEET_SUFFIX[0] = "_r3"
        cmd_sheet(sel)
    elif args[0] == "search2":
        PEXELS_DEAD[0] = True
        cmd_search(sel, force, Q2, "_r2")
    elif args[0] == "sheet2":
        SHEET_SUFFIX[0] = "_r2"
        cmd_sheet(sel)
    else:
        {"search": lambda: cmd_search(sel, force), "sheet": lambda: cmd_sheet(sel)}[args[0]]()
