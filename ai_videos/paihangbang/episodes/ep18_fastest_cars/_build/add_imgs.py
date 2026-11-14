# 新增 / 替换单项图（不经 image_reselect，避免下标变化影响旧候选目录）
import json, hashlib, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageOps
sys.path.insert(0, str(Path(__file__).parent))
from picks_to_claude import large   # noqa  (imports PICKS too; harmless)
EP = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
LIC = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/", "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
       "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/", "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
       "CC0 1.0": "https://creativecommons.org/publicdomain/zero/1.0/"}
JOBS = [  # (data.json name, find json, cand idx, field)
    ("Koenigsegg Jesko Absolut", "11_12_koenigsegg_jesko_absolut.json", int(sys.argv[1]), "image"),
    ("Koenigsegg CCX", "15_16_koenigsegg_ccx.json", int(sys.argv[2]), "image"),
]
d = json.loads((EP / "data.json").read_text(encoding="utf-8")); A = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
for name, fj, idx, field in JOBS:
    it = next(x for x in d["items"] if x["name"] == name)
    c = json.loads((EP / "_build/find" / fj).read_text(encoding="utf-8"))["cands"][idx]
    url, w, h = large(c["page_url"], c["image_url"])
    blob = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    rel = it[field]; dst = EP / rel
    tmp = EP / "_build/find" / ("dl_" + Path(rel).name); tmp.write_bytes(blob)
    im = ImageOps.exif_transpose(Image.open(tmp)).convert("RGB"); im.thumbnail((2400, 2400)); im.save(dst, quality=90)
    A = [a for a in A if a["file"] != rel]
    A.append({"file": rel, "source_page": c["page_url"], "source_url": url, "author": c["author"], "licence": c["licence"],
              "licence_url": LIC.get(c["licence"], ""), "attribution_required": not c["licence"].startswith("CC0"),
              "modified": f"downscaled to {im.size[0]}x{im.size[1]} px and re-encoded as JPEG; renderer will crop",
              "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "retrieved_at": "2026-11-04", "fop_note": "",
              "selected_by": f"Claude, Flickr CC search, candidate {idx}: {c['title'][:60]}"})
    it["image_credit"] = f"{c['author']} / {c['licence']}"
    print(name, im.size, c["licence"], c["author"], c["title"])
(EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(EP / "assets.json").write_text(json.dumps(A, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
