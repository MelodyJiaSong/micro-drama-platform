# ep11 世界最大船舶 · 审片记录（qc.md）

## 配乐审片 · 2026-11-04（独立上下文，两轮）

> 补配乐后由另起上下文的审稿代理测量（未参与制作）；测量脚本与数据在会话 scratchpad `audio_qc/`、`audio_qc2/`。只换音轨，视频流与 `render/_silent/` 原静音版逐流哈希一致（21763 帧）。

**结论：小修后发布（音频无 blocker）**，上面画面复核里唯一的待办 M4「补配乐」已解决。
- 配乐：Suno 任务 87691a72，两首（17799228 / f5ab22d7，95.7 BPM），用 `add_music.py` 按 f5ab@0–145 → 1779@20–140 → f5ab@40–135 → 1779@155–末尾 拼接，4 s 交叉淡化，最后一段放到原曲自然结尾。
- 第 1 轮（A-B-A 直接拼）发现 170–187 s 约 10 LU 的能量洞、片尾画面是全片最响处 → 重排后：响度 −16.0 LUFS，真峰值 −3.9 dBTP；170–187 s 从 −21.7 升到 −16.5；冠军停留 −14.3（原 −15.8）；中段最差 15 s 为 −19.2（原 −21.8）。无削波、无断音，接点处无拼接爆音（最大瞬态均来自 Suno 原曲）。
- minor（需人耳听）：352 s 前后第 3 个接点两曲节拍错开约 1/3 拍，片尾卡上可能听到约 2 s 的“双拍”；片尾 10 s 仍略响于冠军段（约 0.5 LU）。
- `publish.md` 描述框已补 Suno 署名（job 87691a72，clips 17799228 / f5ab22d7），清单已补「不登记 Content ID」。

## 复核 · 2026-11-04

> 独立复核人：另起上下文，没有参与制作，也没有写第 1 轮审片。只写了本文件和 `_build/qc/recheck/`，数据、图片和渲染都没有动。
> 复核对象：`render/ep11_largest_ships_master.mp4`（默认版，04:58）和 `render/ep11_largest_ships_master_with-risk-images.mp4`（风险版，05:03）。两版 manifest 里的 data.json（09d218…）、assets.json（514134…）和全部 47 张图的 sha256 都与现有文件一致，说明成片是用当前输入渲出来的。

### 结论：**小修后发布**，推荐发布**默认版**

画面上的 blocker 已经清零。B1、B2 和 M1 列出的 5 张卡，现在都能看出是船；M2、M3、M5、M6 也都改了。

发布前只差一项：**补配乐**。两版的音轨现在仍是 -91 dB 静音（M4）。配乐用音轨合成补上就行，不需要重渲画面。补完后要做一次响度检查和片尾淡出检查，这两项本轮没法查。

制作方点名的两张遗留卡，我判断都**不阻碍发布**：
- **#13 Hamburg Express class**：船体和「Hapag-Lloyd」字样确实落在文字区下面，只能隐约看到。不过上半张是满载集装箱的船舱段和 APM 岸桥，作为一张集装箱船卡认得出来，与第 1 轮「只有逆光岸桥和天空」的情况不同。这张原图是横幅照片，正方形裁切已经用满全高，调焦点救不回来，要改只能换一张船体下方留出更多水面的照片。列为可选优化。
- **#25 Triple-E**：船首正面很完整，一眼能认出是船，构图也有冲击力。HDR 橙色高光和颗粒感跟全片风格不太统一，属于审美问题（维持 m6 minor），不影响信息传达。

### 逐条核对

| 原问题 | 结论 | 核实依据（本轮帧在 `_build/qc/recheck/master/`、`risk/`） |
|---|---|---|
| B1 #30 Berlin Maersk 看不到船 | **已修** | 改用预裁切，`0097.43_r30_…`：船尾、烟囱「ALL THE WAY TO ZERO」和蓝色船体都清楚。原图只有 777 px，画面略软，可以接受。`zoom_r30_card.png` |
| B2 #13 卡面只有岸桥和天空 | **已修（有遗留，可选）** | 换成 Busan Express 实拍，卡名改为 Hamburg Express class。`0226.70_r13_…`、`zoom_r13_card.png`：能认出是集装箱船，但船体在文字区下（见上） |
| M1 #1 冠军卡看不出船 | **已修** | 默认版换成 kees torn 的侧面照，生活区、黑色船体和「Allseas」字样都看得见（`0327.72_r1_…`、`0328.50/0331.00/0333.50_champ_*`）。缺点是看不出双体船身的尺度。风险版的北海航拍更有气势 |
| M1 #42 Emma（片头首卡） | **已修** | 驾驶楼、箱墙和船体「MAERSK」字样都看得见（`0006.00_r42_…`） |
| M1 #35 Marco Polo | **已修** | 驾驶楼、箱区，加船体「CMA」字样（`0057.30_r35_…`） |
| M1 #24 Barzan | **已修** | 换成 Hapag-Lloyd 涂装，船名字样在文字区上方（`0139.43_r24_…`）。m3 涂装和国旗对不上的问题一并解决 |
| M1 #5 Saadé | **已修** | 绿色船体上能看到「CMA CGM JACQUES SAADE」，GAS AGILITY 已经不在画面里（`0290.58_r5_…`） |
| M2 远海丝路未收 | **已修** | 收为 #31，180,011 GT，计入 China，N = 42。卡上有 AI IMAGE 角标和 NEW 2026 徽章。名次 1–42 连续，数值严格递减 |
| M3 国家口径 | **已修（替代做法）** | 片头、每帧底栏和来源卡都写了「Flag = operator HQ」；HK、ONE→SG、Valemax/Guaibamax→BR 的细则写在描述框 scope 段。计分板页没有单独加脚注，可以接受。Excellence 级按 Costa Toscana 归 Italy，卡名改为 Excellence class |
| M4 母版静音 | **未修** | 两版 volumedetect 都是 mean/max -91.0 dB。**这是发布前的必修项** |
| M5 风险版过期、署名不合格 | **部分修** | 已经用当前数据和渲染器重渲。卡上署名改成真实来源，例如「Allseas (via gCaptain) / unknown」。但 #1、#2、#21、#33、#38 这 5 张图的许可仍然不明，需要用户签字放行 |
| M6 #42 可读时间不足 | **已修** | intro_hold 2.5。7.4 s 时 #42 仍完整，8.0 s 才开始出屏（`0005.50`–`0008.50_hold_*`） |
| m1 船级命名 | **已修** | 卡名改为 Hamburg Express class。sources.md 统一成 Berlin Maersk；只有文件名和 key 还是 beijing_maersk，属于内部命名，不上屏 |
| m2 Star Princess 注记 | **已修** | assets.json 里 `33_sphere.jpg` 的 subject_note 已改为 Star Princess |
| m3 涂装和国旗 | **已修** | Barzan 换成 Hapag 涂装；MOL Triumph 副标题加了「now ONE」 |
| m4 封面剧透冠军 | **已修** | `render/thumbnail.png` 改成 #2–#4，没有 #1（`thumb_small.jpg`） |
| m5 AI 图 | 维持 | 默认版现在有 6 张 AI 图：#10、#22、#31、#33、#37、#38，卡上都有黄色 AI IMAGE 角标，署名写「AI-generated image, not a photo」。描述框写的是「6 images」，数目对得上。风险版 4 张，也都有角标 |
| m6 Triple-E HDR | **未修（不阻碍）** | 见上 |
| m7 checklist 措辞 | **已修** | 已改为「卡上标 AI IMAGE，署名注明 AI-generated」 |
| m8 Excellence 命名 | **已修** | |
| m9 #1 382 m 与 LOA 477 m | 未改（可接受） | 评论区备好回复即可 |

### 新问题

- **n1（minor，内部文档）**：data.json #38 Guaibamax 的 `notes` 和 sources.md 第 62 行仍写着 Yuan Hai Si Lu「so it is NOT listed (to confirm before publishing)」，和它已收为 #31 的现状矛盾。这段文字不上屏，也不在 Comment 2 里，建议顺手改掉。
- 没有发现其他新问题：
  - 名次 1–42 连续，数值严格递减。
  - 6 张洞察卡的位置都对：after 39 写「just below No. 42」；after 31 写「7 of 42」，NEW 2025/2026 徽章数正好 7；after 15 后面接 #14 Ever G；after 7 的「3 container classes」指 #3–#5；after 2 的 62% 也对。
  - 计分板终值 CH 8 / FR 6 / DK 5 / US 4 / CN 4 / TW·HK·SG 3 / DE 2 / BR 2 / KR 1 / IT 1，合计 42，与 data.json 一致。本轮帧里的角落累计也都核对过，计数随卡片递增，没有发现跳号。
  - 长标题「CMA CGM Antoine de Saint Exupéry class」自动缩小了字号，没有出框；「· now ONE」副标题也没有出框。

### 技术核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 分辨率 / 帧率 | 1920×1080 / 60 fps，H.264 yuv420p | 同左 |
| 时长 / 帧数 | 362.717 s / 21,763 帧 = `rank_scroll timeline` 21,763 帧 ✓ | 同左 ✓ |
| 全片解码 | 0 错误（`recheck/decode_master.log`） | 0 错误（`recheck/decode_risk.log`） |
| 卡帧 | 只有计分板定格（336.1 s 起）、来源卡和片尾三段静帧，都在预期内；滚动段没有冻结（`recheck/freeze_master.log`） | 未单独跑 |
| 音轨 | AAC 48 kHz 双声道，-91 dB 静音 → M4 | 同左 |
| validate --strict | OK，42 items、6 insights | |

描述框章节 0:00 / 1:37 / 2:52 / 4:07 / 5:23 / 5:34，和卡片出场时间（#30 97.4 s、#20 172.6 s、#10 248.0 s、#1 入画约 323 s、计分板 333.7 s）对得上。标题 57 字符，含「Top 42」。42 条署名齐全，Flickr 图都附了许可链接。

### 推荐发布哪一版

**默认版。** 默认版的实拍图全部是 CC BY / BY-SA / CC0 / PDM 授权，另外 6 张 AI 图都有标注，没有授权风险。

风险版有 5 张图（#1、#2、#21、#33、#38）许可不明，卡面上直接显示「/ unknown」。这 5 张里 #1 冠军卡的航拍和 #38 的旋筒帆实拍确实更好看，但只有用户签字放行、并补齐授权，才考虑发风险版。现在默认版的冠军卡已经能看出是船，画面上的差距不足以抵消授权风险。

### 发布前清单

1. 补配乐（Suno 曲目或 ep04 的 `add_music.py`），只合成音轨。然后检查响度（目标值以 bible §5 为准）和片尾淡出。
2. 可选：顺手改 n1；#13 有余力再换图（要求船体下方留足水面）；#25 HDR 维持现状即可。
3. 上传时「Altered or synthetic content」选 Yes（默认版有 6 张 AI 图）。

### 本轮抽帧（`_build/qc/recheck/`）

- 默认版 69 帧（`master/`）：
  - 片头 1.0 / 4.9 s；
  - 起始停留 5.5 / 7.0 / 7.4 / 8.0 / 8.5 s；
  - 42 张卡居中时刻各 1 帧（时刻见 `card_times.json`）；
  - 6 张洞察卡；
  - 冠军 328.5 / 331.0 / 333.5 s；
  - 计分板 334.5 / 337.0 / 340.5 s；
  - 来源卡 342.5 s；
  - 片尾 345.0 / 362.6 s；
  - 随机 5 帧：79.63 / 86.41 / 137.38 / 216.11 / 269.43 s。
- 风险版 24 帧（`risk/`）：#1、#2、#10、#13、#21、#22、#30、#31、#33、#37、#38，以及片头、冠军、计分板、来源卡、片尾，外加随机 41.83 / 89.27 s。
- 拼图：`sheet_m_01–18.jpg`、`sheet_r_01–06.jpg`。放大图：`zoom_r13_card.png`、`zoom_r25_card.png`、`zoom_r30_card.png`、`thumb_small.jpg`。
- 脚本：`card_times.py`、`extract.py`、`tile.py`。

## 第 1 轮独立审片 · 2026-11-04

> 独立审片人（另起上下文，未参与制作）。按 `bible.md` §7 与审片说明逐项核对。只写本文件和 `_build/qc/`，没有改数据、图片和渲染。
> 审的产物：`render/ep11_largest_ships_master.mp4`（默认版，2026-11-04 03:43）、`render/ep11_largest_ships_master_with-risk-images.mp4`（风险版，2026-11-04 02:27）。

### 结论：**必须修**（修完重渲默认版，可发布）

数据主值可靠：抽查 16 条，与 VesselFinder / DNV 缓存全部一致。排序、名次、计分板计数也都对。两版成片帧数完整（21,193 帧，与 manifest 时间线一致），全片解码无错，滚动段没有卡帧。

必须修的是画面：**#30、#13 两张卡裁切后完全看不到船**，另有 5 张卡（含冠军和第一张卡）看不出是船。另外几项要在发布前处理：远海丝路未收的理由站不住；国家口径没有在片内说明，Excel 级归德国和「运营公司总部」口径也对不上；母版仍是静音；风险版是旧渲染。

### 逐项结论

| 项 | 结论 | 摘要 |
|---|---|---|
| 1 数据 | 小修 | 抽查 16 条全对，排序与 value 一致；远海丝路未收要改（major）；船级名两处不一致（minor） |
| 2 图片 | **必须修** | 认船全部正确（同型姊妹船都在 `subject_note` 写明，见下表）；但满版正方形裁切后有 2 张卡看不到船、5 张卡看不出主体 |
| 3 成片 | 小修 | 规格、帧数、解码都合格；第 41 名可读时间不足；静音；风险版过期 |
| 4 包装 | 小修 | 标题 57 字符；默认版来源与署名完整，有 AI 图声明；缺国家口径说明；封面提前公布了冠军 |
| 5 观众 | 小修 | 冠军是起重船、GT 不是重量、瑞士内陆国拿第一，这几处反常识点都好；29/41 张集装箱船外加几张裁坏的图，中段容易划走 |

### 问题清单

#### Blocker

**B1 · #30 Berlin Maersk class（1:20–1:26，两版都有）：卡面只有 APM 码头岸桥，船不在画面里。**
- 证据：`_build/qc/frames/master/0082.80_r30_Berlin_Maersk_class.png`。原图 `30_beijing_maersk.jpg` 里 Barcelona Mærsk 只露船尾，位置在画面左下（x 约 10–45%）。正中是岸桥和一艘小杂货船，按默认焦点 [0.5, 0.5] 做正方形裁切后船尾被裁掉。
- 修法：先试 `image_focus` 约 [0.15, 0.8]，裁出来船尾仍太小就换图。Flickr 上 hans m. / kees torn 同系列（Berlin / Brussels / Bangkok Mærsk）还有侧前方视角的候选。

**B2 · #13 Berlin Express class（3:34–3:40，两版都有）：卡面是逆光岸桥剪影和天空，船体在底部文字区下面，看不到。**
- 证据：`0217.20_r13_Berlin_Express_class.png`。原图里 Damietta Express 只占画面左下约 1/4，偏暗、逆光。
- 修法：先试 `image_focus` 约 [0.35, 0.9]。原图本身弱，更建议换一张顺光、整船可见的 Hamburg Express 级照片（12 艘姊妹船任选，卡上写船级）。

#### Major

**M1 · 5 张卡看不出主体（满版正方形裁切的问题，两版都有）。** 按影响排序：
- **#1 Pioneering Spirit（冠军，5:14–5:24）**：卡面是起重梁、吊机和黄色导管架，双体船身全被底部文字区挡住，观众看不出这是「世界最大的船」。建议 `image_focus` 下移到约 [0.55, 0.85]；更好是换一张能看出 382 m 双体船身的侧面或航拍。冠军卡是全片高潮，值得单独补搜。
- **#41 Emma Maersk class（片头第一张卡，0:04–0:12）**：卡面是一整墙集装箱，船名和船体在文字区下面。第一张卡就看不出是船，很伤开头留存。换一张整船照（Emma / Estelle / Ebba Mærsk 等姊妹船都可以）。
- **#34 CMA CGM Marco Polo class（0:52–0:58）**：原图是极宽的正侧面，裁成正方形后约 70% 是天空，船只剩文字区上方的一条缝。建议换图，或焦点设 [0.5, 0.75] 后再看效果。
- **#24 Barzan class（2:07–2:13）**：上半张是阴云，烟囱以下被文字区挡住。焦点下移到约 [0.5, 0.8]。
- **#5 Jacques Saadé class（Top 5，4:38–4:44）**：只是绿色船首的特写，右侧是另一艘船 GAS AGILITY 的船名。观众会以为这张卡是 GAS AGILITY，也看不出船有多大。建议换一张整船照，同级 9 艘任选。
- 次一级（可接受，有余力再改）：#35 MSC London、#31 Benjamin Franklin、#7 MSC Irina 主要是岸桥加箱墙；#21 Disney Adventure 默认版替代图是船厂里被吊机挡住的半艘船；#36 Winning 的 AI 图船体偏下、被文字区挡住（handoff 已知）。
- 根因：渲染前的裁切检查（`cropsheet.jpg`）没有拦住这些卡。建议每张卡对照成片里的实际帧，只看一个问题：「不看文字，认得出这是一艘船吗」。

**M2 · 远海丝路（YUAN HAI SI LU，IMO 1052397，180,011 GT）未收，理由站不住。**
- 证据：VesselFinder 详情页（2026-11-04 实查）显示 2026 年建造，**正在航行**，目的港 Ponta da Madeira（淡水河谷在巴西的矿石码头），ETA 11-22，已经是在役船。新华社图片稿（2026-09-02）写明「货舱容积 28 万立方米」，央媒稿称比同尺度传统矿砂船提升 40% 以上。GT 按围蔽容积计算，所以比同尺寸 Guaibamax 高 3.6% 有合理解释，不是异常值。
- 口径不一致：另有 28 个船级同样只有 VesselFinder 一个来源，都收了；只有这一艘因为「单一来源」被拒。
- 修法：按独立船级收进来，排第 31 名（180,011，排在 Berlin Maersk 180,849 之后），运营方是中远海运散运（新华社稿），国家 China。N 变成 42，计分板 China 变成 4。如果坚持不收，至少在描述框写明理由，并准备好回应评论区。

**M3 · 国家口径没在片内交代；Excel 级归德国与口径自相矛盾。**
- 片内唯一的说明是计分板标题「Ship classes by operator country」，描述框写的是「Flags show the country of the operating company」。观众会马上问：
  - Hong Kong 为什么单列？OOCL 的母公司是中远海运；若并入中国，China 变成 6，与 France 并列第二。
  - ONE 是日本三家船公司合资，为什么算 Singapore？
  - Valemax / Guaibamax 按租船人 Vale 算 Brazil，用的是租船人口径，不是运营公司口径。
  - MSC 算瑞士没有问题（总部日内瓦），Allseas 算瑞士也没问题。
- **Excel 级 → Germany 和口径不一致**：卡上 186,364 GT 取自 Costa Toscana，运营方 Costa 是意大利公司。9 艘里 Carnival Cruise Line（美国）3 艘、AIDA 2 艘、Costa 2 艘、P&O 2 艘。按「级内最大船的运营方」应是 Italy，按「最多艘数」应是 United States，按母公司是 Carnival Corp（US/UK）。现在按「首制船」归德国，是第三套规则，而且只用在这一张卡上。
- 修法：
  1. 在计分板揭晓页加一行脚注（≤90 字符），例如「Country = operator's HQ. Hong Kong listed separately; Valemax/Guaibamax counted for Vale (Brazil).」，描述框同样补一句。
  2. 统一 Excel 级规则：改成取值船 Costa Toscana 的运营方（Italy，配 Costa Toscana / Smeralda 照片），或者归母公司 Carnival（United States）。
  3. topic.md 待确认第 4、5 条请用户拍板。

**M4 · 母版静音（bible §5、§7-6）。** 两版都是 `anullsrc` 静音轨。ep11 的 Suno 曲目没出（README：Suno 下载额度到 11/25 才刷新，v2 任务已排队）。发布前必须补配乐（`--music` 重渲，或用 ep04 的 `add_music.py` 补音轨），补完再做响度与片尾淡出检查。本轮没法查响度。

**M5 · 风险版是旧渲染，屏上署名不合格（只在选风险版发布时才算问题）。**
- 风险版 manifest 里的 data.json 哈希（585155…）与现文件（bc70b9…）不同，是 02:27 用旧渲染器、旧数据渲的。
- 证据：`_build/qc/frames/risk/0143.93_r22_Valemax.png`。Valemax 卡**没有「AI IMAGE」角标**，署名写成「Photo: AI-generated illustration」（AI 图前面却写着「Photo:」）。默认版已经有角标，写的是「AI-generated image, not a photo」。
- 6 张许可不明的图，卡上署名是「Photo: Unknown / unknown」（#37、#32、#21、#10），#2 是「Royal Caribbean (via WPTV) / unknown」。发布出去不专业，也不构成署名。
- #10 OOCL Wisdom 风险图裁成正方形后只看到城市和船厂，船在文字区下面；风险版这张反而不如默认版的 AI 图。#36 Winning 风险图是雾蒙蒙的船厂航拍，两艘船都很小。
- 修法：用户签字放行哪几张，就补全那几张的作者和授权；没有真实署名的不放。#10 风险版改用 AI 替代图或调焦点，然后用当前数据和渲染器重渲风险版。

**M6 · 第 41 名可读时间不足（bible §7-5）。** 本期没设 `layout.intro_hold`，片头一结束（5.0 s）就开始滚动。#41 卡整张可见只有约 1 秒，5.5 s 时左缘已经出屏（`0005.50_start_hold_5.5.png`、`0006.00_r41_….png`）。修法：`layout.intro_hold: 2.5`（data_contract 的建议值），总长加 2.5 s，章节时间码随之后移，记得重跑 publish。

#### Minor

- m1 **船级命名**：Hapag-Lloyd 官方和多家媒体（offshore-energy、lngprime）把 2023 年起的 23,660 TEU 系列叫「Hamburg Express class」，卡上写「Berlin Express class」（按首交船命名，说得通，但懂行的人会挑）。可改成「Hamburg Express class」，或副标题加「a.k.a.」。另外 `sources.md` §3、§5 和 topic.md 写的是「Beijing Maersk 级」，卡上和 data.json 是「Berlin Maersk class」；图片文件名是 `30_beijing_maersk.jpg`。内部文档请统一成 Berlin Maersk（维基叫 B-class）。
- m2 **账本笔误**：`assets.json` 里 `32_sphere.jpg` 的 subject_note 写「Sun Princess」，照片船体上的字是 **STAR PRINCESS**（同级姊妹船，可以用），请改 note。
- m3 **涂装和国旗对不上**：#24 Barzan 照片是 UASC 涂装，卡上挂德国旗；#19 MOL Triumph 照片是 MOL 涂装，卡上挂新加坡旗。观众会疑惑。可在 tags 里加「ex-UASC」「now ONE」之类的短标签（≤24 字符），或换成现涂装的照片。
- m4 **封面 `thumbnail.png` 直接公布了 #1–#3**，和「看到最后才知道冠军」的 Vision 冲突。建议改成 #2–#4 加问号，或用船的剪影悬念版。
- m5 **默认版 5 张 AI 图**（#10、#22、#32、#36、#37）都是通用船型，没有涂装，并非该船级的真实外观；卡上有角标，描述框也声明了，合规。#37 Guaibamax 的戏剧化天光一眼就能看出是 AI。可以接受；以后有可商用实拍图就换掉。
- m6 **#25 Triple-E 照片 HDR 处理过重**（橙色高光、颗粒噪点），在全片里显得不协调，可考虑换图。
- m7 publish.md 的 Upload checklist 写「卡上标 Illustration / Render」，实际卡上是「AI IMAGE」和「AI-generated image, not a photo」，措辞请对齐。
- m8 「Excel class」通行叫法是「Excellence class」（维基条目名），建议卡名改成 Excellence class。
- m9 #1 标签「382 m long」与 VesselFinder 的 LOA 477 m 不一致（后者含托管架）。sources 已说明，评论区可能有人问，备好回复即可。

### 认船核对（逐张，含 image_alt）

| # | 上屏图（默认版 / 风险版） | 图中船 | 是否该船级 | 备注 |
|---|---|---|---|---|
| 1 | 01_pioneering_spirit | Pioneering Spirit（船体可见船名、Allseas） | ✓ | 裁切见 M1 |
| 2 | 02_icon_alt / 02_icon | Icon of the Seas（两张都可见船名） | ✓ | |
| 3 | 03_cma_seine | CMA CGM Seine（船尾船名） | ✓ | 船尾正面视角 |
| 4 | 04_ever_a | Ever Ace | ✓ 姊妹船 | |
| 5 | 05_cma_saade | CMA CGM Jacques Saadé | ✓ 姊妹船 | 构图见 M1 |
| 6 | 06_oasis | Symphony of the Seas | ✓ 姊妹船 | |
| 7 | 07_msc_irina | MSC Loreto（船尾可见 IMO 9934735） | ✓ Irina 组 | |
| 8 | 08_oocl_spain | OOCL Spain | ✓ | |
| 9 | 09_one_innovation | ONE Infinity | ✓ | |
| 10 | 10_oocl_wisdom_gen / 10_oocl_wisdom | AI 通用船 / OOCL Wisdom 船厂航拍 | AI 已标 / ✓ | 风险图裁切见 M5 |
| 11 | 11_msc_gulsun | MSC Gülsün | ✓ | |
| 12 | 12_hmm_algeciras | HMM 船（看不到船名，局部） | 按账本 | 只拍到局部，minor |
| 13 | 13_berlin_express | Damietta Express（船尾 HAMBURG） | ✓ 同系列 | 见 B2 |
| 14 | 14_ever_g | Ever Given | ✓ | |
| 15 | 15_cma_antoine | CMA CGM Jean Mermoz | ✓ 姊妹船 | |
| 16 | 16_msc_world | MSC World Europa | ✓ 姊妹船 | |
| 17 | 17_cosco_universe | COSCO Shipping Planet | ✓ 姊妹船 | |
| 18 | 18_madrid_maersk | Madrid Maersk | ✓ | |
| 19 | 19_mol_triumph | MOL Triumph（MOL 涂装） | ✓ | m3 |
| 20 | 20_oocl_hk | OOCL Hong Kong | ✓ | |
| 21 | 21_disney_adventure_alt / 21_disney_adventure | Disney Adventure（Wismar 舾装中 / 抵新加坡） | ✓ | |
| 22 | 22_valemax_gen | AI 通用 VLOC | AI 已标 | |
| 23 | 23_cosco_aries | COSCO Shipping Aries | ✓ | |
| 24 | 24_barzan | Barzan（UASC 涂装） | ✓ | M1、m3 |
| 25 | 25_triple_e | Majestic Maersk | ✓ 姊妹船 | m6 |
| 26 | 26_msc_oscar | MSC Oscar | ✓ | 原图右缘有摄影师署名，裁切后不在画面内 |
| 27 | 27_cscl_globe | CSCL Globe（COSCO 涂装） | ✓ | |
| 28 | 28_excel | AIDAnova | ✓ 姊妹船 | M3 |
| 29 | 29_meraviglia_plus | MSC Grandiosa | ✓ 姊妹船 | |
| 30 | 30_beijing_maersk | Barcelona Mærsk（船尾船名） | ✓ 同系列 | 见 B1 |
| 31 | 31_cma_franklin | CMA CGM Benjamin Franklin | ✓ | |
| 32 | 32_sphere_gen / 32_sphere | AI 通用 / **Star Princess** | AI 已标 / ✓ | m2 |
| 33 | 33_cma_bougainville | CMA CGM Kerguelen | ✓ 姊妹船 | |
| 34 | 34_cma_explorer | CMA CGM Alexander von Humboldt | ✓ 姊妹船 | M1 |
| 35 | 35_msc_london | MSC New York | ✓ 姊妹船 | |
| 36 | 36_winning_gen / 36_winning | AI 通用 / Winning Creation & Devotion（恒力） | AI 已标 / ✓ 同级 | |
| 37 | 37_guaibamax_gen / 37_guaibamax | AI（旋筒帆）/ Sea Zhoushan | AI 已标 / ✓ | |
| 38 | 38_ever_e | Ever Eco | ✓ 姊妹船 | |
| 39 | 39_ane_maersk | Ane Maersk | ✓ | |
| 40 | 40_meraviglia | MSC Bellissima | ✓ 姊妹船 | |
| 41 | 41_emma_maersk | Emma Maersk（船尾） | ✓ | M1 |

没有发现认错船（同名旧船、相邻泊位的别的船当主体）的情况。**默认版**所有实拍图都是 Flickr CC BY / BY-SA / CC0 / PDM，账本的作者和来源页与图对应；没有图库水印。

### 核对过的数据样本（2026-11-04 实查）

| # | 船级 | 查的船（IMO） | 卡上 GT | 实查 | 来源 | 结果 |
|---|---|---|---|---|---|---|
| 1 | Pioneering Spirit | 9593505 | 403,342 | 403,342 | VesselFinder | ✓ |
| 2 | Icon class | 9829930 | 248,663 | 248,663 | VesselFinder；DNV 缓存 `_build/dnv/9829930.json` grossTon69 = 248663 | ✓ |
| 3 | CMA CGM Seine | 9987196 | 237,742 | 237,742 | VesselFinder | ✓ |
| 4 | Ever A（Ever Aeon） | 9943279 | 236,680 | 236,680 | VesselFinder | ✓ |
| 5 | Jacques Saadé（Champs Elysees） | 9839131 | 236,583 | 236,583 | VesselFinder | ✓ |
| 6 | Oasis（Utopia） | 9880001 | 236,473 | 236,473 | VesselFinder | ✓ |
| 7 | MSC Irina | 9929429 | 236,184 | 236,184 | VesselFinder | ✓ |
| 13 | Berlin Express | 9540118 | 229,376 | 229,376 | VesselFinder | ✓ |
| 16 | MSC World（America） | 9837432 | 216,638 | 216,638 | VesselFinder | ✓ |
| 22 | Valemax（Pacific Unity） | 9806976 | 204,014 | 204,014 | VesselFinder | ✓ |
| 28 | Excel（Costa Toscana） | 9781891 | 186,364 | 186,364 | VesselFinder | ✓ |
| 30 | Berlin Maersk | 9984560 | 180,849 | 180,849 | VesselFinder；gCaptain：6 艘 17,480 TEU、HHI | ✓ |
| 32 | Sphere（Sun Princess） | 9863118 | 177,882 | 177,882 | VesselFinder | ✓ |
| 41 | Emma Maersk | 9321483 | 171,542 | 171,542 | VesselFinder | ✓ |
| 下限 | ORIENTAL ARK（原油轮） | 9424209 | 170,618 | 170,618，Crude Oil Tanker，在营（锚泊塞得港） | VesselFinder | ✓ |
| 未收 | YUAN HAI SI LU | 1052397 | — | 180,011，2026 年建，在航，去 Ponta da Madeira | VesselFinder；新华社 2026-09-02（舱容 28 万 m³，运营方中远海运散运） | 见 M2 |

另外核对了：
- 名次 1–41 连续，value 严格递减，无并列。
- 计分板 CH 8 / FR 6 / DK 5 / US 4 / TW·HK·SG·DE·CN 各 3 / BR 2 / KR 1，合计 41，与 data.json 逐条一致。成片揭晓页和角落计分板的累计都正确（抽了 20 多帧）。
- 洞察卡：6 张都能在 sources §5 找到依据。「6 个船级 2025 年后才有」与 NEW 2025 / NEW 2026 徽章数一致。「3 个集装箱船级排在 Irina 之上」是 #3、#4、#5，正确。「62%」= 403,342 ÷ 248,663 = 1.622，正确。「Next: Ever Given」紧接 #14，正确。
- MSC Irina 24,346 TEU 仍是最大箱量：多家 2026 年的行业综述一致。
- DNV 网页是 JS 应用，WebFetch 读不到，只核对了制作方本地缓存的 JSON（Icon）。

### 成片技术核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 分辨率 / 帧率 | 1920×1080 / 60 fps，H.264 yuv420p | 同左 |
| 时长 / 帧数 | 353.217 s / 21,193 帧 = manifest 时间线 21,193 帧 ✓ | 同左 ✓ |
| 全片解码 | 0 错误（`_build/qc/decode2_master.log`） | 0 错误（`decode2_master_with-risk-images.log`） |
| 卡帧检测 | 只有 335.6 s 起的片尾静帧（预期内）；滚动段 ≥10 s 无冻结 | 同左 |
| 音轨 | AAC 静音（anullsrc）→ M4 | 同左 |
| 输入一致 | manifest 的 data.json / assets.json 哈希 = 现文件 ✓ | 旧哈希，渲染器版本也旧 → M5 |

`python -m rank_scroll validate --strict` 两版都是 OK；timeline 5:53.22。描述框章节 0:00 / 1:22 / 2:43 / 3:58 / 5:14 / 5:25 与卡片出场时间吻合。改 M6 后要重新生成。

### 包装（publish.md）

- 标题「Biggest Ships in the World 2026 | Top 41 by Gross Tonnage」57 字符 ✓。
- 描述：口径说明、来源、41 条署名（CC 许可都附链接）、AI 图声明（5 张）✓。缺国家口径细则（M3），远海丝路要有一句交代（M2）。
- 风险版文案 `_build/publish_with-risk-images.md` 里有 unknown 作者（M5）。
- 时长 5.9 分钟，不到 8 分钟，不能插中插广告；这是口径决定的 N=41，可以接受。

### 观众视角

- 好看的点：冠军是一艘起重船，不是油轮或航母，比 Icon of the Seas 大 62%；「GT 是容积不是重量」；内陆国瑞士拿计分板第一；Ever Given 的同级船。这几处都是可以拿去争论的好钩子。
- 会划走的地方：片头第一张卡是一墙集装箱（M1），#41–#30 之间连续好几张岸桥和箱墙，#30、#34 甚至看不到船。集装箱船占 29/41，外观本来就像，裁坏的图会放大单调感。建议优先修 B1、B2、M1，让每张卡至少有一个完整的船首或船尾轮廓。
- 评论区会争的地方：「Hong Kong 不是国家」「ONE 是日本公司」「Prelude 呢？Seawise Giant 呢？航母呢？」。前两个靠 M3 的脚注，后几个口径行和描述框已经覆盖。

### 抽帧清单（`_build/qc/frames/`）

- 默认版 66 帧（`frames/master/`）：
  - 片头 1.0 / 4.9 / 5.5 s；
  - 41 张卡居中时刻各 1 帧，从 #41 到 #1（时刻见 `_build/qc/card_times.json`）；
  - 6 张洞察卡（27.73 / 88.87 / 150.00 / 204.13 / 267.27 / 309.90 s）；
  - 冠军 318.22 / 321.0 / 324.1 s；
  - 计分板 326.0 / 326.63 / 330.9 s；
  - 来源卡 333.0 s；
  - 片尾 340.0 / 352.9 / 353.2 s；
  - 随机 8 帧（69.26 / 162.43 / 167.05 / 181.73 / 183.14 / 199.8 / 209.41 / 326.63 s）。
- 风险版 10 帧（`frames/risk/`）：#37、#36、#32、#22、#21、#10、#2，片头、计分板、片尾。
- 拼图：`_build/qc/fsheet_m_01–17.jpg`（默认版）、`fsheet_r_01–03.jpg`（风险版）、`img_sheet_01–08.jpg`（47 张素材原图）。脚本：`qc_sheet.py`、`card_times.py`、`extract.py`、`tile_frames.py`。

### 修完后复核要点

1. 改 B1、B2、M1 的焦点或换图后，用 `cropsheet.py` 和成片帧逐张确认「认得出船」。
2. M2、M3 改了数据就重跑 `build.py` → `gen_sources.py` → publish，计分板与洞察卡 1（「just below No. 41」，N 变化后要核）一起复核。
3. 设 `intro_hold`，加配乐，重渲默认版。如果用户签字放行风险版，用当前渲染器、补全署名后重渲。
4. 重渲后交另一轮独立审片，重点看 B1、B2、M1 的帧和音频响度、片尾淡出。
