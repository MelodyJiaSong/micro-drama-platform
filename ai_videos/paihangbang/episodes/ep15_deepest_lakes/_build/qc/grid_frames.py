"""Tile extracted QC frames 2x2 (960x540 each) with labels."""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
src = sys.argv[1]; prefix = sys.argv[2]
files = sorted(glob.glob(os.path.join(src, prefix + "*.jpg")))
os.makedirs(os.path.join(src, "grids"), exist_ok=True)
font = ImageFont.truetype("arial.ttf", 28)
for g in range(0, len(files), 4):
    sheet = Image.new("RGB", (1920, 1080), "black"); d = ImageDraw.Draw(sheet)
    for k, f in enumerate(files[g:g + 4]):
        im = Image.open(f).resize((960, 540), Image.LANCZOS)
        x, y = (k % 2) * 960, (k // 2) * 540
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 200, y + 36], fill="yellow"); d.text((x + 6, y + 3), os.path.basename(f)[:-4], fill="black", font=font)
    sheet.save(os.path.join(src, "grids", f"{prefix}grid_{g // 4:02d}.jpg"), quality=88)
