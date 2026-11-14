# 批量取 Wikipedia 条目导言与 infobox 海拔（维基只作文字与交叉核对来源；批量请求、限速，避免 429）
import json, urllib.request, urllib.parse, time, re
UA = {"User-Agent": "paihangbang-ep14/1.0 (research for a ranking video; contact via repo) python-urllib"}
titles = json.load(open("titles.json", encoding="utf-8"))
def api(params):
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": 2})
    for k in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(10 * (k + 1))
    raise RuntimeError("429")
names = list(titles.values()); res = {}
for i in range(0, len(names), 20):
    r = api({"action": "query", "prop": "extracts|revisions", "exintro": 1, "explaintext": 1, "exlimit": 20, "rvprop": "content|ids", "rvslots": "main", "titles": "|".join(names[i:i+20]), "redirects": 1})
    norm = {x["from"]: x["to"] for x in r["query"].get("normalized", []) + r["query"].get("redirects", [])}
    for p in r["query"]["pages"]:
        wt = p.get("revisions", [{}])[0].get("slots", {}).get("main", {}).get("content", "") if p.get("revisions") else ""
        ib = {}
        for key in ("elevation_m", "elevation_ft", "elevation_ref", "location", "country", "range", "last_eruption", "listing", "prominence_m", "first_ascent"):
            m = re.search(r"\|\s*" + key + r"\s*=\s*(.*)", wt)
            if m: ib[key] = m.group(1).strip()[:300]
        res[p["title"]] = {"missing": p.get("missing", False), "revid": p.get("revisions", [{}])[0].get("revid") if p.get("revisions") else None, "extract": p.get("extract", ""), "infobox": ib}
    res.setdefault("_norm", {}).update(norm)
    time.sleep(3)
json.dump(res, open("raw/wiki_extracts_2026-11-03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for t in names:
    t2 = res["_norm"].get(t, t); t2 = res["_norm"].get(t2, t2)
    v = res.get(t2, {"missing": True})
    print(t, "->", t2, "MISSING" if v.get("missing") else v["infobox"].get("elevation_m"), "|", v.get("infobox", {}).get("last_eruption", ""))
