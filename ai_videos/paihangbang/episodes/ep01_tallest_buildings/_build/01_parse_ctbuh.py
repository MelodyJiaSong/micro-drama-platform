"""Parse the CTBUH Skyscraper Center '100 Tallest Completed Buildings' HTML (saved as data, never executed).

Usage: python -I 01_parse_ctbuh.py <raw/ctbuh_buildings.html> <out ctbuh_top100.json>
"""
import html
import json
import re
import sys
from html.parser import HTMLParser


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.in_table = False
        self.rows = []
        self.row = None
        self.cell = None
        self.href = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table" and a.get("id") == "buildingsTable":
            self.in_table = True
        if not self.in_table:
            return
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.row = []
        elif tag == "td" and self.row is not None:
            self.cell = {"order": a.get("data-order"), "text": "", "href": None,
                         "content": a.get("data-content")}
        elif tag == "a" and self.cell is not None and self.cell["href"] is None:
            self.cell["href"] = a.get("href")

    def handle_endtag(self, tag):
        if not self.in_table:
            return
        if tag == "td" and self.cell is not None:
            self.cell["text"] = re.sub(r"\s+", " ", self.cell["text"]).strip()
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"] += data


def main(src, dst):
    with open(src, encoding="utf-8") as f:
        raw = f.read()
    p = TableParser()
    p.feed(raw)
    out = []
    for r in p.rows:
        if len(r) < 9:
            continue
        out.append({
            "ctbuh_rank": int(r[0]["text"]),
            "name": html.unescape(r[1]["order"] or r[1]["text"]),
            "ctbuh_path": r[1]["href"],
            "city": html.unescape(r[2]["order"] or r[2]["text"]),
            "status": r[3]["order"],
            "year": int(r[4]["order"]) if r[4]["order"] else None,
            "height_m": float(r[5]["order"]),
            "height_text": html.unescape(r[5]["text"]),
            "floors": int(r[6]["order"]) if r[6]["order"] and r[6]["order"].isdigit() else None,
            "material": r[7]["text"],
            "function": r[8]["text"],
        })
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(len(out), "rows")
    for o in out[:60]:
        print(o["ctbuh_rank"], o["name"], "|", o["city"], o["status"], o["year"], o["height_m"], o["floors"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
