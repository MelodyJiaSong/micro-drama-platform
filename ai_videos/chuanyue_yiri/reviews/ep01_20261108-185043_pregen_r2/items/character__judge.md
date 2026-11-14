你是裁决人 **character__judge**（claude · claude-opus-5-5），裁「人物逻辑」审稿项 character 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reconcile\character.md`。

## 两份报告
- a 位（claude-sonnet-5-5/character__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\character__a.md`
- b 位（gpt-6.1-sol/character__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\character__b.md`

## 要裁的维度
- **C3**（抽查）视线：a 2 分（st4 spec 走位 0 秒面朝画左渔夫、8–9 看筐、9–11.7 看年轻渔夫、11.7 起转镜头；st3 第 3–4 秒工人看她脸、「视线落在走近的她脸上」；st5 5–11 秒视线按驴 / 目送 / 铺子分开写清；st4 首帧（放大）Riley 侧脸朝画左渔夫，与 spec 一致。小瑕疵：st5 赶驴人 6.5–7.5 秒瞥裤子时 Riley 在看驴，二人没有视线交汇，仍成立（见问题 3）。）；b 3 分（st3 首帧工人在画右低头、挑夫在骡子画左面向通道，与快照 prompt 第 11–13 行一致；st4 第 12 行明确 8–9 秒看鱼、9–11.7 秒看年轻人、11.7 秒后转向镜头；st5 俯视图分别标出看驴、目送、看铺子与回镜头的朝向。）
- **C7**（抽查）动机连贯：a 2 分（st1 惊奇 → st2 兴奋报目标 → st4 看鱼眼睛一亮 → st3 跟挑夫上坡、看裂缝想起 → st5 走出门洞安静地笑，情绪线连续；st4 末 15.5–18 秒「回头看鱼笑」到 st3 第 0 秒「背对镜头往门洞走」靠剪辑承接，无断裂。小瑕疵：st3 首帧里工人在门洞外右侧（首帧放大：他靠在大拱右墩与小拱之间），spec 写在门洞里面墙根下，会影响「她走进门洞前遇见他」的先后。）；b 3 分（按索引播放顺序 st2 的尝 garum 目标接 st4 见鱼联想，再上坡进入 st3，看到补缝后讲地震，接 st5 安静看街与运货；st5 没有低头看自己裤子或耸肩，未与 story.md 第 45–47 行的“apparently”制造重复发现。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\character__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" character --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\character__judge.md" --by "<你的模型名>/character__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）