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

**审查以审查单为准；出片前走审查循环**（用户 2026-11-07 / 11-08，chuanyue_yiri follow-up 034 / 035 / 036 及 review-v5）。循环是：**Claude 单审打分（2026-11-14 用户改，follow-up 065；原为 Claude＋Codex 双审 → 对比 / 裁决）→ 问题分级 → 定方案 → 实施 → 下一轮复核，最多 3 轮 → 收轮记结论**；每轮审查结果**不设用户 review 闸门**，用户只在出片时确认（用户 2026-11-08）。① `python tools/review_run.py new <集目录> --stage pregen` 出审查单：名册 `.agents/references/project/review_roster.json` 按「阶段 × 法则 × 范围」排审稿项，**每项两位审稿人**——a 位是最适合这一类的 Claude 模型、b 位是最适合的 Codex 模型（`reviewers` / `model_why`，按合适选，不按便宜选）；每类有自己的多维 **rubric** 与审法（`method`）。② 两份任务书 `items/<代号>__a.md`、`__b.md` 各交一位全新上下文的审稿人（互不看报告），派单用 `dispatch <审查单> <代号> --slot a|b --runner … --model … --prompt-file …` 登记；报告「## 评分表」每维 0–3 分，**2、3 分必须写证据**（镜头·秒数·图上位置·文件行·数字），1 分要在问题表有对应行，0 分写原因，缺维度、高分无证据都勾不上。Claude 审稿人自己 `tick --slot a`（作者不能代勾）；Codex 沙箱里没有 python，b 位只写报告并打印 `REPORT WRITTEN: <路径>`，由调用方 `tick --slot b --attest-log <codex exec 日志>` **凭运行日志代为登记**（只限 Codex、日志须含报告路径且晚于派单，v2 单最近一次派单是 Codex 时同样适用）；没审成的 `fail --slot`。③ 两位都勾后工具自动对比（`reconcile/<代号>.md`）：**两人都说没问题不等于没问题**——分歧（差 ≥2，或一人 ≤1 一人 ≥2）交裁决人，两人都打 ≥2 的维度每项再确定性抽 2 维复核，裁决人（名册 `adjudicator`）按 `items/<代号>__judge.md` 逐维给最终分与理由，`adjudicate` 登记；`gate` 要全部裁完才过。④ `issues <审查单>` 由评分与问题表推出分级问题清单（critical＝某维 0 分、任一重出或关键维度 ≤1；major＝其余 1 分与可剪；verify＝存疑；minor＝记录），每条用 `fix <审查单> <I编号> --solution … --status planned|implemented|wontfix [--reason …]` 记方案；**便宜的改动（除 Seedance 积分外都算：改故事、分镜、prompt、编译器、Codex 出图、工具）直接改**，critical 与 major 都 implemented（或 wontfix 写理由）后才能 `new --after <上一轮>` 开下一轮，changes.md 与 previous.md 由问题清单生成，新一轮每位审稿人用 R 一行逐条复核。⑤ `conclude` 写「结果.md」（各类两位审稿人的分并排、最终分、分歧怎么裁、未解决的问题）并记结论（可出片 / 不可出片＋理由，默认按未处理的严重问题推），状态「已收轮」——不等用户 review，审查页也不写「待你确认」（旧单的「待用户确认」用 `migrate` 或 `status` 改成「已收轮」并写 log）。**修复页**：每轮 `fix` 时用 `--file <改了的文件>`（可多次）和 `--before <旧图> --after <新图>` 记下改了什么，再 `corrections <审查单>` 生成 corrections.json / .md——每个有方案的问题、每镜首帧前后（修复前＝`new` 存进 `materials/snapshot/` 的 sha 对上的那张，旧单按审查开始时已在的那版，含 `_r1`、`_r1b_old` 等归档；修复后＝下一轮审的那张或现行）、分镜逐字段 diff、下一轮审稿人的复核结果（已复核通过 / 复核仍有问题 / 待复核）；管理站 /review-run/corrections 与审查单、问题清单双向链接。出片时用户在对话里同意后 `confirm --quote "用户原话"`。开了闸门的剧（workflow.json `"review_gate": "required"`），`shot_take.py submit` 会查覆盖该场的最新一张已收轮出片前审查单是否用户已确认、材料未变，没有就拒绝提交；用户明确要求跳过时才用 `--skip-review "用户原话"`。出片后、剪辑、交付的审查同样开审查单（`--stage take|cut|episode`），全部审完才算审过，不向用户宣称审过。所有审查单存在 `ai_videos/<剧>/reviews/<集>_<时间>_<阶段>_r<轮>/`，管理站剧页「☑ 审查单」与 /review-run 显示；进行中的旧 v2 单（每项一位、必查项 ✓/✗）照旧可用。作者自己的 `review.md` 仍要写，但不能代替审查单。**每个审查大类至少有一种审查机制**（名册 `mechanisms`）：台词分「台词（时长与逻辑）」和「母语听感」两类，后者是英语母语观众盲审，只读 `materials/lines.md`——用户指出结尾台词母语观众听着很怪、原台词审稿人没抓到之后加的。
不追求 100%：视频生成等非确定步骤不在我们控制内，按 2/8 定律把精力花在有价值、能解决的问题上，不为单次失败过度拟合规则；同一镜重试到上限仍不成功就搁置，与用户共同讨论处理方式（见[出片](modules/prompts-generate.md)）。2/8 决定做什么，不降低做到什么程度：纳入范围的部分要高质量、接近 100% 确定，每次改进都用测试固定下来，不让累积的改动拉低整体质量或引入随机问题。
配乐与集级 cue 从新需求设计，不沿用已删除的 legacy BGM 库与 cue 契约。
所有新音频生成（环境音、音效、背景音乐、主题曲、片尾曲等）默认走 Suno 浏览器服务 API/MCP；先按 [声音与音乐](modules/sound.md) 查能力、预检、生成、取回和试听。当前不支持的音频需求明确记录，不擅自改用其他引擎；后期混音与剪辑继续用本机工具。此默认同样适用于独立声音资产，已有音频不重生成。
Seedance视频生成保留本镜指定对白、自然环境声和动作声，明确禁止背景音乐或配乐；无对白镜明确没有人说话。由Prompt编译固定写入，配乐后期独立处理，出片后试听核对。

[Research](resources/research.md) 和 [资产](resources/assets.md) 独立于创作主线，按需读取；资产卡不自动成为当前故事历史。
调用收费服务前遵 CONVENTIONS.md 请求审计；生成与人工剪辑授权继续有效。当前 POC 到 prompt，不自动提交视频。
运行审计写 .audit/；项目要求写 specs/；禁止私有 memory。UI只读；确定版本通过Claude Code/Codex完成，不宣称媒体验收通过。
