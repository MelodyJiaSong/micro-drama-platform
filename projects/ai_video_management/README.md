# ai_video_management

地图资产页新增原版通行研究（follow-up 308）：同一站点内，整图与全部区域可同步切换原图/数据重建的禁行、树木、高差边界、坡道候选和待核占地图层；点击两点检查带余量的直线路段，提供带图例下载及区域视频约束。数据源为 `map_regions.json.navigation`，不把未配准电影图当碰撞地图；独立审查未通过的出图只作返工对照。当前实机寻路、动态单位碰撞与电影图配准未验证。

工作流维护与跨 session 接续：先读 [AI Video 全局工作流与覆盖边界](../../.agents/references/project/ai_video_workflow.md)。全局 UI 按 AI Video / Kimi Code 分类；三大模块各自导航，源编号稳定。`/workflow/settings/coverage` 同时核对当前目录的可读性、编号、共用文档现存引用和已保存 run 的全局来源。修改制作指南、设置、模板或默认值时同步共用目录，刷新核对并运行 `tests/test_global_workflow.py`；当前只读 UI，编辑对应原文件。局部剧输入与历史快照继续在既有导航，隐藏运行上下文不作为已覆盖声明。

Legacy BGM 功能已移除：公共音乐库、旧 cue 时间线、生成/导入/分配/混音 UI 和 API 均不再提供，启动不创建 `_bgm`。新的配乐流程另行设计，历史规格保留为已停用记录。

旧 0–7 阶段流程的管理功能已整体移除（follow-up 233，clean start）：评测中心、编剧室/人物访谈、按块编辑 prompt 与 AI 改写建议、旧 shot / shotlist / Seedream / 选角 / 演员 / 声音 / 演技库视图、抽帧 / 方位背景板 / 末帧承接、人物卡烧录、定版 / 拼接 / 字幕与接缝评分、导出 production、Previz 渲染、小说下载与小说目录浏览、项目类型徽章，以及只服务这些功能的 API、依赖注入、测试和样式；`projects/ai_video_eval` 一并删除（需求记录移到 `specs/development/ai_video_eval/`）。旧剧产物与 `_actors` / `_performances` 等数据原样保留，由 `OBSOLETE.md` 标记，侧栏、剧页与首页显示「已过时」（见下文「已过时标记」）。启动不再创建 `_actors` / `_voices`。

Prompt编译器v3固定保留本镜指定对白、自然环境声和动作声，明确禁止背景音乐/配乐；无对白镜追加没有人说话。约束位于key后的声音行及末尾；旧编译版本显示待更新，既有故事/分镜不被改写。实际音轨仍须出片试听确认。

三模块剧采用 episode → scene → shot；可复用环境资产为 `background/`（其他既有剧兼容资产 `scenes/`）。分镜与编译产物按 `content.scenes[].shots[]` 组织，场内短编号为 `s1` / `st1`，完整镜头 key 为 `ep1_s1_st1`。Prompt 第一行、导航与下载导入共用该 key，生成素材落在 `episodes/ep01/scenes/s1/shots/st1/renders/`。调序保持编号。网页下载的条在剧页点「📥 导入」按完整 key 归位到该镜头的 `renders/<条>/`。UI 按集、场、镜只读展示，创作与编译通过 agent 完成。


侧栏文件树按需加载（follow-up 280）：页面先取 `/api/tree?lazy=1`（导航骨架加前几层，更深的文件夹是 `lazy` 占位），点开、打开深处文件、角色画廊、回收站时再取 `/api/tree/subtree`；不带 `lazy` 的 `/api/tree` 仍返回整棵树。文件变化自动推到页面：后台一个 watchfiles 线程看着 `ai_videos/`，`/api/events`（SSE）推送变化的路径，侧栏、剧页、剪辑页、阅读器只重取被改到的部分，不用手动刷新；剧页静默重取，正在放的视频不中断。

人物卡「样片与正片」（follow-up 286）：在资产库点开一个有技能视频的人物（角色画廊「📄 详情页」），人物卡正文上方有三个标签——**正片**（人物视频＋每个技能最新的正式条，按 Q W E R）、**样片**（每个技能全部草稿，新的在前，附峰值图）、**剪辑拼接**（人物目录 `demo/edit/` 的剪辑排在前面——没有分集的剧把英雄 demo 放这里，follow-up 288——再接用到这个人物素材的集级草稿剪辑 / 正片剪辑，带 cut json 的 note）；数据来自 `GET /api/character-reel`，只读。

Demo 定版标记（follow-up 315）：`GET /api/demo-status` 列出 demo 已定版的人物——人物目录 `demo/edit/final/cut_v*.json` 的 `status` 以「定版」/「锁片」开头取最高版本——以及定版成片、之后未定的剪辑和 `demo/publish.md` 是否写的就是定版成片（ok / stale / missing）。侧栏人物目录、角色画廊、资产总览（格子、预览标题，「✓ Demo 定版」按钮只看定版英雄，`?demo=final`）、英雄预览（标题与 Demo 区，定版成片放第一位）和人物卡「剪辑拼接」里的定版 cut 都打绿色「✓ 定版」标记；发布文案没对上时标记变黄并写「文案待补」，悬停看详情。文件变化自动刷新，只读。

排行榜预览页（follow-up 317 / 320）：`/rank-preview?path=ai_videos/paihangbang` 是系列总览（每期一卡：期号、标题、N、冠军、时长、封面、审片结论、配乐、图片统计，ep11–ep20 置前），`?path=ai_videos/paihangbang/episodes/<期>` 是单期审片页（成片 tab 默认打开「推荐审看」、概况、qc.md 最新结论、交接、卡片网格与明细表、洞察、发布稿）。数据来自只读 `GET /api/rank-preview?path=`（只接受系列根或其下一期目录），视频与图片经 `/api/media`；文件缺失显示「尚未生成」。列表期（data.json `"mode": "list"`，如 ep03）不出冠军，概况写「列表期 · 按成立年份，不排名」与首个 / 末个，明细表名次列改「序」；明细表按字段补 corner、logo（`logo_bg` 底色）、创始人头像与姓名身份（头像风险标红）、主图 `image_risk` 原文（通讯社图红底）、`image_alt_credit`（AI-generated 标黄）、`secondary_display`、可展开 notes，没有这些字段的期不出空列（follow-up 321）。

资产总览（follow-up 293）：侧栏点剧下的「1_资产库」（follow-up 294，点箭头只展开）或剧页「🗂 资产总览」进 `/assets?drama=`，人物、背景、道具各一节，按分组（近卫 / 天灾 / 中立）每个资产一格，可按键或名字过滤；点一格打开预览（大图、该目录全部图片与视频、卡开头的键与状态、人物技能的正片或峰值图），← / → 切换、Esc 关闭；数据来自 `GET /api/asset-overview`，只读。

商店货单（follow-up 316）：剧的 `2_世界观人设/props/shop_items.json`（人读版 `shop_items.md`）存在时，资产总览抬头、地图资产页抬头出现「🛒 商店货单」，地图区域里是出售方的资产（`bg22` 奇迹古树、`m300` 武器商人…）另有「🛒 货单」直达。`/shop-items?drama=` 左边出售方（建筑商店、商人 NPC、Roshan 掉落：键、中文名、类型、所在位置、件数），右边该出售方的物品格（缩略图、中英文名、价格、合成路线）；点物品看类别、价格、合成路线、道具卡与「哪些出售方卖它」，点出售方跳过去；`?seller=` / `?item=` 可分享，搜索框跨全部出售方找物品。数据来自 `GET /api/shop-items?drama=`：路径换成仓库相对，跑出剧目录或文件不在的置空串，图片走 `/api/media`；「谁卖它」按各出售方货单现算（不读顶层 `items` 反查表）。剧没有货单返回空 `source`，JSON 坏了在 `error` 里说明；只读，文件变化自动刷新。测试：`tests/test_shop_items.py`、`apps/ui/test/shop-items.test.tsx`。

单集预览页（follow-up 326）：`/episode-preview?path=ai_videos/<剧>/episodes/epNN`，三模块剧剧页工作台抬头「单集预览」直达。一页看完一集：整集成片（集级正片剪辑最新版，时间线按镜分段、点段跳转、播放时下方显示当前镜台词与外语释义）或逐镜连播原始正式条；人物定妆；每场一张卡（场次标题与一句话、本场最新正片剪辑、逐镜缩略图、台词、审片结论与备注、剪辑入出点与理由）；页尾说明。数据只读：`filming.json`、各镜 `renders/` 的条（优先本场剪辑用到的那条）与 `review.md` 的「状态：」、`/api/scene-cuts`，以及可选的 `{集}/preview.json`（title、tagline、scenes、glosses 外语台词释义、cast、shots 逐镜结论、notes）；视频滚到附近才加载。镜组里的镜头（follow-up 327）找 `groups/gN/renders` 的条，缩略图与逐镜连播从这一镜在镜组条里的起点放（本场剪辑写了入点就用入点），同一条镜组视频连着放。成片模式（follow-up 328）：集目录名可带后缀（`ep01_largest_land_animals`）；没有 `filming.json` 但 `preview.json` 有 `video` 时，页面改为审成片——章节按钮、按 `items`（t、end、title、subtitle、badge、note、flag、image）分段的时间线与卡片、`marks` 叠加物标记、`images` 封面候选、`links` 文档链接、`notes` 待拍板与说明（组件 `EpisodeFilmPreview.tsx`；真实尺度由 `ai_videos/zhenshi_chidu/_tools/make_preview.py` 生成）。测试：`apps/ui/test/episode-preview.test.tsx`。

教学视频台词审（用户 2026-11-08）：审查单索引与审查单页也读 `edu_videos/<系列>/<知识点>/reviews/<轮>/checklist.json`（`tools/edu_review.py` 写，与短剧 v5 双审单同形），问题清单页读同目录 `issues.json`。测试：`tests/test_review_run_api.py`。
教学视频预览（follow-up 339）：网页可访问的顶层目录在 `libs/common/exposed_roots.py` 统一定义，现为 `ai_videos/` 与 `edu_videos/`（只读审片用）。单集预览页成片模式接受知识点路径 `/episode-preview?path=edu_videos/<系列>/tNN_<主题>`，页眉显示「教学视频 · 系列 · 知识点」；`preview.json`（章节 = 画面段、每句一段带缩略图、讲稿 / 时间轴 / 字幕链接）由 `python tools/edu_video.py preview <知识点目录>` 生成。文件变化推送仍只覆盖 `ai_videos/`；侧栏另有「教学视频」一节（follow-up 357）：每个系列一个节点（名字取 README 的 H1），系列有 `课程表.md` 时点系列名打开课程表，下面按 `### 第 N 季` 标题和 `| 季-集 | tNN |` 表格行列出各季各期——有知识点目录的期显示 ✅（`final/*.mp4` 在）或「制作中」，点开进单集预览、展开看讲稿等 `.md` / `.json`；还没目录的期标「规划」，点开课程表；不在课程表里的知识点归到「未排进课程表」。没有课程表的系列直接列知识点目录。季与期是虚拟节点（路径 `<系列>/syllabus/…`），不懒加载（`tree__reader._edu_videos_section`，测试 `tests/test_tree_edu_videos.py`）。审阅页 `/character-review` 同样接受 `edu_videos/` 下带 `review.json` 的目录（follow-up 344，如配音选型 `edu_videos/_shared/voice_lab`）。测试：`tests/test_sandbox_ai_videos_only.py`、`apps/ui/test/episode-preview.test.tsx`。

剧页故事板（follow-up 336）：三模块剧剧页抬头「故事板」（即「影视改编」不选镜头时；侧栏点场次只看该场）给出片前最后一轮人工审阅。每场一节，按 `filming.json` 的场次顺序（即故事顺序）：场次、地点、时间、一行本场目的、总秒数、镜数，以及该场最新一张出片前审查单（`stage=pregen` 且 `scenes` 含本场）的状态签，如「出片前审查 第 3/3 轮 · 进行中（4/8）」，点开进审查单；没有就是「未审」。下面每镜一张卡（宽屏每行 3–4 张）：16:9 首帧图（点开放大）、镜头、时长、人物键、整句台词（说话人与表演提示分开）、三行行动摘要，「展开」看行动 / 走位 / 动作分拍 / 拍摄全文，以及资料包 `prompt.txt`、`planning/`（首帧图所在目录）与首帧 prompt 链接。图只取各镜现行首帧 `scenes/sN/shots/stN/planning/stN_first_frame.png`，由 `/api/episode-workflow` 的 `first_frames`（路径、毫秒修改时间、首帧 prompt）给出，URL 以修改时间为版本号，重画后刷新或文件变化推送即换新图；`planning/_r1`、`_v2_old` 等旧版和 `_obsolete/` 下的旧镜组板、旧场故事板一律不显示，没出的显示「首帧待出」。原先剧页嵌的是 `board/scene_board.json` 的切图（来自旧镜组板，且图片 URL 不随文件变化，浏览器会一直用缓存的旧图），已撤下；`/scene-preview` 单独页仍在，现以 `scene_board.json` 的修改时间破缓存，由 `python tools/scene_board.py <集目录>` 从首帧重建。测试：`apps/ui/test/episode-storyboard.test.tsx`、`tests/test_episode_workflow.py`、`tests/test_review_run_api.py`。

统一故事板入口（follow-up 364）：所有三模块剧在左导航剧名下显示「故事板（按集）」→ EP，进入该剧集 filming 模块的整集故事板；教学视频每期存在 `storyboard/storyboard.json` 时，在该期下显示「故事板」，进入 `/storyboard-preview?path=edu_videos/<系列>/<知识点>`。教学页与短剧页复用同一 `ShotCard` 镜头卡；没有故事板文件的规划期不显示空入口。测试：`tests/test_tree_display_name_zh.py`、`tests/test_tree_edu_videos.py`、`apps/ui/test/audio-storyboard-preview.test.tsx`。

人物审阅页（follow-up 329）：`/character-review?path=ai_videos/<剧>/2_世界观人设/characters/<人物目录>`，读人物目录的 `review.json`（由 `python tools/character_review.py <人物目录>` 生成：建立视频 V、声样 A、三视图 T、表情 E（按 `expressions/_index.json`）、换装阶段 O），每项一个编号、状态（待审 / 通过 / 要修）与备注，用户按编号说哪项要修；重跑生成器保留同文件的状态与备注，文件变了清回待审。只读，文件变化自动刷新。测试：`apps/ui/test/character-review.test.ts`。

付费服务审计：侧栏「请求日志」或 `/request-logs`，按集/人物/场景等范围查看完整请求、结果与错误。日志由调用适配器在发送请求前追加，普通编辑器不能覆盖。四个服务的实际入口、手工调用方式与覆盖边界见 [paid_services.md](../../.agents/references/project/paid_services.md)。

人物固定武器（dota_yingxiong follow-up 075）：人物卡可声明 `武器参考: p编号`；镜头资料读取自动把出场人物的固定武器加入道具参考，换装阶段继承主体卡，已显式引用的不重复。缺武器图阻止编译；生产工具同步时会将漏挂固定武器的旧资料包标为失效。声明与生成顺序见共用资产指南。

## Layout (follow-up 039 — 2026-05-13)

Follows the `apps/+libs/` layout from `.agents/references/project/development.md` §1–6:

```
ai_video_management/
├── apps/
│   ├── api/        # FastAPI executable (main.py, container.py, routes.py, asgi.py, static/)
│   └── ui/         # React SPA (was frontend/)
├── libs/
│   ├── common/     # env_loader, repo_root, safe_resolve, exposed_tree, drama_layout, episode_workflow, …
│   ├── domain/     # (v1 empty; populated incrementally as splits refine)
│   ├── infrastructure/  # __reader/__writer/__middleware/__importer/__extractor/__archiver/__renamer files
│   └── application/     # (v1 empty; per-endpoint Query/Command split is a planned follow-up)
├── tests/
├── Makefile
├── pyproject.toml  # canonical deps (includes dependency-injector)
└── requirements.txt
```

DI wiring: `apps/api/container.py` declares the `Container` with singletons for ExposedTree, SafeResolver, FileReader/Writer, TreeReader, MediaRenamer, MediaArchiver, DownloadsImporter (+ scene / prop / equipment key routers), CharacterViewExtractor, CharacterReader, ResearchReader/Writer, RequestLogReader, EpisodeWorkflowReader/Writer, ShotMaterialsReader, CharacterReelReader, ShopItemsReader and GlobalWorkflowReader. Route handlers live in `apps/api/routes/{aggregate}__route.py`, decorated with `@inject` + `Depends(Provide[Container.x])`. `main.py` overrides `repo_root_path`/`bound_origin` and wires the routes package.

Read-only browser for the artifacts under `ai_videos/` — the six-module episode workflow (story / filming / compiled prompts per scene and shot, with each shot's 资料包 and 生成记录 — drafts carry 通过 / 不通过 buttons that gate the 720p final, follow-up 265 — plus a 审片串联 that stitches every shot's latest take into one chaptered review video — follow-up 260 — and the 剪辑 module page, which plays each scene's cuts by version with their timelines, keeping 草稿剪辑 (from drafts) apart from 正片剪辑 (from final takes) — follow-up 269 — plus a 整集 entry that plays the scenes joined with their transitions, the independent review bound to that render, and the 转场样片 with a clickable index — follow-up 278), the asset library (characters, background, props, equipment), Markdown / JSON / media previews, the Downloads import, character three-view extraction, the request logs and the topic research workspace. Edits are made by Kimi Code on the files themselves.

Production artifacts remain under `ai_videos/`. The Workflow UI additionally reads registered shared rules and safe configuration declarations from the canonical catalog; these are read-only, with credentials and private memory excluded. Project/run inputs retain their existing scope.

## Run

On Windows, from the repository root run `./start.ps1`. It stops any previous
backend / frontend (its recorded PIDs plus whatever listens on 8766 / 5174),
then starts the backend and the Vite dev server in the background using the
project virtual environment (no `make` or global `python` needed). Logs go to
`logs/backend.*.log` and `logs/frontend.*.log`; open `http://127.0.0.1:5174/`.
Flags: `-NoReload`, `-BackendOnly` (serve the built bundle on 8766), `-Stop`,
`-Port 8767` (backend port; the Vite proxy follows it via `BACKEND_PORT`).

The webapp supports three runtime modes. All bind IPv4 loopback only (`127.0.0.1`) — never `0.0.0.0`.

### Production single-process — `make run-prod`

Builds the frontend bundle into `apps/api/static/` and serves SPA + API from one FastAPI process.

```
make build-frontend
make run-prod
```

Open `http://127.0.0.1:8766/`.

### Backend-only alias — `make run`

Alias for `make run-backend`. Expects a previously built bundle in `apps/api/static/` (or treat as API-only).

### Backend + frontend separately (dev) — two terminals

Terminal 1 (backend on `127.0.0.1:8766`):

```
make run-backend
```

Terminal 2 (Vite dev server on `127.0.0.1:5174`):

```
make run-frontend
```

Open `http://127.0.0.1:5174/`. The Vite proxy forwards `/api/*` to the backend (`http://127.0.0.1:${BACKEND_PORT:-8766}`) and rewrites the `Origin` of the dev page's **own** requests (`http://127.0.0.1:<dev port>` / `http://localhost:<dev port>`) to the backend's, so the backend's Origin/Host gate sees a same-shape request in both runtime modes. Any other Origin is forwarded unchanged and refused, so the dev server is not a relay around the gate (`apps/ui/devProxyOrigin.ts`, follow-up 239). The config is `apps/ui/vite.config.ts` only: a compiled `vite.config.js` next to it would take precedence for `vite` / `vite build` and silently drop both the rewrite rule and `BACKEND_PORT`.

## Test

| Target | What it runs |
|---|---|
| `make test-backend` | `pytest` over `tests/`: boot-smoke (incl. the removed old-pipeline endpoints stay 404), tree walk / labels / `OBSOLETE.md` marker (`test_tree_obsolete.py`), episode workflow + compiler, global workflow catalog, Downloads import (shot keys, bg / p / e / c keys, series-shared assets), media archive / purge, character-view path guard, shop items (`test_shop_items.py`), request logs, research, Origin/Host gate on every write endpoint (`test_api_write_origin_guard.py`) and header shapes, runtime port, SPA deep links. |
| `make test-frontend` | Vitest: episode scenes, drama page + 「已过时」badge (`drama-page-obsolete.test.tsx`), global workflow, glossary, workflow map, request logs, research views / API / text, shop items (`shop-items.test.tsx`), sibling white models, dev-proxy Origin rewrite (`dev-proxy-origin.test.ts`). |
| `make e2e` | Playwright: home page, Origin gate, sandbox 404 (`golden_path`), episode workflow, episode scenes, global workflow, request logs. |
| `make boot-smoke` | Boot-smoke pytest: process starts, `GET /api/tree` returns single-section shape. |

## Install

| Target | What it does |
|---|---|
| `make install` | Runs both install targets below. |
| `make install-backend` | `pip install -r backend/requirements.txt` (pip-only). |
| `make install-frontend` | `npm install` inside `frontend/`. |

## 选题调研模块 (follow-up 161 — 2026-09-06)

`/research`（左侧导航 **📊 调研**，或点树里的 `ai_videos/_research/`）浏览「近半年 YouTube
AIGC 系列排行」——为单人创作者挑可翻拍选题而做的调研。

- **数据面**：`ai_videos/_research/{dataset}.json`，每个数据集一份排好序的 series 列表。
  只读——webapp 不写、也不重算任何指标。
- **指标真实性**：播放量 / 点赞数 / 发布日期全部由 `tools/yt_research.py`（封装 `yt-dlp`）
  实测抓取，不接受搜索摘要或凭印象的估算。点赞率 = `like_count / view_count`。
- **四个视图**（follow-up 162）：**总览**（KPI + 象限散点：对数横轴＝播放中位，纵轴＝点赞率中位，
  两条中位线切四象限，点大小＝翻拍易度，填色＝你标的状态）/ **系列**（六维筛选、五种排序、
  卡内定状态与评分、每卡 10 条样本的播放柱＋赞率点）/ **样本库**（100 条样本的可查询表，
  列排序、播放量背景条、赞率前十分位高亮、页脚实时统计）/ **对比**（最多 4 列的转置矩阵，
  数值行标「最佳」）。点任意系列打开**详情抽屉**（概览 / 翻拍流程 / 实测样本 / 风险与变现 / 我的笔记）。
- **你的决定会被保存**：状态（未定 / 短名单 / 在做 / 已弃）、0–5 星评分、系列笔记、
  样本书签与备注，写在 `ai_videos/_research/{dataset}.workspace.json`——
  **与数据集分文件**，所以重跑调研（重新生成 `{dataset}.json`）不会覆盖你的判断；
  工作区按 slug / video_id 引用，重排名次也仍然对得上。
- **接口**：`GET /api/research/datasets`、`/api/research/dataset/{dataset}`、
  `/api/research/dataset/{dataset}/series/{slug}`、`/api/research/dataset/{dataset}/workspace`；
  写入走 `PUT .../series/{slug}/mark` 与 `PUT .../video/{video_id}/mark`。
- **刷新**：重跑调研即可，例如
  `python tools/yt_research.py search "<query>" --sp views_month --limit 25`（发现）与
  `python tools/yt_research.py meta <id>... --jobs 3`（拿 like_count / upload_date）。

## Architecture

- **Backend.** FastAPI on `127.0.0.1:8766` (IPv4 loopback). Strongly typed Python in `backend/libs/` (`@dataclass(frozen=True)` containers, `str | None` syntax). Single-process mode also serves `apps/api/static/`.
- **Frontend.** React + Vite (TypeScript). Recursive sidebar walks `node.children` uniformly; render-mode dispatch in `Reader.tsx` chooses the media previews (video / image / 3D model / PDF / audio / `.blend` download) or `MarkdownView` / `JsonlView` / `CodeView` (read-only); every parse-on-render component is wrapped in `<ParseFallback>` (real React Error Boundary class). Drama pages (`DramaPage.tsx`) host 📥 导入 / 🎭 角色画廊 and the episode workflow (`EpisodeWorkflowPage.tsx`).
- **API surface.**

  | Area | Endpoints |
  |---|---|
  | Tree / files | `GET /api/tree`, `GET /api/file?path=…`, `PUT /api/file` |
  | Media | `GET /api/media?path=…`; `POST /api/rename-media`, `/api/archive-media`, `/api/unarchive-media`, `/api/delete-media`, `/api/hard-delete-media`, `/api/purge-deleted` |
  | Downloads import | `POST /api/import-from-downloads` `{path: 剧根}` |
  | Characters | `GET /api/character-videos?path=…`; `POST /api/extract-character-views`, `/api/extract-all-character-views` |
  | Episode workflow | `GET` / `POST /api/episode-workflow` |
  | Global workflow | `GET /api/global-workflow`, `/api/global-workflow/source?source_id=…`, `/api/global-workflow/coverage` |
  | Process QC（流程与自检，只读） | `GET /api/process-qc`（仓库级检查 + 各剧体检），`/api/process-qc/drama?drama=…`（剧级明细；剧根经 `drama_ref` 校验） |
  | Request logs | `GET /api/request-logs`, `/api/request-log` |
  | Research | `GET /api/research/datasets`, `/api/research/dataset/{dataset}`, `…/series/{slug}`, `…/workspace`; `PUT …/series/{slug}/mark`, `…/video/{video_id}/mark` |
  | Health | `GET /api/health` |
- **Sandbox (single root).** `ai_videos/**/*.{md,json,jsonl,yaml,yml,txt,png,jpg}`. No other workspace path is reachable.
- **Workspace-root anchor.** `RepoRoot.find()` walks up from CWD looking for a directory containing `ai_videos/` as a child; the parent of that match becomes the workspace root.

### ai_video-specific UX

- **中文 display_name in the sidebar (left nav)**: pinyin/English folder names surface their Chinese name via the tree node's `display_name` (rendered by `Sidebar` as `display_name || name`). `tree__reader._project_zh_title` resolves a **drama** folder's title from its `README.md` H1 (`# 《…》— …` → 《…》; the old `1_立项/concept.md` fallback went with follow-up 233). `tree__reader._sidecar_zh_label` resolves a **scene** folder (`…/scenes/{pinyin}/`) from its `{pinyin}.md` H1 `（中文名）` (`# zhenbei_wangfu_zhengting（镇北王府正厅）` → 镇北王府正厅). Shared extractor `_h1_zh` (《…》 → （…） → text after a `·` separator → whole H1). Scene resolution applies anywhere under a `scenes/` folder (keyed names excepted — see next item), so character folders (already Chinese) aren't mislabeled.
- **scene / props 树按路由键标注 · 导入按键归位（follow-up 173 / 174）**：`scenes/` 与 `props/` 下每个带键的节点，标签＝`{键} {名}`，键就是导入归位用的那一个（`libs/common/scene_key.py`、`libs/common/prop_key.py` 各一处定义）：
  `bg4 闪金镇`（主体）· `bg1-1 谷心_北望修道院`（视图目录）· `p15 两层石木旅店`（物件）· `p15-1 正面.png`（物件视图）· `p3 父亲的旧双手锤`（剧情物件）。带键的名字**只按名字标注、不读 H1**——主体卡 H1 是「广场 · Seedance 主体」、视图卡 H1 是 prompt 标题。区目录本身无键，挂区级主体的键（`scenes/registry.toml` 里 `kind = "zone_whole"` 且 `zone`/`continent` 对得上的那一行，`bg172 艾尔文森林`；解析只在 `scene_registry__reader.py`）；大陆不加前缀。固定标签：`_blender` → **3D 场景**、`assets` → **本场景资产**（每块一个 `b{NN}_…/`，内放 `*.link.json` 指向 `props/p{N}_{名}/`，树按目标渲染：`.md` 可读、`.png` 可看、`.glb` 可转）。区目录的 `_plan/`（`plan.toml` + `apply_report.md`）是工具状态，**树里不显示**。
  **场景物件一律是 prop（follow-up 174）**：旧的区级资产库 `scenes/{大陆}/{区}/_assets/` 与 `bg{Z}-a{NN}` 键已退役，每个物件只住 `props/p{N}_{名}/`（卡 + `asset.toml` + `ref/` + 三视图 + `mesh/p{N}.glb`），编号全剧唯一。`.glb` 是 🧊 叶子（一个 GLB 只装一个物件，只存在于 `props/p{N}_*/mesh/`，`_blender/` 里只有 `.blend` + `check_*.png`）；`.blend` 为**只下载**叶子（`DOWNLOAD_ONLY_EXTENSIONS`：`/api/media` 以 attachment 下发，**不算 media**——导入不扫、重命名不碰）。
  导入（`DownloadsImporter` → `readers/scene_route__reader.py` 的 `SceneKeyRouter` / `readers/prop_route__reader.py` 的 `PropKeyRouter`）取文件名里**最左边**的 scene 键或 prop 键，任意深度都能归位：

  | 最左的键 | 落到 | 文件名 |
  |---|---|---|
  | `bg{N}_{主体}` | 主体目录 | `{主体目录名}.png`（`_` 后须是主体名或其截断，防旧 plate 号误认） |
  | `bg{N}-{M}` | 主体下的 `bg{N}-{M}_…/` 视图目录；没有就主体目录 | `{视图目录名}.png` / `bg{N}-{M}.png` |
  | `p{N}-{i}`（图，场景物件＝有 `asset.toml`） | `props/p{N}_{名}/` | 物件卡对应 ```text 块首行（`p15-2_侧面`），卡里没有就 `-1 正面 / -2 侧面 / -3 背面` |
  | `p{N}-{M}`（图，剧情物件＝无 `asset.toml`） | `props/p{N}_{名}/` | 照旧 `p{N}-{M}.png`（shot `参考:` 引的就是它） |
  | `p{N}…`（`.glb`，任一 prop） | 该 prop 的 `mesh/` | `p{N}.glb`（没有 prop 键的 GLB 一律不导入——不按名字词匹配、不进角色 / 场景 / shot） |

  同号两处 → 不猜、留在 Downloads。键**先于**角色/道具/场景的词匹配出现时，键赢（实测 `bg19_加瑞克的小屋` 被角色 `c18_加瑞克` 抢走）；shot 匹配永远不被覆盖。导入后的重命名一趟**不进** `_blender/ planning/ ref/ mesh/`（`GENERATED_DIR_NAMES`；此前会把 `check_plan.png` 改成 `_blender1.png`、`bg4_floorplan.png` 改成 `planning.png`）。测试：`tests/test_tree_scene_key_labels.py`、`tests/test_downloads_import_scene_keys.py`、`tests/test_downloads_import_prop_keys.py`。
- **装备 equipment · 按 `e{N}` 键标注与归位**：装备住 `2_世界观人设/equipment/`（旧剧平铺在剧根 `equipment/`，`drama_layout.equipment_dir`），结构 `equipment/{槽位}/e{N}_{品质}_{名}/`——槽位（`主手`、`胸`…）与品质词都是各剧配置，**只解析键**。键文法与 prop 同一份（`libs/common/key_grammar.py`，`prop_key.py` / `equipment_key.py` 只各给一个字母；`VIEW_NAMES` 只定义一处）。
  - **分类层 · 按名字找、不按深度**：槽位上面可再套分类（`equipment/{分类}/{槽位}/e{N}_…/`，如 `equipment/板甲/胸/e79_蓝_光铸胸甲/`），分类名也是各剧配置。名字解析得出 `e{N}_…` 的目录就是物件，任何深度都算；`loadouts/`、`_*`、`.*` 不进（判据只在 `drama_layout.is_equipment_tool_dir` 一处）——导入、`_series/` 冲突、树标注共用。
  - **树**：物件目录、卡、视图标 `e12 蓝_维里甘之拳` / `e12-1 正面.png`；分类与槽位目录、`loadouts/`、`equipment.toml` / `registry.toml` / `item.toml` 保持原名，`loadouts/` 与 `_*` / `.*` 目录里的带键名字也不标。
  - **导入**（`readers/equipment_route__reader.py` 的 `EquipmentKeyRouter`）：`e{N}-{M}` 图片落到递归找到的 `e{N}_…/`，文件名取物件卡里以该键开头的 ```text 首行（`e1-2_侧面_锤头朝左`），卡里没有就 `e{N}-{M}_{正面|侧面|背面}`（与 prop 共用 `readers/card_view__reader.py`）。**只按键**：装备目录不进名字词候选，item 名里的词、`.mp4` 都拉不进来；裸 `e{N}`、截断的 `e12-`、视频、找不到或同号两处的 `e{N}` 一律留在 Downloads（不交给 `参考:` 里引到的角色词）；GLB 永不进装备（`e` 键在 prop 键之前的 GLB 视为装备模型、不导入，也不会覆盖那个 prop 的 mesh）。
  - **最左键赢**：文件名里 `bg` / `p` / `e` 键与角色词谁最靠左听谁（prompt 首行先于 `参考:` 行），shot 匹配永不被覆盖。系列成员也查 `_series/equipment/`；同一 `e{N}` 在本集与 `_series/` 各有一个目录 → `series_key_conflict`（同名槽位不算冲突）。测试：`tests/test_equipment_key.py`、`tests/test_downloads_import_equipment_keys.py`、`tests/test_tree_equipment_labels.py`。
- **Downloads 导入 · 系列共享资产 (series-shared import)**: on a series member (`ai_videos/{series}/{ep}`), `DownloadsImporter.import_drama` also collects `characters/` / `scenes/` / `props/` from `ai_videos/{series}/_series/` (flat or `2_世界观人设/` layout; resolved in `libs/common/series_shared.py`). They route exactly like the episode's own assets (`_classify` + `asset_key.view_key_in`, plus the keyed scene-subject and any-prop view fallbacks), so `c2-1_…` lands at `_series/characters/c2_…/c2-1.png`. Series assets live **only** in `_series/`: when an episode folder duplicates a shared one (same routing prefix such as `c1`, or identical folder name), a download that would land in either is **not moved** — it stays in Downloads and `errors` reports `series_key_conflict: {episode folder} <-> {series folder}` (repo-relative). Other keys still import; flat dramas are unaffected. Tests: `tests/test_series_shared_asset_import.py`.
  **`_series/` is an asset owner, not a drama (follow-up 172)**: anything validating an ASSET path asks `drama_ref.asset_root_depth()` — drama root (2 or 3 segments) **or** a series' `_series/` (3) — while anything keyed to an episode keeps asking `drama_ref.drama_depth()`, which answers None for `_series` by design. Mixing the two is what made every character-video button (extract-views / extract-all) return `not_a_character_video` on a series-shared character, while the UI's own `CHARACTER_VIDEO_PATH_RE` happily showed the buttons. Guard: `tests/test_character_video_path_guard.py`.
  **角色文件夹 = `cN_…` 或 `mN_…`（follow-up 180）**：怪物与群众 NPC 卡（`m1_Kobold`）也有 turntable，角色画廊、🖼 提取三视图都认它们；这个判定只在 `libs/common/character_dir.py`（前端 `apps/ui/src/lib/characterDir.ts`）定义一次。Tests: `tests/test_character_video_path_guard.py`.
  **一层分组目录（follow-up 284）**：卡目录可直接在 `characters/` / `props/` 下，也可在一层不带键的分组目录下（`characters/近卫_sentinel/c65_Axe/`）。列卡只走 `libs/common/asset_group.py`（`tools/*.py` 也引用；前端 `lib/dramas.ts` `characterFolders`），分组本身不当资产；不含带键子目录的旧式无键目录照旧当资产。角色画廊按分组分段。Tests: `tests/test_asset_groups.py`、`apps/ui/test/character-groups.test.ts`、`tools/tests/test_asset_groups.py`.
  **命令行同一件事**：`python -m apps.cli.extract_views {repo 相对的 turntable.mp4} [...]` 走同一个 `CharacterVideoCommand.extract_views`（时间点与文件名仍只在 `character_video__valueobject.py`），每条打一行 JSON、有失败退出码 1；仓库工具 `tools/char_assets.py` 用它批量补全剧三视图（szzl follow-up 055）。
- **3D 白模预览 (.glb / .gltf, follow-up 169)**: image-to-3D 交回来的白模在浏览器里直接转着看，不用开 Blender。三处落地：① 树节点类型 `model`（`tree__reader._leaf_for`），侧栏挂 🧊 图标、点开即用 `<model-viewer>` 全幅预览（`Reader` 的 `MODEL_EXTS` 分支，拖动旋转 / 滚轮缩放 / 右键平移）；② `SiblingMedia` 把 `.glb`/`.gltf` 当媒体，同 folder 的网格与 `renders/`、`archive/` 三节里都渲成可转的 tile；③ 新增 **🧊 3D 白模** 一节，把**下一层子目录**里的网格（道具的 `whitemodel/raw.glb`、人物的 `model/model.glb`）提到主体卡片上——`tools/whitemodel_normalize.py` 写在子目录，卡片不提就只能靠翻树找到。子目录只捞网格不捞图（views/ frames/ 的图会淹掉卡片），tile 走 `loading="lazy"`，深色底（白模材质被剥光，浅底上是白对白）。`/api/media` 侧早已就绪：`model/gltf-binary` + `inline`。**注意 `.glb` 不进 git（`.gitignore`）—— 白模只存在于生成它的那台机器上。**
- **图片放大 (ZoomableImage)**: Reader 的图片预览、`SiblingMedia` 图片 tile 点击即打开全屏查看器——滚轮以光标为中心缩放（10%–2000%）、拖动平移、双击在「适应 ↔ 放大」间切换、`+`/`-`/`0` 缩放/复位、Esc 或点空白处关闭；底部工具条有 − / + / 适应 / 1:1 / ✕。组件 `apps/ui/src/components/ZoomableImage.tsx`，纯前端、无新依赖。
- **回收站 (recycle bin / `DeletedView`)**: soft-deletes (mp4 / 图片 Reader 的 🗑 Delete) move files into `ai_videos/_deleted/{原路径}`. The `/deleted` route renders a media-preview grid plus two purge paths: **selected media** (`POST /api/hard-delete-media` per file — media-extension only) and **🧹 清空回收站（全部）** (`POST /api/purge-deleted` — one shot, recursively wipes the **entire** `ai_videos/_deleted/` subtree including `.md` sidecars and empty folders, returns `{purged}` count). Both gated by a typed-`DELETE` confirm modal. The header count reflects **all** files in the bin (not just previewable media), so the per-media purge no longer leaves `.md` sidecars + skeleton folders behind. `ai_videos/_deleted/` is fully gitignored — nothing in the bin is ever tracked. Aggregate: `MediaCommand.purge_deleted` → `MediaArchiver.purge_deleted` (`shutil.rmtree` of `_deleted/`).

## Security model

- Localhost-only, IPv4 (`127.0.0.1`). IPv6 (`[::1]`) and `0.0.0.0` are explicitly out of scope.
- **Every write is gated (follow-up 239).** Any method other than GET / HEAD / OPTIONS — in practice every POST / PUT under `/api/` (file save, episode workflow, rename / archive / unarchive / delete / hard-delete media, purge recycle bin, Downloads import, view extraction, research marks) — must carry a `Host` naming the bound loopback address and the app's own `Origin`. Foreign / `null` / wrong-port Origin or a foreign Host (DNS rebinding) → **403** `origin_blocked` before the handler runs. A write with no `Origin` is refused too (validation/security.md SEC-ORIGIN-HOST-01): browsers attach `Origin` to every non-GET request, and a local script that writes through the API sets the app's own Origin explicitly. Loopback aliases (`localhost` ↔ `127.0.0.1` at the bound port) admit. **Any port other than the bound one (default `8766`) is foreign.** The rule is by method (`libs/common/origin.py: is_guarded`), so a new write endpoint is covered without registration; `tests/test_api_write_origin_guard.py` fails if a write route lacks its foreign/own Origin case. Reads (GET) are not gated.
- File access sandboxed through the `ai_videos/` root. Path traversal probes (`..`, percent-encoded, ADS, Windows reserved names, 8.3 short names, mixed slashes, trailing-backslash per Vite CVE-2025-62522) all collapse to a single **404** (no existence oracle). Symlinks / Windows junctions refused outright.
- Extension allowlist for reads: `.md`, `.json`, `.yaml`, `.yml`, `.jsonl`, `.txt`, `.toml`, `.png`, `.jpg`. SVG NOT allowed (code-execution vector). Image extensions are not writable. **PUT extension-rejected returns 400.** 1 MiB body cap on writes.
- **`If-Unmodified-Since` is REQUIRED on PUT for existing files.** Missing → 400; stale → 409.
- Markdown render path uses `rehype-sanitize` default schema; raw HTML, event handlers, and `javascript:` URIs are stripped.
- CSP header on all responses: `default-src 'self'; img-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'wasm-unsafe-eval'; connect-src 'self'; object-src 'none'; base-uri 'self'`. WebAssembly is permitted for the existing model viewer.

## Light-theme app chrome

App chrome (body, sidebars, toolbars, panels, buttons, form controls) is light-only — `:root { color-scheme: light; }`, no `@media (prefers-color-scheme: dark)` overrides. Dark `<pre>` palettes inside `.markdown-view pre`, `.code-view pre` are intentional carve-outs (validated WCAG AA).

### 角色语义文件名保留（2026-10-03）

普通媒体重命名保留 characters 下的 `{角色}_front/side/back.png`、`{角色}_audio.mp3` 与 `{换装键}_front/side/back.png`，避免新人物约定被改回编号文件。相关回归：`tests/test_asset_routing_key_collision.py`。

### 角色合图文件名保留（2026-10-03）

characters下的`{角色}_views.png`和`{造型键}_views.png`同front/side/back/audio文件名一起保留，普通重命名不得改回编号文件。相关测试：`tests/test_asset_routing_key_collision.py`。

## 三模块创作 POC

**流程与自检（2026-10-26，follow-up 310；源自 dota_yingxiong follow-up 257 / 258）**：「工作流 › 1.0 总览 › 1.0.4 自检与进化（仓库级）」`/workflow/qc` 列仓库级自检登记（`.agents/references/project/qc_checks.toml`，只收有共用依据的检查）与各剧体检汇总（逃逸率、缺陷、出片检查结论数、近 7 天 follow-up 进 changelog / 撞号 / 待补）；剧页「🔍 流程与自检」进 `/qc?drama=…` 剧级页：本剧检查（`ai_videos/{剧}/qc_checks.toml`）与「继承自仓库级」分区显示，含缺陷记录、逃逸分析（为什么检查没抓到 → 进化动作）与最近出片的 `qc.json` 结论。**两层不混**：仓库级蓝、剧级绿；剧级检查只能「复制：提议升仓库级」，仓库级检查只能「复制：复核」，缺陷对应仓库级检查时指令要求先征得同意。页面只读——「管理」＝复制写好的指令给 Kimi Code，由 `tools/qc.py` / `tools/followup.py` 写入（锁与日志不被绕过）。本站不执行仓库工具源码，逃逸四分法在 `libs/common/process_qc.py` 与 `tools/qc.py` 同义，改一处同步另一处。

**审查机制图（2026-11-07，follow-up 330；源自 chuanyue_yiri follow-up 032）**：「1.0.4.1 审查机制（草案）」`/workflow/qc/strategy`（`ReviewStrategyPage` + `ReviewStrategyDiagrams`，数据在 `apps/ui/src/lib/reviewStrategy.ts`）用五张 SVG 图讲全流程怎么审：① 主流程（每关 产物 → 机检 → 独立审稿 → 闸门；绿线过、红虚线不过回上游、★ 必须用户点头、橙色漏网回路，点列看该关细节）；② 依赖图（点节点高亮上游 / 下游，说明改了谁、哪些产物与结论作废）；③ 审稿人泳道（按法则分工，谁在哪几关上岗）；④ 结论判定树（严重度 → 本该哪关抓到 → 处理）；⑤ 漏网案例追踪（面包、硬币、油灯：错误从哪关进来、闯过哪几关、新检查在哪关最早拦下）。顶部实时读 `/api/process-qc` 显示试点剧闸门状态与逃逸率。这是**草案**展示：真正生效的检查仍只以 `qc_checks.toml` 为准，用户确认后再落进登记表并改这里的数据。

**审查单（2026-11-07，follow-up 331 / 332；源自 chuanyue_yiri follow-up 034 / 035）**：审查单存在剧目录 `ai_videos/<剧>/reviews/<集>_<时间>_<阶段>_r<轮>/`。`/review-run?path=<剧目录或集目录>` 按「集 → 一条循环链（第 1–3 轮）」列出全部审查单；`/review-run?path=<审查单目录>` 显示一张单（`ReviewRunPage`，数据是 `tools/review_run.py` 写的 `checklist.json`）：第几轮与上一轮 / 下一轮链接、这轮之前改了什么、进度条、按法则分组的每位审稿人一个勾（已打勾 / 未打勾 / 失败）、每人的必查项 ✓/✗、谁在何时打勾、各严重度条数、报告与任务书链接、补登等备注；顶部按状态写明「审查未完成 / 本轮审完 / 已作废 / 已收轮 / 你已确认出片」（2026-11-08 起不再有「待你确认」），收轮后链到「结果.md」并显示你的确认原话。页面只读，打勾只能由审稿人运行 `review_run.py tick`。入口：剧页「☑ 审查单」、单集工作流页头与单集预览眉栏的「审查单」、审查机制页。工作流导航里机制页是「1.0.5 审查机制与审查单」，编号来自名册源 `.agents/references/project/review_roster.json`。

**审查单分两层 + 左侧导航（2026-11-08，follow-up 333）**：左侧导航顶部有「☑ 审查单」一类，按「剧 → 集 → 每轮审查单」列出（同一条循环链的轮次挨着、新的在前，圆点是状态），数据来自只读接口 `GET /api/review-runs`（`ReviewRunReader` 只扫 `ai_videos/*/reviews/*/checklist.json` 与系列下一层，返回标题、状态、轮次、打勾数和各严重度条数）。点剧或集打开该范围的列表，点一张单打开审查单页。**审查单页只给摘要**：标题、状态、第几轮与上一轮 / 下一轮、总进度和问题总数、闸门说明，然后每个审查大类一行——审了没、各严重度问题数、哪些独立审稿人参与（✓ 已审 / ! 失败 / ○ 未审）。**细节在第二层** `/review-run/item?path=<审查单目录>&item=<审稿人>`（`ReviewItemPage`）：范围、谁何时打勾、备注或失败原因；「怎么审」（查什么、方法、编号必查项与 ✓/✗ 结果、任务书与审稿说明链接）；「审查流程」（六步循环，标出这位审稿人走到哪一步）；「结果细节」（报告全文就地渲染，附原始报告链接）。同一类有多位审稿人时页头可以切换。

**每一步是哪个独立 agent 审的（2026-11-08，follow-up 337）**：数据是 `checklist.json` 每项的 `agents`（`python tools/review_run.py dispatch` 每派一次记一条：`runner` 执行方式、`model`、`context` 独立性、`at`、`prompt` 指令原文文件 `agents/<代号>_<n>.md`、`skills`、`note`，可选 `reply` / `replied_at`），类型 `AgentDispatch` 与 `agentShort` / `tickedAttempt` / `skillPart` 在 `apps/ui/src/lib/reviewRun.ts`。审查单页「谁审的（独立 agent）」列每位审稿人一个标签：第一行状态 + 代号，第二行 agent 简称（「Kimi 子代理 · kimi」，取打勾的那次派单，没打勾取最新一次），重派过的标「↻ 第 N 次派单」，悬停列出全部派单；没登记的旧单写「没有派单记录」。详情页最上面是「审稿 agent」：每次派单一张卡，最新的在前、编号，写执行方式、模型、独立性、派单时间、打勾署名与时间（只在打勾的那次；打勾的那次按 `ticked_by` 前缀对上模型或执行方式）、说明；「用了哪些规则 / skill」逐条列出，名册链到工作流源页，`BRIEF.md` 与任务书链到文件；「发给它的完整指令」读 `<审查单>/<prompt>` 原文放在可折叠块里（最新一次默认展开），原文里的控制字符换成 ␇ 等可见符号并提示（原样放进 `<pre>` 会让 Chrome 卡死）；有 `reply` 就按 Markdown 渲染，否则写「回复未存档，结果见下方报告」。没有派单记录的单显示「没有派单记录」和登记命令。左侧导航只列到每轮审查单，`/api/review-runs` 不加 agent 字段，两页直接读 `checklist.json`。测试：`apps/ui/test/review-run.test.tsx`。

**审查大类页（2026-11-08，follow-up 338）**：审查单页点大类名进 `/review-run/law?path=<审查单目录>&law=<法则>`（`ReviewLawPage`，审稿人标签仍进详情页；详情页眉栏也链回所属大类）。先讲这一类，再给结果，自上而下：「这一类是什么」（名称与 `what`）；「想解决什么问题」（`problem` 与「真实踩过的例子」`examples`）；「细分成几个小类」（「共 N 个小类」，小类＝必查项，表格按本轮各审稿人列出 ✓ / ✗ / —，第 2 轮起多一项 R「复核上一轮」；补登的旧单没有逐项结果，按现行名册列小类）；「检查流程」（分工 `partition`：pairs＝每两场一位、halves＝前后两半各一位、whole＝一位看全部，并列出本轮实际几位、各审哪几场；盲审说明 `blind` / `blind_note`；要查什么 `checks`、怎么查 `how`；交报告逐条写 ✓ / ✗ 并由审稿人自己 tick；一行循环说明，可展开六步）；「用了哪些 skill / 规则」（审查机制 `mechanisms`、照着做的文件：名册法则、`BRIEF.md`、各任务书，指定模型 `prefer_model` 及本轮打勾的 agent 没用上时标红，实际跑的 agent 按「执行方式 · 模型 ×次数（打勾 / 没打勾）」合并，旧单退回打勾署名）；最后「检查结果」（本类各严重度合计、每位审稿人一张卡：范围、状态、打勾 agent、严重度、小类 ✗ 数，点开进详情页；再把各审稿人报告里表头含「严重度」的表合成一张问题表，按重出、可剪、记录、存疑排，列镜头（附原条秒数）/ 严重度 / 子类 / 证据 / 建议改动 / 审稿人，长文字截断可展开；道具状态表等其他表不算，严重度归类与 `tools/review_run.py parse_report` 同一规则）。大类说明的唯一源是 `.agents/references/project/review_roster.json` 的 `laws.<法则>`，页面经 `fetchRepoSource`（`/api/global-workflow/source?source_id=repo:…`，`/api/file` 只开放 `ai_videos/`）实时读取；名册读不到或没有这一类时退回审查单里的 `checks` / `how` 快照并提示。逻辑在 `apps/ui/src/lib/reviewLaw.ts`。测试：`apps/ui/test/review-law.test.tsx`。

**审查单 v5：Kimi 单审 rubric、问题清单与修复循环**：`tools/review_run.py` v5 的每个审稿项默认只有 a 位 Kimi（`runner` / `model` / `status` / `report` / `prompt` / `agents`），打勾后其评分即最终分，不对比、不裁决；全部完成后 `issues` 推出 `issues.json`（编号、级别、类别·维度、镜头、问题、证据、来源、建议、成本、状态、方案与历史）。旧 Claude / Codex 双审单的 slots、scores 与 judge 仍按原格式渲染。页面只读，打勾与方案由 `review_run.py tick / fix` 写。
- **审查单页**：v5 每个大类一行里，每个审稿项一个标签——代号与项状态，下面一行「a ✓ Kimi · kimi」。有 `issues.json` 的单（v2 也算）顶部多一张「问题清单」摘要卡：按级别、按状态的条数、当前循环步骤、挡着下一轮的严重 / 主要条数。
- **问题清单页** `/review-run/issues?path=<审查单目录>`（`ReviewIssuesPage`，可带 `level` / `status` / `category` / `scene` 筛选参数）：顶部循环条「本轮审查 → 问题 → 方案 → 实施 → 下一轮复核」标出当前一步，并写明什么挡着下一轮（严重 / 主要里未处理、已定方案未实施、不改没写理由各几条；规则同 `review_run.py resolved()`）；下面按严重在前的表格，每行编号、级别（严重红、主要橙、待核实蓝、记录灰）、类别·维度（链到大类页与审稿项）、镜头（维度问题没有镜头时显示该项范围）、问题（带 a / b → 最终分）、建议改动、成本（便宜 / 要积分）、状态、选定方案或不改理由；点「证据」展开两位审稿人与裁决人的证据（标出哪位、哪个模型、几分）、来源、问题表原行与历史。
- **大类页**：v5 的「细分成几个小类」换成 rubric 评分表，一维一行，每个审稿项显示「Kimi a 分 / 最终」；旧双审单才显示 a / b / 最终与分歧、抽查、裁决。「检查流程」加名册 `method` 审法步骤与修复循环说明；「检查结果」每项一张审稿卡，并链到问题清单。
- **审稿项详情页**：v5 显示 Kimi 审稿卡（执行方式、模型、打勾署名与时间或失败原因、任务书与报告、派单记录、各维评分与证据）。只有旧双审单才显示「对比与裁决」及双方报告。
逻辑在 `apps/ui/src/lib/reviewV5.ts`，部件在 `apps/ui/src/components/ReviewV5.tsx`、`ReviewIssues.tsx`、`ReviewIssuesPage.tsx`。测试：`apps/ui/test/review-v5.test.tsx`，fixture 是 `review_run.py` 在临时目录里真跑出来的一张完成单（含问题清单与 fix）和一张进行中的单，重生成见 `apps/ui/test/fixtures/review-v5/make_fixtures.py`。

**每轮不等用户 review ＋ 修复页（2026-11-08，follow-up review-corrections-page）**：`review_run.py conclude` 把审查单收成「已收轮」并在 `checklist.json` 记 `verdict`（`result` 可出片 / 不可出片、`text`、`reasons`；默认按未处理的严重问题推）；旧单的「待用户确认」由 `review_run.py migrate`（或 `status`）改成「已收轮」并写 log。页面上「已收轮」是绿色中性状态（`STATE_TEXT` / `stateText` / `displayState` 在 `lib/reviewRun.ts`，旧值也按「已收轮」显示），不再有「待你确认」的字样；只有结论是可出片、又还没有确认原话时，审查单页加一行中性的「出片前需用户在对话里确认（出片工具会检查）」。用户的确认只在出片时：`confirm --quote` 仍在，`can-submit`（`shot_take.py`、`review_gate: required`）要求覆盖该场的最新一张已收轮出片前审查单已确认且材料未变。
- **修复页** `/review-run/corrections?path=<审查单目录>`（`ReviewCorrectionsPage`，逻辑 `lib/reviewCorrections.ts`）：数据是 `python tools/review_run.py corrections <审查单>` 写的 `corrections.json`（同时写 `corrections.md`；重跑幂等，内容不变不改时间）。顶部「本轮审查 → 修复 → 下一轮复核」与链接 ← 本轮审查单、← 问题清单、← 上一轮修复页、→ 下一轮审查单；修复汇总（按级别 / 状态 / 复核结果的条数，点即筛选）；再按场 → 镜一张卡：首帧修复前 / 修复后并排（点开放大；修复前＝`new` 存进 `materials/snapshot/first_frames.json` 的 sha 对上的那张，没有快照的旧单取审查开始时已在的那版，含 `planning/_r1`、`_r1b_old`、`_r3` 等归档；修复后＝下一轮审的那版，没开下一轮就是现行首帧）、这一镜修了哪些问题（编号链问题清单、级别、问题、方案、状态、改了的文件链接、谁何时）与下一轮复核标签（已复核通过 / 复核仍有问题 / 待复核，点开看依据：下一轮同类审稿人问题表里同镜头同子类的行、维度最终分、R 一行），分镜文字逐字段 diff（可折叠，红删绿加；修复前取快照 `filming_<场>.json` 或审查材料 `materials/shots/<场>_<镜>/spec.md`，修复后取下一轮的同一份或现行 `filming.json`）、编译 prompt diff（有快照才有）。可按级别 / 状态 / 复核 / 场筛选。没有 `corrections.json` 时显示「还没生成修复记录」和命令。没有 `issues.json` 的旧 v2 单在内存里由问题表推问题，方案配下一轮 `changes.md` 的「- 法则 · 镜头 · … → …」行。
- 审查单页与问题清单页顶部有醒目的「🛠 修复页」，审查单列表每轮也有「修复页」；左侧导航每轮一行加「修复」小按钮（`/api/review-runs` 多一个 `corrections` 布尔，没生成时按钮变淡）。`fix` 多了 `--file`（可多次）、`--before / --after`（成对）和 `--by`，写进问题的 `files` / `frames` 与历史。测试：`apps/ui/test/review-corrections.test.tsx`（fixture 由 `test/fixtures/review-corrections/make_fixture.py` 用 `review_run.py` 真跑两轮生成）、`apps/ui/test/review-run.test.tsx`、`tools/tests/test_review_run.py`。

**哪张审查单是最新的（2026-11-08，follow-up review-run-latest-badge）**：用户「审查单我看不出来哪个是最新的」。`review_run.py` 的标题已带范围、第几次、轮次和开单时间（「ep01 · 场一 · 出片前（第 2 次） 第 1 轮 · 11-08 15:32」）；页面按**范围**（同一集 + 同一阶段 + 同一组场，`scopeKey`；名字取标题第二段「场一 / 场二到场八 / 全集」，标题不是这个格式时用场号）分组，范围里所有审查链的所有轮按开单时间新的在前（同一秒按目录名），最上面一张是「最新」，其余是「已被 <最新那张标题> 取代」（`scopeGroups` / `episodeScopes` / `latestInScope` / `navLabel` 在 `lib/reviewRun.ts`）。
- 左侧导航：剧 → 集 → 范围（「场一 · 出片前」，点开最新一张）→ 每张一行「11-08 15:32 · 第 1 轮」（时间在前；完整标题、状态与「已被…取代」在悬停提示），最新一张带「最新」徽标，旧的变灰；「修复」按钮照旧。导航宽度有限，常态「已完成 / 已收轮」只用绿点，状态字只给进行中、已作废、已确认出片。
- 审查单列表页 `/review-run?path=<剧或集>`：集 → 范围一节（「场一 · 出片前 4 张」），每张写完整标题、状态、修复页、打勾数和问题数；最新一张带「最新」，旧的变灰并加一行「已被 <链接> 取代」。
- 审查单页：不是本范围最新的，标题上方一条横幅「这不是最新的审查单 → 打开最新：<标题>」；是最新的，标题旁一个「最新」徽标（数据来自 `/api/review-runs`，读不到就都不显示）。
- 审查单页读单改走 `GET /api/review-runs/checklist?path=<审查单目录>`（`ReviewRunReader.checklist`，只认 `ai_videos/<剧>[/<子剧>]/reviews/<单>`，上限 16 MiB，读不到 404）：v5 双审单的 `checklist.json` 会超过 `/api/file` 的 1 MiB 上限（chuanyue_yiri 场二到场八第 2 轮 1.5 MB，原先打不开，列表里也漏掉）。测试：`apps/ui/test/review-run.test.tsx`、`tests/test_review_run_api.py`。

工作流同时集中跨剧设置：三模块指南（故事创作只含总览、故事内容、执行与验证三份源）、Kimi Code 代理与执行设置（含三模块编排入口与工作流目录）、制作、服务与资源（含收费服务、模型默认值、调研与共享资产规则，以及请求审计、调研库入口）。目录唯一源 `.agents/references/project/workflow_catalog.json`，自动发现共用规则、短剧skills及已登记配置；正文不复制。`GET /api/global-workflow`、`/source?source_id=…`、`/coverage`分别提供目录、当前源与历史run来源核对。UI只读显示来源、范围、SHA256；配置隐藏凭据、环境变量值、请求头及启动参数，工具默认值以AST读取，不执行源码。用户配置属当前电脑，不能证明历史有效模型/权限。缺失与未登记来源明确展示；通用文件API的边界不扩展。

全局工作流是普通左侧导航项，可展开故事创作、影视改编、Prompt编译；影视改编按拍摄单位从大到小：「1.2.2 片种」（电影的幕、连续剧的集）、「1.2.3 场」、「1.2.4 覆盖」、「1.2.5 镜头」（子页功能镜头、景别、取景、角度与高度、焦点与景深、运镜；正文在 `.agents/skills/ai-videos-pipeline/modules/filming-*.md`）；原 `/workflow/filming/shot-sizes` 重定向到镜头页（follow-up 213/216）。各层共用导航树的缩进、折叠、键盘操作与选中高亮，深链接自动展开父项，文件树加载失败仍可访问全局内容。入口不绑定剧/EP，UI只读。

工作流页以故事创作、影视改编、Prompt编译替换旧阶段图。魔兽世界左侧保留0_research、1_资产库、2_故事、3_影视改编、4_prompt编译，另有「故事板（按集）」（follow-up 364）；stage可展开，点击其EP1子项进入对应内容，无“EP1 创作”独立入口。集目录从实际文件发现。
每模块一个JSON文件；保存/确定只写当前模块，上游内容指纹变化使下游待更新。编译为固定转换，不调用生成服务。
故事 run 机制（profile、run 历史、选用记录、相关页面与 API、`tools/story_run.py`）已移除（follow-up 206）；故事模块从零重写，EP 导航中故事与其他模块同样每集直达 story.json。
三模块及支持文档只读，修改由 Kimi / Codex 完成，UI仅导航、刷新、复制和下载。`GET/POST /api/episode-workflow`保留读写及版本检查能力；UI没有编辑、保存、确定或编译按钮。

## 决策记录（follow-up 225）

规范见目录 1.0.3（`.agents/skills/ai-videos-pipeline/modules/decisions.md`）。剧内导航：故事创作与影视改编的每集下第一项为「决策记录（本集）」（`episodes/epNN/decisions/{module}.md`），影视改编每场下第一项为「决策记录」（`episodes/epNN/scenes/sN/decisions.md`）；文件存在才显示，用普通 Markdown 阅读器打开。

## 总览（follow-up 219）

导航「1_AI Video」最上面是「1.0 总览」（目录组 `"overview": true`，编号为类别号 .0，不占模块编号）：`/workflow/overview` 工作流全景（React Flow：创作段、后期段两条色带蛇形排布六个模块，卡片列步骤、关卡、产出与状态；中间与下方为支持层；实线交接、红色虚线回路、点线支持供给，可按类型筛选；点选看详情与链接；下方模块一览表），`/workflow/glossary` 术语表；两页共用总览抬头切换。数据源 `.agents/references/project/ai_video_workflow_map.json`，构建时打包。

## 六模块（follow-up 218）

工作流与剧内导航改为六模块：故事创作、影视改编、Prompt 编译与出片、剪辑、声音与音乐、成片交付。后三个为占位（`libs/common/episode_workflow.py` 的 `PLACEHOLDER_STAGES`）：导航列出每集入口，页面显示「待设计」与输入输出，不建集文档、不开放 API 写入。全局目录 1.4–1.6 各有一页占位指南；制作资源与术语表顺延为 1.7、1.8。

## 术语表（follow-up 217）

`/workflow/glossary`（导航「1.0 总览 › 术语表」）展示剧、季、集、幕、段落、场、覆盖、镜头、条、拍点、cue、字幕、资产等术语：**关系图**（`@xyflow/react` 12.11.6，节点按类别着色，连线按关系类型区分实线/虚线并标基数，点选高亮关联、按关系类型筛选、可拖动与缩放）、**时间轴**（一季、EP1 全集与冷开场放大三条，SVG 画出边界不对齐的区间）、**术语列表**（中英定义、搜索）。右栏为选中术语的中英定义、别名、区分与分歧、所在模块、仓库位置、全部关联与来源。数据唯一源 `.agents/references/project/ai_video_glossary.json`，构建时打包；镜头类型与具体转折点只进列表，不进关系图。

## 故事片种（follow-up 211）

故事创作分共用原则（1.1.1）与片种（1.1.2：电影、连续剧）。目录 `formats` 声明片种，源的 `formats` 标明适用片种（缺省=共用）、`adapts` 指向它改写的共用源与小节；`GET /api/global-workflow` 原样返回。共用原则页顶部列出「片种适配」，链接跳到片种页对应标题；导航按目录嵌套即可区分片种，不另加标签或片种切换（follow-up 212）。UI 仍只读。

## 全局设置分类与稳定编号（follow-up 198）

目录增加两类与稳定编号注册表；90份当前全局源已编号。左nav按类别→模块/设置组→源分层，run输入与来源核对展示当前编号；保留路径身份和历史冻结内容，未编号新发现项明确显示待编号。

工作流仅两类设置根：1_AI Video与2_系统与代码（follow-up 216 改名；代码、工具脚本与代理设置都归后者）。AI Video前三个子项为1.1_故事创作、1.2_影视改编、1.3_Prompt编译；其他共用制作/服务/资产规则继续归AI Video，代理配置归另一类。具体源三级编号保存在workflow_catalog.json的source_numbers，以scope:path为身份，不以列表位置计算，不重命名正文文件。标题变化保留编号；组号与源号连续并按编号显示，增删迁移后由 `tools/workflow_catalog.py --fix` 整理（follow-up 203）。自动发现未登记编号的项标待编号并被检查拦截；重复/非法号拒绝读取。run展示当前目录对应编号及名称、来源路径、冻结与当前指纹，不回写历史run或冒充当时已记录编号。三模块与历史source_id深链接继续可用，UI只读。

## 故事内容与执行导航（follow-up 200）

工作流→1_AI Video→1.1_故事创作：已清空，从零重写中（follow-up 206）。

## 已过时标记与剧页入口（follow-up 233）

- **已过时**：`ai_videos/` 下某个文件夹里有 `OBSOLETE.md`，`/api/tree` 就给这个节点加 `obsolete: true` 与 `obsolete_note`（该 `OBSOLETE.md` 的路径）；剧根的上级系列目录有 `OBSOLETE.md` 时，系列下每部剧和 `_series/` 都继承（剧自己的 `OBSOLETE.md` 优先作说明）。实现只在 `libs/infrastructure/readers/tree__reader.py`（`OBSOLETE_MARKER_NAME`、`_obsolete_note`）。侧栏行尾、剧页标题旁、首页剧目列表显示「已过时」（`ObsoleteBadge.tsx`，悬停显示说明路径）；剧页另有「📄 过时说明」打开 `OBSOLETE.md`，向已过时的剧导入前先确认。测试：`tests/test_tree_obsolete.py`、`apps/ui/test/drama-page-obsolete.test.tsx`。
- **剧页入口**：所有剧（含六模块剧）的剧页都有「📥 导入」与「🎭 角色画廊」；六模块剧打开某个模块时两者留在工作页上方，导入后工作页重新读取，新条直接出现在生成记录里。导入只认六模块的完整镜头 key（`ep1_s1_st1` → `episodes/ep01/scenes/s1/shots/st1/renders/<条>/`）与 `bg` / `p` / `e` / `c` 资产键和名字匹配；旧 `shots/shotNN`、`{NN}集{NN}镜`、`bg{N}_{方位}` 方位背景板、人物卡和演员库 / 演技库导入已删除。


系列公用资产（follow-up 295）：左侧“仙侠”是 `ai_videos/xianxia/series.json` 标记的系列；点名称打开公用资产，展开后可放公用资产与具体剧目。`shared_library` 引用原库，`/assets?library=` 使用既有文件/媒体接口展示筛选、预览、验收备注和资料链接。

三面设定图按 `views.panels` 显示实际左右顺序与侧视方向（follow-up 311）；不将南／北／东或西侧视图片固定标成正／侧／背。方向标注正确不代表空间连续性已经验收。

公用资产中文导航（follow-up296）：共享库以 `library.json.navigation` 提供大类 → 小类 → 中文资产名；点分类筛选，点资产预览。建筑/场景通过 `views` 展示正面、侧面、背面三面板图，独立标明生成与审图状态。


地图资产（follow-up 299）：剧 `workflow.json.map_regions` 指向区域清单，侧栏和剧页进入 `/map-regions`；地图标记、大区/区域树、四类机位图、建筑引用、实例坐标与可用状态联动。图片沿用原文件/媒体接口，缺图只显示状态。

地图资产页的泉水区域支持生成俯视图／原版游戏截图的同编号建筑对照，入口参数 `region=S1` 或 `D1`、`focus=buildings`；标注叠加于原图，支持放大、显隐编号与资产卡跳转。

泉水对照支持建筑、商店NPC、出生圈分色筛选（每方3＋8＋5）；原版截图与坐标俯视切换，目标点叠加由原版实例坐标实时计算。图片主体位置由人工观察标注；生成结果存在偏差时明确标为布局待核准，其他旧机位标为旧布局待更新。

机位连续性（follow-up 303）：每张派生机位可记录实际使用的俯视母图路径与SHA256；区域机位上方提供母图入口及切换俯视按钮。母图路径或指纹与当前俯视不一致时提示需要复核。记录证明生成参考来源，画面空间一致性仍须逐图检查。


泉水与大本营连接（follow-up 304）：区域清单可声明 `base_connection`（目标区域、古迹名称、全基地坐标图和说明）。泉水对照上方展示出口方位、可展开的完整基地坐标图及相邻大本营导航。近卫泉水向东北进入世界之树内庭，天灾泉水向西南进入冰封王座广场；俯视母图必须同时包含泉水、内部道路和古迹，其他机位记录这张母图来源。旧全基地图若未与当前连接统一，显示布局待复核。

机位复核记录可绑定当前俯视和当前机位的SHA256：母图局部修订后，保留生成时的真实参考，另显示按当前俯视的复核结论；任一图指纹变化后恢复待复核提示。


泉水五英雄空间（follow-up 305）：原图对照可勾选“五英雄活动空间”，在生成俯视上叠加净空范围及H1–H5活动占位，原版截图保持原样。标注绑定俯视SHA，换图后旧标注隐藏。占位依据画面人物尺度作概念检查，不是碰撞模拟或精确米制测绘。


地图区域原图（follow-up 307）：进入或切换区域默认俯视，大区标题直达第一个区域。每区独立“原图”tab，各生成机位可并排显示原图；`original_reference`记录原图、来源、类型、局部范围与版本限制，图片沿用本地媒体接口。缺专用资料时显示完整原版地图，不生成空链接。
