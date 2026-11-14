# 试裁：python trycrop.py out.jpg "label|path|x0,y0,x1,y1|fx,fy" ...  模拟卡片（800x850，文字区从 62% 起）
import sys
from PIL import Image, ImageDraw, ImageOps
out = sys.argv[1]; specs = sys.argv[2:]
W, H = 300, 319; cols = 4
rows = (len(specs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (W + 6), rows * (H + 22)), (20, 20, 24)); dr = ImageDraw.Draw(sheet)
for k, sp in enumerate(specs):
    lab, path, pc, fc = (sp.split("|") + ["", ""])[:4]
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if pc:
        x0, y0, x1, y1 = map(float, pc.split(",")); w, h = im.size
        im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    fx, fy = map(float, fc.split(",")) if fc else (0.5, 0.5)
    w, h = im.size; a = W / H
    if w / h > a:
        cw = h * a; left = max(0, min(w - cw, fx * w - cw / 2)); im = im.crop((int(left), 0, int(left + cw), h))
    else:
        ch = w / a; top = max(0, min(h - ch, fy * h - ch / 2)); im = im.crop((0, int(top), w, int(top + ch)))
    im = im.resize((W, H))
    ov = Image.new("L", (W, H), 0); od = ImageDraw.Draw(ov)
    for yy in range(int(H * 0.5), H): od.line([(0, yy), (W, yy)], fill=int(215 * min(1, (yy - H * 0.5) / (H * 0.3))))
    im = Image.composite(Image.new("RGB", (W, H), (6, 24, 42)), im, ov)
    x = (k % cols) * (W + 6); y = (k // cols) * (H + 22)
    sheet.paste(im, (x, y)); dr.text((x + 4, y + H + 4), lab, fill=(255, 220, 120))
sheet.save(out, quality=88); print("ok")
