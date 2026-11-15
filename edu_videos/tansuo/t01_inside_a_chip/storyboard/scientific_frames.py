"""Deterministic scientific storyboard figures, no edits to generated images."""
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[4]
SB = Path(__file__).resolve().parent
OUT = SB / 'frames'
OUT.mkdir(exist_ok=True)
S = 2
W, H = 1600, 900
FONT = ROOT / '.cache/fonts/misans/MiSans-Regular.ttf'
BG = '#101c29'
INK = '#edf2f7'
MUTED = '#8ea7bb'
BLUE = '#8bdcf7'
AMBER = '#efb55d'


def canvas():
    im = Image.new('RGB',(W*S,H*S),BG)
    return im,ImageDraw.Draw(im)


def line(d,coords,fill=INK,width=3):
    d.line([(x*S,y*S) for x,y in coords],fill=fill,width=width*S)


def text(d,xy,value,size=28,fill=INK,anchor='la'):
    d.text((xy[0]*S,xy[1]*S),value,font=ImageFont.truetype(str(FONT),size*S),fill=fill,anchor=anchor)


def dot(d,x,y,r=5,fill=BLUE):
    d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=fill)


def save(im,key):
    path=OUT/f'{key}_math_r1.png'
    im.resize((W,H),Image.Resampling.LANCZOS).save(path)
    return {'key':key,'path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kind':'code-scientific-figure','source':str(Path(__file__).relative_to(ROOT)).replace('\\','/')}


def inverter():
    im,d=canvas()
    text(d,(100,75),'1 → 0',48,AMBER)
    text(d,(100,140),'反相器 / Inverter',30)
    x=850
    line(d,[(x,160),(x,265)],MUTED,5)
    line(d,[(760,160),(940,160)],MUTED,5)
    text(d,(960,160),'VDD',28,MUTED,'lm')
    line(d,[(x,385),(x,515)],BLUE,5)
    line(d,[(x,635),(x,740)],BLUE,5)
    for w,y in [(100,740),(70,755),(40,770)]:
        line(d,[(x-w/2,y),(x+w/2,y)],BLUE,4)
    text(d,(960,740),'0 V',28,BLUE,'lm')
    for cy,typ,on in [(325,'P',False),(575,'N',True)]:
        line(d,[(x,cy-60),(x-70,cy-60),(x-70,cy-15)],BLUE if on else MUTED,5)
        line(d,[(x-70,cy+15),(x-70,cy+60),(x,cy+60)],BLUE if on else MUTED,5)
        if on:
            line(d,[(x-70,cy-15),(x-70,cy+15)],BLUE,5)
        line(d,[(x-115,cy-65),(x-115,cy+65)],AMBER,4)
        line(d,[(470,cy),(x-115,cy)],AMBER,3)
        if not on:
            d.ellipse(((x-144)*S,(cy-11)*S,(x-122)*S,(cy+11)*S),fill=BG,outline=AMBER,width=3*S)
        text(d,(x+55,cy),typ,40,BLUE if on else MUTED,'lm')
    line(d,[(270,450),(470,450)],AMBER,5)
    line(d,[(470,325),(470,575)],AMBER,3)
    dot(d,470,450,6,AMBER)
    text(d,(250,450),'1',48,AMBER,'rm')
    text(d,(300,495),'IN',25,AMBER)
    line(d,[(x,450),(1200,450)],BLUE,5)
    dot(d,x,450,7,BLUE)
    text(d,(1240,450),'0',48,BLUE,'lm')
    text(d,(1135,495),'OUT',25,BLUE)
    text(d,(100,815),'通断示意 / Switching schematic',24,MUTED)
    return save(im,'inverter')


def voltage():
    im,d=canvas()
    x0,y0,x1,y1=240,700,1410,180
    line(d,[(x0,y1),(x0,y0),(x1,y0)],MUTED,3)
    text(d,(150,170),'V',40)
    text(d,(1420,735),'t',34)
    points=[(240,630),(470,630),(470,260),(860,260),(860,630),(1120,630),(1120,260),(1410,260)]
    line(d,points,BLUE,7)
    text(d,(340,570),'0',62,MUTED,'mm')
    text(d,(660,200),'1',62,BLUE,'mm')
    text(d,(980,570),'0',62,MUTED,'mm')
    text(d,(1270,200),'1',62,BLUE,'mm')
    text(d,(130,800),'电压示意 / Voltage schematic',28,MUTED)
    return save(im,'voltage_01')


def lattice(key,detail):
    im,d=canvas()
    a=.5431020511
    dz=a/4
    layers=44
    # Diamond cubic (001) planes, alternating two-dimensional offsets.
    offsets=[[(0,0),(.5,.5)],[(.25,.25),(.75,.75)],[(0,.5),(.5,0)],[(.25,.75),(.75,.25)]]
    points=[]
    for k in range(layers):
        for cx in range(5):
            for cy in range(2):
                for dx,dy in offsets[k%4]:
                    points.append(((cx+dx)*a,(cy+dy)*a,a/8+k*dz,k))
    def proj(p):
        x,y,z,_=p
        return (365+x*220+y*65,760-z*105-y*22)
    bond=a*math.sqrt(3)/4
    count=0
    for i,p in enumerate(points):
        for q in points[i+1:]:
            if q[3]-p[3]>1:
                break
            dist=math.dist(p[:3],q[:3])
            if abs(dist-bond)<1e-8:
                line(d,[proj(p),proj(q)],'#45697e',1)
                count+=1
    for p in sorted(points,key=lambda p:p[1],reverse=True):
        x,y=proj(p)
        dot(d,x,y,3.3,AMBER if p[3]==0 and detail else '#9fbac9')
    bx=1180
    line(d,[(bx,760),(bx,130)],BLUE,3)
    line(d,[(bx-18,760),(bx+18,760)],BLUE,3)
    line(d,[(bx-18,130),(bx+18,130)],BLUE,3)
    text(d,(1210,445),'6 nm',40,BLUE,'lm')
    text(d,(110,85),'Si  [001]',44)
    text(d,(110,150),'局部放大' if detail else '44 层',48,AMBER)
    text(d,(110,220),'Magnified inset' if detail else '44 layers',23,MUTED)
    if detail:
        text(d,(285,755),'1',30,AMBER,'rm')
    else:
        text(d,(140,810),'a / 4 ≈ 0.136 nm',30,MUTED)
    data=save(im,key)
    data['geometry']={'lattice_constant_nm':a,'direction':'[001]','layers':layers,'plane_spacing_nm':dz,'nominal_thickness_nm':6,'atom_count':len(points),'bond_count':count,'bond_length_nm':bond,'projection':'orthographic oblique; points computed from diamond cubic basis'}
    return data


if __name__=='__main__':
    results=[inverter(),voltage(),lattice('atom_count',True),lattice('atom_thickness',False)]
    (OUT/'scientific_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
