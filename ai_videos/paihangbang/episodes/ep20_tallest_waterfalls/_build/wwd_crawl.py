# -*- coding: utf-8 -*-
"""ep20 调研：抓 World Waterfall Database「Overall Height」榜前 N 页 + 每条瀑布页的事实字段。
只取事实数值（高度、落差数、流量稳定性、坐标、形态），不搬运文字与照片（WWD 法律页：照片受版权保护）。
1.2 s/请求，描述性 UA；原始 HTML 存 raw/wwd/，结果 raw/wwd_top.json。"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

RAW = Path(__file__).parent / "raw"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130 (paihangbang research; 1 req/s)"}
BASE = "https://www.worldwaterfalldatabase.com/"


def fetch(url: str, path: Path) -> str:
    if path.exists() and path.stat().st_size > 5000:
        return path.read_text(encoding="utf-8", errors="replace")
    for k in range(3):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            path.write_bytes(b)
            time.sleep(1.2)
            return b.decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            print("retry", url, e, flush=True)
            time.sleep(5 * (k + 1))
    return ""


def lines(t: str) -> list[str]:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    x = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return [l.strip() for l in x.split("\n") if l.strip()]


def after(L: list[str], label: str, n: int = 2) -> str:
    for i, l in enumerate(L):
        if l == label:
            return " ".join(L[i + 1:i + 1 + n])
    return ""


LABELS = ["Total Height", "Tallest Drop", "Num of Drops", "Avg. Width", "Max. Width", "Pitch", "Run", "Form", "Watershed",
          "Stream", "Avg.  Estm.  Volume", "Avg.  High  Volume", "Avg. Low Volume", "Source", "Flow Consistency", "Best Flow"]


def numbers(L: list[str]) -> dict:
    try:
        i = L.index("By The Numbers")
    except ValueError:
        return {}
    out, cur = {}, None
    for l in L[i + 1:]:
        if l.startswith("This page was last updated"):
            break
        if l in LABELS:
            cur = l
            out[cur] = []
        elif cur:
            out[cur].append(l)
    return {k.lower().replace(".", "").replace("  ", " ").replace(" ", "_"): " ".join(v) for k, v in out.items()}


def main(pages: int) -> None:
    (RAW / "wwd").mkdir(parents=True, exist_ok=True)
    rows = []
    for p in range(1, pages + 1):
        url = BASE + "tallest-waterfalls/total-height" + (f"?page={p}" if p > 1 else "")
        t = fetch(url, RAW / f"wwd_total_height_p{p}.html")
        links = []
        for m in re.finditer(r'href="https://www\.worldwaterfalldatabase\.com/waterfall/([^"]+)"', t):
            if m.group(1) not in links:
                links.append(m.group(1))
        for slug in links:
            rows.append({"list_page": p, "slug": slug})
    out = []
    for k, r in enumerate(rows, 1):
        slug = r["slug"]
        fn = RAW / "wwd" / (re.sub(r"[^\w.-]", "_", urllib.parse.unquote(slug)) + ".html")
        t = fetch(BASE + "waterfall/" + urllib.parse.quote(urllib.parse.unquote(slug)), fn)
        L = lines(t)
        title = next((l.split(" - World Waterfall")[0] for l in L if "World Waterfall Database" in l), "")
        title = title.replace(" ", " ")
        rec = {"rank_wwd": k, "slug": slug, "url": BASE + "waterfall/" + slug, "title": " ".join(title.split()),
               **numbers(L),
               "status": next((m.group(1) for m in re.finditer(r'statusBox ([A-Za-z]+)', t)), ""),
               "ephemeral_text": bool(re.search(r"ephemeral|only flows (during|after)", t, re.I)),
               "updated": next((l for l in L if l.startswith("This page was last updated")), "")}
        out.append(rec)
        print(k, rec["title"], "|", rec.get("total_height"), "|", rec.get("tallest_drop"), "|", rec.get("flow_consistency"), "|", rec["status"], flush=True)
    (RAW / "wwd_top.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
