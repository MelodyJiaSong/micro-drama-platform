# 审片修复：按名称把 cand 目录里的某个候选装到某项的 image（重排后 image_reselect 的 index 键对不上，故手工装）
import hashlib, json, sys
from datetime import date
from pathlib import Path
from PIL import Image, ImageOps
EP = Path(__file__).resolve().parents[1]
name, cand_dir, cid = sys.argv[1], sys.argv[2], sys.argv[3]
focus = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
d = json.loads((EP / "data.json").read_text(encoding="utf-8")); assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
it = next(i for i in d["items"] if i["name"] == name)
m = next(x for x in json.loads((EP / "_build/reselect/cand" / cand_dir / "meta.json").read_text(encoding="utf-8")) if x["id"] == cid)
rel = it["image"]; dst = EP / rel
(EP / "_build/old_img").mkdir(exist_ok=True); dst.replace(EP / "_build/old_img" / (dst.stem + "_pre_qcfix" + dst.suffix))
with Image.open(EP / "_build/reselect/cand" / cand_dir / m["file"]) as im:
    im = ImageOps.exif_transpose(im).convert("RGB"); im.thumbnail((2400, 2400), Image.LANCZOS); im.save(dst, quality=90); size = im.size
lic = m["licence"]
assets = [a for a in assets if a["file"] != rel] + [{"file": rel, "source_page": m["page_url"], "source_url": m["image_url"], "author": m["author"],
    "licence": lic, "licence_url": "https://www.pexels.com/license/" if "pexels" in lic.lower() else ("https://unsplash.com/license" if "unsplash" in lic.lower() else ""),
    "attribution_required": False, "modified": f"downscaled to {size[0]}x{size[1]} px; renderer will crop", "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
    "retrieved_at": date.today().isoformat(), "fop_note": "", "selected_by": "审片修复：Claude 看图换图"}]
it["image_credit"] = f"{m['author']} / {lic}"
if focus: it["image_focus"] = focus
else: it.pop("image_focus", None)
(EP / "data.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("installed", name, rel, size)
