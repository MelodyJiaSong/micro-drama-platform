"""Current mechanism keyframes: new vector drawings, never raster edits.

Top/bottom longitudinal slice and transverse GAA inset use one material model.
Dimensions are pedagogical, not a measured commercial device.
"""
import json
import math
from scientific_frames import canvas, text, line, dot, save, S, BG, INK, MUTED, BLUE, AMBER, OUT

SI = '#758b9b'
OX = '#dce9ed'
GATE = '#344e62'


def rect(d, box, fill, outline=None):
    d.rectangle(tuple(v*S for v in box), fill=fill, outline=outline, width=2*S)


def arrow(d, a, b, color=BLUE):
    line(d, [a,b], color, 3)
    theta=math.atan2(b[1]-a[1], b[0]-a[0])
    pts=[b,(b[0]-13*math.cos(theta-.45),b[1]-13*math.sin(theta-.45)),
         (b[0]-13*math.cos(theta+.45),b[1]-13*math.sin(theta+.45))]
    d.polygon([(x*S,y*S) for x,y in pts],fill=color)


def frame(key, title, subtitle, on=False, field=False, leak=False):
    im,d=canvas()
    text(d,(90,65),title,42)
    text(d,(90,125),subtitle,24,MUTED)
    text(d,(100,220),'纵向剖面 / Longitudinal section',26,MUTED)
    # Silicon is continuous from source to drain. Oxide touches Si; gate touches oxide.
    rect(d,(130,380,1040,510),SI)
    rect(d,(390,363,780,380),OX)
    rect(d,(390,510,780,527),OX)
    rect(d,(390,290,780,363),GATE)
    rect(d,(390,527,780,600),GATE)
    # Source/drain electrodes are separate from the gate stack.
    rect(d,(130,330,250,380),AMBER)
    rect(d,(920,330,1040,380),AMBER)
    text(d,(190,305),'S',26,AMBER,'mm')
    text(d,(980,305),'D',26,AMBER,'mm')
    text(d,(585,326),'G',26,INK,'mm')
    text(d,(585,564),'G',26,INK,'mm')
    if on:
        for x in range(155,1025,34):
            for y in (395,495):
                dot(d,x,y,4,AMBER)
    else:
        for x,y in [(176,417),(290,480),(470,435),(680,475),(850,420),(992,472)]:
            dot(d,x,y,4,AMBER)
    if field:
        for x in (440,535,635,730):
            arrow(d,(x,345),(x,418))
            arrow(d,(x,545),(x,472))
        text(d,(110,650),'蓝箭头：电场；琥珀点：硅内电子',24,BLUE)
        text(d,(110,687),'Field crosses dielectric; carriers stay in silicon.',22,MUTED)
    else:
        text(d,(110,650),'同一块硅，几何不变 / Same silicon, fixed geometry',25,INK)
        text(d,(110,690),'电子密度示意；不是实体道路 / Carrier density, not a road',22,MUTED)
    # Transverse inset: metal/oxide surround silicon on all four sides.
    text(d,(1135,230),'横截面 / Cross-section',22,MUTED)
    rect(d,(1150,300,1490,590),GATE)
    rect(d,(1200,365,1440,525),OX)
    rect(d,(1217,382,1423,508),SI)
    for x,y in ([(1240,400),(1280,400),(1320,400),(1360,400),(1400,400),
                 (1240,490),(1280,490),(1320,490),(1360,490),(1400,490)] if on else [(1270,427),(1380,470)]):
        dot(d,x,y,4,AMBER)
    if leak:
        # One sparse electron and short path stay INSIDE silicon; not through oxide.
        arrow(d,(540,447),(635,447),AMBER)
        text(d,(1125,650),'栅包围每片硅 / GAA',24,INK)
        text(d,(1125,690),'关态仍可能漏电',24,AMBER)
    else:
        text(d,(1140,650),'四面贴合，无空腔',24,INK)
        text(d,(1140,690),'No air gap',22,MUTED)
    for x,label,color in [(100,'硅 / Si',SI),(380,'绝缘层 / Dielectric',OX),(790,'栅 / Gate',GATE)]:
        rect(d,(x,772,x+28,800),color)
        text(d,(x+42,784),label,23,INK,'lm')
    text(d,(100,850),'结构与电荷示意 · 非尺寸实测 / Schematic, not to scale',21,MUTED)
    result=save(im,key)
    result['source']='edu_videos/tansuo/t01_inside_a_chip/storyboard/mechanism_frames.py'
    result['geometry']={'continuous_silicon':True,'air_gap':False,'transverse_gate':'four sides',
                        'carriers':'inside silicon only','on_state':on,'field_arrows':field,'dimensions':'schematic'}
    return result


if __name__=='__main__':
    rows=[
        frame('channel_not_road','硅一直在 / Silicon stays','关态起点 / OFF: no gate control voltage'),
        frame('channel_cycle','通道已形成 / Channel ON','撤去栅压之前 / Before gate voltage is removed',on=True),
        frame('electrons_disperse','撤电之前 / Before switching OFF','下一步：电子散开，材料不动 / Carriers disperse; geometry stays',on=True),
        frame('field_force','隔着绝缘层施力 / Field through dielectric','加栅压后的响应示意 / Gate-field response',on=True,field=True),
        frame('leakage','关断并非绝对零 / OFF is not zero leakage','稀疏载流子仍可能形成漏电流 / Qualitative off-state leakage',leak=True),
    ]
    (OUT/'mechanism_results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(rows,ensure_ascii=False,indent=2))
