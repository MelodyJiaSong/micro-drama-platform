"""Resolve enwiki titles -> Wikidata QIDs, then pull height/floors/dates/country/image via SPARQL.

Usage: python -I 03_wikidata.py <entities.json> <raw_dir> <out wikidata.json>
Raw API responses are saved to raw_dir for audit.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

UA = "paihangbang-research/0.1 (ranking-video data research; python-urllib)"


def get(url, data=None, accept="application/json"):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main(ent_path, raw_dir, out_path):
    ents = json.load(open(ent_path, encoding="utf-8"))
    titles = [v["enwiki"] for k, v in ents.items() if not k.startswith("_")]
    qids = {}
    norm = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        q = urllib.parse.urlencode({"action": "query", "prop": "pageprops", "ppprop": "wikibase_item",
                                    "redirects": 1, "format": "json", "formatversion": 2,
                                    "titles": "|".join(chunk)})
        raw = get("https://en.wikipedia.org/w/api.php?" + q)
        open(f"{raw_dir}/wp_pageprops_{i}.json", "wb").write(raw)
        d = json.loads(raw)["query"]
        m = {}
        for n in d.get("normalized", []):
            m[n["from"]] = n["to"]
        for n in d.get("redirects", []):
            m[n["from"]] = n["to"]
        for p in d["pages"]:
            qids[p["title"]] = p.get("pageprops", {}).get("wikibase_item")
        for t in chunk:
            tt = t
            for _ in range(3):
                tt = m.get(tt, tt)
            norm[t] = tt
        time.sleep(1)
    title2qid = {t: qids.get(norm[t]) for t in titles}
    for t, q in title2qid.items():
        if not q:
            print("NO QID:", ascii(t), "->", ascii(norm[t]))
    vals = " ".join("wd:" + q for q in title2qid.values() if q)
    sparql = f"""
SELECT ?item ?itemLabel ?h ?hUnitLabel ?hRank ?floors ?inception ?start ?opened ?country ?countryLabel ?iso2 ?city ?cityLabel ?image WHERE {{
  VALUES ?item {{ {vals} }}
  OPTIONAL {{ ?item p:P2048 ?hs . ?hs psv:P2048 ?hv . ?hv wikibase:quantityAmount ?h ; wikibase:quantityUnit ?hUnit . ?hs wikibase:rank ?hRank . }}
  OPTIONAL {{ ?item wdt:P1101 ?floors . }}
  OPTIONAL {{ ?item wdt:P571 ?inception . }}
  OPTIONAL {{ ?item wdt:P580 ?start . }}
  OPTIONAL {{ ?item wdt:P1619 ?opened . }}
  OPTIONAL {{ ?item wdt:P17 ?country . OPTIONAL {{ ?country wdt:P297 ?iso2 . }} }}
  OPTIONAL {{ ?item wdt:P131 ?city . }}
  OPTIONAL {{ ?item wdt:P18 ?image . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}"""
    open(f"{raw_dir}/wikidata_query.rq", "w", encoding="utf-8").write(sparql)
    raw = get("https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": sparql, "format": "json"}),
              accept="application/sparql-results+json")
    open(f"{raw_dir}/wikidata_result.json", "wb").write(raw)
    rows = json.loads(raw)["results"]["bindings"]
    by = {}
    for r in rows:
        q = r["item"]["value"].rsplit("/", 1)[1]
        e = by.setdefault(q, {"qid": q, "label": r.get("itemLabel", {}).get("value"), "heights": [], "floors": set(),
                              "inception": set(), "start": set(), "opened": set(), "country": set(),
                              "city": set(), "image": set()})
        if "h" in r:
            e["heights"].append((float(r["h"]["value"]), r.get("hUnitLabel", {}).get("value"),
                                 r.get("hRank", {}).get("value", "").rsplit("#", 1)[-1]))
        for k, key in [("floors", "floors"), ("inception", "inception"), ("start", "start"), ("opened", "opened"),
                       ("image", "image")]:
            if k in r:
                e[key].add(r[k]["value"])
        if "country" in r:
            e["country"].add((r.get("countryLabel", {}).get("value"), r.get("iso2", {}).get("value")))
        if "city" in r:
            e["city"].add(r.get("cityLabel", {}).get("value"))
    out = {}
    for k, v in ents.items():
        if k.startswith("_"):
            continue
        q = title2qid.get(v["enwiki"])
        e = by.get(q, {}) if q else {}
        rec = {"qid": q, "enwiki_resolved": norm[v["enwiki"]]}
        for kk, vv in e.items():
            if isinstance(vv, set):
                vv = sorted(vv, key=str)
            if kk == "heights":
                vv = sorted(set(vv), key=str)
            rec[kk] = vv
        out[k] = rec
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k, r in out.items():
        print(ascii(k), r.get("qid"), r.get("heights"), r.get("floors"), r.get("inception"), r.get("opened"),
              ascii(r.get("country")), "img" if r.get("image") else "NOIMG")


if __name__ == "__main__":
    main(*sys.argv[1:4])
