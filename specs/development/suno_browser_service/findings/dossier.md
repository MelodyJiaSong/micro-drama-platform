# 研究综合

浏览器能力与 Suno 工作流已分开核对（[browser](angle-browser.md)、[suno](angle-suno.md)）。本机用独立持久化 Chrome profile；Browserless 仅接原生 Playwright endpoint。通过官方菜单取得文件，配额不足、挑战与未知提交停止自动推进。唯一任务标题用于关联歌曲，不能把任意新增两首算成本任务。

真实探测于 2026-10-22 到达 Suno 登录页，未进入付费账号；当前 DOM 默认匹配尚未校准。服务和 fixture 可继续实现验证，实际生成与官方下载仍需登录后联调。用户已要求后续自主决策，不再提问；不猜测凭据。

## 2026-10-22 v0.2 续查

上段为初始状态；实际登录后来成功，当前为验证码持久暂停。已保存的 v6 表单快照包括 Advanced、Simple、Sounds、模型选择、Audio/Voice/Inspo、Exclude styles、性别、Duration、Max Mode、Weirdness、Style Influence、Variety、My Taste。新接口在这些证据基础上扩展，但弹窗内部、上传后附件状态、Simple/Sounds 结果归属与下载仍缺真实验证。

官方 [v6 FAQ](https://help.suno.com/en/articles/13924481) 支持 Simple 的多参考输入、自然语言编辑意图及 Max Mode；[模型说明](https://help.suno.com/en/articles/13924993) 列出 v6/v6-wild/v6-mini 与自有 Custom Models；[Sounds](https://help.suno.com/en/articles/10625537) 介绍 One Shot/Loop 与 BPM。旧版 Persona/Audio Upload 指南有版本差异，不能把其旧控件/上限套给 v6。

代理接入用已安装 MCP Python SDK 1.27；本机 `claude mcp add --help`、`codex mcp add --help` 核对注册语法。统一以 HTTP 服务保存任务与秘密，MCP/CLI 不另建浏览器队列。

## v0.3 文档与工作台

本机代码检查发现 route 默认只有生成名称、MCP 参数缺 description，sound.md 仍指向本地生成工具；按 follow-up 003–005 补齐。UI 依赖独立 package-lock，与 API 同源 `/ui/`，不依赖外部 CDN；业务仍仅通过 `/v1`。生成字段从共用 Pydantic schema 提取描述和范围；后台认证/外部调用行为没有另设入口。新增验证全部在本机 fixture，无新 Suno 请求。
