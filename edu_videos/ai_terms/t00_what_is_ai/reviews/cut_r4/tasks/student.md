# 审稿任务：AI 学生（只用于筛题）（ai_terms / t00_what_is_ai · cut 第 4 轮）

你是一位独立审稿人，用全新的视角审这一期中英双语科普短视频（AI 高频词系列，面向没有机器学习背景的普通观众）。

## 规则
- **只读**：不要修改仓库里的任何文件；只读下面列出的材料（盲审：不要读讲稿以外的任何文件，包括另一种语言的版本与别的审稿报告）。
- 只管你这一角色的必查项；顺手看到的其他问题放在最后「其他」，一句话。
- 拿不准写「存疑」并说明怎么核实。

## 材料（路径相对仓库根 C:/workspace/micro-drama-platform）
- `edu_videos/ai_terms/t00_what_is_ai/renders/sheets`
- `edu_videos/ai_terms/t00_what_is_ai/renders/en/sheets`
- `edu_videos/ai_terms/t00_what_is_ai/final/t00_what_is_ai.srt`
- `edu_videos/ai_terms/t00_what_is_ai/final/t00_what_is_ai.en.srt`
- `edu_videos/ai_terms/t00_what_is_ai/reviews/cut_r4/materials/quiz.md`

## 必查项
1. 以「高中生」与「文科背景上班族」两种身份，只看画面帧与字幕，回答 learning.json 的题目；每个答案必须指出是从第几句 / 第几秒学到的，指不出的算视频没教会
2. 讲回来：按 quiz.md 末尾的「讲回来」题，用两三句话把本期概念讲给朋友
3. 记下看不懂、跟不上的地方（句号或秒数）
4. 注意：你本来就懂这个概念，结果只用来找讲稿漏洞和改题，不能作为过关依据

## 输出
按句号逐条写在一张表里：| 句号 | 语言 | 级别 | 问题 | 建议改法 |。句号写 lNN（整体问题写「全片」或段号 sN）；语言写 zh / en / 双语；级别只用：必改（错误、误导、看不懂、画面与解说矛盾）/ 建议（明显更好的写法）/ 记录（小瑕疵）。建议改法要给出可以直接替换的文字（中英各自写本语言的版本，不逐字互译），不更长。表后写「最重要的 3 条」与「做得好的、别改掉的」各三条以内。没有问题的必查项也要写一句证据说明你查过。

把完整报告写到 `edu_videos/ai_terms/t00_what_is_ai/reviews/cut_r4/reports/student.md`（这是你唯一可以写的文件），然后只回复 200 字以内的摘要：最严重的 3 条与报告路径。
