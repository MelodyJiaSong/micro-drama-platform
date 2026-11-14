import json
from PIL import Image, ImageDraw, ImageFont
d=json.load(open('data.json',encoding='utf-8'))
W,H=760,500
try: font=ImageFont.truetype('arial.ttf',22)
except: font=ImageFont.load_default()
def tile(path,label):
    t=Image.new('RGB',(W,H+34),(30,30,30))
    if path:
        im=Image.open(path).convert('RGB'); im.thumbnail((W,H))
        t.paste(im,((W-im.width)//2,34+(H-im.height)//2))
    dr=ImageDraw.Draw(t); dr.text((6,5),label,fill=(255,255,0),font=font)
    return t
items=d['items']; per=4
for s in range(0,len(items),per):
    chunk=items[s:s+per]
    sheet=Image.new('RGB',(2*W+10,len(chunk)*(H+44)),(0,0,0))
    for i,it in enumerate(chunk):
        alt=it.get('image_alt')
        left=tile(it['image'],f"#{it['rank']} {it['name']} [{it['country_iso2']}] RISK/MAIN: {it['image'].split('/')[-1][:40]}")
        right=tile(alt,f"DEFAULT alt: {alt.split('/')[-1][:50]}" if alt else "(default = same as left)")
        sheet.paste(left,(0,i*(H+44))); sheet.paste(right,(W+10,i*(H+44)))
    sheet.save(f'_build/qc/contact_{s//per+1:02d}.jpg',quality=85)
print('ok')
