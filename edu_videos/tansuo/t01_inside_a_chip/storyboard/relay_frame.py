"""Relay principle: coil is electrically separate from the moving contact circuit."""
import json
from scientific_frames import canvas,text,line,dot,save,OUT,MUTED,BLUE,AMBER,INK,S
im,d=canvas()
text(d,(100,75),'继电器：触点真的会动',42)
text(d,(100,140),'Relay: a contact physically moves',28,MUTED)
# Independent coil control circuit, conventional inductor loops.
line(d,[(110,490),(260,490)],AMBER,5)
for i in range(6):
    x=260+i*55
    d.arc((x*S,430*S,(x+55)*S,550*S),180,360,fill=AMBER,width=5*S)
line(d,[(590,490),(720,490)],AMBER,5)
text(d,(310,570),'线圈 / Coil',27,AMBER)
line(d,[(270,510),(580,510)],MUTED,5)
line(d,[(270,525),(580,525)],MUTED,5)
# Separate load contacts: movable conductor on left, fixed conductor on right.
line(d,[(940,400),(1060,400)],BLUE,5)
line(d,[(1060,400),(1250,315)],BLUE,6)
line(d,[(1268.1466,400),(1470,400)],BLUE,5)
dot(d,1060,400,9,INK); dot(d,1268.1466,400,9,INK)
dot(d,1250,315,9,INK)
text(d,(1090,245),'动触点 / Moving',25,BLUE)
text(d,(1280,465),'静触点 / Fixed',25,BLUE)
# Dashed mechanical coupling carries no current.
for x in range(660,1060,30): line(d,[(x,350),(x+14,350)],MUTED,3)
line(d,[(660,350),(660,440)],MUTED,3)
text(d,(670,300),'机械联动 / Motion',23,MUTED)
line(d,[(1200,335),(1215,375)],AMBER,3)
d.polygon([(1203*S,369*S),(1215*S,385*S),(1222*S,365*S)],fill=AMBER)
text(d,(950,600),'两个独立触点，当前断开',27,INK)
text(d,(950,645),'Two separate contacts, open',23,MUTED)
text(d,(100,770),'线圈通电 → 吸动衔铁 → 触点闭合',31,INK)
text(d,(100,825),'原理示意，非器件外形 / Principle schematic, not a physical layout',23,MUTED)
row=save(im,'relay_compare'); row['source']='edu_videos/tansuo/t01_inside_a_chip/storyboard/relay_frame.py'
(OUT/'relay_results.json').write_text(json.dumps([row],indent=2),encoding='utf-8')
