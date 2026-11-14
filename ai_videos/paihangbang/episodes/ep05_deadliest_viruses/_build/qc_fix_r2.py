# -*- coding: utf-8 -*-
"""第 2 轮独立审片（qc.md 第 2 轮 D3/D6/D11、N4–N7）的修正。重复运行安全。"""
import json
from pathlib import Path

B = Path(__file__).resolve().parent
EP = B.parent
p = B / "build.py"
s = p.read_text(encoding="utf-8")
R = [
    # N4：天花出处换成可打开的期刊 DOI
    ('"url": "https://www.carnegiecouncil.org/media/series/39/20091028-smallpox-the-death-of-a-disease", "tier": "peer-reviewed"}',
     '"url": "https://doi.org/10.1016/j.vaccine.2011.06.080", "tier": "peer-reviewed"}'),
    ('{"name": "D.A. Henderson (led WHO eradication), Vaccine 2011; Carnegie Council 2009"',
     '{"name": "D.A. Henderson (led WHO eradication), The eradication of smallpox, Vaccine 2011;29 Suppl 4:D7–D9"'),
    # D3：#25 补作者与题名
    ('{"name": "Epidemiology and Vaccinal Prevention (Russia) 2024 review"',
     '{"name": "Dzagurova et al., Epidemiology and Vaccinal Prevention 2024;23(5) (Russia, TBE 2000–2022)"'),
    # D6：如实写明 2,330 是按 CDC 年度数据求和、由维基百科表格转引
    ('{"name": "CDC ArboNET annual totals 1999–2018 (50,830 cases, 2,330 deaths), as tabulated from CDC data", "url": "https://www.cdc.gov/west-nile-virus/data-maps/historic-data.html", "tier": "aggregator"}',
     '{"name": "CDC ArboNET yearly death counts 1999–2018 summed (2,330), as tabulated in Wikipedia\'s list of West Nile outbreaks; CDC historic-data page blocks scripted access", "url": "https://en.wikipedia.org/wiki/List_of_West_Nile_virus_outbreaks", "tier": "aggregator"}'),
    # D11：计分板分组图标
    ('"tally": {"by": "continent", "title": "How they spread"},',
     '"tally": {"by": "continent", "title": "How they spread", "icons": {"Airborne": "wind", "Blood & sex": "droplet", "Mosquito & tick": "bug", '
     '"Food & water": "glass-full", "Animals": "paw", "Contact": "hand-stop"}},'),
]
n = 0
for old, new in R:
    if new in s:
        continue
    assert s.count(old) == 1, (old[:80], s.count(old))
    s = s.replace(old, new)
    n += 1
p.write_text(s, encoding="utf-8")
print("build.py replacements:", n)

# N1/N5/N7：AI 图账本作者缩短（描述框超长主因）、不写内部路径；乙肝署名不再声称核心来自 PDB
assets = json.loads((EP / "assets.json").read_text(encoding="utf-8"))
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
by_file = {it["image"]: it for it in data["items"]}
for a in assets:
    if not (str(a.get("licence", "")).lower().startswith("ai-generated") or a.get("synthetic")):
        continue
    it = by_file.get(a["file"], {})
    a.setdefault("method", a.get("author", ""))
    a.setdefault("local_file", a.get("source_url", ""))
    a["author"] = "AI illustration (Codex)"
    a["licence"] = "AI-generated"
    a["source_url"] = ""
    a["source_page"] = ""
    if it.get("key") == "hbv":
        it["image_credit"] = "Illustration: AI-generated hepatitis B virus"
(EP / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2), encoding="utf-8")
(EP / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("AI ledger entries shortened")
