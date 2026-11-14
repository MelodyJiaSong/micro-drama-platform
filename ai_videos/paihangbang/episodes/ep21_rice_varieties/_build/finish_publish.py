# -*- coding: utf-8 -*-
"""ep21：`python -m rank_scroll publish` 生成 publish.md 之后的人工改写（第 1 轮审片 m9 / m10，follow-up 060）。
每次重新生成 publish.md 后再跑一次；幂等。

    python ai_videos/paihangbang/episodes/ep21_rice_varieties/_build/finish_publish.py
"""
import re
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
P = EP / "publish.md"
MUSIC = "Music: original instrumental generated for this channel with Suno (job 112eccdb, clips bf844d85 / 0aabb622)."
AI_LINE = "Images: all 30 rice images are AI-generated illustrations (Codex image_gen), not photos."
INTRO = ("From sticky Japanese mochigome to South Asian basmati and the 'rice' that isn't rice: 30 kinds of rice from around "
         "the world, what makes each one different (grain length, texture, colour, aroma) and where it grows.\n"
         "Not a ranking: a journey from East Asia west to the Americas. Per-item sources are in the replies under the "
         "pinned comment. Which one have you eaten? Tell us in the comments!")
TAGS = ("rice varieties, types of rice, kinds of rice, rice around the world, basmati, jasmine rice, koshihikari, "
        "sticky rice, glutinous rice, black rice, red rice, wild rice, risotto rice, paella rice, carnaroli, bomba rice, "
        "carolina gold rice, african rice, sake rice, food geography")
HASHTAGS = "#Rice #RiceVarieties #FoodGeography"
CONTENT_ID = ("- [ ] 配乐为自家 Suno 生成曲（job 112eccdb）：不登记 Content ID；被第三方认领时用本期 request_log.md 的"
              "生成记录申诉（bible §5）")


def main() -> None:
    s = P.read_text(encoding="utf-8")
    # 1 描述首段
    s = re.sub(r"(## Description[^\n]*\n\n```text\n)(.*?)(\n\nChapters:)", lambda m: m.group(1) + INTRO + m.group(3), s, count=1, flags=re.S)
    # 2 逐张 AI 署名合并成一句
    s = re.sub(r"Image credits \(resized and cropped[^\n]*\n(?:[^\n]+: AI illustration[^\n]*\n)+", AI_LINE + "\n", s)
    # 3 配乐署名
    if "Music: original instrumental" not in s:
        s = s.replace("Flags: flagcdn.com", MUSIC + "\nFlags: flagcdn.com", 1)
    # 4 hashtags
    s = re.sub(r"\n#30KindsOfRice[^\n]*\n", "\n" + HASHTAGS + "\n", s)
    # 5 置顶评论：合并成一句署名 + 指向回复
    s = re.sub(r"(## Comment 1（置顶）[^\n]*\n\n```text\n)(.*?)(\n```)",
               lambda m: m.group(1) + AI_LINE + "\n" + MUSIC + "\nPer-item data sources with links: see the reply below." + m.group(3),
               s, count=1, flags=re.S)
    # 5b Ofada 出处如实写成 Wikipedia 转引（qc M3），不冒充专著
    s = re.sub(r"Ofada Rice: Gyimah-Brempong[^\n]*?(https://en\.wikipedia\.org/wiki/Ofada_rice)",
               r"Ofada Rice: Wikipedia, 'Ofada rice' (summarising Gyimah-Brempong et al. 2016, The Nigerian Rice Economy) \1", s)
    # 5c 第 2 轮复核 R2-M1：Paw San、Ofada 出处换成可打开的一手 / 学术来源（不改 data.json，免得渲染清单哈希失配）
    s = re.sub(r"(?m)^Paw San (\([^)\n]*\)): .*$", lambda m: f"Paw San {m.group(1)}: IRRI Rice Today, 'Myanmar Pearl Pawsan wins World's Best Rice 2011' https://ricetoday.irri.org/?p=2874", s)
    s = re.sub(r"(?m)^Ofada Rice (\([^)\n]*\)): .*$", lambda m: f"Ofada Rice {m.group(1)}: Afr. J. Biol. Sci., Ofada rice, a locally cultivated unpolished rice (Elizade Univ.) https://ajbs.scione.com/cms/fulltext.php?id=1177", s)
    # 6 Tags 栏
    if "## Tags" not in s:
        s = s.replace("## Upload checklist", f"## Tags（YouTube 标签栏）\n\n```text\n{TAGS}\n```\n\n## Upload checklist", 1)
    # 7 Content ID 清单
    if "不登记 Content ID" not in s:
        s = s.replace("- [ ] 语言 English；类别 Education\n", "- [ ] 语言 English；类别 Education\n" + CONTENT_ID + "\n", 1)
    P.write_text(s, encoding="utf-8")
    print("publish.md finished:", len(s), "chars")


if __name__ == "__main__":
    main()
