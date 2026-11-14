import json, urllib.request, urllib.parse, re, time
UA = {"User-Agent": "paihangbang-ep14/1.0 (research for a ranking video) python-urllib"}
T = ["Llullaillaco","Pular","Guallatiri","Tutupaca","Tupungatito","Casiri","Yucamane","Corrida de Cori","El Cóndor (volcano)","Cerro El Cóndor","Peinado","Olca","Guayaques","San José (volcano)","Tipas","Popocatépetl","Pico de Orizaba","Mount Damavand","Ubinas","Misti"]
url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({"action":"query","prop":"revisions|extracts","exintro":1,"explaintext":1,"exlimit":20,"rvprop":"content","rvslots":"main","titles":"|".join(T),"redirects":1,"format":"json","formatversion":2})
for k in range(8):
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)); break
    except urllib.error.HTTPError as e:
        print("retry", e.code, flush=True); time.sleep(20 * (k + 1))
store = json.load(open("raw/wiki_extracts_2026-11-03.json", encoding="utf-8"))
for p in r["query"]["pages"]:
    if p.get("missing"): print("MISSING", p["title"]); continue
    wt = p["revisions"][0]["slots"]["main"]["content"]
    m = re.search(r"\|\s*elevation[^=\n]*=\s*(.{0,200})", wt)
    print(p["title"], "::", m.group(1) if m else None)
    store.setdefault(p["title"], {})["extract"] = p.get("extract", "")
    store[p["title"]]["elev_raw"] = m.group(1) if m else None
json.dump(store, open("raw/wiki_extracts_2026-11-03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
