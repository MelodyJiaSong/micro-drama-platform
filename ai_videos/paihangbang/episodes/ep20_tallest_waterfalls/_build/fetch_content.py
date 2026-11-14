# -*- coding: utf-8 -*-
"""follow-up 016 第一步：为每个条目把内容先抓下来落盘 _build/content/NN_<slug>.md（只用网页抓取，不调 Codex）。
来源：WWD 瀑布页（事实字段 + 描述原文，作内部调研笔记，不进成片）、Wikipedia（en / no / de）摘要。
之后由代理人工补「标志性视角 / 易混淆对象 / 最佳拍摄点」小结。"""
from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import wwd_crawl as w  # noqa: E402
from items_def import ITEMS, VALUE_OVERRIDE  # noqa: E402

WUA = {"User-Agent": "paihangbang-research/1.0 (ep20 waterfalls; python-urllib)"}


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.replace("ø", "o").replace("Ø", "O").replace("å", "a").replace("æ", "ae"))
    s = s.encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def wiki_extract(lang: str, title: str) -> tuple[str, str]:
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts|info", "inprop": "url", "explaintext": 1, "redirects": 1,
                                "titles": title, "format": "json", "formatversion": 2})
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://{lang}.wikipedia.org/w/api.php?{q}", headers=WUA), timeout=60).read())
        p = d["query"]["pages"][0]
        time.sleep(2.0)
        return p.get("extract", ""), p.get("fullurl", "")
    except Exception as e:  # noqa: BLE001 —— query API 被限流（429）时退到 REST summary（只有导语）
        try:
            u = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title.replace(" ", "_"))
            d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=WUA), timeout=60).read())
            time.sleep(1.0)
            return "(REST summary) " + d.get("extract", ""), d.get("content_urls", {}).get("desktop", {}).get("page", "")
        except Exception as e2:  # noqa: BLE001
            return f"(fetch failed: {e}; {e2})", ""


def wwd_info(slug: str) -> dict:
    fn = HERE / "raw" / "wwd" / (re.sub(r"[^\w.-]", "_", urllib.parse.unquote(slug)) + ".html")
    t = fn.read_text(encoding="utf-8", errors="replace")
    L = w.lines(t)
    stop = L.index("Location & Directions") if "Location & Directions" in L else len(L)
    paras = [l for l in L[:stop] if len(l) > 160 and "World Waterfall Database" not in l[:60]]
    coords = re.search(r"(-?\d+\.\d+),\s*(-?\d+\.\d+)", "\n".join(L[stop:stop + 10]))
    title = next((l.split(" - World Waterfall")[0] for l in L if "World Waterfall Database" in l), "")
    return {"title": " ".join(title.split()), "numbers": w.numbers(L), "paras": paras,
            "coords": coords.group(0) if coords else "", "status": next(iter(re.findall(r"statusBox ([A-Za-z]+)", t)), ""),
            "updated": next((l for l in L if l.startswith("This page was last updated")), "")}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    out = HERE / "content"
    out.mkdir(exist_ok=True)
    rows = []
    for slug, name, sub, iso, country, wiki in ITEMS:
        info = wwd_info(slug)
        m = int(re.search(r"([\d,]+) meters", info["numbers"].get("total_height", "0 meters")).group(1).replace(",", ""))
        rows.append((VALUE_OVERRIDE.get(slug, m), m, slug, name, sub, iso, country, wiki, info))
    rows.sort(key=lambda r: (-r[0], r[3]))
    summary = []
    for idx, (val, wwd_m, slug, name, sub, iso, country, wiki, info) in enumerate(rows, 1):
        fn = out / f"{idx:02d}_{slugify(name)}.md"
        parts = [f"# {idx:02d} · {name}（{country}）", "",
                 f"- WWD 页：https://www.worldwaterfalldatabase.com/waterfall/{slug}",
                 f"- WWD 名称：{info['title']}；状态 {info['status']}；{info['updated']}",
                 f"- 坐标（WWD）：{info['coords']}",
                 f"- 本期主值：{val} m（WWD total height {wwd_m} m）",
                 "- WWD 数字：" + "；".join(f"{k}={v}" for k, v in info["numbers"].items() if v), "",
                 "## WWD 描述（原文摘录，仅内部调研，不进成片）", ""] + [f"> {p}" for p in info["paras"]] + [""]
        for lang, title in wiki.items():
            ext, url = wiki_extract(lang, title)
            parts += [f"## Wikipedia（{lang}）{title}", url, "", ext[:3500], ""]
        parts += ["## 认图要点（代理小结）", "", "（待补）", ""]
        if not fn.exists() or "（待补）" in fn.read_text(encoding="utf-8"):
            fn.write_text("\n".join(parts), encoding="utf-8")
        summary.append({"idx": idx, "file": fn.name, "slug": slug, "name": name, "value": val, "wwd_m": wwd_m,
                        "flow": info["numbers"].get("flow_consistency", ""), "high_vol": info["numbers"].get("avg_high_volume", ""),
                        "drop": info["numbers"].get("tallest_drop", ""), "drops": info["numbers"].get("num_of_drops", ""),
                        "form": info["numbers"].get("form", ""), "status": info["status"], "coords": info["coords"]})
        print(fn.name, val, info["numbers"].get("flow_consistency", ""), flush=True)
    (HERE / "content" / "_index.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
