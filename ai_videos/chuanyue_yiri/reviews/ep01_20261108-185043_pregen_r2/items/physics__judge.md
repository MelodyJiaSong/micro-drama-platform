你是裁决人 **physics__judge**（claude · claude-opus-5-5），裁「世界物理」审稿项 physics 的分歧并抽查两位都判通过的维度。
审稿说明：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\BRIEF.md`；对比表：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reconcile\physics.md`。

## 两份报告
- a 位（claude-opus-5-5/physics__a）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\physics__a.md`
- b 位（gpt-6.1-sol/physics__b）：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\physics__b.md`

## 要裁的维度
- **P5**（抽查）身体可行：a 2 分（st3 Riley 0–4 秒走 4.6 m（1.15 m/s），挑夫+骡子 14.4 m/14 s≈1.03 m/s；st5 Riley 0–3 秒 3.42 m、3–5 秒 2.34 m（≈1.15 m/s），第 3 秒迈 40 cm 路沿；st5 驴 0–13 秒全程约 1.13 m/s 匀速；小瑕疵：st4 2.5–5 秒年轻渔夫从 (38.44,54.05) 到 (35.9,54.7) 要走 2.62 m，还要丢绳、转身 180°、弯腰，全部塞进 2.5 秒；扣掉约 0.8 秒的松绳转身和弯腰，约 1.5 秒走 2.62 m，相当于 1.7 m/s 小跑（问题表 #4））；b 3 分（st1 第 2.5–3.5 秒转身、3.5–4.5 秒走约 0.6 米，10–12 秒转腰配右脚后挪；st3 Riley 前 4 秒走 4.6 米，随后减速，6.5–7.5 秒整身转向镜头；工人已改为小筐、半筐灰浆并给 3 秒提举。st4 返回船边的年轻渔夫走约 2.62 米／2.5 秒＝1.05 米／秒，抬筐另给 3 秒。st5 前 3 秒走约 3.42 米，路沿约 0.4 米高且明确抬脚、抬身，均无文字上必须滑步或扭颈才能完成的动作。）
- **P6**（抽查）穿模与距离：a 2 分（st3 Riley x=30.7 与工人 x=32.3 相距 1.6 m；通道净宽按俯视图约 3.2 m（29.4–32.6）；st5 Riley 第 5 秒在 (8.4,8.6)，驴中心线 x=11.25，相距 2.85 m；小瑕疵：st4 首帧年长渔夫那根绳从船头结穿过年轻渔夫胯前（st4_ropes.png 绳贴在他的 tunica 上）；st3 第 0 秒骡子右侧驮筐外缘离弯腰工人的头只有约 0.2 m（首帧约 30 px，按小腿换算约 155 px/m）；st5 赶驴人走在驴靠机位一侧，离机位约 1.1 m，不是 changes 说的 1.5 m 以上（问题表 #3、#5、#6））；b 3 分（st3 overhead.toml:40、49 的 Riley 路线 x=30.7、工人 x=32.3，侧向中心距 1.6 米，骡队先行且第 10 秒过通道；st4 船头 x=36.7→37.5，年轻渔夫 x=37.54→38.44，连同 y 差的中心距约 0.93→1.04 米，倒退安排消除了船向静止腿部推进的问题。st5 Riley 停在 (8.4,8.6)，驴队第 7 秒在 (11.25,8.6)，中心距 2.85 米，人走驴靠 Riley 一侧仍约隔 2.6 米，路线不再贴身横穿。）

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

报告写到：`C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\physics__judge.md`

最后一步自己登记裁决：
`python tools/review_run.py adjudicate "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2" physics --report "C:\workspace\micro-drama-platform\ai_videos\chuanyue_yiri\reviews\ep01_20261108-185043_pregen_r2\reports\physics__judge.md" --by "<你的模型名>/physics__judge"`
（在仓库根目录 C:\workspace\micro-drama-platform 运行。）