# 下载第三轮候选：python getr3.py <key> <name> <flickr页 或 图片直链> ；Flickr 页自动取 ≥1600 px 尺寸与许可，写 r3/<key>/<name>.json 元数据
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import flickr_search as fs
from claude_search import page_best
key, name, url = sys.argv[1:4]
D = Path(__file__).parent / "r3" / key; D.mkdir(parents=True, exist_ok=True)
meta = {"page_url": url, "image_url": url, "author": sys.argv[4] if len(sys.argv) > 4 else "", "licence": sys.argv[5] if len(sys.argv) > 5 else "unknown", "source": re.sub(r"^https?://(www\.)?([^/]+).*", r"\2", url)}
m = re.match(r"https://www\.flickr\.com/photos/([^/]+)/(\d+)", url)
if m:
    c = page_best({"id": m.group(2), "page_url": url, "image_url": "", "licence": "", "license": None})
    t = (D.parent.parent / "flickr" / f"p_{m.group(2)}.html").read_text(encoding="utf-8")
    au = re.search(r'"ownerNsid":"[^"]*","username":"([^"]*)"', t) or re.search(r'"realname":"([^"]+)"', t)
    meta.update(image_url=c["image_url"], licence=c.get("licence", "unknown"), source="Flickr", author=meta["author"] or (au.group(1) if au else ""))
f = D / f"{name}.jpg"
subprocess.run(["curl", "-s", "-L", "-m", "60", "-A", fs.UA["User-Agent"], "-o", str(f), meta["image_url"]])
meta["file"] = f"r3/{key}/{name}.jpg"
(D / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
from PIL import Image
print(name, Image.open(f).size, meta["licence"], meta["author"])
