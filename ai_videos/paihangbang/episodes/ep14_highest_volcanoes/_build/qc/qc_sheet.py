import json, sys, os
from PIL import Image, ImageDraw, ImageFont
ep = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(os.path.join(ep,'data.json'),encoding='utf-8'))['items']
out = os.path.join(ep,'_build','qc')
try: font = ImageFont.truetype('arial.ttf', 26)
except: font = ImageFont.load_default()
def sheet(entries, name, cols, cw, ch):
    rows=(len(entries)+cols-1)//cols
    S=Image.new('RGB',(cols*cw, rows*(ch+40)),'black'); dr=ImageDraw.Draw(S)
    for i,(lab,f) in enumerate(entries):
        im=Image.open(os.path.join(ep,f)).convert('RGB'); im.thumbnail((cw,ch))
        x=(i%cols)*cw; y=(i//cols)*(ch+40)
        S.paste(im,(x+(cw-im.width)//2,y+40)); dr.text((x+6,y+6),lab,fill='yellow',font=font)
    S.save(os.path.join(out,name),quality=88)
real=[(f"#{it['rank']} {it['name']}",it['image']) for it in d if not it['image'].endswith('_gen.png')]
gen=[]
for it in d:
    if it['image'].endswith('_gen.png'): gen.append((f"#{it['rank']} {it['name']} (AI only)",it['image']))
    elif it.get('image_alt'): gen.append((f"#{it['rank']} {it['name']} alt",it['image_alt']))
for k in range(0,len(real),6): sheet(real[k:k+6],f'real_{k//6+1}.jpg',3,800,560)
for k in range(0,len(gen),8): sheet(gen[k:k+8],f'gen_{k//8+1}.jpg',4,500,560)
print(len(real),len(gen))
