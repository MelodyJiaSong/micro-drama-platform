# 修复记录：ep01 · 场六、场七 · 出片前 第 3 轮 · 11-14 23:42

本轮审查单：`ai_videos/chuanyue_yiri/reviews/ep01_20261114-234201_pregen_r3`；还没开下一轮

问题来源：issues.json

有方案的问题 11 / 59 条；严重 3，主要 8，待核实 0，记录 0；已复核通过 0，复核仍有问题 0，待复核 11；首帧换了 1 镜，分镜文字改了 2 镜。

## s6

### s6_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame.png`）
- **I10** [主要·wontfix·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：不改

### s6_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`）
- **I2** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；prompt.txt 第 12 行「再讲一句很有名的涂鸦」，changes.m
  - 方案：动作行「再讲一句很有名的涂鸦」改为「再讲一句课本上很有名的留言」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I3** [严重·implemented·待复核] Prompt 文本·T4 图文一致：T4 图文一致 最终 1 分：文字和挂的首帧、站位图、场景图一致；首帧衬衫细方格（x650–1100,y380–700）与「素色米白亚麻」不符；s7_st1 保
  - 方案：首帧第四版衬衫改纯素色亚麻、无方格无暗花；窗洞旁木挡板写进动作行；划痕同 I1
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I4** [主要·implemented·待复核] 世界物理·P1 手数：P1 手数 最终 1 分：自拍镜只剩一只手可用；每个时刻每只手在干什么、有没有多出或少掉的手；首帧年轻行人头高 160 px vs Fortunata 134 
  - 方案：行人路线改到她面前半步多（俯视 y 7.7），文字同步；她喊完右手放下垂在身侧，和行人摆手不再挤在一起
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I6** [主要·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；首帧年轻行人头高 160 px vs Fortunata 134 px → 
  - 方案：同 I4
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I8** [主要·implemented·待复核] 连续性·K3 服装与发型：K3 服装与发型 最终 1 分：衣服、腰带、布包、头发干湿与发型，镜与镜一致；衬衫胸前与袖口有一格格方格纹＋暗花（`work/continuity__a/s7s
  - 方案：同 I3：首帧衬衫改素色，和 s7 st1、st3 一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I10** [主要·wontfix·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：不改
- 分镜「动作」改了：

```diff
@@ -3,3 +3,2 @@
 女店主 Fortunata（腰带上只挂一个拳头大的小皮钱袋）站在车门左边门垛前的人行道上；
-她招客时脸是松的，眉头舒展、嘴角平，带着做生意的精神头。
 两个过路的行人（当地男人，脸刮得干净：一个年长、白短发，穿褪色蓝灰短 tunica；
```

- 分镜「走位」改了：

```diff
@@ -2,3 +2,3 @@
 0–3 秒她脸朝画左前方、目光跟着两个行人往画右移，3.5 秒起转向画面右边的 Riley。
-两个行人在人行道外沿的街面上、从 Fortunata 面前由画左走到画右（每秒一米左右），约 2.5 秒走出画右。
+两个行人在人行道上、从 Fortunata 面前半步多处由画左走到画右（每秒一米左右），约 2.5 秒走出画右。
 Riley 0 秒在画面右边画外，约 4 秒从画面右边沿人行道快步走进来，5 秒停在 Fortunata 右边约一米，两人面对面：Fortunata 在画左、Riley 在画右。
```

- 分镜「节拍」改了：

```diff
@@ -4,6 +4,6 @@
 1.5–3.5秒 Fortunata 朝两个行人吆喝 Hospitium hic locatur!
-（1.5–3.0秒），目光跟着他们往画右移；
+（1.5–3.0秒），目光跟着他们往画右移，喊完右手放下垂在身侧；
 她一开口，前面那个头也不回地抬手往外一摆，两人脚不停，约 2.5 秒走出画右；
-3.5–5秒 约 4 秒 Riley 从画面右边沿人行道快步走进画面，右手攥着钱垂在腰前，5 秒停在 Fortunata 面前、面朝她；
-Fortunata 转过脸看着她走近，目光从她的脸往下扫到长裤，再回到脸，没人说话；
+3.5–5秒 约 4 秒 Riley 从画面右边沿人行道快步走进画面，右手攥着钱，5 秒停在 Fortunata 面前、面朝她；
+Fortunata 转过脸看着她走近，目光从她的脸扫到长裤再回到脸，没人说话；
 5–6秒 Riley 笑着说 Salve!
```


## s7

### s7_st7

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st7/planning/st7_first_frame.png`）
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；首帧灯上方划痕片 x90–330,y380–650 是深色带阴影的长刺状
  - 方案：同 I1：灯上方那片划痕变浅，和 s7 st1 里同一面墙一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`

### s7_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st1/planning/st1_first_frame.png`）
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；首帧灯上方划痕片 x90–330,y380–650 是深色带阴影的长刺状
  - 方案：同 I1：灯上方那片划痕变浅，和 s7 st1 里同一面墙一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`

### s7_st2

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/_r13_candidate/st2_first_frame.png`（_r13_candidate）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`（现行）
- **I1** [严重·implemented·待复核] 时代与世界观·E5 文字：E5 文字 最终 1 分：画面里没有可读的文字、字母、数字（墙、船、招牌、钱币）；1. 送模 prompt.txt 第 12 行「画面」前半写「一小片刻得较深的
  - 方案：首帧第四版：深刻划痕抹掉，墙上只留满墙很细很淡的交叉划痕，放大看不出字形；文字改「一小片浅浅的乱划痕」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I2** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；prompt.txt 第 12 行「再讲一句很有名的涂鸦」，changes.m
  - 方案：动作行「再讲一句很有名的涂鸦」改为「再讲一句课本上很有名的留言」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I3** [严重·implemented·待复核] Prompt 文本·T4 图文一致：T4 图文一致 最终 1 分：文字和挂的首帧、站位图、场景图一致；首帧衬衫细方格（x650–1100,y380–700）与「素色米白亚麻」不符；s7_st1 保
  - 方案：首帧第四版衬衫改纯素色亚麻、无方格无暗花；窗洞旁木挡板写进动作行；划痕同 I1
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I5** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；「垂眼看一眼床头的灯苗」：灯 (0.45,0.8) 在
  - 方案：「垂眼看灯苗」改成「侧过头、低头看一眼身边小凳上的灯苗」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/overhead.toml`
- **I7** [主要·implemented·待复核] 人物逻辑·C8 听者在干什么：C8 听者在干什么 最终 1 分：别人说话或画面焦点在别人身上时，其余每个人逐秒在做什么：有手上的活、反应钉在台词的具体词上；没有站成摆件的空白段（分镜里没写动
  - 方案：念引文时左手手指在膝上轻轻点着；结尾看灯时手指捻一下衬衫下摆
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I8** [主要·implemented·待复核] 连续性·K3 服装与发型：K3 服装与发型 最终 1 分：衣服、腰带、布包、头发干湿与发型，镜与镜一致；衬衫胸前与袖口有一格格方格纹＋暗花（`work/continuity__a/s7s
  - 方案：同 I3：首帧衬衫改素色，和 s7 st1、st3 一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；首帧灯上方划痕片 x90–330,y380–650 是深色带阴影的长刺状
  - 方案：同 I1：灯上方那片划痕变浅，和 s7 st1 里同一面墙一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I11** [主要·wontfix·待复核] 母语听感·N1 / N7 / N8 / N9（R：I37）：N1 / N7 / N8 / N9（R：I37）：引文一字不差、「It says,」像念展板、四步结构（开场、定位、引文、收口）；人物回忆课本时不会这么齐整
  - 方案：不改
- 分镜「动作」改了：

```diff
@@ -1,4 +1,4 @@
 Riley 坐在床边；
-灯正上方、她右肩后的墙上有一小片刻得较深的乱划痕，方向各异的斜线交叉在一起，像随手乱抓的痕迹，颜色只比墙面略深，和满墙的细划痕连成一片；
-她一开始就正对镜头坐着，脸朝镜头、嘴角带笑，停一下才开口，轻声讲这里的住客什么墙上都写，再讲一句很有名的涂鸦：她发誓在历史课本上读过，说到 history textbook 时眉毛一扬，它出自一家和这里差不多的客栈；
+灯正上方、她右肩后的墙上有一小片浅浅的乱划痕，方向各异的斜线交叉在一起，像随手乱抓的痕迹，颜色只比墙面略深，和满墙的细划痕连成一片；
+她一开始就正对镜头坐着，脸朝镜头、嘴角带笑，停一下才开口，轻声讲这里的住客什么墙上都写，再讲一句课本上很有名的留言：她发誓在历史课本上读过，说到 history textbook 时眉毛一扬，它出自一家和这里差不多的客栈；
 两个人名放慢，念完说一句「挺甜的」，安静地笑着，垂眼看一眼灯苗。
```

- 分镜「节拍」改了：

```diff
@@ -6,4 +6,4 @@
 11.5–14秒 from an inn just like this.（11.6–13.8 秒，说到 just like this 时左手掌心朝上朝屋里轻轻一摊、目光跟着朝屋里一扫，马上看回镜头，手放回膝上）；
-14–21.5秒 It says,（14.1–14.6 秒），停半拍，"Vibius Restitutus slept here alone, and missed his Urbana."（15.0–21.0 秒，两个人名放慢，alone 后停半拍）；
+14–21.5秒 It says,（14.1–14.6 秒），停半拍，"Vibius Restitutus slept here alone, and missed his Urbana."（15.0–21.0 秒，念的时候左手手指在膝上轻轻点着，两个人名放慢，alone 后停半拍）；
 21.5–23.9秒 That's kind of sweet.（21.7–23.4 秒），说完嘴角一扬；
-23.9–26秒 她安静地笑着，垂眼看一眼床头的灯苗，不说话
+23.9–26秒 她安静地笑着，侧过头、低头看一眼身边小凳上的灯苗，手指轻轻捻一下衬衫下摆，不说话
```


