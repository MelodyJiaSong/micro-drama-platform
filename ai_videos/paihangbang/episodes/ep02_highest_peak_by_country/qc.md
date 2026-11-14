独立审片（fresh-context 子代理，2026-11-03）

# ep02 · Highest Mountain in Every Country · 审片记录

- 审片对象：`render/ep02_highest_peak_by_country_master.mp4`（sha256 `710d6d22…c425d`，与 manifest 一致）；1920×1080，60 fps，331.0 s，19,860 帧，H.264 + AAC。
- 输入核对：`data.json` / `assets.json` 的 sha256 与 manifest 记录一致，说明成片就是用当前数据渲染的。
- 方法：
  - 抽帧：每 2 s 一张，拼成 6 张接触表，覆盖 0–331 s 全片；另取 1280 宽关键帧 22 张，包括片头、5 张洞察卡、Khazret Sultan 占位卡、前 10 名、冠军段、计分板、来源卡和片尾；再取 640×360 手机尺寸帧 3 张，并查看封面。
  - 运动：在 20、140、200、250、275 s 各取 11 帧连续帧，用行带互相关测位移；全片另跑 freezedetect。
  - 数据：重新计算显示值、英尺换算、排序和大洲计数；查 Wikipedia API、PeakVisor、Euronews 等外部来源。
- 音频：全片静音（mean/max −91 dB）。音乐还没做，按设计如此，不算缺陷；§7 第 6 项未检。

## 结论：**修后可发布**

当前文件**不能直接上传**。阻塞问题只有 1 条（D1：勃朗峰数值已过时），另有 1 条重大问题（D2：冠军段尼泊尔卡被裁）。两条都只需改数据或渲染参数后重渲，格式、版权和其余数据都没有发现结构性问题。

## §7 审片清单

| # | 项目 | 结果 | 证据 |
|---|---|---|---|
| 1 | 名次连续、无重复，排序与 `data.json` 一致 | 通过 | 接触表逐卡核对，画面出场顺序为 50→41、洞察、40→32、洞察、30(IT)、30(FR)、29、28、26(UG)、26(CD)、25→21、洞察、20→11、洞察、10→4、洞察、3、1(NP)、1(CN)，共 50 张卡，和 data.json 倒序一致。并列名次按标准竞赛排名（1,1,3 / 26,26,28 / 30,30,32）跳号，sources.md §1 已写明。脚本复核 value 单调不增。 |
| 2 | 数值能追溯到 `sources.md`，统计期与片头一致 | **不通过** | 50 条都能在 sources.md §4 找到出处；value_display 与 secondary_display 由脚本重算，全部一致（米四舍五入到整数，英尺 = 米 × 3.28084）。问题是勃朗峰：2026-09-17 上萨瓦省测量师公会做了新一轮官方测量，2026-10-14 公布为 **4,807.47 m**（Euronews）。片头写「Data as of Nov 2026」，卡上却仍是 2023 年的 4,806 m，洞察卡 3 的「836 m」也因此不对，应为 835 m。见 D1。 |
| 3 | 国旗与国家对应 | 通过 | 50 张卡的国旗和国名逐一看过，都对得上（flagcdn）。共享山峰的徽章正确：SHARED WITH CHINA / NEPAL / UGANDA / DR CONGO / FRANCE / ITALY。阿富汗用的是前共和国三色旗，见风险 R2。 |
| 4 | 每张图都在 `assets.json`，许可可接受 | 通过 | data.json 引用 49 张图，全部在账本里，sha256 与文件逐一相符，账本里没有多余条目。许可分布：CC BY-SA 2.0–4.0（含 fr/nl/au/de 移植版）37 张、CC BY 6 张、CC0 2 张、PD 3 张，没有 NC、ND 或 GFDL-only。乌兹别克斯坦 Khazret Sultan 无图，用「国旗 + 山形图标 + No free-licensed photo available」占位，没有使用账本外的图。卡上署名和账本作者一致。 |
| 5 | 文字不出框、不闪烁；手机全屏 3 秒内看清名称和数值 | 部分通过 | 滚动匀速，实测每帧整 2 px，相关系数 1.000，不会出现亚像素闪烁；freezedetect 显示 5–292 s 没有冻帧或掉帧。640×360 下山名、国名和主数值都清楚，英尺值和 tag 偏小但能读。剩下的问题：冠军段尼泊尔卡被左边缘裁掉（D2）；洞察卡 1 的「4,095 / m」「4,040 / m.」数字和单位被断到两行（D4）；片头过渡时标题叠在卡片上方（D5）。 |
| 6 | 音乐无爆音、高潮对上前 10 名、片尾干净 | 未检 | 音乐待制作，当前是静音 AAC 轨。 |
| 7 | 描述框来源与署名完整 | 通过（附小问题） | 描述 3,532 字符，在 5,000 以内，没有 `<` `>`；含 50 条图片署名（作者 + 许可）、数据来源行和 flags/icons/font 署名。置顶评论 1 有带许可链接和原图链接的完整署名，8,949 字符（≤10,000）；评论 2 是逐条数据出处，5,250 字符。章节共 7 个，从 0:00 开始，间隔 58/53/64/59/58/10 s，都 ≥10 s，逐个看帧对得上（见下表）。小问题：hashtag 被截断（D6）。 |

### 章节时间点核对（按帧查看）

| 章节 | 时间 | 画面 | 结果 |
|---|---|---|---|
| Intro & #50–#41 | 0:00 | 片头标题 | 对 |
| #40–#31 | 0:58 | Cameroon 洞察卡 + #40 Toubkal + #39 Tajumulco | 对 |
| #30–#21 | 1:51 | Mont Blanc 洞察卡 + #30 Italy 正在进场 | 对 |
| #20–#11 | 2:55 | Elbrus 洞察卡 + #20 Russia | 对 |
| Top 10 | 3:54 | 「From here on…」洞察卡 + #10 Aconcagua（已放大） | 对 |
| No. 1 | 4:52 | #1 Nepal + #1 China | 对 |
| Peaks by continent | 5:02 | 计分板揭晓 | 对 |

### 计分板核对

- 按 data.json 自己算：Asia 19、Africa 8、Europe 8、South America 7、North America 5、Oceania 3，合计 50。
- 302–309 s 的揭晓画面与此完全一致。
- 滚动途中右上角的计数抽查了 52、104、175、234、299 s，和已出场卡片的累计数相符。计数要等卡片过了中线才加，所以刚进场的卡还没计入，见 D7。

### 其他段落

| 段落 | 结果 |
|---|---|
| 片头（0–5 s） | 有标题、口径行（Elevation · Data as of Nov 2026）和来源行 |
| 来源卡（309–313 s） | 列出 Sources、Data as of、Photo credits 的说明、flags/icons/font 许可，都能读 |
| 片尾（313–331 s） | 只在顶部约 25% 放了「Thanks for watching!」，中下部全空，放 YouTube 片尾元素（2 个视频 + 订阅）空间足够 |

## 数据抽查（外部来源）

| 名次 | 山峰 | 片中 | 外部核对 | 结果 |
|---|---|---|---|---|
| 1 | Everest（CN/NP） | 8,849 m / 29,032 ft | 2020 中尼联合公布 8,848.86 m（Wikipedia Mount Everest 条目） | 对 |
| 3 | K2 | 8,611 m | Wikipedia K2 infobox：8,611 m（2014 年另有 8,609 m 实测，注释说明「most sources 8,611」） | 对 |
| 10 | Aconcagua | 6,961 m | 网络来源多为 6,960–6,962 m；库约大学 2012 年报告 6,960.8 m。Wikipedia infobox 现写 6,967.16 m，但引用的是 6,960.8 m 的报告，sources.md 已记录这处矛盾 | 可接受 |
| 20 | Elbrus | 5,642 m | Wikipedia：5,642 m | 对 |
| 30 | Mont Blanc（FR/IT） | 4,806 m / 15,766 ft | **2026-09-17 官方测量 4,807.47 m**（Euronews 2026-10-14；linfodurable 等多家报道）。2023 年为 4,805.59 m | **过时** → D1 |
| 41 | Kinabalu | 4,095 m | Wikipedia 4,095 m；mysabah / PeakVisor 4,095.2 m（1997 卫星复测） | 对 |
| 42 | Aragats | 4,090 m | Wikipedia：4,090 m | 对 |
| 43 | Mount Cameroon | 4,040 m | Wikipedia：4,040 m（注释说明 4,095 m 与 SRTM 不符） | 对 |
| 50 | Jabal an-Nabi Shu'ayb | 3,666 m | Wikipedia（Peaklist）与 PeakVisor：3,666 m | 对 |

洞察卡核对（以 data.json 为准）：

1. Cameroon「often listed at 4,095 m … nearer 4,040 m」：成立，有 SRTM 依据。
2. 「France and Italy still disagree over who owns its summit」：成立，属于有据可查的边界争议。
3. 「836 m taller than Mont Blanc」：按 data.json 算是 836.41 m，成立；但用 2026 年新值 4,807.47 m 算是 834.53 m，应写 **835 m**，见 D1。
4. 「every peak tops 6,950 m, and 9 of the last 10 are in Asia」：成立。最低的是 Aconcagua 6,960.8 m；后 10 张卡里只有阿根廷不在亚洲。
5. 「India also claims K2…」：成立。

## 缺陷清单

1. **D1 · blocker · 2:00–2:06 前后（#30 France / #30 Italy 两张卡）及 2:50–2:58（Elbrus 洞察卡）· 勃朗峰数值过时**
   - 问题：2026 年的官方两年一测已在 2026-09-17 完成，结果 4,807.47 m，2026-10-14 公布。片中仍用 2023 年的 4,805.59 m（显示 4,806 m / 15,766 ft），片头和片尾却写「Data as of Nov 2026」，违反 bible §3.3「发布前 7 天内复核，有变化就重渲」。洞察卡 3 的「836 m」也随之出错。topic.md 风险 6 推断「下一次约在 2027」，这个推断有误。
   - 建议：
     - 改 `_build/items_def.py`：value 改为 4807.47；value_display 改为「4,807 m」，secondary_display 改为「15,772 ft」；source 改为 2026 年测量（Euronews 2026-10-14 / Chambre départementale des géomètres-experts de Haute-Savoie）；notes 补上 2026 年的值。
     - 洞察卡 3 改为「… 835 m taller than Mont Blanc.」
     - 重跑 build.py 和 gen_sources.py，重渲并重新生成 publish.md。
     - 名次不受影响（4,807 m 仍在 4,884 与 4,643 之间）。
     - 顺手再全表复核一次有没有其他 2026 年的新测量值。
2. **D2 · major · 4:56–5:02（冠军段）· 并列冠军的尼泊尔卡被画面左边缘裁掉**
   - 问题：缓停后定格的构图里，China 卡完整居中，右侧配奖杯和「No. 1」标注；Nepal 卡左侧约 15% 出画，国旗、山名首字母和「8,849」的首位数字都被切掉。这既是出框问题（§7.5），又在中尼并列冠军上造成视觉偏向，评论区容易引发争议。topic.md 原本要求「冠军段把两张卡并排同时放大」。
   - 建议：渲染器支持同名次并列强调，两张 #1 卡完整、对称并排，「No. 1」标注居中或放在两卡下方，不只跟着最后一张卡。
3. **D3 · minor · 4:56–5:02 · 冠军卡没有看到 bible §2.2 要求的光晕强调**
   - 问题：画面上只有右侧的 No. 1 文字和奖杯。
   - 建议：修 D2 时一并补上。
4. **D4 · minor · 0:50–0:58 · 洞察卡 1 数字与单位被断行**
   - 问题：「4,095」和「m」、「4,040」和「m.」分在两行。
   - 建议：数字与单位之间用不换行空格（U+00A0），或者让渲染器禁止在「数字 + 单位」之间断行。
5. **D5 · minor · 约 0:03.5–0:05 · 片头过渡时标题层压在卡片上方**
   - 问题：「TOP 50」等半透明文字叠在 Yemen 卡的照片上，持续不到 1.5 s。
   - 建议：标题淡出层放到卡片下方，或者等卡片进场前完成淡出。
6. **D6 · minor · publish.md 描述末行 · hashtag「#HighestMountainInEvery」被截断**
   - 建议：改成「#HighestMountain」或「#Mountains」，再加一个 #Geography 一类的标签。
7. **D7 · minor · 全程 · 角落计分板滞后**
   - 问题：卡片要过中线才计数，所以已经完整在画面上的卡还没计入。例如 0:05.5 时 New Zealand 已在画面上，Oceania 计数还没出现；4:52 时 China 已在画面上，Asia 仍是 18。
   - 建议：改为卡片完全进入画面时计数；或者保留现状，在系列模板里写明「过中线计数」。
8. **D8 · minor · 约 0:04–0:05 · 片头最后约 0.5 s 计分板只有标签「PEAKS BY CONTINENT」，下面没有任何数字 chip**
   - 建议：第一张卡计入前先隐藏这个标签。

## 风险提示（不算缺陷，由用户决定）

- **R1 台湾**：片名是「Every Country」，台湾单列为「Taiwan」并配旗（#44，约 0:30）。sources.md 记为用户既定口径；片头没有「by de-facto control」口径行（topic.md 原计划要加），只有洞察卡 5 说明了 K2 的处理。建议片头口径行加一句「Sovereign states; peaks listed by de-facto control」，同时覆盖台湾和 K2 两个议题。
- **R2 阿富汗国旗**：用的是前共和国三色旗。这与联合国席位旗一致，但和「按实际管辖」口径不完全一致。可能有少量评论，不建议改，知悉即可。
- **R3 置顶评论链接多**：评论 1 含约 100 个链接，YouTube 可能把它自动归为「待审核/垃圾」。上传后用另一个账号确认评论可见；不行就把完整署名放到外部页面，评论里只留一个链接。
- **R4 Aconcagua**：Wikipedia infobox 现为 6,967.16 m，有观众可能据此纠错。sources.md 已有说明，评论区可直接引用。
- **R5 格鲁吉亚 / 肯尼亚先后**：取决于用 5,193 还是 5,203 m，已在 notes 中说明。
- 码率 1.37 Mbps 偏低（CRF 16，但画面多为静态平面图形）。抽帧没看到块效应，YouTube 会重新编码，不算缺陷。

## 观众视角

- 可看性：节奏平稳。每名约 5 s，前 10 名放大后停留更久；5 张洞察卡穿插得当，内容是「数据背后的争议」，信息量好，和纯滚动榜单拉开了差距。
- 不足：滚动段 4 分 50 秒画面完全匀速，没有音乐时会显得单调，音乐完成后再看一次。
- 照片：整体质量好。Ismoil Somoni 是黑白照，Yemen 和 Ras Dashen 是远景，略弱，但可以接受。Khazret Sultan 的占位卡处理得体。
- 措辞：没有发现误导或可能让频道难堪的措辞。最大的观感问题是冠军段（D2）：一个讲「并列」的片子，结尾把一方切掉一角，另一方配上 No. 1，容易被解读为偏向。

## 未能检查的范围

- 音乐与混音（§7.6）：当前是静音轨，待配乐后复审。音乐高潮是否对上前 10 名、片尾 15–20 秒是否干净，都要重新看。
- 50 条里只外部抽查了 9 座山峰；其余条目只核对了 data.json 与 sources.md 的内部一致性。Peakbagger、CIA Factbook（已停刊）无法访问。
- 图片许可没有逐张回 Commons 页面复核，只核对了账本与文件哈希的一致性和许可类型。
- 没有在真机或 YouTube 播放器里实测片尾元素的摆放，也没有实测上传后的画质。
- 没有逐帧检查全部 19,860 帧，只抽了每 2 s 的接触表和关键帧；滚动平滑度只测了 5 个时间点，freezedetect 覆盖了全片。

## 外部核对来源

- Euronews, 2026-10-14, "Mont Blanc: new French measurements, summit grows to 4,807m"：https://www.euronews.com/2026/10/14/mont-blanc-new-french-measurements-summit-grows-to-4807m
- linfodurable：「Le mont Blanc mesuré à 4.807,47 mètres」：https://www.linfodurable.fr/le-mont-blanc-mesure-480747-metres-188-metre-de-plus-quen-2023-selon-des-geometres-experts-59360
- Wikipedia API（K2、Aconcagua、Mount Elbrus、Mont Blanc、Mount Kinabalu、Mount Aragats、Mount Cameroon、Jabal an-Nabi Shu'ayb，取数日 2026-11-03）
- PeakVisor：Mount Kinabalu https://peakvisor.com/peak/mount-kinabalu.html；Jabal an-Nabi Shu'ayb https://peakvisor.com/peak/jabal-an-nabi-shu-ayb-2wc4ac.html
- mysabah：「7 mistakes about Mount Kinabalu」https://www.mysabah.com/wordpress/7-mistakes-about-mount-kinabalu/

## 复审（fresh-context 子代理，2026-11-03，第 2 轮）

- 审片对象：`render/ep02_highest_peak_by_country_master.mp4`（sha256 `04879582…1abad`，与 manifest 一致）。1920×1080，60 fps，328.0 s，19,680 帧；音轨为静音 AAC，mean/max −91 dB，按设计如此。manifest 记录的 `data.json` sha256（`df6207ed…`）、`assets.json` sha256（`824cef6e…`）与当前文件一致。
- 时间线（manifest）：intro 0–5，scroll 5–293，champion 293–299，tally 299–306，sources 306–310，end 310–328。
- 方法：
  - 抽帧：每 2 s 一张，拼成 6 张接触表，覆盖全片；另取 1280 宽关键帧，包括勃朗峰前后 4 张、Elbrus 洞察卡 3 张、Cameroon 洞察卡 2 张、冠军段 9 张（290–298.9 s）、章节时间点 7 张、回归抽查 12 张。
  - 片头：3.0–5.0 s 每 0.2 s 一帧；4.0–6.5 s 顶栏每 0.25 s 一帧。
  - 过渡：tally 过渡 298.8–301 s 每 0.2 s 一帧。
  - 其他：全片 freezedetect，以及冠军卡周边亮度采样。
- 帧文件位置：`C:\Users\light\AppData\Local\Temp\claude\C--workspace-micro-drama-platform\ce8ad49c-b9a5-4916-a2cc-04ed64900cb6\scratchpad\qc_ep02_r2\`

### 上轮缺陷逐条复核

| # | 上轮问题 | 结论 | 证据 |
|---|---|---|---|
| D1 | 勃朗峰数值过时；Elbrus 洞察卡「836 m」 | **已修复** | 1:52（112 s）时 Italy 与 France 两张 #30 卡都显示「4,807 m / 15,773 ft」，118 s 的 France 卡同样如此。<br>2:52（172 s）的洞察卡为「Next: Elbrus, Europe's highest peak, 835 m taller than Mont Blanc.」。<br>换算复核：4,807.47 m 四舍五入为 4,807 m；4,807.47 × 3.28084 = 15,772.54 ft，四舍五入为 **15,773 ft**，正确。上轮建议写的 15,772 是笔误，全片英尺值统一用四舍五入，例如 Everest 为 29,032。5,642 − 4,807.47 = 834.53，取 835 m，正确。<br>data.json 两条 #30 的 value 为 4807.47，source 为 Haute-Savoie 2026-09-17 测量（Euronews 2026-10-14），cross_check 保留 Wikidata 的 4,805.59，notes 列出 2013/2021/2023/2026 四个值。<br>sources.md §4 第 80–81 行与 data.json 一致；topic.md 第 29、32、43 行已更新；publish.md 评论 2 第 172–173 行的出处已改为 2026 测量。<br>排序仍单调不增：4,884 > 4,807.47 > 4,643。 |
| D2 | 冠军段尼泊尔卡被左边缘裁掉 | **已修复** | 293–298.9 s 定格时，Nepal 卡在 1280 宽画面中位于 x≈190–610，China 卡位于 x≈670–1090。两卡等宽等高、完整，并排对称，中心正好在 640。两卡的国旗、山名、8,849 m / 29,032 ft、两个 tag 和 SHARED WITH 徽章全部可见；原来只跟随一侧的「No. 1」与奖杯标注已经去掉，偏向问题消除。 |
| D3 | 冠军卡无光晕 | **已修复** | 两张卡四周都有浅蓝色光晕，放大提亮后两卡一致可见。亮度采样：卡外侧约 50–57，远处背景 45.9，两卡间隙 60–68；不同帧亮度在 42–57 间变化，说明光晕呈呼吸式。freezedetect 也显示 293–299 s 不是静帧。 |
| D4 | 洞察卡 1 数字与单位断行 | **已修复** | 0:52 时洞察卡断行为「often listed at / 4,095 m, but satellite / data puts it nearer / 4,040 m.」，数字与单位在同一行。另外 4 张洞察卡也没有拆开数字和单位，包括「835 m」和「6,950 m,」。 |
| D5 | 片头过渡时标题压在卡片上 | **已修复** | 3.0–5.0 s 每 0.2 s 逐帧查看：标题在 3.4–3.6 s 淡出，3.8 s 为空背景，4.0 s 第一张卡才从右侧进场。没有任何一帧出现标题与卡片叠加。 |
| D6 | publish.md hashtag 被截断 | **已修复** | 描述末行为「#HighestMountainInEveryCountry #Top50 #Ranking #DataComparison」，完整、无截断。 |
| D7 | 角落计数滞后（要过中线才计） | **已修复** | 现在卡片完全进入画面即计数，抽查结果如下：<br>• 104 s：Italy 卡未完全进场，EUROPE 4；<br>• 112 s：Italy 与 France 都完整，EUROPE 6；<br>• 118 s：Indonesia 完整，OCEANIA 由 2 变为 3；同时 Venezuela 只露一半，没有出现 SOUTH AMERICA；<br>• 172 s：Russia 完整，EUROPE 8；<br>• 270 s：India 完整，ASIA 16；<br>• 290 s：两张 #1 都在画面里，ASIA 19。<br>这些数字都与 data.json 中已完整出场的卡片累计数一致。 |
| D8 | 片头末段只有「PEAKS BY CONTINENT」标签、没有数字 chip | **未修复（minor）** | 4.25–4.75 s 顶栏已显示「PEAKS BY CONTINENT」，下面仍没有 chip；而 Yemen、Spain 在约 4.4 s、New Zealand 在约 4.8 s 已完整在画面上。到 5.0 s 三个 chip（OCEANIA 1 / EUROPE 1 / ASIA 1）才同时出现。空标签持续约 0.75 s，片头这几张卡的计数也滞后到滚动段开始才补上。 |

### 章节与发布文案复核

| 章节 | 时间 | 画面（按帧） | 结果 |
|---|---|---|---|
| Intro & #50–#41 | 0:00 | 片头标题（第 0 帧是淡入前的背景，0.7 s 起标题清楚） | 对 |
| #40–#31 | 0:58 | Cameroon 洞察卡 + #40 Toubkal + #39 Tajumulco | 对 |
| #30–#21 | 1:51 | Mont Blanc 洞察卡 + #30 Italy + #30 France（4,807 m） | 对 |
| #20–#11 | 2:55 | Elbrus 洞察卡（835 m）+ #20 Russia + #19 Colombia | 对 |
| Top 10 | 3:54 | 「From here on…」洞察卡 + #10 Aconcagua + #9 Khan Tengri | 对 |
| No. 1 | 4:49 | #3 K2 局部 + #1 Nepal + #1 China，正在缓停 | 对 |
| Peaks by continent | 4:59 | 299.0 s 冠军段开始叠化，299.4 s 计分板完全出现 | 对（落在叠化起点，可接受） |

- 章节间隔分别为 58、53、64、59、55、10 s，末章 29 s，都 ≥ 10 s。
- 字数：描述 3,539 字符（≤ 5,000），置顶评论 1 为 8,949 字符，评论 2 为 5,384 字符（都 ≤ 10,000）。三段文案都没有 `<` `>`。
- 计分板揭晓：Asia 19 / Africa 8 / Europe 8 / South America 7 / North America 5 / Oceania 3，合计 50，与 data.json 一致。
- 封面 `render/thumbnail.png`：China #1 8,849 m、Nepal #1 8,849 m、Pakistan #3 8,611 m，没有过时数值。

### 回归抽查

- 抽查范围：8、30、75、95、135、150、195、215、250、270、304、308 s，共 12 帧，加上 6 张全片接触表。
- 没有发现新的出框、重叠、错旗或错值。Khazret Sultan 占位卡正常；来源卡和片尾与上轮相同。
- freezedetect：冻帧只出现在片头标题停留（0.7–3.2 s）和计分板、来源卡、片尾的静止段（300.2 s 起），滚动段 5–293 s 和冠军段都没有冻帧。

### 新发现

1. **N1 · minor（文档，不进成片）· sources.md §5 第 110 行 · 洞察卡依据没跟着改**
   - 问题：文案已改为「835 m」，「数据支持」一栏却仍写「Elbrus 5,642 − Mont Blanc 4,805.59 = 836.41 m」。这一栏由 `_build/gen_sources.py` 第 81 行硬编码生成。
   - 建议：改为「5,642 − 4,807.47 = 834.53 m」，然后重跑 gen_sources.py。
2. **N2 · nit · 293–299 s 冠军定格 · 左侧仍露出约 1/4 张 #3 K2 卡，右侧是空背景**
   - 问题：两张 #1 卡本身已经对称居中，但整幅画面左重右轻。
   - 建议：可选改进，例如让 #3 在定格前淡出，不影响发布。

### 风险提示（沿用上轮，由用户决定）

- R1：片头仍没有「Sovereign states; peaks listed by de-facto control」一类的口径行，台湾和 K2 的口径只靠洞察卡 5 说明。
- R2–R5：维持上轮判断，没有变化。

## 结论（第 2 轮）：**可发布（静音画面版）**

- 上轮的 blocker D1 和 major D2 都已修复，minor 里 D3–D7 已修复。
- 剩余 D8（片头约 0.75 s 空标签）和 N1（sources.md 内部依据未同步）都是 minor，不阻塞上传。建议上传前顺手修好 N1，D8 可以留到系列模板统一处理。
- **音乐仍待制作**：§7.6 未检。配乐完成后需要再审一次，看混音有没有爆音、高潮是否对上前 10 名（3:54 起）和冠军段（4:53–4:59），片尾 18 s 是否干净，然后才能作为最终成片上传。

## 作者修复记录（代理，2026-11-03，第 2 轮复审之后；非审稿结论）

- D8（片头 4.2–5.0 s 计分板标签无计数）：渲染器改为片头淡入时显示当前可见卡片计数；已重渲，t=4.6 s 帧确认显示 OCEANIA 1 / EUROPE 1 / ASIA 1。
- sources.md 第 110 行 Elbrus 差值依据改为 5,642 − 4,807.47 = 834.53 m（显示 835 m），由 `_build/gen_sources.py` 重新生成。
- 当前母版：`render/ep02_highest_peak_by_country_master.mp4`（328 s，sha256 前 16 位 b47b2e2b10d86aca）。仅上述两处变动，未再独立复审；配乐加入后需要再审一次音频。

## 回归检查（fresh-context 子代理，2026-11-03，第 3 轮）

- 审片对象：`render/ep02_highest_peak_by_country_master.mp4`，sha256 `58756ed0…a0b38`，与 manifest 一致；上轮作者记录里的 `b47b2e2b…` 已被这次重渲取代。
  - 规格：1920×1080，60 fps，328.0 s。
  - 时间线：intro 0–5，scroll 5–293，champion 293–299，tally 299–306，sources 306–310，end 310–328。
  - manifest 记录的 `data.json`、`assets.json` 哈希与当前文件一致。
- 本轮起因：渲染器有改动，涉及 #32 新占位卡、片头时序、计分板版面，以及 `publish.md` 新增的 scope_note。
- 方法：
  - 片头 3.0–5.0 s 每 0.25 s 一帧，并测逐帧亮度。
  - 80–116 s 接触表，用来定位 #32；#32 占位卡取 1280 宽和 640 宽各一帧。
  - 冠军段 296 s；计分板 300、300.5、303 s；来源卡 308 s；片尾 315 s。
  - 章节点 0.8、58、111、175、234、289、300 s。
  - 随机帧 20、70、140、200、250、280 s。
  - 60、140、250 s 测滚动位移；全片 freezedetect。
- 帧文件位置：`C:\Users\light\AppData\Local\Temp\claude\C--workspace-micro-drama-platform\ce8ad49c-b9a5-4916-a2cc-04ed64900cb6\scratchpad\qc_r2b\e2\`。

### 检查结果

| 项 | 结果 | 证据 |
|---|---|---|
| 片头 3.0–5.0 s | **通过** | 标题在 3.0–3.55 s 淡出，约 3.57 s 第一张卡（#50 Yemen）从右侧进场。中间只有约 0.05 s 是空背景，没有任何一帧出现标题和卡片叠加。<br>顶栏和计分板在 4.0–4.5 s 淡入，淡入时就带着 OCEANIA 1 / EUROPE 1 / ASIA 1 三个计数。上轮的 D8（标签下没有数字）确认已修复。<br>小瑕疵（nit）：4.25 s 时 New Zealand 卡还没完全进画面，OCEANIA 就已经计 1，和 D7「完全进场才计数」的规则差一点，肉眼察觉不到 |
| #32 Khazret Sultan 占位卡 | **通过（附 minor）** | 新样式是乌兹别克斯坦国旗 + 山形图标 + 蓝色渐变底，下方写「No free-licensed photo found」，说法如实。卡头国旗、国名和「#32」都对，山名、山脉、4,643 m / 15,233 ft 清楚。<br>问题：说明文字是白字压在浅蓝底上，对比度约 **1.31:1**，在 640 宽手机尺寸下读不出来（见 M1）。<br>描述和评论 1 都没有为 #32 写署名，这是对的；署名一共 49 条 |
| 冠军段 | **通过** | 帧 296 s：Nepal 和 China 两张 #1 卡等大、并排、完整，以画面中线对称，都有 SHARED WITH 徽章，数值都是 8,849 m / 29,032 ft。左边仍露出约 1/4 张 #3 K2 卡（上轮的 N2，nit，没有变化） |
| 计分板 | **通过（版面 nit）** | 帧 300 和 303 s：Asia 19、Africa 8、Europe 8、South America 7、North America 5、Oceania 3，合计 50，与上轮一致。新版面是标题加 6 行条形，整体偏上，下方约 25% 空着，可以接受 |
| 来源卡和片尾 | **通过** | 来源卡（308 s）写「Sources: Wikidata (CC0), national surveys, Wikipedia / Data as of Nov 2026 / Photo credits… / Flags · Icons · Font」。片尾（315 s）只有顶部的「Thanks for watching!」，与上轮相同 |
| 随机帧 | **通过** | 20、70、140、200、250、280 s 共 6 帧，加上 80–116 s 的接触表：没有出框、错旗、错值或重叠。勃朗峰两张卡都是 4,807 m / 15,773 ft，Elbrus 洞察卡是 835 m，都没有回退 |
| 运动和冻帧 | **通过** | 60、140、250 s 都是 2 px/帧，残差 ≤0.018。freezedetect 显示冻帧只出现在片头标题停留（0.68–3.02 s）、冠军定格中间约 0.5 s，以及 300.2 s 之后的计分板、来源卡和片尾静止段。滚动段没有冻帧 |

### 章节与发布文案

| 章节 | 时间 | 画面（按帧） | 结果 |
|---|---|---|---|
| Intro & #50–#41 | 0:00 | 片头标题（0.8 s 已清楚） | 对 |
| #40–#31 | 0:58 | Cameroon 洞察卡 + #40 Toubkal + #39 Tajumulco | 对 |
| #30–#21 | 1:51 | Mont Blanc 洞察卡 + #30 Italy + #30 France | 对 |
| #20–#11 | 2:55 | Elbrus 洞察卡 + #20 Russia + #19 Colombia | 对 |
| Top 10 | 3:54 | 「From here on…」洞察卡 + #10 Aconcagua + #9 Khan Tengri | 对 |
| No. 1 | 4:49 | #3 K2 局部 + #1 Nepal + #1 China | 对 |
| Peaks by continent | 5:00 | 计分板已完整显示 | 对。上轮是 4:59，落在叠化起点；这次改为 5:00，更准 |

- 章节间隔分别为 58、53、64、59、55、11 s，都 ≥10 s。
- 字数：描述 3,843 字符（≤5,000），评论 1 为 8,949 字符，评论 2 为 5,384 字符（都 ≤10,000）。三段都没有 `<` `>`。hashtag 完整。
- 口径说明：描述里新增了「What counts: the highest point of each sovereign country, listed under the country that controls it (de-facto administration). Summits on a border count for every country that shares them… Equal heights share a rank.」，和 `data.json` 的 `scope_note` 一致。这句话同时说清了 K2 和共享山峰的处理，上轮的风险 R1 在描述层面已经部分回应，片头仍没有对应的口径行。还有一点提醒：台湾不是联合国会员国，写「sovereign country」可能仍会被人挑字眼。这属于用户既定口径，知悉即可。

### 新发现

1. **M1 · minor · 约 1:37–1:43（#32 占位卡）· 说明文字对比度过低**
   - 问题：对比度约 1.31:1，手机上读不出来。全片只有这一张占位卡，排名靠后，卡上的国旗和山形图标已经表达了「没有照片」，所以不阻塞发布。
   - 建议：和 ep01 的 N1 一起，在渲染器里把占位说明改成深色字或加深色底带，下次重渲时带上。

## 结论（第 3 轮）：**可发布（静音画面版）**，维持第 2 轮结论

- 渲染器改动没有引入回归。D8 确认已修复。
- 新增的只有 M1（minor）和两处 nit：计分板版面偏上、片头计数早约 0.25 s。都不阻塞上传。
- **音乐仍待制作**，配乐后需要再审一次音频（§7.6）。

## 第 3 轮复核（fresh-context 子代理，2026-11-03）

本节接在上面的「回归检查（第 3 轮）」后面，用来复核渲染器修复后的 M1。被审母版的 sha256 与 manifest 一致（`c8277a96…`，10:54 重渲）。

| 项 | 结论 | 证据 |
|---|---|---|
| M1 #32 Khazret Sultan 占位卡说明文字对比度低 | **已修复** | 帧 100 s：「No free-licensed photo found」下面加了深色圆角底条（约 RGB 9,25,37），字是白色。用 PIL 在 1920×1080 原帧上取色，按 WCAG 公式算，对比度 **17.8:1**，上轮约 1.31:1。底条外的蓝色渐变（约 RGB 27,80,115）放白字也有 8.6:1。在 1280 宽和 640×360 下都看过，手机尺寸能读。乌兹别克斯坦国旗、山形图标、#32、4,643 m / 15,233 ft 都对 |
| 发布文案字数 | **通过** | 描述 3,842 字符，评论 1 为 8,948 字符，评论 2 为 5,383 字符，都在上限内。三段都没有 `<` `>`。也没有「CTBUH」字样 |

### 回归抽查（6 帧）

4、47、171、262、298、309 s 这 6 帧：

- 片头和第一组卡：#50 Yemen、#49 Spain。
- 滚动段：#42–#41 加 Cameroon 洞察卡；#21 Mexico、Elbrus 洞察卡、#20 Russia；#7–#4。
- 冠军段：Nepal 和 China 两张 #1 卡并排，都有 SHARED WITH 徽章，都是 8,849 m。
- 来源卡。

以上都正常，没有出框、错旗、错值或重叠。

### 新发现

- **nit**：说明文字的字号没有放大，字高约 18 px（1080p）。现在对比度已经够，不阻塞。

## 结论（第 3 轮复核）：**可发布（静音画面版）**

- M1 已修复，重渲没有引入回归。
- **音乐仍待制作**，配乐后需要再审一次音频（§7.6）。

## 第 4 轮：版式 v0.2（满版照片卡）独立审片（fresh-context 子代理，2026-11-03，follow-up 004）

背景：用户反馈「图片占比太少」，要求优先级为照片 > 国旗 > 关键数值。渲染器升到 rank_scroll 0.2.0：照片铺满卡片（本期卡宽 720），左上角大国旗，右上角名次，底部渐变上放国家、名称、数值；地点和标签并成一行小字。本轮审的是第一次重渲的静音母版。

**结论：可发布（静音画面版），只需小修。**

- **优先级达成**：滚动时同屏约 2.8 张卡，卡片约占画面 65–70%。没有被遮挡的照片约占 35–40%，算上底部渐变下还能看到的部分约 60%（v0.1 约 24%）。视线顺序是照片 → 国旗（约 200×135 px）→ 大号数值。
- **运动**：逐帧测量，匀速 2 px/帧，没有跳帧，结尾缓停平滑。
- **前 10 名卡**：放大后不碰页头、进度条和相邻卡。

| 级别 | 发现 | 处理 |
|---|---|---|
| 中 | 几张照片主体不清楚：#36 Karisimbi 只有坡面看不到峰顶，#50 也门照片发灰、偏平，而且是第一张卡；#16 Logan 认不出主峰；#6 Ismoil Somoni 近乎单色 | 待换图（优先换 #50），本次未改 |
| 低 | 雪景上白色「SHARED WITH…」药丸边缘看不清 | **已改**：徽章改成深底白字，已重渲 |
| 低 | 并列第一时没有 No. 1 侧栏，第 2 名空缺，观众可能会问 | 待定：考虑加「Tied: same summit」小字 |
| 低 | 结尾统计每行都用同一个地球图标 | 待改 |
| 低（可接受） | 页头计分最多显示 4 个，北美和大洋洲到后半段会被挤掉 | 不改 |

- **音乐**：Suno 自动生成每次在 Create 后都被验证码拦住；用户完成验证后也没有出歌，已在库里确认没有生成。仍是静音，配乐后需要再审一次音频。

## 第 5 轮：全部换图 + Suno 配乐后的独立音画审片（fresh-context 子代理，2026-11-04，follow-up 011 / 021 / 033）

审的是 `render/ep02_highest_peak_by_country_master_with-risk-images.mp4`（372.0 s）：50 张卡全部换图，其中 3 张是 AI 插画；Suno 三段配乐。
- **画面**：每 3 s 抽一帧，另放大 16 张卡，并对照 6 张原图。
- **音频**：ebur128、接缝 RMS、节拍自相关、频谱图。

**结论：修后可发布。**

| 级别 | 发现 | 处理（2026-11-04） |
|---|---|---|
| 高 | 24 张风险图的署名行能看到 All rights reserved、CC BY-NC、unknown | 不改。发布前由用户签字，否则发默认版 |
| 中 | #6 Ismoil Somoni 峰顶在国旗下面 | 换成 c2（Martin Mergili，CC BY-NC-SA，仍是风险图），焦点设为 x=0.35，峰顶在国旗右侧 |
| 中 | #50 也门 AI 图是远景，发灰无力 | 重新出图（Codex，已记日志）：近景宽阔山体，峰顶设施和梯田可见，山形按维基首图 |
| 中 | #18 Hkakabo Razi AI 图没有明确主峰 | 重新出图：单一冰雪金字塔主峰居中 |
| 中 | AI 卡的署名是 "Photo: AI illustration"，自相矛盾 | 署名改为 "Illustration: AI-generated, not a photo"，渲染器见到 `Illustration:` 就不再加 "Photo:"。`tile_images.py` 和 bible 同步修改 |
| 中 | #17 Kilimanjaro 画面主体是大象 | 换成 c1：Kibo 雪顶全貌，Pexels |
| 低 | #4 Kangchenjunga 上部是雾霾天空 | 换成 c6：Unsplash，日照金山，主峰填满上半部 |
| 低 | #7 Noshaq 峰顶被国旗挡住一部分 | 换成 c2，峰顶居中 |
| 低 | #26 乌干达 Mount Stanley 主体不明显 | 换成 c1：雪峰群清楚，仍是保留所有权利的风险图 |
| 低 | Mount Cameroon 的洞察卡放晚了 | `after_rank` 从 41 改为 43 |
| 低 | 开场 20 s 偏轻（-26 到 -23） | 曲 A 改从 20 s 起，片头 5 s 后正好进入主段 |
| 低 | 接缝 1 之后能量回落 | 曲 A 截到 150 s，切在原曲较安静的段落，接曲 B 20 s 处（两边都约 -17 LUFS）；交叉淡化改为等功率。回到曲 A 的末段对齐片尾，A 的高段（原曲 160–180 s）落在视频约 325–345 s，即 #1 揭晓 |
| 低 | #1 是两国并列（中国、尼泊尔），没有右侧的 "No. 1" 标注 | 不改。渲染器只在冠军唯一时显示这个标注，并列时两张卡都有光晕 |
| 低 | #38 Khüiten 是近景 | 不改 |

修后接触表已逐张复核 50 张卡，四个版本重渲中，渲完做第 6 轮复审。

## 第 6 轮：第 5 轮修复后重渲的独立复审（fresh-context 子代理，2026-11-04，follow-up paihangbang 040）

审的是 `render/ep02_highest_peak_by_country_master_with-risk-images.mp4`（372.0 s），sha256 与 manifest 一致。逐卡抽帧加放大图；用 ebur128、频谱和波形相关查音频。

**结论：可发布。前提是用户对 24 张风险图逐张签字，否则发默认版。**

第 5 轮修复已生效：
- **画面**：#6 峰顶在国旗右侧；#17、#4、#26 换图正确；Mount Cameroon 洞察卡在 #43 之后。
- **AI 卡**：3 张都有「AI IMAGE」徽章，标注 "not a photo"。
- **接缝 2**：平滑。

其他核实结果：
- 名次、数值、洞察和计分都与 data.json 一致。
- 响度 -16.0 LUFS，真峰值 -3.6 dBTP。

| 级别 | 发现 | 处理 |
|---|---|---|
| 流程 | 24 张风险图需要用户签字 | 待用户签字 |
| 低 | 123–150 s：曲 A 原曲安静段，S 最低 -20.5。接缝本身平滑 | 不改，交用户试听决定 |
| 低 | 第三段从曲 A 111.8 s 起，和第一段截到 150 s 有重叠：视频 91.8–130 s 的约 38 s 音乐在 277–315 s 重放 | 不改。要对齐 #1 的高段，又要铺满 372 s，必须重复一段；用户若在意，可以再生成一首 Suno 曲替换 |
| 低 | 开场 8.5–21.5 s 回落到 -17 到 -21.7 | 不改，交用户试听 |
| 低 | #7 Noshaq 原图带一道镜头光斑，整体发灰（峰顶完整） | 不改 |
| 低 | #1 并列冠军段没有独立的高潮抬升（S 约 -14，和前段持平） | 不改 |
| 低 | 计分板六个大洲用同一个地球图标（第 4 轮遗留） | 不改 |
| 低 | #15 Denali 署名 "unknown / Public domain:Full Granting Rights" 字面别扭 | 不改 |
