# 调研 A1 · 卡片版式参考（数据排行类 + 食物「每种 X」类）

> 2026-11-06，代理调研。目的：改进每张卡的图片与信息呈现，重点服务下一期「世界各地的大米」（列表期，不排名：展示粒形、颜色、香气、做成什么菜）。
> 素材在 [layout_refs/](layout_refs/)：`frames/<编号>_<slug>/`（每条 4 张：`thumb` 封面、`f25` / `f50` / `f75` 片中帧）、`frames/_review_quads/`（每条 4 帧拼图）、两张对比拼图、`data/`（检索与实测原始数据）、`scripts/`（抓取与拼图脚本）。
> **截图仅供内部分析，版权归原频道，不提交、不外传。**

## 0. 方法与局限（先读）

- **检索**：`tools/yt_research.py search`（按播放排序）共 25 个检索词，原始结果 `layout_refs/data/search_*.jsonl`。
- **播放量实测**：本机 yt-dlp 的单视频页请求（`meta` / 下载）当天全部被 YouTube「Sign in to confirm you're not a bot」拦截（换 player_client 也一样；与 `shengji_zhilu` 等剧此前遇到的情况相同）。没有用 cookies，也没用任何绕过手段。改用无头 Chrome 打开公开观看页读 `ytInitialData`，拿到播放、点赞和日期；时长来自检索结果。数据在 `data/meta_watchpage_2026-11-06.jsonl` 与 `data/layout_refs_2026-11-06.jsonl`。
- **画面**：播放器同样要求登录，**没能下载任何视频，也就没能用 ffmpeg 逐帧抽帧**。改取 YouTube 公开的静态图：自定义封面 `maxresdefault`，以及系统在片长约 25% / 50% / 75% 处自动截的 `maxres1/2/3`。四张都是 1280×720 真实画面，但截取时刻不由我们选。
  - 因此**动效（进场、缩放、停顿）大多没能直接观察**。表中的动效描述，一部分来自已有拆解（Country Cassette，见 `reference_analysis.md`），一部分是从帧里半张卡、镜头角度推断的，已标「推断」。等 yt-dlp 恢复后，可以对 01、11、13、14 四条补低清下载和逐秒抽帧（脚本已备好）。
- 我们的现状帧：`frames/00_ours_ep04_t120.jpg`（ep04 默认母版第 120 秒）。
- Instagram / TikTok 轮播：没有可用的检索工具，未覆盖。

## 1. 逐条发现

A = 数据排行 / 对比卡类，B = 食物「每种 X」类。播放量为 2026-11-06 实测。

| # | 视频 | 频道 | 播放 | 时长 | 图片处理 | 名称 / 国家 / 数值的位置 | 产地怎么表达 | 怎么避免重复 / 动效 |
|---|---|---|---:|---:|---|---|---|---|
| A01 | [Top 50 Best Selling Car Brands (2026)](https://www.youtube.com/watch?v=YzRCcFx3XME) | Country Cassette | 531,107 | 5:08 | 白底，车型侧视抠图 | 顶部黑底国名横幅 → 抠图 → 灰色药丸品牌名 → 柱状图标 + Units Sold + 数值 → Rank N | **国旗做成车门贴膜**，再加顶部国名 | 匀速左移、同屏约 2.5 列；靠车型和车色变化 |
| A02 | [Total Population by Country](https://www.youtube.com/watch?v=wma5fLfVYF0) | WorldTV Studio | 10,282,546 | 7:31 | 3D 国旗方块，体积≈数值 | 悬浮深色信息牌：国名 / 大号数值 / 份额 + 名次 | 国旗就是主体 | 镜头沿队列推进（推断）；分段换场景底色 |
| A03 | [National Fruits of Countries](https://www.youtube.com/watch?v=q6iNqx8nUnI) | WorldTV Studio | 2,001,811 | 2:15 | 3D 实物，**整果和剖面同框**，统一木桌 | 左下紫色大字名称 + 红字国家列表 | **国旗插杆插在主体后方**，多国共享一种 | 每条换摆法（碗装、散放、切开） |
| A04 | [Mobile Brands By Country](https://www.youtube.com/watch?v=OhvO854SS8c) | Dastatistics | 5,730,027 | 5:27 | 产品抠图在粉彩渐变底 | 列头：盾形国旗 + 国名 → logo → 品牌名条 → 产品图 | 盾形国旗列头 | **按国家分组**，同组共用列头；横向滚动（推断） |
| A05 | [Oldest Countries 3D](https://www.youtube.com/watch?v=p3E5Y5AyBYg) | World Data 3D | 6,665,273 | 3:13 | 3D 柱体，柱面嵌历史图片窗 | 柱面：国名 / 黄色数值 / years / 朝代 | 柱顶旗杆 | 镜头环绕；冠军柱用「????」制造悬念（封面） |
| A06 | [Tallest statue size comparison](https://www.youtube.com/watch?v=YEPJDkZRdJU) | Real Data | 58,292,235 | 1:51 | 3D 模型站成一排 | 半透明标签：名称小 / **数值巨大** / 城市, 国家 + 小国旗 | 标签内小国旗 + 地名 | **开头先放「平均人 176 cm」作比例参照**；侧向平移 |
| A07 | [Country Size Comparison 3D](https://www.youtube.com/watch?v=BuN8c74BKdM) | Most Data | 3,966,546 | 32:04 | 卫星影像抠出国土，浅灰底，大量留白 | 旗针旁细体：国名 / km²（mi²） | 国旗插在国土上 | 每个形状都不同，天然不重复 |
| A08 | [Top 50 Rice Producing vs Importing](https://www.youtube.com/watch?v=3FEoOFsZ-8w) | Global Rank | 201,952 | 3:37 | 无实物图，只有圆形国旗徽章 | 左上 #名次，右上原因小签（Water scarcity），国名条，绿 / 红双值格 | 圆形国旗 | 原因小签每条不同。**数值有明显错误**（110% / 00%） |
| A09 | [Leading Rice Exporting Nations](https://www.youtube.com/watch?v=LMEgQRxehlc) | Data Analyst | 6,916,792 | 8:14 | 条形赛跑，右侧手绘牛车米袋插画 | 国名 / 条 / 国旗圆章 / 数值，大号年份 | 条端国旗圆章 | 年份推进。**竖版画面加黑边放进 16:9** |
| A10 | [Largest Rice Exporting Countries](https://www.youtube.com/watch?v=tu54enkhyiE) | Rank the World | 552,134 | 8:15 | 与 A09 几乎相同的模板 | 同 A09 | 同 A09 | 同 A09。同题大米数据片已有至少 2 家 |
| A11 | [Every Country's Favorite Bread](https://www.youtube.com/watch?v=fYv2NP-71HA) | Data World Plus | 82,557 | 8:34 | **食物抠图在纯色 / 渐变底** | 主图 → 名称条 → 黄色国名签 → 透视国旗「底座」 | 国旗做成卡片下半部 | 几乎没有变化：**连续 3 张都叫 White Bread，图也相似** |
| A12 | [Top 30 Best-Selling Men's Fragrances (2026)](https://www.youtube.com/watch?v=rYTs0xE6YAY) | Real Men Real Style | 2,866,461 | 14:55 | 片中主持人手持；**封面瓶子大小≈销量** | 口播 | 无 | 主持人驱动，只借鉴封面的「用尺寸编码数值」 |
| B13 | [12 Types of Rice, Microscope and Cooked](https://www.youtube.com/watch?v=ZDYg9SQthas) | Bon Appétit | 924,169 | 20:19 | **生米小木碗 → 显微镜 → 成品菜满版微距** | 左下细线框编号标签「5 \| BOMBA」，全片位置不变 | 不显示（口播） | 每种米都走生、显微、熟三段，配一道代表菜（Bomba → 西班牙饭） |
| B14 | [Every Rice Explained In 8 Minutes](https://www.youtube.com/watch?v=1X5g92z_OUU) | Food Explained | 51,498 | 8:01 | 白底抠图：**熟米一碗，前景撒一小撮生米** | 名称在图下，居中粗体 | 不显示（口播） | **每种换器皿和点缀**（茉莉花、肉桂丁香、芭蕉叶）；插入等式图「白米 + 黑米 = 紫米」。图疑似 AI 素材 |
| B15 | [How Rice is Made in 10 Countries](https://www.youtube.com/watch?v=pFgndOFYmys) | Epicurious | 492,484 | 17:17 | 俯拍成品菜在木桌，4 宫格 | 左上：**圆形国旗 + 红色国名药丸** | 圆形国旗 + 国名 | 主持人轮换；国家开场卡（大国旗圆章 + 粗体国名） |
| B16 | [16 Rice Dishes From Around The World](https://www.youtube.com/watch?v=qb-gcaO_UIg) | Insider Food | 1,682,786 | 6:57 | 满版视频，人物试吃 + 食物特写 | 左侧**转盘**：顶部编号 16，中间高亮当前国家，上下列出前后几国 | 转盘里写国家 / 地区 | 转盘给出进度感，观众知道还剩几个 |
| B17 | [29 Types Of Bread Around The World](https://www.youtube.com/watch?v=C8U23AS1irY) | Insider Food | 7,685,096 | 8:55 | 满版特写，常拍剖面（玉米面包切面、芝士拉丝） | 系列角标 + 同款转盘 | 同 B16 | 每条一个动作镜头（撕、拉、切） |
| B18 | [What Cheese Looks Like Around The World](https://www.youtube.com/watch?v=2NutfCHAyNM) | Insider Food | 10,218,664 | 9:01 | 满版制作过程 + 切面特写 | 同 B16 | 同 B16 | 同 B17 |
| B19 | [Every Way to Cook an Egg (59 Methods)](https://www.youtube.com/watch?v=qWAagS_MANg) | Bon Appétit | 40,258,276 | 27:11 | 满版，统一大理石台面 | 封面大白字名称；片中**左下线描小图标**表示做法（微波炉、盘子） | 无 | 每条换图标和器具，台面不变，保持系列感 |
| B20 | [Trying Every Type Of Mushroom](https://www.youtube.com/watch?v=wnCCdpt8y6w) | Epicurious | 3,975,232 | 27:55 | 封面是**实物抠图在暖色条纹底**；片中主持人 | 橙色名称条；**事实卡**：圆形小图 + 名称 + AKA 别名 + 3 条要点 | 无 | 事实卡格式固定，内容每条不同 |
| B21 | [Party Rice Around Africa](https://www.youtube.com/watch?v=F1ku3Rljj1c) | Tasty | 3,147,178 | 6:36 | 黑底人物 + 成品菜 | 左上「Ghanaian Jollof Rice / as made by」+ 人名；左下圆形国旗 | 圆形国旗 | 每国一位厨师 |
| B22 | [7 Rice Dishes From Around the World](https://www.youtube.com/watch?v=ihWdzgsIAIM) | Great Big Story | 686,147 | 21:37 | 纪录片满版 | 角标 | 口播 | 人物故事驱动，和我们关系最小 |

对比拼图：

- [layout_refs/contact_sheet_A_food_items.jpg](layout_refs/contact_sheet_A_food_items.jpg)：食物条目怎么呈现（生熟同框、剖面、编号标签、事实卡、国旗药丸、转盘进度、做法图标，加一个重复反例）。
- [layout_refs/contact_sheet_B_data_cards.jpg](layout_refs/contact_sheet_B_data_cards.jpg)：数据卡的数值、产地、比例怎么放，第一格是我们 ep04 的现状。

## 2. 反复出现的模式

1. **两种主图流派。**
   - 数据排行频道几乎都用**抠图放在统一底色上**（A01、A04、A11、B14，A03 / A07 是 3D 版的同一思路）：主体轮廓清楚，底色统一，信息叠在空白处不挡图。
   - 食物编辑类频道（Insider、Bon Appétit）用**满版微距实拍**，靠质感和动作吸引人。
   - 我们现在的满版照片海报卡（bible §2.4）属于后一种，是做数据片的少数派。这本身是差异，但也意味着每张图都得够好（§4.0）。
2. **「内与外」「生与熟」同框，是食物条目的高信息量做法**：B14 熟米加生米，A03 整果加剖面，B13 生米到成品分段，B17 / B18 切面和拉丝。观众一眼就知道它长什么样、吃起来什么样。
3. **国旗几乎人人用，形式决定记忆点**：贴在主体上（A01 车门）、插杆或旗针（A03、A05、A07）、圆章 / 盾徽（A04、A08、B15、B21）、底座（A11）。**样本里没有一个用小地图定位**，只有 A07 的国土形状本身就是地图。地图插图是空位。
4. **数值层级一致**：名称小，数值巨大，单位或地点更小（A06、A01 封面、A02）。我们 ep04 已经是这个层级。
5. **比例参照很有效**：A06 先放「平均人 176 cm」再比较，A12 封面用瓶子大小表示销量。
6. **对抗重复的手段**：
   - 分组：A04 同国共用列头。
   - 进度：B16 转盘、B13 编号标签。
   - 每条换小图标：B19。
   - 每条换器皿和点缀：B14。
   - 插入等式、对比图：B14。
   - 固定格式的事实卡：B20。
   - 反例 A11：同名同貌的条目连排，是整份样本里最单调的一段。
7. **大米数据片已有同题**（A08–A10 生产 / 出口 / 进口），都是条形图或国旗卡，**没有一个拍米本身**。「各种米长什么样、做成什么菜」这一角度在数据片赛道里是空的，在食物编辑类里也只有 B13（92 万）、B14（5 万）两条直接相关。

## 3. 该借什么（按对我们卡片的预期影响排序，侧重大米期）

| 排名 | 借鉴 | 来源 | 大米期具体做法 | 成本 / 风险 |
|---|---|---|---|---|
| 1 | **生熟同框：主图是成菜，角上放生米微距圆窗** | B14、B13、A03 | 满版主图用该米的代表菜（Bomba → paella，Arborio → risotto，糯米 → 芒果糯米饭），右下或左下压一个直径约 220 px 的白边圆窗，放生米粒微距。观众同时看到粒形、颜色和成品。保留用户定的「照片 > 国旗 > 数值」优先级，只是一张卡配两张图 | 每条要两张合格图；`tile_gate` 两张都要审。生米微距可实拍图或 AI 图（标 AI IMAGE，粒形要核实），风险低 |
| 2 | **统一刻度的粒长比例尺**（取代「大号数值」做主数值） | A06 的比例参照、A12 封面 | 每张卡底部数值块改成一条固定刻度（0–10 mm）：画该米的生米粒剪影，按真实长宽比，旁写「6.6 mm · long grain」。所有卡刻度相同，滚动时粒长差异一眼可见。片头先放一张「一粒普通长粒米 = 6–7 mm」作参照 | 矢量绘制，无版权。需要每种米的粒长 / 长宽比数据和出处（D1） |
| 3 | **产地小地图插图**（国旗之外再加定位） | 空位（样本里没人做），A07 | 国旗旁加一个约 160 px 的地区小地图，点出产区（Camargue、Piedmont、不丹帕罗河谷、Carolina）。很多米是地区品种或多国共享，国旗说不清，地图说得清。多国共享照 ep02 的做法挂 SHARED 徽章 | Natural Earth 底图属公有领域。渲染器要加地图组件，中等工作量 |
| 4 | **属性小签 + 一套图标**（颜色色点 / 香气 / 口感 / 用途） | B19 做法图标、A08 原因小签、B20 事实卡 | 底部那行小字换成最多 3 个带图标的小签：实际颜色色点 + Red；香气 Fragrant / Neutral；口感 Sticky / Fluffy / Creamy / Firm。图标全片统一，内容每条不同 | 只改卡片模板。小签超过 3 个就会挤，要硬限 |
| 5 | **按家族分组 + 色带列头**（代替名次药丸） | A04 同国共用列头、B16 转盘 | 列表期没有倒数悬念，改用 6–7 个家族做结构：长粒籼米、短粒粳米、香米、糯米、有色米（红 / 紫 / 黑）、半成品或加工米、「不是米的 wild rice」。同家族的卡顶部共用一条色带和家族名，家族之间插一张洞察卡（D4），比如「同一粒米的胚乳，直链淀粉少就变黏」。也可以按颜色从白到黑排，做成视觉渐变，压轴放黑米或 wild rice | 不改数据契约，只改排序和皮肤 token。计分板（D3）改成「按大洲计数」或「按颜色计数」 |
| 6 | **列表期的进度计数「12 / 40」** | B16 转盘、B13 编号 | 右上名次药丸改成「12 / 40」或家族名加序号。我们已有底部进度条，再加一个数字即可 | 很小 |
| 7 | **别名行（AKA）** | B20 | 名称下一行小字：「aka sushi rice · Calrose」「aka Forbidden Rice」。观众常只认识别名，也能帮搜索 | 很小 |
| 8 | **图解插卡：等式 / 同米两菜** | B14 | 洞察卡做成图解版，例如「白米 + 黑米 = 紫色饭」「同一种 Arborio：risotto vs arancini」 | 每张插卡 2–3 张图 |
| 9 | **按家族变换卡底色（食物期皮肤）** | A11、B20 封面、A04 | 若主图用抠图（成菜抠在纯色底上），每个家族一种底色。**不建议整季改回抠图**：用户 2026-11-03 选了满版照片（follow-up 004）。最多作为「食物期」皮肤试一期，并先给用户看两版样卡 | 抠图质量要过 §4.0 第 2 条；工作量大 |
| 10 | **国旗插签** | A03 插杆、A01 贴膜 | 国旗画成插在饭上的牙签小旗，作为食物期的「国旗呈现方式」token（bible §2.5 允许按期换） | 渲染器加一种国旗样式；可能显得花哨，先出样卡再定 |

大米期一张卡的建议版式（在现有 600–720×800 满版卡上改，从上到下）：

```
[国旗(飘动) + 小地图插图]                 [家族色带: AROMATIC · 12/40]
                  满版成菜照片（代表菜）
                                              ( 生米微距圆窗 )
── 底部深色渐变 ──────────────────────────────────────────
THAILAND · Central Plains                     （强调色小号大写）
Jasmine Rice  (Hom Mali)                      （名称 + aka）
├──────■■■■■■■──────┤ 7.0 mm · long grain     （统一刻度粒长尺）
● white   ✿ fragrant   ≈ soft & slightly sticky   → Khao man gai
Photo: … / licence                            （署名）
```

## 4. 要避免的

- **同名同貌连排**（A11 的三张 White Bread）。大米里「白色长粒」会有很多张，要靠代表菜和产地拉开差异：相似品种合并，或把相似的分到不同家族，不要相邻。
- **竖版画面加黑边放进 16:9**（A09、A10）。
- **数值或文字错误**（A08 的 110% / 00%）。列表期的数值也都要有出处（D1），粒长、直链淀粉含量写清口径。
- **主持人或人物驱动的格式**（B16–B18、B21、B22、A12）。它们的价值来自拍摄和人，我们没有，只借图形元素（转盘、标签、事实卡）。
- **一眼看出是 AI 的素材感**：B14 的图像疑似 AI 素材，播放只有 5 万。这只是相关，不能证明是因果，但 §4.0 本来就要求 AI 图逐张审畸形。生米粒的 AI 图尤其要核对粒形和颜色。
- **重型 3D 场景**（A02、A05、A06）：播放高，但不是我们 skia 渲染器的路线，成本也不对等。
- **事实卡塞太多字**：B20 的事实卡有 3 行长句，适合停住的画面，不适合滚动卡。卡上最多 3 个短签。
- **国旗暗示「国家专属」**：jasmine 在泰国、柬埔寨、越南都有，basmati 印度和巴基斯坦共享，wild rice 根本不是稻属。分别用 SHARED 徽章和「not true rice」小签说明，免得评论区纠错。

## 5. 后续

- yt-dlp 恢复后，补抓 A01、A11、B13、B14 的低清片，逐秒抽帧看进场、停顿和缩放节奏，补进第 1 节。脚本在 `layout_refs/scripts/`。
- 第 3 节第 1–6 条需要改 `projects/rank_scroll` 的卡片模板，涉及数据字段 `image_raw`、`grain_length_mm`、`family`、`aka`、`attributes`，以及 `tile_gate` 对双图的审查。改之前先出 2–3 张样卡给用户选。属于剧级规则，不升仓库级。
