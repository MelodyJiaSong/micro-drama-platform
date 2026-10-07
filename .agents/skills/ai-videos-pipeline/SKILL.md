---
name: ai-videos-pipeline
description: 三模块短剧创作：故事创作、影视改编、Prompt 编译。模块独立保存，上游确定后交接；Research 与人物、场景等资产独立支持。从一个小场景开始。
---

# 三模块创作

先读目标剧 README、workflow.json 和本次模块的输入。新流程标识为 three-module-v1；既有其他剧不批量迁移。
全局入口、稳定编号及跨 session 接续遵循[AI Video 工作流与覆盖边界](../../references/project/ai_video_workflow.md)；改影响制作的共用源时同步目录，登记不表示自动加载所有专项审查。

| 模块 | 输入 | 输出 | 指南 |
|---|---|---|---|
| 故事创作 | 用户的故事方向 | 小说式故事稿 | [story](modules/story.md) |
| 影视改编 | 已确定的故事 | 可拍的分镜 | [filming](modules/filming.md) |
| Prompt 编译 | 已确定的分镜 | 每镜 prompt | [prompts](modules/prompts.md) |

一次只改一个模块；下游不擅自改上游，冲突先提出修改请求。上游改变，下游内容保留并标记待更新。
创作允许候选；接受的输入与版本固定。编译只做确定性转换，不加入创意。
POC 从一个小场景开始；新规则先明确解决什么问题，再比较是否改善，不自动增加审查层。
现有 legacy BGM 库、固定情绪分类、bgm.md cue 契约与生成预设已移除，不作为新配乐设计的输入或默认约束。集级 cue 与剧级音乐资产的关系从新需求设计，不沿用旧实现；历史记录只作历史证据。
Seedance视频生成保留本镜指定对白、自然环境声和动作声，明确禁止背景音乐或配乐；无对白镜明确没有人说话。由Prompt编译固定写入，配乐后期独立处理，出片后试听核对。
每次故事生成/重跑按[独立创作run](modules/story-runs.md)固定输入、隔离transient产物、记录真实agent协作与逐项决策；UI展示结构化记录，跨session/Claude/Codex共用。

[Research](resources/research.md) 和 [资产](resources/assets.md) 独立于创作主线，按需读取；资产卡不自动成为当前故事历史。
调用收费服务前遵 CONVENTIONS.md 请求审计；生成与人工剪辑授权继续有效。当前 POC 到 prompt，不自动提交视频。
运行审计写 .audit/；项目要求写 specs/；禁止私有 memory。UI只读，soft promote只选用草稿；确定版本通过Claude Code/Codex完成，不宣称媒体验收通过。
