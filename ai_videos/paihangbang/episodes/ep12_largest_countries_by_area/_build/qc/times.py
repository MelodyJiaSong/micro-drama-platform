"""QC: 每张卡 / 洞察卡到达屏幕中心的时间（用渲染器自身的 timeline 与 publish._arrive_s）。"""
import sys, json
sys.path.insert(0, r'C:\workspace\micro-drama-platform\projects\rank_scroll')
from rank_scroll.contract import load_episode
from rank_scroll.timeline import build
from rank_scroll.publish import _arrive_s
ep = load_episode(sys.argv[1])
if isinstance(ep, tuple): ep = ep[0]
tl = build(ep)
out = []
for e in tl.elements:
    t = _arrive_s(tl, e.center)
    lab = f"#{e.rank}" if e.kind == 'card' else e.kind
    out.append((round(t, 2), e.kind, getattr(e, 'rank', None)))
    print(f"{t:7.2f} {e.kind} {lab}")
