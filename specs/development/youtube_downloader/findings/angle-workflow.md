---
worker_id: researcher-02-workflow
stage: 3
role: researcher
angle: workflow
status: complete
blockers: []
confidence: high
---

# 本机下载工作流可靠性

## 覆盖问题

Windows 单视频工具如何避免意外批量下载、覆盖已有文件、把未完成文件误报成功，并在用户选定浏览器登录后解释失败。已读取当前 revised_prompt.md、qa.md；2026-10-04 实际检索并打开下列官方资料。本次只研究文档，未读取本机 cookies、调用收费服务或下载视频。

## 已查证事实

- yt-dlp 默认使用 `.part` 并续传未完成文件/分片；`--no-overwrites` 保护全部文件，默认只保护视频，仍可覆盖相关文件。`--force-overwrites` 同时关闭续传。[官方文件选项](https://github.com/yt-dlp/yt-dlp#filesystem-options)
- `--no-playlist` 仅说明当 URL 同时指向视频和列表时下载视频；列表模式另有 `--yes-playlist`。`--ignore-errors` 会把后处理失败视为成功；`--ignore-config` 可隔离用户已有配置。[官方选项](https://github.com/yt-dlp/yt-dlp#usage-and-options)
- 下载存档记录成功下载的 ID，后续据此跳过；它不等于核实当前输出目录仍有文件。[官方 FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-download-only-new-videos-from-a-playlist)
- 浏览器参数可指定浏览器与 profile；未指定 profile 时采用最近访问的 profile，因此“浏览器已登录”不必然对应目标账号。[官方 cookies 参数](https://github.com/yt-dlp/yt-dlp#filesystem-options)
- Windows Chromium cookies 存在数据库占用和 DPAPI 解密失败报告；两个官方问题页本次读取时仍为 Open。前者报告关闭 Chrome 后成功，后者不能据此推断关闭浏览器能修复。[文件占用 #7271](https://github.com/yt-dlp/yt-dlp/issues/7271)、[解密失败 #10927](https://github.com/yt-dlp/yt-dlp/issues/10927)
- cookies 主要用于需账号访问的内容；YouTube 会轮换 cookies，且部分格式/功能仍需外部 PO Token。登录状态不能保证所有视频、格式都可下载。[官方 YouTube 说明](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#youtube)
- 浏览器 cookies 导出组合命令会导出所有网站 cookies；cookies 文件须符合 Netscape 格式。[官方 FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)

## 对规格的建议（工程判断）

| 场景 | 应定义的行为 |
|---|---|
| 输入链接 | 校验支持的单视频路径和视频 ID；混合链接只取该视频；拒绝纯列表、频道和搜索入口。不能只依赖 `--no-playlist`。 |
| 写入与重复 | 显式设置 `--ignore-config`、`--no-overwrites`、续传与 `.part`；文件名包含视频 ID。区分“已有文件，跳过”和“本次下载成功”。 |
| 完成判定 | 展示解析、下载、合并/转码、完成；后处理完成且最终文件存在才报完成。不启用 `ignore-errors`；失败保留可续传中间文件。 |
| 重试 | 用相同目录和输出配置重试；不承诺每次都能续传。有限重试；网络、登录、解密、文件权限和后处理错误分别给出实际原因。 |
| 用户登录 | 默认不读取；用户明确选中浏览器才启用。保留 profile 选择扩展点；读取失败提示关闭占用浏览器或选择另一已登录浏览器后手动重试，不自动杀进程。 |
| 凭据处理 | 只在本机供本次请求使用；不自动导出 cookies 文件，不把 cookies 内容放入日志。 |

首版单视频不必增加全局下载存档：按 ID 跳过会妨碍同一视频另存目录、换分辨率或转 MP3；若未来增加列表，存档至少按输出用途隔离。

## 未研究与待验证

未实测用户机器的浏览器 profile、加密方式、网络和账号访问权限；未验证真实中断续传、同名跳过、后处理失败。实现验收应覆盖这些边界，不以文档研究代替实际成功证据。playlist、cookies 文件导入、PO Token 配置均未获当前需求要求，首版失败提示即可，不自动扩大功能。
