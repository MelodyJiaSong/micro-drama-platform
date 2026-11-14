"""真实尺度 · 合成（bible §2.2 / §2.4）：渲染帧 + 叠加卡片 → 母版 MP4；可选混入配乐。

    python ai_videos/zhenshi_chidu/_tools/compose.py <集目录> [--music <音频>] [--out render/ep_master.mp4] [--cards _build/cards_zh]

顺序：钩子 → 列队（片头卡、标签卡、人体标签、洞察卡）→ 全体合影 → 来源卡。段间 0.4 s 黑场过渡。
帧来自 render_ep.py（_build/frames/<段>/），卡片来自 cards.py（_build/cards/），时间来自 _build/timeline.json。
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 1920, 1080
FADE = 0.35
MARK = (255, 196, 0)


def _marker(im: Image.Image, m: dict, a: float) -> None:
    """肩高标线：地面点到肩高点（动物中线纵深上的投影），两端短横。"""
    (bx, by), (tx, ty) = m["base"], m["top"]
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    col = MARK + (int(235 * a),)
    sh = (0, 0, 0, int(90 * a))
    for dx, c in ((2, sh), (0, col)):
        d.line([(bx + dx, by + dx), (tx + dx, ty + dx)], fill=c, width=5)
        d.line([(tx - 22 + dx, ty + dx), (tx + 22 + dx, ty + dx)], fill=c, width=5)
        d.line([(bx - 14 + dx, by + dx), (bx + 14 + dx, by + dx)], fill=c, width=5)
    im.alpha_composite(lay)


def _alpha(img: Image.Image, a: float) -> Image.Image:
    if a >= 0.999:
        return img
    r, g, b, al = img.split()
    return Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))


def _ramp(t: float, t0: float, t1: float, fade: float = FADE) -> float:
    if t < t0 or t > t1:
        return 0.0
    return max(0.0, min(1.0, (t - t0) / fade, (t1 - t) / fade))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ep", type=Path)
    ap.add_argument("--music", type=Path)
    ap.add_argument("--out", default="render/ep_master.mp4")
    ap.add_argument("--cards", default="_build/cards", help="叠加卡目录（中文版 _build/cards_zh，由 cards_zh.py 生成）")
    ap.add_argument("--limit-s", type=float, help="只合成前 N 秒（试看）")
    args = ap.parse_args()
    ep = args.ep.resolve()
    tl = json.loads((ep / "_build/timeline.json").read_text(encoding="utf-8"))
    fps = tl["fps"]
    cards = ep / args.cards
    frames = ep / "_build/frames"
    load = lambda n: Image.open(cards / n).convert("RGBA")
    hook, title, sources, group_txt, man = (load("hook.png"), load("title.png"), load("sources.png"),
                                            load("group.png"), load("man_label.png"))
    insights = [load(f"insight_{i}.png") for i in range(len(tl["insights"]))]
    labels = {it["data_index"]: load(f"label_{it['data_index']:02d}.png") for it in tl["items"]}

    plan = []   # (段, 段内帧号, 段长)
    for seg in ("hook", "lineup", "group"):
        a, b = tl["segments"][seg]
        plan += [(seg, i, b - a + 1) for i in range(b - a + 1)]
    n_src = int(tl["sources_s"] * fps)
    plan += [("sources", i, n_src) for i in range(n_src)]
    if args.limit_s:
        plan = plan[: int(args.limit_s * fps)]

    out = ep / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    video_only = out.with_name(out.stem + "_video.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "slow",
                           "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video_only)],
                          stdin=subprocess.PIPE)
    lineup_a = tl["segments"]["lineup"][0]
    for k, (seg, i, n) in enumerate(plan):
        t, dur = i / fps, n / fps
        if seg == "sources":
            im = sources.copy()
        else:
            im = Image.open(frames / seg / f"{i:05d}.jpg").convert("RGBA")
            if im.size != (W, H):
                im = im.resize((W, H))
        if seg == "hook":
            im.alpha_composite(_alpha(hook, _ramp(t, 0.6, dur + 1, 0.6)))
        elif seg == "lineup":
            f = lineup_a + i
            ta, tb = tl["title"]
            im.alpha_composite(_alpha(title, _ramp(f / fps, ta / fps, tb / fps)))
            for it in tl["items"]:
                la, lb = it["label"]
                a = _ramp(f / fps, la / fps + 0.15, lb / fps)
                if a > 0:
                    if it.get("marker"):
                        _marker(im, it["marker"], a)
                    im.alpha_composite(_alpha(labels[it["data_index"]], a))
                    mx, my = it["man_label_xy"]
                    ml = _alpha(man, a)
                    im.alpha_composite(ml, (int(mx - ml.width / 2), int(my - ml.height)))
            for ins in tl["insights"]:
                fa, fb = ins["frames"]
                a = _ramp(f / fps, fa / fps, fb / fps)
                if a > 0:
                    im.alpha_composite(_alpha(insights[ins["index"]], a))
        elif seg == "group":
            a = _ramp(t, 0.8, dur + 1, 0.6)
            im.alpha_composite(_alpha(group_txt, a))
            if tl.get("group_man_label_xy") and a > 0:
                (x0, y0), (x1, y1) = tl["group_man_label_xy"]
                k = i / max(n - 1, 1)
                ml = _alpha(man, a)
                im.alpha_composite(ml, (int(x0 + (x1 - x0) * k - ml.width / 2), int(y0 + (y1 - y0) * k - ml.height)))
        # 段间黑场
        edge = min(t, dur - t - 1 / fps)
        if edge < 0.4 and not (seg == "hook" and t < 0.4):
            im = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, max(0.0, edge / 0.4))
        ff.stdin.write(im.convert("RGB").tobytes())
        if k % 300 == 0:
            print(f"[compose] {k}/{len(plan)}", flush=True)
    ff.stdin.close()
    ff.wait()
    total = len(plan) / fps
    if args.music:
        # 静态增益：先测整段配乐的综合响度，再整体加减到 −14 LUFS；不用动态 loudnorm（会把爬升压平，ep01 第 2 轮审片）
        meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(args.music), "-t", f"{total:.3f}", "-af", "ebur128",
                               "-f", "null", "-"], capture_output=True, text=True).stderr
        lufs = float([ln for ln in meas.splitlines() if ln.strip().startswith("I:")][-1].split()[1])
        gain = -14.0 - lufs
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_only), "-i", str(args.music),
                        "-filter_complex", f"[1:a]atrim=0:{total:.3f},afade=t=in:d=0.5,afade=t=out:st={total - 4:.3f}:d=4,"
                                           f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-ar", "48000", "-shortest", str(out)], check=True)
        video_only.unlink()      # 中间文件，混音后删除
    else:
        video_only.replace(out)
    print(f"[compose] {out} {total:.1f}s")


if __name__ == "__main__":
    main()
