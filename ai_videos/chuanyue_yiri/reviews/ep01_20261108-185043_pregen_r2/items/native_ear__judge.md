你是裁决人 **native_ear__judge**（claude · claude-opus-5-5），裁「母语听感」审稿项 native_ear 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reconcile\native_ear.md`。

## 两份报告
- a 位（claude-sonnet-5-5/native_ear__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\native_ear__a.md`
- b 位（gpt-6.1-sol/native_ear__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\native_ear__b.md`

## 要裁的维度
- **N3**（分歧）笑点与回收：a 2 分（开场目标 "find a bed before dark" 与 "try garum" 在 st4 由 "Future garum" 回收，渔夫鱼筐的画面说明接得上；本材料只有 s1，床的回收无法判断；"Future garum" 对不懂 garum 的观众稍隐晦，靠 st2 的 "the sauce" 解释撑住。）；b 0 分（只能核实 lines.md:11→14 的 garum 铺垫与鱼筐笑点；材料止于 :17，没有结尾或 dextram，不能核实维度要求的完整回收。不能据此断言成片遗漏，也不能判完整回收通过。）
- **N5**（抽查）改写：a 2 分（下表每条 "有点怪" 都给了不更长的改写（st3 11 词改 11 词，st1 8 词改 7 词，st2 去掉重复编号）。）；b 3 分（逐句表第 5、6 项涵盖全部“有点怪”句，改写分别为 7→6 词、11→10 词；其余逐句标注保留。改写保留找床、天黑前、尝 garum 及解释，不破坏第 14 行呼应。）
- **N6**（抽查）最别扭的 5 句：a 2 分（最别扭的 5 句排序见下方「最别扭的 5 句」，均为小瑕疵，没有很怪的句子。）；b 3 分（下方按相对生硬程度列出五句，均定位到 lines.md:8、11、17；前两句有轻微问题，后三句仍判自然，未为凑数虚造五个缺陷。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\native_ear__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" native_ear --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\native_ear__judge.md" --by "<你的模型名>/native_ear__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）