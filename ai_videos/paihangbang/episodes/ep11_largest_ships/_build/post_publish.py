# -*- coding: utf-8 -*-
"""rank_scroll publish 生成 publish.md 后的人工补充（可重跑）：标题、开头句、AI 图署名措辞、标签、描述框标签行。
用法：python post_publish.py <publish.md>"""
import re
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
TITLE = "Biggest Ships in the World 2026 | Top 42 by Gross Tonnage"
s = re.sub(r"## Title\n\n.*\n（\d+ 字符[^）]*）", f"## Title\n\n{TITLE}\n（{len(TITLE)} 字符；备选：The 42 Biggest Ship Classes in 2026, Ranked by Size）", s)
s = re.sub(r"^Biggest Ships in the World — top 42 ranked by gross tonnage \([^)]*\)\.",
           "The 42 biggest ship classes sailing in November 2026, ranked by registered gross tonnage (GT) — one card per class, sister ships share a card.",
           s, count=1, flags=re.M)
s = s.replace("AI-generated (AI-generated (Codex image_gen))", "AI-generated illustration (Codex image_gen), not a photo of the ship")
s = s.replace("AI-generated, AI-generated (Codex image_gen)", "AI-generated illustration (Codex image_gen), not a photo of the ship; no source file")
s = re.sub(r"#BiggestShipsInTheWorld #Top42 #Ranking #DataComparison", "#BiggestShips #ContainerShip #CruiseShip", s)
if "## Tags" not in s:
    s = s.replace("## Comment 1", "## Tags（YouTube 标签栏）\n\n```text\nbiggest ships in the world, largest ships 2026, biggest container ship, largest cruise ship, Icon of the Seas, "
                  "Pioneering Spirit, MSC Irina, Ever Given, Valemax, gross tonnage, ship size comparison, ranking\n```\n\n## Comment 1", 1)
s = re.sub(r"#BiggestShipsInTheWorld #Top42 #Ranking #DataComparison", "#BiggestShips #ContainerShip #CruiseShip", s)
s = s.replace("(unknown)", "(licence unknown)").replace(", unknown —", ", licence unknown —")
p.write_text(s, encoding="utf-8")
print("ok", len(s))
