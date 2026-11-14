# 第三轮：对指定项做更宽的 Flickr 搜索（多页、多关键词），拼一张缩略图总览（编号 = 列表下标），供挑整船可见的图
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).parent))
import flickr_search as fs
key = sys.argv[1]; must = sys.argv[2].lower().split("|"); queries = sys.argv[3:]
D = Path(__file__).parent / "r3" / key; D.mkdir(parents=True, exist_ok=True)
seen = {}; 
for q in queries:
    for pg in (1, 2):
        for x in fs.search(q, page=pg):
            t = (x["title"] + " " + x["description"]).lower()
            if any(m in t for m in must) and x["id"] not in seen:
                seen[x["id"]] = x
lst = list(seen.values())
(D / "list.json").write_text(json.dumps(lst, ensure_ascii=False, indent=1), encoding="utf-8")
UA = fs.UA["User-Agent"]; S = 230; cols = 8
rows = (len(lst) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (S + 4) + 4, max(1, rows) * (S + 22) + 4), (20, 20, 24)); dr = ImageDraw.Draw(sheet)
f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
for i, x in enumerate(lst):
    tp = D / f"t{i}.jpg"
    if not tp.exists():
        subprocess.run(["curl", "-s", "-m", "30", "-A", UA, "-o", str(tp), x["image_url"]])
    try:
        im = Image.open(tp).convert("RGB"); im.thumbnail((S, S))
        xx = 4 + (i % cols) * (S + 4); yy = 4 + (i // cols) * (S + 22)
        sheet.paste(im, (xx + (S - im.width) // 2, yy + (S - im.height) // 2))
        dr.text((xx, yy + S + 2), f"{i} {x['licence'][:10]} {x['author'][:14]}", font=f, fill=(230, 230, 120))
    except Exception:
        pass
sheet.save(D / "sheet.jpg", quality=85); print(len(lst))
