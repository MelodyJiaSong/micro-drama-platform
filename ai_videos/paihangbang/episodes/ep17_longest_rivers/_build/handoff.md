# ep17 世界最长河流 Top 50 · 交接（2026-11-03）

## 做了什么

- **调研与数据**：主值统一取 Encyclopaedia Britannica 当前条目（britannica.com 直连被 Cloudflare 拦，经 web.archive.org 2025–2026 快照取原文，`raw/brit/`、`raw/brit_lengths.json`）；Murray–Darling 取 Geoscience Australia 水系值 3,672 km。交叉核对：Wikipedia「List of river systems by length」（revid 1380355572，解析为 `raw/wp_rows.json`）、Liu et al. 2009（前 10 名卫星+实地测量，`raw/liu2009.pdf`）、INPE 2008、Wikidata P2043。条目定义唯一手改处 `items_def.py` → `build.py` → `../data.json`；`gen_sources.py` → `../sources.md`。
- **N = 50**（Rio Negro 与 Ubangi–Uele 并列第 46）。冠军 Nile 6,650 km（Egypt）。大洲计分：Asia 20 · South America 12 · North America 7 · Africa 6 · Europe 4 · Oceania 1。
- **洞察卡 6 条**（after 44/38/29/21/13/2），均在 `sources.md` §5 核过；含 D2（Colorado 很少入海、2009 卫星测量、INPE 2008）与反常识（3 条亚马孙支流都比多瑙河长）。
- **内容抓取**（follow-up 016 第一步）：`content/NN_<key>.md` 50 份（Britannica 原文摘句 + Wikipedia 导语 + 找图要点）。
- **找图**：
  - 第一轮 Codex 联网搜索（follow-up 023 前，`reselect/codex_b00–b09.json`）；第二轮 Codex 补搜启动后按 follow-up 023 立即终止，2 条已记 request 的补记了 Cancelled（未产出、未重提）。
  - 之后全部由 Claude 做：4 个子代理用 Unsplash / Pexels / Pixabay / Flickr CC 站内检索（`reselect/claude_01–04.json`），我再用 Flickr CC 检索补了 12 项难找的（`claude_05.json` 与 cand 里的 `f1`），逐张看拼图（`reselect/sheet_*.jpg`、`final_default.jpg`、`final_risk.jpg`）。
  - 下载器 bug：claude_* 与 codex_* 混排时候选编号错位——发现后已改 `image_reselect_ep17.py`（固定 codex 在前），**清空 cand 重下重评**，再选图 apply；最后脚本核对 data.json 每张图/替代图与 assets.json 的 sha256、作者、许可一一对应（无不符）。
  - 全网都找不到合格图的 8 处用 Codex 出图（`tools/codex_image.py`，prompt 在 `gen/`，日志在 `ai_videos/paihangbang/request_log.md`），每张亲眼看过，均一次合格。
- **校验与渲染**：`validate --strict`（含 `--allow-risk-images`）通过；预览看过片头、洞察卡、前 10、冠军、计分板、来源卡；`thumb`、默认母版、风险版、`publish` 均已出（见最终报告的路径与时长）。

## 图片统计

| 版本 | 可商用实拍 | 许可不明实拍 | AI 生成 | 占位卡 |
|---|---|---|---|---|
| 默认母版 | 42 | 0 | 8（Purus、Lower Tunguska、Ubangi 为主图；Madeira、Japurá、Vilyuy、Olenyok、Kasai 为默认版替代图） | 0 |
| `_with-risk-images` | 35 | 12（Amur、Murray–Darling、Madeira、Juruá、Japurá、Vilyuy、Paraguay、Pilcomayo、Ural、Olenyok、Aldan、Kasai） | 3 | 0 |

- 主动剔除的风险图：Lena（来源页署 Getty Images）、Ubangi（Le Monde / Panos 图片社）——图库/图片社来源不进任何版本，改用 CC BY 实拍（Lena，Artem Svetlov）和 AI 图（Ubangi）。
- 低分辨率但可用：Lena、Juruá、Pilcomayo 的 Flickr 图只拿到 1024 px（原图链接被 Flickr 429 限流），Aldan 替代图 1023 px，Yellow River 以外的 Pixabay 直链 1280 px。Flickr 恢复后可重下原图提升清晰度（页面与原图链接在 `cand/*/meta.json`）。
- 可再升级：Mackenzie 用的是同水系的 Peace River（Alberta）秋景；Ob–Irtysh 用的是额尔齐斯河新疆五彩滩（同水系上游，国旗按河口为 Russia）；Orinoco 图偏平淡（Flickr CC BY-SA）。

## 关键口径与默认（详见 topic.md「待用户确认」）

1. 长度统一用 Britannica（11 条与 Wikipedia 列表或 Liu 2009 差 > 10%，最显眼的是 Zambezi 3,540 vs 常见 2,574–2,740）。
2. 国旗 = 河口所在国（Nile → Egypt，Ganges/Brahmaputra → Bangladesh，Colorado → Mexico）；界河河口取流域较大一方。
3. Songhua / Pearl / Red River (US) 没取到 Britannica 值未收（按维基值会进 44–49 名）。

## 没解决 / 需要注意

- **误杀进程（需主代理知悉）**：为重渲本期，我用 PowerShell 按命令行匹配 `rank_scroll render` 结束进程，匹配面过宽，**同时结束了当时其他期正在跑的 rank_scroll 渲染（及相关 bash/ffmpeg 进程，约 37 个 PID）**。无法事后确认是哪几期；请主代理让其他期检查渲染是否中断、需要重跑。
- WebSearch 本会话额度曾用尽；Britannica 搜索片段只核到 Amu Darya、Pilcomayo、Olenyok 三条（快照正文缺失或 404），已在 notes 标明。
- 竞品发布时间：YouTube 要求登录，yt-dlp 取不到。

## 需要用户决定

1. 长度口径（统一 Britannica）与 Zambezi 值。
2. 国旗规则（河口所在国）。
3. 风险版 12 张许可不明图是否放。
4. 含 8 张 AI 生成图（默认版）——上传须勾选合成内容声明；是否接受。

## 2026-11-04 QC 第 1 轮后的修订（主代理决定，只重渲默认版）

- B1：补收 Araguaia（Britannica 2,627 km，#32，图为巴西旅游部 MTur 公有领域实拍 Aruanã 段）。
- M1/M2：离群值例外规则（同源同口、差 > 25%、无口径解释 → 用通行值）——Zambezi 3,540 → 2,574（#34），Orinoco 2,740 → 2,140 出榜（#51），Kasai 留在 #50。缺水系合计例外仅限 Murray–Darling 这类（Britannica 有分段值无合计），Pearl 按此不收。规则写进 scope_note 与 sources.md §1。
- M3：页眉 / 片头统计行加「Flag = where the river ends」，卡上国家行改「ENDS IN …」（country_name = "Ends in X"），预览确认不出框。
- M4：#21 Indus 换成巴基斯坦苏库尔（Sukkur）Lansdowne / Ayub 桥实拍（Unsplash，Danish Rasool）。
- M5：layout.intro_hold = 2.5。m4：Lena、Pilcomayo 替代图升级到 Flickr 2048 px。
- 洞察卡 after_rank 改为按名次自动计算（Danube after 28、亚马孙支流 after 20）。计分板仍是 Asia 20 · South America 12 · North America 7 · Africa 6 · Europe 4 · Oceania 1。
- 风险版保持 QC 前旧文件，不发布、未重渲（与当前 data.json 不一致）。
- 图片文件名里的名次前缀是初版名次，名次变动后未改名（build.py 现保留原路径）。
