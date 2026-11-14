"""QC: 把抽帧按时间排序拼成 2x2 拼图（960x540 每格），左上角标时间。"""
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
pre, out = sys.argv[1], sys.argv[2]
fs = sorted(glob.glob(f'_build/qc/frames/{pre}_t*.png'))
font = ImageFont.truetype('arial.ttf', 28)
for p in range(0, len(fs), 4):
    s = Image.new('RGB', (1920, 1080)); d = ImageDraw.Draw(s)
    for i, f in enumerate(fs[p:p+4]):
        x, y = (i % 2) * 960, (i // 2) * 540
        s.paste(Image.open(f).convert('RGB').resize((960, 540)), (x, y))
        d.rectangle([x, y, x+160, y+36], fill='black'); d.text((x+6, y+2), os.path.basename(f)[len(pre)+2:-4], fill='yellow', font=font)
    s.save(f'_build/qc/{out}_{p//4+1:02d}.jpg', quality=88)
print(len(fs))
