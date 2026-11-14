# ep18 · Fastest Production Cars · 审片记录（qc.md）

## 复核 · 2026-11-04（返修后，独立上下文）

> 另起上下文复核，没有参与制作，也没写第 1 轮审片。对照第 1 轮问题清单和 `_build/handoff.md`「第 1 轮审片后修订」，逐条核对当前 `data.json` / `assets.json` / `sources.md` / `publish.md` 与两版成片。只写本节和 `_build/qc/recheck/`，没有改数据、图片和渲染，没有调用收费服务。
> - **规格**（ffprobe）：两版都是 1920×1080、60/1 fps、16,723 帧、278.717 s，有 AAC 音轨（静音，系列设计）。`python -m rank_scroll timeline` 也是 16,723 帧、278.72 s（intro 0–5 → scroll 5–243.72 → champion → tally 249.72 → sources 256.72 → end 260.72–278.72），三者一致。两份 manifest 的 output sha256 与文件一致，32 个输入 sha256 与当前文件逐个一致，`draft=false`，所以成片就是按当前数据渲的。`validate --strict` 通过（30 项，6 张洞察卡）。
> - **抽帧**：`_build/qc/recheck/m/`（默认版 42 帧：片头 1/3/4.2/5/6/7.4/8 s，每张洞察卡，改过的卡 CCX / Jesko / Dauer / #10 / Czinger / Tuatara / F1 / ZR1 / Divo / Centodieci，冠军 240/246/249 s，计分板 253 s，来源卡 258.5 s，片尾 265/278 s；随机点 62.1/67.3/106.2/166.4/207.2 s，种子 20261104）。`r/`：风险版 7 帧。拼图是 `s_*.jpg`，局部放大是 `crop_*.png`，`tl.py` 用来算每张卡的进出时间。

### 复核结论：**小修后发布**。推荐发**默认版**

- blocker B1 已修，6 个 major 里 M1、M5、M6 已修，M2–M4 按第 1 轮给的兜底办法做了（在署名里标明图上是哪个版本），没有换图。成片里没看到名次断档、洞察卡错位或文字出框。
- **推荐默认版**。理由：许可干净；三张版本不对的图都在卡上署名和 publish.md 里写明了；唯一一张 AI 图有黄色「AI IMAGE」标记，publish.md 的合成内容声明也改成了 Yes。改完 n1 就能发。
- **风险版对观众更好**（#1、#10、#14 是对的车，#6 是实拍，没有 AI 图），但发之前要满足三条：① 用户对 7 张许可不明的图签字；② 先向 BYD 核实 #1 那张图是不是渲染图（m16）；③ 用 `--allow-risk-images` 重新生成 publish.md，因为现在这份写的是默认版的署名，还写着有 AI 图。三条都做到，就改发风险版。
- 发布前要做的小修：n1（sources.md 里有几段过时的说明，必须改）。n2–n5 可修可不修。m15（Tourbillon 是否已交付）在发布前 7 天复核。

### 原问题逐条

| # | 原问题 | 复核结果 | 依据 |
|---|---|---|---|
| B1 | 漏了 Koenigsegg CCX | **已修** | data 里 #16 是 CCX，400 km/h，CLAIMED，2006，「30 built」，主源是官网 CCX 页。N = 30，名次 1–30 连续，并列是 #20 ×2、#25 ×3，按 1,1,3 式排。VERIFIED / CLAIMED 各 15，和洞察卡一致。计分是美 7、法 6、瑞典 5、英 4、德 3、意 3、中 1、克 1，合计 30，计分板（253 s）和页眉一致。标题、kicker、片头都是 Top 30（3 s、8 s 两帧）。CCX 卡（116.6 s）是蓝色 CCX 实拍，署名对 |
| M1 | Jesko Absolut 约 412 km/h | **已修**（选了方案 ①） | #12 是 412 VERIFIED，tag「Peak in 0-400-0 test」，主源是 Koenigsegg 新闻稿（racecar.com 转载），交叉源是 GoAuto。卡（144.6 s）显示 Örebro、tag、2024 run。置顶评论写了收录理由，也写了 531 km/h 是仿真。sources.md 的口径段还写着「不入榜」，见 n1 |
| M2 | 默认版冠军卡是标准版 U9 | **部分修** | 图没换，仍是标准版 U9 近景（246 s）。卡上署名末尾加了「standard U9 shown」，但字只有约 10 px，手机上看不见。publish.md 两处署名也注明了。这是第 1 轮认可的兜底办法，可以发；彻底解决要靠风险版或拿到授权图 |
| M3 | 默认版 #10 是标准版 Nevera | **部分修** | 做法同 M2，卡上写「standard Nevera shown」（158.8 s） |
| M4 | 默认版 #14 Dauer 是 1994 年勒芒赛车 | **部分修** | 做法同 M2，卡上写「1994 Le Mans race car shown」（130.6 s），图仍有运动模糊、大半是轮胎墙 |
| M5 | 默认版 #6 Czinger 是占位卡 | **已修** | 换成 AI 生成的整车图 `06_czinger_21c_gen.png`。卡上 CLAIMED 下面有黄色 **AI IMAGE** 标记，署名写「AI-generated image, not a photo」（194 s，`crop_czinger_194.png`）。图上没有车标和牌照。账本 licence 写的是「AI-generated (Codex image_gen)」，request_log 有这次调用的记录，publish.md 合成内容声明改成 Yes。风险版这张卡是 Goodwood 实拍，没有 AI 标记，这是对的 |
| M6 | 口径交代太晚 | **已修** | 片头和页眉都写「Top speed · VERIFIED one-way run or maker CLAIM」。scope_note 和置顶评论第一段讲明单向规则，点名 Guinness 双向纪录是 Tuatara 455 km/h，并列出没收的车和理由。#3 后的洞察卡也讲了 455 双向纪录 |
| m1 | Centodieci 默认图只有车尾 | **未修** | 76.4 s 那帧仍只有车尾右后角。handoff 说找不到可商用的整车图 |
| m2 | Divo 构图 | **部分修** | 焦点改成 [0.4, 0.8]，整车能看到（83.4 s），但上半张卡仍是绿篱 |
| m3 | Chiron 构图 | **未修** | 楼梯仍占上半张卡（234.2 s）。车型和车身都对，可以接受 |
| m4 | Tuatara 用的是 Striker 版 | **未修** | 车型对，可以接受 |
| m5 | ZR1 测速地点 | **已修** | notes 改成 ATP Papenburg，2024-10，双向 233.08 / 233.50 mph，并写明图上是敞篷加 ZTK |
| m6 | Tuatara 的 tag | **已修** | 卡上是「2021 2-way avg 455 · 2022 run」（221.6 s） |
| m7 | F1 和 U9 的原型车标注 | **部分修** | U9 卡上显示「Prototype record car」（246 s）。F1 的 data 里加了「XP5 prototype, 1998」，但卡上的信息行放不下，被渲染器丢掉了，屏幕上只有「Ehra-Lessien, Germany · 2-way avg 386 km/h」（`crop_f1_97.png`），见 n2 |
| m8 | 918 / F5 计时方说法不一 | **已修** | notes 写清楚了：918 由 JBPG 自己的设备计时，F5 是 Hennessey 自己的 VBOX，没有独立计时员 |
| m9 | Dauer、EB110 来源偏弱 | **部分修** | Dauer 主源换成 Auto Bild，notes 写了 402 和 404.6 两个数，以及「period press measurement」。EB110 的主源还是 Wikipedia，没有补拍卖页作佐证 |
| m10 | Czinger 数值有两种说法 | **已修** | notes 写了 253 和 281 两说，tag 改成「Low-drag spec」 |
| m11 | 第一张卡停留不到 3 s | **已修** | intro_hold = 2.5。#30 约 4.6 s 落位，7.67 s 左边缘开始出画，完整可读 3 s 以上（4.2、5、7.4 s 几帧） |
| m12 | 章节时间码 | **已修** | 时间码是 0:00 / 2:27 / 3:50 / 4:09。按 timeline 算：#10 约 147 s 进场，154.6 s 完整；#1 约 230 s 进场；计分板 249.7 s 开始。4:09 比计分板早 0.7 s，可以接受 |
| m13 | 署名与描述 | **已修** | 三处 pictured 说明都加了，描述改成「in the pinned comment thread」 |
| m14 | sources.md 有过时条目 | **已修** | 不存在的 `06_czinger_21c_alt.jpg` 那行已删掉。但其他段落有新的过时内容，见 n1 |
| m15 | Tourbillon 交付状态 | **待发布前复核** | 洞察卡没变，发布前 7 天复核 |
| m16 | 风险版 U9 图疑似渲染图 | **未修**（等用户） | 风险版 246 s 那帧仍是红黑「02」涂装、后期很重的图 |
| m17 | Saleen 无法确认是 Twin Turbo | **未修** | 可以接受 |

### 新问题

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| n1 | minor（发布前须修，不影响画面） | sources.md §1、§3、§4 | `gen_sources.py` 重新生成了表格，但正文还是旧的：§1 写「Jesko Absolut…所以不入榜」，又写「N = 28」「Divo / Centodieci 并列 18；Countach / Aventador / EB110 并列 23」；§3 写「第 28 名 Porsche 918」「无官方数字：Jesko Absolut」，「资料不足未收：Koenigsegg CCX / CCXR（无可靠官方最高时速）」；§4 里 #3 洞察卡的依据还是旧卡的内容（Jesko 官网「Time will tell」），after 28 / 23 / 17 三张卡的依据是空的。这些都和 data.json 矛盾 | 改 `gen_sources.py` 里的这几段固定文字，再重新生成：N = 30，并列 20 / 25，第 30 名是 918；Jesko 以 412 入榜；把 CCX 从「未收」里删掉，CCXR 单独说明；补上 4 张洞察卡的依据 |
| n2 | minor | #18 McLaren F1（97.4 s） | 卡上有 subtitle 和两个 tag，一行放不下，渲染器把「XP5 prototype, 1998」丢了。m7 想让观众看到这是原型车，现在看不到 | 删掉 subtitle「Ehra-Lessien」，或者把 tag 改短（比如「XP5 prototype」）后重渲 |
| n3 | minor | #6 Czinger AI 图 | 卡上 tag 写「Low-drag spec」，AI 图画的却是装大尾翼的高下压力外形，和 281 mph 低阻配置对不上 | 可以接受，图上已经标了 AI IMAGE。要重新生成的话，提示词写低阻、无大尾翼 |
| n4 | minor | #6 后和 #3 后两张洞察卡 | 间隔约 28 s，都在讲 Guinness 双向平均和 Tuatara 455，有点重复 | 可选：把 #6 后那张换成别的知识点，比如「Customer Chiron 300+ cars are limited to 440 km/h」 |
| n5 | 记录 | publish.md | 上传清单还写「卡上标 Illustration / Render」，实际卡上是「AI IMAGE」；描述里「1 images」语法不对 | 顺手改一下 |
| — | 观察，不算问题 | #16 CCX「250 mph」 | 400 km/h 换算是 248.5 mph，卡上的 250 是厂方公布的「250+ mph」。sources.md §1 规定 mph 取厂方或计时方公布值，所以符合口径。旁边 #15 Speedtail 403 km/h 也是 250 mph，有人可能会问 | 不改 |

改动有没有引入新问题：名次 1–30 连续，并列处理正确。洞察卡 after_rank 依次是 28 / 23 / 17 / 10 / 6 / 3，每张都插在对应名次的卡之后（23.2、63.4、110.5、165.1、200.3、227.9 s 几帧），内容和位置对得上。抽到的帧里没有文字出框，国旗正确，页眉的累计计数一路递增，最后和计分板一致。片头、来源卡、片尾（18 s，画面干净）都正常。

---

## 第 1 轮独立审片 · 2026-11-04

> 另起上下文的独立审片，没有参与制作。审的是当前的 `data.json` / `sources.md` / `assets.json` / `assets/img/`（含 image_alt），以及 `render/` 下的两版成片：默认母版 `ep18_fastest_cars_master.mp4` 和风险版 `..._with-risk-images.mp4`。两版 manifest 里记的输入 sha256 与当前文件逐个比对，全部一致，所以成片就是按当前数据渲出来的。
> 外部核对只用了 WebSearch / WebFetch，没有调用收费服务。没有改数据、图片和渲染。审片产物在 `_build/qc/`：拼图、抽帧、截取图，以及 `sheet.py`、`tile.py`、`tile2.py` 三个脚本。

### 结论：**必须修**（默认版不能直接发；风险版须修完数据项、并由用户对许可签字后才能发）

每项结论：

| # | 审查项 | 结论 | 一句话 |
|---|---|---|---|
| 1 | 数据 | **必须修** | 抽查的主值都对得上。但 Koenigsegg CCX 按本期口径应该入榜却漏了（官网写 400+ km/h，30 台），第 15–28 名都会变。Jesko Absolut 有 Racelogic 计时的约 412 km/h，要么收进来，要么在口径里写明不收的理由 |
| 2 | 图片 | **必须修**（默认版）/ 小修（风险版） | 默认版有三张图版本不对：冠军卡用的是标准版 U9，#10 用的是标准版 Nevera，#13 用的是 1994 年勒芒赛车。#6 是占位卡，#18 Centodieci 只拍到车尾局部。风险版 28 张车型都对，但其中 7 张许可不明 |
| 3 | 成片 | 通过（小修） | 两版都是 1920×1080、60 fps、15,733 帧、262.217 s，与 manifest 一致，没有截断。没有文字出框，国旗都对，计分板和揭晓也对。#28 只完整停留约 2.3 s，不到 3 s |
| 4 | 包装 | 小修 | 标题 52 字符。章节标签已改成「#28–#11」，但 Top 10 和 No. 1 两个时间码各晚了约 8 s。替代图在署名里被写成 Xtreme / Nevera R / 公路版 |
| 5 | 观众视角 | 小修 | 好看，VERIFIED / CLAIMED 的区分是真卖点。但口径直到 #26 后的洞察卡才解释；把「宣称值」和「实测值」放在一起排名，又把单向速度当官方纪录，都会在评论区被追问 |

### 问题清单

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| B1 | **blocker** | 数据，第 15 名附近（影响 #15–#28） | Koenigsegg 官网 CCX 页面写「400+ km/h (250+ mph) (without rear wing)」（https://www.koenigsegg.com/model/ccx ）。RM Sotheby's 引用的厂方产量：CCX 30 台、CCXR 9 台，共 49 台。按本期规则，「以上」按数字计、≥10 台、已交付，CCX 应以 400 km/h CLAIMED 入榜，排在 Speedtail 403 和 Saleen 399 之间。sources.md §3 写「无可靠官方最高时速」，与官网不符 | 在 `items_def.py` 补 CCX：400，CLAIMED，2006，「30 built」，图片另找。重排后 N = 29，Saleen 及以下名次各降 1；计分板瑞典变 4、与英国并列；洞察卡「14 / 14」改成「14 VERIFIED / 15 CLAIMED」；标题和 kicker 跟着改成 Top 29。也可以明确写「CCX 不收」并说明理由，但当前的理由不成立 |
| M1 | major | 数据，口径；#3 后洞察卡 | Jesko Absolut 2024-06 在 Örebro 做 0-400-0 测试时由 Racelogic 计时，峰值约 412 km/h（GoAuto 报道，Racelogic 英国总部核验时间；峰值只见单一来源）。本期 VERIFIED 的定义是「独立计时的最快单向速度」，不论是否专门跑极速；按这个定义，Jesko 家族约 412 km/h 应排在 #11 附近。洞察卡写「531 km/h 是仿真、从没全力跑过」，这句本身没错，但车迷会拿 412 来反驳 | 二选一：① 找到 Racelogic 或厂方的原始数据后以约 412 km/h VERIFIED 入榜；② 在 scope_note 和置顶评论里加一句「acceleration-test peaks not counted」，洞察卡改成「…its best timed speed so far is ~412 km/h, in an acceleration test」 |
| M2 | major | 默认版 #1 冠军卡（3:35–3:53） | `01_yangwang_u9_xtreme_alt.jpg` 在 Flickr 的标题是「Yangwang U9」，图是标准版 U9（展台立牌写 YANGWANG U9），不是 Xtreme。800 宽的卡裁下来，主要只剩鸥翼门和挡风玻璃，车身大半出画（抽帧 m_222.0、m_230.0）。冠军卡一错，评论区第一条就会是这个 | 默认版首选拿到 BYD 官方媒体库的书面许可（BYD 有 global media center，可以申请），或者找可商用的 Xtreme 实拍（2025 广州车展、2026 北京车展都有展出）。实在没有，就在卡上署名写「Pictured: standard U9」，并把焦点改成能看到整车。最好是用户签字后发风险版 |
| M3 | major | 默认版 #10（2:13–2:28，Top 10 第一张） | `10_rimac_nevera_r_alt.jpg` 在 Flickr 的标题是「Rimac Nevera (2024)」，是黑色标准版，没有 Nevera R 的固定大尾翼 | 同 M2：找可商用的 Nevera R 实拍（2024 年 Monterey、Goodwood 都有），或者署名标注「standard Nevera pictured」 |
| M4 | major | 默认版 #13（1:56–2:08） | `13_dauer_962_le_mans_alt.jpg` 在 Flickr 的标题是「Dauer 962 LM – … 1994 Le Mans」，拍的是 #36 FATurbo 涂装的勒芒赛车，不是上路注册的公路版；画面又有明显运动模糊，卡上大半是轮胎墙（m_120.0、m_125.0）。属于「赛车版冒充公路版」 | 换成公路版实拍（带牌照、黑黄或银色车身的那几台）。拿不到可商用图，就署名标注「1994 Le Mans race version pictured」；推荐发风险版（evo 那张是对的公路版，只是分辨率 1260×710 偏低） |
| M5 | major | 默认版 #6 Czinger 21C（2:50–3:00） | 前 6 名里唯一一张占位卡，写着「Photo withheld: licence unclear」，与 bible §4（follow-up 020）「每张卡都必须有高质量图」冲突。风险版里是 Goodwood 现场图 | 联系 Czinger 媒体部（press kit 一般允许编辑用途）或 Goodwood 拿书面许可；也可以在 Flickr / Wikimedia 再搜一轮「21C V Max」「Czinger Monterey」。都不行就交用户决定发风险版 |
| M6 | major | 片头与口径（全片） | 片头只有「Top speed · Data as of Nov 2026」，VERIFIED / CLAIMED 的含义要到 0:16 的洞察卡才解释。排名把宣称值（Czinger 452）放在实测值（Venom GT 435）之上，又用单向峰值（U9 496、Chiron 490）排冠亚军，而维基「production car speed records」认的官方双向纪录是 Tuatara 455.3 km/h（2021）、Agera RS 447.19 km/h。观众会质疑「排名混用宣称和实测」「#1 不是官方纪录」 | 片头口径行加一句（≤90 字符），例如「Ranked by fastest one-way run (VERIFIED) or maker figure (CLAIMED)」。置顶评论第一句写清 Guinness 双向口径，并点名双向纪录是 Tuatara 455 km/h。下面「口径意见」一节有完整建议 |
| m1 | minor | #18 Centodieci（默认版，1:12–1:22） | 替代图只有车尾右后角（尾翼、八孔进气），一眼认不出是 Centodieci（m_076.0）。车型本身是对的 | 换整车图，或者把焦点挪到前侧；风险版那张是对的 |
| m2 | minor | #18 Divo（1:16–1:26） | 裁切后上半张卡被修剪的绿篱占满，车只在下 1/3，车头被裁掉（m_076.0、m_082.0） | 把 `image_focus` 改成 [0.35, 0.8] 左右，或者换图 |
| m3 | minor | #2 Chiron SS 300+（3:30–3:53） | 楼梯和铁艺栏杆占了上 2/3，车在下方（m_222.0）。车型和涂装都对 | 焦点下移，例如 [0.5, 0.8] |
| m4 | minor | #3 SSC Tuatara（3:16–3:28） | 图是「SSC Tuatara Striker (2024)」，高下压力套件，带固定尾翼，不是跑纪录的低阻版；裁后车只占下 40%，上面是 Jeep 和旗帜（m_200.0） | 能找到标准低阻版的图就换；不换也可以，车型是对的 |
| m5 | minor | #20 Corvette ZR1（1:00–1:10） | 图是 ZR1 敞篷版，装了 ZTK 大尾翼；233 mph 是硬顶无 ZTK 的车跑的。sources.md 把测速地写成 Ehra-Lessien，实际是 ATP Papenburg，2024-10，双向 233.08 / 233.50 mph（Motor1、TFLcar 等多家报道） | 改 notes 里的地点和日期。能换硬顶图更好 |
| m6 | minor | #3 Tuatara 的 tag | 「2-way avg 455 km/h · 2022 run」把 2021 年 KSC 的双向平均和 2022 年客户单向跑写在一起，观众会以为 2022 那次就有双向平均 | 改成「2021 2-way avg 455」 |
| m7 | minor | #16 McLaren F1、#1 U9 Xtreme 的 tag | Chiron 300+ 标了「Pre-production car」，但 F1 的 391 是 XP5 原型车放宽转速限制后跑的，没有标；U9 Xtreme 纪录车的状态也没写 | F1 加「XP5 prototype」tag；U9 若确认是原型或预产车，同样标出 |
| m8 | minor | #28 / #7 口径执行 | 918 Spyder 的 218.4 mph 由 Johnny Bohmer Proving Grounds 计时，记作 VERIFIED；Venom F5 的 271.6 mph 也是在 JBPG 跑的，却记作 CLAIMED，理由是厂方自测。同一个场地两种标法，容易被挑。另外 918 那次跑的是 Weissach 包客户车，数值也有 218 和 218.4 两种说法 | 在 notes 写清两次各由谁计时；如果 F5 那次也是 JBPG 设备计时，就统一标法 |
| m9 | minor | #13 Dauer、#23 EB110 SS 的来源 | 两项只有 aggregator 来源。Dauer 有 Auto Bild 原文（autobild.de/artikel/dauer-962-le-mans-42071.html），另有一份 TÜV 报告写的是 402 km/h；EB110 SS 的 355 是常见厂方数字，351 是 1993 年 Nardò 实测，但不确定那台是不是 SS。Dauer 标 VERIFIED，可「谁计的时」说不清 | Dauer 主源换成 Auto Bild 或 evo 2003，notes 写明有 402 / 404.6 两个数；VERIFIED 保留，但描述框加一句「period press measurement」。EB110 补 RM Sotheby's 或 Bonhams 拍卖页作佐证 |
| m10 | minor | #6 Czinger 的数值 | 281 mph 是 Czinger 2021 年给出的生产规格「低阻 V Max 配置」数字；2022 年 V Max 发布时，Autocar 和 Auto Express 引的厂方数字是 253 mph。80 台是全部车型合计，V Max 本身有没有到 10 台不清楚 | notes 写明 253 / 281 两个说法；tag 可改成「Low-drag spec」 |
| m11 | minor | #28（0:04–0:07） | 片头没有 intro_hold，#28 完整可读约 2.3 s（4.2–6.5 s），不到 bible §7-5 要求的 3 s | `layout.intro_hold = 2.5` |
| m12 | minor | publish.md 章节时间码 | 「#28–#11」标签已改对。时间码（以抽帧为准）：#10 卡 2:13 进场、2:16 完整，写的「2:22 Top 10」晚了约 8 s；#1 卡 3:35 进场、3:40 完整、3:47–3:53 停留，写的「3:43 No. 1」晚了约 7 s；计分板 3:53.2 开始淡入，「3:54」可以 | 改成 0:00 / 2:14 / 3:36 / 3:53 |
| m13 | minor | publish.md 署名与描述 | 署名把替代图写成「#1 Yangwang U9 Xtreme: David Merrett」「#10 Rimac Nevera R: Charles」「#13 Dauer 962 Le Mans: Martin Lee」，实际拍的是标准 U9、标准 Nevera、勒芒赛车。描述写「per-item links in the pinned comment」，但逐项数据来源在 Comment 2（回复），不在置顶评论 | 署名加「(pictured: standard U9)」之类的说明，或者换图后重新生成。描述改成「in the pinned comment thread」 |
| m14 | minor | sources.md §5 | 列了 `06_czinger_21c_alt.jpg`（许可 unknown），但 assets.json 里没有这条，这个文件也不存在，属于过时条目 | 重跑 `gen_sources.py` |
| m15 | minor | #10 后洞察卡（Tourbillon） | 2026-08 有报道称已有一台 Tourbillon 交到 Beverly Hills 酒店，2026-10 的报道说还在「准备开始交付」。到发布时这句可能已经过时 | 发布前 7 天复核；如已交付客户，就改洞察卡并把 Tourbillon 445 km/h 收进榜单 |
| m16 | minor | 风险版 #1 | BYD 新闻图（红黑「02」涂装）运动模糊和后期很重，看不出是实拍还是渲染图 | 用户签字前，向 BYD 媒体库核对原图说明；如果是 CGI，按 bible 不收，或者标明是渲染图 |
| m17 | minor | #15 Saleen S7 | Flickr 标题只写「Saleen S7」，从图上无法确认是 2005 款 Twin Turbo | 找标题或说明里写明 Twin Turbo 的图；不换也可接受 |
| — | 记录 | 音频 | 两版音轨都是静音（mean / max −91 dB）。系列目前的设计就是先不配乐，所以不算缺陷，§7-6 这次没检。配乐做好后要重审高潮是否对上前 10 名、片尾淡出 | — |

### 口径意见（观众会在评论区质疑什么）

1. **「#1 不是官方纪录」**：Guinness 和维基认的是双向平均，现在最高的是 Tuatara 455.3 km/h（2021）和 Agera RS 447.19 km/h。本期按单向排，把 U9 Xtreme 496 和 Chiron 490 排在前两名，一定有人反驳。
   - 建议：保留单向口径，因为它和厂方、媒体的说法一致，也是本期的卖点。但片头口径行要写明，置顶评论第一句点名「双向纪录是 Tuatara 455」。
   - 也可以在冠军揭晓后加一张洞察卡：「Fastest two-way average (Guinness rule): SSC Tuatara, 455 km/h」。这比改排名便宜，还能把争议变成知识点。
2. **「宣称值和实测值混排」**：Czinger 452（宣称）排在 Venom GT 435（实测）前面，Regera 410（限速值）排在 Dauer 405（实测）前面。
   - 建议：维持混排，badge 已经标清了。在片头口径行或第一张洞察卡讲明。
   - 如果想更稳，可以改成「实测榜在前、宣称值另列」，但这要大改，不推荐。
3. **「≥10 台」门槛的执行**：几项都卡在边线上——U9 Xtreme（30 台限量，2026-04 才开始交付）、Centodieci（正好 10 台）、Dauer（约 13 台）、Venom GT（约 13 台），Czinger 的 V Max 有几台不清楚。车迷较真时，可能会说 U9 Xtreme「交付不到 10 台」。
   - 建议：口径写成「≥10 units built or on order and deliveries started」，与现在的执行一致。
4. **「为什么没有 X」**：评论区最可能点名的是 CCX（B1，已确认应入榜）、Jesko Absolut（M1）、Pagani Huayra、Aston Martin Valkyrie。
   - Huayra 的厂方数字找不到一手来源：二手资料给 360、370、383 km/h 都有，pagani.com 的 BC 页没有写最高时速。
   - Valkyrie 公路版二手资料多为约 220 mph，没有找到 Aston Martin 的一手数字。
   - 建议：在置顶评论回复里列一行「Not listed: Huayra / Valkyrie — no official top-speed figure; Jesko Absolut — …; Tourbillon / Gemera — not yet delivered」，提前回答。
5. **单向取最高的连带问题**：Agera RS 显示 458 而不是常见的 447，tag 已经写了「2-way avg 447」。这个处理是好的，保留。

### 核对过的数据样本（亲自 WebSearch / WebFetch，2026-11-04）

| # | 项目 | data.json | 核对结果 | 出处（检索所得） | 结论 |
|---|---|---|---|---|---|
| 1 | Yangwang U9 Xtreme | 496.22，VERIFIED，2025 | 2025-09-14 在 ATP Papenburg 跑出 496.22 km/h，单向，限量 30 台；2026-04-24 北京车展首台交付，2026-06 迪拜开始交付 | cnevpost.com 2025-09-22、2026-04-30；globalchinaev.com；中华网 2026-06 | 对，量产门槛勉强过 |
| 2 | Chiron SS 300+ | 490.484，VERIFIED，预产车 | 2019 年 490.48 km/h，仍是上限参照 | Bugatti newsroom（Mistral 稿件回顾）、Motor1 | 对 |
| 3 | SSC Tuatara | 474.76，VERIFIED | 2022-05-14 在 JBPG 单向 295 mph，Racelogic VBOX，有 Racelogic 技术员在场；2021 年双向 282.9 mph | Hagerty、Motor1、Motor Authority、SSC North America | 对；tag 年份见 m6 |
| 4 | Koenigsegg Agera RS | 457.94，VERIFIED | 2017 年 Pahrump，单向最高 457.94，双向平均 447.19，VBOX | Motor1、CarAdvice、Autoblog | 对 |
| 5 | Bugatti W16 Mistral | 453.91，VERIFIED | 2024-11 在 Papenburg，SGS-TÜV Saar 核验，车手 Andy Wallace | Bugatti newsroom（en / de / fr）、Motor1 | 对 |
| 6 | Czinger 21C | 452，CLAIMED | 281 mph 是低阻 V Max 配置的厂方数字；2022 年发布时另有 253 mph 的说法；2023 年底起交付 | evo、Top Gear、Autocar、H.R. Owen | 对，但见 m10 |
| 7 | Hennessey Venom F5 | 437.1，CLAIMED | 271.6 mph 是在 JBPG 的验证跑，不是极速挑战；到 2026 年没有新的极速纪录 | evo、Motor Authority、Hennessey | 对 |
| 8 | Hennessey Venom GT | 435.31，VERIFIED | 2014-02-14 在 KSC 跑出 270.49 mph，Racelogic 工程师确认 VBOX 3i 数据 | New Atlas、CarAdvice、Hennessey | 对 |
| 9 | Veyron Super Sport | 434.211，VERIFIED | 两个方向分别 427.933 和 434.211，平均 431.072，Guinness 与 TÜV 见证 | Bugatti newsroom、Top Gear、Autocar | 对 |
| 10 | Rimac Nevera R | 431.45，VERIFIED | 2025-07 在 ATP Papenburg，Dewesoft 独立核验 | Dewesoft blog、paultan.org | 对 |
| 13 | Dauer 962 LM | 404.6，VERIFIED | 1998-11 在 Ehra-Lessien 测得 404.6；另一份 TÜV 报告写 402；Evo 2003-09 称它为「最快的上路量产车」 | Wikipedia、Auto Bild、slickpix.de | 数值对，来源偏弱（m9） |
| 20 | Corvette ZR1 | 375，CLAIMED | 233 mph 对，但测速地是 ATP Papenburg（不是 Ehra-Lessien），2024-10，双向 233.08 / 233.50 mph | Motor1、TFLcar、Car and Driver | 数值对，notes 地点错（m5） |
| 22 | Pininfarina Battista | 358.03，VERIFIED | 2023-02 在 NATRAX，VBOX 计时，FMSCI 认可 | Autocar India、Automobili Pininfarina 新闻稿 | 对 |
| 23 | EB110 SS | 355，CLAIMED | 355 是常见厂方数字；1993 年 Nardò 测得 351（是否 SS 不明） | racecar.com、RM Sotheby's、classiccars.com | 可接受（m9） |
| 28 | Porsche 918 Spyder | 351.48，VERIFIED | 2015 款 Weissach 包客户车在 JBPG 跑出 218（218.4）mph；Porsche 额定 214 mph（345 km/h） | Jalopnik、CarBuzz、Robb Report | 可接受（m8） |
| 漏项 | Koenigsegg CCX | — | 官网写 400+ km/h；CCX 30 台、CCXR 9 台 | koenigsegg.com/model/ccx、RM Sotheby's | **应入榜（B1）** |
| 漏项 | Jesko Absolut | 不收 | 2024 年 0-400-0 测试中峰值约 412 km/h，Racelogic 核验时间；峰值只见单一来源 | GoAuto、racecar.com | 见 M1 |
| 口径 | Bugatti Tourbillon | 不收（未交付） | 2026-10 报道「准备开始交付」；2026-08 有一台交到酒店 | Carscoops、Supercar Blondie | 暂时成立（m15） |

另外核对了以下各项，均通过：

- **mph 换算**：28 项全部复算，与卡面一致。
- **VERIFIED / CLAIMED 计数**：各 14，与洞察卡一致。
- **纯电车**：3 台（U9 Xtreme、Nevera R、Battista），其中 2 台在 2025 年创纪录，与洞察卡一致。
- **名次**：1–28 连续；两处并列（18 / 18、23 / 23 / 23）按「1,1,3 式」处理正确。排序与 value 一致。
- **国家计分**：美 7、法 6、英 4、瑞典 / 德 / 意各 3、中 / 克罗地亚各 1，合计 28，与成片揭晓页一致。
- **国旗**：全部对应正确。

### 图片逐张结论（默认版 = 上屏的 image 或 image_alt）

- **车型、版本都对**：#2、#4、#5（替代图是绿色 Mistral 客户车）、#7（替代图是银色 F5）、#8、#9、#11、#12、#14、#16、#17、#21、#22、#23 ×3、#26、#27、#28。
- **车型对、版本或构图有问题**：#3（Striker）、#15（无法确认 TT）、#18 Centodieci（只有车尾）、#18 Divo（裁切）、#20（敞篷加 ZTK）。
- **错版本**：#1（标准 U9）、#10（标准 Nevera）、#13（1994 勒芒赛车）。
- **占位卡**：#6。
- **风险版**：7 张全网图车型都对——U9 Xtreme 纪录车、Mistral 纪录车、Goodwood 现场的 21C、KSC 跑道上的 F5、绿色 Nevera R、带牌照的公路版 Dauer、白色 Centodieci。许可全部是 unknown，需用户签字。Dauer 那张 1260×710 偏软，U9 那张后期很重（m16）。
- 没有水印。账本里 AI 生成图 0 张，publish 的合成内容声明选 No，是对的。

### 抽帧清单（`_build/qc/frames/`）

- 全片扫描：`scan/m_001–066.png`，每 4 s 一帧，480 宽，拼成 `_build/qc/scan1.jpg`、`scan2.jpg`。
- 章节定位：`ch/c_128–236.png`，拼成 `_build/qc/ch.jpg`。
- 默认版全分辨率帧（`master/`）：

  | 内容 | 时间 |
  |---|---|
  | 片头 | 2 s |
  | 片头到 #28 | 3.5、4.2、5、6、7 s |
  | 洞察卡（6 张） | 20、58、104、144、180、210 s |
  | Divo / Centodieci | 76、82 s |
  | Dauer | 120 s |
  | #10 | 138 s |
  | Czinger 占位卡 | 172 s |
  | 冠军 | 230 s |
  | 计分板 | 238 s |
  | 来源卡 | 242 s |
  | 片尾 | 250 s |
  | 随机时间点 | 33、47、91、125、155、193、200、222 s |

- 风险版（`risk/`）：76、82、120、138、172、177、200、222、230 s。
- 拼图：`_build/qc/t0–t8.jpg`。素材候选拼图：`_build/qc/sheet_a/b/c.jpg`（34 张，含 image_alt）。

### 规格核对（ffprobe）

| 文件 | 分辨率 | 帧率 | 帧数 | 时长 | sha256 与 manifest |
|---|---|---|---|---|---|
| master.mp4 | 1920×1080 | 60/1 | 15,733 | 262.217 s | 一致（4e8840…） |
| _with-risk-images.mp4 | 1920×1080 | 60/1 | 15,733 | 262.217 s | 一致（cf330b…） |

时间线：片头 0–5 s → 滚动 5–227.2 s → 冠军 227.2–233.2 s → 计分板 233.2–240.2 s → 来源卡 240.2–244.2 s → 片尾 244.2–262.2 s（18 s，画面干净）。

### 修完后复审要看

1. B1 / M1 改完后，重新生成 data、sources、publish，两版重渲；核对名次、计分板、洞察卡计数和标题 Top N。
2. 默认版 #1 / #10 / #13 / #6 换成对版本的可商用图，或者用户签字发风险版；如果仍用替代图，署名必须写明 pictured 的是什么。
3. 改章节时间码，并设 intro_hold。
