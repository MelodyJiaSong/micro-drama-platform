# -*- coding: utf-8 -*-
"""卡片版式对比（paihangbang follow-up 055）：同一期、同一时刻，按 layout.card_style 的几种版式各出一帧 / 一段，
再拼一张带标签的对比图，交用户选版式。不改该期的 data.json。

    python ai_videos/paihangbang/_tools/style_compare.py <期目录> --t 30 60 [--clip 20 32] [--styles poster split duo polaroid spotlight]

输出 `<期目录>/_build/style_compare/`：
    <style>_t<秒>.png          单帧（1920×1080）
    grid_t<秒>.jpg             五种版式拼成一张（每格左上角标版式名）
    <style>_clip.mp4           --clip 给出时：该时段 960×540 草稿视频（不带音乐）
    cards_<序号>.png           --cards 给出时：同一张卡五种版式原尺寸并排（看字和排版细节）
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))

from rank_scroll import draw as D  # noqa: E402
from rank_scroll.contract import CARD_STYLES, load_episode  # noqa: E402
from rank_scroll.render import Renderer, RenderOptions, render_video  # noqa: E402
from rank_scroll.timeline import FPS  # noqa: E402

LABELS = {"poster": "A · POSTER (current)", "split": "B · SPLIT", "duo": "C · DUO (main + inset)",
          "polaroid": "D · POLAROID", "spotlight": "E · SPOTLIGHT"}
FONT = "C\\:/Windows/Fonts/arialbd.ttf"


def grid(pngs: list[tuple[str, Path]], out: Path) -> None:
    cols = 2 if len(pngs) <= 4 else 3
    args = ["ffmpeg", "-v", "error", "-y"]
    for _, p in pngs:
        args += ["-i", str(p)]
    chains, names = [], []
    for i, (style, _) in enumerate(pngs):
        lab = LABELS.get(style, style).replace(":", r"\:")
        chains.append(f"[{i}:v]scale=960:540,drawtext=fontfile='{FONT}':text='{lab}':x=18:y=h-th-18:fontsize=34:"
                      f"fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=12[v{i}]")
        names.append(f"[v{i}]")
    n = len(pngs)
    while n % cols:
        chains.append(f"color=c=0x111111:s=960x540:d=1[v{n}]")
        names.append(f"[v{n}]")
        n += 1
    rows = [names[r * cols:(r + 1) * cols] for r in range(n // cols)]
    rnames = []
    for r, row in enumerate(rows):
        chains.append("".join(row) + f"hstack=inputs={cols}[r{r}]")
        rnames.append(f"[r{r}]")
    chains.append("".join(rnames) + f"vstack=inputs={len(rnames)}[out]" if len(rnames) > 1 else f"{rnames[0]}null[out]")
    args += ["-filter_complex", ";".join(chains), "-map", "[out]", "-frames:v", "1", "-q:v", "3", str(out)]
    subprocess.run(args, check=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("episode_dir")
    ap.add_argument("--t", type=float, nargs="+", default=[30.0])
    ap.add_argument("--clip", type=float, nargs=2, default=None, metavar=("FROM", "TO"))
    ap.add_argument("--styles", nargs="+", default=list(CARD_STYLES))
    ap.add_argument("--cards", type=int, nargs="+", default=[], help="按出场序号（rank）出单卡并排对比")
    ap.add_argument("--lang", default="en")
    a = ap.parse_args(argv)
    D.LANG = a.lang
    ep, _ = load_episode(Path(a.episode_dir), lang=a.lang)
    out = ep.root / "_build" / "style_compare"
    out.mkdir(parents=True, exist_ok=True)
    for t in a.t:
        frames = []
        for style in a.styles:
            ep.card_style = style
            p = out / f"{style}_t{t:06.1f}.png"
            Renderer(ep, RenderOptions()).save_png(int(t * FPS), p)
            frames.append((style, p))
        g = out / f"grid_t{t:06.1f}.jpg"
        grid(frames, g)
        print(g)
    for rank in a.cards:
        from rank_scroll.cards import card_image
        from rank_scroll.theme import get_theme
        import skia
        th, _ = get_theme(ep.theme)
        it = next(i for i in ep.items if i.rank == rank)
        imgs = []
        for style in a.styles:
            ep.card_style = style
            imgs.append((style, card_image(ep, it, th, 1.0)))
        w = sum(im.width() for _, im in imgs) + 40 * (len(imgs) + 1)
        h = imgs[0][1].height() + 110
        surf = skia.Surface(w, h)
        c = surf.getCanvas()
        c.clear(skia.Color(20, 22, 28))
        x = 40
        f = D.font(30, "ExtraBold")
        for style, im in imgs:
            c.drawImage(im, x, 0)
            D.text(c, LABELS.get(style, style), x + 36, h - 36, f, D.paint("#ffffff"))
            x += im.width() + 40
        cp = out / f"cards_{rank:02d}.png"
        surf.makeImageSnapshot().save(str(cp), skia.kPNG)
        print(cp)
    if a.clip:
        for style in a.styles:
            ep.card_style = style
            p = out / f"{style}_clip.mp4"
            render_video(ep, p, RenderOptions(out_scale=0.5, step=2, draft=True), None, a.clip[0], a.clip[1])
            print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
