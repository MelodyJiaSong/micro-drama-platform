"""Add candidates from a building's Commons category (and an extra search) for items whose first-pass
candidates were unusable. Screening identical to 04_commons_candidates.py (functions loaded from it).

Usage: python -I 04b_category_candidates.py <build_dir> <ctbuh_name> <Commons category title> [extra search]
"""
import importlib.util
import json
import os
import sys


def main(bdir, key, cat, extra=None):
    spec = importlib.util.spec_from_file_location("c04", os.path.join(bdir, "04_commons_candidates.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    path = os.path.join(bdir, "candidates.json")
    allc = json.load(open(path, encoding="utf-8"))
    have = {x["file"] for x in allc[key]}
    titles = []
    d = m.get_json(m.API, {"action": "query", "list": "categorymembers", "cmtitle": cat, "cmtype": "file", "cmlimit": 60})
    titles += [(x["title"], "commons category: " + cat) for x in d["query"]["categorymembers"]]
    if extra and extra.startswith("file:"):
        titles += [("File:" + extra[5:], "wikipedia list row (link had &nbsp;, added manually)")]
    elif extra:
        d = m.get_json(m.API, {"action": "query", "list": "search", "srnamespace": 6, "srlimit": 15, "srsearch": extra})
        titles += [(x["title"], "commons search: " + extra) for x in d["query"]["search"]]
    new = []
    for t, why in titles:
        f = t[5:] if t.startswith("File:") else t
        if f not in have and f not in [n[0] for n in new]:
            new.append((f, why))
    added = []
    for i in range(0, len(new), 10):
        chunk = new[i:i + 10]
        d = m.get_json(m.API, {"action": "query", "titles": "|".join("File:" + f for f, _ in chunk),
                               "prop": "imageinfo|revisions|categories", "iiprop": "url|extmetadata|size|mime",
                               "iiurlwidth": 1600, "rvprop": "content", "rvslots": "main", "cllimit": "max"})
        pages = {p["title"]: p for p in d["query"]["pages"]}
        for f, why in chunk:
            p = pages.get("File:" + f, {})
            rec = {"file": f, "via": why, "title": "File:" + f}
            if not p.get("imageinfo"):
                rec["reject"] = "missing"
                added.append(rec)
                continue
            ii = p["imageinfo"][0]
            em = ii.get("extmetadata", {})
            wt = p["revisions"][0]["slots"]["main"].get("content", "") if p.get("revisions") else ""
            cats = [x["title"] for x in p.get("categories", [])]
            lic = m.strip_html(em.get("LicenseShortName", {}).get("value"))
            ok, lwhy = m.licence_ok(lic)
            rec.update({
                "commons_page": ii.get("descriptionurl"), "orig_url": ii.get("url"), "thumb_url": ii.get("thumburl"),
                "width": ii.get("width"), "height": ii.get("height"), "mime": ii.get("mime"),
                "licence": lic, "licence_url": m.strip_html(em.get("LicenseUrl", {}).get("value")),
                "artist": m.strip_html(em.get("Artist", {}).get("value")),
                "credit": m.strip_html(em.get("Credit", {}).get("value")),
                "attribution_required": (em.get("AttributionRequired", {}).get("value") or "").lower() == "true",
                "usage_terms": m.strip_html(em.get("UsageTerms", {}).get("value")),
                "date": m.strip_html(em.get("DateTimeOriginal", {}).get("value")),
                "description": (m.strip_html(em.get("ImageDescription", {}).get("value")) or "")[:200],
                "fop_templates": sorted(set(x.strip() for x in m.FOP_PAT.findall(wt))),
                "fop_categories": [x for x in cats if "FoP" in x or "FOP" in x or "panorama" in x],
                "deletion_tags": m.DEL_PAT.findall(wt),
                "deletion_categories": [x for x in cats if any(k in x.lower() for k in ("deletion", "copyright violation", "fop cases"))],
            })
            reasons = []
            if not ok:
                reasons.append("licence " + lwhy)
            if rec["deletion_tags"] or rec["deletion_categories"]:
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
            added.append(rec)
    allc[key] += added
    json.dump(allc, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, x in enumerate(allc[key]):
        if x.get("reject") or any(t.lower().startswith("nofop") for t in x.get("fop_templates", [])):
            continue
        print(i, ascii(x["file"])[:80], x["licence"], x["width"], x["height"], x["fop_templates"], ascii(x.get("date"))[:12], "|", ascii(x.get("description"))[:90])


if __name__ == "__main__":
    main(*sys.argv[1:5])
