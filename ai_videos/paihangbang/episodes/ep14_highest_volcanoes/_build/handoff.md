# ep14 世界最高火山 · handoff（子代理 → 主代理）

> 2026-11-03，follow-up 015 子代理。未写 qc.md（独立审片由主代理另起上下文）；未 commit；未跑 followup.py；未调 Suno / ElevenLabs / Dreamina。

## 做了什么

- **数据**：GVP 官方 GeoServer WFS 下载 Holocene（1,214 座）与 Pleistocene（1,452 座）全表（`raw/gvp_*.json`，2026-11-03）。按 GVP 峰顶海拔取 Holocene 前 50（无并列；#50 Popocatépetl 5,393 m，#51 Ticsani 5,382 m）。Wikipedia infobox / 导言作交叉核对（MediaWiki API 批量取，`raw/wiki_extracts_2026-11-03.json`）。生成链：`items_def.py` + `build.py` → `data.json`；`gen_sources.py` → `sources.md`。
- **topic.md / sources.md / publish.md** 已写；publish.md 经 `post_publish.py` 收尾（标题、AI 图署名合并、合成内容声明 Yes、标签、版本说明）。
- **找图**（follow-up 016 / 023 / 追加要求 3–5）：
  1. 每项内容落盘 `content/NN_*.md`（GVP 地质概述 + Wikipedia 导言 + 辨认要点 / 易混对象），要点写进 `data.json` 的 `image_hint`。
  2. Codex 联网搜：第一轮 10 包全做完；第二轮（`research_items.py`）跑到 4 包时按 follow-up 023 停掉（另有一次 `codex_image.py` 生成 Tipas 的调用在停用通知时被我杀掉，日志里该请求结果未知、未落图）。
  3. 我自己搜：Pexels 网页搜索（`pexels_search.py`，必须用 Git 的 curl，urllib / Windows curl 会被 Cloudflare 拦）、Bing 图片全网检索（`bing_search.py`）、低清项再全网升级一轮（`upgrade.py`，单独补搜 7 项：Socompa、Sairecabur、El Cóndor、Coropuna、Cayambe、Láscar、Tutupaca，换了 3 张）。Flickr 可商用搜索（`flickr_search.py`）跑了一会就被限流降级（每页只回 3 条），结果未采用；Openverse 429 + Cloudflare，Unsplash 搜索页 401，Pixabay 403。
  4. 全网都没有可商用图的项，默认版用 Codex 生成（追加要求 4/5 允许；`gen_ai.py` → `tools/codex_image.py`，prompt 在 `gen_prompts/`），39 次生成全部一次合格（逐张看过；另有上面那次被中止的 Tipas 调用）。
  5. 下载用的是一次**全新**的 download（旧 cand 挪到 `reselect/cand_old/`），apply 后逐项核对 assets.json 的 source_url / 作者 / 许可与 meta 一致（重复 URL 的 5 项是同一张图），不受 image_reselect 编号错位 bug 影响；之后**没有**再跑修好的 download（会重排编号）。
- **图来源分布**：
  - 默认母版：可商用照片 10 张（Unsplash 9、Pexels 1）+ ESO CC BY 4.0 替代 1 张（#34 Purico 的 image_alt）+ Codex 生成图 39 张（32 张风险图的 image_alt + 7 张 AI-only）。**无占位卡。**
  - `_with-risk-images` 版：真实照片 43 张（可商用 10 + 风险 33：许可不明 18、来源页写明保留所有权利 14〔Andeshandbook〕、Pixnio 1）+ AI-only 7 张。
  - AI-only（全网找不到合格照片，两版都用生成图）：#33 Olca-Paruma、#36 Tupungatito、#38 Colachi、#39 Nevados Casiri、#41 Guayaques、#47 Corrida de Cori、#49 Cerro Bayo。试过：Codex 两轮、Pexels、Bing（结果只有 GVP CC BY-NC 图、卫星图 / 地图、同名滑雪场 Cerro Bayo、低清小图）。
- **封面**：`thumb` 设在 #18 Sabancaya、#20 Cotopaxi、#50 Popocatépetl（都是可商用真实照片，避免封面全是 AI 图）。改 thumb 标记发生在母版开渲之后，母版 manifest 里的 data.json sha 与现文件差这一字段，不影响画面。

## 关键口径与默认

- 只收 GVP Holocene 名单（含 Evidence Uncertain）；海拔一律用 GVP 值；跨境火山国旗 = GVP Country 字段第一个国家 + SHARED WITH 徽章（18 座，全部 Chile 在前 → 计分板 Chile 30）。
- 标签：calendar = GVP 最近喷发年（BCE / c. … CE / 年份；无年份写 Eruption date unknown 或 Holocene status unclear）；mountain = GVP 火山类型。2026 年有喷发的 3 座加 ERUPTED IN 2026 徽章。

## 没解决的问题

1. **默认母版 39 张 AI 生成图**：画面真实但不是真山，卡上署名「AI-generated image (Codex)」，publish.md 已写合成内容声明 Yes。风险版图更真实，但 33 张要签字（Andeshandbook 14 张明示保留所有权利，需联系作者）。
2. **Pixnio**（#21 Miñiques，「free for personal and commercial use」）不在渲染器许可白名单，只能进风险版；主代理可决定是否加白名单。
3. 风险图里有 2 张分辨率偏低（#6 El Cóndor 800×600、#42 Láscar 1024×666），卡上略软；#9 Pular 原图右下角有很小的摄影师署名水印。
4. #30 Antisana 的 Unsplash 页 WebFetch 打不开（socket hang up），图来自 Codex 第二轮「search-indexed as Antisana」，看图与 Antisana 冰川体一致，但未能在来源页核到地点标签。
5. GVP 网页（volcano.cfm）对脚本是 Cloudflare 验证页，数值以 WFS 为准；Peakbagger 403 未核。竞品发布时间 yt-dlp 被拦未取到。

## 需要用户决定

见 `topic.md`「待用户确认」1–5：Holocene-only 口径、全用 GVP 海拔、跨境国旗规则、默认版 AI 图 vs 风险版、Pixnio 白名单。

## 渲染结果（2026-11-04）

- 默认母版 `render/ep14_highest_volcanoes_master.mp4`：6:20.1（380.1 s），1920×1080，60 fps，h264（静音 aac 轨），92.6 MB；10 个代理同时渲，4.7 fps，用时 81 分钟。
- 风险版 `render/ep14_highest_volcanoes_master_with-risk-images.mp4`：同规格，86.1 MB。
- 两版各抽 3 帧看过（`render/preview/frames_master.jpg`、`frames_risk.jpg`），另有片头 / 洞察卡 / 前 10 / 冠军 / 计分板 / 来源卡预览帧；未见文字出框、国旗错位或裁切问题。
- 封面 `render/thumbnail.png`（#18 Sabancaya / #20 Cotopaxi / #50 Popocatépetl 三张可商用实拍）。
- `publish.md` 对应默认母版；改发风险版须 `publish --allow-risk-images` 后再跑 `_build/post_publish.py`。

## 审片修复（2026-11-04，按主代理指令处理 qc.md 第 1 轮「必须修」）

1. **San José** 改用 GVP 地质概述的 5,856 m（WFS 字段 6,070 m 是邻峰 Marmolejo）：`build.py` 的 `ELEV_FIX`，重排后 San José 排 #24，原 #15–#24 上移；Sabancaya → #17，洞察卡「Next: Sabancaya」改为 after 18，封面重出（#17 / #19 / #50）。publish 章节重生成。
2. **#25 Cordón de Puntas Negras**：原风险图是 Miscanti，撤掉；Bing 再搜 3 轮只找到 Salar de Talar / Piedras Rojas 的湖景，认不出目标火山，**两版都用生成图**。
3. **#18 Licancabur**：换成 Pexels（alisha jean）以 Licancabur 为主体的正面锥体图，`image_focus [0.5, 0.3]`。
4. **NASA 公有领域真实影像**（`_build/nasa_alts.py`，裁切中心都看图定过）：#1 Ojos del Salado（iss074e0760459，Laguna Verde 与火山群俯瞰）、#2 Llullaillaco（ISS022-E-8285）、#5 Coropuna（ISS025-E-6163）、#6 El Cóndor（ISS024-E-12425，NASA 图注点名 Cerro el Cóndor / Peinado 一带）、#7 Parinacota（EO「Volcanic Duo」斜视）、#9 Pular（ISS029-E-17352）、#12 Aracar（ISS006-E-13813，偏雾）、#13 Guallatiri（ISS009-E-6848）、#40 Ubinas（ISS013-E-66488，喷发灰柱）、#48 Tata Sabaya（ISS035-E-18006，锥体 + 崩塌丘）。都作默认版的 image_alt（风险版仍用原地面风险图）。#3 Tipas、#4 Incahuasi 没找到认得出的 NASA 影像，仍是生成图。
   - 现分布：默认版 AI 29 / NASA 10 / Unsplash 8 / Pexels 2 / ESO 1；风险版 风险图 32 / Unsplash 8 / AI 8 / Pexels 2。
5. **洞察卡**：冠军不点名（after 3 改为「Both of the final two are active…」）；「Chile 30」改为「18 of these 50 volcanoes sit right on a national border」；scope_note 写明跨境火山在计分板只按卡片国旗计一次。
6. **标签**：Evidence Uncertain →「Possible recent activity」；Olca-Paruma →「Eruption observed」；Kilimanjaro 洞察卡改措辞；片头口径行改为「Active (Holocene) volcanoes by summit elevation · Smithsonian GVP, Nov 2026」；描述第二行写明 Holocene-only 与 AI 图数量。
7. AI 标注由渲染器自动加（黄色 AI IMAGE 徽章 + 「AI-generated image, not a photo」），已在预览里确认。
- 另顺手修了 qc 的小项：#11 Sierra Nevada、#13 Guallatiri、#42 Láscar、#43 Orizaba 的裁切焦点；sources.md §5 的计数改为动态统计。
- 修复前数据备份：`_build/data_before_qcfix.json`、`_build/assets_before_qcfix.json`。
- **重渲（2026-11-04 03:29）**：两版都是 22,806 帧 = 380.1 s × 60 fps，1920×1080，与 timeline 一致；两份 manifest 里的 data.json / assets.json sha256 与现文件一致。抽帧 `render/preview/qcfix_frames.jpg`（默认版 #21–#11、#8–#1，风险版 #21–#11）看过：NASA 图、AI IMAGE 徽章、Possible recent activity 标签、新口径行都正常上屏。validate --strict 两种模式都通过。

## 复核小修（2026-11-04，qc.md 文首复核段）

- **俯视图换地面实拍**：Flickr CC 搜索已恢复（单线程、每次请求间隔 3 s，`flickr_search.py r2`；CDN 下载要带 Referer 才不 403）。#1 Ojos del Salado（sergejf，CC BY-SA 2.0，峰顶近景，`image_focus [0.35, 0.4]`）、#2 Llullaillaco（Dick Culbert「Llullaillaco del este」，CC BY 2.0，1000×809）、#5 Coropuna（CC BY-SA 2.0，`[0.3, 0.45]`）、#12 Aracar（Kevin Jones，CC BY 2.0）、#13 Guallatiri（Matt and Kim Robinson，CC BY-SA 2.0，带喷气）。都作默认版的 image_alt（`_build/set_alt.py`）。
- #6 El Cóndor、#9 Pular 没有地面实拍，默认版改回生成图；#48 Tata Sabaya 保留 NASA 图（锥体 + 崩塌丘能认出来）；#7 Parinacota、#40 Ubinas 保留 NASA 图。
- **生成图重出**（`_build/gen_ai2.py`，Codex 只做出图）：#44 Isluga、#23 Taapaca 去掉教堂、村庄、梯田；#4 Incahuasi 改成宽阔山体。#2 Llullaillaco 也重出了一张（嶙峋峰顶），但最后用了 Flickr 实拍，生成图没上屏。
- **AI 声明**：source_line 改为「Source: Smithsonian GVP (VOTW) · Some images are AI-generated」（61 字符，来源卡和底栏都显示）；描述第 2 行写明 31 of 50。
- scope_note 补了 San José 的重音；topic.md 的计数和待确认项按现数据改了；publish 重新生成后补了人工内容；封面重出（#17 / #19 / #50，都是实拍）。
- 现分布（默认版）：AI 31、Unsplash 8、Flickr CC 5、NASA 3、Pexels 2、ESO 1。
- 只重渲默认版；`render/ep14_highest_volcanoes_master_with-risk-images.mp4` 还是 03:29 那版，与现 data.json 不一致，不推荐发布。
- 渲染中途为加回 #48 的 NASA 图，按自己的 PID（95048）停过一次渲染，然后重开。
- **复核小修重渲（2026-11-04 04:5x）**：默认版 22,806 帧 = 380.1 s × 60 fps，1920×1080；manifest 记录的 data.json / assets.json sha 与现文件一致。抽帧 `render/preview/m3_frames.jpg`（#45–#43、#24–#23、#5–#4、#2–#1）看过：#1、#2、#5 是地面实拍，#44 Isluga、#23 Taapaca 不再有建筑，底栏显示「Some images are AI-generated」。validate --strict 通过。
