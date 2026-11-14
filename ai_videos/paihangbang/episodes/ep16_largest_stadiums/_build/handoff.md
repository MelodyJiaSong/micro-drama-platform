# ep16 handoff（世界最大体育场 Top 50）

> 2026-11-04 子代理交接。审片（qc.md）由主代理另起独立上下文做。

## 做了什么

1. **调研**：两个调研子任务分别查美国 33 座、其他国家 45 座（含在建 / 关闭的）球场，逐条找官方容量页 / 官方文件，原始记录（含每座球场的全部版本数字、历史容量、纪录上座）在 `_build/research/{us,world}.json`；Wikipedia 只作交叉核对（`_build/raw/` 有列表页 wikitext）。我补核了 Bernabéu（改用 FIFA 2030 申办书 78,297）、Georgia 2026 媒体指南容量表（`_build/raw/uga_2026_media_guide_sanford.txt`）、FoP 各国状态、Azteca「三届世界杯揭幕战」、Indianapolis 赛道座位数（Guinness）。
2. **数据**：`_build/items_def.py`（选择与覆盖）→ `_build/build.py` → `data.json`；`_build/gen_sources.py` → `sources.md`。N = 50，47 个名次（82,000 两座并列 28；80,000 五座并列 36）。冠军 Narendra Modi Stadium 132,000；美国 25 座。
3. **找图**（follow-up 016 / 023 / 追加要求 3–5）：
   - 第一步内容：`_build/content/NN_<slug>.md`（调研子任务写的外观、经典角度、易混淆对象），要点浓缩成 `img_queries.py` 的 image_hint 与检索词（hint 已写进 data.json）。
   - 第二步：`_build/flickr_search.py`（Flickr 公开搜索页，只收 CC BY / BY-SA / CC0 / PD）→ Flickr 中途限流后改 `_build/bing_search.py`（Bing 图片 async 端点：可商用过滤一路 + 放开许可一路 `--open`）。没再调用 Codex 搜索。
   - 下载：`_build/prefetch.py`（curl 顺序下载，Flickr 原图 `_o` 被 429，`_build/fix_sizes.py` 把直链换成 2048 px 的 k 尺寸）；`_build/image_reselect_ep16.py` 是 `_tools/image_reselect.py` 的副本（加了 429 退避、`NO_FETCH=1` 只建 meta），apply 用它。
   - 挑图：`_build/contact.py` 出全候选拼图（`_build/reselect/contact*.jpg`），逐张看后用 `apply --override` 定稿；默认版替代图用 `_build/attach_alts.py` 挂 `image_alt`（契约 v1.4）；`_build/fix_credits.py` 给许可不明的图写「via 域名 / licence unknown」署名。
   - 生成图：11 张，`tools/codex_image.py`（请求日志自动记在 `ai_videos/paihangbang/request_log.md`），prompt 在 `_build/gen/*.txt`，全部是「看台球迷背影 + 国旗 / 球队色」示意图，不复现真实建筑、无真人脸、无 logo；逐张看过，一次合格。
4. **渲染**：`render/ep16_largest_stadiums_master.mp4`（默认版）与 `render/ep16_largest_stadiums_master_with-risk-images.mp4`（风险版），静音；`publish.md` 由 `rank_scroll publish` 生成后人工补写。

## 图片来源分布（50 卡）

| | 默认母版 | 风险版 |
|---|---|---|
| 可商用照片（CC BY / BY-SA / PD / Unsplash / Pexels）且无 FoP 风险 | 9 | 9 |
| 可商用替代照片（image_alt） | 30 | — |
| AI 生成示意图（image_alt） | 11（6 座 FoP 国 + Tiger Stadium、广东奥体、杭州奥体、Bernabéu、Atatürk） | — |
| 风险照片（licence unknown 32 张；FoP 9 张，其中 FNB / Lusail / Stade de France 本身是 CC / PD 许可） | — | 41 |
| 占位卡 | 0 | 0 |

## 关键口径与默认（详见 topic.md「待用户确认」、sources.md §1–§3）

- 主值 = 当前官方**座位**容量（不含站票、临时看台、纪录上座）；MCG 取 95,000（总 100,024 含约 5,000 站位）；Dortmund / Croke Park / Allianz Arena 按座位跌出榜外。
- 不收赛车场 / 赛马场、已拆除 / 重建中 / 在建 / 只部分重开（Camp Nou 62,652 → 不收）。
- 五一体育场 114,000 为估算，屏上 "seats, est." + ESTIMATE 徽章。
- Beaver 用 2025 官方 106,304；Bernabéu 用 FIFA 申办书 78,297；Ohio 用 2026 game notes 102,041。
- 约 15 项主值来源是 aggregator（StadiumDB / Wikipedia 转引官方文件 / AP），sources.md §5 逐条注明。
- 国家 = 所在地；同容量同名次（标准竞赛排名）；容量显示完整整数（不按 3 位有效数字，避免并名次）。

## 没解决的问题

1. **第 50 名对 5 个座位敏感**：Camp Randall 76,130（Wisconsin 2026 game notes 年表）vs 第 51 Empower Field 76,125（无官方页，Wikipedia / Walter P Moore）。同一份 game notes 里还有 76,057 / 76,030，若取后者两者互换。发布前 7 天复核。
2. Misr Stadium 的真实照片极少：风险版用的是 estatebook 博客里的一张场内实拍（1024×665，偏小、像视频截图）；其他候选多为效果图，已排除。
3. 若干风险版照片分辨率偏低（Modi 1920、MetLife 1080×610、Oklahoma 1024×614、Borg El Arab 975×650、Stade des Martyrs 1080×720、Azadi 840×560、Camp Randall 1200×675），满版卡上会略软；要升级需在 Google 图片里再找。
4. 一些默认版替代照片观感一般（Williams-Brice、Jordan–Hare、Ben Hill Griffin 是外立面 / 看台局部，Ohio 是旧航拍），但对象认对、许可可商用。
5. Flickr 公开搜索与静态图在 10 个代理并发时反复限流（429 / 空结果），所以不少 Flickr 候选没下到（Bernabéu、Atatürk 的 CC 图），这两项默认版因此用了生成图；限流解除后可重跑 `_build/prefetch.py --only 40,44` 再换成实拍。
6. 渲染：默认母版 6:20（380.1 s，22,806 帧，1080p60，ffprobe 与 manifest 一致，全片解码无错）。风险版第一次渲染被我自己串行命令里重复启动的同名渲染写坏（解码报 NAL 错），已删掉重渲；我只按自己的 PID 结束了那个重复进程。
7. **我的失误（需主代理知悉）**：约 22:20 我用 PowerShell 按命令行含 `flickr_search` 结束自己的进程时，误杀了 ep13（statues，`flickr_search.py ... _a/_b`）、ep14（volcanoes，`_build/flickr_search.py a/b`）、ep20（waterfalls，`flickr_search.py b`）三个期的找图进程。它们需要各自重跑（输出已存在的批次可能已部分写出）。之后我只按 ep16 专属参数匹配进程。

## 需要用户决定

1. 主值用「座位」口径（vs 含站票总容量）。
2. Beaver（106,304 vs 2026 临时扩容约 108–109k）、Bernabéu（78,297 vs 83,186）、Camp Nou 不收、Clemson 含草坡座区。
3. 9 座 FoP 国球场：默认版用球迷照 / AI 示意图替代，风险版用实拍；是否发风险版。
4. 32 张许可不明的风险照片（多为官方 / 新闻 / 壁纸站）是否签字放行；默认版已全部有可商用或生成图。
5. 含 11 张 AI 生成示意图：上传时须勾选合成内容声明（已写进 publish.md）。

## QC 第 1 轮修改（2026-11-04，主代理授权）

- **B1**：#34 Estadio Monumental（秘鲁）换成 Flickr「Estadio Monumental: Lima - Perú」（erico luxero，CC BY-SA 2.0，夜场内景），直接作主图（可商用，无风险标记）；错图（Estadio Nacional）已移出账本。
- **B2**：#20 Jordan–Hare 风险图换成 auburntigers.com 的满场实拍（licence unknown）。**B3**：#41 Bernabéu 换成 2025-02 新外立面实拍（Carmelo Peciña，CC BY 2.0），两版都用，不再是风险图。
- **M1**：Tiger 默认版换成 Flickr「Tiger Stadium in Baton Rouge」（Roy Luck，CC BY 2.0）；Rungrado 换成「May Day Stadium, Pyongyang」拱顶全景（David Stanley，CC BY 2.0）；MetLife 换成 CC BY-SA 满场内景作主图；FNB 风险图换成完工后的夜景（CC BY 2.0）。广东奥体、杭州奥体、Atatürk 全网（Flickr CC 单线程间隔 3 s、Bing 可商用过滤、Unsplash / Pexels）都没找到可商用实拍，改为无图卡「No free-licensed photo found」，不用 AI 编造；FoP 国 Misr、Borg El Arab、JIS 改为无图卡「Photo withheld: no freedom of panorama」。AI 图从 11 张降到 3 张（Lusail、Stade de France、Azadi，均为 FoP 国、只画球迷背影，带 AI IMAGE 角标）。Camp Randall 默认版仍是比赛近景（背景能看到红色看台），没找到更好的可商用全景；FNB / Martyrs / GBK 按 FoP 扣下原则维持不以建筑为主体的实拍。
- **M3**：Beaver 徽章改「2025 OFFICIAL FIGURE」，并在 #5 后加洞察卡「Next: Beaver Stadium. On Oct 10, 2026, temporary stands let in a record 114,419 fans.」（出处 ClutchPoints / Penn State 公布）；为保持 6 张洞察卡，删掉了 Indianapolis 赛车场那张（口径仍在 scope_note）。
- **M4**：洞察卡改「Five stadiums list a round 80,000 seats…」，sources.md §6 补 Stade de France 80,698。**M5**：layout.intro_hold = 2.5（全片 382.6 s）。**M6**：封面改选 MCG / Wembley / Rose Bowl（`thumb: true`），不出现冠军。**m1**：Camp Randall 徽章改「+100 SEATS IN 2026」。**m3**：sources.md 补 Azteca 90,000 / 87,000 版本。**m12**：publish.md AI 署名去重（`_build/publish_post.py`）。
- 默认版图片分布：可商用实拍 41（主图 12 + 替代 29）、AI 3、无图卡 6；风险版 38 张风险图（licence unknown 29、FoP 9）+ 12 张可商用主图。
- 未处理：m6 Cotton Bowl 裁切、m7 旧貌照片、m8 Modi 替代图分辨率、m10 水印说明、m11 Misr 风险图身份待签字前复核。

## 主代理补充决定（2026-11-04）

- 广东奥体、杭州奥体、Atatürk 默认版改用 `tools/codex_image.py` 生成的写实球场外观图（prompt：`_build/gen/*_v2.txt`，按 content 资料描述飘带顶棚 / 莲花花瓣 / 新月形顶棚；无文字、logo、人物），一次合格，`assets/img/*_gen2.png`。只重渲默认版。
- 默认版现为：可商用实拍 41、AI 生成 6（3 张球迷示意 + 3 张球场外观，均带 AI IMAGE 角标）、无图卡 3（Misr、Borg El Arab、JIS：Photo withheld: no freedom of panorama）。

## 复核返修（2026-11-04）

- **N1**：#27 MetLife 主图换成 Flickr「Metlife Stadium Meadowlands New Jersey」（Anthony Quintano，CC BY 2.0，能看到 MetLife 字样和场内），两版共用；误用的 Yankee Stadium 图已移出。之后每张新图都按来源页标题核过。
- **N2**：#34 Monumental 设 `image_focus [0.0, 0.6]`，「U」字座椅马赛克进入画面（preview 确认）。
- **N4**：publish.md 描述首段加注「6 cards marked AI IMAGE use AI-generated images… 3 of them show real stadiums drawn from public descriptions, so details are not accurate」（`_build/publish_post.py`，也回应 N3）。source_line 未改（两版共用）。
- **M1 / m**：Luzhniki 默认版换成夜景外观全景（Konstantin Malanchev，CC BY 2.0）；AT&T 设 `image_focus [0.3, 0.45]`，默认版穹顶入画。Camp Randall、Martyrs 没有更好的可商用球场全景，维持；FNB、GBK 按 FoP 原则维持非建筑主体实拍；m6 Cotton Bowl 唯一可商用图招牌太宽，裁切无法完整入画，维持；m8 冠军替代图仍是 Pexels 1000×750（没有更大的可商用图）。
- 两版按当前数据重渲。
