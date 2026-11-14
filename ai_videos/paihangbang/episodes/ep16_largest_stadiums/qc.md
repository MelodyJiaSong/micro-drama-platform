# ep16 世界最大体育场 Top 50 · 审片记录（qc.md）

## 复核 · 2026-11-04（第 1 轮返修后，独立上下文）

> 复核人没有参与制作，也没有写第 1 轮审片。只写了本文件和 `_build/qc/recheck/`，没有改数据、图片或渲染。
> 复核对象：默认版 `render/ep16_largest_stadiums_master.mp4`（05:50 重渲，sha256 0a10d74d…），风险版 `render/ep16_largest_stadiums_master_with-risk-images.mp4`（05:24 渲染）。两版 sha256 都与各自 manifest 的 output_sha256 一致。
> 证据：抽帧 `_build/qc/recheck/m/`（默认 74 帧：56 个元素居中点＋片头 / #50 / 冠军 / 计分板 / 来源卡 / 片尾＋5 个随机点 40.69、91.83、113.74、287.49、328.13 s）、`r/`（风险 16 帧），拼版 `sheet_m_1–7.jpg`、`sheet_r_1–2.jpg`；原图对照 `img_a.jpg`（#27 / #34 / #41 / #20 风险图）、`img_gen.jpg`（6 张 AI 图）；局部放大 `crop_34_27_hz_41.jpg`；脚本 `check_manifest.py`、`table.py`、`card_times.txt`。

### 最终结论：**必须修**（两版都不能发；修完 1 个 blocker 后可发默认版）

- **新 blocker N1**：#27 MetLife Stadium 的新主图拍的是 **Yankee Stadium**（纽约洋基棒球场），两版都在用。
- 第 1 轮的 3 个 blocker 都已修好：#34 认对了，#20 风险图和 #41 都换成了实拍。6 个 major 修好 5 个，M1 部分修好。
- **推荐发默认版**。理由：默认版 50 张卡全部可商用，或是带 AI IMAGE 标记的生成图，或是诚实的无图卡。风险版有 29 张「licence unknown」和 9 张 FoP 图要用户逐张签字，而且渲染在数据最后一次修改之前（见 N5）。修完 N1 后两版都要重渲；风险版只在用户签字放行后才发。

### 第 1 轮问题逐条核对

| # | 状态 | 核对结果 |
|---|---|---|
| B1 #34 Monumental 认错 | **已修** | 新图 Flickr olaechea/32214827320，页面标题「Estadio Monumental: Lima - Perú \| Partido amistoso: Universitario de Deportes 1 vs. Once Caldas 2 - 27.01.17」，CC BY-SA 2.0（license=5）。原图看台上有大学体育俱乐部的「U」字马赛克，确认是 Monumental「U」。assets / publish.md（第 61、118 行）/ sources.md 三处署名一致，旧错图已移出账本。剩一个裁切问题，见 N2 |
| B2 风险版 #20 效果图 | **已修** | 新图来自 auburntigers.com，是夜场满场实拍：端区写着「AUBURN」，记分屏写着「SUPER LOUD」，是现状，不是改建效果图（`img_a.jpg`；风险帧 206.83 s）。许可仍是 unknown，属风险版签字范围 |
| B3 风险版 #41 效果图 | **已修** | 新图 Flickr carmelopec/54309465615，标题「04--5-2-2025-PocoX7-Santiago-Bernabeu-4-W」，CC BY 2.0，拍的是 2025 年完工的不锈钢条带新外立面，是实拍。两版共用，不再是风险图。卡上只看到外立面局部，熟悉的观众认得出来，不熟悉的不一定（可接受） |
| M1 看不到球场的卡 | **部分修** | 默认版 50 卡：实拍 41、AI 6、无图卡 3（与 handoff 一致，`table.py`）。看不到球场的卡从 17 张降到 **9 张**：3 张 AI 球迷图（Lusail、Stade de France、Azadi，均为 FoP 国，有标记）、3 张 FoP 无图卡（Misr、Borg El Arab、JIS，写明「Photo withheld: no freedom of panorama」，诚实）、FNB（只有球迷）、GBK（持旗运动员，看台只是虚化背景），以及 N1 认错的 #27。另有 5 张偏弱：Martyrs（仍是场内横幅仪式，m9 未换）、Camp Randall（球员近景，背后是红色看台）、#34（见 N2）、AT&T（只拍到屋顶一角和树）、Luzhniki（大半是天空和顶棚边）。Tiger、Rungrado 换图有效，都能认出球场。最集中的 0:36–1:51 现在是：Atatürk（AI 外观）→ Notre Dame → GBK → Azadi（AI）→ Bernabéu → Martyrs → SdF（AI）→ 杭州（AI 外观）→ 鸟巢 → AT&T → 广东（AI 外观）→ #34。比上一轮好很多，但 13 张里仍有 5 张 AI 图 |
| M2 AI 卡无角标 | **已修** | 6 张 AI 卡都有黄色「AI IMAGE」角标，署名行是「AI-generated image, not a photo」（抽帧 34.5 / 53.5 / 77.17 / 83.5 / 102.5 / 219.5 s）。publish.md 写的是「6 images marked AI-generated are illustrations, not photos」，checklist 也有「Altered or synthetic content → Yes」。剩一处没做：来源卡（362.5 s）没有加「N cards use AI images」这一行（N4） |
| M3 Beaver | **已修** | 徽章改为「2025 OFFICIAL FIGURE」。#5 后面加了洞察卡「Next: Beaver Stadium. On Oct 10, 2026, temporary stands let in a record 114,419 fans.」（85 字符，after_rank 5，位于 Kyle Field 和 Beaver 之间，帧 314.8 s）。sources.md §6 写了出处（ClutchPoints / Penn State）。114,419 这个数第 1 轮已经核过（Daily Collegian），本轮没有再检索 |
| M4「exactly 80,000」 | **已修** | 改为「Five stadiums list a round 80,000 seats: in China, France, the USA and DR Congo.」，sources.md 补了 80,698 |
| M5 #50 停留太短 | **已修** | `layout.intro_hold: 2.5`。抽帧 4.0 s 时卡片刚进场，5.0–7.5 s 完整静止，8.6 s 左边开始出屏，完整可读约 3.7 s，≥3 s |
| M6 封面 | **已修** | `render/thumbnail.png` 是 MCG / Wembley / Rose Bowl 三张实拍（#11 / #16 / #17），没有出现冠军。三张都是默认版里许可干净的主图或替代图 |
| m1 #50 徽章 | 已修 | 「+100 SEATS IN 2026」 |
| m2 Empower 官方页 | 未处理 | 发布前复核（handoff 已列入） |
| m3 Azteca 版本 | 已修 | sources.md 第 27 行 |
| m4 Bernabéu 俱乐部未公布 | 未修 | 徽章仍是「RENOVATED 2025」，屏上看不出这个数不是官方数。可接受，建议在置顶评论里说明 |
| m5 Camp Nou | 未处理 | 发布前复核 |
| m6 Cotton Bowl 裁切 | 未修 | 帧 238.5 s 仍是「TON BOW」加海报 |
| m7 旧貌照片 | 未修 | 可保留 |
| m8 冠军图分辨率 | 未修 | 仍是 Pexels 1000×750，账本作者仍是「pexels.com contributor」（帧 350 s 偏软） |
| m9 Martyrs 横幅 | 未修 | 帧 70.83 s 仍是场内横幅仪式 |
| m10 水印说明 | 未处理 | 风险版签字时一并看 |
| m11 Misr / FNB 风险图 | 部分修 | FNB 风险图换成「Soccer City Stadium at night」（2010-05-27，CC BY 2.0），是完工后的样子，已修。Misr 仍待签字前复核 |
| m12 publish.md | 已修 | AI 署名去掉了重复。章节 1:10 / 2:18 / 3:26 / 4:35 与新时间线一致（#36 首卡约 70.8 s、#30 138.8 s、#20 206.8 s、#10 275.1 s）；「5:43 No. 1」比冠军段开始的 5:47.6 早约 4.6 s，可接受 |
| m13 静音 | 未修 | 配乐另行制作，本轮不做听感检查 |

### 新问题

| # | 严重度 | 版本 | 位置 | 问题与证据 | 建议修法 |
|---|---|---|---|---|---|
| N1 | **blocker** | 两版 | #27 MetLife Stadium，约 2:30–2:45（居中点 157.83 s） | 返修 M1 时换上的主图 `27_metlife_stadium.jpg`，来源 Flickr kenlund/7237907630，页面标题是「**God Bless America, Yankee Stadium**」，描述开头是「Yankee Stadium is a stadium located in The Bronx…」。画面里能看到洋基球场标志性的白色拱形檐饰（frieze），座椅上有「NY」标志（`img_a.jpg` 左上；`crop_34_27_hz_41.jpg`）。这是棒球场，不是 MetLife。屏上卡片正好裁到檐饰和看台，纽约观众一眼就能认出来。另外，画面里有几十张可辨认的普通观众正脸，近景很大。publish.md 第 55、112 行和 sources.md 第 167 行的署名都跟着错了 | 换一张真正的 MetLife 可商用照片（Flickr CC 搜「MetLife Stadium」，只用标题或描述写明 MetLife 的图，优先满场或外观），找不到就用无图卡，不要用别的球场顶替。同步改 assets.json、publish.md、sources.md，**两版都重渲**。建议在换图流程里加一步：每张新图都核对来源页标题。本条就是没核标题才漏过去的 |
| N2 | minor | 两版 | #34 Estadio Monumental，约 1:48（108.83 s） | 横幅原图裁成竖卡后，只剩夜空、灯塔和上层看台。最有辨识度的「U」字马赛克在原图左下，被裁掉了，卡面大半是黑色 | 设 `image_focus`（约 [0.3, 0.7]），让「U」马赛克入画 |
| N3 | minor（需用户知情） | 默认 | #35 广东奥体、#36 杭州奥体、#45 Atatürk（AI 外观图） | **造型和真实建筑没有明显不符**：杭州是一圈白色钢花瓣，在钱塘江南岸，对岸是钱江新城，与「大莲花」一致；广东是东西两片分开的白色飘带顶棚加彩色座椅，与实物特征一致；Atatürk 是只罩住一侧主看台的新月形单片顶棚加田径跑道，与实物特征一致。细节有出入：广东那张把珠江新城天际线和广州塔画在紧挨着球场的背后，实际相距约 10 km，构图上明显压缩了；Atatürk 背景画了海面和远处城区，实际场址在 İkitelli 内陆；三张的花瓣、肋拱数量和座椅配色都是编的。这三张是「照片级写实的真实建筑航拍」，属于第 1 轮建议的选图顺序第 4 条明确不推荐的用法。现在靠 AI IMAGE 角标、「not a photo」署名和上传时的合成内容声明来兜底，不算误导到必须修的程度 | 维持也可以，但建议用户知情后拍板。更稳的做法：重新生成时去掉可辨认的城市天际线和地标（广州塔、钱江新城），或者在 publish.md 里注明「3 AI images depict real stadiums from public descriptions; details are not accurate」。只要这三国（中、土）有可商用实拍出现，就优先换回实拍 |
| N4 | minor | 两版 | 来源卡 362.5 s | 第 1 轮 M2 建议的「6 cards use AI images, not photos」没有加，来源卡只写「Image credits: shown on each card…」 | 有渲染器支持的话加上；没有就靠卡上角标和描述框，可接受 |
| N5 | 说明 | 风险 | 风险版 manifest | 风险版 05:24 渲染，之后 data.json 和 assets.json 在 05:28 又改过（加了 3 张 gen2 外观图），所以 manifest 记录的这两个哈希与当前文件不一致。风险版实际用到的 50 张图（含 #20、#41、#34、#12 新图）哈希全部与当前一致。抽帧看到的洞察卡（Beaver、80,000）、徽章、#50 停留时长都和当前数据一致。gen2 只挂在 image_alt 上，风险模式用不到，所以预计画面没有差异，没有逐帧比对 | 修 N1 时两版都要重渲，重渲后自然恢复一致 |

### 成片技术核对（本轮）

| 项 | 默认版 | 风险版 |
|---|---|---|
| 编码 / 分辨率 / 帧率 | H.264，1920×1080，60/1 | 同左 |
| 时长 | 382.600 s（容器 = 视频流 = 音频流） | 同左 |
| 帧数 | nb_frames 22,956；`-count_frames` 实数 22,956 | 22,956 / 22,956（见 `decode_*.log`） |
| 与 `rank_scroll timeline` 一致 | total 382.60 s，22,956 帧：intro 0–5、scroll 5–347.6、champion –353.6、tally –360.6、sources –364.6、end –382.6，与 manifest 一致 | `--allow-risk-images` 重算结果相同 |
| 全片解码 | `ffmpeg -v error -f null` 退出码 0，无报错 | 退出码 0，无报错 |
| manifest 输入 | 49 项（data、assets、47 张图）全部与当前文件一致 | 52 项中 data.json、assets.json 两项不一致（N5），50 张图一致 |
| `rank_scroll validate` | OK（只有 3 条 FoP 无图卡的预期 warning） | OK |

数据机检（第 1 轮的 `_build/qc/data_check.py` 重跑）：50 条按 value 降序，名次连续性和并列（#28 ×2、#36 ×5）全部正确；value_display 一致；洞察卡 73–90 字符（Azteca 那张正好 90，抽帧显示完整）；6 张洞察卡的 after_rank（41、31、22、11、5、3）都落在对应两张卡之间，「Next: Azteca」紧挨着 #21，「Next: Beaver」紧挨着 #4。国家计数 US 25、CN 3……与计分板帧（357 s）一致。没有发现文字出框、截断或占位卡（JIS 无图卡的说明文字只在卡片滚到屏幕边缘时被切，居中时完整）。

---

## 第 1 轮独立审片 · 2026-11-04

> 独立审片人（另起上下文，未参与制作）。只写本文件和 `_build/qc/` 下的文件，没有改数据、图片或渲染。
> 审片对象：默认版 `render/ep16_largest_stadiums_master.mp4`（sha256 7bee911e…），风险版 `render/ep16_largest_stadiums_master_with-risk-images.mp4`（sha256 b405aa62…）。两版的 sha256 都与各自 manifest 的 output_sha256 一致。manifest 记录的 52 项输入（data.json、assets.json、50 张上屏图）与当前文件逐个比对，全部一致，渲染后没有被改过。

### 结论：**必须修**（两个版本当前都不能发布）

- **默认版**有 1 个 blocker：#34 Estadio Monumental（秘鲁）用的替代图拍的是另一座球场 Estadio Nacional de Lima。另有 5 个 major，最重的是「卡片不显示球场本身」：50 张卡里有 17 张（34%）看不到这座球场，其中 0:36–1:51 这一段连着 13 张卡里有 9 张。
- **风险版**另外还有 2 个 blocker：#20 Jordan–Hare 和 #41 Bernabéu 用的是建筑效果图（CG render），不是实拍。#20 那张画的还是尚未建成的改建方案。
- 帧数完整，技术层面通过（见「成片技术核对」）。

### 问题清单

| # | 严重度 | 版本 | 位置 | 问题与证据 | 建议修法 |
|---|---|---|---|---|---|
| B1 | **blocker** | 默认 | #34 Estadio Monumental（Lima），1:51（111.0 s 居中） | `34_estadio_monumental_lima_alt.jpg` 的 Flickr 来源页标题是「**Estadio Nacional de Lima** \| Christian Córdova」。画面里的莲花火炬塔和喷泉是国家体育场和旁边 Parque de la Reserva 的「魔幻水上公园」，不是大学体育俱乐部（Universitario）的 Monumental「U」。秘鲁观众一眼就能认出来。publish.md 第 34 条署名也跟着错了 | 换一张真正的 Monumental「U」可商用照片。Flickr CC 搜「Estadio Monumental Universitario / Ate」，只用标题或描述写明 Monumental 的图。找不到就先用无图卡，不要用别的球场顶替。同步改 assets.json、publish.md 署名，然后重渲 |
| B2 | **blocker**（风险版） | 风险 | #20 Jordan–Hare，3:29（209.0 s） | `20_jordan_hare_stadium.jpg`（取自 on3.com「Auburn formally approves Jordan–Hare renovation」）是**改建方案效果图**：新西塔楼、广场和秋景都是 CG，现在的球场长得不一样（`_build/qc/s20.jpg`） | 换成现状实拍。或者风险版这张直接沿用默认版的 CC 替代图（Auburn 正立面，许可没问题） |
| B3 | **blocker**（风险版） | 风险 | #41 Santiago Bernabéu，1:02（62.0 s） | `41_santiago_bernabeu.jpg`（取自 arup.com 项目页）是 2019 年 GMP / L35 / Ribas 设计方案的夜景**效果图**，屋顶上的「Realmadrid」字样和广场都是渲染出来的（`_build/qc/s41.jpg`）。当作「现状照片」上屏属于货不对板，效果图还是事务所的版权作品 | 换成 2024–2026 年完工后的实拍（西班牙有全景自由，可以找 CC 图）。同时可以替换掉默认版的 AI 图（见 M1） |
| M1 | **major** | 默认 | 0:36–1:51 最集中；全片共 17 卡 | **默认版有 17/50 张卡看不到这座球场**：11 张 AI「球迷背影」示意图（#6、13、18、22、28 JIS、35、36 杭州、36 法兰西、41、42、45）；5 张实拍对象没错但球场不在画面里或认不出来（#12 FNB 只有球迷特写、#36 Martyrs 是场内「Stop au recrutement d'enfants」横幅仪式、#43 GBK 是持旗残疾人运动员竖幅、#50 Camp Randall 是球员冲撞近景、#2 五一体育场只拍到一角弧顶加花坛）；再加 B1 的错图。#45→#35 这 13 张卡里 9 张不是球场本身，正好落在完播最敏感的第 1–2 分钟。11 张 AI 图构图几乎一样（大旗＋后脑勺＋草皮），会显得「AI 图库」。杭州那张背景还是真实的钱江新城天际线，球场本身却是编的，观众会以为这就是大莲花。题目叫「世界最大体育场」，观众要看的是球场，这就是货不对板 | 按本节下面的「这类题默认版用什么」处理。最少要做到：①**所在国有全景自由的 5 张 AI 卡（Tiger、广东奥体、杭州奥体、Bernabéu、Atatürk）必须换成实拍**。这几张用 AI 不是因为版权，是因为 Flickr 限流没搜完（handoff §没解决的问题 5），重跑 `prefetch.py --only 40,44` 等补搜就行。②FNB、Lusail、Stade de France 三张已经有许可干净的 CC / PD 实拍，只差 FoP 风险，请用户逐国决定是否放行；放行后 AI 卡从 11 张降到 3 张。③#50、#43、#12、#36 Martyrs、#2 换成能看到球场主体的图 |
| M2 | **major** | 默认 | 11 张 AI 卡 | 默认母版是 01:05 开始渲的，早于渲染器 02:41 合入的 follow-up 010，所以 **AI 卡没有黄色「AI IMAGE」角标**，署名行写的是「**Photo:** AI-generated illustration (Codex)」，用的还是 Photo 前缀（例：36.67 s Atatürk、55.67 s Azadi）。手机上 14 px 的小字基本看不见，写实风格的 AI 球迷图会被当成真实照片 | M1 修完后剩下的 AI 卡，用当前渲染器重渲就会自动出「AI IMAGE」角标，署名改为「AI-generated image, not a photo」（ep17 已验证）。来源卡加一行「N cards use AI illustrations, not photos」 |
| M3 | **major** | 两版 | #4 Beaver Stadium，5:18（318.0 s） | 屏上写 106,304 和「-268 SEATS VS 2024」，统计行却是「Official seats, Nov 2026」。实际情况：2026 赛季加了西侧上层看台，AD 公开预估约 108–109k；**2026-10-10 对 USC 的比赛上座 114,419，创队史纪录**（Daily Collegian 报道，Wikipedia infobox 已更新）。片子写的是 2025 年的官方数，徽章暗示球场在缩小，评论区一定会有人纠错。另外，口径说「临时看台不算」，但 106,304 本身据 SI 报道就含约 9,000 个临时 bleacher 座，口径前后不一致（未逐字核原文） | 用户在 topic.md「待确认 2」里定。两条路选一：①保留 106,304，徽章改为「2026 TEMP SEATS NOT COUNTED」或「2025 OFFICIAL」，scope_note 写清楚；②在 #3/#4 之间加一张洞察卡：「Beaver drew 114,419 on Oct 10, 2026 with temporary seats — more than its official capacity」。这本身就是个反常识的亮点。两条路都要重渲 |
| M4 | **major** | 两版 | 洞察卡 after 41，1:07（67.5 s） | 「Five stadiums tie on **exactly** 80,000 seats」。这 5 个都是整数标称值，不是精确座位数：Stade de France 官网写「80,000 spectators in football and rugby configuration」，但广泛引用的精确数是 80,698；鸟巢、杭州、AT&T、Martyrs 也都是取整的数。「exactly」站不住 | 改为「Five stadiums list a round 80,000 seats: in China, France, the USA and DR Congo.」（≤90 字符）。sources.md §2 补 SdF 80,698 这个版本 |
| M5 | **major** | 两版 | #50 Camp Randall，0:03.8–0:05.6 | data.json 没设 `layout.intro_hold`，#50 卡滑入后马上开始左移：4.3 s 左右才停稳，5.6 s 左边文字就开始出框（见 7.5 s 帧里的「dall Stadium」），完整可读时间约 1.5 s，不到 bible §7-5 要求的 3 秒。偏偏这张卡就是那个「只差 5 座」的第 50 名 | `layout.intro_hold: 2.5`（同 ep17 M5 的修法），重渲后时长 +2.5 s，章节时间同步顺延 |
| M6 | **major** | 包装 | `render/thumbnail.png` | 封面直接放了 #1 132,000，和 Vision「看到最后才知道冠军」相冲突。#2 那张是花坛加弧顶一角，#3 是观众背影，三张都看不出是「世界最大的球场」，点击率风险大 | 封面不写 #1 的名次和数值（例如改成「#1 ?」），选 2–3 张最震撼的满场俯拍（如 Michigan、Neyland 格子看台、MCG 夜景）。所选图必须是默认版里许可干净的那几张 |
| m1 | minor | 两版 | #50 徽章 | 「+73 SEATS VS 2024」：Wisconsin 2026 game notes 年表 2024 = 76,057、2025 = 76,030、2026 = 76,130，和上一年比是 +100。同一份 PDF 的 Quick Facts 写「Current capacity: 76,057」，正文写 76,030，官方文件自己就不一致（已下载核对） | 徽章改「+100 SEATS IN 2026」，或者干脆去掉。sources.md 已注明 76,057 / 76,030 两个版本，这条保留；发布前 7 天复核一遍 Wisconsin 设施页 |
| m2 | minor | 两版 | 第 51 名 Empower Field 76,125 | 只有第三方来源（Walter P Moore、Ticketmaster、StadiumDB 一致），没找到 Broncos 官方页 | 发布前再找一次 Broncos 2026 media guide。如果官方数 > 76,130，第 50 名就要换 |
| m3 | minor | 两版 | #21 Azteca 87,500 | AP 写 87,500，IQ Magazine / StadiumDB 写约 90,000，墨西哥城官方场馆页写 87,000 | 维持 AP，在 sources.md §2 补 90,000 / 87,000 这两个版本（取 90,000 的话也还是第 21 名） |
| m4 | minor | 两版 | #41 Bernabéu 78,297 | 皇马没有公布官方数，78,297 来自 2030 世界杯申办书（经 StadiumDB 转述），处理方式和依据都合理，但屏上看起来和其他「官方数」没有区别 | 可以加徽章「CLUB FIGURE UNPUBLISHED」，或者在 scope_note 里点一句 |
| m5 | minor | 两版 | 洞察卡 after 31 | Camp Nou 62,652 是 2026-03 拿到的 Phase 1C 许可数；到 11 月可能已经开放了第三层 | 发布前复核当期容量（只要还 < 76,130，结论不变） |
| m6 | minor | 默认 | #15 Cotton Bowl，4:00 | 外立面图裁成竖卡后，招牌只剩「TON BOW」，海报还压在主体上 | 设 `image_focus` 让完整招牌入画，或者改用场内图 |
| m7 | minor | 默认 | #21、#25、#5、#49 | 替代图是改建前的旧貌：Azteca 是 2010 年的样子（卡上写 REOPENED 2026），River Plate 2011 年还有跑道（卡上写 EXPANDED 2024），Kyle Field 是 2006 年改建前，Razorback 是 2007 年 | 有更新的 CC 图就换；没有的话可以保留 |
| m8 | minor | 默认 | #1 冠军卡 345–351 s | Pexels 原图只有 1000×750，放大到 763×848 后偏软；冠军停留的 6 秒最显眼。账本作者写的是「pexels.com contributor」，没有记真实作者 | 换 ≥2000 px 的图，账本补上作者 |
| m9 | minor | 默认 | #36 Martyrs | MONUSCO 反童兵招募的宣传横幅出现在「最大体育场」卡上，语境不对 | 并入 M1 一起换图 |
| m10 | minor | 风险 | #34、#35、#47 | 原图带水印：TFC Stadiums 角标、新华网「WWW.NEWS.CN」、摄影师签名「kla4067 PHOTO」。抽帧 111.0 / 104.67 / 24.0 s 确认三处都被卡片裁掉了，屏上看不到。但新华网的图是通讯社版权图，风险版签字时要特别注意 | 在账本 `fop_note` 或备注里写明有水印，签字时一并考虑 |
| m11 | minor | 风险 | #13 Misr、#12 FNB | Misr 的风险图 1024×665，像视频截图，我无法独立确认是不是 Misr 球场；FNB 的风险图是 2009 年施工中的样子（周围还是工地） | 签字前再核一次；FNB 有完工后的 CC 图可以换 |
| m12 | minor | 包装 | publish.md | 署名写成「AI-generated (AI-generated (Codex image_gen))」，重复了；第 34 条署名跟着 B1 错了；章节「5:41 No. 1」比冠军居中的 5:45 早 4 秒（可以接受） | 改完重跑 `rank_scroll publish` 再人工补写。intro_hold 改了以后章节整体 +2.5 s |
| m13 | minor | 两版 | 音轨 | 两版都是静音 AAC（volumedetect：mean/max −91 dB，来自 anullsrc），没有配乐。bible §5 要求有配乐，handoff 已说明是静音母版 | 配乐另行制作。本轮没有配乐版，不做听感检查 |

### 用户点名的几个问题，逐条回答

**1. 默认版那 30 张「可商用替代图」到底是什么？**
逐张打开了 Flickr / Pexels 来源页，用标题和描述核对拍摄地点：
- **28 张是该球场本身的照片**。Flickr 标题或描述写明了球场名的有：Michigan、Beaver、Ohio、Neyland、DKR、Bryant–Denny、MCG、Sanford、Cotton Bowl、BHG、Jordan–Hare、Azteca、Accor（ANZ Stadium）、MetLife、Clemson、Lambeau、Luzhniki、Oklahoma、AT&T（「view to Cowboys Stadium from the parking lot」）、Notre Dame、Williams-Brice、Arrowhead、Razorback、Camp Randall、Rungrado、FNB（Soccer City 揭幕战）、Stade des Martyrs（2017-06-10 CAN 预选赛，Martyrs）、GBK（2018 亚残运会）。Modi 那张是 Pexels，页面有反爬，URL slug 是「aerial-view-of-narendra-modi-stadium-in-ahmedabad」，画面也对得上。
- **1 张是别的球场冒充**：#34 用 Estadio Nacional de Lima 冒充 Monumental「U」→ blocker B1。
- 没有发现拿泛体育图库或别的城市球场冒充的情况。问题出在另一面：有 4 张地点对了，球场却不在画面里（FNB 球迷、Martyrs 仪式、GBK 运动员、Camp Randall 球员），另有 2 张很弱（Rungrado 花坛、BHG 外立面局部）→ 归入 M1。

**2. 11 张 AI「球迷示意图」会不会让人觉得货不对板？**
会，而且很明显。这类题的产品就是「看那座球场」。11 张同一模板的「后脑勺＋国旗」把 22% 的卡变成了可以互换的素材图，第 1–2 分钟密度最高（见 M1）。其中 5 张（Tiger、广东、杭州、Bernabéu、Atatürk）所在国有全景自由，换实拍没有任何法律障碍，用 AI 纯属找图没做完。另外，用写实风格去「编」一座真实存在的球场（杭州那张还配了真实天际线），比用占位卡更容易误导观众。

**建议：这类「真实建筑 / 地标」题，默认版按下面的顺序选图**
1. **该建筑本身的可商用实拍**：外观俯拍或满场全景优先。Flickr CC 一轮被限流就分批重跑，再补 Unsplash / Pexels / Openverse。这一步要做完，才能进下一步。
2. **全景自由风险国，请用户逐国决定**。如果图片本身许可干净（CC / PD），只差 FoP 风险（本期的 FNB、Lusail、Stade de France 就是这样），这是个法律风险偏好问题，交给用户签字，不要由代理默认换成 AI。
3. 用户不放行 FoP 的，用**诚实的非照片卡**：例如按 OpenStreetMap 轮廓（ODbL，需署名）画的球场平面示意加城市定位，或者主题色无图卡写明「Photo withheld: no freedom of panorama in Egypt」。这样观众知道缺图的原因，不会被骗。
4. AI 图放到最后，只给「整体氛围」用：不画可辨认的建筑和城市天际线；画风明显非照片；必须带「AI IMAGE」角标；每期上限建议 ≤3 张，并且不能连续出现。
本期按这个顺序做，AI 卡预计可以从 11 张降到 0–3 张。

**3. 容量数值的出处与口径**
- **Beaver 106,304**：数字有出处（Georgia 2026 媒体指南容量表、Wikipedia infobox「106,304 (2025–present)」），但它是 2025 年的数。2026 赛季已经有临时上层看台，2026-10-10 上座 114,419。屏上的「Nov 2026」和「-268」都会招来纠错 → M3。
- **Bernabéu 78,297**：皇马没有公布官方数。这个数出自 2030 世界杯申办书和 FIFA 评估（经 StadiumDB 2026-03 文章转述），和 2025/26 最高上座 78,107 吻合。其他版本有 80,000±1,000（Pérez）、83,186（LaLiga 2023 技术容量）、84,000。选 78,297 合理，sources.md 也写清楚了；建议屏上或描述框点明「俱乐部未公布」→ m4。
- **五一体育场 114,000 est.**：StadiumDB 的估算，2014 年改建后朝方没有公布新数；StadiumDB 还说「官方」口径仍是 150,000。卡上写「seats, est.」、挂 ESTIMATE 徽章、配洞察卡说明，处理得当。小问题：sources.md 写的 Wikipedia 113,281 我没检索到，不影响结论。
- **第 50 / 51 名只差 5 座**：Camp Randall 76,130 我下载了 Wisconsin 2026 game notes（GM9 vs Rutgers）核对，年表里 2026 那一行确实是 76,130；但同一份 PDF 的 Quick Facts 写 76,057，正文写 76,030，官方文件自相矛盾。Empower Field 76,125 只有第三方来源。这个第 50 名两边都不稳：①如果按 Quick Facts 的 76,057 算，Camp Randall 会跌到第 51，Empower 上榜；②徽章「+73 vs 2024」口径奇怪 → m1、m2。建议在描述框或置顶评论里主动说明「#50 vs #51 differ by 5 seats per Wisconsin's 2026 game notes」，把争议变成互动点。

**4. 每张实拍是否认对了球场**
- 默认版 9 张原图实拍全部正确（Kyle、Wembley、Rose Bowl、Bukit Jalil、Nebraska、River Plate、Twickenham、Bird's Nest、LA Coliseum），30 张替代图的情况见第 1 问。
- 风险版 41 张：对象都是对应的球场，但 #20、#41 是效果图（B2、B3）；#13 Misr 无法独立确认（m11）；#26 Accor 那张全景放大看过，是实拍。

**5. 帧数是否完整**：完整，见下表。风险版是重渲后的新文件，全片解码 0 错误。

### 成片技术核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 编码 / 分辨率 / 帧率 | H.264，1920×1080，60/1 | 同左 |
| 时长 | 380.100 s（容器 = 视频流 = 音频流） | 同左 |
| 帧数 | nb_frames 22,806；`-count_frames` 实数 22,806 = 380.1 × 60 | 22,806 / 22,806 |
| 全片解码 | `ffmpeg -v error -f null` 退出码 0，无报错（`_build/qc/decode_master.log`） | 退出码 0，无报错（`decode_master_with-risk-images.log`），确认之前写坏的那版已经被替换 |
| 时间线 | intro 0–5、scroll 5–345.1、champion –351.1、tally –358.1、sources –362.1、end –380.1，与渲染器 `timeline.build` 重算一致 | 同左 |
| 渲染日志 | render_master.log「done in 5548s」；风险版 render_risk2.log「done in 4683s」与 manifest 的 render_seconds 4683.3 对应 | — |
| output sha256 | 与 manifest 一致 | 与 manifest 一致 |
| 音轨 | AAC 静音（−91 dB） | 同左 |

数据机检（`_build/qc/data_check.py`）：50 条按 value 降序；名次按「严格更大的条数 + 1」重算，全部吻合（82,000 并列 #28 后接 #30，80,000 五座并列 #36 后接 #41）；value_display 与 value 一致；徽章 ≤22 字符，tag ≤24 字符，洞察卡 ≤90 字符；国家计数 US 25 · CN 3 · AU/EG/GB/ID 各 2 · 其余 14 国各 1 = 50，和片尾计分板帧（354.0 s）一致；iso2 与国名全部对应，抽帧里的国旗都正确（朝鲜、刚果（金）、伊朗、卡塔尔、马来西亚都看过）。

### 核对过的数据样本（亲自检索或下载原文件）

| 名次 | 球场 | 片中值 | 我的核对 | 结论 |
|---|---|---|---|---|
| 1 | Narendra Modi Stadium | 132,000 | bcci.tv/venues 页面源码有「1,32,000」，并写「The 132,000-capacity venue」 | ✓ |
| 2 | Rungrado May Day | 114,000 est. | StadiumDB 写 114,000（估算），并说明官方口径仍是 150,000；无朝方新数 | ✓（作为估算） |
| 3 | Michigan Stadium | 107,601 | mgoblue.com 设施页源码有 107,601 | ✓ |
| 4 | Beaver Stadium | 106,304 | 2025 年的数，确认；但 2026 年有临时看台，10-10 上座 114,419（Daily Collegian） | ⚠ M3 |
| 5 | Kyle Field | 102,733 | 12thman.com 设施页源码有 102,733 | ✓ |
| 7 | Ohio Stadium | 102,041 | 下载 2026 game notes PDF：「Capacity 102,041」「Present Capacity 102,041」 | ✓ |
| 11 | MCG | 95,000 | 多方转引 MCG：100,024 =「约 95,000 座 + 5,000 站位」 | ✓ |
| 21 | Estadio Azteca | 87,500 | AP 87,500；IQ / StadiumDB 约 90,000；CDMX 87,000 | ⚠ m3 |
| 23 | Bukit Jalil | 85,500 | stadium.gov.my 页面「Seating capacity: 85,500」 | ✓ |
| 36 | Stade de France | 80,000 | stadefrance.com「80,000 spectators in football and rugby configuration」；广泛引用 80,698 | ✓（洞察卡 M4） |
| 41 | Bernabéu | 78,297 | StadiumDB 2026-03：申办书数字，俱乐部未公布 | ⚠ m4 |
| 43 | Gelora Bung Karno | 78,000 | gbk.id「Kapasitas Tempat Duduk: 78.000」（另写「± 78.000」） | ✓ |
| 50 | Camp Randall | 76,130 | 下载 GM9_RUT.pdf：年表 2026 = 76,130；Quick Facts 写 76,057 | ⚠ m1 |
| 51 | Empower Field（出榜） | 76,125 | Walter P Moore / Ticketmaster / StadiumDB 一致，未找到官方页 | ⚠ m2 |
| 洞察卡 | Indianapolis Motor Speedway | ~235,000 | Guinness：2013 年起常设座位 235,000（原 257,325） | ✓ |
| 洞察卡 | Camp Nou | 62,652 | 2026-03 Phase 1C 许可 62,652（Catalan News 等） | ✓（m5 复核） |
| 洞察卡 | 8 of top 10 US college | — | #3–#10 都是美国大学球场，#1、#2 是印度和朝鲜 | ✓ |
| 洞察卡 | Azteca 三届揭幕战 | — | 1970、1986、2026 | ✓ |

### 图片核对

- 全部 91 张上屏图（50 张主图 + 41 张 image_alt）的 sha256 与 assets.json 一致，尺寸见 `_build/qc/ledger.py` 的输出。
- 拼图：`_build/qc/contact_01…13.jpg`（每行左边是主图 / 风险图，右边是默认版替代图）；`_build/qc/gen_sheet.jpg`（11 张 AI 图）；单张放大：`s01 / s20 / s26 / s34a / s36m / s41.jpg`。
- 来源页标题核对：`_build/qc/source_titles.txt`（Flickr / Pexels / Unsplash 共 40 页）。
- AI 痕迹：11 张 AI 图都在账本里标了 AI-generated。国旗画得基本正确，埃及、伊朗国徽画得比较粗；广东那张旗子是纯红色、没有五星。没有看到可辨认的正脸。

### 抽帧清单（`_build/qc/frames/`）

- 默认版（m_*.png，45 帧）：片头 2.5 / 3.8 / 4.6 / 5.4 / 6.0 / 6.6 / 7.5 s；6 张洞察卡 18.5 / 67.5 / 135.5 / 197.17 / 271.5 / 330.57 s；第 50 名 4.6–6.6 s；第 11 / 10 名 266.0 / 277.23 s；#2 336.3 s；冠军 345.1 / 348.5 / 351.0 s；计分板 354.0 / 357.9 s；来源卡 360.0 s；片尾 364.0 / 372.0 / 379.9 s；11 张 AI 卡与 #34 36.67 / 55.67 / 79.33 / 85.67 / 104.67 / 111.0 / 153.67 / 191.67 / 221.67 / 253.33 / 304.43 / 318.03 s；随机 27.3 / 98.33 / 147.33 / 166.33 / 209.0 / 240.67 / 259.67 / 290.83 s。
- 风险版（r_*.png，16 帧）：2.5、24.0、62.0（Bernabéu 效果图）、73.0、104.67、111.0、160.0、209.0（Jordan–Hare 效果图）、228.0、253.33、290.83、336.3、348.5、357.9、360.0、379.9 s。
- 每 3 s 一帧的全片缩略：`_build/qc/strip_m_sheet1–4.jpg`、`strip_r_sheet1–4.jpg`。
- 拼版：`_build/qc/m_sheet_*.jpg`、`r_sheet_*.jpg`。
- 看到的结果：没有文字出框、截断或省略号（长名「Jakarta International Stadium」「Rungrado May Day Stadium」在居中时都完整；卡片在屏幕边缘被切，是滚动造成的，正常）；没有占位卡；国旗全部正确；冠军光晕和右侧「No. 1 · 132,000 seats」正确；计分板 US 25 压轴，与数据一致；来源卡没写 AI 图（M2）。

### 包装（publish.md）

- 标题「Top 50 Largest Stadiums in the World (2026)」43 字符 ✓。
- 描述框有口径、来源、逐图署名、「11 images marked AI-generated are illustrations, not photos」✓；置顶评论 2 条，分别列逐条数据来源和完整许可链接 ✓；「Altered or synthetic content → Yes」写进了 checklist ✓。
- 要改的：#34 署名（B1）；AI 署名重复的文字（m12）；改了 intro_hold 后章节时间要重算；封面（M6）。

### 观众视角（全球英文观众）

- **亮点够**：美国大学球场霸榜（8/10，「没有一座 NFL 主场」）、印度板球场登顶、朝鲜只有估算数、赛车场 23.5 万座不计入、Camp Nou 缺席，都是反常识、能引发评论的点。M3 的 Beaver 2026 年 114,419 上座，如果做成洞察卡会是新的亮点。
- **会在哪划走**：第 1 分钟前后（#45–#35），观众连着看到 AI 球迷图、跑道上的运动员、球场外的仪式、还有一张认错的秘鲁球场，会觉得「这频道没有真图」，这是本期最大的流失点。静音成片也会拉低完播。
- **会在哪吵起来**：Beaver（「它今年已经 11 万+」）、MCG（「100,024」）、五一（「150,000」）、Bernabéu（「83,186 / 85,000」）、Dortmund 和 Croke Park 没上榜。口径说明已经写在片头和描述框；建议置顶评论预先回应这几处。

### 修复后需要复核的项

B1–B3、M1–M6 修完后重渲两版，复核：①#34、#20、#41 三张新图的来源页；②17 张「看不到球场」的卡逐张重看；③AI IMAGE 角标；④#50 可读时长 ≥3 s；⑤Beaver 徽章或洞察卡；⑥80,000 那张洞察卡的措辞；⑦帧数和解码；⑧publish.md 章节与署名；⑨封面。
