# Validation strategy — jimeng_web_bridge

Run: jimeng_web_bridge-20260913-093603

Mode: strategy (stage 5)。parent-direct 编排，并行派出 7 个 level-specialist worker（审计记录见 `.audit/adhoc_agents/2026-09-13/jimeng_web_bridge-20260913-093603/spawns/level-specialist-0{1..7}-*`）。7 个 level 文件的 envelope 都已校验：`status: complete`。

> **Spec 版本说明。** 7 个 level 文件是照 **spec v1** 写的。它们暴露的冲突和缺口已由用户裁决或 parent 定稿，并入 **spec v2**（`final_specs/spec.md` §11 Revision log 逐条标注了来源编号）。**level 文件与 spec v2 冲突时，一律以 spec v2 为准。** stage-6 的运行时 validator 必须同时读 spec v2 和 §11；被取代的测试条目见下文「v1 → v2 取代表」。

## Levels chosen

- **acceptance_criteria** — 必选。约 110 条 Gherkin，覆盖 F1–F7、FR 各组和安全 / 账号风险 NFR，附 FR-1..56 的追溯矩阵。
- **bdd_scenarios** — 必选。规则很重的部分（参考项解析、主体命名、能力矩阵、状态机、暂停分级、幂等、命名、调度、负向提示词）用 Scenario Outline + Examples，拿全仓 271 条真实 `参考:` 行跑过。
- **unit_tests** — 纯函数和解析器很多：预检、指纹、token、状态机、读取器、写入器、中间件。
- **system_tests** — 前后端、浏览器、CLI、SQLite、MCP 必须合起来验证；只有一种运行模式，对应一个 e2e profile。
- **security** — 涉及 bearer token、身份判定、花积分授权、文件沙箱、子进程、机密卫生、账号条款护栏。
- **accessibility** — 7 个 UI 页面，而确认、取消、选定这类动作要么花积分、要么移动文件，必须能用键盘和读屏安全操作。
- **performance** — spec 写明了时延和内存预算：调用 ≤ 85 s、查询 p95、首屏、下载内存等。

## Per-level summary

### Acceptance criteria（`acceptance_criteria.md`）
- 黄金路径：hy3 shot02。3 个上传 + 1 个主体 mention `hy3_主角`；只匹配 hy3 自己的 `bg11-1.png`（hy1、hy2、hy4 各有一张同名文件作为陷阱）；产物落 `renders/`，sidecar 字段齐全。
- 确认闸门在 7 个入口上做负面测试，外加 token 过期、篡改、重放；在点击前后分别崩溃（点击数只能是 0 或 1，绝不出现第 2 次）。
- 追溯矩阵覆盖 FR-1..56。C1–C4 与 G1–G25 已并入 spec v2。

### BDD scenarios（`bdd_scenarios.md`）
- 参考项解析表直接用真实条目。v1 的默认规则实测大面积解析失败：图片 178/382 找不到文件，previz、末帧几乎全挂，负向提示词主要写在引用块里。这些都促成了 v2 的 resolver 修订。
- 状态机、暂停分级、幂等（`idempotency_key` + 指纹 + `reroll`）、调度（上限 3、间隔 15 s、背压）各有一张 Examples 表。
- AMB-01..29 均已在 spec v2 裁定（见 §11）。

### Unit tests（`unit_tests.md`）
- 按层组织，编号形如 `UT-{层}-{聚合}-NN`。包含：状态机全对转移表；每个 config 键的合法和非法样本（兼作 FR-5 契约表）；解析器使用 18 份真实 shot 副本（S1–S18），外加全仓 sweep。
- Windows 与 POSIX skip marker 对照表。`JWB_REQUIRE_PROBE` / `JWB_REQUIRE_FFPROBE` / `JWB_REQUIRE_REAL_REPO` 在 sign-off 时把 skip 转为 fail，防止「全 skip 看起来是通过」。
- 中间件：没有 dev proxy，dev-proxy 前后改写的两形态测试（§11）不适用；另设两条守护测试：确认没有配置 dev proxy、确认不信任 forwarded header。

### System tests（`system_tests.md`）
- harness：
  - Fake 即梦站点：真实 TipTap、点击和上传账本、24 种故障注入；
  - fake `dreamina.exe`；
  - 临时 `ai_videos/` 子集；
  - 6 层硬护栏，保证测试不可能触达真实站点、不可能花积分（spec v2 已补上测试注入点）。
- boot_smoke（SYS-01..07，critical）；黄金路径 SYS-10；MCP e2e（进度通知、`isError` 附建议）；按 Windows `taskkill` 的崩溃安全（SYS-30..34）；暂停分级、调度、浏览器丢失、CLI 出图、主体流程。
- 覆盖前后端契约：每个改状态的端点都在挂载了静态 UI 的模式下测，并做 405 sweep；`{drama}` 用 URL 编码的系列路径；`/api/dramas` 按 UI 真实读取的字段路径遍历；16 个共享 JSON 形状与 UI 字段路径逐一对照；7 个页面各测成功态和错误态。

### Security（`security.md`）
- 87 条 SEC-*，全部 `critical`。
  - 身份判定表：Sec-Fetch + UI 会话 cookie + bearer；另测 uvicorn 必须 `proxy_headers=False`、`/mcp` 挂载后的路径形态、MCP SDK ≥ 1.23（CVE-2025-66416）。
  - 花积分授权：token 伪造、重放、过期；bearer 访问 `/ui-api/*` 一律 403；冻结请求在上传前重新校验。
  - 文件沙箱表：UNC、设备路径、ADS、保留名、结尾点、junction、前缀相同的兄弟目录。
- 机密卫生：用哨兵 token 追踪日志、数据库、sidecar、响应；sidecar 字段走白名单；截图不写入 `ai_videos/`（pre-commit 会把那里的媒体推到 R2）；DOM 快照和 trace 不对外。
- 静态禁用 `route`、`context.request`、`expose_binding`、CDP 端口，并扫描 stealth 或验证码求解类依赖。其余账号条款风险属于用户已知情接受的范围。

### Accessibility（`accessibility.md`）
- 54 条 mandatory（blocker）、13 条 recommended（warning）、11 项人工 walkthrough。
- 花积分和移动文件的动作：进入页面时焦点不在确认按钮上；在文本框里按 Enter 不会触发确认；读屏能播报合计积分；`alertdialog` 默认聚焦安全选项；看板重排后焦点仍停在同一个作业上。
- 状态变化按 5 s 合并后礼貌播报；队列暂停在所有页面顶部横幅提示；状态不只靠颜色表达；浅色主题对比度达标；深色 TOML 面板达 AA；支持减少动态效果。

### Performance（`performance.md`）
- 21 条 PERF-*，其中 14 条 hard。「3 次里 2 次不达标才算 miss」用来过滤计时噪声。
- 调用 ≤ 85 s，进度间隔 ≤ 25 s，MCP 结果 ≤ 20k token；重负载时 `/api/health` p95 ≤ 100 ms，`/api/jobs` p95 ≤ 200 ms，事件循环单次卡顿 ≤ 500 ms；查询 p95 ≤ 500 ms（1000 个作业）；首屏 ≤ 2 s；启动 ≤ 8 s；空闲 CPU ≤ 2 %；下载内存增长 ≤ 64 MB。
- `make test-perf` 在 Windows 开发机上自动跑，只用 fake 站点和 fake CLI；8 h soak 和真实站点的计时都是 observe-only 或人工项。

## Cross-cutting concerns

- **Fake 站点必须和真实页面对得上。** stage 6 开工先做真实站点只读探针：DOM 快照 + 脱敏响应。PageMap 的每个 selector 都要同时在「真实快照」和「fake 站点」上解析成功；解析器夹具只用脱敏后的真实响应。探针完成前，依赖它的测试一律 skip，sign-off 时靠 `JWB_REQUIRE_PROBE=1` 转为 fail。
- **真实上游产物作为夹具**（development.md §10）：真实 shot md 和资产卡的副本放进 `tests/fixtures/real_*`；全仓 sweep 在仓库树存在时运行。媒体字节在 R2，新 clone 未 pull 时相关测试 skip，sign-off 时靠 `JWB_REQUIRE_REAL_REPO=1` 转为 fail。
- **Windows 专项。** 杀进程用 `taskkill /T /F`；junction 要真的建出来测；`dreamina` 必须是 `.exe`；`os.replace` 与大小写不敏感相关的断言要带 skip marker；行尾问题（`core.autocrlf=true`）用 CRLF 夹具覆盖。
- **时钟与定时。** token TTL、提交间隔、等待超时、每日统计都要能通过 DI 注入时钟；调度相关测试使用缩放后的测试 config。
- **隔离与复位。** 每个场景都用独立的临时仓库根、`.data/`、fake 站点端口和 profile。`JWB_TEST_MODE=1` 不加载真实 `.env`，启动前后各校验一次实际生效的 config。
- **两套 backend 共用账号级并发和提交间隔**，调度测试必须混合 web 和 cli 作业。
- **易抖区域。** 事件循环时延、下载限速、Playwright 下载事件时序、页面自动滚动。缓解办法：按记录定位元素、用账本断言，不依赖视觉坐标。

## How runtime validation will use this

stage 6 拆成下列 work unit，按顺序执行（U4 和 U5 在 U3 之后可以并行）。每个 unit 完成后先发 `validation.started`（带 `pre_reading_consulted`），再按 level 并行派 validator：

| # | work_unit_id | work_unit_kind | 内容 | 运行的 level |
|---|---|---|---|---|
| U0 | `site_probe` | `manual_probe` | 真实站点只读探针，采集 DOM 快照和脱敏响应，回答 spec §10 的问题，回写 PageMap 与 config 默认值 | 人工 walkthrough（`validation.requires_manual_walkthrough`），security 静态禁用项自查 |
| U1 | `domain_core` | `backend_domain` | 值对象、实体（作业、批次、operation 状态机）、预检、指纹、确认 token、能力矩阵 | unit_tests（domain）、bdd_scenarios（规则表） |
| U2 | `inputs_and_config` | `backend_adapters` | ShotPromptReader、AssetCardReader、DramaTreeReader、drama_ref、TOML 配置读写、propose | unit_tests（readers、writers）、bdd_scenarios（解析、命名）、acceptance（config / 解析子集）、security（沙箱） |
| U3 | `service_shell` | `backend_api` | FastAPI、身份中间件、SQLite store、Commands/Queries、HTTP routes、MCP tools、调度器（配 FakeBackend）、operation 机制 | **boot_smoke（critical）**、unit_tests（application、middleware、mcp）、system_tests（T1/T2、端点矩阵、405 sweep、consumer walk）、security、performance（API 相关）、acceptance（闸门 / 幂等 / 暂停） |
| U4 | `web_ui_backend` | `backend_integration` | BrowserActor、PageMap、设参数、上传、填写与校验、预演、提交、状态解析、下载，以及 Fake 站点 | unit_tests（clients、parsers）、system_tests（T3 黄金路径、崩溃安全、暂停、浏览器丢失）、security（静态禁用、截图卫生）、performance（事件循环、下载内存） |
| U5 | `cli_backend_assets` | `backend_integration` | DreaminaCliClient、图片与 turntable 流程、候选与 promote、主体同步和创建 | unit_tests、system_tests（CLI、主体流程）、security（子进程）、acceptance（F5/F6） |
| U6 | `management_ui` | `frontend_component` | React 7 页、共享类型 | system_tests（逐页 e2e、共享类型对照）、accessibility、performance（首屏）、acceptance（UI 子集） |
| U7 | `end_to_end` | `e2e` | 全链路：propose → 预检 → UI 确认 → 执行 → 落盘 → 历史；MCP e2e；`make test-perf` | acceptance（全部）、system_tests（全部）、performance（hard 预算）；**最后发 `validation.requires_manual_walkthrough`**（UI 人工走查 + 真实站点只读 canary + 由用户确认的首次真实出片） |

**判定规则**
- severity 依 `agent_refs/validation/general.md` 与 `development.md`：
  - 安全失败、沙箱逃逸、boot 期异常、前后端形状漂移、深链空白页 → `critical`，立即 halt；
  - 验收或黄金路径失败、hard 预算未达、mandatory a11y 失败 → `blocker`，最多 3 轮修订；
  - recommended 与 observe-only 项 → `warning`。
- 同一 `issue_id` 连续两轮复现 → 发 `pipeline.halted`。
- 全部自动化 level 通过后，发 `validation.requires_manual_walkthrough`。**第一次在真实站点点「生成」必须由用户在 UI 里亲自确认。**

## v1 → v2 取代表（level 文件中照 v1 写的条目，运行时按 v2 执行）

| level 文件中的 v1 条目 | v2 下的执行方式 |
|---|---|
| MCP `confirm_batch`、HTTP `auto_confirm` 与自动确认预算的测试（acceptance、system SYS-29、security budget 类、a11y 无关） | 改为断言「MCP 没有确认工具；bearer 访问 `/ui-api/*` 一律 403；只有 UI 身份能确认；confirmer 恒为 `ui_human`」 |
| 点击后遇到「并行上限」→ 回到等待（bdd AMB-18 行、system C2） | 改为 `paused_needs_human(submit_rejected)`，点击数保持 1 |
| 旧写法可经 config override 解决（bdd AMB-04 相关行） | 改为 `legacy_reference_syntax` 错误，且不能豁免 |
| `routing.image = web` 的相关行 | 删除；`routing.image` 固定为 cli |
| 资产卡的 `c1-2` turntable 块被当作图片块（unit A-15） | 改为视频块，走网页、参考 `c1-1`；hy3 c1 卡产出 1 个图片请求 + 1 个视频请求 |
| `resume` 作用于 `restart_during_submit`（system C3） | 改为 API/MCP 拒绝，只允许 UI 裁决（三选一） |
| 指纹包含带时间戳的输出文件名 | 改用 `output_slot` |
| 负向提示词只识别 `##` 标题（system C5） | 引用块和标题两种形式都识别 |
| §9.1「4 个参考上传」 | 3 个上传 + 1 个主体 mention |
| `wait` / MCP 调用上限 90 s | 85 s（`api.max_call_s`） |
| 测试注入方式未定义（system C4） | 使用 `JIMENG_BRIDGE_REPO_ROOT` / `JIMENG_BRIDGE_DATA_DIR` / `JIMENG_BRIDGE_GLOBAL_CONFIG`，`JWB_TEST_MODE` 下不加载 `.env` |

## Carve-outs（stage-5 sign-off 需用户确认不在自动化验证之内）

1. **只有一种运行模式**（`make run`），不做 Vite dev 模式，也就没有它的 e2e profile。
2. **不自动化测试真实站点上的生成、下载、水印和实扣积分**，只做人工触发的只读 canary、U0 探针，以及由用户确认的首次真实出片人工 walkthrough。
3. **不做 Windows Service 形态。**
4. **不对真实站点做性能测试**；8 h soak 与真实站点计时只作 observe-only。
5. **旧版 `参考:` 写法**：只验证会报错，不验证兼容。
6. **同批次内的首帧链式依赖**不支持，只验证会报错。
7. **与 `ai_video_management` 的 `MediaRenamer` 兼容性**（spec §10 Q9）不做自动化测试，由 U0/U7 人工核查。
8. **威胁模型不含**「同一 Windows 用户下蓄意冒充浏览器的本地进程」，也不含「Claude 用浏览器自动化去点本 UI 的确认按钮」（后者由 README 约束）。
9. **账号条款风险**（即梦用户协议 5.1）属于用户知情接受的范围；平台侧如何执行无法验证，只验证 service 自身的护栏。
10. **observe-only 指标**：2 万个作业时的查询时延、单作业准备时长、canary 时长、soak 增长——超出只记 warning。

## Promotion-preservation check

本任务各阶段目录下都**没有** `<stage>/promoted.md`，因此没有需要保留的 pin。按规则，stage 6 不生成这项检查。

## Stage-6 severity decision（用户，2026-09-14）

对 `agent_refs/validation/general.md`「Security failure → critical，未经用户明确同意不得进入修复轮」的**本项目 override**：

- **文件沙箱 / 路径校验类** critical（不涉及积分、账号、确认闸门），parent 可以直接进入修复轮，事后在汇报里说明，并在 `events.jsonl` 里记 `user_approval: standing`。
- **涉及花积分、账号、确认闸门的** critical 仍须逐次征得用户同意。

来源：interview/qa.md「Stage-6 decisions」。
