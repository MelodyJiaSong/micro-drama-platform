import sys, json
sys.path.insert(0, r'C:\workspace\micro-drama-platform\projects\rank_scroll')
from pathlib import Path
from rank_scroll.contract import load_episode
from rank_scroll.timeline import build, FPS
ep, _ = load_episode(Path(r'C:\workspace\micro-drama-platform\ai_videos\paihangbang\episodes\ep11_largest_ships'), strict_images=True)
tl = build(ep)
# find frame when element centre == camera (screen centre)
out = []
for e in tl.elements:
    f0 = None
    for f in range(tl.total_frames):
        if tl.camera(f) >= e.center:
            f0 = f; break
    label = (f"#{e.rank} {ep.items[e.index].name}" if e.kind == 'card' else f"insight after {e.rank}")
    out.append((label, f0, round(f0/FPS, 2) if f0 is not None else None))
for o in out: print(o)
json.dump(out, open(r'C:\workspace\micro-drama-platform\ai_videos\paihangbang\episodes\ep11_largest_ships\_build\qc\card_times.json','w'), ensure_ascii=False)
