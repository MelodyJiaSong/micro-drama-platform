# -*- coding: utf-8 -*-
"""rank_scroll publish 之后的人工补充（可重跑）：AI 图署名措辞、合成内容声明、描述补充、标签与置顶说明。
python -I finish_publish.py  （先 python -m rank_scroll publish <ep> [--allow-risk-images]）"""
from pathlib import Path

P = Path(__file__).parent.parent / "publish.md"
t = P.read_text(encoding="utf-8")
t = t.replace("0:00 Intro & #30–#21", "0:00 Intro & #35–#21")   # 审片第 5 条：N = 35
t = t.replace("AI-generated (AI-generated (Codex image_gen))", "AI-generated illustration (Codex image_gen)")
t = t.replace("AI-generated, AI-generated (Codex image_gen)", "AI-generated illustration (Codex image_gen), not a photo of the real waterfall")
t = t.replace("- [ ] 「Altered or synthetic content」：本片无 AI 生成的逼真画面 → 选 No",
              "- [ ] 「Altered or synthetic content」：**本片含 AI 生成的逼真瀑布画面（默认版 25 张 / 风险版 12 张，卡上黄色「AI IMAGE」标记）→ 选 Yes**（follow-up 016）")
t = t.replace("Sources: World Waterfall Database, Guinness, IGN Peru, USGS\nPer-item",
              "Sources: World Waterfall Database, Guinness, IGN Peru, USGS\n"
              "Note: many of these falls are remote and have never been photographed under a free licence. Where no usable photo exists, "
              "the card shows an AI-generated illustration (labelled on screen) — it is not a photo of the real waterfall.\nPer-item")
t = t.replace("#TallestWaterfallsInTheWorld #Top35 #Ranking #DataComparison",
              "#TallestWaterfallsInTheWorld #Waterfalls #AngelFalls #Geography #Top35 #Ranking")

# 2026-11-04 复核小修：描述首段加 AI 说明；清单写明当前图片构成与封面
t = t.replace("Every number on screen is sourced (per-item links in the pinned comment). Which one surprised you? Tell us in the comments!",
              "Every number on screen is sourced (per-item links in the pinned comment). Which one surprised you? Tell us in the comments!\n"
              "Some images are AI-generated illustrations, marked AI IMAGE on screen.")
import re as _re
t = _re.sub(r"- \[ \] 「Altered or synthetic content」：[^\n]*",
            "- [ ] 「Altered or synthetic content」：**选 Yes**。默认版 35 张卡 = 10 张实拍 + 25 张 AI 生成图（卡上黄色「AI IMAGE」标记 + 「AI-generated image, not a photo」署名）；封面 #3 Mattenbach 是 AI 图，已加同款「AI IMAGE」角标（`_build/thumb_ai_label.py`，原图 `render/thumbnail_raw.png`）", t)
t = t.replace("封面用 `render/thumbnail.png` 或人工改版", "封面用 `render/thumbnail.png`（#1 Angel、#2 Tugela 为实拍，#3 为 AI 图并已标记）")

extra = """
## 人工补充（代理 2026-11-03，`_build/finish_publish.py`）

- **含 AI 生成图**：上传时在「Altered or synthetic content」勾选 Yes（合成内容声明）；描述框已写明。
- 标签（Tags，逗号分隔）：tallest waterfalls in the world, tallest waterfalls, highest waterfalls, angel falls, tugela falls, waterfall height comparison, world waterfall database, norway waterfalls, geography ranking, top 35
- 置顶评论另加一句（放在 Comment 1 最前面）：
  `Angel Falls or Tugela? Guinness lists Angel at 979 m, but that adds rapids below its 807 m main drop. Count only Angel's 807 m main drop and Tugela (948 m) is #1. Which do you count?`
- 风险版（`render/ep20_tallest_waterfalls_master_with-risk-images.mp4`）若选用：重跑 `python -m rank_scroll publish <ep> --allow-risk-images` 再跑本脚本；风险图多为「All rights reserved」，需逐张取得许可（见 `_build/handoff.md`）。
"""
if "## 人工补充" not in t:
    t = t.rstrip() + "\n" + extra
P.write_text(t, encoding="utf-8")
print("publish.md finished")
