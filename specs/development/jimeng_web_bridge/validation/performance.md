---
worker_id: level-specialist-07-performance
stage: 5
role: level-specialist
level: performance
status: complete
blockers: []
confidence: medium
---

# Validation — performance（jimeng_web_bridge）

## 0. 范围、口径与判级

- **对应 spec 条目**：§6 NFR「性能」「可靠性」，FR-18、FR-34、FR-35、FR-52、FR-54。
- **规模假设（按实际用量，不做超出实际的压测）**：单账号单用户，每天 ≤ 50 条 job；单 batch ≤ 30 条，同时 generating ≤ 3 条；同时在线 = 1 个 UI 标签页 + 1 个 Claude 会话 + 偶发脚本。不做多用户压测，不对真实站点施压。
- **判级**：hard 预算未达 → `blocker`；observe-only 超出预期区间 → `warning`，只记录不中断（general.md 标准表）。
- **防抖动**（general.md 原则 2，Windows 开发机噪声大）：hard 项跑 3 轮，**≥ 2 轮超预算**才判 blocker；只 1 轮超记 warning 并附三轮原始数据。百分位用 nearest-rank，每轮丢弃前 20 个预热请求。
- **在哪里跑**：
  - `make test-perf`：Windows 开发机自动跑，全部用 fake 站点 + fake `dreamina`，不花积分；整套 ≤ 40 min，**不并入 `make test`**；
  - `make test-soak`：8 h 长稳，人工触发；
  - manual：真实站点只读 canary 与用户批准的首个真实 job 期间人工记录（PERF-21）。
- **启动方式与 `make run` 一致**：单 uvicorn worker、无 `--reload`、生产构建 UI（`serve_static=True`）；只把 `global.toml` 换成测试副本，按项覆盖 `pacing.min_submit_interval_s`、`canary.interval_min` 等键（仍是「从 config 读」，符合 FR-5）。前置断言事件循环为 `ProactorEventLoop`（Windows 上 Playwright 与 asyncio 子进程都依赖它）。
- **报告与事件**：每次写 `projects/jimeng_web_bridge/.data/perf/{ts}.json`（gitignored），头部记录 CPU、内存、磁盘类型、电源模式、Python / Chrome / Playwright / Node 版本、git commit。stage-6 validator 写 `events.jsonl`：`validation.started`（`levels: ["performance"]` + `pre_reading_consulted`）→ 逐项 `validation.issue.raised`（`level: performance`，severity 按上面判级）或 `validation.pass`；PERF-21 发 `validation.requires_manual_walkthrough`。

### 通用测量工具

| 用途 | 工具 |
|---|---|
| HTTP 延迟 | `httpx.AsyncClient` 直连真实 uvicorn（127.0.0.1），带 Host / Origin / Bearer，经过与生产相同的中间件链 |
| MCP 调用 | 官方 `mcp` Python SDK 的 Streamable HTTP client。请求带 `Authorization` 和 `_meta.progressToken`，记录每条 notification 与最终结果的接收时刻 |
| 事件循环 | 测试模式打开 asyncio debug，`slow_callback_duration = 0.25 s`，采集 "Executing … took" 日志。另挂一个 loop-lag 探针 task：每 100 ms sleep 一次，记录实际超出量，写入 JSONL 日志 |
| 进程资源 | `psutil`：RSS、CPU%、Windows `num_handles()`、线程数。service Python 进程、Playwright driver（node）、Chrome 进程树分开采 |
| SQLite | `EXPLAIN QUERY PLAN`；用 `sqlite3` trace callback 统计每个请求执行的语句数 |
| UI | Playwright 自带的 Chromium（与 service 的 Chrome profile 无关）：Navigation Timing、`PerformanceObserver`（LCP、longtask）、`page.on("request")` 计数 |
| 夹具 | ffmpeg 生成合法 mp4；噪声像素 PNG；随机种子统一为 `20260913` |

---

## A. MCP / HTTP 调用上界

### PERF-01 端点分级与单次调用墙钟上界

- **指标**：客户端发出请求 → 收到最后一个字节，经过的墙钟时间。
- **分级与预算**：

| 类 | 端点 / 工具 | hard | observe-only 目标 |
|---|---|---|---|
| Q 只读 | `GET /api/health`、`/api/session`、`/api/jobs*`、`/api/batches/{id}`、`/api/artifacts/*`、`/api/dramas*`、`/api/config/global`、`/api/entities/reconcile`、`/api/history`；MCP `session_status`、`list_jobs`、`get_screenshot`、`entities(reconcile)` | p95 ≤ 500 ms（PERF-07） | — |
| L 本地计算 / IO | `POST /api/batches`、`confirm`、`cancel`、`pause`、config `propose` / `save`、`candidates/promote`；MCP `precheck_batch`、`confirm_batch`、`cancel_job` | ≤ 90 s | confirm / cancel / pause ≤ 500 ms；config save ≤ 1 s；propose（hy3 真实目录树）≤ 10 s；promote ≤ 2 s |
| A 受 BrowserActor / CLI 串行约束 | `POST /api/session/canary`、`/api/jobs/{id}/steps/{op}`、`/api/entities/sync`、`POST /api/entities`、`/api/jobs/{id}/resume`、`/api/queues/{b}/resume`；MCP `browser_step`、`resume`、`entities(sync)` | ≤ 90 s，**含排队等 actor 的时间** | — |
| W 有界等待 | `POST /api/jobs/wait`、MCP `wait_jobs` | ≤ min(timeout_s, 90) + 2 s | 见 PERF-03 |

- **约束**：`session_status` 和 `GET /api/session` 不得在请求内同步执行 `dreamina user_credit` 或 canary，只返回最近一次快照及其时间戳。否则 Q 类预算不可能成立。
- **方法**：
  - 每个 HTTP 端点和每个 MCP 工具，在 §B–§C 的最坏夹具下各调用 10 次，取最大值；
  - A 类的最坏情况见 PERF-02。
- **位置**：`make test-perf`。

### PERF-02 A 类调用的 deadline 行为（actor 忙时）

- **背景**：BrowserActor 全局串行。调度器可能正占着 actor 做一次最长 3 min 的 preparing，这时进来的 `browser_step`、canary、resume 只能排队。如果等排到、做完才返回，90 s 上界不可能成立。
- **预算（hard）**：service 内部 deadline ≤ 85 s。到点后：
  - 返回「进行中」快照：`status: in_progress`、所属 job 或操作标识、已等待时长、建议下一步（用 `wait_jobs` 或 `GET /api/jobs/{id}` 观察）；
  - **不取消已经在执行的 Playwright 调用**（reliability angle G：取消在途调用属于未定义行为）；
  - 操作在后台照常完成，结果可以查询到。
- **方法一（actor 被占用）**：fake 站点注入「上传完成信号延迟 120 s」，让调度器进入某个 job 的 upload，再并发调用 `POST /api/session/canary`、另一个 job 的 `browser_step(op=preview)`、`resume`。断言：三个调用都在 ≤ 90 s 内返回快照；120 s 后原 upload 正常完成；排队的 canary 随后执行并写入 session。重复 5 次。
- **方法二（单个慢操作）**：fill 策略设为 `type` 写 5000 字，fake 站点每字符加 20 ms（总计约 100 s）；断言 `browser_step(op=fill)` 仍在 ≤ 90 s 内返回进行中快照。
- **位置**：`make test-perf`。
- *（judgment call：spec 只对 `wait_jobs` 写了「到时返回快照」，A 类调用同样需要，见 §M 建议 1。）*

### PERF-03 `wait_jobs` 的进度通知节奏与提前返回

- **指标**：以下三类间隔中的最大值：
  - 请求发出 → 第一条 `notifications/progress`；
  - 相邻两条通知之间；
  - 最后一条通知 → 最终结果。
- **预算**：
  - hard：≤ 30 s（FR-52）；
  - observe-only：≤ 20 s（给 Windows 调度抖动留余量）。
- **场景**：`timeout_s = 90`，watch 3 个始终不结束的 job（fake render 1 h），重复 5 次。附加：请求不带 `progressToken` 时不发通知（协议合规，失败记 warning）。
- **提前返回（observe-only）**：被 watch 的任一 job 进入终态或 `paused_needs_human` 后，≤ 2 s 内返回。重复 5 次。
- **多个等待者同时等（observe-only）**：
  - 5 个 `wait_jobs` 同时等待时，每个仍满足 hard 预算；
  - 等待期间 SQLite 读语句 ≤ 10 条/s。等待不能靠每个等待者各自高频轮询 DB。
- **位置**：`make test-perf`。

### PERF-04 MCP 返回体积

- **指标**：每个工具结果的估算 token 数，口径偏保守：`structuredContent` 与 JSON 文本**都计入**；文本按 UTF-8 字节数 ÷ 2；每个图片块按 宽 × 高 ÷ 750。
- **预算（hard）**：单次结果 ≤ 20 000 token（Claude Code `MAX_MCP_OUTPUT_TOKENS` 默认 25 000，图片始终计入）；图片块长边 ≤ 768 px，单次最多 4 个；不出现 base64 全尺寸截图。
- **最坏夹具**：
  - `precheck_batch`：30 条，每条 10 个参考项。路径用真实深度的中文路径（`ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shotNN/…`）。其中 5 条 error、5 条 warning。
  - `list_jobs`：DB 中有 1000 条 job，不带过滤。
  - `wait_jobs`：同时 watch 30 条。
  - `get_screenshot`：1920 × 5000 的全页截图。
- **注意**：
  - `list_jobs` 如果不分页，1000 条必然超预算，因此要求默认分页（§M 建议 2）；
  - FR-52 要求 `structuredContent` 与 JSON 文本同时返回，体积因此翻倍。
- **位置**：
  - `make test-perf`；
  - 另在 PERF-21 中用真实 Claude Code 跑一次 30 条的 precheck，确认没有输出截断提示（spec open question 9）。

---

## B. 事件循环响应性

### PERF-05 做重活期间 API 仍然可用

- **背景**：单进程单事件循环，BrowserActor、调度器、API、MCP 共用。sha256 哈希、ffprobe、文件复制、TOML 解析、CLI 子进程、缩略图生成，只要有一项在 loop 线程里同步执行，所有接口会一起卡住。
- **探针**（测量期间持续运行）：`GET /api/health` 每 100 ms 一次；`GET /api/jobs` 默认页（或 `limit=50`，见 §M 建议 2，DB 为 `DS-1000`）每 500 ms 一次；loop-lag 探针全程开启。
- **负载场景**（逐个跑，每个持续 ≥ 60 s 或跑完为止）：
  1. BrowserActor fill 5000 字的 prompt，`insert_text` 与 `type` 两种策略各跑一次；
  2. 上传 10 个参考项：1 个 50 MB 视频 + 9 个 30 MB PNG（包括 FR-30 要求的「复制到临时目录并改名」）；
  3. 下载 60 MB 视频 → 分块计算 sha256 → ffprobe → 原子 rename → 写 sidecar；
  4. 30 条 precheck 的哈希最坏夹具（PERF-06）；
  5. 3 个 fake `dreamina text2image` 子进程并行，各自 sleep 20 s 后输出 JSON；
  6. `DramaConfigCommand.propose` 扫描 hy3 真实目录；
  7. 场景 1、3、5 同时进行。
- **预算（hard）**：负载期间
  - `/api/health` p95 ≤ 100 ms、p99 ≤ 300 ms；
  - `/api/jobs` 默认页 p95 ≤ 200 ms；
  - loop-lag 最大值 ≤ 500 ms；
  - asyncio debug 日志里没有任何单次回调 > 500 ms。
- **observe-only**：
  - loop-lag p99 ≤ 100 ms；
  - 单次回调 > 250 ms 的次数，逐条列出调用栈；
  - 空闲基线：`/api/health` p95 ≤ 20 ms。
- **位置**：`make test-perf`，3 轮。

---

## C. precheck 与查询延迟

### PERF-06 precheck 耗时（L 类中最重的调用）

- **夹具**：
  - 30 条 shot，由 `tests/fixtures/real_shots/` 中的 hy3 shot 派生；
  - 共引用 60 个互不相同的 30 MB PNG（噪声像素，达到平台单图上限）+ 30 个 20 MB 的 previz mp4，合计约 2.4 GB；
  - 按固定种子生成一次，缓存在 `.data/tmp/perf_fixtures/`，缺失时才重建。
- **耗时预算**：
  - hard：≤ 90 s（PERF-01）；
  - observe-only：
    - 热缓存 ≤ 15 s；
    - 同一 batch 立即重复 precheck ≤ 5 s（若实现按 `(path, size, mtime_ns)` 缓存哈希）；
    - 冷缓存（重启后首次运行，PERF-21 手工测一次）≤ 45 s。
- **内存（hard）**：哈希过程中 Python RSS 增量 ≤ 64 MB。必须分块读取，不能把整个文件读进内存。
- **位置**：热缓存进 `make test-perf`；冷缓存手工。

### C.0 标准数据集

**`DS-1000`**（seeder 确定性生成，种子 `20260913`）：
- 1000 条 job，分布在 60 天、5 部剧（剧根取 hy1–hy4、wushen_juexing）；100 个 batch（大小 1–30，另有 1 个 60 条）；10 000 条状态转移（每 job 约 10 条）；
- 状态分布：done 80 %、failed 8 %、cancelled 4 %、paused 3 %、generating 3 条，其余 queued；另有 artifacts 行、200 条 24 h 内 idempotency key、50 条主体快照。

**`DS-20K`**（observe-only）：20 000 条 job、200 000 条转移，相当于每天 50 条、用满一年。

### PERF-07 查询端点 p95

- **被测形态**：
  - `GET /api/jobs`：默认页；按 `state` 过滤（活动态集合）；按剧过滤；按 batch 过滤；
  - `GET /api/jobs/{id}`：含转移记录与 artifacts；
  - `GET /api/batches/{id}`：取 60 条的那个 batch；
  - `GET /api/history`：按剧 + 最近 30 天，含每日积分合计；按镜；按资产主体；
  - `GET /api/entities/reconcile`：fixture 目录树，10 部剧的 config；
  - `GET /api/session`、`GET /api/config/global`；
  - `GET /api/artifacts/{job_id}/{name}`：2 MB 截图，完整传输；
  - `GET /api/dramas`、`GET /api/dramas/{drama}/config`：**只读访问真实 `ai_videos/` 目录树**。
- **方法**：
  - 每种形态先 20 次预热，再测量 200 次，顺序执行；
  - 另跑一个 4 并发客户端的变体，模拟 UI、Claude、脚本、调度器写 progress 同时进行。
- **预算**：
  - hard：`DS-1000` 下每种形态 p95 ≤ 500 ms，顺序和 4 并发两种都要满足；
  - observe-only：顺序执行 p95 ≤ 100 ms；`DS-20K` 下 p95 ≤ 1 s。
- **响应体积（observe-only）**：`/api/jobs` 默认页 ≤ 500 KB；列表投影不内嵌转移记录。
- **位置**：`make test-perf`，3 轮。

### PERF-08 索引与语句数（提前报警）

- **`EXPLAIN QUERY PLAN` 断言**：下列查询不得对 jobs / transitions 做全表 `SCAN`：
  - jobs 按 `state`、`batch_id`、剧根 + 时间、指纹过滤。指纹查询用于 FR-24 去重，precheck 每条都会查；
  - history 按日期范围过滤；
  - transitions 按 `job_id` 查询；
  - idempotency 按 key 与过期时间查询。
- **语句数**：每个查询请求执行的 SQL 语句 ≤ 10 条（防 N+1）。
- **分类**：observe-only。真正的契约是延迟，本项只用于提前报警（general.md 原则 1）。
- **位置**：`make test-perf`。

---

## D. UI

### PERF-09 首屏

- **环境**：`make ui-build` 后由 backend 提供静态文件；Playwright 自带 Chromium，viewport 1440 × 900，不节流；冷启动（新 context、禁用缓存）与热启动各 10 次；DB 为 `DS-1000`。
- **指标**：从 `page.goto` 开始，到页面 ready 标志可见为止。ready 的含义是数据已加载、首屏元素已渲染、首屏内可见的缩略图已 decode。同时记录 LCP 和 `loadEventEnd`。
- **预算**：
  - hard：冷启动 p95 ≤ 2 s。适用于三个页面：
    - 落地页；
    - 队列看板；
    - 批次确认页深链 `/batches/{id}`（30 条，每条最多 10 张参考缩略图）。这是 Claude 交给用户的链接。
  - observe-only：
    - 其余 4 个页面冷启动 p95 ≤ 2 s；
    - 主 JS bundle gzip 后 ≤ 500 KB；
    - 批次确认页首屏传输量 ≤ 5 MB。
- **前提**：参考图缩略图必须由服务端先缩到长边 ≤ 320 px 再返回，不能把 30 MB 原图直接发给浏览器（§M 建议 5）。
- **附加断言**：数据接口人为延迟 3 s 时，页面在 ≤ 2 s 内显示 loading 骨架，而不是空白页（FR-55）。失败记 warning；功能层面的检查归 system_tests。
- **位置**：`make test-perf`。

### PERF-10 队列看板在 200 条 job 下的更新成本

- **场景**：
  - 看板上有 200 条非终态 job（压力值，高于真实用量）；
  - fake 让其中 3 条每 2 s 更新一次进度；
  - 观察 60 s。
- **预算**：
  - hard：ready 之后没有任何 ≥ 500 ms 的 long task；
  - observe-only：
    - > 50 ms 的 long task 每分钟累计 ≤ 1 s；
    - 看板 DOM 节点数 ≤ 20 000。
- **位置**：`make test-perf`。

### PERF-11 轮询节奏

- **指标**：页面发往 `/api/*` 的请求数，用 `page.on("request")` 统计。
- **预算（hard）**：
  - 看板可见时，120 s 内所有 `/api/*` 请求平均 ≤ 1 次/s；
  - 同一 URL 不得在上一个请求完成前发出下一个请求（无重叠）；
  - 依次访问 7 个页面再回到看板后，请求速率与只开看板时相同。离开页面必须停掉该页面的轮询，不能层层叠加。
- **预算（observe-only）**：标签页隐藏（`document.hidden`）时，≤ 1 次 / 30 s。
- **若 UI 改用 SSE / WebSocket**：改为断言每个标签页 ≤ 1 条长连接，重连间隔 ≥ 2 s。
- **位置**：`make test-perf`。

---

## E. 调度器

### PERF-12 提交间隔精度

- **场景**：测试 config `pacing.min_submit_interval_s = 5`、`concurrency.max_remote_rendering = 3`；一次确认 10 条 job，fake render 8 s。
- **预算（hard）**：
  - service 侧相邻两次 `→ submitting` 转移的时间差 ≥ 5.000 s。两端用同一时钟，只允许 −10 ms 的取整误差；
  - fake 站点服务端收到相邻两次「生成」请求的时间差 ≥ 4.5 s（给「点击 → 发出请求」的抖动留余量）。
- **预算（observe-only）**：
  - 并发槽位和间隔条件都满足后，下一次提交在 ≤ 2 s 内开始（调度器不应拖延）；
  - 10 条全部 done 的总时长 ≤ 理论值 × 1.3。
- **默认值复测**：默认的 15 s 间隔在 PERF-15 的 soak 末段再测一次（6 条）。
- **不在本层**：并发上限本身（generating ≤ 3、「并行已达上限」时回退）属于功能验收 AC-5，不在这里重复。
- **位置**：`make test-perf`，3 轮。

### PERF-13 空闲时无忙等

- **场景**：service 已启动，浏览器停在 fake 页面，没有 job；`canary.interval_min = 30`（10 min 窗口内不触发）；持续 600 s，每 5 s 采样。
- **预算**：
  - hard：service Python 进程 CPU 平均 ≤ 2 %（按单核计）；
  - observe-only：Chrome 进程树平均 ≤ 5 %；空闲时 SQLite 语句 ≤ 60 条/min。
- **变体（observe-only）**：3 条 job 处于 generating，fake 状态响应每 3 s 一次时，Python CPU 平均 ≤ 5 %，每个 job 的 progress 写库合并后 ≤ 1 次/s。
- **位置**：`make test-perf`。

---

## F. 下载与大文件内存

### PERF-14 下载峰值 RSS

- **结论：视频下载不接受把整个 body 读进内存的方式**（例如 `context.request`）。依据：reliability angle E 指出其 body 整体进内存、默认超时 30 s；Playwright 协议传二进制还要再编码一次，60 MB 文件在 driver 与 Python 两侧会出现数倍于文件大小的瞬时峰值（倍数以 stage-6 实测为准）。
- **要求**：下载路径的内存占用与文件大小无关。由 stage-6 探针二选一：浏览器原生下载（页面下载控件，保存到 `.data/tmp/`），或其他流式写临时文件的做法。两者都要求 sha256 分块计算、ffprobe 直接读磁盘文件。
- **夹具**：fake 站点提供 60 MB 和 200 MB 两个合法 mp4，限速 5 MB/s。200 MB 约需 40 s，能暴露 30 s 默认超时。
- **指标**：覆盖「下载 → 校验 → rename → sidecar」全过程，每 100 ms 采样一次 RSS。增量 = 峰值 − 开始前 10 s 的中位数。
- **预算（hard）**：
  - Python 进程 RSS 峰值增量 ≤ 64 MB，60 MB 和 200 MB 都要满足；
  - 200 MB 下载不因超时而失败；
  - 无论成功或失败，结束后 `.data/tmp/` 中没有残留文件。
- **预算（observe-only）**：
  - Playwright driver（node）RSS 增量 ≤ 128 MB；
  - 200 MB 文件的校验阶段（sha256 + ffprobe）≤ 10 s；
  - 下载耗时 ≤ 文件大小 ÷ 限速 × 1.2 + 10 s。
- **上传侧（hard）**：用同一方法测量 FR-30 复制 10 个 30 MB 参考图的过程，Python RSS 增量 ≤ 64 MB。
- **位置**：`make test-perf`，3 轮。

---

## G. SQLite 并发

### PERF-15 10 min 混合 soak（fake 站点）

- **场景**：
  - 写：调度器跑 20 条 job（fake render 20–40 s 随机，提交间隔 5 s，并发 3；注入 2 次审核拒绝、1 次「并行已达上限」）；fake 状态响应每 2 s 一次，持续写 progress。
  - 读：2 个 UI 轮询客户端（周期 2 s）+ 1 个 MCP 客户端（循环 `wait_jobs`，每 5 s 一次 `list_jobs`）+ 1 个脚本（每 10 s 一次 `GET /api/history`）。
  - 末段再跑 6 条 job，提交间隔用默认的 15 s（供 PERF-12 复测）。
- **预算（hard）**：
  - 日志和响应中 `database is locked` / `SQLITE_BUSY` 出现 0 次；
  - 5xx 响应 0 次；
  - 期间所有读请求 p95 ≤ 500 ms；
  - `PRAGMA journal_mode` 为 `wal`。
- **预算（observe-only）**：
  - 结束时 `-wal` 文件 ≤ 64 MB（说明 checkpoint 在正常工作）；
  - 写连接数始终为 1；
  - progress 平均写入 ≤ 5 次/s。
- **位置**：`make test-perf`。这是整套里最长的一项，约 12 min。

---

## H. 启动与关闭

### PERF-16 启动到 health 可用

- **指标**：进程启动（与 `make run` 相同的命令）→ `GET /api/health` 首次返回 200。
- **预算（hard）**：
  - 5 次冷启动，p95 ≤ 8 s；
  - health 可用**不依赖**浏览器启动、登录检查或 `dreamina version`：让 fake `dreamina version` sleep 30 s、Chrome 启动人为延迟 30 s，仍须满足 ≤ 8 s，且 health 如实报告 `starting`；
  - DB 中有 1000 条 job（含 50 条非终态，其中 3 条处于 `submitting`）时，仍须满足 ≤ 8 s。恢复对账在后台进行。
- **预算（observe-only）**：
  - p95 ≤ 4 s；
  - 浏览器从启动到 `ready`（fake 站点、已登录的 profile）≤ 20 s。
- **位置**：`make test-perf`。

### PERF-17 关闭

- **指标**：以新进程组启动 service，发送 `CTRL_BREAK_EVENT` 请求停止 → 进程退出。
- **预算（hard）**：
  - 退出后没有遗留使用本 profile 的 `chrome.exe` / `node.exe`；
  - 紧接着再次启动，不报 `profile_in_use`。
- **预算（observe-only）**：退出耗时 ≤ 15 s。
- **位置**：`make test-perf`。如果在本机上无法可靠地自动发送信号，降级为手工测试，并用 `skip(reason=…)` 标注原因（development.md §5）。

### PERF-18 canary 耗时（observe-only）

- fake 站点：≤ 15 s。
- 真实站点：在 PERF-21 手工记录实测值，> 60 s 记 warning。原因是 `resume` 要先跑一次 canary，而 `resume` 受 90 s 调用上界约束（PERF-02）。
- **位置**：`make test-perf` + manual。

---

## I. 8 h 长稳（observe-only）

### PERF-19 `make test-soak`

- **场景**：fake 站点跑 8 h，用量对应真实的一天：
  - 50 条视频 job（fake render 2–10 min 随机，种子固定；默认间隔 15 s，并发 3）+ 20 条 CLI 出图（fake `dreamina`）；默认 `canary.interval_min = 30`（约 16 次）；
  - 注入：5 次审核拒绝；2 次队列级暂停（测试脚本经 API 恢复）；1 次杀掉 renderer 进程（触发 `browser_lost` 恢复）。
- **采样**：每 60 s 一次。第 1 小时视为预热，不计入斜率。

| 指标 | 预期区间 |
|---|---|
| Python RSS 斜率（第 1–8 h 线性回归） | ≤ 10 MB/h；终值 ≤ 基线 + 150 MB |
| Python `num_handles()` 斜率 | ≤ 50/h |
| 线程数 | 基线 ± 5 |
| Chrome 进程树 RSS | ≤ 1.5 GB，且不单调增长。若持续增长，建议 spec 增加「空闲时定期 reload 工作页」 |
| loop-lag p99 | 全程 ≤ 100 ms |
| `.data/artifacts/` | 成功 job 只保留 FR-32 的预演截图，每个 job ≤ 1 MB；失败 job 每条 ≤ 30 MB；成功 job 的 trace 文件数为 0 |
| `.data/logs/` | 8 h 内 ≤ 50 MB |
| `.data/tmp/` | 结束时为空 |
| `bridge.db` / `-wal` | ≤ 20 MB / ≤ 64 MB |

- **位置**：人工触发。建议在 stage-6 的自动项全部通过后跑一次。

---

## J. 生产观测指标（observe-only）

### PERF-20 记录每个 job 的耗时，并在历史里展示

由状态转移时间戳派生，写入 DB，并通过 `/api/history`、`/api/jobs/{id}` 和 UI 历史页展示。

| 字段 | 定义 | 预期区间（超出则在历史中标「慢」，并写日志 warning） |
|---|---|---|
| `prep_s`，及子步骤 `set_params_s` / `upload_s` / `fill_s` / `preview_s` | 进入 preparing → 进入 awaiting_submit_slot | `prep_s` ≤ 180 s（spec NFR）；单个上传 ≤ 60 s；fill ≤ 60 s |
| `slot_wait_s` | awaiting_submit_slot → submitting | 仅记录 |
| `submit_s` | submitting → generating | ≤ 30 s |
| `platform_queue_s` | generating → 平台开始渲染。从 `get_history_queue_info` 解析；拿不到时为 null，并注明原因 | 仅记录 |
| `render_s` | 平台开始渲染 → 平台完成 | 仅记录 |
| `download_s` / `verify_s` | downloading 阶段 / 校验阶段 | ≤ 120 s（文件 ≤ 60 MB）/ ≤ 15 s |
| `total_s` | 确认 → done | 仅记录 |
| CLI：`cli_submit_s` / `cli_wait_s` / `download_s` | 同上 | 仅记录 |

- **自动检查**（`make test-perf` 中 fake e2e 跑完之后）：
  1. 上表字段都出现在 history 响应中；
  2. 各阶段之和与 `total_s` 相差 ≤ 1 s。各阶段 = `prep_s` + `slot_wait_s` + `submit_s` + generating 阶段 + `download_s` + `verify_s`；
  3. fake 站点上（每个上传项人为延迟 3 s），hy3 `shot02` 的 `prep_s` ≤ 60 s。
- **分类**：warning。spec 采纳 §M 建议 6 之后，「字段存在」一项升级为验收项。

---

## K. 真实站点手工记录（observe-only，发 `validation.requires_manual_walkthrough`）

### PERF-21 首次真实 canary 与首个用户批准的 job

逐项记录实测值，写回 PageMap 注释和本文件的实测附录：

1. canary 总耗时（PERF-18）。
2. 5000 字 prompt 分别用 `insert_text`、`type`、`execCommand` 填写的耗时。若 `type` > 60 s，canary 不得把它选为默认策略：它会同时威胁 3 min 准备目标和 PERF-02 的单次操作时长。
3. 30 MB 图片从开始上传到出现完成信号的耗时。
4. `prep_s`，与 180 s 目标对照。
5. 下载耗时、文件大小、Python / node 的 RSS 峰值增量，用来复核 PERF-14 的方案选择。
6. 冷缓存下 30 条 precheck 的耗时（PERF-06）。
7. 本机 Claude Code 版本上（PERF-04，spec open question 9）：跑满 90 s 的 `wait_jobs` 不被截断；`timeout: 120000` 生效；30 条 `precheck_batch` 结果没有截断提示。

---

## L. 汇总

| ID | 指标 | 主预算 | 分类 | 位置 |
|---|---|---|---|---|
| PERF-01 | 单次调用墙钟（分 Q / L / A / W 四类） | 全部 ≤ 90 s | hard | test-perf |
| PERF-02 | A 类在 actor 忙时的 deadline | ≤ 90 s 返回进行中快照；不取消在途调用 | hard | test-perf |
| PERF-03 | `wait_jobs` 通知间隔 | ≤ 30 s；提前返回 ≤ 2 s | hard / observe | test-perf |
| PERF-04 | MCP 结果体积 | ≤ 20 000 估算 token；图片长边 ≤ 768 px | hard | test-perf + manual |
| PERF-05 | 负载下的事件循环响应 | health p95 ≤ 100 ms；jobs p95 ≤ 200 ms；loop-lag ≤ 500 ms | hard | test-perf |
| PERF-06 | 30 条 precheck（2.4 GB 参考素材） | ≤ 90 s；RSS 增量 ≤ 64 MB；热缓存 ≤ 15 s | hard / observe | test-perf + manual |
| PERF-07 | 查询 p95（`DS-1000`） | ≤ 500 ms；`DS-20K` ≤ 1 s | hard / observe | test-perf |
| PERF-08 | 查询计划、语句数 | 无全表 SCAN；每请求 ≤ 10 条语句 | observe | test-perf |
| PERF-09 | UI 首屏（冷启动） | p95 ≤ 2 s（落地页 / 看板 / 批次确认页） | hard | test-perf |
| PERF-10 | 看板 200 job 下的 long task | 无 ≥ 500 ms 的 long task | hard | test-perf |
| PERF-11 | UI 轮询速率 | ≤ 1 次/s，无重叠，离开页面不泄漏轮询 | hard | test-perf |
| PERF-12 | 提交间隔 | service 侧 ≥ 配置值；站点侧 ≥ 配置值 − 0.5 s | hard | test-perf |
| PERF-13 | 空闲 CPU | Python 平均 ≤ 2 % | hard | test-perf |
| PERF-14 | 下载 / 上传内存 | Python RSS 增量 ≤ 64 MB（60 MB 与 200 MB 文件） | hard | test-perf |
| PERF-15 | SQLite 10 min soak | locked / BUSY 0 次，5xx 0 次，读 p95 ≤ 500 ms | hard | test-perf |
| PERF-16 | 启动到 health | p95 ≤ 8 s，不依赖浏览器与 CLI | hard | test-perf |
| PERF-17 | 关闭 | 无遗留进程，重启不报 `profile_in_use` | hard | test-perf / manual |
| PERF-18 | canary 耗时 | fake 站点 ≤ 15 s；真实站点 ≤ 60 s | observe | test-perf + manual |
| PERF-19 | 8 h 长稳 | RSS ≤ 10 MB/h，句柄 ≤ 50/h，磁盘占用有界 | observe | test-soak |
| PERF-20 | 每 job 耗时字段 | 字段存在；`prep_s` ≤ 180 s | observe | test-perf + 生产 |
| PERF-21 | 真实站点实测 | 见清单 | observe | manual |

## M. 建议 spec 增加或修改的预算

1. **A 类调用的 deadline 语义**（FR-52 扩展到 §5.10 对应路由）。凡受 BrowserActor 或 CLI 串行约束的工具与路由（canary、`browser_step`、entities sync / create、resume），都应在 ≤ 85 s 时返回进行中快照，并且不取消在途操作。否则 actor 正在做 ≤ 3 min 的 preparing 时，NFR「≤ 90 s」无法成立。
2. **MCP 返回体积与分页**：
   - 单个工具结果 ≤ 20 000 估算 token；
   - `list_jobs`、`GET /api/jobs`、`/api/history` 默认分页（建议默认 50 条，最多 200 条），列表投影不内嵌转移记录；
   - `precheck_batch` 的 MCP 结果只展开 error / warning 条目，ok 条目折叠为计数加确认页 URL；
   - FR-52 要求 structuredContent 与 JSON 文本同时返回，体积因此翻倍，需要算进预算。
3. **查询规模**：「1000 条 job」按每天 50 条算只相当于约 20 天的数据。建议追加 observe-only：20 000 条 job / 200 000 条转移下 p95 ≤ 1 s。
4. **新增 hard NFR**：
   - 负载下事件循环响应（PERF-05）；
   - 下载、哈希、上传的 Python RSS 增量 ≤ 64 MB，且与文件大小无关。这实际上排除了用整 body 读入的 `context.request` 下载视频，FR-35 应加注；
   - 启动到 health ≤ 8 s，且不依赖浏览器与 CLI；
   - 空闲 CPU ≤ 2 %。
5. **参考图缩略图 Query**：FR-54 批次确认页要展示参考图缩略图，但 §5.10 只有 `/api/artifacts`，它只覆盖 job 截图。需要一个受 `ai_videos/` 沙箱约束、返回长边 ≤ 320 px 缩略图的 Query 与路由，否则 30 MB 原图下 2 s 首屏无法实现。
6. **FR-46 历史增加每 job 耗时字段**（PERF-20）。否则 NFR「准备阶段 ≤ 3 min 观测指标」实际上没有地方可以观测。
7. **预演截图的磁盘上界**：FR-32 为每个成功 job 永久保留两张截图，按每天 50 条算一年会增长到数 GB 甚至数十 GB。建议每个 job ≤ 1 MB（JPEG / WebP），或者设定保留期。
8. **`session_status` / `GET /api/session` 只返回快照**，不在请求内同步调用 CLI 或 canary。
9. **§6 入口列表增加 `make test-perf` 与 `make test-soak`**，两者都不并入 `make test`。

## N. 需要确认的 carve-out（general.md 原则 6）

- 不对真实站点做性能或压力测试（只读 canary 除外）。真实 CDN 的下载速度和平台排队时长不受我们控制，只作观测。请确认这是有意为之。
- 不测「1 个 UI 标签页 + 1 个 Claude 会话 + 1 个脚本」以上的并发。
- 冷文件缓存下的哈希耗时、Claude Code 客户端侧的截断行为只做手工观测，不进自动闸门。
