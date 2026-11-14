# -*- coding: utf-8 -*-
"""rank_scroll publish 生成 publish.md 后的人工修订（可重跑：先重新 publish 再跑本脚本）。"""
import json, re
from pathlib import Path
EP = Path(__file__).resolve().parents[1]
p = EP / "publish.md"
s = p.read_text(encoding="utf-8")
d = json.load(open(EP / "data.json", encoding="utf-8"))
title = "Largest Countries in the World by Area | Top 50 (2026)"
s = re.sub(r"## Title\n\n.*\n（\d+ 字符）", f"## Title\n\n{title}\n（{len(title)} 字符；年份为本期版本年，屏上统计行写 Data as of 2024）", s)
s = s.replace("Photo credits (Wikimedia Commons; resized and cropped, no other changes):",
              "Photo credits (Pexels / Unsplash / Creative Commons / NASA; resized and cropped, no other changes):")
# （#43 由 publish 自动列为 AI-generated，无需再插入占位说明）
s = s.replace("Sources: UN Demographic Yearbook 2024, CIA World Factbook\nFull image",
              "Sources: UN Demographic Yearbook 2024, CIA World Factbook\n"
              "Where sources disagree by more than 1% (Saudi Arabia, Libya, Iran, Venezuela, South Sudan, Kenya, France) we use the UN figure; details in the replies under the pinned comment.\nFull image", 1)
s = re.sub(r"#LargestCountriesInTheWorldByArea #Top50 #Ranking #DataComparison",
           "#Geography #LargestCountries #CountrySizeComparison", s)
s = s.replace("1 images marked AI-generated are illustrations, not photos", "1 image marked AI-generated is an illustration, not a photo")
s = s.replace("（卡上标 Illustration / Render）", "（卡上标 AI IMAGE，署名 AI-generated image, not a photo）")
s = s.replace("Disputed areas follow each country's UN figure:", "Region labels follow the UN M49 classification (Iran shown as Middle East). Disputed areas follow each country's UN figure:", 1)
# Comment 2：50 行同一链接压缩成口径说明 + 差异表
rows = []
for it in d["items"]:
    cc = it["cross_check"]
    if cc["diff_pct"] > 1:
        rows.append(f"#{it['rank']} {it['name']}: UN {it['value']:,} km² vs CIA {cc['value']:,.0f} km² ({cc['diff_pct']}%)")
c2 = ("Data sources: every figure is the 2024 surface area (land + inland water) in the UN Demographic Yearbook 2024, Table 3 "
      "https://unstats.un.org/unsd/demographic-social/products/dyb/documents/dyb2024/table03.pdf — except Sudan, which has no UN value: "
      "World Bank WDI AG.SRF.TOTL.K2, 2024 (FAO, CC BY 4.0) https://data.worldbank.org/indicator/AG.SRF.TOTL.K2\n"
      "Sudan: not in UN DYB 2024; World Bank/FAO value 1,878,000 km² (CIA 1,861,484 km², 0.88%).\n"
      "Cross-check: CIA World Factbook, final edition (Jan 2026, public domain).\n"
      "Differences above 1%:\n" + "\n".join(rows) + "\n"
      "France: UN counts metropolitan France + Corsica (551,500 km²); with its five overseas regions (CIA, 643,801 km²) it would rank about 42nd.\n"
      "Order changes if you use CIA figures: Venezuela/Nigeria, South Sudan/Afghanistan, Kenya/Madagascar/Botswana.\n"
      "Pluto: NASA gives an equatorial diameter of 2,377 km, i.e. a surface of about 17.7M km² (Russia: 17.1M km²).\n"
      "Australia's Antarctic claim: about 5.9M km² (Australian Antarctic Division), not counted.\n"
      "Some disputed areas may be counted by two countries (e.g. Aksai Chin in both India's and China's figures); no rank changes.")
s = re.sub(r"## Comment 2（\d+ 字符）\n\n```text\n.*?```", f"## Comment 2（{len(c2)} 字符）\n\n```text\n{c2}\n```", s, flags=re.S)
s = s.replace("## Upload checklist",
              "## Tags\n\nlargest countries, largest countries by area, biggest countries in the world, country size comparison, top 50 countries, "
              "world geography, countries ranked by size, Russia Canada USA China, geography facts, data ranking\n\n"
              "## 风险版说明\n\n默认母版不含 5 张许可不明 / 非商用的图（#11 DR Congo、#22 Angola、#31 Venezuela、#40 South Sudan 用可商用替代图；#43 CAR 用 AI 生成的雨林瀑布图）。"
              "若用户签字用 `_with-risk-images` 版，须先 `python -m rank_scroll publish <ep> --allow-risk-images` 重新生成，再跑本脚本，并补署名。"
              "默认母版含 1 张 AI 生成图（#43 Central African Rep.，Codex image_gen，写实雨林瀑布，不对应具体地点）：上传时 Altered or synthetic content 勾选 Yes。\n\n## Upload checklist", 1)
p.write_text(s, encoding="utf-8")
m = re.search(r"## Description（(\d+) / 5000 字符）\n\n```text\n(.*?)```", s, re.S)
desc = m.group(2)
s = s.replace(m.group(0), f"## Description（{len(desc)} / 5000 字符）\n\n```text\n{desc}```")
p.write_text(s, encoding="utf-8")
print("desc chars", len(desc), "c2", len(c2))
