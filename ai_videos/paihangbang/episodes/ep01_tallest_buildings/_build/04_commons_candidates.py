"""Collect and screen Wikimedia Commons image candidates for each building.

Usage: python -I 04_commons_candidates.py <entities.json> <wikidata.json> <wp_tallest.json> <raw_dir> <out candidates.json>

Candidate order: Wikidata P18 -> image used in the Wikipedia list row -> enwiki article lead image -> Commons search.
For each candidate we fetch imageinfo (url, size, mime, extmetadata) and the file page wikitext + categories,
then screen: licence whitelist, no deletion / copyvio tags, FoP templates recorded.
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
import os

UA = "paihangbang-research/0.1 (ranking-video image licensing check; python-urllib)"
API = "https://commons.wikimedia.org/w/api.php"
ENWP = "https://en.wikipedia.org/w/api.php"


def get_json(base, params):
    params = dict(params, format="json", formatversion=2)
    url = base + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            time.sleep(2.0)
            return data
        except urllib.error.HTTPError as e:
            wait = int(e.headers.get("Retry-After") or 0) or 30 * (attempt + 1)
            print("retry", attempt, e.code, "wait", wait, file=sys.stderr)
            time.sleep(min(wait, 180))
        except Exception as e:  # noqa: BLE001
            print("retry", attempt, e, file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("failed " + url)


def strip_html(s):
    if s is None:
        return None
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def licence_ok(short):
    s = (short or "").strip().lower()
    if not s:
        return False, "no licence"
    if "nc" in re.split(r"[\s\-]", s) or "nd" in re.split(r"[\s\-]", s):
        return False, "NC/ND"
    if s in ("public domain", "pd", "cc0", "cc0 1.0") or s.startswith("pd-") or s.startswith("public domain"):
        return True, "PD/CC0"
    if re.match(r"^cc[ -]by(-sa)?[ -]\d(\.\d)?", s) or s in ("cc by", "cc by-sa", "cc-by", "cc-by-sa"):
        return True, "CC BY/BY-SA"
    if s.startswith("cc0"):
        return True, "CC0"
    return False, "not whitelisted: " + short


DEL_PAT = re.compile(r"\{\{\s*(delete|deletion request|copyvio|speedy|no permission|no source|no license|"
                     r"nsd|npd|nld|dw no source|db-|fair use|non-free)", re.I)
FOP_PAT = re.compile(r"\{\{\s*((?:No)?FoP[-_ ][^}|]*)", re.I)


def wp_list_images(wp_raw):
    w = json.load(open(wp_raw, encoding="utf-8"))["parse"]["wikitext"]
    start = w.find('{| class="sortable wikitable sticky-header-multi')
    end = w.find("\n|}", start)
    out = {}
    for r in re.split(r"\n\|-[^\n]*", w[start:end]):
        links = [x.split("|")[0].strip() for x in re.findall(r"\[\[([^\]]+)\]\]", r) if not x.startswith("File:")]
        imgs = re.findall(r"\[\[File:([^|\]]+)", r)
        if links and imgs:
            out[links[0]] = imgs[0].strip()
    return out


def main(ent_path, wd_path, wp_raw, raw_dir, out_path):
    ents = {k: v for k, v in json.load(open(ent_path, encoding="utf-8")).items() if not k.startswith("_")}
    wd = json.load(open(wd_path, encoding="utf-8"))
    wpimg = wp_list_images(wp_raw)
    # enwiki lead images in batches
    titles = [v["enwiki"] for v in ents.values()]
    lead = {}
    for i in range(0, len(titles), 40):
        d = get_json(ENWP, {"action": "query", "prop": "pageimages", "piprop": "name", "redirects": 1,
                            "titles": "|".join(titles[i:i + 40])})
        m = {}
        for n in d["query"].get("normalized", []) + d["query"].get("redirects", []):
            m[n["from"]] = n["to"]
        pages = {p["title"]: p.get("pageimage") for p in d["query"]["pages"]}
        for t in titles[i:i + 40]:
            tt = t
            for _ in range(3):
                tt = m.get(tt, tt)
            lead[t] = pages.get(tt)
    result = json.load(open(out_path, encoding="utf-8")) if os.path.exists(out_path) else {}
    NOFOP = {"AE", "KR", "KW", "EG", "VN"}
    for key, v in ents.items():
        if key in result:
            continue
        cands = []

        def add(fn, why):
            if not fn:
                return
            fn = urllib.parse.unquote(fn).replace("_", " ").strip()
            if fn.lower().startswith("file:"):
                fn = fn[5:]
            fn = fn[0].upper() + fn[1:]
            if fn not in [c["file"] for c in cands]:
                cands.append({"file": fn, "via": why})

        for img in wd.get(key, {}).get("image", []) or []:
            add(img.rsplit("/", 1)[-1], "wikidata P18")
        add(wpimg.get(v["enwiki"]), "wikipedia list row")
        add(lead.get(v["enwiki"]), "enwiki lead image")
        screened = []

        def screen(chunk):
            if not chunk:
                return
            ft = ["File:" + c["file"] for c in chunk]
            d = get_json(API, {"action": "query", "titles": "|".join(ft), "redirects": 1,
                               "prop": "imageinfo|revisions|categories", "iiprop": "url|extmetadata|size|mime",
                               "iiurlwidth": 1600, "rvprop": "content", "rvslots": "main", "cllimit": "max"})
            if "query" not in d:
                print("API error for", ascii(ft), ascii(str(d)[:300]), file=sys.stderr)
                if len(chunk) > 1:
                    for one in chunk:
                        screen([one])
                return
            norm = {}
            for n in d["query"].get("normalized", []) + d["query"].get("redirects", []):
                norm[n["from"]] = n["to"]
            pages = {p["title"]: p for p in d["query"]["pages"]}
            for c, t in zip(chunk, ft):
                tt = norm.get(t, t)
                tt = norm.get(tt, tt)
                p = pages.get(tt, {})
                rec = dict(c, title=tt)
                if p.get("missing") or not p.get("imageinfo"):
                    rec["reject"] = "missing on Commons (maybe local/non-free file)"
                    screened.append(rec)
                    continue
                ii = p["imageinfo"][0]
                em = ii.get("extmetadata", {})
                wt = ""
                if p.get("revisions"):
                    wt = p["revisions"][0]["slots"]["main"].get("content", "")
                cats = [x["title"] for x in p.get("categories", [])]
                lic = strip_html(em.get("LicenseShortName", {}).get("value"))
                ok, why = licence_ok(lic)
                fop = sorted(set(m.strip() for m in FOP_PAT.findall(wt)))
                fop_cats = [x for x in cats if re.search(r"FoP|FOP|panorama", x)]
                dels = DEL_PAT.findall(wt)
                del_cats = [x for x in cats if re.search(r"deletion|copyright violation|Copyvio|FOP cases", x, re.I)]
                rec.update({
                    "commons_page": ii.get("descriptionurl"),
                    "orig_url": ii.get("url"),
                    "thumb_url": ii.get("thumburl"),
                    "width": ii.get("width"), "height": ii.get("height"), "mime": ii.get("mime"),
                    "licence": lic,
                    "licence_url": strip_html(em.get("LicenseUrl", {}).get("value")),
                    "artist": strip_html(em.get("Artist", {}).get("value")),
                    "credit": strip_html(em.get("Credit", {}).get("value")),
                    "attribution_required": (em.get("AttributionRequired", {}).get("value") or "").lower() == "true",
                    "usage_terms": strip_html(em.get("UsageTerms", {}).get("value")),
                    "date": strip_html(em.get("DateTimeOriginal", {}).get("value")),
                    "description": (strip_html(em.get("ImageDescription", {}).get("value")) or "")[:200],
                    "fop_templates": fop, "fop_categories": fop_cats,
                    "deletion_tags": dels, "deletion_categories": del_cats,
                })
                reasons = []
                if not ok:
                    reasons.append("licence " + why)
                if dels or del_cats:
                    reasons.append("deletion/copyvio tag")
                if ii.get("mime") not in ("image/jpeg", "image/png", "image/webp", "image/tiff"):
                    reasons.append("mime " + str(ii.get("mime")))
                w_, h_ = ii.get("width") or 0, ii.get("height") or 0
                if min(w_, h_) < 700:
                    reasons.append("too small")
                if h_ and w_ / h_ > 2.2:
                    reasons.append("too wide (panorama)")
                if reasons:
                    rec["reject"] = "; ".join(reasons)
                screened.append(rec)

        screen(cands[:10])
        n_ok = sum(1 for x in screened if not x.get("reject"))
        if n_ok < 3 or v["iso2"] in NOFOP:
            q = f'{v["name"]} {v["subtitle"]}'
            d = get_json(API, {"action": "query", "list": "search", "srnamespace": 6, "srlimit": 8,
                               "srsearch": q + " filetype:bitmap"})
            before = len(cands)
            for s_ in d["query"]["search"]:
                add(s_["title"], "commons search: " + q)
            new = cands[before:]
            for i in range(0, len(new), 10):
                screen(new[i:i + 10])
        result[key] = screened
        acc = [s for s in screened if not s.get("reject")]
        print(ascii(key), len(screened), "cands,", len(acc), "acceptable; first:",
              ascii(acc[0]["file"]) if acc else None, acc[0].get("licence") if acc else "", acc[0].get("fop_templates") if acc else "")
        json.dump(result, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:6])
