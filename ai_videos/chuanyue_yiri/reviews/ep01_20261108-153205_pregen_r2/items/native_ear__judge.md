你是裁决人 **native_ear__judge**（claude · claude-opus-5-5），裁「母语听感」审稿项 native_ear 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reconcile\native_ear.md`。

## 两份报告
- a 位（claude-sonnet-5-5/native_ear__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\native_ear__a.md`
- b 位（gpt-6-astra/native_ear__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\native_ear__b.md`

## 要裁的维度
- **N1**（抽查）自然度：a 2 分（逐句听下来约 35 句 Riley 英文，绝大多数自然（s2_st8 "apparently a woman in pants is a lot"、s4_st4 "I'm totally lost… and I still smell like pee"、s8_st4 "Rookie mistake"、s7_st4 "Cozy."）；"有点怪"4 句：s8_st10、s4_st2 第二段、s5_st9、s8_st1；没有"很怪"。）；b 2 分（L8–128 的 Riley 台词逐句见下表；L36 的 his、L50 的 they、L119 的 Rope springs 有轻微听辨负担，其余主要是自然口语。）
- **N3**（抽查）笑点与回收：a 2 分（dextram 线回收完整（s3_st4 随口猜 left → s4_st3 "Left. Definitely left." → s5_st8 店主喊 → s5_st9 "I went the wrong way all morning"）；garum 线 s3_st4/s5_st13/s5_st5/s7_st1 呼应；s7_st6 "Air conditioning / that's the bathroom" 靠画面成立。小瑕疵：s4_st2→s4_st5 的"钱不臭"笑点只靠 "Smell anything?"→"…Nope." 暗示；"Mission two" 的开场目标本范围内无法核（s1 不在材料内）。）；b 2 分（L25→30→67→70 的 dextram 猜错、强化、纠正链可读；L36→39 的 Smell anything/Nope 和 L94→122 的找床/找到床均有回收。L94 的 Mission two 缺 s1 原句，只能保留未核实边界，见 B06。）

## 全部评分维度
- **N1** 自然度：逐句：母语观众听着自然 / 有点怪 / 很怪
- **N2** 别扭原因：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词
- **N3** 笑点与回收：笑点母语观众接得住；开场目标与结尾、dextram 回收得上
- **N4** 人设口吻：像一个二十多岁、亲切的旅行博主在说话，前后口吻一致
- **N5** 改写：每句「有点怪 / 很怪」都给不更长的改写
- **N6** 最别扭的 5 句：列出并排序

评分（0–3 分）：
- **0**：没查或查不了（必须说明原因）
- **1**：有问题（问题表里要有对应条目）
- **2**：基本没问题，有小瑕疵
- **3**：没问题
- 证据规则：打 2 或 3 分必须写证据：指到镜头、秒数、图上位置、文件行或计算数字；没有证据的高分按「没查」处理，打不了勾。（证据至少 8 个字）
- 分歧：两位审稿人同一维度分数相差 ≥2，或一人 ≤1、另一人 ≥2，就是分歧，交裁决人。
- 抽查：两人都打 ≥2 的维度，裁决人每个审稿项随机抽 2 维复核证据，专抓两个模型共同的盲点。

## 规则
- 分歧维度：回到材料本身核两人的证据，谁的证据站得住；抽查维度：专门找两个模型可能**共同**漏掉的问题，不因两人都给高分就放过。
- 每个要裁的维度在报告「## 裁决」写一行：`- <编号> <最终分 0–3> 理由：<引用证据：镜头·秒数·图上位置·文件行>`（理由至少 8 个字）。
- 发现两人都漏的问题，可以加问题表（同审稿报告的表头，含「严重度」列）。只读，不改被审材料。

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\native_ear__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" native_ear --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\native_ear__judge.md" --by "<你的模型名>/native_ear__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）