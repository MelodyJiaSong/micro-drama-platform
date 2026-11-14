你是裁决人 **native_ear__judge**（claude · claude-opus-5-5），裁「母语听感」审稿项 native_ear 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reconcile\native_ear.md`。

## 两份报告
- a 位（claude-sonnet-5-5/native_ear__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__a.md`
- b 位（gpt-6.1-sol/native_ear__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__b.md`

## 要裁的维度
- **N3**（分歧）笑点与回收：a 2 分（目标回收通：s5_st9 L70 "dextram is right?" 回收 s3_st4 L25 "No clue. Sounds like left?" 和 s4_st3 L30 "Left. Definitely left."；s7_st1 L122 "Bed? Found. Garum? Tasted. Budget? …Gone." 回收 s5_st13/st5；s4_st5 "…Nope." 靠典故，不知 "money doesn't smell" 的观众接不住（I98 仍未改，记录级）。）；b 0 分（完整维度包含开场目标与结尾的对应，但 lines.md 从 s2 开始，未提供开场任务原话；不能读取 s1 的 story/spec/prompt，previous.md L164 的截断摘要也不能代替独立核实。已查部分：L25→30→67→70 的 dextram 回收成立，L36→39 的闻钱笑点能理解，L122 的床／鱼露／预算均有范围内前文；缺失部分见 B04。）
- **N1**（抽查）自然度：a 2 分（lines.md 共 40 余句，s2_st2、s3_st1/st2/st3、s4_st1/st3/st4/st5、s5_st5/st11/st12/st14、s6_st3/st6、s7_st4/st6/st7/st1/st3、s8_st4/st9/st6 读来自然；"Ha — it's a truck stop."（L108）、"Rookie mistake."（L53）是地道口语。有点怪的只有 s4_st2（L36）、s7_st2（L125）、s3_st4（L25）、s8_st1（L47）、s3_st2（L19）。）；b 2 分（lines.md L8–128 逐句判断见下表；L36 的鼻子指代有歧义、L25 的猜方向稍牵强，L50、L70、L119 的本轮改词已自然，多数短句符合美式旅行 vlog。）
- **N6**（抽查）最别扭的 5 句：a 3 分（见下「最别扭的 5 句」，已排序。）；b 3 分（已按第一耳阻碍排序列出五句：L36、L25、L47 第二句、L47 第三句、L64 末句；第五句明确判自然，仅作相对排序，不凑造第五个缺陷。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" native_ear --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\native_ear__judge.md" --by "<你的模型名>/native_ear__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）