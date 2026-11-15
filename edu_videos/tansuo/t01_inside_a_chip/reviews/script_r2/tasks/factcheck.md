# 审稿任务：事实核查（tansuo / t01_inside_a_chip · script 第 2 轮）

你是一位独立审稿人，用全新的视角审这一期中英双语科普视频（面向没有专业背景的普通观众）。

## 规则
- **只读**：不要修改仓库里的任何文件；只读下面列出的材料，不要读别的审稿报告。
- 只管你这一角色的必查项；顺手看到的其他问题放在最后「其他」，一句话。
- 拿不准写「存疑」并说明怎么核实。

## 材料（路径相对仓库根 C:/workspace/micro-drama-platform）
- `edu_videos/tansuo/t01_inside_a_chip/reviews/script_r2/materials/lines.md`
- `edu_videos/tansuo/t01_inside_a_chip/claims.json`
- `edu_videos/tansuo/t01_inside_a_chip/research/dossier.md`
- `edu_videos/tansuo/t01_inside_a_chip/reviews/script_r1/issues.md`（上一轮问题与作者处理结论）

## 必查项
1. 逐条核对 claims.json：数字是谁做到的、原话怎么说、单位与口径；需要时打开出处原文（论文页面 / PDF）核对
2. 讲稿与画面文字有没有比原文说得更满（夸大、因果说成相关、相关说成因果）
3. 引文翻译是否忠实原意（例：part…part 不是「一半…一半」）
4. 专业概念是否准确：本期所属领域的老师能否挑出错；类比与简化有没有越过事实边界
5. 讲稿里有没有未登记进 claims.json 的事实性说法
6. R：复核上一轮你这一角色指出的问题（见上一轮 issues.md）：逐条写「已解决 / 未解决 / 改出了新问题」；作者「不采纳」的，判断理由是否成立

## 以前抓到过的同类问题（照这个水平找）
- 初稿把「另训一个模型认出医院 99.9%」说成肺炎模型自己认医院（独立审稿抓到）
- Lazer 的 cases 指数据点，不是病例少

## 输出
按句号逐条写在一张表里：| 句号 | 语言 | 级别 | 问题 | 建议改法 |。句号写 lNN（整体问题写「全片」或段号 sN）；语言写 zh / en / 双语；级别只用：必改（错误、误导、看不懂、画面与解说矛盾）/ 建议（明显更好的写法）/ 记录（小瑕疵）。建议改法要给出可以直接替换的文字（中英各自写本语言的版本，不逐字互译），不更长。表后写「最重要的 3 条」与「做得好的、别改掉的」各三条以内。没有问题的必查项也要写一句证据说明你查过。

把完整报告写到 `edu_videos/tansuo/t01_inside_a_chip/reviews/script_r2/reports/factcheck.md`（这是你唯一可以写的文件），然后只回复 200 字以内的摘要：最严重的 3 条与报告路径。
