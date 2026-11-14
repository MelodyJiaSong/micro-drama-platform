---
worker_id: level-specialist-validation
stage: 5
role: level-specialist
level: strategy
status: complete
blockers: []
confidence: high
---

# Suno 浏览器服务验证策略

Follow-up 002 增量：检查严格 options/mode 组合、引用 ID/路径/媒体/大小/哈希、旧请求幂等指纹、上传审计失败不动作、表单选项读回与提交前漂移；真实 Chrome 离线页面覆盖 Advanced/Simple/Sounds。MCP 用真实 stdio 会话初始化、发现九工具并跨 HTTP 完成一次 fixture 生成/等待/下载，CLI 复查同一任务；检查 token 不进入输出。安装只追加两端 Suno 项，保留其他配置。真实 Suno 暂停与 Browserless 未实测边界继续保留。

Run: `suno_browser_service-20261022-125046`。依据 [spec](../final_specs/spec.md)；本文件是检查计划，不是运行通过证据。真实 Suno 登录、生成、下载及 Browserless native 均未实测。

## 级别与运行范围

| 级别 | 文件 | 执行单元与重点 |
|---|---|---|
| Acceptance | [acceptance_criteria.md](acceptance_criteria.md) | `backend_api`：HTTP 提交、查询、文件获取与安全恢复 |
| BDD | [bdd_scenarios.md](bdd_scenarios.md) | `browser_adapter`：输入、官方生成/下载、登录失效及归属歧义 |
| System / integration（合并必要单元检查） | [system_tests.md](system_tests.md) | `job_store`、`backend_api`、`browser_adapter`、`boot_smoke`：串行、幂等、崩溃、浏览器 fixture 与进程启动 |
| Security | [security.md](security.md) | 上述各单元：鉴权、路径、秘密、调用前审计、外部 URL |

v0.3 增加自建 UI：须构建 TypeScript/Vite，实际 Chrome 驱动同源静态页与真实 API，检查模式/参考/预检/生成/试听/下载、丢失回执后刷新重试原键、验证码暂停、未授权 API、静态路由不遮挡业务、无 token 落盘、桌面/手机无横向溢出。检查可访问标签、可键盘操作表单与运行脚本错误；保存桌面/手机截图人工看图，不冒充独立审稿。官方网页仍需 `validation.requires_manual_walkthrough` 真实登录/生成/下载验收。

## 证据边界与收尾

- 本机 headless fixture 必须实际启动浏览器，驱动可见表单/菜单并通过真实 HTTP 服务取回文件；纯 mock 不能替代。该结果只证明自动化契约。
- 本机专用 profile 的真实登录与一次 Suno 生成/下载单列联调结果，校准实际 DOM、套餐下载权限、歌曲归属与音频可播放性。未运行时标 `NOT-RUN`，不得声明 Suno 已可用。
- Browserless Playwright native endpoint 单列运行模式与同样的联调用例。当前无实例，可做连接契约检查；标 `NOT-RUN-NO-ENDPOINT`，不得将本机通过写成远程通过，也不宣称支持 CDP。
- 多账号、门户、Remix/克隆、代解验证码、绕过配额不进入验证范围，和 spec 一致；本服务自动 Create 的授权已确认，不重复征询。
- 测试用独立 DB/profile/输出目录；真实登录态与 fixture 隔离。fixture 不联系 Suno，不消耗积分。
- Windows 用当前环境 Python/pip；必要平台限制显式 skip 并解释。只终止本次启动的 PID。

## 判定与审计

每个实际运行级别先记录 `validation.started`（含已读 refs SHA256），再记 `validation.pass` 或 `validation.issue.raised`。修复与复验留 `exec.revision.applied`；不能把本策略完成写成运行验证通过。安全/路径逃逸、启动异常为 critical；验收与黄金链路失败为 blocker；未完成的真实联调必须显式保留。按共用迭代规则处理，不掩盖失败或删除断言。

## Promotion preservation

阶段 1–5 重生成时，使用 `libs/promotions.py::parse_promoted_text` 检查各阶段非空 `promoted.md` 中每条 pin 在新产物中原样存在（忽略空白）。缺失为 critical，错位或无理由 orphan 为 blocker；阶段 6 代码不适用。当前任务未发现 `promoted.md`。
