# -*- coding: utf-8 -*-
"""ep03 收尾：组装 → 校验 → sources.md → 两版发布文案 → 两版封面 → （可选）两版母版。

    python ai_videos/paihangbang/episodes/ep03_ai_companies/_build/finalize.py [--render] [--music a.mp3 b.mp3]

- 默认版（可商用图）：publish.md、render/thumbnail.png、render/ep03_ai_companies_master.mp4
- 签字版（含许可未知 / 通讯社图，发布前用户签字）：publish_with-risk-images.md、render/thumbnail_with-risk-images.png、
  render/ep03_ai_companies_master_with-risk-images.mp4（ep03 独立审片 B1 / M6）
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
REPO = EP.parents[3]
RS = REPO / "projects" / "rank_scroll"
sys.path.insert(0, str(RS))

from rank_scroll.contract import load_episode  # noqa: E402
from rank_scroll.publish import write  # noqa: E402
from rank_scroll.render import RenderOptions, render_thumb, render_video  # noqa: E402


def run(*args: str) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run([sys.executable, *args], check=True, cwd=REPO)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--music", nargs="*", default=None)
    a = ap.parse_args()
    b = "ai_videos/paihangbang/episodes/ep03_ai_companies/_build"
    run(f"{b}/make_items_def.py")
    run(f"{b}/build.py")
    run(f"{b}/gen_sources.py")
    for risk in (False, True):
        ep, warns = load_episode(EP, strict_images=True, allow_risk_images=risk)
        tag = "_with-risk-images" if risk else ""
        print(f"validate{tag or ' (default)'}: OK, {len(warns)} warnings")
        print(write(ep, EP / f"publish{tag}.md"))
        render_thumb(ep, EP / "render" / f"thumbnail{tag}.png")
        print(EP / "render" / f"thumbnail{tag}.png")
        if a.render:
            out = EP / "render" / f"{ep.episode}_master{tag}.mp4"
            render_video(ep, out, RenderOptions(), [Path(m) for m in a.music] if a.music else None)
            print(out)


if __name__ == "__main__":
    main()
