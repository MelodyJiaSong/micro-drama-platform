import json
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SB = Path(__file__).resolve().parent
ROOT = SB.parents[3]
OUT = SB / 'diagrams'
OUT.mkdir(exist_ok=True)
FONT = ROOT / '.cache/fonts/misans/MiSans-Regular.ttf'
BG, FG, MUTED, AMBER, CYAN = '#07121B', '#F8F2E5', '#8BABB5', '#EFB569', '#6AD7D5'
SCALE = 2

def studio_background():
    yy,xx=np.mgrid[0:900*SCALE,0:1600*SCALE]
    x=xx/(1600*SCALE);y=yy/(900*SCALE)
    warm=np.exp(-((x-.1)**2/.09+(y-.35)**2/.23))
    cool=np.exp(-((x-.9)**2/.08+(y-.65)**2/.27))
    base=np.zeros((900*SCALE,1600*SCALE,3),dtype=np.float32)
    for k,b in enumerate([5,12,18]):base[:,:,k]=b+warm*[26,15,4][k]+cool*[3,21,28][k]
    grain=np.random.default_rng(60).normal(0,.7,base.shape[:2])
    base+=grain[:,:,None]
    return Image.fromarray(np.uint8(np.clip(base,0,255)))

STUDIO=studio_background()


class Board:
    def __init__(self, sid, title, sub='功能分镜示意 · 非分子真实外形 · 不按比例'):
        self.sid = sid
        self.im = STUDIO.copy()
        self.draw = ImageDraw.Draw(self.im)
        self.text(65, 25, '探索  /  血管里的小船', 18, MUTED)
        self.text(1440,25,sid,22,AMBER)
        self.text(65, 61, title, 43)
        self.text(65, 120, sub, 21, MUTED)
        self.line([(65, 168), (215, 168)], AMBER, 3)
        self.line([(230,168),(1535,168)], '#29434B',1)

    def text(self, x, y, text, size=28, color=FG):
        font = ImageFont.truetype(str(FONT), size*SCALE)
        box = self.draw.textbbox((0, 0), text, font=font)
        assert x*SCALE + box[2] <= 1570*SCALE, (self.sid, text)
        self.draw.text((x*SCALE, y*SCALE), text, fill=color, font=font)

    def line(self, points, color=AMBER, width=4):
        self.draw.line([(x*SCALE,y*SCALE) for x,y in points], fill=color, width=width*SCALE)

    def box(self, x, y, w, h, label, color=AMBER, size=30):
        xy=(x*SCALE,y*SCALE,(x+w)*SCALE,(y+h)*SCALE)
        glow=Image.new('RGBA',self.im.size,(0,0,0,0));d=ImageDraw.Draw(glow)
        d.rounded_rectangle(xy,radius=22*SCALE,outline=color,width=4*SCALE)
        glow=glow.filter(ImageFilter.GaussianBlur(16*SCALE));glow.putalpha(glow.getchannel('A').point(lambda a:int(a*.26)))
        self.im=Image.alpha_composite(self.im.convert('RGBA'),glow).convert('RGB');self.draw=ImageDraw.Draw(self.im)
        self.draw.rounded_rectangle(xy, radius=22*SCALE, fill='#122831', outline='#35505A', width=1*SCALE)
        self.line([(x+24,y+1),(x+w-24,y+1)],color,1)
        self.text(x+22,y+h/2-size*.7,label,size,color)

    def dot(self, x, y, r=17, color=AMBER):
        # Lit spheres make the lipid coding tactile; chart dot positions/counts remain exact.
        from PIL import ImageColor
        rgb=ImageColor.getrgb(color)
        for step in range(max(3,int(r*1.4)),0,-1):
            f=step/max(3,int(r*1.4));rad=r*f
            shade=tuple(int(min(255,v*(.55+.65*(1-f)))) for v in rgb)
            ox=-r*.15*(1-f);oy=-r*.2*(1-f)
            self.draw.ellipse(((x+ox-rad)*SCALE,(y+oy-rad)*SCALE,(x+ox+rad)*SCALE,(y+oy+rad)*SCALE),fill=shade)
        if r>10:self.draw.ellipse(((x-r*.37)*SCALE,(y-r*.42)*SCALE,(x-r*.13)*SCALE,(y-r*.18)*SCALE),fill=tuple(min(255,int(v*.5+110)) for v in rgb))

    def arrow(self, x1,y1,x2,y2,color=AMBER):
        self.line([(x1,y1),(x2,y2)],color)
        if x1==x2:
            sign=1 if y2>y1 else -1
            self.line([(x2-10,y2-15*sign),(x2,y2),(x2+10,y2-15*sign)],color)
        else:
            self.line([(x2-15,y2-10),(x2,y2),(x2-15,y2+10)],color)

    def save(self):
        self.im.resize((1600,900),Image.Resampling.LANCZOS).save(OUT/f'{self.sid}.png')


def chain(sid, title, nodes, focus, footer):
    b=Board(sid,title)
    n=len(nodes); width=(1400-(n-1)*55)/n
    for i,label in enumerate(nodes):
        x=80+i*(width+55)
        b.box(x,300,width,180,label, AMBER if i==focus else MUTED, 30)
        b.text(x,250,f'{i+1:02d}',30,AMBER if i==focus else MUTED)
        if i<n-1: b.arrow(x+width+9,390,x+width+45,390)
    b.text(80,590,footer,30,CYAN)
    b.text(80,760,'逐步出现；同一时刻只强调正在讲的一步。',26,MUTED)
    b.save()


def wall(sid, stage):
    b=Board(sid, ['完整内皮','一颗 LDL 的跨细胞转运','进入后的不同去向'][stage])
    if stage==2:
        b.box(120,330,340,140,'进入血管壁',AMBER)
        b.arrow(460,400,700,270,CYAN); b.box(730,205,540,130,'离开：不指定唯一通路',CYAN)
        b.arrow(460,400,700,560); b.box(730,495,540,130,'滞留：与基质结合',AMBER)
        b.text(120,740,'两条分支仅表示去向，不表示概率或多数／少数。',30)
    else:
        b.text(90,210,'血流侧',30,CYAN); b.arrow(250,235,1410,235,CYAN)
        b.box(110,310,1380,270,'',MUTED)
        for x in [455,800,1145]: b.line([(x,310),(x,580)],MUTED,2)
        b.text(130,405,'连续完整的内皮',30)
        b.text(90,670,'血管壁内',30,CYAN)
        x=970
        if stage==0:
            b.dot(x,275)
            b.text(700,730,'尚未出现破口，也没有成熟斑块。',28)
        else:
            b.draw.ellipse((925*SCALE,397*SCALE,1015*SCALE,487*SCALE),outline=CYAN,width=4*SCALE)
            b.dot(x,442)
            b.arrow(x,275,x,380); b.arrow(x,505,x,650)
            b.text(1040,410,'囊泡内只有一颗',25)
            b.text(650,730,'箭头是运动方向；不复制实心颗粒作残影。',28)
    b.save()


def risk(sid, stage):
    b=Board(sid,'同一风险层内：对照与干预','假设算例 · 非试验数据 · 非个人预测')
    b.text(75,185,'设定：5 年｜每组 100 人｜假设相对风险减少 20%',30,AMBER)
    b.text(75,232,'事件口径相同：5年内至少发生一次所定义的心血管事件',24,MUTED)
    b.text(390,287,'对照',30); b.text(800,287,'干预',30); b.text(1190,287,'绝对差',30)
    counts=[]
    for row,(label,left,right) in enumerate([('较低基线风险',10,8),('较高基线风险',20,16)]):
        y=355+row*230
        active=stage>=row+1
        b.text(70,y+50,label,28,FG if active else MUTED)
        for col,count in enumerate([left,right]):
            x=365+col*410
            for i in range(100):
                c='#E57B75' if active and i<count else '#43566C'
                b.dot(x+(i%10)*18,y+(i//10)*18,6,c)
            b.text(x+200,y+60,f'{count} 人' if active else '待揭示',32,AMBER if active else MUTED)
            counts.append({'row':row,'column':col,'denominator':100,'events':count,'revealed':active})
        b.text(1190,y+50,f'少 {left-right} 人' if active else '待揭示',34,CYAN if active else MUTED)
        if active: b.text(1190,y+103,f'{left-right} 个百分点',24,MUTED)
    b.text(75,835,'红点：发生事件的人；每行先比较组内差，随后比较两行的绝对获益。',24,MUTED)
    b.save()
    (OUT/f'{sid}.json').write_text(json.dumps({'kind':'hypothetical','relative_reduction':.2,'years':5,'groups':counts},indent=2),encoding='utf-8')


def card(sid,title,rows,subtitle='说明性分镜 · 逐行随口播出现'):
    b=Board(sid,title,subtitle)
    if sid=='V22':
        b.text(90,250,'15',180,AMBER);b.text(340,375,'年随访',40)
        b.line([(560,240),(560,730)],'#34545B',1)
        b.text(630,285,'特定 PCSK9 基因变异人群',32,MUTED)
        b.text(630,385,'较低 LDL',58,FG)
        b.text(630,485,'较低冠心病风险',52,CYAN)
        b.text(90,755,'限定研究人群与随访期；不是所有人的终生风险预测。',27,MUTED)
        b.text(90,815,'Cohen et al.  /  NEJM 2006  /  PMID 16554528',23,MUTED)
    elif sid=='V29':
        for x,year,heading,sub in [(90,'2010','他汀随机试验汇总','CTT'),(830,'2015','他汀基础上加用依折麦布','IMPROVE-IT')]:
            b.box(x,235,670,400,'',CYAN if x>100 else AMBER)
            b.text(x+35,270,year,88,CYAN if x>100 else AMBER)
            b.text(x+35,420,heading,32)
            b.text(x+35,500,sub,26,MUTED)
        b.text(100,715,'观察心梗等心血管事件',43)
        b.text(100,800,'不同研究的治疗、人群、终点和获益各有适用范围。',26,MUTED)
    elif sid=='V28':
        b.text(90,225,'血脂不只有 LDL',54)
        for i,(label,color) in enumerate([('胆固醇',AMBER),('甘油三酯',CYAN)]):
            x=180+i*680
            b.dot(x+170,440,95,color)
            b.text(x+55,575,label,44,color)
        b.text(100,725,'他汀主要降低 LDL-C',40)
        b.text(100,810,'不是清空血脂，也不表示其他指标完全不受影响。',25,MUTED)
    elif sid=='V33':
        b.text(90,245,'风险下降',65,AMBER);b.text(470,250,'≠',65,MUTED);b.text(580,245,'风险归零',65)
        for i,label in enumerate(['血压','吸烟','糖尿病']):
            x=120+i*490;b.box(x,420,420,180,'',MUTED)
            b.text(x+35,447,f'0{i+1}',25,CYAN);b.text(x+35,505,label,42)
        b.text(100,750,'整体风险  /  实际降幅  /  持续时间',34,MUTED)
    elif sid=='V37':
        b.text(90,280,'不胖，',100,FG);b.text(90,415,'为什么 LDL 也会高？',75,AMBER)
        b.text(100,720,'接着看身体怎样产生、运输和清除 LDL',30,MUTED)
    elif sid in ['V38','V38b']:
        for i,row in enumerate(rows):b.text(100,245+i*98,row,36 if i==0 else 30,FG if i==0 else MUTED)
    else:
        for i,row in enumerate(rows):
            b.text(100,230+i*100,row,32,AMBER if i==0 else FG)
    b.save()


def lipid_cell(sid, foamy):
    b=Board(sid,'泡沫细胞' if foamy else '免疫细胞吞入颗粒','功能分镜示意 · 此时尚未展示成熟斑块 · 不按比例')
    b.text(90,220,'血管壁内',30,CYAN)
    b.draw.ellipse((560*SCALE,260*SCALE,1210*SCALE,760*SCALE),fill='#203247',outline=CYAN,width=4*SCALE)
    b.draw.ellipse((930*SCALE,415*SCALE,1080*SCALE,580*SCALE),fill='#405573',outline=MUTED,width=2*SCALE)
    if not foamy:
        b.dot(360,460,22)
        b.draw.ellipse((330*SCALE,430*SCALE,390*SCALE,490*SCALE),outline=MUTED,width=3*SCALE)
        b.arrow(400,460,650,460)
        b.text(170,560,'滞留并发生变化的颗粒',28)
        for x,y in [(730,400),(790,490),(740,585)]: b.dot(x,y,23)
        b.text(680,800,'细胞内形成脂滴',30,AMBER)
    else:
        for x,y in [(680,390),(770,350),(870,370),(700,500),(810,460),(860,550),(730,610),(820,650),(920,670),(1090,620)]: b.dot(x,y,29)
        b.text(100,720,'脂滴增多',32,AMBER)
        b.text(100,800,'多年演变由下一镜时间转场交代；不是一吞就变成斑块。',28)
    b.save()


def main():
    b=Board('V10','LDL-C 量的是胆固醇浓度')
    b.box(95,275,620,350,'',MUTED)
    b.text(120,225,'一定体积的血液',30,CYAN)
    for (x,y),cargo in zip([(240,390),(470,405),(360,535)],[3,2,4]):
        b.draw.ellipse(((x-65)*SCALE,(y-65)*SCALE,(x+65)*SCALE,(y+65)*SCALE),outline=MUTED,width=3*SCALE)
        for dx,dy in [(-20,-15),(20,-15),(-20,20),(20,20)][:cargo]:b.dot(x+dx,y+dy,12)
    b.arrow(740,460,880,460)
    b.box(910,350,550,210,'胆固醇浓度',AMBER,38)
    b.text(100,690,'圆圈：LDL 颗粒　金点：胆固醇载荷（数量仅示意）',28,CYAN)
    b.text(100,770,'只看 LDL 携带的胆固醇；不是直接数颗粒，也不是全身总量。',28)
    b.save()
    b=Board('V11','同镜交代生理作用与暴露风险')
    b.text(90,225,'生理作用：受体结合 → 囊泡内吞 → 细胞利用胆固醇',32,CYAN)
    b.line([(90,375),(1500,375)],MUTED,2)
    b.text(90,470,'风险：过量 LDL 长期暴露，提高动脉粥样硬化风险',32,AMBER)
    b.text(90,710,'上下是两个层面的说明；正常内吞不直接导致过量暴露。',28)
    b.save()
    for sid,stage in [('V12',0),('V13',1),('V14',2)]: wall(sid,stage)
    lipid_cell('V16',False);lipid_cell('V17',True)
    card('V22','遗传研究说明什么',['特定 PCSK9 基因变异人群','随访 15 年：LDL 较低，冠心病风险也较低','不能外推为所有人“终生风险减半”','Cohen 等 · NEJM 2006 · PMID 16554528'])
    # V23–V27 now use liver_motion videos/posters; old chain images are archival.
    card('V28','血脂不只一种',['血脂：胆固醇、甘油三酯等','脂蛋白负责运输这些脂质','他汀主要降低 LDL 胆固醇','不等于清空所有血脂'])
    card('V29','结局证据',['他汀：随机试验汇总 · CTT 2010','部分其他降 LDL 治疗：IMPROVE-IT 2015','观察终点：心血管事件','不同治疗、人群和终点的获益范围不同'])
    for sid,stage in [('V30',0),('V31',1),('V32',2)]: risk(sid,stage)
    card('V33','风险不会全部消失',['降低 LDL ≠ 血管恢复全新','血压 · 吸烟 · 糖尿病','还要看整体风险、实际降幅和持续时间'])
    card('V37','留下一个问题',['不胖，为什么 LDL 也会高？','身体怎样产生、运输和清除 LDL'], '后续主题提示 · 顺序服从系列知识点地图')
    card('V38','科普说明',['本片为科普，不能替代医生诊疗','用药、停药请遵医嘱'], '片尾第一屏 · 0–5 秒')
    card('V38b','AI 内容与出处',['画面含 AI 生成合成内容；结构为示意','Nature 2025 · Cohen 2006','CTT 2010 · IMPROVE-IT 2015','EAS 2020 · 中国血脂管理指南 2023','完整出处见随片资料'], '片尾第二屏 · 5–13 秒')
    print('机制与证据分镜图已绘制；使用 MiSans，1600×900。')


if __name__=='__main__':
    main()
