"""QC: per-card centre-arrival times and generator chapters for ep15 (read-only)."""
import sys
sys.path.insert(0, r"C:\workspace\micro-drama-platform\projects\rank_scroll")
from pathlib import Path
from rank_scroll.contract import load_episode
from rank_scroll.timeline import build, FPS, SPEED, W
from rank_scroll.publish import chapters, _arrive_s, _ts

ep_dir = Path(r"C:\workspace\micro-drama-platform\ai_videos\paihangbang\episodes\ep15_deepest_lakes")
for risk in (False, True):
    try:
        ep, _w = load_episode(ep_dir, allow_risk_images=risk)
    except TypeError:
        ep, _w = load_episode(ep_dir)
    tl = build(ep)
    print("risk" if risk else "default", "duration", tl.duration, "frames", tl.total_frames)
    print([(n, a / FPS, b / FPS) for n, a, b in tl.segments])
    if risk: break
    for e in tl.elements:
        name = ep.items[e.index].name if e.kind == "card" else ep.insights[e.index].text[:40]
        # time when element centre reaches screen centre; and time when it enters at right edge
        def t_at(x):
            if x <= tl.cam_start: return tl.f_intro / FPS
            const_end = tl.cam_start + SPEED * tl.f_const
            if x <= const_end:
                return (tl.f_intro + tl.f_hold + (x - tl.cam_start) / SPEED) / FPS
            return None
        tc = t_at(e.center)
        te = t_at(e.center - W // 2 - e.slot // 2)
        print(f"{e.kind:7s} #{e.rank:2d} {name[:40]:40s} enter={te and _ts(te)} ({te and round(te,1)}) centre={tc and _ts(tc)} ({tc and round(tc,1)})")
    print("generator chapters:")
    for t, lab in chapters(ep, tl):
        print(f"  {_ts(t)} {lab}  ({t:.2f})")
