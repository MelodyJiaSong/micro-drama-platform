import sys,glob
from PIL import Image,ImageDraw,ImageFont
files=sorted(glob.glob(sys.argv[1])); out=sys.argv[2]; step=float(sys.argv[3]); start_idx=int(sys.argv[4]) if len(sys.argv)>4 else 0
cols=4
ims=[Image.open(f) for f in files]
w,h=ims[0].size
rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(w*cols,(h+22)*rows),'white'); d=ImageDraw.Draw(S)
f=ImageFont.truetype('arial.ttf',18)
for i,im in enumerate(ims):
    x=(i%cols)*w;y=(i//cols)*(h+22)
    S.paste(im,(x,y+22)); t=(start_idx+i)*step
    d.text((x+4,y+2),f"{files[i][-9:]} t={t:.0f}s ({int(t//60)}:{int(t%60):02d})",fill='black',font=f)
S.save(out,quality=85)
