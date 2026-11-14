import sys
from PIL import Image, ImageDraw
out = sys.argv[1]; files = sys.argv[2:]
w, h = 960, 540
cols = 2; rows = (len(files) + 1) // 2
S = Image.new("RGB", (w * cols, h * rows), "black")
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS)
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 200, 28], fill="black"); d.text((6, 6), f.split("/")[-1], fill="yellow")
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out, quality=88)
