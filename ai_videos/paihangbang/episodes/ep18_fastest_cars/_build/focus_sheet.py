import json,sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
EP=Path(__file__).resolve().parent.parent
d=json.loads((EP/'data.json').read_text(encoding='utf-8'))
F=d['layout']['focus']
rows=[]
for i,it in enumerate(d['items']):
    for k in ('image','image_alt'):
        if it.get(k): rows.append((i,it,k,it[k]))
TW=360;TH=240;cols=4
sheet=Image.new('RGB',(cols*(TW+8)+8,((len(rows)+cols-1)//cols)*(TH+26)+8),(20,20,24))
dr=ImageDraw.Draw(sheet);fnt=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
for n,(i,it,k,f) in enumerate(rows):
    im=ImageOps.exif_transpose(Image.open(EP/f)).convert('RGB'); w,h=im.size
    fx,fy=(it.get('image_focus') or F) if k=='image' else F
    s=min(w,h); x0=max(0,min(w-s,fx*w-s/2)); y0=max(0,min(h-s,fy*h-s/2))
    t=ImageOps.contain(im,(TW,TH)); sc=t.size[0]/w
    x,y=8+(n%cols)*(TW+8),8+(n//cols)*(TH+26)
    sheet.paste(t,(x,y))
    ImageDraw.Draw(sheet).rectangle([x+x0*sc,y+y0*sc,x+(x0+s)*sc,y+(y0+s)*sc],outline=(255,40,40),width=3)
    dr.text((x,y+TH+4),f"idx{i} #{it['rank']} {it['name'][:24]} {k[6:] or 'img'} {w}x{h}",font=fnt,fill=(230,230,230))
sheet.save(EP/'_build'/'focus_sheet.jpg',quality=85); print(len(rows))
