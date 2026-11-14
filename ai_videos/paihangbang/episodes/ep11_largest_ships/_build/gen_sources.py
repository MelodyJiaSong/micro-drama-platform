# -*- coding: utf-8 -*-
"""生成 sources.md（数据出处、交叉核对、洞察卡依据、图片许可）。改数据后重跑。"""
import json
from pathlib import Path

B = Path(__file__).parent
EP = B.parent
data = json.loads((EP / "data.json").read_text(encoding="utf-8"))
assets = json.loads((EP / "assets.json").read_text(encoding="utf-8")) if (EP / "assets.json").exists() else []
by_file = {a["file"]: a for a in assets}
cs = {c["key"]: c for c in json.loads((B / "classes_computed.json").read_text(encoding="utf-8"))}

L = []
L.append("# ep11 · 数据出处、交叉核对与许可（sources.md）\n")
L.append("> 2026-11-03 代理整理（用户授权自主决策）。本文件由 `_build/gen_sources.py` 生成；改数据请改 `_build/classes_def.py` / `build.py` 的 EXTRA 后依次重跑 `compute_classes.py` → `build.py` → `gen_sources.py`。\n")
NPRIM = sum(1 for it in data["items"] if it["source"]["tier"] == "primary")
L.append(f"""## 1. 口径与方法

- **指标**：登记总吨（Gross Tonnage, GT，《1969 年国际船舶吨位丈量公约》），衡量船体围蔽容积，不是重量、不是载重吨。单位 GT，屏上写全数（如 248,663 GT），不按 bible §3.4 取 3 位有效数字——前 13 名之间只差几百 GT，取整会造成大量假并列（代理判断）。
- **一张卡 = 一个船级**：同一船东同一建造计划、同一名义尺寸的姊妹船合并（即使分在几家船厂造）；卡上数值 = 该船级在役船中最大的登记 GT，`representative` 记取到该值的船与 IMO。
- **范围**：2026-11 在役、能自航或拖航作业的船。**不收**：永久系泊的海工装置（FPSO、FLNG、FSO / FSU，例如 Prelude FLNG、Coral-Sul、Egina、TI 级改装的 FSO Asia / Africa / SA Europe / SA Oceania）、军舰（军舰不丈量 GT）、在建船、已拆解船。
- **下限**：只收**大于目前仍在营运的最大油轮**（ORIENTAL ARK，IMO 9424209，170,618 GT，VesselFinder）的船级。这样油轮、VLCC 那一大群 160–170k GT 的同质船自然在榜外，也给出一条清楚的线。榜单因此是 42 个船级，不凑 50。
- **完整性**：用 VesselFinder 高级搜索按 GT 区间自适应切分（每段 ≤20 艘，避免翻页漂移）抓取全部 GT ≥ 160,000 的登记船 1,090 艘（`_build/vf_fleet_gt160_bands.json`，抓取脚本 `vf_bands.py`），逐艘归入船级（`classes_def.py` / `compute_classes.py`）。所有 >170,618 GT 的非海工船都已归入船级。GT 不明的船（如 Heerema 的 Sleipnir，VesselFinder 与 DNV 都无 GT，维基只给排水量 273,700 t）无法排序，不收。
- **来源分级**：
  - primary：**DNV Vessel Register**（船级社公开登记，`vesselregister.dnv.com`，字段 `grossTon69`、船厂、交船日、运营状态），42 个船级中 {NPRIM} 个的代表船或同 GT 姊妹船在 DNV 有登记，数值与 VesselFinder 完全一致。
  - aggregator：**VesselFinder** 船舶详情（IHS Markit / S&P 数据），其余船级的主值；交叉核对用维基百科「List of largest container ships」「List of largest ships by gross tonnage」及各船条目（只作核对）。
  - Equasis 需登录，未用；LR / ABS / BV / KR / CCS 公开登记需登录或为 JS 应用，未能脚本核对。
- **国家归属**：运营公司（班轮公司 / 邮轮公司 / 运营方）总部所在国，不用船旗国（巴拿马、利比里亚等方便旗会误导）。OOCL 总部在香港，标 Hong Kong；ONE（日本三家合资）总部在新加坡，标 Singapore；Valemax / Guaibamax 是按淡水河谷（Vale）规格建造、长期租给 Vale 运矿的船，船东多为中、韩、阿曼等公司，归 Vale 所在的 Brazil；Excellence 级跨 Costa / AIDA / P&O / Carnival 四个品牌，按取值船 Costa Toscana 的运营方 Costa Cruises（热那亚）归 Italy，与其他卡「取值船的运营方」同一规则（QC M3，2026-11-04 改）。片内来源行写「Flag = operator HQ」，描述框口径写明 Hong Kong / Singapore / Brazil 三处。
- **次显示**：`secondary_display` = GT ÷ 泰坦尼克号 46,328 GRT（1912 年登记总吨；新旧丈量规则不同，只作直观比较）。
- **标签**：长度取代表船 LOA（VesselFinder / DNV，四舍五入到米）；「Since」= 该船级首制船交付年（Pioneering Spirit 船体 2014 年交付、2016 年投入作业，写 2016）。
- **统计期**：2026-11-03 取数。发布前 7 天内复核（重点：2026 新交付船的 GT、World Asia 的暂定值）。
""")
L.append("## 2. 逐条数据\n")
L.append("| # | 船级 | 运营方 / 国家 | GT（主值） | 代表船 IMO | 成员 | 主源 | 交叉核对 | 备注 |")
L.append("|---|---|---|---|---|---|---|---|---|")
for it in data["items"]:
    xc = it.get("cross_check") or {}
    xs = f"{xc.get('name','')}" + (f"：{xc['value']:,}（{xc['diff_pct']:+.2f}%）" if xc.get("value") and xc.get("diff_pct") is not None else "")
    src = it["source"]
    L.append(f"| {it['rank']} | {it['name']} | {it['operator']} / {it['country_name']} | {it['value']:,} | {it['representative']['name']} {it['representative']['imo']} | {it['members_count']} 艘，{it['first_year']} 起 | [{src['tier']}] [{src['name']}]({src['url']}) | {xs or '—'} | {it['notes']} |")
L.append("""
## 3. 交叉核对差异（>0.5% 或需人看）

- **Oasis 级**：DNV 登记 Utopia 236,473 / Wonder 235,600；维基与皇家加勒比宣传 236,860 / 236,857。取 DNV。
- **MSC Irina 级**：DNV 236,184；维基列表 233,328（-1.2%）。取 DNV。
- **Icon 级**：皇家加勒比宣传 250,800 GT；DNV 登记 248,663。取 DNV。
- **CMA CGM Seine 级**：维基把 Seine 写成 236,583（与 Saadé 级同值，疑似照抄）；VesselFinder 237,742，Notre Dame 组 236,463。取 VesselFinder，归为同一船级依据 Baird Maritime「Notre Dame 与 Seine 同一系列」。
- **OOCL Wisdom 级**：DNV（OOCL Grace）234,361；维基取整 236,000。取 DNV。
- **MOL Triumph 级 / OOCL Hong Kong 级 / COSCO Universe 级 / Valemax**：维基列表比 VesselFinder 低 0.5–1.4%（旧登记值），VesselFinder 新值与 DNV（Universe 级 Solar、Valemax Pacific Unity）一致，取新值。
- **Sphere 级**：Princess 宣传 175,500；VesselFinder 177,882。取登记值。
- **MSC World 级**：MSC World Asia（2026）VesselFinder 只有 205,700，明显低于两艘姊妹（215,863 / 216,638），疑为暂定值，不影响本级取值（取 World America 216,638）。
- 第二来源缺失（只有 VesselFinder）：Berlin Maersk 级、CMA CGM Bougainville 级、Marco Polo 级、MSC London 级、Winning Ambition 级（Winning Ambition 另有 DNV 登记 174,863）、Guaibamax、Ever E 级、Ane Maersk 级、Meraviglia 级、Emma Maersk 级。均为 IMO 号直查，GT 与同级姊妹一致，判断可用。

## 4. 待确认 / 代理判断

- **YUAN HAI SI LU（远海丝路）**：2026-11-04 按独立审片 M2 收入为第 31 名（180,011 GT，VesselFinder；在航去 Ponta da Madeira）。新华社 2026-09-02：中远海运散运运营、舱容 28 万 m³，比同尺度传统矿砂船提升 40% 以上，可以解释 GT 比 340 m Guaibamax 高 3.6%。GT 仍只有 VesselFinder 一个来源（与其余 28 个船级同等），发布前 7 天复核。
- **Sleipnir**（Heerema 半潜起重船）：GT 不公开，无法排序，不收。
- **永久系泊装置**：Prelude FLNG（VesselFinder 499,167 GT，维基 300,000）、Coral-Sul FLNG 346,165、Koryak FSU 251,053、Nguya FLNG 243,515、TI 级 FSO 234,006–236,638、多艘 FPSO 205–232k，均不收（不是航行的船）。若改口径收入，榜首仍是 Prelude。
""")
L.append("## 5. 洞察卡依据\n")
basis = {
    39: "VesselFinder GT≥160k 清单中 Crude Oil Tanker 最大为 ORIENTAL ARK 170,618 GT；第 42 名 Emma Maersk 级 171,542。",
    31: "首制船 2025 年及以后的船级：CMA CGM Seine（2025）、Disney Adventure（2025-12）、Berlin Maersk（2025）、Ever E（2025）、OOCL Wisdom（2026）、Yuan Hai Si Lu（2026）、Winning Ambition（2026）= 7 个。",
    22: "GT 按 ITC 1969 由围蔽总容积 V 计算（GT = K1·V），不是重量；邮轮上层建筑容积大。",
    15: "Ever Given 属 Ever G 级（第 14 名）；2021-03-23 至 03-29 搁浅堵塞苏伊士运河（维基 2021 Suez Canal obstruction）。",
    7: "MSC Irina 24,346 TEU 为最大箱量（维基 List of largest container ships）；GT 更大的集装箱船级：CMA CGM Seine 237,742、Ever A 236,680、Jacques Saadé 236,583。",
    2: "403,342 / 248,663 = 1.622 → 大 62%；Pioneering Spirit 是平台安装 / 拆除起重船（Allseas）。",
}
for ins in data["insights"]:
    L.append(f"- after #{ins['after_rank']}：「{ins['text']}」— {basis.get(ins['after_rank'], '')}")
L.append("\n## 6. 计分板（运营方国家）\n")
from collections import Counter
cnt = Counter(it["country_name"] for it in data["items"])
L.append("、".join(f"{k} {v}" for k, v in cnt.most_common()))
L.append("\n## 7. 图片许可\n")
L.append("默认母版：Flickr 可商用许可照片为主（CC BY / CC BY-SA / CC0 / PDM，`_build/claude_search.py` 按船名搜、照片页核许可）+ 2 张同为 Flickr 可商用的替代图（image_alt：Icon、Disney Adventure）+ 5 张 Codex 生成写实插图（Valemax 作主图；OOCL Wisdom、Sphere、Winning Ambition、Guaibamax 作 image_alt，这 4 项真实照片许可不明），默认版无占位卡；生成图卡上由渲染器标「AI IMAGE」与「not a photo」。风险版（`_with-risk-images`）6 张卡用许可不明的网页照片（Icon、OOCL Wisdom、Disney Adventure、Sphere、Winning Ambition、Guaibamax），需用户签字。不用维基共享资源的图（follow-up 009 / 023）。每张图的来源页、作者、许可、修改说明见 `assets.json`。\n")
L.append("| # | 船级 | 图中船 / 文件 | 作者 | 许可 | 来源页 |")
L.append("|---|---|---|---|---|---|")
for it in data["items"]:
    a = by_file.get(it.get("image") or "", {})
    L.append(f"| {it['rank']} | {it['name']} | {it.get('image','')} | {a.get('author','—')} | {a.get('licence','—')} | {a.get('source_page','—')} |")
(EP / "sources.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("sources.md written")
