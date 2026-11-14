import sys,os
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1]; files=sys.argv[2:]
W,H=960,540
sheet=Image.new('RGB',(2*W,((len(files)+1)//2)*(H+20)),'white')
d=ImageDraw.Draw(sheet); f=ImageFont.truetype('arial.ttf',16)
for i,p in enumerate(files):
    im=Image.open(p).convert('RGB').resize((W,H))
    x=(i%2)*W; y=(i//2)*(H+20)
    sheet.paste(im,(x,y)); d.text((x+4,y+H+2),os.path.basename(p),fill='black',font=f)
sheet.save(out,quality=85)
