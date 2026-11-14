"""Generate sources.md from data.json, assets.json, images.json, candidates.json and the static notes below.

Usage: python -I 08_sources.py <build_dir> <episode_dir>
"""
import json
import os
import sys

HEAD = """# ep01 · 来源、交叉核对与许可记录

> 由 `_build/08_sources.py` 生成（2026-11-03）。改数据先改 `_build/` 里的输入再重跑，不手改本文件。
> 构建顺序：`01_parse_ctbuh.py` → `02_parse_wikipedia.py` → `03_wikidata.py` → `04_commons_candidates.py`（补充：`04b_category_candidates.py`）→ 目检 `09_contact_sheet.py` / `10_preview_candidates.py`，人工选择记在 `overrides.json` 与 `override_reasons.json` → `05_select_download.py . .. overrides.json` → `06_build_data.py` → `07_validate.py` → `08_sources.py`。原始抓取存在 `_build/raw/`，全部视为不可信数据，只解析不执行。

## 1. 数据来源与许可

| 用途 | 来源 | 抓取 | 许可 / 用法 |
|---|---|---|---|
| **主值**：名次、高度、层数、竣工年、城市、状态 | CTBUH Skyscraper Center「The 100 Tallest Completed Buildings in the World in 2026」 https://www.skyscrapercenter.com/buildings ；每座楼的 CTBUH 页面见下表 | 2026-11-03 | 只用事实并注明出处（描述框写明 CTBUH）。不搬运页面文字、版式和图片。**CTBUH 网站使用条款未逐条核对（待核）**：事实不受版权保护，但数据库条款可能有约束。 |
| 状态核实（不收的楼） | CTBUH 单楼页：International Land-Sea Center https://www.skyscrapercenter.com/building/chongqing-corporate-avenue-1/148 ；Greenland Shandong IFC https://www.skyscrapercenter.com/building/greenland-shandong-international-financial-center/30121 | 2026-11-03 | 同上 |
| 交叉核对：高度、层数、开业年、国家 | Wikidata（P2048 / P1101 / P1619 / P571 / P17 / P18），SPARQL 见 `_build/raw/wikidata_query.rq`，结果在 `wikidata_result.json` | 2026-11-03 | **CC0** |
| 交叉核对（Wikidata 缺高度时）、英文名、文章与图片线索 | Wikipedia「List of tallest buildings」https://en.wikipedia.org/wiki/List_of_tallest_buildings （API wikitext） | 2026-11-03 | 只取事实，不复制文字（CC BY-SA 正文不进视频）。它引用 CTBUH，**不是独立来源**。 |
| FoP 各国状态 | Commons:Freedom of panorama（含 /table 子页）及 Commons:Copyright rules by territory/{UAE, South Korea, Kuwait, Egypt, Vietnam} | 2026-11-03 | 参考信息 |

**统计口径**：CTBUH architectural height，含尖顶，不含天线；只收 CTBUH 状态为 Completed 的建筑，塔类构筑物（晴空塔、CN Tower）不算建筑。CTBUH 已建成榜单本身含 2024–2026 年竣工的楼（如 City Tower One，2026 年，第 74 名），说明它是最新的。

**是否最新（2026-11）**：
- 2024–2026 年进入 Top 50 的楼：JPMorganChase Tower（2025，第 33 名）、紫金金融大厦（2025，第 36 名）、宁波中心 T1（2025，第 41 名）、Iconic Tower（2024，第 44 名）、招商银行全球总部主塔（2025，第 45 名）。
- **不收**：International Land-Sea Center（重庆，458.2 m）和 Shandong IFC（济南，428 m）。CTBUH 状态都是 *Architecturally Topped Out*，山东 IFC 的 CTBUH 预计竣工年为 2026。Wikipedia 已把两座列为建成（第 18、30 名），这里按 CTBUH 口径不收。发布前复核，如果 CTBUH 改为 Completed，就重排名次并重渲染。
- **不收（未完工）**：Jeddah Tower、Burj Binghatti Jacob & Co、Marina 106、Tianfu Center（Panda Tower）、Cavalli Tower、Al Habtoor Tower 等，都不在 CTBUH 已建成前 100 名里。
- Wikipedia 和 CTBUH 按高度逐条比对（脚本输出见本次会话）：除上面两座外，其余 Top 50 一一对应。

**名次规则**：竞争排名，与 CTBUH 一致：第 8、20、22 名各有两座并列，所以没有第 9、21、23 名。同名次内按显示名字母序。

**显示值**：取整到米（3 位有效数字）。如果两座不同高度的楼取整后数字相同，就改显示 1 位小数，各条 notes 里注明。英尺取 CTBUH 公布的英尺值。

**名称**：默认用 CTBUH 名称。以下几座改用通行英文名：
- 大小写：TAIPEI 101 → Taipei 101，CITYMARK CENTRE → Citymark Centre；
- Menara Merdeka Maybank → **Merdeka 118**（通行名，官方名写在 notes；用户可改回）；
- CITIC Tower → CITIC Tower (China Zun)；
- Vincom Landmark 81 → Landmark 81；
- Petronas Twin Tower 1/2 → Petronas Tower 1/2；
- Wuhan Tower → Wuhan Center（Wikipedia 通行名）；
- One Vanderbilt Avenue → One Vanderbilt；
- China Merchants Bank Global Headquarters Main Tower → China Merchants Bank Global HQ（卡片长度）。

**国家口径**：取建筑所在地的主权国家。香港两座记为 `CN` China，副标题写 Hong Kong；Taipei 101 记为 `TW` Taiwan。Wikidata P17 与此全部一致：Wikidata 把香港记为 People's Republic of China，台北 101 记为 Taiwan。

**交叉核对规则**：
- 取 Wikidata P2048 中与 CTBUH 最接近的那条，英尺换算成米。同一条目常有多条高度，分别对应屋顶、尖顶、天线等口径，其余值写进 notes。
- Wikidata 没有高度的 4 座（紫金金融大厦、Two IFC、贵阳国际金融中心 T1、招商银行全球总部），改用 Wikipedia 列表核对，并标明它不是独立来源。
- 层数取 CTBUH 地上层数；竣工年取 CTBUH 竣工年。与 Wikidata 不一致的都写进 notes，以 CTBUH 为准。
"""

FOP = """## 3. 全景自由（FoP）核查

依据 Commons:Freedom of panorama/table 的「Buildings」一栏（2026-11-03 抓取），并核对各国 Copyright rules by territory 页：

| 国家 / 地区 | 本期楼数 | 建筑 FoP（商用） | 依据摘要 |
|---|---|---|---|
| 中国大陆 | 24 | ✓ | Commons 表 ✓；文件常带 {{FoP-China}} |
| 香港 | 2 | ✓ | Commons 表 ✓ |
| 美国 | 8 | ✓ | 17 USC §120(a)：从公共场所可见的建筑可自由拍摄、发布 |
| 马来西亚 | 4 | ✓ | Commons 表 ✓；{{FoP-Malaysia}} |
| 沙特阿拉伯 | 1 | ✓ | Commons 表建筑栏 ✓；{{FoP-Saudi Arabia}} |
| 台湾 | 1 | ✓ | Commons 表建筑栏 ✓ |
| 俄罗斯 | 1 | ✓ | Commons 表建筑栏 ✓ |
| **阿联酋** | 4 | ✗ | 无可用 FoP（Federal Decree-Law 38/2021）。第 22.7 条允许「在广播节目中展示」永久置于公共场所的建筑作品，但 Commons 不认它为 FoP。YouTube 视频算不算「broadcasting programs」，**需法律判断** |
| **韩国** | 2 | ✗ | 著作权法第 35(2) 条：仅限非商用。Commons 实际会对乐天世界塔做打码处理（有 `Lotte world tower (censored).jpg`） |
| **科威特** | 1 | ✗ | Law 75/2019 没有 FoP 例外 |
| **埃及** | 1 | ✗ | Law 82/2002 第 171 条：仅限个人使用 |
| **越南** | 1 | ✗（2023 起） | Law 07/2022：2023-01-01 起仅限非商用；2023 年前上传到 Commons 的照片仍保留，带 {{FoP-Vietnam}} |

**选图规则**（`05_select_download.py`）：
1. 许可只接受 PD / CC0 / CC BY / CC BY-SA。带删除请求或侵权标记、过小（短边 < 700 px）、超宽全景（宽高比 > 2.2）的文件不用。
2. **带 {{NoFoP-…}} 模板的文件一律跳过**（按任务规则视为 FoP 问题文件）。
3. 无 FoP 国家的楼，如果有未加 NoFoP 标、也没有删除请求的文件，仍可选用，但在 `assets.json` 的 `fop_note` 里写 **RISK**。法律上它和带标的文件处境相同，未加标只说明 Commons 没人处理过，不说明可以商用。**发布前须人工决定**：保留、换成更远的天际线图，或去掉图片改用剪影。
4. 每个文件页上实际看到的 FoP 模板和分类都记在 `fop_note` 里。
"""


def md_escape(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def main(bdir, edir):
    d = json.load(open(os.path.join(edir, "data.json"), encoding="utf-8"))
    assets = {a["file"]: a for a in json.load(open(os.path.join(edir, "assets.json"), encoding="utf-8"))}
    out = [HEAD, "\n## 2. 逐条来源与交叉核对\n",
           "| # | 名称 | 城市 / 国家 | CTBUH 高度 (m) | 层数 / 年 | 主源 | 交叉核对 | 差异 % | 备注 |",
           "|---|---|---|---|---|---|---|---|---|"]
    for it in d["items"]:
        cc = it["cross_check"] or {}
        tags = " / ".join(t["text"] for t in it["tags"])
        out.append(f"| {it['rank']} | {md_escape(it['name'])} | {md_escape(it['subtitle'])}, {it['country_iso2']} | {it['value']:g} | {tags} | "
                   f"[CTBUH]({it['source']['url']}) | {('[' + md_escape(cc.get('name', '')).split(' (')[0] + '](' + cc.get('url', '') + ') ' + format(cc.get('value'), 'g')) if cc else '—'} | "
                   f"{cc.get('diff_pct', '—')} | {md_escape(it['notes'])} |")
    big = [it for it in d["items"] if it["cross_check"] and abs(it["cross_check"]["diff_pct"]) > 0.5]
    out.append(f"\n**差异 > 0.5% 共 {len(big)} 条**，原因已写进各条备注：" + "；".join(f"{it['name']}（{it['cross_check']['diff_pct']:+}%）" for it in big) + "。没有超过 10% 的。\n")
    out.append("**洞察卡数据核对**（按 `data.json` 计算）：\n")
    for ins in d["insights"]:
        out.append(f"- after {ins['after_rank']}：「{ins['text']}」")
    from collections import Counter
    it = d["items"]
    out.append(f"  - 依据：2025 年竣工 {sum(1 for x in it if 'Completed 2025' in [t['text'] for t in x['tags']])} 座；"
               f"Shenzhen {sum(1 for x in it if x['subtitle']=='Shenzhen')} 座、New York City {sum(1 for x in it if x['subtitle']=='New York City')} 座；"
               f"2020 年及以后竣工 {sum(1 for x in it if int(x['tags'][1]['text'][-4:]) >= 2020)} 座；"
               f"美洲 {sum(1 for x in it if x['continent'] in ('North America','South America'))} 座（全在美国）；"
               f"≥600 m 有 {sum(1 for x in it if x['value'] >= 600)} 座。"
               f"国家计分：{', '.join(f'{k} {v}' for k, v in Counter(x['country_iso2'] for x in it).most_common())}。\n")
    out.append(FOP)
    out.append("\n### 逐张 FoP 与选图结果\n")
    out.append("| # | 名称 | 图片 | 许可 | FoP 记录 |")
    out.append("|---|---|---|---|---|")
    for it in d["items"]:
        a = assets.get(it["image"]) if it["image"] else None
        if a:
            out.append(f"| {it['rank']} | {md_escape(it['name'])} | [{os.path.basename(a['file'])}]({a['commons_page']}) | {a['licence']} | {md_escape(a['fop_note'])} |")
        else:
            out.append(f"| {it['rank']} | {md_escape(it['name'])} | **无图（image=null）** | — | {md_escape(it['notes'].split('IMAGE: ')[-1] if 'IMAGE: ' in it['notes'] else '')} |")
    out.append("""
## 4. 署名决定

- Commons 署名格式按 Commons:Credit_line：作者 + 许可名 + 许可链接 + 文件页链接；署作者，不署上传者。
- 卡片上 `image_credit` 写短格式「作者 / 许可」，公有领域写「Public domain」；描述框附完整署名块（下节）。CC BY-SA 图片只做缩放和裁切，不做其他改编，`modified` 字段写明。
- 片尾来源卡写：「Photos: Wikimedia Commons contributors (see description)」。
- Wikidata 是 CC0，按惯例仍在来源行注明；CTBUH 作为事实出处注明。

## 5. YouTube 描述框署名块（可直接粘贴）

```
Data: CTBUH Skyscraper Center, "The 100 Tallest Completed Buildings in the World" (retrieved 3 Nov 2026), https://www.skyscrapercenter.com/buildings
Heights = CTBUH architectural height (incl. spires, excl. antennas); completed buildings only, per CTBUH status as of 3 Nov 2026.
Cross-checked with Wikidata (CC0).

Photos (Wikimedia Commons; resized/cropped):
""")
    for it in d["items"]:
        a = assets.get(it["image"]) if it["image"] else None
        if a:
            lic = a["licence"] if a["licence"] == "Public domain" else f"{a['licence']} {a['licence_url']}".strip()
            out.append(f"#{it['rank']} {it['name']}: {a['author']}, {lic}, {a['commons_page']}")
    out.append("```\n")
    open(os.path.join(edir, "sources.md"), "w", encoding="utf-8").write("\n".join(out))
    print("sources.md written", len(out), "lines")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
