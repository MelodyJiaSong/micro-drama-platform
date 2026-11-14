# -*- coding: utf-8 -*-
"""体型对照：从人物卡的「体型 / 年龄 / 种族」一行提取身高，出一张一眼看完的对比图与表。

用法（仓库根目录）：
    python tools/scale_table.py <剧名>              # 写 ai_videos/{剧}/scale_table.{md,png}
    python tools/scale_table.py <剧名> --keys c60_Chaos_Knight m1_Treant   # 只看这几个（技能出片前用）

为什么从卡派生、不另建一张表（dota_yingxiong follow-up 266）
----------------------------------------------------------
用户：「所有人的体型对比，一开始就要设计好」。身高本来就写在每张人物卡里（148 张有），
另建一张手工表＝同一个数字两个出处，必然漂（rule 4i ①）。所以卡是唯一出处，本脚本只读卡、出对比视图；
**改体型＝改卡**，再重跑本脚本。读不出身高的卡列为「待补」——出片前闸门 `spec.scale_table` 会拦住用到它们的技能。
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROW = re.compile(r"\|\s*体型\s*/\s*年龄\s*/\s*种族\s*\|\s*([^|\n]+)\|")
CN = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
REF_HUMAN = 1.8


@dataclass(frozen=True)
class Height:
    key: str
    name: str
    meters: float | None
    kind: str                  # 身高 / 肩高 / 常人
    raw: str
    card: str


def cn_meters(s: str) -> float | None:
    """「两米四」→2.4，「一米八」→1.8，「三米」→3.0。"""
    m = re.search(r"([一二两三四五六七八九])米([一二三四五六七八九])?", s)
    if not m:
        return None
    return CN[m.group(1)] + (CN[m.group(2)] / 10 if m.group(2) else 0.0)


def parse(text: str) -> tuple[float | None, str]:
    shoulder = re.search(r"肩高\s*约?\s*([0-9.]+)\s*(?:m|米)", text)
    if shoulder:
        return float(shoulder.group(1)), "肩高"
    for pat in (r"(?:身高|高)\s*约?\s*([0-9.]+)\s*(?:m|米)", r"约\s*([0-9.]+)\s*(?:m|米)(?!\s*长)"):
        m = re.search(pat, text)
        if m and "体长" not in text[max(0, m.start() - 3):m.start()]:
            return float(m.group(1)), "身高"
    cm = re.search(r"约?\s*([0-9.]+)\s*(?:厘米|cm)(?:高)?", text)
    if cm and not re.search(r"(?:m|米)(?![a-z])", text.replace("厘米", "")):
        return float(cm.group(1)) / 100, "身高"
    cn = cn_meters(text)
    if cn is not None:
        return cn, "身高"
    if "常人" in text:
        return REF_HUMAN, "常人"
    return None, ""


def cards(drama: str) -> dict[str, Path]:
    base = REPO / "ai_videos" / drama
    return {p.stem: p for p in base.glob("**/characters/**/*.md") if p.stem == p.parent.name and re.match(r"^[cm]\d+_", p.stem)}


def height_of(key: str, path: Path) -> Height:
    text = path.read_text(encoding="utf-8")
    title = next((ln.lstrip("# ").strip() for ln in text.splitlines() if ln.startswith("# ")), key)
    row = ROW.search(text)
    raw = row.group(1).strip() if row else ""
    meters, kind = parse(raw) if raw else (None, "")
    return Height(key, title.split("·")[0].strip() or key, meters, kind, raw, path.relative_to(REPO).as_posix())


def heights(drama: str, keys: list[str] | None = None) -> list[Height]:
    found = cards(drama)
    wanted = keys or sorted(found)
    return [height_of(k, found[k]) if k in found else Height(k, k, None, "", "（没有人物卡）", "") for k in wanted]


def write_png(rows: list[Height], out: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont
    known = sorted((r for r in rows if r.meters), key=lambda r: r.meters or 0)
    if not known:
        return
    top = max(max(r.meters or 0 for r in known), REF_HUMAN) * 1.1
    W, H, base, colw = max(900, 70 * len(known) + 120), 640, 560, 70
    img = Image.new("RGB", (W, H), (250, 249, 245))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("msyh.ttc", 14)
    except OSError:
        font = ImageFont.load_default()
    px = (base - 60) / top
    y_ref = base - REF_HUMAN * px
    d.line([(60, y_ref), (W - 20, y_ref)], fill=(59, 130, 246), width=1)
    d.text((62, y_ref - 18), f"常人 {REF_HUMAN} m", fill=(59, 130, 246), font=font)
    for i, r in enumerate(known):
        x = 90 + i * colw
        h = (r.meters or 0) * px
        d.rectangle([x, base - h, x + 40, base], fill=(120, 113, 108) if r.kind != "肩高" else (161, 98, 7))
        d.text((x, base - h - 18), f"{r.meters:g}m", fill=(31, 41, 55), font=font)
        d.text((x - 6, base + 6), r.name[:5], fill=(31, 41, 55), font=font)
    d.text((60, 14), "体型对照（从人物卡派生；棕＝肩高）", fill=(31, 41, 55), font=font)
    img.save(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("drama")
    ap.add_argument("--keys", nargs="*")
    a = ap.parse_args(argv)
    rows = heights(a.drama, a.keys)
    if a.keys:
        for r in rows:
            print(f"{r.key:28} {r.name:10} {f'{r.meters:g} m（{r.kind}）' if r.meters else '待补'}  {r.raw[:40]}")
        return 0 if all(r.meters for r in rows) else 1
    out = REPO / "ai_videos" / a.drama
    lines = ["# 体型对照（**由 tools/scale_table.py 从人物卡派生，不要手改**；改体型＝改卡后重跑）", "",
             f"常人参照 {REF_HUMAN} m；肩高＝四足生物。读不出身高的卡在最后「待补」。", "",
             "| 键 | 名字 | 高度 | 与常人比 | 卡里的原文 |", "|---|---|---|---|---|"]
    for r in sorted((r for r in rows if r.meters), key=lambda r: -(r.meters or 0)):
        lines.append(f"| {r.key} | {r.name} | {r.meters:g} m（{r.kind}） | {(r.meters or 0) / REF_HUMAN:.2f}× | {r.raw[:50]} |")
    todo = [r for r in rows if not r.meters]
    if todo:
        lines += ["", f"## 待补（{len(todo)}）", ""] + [f"- {r.key} {r.name}：{r.raw[:50] or '卡里没有「体型 / 年龄 / 种族」行'}" for r in todo]
    (out / "scale_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_png(rows, out / "scale_table.png")
    print(f"体型对照：{len(rows) - len(todo)} 张卡有身高，{len(todo)} 张待补 → {out.relative_to(REPO)}/scale_table.{{md,png}}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
