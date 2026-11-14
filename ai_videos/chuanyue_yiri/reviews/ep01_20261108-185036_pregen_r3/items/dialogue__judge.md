你是裁决人 **dialogue__judge**（claude · claude-opus-5-5），裁「台词（时长与逻辑）」审稿项 dialogue 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reconcile\dialogue.md`。

## 两份报告
- a 位（claude-sonnet-5-5/dialogue__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\dialogue__a.md`
- b 位（gpt-6.1-sol/dialogue__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\dialogue__b.md`

## 要裁的维度
- **D1**（分歧）说得完：a 2 分（脚本数 43 个说话窗口，全部 ≤2.8 词/秒。最紧：s4_st1「Oh — oh no. That's pee!」5 词/1.8 s=2.78；s5_st12 6 词/2.2 s=2.73。扣停顿后略超：s2_st8 10 词/(4.0−0.5 s)=2.86，s8_st1 19 词/(7.7−1.0 s)=2.84。开口前最短 s8_st10 1.1 s，其余 ≥1.3 s。说完后最短 s2_st2 9.5→11 s=1.5 s，s3_st2 7.4→9 s=1.6 s，s4_st1 9.3→11 s=1.7 s，s7_st2 17.3→19 s=1.7 s，s7_st1 7.2→9 s=1.8 s，均 ≥1.5 s。）；b 1 分（脚本统计 37 个有台词镜头、58 个发声窗口；全部镜头首句前 ≥1.1 秒、末句后 ≥1.5 秒。但 37 份 prompt 的口型行仍统一“正常语速与口型”，与 s3_st4“飞快”、s4_st4“说得慢”、s8_st6“语速从容”相冲突；s2_st8、s8_st1、s5_st9、s7_st7 的停顿预算不足或未量化，详见问题表与计算表。）
- **D2**（分歧）节拍对位：a 2 分（s3_st4 动作总述仍写「她说话时 Felix 抬眼瞄她」，节拍却是 13–14.5 s（她说完 12.8 s 之后）才抬眼，I90 未改。s8_st6 节拍仍是单窗「5.1–8.8 秒」说两句、手一翻，无分句时间，I92 未改。其余各镜台词与动作对位：s2_st2 的 drain 与 stepping stones 手势各在自己的句窗内（1.5–6.5、6.5–9.5 s）；s7_st1 每个问句有各自秒数。）；b 1 分（s3_st4 动作总述仍说“她说话时 Felix 抬眼”，节拍却在 Riley 12.8 秒说完后，13–14.5 秒安排他的独立反应；s8_st6 的 5.1–8.8 秒仍未拆两句与翻手落点。s6_st3 13.6 秒听吆喝的剪辑依赖已经写明。）
- **D4**（分歧）台词逻辑：a 2 分（Mission one 找床（story.md 第 21 行）、Mission two 吃 garum（s5_st7）、s7_st1「Bed? Found. Garum? Tasted. Budget? Gone」都对得上。钱数账本对：7 枚红铜币付面包 2、付酒 2，剩 3 枚加大黄铜币（s6_st3 掌心 3+1），全部付给 Fortunata 后钱尽。迷路线 Hac recta platea…ito ad dextram → 猜 left → s4_st3「Left. Definitely left.」→ s5_st8/st9 回收 dextram，通顺。小瑕疵：s5_st9「all morning」，该镜在下午（I86 未改）；s4_st2「held a coin up to his nose」his 指代不明（I91 未改）。）；b 1 分（目标一找床、目标二试 garum，与 s5_st7“Mission two: done”及 s7_st1 总结一致；钱数 9→7→6→4→0 枚闭合。但 s3_st4“Straight… then dextram”接 s3_st8 出店即左转，直行阶段仍未交代；s4_st2 的 his nose 指代歧义仍在。）
- **D6**（分歧）听得清：a 2 分（s8_st1 prompt 第 12 行写明合唱与叉铃「音量低、隔着墙闷闷的」；s6_st6 写明说话时只剩很轻的碗勺声（I62 已改）。但所有 prompt 第 2 行与末行的声音模板仍只写「仅保留本镜指定对白、自然环境声和动作声」，没有「对白在前、说话时环境声降低」（I64 未改）。s3_st1 的「隆隆的磨声」没写音量（I63 未改）。Salve 与 Sal-VAY 的对比靠 1.6–3.6 s 听清，有风险。）；b 1 分（s8_st1 已明确墙后低音量实声，s6_st6 5.4–7.4 秒已有“很轻的碗勺声”；但 s3_st1 的隆隆磨声和 s8_st4 的出水声仍无对白期降音量要求，58 份 prompt 中未找到“对白清楚在前/环境声降低/对白优先”。实际声轨可懂度待出片，详见问题表。）
- **D3**（抽查）外语与专名：a 2 分（Garum 在 s3_st4、s5_st13、s7_st1 都有 GAH-rum 注音（I46 已改）。s8_st6 注 dum /dʊm/。Hospitium、Convenit、Apage、Assibus、Dupondium 都带古典注音。「Assibus hic bibitur…」是 CIL IV 1679 的真涂鸦。小瑕疵：s5_st13 prompt 第 19 行写 EW-geh，changes.md 写 YOO-geh，两处不一致。s3_st4 的 ito 是将来式命令，口语更常见 i。s8_st6「Dies nihil est. Dum versas te, nox fit.」语法通顺，但是新编句，没有出处，要在片尾说明或标「自拟」。）；b 2 分（s5_st13、s7_st1 当前 prompt 均有 GAH-rum；s8_st6 已用短 u 的 dum /dʊm/；s5_st13 当前为 EW-geh、两音节、硬 g，已非 changes 所述 YOO-geh。Petronius 41 原文与两句浴场对白相符，Terence 问路句是有删节的改编。小瑕疵是 r05:142 仍留 doom，:148 仍留未说明连读的 EH-oo-geh，详见问题表。）
- **D5**（抽查）说话人：a 3 分（s2_st8 Vibia 只表情不出声，节拍 4.5–8.5 s 仅 Riley 说；s8_st6 节拍 5.1–9 s「只有她张嘴」；s6_st3 括注「本镜只生成 Riley 自己的两句话」，吆喝贴 s6_st1（I89 已改）；s5_st8 店主喊 1.6–2.6 s 时 Riley 反应拍「停住头转」不张嘴；s8_st10 门房不说话。manifest 里没有 Riley 音频参考，I60 的串音隐患在 prompt 层面不存在。）；b 3 分（出片前说话人映射清楚：s3_st1 为 Felix 1.6–2.2 秒→Riley 2.8–3.6 秒；s8_st6 为 Riley 1.6–4.3 秒→画右 Helvia 5.1–8.8 秒→Riley 10.1–12.8 秒，首帧两人左右位置对应；s5_st8 明确画右粗嗓男店主喊话，Riley 不说话。s6_st3 已改为“只生成 Riley 自己的两句话”。本分仅证明文字和静态参考的映射，不冒充动态口型验收。）

## 全部评分维度
- **D1** 说得完：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）
- **D2** 节拍对位：台词和动作节拍对得上（说到哪句做哪个动作）
- **D3** 外语与专名：拉丁语语法与出处、注音进了 prompt；专名不易读错
- **D4** 台词逻辑：编号、回收、前后说法一致（目标一二、dextram、钱数）
- **D5** 说话人：每句的说话人对，画内该张嘴的人张嘴，不说话的人不出声
- **D6** 听得清：环境声不盖过台词；悄悄话、远处的话能听清

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\dialogue__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" dialogue --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\dialogue__judge.md" --by "<你的模型名>/dialogue__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）