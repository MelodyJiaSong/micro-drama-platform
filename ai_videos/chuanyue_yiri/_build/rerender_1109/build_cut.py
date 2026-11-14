# -*- coding: utf-8 -*-
"""EP01 11-09 重出后的场剪辑：按分镜顺序，每镜取今天最新一条「保留 / 搁置」的条，入出点取该条 review.md 的剪辑建议。

    python build_cut.py <场> [--dry]

写 scenes/<场>/edit/final/cut_v{N+1}.json（base_version＝上一版）。没有可用条的镜头报出来、不写。
"""
from __future__ import annotations

import glob
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
EP = REPO / "ai_videos/chuanyue_yiri/episodes/ep01"
FPS = 24
INOUT = re.compile(r"(?:剪辑建议入出点|剪辑入出点|应急备用|临时占位|Temporary placeholder)[^0-9]{0,40}?(\d+(?:\.\d+)?)\s*[–\-~]\s*(\d+(?:\.\d+)?)")


def snap(t: float) -> float:
    return round(round(t * FPS) / FPS, 6)


def pick(scene: str, shot: str):
    takes = sorted(t for t in glob.glob(str(EP / f"scenes/{scene}/shots/{shot}/renders/2026*")) if Path(t).name >= "20261109")
    best = None
    for t in reversed(takes):
        rv = Path(t, "review.md").read_text(encoding="utf-8")
        st = re.search(r"^状态：(.+)$", rv, re.M).group(1).strip()
        if st.startswith("已审核（保留") or st.startswith("搁置"):
            best = (Path(t), st, rv)
            break
    if best is None and takes:          # 全是重出：用最新一条当临时占位
        t = takes[-1]
        rv = Path(t, "review.md").read_text(encoding="utf-8")
        best = (Path(t), re.search(r"^状态：(.+)$", rv, re.M).group(1).strip(), rv)
    return best


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    scene, dry = sys.argv[1], "--dry" in sys.argv
    F = json.loads((EP / "filming.json").read_text(encoding="utf-8"))["content"]["scenes"]
    sc = next(s for s in F if s["id"] == scene)
    cut_dir = EP / f"scenes/{scene}/edit/final"
    prev = sorted(cut_dir.glob("cut_v*.json"), key=lambda p: int(re.search(r"v(\d+)", p.name).group(1)))
    base = json.loads(prev[-1].read_text(encoding="utf-8")) if prev else {}
    ver = (base.get("version") or 0) + 1
    events, problems = [], []
    skip = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and not sys.argv[2].startswith("--") else set()
    for sh in sc["shots"]:
        if sh["id"] in skip:
            continue
        got = pick(scene, sh["id"])
        if not got:
            problems.append(f"{sh['id']} 没有今天的条")
            continue
        take, st, rv = got
        g = json.loads((take / "generation.json").read_text(encoding="utf-8"))
        video = take / g["video"]
        dur = float(g.get("duration_s") or sh.get("duration") or 0)
        m = INOUT.search(rv)
        a, b = (float(m.group(1)), float(m.group(2))) if m else (0.0, dur)
        b = min(b, dur)
        note = [f"审片：{st}"]
        if not st.startswith("已审核（保留"):
            note.append("这一条审片未通过（搁置或重出待定），剪辑临时用它，交用户处理")
        events.append({"shot": sh["id"], "take": take.name, "sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
                       "in": snap(a), "out": snap(b),
                       "reason": f"按审片建议入出点 {a}–{b} 秒（2026-11-09 全集按 Riley 新脸重出，follow-up 048）", "notes": note})
    if problems:
        print("✗", "；".join(problems))
    cut = {"scene": scene, "stage": "final", "phase": "粗剪", "version": ver, "base_version": base.get("version"),
           "status": "草稿", "made_at": "2026-11-09", "made_by": "Claude Code",
           "vision": (base.get("vision", "") + f" v{ver}：全场换成 2026-11-09 按 Riley 新脸（F22S）重出的 720p 正式条，入出点取各条审片建议。").strip(),
           "spec": base.get("spec") or {"width": 1280, "height": 720, "fps": 24, "audio_rate": 48000, "loudness_target_lufs": -20.0},
           "有意违例": [], "events": events}
    for e in events:
        print(f"  {e['shot']:5} {e['take']}  {e['in']:6.2f}–{e['out']:6.2f}  {e['notes'][0][:30]}")
    if not dry:
        out = cut_dir / f"cut_v{ver}.json"
        out.write_text(json.dumps(cut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("→", out.relative_to(REPO).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
