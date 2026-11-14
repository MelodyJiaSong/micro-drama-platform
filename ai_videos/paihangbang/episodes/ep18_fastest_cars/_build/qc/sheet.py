import sys, os
from PIL import Image, ImageDraw, ImageFont
ep = sys.argv[1]; out = sys.argv[2]; files = sys.argv[3:]
W,H=640,420
cols=3
rows=(len(files)+cols-1)//cols
sheet=Image.new('RGB',(W*cols,(H+30)*rows),'white')
d=ImageDraw.Draw(sheet)
try: f=ImageFont.truetype('arial.ttf',20)
except: f=None
for i,fn in enumerate(files):
    im=Image.open(os.path.join(ep,fn)); sz=im.size; im=im.convert('RGB'); im.thumbnail((W,H))
    x=(i%cols)*W; y=(i//cols)*(H+30)
    sheet.paste(im,(x,y+30))
    d.text((x+4,y+4),f"{os.path.basename(fn)} {sz[0]}x{sz[1]}",fill='black',font=f)
sheet.save(out,quality=88)
