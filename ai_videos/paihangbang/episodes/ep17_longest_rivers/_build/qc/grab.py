import json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
vid, tag, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
c = json.load(open('centers.json'))
pts = [('intro_1.0',1.0),('intro_3.5',3.5),('intro_4.6',4.6),('t5.5',5.5)]
for kind,rank,name,t in c:
    lab = (f'r{rank:02d}_'+name.split('–')[0].replace(' ','')) if kind=='card' else f'ins_after{rank}'
    pts.append((lab, t if t>5.0 else 5.6))
pts += [('champ_348',348.0),('champ_350.9',350.9),('tally_353',353.0),('tally_357.5',357.5),('sources_360',360.0),('end_365',365.0),('end_379.9',379.9)]
pts += [(f'rand_{x}', x) for x in (20.9, 71.3, 140.4, 196.1, 262.7, 300.0, 333.3, 343.0)]
import os; os.makedirs(outdir, exist_ok=True)
for lab,t in pts:
    out=f'{outdir}/{tag}_{t:07.2f}_{lab}.png'
    if not os.path.exists(out):
        subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',vid,'-frames:v','1',out],check=True)
print(len(pts))
