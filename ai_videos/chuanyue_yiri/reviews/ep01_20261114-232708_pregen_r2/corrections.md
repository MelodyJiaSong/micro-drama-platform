# 修复记录：ep01 · 场六、场七 · 出片前 第 2 轮 · 11-14 23:27

本轮审查单：`ai_videos/chuanyue_yiri/reviews/ep01_20261114-232708_pregen_r2`；还没开下一轮

问题来源：issues.json

有方案的问题 18 / 65 条；严重 5，主要 13，待核实 0，记录 0；已复核通过 0，复核仍有问题 0，待复核 18；首帧换了 2 镜，分镜文字改了 2 镜。

## s6

### s6_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame.png`）
- **I11** [主要·implemented·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：st1 里 Riley 改成快步走进（接 st3 眼睛一亮快步走），删掉「有点累」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`

### s6_st1

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/_r12_candidate/st1_first_frame.png`（_r12_candidate）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`（现行）
- **I1** [严重·implemented·待复核] 人物逻辑·C4 / C2：C4 / C2：视频 prompt 的「人物」段仍写 Fortunata「眼神审视、不苟言笑，但不凶」，而「画面」「动作」写「脸是松的、眉头舒展、带着做生意的精
  - 方案：人物卡 c5 外观句改成「平时眼神审视、不苟言笑，但不凶；招客、做生意时脸是松的，带着精神头」，送模人物行与动作行不再打架；首帧第三版表情松
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I2** [严重·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；首帧 Fortunata 腰间是打孔皮带＋金属方框带扣（约
  - 方案：s6 st1 首帧第三版：腰间改细皮绳挂钱袋，无皮带无金属扣，和 st2 一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I3** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；1. 本轮首帧 Fortunata 脸 x≈690、身体 
  - 方案：首帧第三版拉远：Fortunata 缩到画面横向约 24–42%、头顶约 26%，画右 43–100% 是门口与人行道留给 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I4** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；1. 本轮首帧 Fortunata 脸 x≈690、身体 x490–940，站位图预
  - 方案：同 I3；s7 st2 位置未变（上轮只改衣服），与站位一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I5** [严重·implemented·待复核] 镜头规格·F7 一镜到底：F7 一镜到底 最终 1 分：单镜内不需要切镜；镜头运动写清且做得到；1. 本轮首帧 Fortunata 脸 x≈690、身体 x490–940，站位图预测 x
  - 方案：同 I3：两人都能在中景里，一个景别到底
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I6** [主要·implemented·待复核] 世界物理·P1 手数：P1 手数 最终 1 分：自拍镜只剩一只手可用；每个时刻每只手在干什么、有没有多出或少掉的手；7.8–9 秒右手竖一根手指，之后到 11.6 秒伸右手之前右手状
  - 方案：9 秒右手放下垂在身侧，报价时只有左手四指
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I8** [主要·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；首帧行人头高 215–220 px vs Fortunata 190 px 
  - 方案：行人 2.5 秒出画右，Riley 4 秒才从画右入画，错开 1.5 秒；首帧行人和她隔一步多
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I10** [主要·implemented·待复核] 人物逻辑·C6 / C1：C6 / C1：I32 未改：行人 0–3.3s 向右走到 (8.8,8.6)，Riley 3.5s 在约 (8.0,7.4) 向左走进，间隔约 1.2m，两人
  - 方案：同 I8：出画与入画在时间上错开，不在画右同时进出
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I11** [主要·implemented·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：st1 里 Riley 改成快步走进（接 st3 眼睛一亮快步走），删掉「有点累」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I13** [主要·implemented·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；院子地面成排小方块石（x940–1500, y480–
  - 方案：首帧第三版院子铺大块长方石板，照 st2 画面
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I16** [主要·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾：prompt.txt 第 9 行「人物」：「眼神审视、不苟言笑」；第 15/17 行：「招客时脸是松的、眉头舒展、嘴角平」；首帧 png 里她还
  - 方案：同 I1：人物卡外观句不再与动作行矛盾
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I17** [主要·implemented·待复核] 角色立场·Riley·V3 表情：V3 表情 最终 1 分：我的表情和强度合不合此刻的处境；不过演、不面无表情；spec 与 prompt 动作行：「Riley 看着那四根手指」「Riley 看
  - 方案：10.5–11.6 秒 Riley 看着四根手指，抿一下嘴、有点没把握
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I18** [主要·implemented·待复核] 角色立场·路人与群众·V5 回应：V5 回应 最终 1 分：别人对我说话、做动作时，我会怎么回应、多快；分镜写的回应是不是此刻的我会给的；吆喝 1.5 s 才开口；首帧行人已在画面横向 0–25
  - 方案：她一开口，前面那个行人头也不回地抬手往外一摆，两人脚不停
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -4,3 +4,3 @@
 她招客时脸是松的，眉头舒展、嘴角平，带着做生意的精神头。
-两个过路的行人（普通路人，脸刮得干净的当地男人：一个上了年纪、白短发，穿褪色的蓝灰短 tunica；
+两个过路的行人（当地男人，脸刮得干净：一个年长、白短发，穿褪色蓝灰短 tunica；
 一个年轻、直发，穿本色亚麻短 tunica）一前一后赶路、不说话，从她面前由画左往画右走。
@@ -10,2 +10,2 @@
 钱（p2）进场攥在 Riley 右拳里（看不见），12.2 秒起她右手在两人中间摊开，掌心里 3 枚红铜小钱和 1 枚明显大一圈的金黄大黄铜币。
-画面里共 4 个人：Fortunata、Riley（约 3.5 秒入画）和两个过路的行人（约 3 秒出画）。
+画面里共 4 个人：Fortunata、Riley（约 4 秒入画）和两个过路的行人（约 2.5 秒出画）。
```

- 分镜「走位」改了：

```diff
@@ -2,4 +2,4 @@
 0–3 秒她脸朝画左前方、目光跟着两个行人往画右移，3.5 秒起转向画面右边的 Riley。
-两个行人在人行道外沿的街面上、从 Fortunata 面前由画左走到画右（每秒一米左右），约 3 秒走出画右。
-Riley 0 秒在画面右边画外，约 3.5 秒从画面右边沿人行道走进来（有点累，每秒一米二左右），5 秒停在 Fortunata 右边约一米，两人面对面：Fortunata 在画左、Riley 在画右。
+两个行人在人行道外沿的街面上、从 Fortunata 面前由画左走到画右（每秒一米左右），约 2.5 秒走出画右。
+Riley 0 秒在画面右边画外，约 4 秒从画面右边沿人行道快步走进来，5 秒停在 Fortunata 右边约一米，两人面对面：Fortunata 在画左、Riley 在画右。
 镜头在街上，几乎正对临街墙、略朝西。
```

- 分镜「节拍」改了：

```diff
@@ -5,4 +5,4 @@
 （1.5–3.0秒），目光跟着他们往画右移；
-两人摆一下手、没停，约 3 秒走出画右；
-3.5–5秒 约 3.5 秒 Riley 从画面右边沿人行道走进画面，右手攥着钱垂在腰前，5 秒停在 Fortunata 面前、面朝她；
+她一开口，前面那个头也不回地抬手往外一摆，两人脚不停，约 2.5 秒走出画右；
+3.5–5秒 约 4 秒 Riley 从画面右边沿人行道快步走进画面，右手攥着钱垂在腰前，5 秒停在 Fortunata 面前、面朝她；
 Fortunata 转过脸看着她走近，目光从她的脸往下扫到长裤，再回到脸，没人说话；
@@ -15,8 +15,8 @@
 7.8–9秒 Riley 竖起一根手指，说 One night?
-（7.9–8.6秒），Fortunata 也竖起右手一根手指，轻轻点一下头；
+（7.9–8.6秒），Fortunata 也竖起右手一根手指，轻轻点一下头，9 秒右手放下垂在身侧；
 9–10.5秒 Riley 放下左手，有点期待地等着；
 Fortunata 不说话，左手拇指拨一下挂在左胯的小皮钱袋，目光落在 Riley 攥着钱的右拳上；
-10.5–11.6秒 Fortunata 抬起左手到胸前、手心朝镜头，四根手指张开朝上、拇指折进掌心看不见，一眼数得出是四；
+10.5–11.6秒 Fortunata 抬起左手到胸前、手心朝镜头，四根手指张开朝上、拇指折进掌心看不见；
 看着 Riley 的脸平平地说 Quattuor.（10.7–11.4秒）；
-Riley 看着那四根手指；
+Riley 看着那四根手指，抿一下嘴，有点没把握；
 11.6–13秒 Fortunata 朝 Riley 伸出右手，掌心朝上停在两人中间，左手四指还竖着；
```


### s6 整场 / 未指明镜头

- **I15** [主要·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；「入画时只能是远处一座长满植被的绿山，不冒烟、不当画面主体」没标废止，紧接着又写「
  - 方案：bible §9 删掉「入画时只能是远处绿山」的旧说法，写明已被「山不入画」取代

## s7

### s7_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st1/planning/st1_first_frame.png`）
- **I11** [主要·implemented·待复核] 连续性·K8 镜间接点：K8 镜间接点 最终 1 分：逐个接点（materials/junctions.md 每一条，含没有机检标记的）判：上一镜最后一拍的位置、朝向、视线、手里的东西
  - 方案：st1 里 Riley 改成快步走进（接 st3 眼睛一亮快步走），删掉「有点累」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`

### s7_st2

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/_r12_candidate/st2_first_frame.png`（_r12_candidate）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`（现行）
- **I2** [严重·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；首帧 Fortunata 腰间是打孔皮带＋金属方框带扣（约
  - 方案：s6 st1 首帧第三版：腰间改细皮绳挂钱袋，无皮带无金属扣，和 st2 一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I4** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；1. 本轮首帧 Fortunata 脸 x≈690、身体 x490–940，站位图预
  - 方案：同 I3；s7 st2 位置未变（上轮只改衣服），与站位一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`
- **I7** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；俯视图视线点 (0.4,0.4) 与面朝夹角 133°
  - 方案：回头改成「侧过脸、眼睛往右后方的墙上瞟一眼」，站位视线点改到身侧 (0.2,1.6)
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/overhead.toml`
- **I9** [主要·implemented·待复核] 世界物理·P9 效果有来源：P9 效果有来源 最终 1 分：水花、溅泥、扬尘、影子、反光、湿脚印只出现在有来源的地方（踩在干的石头顶面不溅水，没风不扬尘）；窗洞内侧边亮蓝光晕＋墙面蓝色光束
  - 方案：s7 st2 首帧局部重画：窗洞只透很弱的冷色，去掉蓝色光晕与光束
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- **I12** [主要·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：时间够念：按正常语速（约 2.5 词/秒；语速要正常，不能靠说快塞进镜头）算出每句需要的时间与留白（开口前 ≥1 秒、说完后 ≥1.
  - 方案：台词节拍重排：history textbook 8.1–11.3、from an inn 11.6–13.8、It says 14.1–14.6、引文 15.0–21.0，语速都在 2.5 词/秒附近
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/overhead.toml`
- **I14** [主要·implemented·待复核] 时代与世界观·E5 文字：E5 文字 最终 1 分：画面里没有可读的文字、字母、数字（墙、船、招牌、钱币）；视频 prompt 第 12 行「画面」块仍写「再讲一句很有名的涂鸦」；首帧划
  - 方案：s7 st2 首帧划痕要求画浅、无阴影、看不出字形；出片后抽帧放大 14–22 秒左上墙面复查
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`
- 分镜「动作」改了：

```diff
@@ -4,3 +4,3 @@
 两个人名放慢，念完说一句「挺甜的」，安静地笑着，垂眼看一眼灯苗。
-她的两手放在膝上，说到 every wall 时转头越过右肩朝身后满是划痕的墙瞟一眼、右手拇指轻轻一指，马上转回来看镜头，语气一直轻、嘴型不张大，说到 just like this 时左手掌心朝上朝屋里轻轻一摊，每次做完都放回膝上。
+她的两手放在膝上，说到 every wall 时侧过脸、眼睛往右后方满是划痕的墙上瞟一眼、右手拇指轻轻一指，马上转回来看镜头，语气一直轻、嘴型不张大，说到 just like this 时左手掌心朝上朝屋里轻轻一摊，每次做完都放回膝上。
 西墙南段那扇厚木板门关着，在画面外。
```

- 分镜「走位」改了：

```diff
@@ -2,3 +2,3 @@
 0 秒起脸就正对镜头，窗洞在画面右上方、她身后另一侧；
-一直看着镜头说话，只在说到 every wall 时越过右肩朝身后的墙瞟一眼、说到 just like this 时目光跟着手势朝屋里一扫，每次都马上看回镜头。
+一直看着镜头说话，只在说到 every wall 时侧过脸、眼睛往右后方的墙上瞟一眼、说到 just like this 时目光跟着手势朝屋里一扫，每次都马上看回镜头。
 镜头在她正前方略偏西南，离她一米多。
```

- 分镜「节拍」改了：

```diff
@@ -1,8 +1,8 @@
 0–2.2秒 她坐在床边，脸正对镜头，灯光从画左低低地照亮她半边脸，嘴角带笑，嘴闭着，轻轻吸一口气，不说话；
-2.2–5.5秒 她轻声说 People write on, like, every wall here.（2.3–5.3 秒），说到 every wall 时头越过右肩朝身后满是划痕的墙瞟一眼、右手拇指轻轻一指，马上转回来看镜头，手放回膝上；
+2.2–5.5秒 她轻声说 People write on, like, every wall here.（2.3–5.3 秒），说到 every wall 时侧过脸、眼睛往右后方满是划痕的墙上瞟一眼、右手拇指轻轻一指，马上转回来看镜头，手放回膝上；
 整句语气轻、平，嘴型不张大，不惊呼；
 5.5–8秒 And there's this famous one —（5.7–7.6 秒）；
-8–11.2秒 I swear it was in my history textbook —（8.1–10.9 秒，说到 history textbook 时眉毛一扬）；
-11.2–13.6秒 from an inn just like this.（11.3–13.2 秒，说到 just like this 时左手掌心朝上朝屋里轻轻一摊、目光跟着朝屋里一扫，马上看回镜头，手放回膝上）；
-13.6–21.5秒 It says,（13.8–14.3 秒），停半拍，"Vibius Restitutus slept here alone, and missed his Urbana."（14.8–21.0 秒，两个人名放慢，alone 后停半拍）；
+8–11.5秒 I swear it was in my history textbook —（8.1–11.3 秒，说到 history textbook 时眉毛一扬）；
+11.5–14秒 from an inn just like this.（11.6–13.8 秒，说到 just like this 时左手掌心朝上朝屋里轻轻一摊、目光跟着朝屋里一扫，马上看回镜头，手放回膝上）；
+14–21.5秒 It says,（14.1–14.6 秒），停半拍，"Vibius Restitutus slept here alone, and missed his Urbana."（15.0–21.0 秒，两个人名放慢，alone 后停半拍）；
 21.5–23.9秒 That's kind of sweet.（21.7–23.4 秒），说完嘴角一扬；
```


### s7 整场 / 未指明镜头

- **I15** [主要·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；「入画时只能是远处一座长满植被的绿山，不冒烟、不当画面主体」没标废止，紧接着又写「
  - 方案：bible §9 删掉「入画时只能是远处绿山」的旧说法，写明已被「山不入画」取代

