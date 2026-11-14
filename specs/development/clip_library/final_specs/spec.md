# 素材库（clip_library）原型规格

## Goal
为「长采访提炼成 Short」建立素材地基：按授权搜索并批量下载 YouTube 视频和字幕，给每条素材记录授权状态；按字幕查找原话；按授权截取片段，生成 9:16 画面和出处卡。

## Out of scope
抖音、TikTok（用户协议禁止第三方下载，反爬也不稳定，二期再评估）；自动拼接成片、配音；平台内置的 Remix、Stitch、合拍功能（只能在 App 里用，没有接口）；绕过登录验证。

## Functional requirements
1. `search`：YouTube 搜索默认只返回 CC 授权的视频，可以按时长档、相关度、日期或播放量筛选排序。
2. `download`：支持传链接、链接清单或搜索结果。每条视频的详情只请求一次，再从本地 `info.json` 下载，最高 1080p MP4，同时下载字幕。`source.json` 最后写入，作为下载完成的标记，已完成的自动跳过。单条失败不影响后续视频，最后汇总报告失败项。
3. 授权判定：平台标了 CC 时自动记为 `cc_by`；把没有 CC 标签的视频手动记成 CC，直接拒绝；`permission` 和 `public_domain` 必须写明依据；其余一律记为 `quote`。
4. `find`：在全部或指定素材的字幕中搜关键词，去掉自动字幕滚动造成的重复行，输出时间点。
5. `cut`：`quote` 素材每段最多 10 秒，结束时间不能超出视频时长。默认输出 9:16（模糊背景加居中原画面），带出处卡（频道、授权、标题），同时输出按语言、从片段起点计时的 SRT，并追加一行到出处台账 `clips.jsonl`。
6. `login`：用独立 Chrome 配置打开 Google 官方登录页，登录时不开调试端口。用户关窗后，以无头方式读取 youtube.com 和 google.com 的 cookies，写入 `%LOCALAPPDATA%\clip_library\cookies.txt`；读不到登录标记就报错。之后的下载默认使用这个文件，`--cookies` 或 `--browser` 可以覆盖。账号密码只由用户自己输入。yt-dlp 忽略用户自己的配置文件。
7. 字幕下载失败只记警告，视频是否下载成功以视频文件存在为准（自动翻译字幕常被限流）。

## Acceptance
`pytest` 覆盖授权判定、时间解析、截取上限、字幕去重和搜索过滤参数编码。用合成素材实测 `list`、`find`、`cut`（含 9:16 和横版）：输出 1080×1920、8 秒，出处卡完整在画面内，超过 10 秒的 `quote` 片段被拒绝。真实下载需要用户提供登录方式后再验收。

## 项目规则适用说明
遵循 `.agents/references/project/development.md`（apps/ 与 libs/ 分层、DDD 加 CQRS、依赖注入）。原型阶段的偏差：没有使用仓储 Protocol，命令直接经 Reader 加载、经 Mapper 转成实体；未走 agent_team 六阶段流程（用户 2026-11-14 选择先做原型）。
