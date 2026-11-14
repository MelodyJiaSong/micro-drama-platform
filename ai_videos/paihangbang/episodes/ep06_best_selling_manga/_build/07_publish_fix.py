# -*- coding: utf-8 -*-
"""ep06：`python -m rank_scroll publish <ep> --allow-risk-images` 之后跑，改成封面适用的措辞（审片 #20 #21）。幂等。"""
import re
from pathlib import Path
p = Path(__file__).resolve().parents[1] / "publish.md"
s = p.read_text(encoding="utf-8")
HEAD = "> 由 `python -m rank_scroll publish` 生成；上传前人工检查。上传由用户亲手做。"
if HEAD in s:
    s = s.replace(HEAD, "> 由 `python -m rank_scroll publish --allow-risk-images` 生成，再经 `_build/07_publish_fix.py` 改成封面措辞；上传前人工检查。上传由用户亲手做。\n"
                  "> 封面均为版权作品（licence unknown），用带图版还是默认版由用户发布前决定（follow-up 014）。")
s = s.replace("Every number on screen is sourced and cross-checked.",
              "Every number on screen comes from a published figure, with its year shown on the card.")
s = s.replace("Image credits (resized and cropped, no other changes):",
              "Cover art (© the respective creators and publishers; shown to identify each series):")
s = s.replace("Full photo credits (author, licence, licence link, source file):",
              "Cover art credits (© creator / publisher) and where each cover image was taken from:")
s = s.replace("full photo credits", "full image credits")
s = s.replace("#Best-sellingMangaOfAllTime", "#BestSellingManga #Manga")   # 审片 2 轮：连字符会截断 hashtag
s = re.sub(r" \((unknown|禁無断複写転載|All rights reserved\.)[^\n]*\)$", "", s, flags=re.M)
s = re.sub(r", (unknown|禁無断複写転載|All rights reserved\.)[^—\n]* — ", " — ", s)
# 审片 #21-③：来源评论里不留内部笔记
s = re.sub(r" \((dead link[^)]*|text seen via[^)]*)\)", "", s)
s = s.replace("Ritsumeikan Univ. lecture PDF cited by Wikipedia", "Ritsumeikan Univ. lecture notes (2012), as cited by Wikipedia")
MUSIC = "Music: original instrumental made for this video with Suno (paid plan)."
if MUSIC not in s:
    s = s.replace("Icons: Tabler Icons (MIT) · Font: Inter (SIL OFL 1.1)", "Icons: Tabler Icons (MIT) · Font: Inter (SIL OFL 1.1)\n" + MUSIC, 1)
CHK = "- [ ] 配乐为 Suno 生成（job b3cf1124…，一首曲子中段重复 28 小节补足长度）：不要把它登记进 Content ID（bible §5）；被误认领时用 request_log.md 申诉"
if CHK not in s and "## Upload checklist" in s:
    s = s.replace("## Upload checklist\n", "## Upload checklist\n\n" + CHK + "\n", 1)
p.write_text(s, encoding="utf-8")
print("unknown left:", s.count("unknown"), "| notes left:", len(re.findall(r"dead link|search snippet", s)))
