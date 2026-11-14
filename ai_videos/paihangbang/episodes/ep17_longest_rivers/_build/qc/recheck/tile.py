import sys, os
from PIL import Image, ImageDraw, ImageFont
files = sys.argv[2:]; out = sys.argv[1]
font = ImageFont.truetype('arial.ttf', 22)
cols = 2; rows = (len(files) + 1) // 2
S = Image.new('RGB', (cols * 960, rows * 570), 'white'); d = ImageDraw.Draw(S)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB').resize((960, 540), Image.LANCZOS); x = (i % 2) * 960; y = (i // 2) * 570
    S.paste(im, (x, y + 30)); d.text((x + 5, y + 3), os.path.basename(f), fill='black', font=font)
S.save(out, quality=90)
