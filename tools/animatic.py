# -*- coding: utf-8 -*-
"""整集 animatic：出片前用现成的图 + 字幕按镜长把一集拼出来，先看节奏再花钱出片（ai_video.md rule 44）。

    python tools/animatic.py <剧> <ep>            # → {ep}_animatic.mp4 + {ep}_animatic.segments.json + animatic/animatic.json
    python tools/animatic.py <剧> <ep> --check    # animatic 与当前分镜结构、与 viewing_animatic/review.md 还对不对得上

每镜每个分镜段一张图：已出片的镜直接用成片（animatic 随出片逐步变成成片）；没出片的按
`keyframe/k{段号}.png` → previz 在段中点的一帧 → 参考行里第一张场景图 → 纯色底 取图，印上镜号、段、景别与动作摘要；
台词按时间窗烧字幕（tools/post/subs.py 同一套样式）；已出片的镜带它自己的声音，其余静音。
结构指纹 ＝ 每镜时长 + 分镜段 + 台词（人 / 句 / 时间窗）：prompt 措辞改了不作废，镜长、分段、台词改了才要重拼重审。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
for _p in (REPO / "tools", REPO / "tools" / "post", REPO / "tools" / "previz"):
    sys.path.insert(0, str(_p))
import post_common as pc  # noqa: E402
import prompt_compact  # noqa: E402
import seedance_kit  # noqa: E402
import subs  # noqa: E402
from planstyle import font  # noqa: E402

SUB = "animatic"
MANIFEST = "animatic.json"
REVIEW_DIR = "viewing_animatic"
REVIEW = "review.md"
SHA_TAG = "视频 sha256:"
FPS = 24
FENCE = "`" * 3
IMAGE = (".png", ".jpg", ".jpeg", ".webp")


@dataclass(frozen=True)
class Frame:
    a: int
    b: int
    head: str
    summary: str
    src: Path | None
    how: str
    t: float | None = None      # 从视频里取帧时的秒数


def design_block(md: Path) -> str:
    m = re.search(FENCE + r"text\n(.*?)\n" + FENCE, md.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit(f"{md} 没有设计稿 text 块")
    return m.group(1)


def duration(md: Path) -> float:
    secs = pc.md_duration(md)
    if secs is None:
        raise SystemExit(f"{md} 缺 front matter duration_s")
    return secs


def rendered(d: Path) -> bool:
    """这一镜用成片：有 shotNN.mp4 且不是旧片（md 改了时长、片没重出的旧片退回分镜卡并警告）。"""
    mp4 = pc.shot_mp4(d)
    if not mp4.is_file():
        return False
    why = pc.stale_take(pc.shot_md(d), mp4)
    if why:
        pc.warn(f"{why}；animatic 这一镜改用分镜卡")
    return why is None


def structure(epd: Path) -> dict:
    out = {}
    for d in pc.shot_dirs(epd):
        md = pc.shot_md(d)
        secs = duration(md)
        segs = [(s.a, s.b, s.head) for s, _ in prompt_compact.timeline(design_block(md), secs)]
        lines = [(ln.speaker, ln.text, ln.t0, ln.t1) for ln in pc.dialogue(md)]
        out[d.name] = {"dur": secs, "segs": segs, "lines": lines}
    return out


def fingerprint(epd: Path) -> str:
    return hashlib.sha256(json.dumps(structure(epd), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _first_scene_image(md: Path) -> Path | None:
    for line in md.read_text(encoding="utf-8").split("\n"):
        u = seedance_kit.UPLOAD.match(line)
        if u and u.group("rel") and "场景" in u.group("label"):
            p = (md.parent / u.group("rel")).resolve()
            if p.suffix.lower() in IMAGE and p.is_file():
                return p
    return None


def _readable(video: Path) -> bool:
    """别的会话正在渲的 previz（moov 还没写）读不了，跳到下一个图源。"""
    if not video.is_file():
        return False
    try:
        return pc.probe(video).v_dur > 0
    except SystemExit:
        return False


def frames(d: Path) -> list[Frame]:
    md = pc.shot_md(d)
    secs = duration(md)
    previz = d / "previz" / f"{d.name}_previz.mp4"
    has_pv = _readable(previz)
    scene = _first_scene_image(md)
    plan = d / "planning" / f"{d.name}_overhead_ref.png"
    out = []
    for i, (s, acts) in enumerate(prompt_compact.timeline(design_block(md), secs), 1):
        summary = "；".join(acts)[:160]
        key = d / "keyframe" / f"k{i}.png"
        mid = (s.a + s.b) / 2
        if key.is_file():
            out.append(Frame(s.a, s.b, s.head, summary, key, "首帧图"))
        elif has_pv:
            out.append(Frame(s.a, s.b, s.head, summary, previz, "previz", mid))
        elif scene:
            out.append(Frame(s.a, s.b, s.head, summary, scene, "场景图"))
        elif plan.is_file():
            out.append(Frame(s.a, s.b, s.head, summary, plan, "平面图"))
        else:
            out.append(Frame(s.a, s.b, s.head, summary, None, "无图"))
    return out


def _grab(video: Path, t: float, out: Path) -> Path:
    pc.run([pc.FFMPEG, "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", out])
    return out


def _card(fr: Frame, shot: str, i: int, w: int, h: int, work: Path) -> Path:
    img = Image.new("RGB", (w, h), (18, 18, 20))
    src = fr.src
    if src is not None and fr.t is not None:
        src = _grab(src, fr.t, work / f"{shot}_k{i}_src.png")
    if src is not None:
        pic = Image.open(src).convert("RGB")
        pic.thumbnail((w, h))
        img.paste(pic, ((w - pic.width) // 2, (h - pic.height) // 2))
    dr = ImageDraw.Draw(img)
    f1, f2 = font(max(18, h // 30), bold=True), font(max(14, h // 42))
    rows, cur = [], ""
    for ch in fr.summary:
        if f2.getlength(cur + ch) > w - 32:
            rows.append(cur)
            cur = ""
        cur += ch
    rows = (rows + [cur])[:3]
    band = 16 + f1.size + len(rows) * (f2.size + 4)
    dr.rectangle([0, 0, w, band], fill=(0, 0, 0))
    dr.text((16, 8), f"{shot} · 镜头{i} · {fr.a}–{fr.b}秒 · {fr.head}（{fr.how}）", font=f1, fill=(255, 220, 120))
    for k, r in enumerate(rows):
        dr.text((16, 12 + f1.size + k * (f2.size + 4)), r, font=f2, fill=(235, 235, 235))
    out = work / f"{shot}_k{i}.png"
    img.save(out)
    return out


def shot_clip(d: Path, w: int, h: int, work: Path) -> Path:
    """一镜一条（逐镜落盘、输入没变就跳过）：已出片用成片；否则每段一张卡、按段长摆，配静音音轨。"""
    out = work / f"{d.name}.mp4"
    md, mp4 = pc.shot_md(d), pc.shot_mp4(d)
    secs = duration(md)
    scale = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p"
    if rendered(d):
        sig = pc.signature([mp4], w=w, h=h, how="成片")
        if not pc.fresh(out, sig):
            has_a = pc.probe(mp4).has_audio
            pc.run([pc.FFMPEG, "-y", "-i", mp4] + ([] if has_a else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"])
                   + ["-vf", scale, "-map", "0:v", "-map", "0:a" if has_a else "1:a", "-c:v", "libx264", "-crf", "23",
                      "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest", out])
            pc.stamp(out, sig)
        return out
    frs = frames(d)
    srcs = [f.src for f in frs if f.src is not None]
    sig = pc.signature([md] + srcs, w=w, h=h, how=[f.how for f in frs])
    if pc.fresh(out, sig):
        return out
    cards = [_card(f, d.name, i, w, h, work) for i, f in enumerate(frs, 1)]
    lst = work / f"{d.name}.txt"
    lst.write_text("".join(f"file '{c.name}'\nduration {f.b - f.a}\n" for c, f in zip(cards, frs))
                   + f"file '{cards[-1].name}'\n", encoding="utf-8")
    pc.run([pc.FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lst.name, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-vf", scale, "-t", f"{secs:.3f}", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "23",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", out.name], cwd=work)
    pc.stamp(out, sig)
    return out


def build(epd: Path) -> Path:
    work = epd / SUB
    work.mkdir(exist_ok=True)
    dirs = pc.shot_dirs(epd)
    segs, t = [], 0.0
    for d in dirs:
        secs = duration(pc.shot_md(d))
        segs.append(pc.Seg(d.name, t, secs))
        t += secs
    w, h = subs.canvas(epd, segs)
    clips = [shot_clip(d, w, h, work) for d in dirs]
    segs = [pc.Seg(s.shot, sum(pc.probe(c).v_dur for c in clips[:k]), pc.probe(c).v_dur) for k, (s, c) in enumerate(zip(segs, clips))]
    lst = work / "all.txt"
    lst.write_text("".join(f"file '{c.name}'\n" for c in clips), encoding="utf-8")
    raw = work / f"{epd.name}_animatic_raw.mp4"
    pc.run([pc.FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lst.name, "-c", "copy", raw.name], cwd=work)
    out = epd / f"{epd.name}_animatic.mp4"
    has_zh = any(ln.zh for d in dirs for ln in pc.dialogue(pc.shot_md(d)))
    subs.burn(raw, out, epd, segs, "both" if has_zh else "src", subs.FONT, work / f"{epd.name}_animatic.ass")
    pc.write_segments(epd / f"{epd.name}_animatic.segments.json", segs, approx=False)
    (work / MANIFEST).write_text(json.dumps({"structure": fingerprint(epd), "video_sha256": pc.sha256(out),
                                             "built_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                                             "shots": {d.name: [f.how for f in frames(d)] if not rendered(d) else ["成片"]
                                                       for d in dirs}}, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def problems(epd: Path) -> list[str]:
    """出片前闸门（seedance_kit open 调）：animatic 要在、要跟得上当前分镜结构、要被整集观感审过这一版。"""
    man = epd / SUB / MANIFEST
    video = epd / f"{epd.name}_animatic.mp4"
    if not (man.is_file() and video.is_file()):
        return [f"{epd.name} 还没有 animatic：python tools/animatic.py <剧> {epd.name}"]
    m = json.loads(man.read_text(encoding="utf-8"))
    out = []
    if m.get("structure") != fingerprint(epd):
        out.append("animatic 过期（镜长 / 分镜段 / 台词改过）：重跑 tools/animatic.py 并重审")
    review = epd / REVIEW_DIR / REVIEW
    tag = re.search(re.escape(SHA_TAG) + r"\s*([0-9a-f]{64})", review.read_text(encoding="utf-8")) if review.is_file() else None
    if not tag:
        out.append(f"animatic 还没审：跑 python tools/viewing_packet.py <剧> {epd.name} --video {video.name}，再按 ai_videos__整集观感 出 {REVIEW_DIR}/{REVIEW}")
    elif tag.group(1) != m.get("video_sha256"):
        out.append(f"{REVIEW_DIR}/{REVIEW} 审的是旧版 animatic：重审")
    return out


def main() -> int:
    pc.utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("drama")
    ap.add_argument("ep")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    epd = pc.ep_dir(pc.drama_root(a.drama), pc.ep_name(a.ep))
    if a.check:
        bad = problems(epd)
        print("\n".join(bad) if bad else "animatic 与当前分镜一致，且已审过")
        return 1 if bad else 0
    print(build(epd))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
