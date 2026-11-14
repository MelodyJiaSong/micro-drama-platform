import subprocess, sys
from PIL import Image, ImageDraw
tag, src, times = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(',')]
out=[]
for t in times:
    fn=f'_build/qc/frames/{tag}_{t:07.2f}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t}','-i',src,'-frames:v','1',fn],check=True)
    out.append((t,fn))
# sheets 2 cols x 3 rows of 960x540
for s in range(0,len(out),6):
    ch=out[s:s+6]; rows=(len(ch)+1)//2
    sh=Image.new('RGB',(1930,rows*560),(0,0,0)); d=ImageDraw.Draw(sh)
    for i,(t,fn) in enumerate(ch):
        im=Image.open(fn).convert('RGB').resize((960,540)); x=(i%2)*970; y=(i//2)*560
        sh.paste(im,(x,y+18)); d.text((x+4,y+2),f'{tag} t={t:.2f}s',fill=(255,255,0))
    sh.save(f'_build/qc/{tag}_sheet_{sys.argv[4]}_{s//6+1}.jpg',quality=88)
