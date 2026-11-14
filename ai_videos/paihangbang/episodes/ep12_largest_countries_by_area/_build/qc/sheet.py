"""QC: 把上屏图按卡比例 (720x800) 裁成缩略图拼图，每张 3x3。"""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
ep = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(os.path.join(ep, 'data.json'), encoding='utf-8'))
files = []
for it in d['items']:
    files.append((f"#{it['rank']} {it['name']} | {it['subtitle']}", it['image'], it.get('image_focus') or d['layout']['focus']))
    if it.get('image_alt'):
        files.append((f"#{it['rank']} ALT {it['name']} | {it['subtitle']}", it['image_alt'], it.get('image_focus') or d['layout']['focus']))
W, H = 540, 600
font = ImageFont.truetype('arial.ttf', 22)
out = os.path.join(ep, '_build', 'qc')
def crop(im, focus):
    iw, ih = im.size; r = W / H
    if iw / ih > r:
        nw = int(ih * r); x = int((iw - nw) * focus[0]); box = (x, 0, x + nw, ih)
    else:
        nh = int(iw / r); y = int((ih - nh) * focus[1]); box = (0, y, iw, y + nh)
    return im.crop(box).resize((W, H), Image.LANCZOS)
per = 9
for p in range(0, len(files), per):
    sheet = Image.new('RGB', (W * 3, (H + 34) * 3), 'black'); dr = ImageDraw.Draw(sheet)
    for i, (lab, f, foc) in enumerate(files[p:p + per]):
        im = Image.open(os.path.join(ep, f)).convert('RGB')
        x, y = (i % 3) * W, (i // 3) * (H + 34)
        sheet.paste(crop(im, foc), (x, y + 34))
        dr.text((x + 4, y + 4), f"{lab} {im.size[0]}x{im.size[1]}", fill='yellow', font=font)
    sheet.save(os.path.join(out, f'img_sheet_{p // per + 1:02d}.jpg'), quality=85)
print(len(files))
