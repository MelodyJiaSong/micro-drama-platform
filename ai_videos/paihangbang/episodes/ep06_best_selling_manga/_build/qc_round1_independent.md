# ep06 · 独立审片 第 1 轮（fresh context）

- 审片对象：`render/ep06_best_selling_manga_master_with-risk-images.mp4`（1920×1080，60 fps，214.97 s，静音）；manifest 中 `data.json` / `assets.json` 的 sha256 与当前文件一致，确认审的是当前产物。
- 输入：`data.json`、`sources.md`、`topic.md`、`assets.json`、`publish.md`、`_build/research/group_{a,b,c}.json`、`_build/raw/wp_best_selling_manga_2026-11-03.json`；系列规则 `bible.md` §2.4、§3、§7。
- 方法：用 ffmpeg 每 2 s 抽一帧（107 帧），片头和冠军段另按 0.5 s / 1 s 抽帧拼图；30 张卡逐张在完整入画的帧上核对；挑 4 张图做 1:1 局部放大，检查清晰度；联网核对了 JJK、Demon Slayer、HxH、FMA、Kingdom、Conan、Ippo、Crayon Shin-chan 的公开数字。Oricon、Wikipedia、web.archive 的页面 WebFetch 抓不到，相关核对只能靠搜索摘要和研究 JSON 里的原文引用。
- 抽帧目录：`C:\Users\light\AppData\Local\Temp\claude\6a0e85057da57c29\1b890543-b139-4145-b77c-3dd7b6a1aa40\scratchpad\qc_frames\`（`tNNN.jpg` ≈ 第 (NNN−1)×2 秒；另有 `intro_tile.jpg`、`champ_tile.jpg`、`sharp_check.png`、`src_sheet.jpg`）。
- 未审：音乐（不在范围）；滚动是否闪烁（静帧无法判断，实测约 119 px/s ≈ 1.98 px/帧，接近但未确认是整数步进）。

## 结论：**小修后可发布**（当前这一版不可发布）

数据骨架扎实：30 个数值都能在 `sources.md` 和研究 JSON 里找到原文；名次连续，并列处理正确；30 张封面都是对应作品；计分板计数正确。不过屏上有一处硬伤（JJK「一年」）和两条站不住的洞察。「as of 年份」的标法前后不一。片头来源行与实际来源不符。#30 几乎没有可读时间。#2、#4 两张封面模糊。这些都只需改 data.json / 换图 / 调渲染参数后重渲，不必重做调研。另有两项闸门要用户拍板：版权封面（§7-4）和旧数字例外（§3.3）。

## 发现清单

| # | 严重度 | 时间 / 名次 | 问题 | 证据 | 建议修改 |
|---|---|---|---|---|---|
| 1 | **blocker** | 洞察卡（after #11，约 1:48–1:56）＋ #10 JJK 徽章（约 1:52–2:05） | 「Jujutsu Kaisen added 50 million copies **in a single year** after its 2024 finale」和徽章「+50M IN ONE YEAR」都与出处不符。1 亿部是 2024-09 完结时，1.5 亿部是 2025-12-20，实际用了 **1 年 3 个月**。研究 JSON 原文就是「1年3ヶ月で5000万部増加」，one_line_fact 也写的是「in the 15 months」。`sources.md` §3 却写成「1年で+5000万部」「2024-12 为 1 亿」，转述有误 | t054、t057、t060；group_a.json Jujutsu Kaisen `notes`、`one_line_fact`；联网搜索结果同为 2024-09 → 2025-12 | 洞察改为「…added 50 million copies in the 15 months after its 2024 finale.」；徽章改为「+50M IN 15 MONTHS」；同时改正 `sources.md` §3 |
| 2 | major | 洞察卡（after #8，约 2:10–2:20） | 「Demon Slayer ended in 2020 with 23 volumes, then sold 70M more in 4.5 years」口径错配。「4 年半 +7000 万」是拿 2021-02 的 1.5 亿和 2025-07 的 2.2 亿相减：前者按集英社当时的推移是国内数（含电子），后者是全世界（国内 1.64 亿 + 海外 0.56 亿）。国内实际只增约 1400 万，增量大部分来自把海外版计入。另外「ended in 2020, then…」的起点也不对：2020-12 完结时是 1.2 亿，不是 1.5 亿 | t066、t069；group_a Demon Slayer `value_text_original`；搜索：集英社推移「2020-12-04 1億2000万部 → 2021-02-15 1億5000万部」 | 换成稳妥的算术事实，如「Demon Slayer reached 220M with only 23 volumes — about 9.6M copies per volume.」；或明确写「worldwide total incl. 56M overseas」 |
| 3 | major | 洞察卡（after #28，0:05–0:17）＋剔除 Crayon Shin-chan | 「only about 58M of that is the manga」过度推断。依据是 2015 年万代页面的明细：漫画 5500 万 + 新作 300 万；另有「海外関連書籍 7000 万」。「海外关联书籍」很可能包含海外翻译版漫画（该作在华语圈和韩国销量很大），研究笔记也没核实。而其他作品（One Piece、鬼灭、MHA 等）的主值都含海外版。如果这 7000 万里有翻译漫画，Crayon Shin-chan 应在榜内，约第 13 名。剔除决定和洞察卡文字都建立在这个未核实的解读上，懂行的观众很可能来挑这条 | t004、t006、t009；group_a Crayon Shin-chan `notes`；联网未能取到原页 | 洞察卡改为可证的说法：「Crayon Shin-chan's often-quoted 148M also counts picture books and other related books, so it is left out.」。剔除理由也改成「数字含非漫画书籍、无法拆分出可比的漫画口径」，不要断言「漫画只有 58M」。如能取到原页确认 7000 万不含翻译漫画，可恢复原句 |
| 4 | major | 全片 30 张卡的「as of 年份」 | 同一个标签含义不一。Sangokushi 标 2026（数字自 2020 年起没变过，2026 年只是复述），Captain Tsubasa 标 2026（2023 年首报），Fist of the North Star 标 2025（里程碑约在 2019 年）。另一边，Touch 标 2004（2025 年也有复述），Golgo 13 标 2022（2025、2026 都有复述），Naruto 标 2023（2026 年有复述），Bleach 标 2022（2025 年有复述）。观众会以为前者是新数字 | t003、t018、t036、t024、t081；data.json 各条 `notes` | 统一一条规则。建议「as of」= 该数字首次被公布的年份：Sangokushi 改约 2020，Captain Tsubasa 改 2023，Fist of the North Star 改约 2019（或注明「restated」）；其余按同一规则逐条复核 |
| 5 | major（待用户决定） | 全片 | 21/30 的主值超过 bible §3.3 的 18 个月：17 条名义上过期，另有 #4 所列 3 条实际也是旧数字；最旧的是 1999、2004、2012、2014 年。「旧值是下限」逻辑成立，但旧值之间、旧值与新值之间的相对名次未必真实，比如 Vagabond 82M（2012）与 Kinnikuman 85M（2025）。topic.md 标明此例外「待用户点头」，目前没有确认记录。片头「Latest official figures · Nov 2026」也容易让人以为全是 2026 年的数字 | t002 片头；`topic.md`、`sources.md` §2-4 | 请用户明确批准例外，并记录到 `sources.md`。片头统计行改为「Latest announced figure per series (year shown on each card)」 |
| 6 | major | 片头 0:00–0:04、底栏全程、来源卡 3:13 | 来源行「Sources: publisher announcements, Oricon, Natalie, Mantan Web, ANN」与实际不符：30 条主值里 **Natalie 一条都没有**（全部 403 未取到），ANN 只有 1 条；Wikipedia 作主值依据的有 3 条（Sazae-san 引日文 Wikipedia，Vagabond 引 Wikipedia 引用的已失效 PDF），还用了 Chunichi、AFP、Anime!Anime、Kyodo、作者本人 X 等。bible §3.2 规定 aggregator 作主值时屏上要写「据 X 整理」 | t002、t098；data.json `source.name` 统计 | 改为「Sources: publisher announcements & Japanese media (Oricon, Mantan Web, Anime!Anime, Kyodo…), see description」，去掉 Natalie。Sazae-san、Vagabond 卡的数值旁加「est.」或「via Wikipedia」 |
| 7 | major | #30 Haikyu!!（0:04–0:06） | 第一张卡在 4.0–4.5 s 原地淡入后马上开始左移，名称和数值约 1 秒后就被左边缘切掉（6 s 时只剩「!」）。可读时间远低于 §7-5 要求的 3 秒，其余卡约 11 秒 | `intro_tile.jpg`、t003、t004 | 让第一组卡从右侧滚入（与 §2.3 一致），或片头后整排静止 2–3 s 再开始滚动 |
| 8 | major | #4 Detective Conan（2:30–2:45） | 封面明显糊、有 JPEG 块：「名探偵コナン」字样锯齿，柯南脸部发软。来源为 Kobo 小图，放大存成 1527×2400，实际细节远不够；它在 top 10 放大卡上停留约 11 秒 | t078、t081、`sharp_check.png` 第 1 幅 | 换高分辨率第 1 卷封面（小学馆官方、Google Play 原图或少年 Sunday 官方 X） |
| 9 | major | #2 Golgo 13（2:34–2:52） | 两个问题：① 图片偏糊（226 KB，Kobo 1200 px 级）；② 裁切后，可辨识的竖排「ゴルゴ13」大字只剩右半边的抽象红色楼宇块，主角 Duke Togo 缩在右下角，外国观众认不出这是 Golgo 13 | t081、t084、`sharp_check.png` 第 2 幅、`src_sheet.jpg` 第 1 幅 | 换更清晰的封面；或按图设 `image_focus` 把焦点偏左，保住标题字；也可换用官方主视觉（Duke Togo 半身） |
| 10 | minor | #12 Oishinbo（1:38–1:50） | 封面是**第 2 卷**（图上标「② 幻の魚」），不是第 1 卷，且偏糊。作品本身没错 | t051、`src_sheet.jpg` 第 5 幅 | 有清晰的第 1 卷就换掉；否则在 assets.json 注明卷号（topic.md 的「25 张第 1 卷」也应复核） |
| 11 | minor | #16 Fist of the North Star（1:07–1:22） | 卡上出版社写 Shueisha、署名「© Buronson & Tetsuo Hara / Shueisha」，但封面是 VIZ 英文版，publish.md 署名写的又是 VIZ Media，前后不一致；现行版权方为 Coamix。集英社 2026-07 称 HxH 是本社「第 12 部」破亿作品，与本片 16 部集英社作品中破亿的 13 部（含北斗）对不上，说明集英社自己不把北斗算作本社作品。计分板的 Shueisha 16 因此可能被挑刺 | t036、t039；publish.md Comment 1；搜索结果（sakigake 2026-07-03） | 署名改为「© Buronson & Tetsuo Hara / Coamix」；出版社行写「Shueisha (orig.)」，或在 sources.md 注明计分口径为「原单行本出版社」 |
| 12 | minor | #16 Hunter × Hunter 徽章 | 「NEW: 100M IN JUNE 2026」：6-29 是公布日，突破是在 7-3 第 39 卷发售时（「7月3日発売の最新39巻で1億部を突破」） | t030；data.json 原文引用 | 改为「NEW: 100M IN JULY 2026」或「NEW: 100M IN 2026」 |
| 13 | minor | #23 Fullmetal Alchemist 徽章 | 「NEW: 90M IN JULY 2026」：依据是 2026-07-10 的 X 帖子，日文 Wikipedia 记为 2026 年 4 月，首达日期未确认 | t018、t021；data.json `notes` | 改为「NEW: 90M IN 2026」 |
| 14 | minor | #2 Golgo 13 徽章、#16 Hajime no Ippo 徽章 | 「RECORD 221 VOLUMES」「145 VOLUMES SO FAR」是截至 2026 年年中的卷数。Golgo 13 约一年 4 卷，到 11 月很可能已出 222；Ippo 的 146 卷原预计 2026 年 5–6 月出版，本次未能确认是否已出 | t081、t036；data.json `notes`；联网查到的最新为 145 卷（2026-01-16） | 发布前复核；或改为「220+ VOLUMES · GUINNESS RECORD」「145+ VOLUMES」 |
| 15 | minor | #25 Sazae-san、#27 Vagabond、#28 Tokyo Revengers、#26 Kinnikuman、#8 Slam Dunk | 出处偏弱：Sazae-san 是日文 Wikipedia 引两本旧书的加总；Vagabond 唯一出处是失效链接；Tokyo Revengers 只看到搜索摘要（页面 403）；Kinnikuman 是作者本人 X 帖，ABEMA 同日仍写 7700 万；Slam Dunk 的交叉核对是循环引用 | data.json `source` / `notes` | 保留可以，但卡上或描述中标注（见 #6）。Vagabond 可按 notes 的备选降为「80M+」并引 Japan Times |
| 16 | minor | 洞察卡（after #2，2:52–3:05） | 「twice as many copies as any other manga」：Doraemon 是「3 億部超」，比值 ≤ 2，严格说不一定满 2 倍 | t084、t087 | 改为「about twice as many」 |
| 17 | minor | #23 Captain Tsubasa | 口径冲突：有报道称国内 9000 万，也有称全世界 9000 万（AFP 2024 年报的是国内 7000 万 + 海外 1000 万）；没有集英社一手来源 | data.json `notes` | 卡上不改，在 sources.md 写明取舍；年份按 #4 处理 |
| 18 | minor | 版面 | #23 Captain Tsubasa 的「#23」药丸压住 logo 的「CAPTAIN」；#12 Oishinbo 的徽章和名次压住「美味しんぼ」logo；#8 Slam Dunk、#6 Naruto 的作品名白字叠在封面红色 logo 上，层次略乱。都不影响阅读 | t021、t051、t063、t072 | 可选：按图调 `image_focus` |
| 19 | minor | 计分板 3:06–3:13 | 每个出版社前都画着地球仪图标，那是国旗位的占位，没有信息量 | t096 | 去掉图标，或换书本图标 |
| 20 | minor | 来源卡 3:13 | 「Photo credits」不准确，内容是封面插画 | t098 | 改为「Cover art credits」 |
| 21 | minor | publish.md（§7-7） | ① 章节「0:00 Intro & #30–#21」：本榜没有 #21，实际是 #30–#23；#16 的章节点写 0:50，但 #16 Touch 约 0:44 已完整入画。② 描述称「Every number on screen is sourced and cross-checked」，与 #15 所列弱出处矛盾。③ 置顶的来源评论里留有内部笔记，如「dead link, 404 on 2026-11-03」「text seen via search snippet; page returned 403 to fetch」，不宜公开。④「shown at reduced size」与满版封面的实际呈现不符，是版权说法上的风险 | publish.md | 修正章节文字与时间点；删掉「cross-checked」的绝对化说法；清理评论里的内部备注；版权措辞交用户定 |
| 22 | **blocker（待用户决定）** | 全片 30 张封面（§7-4） | 30 张全是版权封面，`licence: unknown`，不满足「许可是允许的类型」。topic 已说明以带图版为主片、由用户决定，目前没有用户放行记录 | assets.json；topic.md「风险 1」 | 用户明确决定后，按 `qc.py override` 或项目流程记录 |
| 23 | minor | 时长 | 3:35，低于 bible §2.1 的 5–8 分钟目标（Top 30 允许，但不满 8 分钟，不能插中插广告） | manifest | 仅提示；如需拉长可加洞察卡（topic 里有备选） |

## 逐卡核对（30/30）

所有卡的名次、作品名、出版社行、数值、「as of」年份、作者和年份标签、署名，与 data.json 逐字一致。未发现文字出框或互相遮挡。作品名（约 44 px 粗体）和数值（约 80 px）在手机全屏下 3 秒内看得清；#30 例外（见 #7）。

| 名次 | 作品 | 封面是否正确 | 清晰度 / 裁切 | 备注 |
|---|---|---|---|---|
| 1 | One Piece | ✔ 第 1 卷 | 好 | 冠军段正常 |
| 2 | Golgo 13 | ✔ 第 1 卷（SP Comics） | **糊、标题被裁** | #9、#14 |
| 2 | Doraemon | ✔ 第 1 卷 | 略软，可接受 | |
| 4 | Detective Conan | ✔ 第 1 卷 | **糊** | #8 |
| 5 | Dragon Ball | ✔ | 好 | |
| 6 | Naruto | ✔ | 好 | |
| 7 | Demon Slayer | ✔ | 好 | 洞察卡见 #2 |
| 8 | Slam Dunk | ✔ 新装再编版 #1 | 好 | |
| 9 | KochiKame | ✔ 第 200 卷 | 好 | 157M 是 2014 年日本国内数，as of 2014 已标 |
| 10 | Jujutsu Kaisen | ✔ | 好 | 徽章错误，见 #1 |
| 11 | Attack on Titan | ✔ | 好 | |
| 12 | Oishinbo | ✔ 作品对（第 2 卷） | 偏软 | #10 |
| 13 | Bleach | ✔ | 好 | |
| 14 | JoJo | ✔ | 好 | |
| 14 | Kingdom | ✔ 第 71 卷 | 好 | |
| 16 | Baki | ✔ 英文版 Baki the Grappler 1 | 好 | 图源是博客转链的 Amazon 图，出处偏弱 |
| 16 | Fist of the North Star | ✔ VIZ 英文版 1 | 好 | #11 |
| 16 | Hajime no Ippo | ✔ | 好 | #14 |
| 16 | Hunter × Hunter | ✔ | 好 | #12 |
| 16 | My Hero Academia | ✔ | 好 | |
| 16 | Kindaichi | ✔ 原系列第 1 卷 | 好 | |
| 16 | Touch | ✔ | 好 | as of 2004 |
| 23 | Captain Tsubasa | ✔ 小学生编电子版 1 | 好 | #4、#17、#18 |
| 23 | Fullmetal Alchemist | ✔ | 好 | #13 |
| 25 | Sazae-san | ✔ | 好 | 出处弱，见 #15 |
| 26 | Kinnikuman | ✔ | 好 | |
| 27 | Vagabond | ✔ | 好 | 出处已失效 |
| 28 | Sangokushi | ✔ | 好 | 年份错标，见 #4 |
| 28 | Tokyo Revengers | ✔ | 好 | |
| 30 | Haikyu!! | ✔ | 好 | 可读时间不足，见 #7 |

## 其余段落

- **片头（0–4 s）**：标题、kicker、统计行、来源行都看得清；来源行内容有误（#6），统计行有误导（#5）。
- **洞察卡 5 张**：「seven series tied at the 100-million mark」正确（#16 并列 7 部）；JJK 错（#1）；Demon Slayer 误导（#2）；Crayon Shin-chan 过度推断（#3）；One Piece 基本成立（#16）。
- **冠军段（2:56–3:06）**：One Piece 卡居中，右侧是 No. 1 / 600M / as of 2026，版面正常。
- **计分板（3:06–3:13）**：Shueisha 16、Kodansha 5、Shogakukan 4、Leed / Akita / Square Enix / Shimaisha / Ushio 各 1，合计 30，与 data.json 一致。滚动中右上角的实时计数也逐步正确累加。口径争议见 #11。
- **来源卡（3:13–3:17）**、**片尾（3:17–3:35）**：片尾留出 YouTube 片尾元素的空位，正常。来源卡见 #6、#20。

## 榜单事实核查（抽查 ≥ 10 条）

| 作品 | 屏上值 | 研究 JSON / 出处原文 | 核对结果 |
|---|---|---|---|
| One Piece | 600M · 2026 | 「全世界の累計発行部数が6億部を突破」（Oricon 2026-03-04，ANN 同） | ✔ |
| Doraemon | 300M · 2024 | 「全世界で３億部超」（小学馆广告 PDF） | ✔（「超」，见 #16） |
| Golgo 13 | 300M · 2022 | 「シリーズ累計3億冊超」（ANN 引小学馆） | ✔（系列合计，含全部形式） |
| Detective Conan | 270M · 2023 | 「全世界で累計2億7000万部を突破」（中日新闻） | ✔；搜索未见 2.8 亿 |
| Dragon Ball | 260M · 2024 | AFP 引集英社「more than 260 million」 | ✔ |
| Demon Slayer | 220M · 2025 | 「2億2000万部（国内１億6400万部・海外5600万部／デジタル版含む）」 | 数值 ✔；洞察 ✘（#2） |
| Jujutsu Kaisen | 150M · 2025 | 「1億5000万部を突破…（デジタル版含む）」，「1年3ヶ月で5000万部増加」 | 数值 ✔；「一年」✘（#1） |
| Kingdom | 120M · 2026 | 「累計発行部数1億2000万部（電子版含む）を突破」 | ✔；搜索未见 1.3 亿 |
| Hunter × Hunter | 100M · 2026 | 「7月3日発売の最新39巻で1億部を突破」 | 数值 ✔；徽章月份见 #12 |
| Fullmetal Alchemist | 90M · 2026 | 月刊少年ガンガン X「全世界シリーズ 累計9000万部突破!!」 | ✔（搜索只查到 8000 万，但官方帖子更新） |
| Kinnikuman | 85M · 2025 | 作者 X「8500万部突破」 | ✔（非出版社发布，见 #15） |
| Haikyu!! | 75M · 2025 | 「電子版を含むコミックスの累計発行部数は7500万部以上」 | ✔ |
| KochiKame | 157M · 2014 | 集英社媒体资料「1億5720万部」（2014 年 2 月，日本国内销售） | ✔ |

**Top 30 是否有遗漏**：对照 Wikipedia 基线，以及研究里列出的 70M 上下作品（Gintama 73M、Fairy Tail 72M、Rurouni Kenshin 72M、Berserk 70M、Blue Lock 65M 等），榜尾门槛 75M 设置合理。没有发现有官方数字却漏掉的作品。Black Jack 的「1 亿」在 Wikipedia 上已注明 NHK 称无官方统计，官方可考约 4766 万，不进榜也合理。

**剔除判断**：
- Astro Boy：剔除合理（1981 年「関連書籍」累计，含绘本，没有出版社数字）。
- Major：剔除对榜单没有影响（55M 和 Wikipedia 的 66.66M 都低于 75M）。
- Crayon Shin-chan：剔除理由不稳，见 #3，是评论区最可能被挑的一点。

**旧数字作为下限**：逻辑成立，但需要用户批准，并统一「as of」规则（#4、#5）。

## §7 清单

1. 名次连续、无重复，排序与 data.json 一致：**通过**。
2. 数值可追到 sources.md，统计期与片头一致：**部分不通过**。数值都能追到；统计期与片头「Nov 2026」不一致，as-of 规则不统一（#4、#5）；片头来源行不符（#6）。
3. 国旗与国家：本期不显示国旗，改用出版社行，口径已在 topic.md 定好：**通过**（北斗口径见 #11）。
4. 图片都在 assets.json 里且许可允许：**不通过（待用户决定）**（#22）。
5. 文字不出框，手机全屏 3 秒内看得清：**基本通过**。#30 例外（#7）；闪烁未能验证。
7. 描述框来源与署名完整：**基本通过**，但有章节、措辞和内部备注问题（#21）。

## 总结

结论：**小修后可发布**。改动集中在 data.json 文案、两张封面和片头时序，重渲一次即可。最需要先改的三件事：

1. **JJK「一年 +5000 万」与出处不符**（实为 1 年 3 个月），洞察卡和徽章两处都要改。
2. **鬼灭「4.5 年 +7000 万」和蜡笔小新「漫画只有 5800 万」两条洞察站不住**：前者是国内数和全球数相减，后者是对「海外关联书籍」的未核实解读，而这个解读同时决定了蜡笔小新是否被剔除。
3. **「as of 年份」规则不统一，片头来源行不实**：Sangokushi、Captain Tsubasa、北斗把旧数字标成新年份，Natalie 一条主值都没提供。

其次要改的是 #30 Haikyu!! 只有约 1 秒可读，以及 #4 Conan、#2 Golgo 13 封面模糊且 Golgo 标题被裁。

需要用户拍板的两项闸门：版权封面带图版是否发布（§7-4），以及 21/30 条超过 18 个月的旧数字例外（§3.3）。
