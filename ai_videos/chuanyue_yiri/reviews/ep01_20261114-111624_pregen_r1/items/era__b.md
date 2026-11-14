你是独立审稿人 **era__b**（b 位 · codex · gpt-6.1-sol），只管「时代与世界观」这一类。阶段：出片前（故事＋分镜＋prompt＋首帧/故事板）。
先完整读审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\BRIEF.md`，严格按它的规则和报告格式做。
同一项还有另一位审稿人（a 位，另一个模型）独立审；**不要读它的报告**，也不要读 reconcile/ 下的文件。

## 这一类是什么
画面和台词符合公元 75 年的庞贝：器物、建筑、服饰、发型都对；遵守系列禁区（画面不出现烟柱、维苏威不提）；不出现现代物件和文字。

想解决的问题：穿越剧最怕出戏：中世纪小镇、百叶窗、玻璃灯罩、耳环、相机，或开场城上一缕白烟被当成火山预兆。

为什么由这类模型审：看图认器物建筑服饰，加史实知识

## 范围
s1、s2、s3、s4、s8、s5、s6、s7

## 材料
- 总索引 `materials/index.md`；每镜 `materials/shots/<场>_<镜>/spec.md`（及拼图）；全集台词 `materials/lines.md`。
- 集目录、bible、故事稿、人物卡、场景卡路径见 BRIEF.md「材料」。

## 要查什么
时代可信度（建筑、街道、器物、服装发型、食物；有无现代物件）；系列禁区（以 bible 为准，规则源本身有矛盾也要报）；画面不出现相机、手机、自拍杆、文字；主角服装是否始终符合设定。

## 怎么查
以 scene1.jpg 为主，疑点看 sheet1/sheet4 或自己放大；读 bible 与考据资料；同时检查分镜与 prompt 里会诱发问题的写法。

## 审法（按步骤做）
1. 列出首帧和场景图里看得见的所有器物、建筑构件、衣着，逐项判断年代
2. 放大找文字和类字母的涂痕
3. 读 prompt 和卡片找火山词、禁区词
4. 台词里的史实对照考据 dossier

## 评分维度（报告「## 评分表」里每维一行：`- <编号> <0–3> 证据：…`）
- **E1** 器物：器物是公元 75 年庞贝有的（陶灯、双耳罐、铜币），没有现代或中世纪器物
- **E2** 建筑与材质：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍
- **E3** 服饰与发型：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰
- **E4** 系列禁区：画面不出现烟柱、白烟、冒白气的山；prompt 不写火山词；维苏威不提
- **E5** 文字：画面里没有可读的文字、字母、数字（墙、船、招牌、钱币）
- **E6** 史实一致：台词和画面里的史实与考据一致（地震年份、浴场时间、物价、尿税）
- **E7** 规则源：场景卡、道具卡、考据负面词里没有和以上冲突的写法

评分（0–3 分）：
- **0**：没查或查不了（必须说明原因）
- **1**：有问题（问题表里要有对应条目）
- **2**：基本没问题，有小瑕疵
- **3**：没问题
- 证据规则：打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。（证据至少 8 个字）
- 分歧：两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。
- 抽查：两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。
- 打 1 分：问题表里必须有对应条目；打 0 分：写 `原因：` 说明为什么查不了。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\era__b.md`

## 最后一步（Codex 审稿位）
Codex 沙箱只能看到工作区，python 不在里面，**你不用、也不要运行 tick**。只要：
1. 把报告写到 `C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\era__b.md`；
2. 在你最后的输出里单独打印一行：`REPORT WRITTEN: C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\era__b.md`。
调用你的人会凭 `codex exec` 的运行日志代为登记（日志里必须有这一行，且晚于派单时间），不会替你写或改报告。
（只有在沙箱外、能直接运行 python 时才可以自己打勾：`python tools/review_run.py tick "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1" era --slot b --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261114-111624_pregen_r1\reports\era__b.md" --by "gpt-6.1-sol/era__b"`；找不到 `python` 用 `C:/Users/light/AppData/Local/Programs/Python/Python311/python.exe`。）
- 你在 Codex 里跑（`codex exec` 跑这份任务书）。