import json,urllib.request,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps, ImageDraw, ImageFont
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130"}
src=sys.argv[1]; out=Path(sys.argv[2])
d=json.load(open(src,encoding='utf-8'))
jobs=[]
for it in d['items']:
    for k,c in enumerate(it['images']):
        jobs.append((it['key'],k,c))
def f(j):
    key,k,c=j; p=out/key; p.mkdir(parents=True,exist_ok=True); fn=p/f"r{k}.jpg"
    if not fn.exists():
        try: fn.write_bytes(urllib.request.urlopen(urllib.request.Request(c['image_url'],headers=UA),timeout=60).read())
        except Exception as e: return
list(ThreadPoolExecutor(6).map(f,jobs))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',12)
for it in d['items']:
    p=out/it['key']; TW,TH=200,200; n=len(it['images']); cols=10
    sheet=Image.new('RGB',(cols*(TW+4),((n+cols-1)//cols)*(TH+30)+4),(20,20,20)); dr=ImageDraw.Draw(sheet)
    for k,c in enumerate(it['images']):
        x=(k%cols)*(TW+4); y=(k//cols)*(TH+30)
        try:
            im=ImageOps.exif_transpose(Image.open(p/f"r{k}.jpg")).convert('RGB'); im.thumbnail((TW,TH)); sheet.paste(im,(x,y))
        except Exception: pass
        dr.text((x,y+TH+2),f"r{k} {c['author'][:14]}",font=font,fill=(255,255,255)); dr.text((x,y+TH+15),c['why'][8:38],font=font,fill=(180,180,180))
    sheet.save(out/f"sheet_{it['key']}.jpg",quality=85); print(it['key'],n)
