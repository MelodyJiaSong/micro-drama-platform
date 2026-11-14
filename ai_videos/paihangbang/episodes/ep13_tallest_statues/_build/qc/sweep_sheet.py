from PIL import Image, ImageDraw, ImageFont
import glob, os
qc = os.path.dirname(os.path.abspath(__file__))
f = ImageFont.truetype('arial.ttf', 20)
for v in ['d', 'r']:
    fs = sorted(glob.glob(os.path.join(qc, f'sweep_{v}', 's_*.jpg')))
    for s in range(0, len(fs), 6):
        sh = Image.new('RGB', (1280, 1080), 'white'); d = ImageDraw.Draw(sh)
        for i, p in enumerate(fs[s:s+6]):
            im = Image.open(p); x, y = (i % 2)*640, (i//2)*360; sh.paste(im, (x, y))
            n = int(os.path.basename(p)[2:5]); t = (n-1)*5
            d.rectangle((x, y+330, x+80, y+358), fill='yellow'); d.text((x+3, y+333), f't={t}', fill='black', font=f)
        sh.save(os.path.join(qc, f'sweep_{v}_{s//6+1:02d}.jpg'), quality=90)
