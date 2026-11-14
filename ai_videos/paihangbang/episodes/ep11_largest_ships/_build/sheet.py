# 每项一张候选总览图：所有候选缩略图 + 编号 + 分辨率 + 作者/许可，供人工逐张看
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "_tools"))
from image_reselect import item_key
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 15)
fb = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 20)
out = EP / "_build" / "sheets"; out.mkdir(exist_ok=True)
only = set(sys.argv[1:])
TW, TH = 300, 300
for i, it in enumerate(data["items"]):
    if only and it["key"] not in only: continue
    d = EP / "_build" / "reselect" / "cand" / item_key(i, it)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else []
    cols = 5; rows = max(1, (len(meta) + cols - 1) // cols)
    sh = Image.new("RGB", (cols * (TW + 10) + 10, 40 + rows * (TH + 60)), (24, 24, 28))
    dr = ImageDraw.Draw(sh)
    dr.text((10, 8), f"#{it['rank']} {it['name']}  idx {i}", font=fb, fill=(255, 255, 255))
    for k, m in enumerate(meta):
        x = 10 + (k % cols) * (TW + 10); y = 40 + (k // cols) * (TH + 60)
        try:
            with Image.open(d / m["file"]) as im:
                im = ImageOps.exif_transpose(im).convert("RGB"); im.thumbnail((TW, TH))
                sh.paste(im, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
        except Exception:
            pass
        dr.text((x, y + TH + 2), f"{m['id']} {m.get('w')}x{m.get('h')} {m.get('licence','')[:14]}", font=f, fill=(220, 220, 120))
        dr.text((x, y + TH + 20), f"{m.get('author','')[:18]} | {m.get('why','')[9:40]}", font=f, fill=(190, 190, 190))
    sh.save(out / f"{it['rank']:02d}_{it['key']}.jpg", quality=85)
print("ok")
