# ep15 · 世界最深湖泊 · 交接（子代理 2026-11-03）

## 做了什么
- 调研 → `topic.md`、`data.json`（契约 v1.4，theme `abyss`，card_w 720）、`sources.md`（逐条出处、测量方式与年份、交叉核对、争议、洞察依据、图片许可）。数值唯一定义处 `_build/items_def.py`，`build.py` → `data.json`，`gen_sources.py` → `sources.md`。原始抓取在 `_build/raw/`（Wikipedia wikitext 带 revid、ILEC 数据册、Minowa 2023 / Tournier 2025 全文抽取、UNESCO 页）。
- 找图第一步内容落盘：`_build/content/NN_<slug>.md`（36 份，来自 Wikipedia 文字 + 调研笔记），要点写进每项 `image_hint`。
- 找图：Codex 搜索第 1 轮（8 批，codex_b*.json）→ 用户改规则后停用 Codex 搜索（第 2 轮 r2 被中途停止，未产出文件；request_log 里可能有 1–2 条无结果的请求）→ Claude 自己找：Pexels / Unsplash 站内搜索页（`claude_stock.json`，`stock_cands.py`）、Flickr CC 站内搜索（`claude_flickr.json`，`flickr_cands.py`）、全网页面取图（`claude_web.json`，`web_cands.py`）。逐张看拼图（`_build/sheets/`）后在 `_build/choices.json` 定稿，`final_apply.py` 写图与 `assets.json`（支持 `image_alt` 与生成图）。
- Codex 只做出图（`tools/codex_image.py`，请求日志脚本自动写）：10 张，均亲眼看过，一次通过。
- 校验：`validate --strict` 默认版 / `--allow-risk-images` 均 OK；预览帧（片头、#33–#35、洞察卡 Poso / Sarez / Viedma / Baikal、前 10、冠军、计分板、来源卡）已看。
- 渲染：默认母版 `render/ep15_deepest_lakes_master.mp4`、风险版 `render/ep15_deepest_lakes_master_with-risk-images.mp4`（ffprobe：1920×1080、60 fps、286.8 s，静音），各抽 3 帧看过；`publish.md`（默认版）与 `publish_with-risk-images.md`（风险版）。

## 关键口径与默认（详见 topic.md「待用户确认」与 sources.md §1–§3、§6）
- N = 36：天然湖、最大实测水深 > 400 m 全收；里海算湖；冰下湖（Vostok）、水库不收；Lake Chelan（小坝抬高 6.4 m 的天然湖）收。
- 改正常见错值：Poso 450 → 395 m（2022 多波束，出榜，做成洞察卡）、Fagnano 449 → 206 m（出榜）、O'Higgins 836 → 799 m、Argentino 719 → 607 m、Issyk-Kul 702 → 668 m。
- 争议：Viedma 取 ~750 m（2023 论文）而非 900 m（2022 新闻稿），卡上 DEPTH DISPUTED + 洞察卡；Argentino 取 607 m，DEPTH DISPUTED。
- 国旗：按湖面占比最大国；里海按岸线最长（哈萨克斯坦）；Tanganyika 按 FAO 表用刚果（金）（Wikipedia 写坦桑尼亚，不用）；Kivu（刚果金）、Superior（美国）按惯例，未核面积划分。
- 计分板按大洲：Asia 9 > North America 8 > South America 7 > Europe 5 > Oceania 4 > Africa 3。

## 图片来源分布（36 卡）
- 默认母版：可商用照片 26 张（Pexels / Unsplash / Flickr CC BY-SA / EGU CC BY 3.0 / Arto Teräs CC BY-SA 3.0）+ Codex 生成图 10 张（#11 Matano、#13 Hornindalsvatnet、#14 Quesnel、#18 Salvatnet、#21 Hauroko、#22 Cochrane、#22 Tinn、#24 Adams、#28 Great Bear、#33 Khantayskoye）；无占位卡。
- 风险版：许可不明照片 11 张（#3 Caspian、#4 O'Higgins、#8 Great Slave、#11 Matano、#13 Hornindal、#14 Quesnel、#21 Hauroko、#22 Cochrane、#22 Tinn、#24 Adams、#28 Great Bear —— 其中 #3/#4/#8 默认版用可商用替代图，其余 8 张默认版用生成图），生成图 2 张（#18、#33：全网没找到合格照片）。
- 生成图卡上署名「AI-generated image (not a photo)」，账本 licence「AI-generated (Codex image_gen)」，publish.md 已写明并要求上传勾选合成内容声明。

## 没解决的问题
1. **Flickr 静态图被 429 限流**（多代理同时抓），Flickr CC 候选约 125 张只下到 5 张（Tanganyika 2、Great Slave 3，看过都不如现图）。下载脚本已停。之前以为有的「Great Slave East Arm 悬崖 CC0」是候选编号错位造成的误标，实际不存在（该图许可不明，仍在风险版）。其余 Flickr CC 候选（Hornindalsvatnet Eduard Marmet CC BY-SA 2.0、Quesnel / Hauroko / Cochrane / Adams / Great Bear / Matano / Tinn / Caspian 各若干）没有看过，可能替换默认版的生成图。限流解除后：`cd _build && python flickr_slow_dl.py` → 共用 `image_reselect.py download` → `normalize_meta.py` → `sheet_all.py` 看图 → 改 `choices.json` → `final_apply.py` → `gen_sources.py` → 重渲默认母版（本机多代理并发时约 45 分钟）。
2. 默认版几张图偏弱：#3 Caspian（阴天灰色礁石）、#4 O'Higgins（900×600 放大）、#8 Great Slave（房屋占画面）——都是 Flickr 能升级的项。
3. 渲染器 `publish` 的章节分组对 N=36 漏掉 #36–#31（只认 50/40/30/20 段起点），publish.md 已手改为「0:00 Intro & #36–#21」，建议主代理修生成器。
4. 共享 WebSearch 额度中途用尽过：Murdie 1999、Crowe 2008、Petticrew 2015、Seppälä 2005、NVE 1984 测深图等记为「经 Wikipedia 转引」；Lake Wakatipu 420 m 未能核到一手（代理印象 NZ 测深更低，约 380 m，若属实则出榜）。
5. 时长约 4:47，低于 bible 建议 5–8 分钟（N 由数据决定）。

## 需要用户决定
- topic.md「待用户确认」7 条（N=36、里海、Vostok、Viedma/Argentino 取值、Kivu/Superior/Tanganyika 国旗）。
- 风险版 11 张许可不明照片是否签字使用；默认版 10 张 AI 生成图是否接受（或等 Flickr 解禁换真图）。

## 2026-11-04 独立审片后修复（qc.md：B1、B2、M1–M4 + 部分 minor）
- **B1**：Lake Wakatipu 移出（420 m 无出处；LINZ NZ 252 为 376 m，MfE/LAWA 与 NZJMFR 1970 为 380 m），改为 **Top 35**；Khantayskoye #33、Grey #34、Superior #35；计分板 Asia 9 / NA 8 / SA 7 / Europe 5 / Oceania 3 / Africa 3。Poso 洞察卡改为合并说 Poso 与 Wakatipu 两个旧值。Hauroko、Manapouri 的出处改为条目本身（不再写 Lowe & Green）。
- **B2**：#5 Viedma 换成 Flickr「Glacier Viedma and Lago Viedma」（Su--May，CC BY 2.0，5184×3456；作者说明是坐游船去冰川），焦点 [0.5, 0.75]。
- **M1**：#8 Great Slave 默认版换成 Flickr「Great Slave Lake in Yellowknife」（Alan Sim，CC BY-SA 2.0），能看到大片湖面，焦点避开告示牌；风险版仍用 East Arm 悬崖图（J. Hipfner，许可不明）。
- **M2**：渲染器已有 `layout.intro_hold`，已设为 2.5 s。
- **M3**：明写版权所有的 4 张（#3 Caspian、#4 O'Higgins、#22 Cochrane、#28 Great Bear）已从风险版撤下，两版都用默认图（#22、#28 用生成图）。风险版剩 7 张许可不明照片，卡面署名只写作者或来源站名。
- **M4**：用修好的生成器重新生成两份 publish，章节为 0:00 / 0:28 / 1:42 / 2:55 / 4:03 / 4:14。描述加了里海最深点在南里海、Poso 与 Wakatipu 的改正说明；AI 生成图的「source file」写成 generated for this video。
- **minor**：Viedma 洞察卡措辞与测深年份（2017–2020）已改；改正旧值的标签放到第一位；Issyk-Kul 换成能看到湖面的 Pexels 图（Nizar F）；Great Bear 标签改为「Largest wholly in Canada」；after 2 洞察卡改成不点名冠军；De Batist 年份改为 2001；补抓 Poso 论文正文 PDF。
- **当前图片分布**：默认母版 25 张可商用照片 + 10 张生成图；风险版换上 7 张许可不明照片。
- **未处理**：封面草图仍写出 #1–#3（渲染器默认，审片 minor 9）；#33/#35 的图片文件名仍用旧名次编号（34/35 的文件叫 35_lago_grey、36_lake_superior，不影响渲染）；Flickr 下载仍受限流，其余 CC 候选没看完。
- **重渲（2026-11-04）**：两版均 `validate --strict` OK；`render/ep15_deepest_lakes_master.mp4` 与 `render/ep15_deepest_lakes_master_with-risk-images.mp4` 均为 1920×1080、60 fps、16,976 帧 = 282.93 s，与 manifest 时间线一致；抽帧看过（片头首卡停留、#5 Viedma、#8 Great Slave 两版、Poso/Wakatipu 洞察卡）。publish.md / publish_with-risk-images.md 已重新生成并补人工内容（标题 Top 35 Ranked、里海最深点、AI 图说明、合成内容声明）。
