---
worker_id: researcher-01-download
stage: 3
role: researcher
angle: download
status: complete
blockers: []
confidence: high
---

# 下载依赖与格式处理

核查日期：2026-10-04。已使用实际网页搜索与原文读取；仅查官方资料，未调用下载服务、读取 cookies 或下载视频。

## 1. 覆盖问题

Windows 本机工具如何完成带声音的视频与 MP3 下载，避免把缺少依赖、格式不可用、容器不兼容误报为成功。以当前 revised_prompt.md 和 interview/qa.md 为范围。

## 2. 关键发现

- **完整 YouTube 支持包含 JS 执行依赖。** EJS 官方指南推荐 Deno，最低 2.3.0，默认启用；Node 最低 22.0.0，须显式启用。Windows 可使用同目录运行时或明确路径。官方 yt-dlp.exe 已捆绑 EJS；Python 安装应使用 `yt-dlp[default]`，并随 yt-dlp 更新 EJS。以上是当前文档版本，不能冻结为永久要求。[EJS 指南](https://github.com/yt-dlp/yt-dlp/wiki/EJS)
- **高清完整视频需要合并。** YouTube 的较高画质通常分开提供视频与音频，须用 FFmpeg 合并，只有视频流下载成功不等于完整视频完成。[官方 FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#do-i-need-any-other-programs)
- **FFmpeg 与 FFprobe 要是真实可执行文件。** MP3 使用 `-x --audio-format mp3` 后处理；Python 同名 ffmpeg 包不能代替二进制。`--merge-output-format` 只影响发生合并的任务；换容器用 remux，目标不支持原编码则失败。[依赖与后处理](https://github.com/yt-dlp/yt-dlp#dependencies)
- **格式应按视频实际可用信息选择。** `-F` 列出格式；可按 height、vcodec、acodec 等筛选，字段可能缺失。`-S res:720` 无低于上限格式时可选到更大尺寸，故严格上限应使用筛选条件；竖屏需明确质量档按高度还是短边（res）定义。[格式筛选与排序](https://github.com/yt-dlp/yt-dlp#format-selection)
- **容器和编码是不同约束。** FFmpeg streamcopy 直接复制压缩数据，不降低画质；转码需要解码再编码，增加计算成本且通常有损。因此 MP4 容器不能证明输出是 H.264，MP3 转换也不会改善源音质。[FFmpeg streamcopy / transcoding](https://ffmpeg.org/ffmpeg.html#Streamcopy)
- **最终文件位置要在后处理完成后取得。** 官方要求用 `after_move:filepath` 获取最终路径；合并或转换可能改变预估扩展名。视频下载进度 100% 后仍可能处理失败。[输出模板说明](https://github.com/yt-dlp/yt-dlp#output-template)
- **更新与站点限制影响可靠性。** 官方推荐常规用户使用 nightly；stable 也可能因站点变化失效。YouTube 部分格式需要外部 PO Token；默认客户端会尝试无需 token 的路径。当前账号可访问不能保证工具一定成功；OAuth 已不能用于 yt-dlp 的 YouTube 登录。[更新说明](https://github.com/yt-dlp/yt-dlp#update)、[YouTube 提取器说明](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#youtube)

## 3. 对规格的具体建议

以下是据资料作出的项目建议，不是用户已确认的新增需求：

- 启动检查 yt-dlp、FFmpeg、FFprobe、JS 运行时与 EJS；缺少依赖时提供具体名称和修复步骤。保持可升级版本，记录任务使用的版本，避免静默自更新破坏正在运行的任务。
- 默认单视频；质量选项表示最大目标分辨率，低于目标时展示实际质量；无符合格式时报错。若采用此策略，必须在 UI 写清“最高不超过”，不能把 720p 任务结果静默提升到 1080p。
- 最佳质量优先保留源编码并合并到兼容容器。若要求固定 MP4/H.264，则单列为兼容输出策略，并说明可能降低可用画质或需要转码；不要仅改文件后缀。
- MP3 单独走音频选择与转换；任务状态至少区分解析、下载、合并/转换、完成、失败。只在最终文件存在且后处理成功后开放输出文件入口。
- 保留“用户显式选择后读取浏览器登录”的边界。JS、cookies、PO Token、网络与格式错误分别保留原因，避免用“请登录”覆盖全部失败。

## 4. 未解决问题 / 未调研

- 输出优先保持最高质量，还是优先固定 MP4/H.264 兼容性？资料能说明取舍，不能替用户决定。
- MP3 默认码率及竖屏质量档规则尚需在规格中明确；这些不阻止下载能力设计。
- 未验证任何实际视频、账号、代理、浏览器 cookies 或 PO Token 插件；当前结论是官方文档支持的设计依据，不是现场下载成功证据。打包许可证与浏览器凭据处理由其他研究角度覆盖。
