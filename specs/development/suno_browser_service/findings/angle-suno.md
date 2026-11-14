---
worker_id: researcher-suno
stage: 3
role: researcher
angle: suno
status: complete
confidence: high
blockers: []
---

# Suno 网页创建与官方下载

核查日期：2026-10-22。范围仅为公开官方帮助与条款；未登录、未生成、未消费 credits 或下载额度。结论对公开文档可信度高，对实际账号 UI 未验证。

## 关键事实

| 环节 | 官方证据 | 对服务的意义 |
|---|---|---|
| 简单模式 | `/create` 选择 Simple，填写想听的歌曲描述。[Simple Mode，2025-12-19](https://help.suno.com/en/articles/2462273) | 首版可仅接受自然语言 prompt；官方页面没有提供可依赖的 DOM selectors。 |
| 生成与成本 | 当前 v6 FAQ 写明一次生成两首、合计 10 credits；多媒体输入和 Max Mode 可能增加成本。[v6 FAQ，2026-09-09](https://help.suno.com/en/articles/13924481) | 一次任务返回歌曲数组；不要把一次点击算成一首，也不要固定总成本。首版文本模式不要隐式开启额外功能。 |
| 完成信号 | Android 帮助称生成两首进入 Library，就绪时提示可播放；这仅证明移动端行为。[Android Simple Mode](https://help.suno.com/en/articles/3726657) | 尚无网页端稳定完成标记证据，不能把 Android 提示文案、固定睡眠或初现歌曲卡片当成网页完成契约。 |
| 单曲下载 | 在 Library / Workspace 找到歌曲，经 More Actions（…）→ Download → 格式选项。[官方下载步骤，2026-09-09](https://help.suno.com/en/articles/2409921) | 应通过官方下载 UI；多曲批量下载会形成 ZIP，首版逐曲下载可避免额外解包与关联问题。 |
| 格式 | MP3 所有计划；WAV 限 Pro / Premier 且通过网站下载。[格式说明，2026-09-09](https://help.suno.com/en/articles/13926081) | 支持 MP3 / WAV，但格式不存在时明确失败，不能把 MP3 转码伪称官方 WAV。 |
| 下载额度 | Pro 每月 20 首，Premier 60 首；按账单日重置、不结转，可另外购买。[额度说明，2026-09-09](https://help.suno.com/en/articles/13926209) | 付费订阅不代表无限下载；下载耗尽必须独立报告，不自动购买。 |
| 下载计数 | 同一首多次下载、不同格式、stems 计同一首；失败或中断不计。旧歌曲也适用限额，除非此前已下载。[计数规则](https://help.suno.com/en/articles/13926145)、[旧歌曲规则](https://help.suno.com/en/articles/13926593) | 按歌曲 ID 保存下载记录；下载失败不应重新生成，恢复只处理已识别歌曲。 |

## 明文自动化限制

[Suno Terms](https://suno.com/terms) 显示 2026-08-10 修订、2026-09-03 生效。Conditions of Access and Use 第 12 项原文为：

> engage in or use any data mining, robots, scraping, or similar data gathering or extraction methods

第 13 项另禁止绕过 Suno 的访问封禁。上述是明确的 robots / scraping 限制；本次没有找到针对用户自己付费账号的浏览器自动化例外。把网页自动化作为可供其他程序调用的服务，存在实际账号/条款风险；付费账户和用户对仓库“生成永远人点”的例外授权，均不证明已获 Suno 许可。这是对文本与本任务关系的判断，不是法律结论。

## 规格建议（设计判断）

- 在 README 显示核查日期、条款链接及上述已确认限制。遇 CAPTCHA、访问封禁、重新登录或额度不足时进入可诊断暂停状态；不做挑战代解、隐藏身份或封禁绕过。
- 显式持久化点击前/点击后/已发现歌曲/已下载状态。Create 后结果未知时禁止自动重提；已有歌曲可恢复下载。
- 任务持有歌曲 ID 与来源链接，完成标准包括官方浏览器下载结束、文件非空及类型检查。生成完成与文件可下载分开判断。
- UI selectors 应来自账号实际检查并可集中更新；当前文档只能支持工作流，不能支持任何具体 placeholder、CSS class、ARIA name、完成标记或下载弹窗结构。

## 未研究 / 待实测

1. 用户账号具体计划、当前额度、界面语言及地区可用性。
2. 当前网页 Create 的准确控件、生成中/成功/失败标记、两首歌曲的关联方式、WAV 是否需要二次等待。
3. Suno 是否愿意对此内部自动化用途提供书面授权；未发送任何联系信息。
4. 本次没有验证官方 API 是否不存在；只能陈述实现目标采用网页，不把搜索未发现 API 等同于官方声明。

本角度研究完整；上述缺口应进入线上验收清单，不能据此宣称真实 Suno 端到端已通过。
