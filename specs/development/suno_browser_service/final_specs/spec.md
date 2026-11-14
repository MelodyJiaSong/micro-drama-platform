# Suno 浏览器服务

## Goal
通过本机后台浏览器操作用户付费 Suno 账号，输入 prompt、自动生成并经官方下载音乐；其他 agent / 程序通过 HTTP API 调用。兼容 Browserless 的 Playwright 连接。

## 用户确认
2026-10-22：采用“本机后台浏览器，兼容 Browserless 接入”；“Suno 作为例外，自动生成并下载”。该例外仅适用于本服务，不修改其他生成的人点规则。

## User roles & primary flows
用户首次在独立浏览器窗口登录 → 程序提交带幂等键的音乐任务 → 查询状态 → 取得音频文件。验证码、账号失效或网页变更时保留任务供人工处理。

## Functional requirements
1. `POST /v1/jobs` 接收 prompt、instrumental、format（mp3/wav）、target、可选 lyrics；返回 job ID。必填 Idempotency-Key，同键同请求返回原任务，同键不同请求拒绝。默认 Advanced 纯音乐；Advanced 人声须提供歌词，v0.2 的 Simple 可仅通过 prompt 提出写词需求。
2. 后台按单账号串行执行；SQLite 保存任务、提交前基线、歌曲链接、已下载文件及错误状态。服务重启不重提结果未知的生成。
3. 只经网页填写、点击 Create、观察新歌曲、使用官方 Download 菜单；不调用逆向私有 API，不绕过验证码、账号限制及下载配额。
4. 登录使用专用本机 profile，程序不接收用户 Suno 密码。提供独立登录命令：先正常启动已安装的 Chrome，由用户手动认证且不连接自动化；关闭专用窗口后才由程序验证 Suno 页面并保存状态。任务遇登录失效暂停。远程连接可使用 Playwright 原生 endpoint，登录态通过本机私有 storage state 导入。
5. 查询与文件 API 有 Bearer 鉴权；默认仅监听 127.0.0.1。输出文件仅可按 job ID 与安全文件名读取。
6. 生成前先持久化 submitting，收费调用前写 RequestLog。超时不自动再次 Create。提供恢复已知 song URL 的接口，只补收不重生成。
7. 采用 Advanced / Custom 模式设置唯一任务标题；这是自主执行时为可靠关联作出的实现判断。已有歌曲与并发手工生成不可误收；一次收取本次新增且标题精确匹配的两首，发现歧义暂停。歌曲链接出现后继续等待官方下载控件可用，不把链接出现算作音频完成。每条音频下载完成后原子落盘并计算大小/哈希。
8. 每个浏览器连接、页面导航/准备、提交、轮询、下载均在调用前记录。网页自身后台网络请求不宣称逐 HTTP 拦截；费用未知照实记录。
9. 验证码或拒绝访问触发整个队列的持久暂停；重启不清除，健康接口暴露 automation_paused。人工登录校验后解除队列暂停，仍保留未知提交的幂等保护。
10. v0.2 在保持旧请求及幂等指纹兼容的基础上增加 mode（advanced/simple/sounds）、标题前缀、严格 options 与 references。模型、排除风格、性别、Weirdness/Style/Audio/Variety、时长、Max Mode/My Taste、已有 Voice/Inspo、Sounds 类型/BPM 传到 UI 并核对；未识别选项拒绝，不忽略。Simple 人声可仅提供 prompt，Advanced 仍须明确歌词。
11. 参考媒体先经鉴权 multipart API 保存本机（最大 64 MiB、哈希校验和媒体探测），任务只使用 asset_id，不接收服务端任意文件路径；正式网页上传前审计并核对原哈希。支持 Suno 歌曲/歌单 URL，禁止任意远程媒体抓取。UI 要求权利确认时，只有显式 rights_confirmed 才可勾选。
12. GET capabilities 和 POST plan 提供机器可读 schema、选项限制、暂停状态、实测边界；plan 不建任务、不操作浏览器、不收费。Job 响应含 request、applied_options、next_action。
13. JSON CLI 与 stdio MCP 共用 HTTP API、鉴权、幂等与错误，MCP 暴露九个工具；本机 token 不写入 prompt 或配置。提供两端 MCP 注册脚本和共用 suno-music skill。下载回本机目录后核对 SHA，遇同名不同内容保留原文件。
14. HTTP/OpenAPI 与 MCP 的每个输入字段、每个操作必须说明用途、默认值/限制、返回值、付费副作用、幂等与恢复。README 提供端到端示例、Job/错误契约；description 从共享 schema 暴露，避免 UI/MCP 分叉。
15. 提供 light theme React/TypeScript UI `/ui/`：三模式、参考上传/链接、全部可选字段、预检与生成、最近任务/搜索/自动刷新、错误恢复、音频试听和 SHA 校验后下载。所有业务调用仍经鉴权 API。token 仅页面内存；提交回执丢失保留原请求/键至当前标签页 sessionStorage，刷新后可重试原键，不新建重复任务。暂停时禁止新生成，仍可预检/取回；不暴露秘密、登录 cookie 或任意本机文件。
16. 所有新音频生成默认走本服务，包括环境声、音效、配乐、主题曲等；其他未支持音频需求先查能力并报告缺口，不自动切引擎。共用流程覆盖生成前需求/归属、预检、稳定键、查询/恢复、校验下载、试听与混音交接。现有音频复用及后期剪辑/响度不属于新生成。

## Non-functional requirements
保留用户现有工作区改动。沿用 apps/libs 分层、dependency-injector。全局服务日志归属 `.audit/service_requests/suno_browser_service/`；指定制作目标必须位于仓库 ai_videos 下。运行配置、cookies、令牌不进 Git 或日志。

v0.2 局部结构约定：HTTP、MCP 与 CLI 的共享 Pydantic 请求 schema 唯一放 `libs/common/generation.py`，避免三个 transport 各维护一份选项；这是本项目对通常路由内请求体位置的限定例外。该文件只做类型、边界与组合验证，不进行 I/O；domain 不导入它。应用 Queries/Commands 分开，网页操作和 HTTP 客户端仍在 infrastructure。

## Acceptance criteria summary
真实 HTTP 提交/查询/文件链路、本地浏览器 fixture 的输入→生成→下载、幂等并发与崩溃恢复、路径与鉴权边界、日志失败不发请求。真实 Suno 登录及一次音乐生成/下载另作联调，不用 fixture 结果冒充。

## Out of scope
本次不提供多账号、多用户门户、声音注册/验证、模型训练、公开发布、Studio 时间线编辑、验证码代解或绕过下载配额。Simple 可以自然语言表达编辑/自动歌词意图，复杂 Remix 专用操作不保证支持；不把选项 schema 当 UI 实测。Browserless 无现成实例，连接代码明确未实测。

## Open questions
真实登录与 Pro 套餐已确认，v6 基础表单曾校准；当前验证码阻塞生成，实际下载流程仍未验收。新增模式、上传、更多选项已有实现和离线测试，但缺真实账号逐项联调；Simple/Sounds 若不能设置精确任务标题则必须在 Create 前停止，不能误收库中其他生成。

2026-10-24（follow-up 007）：本机模式默认常驻一个浏览器窗口，任务间复用同一上下文；窗口被关后下一任务重开；`SUNO_BROWSER_KEEP=0` 恢复每任务开关。验证码仍由人在窗口完成，不隐藏自动化、不自动解。
