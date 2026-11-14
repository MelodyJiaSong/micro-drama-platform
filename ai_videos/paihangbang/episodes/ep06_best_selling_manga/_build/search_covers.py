# -*- coding: utf-8 -*-
"""ep06 漫画封面候选：Codex 联网搜（bible §4 / follow-up 009），只找链接、不生成图。

输出与 `_tools/image_reselect.py search` 同格式（`_build/reselect/codex_bNN.json`），之后照常跑
`image_reselect.py download / score / apply`。与通用 search 的区别只在提示词：要的是漫画第 1 卷
日文原版封面（或出版社官方漫画主视觉），不是实景照片；作品均为版权作品，许可照实记录。

    python ai_videos/paihangbang/episodes/ep06_best_selling_manga/_build/search_covers.py [--workers 4] [--batch 5]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "ai_videos" / "paihangbang" / "_tools"))
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
from image_reselect import SCHEMA, ep_paths, item_key  # noqa: E402
from tools.service_request import RequestLog  # noqa: E402

PROMPT = """Use web search to find the best high-resolution images of the OFFICIAL COVER ART of each Japanese manga series below, for a full-bleed portrait (3:4) card in a YouTube ranking video about the best-selling manga of all time.
For EACH series return up to {n} candidates, best first. Priority:
1. the cover of volume 1 of the ORIGINAL JAPANESE tankobon edition (flat front-cover scan, not a photo of a physical book);
2. the cover of another well-known volume of the Japanese edition, or an official English-edition volume 1 cover;
3. an official manga key visual / anniversary illustration published by the publisher or the official series site (manga art, NOT anime screenshots).
Requirements: long side >= 1000 px (bigger is better), sharp, true colours, the whole cover visible, no watermarks, no shop badges or price stickers, no collages, no fan art, no AI-generated images.
Good places: the publisher's own catalogue pages and CDNs (Shueisha s-manga.net / shueisha.co.jp, Kodansha kodansha.co.jp / kc.kodansha.co.jp, Shogakukan shogakukan.co.jp / shogakukan-comic.jp, Akita Shoten, Futabasha, Square Enix, Hakusensha), official series sites, VIZ / Kodansha USA / Yen Press, Amazon product images (m.media-amazon.com, use the largest size variant), BookWalker, Honto, Rakuten Books.
Do NOT use Wikimedia Commons / Wikipedia images (no upload.wikimedia.org).
For each candidate give a DIRECT image file URL that downloads the image itself, the page URL, the source site, the author/rights holder (e.g. "Eiichiro Oda / Shueisha"), the licence EXACTLY as stated on the page (usually "All rights reserved"; write "unknown" if none is stated), and a short reason (which volume / edition, size).
Copy each key exactly. Do not run shell commands. Return only the JSON.
{extra}
Series:
{subjects}"""


ROUND2 = """
THIS IS A SECOND, DEEPER SEARCH: an earlier search returned only 1-2 usable images per series, most of them only 1200 px tall. Now return AT LEAST 6 DIFFERENT candidates per series, each from a different URL, and aim for long side >= 1500 px:
- Amazon (amazon.co.jp / amazon.com) product images: give the m.media-amazon.com/images/I/<id>.jpg URL WITHOUT any size suffix like ._SL1500_ or ._AC_UL600_ (that returns the original, largest file);
- Kodansha dvs-cover.kodansha.co.jp, Shogakukan / Shueisha / Square Enix / Akita Shoten / Asahi / Ushio catalogue images at their largest size; BookWalker (c.bookwalker.jp) cover images; Rakuten Kobo cdn.kobo.com/book-images/<id>/1650/2200/100/False/... (largest size); VIZ / Kodansha USA / Seven Seas English covers; official anniversary key visuals and official X image posts (pbs.twimg.com ...?name=orig).
Several different volumes of the same series are welcome (volume 1 first, then the most iconic covers), as long as each one is a clean flat front cover or an official illustration."""


def subject_line(i: int, it: dict) -> str:
    ja = it.get("name_ja", "")
    extra = ", ".join(x for x in (ja, it.get("author", ""), it.get("publisher", "")) if x)
    return f"- key {item_key(i, it)}: {it['name']} ({extra})"


def run(batch: list[tuple[int, dict]], tag: str, n: int, extra: str = "") -> str:
    p = ep_paths(EP)
    out = p["build"] / f"codex_{tag}.json"
    if out.exists():
        return f"{tag} 已有，跳过"
    prompt = PROMPT.format(n=n, extra=extra, subjects="\n".join(subject_line(i, it) for i, it in batch))
    schema = p["build"] / "codex_schema.json"
    argv = [shutil.which("codex") or "codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
            "--output-schema", str(schema), "-o", str(out), "-"]
    req = {"argv": argv, "prompt": prompt, "purpose": "排行榜 ep06 漫画封面候选链接（只找链接，不生成图）", "output": str(out),
           "cost": "ChatGPT 订阅额度，未知"}
    r = RequestLog(EP).invoke("codex_cli", "web_search", req, lambda: subprocess.run(
        argv, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1500))
    return f"{tag} rc={r.returncode} {'ok' if out.exists() else 'NO OUTPUT ' + r.stderr[-300:]}"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--batch", type=int, default=5)
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--round", type=int, default=1, help="2 = 第二轮深搜（输出 codex_b2_NN.json，与第一轮合并下载）")
    ap.add_argument("--only", nargs="*", type=int, default=None, help="只搜这些 items 下标")
    a = ap.parse_args()
    p = ep_paths(EP)
    p["build"].mkdir(parents=True, exist_ok=True)
    (p["build"] / "codex_schema.json").write_text(json.dumps(SCHEMA), encoding="utf-8")
    data = json.loads(p["data"].read_text(encoding="utf-8"))
    items = [x for x in enumerate(data["items"]) if a.only is None or x[0] in a.only]
    batches = [items[k:k + a.batch] for k in range(0, len(items), a.batch)]
    with ThreadPoolExecutor(a.workers) as ex:
        pre = "" if a.round == 1 else f"{a.round}_"
        extra = "" if a.round == 1 else ROUND2
        for msg in ex.map(lambda kb: run(kb[1], f"b{pre}{kb[0]:02d}", a.n, extra), enumerate(batches)):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
