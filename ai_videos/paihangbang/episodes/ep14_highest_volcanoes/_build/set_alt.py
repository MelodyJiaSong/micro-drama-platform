# 复核小修：把 Flickr CC 地面实拍（_build/flickr_r2/）设为某项默认版的 image_alt（可商用、需署名）
import hashlib, json, sys
from datetime import date
from pathlib import Path
from PIL import Image, ImageOps
EP = Path(__file__).resolve().parents[1]
name, key, fid = sys.argv[1], sys.argv[2], sys.argv[3]
focus = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
d = json.loads((EP / "data.json").read_text(encoding="utf-8")); assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
it = next(i for i in d["items"] if i["name"] == name)
m = next(x for x in json.loads((EP / "_build/flickr_r2" / key / "meta.json").read_text(encoding="utf-8")) if x["id"] == fid)
stem = Path(it["image"]).stem.replace("_gen", "").replace("_nasa", "")
rel = f"assets/img/{stem}_flickr.jpg"
with Image.open(EP / "_build/flickr_r2" / key / m["file"]) as im:
    im = ImageOps.exif_transpose(im).convert("RGB"); im.thumbnail((2400, 2400), Image.LANCZOS); im.save(EP / rel, quality=92); size = im.size
lic = m["licence"]; kind = "by-sa" if "SA" in lic else "by"; ver = lic.split()[-1]
assets = [a for a in assets if a["file"] != rel] + [{"file": rel, "source_page": m["page_url"], "source_url": m["image_url"], "author": m["author"],
    "licence": lic, "licence_url": f"https://creativecommons.org/licenses/{kind}/{ver}/", "attribution_required": True,
    "modified": f"resized to {size[0]}x{size[1]} px; renderer crops; no other changes", "sha256": hashlib.sha256((EP / rel).read_bytes()).hexdigest(),
    "retrieved_at": date.today().isoformat(), "fop_note": "", "selected_by": "复核小修：Flickr CC 地面实拍（单线程 3 s 间隔检索），Claude 看图认对"}]
credit = f"{m['author']} / {lic}"
if it.get("image_risk"):
    it["image_alt"], it["image_alt_credit"] = rel, credit
    if focus: it["image_focus"] = focus
    else: it.pop("image_focus", None)
else:
    it["image"], it["image_credit"] = rel, credit
    if focus: it["image_focus"] = focus
    else: it.pop("image_focus", None)
used = {i.get("image") for i in d["items"]} | {i.get("image_alt") for i in d["items"]}
assets = [a for a in assets if a["file"] in used]
(EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("set", name, rel, size, credit)
