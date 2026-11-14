import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
d = sys.argv[1]; tag = sys.argv[2]
fs = sorted(glob.glob(os.path.join(d, 'frames', tag + '_*.jpg')))
font = ImageFont.truetype('arial.ttf', 28)
for k in range(0, len(fs), 4):
    S = Image.new('RGB', (1920, 1080 + 0), 'black'); dr = ImageDraw.Draw(S)
    for i, f in enumerate(fs[k:k+4]):
        im = Image.open(f); im = im.resize((960, 540))
        x = (i % 2) * 960; y = (i // 2) * 540
        S.paste(im, (x, y)); dr.text((x + 8, y + 500), os.path.basename(f), fill='lime', font=font)
    S.save(os.path.join(d, f'tile_{tag}_{k//4+1:02d}.jpg'), quality=90)
print(len(fs))
