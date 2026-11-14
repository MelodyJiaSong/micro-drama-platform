# 变更记录

## 2026-10-22 初始实现

- 用户要求将 Suno 网页 prompt → 生成 → 官方下载封装为服务，随后确认本机后台浏览器兼容 Browserless，并授权 Suno 自动 Create/下载例外。
- 用户要求后续自主尽可能完成，不再提问。使用独立项目与 profile，未触碰其他会话制作资产；既有账号未连接，真实联调停在登录页。
- 实现 FastAPI、Bearer 鉴权、幂等任务、SQLite 串行与恢复、Custom 唯一标题关联、MP3/WAV 官方下载、本机与原生 Browserless 连接、Windows 脚本与私有 ACL。
- 默认纯音乐；人声需歌词、自动写词不在本次范围，这是为了以 Custom 唯一标题可靠关联结果作出的实现判断。
- RequestLog 增加独立软件服务归属和 WebSocket URL 脱敏；登记共用服务说明、工作流源与依赖。
- 自动测试与实际后台进程已验证；真实 Suno 生成/下载、远程 Browserless 未通过验收，详见 validation/result.md。

## Follow-up 001 — 2026-10-22 19:53:27
Source: user_input/follow_ups/202610.md - section 001
Summary: 修复 Google 拒绝自动化登录；认证阶段使用普通 Chrome，关闭后再由服务验证会话。

Auto-updated:
- ManualBrowserClient、SessionCommand、Settings.profile_dir、BrowserClient — 普通浏览器登录与共用 profile 路径，认证和自动化分开。
- README、paid_services、final_specs/spec — 更新操作方法与实际边界。
- 两项审计/配置测试；浏览器相关回归共 17 passed。

No conflicts found in: 任务状态机、API 契约、输出文件、EP1 配乐请求和制作资产。

Pending: 普通窗口已实际打开，用户手动登录与后续真实 Suno Create/Download 仍未完成。

Validation note: 工作流编号通过（191 源）；全库工作流回归另有仙侠 STATUS.md 引用未登记，记录为范围外失败。用户手动登录窗口仍打开，服务暂未重启。


### Follow-up 001 执行续记 — 2026-10-22

用户确认“已登录”；实际保存认证态并进入 Pro 账号。新版 v6 的 Advanced / Lyrics editor / Create song 已适配，先等待歌词编辑器，再填写风格与标题；纯音乐清空旧歌词，风格超过页面 maxlength 拒绝。已加入对应离线 Chrome 回归。

EP1 原 M01 恢复后只点一次 Create，后续需要的 M02 也只提交一次；两者未确认歌曲。M02 生成等待期间检测到可见验证码 iframe（20:10:28），不再调用 Suno。自动化改为持久暂停整个队列，API 可查询，重启不继续生成；普通窗口人工处理并登录校验成功后才清除暂停。未知提交仍拒绝空恢复。

真实官方下载尚未验收：账号歌曲页完全加载后有两个 More options 控件。Suno Sounds 页已观察到 effects / loops / one-shots，但 API 未接入，不把本地 MOSS 误称 Suno 环境声。真实证据：`.audit/adhoc_agents/2026-10-22/suno-v6-live/result.json`。此前 Pending 与未登录结论为当时记录，由本段当前结果取代。


## Follow-up 002 — 2026-10-22 21:32:33
Source: user_input/follow_ups/202610.md - section 002
Summary: 扩展 Suno 模式、14 项选项、参考素材、JSON CLI 和九工具 MCP；双代理已注册，真实 Suno 继续保留验证码暂停。

Auto-updated:
- projects/suno_browser_service/ — 共享 schema、选项/引用浏览器适配、资产/API、客户端、CLI/MCP、示例、安装脚本与回归。
- .agents/skills/suno-music/、.agents/skill-aliases.json、.claude/skills/ — 唯一共用技能及生成入口。
- .agents/references/project/paid_services.md、workflow_catalog.json — 当前能力边界与新增源编号。
- interview/qa.md、findings/dossier.md、final_specs/spec.md、validation/* — 新范围、数据约束、验证结果、真实联调缺口。
- user_input/revised_prompt.md、README.md — 用法、恢复与实际状态。

No conflicts found in: 旧服务审计、已有 job / 幂等键、EP1 音乐与环境声产物、其他剧和管理应用源码。没有新 Suno Create、上传或下载调用。

Validation: 服务/审计 146 passed、1 skipped；最终相关回归 37 passed；Python 与技能入口有效；目录 206 源编号连续。全库工作流一项既有仙侠 STATUS 引用登记失败；真实 Suno 功能与 Browserless 未验收。MCP 注册前后核对无其他设置改变，安装复跑通过。详见 validation/result.md 与 .audit/adhoc_agents/2026-10-22/suno-options-002/。

## Follow-up 003–005 — 2026-10-22 22:50:13
Source: user_input/follow_ups/202610.md - sections 003–005
Summary: 完善 API/MCP 文档，提供本机创作工作台，将 Suno 设为所有新音频生成的默认入口。

Auto-updated:
- projects/suno_browser_service/README.md、generation.py、HTTP routes、MCP main — 参数/返回值/副作用与错误恢复的内联说明，完整串联示例。
- apps/ui/、apps/api/app_factory.py、setup/start/Makefile — 同源 React UI、模式/参考/选项、任务查询/恢复、校验试听下载、构建与启动入口。
- API 启动时串行初始化数据库相关 providers — 修复完整回归发现的并发首次请求 WAL 初始化争抢，幂等事务逻辑保留。
- 共用 sound/pipeline/资产/人物资产/paid_services/suno-music、workflow map/capabilities — 新音频默认 Suno，能力缺口不自动换引擎；混音处理继续本机工具。
- workflow_catalog.json — 登记 UI/启动配置与代码源；补登记既有仙侠 README 所引用的 STATUS.md，使引用覆盖检查通过，未改资产文件。
- interview/findings/spec/validation 与 revised_prompt — 文档/UI/默认路由意图、风险边界和验收。

No conflicts found in: 既有任务与提交记录、真实 Suno 暂停、EP1 媒体、其他剧资产内容、其他代理配置。两端 MCP 注册复查均存在，未改写。执行与最终结果见 validation/result.md；本轮无真实 Suno 调用，无独立审稿声明。

## follow-up 006 — 2026-10-24

Summary: v6 Sounds 按真实页面适配（等待面板、data-selected、无标题框按新增片段收取、拒绝时长与超长 prompt）；浏览器默认可见，遇验证码等人在窗口完成后继续同一任务。141 passed / 1 skipped。

Auto-updated:
- libs/common/{settings,generation}.py、libs/infrastructure/clients/{form,suno}__client.py、libs/application/commands/runtime__command.py、libs/application/mappers/job__mapper.py、apps/ui/src/Options.tsx（重建 static）、tests、README.md

## follow-up 007 — 2026-10-24

Summary: 本机浏览器常驻一个窗口，任务间复用，不再每个任务新开 Chrome；验证码处理方式不变。

Auto-updated:
- libs/infrastructure/clients/browser__client.py、libs/common/settings.py、libs/application/commands/runtime__command.py、tests/libs/test_kept_browser.py、README.md、final_specs/spec.md、user_input/revised_prompt.md（补入漏掉的 006 与 007）

## Follow-up 008 — 2026-11-03 19:25:19
Source: user_input/follow_ups/202611.md - section 008
Summary: 常驻窗口连接模式：open-window.ps1 以服务专用 profile 开普通 Chrome（仅 127.0.0.1 调试端口），服务经 CDP 接管；窗口内直接登录无需停服；验证码/登录墙即时提示并在同窗口等人；验证码未解即消失时提早报 uncertain

Auto-updated:
- projects/suno_browser_service（settings / browser / manual_browser / suno / runtime / session / audio_writer / app_factory，apps/window，open-window.ps1，start.ps1，tests），README、suno-music SKILL、sound.md、paid_services.md

验证: pytest projects/suno_browser_service/tests 全通过；2026-11-03 真实账号 Advanced 纯音乐：常驻窗口内自动 Create→认领→官方下载，任务 75c2aee8 完成 2 首 MP3（ffprobe 194.8s/214.8s），fa07658f、ea35c3d5 经 recollect 补收各 2 首
费用: Suno 3 次成功生成（6 首）积分未读回；下载 8 次（含 2 次落入用户 Downloads）

No conflicts found in: （未单独核查）


## Follow-up 009 — 2026-11-04 00:17:46
Source: user_input/follow_ups/202611.md - section 009
Summary: Suno 服务常驻窗口自愈：卡住的标签页自动换新、窗口不节流、端口卡死换口、窗口没了自动重开、未提交的窗口错误自动重排

Auto-updated:
- browser__client: 工作标签页对 beforeunload 选离开、renew_page 换新标签页、连接超时先关卡死标签页（close_hung_tabs）再连一次
- manual_browser__client: 窗口带 --disable-backgrounding-occluded-windows 等三项渲染开关；9333 被卡死进程占着时换下一个空闲端口并记 window_port；end_profile_processes 只结束服务专用 profile 的 Chrome
- runtime__command: 有排队任务而窗口没了时每分钟自动重开；常驻模式下未提交（preparing/downloading）的窗口类错误自动重排最多 3 次；Create 后 240 s 仍未见应答也开始刷新；quota_exhausted 与 challenge 一样暂停自动化
- suno__client: 打开页面超时换标签页重试；cookie 提示按 Reject All（Deny all optional cookies）并用 add_locator_handler 常驻；控件找不到时审计 control_missing；提交后截图失败不再把已提交任务判成 uncertain；Out of Downloads 识别为 quota_exhausted
- form__client: clear_form 确认 Suno 新增的 Clear entire form? 对话框（role=alertdialog）；Simple 模式描述框无标签时用唯一可见 textarea
- README / suno-music SKILL / sound.md / paid_services.md / paihangbang README：记录自愈机制、型号默认、下载月度上限与当晚结果

验证: 实机：ep12/15/16/17/18/19 由服务完成生成→认领→官方下载（ffprobe 60–220 s），ep05/06 同；close_hung_tabs、consent_reject、clear_form、窗口自动重开均在审计里实测出现
费用: Suno Song credits 2500→2370（读回）；下载额度用尽（Out of Downloads，11/25/26 刷新）

No conflicts found in: 各期找图、审片、预览页由各自会话负责，本会话未改


## Follow-up 010 — 2026-11-14 13:00:36
Source: user_input/follow_ups/202611.md - section 010
Summary: target 归属根放宽为 ai_videos 与 edu_videos（RequestLog 已支持 edu_videos/<系列>/<知识点>，suno-music skill 也如此约定）；根目录与不存在路径仍拒绝；测试补 edu_videos 两例

Auto-updated:
- libs/application/commands/job__command.py（target 允许 edu_videos 下已有目录）、libs/common/generation.py（字段说明）、tests/api/test_jobs.py（edu_videos 根与不存在路径仍 422）

验证: pytest projects/suno_browser_service/tests：180 passed 1 skipped；服务已重启 health ok；edu target 实际 create 成功（job 817c57f5…）

No conflicts found in: 只放宽归属根，其余校验不变


## Follow-up 011 — 2026-11-14 14:42:40
Source: user_input/follow_ups/202611.md - section 011
Summary: 实测 Suno 歌曲页自己的菜单按钮改名为 More options for <歌名>；下载先找该按钮（唯一即用），找不到再退回原 More options 逻辑；补回归测试

Auto-updated:
- libs/infrastructure/writers/audio__writer.py（先找 More options for <歌名> 的按钮，唯一即用，否则退回原逻辑）、tests/libs/test_browser.py（新增 titled-label 回归测试）

验证: 实测 CDP 读到歌曲页按钮 aria-label 为 More options for <title>；pytest 181 passed 1 skipped；服务重启后 job 163bf014… 两首 WAV 下载完成并校验 SHA256

No conflicts found in: 只扩展选择器，旧页面结构仍走原分支

