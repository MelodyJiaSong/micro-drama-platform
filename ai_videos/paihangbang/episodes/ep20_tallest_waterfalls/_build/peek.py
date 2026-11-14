# python -I peek.py idx c1 c2 ... → reselect/peek.jpg（选定候选放大并排，便于认图）
import json,sys
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
d=json.load(open('../data.json',encoding='utf-8'))
args=sys.argv[1:]; tiles=[]
cur=None
for a in args:
    if a.isdigit(): cur=int(a); continue
    it=d['items'][cur]; p=Path('reselect/cand')/f"{cur:02d}_{Path(it['image']).stem}"
    tiles.append((f"{cur}:{a}", p/f"{a}.jpg" if (p/f"{a}.jpg").exists() else p/f"{a}"))
H=560
ims=[]
for lab,f in tiles:
    im=ImageOps.exif_transpose(Image.open(f)).convert('RGB'); w=int(im.width*H/im.height); ims.append((lab,im.resize((w,H))))
W=sum(i.width for _,i in ims)+10*len(ims)
sheet=Image.new('RGB',(W,H+30),(20,20,20)); x=0; dr=ImageDraw.Draw(sheet); f=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc',18)
for lab,im in ims:
    sheet.paste(im,(x,30)); dr.text((x+4,4),lab,font=f,fill=(255,255,255)); x+=im.width+10
if sheet.width>2400: sheet=sheet.resize((2400,int(sheet.height*2400/sheet.width)))
sheet.save('reselect/peek.jpg',quality=88)
