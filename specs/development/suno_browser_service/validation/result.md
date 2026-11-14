# 验证结果（2026-10-22）

当前：普通 Chrome 登录成功，v6 Advanced 表单已适配；真实 EP1 M01/M02 各点击 Create 一次，未确认歌曲。M02 随后检测到验证码，整个队列持久暂停。`http://127.0.0.1:8770/health` 为 200、`automation_paused=true`，表示查询可用、浏览器任务不执行。真实生成/下载与 Browserless 仍未验收。

以下为初始实现时的历史验证；当前回归与联调结果见文末。

| 范围 | 实际结果 |
|---|---|
| 服务 + 共用 RequestLog 测试 | `102 passed, 1 skipped`，36.97 秒；2 条 uvicorn/websockets 依赖弃用提醒 |
| 工作流目录回归 | `12 passed, 1 skipped`，2.89 秒 |
| 真实浏览器离线端到端 | 包含在上面：真实 uvicorn HTTP → worker → SQLite → Chrome → 两首 WAV → HTTP 文件字节/哈希；第二首失败后仅补收第二首，总 Create=1 |
| Windows 私有目录、junction | 实测 ACL 限当前用户/SYSTEM/Admin；读写均拒绝越界，拒绝前不在外部创建目录 |
| 两项 skip | 当前用户无 Windows symlink 创建权限；junction 等价路径逃逸检查实际通过 |
| 实际进程 | `start.ps1` 启动成功；`stop.ps1` 正常停止；再次启动与健康/鉴权/幂等/任务查询成功 |
| Python 编译 | `compileall` 通过 |
| 工作流/skill 入口 | 11 组 / 190 源，编号连续；5 个 canonical skill / 10 个 Claude 入口检查通过 |
| 真实 Suno | Chrome 实际访问到登录页；未进入付费账号。后续 `needs_login`，不假报已生成 |
| Browserless | 文档与连接代码已核对；无实际 endpoint，未实测 |

默认端口原候选 8766/8767 被其他服务占用，最终使用已核实空闲的 8770；未终止这些进程。启动先绑定端口，避免端口冲突时 worker 提前处理生成任务。后台脚本适配 Windows venv Python 启动器父子 PID。

独立审查发现的空 token、活跃任务恢复、读写路径越界、Windows ACL 和下载等待问题已修复并复验；人声输入要求已明确在规格和 README。三名独立 worker 分担研究、策略、API/浏览器验证与审查，没有把作者自审当独立审稿。

## 接续位置

1. 按 [README](../../../../projects/suno_browser_service/README.md) 停服务，在专用 Chrome 完成首次登录，再启动。
2. 用 `login.ps1 -Inspect` 读取当前可见控件；必要时校准私有 `selectors.json`。默认英文可访问名称是未登录条件下的实现候选。
3. 登录后联调一次生成和官方 MP3/WAV 下载，验证套餐、歌曲归属、完整可播放音频；在此之前不宣称 Suno 可用。

用户已要求自主完成、不再提问，本次未向用户追加登录请求，也未猜测凭据。`validation.requires_manual_walkthrough` 保留为未完成项。

运行证据：`.audit/adhoc_agents/2026-10-22/suno_browser_service-20261022-125046/`；真实任务 `218794c61d734babb532a3c9ad334b1f`，boot-smoke.json；请求日志 `.audit/service_requests/suno_browser_service/request_log.md`。没有提交 Git commit，也未覆盖工作区原有制作/管理应用改动。


## Follow-up 001：首次 Google 登录修复

用户实际遇到 Google 不安全浏览器提示。原 Playwright 登录窗口已结束；新入口用普通 Chrome、同一专用 profile，待用户关闭后验证和导出。实际进程检查没有 automation 或 remote-debugging 参数；这只确认启动方式，不证明 Google 接受登录。

`test_manual_login.py` + `test_browser.py` + `test_suno_request_audit.py`：17 passed / 18.33 秒，覆盖日志失败禁止启动、远程配置禁止误开本机 profile，以及原 Chrome 表单、下载和 Cookie 持久化回归。真实 Google 登录和账号内生成仍待检查。

工作流编号同步：11 组 / 191 源，新增手动浏览器实现已登记。全库工作流测试为 11 passed、1 skipped、1 failed：仙侠共享 README 新引用的 `ai_videos/_shared/xianxia/STATUS.md` 未登记，属于本次 Suno 改动范围外的共享文件；本轮未修改其内容，也不宣称全库检查通过。审计：`.audit/adhoc_agents/2026-10-22/suno-manual-login-001/result.json`。


## 当前 v6 联调与回归

- 用户确认已登录后，专用 profile 与 storage state 实际保存；账号菜单、Pro 套餐和 v6 表单均实际读取。首次生成前为 2470 credits / 27 downloads；M01 核对时仍为同值，不能据此断言没有提交。M02 后未继续查询配额，费用未知。
- M01 `11bb141ca9164b79b88825820db8dc99`、M02 `7559bb5d429a420a8c9c55480aa3384f` 的请求日志各恰好一条 Create request。M01 未找到精确标题结果；M02 于 2026-10-22 20:10:28 检测到可见验证码 iframe，错误 `challenge`，未再次生成或继续其余四条。
- 新适配覆盖 Advanced 与旧 Custom 分辨、同名 Duration Custom 不误点、v6 歌词清空、Styles 长度与回读。验证码暂停整个队列，重启保留；HTTP 查询和已有文件服务仍可用。人工普通窗口登录校验后解除队列暂停，提交结果未知的任务仍需歌曲 URL。
- 实际下载未验收。已读官方菜单，但完整加载后的歌曲页有主操作和播放器两处 More options，默认唯一匹配会停止；需要后续现场校准。未下载已有歌曲来假冒本次生成。
- `pytest projects/suno_browser_service/tests tools/tests/test_suno_request_audit.py tools/tests/test_service_request.py -q --tb=short -ra`：**108 passed、1 skipped、2 dependency warnings，60.58 秒**。新增回归验证验证码暂停后第二条不被执行、进程重建仍暂停；Chrome fixture 验证表单/官方下载流程，不能替代 Suno 实测。
- `compileall` 通过；workflow_catalog `--fix` 0 处变更，`--check` 11 组 / 191 源编号连续；skills 5 / adapters 10 检查通过。
- 全库工作流回归仍是 **11 passed、1 skipped、1 failed**：`ai_videos/_shared/xianxia/README.md` 引用未登记的 `STATUS.md`，与本次 Suno 代码无关，未覆盖其他会话文件。

证据：`.audit/adhoc_agents/2026-10-22/suno-v6-live/result.json` 与本集 request_log.md。当前接续步骤以服务 README 和 EP1 `post/audio/suno_prompts.md` 为准，前文“未登录”属于历史状态。原 v6 环境声试听片 SHA256 未变；没有音乐混音版或整集成片新产物。

## Follow-up 002：选项、参考与代理入口（v0.2）

实现三种 mode、14 个 options 字段与上传/URL 参考；GET capabilities、POST plan 与资产接口；JSON CLI、九个 stdio MCP 工具、共用 suno-music skill。旧基础请求默认值维持原幂等指纹，新增组合严格验证，网页控件读回不符或单位不明时停在 Create 前。修复 Styles 误匹配 Exclude styles 的风险，并增加对应 v6 浏览器回归。

- 全套服务与请求审计回归：146 passed、1 skipped、2 dependency warnings，119.40 秒。最终 Duration 秒/分钟/时钟单位核验后，相关 API 与真实 Chrome 表单复验 37 passed，38.66 秒。
- 最后修正参考文件上传的 MIME 类型，并断言浏览器收到 `audio/wav`；高级选项与真实 MCP 调用链复验 2 passed、2 dependency warnings，20.30 秒。最终编译与 scoped diff check 通过；服务已重启加载该修改，健康检查成功，`automation_paused=true` 保持不变。
- MCP 真实 stdio 初始化、九工具发现、结构化返回、跨真实本机 HTTP 的预检/上传/幂等生成/等待/下载/SHA 校验通过；外部 Suno 用隔离 HTTP fixture 替换，没有消费积分。CLI 查询同一任务及错误退出契约通过。
- 实际本机 API 的三个示例 plan 成功，browser_called=false；重启后 automation_paused 仍为 true，原任务未重提。
- Claude 项目 `.mcp.json` 与 Codex MCP 已注册，安装脚本复跑不改既有项。Codex CLI 首次注册把 node_repl 的空 args 列表省略，已只恢复该字段；其余解析配置与私有备份完全一致。当前会话需重启/重新加载才发现新工具。
- Python 编译、skill quick_validate（UTF-8 模式）、6 个共用 skill / 12 个 Claude 入口、workflow_catalog 11 组 / 206 源编号连续全部通过。
- 全库工作流测试仍 11 passed、1 skipped、1 failed：既有 `ai_videos/_shared/xianxia/README.md` 引用未登记的 `STATUS.md`；没有覆盖其他会话文件。

未完成：真实 Suno 验证码解除后逐项校准新模式/上传/Voice/Inspo/更多控件、精确结果归属和官方下载；Browserless 无实际实例。`validation.requires_manual_walkthrough` 仍待做，不能把本地通过写成真实生成下载可用。当前 API 提供能力边界给调用代理，未删除暂停文件、没有新 Create。

本轮主代理直接实现与测试，未宣称独立代码审查。审计：`.audit/adhoc_agents/2026-10-22/suno-options-002/`。

## Follow-up 003–005：文档、UI 与音频默认路由（v0.3）

2026-10-22 22:58 完成验证：

- 完整服务与收费审计回归 **149 passed、1 skipped、2 dependency warnings，125.71 秒**。初次完整回归暴露首批并发请求触发多个 lazy provider 同时初始化 WAL 的争抢；改为 API lifespan 串行初始化数据库相关 query/command 后整套通过，没有删除或降低并发幂等断言。
- 新增四项 UI/OpenAPI/MCP 验证先行通过：真实编译 React 页→实际本机 HTTP→SQLite/worker→隔离 Chrome 网页→SHA 校验试听/下载；上传、Sounds 参数预检、生成、丢失回执后刷新并用原键重试、暂停禁生成均覆盖，外部 Suno 未访问。
- OpenAPI 全部公开操作、生成字段与九 MCP 工具顶层参数有描述；真实 stdio 工具发现、调用及结构化输出通过。两端注册脚本复跑显示已有匹配 entry，不改其他配置。
- React/TypeScript/Vite 生产构建通过；Python compileall、scoped diff check 通过。前端产物挂载 `/ui/`，API `/v1`、`/docs` 不受静态路由遮盖，业务仍鉴权。
- 本机现有任务实际页面检查与截图：1440 px 桌面、390 px 手机。修复真实长标题在手机上的溢出后重新截图；无横向溢出或 pageerror，页面正文无 token，无新 job。截图为主代理视觉验收，不宣称独立审稿。
- 工作流 **11 组 / 223 源** 编号连续；6 个共用 skill / 12 个 Claude 入口与 suno-music frontmatter 通过。管理应用全局工作流 **12 passed、1 skipped**；仅补登记既有仙侠 README 已引用的 STATUS.md，解决之前的覆盖失败，未改资产内容。
- 新音频默认 Suno 写入声音模块、pipeline、独立声音资产/人物资产入口、paid_services、共用 skill、工作流全景和机器 capabilities；MOSS/ACE-Step 等不再自动回退。准确 TTS、声线克隆、源分离目前未支持，明确报告缺口；后期混音仍用本机工具。

本轮真实 Suno 调用为 **0**；原任务和持久验证码暂停保留。真实新控件、官方生成/下载和 Browserless 仍待验收，不能把本地 UI/fixture 通过当真实付费链路可用。审计与截图：`.audit/adhoc_agents/2026-10-22/suno-ui-workflow-003-005/`。

