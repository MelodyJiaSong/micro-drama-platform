import sys
sys.path.insert(0, r"C:\workspace\micro-drama-platform\projects\rank_scroll")
from rank_scroll.contract import load_episode
from rank_scroll import timeline as T
ep_dir = r"C:\workspace\micro-drama-platform\ai_videos\paihangbang\episodes\ep18_fastest_cars"
r = load_episode(ep_dir)
ep = r[0] if isinstance(r, tuple) else r
tl = T.build(ep)
W = T.W
def t_of(x):
    # first frame where camera >= x
    for f in range(tl.total_frames):
        if tl.camera(f) >= x:
            return f / 60
    return None
print("hold frames", tl.f_hold, "intro", tl.f_intro)
for e in tl.elements:
    name = ep.items[e.index].name if e.kind == "card" else (ep.insights[e.index].text[:40] if hasattr(ep,'insights') else '')
    full_in = t_of(e.center + e.slot/2 - W/2)   # right edge on screen
    centre = t_of(e.center)
    leave = t_of(e.center - e.slot/2 + W/2)     # left edge leaving
    print(f"{e.kind:8s} r{e.rank:>3} {name[:40]:40s} fullin {full_in} centre {centre} leftedge-out {leave}")
