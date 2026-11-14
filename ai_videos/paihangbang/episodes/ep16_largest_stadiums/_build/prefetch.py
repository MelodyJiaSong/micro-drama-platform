# -*- coding: utf-8 -*-
"""ep16：按 image_reselect download 的同一编号规则（codex_b*.json + claude_*.json 排序合并、跳过维基）预先用 curl 顺序下载候选，
避开 Python 并发时 Flickr 静态图 429。下完再跑 image_reselect download 生成 meta（已存在的文件会跳过）。

    python _build/prefetch.py [--only idx,idx] [--gap 1.5]"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
EP = B.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--gap", type=float, default=1.5)
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x}
    data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
    rs = B / "reselect"
    found: dict[str, list[dict]] = {}
    for f in sorted([*rs.glob("codex_b*.json"), *rs.glob("claude_*.json")]):
        for row in json.loads(f.read_text(encoding="utf-8")).get("items", []):
            found.setdefault(row["key"], []).extend(row["images"])
    for i, it in enumerate(data["items"]):
        if only and i not in only:
            continue
        key = f"{i:02d}_{Path(it['image']).stem}"
        d = rs / "cand" / key
        d.mkdir(parents=True, exist_ok=True)
        n = 0
        for k, c in enumerate(found.get(key, [])):
            if "wikimedia.org" in c["image_url"] or "wikipedia.org" in c["image_url"]:
                continue
            f = d / f"c{k}.jpg"
            if f.exists() and f.stat().st_size > 50_000:
                n += 1
                continue
            for attempt in range(3):
                r = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, "-e", c.get("page_url") or "", "-o", str(f), "-w", "%{http_code}", c["image_url"]],
                                   capture_output=True, text=True)
                time.sleep(a.gap)
                if r.stdout.strip() == "200" and f.exists() and f.stat().st_size > 50_000:
                    n += 1
                    break
                f.unlink(missing_ok=True)
                if r.stdout.strip() != "429" or c["image_url"].endswith("_o.jpg"):
                    break                                   # Flickr 原图限流：跳过，等 fix_sizes 换成 k 链接再下
                time.sleep(10 * (attempt + 1))
        print(f"{key}: {n}/{len(found.get(key, []))}", flush=True)


if __name__ == "__main__":
    main()
