你是裁决人 **native_ear__judge**（claude · claude-opus-5-5），裁「母语听感」审稿项 native_ear 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reconcile\native_ear.md`。

## 两份报告
- a 位（claude-sonnet-5-5/native_ear__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\native_ear__a.md`
- b 位（gpt-6-astra/native_ear__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\native_ear__b.md`

## 要裁的维度
- **N2**（分歧）别扭原因：a 1 分（s1_st4 指代不清（指着鱼说 "That's garum"）；s1_st3 讲解腔（"They had a huge earthquake…"）；s1_st2 "Mission one/two" 电报式罗列加 "75 AD" 写法（见问题表）。）；b 2 分（第 11 行连续「Mission one / Mission two」略显预先编排；第 8 行碎句有惊讶语境，第 17 行 had / ago 与 AD 75 当下视角相容，未发现明确直译或时态错误。）
- **N1**（抽查）自然度：a 2 分（lines.md 共 4 句台词（s1_st1 / st2 / st4 / st3）。st1、st2 基本自然，st4 "That's garum. …Eventually." 很怪，st3 有点怪（讲解腔）。）；b 2 分（lines.md 第 8、11、14、17 行共 12 个句子／独立话语单位，10 个自然，2 个「Mission」句有轻微念提纲感；无「很怪」。逐句表列全。）
- **N4**（抽查）人设口吻：a 2 分（st1、st2 是年轻 vlogger 口吻（"Okay… I just time-traveled"、"Good morning from Pompeii!"）；st3 的 "They had a huge earthquake twelve years ago. They're still fixing the damage." 变成导游腔，口吻略掉。）；b 2 分（第 8 行 Okay、第 11 行预算揭示、第 14 行悄悄话式 Eventually 连起来像亲切旅行博主；第 11 行双 Mission 稍显主持提纲，其余口吻一致。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\native_ear__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1" native_ear --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153208_pregen_r1\reports\native_ear__judge.md" --by "<你的模型名>/native_ear__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）