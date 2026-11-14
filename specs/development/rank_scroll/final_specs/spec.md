# Spec · rank_scroll（v1，2026-11-03，AUTONOMOUS）

## Goal
命令行渲染器：把一个符合 `ai_videos/paihangbang/data_contract.md` 的剧集目录渲染成 1920×1080 60fps 的横向滚动 Top-N 排行视频，带国旗、图标、名次变化徽章、洞察卡、计分板、来源卡、片尾与可选音乐；输出可复现，可快速出草稿。

## Out of scope
旁白 / TTS；上传 YouTube；音乐生成（由 suno 服务完成）；图片下载（由数据整理步骤完成）；竖版 Shorts（v2）；柱状图竞赛（v2）；4K（v2）。

## User roles & primary flows
- 制作者（代理或用户）：`python -m rank_scroll render <ep_dir> [--music f] [--draft] [--from S --to S] [--out f]`；`preview <ep_dir> --t 12.5` 出单帧 PNG；`validate <ep_dir>` 校验输入；`thumb <ep_dir>` 出封面草图。

## Functional requirements
1. FR1 校验：data.json 字段、类型、长度上限、图标名、rank 顺序；图片存在且列在 assets.json；国旗存在。错误列表化输出，`validate` 退出码非 0。
2. FR2 时间线：按 interview 第 4 条生成段落（intro / 卡片 / 洞察 / top10 减速 / 冠军停留 / 计分板揭晓 / 来源卡 / 片尾），总时长可由 `timeline` 子命令打印。
3. FR3 滚动：卡片带从右向左平移；名次 N 首先出现在右侧，冠军最后停在画面中央；同屏约 3 张（卡宽按期由 `layout.card_w` 定，480–800）。
（follow-up 008，2026-11-03）可选 `layout.intro_hold`（0–6 s，默认 0）：滑入后整排静止再滚动；publish 章节按每组实际最小名次标注。
4. FR4 卡片解剖（v0.2，2026-11-03 follow-up 004，优先级 照片 > 国旗 > 关键数值）：主图满版铺满卡片（cover 裁切，焦点取 `image_focus` 或 `layout.focus`）；左上大国旗（原比例、白边）；右上名次药丸；徽章在国旗下；底部深色渐变上依次是国名、名称、主数值（大字）+ 次数值；副标题与 ≤2 个标签合成一行小字；署名最小号放在最底一行。无图卡居中放大国旗、主题图标和一行原因。
5. FR5 前 10 名放大 1.06×（卡高 848 px，不碰页头和进度条）；冠军卡有光晕。
6. FR6 洞察卡：在 `after_rank` 指定的位置插入滚动带，宽度为照片卡的 72%，文字竖直居中。
7. FR7 计分板：常驻右上，按 `tally.by` 统计已完整进入画面的卡片，显示前 5；结尾揭晓全表（前 8）。
8. FR8 片头：kicker + 标题 + metric/period + source_line；片尾前来源卡列出 source_line 与「Image credits in description」。
9. FR9 音乐：`--music` 时混入，淡入淡出，长度对齐；无音乐时输出静音轨（YouTube 兼容）音乐先单独做成「音乐床」：每首可写 `song.mp3@IN:OUT` 截取（同一首可重复用作结尾再现），4 s 交叉淡入，`--music-fit end` 时跳过末首开头多出的部分让它自然结束在片尾；loudnorm 两遍线性（I=-16、TP=-1.5）。（follow-up 006）
10. FR10 输出：MP4（H.264 yuv420p，正片 libx264 CRF 16 preset slow；`--draft` 用 960×540 + h264_nvenc 或 ultrafast）；同目录写 `render_manifest.json`（输入文件 sha256、模板版本、参数、时长、ffmpeg 命令）。
11. FR11 封面：1280×720 PNG。
12. FR12 主题：`theme` 名映射到 token；未知主题回退 default 并警告。

## Non-functional requirements
- 1080p60 渲染 6 分钟片 ≤ 15 分钟（本机）。
- 文本不出框：自动缩小字号以适配宽度（下限后截断加省略号）。
- 可复现：无随机；同输入 → 同帧（帧哈希测试）。
- 依赖：skia-python 144.1、numpy、ffmpeg（PATH）。

## Acceptance criteria summary
见 `validation/acceptance_criteria.md`。

## Open questions
无阻塞项；音乐时长与段落对齐策略待成片后人工评估。
