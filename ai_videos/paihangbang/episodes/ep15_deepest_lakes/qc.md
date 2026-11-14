# ep15 · 独立审片记录（qc.md）

## 复核 · 2026-11-04（返修后，独立上下文）

> 复核人没有参与制作，也没有参与第 1 轮审片。核对对象是当前的 `data.json`、`assets.json`、`sources.md`、`topic.md`、`publish.md`、`publish_with-risk-images.md`，以及 `render/` 下两版重渲后的成片。两份 manifest 各有 37 个输入，sha256 与当前文件全部一致，所以成片对应的就是当前数据。没有调用收费服务；只用 WebFetch 打开了 2 个 Flickr 来源页。抽帧放在 `_build/qc/recheck/`：`m_*` 是默认版，`r_*` 是风险版，`ch_*` 是章节时间点，`src_*` 是换掉的原图，2×2 拼图在 `grids/`。

**结论：可发布，推荐发布默认版**（`render/ep15_deepest_lakes_master.mp4` + `publish.md`）。第 1 轮的 2 个 blocker、4 个 major 都已修好，没有引入新的 blocker 或 major。剩下的都是 minor（见文末清单），不影响发布，可以在上传时或下期顺手改。

**为什么推荐默认版**
- 默认版 35 张图都是可商用照片或标明的生成图（25 张实拍 + 10 张 AI 生成），可以直接发。
- 风险版有 7 张许可不明的照片，必须用户签字后才能用。
- 风险版主要换掉的是默认版的生成图，但这几张不在前 10，换掉对观感帮助有限。唯一在前 10 的风险图是 #8 Great Slave 的 East Arm 悬崖图，比默认版的好看，但默认版现在的图也能看清湖面。
- 风险版描述框会公开写出 4 处「unknown (unknown)」署名（见 N3）。

### 技术核对（两版相同）
- ffprobe：1920×1080，60/1 fps，h264 yuv420p，逐帧计数 **16,976 帧**，时长 282.933 s。音轨是 aac 静音，与 manifest 一致。
- `python -m rank_scroll timeline`：总长 282.93 s，16,976 帧。分段为 intro 0–5、scroll 5–247.93、champion –253.93、tally –260.93、sources –264.93、end –282.93，与帧数一致，没有截断。
- `validate --strict`：默认版、`--allow-risk-images` 两版都 OK（35 items，5 insights）。
- `assets.json`：42 条记录的 sha256 与文件一致。

### 原问题逐条

| 编号 | 原问题 | 复核结果 | 依据 |
|---|---|---|---|
| B1 | Wakatipu 420 m 无出处，应出榜 | **已修** | `data.json` 现为 35 项，kicker 为 `TOP 35`，#33 Khantayskoye / #34 Grey / #35 Superior。`sources.md` §3 排除表写明 LINZ 376 m、MfE/LAWA/NZJMFR 380 m。计分板 Asia 9 / NA 8 / SA 7 / Europe 5 / Africa 3 / Oceania 3，我逐项复数一致，成片 257 s 帧也一致。Poso 洞察卡改成合并说两湖（86 字符，40 s 帧可读）。Hauroko、Manapouri 的出处已不再写 Lowe & Green。标题、描述、topic 都改成 Top 35。 |
| B2 | #5 Viedma 主图不是 Viedma | **已修** | 新图是 Flickr「Glacier Viedma and Lago Viedma」（Su--May）。我打开来源页确认：许可 CC BY 2.0，作者说明是坐游船去冰川。原图底部有湖面，卡上主要是冰川前缘和群峰（`m_214.1`）。认湖没有问题。 |
| M1 | #8 Great Slave 默认图看不到湖 | **已修** | 新图是 Flickr「Great Slave Lake in Yellowknife」（Alan Sim），来源页确认许可 CC BY-SA 2.0。卡上大片湖面和对岸林线清楚（`m_189.0`）。前景仍有一块「Public Dock」小告示牌和一个蓝顶垃圾箱，观感偏平，但不占主体。 |
| M2 | #36 停留不足 3 秒 | **已修** | `layout.intro_hold = 2.5`。抽帧 4.6 / 5.5 / 7.0 / 7.5 s 时首卡 #35 完全静止，8.5 s 才开始移动，9.2 s 时名称和数值仍完整（`m_004.6`–`m_009.2`）。可读约 3.5 s。 |
| M3 | 风险版 4 张「版权所有」图与「licence unknown」署名 | **已修** | #3、#4、#22 Cochrane、#28 的风险图已撤下，文件与默认图逐字节相同（md5 一致），`sources.md` 已注明。风险版卡面署名只写作者或站名，例如「Photo: volda.kommune.no」「Photo: J. Hipfner」，成片里没有「licence unknown」字样（`r_*`）。描述框的写法另见 N3。 |
| M4 | publish 章节需要重新生成 | **已修** | 两份 publish 的章节都是 0:00 / 0:28 / 1:42 / 2:55 / 4:03 / 4:14，与生成器按当前时间线复算的结果一致。按时间点抽帧核对（`ch_*`）：0:28 时 #30 居中；1:42 时 #20 居中；2:55 时 #10 居中；4:03 时 #1 已进场；4:14 时是计分板。相邻章节间隔都 ≥ 10 s。「已手改」那一行已删除。 |
| m1 | Viedma 洞察卡措辞与测深年份 | 已修 | 卡上文字为「…reported 900 m (unpublished); peer-reviewed sonar: ~750 m.」，86 字符；`sources.md` 测深年份改为 2017-01 至 2020-06。 |
| m2 | 改正旧值的标签被挤掉 | 已修 | 成片里能看到「Survey 2020 (was 836 m)」「2022 claim: 900 m」「Often listed as 719 m」「Often listed as 702 m」「Echo sounding (was 464)」（`m_182.2`、`m_195.8`、`m_214.1`、`m_220.9`、`m_115.2`）。 |
| m3 | #7 Issyk-Kul 看不到湖 | **部分修** | 换成了 Pexels 黄昏湖面图（Nizar F）。原图下半是湖面，但卡上是默认居中裁切，上 2/3 是空的灰蓝天，远山只剩一条细线，湖面大半被数值块盖住（`m_195.8`）。前 10 里这张最弱。建议设 `image_focus: [0.5, 0.8]`。 |
| m4 | #3 里海国旗与默认图偏弱 | 部分修 | 描述框已加里海最深点在南里海的说明。默认图仍是阴天灰色礁石，而且仍在封面里。 |
| m5 | AI 图雷同、扎堆 | 未修（已知） | 默认版仍有 10 张生成图，都标了 AI IMAGE 黄色角标，署名也写明（见下）。等 Flickr 限流解除后再换。 |
| m6 | #20 Nahuel Huapi 视角 | 未改 | 可接受。 |
| m7 | Tazawa / Te Anau 来源页地点未核 | 未改 | 发布前人工点开来源页确认一次。 |
| m8 | Great Bear 标签 | 已修 | 卡上为「Largest wholly in Canada」（`r_051.8` 完整可见）。 |
| m9 | after 2 洞察卡点名冠军；封面写出 #1–#3 | 洞察卡已修；**封面未修** | 洞察卡改成了「Next, No. 1: a lake holding…」。`render/thumbnail.png` 仍是 #1 Baikal / #2 / #3 三张图并写出名次与数值，提前揭晓冠军。上传时请人工换封面。 |
| m10 | O'Higgins 原图分辨率低 | 未改 | 可接受。 |
| m11 | sources 记录小错 | 已修 | Poso 正文 PDF 已补抓（`poso_tournier2025_main.pdf`）；De Batist 年份改为 2001。 |
| m12 | 置顶评论里 AI 图写的是本地路径 | 已修 | 改为「generated for this video (Codex image_gen)」。 |
| m13 | 成片静音 | 未改（已知） | 两版仍是 anullsrc。 |
| m14 | 时长低于 5 分钟 | 未改（已知） | 现为 4:43。 |

**AI IMAGE 角标**：默认版 10 张生成图（#11、#13、#14、#18、#21、#22 Cochrane、#22 Tinn、#24、#28、#33）抽到的帧里都有黄色「AI IMAGE」角标，并署名「AI-generated image (not a photo)」。风险版的 4 张生成图（#18、#22 Cochrane、#28、#33）也都有。实拍卡上没有误标。publish 上传清单要求勾选「Altered or synthetic content」。

### 新问题检查
- 名次连续性：ranks 依次为 1–15、15、17–22、22、24–25、25、27–30、30、32–35。四组并列（Toba / Sarez 505、Cochrane / Tinn 460、Chelan / Mjøsa 453、Como / Te Anau 425）都按 1,1,3 式跳号，正确；末名 35 = N。
- 洞察卡位置：after 30（Poso / Wakatipu）在 #30 Como 之后、#29 前（40 s）；after 17 后面紧接 #15 Sarez；after 11 在 #10 前；after 6 后面紧接 #5 Viedma；after 2 后面紧接 #1。卡上内容与相邻的卡对得上，没有错位。
- 文字出框：抽到的 49 帧里，名称、数值、标签、徽章、署名都没有出框或省略号。最长的「Lago Cochrane / Pueyrredón」「Lago O'Higgins / San Martín」也完整显示。
- 随机抽查 44.3、120.2、178.1、215.4、261.4 s：都正常。

**新发现的 minor**
- **N1**：#5 Viedma 新图、#4 O'Higgins、#9 Argentino 三张都是近景冰川前缘，#9 → #4 之间约 40 s 内连续出现三次相似的冰墙画面，Viedma 卡上也几乎看不到湖面。可以接受；如有 Viedma 湖面加 Fitz Roy 的远景，可以替换。
- **N2**：`sources.md` §4 的 #30 Te Anau 仍写「NZ Ministry for the Environment (via Wikipedia); Lowe & Green 1987」，链接指向没有引注的「List of lakes of New Zealand」，Comment 2 也会照此公开。建议改为链接「Lake Te Anau」条目，并去掉 Lowe & Green。
- **N3**：`publish_with-risk-images.md` 的描述和 Comment 1 里，#13、#14、#22 Tinn、#24 的署名是「unknown (unknown)」或「unknown, unknown」，和卡面上的站名署名（volda.kommune.no 等）不一致，观感差。只有在用风险版时才需要处理：改成站名，并写「used with permission」或说明授权情况。
- **N4**（不影响成片）：`assets/img/` 里有没进账本的多余文件：`03_caspian_sea_alt.jpg`、`04_lago_ohiggins_alt.jpg`、`22_lago_cochrane_alt.jpg`、`28_great_bear_lake_alt.jpg`（与正图相同）和 `33_lake_wakatipu.jpg`（已出榜）。另外 #34 / #35 的文件名仍是旧编号 `35_` / `36_`。

### 本轮抽帧清单（`_build/qc/recheck/`）
- 默认版 `m_*`：2.5（片头）、4.6 / 5.5 / 7.0 / 7.5 / 8.5 / 9.2（首卡停留）、15.5（#33 AI 角标）、40.0（Poso / Wakatipu 洞察卡）、51.8（#28）、89.8（#22 并列）、115.2（#18）、164.2、169.7（洞察卡 3）、182.2（#9）、189.0（#8 新图）、195.8（#7 新图）、208.3（Viedma 洞察卡）、214.1（#5 新图）、220.9（#4）、227.7（#3）、240.2（after 2 洞察卡）、245.0、250.0（冠军）、257.0（计分板）、262.5（来源卡）、275.0、282.9（片尾），以及随机点 44.3 / 120.2 / 178.1 / 215.4 / 261.4。
- 章节点 `ch_*`：28.2 / 102.5 / 175.4 / 243.9 / 254.9。
- 风险版 `r_*`：51.8、77.2、83.5、89.8、96.2、145.2、151.5、164.2、189.0、220.9、227.7（7 张风险图与撤下的 4 张逐一上屏）。
- 原图缩略 `src_05_lago_viedma.jpg`、`src_07_issyk_kul.jpg`、`src_08_great_slave_lake_alt.jpg`；封面缩略 `thumb_small.jpg`。

---

## 第 1 轮独立审片 · 2026-11-04

> 审片人是独立上下文，没有参与制作。审的对象：当前的 `data.json`、`sources.md`、`assets.json`、`assets/img/`（47 张，含 image_alt）、`publish.md` / `publish_with-risk-images.md`、`render/` 下两版成片（manifest 的输入 sha256 与当前文件一致，成片对应当前数据）。
> 数据用 WebSearch / WebFetch 抽查，并读了本地 `_build/raw/`；没有调用任何收费服务。审片产物：`_build/qc/`（拼图、抽帧、时间线脚本）。
> 按委托说明，现有成片没有「AI IMAGE」角标，**不记为问题**。

**结论：必须修后再发布。** 有 2 个 blocker：#33 Lake Wakatipu 的 420 m 没有出处，有据的值约 380 m，应当出榜；#5 Lago Viedma 的主图不是 Viedma 湖。另有 4 个 major。制作方改正的五个常见错值都有可靠出处，其中 Poso、Fagnano、O'Higgins、Argentino、Viedma 我亲自核到了原文。修完要重出数据、重渲两版、重新生成 publish 文本，再复审改动处。

---

## Blocker

### B1 #33 Lake Wakatipu 的 420 m 无出处；可靠来源都是约 376–380 m，应当出榜
- **证据**
  - en.wikipedia「Lake Wakatipu」的 infobox 和正文都写 420 m，**没有引注**。Talk 页「Size and depth」一节（Johnragla，2023-05-26）指出，条目原来写 380 m，后来改成 420 m，改动没有出处。同一帖还列出：环境部 2010 年湖泊水质报告 380 m、LAWA 380 m、**LINZ 海图 NZ 252 最大水深 376 m**。帖里另一个 420 m 的来源是 Stuff 的报道，标题是「Hauroko NZ's deepest lake」，可能把 Hauroko 的数和 Wakatipu 搞混了。
  - *NZ Journal of Marine and Freshwater Research* 1970 年关于该湖夏季等温层的文章（doi 10.1080/00288330.1970.9515338），摘要写 maximum depth 380 m。Britannica 给 1,240 ft（378 m）。
  - `sources.md` 把这个值记为「Lowe & Green 1987 via Wikipedia 'List of lakes of New Zealand'」。实查该列表，深度一节**只有 Waikaremoana 一条带引注**，Wakatipu 的 420 也没有出处。所以这条归属本身不成立。
- **影响**：榜单门槛是 400 m。按 376–380 m 算，Wakatipu 不在榜上，现在等于收了一个不合格的湖。新西兰观众很熟这个湖，这里被挑出来的风险很高。
- **修法**
  1. 在 `items_def.py` 里把 Wakatipu 移进排除表：`("Lake Wakatipu (New Zealand)", "~380 m", "Wikipedia's 420 m is uncited; LINZ chart NZ 252 shows 376 m; MfE/LAWA and Irwin-era survey (NZJMFR 1970) give 380 m -> below the 400 m cut.")`。
  2. N 改为 **35**：Khantayskoye 单独排 #33，Lago Grey #34，Lake Superior #35，其余名次不变。kicker 改成 `TOP 35`，标题和 publish 标题改成「Top 35」，Oceania 计分改成 3（Asia 9 / NA 8 / SA 7 / Europe 5 / Oceania 3 / Africa 3）。`topic.md`、`sources.md` §1/§3（「400 m 以下最近」改为 Poso 395、Hāwea 392、Wakatipu ~380）同步改。
  3. 可选：在 after 30 的 Poso 洞察卡旁加一句。例如另起一张卡，放在 #35 之后（≤90 字符，82 字符）：「Lake Wakatipu, long listed at 420 m, is really about 380 m deep, so it is out too.」。这也是本期「改正常见错值」的又一个卖点。
  4. 同类问题：#21 Hauroko、#29 Manapouri 也写着「Lowe & Green 1987 via Wikipedia list」，但列表里没有这个引注。#30 Te Anau 我核到了：其条目正文的 425 m 引的是环境部《Lakes in New Zealand》。Hauroko 和 Manapouri 应改为引条目或报告原文，不要再写成 Lowe & Green。

### B2 #5 Lago Viedma 的主图不是 Viedma 湖
- **证据**：`assets/img/05_lago_viedma.jpg`（Pexels 39277375，Yani Martinez）。画面是 Fitz Roy 群峰和右侧的 Piedras Blancas 冰川，近景是一个被南青冈林围住的小湖，对岸约 1 km 就是林坡，前景是步道沙土和枯木。这是 El Chaltén 附近步道上的小湖，**很可能是 Laguna Capri**。Lago Viedma 长约 80 km，在 Fitz Roy 东南方十几公里外，四周是草原，不可能有这种近景。Pexels 页面的地点标签只有「El Chalten, Santa Cruz」，「over Lago Viedma」只出现在网站自动生成的描述里。候选记录（`claude_stock.json`）里也只写了「Pexels: mountains over Lago Viedma」，没有核对画面。
- **影响**：前 5 名、而且是本期「争议湖」那张卡认错了湖，去过的观众一眼就能认出来。
- **修法**：换成能确认是 Viedma 的图。可选：Viedma 冰川前缘与湖面（游船视角）；从 Ruta 23 或 Viedma 湖东岸看 Fitz Roy、湖面占画面一半以上的远景。Unsplash、Pexels、Flickr CC 用「Glaciar Viedma」「Lago Viedma」搜。找到后先看画面是否有冰川或大湖面，再看来源页地点。

---

## Major

### M1 #8 Great Slave Lake 默认版替代图：卡上看不到湖，地点也没核实
- **证据**：`08_great_slave_lake_alt.jpg`（Unsplash SJaLMYcH6So，Ken Cheung）。在 720×800 满版卡上，画面被木屋、木栈道和极光占满，**看不到湖面**（抽帧 3:01–3:19，见 `frames/m_0192.8.jpg`、`m_0199.0.jpg`）。候选记录只写了「Unsplash 'yellowknife': boat and house on the lake」，是按搜索词取的，来源页没有核到湖名。这类极光木屋在 Yellowknife 一带很多，也可能在别的湖（如 Blachford Lake）。本次 Unsplash 页面被反爬拦截，我没能打开。这张图也违反了本期 `layout.image_prefer` 的「no buildings dominating」。
- **修法**：换一张能看到大片湖面、地点核实为 Great Slave Lake 的可商用图（East Arm 悬崖、Yellowknife Bay 湖面）。handoff 记录的 Flickr CC 候选解禁后优先补这一张。实在没有，宁可用风险版那张 East Arm 悬崖图，并争取作者授权。

### M2 #36 只停留约 1.5 秒就开始被裁，读不满 3 秒
- **证据**：`data.json` 的 layout 没有 `intro_hold`。抽帧 4.6 s、5.0 s、5.5 s、6.0 s：卡片约 4.6 s 才滑入完整，5.0 s 就开始左移；6.0 s 时数值已被裁成「06 m」。违反 bible §7-5（手机全屏 3 秒内看清名称和数值）。data_contract 对此有现成参数，并建议用 2.5。
- **修法**：`layout.intro_hold = 2.5`，和 B1 一起重渲。重渲后时长、章节都会变，见 M4。

### M3 风险版 11 张「licence unknown」中，4 张来源页明写「版权所有」，不应进签字池；屏上署名也不宜写「licence unknown」
- **证据**：`sources.md` §7 和 `publish_with-risk-images.md` 的署名：#3 Caspian（Tour-Mangystau，**All rights reserved**）、#4 O'Higgins（gochile.cl，**Todos los derechos reservados**）、#22 Cochrane（gochile.cl，**Todos los derechos reservados**）、#28 Great Bear（dstewartfishing.com，**All rights are reserved**）。bible §4 的 `image_risk` 机制针对的是「许可不明」，这 4 张是许可明确不允许，用了就是明知侵权。描述框还会把「All rights reserved」原样公开。另外风险版卡面署名直接显示「Photo: unknown / licence unknown」（抽帧 `r_0081.0.jpg`、`r_0093.7.jpg`、`r_0149.0.jpg` 等），观感很差。
- **修法**：这 4 张改标 `image_risk = "all rights reserved"`，从风险版撤下（风险版改用默认版的替代图）；或者先取得作者书面授权，授权记入账本再放。其余 7 张真正许可不明的，卡面署名去掉「licence unknown」字样，只写来源站名，例如「Photo: Volda kommune」。

### M4 publish.md 章节：当前时间码对，但 B1、M2 修完后必须重新生成
- **核对**（`_build/qc/timeline_check.py` 按当前渲染器复算，并逐帧确认）：

| publish.md | 复算 | 画面（抽帧） | 结论 |
|---|---|---|---|
| 0:00 Intro & #36–#21 | 片头 0–5 s；#36 5.0 s 到中线，#21 Hauroko 100.0 s 到中线 | `m_0002.5`、`m_0006.0`、`m_0100.0` | 对 |
| 1:46 #20–#11 | #20 Nahuel Huapi 106.33 s 到中线 | `m_0106.3`：#20 居中 | 对 |
| 2:59 Top 10 | #10 Crater 179.23 s 到中线 | `m_0179.2`：#10 居中 | 对 |
| 4:07 No. 1 | 冠军段起点 251.77 − 4 = 247.77 s | `m_0247.8`：Baikal 卡已进入 | 对 |
| 4:18 Deep lakes by continent | 计分板段起点 257.77 + 1 = 258.77 s | `m_0258.8`：计分板 | 对 |

  「Sources & credits」4:24 与上一章只差 6 s，按 YouTube 的 ≥10 s 规则被合并，合理。两版成片时间线相同，风险版章节也对。
- **补充**：现在的生成器已经修好（`publish.py` 的注释写着 N=36 → #36–#31 not dropped）。它对当前数据输出的是「0:00 Intro & #36–#32 / 0:32 #30–#21 / 1:46 / 2:59 / 4:07 / 4:18」，比手改版多一个 0:32 章节。因为并列名次，#31 空缺，标签写 #36–#32 是对的。
- **修法**：B1、M2 修完后时间线会变（N=35，并且加 2.5 s 停留），手改的时间码全部失效。用 `python -m rank_scroll publish` 重新生成两份 publish 文本，删掉清单里「已手改」那一行，再按上表方法抽帧复核。

---

## Minor

1. **#5 Viedma 洞察卡措辞和出处小错**：sources.md 写 Minowa 2023 的 Viedma 数据来自「Boat echo-sounding 2012–2014」，原文（§3.1）是 **2017 年 1 月至 2020 年 6 月**测深，再合并早年数据。所以 2023 论文的实测**早于** 2022 年 5 月那次 900 m 调查。900 m 至今只有 CONICET 新闻稿，没有找到同行评审发表。现在的洞察卡「a 2022 survey claimed 900 m; a 2023 study measured about 750 m」容易让人读成「新研究推翻了旧说法」。建议改为（91 字符，需压到 ≤90，可去掉 "Lago"）：「Next: Viedma. A 2022 survey reported 900 m (unpublished); peer-reviewed sonar: ~750 m.」。750 m 的取值本身合理（scope 写的是 latest *published* sounding）。
2. **改正旧值的标签被挤掉**：渲染器从后往前丢标签。O'Higgins「Survey 2020 (was 836 m)」、Viedma「2022 claim: 900 m」、Argentino「Often listed as 719 m」、Issyk-Kul「Often listed as 702 m」、Salvatnet「(was 464)」在成片里都没有显示，只剩 Floor 标签（抽帧 3:06、3:19、3:37、3:44）。这是本期 D2 差异点。建议对这几项把「旧值」标签放第一个、Floor 放第二个。
3. **#7 Issyk-Kul 裁切看不到湖**：卡上只有蓝天和雪山，湖面被底部数值块盖住（`frames/zoom_199_issyk.jpg`）。建议设 `image_focus: [0.5, 0.85]` 或换图。
4. **#3 里海**：
   - 国旗：哈萨克斯坦（按岸线最长）。卡上「SHARED BY 5 COUNTRIES」能化解大部分疑问，但最深点在南里海，离哈国很远，评论区会问「为什么是哈萨克斯坦」。建议 scope_note 保留现有写法，同时在置顶评论或描述里加一句「Caspian: flag = longest shoreline (Kazakhstan); deepest point lies in the South Caspian basin」。
   - 算不算湖：卡上已有「Largest lake on Earth」标签，描述框也写了「counted as a lake」，可接受。
   - 计分板：Asia 9 > NA 8 的悬念靠里海记 Asia 撑着。若记 Europe 就是 8:8 平。这个口径在 sources 里写了，可接受。
   - 默认版替代图（Aktau 阴天灰色礁石）偏弱，而且是封面三张之一。
5. **AI 生成图（默认版 10 张）**：账本、描述、上传清单都写明了。卡面署名「AI-generated image (not a photo)」字号很小，角标稍后由渲染器补，不记问题。看图结论：
   - 没有明显瑕疵（无畸形、无文字、无水印）。
   - 但都是泛化的「挪威峡湾 / 加拿大林湖」风格。Hornindalsvatnet、Salvatnet、Tinn 三张几乎可以互换。Quesnel 的生成图是高耸雪峰夹峡湾，而实际主湖盆是低缓林丘，见风险版实拍。Tinn 的生成图是花岗岩绝壁，有夸张。
   - 0:55–2:50 之间连续出现 6–7 张 AI 图，观众容易觉得「AI 糊弄」并划走。
   - 建议 Flickr 解禁后优先替换 Quesnel、Tinn、Great Bear、Hornindal。
6. **#20 Nahuel Huapi**：Cerro Campanario 视角，画面主体其实是前景的 Lago Moreno / Laguna El Trébol，Nahuel Huapi 只在远处露出湖臂。可接受；如有更正面的 Nahuel Huapi 湖面图可换。
7. **未能打开来源页核地点的图**（Unsplash 反爬拦截）：#32 Tazawa（候选记录是按同系列推断的，「golden statue set」）、#30 Te Anau。画面可信，Tazawa 疑似背景为秋田驹岳。发布前人工点开来源页确认一次地点。#2 Tanganyika 的 Pexels 页地点为 Bujumbura（布隆迪岸），是 Tanganyika 湖，没问题。
8. **#28 Great Bear 标签「Largest lake in Canada」**：不严谨，按加拿大境内水面算，Huron、Superior 的加方部分都更大。改为「Largest wholly in Canada」（24 字符）。
9. **after 2 洞察卡提前点名冠军**：「Lake Baikal holds…」在 3:53 进场，比 Baikal 卡早约 5 s。建议改成悬念式（83 字符）：「Next, No. 1: a lake holding about 20% of the world's unfrozen fresh water (UNESCO).」。另外封面草图直接写出 #1–#3（含冠军），与 Vision「看到最后才知道冠军」冲突。建议封面只放冠军图、不写名次，或标「#1 = ?」。
10. **#4 O'Higgins 默认版替代图**：Arto Teräs 博客，原图只有 900×600。来源和许可我核过（CC BY-SA 3.0 Unported，图注「The ice wall of the glacier O'Higgins」）。图放大到 720×800 卡偏软，可接受，有更高清的再换。
11. **sources.md 记录小错**：
    - Poso 一行说「本地抽取 `_build/raw/poso_tournier2025.txt` 正文」，实际本地文件只是补充材料（SI），没有「395 m」这句。我在 oap.unige.ch 论文正文核到了 §4.1「maximum depth of 395 m」和 §3.1「Nov. 2022, Kongsberg EM2040 multibeam」，建议补抓正文 PDF（`/article/view/1604/2249`）。
    - Issyk-Kul 的 De Batist 年份，HESS 文献表是 **2001**，不是 2002。
12. **置顶评论里 AI 图的「source file」写的是本地路径** `_build/gen/…png`，对观众没有意义。改为「generated for this video (Codex image_gen)」。
13. **成片静音**：两版都是 anullsrc，volumedetect 实测 −91 dB。`assets/music/` 里有两首 mp3，但没有混进成片。配乐相关的 §7-6 本轮没有可审对象。
14. **时长约 4:47**（修完约 4:44），低于 bible 5–8 分钟，属已知取舍。

---

## 已确认无问题（摘要）

- **名次与排序**：36 条按 value 降序，同值同名次（1,1,3 式）正确，英尺换算全部正确（脚本复核）。`validate --strict` 两版都 OK。
- **成片技术参数**：两版都是 1920×1080、60 fps、h264 yuv420p，时长 286.767 s，**17,206 帧**，与 manifest 时间线一致，没有截断。manifest 的 38 个输入 sha256 与当前文件全部一致。
- **文字**：抽帧里没看到出框、截断、省略号或占位卡。风险版里里海那行很长的署名也在卡内。
- **国旗**：36 张都和 country_iso2 对应。Tanganyika 用刚果（金）的依据核实（FAO LTR 表：DRC 14,800 km²（45%）> 坦桑尼亚 13,500 km²（41%））。
- **其余实拍认湖**：Baikal（Olkhon 岛 Shaman Rock）、Crater（Wizard Island）、General Carrera（大理石洞）、Argentino（Perito Moreno 冰川，注入 Lago Argentino）、Tahoe（Sand Harbor）、Como（Varenna / Bellagio 一带）、Wakatipu（Queenstown）、Grey（冰山）、Superior（Pictured Rocks）、Sarez（EGU Imaggeo，CC BY 3.0）、Kivu（MONUSCO Flickr，Goma 附近）、Van（Pexels 页标 Lake Van）、Malawi（Pexels 页标 Lake Malawi）、Mjøsa（Pexels 页标 Mjøsa / Lillehammer）、Caspian 默认图（Pexels 页标 Aktau）、Issyk-Kul、Toba、Chelan、Manapouri。都没有发现认错或水印。
- **包装**：标题「Deepest Lakes in the World | Top 36 Ranked (2026)」49 字符（改 35 后不变）。描述含 scope_note、逐张署名、AI 图说明。上传清单要求勾选「Altered or synthetic content」。

---

## 数据核对样本（本轮亲自核）

| # | 湖 | 屏上值 | 核对来源（本轮打开） | 结果 |
|---|---|---|---|---|
| 1 | Baikal | 1,642 m | en.wikipedia「Lake Baikal」（INTAS 引注）；UNESCO 754「20% of the world's total unfrozen freshwater」（本地 raw） | 一致；洞察卡 20% 有据 |
| 2 | Tanganyika | 1,470 m | FAO LTR GEN.HTM（本地 raw）：max 1,470 m（南盆）、面积分国表 | 一致；国旗依据成立 |
| 3 | Caspian | 1,025 m | Wikipedia infobox（raw）1,025 m；oq.gov.kz（未重开） | 一致（通行值） |
| 4 | O'Higgins | 799 m | Minowa et al. 2023 §4.1.1「799 m」，2020 年 2 月实测（raw PDF 全文） | 一致；「Survey 2020 (was 836 m)」成立 |
| 5 | Viedma | ~750 m | Minowa 2023 §4.1.2「∼750 m」（测于 2017–2020）；CONICET 900 m 仅为新闻稿，没有同行评审发表 | 取值合理；措辞见 Minor 1 |
| 6 | Malawi | 706 m | ILEC WLDB 3594「706」 | 一致 |
| 7 | Issyk-Kul | 668 m | Zavialov 2018 HESS：668 m「most plausible」，702 m 无据 | 一致 |
| 9 | Argentino | 607 m | Minowa 2023 §4.1.3 Brazo Upsala「607 m」；Wikipedia 719 m 引的是死链 | 一致，DEPTH DISPUTED 合理 |
| 10 | Crater | 594 m | USGS「new maximum depth 594 m (1,949 ft)」，2000 年夏 | 一致 |
| 30 | Te Anau | 425 m | en.wikipedia「Lake Te Anau」正文引环境部《Lakes in New Zealand》 | 一致 |
| 33 | Wakatipu | 420 m | Wikipedia 无引注；Talk 页：LINZ NZ 252 为 376 m，MfE / LAWA 为 380 m；NZJMFR 1970 为 380 m；Britannica 378 m | **不成立 → B1** |
| 35 | Grey | 410 m | Sugiyama et al. 2021 Nat. Commun.「a 410-m-deep glacial lake」（raw） | 一致 |
| 36 | Superior | 406 m | Wikipedia 引 US EPA 1,333 ft（raw） | 一致 |
| 出榜 | Poso | 395 m | Tournier et al. 2025 *Sedimentologika* 正文 §4.1「maximum depth of 395 m」，2022 年 11 月多波束；Oeschger 中心 2023 年报道也是 395 m | 改正成立 |
| 出榜 | Fagnano | 206 m | Zanolla, Lodolo et al. 2011 *BGTA* 52(1)「Maximum water depth (206 m) is found in the eastern part」 | 改正成立 |

统计期：全部为 2026-11-03 取数的「最新已发表实测」。屏上统一写「Data as of Nov 2026」，与片头一致。

---

## 抽帧清单（`_build/qc/frames/`，2×2 拼图在 `frames/grids/`）

默认母版 `m_*.jpg`：

| 时间 | 内容 |
|---|---|
| 2.5 s | 片头 |
| 4.6 / 5.0 / 5.5 / 6.0 s | #36–#33 进场与开始滚动（M2） |
| 13.0 s | #35–#33 |
| 23.0 s | #33–#30 |
| 43.8 s | 洞察卡 1 Poso |
| 49.3 s | #29 / #28 |
| 66.0 s | #27–#25 |
| 81.0 s | #25–#22 |
| 93.7 s | #22 / #21 |
| 100.0 s | #22–#20 |
| 106.3 s | #20（章节 1:46） |
| 119.0 s | #19–#17 |
| 130.8 s | 洞察卡 2 Sarez |
| 136.3 s | #15 并列 |
| 149.0 s | #15–#13 |
| 160.0 s | #13–#11 |
| 173.5 s | 洞察卡 3 |
| 179.2 s | 第 10 名（章节 2:59） |
| 186.0 s | #10–#8 |
| 192.8 s | #9–#7 |
| 199.0 s | #8–#6 |
| 212.2 s | 洞察卡 4 Viedma |
| 217.9 s | #5 |
| 224.7 s | #5–#3 |
| 231.5 s | #4–#2 |
| 238.3 s | #3 / #2 / 洞察卡 5 |
| 244.0 s | 洞察卡 5 / #1 进场 |
| 247.8 s | 章节 4:07 |
| 255.0 s | 冠军 |
| 258.8 / 261.0 s | 计分板 |
| 266.0 s | 来源卡 |
| 278.0 / 286.6 s | 片尾（含最后一帧） |

风险版 `r_*.jpg`：55.7、81.0、87.3、93.7、100.0、149.0、155.3、168.0、192.8、224.7、231.5 s（11 张风险图逐一上屏）。

另有局部放大：`zoom_199_issyk.jpg`（Issyk-Kul 裁切）、`zoom_r231_caspian_credit.jpg`（风险版里海署名未出框）。图片拼图在 `_build/qc/sheets/sheet_00–07.jpg`（47 张全看）。

## 观众视角

- **亮点**：
  - 「湖底在海平面下 / 上多少米」很新鲜，例如 Sarez 湖底仍在海拔 2,758 m，Baikal 湖底在海平面下 1,187 m。
  - Poso 出榜洞察卡、Viedma 争议卡都有「原来榜单是错的」的爽点。
  - 冠军 Baikal 加 20% 淡水收尾，干净利落。
- **会划走的地方**：
  - 开头 #36 一闪而过（M2）。
  - 0:55–2:50 一长段冷门湖，叠加连续的 AI 图（Minor 5），这是最危险的区段。
  - 前 10 里 Great Slave 只见木屋不见湖（M1）、Issyk-Kul 只见雪山不见湖（Minor 3），会削弱「湖」的观感。
- **评论区预判**：
  - 里海算不算湖、为什么挂哈萨克斯坦旗。
  - Viedma 900 m。
  - 新西兰观众指出 Wakatipu 没有 420 m（B1 修掉后可主动做成卖点）。
