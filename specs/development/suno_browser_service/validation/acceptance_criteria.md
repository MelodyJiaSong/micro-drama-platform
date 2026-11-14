---
worker_id: level-specialist-validation
stage: 5
role: level-specialist
level: acceptance_criteria
status: complete
blockers: []
confidence: high
---

# 验收条件

全部为待执行场景；FR 编号对应 spec。

```gherkin
Scenario: AC-01 程序提交并取得音乐（FR1、3、7）
  Given 已配置鉴权、可用浏览器会话及可写审计归属
  When 程序带 Idempotency-Key 提交 prompt、instrumental、format 和合法 target
  Then API 返回可查询 job ID，后台输入正确内容且只点击一次 Create
  And 官方菜单导出的本次歌曲可由文件 API 获取，大小和哈希与落盘文件一致

Scenario: AC-02 并发幂等与单账号串行（FR1、2）
  Given 多个调用者并发提交同键同参数，以及两个不同任务
  When 服务排队执行并在完成后重启
  Then 同键请求始终关联一个持久任务，同键不同参数被拒绝
  And 单账号任意时刻最多一个浏览器任务执行，重启不重新生成已提交任务

Scenario: AC-03 提交结果未知时安全恢复（FR2、6）
  Given submitting 已持久化，Create 前后发生崩溃或连接超时
  When 服务重启或调用者重复请求
  Then 任务保留待处理状态，Create 不再自动调用
  And 用户提供已知 song URL 后只补收官方导出，保留已完成文件

Scenario: AC-04 外部调用先审计（FR6、8）
  Given 任一浏览器连接、准备、导航、提交、轮询或下载即将执行
  When RequestLog 无法先持久写入，或 target 无合法归属
  Then 本次外部动作不发生，任务保留可解释错误
  And 成功和失败结果均使用对应 request_id，费用未知不填写为已知零

Scenario: AC-05 登录或页面障碍（FR3、4、7）
  Given 登录失效、验证码、下载受限、DOM 不匹配或歌曲归属歧义
  When 后台遇到该情况
  Then 任务暂停并说明人工处理原因，不绕过障碍或误收歌曲

Scenario: AC-06 授权与文件边界（FR5）
  Given 服务默认只监听 127.0.0.1
  When 请求缺失或使用错误 Bearer，或尝试跨 job / 输出根目录读取文件
  Then 请求被拒绝，不泄露数据且不触发浏览器动作
```

## v0.2 增量验收
- 同一请求 schema 可从 HTTP、CLI、MCP 调用；agent 可发现模式、限制、暂停状态与实测差距。
- 上传本机媒体返回不可变 asset_id，已改内容拒绝；未知选项/冲突模式拒绝且不排队。
- 模式、模型、滑杆、切换项、时长和参考必须实际写入并核验；不存在/歧义/单位未知停在 Create 前，不能忽略参数。
- 同一幂等键跨客户端只生成一次；已下载成品复制后 SHA 一致，不覆盖同名不同内容。
- 新增真实 Suno 功能验收未执行时逐项标未实测，不降低为 fixture 通过。

## v0.3 文档、工作台与默认路由
- OpenAPI 的全部操作/输入字段、九 MCP 工具及其顶层参数均有说明；说明与实际返回结构、收费和恢复行为一致。
- UI 通过真实同源 API 进行模式/参考/预检、生成、进度、校验试听及下载；丢失回执并刷新后重试原键只存在一个任务/一次 Create。
- 暂停时新生成不可点击；未授权业务请求拒绝；token 不落 sessionStorage/页面正文，静态挂载不遮盖 API。
- 桌面与 390 px 手机布局无水平溢出；真实长任务标题、错误状态保持可读。
- 共用声音模块、全景、独立资产入口、skill 和 capabilities 的默认引擎一致；完整混音流程与真实 Suno 仍不得提前标为验收完成。

