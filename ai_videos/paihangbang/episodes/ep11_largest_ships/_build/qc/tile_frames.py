import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
src = sys.argv[1]; prefix = sys.argv[2]
files = sorted(glob.glob(os.path.join(src, '*.png')))
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)
W, H = 960, 540
n = 0
for s in range(0, len(files), 4):
    sheet = Image.new('RGB', (W*2, (H+30)*2), 'white'); d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files[s:s+4]):
        im = Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS)
        x = (i % 2)*W; y = (i//2)*(H+30)
        sheet.paste(im, (x, y+30)); d.text((x+6, y+4), os.path.basename(f), fill='black', font=font)
    n += 1
    sheet.save(f'{prefix}_{n:02d}.jpg', quality=88)
print(n)
