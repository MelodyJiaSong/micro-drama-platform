---
worker_id: level-specialist-01-acceptance_criteria
stage: 5
role: level-specialist
level: acceptance_criteria
status: complete
blockers:
  - "C1 critical carve-out conflict: FR-18 背压「并行任务已达上限 → 放回 awaiting_submit_slot」 vs §2「任何形式的自动重复提交」/ FR-20 提交零自动重试 / §9.3「只点击一次生成」"
  - "C2 critical carve-out conflict: §2「网页端图片生成 out of scope」 vs FR-1 routing.image 允许取 web"
  - "C3 critical carve-out conflict: §2「旧写法通过每剧 config override 解决」 vs FR-8「旧写法一律预检错误」+ prompt 逐字节不改（=>@1 的槽位号没有任何 config 键能消除）"
  - "C4 critical gate ambiguity: HTTP bearer-token 调 POST /api/batches/{id}/confirm 时 confirmer 如何判定，是否受 confirm.allow_http_auto 与每日预算约束（否则脚本可绕过 FR-15）"
confidence: medium
---

# Acceptance criteria — jimeng_web_bridge

Run: `jimeng_web_bridge-20260913-093603` · Level: acceptance_criteria · 契约：`final_specs/spec.md`（FR-1..FR-56、§6 NFR、§9）

## 0. 约定

- **场景 ID 与标签**：场景 ID 为 `AC-{组}-{NN}`，每个场景带 `@severity:*` 与 `@FR-n` 标签。
- **严重度**：按 `validation/general.md` 标准表，叠加 `validation/development.md` 的升级表。
  - `critical`（立即 halt）：安全失败、沙箱逃逸、未确认却花了积分、自动重复提交、测试触碰真实站点、启动失败。
  - `blocker`（3 轮修订上限）：其余验收失败。
  - `warning`：观测指标越界，只记录（§19）。
- **只跑离线**：所有自动化场景都跑在 `FakeJimeng`（离线 Fake 即梦站点）与 fake `dreamina` 上。`@manual` 场景才碰真实站点，并发 `validation.requires_manual_walkthrough`。
- **待裁决场景**：标 `@pending:Cn` / `@pending:Gn` 的场景，期望值取决于 §20 里待裁决的 spec 缺口。裁决前按「现有 spec 最严读法」执行，裁决后由 parent 回填。
- **断言对象**：断言读消费方看得到的东西——FakeJimeng 服务端记录、盘上字节、API / MCP 返回、真实浏览器里渲染出的 DOM。不读实现内部变量。
- **pin 保留检查**：本任务各阶段都没有 `promoted.md`，不生成此项检查。

## 1. 公共 Background 与真实数据夹具

```gherkin
Background: 离线测试世界
  Given 临时仓库根 T；T/ai_videos/huangye_shenghuo/ 是真实子树的拷贝（series.json、_series/、hy1–hy4 的全部 md 与 .link.json 逐字节保留；媒体文件保留文件名，内容换成小占位文件并记录 sha256）
  And T/ai_videos/ 另含 wushen_juexing、rexue_gaoxiao、xianjian_yi_mv 的最小子树（角色卡目录名 + §1 表中 shot md 的逐字节副本）
  And FakeJimeng 运行在本机，服务端记录 generate_clicks[{job_hint, at}]、上传文件名序列、编辑器 DOM（纯文本 + mention 节点序列）、entity_mutations[]、全部请求及其发起方（页面脚本 / 外部）
  And FakeJimeng 可注入 captcha_popup | login_expired | insufficient_credit | moderation_reject | real_face_rejected | upload_rejected | concurrency_limit_notice | editor_append_on_blur | missing_control:{name} | malformed_history_body | suppress_submit_response | close_context
  And fake dreamina（DREAMINA_CLI_PATH 指向它）逐次记录 argv 数组，可设 ok | fail | not_logged_in | compliance_required | version=1.4.4
  And .env 设 JIMENG_BRIDGE_TOKEN=test-token-7f3a，JIMENG_BRIDGE_PROFILE_DIR 指向临时目录
  And service 用与 `make run` 相同的入口启动（API + /mcp + 已构建 UI，serve_static=True），监听 127.0.0.1:8790
  And 出站到 *.jianying.com / *.bytedance.com / *.capcut.com 的连接全部被拦截，一旦命中即判失败
  And 主体快照 = { hy3_主角, hy1_主角, xj_测试 }，同步于 1 h 前
  And T/ai_videos/huangye_shenghuo/hy3/jimeng_config.toml = FR-2 默认值 + [entities] overrides = { "c1_砌炉的老人" = "hy3_主角" }
  And 时钟可注入（FakeClock）；提交间隔一律以 FakeJimeng 服务端时间戳断言
```

| 夹具 | 真实值（取自仓库，2026-09-13） |
|---|---|
| golden shot | `huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md`：`## 视频 prompt` 围栏正文 2314 字符（hy3 各镜最大 3693）；`比例: 16:9`；`时长: 22秒` |
| shot02 参考项 | `bg11-1(场景参考图)` → `2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11-1.png`<br>`砌炉的老人(Seedance 人物 entity)` → 主体 `hy3_主角`<br>`p2-1(随身装备锚点)` → `props/p2_随身装备/p2-1.png`<br>`p3-1(抹泥板锚点)` → `props/p3_抹泥板与黏土壁炉/p3-1.png` |
| 同 stem 陷阱 | `bg11-1.png` 在 hy1（`yulin/bg11_溪谷`）、hy2（`hongshan/bg11_地窝风暴夜`）、hy4（`shenxue/bg11_雪井风雪夜`）各有一张 |
| 反向提示词 | 紧跟视频 prompt、由「反向提示词」引出的 ```text 围栏，开头为 `第二个人, 人群, 路人` |
| 角色卡 | hy3 `c1_砌炉的老人/`：`c1-1.png`、`c1-2.mp4`；md 内有 `c1-1_砌炉的老人立绘`、`c1-2_砌炉的老人turntable` 两个块<br>hy3 `c2_獾/`：`c2-1.png`；md 内有 `c2-1_獾锚点` 块，以及锁定描述符裸围栏 |
| 跨集复用 | hy2 `characters/c1_造家的人/c1_造家的人.png.link.json` → hy1 同名文件<br>hy2 `props/p2_随身装备/p2_随身装备.png.link.json` → hy1 同名文件 |
| 旧写法（真实） | rexue_gaoxiao：`学校泳池_bg2_水面_俯拍=>@1`、`(道具参考图)`（共 20 个 shot 带 `=>@数字`）<br>xianjian_yi_mv shot18：`c3_英气女子=>@, s5_bg3_石门内侧=>@`（无括号）<br>wushen_juexing：`裴知秋=>, bg6_座前_虚化背景=>`（无 `@`） |
| 已有产物 | hy3 `shot01/renders/`、`shot02/renders/` 已有手工下载的 mp4 |

## 2. F1 首次启动与登录

```gherkin
@severity:blocker @FR-25 @FR-26 @FR-27 @FR-56
Scenario: AC-F1-01 未登录首启 → login_required → 手动登录 → ready
  Given profile 目录为空，FakeJimeng 处于未登录态
  When 用户执行 make run
  Then 按 browser.channel 启动有界面浏览器，打开 browser.start_url 指向的创作页
  And GET /api/session 返回 web.login = "login_required"；ToastClient 收到 1 条「需要登录」；浏览器窗口被置前
  When 测试替身在 FakeJimeng 完成扫码登录
  Then canary 自动运行且逐项通过；session 变为 "ready"；记录了 browser_version 与 web_version

@severity:critical @FR-26
Scenario: AC-F1-02 service 永不输入凭据
  Given 会话为 login_required
  When 过去 5 min（FakeClock），期间两次调用 POST /api/session/canary
  Then FakeJimeng 登录表单所有输入框收到的键入 / fill 事件数 = 0

@severity:blocker @FR-25
Scenario Outline: AC-F1-03 浏览器启动失败的分类，且不删锁文件
  Given <前置>
  When service 启动浏览器
  Then session.web.error = "<分类>"，且 profile 内锁文件的存在性与 mtime 不变
  Examples:
    | 前置 | 分类 |
    | 另一进程占用同一 profile | profile_in_use |
    | browser.channel 指向不存在的可执行文件 | browser_missing |
    | 浏览器进程在启动超时内未回连 | launch_timeout |
```

## 3. F2 剧 config（§5.1）

```gherkin
@severity:blocker @FR-2 @FR-3
Scenario: AC-F2-01 为 hy3 提议默认 config（§9.7）
  Given hy3 剧根下没有 jimeng_config.toml
  When POST /api/dramas/huangye_shenghuo%2Fhy3/config/propose
  Then 提议 drama.abbrev = "hy3"，不需要确认
  And entities 提议：c1_砌炉的老人 → "hy3_砌炉的老人"，c2_獾 → "hy3_獾"
  And "hy3_砌炉的老人" 带 needs_confirmation: true，原因含「期望主体名与即梦现有主体不一致」（快照里有未映射的 hy3_主角）  @pending:G24
  And references 预览列出 shot01–shot14 的全部参考项及解析结果；shot02 的 3 个 image 项解析成功
  And 盘上仍没有 jimeng_config.toml（propose 不写文件）

@severity:blocker @FR-2 @FR-3 @FR-11
Scenario: AC-F2-02 独立剧缺缩写 → 需要确认 → 预检报出 config 键
  Given 独立剧 wushen_juexing（2 段剧根）没有 config
  When 执行 propose
  Then drama.abbrev = ""，needs_confirmation: true，原因「独立剧缺缩写」
  When 按提议原样保存，再预检该剧任一 shot
  Then 该条是 error，config_key = "drama.abbrev"

@severity:blocker @FR-3
Scenario: AC-F2-03 已有 config 不被覆盖
  Given hy3 已有 config，sha256 = H0
  When 执行 propose
  Then 返回逐键 diff 建议（例如 references.search_exclude），文件 sha256 仍为 H0

@severity:blocker @FR-3 @FR-10
Scenario: AC-F2-04 hy2 跨集复用沿用来源集缩写
  Given hy2 没有 config
  When 执行 propose
  Then c1_造家的人 的期望主体名 = "hy1_造家的人"（不是 hy2_造家的人），needs_confirmation: true（快照只有 hy1_主角）
  And p2_随身装备 解析到 hy1 目标文件，sha256 取目标文件的字节

@severity:blocker @FR-4
Scenario: AC-F2-05 保存保留注释与键序，写入原子
  Given hy3 config 含注释「# 主角沿用已有主体」，键序是自定义的
  When 带读取时的 hash 保存修改 video.resolution = "480p"
  Then 文件除这一值外逐字节不变
  When 在 rename 之前注入写失败
  Then 原文件字节不变，也没有残留的半截文件

@severity:blocker @FR-1 @FR-2 @FR-4
Scenario Outline: AC-F2-06 schema 校验拒绝非法值，并指出字段路径
  When PUT <端点>，把 <字段> 设为 <值>
  Then 响应为业务错误，config_key = "<字段>"，文件字节不变
  Examples:
    | 端点 | 字段 | 值 |
    | /api/dramas/{hy3}/config | video.negative_prompt | "merge_into_prompt" |
    | /api/dramas/{hy3}/config | outputs.image_on_existing | "overwrite" |
    | /api/dramas/{hy3}/config | video.reference_mode | "首尾帧" |
    | /api/dramas/{hy3}/config | references.rules[0].kind | "gif" |
    | /api/config/global | server.host | "0.0.0.0" |
    | /api/config/global | routing.video | "api" |

@severity:blocker @FR-4 @FR-54
Scenario: AC-F2-07 并发修改返回 409
  Given UI 读取 hy3 config，得到 hash H1
  And 文件随后被外部编辑器改动
  When UI 带 H1 执行 PUT
  Then 返回 409，文件保持外部改动后的内容；UI 显示冲突提示，不丢弃用户输入

@severity:blocker @FR-5
Scenario: AC-F2-08 规则不写死（契约测试）
  Given validation 产物「config schema 键 ↔ FR」对照表
  Then schema 键集合 = 对照表键集合，且每个键指向的 FR 都存在
  And apps/ 与 libs/ 源码中不出现剧相关字面量：hy3、huangye_shenghuo、砌炉的老人、场景参考图、Seedance 人物 entity、{abbrev}_{character_name}
  When 把 hy3 的 entities.name_template 改为 "{abbrev}-{character_name}" 后再预检
  Then 期望主体名随之变为 "hy3-獾"
```

## 4. F3 Claude 出一集视频（golden path）

```gherkin
@severity:blocker @FR-6 @FR-8 @FR-13 @FR-14 @FR-17 @FR-29 @FR-30 @FR-31 @FR-33 @FR-35 @FR-42 @FR-51 @FR-52
Scenario: AC-F3-01 MCP 出 hy3 shot02 全链路（§9.1）
  Given 会话 ready，web 队列空闲
  When MCP precheck_batch(items=["ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md"])
  Then 返回 batch_id、confirmation_token、确认页 URL、合计预计积分（带 as_of）
  And 条目 ok，params = {model: seedance2.5, ratio: "16:9", duration_s: 22, resolution: 720p, count: 1, reference_mode: 全能参考}
  And references 依次为 [bg11-1:image, 砌炉的老人:entity→hy3_主角, p2-1:image, p3-1:image]，每个 image 带 sha256
  And batch 为 awaiting_confirm，FakeJimeng generate_clicks = 0
  When 用户在真实浏览器打开确认页，点「确认并开始」
  Then batch.confirmer = ui_human，确认时间入库；执行前 canary 运行一次并通过
  And FakeJimeng 控件读回：视频生成 / Seedance 2.5 / 全能参考 / 16:9 / 720P / 数量 1 / 22s
  And 上传文件名序列恰为 [bg11-1.png, p2-1.png, p3-1.png]（主体项不上传）  @pending:G1
  And 编辑器 mention 节点序列 = [bg11-1, hy3_主角, p2-1, p3-1]
  And 编辑器纯文本（空白规范化，mention 按名称计）= prompt 原文中 4 处 `@` 换成对应名称；首行为 shot02，含 `参考:` 行
  And 编辑器文本不含「第二个人, 人群, 路人」
  And job 转移 = queued → preparing(set_params→upload→fill→preview) → awaiting_submit_slot → submitting → generating → downloading → done
  And generate_clicks 恰为 1
  When Claude 循环调用 wait_jobs，直到 done
  Then 每次调用 ≤ 90 s 返回
  And shot02/renders/ 下恰好新增 1 个 shot02_{YYYYMMDD-HHmmss}.mp4，sha256 = FakeJimeng 下发文件的 sha256
  And 旁边有 .mp4.jimeng.json，满足 AC-OUT-02；renders/ 下原有文件的名字与字节都不变

@severity:blocker @FR-7 @FR-15
Scenario: AC-F3-02 脚本经 HTTP 出同一镜（入口对等）
  Given global confirm.allow_http_auto = true，当日 auto_confirm 累计 = 0
  When 脚本带 Bearer token 调 POST /api/batches（shot02，auto_confirm=true），再循环调 POST /api/jobs/wait
  Then confirmer = http_auto；产物、sidecar 字段、generate_clicks = 1，与 AC-F3-01 一致  @pending:C4 @pending:G8

@severity:blocker @FR-14 @FR-15 @FR-51
Scenario: AC-F3-03 在 Claude Code 权限询问里批准 confirm_batch
  When MCP confirm_batch(batch_id, token)（该调用已被人工批准）
  Then batch.confirmer = mcp，队列开始执行
```

## 5. F4 暂停与恢复（§5.5 FR-21 / FR-23）

```gherkin
@severity:blocker @FR-18 @FR-21 @FR-23 @FR-56
Scenario: AC-F4-01 验证码 → 暂停 web 队列 → 人工处理 → 恢复（§9.4）
  Given 已确认 batch 含 hy3 shot03、shot04；另有已确认的 CLI 图片 job c2-1
  When shot03 处于 set_params 时，FakeJimeng 注入 captcha_popup
  Then web 队列暂停，reason = captcha_or_risk_popup，附全页截图路径
  And shot03 → paused_needs_human(captcha_or_risk_popup)；shot04 不再前进  @pending:G19
  And ToastClient 收到 1 条队列暂停通知（含原因）
  And CLI job c2-1 继续跑到 done；暂停期间 generate_clicks 不增加
  When 替身关闭弹窗，调用 POST /api/queues/web/resume
  Then 先跑 canary 且通过，shot03、shot04 最终 done，每条各只点 1 次生成

@severity:blocker @FR-23 @FR-27
Scenario: AC-F4-02 恢复前自检失败 → 保持暂停
  Given web 队列因 login_expired 暂停，FakeJimeng 仍未登录
  When MCP resume(queue="web")
  Then isError: true，原因 login_expired 仍在；队列仍暂停，generate_clicks 不变

@severity:blocker @FR-20 @FR-21
Scenario: AC-F4-03 审核被拒只让该 job 失败
  Given 已确认 batch 含 shot03、shot04、shot05，shot03 已提交
  When FakeJimeng 对 shot03 返回 moderation_reject
  Then shot03 → failed(moderation_reject)，prompt_sha256 与预检一致，之后没有针对 shot03 的点击
  And web 队列未暂停，没有队列级 toast，shot04、shot05 跑到 done

@severity:blocker @FR-1 @FR-21 @FR-38 @FR-40
Scenario Outline: AC-F4-04 暂停原因的分级
  When 注入 <注入>
  Then reason = <reason>，影响范围 = <范围>
  And 队列级：该 backend 队列暂停 + 1 条 toast + 截图路径入库；作业级：队列继续，没有队列级 toast
  Examples:
    | 注入 | reason | 范围 |
    | login_expired | login_expired | web 队列 |
    | captcha_popup | captcha_or_risk_popup | web 队列 |
    | insufficient_credit | insufficient_credit | web 队列 |
    | missing_control:TipTap 编辑器 | page_contract_broken | web 队列 |
    | close_context | browser_lost | web 队列 |
    | dreamina not_logged_in | cli_login_required | cli 队列 |
    | dreamina compliance_required | compliance_confirmation_required | cli 队列 |
    | moderation_reject | moderation_reject | 仅该 job（failed） |
    | real_face_rejected | real_face_rejected | 仅该 job @pending:G2 |
    | upload_rejected | upload_rejected | 仅该 job @pending:G2 |
    | 持续的 editor_append_on_blur | fill_mismatch | 仅该 job @pending:G2 |
    | generating 超过 wait.timeout_h = 12 h（FakeClock） | wait_timeout | 仅该 job（paused_needs_human） |
```

## 6. F5 资产出图（§5.7 / FR-9 / FR-43）

```gherkin
@severity:blocker @FR-9 @FR-38 @FR-39 @FR-43 @FR-44
Scenario: AC-F5-01 text2image → 候选 → promote → 旧文件归档（§9.9）
  Given hy3 c2_獾.md 里有首行为 c2-1_獾锚点 的 ```text 块；image config 取默认（5.0 / 2k / command auto / characters 3:4）
  And 盘上 c2_獾/c2-1.png 的 sha256 = S0
  When precheck_batch(items=[{card_path: ".../characters/c2_獾/c2_獾.md", key: "c2-1"}])，并在 UI 确认
  Then fake dreamina 的 argv 是数组，子命令为 text2image，含模型 5.0、2k、3:4
  And 拿到 submit_id 立即持久化，job → generating；随后用 query_result --submit_id … --download_dir {临时目录} 轮询下载
  And 候选落在 c2_獾/_candidates/c2-1/{ts}_{i}.png；c2-1.png 仍为 S0
  When POST /api/candidates/promote 选定其中一张
  Then 原文件先移到 ai_videos/_deleted/huangye_shenghuo/hy3/2_世界观人设/characters/c2_獾/c2-1.png.{ts}.png（字节 = S0）
  And c2_獾/c2-1.png 的字节 = 选定候选的字节；sidecar 落点符合 G14 的裁决  @pending:G14

@severity:blocker @FR-9
Scenario: AC-F5-02 只有路由键开头的块才是 prompt
  When 对 c2_獾.md 做资产预检（不指定 key）
  Then 恰好产生 1 个请求，block_key = "c2-1"；锁定描述符裸围栏不产生请求
  When 对 c1_砌炉的老人.md 做资产预检
  Then c1-1 → image 请求；c1-2（turntable，视频块）按 G21 的裁决处理，不得静默当成 text2image  @pending:G21

@severity:blocker @FR-9 @FR-43
Scenario: AC-F5-03 image2image 与 image_on_existing=fail
  Given hy3 config 为块 c2-1 指定参考图 characters/c2_獾/c2-1.png，且 outputs.image_on_existing = "fail"
  When 预检、确认并执行
  Then fake dreamina 子命令为 image2image，参考图路径作为单独的 argv 元素传入
  When promote 其中一个候选
  Then 业务错误 config_key = "outputs.image_on_existing"；c2-1.png 字节不变，_deleted/ 下无新增
```

## 7. F6 主体对账与创建（§5.9）

```gherkin
@severity:blocker @FR-47 @FR-48
Scenario: AC-F6-01 同步 + 三态对账
  When POST /api/entities/sync
  Then FakeJimeng 主体页被打开；dreamina_subject/get 的发起方是页面脚本（service 没有自行发出该请求）
  And 快照每项含名称、缩略图 URL、修改时间、同步时间
  When GET /api/entities/reconcile（只有 hy3 有 config）
  Then mapped = [hy3_主角 ← c1_砌炉的老人]；missing_on_platform = [hy3_獾]；unmapped_on_platform = [hy1_主角, xj_测试]

@severity:blocker @FR-49 @FR-55
Scenario: AC-F6-02 经确认创建缺失主体 hy3_獾
  When 在主体对账页对 hy3_獾 点「创建」
  Then 预检：名称 ≤ 20 字，source_images 命中 c2_獾/c2-1.png；进入确认页，描述默认取锁定描述符且可编辑  @pending:G11
  When 把描述改成「成年欧洲獾」后确认
  Then FakeJimeng 依次收到：新建主体表单 → 上传 c2-1.png → 名称 hy3_獾 + 描述「成年欧洲獾」→ 保存
  And 随后自动再同步一次，reconcile 中 hy3_獾 = mapped
  And 确认前 entity_mutations = 0

@severity:blocker @FR-49
Scenario: AC-F6-03 同名主体已存在 → 直接复用
  Given 快照已含 hy3_獾
  When 确认创建 hy3_獾
  Then entity_mutations 不增加，返回复用结果

@severity:critical @FR-50 @FR-11
Scenario: AC-F6-04 永不做破坏性操作；名称超长预检报错
  Then 整个测试套件跑完后，FakeJimeng entity_mutations 里没有 rename / delete / overwrite 类调用
  When config override 把 c2_獾 映射为 21 字的主体名，再预检 hy3 任一引用它的 shot
  Then error，config_key = "precheck.entity_name_max_chars"（或该 override 键）

@severity:blocker @FR-49
Scenario: AC-F6-05 疑似写实真人只给 warning
  Given source_images 被判为疑似写实真人
  When 预检创建
  Then 结果是 warning，不是 error，仍可确认
```

## 8. F7 分步调试

```gherkin
@severity:critical @FR-16 @FR-32
Scenario: AC-F7-01 未确认 job 可以分步到 preview，但不能 submit
  Given shot02 已预检，batch 为 awaiting_confirm
  When 依次调用 POST /api/jobs/{id}/steps/set_params、upload、fill、preview
  Then 每步成功，preview 存下全页 + composer 两张截图和页面预计积分；generate_clicks = 0
  When POST /api/jobs/{id}/steps/submit
  Then 业务错误（未确认），job 从未进入 submitting，generate_clicks = 0

@severity:blocker @FR-18 @FR-33
Scenario: AC-F7-02 确认后分步 submit 仍受节流约束
  Given 同 batch 已确认，距上一次点击生成 5 s
  When MCP browser_step(op="submit")
  Then 点击发生时刻与上一次点击相差 ≥ 15 s（服务端时间戳），且这一步只有 1 次点击
```

## 9. 输入与请求规范化（§5.2）

```gherkin
@severity:blocker @FR-6 @FR-8 @FR-31
Scenario: AC-IN-01 prompt 逐字节保留，反向提示词单独携带
  When 预检 shot02
  Then GenerationRequest.prompt 的 sha256 = shot02.md 中 `## 视频 prompt` 第一个 ```text 围栏正文的 sha256
  And negative_prompt = 紧随其后的「反向提示词」围栏正文，与 prompt 没有任何拼接

@severity:blocker @FR-8 @FR-10
Scenario Outline: AC-IN-02 默认 rules 自上而下取第一条匹配
  When 预检含 <token> 的 shot
  Then kind = <kind>，解析为 <结果>
  Examples:
    | token | kind | 结果 |
    | bg11-1(场景参考图) | image | hy3 caoya/bg11_崖脚洼地/bg11-1.png（唯一命中；hy1/hy2/hy4 的同名文件不在搜索范围） |
    | 砌炉的老人(Seedance 人物 entity) | entity | hy3_主角（override） |
    | p2-1(随身装备锚点) | image | hy3 props/p2_随身装备/p2-1.png |
    | 本镜首帧(上一镜末帧)（派生夹具：hy3 shot03 副本） | first_frame | shots/shot02/shot02_lastframe.png |
    | shot03_previz(previz灰模视频)（派生夹具） | video | 本镜目录内 stem 为 shot03_previz 的视频 |
    | 砌炉的老人声音(角色声音)（派生夹具） | audio | 剧根内 stem 为 砌炉的老人声音 的音频 |

@severity:blocker @FR-8 @FR-52
Scenario Outline: AC-IN-03 解析错误可操作——指出要填的 config 键（§9.8）
  When 预检 <shot>
  Then 该条是 error，message 指出 <token>，config_key = <config_key>；MCP 返回 isError: true，附同一条建议
  Examples:
    | shot | token | config_key |
    | hy3 派生夹具：引用 bg99-1(场景参考图) | bg99-1 缺文件 | references.overrides."bg99-1" |
    | hy3 派生夹具：_series/ 下再放一张 bg11-1.png | bg11-1 多重匹配 | references.overrides."bg11-1" |
    | rexue_gaoxiao/shot02.md | (道具参考图) 没有命中任何规则 | references.rules |
    | rexue_gaoxiao/shot02.md | 学校泳池_bg2_水面_俯拍=>@1 已填槽位号 | @pending:C3 |
    | xianjian_yi_mv/shot18.md | c3_英气女子=>@ 无括号 | references.overrides."c3_英气女子" @pending:C3 |
    | hy3 shot01 副本加 本镜首帧(上一镜末帧) | 找不到 shot00_lastframe.png | references.overrides."本镜首帧" |

@severity:critical @FR-8
Scenario: AC-IN-04 参考行里有无法识别的写法时，不能静默解析出 0 个参考项
  When 预检 wushen_juexing 中 `参考: \`裴知秋=>, bg6_座前_虚化背景=>, …\`` 的 shot
  Then 该条是 error，不是「0 个参考项的 ok」
  And 对任何 ok 条目：prompt 中 `=>@` 的出现次数 = references 数量  @pending:G15

@severity:blocker @FR-10
Scenario: AC-IN-05 剧根解析与 drama_ref 语义一致（针对真实 ai_videos 树，只读）
  Then huangye_shenghuo/hy3 = 3 段剧根；wushen_juexing = 2 段剧根
  And huangye_shenghuo 本身、huangye_shenghuo/_series、_deleted、_actors、_bgm 都不是剧
  And GET /api/dramas 把 hy1–hy4 折叠在 huangye_shenghuo 下，且不按路径深度推断  @pending:G22

@severity:critical @FR-10
Scenario Outline: AC-IN-06 .link.json 解析的沙箱
  Given hy2 某卡片的 .link.json target = <target>
  When 解析该参考项
  Then <结果>
  Examples:
    | target | 结果 |
    | ai_videos/huangye_shenghuo/hy1/2_世界观人设/props/p2_随身装备/p2_随身装备.png | 解析到 hy1 文件，sha256 取目标字节 |
    | ai_videos/../.env | 拒绝（逃出 ai_videos/） |
    | 一个 symlink 文件（Windows 无开发者模式时跳过并注明原因） | 拒绝 |

@severity:critical @FR-7
Scenario Outline: AC-IN-07 原始入口的路径沙箱
  When POST /api/batches，原始条目 files = [<path>]
  Then 该条是 error，服务端没有读取该文件
  Examples:
    | path |
    | C:\Windows\win.ini |
    | ai_videos/huangye_shenghuo/hy3/../../../projects/jimeng_web_bridge/.data/bridge.db |
    | ..\.env |
```

## 10. 静态预检（§5.3）

```gherkin
@severity:blocker @FR-11
Scenario: AC-PRE-01 预检是纯函数
  When 预检 hy3 shot01–shot14
  Then 预检期间 FakeJimeng 收到的请求数 = 0，fake dreamina 调用数 = 0

@severity:blocker @FR-1 @FR-11
Scenario Outline: AC-PRE-02 能力矩阵越界 → error
  Given shot02 用 <覆盖> 预检
  Then error 指出 <原因>，params 保持请求值（不降级）
  Examples:
    | 覆盖 | 原因 |
    | model = seedance2.0_vip | duration_s 22 超出 4–15 |
    | resolution = 1080p | seedance2.5 不支持 1080p |
    | 派生夹具：31 个图片参考 | 超出 seedance2.5 图片上限 30 |
    | ratio = "5:4" | 比例不在支持范围 |

@severity:blocker @FR-11
Scenario: AC-PRE-03 路由到 cli 却需要 web 能力 → error，不降级
  Given global routing.video = "cli"
  When 预检 shot02（seedance2.5、22 s、含主体）
  Then error 分别列出 cli 不支持 2.5、不支持 >15 s、不支持主体

@severity:blocker @FR-2 @FR-11
Scenario: AC-PRE-04 prompt 字数上限
  Then shot02（2314 字符）通过；派生夹具（5001 字符）报 error，config_key = "precheck.prompt_max_chars"  @pending:G18

@severity:blocker @FR-11
Scenario Outline: AC-PRE-05 主体引用检查
  Given <前置>
  When 预检 shot02
  Then 结果 = <结果>
  Examples:
    | 前置 | 结果 |
    | 快照同步于 25 h 前 | warning（快照过旧） |
    | 删除 override，期望名 hy3_砌炉的老人 不在快照 | error，提示去主体对账页创建，或填 entities.overrides."c1_砌炉的老人" |

@severity:blocker @FR-11 @FR-42
Scenario: AC-PRE-06 输出目标不可写或会被覆盖 → error
  Given shot02/renders 被设为只读（Windows ACL）
  When 预检 shot02
  Then error 指出输出目录不可写

@severity:blocker @FR-11 @FR-31
Scenario: AC-PRE-07 negative_prompt 策略为 fail 且平台没有负向框 → error
  Given hy3 video.negative_prompt = "fail"，PageMap 标明全能参考下没有负向框
  Then 预检 shot02 报 error，config_key = "video.negative_prompt"

@severity:blocker @FR-12
Scenario: AC-PRE-08 两种预计积分并列，偏差高亮
  Given price_table 让 shot02 的静态估算 = 400（带 as_of）
  When 对该 job 做浏览器预演，FakeJimeng 显示预计 520
  Then API 与确认页同时给出 static = 400、page = 520，并标记偏差 30% > estimate_deviation_warn_pct(20)

@severity:blocker @FR-11 @FR-13
Scenario: AC-PRE-09 含 error 条目的批次
  When 一次预检 shot02 与 rexue_gaoxiao/shot02.md
  Then 返回逐条结果与合计；error 条目不计入可确认合计；确认页的 error 条目不可勾选
  And 对该 batch 调 confirm 的结果按 G9 裁决；剔除 error 条目必须重新预检（生成新的 batch_id 与 token）  @pending:G9
```

## 11. 确认闸门（§5.4）

```gherkin
@severity:critical @FR-16 @FR-33
Scenario Outline: AC-GATE-01 未确认的 batch 从任何入口都进不了 submitting（§9.2）
  Given shot02 已预检，batch 为 awaiting_confirm
  When <入口>
  Then 该 job 的转移记录里没有 submitting，generate_clicks = 0，FakeJimeng 没有收到提交请求
  Examples:
    | 入口 |
    | HTTP POST /api/jobs/{id}/steps/submit |
    | MCP browser_step(op="submit") |
    | HTTP POST /api/jobs/{id}/resume |
    | MCP resume(job_id) |
    | HTTP POST /api/queues/web/resume |
    | 调度器空转 10 min（FakeClock） |
    | 杀进程后重启 service |

@severity:critical @FR-13 @FR-14
Scenario Outline: AC-GATE-02 token 被篡改 → 拒绝
  When 用 <token> 确认 batch A
  Then 业务错误，batch A 仍为 awaiting_confirm，没有创建任何可提交的 job
  Examples:
    | token |
    | 签名改动 1 个字节 |
    | batch B 签发的 token |
    | 把签入的合计积分改为 1 后重新 base64 编码 |

@severity:critical @FR-13 @FR-14
Scenario: AC-GATE-03 token 30 min 过期
  Given batch 于 T0 签发 token
  When 在 T0 + 30 min + 1 s 确认
  Then 拒绝（过期）
  When 对另一 batch，在 T0 + 29 min 59 s 确认
  Then 成功

@severity:critical @FR-14
Scenario: AC-GATE-04 token 单次有效（重放）
  Given batch 已用 token 确认一次
  When 用同一 token 并发发送 2 次 confirm，再串行发送 1 次
  Then 全部被拒；job 数与 confirmer 记录都只有 1 份

@severity:critical @FR-1 @FR-15
Scenario Outline: AC-GATE-05 HTTP auto_confirm 的开关与每日预算
  Given confirm.allow_http_auto = <开关>，budget.auto_confirm_daily_credits = 2000，当日已用 <已用>
  When 脚本对预计 400 积分的 batch 用 auto_confirm=true 预检
  Then <结果>
  Examples:
    | 开关 | 已用 | 结果 |
    | false | 0 | 拒绝，batch 仍需人工确认 |
    | true | 1600 | 接受，confirmer = http_auto，当日累计 2000 |
    | true | 1700 | 拒绝（超预算），不入队 |

@severity:critical @FR-15 @FR-51
Scenario: AC-GATE-06 MCP 不能自动确认；bearer 调 confirm 不能绕过开关
  When MCP precheck_batch 带 auto_confirm=true
  Then batch 仍为 awaiting_confirm  @pending:G8
  Given confirm.allow_http_auto = false
  When 脚本拿 precheck 返回的 token，带 Bearer 调 POST /api/batches/{id}/confirm
  Then 拒绝，或以 http_auto 身份受开关约束；调用方自报的 confirmer 字段被忽略  @pending:C4

@severity:blocker @FR-15 @FR-53
Scenario: AC-GATE-07 README 约束
  Then README 含 .mcp.json 片段（type http、url http://127.0.0.1:8790/mcp、Authorization Bearer ${JIMENG_BRIDGE_TOKEN}、timeout 120000）
  And README 明写「不要把 confirm_batch 加入 allow 列表」
```

## 12. 作业队列与状态机（§5.5）

```gherkin
@severity:blocker @FR-17
Scenario Outline: AC-Q-01 非法状态转移抛领域错误
  When JobEntity 从 <from> 转到 <to>
  Then 抛出命名领域错误，状态不变
  Examples:
    | from | to |
    | queued | submitting |
    | awaiting_submit_slot | generating |
    | done | submitting |
    | cancelled | preparing |
    | failed | submitting |
  And 每次合法转移都记录 {from, to, at, reason?}

@severity:blocker @FR-17
Scenario: AC-Q-02 preparing 子步骤进度
  When shot02 处于 preparing
  Then GET /api/jobs/{id} 依次显示 set_params → upload → fill → preview，各带进度

@severity:blocker @FR-18
Scenario: AC-Q-03 远端并发 ≤ 3，提交间隔 ≥ 15 s（§9.5）
  Given 已确认 hy3 shot03–shot08 共 6 条，FakeJimeng 让每条渲染 10 min
  When 队列跑到全部 done
  Then 转移日志任一时刻 generating（及 submitting）数 ≤ 3  @pending:G6
  And 相邻两次点击生成的服务端时间差都 ≥ 15 s
  And UI 动作从不重叠（BrowserActor 动作日志没有交叠区间）

@severity:critical @FR-18 @FR-20
Scenario: AC-Q-04 「并行任务已达上限」是背压，不算失败，也不能变成自动重复提交
  Given 已有 3 条 generating，FakeJimeng 对第 4 条注入 concurrency_limit_notice
  When 调度器推进第 4 条
  Then 第 4 条回到 awaiting_submit_slot，reason = 并发上限；不是 failed，队列也未暂停
  And 有 generating 结束后，第 4 条被提交
  And 第 4 条在平台侧只产生 1 条任务，且 generate_clicks 满足 C1 的裁决（默认最严读法：只点击 1 次，即上限提示须在点击前识别）  @pending:C1

@severity:critical @FR-19
Scenario Outline: AC-Q-05 提交中崩溃 → restart_during_submit，绝不自动重提（§9.3）
  Given shot02 已确认，FakeJimeng 挂钩 <时点>，挂钩一触发就强杀 service 进程（taskkill /F）
  When 重启 service，并在 FakeClock 下空转 30 min
  Then shot02 = paused_needs_human(restart_during_submit)
  And generate_clicks 总数 = <点击数>；重启后没有新增点击
  And 恢复语义按 G4 的裁决；未裁决前，resume_job 不得自动点击生成  @pending:G4
  Examples:
    | 时点 | 点击数 |
    | submitting 已落库、点击之前 | 0 |
    | 点击已被 FakeJimeng 记录、提交响应返回之前 | 1 |

@severity:blocker @FR-19
Scenario: AC-Q-06 重启时 generating / downloading 自动续跑
  Given 一条 generating、一条 downloading 的 job，service 被强杀
  When 重启
  Then 两条都恢复轮询 / 下载，最终 done；generate_clicks 不变；下载目标不出现半截文件

@severity:critical @FR-20
Scenario Outline: AC-Q-07 重试边界
  When <注入>
  Then <结果>
  Examples:
    | 注入 | 结果 |
    | upload 瞬时失败 3 次后成功 | 成功（第 4 次尝试 = 3 次重试） |
    | download 连续失败 4 次 | 停止重试，进入暂停或失败（按 G2 裁决），目标路径无文件 |
    | 读回的时长持续不一致 | 重试后 → page_contract_broken |
    | 提交后 FakeJimeng 返回 500 且历史中无记录 | 零重试：generate_clicks = 1，→ paused_needs_human(restart_during_submit) |
  And fill 的重填次数按 G3 裁决（FR-20 说 3 次，FR-31 说 1 次）  @pending:G3

@severity:blocker @FR-22
Scenario Outline: AC-Q-08 取消
  Given job 处于 <状态>
  When POST /api/jobs/{id}/cancel
  Then <结果>
  Examples:
    | 状态 | 结果 |
    | queued / preparing / awaiting_submit_slot | cancelled，generate_clicks 不变，credits_charged = 0 |
    | generating | 停止等待与下载；响应与 UI 都含「积分不会退还」；renders/ 无新文件；终态名按 G12 裁决 |

@severity:blocker @FR-24
Scenario Outline: AC-Q-09 idempotency_key
  Given 首次 precheck(shot02, idempotency_key="k-hy3-ep-01") 于 T0 返回 batch A
  When 在 <时刻> 用同一 key 以 <内容> 再次调用
  Then <结果>
  Examples:
    | 时刻 | 内容 | 结果 |
    | T0 + 1 h | 同内容 | 返回 batch A 的首次结果（同 batch_id 与 token） |
    | T0 + 1 h | 改为 shot03 | HTTP 409 / MCP isError: true |
    | T0 + 25 h | 改为 shot03 | 按新 key 处理，返回新 batch |

@severity:critical @FR-24 @FR-11
Scenario: AC-Q-10 指纹去重与 reroll（§9.6）
  Given shot02 的 job J1 已 done
  When 再次预检 shot02
  Then 条目标注已有 job J1；确认后返回 J1，generate_clicks 不增加  @pending:G5
  When 以 reroll: true 预检并确认
  Then 创建新 job J2，attempt = 2，generate_clicks + 1，renders/ 下新增 1 个文件
  When 对 failed 或 cancelled 的同指纹 job 重新预检
  Then 不去重，直接创建新 job
```

## 13. WebUiBackend（§5.6）

```gherkin
@severity:critical @FR-27
Scenario: AC-WEB-01 canary 只读逐项检查，永不点击生成
  When 运行 canary（批次前、每 30 min、恢复前各触发 1 次）
  Then 逐项结果含：登录标志、创作类型 / 模型 / 参考模式 / 比例·分辨率·数量 / 时长控件、TipTap 编辑器、上传入口、生成按钮、预计积分文本、状态响应已截获并可解析
  And generate_clicks = 0，FakeJimeng 没有收到提交请求
  When 依次对 Outline 行注入 missing_control:{上传入口 | 生成按钮 | 预计积分文本}
  Then 每次都判 page_contract_broken，web 队列暂停

@severity:blocker @FR-27
Scenario: AC-WEB-02 每个 batch 开始执行前必跑 canary
  When 连续确认两个 batch
  Then 每个 batch 的第一条 preparing 之前各有一条 canary 记录

@severity:blocker @FR-28
Scenario: AC-WEB-03 PageMap 集中注册、无坐标点击（静态检查）
  Then 全部 selector 与流程步骤只出现在 jimeng_page__map.py，并标注 web_version
  And 源码中没有 mouse.click(x, y)，也没有带 position 参数的 click

@severity:blocker @FR-29
Scenario: AC-WEB-04 参数逐项读回
  Given FakeJimeng 让第一次设置的时长显示为 15s
  When set_params(duration_s = 22)
  Then 重试后读回 22s 并继续；若持续显示 15s，则 page_contract_broken，不进入 upload

@severity:blocker @FR-30
Scenario: AC-WEB-05 上传前改名为 {name}{ext}
  Given 派生夹具 shot03：第一项为 本镜首帧(上一镜末帧)，解析到 shot02_lastframe.png
  When upload
  Then FakeJimeng 收到的第一个文件名是「本镜首帧.png」，字节 = shot02_lastframe.png；源文件未被改名
  And 等到 FakeJimeng 的上传完成信号后才进入 fill；注入 upload_rejected → upload_rejected

@severity:critical @FR-31
Scenario Outline: AC-WEB-06 填写校验不通过就绝不提交
  Given 注入 <注入>
  When fill
  Then <结果>
  Examples:
    | 注入 | 结果 |
    | 第一次失焦后追加多余文字 | 清空重填 1 次，校验通过 |
    | 每次都追加多余文字 | fill_mismatch，generate_clicks = 0 |
    | @ 候选列表顺序被打乱，点错主体 | mention 序列不等 → 重填；仍不等 → fill_mismatch |

@severity:blocker @FR-2 @FR-31
Scenario Outline: AC-WEB-07 负向提示词策略
  Given FakeJimeng <负向框>，video.negative_prompt = "platform_field_or_omit"
  When 填写 shot02
  Then <结果>，且正向编辑器永远不含反向提示词
  Examples:
    | 负向框 | 结果 |
    | 有负向输入框 | 负向框文本 = 反向提示词围栏正文 |
    | 没有负向输入框 | 省略，job 带 warning |

@severity:blocker @FR-32
Scenario: AC-WEB-08 预演截图与页面积分入库
  When preview
  Then job artifacts 有全页 + composer 两张截图和页面预计积分；GET /api/artifacts/{job_id}/{name} 可取回

@severity:critical @FR-33
Scenario Outline: AC-WEB-09 截获不到提交响应时对账
  Given 注入 suppress_submit_response，FakeJimeng 历史中 <历史>
  When 已确认的 shot02 被提交
  Then <结果>，generate_clicks = 1
  Examples:
    | 历史 | 结果 |
    | 有一条晚于提交时刻、prompt 前缀为 shot02 的记录 | generating，platform_task_id = 该记录 id |
    | 没有这样的记录 | paused_needs_human(restart_during_submit) |

@severity:blocker @FR-34
Scenario: AC-WEB-10 被动状态观察
  When FakeJimeng 的 get_history_queue_info / get_history_by_ids 响应推进到 37%、排队第 2、完成
  Then job 依次记录这些进度与状态
  When 注入 malformed_history_body，连续次数超过阈值
  Then page_contract_broken（队列级），job 本身不 failed；body 读取失败有计数  @pending:G7

@severity:critical @FR-35 @FR-45
Scenario Outline: AC-WEB-11 下载校验 + 原子落盘
  Given FakeJimeng 下发 <文件>
  When 下载 shot02
  Then <结果>
  Examples:
    | 文件 | 结果 |
    | 22 s、16:9、sha256 S1 的 mp4 | 目标文件 sha256 = S1；ffprobe 读出 22 s、16:9；credits_charged 取自「详细信息」 |
    | 传到一半被截断 | 目标路径无文件，临时文件被清理，最多重试 3 次 |
    | 8 s 的 mp4 | 校验失败，目标路径无文件（时长容差按 G17 裁决） |
  And 任何时刻，目标路径上不会出现大小 < 最终大小的文件

@severity:blocker @FR-36
Scenario: AC-WEB-12 失败现场只在失败或暂停时保留
  Then paused / failed 的 job 在库里有截图、DOM 快照、trace 片段的路径且文件存在
  And done 的 job 只有 FR-32 的预演截图，没有 DOM 快照和 trace

@severity:blocker @FR-37
Scenario: AC-WEB-13 浏览器丢失
  Given 2 条 generating
  When 注入 close_context
  Then browser_lost → web 队列暂停 → context 重建 → 检查登录 → 两条 generating 对账后恢复轮询；generate_clicks 不变
```

## 14. DreaminaCliBackend（§5.7）

```gherkin
@severity:critical @FR-38
Scenario: AC-CLI-01 只调用文档化命令，参数以列表传入、不经 shell
  Given 资产块 prompt 含字面量「"; del C:\x & echo 1」
  When 执行该 CLI job
  Then fake dreamina 记录的 argv 中，prompt 是完整的单个元素，且没有产生任何副作用文件
  And 整个测试套件的 argv 子命令只出现 text2image、image2image、query_result、list_task、user_credit、version

@severity:blocker @FR-39
Scenario: AC-CLI-02 CLI 生命周期
  When 确认 c2-1
  Then 生成命令返回 submit_id 的同时 job 持久化为 generating；先下载到临时目录，按 FR-35 校验后才进入 _candidates/c2-1/

@severity:blocker @FR-40
Scenario: AC-CLI-03 CLI 未登录
  Given fake dreamina = not_logged_in
  When 执行 c2-1
  Then cli_login_required，CLI 队列暂停，UI 提示用户自己运行 `dreamina login`
  And argv 日志里从未出现 login；web 队列照常

@severity:blocker @FR-38
Scenario: AC-CLI-04 非零退出码与合规确认映射
  Then fake dreamina 以 AigcComplianceConfirmationRequired 退出 → compliance_confirmation_required；以未知非零码退出 → 映射到对应暂停原因，且不自动重提

@severity:blocker @FR-41
Scenario: AC-CLI-05 版本检查
  Given fake dreamina version = 1.4.4，cli.min_version = 1.4.5
  When service 启动
  Then GET /api/session 的 cli.version = 1.4.4，并带 warning；service 正常可用
```

## 15. 产物与记录（§5.8）

```gherkin
@severity:blocker @FR-42
Scenario: AC-OUT-01 视频命名，永不覆盖
  Given shot02 video.count = 2
  Then 产出 shot02_{ts}_1.mp4、shot02_{ts}_2.mp4
  Given renders/ 下已有与本次同名的文件
  Then 该文件字节不变，本次不覆盖

@severity:critical @FR-44
Scenario: AC-OUT-02 sidecar 字段齐全，不含机密
  When AC-F3-01 完成
  Then shot02_{ts}.mp4.jimeng.json 含：
    | 字段 | 期望 |
    | job_id / batch_id / backend | 与库一致 / web |
    | source | {type: shot, path: …/shot02/shot02.md, block_key: null} |
    | prompt_sha256 / negative_prompt_sha256 | = AC-IN-01 的两个 sha256 |
    | references | 4 项：bg11-1 image(path, sha256)、砌炉的老人 entity=hy3_主角、p2-1、p3-1 |
    | params | {seedance2.5, 16:9, 22, 720p, 1, 全能参考} |
    | platform_task_id / credits_estimated{static,page} / credits_charged | 非空 |
    | submitted_at / finished_at / confirmer | ISO 时间 / ui_human |
    | web_version / browser_version | 非空 |
    | output | {sha256 = 文件 sha256, size, duration_s: 22, width, height} |
  And sidecar、.data/logs/、bridge.db 中都搜不到 test-token-7f3a

@severity:critical @FR-45
Scenario: AC-OUT-03 字节原样保存
  Then 落盘文件与 FakeJimeng 下发文件逐字节相等（含嵌入的元数据 / 隐式 AI 标识区块）

@severity:blocker @FR-46
Scenario: AC-OUT-04 生成历史与余额对账
  When GET /api/history?drama=huangye_shenghuo/hy3&shot=shot02
  Then 列出预估与实扣积分、每日合计；可按资产主体 c2_獾、按日期筛选
  And batch 记录中有开始与结束各读一次的 commerce 余额（CLI 为 user_credit）
```

## 16. HTTP API / MCP / UI / 通知（§5.10–§5.13）

```gherkin
@severity:blocker @§5.10
Scenario: AC-API-01 每个 route 恰好对应一个 Query / Command（静态 + 运行时）
  Then §5.10 的 25 行路由全部存在，每个 handler 只调用表中那一个方法
  And apps/ 不 import libs/infrastructure 或 libs/domain；每个 route 模块的 provider 都在 container 中

@severity:blocker @§5.10
Scenario: AC-API-02 serve_static=True 下，状态变更路由没有被静态挂载遮蔽
  When 对全部 POST / PUT 路由各发一次合法请求（prod 模式）
  Then 没有一个返回 405

@severity:blocker @§5.10
Scenario: AC-API-03 统一错误形状与剧参数编码
  When GET /api/dramas/huangye_shenghuo%2Fhy3/config
  Then 返回 hy3 的 config
  When 触发任一业务错误
  Then body = {error_code, message, hint, config_key?}

@severity:critical @§5.10 @NFR-安全
Scenario: AC-API-04 artifact 路径沙箱
  When GET /api/artifacts/{job_id}/..%2F..%2Fbridge.db，以及 /api/artifacts/{job_id}/C:%5CWindows%5Cwin.ini
  Then 拒绝，响应不含文件内容

@severity:blocker @FR-51
Scenario: AC-MCP-01 工具集
  Then tools/list 恰为 session_status、precheck_batch、confirm_batch、wait_jobs、list_jobs、cancel_job、resume、browser_step、entities、get_screenshot
  And precheck_batch 接受 shot 路径、{card_path, key}、原始请求三种 item

@severity:blocker @FR-52 @NFR-性能
Scenario: AC-MCP-02 全部工具 ≤ 90 s 返回；wait_jobs 有进度通知
  Given FakeJimeng 让 shot02 渲染 10 min
  When 调用 wait_jobs
  Then 90 s 内返回当前快照 + 建议的下一步，期间每 ≤ 30 s 收到一次 notifications/progress
  And 其余 9 个工具在最慢注入（上传慢、canary 慢）下也都在 90 s 内返回

@severity:blocker @FR-52
Scenario: AC-MCP-03 返回形状
  Then 每个工具的 structuredContent 与 text 内容的 JSON 相等
  And get_screenshot 返回截图路径 + 长边 ≤ 768 px 的缩略图，不返回原图字节

@severity:blocker @FR-52
Scenario: AC-MCP-04 业务错误可照做
  When 对未确认 batch 调 browser_step(op="submit")
  Then isError: true，建议含确认页 URL
  When 删除 c1 的 override 后预检 shot02
  Then isError 条目建议含「在 config 填写 entities.overrides."c1_砌炉的老人"」或「去主体对账页创建」

@severity:blocker @FR-52
Scenario: AC-MCP-05 不使用 elicitation 与 MCP tasks
  Then initialize 响应的 capabilities 不声明 elicitation / tasks，任何工具都不发 elicitation 请求

@severity:blocker @FR-53
Scenario: AC-MCP-06 接入片段可用
  When 按 README 的 .mcp.json 片段（带正确 token）连接 /mcp
  Then session_status 成功；去掉 Authorization 头后返回 403

@severity:blocker @FR-54 @FR-55
Scenario Outline: AC-UI-01 七个页面在真实浏览器里渲染（make run 静态构建，单一运行模式）
  When 打开 <页面>
  Then 成功态：<结构断言> 可见，consoleErrors 为空
  When 该页主数据接口被替身返回 500
  Then 显示错误态文案，main 非空（不是白屏）
  Examples:
    | 页面 | 结构断言 |
    | 会话 | web 登录状态、canary 逐项列表、browser_version、CLI 版本与余额、「运行 canary」按钮 |
    | 剧 config | 剧列表中 huangye_shenghuo 折叠 hy1–hy4；表单 + TOML 原文视图；参考项解析预览里有 shot02 的 4 项 |
    | 批次确认 | 条目的缩略图、主体 hy3_主角、参数、static / page 积分、合计、「确认并开始」 |
    | 队列看板 | 按状态分列；子步骤进度；暂停原因 + 截图 |
    | 历史与积分 | 筛选器；预估 / 实扣；每日合计；候选图网格 +「选定」 |
    | 主体对账 | 三态分组；missing 项的「创建」按钮 |
    | 全局设置 | global.toml 表单 |

@severity:blocker @FR-12 @FR-54 @FR-55
Scenario: AC-UI-02 批次确认页与 API 一致（§9.12）
  Then 页面合计积分 = GET /api/batches/{id} 的合计；error 条目的确认控件被禁用；点「确认并开始」后 confirmer = ui_human

@severity:blocker @FR-54
Scenario: AC-UI-03 剧 config 页
  Then needs_confirmation 的项置顶并标黄；保存前本地 schema 校验会阻止非法值；遇到 409 显示冲突提示

@severity:blocker @FR-22 @FR-54
Scenario: AC-UI-04 队列看板的取消文案
  When 对 generating 的 job 点「取消」
  Then 先弹出二次确认，文案含「提交后取消不退积分」；对 queued 的 job 不出现该文案

@severity:blocker @FR-43 @FR-46 @FR-54
Scenario: AC-UI-05 历史页选定候选
  When 在候选网格对 c2-1 的某张点「选定」
  Then 效果与 AC-F5-01 的 promote 相同

@severity:critical @FR-48 @FR-54 @NFR-安全
Scenario: AC-UI-06 主体页三态与 API 一致；全局设置页不展示机密
  Then 主体页三态计数 = GET /api/entities/reconcile
  And 全局设置页 DOM 与 GET /api/config/global 响应中都不含 test-token-7f3a，也没有 token 输入框

@severity:blocker @FR-55
Scenario: AC-UI-07 浅色主题
  Then 构建产物 CSS 只有 color-scheme: light，body / 侧栏 / 面板 / 按钮上没有 prefers-color-scheme: dark 覆盖

@severity:blocker @FR-56
Scenario: AC-NTF-01 toast 触发时机与深链
  Then ToastClient 在队列级暂停、batch 全部完成、需要登录时各被调用 1 次，每次带对应 UI 页面 URL（点击后打开页面为 @manual）

@severity:blocker @FR-56
Scenario: AC-NTF-02 toast 失败不影响作业
  Given ToastClient 每次都抛异常
  When 执行 AC-F4-01
  Then 日志记录 toast 失败，队列暂停、恢复、job done 与 AC-F4-01 完全一致
```

## 17. NFR：安全、账号风险、可靠性、性能、可测性

```gherkin
@severity:critical @NFR-安全
Scenario: AC-SEC-01 只绑定 127.0.0.1
  Then 监听地址只有 127.0.0.1:8790；从本机非回环网卡 IP 连接失败

@severity:critical @NFR-安全
Scenario Outline: AC-SEC-02 Host / Origin / token 闸门（/api/* 与 /mcp 都测，prod 模式）
  When 请求 <路径>，Host = <Host>，Origin = <Origin>，Authorization = <Auth>
  Then 状态码 = <code>
  Examples:
    | 路径 | Host | Origin | Auth | code |
    | /api/jobs | evil.example:8790 | (无) | Bearer test-token-7f3a | 403 |
    | /api/jobs | 192.168.1.5:8790 | (无) | Bearer test-token-7f3a | 403 |
    | /api/jobs | 127.0.0.1:8790 | http://evil.example | (无) | 403 |
    | /api/jobs | 127.0.0.1:8790 | http://localhost:5173 | (无) | 403 |
    | /api/jobs | 127.0.0.1:8790 | http://127.0.0.1:8790 | (无) | 200 |
    | /api/jobs | localhost:8790 | http://localhost:8790 | (无) | 200 |
    | /mcp | 127.0.0.1:8790 | (无) | (无) | 403 |
    | /mcp | 127.0.0.1:8790 | (无) | Bearer wrong | 403 |
    | /mcp | 127.0.0.1:8790 | (无) | Bearer test-token-7f3a | 200 |
  # 没有 Vite 代理之类的改写头层（单一运行模式）；5173 这一行证明未广告的 dev server 形态被拒

@severity:critical @NFR-安全
Scenario: AC-SEC-03 token 不外泄
  When 跑完整个测试套件
  Then .data/logs/**、bridge.db、所有 *.jimeng.json、artifacts/、API 与 MCP 响应中都搜不到 test-token-7f3a

@severity:critical @NFR-安全
Scenario Outline: AC-SEC-04 写入沙箱
  When 以 output_dir = <目标> 预检原始请求
  Then error，盘上无写入
  Examples:
    | 目标 |
    | projects/jimeng_web_bridge/config |
    | ai_videos/../projects |
    | 指向 ai_videos 之外的 junction / symlink（无权限时跳过并注明原因） |

@severity:blocker @NFR-账号风险
Scenario: AC-RISK-01 README 首屏风险告知
  Then README 首屏写明：用户协议 5.1 禁止自动化接入；付费协议 6.5 / 8.2 可作废权益或封号；本人账号、本机、自用，风险自担
  And 写明素材按 9.3 授权平台优化模型，写实真人素材可能被拒

@severity:critical @NFR-账号风险 @§2
Scenario: AC-RISK-02 零对抗检测、零接口重放（静态 + 运行时）
  Then 依赖清单没有 stealth / undetected / 验证码求解类包；源码不改 navigator.webdriver、不加 --disable-blink-features=AutomationControlled、不注入指纹脚本
  And 运行时 FakeJimeng 收到的生成 / 历史 / 主体接口请求，发起方全部是页面脚本；service 从未用 route.fulfill / 改写请求篡改这些接口
  And 源码中没有去水印或剥离元数据的处理

@severity:critical @NFR-可测性
Scenario: AC-RISK-03 自动化测试绝不触碰真实站点与真实 CLI
  Then make test 全程出站拦截器命中数 = 0；~/bin/dreamina 的调用数 = 0（进程审计）
  And make canary 不属于 make test

@severity:blocker @NFR-账号风险
Scenario: AC-RISK-04 固定节奏、单账号单 profile
  Then 调度器不引入随机抖动（同一输入两次运行的提交间隔序列相同）；全局只有一个 persistent context 与一个 profile

@severity:critical @NFR-部署
Scenario: AC-NFR-01 启动冒烟（development.md §4）
  When make run
  Then 进程启动无异常；GET /api/health = 200；GET /api/session 形状完整；GET / 返回构建好的 UI index

@severity:critical @NFR-可靠性
Scenario: AC-NFR-02 WAL 与唯一写者，任何重启都不自动重复提交
  Then bridge.db 的 journal_mode = wal
  And 在 AC-Q-05、AC-Q-06、AC-WEB-13 连跑 3 次随机时点强杀的混沌测试后，每个 job 的平台任务数 ≤ 1

@severity:blocker @NFR-性能
Scenario: AC-NFR-03 硬性能预算
  Given 库中预置 1000 条 job
  Then GET /api/jobs、/api/jobs/{id}、/api/history、/api/batches/{id} 各 200 次，p95 ≤ 500 ms
  And UI 首屏（本机、已构建）≤ 2 s；所有 HTTP / MCP 调用 ≤ 90 s（与 AC-MCP-02 共享）

@severity:blocker @NFR-部署
Scenario: AC-NFR-04 入口与依赖
  Then Makefile 有 run / ui-build / test / canary；不调用 uv；pip + .venv 可装可跑
  And README 不宣传 Vite dev server 模式（e2e profile 数 = 运行模式数 = 1）

@severity:blocker @NFR-可观测
Scenario: AC-NFR-05 结构化日志
  Then .data/logs/ 下每行是合法 JSON；每个 job 的状态转移可在库中完整回放

@manual
Scenario: AC-NFR-06 人工 walkthrough（validation.requires_manual_walkthrough）
  Then 用户登录后跑 make canary，对真实站点逐项通过、全程不点生成（§9.13）
  And 在真实 Windows 桌面上点 toast，打开 UI 对应页面
  And 七个页面的视觉层级、对比度、焦点可见性过一遍人工检查
  And 在本机 Claude Code 验证 .mcp.json 的 timeout 120000 生效（§10 Q9）；stage-6 探针核实会员下载无水印（§10 Q1）
```

## 18. Traceability matrix

| FR | 场景 |
|---|---|
| FR-1 | AC-F2-06, AC-PRE-02, AC-PRE-03, AC-GATE-05, AC-Q-03, AC-F4-04, AC-CLI-05 |
| FR-2 | AC-F2-01, AC-F2-02, AC-F2-06, AC-PRE-04, AC-PRE-07, AC-WEB-07 |
| FR-3 | AC-F2-01, AC-F2-02, AC-F2-03, AC-F2-04 |
| FR-4 | AC-F2-05, AC-F2-06, AC-F2-07 |
| FR-5 | AC-F2-08 |
| FR-6 | AC-F3-01, AC-IN-01 |
| FR-7 | AC-IN-07, AC-F3-02, AC-SEC-04 |
| FR-8 | AC-F3-01, AC-IN-01, AC-IN-02, AC-IN-03, AC-IN-04 |
| FR-9 | AC-F5-01, AC-F5-02, AC-F5-03 |
| FR-10 | AC-F2-04, AC-IN-02, AC-IN-05, AC-IN-06 |
| FR-11 | AC-PRE-01…07, AC-PRE-09, AC-F2-02, AC-F6-04, AC-Q-10 |
| FR-12 | AC-PRE-08, AC-UI-02 |
| FR-13 | AC-F3-01, AC-PRE-09, AC-GATE-02, AC-GATE-03 |
| FR-14 | AC-F3-01, AC-F3-03, AC-GATE-02, AC-GATE-03, AC-GATE-04 |
| FR-15 | AC-F3-02, AC-F3-03, AC-GATE-05, AC-GATE-06, AC-GATE-07 |
| FR-16 | AC-GATE-01, AC-F7-01 |
| FR-17 | AC-Q-01, AC-Q-02, AC-F3-01 |
| FR-18 | AC-Q-03, AC-Q-04, AC-F4-01, AC-F7-02 |
| FR-19 | AC-Q-05, AC-Q-06, AC-NFR-02 |
| FR-20 | AC-Q-07, AC-Q-04, AC-F4-03 |
| FR-21 | AC-F4-01, AC-F4-03, AC-F4-04 |
| FR-22 | AC-Q-08, AC-UI-04 |
| FR-23 | AC-F4-01, AC-F4-02 |
| FR-24 | AC-Q-09, AC-Q-10 |
| FR-25 | AC-F1-01, AC-F1-03 |
| FR-26 | AC-F1-01, AC-F1-02 |
| FR-27 | AC-F1-01, AC-F4-02, AC-WEB-01, AC-WEB-02 |
| FR-28 | AC-WEB-03 |
| FR-29 | AC-F3-01, AC-WEB-04 |
| FR-30 | AC-F3-01, AC-WEB-05 |
| FR-31 | AC-F3-01, AC-IN-01, AC-WEB-06, AC-WEB-07, AC-PRE-07 |
| FR-32 | AC-WEB-08, AC-F7-01 |
| FR-33 | AC-F3-01, AC-GATE-01, AC-WEB-09, AC-F7-02 |
| FR-34 | AC-WEB-10 |
| FR-35 | AC-F3-01, AC-WEB-11（「会员无水印」仅 @manual） |
| FR-36 | AC-WEB-12 |
| FR-37 | AC-WEB-13 |
| FR-38 | AC-CLI-01, AC-CLI-04, AC-F5-01, AC-F4-04 |
| FR-39 | AC-CLI-02, AC-F5-01 |
| FR-40 | AC-CLI-03, AC-F4-04 |
| FR-41 | AC-CLI-05 |
| FR-42 | AC-OUT-01, AC-F3-01, AC-PRE-06 |
| FR-43 | AC-F5-01, AC-F5-03, AC-UI-05 |
| FR-44 | AC-OUT-02, AC-F5-01 |
| FR-45 | AC-OUT-03, AC-WEB-11 |
| FR-46 | AC-OUT-04, AC-UI-05 |
| FR-47 | AC-F6-01 |
| FR-48 | AC-F6-01, AC-UI-06 |
| FR-49 | AC-F6-02, AC-F6-03, AC-F6-05 |
| FR-50 | AC-F6-04 |
| FR-51 | AC-MCP-01, AC-F3-01, AC-F3-03, AC-GATE-06 |
| FR-52 | AC-MCP-02, AC-MCP-03, AC-MCP-04, AC-MCP-05, AC-IN-03 |
| FR-53 | AC-MCP-06, AC-GATE-07 |
| FR-54 | AC-UI-01…06, AC-F2-07 |
| FR-55 | AC-UI-01, AC-UI-02, AC-UI-07, AC-F6-02 |
| FR-56 | AC-NTF-01, AC-NTF-02, AC-F1-01, AC-F4-01 |
| §5.10 路由表 | AC-API-01…04 |
| NFR 部署 / 可靠性 / 性能 / 可观测 | AC-NFR-01…05, AC-MCP-02 |
| NFR 安全 | AC-SEC-01…04, AC-API-04, AC-CLI-01, AC-IN-06, AC-IN-07, AC-UI-06 |
| NFR 账号风险 / 可测性 | AC-RISK-01…04 |
| §9 验收 1–13 | 1→AC-F3-01 · 2→AC-GATE-01…04 · 3→AC-Q-05 · 4→AC-F4-01/03 · 5→AC-Q-03/04 · 6→AC-Q-09/10 · 7→AC-F2-01/05/06/07 · 8→AC-IN-03 · 9→AC-F5-01, AC-CLI-03 · 10→AC-MCP-02/04 · 11→AC-SEC-02, AC-IN-07 · 12→AC-UI-01/02 · 13→AC-NFR-06 |

**只能部分离线验证的 FR**：
- FR-30：上传完成信号，依赖 §10 Q2。
- FR-33：提交响应里的任务标识字段，依赖 §10 Q3。
- FR-34：解析器 schema 依赖 §10 Q3，失败阈值没有取值（G7）。
- FR-35：会员无水印、下载入口，依赖 §10 Q1。
- FR-1：`model_limits` 数值依赖 §10 Q5。
- FR-56：toast 点击后打开页面。

以上各项的离线场景都针对 FakeJimeng 假设的契约，因此 FakeJimeng 必须在 stage-6 探针后同步真实站点（见 G25）。

## 19. §2 Out-of-scope 与 observe-only 清单（general.md §6：请用户确认「不在验证闸门内」是本意）

| # | §2 out-of-scope 条目 | 验证姿态 | 与其他章节冲突？ |
|---|---|---|---|
| 1 | 全能参考之外的全部模式（首尾帧、智能多帧等）；承接首帧按上传项处理 | 反向验证：AC-F2-06（reference_mode=首尾帧 被拒）、AC-IN-02（first_frame 走上传） | 无 |
| 2 | 网页端图片生成 | 无正向场景 | **C2 critical**：FR-1 `routing.image` 允许取 `web` |
| 3 | 伪造 / 重放内部接口、任何对抗检测 | AC-RISK-02（critical） | 无（FR-35「结果 URL 下载」须证明是 CDN 直链，不是接口重放，列入 G25） |
| 4 | 去水印、剥离元数据 | AC-OUT-03、AC-RISK-02 | 无（「会员无水印原片」是平台权益，不是去水印） |
| 5 | 多账号、远程部署、对 127.0.0.1 以外开放 | AC-SEC-01/02、AC-F2-06（host=0.0.0.0 被拒）、AC-RISK-04 | 无 |
| 6 | 自动改写 prompt 重提；任何形式的自动重复提交 | AC-F4-03、AC-Q-05、AC-Q-07、AC-NFR-02 | **C1 critical**：FR-18 背压回到 awaiting_submit_slot 后再次提交 |
| 7 | 自动改名 / 删除即梦主体 | AC-F6-04（critical） | 无 |
| 8 | 定版、拼接、字幕、BGM | 不测 | 未决：§10 Q8 `MediaRenamer` 改名 renders/ 会让 sidecar 失配——跨项目兼容，无验收场景，请用户确认 |
| 9 | 不回溯改旧剧 shot md，旧写法走 config override | AC-IN-03 | **C3 critical**：FR-8 把旧写法定为无条件错误，prompt 又逐字节不改 |
| 10 | Windows Service 形态 | 不测；AC-NFR-06 只在交互桌面人工验证 | 无 |
| — | 单一运行模式（§6，不宣传 Vite dev server） | AC-NFR-04、AC-SEC-02 的 5173 行 | 无（e2e profile 数 = 1） |

| Observe-only / 尽力而为（越界 = `warning`，不 halt） | 来源 |
|---|---|
| 单 job 准备阶段（set_params → preview）≤ 3 min | §6 性能 |
| toast 送达（失败只记日志） | FR-56 |
| 静态估算与页面积分偏差 > 20% 只高亮 | FR-12（与 G10 有张力：确认后花费可能超出确认额） |
| CLI 版本低于 min_version 只 warning | FR-41 |
| 主体快照超过 24 h 只 warning | FR-11.6 |
| 疑似写实真人只 warning | FR-49 |
| 负向框不存在时省略并 warning | FR-31 |

硬预算（越界 = `blocker`）：HTTP / MCP ≤ 90 s；查询 p95 ≤ 500 ms（1000 条 job）；UI 首屏 ≤ 2 s。

## 20. Spec gaps / carve-outs to surface

| ID | 严重度 | 缺口 | 建议修法 |
|---|---|---|---|
| **C1** | critical | FR-18「并行任务已达上限 → 放回 awaiting_submit_slot 等待」若在点击生成**之后**才识别，同一 job 会被第二次点击，违反 §2 #6、FR-20 零自动重试、§9.3「只点击一次」 | 规定上限在点击前识别（读 `get_history_queue_info` 或页面提示）；如果点击后才出现，必须证明平台没有建任务（无提交响应、历史无新记录）才回到等待，否则 → `paused_needs_human`；每个 job 记 `submit_attempts` |
| **C2** | critical | §2 排除网页端图片生成，FR-1 却允许 `routing.image = web` | v1 schema 把 `routing.image` 限为 `cli`；或能力矩阵声明 web 不具备 image 能力，预检报错 |
| **C3** | critical | §2 说旧写法走 config override 解决；FR-8 把 `=>@2` 和无括号写法定为无条件预检错误，FR-8/31 又要求 prompt 逐字节不改。真实旧剧 rexue_gaoxiao（20 个 shot `=>@1`）、wushen_juexing（`名=>`）、xianjian_yi_mv（无括号）没有任何 config 路径可以跑通 | 明确 v1 不支持旧剧，从 §2 删掉「通过 override 解决」；或新增 `references.legacy_syntax = "reject" \| "normalize_slot"`，并规定填写时如何处理 `@` 后的数字（且不改盘上 md） |
| **C4** | critical | 脚本带 bearer token 调 `POST /api/batches/{id}/confirm` 时 confirmer 怎么定没写，可能绕过 `allow_http_auto` 与预算；§5.10 也没写 `auto_confirm` 挂在哪个路由 | confirmer 由认证通道推导（同源 UI = ui_human，/mcp = mcp，bearer HTTP = http_auto，受开关与预算约束），忽略调用方自报 |
| G1 | low | §9.1「4 个参考项按 stem 上传」与 FR-30「上传非主体项」矛盾：shot02 实为 3 个上传 + 1 个主体 mention | 改 §9.1 措辞 |
| G2 | high | FR-21 作业级原因哪些是终态 `failed`、哪些是 `paused_needs_human` 没写（只有 moderation_reject、wait_timeout、restart_during_submit 可推出）；下载重试耗尽后的状态也未定义 | 补表：moderation_reject / real_face_rejected → failed；upload_rejected / fill_mismatch / wait_timeout / restart_during_submit / download_exhausted → paused_needs_human |
| G3 | medium | FR-20 说 fill 最多重试 3 次，FR-31 说清空重填 1 次 | 以 FR-31 为准，修改 FR-20 |
| G4 | high | `restart_during_submit` 怎么恢复没写：`resume_job` 如果直接重新提交，就等于自动重提 | 只允许 UI 人工二选一：「平台已有任务（填 task id）→ generating」或「确认未提交 → awaiting_submit_slot」，记为 ui_human 的一次新授权 |
| G5 | high | FR-24 指纹含 `output_target`；若它是带时间戳的最终文件名，指纹永不重复，§9.6 无法成立 | 规定 output_target 进入指纹时取目录 + 命名模板，不取解析后的文件名 |
| G6 | medium | FR-18 只对 `generating` 计上限，`submitting` 中的 job 不计，可能出现第 4 条同时渲染 | 上限对 `submitting ∪ generating` 计数 |
| G7 | medium | FR-5 要求阈值一律来自 config，但 token 30 min、幂等 24 h、快照 24 h、重试 3 次、90 s / 30 s / 768 px 都写死；FR-34「连续失败阈值」没有取值，无法测试 | 补 config 键；或在 FR-5 明确「协议常量」豁免清单，并给 FR-34 定值 |
| G8 | high | `auto_confirm` 挂在哪个路由；MCP 是否必须拒绝；「当日」按哪个时区切日 | 挂在 `POST /api/batches`；MCP 忽略并报错；按本机本地时区 00:00 切日 |
| G9 | medium | 含 error 条目的 batch 能否确认（全拒还是只确认 ok 条目）不明 | 有任一 error 就拒绝 confirm，或不签发 token |
| G10 | high | token 只签入静态合计积分；确认后预演读到的页面积分可能远超确认额，却没有闸门 | 页面积分 > 确认额 × (1 + warn_pct) 时，作业级暂停 `estimate_exceeds_confirmed` |
| G11 | high | FR-49 创建主体要确认，但 §5.10 只有 `POST /api/entities`，没有 token 两段式；FR-16 只约束 job | 主体创建复用 batch 闸门（item kind = entity_create），或增加 precheck / confirm 两段 |
| G12 | medium | FR-22 提交后取消的终态名未定义；在 `submitting` 期间发起取消怎么处理也未定义 | 终态 `cancelled` + `credits_forfeited: true`；submitting 期间取消按「提交后」处理，在下一个检查点生效 |
| G13 | low | 交叉引用写错：FR-35「写 sidecar（FR-45）」应为 FR-44；FR-39「FR-44 的候选目录」应为 FR-43 | 改编号 |
| G14 | medium | 图片 sidecar 写在候选图、promote 后的 `{key}.png`，还是两者都写；归档时旧 sidecar 怎么处理，均未定义 | 候选下载时写 sidecar；promote 写 `{key}.png.jimeng.json`（含 `promoted_from`）；归档时旧 sidecar 随图一起移走 |
| G15 | high | `参考:` 里不符合任何已知写法的 token（wushen_juexing `裴知秋=>`）可能被静默解析成 0 项 | 加不变量：prompt 中 `=>@` 出现次数 = references 数；`参考:` 行里出现任何 `=>` 但未解析 → error |
| G16 | low | 默认 rules 漏掉真实 label：`道具参考图`（8 处）、`上一镜末帧·水面` 类带后缀的写法（3 处）、`道家手印参考图`、`大地裂痕参考图` | 默认规则加 `上一镜末帧*`，并在末尾加兜底 `*参考图` → image |
| G17 | medium | FR-35 ffprobe「预期时长」没有容差 | 新增 config 键，例如 `download.duration_tolerance_s = 0.5` |
| G18 | low | FR-11.5「字数」计量单位未定义（码点 / CJK / 去空白）。hy3 各镜 ≤ 3693 码点，当前不构成风险 | 定义为围栏正文的 Unicode 码点数，与格式契约 K10 对齐 |
| G19 | medium | 队列级暂停时，未触发暂停的 job 状态怎么变没写；generating job 是否继续观察和下载也没写 | 暂停是 per-backend 队列属性；只有触发暂停的 job 进入 paused；其余保持原状态不前进；被动观察与下载照常 |
| G20 | low | `price_table ×时长` 对图片没有意义 | 图片按张计价 |
| G21 | medium | FR-9 没说资产块怎么判断出图还是出视频：`c1-2_砌炉的老人turntable` 是视频块，会被误路由到 text2image | 按 key 对应的已有产物扩展名，或 config 逐块 `kind` 判定；视频块在 v1 预检直接报错 |
| G22 | low | FR-10 文字只排除系列下的 `_` 目录；实际 drama_ref.py 两级都排除 `_`，而 `notes/` 在两边都会被判为平铺剧 | FR-10 改为「两级 `_` 前缀都不是剧」；`list_dramas` 过滤不含 `5_6_分镜与prompt` / `episodes` 的目录（或在 config 中列排除项） |
| G23 | high | 确认后、上传前 shot md 或参考文件被改动，没有复核，花的是未确认的内容 | 执行时重算 prompt 与参考项的 sha256，与确认摘要比对，不一致 → 作业级暂停 `source_changed_since_confirm` |
| G24 | medium | FR-3「期望主体名与即梦现有主体不一致」的判定规则未定义（§9.7 依赖它） | 例如：快照中存在 `{abbrev}_*` 且未被任何卡映射、而期望名不在快照 → needs_confirmation |
| G25 | blocker（development.md §10） | FR-34 / FR-47 的响应解析器与 CLI JSON 解析只有 FakeJimeng 手写样本，违反「解析器要用真实上游输出测试」 | stage-6 只读探针把 `get_history_queue_info`、`get_history_by_ids`、`dreamina_subject/get` 响应，以及 `dreamina version` / `user_credit` / `query_result` 输出脱敏后存入 `tests/fixtures/real_responses/`；解析器单测跑在这些样本上，并据此校准 FakeJimeng |
