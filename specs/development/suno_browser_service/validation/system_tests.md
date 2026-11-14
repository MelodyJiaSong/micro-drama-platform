---
worker_id: level-specialist-validation
stage: 5
role: level-specialist
level: system_tests
status: complete
blockers: []
confidence: high
---

# 系统与必要单元检查

只描述测试，不在 stage 5 执行尚未存在的实现。所有测试从调用方契约断言结果，不仅断言内部方法被调用。

| ID / 执行单元 | 设置与动作 | 通过条件 |
|---|---|---|
| SYS-01 / boot_smoke | 启动实际服务进程，使用独立临时 DB；HTTP 调健康、提交与查询 | 无启动异常；健康 200；真实持久任务返回正确状态/ID，消费者能循返回链接获取音频；退出只清理自身 PID |
| SYS-02 / browser_adapter | 本机真实 headless 浏览器打开本地 fixture；通过 HTTP 提交 prompt→等待 DOM 歌曲→官方式菜单下载 | DOM 表单值正确，Create 计数 1；渲染歌曲与菜单结构有效；服务返回的文件字节/大小/哈希正确；测试不向 Suno 发请求 |
| SYS-03 / job_store | 并发同键相同/不同请求；并发不同任务；重启再次请求 | DB 唯一约束或等效事务保证一个 job；同键不同规范化请求冲突；队列串行。第二服务进程不能并行操作同一账号/profile |
| SYS-04 / job_store | 在 submitting 落盘后、点击后未保存 URL、保存 URL 后、第一首文件完成后分别中断重启 | 任何可能已提交分支都不会 Create；原始基线/已知 URL/成功文件保留；安全恢复只补收，completed 不重跑 |
| SYS-05 / browser_adapter | fixture 置入旧歌、列表乱序、无关新歌、手工同 prompt 歌、仅一首/两首/三首结果 | 可确证关联才接收；实际数量来自本次页面证据；歧义暂停，不把最新两首自动当结果 |
| SYS-06 / backend_api | 在实际部署配置上调用全部变更路由，完整走提交→查询→恢复→文件 | 正确鉴权及响应语义；不被静态路由等拦成 405；消费者按真实字段/URL 下载，不仅检查 key 存在 |
| SYS-07 / browser_adapter | 每个外部动作前注入 RequestLog 写入失败；分别模拟动作错误及结果日志失败 | request 未成功落盘则动作数为零；结果日志失败不造成重新 Create；日志关联同 request_id，秘密脱敏 |
| SYS-08 / browser_adapter | 官方导出下载中断/空文件/HTML 错误页；第二首失败；重试补收 | 未完成文件不以成品暴露；有效成品原子落地，有大小/哈希；成功条目不丢失或再次生成 |
| SYS-09 / local_real | 人工登录专用 profile 后，后台真实 Suno 输入→一次生成→官方菜单下载 | 当前页面与实际套餐支持链路；关联歌曲正确，音频可播放；输出 RequestLog/歌曲链接/文件证据；当前 NOT-RUN |
| SYS-10 / browserless_native | 配置真实 Playwright native endpoint 与私有 storage state，重复 SYS-09 黄金链路 | native 连接/会话/官方导出均完成；本地 fixture 不替代此证据；当前 NOT-RUN-NO-ENDPOINT |

SYS-03/04/07 与鉴权/路径解析的分支用小型单元或集成测试即可，不另建重复清单。Windows symlink 权限或 POSIX 信号限制需明确 skip，不能伪报通过；普通崩溃恢复应使用跨平台进程控制执行。无硬性能指标，不增加吞吐量门槛。

## v0.2 增量
运行 `test_options.py`、`test_form.py`、`test_agent_interfaces.py`：覆盖模式/参数/参考、控件读回、Styles 与 Exclude 的区分、上传前审计、权利确认、真实 stdio MCP→HTTP→SQLite/Chrome fixture→下载，以及 CLI 共享同一 job。示例 plan、两端 MCP 注册与重复安装另在本机检查；真实 Suno 和 Browserless 单列未验收。

## v0.3 增量
`npm ci` / `npm run build`；`test_ui.py` 覆盖实际编译页面→同源 HTTP/SQLite/worker→隔离 Chrome fixture→校验下载、上传/模式/预检、回执丢失/刷新/原键重试、暂停和小屏布局。`test_agent_interfaces.py` 同时断言 MCP schema 描述。工作流改动运行 catalog、skills 入口和管理应用 `test_global_workflow.py`；真实本机现有任务截图另存审计，不创建收费任务。

