# Suno 浏览器服务

本机 Chrome 后台操作 Suno，向 agent / 程序提供 HTTP API。采用专用登录 profile、SQLite 串行任务队列，支持 MP3 / WAV 官方下载。默认 Advanced 纯音乐。

**入口**：[创作工作台](http://127.0.0.1:8770/ui/) · [Swagger 可调用文档](http://127.0.0.1:8770/docs) · [ReDoc 参考](http://127.0.0.1:8770/redoc) · [OpenAPI JSON](http://127.0.0.1:8770/openapi.json)。当前 v0.3；本服务是所有新音频生成的默认入口，包含环境音、音效、背景音乐、主题曲等；共用流程见 [声音与音乐](../../.agents/skills/ai-videos-pipeline/modules/sound.md)。未支持的配音/克隆等能力明确报告，不自动换引擎。

## 人工工作台

运行 `start.ps1` 后访问 `/ui/`。首次把本机私有 `service-token.txt` 的内容填入「服务访问令牌」；页面有复制到剪贴板的本机命令，不需要 Suno 密码。令牌只留在页面内存，刷新后重新连接；请求正文与尚未获得回执的任务键保存在当前标签页的 sessionStorage，以便刷新后恢复同一提交，不含令牌。

选择 Simple / Advanced / Sounds → 写描述或歌词 → 按需上传参考、填写更多选项 → 预检 → 生成。更多选项的范围与说明来自 API schema。上传先存本机，生成时才发送 Suno；切换模式会清空不兼容选项和参考。生成按钮也自动先预检。API 暂停时禁止新生成，仍可编辑与预检；提交超时会锁定原请求并提供「重试同一请求」。

「任务与音乐」查看最近 100 个任务，每 4 秒刷新；已登记成品可以加载试听、核对 SHA256 后下载。恢复面板接受已确认歌曲链接；不会解除验证码暂停。只有 completed 任务提供「使用这些设置创作新任务」。本工作台覆盖本服务已实现的创作操作，不等于 Suno Studio 完整编辑器；尚未提供的发布、训练、声音注册、时间线剪辑不显示为可用功能。

首次部署先运行 `setup.ps1`（Python + Node.js/npm）；前端源码在 `apps/ui/`，`npm ci` 后 `npm run build` 输出到 `apps/api/static/`。源码与锁文件保留，构建产物和 node_modules 不进 Git。API 挂载 `/ui/`，不会覆盖 `/v1` 或 `/docs`；本机 token 认证继续适用。前端修改后重新构建，API 首次挂载静态目录需重启服务。

**v0.2 代理入口：**同一请求 schema 同时用于 HTTP、JSON CLI 和 10 个 stdio MCP 工具；Kimi 共用 skill 为 `/skill:suno-music`。Advanced 人声须写歌词；Simple 可让 Suno 根据 prompt 写词。新增模式与更多控件通过离线 Chrome 测试，真实账号仍受下述验证码阻塞，不能将“接口已实现”理解为“所有 Suno 页面已实测”。

## Kimi / Codex 快速接入

仓库根执行 `./projects/suno_browser_service/install-agents.ps1`，校验 `.agents/mcp.json` 的 Suno 路径后生成 `.kimi-code/mcp.json` 和 `.codex/config.toml`。其他服务保留在共用定义中；不修改用户配置或凭据。重启 Kimi / Codex 后查看实际 MCP 连接状态；Codex 项目配置需要项目已受信任。两端分别使用 `/skill:suno-music` / `$suno-music`，或自然语言指定同一 skill。

MCP 工具：`suno_capabilities`、`suno_plan`、`suno_upload_reference`、`suno_create`、`suno_get_job`、`suno_list_jobs`、`suno_wait_job`、`suno_resume_job`、`suno_cancel_job`、`suno_download`。工具有类型化参数、结构化结果和读写提示。capabilities 暴露机器可读 JSON schema、实现/实测边界和队列暂停状态；plan 只做本机检查，不建任务、不收费。

| MCP 工具 | 输入 | 返回与副作用 |
|---|---|---|
| `suno_capabilities` | 无 | schema、模式/选项、上传限制、暂停和实测状态；本机只读 |
| `suno_plan` | `request` | `schema_valid/request/references/warnings/automation_paused`；不建任务，不收费 |
| `suno_upload_reference` | 本机 `path`、可选 `rights_confirmed` | 素材 `id/kind/bytes/sha256/...`；将 id 放到 references[].asset_id，只写本机 |
| `suno_create` | `request`、`idempotency_key` | Job；后台可能收费，回执不代表已生成 |
| `suno_get_job` | `job_id` | Job；读取本机状态 |
| `suno_list_jobs` | 无 | 最近 100 个 Job；MCP 的 structuredContent.result 为列表 |
| `suno_wait_job` | `job_id`、`seconds`（0–45，默认 45） | `{job,timed_out}`；暂停时可附 automation_paused/next_action |
| `suno_resume_job` | `job_id`、`song_urls`（0–2 条）、`recollect` | Job；已确认歌曲只下载，确定未提交任务可能首次生成；recollect 只到库里重新认领 |
| `suno_cancel_job` | `job_id` | Job（cancelled）；只取消从未点 Create 的排队 / 暂停任务，不访问 Suno（CLI `cancel --job`，HTTP `POST /v1/jobs/{id}/cancel`） |
| `suno_download` | `job_id`、本机 `output_directory` | `{job_id,status,files,next_action}`，files 含 path；仅取回本机成品并校验 SHA |

MCP 参数有内联描述，`request` 的字段说明与 OpenAPI 共用。读取成功结果用 `structuredContent`；`isError=true` 时读取 content 中错误文本，不把错误当生成失败后换键。CLI 包装为 `{ok,result}` 或 `{ok:false,error}`；HTTP 按状态码处理，三者的 Job 内容一致。

一条不带参考的 MCP 调用链（只在需要实际生成时执行 create）：

```text
suno_capabilities({})
suno_plan({"request":{"prompt":"Warm piano, gentle strings, no vocals","instrumental":true}})
suno_create({"request":{"prompt":"Warm piano, gentle strings, no vocals","instrumental":true},"idempotency_key":"episode-theme-001"})
suno_wait_job({"job_id":"<上一步返回的 id>","seconds":45})
suno_download({"job_id":"<同一个 id>","output_directory":"C:/music/delivered"})
```

等待返回未完成时继续同一 job；`automation_paused` 或需处理状态转恢复流程。上传例：`suno_upload_reference({"path":"C:/music/reference.wav","rights_confirmed":true})`，将返回 `id` 原样填进 `request.references`；不要把本机路径填到 asset_id。

没有 MCP 时使用同等 JSON CLI，所有正文放 UTF-8 文件，避免 PowerShell 转义：

```powershell
$SunoCli = 'projects/suno_browser_service/apps/cli/main.py'
./.venv/Scripts/python.exe $SunoCli capabilities
./.venv/Scripts/python.exe $SunoCli schema
./.venv/Scripts/python.exe $SunoCli plan --file projects/suno_browser_service/examples/instrumental.json
./.venv/Scripts/python.exe $SunoCli upload --file C:/music/reference.wav --rights-confirmed
./.venv/Scripts/python.exe $SunoCli create --file request.json --key ep1-theme-v1
./.venv/Scripts/python.exe $SunoCli wait --job JOB_ID --seconds 45
./.venv/Scripts/python.exe $SunoCli download --job JOB_ID --output C:/music/delivered
```

CLI stdout 只输出 JSON：成功 `{"ok":true,"result":...}`，失败 `{"ok":false,"error":...}` 且退出 1。`--file -` 可从 stdin 读 JSON。等待一次最多 45 秒，完成/暂停/需关注时提前返回；超时继续查原任务。令牌自动从私有文件或 `SUNO_SERVICE_TOKEN` 读取，不写进 MCP 配置。接口地址可通过 `SUNO_SERVICE_URL` 指定本机端口，只允许 loopback HTTP。

## 模式与参数

`mode` 默认 `advanced`，也接受 `simple` / `sounds`。所有未知参数、冲突组合和超界值拒绝；可选参数不传时使用页面默认值。生成前会读回请求指定的选项，缺控件、歧义、不可读回、标题不能设置均停止，不悄悄降级。

| 字段 | 内容 |
|---|---|
| `prompt` / `lyrics` / `instrumental` | 风格或自然语言需求；Advanced 的人声歌词；默认纯音乐 |
| `title` | 自选标题前缀，服务追加唯一 job 标记关联结果 |
| `options.model` | 页面精确模型名：v6、v6-wild、v6-mini 或已有 Custom Model |
| `options.exclude_styles` | 排除风格，最多 1000 字符 |
| `options.vocal_gender` | male / female；仅人声 |
| `options.weirdness` / `style_influence` / `audio_influence` / `variety` | 0–100，映射到页面滑杆；页面不支持的步长拒绝；audio_influence 需参考或 Voice |
| `options.duration_seconds` | 1–480 秒，页面更严限制优先 |
| `options.max_mode` / `my_taste` | 显式 true / false；Max Mode 可能增加积分消耗 |
| `options.voice_name` / `inspiration_name` | 精确选择已有 Voice/Style Persona、灵感歌单；不注册/克隆声音、不训练模型 |
| `options.sound_type` / `bpm` | Sounds 专用 one_shot / loop，BPM 20–300 |
| `references` | 最多 8 个 `{asset_id}` 或 `{url}`，二选一；URL 限 Suno song/playlist |
| `format` / `target` | mp3 / wav；制作归属目录，独立任务可省略 |

依据 [v6 FAQ](https://help.suno.com/en/articles/13924481)、[模型说明](https://help.suno.com/en/articles/13924993) 与 [Sounds 文档](https://help.suno.com/en/articles/10625537)：Simple 支持多种参考和自然语言编辑意图，Sounds 提供 One Shot/Loop。本服务为这些入口提供表单适配；Cover/Extend 等可在 Simple 的 prompt 中表达意图，但没有将 Studio 复杂剪辑操作伪装成已实现的专用 API。实际控件、上传附件展示和精确歌曲归属需在解除验证码后逐项校准。

### 参考文件

`POST /v1/assets` 使用 multipart 字段 `file`、`rights_confirmed`，先保存本机并返回 SHA256 asset_id；`GET /v1/assets/{id}` 查询并重新核对哈希。最大 64 MiB，支持 WAV/MP3/FLAC/M4A/OGG、MP4/MOV/WebM、PNG/JPEG/WebP，ffprobe 核对实际媒体。Advanced 只接受音频上传；图片/视频用 Simple。网页自身的格式/时长/数量限制更严时停止，不伪造接受。

将返回 ID 放进请求：`"references":[{"asset_id":"返回的64位ID"}]`。正式任务执行时才经网页文件输入上传 Suno，操作前记录素材名称、大小、哈希与参数。只有有权使用时设置 `rights_confirmed=true`；若网页要求权利确认而本地未确认，任务暂停，不能替用户勾选。文件内容改变会拒绝。媒体不会被 CLI 当作任意 URL 抓取。

示例见 `examples/instrumental.json`、`examples/song.json`、`examples/sound-loop.json`。预检不等于真实 UI 验收；查询任务的 `applied_options` 是实际已读回的字段，`next_action` 给代理下一步。

**当前边界（2026-10-22）：**普通 Chrome 登录成功，专用 profile 已保存；真实 Pro 账号的 v6 Advanced 表单已适配。EP1 的 M01、M02 各点击 Create 一次，未确认新歌曲；M02 随后出现验证码，整个自动化队列已持久暂停。实际 MP3/WAV 下载、Browserless 仍未验收，不能宣称真实生成链路可用。

2026-10-22 用户明确允许本服务自动 Create 和下载。Suno 当前条款仍限制 robots / scraping，未查到自有付费账号的自动化例外；遇验证码、拒绝访问或配额不足暂停，不绕过。[Suno 条款](https://suno.com/terms)。Pro / Premier 的官方下载有独立配额，以账号显示为准。[官方下载规则](https://help.suno.com/en/articles/13876865)

## Windows 启动

从仓库根目录运行（本机依赖已装，通常可跳过 setup）：

```powershell
./projects/suno_browser_service/setup.ps1
./projects/suno_browser_service/login.ps1
./projects/suno_browser_service/start.ps1
```

**默认常驻窗口模式（2026-11-03）**：`start.ps1` 启动服务后顺带运行 `open-window.ps1`，用本服务专用 profile 打开一个普通 Chrome 窗口，调试端口只绑定 `127.0.0.1:9333`（`SUNO_BROWSER_ATTACH_PORT`）。人一直开着它；服务经 CDP 接管，在自己单独的标签页里操作，断开时只停连接、不关窗口。没登录就直接在这个窗口登录，不用停服务；`login.ps1` 在本模式下只是打开 / 确认这个窗口。服务遇登录页或验证码时把窗口提到前面等人（`next_action` 为 `complete_suno_login_in_open_window` / `complete_suno_verification_in_open_window`），人花的时间不计入超时。窗口关着时任务保持 queued，`/health` 的 `browser_window` 为 `closed`；有排队任务时服务每分钟自己重开一次窗口（`SUNO_WINDOW_AUTO_OPEN=0` 关闭），若服务专用 profile 的 Chrome 还占着 profile 却不再响应端口（2026-11-03 实测出现过），先结束这一个 profile 的 Chrome 进程（审计 `window_stuck_end`，不碰人的其他 Chrome）再重开。9333 被退出卡死的 Chrome 占着（端口在监听却不应答，进程杀不掉）时，窗口改开在下一个空闲端口（9334–9343），实际端口记在私有目录 `window_port`，health、接管与审计都跟着它走；不要在别处写死 9333。窗口以 `--disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling` 打开（与 Playwright 自己启动时相同），被遮挡或最小化时服务的标签页照常渲染。窗口开着期间本机其他程序也能经该端口控制这个已登录的 Suno 窗口。`SUNO_BROWSER_ATTACH_PORT=0` 恢复下文的旧模式。

2026-11-03 实测要点：① Create 后 Suno 先跑自己的检查，生成请求可能晚很久才发出，歌曲行 3–5 分钟后才出现；Create 后在看到生成请求的应答前**不刷新标签页**（刷新会打断 Create），应答里带两个 clip id 就直接认领，否则之后每 45 秒（`refresh_seconds`）刷新列表按标题找；`SUNO_CLIP_APPEAR_WAIT` 可设「多少秒没出现歌曲行就提前报 uncertain」，默认 0 关闭。② 歌曲行出现时可能仍在生成，菜单 Download 为禁用；下载前最多等 10 分钟直到可用（`song_not_ready`）。③ 接管现有 Chrome 时 Playwright 的下载对象为空、Chrome 会存进用户「下载」文件夹；本模式下单次下载改为让 Chrome 存进私有 `downloads/` 再移到输出目录，结束后恢复窗口默认下载设置。④ 2026-11-03 晚 14 个任务连续在打开 `/create` 时 60 秒超时：服务自己的工作标签页卡住了（新标签页 4 秒就能打开）。现在工作标签页对「离开此网站？」一类 beforeunload 对话框选择离开（Playwright 默认会取消，标签页就留在原地），打开页面超时会关掉卡住的标签页、换一个新的再试一次（审计 `work_tab_renewed`）；还没提交（preparing）或只在下载时因窗口本身出错的任务自动重新排队，最多 3 次（`transient_retries`），提交后出错仍照旧报 uncertain、不重提。⑤ 同晚强制重启窗口后 Suno 重新弹出 cookie 提示（Customize / Reject All / Accept All），它盖住了 Create，点击被拦截、没有生成却报了 uncertain；服务现在遇到这个提示就点 **Reject All**（只保留网站必需的 cookie，审计 `consent_reject`），没有拒绝选项时不替用户点同意。该按钮的可访问名称是「Deny all optional cookies」。⑥ Suno 新增「Clear entire form?」确认框（`role=alertdialog`，Confirm / Cancel）：清空上一个任务留下的表单时不点 Confirm，模态框会把整张表单藏起来，之后每个控件都找不到（报 ui_changed）；现在按可见文字点 Confirm（只清空草稿，不提交）。控件找不到时审计 `control_missing` 记下候选数、打开的模态框和截图 `missing-<控件>.png`。⑦ 型号默认值：账号有 v6（Pro，「best model」）、v6-wild（Pro）、v6-mini 三种；同晚 cookie 状态丢失后页面默认从 v6-mini 变成 v6，v6 出的长度不稳定（ep16 两首只有 72 s / 60 s，ep12 两首 182 s / 167 s），v6-mini 是 3–3.5 分钟（ep01/ep02）。当晚改回 v6-mini 后的两次 Create（ep13、ep14）点完一直转圈、库里始终没有歌（v6-mini 标注为免费档，疑似排队或限流），于是页面默认又改回 v6 并经刷新确认保持；要固定型号就在请求里写 `options.model`，不写就是页面当前默认。⑧ **下载有月度上限**：Pro 账号页（suno.com/account）除了 Song credits，还有「Downloads remaining」。2026-11-04 凌晨查到只剩 1（Song credits 还有 2370）——每个任务官方下载两首，测试与 14 期配乐一晚就用光。额度不够时下载会失败而生成照样扣点数，所以下载额度见底时先暂停（`automation-paused.json`），由用户决定买下载额度、等重置，或改成每个任务只下一首。

旧模式（`SUNO_BROWSER_ATTACH_PORT=0`）：登录命令直接打开已安装的普通 Chrome，使用本服务的专用 profile；认证过程中不连接 Playwright。请手动登录 Suno，看到自己的账号后关闭该专用窗口；程序随后检查 Suno 页面并导出私有登录态，不再要求按 Enter。不要使用日常 Chrome profile。服务运行期间登录命令会拒绝占用同一 profile；先 `stop.ps1`，登录命令成功结束后再 `start.ps1`。

如果 Google 提示 “This browser or app may not be secure”，[官方说明](https://support.google.com/accounts/answer/7675428?hl=en) 列出了软件控制浏览器等可能原因。本入口已改为正常 Chrome 人工登录；不改 Google 安全设置，不伪装浏览器或绕过验证。本次用户已完成登录，后续 Suno 账号状态检查成功。手动登录目前要求 `SUNO_BROWSER_CHANNEL=chrome`；远程 Browserless 使用其自身交互会话。

- OpenAPI / 调试页：`http://127.0.0.1:8770/docs`
- 健康：`http://127.0.0.1:8770/health`（只表示 worker 存活，不表示 Suno 已登录）
- 后台启动：`start.ps1`（并打开常驻窗口）；前台：`start.ps1 -Foreground`
- 常驻窗口：`open-window.ps1`（已开着就只确认）
- 平滑停止：`stop.ps1`；等待当前浏览器操作退出，不强杀其他进程
- 运行数据：`.audit/service_requests/suno_browser_service/`。Windows ACL 限当前用户、SYSTEM、Administrators；profile、storage-state、token 不进 Git。

## 调用示例

所有 `/v1` 接口必须带 Bearer token。首次启动自动在私有目录创建 `service-token.txt`；不要把它写进 prompt 或日志，也不要提交 Git。可用 `SUNO_SERVICE_TOKEN` 环境变量覆盖（至少 24 字符）。

```powershell
$Token = (Get-Content .audit/service_requests/suno_browser_service/service-token.txt -Raw).Trim()
$Headers = @{ Authorization = "Bearer $Token"; 'Idempotency-Key' = 'episode-01-bgm-001' }
$Body = @{ prompt = 'Warm cinematic piano, gentle strings, reflective, no vocals'; instrumental = $true; format = 'mp3' } | ConvertTo-Json
$Job = Invoke-RestMethod http://127.0.0.1:8770/v1/jobs -Method Post -Headers $Headers -ContentType 'application/json' -Body $Body
Invoke-RestMethod "http://127.0.0.1:8770/v1/jobs/$($Job.id)" -Headers $Headers
```

相同幂等键与相同参数永远返回同一任务；修改参数须用新键。生成一次通常产生两首；不要因 HTTP 超时换新键重试。Advanced / Custom 模式自动设置 `suno-job-<job ID>` 标题，精确关联新歌曲，避免误收库中旧歌。

状态 `completed` 后，响应 `files` 中每项含 `name`、`bytes`、`sha256`、`song_url`：

```powershell
$Job = Invoke-RestMethod "http://127.0.0.1:8770/v1/jobs/$($Job.id)" -Headers $Headers
$File = $Job.files[0]
Invoke-WebRequest "http://127.0.0.1:8770/v1/jobs/$($Job.id)/files/$($File.name)" -Headers $Headers -OutFile $File.name
```

可选 `target` 为仓库 `ai_videos/` 下已有的剧/集/资产目录，决定请求日志归属；音乐文件仍由服务保存。未指定时记录到独立服务审计目录，不创建虚构剧。Advanced 人声用 `instrumental=false` 和 `lyrics`，prompt 表示音乐风格；Simple 人声可在 prompt 中描述歌词需求。

| 接口 | 用途 |
|---|---|
| `GET /v1/capabilities` | schema、功能边界、上传限制与暂停状态 |
| `POST /v1/plan` | 本机参数/参考预检，不创建任务或操作网页 |
| `POST /v1/assets` / `GET /v1/assets/{id}` | 本机参考素材上传与哈希核对 |
| `POST /v1/jobs` | 提交；必填 `Idempotency-Key` |
| `GET /v1/jobs` | 最近 100 个任务 |
| `GET /v1/jobs/{id}` | 状态、错误、歌曲链接和成品元信息 |
| `GET /v1/jobs/{id}/files/{name}` | 下载已登记成品 |
| `POST /v1/jobs/{id}/resume` | 恢复暂停任务；不重提未知生成 |

## 暂停与恢复

Job 的 `request` 表示请求参数（旧任务可能没有新增字段）；`applied_options` 是网页已读回的选项，不是生成质量保证；`next_action` 是下一步提示。`song_urls` 代表已确认链接，`files` 代表实际已下载文件，每项有 `name/bytes/sha256/song_url`。时间字段为 UTC ISO 格式。`files=[]` 或只有歌曲链接时不能宣称音频完成。

| 状态 | 处理 |
|---|---|
| `completed` | 核对 files，下载并试听；需要另一首才明确创建新任务 |
| `needs_login` | 停服务→登录→启动→对该任务 `resume` |
| `needs_attention` | 读取 `error`；处理界面、额度、网络或下载问题后恢复 |
| `uncertain` | 可能已扣积分；在 Suno 确认结果后提供歌曲 URL，仅补收 |
| `queued / preparing / submitting / waiting / downloading` | 正在处理；禁止并发恢复 |

```json
{"song_urls":["https://suno.com/song/00000000-0000-0000-0000-000000000001"]}
```

将上面的真实歌曲地址作为 `POST /v1/jobs/{id}/resume` 的 JSON。已知歌曲链接的下载失败可以传 `{}`；已完成的第一首保留并校验后跳过，只补收失败条目。可能提交且没有歌曲链接时拒绝空恢复，避免重扣积分。

**有人值守的验证（2026-10-24）**：服务默认以可见窗口运行浏览器（`SUNO_BROWSER_HEADLESS=1` 才隐藏）。Suno 在点 Create 时常弹 hCaptcha；可见模式下服务把窗口提到前台、不碰验证码，等人在窗口里完成（默认 600 秒，`SUNO_CHALLENGE_WAIT` 调整），期间任务 `next_action=complete_suno_verification_in_open_window`；完成后同一任务继续，超时才按下述暂停。隐藏模式或远程 Browserless 不等待，直接暂停。

**常驻单窗口（2026-10-24）**：本机模式默认只开一个浏览器窗口，所有任务在里面排队复用（审计记 `browser_reuse`），不再每个任务新开、做完即关；人把窗口关掉，下一个任务会重开；服务停止时关闭。`SUNO_BROWSER_KEEP=0` 恢复旧行为。验证码仍由人在这个窗口里完成，服务不隐藏自动化特征、不自动解验证码。

**重新认领（recollect，2026-10-24）**：已提交但 `uncertain`、超时或认错的任务，`resume` 传 `{"recollect": true}`（CLI `--file`，MCP `recollect=true`）只到库里用搜索框按标题 / Sounds prompt 找回两条，不填表、不点 Create、不收费；已下载文件的任务不能用，也不能与 song_urls 同传。

验证码超时会在私有目录写入 `automation-paused.json`，暂停整个队列，重启不会清除。`/health` 的 `automation_paused=true` 表示 API 可查询但不执行浏览器任务。人工处理后运行普通 Chrome 登录流程并完成校验，才清除暂停；`-Inspect` 不清除。已提交但结果未知的任务仍须核对歌曲 URL，只补收，不能空恢复重生成。不要手工删除暂停文件来绕过验证。后续发生验证时保存私有 `challenge.json/png`；当前触发证据在本集 request_log.md。

### 错误与重试契约

HTTP 业务错误示例：`{"error":{"code":"idempotency_conflict","message":"同一幂等键已用于不同请求"}}`；FastAPI schema 错误用 `{"detail":[{"loc":["body","mode"],"msg":"...","type":"..."}]}`。HTTP 202 仅表示本机接受任务；后续执行错误在 Job.error，不能仅靠提交状态码判断生成成功。

| 情况 | HTTP / code | 调用者应做什么 |
|---|---|---|
| 无效令牌 | 401 | 从本机私有配置确认服务令牌，不使用 Suno 密码 |
| 未知字段/冲突选项/非法目标 | 422 / detail 或 invalid_options、invalid_target | 修正参数，plan 仅校验 schema/资产，提交仍校验目标和媒体模式组合 |
| 上传过大/无效媒体 | 413 asset_too_large / 422 invalid_media | 使用范围内有效文件；确认 ffprobe 可用 |
| 同键不同请求 | 409 idempotency_conflict | 找回原任务并核对；仅明确新创作时使用新键 |
| 文件/任务不存在 | 404 | 使用服务返回的 id/name，不自行拼造路径 |
| 资产被改写 | 409 asset_changed | 重新上传当前文件取得新 id，勿覆盖原资产 |
| 不可恢复或未知歌曲 | 409 job_active / song_urls_required | 查询原任务；未知提交核对 Suno 歌曲后补收 |
| 本机服务不可达/提交超时 | CLI service_unavailable 或连接错误 | 启动服务，保持原请求和幂等键；不换键重提 |
| 网页控件、登录、验证码等 | Job.error | 读 status/next_action；校准或人工处理后恢复原任务 |

没有删除任务、取消已提交生成、自动清验证码或批量重试接口。下载到指定目录由 MCP/CLI 完成；HTTP 下载返回字节，调用方自行保存。Browserless 只是浏览器后端选项，本机 API/MCP 仍为 loopback 服务。

## 页面校准

当前控件按英文可访问名称匹配；已适配 v6 的 Advanced、Lyrics editor、Create song。v6 Sounds（2026-10-24 现场核对）：切换标签后面板延迟渲染，控件查找等待最多 15 秒；prompt 上限 500 字符；Type 为 One-Shot / Loop，选中状态读 `data-selected`；另有 BPM（Auto）与 Key（Any）；**没有标题框和时长控件**，所以 Sounds 不能设 `duration_seconds`，结果按库列表里片段行显示的 prompt（只比字母数字，前 80 个）认领提交后新出现的两条；同账号多个会话并发也不会认错，但不要同时排两条 prompt 开头相同的 Sounds。页面还有 Speech（朗读）标签，服务尚未接入。v6 纯音乐将歌词清空，Styles 超过页面上限（本次 1000 字符）在提交前拒绝；旧 Custom 开关仍支持。官方歌曲页面有播放器的 More actions 和推荐列表的多个 More options；下载只点本歌曲行内的 More options（3 层内含本歌曲链接）→ 菜单项 Download → 弹窗里的 MP3 / WAV（另有 M4A、MP4、Stems）。弹窗显示账号下载余量（Pro，2026-10-24 时 27 次，次日刷新）。`login.ps1 -Inspect` 将可见控件名称、placeholder、ID 写入私有 `controls.json`，不导出输入值。如报 `ui_changed / ui_ambiguous`，在同一私有目录创建 `selectors.json`，按现场 DOM 覆盖以下键的 CSS selector：

`custom, style, title, lyrics, instrumental, create, more, download, mp3, wav`

扩展控件键：`simple, prompt, model, model_choice, voice_name, voice_name_choice, inspiration_name, inspiration_name_choice, exclude_styles, vocal_gender, weirdness, style_influence, audio_influence, variety, duration_seconds, max_mode, my_taste, sound_type, bpm, upload_input, add_reference, upload_confirm, reference_chip, reference_url, attach_reference`。保持每个 selector 指向唯一控件；不能用覆盖配置绕过选中状态核验。

每个 selector 必须唯一匹配可见控件；未知键拒绝。配置只接受 CSS，不执行脚本。歌词、样式、标题和纯音乐状态会检查，找不到时停在提交前；不盲点相似按钮。官方新弹窗、下载转换流程或 UI 变化仍可能需要适配代码。

## Browserless

本机不需要 Browserless 账户。要接远程服务，设置 `SUNO_BROWSER_WS` 为 **原生 Playwright** 连接，例如 `wss://<your-fleet>/chromium/playwright?token=...`，并在服务私有目录放置登录导出的 `storage-state.json`。该文件含凭据，只用于目标 Suno 页面。端点 token 只放环境变量。

`chromium.connect()` 与 `download.save_as()` 对应 [Browserless 官方文件传输方式](https://docs.browserless.io/baas/features/file-transfers#playwright)。客户端与服务端 Playwright 主、次版本须匹配。普通 CDP URL 不受支持；不要传 `/` CDP 端点。远程首次登录在 Browserless 自身交互会话完成，本服务的 `login.ps1` 仅支持本机。未连接实际实例，不承诺登录态跨环境可直接复用。

其他环境变量：`SUNO_BROWSER_CHANNEL`（默认 chrome）、`SUNO_BROWSER_HEADLESS`（默认 0 可见，1 隐藏）、`SUNO_BROWSER_KEEP`（默认 1 常驻单窗口，0 每任务开关）、`SUNO_GENERATION_TIMEOUT`（默认 600 秒）、`SUNO_BROWSER_ATTACH_PORT`（默认 9333 常驻窗口，0 关闭）、`SUNO_CLIP_APPEAR_WAIT`（默认 0 关闭）、`SUNO_WINDOW_AUTO_OPEN`（默认 1 有排队任务时自动重开常驻窗口，0 关闭）、`SUNO_SERVICE_PORT`（默认 8770）。服务始终绑定 127.0.0.1；没有做公网部署。

## 验证与审计

```powershell
./.venv/Scripts/python.exe -m pytest projects/suno_browser_service/tests
./.venv/Scripts/python.exe -m pytest tools/tests/test_service_request.py tools/tests/test_suno_request_audit.py
```

本地浏览器测试使用真实 Chrome 与本机 HTTP fixture，阻断外网；与 Suno 实测分别记录。服务的连接、导航、填写、提交、轮询、官方下载通过 `tools/service_request.py::RequestLog`，request 落盘失败就不调用。浏览器网页自行发出的内部 HTTP 不宣称逐条拦截，费用没有回执时记未知。

运行证据与待办见 [validation/result.md](../../specs/development/suno_browser_service/validation/result.md)。程序结构为 `apps/`（入口）与 `libs/`（业务/存储/浏览器）。令牌创建与私有目录初始化属于启动准备；不作为用户任务的业务写操作。
