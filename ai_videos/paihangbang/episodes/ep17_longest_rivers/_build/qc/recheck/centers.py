import json, sys
sys.path.insert(0, r'C:/workspace/micro-drama-platform/projects/rank_scroll')
from rank_scroll import contract, timeline as T
ep_dir = r'C:/workspace/micro-drama-platform/ai_videos/paihangbang/episodes/ep17_longest_rivers'
import inspect
fn = [n for n in dir(contract) if n.startswith('load')]
ep, warns = contract.load_episode(ep_dir); print("warnings", warns)
tl = T.build(ep)
out = []
for e in tl.elements:
    # first frame where camera >= centre
    f0 = tl.f_intro
    tgt = e.center
    if tgt <= tl.cam_start:
        t = (tl.f_intro) / 60
    else:
        f = tl.f_intro + tl.f_hold
        while tl.camera(f) < tgt and f < tl.segments[1][2]: f += 1
        t = f / 60
    name = ep.items[e.index].name if e.kind == 'card' else f'INSIGHT after {e.rank}'
    out.append([e.kind, e.rank, name, round(t, 2)])
json.dump(out, open('centers.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('hold', tl.f_hold/60, 'cam_start', tl.cam_start)
for o in out: print(o)
