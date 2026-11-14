import json, os, sys
from PIL import Image, ImageDraw, ImageFont
ep = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out = os.path.join(ep, '_build', 'qc')
d = json.load(open(os.path.join(ep, 'data.json'), encoding='utf-8'))
entries = []
for it in d['items']:
    entries.append((f"#{it['rank']} {it['name']} [main]{' RISK' if it.get('image_risk') else ''}", it['image']))
    if it.get('image_alt') and it['image_alt'] != it['image']:
        entries.append((f"#{it['rank']} {it['name']} [alt]", it['image_alt']))
font = ImageFont.truetype('arial.ttf', 18)
TW, TH = 420, 560
per = 8
for s in range(0, len(entries), per):
    chunk = entries[s:s+per]
    sheet = Image.new('RGB', (TW*4, (TH+48)*2), 'white')
    dr = ImageDraw.Draw(sheet)
    for i, (lab, f) in enumerate(chunk):
        im = Image.open(os.path.join(ep, f)).convert('RGB')
        w, h = im.size
        im.thumbnail((TW, TH))
        x, y = (i % 4)*TW, (i//4)*(TH+48)
        sheet.paste(im, (x + (TW-im.size[0])//2, y))
        dr.text((x+4, y+TH+2), lab[:44], fill='black', font=font)
        dr.text((x+4, y+TH+24), f"{os.path.basename(f)} {w}x{h}", fill='blue', font=font)
    sheet.save(os.path.join(out, f'contact_{s//per+1}.jpg'), quality=88)
print(len(entries))
