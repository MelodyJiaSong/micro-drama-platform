"""QC contact sheets of on-screen images (read-only on assets)."""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
ep = sys.argv[1]
files = sorted(glob.glob(os.path.join(ep, "assets/img/*")))
out = os.path.join(ep, "_build/qc/sheets"); os.makedirs(out, exist_ok=True)
TW, TH = 760, 520
try:
    font = ImageFont.truetype("arial.ttf", 22)
except Exception:
    font = ImageFont.load_default()
for s in range(0, len(files), 6):
    sheet = Image.new("RGB", (TW * 3, (TH + 30) * 2), "white")
    d = ImageDraw.Draw(sheet)
    for k, f in enumerate(files[s:s + 6]):
        im = Image.open(f).convert("RGB"); im.thumbnail((TW, TH))
        x, y = (k % 3) * TW, (k // 3) * (TH + 30)
        sheet.paste(im, (x + (TW - im.width) // 2, y + 30))
        d.text((x + 5, y + 4), f"{os.path.basename(f)} {Image.open(f).size}", fill="black", font=font)
    sheet.save(os.path.join(out, f"sheet_{s // 6:02d}.jpg"), quality=85)
print(len(files))
