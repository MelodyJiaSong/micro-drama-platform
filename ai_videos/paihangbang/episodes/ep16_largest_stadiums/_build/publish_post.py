# -*- coding: utf-8 -*-
"""ep16：rank_scroll publish 生成 publish.md 后的人工补写（标题、AI 署名去重、标签、说明）。python _build/publish_post.py"""
import re
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "publish.md"
s = p.read_text(encoding="utf-8")
s = re.sub(r"Largest Stadiums in the World \| Top 50 \(2026\)\n（\d+ 字符）",
           "Top 50 Largest Stadiums in the World (2026)\n（43 字符；人工定稿。备选：Biggest Stadiums in the World by Seats | Top 50 (2026)，53 字符）", s)
s = s.replace("AI-generated (AI-generated (Codex image_gen))", "AI-generated illustration, not a photo (Codex image_gen)")
s = s.replace("AI-generated, AI-generated (Codex image_gen)", "AI-generated illustration, not a photo (Codex image_gen; no source file)")
s = s.replace("#LargestStadiumsInTheWorld #Top50 #Ranking #DataComparison", "#LargestStadiums #Stadiums #Top50")
if "## Tags（上传时填" not in s:
    s = s.replace("## Upload checklist", """## Tags（上传时填，≤500 字符）

largest stadiums in the world, biggest stadiums, biggest stadium in the world, stadium capacity, largest stadiums 2026, top 50 stadiums, narendra modi stadium, rungrado may day stadium, michigan stadium, beaver stadium, college football stadiums, world cup 2026 stadiums, cricket stadium, football stadium, data ranking

## 人工补充说明（代理 2026-11-04，QC 第 1 轮修改后）

- **含 AI 生成图**：默认版 6 张 Codex 生成图，卡上有黄色「AI IMAGE」角标：3 张「看台球迷背影」示意图（Lusail、Stade de France、Azadi，所在国无商用全景自由）＋ 3 张按资料描述生成的球场外观图（广东奥体、杭州奥体、Atatürk，全网找不到可商用实拍）；**上传时「Altered or synthetic content」选 Yes**。
- 默认版 3 张无图卡：Misr、Borg El Arab、JIS（Photo withheld: no freedom of panorama）。
- 本 publish.md 对应**默认母版**。若用户签字改发风险版，运行 `python -m rank_scroll publish <ep> --allow-risk-images` 后再跑 `python _build/publish_post.py`。
- 置顶评论建议加一句：「Seated capacity only: standing room, temporary stands and record crowds are not counted (Beaver Stadium drew 114,419 on Oct 10, 2026, above its 106,304 official seats). #50 Camp Randall (76,130) edges #51 Empower Field (76,125) by 5 seats per Wisconsin's 2026 game notes.」

## Upload checklist""")
s = s.replace("Every number on screen is sourced (per-item links in the pinned comment).",
              "Every number on screen is sourced (per-item links in the pinned comment). Note: 6 cards marked AI IMAGE use AI-generated images, not photos; 3 of them show real stadiums drawn from public descriptions, so details are not accurate.", 1)
p.write_text(s, encoding="utf-8")
print("publish.md post-edited")
