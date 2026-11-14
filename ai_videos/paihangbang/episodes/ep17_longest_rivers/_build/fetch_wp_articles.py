# -*- coding: utf-8 -*-
"""取候选河流的 Wikipedia 纯文本（只作文字来源，写 _build/content/ 用）→ raw/wp_articles/<title>.txt"""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path
D = Path(__file__).parent / "raw" / "wp_articles"; D.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "paihangbang-research/1.0 (river list cross-check; python-urllib)"}
for t in sys.argv[1:]:
    f = D / (t.replace(" ", "_").replace("/", "_") + ".txt")
    if f.exists(): continue
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts|revisions", "rvprop": "ids", "explaintext": 1, "redirects": 1,
                                "titles": t, "format": "json", "formatversion": 2})
    for k in range(6):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers=UA), timeout=60)); break
        except Exception as e:  # noqa: BLE001  429 退避
            print("retry", t, e, flush=True); time.sleep(15 * (k + 1))
    p = d["query"]["pages"][0]
    f.write_text(f"TITLE: {p.get('title')}\nREVID: {p.get('revisions',[{}])[0].get('revid')}\n\n{p.get('extract','')}", encoding="utf-8")
    print(t, len(p.get("extract", "")), flush=True); time.sleep(2.5)
