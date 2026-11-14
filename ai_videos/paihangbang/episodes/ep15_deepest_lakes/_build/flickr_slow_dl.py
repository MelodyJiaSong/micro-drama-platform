# -*- coding: utf-8 -*-
"""Flickr 静态图被 429 限流时慢速补下：按 image_reselect.py download 的同一编号规则（claude_*.json 与 codex_b*.json 排序合并、跳过维基）
把 Flickr 候选预先下载到 cand/<key>/c<k>.jpg，之后再跑共用 download 即会跳过已存在文件并写 meta。"""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EP = Path(__file__).resolve().parents[1]
B = EP / "_build" / "reselect"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
found: dict[str, list] = {}
for f in [*sorted(B.glob("codex_b*.json")), *sorted(B.glob("claude_*.json"))]:  # 与共用 download 同序（先 codex_b 再 claude_）
    for row in json.loads(f.read_text(encoding="utf-8")).get("items", []):
        found.setdefault(row["key"], []).extend(row["images"])
todo = []
for key, imgs in found.items():
    for k, c in enumerate(imgs):
        if "wikimedia.org" in c["image_url"] or "wikipedia.org" in c["image_url"]:
            continue
        if "staticflickr" in c["image_url"]:
            dst = B / "cand" / key / f"c{k}.jpg"
            if not dst.exists():
                todo.append((dst, c["image_url"]))
PRIO = ["04_05", "07_08", "12_13", "02_03", "13_14", "20_21", "21_22", "22_22", "23_24", "27_28", "10_11", "03_04", "32_33"]
todo.sort(key=lambda t: next((n for n, p in enumerate(PRIO) if t[0].parent.name.startswith(p)), 99))
print("todo", len(todo), flush=True)
wait = 3
def curl_get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "120", "-A", UA["User-Agent"], "-w", "\n%{http_code}", url], capture_output=True)
    body, _, code = r.stdout.rpartition(b"\n")
    return int(code or 0), body
for dst, url in todo:
    for attempt in range(5):
        code, blob = curl_get(url)
        if code == 200 and len(blob) > 50_000:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(blob)
            print("ok", dst.parent.name, dst.name, len(blob), flush=True)
            break
        if code == 429:
            print("429 backoff", 60 * (attempt + 1), flush=True)
            time.sleep(60 * (attempt + 1))
            continue
        print("fail", code, dst.parent.name, url, flush=True)
        break
    time.sleep(wait)
print("done", flush=True)
