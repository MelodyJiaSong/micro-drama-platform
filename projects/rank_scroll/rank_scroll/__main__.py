"""CLI: python -m rank_scroll {validate,timeline,preview,render,thumb} <episode_dir> ..."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .contract import ContractError, load_episode
from .render import RenderOptions, Renderer, render_thumb, render_video
from .timeline import FPS, build, describe


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="rank_scroll")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "timeline", "preview", "render", "thumb", "publish"):
        sp = sub.add_parser(name)
        sp.add_argument("episode_dir")
        sp.add_argument("--strict", action="store_true", help="missing images are errors")
        sp.add_argument("--lang", default="en", help="en（读 data.json）或 zh（读 data.zh.json，大陆中文版；follow-up 015）")
        sp.add_argument("--allow-risk-images", action="store_true",
                        help="include photos flagged image_risk (e.g. no commercial freedom of panorama)")
        if name == "preview":
            sp.add_argument("--t", type=float, nargs="+", required=True, help="times in seconds")
            sp.add_argument("--out-dir", default=None)
            sp.add_argument("--half", action="store_true")
        if name == "render":
            sp.add_argument("--music", nargs="+", default=None,
                            help="audio files crossfaded in order; optional in/out seconds: song.mp3@IN:OUT (e.g. a.mp3@:188)")
            sp.add_argument("--music-fit", choices=("none", "end"), default="none",
                            help="end: if the music is longer than the video, skip the start of the last track so it "
                                 "ends naturally with the video")
            sp.add_argument("--draft", action="store_true", help="960x540 30fps NVENC")
            sp.add_argument("--from", dest="t_from", type=float, default=None)
            sp.add_argument("--to", dest="t_to", type=float, default=None)
            sp.add_argument("--out", default=None)
        if name == "thumb":
            sp.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    ep_dir = Path(a.episode_dir)
    try:
        from . import draw as _D
        _D.LANG = a.lang
        ep, warnings = load_episode(ep_dir, strict_images=a.strict, allow_risk_images=a.allow_risk_images, lang=a.lang)
    except ContractError as e:
        print("CONTRACT ERRORS:", file=sys.stderr)
        for err in e.errors:
            print("  -", err, file=sys.stderr)
        return 2
    for w in warnings:
        print("warning:", w, file=sys.stderr)
    if a.cmd == "validate":
        print(f"OK {ep.episode}: {len(ep.items)} items, {len(ep.insights)} insights, theme {ep.theme}")
        return 0
    if a.cmd == "publish":
        from .publish import write
        print(write(ep))
        return 0
    if a.cmd == "timeline":
        print(describe(build(ep)))
        return 0
    render_dir = ep.root / "render"
    render_dir.mkdir(exist_ok=True)
    if a.cmd == "preview":
        out_dir = Path(a.out_dir) if a.out_dir else render_dir / ("preview" if a.lang == "en" else f"preview_{a.lang}")
        out_dir.mkdir(parents=True, exist_ok=True)
        r = Renderer(ep, RenderOptions(out_scale=0.5 if a.half else 1.0))
        for t in a.t:
            p = out_dir / f"t{t:07.2f}.png"
            r.save_png(int(t * FPS), p)
            print(p)
        return 0
    if a.cmd == "thumb":
        out = Path(a.out) if a.out else render_dir / ("thumbnail.png" if a.lang == "en" else f"thumbnail_{a.lang}.png")
        render_thumb(ep, out)
        print(out)
        return 0
    opts = RenderOptions(out_scale=0.5, step=2, draft=True) if a.draft else RenderOptions()
    suffix = ("draft" if a.draft else "master") + ("_with-risk-images" if a.allow_risk_images else "") + ("" if a.lang == "en" else f"_{a.lang}")
    out = Path(a.out) if a.out else render_dir / f"{ep.episode}_{suffix}.mp4"
    render_video(ep, out, opts, list(a.music) if a.music else None, a.t_from, a.t_to, music_fit=a.music_fit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
