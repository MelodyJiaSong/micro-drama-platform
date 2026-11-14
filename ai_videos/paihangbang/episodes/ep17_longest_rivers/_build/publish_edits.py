# -*- coding: utf-8 -*-
"""rank_scroll publish 之后的人工补充（可重复执行）。"""
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "publish.md"
s = p.read_text(encoding="utf-8")
s = s.replace("Longest Rivers in the World | Top 50 (2026)\n（43 字符）",
              "Top 50 Longest Rivers in the World (2026) | Nile vs Amazon\n（58 字符）\n\n备选：Longest Rivers in the World | Top 50 (2026)（43 字符）")
s = s.replace("AI-generated (AI-generated (Codex image_gen))", "AI-generated illustration (Codex image_gen), not a photo")
s = s.replace("AI-generated, AI-generated (Codex image_gen)", "AI-generated illustration (Codex image_gen), not a photo")
if "Where other surveys differ" not in s:
    s = s.replace("Flag = country where the river ends (sea, lake or a bigger river).\n",
                  "Flag = country where the river ends (sea, lake or a bigger river).\n"
                  "Where other surveys differ a lot (Salween, Brahmaputra, Mekong…), we list Britannica's figure.\n", 1)
s = s.replace("#LongestRiversInTheWorld #Top50 #Ranking #DataComparison", "#LongestRiversInTheWorld #Nile #Amazon #Geography #Top50 #DataComparison")
if "## 标签（Tags" not in s:
    s += """
## 标签（Tags，逗号分隔）

longest rivers in the world, longest rivers, top 50 rivers, nile vs amazon, longest river in the world, world rivers ranking, river length comparison, yangtze, mississippi missouri, yenisei, geography, data comparison, encyclopaedia britannica, 2026

## 置顶评论说明

- Comment 1（图片署名全文）发布后置顶；Comment 2（逐条数据来源）回复在 Comment 1 下。
- 可另发一条互动评论：「Britannica says the Nile (6,650 km); Brazil's INPE says the Amazon (6,992 km). Which side are you on?」
- 评论区常见问题的回复要点：St. Lawrence（Britannica 无五大湖水系总长，未收）；Pearl / Red River（Britannica 无总长，未收）；Zambezi / Orinoco（Britannica 值为离群值，改用通行值，见描述框）；国旗＝河口所在国。

## 版本与图片（代理补充，2026-11-04 QC 修订后）

- 发布用默认母版 `render/ep17_longest_rivers_master.mp4`：50/50 张卡有图——42 张可商用实拍（Unsplash / Pexels / Pixabay / Flickr CC BY·BY-SA / 巴西旅游部公有领域）+ 8 张 AI 生成插画（卡上有 AI IMAGE 角标）。
- `_with-risk-images` 版为 QC 前旧数据，**不建议发布**（QC M6），未随本轮重渲。
- 含 AI 生成图：上传时勾选合成内容声明。
"""
p.write_text(s, encoding="utf-8")
import re
d = s[s.index("```text") + 7:]; d = d[:d.index("```")]
s = re.sub(r"## Description（\d+ / 5000 字符）", f"## Description（{len(d.strip())} / 5000 字符）", s)
p.write_text(s, encoding="utf-8")
print("description chars", len(d.strip()))
