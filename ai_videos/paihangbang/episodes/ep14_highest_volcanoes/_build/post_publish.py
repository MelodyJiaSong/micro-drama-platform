# -*- coding: utf-8 -*-
"""publish.md 人工收尾（由 `python -m rank_scroll publish` 生成后运行）：
标题带年份；AI 生成图署名合并成一行；加合成内容声明；标签；清单改「Altered or synthetic content → Yes」。"""
import re
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "publish.md"
s = P.read_text(encoding="utf-8")
TITLE = "Top 50 Highest Volcanoes in the World (2026)"
s = re.sub(r"## Title\n\n.*\n（\d+ 字符）", f"## Title\n\n{TITLE}\n（{len(TITLE)} 字符）", s)


def merge_ai(block: str, pat: str, head: str) -> str:
    lines = block.split("\n")
    ai = [re.match(r"#(\d+) ", l).group(1) for l in lines if re.search(pat, l)]
    out, done = [], False
    for l in lines:
        if re.search(pat, l):
            if not done:
                out.append(head + ", ".join("#" + n for n in ai))
                done = True
            continue
        out.append(l)
    return "\n".join(out)


s = merge_ai(s.split("## Comment 1")[0], r"^#\d+ .*: AI-generated \(AI-generated", "AI-generated illustrations (made with Codex image_gen, not photos of the real mountain): ") \
    + "## Comment 1" + merge_ai(s.split("## Comment 1")[1], r"^#\d+ .*: AI-generated, AI-generated", "AI-generated illustrations (Codex image_gen, no source photo): ")
s = s.replace("Image credits (resized and cropped, no other changes):",
              "Note: where no freely licensed photo of a remote Andean volcano exists, the card shows an AI-generated illustration (marked on the card).\n\nImage credits (resized and cropped, no other changes):")
s = s.replace("#HighestVolcanoesInTheWorld #Top50 #Ranking #DataComparison",
              "#Volcanoes #HighestVolcanoes #Andes #Top50 #Ranking")
s = s.replace("- [ ] 「Altered or synthetic content」：本片无 AI 生成的逼真画面 → 选 No",
              "- [ ] 「Altered or synthetic content」：**本片含 AI 生成的逼真火山图（默认母版 39 张，卡上署名 AI-generated image）→ 选 Yes**")
if "## Tags" not in s:
    s = s.replace("## Upload checklist", "## Tags\n\nhighest volcanoes in the world, tallest volcanoes, largest volcanoes, volcano ranking, Ojos del Salado, Llullaillaco, Andes volcanoes, Chimborazo, Cotopaxi, Kilimanjaro, active volcanoes, Smithsonian Global Volcanism Program, top 50\n\n## Upload checklist")
if "风险版" not in s:
    s = s.replace("## Upload checklist", "## 版本说明\n\n本文件对应**默认母版**（`render/ep14_highest_volcanoes_master.mp4`）。若用户签字改发 `_with-risk-images` 版，先 `python -m rank_scroll publish <ep> --allow-risk-images` 重生成，再跑 `python _build/post_publish.py`；该版 33 张照片许可不明 / 保留所有权利，须逐张取得许可或确认可用。\n\n## Upload checklist")
import json
EP = P.parent
_d = json.loads((EP / "data.json").read_text(encoding="utf-8")); _A = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}
n_ai = sum(1 for it in _d["items"] if _A[(it.get("image_alt") if it.get("image_risk") else it["image"])]["licence"].startswith("AI"))
line2 = (f"Only volcanoes active in the last ~11,700 years (Smithsonian GVP Holocene list) are ranked. "
         f"{n_ai} of the 50 volcano images are AI-generated illustrations, not photos (marked AI IMAGE on each card).")
s = re.sub(r"Highest Volcanoes in the World — top 50 ranked by .*?\(Smithsonian GVP, Nov 2026\)\.",
           "Highest Volcanoes in the World — the top 50 active (Holocene) volcanoes, ranked by summit elevation (Smithsonian GVP data, Nov 2026).", s, count=1)
s = s.replace("Every number on screen is sourced", line2 + chr(10) + "Every number on screen is sourced", 1)
s = s.replace("本片含 AI 生成的逼真火山图（默认母版 39 张", f"本片含 AI 生成的逼真火山图（默认母版 {n_ai} 张")
s = s.replace("Note: where no freely licensed photo of a remote Andean volcano exists, the card shows an AI-generated illustration (marked on the card).",
              "Note: where no freely licensed photo of a remote Andean volcano exists, the card shows an AI-generated illustration (marked AI IMAGE). Several cards use public-domain NASA astronaut photos taken from the International Space Station.")
s = s.replace("33 张照片许可不明 / 保留所有权利", "32 张照片许可不明 / 保留所有权利")
s = s.replace("卡上标 Illustration / Render", "卡上标黄色 AI IMAGE 徽章")
P.write_text(s, encoding="utf-8")
print("ok")
