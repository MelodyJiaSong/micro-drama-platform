# changelog · xianjian_yi

## 立项（重启） — 2026-09-19 15:36:21
Source: user_input/raw_prompt.md + follow_ups/202609.md - section 001
Summary: 删除旧的 xianjian_yi_mv（MV 单片），改立为按游戏进度逐场景推进的 81 集长篇电影，体裁定为 ARPG 式一镜到底。

删除（不可恢复）:
- ai_videos/xianjian_yi_mv/ — 整个旧项目（421 文件 / 370MB：52 镜分镜、11 张人物卡、11 处场景、6 件物件、全部 png/mp4/mp3）
- ai_videos/_deleted/xianjian_yi_mv* — 8 个历史归档（161MB）
- specs/ai_video/xianjian_yi_mv/ — 旧 spec（raw/revised prompt、三个月 follow-up、changelog）
- ai_videos/assets.json — 移除 198 条 xianjian 资产条目（R2 对象未 prune，仅脱离索引）

保留并迁入新结构:
- ai_videos/xianjian_yi/_series/0_原作资料/ — 98 柔情版全剧本 + 95 官方攻略本 + 场景志 + 剧版对照 + 图证
- ai_videos/xianjian_yi/_series/characters/c1_李逍遥/ — 人物卡 + 立绘 + turntable（旧项目唯一保留资产）

新建:
- ai_videos/xianjian_yi/series.json — 系列标记（episode_prefix=xj）
- ai_videos/xianjian_yi/proposal.md — 立项总纲 + 一镜到底 divergence note
- ai_videos/xianjian_yi/README.md — 中文说明
- ai_videos/xianjian_yi/_series/series_bible.md — 跨集不变量
- ai_videos/xianjian_yi/_series/episode_map.md — 81 集分集表 + 几何复用表
- ai_videos/xianjian_yi/_series/0_原作资料/refs_game98/ — 逐场景参考帧库（派生缓存）
- tools/fetch_xianjian_refs.py — 参考帧库抽取工具

harness 侧改动:
- tools/assets/scanner.py — refs_game98/ 加入派生缓存跳过名单，不进 R2
- .gitignore — 新增 ai_videos/**/refs_game98/；_raw/ 规则由 ai_videos/*/ 放宽为 ai_videos/**/ 以适配系列嵌套
