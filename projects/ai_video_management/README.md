# ai_video_management

工作流维护与跨 session 接续：先读 [AI Video 全局工作流与覆盖边界](../../.agents/references/project/ai_video_workflow.md)。全局 UI 按 AI Video / Claude Code与Codex 分类；三大模块各自导航，源编号稳定。`/workflow/settings/coverage` 同时核对当前目录的可读性、编号、共用文档现存引用和已保存 run 的全局来源。修改制作指南、设置、模板或默认值时同步共用目录，刷新核对并运行 `tests/test_global_workflow.py`；当前只读 UI，编辑对应原文件。局部剧输入与历史快照继续在既有导航，隐藏运行上下文不作为已覆盖声明。

Legacy BGM 功能已移除：公共音乐库、旧 cue 时间线、生成/导入/分配/混音 UI 和 API 均不再提供，启动不创建 `_bgm`。新的配乐流程另行设计，历史规格保留为已停用记录。

旧 0–7 阶段流程的管理功能已整体移除（follow-up 233，clean start）：评测中心、编剧室/人物访谈、按块编辑 prompt 与 AI 改写建议、旧 shot / shotlist / Seedream / 选角 / 演员 / 声音 / 演技库视图、抽帧 / 方位背景板 / 末帧承接、人物卡烧录、定版 / 拼接 / 字幕与接缝评分、导出 production、Previz 渲染、小说下载与小说目录浏览、项目类型徽章，以及只服务这些功能的 API、依赖注入、测试和样式；`projects/ai_video_eval` 一并删除（需求记录移到 `specs/development/ai_video_eval/`）。旧剧产物与 `_actors` / `_performances` 等数据原样保留，由 `OBSOLETE.md` 标记，侧栏、剧页与首页显示「已过时」（见下文「已过时标记」）。启动不再创建 `_actors` / `_voices`。

Prompt编译器v3固定保留本镜指定对白、自然环境声和动作声，明确禁止背景音乐/配乐；无对白镜追加没有人说话。约束位于key后的声音行及末尾；旧编译版本显示待更新，既有故事/分镜不被改写。实际音轨仍须出片试听确认。

三模块剧采用 episode → scene → shot；可复用环境资产为 `background/`（其他既有剧兼容资产 `scenes/`）。分镜与编译产物按 `content.scenes[].shots[]` 组织，场内短编号为 `s1` / `st1`，完整镜头 key 为 `ep1_s1_st1`。Prompt 第一行、导航与下载导入共用该 key，生成素材落在 `episodes/ep01/scenes/s1/shots/st1/renders/`。调序保持编号。网页下载的条在剧页点「📥 导入」按完整 key 归位到该镜头的 `renders/<条>/`。UI 按集、场、镜只读展示，创作与编译通过 agent 完成。


侧栏文件树按需加载（follow-up 280）：页面先取 `/api/tree?lazy=1`（导航骨架加前几层，更深的文件夹是 `lazy` 占位），点开、打开深处文件、角色画廊、回收站时再取 `/api/tree/subtree`；不带 `lazy` 的 `/api/tree` 仍返回整棵树。文件变化自动推到页面：后台一个 watchfiles 线程看着 `ai_videos/`，`/api/events`（SSE）推送变化的路径，侧栏、剧页、剪辑页、阅读器只重取被改到的部分，不用手动刷新；剧页静默重取，正在放的视频不中断。

付费服务审计：侧栏「请求日志」或 `/request-logs`，按集/人物/场景等范围查看完整请求、结果与错误。日志由调用适配器在发送请求前追加，普通编辑器不能覆盖。四个服务的实际入口、手工调用方式与覆盖边界见 [paid_services.md](../../.agents/references/project/paid_services.md)。

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

DI wiring: `apps/api/container.py` declares the `Container` with singletons for ExposedTree, SafeResolver, FileReader/Writer, TreeReader, MediaRenamer, MediaArchiver, DownloadsImporter (+ scene / prop / equipment key routers), CharacterViewExtractor, CharacterReader, ResearchReader/Writer, RequestLogReader, EpisodeWorkflowReader/Writer, ShotMaterialsReader and GlobalWorkflowReader. Route handlers live in `apps/api/routes/{aggregate}__route.py`, decorated with `@inject` + `Depends(Provide[Container.x])`. `main.py` overrides `repo_root_path`/`bound_origin` and wires the routes package.

Read-only browser for the artifacts under `ai_videos/` — the six-module episode workflow (story / filming / compiled prompts per scene and shot, with each shot's 资料包 and 生成记录 — drafts carry 通过 / 不通过 buttons that gate the 720p final, follow-up 265 — plus a 审片串联 that stitches every shot's latest take into one chaptered review video — follow-up 260 — and the 剪辑 module page, which plays each scene's cuts by version with their timelines, keeping 草稿剪辑 (from drafts) apart from 正片剪辑 (from final takes) — follow-up 269 — plus a 整集 entry that plays the scenes joined with their transitions, the independent review bound to that render, and the 转场样片 with a clickable index — follow-up 278), the asset library (characters, background, props, equipment), Markdown / JSON / media previews, the Downloads import, character three-view extraction, the request logs and the topic research workspace. Edits are made by Claude Code / Codex on the files themselves.

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
| `make test-backend` | `pytest` over `tests/`: boot-smoke (incl. the removed old-pipeline endpoints stay 404), tree walk / labels / `OBSOLETE.md` marker (`test_tree_obsolete.py`), episode workflow + compiler, global workflow catalog, Downloads import (shot keys, bg / p / e / c keys, series-shared assets), media archive / purge, character-view path guard, request logs, research, Origin/Host gate on every write endpoint (`test_api_write_origin_guard.py`) and header shapes, runtime port, SPA deep links. |
| `make test-frontend` | Vitest: episode scenes, drama page + 「已过时」badge (`drama-page-obsolete.test.tsx`), global workflow, glossary, workflow map, request logs, research views / API / text, sibling white models, dev-proxy Origin rewrite (`dev-proxy-origin.test.ts`). |
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

工作流同时集中跨剧设置：三模块指南（故事创作只含总览、故事内容、执行与验证三份源）、Claude/Codex代理与执行设置（含三模块编排入口与工作流目录）、制作、服务与资源（含收费服务、模型默认值、调研与共享资产规则，以及请求审计、调研库入口）。目录唯一源 `.agents/references/project/workflow_catalog.json`，自动发现共用规则、短剧skills及已登记配置；正文不复制。`GET /api/global-workflow`、`/source?source_id=…`、`/coverage`分别提供目录、当前源与历史run来源核对。UI只读显示来源、范围、SHA256；配置隐藏凭据、环境变量值、请求头及启动参数，工具默认值以AST读取，不执行源码。用户配置属当前电脑，不能证明历史有效模型/权限。缺失与未登记来源明确展示；通用文件API的边界不扩展。

全局工作流是普通左侧导航项，可展开故事创作、影视改编、Prompt编译；影视改编按拍摄单位从大到小：「1.2.2 片种」（电影的幕、连续剧的集）、「1.2.3 场」、「1.2.4 覆盖」、「1.2.5 镜头」（子页功能镜头、景别、取景、角度与高度、焦点与景深、运镜；正文在 `.agents/skills/ai-videos-pipeline/modules/filming-*.md`）；原 `/workflow/filming/shot-sizes` 重定向到镜头页（follow-up 213/216）。各层共用导航树的缩进、折叠、键盘操作与选中高亮，深链接自动展开父项，文件树加载失败仍可访问全局内容。入口不绑定剧/EP，UI只读。

工作流页以故事创作、影视改编、Prompt编译替换旧阶段图。魔兽世界左侧固定0_research、1_资产库、2_故事、3_影视改编、4_prompt编译；stage可展开，点击其EP1子项进入对应内容，无“EP1 创作”独立入口。集目录从实际文件发现。
每模块一个JSON文件；保存/确定只写当前模块，上游内容指纹变化使下游待更新。编译为固定转换，不调用生成服务。
故事 run 机制（profile、run 历史、选用记录、相关页面与 API、`tools/story_run.py`）已移除（follow-up 206）；故事模块从零重写，EP 导航中故事与其他模块同样每集直达 story.json。
三模块及支持文档只读，修改由Claude Code/Codex完成，UI仅导航、刷新、复制和下载。`GET/POST /api/episode-workflow`保留读写及版本检查能力；UI没有编辑、保存、确定或编译按钮。

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
