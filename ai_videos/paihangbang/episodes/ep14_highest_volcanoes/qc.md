# ep14 世界最高火山 · 审片记录（qc.md）

## 配乐审片 · 2026-11-04（独立上下文）

> 补配乐后由另起上下文的审稿代理测量（未参与制作）；脚本与数据在会话 scratchpad `audio_qc/`。只换音轨（默认版；风险版已在 `render/_stale/`），视频流与 `render/_silent/` 原静音版逐流哈希一致（22806 帧）。

**结论：小修后发布（音频无 blocker）**，上面「放行前」第①项配乐已解决。
- 配乐：Suno 任务 8b54e2a2，两首（dcbe6731 174 s、64cf1328 120 s），按 dcbe → 64cf → dcbe 拼接，4 s 交叉淡化，fit=end，最后一段放到原曲自然结尾。
- 响度 −16.0 LUFS，真峰值 −5.0 dBTP；前十名段 −15.5（前段 −18.5），冠军、计分板、片尾约 −14 直到淡出，贴合度好。
- minor：第 1 个接点 169.9–173.9 s 从 −14 降到 −20/−21 并维持到约 194 s（约 6–7 LU，渐变，来自曲子本身）；开头 0.42 s 为原曲前导静音。无削波、断音或拼接爆音。
- `publish.md` 已补 Suno 署名与 Content ID 清单项。

## 复核 · 2026-11-04

> 独立复核人（未参与制作，也没写第 1 轮审片，另起上下文）。只写本文件和 `_build/qc/recheck/`，没有改数据、图片或渲染。
> 复核对象：03:29 重渲的 `render/ep14_highest_volcanoes_master.mp4`（默认版，sha256 bc5ee748…）和 `render/ep14_highest_volcanoes_master_with-risk-images.mp4`（风险版，sha256 9e5fea8c…）。两份 manifest 的 output_sha256 与文件一致，记录的 52 个输入（data.json `0f81c2e7…`、assets.json `f7d4f720…` 和全部上屏图片）逐个重算 sha256，也都与现文件一致。`validate --strict` 默认、风险两种模式都通过。

### 最终结论：**默认版小修后发布；风险版必须修**（blocker 3 未解除）

- **推荐发布默认版**。它唯一的 blocker（#1 San José 的海拔）已经修好；头部卡换成了 NASA 公有领域实拍；每张 AI 卡都有黄色「AI IMAGE」徽章，署名改成了「AI-generated image, not a photo」；两张泄露结果的洞察卡也改了。剩下的问题都不阻断发布：#3、#4 仍是 AI 图，Isluga、Taapaca 的 AI 图仍在仿造真实村庄和教堂，冠军卡的 ISS 俯视图辨识度低，片尾来源卡没提 AI，音轨静音。
- **风险版不能发**：32 张风险图仍然没有书面许可，卡上照样显示「all rights reserved」「licence unknown」（原问题 3）。#11 Sierra Nevada 调过焦点后仍然只看得到云。
- 默认版**放行前至少做到**：①配乐到位后重渲，或用户明确同意按「静音画面版」放行（同 ep02）；②用户对 topic.md「待用户确认」第 4 条（29 张 AI 图）签字。下面列的小修建议做了更好，不做也不阻断。

### 原问题逐条复核

| # | 原严重度 | 结果 | 复核证据 |
|---|---|---|---|
| 1 | blocker | **已修** | data.json 里 San José 现在是 5,856 m，排 #24（Taapaca 5,860 m 与 Cordón de Puntas Negras 5,852 m 之间）。原 #15–#24 各上移一位，1–50 名连续，数值单调不增，无并列。sources.md §1/§3、topic.md、Comment 2 都注明「Geological Summary value」。成片 179.0 s 的卡显示「#24 San José 5,856 m · 19,213 ft」（`M_179.00.jpg`）。 |
| 2 | blocker（风险版） | **已修** | #25 的 image 已经改成 `25_cordon_de_puntas_negras_gen.png`，没有 image_risk，Miscanti 那张图已撤。风险版 172.67 s 的卡带 AI IMAGE 徽章（`R_172.67.jpg`）。 |
| 3 | blocker（风险版） | **未修** | 风险版仍有 32 张许可不明或保留所有权利的图（Andeshandbook 一家仍占多数），卡上照样显示「all rights reserved」「licence unknown」（`R_179.00.jpg`、`R_346.00.jpg` 等）。这一项要用户签字或拿到授权，不是制作方能修的。 |
| 4 | major | **已修** | #18 Licancabur 换成 Pexels 29287306（alisha jean，页面标题「majestic view of Licancabur volcano」），`image_focus [0.5, 0.3]`。两版的卡上都是完整的单个锥体，Juriques 不再出现（`M_217.00.jpg`、`R_217.00.jpg`）。 |
| 5 | major | **部分修** | 黄色「AI IMAGE」徽章：渲染器按 assets.json 的 licence 字段自动加（`contract.py`），29 个 `_gen.png` 文件的 licence 都是「AI-generated」。抽帧里出现的 AI 卡（两版合计 30 多张）都带徽章；实拍卡和 NASA 卡上没有误加。署名行改成「AI-generated image, not a photo」。publish.md 描述第 2 行写了「29 of the 50 … AI-generated illustrations, not photos」。**未做**的是片尾来源卡（360 s），它仍然只写「Image credits: shown on each card and listed in the description」，没有 AI 那一行。 |
| 6 | major | **部分修** | #1、#2、#5、#6、#7、#9、#12、#13、#40、#48 换成了 NASA 实拍，#7 Chungará 名片照和 #40 乌比纳斯村的 AI 图因此不再上屏。**仍未修**：#44 Isluga 的 AI 图还是白教堂加羊驼（`M_038.33.jpg`）；#23 Taapaca（原 #24）的 AI 图还是村舍加梯田，即仿普特雷（`M_185.33.jpg`）；#3 Tipas、#4 Incahuasi 这两张前 5 名的卡还是完美雪锥式 AI 图（`M_318.03.jpg`）；#45 Yucamane 也一样。 |
| 7 | major | **已修** | after_rank 3 的洞察卡改成「Both of the final two are active: each has erupted in the last 2,000 years.」，没有点名（`M_330.57.jpg`）。依据：750 CE、1877 年，与 sources.md §4 一致。 |
| 8 | major | **已修**（采用方案 b） | after_rank 26 的洞察卡改成「18 of these 50 volcanoes sit right on a national border.」，不再提前报出总数（`M_167.17.jpg`）。scope_note 说明跨境火山只按卡片国旗计一次。计分板仍是 CL 30 / PE 7 / AR 4 / EC 4 / MX 2 / IR 1 / RU 1 / BO 1，与 data.json 重新统计的结果一致，各帧右上角的逐卡累计也对（例如 217 s 时 CL 19）。**留下的风险**：#1、#2 仍然只挂智利旗，阿根廷观众可能在评论区争论（方案 a 没采用，属于用户决策）。 |
| 9 | major | **已修** | 6 座 Evidence Uncertain 的火山（#4、#9、#20、#21、#29、#47）标签改为「Possible recent activity」，#33 Olca-Paruma 改为「Eruption observed」。scope_note 写了「including 6 that GVP lists with uncertain Holocene evidence」，计数与 data.json 一致。Kilimanjaro 洞察卡已改措辞（`M_050.17.jpg`）。片头口径行改为「Active (Holocene) volcanoes by summit elevation · Smithsonian GVP, Nov 2026」（`M_001.50.jpg`）。小遗留：#47 Corrida de Cori 的 GVP 概述给的年龄约 34 万年，标「recent」仍然偏乐观，可以不改。 |
| 10 | major | **未修** | 两版音轨都还是静音（volumedetect mean = max = −91.0 dB）。这是已知的 Suno 阻塞。 |
| 11 | minor（风险版） | **未修** | 焦点改成 [0.5, 0.6] 后，卡上仍然是蓝天加两团云，山体被云和信息块挡住（`R_266.00.jpg`）。 |
| 12 | minor（风险版） | **已修** | 焦点 [0.65, 0.4] 后，雪顶火山进入画面右半部，教堂废墟退到左下角（`R_253.33.jpg`）。 |
| 13 | minor（风险版） | **已修** | 焦点 [0.3, 0.4] 后，Láscar 主体在卡中（`R_055.67.jpg`）。图仍是 1024×666 低清，可接受。 |
| 14 | minor（风险版） | **未修** | #3、#24 Taapaca（现 #23）、#9、#34、#45、#40 的风险图和焦点都没动（`R_324.83.jpg`、`R_185.33.jpg` 等）。只影响风险版。 |
| 15 | minor | **已修** | Orizaba 焦点 [0.5, 0.55]，山体位于卡片中部（`M_044.67.jpg`）。 |
| 16 | minor | **部分修** | AI 图从 39 张降到 29 张，但剩下的仍是同一种配方（晴空、雪锥、盐湖、针茅）。#47 主体有歧义的问题没变。 |
| 17 | minor | **未变** | Guayaques 仍用 GVP 5,598 m，等用户决定（topic.md 待确认 2）。 |
| 18 | minor | **已修** | sources.md §5 改成动态统计：默认版 AI 29 / NASA 10 / Unsplash 8 / Pexels 2 / CC BY 1，风险版 风险图 32 / Unsplash 8 / AI 8 / Pexels 2。按 data.json 和 assets.json 重算，结果一致。 |
| 19 | minor | **已修** | 描述第 2 行就是 AI 声明，用词统一为「AI-generated … not photos」，与卡上一致。 |
| 20 | — | — | 不需要改。 |

另外核对了 handoff 里列出的其他改动：
- 「Next: Sabancaya」洞察卡的 after_rank 已改为 18，落在 #18 Licancabur 和 #17 Sabancaya 之间（`M_222.50.jpg`）。
- 封面 `render/thumbnail.png` 显示 #17 / #19 / #50，三张都是可商用实拍，名次与 data.json 一致。
- publish.md 的章节点（1:08 #40、2:16 #30、3:24 #20、4:32 Top 10、5:52 计分板）与 timeline 算出的卡片居中时间（68.33 / 136.33 / 204.33 / 272.57 / 351.1 s）对得上。

### 新问题（这次返修带来的或复核中新发现的）

| # | 严重度 | 版本 | 位置 | 证据 | 建议 |
|---|---|---|---|---|---|
| N1 | major（观感） | 默认版 | #1 冠军卡（约 5:45–5:51）及 #2、#5、#6、#9、#12、#13、#48 | NASA 图多数是 ISS 垂直俯视的局部。冠军卡上是一片雪斑和沟壑纹理，看不出是一座山，也看不出它是最高的那座（`M_346.00.jpg`）。#12 Aracar 灰雾很重，几乎是一片粉灰（`M_259.67.jpg`）；#9 Pular、#48 Tata Sabaya 也一样认不出来。只有 #7 Parinacota 的斜视图一眼能看出是火山。图是真的，数据也没错，但冠军停留这 6 秒的视觉高潮弱了。 | 不阻断发布。可以：①把 #1、#2 裁到峰顶火山口附近，让锥体占满卡；②在署名或副标题里写「Seen from the ISS」，让观众知道这是太空俯视；③NASA EO 如果有 Ojos del Salado 的斜视图，优先换上。 |
| N2 | minor | 两版 | 片尾来源卡 | 没有 AI 声明（见原问题 5）。 | 加一行「29 of 50 images are AI-generated illustrations」。风险版改为 8。 |
| N3 | minor | 文档 | `topic.md`「风险」2、4 和「待用户确认」4、5 | 还写着「San José −3.5%」（现在 GVP 与 Wikipedia 同为 5,856 m，差 0%）、「Codex 生成图 39 张」「真实照片 43 张」「#21 Miñiques」（现在是 #20）。 | 按现数据改：29 张 AI、风险版 32 张风险图，Miñiques 改为 #20。这些只在内部文档里，不上屏。 |
| N4 | minor | publish.md | Upload checklist 第 3 条 | 写的是「卡上标 Illustration / Render」，而实际卡上是「AI IMAGE」。 | 改成「AI IMAGE」。只是内部清单。 |
| N5 | minor | 描述框 | scope_note | 「San Jose uses the 5,856 m …」少了重音，片中和其他地方都写 San José。 | 改成 San José。 |

**名次和洞察卡的回归检查**：没有发现新问题。名次 1–50 连续，没有跳号或重号。6 张洞察卡的 after_rank（43 / 34 / 26 / 18 / 9 / 3）都落在对应的卡后面，timeline 计算和抽帧一致。全部抽帧里，居中的卡和洞察卡都没有文字出框、截断或省略号。只有屏幕两侧半露的邻卡被画框切掉，那是滚动造成的，不是排版问题。国旗与 country_iso2 一致。

### 成片技术核对（重渲版）

| 项 | 默认版 | 风险版 |
|---|---|---|
| 时长 / 帧数 | 380.100 s / 22,806 帧 | 同 |
| 分辨率 / 帧率 | 1920×1080 / 60 fps（h264） | 同 |
| 与 `python -m rank_scroll timeline` 对照 | total 380.10 s = 22,806 帧，分段 intro 0–5 / scroll 5–345.1 / champion 345.1–351.1 / tally 351.1–358.1 / sources 358.1–362.1 / end 362.1–380.1，完全一致 | 同 |
| 音轨 | aac，静音 −91 dB | 同 |
| manifest | output 和 52 个输入的 sha256 全部与现文件一致 | 同 |

### 抽帧清单（`_build/qc/recheck/`）

- 默认版 44 帧（`M_<秒>.jpg`）：
  - 片头：1.5、3.0、4.8、6.0；
  - 改动过的卡：#48 13.0、#47 19.33、#45 32.0、#44 38.33、#43 44.67、#42 55.67、#40 68.33、#34 106.33、#33 117.33、#25 172.67、#24 179.0、#23 185.33、#20 204.33、#18 217.0、#17 228.0、#13 253.33、#12 259.67、#11 266.0、#9 279.37、#7 297.63、#6 304.43、#5 311.23、#4 318.03、#3 324.83、#2 336.3；
  - 洞察卡：50.17、167.17、222.5、330.57；
  - 冠军：346.0、350.5；计分板：354.0、357.8；来源卡：360.0；片尾：370.0；
  - 随机 5 点（seed 20261104）：76.08、82.53、131.08、206.05、256.83。
- 风险版 18 帧（`R_<秒>.jpg`）：片头、#45/#44/#43、#42、#25/#24/#23、#20、#18、#13、#11、#4、#3、#2、冠军、计分板、来源卡。
- 拼图：`tile_M_01…11.jpg`、`tile_R_01…05.jpg`，每张 4 帧缩小拼接，左上角是文件名。

## 第 1 轮独立审片 · 2026-11-04

> 独立审片人（未参与制作，另起上下文），按 `bible.md` §6 ⑥ / §7 与审片说明执行。只写本文件和 `_build/qc/`，未改数据、图片、渲染。
> 审片对象：`render/ep14_highest_volcanoes_master.mp4`（默认版，sha256 e309b2d2…）与 `render/ep14_highest_volcanoes_master_with-risk-images.mp4`（风险版，sha256 478240c6…）。两份 manifest 记录的 `data.json` / `assets.json` sha256 与现文件一致（handoff 里「母版 manifest 与现 data.json 差 thumb 字段」的提示已不成立）。

### 结论：**必须修**（1 个 blocker 影响两版；风险版另有 2 个 blocker）

- 数据主体可靠：50 条主值、国家字段、最近喷发年当天重新从 GVP 官方 WFS 拉取，**50/50 一致**；排序、名次连续无误。
- 但 **#14 San José 的 6,070 m 实际是邻峰 Marmolejo 的高度**（GVP 自己的地质概述写 San José 5,856 m），必须改值重排后重渲。
- **AI 图问题**：默认版 50 张卡里 39 张（78%）是逼真的 AI 生成风景，包括冠军 #1 和前 7 名里的 6 张；卡上标注只有底部最小号一行「Photo: AI-generated image (Codex)」，手机上看不清，而且写的是「Photo」。**不建议原样发布默认版**，也**不建议把风险版当发布主版本**（33 张未获许可，其中 #25 认错了山、多张构图差）。建议路线见「对 AI 图与两版的建议」。
- 口径（Holocene-only、Kilimanjaro 不在榜）讲得清楚，洞察卡 1 能接住；但「Holocene status unclear」标签和国旗计分规则会让观众困惑，洞察卡 3、6 还提前泄露了计分板结果和冠军名字。

### 问题清单

| # | 严重度 | 版本 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|---|
| 1 | **blocker** | 两版 | #14 San José（约 4:12） | GVP WFS 的 Elevation 字段是 6,070，但 GVP 同一条目的 Geological_Summary 写明「The glaciated **6070-m-high Marmolejo** stratovolcano… **San José is a 5856-m-high** stratovolcano」。Wikipedia 也是 5,856 m。字段值属于同组的 Pleistocene 火山 Marmolejo，不是 San José。 | `items_def.py` / `build.py` 对 San José 用 5,856 m（来源写「GVP Geological Summary」，notes 记 WFS 字段 6,070 的问题）。重排后 San José 落到 #24（Taapaca 5,860 与 Cordón de Puntas Negras 5,852 之间），原 #15–#24 各上移一位；洞察卡 4「Next: Sabancaya」的 `after_rank` 从 19 改为 18（Sabancaya 变 #17）；封面 #18 → #17；重跑 `gen_sources.py`、publish、两版重渲。scope_note 里「全部取 GVP 值」改为「GVP values (one corrected from GVP's own summary)」。 |
| 2 | **blocker** | 风险版 | #25 Cordón de Puntas Negras（约 2:58） | 风险图来源页是 Andeshandbook「**Miscanti**」页（`/cerro/1123/miscanti`），页面写明是 Volcán Miscanti 5,622 m，Puntas Negras 是「位于其东侧的另一组山」。画面主体是 Laguna Miscanti 后面的 Cerro Miscanti。 | 风险版不能用这张。要么另找 Puntas Negras（Laguna Tuyajto / Piedras Rojas 一带的黑色锥群）实拍，要么风险版也用 AI 图。 |
| 3 | **blocker** | 风险版 | 全片 33 张风险图 | 许可不明 18 张、来源页「todos los derechos reservados」14 张、Pixnio 1 张。卡上署名直接显示「licence unknown」「all rights reserved」。 | 未逐张取得书面许可前不得发布风险版（handoff 已列为用户签字项，这里确认仍是 blocker）。Andeshandbook 一家就占 18 张（14 张明示 + 4 张 unknown 也来自该站），优先统一联系授权。 |
| 4 | major | 两版 | #19 Licancabur（约 3:31） | Unsplash 原页确认地点 San Pedro de Atacama、描述「El volcán Licancabur」。但构图是在 Hito Cajón 一带拍的：**画面主体是近处的大山 Juriques**（平截的火山口顶），Licancabur 是左侧远处较小的锥体。渲染器按中心裁切后，卡片几乎只剩 Juriques，Licancabur 只露左边缘。 | 加 `image_focus: [0.0, 0.4]` 至少让左侧锥体完整进卡；更好是换一张以 Licancabur 为主体的可商用图（San Pedro 方向的正面锥体是最常见视角）。 |
| 5 | major | 默认版 | 39 张 AI 卡（全片） | 卡上 AI 标注只在最底一行最小号字（1080p 下约 10 px 高），手机全屏读不出；文字是「**Photo:** AI-generated image (Codex)」，自相矛盾。片尾来源卡只写「Photo credits: shown on each card」，没提 AI。 | 在国旗下方加一个与 SHARED WITH 同款的徽章「AI IMAGE」或「AI ILLUSTRATION」；署名行改为「AI-generated image, not a photo」；来源卡加一行「39 of 50 images are AI-generated illustrations」。需要改渲染器或 data（徽章字段已有）。 |
| 6 | major | 默认版 | #7、#44、#24、#40、#47 等 | 多张 AI 图实际在仿造真实的标志性场景：#7 = Parinacota 与 Pomerape 倒映在 Chungará 湖（几乎是那张名片照），#44 = 伊斯卢加白色教堂 + 羊驼，#24 = 普特雷村 + 梯田，#40 = 乌比纳斯村梯田。观众会当成真实照片。另有 #2 Llullaillaco、#4 Incahuasi、#45 Yucamane 被画成完美雪锥，与真山外形明显不符（真 Llullaillaco 见风险图，山顶嶙峋）。 | 见下节建议；至少 #1–#7 这些头部卡不该用仿真照式 AI 图。 |
| 7 | major | 两版 | 洞察卡 6（after #3，约 5:20） | 「Both of the top two have erupted: **Ojos del Salado** around 750 CE, Llullaillaco in 1877」出现在 #2、#1 之前，提前说出冠军名字，破坏「看到最后才知道冠军」（Vision）。 | 移到 #1 之后（冠军停留期间或计分板前），或改写成不点名：「The top two have both erupted in the last 1,300 years.」 |
| 8 | major | 两版 | 洞察卡 3（after #26，约 2:52）+ 计分板 | 「Chile flies 30 of these 50 flags」在第 2:52 就公布了计分板最终结果，D3 悬念线失效。而且 30 有 18 座来自 GVP 国家字段的书写顺序（Chile-Argentina 一律智利在前），阿根廷、玻利维亚观众会认为计分不公：#1 Ojos del Salado、#2 Llullaillaco 只挂智利旗。 | 二选一：(a) 计分板把跨境火山同时计入两国（Chile 30 / Argentina 17 / Bolivia 6，标题加「border volcanoes count for both」），卡上并列两面国旗；(b) 维持现规则，但洞察卡 3 改成不报总数，例如「18 of these sit right on a national border.」，计分板留到结尾揭晓。推荐 (a)，更符合「替自己的国家加油」。 |
| 9 | major | 两版 | 7 张「Holocene status unclear」卡（#4、#9、#21、#22、#29、#33、#47） | 洞察卡 1 说 Kilimanjaro 落选是因为「no known eruption in the last 11,700 years」，同一片里 #4 Incahuasi 等卡写着「Holocene status unclear」却在榜，观众会问「为什么它们能进」。#47 Corrida de Cori 的 GVP 概述还写着测得的年龄约 34 万年。#33 Olca-Paruma 在 GVP 是 *Eruption Observed*（无年份），却因标签规则落到「unclear」，属于标签 bug。 | 标签改为「Possible Holocene activity」，scope_note 补一句「includes 6 volcanoes GVP lists with uncertain Holocene evidence」；Olca-Paruma 改为「Eruption date unknown」或「Historical eruption reported」。洞察卡 1 可改为「No Kilimanjaro? It isn't on GVP's list of volcanoes active in the last 11,700 years.」，与在榜的不确定项不冲突。 |
| 10 | major | 两版 | 全片音轨 | 音轨为静音（volumedetect mean = max = −91 dB）。系列配乐受 Suno 验证码阻塞（README ⛔），属已知状态。 | 与 ep02 一样可作「静音画面版」放行，但发布前应补配乐重渲；按 bible §5 需要配乐。 |
| 11 | minor | 风险版 | #11 Sierra Nevada（约 4:24） | 裁切后山体被云和底部信息块遮住，卡片主体是天空和云团；原图左上还有传感器灰斑。 | 换图或设 `image_focus` 下移；Andeshandbook 同页其他照片可选。 |
| 12 | minor | 风险版 | #13 Guallatiri（约 4:18） | 竖卡中心裁切把火山推到右边缘、被切掉一半，画面主体变成教堂废墟。 | `image_focus: [0.65, 0.4]`。 |
| 13 | minor | 风险版 | #42 Láscar（约 0:58） | 1024×666 低清，裁切后右侧的 Aguas Calientes 锥体比 Láscar 本体（左侧冒气的山）更显眼，观众容易把锥体当成 Láscar。 | `image_focus` 左移到冒气处，或换图。 |
| 14 | minor | 风险版 | #3 Tipas、#24 Taapaca、#9 Pular、#34 Purico、#45 Yucamane、#40 Ubinas | #3 一半画面是近景碎石坡；#24 火山很小，大半是云；#9 主体是盐湖和火烈鸟，火山在远处；#34 山很远；#45 像网络摄像头截图，偏糊；#40 过度锐化、偏色。 | 若风险版要发，逐张换图或调焦点。 |
| 15 | minor | 两版 | #43 Pico de Orizaba | 竖幅航拍，焦点 y=0.4 下卡片上半是空天，山体偏小。 | `image_focus: [0.5, 0.55]`。 |
| 16 | minor | 默认版 | AI 图整体 | 39 张同一配方（晴空 + 雪顶锥 + 盐湖或湖 + 黄色针茅），连续滚动时显得重复，像「AI 风景图集」。未见明显 AI 瑕疵（手、文字、结构错乱等），#47 后景雪锥不是 Corrida de Cori 本身（它是前景的黑色小锥群），主体有歧义。 | 若保留 AI 图，生成 prompt 加入每座火山的真实外形特征（Llullaillaco 嶙峋山顶、Ojos del Salado 宽阔山体等），去掉教堂、村庄等可识别地标。 |
| 17 | minor | 数据 | #41 Guayaques | GVP 5,598 m，Wikipedia 5,076 m（−9.3%，接近 bible §3.4 的 10% 阈值）。GVP 概述没给海拔，无法像 San José 那样用 GVP 自身文本判断。 | 维持 GVP 值，按 topic.md 待确认项由用户定；可在置顶评论预先说明。 |
| 18 | minor | 文档 | `sources.md` §5 | 写「AI 生成图 39 张（33 张作风险图的 image_alt，7 张 AI-only）」，33 + 7 = 40；实际是 32（Purico 用 ESO 图）。 | 改成 32。 |
| 19 | minor | 包装 | `publish.md` 描述 | AI 声明放在描述第 5 段之后，首屏看不到；描述称它们是「illustrations」，卡上却写「Photo」。标签含「Kilimanjaro」，但它不在榜（片中有解释，问题不大）。 | 在描述第二行写明「39 of the 50 volcano images are AI-generated (marked on each card)」；卡上和描述的用词统一。 |
| 20 | minor | 两版 | 洞察卡 | 屏上无出处（sources.md §4 已逐条核过，并不缺依据）。与系列其他期一致，可不改。 | — |

已核实**无问题**的项（handoff 中原列为待核）：#30 Antisana（Unsplash 页标注 Antisana, Ecuador）、#18 Sabancaya（摄影师写明在 Hualca Hualca 上拍 Sabancaya 喷发）、#8 Chimborazo、#37 Elbrus（Gum Bashi 观景台）、#50 Popocatépetl、#35 Damavand（地点 Damavand, Iran，外形吻合）、#21 Miñiques（Pixnio 标题「Laguna Miñiques… volcano Miñiques in the background」，主体正确）。#34 默认版替代图（ESO potw1215a「All around Chajnantor」360° 全景的截取）拍的是 Purico 火山群一带（Chajnantor / Toco），可接受，但画面里有微波天线塔，地点辨识度低。#4、#9、#16、#34 原图上的水印 / 署名（AEX、© 摄影师名）都在竖卡裁切范围之外，渲染画面里看不到。

### 对 AI 图与两版的建议

**默认版现状不可接受，风险版也不能当发布主版本。**

- 默认版合法，但 78% 的卡是逼真的 AI 风景，冠军和前 7 名里 6 张是假的，仿造了 Chungará 湖、伊斯卢加教堂这类真实名景，卡上 AI 标注又几乎看不见。这与本系列 Vision「数字真实、有出处」冲突。观众一旦认出（安第斯观众会认出 Parinacota 和 Llullaillaco 不长这样），评论区会转向「AI slop / fake」，可信度在头部卡上受损最大。
- 风险版图更真，但 33 张未获许可，卡上直接写着 all rights reserved；#25 认错山；#11、#13、#24、#3 构图差。
- **推荐路线**（按投入从小到大）：
  1. 先修 #1、#5（标注改成显眼的 AI 徽章，用词改为「not a photo」），再修 #7、#8（洞察卡泄露），并修 blocker #1（San José）。做完这些，默认版可作为「合法但打了折扣」的版本发布。
  2. 用公有领域的真实影像替换头部 AI 卡：NASA Earth Observatory、ISS 宇航员照片（eol.jsc.nasa.gov，美国政府作品，公有领域，不违反「不用维基共享资源」的规定）里有 Ojos del Salado、Llullaillaco、Parinacota、Láscar、Sabancaya、Ubinas、Incahuasi 一带的高清斜视或航拍。不如地面照漂亮，但是真的，适合满版卡。至少换掉 #1–#7。
  3. 统一联系 Andeshandbook（Sociedad Geográfica de Documentación Andina）申请这 18 张图的使用许可。拿到书面授权后，风险版扣除 #25 和低质图，大部分就能转正。Flickr CC 搜索当时只是被限流，换时段重试也值得一做。
- 如果必须二选一、不再找图：发**默认版**（法律上安全），但第 1 步必须先做。

### 口径与观众困惑

- **Kilimanjaro 不在榜**：洞察卡 1 在约 0:55 直接回答，描述框 scope_note 写了 Sajama、Tupungato，处理得当。唯一冲突是问题 9 的「Holocene status unclear」标签，修完即可。
- **跨境国旗**：见问题 8。#1、#2 两座最受关注的火山只挂智利旗，SHARED WITH 徽章字号小，阿根廷观众（这类片的主要观众之一）大概率会在评论区争论。双旗加双计数是最省事的解法。
- 片头口径行「Summit elevation · Smithsonian GVP data」没出现「Holocene / active」字样。一般观众默认「最高火山」包括 Kilimanjaro、Sajama。建议把片头口径行改成「Active (Holocene) volcanoes by summit elevation · Smithsonian GVP」，让口径在第一秒就清楚。

### 观众视角（全球英文观众）

- **亮点**：#1 Ojos del Salado（多数人不知道世界最高火山是它）；「Chimborazo 离地心最远」「Mauna Kea 从海底量 10,200 m」两张洞察卡；3 座 2026 年仍在喷发的火山带 ERUPTED IN 2026 徽章；Sabancaya 喷发柱的画面很抓人。
- **会划走的地方**：0:00–2:30 连续 20 多张智利、阿根廷冷门名字配相似的雪锥图（默认版尤其如此，AI 图同质），没有声音，信息变化少；第 2:52 洞察卡提前公布了计分板；第 5:20 洞察卡提前说出冠军。
- **反常识点**可以再强化：「Chile 30」改成双计数后，阿根廷 17 是第二悬念；「最高的 50 座火山里 46 座在安第斯」值得做成一张洞察卡。

### 核对过的数据样本

当天（2026-11-04）用 WebFetch 直接查询 GVP 官方 GeoServer WFS（`GVP-VOTW:Smithsonian_VOTW_Holocene_Volcanoes`，Elevation > 5,370），返回 51 座（含 #51 Ticsani），与 `data.json` 逐条比对。

| # | 火山 | 屏上值 | GVP WFS（11-04 实取） | 其他核对 | 结论 |
|---|---|---|---|---|---|
| 1 | Ojos del Salado | 6,879 m · Chile/Arg · c. 750 CE | 6879 · Chile-Argentina · 750 | GVP 概述 6,879 m | ✓ |
| 2 | Llullaillaco | 6,739 m · 1877 | 6739 · Chile-Argentina · 1877 | — | ✓ |
| 3 | Tipas | 6,658 m · Argentina | 6658 · Argentina · null | GVP 概述：世界第三高的活火山，峰顶在阿根廷 | ✓ |
| 4 | Incahuasi | 6,638 m | 6638 · Chile-Argentina · null | — | ✓ |
| 5 | Coropuna | 6,377 m · Peru | 6377 · Peru · null | — | ✓ |
| 8 | Chimborazo | 6,261 m · c. 550 CE | 6261 · Ecuador · 550 | 距地心 6,384.4 km、比 Everest 远约 2.1 km（Wikipedia / Guinness） | ✓ |
| 14 | San José | 6,070 m | 6070 · Chile-Argentina · 1960 | **GVP 概述：San José 5,856 m，6,070 是 Marmolejo**；Wikipedia 5,856 m | ✗ 问题 1 |
| 18 | Sabancaya | 5,960 m · 2026 | 5960 · Peru · 2026 | — | ✓ |
| 20 | Cotopaxi | 5,911 m · 2023 | 5911 · Ecuador · 2023 | — | ✓ |
| 35 | Damavand | 5,670 m · 5350 BCE | 5670 · Iran · −5350 | — | ✓ |
| 37 | Elbrus | 5,642 m · c. 50 CE | 5642 · Russia · 50 | — | ✓ |
| 41 | Guayaques | 5,598 m | 5598 · Chile-Bolivia · null | Wikipedia 5,076 m（−9.3%） | ✓（有争议，问题 17） |
| 42 | Láscar | 5,592 m · 2026 | 5592 · Chile · 2026 | 2026-02-08 灰气排放（VAAC，约 6,400 m），2026-03-05 SERNAGEOMIN 升黄色预警 | ✓ |
| 50 | Popocatépetl | 5,393 m · 2026 | 5393 · Mexico · 2026 | 第 51 名 Ticsani 5,382 m，边界正确 | ✓ |
| 洞察 1 | Kilimanjaro | Pleistocene | GVP Pleistocene 表 222150，5,881 m；概述称最近火山活动约 15–20 万年前 | — | ✓ |
| 洞察 2 | Mauna Kea | 约 10,200 m | — | Guinness 约 10,205 m | ✓ |
| 洞察 3 | Chile 30 / 边境 18 | — | 本地统计 CL 30，其中 Chile-Argentina 13、Chile-Bolivia 5 | — | ✓（但见问题 8） |

其余 36 条（#6、#7、#9–#13、#15–#17、#19、#21–#34、#36、#38–#40、#43–#49）的海拔、国家字段、最近喷发年同样与 WFS 实取一致。另用本地 `raw/gvp_holocene.json` 独立排序，前 50 名单与顺序与 `data.json` 一致，无并列；计分板 CL 30 / PE 7 / AR 4 / EC 4 / MX 2 / IR 1 / RU 1 / BO 1 与卡片国旗一致。

### 成片技术核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 时长 | 380.100 s（6:20.1） | 380.100 s |
| 分辨率 / 帧率 | 1920×1080 / 60 fps | 同 |
| 帧数 | 22,806 = 380.1 × 60，与 manifest 时间线一致（intro 0–5、scroll 5–345.1、champion 345.1–351.1、tally 351.1–358.1、sources 358.1–362.1、end 362.1–380.1），未截断 | 同 |
| 音轨 | aac，静音（−91 dB） | 同 |
| sha256 | 与 manifest 一致 | 与 manifest 一致 |

画面：文字均未出框，没有截断或省略号；国旗与国家一致（50 张逐一看到）；没有占位卡；计分板逐卡累计正确，结尾 8 国条形图与数据一致；冠军光晕和 No. 1 面板正常；来源卡、片尾正常。publish.md 的章节时间点（1:08、4:32、5:41、5:52）与画面对得上。标题 44 字符，不超过 60。封面用 3 张可商用实拍（#18、#20、#50），合格；问题 1 修完后 Sabancaya 的名次标签要从 #18 改为 #17。

### 抽帧清单

都在 `_build/qc/frames/`（`M_` = 默认版，`R_` = 风险版，文件名为秒数），每版 47 帧：
- 片头：2.0、4.5；
- 滚动段每 9 s 一帧：9.0–342.0（覆盖全部 50 张卡和 6 张洞察卡：54 / 108–117 / 162–171 / 216 / 288 / 324–333 等）；
- 前 10 名：279–342；冠军：347.0、350.0；计分板：354.0、357.5；来源卡：360.0；片尾：366.0、378.0。
- 拼图：`_build/qc/tile_M_01…12.jpg`、`tile_R_01…12.jpg`（每张 4 帧，拼缝处的文字重叠是拼图造成的，不是成片问题）；上屏原图拼图 `_build/qc/real_1…8.jpg`（43 张实拍）、`gen_1…5.jpg`（39 张 AI 图 + ESO 替代图）；脚本 `_build/qc/qc_sheet.py`、`grab.sh`、`tile.py`。
