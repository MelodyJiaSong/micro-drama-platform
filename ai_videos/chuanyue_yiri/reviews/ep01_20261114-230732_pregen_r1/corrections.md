# 修复记录：ep01 · 场六、场七 · 出片前 第 1 轮 · 11-14 23:07

本轮审查单：`ai_videos/chuanyue_yiri/reviews/ep01_20261114-230732_pregen_r1`；还没开下一轮

问题来源：issues.json

有方案的问题 16 / 63 条；严重 7，主要 9，待核实 0，记录 0；已复核通过 0，复核仍有问题 0，待复核 16；首帧换了 2 镜，分镜文字改了 1 镜。

## s6

### s6_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame.png`）
- **I9** [主要·wontfix·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：不改

### s6_st1

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/_r11_candidate/st1_first_frame.png`（_r11_candidate）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`（现行）
- **I1** [严重·implemented·待复核] 人物逻辑·C3 视线：C3 视线 最终 1 分：每个时刻每个人看向谁，合理（不无缘无故看镜头、不无视身边的怪事）；st1_first_frame.png 里 Fortunata 的头
  - 方案：首帧重画：Fortunata 头和眼睛朝画左看行人；行人改成看前面的街、不看镜头、不说话
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I2** [严重·implemented·待复核] 人物逻辑·C4 / C2：C4 / C2：首帧 Fortunata 皱眉冷脸，不是「脸是松的、眉头舒展、带着做生意的精神头」；而 prompt「人物」里 Fortunata 是「眼神审视
  - 方案：首帧 prompt 删掉「眼神审视、不苟言笑」，改写招客时脸是松的、眉头舒展、不皱眉不眯眼；重画
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I3** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；1. 首帧 Fortunata 在画中央 x≈820，站位
  - 方案：s6 st1 首帧按站位图重画：Fortunata 移到画左约 30–55%、缩到大腿以上，画右半边空出给 Riley；s7 st2 首帧中近景与站位一致（只改衣服）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I4** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；1. 首帧 Fortunata 在画中央 x≈820，站位图预测 x≈532。<br
  - 方案：同 I3：首帧人物位置按站位图重排
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I5** [严重·implemented·待复核] 镜头规格·F7 一镜到底：F7 一镜到底 最终 1 分：单镜内不需要切镜；镜头运动写清且做得到；1. 首帧 Fortunata 在画中央 x≈820，站位图预测 x≈532。<br>2.
  - 方案：首帧与镜头行都是中景双人一个景别到底，Riley 入画位置留在画右半边，不再需要切近景
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I6** [严重·implemented·待复核] Prompt 文本·T4 图文一致：T4 图文一致 最终 1 分：文字和挂的首帧、站位图、场景图一致；overhead_ref：Fortunata 5 秒后朝东面向 Riley、机位在她正南；「手
  - 方案：四指改为左手抬到胸前、手心朝镜头，镜头看得到四指正面
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I7** [严重·implemented·待复核] 角色立场·Fortunata·V3 表情：V3 表情 最终 1 分：我的表情和强度合不合此刻的处境；不过演、不面无表情；首帧 Fortunata 眯眼斜视、嘴唇抿紧、眉心微锁（st1_ff_face.p
  - 方案：同 I2：首帧表情改松
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I9** [主要·wontfix·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：不改
- **I11** [主要·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；首帧衬衫是清楚的细格纹，腰带是深棕皮带＋金属扣（work/
  - 方案：s7 st2 首帧局部重画：素色米白亚麻衬衫、橄榄色帆布腰带，脸与其余不变
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I12** [主要·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数 最终 1 分：动作节拍的秒数排得下（走多远、几秒到），没有挤压；1.5 秒内要做 5 件事：右手放下、拇指拨钱袋、目光从脸扫到靴、瞥一眼身后的街
  - 方案：9–10.5 秒只留：左手拇指拨一下钱袋、目光落在她右拳；打量（脸→长裤→脸）挪到 3.5–5 秒她走近时
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I13** [主要·implemented·待复核] Prompt 文本·T7·节拍过满、靴子出画：T7·节拍过满、靴子出画：动作 9–10.5 秒：放手、拨钱袋、扫脸→靴子→身后街→右拳，1.5 秒 4 个视线目标；构图膝盖以上，靴子拍不到
  - 方案：同 I12，并把「扫到靴子」改成「扫到长裤」（中景拍不到靴子）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I14** [主要·implemented·待复核] 角色立场·Fortunata·V7 本集内一致：V7 本集内一致：st1 节拍 10.5–11.6 秒「四根并排竖直朝上、拇指折在掌心里」；st2（已出片）动作首句与首帧「四指张开朝上、拇指弯进掌心」；切点同
  - 方案：st1 四指改成「四根手指张开朝上、拇指折进掌心看不见」，和已出片的 st2 开头一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I15** [主要·implemented·待复核] 角色立场·Fortunata·V4 视线：V4 视线：9–10.5 秒 1.5 秒内要做：右手放下、拇指拨钱袋、目光脸→靴子、瞥身后街、落到右拳，共 4 个视线落点；3.5–5 秒 Riley 走近时我
  - 方案：3.5–5 秒 Riley 走近时 Fortunata 转脸看她、目光从脸扫到长裤再回到脸
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I16** [主要·implemented·待复核] 角色立场·路人与群众·V7 跨集一致：V7 跨集一致 最终 1 分：跨集一致：和行为档案（人物目录 behavior.md）、前几集的我对照——说话方式、口头禅、对陌生人的态度、肢体习惯、表情分寸、
  - 方案：st1 行人换成一老（白短发、褪色蓝灰 tunica）一少（直发、本色亚麻 tunica），和 st6 车夫、st3 铺子主人的褐衣卷发区分开
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- 分镜「动作」改了：

```diff
@@ -4,3 +4,4 @@
 她招客时脸是松的，眉头舒展、嘴角平，带着做生意的精神头。
-两个过路的行人（普通路人，脸刮得干净的当地男人，穿褐色和灰色短 tunica）侧脸相对、边走边低声聊着，从她面前由画左往画右走。
+两个过路的行人（普通路人，脸刮得干净的当地男人：一个上了年纪、白短发，穿褪色的蓝灰短 tunica；
+一个年轻、直发，穿本色亚麻短 tunica）一前一后赶路、不说话，从她面前由画左往画右走。
 Riley 从画右走来，两人互道 Salve；
```

- 分镜「走位」改了：

```diff
@@ -6,2 +6,2 @@
 配角：Fortunata 先招呼过路的人，Riley 走来后一直看着她：只看手势，在想「一个外地女人，一个人，付得起吗」。
-两个行人只顾聊天。
+两个行人只顾赶路。
```

- 分镜「节拍」改了：

```diff
@@ -1,9 +1,9 @@
-0–1.5秒 Fortunata 脸是松的，嘴闭着，看着从画面左边走来的两个行人，右手抬到肩边、手心朝着自己朝他们往回招两下；
-两个行人侧脸相对，边聊边从画面左边往右走；
-Riley 还没入画，没人说话；
+0–1.5秒 Fortunata 脸是松的、眉头舒展，嘴闭着，看着从画面左边走来的两个行人，右手抬到肩边、手心朝着自己往回招两下；
+两个行人一前一后赶路、不说话，从画面左边往右走；
+Riley 还没入画；
 1.5–3.5秒 Fortunata 朝两个行人吆喝 Hospitium hic locatur!
-（1.5–3.0秒），目光跟着他们；
-两人照样边聊边走，约 3 秒走出画右；
+（1.5–3.0秒），目光跟着他们往画右移；
+两人摆一下手、没停，约 3 秒走出画右；
 3.5–5秒 约 3.5 秒 Riley 从画面右边沿人行道走进画面，右手攥着钱垂在腰前，5 秒停在 Fortunata 面前、面朝她；
-Fortunata 转过脸看她，没人说话；
+Fortunata 转过脸看着她走近，目光从她的脸往下扫到长裤，再回到脸，没人说话；
 5–6秒 Riley 笑着说 Salve!
@@ -17,4 +17,4 @@
 9–10.5秒 Riley 放下左手，有点期待地等着；
-Fortunata 不说话，右手放下来，拇指拨一下腰间的小皮钱袋，目光从 Riley 的脸扫到靴子，朝她身后的街上瞥一眼，落在她攥钱的右拳上；
-10.5–11.6秒 Fortunata 抬起左手到胸前，竖起四根手指：食指、中指、无名指、小指四根并排竖直朝上，拇指折在掌心里、被四根手指挡住看不见，手心朝 Riley，一眼数得出是四；
+Fortunata 不说话，左手拇指拨一下挂在左胯的小皮钱袋，目光落在 Riley 攥着钱的右拳上；
+10.5–11.6秒 Fortunata 抬起左手到胸前、手心朝镜头，四根手指张开朝上、拇指折进掌心看不见，一眼数得出是四；
 看着 Riley 的脸平平地说 Quattuor.（10.7–11.4秒）；
```


### s6_st2

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/st2_first_frame.png`）
- **I9** [主要·wontfix·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：不改
- **I14** [主要·implemented·待复核] 角色立场·Fortunata·V7 本集内一致：V7 本集内一致：st1 节拍 10.5–11.6 秒「四根并排竖直朝上、拇指折在掌心里」；st2（已出片）动作首句与首帧「四指张开朝上、拇指弯进掌心」；切点同
  - 方案：st1 四指改成「四根手指张开朝上、拇指折进掌心看不见」，和已出片的 st2 开头一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`

### s6_st6

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st6/planning/st6_first_frame.png`）
- **I16** [主要·implemented·待复核] 角色立场·路人与群众·V7 跨集一致：V7 跨集一致 最终 1 分：跨集一致：和行为档案（人物目录 behavior.md）、前几集的我对照——说话方式、口头禅、对陌生人的态度、肢体习惯、表情分寸、
  - 方案：st1 行人换成一老（白短发、褪色蓝灰 tunica）一少（直发、本色亚麻 tunica），和 st6 车夫、st3 铺子主人的褐衣卷发区分开
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`

## s7

### s7_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st1/planning/st1_first_frame.png`）
- **I8** [主要·wontfix·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；s7_st1 已出片末帧（17.8 秒）她转头越过右肩看画左划痕；st2 改稿后（`git d
  - 方案：不改
- **I9** [主要·wontfix·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：不改

### s7_st2

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/_r11_candidate/st2_first_frame.png`（_r11_candidate）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`（现行）
- **I3** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；1. 首帧 Fortunata 在画中央 x≈820，站位
  - 方案：s6 st1 首帧按站位图重画：Fortunata 移到画左约 30–55%、缩到大腿以上，画右半边空出给 Riley；s7 st2 首帧中近景与站位一致（只改衣服）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I4** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；1. 首帧 Fortunata 在画中央 x≈820，站位图预测 x≈532。<br
  - 方案：同 I3：首帧人物位置按站位图重排
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I6** [严重·implemented·待复核] Prompt 文本·T4 图文一致：T4 图文一致 最终 1 分：文字和挂的首帧、站位图、场景图一致；overhead_ref：Fortunata 5 秒后朝东面向 Riley、机位在她正南；「手
  - 方案：四指改为左手抬到胸前、手心朝镜头，镜头看得到四指正面
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I8** [主要·wontfix·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；s7_st1 已出片末帧（17.8 秒）她转头越过右肩看画左划痕；st2 改稿后（`git d
  - 方案：不改
- **I9** [主要·wontfix·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：不改
- **I10** [主要·wontfix·待复核] 母语听感·N2 / N7 / N9：N2 / N7 / N9：全镜是一段完整结构的演讲，引文一字不差，真人更碎、更随口
  - 方案：不改
- **I11** [主要·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；首帧衬衫是清楚的细格纹，腰带是深棕皮带＋金属扣（work/
  - 方案：s7 st2 首帧局部重画：素色米白亚麻衬衫、橄榄色帆布腰带，脸与其余不变
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`

