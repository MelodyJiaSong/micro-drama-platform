# ep18 · Fastest Production Cars · 交接（handoff）

> 2026-11-03 子代理（follow-up 015 / 016 / 023 / 追加要求 3–4）。不写 qc.md，审片由主代理另起上下文。

## 做了什么

1. **调研 → 数据**：`_build/items_def.py`（唯一数据源）→ `build.py` 生成 `data.json`、`_build/content/NN_*.md`（每项内容摘要：记录细节、外观辨认、易混淆对象、image_hint）→ `gen_sources.py` 生成 `sources.md`。Wikipedia 原文存 `_build/raw/`（只作交叉核对）。`topic.md` 按模板写好。
2. **N = 28**（严格 >350 km/h 的量产公路车，数据只够 28，不凑数）；VERIFIED 14 / CLAIMED 14；6 张洞察卡；tally 按品牌国：美 7 > 法 6 > 英 4 > 瑞典 / 德 / 意 3 > 中 / 克罗地亚 1。冠军 **Yangwang U9 Xtreme 496 km/h**（2025-09 ATP 认证，单向）。
3. **找图**（全程没有调用 Codex）：
   - 第一步内容落盘 `_build/content/`；第二步 Claude 自己在 Flickr 可商用 CC（BY/BY-SA/CC0/PDM）站内搜索两轮（`_build/find_imgs.py`，候选拼图 `_build/find/sheet_*.jpg`，逐张看过挑选写 `_build/picks.py`）→ `picks_to_claude.py` 解析 2048 px 大图写 `_build/reselect/claude_b01.json` → `image_reselect.py download / score / apply --override …`（看了 review_01–03）。Pexels 站内搜索被 Cloudflare 拦，Unsplash 401，Openverse 被拦。
   - 放开来源（追加要求 3）：WebSearch 找页面 → `_build/webimgs.py` 取页面大图 → 看拼图 `_build/find/web/*/sheet.jpg` → `_build/finalize_risk.py` 把 5 张全网图放进 image（`image_risk = "licence unknown"`），可商用图挪到 `image_alt`。
   - 裁切：卡宽 800（汽车多为横幅），11 张设了 `image_focus`；`_build/focus_sheet.py` 出裁切框拼图核对。
4. **图片来源分布**（按追加要求 5 质量优先又升级了 2 张：W16 Mistral、Venom F5 改用厂方纪录 / 跑道新闻图）：
   - 默认母版：27 张可商用实拍（Flickr CC BY / BY-SA / CC0）+ 1 张占位卡（Czinger 21C）。
   - `_with-risk-images` 版：28 张全有图 = 21 张可商用 + 7 张许可不明的全网图（Yangwang U9 Xtreme 纪录车、W16 Mistral 纪录车、Czinger 21C Goodwood 现场、Venom F5 KSC 跑道、Rimac Nevera R、Dauer 962 LM 公路版、Bugatti Centodieci），这 7 项默认版除 Czinger 外都有可商用 image_alt。
   - AI 生成 0 张（Codex 一次都没调用，request_log 无新增）。单独补搜：Flickr 第二轮 13 项；全网检索 9 项（上述 7 项 + Tuatara、Ultimate Aero 看过但现图更好未换）。
5. 校验 `validate --strict` 通过（仅提示 Czinger 默认版扣图）；预览帧在 `render/preview/`（默认）与 `render/preview/risk/`；封面 `render/thumbnail.png`；母版与风险版见 `render/`。

## 关键口径与默认（详见 topic.md「待用户确认」）

- 量产 = 同规格客户车 ≥10 台且 2026-11 前已开始交付；每车型一张卡、取最快公路版本；国家 = 品牌发源国。
- VERIFIED = 独立第三方计时的最快**单向**速度（双向平均写在 tag）；CLAIMED = 厂方额定或厂方自测；设计目标、仿真不算（Venom F5 用实跑 271.6 mph 而非 311+ 目标；Jesko Absolut 无官方数字不收）。
- 未交付不收：Bugatti Tourbillon、Koenigsegg Gemera、Zenvo Aurora、Aspark Owl。额定恰好 350 的不收（P1、F80、W1、LaFerrari、Revuelto、SU7 Ultra）。

## 没解决的问题

1. **默认版的替代图不是同一版本**（风险版是对的车）：#5 Mistral 默认是另一台绿色客户车（同车型，可以）、#7 Venom F5 默认是博物馆银色车（同车型）、#1 默认显示标准版 Yangwang U9（不是 Xtreme）、#10 显示标准版 Rimac Nevera（不是 Nevera R）、#13 显示 1994 年勒芒参赛版 Dauer 962 LM（不是公路版）、#18 Centodieci 只有尾部局部。可商用实拍里找不到对应版本；风险版用的是对的车。
2. **Czinger 21C 默认版是占位卡**：Flickr 可商用里没有真实照片（唯一一张 CC0 是 AI 图/渲染，已排除），全网图（Goodwood 现场照）许可不明 → 只进风险版。按追加要求 3/4，「已有全网合格图」不触发 Codex 生成；如主代理要默认版也有图，需另定（生成图要避开车标，且会让一辆真实车型由 AI 图代替）。
3. Flickr 站内搜索在第二轮后被限流（返回空结果 / 429），#11 SSC Ultimate Aero 首选白车图没下成，改用同作者蓝车（车门打开、人群背景）。
4. 两项主值只有 aggregator 级来源：Dauer 962 LM（Evo 2003 / Auto Bild 经 Wikipedia 转引）、EB110 SS（Wikipedia，另有 351 km/h 说法）。
5. 渲染器缺：发动机 / 速度表类图标（只能用 calendar、users、ruler、trophy、flag 代替）；publish 自动章节写成「#20–#11」（应为「#28–#11」，publish.md 已手改）。
6. WebSearch 配额曾用尽（10 个代理共享），Divo / Centodieci / ZR1 / Noble / One-77 / AMG One / Countach / Aventador 的数值主要靠 Wikipedia 引用的厂方 / 媒体链接核对，没有逐个打开原文。

## 需要用户决定

1. 入榜线 >350 km/h、N = 28 是否接受（要 30+ 就得收 350 并列的一串）。
2. 实测取单向最高（Agera RS 显示 458 而非常见 447）是否接受。
3. 预产 / 原型纪录车（Chiron 300+、U9 Xtreme、McLaren F1 XP5）按纪录计是否接受。
4. 风险版 5 张全网图（BYD、Rimac、Bugatti 新闻图与 evo、Goodwood 媒体图）能否签字放进发布版；不签字就发默认版（含 1 张占位卡和 3 张「同车型不同版本」的替代图）。
5. 国家按品牌发源国（EB110 计法国、Pininfarina 计意大利）。

## 成片

- 默认母版 `render/ep18_fastest_cars_master.mp4`：1920×1080、60 fps、15,733 帧、4:22（静音）。第一次渲染进程中途退出（exit 255，只写出 4,681 帧、没有 manifest），已重渲，ffprobe 帧数完整。
- 风险版 `render/ep18_fastest_cars_master_with-risk-images.mp4`：规格同上，4:22。
- 两版都从成片抽了 3 帧看过（`_build/frames/`）。publish.md 对应默认版，已手改章节「#28–#11」、描述和标签。

## 第 1 轮审片后修订（2026-11-04，qc.md「必须修」）

- **B1** 补 Koenigsegg CCX：官网 CCX 页「Top Speed: 400+ km/h (250+ mph) (without rear wing)」，Wikipedia：CCX 30 台（另 9 台 CCXR）→ 400 km/h CLAIMED，#16。图：Flickr CC BY 2.0（pyntofmyld，蓝色 CCX）。
- **M1** Jesko Absolut：Koenigsegg 2024-07 新闻稿（racecar.com 全文转载）写「from standstill to 412 km/h and back to zero」，数据由 Racelogic 设备记录、Racelogic 英国总部核验；GoAuto 同述 → 按「独立计时单向最高」规则 412 km/h VERIFIED，#12，tag「Peak in 0-400-0 test」。图：Flickr CC BY 2.0（David Merrett，银色 Absolut）。
- 于是 **N = 30**（实测 15 / 宣称 15），标题、kicker、计分板（瑞典 5）、洞察卡计数同步；#3 后洞察卡改为「By Guinness rules the record is still the Tuatara's 455 km/h two-way average (2021).」
- **M2–M4**：Flickr 可商用再搜一轮（_r3），仍无 U9 Xtreme、Nevera R、Dauer 公路版 → 默认版署名写明「standard U9 shown / standard Nevera shown / 1994 Le Mans race car shown」（卡上与 publish.md 都标了）。冠军卡默认图车身仍偏满（原图就是近景），找不到更好的可商用整车图。
- **M5**：Czinger 21C 默认版用 `tools/codex_image.py` 生成写实插画 1 张（第 1 次即合格：整车、无 logo、无牌照），`assets/img/06_czinger_21c_gen.png`，作 image_alt，账本 licence「AI-generated (Codex image_gen)」；publish.md 已改为合成内容声明 Yes。请求日志由脚本自动写入。
- **M6**：metric_label 改为「Top speed · VERIFIED one-way run or maker CLAIM」（片头与页眉都显示）；scope_note 写明单向规则与 Guinness 双向纪录 Tuatara 455 km/h；置顶评论首段点明并列出「Not listed」。
- 小修：Tuatara tag「2021 2-way avg 455」(m6)；F1 加「XP5 prototype, 1998」、U9 加「Prototype record car」(m7)；ZR1 notes 改为 ATP Papenburg 2024-10 双向 233.08/233.50 mph、图是敞篷 ZTK (m5)；Czinger notes 写明 253/281 两说、tag「Low-drag spec」(m10)；Dauer 主源换 Auto Bild，notes 写 402/404.6 两数 (m9)；918 / F5 notes 写清计时方 (m8)；`layout.intro_hold = 2.5` (m11)；章节时间码按 timeline 重算 0:00 / 2:27 / 3:50 / 4:09 (m12)；sources.md 重新生成 (m14)。
- 未改：#18→#20 Divo / Chiron / Tuatara 的构图（横幅图在方卡里只能水平移动焦点，竖向无余量）；Centodieci 默认图仍是车尾局部（无可商用整车图）；m15 Tourbillon 交付状况发布前复核；m16 U9 风险图是否 CGI 需用户向 BYD 核对。
- 修订后两版重渲完成：默认母版、风险版均 1920×1080、60 fps、16,723 帧、4:38.7，manifest 已写；抽帧（`_build/frames/n_*.jpg`）看过：片头口径行、Top 30、#1 署名「standard U9 shown」、计分板瑞典 5 均正确。

## 复核后小修（2026-11-04，qc.md 复核段）

- n1 sources.md 正文与 data.json 对齐：`gen_sources.py` 固定段改为 N = 30、并列 20 / 25、第 30 名 918、Jesko 以 412 VERIFIED 入榜、CCX 从「未收」删除（CCXR 归入 CCX 家族）、4 张洞察卡依据补齐，已重新生成。
- n2 McLaren F1：subtitle 缩为「Ehra-Lessien」，tag 改为「XP5 prototype」「2-way avg 386」，卡上三项都显示（预览 97.4 s 已看）。
- n3 Czinger AI 图用 `tools/codex_image.py` 重出为低阻车身（长尾、无大尾翼、无 logo / 牌照），`assets/img/06_czinger_21c_gen_lowdrag.png`，旧的大尾翼版移到 `_build/old_img/`；共调用 Codex 出图 2 次（均有 request_log）。
- n4 #6 后洞察卡改为「Chiron 300+ customer cars are capped at 440 km/h; the 490 run used a pre-production car.」，Guinness 双向纪录只留 #3 后一张。
- n5 publish.md：重新 publish 后补章节（0:00 / 2:27 / 3:50 / 4:09）、pictured 说明、AI 图声明（Altered or synthetic content → Yes）、置顶评论口径段与 Not listed，修「1 image」语法。
- m3 Chiron 换成同组候选 c1（Charles, CC0，草坪上的黑橙 Super Sport，车更大）。m1 Centodieci、m4 Tuatara Striker、m9 EB110 拍卖页佐证、m17 Saleen 未改（无更好的可商用图 / 无可靠页面）。
- 只重渲默认母版（风险版不重渲、不推荐）；封面已重出。
- 默认母版重渲完成：1920×1080、60 fps、16,723 帧、278.717 s；抽帧（_build/frames/f_*.jpg）看过 F1 三项信息、Czinger 低阻 AI 图与 AI IMAGE 标记、#6 后新洞察卡、冠军卡。风险版保留上一轮成片，未重渲，不推荐。
