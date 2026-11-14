# -*- coding: utf-8 -*-
"""CDC PHIL 候选升级：*_lores.jpg（约 700 px）→ 同号原始 TIFF，转 JPEG（长边 ≤ 4000）作新候选 h<id>（follow-up 024：Claude 自己找图下载）。"""
import json, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
CAND = Path(__file__).resolve().parent / "reselect" / "cand"
UA = {"User-Agent": "Mozilla/5.0 (paihangbang ep05 image fetch)"}

def job(d: Path):
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    have = {m["id"] for m in meta}
    seen, out = set(), []
    for m in list(meta):
        g = re.search(r"PHIL_Images/(\d+)/\1_lores\.jpg", m.get("image_url", ""))
        if not g or g.group(1) in seen or f"h{g.group(1)}" in have:
            continue
        pid = g.group(1); seen.add(pid)
        url = f"https://wwwn.cdc.gov/phil/PHIL_Images/{pid}/{pid}.tif"
        try:
            blob = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()
            im = Image.open(BytesIO(blob)).convert("RGB")
            if max(im.size) > 4000:
                im.thumbnail((4000, 4000), Image.LANCZOS)
            f = d / f"h{pid}.jpg"; im.save(f, quality=92)
            meta.append({**{k: m[k] for k in ("page_url", "source", "author", "licence", "why") if k in m},
                         "image_url": url, "id": f"h{pid}", "file": f.name, "w": im.size[0], "h": im.size[1],
                         "note": "CDC PHIL original TIFF (same image as lores candidate), converted to JPEG"})
            out.append(f"h{pid} {im.size}")
        except Exception as e:  # noqa: BLE001
            out.append(f"{pid} FAIL {e}")
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return d.name, out

with ThreadPoolExecutor(4) as ex:
    for name, out in ex.map(job, sorted(p for p in CAND.iterdir() if (p / "meta.json").exists())):
        if out: print(name, out, flush=True)
