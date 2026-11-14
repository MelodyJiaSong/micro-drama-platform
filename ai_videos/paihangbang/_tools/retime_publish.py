# -*- coding: utf-8 -*-
"""时间轴变了（如滚动速度改动，follow-up 068）后，就地改发布稿里的章节时间与时长，保留人工润色过的章节标签。

    python ai_videos/paihangbang/_tools/retime_publish.py <期> [<期> ...]

- publish.md：「Chapters:」后的「M:SS 标签」行按新时间轴逐行换时间（条数须与新算的一致，不一致就报告、不改）；
  清单里「时长 X 分钟」与各节字符数随之更新。
- publish.zh.md：连续的「M:SS 标签」章节块同样换时间；「时长 M:SS」更新。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "projects" / "rank_scroll"))
sys.path.insert(0, str(HERE))
from rank_scroll.contract import load_episode  # noqa: E402
from rank_scroll.publish import _ts, chapters  # noqa: E402
from rank_scroll.timeline import build  # noqa: E402
from regate_publish import recount  # noqa: E402
from upload import episode  # noqa: E402

CH = re.compile(r"^(\d+:\d\d) (.+)$")


def retime_blocks(text: str, times: list[str]) -> tuple[str, list[str]]:
    """每个连续的章节行块（≥ 3 行、首行 0:00）按顺序换时间。返回 (新文本, 问题)。"""
    lines, probs, i = text.split("\n"), [], 0
    while i < len(lines):
        if CH.match(lines[i]) and lines[i].startswith("0:00 "):
            j = i
            while j < len(lines) and CH.match(lines[j]):
                j += 1
            if j - i >= 3:
                if j - i != len(times):
                    probs.append(f"第 {i + 1} 行起的章节块 {j - i} 条，新时间轴算出 {len(times)} 条，未改")
                else:
                    for k in range(i, j):
                        lines[k] = f"{times[k - i]} {CH.match(lines[k]).group(2)}"
            i = j
        else:
            i += 1
    return "\n".join(lines), probs


def main() -> None:
    for arg in sys.argv[1:]:
        ep = episode(arg)
        msgs = []
        for lang, fname in (("en", "publish.md"), ("zh", "publish.zh.md")):
            p = ep / fname
            if not p.is_file() or (lang == "zh" and not (ep / "data.zh.json").is_file()):
                continue
            e, _ = load_episode(ep, lang=lang)
            tl = build(e)
            times = [_ts(t) for t, _ in chapters(e, tl)]
            t = p.read_text(encoding="utf-8")
            t, probs = retime_blocks(t, times)
            mins = tl.duration / 60
            t = re.sub(r"时长 \d+(?:\.\d+)? 分钟", f"时长 {mins:.1f} 分钟", t)
            t = re.sub(r"时长 \d+:\d\d", f"时长 {int(tl.duration // 60)}:{int(tl.duration % 60):02d}", t)
            if lang == "en":
                desc = re.search(r"## Description（(\d+) / 5000 字符）\n\n```text\n(.*?)\n```", t, flags=re.S)
                if desc:
                    t = t.replace(desc.group(0), desc.group(0).replace(f"（{desc.group(1)} / 5000", f"（{len(desc.group(2))} / 5000", 1))
                t = recount(t)
            p.write_text(t, encoding="utf-8")
            msgs.append(f"{fname} {tl.duration:.1f}s 章节 {len(times)} 条" + (f"；⚠ {'；'.join(probs)}" if probs else ""))
        print(ep.name, "：", "；".join(msgs))


if __name__ == "__main__":
    main()
