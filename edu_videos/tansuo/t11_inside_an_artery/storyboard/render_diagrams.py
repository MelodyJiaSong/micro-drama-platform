import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SB = Path(__file__).resolve().parent
ROOT = SB.parents[3]
OUT = SB / 'diagrams'
OUT.mkdir(exist_ok=True)
FONT = ROOT / '.cache/fonts/misans/MiSans-Regular.ttf'
BG, FG, MUTED, AMBER, CYAN = '#101C2A', '#F5F3ED', '#ADBDCC', '#EDB55E', '#74CBD2'
SCALE = 2


class Board:
    def __init__(self, sid, title, sub='功能分镜示意 · 非分子真实外形 · 不按比例'):
        self.sid = sid
        self.im = Image.new('RGB', (1600*SCALE, 900*SCALE), BG)
        self.draw = ImageDraw.Draw(self.im)
        self.text(65, 42, sid + '  /  ' + title, 42)
        self.text(65, 105, sub, 25, MUTED)
        self.line([(65, 157), (1535, 157)], '#35475A', 2)

    def text(self, x, y, text, size=28, color=FG):
        font = ImageFont.truetype(str(FONT), size*SCALE)
        box = self.draw.textbbox((0, 0), text, font=font)
        assert x*SCALE + box[2] <= 1570*SCALE, (self.sid, text)
        self.draw.text((x*SCALE, y*SCALE), text, fill=color, font=font)

    def line(self, points, color=AMBER, width=4):
        self.draw.line([(x*SCALE,y*SCALE) for x,y in points], fill=color, width=width*SCALE)

    def box(self, x, y, w, h, label, color=AMBER, size=30):
        self.draw.rounded_rectangle((x*SCALE,y*SCALE,(x+w)*SCALE,(y+h)*SCALE), radius=16*SCALE, fill='#203247', outline=color, width=3*SCALE)
        self.text(x+22,y+h/2-size*.7,label,size,color)

    def dot(self, x, y, r=17, color=AMBER):
        self.draw.ellipse(((x-r)*SCALE,(y-r)*SCALE,(x+r)*SCALE,(y+r)*SCALE),fill=color)

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
    for i,row in enumerate(rows):
        b.text(100,230+i*100,row,32,AMBER if i==0 else FG)
    b.save()


def main():
    chain('V10','LDL-C 量的是货物含量',['LDL 颗粒','携带的胆固醇','LDL-C 含量'],1,'不等同于直接计数 LDL 颗粒。')
    b=Board('V11','同镜交代生理作用与暴露风险')
    b.text(90,225,'生理作用：受体结合 → 囊泡内吞 → 细胞利用胆固醇',32,CYAN)
    b.line([(90,375),(1500,375)],MUTED,2)
    b.text(90,470,'风险：过量 LDL 长期暴露，提高动脉粥样硬化风险',32,AMBER)
    b.text(90,710,'上下是两个层面的说明；正常内吞不直接导致过量暴露。',28)
    b.save()
    for sid,stage in [('V12',0),('V13',1),('V14',2)]: wall(sid,stage)
    card('V22','遗传研究说明什么',['特定 PCSK9 基因变异人群','随访 15 年：LDL 较低，冠心病风险也较低','不能外推为所有人“终生风险减半”','Cohen 等 · NEJM 2006 · PMID 16554528'])
    chain('V23','从血管去看肝脏',['血中 LDL','肝脏定位','单个肝细胞'],1,'探索表涟漪连接两个位置，先定位，再讲机制。')
    nodes=['合成减少','受体增多','LDL 内吞','血中颗粒减少']
    for sid,focus in [('V24',0),('V25',1),('V26',2)]:
        chain(sid,'他汀作用的顺序',nodes,focus,'功能节点只代表作用关系；受体与酶不画成伪真实分子结构。')
    chain('V27','不只是化验单数字',['循环颗粒减少','滞留机会减少'],1,'独立限制：遗传等升高原因仍在；不能画成上述链条造成遗传原因。')
    card('V28','血脂不只一种',['血脂：胆固醇、甘油三酯等','脂蛋白负责运输这些脂质','他汀主要降低 LDL 胆固醇','不等于清空所有血脂'])
    card('V29','结局证据',['他汀：随机试验汇总 · CTT 2010','部分其他降 LDL 治疗：IMPROVE-IT 2015','观察终点：心血管事件','不同治疗、人群和终点的获益范围不同'])
    for sid,stage in [('V30',0),('V31',1),('V32',2)]: risk(sid,stage)
    card('V33','风险不会全部消失',['降低 LDL ≠ 血管恢复全新','血压 · 吸烟 · 糖尿病','还要看整体风险、实际降幅和持续时间'])
    card('V37','下一期的问题',['不胖，为什么 LDL 也会高？','身体怎样产生、运输和清除 LDL'], '下期主题提示 · 不指定未经确定的集号')
    card('V38','科普说明',['本片为科普，不能替代医生诊疗','用药、停药请遵医嘱'], '片尾第一屏 · 0–4 秒')
    card('V38b','AI 内容与出处',['画面含 AI 生成合成内容；结构为示意','Nature 2025 · Cohen 2006','CTT 2010 · IMPROVE-IT 2015','完整出处见随片资料'], '片尾第二屏 · 4–8 秒')
    print('机制与证据分镜图已绘制；使用 MiSans，1600×900。')


if __name__=='__main__':
    main()
