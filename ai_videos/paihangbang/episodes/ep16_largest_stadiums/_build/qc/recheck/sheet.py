import sys
from PIL import Image, ImageDraw
out=sys.argv[1]; files=sys.argv[2:]
W=640; ims=[]
for f in files:
    im=Image.open(f).convert('RGB'); im.thumbnail((W,W)); 
    c=Image.new('RGB',(W,W+30),'white'); c.paste(im,(0,30)); ImageDraw.Draw(c).text((5,5),f.split('/')[-1],fill='black'); ims.append(c)
cols=2; rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*W,rows*(W+30)),'gray')
for i,c in enumerate(ims): S.paste(c,((i%cols)*W,(i//cols)*(W+30)))
S.save(out,quality=85)
