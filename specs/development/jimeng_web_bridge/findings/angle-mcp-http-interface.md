---
worker_id: researcher-04-mcp-http-interface
stage: 3
role: researcher
angle: mcp-http-interface
status: complete
blockers: []
confidence: medium
---

# Angle: mcp-http-interface

## 1. What this angle covers

一个常驻本地 service（持有 headful 浏览器 + 作业队列）如何同时向 HTTP 客户端与 Claude Code（MCP）暴露「耗时数分钟、花积分、可能卡在人工环节」的作业：传输形态、异步句柄、precheck → 确认、进度与暂停通知、幂等防重、作业状态机与持久化、Windows 桌面通知。事实类结论均附来源；**标「观点」的是本 worker 的判断**。confidence 取 medium：规范事实为 high，但 Claude Code 客户端行为变化快、且有多个未修 bug，推荐方案依赖这些 bug 的现状。

## 2. Key findings

### 2.1 MCP 规范现状（截至 2026-09）

- **2025-11-25**：tasks 以 *experimental* 形式进入核心（SEP-1686），工具级 `execution.taskSupport: forbidden | optional | required`；新增 URL-mode elicitation。[S1][S7]
- **2026-07-28（现行版）大改** [S2]：
  - 去掉协议级 session 与 `Mcp-Session-Id`；原文："Servers that need cross-call state use explicit, server-minted handles passed as ordinary tool arguments"（SEP-2567）。
  - tasks 移出核心，成为扩展 `io.modelcontextprotocol/tasks`：用 `tasks/get` 轮询 + `tasks/update` 回填输入，删除 `tasks/result` 与 `tasks/list`。
  - server 主动发起的 `elicitation/create` 被 **MRTR** 取代：返回 `InputRequiredResult`（`resultType: "input_required"`）+ `requestState`，客户端带 `inputResponses` 重发原请求。
  - `resources/subscribe` 被 `subscriptions/listen` 取代；`notifications/progress` 仍走所属请求的响应流。
  - **删除 SSE 断线续传（`Last-Event-ID`）**：流一断，在途请求即丢失，客户端 MUST 以新 request id 重发。→ 重发必然发生，server 必须幂等。
- tasks 扩展五态：`working / input_required / completed / failed / cancelled`，后三者为终态；取消是**协作式**（server 可以不停）；task 必须在响应发出前**持久化创建**。[S3]
- MRTR 规范明确：完整性保护的 `requestState` 只能限定重放窗口，"do not by themselves guarantee single-use"，一次性兑换 MUST 由 server 侧强制。[S5]
- form-mode elicitation 只支持扁平原始类型 schema，布尔确认框够用；但 MUST NOT 用它收密码/凭据。[S8]
- 规范对工具的定位：SHOULD 始终有人在环、能拒绝工具调用；客户端 SHOULD 对敏感操作弹确认。业务错误用 `isError: true`（Tool Execution Error），便于模型自行纠正；返回 `structuredContent` 时 SHOULD 同时给序列化 JSON 文本。[S7]

### 2.2 Claude Code 实际支持情况 [S9]

| 项 | 现状 |
|---|---|
| 传输 | stdio / http (Streamable) / sse（已弃用）/ ws；`.mcp.json` 支持 `headers` 与 `${VAR}` 环境变量展开 |
| 协议版本 | v2.1.232+ 使用 v2 runtime（TS SDK 2.0），会与 **HTTP** server 协商 2026-07-28；stdio 需设 `MCP_PROTOCOL_NEGOTIATION=auto` 才会协商 |
| 墙钟超时 | `MCP_TOOL_TIMEOUT` 未设置时约 28 h；per-server `timeout` 是硬墙钟，**progress 通知不能延长它** |
| 空闲超时 | HTTP/SSE/WS **5 min**，stdio **30 min**；既无响应也无 progress 即中止 |
| 自动转后台 | 调用超过 2 min 自动转成后台 task（v2.1.212+），出现在 `/tasks` 中，**会话退出即丢失** |
| 输出上限 | `MAX_MCP_OUTPUT_TOKENS` 默认 25 000；**图片内容始终计入** |
| elicitation | 支持（对话框；对话框打开期间调用不会转后台）；社区资料称 v2.1.76 引入 [S13] |
| MCP tasks 扩展 | 官方 client matrix 未列出任何客户端支持 tasks [S4]；Claude Code 的 SEP-1686 需求 #18617 **closed as not planned** [S10] |

已知未修 bug（均为 open）：
- **#93143**：Streamable HTTP 工具调用在约 **352–365 s** 被截断；per-server timeout 设 24 h、`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT=0` 都无效（v2.1.266）。[S11]
- **#85442**：远程 Streamable HTTP 的 **form elicitation 不弹出**，客户端 20 s 超时（v2.1.226）；stdio 是否正常未测。[S12]

### 2.3 传输与挂载

- Streamable HTTP 规范安全要求：MUST 校验 `Origin`（非法即 403）；本地运行 SHOULD 只绑 127.0.0.1；SHOULD 鉴权。目的是防 DNS rebinding。[S6]
- MCP Python SDK < 1.23.0 默认不开 DNS rebinding 防护（CVE-2025-66416）。现在 `FastMCP()` 在 host 为 127.0.0.1/localhost 时默认开启；直接用低层 `StreamableHTTPSessionManager` 的须手动配 `TransportSecuritySettings(allowed_hosts, allowed_origins)`。[S17]
- 挂进 FastAPI：`mcp.streamable_http_app()`（官方 SDK）或 FastMCP 的 `http_app()` 都能 `app.mount("/mcp", …)`，但**被挂载子应用的 lifespan 不会运行**。宿主 lifespan 必须 `async with mcp.session_manager.run()`（或把 `mcp_app.lifespan` 传给宿主），否则首个请求就报 "Task group is not initialized"。[S14][S15]
- FastMCP 的 `task=True` 后台任务实现了 tasks 扩展，但默认 `memory://` 后端下"If the server restarts, all pending tasks are lost"，要持久化得接 Redis。[S16] → 不能拿它当作业库。
- 仓库先例：`.mcp.json` 已用 `type: http, url: http://127.0.0.1:8765/mcp` 接入常驻的 `cascadeur` 进程；本次会话该服务未启动，Claude Code 只报 ConnectionRefused。HTTP 形态下 service 生命周期完全独立于 Claude 会话，正是本需求要的。

### 2.4 幂等（业界成熟做法）

Stripe：按 key 保存**首次**请求的状态码与响应体（**失败也保存**），同 key 重试返回同一结果；同 key 不同参数直接报错；key 保存至少 24 h 后可清理；参数校验失败或与并发执行冲突时**不保存结果**、允许重试。[S18]

### 2.5 Windows 桌面通知

- Session 0 中的服务无法显示任何 UI，推荐做法是把 UI 放进交互会话里的独立进程、通过 IPC 通信。[S19][S20] headful 浏览器同样需要交互会话，所以 service 必须以登录用户身份跑在桌面会话里，**不能做成 Windows Service**。
- `windows-toasts`：基于 WinRT SDK 绑定，支持 Win10/11，1.3.1 版发布于 2025-05。点击回调 `on_activated` 需要注册自定义 AUMID（自带 `register_hkey_aumid.py`），否则 toast 进入 Action Center 后只会触发 `on_dismissed`。[S21][S22] 备选库 `win11toast`。

## 3. Implications for the spec

1. **传输：MCP 挂在同一个 FastAPI/uvicorn 进程上**（`/mcp`，Streamable HTTP），与 `/api/*` 共用 DI container。MCP tool 与 route 同级，是 transport 边缘的薄包装，**每个 tool 映射恰好一个 Query/Command 方法**。只绑 127.0.0.1，开启 Host/Origin 白名单，外加静态 bearer token：`.mcp.json` 写 `"headers": {"Authorization": "Bearer ${JIMENG_BRIDGE_TOKEN}"}`，token 放 gitignored `.env`。*（观点：stdio 代理多一跳、多一份 schema，仅在 HTTP 客户端 bug 无解时作为后备。）*
2. **所有 MCP tool 必须在数秒到约 1.5 min 内返回，禁止长阻塞调用。** 不依赖 MCP tasks 扩展（Claude Code 不支持），不靠 progress 续命（#93143 约 6 min 截断），也避开 2 min 自动转后台（后台 task 会话退出即丢）。作业句柄就是应用层的 `job_id` / `batch_id`，作为普通参数传递，正合 SEP-2567 的建议。
3. **`wait_job(job_ids, timeout_s)` 做有界等待**：`timeout_s` 上限 ≤ 90 s，期间每 ≤ 30 s 发一次 `notifications/progress`；到期返回当前快照（状态、阶段、已等待时长、建议下一步），由 Claude 循环调用。项目级 `.mcp.json` 为该 server 设 `"timeout": 120000` 兜底。*（观点）*
4. **确认闸门不走 elicitation**：HTTP 下有 #85442（不弹框、20 s 超时），`claude -p` 也无人应答。改为两步：
   - `precheck_batch(items)` 返回 `batch_id`、预估积分、逐项校验结果、表单截图路径和 `confirmation_token`。token 用 HMAC 绑定 batch 内容摘要、预估积分和过期时间。
   - `confirm_batch(batch_id, confirmation_token)` 通过后才入队。token **单次使用、由 server 侧强制**（同 MRTR 规范的警告）；batch 内容一变，token 即失效。

   「不能静默花钱」靠两层保证：(a) `confirm_batch` **不进 Claude Code 的 permissions allow 列表**，每次调用都要人工授权；(b) `auto_confirm` 只在 HTTP API 暴露、默认关闭，MCP 上不暴露。*（观点）*
5. **幂等分两层**：
   - (a) 客户端可带 `idempotency_key`，按 Stripe 语义保存首次结果；同 key 不同参数返回 409 / `isError`。
   - (b) server 自算 `fingerprint = sha256(规范化 prompt + 每个 ref 文件的 sha256 + params + 目标输出路径)`。若已有同指纹的非终态或 `done` 作业，直接返回已有 `job_id`。有意重抽须显式传 `reroll: true`，并记录 attempt 序号。

   2026-07-28 已取消续传，重发必然发生，这两层是硬需求。
6. **状态机（SQLite + WAL，service 是唯一写者）**：

| 状态 | 进入时持久化的内容 | 服务重启后怎么处理 |
|---|---|---|
| `draft` → `prechecked` | 校验结果、预估积分、表单截图路径 | 保留 |
| `awaiting_confirm` | token 摘要、过期时间 | 已过期则退回 `prechecked` |
| `queued` | 确认来源（human / auto_confirm）、确认时间 | 重新排队 |
| `submitting` | **点击「生成」之前**写入 | **绝不自动重提** → `paused_needs_human`（reason=`restart_during_submit`，需人工去即梦历史核对） |
| `generating` / `downloading` | 平台侧任务标识、开始时间 | 恢复轮询 / 重新下载 |
| `paused_needs_human` | `reason`（`captcha` / `moderation_reject` / `login_expired` / `restart_during_submit` / `dom_changed`）+ 截图 | 保留，等待 `resume_job` |
| `done` / `failed` / `cancelled` | 输出路径 + sidecar json / 错误信息 + 截图 | 终态 |

   `cancel` 是协作式的：进入 `submitting` 之后再取消**不会退还积分**，只是停止等待和下载，响应里必须说清楚。对外状态另映射到 tasks 扩展的五态，将来客户端支持时可以直接对接。*（观点）*
7. **返回内容**：同时给 `structuredContent` 和同内容的 JSON 文本。截图默认只返回文件路径 + 降采样缩略图（长边 ≤ 768 px 的 JPEG），全图通过单独的 `get_screenshot` 获取，避开 25k token 上限。业务错误一律用 `isError: true`，并附可操作的建议。
8. **tool 数量控制在约 12 个以内**：
   - `precheck_batch`（覆盖 prompt / shot_path / asset 三种输入）
   - `confirm_batch`
   - 作业类 4 个：`wait_job`、`list_jobs`、`cancel_job`、`resume_job`
   - `browser_step(op = upload | fill | preview | submit | download)`，其中 submit 同样受确认闸门约束
   - `entity`（create / select）
   - `get_screenshot`

   合计约 10 个。*（观点：分步操作合并为一个 op 枚举。）*
9. **分层落点**：`development.md` §1 没有定义 MCP 的角色。建议新增 `apps/api/mcp_tools/{aggregate}__tool.py`，规则与 routes 相同，并在 spec 里写 divergence note。*（观点）*
10. **暂停通知**：service 以登录用户身份在交互桌面会话中运行；用 `windows-toasts` + 注册好的 AUMID，点击 toast 打开 service 本地页面或把浏览器窗口置前。toast 只是尽力而为，**唯一真相源是作业状态**：Claude 通过 `wait_job` 看到 `paused_needs_human` + reason + 截图。

## 4. Open questions surfaced

1. MCP 路径上的「人工确认」由谁执行？选项：Claude Code 权限询问（上文方案）、service 自带的网页确认页、或等 Claude Code 修好 HTTP elicitation 再用。autonomous 模式下是否允许 Claude 自行确认？
2. 用户本机 Claude Code 的版本和 runtime（v1/v2）需要实测三件事：长调用的实际截断点、HTTP elicitation 能否弹出、per-server `timeout` 是否生效。
3. 预估积分从哪里来：即梦表单提交前是否显示消耗（归 DOM/平台 angle）？预估与实扣不一致时怎么处理？
4. 重抽与去重的边界：同一 shot 反复重生成是常态，是否默认允许？每个 shot 设多少次上限？
5. `restart_during_submit` 的人工核对能否半自动化，比如读即梦历史列表、按 prompt 首行路由键匹配？
6. 单个 batch 的确认上限（最大积分 / 最大条数）是多少？超出是否强制拆批？
7. MCP tool 放在 `apps/api/` 内，还是单独的 `apps/mcp/`（同进程挂载）？需要在 stage 4 定下并写 divergence note。

## Sources

- [S1] https://modelcontextprotocol.io/specification/2025-11-25/changelog
- [S2] https://modelcontextprotocol.io/specification/2026-07-28/changelog
- [S3] https://modelcontextprotocol.io/extensions/tasks/overview
- [S4] https://modelcontextprotocol.io/extensions/client-matrix
- [S5] https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr
- [S6] https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- [S7] https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- [S8] https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation
- [S9] https://code.claude.com/docs/en/mcp
- [S10] https://github.com/anthropics/claude-code/issues/18617
- [S11] https://github.com/anthropics/claude-code/issues/93143
- [S12] https://github.com/anthropics/claude-code/issues/85442
- [S13] https://aibuilderhub.dev/en/blog/claude-code-mcp-elicitation （二手来源）
- [S14] https://py.sdk.modelcontextprotocol.io/run/asgi/
- [S15] https://gofastmcp.com/deployment/http
- [S16] https://gofastmcp.com/servers/tasks
- [S17] https://github.com/advisories/GHSA-9h52-p55h-vw2f
- [S18] https://docs.stripe.com/api/idempotent_requests
- [S19] https://learn.microsoft.com/en-us/previous-versions/bb756986(v=msdn.10)
- [S20] https://www.firedaemon.com/post/microsoft-windows-interactive-services-and-session-0-isolation
- [S21] https://github.com/DatGuy1/Windows-Toasts
- [S22] https://windows-toasts.readthedocs.io/en/latest/custom_aumid.html
