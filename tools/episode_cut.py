# -*- coding: utf-8 -*-
"""集级剪辑：场与场怎么接（转场工具箱，ai_video_management follow-up 277）。

    python tools/episode_cut.py menu                                  # 列出转场菜单（名称、ffmpeg 实现、用途、时长范围）
    python tools/episode_cut.py check   <集级剪辑决定.json>           # 只核对
    python tools/episode_cut.py join    <集级剪辑决定.json>           # 按决定把各场成片接起来，回读并与应有切点对账
    python tools/episode_cut.py gallery <集级剪辑决定.json> s1 s2 [转场…]   # 在两场交界处把各种转场各出一段样片，接成一条供挑选

菜单是 `.agents/skills/ai-videos-pipeline/modules/edit-transitions.md`「剪辑可做」一栏的实现：只能从菜单里选、每次写理由；
匹配剪辑、遮挡过渡、真正的甩镜要在分镜里设计、两镜各自生成，剪辑做不出来（菜单里的「模拟甩镜」只是近似）。

集级剪辑决定 `{集}/edit/{draft|final}/cut_v{N}.json`：
    scenes[]       {scene, cut_version, sha256}：接哪一版场剪辑（scene_cut.py render 出的干净版）；sha 不符就拒绝
    transitions[]  每对相邻场一条 {from, to, type, duration, audio, reason}
                   type 见菜单；重叠类（叠化、黑场、划像…）让两场重叠 duration 秒，声音同步交叉淡化
                   audio 可选：{"j": 秒}  下一场的声音先进（取下一场第一条在入点之前的原声），
                           {"l": 秒}  上一场的声音拖后（取上一场最后一条在出点之后的原声）；两者只用于切类转场
    head / tail    片头 / 片尾：cut、fade_black、fade_white（淡入 / 淡出，带 duration）
成片 `{集}_{stage}_v{N}.mp4`、样片 `转场样片_{场}_{场}.mp4`（不进 git）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from projects.ai_video_management.libs.common.scene_cut import EDGES as EDGE_MENU, TRANSITIONS
from tools.scene_cut import FONT, STAGES, ff, probe, sha256, take_dir, take_video

MENU = TRANSITIONS          # 菜单只在 libs/common/scene_cut.py 维护一份，界面也读它
EDGES = {k: color for k, (_, color) in EDGE_MENU.items()}
SAMPLE_PAD = 2.5           # 样片里交界两侧各留几秒


def menu() -> None:
    for k, (name, xf, d, mx, use) in MENU.items():
        span = "不重叠" if xf is None else "默认 %.1fs，≤%ds" % (d, mx)
        print("%-13s %-8s %-11s %-16s %s" % (k, name, xf or "—", span, use))
    print("audio：{\"j\": 秒} 下一场声音先进 / {\"l\": 秒} 上一场声音拖后（只配切类）")
    print("head / tail：%s（淡入 / 淡出带 duration）" % "、".join(EDGES))


# ---------- 决定 ----------

def load(path: Path) -> tuple[dict, Path]:
    cut = json.loads(path.read_text(encoding="utf-8"))
    stage = cut.get("stage")
    if stage not in STAGES or path.parent.name != stage or path.parent.parent.name != "edit":
        raise SystemExit("集级剪辑决定要放在 {集}/edit/draft/ 或 edit/final/，stage 与目录一致：%s" % path)
    return cut, path.parent.parent.parent


def check(cut: dict) -> list[str]:
    problems, scenes = [], [s["scene"] for s in cut["scenes"]]
    trans = cut.get("transitions", [])
    if [(t.get("from"), t.get("to")) for t in trans] != list(zip(scenes, scenes[1:])):
        problems.append("transitions 要按顺序给出每一对相邻场（from / to）")
    for t in trans:
        problems += ["%s→%s：%s" % (t.get("from"), t.get("to"), p) for p in transition_problems(t)]
    for k in ("head", "tail"):
        e = cut.get(k, {"type": "cut"})
        if e.get("type") not in EDGES or (e["type"] != "cut" and not 0 < e.get("duration", 0) <= 3):
            problems.append("%s：只能是 %s，淡入淡出要写 0–3 秒 duration" % (k, " / ".join(EDGES)))
    return problems


def transition_problems(t: dict) -> list[str]:
    if t.get("type") not in MENU:
        return ["未知转场 %s（`episode_cut.py menu` 看可选项）" % t.get("type")]
    _, xf, _, mx, _ = MENU[t["type"]]
    out = []
    if xf and not 0 < t.get("duration", 0) <= mx:
        out.append("%s 要写 0–%d 秒的 duration" % (t["type"], mx))
    audio = t.get("audio") or {}
    if set(audio) - {"j", "l"} or any(not 0 < v <= 3 for v in audio.values()):
        out.append("audio 只能写 j / l（0–3 秒）")
    if audio and xf:
        out.append("J / L 只配切类转场（重叠类已经交叉淡化声音）")
    if not t.get("reason"):
        out.append("没有理由")
    return out


def scene_render(ep: Path, stage: str, item: dict) -> tuple[Path, dict]:
    """场的干净版成片与它的剪辑决定；sha 须与集级决定里记的一致（场被重剪过就要重新决定）。"""
    sc_path = ep / "scenes" / item["scene"] / "edit" / stage / ("cut_v%s.json" % item["cut_version"])
    sc = json.loads(sc_path.read_text(encoding="utf-8"))
    out = (sc.get("output") or {}).get("files", {}).get("clean")
    if not out:
        raise SystemExit("%s 还没渲染：先跑 scene_cut.py render %s" % (item["scene"], sc_path))
    vid = sc_path.parent / out["path"]
    if sha256(vid) != out["sha256"] or item.get("sha256") not in (None, out["sha256"]):
        raise SystemExit("%s 的成片和决定里记的 sha256 不一致（场被重剪或重渲染过）" % item["scene"])
    return vid, sc


def spill(ep: Path, sc: dict, stage: str, side: str, secs: float) -> tuple[Path, float, float, float] | None:
    """J / L 要的场外原声：side='j' 取本场第一条入点之前，'l' 取本场最后一条出点之后。返回 (视频, 起, 止, 增益 dB)。"""
    evs = [e for e in sc["events"] if not e.get("placeholder")]
    gains = [g for g, e in zip(sc.get("output", {}).get("audio_gain_db", []), sc["events"]) if not e.get("placeholder")]
    if not evs:
        return None
    i = 0 if side == "j" else -1
    ev = evs[i]
    vid = take_video(take_dir(ep / "scenes" / sc["scene"], ev, stage))
    dur = float(probe(vid)["format"]["duration"])
    a, b = (ev.get("audio_in", ev["in"]) - secs, ev.get("audio_in", ev["in"])) if side == "j" \
        else (ev.get("audio_out", ev["out"]), ev.get("audio_out", ev["out"]) + secs)
    if a < 0 or b > dur + 1e-3:
        raise SystemExit("%s 的 %s 要 %.2f 秒场外原声，但条里不够（%s %.2f–%.2f，条长 %.2f）" % (sc["scene"], side.upper(), secs, ev["shot"], a, b, dur))
    return vid, a, b, (gains[i] if gains else 0.0)


# ---------- 渲染 ----------

def assemble(segs: list[dict], trans: list[dict], head: dict, tail: dict, sp: dict, out: Path,
             label: str | None = None) -> tuple[float, list[float]]:
    """segs：{video, start, dur, inner_cuts[], j, l}（start / dur 是在源成片里的取段；j / l 为 spill() 结果或 None）。
    返回 (总长, 应有切点)。画面用 xfade / concat 串接；声音逐段铺到时间线上再混（交叉淡化、J / L）。"""
    fps, ar = sp["fps"], sp["audio_rate"]
    tmp = Path(tempfile.mkdtemp(prefix="ep_cut_"))
    pos, t, cuts = [], 0.0, []
    for k, s in enumerate(segs):
        if k:
            xf = MENU[trans[k - 1]["type"]][1]
            t -= trans[k - 1]["duration"] if xf else 0.0
            if not xf:
                cuts.append(round(t, 3))
        pos.append(t)
        cuts += [round(t + c, 3) for c in s.get("inner_cuts", [])]
        t += s["dur"]
    total = t
    # 画面
    ins, fc = [], []
    for k, s in enumerate(segs):
        ins += ["-ss", "%.3f" % s["start"], "-t", "%.3f" % s["dur"], "-i", str(s["video"])]
        fc.append("[%d:v]settb=AVTB,fps=%d,format=yuv420p,setpts=PTS-STARTPTS[v%di]" % (k, fps, k))
    cur, acc = "[v0i]", segs[0]["dur"]
    for k in range(1, len(segs)):
        tr = trans[k - 1]; xf = MENU[tr["type"]][1]
        if xf:
            fc.append("%s[v%di]xfade=transition=%s:duration=%.3f:offset=%.3f[v%d]" % (cur, k, xf, tr["duration"], acc - tr["duration"], k))
            acc += segs[k]["dur"] - tr["duration"]
        else:
            fc.append("%s[v%di]concat=n=2:v=1:a=0[v%d]" % (cur, k, k))
            acc += segs[k]["dur"]
        cur = "[v%d]" % k
    post = []
    if head.get("type", "cut") != "cut":
        post.append("fade=t=in:d=%.3f:color=%s" % (head["duration"], EDGES[head["type"]]))
    if tail.get("type", "cut") != "cut":
        post.append("fade=t=out:st=%.3f:d=%.3f:color=%s" % (total - tail["duration"], tail["duration"], EDGES[tail["type"]]))
    if label:
        post.append("drawtext=fontfile='%s':text='%s':x=(w-tw)/2:y=h-60:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=10"
                    % (FONT.replace(":", "\\:"), label.replace(":", "\\:").replace("'", "")))
    fc.append("%s%s[vo]" % (cur, ",".join(post) or "null"))
    # 声音：每段（含 J / L 的场外原声）先出 wav，再按位置铺开混合
    clips = []
    for k, s in enumerate(segs):
        fin = trans[k - 1]["duration"] if k and MENU[trans[k - 1]["type"]][1] else 0.02
        fout = trans[k]["duration"] if k < len(trans) and MENU[trans[k]["type"]][1] else 0.02
        if k == 0 and head.get("type", "cut") != "cut":
            fin = head["duration"]
        if k == len(segs) - 1 and tail.get("type", "cut") != "cut":
            fout = tail["duration"]
        w = tmp / ("a%02d.wav" % k)
        ff(["-ss", "%.3f" % s["start"], "-t", "%.3f" % s["dur"], "-i", str(s["video"]), "-vn", "-af",
            "aresample=%d,aformat=channel_layouts=stereo,afade=t=in:d=%.3f,afade=t=out:st=%.3f:d=%.3f"
            % (ar, fin, s["dur"] - fout, fout), "-c:a", "pcm_s16le", str(w), "-y"])
        clips.append((pos[k], w))
        for side in ("j", "l"):
            if not s.get(side):
                continue
            vid, a, b, g = s[side]
            w = tmp / ("%s%02d.wav" % (side, k))
            fade = "afade=t=in:d=%.3f" % ((b - a) * 0.6) if side == "j" else "afade=t=out:st=0:d=%.3f" % (b - a)
            ff(["-ss", "%.3f" % a, "-i", str(vid), "-t", "%.3f" % (b - a), "-vn", "-af",
                "aresample=%d,aformat=channel_layouts=stereo,volume=%.1fdB,%s" % (ar, g, fade), "-c:a", "pcm_s16le", str(w), "-y"])
            clips.append((pos[k] - (b - a) if side == "j" else pos[k] + s["dur"], w))
    ains = ["-f", "lavfi", "-t", "%.3f" % total, "-i", "anullsrc=r=%d:cl=stereo" % ar]
    afc = []
    for n, (p, w) in enumerate(clips, start=1):
        ains += ["-i", str(w)]
        ms = max(0, int(round(p * 1000)))
        afc.append("[%d:a]adelay=%d|%d[d%d]" % (n, ms, ms, n))
    afc.append("[0:a]" + "".join("[d%d]" % n for n in range(1, len(clips) + 1)) + "amix=inputs=%d:normalize=0:duration=first[m]" % (len(clips) + 1))
    mix = tmp / "mix.wav"; (tmp / "afc.txt").write_text(";".join(afc), encoding="utf-8")
    ff([*ains, "-/filter_complex", str(tmp / "afc.txt"), "-map", "[m]", "-c:a", "pcm_s16le", str(mix), "-y"])
    (tmp / "fc.txt").write_text(";".join(fc), encoding="utf-8")
    ff([*ins, "-i", str(mix), "-/filter_complex", str(tmp / "fc.txt"), "-map", "[vo]", "-map", "%d:a" % len(segs),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(fps),
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out), "-y"])
    return total, cuts


def inner_cuts(sc: dict) -> list[float]:
    x, out = 0.0, []
    for ev in sc["events"][:-1]:
        x += ev["duration"] if ev.get("placeholder") else ev["out"] - ev["in"]
        out.append(round(x, 3))
    return out


def readback(o: Path, total: float, cuts: list[float]) -> dict:
    pr = probe(o); v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    dur = float(pr["format"]["duration"])
    bl = ff(["-i", str(o), "-vf", "blackdetect=d=0.1:pix_th=0.05", "-an", "-f", "null", "-"])
    # 阈值 8：本剧阴天冷灰画面，切点 scdet 分数只有 10–13（ep01 s1→s2 实测），12 会漏
    sc = ff(["-i", str(o), "-vf", "scdet=threshold=8", "-f", "null", "-"])
    found = [float(x) for x in re.findall(r"lavfi\.scd\.time: ([\d.]+)", sc)]
    return {"path": o.name, "sha256": sha256(o), "duration_s": round(dur, 3), "expected_s": round(total, 3),
            "duration_ok": abs(dur - total) < 0.25, "frames": int(v.get("nb_frames", 0)),
            "size": "%sx%s" % (v["width"], v["height"]), "fps": v["avg_frame_rate"],
            "black_segments": re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bl),
            "cuts_expected": cuts, "cuts_found": found,
            "cuts_unexpected": [x for x in found if all(abs(x - c) > 0.1 for c in cuts)],
            "cuts_missed": [c for c in cuts if all(abs(x - c) > 0.1 for x in found)]}


def join(path: Path) -> None:
    cut, ep = load(path)
    problems = check(cut)
    if problems:
        raise SystemExit("集级剪辑决定有问题：\n  - " + "\n  - ".join(problems))
    trans, segs = cut.get("transitions", []), []
    for k, item in enumerate(cut["scenes"]):
        vid, sc = scene_render(ep, cut["stage"], item)
        j = (trans[k - 1].get("audio") or {}).get("j") if k else None
        l = (trans[k].get("audio") or {}).get("l") if k < len(trans) else None
        segs.append({"video": vid, "start": 0.0, "dur": float(probe(vid)["format"]["duration"]), "inner_cuts": inner_cuts(sc),
                     "j": spill(ep, sc, cut["stage"], "j", j) if j else None,
                     "l": spill(ep, sc, cut["stage"], "l", l) if l else None})
    o = path.parent / ("%s_%s_v%s.mp4" % (ep.name, cut["stage"], cut["version"]))
    total, cuts = assemble(segs, trans, cut.get("head", {"type": "cut"}), cut.get("tail", {"type": "cut"}), cut["spec"], o)
    r = readback(o, total, cuts)
    r["rendered_at"] = datetime.now().isoformat(timespec="seconds")
    cut["output"] = r
    path.write_text(json.dumps(cut, ensure_ascii=False, indent=1), encoding="utf-8")
    print(r["path"], r["duration_s"], "s（应 %.2f）" % total, r["frames"], "帧", r["size"], r["fps"],
          "时长对" if r["duration_ok"] else "时长不对", "黑段", r["black_segments"] or "无")
    print("切点：应有", cuts, "| 检出", r["cuts_found"], "| 意外", r["cuts_unexpected"] or "无", "| 漏检", r["cuts_missed"] or "无")


# ---------- 样片 ----------

def gallery(path: Path, a: str, b: str, kinds: list[str]) -> None:
    """交界两侧各 SAMPLE_PAD 秒，每种转场出一段带名字的样片，接成一条；另加片头淡入、片尾淡出与 J / L 的样片。"""
    cut, ep = load(path)
    items = {s["scene"]: s for s in cut["scenes"]}
    (va, sca), (vb, scb) = scene_render(ep, cut["stage"], items[a]), scene_render(ep, cut["stage"], items[b])
    da, db = float(probe(va)["format"]["duration"]), float(probe(vb)["format"]["duration"])
    sp, tmp = cut["spec"], Path(tempfile.mkdtemp(prefix="ep_gallery_"))
    jl = 0.75
    samples = []
    for k in kinds or list(MENU):
        name, xf, d, _, _ = MENU[k]
        samples.append((k, "%s %s%s" % (name, k, "" if not xf else " %.1fs" % d), {"type": k, "duration": d}, None))
        if k == "cut":
            samples.append(("cut_j", "切 + J 声音先进 %.2fs" % jl, {"type": "cut", "audio": {"j": jl}}, None))
            samples.append(("cut_l", "切 + L 声音拖后 %.2fs" % jl, {"type": "cut", "audio": {"l": jl}}, None))
    parts, kept = [], []
    for n, (k, label, tr, _) in enumerate(samples):
        pad = SAMPLE_PAD + (tr.get("duration") or 0) / 2
        try:
            sa = {"video": va, "start": max(0.0, da - pad), "dur": min(pad, da),
                  "l": spill(ep, sca, cut["stage"], "l", tr["audio"]["l"]) if "l" in tr.get("audio", {}) else None}
            sb = {"video": vb, "start": 0.0, "dur": min(pad, db),
                  "j": spill(ep, scb, cut["stage"], "j", tr["audio"]["j"]) if "j" in tr.get("audio", {}) else None}
        except SystemExit as e:          # 条里没有足够的场外原声（如 L 要上一条出点之后的声音）：这一种在本交界做不了
            print("跳过 %s：%s" % (label, e)); continue
        kept.append((k, label, tr, None))
        o = tmp / ("%02d_%s.mp4" % (n, k))
        assemble([sa, sb], [tr], {"type": "cut"}, {"type": "cut"}, sp, o, label)
        parts.append(o)
    for n, (edge, label, seg) in enumerate([("head", "片头 fade_black 淡入 1.0s", {"video": va, "start": 0.0, "dur": 3.0}),
                                            ("tail", "片尾 fade_black 淡出 1.0s", {"video": vb, "start": max(0.0, db - 3.0), "dur": min(3.0, db)})]):
        o = tmp / ("9%d_%s.mp4" % (n, edge))
        e = {"type": "fade_black", "duration": 1.0}
        assemble([seg], [], e if edge == "head" else {"type": "cut"}, e if edge == "tail" else {"type": "cut"}, sp, o, label)
        parts.append(o)
    gap = tmp / "gap.mp4"     # 样片之间 0.5 秒黑，免得把样片之间的接缝当成转场
    ff(["-f", "lavfi", "-i", "color=c=black:s=%dx%d:r=%d:d=0.5" % (sp["width"], sp["height"], sp["fps"]),
        "-f", "lavfi", "-i", "anullsrc=r=%d:cl=stereo" % sp["audio_rate"], "-t", "0.5",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", str(gap), "-y"])
    lst = tmp / "list.txt"
    lst.write_text("".join("file '%s'\nfile '%s'\n" % (p.as_posix(), gap.as_posix()) for p in parts), encoding="utf-8")
    o = path.parent / ("转场样片_%s_%s.mp4" % (a, b))
    ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", str(sp["fps"]), "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(o), "-y"])
    t, index = 0.0, []
    for (k, label, _, _), p in zip(kept + [("head", "片头淡入", 0, 0), ("tail", "片尾淡出", 0, 0)], parts):
        index.append("%5.1fs  %s" % (t, label)); t += float(probe(p)["format"]["duration"]) + 0.5
    (path.parent / ("转场样片_%s_%s.txt" % (a, b))).write_text("\n".join(index) + "\n", encoding="utf-8")
    print(o, "%.1fs" % float(probe(o)["format"]["duration"])); print("\n".join(index))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("menu")
    c = sub.add_parser("check"); c.add_argument("cut")
    j = sub.add_parser("join"); j.add_argument("cut")
    g = sub.add_parser("gallery"); g.add_argument("cut"); g.add_argument("a"); g.add_argument("b"); g.add_argument("kinds", nargs="*")
    args = ap.parse_args()
    if args.cmd == "menu":
        menu()
    elif args.cmd == "check":
        problems = check(load(Path(args.cut))[0])
        print("问题：" + ("无" if not problems else "")); [print("  - " + p) for p in problems]
        sys.exit(1 if problems else 0)
    elif args.cmd == "join":
        join(Path(args.cut))
    else:
        bad = [k for k in args.kinds if k not in MENU]
        if bad:
            raise SystemExit("未知转场 %s（`episode_cut.py menu` 看可选项）" % bad)
        gallery(Path(args.cut), args.a, args.b, args.kinds)


if __name__ == "__main__":
    main()
