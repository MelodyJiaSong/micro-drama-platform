# ep12 · 交接（2026-11-03，子代理）

## 做了什么

1. **调研与口径**：主源 UN Statistics Division《Demographic Yearbook 2024》Table 3 的 Surface area 2024 列（PDF 存 `raw/`，`parse_dyb.py` 按坐标抽列）；交叉核对 CIA World Factbook 最终版（2026-02 停刊，`factbook/factbook.json` 2026-01-22 最后同步，CC0/公有领域）；World Bank AG.SRF / AG.LND 2024 只作参考（其 2024 序列明显异常：Canada 15,634,410、Norway 624,500、Sweden 528,860）。Sudan 在 DYB 2024 无值 → 用 World Bank/FAO 1,878,000。
2. **data.json**：`items_def.py`（人工定义：ISO、M49 大洲、照片题材、标签、徽章、notes）→ `build.py`（读 raw，算值、显示、交叉核对）；`mk_text.py` 写洞察卡与 scope_note；`gen_sources.py` 生成 `sources.md`。N = 50，冠军 Russia 17,098,246 km²；大洲计分 Africa 23 / Asia 13 / South America 7 / Europe 3 / North America 3 / Oceania 1。
3. **找图**（follow-up 016 → 023 → 用户追加要求 3/4）：
   - 第一步：`fetch_content.py` 抓每项 Wikipedia 文字到 `content/`，`image_guide.py` 补「找图要点」并写 image_hint。
   - Codex 联网搜索跑了第 1 轮全部 10 包 + 第 2 轮（`image_search2.py`）前 5 包（下标 0–24）；用户 023 叫停后终止，r2_05 / r2_06 两个未完成请求已在 `request_log.md` 补 error 事件（不重提）。
   - 之后全部由 Claude 用 WebFetch（Pexels / Unsplash 站内搜索页、Flickr 照片页、EGU 媒体库）+ 少量 WebSearch 自己找：`claude_cands.py` → `reselect/claude_01.json`、`claude_02.json`（直链逐个 GET 验证）。
   - download → score → **逐张看 `sheet_*.jpg`（`contact_sheet.py`，全部候选按卡比例裁切）** → apply（全量 --override）→ `add_alts.py`（契约 v1.4 image_alt）。
4. 校验 `validate --strict` 通过；预览帧已看（片头、#48–46、CAR 占位、SSD 洞察、Venezuela 洞察、#23–21、Greenland 洞察、China/US 洞察、冠军、计分板、来源卡）。

## 图片结果（50 卡）

- 默认母版：**49 张可商用照片**（Pexels / Unsplash / CC BY / CC BY-SA / NASA 公有领域），其中 4 张是风险项的默认替代（image_alt：DR Congo、Angola、Venezuela、South Sudan）；#43 Central African Rep. 用 **AI 生成图**（主代理决定，`tools/codex_image.py`，写实雨林瀑布、不对应具体地点、无人物无文字，prompt 在 `_build/car_prompt.txt`，作 image_alt；卡上地点行改为 Central African rainforest）。默认母版因此重渲，publish.md 已注明含 AI 图、上传勾选合成内容声明。
- 风险版 `_with-risk-images`：50 张全有图。风险图 5 张（image_risk = licence unknown）：#11 DR Congo Nyiragongo 熔岩湖（bucolicae.com，Hanspeter Gass，许可不明；用户追加要求 5 质量优先升级）、#22 Angola Kalandula 全景（expedia.com.br，版权保留）、#31 Venezuela Angel Falls（Flickr ron brinkmann，CC BY-NC-SA 2.0，非商用）、#40 South Sudan Sudd 航拍（Marcus Westberg / National Geographic España，许可不明）、#43 CAR Dzanga Bai 森林象（Daniel Hoops，许可不明）。
- AI 生成：1 张（#43 CAR，默认版）。
- 题材调整（原计划找不到可用图）：Libya → 利比亚撒哈拉绿洲航拍（替 Ubari 湖）；Iran → Mount Damavand（替 Lut 沙漠雅丹，免费图只有一张暗的剪影）；Niger → Agadez 大清真寺（16 世纪泥砖，UNESCO）；Mali → 巴马科尼日尔河（Bandiagara 无可商用图）；Ethiopia → Simien 狮尾狒；Venezuela 默认版 → Canaima 国家公园瀑布与平顶山；Mozambique → 莫桑比克海岸航拍；Somalia → 摩加迪沙海岸古堡；South Sudan 默认版 → Sudd 湿地卫星影像（INPE，CC BY-SA 2.0）；Mauritania → Richat 结构（NASA ISS 照片，公有领域）。
- 低分辨率：#20 Chad 三张 Flickr CC BY 2.0 原图只有 1024×768（卡高 800，基本无放大）；#28 Mauritania NASA 图 1280×850。

## 候选编号错位 bug 的核对（主代理通知）

- 我在 apply 之前已发现同一问题：删掉所有含 claude 候选的项的 cand 目录，用当时的工具全部重下，再逐张看图后 apply，所以没有错配。
- 收到通知后没有重跑 download（新排序会让 c<k> 重新编号，与我已核对的 override 对不上），改为**逐张核对**：`verify_assets.py` 重新下载 assets.json 里每个 source_url，与上屏文件比 32×32 灰度差与宽高比——53 个文件中 52 个一致（差 ≤ 0.1）；#13 Mexico 的 Pexels 原图（6000×4000）两次下载超时，未比对，但 Mexico 没有 claude 候选、编号从未变动，且图已目视确认是铜峡谷类峡谷。
- 用户追加要求 5（质量优先）复查：Libya 更经典的 Ubari 湖照片来源页明写「禁止任何使用」，不放进风险版；DR Congo 升级为熔岩湖彩色照（风险版）。Mali（巴马科尼日尔河）仍偏弱：Bandiagara / Hand of Fatima 无可商用图，且风险图与默认替代图题材不同会让卡上地名对不上，暂保留。

## 关键口径与默认（待用户确认，详见 topic.md）

1. 主源 UN DYB 2024（各国官方数），Factbook 交叉核对；差异 > 1% 的 7 项写进 notes：Saudi Arabia、Libya（UN 168 万 vs CIA 176 万，差 5%）、Iran、Venezuela、South Sudan、Kenya、France。
2. France 只算本土 + 科西嘉（551,500，第 48，徽章 EXCL. OVERSEAS REGIONS）；含海外大区则约第 42。
3. 西撒哈拉按 UN 单列，不计入 Morocco；若计入（Factbook 口径 716,550）Morocco 第 39，Thailand 掉出。
4. 克什米尔：India 用含主张地区的官方数（徽章 INCL. CLAIMED AREAS），Pakistan 用不含 AJK/GB 的官方数；名次不变。Ukraine 国际承认边界（徽章 RECOGNISED BORDERS），Russia 不含克里米亚。
5. 南极主张一律不计（Australia、Argentina、Chile、France）。
6. 名次敏感：Venezuela/Nigeria、South Sudan/Afghanistan、Kenya/Madagascar/Botswana 的先后随来源变（洞察卡 2 主动说明 Venezuela/Nigeria）。
7. 卡上国家行改放 UN M49 次区域（East Africa、South Asia…），因为名称行已是国名；Russia 写 Europe & Asia。计分板大洲按 M49（Russia → Europe）。

## 没解决的问题 / 需要主代理处理

1. **#43 Central African Rep.（已由主代理决定用 AI 图解决）**：Pexels、Unsplash（含 Unsplash+ 以外）、Flickr CC、WebSearch「Dzanga Bai Creative Commons」都没有可商用 CAR 照片。按用户追加要求 4 未生成（有风险图）。如要默认版无占位：主代理用 Google 图片再找，或决定改用 Codex 生成（`assets/img/43_central_african_rep_gen.png` 作 image_alt）。
2. **共用工具 bug（image_reselect.py download）**：候选 id 按 `sorted(codex_b*.json + claude_*.json)` 编号，`claude_` 排在 `codex_` 前面；对已下载过 Codex 候选的项再加 claude 文件后，新 meta 的 c0… 指向旧的 c0.jpg 文件（下载时文件已存在就跳过），许可与图片错配。我删掉受影响项的 cand 目录全部重下解决了；建议主代理改成 codex 在前或按文件名哈希命名。另：download 每次重写 meta.json，会冲掉手工修正的许可（我用 `fix_meta_licences.py` 在 apply 前重写）。
3. `image_reselect apply` 对 CC BY-NC-SA / 版权保留的图统一写 image_risk = "licence unknown"，sources.md 里按来源页写了真实许可。
4. Pexels 作者名多数取自下载文件名里的用户名（如 carlos-jamaica、yahyesomali），Pexels License 不要求署名，但描述框里显示的是用户名。
5. 竞品视频发布时间未取到（yt-dlp 单视频请求失败）。
6. WebSearch 配额曾用尽（会话共享 200 次），中途主要靠 WebFetch。

## 需要用户决定

- 上面「关键口径」1–5；风险版 5 张图是否签字使用（Angel Falls 为 NC 许可，商用频道原则上不能用）。
- #43 CAR 默认版占位 vs 生成图。

## QC 后修订（2026-11-04，主代理决定）

- #30 Tanzania 换图：原 Kilimanjaro+长颈鹿实拍于肯尼亚 Amboseli（QC major）；改用 Pexels Dirk Pothen 的 Serengeti 照片（来源页 contentLocation = Tanzania），地点行 Serengeti National Park，旧图存 `_build/old_img/30_tanzania_amboseli.jpg`。
- #43 CAR：地点行改「Illustrative rainforest scene」；渲染器自动显示 AI IMAGE 标记与「AI-generated image, not a photo」。
- layout.intro_hold = 2.5（片长 382.6 s / 22956 帧）。
- France 加标签「With overseas: #42」；India 徽章改「INDIA'S OFFICIAL AREA」；Iran 地区行改 Middle East（描述框注明地区按 UN M49）；Greenland 洞察卡改为「…is self-governing and listed apart from Denmark; alone it'd be 13th.」。
- sources.md 补「部分争议区可能被两国重复计入，名次不受影响」；publish.md 重新生成并修 QC #11 各项（Sudan 单列、单复数、置顶评论指向、AI 标记说明）。
- 只重渲默认母版；**风险版不推荐、未重渲**（其 data/assets 哈希已过期）。
