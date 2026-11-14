"""Build ep02 data.json + assets.json + assets/img/*.jpg from items_def.py and Commons metadata.

Usage (from anywhere):  python -I <this dir>/build.py [--no-download]
- Reads raw/commons_info_round*.json (Commons imageinfo responses saved by commons_info.py);
  queries Commons again only for chosen files missing from them.
- Downloads the 1600 px thumbnail (or the original if narrower), applies the optional crop,
  saves JPEG q=90 as assets/img/NN_<slug>.jpg, records sha256.
Downloaded bytes are opened only by Pillow; nothing downloaded is executed.
"""
import hashlib, html, io, json, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
sys.path.insert(0, str(HERE))
from items_def import ITEMS, INSIGHTS  # noqa: E402

RETRIEVED = "2026-11-03"
UA = {"User-Agent": "paihangbang-research/0.1 (contact via repo owner)"}
OK_PREFIX = ("cc by ", "cc by-sa ", "cc0", "public domain", "pd")

# Plain-text author overrides where Commons 'Artist' HTML is noisy (checked by hand on the file pages' metadata).
AUTHOR_OVERRIDE = {
    "Karisimbi2.jpg": "Amakuru",
    "Ukok Plateau 2.jpg": "Kobsev",
    "Mount Wilhelm.jpg": "Nomadtales",
    "Cerro Chirripo Picture 1191 zoom in.jpg": "Peter Andersen; derivative work: Mariordo",
    "Pico Cristobal Colon.jpg": "Sylvain Perret",
    "Kodaki fuji frm shojinko refurb.jpg": "名古屋太郎 (edited by Hannes_24)",
    "Mount Noshaq seen from the base camp (photo Louis Meunier).jpg": "Louis Meunier",
    "Teide von Nordosten (Zuschnitt 2).jpg": "Thomas Wolf, www.foto-tw.de",
    "Wonder Lake and Denali.jpg": "Denali National Park and Preserve (NPS)",
}


def fetch(url, tries=6):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            wait = int(e.headers.get("Retry-After") or 0) or 10 * (k + 1)
            print("429, sleeping", wait, flush=True)
            time.sleep(min(wait, 120))


def plain(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def licence_ok(lic):
    l = (lic or "").lower().strip()
    if not l or re.search(r"\b(nc|nd)\b", l) or "gfdl" == l:
        return False
    return l.startswith(OK_PREFIX)


def short_licence(lic):
    l = lic.strip()
    if l.lower().startswith(("public domain", "pd")):
        return "Public domain"
    return l


def load_info():
    info = {}
    for f in sorted((HERE / "raw").glob("commons_info_round*.json")):
        for k, v in json.loads(f.read_text(encoding="utf-8"))["info"].items():
            if v:
                info[k[5:]] = v
    return info


def query_info(titles):
    out = {}
    q = {"action": "query", "titles": "|".join("File:" + t for t in titles), "prop": "imageinfo",
         "iiprop": "url|extmetadata|size|mime", "iiurlwidth": "1600", "format": "json", "formatversion": "2"}
    d = json.loads(fetch("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)))
    norm = {n["to"]: n["from"] for n in d["query"].get("normalized", [])}
    for p in d["query"]["pages"]:
        ii = p["imageinfo"][0]; em = ii.get("extmetadata", {})
        out[norm.get(p["title"], p["title"])[5:]] = {
            "title": p["title"], "width": ii["width"], "height": ii["height"], "mime": ii["mime"],
            "thumburl": ii.get("thumburl"), "url": ii["url"], "descriptionurl": ii["descriptionurl"],
            "meta": {k: em.get(k, {}).get("value") for k in ["LicenseShortName", "LicenseUrl", "Artist", "Credit", "AttributionRequired"]}}
    (HERE / "raw" / "commons_info_round9_build.json").write_text(json.dumps({"candidates": {}, "info": {"File:" + k: v for k, v in out.items()}}, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def rnd(x):
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def main(download=True):
    from PIL import Image
    info = load_info()
    missing = [it["image"][0] for it in ITEMS if it["image"] and it["image"][0] not in info]
    if missing:
        info.update(query_info(missing))
    items = sorted(ITEMS, key=lambda it: (-it["value"], it["country"]))
    # standard competition ranking: ties share a rank, next rank skips (1,1,3 ...)
    ranked, prev_v, prev_r = [], None, 0
    for i, it in enumerate(items, 1):
        r = prev_r if it["value"] == prev_v else i
        prev_v, prev_r = it["value"], r
        ranked.append((r, it))
    assert len(ranked) == 50, len(ranked)
    img_dir = EP / "assets" / "img"; img_dir.mkdir(parents=True, exist_ok=True)
    data_items, assets = [], []
    for r, it in ranked:
        slug = slugify(it["name"])
        if it.get("badge"):
            slug += "_" + it["iso"].lower()  # shared summit: one file per country card
        image_rel, credit = None, None
        if it["image"]:
            title, crop = it["image"]
            m = info[title]; meta = m["meta"]
            lic = (meta.get("LicenseShortName") or "").strip()
            if not licence_ok(lic):
                raise SystemExit(f"licence not acceptable: {title} {lic}")
            author = AUTHOR_OVERRIDE.get(title) or plain(meta.get("Artist")) or plain(meta.get("Credit")) or "Unknown"
            src = m.get("thumburl") if m["width"] > 1600 and m.get("thumburl") else m["url"]
            fname = f"{r:02d}_{slug}.jpg"; path = img_dir / fname
            mods = []
            if download or not path.exists():
                raw = fetch(src)
                im = Image.open(io.BytesIO(raw))
                im = im.convert("RGB")
                if crop:
                    w, h = im.size
                    im = im.crop((round(crop[0] * w), round(crop[1] * h), round(crop[2] * w), round(crop[3] * h)))
                im.save(path, "JPEG", quality=90, optimize=True)
                time.sleep(1)
            saved_w, saved_h = Image.open(path).size
            if crop:
                pass
            elif saved_w < m["width"]:
                mods.append(f"resized to {saved_w}x{saved_h} (Commons thumbnail, requested 1600 px)")
            if crop:
                mods.append(f"cropped to remove caption overlays ({saved_w}x{saved_h})")
            mods.append("re-encoded as JPEG")
            sha = hashlib.sha256(path.read_bytes()).hexdigest()
            short = short_licence(lic)
            credit = "Public domain" if short == "Public domain" else f"{author} / {short}"
            image_rel = f"assets/img/{fname}"
            assets.append({
                "file": image_rel,
                "commons_page": m["descriptionurl"],
                "source_url": src,
                "author": author,
                "licence": short,
                "licence_url": meta.get("LicenseUrl") or "",
                "attribution_required": str(meta.get("AttributionRequired") or "").lower() == "true",
                "modified": "; ".join(mods),
                "sha256": sha,
                "retrieved_at": RETRIEVED,
                "fop_note": "",
            })
        cc = dict(it["cross"])
        cc["diff_pct"] = round(abs(it["value"] - cc["value"]) / it["value"] * 100, 2)
        v = it["value"]
        data_items.append({
            "rank": r,
            "name": it["name"],
            "subtitle": it["subtitle"],
            "country_iso2": it["iso"],
            "country_name": it["country"],
            "continent": it["continent"],
            "value": v,
            "value_display": f"{rnd(v):,} m",
            "secondary_display": f"{rnd(v * 3.28084):,} ft",
            **({"badge": it["badge"]} if it.get("badge") else {}),
            "tags": it["tags"],
            "image": image_rel,
            "image_credit": credit,
            "source": {**it["source"], "retrieved_at": RETRIEVED},
            "cross_check": cc,
            "notes": it["notes"],
            "wikidata": it["qid"],
        })
    data = {
        "episode": "ep02_highest_peak_by_country",
        "title": "Highest Mountain in Every Country",
        "kicker": "TOP 50",
        "metric_label": "Elevation",
        "unit": "m",
        "period_label": "Data as of Nov 2026",
        "source_line": "Sources: Wikidata (CC0), national surveys, Wikipedia",
        "theme": "alpine",
        "tally": {"by": "continent", "title": "Peaks by continent"},
        "items": data_items,
        "insights": INSIGHTS,
    }
    (EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"items={len(data_items)} images={len(assets)}")


if __name__ == "__main__":
    main(download="--no-download" not in sys.argv)
