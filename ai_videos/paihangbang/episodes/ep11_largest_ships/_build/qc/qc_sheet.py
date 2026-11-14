import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
files = sorted(glob.glob('assets/img/*'))
out = '_build/qc'
W, H = 900, 560
per = 6
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 26)
for s in range(0, len(files), per):
    chunk = files[s:s+per]
    sheet = Image.new('RGB', (W*2, (H+40)*3), 'white')
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        im = Image.open(f).convert('RGB'); im.thumbnail((W, H))
        x = (i % 2) * W; y = (i // 2) * (H+40)
        sheet.paste(im, (x + (W-im.width)//2, y+40))
        d.text((x+8, y+6), os.path.basename(f), fill='black', font=font)
    sheet.save(f'{out}/img_sheet_{s//per+1:02d}.jpg', quality=85)
print('ok')
