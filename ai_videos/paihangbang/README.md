# 排行榜（paihangbang）· 数据排行滚动视频系列

## Vision（观众体验）

> **几分钟看完一份全世界的最新排名：每张卡一眼看懂是谁、哪国、多少、第几，看到最后才知道冠军是谁、哪个国家上榜最多。**

核心：数字真实、有出处、是最新的；每一期都有观众原本不知道的变化（谁在涨、谁在跌、谁是新上榜）。

（Vision 由代理起草，**待用户确认**。）

| 体验 | 怎么做到 | 规范位置 |
|---|---|---|
| 一眼看懂 | 卡片固定解剖：国家条 → 主图 → 名称 → 主数值 → 变化 → 小图标 → 名次；同屏 3 张，匀速滚动 | `bible.md` §2 |
| 看到最后 | 倒数到第 1 名；前 10 名减速放大；国家计分板压轴 | `bible.md` §2.2、§1 D3 |
| 真实、可争论 | 每个数字可追溯到来源和统计期；描述框附来源 | `bible.md` §3 |
| 每期不一样 | 洞察卡、名次变化、主题皮肤、题材族和呈现方式轮换 | `bible.md` §1 |

## 这是什么，不是什么

- 是参考片格式（Country Cassette《Top 50 Best Selling Car Brands in the World (2026)》，5 分钟，48.8 万播放）的**系列化、数据可信版**。
- **不是短剧**：不走 three-module-v1 六模块，没有 `workflow.json`，不需要人物、分镜、Seedance。
- 本目录的规则只在本系列生效（剧级）；要升到仓库级，须用户明确同意。

## 文件

| 文件 | 内容 |
|---|---|
| [bible.md](bible.md) | 制作圣经：定位与差异化、格式规范、数据规范、版权、音乐、单集流程、审片清单、技术路线 |
| [topics.md](topics.md) | 第一季 10 期选题、打分、试播建议、每期 `topic.md` 模板 |
| [0_research/reference_analysis.md](0_research/reference_analysis.md) | 参考片逐帧拆解，频道与竞品的实测播放（原始数据在 `0_research/data/`） |
| [0_research/genre_and_topics.md](0_research/genre_and_topics.md) | 赛道、同类频道、YPP 变现风险、格式变体、候选选题 |
| [0_research/toolchain.md](0_research/toolchain.md) | 数据源许可、图片 / logo / 国旗 / 图标版权、渲染器比较、音乐、本机工具现状 |
| `episodes/epNN_<slug>/` | 每期产物（尚未开始），结构见 `bible.md` §6 |
| `release/` | **正式版**（每期稳妥版英文 + 中文视频与封面，render 的硬链接）与预览页：`release/index.html` 总览，`release/<期>/index.html` 单期（双语播放器、发布稿一键复制、审片结论、待定事项）。用 `python ai_videos/paihangbang/_tools/release.py` 收录 / 刷新，`--check` 只报告；某期改发风险版写进 `release_choices.json` |

需求记录：`specs/ai_video/paihangbang/user_input/`。收费服务（Suno、ElevenLabs、Codex 出图）的请求日志归属本目录 `request_log.md`，经 `tools/service_request.py` 写入。

## 状态（2026-11-03 夜间自主推进后）

- ⛔ **配图硬闸门（用户 2026-11-05，follow-up 054，`bible.md` §4.0）：每张卡必须有高质量配图，否则不出片。** `python ai_videos/paihangbang/_tools/tile_gate.py check` 判（零空卡 + 裁后分辨率 + 逐卡独立审图），未过的期 `release.py` 不收录、`upload.py` 不上传。2026-11-05 首次检查 16 期全部未过：所有期都还没有逐卡独立审图记录；另有空卡——ep01 23 个名次、ep02 23 个、ep06 默认版封面全扣、ep13 9 个、ep16 3 个（默认版），且都不在榜尾、不能靠截短解决，须补图或改发签字后的风险版。下面各期「可发布」结论均以过此闸门为前提。

- ✅ 调研、Foundation（`bible.md`、`topics.md`、`data_contract.md`）。
- ✅ 渲染器 `projects/rank_scroll/` v0.1（规格 `specs/development/rank_scroll/`，13 项测试通过）。
- ✅ ep02 各国最高峰：数据 + 49/50 图 → 母版 `episodes/ep02_highest_peak_by_country/render/ep02_highest_peak_by_country_master.mp4`（约 6:12，静音）。2026-11-03 按用户反馈改版（follow-up 004）：满版照片卡，卡宽 720。第 4 轮独立审片结论「可发布（静音画面版），只需小修」（`qc.md`）。
- 🟡 ep01 世界最高建筑：数据 + 45/50 图（其中 5 张 FoP 风险图默认不放）→ 母版 `episodes/ep01_tallest_buildings/render/ep01_tallest_buildings_master.mp4`（约 5:29，静音），已改成满版照片卡（follow-up 004）。第 4 轮审片：版式达标，但 10 张无图卡（含第 1 名）在新版式下更显眼，须先定 FoP 图怎么处理（见下表第 1 项）。
- 🟡 ep04 世界最大陆地动物 Top 30（follow-up 012/018/022/030/035/039/042）：数据（成年雄性典型体重，逐条出处见 `sources.md`）+ 30/30 实拍图（iNaturalist CC / Pexels / Unsplash / 美国政府公有领域；爪哇犀、野牦牛默认版用 Commons 博物馆标本图，风险版用许可未知的野外照）→ 带 Suno 配乐母版 `episodes/ep04_largest_land_animals/render/`（4:16；默认版 + 风险图版）。三轮独立审片 + 第 4 轮独立复核，结论「可发布（默认母版静音画面版）」，minor 已改（`qc.md`）；上传前须用户签字森林象取值（M8）。配乐：Suno v2 任务 101bce70 两首纯音乐，2026-11-04 用 `_build/add_music.py` 补音轨（不重渲），独立配乐审片见 `qc.md`。审片页 `http://127.0.0.1:5174/rank-preview?path=ai_videos%2Fpaihangbang%2Fepisodes%2Fep04_largest_land_animals`。
- 🟡 ep05 历史上致死人数最多的 30 种病毒（follow-up 013/016/024/034/038）：数据（有据总数 + GBD/WHO 年度锚点推算，标 est.）+ 30/30 高清主图（实拍电镜 19 张 + AI 插画 11 张，卡上标 AI IMAGE）+ Suno 配乐 → 带配乐母版 `episodes/ep05_deadliest_viruses/render/ep05_deadliest_viruses_master.mp4`（4:18）；三轮画面审片 + 两轮配乐审片（`qc.md`）。预览：http://127.0.0.1:5174/rank-preview?path=ai_videos%2Fpaihangbang%2Fepisodes%2Fep05_deadliest_viruses 。待用户：认可口径与 6 条单国例外、是否保留乙肝 / EB / SARS 的 AI 插画（`topic.md`）。
- 🟡 ep06 史上最畅销日本漫画 Top 30（follow-up 014/019/026）：数据（出版社公布的累计发行量，口径与取舍见 `sources.md` §2）+ 30/30 高清封面（Claude 与此前 Codex 两轮联网找图、逐张核对作品）→ 带图版主片 `episodes/ep06_best_selling_manga/render/ep06_best_selling_manga_master_with-risk-images.mp4`（3:37，配 Suno 原创纯音乐：两首手工拼成底轨，独立音频审片后修了接点），默认版封面全扣下、同样配乐。两轮独立审片 + 音频审片已改完（`qc.md`），配乐待人耳试听；待用户定：用不用版权封面、18 个月旧数字例外、Crayon Shin-chan 剔除。
- 🟡 ep03 30 家 AI 公司（列表期，不排名；follow-up 010/017/025/032/036/037）：Claude 三路调研 + 独立事实核查（`_build/qc_data_independent.md`，已按报告修正）；每家 logo、公司图、创始人头像三类参考图全部下载在 `assets/ref/`；渲染器新增列表模式与公司卡（rank_scroll follow-up 004/012/013）。两版母版（约 4:05）：**签字版** `render/ep03_ai_companies_master_with-risk-images.mp4`（真实照片，多数许可未知、含 6 张通讯社图，需用户签字）与**默认版** `render/ep03_ai_companies_master.mp4`（全部可商用：CC 实拍或 Codex 生成插图，每卡有图）。配乐：Suno 两首（57 s + 72 s）接链循环铺底，2026-11-04 补下第二首后两版重渲，待人耳试听。独立审片 `qc.md`：小修后可发布，blocker / major 已处理，待用户看片与签字。
- 🟡 配乐（2026-11-04 08:50 更新：账号现显示 Song credits 10,000、Downloads 60，下载额度暂停已按服务自带方法解除，暂停记录存档为 `automation-paused.cleared-*.json`；ep11 / ep13 / ep14 / ep20 已出歌并配上。09:00：ep11 / ep13 / ep16 的 v2 uncertain 任务按库重新认领均未找到（确认没生成）；ep16 v3（6728b05e）又只出 62 s / 58 s，改用「长结构」提示词的 v4（181445fe）两首各 172 s，已用 `ep04…/_build/add_music.py` 只换两版 ep16 母版音轨（无静音段），短曲留在 `assets/music/` 与 `v3/`。以下为 02:30 旧记录，suno_browser_service follow-up 009）：Suno 服务已修好并跑完一轮。**已下载 2 首**、放进 `episodes/<期>/assets/music/`：ep12、ep15、ep17、ep18、ep19；ep05、ep06 的歌在服务输出目录（由各自会话取用）；ep16 只有 72 s / 60 s 两首短曲；ep03 两首已取回（第二首 11-04 补下）。**未出歌**：ep11、ep13、ep14、ep20（点了 Create 库里没有，未扣点），v2 任务已排队。⛔ **Suno 下载额度用完**：账号页「Out of Downloads」，Pro 月度下载 0，**11/25/26 刷新**（Song credits 还剩 2370）。服务已暂停新任务（`automation-paused.json`），等用户决定买下载额度还是等刷新；渲染用 `python -m rank_scroll render <ep> --music a.mp3 b.mp3`。
- 🟡 **ep11–ep20 十期（follow-up 015 等，2026-11-04 用户授权整夜自主推进）**：按 YouTube 同题实测需求选题（`0_research/data/yt_demand_2026-11-03.jsonl`），每期一个并行代理做完数据、两步找图（先抓内容再找图；可商用优先、全网补、实在没有才 Codex 出图，卡上自动标黄色 AI IMAGE）、渲染与 `publish.md`；每期至少一轮独立审片加一轮独立复核（`qc.md` 文首），blocker 已清零。**推荐发布默认版**（`render/<期>_master.mp4`），风险版（`_with-risk-images`）含许可不明或 FoP 风险图，未签字前不发；过时的风险版移到 `render/_stale/`，加配乐前的静音版备份在 `render/_silent/`。
  | 期 | 题目 | N / 冠军 | 时长 | 配乐 | 默认版图片 | 主要待定 |
  |---|---|---|---|---|---|---|
  | ep11 | Biggest Ships（GT，按船级） | 42 / Pioneering Spirit | 6:03 | ✅（v3 两首，A-B-A） | 实拍 + 6 AI | 风险版 5 张签字 |
  | ep12 | Largest Countries by Area | 50 / Russia | 6:23 | ✅ | 49 实拍 + 1 AI | 法国本土口径、西撒哈拉、克什米尔 |
  | ep13 | Tallest Statues（本体高度） | 41 / Statue of Unity | 4:38 | ✅（v3 两首） | 实拍 + 9 AI + 9 占位（雕塑 FoP / 许可） | 9 张占位与俄乌塞等 FoP 逐项签字 |
  | ep14 | Highest Volcanoes（GVP Holocene） | 50 / Ojos del Salado | 6:20 | ✅（v2 两首，A-B-A；默认版） | 实拍约 19 + 31 AI | AI 图比例、Holocene 口径 |
  | ep15 | Deepest Lakes（>400 m） | 35 / Baikal | 4:43 | ✅ | 实拍 + 10 AI | 风险版 7 张签字 |
  | ep16 | Largest Stadiums（座位数） | 50（47 名次）/ Narendra Modi | 6:23 | ✅（v4 两首长曲，172 s ×2 接链；待人耳试听） | 41 实拍 + 6 AI + 3 FoP 占位 | FoP 国家放不放、Beaver 取值 |
  | ep17 | Longest Rivers（Britannica，国旗=入海国） | 50 / Nile | 6:23 | ✅ | 实拍 + 8 AI | 离群值例外规则 |
  | ep18 | Fastest Production Cars（>350 km/h） | 30 / Yangwang U9 Xtreme | 4:39 | ✅ | 实拍 + 1 AI（3 张为相近版本并已注明） | 入榜线、单向取值 |
  | ep19 | Most Visited Countries（UN Tourism 2024） | 50 / France | 6:15 | ✅ | 50 可商用实拍 | 英国 38.2M 口径、中国缺数据 |
  | ep20 | Tallest Waterfalls（总落差） | 35 / Angel Falls | 4:02 | ✅（v2 两首） | 10 实拍 + 25 AI | Angel 979 vs 807 m、AI 图比例 |

  配乐用另一会话下好的 Suno 两首，经 `episodes/ep04_largest_land_animals/_build/add_music.py` 只换音轨（-16 LUFS，片尾淡出，帧数不变）。ep11 / ep13 / ep14 / ep20 在 2026-11-04 账号升级额度后补齐（Suno 任务 87691a72 / 2f127467 / 8b54e2a2 / f90acccf），同法只换音轨，原静音版在 `render/_silent/`。各期 `publish.md` 描述框已补 Suno 配乐署名、清单已补「不登记 Content ID」一条（ep12、ep14–ep20 同补）。上传 AI 图的期一律勾选合成内容声明（各期 `publish.md` 已写）。
- 🟡 ep21 世界各种大米 30 种（列表期，不排名；follow-up 055/056/057/059/060）：用户 2026-11-06 定 poster 版式、卡片只拍米本身，第 1 轮独立审片（`qc.md`，1 blocker / 5 major）后改版：大字统一粒长四档（USDA 口径）、副字口感、标签颜色香气，未核实说法已换（见 `sources.md` 文末），Basmati / 野米双旗（`_assets/flags/in-pk.png`、`us-ca.png`），计分板按大洲。配图 30/30 Codex 写实 AI 图（`_build/gen_ai.py`），`tile_gate` 通过。带 Suno 配乐（job 112eccdb）的英文母版 `render/ep21_rice_varieties_master.mp4` 与中文母版 `render/ep21_rice_varieties_master_zh.mp4`（约 4:09），封面 `render/thumbnail{,_zh}.png`（`_build/make_thumb.py`），发布稿 `publish.md`（再跑 `_build/finish_publish.py`）/ `publish.zh.md`（文案覆盖 `zh_publish.json`）。待：第 2 轮独立复核、Ofada 主出处替换（研究稿 §5）。
- ⬜ 上传（follow-up 053）：`_tools/upload.py youtube <期>` 经 YouTube API 传成**私享**（标题、描述、标签、合成内容声明、封面取自 `publish.md` 与 `release/<期>/`），用户在 Studio 检查后亲手公开，再 `upload.py comments <期>` 发评论、手动置顶；`upload.py douyin <期>` 在本机 Chrome 自动填抖音发布页，「发布」由用户亲手点。AI 声明与实际要发的版本对不上时拒传；记录在各期 `uploads.json`，`upload.py status` 看总览。`upload.py tiktok <期>` / `upload.py tiktok-all` 在独立 Chrome 配置里自动填 TikTok Studio（英文版成片、说明与话题、封面、AI 生成内容标识；说明优先用 `publish.md` 的「## TikTok」节，没有就自动拼），「Post」由用户亲手点（TikTok 网页版没有存草稿；`--rehearse` 只演练不发布，follow-up 066）。首次需 `python tools/youtube_upload.py auth`、`python tools/douyin_upload.py login`、`python tools/tiktok_upload.py login`。其余平台照 `publish.zh.md` 手动。

## 发布前待用户决定

| # | 事项 | 代理默认（可改） |
|---|---|---|
| 1 | ep01 五张全景自由（FoP）风险图（Burj Khalifa、23 Marina、Al Hamra、Iconic Tower、Landmark 81：所在国无商用全景自由） | **默认母版不放**（占位卡写「Photo withheld: architecture copyright」）；另渲了 `_master_with-risk-images.mp4` 供对比（选它就用 `python -m rank_scroll publish <ep> --allow-risk-images` 重新生成 publish.md，补 5 条署名）。注意 Burj Khalifa 那张本身是逆光远景、辨认度低（审片 major），要放最好先换一张更清楚的 |
| 2 | ep01 未完工楼（重庆陆海国际中心 458 m、山东 IFC 428 m 为 CTBUH「封顶未完工」）不收 | 按 CTBUH 口径不收；发布前 7 天复核 |
| 3 | ep02 台湾单列、印度最高点取干城章嘉峰（洞察卡说明「按实际管辖」）、阿富汗国旗用 flagcdn 版本 | 保留 |
| 4 | 置顶评论约 100 个链接可能被 YouTube 判为垃圾评论 | 先发一条试；不行改为只放作者 + 许可名、链接放描述框外的页面 |
| 5 | Vision 措辞 | 见文首 |
| 6 | ep06 30 张漫画封面均为版权作品 | 代理默认以带图版为主片（follow-up 014/019），默认版全部占位；发布前由用户定 |
| 7 | ep06 21/30 条发行量超过 bible §3.3 的 18 个月 | 按「累计只增不减、旧值是下限」例外收录，卡上标首次公布年份 |
| 8 | ep06 Crayon Shin-chan（1.48 亿含约 2000 万非漫画书）剔除 | 剔除；如收录约排第 13（海外 7000 万是否为漫画未核实） |
| 9 | ep04 爪哇犀（#7，WWF Italia / Stephen Belcher）、野牦牛（#11，Coke Smith）两张野外照许可未知 | 默认母版用博物馆标本图（可商用）；选风险版须先取得授权或签字，再 `publish --allow-risk-images` |
| 10 | ep04 非洲森林象取 2,000 kg（Larramendi 2016，卡上标「Estimate: none weighed」） | 保留；若改取 4,500 kg 它会升到第 3–4 名 |

## 已定（用户 2026-11-03，follow-up 001）

| # | 决定 | 结论 |
|---|---|---|
| 1 | 试播选题 | **ep01 世界最高建筑 Top 50**、**ep02 各国最高峰 Top 50**（每国取最高点，按海拔排序；follow-up 002） |
| 2 | 画面语言 / 观众 | **英文，面向全球** |
| 3 | 音乐 | **Suno**（本机服务，每期独有一首；调用前先写 `request_log.md`） |
| 4 | 旁白 | **试播先不加** |
| 5 | 滚动方向 | **卡片向左平移，读序从左到右，冠军最后出场**（和参考片一致） |
| 6 | 渲染器 | **Python + skia + ffmpeg 自建**（开发项目 `projects/rank_scroll/`） |
| 7 | 频道 | **用已有频道**（频道名、近期上传构成待补，影响片尾推荐和题材轮换） |

Vision 仍待用户确认。

## 审片链接

- 系列总览：<http://127.0.0.1:5174/rank-preview?path=ai_videos%2Fpaihangbang>（每期一卡，点进单期看成片、审片结论、卡片明细、洞察、发布稿与交接）
- 单期：`http://127.0.0.1:5174/rank-preview?path=ai_videos%2Fpaihangbang%2Fepisodes%2F<期目录>`
- ep03 AI 公司（列表期）：<http://127.0.0.1:5174/rank-preview?path=ai_videos%2Fpaihangbang%2Fepisodes%2Fep03_ai_companies>
