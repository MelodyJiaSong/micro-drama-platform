# 魔兽世界

## Vision（观众体验）

> **跟着主角们一路走进一个全新的艾泽拉斯，它像指环王一样真实宏伟：没玩过的人看得懂，老玩家处处认得出；每到一个新地方都是一次震撼，故事的规模远超当年的游戏。**

核心：一个人的力量永远不够；够用的前提，是承认不够、开口求助。

全剧 Vision：剧级一句话体验与核心，由用户定（2026-10-11）；接不上核心的想法再好也不用；每个环节创作与审查都对照它；故事、分镜、剪辑、声音的取舍都围绕它，改动须用户同意并记理由。写法见[观众](../../.agents/skills/ai-videos-pipeline/modules/story-audience.md)；每集的体验写在集级故事决策记录开头，边拍边加。

| 体验 | 怎么做到 | 主要落在 |
|---|---|---|
| 一起探索 | 观众与主角们同步发现世界，不提前交代；每到一个新地点给一场「抵达」（如第一次看见暴风城），用建立镜头展示它的宏伟 | 故事（行程）；影视改编（建立镜头、运镜、光）；生成预算优先给这些时刻 |
| 两层都看懂 | 剧情靠画面与人物交代清楚，不依赖游戏知识；原场景、NPC、建筑与装备设计是老玩家能认出的一层，认不出也不影响理解 | 故事；资产（场景与人物还原游戏设计） |
| 震撼 | 宏伟建筑、技能与特效集中在抵达和关键战斗，不平摊到每一镜 | 影视改编、[注意力引导](../../.agents/skills/ai-videos-pipeline/modules/filming-attention.md)、Prompt 编译 |
| 规模更大 | 剧情事件大于游戏任务：牵动王国、阵营、瘟疫等大局，同时落在主角们自己身上 | 故事；[全剧方向](2_世界观人设/series.md) |
| 风格 | 魔兽电影、指环王式的真实奇幻史诗感 | `workflow.json` 风格；人物与场景资产 |
| 不要 | CG 过场动画感（负面词之后再加） | Prompt 负面词 |

从 EP1 重新开始。Research 与人物、场景等资产独立保留，旧剧情不继承。

2026-10-13/14，follow-up 048 / 049：Scene2 冷开场与全集遗留问题的故事修订已确定（代理按自主授权，评分卡待用户补打）；2026-10-15 分镜整集按新故事重做并确定（16 场 · 113 镜 · 731 秒）。审核与下游缺口见 `episodes/ep01/decisions/story.md` 的048、049节和 `decisions/filming.md`。2026-10-15 用户要求 s2 先单场编译并用 Dreamina CLI 出片，其它场仍待补参考后编译。


Legacy BGM 库、cue 时间线与管理入口已移除，新流程不继承其固定分类、格式或生成预设。配乐与 cue 将按新的创作需求设计；现有独立音乐资产及历史 run 不变。

EP1 的 `episodes/ep01/cue/` 为集级配乐 cue 占位目录，与 `scenes/` 并列；当前仅有 `.gitkeep`，具体音乐流程与数据格式待后续补充。

Seedance prompt 固定声明：仅保留本镜指定对白、自然环境声和动作声，不要背景音乐或配乐；无对白镜明确没有人说话。配乐后期独立处理，出片后试听确认。编译器v3自动加入该规则，旧编译版本标待更新。

制作结构为剧 → 集（episode）→ 场（scene）→ 镜头（shot）。可复用的环境资产在 `2_世界观人设/background/`，通过 `bgN` 绑定到场次；同一背景可以用于多场。原资产 `scenes/` 已迁移，媒体内容与历史 run 保留。

`filming.json` 的 `content.scenes` 按场组织，每场有 `id`（s1）、`background`（bg2 或空）、`location`、`time`、`purpose` 和 `shots`；镜头有 `id`（st1）、`duration`、`cast`（出场人物资产键）、`action`、`blocking`、`beats`、`camera`、`lighting`、`dialogue`（follow-up 227）。编号是稳定身份，数组顺序决定播放顺序，不因调序重新编号。EP1 故事已确定；当前分镜已有内容，s3 修订已获直接编译授权并完成 v9 编译（follow-up 040）。

编译结果按场保存在 `prompts.json`，镜头 key 与 prompt 第一行均为 `ep1_s1_st1`。派生文件落在 `episodes/ep01/scenes/s1/shots/st1/prompt.txt`；包含完整 key 的下载文件导入同镜头的 `renders/`，不改原文件名。缺失、不完整或找不到唯一对应镜头的 key 不导入。

之后剧情以魔兽游戏主线为骨架，允许适度补写；每次创作明确选用游戏版本、阶段锚点及可改边界。片种为连续剧（workflow.json `format: series`），故事创作读共用故事原则与连续剧页。EP1 故事已确定（follow-up 025）；影视改编按新流程（片种 → 场 → 覆盖 → 镜头）重做全集：12 场、92 镜、生成时长 564 秒（follow-up 045 当前值），s3 修订已确定并编译（follow-up 040），s4 的18镜145秒修订已确定并编译（follow-up 045）。决策记录：集级 `episodes/ep01/decisions/filming.md`，场级 `episodes/ep01/scenes/sN/decisions.md`。全剧方向与伏笔账本见 `2_世界观人设/series.md`。

| 模块 | 文件 | 内容 |
|---|---|---|
| 故事创作 | episodes/ep01/story.json | 故事方向、正文 |
| 影视改编 | episodes/ep01/filming.json | 时长、场景、动作、摄影、对白 |
| Prompt 编译与出片 | 各镜 planning/overhead.toml、previz/；episodes/ep01/prompts.json；各镜 renders/ | 每镜 overhead（复杂镜 previz）；带参考的编译结果；生成的条 |
| 剪辑、声音与音乐、成片交付 | 待设计 | 后期三个模块，暂为占位 |

左侧导航：0_research、1_资产库、2_故事、3_影视改编、4_Prompt编译与出片、5_剪辑、6_声音与音乐、7_成片交付（后三个为占位）。
各 stage 是可展开目录；当前各含EP1，点击子项才进入内容。
资产库保存世界规则及选定资产的长期事实；集内已确定的状态变化记在该集 state_changes.md。
上游确定后交接；上游改变，下游保留并标记待更新。
第一步先确定一个小故事；人物、地点、时长、对白语言重新选择，不沿用旧救援剧情。
Research：0_research/。资产库：2_世界观人设/。已有资产卡只供参考，不是当前故事历史。

UI只读，所有创作修改通过Claude Code/Codex。

Prompt 参考设置在 `workflow.json`：`prompt`（模型 seedance2.5、比例 16:9、全剧风格行）与 `figure_colors`（人物卡号 → overhead 圆点与 previz 人偶的颜色，不用绿色）。

## Scene3 出片现状（2026-10-11）

五镜已生成并下载，共760积分；生成/技术检查完成，独立内容初筛changes_required（1 blocker、4 major、2 minor、1输入冲突）。38.304秒全条预览、英文地点字幕样片、试听WAV与修复交接已备。其他会话s4改动使全集指纹失效，本次s3五包已scope sync为失效、冻结提交包与视频保留。未试听、未锁片，R2缺凭据。

[五镜生成交接](episodes/ep01/scenes/s3/generation_handoff.md)。

## Scene4 出片现状（2026-10-12）

Scene4已补齐缺失st17并执行两轮关键修复，共新增22条视频、回执3680积分；当前18镜145秒（st8后新增稳定st18，st10延长2秒），全集12场92镜564秒。新增c1-13盖回破包、c2-2腰佩短剑两套三视图；独立文本复核0 blocker/major，v9确定性编译及资料包ok92。最终18镜独立采样仍7 major/5 moderate，达第三轮的相关镜搁置，不再自动重出。146.165秒全候选预览、试听WAV、自动转写及18条审核已备；未完整播放或试听、未锁片，R2缺凭据未上传。中文回执编码修复已验证，先前7个回执异常只恢复任务号补收，没有重复提交。最终账户余额8906（另会话Scene2支出2480），本次6000积分上限未超。

[18镜预览](../../.audit/adhoc_agents/2026-10-12/s4-resume/previews_third/ep01_s4_18shot_candidates_preview.mp4)；[生成与审核交接](episodes/ep01/scenes/s4/generation_handoff.md)；[修复与搁置计划](episodes/ep01/scenes/s4/regen_plan.md)。
