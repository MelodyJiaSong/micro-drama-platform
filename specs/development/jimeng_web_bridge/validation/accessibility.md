---
worker_id: level-specialist-06-accessibility
stage: 5
role: level-specialist
level: accessibility
status: complete
blockers: []
confidence: high
---

# Accessibility validation — jimeng_web_bridge 本地管理 UI

Level = accessibility。基准 WCAG 2.2 AA。依据：spec §3 F2–F7、§5.12 FR-54 / FR-55、`agent_refs/project/development.md` §7、`agent_refs/validation/general.md` §4 与标准严重度表、`agent_refs/validation/development.md` §7 / §8 / §9。

## 0. 范围与判定

**目标。** 被测对象是 `projects/jimeng_web_bridge/apps/ui/`（Vite + React + TS，中文界面），由 `make run` 在 FastAPI 同进程里提供，地址 `127.0.0.1:8790`。spec §6 只允许这一种运行模式，所以 a11y e2e 只有一个 Playwright profile，跑在构建产物上，不跑 Vite dev server。

**页面代号。** 路由路径以 stage 6 实现为准，下文用 P1–P7 指代。

| 代号 | 页面 | 主要 FR | 高风险动作 |
|---|---|---|---|
| P1 | 会话 | FR-54.1、FR-26/27/40 | 运行 canary、打开浏览器窗口（均只读） |
| P2 | 剧 config | FR-54.2、FR-3/4 | 保存（写进 git 的文件，可能 409） |
| P3 | 批次确认（含 FR-49 主体创建确认） | FR-54.3、FR-13/14 | **确认并开始 = 花积分**；创建主体 = 写即梦 |
| P4 | 队列看板 | FR-54.4、FR-17/21/22/23、F7 | **提交后取消不退积分**、分步提交、恢复 |
| P5 | 历史与积分 | FR-54.5、FR-43/46 | **选定 = 升格定稿 + 归档旧文件** |
| P6 | 主体对账 | FR-54.6、FR-47/48/49 | 创建（跳转 P3 确认） |
| P7 | 全局设置 | FR-54.7、FR-1 | 保存；`confirm.allow_http_auto` 开关 |

**严重度。** 按 general.md 标准表：`mandatory` 失败 = `blocker`（3 轮修订上限），`recommended` 缺口 = `warning`。两个例外：
- A11Y-VIS-4（chrome 暗色覆盖）的 blocker 直接来自 development.md §7；
- A11Y-ERR-1 如果表现为深链接白屏，按 development.md 严重度表升为 `critical`。

**力度。** 单用户、本机工具，不做移动端、触屏、多语言。但凡是花积分、写即梦、移动文件的动作，「键盘可达、防误触、执行前能感知后果」一律 mandatory。

**不在本 level。** 即梦网站本身与 Fake 即梦站点 fixture（测试基础设施）；Windows toast 的系统层可达性（FR-56，OS 负责）；MCP 与 HTTP API；3.3.8 Accessible Authentication（登录发生在即梦站点，本 UI 无认证表单，N/A）。

## 1. 验证手段（所有 check 共用）

- **V-AXE**：`@axe-core/playwright`，tags `wcag2a`、`wcag2aa`、`wcag21a`、`wcag21aa`、`wcag22aa`。
  - 扫描点：P1–P7 × {加载成功、加载失败、空数据}；每个对话框打开态；队列级暂停横幅出现态；P2 的 needs_confirmation 态与 409 态。
  - WCAG tag 违规的严重度跟随所挂 check。另显式启用 best-practice 规则 `landmark-one-main`、`page-has-heading-one`、`region`（挂 DOC-3 / DOC-4，按 mandatory）；其余 best-practice 违规记 warning。
  - 误报只能在 issue 记录里逐条写理由豁免，不得全局关闭规则。
- **V-LINT**：`eslint-plugin-jsx-a11y` recommended 规则集接入 `make test`，静态抓 `div onClick`、缺 label、正 tabindex。
- **V-KB**：纯键盘流程脚本。被测流程内只用 `keyboard.press` / `keyboard.type`，禁止 `click()` / `fill()`；结果用请求记录器（`page.on('request')`）和读回 API 断言。
- **V-LIVE**：`addInitScript` 注入 MutationObserver，带时间戳记录 `[aria-live]`、`[role=status]`、`[role=alert]` 的文本变化。
- **V-STATE**：状态矩阵 fixture，离线、零积分（Fake 即梦站点 + fake `dreamina` + 预置 SQLite）。需覆盖：
  - 批次含 ok / warning / error 条目与五种参考 kind（其中一项文件缺失）；
  - 每种 `JobState`；7 种队列级 + 6 种作业级暂停原因，各带截图；
  - config 含 needs_confirmation 项与「已有 config」逐键 diff；reconcile 三态；候选网格含已有定稿；
  - 会话 `ready` / `login_required` / `page_contract_broken` / `cli_login_required`。
- **V-DECOLOR**：注入 CSS 把所有颜色统一成灰阶，断言状态信息仍能以文字读到。
- **V-MW**：人工走查（§4），NVDA + Chrome（本仓库标准主机为 Windows 11）。

**事件。** runtime 以 `levels: ["accessibility"]` 发 `validation.started`；每个失败 check 发一条 `validation.issue.raised`（`issue_id` = check 编号）；自动化 mandatory 全过后发 `validation.requires_manual_walkthrough`。

## 2. Mandatory checks（失败 → `blocker`）

### 2.1 文档结构 A11Y-DOC

- **A11Y-DOC-1 页面语言** — P1–P7 · 3.1.1 (A) · `mandatory`
  - 要求：构建产物 `index.html` 为 `<html lang="zh-CN">`。
  - 验证：V-AXE `html-has-lang` / `html-lang-valid`，并断言值精确等于 `zh-CN`。
- **A11Y-DOC-2 每个路由有唯一标题** — P1–P7 · 2.4.2 (A) · `mandatory`
  - 要求：客户端路由切换后 `document.title` 随之更新，含页面名，7 页互不相同；P3 标题含 batch 标识，P2 含剧名。*(judgment call — 格式由实现定，只断言「非空 + 含页面名 + 唯一」)*
  - 验证：Playwright 逐路由断言，导航栏切换与直接深链接两种进入方式都测。
- **A11Y-DOC-3 地标** — P1–P7 · 1.3.1 (A)、2.4.1 (A) · `mandatory`
  - 要求：恰好一个 `<main>`；主导航 `<nav aria-label="主导航">` 含 7 项，当前页链接带 `aria-current="page"`；全局暂停横幅位于某个地标内。
  - 验证：V-AXE `landmark-one-main`、`region` + 脚本断言 `aria-current`。
- **A11Y-DOC-4 标题层级** — P1–P7 · 1.3.1、2.4.6 (AA) · `mandatory`
  - 要求：每页恰好一个 `h1`（页面名）。页内分区用 `h2`：P4 每个状态列、P2 每个 TOML 表（`[drama]` / `[entities]` / …）、P3 每个条目、P1 web 与 CLI 两块。
  - 验证：V-AXE `page-has-heading-one` + 脚本断言 `h1` 数量与文字。
- **A11Y-DOC-5 路由切换后的焦点** — P1–P7 · 2.4.3 (A) · `mandatory`
  - 要求：切换后焦点移到新页 `h1`（`tabindex="-1"`）或 `<main>`，不留在已卸载元素或 `body`。
  - 验证：V-KB，导航栏按 Enter 切换后断言 `document.activeElement`。

### 2.2 键盘 A11Y-KB

- **A11Y-KB-1 全部控件可键盘操作** — P1–P7 · 2.1.1 (A)、1.3.2 (A)、4.1.2 (A) · `mandatory`
  - 要求：交互控件是原生 `button` / `a` / `input` / `select`，或带 role + `tabindex="0"` + 键盘处理；无正 tabindex；Tab 顺序与视觉顺序一致。
  - 验证：V-LINT；V-AXE `nested-interactive`、`button-name`、`scrollable-region-focusable`；KB-2 流程脚本。
- **A11Y-KB-2 每条主流程能纯键盘走完** — 2.1.1 · `mandatory`（每条一个 V-KB 用例）
  - F2（P2）：展开系列 → 选中 hy3 → 「生成默认 config」→ 跳到首个需确认项并修改 → 保存成功。
  - F3（P3）：从确认页 URL 进入 → Tab 逐条浏览 → 聚焦「确认并开始」→ Space → batch 已确认。
  - F4（P4）：定位暂停 job → 打开截图 → 关闭 → 「恢复」；对 `generating` 的 job「取消」→ 二次确认 → `cancelled`。
  - F5（P5）：筛选到某 key → 方向键选候选 → 「选定」→ 归档确认 → 定稿更新。
  - F6（P6）：定位 `missing_on_platform` 行 → 「创建」→ 确认页编辑描述 → 确认。
  - F7（P4）：分步 上传 → 填写 → 预演 → 提交（带二次确认）。P1：「运行 canary」「打开浏览器窗口」。P7：修改并保存。
- **A11Y-KB-3 没有键盘陷阱** — P2、P4、P5 · 2.1.2 (A) · `mandatory`
  - 要求：原文 TOML 视图若是截获 Tab 缩进的代码编辑器，必须能 Esc 后 Tab 离开，并在旁边文字说明；截图大图、对话框、下拉框都能 Esc 退出。
  - 验证：V-KB，在每个复合控件内连按 Tab 20 次，断言焦点最终离开。
- **A11Y-KB-4 高风险动作不绑快捷键** — P3–P6 · 2.1.4 (A) · `mandatory`
  - 要求：确认、取消、选定、分步提交、创建主体**不得**绑定任何快捷键；其他单字符快捷键（如 `r` 刷新）若实现，须可关闭或需修饰键。
  - 验证：代码审查；V-KB 在 P3 / P4 / P5 焦点位于 `h1` 时依次按全部字母与数字键，请求记录器断言零写请求。
- **A11Y-KB-5 排序不只能拖拽** — P2 · 2.5.7 (AA) · `mandatory`
  - 要求：`references.rules` 自上而下取第一条匹配（FR-8），顺序就是语义。重排须有「上移 / 下移」按钮，名称含序号与 `label_glob`（如「上移规则 3（`*锚点`）」）；移动后焦点跟随该行并礼貌播报新位置。只能拖拽 = fail。
  - 验证：V-KB 重排后保存，读回 config 断言顺序。
- **A11Y-KB-6 目标尺寸** — P1–P7 · 2.5.8 (AA) · `mandatory`
  - 要求：图标按钮（打开截图、上移 / 下移、删除 override 行、候选选择）≥ 24×24 CSS px，或间距满足该条例外。
  - 验证：V-AXE `target-size`。

### 2.3 花积分 / 写即梦 / 移动文件的闸门 A11Y-GATE

- **A11Y-GATE-1 确认不能被隐式提交触发** — P3（含主体创建确认）· 3.3.4 (AA)、3.2.2 (A) · `mandatory`
  - 要求：「确认并开始」「创建主体」是 `type="button"`，不是 `<form>` 的 submit；在确认页任何文本输入框（如 FR-49 可编辑描述）里按 Enter 都不产生确认请求。
  - 验证：V-KB 逐个聚焦文本输入框按 Enter；请求记录器断言 `POST /api/batches/{id}/confirm` 与 `POST /api/entities` 均为 0。
- **A11Y-GATE-2 进入页面不预聚焦确认按钮** — P3 · 3.2.1 (A)、3.3.4 · `mandatory`
  - 要求：加载后焦点在 `h1`；确认按钮无 `autoFocus`。用户点开 Claude 给的链接后连按 Enter / Space 不会确认。
  - 验证：V-KB 加载后不按 Tab，Enter、Space 各连按 3 次，断言确认请求为 0。
- **A11Y-GATE-3 按确认之前能感知后果** — P3 · 1.3.1、3.3.4、2.5.3 (A) · `mandatory`
  - 要求：「确认并开始」经 `aria-describedby` 关联合计预计积分（静态、页面、`as_of`）、条目数、警告数；另设 `aria-label` 时须以可见文字「确认并开始」开头（2.5.3）；每条 warning 以文字列出，合计区有「N 条警告」链接跳到首条。
  - 验证：V-AXE；断言 accessible description 含合计积分，且与 `GET /api/batches/{id}` 一致（与 spec §9 第 12 条共用断言数据）。
- **A11Y-GATE-4 不能确认的原因以文字暴露** — P3 · 4.1.2、3.3.1 (A) · `mandatory`
  - 要求：有 error 条目时，确认按钮用 `aria-disabled="true"`（保持可聚焦）+ `aria-describedby` 指向「N 条存在错误，需修正后重新预检」；error 条目带文字「错误」+ 图标 + 错误信息（含应填 config 键）。只用原生 `disabled`（原因不可达）或只靠红色 = fail。
  - 验证：V-STATE 错误批次；V-KB 聚焦后断言 description；V-DECOLOR。
- **A11Y-GATE-5 只触发一次，结果有播报** — P3 · 4.1.3 (AA) · `mandatory`
  - 要求：激活后立即进入忙态；按住 Enter 或连按两次 Space 只产生 1 个确认请求；成功以 `role="status"` 播报「已确认，N 条进入队列」并给出前往队列看板的链接。token 单次有效（FR-14），UI 不得把第二次被拒播报成错误。
  - 验证：V-KB + V-LIVE。
- **A11Y-GATE-6 token 过期后可恢复** — P3 · 2.2.1 (A)、3.3.7 (A) · `mandatory`
  - 要求：token 30 min 过期（FR-13）。页面以文字显示过期绝对时刻（倒计时若有，不进 live region）；过期后 `role="alert"` 播报，确认按钮进入 GATE-4 式禁用，并提供键盘可达的「重新预检」，重新预检不要求重新输入已编辑的主体描述。
  - 验证：V-STATE 注入过期 token 或伪造时钟。
- **A11Y-GATE-7 后果写进可访问名称** — P4、P5、P6 · 2.4.6、4.1.2 · `mandatory`
  - 要求：P4 取消按钮名称含 job 身份并随状态写明后果——`submitting` 之前「取消 shot02（未提交，不花积分）」，之后「取消 shot02（已提交，积分不退还）」；同页不得有多个同名「取消」「恢复」「分步：提交」「创建」；P5「选定」名称含 key 与候选序号。
  - 验证：脚本收集同页全部 button 的 accessible name 断言唯一；V-AXE。

### 2.4 对话框 A11Y-DLG

适用：提交后取消（FR-22）、分步提交（F7，按 FR-55 走二次确认）、选定并归档（FR-43 `image_on_existing=archive`）、409 冲突（FR-4）、截图大图查看。

- **A11Y-DLG-1 语义** — P2、P4、P5 · 4.1.2、1.3.1 · `mandatory`
  - 要求：前三种高风险确认用 `role="alertdialog"`，409 与截图用 `role="dialog"`；带 `aria-modal="true"`、`aria-labelledby`（标题）、`aria-describedby`（后果文字，如「该任务已提交，取消后积分不会退还」「shot02 将立即提交，预计 X 积分」「现有 `c1-1_….png` 将移到 `_deleted/…`」）。原生 `<dialog>` + `showModal()` 可接受。
  - 验证：V-AXE `aria-dialog-name` + 断言 description 文字。
- **A11Y-DLG-2 初始焦点在安全动作上** — 同上 · 3.3.4 · `mandatory`
  - 要求：打开后焦点落在「返回」/「不取消」或标题上，绝不落在执行按钮；打开后立即按 Enter 得到安全结果。
  - 验证：V-KB 打开后立即 Enter，断言零写请求。
- **A11Y-DLG-3 焦点圈定与 Esc** — 同上 · 2.4.3、2.1.2 · `mandatory`
  - 要求：Tab / Shift+Tab 在对话框内循环；背景 `inert`（或等效），不可聚焦；Esc 等同安全动作。
  - 验证：V-KB 连按 Tab 30 次断言焦点始终在 dialog 内；Esc 后零写请求。
- **A11Y-DLG-4 关闭后焦点归还（含触发元素已消失）** — P4、P5 · 2.4.3 · `mandatory`
  - 要求：关闭后焦点回到触发控件。触发控件已因数据变化消失时（取消后卡片移到「已取消」列、选定后候选网格重渲染），焦点落到同一 job 卡片的新位置或该 key 的候选组，绝不落到 `body`。
  - 验证：V-KB 断言 `activeElement !== body`，且 `data-job-id`（或 key）与触发时相同。
- **A11Y-DLG-5 409 冲突可操作，不丢输入** — P2、P7 · 3.3.1、3.3.4、3.3.7 · `mandatory`
  - 要求：保存返回 409 时以 dialog 或 `role="alert"` 呈现且焦点移入，说明「文件已在别处被修改」，动作全部键盘可达；关闭提示后表单里未保存的修改仍在。
  - 验证：V-STATE 加载后改动盘上 TOML，再保存。

### 2.5 表单 A11Y-FORM（P2、P7、P5 筛选、P3 描述）

- **A11Y-FORM-1 程序化标签** — P2、P3、P5、P7 · 1.3.1、3.3.2 (A)、4.1.2 · `mandatory`
  - 要求：每个控件有 `<label for>` 或被 label 包裹；可见文字 = 中文说明 + config 键（如「剧缩写 `drama.abbrev`」），使预检错误里的 config 键能对应到控件；placeholder 不能是唯一标签；单位（秒 / 小时 / 积分）写在 label 或 description。
  - 验证：V-AXE `label`；脚本断言 schema 每个可编辑键都有 accessible name 含该键的控件。
- **A11Y-FORM-2 分组、枚举与开关** — P2、P7 · 1.3.1、3.3.2、4.1.2 · `mandatory`
  - 要求：TOML 表用 `<fieldset><legend>` 或 `role="group"` + `aria-labelledby`；枚举键（`video.negative_prompt`、`outputs.image_on_existing`、`routing.video` / `routing.image`、`browser.channel`）用单选组或带标签 `<select>`；布尔键用 checkbox 或 `role="switch"` + `aria-checked`。`confirm.allow_http_auto` 的 description 须写明「开启后脚本可带 auto_confirm 跳过人工确认直接花积分（受每日预算约束）」。
  - 验证：V-AXE `aria-toggle-field-name`；断言该开关的 description 文字。
- **A11Y-FORM-3 剧列表** — P2 · 4.1.2 · `mandatory`
  - 要求：系列折叠用 disclosure button（`aria-expanded`）或完整 tree 模式（`role="tree"` + 方向键）；选中剧带 `aria-current` 或 `aria-selected`。
  - 验证：V-KB（KB-2 的 F2）。
- **A11Y-FORM-4 校验错误** — P2、P7 · 3.3.1、3.3.3 (AA)、4.1.3、3.3.7 · `mandatory`
  - 要求：schema 拒绝保存时（FR-4 返回字段路径）：
    - 顶部错误汇总以 `role="alert"` 呈现或获得焦点，每条是跳到对应控件的链接；
    - 出错控件带 `aria-invalid="true"` + `aria-describedby`，错误文字含字段路径与修正建议；路径无对应控件（仅在原文 TOML）时，汇总里写出完整路径；
    - 即时校验只在 blur 或提交时播报，不逐键播报；失败后已输入值全部保留。
  - 验证：V-STATE 提交非法值（如 `precheck.entity_name_max_chars = -1`），断言 alert、`aria-invalid`、description 含路径、链接能把焦点带到控件。
- **A11Y-FORM-5 「需要你确认」不只靠黄色** — P2 · 1.4.1 (A)、1.3.1 · `mandatory`
  - 要求：FR-3 每个 `needs_confirmation` 项同时具备文字徽标「需要你确认」、经 `aria-describedby` 关联的原因文字（如「独立剧缺缩写」「期望主体名与即梦现有主体不一致」）、页面汇总「N 项需要你确认」。状态已由文字传达，黄色本身不需达到 3:1，但黄底上的文字仍须满足 VIS-1。
  - 验证：V-STATE；V-DECOLOR 后断言每项仍有徽标与原因。
- **A11Y-FORM-6 已有 config 的逐键 diff** — P2 · 1.4.1 · `mandatory`
  - 要求：新增 / 删除 / 修改以文字或带读屏文字的 +/− 前缀表达，不只靠红绿。
  - 验证：V-STATE（已有 config 时 propose）+ V-DECOLOR。
- **A11Y-FORM-7 原文 TOML 视图** — P2 · 1.3.1、2.1.1、4.1.2 · `mandatory`
  - 要求：表单 / 原文切换用 tabs（`role="tablist"` + 方向键 + `aria-selected`）或两个 `aria-pressed` 按钮；只读 `<pre>` 可横向滚动时须带 `tabindex="0"` 与 `aria-label="jimeng_config.toml 原文"`；可编辑时为带标签的 textarea / 编辑器，语法错误以文字给出行列并关联。
  - 验证：V-AXE `scrollable-region-focusable`；V-KB。

### 2.6 实时更新 A11Y-LIVE（P4 为主，横幅全局）

- **A11Y-LIVE-1 状态转移礼貌播报，且不刷屏** — P4 · 4.1.3 · `mandatory`
  - 要求：用一个首次渲染起就在 DOM 里的 `role="status"` 区域，只播报 job 进入 `generating` / `done` / `failed(原因)` / `cancelled` / 作业级 `paused_needs_human(原因)` 以及「批次全部完成」；平台进度百分比与子步骤进度**不播报**；5 s 窗口内的多条转移合并成一条（「3 个任务更新：shot02 完成，…」）。*(judgment call — 5 s 合并窗口)*
  - 验证：V-LIVE，Fake 站点 10 s 内推 30 次进度 + 6 次转移，断言 status 文字变化 ≤ 3 次且不含 `%`。
- **A11Y-LIVE-2 队列级暂停强播报，任何页面可见** — P1–P7 · 4.1.3、1.3.1 · `mandatory`
  - 要求：出现 FR-21 队列级原因时，应用外壳显示 `role="alert"` 横幅，含 backend 与中文原因（「web 队列已暂停：出现验证码或风控弹窗，请在浏览器窗口处理后恢复」），附键盘可达的「查看截图」「恢复」「前往队列看板」；每个暂停事件只播报一次，轮询不重播。toast 只是尽力而为（FR-56），横幅才是可靠通道。
  - 验证：V-LIVE，停在 P2 时注入验证码弹窗，断言 alert 出现 1 次；继续轮询 60 s 次数不增加。
- **A11Y-LIVE-3 刷新不抢焦点，也不偷换焦点目标** — P4 · 2.4.3、3.2.2 · `mandatory`
  - 要求：更新从不移动焦点；列表以 `job_id` 为稳定 key；聚焦的 job 换列后焦点仍在同一 job；重排不能让已聚焦的「取消」变成另一个 job 的「取消」。
  - 验证：V-KB 聚焦 job A 的取消按钮 → Fake 站点推动 A、B 同时转移 → 断言焦点 `data-job-id` 仍为 A，按 Enter 打开的是 A 的对话框。
- **A11Y-LIVE-4 可冻结自动刷新，「暂停」不混用** — P4 · 2.2.2 (A) · `mandatory`
  - 要求：看板提供「冻结看板刷新」开关（冻结期间 LIVE-2 横幅照常生效）；它的名称须与「暂停 web / CLI 队列」（`pause_queue`，真实后端动作）和状态标签「需人工处理」（`paused_needs_human`）明显区分，不得三者都叫「暂停」。
  - 验证：V-KB；断言三者 accessible name 各不相同。
- **A11Y-LIVE-5 状态不只靠颜色** — P4 · 1.4.1、1.3.1、4.1.2 · `mandatory`
  - 要求：
    - 卡片有中文状态文字（不直接显示枚举）+ `aria-hidden` 图标；列标题含状态名与计数（「生成中（2/3）」，反映 `max_remote_rendering`）；暂停 / 失败原因为文字；
    - 进度用 `role="progressbar"`，带 `aria-label`（job 名）、`aria-valuenow/min/max`、`aria-valuetext`（「上传 2/4 · 平台进度 37%」）；
    - 子步骤 `set_params → upload → fill → preview` 为有序列表，当前步 `aria-current="step"`，已完成步有文字「已完成」。
  - 验证：V-AXE `aria-progressbar-name`；V-DECOLOR。
- **A11Y-LIVE-6 异步动作有结果播报** — P1、P4 · 4.1.3 · `mandatory`
  - 要求：
    - P1「运行 canary」期间区域 `aria-busy`、按钮显示忙态文字；结束时通过则礼貌播报「canary 通过 {n}/{n}」，失败则 alert 并列出失败项；逐项结果以文字 + 图标表达；
    - 「打开浏览器窗口」效果在页面之外，须播报「已将浏览器窗口置前」；`cli_login_required` 以文字提示「请在终端运行 `dreamina login`」；
    - P4「恢复」时 canary 失败（FR-23）以 alert 播报原因。
  - 验证：V-STATE + V-LIVE。

### 2.7 图片 A11Y-IMG

- **A11Y-IMG-1 参考缩略图** — P3 · 1.1.1 (A) · `mandatory`
  - 要求：`alt` = `{name}，{label}，{kind 中文}`，视频参考封面同式；音频无图时以文字行呈现；主体写「主体 hy3_主角」；文件缺失显示文字「文件缺失：{name}」而非破图；解析出的路径同时以文字给出。
  - 验证：V-AXE `image-alt`；断言 alt 含 `name` 并与 `GET /api/batches/{id}` 的 references 对账。
- **A11Y-IMG-2 截图** — P1、P4 · 1.1.1、1.3.1 · `mandatory`
  - 要求：暂停截图（FR-21）、预演截图（FR-32）、失败现场（FR-36）的 alt 写明类型 + job + 原因 + 时间（「暂停截图 · shot02 · 验证码或风控弹窗 · 18:15:02」）；原因同时以文本出现在截图旁，截图不是唯一信息来源；打开大图的是按钮，名称含同样信息，大图查看遵守 DLG。
  - 验证：V-AXE + 脚本断言 alt 与相邻原因文字。
- **A11Y-IMG-3 候选网格的选中状态** — P5 · 4.1.2、1.3.1、3.2.2 · `mandatory`
  - 要求：每个 key 一组单选——`role="radiogroup"` + `aria-label="{key} 候选图"`，每张 `role="radio"` + `aria-checked`，方向键移动（或视觉隐藏的原生 radio 以图片为 label）；`aria-pressed` 切换按钮仅在组内恒只有一个 pressed 时可接受。alt =「{key} 候选 {i}，{ts}」；当前定稿以文字标出。移动选择**不触发**升格，升格只由单独的「选定」+ DLG 归档确认完成。
  - 验证：V-AXE；V-KB 按方向键 3 次，断言 `POST /api/candidates/promote` 为 0。
- **A11Y-IMG-4 图标与悬停内容** — P1–P7 · 1.1.1、1.4.13 (AA) · `mandatory`
  - 要求：装饰图标 `aria-hidden` 或 `alt=""`；纯图标按钮有名称；缩略图若有悬停放大 / tooltip，须可 Esc 关闭、鼠标可移入、键盘聚焦同样出现。
  - 验证：V-AXE `button-name`；V-KB 聚焦缩略图后按 Esc。

### 2.8 表格 A11Y-TBL（P3 条目、P2 参考项解析预览、P5 历史、P6 对账、P1 canary 逐项）

- **A11Y-TBL-1 表格语义** — 上述各表 · 1.3.1 · `mandatory`
  - 要求：原生 `<table>`，带 `<caption>` 或 `aria-labelledby`；列头 `<th scope="col">`，身份列（shot / job / 主体名）为 `<th scope="row">`；不用 div 拼表；除非完整实现 grid 键盘模式，否则不用 `role="grid"`。
  - 验证：V-AXE `th-has-data-cells`、`td-headers-attr`、`table-duplicate-name`；脚本断言每表有 caption 或 label。
- **A11Y-TBL-2 排序（如果实现）** — P5、P6 · 4.1.2、4.1.3 · `mandatory`（spec 未要求排序，未实现则 N/A）
  - 要求：排序控件是 `<th>` 内的 `<button>`；仅当前排序列带 `aria-sort`；排序变化礼貌播报。
  - 验证：V-KB + V-LIVE。
- **A11Y-TBL-3 筛选与结果播报** — P5、P6 · 3.3.2、4.1.3 · `mandatory`
  - 要求：剧 / 镜 / 主体 / 日期筛选控件有标签（「起始日期」「结束日期」附格式说明）；应用筛选后 status 播报「共 N 条，预估 X、实扣 Y 积分」；空结果以文字说明。
  - 验证：V-LIVE。
- **A11Y-TBL-4 状态与偏差是文字** — P2、P3、P5、P6 · 1.4.1 · `mandatory`
  - 要求：P6 三态显示「已映射 / 即梦缺失 / 即梦上有但未映射」+ 图标，「创建」只在缺失行且名称含主体名；预估偏差超 `estimate_deviation_warn_pct` 时以文字「偏差 +34%（阈值 20%）」标出；`as_of` 以文字给出；P2 解析预览错误行以文字「错误」+ 信息 + 应填 config 键呈现。
  - 验证：V-STATE + V-DECOLOR。
- **A11Y-TBL-5 200% 缩放与重排** — P1–P7 · 1.4.4 (AA)、1.4.10 (AA) · `mandatory`
  - 要求：视口 640×360 CSS px（≈ 1280×720 窗口 200%）下无内容丢失、重叠或中文标签截断，页面本身无横向滚动；允许横向滚动的只有表格、原文 TOML `<pre>`、截图查看器、看板列容器，且这些容器可聚焦、有名称。
  - 验证：Playwright 视口 640×360 断言 `scrollWidth <= clientWidth`；V-AXE `scrollable-region-focusable`；真实 Ctrl+ 缩放见 MW-6。

### 2.9 视觉：对比度、主题、焦点、动画 A11Y-VIS

- **A11Y-VIS-1 文字对比度** — P1–P7 · 1.4.3 (AA) · `mandatory`
  - 要求：浅色 chrome 上正文 ≥ 4.5:1、大字 ≥ 3:1。重点查：灰色辅助文字（`as_of`、路径、时间戳）、黄色需确认行上的文字、状态徽标（白字配绿 / 橙底）、错误红字、`aria-disabled` 但仍需阅读的按钮文字。
  - 验证：在 V-STATE 各状态下跑 V-AXE `color-contrast`；MW-5 补查。
- **A11Y-VIS-2 非文字对比度** — P1–P7 · 1.4.11 (AA) · `mandatory`
  - 要求：输入框边框、checkbox / radio / switch 各状态、进度条填充 vs 轨道、候选选中边框、焦点环与相邻颜色 ≥ 3:1。
  - 验证：单元测试对 CSS 设计 token 配对计算对比度；MW-5。
- **A11Y-VIS-3 暗色原文 TOML 面板** — P2 · 1.4.3、1.4.11、2.4.7 (AA) · `mandatory`
  - 要求：development.md §7 carve-out 允许的暗色 `<pre>`：暗色是该元素无条件默认值、不由媒体查询触发；所有语法高亮 token 对暗底 ≥ 4.5:1（注释色最常翻车）；选区与焦点环在暗底可见，焦点环同时与相邻白色 chrome ≥ 3:1。
  - 验证：语法高亮渲染完成后跑 V-AXE `color-contrast`；MW-4。
- **A11Y-VIS-4 chrome 不随系统切换暗色** — P1–P7 · development.md §7（blocker 来源）· `mandatory`
  - 要求：构建 CSS 的 `:root` 只有 `color-scheme: light`；不存在作用于 body / 导航 / 工具栏 / 面板 / 按钮 / 表单的 `@media (prefers-color-scheme: dark)`。
  - 验证：扫描 `apps/api/static/**/*.css` 与 `apps/ui/src/**` 的 `prefers-color-scheme` 逐条判定；`emulateMedia({ colorScheme: 'dark' })` 下 `body`、导航、按钮的 computed 背景色与 light 一致，V-AXE `color-contrast` 结果不变。
- **A11Y-VIS-5 焦点可见，且不被遮挡** — P1–P7 · 2.4.7、2.4.11 (AA) · `mandatory`
  - 要求：每个可聚焦元素键盘聚焦时有可见指示（`:focus-visible`），无「`outline: none` 且无替代」；焦点元素不被 sticky 头部、全局暂停横幅、底部操作栏完全遮住。
  - 验证：V-KB 逐页 Tab 遍历，断言 computed `outline` / `box-shadow` 非 none，且中心点 `elementFromPoint` 命中自身或后代；横幅显示态再跑一遍。
- **A11Y-VIS-6 动画** — P1、P4 · 2.2.2 (A)、2.3.1 (A) · `mandatory`
  - 要求：持续超过 5 s 的动画（「生成中」脉冲、不定进度条纹、spinner——即梦渲染动辄数分钟）在 `prefers-reduced-motion: reduce` 下停止或提供停止方式；进度数值仍以文字更新；无每秒 3 次以上闪烁。
  - 验证：`emulateMedia({ reducedMotion: 'reduce' })` 后断言 `document.getAnimations()` 中无 `iterations === Infinity`。

### 2.10 错误与空状态 A11Y-ERR

- **A11Y-ERR-1 数据加载失败不白屏** — P1–P7 · 4.1.3、3.3.1；development.md §8 / §9 · `mandatory`
  - 要求：每页（含深链接直接进入）在 API 500、网络中断、403 时，`<main>` 内仍有 `h1` + `role="alert"` 错误块，文字含 `message` 与 `hint`（§5.10 错误结构），并有键盘可达「重试」。空数据时显示说明文字（「还没有任务」「该剧还没有 config，可以点『生成默认 config』」）。
  - 严重度：深链接进入后 main 为空 → `critical`；有错误但未以 alert 暴露或无重试 → `blocker`。
  - 验证：`page.route('**/api/**')` 逐页注入 500 / abort / 403，断言 main 非空、alert 存在、重试可聚焦、console 无未捕获错误。
- **A11Y-ERR-2 渲染期异常的回退界面可达** — P2、P3、P4 · 4.1.3；development.md §9 · `mandatory`
  - 要求：解析后再渲染的组件（原文 TOML 视图、config diff、参考项解析预览、截图元数据）由各自面板的 Error Boundary 包住；回退界面为 `role="alert"` 文本 + 重试；页面其余部分仍可操作，焦点不掉到 `body`。
  - 验证：V-STATE 返回畸形 config 或缺字段的 job 响应。
- **A11Y-ERR-3 动作失败强播报** — P2–P7 · 4.1.3、3.3.1、3.3.3 · `mandatory`
  - 要求：确认被拒（过期 / 摘要不一致 / 已使用）、恢复时 canary 失败（FR-23）、创建主体失败、选定失败、保存失败，一律 `role="alert"` 播报中文原因 + hint；焦点留在触发控件或移到错误信息，不丢失。
  - 验证：V-STATE + V-LIVE。

## 3. Recommended checks（缺口 → `warning`）

- **A11Y-REC-1**：「跳到主内容」skip link（2.4.1 最低要求已由地标满足）。
- **A11Y-REC-2**：代码标识符与原文 TOML 标 `lang="en"` + `translate="no"`（3.1.2 对技术术语有豁免）。
- **A11Y-REC-3**：标题严格不跳级（axe `heading-order`）。
- **A11Y-REC-4**：P2「下一个需要确认的项」跳转；解析预览里「应填 config 键」做成链接，把焦点带到对应 override 控件。
- **A11Y-REC-5**：token 过期前 2 分钟一次性礼貌提醒（不是逐秒倒计时播报）。
- **A11Y-REC-6**：点击 toast（FR-56）进入的页面，焦点落到对应 job 或横幅。
- **A11Y-REC-7**：400% 缩放（320 CSS px）可重排；1.4.12 调整文字间距后不截断。
- **A11Y-REC-8**：焦点环 ≥ 2 px 且 ≥ 3:1（2.4.13，AAA）。
- **A11Y-REC-9**：加载中区域 `aria-busy="true"` + 「加载中…」文字。
- **A11Y-REC-10**：P1 `dreamina login` 命令旁提供复制按钮，复制成功礼貌播报。
- **A11Y-REC-11**：P7 以文字说明「token 等机密在 `.env` 中配置，此处不显示」。
- **A11Y-REC-12**：进入 P3 时经 `h1` description 或 status 播报一次「N 条，预计 X 积分，M 条警告，K 条错误」。
- **A11Y-REC-13**：axe 其余 best-practice 规则零违规。

## 4. 人工走查清单（发 `validation.requires_manual_walkthrough`）

环境：Windows 11 + Chrome + NVDA（最新稳定版，中文语音）；离线 Fake 即梦站点 + V-STATE 预置状态；不接真实账号。

- **MW-1 读屏走完 F3**：只听不看。按确认前能否听到条目数、合计积分（静态 / 页面）、每条 warning / error；确认只触发一次；能听到结果。
- **MW-2 播报体感**：Fake 站点连续生成 5 分钟，礼貌播报是否打扰到在其他页面干活；在 P2 编辑时注入验证码弹窗，是否立即听到且只听到一次。
- **MW-3 高风险对话框**：提交后取消、分步提交、选定归档——是否先听到后果文字才到执行按钮；Esc 或打开后立即 Enter 都是安全结果。
- **MW-4 焦点可见**：七页 + 暗色 TOML 面板 + 黄色需确认行 + 横幅显示态，真实键盘下焦点始终看得见、不被横幅挡住。
- **MW-5 对比度抽查**：用 Colour Contrast Analyser 取色，查 axe 算不了的——截图上的叠加文字、半透明 / 渐变背景、状态徽标、候选选中边框、进度条、焦点环。
- **MW-6 200% 缩放**：1280×720 窗口 Ctrl+ 到 200%，七页可读可用，看板能完成取消与恢复，中文标签不截断。
- **MW-7 减少动画**：Windows「设置 → 辅助功能 → 视觉效果」关闭「动画效果」，无脉冲 / 条纹动画，进度仍可感知。
- **MW-8 中文读屏质量**：NVDA 以中文语音读界面；状态读中文标签而非 `paused_needs_human` 这类枚举；config 键与路径可辨。
- **MW-9 感知延迟**：canary、生成默认 config、保存、确认、恢复时忙态可感知，不会被误以为卡死。
- **MW-10 措辞可懂**：「积分不会退还」「将移到 `_deleted/`」「开启后脚本可跳过人工确认」对用户本人清楚无歧义。
- **MW-11 toast 落点**：点击 toast 打开正确页面；若实现了 REC-6，焦点落在对应项上。

## 5. 注记（给 parent 综合）

1. **mandatory 范围需要用户确认。** spec FR-54 / FR-55 没有 a11y 条款；本 level 的 mandatory 集合来自 general.md 标准严重度表，加上花钱、移动文件的动作。建议 stage-5 签核时向用户确认，尤其是 LIVE-4（冻结看板刷新）、GATE-6（token 过期处理）、KB-4（高风险动作禁止快捷键）。
2. **与 a11y 相关的 spec 缺口**，建议 parent 路由到 spec 或 system_tests：
   - (a) token 30 min 过期后 UI 如何呈现与恢复，spec 没写——GATE-6 补上。
   - (b) F7 分步「提交」在 UI 上的二次确认形式没写——本 level 按 FR-55 视为 DLG 适用。
   - (c) 看板更新机制（轮询还是推送）没定——LIVE-1 / LIVE-3 与机制无关。
   - (d) FR-49 主体创建确认是否复用批次确认页没定——GATE-1 至 GATE-5 两种都覆盖。
   - (e) 「暂停」在 UI 上有三义（`pause_queue` 动作、`paused_needs_human` 状态、冻结刷新）——LIVE-4 要求区分。
3. **`resume_queue` 不要求二次确认。** 恢复后继续提交的是**已确认**批次，不构成新的花钱授权，只要求结果播报（LIVE-6）。*(judgment call)*
4. **与其他 level 的边界。** 确认闸门的服务端强制（FR-14 / FR-16）归 security 与 system_tests；合计积分一致（spec §9 第 12 条）由 system_tests 断言，GATE-3 复用同一份数据；白屏本身属 development.md §8 逐页 e2e，ERR-1 只加 a11y 断言。
5. **judgment call 阈值**：5 s 播报合并窗口、640×360 CSS px 模拟 200% 缩放、高风险对话框用 `alertdialog`。24×24 px 目标尺寸是 WCAG 2.5.8 原值，不是 judgment call。
