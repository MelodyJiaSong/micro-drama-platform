# 用户原始需求

我有https://suno.com/ 的付费账户，由于他没有api接口，我需要你帮我通过browserless的web 自动工具，模拟输入prompt，然后自动下载生成好的音乐，然后把这个build成一个service其他的agent或程序可以调用。

# Suno 服务追加指令 · 2026-10

---

## 001 — 2026-10-22 19:53:27 — 修复 Google 拒绝自动化浏览器登录

### 指令

用户愿意手动登录，随后反馈 Google 提示 “This browser or app may not be secure. Try using a different browser.”；修复首次登录流程并继续 EP1 配乐任务。

### 处理

保留专用 profile。登录入口改为直接启动普通 Chrome，不使用 Playwright 认证、不开放调试端口；用户看到 Suno 账号后关闭窗口，程序再验证并导出状态。Google 官方将自动化浏览器列为拒绝登录原因之一，属于与现场吻合的原因判断，不能据此保证普通浏览器一定通过。原 API 任务和幂等键保持，不重复下单。

### 当前结果

已打开普通 Chrome 专用窗口，等待用户认证。相关离线浏览器及审计回归 17 passed；真实登录是否成功待窗口关闭后的实际检查。认证前服务保持停止。

---

## 002 — 2026-10-22 21:32:33 — 扩展网页选项与双代理接口

### 指令

尽可能纳入 Suno 网页的模式、参数和上传参考文件，并提供对 Claude Code 与 Codex 友好的调用接口。

### 执行判断

按现有项目局部扩展，不重跑六阶段。HTTP 保留旧请求兼容，增加严格参数、素材上传、无收费预检与能力发现；提供 JSON CLI、stdio MCP、共用 skill 和两端安装入口。基于官方 v6 文档及已保存页面证据覆盖 Advanced / Simple / Sounds、模型、参考媒体与更多设置；实际缺少控件或无法读回时在 Create 前拒绝，不能静默丢参数。界面支持、离线测试、真实账号验收分别标注。

Suno 验证码暂停不清除，本轮不为选项测试消耗生成额度；已有结果未知的 M01/M02 不重提。既有授权持续有效，不再询问可自行决定的实现选择。参考素材先存本机私有目录、记录哈希，只有正式浏览器任务才上传 Suno 并先写请求日志。用户调用不会隐式训练模型、创建声音、公开发布或更改账号。

### 摘要

已实现 v0.2：三种模式、14 个高级选项、上传/引用媒体、capabilities/plan、9 个 MCP 工具与 JSON CLI；共用 suno-music skill 两端入口已同步。Claude 项目 MCP 与 Codex MCP 已实际注册且复跑幂等，其他配置保留。全套服务/审计测试 146 passed、1 skipped；最终时长单位校验后相关表单/API 37 项再验通过。真实 Suno 验证码仍在，新增 UI 功能和官方下载未作真实生成验收，Browserless 未实测。

---

## 003 — 2026-10-22 22:50:13 — 文档说明与流程接入

### 指令
确保 API 有足够的文档和 description 帮助其他人理解；确认 MCP 实现，并加入共用制作流程。

### 摘要
补全所有生成字段、HTTP 操作与九个 MCP 工具的用途、参数、返回值、副作用、错误和恢复语义；README 提供串联示例。把能力发现→预检→固定键生成→查询→下载→试听→混音交接接入声音模块和全景。MCP 已实现并注册，不把配置存在当当前会话已加载。

---

## 004 — 2026-10-22 22:50:13 — 本机创作 UI

### 指令
为工具加 UI，用户可以操作类似 Suno 网页提供的模式、参考、选项、生成和音频结果。

### 执行判断
新增 React/TypeScript 本机工作台，与 API 同源挂载 `/ui/`，保持 light theme。复用既有 schema/队列/审计，不新增浏览器生成入口。覆盖三模式、十四项可选参数、上传与 URL 参考、预检、进度、错误恢复、试听和校验后下载。token 只存页面内存，未明确回执的提交在 sessionStorage 保留原请求和幂等键，刷新可安全重试。已知能力缺口和验证码暂停在 UI 明示，不提供未实现的 Studio 编辑/训练/发布。

### 摘要
实现可构建、可运行的本机 UI，配套真实 Chrome + 本机 HTTP 的集成验证与桌面/手机布局检查；真实 Suno 使用现有暂停状态，不为 UI 验收付费生成。

---

## 005 — 2026-10-22 22:50:13 — 所有音频生成默认 Suno

### 指令
制作流程的环境音、背景音、主题曲等一切新音频生成默认使用该 API。用户继续要求自主完成、不询问可判断事项。

### 执行判断与摘要
共用 sound 模块、pipeline、独立资产入口、paid_services、suno-music skill、全景与机器 capabilities 使用同一默认路由。环境/动作声用 Sounds，配乐与歌曲用 Advanced/Simple；不支持的准确 TTS/克隆/分离先报能力缺口，不静默换引擎。已有资产可复用，混音/剪辑/响度处理继续本机工具。Suno 的验证码和未知提交保护保持，自动生成授权不扩展到视频服务。MOSS/ACE-Step 等只作用户明确选择的替代。

## 006 — 2026-10-24 — Sounds 现场适配与有人值守验证

### 指令
用户：「如果这个service没启动，你自己启动就行，或者可能有mcp了」「你过程中感觉sunoapi有什么需要improve的，你就直接改了就行」。来源：dota_yingxiong follow-up 113（全能骑士技能音效）。

### 执行判断与摘要
- 现场问题：五条 Sounds 任务全部 `ui_changed: 找不到 prompt`（未提交、未扣费）。只读检查真实 v6 Sounds 页（`controls_sounds*.json`、`inspect_sounds*.png`，私有目录）：面板切标签后延迟渲染；prompt 上限 500；Type 按钮写作 One-Shot、选中态在 `data-selected`；有 BPM / Key；**没有标题框和时长控件**；另有 Speech 标签。
- 改动：`FormClient.find` 等待 15 秒；`selected` 认 `data-selected`；sound_type 标签兼容 One-Shot；Sounds 无标题框时不填标题、提交前不核标题，收取按「提交后新增片段、连续两次轮询一致」（上限 4）；请求校验拒绝 Sounds 的 `duration_seconds` 与超过 500 字的 prompt；本机 UI 同步去掉 Sounds 时长并重建。
- 第一条真实任务（k32 施放，`bca6dea1`）表单填写正确，点 Create 后 Suno 弹 hCaptcha，服务按旧规则暂停、任务 uncertain。随后只读核对库：baseline 之外无新片段，确认未生成。
- 有人值守验证：服务改为默认可见窗口（`SUNO_BROWSER_HEADLESS=1` 才隐藏）；遇验证码把窗口提到前台、不碰验证码，等人完成（默认 600 秒，`SUNO_CHALLENGE_WAIT`），期间 `next_action=complete_suno_verification_in_open_window`，完成后同一任务继续；超时、隐藏模式、远程 Browserless 仍按原规则暂停。不自动解验证码。
- 测试：`pytest projects/suno_browser_service/tests` 141 passed / 1 skipped（新增 v6 Sounds 夹具、验证等待 / 超时 / 隐藏模式用例）。README「页面校准」与暂停段、`suno-music` skill、`modules/sound.md` 同步。
- 未验证：Sounds 成品下载菜单仍未实测；可见窗口能否减少验证码出现未知。

## 007 — 2026-10-24 11:20:00 — 常驻单窗口

### 指令
用户（来自 dota_yingxiong Luna 技能音效任务）：「每次suno都跳出新的brower，然后verfify I am human,有没有办法一劳永逸解决这个问题」。经说明「一劳永逸」只能靠绕过验证、不做之后，用户选「先做1吧」（常驻一个窗口），并「2也可以做」（攒批提交，属使用方式，非代码改动）。

### 执行判断与摘要
- 原因：登录态本来保留在专用 profile；跳出的是点 Create 时 Suno 的 hCaptcha（由 Suno 风控决定），以及每个任务各开一次 Chrome、做完即关。
- 改动：本机模式默认常驻一个浏览器窗口（`Settings.keep_browser`，`SUNO_BROWSER_KEEP=0` 恢复每任务开关）；后续任务复用同一上下文并把窗口提到前台，审计记 `browser_reuse`；窗口被人关掉则下个任务重开；worker 线程退出时关闭。Playwright 同步 API 只在 worker 线程使用。远程 Browserless 与手动登录不变。
- 不做：不隐藏自动化特征、不接打码服务、不自动解验证码（违反 Suno 条款与本服务既有规则）。验证码是否因此变少未知，待实测。
- 测试：新增 `tests/libs/test_kept_browser.py`（假 Playwright：复用、窗口关闭后重开、关闭清理、环境变量默认）。
- 续（同日）：同账号有其他会话（水晶室女、Luna）并发排 Sounds，「提交后新增片段」认领会串号 → 改按库列表片段行显示的 prompt（只比字母数字前 80 位）认领两条。下载：歌曲页有播放器 More actions 与推荐列表多个 More options，改为只点本歌曲行内的 More options；Download 弹窗是多选格式（MP3 默认勾），先只勾目标格式并读回 ✓ 再点 Download / Unlock & Download（此前一次拿到 MP3、一次等不到下载）。新增 `resume` 的 `recollect`（只到库里用搜索框按标题 / prompt 重新认领，不填表不点 Create，90 秒找不到就报）与 `cancel`（只取消从未提交的任务；HTTP / CLI / MCP 都有，MCP 工具 10 个）。全量测试 147 passed / 1 skipped。实测：全能骑士 k31 / k32 施放 4 条 WAV 官方下载成功（48 kHz）。

---

## 008 — 2026-11-03 19:25:19 — attach-open-window

> severity: medium

### 指令

改进流程：我自己一直开着一个窗口，服务直接在里面操作，不用每次等太久；用户同意按建议实施

### 摘要

常驻窗口连接模式：open-window.ps1 以服务专用 profile 开普通 Chrome（仅 127.0.0.1 调试端口），服务经 CDP 接管；窗口内直接登录无需停服；验证码/登录墙即时提示并在同窗口等人；验证码未解即消失时提早报 uncertain

---

## 009 — 2026-11-04 00:17:46 — window-self-recovery

> target_artifacts:
>   - projects/suno_browser_service/libs
>   - projects/suno_browser_service/README.md
> severity: high

### 指令

用户：「做完之后请仔细review和审查你的工作产出，然后用suno 配上音乐……」；随后：「接下来我要睡觉了，你需要尽可能多的完成之后你能想到的步骤，不要问我问题……」。执行边界（代理判断）：各期的找图、审片、预览页由各自会话负责，本会话不重复做；本会话负责 Suno 服务——排行榜 14 个配乐任务全部在打开 /create 时 60 秒超时（服务工作标签页卡住、窗口被遮挡时渲染被节流、退出卡死的 Chrome 占着 9333 端口），修到服务无人值守也能自愈，再把没提交过的任务原 job 恢复。

### 摘要

Suno 服务常驻窗口自愈：卡住的标签页自动换新、窗口不节流、端口卡死换口、窗口没了自动重开、未提交的窗口错误自动重排

---

## 010 — 2026-11-14 13:00:36 — allow_edu_videos_target

> target_artifacts:
>   - projects/suno_browser_service/libs/application/commands/job__command.py
>   - projects/suno_browser_service/libs/common/generation.py
>   - projects/suno_browser_service/tests/api/test_jobs.py
> severity: low

### 指令

（edu_videos 热点相迎 t01 需要 Suno 配乐，用户要求 Suno 配乐）

### 摘要

target 归属根放宽为 ai_videos 与 edu_videos（RequestLog 已支持 edu_videos/<系列>/<知识点>，suno-music skill 也如此约定）；根目录与不存在路径仍拒绝；测试补 edu_videos 两例

---

## 011 — 2026-11-14 14:42:40 — song_menu_titled_label

> target_artifacts:
>   - projects/suno_browser_service/libs/infrastructure/writers/audio__writer.py
>   - projects/suno_browser_service/tests/libs/test_browser.py
> severity: medium

### 指令

suno 我看到你 create 成功了（下载卡在 ui_ambiguous：more 匹配多个可见控件）

### 摘要

实测 Suno 歌曲页自己的菜单按钮改名为 More options for <歌名>；下载先找该按钮（唯一即用），找不到再退回原 More options 逻辑；补回归测试
