---
worker_id: level-specialist-04-system_tests
stage: 5
role: level-specialist
level: system_tests
status: complete
blockers: []
confidence: medium
---

# System tests — jimeng_web_bridge

Run: jimeng_web_bridge-20260913-093603
依据：`final_specs/spec.md`（F1–F7、FR-1..FR-56、NFR「可测性」、§9、§10）· `findings/angle-page-anatomy.md` · `findings/angle-browser-automation-reliability.md` · `agent_refs/validation/{general,development}.md` · `agent_refs/project/development.md`。

confidence 定为 medium，原因有二：真实即梦 DOM／响应体要到 stage-6 探针才拿得到，Fake 站点的保真度要等探针回灌后才能锁死（§17）；另外有几处 spec 冲突需要 parent 裁决（§19）。

---

## 0. 总则

### 0.1 分层

| 层 | 名称 | 起法 | 能否 DI override | 主要用途 |
|---|---|---|---|---|
| T0 | `boot_smoke` | 子进程跑 `make run` 同一入口（§1.4 的 repo-root 覆盖） | 否 | 启动、健康、MCP 握手、干净退出 |
| T1 | prod-mode 集成 | pytest 进程内 `create_app(container, serve_static=True)` + `TestClient`（含 lifespan） | 是 | 逐 endpoint 覆盖、405 sweep、consumer-walk、shared types |
| T2 | 进程内系统 | pytest 在后台线程起真实 uvicorn（Windows ProactorEventLoop）+ 真实 BrowserActor + Fake 即梦站点 + fake dreamina | 是（toast、clock） | 暂停分级矩阵、调度、闸门、token 过期、浏览器丢失 |
| T3 | 进程级 e2e | 子进程跑 `make run` 同一入口 + `@playwright/test` 驱动管理 UI + 官方 MCP Python SDK 客户端 | 否 | 黄金路径、MCP e2e、崩溃安全、7 页 UI、CLI 与主体流程 |
| T4 | 人工 | `make canary`（真实站点只读）+ UI 人工 walkthrough | — | `validation.requires_manual_walkthrough` |

- **只有一种运行模式**（NFR：`make run`；README 不宣传 Vite dev server）→ **Playwright e2e profile 恰好一个：`run`**。T3 的 `webServer.command` 必须与 Makefile `run` 目标调用的是同一模块（SYS-05 用静态断言防漂移）。stage-5 strategy 里 profile 数 ≠ 运行模式数，按 `blocker` 处理。
- 所有 T1–T3 都挂静态 UI（serve_static=True 等价）。UI 构建产物必须先由 `make ui-build` 产出；缺 `apps/api/static/index.html` 时 harness 预检直接失败，**不允许 skip**。
- 测试目录（development.md §6）：`tests/api/system/`（T1）、`tests/system/`（T2、T3 的 Python 侧）、`tests/ui/e2e/*.spec.ts` + `tests/ui/playwright.config.ts`（T3 的 UI 侧，依赖装在 `apps/ui/node_modules`），fixtures 放在 `tests/fixtures/{fake_jimeng_site,fake_dreamina,real_shots,real_dom_snapshots,real_responses}/`。
- Python 一律 `pip` + 仓库 `.venv`（development.md §6），Makefile 里不得出现 `uv run`。

### 0.2 场景编号与 severity

编号 `SYS-NN`。严重度沿用 general.md 与 development.md 的表，本层额外约定：

| 失败类 | severity |
|---|---|
| T0 `boot_smoke` 任一失败 | `critical`，立即 halt，不走修订轮 |
| **任何自动化测试触达真实即梦域名或真实 `dreamina`**（§1.5 护栏跳闸） | `critical`，立即 halt |
| 未确认 batch 的 job 进入 `submitting`，或 fake 站点 ledger 记到多余的「生成」点击 | `critical` |
| 路径逃逸／沙箱写出界 | `critical` |
| UI 深链或数据加载失败时出现空白页 | `critical` |
| 前后端 JSON 字段漂移（§14） | `critical` |
| 黄金路径 e2e 失败；state-changing endpoint 缺 prod-mode 测试；405 sweep 命中 | `blocker` |
| 暂停分级错层（job 级原因停了整个队列，或反过来） | `blocker` |
| 调度约束违反（generating > 上限、提交间隔 < 下限） | `blocker` |
| 缺 Windows skip marker 的 POSIX-only 测试 | `blocker` |
| 已知 flaky 区域（§18）单次超时、重跑通过 | `warning` |

### 0.3 work_unit_kind → 场景

| work_unit_kind | 跑哪些 SYS |
|---|---|
| `boot_smoke` | SYS-01..06 |
| `backend_api` | §13 全表 + SYS-60..63（consumer-walk／shared types）+ 与该 unit 相关的 T2 场景 |
| `browser_backend`（WebUiBackend／PageMap／BrowserActor） | SYS-10、SYS-30..35、SYS-40..49、SYS-50..52、SYS-55，外加 §17.3 的 PageMap 双向解析测试 |
| `cli_backend` | SYS-70..74 |
| `entity` | SYS-80..83 |
| `mcp_transport` | SYS-20..27 |
| `frontend_component` | §15 与该页面对应的 SYS-9x + SYS-10 |
| 收尾 | 全量 T0–T3 通过 → 发出 `validation.requires_manual_walkthrough`（§16 canary + UI walkthrough） |

---

## 1. 测试 harness

### 1.1 Fake 即梦站点（`tests/fixtures/fake_jimeng_site/`）

**形态。** 一组静态 HTML/JS/CSS，加一个**极小的本地 stub server**。stub 不可省：状态轮询、提交台账、故障注入都要动态 JSON（见 §19 C12）。
- 由 harness 在 `127.0.0.1:{随机端口}` 启动。
- 前端全部离线：TipTap／ProseMirror 用**真实库**，版本钉死、vendored。手写的 contenteditable 会让插入策略测出假阳性。
- 路径和 query 形状照抄真实站点，让 PageMap 与解析器走的是同一条路：
  - `/ai-tool/generate?type=video&workspace=…`
  - `/ai-tool/elements`
  - 页面 query 与所有 XHR 都带 `aid=513695&web_version=7.5.0-fake&da_version=…`。

**DOM 解剖必须覆盖**（逐条对应 page-anatomy §A–§D）：
1. **工具栏**，顺序为 `[创作类型][模型][参考模式][比例·分辨率·数量][时长][@] … [预计积分][发送↑]`。
   - 创作类型下拉：Agent 模式／图片生成／视频生成／音乐生成／音频生成／数字人／动作模仿。**首帧先渲染「Agent 模式」骨架，约 300 ms 后恢复上次类型**（加载竞态）。
   - 模型下拉：即梦 Seedance 2.5／Seedance 2.0 mini／2.0 Fast VIP／2.0 VIP／2.0 Fast，列表可滚动，每项带说明文字。
   - 参考模式：全能参考／首尾帧／智能多帧／智能编辑（Beta）／超长视频（Beta）。
   - 比例·分辨率·数量弹层：比例 6 种、480P／720P／1080P、数量 1–4。
   - 时长：0–30 滑杆 + 数字输入框（单位 s）。
   - 每个控件的「显示值」可读回，供 FR-29 校验。
2. **编辑器** `div.tiptap.ProseMirror[contenteditable=true][role=textbox]`：
   - 占位文字是 widget；
   - **DOM 里同时存在第二个隐藏的编辑器实例**（用来抓 selector 歧义）。
3. **上传**：没有常驻 `<input type=file>`，只有「+ 参考内容」卡片（hover 提示「上传参考内容」），点击时才动态创建 file input。
   - 上传后出现缩略图与进度，完成信号可配置（缩略图出现／进度条消失／上传 XHR 返回），以便 §17 探针结论回灌。
   - 上传完成后，素材以**文件 stem** 出现在 @ 候选列表。
4. **@ 选择器**：标题「可能@的内容」，首行「+ 创建主体」，下面是带缩略图的主体行（`hy3_主角`、`hy1_主角`、`f80_f80`、`xj_酒剑仙`、`xj_阿奴`……），每行带「…」菜单；已上传素材也在列表里。
   - 选中后插入 mention 节点，节点带 name 属性。
5. **预计积分**：现价 + 划线原价（fixture 价 20／26 积分每秒，22 s → `440`／`572`），随参数变化而重算。
6. **负向框**：由开关决定有无（`negative_box=on|off`，对应 §10 Q4 未决）。
7. **历史记录流**：
   - 每条记录顶部是参考缩略图条；prompt 内 @ 项渲染为 chip；
   - 元信息行 `即梦 Seedance 2.5 | 22s | 16:9 | 720P | 详细信息ⓘ`，hover 详细信息显示「生成时间」「消耗积分数」，生成中显示「计算中」；
   - 生成中叠加「N%造梦中」，并有文字「超级会员 成功进入生成阶段…」；
   - 浮标「k/3 生成中… 回到底部」；
   - **有记录更新时自动滚到底部**（专抓坐标点击）；
   - 已完成记录带「重新编辑」「再次生成」「⋯」和若干**无文字无 aria-label** 的 `span.action-button-*`；
   - 下载入口位置可配置（`download_entry=menu|icon`，§10 Q1 未决）。
8. **主体页** `/ai-tool/elements`：卡片网格，首张是「新建主体」，带筛选／时间／排序。
   - 「设置主体」弹窗：`参考主体*`（主图 + 附加图位 + 添加）、`添加角色`、`名称*` 带 `x/20` 计数、`描述`、`保存`。
9. **页头**：积分文本（`1.1万` 形态）、会员标识、登录标志（头像）。未登录时换成「登录」按钮，并出现扫码登录弹层。

**Stub 接口**（响应体形状以 §17 探针抓到的真实 body 为模板，探针前先用占位 schema，版本号标 `fake-pre-probe`）：
- `POST /mweb/v1/get_history_queue_info`、`POST /mweb/v1/get_history_by_ids`：页面每 2 s 轮询一次，**空闲时也轮询**（FR-27 canary 要能截获「最近一次状态响应」）。
- `POST /mweb/v1/creation_agent/v2/subscribe_session`：长轮询，先 pending 后 200。
- `POST /mweb/v1/video_generate/get_common_config`、`POST /mweb/v1/dreamina_subject/get`、`POST /mweb/v1/get_asset_list`。
- `POST /commerce/v1/benefits/user_credit`、`POST /commerce/v1/benefits/user_credit_history`。
- 提交接口：路径在探针前用占位 `/mweb/v1/aigc_draft/generate`，由 PageMap／解析器配置指向，不写死。
- 上传接口：占位，完成信号可配置。
- 视频结果 URL：带签名和过期参数的形状（`/{sig}/{expiry}/video/tos/…`），过期后返回 403（用来测「CDN URL 过期」）。
  - 下载得到 fixture mp4：**22 s、16:9、极低码率，sha256 固定**，fixture 构建时由 ffmpeg 生成，结果进 git。

**控制面（只有 harness 能调，与页面分端口）** `http://127.0.0.1:{ctl_port}/__fake__/…`：
- `ledger`：结构化台账，每次控件设值（控件、显示值、时间）、每次上传（文件名、字节 sha256、顺序）、编辑器最终快照（纯文本、mention 序列）、负向框内容、**每一次「生成」点击**（单调时间戳、当时 payload 摘要、是否被接受、产生的 task_id）、主体表单保存。
- `inject`：见下表。每条注入可指定「下一次 X 时生效」「持续 N 次」「在 job 的第几阶段生效」。
- `release`／`hold`：门控（生成按钮启用门、提交响应门、任务完成门、上传完成门）。
- `seed`：预置外部任务（例如用户手工在跑的 2 条）、主体列表、积分余额、登录态。
- `reset`：清空台账与状态。

**故障注入目录**

| inject id | Fake 站点行为 | 期望产品结果 | FR |
|---|---|---|---|
| `captcha_popup` | 下一个 UI 动作前弹出「安全验证」遮罩（滑块占位），遮罩不消失 | web 队列 `captcha_or_risk_popup`，整队暂停、toast、截图；**不做任何求解尝试**（ledger 无遮罩内交互） | FR-21、§2 |
| `risk_popup` | 提交后弹「检测到异常行为」 | 同上 | FR-21 |
| `login_expired` | 头像消失、出现「登录」+ 扫码弹层；XHR 返回未登录码 | `login_expired`，web 队列暂停；session 变 `login_required`；窗口置前（记录日志事件）；service 不输入任何凭据 | FR-21、FR-26 |
| `insufficient_credit` | 余额置 0，点击生成弹「积分不足」且不建任务 | `insufficient_credit`，队列暂停 | FR-21 |
| `backpressure` | 点击生成弹 toast「并行任务已达上限」，**不建任务、无提交成功响应** | job 回到 `awaiting_submit_slot`，不算失败；之后重点击只能在「无任务被创建」有正面证据时发生（§19 C2） | FR-18 |
| `moderation_reject` | 任务在 `get_history_by_ids` 里转失败，带审核原因 | 仅该 job `failed(moderation_reject)`，队列继续，prompt 不被改写 | FR-20、FR-21 |
| `real_face_rejected` | 上传或生成失败，原因「暂不支持真人人脸」 | 该 job `real_face_rejected`，队列继续 | FR-21 |
| `upload_reject` | 指定文件上传被拒（格式／大小提示） | 该 job `upload_rejected`；按 FR-20 最多重试 3 次后停 | FR-20、FR-30 |
| `editor_append_on_refill` | 失焦后再写入变成追加（复现 Playwright #39492 形态） | 首次校验失败 → 清空重填一次 → 仍失败 → `fill_mismatch`，ledger 生成点击 = 0 | FR-31 |
| `editor_drop_mention` | 第 k 个 mention 选中后不插入节点 | 同上（mention 序列不一致） | FR-31 |
| `mention_candidate_missing` | @ 列表里找不到某个 stem | `fill_mismatch`（或 `upload_rejected`，由上传完成判定决定）；不提交 | FR-30、FR-31 |
| `control_readback_mismatch` | 设时长 22，显示值却是 15 | 重试后仍不一致 → `page_contract_broken`，队列暂停 | FR-29 |
| `layout_next` | 模型下拉换了文本或结构、编辑器 role 被移除 | canary 失败 → `page_contract_broken` | FR-27、FR-28 |
| `status_malformed` | 状态响应 body 非 JSON 或缺字段，连续 N 次 | 连续超阈值 → `page_contract_broken`；阈值以下只计数 | FR-34 |
| `status_delayed` | 状态响应延迟 20 s 或长时间空白 | job 保持 `generating`，不误判；超过 `wait.timeout_h` → `wait_timeout` | FR-34、FR-19 |
| `body_unreadable` | 响应在读 body 前页面导航走（复现「No resource with given identifier」） | 读失败计数，不崩溃 | FR-34 |
| `submit_response_hidden` | 点击后提交响应不可被截获（例如走 iframe） | 按 FR-33 在历史里找「提交时刻之后、prompt 前缀一致」的最新一条来对账；对不上 → `paused_needs_human(restart_during_submit)` | FR-33 |
| `page_reload_mid_generation` | 任务生成中时整页 reload | 监听器重挂，状态继续被截获；不重复点击 | FR-34、FR-37 |
| `download_watermark_variant` | 下载控件和 CDN URL 返回不同字节 | FR-35 校验 sha256／size 不一致 → 该 job 不落盘，进入暂停；探针定案前只作可配置分支 | FR-35 |
| `download_truncated` | 下载字节截断 | ffprobe／size 校验失败 → 重试 ≤ 3 → 仍失败则暂停；目标路径不出现半截文件 | FR-20、FR-35 |
| `cdn_url_expired` | 结果 URL 返回 403 | 走备用下载入口或暂停；不落半截文件 | FR-35 |
| `compliance_popup` | 弹出合规确认弹窗 | `compliance_confirmation_required`，队列暂停 | FR-21 |
| `entity_save_fail` | 主体表单保存后，下一次同步里没有该主体 | create 结果为「验证失败」，不重复创建 | FR-49 |
| `logged_out_at_boot` | 冷启动时就未登录 | F1：`login_required` → `seed login` 后 canary 通过 → `ready` | F1、FR-26 |

### 1.2 fake `dreamina`（`tests/fixtures/fake_dreamina/`）

- **必须是真 `.exe`，不许用 `.cmd`／`.bat`。** `.cmd` 会经过 `cmd.exe`：`%`、`^`、`&` 被改写，FR-38「列表传参、不经 shell」的保证就测不出来了。做法：fixture 是一个带 console-script 入口的小 Python 包，session 开始时 `pip install --no-deps --prefix {tmp}/fake_cli`，得到 `{tmp}/fake_cli/Scripts/dreamina.exe`（distlib launcher）。test global.toml 的 `cli.path` 指向它。**不装进仓库 `.venv`**，免得在用户 PATH 上遮住真 CLI。
- 行为由 `FAKE_DREAMINA_STATE={tmp}/fake_cli/state.json` 控制（service 子进程继承环境）。每次调用把 **argv 数组原样**、cwd、时间追加进 `{tmp}/fake_cli/calls.jsonl`。
- 支持的命令：`version`（输出 `1.4.5`；可切成 `1.4.0` 测 FR-41 warning）、`user_credit`、`text2image`、`image2image`、`query_result --submit_id --download_dir`、`list_task`。其余命令一律非零退出，并在 stderr 写 `unexpected command`（抓调用范围越界）。
- 模式：
  - `ok`：返回 `submit_id`，第 k 次 query 才完成，下载写出 4 张 fixture PNG，sha256 固定。
  - `not_logged_in`；`compliance_required`（输出 `AigcComplianceConfirmationRequired`）；`nonzero_exit`；`malformed_json`；`slow_query`（query 需 N 次）；`download_corrupt`（PNG 截断）。
- **绝不读取** `~/.dreamina_cli/`。harness 另把子进程的 `USERPROFILE`／`HOME` 指向 `{tmp}/home`（纵深防御，见 §1.5）。

### 1.3 `ai_videos/` 子集（临时 repo root）

每个 session 复制一份到 `{tmp}/repo/ai_videos/`，只读来源是仓库当前树。**全部是真实文件**（development.md §10：解析器要跑在真实上游产物上）：

| 用途 | 复制的路径 |
|---|---|
| 系列标记 | `huangye_shenghuo/series.json`、`huangye_shenghuo/_series/series_bible.md` |
| 黄金路径 shot | `huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/{shot02.md, renders/…}`（renders 里已有 1 个 mp4，用来断言「永不覆盖」）；另带 `shot01/shot01.md`、`shot03/shot03.md` 凑一批 |
| shot02 引用资产 | `hy3/2_世界观人设/scenes/caoya/bg11_崖脚洼地/{bg11-1.png, bg11_崖脚洼地.md}`、`hy3/2_世界观人设/props/p2_随身装备/{p2-1.png, p2_随身装备.md}`、`hy3/2_世界观人设/props/p3_抹泥板与黏土壁炉/{p3-1.png, p3-2.png, p3_抹泥板与黏土壁炉.md}`、`hy3/2_世界观人设/characters/c1_砌炉的老人/{c1-1.png, c1_砌炉的老人.md}` |
| 跨集 `.link.json` | `hy2/2_世界观人设/characters/c1_造家的人/*.link.json`、`hy2/2_世界观人设/props/{p1_砍刀,p2_随身装备}/*.link.json`、`hy2/2_世界观人设/scenes/hongshan/{bg2_树冠仰视/bg2-1.png, bg3_红杉林步道/bg3-1.png}`、`hy2/5_6_分镜与prompt/shots/shot01/shot01.md`，以及 link 指向的 `hy1/2_世界观人设/characters/c1_造家的人/{c1_造家的人.png, .mp4, .md}` 和 `hy1/2_世界观人设/props/{p1_砍刀,p2_随身装备}/*.png` |
| 旧写法（真实） | `rexue_gaoxiao/5_6_分镜与prompt/shots/shot01/shot01.md`（`=>@1`，无括号）、`shot02/shot02.md`（`姜川野=>@1, …=>@2`） |
| 平铺剧 | `rexue_gaoxiao/README.md`、`wushen_juexing/README.md` |
| 非剧目录 | `_deleted/`（空目录 + 1 个占位文件） |
| 合成夹具（仅这几条是手写的，文件名带 `__synthetic`） | `hy3/…/shot90__synthetic/shot90__synthetic.md`：参考项多重匹配（在剧根另放一个同 stem `bg11-1.jpg`）、未知 label、`上一镜末帧`；`evil.png.link.json`（target 为 `../../../Windows/win.ini`）；主体名 21 字的 override；含 `%^&|"` 与反引号的资产卡块 |

真实树的观察（本 worker 已核对）：
- hy3 内 `bg11-1`／`p2-1`／`p3-1`／`c1-1` 各只有一个文件，黄金路径不会误触多重匹配。
- hy2 的 4 个 `.link.json` 目标都存在。
- hy1 `c1_造家的人/` 下只有 `c1_造家的人.png`，**没有 `*-1.png`**，所以 FR-2 默认 `source_images` 在该卡上会匹配空（§11 用它做真实用例）。
- hy3 14 个 shot 的负向块标题都是引用行 `> **反向提示词**（…）：`，不是 markdown 标题（§19 C5）。
- hy3 `bg11_崖脚洼地.md` 里有 2 个 ```text 块：`bg11-1_崖脚洼地全景`（有路由键）和 `人、人物、人影、人群`（负向清单，无路由键，不应成为请求）。

### 1.4 临时 `.data/` 与配置注入

- 每个 T2／T3 session：`{tmp}/repo/` 做 repo root，下含 `ai_videos/`（§1.3）、`projects/jimeng_web_bridge/config/global.toml`（测试值，§1.7）、`.env`（只含测试 token），数据目录 `{tmp}/data/`（`bridge.db`、`chrome_profile/`、`artifacts/`、`logs/`、`tmp/`）。
- **代码仍从真实项目目录运行**，只把 repo root 与数据目录重定向。spec 目前没有这个开关（FR-1 只允许覆盖 token、profile、CLI path），这是测试可执行性缺口，见 §19 C4。建议最小修补：`JIMENG_BRIDGE_REPO_ROOT`（同时决定 `ai_videos/`、`.env`、`config/global.toml` 的查找根）+ `JIMENG_BRIDGE_DATA_DIR`。
- T1 用 container override 注入同样的路径。

### 1.5 硬护栏：自动化测试不可能触达真实站点、不可能花积分

多层叠加，任何一层跳闸都立即 abort session，并按 `critical` 记为 `pipeline.halted`：

| 层 | 机制 | 防住什么 |
|---|---|---|
| G1 启动前配置审计 | pytest session fixture 与 Playwright `globalSetup` 在**启动 service 之前**，用 service 自己的配置 reader（不另写一份）解析「test global.toml + `{tmp}/repo/.env` + 当前进程环境变量」，得到**有效配置**。以下任一不成立即 abort：`browser.start_url` 的 host ∈ {`127.0.0.1`,`localhost`} 且端口 = fake 站点端口；`browser.profile_dir` 位于 `{tmp}/` 内；`cli.path` 解析到 `{tmp}/fake_cli/Scripts/dreamina.exe`；`server.host` 为 loopback；进程环境里的 `JIMENG_BRIDGE_PROFILE_DIR`／`DREAMINA_CLI_PATH` 不存在或同样指向 `{tmp}` | 仓库根的真实 `.env` 优先级高于 config（FR-1），可能把测试悄悄指向真实已登录 profile 或真实 CLI |
| G2 启动后复核 | service 起来后先调 `GET /api/config/global`（非机密字段）和 `GET /api/session`，再核一遍 start_url、profile_dir，以及 cli 版本是否为 fake 的 `1.4.5-fake`；不符立即 `taskkill /T /F` 进程树 | 配置加载顺序与 G1 推算不一致 |
| G3 零凭据浏览器 | test global.toml 设 `browser.channel = "chromium"`（Playwright 自带，不是用户的品牌 Chrome），每个 session 新建 profile → 即使跑到真实域名也没有登录态，不可能生成 | G1、G2 同时失效 |
| G4 fake 站点身份握手 | fake 页面在 `<meta name="x-fake-jimeng">` 里放 harness 生成的 session nonce；首个 canary 之后比对 BrowserActor 页面上的 nonce（取自 canary 明细或日志事件），比对不上 → abort | start_url 被重定向到别处 |
| G5 事后哨兵 | session 前后各记录一次 mtime 与 size，有任何变化 → `critical`：真实 `projects/jimeng_web_bridge/.data/chrome_profile/Default/Cookies`、`~/.dreamina_cli/tasks.db`、仓库真实 `ai_videos/**/renders/` 的文件清单 | 前面几层全部失效后的最后发现手段 |
| G6 `make canary` 隔离 | 只有 `make canary` 会碰真实站点：不被 `make test` 依赖；要求交互式终端 + 明文确认短语；环境里有 `JIMENG_BRIDGE_TEST=1` 时直接拒绝运行 | 误把 canary 塞进自动化 |

- 测试进程不得读取仓库根 `.env`，也不得拿到真实 token。harness 生成随机 token，写进 `{tmp}/repo/.env`。
- §19 C9 可能需要的测试专用 fault hook：只在 `JIMENG_BRIDGE_TEST=1` 且 repo root 位于系统临时目录时生效。security level 需另外证明它在正常 `make run` 下是惰性的。

### 1.6 隔离与复位

- **每个 SYS 场景前**：
  - 重新复制 `{tmp}/repo/ai_videos/`（子集约数十 MB，可接受）；
  - 删除并重建 `bridge.db`；
  - fake 站点 `reset`；
  - 重置 fake CLI 的 `state.json` 与 `calls.jsonl`；
  - 清空 `artifacts/` 和 `logs/`。
- **浏览器 profile**：同一个 T3 文件内复用，省启动时间。崩溃类场景（§6、§9）结束后强制重建：harness 用 `taskkill /T /F` 清掉测试浏览器进程树，再删除整个 `{tmp}/data/chrome_profile/`。这是 **harness 的动作，不是产品行为**（FR-25 禁止产品自动删锁）。
- **串行**：`workers: 1`。单 BrowserActor + 单 profile，本来就不允许并发 session。
- **失败现场**：Playwright `trace: retain-on-failure`；另把 `{tmp}/data/logs/*.jsonl`、fake 站点 ledger、`calls.jsonl` 拷进测试报告目录，免得 tmp 清理后无法复盘。

### 1.7 测试缩放配置（test global.toml 与 spec 默认值的差异）

| 键 | spec 默认 | 测试值 | 理由 |
|---|---|---|---|
| `server.port` | 8790 | 随机空闲端口 | 不与用户本机正在跑的 service 冲突 |
| `browser.start_url` | 真实即梦 | `http://127.0.0.1:{fake}/ai-tool/generate?type=video` | G1 |
| `browser.channel` | chrome | chromium | G3 |
| `pacing.min_submit_interval_s` | 15 | 2 | 调度断言在秒级完成 |
| `wait.timeout_h` | 12 | 0.002（约 7.2 s） | 让 wait_timeout 可测；要求 schema 接受浮点（§19 C8） |
| `canary.interval_min` | 30 | 30；SYS-35 单独用 0.1 测周期触发 | |
| `confirm.allow_http_auto` | false | false；SYS-29 切 true | |
| `budget.auto_confirm_daily_credits` | 2000 | 1000 | 3 镜批次（>1000）会命中上限 |
| `notifications.toast` | true | true（T2 用 DI override 收集；T3 断言日志事件） | |
| `price_table.*` | 带 as_of | 固定 20 积分/秒（seedance2.5 · 720p） | 与 fake 页面价一致；偏差场景另行覆盖 |

### 1.8 Windows 与平台标记

- canonical 主机就是 Windows。以下测试标 `pytest.mark.skipif(sys.platform == "win32", reason="STATUS=SKIPPED-WINDOWS-…")`，并各配一条 Windows 等价测试：

  | 跳过的 POSIX-only 测试 | reason 标签 | Windows 上的等价测试 |
  |---|---|---|
  | 真 symlink 拒绝（需要开发者模式） | `SKIPPED-WINDOWS-SYMLINK` | junction（`mklink /J`）拒绝，无需特权 |
  | `os.replace` 断电原子性 | `SKIPPED-WINDOWS-POWERLOSS` | 只保留「rename 前目标不可见」 |
  | 大小写敏感路径冲突 | `SKIPPED-WINDOWS-CASE` | — |
  | 基于 signal 的进程控制 | `SKIPPED-WINDOWS-SIGNAL` | 崩溃用 `taskkill /T /F`（TerminateProcess）；「用户关窗」用不带 `/F` 的 `taskkill`（发 WM_CLOSE） |

- Windows-only 测试（toast、ProactorEventLoop、窗口置前）在非 Windows 上标 `skipif(sys.platform != "win32", reason="STATUS=SKIPPED-NONWINDOWS-…")`。
- `ffprobe` 缺失时 harness 预检直接失败，**不 skip**：FR-35 依赖它，skip 会把黄金路径藏掉。
- 临时 repo root 放在含空格和中文的目录下（`{tmp}/测试 root/`），专门覆盖 Windows 上的路径编码与引号问题。

---

## 2. boot_smoke（T0，work_unit_kind=`boot_smoke`，失败即 `critical`）

**SYS-01 冷启动。**
- **Setup**：§1.4 临时 repo root；fake 站点已起、已 `seed login`；fake CLI 为 `ok`；数据目录为空。
- **Action**：用 Makefile `run` 目标的同一命令起子进程，只多 repo-root 和 data-dir 两个覆盖。
- **Assert**：
  - 60 s 内端口可连，stderr 无 Traceback；
  - `GET /api/health` → 200 `application/json`；
  - `bridge.db` 为 WAL 模式；
  - `.data/logs/` 出现首条 JSONL 启动事件，且不含 token 字符串。

**SYS-02 会话形状。**
- **Action**：`GET /api/session`，最多轮询 90 s 直到 canary 完成。
- **Assert**：
  - web 部分：`web.login_state ∈ {login_required, ready}`；`web.canary` 是逐项数组，每项形如 `{check, ok, detail?}`；`web.browser_version` 非空；`web.web_version = "7.5.0-fake"`。
  - cli 部分：`cli.logged_in = true`；`cli.version = "1.4.5-fake"`；`cli.balance` 为数字。
  - canary 全项 ok → `ready`。
  - fake ledger：生成点击 = 0，控件设值 = 0（canary 只读，FR-27）。

**SYS-03 MCP 握手。**
- **Action**：用官方 MCP Python SDK 的 Streamable HTTP 客户端，带 `Authorization: Bearer {test token}`，依次 `initialize` → `tools/list`。
- **Assert**：
  - initialize 成功；
  - 工具名集合**恰好**等于 FR-51 的 10 个，多一个少一个都算失败：`session_status, precheck_batch, confirm_batch, wait_jobs, list_jobs, cancel_job, resume, browser_step, entities, get_screenshot`；
  - 每个工具有 `inputSchema`（type=object）；
  - 首个请求不报 "Task group is not initialized"——这个错误说明挂载的 MCP 子应用 lifespan 没被宿主运行（mcp-http-interface angle）。

**SYS-04 UI 已挂载。**
- **Action**：`GET /`、`GET /batches/does-not-exist`（深链）、`GET /assets/{构建产物中的某个 js}`、`GET /api/nope`。
- **Assert**：
  - 前两个都是 200 `text/html`，并含 root 挂载点；
  - js 为 200，content-type 正确；
  - `/api/nope` 是 404 JSON，**不是** index.html——静态 `html=True` 兜底不得吞掉 `/api/*`。

**SYS-05 单模式防漂移（静态检查）。**
- Makefile `run` 调用的模块，与 `tests/ui/playwright.config.ts` 中 `webServer.command` 调用的模块一致。
- Makefile 不含 `uv`，也没有 `run-frontend`／`dev` 这类第二运行模式目标。
- README 不出现 Vite dev server 启动说明。
- `vite.config.ts` 若出现 `server.proxy`，本层记 `warning`，并转 security level 做 general.md §7 的三形状测试。

**SYS-06 干净退出。**
- **Action**：以 `CREATE_NEW_PROCESS_GROUP` 启动，发 CTRL_BREAK，等 30 s。
- **Assert**：
  - 进程正常退出；
  - 命令行含 `{tmp}/data/chrome_profile` 的 Chrome 进程为 0（查 `Win32_Process`）；
  - profile 下无 `lockfile`；
  - 立即重跑 SYS-01 → 能启动，**不报 `profile_in_use`**。

**SYS-07 启动失败分类**（附属场景，`blocker`）：
- 预先起一个占用同一 profile 的 Chromium → `GET /api/session` 显示 `web.launch_error = profile_in_use`；锁文件**仍在**（FR-25）；`/api/health` 仍 200。
- `channel=chrome` 且本机无 Chrome → `browser_missing`（本机已装则 skip，并写明 reason）。
- start_url 指向不响应端口 → 分类为 `launch_timeout` 或 canary 失败，按实现断言其一。

---

## 3. 黄金路径 e2e（T3，浏览器驱动 UI + 真实后端 + Fake 站点）

**SYS-10 hy3 shot02 全链路**（§9 AC1、AC7、AC12）。管理 UI 由 Playwright 测试浏览器驱动；BrowserActor 驱动 fake 站点。两者是不同的浏览器。

**Setup**
- §1.3 子集。
- fake 站点 `seed`：已登录；主体 = `hy3_主角, hy1_主角, f80_f80, xj_酒剑仙, xj_阿奴`；余额 11000；`negative_box=off`。
- hy3 **预置**一份手写 `jimeng_config.toml`：含注释行 `# 手写注释：保留我`，只有 `[drama] abbrev = "hy3"` 和 `[video] resolution = "720p"`。
- 测试浏览器全程收集 console error 与 `pageerror`。

**Steps 与断言**
1. **会话页**：打开 `/`。显示 web 已就绪、canary 逐项全绿、`7.5.0-fake`、CLI 版本与余额。
2. **主体同步**：主体对账页点「同步」→ 出现 5 个即梦主体。
3. **生成默认 config**：
   - 剧 config 页的剧列表里展开「荒野生活」，子项为 `hy1, hy2, hy3`，**没有 `_series`**；`rexue_gaoxiao`、`wushen_juexing` 与系列同级。
   - 选 hy3，点「生成默认 config」。
   - **Assert**：
     - 磁盘文件字节不变（FR-3 不覆盖），UI 展示逐键 diff；
     - `drama.abbrev = hy3`；
     - 置顶标黄的需确认项含「期望主体名 `hy3_砌炉的老人` 与即梦现有主体不一致」；
     - 参考项解析预览里，shot02 的 `砌炉的老人` 报「主体不在快照中」，并提示键 `entities.overrides."c1_砌炉的老人"`。
4. **表单编辑**：在表单填 `entities.overrides."c1_砌炉的老人" = "hy3_主角"`，保存。
   - **磁盘**：
     - 仍含 `# 手写注释：保留我`，原键顺序不变，新键已写入；
     - 无遗留临时文件（原子写，FR-4）。
   - **UI**：解析预览里 shot02 四项全部 resolved：
     - `bg11-1` → `…/bg11_崖脚洼地/bg11-1.png`（image）
     - `砌炉的老人` → `entity: hy3_主角`
     - `p2-1` → `…/p2_随身装备/p2-1.png`
     - `p3-1` → `…/p3_抹泥板与黏土壁炉/p3-1.png`
5. **非法值**：`video.resolution` 改成 `8k` → 保存被拒，字段旁显示路径 `video.resolution`，磁盘不变。改回。
6. **409**：UI 加载后，测试进程往磁盘文件追加一行注释 → UI 保存 → 显示「文件已被别处修改」，磁盘保留测试进程写入的版本。
7. **precheck（HTTP，带 bearer 与 `idempotency_key`）**：`POST /api/batches`，items = `[hy3 shot02]`。
   - `params = {model: seedance2.5, ratio: "16:9", duration_s: 22, resolution: "720p", count: 1, reference_mode: "全能参考"}`。
   - references 顺序 = `[bg11-1(image), 砌炉的老人(entity→hy3_主角), p2-1(image), p3-1(image)]`；每个 image 项的 sha256 等于测试侧对文件自算的值。
   - `prompt_sha256` 等于 `## 视频 prompt` 下第一个 ```text 围栏内原文字节的 sha256（逐字节，含首行 `shot02` 和 `参考:` 行，FR-8）。
   - `negative_prompt` 等于 `> **反向提示词**` 引用行之后那个围栏的原文（§19 C5）。
   - 无 error；1 条 warning：平台无负向框，负向词将被省略。
   - `credits.static = 440`；`confirmation_token` 非空；`confirm_url` 指向 UI。
8. **确认页**（测试浏览器打开 `confirm_url`），逐项核对 DOM：
   - 1 条条目，4 个参考项，其中 3 张缩略图；
   - 主体显示 `hy3_主角`；
   - 参数行 `Seedance 2.5 · 16:9 · 22s · 720P · ×1`；
   - 静态预计 440；
   - **合计积分文本 = API 返回的合计**（AC12）；
   - warning 可见；「确认并开始」可用。
9. **确认**：点击。
   - `GET /api/batches/{id}` 显示 confirmed、`confirmer=ui_human`、带确认时间。
   - 同一 token 再调 `POST …/confirm` → 被拒（单次有效，AC2）。
10. **队列看板**：job 状态依次出现 `preparing`（子步骤 `set_params → upload → fill → preview`）→ `awaiting_submit_slot` → `submitting` → `generating`，`N%` 递增。以状态序列断言：允许跳过中间态，不允许倒序。
11. **fake ledger（AC1 核心）**：
    - 控件读回：创作类型 = 视频生成、模型 = 即梦 Seedance 2.5、参考模式 = 全能参考、比例 = 16:9、分辨率 = 720P、数量 = 1、时长 = 22。
    - 上传 **3** 个文件，顺序 `bg11-1.png`、`p2-1.png`、`p3-1.png`；平台显示名的 stem 与参考项 name 逐字一致；字节 sha256 与源文件一致（FR-30；与 AC1 措辞的差异见 §19 C1）。
    - mention 序列 = `[bg11-1, hy3_主角, p2-1, p3-1]`；规范化纯文本等于期望文本。
    - 编辑器文本不含负向词片段（抽查 `第二个人, 人群`）；负向框为空。
    - **生成点击恰好 1 次**，发生在 `confirmed_at` 之后。
12. **预演产物**：artifacts 有全页截图和 composer 局部截图各 1 张；`GET /api/artifacts/{job_id}/{name}` → 200 `image/png`；看板显示缩略图。
13. **完成**（`release` 完成门）：
    - **磁盘**：
      - `shot02/renders/` 新增恰好 1 个文件，名称匹配 `shot02_\d{8}-\d{6}\.mp4`；
      - 原有 `jimeng-2026-09-13-…mp4` 的字节与 mtime 不变；
      - 新文件 sha256 = fake fixture 的 sha256（FR-45）；
      - `renders/` 和 `.data/tmp/` 无临时残留。
    - **sidecar** `shot02_….mp4.jimeng.json`，FR-44 字段全部存在且类型正确：
      - `job_id`、`batch_id`、`backend=web`；
      - `source{type=shot, path, block_key}`、`prompt_sha256`（与步骤 7 相同）、`negative_prompt_sha256`；
      - `references[4]`：image 项带 path + sha256，entity 项为 `hy3_主角`；`params`；
      - `platform_task_id`（= ledger 里的 task_id）、`credits_estimated{static:440, page:440}`、`credits_charged:440`（取自 fake 详细信息）；
      - `submitted_at` < `finished_at`；`confirmer=ui_human`；
      - `web_version=7.5.0-fake`、`browser_version` 非空；
      - `output{sha256, size, duration_s≈22, width, height}`，宽高比为 16:9。
      - 全文不含 test token。
14. **历史页**：筛选 剧 = hy3、镜 = shot02 → 1 行，预估 440 / 实扣 440，当日合计 440；batch 详情显示开始／结束余额 11000 → 10560。
15. **结构健全**：
    - 访问过的每页 `main` 非空；侧边导航 7 项齐全；
    - 系列树至少有 1 个展开的系列节点 + 3 个剧叶子；
    - `consoleErrors` 与 `pageerror` 为空；
    - 测试浏览器记录的所有非 GET 请求都没有 405 或 403。

---

## 4. MCP e2e（T3，真实 MCP 客户端 · Streamable HTTP）

客户端统一用官方 MCP Python SDK。每个 tool 调用都记录墙钟耗时，**任一调用 ≥ 90 s 即为 `blocker`**（FR-52）。

**SYS-20 Claude 主流程**（F3 / AC10）
- **Setup**：同 SYS-10，但 hy3 config 已含 override；fake 完成门处于 hold。
- **Action / Assert**：
  1. `session_status`：`structuredContent` 与 `content[0].text` 解析出的 JSON **完全相等**。
  2. `precheck_batch`，参数 `items=[{shot: "ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md"}, {shot: …/shot03.md}]`：
     - 返回 `batch_id`、逐条结果、合计积分、`confirmation_token`、`confirm_url`；
     - `structuredContent` 的键集合与 `POST /api/batches` 的响应体键集合相同（两个入口共用同一个 DTO，§14）。
  3. `confirm_batch(batch_id, token)`：
     - 成功，`confirmer = mcp`；
     - 同一 token 再调 → `isError: true`，文本提示「token 已使用」。
  4. `wait_jobs(job_ids, timeout_s=65)` 在完成门 hold 期间调用：
     - 注册 progress 回调，收到 ≥ 2 条 `notifications/progress`，相邻间隔 ≤ 30 s；
     - 调用在 65 s + 5 s 内返回，返回当前快照：每个 job 的 state、子步骤、已等待时长、`next_action` 建议。
  5. `release` 完成门，之后循环 `wait_jobs(timeout_s=20)` 直到全部 `done`：
     - 每次调用 < 90 s；
     - 终态快照带产物路径，且产物已按 SYS-10 第 13 步落盘。
  6. `list_jobs(batch_id)` 与 `GET /api/jobs?batch=…` 返回的 id 集合一致。
  7. `get_screenshot(job_id, name)`：
     - 返回 path 与缩略图（image content，长边 ≤ 768 px，测试侧解码核对尺寸）；
     - **不返回原图 base64**。

**SYS-21 isError 可操作建议**（AC8、AC10）

每行都要求：`isError: true`，文本同时含 `error_code` 和一条可以照做的建议；fake ledger 无任何写入。

| 输入 | 期望建议文本包含 |
|---|---|
| `rexue_gaoxiao/…/shot01.md`（真实旧写法 `=>@1`、无括号） | `references.overrides."学校泳池_bg2_水面_俯拍"` 或「新增一条 rule」 |
| 合成 `shot90__synthetic`：多重匹配 `bg11-1` | 候选路径列表 + `references.overrides."bg11-1"` |
| 合成：未知 label | `references.rules` |
| 缺 override 的 hy3 shot02 | `entities.overrides."c1_砌炉的老人"` 或主体对账页 URL |
| 调 `confirm_batch`，token 被篡改一位 | 「在 UI 确认页确认：{url}」 |
| `browser_step(op=submit)`，job 所属 batch 未确认 | 「先确认 batch：{url}」 |
| `precheck_batch` 与首次同 `idempotency_key`、不同内容 | 409 语义：「idempotency_key 已用于不同内容」 |

**SYS-22 bearer 与 Origin**（AC11，传输层的 e2e 补充；细节归 security level）
- 不带 `Authorization` → 403，MCP 握手失败。
- token 错误 → 403。
- token 正确、但 `Origin: http://evil.example` → 403。
- token 正确、但 `Host: evil.example:{port}` → 403（DNS rebinding）。
- 以上各请求都不会在 `bridge.db` 里创建 batch；日志里不出现 token 原文。

**SYS-23 进度通知不能被当作续命**
- **Action**：`wait_jobs(timeout_s=200)`，超过上限。
- **Assert**：
  - 被夹到 ≤ 90 s，或以 `isError` 拒绝（二选一，按 DTO 约定断言）；
  - 绝不会阻塞超过 90 s。

**SYS-24 `.mcp.json` 片段（静态检查）**
- 解析 README 中的 `.mcp.json` 代码块，断言：`type=http`、`url=http://127.0.0.1:8790/mcp`、`headers.Authorization = "Bearer ${JIMENG_BRIDGE_TOKEN}"`、`timeout = 120000`。
- README 明文写有「`confirm_batch` 不要加入 allow 列表」。
- 真实 Claude Code 上的截断点与 timeout 是否生效，属于 §17 探针 Q9 的人工项。

**SYS-25 `entities` 与 `resume` 工具的二选一参数**
- `entities(action=sync)` 与 `entities(action=reconcile, drama=hy3)` 分别映射到 sync 与 reconcile。
- `resume(job_id=…)` 与 `resume(backend=web)` 分别映射到 `resume_job` 与 `resume_queue`。
- 两个参数都给、或都不给 → `isError`。

---

## 5. 确认闸门：跨入口硬不变量（T2 为主，AC2 / FR-16）

**共同 Setup**：precheck 一个含 shot02 的 batch，不确认。以下每个场景结束时都要断言：
- fake ledger 的生成点击 = 0；
- 该 batch 下所有 job 的转移历史里从未出现 `submitting`。

**SYS-26 未确认，所有入口都被挡住。**
- 被挡的入口：
  - `POST /api/jobs/{id}/steps/submit`（HTTP）；
  - MCP `browser_step(op=submit)`；
  - `POST /api/jobs/{id}/resume`；
  - `POST /api/queues/web/resume`。
- 以上都拒绝，返回业务错误信封 `{error_code, message, hint}`。
- 分步 `set_params`、`upload`、`fill`、`preview` **允许**执行（F7），执行后 ledger 有设值、上传、填写记录，但无生成点击。

**SYS-27 token 失效的三种形态。**
- **过期**（T2，DI override clock：前进 31 min）→ 拒绝。
- **篡改**：改动 batch 内容摘要，例如 precheck 之后改了 shot02.md 的一个字节 → 拒绝，且提示重新预检。
- **重放**：先成功确认一次，再用同一 token 调用 → 拒绝。

**SYS-28 带 error 条目的 batch 不能被确认。**
- precheck 结果里含 error 条目 → UI 确认按钮 disabled；API confirm 被拒；需要重新预检。

**SYS-29 `auto_confirm` 与预算。**
- `allow_http_auto=false` 时，`POST /api/batches` 带 `auto_confirm=true` → 拒绝，并提示 `confirm.allow_http_auto`。
- 切 `true`，预算 1000：
  - 2 镜批次（440×2 = 880）→ 自动确认，`confirmer=http_auto`；
  - 同日再来 1 镜（累计 1320 > 1000）→ 拒绝，提示 `budget.auto_confirm_daily_credits`。
- MCP `precheck_batch` 不接受 `auto_confirm` 参数（schema 里没有该参数，或传了即 `isError`）。

---

## 6. 崩溃安全（T3，进程级杀进程，AC3 / FR-19）

**杀法（Windows）**：
- `taskkill /T /F /PID {service_pid}`，把 service 连同 Playwright driver 与 Chrome 进程树一起终止，等价于断电或崩溃。
- harness 随后清理测试 profile 的锁（§1.6），模拟「用户重启电脑后再起 service」。
- 「只杀 service、留下孤儿 Chrome」单列为 SYS-34。

**SYS-30 `submitting` 已持久化、尚未点击时被杀。**
- **Setup**：fake `hold` 生成按钮启用门（按钮 disabled）。confirm 一个 1 镜 batch。
- **Action**：
  1. 以只读方式轮询 `bridge.db`（WAL 允许并发读），直到 job 状态 = `submitting`，并且 ledger 点击 = 0；
  2. 杀进程树；
  3. `release` 按钮门；
  4. 重启。
- **Assert**：
  - 重启后该 job 为 `paused_needs_human(restart_during_submit)`；
  - 转移历史为 `… → submitting → paused_needs_human`；
  - 在 30 s 观察窗口内（覆盖 ≥ 2 次调度 tick 与 canary），ledger 点击仍为 0；
  - toast 与看板上都能看到原因。
- **可达性说明**：如果实现是「先等按钮可点、再持久化 submitting」，这个窗口就测不到，要按 §19 C9 决定是否加测试专用 fault point。**测不到时记 `warning`，不能让场景假装通过。**

**SYS-31 已点击、提交响应尚未返回时被杀。**
- **Setup**：fake `hold` 提交响应门。
- **Action**：等 ledger 点击 = 1 → 杀进程树 → `release`（fake 站点照常创建任务并开始生成）→ 重启。
- **Assert**：
  - job 为 `paused_needs_human(restart_during_submit)`；
  - 观察窗口内 ledger 点击**仍为 1**；
  - 平台侧恰好 1 个任务；
  - **绝不自动重提**。

**SYS-32 `generating` 中被杀。**
- **Action**：job 进入 `generating`、平台进度 40% 时杀进程树 → 重启 → `release` 完成门。
- **Assert**：
  - 重启后 job 保持 `generating`，并恢复轮询：进度从 ≥ 40% 继续更新；
  - 最终 `done`，产物与 sidecar 按 SYS-10 第 13 步齐全；
  - ledger 点击 = 1；
  - 恢复前先跑了一次 canary（日志事件顺序：canary 在前，`poll.resumed` 在后）。

**SYS-33 `downloading` 中被杀。**
- **Setup**：fake 下载限速到 5 s。
- **Action**：下载进行中杀进程树 → 重启。
- **Assert**：
  - 目标 `renders/` 下**没有**半截文件（杀进程时 `.data/tmp/` 可以有残留）；
  - 重启后重新下载并完成校验，最终恰好 1 个产物 + 1 个 sidecar；
  - ledger 点击 = 1。

**SYS-34 孤儿浏览器持有 profile。**
- **Action**：只 `taskkill /F` service 的 python 进程，不带 `/T`，留下 Chrome → 重启。
- **Assert**：
  - `web.launch_error = profile_in_use`；
  - 锁文件仍在（产品不删）；
  - web 队列暂停，CLI 队列不受影响；
  - UI 会话页显示可操作提示；
  - 用户（harness）关掉孤儿 Chrome 后，点「打开浏览器窗口」恢复 `ready`；
  - 未完成 job 的状态按 FR-19 处理。

---

## 7. 暂停分级与恢复（T2，AC4 / FR-21 / FR-23 / FR-56）

**共同 Setup**
- web 队列：confirm 3 镜（shot01、shot02、shot03）。
- CLI 队列：confirm 1 个资产块（p3-1）。
- 注入 `ToastClient` 的 DI override：记录型 fake，记下 `{reason, page_url, screenshot_path}`。

**SYS-40 队列级矩阵。** 每一行都是独立场景，并跑同一组断言：
- ① 触发该原因的**那一个** backend 队列变为 paused，原因码与表中一致；另一个 backend 的队列继续推进（有新的状态转移作证）。
- ② toast fake 恰好收到 1 次，reason 正确，`page_url` 指向 UI 队列看板或会话页。
- ③ artifacts 里有截图 + DOM 快照（FR-36），路径已入库，`GET /api/artifacts/…` → 200。
- ④ 暂停期间 web 的 ledger 点击数不再增加（web 原因），或 fake CLI 的 `calls.jsonl` 不再出现生成命令（cli 原因）。
- ⑤ 看板显示原因文字 + 截图。

| 原因 | 注入 | 暂停的 backend |
|---|---|---|
| `captcha_or_risk_popup` | `captcha_popup`（在 `upload` 阶段）；`risk_popup`（提交后） | web |
| `login_expired` | `login_expired`（在 `fill` 阶段） | web |
| `insufficient_credit` | `insufficient_credit` | web |
| `page_contract_broken` | 三个变体：`control_readback_mismatch`；`layout_next`；`status_malformed` 超阈值 | web |
| `browser_lost` | 见 §9 | web |
| `compliance_confirmation_required` | fake 站点 `compliance_popup`（web）；fake CLI `compliance_required`（cli） | 各自 |
| `cli_login_required` | fake CLI `not_logged_in` | cli |

**SYS-41 作业级矩阵。** 每行独立，断言：
- ① 只有目标 job 进入对应终态或暂停态；
- ② 同批其余 job 继续推进并最终 `done`；
- ③ 不发队列级 toast（toast fake 调用数为 0）；
- ④ 失败现场留存；成功 job 只保留预演截图（FR-36）；
- ⑤ prompt 与参考项未被改写：`prompt_sha256` 不变，ledger 里没有第二个 payload。

| 原因 | 注入 | 期望态 | 附加断言 |
|---|---|---|---|
| `moderation_reject` | 对 shot02 注入 `moderation_reject` | `failed(moderation_reject)` | 该 job 点击 = 1，**不重提** |
| `real_face_rejected` | `real_face_rejected` | `failed` 或 paused（按 enum 断言原因码） | 同上 |
| `upload_rejected` | 对 `p2-1.png` 注入 `upload_reject`，持续 4 次 | `upload_rejected` | ledger 恰好 4 次上传尝试（1 次 + 3 次重试，FR-20），点击 = 0 |
| `fill_mismatch` | `editor_append_on_refill` 和 `editor_drop_mention` 两个变体 | `fill_mismatch` | 填写恰好 2 轮（首次 + 清空重填 1 次），点击 = 0 |
| `wait_timeout` | `status_delayed`，超过 7.2 s | `paused_needs_human(wait_timeout)` | 平台任务仍在，不重提 |
| `restart_during_submit` | 见 §6 | — | — |

**SYS-42 恢复前先跑自检。**
- 队列级暂停后，web 路径：
  - 注入不解除 → `POST /api/queues/web/resume` → 响应带「自检失败」原因，队列仍 paused，ledger 显示 canary 只读、点击 0；
  - 解除注入（`seed login`，或关闭遮罩）→ 再 resume → canary 通过 → 队列恢复 → 被暂停的 job 继续。
  - 日志顺序：`canary.started` 在前、`queue.resumed` 在后。
- CLI 路径：先调 `user_credit`（在 `calls.jsonl` 里可见），失败则保持暂停。
- `resume_job` 同理，对 `wait_timeout` 的 job 执行。
- 对 `restart_during_submit` 的 resume 语义见 §19 C3。本场景只断言安全侧：resume **不会**在没有新确认的情况下产生第二次点击。

**SYS-43 toast 失败不影响作业**（FR-56）
- toast fake 抛异常 → 队列照常暂停，状态照常入库；日志有 `toast.failed`；API 与 UI 状态正确。

**SYS-44 T3 侧的 toast 证据**
- 进程级场景（SYS-30、SYS-31、SYS-50）无法 override DI，改为断言 `.data/logs/*.jsonl` 里有 `toast.attempted{reason}` 事件（或 `toast.failed`，二者其一；Windows 通知是否真的显示归人工 walkthrough）。
- 事件名需在实现时固定为日志契约（§19 C7）。

**SYS-45 取消**（FR-22）
- `submitting` 之前取消 → `cancelled`；点击 0；响应不含退款提示。
- `generating` 中取消 → 停止轮询与下载；响应与 UI 取消对话框里都有「积分不会退还」；平台任务不受影响；`renders/` 不落产物。
- 看板上的取消按钮，在提交前后显示不同的确认文案（T3 断言 DOM 文本）。

**SYS-46 幂等与去重**（AC6 / FR-24）
- 同一 `idempotency_key`、同内容再次 precheck → 返回同一个 `batch_id`。
- 已确认并 `done` 的 shot02，不带 key 再 precheck → 结果标注已有 job（指纹命中）；confirm 后不新建 job、点击数不变。
- 带 `reroll: true` → 新 job，`attempt = 2`，点击 +1，产物文件名不冲突。
- key 过期：clock override 前进 25 h → 同 key 不同内容也被接受。

---

## 8. 调度（T2，AC5 / FR-18）

**SYS-47 并发上限与提交间隔。**
- **Setup**：`max_remote_rendering=3`，`min_submit_interval_s=2`；confirm 5 个 job，参数略有不同（避免指纹去重），所有完成门 hold。
- **Action**：以 200 ms 采样 `GET /api/jobs` 状态计数，同时读 ledger。
- **Assert**：
  - 采样期间 `generating` 数始终 ≤ 3；
  - 3 个进入 `generating` 后，第 4、5 个停在 `awaiting_submit_slot`；
  - 按 ledger 单调时间戳，相邻两次**被接受**的点击间隔 ≥ 2.0 s（这里无容差：事件循环延迟只会让间隔变长）；
  - UI 动作全局串行：ledger 中任意两个 job 的 `set_params`、`upload`、`fill` 时间段互不重叠；
  - 放行 1 个 job 完成 → 第 4 个在 ≥ 2 s 间隔约束下提交；最终 5 个全部 `done`，点击恰好 5 次。

**SYS-48 背压「并行任务已达上限」。**
- **Setup**：fake `seed` 2 个外部生成中的任务（模拟用户手工在跑），平台上限 3；service 自己 confirm 3 个 job。
- **Assert**：
  - 第 1 个 job 被接受；
  - 第 2 个点击触发 `backpressure` → 该 job 回到 `awaiting_submit_slot`，状态历史带 reason，**不是** failed、也不是 paused，无 toast；
  - 外部任务完成 1 个后，第 2 个才再次点击，且 ledger 显示前一次点击 `accepted=false`、没有产生 task_id（重点击的前提，§19 C2）；
  - 平台侧每个 job 恰好 1 个任务。

**SYS-49 某个 backend 暂停不影响另一个。**
- web 注入 `captcha_popup`，CLI 队列同时有 2 个资产块 → CLI 两块照常完成，web 保持暂停。反向同理（CLI `not_logged_in`，web 完成）。

---

## 9. 浏览器丢失（T2 / T3，FR-37）

**SYS-50 用户关窗（优雅关闭）。**
- **Setup**：2 个 job 在 `generating`（进度 30%），1 个在 `queued`。
- **Action**：对 BrowserActor 的 Chrome 主进程发不带 `/F` 的 `taskkill /PID`（WM_CLOSE，等价于点窗口 X）。PID 从 `Win32_Process` 中「命令行含测试 profile」的记录找出。
- **Assert**：
  - 5 s 内 web 队列 `browser_lost`（toast 或日志事件有记录）；
  - 随后自动重建 context，`GET /api/session` 的 `browser_version` 仍可读；
  - 登录检查通过（fake 仍为登录态）；
  - 对账：2 个 `generating` 的 job 通过 fake 历史响应被重新关联，进度继续；
  - 恢复后 `queued` 的 job 在 canary 通过后才开始准备；
  - ledger 总点击 = 2（没有重提）。

**SYS-51 浏览器崩溃（强杀）。** 与 SYS-50 相同，但用 `taskkill /T /F` 杀 Chrome 进程树（不杀 service），断言相同。另外覆盖 Windows 上「关掉所有页面后不触发 context `close`」这类不一致（reliability angle #29726）：service 必须靠 page `close`／`crash`，或下一个动作失败，来识别 `browser_lost`，**不能卡住**。判据：60 s 内有状态变化。

**SYS-52 重建后登录失效。** 关窗的同时 fake 切到 `login_expired` → 重建后 `login_required`，队列保持 paused，原因为 `login_expired`；`seed login` + resume → canary → 对账 → 继续。

**SYS-53 页面 reload 与 body 读取失败**（FR-34）
- `page_reload_mid_generation` → 监听不丢，进度继续，点击数不变。
- `body_unreadable` 连续 2 次（低于阈值）→ 只计数，job 不变。
- `status_malformed` 超阈值 → `page_contract_broken`（SYS-40 已覆盖）。

**SYS-54 提交响应截获不到时的对账**（FR-33）
- `submit_response_hidden` + 历史里有一条「提交时刻之后、prompt 前缀一致」的记录 → 关联成功，进入 `generating`。
- 历史里没有匹配记录 → `paused_needs_human(restart_during_submit)`，点击 = 1。

**SYS-55 canary 周期触发**：`canary.interval_min=0.1` → 30 s 内至少 2 次 canary 事件，ledger 无设值与点击；`layout_next` 在两次 canary 之间注入 → 下一次 canary 失败并暂停 web 队列。

---

## 10. CLI 出图（T3 / T2，F5 / AC9 / FR-38..FR-43）

**SYS-70 资产卡 → 候选 → 升格**（T3）
- **Setup**：fake CLI 为 `ok`，`slow_query` 设 k=3；使用真实卡 `hy3/2_世界观人设/props/p3_抹泥板与黏土壁炉/p3_抹泥板与黏土壁炉.md`。
- **Steps / Assert**：
  1. MCP `precheck_batch(items=[{card_path: …p3_抹泥板与黏土壁炉.md, key: "p3-1"}])`：
     - 恰好 1 条请求，`source.block_key = p3-1`；
     - prompt 等于首行为 `p3-1_抹泥板锚点` 的 ```text 块原文（锁定描述符所在的裸围栏不被当成 prompt，FR-9）；
     - `command = text2image`（无参考图）；
     - params 为 `model=5.0, resolution=2k, ratio=1:1`（props 默认）；
     - 该块列在 CLI backend 下。
  2. 反例：对 `bg11_崖脚洼地.md` 全卡 precheck → 只产生 `bg11-1` 一条请求，负向清单块 `人、人物、人影、人群` 不成为请求。
  3. UI 确认 → 看板中 CLI job 进入 `generating`，`submit_id` 入库。`calls.jsonl` 的顺序：`user_credit`（批次开始读余额）→ `text2image` → `query_result` ×3（最后一次带 `--download_dir`，位于 `.data/tmp/` 之下）→ `user_credit`（批次结束读余额）。
  4. **argv 断言（FR-38）**：
     - `text2image` 的 argv 数组中 `--prompt` 的下一个元素与块原文**逐字节相等**（含换行、中文标点、反引号）；
     - 第二个合成块（含 `%^&|"`）走同一流程时 argv 同样逐字节相等——证明没有经过 `cmd.exe`；
     - argv 里不出现 token。
  5. 完成后 `p3_抹泥板与黏土壁炉/_candidates/p3-1/` 下有 4 个 `{ts}_{i}.png`，sha256 与 fixture 一致，每个旁边有 `.jimeng.json`（`backend=cli`、`cli_version=1.4.5-fake`、`platform_task_id=submit_id`）。
  6. 历史页 → 候选网格显示 4 张 → 选第 2 张「选定」→ 二次确认 →
     - `p3-1.png` 字节 = 第 2 张候选；
     - 原 `p3-1.png` 已移到 `ai_videos/_deleted/huangye_shenghuo/hy3/2_世界观人设/props/p3_抹泥板与黏土壁炉/p3-1.png.{ts}.png`，字节等于原文件（FR-43）；
     - `p3-2.png` 不受影响；
     - 升格后的 `p3-1.png` 旁有 sidecar。
  7. `image_on_existing = "fail"` 变体：先改该剧 config，再升格 → 被拒，原文件不动，`_deleted/` 无新增。

**SYS-71 CLI 未登录只暂停 CLI 队列**（T2）
- fake CLI 为 `not_logged_in`；同时 confirm 1 个 web job 与 1 个资产块。
- **Assert**：
  - CLI 队列 `cli_login_required`；UI 会话页提示「请自行运行 `dreamina login`」；`calls.jsonl` 里没有 `login` 命令（service 不代为登录，FR-40）；
  - web job 照常 `done`；
  - 切回 `ok` → resume CLI 队列 → 先 `user_credit`，再继续。

**SYS-72 CLI 失败形态**（T2）
- `compliance_required` → 队列暂停，原因 `compliance_confirmation_required`。
- `nonzero_exit` 与 `malformed_json` 都要映射成明确的原因码，不能抛成未分类的 500（断言 API 错误信封或 job 原因码其一）。
- `download_corrupt` → 下载重试 ≤ 3 → 仍失败则该 job 暂停；`_candidates/` 下无坏文件。

**SYS-73 能力矩阵与路由**（T1 + T2，预检阶段，不调 CLI）
- `routing.video = cli`，shot02（2.5、22 s、主体）→ 预检 error：「cli 不支持主体 / 2.5 / >15 s」，不降级；`calls.jsonl` 为空。
- `routing.video = cli`，合成 10 s、2.0、无主体的请求 → ok，并路由到 CLI backend。

**SYS-74 版本 warning**：fake 输出 `1.4.0` → 启动日志有 warning，`GET /api/session` 的 `cli.version_warning` 为真，服务仍可用（FR-41）。

---

## 11. 主体流程（T3，F6 / FR-47..FR-50）

**SYS-80 同步与三态对账**
- **Setup**：
  - fake 主体列表：`hy3_主角, hy1_主角, f80_f80, xj_酒剑仙`；
  - hy3 config 带 override（→ `hy3_主角`）；
  - hy2 无 config，按提议默认值计算；
  - hy1 无 config。
- **Action**：主体对账页点「同步」→ 查看对账表。
- **Assert**：
  - 同步读取的是 `dreamina_subject/get` 的响应；快照带名称、缩略图 URL、修改时间、同步时间。
  - `hy3_主角` → `mapped`（hy3）。
  - `hy1_造家的人` → `missing_on_platform`。期望名来自 hy1 卡，以及 hy2 通过 `.link.json` 的跨集来源（FR-3，沿用来源集缩写 `hy1_`，**不是** `hy2_造家的人`）。
  - `f80_f80`、`xj_酒剑仙` → `unmapped_on_platform`（临时子集里没有对应剧）。
  - `hy1_主角` 若没有剧映射到它，也是 `unmapped_on_platform`。
  - ledger 无任何写操作（FR-50）。

**SYS-81 创建缺失主体（含真实 glob 缺口）**
1. 对 `hy1_造家的人` 点「创建」→ 预检 error：`source_images` 默认 `{card_dir}/*-1.png` 在 `c1_造家的人/` 下匹配为空（该卡只有 `c1_造家的人.png`，真实树如此）；提示键 `entities.source_images`。
2. 在 hy1 config 里把 `source_images` 改为 `["{card_dir}/c1_造家的人.png"]` → 重新预检：
   - ok；
   - 名称 7 字 ≤ 20；
   - 描述预填为卡中的锁定描述符；
   - 「疑似写实真人」warning 按实现判定，只断言字段存在。
3. 确认页编辑描述 → 确认。
   - **fake ledger**：打开「新建主体」→ 上传 1 张图（sha256 = 卡图）→ 名称 `hy1_造家的人` → 描述等于编辑后文本 → 保存恰好 1 次。
4. 自动再同步 → 对账变为 `mapped`；create 结果为「已验证」。
5. 再点一次「创建」同名 → 直接复用，ledger 不产生第二次保存（FR-49）。

**SYS-82 负面与边界**
- 合成 override 使名称为 21 字 → 预检 error「名称 ≤ 20」，确认按钮不可用。
- `entity_save_fail` → 再同步看不到 → 结果「验证失败」，不自动重试创建。
- 快照超过 24 h（clock override，T2）→ shot02 预检出现「主体快照已过期」warning，但不是 error（FR-11 第 6 条）。
- 任何流程的 ledger 都不出现改名、删除、覆盖已有主体的操作（FR-50）：检查主体「…」菜单交互为 0 次。

**SYS-83 hy2 shot01 跨集引用预检**（`.link.json` 解析，T1）
- hy2 shot01 预检，断言：
  - `bg2-1`、`bg3-1`（label 为 `场景参考图·第二、三段：步道纵深全景`，命中 `场景参考图*`）解析到 hy2 场景文件；
  - `p1_砍刀`、`p2_随身装备` 通过 `.link.json` 解析到 **hy1 目标文件**，sha256 = hy1 文件的 sha256；
  - `造家的人` → `entity: hy1_造家的人`。
- 合成 `evil.png.link.json` → 预检 error（逃出 `ai_videos/`，`critical` 类）；目标文件不被读取。
- junction 指向 `ai_videos/` 外 → 拒绝（Windows 等价测试，§1.8）。

---

## 12. 幂等与去重

已并入 SYS-46（§7），另见 SYS-21 中 idempotency_key 冲突一行。

---

## 13. prod-mode endpoint 覆盖（T1，`serve_static=True`，development.md §1）

**原则**
- 每个 state-changing endpoint 至少有 1 条 prod-mode 集成测试，app 构造方式与 `make run` 相同：静态 UI 挂在 `/`，且 `html=True`。
- 断言有三条：
  - 状态码符合业务预期；
  - `content-type` 必须是 `application/json`；
  - 响应体符合 DTO 形状。
- **只断 200 不够。** 路由缺失或被遮蔽时，GET 会被静态兜底，返回 200 的 index.html；非 GET 则返回 405。
- `{drama}` 参数一律用**系列成员** `huangye_shenghuo%2Fhy3`（3 段），外加一个平铺剧 `rexue_gaoxiao`。原因：Starlette 会把 `%2F` 解码进 path，若路由没声明为 `{drama:path}`，请求就掉进静态 mount——GET 得到 index.html，PUT/POST 得到 405。这正是本仓库踩过的那一类问题。

| # | Method Path | 映射 | prod-mode 测试（T1 名称） | 业务断言要点 |
|---|---|---|---|---|
| E1 | POST `/api/session/canary` | `SessionCommand.run_canary` | `test_session_canary_prod` | 200 + canary 逐项数组；fake ledger 无写入 |
| E2 | POST `/api/batches` | `BatchCommand.precheck` | `test_batches_precheck_prod` | shot02 结果形状（§14 S2）；错误条目带 `config_key` |
| E3 | POST `/api/batches/{id}/confirm` | `BatchCommand.confirm` | `test_batch_confirm_prod` | 正确 token → 200；重放 → 业务错误信封（409 或 403，按约定） |
| E4 | POST `/api/jobs/wait` | `JobQuery.wait` | `test_jobs_wait_prod` | `timeout_s=1` 时 ≤ 3 s 返回快照；超上限被夹或拒绝 |
| E5 | POST `/api/jobs/{id}/cancel` | `JobCommand.cancel` | `test_job_cancel_prod` | queued → cancelled；generating → 带「积分不会退还」 |
| E6 | POST `/api/jobs/{id}/resume` | `JobCommand.resume` | `test_job_resume_prod` | 自检失败 → 保持 paused + 原因 |
| E7 | POST `/api/queues/{backend}/pause` | `JobCommand.pause_queue` | `test_queue_pause_prod` | `web`／`cli` → 200；非法 backend → 422 或业务错误 |
| E8 | POST `/api/queues/{backend}/resume` | `JobCommand.resume_queue` | `test_queue_resume_prod` | 先自检（override 为记录型 fake，断言调用顺序） |
| E9 | POST `/api/jobs/{id}/steps/{op}` | `BrowserStepCommand.run` | `test_browser_step_prod`（参数化 5 个 op） | `submit` 在未确认时被拒（FR-16）；非法 op → 422 |
| E10 | POST `/api/dramas/{drama}/config/propose` | `DramaConfigCommand.propose` | `test_drama_config_propose_prod` | hy3 已有 config → diff，不写盘；hy2 无 config → 提议体 |
| E11 | PUT `/api/dramas/{drama}/config` | `DramaConfigCommand.save` | `test_drama_config_save_prod` | 保留注释；hash 不匹配 → 409；schema 非法 → 422 + 字段路径 |
| E12 | PUT `/api/config/global` | `GlobalConfigCommand.save` | `test_global_config_save_prod` | 保存后 GET 不含机密字段；`server.host = 0.0.0.0` → 被拒 |
| E13 | POST `/api/entities/sync` | `EntityCommand.sync` | `test_entities_sync_prod` | BrowserActor 为 override fake，返回快照 |
| E14 | POST `/api/entities` | `EntityCommand.create` | `test_entities_create_prod` | 21 字名称 → 预检错误；同名 → 复用 |
| E15 | POST `/api/candidates/promote` | `CandidateCommand.promote` | `test_candidates_promote_prod` | 归档到 `_deleted/`；候选路径越界（`..`）→ 拒绝 |
| E16 | POST `/mcp`（及 SDK 使用的 DELETE `/mcp`） | MCP 挂载 | `test_mcp_mount_not_shadowed_prod` | 带 bearer 的 initialize → 200（不是 405）；**GET `/mcp` 不纳入 sweep**，因为 MCP SDK 自己可能合法地返回 405 |

**只读 GET 的 prod-mode 检查**：`test_get_routes_json_not_spa_prod`，参数化 §5.10 全部 10 个 GET 路由。它们都必须返回 JSON，不能是 `text/html`。其中 `GET /api/artifacts/{job_id}/{name}` 例外，期望 `image/png`；越界 name（`..%2F..%2Fbridge.db`）→ 404 或 403 JSON（`critical` 类）。

**405 sweep**
- 测试名：`test_guarded_routes_never_405_prod`。
- `GUARDED_ROUTES` 从 app 的路由表**自动枚举**，而不是手写：凡是方法 ∉ {GET, HEAD} 的 `/api/*` 路由，加上 POST `/mcp`。枚举结果还要与上表 E1–E16 做集合比对——多出或缺少都算失败，防止新加的路由漏测。
- 对每条路由用合法鉴权头（同源 Origin，或 bearer）发请求，body 可以最小或不合法。断言：状态码 ≠ 405，且响应不是 `text/html`。
- 在 `serve_static=True` 下跑。另跑一次 `serve_static=False` 作为对照：两次状态码必须一致，不一致说明静态 mount 在改变路由行为。

**入口映射契约**（与 unit level 共享）：每个 route、每个 MCP tool 恰好调用一个 Query/Command 方法。T1 用记录型 override 断言：调用计数 = 1，且方法名等于 §5.10 / FR-51 表中的映射。

---

## 14. consumer-walk 与 shared types（T1，development.md §2 / §3，漂移 = `critical`）

### 14.1 SYS-60 `GET /api/dramas` consumer walk

spec §5.10 没有定义这个响应的字段名（§19 C6）。本层给出**期望契约**，stage 6 必须在 DTO 与 `apps/ui/src/types.ts` 的**同一个变更**里把它钉死。字段名建议沿用 `ai_video_management` 树的约定：
- 节点 `{name, name_zh?, type: "series" | "drama", children?, is_drama?, drama?}`；
- `drama` = 剧根相对路径（例如 `huangye_shenghuo/hy3`），UI 调用时自行 `encodeURIComponent`。

测试 `test_dramas_consumer_walk`，**只使用 UI 实际读取的字段名**，递归下降：
- 每个 `type == "series"` 的节点必须有非空 `children`，缺失即大声失败（不能静默当叶子处理）；
- 每个叶子 `is_drama == true`，且带 `drama`；
- 对每个叶子，用 `encodeURIComponent(drama)` 调 `GET /api/dramas/{…}/config`，结果只能是 200 JSON 或 404 JSON（`error_code = config_not_found`），**不能是 index.html**；
- 名称含 `_series`、`_deleted` 的节点一律不出现；
- `huangye_shenghuo` 的 children 集合 = `{hy1, hy2, hy3}`（临时子集）；
- `rexue_gaoxiao`、`wushen_juexing` 为顶层叶子；
- 叶子的 depth（2 或 3）与本项目 `libs/common/drama_ref.py` 的计算结果一致。divergence 2 的真实树契约测试归 unit level，这里只做 consumer 视角。

### 14.2 SYS-61 shared types 清单

每个跨边界 JSON 形状都要列出 consumer 字段路径。实现时由测试做两件事：
1. 从后端 DTO（dataclass 或 Pydantic）导出 JSON Schema；
2. 解析 `apps/ui/src/types.ts` 中同名 interface 的字段（`tsc` 生成声明文件后做 AST 读取）。

两边做集合比对：**UI 读取、但后端没有的字段 → `critical`**；后端有、UI 未读 → 仅记录。

| # | 形状（DTO → TS type） | 来源 endpoint / tool | consumer 字段路径（UI 读取） |
|---|---|---|---|
| S1 | `SessionStatusQdto` → `SessionStatus` | GET `/api/session`、`session_status` | `web.login_state`、`web.canary[].check/ok/detail`、`web.browser_version`、`web.web_version`、`web.launch_error`、`cli.logged_in`、`cli.version`、`cli.version_warning`、`cli.balance` |
| S2 | `BatchPrecheckCdto` → `BatchPrecheck` | POST `/api/batches`、`precheck_batch` | `batch_id`、`items[].source.{type,path,block_key}`、`items[].params.{model,ratio,duration_s,resolution,count,reference_mode}`、`items[].references[].{name,label,kind,resolved_path,entity_name,sha256,thumbnail_url}`、`items[].issues[].{severity,code,message,hint,config_key}`、`items[].credits.{static,page}`、`items[].existing_job_id`、`total_credits.{static,page}`、`deviation_warn`、`confirmation_token`、`expires_at`、`confirm_url` |
| S3 | `BatchQdto` → `Batch` | GET `/api/batches/{id}` | S2 字段 + `status`、`confirmer`、`confirmed_at`、`balance_start`、`balance_end`、`job_ids[]` |
| S4 | `JobQdto` → `Job` | GET `/api/jobs`、`/api/jobs/{id}`、`list_jobs` | `job_id`、`batch_id`、`backend`、`state`、`substep.{name,progress}`、`platform_progress_pct`、`pause_reason`、`fail_reason`、`transitions[].{from,to,at,reason}`、`artifacts[].{name,url}`、`output.{path,sidecar_path}`、`attempt`、`credits.{estimated,charged}`、`refund_notice` |
| S5 | `JobWaitQdto` → `JobWaitSnapshot` | POST `/api/jobs/wait`、`wait_jobs` | `jobs[]`（S4）、`waited_s`、`all_terminal`、`next_action` |
| S6 | `DramaTreeQdto` → `DramaNode` | GET `/api/dramas` | 见 14.1 |
| S7 | `DramaConfigQdto` → `DramaConfigView` | GET `/api/dramas/{drama}/config` | `toml_text`、`content_hash`、`values`（按 schema 分节）、`needs_confirmation[].{key,reason}`、`reference_preview[].{shot,references[].{name,label,kind,resolved,error,config_key}}`、`parse_error` |
| S8 | `DramaConfigProposalCdto` → `DramaConfigProposal` | POST `…/config/propose` | `exists`、`proposal_toml`、`diff[].{key,current,proposed}`、`needs_confirmation[]` |
| S9 | `DramaConfigSaveCdto` → `SaveResult` | PUT `…/config` | `content_hash`、`schema_errors[].{path,message}` |
| S10 | `GlobalConfigQdto` → `GlobalConfigView` | GET/PUT `/api/config/global` | `values`（**不含**任何 token 或机密键）、`content_hash`、`schema_errors[]` |
| S11 | `EntityReconcileQdto` → `EntityReconcile` | GET `/api/entities/reconcile`、`entities` | `snapshot_synced_at`、`stale`、`rows[].{name,state,drama,character_dir,thumbnail_url,modified_at}` |
| S12 | `EntityCreateCdto` → `EntityCreateResult` | POST `/api/entities` | `batch_id`/`confirm_url`、`issues[]`、`result.{created,reused,verified}` |
| S13 | `HistoryQdto` → `HistoryPage` | GET `/api/history` | `rows[].{job_id,drama,shot,subject,date,credits_estimated,credits_charged,output_path}`、`daily_totals[].{date,estimated,charged}`、`candidates[].{key,subject_dir,files[].{path,thumbnail_url}}` |
| S14 | `CandidatePromoteCdto` → `PromoteResult` | POST `/api/candidates/promote` | `promoted_path`、`archived_path` |
| S15 | `ErrorEnvelope` → `ApiError` | 所有 4xx/5xx 业务错误 | `error_code`、`message`、`hint`、`config_key` |
| S16 | `ArtifactQuery` 响应 | GET `/api/artifacts/…`、`get_screenshot` | UI：`<img src>`；MCP：`path`、`thumbnail`（image content） |

- **SYS-62 MCP 与 HTTP 同形**：S1、S2、S4、S5、S11 的 MCP `structuredContent` 键集合 = HTTP JSON 键集合（同一个 DTO）。
- **SYS-63 UI 只经 `api.ts` 调用**：静态检查 `apps/ui/src/**` 中 `fetch(` 只出现在 `api.ts`；`api.ts` 导出的每个函数的 path 模板都 ∈ §5.10 路由表。

---

## 15. UI 页面覆盖（T3，FR-54 七页 × 成功态 / 错误态，development.md §8 / §9）

- **错误态注入方式**：只在**测试浏览器**里用 `page.route` 把该页首个数据接口改成 500 或断网；BrowserActor 不受影响。
- **每条场景统一断言**：
  - `main` 非空；
  - 页面特有 selector 存在；
  - 错误态有可见的错误文案 + 重试按钮，**绝不空白**；
  - `consoleErrors` 为空（注入的 500 所产生的 network 错误日志按白名单排除，其余一律不允许）；
  - **深链直接打开**（新标签页直接访问该 URL）同样成立。

| SYS | 页面 | 成功态特有断言 | 错误态 / 特殊渲染模式 |
|---|---|---|---|
| SYS-90 | 会话 | canary 逐项列表；web 与 CLI 两块卡片；「打开浏览器窗口」「运行 canary」按钮可点，点击后列表刷新 | `/api/session` 500 → 错误态；`launch_error=profile_in_use` 渲染可操作提示（SYS-34） |
| SYS-91 | 剧 config（表单视图） | 系列折叠树；表单分节；需确认项置顶标黄；参考项解析预览表 | `/api/dramas` 500 → 错误态；409 冲突提示（SYS-10 第 6 步）；schema 错误字段高亮 |
| SYS-92 | 剧 config（原文 TOML 视图） | 切换到原文视图，文本等于磁盘内容 | **渲染时解析的组件必须有 Error Boundary**：hy1 夹具放一份语法损坏的 `jimeng_config.toml` → 深链打开 → 显示「config 解析失败 + 行号」，不白屏（development.md §9，blank = `critical`） |
| SYS-93 | 批次确认 | 逐条参考项缩略图、主体、参数、静态/页面积分、合计 = API；「确认并开始」 | 含 error 条目时按钮 disabled，error 行可见；静态与页面偏差 > 20% 时高亮（fake 页面价调成 600）；batch 不存在的深链 → 「未找到」；token 已过期 → 提示重新预检 |
| SYS-94 | 队列看板 | 按状态分列；子步骤进度；平台进度 %；暂停原因 + 截图缩略图；取消/恢复/分步按钮 | `/api/jobs` 500 → 错误态；取消对话框在提交前后文案不同（SYS-45）；截图 404 → 占位图，而不是破图 |
| SYS-95 | 历史与积分 | 剧/镜/主体/日期筛选生效；预估与实扣列；每日合计；候选网格 +「选定」 | `/api/history` 500 → 错误态；无数据 → 空态文案（与错误态区分）；候选图加载失败 → 占位 |
| SYS-96 | 主体对账 | 三态徽标；缺失项「创建」走确认页 | `/api/entities/reconcile` 500 → 错误态；从未同步 → 「尚未同步」空态；快照过期 → 警示条 |
| SYS-97 | 全局设置 | 表单；保存后值回显 | 页面源码与 network 响应中都不出现 token 值或 token 字段；非法 `server.host` 字段错误；GET 500 → 错误态 |

**SYS-98 主题与语言（静态 + DOM）**
- 构建产物 CSS 中没有作用于 `body`、导航、面板的 `prefers-color-scheme: dark` 块；`:root` 的 `color-scheme` 为 `light`（project/development.md §7）。
- 7 页主导航文案为中文。
- 视觉层级、对比度、焦点可见性归 accessibility level 与人工 walkthrough。

**SYS-99 花积分按钮的二次确认**（FR-55）
- 以下按钮都必须经过确认页或二次确认对话框才会发请求：「确认并开始」「创建主体」「选定」「分步 submit」「恢复队列」。
- 测试方法：点击后在确认前取消 → 断言 network 中没有对应的 POST。
