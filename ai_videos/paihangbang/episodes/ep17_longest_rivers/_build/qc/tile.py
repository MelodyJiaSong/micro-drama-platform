import sys,glob,os
from PIL import Image, ImageDraw, ImageFont
files=sorted(glob.glob(sys.argv[1])); prefix=sys.argv[2]; per=int(sys.argv[3]) if len(sys.argv)>3 else 4
font=ImageFont.truetype('arial.ttf',22)
for k in range(0,len(files),per):
    grp=files[k:k+per]; cols=2; rows=(len(grp)+1)//2
    S=Image.new('RGB',(cols*960,rows*570),'white'); d=ImageDraw.Draw(S)
    for i,f in enumerate(grp):
        im=Image.open(f).convert('RGB').resize((960,540)); x=(i%2)*960; y=(i//2)*570
        S.paste(im,(x,y+30)); d.text((x+5,y+3),os.path.basename(f),fill='black',font=font)
    S.save(f'{prefix}_{k//per+1:02d}.jpg',quality=88)
