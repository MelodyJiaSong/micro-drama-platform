# ep20 · 世界最高瀑布 Top 35 · 审片记录

## 配乐审片 · 2026-11-04（独立上下文，两轮）

> 补配乐后由另起上下文的审稿代理测量（未参与制作）；脚本与数据在会话 scratchpad `audio_qc/`、`audio_qc2/`。只换音轨，两版视频流与 `render/_silent/` 原静音版逐流哈希一致（14498 帧）。

**结论：通过**（一处建议人耳试听）。
- 配乐：Suno 任务 f90acccf，两首（7314ca5d / 856a32a0），按 856a@0–80.5 → 7314@5–145 → 7314@155.7–末尾 拼接，4 s 交叉淡化，最后一段放到原曲自然结尾。
- 第 1 轮（两首直接拼）发现冠军停留（206.6–212.6 s）落在曲子的安静段（中位 −21.1）→ 重排后冠军停留 −13.9，成为全片最响段；前十名段 −15.6；响度 −16.0 LUFS，真峰值 −2.9 dBTP；中段最差 15 s 为 −18.2。无削波、断音或拼接爆音。
- 同曲跳接（212.5–216.5 s，跳过原曲 145–155.7 s 的低谷段）：节拍对齐误差 10 ms，响度变化 ≤ 0.8 LU/s；但跨度为 7.5 小节，可能错半小节，建议人耳听 212–218 s。
- `publish.md` 已补 Suno 署名（job f90acccf，clips 7314ca5d / 856a32a0）与 Content ID 清单项。

## 复核 · 2026-11-04

> 独立复核人：没有参与制作，也没有写第 1 轮审片。对照第 1 轮问题清单和 `_build/handoff.md`「第 1 轮审片后的修改」，逐条核对**当前文件与成片**。只写了本文件和 `_build/qc/recheck/`，没有改数据、图片或渲染。

### 核对依据

- **成片规格**：用 ffprobe 逐帧计数，两版都是 1920×1080、60 fps、H.264，14,498 帧，241.633 s。与 `python -m rank_scroll timeline` 的结果一致：共 14,498 帧，分段为 intro 0–5、scroll 5–206.63、champion –212.63、tally –219.63、sources –223.63、end –241.63。
- **manifest**：两版 output_sha256 与文件一致；37 项 inputs 的 sha256 与当前 data.json、assets.json 和各张图逐一比对，全部一致，draft = false。`validate --strict` 结果 OK。
- **抽帧**：放在 `_build/qc/recheck/`。默认版 `d_*.jpg`（文件名里的数字是秒数），包括：
  - 片头 0.5、2.5、4.6 s
  - #35–#33 在 6 s、10.5 s
  - 5 张洞察卡在 31.13、83.07、135、184.4、199.8 s
  - 改动过的卡：#13 在 125 s，#8 在 156.6 s，#2 在 195 s，#1 在 203 和 206.6 s
  - 冠军 209.5 s，计分板 216 s，来源卡 221.5 s，片尾 230 s
  - 另有 5 个随机点（种子 20261104）：50.48、55.07、89.55、142.81、178.88 s

  风险版 `r_*.jpg` 在 6、195、206.6、221.5 s。
- **元素时间**：每张卡和洞察卡居中的时间点用 `timeline.build` 算出，再按这些时间点抽帧核对。

### 原问题逐条结论

| # | 原严重度 | 结论 | 证据 |
|---|---|---|---|
| 1 | blocker（只针对风险版） | **未修**（按设计没动） | 风险版仍用 14 张无许可图，卡上照印「Photo: World Waterfall Database / All rights reserved」（r_006 #35）和「Hougaard Malan / unknown」（r_194.97 #2）。handoff 写明需先取得书面许可 |
| 2 | major | **部分修** | ✅ 25 张 AI 卡左上都有醒目的黄色「AI IMAGE」角标（徽章级，放在 SEASONAL 下面），署名改为「AI-generated image, not a photo」（抽帧中逐张可见）。✅ #2 Tugela 换成 CC0 实拍：Flickr 39498453682，页面核对过是 CC0 1.0，标题「Tugela falls｜Royal Natal NP」，画面是 Amphitheatre 和瀑布，认对。❌ 其余可补实拍的景点（Kjeragfossen、Kukenán、Vinnufossen、Sentinel、Mattenbach 等）没补上，前 10 名仍有 6 张 AI 图（#3 #5 #6 #7 #9 #10），全片 25/35。❌ 片头和来源卡仍没有提 AI 图（d_000.50、d_221.50），只在描述框里写了。有了角标以后，「冒充实景」的风险已经大大降低 |
| 3 | major | **已修** | 洞察卡 5 屏上是「Angel's 979 m adds rapids below its 807 m drop. Drop those and Tugela (948 m) wins.」（d_199.80，未出框）。置顶评论同步为「Count only Angel's 807 m main drop and Tugela (948 m) is #1」 |
| 4 | major | **已修** | #1 上屏「Canaima NP · 807 m main drop」（d_203、d_209.5）；#33「Runs Jun 20–Aug 20」、#35「Usually dry by July」都上屏了（d_006）。第二个标签照旧会被丢（#1 Guinness record、#2 5 tiers、#4 IGN survey 2007、#33 328 m），但关键信息都在第一个标签。冠军面板没有加 disputed 一行，属可选项 |
| 5 | minor | **已修** | 章节是「0:00 Intro & #35–#31」。各章节时间与元素时间对得上：#30 在 26.5 s，#20 在 87.7 s，#10 在 145.2 s，tally 从 212.6 s 起 |
| 6 | minor | **已修** | scope_note 和描述框都写了「Tugela: Guinness」 |
| 7 | minor | **已修** | 洞察卡 2「…; World Waterfall Database estimates ~479 m.」（d_083.07） |
| 8 | minor | **已修** | #33 第二个标签改为「Longest drop 328 m」（数据里核对过；不上屏） |
| 9 | minor | **已修**（按建议里的选项 A） | notes 说明了 Vinnu 是官方名；评论 2 写「World Waterfall Database: Vinnu」 |
| 10 | minor | **已修** | Kjelfossen 重新裁过，主瀑布居中（d_125.03）。Browne 加了 image_focus [0.7, 0.5]，瀑布到了画面中线（d_156.63），但仍是一条细线，原图所限 |
| 11 | minor | **未修** | assets.json、sources.md 和置顶评论的来源仍是 wondermondo 转载页，handoff 承认没找到 Flickr 原图页 |
| 12 | minor | **已修** | Yosemite 交叉核对链接改为 `…/yosemite-falls-all-three-sections`（sources.md 第 70 行、data.json） |
| 13 | minor | **未修** | 两版仍是静音 AAC，volumedetect 测得 mean = max = −91 dB |
| 14 | minor | 知悉 | 时长 4:01.6 没变 |
| 15 | minor（文档） | **已修** | topic.md 改为「Angel 按本期入选规则排第 10」 |

### 新问题

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| N1 | **major** | `render/thumbnail.png` | 文件时间是 11-03 23:19，早于全部修改，没有重出。封面上 #2 仍是第 1 轮指出外观不符的那张**旧 AI Tugela 图**（草坡加两级直瀑），和成片里的实拍不一致；#3 是 AI 图 Mattenbach；三张图都没有 AI 标记。`render_thumb` 本身也不画 AI 角标。封面是曝光最多的一张图，publish 清单又让上传时用它 | 重跑 `rank_scroll thumb`。最好在 data.json 给 #1 Angel、#2 Tugela（实拍）、#4 Yumbilla 设 `thumb`，让封面只用实拍；如果保留 AI 图，就要给 thumb 加 AI 角标 |
| N2 | minor | publish.md 上传清单 | 写「卡上标 Illustration / Render」，屏上实际是「AI IMAGE」。当前 publish.py 生成的已经是新文案，说明 publish.md 生成在渲染器改动之前 | 重跑 `rank_scroll publish`，再跑 `_build/finish_publish.py` |
| N3 | minor（措辞） | 洞察卡 5 | 「…807 m drop. Drop those…」两个 drop 意思不同，连在一起读有点拗口 | 可选：改成「Leave those out and Tugela (948 m) wins.」（字数仍 ≤ 90）。改不改都不挡发布 |
| N4 | info | 渲染可复现性 | 默认版约 02:09 开渲，`rank_scroll/cards.py` 在 02:41 改过，所以两版用的卡片代码不完全相同，manifest 也不记代码哈希。抽帧看两版排版一致，没发现问题 | 知悉。以后两版同批重渲时避开代码改动 |
| N5 | info | 风险版 #2 | 风险版仍用无许可的 Hougaard Malan 图，没有换成现成的 CC0 图 | 风险版本来就不发，知悉 |

改动带来的回归检查：35 个名次连续，同值同名次（22/22、24/24），排序与 value 一致。5 张洞察卡的 after_rank 位置正确：30（季节说明）、21、12（Mongefossen 773 m 排在 #12 771 m 和 #11 783 m 之间）、4（「Next: a Swiss fall」紧接 #3 Mattenbach）、2（在 #1 之前）。抽到的帧里没有文字出框或省略号，洞察卡文字都在卡内。计分板终值 NO 11、US 10、VE 3、NZ 3、CH / PE / FR 各 2、ZA / CA 各 1，合计 35；角落计分板到 #5 时挪威反超（d_178.88），正确。没有占位卡。

### 最终结论

| 版本 | 结论 |
|---|---|
| **默认版** `ep20_tallest_waterfalls_master.mp4` | **小修后发布**。成片本身可以发：3 条 major 里 #3、#4 已修，#2 靠醒目的 AI 角标和 Tugela 实拍降到可接受。上传前必须重出封面（N1），并重新生成 publish.md（N2）。建议（不挡发布）：补实拍替换 AI 图，来源卡或片头加一句「Some images are AI illustrations」，补 Browne 原图页，配乐 |
| **风险版** `…_with-risk-images.mp4` | **必须修，不能发布**。14 张图仍无许可（原第 1 条），卡上照印「All rights reserved / unknown」 |

**推荐发布：默认版。** 理由：默认版所有图片都有可商用许可或是标明的 AI 图，数据和措辞问题都已修好。风险版的实拍虽然更多，但 14 张图没有书面许可，其中 WWD 和 Northwest Waterfall Survey 明令禁止未经许可使用，发布有下架和侵权风险。

## 第 1 轮独立审片 · 2026-11-04

> 独立审片人（没有参与制作，按 `qc_brief.md` 审）。审的是当前文件：`render/` 两版成片（manifest 的 output_sha256 与文件一致，inputs 的 sha256 与当前 data.json、assets.json 和各张图一致）。主代理之后如果给 AI 图补真实照片并重渲，本轮的图片和成片结论要重审。只写了本文件和 `_build/qc/`，没有改数据、图片或渲染。

### 结论

| 版本 | 结论 | 一句话 |
|---|---|---|
| **默认版** `ep20_tallest_waterfalls_master.mp4`（9 张实拍 + 26 张 AI 图） | **小修后发布**（下面 3 条 major 修完；第 1 条最好修） | 数据扎实，口径也执行得一致。最大的问题是 26/35 张 AI 图，前 10 名里也有 7 张，卡上的 AI 标注又几乎看不清，观众会把 AI 图当成真瀑布照片 |
| **风险版** `…_with-risk-images.mp4`（23 张实拍 + 12 张 AI 图） | **必须修，不能发布** | 14 张图没有许可。其中 5 张来自明令禁止未经书面许可使用的 WWD / Northwest Waterfall Survey，另有职业摄影师的画廊作品和 Instagram 转载图；卡上署名还直接印着「All rights reserved」 |

**发布主版本建议：默认版。** 风险版的 14 张图，没有逐张拿到书面许可之前不要发布，也不要上传为不公开视频。更好的做法：把风险版里认对了的瀑布当作「这条瀑布长什么样」的参照，去找可商用的实拍图（Flickr CC、Unsplash、Pexels、作者授权）替换默认版的 AI 图，然后只发默认版。

### 问题清单

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| 1 | **blocker（只针对风险版）** | 风险版 #2 #3 #5 #6 #9 #10 #11 #14 #16 #17 #24 #30 #31 #35 | assets.json 里许可为 unknown 或 All rights reserved，共 14 张。#24 和 #35 取自 WWD，#11 #30 #31 取自 waterfallsnorthwest：这两站都写明照片未经书面许可不得使用。#2 Tugela 是 Hougaard Malan 在 osnerartgallery 卖的艺术作品；#10 Waihilau 是 Bruce Omori 的作品，取自 Instagram 转载站 instagrammernews；#9 和 #16 的原图带 © 水印或说明字。成片卡上直接印着「Photo: Northwest Waterfall Survey / All rights reserved」「… / unknown」（抽帧 r005、r025、r105、r140、r150） | 不发风险版。如果某张一定要用，先拿到书面授权并存档，再把账本许可改成「licensed by permission」 |
| 2 | **major** | 默认版全片，尤其是前 10 名（#2 #3 #5 #6 #7 #9 #10 是 AI 图） | 26/35 张是 Codex 生成的逼真照片风格图。卡上的「Photo: AI-generated illustration」在 1080p 下约 13 px，灰字（`_build/qc/frames/crop_credit_def150.png`），手机上基本看不见。片头和来源卡也都没有提 AI。几张 AI 图看起来像在冒充真实景点：#35 Sentinel 画的是 Yosemite 的 Sentinel Rock 加瀑布；#3 Mattenbach 和 #32 Ägertenbach 都是 Lauterbrunnen 石灰岩壁上一条细瀑，像 Staubbach，两张图也几乎一样；#2 Tugela 画成草坡上的两级直瀑，和真实的 Amphitheatre 五级瀑布外观不符；#22 Kjeragfossen、#29 Kukenán、#23 Yutajé 都是知名景点，看过的人一眼就能认出不像 | ① **优先补可商用实拍**：Tugela、Vinnufossen、Kjeragfossen、Kukenán、Sentinel、Mattenbach、Skorga、Døntefossen 都是常被拍的景点。线索：Unsplash「LU0fo0E36RE」（De wet Cilliers，标 Tugela Falls，未核对画面）；Flickr CC 按瀑布名加 `license=1,2,4,5,9,10` 搜。② 留下的 AI 图，卡上署名改成醒目的角标 **「AI ILLUSTRATION」**（徽章级字号，放在国旗下面），不要写「Photo:」。③ 片头统计行或来源卡加一句「Some images are AI illustrations, not photos」 |
| 3 | **major** | 洞察卡 5（after #2，约 3:15–3:25），publish.md 置顶评论 | 原文「Angel's 979 m includes rapids below its 807 m plunge. **Count the plunge only: Tugela wins.**」逻辑不通：Tugela 的 948 m 是五级总落差，不是单级（单级最长 411 m）。如果真的「只算单级」，Angel 的 807 m 远超 Tugela。Guinness 原话是「如果 Angel 的实际高度只有最初 807 m 那一段，多级的 948 m Tugela 就是最高」。懂行的观众会在评论区抓这一点 | 改成「Angel's 979 m adds rapids below its 807 m drop. Drop those and Tugela (948 m) wins.」（83 字符，≤90）。置顶评论同步改成「count only Angel's 807 m main drop and Tugela (948 m) is #1」 |
| 4 | **major** | 冠军卡 #1、#33 Mardalsfossen、#35 Sentinel 等（标签被丢） | 渲染器「放不下就从后往前丢」：#1 的标签「Single plunge 807 m · Guinness record」整行没有上屏，屏上只有 HEIGHT DISPUTED 徽章和地点；#33 的「Runs Jun 20–Aug 20」（解释 HYDRO-REGULATED 的关键信息）没上屏；#35 的「Usually dry by July」、#34 和 #31 的标签也都丢了（抽帧 s001–s004、s040–s042） | 缩短 subtitle（如「Canaima NP」「Eikesdalen」「Yosemite NP」），让第一个标签能显示；冠军右侧的 No. 1 面板可以加一行「807 m single drop · disputed」 |
| 5 | minor | publish.md 章节 | 「0:00 Intro & #30–#21」应为 **#35–#21**（N = 35） | 改章节文字 |
| 6 | minor | scope_note / 描述框 | scope_note 写「只收 database surveyed / confirmed with a stated basis」，例外只列了 Angel 和 Yumbilla；Tugela 在 WWD 是 Unconfirmed，是靠「Guinness 引同一数」才入选的，屏外说明漏了它 | 在 scope_note 的例外里加上「Tugela: Guinness」 |
| 7 | minor | 洞察卡 2（after #21） | 「elevation data put it nearer 479 m」：479 m 是 WWD 用 Google Earth 高程剖面做的估算，WWD 自己的状态是 Unconfirmed，屏上写得像定论 | 改成「…but the World Waterfall Database estimates ~479 m」 |
| 8 | minor | #33 Mardalsfossen 数据 | data.json 的标签「Free fall 262 m」；WWD 页面写 Tallest Drop 328 m（2026-10-13 更新）。现在因标签被丢没上屏，修第 4 条后会上屏 | 改成 WWD 的 328 m 或删掉这个标签 |
| 9 | minor | #6 名称 | WWD（2026-10-13）写 Vinnu 是官方名，「Vinnufossen is used incorrectly in some sources」 | 可保留通用名，在 notes 或置顶评论说明；或者屏上写「Vinnufossen (Vinnu)」，前提是放得下 |
| 10 | minor | #13 Kjelfossen、#8 Browne 构图 | Kjelfossen 卡的上半部是灰天，瀑布挤在右侧（s024）；Browne 原图 1000×750，瀑布在画面右侧，只是一条细线（来源页说明是「Browne Falls (to the right)」），卡上主体太小 | Kjelfossen 把 image_focus 往下右调；Browne 优先换图，至少把 image_focus 调到 [0.65, 0.5] |
| 11 | minor | #8 Browne 许可链 | 账本来源页是 wondermondo 转载页，原作者是 Flickr floydwilde（CC BY-SA 2.0），没有链到原图 | 找到 Flickr 原图页，补进账本和置顶评论 |
| 12 | minor | sources.md 的 Yosemite 交叉核对链接 | `https://www.usgs.gov/media/images/yosemite-falls` 返回 404；USGS 现有的是 `…/media/images/yosemite-falls-all-three-sections`（图注「highest measured waterfall in North America, 2,425 ft」） | 改链接 |
| 13 | minor | 音轨 | 两版都是 anullsrc 静音 AAC，没有配乐，听感没法审 | 按 bible §5 配乐后再按 §7-6 查响度和片尾 |
| 14 | minor | 时长 | 4:01.6，比 bible 建议的 5–8 分钟短，插不了中插广告。N = 35 的理由成立 | 知悉即可；不建议为凑时长放进未证实条目 |
| 15 | minor（文档） | topic.md「待用户确认」第 1 条 | 写「按 WWD 只算 807 m，Angel 掉到约第 13」。按本期入选规则，807 m 应该排在 Kjerrskredfossen 831 m 之后，是**第 10**（约第 13 是 WWD 未过滤原榜的位置） | 改成「约第 10」，免得用户误判 |

**认图核对（实拍图）**：

| 名次 | 图 | 结论 |
|---|---|---|
| #1 Angel | Imaggeo 19005「Kerepakupai Vená – Canaima」，CC BY-SA 3.0（页面核对过） | ✅ 认对 |
| #4 Yumbilla | Flickr「amazonas bongará Catarata Yumbilla 2」，CC BY-SA 2.0 | ✅ 标题对得上 |
| #8 Browne | wondermondo 图注「Browne Falls (to the right)」 | ✅ 认对，但主体小（第 10 条） |
| #12 Gocta | Flickr MI PERÚ「Cataratas Gocta」，PDM；画面是两级瀑布 | ✅ |
| #13 Kjelfossen | Flickr「Kjelfossen Waterfalls from Gudvangen」 | ✅（构图见第 10 条） |
| #18 Yosemite | Pexels，画面是 Upper Yosemite Fall | ✅ 只拍到上段，可接受 |
| #21 Trou de Fer、#33 Mardalsfossen、#34 Cascade Blanche | Flickr 标题都对得上，画面也符合 | ✅ 三张都对。Cascade Blanche 原图右下角有作者签名「by VillageHero」，是作者署名，不算图库水印 |
| 风险图 #9 Kjerrskredfossen | John Wise 页面图注「Kjerrskredsfossen seen from Gudvangen」 | ✅ 认对，但只拍到顶上一段跌落，和卡上「6+ tiers」不呼应；原图带 © 水印 |
| 风险图 #3 Mattenbach、#14 Isella | 瀑布在画面里只是远处一条细线 | ⚠ 主体太弱，认不出 |
| 其余风险图（#2 #5 #6 #10 #11 #16 #17 #24 #30 #31 #35） | 来源页标题对得上，画面符合内容笔记 | ✅ 认对；许可问题见第 1 条 |

**AI 图瑕疵**：26 张逐张看过（`_build/qc/gen_a.jpg`、`gen_b.jpg`，全尺寸抽看了 #2、#16、#35），没有明显的生成畸形（水流断裂、重影、文字或 logo）。问题在于「像真照片」和同质化：雪山、冰川、绿坡、细瀑的构图一再重复，#3 和 #32、#7 和 #27（底部都是湖面），连续出现时容易看腻。

### 核对过的数据样本（2026-11-04 亲自上网核对）

| 名次 | 瀑布 | 屏上值 | 核对来源 | 结果 |
|---|---|---|---|---|
| 1 | Angel Falls | 979 m / 3,212 ft，HEIGHT DISPUTED | Guinness 页：total drop 979 m (3,212 ft)，longest single drop 807 m，「if only 807 m … Tugela 948 m would be tallest」；WWD Kerepakupai Merú 807 m，Confirmed，第 14 位 | ✅ 数对；洞察卡措辞见第 3 条 |
| 2 | Tugela Falls | 948 m，SEASONAL | WWD：948 m，tallest drop 411 m，5 drops，Unconfirmed，4 months，2026-10-17 更新；983 m（2016）测点在 1 km 外 | ✅ |
| 3 | Mattenbach | 930 m，REMEASURED 2020 | WWD：930 m，Confirmed；Vertical Water Canyoning Team 2020 年绳降实测，原估 840 m；流量月数空白 | ✅（不标 SEASONAL 与规则一致） |
| 4 | Yumbilla | 895 m | MercoPress 2007-12-04：IGN 测得 895.4 m；WWD 榜单 896 m，Unconfirmed | ✅ |
| 5 | Skorga | 875 m | WWD 榜单 875 m，Cataloged | ✅ |
| 6 | Vinnufossen | 845 m | WWD：845 m，tallest 575 m，Cataloged，9 months，2026-10-13 更新 | ✅（名称见第 9 条） |
| 7 | James Bruce | 840 m | WWD 榜单 840 m，Confirmed | ✅ |
| 8 | Browne | 836 m | WWD：836 m，Confirmed，6 drops；旧值 2,031 ft（约 619 m），WWD 认为是低估 | ✅ |
| 10 | Waihilau | 792 m，「One single drop」 | WWD：total = tallest = 792 m，1 drop，12 months | ✅ |
| 12 | Gocta | 771 m，「Lower drop 540 m」 | WWD：771 m，tallest 540 m，2 drops | ✅ |
| 13 | Kjelfossen | 765 m | WWD 榜单 765 m，Cataloged | ✅ |
| 18 | Yosemite | 739 m / 2,425 ft，「Upper fall 436 m」 | WWD：739 m，tallest 436 m，8 months；USGS 图注 2,425 ft | ✅（链接见第 12 条） |
| 22 | Kjeragfossen | 715 m，「Free fall 715 m」 | WWD：715 m = tallest，1 drop，Plunge，「nearly entirely free-falling」，只在融雪或大雨时有水 | ✅（SEASONAL 合理） |
| 33 | Mardalsfossen | 645 m | WWD：645 m，tallest **328 m**，9 months，水电调节 | ✅ 主值对；标签见第 8 条 |
| 35 | Sentinel | 631 m | WWD：631 m，tallest 210 m，11 drops，6 months | ✅ |
| 洞察 3 | Mongefossen | 773 m，1977 年起断流 | WWD：773 m；1977 年引入 Grytten 水电站，此后基本断流 | ✅ |
| 洞察 2 | Mutarazi | 762 → 479 m | WWD Mutarazi-Falls-8：1,572 ft / 479 m，Unconfirmed，2025-05-27 更新 | ✅（措辞见第 7 条） |
| 洞察 4 | Mattenbach +90 m | — | 同 #3 | ✅ |

其他核对：

- WWD「Overall Height」第 1 页（35 条）的顺序与 sources.md §2 的排除表一致：Tres Hermanas、Haloku、Olo'upena、Los Chorros de Cura、Pu'uka'oku 都是 Unconfirmed，Terror 和 Helgåfossen 是 Confirmed，均已排除。入选规则执行一致。
- 名次连续，同值同名次（22、22、24、24、26），排序与 value 一致。
- 国旗与国家逐张看过；留尼汪计 France，与口径一致。
- 计分板：Norway 11、US 10、Venezuela 3、New Zealand 3、CH / PE / FR 各 2、ZA / CA 各 1，合计 35 ✅。角落计分板随滚动累加正确，#5 Skorga 出场时挪威反超美国，悬念成立。

### 成片技术核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 分辨率 / 帧率 | 1920×1080 / 60 fps ✅ | 同 ✅ |
| 时长 / 帧数 | 241.633 s / 14,498 帧 = 241.633 × 60 ✅，未截断 | 同 ✅ |
| timeline（manifest） | intro 0–5、scroll 5–206.6、champion 206.6–212.6、tally 212.6–219.6、sources 219.6–223.6、end 223.6–241.6，抽帧逐段对上 ✅ | 同 |
| output_sha256 / inputs | 与文件一致 ✅ | 同 ✅ |
| 音频 | anullsrc 静音（第 13 条） | 同 |
| 文字出框 / 省略号 | 没发现名称或数值截断；标签整行被丢的问题见第 4 条 | 同 |
| 占位卡 | 无 ✅ | 无 ✅ |

### 观众视角（全球英文观众）

- **会划走的地方**：片头 5 s 是纯标题加绿底，没有一张瀑布画面（full_def_003）。开场 #35–#24 都是冷门名字，默认版里大多是 AI 图，最容易在 0:05–0:40 流失。建议片头叠一张 Angel 的实拍做背景，或者在统计行后面加一句钩子（「Angel or Tugela? Only one is No. 1」）。
- **亮点（反常识）**：Angel 到底算不算第一（Guinness 与 WWD 的分歧）；Mongefossen 因为水电站「消失」；Mattenbach 2020 年绳降实测「长高」90 m；Mutarazi 被下调；挪威与美国 11 比 10 的计分板拉锯。这几张洞察卡和计分板是本期最有价值的部分。
- **信任风险**：标题承诺「世界最高瀑布」，观众期待看到真实景观。前 10 名有 7 张是 AI 图，一旦有人在评论区指出「这不是 Tugela」，会伤害「数字真实、有出处」的系列定位（Vision 核心）。所以第 2 条虽然不涉及法律，也排在 major 第一位。

### 抽帧清单（`_build/qc/frames/`）

- 默认版每 5 s 一帧，共 48 帧：`def/s000–s047.jpg`（s000 ≈ 0 s、s001 ≈ 5 s …）；拼图 `sheet_def_0–7.jpg`。涵盖片头（s000）、#35（s001）、全部 5 张洞察卡（s005–s007、s015–s017、s025–s028、s035–s037、s039–s042）、#20 到 #11（s018–s028）、第 10 名附近（s028–s030）、冠军（s040–s042）、计分板（s043）、来源卡（s044）、片尾（s045–s047）。
- 全尺寸帧：`full_def_000/003/150/197/205/210/216/221/230.png`；AI 署名字号特写 `crop_credit_def150.png`。
- 风险版：`risk/r005 r025 r055 r060 r105 r115 r140 r150 r165 r170 r185 r195.jpg`，拼图 `sheet_risk_0–1.jpg`；特写 `full_risk_150.png`、`crop_risk150.png`。
- 素材拼图：实拍 `_build/qc/real_a/b/c.jpg`，AI 图 `gen_a/b.jpg`、`gen_detail.jpg`。脚本 `sheet.py`、`fsheet.py`。

### 本轮没审到的

- 配乐（片子是静音的）。
- 风险版每张原图的水印在卡片裁切后是否露出：只抽看了 #9，其余没有逐张放大看。反正结论是不发风险版。
- Wikipedia 交叉核对值：没有逐条复核，只看了 WWD 和权威源。
