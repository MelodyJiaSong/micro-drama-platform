# -*- coding: utf-8 -*-
"""规则库体量闸门（ai_video.md 更新协议第 5 条）：开工必读的现行规范超了上限就报警。

    python tools/check_canon.py [--quiet]     # Stop hook 每回合结束跑；超限才说话，退出码 1

现行规范只写现行规则（每条 ≤ 3 行 + 机检指针），来历与事故写进 ai_video_history.md。它一旦长回去，
新会话读不完、读到哪条算哪条——这正是 2026-09-28 把 626 KB 旧文件拆成现行 + 沿革的原因。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CANON = REPO / ".claude" / "agent_refs" / "project" / "ai_video.md"
LIMIT_BYTES = 60_000


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    size = CANON.stat().st_size
    if size > LIMIT_BYTES:
        print(f"⚠ {CANON.relative_to(REPO).as_posix()} {size:,} B > {LIMIT_BYTES:,} B：把来历 / 事故 / 举例挪进 ai_video_history.md，"
              f"单剧教训挪回 specs/ai_video/{{剧}}/lessons.md（更新协议 1–3）")
        return 1
    if not a.quiet:
        print(f"{CANON.name} {size:,} / {LIMIT_BYTES:,} B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
