# Spec — jimeng_web_bridge

Run: jimeng_web_bridge-20260913-093603
task_type: development · target: `projects/jimeng_web_bridge/`
Compiled from: `user_input/revised_prompt.md` + `interview/qa.md`（含 post-research decisions）+ `findings/dossier.md`（5 个 angle）

---

## 1. Goal

在本机构建一个独立的常驻 service `jimeng_web_bridge`，把即梦的生成能力封装成人、Claude、自动化脚本都能调用的接口。它负责「参考素材 → prompt → 参数 → 提交 → 等待 → 取回并落盘」的完整链路，形态是 HTTP API + MCP + 本地管理网页。

**后端有两条路，共用同一个接口：**
- **视频走网页。** 驱动用户已登录的即梦网页（Seedance 2.5、16–30 s、@主体、多参考），手段是真实 UI 操作 + 被动读页面自己的网络响应。
- **图片走官方 CLI。** Seedream 出图调用官方 `dreamina` CLI。

**两条路共用的部分：**
- 输入适配：原始参数 / `shotNN.md` / 资产卡；
- 静态预检 + 预计积分；
- 人工确认闸门——未经确认不花一分积分；
- 带并发上限、可暂停恢复、重启不丢的作业队列；
- 结果原子落盘到仓库对应目录，并写 sidecar 记录。

**每部剧的所有路由键、命名、映射、默认值、校验阈值都放在该剧自己的 config 里。** service 先按默认值提议，用户在 UI 上查看和修改。

---

## 2. Out of scope（v1）

- 网页上除「视频生成 · 全能参考」之外的模式：首尾帧、智能多帧、智能编辑、超长视频、Agent 模式、音乐 / 音频生成、数字人、动作模仿。
  - 承接镜的「本镜首帧（上一镜末帧）」按全能参考里的一个上传项处理，不走首尾帧模式。
- 网页端图片生成。v1 的图片一律走官方 CLI。
- 伪造或重放即梦内部接口（cookie / 签名），以及任何对抗检测手段：stealth 插件、指纹伪装、验证码求解、改 webdriver 标志。
- 去水印、剥离元数据。
- 多账号、账号轮换、远程部署，以及对 127.0.0.1 以外开放服务。
- 自动改写 prompt 后重提（包括审核被拒的情况），以及任何形式的**自动重复提交**。
- 自动改名或删除即梦上已有的主体。
- 定版、拼接、字幕、BGM。这些已由 `ai_video_management` 负责；本 service 只把产物放到它们约定的位置。
- 为适配本 service 回溯修改旧剧的 shot md（CLAUDE.md「规则变更不回溯」）。旧写法通过每剧 config 的 override 解决。
- Windows Service 形态（浏览器与 toast 都需要交互桌面会话）。

---

## 3. 用户角色与主流程

| 角色 | 入口 | 典型动作 |
|---|---|---|
| 用户（人） | 本地管理网页 | 登录即梦、改 config、确认批次、处理暂停、选定候选图、主体对账 |
| Claude | MCP（`/mcp`） | 预检一集的 shot、提示用户去确认、循环等待、汇报结果 |
| 自动化脚本 | HTTP API（`/api/*`） | 与 Claude 相同；可以显式 `auto_confirm`，默认关闭，且受预算约束 |

### F1 首次启动与登录

1. 用户运行 `make run`。
2. service 以专用 profile 启动有界面的 Chrome，打开即梦创作页。
3. 检测到未登录 → 会话状态 `login_required`，弹出 toast，窗口置前。
4. 用户手动扫码登录。
5. canary 只读自检通过 → 会话状态 `ready`。

### F2 为一部剧建立 config

1. 用户在 UI 选中一部剧，点「生成默认 config」。
2. service 扫描剧目录，提议 `jimeng_config.toml`：剧缩写、主体名映射、参考项解析规则、默认档位……
3. UI 以表单展示提议，并标出「需要你确认」的项（例如独立剧的缩写、与已有主体冲突的名字）。
4. 用户修改后保存；文件落在剧目录、进 git。

### F3 Claude 生成一集的视频（主流程）

1. Claude 调用 `precheck_batch`，传入若干 `shotNN.md`。
2. service 返回 `batch_id`、逐条预检结果、预计积分、UI 确认页链接。
3. Claude 把链接交给用户。用户在 UI 确认页看到每条的解析结果、参考图缩略图、预计积分，点「确认」。（也可以在 Claude Code 的权限询问里批准 `confirm_batch`。）
4. 队列开始执行：UI 动作串行（选档位 → 上传 → 填写 → 预演截图 → 提交），远端同时渲染不超过 3 条。
5. Claude 反复调用 `wait_jobs`（每次 ≤ 90 s），直到完成。
6. 结果落到 `shots/shotNN/renders/`，旁边写 sidecar。之后用户在 `ai_video_management` 里照常定版、拼接。

### F4 暂停与恢复

1. 出现验证码或风控弹窗、登录失效、积分不足、页面结构对不上 → 暂停整个队列，弹 toast，附原因和截图。
2. 用户在浏览器窗口里处理完，回 UI 点「恢复」。
3. 审核被拒的 job 单独标为失败，队列继续。

### F5 资产出图

1. 预检资产卡里以路由键开头的 prompt 块。
2. 用户确认。
3. 调用 CLI `text2image` 或 `image2image`。
4. 候选图落到 `_candidates/{key}/`。
5. 用户在 UI 选定一张 → 升格为 `{key}.png`，旧文件先归档。

### F6 主体对账与创建

1. UI 主体页同步即梦上的主体列表。
2. 与各剧 config 的期望主体名对账：已映射 / 即梦缺失 / 没有映射。
3. 缺失的主体经预检 + 确认后，由 service 走「新建主体」表单创建，再同步一次验证。

### F7 分步调试

对单个 job 分步执行 上传 → 填写 → 预演截图。确认后才允许提交。

---

## 4. 架构总览

```
┌──────────── 单进程 service（FastAPI / uvicorn，127.0.0.1） ────────────┐
│  /api/*  (HTTP routes)     /mcp  (Streamable HTTP tools)   /  (React UI)  │
│        └───────────── 每个入口 = 恰好一个 Query/Command 方法 ─────────────┘  │
│  application: BatchCommand · JobCommand · DramaConfigCommand · EntityCommand │
│               SessionCommand · BrowserStepCommand · *Query                    │
│  domain:      GenerationRequest · ReferenceItem · JobEntity(状态机) · Batch   │
│               Precheck(纯函数) · Fingerprint · ConfirmationToken · DramaConfig│
│               ports: GenerationBackend · JobRepository · DramaConfigRepository│
│  infrastructure:                                                             │
│    WebUiBackend ─ BrowserActor(单个 async Playwright，串行 UI 动作)            │
│                   PageMap(selector 注册表，带 web_version) · ResponseParsers   │
│    DreaminaCliBackend ─ 子进程调用 dreamina                                     │
│    ShotPromptReader · AssetCardReader · DramaTreeReader(.link.json)           │
│    SQLite(WAL) JobStore · OutputWriter(原子落盘+sidecar) · TomlConfigStore      │
│    ToastClient · Host/Origin/Token middleware                                 │
└──────────────────────────────────────────────────────────────────────────────┘
      ▲ 专用 Chrome profile（有界面）          ▲ ~/bin/dreamina（官方 CLI）
      │ jimeng.jianying.com                   │
      ▼                                       ▼
 ai_videos/**/renders/*.mp4 + *.jimeng.json    ai_videos/**/_candidates/{key}/*.png
```

- **调度器**：负责 queued → 准备 → 提交，维护「远端同时渲染数 ≤ 上限」和最小提交间隔。
- **BrowserActor**：单个 async task 从命令队列里串行消费所有 UI 动作。取消只在两个动作之间的检查点生效。
- **backend 路由**：按全局 config 的 `routing` 决定视频 / 图片分别走哪个 backend。请求需要的能力由能力矩阵在**预检阶段**检查，运行时不做降级。

---

## 5. Functional requirements

> 编号即验收锚点。「config 键」表示该值必须来自 config，不能写死在代码里（FR-5）。

### 5.1 配置

**FR-1 全局 config。** 路径 `projects/jimeng_web_bridge/config/global.toml`，进 git，只放非机密、与机器无关的值。机器专属值和机密从仓库根目录 gitignored 的 `.env` 读取（`JIMENG_BRIDGE_TOKEN`、`JIMENG_BRIDGE_PROFILE_DIR`、`DREAMINA_CLI_PATH`，均可选覆盖）。键与提议默认值：

| 键 | 默认 | 说明 |
|---|---|---|
| `server.host` / `server.port` | `127.0.0.1` / `8790` | host 只允许 127.0.0.1 / localhost |
| `routing.video` / `routing.image` | `web` / `cli` | 取值 `web` 或 `cli`，与能力矩阵一起在预检时校验 |
| `concurrency.max_remote_rendering` | `3` | 同时在即梦渲染的条数 |
| `pacing.min_submit_interval_s` | `15` | 两次提交之间的最小间隔（固定值，不做随机化） |
| `wait.timeout_h` | `12` | 超时后进入 `paused_needs_human(wait_timeout)` |
| `confirm.allow_http_auto` | `false` | 是否允许 HTTP 调用传 `auto_confirm` |
| `budget.auto_confirm_daily_credits` | `2000` | 仅约束 auto_confirm 的批次 |
| `browser.channel` | `chrome` | `chrome` 或 `chromium` |
| `browser.profile_dir` | `projects/jimeng_web_bridge/.data/chrome_profile` | |
| `browser.start_url` | `https://jimeng.jianying.com/ai-tool/generate?type=video` | workspace 参数可在此填写 |
| `canary.interval_min` | `30` | 另外每批开始前必跑一次 |
| `cli.path` / `cli.min_version` | `~/bin/dreamina` / `1.4.5` | |
| `notifications.toast` | `true` | |
| `model_limits.*` | 见下表，带 `as_of = 2026-09-13` | 预检用的能力矩阵 |
| `price_table.*` | 带 `as_of` | 只作静态预估兜底 |

`model_limits` 提议默认值：

| 模型键 | backend | 时长 s | 分辨率 | 图 / 视频 / 音频上限 | 主体 |
|---|---|---|---|---|---|
| `seedance2.5` | web | 4–30 | 480p, 720p | 30 / 10 / 10（页面称最多 50 个参考素材；以 stage-6 探针为准） | 支持 |
| `seedance2.0_vip` | web, cli | 4–15 | 720p, 1080p | 9 / 3 / 3 | web 支持，cli 不支持 |
| `seedance2.0fast_vip` / `seedance2.0` / `seedance2.0fast` | web, cli | 4–15 | 720p | 9 / 3 / 3 | web 支持，cli 不支持 |
| `seedream5.0`（及 3.0–4.7） | cli | — | 2k, 4k（3.x 为 1k, 2k） | image2image 1–10 张 | — |

**FR-2 每剧 config。** 路径 `ai_videos/{drama_root}/jimeng_config.toml`，进 git。drama root 按 `series.json` 标记规则判定（FR-10）。结构与提议默认值：

- `[drama]`
  - `abbrev`：系列剧成员默认取集目录名（`hy3`）。独立剧留空，空值时预检报错并提示「需要你确认」。
- `[entities]`
  - `name_template = "{abbrev}_{character_name}"`，其中 `character_name` 是角色卡目录去掉 `c{N}_` 前缀后的中文名。
  - `overrides = { "c1_砌炉的老人" = "hy3_主角" }`，用来映射已有主体。
  - `source_images`：建主体时上传哪些角色卡文件的 glob，默认 `["{card_dir}/*-1.png"]`。
  - `description_from`：主体描述的来源，默认取角色卡的锁定描述符。
- `[references]`
  - `rules`：有序数组，每项 `{label_glob, kind, resolver}`，默认值见 FR-8 的表。
  - `overrides`：`{ "{参考项名}" = "ai_videos/…/file.png" | "entity:{主体名}" }`。
  - `search_exclude = ["_deleted", "_candidates", "renders", "previz/frames"]`。
- `[video]`
  - `model = "seedance2.5"`、`resolution = "720p"`、`count = 1`、`reference_mode = "全能参考"`；
  - `ratio_source = "shot"`、`duration_source = "shot"`（取 shot md 里的 `比例:` / `时长:`）；
  - `negative_prompt = "platform_field_or_omit"`：取值 `platform_field_or_omit | omit | fail`，**永不并入正向 prompt**。
- `[image]`
  - `model = "5.0"`、`resolution = "2k"`、`command = "auto"`（没有参考图用 text2image，有参考图用 image2image）；
  - `ratio`：按主体类型给默认（characters 3:4、scenes 16:9、props 1:1），可逐块覆盖。
- `[outputs]`
  - `video_name = "{shot}_{ts}{_i}.mp4"`，写在 `{shot_dir}/renders/` 下；
  - `image_candidates_dir = "_candidates/{key}"`；
  - `image_on_existing = "archive"`：取值 `archive | fail`，archive 表示移入 `ai_videos/_deleted/…`。
- `[precheck]`
  - `prompt_max_chars = 5000`（沿用仓库契约；网页硬上限未知，由 FR-31 的填写校验兜底）；
  - `entity_name_max_chars = 20`；
  - `estimate_deviation_warn_pct = 20`。

**FR-3 提议默认 config（`DramaConfigCommand.propose`）。**
- 扫描剧目录生成上述结构的提议：列出所有角色卡、所有参考项名，以及它们按默认规则的解析结果。
- **已存在的 config 不会被覆盖**。这种情况下返回逐键 diff 建议。
- 跨集复用的角色卡（`.link.json` 指向其他集）：主体名默认沿用来源集缩写（hy2 复用 hy1 的人 → `hy1_…`）。
- 每个「需要用户确认」的键在提议结果里带 `needs_confirmation: true` 和原因，例如「独立剧缺缩写」「期望主体名与即梦现有主体不一致」「参考项多重匹配」。

**FR-4 config 读写。**
- 使用 round-trip 解析，保留注释与键顺序。
- 保存前做 schema 校验；非法值拒绝并指出具体字段路径。
- 写入是原子的：临时文件 → rename。
- UI 保存时带上读取时的内容 hash；文件已被别处改动则返回 409。

**FR-5 规则不写死。** 凡涉及剧、命名、路由键、映射、默认档位、阈值的规则，一律从 config 读取。validation 用一张「config schema 键 ↔ 本 spec FR」对照表做契约测试。

### 5.2 输入与请求规范化

**FR-6 `GenerationRequest` 值对象（frozen）。** 字段：
- `kind`：`video | image`；
- `prompt`：逐字节原文；
- `references`：有序 `ReferenceItem{name, label, kind: image|video|audio|entity|first_frame, resolved_path | entity_name, sha256}`；
- `negative_prompt`：可选；
- `params`：`{model, ratio, duration_s, resolution, count, reference_mode}`；
- `output_target`；
- `source`：`{type: raw|shot|asset, path, block_key}`。

三种入口都规范化成它。

**FR-7 原始入口。** 接收 `prompt` + 有序文件路径列表 + 可选主体名列表 + `params` + `output_dir`。文件路径必须落在 `ai_videos/` 沙箱内。

**FR-8 shot 适配（`ShotPromptReader`）。**
- `## 视频 prompt` 下第一个 ```text 围栏里的**全部原文**就是 prompt，一个字节都不改（包括首行 `shotNN` 和 `参考:` 行本身）。
- 其后紧跟、以「反向提示词」为标题的 ```text 围栏作为 `negative_prompt`。
- 在围栏内解析：
  - `比例:` → `ratio`；
  - `时长:`（`22秒` / `22s`）→ `duration_s`；
  - `参考:` 行里每个 `` `{name}({label})=>@` `` 按出现顺序变成一个 `ReferenceItem`。
- 解析按 config `references.rules` **自上而下取第一条匹配**。提议默认规则（依据全仓 271 条 `参考:` 行的统计）：

| label_glob | kind | resolver |
|---|---|---|
| `场景参考图*`、`*锚点`、`角色参考图`、`单位参考图`、`场景主体`、`物件主体` | image | `stem_in_drama`：在剧根和 `{series}/_series/` 里找 stem 等于 `name` 的图片，`.link.json` 视为目标文件 |
| `Seedance 人物 entity`、`人物主体` | entity | `entity`：`name` → 角色卡目录 → `entities` 模板 / overrides → 主体名 |
| `previz灰模视频`、`3D预演视频` | video | `stem_in_shot`：在本镜目录里找 stem 等于 `name` 的视频 |
| `上一镜末帧` | first_frame | `prev_shot_lastframe`：`shots/shot{NN-1}/shot{NN-1}_lastframe.png` |
| `*声音` | audio | `stem_in_drama` |

- 以下情况一律是**预检错误**，并在错误里指出应当填写的 config 键（`references.overrides."{name}"` 或新增一条 rule）：
  - 某项找不到文件；
  - 匹配到多个文件；
  - label 没有命中任何规则；
  - 写成了已填槽位号（`=>@2` 这类旧写法）；
  - 没有括号的旧写法。

**FR-9 资产卡适配（`AssetCardReader`）。**
- 在 `characters/*`、`props/*`、`scenes/*` 的主体 md 里，只取**首行以路由键开头**的 ```text 块（`c1-1_…`、`p3-2_…`、`bg11-1_…`，规则 4b-A）。一块对应一个请求。
- 锁定描述符和负面词所在的裸围栏不当 prompt。
- 输出目标是该主体目录。`block_key` 就是路由键。
- 参考图（image2image）由 config 按块覆盖指定；默认没有参考图 → 走 text2image。

**FR-10 剧目录解析。**
- drama root 规则：`ai_videos/` 下含 `series.json` 的目录是系列，其下非 `_` 开头的子目录是剧；否则该目录本身就是剧。与 `projects/ai_video_management/libs/common/drama_ref.py` 语义一致，见 §8 divergence 1。
- `.link.json` 按 target 解析，拒绝逃出 `ai_videos/` 或指向 symlink 的目标。
- 所有文件读写都受仓库沙箱约束。

### 5.3 预检

**FR-11 静态预检（纯函数，不开浏览器、不调 CLI）。** 每条请求检查：
1. 每个参考文件存在、可读，并计算 sha256。
2. 参考种类和数量在所选模型的 `model_limits` 之内。
3. `duration_s`、`resolution`、`ratio` 属于该模型支持的范围。
4. 所选 backend 具备该请求需要的全部能力。例如路由到 `cli` 却用了主体、2.5 或 >15 s → 错误，不降级。
5. prompt 字数 ≤ `precheck.prompt_max_chars`。
6. 主体引用：名称 ≤ 20 字，且存在于最近一次主体同步的快照里。快照超过 24 h 给 warning；缺失则报错，并提示去主体对账页创建。
7. 输出目录可写，目标文件不会被覆盖。
8. 指纹去重（FR-24）命中时标注已有 job。
9. `negative_prompt` 策略为 `fail` 且平台没有负向框 → 错误。

结果分为 `ok` / `warning` / `error`。有 error 的条目不能进入确认。

**FR-12 预计积分。**
- 静态估算：`price_table` × 时长 × 数量，并标注 `as_of`。
- 可选的**浏览器预演**（FR-32）读取页面自己显示的预计积分。
- 两个值都展示；偏差超过 `estimate_deviation_warn_pct` 时高亮。

**FR-13 `BatchCommand.precheck(items, idempotency_key?)`。** 返回：
- `batch_id`；
- 逐条结果：解析后的参考项、主体、参数，以及 error / warning；
- 合计预计积分；
- `confirmation_token`：HMAC，签入 batch 内容摘要、合计预计积分、过期时间（30 min）；
- UI 确认页 URL。

batch 持久化为 `awaiting_confirm`。剔除 error 条目需要重新预检。

### 5.4 确认闸门

**FR-14 `BatchCommand.confirm(batch_id, token, confirmer)`。**
- token 单次有效，由服务端强制。内容摘要不一致或已过期 → 拒绝。
- `confirmer` 取值 `ui_human | mcp | http_auto`，连同确认时间一起入库。

**FR-15 确认入口。**
- **UI 确认页**是默认、推荐的确认方式。
- MCP 提供 `confirm_batch` 工具。README 明确要求**不要**把它加入 Claude Code 的 allow 列表，这样每次调用都要人工批准。
- HTTP 接受 `auto_confirm=true` 的前提是 `confirm.allow_http_auto = true`，并且当日 auto_confirm 累计预计积分 ≤ `budget.auto_confirm_daily_credits`。超出即拒绝。

**FR-16 硬不变量。** 没有经过确认的 batch 里的任何 job，无论从哪个入口（含 `browser_step`），都不能进入 `submitting`。

### 5.5 作业队列与状态机

**FR-17 `JobEntity` 状态机**（由实体方法守护，非法转移抛领域错误）：

```
queued → preparing → awaiting_submit_slot → submitting → generating → downloading → done
   ↘           ↘                ↘                ↘              ↘
   cancelled   paused_needs_human / failed（按 FR-21 分级）
```

- 每次转移都记录 `{from, to, at, reason?}`。
- `preparing` 的子步骤依次为 `set_params → upload → fill → preview`，各自带进度。

**FR-18 调度。**
- UI 动作全局串行，只有一个 BrowserActor。
- 状态为 `generating` 的 job 数 ≤ `concurrency.max_remote_rendering`。
- 两次提交间隔 ≥ `pacing.min_submit_interval_s`。
- 页面提示「并行任务已达上限」时，把 job 放回 `awaiting_submit_slot` 等待，**不算失败**。
- 同一个 backend 被暂停时，只停该 backend 的队列。

**FR-19 崩溃安全提交。**
- **点击「生成」之前**先持久化 `submitting` 和指纹。
- 服务启动时：
  - 发现 `submitting` → `paused_needs_human(restart_during_submit)`，**绝不自动重提**；
  - 发现 `generating` / `downloading` → 恢复轮询或下载。

**FR-20 重试边界。**
- 提交这一步零自动重试。
- `set_params` / `upload` / `fill` / `download` 各自最多重试 3 次。
- 审核被拒的 job 进入 `failed(moderation_reject)`，不改写 prompt。

**FR-21 暂停分级。**
- **队列级**（暂停该 backend 整个队列，弹 toast，附截图）：`login_expired`、`captcha_or_risk_popup`、`insufficient_credit`、`page_contract_broken`、`browser_lost`、`cli_login_required`、`compliance_confirmation_required`。
- **作业级**（只影响该 job，队列继续）：`moderation_reject`、`real_face_rejected`、`upload_rejected`、`fill_mismatch`、`wait_timeout`、`restart_during_submit`。

**FR-22 取消。**
- 在 `submitting` 之前取消 → `cancelled`，不花积分。
- 之后取消 → 停止等待和下载；响应和 UI 都明确显示「积分不会退还」。

**FR-23 恢复。** `resume_job` 和 `resume_queue` 在恢复前先跑一次 canary（web）或 `user_credit`（cli）。自检失败时保持暂停，并返回原因。

**FR-24 幂等与去重。**
- 调用方可以带 `idempotency_key`：同 key、同内容 → 返回首次结果；同 key、不同内容 → 409 / `isError`。key 保留 24 h。
- 服务端指纹 = `sha256(prompt + 每个参考项的 sha256 或主体名 + negative_prompt + params + output_target)`。同指纹已有非终态或 `done` 的 job → 直接返回那个 job，除非请求带 `reroll: true`（记录 attempt 序号）。

### 5.6 WebUiBackend（Playwright，有界面）

**FR-25 会话。**
- 常驻单个 persistent context，channel 和 profile 从 config 读。
- 启动失败分类为 `profile_in_use` / `browser_missing` / `launch_timeout`，**不自动删除锁文件**。
- 记录 `browser.version`，以及页面 query 里的 `web_version`。

**FR-26 登录。**
- 进入即梦后检测登录标志。未登录 → `login_required`，窗口置前，弹 toast，等待用户手动登录。
- service 不向页面输入任何凭据。

**FR-27 canary（只读）。**
- 触发时机：每个 batch 开始执行前、每 `canary.interval_min` 分钟、恢复前。
- 检查项：登录标志；创作类型、模型、参考模式、比例·分辨率·数量、时长控件存在；TipTap 编辑器存在；上传入口存在；生成按钮存在；预计积分文本可读；最近一次状态响应可以被截获并解析。
- 任一失败 → `page_contract_broken`。
- **canary 绝不点击生成。**

**FR-28 PageMap。**
- 所有 selector 和流程步骤集中在一个模块里，标注已验证的 `web_version`。
- 优先按角色和文本定位；**禁止坐标点击**。页面会自动滚动，所以要先定位到记录，再在记录内部找控件。

**FR-29 设置参数。**
- 按请求依次设置：创作类型=视频生成、模型、参考模式=全能参考、比例、分辨率、数量、时长。
- 每设置一项就读回控件显示值校验；不一致 → 重试，仍不一致 → `page_contract_broken`。

**FR-30 上传。**
- 按参考项顺序上传非主体项。
- 平台上显示的素材名必须等于参考项 `name`：必要时先把文件复制到临时目录，改名为 `{name}{ext}` 再上传。
- 等待页面给出完成信号，具体信号在 stage-6 探针中确定。
- 上传被拒 → `upload_rejected`。

**FR-31 填写。**
- 以 prompt 中每个 `=>@` 的位置切段。
- 文本段用可切换的插入策略写入（`insert_text` / `type` / `execCommand`，由 canary 实测选定）。
- 每个 `=>@` 处的 `@` 替换为对应参考项的 mention：输入 `@` → 按名过滤 → 点选候选项。候选项是上传素材的 stem，或主体名。
- 填完后校验两件事：
  - 编辑器纯文本（规范化空白，mention 以名称计）等于期望文本；
  - mention 节点序列等于期望序列。
- 不一致 → 清空重填一次；仍不一致 → `fill_mismatch`，**绝不提交**。
- 负向提示词：按 `video.negative_prompt` 策略处理，平台有负向输入框就填，没有就省略并记 warning。

**FR-32 预演。**
- 填写完成后，截全页 + composer 局部两张图，读取页面显示的预计积分，存入 job artifacts。
- `browser_step(op=preview)` 到这一步为止。

**FR-33 提交。**
- 只对已确认的 job 执行（FR-16），并满足 FR-18 的并发与间隔。
- 点击前持久化 `submitting`。
- 点击后被动截获提交响应，拿到平台侧任务标识 → `generating`。截获不到时，在历史记录里找「提交时刻之后、prompt 前缀一致」的最新一条来对账；对不上 → `paused_needs_human(restart_during_submit)`。

**FR-34 状态观察。**
- 在 context 级只读监听 `get_history_queue_info` 和 `get_history_by_ids` 的响应。解析器是纯函数，带版本号和 schema 校验。
- 进度百分比、排队信息、完成或失败状态写入 job。
- body 读取失败要计数；解析连续失败超过阈值 → `page_contract_broken`。

**FR-35 下载。**
- 完成后取**会员无水印原片**。用页面下载控件还是结果 URL，在 stage-6 探针中确定，并证明两者一致。
- 流程：写临时文件 → 校验 size、sha256，且 ffprobe 能读出预期时长和比例 → 原子 rename 到目标 → 写 sidecar（FR-45）。
- 从「详细信息」读取实际消耗积分，写入 job 和 sidecar。

**FR-36 失败现场。** 只有在失败或暂停时才保留：截图 + DOM 快照 + 该 job 的 trace 片段，路径入库。成功的 job 只保留 FR-32 的预演截图。

**FR-37 浏览器丢失。** 收到 context、page 的 close 或 crash 事件 → `browser_lost`：暂停 web 队列 → 重建 context → 检查登录 → 对账所有 `generating` 的 job。

### 5.7 DreaminaCliBackend（官方 CLI）

**FR-38 调用范围。**
- 只用文档化命令：`text2image`、`image2image`、`query_result --submit_id --download_dir`、`list_task`、`user_credit`、`version`。
- 以子进程方式调用，参数用列表形式传入，不经 shell 拼接。
- 解析 JSON 输出。以下情况映射到暂停原因：非零退出码、未登录、`AigcComplianceConfirmationRequired`。

**FR-39 生命周期。**
- 提交 = 执行生成命令（不带或只带很短的 `--poll`），拿到 `submit_id` 立即持久化 → `generating`。
- 之后轮询 `query_result`，完成后 `--download_dir` 下载到临时目录 → 同 FR-35 校验 → 落盘到 FR-44 的候选目录。

**FR-40 登录。** CLI 未登录或登录失效 → `cli_login_required`，暂停 CLI 队列。UI 提示用户自己运行 `dreamina login`，service 不代为登录。

**FR-41 版本。** 启动时执行 `dreamina version` 并记录。低于 `cli.min_version` → warning。

### 5.8 产物与记录

**FR-42 视频落点。** `{shot_dir}/renders/{video_name}`，默认 `shot02_20260913-181500.mp4`；`count > 1` 时加 `_1`…`_N`。永不覆盖已有文件。

**FR-43 图片落点。**
- 候选图写入 `{subject_dir}/_candidates/{key}/{ts}_{i}.png`。
- `promote(candidate)` 把选中的候选复制为 `{subject_dir}/{key}.png`。已有同名文件时按 `image_on_existing` 处理：`archive` 表示先移入 `ai_videos/_deleted/{原相对路径}.{ts}.png`。

**FR-44 sidecar。** 每个产物旁边写 `{产物文件名}.jimeng.json`，进 git。字段：
- 任务：`job_id`、`batch_id`、`backend`；
- 来源：`source{type, path, block_key}`、`prompt_sha256`、`negative_prompt_sha256`；
- 参考：`references[{name, kind, path | entity, sha256}]`、`params`；
- 平台：`platform_task_id`、`credits_estimated{static, page}`、`credits_charged`；
- 时间与确认：`submitted_at`、`finished_at`、`confirmer`；
- 版本：`web_version | cli_version`、`browser_version`；
- 产物：`output{sha256, size, duration_s?, width, height}`。

**FR-45 原样保存。** 下载的字节不做任何修改，不剥离元数据（保留平台写入的隐式 AI 标识）。

**FR-46 生成历史。** `HistoryQuery` 按剧、镜、资产主体、日期查询 job，给出预估与实扣积分、每日合计。数据同时对账 `commerce` 余额：批次开始和结束各读一次余额，写入 batch。

### 5.9 主体

**FR-47 同步。** `EntityCommand.sync()` 打开主体页，被动读取 `dreamina_subject/get` 的响应，生成本地主体快照（名称、缩略图 URL、修改时间、同步时间）。

**FR-48 对账（`EntityQuery.reconcile(drama?)`）。** 期望主体名来自各剧 config（模板 + overrides + 跨集来源）。每项输出三种状态之一：`mapped` / `missing_on_platform` / `unmapped_on_platform`（即梦上有、任何剧都没有映射到）。

**FR-49 创建（`EntityCommand.create(drama, character_dir)`）。**
- 预检：名称 ≤ 20 字；`source_images` 存在；图片若疑似写实真人，给 warning。
- 在 UI 确认页确认；描述可以在确认页编辑。
- 执行：进入「新建主体」表单 → 上传参考图 → 填名称和描述 → 保存 → 再同步一次，验证主体已存在。
- 同名主体已存在 → 直接复用，不再创建。

**FR-50 不做破坏性操作。** service 永不改名、删除或覆盖即梦上已有的主体。

### 5.10 HTTP API（每个 route 恰好对应一个 Query / Command 方法）

| Method | Path | 映射 |
|---|---|---|
| GET | `/api/health` | `SessionQuery.health` |
| GET | `/api/session` | `SessionQuery.status`（web 登录、canary、浏览器版本；cli 登录、版本、余额） |
| POST | `/api/session/canary` | `SessionCommand.run_canary` |
| POST | `/api/batches` | `BatchCommand.precheck` |
| GET | `/api/batches/{id}` | `BatchQuery.get` |
| POST | `/api/batches/{id}/confirm` | `BatchCommand.confirm` |
| GET | `/api/jobs` | `JobQuery.list`（按状态、剧、批次过滤） |
| GET | `/api/jobs/{id}` | `JobQuery.get` |
| POST | `/api/jobs/wait` | `JobQuery.wait`（有界等待，≤ 90 s） |
| POST | `/api/jobs/{id}/cancel` | `JobCommand.cancel` |
| POST | `/api/jobs/{id}/resume` | `JobCommand.resume` |
| POST | `/api/queues/{backend}/pause` | `JobCommand.pause_queue` |
| POST | `/api/queues/{backend}/resume` | `JobCommand.resume_queue` |
| POST | `/api/jobs/{id}/steps/{op}` | `BrowserStepCommand.run`，op ∈ `set_params \| upload \| fill \| preview \| submit`；`submit` 同样受 FR-16 约束 |
| GET | `/api/artifacts/{job_id}/{name}` | `ArtifactQuery.get`（截图，路径受沙箱约束） |
| GET | `/api/dramas` | `DramaConfigQuery.list_dramas` |
| GET | `/api/dramas/{drama}/config` | `DramaConfigQuery.get` |
| POST | `/api/dramas/{drama}/config/propose` | `DramaConfigCommand.propose` |
| PUT | `/api/dramas/{drama}/config` | `DramaConfigCommand.save` |
| GET / PUT | `/api/config/global` | `GlobalConfigQuery.get` / `GlobalConfigCommand.save` |
| POST | `/api/entities/sync` | `EntityCommand.sync` |
| GET | `/api/entities/reconcile` | `EntityQuery.reconcile` |
| POST | `/api/entities` | `EntityCommand.create` |
| GET | `/api/history` | `HistoryQuery.list` |
| POST | `/api/candidates/promote` | `CandidateCommand.promote` |

- `{drama}` 是 URL 编码后的剧根相对路径。
- 业务错误统一返回 `{error_code, message, hint, config_key?}`。

### 5.11 MCP（`/mcp`，Streamable HTTP，与 HTTP 同进程）

**FR-51 工具集**（约 10 个）：

| 工具 | 映射 |
|---|---|
| `session_status` | `SessionQuery.status` |
| `precheck_batch` | `BatchCommand.precheck`；items 可以是 shot 路径、资产块（`{card_path, key}`）或原始请求 |
| `confirm_batch` | `BatchCommand.confirm` |
| `wait_jobs` | `JobQuery.wait` |
| `list_jobs` | `JobQuery.list` |
| `cancel_job` | `JobCommand.cancel` |
| `resume` | `JobCommand.resume` / `resume_queue`，二选一由参数决定 |
| `browser_step` | `BrowserStepCommand.run` |
| `entities` | `EntityQuery.reconcile` / `EntityCommand.sync` |
| `get_screenshot` | `ArtifactQuery.get` |

**FR-52 调用约束。**
- 每个工具在 90 s 内返回。`wait_jobs` 在等待期间每 ≤ 30 s 发一次 `notifications/progress`，到时间就返回当前快照和建议的下一步。
- 返回内容：`structuredContent` + 同内容的 JSON 文本。截图只给路径 + 长边 ≤ 768 px 的缩略图。
- 业务错误用 `isError: true`，并附上可以照做的建议（例如「在 UI 确认页确认：{url}」「在 config 填写 `references.overrides."砌炉的老人"`」）。
- 不使用 elicitation，也不依赖 MCP tasks 扩展。

**FR-53 接入。** README 给出 `.mcp.json` 片段：`type: http`、`url: http://127.0.0.1:8790/mcp`、`headers.Authorization: Bearer ${JIMENG_BRIDGE_TOKEN}`、`timeout: 120000`，并写明 `confirm_batch` 不要加入 allow 列表。

### 5.12 本地管理 UI（`apps/ui/`，React，中文界面，浅色主题）

**FR-54 页面：**
1. **会话**：web 登录状态、canary 结果（逐项）、浏览器与 `web_version`；CLI 登录、版本、余额；按钮「打开浏览器窗口 / 运行 canary」。
2. **剧 config**：
   - 剧列表（系列折叠显示）；
   - 表单编辑 + 原文 TOML 视图；
   - 「生成默认 config」；
   - 需要确认的项置顶标黄；
   - 保存前做 schema 校验；遇到 409 冲突给出提示；
   - 参考项解析预览：列出每个 shot 的参考项、解析结果和错误。
3. **批次确认**：逐条展示解析后的参考项（缩略图）、主体、参数、预计积分（静态 / 页面），合计积分；error 条目不可确认；「确认并开始」按钮。
4. **队列看板**：按状态分列；每个 job 显示子步骤进度、平台进度百分比；暂停原因 + 截图；取消、恢复、分步操作按钮；取消前明确「提交后取消不退积分」。
5. **历史与积分**：按剧、镜、主体、日期筛选；预估与实扣积分；每日合计；图片候选网格 +「选定」（FR-43）。
6. **主体对账**：即梦主体快照 × 各剧期望名，显示三态；缺失项「创建」（走确认）。
7. **全局设置**：`global.toml` 表单编辑，机密字段不展示。

**FR-55 UI 约束。**
- 浅色主题（development.md §7）；数据加载失败时显示错误态，不渲染空白页。
- 所有「花积分 / 写即梦」的按钮都要经过确认页，或二次确认。

### 5.13 通知

**FR-56 Windows toast。**
- 触发：队列级暂停、batch 全部完成、需要登录。
- 点击 toast 打开 UI 的对应页面。
- toast 只是尽力而为：发送失败只记录日志，不影响作业；作业状态才是唯一真相。

---

## 6. Non-functional requirements

**部署与运行**
- 以当前登录用户的身份，在交互桌面会话里运行（不做 Windows Service）。
- 入口：`make run`（单进程：API + MCP + 已构建的 UI）、`make ui-build`、`make test`、`make canary`（对真实站点做只读 canary）。
- Python 依赖走 pip + `.venv`，不依赖 `uv`（validation/development.md §6）。
- 只提供一种运行模式。README 不宣传 Vite dev server 模式。

**安全**
- 只绑定 `127.0.0.1`；Host 与 Origin 做 allowlist，非法请求返回 403。
- 非同源客户端（MCP、脚本）必须带 `Authorization: Bearer {JIMENG_BRIDGE_TOKEN}`。同源 UI 通过 Origin 校验放行。
- token 只存在于 `.env`，不写日志、不进 sidecar。
- 文件访问沙箱：读限于仓库 `ai_videos/`；写限于 `ai_videos/` 下的目标目录和 `projects/jimeng_web_bridge/.data/`；拒绝 symlink 和 `..`。
- CLI 子进程参数用列表传入，不经 shell。

**账号风险（用户知情接受）**
- README 首屏写明：即梦用户协议 5.1 禁止用自动化工具接入，付费协议 6.5 / 8.2 可以作废权益或封号。本项目为本人账号、本机、个人自用；风险由用户承担。
- 设计上压小暴露面：单账号、单 profile、只在本机提供服务、固定提交间隔、并发上限、auto_confirm 预算、提交零自动重试、零对抗检测；图片走官方 CLI。
- README 注明：上传素材按用户协议 9.3 授权平台用于优化模型；写实真人素材可能被拒。

**可靠性**
- SQLite 开 WAL，service 是唯一写者。
- 重启恢复遵循 FR-19 / FR-23；任何情况下都不会自动重复提交。
- 所有下载都经过临时文件 → 校验 → 原子 rename。

**性能**
- MCP / HTTP 调用 ≤ 90 s 返回；查询类接口在 1000 条 job 规模下 p95 ≤ 500 ms。
- UI 首屏 ≤ 2 s（本机）。
- 单 job 准备阶段（set_params → preview）目标 ≤ 3 min，属观测指标，不作硬性要求。

**可观测**
- 结构化 JSONL 日志写入 `.data/logs/`。
- 每个 job 的状态转移入库；失败现场按 FR-36 保存。

**可测性**
- **离线 Fake 即梦站点**：本地静态 HTML fixture 模拟 composer（TipTap 编辑器、@ 候选、上传入口、各参数控件、预计积分、生成按钮）和状态轮询接口，可以注入验证码弹窗、审核拒绝、并发上限提示、登录失效。WebUiBackend 的 e2e 全部跑在它上面，不花积分。
- **fake `dreamina` 可执行脚本**：覆盖 CLI adapter 的成功、失败、未登录、合规确认路径。
- 真实站点只跑只读 canary（`make canary`，手动触发）。

**代码规范**
- 遵循 `.claude/agent_refs/project/development.md` §1–7：apps/ + libs/ DDD + CQRS、`dependency_injector`、强类型、单一职责、测试目录镜像源码树。
- README 用中文，随功能变更同步更新。

---

## 7. 项目布局

```
projects/jimeng_web_bridge/
├── README.md  Makefile  pyproject.toml  requirements.txt  .gitignore(.data/, apps/api/static/, apps/ui/node_modules/)
├── config/global.toml
├── apps/
│   ├── api/  main.py · app_factory.py · container.py
│   │   ├── routes/{session,batch,job,browser_step,artifact,drama_config,global_config,entity,history,candidate}__route.py · __init__.py
│   │   └── mcp_tools/{session,batch,job,browser_step,entity,artifact}__tool.py · __init__.py   ← divergence 1
│   └── ui/   (Vite + React + TS；构建产物输出到 apps/api/static/)
├── libs/
│   ├── common/        enums.py(JobState, PauseReason, BackendKind, RefKind) · drama_ref.py · paths.py
│   ├── domain/
│   │   ├── entities/      generation_job__entity.py · batch__entity.py
│   │   ├── value_objects/ generation_request__valueobject.py · reference_item__valueobject.py · generation_params__valueobject.py
│   │   │                  drama_config__valueobject.py · global_config__valueobject.py · model_limits__valueobject.py
│   │   │                  fingerprint__valueobject.py · confirmation_token__valueobject.py · precheck_result__valueobject.py
│   │   │                  （不设 domain services：静态预检是 precheck_result__valueobject.py 旁的纯函数模块 precheck__valueobject.py）
│   │   ├── errors/        job__error.py · batch__error.py · precheck__error.py · config__error.py
│   │   └── repositories/  job__repository.py · batch__repository.py · drama_config__repository.py
│   │                      generation_backend__repository.py (Protocol：GenerationBackend 端口)
│   ├── application/
│   │   ├── commands/  batch__command.py · job__command.py · browser_step__command.py · drama_config__command.py
│   │   │              global_config__command.py · entity__command.py · session__command.py · candidate__command.py
│   │   ├── queries/   batch__query.py · job__query.py · drama_config__query.py · global_config__query.py
│   │   │              entity__query.py · session__query.py · history__query.py · artifact__query.py
│   │   ├── dtos/      {同名}__dto.py
│   │   └── mappers/   {同名}__mapper.py
│   └── infrastructure/
│       ├── clients/   jimeng_browser__client.py(BrowserActor) · jimeng_page__map.py · dreamina_cli__client.py · toast__client.py
│       ├── readers/   shot_prompt__reader.py · asset_card__reader.py · drama_tree__reader.py · jimeng_response__reader.py
│       │              drama_config__reader.py · global_config__reader.py
│       ├── writers/   job_store__writer.py(SQLite) · output__writer.py · drama_config__writer.py · artifact__writer.py
│       │              web_ui_backend__writer.py · dreamina_cli_backend__writer.py  (GenerationBackend 实现)
│       ├── daos/      job__dao.py · jimeng_history__dao.py · dreamina_result__dao.py · entity_snapshot__dao.py
│       ├── errors/    jimeng_browser__error.py · dreamina_cli__error.py · config_io__error.py
│       └── middleware/ host_origin__middleware.py · bearer_token__middleware.py
├── tests/  (镜像 apps/ + libs/；fixtures/fake_jimeng_site/ · fixtures/fake_dreamina/ · fixtures/real_shots/ 真实 shot md 副本)
└── .data/  (gitignored：bridge.db · chrome_profile/ · artifacts/ · logs/ · tmp/)
```

---

## 8. Divergence notes

1. **MCP 工具层级。** `development.md` §1 没有定义 MCP 的角色，本项目新增 `apps/api/mcp_tools/{aggregate}__tool.py`，规则与 routes 相同：每个工具只做传输包装，恰好映射一个 Query / Command 方法；和路由一样经 `container.wire()` 注入，每个工具文件与它的 provider 在同一个变更里落地（development.md §5）。
2. **剧根解析重复实现。** CLAUDE.md 规定剧根只在 `ai_video_management/libs/common/drama_ref.py` 一处解析，但项目之间禁止互相 import。本项目在 `libs/common/drama_ref.py` 按**同一条 `series.json` 标记规则**重新实现（同样不按路径深度推断），并用契约测试针对真实 `ai_videos/` 树断言：`huangye_shenghuo/hy3` 是 3 段、`wushen_juexing` 是 2 段、`_series` / `_deleted` 不是剧。以后如果把它提升为仓库共享工具，这里跟着改。
3. **运行时数据落在项目目录下的 `.data/`（gitignored）。** 这是 service 的运行数据，不是 CLAUDE.md 意义上的 workflow 状态面。
4. **新增的 `ai_videos` 结构文件。** 剧根的 `jimeng_config.toml`，以及产物旁的 `*.jimeng.json` sidecar。文件名是英文，内容可以含中文，都进 git。

---

## 9. Acceptance criteria summary（完整条目在 stage 5）

1. **离线端到端**：在 Fake 即梦站点上，用 hy3 的真实 `shot02.md` 走完 precheck → UI 确认 → 执行，结果如下：
   - 模型、比例、时长控件被设成 2.5 / 16:9 / 22s；
   - 4 个参考项按 stem 上传，主体 @ 到 `hy3_主角`（由 config override 映射）；
   - 编辑器校验通过；
   - 产物落到 `renders/shot02_*.mp4` + sidecar，字段齐全。
2. **确认闸门**：未确认的 batch 无法进入 `submitting`，涵盖所有入口（HTTP / MCP / browser_step）；token 过期、被篡改或重复使用都会被拒绝。
3. **崩溃安全**：在 `submitting` 状态杀掉进程后重启 → `paused_needs_human(restart_during_submit)`，全程只点击过一次生成。
4. **暂停分级**：注入验证码弹窗 → web 队列暂停并弹 toast；注入审核拒绝 → 只有该 job 失败，其余继续。
5. **并发与间隔**：同时处于 generating 的 job ≤ 3；两次提交间隔 ≥ 15 s；注入「并行已达上限」提示 → job 回到等待，不算失败。
6. **幂等**：同内容重复预检和确认返回同一个 job；`reroll: true` 生成新的 attempt。
7. **config**：对 hy3 执行 propose，得到 `abbrev = hy3`，并标出主体名冲突需要确认；保存后注释保留；非法值被拒绝；并发修改返回 409。
8. **解析错误可操作**：旧写法 `=>@2`、多重匹配、未知 label → 预检错误，并给出应当填写的 config 键。
9. **CLI 出图**：fake dreamina 下完成 text2image → 候选落盘 → promote 为 `{key}.png`，旧文件归档；CLI 未登录时 CLI 队列暂停。
10. **MCP 调用约束**：所有工具 ≤ 90 s 返回；`wait_jobs` 带进度通知；业务错误返回 `isError` + 建议。
11. **安全**：非 127.0.0.1 的 Host、非法 Origin、缺少 token → 403；路径逃逸 → 拒绝。
12. **UI**：七个页面在真实浏览器里渲染，覆盖加载成功态和错误态；批次确认页的合计积分与 API 一致。
13. **真实站点只读 canary**：人工触发，用户登录状态下逐项通过，全程不点击生成（手工 walkthrough）。

---

## 10. Open questions（stage 6 开工时的真实站点只读探针，逐项写回 PageMap 和本 spec）

1. **下载**：入口在「⋯」菜单还是视频上的图标按钮？会员下载是否无水印？结果 CDN URL 与下载文件是否一致？
2. **上传**：完成信号是什么？上传后的素材在 @ 候选列表里显示的名字，是否就是文件 stem？
3. **提交**：提交接口的 URL 与响应里的平台任务标识字段是什么？`get_history_by_ids` 中进度、状态、结果的字段是什么？
4. **负向框**：Seedance 2.5 全能参考下是否有负向提示词输入框？（决定 `negative_prompt` 策略的实际效果。）
5. **2.5 的真实上限**：参考数量（页面称 50，第三方资料称 30 / 10 / 10）、1080P 是否可选、prompt 字数硬上限。`get_common_config` 的响应能否直接作为能力矩阵的数据来源？
6. **主体表单**：能否上传视频（turntable）？「添加角色」是什么？描述有无字数上限？
7. **CLI**：1.4.18 是否新增 Seedance 2.5、主体或 30 s 支持？CLI 余额 8712 与网页「1.1万」是否为同一积分池？（影响 `routing` 与预算口径。）
8. **与 `ai_video_management` 的兼容**：`MediaRenamer` / `rename_drama` 会不会改名 `renders/` 下的产物或 `_candidates/`，导致 sidecar 失配？如会，本项目的命名改为它能接受的形式（通过 config 调整，不改 webapp）。
9. **Claude Code 实测**：本机 Claude Code 版本上，Streamable HTTP 工具调用的实际截断点，以及 `timeout: 120000` 是否生效。
