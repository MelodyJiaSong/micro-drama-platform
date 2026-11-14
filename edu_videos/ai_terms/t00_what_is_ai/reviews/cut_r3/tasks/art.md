# 审稿任务：美术指导（ai_terms / t00_what_is_ai · cut 第 3 轮）

你是一位独立审稿人，用全新的视角审这一期中英双语科普短视频（AI 高频词系列，面向没有机器学习背景的普通观众）。

## 规则
- **只读**：不要修改仓库里的任何文件；只读下面列出的材料，不要读别的审稿报告。
- 只管你这一角色的必查项；顺手看到的其他问题放在最后「其他」，一句话。
- 拿不准写「存疑」并说明怎么核实。

## 材料（路径相对仓库根 C:/workspace/micro-drama-platform）
- `edu_videos/ai_terms/t00_what_is_ai/renders/sheets`
- `edu_videos/ai_terms/t00_what_is_ai/renders/en/sheets`
- `edu_videos/ai_terms/t00_what_is_ai/final/t00_what_is_ai.srt`
- `edu_videos/ai_terms/t00_what_is_ai/final/t00_what_is_ai.en.srt`
- `edu_videos/_shared/design/design_system.md`
- `edu_videos/_shared/design/tokens.json`
- `edu_videos/ai_terms/t00_what_is_ai/reviews/cut_r2/issues.md`（上一轮问题与作者处理结论）

## 必查项
1. 对照 design_system.md 与 tokens.json：颜色、字号阶梯、字重、留白、对齐、安全区
2. 每个画面是否承载概念（没有装饰性配图）；标签是否贴在所指之物旁、有没有多余的图例
3. 数据颜色含义是否全片一致（练习 = 墨黑实心、考试 = 琥珀空心、出问题 = 红、刚刚好 = 绿）
4. 层级：一眼先看到什么、第二眼看什么；同屏元素是否过多
5. 动效：一次只动一样、有无廉价特效；画面与解说是否同步（看每句收口的帧是否正好讲到画面上的东西）
6. 中英两版各自是否出框、断行是否难看
7. 插图：是否统一 I1 陶土风格、背景是否与舞台融合
8. R：复核上一轮你这一角色指出的问题（见上一轮 issues.md）：逐条写「已解决 / 未解决 / 改出了新问题」；作者「不采纳」的，判断理由是否成立

## 以前抓到过的同类问题（照这个水平找）
- v2 黑底 + 多色 + Manim 默认特效，被用户评为不够精修

## 输出
按句号逐条写在一张表里：| 句号 | 语言 | 级别 | 问题 | 建议改法 |。句号写 lNN（整体问题写「全片」或段号 sN）；语言写 zh / en / 双语；级别只用：必改（错误、误导、看不懂、画面与解说矛盾）/ 建议（明显更好的写法）/ 记录（小瑕疵）。建议改法要给出可以直接替换的文字（中英各自写本语言的版本，不逐字互译），不更长。表后写「最重要的 3 条」与「做得好的、别改掉的」各三条以内。没有问题的必查项也要写一句证据说明你查过。

把完整报告写到 `edu_videos/ai_terms/t00_what_is_ai/reviews/cut_r3/reports/art.md`（这是你唯一可以写的文件），然后只回复 200 字以内的摘要：最严重的 3 条与报告路径。
