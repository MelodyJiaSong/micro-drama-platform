# 下载工具研究结论

Run: youtube_downloader-20261004-094351

## Angles researched
- download：高清合并、音频转换、YouTube 脚本运行依赖。
- workflow：续传、已有文件、列表、cookies 与失败边界。

## Cross-cutting insights
网络下载结束不等于完成，必须等待 FFmpeg 后处理成功并确认最终文件存在（download + workflow）。高清要求与可用格式会变化，质量作为上限而非承诺（download + workflow）。

## Recommendations for the spec
使用 yt-dlp[default] 携带 EJS，检查 FFmpeg/ffprobe 和 Deno。单视频严格校验，显式 --ignore-config、--no-playlist、--continue、--no-overwrites；后处理失败保持失败。不默认读取浏览器 cookies。

## Open questions surviving research
实际 YouTube 访问受当前网络与平台风控影响，须实测并报告结果。MP4 容器不保证每个播放器都支持其视频编码。

来源：[下载依赖研究](angle-download.md)、[可靠性研究](angle-workflow.md)。
