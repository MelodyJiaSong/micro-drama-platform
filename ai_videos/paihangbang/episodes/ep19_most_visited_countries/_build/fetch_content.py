# -*- coding: utf-8 -*-
"""找图第一步：为每个景点抓维基百科纯文字摘要（只作文字来源，不用图）→ content/raw/<slug>.json"""
import json, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from landmarks import LANDMARKS
UA = {"User-Agent": "paihangbang-research/1.0 (ep19 content fetch; python-urllib)"}
out = Path(__file__).parent / "content" / "raw"
out.mkdir(parents=True, exist_ok=True)
for country, (name, place, wp, note) in LANDMARKS.items():
    slug = re.sub(r"[^a-z0-9]+", "_", country.lower()).strip("_")
    f = out / f"{slug}.json"
    if f.exists():
        continue
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts|coordinates|description", "explaintext": 1, "exsectionformat": "plain",
                                "redirects": 1, "titles": wp, "format": "json", "formatversion": 2})
    try:
        for attempt in range(6):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers=UA), timeout=60))
                break
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == 5:
                    raise
                time.sleep(20 * (attempt + 1))
        p = d["query"]["pages"][0]
        text = p.get("extract", "")
        f.write_text(json.dumps({"country": country, "landmark": name, "wp_title": p.get("title"), "description": p.get("description"),
                                 "coordinates": p.get("coordinates"), "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(p.get("title", wp).replace(" ", "_")),
                                 "extract": text[:9000], "retrieved_at": "2026-11-03"}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(country, p.get("title"), len(text))
    except Exception as e:
        print("FAIL", country, wp, e)
    time.sleep(4)
