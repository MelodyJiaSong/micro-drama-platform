"""Two CMOS inverter stages with an explicit output-to-next-gate wire."""
import json
from scientific_frames import canvas,text,line,dot,save,OUT,MUTED,BLUE,AMBER,INK,S,BG

def stage(d,x,high):
    # Node x is common drain/output; gate electrodes remain visibly separate.
    line(d,[(x,225),(x,295)],MUTED,4)
    line(d,[(x-45,225),(x+45,225)],MUTED,4)
    text(d,(x+65,225),'VDD',22,MUTED,'lm')
    line(d,[(x,385),(x,515)],BLUE,4)
    line(d,[(x,605),(x,675)],MUTED,4)
    for w,y in [(80,675),(55,689),(28,703)]:
        line(d,[(x-w/2,y),(x+w/2,y)],MUTED,3)
    for cy,label,on in [(340,'P',not high),(560,'N',high)]:
        color=BLUE if on else MUTED
        line(d,[(x,cy-45),(x-55,cy-45),(x-55,cy-12)],color,4)
        line(d,[(x-55,cy+12),(x-55,cy+45),(x,cy+45)],color,4)
        if on: line(d,[(x-55,cy-12),(x-55,cy+12)],color,4)
        line(d,[(x-100,cy-50),(x-100,cy+50)],AMBER,4)
        line(d,[(x-175,cy),(x-100,cy)],AMBER,3)
        text(d,(x+30,cy),label+(' ON' if on else ' OFF'),25,color,'lm')
    line(d,[(x-175,340),(x-175,560)],AMBER,3)
    dot(d,x-175,450,5,AMBER)
    dot(d,x,450,6,BLUE)

if __name__=='__main__':
    im,d=canvas()
    text(d,(90,65),'输出连到下一级栅极',42)
    text(d,(90,125),'Output wire drives the next gates',28,MUTED)
    stage(d,545,True); stage(d,1170,False)
    line(d,[(140,450),(370,450)],AMBER,4)
    text(d,(175,408),'IN = 1',30,AMBER)
    line(d,[(545,450),(995,450)],BLUE,5)
    text(d,(755,408),'OUT = 0',30,BLUE,'mm')
    text(d,(755,490),'导线 / Wire',24,MUTED,'mm')
    line(d,[(1170,450),(1440,450)],BLUE,5)
    text(d,(1400,408),'OUT = 1',30,BLUE,'mm')
    text(d,(430,758),'本级 / Stage 1',25,INK)
    text(d,(1050,758),'下一级 / Stage 2',25,INK)
    text(d,(90,835),'通断示意；稳态 1 → 0 → 1 / Switching schematic, steady state',23,MUTED)
    row=save(im,'array_signal')
    row['source']='edu_videos/tansuo/t01_inside_a_chip/storyboard/array_frame.py'
    (OUT/'array_results.json').write_text(json.dumps([row],indent=2),encoding='utf-8')
    print(json.dumps(row))
