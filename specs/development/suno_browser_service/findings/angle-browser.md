---
worker_id: researcher-browser
stage: 3
role: researcher
angle: browser
status: complete
blockers: []
confidence: high
---

# 浏览器、登录态与远程文件下载

核查：2026-10-22；仅查 Playwright / Browserless 官方文档，未访问 Suno 账号、连接 Browserless 或发起收费请求。`complete` 指文档研究完成，不表示线上兼容性验证完成。

## 覆盖问题

如何让本机服务保留登录、自动操作页面并可靠收回文件，同时为 Browserless 保留明确的接入边界。用户已选择本机后台浏览器、兼容 Browserless，并明确允许本服务自动 Create 和下载。

## 已查证结论

| 路径 | 官方证据与边界 | 本服务建议 |
|---|---|---|
| 本机持久化浏览器 | `launch_persistent_context(user_data_dir)` 保留会话；一个目录不能由多个浏览器实例同时使用，不能借用日常 Chrome 默认目录。[Playwright BrowserType](https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch-persistent-context) | 独立 profile；同账号单 worker；人工首次登录后后台复用。 |
| Browserless 原生 Playwright | `/chromium/playwright` 对应 `chromium.connect()`；普通 `/`、`/chromium` 为 CDP。[连接路径](https://docs.browserless.io/baas/connection-url-patterns) 原生协议双方须匹配 Playwright 主、次版本。[Playwright connect](https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect) | 下载优先走该方式；协议类型明确配置，不能将任意 WS 地址都传给同一连接方法。 |
| Browserless 原生协议下载 | 官方示例明确使用 `connect()` 后 `download.saveAs()`，将文件保存到脚本所在机器。[文件传输](https://docs.browserless.io/baas/features/file-transfers#playwright) | Python 对应 `save_as()`；此为官方支持证据，仍需接入实例实测。 |
| Browserless CDP 下载 | 官方扩展 `Browserless.setDownloadEnabled` + `Browserless.fileDownloaded` 回传 base64；默认关闭，每个会话启用，传输计入流量。[文件传输](https://docs.browserless.io/baas/features/file-transfers#downloading-files) | 若支持 CDP，显式实现该传输路径；先查实例是否支持扩展，不能假定所有自托管版本都有。 |
| 普通远程 CDP | Playwright 明确其保真度低于原生协议；本次查到的官方示例**不足以证明任意远程 CDP 的 `save_as()` 都能收回文件**。[Playwright CDP](https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp) | 不把“连接成功”当“下载可用”；没有文件传输能力时返回明确不支持，避免生成后才发现取不回。 |

下载应先注册 `expect_download()` 再点击官方菜单，等 `save_as()` 完成后才能关闭上下文。`download.path()` 在远程连接会抛错；上下文关闭会删除它管理的下载文件，因此不能把临时路径当结果交付。[Playwright Download](https://playwright.dev/python/docs/api/class-download)

登录态可以通过 `storage_state()` 导出，并在 `new_context(storage_state=...)` 恢复；其中含敏感 cookie 等，不能进 Git 或响应日志。`sessionStorage` 不在自动持久化 API 中，不能承诺状态文件覆盖任何站点的全部登录机制。[Playwright Authentication](https://playwright.dev/python/docs/auth) 如登录依赖 IndexedDB，导出需启用 `indexed_db=True`（自 v1.51）；是否适用于 Suno 尚未实测。[BrowserContext](https://playwright.dev/python/docs/api/class-browsercontext#browser-context-storage-state)

复用已有 Browserless 默认上下文和创建新上下文是不同操作：新上下文不会自动继承原上下文 cookies / 启动配置。[Browserless Playwright 配置](https://docs.browserless.io/baas/advanced-configurations/playwright-customizations#default-context) Browserless 的 Session API 可保留跨重启状态；文档不推荐 Playwright 使用依赖 `disconnect()` 的短期 Standard Sessions。[会话管理](https://docs.browserless.io/baas/session-management) 这些云端能力可以后续选配，不应成为本机模式的依赖。

## 规格建议（工程判断）

- v1 默认 `local`；可选 `playwright_ws`。若保留 `browserless_cdp`，必须带独立的文件传输实现与能力检查，不承诺通用远程 CDP 下载。
- 本机 `login` 使用同一独立 profile 的可见窗口；后台 worker 启动前独占该目录。远程模式使用明确的 storage-state 文件或已登录默认上下文，二者不得静默混用。
- 结果以服务端自行分配的文件名保存，不直接相信网站建议文件名；下载完成后核对文件大小、音频格式、SHA256，再把任务标完成。下载失败只重试下载，不能重按 Create。
- 原生协议接入前记录客户端版本和服务端兼容版本。端点日志隐藏 token；异常截图和状态文件不直接暴露给 API 调用方。
- 无论模式，付费提交前 RequestLog 必须成功落盘；页面导航/查询、下载、错误按仓库契约留痕。本研究无这类调用。

## 待实测 / 未研究

1. 本机：人工登录后关闭、后台重启仍保持 Suno 登录；官方 MP3 / WAV 菜单能产生完整下载；验证码/重新登录进入待人工状态。
2. 原生远程：使用匹配版本的实际 Browserless，下载测试附件并确认文件存在于服务主机；再验证 Suno 登录与官方菜单。
3. CDP：实际实例扩展支持情况、事件与页面/文件关联、大文件完整性、超时及断线恢复。普通远程 CDP 的 `save_as()` 未验证。
4. Suno 当前 DOM、下载权限、WAV 异步流程、套餐条款不属于本角度；不能由浏览器能力文档推断。所有来源均为文档支持证据，本研究没有运行浏览器兼容性测试。
