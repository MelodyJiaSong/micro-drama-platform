你是裁决人 **character_A__judge**（claude · claude-opus-5-5），裁「人物逻辑」审稿项 character_A 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reconcile\character_A.md`。

## 两份报告
- a 位（claude-sonnet-5-5/character_A__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\character_A__a.md`
- b 位（gpt-6.1-sol/character_A__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\character_A__b.md`

## 要裁的维度
- **C2**（抽查）想要什么：a 2 分（s3_st1 5.5–10 秒付钱、拿面包动作都服务买面包；s4_st1 1.5–2.5 秒被熏→大喊→捏鼻→退，动机清楚；s8_st2 3–13 秒门房要钱→收钱→再打量，目的清楚。小瑕疵：s8_st1 Riley 为什么直奔浴场只靠台词「everybody hits the baths」交代，没有动作拍）；b 3 分（s3_st1 5.5–11.5 秒指面包、付钱、收钱、递饼服务买卖目的；s4_st1 6–11 秒赶人、退出、复工各有目的；s8_st5 2.5–14 秒从发现注视到示范与递刮板，热心帮助有行动依据。）
- **C5**（抽查）主持人性格：a 3 分（s2_st8 1–2.5 秒向瞪她的 Vibia 挥手、8.5–11 秒憋笑瞟一眼（好奇、敢试、自嘲）；s3_st1 学说 Sal-VAY；s4_st1 7.6–9.4 秒举手说 Okay, okay；s8_st4「Rookie mistake」自嘲，s8_st8 1–2.5 秒对看她的妇女挥手；每次当地人有动作她都有回应）；b 3 分（s3_st1 2.5–5.5 秒敢学招呼且和 Felix 一起笑；s2_st8 遭冷落后忍笑调侃自己；s4_st1 7.6–11 秒举手回应并退出；s8_st9 9.7–13 秒还刮板、对 Helvia 笑，符合好奇、敢试、自嘲且有礼貌的人设。）

## 全部评分维度
- **C1** 知道什么：每个人此刻知道什么、不知道什么，行为不越过他的认知
- **C2** 想要什么：每个人此刻的目的清楚，动作服务于目的
- **C3** 视线：每个时刻每个人看向谁，合理（不无缘无故看镜头、不无视身边的怪事）
- **C4** 反应拍：配角的反应单独占拍，不被吞掉；反应和身份、性格相符
- **C5** 主持人性格：Riley 的反应符合人设（好奇、敢试、自嘲），对当地人有回应
- **C6** 路人：路人有合理的反应且不雷同，不抢主笑点
- **C7** 动机连贯：跨镜头的情绪与动机连得上，没有突然的转变

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\character_A__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" character_A --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\character_A__judge.md" --by "<你的模型名>/character_A__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）