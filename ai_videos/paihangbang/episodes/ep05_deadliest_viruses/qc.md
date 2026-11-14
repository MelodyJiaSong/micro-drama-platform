独立审片 · 第 3 轮（fresh-context 子代理，2026-11-04）

# ep05 · Deadliest Viruses in History · 审片记录（第 3 轮）

- 审片对象：`render/ep05_deadliest_viruses_master.mp4`，01:17:58 重渲。
  - sha256 `433b7dca…e5081`，与 manifest 一致。
  - 1920×1080，60 fps，258.1 s，15,486 帧，H.264（约 1.64 Mbps）加 AAC 静音轨。
  - 时间线与第 2 轮相同：片头 0–5、滚动 5–223.1、冠军 223.1–229.1、计分板 229.1–236.1、来源卡 236.1–240.1、片尾 240.1–258.1 s。
- 输入核对：重算了 manifest 中 32 个输入的 sha256，与当前文件逐一相同。
  - `data.json` 为 `a2f7f111…`，`assets.json` 为 `f14db25a…`，另有 30 张图。
  - 生成时间：`publish.md`（01:18:02）和 `thumbnail.png`（01:18:01）都在本次母版之后生成；`data.json`、`assets.json`、`sources.md`、`topic.md` 都在 00:46 改过。
  - 30 张卡用图与第 2 轮相同，文件时间都早于第 2 轮报告。11 张 AI 图没有重新出图。
- 方法：
  - 抽帧：每 2 s 一张，拼成 6 张 5×5 接触表（带时间码），覆盖 0–258 s。
  - 1080p 关键帧 24 张：片头、7 张洞察卡、#27 / #12 / #5 等 AI 卡、#10、冠军、计分板、来源卡、片尾。
  - 手机尺寸：640×360 帧 5 张，并查看封面。
  - 全片跑 freezedetect 和 volumedetect；重算发布稿三段文字的字符数和链接数，并检查内部路径。
  - 联网核对：天花 DOI（经 PubMed、Crossref、OWID）、TBE 原文 PDF、西尼罗（维基百科页和 CDC 检索结果），另随机抽查 #13 甲肝、#26 MERS、#29 克里米亚-刚果出血热。
  - 看了 #5 / #12 / #27 的原 CDC 候选图和其他候选图，用来判断 N3 的理由是否属实。
- 音频：全片静音（mean / max −91.0 dB），§7 第 6 项**未检**。
  - `_build/music_watch.py` 仍在轮询 Suno 任务（日志最后一条 01:14 queued）。任务完成后它会自动重渲母版，并重跑 publish 和 thumb。
  - 本报告只对 sha256 `433b7dca…` 这一版有效。

## 结论：**可发布（仅指静音画面这一层；上传前还要完成用户决定项和配乐复审）**

- **已修**：第 2 轮的阻塞和重大问题都已解决。
  - N1：描述框 3,370 字符。
  - N2：合成内容声明改为 Yes，描述框注明「11 images marked AI-generated are illustrations, not photos」，来源卡改为「Image credits」。
  - D11：计分板 6 个分组各有自己的图标。
  - N4：天花出处换成 Henderson 2011 的 DOI，链接可以解析，OWID 也引这篇作 300M 的出处。
  - N5：评论里不再出现内部路径。
- **转为用户决定**：N3（乙肝、EB 病毒、SARS 用 AI 插画）。作者在 topic.md 写下的理由大体属实，图上和描述框的披露完整，3 张图没有科学性错误（乙肝内部画得简化，见 N7）。是否接受由用户定，不算阻塞。
- **还没修好的**：都是小问题，名次和屏上数字都不受影响。
  - D6 / R1：西尼罗出处改成维基百科转引，窗口仍截到 2018 年。
  - N6：topic.md 有几处没跟上数据。
  - N7：3 张疱疹病毒插画构图雷同。
  - 另有几条新的轻微问题（R1–R6）。

上传前必须完成：

1. 用户确认选题卡、6 条单国计数的时效例外、N3 保留 AI 图。
2. 配乐完成、自动重渲以后，对新母版复审 §7 第 6 项，并重核 sha256、章节和发布稿。

## §7 审片清单

| # | 项目 | 结果 | 证据 |
|---|---|---|---|
| 1 | 名次连续、无重复，排序与 `data.json` 一致 | 通过 | 接触表逐卡看，出场顺序：#30、洞察 0、#29→#27、洞察 1、#26→#22、洞察 2、#21→#16、洞察 3、#15→#8、洞察 4、#7→#4、洞察 5、#3→#2、洞察 6、#1。共 30 张卡加 7 张洞察卡，after_rank 是 30 / 27 / 22 / 16 / 8 / 4 / 2。value 单调递减。 |
| 2 | 数值能追溯到 `sources.md`，统计期与片头一致 | 通过（附小问题） | 30 条显示值与 sources.md §2 一致；sources.md §3 已改为 561 和 17,809。联网核对 6 项都对上（见「数据抽查」）。残留问题在 #24 西尼罗：出处是维基百科转引，可 CDC 有 1999–2025 年的定稿数据（2026-09-16），窗口仍截到 2018（D6，以及 R1）。 |
| 3 | 国旗与国家对应 | 不适用 | `layout.flags = false`。计分板按 data.json 重算：Airborne 7、Mosquito & tick 6、Contact 5、Blood & sex 4、Food & water 4、Animals 4，与 233 s 的画面一致。6 个图标都不同（风、虫、手、水滴、杯、爪），D11 已修。 |
| 4 | 每张图都在 `assets.json`，许可可以接受 | 通过（附小问题） | 30/30 在账本里，sha256 全部相符。许可：公有领域 / PDM 9 张、Unsplash 9 张、CC BY 2.0 1 张、AI 生成 11 张。11 张 AI 图都标了 `synthetic: true`，方法、参考 PDB 和本地原图写在 `method` 和 `local_file` 字段，不进发布稿。#5 / #12 / #27 的 Codex 出图在 `ai_videos/paihangbang/request_log.md` 里有请求和结果记录（第 41545–41791 行一带）。小问题：账本许可从 `AI-generated (Codex image_gen…)` 改成了 `AI-generated`，渲染器靠前缀匹配照样放行，但与 data_contract 和 bible §4 规定的写法 `AI-generated (Codex image_gen)` 不一致（R2）。 |
| 5 | 文字不出框、不闪烁；手机全屏 3 秒内看清名称和数值 | 通过 | freezedetect 报的冻帧：片头 0.68–3.02 s，冠军段 224.98–225.50 和 225.82–226.33（光晕呼吸的低变化段，属正常），计分板 230.5–236.1，来源卡 236.5–240.1，片尾 240.5 s 以后。滚动段 5–223 s 没有冻帧。最长名称（Hand-foot-mouth viruses、COVID-19 (SARS-CoV-2)、Tick-borne encephalitis）都没有出框。640×360 下病毒名、主数值和 est. / reported 都清楚，署名行读不出来（同第 2 轮），所以 AI 的披露在手机上要靠 YouTube 合成标签和描述框。 |
| 6 | 音乐无爆音、高潮对上前 10 名、片尾干净 | **未检** | 当前是静音 AAC 轨。配乐重渲后要复审。 |
| 7 | 描述框来源与署名完整 | 通过（附轻微问题） | 描述 **3,370 / 5,000**，评论 1 有 3,796 字符（29 个链接），评论 2 有 5,147 字符（30 个链接）。三段都没有 `<` `>`，也没有 `_build`、盘符、`.png` 这类内部路径（N5 已修）。章节 0:00 / 1:17 / 2:25 / 3:39 / 3:50，逐个对帧都对（见下表）。#9 CC BY 2.0：描述框写了作者和许可名，评论 1 补了许可链接和来源页。清单写的是「Altered or synthetic content → 选 Yes」（N2 已修）。轻微问题见 R1、R3、R5。 |

### 章节时间点核对（按帧查看）

| 章节 | 时间 | 画面 | 结果 |
|---|---|---|---|
| Intro & #30–#21 | 0:00 | 片头标题 | 对 |
| #20–#11 | 1:17 | #21 HEV 在左，#20 Hantavirus 居中 | 对 |
| Top 10 | 2:25 | #11 RSV 在左，#10 Norovirus 居中（已放大） | 对 |
| No. 1 | 3:39 | 洞察卡 6 加 #1 Smallpox 进场 | 对 |
| How they spread | 3:50 | 计分板揭晓 | 对 |

### 其他段落

| 段落 | 结果 |
|---|---|
| 片头（0–5 s） | TOP 30、标题、口径行「Deaths · est. = modelled estimate · years vary by virus · Nov 2026」、来源行，都完整。 |
| 洞察卡 | 7 张都读得清，文字没有超出卡片。 |
| 冠军段 | Smallpox 居中，有光晕、奖杯和「No. 1 / 300M est.」。 |
| 计分板 | 数值正确，图标已经分开（D11 已修）。Food & water 用的 `glass-full` 是高脚杯，可能被读成「酒」（R6）。 |
| 来源卡 | 「SOURCES & CREDITS」、来源行、口径行，以及「Image credits: shown on each card and listed in the description」，不再写「Photo credits」。 |
| 片尾 | 只在顶部放了「Thanks for watching!」，中下部空着，可以放片尾元素。 |
| 封面 | 1280×720，用 #1–#3 的实拍图，没有 AI 图。「#1 300M」没有带 est.，和片中不一致（R4）。冠军剧透问题同前。 |

## 数据抽查（外部来源，本轮）

| 名次 | 项 | 片中 | 外部核对 | 结果 |
|---|---|---|---|---|
| 1 | Smallpox | 300M est.（1900–1977） | 核对路径：<br>- DOI 10.1016/j.vaccine.2011.06.080 经 PubMed（PMID 22188929）和 Crossref 核对：Henderson DA，The eradication of smallpox — An overview of the past, present, and future，Vaccine 2011;29 Suppl 4:D7–D9，与 data.json 的出处名一致。<br>- 全文是付费的，摘要里没有 300M。<br>- Our World in Data 天花页的注 17 正是引这篇作「an estimated 300 million people died of the disease」（20 世纪）。 | 对，N4 已修。小问题：sources.md 备注里的「'conservative'」一词出自 2009 年 Carnegie 讲座，不在这篇论文里，只是内部文档，不影响发布。 |
| 25 | TBE | 1,136（俄罗斯 2000–2022） | epidemvac.ru 的 PDF 可以下载。作者 Дзагурова Т. К. 等，Том 23, № 5。摘要原文：「668 (0,4%) и 1136 (1,6%) летальных исходов от ГЛПС и КЭ」，2000–2022 年。 | 对；作者已补上，D3 已修。 |
| 24 | West Nile | 2,330（美国 1999–2018） | 维基百科「List of West Nile virus outbreaks」写的是 1999–2018 年 50,830 例、2,330 死，引用 CDC「Final Cumulative Maps & Data for 1999–2018」（2019-10-09）。CDC 历史数据页现在覆盖 1999–2025，2026-09-16 定稿；本轮直连超时，累计数没能直接看到。 | 数对。但有一手来源（CDC 定稿页）却用维基百科作主值，窗口也过时（D6 部分修，另见 R1）。 |
| 13 | Hepatitis A（随机） | 锚点 107,920 / 39,280 | Europe PMC 全文 PMC8514357（Cao et al., Hepatol Int 2021）Table 1：Deaths Overall 1990 年 107.92 ×10³、2019 年 39.28 ×10³。正文写的「10.79 thousand… 3.93 thousand」是原文笔误，以表为准。 | 对 |
| 26 | MERS（随机） | 960 | ECDC 页面「Situation update, 29 September 2026」：自 2012 年起 2,649 例、960 死。 | 对。出处名里的日期「2 July 2026」偏旧，数字没变，不改也可以。 |
| 29 | CCHF（随机） | 469（土耳其 2002–2017） | PMC6335890 是 Blair et al., AJTMH 2019 的综述。检索结果显示其 Table 2 中 Turkey 2002–2017 为 10,333 例、469 死（PMC 直连被验证页拦住，经检索摘要核对）。 | 对 |

洞察卡：数据没变，第 2 轮逐条复算的结论沿用，7 张都成立。

## N3 自主决定的核查（AI 插画：#5 乙肝、#12 EB 病毒、#27 SARS）

topic.md 记录的理由逐条对照原候选图：

| 卡 | topic.md 的理由 | 实际看图 | 判断 |
|---|---|---|---|
| #5 乙肝 | PHIL 10755「主体只占画面角落、大半是空底」 | 确实大半是蓝色空底，橙色 Dane 颗粒聚在右上，左下另有 1 个。不过用 `image_focus` 对准颗粒团裁切，720×800 卡上仍能放下 4 个颗粒。这个办法理由里没提到。 | 大体属实，但漏了「可以裁切」这个替代办法 |
| #12 EB 病毒 | PHIL 10234「颗粒很重的黑白组织切片」 | 属实：灰度薄切片，病毒粒子小而稀疏。另一张彩色候选（NIAID c2）许可不明。 | 属实 |
| #27 SARS | PHIL 3466「黑白负染」 | 画质评价属实：灰度、颗粒密。但 3466 是**薄切片**，不是负染，措辞不准。其余彩色候选（PHIL 15528 等）带箭头或标注。 | 结论属实，措辞有小错 |

科学性和披露：

- #27：标注「AI-generated coronavirus particle」，没有冒充 SARS-CoV-1 的特定结构。冠状病毒的形态画得对，SARS-CoV-1 和 SARS-CoV-2 在形态上本来分不开，所以不算画错。但红刺加蓝灰底的配色仍然很像 CDC 那张著名的新冠插画，容易引来「放错图」的评论。第 2 轮建议至少换个配色，本轮没有做。
- #5：署名已改为「Illustration: AI-generated hepatitis B virus」，不再声称核心来自 PDB 6HTX。但剖面里看不到二十面体核心衣壳，是一团杂乱的蛋白，属于科学上简化过头（并入 N7）。不算错图。
- #12：二十面体衣壳加包膜，是可以接受的疱疹病毒示意，没画皮层（tegument）属于常见简化。
- 披露：卡上标了「Illustration: AI-generated…」，描述框写明 11 张是插画，上传清单选 Yes，账本标 `synthetic: true`，三处一致。

结论：理由诚实，记录可追溯，原图也留着可以随时换回，**定为用户决定项**，不算缺陷。建议用户决定时也看一下 #5 的裁切方案（PHIL 10755 对准颗粒团）和 #27 换配色这两个折中办法。

## 前几轮未关闭问题的状态

| ID | 级别 | 本轮状态 | 依据 |
|---|---|---|---|
| D3 | major | **已修** | #25 出处名改为「Dzagurova et al., Epidemiology and Vaccinal Prevention 2024;23(5)」，PDF 可以打开，数字对上；#1 已换 DOI。 |
| D6 | minor | **部分修** | 原问题 ①「藏起维基这一步」已改正：出处名如实写「as tabulated in Wikipedia's list…」，tier 记为 aggregator。仍有三处不对：<br>- bible §3.2 规定 aggregator 只在没有 primary 时作主值。维基页面自己引的就是 CDC「Final Cumulative Maps & Data for 1999–2018」，CDC 现在还有 1999–2025 的定稿数据。<br>- 窗口仍截到 2018，比 CDC 定稿数据少 7 年（按 CIDNI 讲座约 3,000 推算，少算约 700 人）。<br>- notes 写「last CDC-based cumulative total found」，与事实不符。<br>名次不受影响：补到 2025 年大约 3,000–3,200，仍低于 #23 的 3,632。 |
| D8 | minor | **基本修好** | 合成内容声明已与 bible 一致（选 Yes）。账本许可字符串缩短后与契约写法不一致，见 R2。 |
| D11 | minor | **已修** | 计分板 6 个分组用 6 个不同图标（`tally.icons`，渲染器 follow-up 009）。 |
| N1 | blocker | **已修** | 描述 3,370 字符，publish.md 不再标「⚠ 超长」。 |
| N2 | major | **已修** | 改 `publish.py` 后按账本 licence 或 `synthetic` 判断，清单选 Yes，描述框加了 AI 插画说明，来源卡改为「Image credits」。手机上读不到卡上的 AI 署名，这是版式限制，靠 YouTube 合成标签补，可以接受。 |
| N3 | major | **转为用户决定** | 见上节。topic.md 已记录代理在夜间授权下的自主决定和理由。用户确认前不要上传。 |
| N4 | minor | **已修** | DOI 可以解析，PubMed 和 Crossref 的题录与出处名一致。 |
| N5 | minor | **已修** | 评论 1 里 AI 图只写「AI illustration (Codex), AI-generated」，没有路径。 |
| N6 | minor | **部分修** | sources.md §3 已改为 561 / 17,809；topic.md 的「19 张实拍 + 11 张 AI」已改。topic.md 仍有过时内容：<br>- 计分板写「Food & water 5 / Contact 4」，实际是 4 / 5。<br>- 「6 张洞察卡」，实际 7 张。<br>- 屏上统计行写「Deaths · Best documented estimates · Nov 2026」，实际已改为 est. 口径行。<br>- 「维基百科只作交叉核对」与紧接着的「西尼罗主值由维基百科转引」自相矛盾。<br>这些不影响成片。 |
| N7 | minor | **部分修** | #5 署名已按建议改。#12 / #17 / #19 三张疱疹病毒插画构图完全相同（衣壳、半透明包膜、一圈突起，只是换了橙 / 蓝 / 紫），在 75–140 s 内出现三次；#5 剖面没有核心衣壳。 |

第 1 轮其余各项（D1、D2、D4、D5、D7、D9、D10、D12、D13）在第 2 轮已经关闭，本轮看到的画面和数据没有回退。

## 本轮新缺陷

1. **R1 · minor · publish.md 评论 2、data.json #24 · 发给观众的出处里写了内部操作说明**
   - 问题：#24 的出处名写着「CDC historic-data page blocks scripted access」。这是脚本取数时遇到的情况，观众看了会觉得莫名其妙，也像在给不用一手来源找借口。
   - 建议（与 D6 一起改）：
     - 出处改成 CDC 一手页面：CDC「West Nile virus: Historic Data」，或维基所引 CDC「Final Cumulative Maps & Data for 1999–2018」的存档链接，tier 改为 primary。
     - 如果有条件，人工打开 CDC 页面，把主值更新到 1999–2025。
     - 删掉「blocks scripted access」，notes 不要再写「last … found」。
     - 改完重跑 build、gen_sources、publish；如果改了数值还要重渲，可以和配乐重渲合并做。
2. **R2 · minor · assets.json（11 条 AI 图）· 许可字符串不符合契约写法**
   - 问题：`qc_fix_r2.py` 把 licence 统一改成了 `AI-generated`。data_contract 白名单和 bible §4 / follow-up 032 规定账本记作 `AI-generated (Codex image_gen)`。渲染器靠前缀照样放行，但以后按全名做审计或检索会漏掉这些条目。
   - 另外：#5 / #12 / #13 / #27 四条没有 `request_log` 字段，其余 7 条有。
   - 建议：licence 恢复为 `AI-generated (Codex image_gen)`，描述框的署名可以照常用这个；如果描述框长度紧，可以只在发布稿里缩写。4 条补上 `request_log` 字段，重跑 publish，确认描述框仍在 5,000 以内（现在约 3,370，加 11 × 16 字符没有问题）。
3. **R3 · 轻微 · publish.md · 标题和描述措辞**
   - 问题：
     - 标题自动生成为「Deadliest Viruses in History | Top 30 (2026)」，与 topic.md 定的「… | Top 30 by Death Toll」不同。按 bible §3.3，括号里的年份表示「统计期」，这里统计期各卡不同，「(2026)」容易被理解成「2026 年的数据」。
     - 描述框写「Per-item data sources and full photo credits with links: see the pinned comment」，但数据出处在评论 2（回复在置顶评论下面）。评论 1 的标题仍是「Full photo credits」，可 11 张不是照片。
     - 清单里写「卡上标 Illustration / Render」，Render 已经不用了。
   - 建议：上传时手动用 topic.md 的标题，或者 `publish` 传 `title` 参数。描述改为「…see the pinned comment and its reply」，评论 1 标题改为「Full image credits」。都只改发布稿，不用重渲。
4. **R4 · 轻微 · render/thumbnail.png · 封面「#1 300M」没有带 est.**
   - 问题：片中和冠军段都写「300M est.」，封面去掉了。封面也是对外数字，和 D2 的口径要一致。#2 的 52.4M、#3 的 44.2M 也都是 est.。
   - 建议：封面草图的数值药丸带上 est.，或者在封面加一行「est.」小字。也可以由用户人工改版封面时一起处理。
5. **R5 · 轻微 · publish.md 描述框 · 第 9 名 CC BY 2.0 的许可链接只在评论里**
   - 问题：描述框写了「(CC BY 2.0)」，许可 URL 和来源页在置顶评论 1 里。CC BY 要求「合理的方式」给出许可链接，放在置顶评论一般可以接受，但评论有被折叠或误删的风险。
   - 建议：只在描述框 #9 这一行后面补上 `https://creativecommons.org/licenses/by/2.0/`（约 45 字符）。不补也不算违规，属于加固。
6. **R6 · 轻微 · 计分板 Food & water 图标**
   - 问题：`glass-full` 画出来是高脚杯，配「Food & water」可能被读成「酒」。
   - 建议：换成 Tabler 的 `bottle` 或 `tools-kitchen-2`（需要先加进渲染器的 ICONS 和 assets/icons），下次重渲时改。

## 风险与用户决定项（不算缺陷）

- **U1 · N3 是否保留 3 张 AI 插画**（#5 乙肝在前 10 名内）。代理的理由大体属实，见上节。可以选：
  - 保留现状，需要用户确认；
  - #5 换回 PHIL 10755，用 `image_focus` 对准颗粒团裁切；
  - 保留 AI 图，但 #27 换掉红刺灰底的配色，避免被认成新冠插画。
  - 后两种需要重渲，可以和配乐重渲合并。
- **U2 · 选题卡还没获批**：topic.md 头部仍写「口径与名单待用户点头」，6 条单国计数的时效例外仍写「待用户认可」（同第 2 轮 R1、R3）。
- **U3 · 配乐自动重渲**：`music_watch.py` 仍在守候，01:14 状态是 queued，中间多次 unreachable。重渲以后 sha256、手机帧、章节和发布稿都要对新文件复核，§7 第 6 项那时才第一次检查。
- **U4 · 时长 4:18**：短于 bible 5–8 分钟的目标，不能插中插广告，是已知取舍。
- **U5 · 封面剧透**：封面直接展示 #1–#3（同前）。
- **U6 · 洞察卡间距**：after #30 和 after #27、after #4 和 after #2 都只隔 2–3 名（同前）。
- **U7 · 评论链接多**：两条评论各有约 30 个链接，可能被自动转入待审核。上传后请换一个账号确认能看到。
- **U8 · 评论区纠错点**：同前（流感 1918 的估计范围、乙肝和狂犬病按 WHO 口径更高、新冠超额死亡、麻疹「2 亿」）。另外，西尼罗截到 2018 年也可能被人指出。
- **U9 · 契约文档落后于渲染器**：渲染器已支持 `tally.icons` 和新增的病毒图标（rank_scroll follow-up 009），`data_contract.md` v1.4 还没写进去。这是系列层面的文档问题，不归本集。

## 观众视角

- 口径交代清楚：片头、每张卡的顶栏和底栏、洞察卡 0 都在讲 est. 和年份各不相同。计分板的图标分开后，一眼就能看出是在讲传播途径。
- 中段（14–135 s）AI 插画多，色彩统一，好看。但 #12、#17、#19 三张疱疹病毒插画在 1 分钟内重复出现，同一个模样只是换了颜色，细心的观众会觉得像「同一张图换色」。
- #27 SARS 一出来就像新冠的官方插画，可能有人在评论区说「放错图」。描述框已经说明是 AI 插画，可以回应，但不能完全避免。
- 没有甩锅或阴谋论表述；不挂国旗的决定没问题。

## 未能检查的范围

- 音乐与混音（§7.6）：静音轨，未检。
- 天花论文是付费全文，「300 million」是靠 OWID 的引用核对的，没有看到论文原文。
- CDC 西尼罗历史数据页直连超时，1999–2025 的累计数没有直接读到。
- PMC 直连被验证页拦住：#13 改用 Europe PMC 全文 API 核对，#29 经检索摘要核对。
- 其余 24 项本轮没有重新联网，数据与第 2 轮相同，结论沿用第 2 轮。
- 只看了每 2 s 的接触表和 24 张关键帧，没有逐帧查看；没有重做行位移的亚像素测量（渲染器版本仍是 0.2.0，滚动参数没变）。
- 没有在真机或 YouTube 播放器里实测。

## 外部核对来源（本轮）

- PubMed 22188929（Henderson, Vaccine 2011;29 Suppl 4:D7–9）：https://pubmed.ncbi.nlm.nih.gov/22188929/ ；Crossref：https://api.crossref.org/works/10.1016/j.vaccine.2011.06.080
- Our World in Data 天花页（注 17 引 Henderson 2011 作 300M 的出处）：https://ourworldindata.org/smallpox
- Дзагурова Т. К. и др., Эпидемиология и Вакцинопрофилактика 23(5)：https://www.epidemvac.ru/jour/article/download/2087/1073
- List of West Nile virus outbreaks（引 CDC「Final Cumulative Maps & Data for 1999–2018」）：https://en.wikipedia.org/wiki/List_of_West_Nile_virus_outbreaks
- CDC West Nile Historic Data（1999–2025）：https://www.cdc.gov/west-nile-virus/data-maps/historic-data.html （直连超时，经检索结果确认范围和定稿日期）
- Cao et al., Hepatol Int 2021（Europe PMC 全文）：https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8514357/fullTextXML
- ECDC MERS-CoV situation update, 29 September 2026：https://www.ecdc.europa.eu/en/middle-east-respiratory-syndrome-coronavirus/threats-and-outbreaks
- Blair et al., AJTMH 2019（PMC6335890 Table 2）：https://pmc.ncbi.nlm.nih.gov/articles/PMC6335890/table/t2

---

## 附：第 2 轮报告（存档）

独立审片 · 第 2 轮（fresh-context 子代理，2026-11-04）

# ep05 · Deadliest Viruses in History · 审片记录（第 2 轮）

- 审片对象：`render/ep05_deadliest_viruses_master.mp4`（sha256 `dc5dbb58…a3062`，与 manifest 一致）；1920×1080，60 fps，258.1 s，15,486 帧，H.264（约 1.63 Mbps）+ AAC 静音轨。时间线：片头 0–5、滚动 5–223.1、冠军 223.1–229.1、计分板 229.1–236.1、来源卡 236.1–240.1、片尾 240.1–258.1 s。
- 输入核对：`data.json`（`ae73aa8a…`）、`assets.json`（`ca1ff78c…`）的 sha256 与 manifest 一致；30 张图逐张重算 sha256，与账本、manifest 三方一致；30 张卡用图全部在账本里。成片就是用当前数据渲染的。
- 方法：
  - 抽帧：每 2 s 一张，拼成 6 张 5×5 接触表（带时间码），覆盖 0–258 s。另取 1080p 关键帧 32 张：片头、7 张洞察卡、11 张 AI 插画卡全部、前 10 名、冠军、计分板、来源卡、片尾。再取 640×360 手机尺寸帧 4 张，并查看封面。
  - 全片跑 freezedetect 和 volumedetect。
  - 图片：11 张 AI 插画逐张看图，核对是否像所标病毒；10 个 PDB 参考编号经 RCSB API 核对条目标题；新换的 #20 汉坦来源页（CDC PHIL 14271）联网核对图注与许可；`request_log.md` 核对 11 次 Codex 出图都有请求和结果记录。
  - 数据：逐条核对 data.json → sources.md → publish.md；联网抽查 16 个出处（优先本轮改过链接的条目，见「数据抽查」）；7 张洞察卡逐条复算。
  - 发布稿：重算描述框和两条评论的字符数，查看 `rank_scroll/publish.py` 的生成逻辑。
- 音频：全片静音（mean/max −91.0 dB）。音乐待制作，按设计如此，不算缺陷；§7 第 6 项**未检**。注意 `_build/music_watch.py` 正在等 Suno 任务，完成后会自动重渲母版、重跑 publish 和 thumb，本报告只对上面这个 sha256 有效。

## 结论：**修后可发布（当前文件不能直接上传）**

第 1 轮 13 条中 9 条已修、3 条部分修、1 条未修。核心问题 D1（手足口病数被标成 EV-A71）和 D2（方法交代）已经修好：片头口径行、「How to read」洞察卡、#1–#3 补 est. 都到位，屏上数字与出处一致。

但本轮出现 1 条阻塞和 2 条重大问题：

- **N1 · blocker**：描述框 5,402 字符，超过 YouTube 5,000 上限，publish.md 自己也标了「⚠ 超长」，上传时会被拒。
- **N2 · major**：合成内容声明前后矛盾。11 张卡用了 AI 插画，上传清单却写「本片无 AI 生成的逼真画面 → 选 No」，与 bible §4、topic.md（选 Yes）冲突。描述框也缺少「Illustration = AI 生成」的说明。作者说已修，实际 publish.md 是 00:21 由 `publish.py` 重新生成的，其中的判断逻辑漏判，修改没有留下来。
- **N3 · major**：#5 乙肝、#12 EB 病毒、#27 SARS 原本有可用的 CDC 实拍电镜图（第 1 轮评为「好 / 可接受」），本轮被换成 AI 插画。这违反 follow-up 034 / bible §4 032 的「实在找不到合适真实图才交 Codex」，而且 #5 在前 10 名里。

N1、N2 只改发布稿和生成脚本，不需要重渲。N3 如果换回实拍图需要重渲；如果用户同意保留 AI 图，需要留下用户签字记录。其余是小问题。

## §7 审片清单

| # | 项目 | 结果 | 证据 |
|---|---|---|---|
| 1 | 名次连续、无重复，排序与 `data.json` 一致 | 通过 | 接触表逐卡核对，出场顺序：#30、洞察 0（How to read）、#29→#27、洞察 1、#26→#22、洞察 2、#21→#16、洞察 3、#15→#8、洞察 4、#7→#4、洞察 5、#3→#2、洞察 6、#1。共 30 张卡加 7 张洞察卡，after_rank（30/27/22/16/8/4/2）与 data.json 一致；value 单调递减，无并列。 |
| 2 | 数值能追溯到 `sources.md`，统计期与片头一致 | 通过（附小问题） | 30 条显示值与 sources.md §2 一致，est. / reported / 无标记与 value_kind 一致。片头口径行改为「Deaths · est. = modelled estimate · years vary by virus · Nov 2026」，并加了洞察卡 0 说明读法。联网抽查 16 个出处，15 个能对上数（见下）。问题：#1 天花的出处链接返回 404（N4）；#24 的 2,330 实为维基百科根据 CDC 年表整理的数，出处却只写 CDC 历史数据页，而且窗口截在 2018（D6 部分修）；sources.md §3 洞察 2 的依据仍写「556 = 17,804」（N6）。 |
| 3 | 国旗与国家对应 | 不适用 | `layout.flags = false`。计分板按传播途径重算：Airborne 7、Mosquito & tick 6、Contact 5、Blood & sex 4、Food & water 4、Animals 4，与 229–236 s 的揭晓画面一致。手足口病已改归 Contact（D9）。 |
| 4 | 每张图都在 `assets.json`，许可可接受 | 通过（附问题） | 30/30 在账本里，sha256 全部相符。许可分布：公有领域 / PDM 9 张、Unsplash License 9 张、CC BY 2.0 1 张（#9，署名已补全）、`AI-generated (Codex image_gen…)` 11 张，都在 data_contract 白名单和渲染器 `ACCEPTED_LICENCE_PREFIXES` 里。11 次出图在 `ai_videos/paihangbang/request_log.md` 都有请求和结果记录。10 个 PDB 参考编号经 RCSB 核对，都对应所标病毒（6HTX 乙肝核心衣壳、6W19 EBV 衣壳、4QPI 甲肝、3J27 登革、6LGN VZV C-衣壳、5WSN 乙脑、6B43 KSHV 衣壳、2ZTN 戊肝 ORF2、3VBS EV71、5O6A TBEV 成熟颗粒）。#20 换成 CDC PHIL 14271，已联网核对：Sin Nombre 汉坦病毒 TEM，公有领域，卡上署名注明「(Sin Nombre virus)」。问题：有实拍图却换成 AI 图（N3）；合成内容声明口径（N2）。 |
| 5 | 文字不出框、不闪烁；手机全屏 3 秒内看清名称和数值 | 通过（附问题） | freezedetect 只在片头静止（0.68–3.02 s）、计分板定格（230.5–236.1）、来源卡（236.5–240.1）和片尾报冻帧，滚动段 5–223 s 没有冻帧。最长名称「Hand-foot-mouth viruses」「COVID-19 (SARS-CoV-2)」「Tick-borne encephalitis」都在卡内，没有出框。最长署名「Illustration: AI-generated, based on PDB 2ZTN (virus-like particle)」在 1080p 下完整可读。640×360 下病毒名、主数值、est. / reported 都清楚；但署名行（含「Illustration: AI-generated」）在手机上读不出来，手机观众只能靠描述框和 YouTube 合成标签知道这些图是 AI 生成的（见 N2）。 |
| 6 | 音乐无爆音、高潮对上前 10 名、片尾干净 | **未检** | 音乐待制作，当前是静音 AAC 轨。配乐重渲后需要复审本项，并重核 sha256。 |
| 7 | 描述框来源与署名完整 | **不通过** | 描述 **5,402 字符，超过 5,000**（N1）。没有 `<` `>`。评论 1 有 6,230 字符，评论 2 有 5,711 字符，都在 10,000 以内。章节 0:00 / 1:17 / 2:25 / 3:39 / 3:50，间隔 77/68/74/11 s，都 ≥10 s，逐个对帧都对得上（见下表）。#9 的 CC BY 署名已补全（描述框加评论 1 的许可链接）。「cross-checked」已删，scope_note 写了窗口局限。问题：合成内容一项选 No，描述框也没有说明「Illustration = AI 生成」（N2）；评论 1 把本地路径 `_build/gen/*.png` 当作「source file」发出去（N5）；评论 2 中 #1 链接 404（N4）。 |

### 章节时间点核对（按帧查看）

| 章节 | 时间 | 画面 | 结果 |
|---|---|---|---|
| Intro & #30–#21 | 0:00 | 片头标题 | 对 |
| #20–#11 | 1:17 | #21 HEV 在左，#20 Hantavirus 居中，#19 进场 | 对 |
| Top 10 | 2:25 | #11 RSV 在左，#10 Norovirus 居中（已放大） | 对 |
| No. 1 | 3:39 | 洞察卡 6 + #1 Smallpox 进场 | 对 |
| How they spread | 3:50 | 计分板揭晓（3:49.1 开始） | 对 |

### 其他段落

| 段落 | 结果 |
|---|---|
| 片头（0–5 s） | 有 TOP 30、标题、新口径行和来源行，D2 已解决。 |
| 洞察卡 0（约 4–12 s） | 「How to read: est. = modelled estimate, no tag = counted deaths. Years differ per card.」读得清。#8 的「reported」是第三种标记，卡上直接写了，可以接受。 |
| 冠军段（223–229 s） | Smallpox 居中，有光晕、奖杯和「No. 1 / 300M est.」，est. 已补上。 |
| 计分板（229–236 s） | 6 行数值正确，图标仍全是同一个地球（D11 未修）。 |
| 来源卡（236–240 s） | Sources、口径行、「Photo credits: shown on each card and listed in the description」、图标和字体许可。11 张是 AI 插画，「Photo credits」的说法不准（并入 N2）。 |
| 片尾（240–258 s） | 只在顶部放了「Thanks for watching!」，中下部全空，放片尾元素没问题。 |
| 封面 | 1280×720，用 #1–#3 的实拍图，没有 AI 图。冠军剧透问题仍在（R5）。 |

## 图片逐张核对（本轮变动部分）

19 张实拍图除 #20 外与第 1 轮相同（sha256 未变），结论沿用第 1 轮。下表只列本轮新换的 12 张。

| # | 病毒 | 新图 | 卡上标注 | 是否所标病毒 / 科学性 | 备注 |
|---|---|---|---|---|---|
| 5 | Hepatitis B | AI 插画，参考 PDB 6HTX（HBV 核心衣壳） | Illustration: AI-generated, core based on PDB 6HTX | 外层是带 HBsAg 突起的包膜剖面，可以读作 Dane 颗粒；但内部画成一团杂乱的蛋白，看不出二十面体核心衣壳，与「core based on 6HTX」对不上 | **原有 CDC PHIL 10755 实拍图（第 1 轮评「好」）被替换（N3）**；科学性偏松（N7） |
| 12 | EBV | AI 插画，参考 PDB 6W19（EBV 衣壳） | Illustration: AI-generated, based on PDB 6W19 capsid | 二十面体衣壳加半透明包膜和糖蛋白突起，是可以接受的疱疹病毒示意 | **原有 CDC PHIL 10234 实拍图被替换（N3）**；与 #17、#19 构图雷同（N7） |
| 13 | Hepatitis A | AI 插画，参考 PDB 4QPI | Illustration: AI-generated, based on PDB 4QPI structure | 无包膜二十面体小 RNA 病毒颗粒，可信 | D12 的处理方式，可以接受 |
| 14 | Dengue | AI 插画，参考 3J27 | …based on PDB 3J27 structure | 成熟黄病毒 E 蛋白「人字纹」表面，可信 | 配色与 #18、#25 已区分 |
| 17 | Varicella-zoster | AI 插画，参考 6LGN | …based on PDB 6LGN structure | 疱疹病毒衣壳加包膜，可信 | 见 N7 |
| 18 | Japanese encephalitis | AI 插画，参考 5WSN | …based on PDB 5WSN structure | 黄病毒人字纹，可信 | |
| 19 | KSHV | AI 插画，参考 6B43 | …based on PDB 6B43 structure | 疱疹病毒衣壳加包膜，可信 | 见 N7 |
| 20 | Hantavirus | CDC PHIL 14271（Goldsmith），Sin Nombre TEM | Photo: CDC / C. Goldsmith / Public domain (Sin Nombre virus) | 是汉坦病毒属（已联网核图注与许可） | 种与数据（中国 HFRS）不同，卡上已注明，可以接受 |
| 21 | Hepatitis E | AI 插画，参考 2ZTN | …based on PDB 2ZTN (virus-like particle) | 已注明是病毒样颗粒，措辞准确 | D13 已修 |
| 23 | Hand-foot-mouth viruses | AI 插画，参考 3VBS（EV71） | …based on PDB 3VBS structure | 肠道病毒二十面体颗粒，可信 | |
| 25 | TBE | AI 插画，参考 5O6A | …based on PDB 5O6A structure | 黄病毒人字纹，可信 | |
| 27 | SARS (SARS-CoV-1) | AI 插画，纯文字 prompt，无结构参考 | Illustration: AI-generated coronavirus particle | 冠状病毒形态正确 | **原有 CDC PHIL 3466 实拍图被替换（N3）**；红刺灰底的样子很像 CDC 那张著名的 SARS-CoV-2 插画，容易被认成新冠（N3） |

11 张 AI 图都标了「Illustration: AI-generated…」，没有任何一张自称照片；画面中没有文字、水印或比例尺。都是明显的 3D 插画风格，但质感接近写实渲染。

## 数据抽查（外部来源，本轮）

| 名次 | 项 | 片中 | 外部核对 | 结果 |
|---|---|---|---|---|
| 1 | Smallpox | 300M est.（1900–1977） | data.json 的 URL `carnegiecouncil.org/media/series/39/20091028-smallpox-the-death-of-a-disease` 返回 **404**（页面显示「Page Not Found」）。可用的页面是 `es.carnegiecouncil.org/media/podcast/20091028b-smallpox-the-death-of-a-disease-the-inside-story-of-eradicating-a-worldwide-killer` | 数对，**链接坏了（N4）** |
| 3 | HIV | 44.2M est. | WHO GHO HIV 主题页：「about 44.2 million [33.8–61.1 million] people have died」 | 对 |
| 6 | Rotavirus | 锚点 659,053 / 235,331 | PMC9585833（Du et al.）：「decreased from 659,053 … in 1990 to 235,331 … in 2019」 | 对（链接已从首页换成具体文章） |
| 7 | HPV | 锚点 184,527 / 280,479 | DOAJ cafdc2cb…：Hu Yao 等，Int J Clin Pract 2022，宫颈癌死亡 1990 年 184,527、2019 年 280,479（经检索结果核对，DOAJ 直连被拦） | 对 |
| 10 | Norovirus | 锚点 242,996 / 135,798 | PMC9247406 表格：Global 242996 / 135798 | 对 |
| 11 | RSV | 锚点 139,762 / 94,918 / 31,525 | PMC13190074 表格：RSV All ages Global 139,762 / 94,918 / 31,525 | 对 |
| 14 | Dengue | GBD 2021 锚点 | DOAJ fc984abe…：Zhang et al., PLoS NTD 2025 年 3 月（DOI 10.1371/journal.pntd.0012932），基于 GBD 2021 | 文章对；死亡锚点没能在摘要里看到 |
| 16 | Rabies | 2021 锚点 10,084 | Frontiers 1683863：「10,084 deaths」（2021） | 对；1990 锚点在补充材料里，未核 |
| 17 | VZV | 锚点 15,633 / 13,931 | Frontiers 1654535：「15,633 … in 1990 to 13,931 … in 2021」 | 对 |
| 18 | Japanese encephalitis | 275,792（中国 1950–2018） | BES 2021;34(3):175–183，Chen et al.：「2,364,177 JE cases and 275,792 deaths」（经检索结果核对，直连超时） | 对 |
| 20 | Hantavirus（图） | PHIL 14271 | CDC PHIL 页：Sin Nombre virus TEM，公有领域 | 对 |
| 23 | Hand-foot-mouth viruses | 3,632（中国 2008–2017） | 《疾病监测》2022;37(2):233–240，李佳玲等：「报告病例 18,183,889 例、死亡 3,632 例」（经检索结果核对，直连被拦） | 对，D1 已修 |
| 24 | West Nile | 2,330（美国 1999–2018） | CDC 历史数据页直连 403。按 CDC ArboNET 历年死亡数（1999–2015 合计 1,911，加 2016 年 106、2017 年 146、2018 年 167）加总得 2,330 | 数对；但见 D6 |
| 25 | TBE | 1,136（俄罗斯 2000–2022） | epidemvac.ru PDF：Дзагурова Т. К. 等，《Эпидемиология и Вакцинопрофилактика》Vol. 23 No 5：「668 (0,4%) и 1136 (1,6%) летальных исходов от ГЛПС и КЭ」，2000–2022 年 | 对；出处名仍没写作者和题名（D3 残留） |
| 28 | Marburg | 561 | 479 + 2 + 35 + 6 + 15 + 10 + 9 + 5 = 561 | 对，D7 已修 |
| 30 | Nipah | 435 | PMC11414670：「As of May 2024, there have been 754 confirmed human NiV cases with 435 deaths」 | 对，D3 错链已修 |

洞察卡复核（7 张）：

0. 「How to read: est. = modelled estimate, no tag = counted deaths. Years differ per card.」与各卡标记一致，成立。
1. 「Rare viruses are barely tracked: several counts here cover only one country.」成立（#18、#20、#23、#24、#25、#29 共 6 项是单国计数）。
2. 「Ebola, SARS, MERS and Marburg together killed fewer than 18,000 people.」成立：15,514 + 774 + 960 + 561 = 17,809。sources.md §3 仍写 556 / 17,804（N6）。
3. 「Rabies is almost always fatal once symptoms start, yet a vaccine has existed since 1885.」成立。
4. 「COVID-19's reported toll is 7.1M. Excess-death studies put it at 15–28M.」成立（WHO 14.83M 约等于 15M，The Economist 27–28.5M）。
5. 「Measles and HIV are neck and neck, and measles is only counted from 1980.」成立（43M vs 44.2M）。
6. 「Smallpox is the only human disease ever eradicated. Its last natural case was in 1977.」成立（用「natural」排除了 1978 年伯明翰实验室感染）。

## 第 1 轮问题复核

| ID | 级别 | 状态 | 依据 |
|---|---|---|---|
| D1 | blocker | **已修** | 卡名改为「Hand-foot-mouth viruses」，标签「Enteroviruses (EV-A71)」，主值 3,632 的出处改为李佳玲等 2022（jbjc DOI），已核对原文数字；notes 说明 EV-A71 是主要致死型。 |
| D2 | major | **已修** | 片头和每张卡顶部、底部都有口径行「est. = modelled estimate · years vary by virus」；加了洞察卡 0 说明读法；#1、#2、#3 补 est.；描述框 scope_note 写明窗口不同、旧的和被忽视的病毒被低估。来源卡没有单独加「被低估」那句，口径行已足够，不算残留。 |
| D3 | major | **部分** | 12 条首页 / 404 / 错链都换成具体文章，抽查 9 条能对上数。残留：#1 天花链接 404（N4，可能第 1 轮时就坏了，当时没抽查这条）；#25 出处名仍没有作者和题名（应为 Dzagurova T.K. et al., Epidemiology and Vaccinal Prevention 2024;23(5)）。 |
| D4 | major | **已修** | 卡上「Photo: NIAID/Rockefeller Univ. (Catanese, Rice) / CC BY 2.0」；账本、描述框、评论 1（带许可链接）都已补全。 |
| D5 | major | **已修（文字）** | 首句改为「Every number on screen is sourced…」，scope_note 补了局限说明。但描述总长超限，见 N1。 |
| D6 | minor | **部分** | 主值改为 2,330（1999–2018），加总与 CDC 年表一致。残留：① 2,330 实际取自维基百科对 CDC 年表的整理（qc_fix_r1.py 原记录写明「CDC data via Wikipedia」，topic.md 也这样写），修后出处名改成「as tabulated from CDC data」，链接只指向 CDC 历史数据页，页面上没有这个累计数，维基这一步被藏掉了；按 bible §3.2，aggregator 作主值应写明「据 X 整理」。② CDC 有 1999–2025 的年度数据，截到 2018 年白白少算约 700 人（窗口过时 8 年）。名次不受影响。 |
| D7 | minor | **已修** | 561，notes 和 source 名都写明 9 confirmed + 5 probable。 |
| D8 | minor | **部分** | 账本许可已统一为 `AI-generated (Codex image_gen…)`，符合 data_contract 白名单，PDB 结构图不再冒充 AI 生成。但 publish.md 上传清单仍是「无 AI 生成的逼真画面 → 选 No」，与 bible §4 / topic.md 冲突，问题比第 1 轮更重（11 张 AI 图），升级为 N2。 |
| D9 | minor | **已修** | #9 改为 Hepacivirus；#17 改为 Vaccine since 1986；#23 归 Contact；#8 改为 COVID-19 (SARS-CoV-2)，#27 改为 SARS (SARS-CoV-1)；#20 卡上注明 Sin Nombre virus。 |
| D10 | minor | **已修（账本）** | #6 账本改为 PHIL 178 页面和 TIFF。`_build/reselect/picks.json`（23:00）仍是过期文件，未处理，不影响成片。 |
| D11 | minor | **未修** | 计分板 6 行仍是同一个地球图标。 |
| D12 | minor | **已修** | 甲肝改为 AI 插画（参考 4QPI），主体饱满。 |
| D13 | minor | **已修** | PDB 渲染图全部换成插画，配色各不相同；「capsid」改为「structure」；#21 注明 virus-like particle。新出现的疱疹病毒插画雷同，见 N7。 |

## 本轮新缺陷

1. **N1 · blocker · publish.md 描述框 · 5,402 字符，超过 YouTube 5,000 上限**
   - 问题：11 条 AI 图署名把账本的 author 和 licence 原样拼在一起，每条约 200 字符，而且「AI-generated」重复两遍；描述框里一共出现 22 次「AI-generated」。publish.md 标题处自己已经标了「⚠ 超长」。
   - 建议：
     - 改 `publish.py` 的 compact 署名：AI 图一律输出短格式，如「#5 Hepatitis B: AI illustration (Codex image_gen), ref. RCSB PDB 6HTX」，大约能省 1,500 字符。
     - 或者把账本 author 改短，例如「AI illustration (Codex image_gen); ref. render of PDB 6HTX」。
     - 改完重跑 `python -m rank_scroll publish`，确认 ≤ 5,000。
     - 不要手改 publish.md：`music_watch.py` 配乐完成后会重跑 publish，手改会被覆盖。
2. **N2 · major · publish.md 上传清单、描述框、来源卡、手机端 · 合成内容声明前后矛盾，作者声称已修但实际没有**
   - 问题：
     - 上传清单写「Altered or synthetic content：本片无 AI 生成的逼真画面 → 选 No」。bible §4（follow-up 020 / 032 / 024）要求 AI 图上传时勾选合成内容声明，topic.md 写的也是「上传时合成内容声明选 Yes」。
     - 原因在 `projects/rank_scroll/rank_scroll/publish.py`：第 108 和 125 行用 compact 署名里有没有「Illustration」来判断，而 compact 取的是账本 author（「AI-generated with Codex image_gen…」），不含这个词。所以判断落空，选成 No，描述框的「'Illustration' = AI-generated image, not a photo」说明也没加上。
     - 来源卡写「Photo credits: shown on each card…」，11 张不是照片。
     - 卡上的「Illustration: AI-generated」在 640×360 下读不出来，手机观众只能靠 YouTube 合成标签和描述框得知。
   - 建议：
     - `publish.py` 改为按账本 `synthetic: true` 或 licence 以「AI-generated」开头来判断。
     - 清单改为选 **Yes**，与 bible 一致；描述框首段加一句「11 virus images are AI-generated scientific illustrations (labelled on screen), not micrographs」。
     - 来源卡改为「Image credits (photos and AI illustrations)…」，需要重渲，可以和配乐重渲合并做。
     - 改完重跑 publish。
3. **N3 · major · #5 Hepatitis B（约 178–190 s）、#12 EBV（约 128–140 s）、#27 SARS（约 14–26 s）· 有可用实拍图却换成 AI 插画**
   - 问题：
     - 三张卡第 1 轮用的是 CDC PHIL 实拍电镜图（10755 Dane 颗粒，第 1 轮评「好」；10234 EBV 和 3466 SARS，评「可接受」）。本轮账本写「自审：网上可商用图画面空 / 黑白颗粒重 → Codex 出图」，没有用户签字记录。
     - follow-up 034 和 bible §4 032 的规则是「实在找不到合适的高质量真实图，才把最后出图交给 Codex」。在一个以「每个数字都有出处」为卖点的科普榜单里，把真实电镜图换成生成图，会削弱可信度。#5 还在前 10 名。
     - #27 SARS 插画只用了文字 prompt，红刺灰底的构图和配色很像 CDC 那张广为流传的 SARS-CoV-2 插画，观众容易认成新冠，正好和 #8 混淆（D9 刚把这两个名字分开）。
   - 建议：
     - 首选：#5、#12、#27 换回 CDC PHIL 10755、10234、3466（候选库 `_build/reselect/cand/04_05_hbv/h10755.jpg`、`11_12_ebv/p10234.jpg`、`26_27_sars/p3466.jpg` 都还在；`_build/old_img/` 是空的），重渲。
     - 如果用户认可 AI 图更好，就在 topic.md 或 follow-up 里留下用户签字记录；#27 至少换掉红刺灰底的配色，避开 CDC 新冠插画的样子。
4. **N4 · minor · data.json / sources.md / 评论 2 · #1 天花出处链接 404**
   - 问题：`https://www.carnegiecouncil.org/media/series/39/20091028-smallpox-the-death-of-a-disease` 打开是「Page Not Found | 404」。出处名里的「Vaccine 2011」也没有链接。
   - 建议：改为 `https://es.carnegiecouncil.org/media/podcast/20091028b-smallpox-the-death-of-a-disease-the-inside-story-of-eradicating-a-worldwide-killer`（第 1 轮已核对该页有「conservatively about 300 million」），重跑 gen_sources 和 publish。
5. **N5 · minor · publish.md 评论 1 · AI 图的「source file」是本地路径**
   - 问题：11 条 AI 图署名的末尾是 `_build/gen/hbv_codex_v1.png` 这类仓库内部路径，观众点不开，还暴露了内部目录结构。
   - 建议：AI 图改为「generated for this video; structural reference: https://www.rcsb.org/structure/6HTX」；#27 写「text prompt only」，不附链接。
6. **N6 · minor · sources.md §3、topic.md · 文档没跟上数据**
   - 问题：
     - sources.md §3 洞察 2 的依据仍是「556 = 17,804」，应为 561 和 17,809。
     - topic.md 写「22 张实拍 + 8 张 AI」，实际是 19 张实拍 + 11 张 AI。
     - topic.md 写「仅西尼罗病毒的 2,330 一条交叉核对值来自维基」，现在 2,330 是主值。
   - 建议：`gen_sources.py` 的洞察依据改成从 data.json 计算，不要写死；topic.md 同步改数。
7. **N7 · minor · 插画观感与准确度**
   - 问题：
     - #5 乙肝插画内部是一团杂乱的蛋白，看不出二十面体核心，与署名「core based on PDB 6HTX」对不上。
     - #12 EBV、#17 VZV、#19 KSHV 三张疱疹病毒图构图相同（衣壳、半透明包膜、一圈突起），在 75–140 s 内出现三次。
   - 建议：#5 如果按 N3 换回实拍图，问题自然消失；保留的话，把署名改为「AI-generated hepatitis B virus」。三张疱疹病毒图各换一个视角或剖面，例如其中一张只画衣壳。

## 风险提示（不算缺陷，由用户决定）

- **R1 选题卡仍未获批**：topic.md 头部仍写「口径与名单待用户点头」，6 条单国计数的时效例外也写着「待用户认可」。发布前请用户确认。
- **R2 配乐后自动重渲**：`_build/music_watch.py` 会在 Suno 任务完成后自动重渲母版、重跑 publish 和 thumb。重渲后 sha256 会变，本报告不再对应新文件；§7 第 6 项和 N1、N2 的修复都要在新产物上复核。
- **R3 西尼罗与单国窗口偏旧**：#24 截到 2018，#20 截到 2007，#23 和 #29 截到 2017，与 bible §3.3「超过 18 个月未更新不用」冲突，按例外处理需要用户认可（同第 1 轮 R2）。
- **R4 评论区纠错点**：同第 1 轮 R3（流感 1918 的估计范围、乙肝 / 狂犬病按 WHO 口径更高、新冠超额死亡、麻疹「2 亿」的说法）。另加一条：观众可能指出「11 张不是真图」，描述框需要按 N2 预先说明。
- **R5 封面剧透**：封面直接展示 #1 300M、#2、#3，同第 1 轮。
- **R6 洞察卡间距**：after #30 与 after #27、after #4 与 after #2 都只隔 2–3 名，不符合契约「每 8–12 名一条」的建议节奏。观感上片头连出两张字卡（约 4–12 s 和 24–34 s），影响不大。
- **R7 时长 4:18**：短于 bible 5–8 分钟目标，不能插中插广告，是已知取舍。
- **R8 置顶评论链接多**：评论 1 有 29 个链接，评论 2 有 30 个，可能被自动转入待审核。上传后请用另一个账号确认能看到。

## 观众视角

- 口径交代比第 1 轮清楚很多：片头、每卡顶栏、洞察卡 0 都在讲「est. 是什么、年份各不相同」，评论区「in History 却只算 12 年」这类批评有了现成的回答。
- AI 插画色彩饱满、统一，中段（14–135 s）比第 1 轮的灰度结构图好看。但实拍和插画交替出现，懂行的观众会问「哪些是真的」。卡上的小字署名在手机上看不到，所以描述框里的说明（N2）是必要的。#27 SARS 那张一看就像新冠的官方插画，容易引来「放错图」的评论（N3）。
- 措辞上仍然没有甩锅或阴谋论表述，不挂国旗的决定是对的。

## 未能检查的范围

- 音乐与混音（§7.6）：静音轨，未检。
- 外部抽查覆盖 16 项。jbjc、besjournal、doaj 直连被拦或超时，改用检索结果中的摘要核对；CDC 西尼罗历史数据页返回 403，2,330 是按 CDC 年度数（据本审片掌握的公开数字）复算的，没有在页面上直接看到；CDC 马尔堡页返回 403。#2、#4、#5、#8、#9、#12、#13（锚点数字）、#15、#19、#21、#22、#26、#27、#29 本轮没有回原文核对。
- 只看了每 2 s 的接触表和 32 张关键帧，没有逐帧查看；本轮没有重做行位移的亚像素测量（渲染器版本 0.2.0 未变，第 1 轮已测）。
- 没有在真机或 YouTube 播放器里实测。

## 外部核对来源（本轮）

- 李佳玲等，2008–2017 年中国手足口病发病与死亡趋势，《疾病监测》2022;37(2)：https://www.jbjc.org/en/article/doi/10.3784/jbjc.202107090395
- Chen et al., Japanese Encephalitis in China 1950–2018, BES 2021;34(3)：https://www.besjournal.com/cn/article/doi/10.3967/bes2021.024
- Дзагурова Т. К. и др., Эпидемиология и Вакцинопрофилактика 23(5)：https://www.epidemvac.ru/jour/article/download/2087/1073
- Nipah 754 例 / 435 死：https://pmc.ncbi.nlm.nih.gov/articles/PMC11414670/
- RSV GBD 2021：https://pmc.ncbi.nlm.nih.gov/articles/PMC13190074/
- 轮状病毒 GBD 2019：https://pmc.ncbi.nlm.nih.gov/articles/PMC9585833/
- 诺如病毒 GBD 2019：https://pmc.ncbi.nlm.nih.gov/articles/PMC9247406/
- 狂犬病 GBD 2021：https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1683863/full
- VZV GBD 2021：https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1654535/full
- 宫颈癌 1990–2019（Hu Yao 等）：https://doaj.org/article/cafdc2cb127642cea4929c407d6b0af1
- 登革 GBD 2021（Zhang et al., PLoS NTD 2025）：https://doaj.org/article/fc984abe412d454ba203a63e2ab18cf9
- WHO GHO HIV：https://www.who.int/data/gho/data/themes/hiv-aids
- CDC PHIL 14271：https://wwwn.cdc.gov/phil/Details.aspx?pid=14271
- Carnegie Council（data.json 链接 404）：https://www.carnegiecouncil.org/media/series/39/20091028-smallpox-the-death-of-a-disease ；可用页面：https://es.carnegiecouncil.org/media/podcast/20091028b-smallpox-the-death-of-a-disease-the-inside-story-of-eradicating-a-worldwide-killer
- RCSB PDB 条目 API（6HTX、6W19、4QPI、3J27、6LGN、5WSN、6B43、2ZTN、3VBS、5O6A）：https://data.rcsb.org/rest/v1/core/entry/<ID>

---

## 附：第 1 轮报告（存档）

独立审片（fresh-context 子代理，2026-11-03）

# ep05 · Deadliest Viruses in History · 审片记录

- 审片对象：`render/ep05_deadliest_viruses_master.mp4`（sha256 `abb29545…a5df529`，与 manifest 一致）；1920×1080，60 fps，253.4 s，15,206 帧，H.264（约 1.68 Mbps）+ AAC 静音轨。
- 输入核对：`data.json`（`f1bd0869…`）、`assets.json`（`e490b71e…`）的 sha256 与 manifest 记录一致，30 张图的 sha256 与账本逐一相符。成片就是用当前数据渲染的。
- 方法：
  - 抽帧：每 2 s 一张，拼成 6 张 5×5 接触表，覆盖 0–253 s。另取 1080p 关键帧约 20 张：片头、6 张洞察卡、#30–#28、前 10 名、冠军段、计分板、来源卡、片尾、5 个章节时间点，以及两条署名行的放大裁切。再取 640×360 手机尺寸帧 3 张，并查看封面。
  - 运动：在 40、100、150、180 s 各取 6 帧连续帧，做行均值位移匹配。全片另跑 freezedetect 和 volumedetect。
  - 图片：把 30 张成片用图与 `_build/reselect/cand/*` 的候选逐张做相似度匹配，核对账本来源页与实际文件是否一致；再联网打开 7 个来源页，直接核对图注与许可。
  - 数据：逐条核对 data.json → sources.md → publish.md；联网抽查 9 项数字（见「数据抽查」）。
- 音频：全片静音（mean/max −91 dB）。音乐还没做，按设计如此，不算缺陷；§7 第 6 项未检。

## 结论：**修后可发布**

当前文件**不能直接上传**。阻塞问题有 1 条（D1：#23 卡把「手足口病全部死亡」标成 EV-A71 死亡，引用的出处也对不上）。另有 4 条重大问题：

- D2：排名方法在屏幕上没有交代。各卡统计窗口长短不一，`est.` 的含义也没说明，标题却是「in History」。
- D3：约三分之一的数据出处是期刊首页、错链或 404，观众核对不了。
- D4：#9 丙肝图是 CC BY 2.0，署名不完整。
- D5：描述框写「每个数字都经过交叉核对」，实际有 10 项没有交叉核对；口径局限也没写进描述框。

图片方面：30 张图都是所标病毒（或该病毒真实结构数据的渲染图），没有发现错图、水印或印在图上的标签。格式和滚动都正常。上面几条都能通过改数据、改文案、重渲修好，没有结构性问题。

## §7 审片清单

| # | 项目 | 结果 | 证据 |
|---|---|---|---|
| 1 | 名次连续、无重复，排序与 `data.json` 一致 | 通过 | 接触表逐卡核对，出场顺序是 #30→#28、洞察 1、#27→#23、洞察 2（after #22 的位置见下）、#22→#17、洞察 3、#16→#9、洞察 4、#8→#5、洞察 5、#4→#2、洞察 6、#1，共 30 张卡加 6 张洞察卡，和 data.json 倒序一致。脚本复核 value 单调递减、无并列。洞察卡位置（after 27/22/16/8/4/2）都和 data.json 一致。 |
| 2 | 数值能追溯到 `sources.md`，统计期与片头一致 | **不通过** | 30 条都能在 sources.md §2 找到同名条目，显示值与原值取整一致（est. 2 位有效数字，documented 原样或 3 位）。问题有三类：① #23 显示值与卡名不符，引用 URL 也不是含该数的文献（D1）；② 10 条 URL 只指到期刊或机构首页，#20 是 404，#30 疑似错链，#25 只有俄文期刊首页（D3）；③ 片头口径行只写「Best documented estimates · Nov 2026」，不同窗口和 est. / documented 的区别在屏幕上没有任何说明（D2）。 |
| 3 | 国旗与国家对应 | 不适用 | 本期 `layout.flags = false`，不挂国旗。计分板按传播途径累计：重算得 Airborne 7、Mosquito & tick 6、Food & water 5、Blood & sex 4、Contact 4、Animals 4，与 224–231 s 的揭晓画面一致。分类上有一处可商榷，见 D9。 |
| 4 | 每张图都在 `assets.json`，许可可接受 | 部分通过 | 30/30 在账本里，sha256 全部相符。许可分布：公有领域 / PDM 13 张、Unsplash License 9 张、CC BY 2.0 1 张（#9）、PDB 坐标自渲染 7 张。没有 NC、ND、GFDL-only 或来源不明的图。与候选库逐张匹配，账本来源页和实际文件一致（相似度 1.000）；只有 #6 轮状病毒的实际文件是 CDC PHIL 178 原始 TIFF，账本却记成 USGS 页面加缩略图 URL（D10）。问题：#9 的 CC BY 署名不完整（D4）；7 张渲染图在账本里记成「AI-generated」，与 data_contract 的白名单和 publish.md 的合成内容勾选口径不一致（D8）。 |
| 5 | 文字不出框、不闪烁；手机全屏 3 秒内看清名称和数值 | 通过（附小问题） | 实测 40/100/150/180 s 每帧整 2 px 位移，不会出现亚像素闪烁。freezedetect 只在片头静止段（0.7–3.0 s）、计分板定格、来源卡、片尾报冻帧，滚动段 5–218 s 没有冻帧或掉帧。最长名称「Tick-borne encephalitis」「Kaposi sarcoma virus」「DEATHS · 4 PANDEMICS, 1918–2009」都在卡内，没有出框。640×360 下病毒名、主数值和 est. / reported 标记都清楚；署名行和标签行在手机上读不出来，「Render… not a photo」说明因此在手机上看不到（见 D8）。前 10 名放大约 1.06×，冠军段有光晕、奖杯和 No. 1 300M 面板。 |
| 6 | 音乐无爆音、高潮对上前 10 名、片尾干净 | 未检 | 音乐待制作，当前是静音 AAC 轨。 |
| 7 | 描述框来源与署名完整 | **部分通过** | 描述 4,469 字符（≤5,000），没有 `<` `>`。置顶评论 1 有 5,855 字符，评论 2 有 5,397 字符，都在 10,000 以内。描述含 30 条图片署名，渲染图注明「3D render from public structure data, not a photo」。章节 5 个，从 0:00 开始，间隔 73/68/73/11 s，都 ≥10 s，逐个看帧都对得上（见下表）。问题：#9 CC BY 署名不完整（D4）；「Every number… cross-checked」不实，口径局限没有写（D5）；评论 2 把首页、404 和错链当出处发出去（D3）；上传清单的合成内容一项与 bible 冲突（D8）。 |

### 章节时间点核对（按帧查看）

| 章节 | 时间 | 画面 | 结果 |
|---|---|---|---|
| Intro & #30–#21 | 0:00 | 片头标题 | 对 |
| #20–#11 | 1:13 | #21 HEV 正在出画，#20 Hantavirus 居中 | 对 |
| Top 10 | 2:21 | #11 RSV 在左，#10 Norovirus 居中（已放大） | 对 |
| No. 1 | 3:34 | 洞察卡 6 + #1 Smallpox 进场 | 对 |
| How they spread | 3:45 | 计分板揭晓（条形图正在生长） | 对 |

### 其他段落

| 段落 | 结果 |
|---|---|
| 片头（0–5 s） | 有 TOP 30、标题、「Deaths · Best documented estimates · Nov 2026」和来源行；没有说明排名方法（D2）。约 4.5 s 时标题已淡出、卡片进场，没有出现叠压。 |
| 冠军段（218–224 s） | Smallpox 居中，有光晕，右侧是奖杯和「No. 1 / 300M」。天花电镜图本身偏灰绿、低对比，作为冠军图略弱，不算缺陷。 |
| 计分板（224–231 s） | 6 行数值正确。每行图标都是同一个地球图标，没有按传播途径区分（D11）。 |
| 来源卡（231–235 s） | Sources、口径行、照片署名说明、图标和字体许可都能读；没有交代 est. 的含义（D2）。 |
| 片尾（235–253 s） | 只在顶部放了「Thanks for watching!」，中下部全空，放 YouTube 片尾元素空间足够。 |

## 图片逐张核对

核对依据：每张图先和候选库做相似度匹配，确认账本来源页就是实际文件的来源；图注取自选图时记录的原始图注（`_build/reselect/` 里的 `why` 字段）。其中 #2、#3、#7、#9、#12、#13、#27 七个来源页本次重新联网打开核对。

| # | 病毒 | 图 | 是否所标病毒 | 质量 / 备注 |
|---|---|---|---|---|
| 1 | Smallpox | CDC PHIL 10144，Murphy，负染 TEM | 是（天花病毒） | 灰绿低对比，可接受 |
| 2 | Influenza | NIH Flickr 54270398294，甲型 H1N1 着色 TEM | 是（已核 Flickr 图注） | 好 |
| 3 | HIV | NIH Flickr 20683459455，HIV（黄）攻击 T 细胞 SEM | 是（已核，PDM） | 好 |
| 4 | Measles | CDC PHIL 10707，单个麻疹病毒粒子 | 是 | 好 |
| 5 | Hepatitis B | CDC PHIL 10755，Dane 颗粒 | 是 | 好 |
| 6 | Rotavirus | CDC PHIL 178（账本误记为 USGS，D10） | 是 | 好 |
| 7 | HPV | Unsplash / NIAID IRF，HPV 颗粒（品红） | 是（已核 Unsplash 图注：「HPV virus particles (magenta) harvested and purified from cell culture supernatant」） | 好 |
| 8 | SARS-CoV-2 | NIH Flickr 49919836657，NIAID IRF 患者分离株 | 是 | 好 |
| 9 | Hepatitis C | NIH Flickr 53077378506，单个 HCV 病毒粒子着色 TEM | 是（已核） | 好；**署名不完整（D4）** |
| 10 | Norovirus | CDC PHIL 10706 | 是 | 好 |
| 11 | RSV | Unsplash / NIAID，A549 细胞上 RSV 的 SEM | 是 | 好 |
| 12 | EBV | CDC PHIL 10234，Murphy | 是（已核：「numerous Epstein-Barr virus (EBV) virions」） | 灰度，可接受 |
| 13 | Hepatitis A | CDC PHIL 2739，Partin | 是（已核：「small cluster of… hepatitis A virus」） | **弱**：灰度、颗粒感重，主体只占画面中央一小块，约 112–128 s（D12） |
| 14 | Dengue | 渲染图，PDB 3J27（DENV-2 成熟病毒粒子 cryo-EM） | 是（结构数据） | 见 D8 / D13 |
| 15 | Yellow fever | Unsplash / NIAID，Vero E6 细胞内质网中的黄热病毒 | 是（据记录图注） | 病毒颗粒小、主体是细胞，可接受 |
| 16 | Rabies | Unsplash / NIAID，仓鼠肾细胞上的狂犬病毒（红） | 是（据记录图注；页面自动标题「blood cells」不对，可忽略） | 好 |
| 17 | Varicella-zoster | 渲染图，PDB 6LGN（VZV C-衣壳） | 是 | 与 #19 外观几乎一样（D13） |
| 18 | Japanese encephalitis | 渲染图，PDB 5WSN（JEV 成熟病毒粒子） | 是 | 见 D13 |
| 19 | KSHV | 渲染图，PDB 6B43（KSHV 衣壳） | 是 | 见 D13 |
| 20 | Hantavirus | CDC PHIL 1136，Sin Nombre 病毒 | 是汉坦病毒属，但不是本卡数据对应的种 | 卡上数据是中国 HFRS（汉滩 / 汉城病毒），图是美洲的 Sin Nombre（D9） |
| 21 | Hepatitis E | 渲染图，PDB 2ZTN（基因 3 型 ORF2，T=1 病毒样颗粒） | 是 HEV 蛋白，但不是天然病毒粒子 | D13 |
| 22 | Ebola | Unsplash / CDC，Murphy 1976 年分离株「6 字形」 | 是 | 好 |
| 23 | EV-A71 | 渲染图，PDB 3VBS（EV71 成熟病毒粒子晶体结构） | 是 | 好 |
| 24 | West Nile | Unsplash / NIAID IRF，Vero E6 细胞内的西尼罗病毒 | 是（据记录图注） | 好 |
| 25 | TBE | 渲染图，PDB 5O6A（TBEV 成熟病毒粒子） | 是 | 见 D13 |
| 26 | MERS | CDC PHIL 18113，NIAID，5 个 MERS-CoV 粒子 | 是 | 好 |
| 27 | SARS | CDC PHIL 3466，Goldsmith / Ksiazek 2003 | 是（已核：图注写「coronavirus」，页面分类为 SARS，2003 年 SARS 分离株） | 灰度，可接受 |
| 28 | Marburg | Unsplash / NIAID IRF，马尔堡病毒（橙） | 是 | 好 |
| 29 | CCHF | Unsplash / NIAID，CCHF 病毒（黄）SEM | 是 | 好 |
| 30 | Nipah | Unsplash / NIAID IRF，Vero 细胞旁的尼帕病毒（红） | 是 | 好 |

渲染图的科学性：7 个 PDB 条目都对应所标病毒，渲染方式是 Cα 珠点、按链着色。看上去明显是分子模型，不像照片。1080p 下卡上署名「Render: PDB xxxx capsid structure (CC0 data), not a photo」读得清（已裁切放大核对 70 s 和 116 s）。抽帧中所有图片都没有发现水印、比例尺、箭头或印在图上的文字。

## 数据抽查（外部来源）

| 名次 | 项 | 片中 | 外部核对 | 结果 |
|---|---|---|---|---|
| 1 | Smallpox | 300M（1900–1977） | Henderson 在 Carnegie Council 讲座中说，20 世纪死亡「conservatively about 300 million」；有的资料给 300–500M | 数对，但这是**估算**，卡上没有 est. 标记（D2） |
| 3 | HIV | 44.2M（1981–2025） | WHO HIV 情况说明书（2026-07-27）：「having claimed an estimated 44.2 million lives to date」 | 对 |
| 4 | Measles | 43M est.（锚点 1980 年 2.6M/年） | WHO 情况说明书旧版：「In 1980, before widespread vaccination, measles caused an estimated 2.6 million deaths each year」 | 锚点对；1980→2000 线性插值较粗，已标 est. |
| 20 | Hantavirus | 46,427（中国 1950–2007） | Zhang et al., EID 2010;16(8):1195–1203：1,557,622 例、46,427 死 | 数对；**data.json 的 URL（…/09-1745_article）返回 404**，正确文章编号是 09-0470（D3） |
| 23 | EV-A71 | 3,632（中国 2008–2017） | 李佳玲等，《疾病监测》2022：2008–2017 年手足口病**共报告死亡 3,632 例**（全部肠道病毒） | **数是手足口病总死亡，不是 EV-A71 死亡**（D1） |
| 24 | West Nile | 3,000（美国 1999–2024） | CDC ArboNET 历史数据页（1999–2025，2026-09-16 定稿）有一手数据；CDC 1999–2015 表为 1,911 死 | 量级合理；但用的是一份护理讲座 PDF 的「约 3,000」，有一手来源没用（D6） |
| 26 | MERS | 960（2012–2026） | ECDC 2026-08-03：累计 2,649 例、960 死；2026-03-02 为 959 死 | 对 |
| 28 | Marburg | 556（含 Ethiopia 2025 计 9） | 埃塞俄比亚 2026-01-26 宣布疫情结束：确诊 14 例、确诊死亡 9 例，另有 5 例死亡为 probable | 口径不一：赤道几内亚计入了 probable，埃塞俄比亚没有；按 notes 口径应为 561（D7），不影响名次 |
| 30 | Nipah | 435（1998–2024） | 754 例、435 死（截至 2024-05）出自 PMC11414670 | 数对；**data.json 引的是 PMC10413696**（2023 年编号，本次打不开、无法核实），疑似错链（D3） |

洞察卡核对：

1. 「Rare viruses are barely tracked: several counts here cover only one country.」成立：#18、#20、#23、#24、#25、#29 共 6 项是单国计数。
2. 「Ebola, SARS, MERS and Marburg together killed fewer than 18,000 people.」成立：15,514 + 774 + 960 + 556 = 17,804。Marburg 改为 561 后合计 17,809，仍成立。
3. 「Rabies is almost always fatal once symptoms start, yet a vaccine has existed since 1885.」成立（WHO 狂犬病情况说明书；巴斯德 1885 年接种 Joseph Meister）。
4. 「COVID-19's reported toll is 7.1M. Excess-death studies put it at 15–28M.」基本成立：WHO 超额死亡 14.83M 只覆盖 2020–21，The Economist 约 27–28.5M 覆盖全程。两个窗口不同，但「studies put it at」的说法可以接受。卡名写的是「SARS-CoV-2」，洞察卡写的是「COVID-19」，见 D9。
5. 「Measles and HIV are neck and neck, and measles is only counted from 1980.」成立（43M vs 44.2M）。不过 HIV 自己的不确定区间就有 33.8–61.1M，第 3、4 名的先后在误差之内。这张卡已经点到，可以接受。
6. 「Smallpox is the only human disease ever eradicated. Its last natural case was in 1977.」成立（1977 年索马里；1980 年 WHO 宣布根除）。

## 缺陷清单

1. **D1 · blocker · #23 Enterovirus A71 卡（约 42–58 s）· 显示值不是 EV-A71 死亡数，出处链接也对不上**
   - 问题：3,632 是中国大陆 2008–2017 年**手足口病全部死亡**（李佳玲等，《疾病监测》2022）。手足口病由多种肠道病毒引起，sources.md 自己也写了「EV-A71 caused ~90%」。卡上却写「Enterovirus A71 · 3,632」。
     - data.json 的 source.url 指向 Xing et al., Lancet ID 2014，那篇只覆盖 2008–2012 年，cross_check 也引同一篇。也就是说，主值本身没有可追溯的出处，违反 §7.2。
     - 另外，数值记成 documented，没有标 est.。
   - 建议：二选一。
     - (a) 卡名改为「Hand, foot & mouth disease (EV-A71 & others)」，保留 3,632，source 改成李佳玲等 2022 的 DOI 或链接。
     - (b) 保留卡名，数值按 ~90% 改为约 3.3K，并标 est.，notes 写明推算方法。
     - 两种改法名次都不变（仍在 15,514 与 3,000 之间）。改后重跑 gen_sources / publish，再重渲。
2. **D2 · major · 片头（0–5 s）、来源卡（231–235 s）、各卡标记 · 排名方法没有在屏幕上交代，「in History」容易被误读**
   - 问题：各卡窗口差别很大。
     - 丙肝只算 2013–2024，诺如算 1990–2024，麻疹从 1980 算，流感只算 4 次大流行，日本脑炎、汉坦、CCHF、TBE 是单国计数。乙肝、狂犬病用的是 GBD 口径，比 WHO 口径低 2–6 倍（sources.md 已记）。
     - 屏幕上只有每卡的窗口小字和 `est.` 标记，没有任何地方说明「这是各自窗口内有记录的死亡，不是全史总数」，也没有说明 `est.` 是什么意思。
     - 反过来，#1 天花 300M、#2 流感 52.4M 本身就是模型估算（1918 年的估计在 17.4M 到 100M 之间），卡上却**没有** est.。观众会把「无标记 = 更可靠」读反。
     - topic.md 写过「已知局限，洞察卡和描述框都说明」，成片里只有洞察卡 5 点到了麻疹一项。
   - 建议：
     - 片头口径行改为类似「Deaths in each card's window · documented totals or est. (summed yearly estimates)」。
     - 来源卡加一行「est. = yearly global estimates summed over the years shown; windows differ, so older and neglected viruses are undercounted」。
     - #1、#2 卡在数值后加 `est.`，或者把 secondary 改为「≥300M」「~52M」。
     - 可以把洞察卡 1 换成一张专讲口径的卡。改后重渲。
3. **D3 · major · data.json / sources.md / publish.md 评论 2 · 约 12 条出处不可追溯**
   - 问题：bible D1 要求「每个数字有出处」。下面这些条目，观众点开链接找不到对应的数：
     - 只链到期刊或机构首页（10 条）：#6 `virologyj.biomedcentral.com/`、#7 和 #19 `gco.iarc.who.int/`、#10、#16、#17 `frontiersin.org/journals/public-health`、#11 `jtd.amegroups.org/`、#14 `journals.plos.org/plosntds/`、#18 `besjournal.com/`、#25 `epidemvac.ru/`（连作者和标题都没有）。
     - 404：#20 `…/eid/article/16/8/09-1745_article`，应为 `09-0470`。
     - 疑似错链：#30 PMC10413696，754/435 实际出自 PMC11414670。
   - 建议：每条补上具体文章的 DOI 或 PMC 链接，并写全作者、年份、标题；#25 补上俄文综述的作者、题名和 DOI。改完重跑 gen_sources.py 和 publish。只改数据出处不需要重渲（D1 除外）。
4. **D4 · major · #9 Hepatitis C 卡（约 140–156 s）、publish.md 描述与评论 1 · CC BY 2.0 署名不完整**
   - 问题：Flickr 原页的署名行是「NIAID and The Rockefeller University」，显微图作者是 Maria Teresa Catanese 和 Charles M. Rice。卡上、描述和账本却只写「NIH」。CC BY 要求按许可人指定的方式署名。
   - 建议：
     - 账本 author 改为「Maria Teresa Catanese & Charles M. Rice, The Rockefeller University; NIAID」。
     - 描述框改为「NIAID / The Rockefeller University (M. T. Catanese, C. M. Rice), CC BY 2.0, https://creativecommons.org/licenses/by/2.0/」。
     - 卡上署名在重渲时同步改成「Photo: NIAID / Rockefeller Univ. / CC BY 2.0」。
5. **D5 · major · publish.md 描述 · 「Every number on screen is sourced and cross-checked」不实，口径局限缺失**
   - 问题：30 条里有 10 条没有 cross_check：#12 EBV、#13 HAV、#15 YF、#17 VZV、#19 KSHV、#20 Hanta、#25 TBE、#27 SARS、#28 Marburg、#30 Nipah。描述框的 scope 段也只解释了 est.，没有写「窗口不同，所以这是有记录死亡的排名；旧的和被忽视的病毒被低估；乙肝、狂犬病按 WHO 口径会高 2–6 倍」。
   - 建议：
     - 首句改为「Every number on screen has a source and a time window (see pinned comment).」。
     - scope_note 末尾补一句局限说明（≤600 字符内放得下）。
     - 或者把缺的 10 条交叉核对补齐。
6. **D6 · minor · #24 West Nile 卡（约 36–48 s）· 用二手讲座 PDF 的约数，标成 documented**
   - 问题：主值来自一份护理讲座 PDF 的「~3,000」（tier = aggregator），屏上显示「3,000」，没有「~」或 est.，也没有标「据 X 整理」（bible §3.2）。CDC ArboNET 历史数据页已有 1999–2025 年的一手累计数。
   - 建议：从 CDC 历史数据页取 1999–2024（或 1999–2025）累计死亡的确数作主值；取不到就显示「~3,000」，并标 est.。
7. **D7 · minor · #28 Marburg · probable 死亡口径不一致**
   - 问题：赤道几内亚 2023 计入了 probable，埃塞俄比亚 2025 只计 9 例确诊死亡，漏了 WHO 报告的 5 例 probable。notes 写的是「probable deaths counted where WHO reported them」。
   - 建议：改为 561（或者全表统一只计确诊）。洞察卡 2 仍成立，名次不变。
8. **D8 · minor · assets.json / data_contract / publish.md 上传清单 · 渲染图的许可标签和合成内容口径互相矛盾**
   - 问题：
     - 账本把 7 张图记为「AI-generated (Claude-rendered…)」。这些图其实是脚本按 PDB 原子坐标确定性渲染的分子模型，不是生成式 AI 出的图；data_contract 的可接受许可列表里也没有这一类，只有 Codex image_gen。
     - bible §4（follow-up 024）要求「上传时按合成内容声明处理」，publish.md 上传清单却写「本片无 AI 生成的逼真画面 → 选 No」。
     - 卡上的「not a photo」说明在手机尺寸下读不出来。
   - 建议：
     - 账本 licence 改为「Channel render of PDB coordinates (CC0 data)」，在 data_contract 白名单补上这一类。
     - 合成内容一项由用户定一个口径，bible 和 publish 清单同步。本审片的意见：这些图明显是分子模型，不属于 YouTube 要求声明的「逼真合成」，选 No 风险很低；但必须和 bible 一致。
     - 描述框已经写了「'Render' = 3D render… not a photo」，可以保留。
9. **D9 · minor · 多张卡的标签和命名 · 小的事实或口径瑕疵**
   - #9 丙肝标签「Flavivirus」不准确：HCV 属于黄病毒科丙型肝炎病毒属（Hepacivirus），不是黄病毒属。改为「Hepacivirus」或「Flaviviridae」。
   - #17「Vaccine since 1974」是 Oka 株研制的年份，首次获批是 1980 年代中期；其他卡大多用获批年份。改为首次获批年份，或者统一口径。
   - #23 EV-A71 归到「Food & water」不妥：手足口病主要经密切接触、飞沫和粪口传播。归入「Contact」更准确，计分板变为 Food & water 4、Contact 5。
   - #20 图是美洲的 Sin Nombre 病毒（HPS），数据却是中国的 HFRS（汉滩 / 汉城病毒）。可在 CDC PHIL 找汉滩病毒图替换，或者接受属级配图。
   - #8 卡名「SARS-CoV-2」用的是病毒名，旁边洞察卡写「COVID-19」，而 #27 的「SARS」是病名，观众容易把 #8 和 #27 搞混。建议 #8 改为「COVID-19 (SARS-CoV-2)」或「SARS-CoV-2 (COVID-19)」。
10. **D10 · minor · assets.json #6 Rotavirus · 来源记录与实际文件不符**
    - 问题：实际文件（2400×1852）与候选 `h178`（CDC PHIL 178 原始 TIFF）完全一致。账本的 source_page 和 source_url 却是 USGS 页面及其缩略图 URL（`…/thumbnails/image/RotavirusTEM.color_.178.png`）。两者都是公有领域，许可不受影响，但出处记录不准。
    - 建议：source_page 改为 `https://wwwn.cdc.gov/phil/Details.aspx?pid=178`，source_url 改为对应 TIFF，同步描述和评论 1。另外，`_build/reselect/picks.json` 有 11 项与最终账本不一致（如 HIV、HCV、MERS、SARS、WNV、Ebola），是过期文件。建议更新或删除，免得以后有人照着它「回滚」。
11. **D11 · minor · 计分板（224–231 s）· 6 行都用同一个地球图标**
    - 建议：换成区分传播途径的 Tabler 图标（如 wind、bug、droplet、heart、hand、paw；注意 data_contract 图标白名单需要同步扩充），或者干脆去掉图标。
12. **D12 · minor · #13 Hepatitis A 卡（约 112–128 s）· 主图偏弱**
    - 问题：灰度、颗粒感重，病毒簇只占画面中央一小块，手机上基本只看到灰底。
    - 建议：在 CDC PHIL 另找一张 HAV 着色 TEM，或者调高这张图的裁切焦点和放大倍数。
13. **D13 · minor · 渲染图署名措辞与观感 · #14、#17、#18、#19、#21、#25（约 30–122 s）**
    - 问题：
      - 3J27、5WSN、5O6A 三个黄病毒模型画的是包膜 E/M 蛋白外壳，不是衣壳（衣壳蛋白 C 在结构里没有解析出来），卡上写「capsid structure」不准确。
      - 2ZTN 是截短 ORF2 组装成的 T=1 病毒样颗粒，比天然 HEV 病毒粒子（T=3）小。
      - #17 VZV 和 #19 KSHV 两张衣壳渲染图几乎一样；#14、#18、#25 三张黄病毒图也相似，在 30–122 s 里重复感明显。
    - 建议：
      - 黄病毒三张改写「Render: PDB 3J27 virus surface structure…」，#21 写「…virus-like particle…」。
      - 两张疱疹病毒和三张黄病毒各换一个配色或视角，拉开差别。

## 风险提示（不算缺陷，由用户决定）

- **R1 选题卡未获批**：topic.md 头部仍写「口径与名单待用户点头」，bible 也是「待用户确认」。发布前请确认用户已认可「只收病毒、各卡自带窗口、单国计数上榜、不挂国旗」这套口径。
- **R2 单国窗口偏旧**：#20 汉坦（截至 2007）、#23（2017）、#29 CCHF（2017）、#18 日本脑炎（2018）、#25 TBE（2022）的窗口早已结束。bible §3.3 规定「主值超过 18 个月未更新的不用」。这些是历史累计数，可以视为例外，但应在 topic.md 或 sources.md 写明是例外，并由用户确认。日本脑炎只算中国，而全亚洲每年约 2.5 万人死亡；如果按年度估计推算全亚洲，会排进前 15。评论区大概率有人指出这一点。
- **R3 评论区纠错点**：流感（1918 年的估计在 17.4M 到 100M 之间；季节性流感没算）、乙肝和狂犬病（WHO 口径高 2–6 倍）、新冠（超额死亡 15–28M 足以排进前 5）、麻疹（「200M」的流行说法）。sources.md 都已备好替代值，可以直接在评论里引用。
- **R4 时长 4:13**：短于 bible §2.1 的 5–8 分钟目标，也短于 topic.md 预估的约 4:30。不能插中插广告，这是已知的；完播率测试时注意与 Top 50 期分开比较。
- **R5 封面剧透**：thumbnail 直接展示 #1 300M、#2、#3，冠军悬念没了。不过封面上不写病毒名，观众要点进来才知道是什么病毒。是否保留由用户决定。
- **R6 广告友好度**：全片没有血腥或病人画面，以电镜图和结构图为主，新冠部分只陈述 WHO 数据。整体偏教育，风险低。
- **R7 置顶评论链接多**：评论 1 约 30 个链接，评论 2 约 30 个，YouTube 可能自动把评论归为「待审核」。上传后用另一个账号确认能看到。
- 码率 1.68 Mbps（CRF 16）。电镜图颗粒多，抽帧没看到块效应，YouTube 会重新编码，不算缺陷。

## 观众视角

- 可看性：每名约 6.3 s，照片满版，色彩丰富，是目前几期里画面最「好看」的一期。6 张洞察卡节奏均匀，内容（根除、疫苗、报告数和超额死亡的差距）有信息量。
- 不足：中段（30–122 s）渲染图集中出现，又彼此相似，观感有点重复（D13）。榜单后半段充满「CHINA ONLY」「RUSSIA ONLY」这类徽章，懂行的观众会觉得「这些不该和全球数比」。D2 的口径说明是这期能不能经得起评论区的关键。
- 措辞：没有阴谋论或甩锅表述，不挂国旗的决定是对的。最容易挨批的是「in History」配上「丙肝只算 12 年」这种对比，修 D2 和 D5 后可以大幅缓解。

## 未能检查的范围

- 音乐与混音（§7.6）：当前是静音轨，配乐后需要复审。
- 外部抽查覆盖 9 项。其余条目（乙肝、轮状、HPV、丙肝、诺如、RSV、EBV、甲肝、登革、黄热病、狂犬病、VZV、KSHV、戊肝、Ebola 分项、TBE、CCHF、新冠 7,117,689）只核对了 data.json、sources.md 和 cumulative 锚点的内部一致性，没有回原文献核对。新冠 WHO 仪表板和 UNAIDS 情况说明书页面没能直接打开（UNAIDS 返回 403），HIV 用 WHO 情况说明书代替核对。
- PMC 页面被验证码挡住，#30 错链只能根据检索结果判断；CDC 西尼罗病毒的累计死亡确数在交互仪表板里，没能取到。
- 图片：7 个来源页本次直接核对过，其余 23 个依据选图时记录的原始图注和候选库匹配，没有逐页重新打开。Unsplash 许可只按账本记录判断。
- 只抽了每 2 s 的接触表和约 25 张关键帧，没有逐帧查看全部 15,206 帧；滚动平滑度只测了 4 个时间点，freezedetect 覆盖了全片。
- 没有在真机或 YouTube 播放器里实测片尾元素摆放和上传后的画质。

## 外部核对来源

- WHO, HIV and AIDS fact sheet（2026-07-27）：https://www.who.int/news-room/fact-sheets/detail/hiv-aids
- ECDC, MERS-CoV worldwide overview / periodic monitoring 2026-08-03：https://www.ecdc.europa.eu/en/public-health-events/2012-eip-00049/2026-08-03
- Carnegie Council, D.A. Henderson「Smallpox — the Death of a Disease」（2009）：https://es.carnegiecouncil.org/media/podcast/20091028b-smallpox-the-death-of-a-disease-the-inside-story-of-eradicating-a-worldwide-killer
- Zhang et al., Hantavirus Infections in Humans and Animals, China, EID 2010;16(8):1195–1203：https://wwwnc.cdc.gov/eid/article/16/8/09-0470_article
- 李佳玲等，2008–2017 年中国手足口病死亡（《疾病监测》2022），经检索结果核对：https://redi.cedia.edu.ec/document/86381
- Nipah 754 例 / 435 死（截至 2024-05）：https://pmc.ncbi.nlm.nih.gov/articles/PMC11414670
- 埃塞俄比亚马尔堡疫情结束（2026-01）：https://www.healio.com/news/infectious-disease/20260127/ethiopias-first-marburg-outbreak-is-over ；https://www.unmc.edu/healthsecurity/transmission/2026/01/28/ethiopia-declares-end-of-marburg-virus-outbreak-after-42-days-without-new-cases/
- CDC West Nile virus Historic Data（1999–2025）：https://www.cdc.gov/west-nile-virus/data-maps/historic-data.html
- WHO 麻疹情况说明书旧版（1980 年 2.6M/年）转载：https://www.medicusmundi.ch/de/advocacy/publikationen/nachrichten-newsletter/oeffentliche-gesundheit-im-globalen-dorf/fokus-globale-gesundheit-und-die-schweiz/2013-08-05-who-health-topics-measles
- 图片来源页（本次直接核对）：Unsplash HPV（WCN8lfZX4ZI）、Flickr nihgov 53077378506 / 20683459455 / 54270398294、CDC PHIL 3466 / 10234 / 2739。

---

## 第 4 轮：配乐审片（2026-11-04）

独立审片 · 第 4 轮（fresh-context 子代理，只审配乐和新文件完整性；画面以第 3 轮为准）

- 审片对象：`render/ep05_deadliest_viruses_master.mp4`，02:39 由 `_build/music_watch.py` 带配乐重渲。
  - sha256 `6aadf174…1405e`，与 manifest 一致。
  - 15,486 帧 = 258.1 s × 60，H.264 1920×1080。
  - AAC 48 kHz 立体声 256 kbps，时长 258.1 s（12,100 帧），音轨覆盖全片。
- 配乐来源：同一个 Suno 任务 `90bd9426…` 出的两条不同 clip。
  - A：`00fb676e…`，188.84 s，sha `8f068872…`。
  - B：`876f759b…`，219.60 s，sha `95d33ae1…`。
  - 请求写了 `instrumental: true`，并排除 vocals 和 choir（`ai_videos/paihangbang/request_log.md` 第 65,5xx 行一带）。
- 方法：
  - 用 ffmpeg ebur128 测整体响度、真峰值和 LRA。
  - 用 Python 按 BS.1770 K 加权算 3 s 短期、0.4 s 瞬时响度曲线，并统计削波样本。
  - 用 librosa 做节拍、调性（chroma 加 Krumhansl 模板）、频谱重心和低频占比。
  - 在接缝、#5、#3 和片尾各抽帧，和音乐对位。
  - 按渲染器的同一条滤镜链（atrim、4 s tri 交叉淡化、1 s 淡入、3 s 淡出），在本地拼出两个修复候选，比较响度曲线。
  - **审片人听不到声音**，结论全部来自测量。

### 结论：**修后可发布**（带配乐的这一版）

- 文件完整，没有爆音，响度合规，片尾干净。
- 但在前 10 名中段（3:03–3:08，#5 乙肝）有一处换曲接缝：
  - A 曲先走到自然收尾，响度掉一个坑；
  - 紧接着另一首调性不同的 B 曲从中段满音量进来。
  - 听感接近「一首歌结束了，又换了一首」，正好打断高潮段（M1）。
- 用现有素材改拼接参数、重渲一次就能修，不需要重新生成音乐。
- 上传前，第 3 轮列出的用户决定项（U1 N3 的 AI 图、U2 选题卡）仍要完成。

### 完整性核对

| 项 | 结果 |
|---|---|
| 帧数与时长 | 通过。15,486 帧 = 258.1 × 60。视频流、音频流和容器时长都是 258.100 s。 |
| 音轨覆盖 | 通过。0–258.1 s 连续，没有静音段。瞬时响度低于 −35 LUFS 的只有开头 0.2–0.5 s（淡入）和片尾 256.5 s 以后（淡出）。 |
| 输入 hash | 通过。32 个输入（data.json、assets.json、30 张图）重算 sha256，和 manifest 逐一相同。 |
| music 段 | 通过。两个 mp3 的 sha256 和 manifest 相同。out_s 等于文件时长。拼接算式 188.84 + (219.60 − 146.34) − 4 = 258.10 s，正好等于片长，没有触发 aloop 回绕。 |
| 和第 3 轮相比的变动（只记录，未全面复审） | `data.json` 的 hash 从 `a2f7f111…` 变成 `6366593b…`，`assets.json` 从 `f14db25a…` 变成 `0ed8ad0b…`，01:35 改的，晚于第 3 轮报告。抽查到的改动：R1 已修（出处里没有「blocks scripted access」了）；R2 已修（11 条许可恢复为 `AI-generated (Codex image_gen)`，11 条都有 `request_log`）。画面上新增了黄色「AI IMAGE」角标，以及「AI-generated image, not a photo」署名（rank_scroll follow-up 010）。我抽看了 #5 的 1080p 帧和 10–110 s 的接触表：角标和名次药丸、「CHINA / RUSSIA / US ONLY」徽章叠放时没有重叠，都读得清。逐卡复审不在本轮范围。 |
| 渲染器状态 | `projects/rank_scroll/rank_scroll/cards.py` 在 02:41 又改过，晚于这次母版渲染（02:09–02:39）。按 M1 重渲时会带进这些没审过的卡片改动，所以重渲后要抽查画面。 |

### 响度与削波

| 对象 | 整体响度 | 真峰值 | LRA | 样本峰值 | ≥ −0.1 dBFS 样本 | ≥ −1 dBFS 样本 |
|---|---|---|---|---|---|---|
| 母版音轨 | **−16.0 LUFS** | **−5.6 dBTP** | 7.0 LU | −5.66 dBFS | **0** | 0 |
| A 原曲 | −14.7 | −3.7 | 7.3 | −3.68 | 0 | 0 |
| B 原曲 | −14.3 | −3.8 | 8.0 | −3.84 | 0 | 0 |

- 渲染器的目标是 `I=-16:TP=-1.5:LRA=11`，两遍 linear，实测和目标一致。
  - 增益是固定的 −1.9 dB，没有动态压缩，所以 LRA 基本保留（7.0 / 7.3）。
  - 直流偏移可以忽略；L/R 相关 0.58，是正常的立体声。
- 瞬时响度在 100 ms 内跳变超过 3 LU 的点：
  - 0.3 s（淡入）、4.1 s（A 原曲的进入）、201.2 s（B 原曲的段落进入）、257.3 s 以后（淡出）。
  - 没有剪辑造成的突跳或爆音。

3 s 短期响度（每 5 s 的平均值，LUFS）：

- 0–5：−25.4（片头）
- 5–40：−24 → −19.5
- 40–100：−18 ± 1
- 100–130：−16 → −15
- 130–180：−14 ~ −15.5
- **180–190：最低 −22.8**（M1）
- 190–230：−13.4 ~ −14，其中 199.5 s 有一个 −23.5 的低点（见下）
- 230–240：−15
- 240–255：−15 ~ −16.6
- 255–258.1：淡出

### 结构对位（按 manifest 时间线）

时间线：片头 0–5、滚动 5–223.1（前 10 名从 2:25 / 145 s 开始，#10 居中）、冠军 223.1–229.1、计分板 229.1–236.1、来源卡 236.1–240.1、片尾 240.1–258.1 s。

| 段落 | 短期响度均值 | RMS | 低频（<150 Hz）占比 | 判断 |
|---|---|---|---|---|
| #30–#21（5–77 s） | −19.4 LUFS | 36.7 dB | 48.6 % | 铺垫 |
| #20–#11（77–145 s） | −16.5 | 39.0 | 40.6 % | 逐步抬升 |
| 前 10 名 #10–#2（145–219 s） | −15.0 | 41.5 | 54.7 % | 比上一段高 1.5 LU、RMS 高 2.5 dB，低频明显加重（鼓和贝斯进来） |
| #1 加冠军（219–229.1 s） | **−13.6** | 43.1 | 69.4 % | 全片最响 |
| 计分板加来源卡（229.1–240.1 s） | −14.7 | 43–44 | 80–87 % | 持续 |
| 片尾（240.1–258.1 s） | −16.8 | 42.0 | 79.7 % | 收尾 |

- **高潮和前 10 名基本对上，但有两处打折扣**：
  1. 高能平台从约 130 s（#13 附近）就开始了，2:25 进前 10 名时没有明显的再抬升（140–145 s 是 −14.6，145–150 s 是 −14.1）。全片最响的一段在 203–230 s，对着 #3 → No. 1 → 冠军，这一点很好。
  2. 在 3:03–3:08 被 M1 的接缝打断。
- **199.5 s 的低点不算缺陷**：这是 B 原曲自己的段落间歇（B 160–162 s），大约 3 s。它正好落在 #4 和 #3 之间的洞察卡 5 上，201.2 s 响度回升 3.3 LU 进 B 最响的段落，同时 #3 HIV 进场，对位反而合适。
- **片头**：1 s 淡入，A 的前奏约 −25 LUFS，垫在标题下面。4.1 s 有一次进入，正好赶在 5.0 s 滚动开始前，合适。
- **片尾 18 s（240.1–258.1）干净**：
  - 240–251 s 是 B 原曲最后一段，−15 ~ −16 LUFS。
  - 254.5 s 有 B 自带的收尾重音（瞬时 −13.9），随后自然衰减：256.0 s −28.5，256.5 s −36.6，257.0 s −47.0，257.5 s −62.5。
  - 最后 1 s 的 RMS 是 −58 dBFS，最后 50 ms 峰值 −117 dBFS。
  - B 原曲在 219.0 s 自然衰减到 −48 LUFS，再叠加渲染器的 3 s 淡出。
  - 没有在乐句中途硬切。

### 两首原曲单独检查

| 项 | A `00fb676e` | B `876f759b` |
|---|---|---|
| 时长 | 3:08.84 | 3:39.60 |
| 响度 / 真峰值 | −14.7 LUFS / −3.7 dBTP | −14.3 LUFS / −3.8 dBTP |
| 速度 | 117.45 BPM | 117.45 BPM（相同） |
| 调性估计 | 以 D 为中心：全曲 D 小调，相关 0.77；130–170 s 最强的音级是 D G C A | 以 C 为中心：全曲 C 小调，相关 0.82；146–200 s 偏 F 小调，0.66–0.71，最强的音级是 F A♭ G C |
| 结构 | 0–20 s 前奏；120–130 s 间歇；130–170 s 最响（−12 ~ −13）；约 170 s 起频谱重心从约 2,400 Hz 降到约 1,200 Hz，进入尾声；182.5 s 开始自然收尾 | 0–20 s 前奏；115–125 s 间歇；160–162 s 短间歇；165–190 s 最响（−11.5）；215 s 以后自然收尾 |
| 人声 | 请求设了纯音乐，并排除 vocals 和 choir。300–3000 Hz 包络在 3–8 Hz 的音节调制比，A 中位数 0.73、B 0.65，全曲都偏高，也没有哪一段突出（最大 0.87 / 0.85）。这是滴答式打击乐造成的，这个指标分不出人声。**没有发现人声迹象，但不能排除，要靠人耳。** | 同左 |

### §7 第 6 项结果

| 子项 | 结果 | 数据 |
|---|---|---|
| 无爆音 | **通过** | 真峰值 −5.6 dBTP；样本峰值 −5.66 dBFS；≥ −0.1 dBFS 的样本 0 个；没有剪辑造成的突跳。整体 −16.0 LUFS，LRA 7.0 LU。 |
| 高潮对上前 10 名 | **部分通过** | 前 10 名比 #20–#11 高 1.5 LU，低频占比从 40.6 % 升到 54.7 %，最响段落对着 #3 到冠军。但 3:03–3:08 有接缝坑，比前后低 8–9 LU，还换曲换调（M1）。 |
| 片尾 15–20 秒干净 | **通过** | 片尾卡 18 s，B 自然收尾加 3 s 淡出，最后 50 ms 峰值 −117 dBFS，没有硬切。 |
| **合计** | **未通过**，修 M1 后复测 | |

### 缺陷

1. **M1 · major · 3:03–3:08（#5 乙肝居中）换曲接缝：能量坑加调性跳变，打断前 10 名的高潮段**
   - 现象：
     - A 原曲 182.5 s 开始自然收尾，短期响度 −14.1 → −17.7 → −21.0 → −23.7 → −28.2（182.5–186.5 s）。
     - 渲染器在 184.84–188.84 s 做 4 s 交叉淡化，接进 B 的 146.34 s。B 在这个位置是满音量的中段，−12.4 LUFS。
     - 母版的短期响度：182.5 s −16.0，183.5 s −19.6，184.5 s −22.8，185.5 s −22.8，186.5 s −20.2，187.5 s −16.9，188.5 s −15.1。比前后的 −14 低 8–9 LU，持续约 3 s。
     - 调性中心从 D 换到 C / F。
     - 再往前，A 从约 170 s 起已进入尾声（频谱重心减半），所以 #7 → #5 这十几秒都在跟着「收尾」。
     - 速度相同，A 的节拍在接缝前已经停了，所以不会有鼓点错位。但整体听起来就是「歌放完了，又换了一首」。
   - 根因：
     - Suno 两条 clip 都不够 4:18，`--music-fit end` 只裁掉 B 的开头，A 原样播到它自己的结尾，接缝就落在 A 的尾声里。
     - 渲染器 docstring 说「follow-up 修过接缝能量坑」，但这一种情况没有覆盖到。
   - 修法：任选一个，重渲后复测本节全部数字。
     - **方案 1（零成本，建议先试）：只用 A 曲两段拼接，不换曲也不换调**
       ```
       --music assets/music/00fb676e-b8e8-4ad5-8276-3bd7fedbb493.mp3@1.35:170.25 assets/music/00fb676e-b8e8-4ad5-8276-3bd7fedbb493.mp3@95.64 --music-fit end
       ```
       - 两段的入点和出点按跟踪到的节拍网格对齐：交叉淡化起点 166.25 s 到第二段入点 95.64 s 相隔 140 拍，也就是整 35 小节（4/4）。拼出来正好 258.10 s。
       - 第一段从 1.35 s 开始，所以 A 前奏的进入点从 4.1 s 提前到约 2.75 s，仍然在 5.0 s 滚动开始之前。
       - 接缝落在母版 164.9–168.9 s（#7 附近），第一段这 4 s 取的是 A 的 166.25–170.25 s，仍在高能段，没有坑。
       - A 的尾声（170–188.84 s）正好对上母版 239.3–258.1 s，也就是片尾卡，片尾由 A 自然收尾。
       - 本地按同一滤镜链拼出来测过：10–250 s 内没有剪辑造成的坑。最低点是 193.5 s 的 −22.0，那是 A 自己 120–125 s 的间歇，落在 #4 / #5 附近。前 10 名均值 −15.2。
       - 代价：A 的 95.6–170 s（约 75 s）会听到两次；接缝后 165–185 s 比接缝前（−14）低约 1.5–3.4 LU（每 5 s 均值 −17.4 / −16.3 / −15.7 / −15.5）。
     - **方案 2（零成本）：只用 B 曲**
       ```
       --music assets/music/876f759b-e3f0-4140-8087-d287b4e479ba.mp3@2.18:112.57 assets/music/876f759b-e3f0-4140-8087-d287b4e479ba.mp3@67.89 --music-fit end
       ```
       - 交叉淡化起点到第二段入点相隔 80 拍，也就是整 20 小节。结尾和现在一样，重复约 45 s。
       - 本地测过：接缝后 106–135 s 掉约 3 LU；B 自己 115–125 s 的间歇落在 153–165 s（#9–#8）；前 10 名只比上一段高约 1 LU。效果不如方案 1。
     - **方案 3（最好，要人点）**：用 Suno 对 A 做 extend，或者重新生成一首 ≥ 4:30 的单曲，这也符合 bible §5「每期一首」。先写 `request_log.md`，由用户亲手点生成。拿到后用 `--music 新曲.mp3 --music-fit end`。
   - 注意：
     - 方案 1 和 2 的节拍点来自 librosa 节拍跟踪（117.45 BPM），只保证整小节，不保证 8 小节乐句和强拍。乐句是否对齐、接缝听感如何，要有人戴耳机确认；必要时以 ±1 小节（2.04 s）微调入点，并同步调整第一段的起点，使总长仍等于 258.1 s。
     - 重渲会带进 02:41 以后的 `cards.py` 改动，重渲后要抽查画面，并重核 sha256、章节和发布稿。
     - 建议给渲染器加一个检查：当非最后一段的末 6 s 短期响度比该段中位数低 6 LU 以上时报警（说明接缝落在了尾声里）。记一条 rank_scroll follow-up。
2. **M2 · minor · 偏离 bible §5「每期一首 4–8 分钟纯音乐」**
   - 现在是同一任务的两条不同 clip（3:08 + 3:39）拼起来，两条都短于片长，这正是 M1 的根源。
   - 修法：走 M1 方案 3。如果系列以后允许「同任务 clip 拼接」，要由用户在 bible §9 记一条决定，并写明「同调同速、接缝避开尾声」等条件。
3. **M3 · 轻微（可选）· 整体 −16 LUFS**
   - YouTube 以约 −14 LUFS 为参考，只压低偏响的视频，不抬高偏轻的，所以本片会比同类视频轻约 2 dB。
   - 现在的真峰值余量足够，改到 −14 后真峰值约 −3.6 dBTP。
   - 修法：二选一。纯音乐的榜单片把渲染器目标改成 `I=-14:TP=-1.5`；或者把 −16 写进 bible §5，作为系列标准。不影响发布。
4. **M4 · 轻微 · publish.md 没有任何配乐来源信息**
   - bible §5 写明「AI 曲有被 Content ID 误认领的风险，申诉要靠请求日志」「不把自家曲目登记进 Content ID」，但上传清单里没有这一项。
   - 修法：在 `publish.py` 模板里加，不要手改 publish.md（重跑会覆盖）。
     - 上传清单加一条：「配乐：Suno 任务 `90bd9426…`，clip `00fb676e` / `876f759b`。不登记 Content ID。如果被认领，用 `ai_videos/paihangbang/request_log.md` 的对应条目申诉。」
     - 描述框可以选加一行「Music: original score generated with Suno」（约 45 字符）。
   - 描述框现在 3,593 / 5,000 字符，加上以后约 3,640，没有问题。合成内容声明已选 Yes，覆盖 AI 图；bible 没有要求对 AI 音乐另作声明。
5. **M5 · 轻微 · manifest 的配乐记录不够审计用**
   - `music_bed` 只存了 loudnorm 第一遍的分析 JSON（`normalization_type: dynamic`、`output_i: -14.10`），容易被误读成「动态压到 −14」。
   - 没有记目标串、linear 模式和第二遍或成品的实测值，中间文件 `.music.wav` 也已删除，没法复核拼好的音床。
   - 修法：manifest 加上 `target: "I=-16:TP=-1.5:LRA=11"`、`linear: true`，以及成品音轨的 ebur128 实测（I / TP / LRA）。

### 未能检查的范围

- **没有试听**。以下几项只能间接推断，需要人戴耳机过一遍：
  - 音色是否刺耳，有没有 Suno 常见的金属感或失真伪影；
  - 199.5 s 的间歇听起来是否有意为之；
  - 是否有隐约的人声或合唱；
  - 方案 1 和 2 的接缝听感。
- 调性和节拍是算法估计（Krumhansl 模板相关 0.62–0.82，节拍跟踪的抖动约 ±0.1 s），不是乐谱级的结论。
- 没有核实 Suno 账号（ID3 artist `dalu198649`）出曲时是不是 Pro / Premier 档，这决定能否商用。
- Content ID 只有上传后才能看到。
- 第 3 轮以后的画面改动（AI IMAGE 角标、新署名文字、data / assets 的文字修正）只做了抽查，没有逐卡复审。
- 没有在真机或 YouTube 播放器里实测。

## 第 5 轮：配乐修复复核（2026-11-04）

独立审片 · 第 5 轮（fresh-context 子代理，只复核 M1 修复后的重渲母版、新 AI 角标抽查和发布稿的配乐署名；其余画面以第 3 轮为准）

- 审片对象：`render/ep05_deadliest_viruses_master.mp4`，03:35 重渲（manifest `render_seconds` 1893.8，约 03:04 开始）。
  - sha256 `1662eeb7…c87c5f1`，与 manifest 一致。
  - 渲染开始晚于 `cards.py`（02:41）和 `data.json`（03:02），所以第 4 轮提醒的卡片改动和配乐署名都已包含在内。
- 方法：
  - 用 ffprobe 核对帧数和音视频时长，用 ffmpeg ebur128 测整体响度、真峰值和 LRA。
  - 用 Python 按 BS.1770 K 加权算短期响度（3 s 窗，0.5 s / 0.1 s 步进）和瞬时响度（0.4 s），并统计削波样本。
  - 把母版音轨和 A 原曲做互相关，确认实际拼接位置；用 librosa 的 onset 包络检查交叉淡化两半是否对拍。
  - 用 `rank_scroll.timeline` 算出 30 张卡的居中时刻，在每个居中帧检测黄色角标像素，再对其中 9 帧（24.0、41.33、54.0、71.33、87.2、96.67、123.5、133.0、184.57 s）看 1080p 原图。
  - **审片人听不到声音**，结论全部来自测量。

### 结论：**可发布**（带配乐的这一版；只是测量层面的结论）

- M1 已修好：
  - 3:03 的换曲坑没有了，全片只用 A 一首曲，没有换调。
  - 新接缝在 164.9–168.9 s（第 8 名后的洞察卡到 #7）。这里最低 −18.8 LUFS，比前后的 −14.3 低 4.5 LU，低于 −6 LU 的报警线。
  - 没有爆音，片尾干净。
- 上传前还要做三件事（都不需要重渲）：
  1. 人戴耳机完整听一遍（见「需要人耳确认」）。
  2. 顺手修发布稿的两处轻微问题（M4′、M7）。
  3. 完成第 3 轮列出的用户决定项（U1、U2）。

### 完整性核对

| 项 | 结果 |
|---|---|
| 帧数与时长 | 通过。15,486 帧 = 258.1 × 60。H.264 1920×1080 60 fps。视频流、音频流和容器时长都是 258.100 s。 |
| 音轨覆盖 | 通过。AAC 48 kHz 立体声，12,100 帧，258.100 s。0–258.1 s 连续：开头是 1 s 淡入，A 前奏在 2.9 s 进入（第 4 轮预计约 2.75 s），早于 5.0 s 滚动开始；结尾最后 1 s RMS −68.8 dBFS，最后 50 ms 是数字静音。 |
| 输入 hash | 通过。32 个输入（data.json、assets.json、30 张图）重算 sha256，和 manifest 逐一相同。`data.json` 现在是 `34493d97…`，第 4 轮时是 `6366593b…`，03:02 改过；顶部新增了 `music_credit` 字段（第 5 行）。文件没有进 git，无法逐字段 diff，其他字段是否也改过没有核实。`assets.json` 仍是 `0ed8ad0b…`，没变。 |
| music 段 | 通过。manifest 有两段，都是 `00fb676e…mp3`（sha `8f068872…`，和当前文件相同）。第一段 in 1.35 / out 170.25，第二段 in 95.64 / out 188.84（等于文件时长），`fit: end`，交叉淡化 4.0 s。和第 4 轮建议的参数完全一致。168.9 + 93.2 − 4 = 258.1 s，正好等于片长，所以 fit=end 没有再裁，也没有 aloop 回绕。B 曲 `876f759b` 没有用到。 |
| 实际拼接位置 | 通过。按 2 s 窗互相关：母版 20、80、150、160 s 分别对上 A 的 +1.35 s（r 0.98–1.00）；母版 172、200、230、250 s 分别对上 A 的 −69.26 s（r 0.999–1.000）。接缝就在 manifest 算出的 164.9–168.9 s。交叉淡化两半（A 166.25 s 和 A 95.64 s 起各 12 s）的 onset 包络在 0 ms 处相关最高（r 0.77），两个切点离各自最近的节拍都是 −42 / −43 ms，**对拍**。 |
| manifest 审计字段 | 没有改进。`music_bed` 仍然只存 loudnorm 第一遍的 JSON，没有 target 和 linear（M5 未修）。 |

### 响度与削波

| 对象 | 整体响度 | 真峰值 | LRA | 样本峰值 | ≥ −0.1 dBFS | ≥ −1 dBFS | ≥ −3 dBFS |
|---|---|---|---|---|---|---|---|
| 本轮母版 | **−16.0 LUFS** | **−5.4 dBTP** | 6.4 LU | −5.38 dBFS | **0** | 0 | 0 |
| 第 4 轮母版（对照） | −16.0 | −5.6 | 7.0 | −5.66 | 0 | 0 | — |

- 直流偏移可以忽略（3.6e-4 / −9e-5），L/R 相关 0.52，是正常的立体声。
- 瞬时响度在 100 ms 内变化超过 3 LU 的点只有 4 个：
  - 0.5 s 和 0.6 s：淡入。
  - 2.9 s：A 前奏进入，+4.0。
  - 84.0 s：A 曲内部的一次 −3.1，对着 #19 居中，不是剪辑造成的。
  - **接缝处没有**。
- 短期响度每秒变化超过 3 LU 的点：121.5 s（−3.4）、192.5 s（−3.4），这两处都是 A 曲自己的间歇（见下）；另有 253.5–256.5 s 的片尾自然衰减。

3 s 短期响度（每 5 s 的平均值，LUFS）：

- 0–10：−23.5 ~ −23.8（片头）
- 10–40：−21 → −19
- 40–100：−17 ~ −18.7
- 100–120：−16.2 → −14.5
- 120–125：**−19.6**（最低 −22.5，A 自己的间歇）
- 125–165：−15.9 → −14.7 → −13.7 ~ −14.2
- 165–170：**−17.3**（接缝，最低 −18.8）
- 170–185：−16.4 / −15.7 / −15.6
- 185–190：−14.5
- 190–195：**−19.1**（最低 −22.5，A 间歇的第二次出现）
- 195–200：−16.4
- 200–250：−13.8 ~ −15.4
- 250–255：−18.3（A 自然收尾）
- 255–258.1：淡出

**按 0.1 s 步进统计响度坑**（参考值 = 前后 5–20 s 的中位数）：

| 位置 | 低于参考 4 LU | 低于参考 6 LU | 最低 | 性质 |
|---|---|---|---|---|
| 121.2–124.7 s（#14 → #13） | 3.6 s | 2.0 s（121.7–123.6） | −22.5 @ 122.6 s | A 原曲 120–125 s 的间歇，不在前 10 名 |
| 167.0–168.7 s（接缝，洞察卡 8 → #7） | 1.8 s | **0 s** | −18.8 @ 167.9 s | 接缝，同曲对拍交叉淡化 |
| 191.8–195.4 s（#4 居中 → 洞察卡 4） | 3.7 s | **2.1 s**（192.3–194.3） | −22.5 @ 193.1 s | 同一个 A 间歇第二次出现，第二段 A 95.64 s 起 |

- 「坑 > 6 LU 且 > 2 s」的报警线只碰到一处：192.3–194.3 s，2.1 s，只超出 0.1 s，属于临界。
- 这一处是乐曲自己写好的「停一拍再起」：之后 4 s 回到 −14.6，正好在 #3 HIV（202.8 s）进场之前抬回来。第 4 轮对 B 曲 199.5 s 那个同类间歇的判定是「不算缺陷」。本轮按同一标准，列为轻微的人耳确认项（M6），不算 blocker。
- 没有突跳。

### 结构对位（按 manifest 时间线和 `rank_scroll.timeline` 算出的居中时刻）

| 段落 | 短期响度均值 / 中位数 | 最低 | RMS | 低频（<150 Hz）占比 |
|---|---|---|---|---|
| #30–#21（5–77 s） | −19.1 / −19.0 | −24.9 | −21.9 dBFS | 49.0 % |
| #20–#11（77–145 s） | −16.3 / −15.9 | −22.5 | −19.7 | 40.0 % |
| 前 10 名 #10–#8（145–164.9 s，接缝前） | −14.0 / −14.0 | −14.5 | −17.9 | 32.3 % |
| 接缝（164.9–168.9 s） | −17.2 / −17.7 | −18.8 | −20.8 | 47.4 % |
| #7–#5（168.9–188 s，接缝后） | −15.8 / −15.8 | −17.9 | −19.8 | 33.1 % |
| #4–#2（188–219 s） | −15.5 / −14.6 | −22.5 | −18.8 | 42.8 % |
| **前 10 名合计 #10–#2（145–219 s）** | **−15.3 / −14.6** | −22.5 | −18.8 | 37.4 % |
| #1 加冠军（219–229.1 s） | −14.0 / −14.0 | −14.4 | −17.9 | 27.9 % |
| 计分板加来源卡（229.1–240.1 s） | −14.2 / −14.3 | −14.8 | −17.8 | 40.8 % |
| 片尾（240.1–258.1 s） | −17.8 / −15.4 | −34.8 | −18.7 | 52.1 % |

- **整体仍是逐段抬升**：#30–#21 −19.1 → #20–#11 −16.3 → 前 10 名 −15.3（中位数 −14.6）→ #1 和冠军 −14.0。前 10 名比上一段高 1.0 LU（中位数高 1.3 LU）。
- **前 10 名内部有一段下沉**：接缝后的 #7–#5 是 −15.8，比接缝前的 #10–#8 低 1.8 LU；接着 #4 碰上间歇，到 #3 之后才回到 −14.5。
  - 这是第 4 轮方案 1 已经写明的代价：第二段从 A 95.64 s 开始，A 的这一段本来就比它 130–170 s 的高潮段轻。
  - 和第 4 轮相比，坑从 8–9 LU、换曲换调，降到 4.5 LU、同曲对拍，打断感应该小很多。
- 高能平台从 115–130 s（#15–#13）就开始了，2:25 进前 10 名时仍没有明显的再抬升。这个问题第 4 轮也指出过，本轮没有变好，也没有变坏。
- A 的 130–170 s 高潮段第二次出现在母版 199.3–239.3 s，对着 #3 → #2 → No. 1 → 冠军 → 计分板，最响段落对着榜首，这一点保住了。
- **片尾干净**：
  - A 在 182.5 s 开始的自然收尾落在母版 251.8 s，也就是片尾卡（240.1–258.1）的最后 6 s。
  - 短期响度 251.0 s −14.5 → 253.0 s −20.3 → 255.0 s −26.4 → 256.5 s −34.8，再叠渲染器 255.1 s 起的 3 s 淡出。
  - 最后 50 ms 是数字静音，没有在乐句中途硬切。
- **重复**：A 的 95.6–170.3 s（74.6 s）在母版里出现两次（94.3–168.9 s 和 164.9–239.5 s）。测量看不出问题，听感要靠人耳。

### §7 第 6 项结果

| 子项 | 结果 | 数据 |
|---|---|---|
| 无爆音 | **通过** | 真峰值 −5.4 dBTP；样本峰值 −5.38 dBFS；≥ −1 dBFS 的样本 0 个；没有剪辑造成的突跳（接缝处瞬时响度没有超过 3 LU / 100 ms 的跳变）。整体 −16.0 LUFS，LRA 6.4 LU。 |
| 高潮对上前 10 名 | **通过**（有保留） | 前 10 名均值 −15.3 / 中位数 −14.6，比 #20–#11 高 1.0 / 1.3 LU；最响段落（−14.0）对着 #1 和冠军。M1 的坑和换调已消除，接缝最低只低 4.5 LU，没有 > 6 LU 且持续 1 s 以上的时段。保留：#7–#5 下沉 1.8 LU；#4 处的乐曲间歇 2.1 s，临界（M6）。 |
| 片尾 15–20 秒干净 | **通过** | 片尾卡 18 s；A 自然收尾（母版 251.8 s 起）加 3 s 淡出；最后 1 s RMS −68.8 dBFS，最后 50 ms 数字静音。 |
| **合计** | **通过** | M6 交给人耳确认 |

### AI 角标抽查

- 30 张卡逐张检测：在各自居中帧的卡片顶部区域（y 140–330，x 560–1360）找黄色 `#f5c518` 像素。
  - 11 张 AI 卡（#5、#12、#13、#14、#17、#18、#19、#21、#23、#25、#27）都有角标，每张 3,069–3,084 个像素。#5 是放大卡，3,463 个。像素数一致，说明角标没有被遮住。
  - 19 张实拍卡都没有角标，都是 0 像素；只有 #3 有 2 个像素，是图里的噪点。
- 1080p 原图看了 9 帧，11 张 AI 卡全部覆盖，同时看到实拍卡 #28、#26、#24、#22、#20、#16、#15、#11、#6、#4：
  - 没有徽章的卡：「AI IMAGE」在左上角（#27、#21、#17、#14、#13、#5），和右上角的名次药丸隔开 400 px 以上。
  - 有 CHINA ONLY / RUSSIA ONLY / CANCER DEATHS 徽章的卡：「AI IMAGE」往下移 50 px，排在徽章下面（#25、#23、#19、#18、#12），没有重叠，和图片主体、名称、数字也都不重叠。
  - 底部署名「AI-generated image, not a photo」右对齐，和实拍卡的「Photo: …」在同一位置。字小但清楚，和信息行不冲突。
  - 实拍卡上没有角标，署名仍是「Photo: …」。
- 冠军、计分板、来源卡和片尾卡没有重看。

### 发布稿（publish.md，03:35 生成）

| 项 | 结果 |
|---|---|
| 描述框长度 | 通过。3,703 / 5,000 字符（UTF-8 3,714 字节），没有 YouTube 禁用的 `<` `>`。 |
| 配乐署名 | **有，但不准确**。描述框第 60 行：「Music: original instrumental generated for this channel with Suno (job 90bd9426, clips 00fb676e / 876f759b).」本片已经只用 `00fb676e`，`876f759b` 不在片中（M4′）。 |
| Content ID 上传清单项 | **没有加**。第 4 轮 M4 建议的「不登记 Content ID；被认领时用 request_log 申诉」不在 Upload checklist 里（M4′）。 |
| 合成内容声明 | 通过。清单写明「Altered or synthetic content → 选 Yes」。但括号里还写着「卡上标 Illustration / Render」，画面现在标的是「AI IMAGE」，说法过时了（M7）。 |
| 描述里的图片署名 | 和画面一致：11 张标 `AI-generated (Codex image_gen)`，另有一句「11 images marked AI-generated are illustrations, not photos」。 |

### 第 4 轮缺陷状态

| 编号 | 状态 |
|---|---|
| M1 · major 换曲接缝 | **已修复**。数据见上。 |
| M2 · minor 偏离 bible §5「每期一首 4–8 分钟」 | **部分缓解**。现在只用一首曲，但这首只有 3:08，靠重复 74.6 s 才够 4:18，仍不满足「4–8 分钟」。修法不变：走第 4 轮方案 3（extend 或重新生成 ≥ 4:30 的单曲，要人点），或者由用户在 bible §9 记一条决定，允许「单曲内部对拍重复」。 |
| M3 · 轻微（可选）整体 −16 LUFS | 没有变化，仍是 −16.0。修法同第 4 轮，不影响发布。 |
| M4 · 轻微 发布稿缺配乐来源 | **部分修复**，剩下的问题记为 M4′（见下）。 |
| M5 · 轻微 manifest 配乐审计字段 | **没有修**。修法同第 4 轮。 |

### 剩余缺陷

1. **M4′ · 轻微 · 配乐署名写了一条没用到的 clip，上传清单缺 Content ID 项**
   - 现象：描述框写的是「clips 00fb676e / 876f759b」，母版实际只用了 `00fb676e`（见上面的互相关）。Upload checklist 没有 Content ID 相关条目。
   - 修法：
     - 改 `data.json` 的 `music_credit`，改成「…with Suno (job 90bd9426, clip 00fb676e).」，然后重跑 `publish`。不要手改 publish.md，重跑会覆盖。
     - 在 `publish.py` 的上传清单模板里加一条：「配乐：Suno 任务 `90bd9426…`，clip `00fb676e`；不登记 Content ID；被认领时用 `ai_videos/paihangbang/request_log.md` 的对应条目申诉」。
   - 注意：`data.json` 是 manifest 记录的渲染输入。只改 `music_credit` 不影响画面（只有 `publish.py` 第 160 行读它），但改完 hash 就和 manifest 对不上了。二选一：
     - 下次重渲时一起带上；
     - 不重渲，在 qc 或 follow-up 里记明「渲染后只改了不上画面的 `music_credit`」，并记录新 hash。
2. **M6 · 轻微（人耳确认）· #4 居中时乐曲间歇，加上 #7–#5 下沉**
   - 现象：
     - 192.3–194.3 s，短期响度比前后低 6 LU 以上，持续 2.1 s，最低 −22.5，正好在 #4 Measles 居中（191.4 s）之后。
     - 168.9–188 s（#7–#5）比 #10–#8 低 1.8 LU。
     - 两处都是 A 曲本身的编排，不是剪辑造成的。
   - 判断：如果人耳听来是有意的「停一拍、再推到 #3」，就接受，不用改。
   - 如果要改（零成本，先本地试拼）：第一段出点和第二段入点同时提前 2 小节（4.08 s），即 `…00fb676e…mp3@1.35:166.17 …00fb676e…mp3@91.56 --music-fit end`。
     - 总长仍是 258.1 s。片头和片尾都不变。
     - 接缝移到 160.9–164.9 s（第 8 名一带），这一段取自 A 162.2–166.2 s，仍在高能段。
     - 间歇移到约 196.4–198.4 s，落在洞察卡 4（197.1 s）上，不再压在 #4 名次揭晓上。
     - 这个修法没有实测，要按第 4 轮的同一套方法复测，并由人耳确认接缝。
3. **M7 · 轻微 · 上传清单里的合成内容说明过时**
   - 现象：写的是「卡上标 Illustration / Render」，画面上实际标的是「AI IMAGE」。
   - 修法：改 `publish.py` 第 176 行的模板文字，再重跑 `publish`。
4. M2、M3、M5 见上表，都没有变化，都不阻塞发布。

### 需要人耳确认

- 接缝（2:45–2:49，洞察卡 8 → #7）：同曲对拍交叉淡化，测出来对拍；还要确认 8 小节乐句是否顺，以及有没有重拍叠两次的「flam」感。
- 重复段：A 的 95.6–170.3 s 在 1:34–2:49 和 2:45–3:59 各出现一次。要确认听众会不会明显觉得「同一段又来一遍」。
- #4 处的间歇（3:12–3:14，M6）：要确认听感是「蓄力」还是「掉了」。
- 第 4 轮留下的人耳项仍然有效：Suno 常见的金属感或失真伪影、隐约的人声或合唱、2:01–2:04（#14 → #13）那次 A 间歇的听感。

### 未能检查的范围

- **没有试听**，见上一节。
- `data.json` 从 `6366593b…` 到 `34493d97…` 的改动：只确认新增了 `music_credit`，没有逐字段 diff（文件没进 git）。
- `render/thumbnail.png`（03:35 重新生成）、冠军、计分板、来源卡和片尾卡在新渲染器下的画面，本轮没有看。
- Suno 账号档位能否商用、Content ID，同第 4 轮，未核实。
- 没有在真机或 YouTube 播放器里实测。

## 作者处理记录（第 5 轮之后，2026-11-04，非审片结论）

- M4′：`data.json` 的 `music_credit` 改为只列实际使用的 clip 00fb676e；M7：上传清单合成内容一行改为「卡上标 AI IMAGE」；清单加 Content ID 一行（`rank_scroll/publish.py` 模板）。publish.md 已重新生成。
- 这次 `data.json` 只改了 `music_credit`（只进描述框，不上屏），所以母版没有重渲；manifest 里 data.json 的哈希因此与当前文件不一致，属预期。下次重渲会自动对齐。
- M6（#4 处曲子自带约 2 秒停顿）、M2（单曲 3:08 重复约 75 秒）、M3（−16 LUFS）、M5（manifest 未记录 loudnorm 目标）留给用户戴耳机听后决定，未改。

## 作者处理记录（2026-11-04 08:43–08:56，非审片结论）

- 用户说「suno is good now」后，试着生成一首 ≥4:30 的整曲，用来去掉拼接点、75 秒重复段和 #4 处的停顿（M2 / M6）。
- 第一次（job 0c5b3ebb）带 `duration_seconds=285`。服务报 `unverified_units`：页面上时长控件的单位不明确，在 Create 之前就停了，没有提交，也没扣点。
- 第二次（job 2740c983）去掉时长选项，只在 prompt 里写「五分钟、不停顿」，出了 2 首：
  - 0d5852e5：3:33，−15.5 LUFS，峰值 −3.7 dBFS；
  - 173175d4：3:22，−13.9 LUFS，峰值 −3.7 dBFS。
  - 两首中间都没有超过 0.7 s 的静音（−35 dB 阈值），只有结尾约 1.3 s 的淡出。
- 两首都不够 4:18，用了仍然要拼接或重复，所以母版不改，继续用 00fb676e 的拼接版。两首新曲留在 `assets/music/`，作候选。
- 要真正去掉拼接，得等服务校准时长控件，或者在 Suno 里用 Extend 把曲子接长。
