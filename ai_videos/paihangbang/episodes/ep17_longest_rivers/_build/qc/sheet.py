import json, sys
from PIL import Image, ImageDraw, ImageFont
ep = sys.argv[1]
d = json.load(open(f'{ep}/data.json', encoding='utf-8'))
entries = []
for it in d['items']:
    if it.get('image_alt'):
        entries.append((f"{it['rank']} {it['name']} [DEF alt]", it['image_alt']))
        entries.append((f"{it['rank']} {it['name']} [RISK]", it['image']))
    else:
        entries.append((f"{it['rank']} {it['name']}", it['image']))
W, H = 480, 320
try: font = ImageFont.truetype('arial.ttf', 18)
except: font = ImageFont.load_default()
def sheet(ents, out):
    cols = 4; rows = (len(ents)+cols-1)//cols
    S = Image.new('RGB', (cols*W, rows*(H+26)), 'white'); dr = ImageDraw.Draw(S)
    for i,(lab,p) in enumerate(ents):
        im = Image.open(f'{ep}/{p}').convert('RGB'); sz = im.size
        im.thumbnail((W,H)); x=(i%cols)*W; y=(i//cols)*(H+26)
        S.paste(im,(x+(W-im.width)//2,y+26)); dr.text((x+4,y+3),f'{lab} {sz[0]}x{sz[1]}',fill='black',font=font)
    S.save(out, quality=85)
half = len(entries)//3+1
for k in range(3):
    sheet(entries[k*half:(k+1)*half], f'{ep}/_build/qc/sheet_{k+1}.jpg')
print(len(entries))
