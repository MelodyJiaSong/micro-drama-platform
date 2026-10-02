# -*- coding: utf-8 -*-
"""场景图结构审图（follow-up 036：bg177 主厅的石柱只到半墙、柱头上什么都没托，出片才看出来）。

出图后、挂进 shot 之前，Claude 逐张看图过 CHECKLIST，结论写进这张图自己那份 md 的 `审图` 行：

    > **审图**：通过 · 2026-09-27 · 1a2b3c4d5e6f · 备注

结论绑定图片字节（sha256 前 12 位）：图重出了，旧的「通过」自动作废。生成器挂图前调 `gate()`，没审或没过即 blocker。

    python tools/scene_review.py todo <目录或 png ...>          # 列出没审 / 没过 / 审后图变了的
    python tools/scene_review.py set <png> pass|fail "<备注>"   # 看过图后记结论
    python tools/scene_review.py checklist                      # 打印清单
"""
from __future__ import annotations

import datetime
import hashlib
import re
import sys
from pathlib import Path

CHECKLIST = (
    "S1 承重连续：柱子从地面顶到梁或屋架、梁搭在柱或墙上、拱有拱脚；没有半截断掉、悬在空中的构件",
    "S2 通得到：门、楼梯、走道通向说得通的地方；楼梯不撞墙，门不开在半空",
    "S3 不悬空：物件、家具、草木落在地面或支撑物上",
    "S4 尺度对：门高约 2 m、台阶一级约 15–18 cm，门窗家具与人的比例合理",
    "S5 无文字：画面里没有可读文字、水印、logo",
    "S6 对得上：光的方向、时段、天气与卡里写的一致；主要构件的数量与位置不和场地平面图矛盾",
)
LINE = re.compile(r"^> \*\*审图\*\*：(通过|不通过) · (\d{4}-\d{2}-\d{2}) · ([0-9a-f]{12})(?: · (.*))?$", re.M)


def sha12(png: Path) -> str:
    return hashlib.sha256(png.read_bytes()).hexdigest()[:12]


def card_of(png: Path) -> Path:
    """一张场景图一个目录：图与卡同名。"""
    return png.with_suffix(".md")


def status(png: Path) -> tuple[bool, str]:
    """(能不能挂, 原因)。"""
    if not png.is_file():
        return False, "图不存在"
    card = card_of(png)
    m = LINE.search(card.read_text(encoding="utf-8")) if card.is_file() else None
    if not m:
        return False, "没审过图"
    if m.group(3) != sha12(png):
        return False, "审图之后图重出了（%s 审的是 %s，现在是 %s）" % (m.group(2), m.group(3), sha12(png))
    if m.group(1) != "通过":
        return False, "审图不通过：%s" % (m.group(4) or "")
    return True, "通过 · %s" % m.group(2)


def record(png: Path, ok: bool, note: str) -> None:
    card = card_of(png)
    text = card.read_text(encoding="utf-8")
    line = "> **审图**：%s · %s · %s%s" % ("通过" if ok else "不通过", datetime.date.today().isoformat(), sha12(png),
                                        (" · " + note) if note else "")
    if LINE.search(text):
        text = LINE.sub(lambda _m: line, text, count=1)
    else:                                   # 放进卡头的引用块：H1 之后第一行 `> ` 之前
        lines = text.split("\n")
        i = next((k for k, s in enumerate(lines) if s.startswith("> ")), None)
        if i is None:
            i = 1
            lines[i:i] = ["", line]
        else:
            lines[i:i] = [line]
        text = "\n".join(lines)
    card.write_text(text, encoding="utf-8")


def gate(pngs: list[Path]) -> list[str]:
    out = []
    for p in pngs:
        ok, why = status(p)
        if not ok:
            out.append("%s：%s——看图过 scene_review 清单（S1–S6）再挂（follow-up 036）" % (p.name, why))
    return out


def _images(args: list[str]) -> list[Path]:
    out: list[Path] = []
    for a in args:
        p = Path(a)
        if p.suffix == ".png":
            out.append(p)
            continue
        for md in sorted(p.rglob("*.md")):                         # 场景图＝与所在目录同名的 png
            png = md.with_suffix(".png")
            if md.stem == md.parent.name and png.is_file():
                out.append(png)
    return out


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("todo", "set", "checklist"):
        print(__doc__)
        return 2
    if argv[0] == "checklist":
        print("\n".join(CHECKLIST))
        return 0
    if argv[0] == "set":
        png, verdict, note = Path(argv[1]), argv[2], (argv[3] if len(argv) > 3 else "")
        if verdict not in ("pass", "fail"):
            raise SystemExit("结论只能是 pass / fail")
        record(png, verdict == "pass", note)
        print("%s → %s" % (png.name, status(png)[1]))
        return 0
    bad = 0
    for png in _images(argv[1:]):
        ok, why = status(png)
        if not ok:
            bad += 1
            print("✗ %s  %s" % (png, why))
    print("%d 张没审 / 没过" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
