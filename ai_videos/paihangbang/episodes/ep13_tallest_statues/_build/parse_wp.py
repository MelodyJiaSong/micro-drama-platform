import re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
t = open("raw/wp_list_tallest_statues.wikitext", encoding="utf-8").read()
secs = re.split(r"\n==\s*([^=]+?)\s*==\n", t)
out = []
for k in range(1, len(secs), 2):
    sec, body = secs[k], secs[k+1]
    for row in body.split("\n|-")[1:]:
        cells = [c.strip() for c in re.split(r"\n\s*\|(?!\})", "\n" + row.strip("\n")) if c.strip()]
        def clean(c):
            c = re.sub(r"<ref[^>]*/>", "", c); c = re.sub(r"<ref.*?</ref>", "", c, flags=re.S)
            c = re.sub(r"\{\{cvt\|([\d.,]+)\|m[^}]*\}\}", r"\1 m", c)
            c = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", c)
            c = re.sub(r"\{\{[^}]*\}\}", "", c)
            return re.sub(r"\s+", " ", c).strip()
        cells = [clean(c) for c in cells]
        out.append({"section": sec, "cells": cells})
json.dump(out, open("raw/wp_rows.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in out:
    c = r["cells"]
    print(r["section"][:12], "|", " | ".join(x[:60] for x in c[1:8]))
