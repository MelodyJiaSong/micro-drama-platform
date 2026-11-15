import json,subprocess,sys,hashlib,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'tools'))
from blender_exe import BLENDER
OUT=Path(__file__).resolve().parent
MODE=sys.argv[1] if len(sys.argv)>1 else 'stills'
IDS=sys.argv[2:] or ['V23','V24','V25','V26','V27']
dur={'V23':7,'V24':7,'V25':9,'V26':7,'V27':10}
titles={'V23':'走近肝脏','V24':'胆固醇合成减少','V25':'更多受体，更多结合位点','V26':'跟住这一颗 LDL','V27':'清除以后，循环颗粒减少'}
sub={'V23':'器官定位 → 肝细胞','V24':'作用关系示意；不是分子真实外形','V25':'时间压缩；不是服药瞬间完成','V26':'剖面演示：结合 → 膜内陷 → 囊泡分离','V27':'仍有 LDL 循环；不是清空血脂'}
FONT=ROOT/'.cache/fonts/misans/MiSans-Regular.ttf'
FFMPEG=shutil.which('ffmpeg')

def overlay(sid):
 im=Image.new('RGBA',(960,540));d=ImageDraw.Draw(im)
 for y in range(100):d.line([(0,y),(960,y)],fill=(3,12,18,int(220*(1-y/100))))
 for y in range(450,540):d.line([(0,y),(960,y)],fill=(3,12,18,int(210*((y-450)/90))))
 d.text((30,18),titles[sid],font=ImageFont.truetype(str(FONT),26),fill='#F7EEE0')
 d.text((30,56),sub[sid],font=ImageFont.truetype(str(FONT),15),fill='#9ABCC3')
 if sid=='V24':
  d.text((30,465),'白：他汀作用标记   /   青绿：酶作用位置   /   金：胆固醇合成产物',font=ImageFont.truetype(str(FONT),16),fill='#E6E3D9')
 if sid=='V26':
  d.text((30,465),'前侧剖开以展示内部；线框表示囊泡包膜',font=ImageFont.truetype(str(FONT),16),fill='#E6E3D9')
 d.text((30,507),'探索  /  血脂     ·     结构与颜色示意',font=ImageFont.truetype(str(FONT),15),fill='#C2D1D4')
 d.text((766,507),f'{sid}  ·  无声预演',font=ImageFont.truetype(str(FONT),15),fill='#EFB569')
 path=OUT/f'{sid}_overlay.png';im.save(path);return path

def encode(sid):
 frame_dir=OUT/'frames_eevee'/sid;n=dur[sid]*12
 frames=sorted(frame_dir.glob('*.png'));assert len(frames)==n,(sid,len(frames),n)
 ov=overlay(sid);out=OUT/f'{sid}.mp4'
 cmd=[FFMPEG,'-hide_banner','-loglevel','error','-y','-framerate','12','-i',str(frame_dir/'%04d.png'),'-i',str(ov),'-filter_complex','[0:v][1:v]overlay=0:0:format=auto,format=yuv420p,fps=24[v]','-map','[v]','-c:v','libx264','-crf','18','-preset','fast','-movflags','+faststart',str(out)]
 subprocess.run(cmd,check=True)
 im=Image.open(frames[int(n*.56)]).convert('RGBA');im=Image.alpha_composite(im,Image.open(ov).convert('RGBA'));im.convert('RGB').save(OUT/f'{sid}_poster.png')
 print('encoded',sid,flush=True)

if MODE in ['stills','render']:
 for sid in IDS:
  with (OUT/f'{sid}_{MODE}.log').open('w',encoding='utf-8') as log:
   proc=subprocess.run([BLENDER,'--factory-startup','-b','-t','8','--python',str(OUT/'render_blender.py'),'--',sid,'still' if MODE=='stills' else 'animation'],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
  if proc.returncode:raise RuntimeError(f'{sid} render failed; see log')
  print('rendered',sid,MODE,flush=True)
  if MODE=='render':encode(sid)
elif MODE=='encode':
 for sid in IDS:encode(sid)
elif MODE=='concat':
 listing=OUT/'concat.txt';listing.write_text('\n'.join("file '"+str(OUT/f'{sid}.mp4').replace('\\','/')+"'" for sid in dur),encoding='utf-8')
 subprocess.run([FFMPEG,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/'liver_motion_v4.mp4')],check=True)
 print('40-second silent liver motion preview ready')
