# 魔兽世界

从 EP1 重新开始。Research 与人物、场景等资产独立保留，旧剧情不继承。

Legacy BGM 库、cue 时间线与管理入口已移除，新流程不继承其固定分类、格式或生成预设。配乐与 cue 将按新的创作需求设计；现有独立音乐资产及历史 run 不变。

EP1 的 `episodes/ep01/cue/` 为集级配乐 cue 占位目录，与 `scenes/` 并列；当前仅有 `.gitkeep`，具体音乐流程与数据格式待后续补充。

Seedance prompt 固定声明：仅保留本镜指定对白、自然环境声和动作声，不要背景音乐或配乐；无对白镜明确没有人说话。配乐后期独立处理，出片后试听确认。编译器v3自动加入该规则，旧编译版本标待更新。

制作结构为剧 → 集（episode）→ 场（scene）→ 镜头（shot）。可复用的环境资产在 `2_世界观人设/background/`，通过 `bgN` 绑定到场次；同一背景可以用于多场。原资产 `scenes/` 已迁移，媒体内容与历史 run 保留。

`filming.json` 的 `content.scenes` 按场组织，每场有 `id`（s1）、`background`（bg2 或空）、`location`、`time`、`purpose` 和 `shots`；镜头有 `id`（st1）、`duration`、`action`、`camera`、`dialogue`。编号是稳定身份，数组顺序决定播放顺序，不因调序重新编号。当前 EP1 分镜仍为空，故事仍是未确定草稿。

编译结果按场保存在 `prompts.json`，镜头 key 与 prompt 第一行均为 `ep1_s1_st1`。派生文件落在 `episodes/ep01/scenes/s1/shots/st1/prompt.txt`；包含完整 key 的下载文件导入同镜头的 `renders/`，不改原文件名。缺失、不完整或找不到唯一对应镜头的 key 不导入。

之后剧情以魔兽游戏主线为骨架，允许适度补写，按[通用故事指南](../../.agents/references/project/story_guidelines.md)滚动组织EP。每次创作明确选用游戏版本、阶段锚点及可改边界；当前候选和旧run不因新规则自动重写。[本次研究](../../specs/ai_video/shengji_zhilu/findings/story-guideline-research-20261004.md)保存来源与适用性。

| 模块 | 文件 | 内容 |
|---|---|---|
| 故事创作 | episodes/ep01/story.json | 故事方向、正文 |
| 影视改编 | episodes/ep01/filming.json | 时长、场景、动作、摄影、对白 |
| Prompt 编译 | episodes/ep01/prompts.json | 固定规则编译结果 |

左侧导航：0_research、1_资产库、2_故事、3_影视改编、4_prompt编译。
三创作stage是可展开目录；当前各含EP1，点击子项才进入内容。
资产库保存世界规则及选定资产的长期事实；EP1先分共享配置·Persistent、当前EP1、runs·Transient。共享输入/规则在run外；当前EP1是指向所选run的soft link；run1/run2各分输入与规则、产出（候选故事/变化）与过程（创作日志）。state_changes.md仅记录已确定变化，前集确定后人工核对并承接，不读取未来集。
上游确定后交接；上游改变，下游保留并标记待更新。
第一步先确定一个小故事；人物、地点、时长、对白语言重新选择，不沿用旧救援剧情。
Research：0_research/。资产库：2_世界观人设/。已有资产卡只供参考，不是当前故事历史。

UI只读，所有创作修改通过Claude Code/Codex。通用流程见[独立创作run](../../.agents/skills/ai-videos-pipeline/modules/story-runs.md)。EP/shared/为独立persistent配置，明确profile的input/rules分文件管理，当前方向仍属暂定假设；每次run冻结输入、单独保存候选与过程，不继承旧候选。
本轮候选《一枚铜币》已载入EP1故事草稿，尚未确定。run：story-run-20261003-214907-dd638b81。人物、交接棚、交易惯例均为本轮虚构候选；独立审稿提醒魔兽辨识度偏弱，取舍及完整证据见创作记录。

第二次同规则候选《少掉的两枚铜币》已独立保存：story-run-20261003-144640-85f316d4。当前选用Run1；两run均可通过promote CLI选作草稿，原候选保留。共享baseline-v1为两次完全相同输入/规则，workflow-v2为后续流程版本，本实验未用。

[两次run输入与流程清单](../../specs/ai_video/shengji_zhilu/findings/run-input-inventory-20261004.md)列出五份实际取用文件、完整setting、作者/审稿输入边界及历史信息缺口。UI各run的输入软链接打开当时版本，审稿实际输入包与作者初稿也可独立查阅；独立审计文件须与历史SHA256一致，不用变化后的内容冒充当时版本。
