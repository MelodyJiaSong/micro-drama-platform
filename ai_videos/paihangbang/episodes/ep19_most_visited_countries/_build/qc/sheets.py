"""QC: tile extracted frames into labelled sheets (2 cols x 3 rows, 960x540 each)."""
import pathlib, sys
from PIL import Image, ImageDraw
d = pathlib.Path(__file__).resolve().parent
frames = sorted((d / "frames").glob("t*.png"))
out = d / "sheets"; out.mkdir(exist_ok=True)
per = 6
for s in range(0, len(frames), per):
    sheet = Image.new("RGB", (1920, 1620), "black")
    dr = ImageDraw.Draw(sheet)
    for i, f in enumerate(frames[s:s + per]):
        im = Image.open(f).convert("RGB").resize((960, 540), Image.LANCZOS)
        x, y = (i % 2) * 960, (i // 2) * 540
        sheet.paste(im, (x, y))
        dr.rectangle([x, y, x + 150, y + 26], fill="black")
        dr.text((x + 6, y + 6), f.stem, fill="yellow")
    p = out / f"sheet_{s // per:02d}.jpg"
    sheet.save(p, quality=88)
    print(p.name)
