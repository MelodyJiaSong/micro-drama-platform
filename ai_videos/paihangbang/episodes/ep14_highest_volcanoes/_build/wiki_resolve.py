# 用 Wikipedia 搜索 API 为 GVP Holocene 前 50 找条目名（维基只作文字与核对来源）
import json, urllib.request, urllib.parse, time, sys
UA = {"User-Agent": "paihangbang-ep14/1.0 (research; python-urllib)"}
d = json.load(open("raw/gvp_holocene.json", encoding="utf-8"))
rows = sorted([x["properties"] for x in d["features"]], key=lambda p: -(p.get("Elevation") or -1e9))[:52]
out = []
for p in rows:
    q = p["Volcano_Name"]
    if ", " in q:
        a, b = q.split(", ", 1); q = f"{b} {a}"
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": f"{q} volcano {p['Country'].split('-')[0]}", "srlimit": 3, "format": "json"})
    r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA)))
    hits = [h["title"] for h in r["query"]["search"]]
    out.append({"vn": p["Volcano_Number"], "gvp_name": p["Volcano_Name"], "query": q, "hits": hits})
    print(p["Volcano_Number"], p["Volcano_Name"], "->", hits, flush=True)
    time.sleep(0.3)
json.dump(out, open("raw/wiki_hits.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
