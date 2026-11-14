你是裁决人 **physics_A__judge**（claude · claude-opus-5-5），裁「世界物理」审稿项 physics_A 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reconcile\physics_A.md`。

## 两份报告
- a 位（claude-opus-5-5/physics_A__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\physics_A__a.md`
- b 位（gpt-6-astra/physics_A__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\physics_A__b.md`

## 要裁的维度
- **P3**（抽查）交接三段：a 2 分（钱、面包、布包的交接都分三步写清了。s3_st1 6.5–8.5 秒她把钱放在面前石台外沿，8.5–10 秒 Felix 探身把钱拨到手边、拢进碗（碗在 (6.2,4.2)，离他约 0.6 m）；s3_st7 7–8.5 秒交接在石台正上方，两人相距 1.4 m，Riley 右手接布结、左手托底，Felix 收手。小瑕疵：s3_st1 10–11.5 秒 Felix 不挪步，「侧过身」去拿那一摞里的面包，那一摞在 (6.7,4.3)，离他 (5.8,3.75) 约 1.05 m，伸手会偏远。）；b 3 分（s3_st1 6.5–8.5 秒左裤袋→左手两枚钱→石台外沿，8.5–10 秒 Felix 收到碗，10–11.5 秒库存面包→手→她面前石台；s3_st7 7–8.5 秒 Felix 捏结递出，Riley 右手接结、左手托底，8.5–11 秒双手将长布角系到左腰带；两人中心距已从约 2 米改为 1.4 米且同时探身。交接来源、接触与最终支撑可对应。）
- **P4**（抽查）重力与支撑：a 2 分（水罐都有支撑。s2_st7 首帧罐底坐在槽沿上（x≈750–950，y≈820），s2_st8 首帧在 x≈1030–1180、y≈660，s2_st4 首帧在 x≈600–680、y≈520；s2_st5 首帧水柱落进罐口，上面的手扣着罐口沿、下面的手托着罐底（work/s2st5_hands.png）；s3 的托板都是两手平端，碗和面包都放在台面上。瑕疵：一是 s2 全场光线写成「太阳在喷泉对面（西）那排房子的屋顶后面」，清晨的太阳在西边，不合物理；st2、st5 首帧里还能看到太阳本身。二是垫脚石高度前后不一：st1 写「高出路面约一掌半，和人行道一样高」，st3 prompt 写路缘「高出路面约四十厘米」。这两条都是记录级。）；b 3 分（s2_st5 0 秒画左水柱进入罐口，双手扶托罐；1.5–3 秒提起放槽沿，st7 / st8 首帧罐底落在槽沿。s3_st2 0 秒圆面包落台面，右掌压住；s3_st5 3–8 秒长柄铲托面包再滑到炉旁砖台，粉末写向下撒落；s3_st6 5.5–8 秒先放托板再摆面包。当前图及文字未发现无支撑悬浮；尚无本轮视频可验证水流、火焰和粉末的逐帧运动。）

## 全部评分维度
- **P1** 手数：自拍镜只剩一只手可用；每个时刻每只手在干什么、有没有多出或少掉的手
- **P2** 道具来源与去向：每件道具进场时在哪、出场时在哪；没有凭空出现或消失
- **P3** 交接三段：交接写清从哪拿、交到哪、对方怎么握住或收起；钱、灯、刮板都要
- **P4** 重力与支撑：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对
- **P5** 身体可行：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步
- **P6** 穿模与距离：人、动物、道具之间的距离够，走位路线不穿墙、不撞人
- **P7** 服装与动作相容：衣服允许这个动作（短袖不能卷袖、塞进腰里的下摆不会自己跑出来）
- **P8** 首帧 = 第 0 秒：首帧画的正是第 0 秒的状态，和节拍第一拍接得上

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\physics_A__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2" physics_A --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-153205_pregen_r2\reports\physics_A__judge.md" --by "<你的模型名>/physics_A__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）