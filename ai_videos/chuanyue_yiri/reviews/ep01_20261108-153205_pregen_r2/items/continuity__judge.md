你是裁决人 **continuity__judge**（claude · claude-opus-5-5），裁「连续性」审稿项 continuity 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reconcile\continuity.md`。

## 两份报告
- a 位（claude-opus-5-5/continuity__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__a.md`
- b 位（gpt-6.1-sol/continuity__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__b.md`

## 要裁的维度
- **K3**（抽查）服装与发型：a 2 分（衬衫（米白短袖挽袖）、橄榄腰带、卡其工装裤、深棕短靴 58 张首帧一致；布包 s2 无 → s3_st7 8.5 秒系上 → s3_st4/st8、s4、s8、s5 至 st13 都在左胯 → s5_st13 解下、s5_st7 腰上空（I18 已改好）→ s6、s7 无，全对；s8_st4/st5/st9/st6 头发干蓬、鬓角汗湿、肩头微湿（I19 已改好）。小瑕疵：s8_st5/st9/st6 首帧布包像一只单独立在石凳上的包，看不出系在腰带上。）；b 2 分（s3_st7 8.5–11 秒系左胯布包，s4_st1、s8_st3/st7、s5_st2/st13 首帧维持左侧，s5_st7 后腰上无包；全程米白短袖、橄榄腰带、卡其裤。s8_st5/st9 胸前发梢比 st4 更成束、显湿，是否超出“仅鬓角汗湿”存疑，见 C07。）
- **K7**（抽查）跨场引用：a 3 分（s3_st4「Sounds like left?」→ s3_st8 往她的左边（画右）走 → s4_st3「Left. Definitely left.」→ s5_st8 Dextram 往右拐 → s5_st9「went the wrong way all morning」；s5_st13「缺了一瓣」对 s3_st2 掰的一瓣，s5_st7「缺两瓣」对 s5_st13 第二瓣；s5_st1「Clean-ish」对 s8 浴场；s4_st4「still smell like pee」对 s4_st1；s7_st1「Garum? Tasted / Budget? Gone」对 s5_st5、s6_st2；s8_st1 两点、s5_st1 三点半与场标题时段一致。）；b 3 分（s3_st4 2.3–5.2 秒 Felix 说 dextram、8.2–12.8 秒 Riley 猜 left，st8 向自己的左边出发；s5_st8 先演驴车右转，st9 才说“dextram means right”。s5_st13 解开早晨七瓣面包再掰一瓣，st5 试味、st7 完成目标二，s6_st2 付清及 s7_st1 的 Bed/Garum/Budget 回收均有前事。）

## 全部评分维度
- **K1** 道具状态表：逐镜列出每件道具进、出场状态，前后接得上
- **K2** 钱账：每次付钱前后的枚数和种类，全集账平
- **K3** 服装与发型：衣服、腰带、布包、头发干湿与发型，镜与镜一致
- **K4** 光与时间：光向、时段、天色随时间推进合理，同场一致
- **K5** 站位接续：上一镜结束的位置、朝向接下一镜开始
- **K6** 环境接续：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现
- **K7** 跨场引用：台词或画面提到前面的事（面包、方向、钱），前面确实发生过

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" continuity --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\continuity__judge.md" --by "<你的模型名>/continuity__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）