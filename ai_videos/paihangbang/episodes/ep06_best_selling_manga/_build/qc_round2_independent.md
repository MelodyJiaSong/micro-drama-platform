# ep06 · 独立审片 第 2 轮（fresh context）

- 审片对象：`render/ep06_best_selling_manga_master_with-risk-images.mp4`（1920×1080，60 fps，217.47 s，静音）。manifest 记录的 `data.json`、`assets.json`、30 张封面和成片的 sha256 与当前文件逐一一致，确认审的是当前产物。默认版 `render/ep06_best_selling_manga_master.mp4` 只做抽查。
- 输入：`data.json`、`sources.md`、`topic.md`、`publish.md`、`assets.json`、`_build/research/group_a.json`（Crayon Shin-chan 明细）、`_build/06_qc_fixes.py`、`_build/07_publish_fix.py`、`render/thumbnail.png`；系列规则 `bible.md` §2.1–2.3、§3.2–3.3、§7。
- 方法：
  - 滚动段每 5 s 抽一帧全分辨率（36 帧），30 张卡和 5 张洞察卡都在完整入画的帧上逐张核对。
  - 片头 0–12 s 每 0.5 s 抽一帧；Haikyu!! 的进场（3.0–5.4 s）和出画（7.0–9.4 s）每 0.2 s 抽一帧。
  - 冠军、计分板、来源卡、片尾各抽帧。
  - 新换的 3 张封面在成片里 1:1 裁图看清晰度，并与原图对照。
  - 用相邻帧像素互相关测滚动步进。
  - 默认版抽 5 帧，另看了缩略图。
- 抽帧目录：`C:\Users\light\AppData\Local\Temp\claude\6a0e85057da57c29\1b890543-b139-4145-b77c-3dd7b6a1aa40\scratchpad\qc2_frames\`
  - `grid_*.jpg`：滚动段 2×2 拼图
  - `intro_tile.jpg`、`intro_3to5.jpg`、`haikyu_exit.jpg`：片头和 #30
  - `sharp3.png`、`oishinbo_crop.png`、`new_covers.jpg`：新封面
  - `gridX1/2.jpg`：冠军、计分板、来源卡、片尾
  - `gridD.jpg`、`dsrc_thumb.jpg`：默认版和缩略图
- 未审：音乐（不在范围）。本轮没有联网复核数字，事实核对以研究 JSON 和 `sources.md` 的原文引用为准。

## 结论：**小修后可发布**

成片画面本身已基本达标：
- 第 1 轮指出的屏上硬伤都已改掉：JJK「一年」、鬼灭和蜡笔小新两条洞察、as-of 规则、片头来源行、#30 可读时间、Conan 和 Golgo 13 封面模糊。
- 30 张卡逐张核对无误，计分板计数正确，滚动是整数 2 px/帧。

但发布物料里有 3 处新问题，都不用重渲视频：
1. `publish.md` 的标题末尾多了「(card)」（N1）。
2. `thumbnail.png` 是修改前的旧图，仍写着已被改掉的「Latest official figures · Nov 2026」，用的也是旧的 Golgo 13 封面（N2）。
3. 默认版的来源卡说「Image credits: shown on each card」，与画面不符（N3）。

此外，两项闸门仍须用户拍板：版权封面（§7-4）和 18 个月旧数字例外（§3.3）。

## 第 1 轮发现复核

| # | 第 1 轮问题 | 状态 | 本轮证据 |
|---|---|---|---|
| 1 | JJK「一年 +5000 万」 | **已修** | 洞察卡（约 1:52–2:00）为「…added 50 million copies in the 15 months after its 2024 finale.」；徽章为「+50M IN 15 MONTHS」（s120、s125）；`sources.md` §3 已改为 2024-09 → 2025-12-20、「1年3ヶ月」 |
| 2 | 鬼灭「4.5 年 +7000 万」口径错配 | **已修** | 改为「Demon Slayer has just 23 volumes: about 9.6M copies each, the most per volume here.」。复算 220M/23 ≈ 9.57M。其他作品都更低：Doraemon 按 45 卷约 6.7M，Dragon Ball 约 6.2M，Slam Dunk 约 6.0M，One Piece 约 5.2M，「the most per volume here」成立 |
| 3 | 蜡笔小新「漫画只有 58M」过度推断 | **已修（措辞）** | 改为「…148M is left out: it also counts ~20M non-manga books.」，与万代 2015 明细（国内关联书籍约 2000 万）一致，不再断言海外 7000 万的性质。剔除决定本身仍待用户确认（`sources.md` §2-1 已写明） |
| 4 | as-of 年份规则不一 | **基本已修** | 规则统一为「数字首次公布的年份」。Sangokushi 2020、Captain Tsubasa 2023、北斗 2019、Golgo 13 2021，屏上与 data.json `figure_year` 30/30 一致。个别仍与自家 notes 不一致，见 N5 |
| 5 | 21/30 超过 18 个月（§3.3 例外） | **未修（待用户）** | 片头统计行已改为「Latest announced figure · year on each card」，误导问题已解决；例外本身仍无用户批准记录 |
| 6 | 片头 / 底栏 / 来源卡的来源行不实 | **部分** | 三处统一为「Sources: publishers, Oricon, Mantan Web, ANN, other media, Wikipedia」，去掉了 Natalie、加上了 Wikipedia ✔。但 Sazae-san（主源是日文 Wikipedia）和 Vagabond（Wikipedia 引用的失效 PDF）卡上仍没有「via Wikipedia」或「est.」，与 bible §3.2「aggregator 作主值时屏上写据 X 整理」不完全一致（见第 15 条） |
| 7 | #30 Haikyu!! 可读时间不足 | **已修** | 卡片约 3.6–4.6 s 从右侧快速滑入，约 4.7 s 停稳（x≈40 px），静止到约 7.5 s 后开始滚动，约 8.0 s 左缘出画。完整可读约 **3.3 s**（≥ 3 s，余量不大），名称到约 8.4 s 仍可辨认 |
| 8 | #4 Conan 封面糊 | **已修** | 换成 Google Play 第 1 卷（1528×2400）。成片 1:1 裁图看，标题砖纹和柯南线条都清楚，作品正确，裁切保住了「名探偵コナン」logo |
| 9 | #2 Golgo 13 封面糊、标题被裁 | **已修** | 换成 SP Comics 第 206 卷（1440×2048）。画面清晰，Duke Togo 半身和竖排「ゴルゴ」大字都在画内，卷号「206」被裁掉（不会造成误解）。小瑕疵：徽章「RECORD: 220+ VOLUMES」压住封面上的作者名「さいとう・たかを」，不影响识别 |
| 10 | #12 Oishinbo 是第 2 卷 | **已修** | 换成第 1 卷「豆腐と水」（Google Play，1701×2400），画面清晰。顶部 logo 仍被徽章和名次压住，属第 18 条旧问题 |
| 11 | 北斗出版社 / 署名口径 | **部分** | 卡上署名改为「© Buronson & Tetsuo Hara / Coamix · English ed.」，Baki 也标了「English ed.」✔。但出版社行和计分板仍记 Shueisha，`sources.md` 没写「按原单行本出版社计分」的口径（§2-6 只说明了 Golgo）。`publish.md` 署名仍为「Buronson / Tetsuo Hara / VIZ Media」，与屏上的 Coamix 不一致 |
| 12 | HxH 徽章月份 | **已修** | 「NEW: 100M IN JULY 2026」 |
| 13 | FMA 徽章月份 | **已修** | 「NEW: 90M IN 2026」 |
| 14 | 卷数会过期 | **已修** | 「RECORD: 220+ VOLUMES」「140+ VOLUMES」 |
| 15 | 弱出处（Sazae-san、Vagabond、Tokyo Revengers、Kinnikuman、Slam Dunk） | **未修**（作者未声称修） | 屏上无标注。Comment 2 里 Vagabond 仍只给失效的立命馆 PDF 链接 |
| 16 | 「twice as many」 | **已修** | 「about twice as many」 |
| 17 | Captain Tsubasa 口径冲突 | **未修**（作者未声称修） | data.json notes 里记了冲突，`sources.md` §2 没有专门写取舍。可接受 |
| 18 | 徽章 / 名次压 logo | **未修**（作者说明不改） | #23 Tsubasa、#12 Oishinbo、#2 Golgo 13 仍有轻微遮挡，不影响阅读 |
| 19 | 计分板地球仪图标 | **未修**（作者说明不改） | gridX1 下排 |
| 20 | 来源卡「Photo credits」 | **已修**（带图版） | 现为「Image credits: shown on each card and listed in the description」。默认版的问题见 N3 |
| 21 | publish.md | **部分** | ①章节已改为「#30–#23」「#16–#11」✔；②「cross-checked」已删 ✔；③内部备注（dead link、search snippet）已清 ✔；④「shown at reduced size to identify each series」仍在，与第 22 条一起交用户 |
| 22 | 版权封面（§7-4） | **未修（待用户）** | assets.json 30 张都是 `licence: unknown` |
| 23 | 时长 3:37 < 5 分钟 | **未修**（作者说明不改） | 仅提示 |

## 新发现

| # | 严重度 | 位置 | 问题 | 证据 | 建议修改 |
|---|---|---|---|---|---|
| N1 | **major** | publish.md 标题 | 标题为「Best-Selling Manga of All Time \| Top 30 **(card)**」，末尾的「(card)」是生成模板的残留（疑似从新的 period_label「…year on each card」截出来的），观众会看不懂 | publish.md「## Title」 | 改为如「Best-Selling Manga of All Time \| Top 30 Ranked by Copies (2026)」。检查 `rank_scroll publish` 标题模板，07 脚本里也加一条替换，避免重新生成时复发 |
| N2 | **major** | `render/thumbnail.png` | 缩略图是修改前生成的（23:41，早于 00:23 的数据修改）：① 统计行仍为第 1 轮已判定误导的「Latest official figures · Nov 2026」（#5）；② #2 位置用的是被替换掉的旧 Golgo 13 封面（红楼图、标题被裁）；③ 图里有 3 张版权封面，如果用户选默认版发布，缩略图仍会泄露封面。publish.md 的上传清单直接指向这张图 | `dsrc_thumb.jpg` 下半；文件时间戳 | 用当前 data.json 重新生成缩略图，统计行与片头一致。再按带图版 / 默认版各出一张，或在 publish.md 注明默认版不能用这张缩略图 |
| N3 | minor | 默认版来源卡（3:15–3:19） | 默认版的卡上没有封面，也没有「Illustration:」署名行，来源卡却写「Image credits: shown on each card and listed in the description」。默认版配的 publish.md（带图版措辞和整段封面署名）也对不上 | `dsrc_thumb.jpg` 上半；`gridD.jpg` | 默认版来源卡改为「Cover images withheld」之类，或删去这一行；按默认版另生成一份 publish 草稿（不加 `--allow-risk-images`） |
| N4 | minor | publish.md 标签 | 「#Best-sellingMangaOfAllTime」里有连字符，YouTube 在连字符处截断标签，实际只生效「#Best」 | publish.md 描述末行 | 改为「#BestSellingManga」 |
| N5 | minor | #14 JoJo（约 1:28–1:40）、#11 Attack on Titan（约 1:47–1:58） | 按新规则「as of = 首次公布年份」，JoJo 自家 notes 写「120M has been restated unchanged since ~2022 (JA Wikipedia: 2022年1月時点)」，卡上却标 2023；AoT notes 称 Wikipedia 写「By November 2023」，卡上标 2024（这条依据较弱，可保留）。Naruto（2023）、Bleach（2022）、Doraemon（2024）的「首次公布年份」也没有在 notes 里核实，只是沿用来源日期 | data.json notes；`06_qc_fixes.py` FIRST_ANNOUNCED | JoJo 改为 2022；其余在 sources.md §2-4 注明「首次公布年份未能核实，按最早找到的日期」，避免规则被挑刺 |
| N6 | minor | publish.md 章节 | 「2:01 Top 10」略晚：#10 JJK 约 1:57 就已完整入画，JJK 洞察卡约 1:52 出现。其余章节点与实际时间吻合：0:52 时「Next: seven series」洞察卡在画，2:58 时 One Piece 已入画，3:09 时计分板 3:08.5 开始 | s115、s120 帧 | 改为 1:56 左右（可选） |
| N7 | minor | topic.md | 立项文档仍保留旧文案：统计行「Latest official figures · Nov 2026」、洞察「only about 58M」「in a single year」、徽章「+50M IN ONE YEAR」「100M IN JUNE 2026」。不影响成片，但以后照 topic.md 重跑会把错误带回来 | topic.md 第 8、17、19、21 行 | 同步为现行文案，或标注「已被 06_qc_fixes 取代」 |
| N8 | minor | publish.md 署名一致性 | 除北斗外（见第 11 条），Sazae-san 卡上写「© Machiko Hasegawa / Shimaisha」，publish.md 写「長谷川町子美術館」；Kindaichi 的 publish.md 署名漏掉 Seimaru Amagi，而卡上作者是「Amagi, Kanari & Sato」 | publish.md Comment 1；data.json `image_credit` | 卡上署名与描述框统一为同一版权方写法 |

## 逐卡核对（30/30）

所有卡的名次、作品名、出版社行、数值、「as of」年份（= `figure_year`）、作者和年份标签、徽章、署名，与 data.json 逐字一致。没有文字出框，也没有卡与卡互相遮挡（拼图中看似重叠的地方，是相邻帧拼接处的假象）。

| 名次 | 作品 | 数值 · as of | 徽章 | 封面 |
|---|---|---|---|---|
| 1 | One Piece | 600M · 2026 | — | ✔ 第 1 卷 |
| 2 | Golgo 13 | 300M · 2021 | RECORD: 220+ VOLUMES | ✔ 第 206 卷（新），清晰 |
| 2 | Doraemon | 300M · 2024 | — | ✔ |
| 4 | Detective Conan | 270M · 2023 | — | ✔ 第 1 卷（新），清晰 |
| 5 | Dragon Ball | 260M · 2022 | — | ✔ |
| 6 | Naruto | 250M · 2023 | — | ✔ |
| 7 | Demon Slayer | 220M · 2025 | ONLY 23 VOLUMES | ✔ |
| 8 | Slam Dunk | 185M · 2025 | — | ✔ |
| 9 | KochiKame | 157M · 2014 | — | ✔ |
| 10 | Jujutsu Kaisen | 150M · 2025 | +50M IN 15 MONTHS | ✔ |
| 11 | Attack on Titan | 140M · 2024 | — | ✔（年份见 N5） |
| 12 | Oishinbo | 135M · 2020 | ON HIATUS SINCE 2014 | ✔ 第 1 卷（新），清晰 |
| 13 | Bleach | 130M · 2022 | — | ✔ |
| 14 | JoJo | 120M · 2023 | — | ✔（年份见 N5） |
| 14 | Kingdom | 120M · 2026 | NEW: 120M IN JAN 2026 | ✔ |
| 16 | Baki | 100M · 2024 | — | ✔ 英文版，署名标了 English ed. |
| 16 | Fist of the North Star | 100M · 2019 | — | ✔ 英文版，署名 Coamix |
| 16 | Hajime no Ippo | 100M · 2023 | 140+ VOLUMES | ✔ |
| 16 | Hunter × Hunter | 100M · 2026 | NEW: 100M IN JULY 2026 | ✔ |
| 16 | My Hero Academia | 100M · 2024 | — | ✔ |
| 16 | Kindaichi | 100M · 2019 | — | ✔ |
| 16 | Touch | 100M · 2004 | — | ✔ |
| 23 | Captain Tsubasa | 90M · 2023 | — | ✔ |
| 23 | Fullmetal Alchemist | 90M · 2026 | NEW: 90M IN 2026 | ✔ |
| 25 | Sazae-san | 86M · 1999 | OLDEST ON THE LIST | ✔（出处弱） |
| 26 | Kinnikuman | 85M · 2025 | — | ✔ |
| 27 | Vagabond | 82M · 2012 | ON HIATUS SINCE 2015 | ✔（出处失效） |
| 28 | Sangokushi | 80M · 2020 | — | ✔ |
| 28 | Tokyo Revengers | 80M · 2024 | — | ✔ |
| 30 | Haikyu!! | 75M · 2025 | — | ✔，可读约 3.3 s |

- **洞察卡 5 张**：都已与 `sources.md` §3 核对，均成立。蜡笔小新这张只陈述了确定的部分。
- **计分板**：Shueisha 16、Kodansha 5、Shogakukan 4、Leed / Akita / Square Enix / Shimaisha / Ushio 各 1，合计 30，与 data.json 一致。右上角实时计数逐步累加到同样的结果。
- **冠军段**（3:02–3:08）：One Piece 卡，右侧依次是奖杯、No. 1、600M、as of 2026，正常。
- **来源卡**（3:15）和**片尾**（3:19–3:37）：正常，片尾留出 18 s 的空位。
- **默认版**：30 张卡都是「Cover withheld: copyrighted artwork」占位，整齐，没有漏出封面，也没有「Illustration:」行。徽章在占位卡上显示正常。来源卡见 N3，缩略图见 N2。

## §7 清单

1. **名次连续、无重复，排序与 data.json 一致：通过。**
2. **数值可追到 sources.md，统计期与片头一致：通过（附条件）。** 30 个数值都能在 `sources.md` 找到原文；片头统计行「Latest announced figure · year on each card」与卡上的年份标法一致。条件是用户批准 §3.3 的旧数字例外（#5）。年份细节见 N5。
3. **国旗 / 国家（本期为出版社）：通过。** 北斗记在 Shueisha 名下的口径应写进 sources.md（#11）。
4. **图片都在 assets.json 里，许可允许：不通过（待用户决定）**（#22）。30 张都登记了，但 `licence: unknown`。默认版满足本项，但要先处理 N2 和 N3。
5. **文字不出框、不闪烁，手机全屏 3 秒内看得清：通过。** 实测整数 2 px/帧（120 px/s），#30 可读约 3.3 s。
7. **描述框来源与署名完整：部分不通过。** 标题有「(card)」残留（N1），缩略图过期（N2），署名有不一致处（#11、N8），标签失效（N4），Vagabond 来源链接已失效（#15）。

## 总结

结论：**小修后可发布**。第 1 轮声称修好的 #1、#2、#3、#4、#6、#7、#8、#9、#10、#12、#13、#14、#16、#20 都已在画面和文件里落实。新换的 Conan、Golgo 13、Oishinbo 封面作品正确、清晰、裁切合理。#30 Haikyu!! 可读约 3.3 s。30 张卡、5 张洞察卡和计分板都没有发现回退，视频本身不需要重渲。

上传前必须做的三件事：

1. publish.md 标题去掉「(card)」（N1）。
2. 用当前数据重新生成缩略图：旧图还写着「Latest official figures · Nov 2026」，用的也是旧 Golgo 封面（N2）。
3. 若用默认版发布，改掉来源卡的「Image credits: shown on each card」，并换一份不含封面署名的发布草稿（N3）。

其余都是小修：JoJo 的 as-of 年份改为 2022、北斗和 Sazae-san 署名统一、标签去掉连字符、topic.md 同步现行文案。

仍须用户拍板：版权封面带图版是否发布（§7-4、#21④、#22）、18 个月旧数字例外（#5）、Crayon Shin-chan 是否剔除。
