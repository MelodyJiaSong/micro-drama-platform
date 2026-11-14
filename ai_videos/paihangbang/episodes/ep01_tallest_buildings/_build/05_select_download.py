"""Select one Commons image per building, download a 1600 px thumbnail, re-encode JPEG, write ledger.

Usage: python -I 05_select_download.py <build_dir> <episode_dir> [overrides.json]
Reads candidates.json, ctbuh_top100.json, entities.json; optional overrides {ctbuh_name: "File name.jpg" | null}.
Writes images.json (build_dir), assets.json + assets/img/NN_<slug>.jpg (episode_dir).
Downloaded bytes go to <build_dir>/dl/ (untrusted data; only decoded by Pillow, never executed).

Selection policy (see sources.md):
 1. candidate must have passed screening (licence whitelist, no deletion/copyvio tags, size, not panorama);
 2. skip files carrying a {{NoFoP-...}} template (task rule: NoFoP-tagged = problem);
 3. first remaining candidate in order P18 -> Wikipedia list -> enwiki lead -> Commons search, unless overridden;
 4. Petronas Tower 2 avoids reusing the Tower 1 file.
"""
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

from PIL import Image

UA = "paihangbang-research/0.1 (ranking-video image licensing check; python-urllib)"
RETRIEVED = "2026-11-03"
COUNTRY_FOP = {  # Commons:Freedom of panorama/table, 'Buildings' column, fetched 2026-11-03
    "CN": ("OK", "China: FoP for buildings OK (commercial)."),
    "HK": ("OK", "Hong Kong: FoP for buildings OK (commercial)."),
    "MY": ("OK", "Malaysia: FoP for buildings OK (commercial)."),
    "SA": ("OK", "Saudi Arabia: FoP for buildings OK (Commons table)."),
    "US": ("OK", "United States: architecture photos are free (17 USC 120(a))."),
    "TW": ("OK", "Taiwan: FoP for buildings OK (commercial)."),
    "RU": ("OK", "Russia: FoP for buildings OK (Commons table)."),
    "AE": ("NO", "UAE: no usable FoP for commercial use (Decree-Law 38/2021 art. 22.7 only covers presenting works in broadcasting programs)."),
    "KR": ("NO", "South Korea: FoP non-commercial only (Copyright Act art. 35(2))."),
    "KW": ("NO", "Kuwait: no FoP (Law 75/2019)."),
    "EG": ("NO", "Egypt: no FoP (Law 82/2002 art. 171, personal use only)."),
    "VN": ("NO", "Vietnam: FoP non-commercial only since 2023-01-01 (Law 07/2022); pre-2023 Commons uploads still hosted."),
}


def slug(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def fetch(url):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                b = r.read()
            time.sleep(1.5)
            return b
        except urllib.error.HTTPError as e:
            wait = int(e.headers.get("Retry-After") or 0) or 20 * (attempt + 1)
            print("  retry", e.code, "wait", wait, url, file=sys.stderr, flush=True)
            time.sleep(min(wait, 660))
    raise RuntimeError("download failed " + url)


def std_url(c):
    """Standard thumbnail step (https://w.wiki/GHai): 1920 px (downscaled locally) or 1280 px; else original."""
    o = c["orig_url"].split("?")[0]
    w = c["width"] or 0
    name = o.rsplit("/", 1)[1]
    if o.lower().endswith((".tif", ".tiff")):
        return c["thumb_url"]
    for step in (1920, 1280):
        if w > step:
            return o.replace("/wikipedia/commons/", "/wikipedia/commons/thumb/") + f"/{step}px-{name}"
    return o


def credit_of(c):
    lic = c["licence"]
    if lic.lower().startswith("public domain") or lic.lower().startswith("pd"):
        return "Public domain", "Public domain"
    author = (c.get("artist") or "").strip() or "Unknown author"
    return author, lic


def main(bdir, edir, ov_path=None):
    cands = json.load(open(os.path.join(bdir, "candidates.json"), encoding="utf-8"))
    ctbuh = json.load(open(os.path.join(bdir, "ctbuh_top100.json"), encoding="utf-8"))[:50]
    ents = json.load(open(os.path.join(bdir, "entities.json"), encoding="utf-8"))
    ov = json.load(open(ov_path, encoding="utf-8")) if ov_path else {}
    os.makedirs(os.path.join(bdir, "dl"), exist_ok=True)
    os.makedirs(os.path.join(edir, "assets", "img"), exist_ok=True)
    prev = json.load(open(os.path.join(bdir, "images.json"), encoding="utf-8")) if os.path.exists(os.path.join(bdir, "images.json")) else {}
    images, ledger, used = {}, [], set()
    for c in ctbuh:
        key = c["name"]
        e = ents[key]
        iso_fop = "HK" if e["subtitle"] == "Hong Kong" else e["iso2"]
        fop_status, fop_country = COUNTRY_FOP[iso_fop]
        pool = [x for x in cands.get(key, []) if not x.get("reject")]
        skipped_nofop = [x["file"] for x in pool if any(t.lower().startswith("nofop") for t in x["fop_templates"])]
        pool = [x for x in pool if x["file"] not in skipped_nofop]
        choice = None
        if key in ov:
            if ov[key] is None:
                pool = []
            else:
                pool = [x for x in cands.get(key, []) if x["file"] == ov[key] and not x.get("reject")]
                assert pool, ("override not acceptable", key, ov[key])
        for x in pool:
            if x["file"] in used:
                continue
            choice = x
            break
        if not choice:
            images[key] = None
            print(c["ctbuh_rank"], ascii(key), "NO IMAGE; NoFoP-skipped:", len(skipped_nofop), flush=True)
            continue
        used.add(choice["file"])
        fn = f"assets/img/{c['ctbuh_rank']:02d}_{slug(e['name'])}.jpg"
        out = os.path.join(edir, fn)
        side = os.path.join(bdir, "dl", f"{c['ctbuh_rank']:02d}_{slug(e['name'])}.src.json")
        meta = json.load(open(side, encoding="utf-8")) if os.path.exists(side) else None
        if meta is None and os.path.exists(out) and key not in ov:
            # downloaded by the first (interrupted) run, deterministic first choice, thumb_url from API
            meta = {"commons_file": choice["file"], "source_url": choice["thumb_url"]}
            json.dump(meta, open(side, "w", encoding="utf-8"), ensure_ascii=False)
        if not (meta and meta["commons_file"] == choice["file"] and os.path.exists(out)):
            url = std_url(choice)
            raw = fetch(url)
            dl = os.path.join(bdir, "dl", f"{c['ctbuh_rank']:02d}_{slug(e['name'])}.bin")
            open(dl, "wb").write(raw)
            meta = {"commons_file": choice["file"], "source_url": url}
            im = Image.open(io.BytesIO(raw))
            im.load()
            im = im.convert("RGB")
            if im.width > 1600:
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(out, "JPEG", quality=90, optimize=True)
            json.dump(meta, open(side, "w", encoding="utf-8"), ensure_ascii=False)
        im = Image.open(out)
        size = im.size
        sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
        author, lic = credit_of(choice)
        tmpl = ", ".join(choice["fop_templates"]) or "none"
        fop_note = f"File page FoP templates: {tmpl}. Country: {fop_country}"
        if fop_status == "NO":
            fop_note += (" RISK: building is copyrighted architecture in a no-commercial-FoP country; Commons hosts the file"
                         " without a NoFoP tag or deletion request, but commercial (monetised) use needs human/legal sign-off.")
        if skipped_nofop:
            fop_note += f" Skipped NoFoP-tagged candidates: {'; '.join(skipped_nofop[:4])}."
        modified = f"downscaled to {size[0]}x{size[1]} px and re-encoded as JPEG; renderer will crop" if (choice["width"] or 0) > 1600 \
            else f"re-encoded as JPEG ({size[0]}x{size[1]} px); renderer will crop"
        entry = {
            "file": fn,
            "commons_page": choice["commons_page"],
            "source_url": meta["source_url"],
            "author": author,
            "licence": lic,
            "licence_url": choice.get("licence_url") or "",
            "attribution_required": bool(choice.get("attribution_required")) and lic != "Public domain",
            "modified": modified,
            "sha256": sha,
            "retrieved_at": RETRIEVED,
            "fop_note": fop_note,
        }
        ledger.append(entry)
        credit = "Public domain" if lic == "Public domain" else f"{author} / {lic}"
        images[key] = {"file": fn, "credit": credit, "commons_file": choice["file"], "via": choice["via"],
                       "orig_size": [choice["width"], choice["height"]], "saved_size": list(size),
                       "fop_country_status": fop_status}
        print(c["ctbuh_rank"], ascii(key), "->", ascii(choice["file"]), lic, ascii(author)[:40], size, choice["fop_templates"], flush=True)
        json.dump(images, open(os.path.join(bdir, "images.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(images, open(os.path.join(bdir, "images.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(ledger, open(os.path.join(edir, "assets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main(*sys.argv[1:4])
