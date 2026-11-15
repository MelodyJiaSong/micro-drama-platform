# -*- coding: utf-8 -*-
"""场故事板（follow-up 336）：把一场里各镜组的镜组板切成每镜一格，按镜头顺序从左到右铺开，每格配文字与时间范围。

    python tools/scene_board.py <集目录> [sN]        # 建 / 更新（只在来源变了时重画）
    python tools/scene_board.py <集目录> --check     # 只报告哪些场的故事板过期

它只给人和代理 review（图、时长、顺序），**不上传**给视频模型。产物在 `scenes/sN/board/`：
    `p01_st1.jpg` …          每镜一格（从镜组板切出来；镜组板第 i 格对应镜组第 i 个镜头）
    `scene_board.json`       每格的镜头、镜组、图、文字、起止秒，以及来源指纹（镜组板 sha256 + 本场分镜）
    `scene_board.png`        整场一张图：每格图片在上、文字在下、底部标「0–8 秒」，从左到右、每行 4 格往下排
镜组板是 N 格网格：N ≤ 4 按 2×2，更多按 3 列；格间留白在切图时去掉一圈。没写镜组的单镜用它的首帧图 `shots/stN/planning/stN_first_frame.png` 当一格（chuanyue_yiri follow-up 020）；两样都没有的画一张「还没有故事板」的占位格。
`tools/shot_pack.py sync` 每次同步资料包后顺带更新（Kimi Stop hook 每回合跑），所以改了镜组板，场故事板一定跟着更新。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOARD_DIR = "board"
INDEX = "scene_board.json"
STRIP = "scene_board.png"
GROUP_BOARD = "board.png"
FIRST_FRAME = "{shot}_first_frame.png"   # 单镜的首帧图（prompts-generate.md「重试与搁置」）
PANEL_W, PANEL_H = 640, 360
INSET = 0.012                        # 去掉格间留白
FONT = "C:/Windows/Fonts/msyh.ttc"
VERSION = 3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def grid(n: int) -> tuple[int, int]:
    return (2, 2) if n <= 4 else (3, math.ceil(n / 3))


def panels(scene: dict, ep_dir: Path) -> list[dict]:
    """每镜一项：所属镜组、镜组板路径与格号、起止秒。没写镜组的镜头自成一组（没有镜组板）。"""
    group_of = {}
    for g in scene.get("groups", []):
        for i, sid in enumerate(g["shots"]):
            group_of[sid] = (g["id"], i, len(g["shots"]))
    out, t = [], 0
    for shot in scene["shots"]:
        gid, idx, n = group_of.get(shot["id"], (None, 0, 1))
        board = ep_dir / "scenes" / scene["id"] / "groups" / gid / GROUP_BOARD if gid else None
        if board is None:   # 单镜：用它的首帧图当这一格（chuanyue_yiri follow-up 020）；首帧图也会作为该镜第一张参考上传
            board = ep_dir / "scenes" / scene["id"] / "shots" / shot["id"] / "planning" / FIRST_FRAME.format(shot=shot["id"])
        out.append({"shot": shot["id"], "group": gid, "cell": idx, "cells": n, "start": t, "end": t + shot["duration"],
                    "board": board if board and board.is_file() else None,
                    "text": shot["beats"], "action": shot["action"], "dialogue": shot["dialogue"]})
        t += shot["duration"]
    return out


def source(scene: dict, items: list[dict]) -> str:
    boards = sorted({str(i["board"]) for i in items if i["board"]})
    return fingerprint({"v": VERSION, "scene": scene, "boards": {Path(b).relative_to(REPO).as_posix(): sha256(Path(b)) for b in boards}})


def cut(board: Path, cell: int, cells: int):
    from PIL import Image
    im = Image.open(board).convert("RGB")
    if cells == 1:            # 单镜首帧图：整张就是这一格
        return im.resize((PANEL_W, PANEL_H))
    cols, rows = grid(cells)
    w, h = im.width / cols, im.height / rows
    x, y = (cell % cols) * w, (cell // cols) * h
    box = (x + w * INSET, y + h * INSET, x + w * (1 - INSET), y + h * (1 - INSET))
    return im.crop(tuple(round(v) for v in box)).resize((PANEL_W, PANEL_H))


def placeholder():
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (PANEL_W, PANEL_H), (40, 44, 52))
    ImageDraw.Draw(im).text((PANEL_W // 2, PANEL_H // 2), "还没有故事板", fill=(170, 176, 186), anchor="mm",
                            font=ImageFont.truetype(FONT, 28))
    return im


def strip(items: list[dict], images: list, out: Path, per_row: int = 4) -> None:
    """整场图：每格图在上、文字在下、底部时间，从左到右、每行 per_row 格往下换行（不用横向滚动）。镜组用顶部色条区分。"""
    from PIL import Image, ImageDraw, ImageFont
    font, bold = ImageFont.truetype(FONT, 20), ImageFont.truetype(FONT, 24)
    lines = [textwrap.wrap(i["text"], 30)[:9] for i in items]
    text_h = 30 * max((len(x) for x in lines), default=1) + 20
    pad, bar = 16, 8
    cell_h = bar + PANEL_H + 12 + text_h + 48
    cols = min(per_row, max(len(items), 1))
    rows = math.ceil(len(items) / cols) if items else 1
    W = pad + cols * (PANEL_W + pad)
    H = pad + rows * (cell_h + pad)
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)
    palette = [(37, 99, 235), (217, 119, 6), (5, 150, 105), (190, 24, 93), (124, 58, 237)]
    groups = list(dict.fromkeys(i["group"] or i["shot"] for i in items))
    for k, (item, im, text) in enumerate(zip(items, images, lines)):
        x = pad + (k % cols) * (PANEL_W + pad)
        top = pad + (k // cols) * (cell_h + pad)
        d.rectangle((x, top, x + PANEL_W, top + bar), fill=palette[groups.index(item["group"] or item["shot"]) % len(palette)])
        canvas.paste(im, (x, top + bar))
        y = top + bar + PANEL_H + 12
        for line in text:
            d.text((x, y), line, fill=(33, 48, 71), font=font)
            y += 30
        label = "%d–%d 秒 · %s · %s" % (item["start"], item["end"], item["shot"], ("镜组 " + item["group"]) if item["group"] else "单镜")
        d.text((x, top + cell_h - 40), label, fill=(7, 89, 133), font=bold)
    canvas.save(out)


def build(ep_dir: Path, scene: dict, force: bool = False) -> bool:
    folder = ep_dir / "scenes" / scene["id"] / BOARD_DIR
    items = panels(scene, ep_dir)
    src = source(scene, items)
    index = folder / INDEX
    if not force and index.is_file() and json.loads(index.read_text(encoding="utf-8")).get("source") == src:
        return False
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("p*_st*.jpg"):
        old.unlink()
    images, entries = [], []
    for k, item in enumerate(items, 1):
        im = cut(item["board"], item["cell"], item["cells"]) if item["board"] else placeholder()
        name = "p%02d_%s.jpg" % (k, item["shot"])
        im.save(folder / name, quality=88)
        images.append(im)
        entries.append({"shot": item["shot"], "group": item["group"], "start": item["start"], "end": item["end"],
                        "image": (folder / name).relative_to(REPO).as_posix(), "text": item["text"], "action": item["action"],
                        "dialogue": item["dialogue"],
                        "board": item["board"].relative_to(REPO).as_posix() if item["board"] else None, "cell": item["cell"] + 1})
    strip(items, images, folder / STRIP)
    index.write_text(json.dumps({"scene": scene["id"], "location": scene["location"], "time": scene["time"],
                                 "total": items[-1]["end"] if items else 0, "source": src, "panels": entries},
                                ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return True


def stale(ep_dir: Path, scene: dict) -> bool:
    index = ep_dir / "scenes" / scene["id"] / BOARD_DIR / INDEX
    return not index.is_file() or json.loads(index.read_text(encoding="utf-8")).get("source") != source(scene, panels(scene, ep_dir))


def scenes(ep_dir: Path) -> list[dict]:
    filming = ep_dir / "filming.json"
    return json.loads(filming.read_text(encoding="utf-8"))["content"]["scenes"] if filming.is_file() else []


def sync(ep_dir: Path, quiet: bool = False) -> list[str]:
    """更新本集所有场里**已有镜组板**的场故事板；返回更新了的场。没有任何镜组板的场不画（免得满屏占位格）。"""
    done = []
    for scene in scenes(ep_dir):
        if not scene.get("groups"):
            continue
        if build(ep_dir, scene):
            done.append(scene["id"])
            if not quiet:
                print("  → %s 场故事板已更新" % scene["id"])
    return done


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="场故事板：各镜组板切成每镜一格，从左到右铺开，给人 review")
    ap.add_argument("episode", type=Path)
    ap.add_argument("scene", nargs="?")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    ep = a.episode.resolve()
    targets = [s for s in scenes(ep) if a.scene in (None, s["id"])]
    if a.check:
        bad = [s["id"] for s in targets if s.get("groups") and stale(ep, s)]
        print("过期：%s" % "、".join(bad) if bad else "场故事板都是最新的")
        return 1 if bad else 0
    for s in targets:
        print("  %s %s" % (s["id"], "已更新" if build(ep, s, a.force) else "无变化"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
