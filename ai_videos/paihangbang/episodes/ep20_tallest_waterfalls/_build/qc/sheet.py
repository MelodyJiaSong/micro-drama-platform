import sys,glob,os
from PIL import Image,ImageDraw,ImageFont
files=sys.argv[2:]; out=sys.argv[1]
W,H=360,480; cols=4
rows=(len(files)+cols-1)//cols
sheet=Image.new('RGB',(cols*W,rows*(H+24)),'white')
d=ImageDraw.Draw(sheet)
try: f=ImageFont.truetype('arial.ttf',16)
except: f=None
for i,p in enumerate(files):
    im=Image.open(p).convert('RGB'); im.thumbnail((W,H))
    x=(i%cols)*W; y=(i//cols)*(H+24)
    sheet.paste(im,(x+(W-im.width)//2,y))
    d.text((x+4,y+H+3),os.path.basename(p)+f' {Image.open(p).size}',fill='black',font=f)
sheet.save(out,quality=88)
