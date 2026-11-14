# Findings dossier · rank_scroll

研究已在系列层完成，本项目不重复：

- 渲染方案比较、许可、本机工具：`ai_videos/paihangbang/0_research/toolchain.md` §4、§7。
- 参考片画面结构与节奏（每名约 6 s，同屏约 2.5 列，倒数）：`ai_videos/paihangbang/0_research/reference_analysis.md` §1。
- YPP 风险对格式的要求（来源、变化、洞察、计分板）：`genre_and_topics.md` §3，落到 `bible.md` §1。

本项目补充的实测（2026-11-03）：

- skia-python 144.1 安装成功，`skia.SVGDOM` 可用；Tabler SVG 使用 `currentColor`，渲染前替换为具体颜色。
- Pillow 无 raqm；不用 Pillow 排版。
- ffmpeg 支持 `-f rawvideo -pix_fmt rgba` 从 stdin 读帧。
