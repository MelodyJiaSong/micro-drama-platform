"""Generate ../sources.md from data.json + assets.json (run after build.py).
Usage: python -I <this dir>/gen_sources.py"""
import json
from pathlib import Path

EP = Path(__file__).resolve().parent.parent
d = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = {a["file"]: a for a in json.loads((EP / "assets.json").read_text(encoding="utf-8"))}


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


L = []
A = L.append
A("# ep02 · 数据出处、交叉核对与许可（sources.md）")
A("")
A("> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_def.py` 后重跑 `build.py` → `gen_sources.py`。")
A("")
A("## 1. 口径")
A("")
A("- **榜单**：每个主权国家的最高点，按海拔（米）降序，取前 50。")
A("- **国家名单**：Wikidata「主权国家」(Q3624078) 且有 P297 ISO 代码、P610 最高点；查询见 `0_research/data/wikidata_country_highest_points.rq`，原始结果 `wikidata_country_highest_points_2026-11-03.json`。名单含台湾（卡上写 \"Taiwan\"）。格陵兰（3,694 m）、南极洲非主权国家，不入榜。")
A("- **国名**：通用英文短名（China、DR Congo、United States、Turkey…）。")
A("- **海拔取值规则**：")
A("  1. 原查询对每座山取所有 P2044 声明的 **MAX**，会选中过时或错误的值（珠峰 8,850、勃朗峰 2013 年的 4,810.02、达马万德 5,628、塔胡穆尔科 4,220）。本期改为取 Wikidata **preferred rank** 的值；没有 preferred 时取 normal 值并与第二来源核对。")
A("  2. 每一条都与第二来源核对：Wikipedia「List of elevation extremes by country」（revid 1381548721，2026-10-23）；差异处再查该山 Wikipedia 条目的 infobox 及其引用（USGS、大学测量、Peaklist 等）。")
A("  3. 取「支持最好」的值作 `value`，另一来源写进 `cross_check`。差异 > 0.5% 或影响排序的，写进 `notes`。")
A("  4. Peakbagger 对脚本请求返回 403，网页抓取工具也被拦，**本期没有直接核到 Peakbagger**；凡 Wikipedia 引用 Peakbagger / Peaklist 的值，记为「经 Wikipedia 转引」。")
A("- **显示**：`value_display` 四舍五入到整米；`secondary_display` = 米 × 3.28084 四舍五入到整英尺。")
A("- **同值同名次（标准竞赛排名 1,1,3）**：共享山峰两国同名次，下一名跳号，所以第 50 名就是第 50 个国家；同名次内按国名字母序，顺序稳定（China→Nepal、DR Congo→Uganda、France→Italy）。")
A("")
A("## 2. 归属与大洲判断（待用户复核）")
A("")
A("| 议题 | 本期做法 | 依据 |")
A("|---|---|---|")
A("| 归属总原则 | 按实际管辖（de-facto administration） | topics.md §3 |")
A("| 台湾 | 保留，标 \"Taiwan\"（玉山 3,952 m，第 44） | Wikidata 主权国家名单含台湾；用户既定 |")
A("| 印度 / K2 | 印度取干城章嘉峰 8,586 m；K2 归巴基斯坦。印度官方地图把 K2 所在地区划入拉达克，主张 K2 为本国最高点 | 实际管辖；洞察卡 4 说明 |")
A("| 共享山峰 | 同一山顶同时是两国最高点的，各国一张卡，`badge` 写 SHARED WITH …：珠峰（中国/尼泊尔）、斯坦利山（刚果（金）/乌干达）、勃朗峰（法国/意大利） | topics.md §3 |")
A("| 勃朗峰主权 | 法意两国对峰顶一带边界有争议（Wikipedia：\"Ownership of the summit area has long been disputed\"）；两国都计入，`notes` 说明；洞察卡 2 提及 | Wikipedia 'Mont Blanc' |")
A("| 其他边境峰 | K2、干城章嘉、诺沙克、托木尔、汗腾格里、奥霍斯-德尔萨拉多、什哈拉、巴扎尔杜久、卡里辛比、友谊峰、哈兹拉特苏丹等位于国界上，但另一国的最高点不是它，所以不加 SHARED 徽章，只在 `notes` 写明 | 徽章只表示「同为两国最高点」 |")
A("| 不丹 | 冈仁布钦（Gangkhar Puensum）位于不丹—中国边界附近，边界走向有争议；按实际管辖计入不丹 | Wikipedia |")
A("| 大洲（计分板） | 按**山顶所在位置**，不按国家习惯分组 | 用户既定 |")
A("| 厄尔布鲁士 | Europe（在大高加索分水岭以北） | 用户既定 |")
A("| 什哈拉（格鲁吉亚） | Europe（位于大高加索主分水岭上，分水岭作欧亚界时界上山峰计入欧洲） | 用户既定 |")
A("| 巴扎尔杜久（阿塞拜疆） | Europe，与什哈拉同规则（同在主分水岭上）；注意阿塞拜疆通常被归入亚洲 | 代理判断，保持规则一致 |")
A("| 阿拉拉特（土耳其）、阿拉加茨（亚美尼亚） | Asia（亚美尼亚高原，在高加索分水岭以南） | 用户既定 / 同规则 |")
A("| 查亚峰（印尼） | Oceania（新几内亚岛位于澳大利亚大陆架上；七大洲最高峰惯例亦把它算大洋洲） | 代理判断 |")
A("| 泰德峰（西班牙） | Europe（加那利群岛是大洋火山岛，不在任何大陆架上，按所属国计） | 代理判断：大陆架岛归该大陆，大洋岛随国家 |")
A("| 计分结果 | Asia 19、Europe 8、Africa 8、South America 7、North America 5、Oceania 3 | data.json |")
A("")
A("## 3. 前 50 名边界核对")
A("")
A("- 第 49 西班牙 Teide 3,715 m（两源一致）；第 50 也门 Jabal an-Nabi Shu'ayb 3,666 m（两源一致；旧资料有 3,760 m，取哪一个都在榜内）。")
A("- 第 51 伊拉克 Cheekha Dar 3,611 m（Wikidata 与 Wikipedia 一致，Wikipedia 转引 Peakbagger），比第 50 低 55 m；第 52 莱索托 3,482 m。")
A("- 修正后唯一的名次移动：喀麦隆 4,095 → 4,040 m，从并列第 41 降到第 43；格鲁吉亚若取 5,203 m 会和肯尼亚（5,199 m）互换。**入榜的 50 国不因任何修正而改变。**")
A("- 原查询结果第 19/20 行哥伦比亚出现两次（Simón Bolívar 与 Cristóbal Colón 同为 5,775 m），只取 Cristóbal Colón 一条。")
A("")
A("## 4. 逐条出处与交叉核对")
A("")
A("差异 = |value − cross| / value。所有条目 retrieved_at = 2026-11-03。")
A("")
A("| # | 国家 | 山峰 | value (m) | 主值来源 | 交叉核对 | 差异 % | 备注 |")
A("|---|---|---|---|---|---|---|---|")
for it in d["items"]:
    s, c = it["source"], it["cross_check"]
    flag = "⚠ " if c["diff_pct"] > 0.5 or "ORDER-SENSITIVE" in it["notes"] or "DISCREPANCY" in it["notes"] else ""
    A(f"| {it['rank']} | {esc(it['country_name'])} | {esc(it['name'])} | {it['value']} | [{esc(s['name'])}]({s['url']}) | [{esc(c['name'])}]({c['url']}): {c['value']} | {c['diff_pct']} | {flag}{esc(it['notes'])} |")
A("")
A("**Tag 出处**：`First ascent YYYY` 取自 Wikidata P793（first ascent）+ P585；Wikidata 没有的从该山 Wikipedia infobox 补（Ismoil Somoni、Aconcagua、Ojos del Salado、Huascarán、Hkakabo Razi、Pico de Orizaba、Mont Blanc、Mount Wilhelm、Toubkal、Mount Aragats、Cerro Chirripó、Mount Ararat）。两源年份冲突的不加（Bazardüzü、Kinabalu、Yushan、Damavand、Mount Cameroon）。火山类 tag 取 Wikidata P31 或 Wikipedia 短描述；\"Highest in …\" 取 Wikipedia 短描述 / 列表脚注。")
A("")
A("## 5. 洞察卡核对")
A("")
A("| after_rank | 文案 | 数据支持 |")
A("|---|---|---|")
support = {
    41: "Mount Cameroon：Wikidata 4,095 m vs Wikipedia（SRTM 无高于约 4,027 m 的格点）4,040 m；本期取 4,040",
    32: "Mont Blanc notes：Wikipedia「Ownership of the summit area has long been disputed between France and Italy」",
    21: "Elbrus 5,642 − Mont Blanc 4,807.47（2026-09 测量）= 834.53 m，显示取整 835 m；Wikipedia「Highest mountain of Russia and Europe」",
    11: "第 1–10 名最低为 Aconcagua 6,960.8 m > 6,950；10 张卡中 9 张 continent = Asia（仅阿根廷例外）",
    4: "K2 notes：印度主张该地区；按实际管辖归巴基斯坦（Wikipedia 列表 K2 脚注）",
}
for ins in d["insights"]:
    A(f"| {ins['after_rank']} | {esc(ins['text'])} | {support.get(ins['after_rank'], '')} |")
A("")
A("## 6. 许可")
A("")
A("- **Wikidata**：CC0，数值可直接使用。")
A("- **Wikipedia**：只用作事实来源（数值、年份、归属说明），不搬运文字；事实本身不受版权保护。屏上与描述框不复制 Wikipedia 文本。")
A("- **USGS**：美国联邦政府作品，公有领域。Universidad Nacional de Cuyo、Peaklist 等只引用测量数值（事实）。")
A("- **图片**：全部来自 Wikimedia Commons，逐张核对 extmetadata 的 LicenseShortName，只收 Public domain / CC0 / CC BY / CC BY-SA（含移植版本如 CC BY-SA 2.0 fr、2.5 nl、2.1 au、3.0 de）。拒绝：`Dejen misura da cima W.jpg`（许可仅为 \"Attribution\" 自由文本，非标准 CC，保守弃用）。所有改动只有缩放、重新编码 JPEG，Hkakabo Razi 一张为去掉上传者叠加的海拔字样做了裁切（CC0）。CC BY-SA 图只缩放裁切，不做其他改编。自然景观，无全景自由（FoP）问题。")
A("- **缺图**：第 32 名乌兹别克斯坦 Khazret Sultan——无 P18、无 Commons 分类，英/俄/乌兹别克/塔吉克拼写搜索都找不到可确认是该峰且许可合格的照片，`image` = null，渲染器需用占位（国旗或剪影）。")
A("- **低分辨率提示**：Puncak Jaya 原图仅 640×480、Mount Logan 975×639、Jabal an-Nabi Shu'ayb 1024×768、Pico de Orizaba 1024×768、Karisimbi 1134×504、Hkakabo Razi 裁后 1037×775；卡片主图区小，预计够用，渲染后抽检。")
A("- **内容提示**：Ismoil Somoni Peak 为黑白老照片（1985）；Ras Dashen 是走向平顶山体的步道视角；Khüiten Peak 是从 Ukok 高原远眺 Tavan Bogd 山群；也门一张为从 Haraz 远眺山脊（均为 Wikipedia 条目所用图或最佳可得）。")
A("")
A("## 7. 图片署名（可直接贴进 YouTube 描述）")
A("")
A("```text")
A("Mountain photos via Wikimedia Commons (resized/cropped):")
for it in d["items"]:
    if not it["image"]:
        continue
    a = assets[it["image"]]
    lic = a["licence"]
    who = "public domain" if lic == "Public domain" else f"{a['author']}, {lic}"
    A(f"#{it['rank']} {it['name']} ({it['country_name']}): {who} – {a['commons_page']}")
A("Data: Wikidata (CC0); USGS; national and university surveys; cross-checked with Wikipedia.")
A("```")
A("")
A("上面完整版带链接，约 7,000+ 字符，**超过 YouTube 描述 5,000 字符上限**。描述框用下面的紧凑版（名次、国家代码、作者、许可，约 1,900 字符），完整版放置顶评论或频道外的公开页面，由用户发布时决定。")
A("")
A("```text")
A("Photos: Wikimedia Commons (resized/cropped). Licences: creativecommons.org/licenses")
for it in d["items"]:
    if not it["image"]:
        continue
    a = assets[it["image"]]
    who = "public domain" if a["licence"] == "Public domain" else f"{a['author']}, {a['licence']}"
    A(f"#{it['rank']} {it['country_iso2']}: {who}")
A("Data: Wikidata (CC0), USGS, national surveys; checked against Wikipedia.")
A("```")
A("")
(EP / "sources.md").write_text("\n".join(L), encoding="utf-8")
print("sources.md lines:", len(L))
