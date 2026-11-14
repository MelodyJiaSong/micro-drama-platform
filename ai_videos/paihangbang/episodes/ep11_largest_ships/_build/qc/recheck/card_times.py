import sys, json
sys.path.insert(0, r'C:\workspace\micro-drama-platform\projects\rank_scroll')
from pathlib import Path
from rank_scroll.contract import load_episode
from rank_scroll.timeline import build, FPS
EP = Path(r'C:\workspace\micro-drama-platform\ai_videos\paihangbang\episodes\ep11_largest_ships')
ep, _ = load_episode(EP, strict_images=True)
tl = build(ep)
out = []
for e in tl.elements:
    f0 = next((f for f in range(tl.total_frames) if tl.camera(f) >= e.center), None)
    label = (f"#{e.rank} {ep.items[e.index].name}" if e.kind == 'card' else f"insight after {e.rank}")
    out.append((label, f0, round(f0/FPS, 2) if f0 is not None else None))
for o in out: print(o)
print('total_frames', tl.total_frames)
json.dump(out, open(EP / '_build/qc/recheck/card_times.json', 'w', encoding='utf-8'), ensure_ascii=False)
