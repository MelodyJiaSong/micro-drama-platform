# Findings dossier — jimeng_web_bridge

Run: jimeng_web_bridge-20260913-093603

## Angles researched

1. **page-anatomy**（parent 直接执行，Claude in Chrome 实地勘察 + 本机 CLI 检查）— 即梦网页真实的控件、编辑器、@ 绑定、状态接口、主体表单长什么样。
2. **prior-art** — 社区已有的即梦 / Dreamina 自动化走的是什么路线，哪些活下来了，哪些死了、封了。
3. **platform-limits-risk** — 队列、预检、积分预估、暂停逻辑必须写进去的上限、成本与条款。
4. **browser-automation-reliability** — 常驻 headful Playwright service 靠什么天天稳定跑，要预设哪些失败模式。
5. **mcp-http-interface** — 耗时数分钟、要花积分、可能卡在人工环节的作业，怎么同时暴露给 HTTP 和 Claude Code MCP。

## Cross-cutting insights

- **即梦官方 CLI `dreamina` 改变了立项前提，但替代不了网页。**
  - 现状：本机已原生安装 1.4.5 并登录（ultra，8712 积分），官方最新版是 1.4.18。它是官方渠道，走的是账号积分，不碰 DOM，也就没有条款风险。
  - 能覆盖：Seedream 出图（`text2image` 3.0–5.0、2k/4k；`image2image` 1–10 张），以及 Seedance 2.0 全能参考（≤9 图 / 3 视频 / 3 音频，4–15 s）。
  - 覆盖不了：仓库当前的出片方式——Seedance 2.5、16–30 s、`@主体`、单条到 50 个参考。
  - 结论：合理形态是 **一个 `GenerationBackend` 端口 + 两个 adapter（网页 UI / 官方 CLI）**，队列、预检、确认、落盘这些逻辑两个 adapter 共用。 *(prior-art + page-anatomy)*
- **条款明文禁止自动化，只能「知情接受 + 压小暴露面」。** 用户协议 5.1 写的是「不得使用任何自动化程序……接入即梦AI」，付费协议 6.5 / 8.2 可以作废权益、封号。这对 UI 自动化同样适用。压小暴露面的手段：
  - 单账号、单个持久化 profile；
  - 只绑 127.0.0.1；
  - 按人的节奏提交，设每日积分预算；
  - **提交这一步零自动重试**；
  - 不做任何对抗检测；
  - 能走官方 CLI 的就走 CLI。 *(prior-art + platform-limits-risk + browser-automation-reliability)*
- **重放内部接口这条路被实证否定，被动读响应这条路被实证可行。**
  - 否定：生成和历史请求都带 `msToken` / `a_bogus` 签名；社区的 cookie 重放项目 12 个月内相继归档，还有 `1019 shark not pass`、「unusual activity」的报告。
  - 可行：页面自己在轮询 `get_history_queue_info`、`get_history_by_ids`（外加 `subscribe_session` 长轮询）。在 CDP 层监听这些响应就能拿到状态，不必伪造任何请求。页内 monkey-patch 抓不到，要用 Playwright 的 `page.on("response")`。 *(page-anatomy + prior-art + browser-automation-reliability)*
- **`=>@` 的绑定契约其实已经存在。**
  - 用户手工出片时，上传的素材按**文件名 stem** 被 @（`bg14-1`），人物项 @ 的是主体名（`hy3_主角`）。
  - 仓库的路由键契约（`libs/common/asset_key.py`，文件名即路由键）刚好给 shot 适配层提供了确定性映射：`{key}(类型)=>@` → 上传 stem 为 `key` 的文件 → @ 这个 stem。
  - 社区里没有任何项目自动化过即梦的 @ 编辑器和主体，这部分只能自研，也要自己维护。 *(page-anatomy + prior-art)*
- **「质量优先 + 最高分辨率」这个默认值和平台上限有冲突。**
  - 2.0：最长 15 s，可以出 1080p。
  - 2.5：最长 30 s，第三方资料说最高 720p（页面弹层虽然列出了 1080P，但没核实 2.5 能不能选）。
  - 仓库很多镜在 16–30 s，只能用 2.5。
  - → 必须写死「时长 → 模型 → 分辨率」的决策顺序，并在确认环节把选择结果显示出来。 *(platform-limits-risk + page-anatomy + qa)*
- **积分以页面自报为准，价差动机要按实测验证。**
  - 页面提交前会显示预计积分（2.5 · 26 s · 720P → 520，划线原价 676），「详细信息」里有实际消耗。
  - 研究推算：网页相对 API 只在部分档位便宜（2.0 标准排队通道约便宜 1.2–4 倍；2.5 720p 持平或更贵）。页面横幅称「2.5 720P 低至 0.4 元/秒」。
  - → 每个 job 记录预估与实扣积分，由实测数据判断省不省。 *(platform-limits-risk + page-anatomy)*
- **MCP 调用必须短，确认必须显式。**
  - Claude Code 约 5 min 空闲超时、Streamable HTTP 约 6 min 截断（#93143）、HTTP 下 elicitation 不弹框（#85442），也不支持 MCP tasks 扩展。
  - 同时，积分不能被静默花掉。
  - 两者合起来定下接口形态：`precheck_batch` 返回一次性确认 token → `confirm_batch(token)` 才入队 → `wait_job` 有界等待 ≤ 90 s、循环调用。
  - `confirm_batch` 不进 Claude Code 的 allow 列表；`auto_confirm` 只在 HTTP 上开放。 *(mcp-http-interface + prior-art)*
- **「提交」必须是崩溃安全的单次动作。**
  - 点「生成」之前先持久化 `submitting` 和指纹；重启后遇到这种状态一律 `paused_needs_human`，由人去历史里核对。
  - 页面自动滚动、编辑器失焦会追加内容，所以填完必须校验（纯文本 + mention 节点），不一致就绝不提交。
  - UI 动作由单个 browser actor 串行执行。并发上限只限制「远端同时在渲染」的条数；这个账号手动时常态就是 2–3 条并发。 *(browser-automation-reliability + mcp-http-interface + page-anatomy)*

## Per-angle highlights

### page-anatomy

- 工具栏：`创作类型 | 模型 | 参考模式 | 比例·分辨率·数量 | 时长 | @ | 预计积分 | 发送`。
  - 模型含 Seedance 2.5 / 2.0 mini / 2.0 Fast VIP / 2.0 VIP / 2.0 Fast 等。
  - 参考模式：全能参考 / 首尾帧 / 智能多帧 / 智能编辑 / 超长视频。
  - 比例 6 种，480/720/1080P，数量 1–4，时长 0–30 s。
- 编辑器是 **TipTap / ProseMirror**；页面上没有常驻的 file input。
- @ 选择器列出主体，第一行是「+ 创建主体」。主体名 ≤ 20 字。「设置主体」弹窗的字段是参考图 + 添加角色 + 名称 + 描述，**没有看到视频上传位**。
- 已有主体 `hy3_主角`、`hy1_主角`、`xj_*`，与 interview 定的「目录中文名」规则不一致。
- 结果是带签名、会过期的 CDN 视频地址。下载入口和是否带水印没有核实。
- CLI 1.4.5：`multimodal2video` 只支持 2.0 系列、4–15 s，没有主体参数；`text2image` / `image2image` 覆盖 Seedream。

### prior-art

- 路线 A（cookie 重放）：主力项目归档或删库，签名闸门挡路，有风控报告。**不采用。**
- 最接近本项目的是 DanikVR/dreamina-seedance-mcp（MIT）：MCP 只做传输，5 个工具（status / generate 立即返回 jobId / edit / wait / cancel），明确拒绝绕过验证码、私有 API、去水印。
- 反面教材：Seedance Automation 扩展，并发 6、自动重试 20 次。
- License：GPL-3.0 的项目不拷代码；MIT / Apache 的项目可以参考结构并注明出处。

### platform-limits-risk

- 按模型的上限：
  - 2.0：4–15 s，1080p 仅标准版，素材 ≤ 9 图 / 3 视频 / 3 音频。
  - 2.5：≤ 30 s，最高 720p，素材 ≤ 30 图 / 10 视频 / 10 音频（第三方来源）。
- 以下都**没有公开数字**：并发上限、审核失败是否退积分、网页端 prompt 长度硬上限（第三方 API 文档写 500 字，仓库规则是 5000，都没有网页出处）。
- 排队几小时是常态 → 等待超时按小时计，重启后恢复轮询，不重新提交。
- 2026-02-09 起网页端拒绝真人素材做主体；写实人像也可能被拦。
- 会员下载去水印（付费协议 4.1.1）；AI 生成内容标识办法要求保留隐式标识，不得剥离元数据。

### browser-automation-reliability

- Profile：专用目录；锁残留或损坏要分类报出来，**不自动删锁**；记录浏览器版本。
- 用户手动关掉浏览器时 Playwright 行为不一致 → 监听 `close` / `crash`，进入 `browser_lost`，暂停队列，然后重建 → 检查登录 → 对账。
- 富文本编辑器：`fill` 失焦后会追加；中文逐字 type 与 `insert_text` 事件相同 → 填充策略做成可切换，由 canary 选定，填完必校验。
- 被动读 body 容易报「No resource with given identifier」→ 回调里立刻读，读失败计数；解析失败算 `page_contract_broken`，不算 job 失败。
- 下载：先写临时文件 → 校验 size / sha256 / ffprobe → 原子 rename → 写 sidecar。
- Playwright 非线程安全 → 在 uvicorn 内用 async API + 单 actor；取消只在动作之间的检查点生效。

### mcp-http-interface

- MCP 挂在同一个 FastAPI 进程的 `/mcp`（Streamable HTTP），共用 DI container；只绑 127.0.0.1，校验 Host / Origin，外加 bearer token（放 `.env`）。
- 所有 tool 在 90 s 内返回；`wait_job` 做有界等待；不用 elicitation，不用 MCP tasks。
- 两层幂等：客户端 `idempotency_key`（Stripe 语义）+ 服务端指纹。有意重抽要显式传 `reroll: true`。
- 状态机存在 SQLite（WAL），`submitting` 在点击之前落库；暂停原因有：`captcha` / `moderation_reject` / `login_expired` / `restart_during_submit` / `dom_changed`。
- tool 总数约 10 个；截图返回路径 + 缩略图；`windows-toasts` + AUMID 做通知，但它只是尽力而为，真相以作业状态为准。
- `development.md` 没有定义 MCP 的层级落点 → spec 要写 divergence note（建议 `apps/api/mcp_tools/{aggregate}__tool.py`）。

## Recommendations for the spec

1. **端口 + 双 adapter**：`GenerationBackend` 协议，实现 `WebUiBackend`（Playwright headful）与 `DreaminaCliBackend`（子进程调用官方 CLI）。每个生成请求按「能力矩阵」路由：模型、时长、参考数量、是否用主体、是否是图片。*（待用户确认，见下方开放问题 1）*
2. **输入统一成一个 `GenerationRequest` 值对象**（prompt 文本 + 有序参考项 + 主体引用 + 参数 + 目标输出路径），三种入口都规范化成它：原始参数、`shotNN.md`、资产卡。
   - shot 适配层解析 `参考:` 行，`{key}(类型)=>@` → 盘上 stem 为 `key` 的文件；人物项 → 主体名。
   - 资产卡适配层解析以路由键开头的 ```text 块。
3. **预检是纯函数，能跑在任何 backend 之前**，检查项：
   - 文件都存在；
   - 数量与格式符合所选模型的上限表（放配置、带 `as_of`）；
   - 时长 → 模型 → 分辨率决策；
   - prompt 长度（可配置，默认沿用仓库 5000 契约）；
   - 主体名存在、≤ 20 字；
   - 指纹去重。

   浏览器侧预演（填表 + 截图 + 读页面预计积分）作为可选的第二段预检。
4. **确认闸门**：`precheck_batch` → HMAC 一次性 token（绑定内容摘要、预估积分、过期时间）→ `confirm_batch`。HTTP 上的 `auto_confirm` 默认关闭，并受每日积分预算约束。
5. **作业状态机持久化到 SQLite**（service 数据目录，gitignored）。`submitting` 在点击前落库；重启遇到这个状态 → `paused_needs_human`。**提交零自动重试**；上传、填表、下载可以重试。
6. **暂停分级**：
   - 整个队列暂停 + toast：`login_expired` / `captcha_or_risk_popup` / `insufficient_credit` / `page_contract_broken` / `browser_lost`。
   - 单个 job 失败：`moderation_reject` / `real_face_rejected`。
7. **selector registry + canary**：selector 集中放在一个 page-map 模块，带 `web_version` 标注。canary 在每批开始前做只读自检（登录、编辑器、上传入口、参数控件、生成按钮、状态接口可截获），失败就暂停。失败现场留截图 + DOM 快照 + trace chunk。
8. **落盘**：
   - 视频 → `shots/shotNN/renders/{shotNN}_{YYYYMMDD-HHmmss}.mp4` + 同名 `.json` sidecar；
   - 图片 → 资产主体目录 `{routing_key}.png` + sidecar；
   - 下载经临时文件 → 校验 → 原子 rename；不剥离元数据。
9. **传输**：FastAPI `/api/*` + 挂载的 `/mcp`，每个 route 和 MCP tool 各映射一个 Query / Command 方法，只绑 127.0.0.1 + token。MCP tool 放 `apps/api/mcp_tools/` 并写 divergence note。
10. **README 写明**：账号条款风险（用户知情接受）、上传素材授予字节优化模型的权利、真人或写实人像素材可能被拒。

## Open questions surviving research

1. **backend 策略**：网页为主 + CLI 补位，还是只做网页，还是只做 CLI？这改变了立项前提，需要用户定。 *(prior-art, page-anatomy)*
2. **默认模型档**：「质量优先」遇到「2.5 最高 720p / 2.0 最长 15 s」时怎么取舍？ *(platform-limits-risk, page-anatomy)*
3. **主体命名迁移**：已有的 `hy3_主角` 与规则 `hy3_砌炉的老人` 冲突，怎么处理？另外建主体的弹窗里没有 turntable 视频位。 *(page-anatomy)*
4. **并发默认值**：研究建议 1；这个账号手动时常态是 2–3。 *(platform-limits-risk, page-anatomy)*
5. **stage 6 探针再确认的页面细节**：
   - 下载入口与水印；
   - 上传完成信号；
   - mention 候选项的 DOM；
   - 提交接口与平台任务 id；
   - `get_common_config` 是否带上限。

   *(page-anatomy, browser-automation-reliability)*
6. **CLI**：
   - 1.4.18 是否已支持 2.5 或主体？
   - CLI 的 8712 积分与网页的 1.1万 是否同一个积分池？
   - 网页端 prompt 长度硬上限是多少？

   *(page-anatomy, platform-limits-risk)*
7. **Claude Code 实测**：本机版本上 MCP 的截断点与超时配置是否生效，stage 6 集成时测。 *(mcp-http-interface)*
