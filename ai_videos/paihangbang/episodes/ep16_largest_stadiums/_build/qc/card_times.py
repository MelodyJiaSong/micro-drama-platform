import sys
sys.path.insert(0, r'C:/workspace/micro-drama-platform/projects/rank_scroll')
from rank_scroll.contract import load_episode
from rank_scroll import timeline as T
ep = load_episode('.')
if isinstance(ep, tuple): ep = ep[0]
tl = T.build(ep)
print('segments', tl.segments, 'hold', tl.f_hold)
for el in tl.elements:
    # find first frame where camera >= center
    f0 = None
    for f in range(tl.total_frames):
        if f >= tl.f_intro and tl.camera(f) >= el.center:
            f0 = f; break
    name = ep.items[el.index].name if el.kind=='card' else 'INSIGHT '+ep.insights[el.index].text[:40]
    print(f"{el.kind:7s} r{el.rank:<3d} t={f0/60 if f0 is not None else -1:7.2f}s f={f0} {name}")
