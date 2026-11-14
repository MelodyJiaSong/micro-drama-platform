import sys,glob
from PIL import Image, ImageDraw
out=sys.argv[1]; files=sys.argv[2:]
W,H=640,360; cols=3; rows=(len(files)+cols-1)//cols
S=Image.new('RGB',(cols*W,rows*H),'black')
for i,f in enumerate(files):
    im=Image.open(f).convert('RGB').resize((W,H)); d=ImageDraw.Draw(im); d.rectangle((0,0,150,18),fill='black'); d.text((3,3),f.split('_')[-1][:-4],fill='yellow')
    S.paste(im,((i%cols)*W,(i//cols)*H))
S.save(out,quality=85)
