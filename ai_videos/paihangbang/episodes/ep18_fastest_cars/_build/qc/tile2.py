import sys,glob,os
from PIL import Image,ImageDraw,ImageFont
files=sys.argv[3:]; out=sys.argv[1]; W=int(sys.argv[2])
ims=[Image.open(f).convert('RGB') for f in files]
for im in ims: im.thumbnail((W,W))
w,h=ims[0].size; cols=2; rows=(len(ims)+1)//2
S=Image.new('RGB',(w*cols,(h+24)*rows),'white'); d=ImageDraw.Draw(S); f=ImageFont.truetype('arial.ttf',20)
for i,im in enumerate(ims):
    x=(i%cols)*w;y=(i//cols)*(h+24); S.paste(im,(x,y+24)); d.text((x+4,y+2),os.path.basename(files[i]),fill='black',font=f)
S.save(out,quality=88)
