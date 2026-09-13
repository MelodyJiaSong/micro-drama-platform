---
worker_id: researcher-03-browser-automation-reliability
stage: 3
role: researcher
angle: browser-automation-reliability
status: complete
blockers: []
confidence: medium
---

# Angle：browser-automation-reliability

## 1. 本 angle 覆盖范围

本 angle 研究一个**长期驻留在本机、有头（headful）、使用 persistent context 的 Playwright service** 在日常驱动复杂 SPA 时靠哪些运维模式保持可靠，以及 spec 必须写明的失败模式。具体包括：profile 生命周期、上传、富文本编辑器与 @ 提及、被动网络观察、下载、页面改版后的韧性、并发模型、节奏控制。

标注约定：**【文档】/【issue】/【博客】** 表示有来源的事实，**【观点】** 表示本研究者的判断。本研究**没有访问**即梦站点，即梦的编辑器实现、接口形态、DOM 结构一律未知。反检测类手段（stealth、指纹伪装、验证码求解、改 webdriver 标志）**不在本范围内**，本文不作讨论。

仓库原型 `tools/kling_autopilot/kling_session.py` 离生产可用还差这些：
- 使用 sync API，而且没有线程模型；
- 每次运行都新起一个浏览器、用完就关，没有常驻；
- 用 `fill("")` 加逐字 `type` 输入，填完不校验；
- 用 DOM 标志 `result_ready` 同步等待结果，没有网络观察；
- 下载依赖 `expect_download` 抓取的临时文件；
- 没有 browser close / crash 监听，没有失败时的现场留存，没有幂等保护，selector 仍是占位。

## 2. 主要发现

### A. Persistent context 的生命周期（Windows）
- 【文档】同一个 user data dir 不能同时被多个浏览器实例使用。把 `user_data_dir` 指向 Chrome 日常使用的 "User Data" 目录已**不再受支持**，可能出现页面加载不出或浏览器直接退出。官方建议另建一个空目录专门给自动化用。[BrowserType](https://playwright.dev/python/docs/api/class-browsertype)
- 【来源】Windows 版 Chrome 通过 user data dir 下的 `lockfile`（ProcessSingleton 机制）实现单实例互斥。浏览器没有正常退出时，锁可能残留，于是出现 "profile in use"。[chromium-reviews](https://groups.google.com/a/chromium.org/g/chromium-reviews/c/kqQqGxbTqHc)
- 【issue】macOS 上有报告：headless 模式的 persistent context 退出后遗留 `SingletonLock`，profile 数据库损坏，Chrome 提示 "Something went wrong when opening your profile"。[#35466](https://github.com/microsoft/playwright/issues/35466) Windows 上**没有找到**同级别的公开报告，但"没有干净关闭 → 锁残留或 profile 损坏"这一类故障真实存在。
- 【issue】用户手动关掉最后一个 tab 或窗口时，行为不一致：
  - headed + persistent 模式下，之后再调 `context.close()` 会抛 `TargetClosedError`。[py#2753](https://github.com/microsoft/playwright-python/issues/2753)
  - Windows 上关闭全部页面后再 `new_page`，报 `Target.createTarget: Failed to open a new tab`，而且没有触发 context 的 `close` 事件。[#29726](https://github.com/microsoft/playwright/issues/29726)
- 【文档】`channel="chrome"` 使用本机安装的品牌版 Chrome。Playwright 自带的 Chromium 缺少部分专有编解码器，因为授权原因没有打包。[browsers](https://playwright.dev/python/docs/browsers) 但 Playwright 不负责安装或更新品牌版 Chrome，它会自行升级，逐渐偏离 Playwright 当初测试的版本（报告中是 1.52 对应 Chrome 135，实际装的是 139）。[#37022](https://github.com/microsoft/playwright/issues/37022)
- 【文档】Playwright 默认给 Chromium 加 `--disable-background-timer-throttling`、`--disable-backgrounding-occluded-windows`、`--disable-renderer-backgrounding` 三个参数，所以窗口被遮挡或最小化时页面计时器不会被节流。[chromiumSwitches.ts](https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/chromium/chromiumSwitches.ts) 【观点】不要用 `ignore_default_args` 把它们去掉，否则页面在后台轮询可能变慢。
- 【文档】`handle_sigint` / `handle_sigterm` 默认为 true：service 收到 Ctrl-C 就会关闭浏览器。[BrowserType](https://playwright.dev/python/docs/api/class-browsertype)

### B. 上传
- 【文档】`set_input_files` 直接作用于 `<input type=file>`。如果 input 是动态创建的，用 `expect_file_chooser` 包住触发上传的那次点击。[input](https://playwright.dev/python/docs/input)
- 【issue】常被引用的 50MB 上限只针对"浏览器与 Playwright server 不在同一台机器"的远程连接场景，本地 launch 不受限。[#34149](https://github.com/microsoft/playwright/issues/34149)
- 【观点】`set_input_files` 返回只代表文件已交给 input，**不代表上传完成**。必须等页面自己给出完成信号（缩略图出现、进度条消失、上传接口返回），并给上传单独配置超时。

### C. 富文本编辑器与 @ 提及
- 【文档】几种输入方式在事件层面的区别：
  - `fill` 支持 contenteditable，但只触发 `input` 事件；
  - `press_sequentially` 逐字发出完整键盘事件；
  - `keyboard.insert_text` 只派发 `input`，不发 keydown / keyup。
  - 非 US 键盘字符（中文就属于这类）用 `keyboard.type` 输入时，**也只发 `input` 事件**。

  所以对中文来说，逐字 type 和 insert_text 在事件上几乎没有差别，逐字输入 5000 字只是更慢。[input](https://playwright.dev/python/docs/input)、[keyboard](https://playwright.dev/python/docs/api/class-keyboard)
- 【issue】contenteditable 失焦后再次 `fill`，文本会**追加**而不是替换（1.56 版本报告，已有关联 PR）。[#39492](https://github.com/microsoft/playwright/issues/39492)
- 【博客】ProseMirror、Lexical 这类编辑器以自己的内部状态为准，直接改 DOM 或 innerHTML 会被丢弃：
  - ProseMirror 实测：`fill` 失败，逐字 type 可用但慢，`execCommand('insertText')` 可用。[dev.to ProseMirror](https://dev.to/vesper_finch/how-i-defeated-prosemirror-the-only-way-to-programmatically-insert-text-into-rich-text-editors-1208)
  - Lexical 会过滤不可信（non-trusted）的事件；Playwright 的键盘输入走 Chromium 自己的输入管线，属于可信事件。[dev.to Lexical](https://dev.to/snake_sun/why-reddit-indiehackers-and-twitter-lexical-editors-block-programmatic-input-3d76)（该文中关于绕过特定站点反机器人的部分已排除，不采用。）
  - MDN：`execCommand` 已弃用，但 `insertText` 能保留撤销栈，目前仍有正当用途。[MDN](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand)
- 【文档】走剪贴板粘贴需要 `grant_permissions(["clipboard-read","clipboard-write"])`。[BrowserContext](https://playwright.dev/python/docs/api/class-browsercontext) 【观点】headful 机器上系统剪贴板和用户共用，存在竞态。
- 【观点】换行行为（Enter 是否新起段落、Shift+Enter 是否软换行）没有文档说明，只能实测。@ 提及节点只能走真实交互：输入 `@` → 等候选浮层出现 → 点击选项。

### D. 被动网络观察
- 【文档】可用的钩子是 `page.on("response")` 和 `expect_response`（支持 glob、regex、predicate 匹配）。[network](https://playwright.dev/python/docs/network) Service Worker 相关：
  - Service Worker 自己发起的请求只在 **BrowserContext 级**事件里报告；
  - 由 Service Worker 应答的页面请求，其响应 `from_service_worker=True`；
  - 设置 `service_workers="block"` 可以屏蔽 Service Worker。

  [service-workers](https://playwright.dev/python/docs/service-workers)
- 【issue】在 response 回调里读取 body 经常报 `Network.getResponseBody: No resource with given identifier found`。常见触发场景：页面已导航、redirect、跨进程 iframe（OOPIF）、worker 发出的请求。[#26388](https://github.com/microsoft/playwright/issues/26388)、[py#1143](https://github.com/microsoft/playwright-python/issues/1143)、[#20809](https://github.com/microsoft/playwright/issues/20809)、[#35678](https://github.com/microsoft/playwright/issues/35678) 结论：body 要在回调里**立刻读取**并做容错，不能假设过一会儿还读得到。
- 【观点】service 重启后对账的做法：不重放提交，而是打开历史或资产列表页，让页面自己发出列表请求，被动截获后再和本地 job 匹配。

### E. 下载
- 【文档】下载文件默认放在临时目录，context 关闭时删除。persistent context 可以设置 `downloads_path`；`accept_downloads` 默认为 true；需要 `save_as` 才能保留。[downloads](https://playwright.dev/python/docs/downloads)
- 【文档】`context.request` 与浏览器**共用同一个 cookie jar**。它的响应整体放在内存里，默认超时 30s。[APIRequestContext](https://playwright.dev/python/docs/api/class-apirequestcontext) 【观点】取大视频文件时要调大超时，并评估内存占用。

### F. 应对页面改版
- 【文档】locator 优先用 `get_by_role`、文本或 test id，避免依赖 DOM 结构的 CSS 选择器；可以用 codegen 帮忙挑 locator。[best-practices](https://playwright.dev/docs/best-practices)
- 【文档】trace 记录每一步的 DOM snapshot、截图胶片和网络请求。同一个 context 内可以用 `start_chunk` / `stop_chunk` 分段录制多份 trace。[trace-viewer](https://playwright.dev/python/docs/trace-viewer)、[Tracing](https://playwright.dev/python/docs/api/class-tracing)

### G. 并发
- 【文档】Playwright **不是线程安全的**，每个线程需要自己的实例。在正运行的 asyncio loop 里调用 sync API 会直接报错。取消一个正在执行 Playwright 调用的 task 属于未定义行为，需要时用 `asyncio.shield` 保护。Windows 上必须使用 ProactorEventLoop。[library](https://playwright.dev/python/docs/library)、[py#462](https://github.com/microsoft/playwright-python/issues/462)
- 【issue】跨线程使用 sync API 会报 `greenlet.error: cannot switch to a different thread`。[py#1422](https://github.com/microsoft/playwright-python/issues/1422)

### H. 节奏
- 【文档】`slow_mo` 只是给每个操作加统一的延迟，用途是"方便看清发生了什么"，不是限速手段。[BrowserType](https://playwright.dev/python/docs/api/class-browsertype)
- 【观点】节奏控制的目标是**控制成本 + 出于礼节降低风控风险**，不是伪装。

## 3. 对 spec 的影响（均为可落地的【观点】，事实依据见 §2）

1. **Profile。** 使用专用目录，禁止指向日常 Chrome 的 User Data。启动失败要分类为 `profile_in_use`、`browser_missing`、`launch_timeout`，**不要自动删除锁文件**，报出来让人确认。启动时把 `browser.version` 写入 DB 和每次 canary 的记录。
2. **浏览器通道可配置**（`chrome` / `chromium`）。默认用 `chrome`，原因是真实品牌浏览器、编解码器齐全。spec 要明确承认 Chrome 自动升级带来的漂移风险。
3. **常驻单 context + 单一"工作页"**，所有 UI 动作串行执行。监听 context `close`、page `close`、page `crash`：一旦触发，状态置为 `browser_lost`，暂停队列，然后重建 context → 做登录检查 → 对账。**不依赖"关掉最后一个 tab"会发生什么。**
4. **登录失效检测**写进 canary（检查未登录标志、是否被重定向到登录页）。失效则置 `login_required`，暂停队列并弹 Windows toast。
5. **上传完成判定：** 页面可见的完成态 +（能观察到时）上传接口响应 + 该文件出现在 @ 候选列表中。上传超时单独配置。
6. **编辑器填充做成可切换策略**：type、insert_text、execCommand、paste 四种，由 canary 实测选定。填充后**必须校验**：规范化后的纯文本等于期望，mention 节点数量和名称逐一匹配。不一致就置 `fill_mismatch`，清空重来或暂停，**绝不提交**。
7. **提交幂等：** 点击"生成"之前先落库 `submitting` 状态和幂等键（例如 prompt 与参数的 hash）。如果点击后崩溃，重启时置为 `submit_unknown`，只做对账、不重复提交；同一个幂等键默认拒绝再次提交。
8. **网络观察：**
   - 在 context 级挂 `response` 监听，只读不改，不使用 `route`；
   - 响应解析做成带版本号、有 schema 校验的纯函数；
   - body 读取失败要计数，解析失败算作 `page_contract_broken`，而不是作业失败。
9. **下载：** 固定 `downloads_path`。主路径是用 `context.request` GET 被动观察到的媒体 URL（加大超时），页面下载按钮作为后备。流程为：先写临时文件 → 校验大小、sha256、能被 ffprobe 读 → 原子 rename → 写 sidecar json（含 job_id、source_url、sha256、size、browser.version）。
10. **失败现场留存：** 截图 + `page.content()` DOM 快照 + 该 job 的 trace chunk。**只在失败时保留**，路径写入 DB。
11. **并发模型：**
    - 在 uvicorn 内用 async API；由单个 browser actor task 从命令队列串行消费。另一种方案是 sync API 独占一个专用线程，HTTP 层通过队列与它通信。两种任选其一。
    - 取消在动作之间的检查点生效，**不去 cancel 正在执行的 Playwright task**。
    - "并发上限"只限制远端同时渲染中的 job 数，UI 动作始终全局串行。
12. **节奏：** 可配置两次提交之间的最小间隔、每小时和每日提交上限、出现异常后的冷却时间。失败后**不自动重试提交**。
13. **Canary 作为批次前置关卡：** 检查登录态、编辑器、上传入口、参数控件、生成按钮是否都在，历史列表接口能否截获。全程不点"生成"。任何一项失败就暂停。所有 selector 集中放在一份 registry 文件里，canary 就是对这份 registry 的逐项自检。

## 4. 待确认问题

- 即梦的编辑器是哪种实现（Slate、Lexical、ProseMirror 还是自研）？@ 节点的 DOM 结构是什么？需要用户在自己的登录态下 F12 确认，适合在 stage 6 做一次探针。
- 生成进度是 HTTP 轮询、WebSocket 还是 SSE？如果是 WebSocket，就需要 `page.on("websocket")` 方案，本次**没有研究**。
- 站点有没有 Service Worker？这决定监听应该挂在 page 级还是 context 级。
- 结果媒体 URL 是否带签名、有效期多长？直接取 URL 得到的文件与点下载按钮得到的是否是同一版本（水印、清晰度）？
- 上传是否直传对象存储、是否分片？页面的完成信号具体是什么？
- 品牌版 Chrome 自动升级会不会中断长驻 service？是否要改为固定版本（例如 Chrome for Testing）？本次没有找到权威结论。
- Windows 上非正常关闭导致 profile 损坏的实际发生频率：**没有找到** Windows 专项报告，建议定期备份 profile 作为兜底。
