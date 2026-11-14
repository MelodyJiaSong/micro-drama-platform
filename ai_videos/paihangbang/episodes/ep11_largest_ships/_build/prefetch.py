# 候选图预下载（curl；image_reselect 的 urllib 下载被 Flickr 静态图拒绝）。编号与 image_reselect.download 完全一致。
import json, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools"))
from image_reselect import item_key
B = EP / "_build" / "reselect"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
found = {}
for f in sorted([*B.glob("codex_b*.json"), *B.glob("claude_*.json")]):
    for row in json.loads(f.read_text(encoding="utf-8")).get("items", []):
        found.setdefault(row["key"], []).extend(row["images"])
jobs = []
for i, it in enumerate(data["items"]):
    key = item_key(i, it); d = B / "cand" / key; d.mkdir(parents=True, exist_ok=True)
    for k, c in enumerate(found.get(key, [])):
        f = d / f"c{k}.jpg"
        if not f.exists() and "wikimedia" not in c["image_url"]:
            jobs.append((c["image_url"], f))
def dl(j):
    u, f = j
    r = subprocess.run(["curl", "-s", "-L", "-m", "60", "-A", UA, "-o", str(f), u])
    if f.exists() and f.stat().st_size < 50000: f.unlink()
with ThreadPoolExecutor(4) as ex: list(ex.map(dl, jobs))
print("prefetched", len(jobs))
