---
worker_id: level-specialist-validation
stage: 5
role: level-specialist
level: security
status: complete
blockers: []
confidence: high
---

# 安全边界

下面是待运行检查，不是已发现漏洞；任一实际 SEC 失败为 critical。

| ID | 检查 | 预期 |
|---|---|---|
| SEC-01 鉴权 | 创建、查询、恢复、文件全部业务路由测试无 token/错误 token/正确 token；检查默认绑定 | 未授权不读写任务、不启动浏览器；默认 127.0.0.1；无 token 的生产配置不能悄然提供业务能力 |
| SEC-02 输出范围 | job ID / 文件名包含 `..`、编码路径、`/`、`\`、绝对盘符、UNC、Windows ADS；文件属于另一个 job；软链接/junction 越界 | 仅读取该 job 已登记成品，最终解析路径仍在允许根内；拒绝越界，不拼接任意请求路径 |
| SEC-03 target 范围 | 相对/绝对 target、`ai_videos` 前缀近似目录、`..`、symlink/junction | 指定制作归属经 resolve 后在仓库 ai_videos 内；缺省归属明确到服务审计目录；非法 target 不产生请求 |
| SEC-04 URL 与配置 | 恢复 URL 输入 localhost、内网、file/data/javascript、伪造 suno.com 后缀、含凭据 URL；远程 endpoint 入口 | 恢复只接收预期 Suno 官方歌曲 URL，不能成为 SSRF/任意导航；endpoint 仅由运维本机配置提供，不接受任务传入 |
| SEC-05 秘密 | 检查 Git、HTTP 错误、RequestLog、控制台、启动失败及异常栈 | Suno 密码不入服务；profile/storage state/token/带 token endpoint 不入 Git 或输出；日志保留 prompt 等请求参数但脱敏凭据 |
| SEC-06 审计与生成次数 | request 写入失败、提交后超时、DB 写失败、结果日志失败、进程重启、调用者重试 | 未先记账不调用；可能提交后绝不因错误或恢复自动再次 Create；自动生成例外只限定本服务 |
| SEC-07 官方能力边界 | 代码与浏览器行为检查，下载不可用及验证码 fixture | 只调用用户可见网页 Create/Download；不逆向私有 API、不下载播放流替代官方导出、不绕过 CAPTCHA/配额/账号限制 |

路径验证须覆盖 Windows 实际语义；确因权限无法建立链接的测试显式 skip。浏览器网页自己的内部 HTTP 不宣称逐请求审计；本服务控制的连接/导航/准备/提交/轮询/下载动作必须先记 RequestLog。

## v0.2 参考和代理边界
参考 API 只接受上传字节与服务 asset_id，不接受服务端任意文件路径；限制格式、64 MiB、媒体探测、存储路径和 SHA。引用 URL 仅 Suno song/playlist，不抓取任意 URL。MCP/CLI 本机路径是调用者明确要上传的文件，令牌只从私有文件/环境读取，服务地址限 loopback。下载输出校验哈希、拒绝重定向路径与同名不同内容，原子发布；MCP 安装保留其他配置。

上传 Suno 前先审计，参考权利确认不替用户勾选；既有验证码暂停不因新模式、MCP 或重启解除。只选择已有 Voice/Persona，不注册声纹、训练模型、发布作品。

## v0.3 工作台
UI 公开静态壳，业务仍 Bearer 鉴权且仅本机；token 只在页面内存，URL、日志、localStorage/sessionStorage 不含令牌。sessionStorage 只保存当前未获回执的请求与幂等键。媒体获取同样鉴权，经大小/SHA256 核对才建 blob 供试听下载；没有向第三方 origin 发送 token 的能力。静态页 CSP 限同源脚本/连接、禁 iframe 嵌入与对象，产物不依赖 CDN。未知提交保留原键，恢复不清验证码，原任务不可随意另键重提。

