# Spec — jimeng_web_bridge

Run: jimeng_web_bridge-20260913-093603
task_type: development · target: `projects/jimeng_web_bridge/`
Compiled from: `user_input/revised_prompt.md` + `interview/qa.md`（含 post-research decisions 与 stage-5 decisions）+ `findings/dossier.md`（5 个 angle）
Version: **v2**（在 stage-5 validation 暴露的冲突和缺口基础上修订；每一处改动的出处见 §11 Revision log）

---

## 1. Goal

在本机构建一个独立的常驻 service `jimeng_web_bridge`，把即梦的生成能力做成人、Claude、自动化脚本都能调用的接口：参考素材 → prompt → 参数 → 提交 → 等待 → 取回并落盘，全链路打通。对外有三种形态：HTTP API、MCP、本地管理网页。

**两条生成通道：**
- **视频走网页。** 驱动用户已登录的即梦网页出片（Seedance 2.5、16–30 s、@主体、多参考）。做法是真实 UI 操作，状态只被动读取页面自己发出的网络响应。
- **图片走官方 CLI。** Seedream 出图调用官方 `dreamina` CLI。

两条通道共用下面这些能力：
- 输入适配：原始参数 / `shotNN.md` / 资产卡；
- 静态预检，给出预计积分；
- 确认闸门：**只有本地网页里的人能确认，未经确认不花一分积分**；
- 作业队列：有并发上限、可暂停恢复、重启后不丢；
- 结果原子落盘到仓库对应目录，并写 sidecar。

**config 规则：** 每部剧的路由键、命名、映射、默认值、校验阈值都放在这部剧自己的 config 里；账号级的阈值放在全局 config 里。service 先按默认值提议，用户在 UI 上查看和修改。

---

## 2. Out of scope（v1）

1. 网页上除「视频生成 · 全能参考」以外的模式：首尾帧、智能多帧、智能编辑、超长视频、Agent 模式、音乐、音频、数字人、动作模仿。承接镜的「本镜首帧（上一镜末帧）」按全能参考里的一个上传项处理。
2. 网页端图片生成。图片一律走官方 CLI，`routing.image` 不可配置。
3. 伪造或重放即梦内部接口，或主动请求平台 URL（包括用 `context.request` 直接拉结果 URL）。任何对抗检测手段也不做：stealth、指纹伪装、验证码求解、改 webdriver 标志、暴露给页面的 binding、CDP 调试端口。
4. 去水印，剥离元数据。
5. 多账号、账号轮换、远程部署、对 127.0.0.1 以外开放。
6. 自动改写 prompt 后重提。**任何形式的自动重复提交**都不做，包括平台在点击之后才拒绝的情况（FR-33）。
7. 通过 MCP 或持 token 的 HTTP 客户端确认批次（FR-14）。也不设按预算自动确认。
8. 自动改名或删除即梦上已有的主体。
9. **旧版 `参考:` 写法**：已填槽位号（`=>@1`）、无括号项（`名字=>@`）、无 `@`（`名字=>`）。预检时报错说明，不提供兼容。老剧要重拍哪一镜，先把那一镜改成现行写法（CLAUDE.md「规则变更只对改动的产物生效」）。
10. 同一批次内的首帧链式依赖：上一镜末帧要等本批次上一镜生成完才有。v1 里末帧文件不存在就预检报错。
11. 抽取末帧、定版、拼接、字幕、BGM。这些由 `ai_video_management` 负责。
12. Windows Service 形态。
13. 性能测试打真实站点。

---

## 3. 用户角色与主流程

| 角色 | 入口 | 能做 | 不能做 |
|---|---|---|---|
| 用户（人） | 本地管理网页（UI 身份） | 一切，包括**确认批次**、改全局 config、处理「待人工处理」、选定候选 | — |
| Claude | MCP `/mcp`（持 bearer token） | 预检、查询、等待、取消、恢复（限可自动恢复的原因）、分步调试到预演、主体同步/对账/申请创建、选定候选 | 确认、提交、改全局 config、处理提交结果不明的作业 |
| 自动化脚本 | HTTP `/api/*`（持 bearer token） | 与 Claude 相同 | 同上 |

### F1 首次启动与登录

1. `make init` 写入 `JIMENG_BRIDGE_TOKEN`；`make run` 启动服务。
2. service 用专用 profile 启动有界面的 Chrome，进入即梦创作页。
3. 检测到未登录 → 会话状态 `login_required`，弹 toast，把窗口置前。
4. 用户手动扫码登录。
5. canary 只读自检通过 → 会话状态 `ready`。

### F2 为一部剧建立 config

1. 在 UI 选中剧，点「生成默认 config」。
2. service 扫描剧目录，给出 `jimeng_config.toml` 的提议，把需要用户确认的项置顶。
3. 用户修改后保存。文件落在剧目录，进 git。

### F3 Claude 生成一集的视频（主流程）

1. Claude 调 `precheck_batch`，参数是若干 `shotNN.md`。
2. 返回 `batch_id`、摘要、确认页链接。
3. Claude 把链接交给用户。用户在 UI 确认页核对每条的参考图缩略图、主体、参数、预计积分，点「确认并开始」。
4. 队列按「有空槽 → 准备 → 预演 → 校验 → 立即提交」逐条执行：UI 动作串行，同时在远端渲染的 ≤ 3 条。
5. Claude 循环调用 `wait`（每次 ≤ 85 s），直到全部结束。
6. 结果落到 `shots/shotNN/renders/` 并写 sidecar。之后照常在 `ai_video_management` 里定版、拼接。

### F4 暂停与恢复

1. 出现验证码或风控弹窗、登录失效、积分不足、页面结构对不上 → 「队列已暂停」+ toast。
2. 用户在浏览器窗口里处理完，点「恢复队列」。
3. 审核被拒 → 该作业「失败」，队列继续。
4. 提交结果不明 → 该作业「待人工处理」，只能在 UI 里裁决。

### F5 资产出图与 turntable

1. 预检资产卡里以路由键开头的块：图片块走 CLI；视频块（turntable）走网页视频，以同卡立绘作参考。
2. 用户在 UI 确认。
3. 执行，候选落到 `_candidates/{key}/`。
4. 用户在 UI 选定一个候选 → 升格为 `{key}.{ext}`，旧文件归档。

### F6 主体对账与创建

1. 同步即梦主体列表，与各剧期望名对账。
2. 缺失的主体作为 `entity_create` 条目加入批次，由用户在 UI 确认。
3. 执行「新建主体」表单，完成后再同步一次核验。

### F7 分步调试

对单个作业分步执行 `set_params → upload → fill → preview`，不需要确认。「提交这一步」只在 UI 里对已确认的作业开放，并有二次确认。

---

## 4. 架构总览

```
┌──────────── 单进程 service（FastAPI / uvicorn，127.0.0.1，proxy_headers=False） ────────────┐
│  /api/*（bearer 或 UI 身份）  /ui-api/*（仅 UI 身份）  /mcp（仅 bearer）  /（React UI）       │
│        └──────────── 每个入口 = 恰好一个 Query/Command 方法（MCP tool 同理） ────────────┘   │
│  application: BatchCommand · JobCommand · OperationCommand · DramaConfigCommand ·            │
│               GlobalConfigCommand · EntityCommand · CandidateCommand · *Query                │
│  domain: GenerationRequest · ReferenceItem · FrozenRequest · JobEntity(状态机) · BatchEntity   │
│          OperationEntity · Precheck(纯函数) · Fingerprint · ConfirmationToken · DramaConfig    │
│          ports: GenerationBackend · JobRepository · BatchRepository · DramaConfigRepository   │
│  infrastructure:                                                                             │
│    WebUiBackend ─ BrowserActor(单个 async Playwright，串行 UI 动作) · PageMap · ResponseParsers│
│    DreaminaCliBackend ─ 子进程 dreamina.exe（argv 列表）                                        │
│    ShotPromptReader · AssetCardReader · DramaTreeReader · ThumbnailReader                    │
│    SQLite(WAL) Store · OutputWriter(原子落盘+sidecar) · TomlConfigStore · ToastClient          │
│    RequestClass middleware(Host/Origin/Sec-Fetch/UI 会话 cookie/bearer)                        │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **调度器**：负责作业的放行，约束有三条：账号级并发（`submitting` + `generating` 的条数 ≤ 上限）、最小提交间隔、backend 队列是否处于暂停状态。
- **BrowserActor**：从命令队列里串行消费。取消只在动作之间的检查点生效。
- **长耗时操作**：canary、主体同步 / 创建、分步操作、恢复自检，全部以 `OperationEntity` 在后台执行。API 和 MCP 立即返回 `operation_id` 和当前快照，之后用 `wait` 等待。

---

## 5. Functional requirements

> 编号是验收锚点。凡是「阈值 / 规则」都必须来自 config（FR-5）。

### 5.1 配置

**FR-1 全局 config。**
- 文件在 `projects/jimeng_web_bridge/config/global.toml`，进 git。只放非机密、与机器无关的值。
- 机器专属值和机密放在仓库根目录 gitignored 的 `.env`：
  - `JIMENG_BRIDGE_TOKEN`：必填，≥ 32 字符，不满足则 service 拒绝启动；`make init` 生成。
  - `JIMENG_BRIDGE_PROFILE_DIR`、`DREAMINA_CLI_PATH`：可选覆盖。
- HMAC 密钥在首次启动时随机生成，写入 `.data/secret.key`，不进 git。

| 键 | 默认 | 取值约束 |
|---|---|---|
| `server.port` | `8790` | host 固定为 127.0.0.1，不可配置 |
| `routing.video` | `web` | `web \| cli`；按能力矩阵预检 |
| `concurrency.max_remote_rendering` | `3` | 1–5；账号级，`submitting` + `generating` 合计 |
| `pacing.min_submit_interval_s` | `15` | ≥ 5，固定值不随机 |
| `wait.timeout_h` | `12` | 1–48 |
| `retries.set_params` / `retries.upload` / `retries.download` | `3` / `3` / `3` | 0–5 |
| `retries.fill` | `1` | 0–2（清空重填的次数） |
| `confirm.token_ttl_min` | `30` | 5–240 |
| `idempotency.retention_h` | `24` | 1–168 |
| `status.parse_failure_threshold` | `5` | 连续解析失败次数，1–50 |
| `entities.snapshot_stale_h` | `24` | 1–168 |
| `download.duration_tolerance_s` | `0.5` | 0.1–2 |
| `api.max_call_s` / `api.progress_interval_s` | `85` / `25` | max_call_s ≤ 85 |
| `api.page_size_default` / `api.page_size_max` | `50` / `200` | |
| `api.max_body_bytes` / `api.max_batch_items` | `1048576` / `50` | |
| `mcp.thumbnail_max_px` / `ui.reference_thumb_max_px` | `768` / `320` | |
| `artifacts.preview_max_bytes` / `artifacts.preview_retention_days` | `1048576` / `30` | |
| `time.timezone` | `Asia/Shanghai` | 用于每日统计与文件名时间戳 |
| `browser.channel` / `browser.profile_dir` / `browser.start_url` | `chrome` / `.data/chrome_profile` / 即梦视频创作页 | start_url 必须是 `https://jimeng.jianying.com/`（测试模式除外，见 NFR 可测性） |
| `canary.interval_min` | `30` | 另外在每批开始前、每次恢复前都跑一次 |
| `cli.path` / `cli.min_version` | `~/bin/dreamina.exe` / `1.4.5` | 必须解析为 `.exe` 文件；拒绝 `.cmd` / `.bat` / `.ps1` |
| `notifications.toast` | `true` | |
| `model_limits.*` | 见下表 | `as_of` 必填 |
| `price_table.video[]` / `price_table.image[]` | `{model, resolution, credits_per_second}` / `{model, resolution, credits_per_image}` | `as_of` 必填 |

`model_limits` 提议默认（`as_of = 2026-09-13`；带 * 的值以 stage-6 探针实测为准）：

| 模型键 | backend | 时长 s | 分辨率 | 比例 | 图 / 视频 / 音频上限 | 主体 | 负向输入框* |
|---|---|---|---|---|---|---|---|
| `seedance2.5` | web | 4–30 | 480p, 720p* | 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | 30 / 10 / 10*（页面称合计 50） | 支持 | false* |
| `seedance2.0_vip` | web, cli | 4–15 | 720p, 1080p | 同上 | 9 / 3 / 3 | web 支持 / cli 不支持 | false* |
| `seedance2.0fast_vip`、`seedance2.0`、`seedance2.0fast` | web, cli | 4–15 | 720p | 同上 | 9 / 3 / 3 | web 支持 / cli 不支持 | false* |
| `seedream5.0`（另有 3.0–4.7） | cli | — | 2k, 4k（3.x：1k, 2k） | 21:9, 16:9, 3:2, 4:3, 1:1, 3:4, 2:3, 9:16 | image2image 1–10 | — | — |

计数规则：主体 mention **不计入**图片上限（`count_entities_as_images = false`*）；首帧计入图片上限。

**FR-2 每剧 config。**
- 文件在 `ai_videos/{drama_root}/jimeng_config.toml`，进 git。
- **不得包含全局 config 的节**（`concurrency`、`pacing`、`retries`、`cli`、`browser` 等），出现即 schema 拒绝。

结构与提议默认：

- `[drama]`
  - `abbrev`：系列成员默认取集目录名（如 `hy3`）；独立剧留空，并标为需确认。
- `[entities]`
  - `name_template = "{abbrev}_{character_name}"`。`character_name` 为角色卡目录名去掉 `^c\d+_` 前缀；没有该前缀就用整个目录名。
  - `overrides = {}`，形如 `{ "c1_砌炉的老人" = "hy3_主角" }`。
  - `source_images = ["{card_dir}/c*-1.*", "{card_dir}/{card_dir_name}.png"]`：取第一个存在的文件。
  - `description_from = "locked_descriptor"`。
- `[references]`
  - `rules`：有序数组 `[{label_glob, kind, resolver}]`，默认值见 FR-8。
  - `overrides = {}`，形如 `{ "{参考项名}" = "ai_videos/…/file.png" | "entity:{主体名}" }`。
  - `search_exclude = ["_deleted", "_candidates", "renders", "frames", "_blender"]`。
- `[video]`
  - `model = "seedance2.5"`、`resolution = "720p"`、`count = 1`；
  - `ratio_source = "shot"`、`duration_source = "shot"`；
  - `negative_prompt = "platform_field_or_omit"`：`platform_field_or_omit | omit | fail`，**永不并入正向 prompt**。
- `[image]`
  - `model = "seedream5.0"`、`resolution = "2k"`、`count = 1`；
  - `ratio_by_subject = { characters = "3:4", scenes = "16:9", props = "1:1" }`；
  - `block_overrides = {}`：可按路由键覆盖 ratio、model、`reference_keys`。
- `[assets]`
  - `video_block_match = { first_line_contains = ["turntable"], has_field = ["时长:"] }`：两个条件满足其一即视为视频块。
  - `video_reference = "{card_dir}/c{N}-1.*"`（同卡立绘）。
  - `video_default = { model = "seedance2.5", resolution = "720p", ratio = "9:16", duration_s = 4 }`：块内有 `比例:` / `时长:` 时以块内为准。
- `[outputs]`
  - `video_name = "{shot}_{ts}{suffix}.mp4"`，其中 `ts = YYYYMMDD-HHmmss`；`suffix` 在 `count > 1` 时为 `_1..N`，同秒冲突时再追加 `_dup2..`。
  - `image_candidates_dir = "_candidates/{key}"`。
  - `on_existing = "archive"`：`archive | fail`。
- `[precheck]`
  - `prompt_max_chars = 5000`（按 Unicode 码点计数，规范化之后算）。
  - `entity_name_max_chars = 20`。
  - `estimate_tolerance_pct = 20`。

**FR-3 提议默认 config（`DramaConfigCommand.propose`）。**
- 扫描剧目录，输出上述结构。**已有 config 时不覆盖**，只返回逐键 diff。
- 每个 `needs_confirmation` 项都附原因。触发条件：
  1. 独立剧缺少 `abbrev`。
  2. 期望主体名不在最近一次主体快照里，**而且**快照中存在以 `{abbrev}_` 开头、却没有映射到本剧任何角色卡的主体。原因写成「可能已有同一角色的主体，名称不同，例如 `hy3_主角`」。
  3. 从来没做过主体同步：提示先同步。
  4. 参考项在默认规则下解析失败或多重匹配：给出建议的 override 键。
- 跨集复用的角色卡（`.link.json` 指向其他集）：主体名跟随来源集。来源集有 config 就按来源集的模板和 overrides 计算；没有就用来源集目录名作为 `abbrev`。

**FR-4 config 读写。**
- round-trip 保留注释与键顺序。
- 保存前做 schema 与取值约束校验，非法值拒绝并给出字段路径。
- 写入是原子的：临时文件 → rename。
- 保存请求携带读取时的内容 hash；文件已被改动 → 409。
- **全局 config 只能由 UI 身份写入**；bearer 客户端只读，而且读不到机密。

**FR-5 规则不写死。** 凡涉及剧、命名、路由键、映射、默认档位、阈值的内容，一律从 config 读取。validation 用「config schema 键 ↔ FR」对照表做契约测试。

### 5.2 输入与请求规范化

**FR-6 `GenerationRequest`（frozen）。** 字段如下；三种入口都规范化为它。
- `kind`：`video | image`
- `prompt`：见 FR-8 规范化
- `negative_prompt?`
- `references`：有序的 `ReferenceItem{name, label, kind: image|video|audio|entity|first_frame, resolved_path | entity_name, sha256?}`
- `params`：`{model, ratio, duration_s?, resolution, count, reference_mode?}`
- `output_slot`：视频为 shot 目录；图片为 `{subject_dir}#{key}`
- `source`：`{type: raw|shot|asset_image|asset_video|entity_create, path, block_key?}`

**FR-7 原始入口。** 参数为 `prompt`、有序文件路径、可选主体名、`params`、`output_dir`。文件路径必须在 `ai_videos/` 沙箱内；原始视频入口的 prompt 里用 `=>@` 标记 mention 位置，与 FR-31 同一套机制。

**FR-8 shot 适配（`ShotPromptReader`）。**

*prompt 提取与规范化*
- `## 视频 prompt` 下第一个 ```text 围栏里的全部内容就是 prompt。
- 规范化步骤：UTF-8 解码 → 去 BOM → CRLF/CR 统一为 LF → 去掉围栏内容末尾的换行。**规范化之后逐字节发送**，也用这个结果计算 hash 和字数。

*负向提示词*
- 定义：在 prompt 围栏之后、下一个 `##` 标题之前出现的第一个 ```text 围栏，并且它前一个非空行包含「反向提示词」（`##` 标题或 `> **反向提示词**` 引用块都算）。
- 围栏内的 `负面词:` 行属于正向 prompt 原文，不单独提取。

*字段解析（在 prompt 围栏内）*
- `比例:`：允许两侧有反引号、后面跟注释、同一行用 `｜` 分隔多个字段；取第一个 `\d+:\d+`。不在所选模型的比例列表里 → 预检错误。
- `时长:`：允许 `22秒`、`22s`、`22 s`，允许反引号，允许与其他字段同行；取第一个数字，四舍五入为整数秒。

*`参考:` 行*
- 以 `=>@` 为边界切分（一对反引号里可以包含多项），每项必须匹配 `^\s*{name}\((label)\)=>@$`，标点和反引号去掉后判断。
- **完整性校验**：prompt 中「紧跟在参考项后面的 `=>@`」的个数必须等于解析出的项数。
- 出现以下旧写法之一 → 预检错误 `legacy_reference_syntax`，说明「v1 只支持现行写法，请把该镜 `参考:` 行改为 `` `{名}({类型})=>@` ``」，**不能通过 config 豁免**：
  - `=>@` 后面跟了数字；
  - 项没有括号；
  - 项是 `名字=>` 而没有 `@`。
- 有 `参考:` 行但一项都没解析出来，或 `参考:` 行里有无法识别的片段 → 预检错误，绝不静默当作零参考。
- 没有 `参考:` 行、正文也没有 `=>@` → 零参考，合法。

*规则匹配*
- 每项按 `references.overrides` → `references.rules` 的顺序自上而下取第一条匹配。提议默认规则：

| label_glob | kind | resolver |
|---|---|---|
| `场景参考图*`、`*锚点`、`角色参考图`、`单位参考图`、`道具参考图`、`场景主体`、`物件主体` | image | `asset_file` |
| `Seedance 人物 entity`、`人物主体` | entity | `entity` |
| `previz灰模视频`、`3D预演视频` | video | `shot_video` |
| `上一镜末帧*` | first_frame | `prev_shot_lastframe` |

*resolver 语义*
- 所有 resolver 只在剧根和 `{series}/_series/` 下查找，并排除 `search_exclude` 中的目录。
- `asset_file`：按以下顺序查找，**第一个产生结果的步骤定胜负**；同一步骤内命中多个 → 预检错误 `ambiguous_reference`，要求填写 `references.overrides."{name}"`。
  1. stem 等于 `name` 的图片（`.png/.jpg/.jpeg/.webp`，或对应的 `.{ext}.link.json`）；
  2. 若 `name` 形如路由键 `^(bg|c|p)\d+-\d+$`：stem 以 `{name}_` 开头的图片；
  3. 若 `name` 是主体目录名（`bg{N}_…` / `c{N}_…` / `p{N}_…`）：该目录下的 `{name}.{ext}` 或 `{name}.{ext}.link.json`。
- `entity`：`name` → 匹配角色卡目录（目录名等于 `name`，或去掉 `c{N}_` 前缀后等于 `name`）→ 按 `entities` 模板和 overrides 得到主体名（跨集复用规则见 FR-3）。
- `shot_video`：在本镜目录（含子目录 `previz/`）里查找 stem 等于 `name` 的 `.mp4/.mov`；找不到时再试「交换顺序」的别名：`previz_shotNN` ↔ `shotNN_previz`。
- `prev_shot_lastframe`：`shots/shot{NN-1}/shot{NN-1}_lastframe.png`。不存在、或本镜是 shot01 → 预检错误（§2 第 10 条）。

**FR-9 资产卡适配（`AssetCardReader`）。**
- 在 `characters/*`、`props/*`、`scenes/*` 的主体 md 里，只取**首行以路由键开头**的 ```text 块（`c1-1_…`）。一块对应一个请求。锁定描述符、负面词所在的裸围栏都不当 prompt。
- 按 `[assets].video_block_match` 判定块的类型：
  - **图片块** → `asset_image`，走 CLI。`image.block_overrides.{key}.reference_keys` 非空时用 image2image，否则 text2image。
  - **视频块** → `asset_video`，走网页全能参考。参考图是 `assets.video_reference` 解析出的同卡立绘；参数取块内字段，缺省用 `assets.video_default`。

**FR-10 剧目录解析。**
- `ai_videos/` 下含 `series.json` 的目录是系列，系列下非 `_` 开头的子目录是剧；其余非 `_` 开头的目录本身就是剧。
- **可列入 UI 与 API 的剧**还要满足：剧根下存在任意 `shot*.md`，或存在 `characters/`、`props/`、`scenes/` 目录，或已有 `jimeng_config.toml`。这条用来排除 `notes/` 这类目录。
- `.link.json` 按 target 解析：拒绝逃出 `ai_videos/`、拒绝 symlink 或 junction、拒绝 UNC 或设备路径。
- 所有文件读写都受仓库沙箱约束（见 NFR 安全）。

### 5.3 预检

**FR-11 静态预检（纯函数，不开浏览器、不调 CLI）。** 每条检查以下各项：
1. 参考文件存在且可读，算出 sha256。
2. 参考的种类与数量在所选模型的 `model_limits` 内。
3. 时长、分辨率、比例在该模型范围内。
4. 所选 backend 具备所需能力，否则报错（**不降级**）。
5. prompt 码点数不超过上限。
6. 主体名不超过 20 码点，并且在主体快照中存在。快照过期给 warning；缺失给 error。
7. 输出目录可写。
8. 指纹去重（FR-24）。
9. 负向提示词策略：策略为 `fail`、shot 有负向提示词、但模型的 `负向输入框 = false` → error。
10. `entity_create` 条目：名称长度合规、`source_images` 存在、快照中没有同名主体（有同名时标为「复用」）。

每条的结果分为 `ok` / `warning` / `error`。

**FR-12 预计积分。**
- 视频：`ceil(duration_s) × credits_per_second × count`。
- 图片：`credits_per_image × count`。
- `entity_create`：0。
- 价格表里没有对应项 → warning「无法估算」。
- 历史里若有同 `model × resolution` 的实扣记录，一并显示「最近实测单价」，方便用户更新价格表。

**FR-13 `BatchCommand.precheck(items, idempotency_key?)`。**
- 返回 `batch_id`、摘要（ok / warning / error 计数，合计预计积分）、确认页 URL。
- 逐条明细用分页的 `BatchQuery.get` 获取。MCP 返回里的 ok 条目只给计数。
- **token 不返回给 bearer 客户端**（FR-14）。
- batch 状态为 `awaiting_confirm`。含 error 条目的 batch 不能确认，需要剔除后重新预检（UI 提供「剔除错误项并重新预检」）。
- 同一请求中，items 数不超过 `api.max_batch_items`。

### 5.4 确认闸门

**FR-14 只有 UI 身份能确认。**
- 确认路由是 `POST /ui-api/batches/{id}/confirm`，只接受 UI 身份的请求（NFR 安全的身份判定）。**任何带 bearer token 的请求一律 403**。MCP 不提供任何确认工具。
- `confirmer` 由服务端根据身份判定并写入，只有一种值 `ui_human`，客户端传不进来。
- token 流程：UI 打开确认页时，通过 `GET /ui-api/batches/{id}/confirmation` 取得 HMAC token。token 绑定 batch 内容摘要、合计预计积分、过期时间（`confirm.token_ttl_min`）。
  - 单次有效，由服务端强制；摘要不一致或已过期 → 拒绝。
  - 确认页显示倒计时；过期后提供「重新预检」，按同一组 items 重新生成 batch。
- **威胁模型声明**：这道闸门防的是 Claude 或自动化脚本经由受支持的接口花掉积分，不防同一 Windows 用户下蓄意冒充浏览器的本地进程——这类进程本来就能直接操作即梦页面。README 写明：不要让 Claude 用浏览器自动化工具去点这个 UI 的确认按钮。

**FR-15 冻结请求。**
- 确认时，每个作业的 `FrozenRequest` 被持久化：规范化后的 prompt 全文、负向提示词、有序参考项及其 sha256、主体名、params、output_slot，以及所用 config 的 digest。
- 执行时**只用冻结请求**，不重新读取 shot md 或 config。
- 上传前重算每个参考文件的 sha256：任一不一致 → 作业进入「待人工处理」（`inputs_changed`），需要重新预检。

**FR-16 硬不变量。** 没经确认的作业，不论从哪个入口，都**不会进入 `preparing`（分步调试除外）、也不会进入 `submitting`**。分步调试（F7）的 `set_params / upload / fill / preview` 可以用于未确认的作业，但不会让它进入队列。

### 5.5 作业队列与状态机

**FR-17 `JobEntity` 状态机**（转移由实体方法守护，非法转移抛领域错误，每次转移记录 `{from, to, at, reason?}`）：

```
queued ──(有槽+间隔满足+队列运行中)──▶ preparing[set_params→upload→fill→preview→verify] ──▶ submitting ──▶ generating ──▶ downloading ──▶ done
   │                                     │                                               │            │              │
   └──▶ cancelled                        ├──▶ paused_needs_human                          ├──▶ paused_needs_human (见 FR-21)
                                         └──▶ failed                                     └──▶ failed / cancelled(credits_spent)
```

- `queued` 带一个 `blocked_on` 字段：`slot | interval | queue_paused | none`。
- **准备只在拿到槽位后进行，准备完成后立即提交。** 任何作业都不会拿着一个已填好的 composer 去等待。点击前再做一次 `verify`，确认编辑器内容与 mention 序列（FR-31）。
- 作业级终态与「待人工处理」的归属：

| 原因 | 进入的状态 | 能否用 `resume` 恢复 | 恢复后回到 |
|---|---|---|---|
| `moderation_reject`、`real_face_rejected`、`upload_rejected` | `failed` | — | — |
| `fill_mismatch`、`step_failed`（set_params / upload / fill 重试耗尽） | `paused_needs_human` | 可以（API / MCP / UI） | `queued`，composer 先清空 |
| `inputs_changed` | `paused_needs_human` | 不可以，只能重新预检 | — |
| `wait_timeout` | `paused_needs_human` | 可以 | `generating`（继续轮询） |
| `download_failed`（下载重试耗尽） | `paused_needs_human` | 可以 | `downloading` |
| `restart_during_submit`、`submit_rejected`、`submit_unconfirmed` | `paused_needs_human` | **仅 UI 裁决**（FR-19） | 由裁决决定 |
| `estimate_exceeds_confirmed` | `paused_needs_human` | **仅 UI 批准** | `preparing` → `submitting` |
| `cli_error` | `paused_needs_human` | 可以 | 提交前的错误 → `queued`；提交后的错误 → `generating` |

**FR-18 调度。**
- UI 动作全局串行，只有一个 BrowserActor。
- 账号级并发：状态为 `submitting` 或 `generating` 的作业合计 ≤ `concurrency.max_remote_rendering`，web 与 cli 共用这个额度。
- 两次提交的间隔 ≥ `pacing.min_submit_interval_s`，web 与 cli 共用。
- **点击之前**，如果页面已经显示「并行任务已达上限」，或者被动观察到的平台在途数 ≥ 上限，作业保持 `queued(blocked_on=slot)`，**不点击**。
- 某个 backend 的队列被暂停时，只影响该 backend 的作业。

**FR-19 崩溃安全提交与 UI 裁决。**
- 点击前持久化 `submitting` 和指纹。点击后按 FR-33 拿到平台任务标识，才进入 `generating`。
- 启动时：`submitting` → `paused_needs_human(restart_during_submit)`；`generating` / `downloading` → 先 canary，再恢复轮询或下载。
- `restart_during_submit` / `submit_rejected` / `submit_unconfirmed` 的裁决**只能在 UI 里做**。UI 列出即梦历史中提交时刻前后、prompt 前缀一致的记录，供用户三选一：
  1. 「这就是它」→ 关联平台任务，进入 `generating`；
  2. 「确认没有提交」→ 允许人工再提交一次，这是用户的显式操作，计为新的 attempt；
  3. 「取消」→ `cancelled`。

**FR-20 重试边界。**
- **提交这一步零自动重试。**
- 各步骤的重试次数取 `retries.*`。
- 审核被拒不改写 prompt。

**FR-21 暂停分级。**
- **队列级**：`login_expired`、`captcha_or_risk_popup`、`insufficient_credit`、`page_contract_broken`、`browser_lost`（web）；`cli_login_required`、`compliance_confirmation_required`（cli）。
  - 效果：设置该 backend 的 `queue_state = paused(reason)`，弹 toast；在 UI 所有页面顶部显示「队列已暂停」横幅。
  - 作业状态不批量改写：`queued` 的作业 `blocked_on = queue_paused`；`preparing` 的作业在下一个检查点退回 `queued`，composer 在恢复时清空；`generating` 的作业，只要浏览器或 CLI 仍然可用就继续被动观察，否则在恢复后重新对账。
- **作业级**：见 FR-17 表。只影响该作业，队列继续。

**FR-22 取消。**
- `queued` / `preparing` 中取消 → `cancelled`，不花积分。
- `submitting` 中取消 → 先记 `cancel_requested`，等点击结果：没有点击 → `cancelled`；已经提交 → `cancelled(credits_spent=true)`。
- `generating` / `downloading` 中取消 → `cancelled(credits_spent=true)`，停止等待和下载。
- 响应和 UI 都明确显示「积分不会退还」。

**FR-23 恢复。**
- `resume_job`：只接受 FR-17 表中标为「可以」的原因。
- `resume_queue`：先执行一次 canary（web）或 `user_credit`（cli）作为后台 operation。自检通过才把 `queue_state` 设为 `running`，失败则保持暂停并返回原因。

**FR-24 幂等与去重。**
- `idempotency_key`：同 key 同内容 → 返回首次结果；同 key 不同内容 → 409 / `isError`。保留 `idempotency.retention_h`。「同内容」判定为规范化请求体的 canonical JSON sha256 相等。
- 指纹计算：`fingerprint = sha256(canonical_json({kind, prompt_sha256, negative_prompt_sha256|null, references:[{kind, name, sha256|entity}], params, output_slot}))`。canonical JSON 的要求是：键排序、UTF-8、无多余空白、`null` 与空串区分。
- **`output_slot` 不含带时间戳的文件名。**
- 同指纹已有非终态或 `done` 的作业 → 直接返回它，除非传 `reroll: true`，此时记录 `attempt` 序号。

### 5.6 WebUiBackend（Playwright，有界面）

**FR-25 会话。**
- 常驻单个 persistent context。
- 启动失败分类为 `profile_in_use` / `browser_missing` / `launch_timeout`。**不自动删除锁文件。**
- 记录 `browser.version` 与页面的 `web_version`。

**FR-26 登录。**
- 检测不到登录标志 → `login_required`，把窗口置前并弹 toast。
- service 不向页面输入任何凭据。

**FR-27 canary（只读，作为后台 operation 执行）。**
- 检查项：登录标志；创作类型、模型、参考模式、比例 · 分辨率 · 数量、时长这些控件；TipTap 编辑器；上传入口；生成按钮；预计积分文本；最近一次状态响应能被截获并解析。
- 任一项失败 → `page_contract_broken`。
- **canary 不点击生成。**

**FR-28 PageMap。**
- selector 与流程步骤集中在一个模块，标注已验证的 `web_version`。
- 按角色和文本定位，**禁止坐标点击**。
- 先定位到记录，再在记录内部找控件。

**FR-29 设置参数。**
- 依次设置：创作类型 = 视频生成、模型、参考模式 = 全能参考、比例、分辨率、数量、时长。
- 每设置一项就读回控件显示值校验。
- 重试次数用 `retries.set_params`，耗尽 → `step_failed`。

**FR-30 上传。**
- 按顺序上传非主体参考项：先复制到 `.data/tmp/` 并命名为 `{name}{ext}`，再上传，确保平台显示名等于 `name`。
- 等待页面完成信号（stage-6 探针确定）。
- 被拒 → `upload_rejected`；超时或出错按 `retries.upload` 重试。

**FR-31 填写与校验。**
- 以 prompt 中每个参考项的 `=>@` 为界切段：文本段用可切换的插入策略写入（由 canary 实测选定）；在每个 `=>@` 的 `@` 处插入 mention——输入 `@` → 按名称过滤 → 点选对应候选项（上传素材的 stem 或主体名）。
- prompt 中其他普通 `@` 按普通文本输入。如果平台把它弹成候选菜单，要关闭菜单而不选择。
- **verify**：编辑器纯文本（规范化空白，mention 以名称计）等于期望，并且 mention 节点序列等于期望。
- 不一致 → 清空重填，最多 `retries.fill` 次；仍不一致 → `fill_mismatch`。
- 负向提示词按 `video.negative_prompt` 策略处理。

**FR-32 预演。**
- 截全页和 composer 局部，存为 JPEG/WebP，单张 ≤ `artifacts.preview_max_bytes`，保留 `artifacts.preview_retention_days` 天。
- 读取页面显示的预计积分，写入作业。
- 页面预计积分超出冻结时的静态预计积分 `precheck.estimate_tolerance_pct` 以上 → `paused_needs_human(estimate_exceeds_confirmed)`，不提交。
- 静态预计缺失（价格表无对应项）时，确认页已显示「无法估算」。这种情况下以页面预计为准，**首个作业**同样进入这个暂停，由人批准。

**FR-33 提交。**
- 前置条件：作业已确认（FR-16），调度许可（FR-18），verify 通过。
- 点击前持久化 `submitting`。
- 点击后被动截获提交响应，拿到平台任务标识 → `generating`。
- 页面在点击后提示「并行任务已达上限」或其他拒绝 → `paused_needs_human(submit_rejected)`，**绝不自动再点**。
- 截获不到响应，而历史记录里也对不上 → `paused_needs_human(submit_unconfirmed)`。

**FR-34 状态观察。**
- 在 context 级只读监听 `get_history_queue_info` 与 `get_history_by_ids` 的响应。不使用 `route`，不修改请求。
- 解析器是带版本号与 schema 校验的纯函数，**测试夹具来自 stage-6 探针采集、脱敏后的真实响应**。
- 连续解析失败达到 `status.parse_failure_threshold` 次 → `page_contract_broken`。

**FR-35 下载。**
- **只通过页面自身的下载控件触发下载**，由 Playwright download 事件以流式方式存到 `.data/tmp/`。不直接请求结果 URL。
- 校验：size、sha256；ffprobe 读出的时长与期望相差不超过 `download.duration_tolerance_s`，比例一致。
- 原子 rename 到目标 → 写 sidecar（FR-44）。Python 进程内存增长 ≤ 64 MB，与文件大小无关。
- 从「详细信息」读取实扣积分。
- 重试次数用 `retries.download`，耗尽 → `download_failed`。

**FR-36 失败现场。**
- 只在失败或暂停时保留截图、DOM 快照、trace 片段，存到 `.data/artifacts/`。
- **只有截图可以经 API 访问**，DOM 快照与 trace 永不对外。

**FR-37 浏览器丢失。**
- context 或 page 的 close / crash → `browser_lost`。
- 处理顺序：暂停 web 队列 → 重建 context → 检查登录 → 对账所有 `generating` 的作业。

### 5.7 DreaminaCliBackend（官方 CLI）

**FR-38 调用范围。**
- 可用命令：`text2image`、`image2image`、`query_result --submit_id --download_dir`、`list_task`、`user_credit`、`version`。
- 调用方式：子进程、argv 列表、`--flag=value` 形式，不经 shell。
- 解析 JSON 输出。以下情况映射到暂停原因：未登录 → `cli_login_required`；`AigcComplianceConfirmationRequired` → `compliance_confirmation_required`；其余非零退出码 → 作业级 `cli_error`，附 stderr 尾部。完整退出码映射表由 stage-6 探针补全。

**FR-39 生命周期。**
- 提交：执行生成命令，不带 `--poll`，拿到 `submit_id` 立即持久化 → `generating`。
- 轮询 `query_result`，完成后 `--download_dir` 下载到 `.data/tmp/` → 同 FR-35 校验 → 落到 FR-43 的候选目录。

**FR-40 登录。** CLI 未登录 → CLI 队列暂停，UI 提示用户运行 `dreamina login`。service 不代为登录。

**FR-41 版本。** 启动时读取 CLI 版本（作为后台 operation，不阻塞启动）；低于 `cli.min_version` → warning。

### 5.8 产物与记录

**FR-42 视频落点。** `{shot_dir}/renders/{video_name}`，永不覆盖已有文件。资产视频块的结果落到 `{card_dir}/_candidates/{key}/{ts}{suffix}.mp4`。

**FR-43 图片与候选。**
- 候选落到 `{subject_dir}/_candidates/{key}/{ts}{suffix}.{ext}`。
- `CandidateCommand.promote(candidate)` 把候选复制为 `{subject_dir}/{key}.{ext}`。已存在同名文件时，按 `on_existing` 处理：`archive` 表示先把旧文件连同它的 sidecar 移入 `ai_videos/_deleted/{原相对目录}/{stem}.{ts}{ext}`。
- promote 允许 UI 与 bearer 身份调用（不花积分，可以从 `_deleted` 找回）。

**FR-44 sidecar。**
- 位置：每个产物文件（renders 视频、候选、升格后的文件）旁边写 `{文件名}.jimeng.json`，进 git。升格后的文件带 `promoted_from`；归档时 sidecar 随文件一起移动。
- 字段（**白名单**，不含账号 id、cookie、token、签名 URL）：
  - 任务：`job_id`、`batch_id`、`attempt`、`backend`
  - 来源：`source{type, path, block_key}`、`prompt_sha256`、`negative_prompt_sha256`
  - 参考：`references[{name, kind, path | entity, sha256}]`
  - 参数与平台：`params`、`platform_task_id`
  - 积分：`credits_estimated{static, page}`、`credits_charged`
  - 时间与确认：`confirmed_at`、`confirmer`、`submitted_at`、`finished_at`
  - 耗时：`durations{prepare_s, queue_wait_s, render_s, download_s}`
  - 版本：`web_version | cli_version`、`browser_version`
  - 产物：`output{sha256, size, duration_s?, width, height}`

**FR-45 原样保存。** 不修改下载的字节，不剥离元数据。截图、DOM、trace **永远不写到 `ai_videos/` 下**。

**FR-46 生成历史。**
- `HistoryQuery` 分页按剧、镜、主体、日期（`time.timezone`）查询。
- 返回内容：预估与实扣积分、每日合计、各阶段耗时、候选网格。
- 每个 batch 在开始和结束时各读一次余额，写入 batch。

### 5.9 主体

**FR-47 同步。** `EntityCommand.sync()`（后台 operation）打开主体页，被动读取 `dreamina_subject/get` 的响应，生成主体快照（名称、缩略图、修改时间、同步时间）。

**FR-48 对账。**
- 期望名的来源：各剧 config + 跨集复用规则。
- 三态：`mapped` / `missing_on_platform` / `unmapped_on_platform`。

**FR-49 创建。**
- `EntityCommand.request_create(drama, character_dir)`（API / MCP / UI 均可调用）：往一个 batch 里加入 `entity_create` 条目，预检按 FR-11 第 10 项。
- **确认只在 UI 的批次确认页进行**。描述可以在确认页编辑，编辑后的内容写入冻结请求。
- 执行：进入「新建主体」表单 → 上传参考图 → 填写名称和描述 → 保存 → 重新同步核验。
- 同名主体已存在 → 复用，不创建。

**FR-50 不破坏。** service 永不改名、删除或覆盖即梦上的主体。

### 5.10 HTTP API

身份类别见 NFR 安全：**A** = bearer 或 UI 身份均可；**U** = 仅 UI 身份。所有列表接口都分页（`page_size_default` / `page_size_max`）。

| Method | Path | 身份 | 映射 |
|---|---|---|---|
| GET | `/api/health` | 免认证（只返回 `{ok}`） | `SessionQuery.health` |
| GET | `/api/session` | A | `SessionQuery.status`（返回最近一次快照，**不在请求内调用 CLI 或 canary**） |
| POST | `/api/operations/canary` | A | `OperationCommand.start_canary` |
| GET | `/api/operations/{id}` | A | `OperationQuery.get` |
| POST | `/api/batches` | A | `BatchCommand.precheck` |
| GET | `/api/batches/{id}` | A | `BatchQuery.get`（分页明细，不含 token） |
| GET | `/ui-api/batches/{id}/confirmation` | U | `BatchQuery.confirmation`（含 token 与倒计时） |
| POST | `/ui-api/batches/{id}/confirm` | U | `BatchCommand.confirm` |
| POST | `/api/batches/{id}/reprecheck` | A | `BatchCommand.reprecheck`（剔除错误项或过期重建） |
| GET | `/api/jobs` | A | `JobQuery.list`（不含转移记录） |
| GET | `/api/jobs/{id}` | A | `JobQuery.get`（含转移记录） |
| POST | `/api/wait` | A | `WaitQuery.wait`（`job_ids \| batch_id \| operation_id`，≤ `api.max_call_s`） |
| POST | `/api/jobs/{id}/cancel` | A | `JobCommand.cancel` |
| POST | `/api/jobs/{id}/resume` | A | `JobCommand.resume`（仅可自动恢复的原因） |
| POST | `/ui-api/jobs/{id}/adjudicate` | U | `JobCommand.adjudicate`（FR-19 三选一；`estimate_exceeds_confirmed` 批准） |
| POST | `/api/queues/{backend}/pause` | A | `JobCommand.pause_queue` |
| POST | `/api/queues/{backend}/resume` | A | `OperationCommand.start_resume_queue` |
| POST | `/api/jobs/{id}/steps/{op}` | A | `OperationCommand.start_step`（op ∈ `set_params\|upload\|fill\|preview`） |
| POST | `/ui-api/jobs/{id}/steps/submit` | U | `OperationCommand.start_step_submit`（已确认作业，二次确认） |
| GET | `/api/artifacts/{job_id}/{name}` | A | `ArtifactQuery.get_screenshot`（仅图片；`nosniff`） |
| GET | `/api/thumbs` | A | `ThumbnailQuery.get`（`?path=`，沙箱内，长边 ≤ `ui.reference_thumb_max_px`） |
| GET | `/api/dramas` | A | `DramaConfigQuery.list_dramas`（系列嵌套：`{name, path, type: series\|drama, children[]}`） |
| GET | `/api/dramas/{drama}/config` | A | `DramaConfigQuery.get` |
| POST | `/api/dramas/{drama}/config/propose` | A | `DramaConfigCommand.propose` |
| PUT | `/api/dramas/{drama}/config` | A | `DramaConfigCommand.save` |
| GET | `/api/config/global` | A | `GlobalConfigQuery.get`（无机密） |
| PUT | `/ui-api/config/global` | U | `GlobalConfigCommand.save` |
| POST | `/api/operations/entity-sync` | A | `OperationCommand.start_entity_sync` |
| GET | `/api/entities/reconcile` | A | `EntityQuery.reconcile` |
| POST | `/api/entities/create-requests` | A | `EntityCommand.request_create` |
| GET | `/api/history` | A | `HistoryQuery.list` |
| POST | `/api/candidates/promote` | A | `CandidateCommand.promote` |

- `{drama}` 是 URL 编码后的剧根相对路径。
- 业务错误统一为 `{error_code, message, hint, config_key?}`。
- 请求体上限 `api.max_body_bytes`。

### 5.11 MCP（`/mcp`，Streamable HTTP，同进程，仅 bearer）

**FR-51 工具集（10 个，没有确认或提交类工具）：**

| 工具 | 映射 |
|---|---|
| `session_status` | `SessionQuery.status` |
| `precheck_batch` | `BatchCommand.precheck`（items：shot 路径、`{card_path, key}` 资产块、原始请求） |
| `get_batch` | `BatchQuery.get` |
| `wait` | `WaitQuery.wait` |
| `list_jobs` | `JobQuery.list` |
| `cancel_job` | `JobCommand.cancel` |
| `resume` | `JobCommand.resume` 或 `OperationCommand.start_resume_queue`（二选一参数） |
| `browser_step` | `OperationCommand.start_step`（op ∈ `set_params\|upload\|fill\|preview`，**无 submit**） |
| `entities` | `start_entity_sync` / `EntityQuery.reconcile` / `EntityCommand.request_create`（action 参数） |
| `get_screenshot` | `ArtifactQuery.get_screenshot` |

**FR-52 调用约束。**
- 每个工具在 `api.max_call_s` 内返回。浏览器或 CLI 相关的工具只负责发起 operation，并返回快照。
- `wait` 期间每 ≤ `api.progress_interval_s` 发一次 `notifications/progress`，到时限返回快照和建议的下一步。
- 返回 `structuredContent` 加上同内容的 JSON 文本，**两者合计 ≤ 约 20k token**：列表分页，截图只给路径和 ≤ `mcp.thumbnail_max_px` 的缩略图。
- 业务错误返回 `isError: true`，附可照做的建议。例如「请在 UI 确认：{url}」「在 config 填写 `references.overrides."砌炉的老人"`」「该镜使用旧版参考写法，请改为 `` `{名}({类型})=>@` ``」。
- 不使用 elicitation，不依赖 MCP tasks 扩展。

**FR-53 接入。** README 给出 `.mcp.json` 片段：`type: http`、`url: http://127.0.0.1:8790/mcp`、`headers.Authorization: Bearer ${JIMENG_BRIDGE_TOKEN}`、`timeout: 120000`。

### 5.12 本地管理 UI（`apps/ui/`，React，中文，浅色主题）

**FR-54 页面：**
1. **会话**：web 登录、canary 逐项结果、浏览器与 `web_version`；CLI 登录、版本、余额（最近快照）；按钮「打开浏览器窗口」「运行 canary」。
2. **剧 config**：
   - 剧列表（系列折叠）；
   - 表单编辑 + 原文 TOML 视图（深色 `<pre>` 属于允许的例外）；
   - 「生成默认 config」；需确认项置顶，用图标 + 文字标识；
   - schema 错误就地提示；409 冲突时弹对话框；
   - 参考项解析预览，含旧写法说明。
3. **批次确认**：
   - 逐条显示参考缩略图（`/api/thumbs`）、主体、参数、静态预计积分与最近实测单价；
   - 合计积分；今日已确认积分合计；token 倒计时；
   - error 条目不能确认；「剔除错误项并重新预检」「确认并开始」。
4. **队列看板**：
   - 分列：排队 / 准备 / 渲染中 / 下载中 / 待人工处理 / 完成 / 失败 / 取消；
   - 每个作业显示子步骤进度、平台进度、`blocked_on`；
   - 待人工处理：原因 + 截图 + 可执行操作，其中 FR-19 裁决和积分批准只在这里；
   - 取消、恢复、分步操作；
   - 「冻结刷新」开关；
   - 采用 3 s 轮询，带 `since` 游标，v1 不用 SSE。
5. **历史与积分**：筛选；预估与实扣；每日合计；各阶段耗时；候选网格 +「选定」。
6. **主体对账**：三态表 +「申请创建」（进入批次确认页）。
7. **全局设置**：表单编辑，含取值约束提示，不展示机密。

**FR-55 UI 约束。**
- 浅色主题（development.md §7）。
- 数据加载失败时显示错误态和「重试」，不出现空白页；解析型组件包在 error boundary 里。
- 三种「暂停」措辞必须区分：「队列已暂停」（队列标志）/「待人工处理」（作业）/「已冻结刷新」（界面）。
- 所有花积分或改动即梦的按钮都不设键盘快捷键。确认页进入时焦点在标题上，不在确认按钮上。「提交后取消」「分步提交」「选定并归档」都用 `alertdialog` 二次确认，默认焦点放在安全选项上。

### 5.13 通知

**FR-56 Windows toast。**
- 触发：队列级暂停、作业进入待人工处理、batch 全部结束、需要登录。
- 点击后打开 UI 对应页面。
- 尽力而为：失败只记日志。

---

## 6. Non-functional requirements

**部署与运行**
- 以当前登录用户的身份在交互桌面会话中运行。
- 入口：
  - `make init`：生成 token、创建 `.data/`；
  - `make run`：单进程运行 API + MCP + 已构建的 UI；
  - `make ui-build`；
  - `make test`；
  - `make test-perf`：Windows 开发机上自动跑，不并入 `make test`；
  - `make test-soak`：8 h 稳定性测试，人工触发；
  - `make canary`：对真实站点跑只读 canary，人工触发。
- pip + `.venv`，不依赖 `uv`。只有一种运行模式，不宣传 Vite dev server。

**安全**
- 只绑定 `127.0.0.1`；`proxy_headers=False`，不信任 `X-Forwarded-*`；Host allowlist；不开 CORS。
- **身份判定**（中间件统一执行，先于路由）：

| 请求特征 | 身份 |
|---|---|
| `/mcp` 路径 | 必须 bearer，否则 403 |
| 带 `Authorization: Bearer` 且与 `.env` token 常量时间比较一致 | bearer（不能访问 `/ui-api/*`） |
| 无 bearer，`Sec-Fetch-Site: same-origin`，存在 UI 会话 cookie（UI 外壳页下发，HttpOnly、SameSite=Strict、每次启动轮换），且非 GET 请求的 Origin 为本服务 | UI |
| `GET /`、静态资源、`/api/health` | 免认证 |
| 其他 | 403 |

- MCP Python SDK 版本 ≥ 1.23.0，并显式配置 `TransportSecuritySettings`（allowed hosts / origins）。
- 文件沙箱：
  - 读仅限仓库 `ai_videos/`；写仅限 `ai_videos/` 下的目标目录、`ai_videos/_deleted/` 与 `projects/jimeng_web_bridge/.data/`。
  - 拒绝：`..`、绝对或盘符路径、UNC 与设备路径、symlink 和 junction、NTFS 备用数据流（`:`）、保留名、结尾的点或空格、与 `ai_videos` 共前缀的兄弟目录。
- 子进程：argv 列表，`cli.path` 必须是 `.exe`；只有 UI 身份能修改 `cli.path`，并写审计日志。
- 机密卫生：token 与 HMAC 密钥不出现在日志、数据库、sidecar、响应、MCP 输出里；`.gitignore` 覆盖 `.data/` 与 `.env`（用测试断言）。
- 静态禁用：不使用 `page.route` / `context.route`、`context.request`、`expose_binding` / `expose_function`、`--remote-debugging-port`。依赖扫描拒绝 stealth、验证码求解类包。

**账号风险（用户知情接受）**
- README 首屏写明：即梦用户协议 5.1 禁止用自动化工具接入，付费协议 6.5 / 8.2 可以作废权益或封号；本项目为本人账号、本机、个人自用，风险由用户承担。
- 设计上压小暴露面：单账号、单 profile、只在本机服务、固定提交间隔、并发上限、提交零自动重试、零对抗检测、人工确认、图片走官方 CLI。这些约束在**服务端强制**。
- README 注明：上传素材按用户协议 9.3 授权平台用于优化模型；写实真人素材可能被拒。

**可靠性**
- SQLite WAL，service 是唯一写者。
- 重启恢复遵循 FR-19 / FR-23，任何情况下都不会自动重复提交。
- 下载一律经过 临时文件 → 校验 → 原子 rename。

**性能（hard = 不达标即 blocker；observe = warning）**
- hard：MCP 和 HTTP 每次调用 ≤ 85 s 返回；`wait` 至少每 25 s 发一次进度。
- hard：填写、上传、下载、哈希、ffprobe、CLI 子进程等重负载进行时，`/api/health` p95 ≤ 100 ms，`/api/jobs` p95 ≤ 200 ms，事件循环单次卡顿 ≤ 500 ms。
- hard：1000 个作业时，查询类接口 p95 ≤ 500 ms。
- hard：UI 冷启动首屏 ≤ 2 s。
- hard：启动到 health 可用 ≤ 8 s（不等浏览器与 CLI）。
- hard：空闲 CPU ≤ 2 %。
- hard：下载时 Python 进程内存增长 ≤ 64 MB。
- observe：20000 个作业时查询 p95 ≤ 1 s；单个作业准备阶段 ≤ 3 min；canary 耗时；8 h soak 中内存与磁盘的增长。

**可观测**
- JSONL 日志写到 `.data/logs/`。
- 作业转移、各阶段耗时、预估与实扣积分都入库。

**可测性**
- **离线 Fake 即梦站点**：本地 HTML fixture，模拟 composer、@ 候选、上传、参数控件、预计积分、生成按钮、下载控件、主体页、状态轮询接口。支持注入以下故障：验证码、审核拒绝、点击前后的并发上限提示、登录失效、上传拒绝、失焦追加、延迟或畸形的状态响应、页面重载。
- **fake `dreamina`**：优先提供真实 `.exe`，保证「不经 shell」这一点也被测到；只有在 `JWB_TEST_MODE=1` 时才允许用 launcher 配置调起非 `.exe`。
- **测试注入点**（仅环境变量）：`JIMENG_BRIDGE_REPO_ROOT`（临时仓库根，内含 `ai_videos/` 子集）、`JIMENG_BRIDGE_DATA_DIR`（临时 `.data/`）、`JIMENG_BRIDGE_GLOBAL_CONFIG`（测试用 `global.toml`）。`JWB_TEST_MODE=1` 时**不加载仓库根目录的 `.env`**，只认显式传入的环境变量，防止测试悄悄用上真实 profile。
- **测试专用 fault point 与 toast sink**：仅在 `JWB_TEST_MODE=1` 下启用，例如「持久化 submitting 之后暂停」的门、把 toast 写进文件而不是真的弹出。生产模式下这些钩子不存在。
- **硬护栏**：测试模式下 `browser.start_url` 必须是 localhost、`cli` 必须是 fake、profile 必须是测试临时目录；启动前和启动后各校验一次实际生效的 config，不满足就中止。
- **解析器测试**：使用真实 shot md 与资产卡的副本；状态响应解析器使用 stage-6 探针采集并脱敏的真实响应。
- 真实站点只跑人工触发的只读 canary。

**代码规范**
- 遵循 `.claude/agent_refs/project/development.md` §1–7。
- 各项目自己的 `requirements.txt` 与仓库根 `pyproject.toml` 保持镜像。
- README 用中文，随功能更新。

---

## 7. 项目布局

```
projects/jimeng_web_bridge/
├── README.md  Makefile  pyproject.toml  requirements.txt  .gitignore(.data/)
├── config/global.toml
├── apps/
│   ├── api/  main.py · app_factory.py · container.py
│   │   ├── routes/{session,operation,batch,job,wait,artifact,thumbnail,drama_config,global_config,entity,history,candidate}__route.py · __init__.py
│   │   └── mcp_tools/{session,batch,wait,job,operation,entity,artifact}__tool.py · __init__.py   ← divergence 1
│   └── ui/   (Vite + React + TS；构建产物输出到 apps/api/static/，已被根 .gitignore 覆盖)
├── libs/
│   ├── common/        enums.py · drama_ref.py · paths.py · canonical_json.py
│   ├── domain/
│   │   ├── entities/      generation_job__entity.py · batch__entity.py · operation__entity.py
│   │   ├── value_objects/ generation_request__valueobject.py · frozen_request__valueobject.py · reference_item__valueobject.py
│   │   │                  generation_params__valueobject.py · drama_config__valueobject.py · global_config__valueobject.py
│   │   │                  model_limits__valueobject.py · fingerprint__valueobject.py · confirmation_token__valueobject.py
│   │   │                  precheck__valueobject.py（纯函数）· precheck_result__valueobject.py · pause_reason__valueobject.py
│   │   ├── errors/        job__error.py · batch__error.py · precheck__error.py · config__error.py · operation__error.py
│   │   └── repositories/  job__repository.py · batch__repository.py · operation__repository.py · drama_config__repository.py
│   │                      generation_backend__repository.py（GenerationBackend 端口 Protocol）
│   ├── application/
│   │   ├── commands/  batch · job · operation · drama_config · global_config · entity · candidate  (__command.py)
│   │   ├── queries/   session · batch · job · wait · operation · artifact · thumbnail · drama_config · global_config · entity · history  (__query.py)
│   │   ├── dtos/      {同名}__dto.py
│   │   └── mappers/   {同名}__mapper.py
│   └── infrastructure/
│       ├── clients/   jimeng_browser__client.py(BrowserActor) · jimeng_page__map.py · dreamina_cli__client.py · toast__client.py
│       ├── readers/   shot_prompt__reader.py · asset_card__reader.py · drama_tree__reader.py · jimeng_response__reader.py
│       │              thumbnail__reader.py · drama_config__reader.py · global_config__reader.py
│       ├── writers/   store__writer.py(SQLite) · output__writer.py · drama_config__writer.py · artifact__writer.py
│       │              web_ui_backend__writer.py · dreamina_cli_backend__writer.py
│       ├── daos/      job__dao.py · batch__dao.py · operation__dao.py · jimeng_history__dao.py · dreamina_result__dao.py · entity_snapshot__dao.py
│       ├── errors/    jimeng_browser__error.py · dreamina_cli__error.py · config_io__error.py · sandbox__error.py
│       └── middleware/ request_class__middleware.py · security_headers__middleware.py
├── tests/  (镜像源码树；fixtures/fake_jimeng_site/ · fixtures/fake_dreamina/ · fixtures/real_shots/ · fixtures/real_cards/ · fixtures/real_responses/)
└── .data/  (gitignored：bridge.db · secret.key · chrome_profile/ · artifacts/ · logs/ · tmp/)
```

---

## 8. Divergence notes

1. **MCP 工具层级。** `development.md` 没有定义 MCP 的层级，这里新增 `apps/api/mcp_tools/{aggregate}__tool.py`，规则与 routes 相同：一个工具映射一个 Query / Command 方法；工具文件与它的 provider 在同一个变更里落地。
2. **剧根解析重新实现。** 项目之间不能互相 import，所以本项目在 `libs/common/drama_ref.py` 里按**同一条 `series.json` 规则**重新实现（不按路径深度判定）。另外叠加 FR-10 的「可列入」条件，用来排除 `notes/`。契约测试针对真实 `ai_videos/` 树运行。
3. **运行时数据放在项目目录下的 `.data/`**（gitignored）。它不是 CLAUDE.md 所说的 workflow 状态面。
4. **新增 `ai_videos` 结构文件**：剧根下的 `jimeng_config.toml`、产物旁的 `*.jimeng.json`，以及 `_candidates/` 目录。
5. **行尾。** 仓库 `core.autocrlf=true` 且没有 `.gitattributes`，所以 FR-8 在读入时统一成 LF。给 `ai_videos/**/*.md` 加 `.gitattributes`（`eol=lf`）属于仓库级改动，不在本项目范围内，作为建议记录。

---

## 9. Acceptance criteria summary（完整条目见 `validation/`）

1. **离线端到端**：Fake 站点 + hy3 `shot02.md`（prompt 2314 码点）走完 precheck → UI 确认 → 执行，检查以下结果：
   - 控件设为 2.5 / 16:9 / 22s；
   - **3 个素材按 stem 上传**（`bg11-1`、`p2-1`、`p3-1`，只匹配 hy3 自己的文件）；
   - **1 个主体 mention** `hy3_主角`（经 override）；
   - verify 通过；
   - 产物落到 `renders/shot02_*.mp4`，sidecar 字段齐全。
2. **确认闸门**：
   - 任何入口都不能让未确认的作业进入 `submitting`，也不能进入非调试的 `preparing`；
   - bearer 访问 `/ui-api/*` → 403，MCP 没有确认工具；
   - token 过期、篡改、重放 → 拒绝；
   - 确认后改动参考文件 → `inputs_changed`。
3. **崩溃安全**：在 `submitting` 前后杀进程再重启 → 作业进入待人工处理，生成按钮的点击次数为 0 或 1，**绝不出现第 2 次**。只能在 UI 裁决。
4. **暂停分级**：
   - 注入验证码 → web 队列暂停，CLI 不受影响；
   - 注入审核拒绝 → 该作业 `failed`，其余继续；
   - 点击后注入并发上限提示 → `submit_rejected`，不会再点。
5. **并发与间隔**：`submitting` + `generating` ≤ 3；两次提交间隔 ≥ 15 s；点击前出现并发上限提示 → 不点，继续等待。
6. **幂等**：同样内容再预检，返回同一作业（指纹不含时间戳文件名）；`reroll` 产生新的 attempt。
7. **config**：
   - 对 hy3 做 propose → `abbrev=hy3`；在含 `hy3_主角` 的主体快照下标出「可能已有同一角色的主体」；
   - 保存后注释仍在；
   - 非法值与取值越界被拒；
   - 并发保存 → 409；
   - bearer 写全局 config → 403。
8. **解析**：
   - 旧写法（rexue `=>@1`、wushen `名字=>`、xianjian 无括号）→ `legacy_reference_syntax`；
   - 多重匹配 → 报出 override 键；
   - 负向引用块被正确提取；
   - `参考:` 行无法识别 → 报错，不静默处理。
9. **CLI 出图与 turntable**：
   - fake dreamina text2image → 候选 → promote 为 `{key}.png`，旧文件与 sidecar 一起归档；
   - `c1-2` turntable 块走网页视频，参考 `c1-1`；
   - CLI 未登录时 CLI 队列暂停。
10. **MCP**：10 个工具全部在 85 s 内返回；`wait` 有进度通知；结果 ≤ 20k token；业务错误返回 `isError` + 建议。
11. **安全**：非法 Host、伪造 `Sec-Fetch` 但没有会话 cookie、缺少 token、沙箱逃逸（UNC / ADS / junction）→ 拒绝；token 不出现在任何输出里。
12. **UI**：7 个页面在真实浏览器里的成功态和错误态；确认页合计积分与 API 一致；axe 检查无 mandatory 违规。
13. **真实站点只读 canary**：人工触发，全部通过，不点击生成（手工 walkthrough）。

---

## 10. Open questions（stage 6 开工时对真实站点做只读探针，结果回写 PageMap、config 默认值和本 spec）

1. **下载**：下载控件在哪里（「⋯」还是图标）？会员下载是否无水印？文件名是什么，时长和比例是否与生成参数一致？
2. **上传**：完成信号是什么？素材在 @ 候选里显示的名称是否等于文件 stem？
3. **提交**：提交响应里平台任务标识的字段是什么？`get_history_by_ids` / `get_history_queue_info` 里进度、状态、结果的字段是什么？采集后脱敏，存入 `tests/fixtures/real_responses/`。
4. **并发上限提示**：出现在点击之前还是之后，文案是什么？「平台在途数」能否从状态响应里读到？
5. **负向输入框**：Seedance 2.5 / 2.0 全能参考下是否有负向输入框？这决定 `model_limits.*.负向输入框`。
6. **2.5 的真实上限**：参考数量、主体是否计入图片上限、1080P 能否选、prompt 硬上限。`get_common_config` 能否作为能力矩阵的数据来源？
7. **主体表单**：能否上传视频？「添加角色」是什么？描述有无上限？
8. **CLI**：1.4.18 是否新增了 2.5、主体或 30 s 支持？退出码与 JSON 错误结构是什么？CLI 余额与网页余额是否同一个积分池？
9. **与 `ai_video_management` 的兼容**：`MediaRenamer` / `rename_drama` 会不会动 `renders/` 下的产物、`_candidates/` 或 `*.jimeng.json`？如会，调整本项目的 `outputs` 默认值，不改 webapp。
10. **Claude Code 实测**：Streamable HTTP 调用的实际截断点，`timeout: 120000` 是否生效。

---

## 11. Revision log（v1 → v2，来源为 stage-5 各 level 文件的编号）

| 改动 | 来源 |
|---|---|
| 只有 UI 身份能确认；移除 MCP `confirm_batch`、HTTP `auto_confirm` 与自动确认预算；confirmer 由服务端判定；新增 `/ui-api/*` 身份类别 | 用户 stage-5 决策；acceptance C4 · bdd AMB-21/22/23 · security G-2/G-9/SEC-C07 · unit A-02 |
| 旧版 `参考:` 写法一律报错，不能豁免 | 用户 stage-5 决策；acceptance C3 · bdd AMB-04 |
| 资产卡视频块（turntable）走网页视频，参考同卡立绘；新增 `[assets]` 配置 | 用户 stage-5 决策；acceptance G21 · unit A-15 |
| 点击后才出现的并发上限拒绝 → `submit_rejected`，不自动再点；点击前的判断用于等待 | acceptance C1 · bdd AMB-18 |
| `routing.image` 不可配置（固定 cli） | acceptance C2 |
| 准备只在拿到槽位后进行；点击前 verify；并发额度计入 `submitting` | bdd AMB-19 · acceptance G6 |
| 作业级原因 → 终态 / 待人工处理的完整表；恢复语义；`restart_during_submit` 等只能 UI 裁决；取消语义 | acceptance G2/G4/G12 · bdd AMB-13/15/16/17 · unit A-03 |
| 队列级暂停 = backend 队列标志 | bdd AMB-14 · unit A-04 · acceptance G19 |
| 并发与间隔为账号级（web + cli 合计） | bdd AMB-20 |
| 指纹 canonical 编码，改用 `output_slot`（不含时间戳文件名） | acceptance G5 · bdd AMB-24 · unit A-06 |
| 冻结请求，上传前重算哈希（`inputs_changed`） | acceptance G23 · security G-5/SEC-C05 |
| 页面预计积分超出已确认值 → 暂停等人批准 | acceptance G10 · security G-6 |
| 所有阈值进入全局 config 并加取值约束；每剧 config 禁止出现全局节 | acceptance G7 · unit A-08 · security G-4/G-15/G-8 |
| `price_table` 结构；图片按张计价；计数单位为码点 | unit A-09 · acceptance G18/G20 · bdd AMB-11 |
| prompt 规范化（BOM / CRLF） | unit A-07 |
| 负向提示词引用块识别；`参考:` 行多项切分与完整性校验；时长和比例的宽松解析；比例白名单 | bdd AMB-01/02/03 · acceptance G15 · unit 真实文件调研 |
| resolver 修订：路由键前缀匹配、主体目录主图、previz 别名与 `previz/` 子目录、`道具参考图`、`上一镜末帧*`；移除无数据的 `*声音` | bdd 真实数据统计 · acceptance G16 · unit 调研 |
| 首帧链式依赖不支持，末帧缺失即报错 | bdd AMB-07 |
| 主体名冲突的判定规则；跨集复用时的主体命名来源 | acceptance G24 · bdd AMB-09/10 · unit A-05 |
| 主体创建经批次确认页（`entity_create` 条目） | acceptance G11 · accessibility gap |
| sidecar 覆盖候选 / 升格 / 归档；字段白名单；含各阶段耗时 | acceptance G14 · security · performance 6 |
| 可列入的剧排除 `notes/` | acceptance G22 · unit 警告项 |
| 身份判定表（Sec-Fetch + 会话 cookie + bearer）；token 必填且 ≥ 32 字符；`proxy_headers=False`；MCP SDK ≥ 1.23；HMAC 密钥来源；`cli.path` 只能是 `.exe` | security G-1/G-3/G-12/G-13/G-14/SEC-N11/N12/D01 · unit A-01 |
| 只提供截图，DOM 与 trace 永不对外；截图不写入 `ai_videos/` | security G-11 |
| 下载只走页面下载控件（不用 `context.request`），流式落盘，内存增长 ≤ 64 MB | performance · security 静态禁用 |
| 长耗时操作改为后台 operation，所有调用 ≤ 85 s；分页；MCP 结果 ≤ 20k token；session 状态只读快照 | performance 1/2/8 |
| 新增 `/api/thumbs`；预演截图大小与保留期；性能 hard 预算扩充；`make test-perf` / `test-soak` | performance 3/4/5/7/9 · security G-10 |
| UI：token 倒计时与重新预检、三种「暂停」措辞、冻结刷新、3 s 轮询、无快捷键、二次确认用 alertdialog | accessibility gaps |
| §9.1 改为「3 个上传 + 1 个主体」 | acceptance G1 · bdd AMB-28 |
| 解析器使用探针采集并脱敏的真实响应作为夹具 | acceptance G25 · unit |
| 测试注入点 `JIMENG_BRIDGE_REPO_ROOT` / `_DATA_DIR` / `_GLOBAL_CONFIG`；测试模式下不加载 `.env`；测试专用 fault point 与 toast sink；fake dreamina 优先用 `.exe` | system C4/C7/C9 |
