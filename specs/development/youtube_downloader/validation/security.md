---
worker_id: level-specialist-02-security
stage: 5
role: level-specialist
level: security
status: complete
blockers: []
confidence: high
---

# 安全验证策略

依据 `final_specs/spec.md`、validation playbook 与 validation/{general,development}.md。这里只定义 stage 6 检查，未执行运行时验收；窗口和 CLI 均适用。

| 编号 | 场景与证据 | 必须满足 |
|---|---|---|
| SEC-01 链接入口 | 输入 `file://`、FTP、伪装域名 `youtube.com.evil.example`、`youtube.com@evil.example`、含账号密码 URL、缺失/畸形 ID、纯列表和频道。记录错误、任务 PID 与输出目录。 | 本地拒绝；不启动下载进程、不访问链接、不读取 cookies、不产生输出。合法 watch/Shorts/live/embed/youtu.be 走同一验证入口。 |
| SEC-02 单视频约束 | 合法视频 URL 附带 `list`、`index` 或无关查询；同时试重复 `v` 和追加选项样式文本。检查传入下载器的 URL 和结果。 | 只下载一个确定的视频；歧义 ID 拒绝或明确规范化，查询不能触发列表或改变命令选项。 |
| SEC-03 进程参数 | 保存目录含空格、`&`、`$()`、中文；非法 URL 含引号、分号、换行。静态检查进程启动与记录真实参数边界。 | 不通过 shell；目录作为一个参数原样传入，不展开或执行其中字符。URL 校验先于进程启动，选项不得来自任意用户文本。 |
| SEC-04 配置隔离 | 在隔离临时 HOME/APPDATA 下放置 yt-dlp 配置，包含 `--yes-playlist` 与写标记文件的 `--exec`；在下载适配层用无敏感数据的本地媒体夹具启动真实下载器，不改公开 URL 白名单。 | 使用 `--ignore-config`；标记文件不存在；预期输出及单视频行为不受配置影响。测试不修改用户真实配置。 |
| SEC-05 cookies 选择 | 默认设置运行；再分别显式选择 Chrome、Edge、Firefox并检查参数。用失败夹具验证无法读取数据库/解密。 | 默认不传浏览器 cookies 参数且不访问 cookies；选中时仅传选定浏览器；失败显示真实原因，不静默改用其他浏览器、不自动导出 cookies、不把 cookies 内容写入日志。无需读取真实凭据来证明默认隔离。 |
| SEC-06 任务树关闭 | 测试下载任务产生持续运行子进程；另起独立哨兵进程。分别点击取消、关闭窗口和 CLI Ctrl+C；检查每个 PID、退出状态与 `.part`。 | 终止自己的根任务及子进程，哨兵继续；不按进程名称批量杀；CLI 返回非零；分片保留。窗口关闭不能留下本任务后台写文件。 |
| SEC-07 失败与保护 | 分别触发网络失败、权限错误、后处理非零、返回零但最终文件缺失；预先放置同名文件并保存 SHA256。 | 无错误路径显示“完成”；不启用 `ignore-errors`；已有文件 SHA256 不变；跳过与成功区分；只有进程成功且最终文件存在才完成。 |

真实网络成功流程交由系统验收；安全失败夹具在临时目录执行。非法入口测试观察调用边界，配置注入和任务树测试运行真实子进程，不能只检查代码字面量。未执行项明确记未验证。

项目为原生 Tk 与 CLI，无服务器、API、Web 前端或代理；Origin/Host/CSRF、浏览器 E2E 和生产静态路由 gate 不适用。Tk 事件循环、窗口关闭和 CLI 取消均必须实测。该适用性来自规格的明确说明，不免除人工窗口试用。

任意 SEC-* 失败按共用 severity policy 记 `critical`，立即停止该工作单元并报告；运行时必须记录 `validation.started` 与实际 `validation.pass` / `validation.issue.raised`。本文件 status 表示策略完成，不代表实现通过。
