# 封面后处理：rank_scroll thumb 取前三名，#3 Mattenbach 是 AI 图但封面无标记 → 在该卡国旗下加黄色「AI IMAGE」角标（与片中标记一致）。
# 原图另存 render/thumbnail_raw.png。python -I thumb_ai_label.py（先跑 python -m rank_scroll thumb）
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).parent.parent / "render"
raw = R / "thumbnail_raw.png"
src = R / "thumbnail.png"
src.replace(raw) if not raw.exists() or src.stat().st_mtime > raw.stat().st_mtime else None
im = Image.open(raw).convert("RGB")
d = ImageDraw.Draw(im)
f = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
x, y, txt = 864, 342, "AI IMAGE"
w = d.textlength(txt, font=f)
d.rounded_rectangle([x, y, x + w + 24, y + 36], radius=18, fill=(255, 205, 40))
d.text((x + 12, y + 4), txt, font=f, fill=(20, 20, 20))
im.save(src)
print("thumbnail labelled")
