# ep17 世界最长河流 Top 50 · 审片记录（qc.md）

## 复核 · 2026-11-04

> 独立复核人（另起上下文，未参与制作，也没写第 1 轮审片）。只写本文件与 `_build/qc/recheck/`，未改数据、图片、渲染。
> 被复核对象：默认版 `render/ep17_longest_rivers_master.mp4`（sha256 cd81bb25…，与 manifest 的 output_sha256 一致）。manifest 输入 data.json b22e04ef… / assets.json f48cf84f… 与当前文件一致，52 张上屏图 sha256 全部对得上（0 不符）。
> 风险版 `_with-risk-images` 本轮未重渲，manifest 输入仍是 QC 前 data.json ae2a9ae3…（漏 Araguaia、Zambezi 3,540、Orinoco 在榜），只确认结论，未逐帧审。

### 最终结论：**可发布（默认版）**

第 1 轮的 1 个 blocker、5 个 major 都已修好，并在成片里亲眼核到；没有引入名次、洞察卡或出框类的新问题。剩下的都是 minor（见下），不挡发布。如果顺手修 n1 / n2，需要重渲一次。

**推荐发布默认版**。理由：① 风险版的数据是 QC 前的旧版本，名次从 #32 起就和描述框、置顶评论对不上，还保留了 Zambezi 3,540 的离群值，Orinoco 也还在榜上；② 风险版里有 5 张图的来源页明写「保留全部权利」，屏上署名直接显示「unknown」「All rights reserved」（第 1 轮 M6）。默认版这 12 处已经换成可商用实拍或 AI 图，publish.md 也是按默认版生成的。

### 技术核对（默认版）

| 项 | 结果 |
|---|---|
| 分辨率 / 帧率 / 编码 | 1920×1080，60/1（r = avg），H.264，yuv420p；音轨 AAC 静音（anullsrc，同第 1 轮 m9） |
| 时长 / 帧数 | 容器 = 视频流 382.600 s；`-count_packets` 22,956 帧 = 382.6 × 60，与 render_master.log「22956 frames」一致 |
| 时间线 | `python -m rank_scroll timeline`：intro 0–5、scroll 5–347.6（含 intro_hold 2.5 s）、champion –353.6、tally –360.6、sources –364.6、end –382.6，总 22,956 帧，与 manifest 完全一致 |
| validate | `validate --strict`（不带 risk）：OK，50 条、6 张洞察卡 |
| 数据机检 | 50 条按 value 降序；名次按「严格更长的条数 + 1」重算全部吻合（并列 #46 后接 #48）；`value_display` 与 `secondary_display`（km ÷ 1.609344 取整）全部一致；大洲 Asia 20 · South America 12 · North America 7 · Africa 6 · Europe 4 · Oceania 1 = 50，与片尾计分板帧一致 |
| 章节 | publish.md 的章节时间与当前时间线对得上（1:10 = #40 Ural 居中 70.8 s，2:18 = #30 Tocantins 138.8 s，3:26 = #20 Indus 206.8 s，4:39 = #10 Amur 279.7 s，5:43 = 冠军段前 4 s，5:54 = 计分板） |

### 第 1 轮问题逐条

| 编号 | 问题 | 结论 | 核到的证据 |
|---|---|---|---|
| B1 | 漏收 Araguaia | **已修** | data.json #32 Araguaia 2,627 km / 1,632 mi，Ends in Brazil，「Joins the Tocantins · Tocantins tributary」，出处为 Britannica 原句；成片 126.17 s 帧显示正确（巴西旗，署名「Augusto Miranda / MTur / Public domain」）。Orinoco 按 M1a 规则改为 2,140 后落到 #51 出榜，所以 Kasai 留在 #50，与第 1 轮的推演一致 |
| M1 | Zambezi 3,540 离群值 | **已修** | 改为 2,574 km（#34，排在 Nelson 2,575 之后），1,599 mi；离群值规则同时写进 scope_note、描述框和 sources.md §1；sources.md 记了「Britannica 3,540」；113.5 s 帧显示正确。描述框没写出 3,540 这个数，只说「25%+ off」，可以接受 |
| M2 | 其余差 > 10% 的条目 | **已修** | 按同一规则，Orinoco 一并换值；描述框加了「Where other surveys differ a lot (Salween, Brahmaputra, Mekong…), we list Britannica's figure.」；置顶评论说明里写了 Zambezi / Orinoco 的回复要点 |
| M3 | 屏上没说明国旗规则 | **已修** | 片头副标题、页眉和来源卡都写着「Flag = where the river ends」，页脚右侧也常驻；所有卡的国家行改成「ENDS IN …」（抽帧看到 ENDS IN ROMANIA / BANGLADESH / MEXICO / PAKISTAN / UNITED STATES 等），描述框署名行同步 |
| M4 | Indus 用的是拉达克照片 | **已修** | 换成 Unsplash Danish Rasool 拍的苏库尔 Lansdowne / Ayub 双桥（巴基斯坦信德省），206.83 s 帧可见红色拱桥，Ends in Pakistan，署名一致 |
| M5 | 第 50 名可读时间不够 | **已修** | `layout.intro_hold = 2.5`；抽帧 4.6 / 6.0 / 7.4 s，Kasai 完整停在左侧，约 7.8 s 才开始出框，完整可读约 3.2 s；Kasai 卡有黄色 AI IMAGE 角标 |
| M6 | 风险版不建议发布 | **维持**（不需要修） | 见上方推荐理由；publish.md「版本与图片」也写明不发布风险版 |
| m1 | Songhua / Pearl / Red River 等未收 | **已修** | sources.md 写了 Songhua 1,925；Pearl 按「缺水系合计例外只适用于 Murray–Darling 这类」不收，规则写进 §1；Red River 写明无 Britannica 长度 |
| m2 | 英里数比原文更精确 | **未修** | 仍是从 km 反算（如 Amazon 3,977 mi、Indus 1,988 mi）。minor，可以保留 |
| m3 | 构图偏天空 | **部分修** | Irrawaddy 焦点改成 y = 0.8、Tocantins 改成 0.75，但画面仍以粉色天空 / 日落为主，河很少（见 n2） |
| m4 | 低分辨率图 | **部分修** | Lena 2048×1152、Pilcomayo 替代图 2048×1536 已升级；Juruá 替代图 1024×613、Aldan 替代图 1023×644 仍是低分辨率 |
| m5 | Olenyok 的 AI 图像勒拿石柱 | **未修**（可接受） | 仍是石灰岩石柱倒影的构图，但已有 AI IMAGE 角标和「AI-generated image, not a photo」字样 |
| m6 | Amazon 主图不够「一眼亚马孙」 | **未修** | 仍是窄侧汊航拍。minor |
| m7 | 用同水系的图 | 可接受，不变 | — |
| m8 | 封面直接亮出冠军 | **未修** | thumbnail 没改。可接受 |
| m9 | 没有配乐 | **未修**（系列已知事项） | 音轨仍是静音 |

### 新问题（都是 minor）

- **n1 来源行漏了 Zambezi 的数据来源**：片头、页脚、来源卡和描述框的「Sources:」都只写「Encyclopaedia Britannica, Geoscience Australia」，但 #34 Zambezi 的 2,574 km 实际取自 Wikipedia / Wikidata（scope_note 和置顶评论里有说明）。建议 `source_line` 补上「…, Wikidata」或「others where noted」。改了要重渲。
- **n2 #49 Irrawaddy 变成开场画面**：名次顺移后，Irrawaddy 在片头 2.5 s 停顿里全程占着第二张卡的位置，满卡粉色天空，河只有底部一条细带（`_build/qc/recheck/tiles/t13_irrawaddy.jpg`）。这是观众最先看到的画面之一，建议换一张河面清楚的伊洛瓦底江实拍（比如蒲甘段、曼德勒段）。改了要重渲。
- **n3 publish.md 上传清单措辞过时**：清单写「卡上标 Illustration / Render」，成片实际是「AI IMAGE」角标。只改文字，不影响成片。
- 已核未发现问题的项：名次连续（只有并列 #46 跳过 #47）；6 张洞察卡的 after_rank 都紧接对应河流（44→Colorado #43，38→Ganges #37，28→Danube #27，20→Purus / Juruá / Madeira 三条都长于 Danube 2,850，13→Mekong #12，2→Nile）；没有文字出框，最长的「Mackenzie–Peace–Finlay」「Nelson–Saskatchewan」「Japurá–Caquetá」「ENDS IN UNITED STATES」都在卡内；8 张 AI 图卡（Kasai、Olenyok、Ubangi、Vilyuy、Japurá、Lower Tunguska、Purus、Madeira）都抽帧看到黄色 AI IMAGE 角标。

### 抽帧清单（`_build/qc/recheck/frames/`，拼图在 `tiles/`）

- 片头 0.5 / 2.0 / 3.5 / 4.6 s；停顿段 6.0 / 7.4 / 7.8 / 8.0 s。
- 49 张卡（#49 至 #1）和 6 张洞察卡各在居中时刻抽 1 帧，时刻用 `recheck/centers.py` 按当前 rank_scroll 时间线算出（`centers.json`）；#50 Kasai 在片头和停顿段的帧里已经看到。
- 冠军 349.0 / 353.4 s；计分板 355.0 / 360.3 s；来源卡 362.6 s；片尾 366.0 / 382.5 s。
- 5 个随机点（seed 20261104）：83.81 / 90.97 / 144.80 / 227.93 / 284.24 s。144.80 s 在拼图里看着像两张卡叠在一起，原因是拼图把相邻两格贴在了一起，单帧全图核过（`tiles/t12_1448_compare.jpg`，快速 seek 和精确 seek 逐像素一致），画面正常。

---

## 第 1 轮独立审片 · 2026-11-04

> 独立审片人（另起上下文，未参与制作）。按 `qc_brief`、bible §2/§3/§4/§7、`data_contract.md` 审。只写本文件与 `_build/qc/`，未改数据、图片、渲染。
> 已知不计：渲染器新加的 AI 图「AI IMAGE」角标与「AI-generated image, not a photo」署名、章节分组修复，现有成片还没有，不记为问题。
> 被审对象：`render/ep17_longest_rivers_master.mp4`（sha256 b715ed2d…）与 `render/ep17_longest_rivers_master_with-risk-images.mp4`（sha256 e4d6abe9…），输入 data.json ae2a9ae3… / assets.json 80f14851…（与 manifest 一致，图片 sha 全部对得上）。

### 结论：**必须修**（修后重渲即可发布默认版；风险版不建议发布）

数据层有 1 个 blocker（漏收 Araguaia，导致 #34 起名次全错、第 50 名应出榜），另有 Zambezi 数值问题和「国旗按河口」在屏上没有任何说明（约 17 张卡照片所在国 ≠ 国旗）。渲染本身完整：两版都是 22,806 帧 = 380.1 s × 60，与 manifest 时间线一致，全片解码无错误，滚动段无冻结、无黑帧，没有被误杀截断的迹象。

| 审查项 | 结论 |
|---|---|
| 1 数据 | **必须修**（B1、M1、M2；其余为注明类） |
| 2 图片 | **小修**（默认版 42 实拍认对河流、无水印；M4 印度河照片配巴基斯坦旗；若干构图偏天空） |
| 3 成片 | **小修**（帧数完整；M3 屏上无国旗口径；M5 第 50 名可读时间不足） |
| 4 包装 | **通过**（标题 58 字符；描述含口径、来源、AI 图声明、逐图署名）；Araguaia 修后需重跑 `publish` |
| 5 观众视角 | 有亮点（Nile vs Amazon 压轴、亚马孙支流比多瑙河长），但 #50–#25 段西伯利亚 / 亚马孙小支流密集、几张偏天空的图，是最可能划走处 |

---

### 问题清单

#### Blocker

**B1 · 漏收 Araguaia（Britannica 2,627 km），#34 起名次全错，Kasai 应出榜**
- 位置：#34–#50（全片 1:51 以前的倒数段）、计分板、洞察卡 after_rank。
- 证据：Britannica「Araguaia River」：rises near Alto Araguaia, Mato Grosso, flows north-northeast **for 1,632 miles (2,627 km)** to its junction with the Tocantins at São João do Araguaia（Britannica print article 31943，经 WebSearch 核到原句；Wikipedia infobox 同值）。本期口径明写「不在水系主线上的大支流照列」（Vilyuy、Aldan、Paraguay 等都列了），Araguaia 是 Tocantins 的支流、不在 Britannica 的 Tocantins 2,699 km 主线上，按规则必须入榜。制作方 `_build/raw/brit/` 抓了 100 多条 Britannica 条目，唯独没有 Araguaia；`sources.md` §4 也只把它当作「Tocantins–Araguaia 3,650 维基水系值」排除，没有查 Araguaia 自身长度。
- 修法：`items_def.py` 加 Araguaia（2,627 km，1,632 mi；河口 = 汇入 Tocantins 处，在 Brazil；South America；tag「Joins the Tocantins」「Tocantins tributary」），排在 Vilyuy 2,650（#33）与 Nelson 2,575 之间成 #34；Nelson 起顺移，Rio Negro / Ubangi 并列 #47，Dnieper #49，Irrawaddy #50，**Kasai 出榜**（#51）。洞察卡 after_rank 跟着改：「Next: the Colorado」改 after 45，「Next: the Ganges」改 after 39。计分板变成 South America 13、Africa 5。再跑 build → gen_sources → validate → render → publish。（若同时采纳 M1，见下方名次推演。）
- 顺带核了其余可能漏收的（Britannica 值）：Kolyma 2,129（低于线，正确）、Songhua 1,925（低于线）、Orange 约 2,090、Xingu 约 2,100、Tarim 约 2,030、Columbia 2,000、Brazos 2,060——都在线下，**没有发现别的漏项**。

#### Major

**M1 · Zambezi 3,540 km 是 Britannica 的离群值，不是口径差，建议换值**
- 位置：#16（3:54 前后），计分板不受影响（Africa）。
- 证据：Britannica 原文确实是「flows eastward for about 2,200 miles (3,540 kilometres) from its source on the Central African Plateau」（WebSearch 与本地快照 `_build/raw/brit/Zambezi-River.html` 都核到）。但同一条目的 Physiography 写的源头是「a marshy bog near Kalene Hill, Zambia」——和常见 2,574 km（Wikipedia 正文 / Wikidata / 多数赞比西流域资料）是**同一个源头、同一个河口**，没有更长的支流源或不同河口可以解释 38% 的差距。与 Mississippi–Missouri、Ob–Irtysh 那种「含支流源」的口径差不同，这一条是 Britannica 自身数值偏大。放在 #16，还排在 Volga（欧洲第一长河 3,530）之上，是评论区最容易抓的错。
- 修法（二选一，推荐 a）：
  a. 定一条写进 `sources.md` §1 与 scope_note 的例外规则：「Britannica 值与同源头、同河口的其他权威数值相差 > 25%、且无口径解释时，改用后者并注明」——Zambezi 改 2,574 km，落到 #35（Nelson 2,575 之后、Paraguay 2,550 之前）；屏上 notes / 描述框写「Britannica gives 3,540 km」。
  b. 保留 3,540，但卡片加徽章 `BRITANNICA FIGURE`、tag「Others: 2,574 km」，并在描述框单列一句。只写 notes 不上屏不够。
- 若同时做 B1 + M1a：Volga 升 #16 … Japurá #28、Euphrates #29、Orinoco #30、Tocantins #31、Vilyuy #32、Araguaia #33、Nelson #34、Zambezi #35、Paraguay #36 … Irrawaddy #50，Kasai 出榜；洞察卡「The next 3 rivers are only tributaries of the Amazon」改 after 20、「Next: the Danube」改 after 28。

**M2 · 其余 10 条「差 >10%」的定性与修法**（制作方自报 11 条，逐条核了 Britannica 原文；除 Zambezi 外都不必换值）

| # | 河 | Britannica 原文（已核） | 对照值 | 差异原因 | 建议 |
|---|---|---|---|---|---|
| 10 | Amur–Argun | 世界长河表「Amur–Argun 4,444 km / 2,761 mi」（WebSearch 核到） | Liu 2009 5,498 | **口径**：Liu 量到蒙古境内另一源头（克鲁伦河经呼伦湖） | 保留；notes 已写，够 |
| 12 | Mekong | 「about 2,700 miles (4,350 km)」（本地快照 + 表） | Liu 2009 4,909 | **测法**：卫星+实地 vs 地图量算 | 保留；已有洞察卡讲这件事，好 |
| 19 | Juruá | 「calculated to exceed 2,040 miles (3,283 km)」（WebSearch 核到） | 维基列表 2,410 | **测法**：最曲折的河，弯道量法差异大；维基正文本身也用 3,283 | 保留；可在描述框提一句 |
| 27 | Brahmaputra | 「some 1,800 miles (2,900 km) from its source … to its confluence with the Ganges」（WebSearch 核到） | 维基 3,969 | **口径**：Britannica 量到与恒河汇合，维基续算 Padma–Meghna 到海 | 保留；tag「Joins the Ganges」已对应 |
| 30 | Euphrates | 「1,740 miles (2,800 km)」（本地快照） | 维基 3,596 | **口径**：维基算 Murat 源 + Shatt al-Arab | 保留 |
| 31 | Orinoco | 「some 1,700 miles (2,740 km) from its source in the Guiana Highlands」（WebSearch 核到） | 维基 2,101–2,140 | **无口径解释**：Britannica 写的源头就是圭亚那高原（与 2,140 同源）；Guaviare 水系（约 3,010）Britannica 没有采用 | 次于 Zambezi 的离群值。若采纳 M1a 规则（差 >25% 才换），Orinoco 差 28%，应一并换成约 2,140 → 正好落到 #51 出榜（Kasai 留在 #50）；若不想动，至少同 M1b 上屏注明。由人定，二者必须同一标准 |
| 32 | Tocantins | 「its 1,677-mile (2,699-kilometre) course」（本地快照） | 维基 3,650 | **口径**：维基算 Tocantins–Araguaia 水系 | 保留；但正因此必须单列 Araguaia（B1） |
| 41 | Salween | 「flows generally south for about 1,500 miles (2,400 km)」（WebSearch 核到） | 维基 3,060 / Wikidata 2,815 | 测法 / 源头不一（中方怒江段约 2,000 km，全长常见 2,800–3,200） | 保留并在描述框列为偏低值；评论区可能挑 |
| 43 | Colorado | 「1,450 miles (2,330 kilometres)」（本地快照） | 维基 2,945 | **口径**：维基算 Green River 源 | 保留 |
| 49 | Irrawaddy | 「about 1,350 miles (2,170 km)」（本地快照） | 维基 2,809 | **口径**：维基算 N'Mai–独龙江源 | 保留 |

- 统一建议：描述框 scope_note 后加一句「Where other surveys differ a lot (Zambezi, Orinoco, Salween, Brahmaputra…), we list Britannica's figure; see pinned comment」，Comment 2 对这几条附对照值。

**M3 · 「国旗 = 河口所在国」屏上没有任何说明，约 17 张卡照片所在国与国旗不同**
- 位置：片头（0:00–0:05）只有「Length · Data as of Nov 2026」和来源行；来源卡（6:00）也没有。口径只在描述框。
- 证据（照片拍摄地 → 卡上国旗）：Indus 拉达克（印控）→ 巴基斯坦；Yukon 道森市（加拿大）→ 美国；Danube 布达佩斯 → 罗马尼亚；Zambezi 维多利亚瀑布（赞比亚/津巴布韦）→ 莫桑比克；Colorado 马蹄湾（亚利桑那）→ 墨西哥；Ganges 恒河晨舟（印度）→ 孟加拉；Brahmaputra（印度/西藏）→ 孟加拉；Salween 云南怒江 → 缅甸；Mekong 琅勃拉邦（老挝）→ 越南；Ishim 阿斯塔纳（哈萨克斯坦）→ 俄罗斯；Syr Darya 托克托古尔（吉尔吉斯）→ 哈萨克斯坦；Amu Darya 喷赤河（塔吉克）→ 乌兹别克；Euphrates 哈尔费蒂（土耳其）→ 伊拉克；Ob–Irtysh 新疆五彩滩 → 俄罗斯；Niger 巴马科（马里）→ 尼日利亚；Pilcomayo 苏克雷桥（玻利维亚）→ 巴拉圭；Ubangi（AI，班吉/中非）→ 刚果（金）。卡上国家名用强调色大写写在河名正上方，观众自然读成「这是 X 国的河」。亚马孙挂巴西、尼罗河挂埃及没问题；问题集中在多国河流。
- 修法：① 片头统计行改为「Length · Flag = country where the river ends · Data as of Nov 2026」（`period_label` 或渲染器副标题），来源卡加同一句；② 卡上国家行改为「ENDS IN ROMANIA」这类写法（渲染器加 `country_prefix` 或 data 里 `country_name` 改写；注意描述框署名行会跟着变，需同步 publish 模板）；③ 不必换国旗规则——改成「流域最大国」或多国旗同样有争议，河口规则可核实、一致，只要讲清楚。

**M4 · Indus 卡：拉达克（印控克什米尔）照片 + 巴基斯坦国旗，政治敏感**
- 位置：#21（3:18）。
- 证据：图源 Pexels「confluence of Zanskar and Indus rivers in Leh Ladakh India」；卡上巴基斯坦国旗 + 「PAKISTAN」。印度观众会读成「把拉达克标成巴基斯坦」，是全片最可能引战的一张。
- 修法：换一张巴基斯坦本土（非争议区）印度河实拍，如 Tarbela / Attock / Sukkur 堰 / 海得拉巴段（避免斯卡都、吉尔吉特等巴控争议区）；找不到可商用图就用 M3 的「ENDS IN PAKISTAN」并在署名行写「Photo: Ladakh」。

**M5 · 第 50 名 Kasai（修后为 Irrawaddy）停留不足 3 秒**
- 位置：0:03.5–0:05.4。
- 证据：`data.json` 没设 `layout.intro_hold`；第一张卡 0:04.6 才滑到位，0:05.0 起即匀速左移，0:05.33 左边缘出框——完整可读约 1 s，不满足 bible §7-5「3 秒内看得清」。`data_contract` 已建议 2.5。
- 修法：`layout.intro_hold: 2.5`，随本轮重渲一起出。

**M6 · 风险版（_with-risk-images）不建议发布**
- 12 张中 5 张来源页明写保留全部权利（Amur dronestagram「All rights reserved」、Madeira 波多韦柳市府「Todos os direitos reservados」、Paraguay 科伦巴市府、Pilcomayo「Todos los derechos reservados」、Ural「Все права защищены」），不是「许可不明」而是明确不许；屏上署名行直接显示「unknown / unknown」「All rights reserved」等字样（R 帧 0:05.6、0:38、2:22 等），Olenyok、Vilyuy 原图带摄影师签名水印。默认版的替代图质量已够，默认版即可发布。
- 修法：用户签字前不发布风险版；如坚持用其中某张，先联系作者取得书面许可，署名改为真实作者。

#### Minor

- **m1 Songhua / Pearl / Red River 未收**：
  - Songhua 未收**合理**：Britannica Sungari 条目给 1,925 km（约 1,195 mi），低于第 50 名；sources.md §4「no Britannica figure retrieved」应改为这个值。
  - Red River (US) 未收**可接受**：Britannica 条目确实不给长度（本地快照与网页都没有），维基 2,190 km；且下游已改道 Atchafalaya，是否算 Mississippi 支流本身有争议。描述框可列为「not ranked: no Britannica length」。
  - Pearl（珠江–西江）未收**与 Murray–Darling 的例外不一致**：Britannica 无总长，而 Murray–Darling 因 Britannica 无水系值就改用国家机构（Geoscience Australia）。同理可用中国水利部珠江水利委员会数值（西江约 2,214 km，系统约 2,320 km；本轮未取到官方原文）→ 约 #46–48。二选一：要么把例外规则写死为「仅用于 Britannica 已有分段值、只缺水系合计的河」（Murray–Darling 符合，Pearl 不符合 → 不收，并写进 scope_note），要么按国家机构数收 Pearl。推荐前者，改动最小。
  - St. Lawrence–Great Lakes（维基 3,058，约 #23）同理：Britannica 无系统长度（只给航道 3,766 km 与河段），不收合理，但北美观众会问，建议写进 Comment 2 的「为什么没有」。
- **m2 英里换算的伪精度**：Britannica 很多条是英里为主、整百取整（Amazon「at least 4,000 miles」、Indus「some 2,000 miles」、Niger「2,600 miles」），卡上由 km 反算成 3,977 / 1,988 / 2,610 mi，比原文更「精确」。建议 `secondary_display` 直接用 Britannica 原文英里数。
- **m3 构图偏天空、河几乎看不见**：#49 Irrawaddy（满卡粉色天空，河与船被数值块盖住）、#32 Tocantins（日落天空 + 桥）、#35 Paraguay 替代图、#40 Ural 替代图（楼与天空）、#9 Congo（主体是破船）。建议 `image_focus` 往下调（y≈0.7–0.8）或换图；Irrawaddy 最明显。
- **m4 低分辨率**：Lena 1024×576、Juruá 替代图 1024×613、Pilcomayo 替代图 1024×768、Aldan 替代图 1023×644 在 720×800 卡上放大约 1.4–1.6×（超采样下更高），满屏看略软；Flickr 限流恢复后重下原图（handoff 已记）。
- **m5 #44 Olenyok 的 AI 图**：橙色石灰岩石柱倒影，与勒拿河上最著名的「勒拿石柱」（Lena Pillars）几乎一样，懂行的观众会以为放错河。新渲染器会加 AI IMAGE 角标，可接受；更稳妥是 prompt 改成奥列尼奥克河常见的低岸冻土苔原景观。其余 7 张 AI 图（Madeira、Purus、Lower Tunguska、Japurá/Araracuara 峡谷、Vilyuy、Ubangi、Kasai）景观与真实河段特征相符，未发现误导性地标。
- **m6 #2 Amazon 主图**：Pexels 标注秘鲁境内亚马孙，但画面主体是一条窄侧汊（宽干流只在远景），作为第 2 名不够「一眼亚马孙」。可换马瑙斯「Meeting of Waters」或宽干流航拍。
- **m7 #13 Mackenzie 用的是 Peace River（Alberta）、#7 Ob–Irtysh 用的是额尔齐斯河新疆段、#34 Nelson 图源只写「Saskatchewan River」**：同水系，可接受；handoff 已列为可再升级。
- **m8 封面**直接亮出 #1 Nile，与 Vision「看到最后才知道冠军」略冲突；标题本身已有「Nile vs Amazon」，可接受，也可改为 #2–#4 或加问号。
- **m9 无配乐**：两版音轨均为静音（anullsrc，manifest 可见）；`assets/music/` 下有 2 个 mp3 但未混入。按系列现状属已知事项，配乐版出来后需再查响度与片尾淡出。

### 已核对的数据样本（≥10 条，含前 5 名与冠军）

本轮 britannica.com 与 web.archive.org 均无法直连（工具拦截），以 WebSearch 取 Britannica 页面原句；WebSearch 未返回原句的，用制作方存档快照 `_build/raw/brit/` 交叉确认并标注。

| # | 河 | 屏上值 | 核到的出处原句 | 核对方式 | 结论 |
|---|---|---|---|---|---|
| 1 | Nile（冠军） | 6,650 km | Britannica：about 4,132 mi (6,650 km)，量自汇入维多利亚湖的最远源头 | WebSearch | 一致 |
| 2 | Amazon | 6,400 km | Britannica：6,400 km（at least 4,000 mi）；INPE 2008 6,992 km 另有报道 | WebSearch + 快照 | 一致；英里见 m2 |
| 3 | Yangtze | 6,300 km | 「3,915 miles (6,300 km)」 | 本地快照（WebSearch 未返回原句） | 一致 |
| 4 | Mississippi–Missouri | 5,971 km | Britannica：combined length 3,710 mi，世界第 4 | WebSearch | 一致 |
| 5 | Yenisey–Angara–Selenga | 5,539 km | 「with the Selenga … 3,442 miles (5,539 km)」 | WebSearch | 一致 |
| 10 | Amur–Argun | 4,444 km | Britannica 世界长河表 4,444 km / 2,761 mi | WebSearch | 一致 |
| 12 | Mekong | 4,350 km | 表与条目 4,350 km；Liu 2009 Table 4,909 km（洞察卡） | WebSearch + `liu2009.txt` | 一致；洞察卡有据 |
| 16 | Zambezi | 3,540 km | 「about 2,200 miles (3,540 kilometres)」；源头 Kalene Hill | WebSearch + 快照 | 与原文一致，但为离群值（M1） |
| 19 | Juruá | 3,283 km | 「calculated to exceed 2,040 miles (3,283 km)」 | WebSearch | 一致 |
| 27 | Brahmaputra | 2,900 km | 「some 1,800 miles (2,900 km) … to its confluence with the Ganges」 | WebSearch | 一致（口径差） |
| 31 | Orinoco | 2,740 km | 「some 1,700 miles (2,740 km) from its source in the Guiana Highlands」 | WebSearch + 快照 | 与原文一致，离群（M2） |
| 41 | Salween | 2,400 km | 「about 1,500 miles (2,400 km)」 | WebSearch | 一致 |
| — | Araguaia（漏收） | — | 「1,632 miles (2,627 km)」 | WebSearch | **应入榜 #34（B1）** |
| — | Songhua（未收） | — | Britannica Sungari ≈1,925 km | WebSearch | 未收正确 |
| — | Kolyma（#51 候选） | — | 「1,323 miles (2,129 km)」 | 本地快照 | 未收正确 |
| — | St. Lawrence | — | Britannica 无系统长度（只有航道 3,766 km） | WebSearch + 快照 | 未收合理 |
| — | Red River (US) | — | Britannica 条目无长度 | WebSearch + 快照 | 未收可接受 |

其他机检：50 条名次连续（并列 #46 后接 #48）、按 value 降序、`value_display` / 英里换算与 value 一致；大洲计分 20/12/7/6/4/1 = 50，与片尾计分板一致；6 张洞察卡的「Next: …」都紧接对应河流（0:43.8→Colorado、1:26.5→Ganges、2:28.2→Danube、3:23.5→Purus/Juruá/Madeira、4:18.8 Mekong、5:37.4 Amazon/Nile），文案在 sources.md §5 均有出处（INPE 6,992、Liu 4,909、Britannica「10 countries」、Colorado 少入海）。

### 成片技术核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 分辨率 / 帧率 / 编码 | 1920×1080，60/1，H.264 High，yuv420p | 同 |
| 时长 | 380.100 s（视频流 = 容器） | 同 |
| 帧数（-count_packets） | 22,806 = 380.1×60，与 manifest / render log「22806 frames」一致 | 22,806，一致 |
| 时间线（manifest） | intro 0–5、scroll 5–345.1、champion 345.1–351.1、tally –358.1、sources –362.1、end –380.1；用当前 rank_scroll 重算 timeline 结果相同 | 同 |
| 全片解码 | 无错误（`_build/qc/decode_*.log` 为空） | 同 |
| freezedetect / blackdetect | 仅片头标题（0.7–3.0 s）、计分板、来源卡、片尾静止；滚动段与冠军段无冻结；无黑场（`_build/qc/detect_*.txt`） | 同 |
| 输入一致性 | manifest 里 data.json、assets.json、52 张图 sha256 与当前文件全部一致 | 同 |
| 音轨 | AAC 静音（anullsrc） | 同 |

结论：误杀进程**没有**波及本期两版成片，帧数完整、未截断。

### 抽帧清单（`_build/qc/frames/`，拼图在 `_build/qc/tiles/`）

- 默认版（M_*，75 帧）：片头 1.0 / 3.5 / 4.6 / 5.5 s；50 张卡各在居中时刻 1 帧（5.6 s Kasai … 345.1 s Nile，时刻由 `centers.json` 按 rank_scroll 时间线计算）；6 张洞察卡（43.83 / 86.50 / 148.17 / 203.50 / 258.83 / 337.37 s）；冠军 348.0 / 350.9；计分板 353.0 / 357.5；来源卡 360.0；片尾 365.0 / 379.9；随机 20.9 / 71.3 / 140.4 / 196.1 / 262.7 / 300.0 / 333.3 / 343.0 s。
- 风险版（R_*，17 帧）：12 张风险图卡各 1 帧（Kasai 5.6、Aldan 32.0、Olenyok 38.33、Ural 68.33、Pilcomayo 81.0、Paraguay 104.67、Vilyuy 117.33、Japurá 142.67、Juruá 215.33、Madeira 221.67、Murray–Darling 240.67、Amur 277.23），片头、冠军、计分板、来源卡、片尾各 1 帧。
- 素材拼图：`_build/qc/sheet_1..3.jpg`（全部 62 张上屏图含 image_alt，标注分辨率）。
- 看帧结论：无文字出框 / 截断 / 省略号（最长名「Mackenzie–Peace–Finlay」「Yenisey–Angara–Selenga」都在卡内）；国旗与 data.json 一致；无占位卡；冠军段 No. 1 面板、光晕、计分板与结尾揭晓正确；问题见 M3、M4、M5、m3。

### 观众视角（全球英文观众）

- 好看的：标题「Nile vs Amazon」+ 冠军前一张洞察卡「Is the Nile really No. 1?」压轴到位；「3 条亚马孙支流都比多瑙河长」反常识、好转发；Hukou 瀑布、马蹄湾、维多利亚瀑布、布达佩斯等图很抓眼。
- 会划走的：#50–#25 连续出现 Kasai / Aldan / Olenyok / Ishim / Vilyuy 等陌生名字，配几张偏天空或 AI 的图，节奏偏平；建议给这一段加一张「Siberia has 9 rivers in this list」类洞察卡（需按修后名单重数并核出处）。
- 评论区预期：① Zambezi 太长（M1）；② 「Indus 为什么挂巴基斯坦、照片却是拉达克」（M4）；③ 「Danube / Ganges / Colorado 国旗不对」（M3）；④ St. Lawrence、Brahmaputra 3,848 等「你漏了 / 你量短了」。M1、M3、M4 修掉后，剩下的都能用描述框口径回应。
