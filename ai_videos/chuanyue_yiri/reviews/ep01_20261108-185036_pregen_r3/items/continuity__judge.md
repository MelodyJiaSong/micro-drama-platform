你是裁决人 **continuity__judge**（claude · claude-opus-5-5），裁「连续性」审稿项 continuity 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reconcile\continuity.md`。

## 两份报告
- a 位（claude-opus-5-5/continuity__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\continuity__a.md`
- b 位（gpt-6.1-sol/continuity__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\continuity__b.md`

## 要裁的维度
- **K2**（抽查）钱账：a 2 分（全集钱账算得平：开场 7 红铜＋1 浅色小铜币＋1 大黄铜币＝9 枚；s3_st1 付 2 红铜→7 枚；s4_st2 拿出 1 枚、s4_st5 放回→7 枚；s8_st2 付浅色小铜币→6 枚（5＋1）；s5_st3 付 2 红铜→4 枚（3＋1）；s6_st2 付 3 红铜＋1 大黄铜币→0 枚；s7_st1「Budget? …Gone.」对得上。s6_st2 首帧放大，掌心正好 3 铜＋1 金黄大币（z_s6_st2_coins.jpg）。小瑕疵：s5_st12 道具行写「钱在裤袋里」，s5_st3 第 0 秒钱已经攥在右拳里，掏钱换手在两镜之间的画外完成（问题表记录））；b 3 分（起始 7 as＋1 quadrans＋1 sestertius＝9 枚；s3_st1 支出 2 as 后 7 枚，s8_st2 支出 quadrans 后 6 枚，s5_st3 支出 2 as 后 4 枚，s6_st2 支出最后 3 as＋大币后为 0；s4_st2→st5 取闻一枚又放回，无消费；s6_st2 FF 右掌可数三红一黄。）
- **K3**（抽查）服装与发型：a 3 分（58 张首帧逐张核对：米白亚麻短袖衬衫袖口挽起、橄榄色腰带、卡其工装裤、深棕短靴全集一致；乌黑波浪长发一直披散，s8_st4/st5/st9/st6/st7 首帧头发干蓬松、只有鬓角汗湿；布包 s3_st7 第 8.5 秒才系上（st7 首帧腰带左侧空着），s3_st4/st8、s4_st1/st4、s8_st1/st2/st3/st8/st7、s5_st8/st2/st12/st3/st14/st13 都在左胯，s5_st7 起腰带空着，s6、s7 都没有布包，前后对得上；Vibia（红披巾＋赭黄裙＋发簪髻）、Felix、Asellina、Fortunata、门房、Helvia 的服装在各自的镜头之间一致）；b 2 分（s8_st5／st9／st6 FF 均是 Riley 左胯、靠两人之间的包，长布角连回左腰；全范围米白短袖、卡其裤、橄榄腰带、披散长发保持。st5／st9 胸前发梢仍略成细束，较 st4 与门外 st7 蓬松度低，湿发观感存疑，见 C07，未当作已证实整头湿干跳变。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\continuity__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3" continuity --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185036_pregen_r3\reports\continuity__judge.md" --by "<你的模型名>/continuity__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）