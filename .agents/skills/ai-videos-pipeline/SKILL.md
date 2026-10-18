---
name: ai-videos-pipeline
description: 短剧六模块：故事创作、影视改编、Prompt 编译与出片、剪辑、声音与音乐、成片交付（后三个待设计）。模块独立保存，上游确定后交接；Research 与人物、场景等资产独立支持。从一个小场景开始。
---

# 短剧六模块

先读目标剧 README、workflow.json 和本次模块的输入。新流程标识沿用 three-module-v1（标识名不变）；既有其他剧不批量迁移。
全局入口、目录编号及跨 session 接续遵循[AI Video 工作流与覆盖边界](../../references/project/ai_video_workflow.md)；改影响制作的共用源时同步目录。

**第一原则：观众是主角。** 每个模块的每个选择，先问观众此刻知道什么、在想什么、在等什么，再问人物该怎么做、事情先后怎么排；见[观众](modules/story-audience.md)。

**全剧 Vision 与核心。** 剧 README 开头的「## Vision（观众体验）」是全剧宗旨：一句话 Vision（观众感受到什么）加一行「核心：」（这部剧唯一关于什么，见[观众](modules/story-audience.md)）。下文的「对照 Vision」都包括核心：接不上核心的想法再好也不用。每个模块：**创作前**先读；**创作时**每个取舍对照它，与它冲突的方案不选；**审查时**第一问是「这个产物是否满足 Vision」，答案与理由写进决策记录或审核记录。Vision 由用户定，代理不改；觉得它该改，提出来由用户决定。

| 模块 | 输入 | 输出 | 指南 |
|---|---|---|---|
| 故事创作 | 用户的故事方向 | 小说式故事稿 | [故事结构](modules/story-structure.md) + 本剧[片种](modules/story-formats.md)页 |
| 影视改编 | 已确定的故事 | 可拍的分镜 | [filming](modules/filming.md) + 本剧[片种](modules/filming-formats.md)页 |
| Prompt 编译与出片 | 已确定的分镜；资产与场地平面图 | 每镜 overhead（默认不做 previz）；带参考的 prompt；生成的条 | [prompts](modules/prompts.md) |
| 剪辑（待设计） | 各镜头的条 | 锁片版本 | [edit](modules/edit.md) |
| 声音与音乐（待设计） | 锁片版本 | 混音与分轨 | [sound](modules/sound.md) |
| 成片交付（待设计） | 锁片版本与终混 | 平台母版 | [delivery](modules/delivery.md) |

创作段：故事创作 → 影视改编 → Prompt 编译与出片；后期段：剪辑 → 声音与音乐 → 成片交付。待设计的模块只占位，不自行发明数据格式或流程；出片仍由用户决定生成，将来可按[出片](modules/prompts-generate.md)的前提切换为自动。

故事创作先读剧 README 的「Vision（观众体验）」（剧级一句话体验，用户定；缺了先问，不自行写定），再读共用原则与剧 workflow.json `format` 对应的片种页（`film` 电影 / `series` 连续剧）；未声明就先问用户，不自行假定。连续剧另读剧级 `2_世界观人设/series.md`（全剧方向与伏笔账本），本集钉子留宽；定稿后更新账本。
模块、关卡与交接的全景以[工作流全景](../../references/project/ai_video_workflow_map.json)为准；术语以[术语表](../../references/project/ai_video_glossary.json)为准：剧、季、集、幕、段落、场、拍点、镜头、条、cue 等的定义与相互关系。
交给用户确定前先跑交稿前自检（`tools/audience_check.py`），确定时由用户打评分卡，见[决策记录](modules/decisions.md)。每次创作同时写[决策记录](modules/decisions.md)：故事创作写集级，影视改编写集级与场级；依据写到指南编号与小节。
一次只改一个模块；下游不擅自改上游，冲突先提出修改请求。上游改变，下游内容保留并标记待更新。
创作允许候选；接受的输入与版本固定。编译只做确定性转换，不加入创意。
POC 从一个小场景开始；新规则先明确解决什么问题，再比较是否改善，不自动增加审查层。
不追求 100%：视频生成等非确定步骤不在我们控制内，按 2/8 定律把精力花在有价值、能解决的问题上，不为单次失败过度拟合规则；同一镜重试到上限仍不成功就搁置，与用户共同讨论处理方式（见[出片](modules/prompts-generate.md)）。2/8 决定做什么，不降低做到什么程度：纳入范围的部分要高质量、接近 100% 确定，每次改进都用测试固定下来，不让累积的改动拉低整体质量或引入随机问题。
配乐与集级 cue 从新需求设计，不沿用已删除的 legacy BGM 库与 cue 契约。
Seedance视频生成保留本镜指定对白、自然环境声和动作声，明确禁止背景音乐或配乐；无对白镜明确没有人说话。由Prompt编译固定写入，配乐后期独立处理，出片后试听核对。

[Research](resources/research.md) 和 [资产](resources/assets.md) 独立于创作主线，按需读取；资产卡不自动成为当前故事历史。
调用收费服务前遵 CONVENTIONS.md 请求审计；生成与人工剪辑授权继续有效。当前 POC 到 prompt，不自动提交视频。
运行审计写 .audit/；项目要求写 specs/；禁止私有 memory。UI只读；确定版本通过Claude Code/Codex完成，不宣称媒体验收通过。
