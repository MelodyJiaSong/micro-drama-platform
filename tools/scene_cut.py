# -*- coding: utf-8 -*-
"""剪辑（试行，follow-up 060）：按一场的剪辑决定文件把各镜的条接成一条片。

    python tools/scene_cut.py annotate <集目录> <场> [镜头…]   # 每条写 annotation.json（逐词台词、内切、冻帧、黑帧、响度）
    python tools/scene_cut.py check    <剪辑决定.json>          # 只核对：条在不在、sha 对不对、入出点、切点离词、镜长统计
    python tools/scene_cut.py render   <剪辑决定.json>          # 照决定渲染（干净版 + 标注版），回读核对后把结果写回 output 段

剪辑模块（.agents/skills/ai-videos-pipeline/modules/edit.md）还是设计稿，本工具只实现其中「先标注再挑、决定是数据、
渲染只照它出、回读核对」的最小部分，数据格式随模块设计再定，不作为最终格式。

草稿剪辑与正片剪辑分开放（follow-up 061）：
    `{场目录}/edit/draft/cut_v{N}.json`   草稿剪辑：只用各镜 drafts/ 里的 480p 草稿条，看结构、节奏、缺什么
    `{场目录}/edit/final/cut_v{N}.json`   正片剪辑：只用各镜 renders/ 里的 720p 正式条，走向锁片
    成片 `{场}_{draft|final}_v{N}.mp4` 与 `_标注` 版放在同一目录（不进 git）。
剪辑决定：
    stage      draft / final，须与所在目录一致；phase 写剪到哪一步（初接 / 粗剪 / 精剪 / 锁片）
    events[]   按播放顺序；镜头事件 {shot, take, sha256, in, out, reason, notes[]}，入出点单位秒、对齐到帧；
               可选 audio_in / audio_out（同一条的声音区间，缺省同画面）：声音与画面保持同步，区间比画面长的部分
               压到相邻镜头的画面上——J 剪辑（声音先进）用 audio_in < in，L 剪辑（声音拖后）用 audio_out > out；
               同一镜可拆成几个事件（如把一段反应挪到别处）；word_cut_ok（理由）放行识别器时间不准造成的「切在词中间」
               可选 grade {gamma, brightness, contrast, saturation, reason}：整段统一调亮度 / 反差（ffmpeg eq），对齐同场参考镜
               缺镜占位 {shot, placeholder: true, duration, reason, text[]}，渲染成写着缺什么的黑卡，静音
    spec       输出规格（宽高、帧率、采样率、临时响度目标 LUFS）
    status     草稿 / 批准（批准只由用户写）；base_version 防并行会话互相覆盖
场与场怎么接（转场菜单、J/L、片头片尾、转场样片）见 `tools/episode_cut.py`。
标注 `annotation.json` 放在条目录里（与 review.md 同处）；台词用 faster-whisper（MIT 许可，需 `pip install faster-whisper`），
不把剧本台词喂给识别器，免得把模型改掉的词「认」成剧本。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FONT = "C:/Windows/Fonts/msyh.ttc"
STAGES = ("draft", "final")
GRADE_KEYS = ("gamma", "brightness", "contrast", "saturation")   # 事件可选 grade：ffmpeg eq 的这几项
TAKE_DIR = {"draft": "drafts", "final": "renders"}     # 草稿剪辑只用草稿条，正片剪辑只用正式条


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ff(args: list[str]) -> str:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit("ffmpeg 失败：%s\n%s" % (" ".join(args[:6]), r.stderr[-1500:]))
    return r.stderr


def probe(p: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,avg_frame_rate,nb_frames,sample_rate",
                        "-of", "json", str(p)], capture_output=True, text=True)
    return json.loads(r.stdout)


def take_video(take_dir: Path) -> Path:
    return next(f for f in take_dir.glob("*.mp4"))


# ---------- annotate ----------

def annotate(ep: Path, scene: str, shots: list[str]) -> None:
    from faster_whisper import WhisperModel  # 只有标注需要
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    root = ep / "scenes" / scene / "shots"
    dirs = sorted((d for d in root.glob("st*/drafts/2*") if d.is_dir()), key=lambda d: (int(d.parent.parent.name[2:]), d.name))
    dirs += sorted((d for d in root.glob("st*/renders/2*") if d.is_dir()), key=lambda d: (int(d.parent.parent.name[2:]), d.name))
    for td in dirs:
        if shots and td.parent.parent.name not in shots:
            continue
        out = td / "annotation.json"
        vid = take_video(td)
        digest = sha256(vid)
        if out.is_file() and json.loads(out.read_text(encoding="utf-8")).get("sha256") == digest:
            continue
        segs, _ = model.transcribe(str(vid), language="en", word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
        words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2), "p": round(w.probability, 2)}
                 for s in segs for w in (s.words or [])]
        dur = float(probe(vid)["format"]["duration"])
        sc = ff(["-i", str(vid), "-vf", "scdet=threshold=12", "-f", "null", "-"])
        fr = ff(["-i", str(vid), "-vf", "freezedetect=n=0.003:d=0.4", "-map", "0:v", "-f", "null", "-"])
        bl = ff(["-i", str(vid), "-vf", "blackdetect=d=0.05:pix_th=0.10", "-an", "-f", "null", "-"])
        rec = {
            "take": td.name, "video": vid.name, "sha256": digest, "duration": round(dur, 3),
            "annotated_at": datetime.now().isoformat(timespec="seconds"), "asr": "faster-whisper small.en，未喂剧本",
            "transcript": " ".join(w["w"] for w in words), "words": words,
            "scene_changes": [[float(t), float(s)] for s, t in re.findall(r"lavfi\.scd\.score: ([\d.]+), lavfi\.scd\.time: ([\d.]+)", sc)],
            "freezes": [[float(a), float(b)] for a, b in re.findall(r"freeze_start: ([\d.]+).*?freeze_end: ([\d.]+)", fr, re.S)],
            "blacks": [[float(a), float(b)] for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bl)],
        }
        out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        print("标注", td.parent.parent.name, td.name, "|", rec["transcript"][:120])


# ---------- check ----------

def load_cut(path: Path) -> tuple[dict, Path]:
    """(剪辑决定, 场目录)；文件须在 `{场}/edit/{draft|final}/`，且 stage 与目录一致。"""
    cut = json.loads(path.read_text(encoding="utf-8"))
    stage = cut.get("stage")
    if stage not in STAGES or path.parent.name != stage or path.parent.parent.name != "edit":
        raise SystemExit("剪辑决定要放在 {场}/edit/draft/ 或 edit/final/，stage 与目录一致：%s（stage=%s）" % (path, stage))
    return cut, path.parent.parent.parent


def take_dir(scene_dir: Path, ev: dict, stage: str) -> Path:
    d = scene_dir / "shots" / ev["shot"] / TAKE_DIR[stage] / ev["take"]
    if not d.is_dir():
        raise SystemExit("找不到条：%s %s（%s剪辑只用 %s/ 里的条）" % (ev["shot"], ev["take"], "草稿" if stage == "draft" else "正片", TAKE_DIR[stage]))
    return d


def check(path: Path, quiet: bool = False) -> list[str]:
    cut, scene_dir = load_cut(path)
    fps = cut["spec"]["fps"]
    problems, lines, lens, spans = [], [], [], []
    t = 0.0
    for ev in cut["events"]:
        if ev.get("placeholder"):
            lines.append("%6.2f  %-5s 缺镜占位 %.1fs  %s" % (t, ev["shot"], ev["duration"], ev.get("reason", "")))
            t += ev["duration"]; lens.append(ev["duration"]); continue
        td = take_dir(scene_dir, ev, cut["stage"])
        vid = take_video(td)
        if ev.get("sha256") and sha256(vid) != ev["sha256"]:
            problems.append("%s：视频 sha256 与决定里记的不符（条被换过）" % ev["shot"])
        ann = json.loads((td / "annotation.json").read_text(encoding="utf-8")) if (td / "annotation.json").is_file() else {}
        dur = ann.get("duration") or float(probe(vid)["format"]["duration"])
        a, b = ev["in"], ev["out"]
        aa, ab = ev.get("audio_in", a), ev.get("audio_out", b)
        if not (0 <= a < b <= dur + 1e-3):
            problems.append("%s：入出点 %.2f–%.2f 超出条长 %.2f" % (ev["shot"], a, b, dur))
        if not (0 <= aa < ab <= dur + 1e-3):
            problems.append("%s：声音区间 %.2f–%.2f 超出条长 %.2f" % (ev["shot"], aa, ab, dur))
        if abs(a * fps - round(a * fps)) > 1e-3 or abs(b * fps - round(b * fps)) > 1e-3:
            problems.append("%s：入出点没对齐到帧（%s fps）" % (ev["shot"], fps))
        spans.append((t + aa - a, t + ab - a, ev["shot"],
                      [{"w": w["w"], "ts": t + max(w["s"], aa) - a, "te": t + min(w["e"], ab) - a}
                       for w in ann.get("words", []) if w["e"] > aa and w["s"] < ab]))
        g = ev.get("grade") or {}
        if g and (set(g) - set(GRADE_KEYS) - {"reason"} or not g.get("reason")):
            problems.append("%s：grade 只能写 %s，并写 reason" % (ev["shot"], " / ".join(GRADE_KEYS)))
        if not ev.get("reason"):
            problems.append("%s：没有理由" % ev["shot"])
        cutw = []
        for w in ann.get("words", []):
            for edge, name in ((aa, "声音入"), (ab, "声音出")):
                if w["s"] + 0.03 < edge < w["e"] - 0.03:
                    cutw.append("%s点切在词「%s」中间" % (name, w["w"]))
        kept = [w["w"] for w in ann.get("words", []) if w["s"] >= aa - 0.05 and w["e"] <= ab + 0.05]
        dropped = [w["w"] for w in ann.get("words", []) if w["e"] < aa or w["s"] > ab]
        if cutw and ev.get("word_cut_ok"):      # 识别器把静音并进了词里，人核对过：写明理由放行
            cutw = []
        if cutw:
            problems.append("%s：%s" % (ev["shot"], "；".join(cutw)))
        free = [f for f in ann.get("scene_changes", []) if a < f[0] < b]
        if free:
            problems.append("%s：可用段内检出内切 %s" % (ev["shot"], free))
        jl = (" 声%5.2f–%5.2f" % (aa, ab)) if (aa, ab) != (a, b) else ""
        lines.append("%6.2f  %-5s %s %5.2f–%5.2f (%4.1fs)%s  台词：%s%s" % (
            t, ev["shot"], ev["take"][-8:], a, b, b - a, jl, " ".join(kept)[:90] or "—",
            ("  | 剪掉：" + " ".join(dropped)) if dropped else ""))
        t += b - a; lens.append(b - a)
    for i, (s0, e0, sh0, w0) in enumerate(spans):
        for s1, e1, sh1, w1 in spans[i + 1:]:
            hit = [(x["w"], y["w"]) for x in w0 for y in w1 if x["ts"] < y["te"] and y["ts"] < x["te"]]
            if hit:
                problems.append("%s 与 %s 的台词在时间线上撞在一起：%s" % (sh0, sh1, hit[:3]))
    real = [x for x, ev in zip(lens, cut["events"]) if not ev.get("placeholder")]
    stats = "总长 %.1fs，%d 个事件（缺镜占位 %d），平均镜长 %.1fs，最长 %.1fs" % (
        t, len(lens), len(lens) - len(real), (sum(real) / len(real)) if real else 0, max(real) if real else 0)
    if not quiet:
        print("\n".join(lines)); print(stats)
        print("问题：" + ("无" if not problems else "")); [print("  - " + p) for p in problems]
    return problems


# ---------- render ----------

def loudness(vid: Path, a: float, b: float) -> float:
    err = ff(["-ss", "%.3f" % a, "-to", "%.3f" % b, "-i", str(vid), "-vn", "-af", "ebur128", "-f", "null", "-"])
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else -70.0


def card(ev: dict, size: tuple[int, int], out: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", size, (16, 16, 16)); d = ImageDraw.Draw(im)
    big, small = ImageFont.truetype(FONT, 26), ImageFont.truetype(FONT, 17)
    d.text((40, 40), "缺镜 %s · %ss" % (ev["shot"], ev["duration"]), fill=(240, 200, 80), font=big)
    d.text((40, 82), ev.get("reason", ""), fill=(170, 170, 170), font=small)
    y = 125
    for para in ev.get("text", []):
        line = ""
        for ch in para:
            if d.textlength(line + ch, font=small) > size[0] - 80:
                d.text((40, y), line, fill=(225, 225, 225), font=small); y += 25; line = ""
            line += ch
        d.text((40, y), line, fill=(225, 225, 225), font=small); y += 33
    im.save(out)


def render(path: Path) -> None:
    if check(path, quiet=True):
        check(path); raise SystemExit("先修好决定文件里的问题再渲染")
    cut, scene_dir = load_cut(path)
    sp = cut["spec"]; W, H, fps, ar = sp["width"], sp["height"], sp["fps"], sp["audio_rate"]
    target = sp.get("loudness_target_lufs", -20.0)
    stem = "%s_v%s" % (cut["stage"], cut["version"])
    tmp = Path(tempfile.mkdtemp(prefix="cut_"))
    venc = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(fps), "-an"]
    parts = {"clean": [], "label": []}
    gains, clips = [], []          # clips：(时间线位置, wav)
    t = 0.0
    for i, ev in enumerate(cut["events"]):
        if ev.get("placeholder"):
            png = tmp / ("card%02d.png" % i); card(ev, (W, H), png)
            for kind in parts:
                o = tmp / ("%s%02d.mp4" % (kind, i))
                ff(["-loop", "1", "-framerate", str(fps), "-i", str(png), "-t", "%.3f" % ev["duration"],
                    "-vf", "format=yuv420p", *venc, str(o), "-y"])
                parts[kind].append(o)
            gains.append(None); t += ev["duration"]; continue
        vid = take_video(take_dir(scene_dir, ev, cut["stage"]))
        a, b = ev["in"], ev["out"]
        aa, ab = ev.get("audio_in", a), ev.get("audio_out", b)
        lu = loudness(vid, aa, ab)
        g = 0.0 if lu < -45 else max(-10.0, min(10.0, target - lu))
        gains.append(round(g, 1))
        fade = 0.02
        wav = tmp / ("a%02d.wav" % i)
        ff(["-ss", "%.3f" % aa, "-i", str(vid), "-t", "%.3f" % (ab - aa), "-vn",
            "-af", "aresample=%d,aformat=channel_layouts=stereo,volume=%.1fdB,afade=t=in:d=%.2f,afade=t=out:st=%.3f:d=%.2f"
            % (ar, g, fade, ab - aa - fade, fade), "-c:a", "pcm_s16le", str(wav), "-y"])
        clips.append((t + aa - a, wav))
        base = "scale=%d:%d:flags=lanczos,setsar=1,fps=%d" % (W, H, fps)
        if ev.get("grade"):          # 整段统一的一次调整（不逐帧重估，免得闪），对齐同场参考镜的亮度
            base += ",eq=" + ":".join("%s=%s" % (k, ev["grade"][k]) for k in GRADE_KEYS if k in ev["grade"])
        label = "%s · %s · %.2f–%.2f" % (ev["shot"], ev["take"][-8:], a, b)
        dt = ("drawtext=fontfile='%s':text='%s':x=10:y=10:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=4"
              % (FONT.replace(":", "\\:"), label.replace(":", "\\:")))
        for kind, vf in (("clean", base), ("label", base + "," + dt)):
            o = tmp / ("%s%02d.mp4" % (kind, i))
            ff(["-ss", "%.3f" % a, "-i", str(vid), "-t", "%.3f" % (b - a), "-vf", vf, *venc, str(o), "-y"])
            parts[kind].append(o)
        t += b - a
    total = t
    # 声音：各段按与画面同步的位置铺到时间线上再混（J/L 剪辑的声音压到相邻画面上）
    mix = tmp / "mix.wav"
    ins, fc = ["-f", "lavfi", "-t", "%.3f" % total, "-i", "anullsrc=r=%d:cl=stereo" % ar], []
    for k, (pos, wav) in enumerate(clips, start=1):
        ins += ["-i", str(wav)]
        ms = max(0, int(round(pos * 1000)))
        fc.append("[%d:a]adelay=%d|%d[d%d]" % (k, ms, ms, k))
    fc.append("[0:a]" + "".join("[d%d]" % k for k in range(1, len(clips) + 1))
              + "amix=inputs=%d:normalize=0:duration=first[m]" % (len(clips) + 1))
    script = tmp / "mix.txt"; script.write_text(";".join(fc), encoding="utf-8")
    ff([*ins, "-/filter_complex", str(script), "-map", "[m]", "-c:a", "pcm_s16le", str(mix), "-y"])
    outs = {}
    for kind, files in parts.items():
        lst = tmp / ("%s.txt" % kind)
        lst.write_text("".join("file '%s'\n" % f.as_posix() for f in files), encoding="utf-8")
        vtmp = tmp / ("%s_v.mp4" % kind)
        ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vtmp), "-y"])
        name = "%s_%s%s.mp4" % (scene_dir.name, stem, "" if kind == "clean" else "_标注")
        o = path.parent / name
        ff(["-i", str(vtmp), "-i", str(mix), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
            "-shortest", "-movflags", "+faststart", str(o), "-y"])
        outs[kind] = o
    # 回读核对
    expect = sum(ev["duration"] if ev.get("placeholder") else ev["out"] - ev["in"] for ev in cut["events"])
    result = {"rendered_at": datetime.now().isoformat(timespec="seconds"), "expected_s": round(expect, 3), "files": {}}
    for kind, o in outs.items():
        pr = probe(o)
        v = next(s for s in pr["streams"] if s["codec_type"] == "video")
        dur = float(pr["format"]["duration"])
        bl = ff(["-i", str(o), "-vf", "blackdetect=d=0.1:pix_th=0.05", "-an", "-f", "null", "-"])
        result["files"][kind] = {"path": o.name, "sha256": sha256(o), "duration_s": round(dur, 3), "frames": int(v.get("nb_frames", 0)),
                                 "size": "%sx%s" % (v["width"], v["height"]), "fps": v["avg_frame_rate"],
                                 "black_segments": re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bl),
                                 "duration_ok": abs(dur - expect) < 0.25}
    result["audio_gain_db"] = gains
    cut["output"] = result
    path.write_text(json.dumps(cut, ensure_ascii=False, indent=1), encoding="utf-8")
    for kind, f in result["files"].items():
        print(kind, f["path"], f["duration_s"], "s（应 %.2f）" % expect, f["frames"], "帧", f["size"], f["fps"],
              "时长对" if f["duration_ok"] else "时长不对", "黑段", f["black_segments"] or "无")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("annotate"); a.add_argument("ep"); a.add_argument("scene"); a.add_argument("shots", nargs="*")
    c = sub.add_parser("check"); c.add_argument("cut")
    r = sub.add_parser("render"); r.add_argument("cut")
    args = ap.parse_args()
    if args.cmd == "annotate":
        annotate(Path(args.ep), args.scene, args.shots)
    elif args.cmd == "check":
        sys.exit(1 if check(Path(args.cut)) else 0)
    else:
        render(Path(args.cut))


if __name__ == "__main__":
    main()
