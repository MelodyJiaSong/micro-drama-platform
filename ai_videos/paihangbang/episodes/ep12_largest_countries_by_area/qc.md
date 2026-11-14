# ep12 · 审片记录（qc.md）

## 复核 · 2026-11-04（返修后，独立上下文）

> 复核人没有参与制作，也没有写第 1 轮审片。只写本文件和 `_build/qc/recheck/`，没有改数据、图片或渲染。
> 复核对象：`render/ep12_largest_countries_by_area_master.mp4`，sha256 1cba37c7…，04:12 渲完。风险版本轮没有重渲，只确认结论。

### 最终结论：**可发布（默认版）**，风险版不发布

- **推荐发布默认版。** 第 1 轮唯一的 major（#1 Tanzania 图）已经修好，其余影响观众的 minor（#3–#8）也都改了。剩下的 2 条只涉及来源卡和内部文档，不影响上屏数据。
- **风险版不推荐。** 它仍然过时：manifest 里 data.json、assets.json、`30_tanzania.jpg` 三个哈希与当前文件不一致，片中还是肯尼亚 Amboseli 的图，本轮的改动它一条都没有。另外它含非商用（NC）图和「版权保留」图。
- 下面「未修」各条都不阻塞发布，可以留到下次顺手改。

### 技术核对（默认版）

| 项 | 结果 |
|---|---|
| 分辨率 / 帧率 | 1920×1080，r = avg = 60/1 ✓ |
| 时长 / 帧数 | 382.600 s；容器 nb_frames 22,956，`-count_frames` 实际解码 22,956（`recheck/countframes.txt`）= 382.6 × 60 ✓ |
| 与 `python -m rank_scroll timeline` 对照 | 两者一致：intro 0–5 / scroll 5–347.6 / champion 347.6–353.6 / tally 353.6–360.6 / sources 360.6–364.6 / end 364.6–382.6 ✓ |
| manifest | output_sha256 与文件一致。inputs 共 52 项，与当前 data.json、assets.json 和全部图片逐一比对，**全部一致** ✓。渲染 03:03 开始，晚于 data/assets（03:01）和 `cards.py` 加 AI 标记（02:41） |
| 渲染日志 | `done in 4120s`，没有截断 |
| 音频 | AAC 静音轨，时长 382.6 s（仍是无配乐版） |
| publish.md 章节 | 1:10 #40（70.83）、2:18 #30（138.83）、3:26 #20（206.83）、4:35 Top 10（275.07）、5:54 计分板（353.6）都与到达时间吻合。5:43 No. 1 按 publish.py 规则取冠军段前 4 s ✓ |

### 原问题逐条

| # | 原严重度 | 状态 | 核实依据 |
|---|---|---|---|
| 1 | major | **已修** | data.json 地点行改为「Serengeti National Park」，署名 Dirk Pothen / Pexels License。assets.json 的 sha256 与文件一致，selected_by 写明是按 QC #1 换的图。sources.md §4 / §5 与 publish.md 都同步了，旧图存在 `_build/old_img/30_tanzania_amboseli.jpg`。成片 138.83 s 看到金合欢树加角马群，是塞伦盖蒂草原的画面。注意：Pexels 来源页这次返回 403，我**没能独立复核 contentLocation = Tanzania**，只确认了 slug（serengeti-acacia-tree-and-wildebeest-migration）和画面都对得上 |
| 2 | major（仅风险版） | 未修（按决定不重渲） | 风险版继续判为过时，不发布，理由见结论 |
| 3 | minor | **已修** | 47.17 s：#43 卡上有黄色「AI IMAGE」标记，地点行是「Illustrative rainforest scene」，署名「AI-generated image, not a photo」✓。publish.md 写明含 AI 图，上传清单要求勾选 synthetic content |
| 4 | minor | **已修** | layout.intro_hold = 2.5。抽帧 5.0 / 6.2 / 7.4 s 时 #50 完整静止、文字完整，8.0 s 才开始滚动。最后一名完整可读约 2.5 s ✓ |
| 5 | minor | **已修** | 15.50 s：France 显示「Étretat cliffs, Normandy · With overseas: #42」，没有出框。核对过：含海外大区约 64 万 km²，大于 #42 Somalia（638k），小于 #41 Afghanistan（653k），所以 #42 正确 |
| 6 | minor | **已修** | 250.33 s 的洞察卡改为「Greenland (2.17M km²) is self-governing and listed apart from Denmark; alone it'd be 13th.」，排在 #14 之后、#13 之前，位置正确 |
| 7 | minor | **已修** | 295.47 s：India 徽章改为「INDIA'S OFFICIAL AREA」。描述框里关于克什米尔的说明还在 |
| 8 | minor | **已修** | 描述框加了「Region labels follow the UN M49 classification (Iran shown as Middle East)」。Iran 卡在 225.83 s 显示 MIDDLE EAST。由此引出一条小问题，见新问题 N1 |
| 9 | minor | **未修** | 362.5 s 的来源卡仍然没有口径行。原建议本来就附了「若渲染器支持」；口径在描述框里写全了，不阻塞发布 |
| 10 | minor | **已修** | sources.md §1 第 19 行补了重复计入的说明（阿克赛钦、伊莱米三角）。Comment 2 末行也加了一句 |
| 11 | minor | **已修** | ① Comment 2「Differences above 1%」里已经没有 Sudan，Sudan 单列一行 ✓ ② 改成「1 image marked AI-generated」✓ ③ 描述改为「see the pinned comment and the replies under it」✓（第 2 行仍写「per-item links in the pinned comment」，略不精确，可忽略）④ 上传清单改为「卡上标 AI IMAGE」✓ |
| 12 | minor | **未修** | sources.md §2 / §4 / §5 的「国家」列仍然是 UN 次区域（例如 `\| 30 \| East Africa \|`），不是国名。这是内部文档，不上屏 |
| 13 | minor（可选） | 未改 | #22 Angola 默认图没换（原建议「没有更好的就保留」） |
| 14 | minor（可选） | 未改 | #13 Mexico、#45 Kenya 没换图（可选项） |

### 新问题（本轮引入或本轮才发现）

| # | 严重度 | 位置 | 说明 | 建议 |
|---|---|---|---|---|
| N1 | minor（外观） | #17 Iran 与 #12 Saudi Arabia / #36 Türkiye / #49 Yemen | 只把 Iran 改成「MIDDLE EAST」，其他西亚国家仍显示「WESTERN ASIA」。#12 Saudi 卡上地区行是 WESTERN ASIA，标签却写「Largest in Middle East」，同一张卡上两种叫法并存。描述框已经说明 Iran 是例外，不算错，但细心的观众会注意到 | 可选：保持现状；或者把 Saudi 标签改成「Largest in W. Asia」。下次重渲时顺手处理，本期不必为此重渲 |
| N2 | minor（第 1 轮漏看，不是本轮引入） | #6 Australia（302.27 s） | 卡上只显示「Uluru, Northern Territory · Largest in Oceania」。第二个标签「Antarctic claim excluded」放不下，被渲染器省掉了，旧风险版同样如此。没有出框；这条说明在 Comment 2 里有 | 不阻塞。如果想上屏，可以删掉「Largest in Oceania」，或缩短地点行 |

另外核过、没有发现问题的：名次 1–50 连续，value 严格降序；6 张洞察卡的 after_rank 分别是 41 / 32 / 21 / 14 / 4 / 2，每张都紧跟在对应卡后面，「Next: …」说的都是下一张卡的国家；计分板 Africa 23 / Asia 13 / South America 7 / Europe 3 / North America 3 / Oceania 1，合计 50；冠军卡与 No. 1 揭晓正确；抽到的帧里都没有文字出框或占位卡。

### 抽帧（`_build/qc/recheck/`，拼图 `tile_01–08.jpg`）

- 片头：1.0 / 2.5 / 4.0 / 4.9 s；#50 停留：5.0 / 6.2 / 7.4 / 8.0 / 8.6 s
- 改动过的卡：#48 France 15.50、#43 CAR 47.17、#30 Tanzania 138.83、#17 Iran 225.83、#7 India 295.47
- 洞察卡（全部 6 张）：65.33 / 127.00 / 201.33 / 250.33 / 321.60 / 339.87
- 冠军 349.6 / 352.5；计分板 355.0 / 359.0；来源卡 362.5；片尾 370.0 / 382.4
- 随机 5 点（seed 20261104）：87.35 / 94.38 / 147.2 / 228.79 / 284.06
- 补充：Australia / Canada 标签行局部图 `crop_meta_lines.png`，风险版 Australia 对照图 `r_t299.77.png`

---

## 第 1 轮独立审片 · 2026-11-04

> 独立审片人（未参与制作），按 `qc_brief`（bible §6 ⑥ / §7）执行。只写本文件与 `_build/qc/`，未改数据、图片、渲染。
> 审片对象：`render/ep12_largest_countries_by_area_master.mp4`（默认版，sha256 df2d461f…）与 `_master_with-risk-images.mp4`（风险版，sha256 00489960…）。

### 结论：**小修后发布**（默认版）；风险版**不建议发布**

数据可靠：名次、排序与 UN DYB 2024 原表一致，抽查 26 条全部吻合。口径交代清楚，处理也站得住。两版帧数都完整（22,806 帧，与 manifest 时间线一致），版式没有出框或占位卡。

默认版发布前须修 1 条 major：#30 Tanzania 的照片实际拍摄于肯尼亚 Amboseli。另外有几条 minor，建议在同一次重渲时一起改：AI 标记、#50 停留时间、France 标签、Greenland 洞察卡措辞。

风险版不建议发布。原因有两条：一是它渲染后 data.json / assets.json 又改过，片子已过时；二是片中含非商用（NC）图和「版权保留」图，卡上直接写着「licence unknown / All rights reserved」。

### 问题清单

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| 1 | **major** | #30 Tanzania（2:16） | 来源页 Unsplash `1ZfMAnL4ubE` 位置标注为「Amboseli, Kenia」，标签有 amboseli、kenia。这是从肯尼亚一侧拍的经典「长颈鹿 + 乞力马扎罗」机位。山本身在坦桑尼亚，但图代表的是肯尼亚旅游的标志性视角，坦、肯两国观众都能认出来，也是评论区的老话题 | 换一张在坦桑尼亚境内拍的图：从 Moshi / 乞力马扎罗国家公园看山，或者 Serengeti、Ngorongoro、桑给巴尔。地点行随图改，账本与 sources.md 同步 |
| 2 | **major**（仅风险版） | `_with-risk-images` 全片 | manifest 记的 data.json / assets.json 哈希与当前文件不一致。风险版 01:05 渲染完，两个文件 01:09 才改，所以 #43 地点行仍是旧的「Dzanga-Sangha」。另外 #31 Angel Falls 是 CC BY-NC-SA 2.0（非商用），#22 Angola 来源页写明「Todos os direitos reservados」，卡上署名直接显示「licence unknown」「All rights reserved」 | 默认版作为正式片。用户若坚持用风险版：至少去掉 #22、#31 两张，用当前数据重渲，并按 publish.md 风险版说明重新生成发布文案 |
| 3 | minor（按说明：渲染器后加功能） | #43 Central African Rep.（0:44） | 母版 02:38 渲完，`cards.py` 02:41 才加 AI IMAGE 标记，所以卡上没有标记。署名行还写成「Photo: AI-generated image」，这张不是照片，「Photo:」说法自相矛盾。地点行「Central African rainforest」看起来像真实地点 | 重渲后会自动带上 AI IMAGE 标记，署名也会变成「AI-generated image, not a photo」。地点行可改成「Illustrative rainforest scene」之类 |
| 4 | minor | #50 Thailand（0:03–0:06） | 没设 `layout.intro_hold`。卡片滑入在约 5.0 s 结束，随即开始滚动，约 5.5 s 左侧文字就开始被切。最后一名完整静止可读不到 2 秒（ep02 等期都用 2.5 s） | 在 data.json 的 layout 里加 `"intro_hold": 2.5`，与第 1、3 条一起重渲（时长约 +2.5 s，章节时间会变，publish.md 需重新生成） |
| 5 | minor（观众反弹风险） | #48 France（0:13） | 用 UN 口径 551,500（本土 + 科西嘉）排第 48。维基百科、Worldometer 等大众榜单多用 643,801（含 5 个海外大区）、排约第 42。海外大区在法律上是法国本土的一部分，跟格陵兰不同，评论区大概率有人说「错了」。徽章 EXCL. OVERSEAS REGIONS 已经交代 | 保留 UN 口径，在卡上加一个标签 `{"icon":"ruler","text":"With overseas: #42"}`（18 字符，与 Canada「By land only: #4」同一种写法），把可能的批评变成知识点 |
| 6 | minor | 洞察卡 after 14（4:08） | 「Greenland … would rank 13th, but it's part of the Kingdom of Denmark」：既然说它属于丹麦王国，观众自然会问「那为什么不算进丹麦」。丹麦本土约 4.3 万 km² 加格陵兰约 221 万 km²，反而会略超沙特（2,206,714），排第 12。现在的说法在逻辑上留了口子 | 改成 UN 单列的理由，例如「Greenland (2.17M km²) is self-governing and listed apart from Denmark; alone it'd be 13th.」（≤ 90 字符；数据在 sources.md 已有） |
| 7 | minor（观众反弹风险） | #7 India（4:52，前 10 名高曝光） | 徽章「INCL. CLAIMED AREAS」符合事实，但「claimed」一词对印度观众是刺激词，名次又不受影响（去掉争议区仍是第 7）。印度是 YouTube 最大的英语受众之一 | 建议改成「INDIA'S OFFICIAL AREA」（21 字符），或干脆去掉徽章，细节留在描述框 scope_note（已写明含克什米尔全部主张地区）。巴基斯坦一侧不用标 |
| 8 | minor | 地区标签：#17 Iran「SOUTH ASIA」、#13 Mexico「CENTRAL AMERICA」、#38 Zambia / #34 Mozambique「EAST AFRICA」 | 都符合 UN M49，但大众认知是伊朗属中东 / 西亚、墨西哥属北美、赞比亚属南部非洲，会被当成错误。描述框没写明地区标签按 UN M49 划分 | 在描述框口径段加一句「Regions follow the UN M49 classification」。也可以只把 Iran 改显示为「Western Asia」/「Middle East」（计分板按大洲统计，不受影响） |
| 9 | minor | 来源卡（5:58） | 口径只放在描述框里，片尾来源卡没有一行口径说明 | 来源卡加一行（若渲染器支持）：「Areas as reported to the UN; Antarctic claims & separately listed territories excluded.」 |
| 10 | minor | 数据注记 | ① India 3,287,263 含阿克赛钦，China 9,600,000 是中方官方整数，也含阿克赛钦，约 3.8 万 km² 两国重复计算；② Kenya UN 值比 Factbook 多 11,591、South Sudan 多 14,512，量级都接近伊莱米三角（Ilemi，1.0–1.4 万 km²），可能两边都计入了；③ China 9.6M 是否含台湾说不清（DYB 脚注更像是针对人口）。三处都不改变名次 | sources.md §1 的争议地区处补一句「部分争议区可能被两国重复计入，名次不受影响」。不必上屏 |
| 11 | minor | publish.md | ① Comment 2「Differences above 1%」把 Sudan（0.88%）也列进去了；② 描述写「1 images marked」（复数错）；③ 描述写「Per-item data sources … see the pinned comment」，但置顶评论只有图片署名，数据来源在 Comment 2；④ 上传清单写「卡上标 Illustration / Render」，与实际卡面不符 | 重渲后重新跑 publish 再改措辞；Sudan 那行移到 Comment 2 的单独一行「Sudan: not in UN DYB, World Bank/FAO value」 |
| 12 | minor | sources.md §2 / §4 / §5「国家」列 | 显示的是 UN 次区域（Western Asia…），不是国名，是 gen_sources.py 的字段错用 | 改为 `name`，重新生成 |
| 13 | minor（画面） | #22 Angola 默认图 | 赤膊男子占了画面中心，与本期 image_prefer「no people as the main subject」不符，人比瀑布显眼 | 有更好的可商用 Kalandula 全景就换；没有就保留 |
| 14 | minor（画面） | #13 Mexico、#45 Kenya | Mexico：Pexels 页确认是 Chihuahua 的 Copper Canyon，但画面平、辨识度低；Kenya：剪影树配落日，卡上的数值盖住了太阳，看不出是马赛马拉 | 可选：换一张辨识度更高的（Copper Canyon 观景台 / 马赛马拉动物迁徙） |

不算问题、已核对通过的：争议口径（Western Sahara 单列、Morocco 不入榜，描述框写明「with it Morocco would rank 39th」；Ukraine 用 RECOGNISED BORDERS、Russia 不含克里米亚；南极主张不计；Taiwan 不进前 50、片中不出现）已在 scope_note、徽章和 Comment 2 中交代。不建议为 Taiwan 再加说明（没有上屏需要，加了反而徒增争议）。Venezuela/Nigeria 来源分歧已由洞察卡主动说明，处理得好。Sudan 用 World Bank 1,878,000（UN 缺值）合理，名次不变。

### 数据核对样本（主值逐条用 PyMuPDF 从 UN DYB 2024 Table 3 原 PDF 独立读出）

线上 PDF（WebFetch 取得）的 sha256 = 908f1718…，与 `_build/raw/dyb2024_table03.pdf` 完全一致。抽取脚本：`_build/qc/dyb_lines.py`。

| 名次 | 国家 | data.json value | UN DYB 2024 原表 | 交叉核对（网页） | 结论 |
|---|---|---|---|---|---|
| 1 | Russia（冠军） | 17,098,246 | 17 098 246 | Factbook 17,098,242 | ✓ |
| 2 | Canada | 9,984,670 | 9 984 670 | Factbook 9,984,670 | ✓ |
| 3 | United States | 9,833,517 | 9 833 517 | Factbook 9,833,517 | ✓ |
| 4 | China | 9,600,000 | 9 600 000 | Factbook 9,596,960 | ✓ |
| 5 | Brazil | 8,510,417 | 8 510 417 | Factbook 8,515,770 | ✓ |
| 6 | Australia | 7,692,024 | 7 692 024 | — | ✓ |
| 7 | India | 3,287,263 | 3 287 263 | — | ✓ |
| 8 | Argentina | 2,796,427 | 2 796 4|27（与脚注 68 粘连，build.py 已核读） | — | ✓ |
| 9 | Kazakhstan | 2,724,910 | 2 724 910 | — | ✓ |
| 10 | Algeria | 2,381,741 | 2 381 741 | — | ✓ |
| 12 | Saudi Arabia | 2,206,714 | 2 206 714 | Factbook 2,149,690（−2.6%，notes 已写） | ✓ |
| 13 | Mexico | 1,964,375 | 1 964 375 | — | ✓ |
| 15 | Sudan | 1,878,000 | 「...」（无值） | WB 2024 = 1,878,000（raw 与 macrotrends 一致）；Factbook 1,861,484 | ✓（口径已说明） |
| 16 | Libya | 1,676,198 | 1 676 198 | Factbook 1,759,540（网页确认，+5.0%） | ✓ |
| 17 | Iran | 1,630,848 | 1 630 848 | — | ✓ |
| 19 / 20 | Peru / Chad | 1,285,216 / 1,284,000 | 1 285 216 / 1 284 000 | 差 1,216，洞察卡正确 | ✓ |
| 31 | Venezuela | 929,690 | 929 690（与人口 27,227,930 同一行，PDF 文本层串栏） | Factbook 912,050 | ✓ |
| 32 | Nigeria | 923,768 | 923 768 | Venezuela − Nigeria = 5,922，洞察卡正确 | ✓ |
| 35 | Pakistan | 796,096 | 796 096 | — | ✓ |
| 40 | South Sudan | 658,841 | 658 841 | Factbook 644,329 | ✓ |
| 45 | Kenya | 591,958 | 591 958 | Factbook 580,367（网页确认） | ✓ |
| 48 | France | 551,500 | 551 500 | Factbook 643,801 | ✓ |
| 50 | Thailand | 513,140 | 513 140 | 第 51 名 Spain 原表 506 009 | ✓ |
| — | Greenland | （洞察卡 2.17M，第 13） | 2 166 086 | 位于 Saudi 2,206,714 与 Mexico 1,964,375 之间 | ✓ |
| — | Morocco | （不入榜） | 446 550 | 含西撒哈拉 716,550 → 第 39 | ✓ |

另：名次 1–50 连续、按 value 严格降序、无并列；value_display / secondary_display 按 3 位有效数字取整全部正确；6 条洞察卡 ≤ 90 字符，数字都能在 sources.md 追到出处（Pluto：π·2377² ≈ 17.75M km²；陆地面积 China 9,326,410 > US 9,147,593 > Canada 9,093,507）。计分板 Africa 23 / Asia 13 / South America 7 / Europe 3 / North America 3 / Oceania 1，合计 50，与数据一致。国旗 50 面逐张对过（含 Afghanistan、Mozambique、Saudi、Kazakhstan 这类细节多的国旗），全部正确。

### 图片核对（全部 55 张上屏图，拼图 `_build/qc/img_sheet_01–07.jpg`）

- 逐张看过：主体、清晰度、裁切、水印、AI 痕迹均无问题。实拍图中无 AI 痕迹，唯一一张 AI 图（#43 默认版）已在账本标明。
- 来源页的位置标注已逐张核对（Pexels 用页面 JSON，Unsplash 用 WebFetch）：Russia 是贝加尔湖（Иркутская обл.）；Iran 是 Damavand（Tehran Province）✓，正是 Haraz 路上看山的经典机位；Kazakhstan 是 Charyn ✓；India 是 Kanchenjunga（从 Tiger Hill / 大吉岭拍）✓；Zambia 是 Victoria Falls, Zambia ✓；Kenya 是 Maasai Mara ✓；Ukraine 是 Synevyr（外喀尔巴阡）✓；Pakistan 是 Saif-ul-Maluk ✓；Sudan 是 Meroë ✓；Botswana 是 Okavango ✓；Mongolia 是 Mongolia ✓；Mozambique 是 Mozambique ✓；Mexico 是 Chihuahua Copper Canyon ✓；Mali 是 Bamako 的尼日尔河 ✓；Libya 是 Libya ✓；Ethiopia 是 Ethiopia（狮尾狒）✓；Angola 默认图是 Malanje 的 Kalandula ✓；Nigeria 是 Zuma Rock ✓；Niger 是 Agadez ✓；US 是 Grand Canyon ✓。**唯一认错地点的是 #30 Tanzania（Amboseli, Kenya）**，见问题 1。
- 分辨率：#20 Chad 1024×768、#28 Mauritania 1280×850 偏小，成片里看得出略软，但可以接受（handoff 已记）。
- 风险标记合理：5 张都标成 licence unknown；sources.md 里写的是真实许可（NC / 版权保留 / 未知）。

### 成片技术核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 分辨率 / 帧率 | 1920×1080 / 60 fps（r = avg = 60/1）| 同 |
| 时长 | 380.100 s | 380.100 s |
| 帧数（`ffprobe -count_frames`） | 22,806 = 380.1 × 60 ✓ | 22,806 ✓ |
| 文件 sha256 与 manifest output_sha256 | 一致 | 一致 |
| manifest inputs 与当前文件 | 全部一致 | **data.json、assets.json 不一致（过时）** |
| 音频 | AAC 静音轨（anullsrc，−91 dB），无配乐版 | 同 |
| 时间线 | intro 0–5 / scroll 5–345.1 / champion 345.1–351.1 / tally 351.1–358.1 / sources 358.1–362.1 / end 362.1–380.1 | 同 |
| 章节时间（publish.md） | 1:08 #40、2:16 #30、3:24 #20、4:32 Top 10、5:41 No.1、5:52 计分板，与卡片到达时间吻合 ✓ | — |

两个版本的渲染日志都写「done」，帧数也完整，没有被误杀留下的截断。没有配乐版，所以响度 / 淡出检查不适用（音乐待 Suno 恢复后再审）。

### 抽帧清单（`_build/qc/frames/`，拼图 `_build/qc/mtile_01–20.jpg`、`rtile_01–02.jpg`、`intro_sheet.jpg`）

- 默认版（`m_t*.png`，78 帧）：片头 1.0 / 2.5 / 3.5 / 4.2 / 4.9 / 5.5；50 张卡各取到达屏幕中心那一帧（6.67 … 345.10，由 `_build/qc/times.py` 用渲染器 timeline 算出）；6 张洞察卡 62.83 / 124.50 / 198.83 / 247.83 / 319.10 / 337.37；冠军 347.5 / 350.5；计分板 352.0 / 354.5 / 357.5；来源卡 360.0；片尾 364 / 372 / 379.9；随机 20.4 / 97.1 / 152.8 / 214.6 / 233.3 / 283.2 / 302.0 / 341.0。
- 风险版（`r_t*.png`，8 帧）：#43 44.67、#40 68.33、#31 130.00、#22 187.00、#11 266.00、冠军 350.5、来源卡 360.0，外加片尾倒数 3 秒 1 帧。
- 看到的情况：没有文字出框或省略号截断；国旗全对；没有占位卡；计分板与冠军揭晓正确；滚动接缝处（卡片半出屏）属正常。洞察卡上没有标出处（系列惯例），出处在 sources.md §3 与 Comment 2。

### 观众视角（全球英文观众）

- **好看**：50 张满版风景几乎都是各国最有辨识度的画面（Moraine Lake、Uluru、Richat、Socotra、Deadvlei、Meroë），能当成「环游世界」来看，这是同题地图对比片没有的卖点。
- **反常识亮点**：Russia 比冥王星小、按陆地面积 China 超过 US、Chad 和 Peru 只差一个香港、Venezuela/Nigeria 换个数据源就互换名次。都放在前 10 名和中段，节奏合适。
- **可能划走**：#50–#41 这段国家冷门（Yemen、Botswana、Kenya…），画面也偏暗（剪影、阴天），开头 1 分钟留人能力一般。#50 只停留约 1.5 秒（问题 4）。建议用 intro_hold，并在片头口径行或第一张洞察卡前给个钩子（如「Africa takes almost half of this list」）。
- **评论区焦点**预计依次是：France #48（问题 5）、India 徽章（问题 7）、Kilimanjaro 图（问题 1）、Iran 被标成 South Asia（问题 8）、Greenland/Denmark（问题 6）。修完 1、5–8，评论区争的会是「口径」，而不是「你错了」。
