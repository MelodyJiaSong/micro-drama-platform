# 修复记录：ep01 · 场二到场八 · 出片前 第 3 轮 · 11-08 18:50

本轮审查单：`ai_videos/chuanyue_yiri/reviews/ep01_20261108-185036_pregen_r3`；还没开下一轮

问题来源：issues.json

有方案的问题 117 / 117 条；严重 37，主要 12，待核实 16，记录 52；已复核通过 0，复核仍有问题 0，待复核 117；首帧换了 14 镜，分镜文字改了 57 镜。

## s2

### s2_st3

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/_r3_before/st3_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame.png`（现行）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I39** [主要·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；s3st5_flour.png：下磨石一圈是一道道竖直往下淌、带反光的
  - 方案：s3_st5 首帧局部修成干面粉，文字写干燥细白面粉簌簌撒落，负面词加「往下流的液体、水帘、湿亮的条痕、面糊」；s2 光线行按绝对方位逐镜写，s2_st1/st3 首帧压暗东侧；s3_st7 布包写左前臂支撑；垫脚石统一「高出路面约四十厘米」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/st5_first_frame_prompt.txt`
- **I40** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml Riley path `[
  - 方案：s3_st7 8.5 s 面朝点改回 Felix；s2_st2 删掉 7.3 s 的转身；s2_st8 改上身左拧、从左肩回头用眼角看；s2_st5 节拍拆成接水 / 提罐稳放 / 听见外国话直腰转头 / 目光下扫
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- 分镜「光线」改了：

```diff
@@ -1,4 +1,6 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜镜头在西侧人行道上朝东拍：受光的西侧墙在镜头身后，正对镜头的东侧铺面整面在柔和的阴影里，只有屋檐上方的天空发亮；
 只有自然光。
```


### s2_st1

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/_r3_before/st1_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame.png`（现行）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I24** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；overhead Vibia 离镜头 3.5 m（在 Ri
  - 方案：s2_st8 文字与 overhead 改成 Vibia 在 Riley 身后约一米（贴首帧）；s2_st4 起点与擦肩提前到 0–1.5 s；s2_st1 机位改为垫脚石南约 2.5 m、离地 0.5 m；s8_st8 两位妇女站位对调贴首帧；s3_st6 机位推到 (5.8,6.0)、标中近景
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st6/planning/overhead.toml`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I39** [主要·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；s3st5_flour.png：下磨石一圈是一道道竖直往下淌、带反光的
  - 方案：s3_st5 首帧局部修成干面粉，文字写干燥细白面粉簌簌撒落，负面词加「往下流的液体、水帘、湿亮的条痕、面糊」；s2 光线行按绝对方位逐镜写，s2_st1/st3 首帧压暗东侧；s3_st7 布包写左前臂支撑；垫脚石统一「高出路面约四十厘米」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/st5_first_frame_prompt.txt`
- **I40** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml Riley path `[
  - 方案：s3_st7 8.5 s 面朝点改回 Felix；s2_st2 删掉 7.3 s 的转身；s2_st8 改上身左拧、从左肩回头用眼角看；s2_st5 节拍拆成接水 / 提罐稳放 / 听见外国话直腰转头 / 目光下扫
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- 分镜「动作」改了：

```diff
@@ -2,3 +2,3 @@
 深灰色的玄武岩大石板路面，一道浅浅的清水顺着路面哗哗流下；
-路中间横排着三块椭圆的大垫脚石，石头顶面和两边的人行道一样高，高出路面和水面约一掌半，石头之间留着让车轮过的缝。
+路中间横排着三块椭圆的大垫脚石，石头顶面和两边的人行道一样高（高出路面约四十厘米），石头之间留着让车轮过的缝。
 Riley 从画左的人行道边平着迈上第一块石头，在三块石头之间轻快地一步一跳，再平着迈上画右（喷泉那一侧）的人行道，修长的腿迈得很轻快，靴底在湿石头上踩稳，每一步都落在石面上；
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-镜头在西边人行道上、垫脚石南边约四米，离地约三十厘米，朝北偏东斜看三块垫脚石；
+镜头在西边人行道上、垫脚石南边约两米半，离地约半米，朝北偏东斜看三块垫脚石；
 她从画左（西边人行道）走到画右（东边人行道），横过画面，再往画右走出画面；
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
-他拍，低机位，离地约三十厘米、微微朝下，离石头约四米，斜着拍她的腿和靴子踩过三块垫脚石，画面上缘在她腰部，流水在前景；
+他拍，低机位，离地约半米、微微朝下，离石头约两米半，斜着拍她的腿和靴子踩过三块垫脚石，画面上缘在她腰部，流水在前景；
 一种运镜：横摇，镜头跟着她往右摇约二十度，第 4.5 秒停住，停在第三块石头和画右的路缘上，她约第 6 秒从画右走出画面。
```

- 分镜「光线」改了：

```diff
@@ -1,4 +1,7 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜画左是西侧墙，上半截受光；
+画右远处的东侧店面在阴影里；
 只有自然光。
```


### s2_st2

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st2/planning/st2_first_frame.png`）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I40** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml Riley path `[
  - 方案：s3_st7 8.5 s 面朝点改回 Felix；s2_st2 删掉 7.3 s 的转身；s2_st8 改上身左拧、从左肩回头用眼角看；s2_st5 节拍拆成接水 / 提罐稳放 / 听见外国话直腰转头 / 目光下扫
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- **I85** [记录·implemented·待复核] 人物逻辑·C1（I56 未改）：C1（I56 未改）：overhead 里 Riley 离喷泉约 3.5 m；st2 她说 11 秒话，Vibia 在 st5 才转头，没有写「听见英语」；st
  - 方案：s2_st5 节拍加「2.6–3.4 s 听见身后有人大声说外国话，直腰转头」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- **I89** [记录·implemented·待复核] 人物逻辑·C1 / C4 / C7 / R · 注意的触发：C1 / C4 / C7 / R · 注意的触发：两人位置约为 Riley(15,21)、Vibia(14.3,23.75)，相距约 2.84 米。st5 ov
  - 方案：s2_st5 触发统一为听见身后的外国话后直腰转头，分镜和 toml 同步；v13 重编、overhead 重出
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-11
+18
```

- 分镜「动作」改了：

```diff
@@ -4,3 +4,4 @@
 她轻松地讲这条街就是排水沟；
-说到 the street IS the drain 时左手朝身后的路面一摊，说到 stepping stones 时左手拇指越过左肩朝身后的垫脚石一指，马上放下。
+说到 the drain 时左手朝身后的路面一摊，说到 stepping stones 时左手拇指越过左肩朝身后的垫脚石一指，马上放下；
+说到 whatever's in there 时皱一下鼻子。
 喷泉和接水的女人在镜头左边的画外。
```

- 分镜「节拍」改了：

```diff
@@ -1,4 +1,6 @@
 0–1.5秒 她刚跳上人行道，回过身对着镜头喘口气笑，还没开口；
-1.5–6.5秒 说 No sewers on most of these streets — the street IS the drain.，说到 drain 时左手朝身后的路面一摊，说完停半拍；
-6.5–9.5秒 说 That's what the stepping stones are for.，说到 stepping stones 时左手拇指越过肩膀朝身后的垫脚石一指，马上放下；
-9.5–11秒 说完她看着镜头笑着点点头，嘴闭着
+1.5–3秒 说 Okay, made it.；
+3–8.5秒 说 So there's no sewer here — the street basically is the drain.，说到 drain 时左手朝身后的路面一摊，说完停半拍；
+8.5–13秒 说 That's why they've got these big stepping stones,，说到 stepping stones 时左手拇指越过肩膀朝身后的垫脚石一指，眼睛一直看着镜头，马上放下；
+13–16.5秒 说 so you don't have to walk through… whatever's in there.，through… 之后停一下，说 whatever's in there 时皱一下鼻子；
+16.5–18秒 说完她看着镜头笑着点点头，嘴闭着
```

- 分镜「光线」改了：

```diff
@@ -1,4 +1,6 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜镜头朝西：她身后正对镜头的西侧铺面上半截受光，她自己站在东侧墙下的阴影里；
 只有自然光。
```

- 分镜「台词」改了：

```diff
@@ -1 +1,3 @@
-Riley（轻松讲解，美式英语）：No sewers on most of these streets — the street IS the drain. That's what the stepping stones are for.
+Riley（轻松讲解，美式英语；
+刚过完街还有点喘；
+through… 之后停一下，说 whatever's in there 时皱一下鼻子）：Okay, made it. So there's no sewer here — the street basically is the drain. That's why they've got these big stepping stones, so you don't have to walk through… whatever's in there.
```


### s2_st5

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/st5_first_frame.png`）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I22** [严重·implemented·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；首帧左上高窗是木框加竖条、横条的分格窗（z_s8st2
  - 方案：s8_st2 首帧局部修成光秃的方窗洞，ffp 负面词加「窗格、窗框分格、带玻璃的窗」；s3_st8 首帧去掉墙上竖管，负面词加「墙上的竖管、落水管」；s2_st5/st7 文字删掉石块形状描写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/st2_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I40** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml Riley path `[
  - 方案：s3_st7 8.5 s 面朝点改回 Felix；s2_st2 删掉 7.3 s 的转身；s2_st8 改上身左拧、从左肩回头用眼角看；s2_st5 节拍拆成接水 / 提罐稳放 / 听见外国话直腰转头 / 目光下扫
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- **I85** [记录·implemented·待复核] 人物逻辑·C1（I56 未改）：C1（I56 未改）：overhead 里 Riley 离喷泉约 3.5 m；st2 她说 11 秒话，Vibia 在 st5 才转头，没有写「听见英语」；st
  - 方案：s2_st5 节拍加「2.6–3.4 s 听见身后有人大声说外国话，直腰转头」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- **I89** [记录·implemented·待复核] 人物逻辑·C1 / C4 / C7 / R · 注意的触发：C1 / C4 / C7 / R · 注意的触发：两人位置约为 Riley(15,21)、Vibia(14.3,23.75)，相距约 2.84 米。st5 ov
  - 方案：s2_st5 触发统一为听见身后的外国话后直腰转头，分镜和 toml 同步；v13 重编、overhead 重出
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- 分镜「动作」改了：

```diff
@@ -2,9 +2,10 @@
 镜头站在喷泉北边的人行道上，顺着街朝喷泉看（朝南）：画左是东侧店铺的墙，牛头出水口在石槽靠墙的那一头（画面中间偏左），石槽从画左伸到画中；
-画右是深灰色玄武岩石块铺的路面：一块块圆角的小石块大致成行铺开，被流水打湿发亮，朝画面深处延伸。
+画右是深灰色玄武岩石块铺的路面，被流水打湿发亮，朝画面深处延伸。
 接水的女人 Vibia 在画面中间偏右，站在石槽靠街这一角的外面，侧背对镜头，弯腰探过槽沿，把一只两耳的赭红色陶水罐伸到牛头出水口下，水柱直接落进罐口、溅起水花；
 右手托着罐底，左手握着罐颈。
-罐子接满后，她两手把罐子提起来，搁在身前石槽靠街这一角的槽沿上，直起腰，转过头一抬眼就看见了画外的 Riley：先看她的脸，然后目光慢慢往下扫，扫过腰，落在她的腿上，停在那儿。
+罐子接满后，她两手把罐子提起来，搁在身前石槽靠街这一角的槽沿上；
+身后人行道上有人大声说着听不懂的外国话，她直起腰，转过头一抬眼就看见了画外的 Riley：先看她的脸，然后目光慢慢往下扫，扫过腰，落在她的腿上，停在那儿。
 道具：水罐从出水口下面 → 她两手提起 → 搁在她身前的槽沿上（出场时在槽沿上，满的，她两手扶着）。
-配角——Vibia：此刻看着画外的 Riley（视线落在镜头左边约一拳、和镜头差不多高的地方，Riley 在镜头左后方），先是好奇「这人是谁」，目光扫到裤子时变成「女人怎么穿着男人的裤子？
-」；
+配角——Vibia：此刻看着画外的 Riley（视线落在镜头左边：先在和镜头差不多高的地方看她的脸，再往下落到偏低处看她的腿；
+Riley 在镜头左后方），先是好奇，目光扫到裤子时变成困惑：一个女人穿着男人的裤子；
 这一镜她的眉毛还平着，表情愣住、困惑，嘴抿着。
```

- 分镜「走位」改了：

```diff
@@ -2,2 +2,2 @@
 Riley 在镜头左后方的画外。
-女人转头看 Riley 时，视线落在镜头左边一点，眼睛看着自己的事。
+女人转头看 Riley 时，视线落在镜头左边，先平视、再往下。
```

- 分镜「节拍」改了：

```diff
@@ -1,4 +1,5 @@
-0–1.5秒 女人弯腰接水，水柱哗哗落进罐口，她低头看着罐子；
-1.5–3秒 罐子满了，她两手把罐子提起来搁在身前的槽沿上，直起腰，转过头抬眼看向画外的 Riley，目光先落在 Riley 的脸上；
-3–5秒 她的目光从 Riley 的脸慢慢往下扫，下巴微微一低，视线停在画外 Riley 的腿上，表情愣住、困惑，嘴抿着；
+0–1.2秒 女人弯腰接水，水柱哗哗落进罐口，她低头看着罐子；
+1.2–2.6秒 罐子满了，她两手把罐子提起来，稳稳搁在身前的槽沿上；
+2.6–3.4秒 听见身后有人大声说外国话，她直起腰，转过头抬眼看向画外的 Riley，目光先落在 Riley 的脸上；
+3.4–5秒 她的目光从 Riley 的脸慢慢往下扫，下巴微微一低，视线停在画外 Riley 的腿上，表情愣住、困惑，嘴抿着；
 5–7秒 她就那样盯着看，直着腰，两手扶着槽沿上的满水罐，一动不动
```

- 分镜「光线」改了：

```diff
@@ -1,4 +1,6 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜镜头朝南：画右西侧那排墙上半截受光，画左东侧的墙、喷泉和女人在阴影里；
 只有自然光。
```


### s2_st6

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st6/planning/st6_first_frame.png`）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I39** [主要·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；s3st5_flour.png：下磨石一圈是一道道竖直往下淌、带反光的
  - 方案：s3_st5 首帧局部修成干面粉，文字写干燥细白面粉簌簌撒落，负面词加「往下流的液体、水帘、湿亮的条痕、面糊」；s2 光线行按绝对方位逐镜写，s2_st1/st3 首帧压暗东侧；s3_st7 布包写左前臂支撑；垫脚石统一「高出路面约四十厘米」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/st5_first_frame_prompt.txt`
- 分镜「光线」改了：

```diff
@@ -1,4 +1,6 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜镜头朝北偏东：画右虚化的东侧墙在阴影里，画左远处西侧墙的上半截受光；
 只有自然光。
```


### s2_st7

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st7/planning/st7_first_frame.png`）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I22** [严重·implemented·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；首帧左上高窗是木框加竖条、横条的分格窗（z_s8st2
  - 方案：s8_st2 首帧局部修成光秃的方窗洞，ffp 负面词加「窗格、窗框分格、带玻璃的窗」；s3_st8 首帧去掉墙上竖管，负面词加「墙上的竖管、落水管」；s2_st5/st7 文字删掉石块形状描写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/st2_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I57** [待核实·planned·待复核] 人物逻辑·C3 / C7 · 从看腿接到看脸：C3 / C7 · 从看腿接到看脸：st5 收尾与 st6 主观插入都落在腿/靴；st7 spec 要第 0 秒头微低、目光在镜头左边偏低处，到 2.5 秒后才
  - 方案：出片后核 s2_st7 0–2.5 s 有没有先看低处再抬眼；不行再局部修首帧（下巴略收、眼球下视）
- 分镜「动作」改了：

```diff
@@ -1,3 +1,3 @@
-他拍，和 st5 同一个机位（朝南顺街看：东墙和牛头出水口在画左，石槽在画面左半，街面在画右）、同一个接水的女人 Vibia。
-她直着腰站在石槽靠街这一角的外面，在画面中间偏右，身子转过来朝着镜头左边，两手扶着搁在身前槽沿上的满水罐；
+他拍，镜头站在喷泉北边约两米的人行道上，朝南顺街看：东墙和牛头出水口在画左，石槽在画面左半，石块路面在画右。
+接水的女人 Vibia 直着腰站在石槽靠街这一角的外面，在画面中间偏右，身子转过来朝着镜头左边，两手扶着搁在身前槽沿上的满水罐；
 她的头只微微低着，视线落在画外 Riley 的腿上（镜头左边、比镜头低一点的地方）。
@@ -6,3 +6,3 @@
 道具：满水罐一直搁在她身前的槽沿上，她两手扶着。
-配角——Vibia：此刻看着画外的 Riley（视线在镜头左边一点），心想「这成何体统」——是看不惯，眉心舒展、眼睛睁圆。
+配角——Vibia：此刻看着画外的 Riley（视线在镜头左边一点），脸上写着看不惯：眉心舒展、眼睛睁圆。
 画面里只有她一个人。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
-同 st5：镜头在喷泉北边约两米的人行道上，朝南顺街看；
+镜头在喷泉北边约两米的人行道上，朝南顺街看；
 她在画面中间偏右，石槽和牛头出水口在画面左半；
-Riley 在镜头左后方的画外，她的视线在镜头左边一点，眼睛看着自己的事。
+Riley 在镜头左后方的画外，她的视线在镜头左边一点。
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
-他拍，固定机位（与 st5 同机位）。
+他拍，固定机位，镜头在喷泉北边约两米的人行道上。
 中近景，腰以上：女人在画面中间偏右，牛头出水口和石槽在画面左半，槽沿和水罐在画面下部；
```

- 分镜「光线」改了：

```diff
@@ -1,4 +1,6 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜镜头朝南：画右西侧那排墙上半截受光，画左东侧的墙、喷泉和女人在阴影里；
 只有自然光。
```


### s2_st8

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/st8_first_frame.png`）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I24** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；overhead Vibia 离镜头 3.5 m（在 Ri
  - 方案：s2_st8 文字与 overhead 改成 Vibia 在 Riley 身后约一米（贴首帧）；s2_st4 起点与擦肩提前到 0–1.5 s；s2_st1 机位改为垫脚石南约 2.5 m、离地 0.5 m；s8_st8 两位妇女站位对调贴首帧；s3_st6 机位推到 (5.8,6.0)、标中近景
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st6/planning/overhead.toml`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I40** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml Riley path `[
  - 方案：s3_st7 8.5 s 面朝点改回 Felix；s2_st2 删掉 7.3 s 的转身；s2_st8 改上身左拧、从左肩回头用眼角看；s2_st5 节拍拆成接水 / 提罐稳放 / 听见外国话直腰转头 / 目光下扫
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- **I41** [主要·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；overhead 女孩 (14.3,26.4)@4.5 → (14.0,22
  - 方案：s2_st4 女孩错身后拐进石槽南边一间敞门铺子（7 s 进门），Riley 0–1.5 s 从 Vibia 和路缘之间走过；s3_st1 Felix 东挪半步取面包；s2_st8 Vibia 距离按首帧改约一米
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`
- 分镜「动作」改了：

```diff
@@ -3,10 +3,10 @@
 牛头出水口和石槽在她正后方，大半被她的头和肩挡住，石槽靠街的一角从她左肩外露出来；
-接水的女人 Vibia 在画右、Riley 左肩后面约三米，站在石槽靠街这一角的外面，直着腰，上半身露在 Riley 肩膀上方；
+接水的女人 Vibia 在画右、Riley 左肩后面约一米，站在石槽靠街这一角的外面，直着腰，上半身露在 Riley 肩膀上方；
 再往画右是不规则多边形大石板铺的街面。
-Riley 觉出被人盯着，从左肩回头，看见女人挑着眉看她，笑着用左手冲她挥了挥；
-女人把头扭开，低头看着自己的水罐，用手掌抹罐身外面的水。
+Riley 觉出被人盯着，上身往左一拧、从左肩回头，用眼角看见女人挑着眉看她，笑着用左手冲她挥了挥；
+女人把头扭开，从腰带里抽出一小块布，低头擦罐身外面的水。
 Riley 转回镜头，抿着嘴忍着笑，说那句话；
 说完又憋着笑往左肩后瞟了一眼。
-道具：女人的满水罐一直搁在她身前的槽沿上，她两手扶着、后来用手掌抹罐身，罐子一直在槽沿上。
-配角——Vibia：第 0–2.5 秒两道眉毛高高挑起、额头起横纹、嘴角往下撇，带着看不惯的神情看 Riley，心想「穿成这样还冲我挥手」；
+道具：女人的满水罐一直搁在她身前的槽沿上，她两手扶着、后来拿一小块布擦罐身，罐子一直在槽沿上。
+配角——Vibia：第 0–2.5 秒两道眉毛高高挑起、额头起横纹、嘴角往下撇，带着看不惯的神情看 Riley，被她一挥手更看不惯；
 第 2.5–3.5 秒把头扭开，之后只看自己的水罐。
```

- 分镜「走位」改了：

```diff
@@ -2,3 +2,3 @@
 Riley 面对镜头，背朝喷泉；
-东墙和水塔在画面左缘（她右肩后），出水口和石槽在她正后方，女人在画右、Riley 左肩后面约三米，上半身露在 Riley 肩膀上方，街面在画右远处。
-Riley 回头时从左肩往后看。
+东墙和水塔在画面左缘（她右肩后），出水口和石槽在她正后方，女人在画右、Riley 左肩后面约一米，上半身露在 Riley 肩膀上方，街面在画右远处。
+Riley 回头时上身往左拧、从左肩往后看。
```

- 分镜「节拍」改了：

```diff
@@ -1,6 +1,6 @@
-0–1秒 Riley 对着镜头，觉出被人盯着，从左肩回头，看见画右挑着眉的女人，嘴还闭着；
+0–1秒 Riley 对着镜头，觉出被人盯着，上身往左一拧、从左肩回头，看见画右挑着眉的女人，嘴还闭着；
 1–2.5秒 她笑着用左手冲女人挥了挥；
-2.5–3.5秒 女人把头扭开，低头看着自己的水罐，用手掌抹罐身（单独一拍）；
-3.5–4.5秒 Riley 转回镜头，抿着嘴忍着笑，嘴还闭着；
-4.5–8.5秒 她忍着笑说那句话（And yeah… 之后停半拍）；
-8.5–11秒 说完她憋着笑往左肩后瞟了一眼，咬着嘴唇笑，嘴闭着
+2.5–3.5秒 女人把头扭开，从腰带里抽出一小块布，低头擦罐身（单独一拍）；
+3.5–4.3秒 Riley 转回镜头，抿着嘴忍着笑，嘴还闭着；
+4.3–8.8秒 她忍着笑说 Yeah… I don't think she's a fan of the pants.（4.4–8.7 秒，Yeah… 之后停半拍）；
+8.8–11秒 说完她憋着笑往左肩后瞟了一眼，咬着嘴唇笑，嘴闭着
```

- 分镜「光线」改了：

```diff
@@ -1,4 +1,6 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜镜头朝南：画右远处西侧那排墙上半截受光，画左东侧的墙和水塔、她们两人在阴影里；
 只有自然光。
```

- 分镜「台词」改了：

```diff
@@ -1 +1,2 @@
-Riley（忍着笑，美式英语）：And yeah… apparently a woman in pants is a lot.
+Riley（忍着笑，美式英语；
+Yeah… 之后停半拍）：Yeah… I don't think she's a fan of the pants.
```


### s2_st4

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/st4_first_frame.png`）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I24** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；overhead Vibia 离镜头 3.5 m（在 Ri
  - 方案：s2_st8 文字与 overhead 改成 Vibia 在 Riley 身后约一米（贴首帧）；s2_st4 起点与擦肩提前到 0–1.5 s；s2_st1 机位改为垫脚石南约 2.5 m、离地 0.5 m；s8_st8 两位妇女站位对调贴首帧；s3_st6 机位推到 (5.8,6.0)、标中近景
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st6/planning/overhead.toml`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I27** [严重·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数 最终 1 分：动作节拍的秒数排得下（走多远、几秒到），没有挤压；overhead Riley (13.6,20.6) 离镜头 3.4 m、Vib
  - 方案：s2_st4 擦肩提前到 0–1.5 s、老人挪到西人行道；s8_st3 起点前移 0.6 m；s8_st7 老汉路线重排、约 6.5 s 出画右；s3_st1 第 0 秒改为已站定；v7 各镜节拍按新镜长重排，overhead 闸门 63 镜 0 blocker 0 warning
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`
- **I41** [主要·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；overhead 女孩 (14.3,26.4)@4.5 → (14.0,22
  - 方案：s2_st4 女孩错身后拐进石槽南边一间敞门铺子（7 s 进门），Riley 0–1.5 s 从 Vibia 和路缘之间走过；s3_st1 Felix 东挪半步取面包；s2_st8 Vibia 距离按首帧改约一米
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`
- **I55** [待核实·implemented·待复核] 人物逻辑·C7 / C5：C7 / C5：Riley 从刚瞪过她的 Vibia 身边一臂宽处走过，spec 写 Vibia「只顾自己的罐子」，没说是刻意不理；模型可能画成毫无关系的路人，
  - 方案：s2_st4 Vibia 改「眼睛不抬，嘴角还撇着，故意只顾自己的罐子」，文字和 ffp 同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/st4_first_frame_prompt.txt`
- **I66** [记录·implemented·待复核] 世界物理·P2 道具来源：P2 道具来源：首帧 Vibia 右手拿一块抹布擦罐（s2st4_vibia_riley.png x≈75–110,y≈235–265），别的镜都没有这块布，文
  - 方案：不修图，改文字：s2_st8 2.5–3.5 s 从腰带里抽出一小块布擦罐，s2_st4 写右手里的一小块布
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/st4_first_frame_prompt.txt`
- **I87** [记录·implemented·待复核] 人物逻辑·C6：C6：「胳膊肘碰同伴」出现在 s4_st1 6.8 秒和 s8_st3 4–5.5 秒；「看长发」出现在 s2_st4、s8_st2、s8_st7 三处；当地人
  - 方案：s4_st1 去掉胳膊肘碰同伴（改成互看一眼、咧嘴笑）；s8_st3 改成对视、用下巴一指；s8_st7 老汉改看短靴和布包
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -4,8 +4,8 @@
 Riley 沿着这一侧人行道靠街心的外沿、贴着路缘往前走远：她从站在石槽靠街一角的 Vibia 和路缘之间走过，两人隔着一臂宽，路线和石槽错开约一米；
-Vibia 直着腰，侧背对镜头，低头用手掌抹槽沿上水罐的罐身，只顾自己的罐子。
+Vibia 直着腰，侧背对镜头，低头用右手里的一小块布擦槽沿上水罐的罐身，眼睛不抬，嘴角还撇着，故意只顾自己的罐子。
 Riley 一直往街的深处走，高挑的背影慢慢融进街上的人群。
 街上四个路人（普通路人，各忙各的）：一个顶着圆藤筐的小女孩（十一二岁，深棕色齐肩短发，穿褪色的靛蓝色短袖 tunica、腰上系一根细带，赤脚；
-藤筐稳稳顶在头上，两手空着自然摆）沿同一侧人行道迎面走来，往墙边让一步，和 Riley 错身时抬眼好奇地看她披散的长发，伸手摸了摸自己齐肩的短发，接着往前走；
+藤筐稳稳顶在头上，两手空着自然摆）沿同一侧人行道迎面走来，往墙边让一步，和 Riley 错身时抬眼好奇地看她披散的长发，伸手摸了摸自己齐肩的短发，然后拐进石槽南边一间敞着门的铺子；
 一个肩上扛着双耳陶罐的搬运工在路面上低头走自己的路；
-一个老人牵着一个小孩在对面人行道上慢慢走。
+一个老人牵着一个小孩在对面（西侧）人行道上慢慢走。
 街的尽头被房屋和一道弯挡住。
@@ -14,4 +14,5 @@
 Riley 两手空着，钱在她裤袋里。
-第 0 秒：Riley 在画面中间偏右、人行道外沿贴着路缘、离镜头约三米半，全身背影，背对镜头刚迈步往街深处走；
-她左前方约三米、画面左半是牛头石槽喷泉，Vibia 直着腰站在石槽靠街的一角（画面中间偏左），侧背对镜头；
+第 0 秒：Riley 在画面中间偏右、人行道外沿贴着路缘，全身背影，背对镜头刚迈步往街深处走；
+Vibia 在她左前方约一米、画面中间偏左，直着腰站在石槽靠街的一角，侧背对镜头，右手拿着一小块布擦罐身；
+牛头石槽喷泉在画面左半；
 Riley 的路线在 Vibia 右边、Vibia 和路缘之间留着一人宽的空地；
```

- 分镜「走位」改了：

```diff
@@ -1,4 +1,4 @@
 镜头固定在喷泉这一侧人行道上、垫脚石东北边，朝南顺着街看，东墙和喷泉在画面左半；
-Riley 从第 0 秒起就贴着路缘走（人行道靠街心的那一边），从 Vibia 和路缘之间直直走过去，一直走在这一侧人行道上；
-顶筐的女孩沿同一侧人行道迎面走来，在石槽南边和 Riley 错身，女孩靠墙、Riley 靠路缘；
-搬运工在路面上，老人和小孩在对面人行道上。
+Riley 第 0 秒在 Vibia 身后约一米，从第 0 秒起就贴着路缘走（人行道靠街心的那一边），0–1.5 秒从 Vibia 和路缘之间直直走过去，一直走在这一侧人行道上；
+顶筐的女孩沿同一侧人行道迎面走来，在石槽南边和 Riley 错身，女孩靠墙、Riley 靠路缘，随后女孩拐进石槽南边一间铺子；
+搬运工在路面上，老人和小孩在对面（西侧）人行道上。
```

- 分镜「节拍」改了：

```diff
@@ -1,5 +1,6 @@
-0–1.5秒 Riley 背对镜头、贴着路缘迈步往前走；
-1.5–4秒 Riley 从 Vibia 和路缘之间走过，Vibia 低头抹罐身，Riley 接着沿同一侧人行道往前走；
+0–1.5秒 Riley 背对镜头、贴着路缘迈步，从 Vibia 和路缘之间走过，Vibia 低头擦罐身，眼睛不抬；
+1.5–4秒 Riley 接着沿同一侧人行道往前走；
 4–5.5秒 顶筐的女孩迎面走来，往墙边让一步，和 Riley 错身时抬眼盯着她披散的长发看，摸了摸自己齐肩的短发（单独一拍）；
-5.5–8.5秒 Riley 越走越远，从扛陶罐的搬运工身边走过，修长的身影在人群里很显眼；
+5.5–8.5秒 女孩拐进石槽南边一间铺子；
+Riley 越走越远，从扛陶罐的搬运工身边走过，修长的身影在人群里很显眼；
 8.5–10秒 她走进远处的人群里，镜头停在原地，街上热闹起来，只有环境声
```

- 分镜「光线」改了：

```diff
@@ -1,4 +1,6 @@
 清晨。
-太阳在东边，低低地藏在喷泉这一侧（东侧）那排房子的屋顶后面、始终在画外：街对面西侧那排墙的上半截被晨光照成暖金色，喷泉这一侧的墙、人行道和大半个街面在柔和的阴影里，路面的流水反光；
+太阳在东边，低低地藏在东侧（喷泉这一侧）那排房子的屋顶后面、始终在画外：西侧那排墙朝东的那一面，上半截被晨光照成暖金色；
+东侧那排墙、东边人行道和大半个街面在柔和的阴影里，路面的流水反光；
 天空晴朗干净；
+本镜镜头朝南：画右西侧那排铺子的墙上半截受光，画左东侧的墙和喷泉在阴影里；
 只有自然光。
```


### s2 整场 / 未指明镜头

- **I106** [记录·implemented·待复核] 母语听感·N4 口癖/节奏：N4 口癖/节奏：省略号拖音 8 镜以上；basically 仍有 s8_st1、s5_st5（I97 未改）
  - 方案：v7 全部台词按新听感标准重写，s8_st1 去掉 basically

### s2 整场 / 未指明镜头

- **I112** [记录·planned·待复核] 时代与世界观·E6·出处：E6·出处：卡里把 Petronius Sat. 41 说成「浴场闲聊」；该句出自 Trimalchio 宴会场景
  - 方案：c7 卡与 r05 #21 的出处改成 Petronius Sat. 41（宴席闲谈），台词不动；未做

## s3

### s3_st5

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/_r2_old/st5_first_frame.png`（_r2_old）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/st5_first_frame.png`（现行）
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I28** [严重·implemented·待复核] 镜头规格·F7 一镜到底：F7 一镜到底 最终 1 分：单镜内不需要切镜；镜头运动写清且做得到；overhead 机位 (6,9)，0/3 s 看 (4.6,1.8)，6 s 看 (12
  - 方案：s3_st5 分镜、prompt、overhead note 改成摇约五十度
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/overhead.toml`
- **I39** [主要·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；s3st5_flour.png：下磨石一圈是一道道竖直往下淌、带反光的
  - 方案：s3_st5 首帧局部修成干面粉，文字写干燥细白面粉簌簌撒落，负面词加「往下流的液体、水帘、湿亮的条痕、面糊」；s2 光线行按绝对方位逐镜写，s2_st1/st3 首帧压暗东侧；s3_st7 布包写左前臂支撑；垫脚石统一「高出路面约四十厘米」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/st5_first_frame_prompt.txt`
- 分镜「动作」改了：

```diff
@@ -1,3 +1,4 @@
-面包房里（镜头在门脸外的街上往里看）：一头蒙着眼的灰驴套着一根木横杆，沿着西边那座石磨四周的圆形走道从侧面走过，横杆带着黑灰色沙漏形石磨的上半截绕中轴慢慢转，石磨低低地隆隆响，面粉从磨石下沿撒落到磨盘四周的石槽里；
+面包房里（镜头在门脸外的街上往里看）：一头蒙着眼的灰驴套着一根木横杆，沿着西边那座石磨四周的圆形走道从侧面走过，横杆带着黑灰色沙漏形石磨的上半截绕中轴慢慢转，石磨低低地隆隆响，干燥的细白面粉从磨石下沿簌簌撒落，在磨盘底座周围的平台上铺成薄薄一层；
 东边还有一座同样的石磨，静静立着。
+镜头前景是门脸石台的一角，台面上摊着一层刚出炉的圆面包。
 镜头从石磨横摇到店里东头的砖砌半圆顶炉子：炉口透出火光，门楣下贴着一缕淡淡的炉烟。
@@ -7,4 +8,4 @@
 木铲的长柄单独一根，和石磨横杆错开。
-配角：Felix 只看着手里的铲子和面包，心思在活儿上，还没注意到门外的 Riley。
-第 0 秒：画面里是蒙眼的驴和西边那座石磨，驴侧身走在磨道上，画右边缘是东边那座静着的石磨；
+配角：Felix 只看着手里的铲子和面包，心思全在活儿上。
+第 0 秒：画面里是蒙眼的驴和西边那座石磨，驴侧身走在磨道上，磨盘底座周围铺着一层干面粉，画右边缘是东边那座静着的石磨，左下前景是石台一角和台面上摊着的一层面包；
 炉子和 Felix 在画右画外。
```

- 分镜「走位」改了：

```diff
@@ -2,2 +2,2 @@
 驴和西边的石磨在店里西头（画左），东边的石磨在店中间，炉口在店里东头深处（摇过去之后在画面中间）；
-Felix 侧对镜头站在炉口前，从头到尾不离开炉口。
+Felix 侧对镜头站在炉口前，从头到尾站在炉口前。
```

- 分镜「节拍」改了：

```diff
@@ -1,2 +1,2 @@
-0–3秒 镜头停在驴和石磨上：蒙眼的驴侧身走在磨道上，横杆推着石磨转，面粉从磨石下沿撒落，只有磨声；
+0–3秒 镜头停在驴和石磨上：蒙眼的驴侧身走在磨道上，横杆推着石磨转，干面粉从磨石下沿簌簌撒落，只有磨声；
 3–6秒 镜头缓缓横摇到炉口，两座石磨先后出画：Felix 在炉口前双手握着长柄木铲，从炉口抽出一个冒热气的深棕色圆面包，眼睛看着面包；
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
-他拍，建立镜头：全景，0–3 秒停在画左的石磨与驴，3–6 秒缓缓横摇到店里东头深处的炉口与 Felix，摇过去约一百一十度，摇完时两座石磨都在画左画外，6–8 秒停在炉口；
+他拍，建立镜头：全景，0–3 秒停在画左的石磨与驴，3–6 秒缓缓横摇到店里东头深处的炉口与 Felix，摇过去约五十度，摇完时两座石磨都在画左画外，6–8 秒停在炉口；
 眼平；
```


### s3_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st1/planning/st1_first_frame.png`）
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I20** [严重·implemented·待复核] 台词（时长与逻辑）·D6 听得清：D6 听得清 最终 1 分：环境声不盖过台词；悄悄话、远处的话能听清；prompt.txt 第 2 行与末行声音模板无「对白压过环境声」；s8_st1 合唱、s
  - 方案：编译器 v14：有台词的镜头声音行加「对白优先：有人说话时环境声和动作声压低到对白下面，每句台词清楚可辨」（ep01 共 82 处）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I27** [严重·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数 最终 1 分：动作节拍的秒数排得下（走多远、几秒到），没有挤压；overhead Riley (13.6,20.6) 离镜头 3.4 m、Vib
  - 方案：s2_st4 擦肩提前到 0–1.5 s、老人挪到西人行道；s8_st3 起点前移 0.6 m；s8_st7 老汉路线重排、约 6.5 s 出画右；s3_st1 第 0 秒改为已站定；v7 各镜节拍按新镜长重排，overhead 闸门 63 镜 0 blocker 0 warning
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I38** [主要·implemented·待复核] 世界物理·P3 交接三段：P3 交接三段 最终 1 分：交接写清从哪拿、交到哪、对方怎么握住或收起；钱、灯、刮板都要；prompt 还写「探身伸手把两枚钱拨到手边、拢进小陶碗」；st7、
  - 方案：s3_st1 改「拨到手边，用拇指和食指拈起来，越过碗沿放进小陶碗」、Felix 东挪半步取最近的面包、左手掀开左侧袋盖；s3_st7 改左前臂把布包按在左胯、两手打结后才松开
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st1/planning/overhead.toml`
- **I41** [主要·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；overhead 女孩 (14.3,26.4)@4.5 → (14.0,22
  - 方案：s2_st4 女孩错身后拐进石槽南边一间敞门铺子（7 s 进门），Riley 0–1.5 s 从 Vibia 和路缘之间走过；s3_st1 Felix 东挪半步取面包；s2_st8 Vibia 距离按首帧改约一米
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`
- **I42** [主要·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；首帧 Riley 已经整个人在画里站定，没有「刚进画、还差一步」；左
  - 方案：s3_st1 第 0 秒改为已站在石台外、刚停下，toml 删进场路点；写左手掀开左侧大口袋袋盖；s3_st5 面包摆法按首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st1/planning/overhead.toml`
- 分镜「动作」改了：

```diff
@@ -2,11 +2,11 @@
 石台上，Felix 左手边（东边）摞着一摞深棕色的八瓣圆面包（每个直径约二十厘米），石台中段靠里放着一只装钱的小陶碗，也在 Felix 左手边、他伸手就够得着；
-后景里能看到东边那座静着的石磨和最里面炉口的火光，驴拉的那座石磨在画左画外，只听得见隆隆的磨声。
-Riley 从画右的街上走进画面，来到石台外侧、正对着 Felix 站定，看着面包；
+后景里能看到东边那座静着的石磨和最里面炉口的火光，驴拉的那座石磨在画左画外，只听得见低低的、从画外传来的隆隆磨声，有人说话时磨声更轻。
+Riley 站在石台外侧的街面上、正对着 Felix，刚停下脚步，看着面包；
 面包师 Felix 站在石台里侧，看见她，咧嘴一笑，洪亮地招呼她。
 Riley 学着回了一句，按英文单词念成 Sal-VAY，Felix 笑出声。
-她竖起一根手指、指一下那摞面包，放下手，左手伸进裤子左侧的大口袋，捏出两枚红铜小钱放在自己面前的石台外沿上；
-Felix 探身伸手把两枚钱拨到手边、拢进小陶碗，再侧过身从那一摞里拿起一个面包，放到她面前的石台上。
+她竖起一根手指、指一下那摞面包，放下手，左手掀开裤子左侧大口袋的袋盖，伸进去捏出两枚红铜小钱，放在自己面前的石台外沿上；
+Felix 探身把两枚钱拨到手边，用拇指和食指拈起来，越过碗沿放进小陶碗，再往东挪半步、探身从那一摞上拿起最近的一个面包，回身放到她面前的石台上。
 道具（钱，p2）：付前——全部钱收在她裤子左侧的大口袋里（7 枚红铜小钱＋1 枚更小的浅色小铜币＋1 枚大黄铜币）；
 付出——她从裤兜里只捏出两枚红铜小钱，手心里正好 2 枚，放在她面前的石台外沿上；
-付后——Felix 把这 2 枚拢进小陶碗，碗留在石台上 Felix 左手边；
+付后——Felix 把这 2 枚放进小陶碗，碗留在石台上 Felix 左手边；
 她的裤兜里剩 5 枚小钱＋小铜币＋大黄铜币。
```

- 分镜「走位」改了：

```diff
@@ -2,3 +2,3 @@
 Felix 在石台里侧、面朝街；
-Riley 从画右的街上走进来，停在石台外侧、正对着 Felix，两人隔着约 0.8 米深的石台对视，相距不到一米半，伸手就能隔着石台递东西。
+Riley 站在石台外侧、正对着 Felix，两人隔着约 0.8 米深的石台对视，相距不到一米半，伸手就能隔着石台递东西。
 镜头在街上、石台西头外侧约半米，两人的西边偏南，侧对两人：Felix 在画面左半、石台后，Riley 在画面右半、石台前，两人都是侧身；
```

- 分镜「节拍」改了：

```diff
@@ -1,4 +1,3 @@
-0–1.5秒 第 0 秒：Felix 在画面左半的石台里侧低头整理那一摞面包；
-Riley 刚从画右边缘走进画面，离石台还有一步；
-她走到石台外侧、正对着 Felix 站定，双手空着垂在身侧，看着面包，两人都安静；
+0–1.5秒 第 0 秒：Felix 在画面左半的石台里侧，低头把刚出炉的面包摞成一摞；
+Riley 已经站在画面右半的石台外侧、正对着 Felix，刚停下脚步，双手空着垂在身侧，看着面包，两人都安静；
 1.5–2.5秒 Felix 抬头看见她，咧嘴笑，洪亮地说 Salve（1.6–2.2 秒）；
@@ -8,5 +7,5 @@
 5.5–6.5秒 Riley 竖起一根手指，指一下那摞面包，1 秒后放下手；
-6.5–8.5秒 她左手伸进裤子左侧的大口袋，捏出两枚红铜小钱，放在面前的石台外沿上，手收回；
-8.5–10秒 Felix 低头看钱，探身伸手把两枚钱拨到手边、拢进小陶碗（单独一拍）；
-10–11.5秒 Felix 侧过身从那一摞里拿起一个面包，放到她面前的石台上；
+6.5–8.5秒 她左手掀开裤子左侧大口袋的袋盖，伸进去捏出两枚红铜小钱，放在面前的石台外沿上，手收回；
+8.5–10秒 Felix 低头看钱，探身把两枚钱拨到手边，用拇指和食指拈起来，越过碗沿放进小陶碗（单独一拍）；
+10–11.5秒 Felix 往东挪半步、探身从那一摞上拿起最近的一个面包，回身放到她面前的石台上；
 11.5–13秒 两人对视笑，Felix 点点头，两人都安静
```


### s3_st2

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st2/planning/st2_first_frame.png`）
- **I42** [主要·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；首帧 Riley 已经整个人在画里站定，没有「刚进画、还差一步」；左
  - 方案：s3_st1 第 0 秒改为已站在石台外、刚停下，toml 删进场路点；写左手掀开左侧大口袋袋盖；s3_st5 面包摆法按首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st1/planning/overhead.toml`
- **I46** [主要·implemented·待复核] 母语听感·N2 别扭原因：N2 别扭原因 最终 1 分：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词；L36 "His son called it gross — so Dad
  - 方案：v7 重写全部 Riley 台词：s4_st2 改「…held a coin up to his son's nose and went, "Does this smell?"」；s7_st2「…I swear this was in my history textbook…」；s3_st4、s8_st1、s3_st2 一并重写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-9
+14
```

- 分镜「动作」改了：

```diff
@@ -2,5 +2,6 @@
 她身后整幅背景是门脸外的街和街对面一排素面抹灰的铺面墙。
-她右手手掌平按在面包上把它压稳，左手手指扣住其中一瓣的外缘，顺着刀口往上一掰——干脆的一下，这一瓣整块断开，掰开处冒出热气，面包心是浅褐色、粗糙多孔的全麦质地；
+她先看见面包上划好的刀口，惊喜地说出来；
+右手手掌平按在面包上把它压稳，左手手指扣住其中一瓣的外缘，说到 snaps right off 时顺着刀口往上一掰——干脆的一下，这一瓣整块断开，掰开处冒出热气，面包心是浅褐色、粗糙多孔的全麦质地；
 其余七瓣还连在一起，平放在石台上，被她右手按着。
-她左手把这一瓣举到胸前、下巴以下，脸始终露在外面，笑着对镜头说话。
+她左手把这一瓣举到胸前、下巴以下，脸始终露在外面，笑着对镜头说完后两句。
 道具：进场——整个面包在石台上，她右手按在面包上、左手扣着一瓣的边；
```

- 分镜「节拍」改了：

```diff
@@ -1,5 +1,8 @@
-0–1秒 第 0 秒：Riley 站在石台外侧、面朝镜头，右手掌平按在面前石台上的整个圆面包上，左手手指扣着其中一瓣的外缘，低头看面包，嘴闭着；
-1–2.5秒 她左手顺着刀口往上一掰，干脆的一下，这一瓣整块断开，冒出热气，剩下七瓣平放在石台上不动；
-2.5–3.5秒 她左手把这一瓣举到胸前、下巴以下，抬眼看镜头，得意地笑，嘴闭着；
-3.5–7.5秒 她看着镜头说那句话（3.6–7.4 秒）；
-7.5–9秒 她得意地挑挑眉，低头看那一瓣冒热气，面包离嘴还有一拳远，嘴闭着
+0–1.5秒 第 0 秒：Riley 站在石台外侧、面朝镜头，右手掌平按在面前石台上的整个圆面包上，左手手指扣着其中一瓣的外缘，低头看面包上划好的刀口，嘴闭着；
+1.5–3.2秒 她低头看着面包，惊喜地说 Oh, it's pre-cut!
+，左手手指顺着一道刀口划一下；
+3.2–6.2秒 说 Look at that — it just snaps right off.，说到 snaps right off 时左手顺着刀口往上一掰，干脆的一下，这一瓣整块断开，冒出热气，剩下七瓣平放在石台上不动；
+6.2–7.2秒 她左手把这一瓣举到胸前、下巴以下，抬眼看镜头，得意地笑，嘴闭着；
+7.2–11秒 她看着镜头说 So the Romans basically had sliced bread first.；
+11–12.2秒 说 Love that.，点一下头；
+12.2–14秒 她得意地挑挑眉，低头看那一瓣冒热气，面包离嘴还有一拳远，嘴闭着
```

- 分镜「台词」改了：

```diff
@@ -1 +1,2 @@
-Riley（得意地，美式英语）：Pre-sliced bread. Before sliced bread was even a thing.
+Riley（发现新东西，又惊喜又得意，美式英语）：Oh, it's pre-cut!
+Look at that — it just snaps right off. So the Romans basically had sliced bread first. Love that.
```


### s3_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st3/planning/st3_first_frame.png`）
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I42** [主要·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；首帧 Riley 已经整个人在画里站定，没有「刚进画、还差一步」；左
  - 方案：s3_st1 第 0 秒改为已站在石台外、刚停下，toml 删进场路点；写左手掀开左侧大口袋袋盖；s3_st5 面包摆法按首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st1/planning/overhead.toml`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-7
+10
```

- 分镜「动作」改了：

```diff
@@ -5,3 +5,3 @@
 店里深处偏暗，砖炉在画右画外，炉火的橙红光从画右映进来。
-她左手捏着刚掰下的那一瓣（扇形、深棕硬皮、浅褐粗孔的芯，缺了一小口），嘴里已经有面包，闭着嘴嚼，眉毛先微挑（意外地扎实），再满意地点头，慢慢说出它的味道。
+她左手捏着刚掰下的那一瓣（扇形、深棕硬皮、浅褐粗孔的芯，缺了一小口），嘴里已经有面包，闭着嘴嚼，眉毛先微挑（意外地扎实），边嚼边点头，按正常语速说出它的味道。
 道具：进场和出场都是左手捏着那一瓣；
```

- 分镜「节拍」改了：

```diff
@@ -1,3 +1,4 @@
 0–1.5秒 第 0 秒：她面朝镜头站在石台前，左手把那一瓣捏在胸前，嘴里已经有面包，闭着嘴慢慢嚼，眉毛微挑，嘴一直闭着；
-1.5–4.5秒 边嚼边点头，慢慢说出那句评价，词与词之间停一下（1.6–4.3 秒）；
-4.5–7秒 她满意地闭眼点点头，把那一瓣朝镜头晃一下，嘴闭着
+1.5–8.5秒 边嚼边说那段评价，正常语速（1.6–8.3 秒）：Mm — mm. 时眉毛一挑，Okay, that's really dense. 时点头，Like, kind of smoky?
+时歪一下头想，It's so good, though. 时满意地笑；
+8.5–10秒 她满意地闭眼点点头，把那一瓣朝镜头晃一下，嘴闭着
```

- 分镜「台词」改了：

```diff
@@ -1 +1,3 @@
-Riley（嚼着，满意，美式英语）：Mm. Dense… kinda smoky. So good.
+Riley（嘴里有面包、边嚼边说，满意，美式英语；
+Mm — mm. 是嚼着面包的哼声）：Mm — mm. Okay, that's really dense. Like, kind of smoky?
+It's so good, though.
```


### s3_st7

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st7/planning/st7_first_frame.png`）
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I38** [主要·implemented·待复核] 世界物理·P3 交接三段：P3 交接三段 最终 1 分：交接写清从哪拿、交到哪、对方怎么握住或收起；钱、灯、刮板都要；prompt 还写「探身伸手把两枚钱拨到手边、拢进小陶碗」；st7、
  - 方案：s3_st1 改「拨到手边，用拇指和食指拈起来，越过碗沿放进小陶碗」、Felix 东挪半步取最近的面包、左手掀开左侧袋盖；s3_st7 改左前臂把布包按在左胯、两手打结后才松开
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st1/planning/overhead.toml`
- **I39** [主要·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；s3st5_flour.png：下磨石一圈是一道道竖直往下淌、带反光的
  - 方案：s3_st5 首帧局部修成干面粉，文字写干燥细白面粉簌簌撒落，负面词加「往下流的液体、水帘、湿亮的条痕、面糊」；s2 光线行按绝对方位逐镜写，s2_st1/st3 首帧压暗东侧；s3_st7 布包写左前臂支撑；垫脚石统一「高出路面约四十厘米」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st5/planning/st5_first_frame_prompt.txt`
- **I40** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml Riley path `[
  - 方案：s3_st7 8.5 s 面朝点改回 Felix；s2_st2 删掉 7.3 s 的转身；s2_st8 改上身左拧、从左肩回头用眼角看；s2_st5 节拍拆成接水 / 提罐稳放 / 听见外国话直腰转头 / 目光下扫
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st5/planning/overhead.toml`
- **I42** [主要·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；首帧 Riley 已经整个人在画里站定，没有「刚进画、还差一步」；左
  - 方案：s3_st1 第 0 秒改为已站在石台外、刚停下，toml 删进场路点；写左手掀开左侧大口袋袋盖；s3_st5 面包摆法按首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st1/planning/overhead.toml`
- **I67** [记录·wontfix·待复核] 世界物理·P2 动物持续存在：P2 动物持续存在：三张首帧呈现两座磨，当前画面未见拉西磨的驴；st3 刚建立了同店西磨与驴。changes.md 明确 st4/st7 保留现图为记录级。当前
  - 方案：维持上一轮决定，记录；出片时如果西磨在转而磨道空着，再补遮挡
- 分镜「动作」改了：

```diff
@@ -6,3 +6,3 @@
 他探身越过石台，捏着结把布包递过去，Riley 也往前探身，右手接住布结，左手托一下布包底；
-她低头把两个长布角绕过腰带左侧，打一个结、拉紧，扁圆的布包（和一个面包差不多大）垂在她左胯边，她拍拍布包。
+她低头，用左前臂把布包按在左胯上，两手把两个长布角绕过腰带左侧，打一个结、拉紧，系牢后才松开前臂，扁圆的布包（和一个面包差不多大）垂在她左胯边，她拍拍布包。
 最后 Felix 转身去端身后工作台上的木托板（托板上是另一批刚出炉的五个面包）。
```

- 分镜「节拍」改了：

```diff
@@ -7,3 +7,3 @@
 7–8.5秒 他探身越过石台，捏着布结把布包递过去，Riley 往前探身，伸右手接住布结，左手托一下布包底；
-8.5–11秒 Riley 低头，把两个长布角绕过腰带左侧、打一个结、拉紧，布包垂在她左胯边，Felix 的手已经收回；
+8.5–11秒 Riley 低头，用左前臂把布包按在左胯上，两手把两个长布角绕过腰带左侧、打一个结、拉紧，系牢后才松开前臂，布包垂在她左胯边，Felix 的手已经收回；
 11–13秒 她拍拍布包，抬头冲 Felix 笑；
```


### s3_st4

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st4/planning/st4_first_frame.png`）
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I21** [严重·implemented·待复核] 台词（时长与逻辑）·D4·路线逻辑；R I88：D4·路线逻辑；R I88：s3_st4 复述“Straight… then dextram”；s3_st8 只从柜台走两步到街上便向左走，首帧与两份俯视图也没
  - 方案：v7 s3_st4 改为「Okay… I definitely heard "dextram." No idea what that means. It's fifty-fifty, right? I'm gonna say… left.」，去掉 Straight；s4_st3「Okay, I'm going left…」；s5_st9 回收「"Dextram" means right?」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I45** [主要·implemented·待复核] 台词（时长与逻辑）·D2 节拍对位：D2 节拍对位 最终 1 分：台词和动作节拍对得上（说到哪句做哪个动作）；总述「她说话时 Felix 抬眼」与节拍「她说完后 13–14.5 s 才抬眼」相抵（
  - 方案：s3_st4 总述改「她说完后 Felix 才抬眼」；s8_st6 拉丁语拆成两句分别落点，说到 versas 时翻手
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I46** [主要·implemented·待复核] 母语听感·N2 别扭原因：N2 别扭原因 最终 1 分：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词；L36 "His son called it gross — so Dad
  - 方案：v7 重写全部 Riley 台词：s4_st2 改「…held a coin up to his son's nose and went, "Does this smell?"」；s7_st2「…I swear this was in my history textbook…」；s3_st4、s8_st1、s3_st2 一并重写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I67** [记录·wontfix·待复核] 世界物理·P2 动物持续存在：P2 动物持续存在：三张首帧呈现两座磨，当前画面未见拉西磨的驴；st3 刚建立了同店西磨与驴。changes.md 明确 st4/st7 保留现图为记录级。当前
  - 方案：维持上一轮决定，记录；出片时如果西磨在转而磨道空着，再补遮挡
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-16
+20
```

- 分镜「动作」改了：

```diff
@@ -1,3 +1,3 @@
 面包房门脸前，石台两侧，两人隔着石台正对面：Riley 站在石台外侧的街面上，身后是门脸外的街，布包挂在她左胯；
-Felix 在石台里侧，双手端着一块木托板，托板上正好五个刚出炉的深棕色圆面包（下面三个、上面两个，每个都划着八道放射形刀口），从头到尾都是这五个——这块托板是他上一镜末尾从身后工作台上端起来的，五个是另一批刚出炉的面包，和石台上那一摞分开；
+Felix 在石台里侧，双手端着一块木托板，托板上正好五个刚出炉的深棕色圆面包（下面三个、上面两个，每个都划着八道放射形刀口），从头到尾都是这五个——这块托板是他刚从身后工作台上端起来的，五个是另一批刚出炉的面包，和石台上那一摞分开；
 石台上是小陶碗和那一摞待卖的面包。
@@ -6,5 +6,5 @@
 Riley 皱着眉想了想，嘴唇无声地动了动；
-然后转身面向镜头，随口一猜：说到 No clue 时耸一下肩，说到 Sounds like left?
-时歪头、挑眉。
-她说话时 Felix 抬眼瞄她一下，看她对着空气说外国话，鼓起腮帮憋住笑，又低头看面包。
+然后转身面向镜头，随口一猜：说到 No idea what that means 时耸一下肩，说到 Left or right?
+Fifty-fifty. 时歪头、挑眉，停一下才说 left。
+她说完后 Felix 才抬眼瞄她一下，看她对着空气说外国话，鼓起腮帮憋住笑，又低头看面包。
 她始终站在门脸外的街面上。
```

- 分镜「走位」改了：

```diff
@@ -4,2 +4,2 @@
 石台一直横在两人中间。
-镜头在街上、石台西头外侧约半米，两人的西边偏南，侧对两人，与 st1 同一机位。
+镜头在街上、石台西头外侧约半米，两人的西边偏南，侧对两人。
```

- 分镜「节拍」改了：

```diff
@@ -7,7 +7,7 @@
 7–8秒 她转身面向镜头，嘴闭着；
-8–13秒 她对着镜头随口一猜，说那句话（8.2–12.8 秒）：No clue 时耸一下肩，Sounds like left?
-时歪头、挑眉；
-13–14.5秒 Felix 抬眼瞄她一下，鼓起腮帮憋住笑，又低头看面包（单独一拍；
+8–17秒 她对着镜头随口一猜，正常语速边想边说那段话（8.2–16.8 秒）：Okay… I definitely heard "dextram." 时皱着眉，No idea what that means. 时耸一下肩，Left or right?
+Fifty-fifty. 时歪头、挑眉，I'm gonna say… 停一下，再说 left.；
+17–18.5秒 Felix 抬眼瞄她一下，鼓起腮帮憋住笑，又低头看面包（单独一拍；
 Riley 嘴闭着）；
-14.5–16秒 Riley 对自己果断地点一下头，嘴闭着；
+18.5–20秒 Riley 对自己果断地点一下头，嘴闭着；
 两人都安静
```

- 分镜「台词」改了：

```diff
@@ -1,3 +1,6 @@
 Riley（问，美式英语，GAH-rum，重音在前，问句上扬）：Garum?
-/ Felix（拉丁语，飞快，眼睛看着面包，古典读法 hahk REK-tah plah-TEH-ah… EE-toh ahd DEK-strahm，不是意大利语腔）：Hac recta platea… ito ad dextram!
-/ Riley（皱眉随口一猜，美式英语）：Okay. Straight… then 'dextram.' No clue. Sounds like left?
+/ Felix（拉丁语，飞快，眼睛看着面包，古典读法 hahk REK-tah plah-TEH-ah… EE-toh ahd DEK-strahm）：Hac recta platea… ito ad dextram!
+/ Riley（皱眉随口一猜，美式英语；
+dextram 照她听到的念 DEK-strahm；
+Okay… 之后、say… 之后各停一下）：Okay… I definitely heard "dextram." No idea what that means. Left or right?
+Fifty-fifty. I'm gonna say… left.
```


### s3_st8

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st8/planning/_r3_before/st8_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st8/planning/st8_first_frame.png`（现行）
- **I21** [严重·implemented·待复核] 台词（时长与逻辑）·D4·路线逻辑；R I88：D4·路线逻辑；R I88：s3_st4 复述“Straight… then dextram”；s3_st8 只从柜台走两步到街上便向左走，首帧与两份俯视图也没
  - 方案：v7 s3_st4 改为「Okay… I definitely heard "dextram." No idea what that means. It's fifty-fifty, right? I'm gonna say… left.」，去掉 Straight；s4_st3「Okay, I'm going left…」；s5_st9 回收「"Dextram" means right?」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I22** [严重·implemented·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；首帧左上高窗是木框加竖条、横条的分格窗（z_s8st2
  - 方案：s8_st2 首帧局部修成光秃的方窗洞，ffp 负面词加「窗格、窗框分格、带玻璃的窗」；s3_st8 首帧去掉墙上竖管，负面词加「墙上的竖管、落水管」；s2_st5/st7 文字删掉石块形状描写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/st2_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I27** [严重·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数 最终 1 分：动作节拍的秒数排得下（走多远、几秒到），没有挤压；overhead Riley (13.6,20.6) 离镜头 3.4 m、Vib
  - 方案：s2_st4 擦肩提前到 0–1.5 s、老人挪到西人行道；s8_st3 起点前移 0.6 m；s8_st7 老汉路线重排、约 6.5 s 出画右；s3_st1 第 0 秒改为已站定；v7 各镜节拍按新镜长重排，overhead 闸门 63 镜 0 blocker 0 warning
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I67** [记录·wontfix·待复核] 世界物理·P2 动物持续存在：P2 动物持续存在：三张首帧呈现两座磨，当前画面未见拉西磨的驴；st3 刚建立了同店西磨与驴。changes.md 明确 st4/st7 保留现图为记录级。当前
  - 方案：维持上一轮决定，记录；出片时如果西磨在转而磨道空着，再补遮挡
- 分镜「动作」改了：

```diff
@@ -2,3 +2,3 @@
 Riley 站在石台外侧，侧背对镜头、面朝石台里的 Felix，挥一下右手告别；
-然后转身朝街上走两步，走到街上停住，低头看一眼自己的左手、把左手往身侧一抬，自信地点头，然后朝她自己的左边（街的东头，画右）转身，大步走出画右；
+然后转身朝街上走两步，走到街上停住，低头看一眼自己的左手、把左手往身侧一抬，确认哪边是左，自信地点头，然后朝她自己的左边（街的东头，画右）转身，大步走出画右；
 布包在她左胯边随步子晃。
@@ -10,3 +10,3 @@
 Felix 的托板上正好五个面包，一直端在他两手里。
-配角：Felix 看着她往画右走，还没反应过来；
+配角：Felix 看着她往画右走，一时愣住；
 路过的小男孩好奇的是她的靴子。
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-镜头在门脸斜对面（西南边）的街边，朝东北斜对门脸，在 Felix 和 Riley 连线的西侧（和前几镜同一侧）：Felix 在石台里侧、画面左侧三分之一处，Riley 在他右边一点，两人在画面里错开；
+镜头在门脸斜对面（西南边）的街边，朝东北斜对门脸，在 Felix 和 Riley 连线的西侧：Felix 在石台里侧、画面左侧三分之一处，Riley 在他右边一点，两人在画面里错开；
 Riley 从石台外侧走到街上（离镜头更近、画面偏右），再朝她自己的左边（街的东头，画右）走出画；
```

- 分镜「节拍」改了：

```diff
@@ -4,4 +4,4 @@
 1.5–3.5秒 她转身朝街上走两步，走到街上；
-3.5–4.5秒 她停住，低头看一眼自己的左手，把左手往身侧一抬，自信地点头；
-4.5–6秒 一对母子从画右沿街走来，从她身后错身而过，小男孩拽拽母亲的袖子、指着她的短靴，母亲拉着孩子往画左走（单独一拍，Riley 没注意）；
+3.5–4.5秒 她停住，低头看一眼自己的左手，把左手往身侧一抬，确认哪边是左，自信地点头；
+4.5–6秒 一对母子从画右沿街走来，从她身后错身而过，小男孩拽拽母亲的袖子、指着她的短靴，母亲拉着孩子往画左走（单独一拍，Riley 只顾看自己的左手）；
 6–9秒 Riley 朝她自己的左边（画右）转身，大步走出画右，布包随步子晃；
```


### s3_st6

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st6/planning/st6_first_frame.png`）
- **I24** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；overhead Vibia 离镜头 3.5 m（在 Ri
  - 方案：s2_st8 文字与 overhead 改成 Vibia 在 Riley 身后约一米（贴首帧）；s2_st4 起点与擦肩提前到 0–1.5 s；s2_st1 机位改为垫脚石南约 2.5 m、离地 0.5 m；s8_st8 两位妇女站位对调贴首帧；s3_st6 机位推到 (5.8,6.0)、标中近景
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st6/planning/overhead.toml`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I109** [记录·planned·待复核] 时代与世界观·E1 器物：E1 器物：钱碗里三枚币，一枚黄、一枚银白、一枚深色（z_s3st6_bowl.png）。银白的那枚像现代镍币，和账上「碗里是 2 枚红铜 as」也对不上
  - 方案：文字已写碗里两枚红铜小钱；s3_st6 首帧局部修成两枚红铜（可选）还没做
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -1,3 +1,3 @@
 Felix 一个人站在石台里侧，双手还端着木托板，托板上正好五个面包；
-石台上他左手边（画右）是小陶碗。
+石台上他左手边（画右）是小陶碗，碗里有两枚红铜小钱。
 他的目光跟着 Riley 往画右移过去（她已经出画，往她自己的左边、街的东头走了），看出她走反了；
```


### s3 整场 / 未指明镜头

- **I106** [记录·implemented·待复核] 母语听感·N4 口癖/节奏：N4 口癖/节奏：省略号拖音 8 镜以上；basically 仍有 s8_st1、s5_st5（I97 未改）
  - 方案：v7 全部台词按新听感标准重写，s8_st1 去掉 basically

### s3 整场 / 未指明镜头

- **I112** [记录·planned·待复核] 时代与世界观·E6·出处：E6·出处：卡里把 Petronius Sat. 41 说成「浴场闲聊」；该句出自 Trimalchio 宴会场景
  - 方案：c7 卡与 r05 #21 的出处改成 Petronius Sat. 41（宴席闲谈），台词不动；未做

## s4

### s4_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st3/planning/st3_first_frame.png`）
- **I2** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；spec 动作行和走位行、prompt「画面」「走位」「动作」三行、over
  - 方案：s4_st3 统一为从她左后方（街南侧、画右）擦过，toml 补南侧墙与菜筐；s8_st7 Riley 走下路缘石停在街边、老汉走街面；s8_st10 出画路线东移、离镜头≥0.9 m；overhead 闸门 0 blocker
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st10/planning/overhead.toml`
- **I16** [严重·implemented·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；z_s5_st8_right.jpg：驴头和赶车人都朝着镜头走过来，spec 写的是车「直直往
  - 方案：s5_st8 首帧修成车尾朝镜头、往画右拐可读；s4_st3 改「左后方」；s6_st1 墙龛改「在她右后方（画面上在她左边）」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I21** [严重·implemented·待复核] 台词（时长与逻辑）·D4·路线逻辑；R I88：D4·路线逻辑；R I88：s3_st4 复述“Straight… then dextram”；s3_st8 只从柜台走两步到街上便向左走，首帧与两份俯视图也没
  - 方案：v7 s3_st4 改为「Okay… I definitely heard "dextram." No idea what that means. It's fifty-fifty, right? I'm gonna say… left.」，去掉 Straight；s4_st3「Okay, I'm going left…」；s5_st9 回收「"Dextram" means right?」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I72** [记录·planned·待复核] 世界物理·流程（审稿后改动未复核）：流程（审稿后改动未复核）：这四镜的 overhead.toml 在审稿后（19:38–19:41）被改过，资料包标了 `_失效.md`；两位审稿人和本裁决看的都
  - 方案：这四镜在 r3/v7 修改后已重出 overhead、v13 重编、shot_pack sync 63/63 ok；新版走位进下一轮审查复核
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-10
+13
```

- 分镜「动作」改了：

```diff
@@ -2,4 +2,4 @@
 她信心满满地对镜头说话。
-第 3.5 秒前后，一个肩上扛着一捆柴的男人（普通路人，只顾赶路；
-脸刮得干净）从镜头身后走过来，从画右边缘走进画面，侧过身、把肩上的柴往外一挪给她让路，从她右后方擦过，背对镜头往画面深处走远。
+第 7 秒前后，一个肩上扛着一捆柴的男人（普通路人，只顾赶路；
+脸刮得干净）从镜头身后走过来，从画右边缘走进画面，侧过身、把肩上的柴往外一挪给她让路，从她左后方（街的南侧、画右）擦过，背对镜头往画面深处走远。
 走着走着，她猛地停步，鼻翼抽动两下，头先偏左吸一口，再偏右吸一口，脸皱成一团，然后循着味转头看向她右手边。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
 Riley 沿洗衣坊外的窄街朝镜头方向走（朝西），镜头在她伸直的右臂末端、在她面前，跟着她一起走；
-扛柴的男人迎面朝东走：先在镜头身后，第 3.5 秒前后从画右边缘入画，从她右后方（街的南侧）擦过，背对镜头往画面深处走远；
-第 5 秒她停住，洗衣坊敞开的大门在她右手边（画左外），第 7.5 秒她转头看过去，大门在画外。
+扛柴的男人迎面朝东走：先在镜头身后，第 7 秒前后从画右边缘入画，从她左后方（街的南侧、画右）擦过，背对镜头往画面深处走远；
+第 8 秒她停住，洗衣坊敞开的大门在她右手边（画左外），第 10.5 秒她转头看过去，大门在画外。
```

- 分镜「节拍」改了：

```diff
@@ -1,8 +1,8 @@
 0–1.5秒 第 0 秒：她面朝镜头走在窄街上，左手空着，边走边看两边的铺子，嘴闭着；
-1.5–3.5秒 她对着镜头信心满满地说那句话（1.7–3.2 秒）；
-3.5–5秒 她笑着接着走，嘴闭着；
-一个扛柴的男人从画右边缘走进画面，侧身把柴挪开给她让路，从她右后方擦过，背对镜头往深处走（单独一拍，她没注意）；
-5–5.5秒 她猛地停步；
-5.5–7.5秒 她鼻翼抽动两下，头先偏左吸一口，再偏右吸一口，脸皱成一团，嘴闭着；
-7.5–9秒 她循着味转头看向她右手边，眼睛睁大；
-9–10秒 她保持看着那边，嘴闭着
+1.5–6.5秒 她边走边对着镜头信心满满地说那段话，正常语速（1.6–6.3 秒）：Okay, I'm going left. I'm, like, ninety percent sure.，停一下，说 Left. 时果断点一下头；
+6.5–8秒 她笑着接着走，嘴闭着；
+一个扛柴的男人从画右边缘走进画面，侧身把柴挪开给她让路，从她左后方擦过，背对镜头往深处走（单独一拍，她只顾往前走）；
+8–8.5秒 她猛地停步；
+8.5–10.5秒 她鼻翼抽动两下，头先偏左吸一口，再偏右吸一口，脸皱成一团，嘴闭着；
+10.5–12秒 她循着味转头看向她右手边，眼睛睁大；
+12–13秒 她保持看着那边，嘴闭着
```

- 分镜「台词」改了：

```diff
@@ -1 +1,2 @@
-Riley（信心满满，美式英语）：Left. Definitely left.
+Riley（信心满满，美式英语；
+I'm, like, ninety percent sure 带点自我说服，最后 Left. 一锤定音）：Okay, I'm going left. I'm, like, ninety percent sure. Left.
```


### s4_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame.png`）
- **I1** [严重·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml 里 Riley 的朝向：0
  - 方案：s4_st1 1.5–2.5 s 改为整个人转身朝门；7.6 s 起双手投降状、上身左拧从左肩回头瞥 Tertius，再把脸转回镜头说话，overhead 面朝点全程对机位；v7 台词窗顺延（镜长 11→13 s）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/overhead.toml`
- **I2** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；spec 动作行和走位行、prompt「画面」「走位」「动作」三行、over
  - 方案：s4_st3 统一为从她左后方（街南侧、画右）擦过，toml 补南侧墙与菜筐；s8_st7 Riley 走下路缘石停在街边、老汉走街面；s8_st10 出画路线东移、离镜头≥0.9 m；overhead 闸门 0 blocker
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st10/planning/overhead.toml`
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I47** [主要·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；story.md:75「柳条笼子…底下冒出细细的黄白色烟」、:53「一缕烟从门楣上
  - 方案：story.md 与 story.json 同步（柳条笼冒烟、门楣飘烟都去掉）；c7 卡浴袍改裹身长衣；bg3 光线去掉炉烟；s8 负面词同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p4_刮板/p4_刮板.md`
- **I56** [待核实·implemented·待复核] 人物逻辑·C4 / R · 后排工人的首次反应：C4 / R · 后排工人的首次反应：首帧后排两人都背侧身埋头踩布，故没有一开始围观是合理的；但 spec 直到 6.8 秒才让两人一起停脚、看 Riley、互
  - 方案：s4_st1 后排工人写成「一直埋头踩布，这时才抬头看见捏鼻子的她，停下脚，互相看一眼，咧嘴一笑」；出片后核首次抬眼的时机
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/overhead.toml`
- **I72** [记录·planned·待复核] 世界物理·流程（审稿后改动未复核）：流程（审稿后改动未复核）：这四镜的 overhead.toml 在审稿后（19:38–19:41）被改过，资料包标了 `_失效.md`；两位审稿人和本裁决看的都
  - 方案：这四镜在 r3/v7 修改后已重出 overhead、v13 重编、shot_pack sync 63/63 ok；新版走位进下一轮审查复核
- **I82** [记录·implemented·待复核] 人物逻辑·C3：C3：spec 写「举起双手、手心朝着 Tertius（画左），一边往门口慢慢退一边扭头冲他说话」，节拍又写「脸朝着镜头这边」；两句视线互相冲突：她在对 Ter
  - 方案：s4_st1 改为「上身往左一拧、从左肩回头瞥一眼 Tertius，再把脸转回镜头这边」说话，视线不再冲突
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/overhead.toml`
- **I86** [记录·implemented·待复核] 人物逻辑·C4 / C7（I57 未改）：C4 / C7（I57 未改）：后排两工人在 2.6–4.4 秒的大喊期间没反应，到 6.8 秒才停脚；spec 没写他们是埋头没听见、被捏鼻子才注意到
  - 方案：s4_st1 后排工人写成一直埋头踩布、看见她捏鼻子才抬头
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I87** [记录·implemented·待复核] 人物逻辑·C6：C6：「胳膊肘碰同伴」出现在 s4_st1 6.8 秒和 s8_st3 4–5.5 秒；「看长发」出现在 s2_st4、s8_st2、s8_st7 三处；当地人
  - 方案：s4_st1 去掉胳膊肘碰同伴（改成互看一眼、咧嘴笑）；s8_st3 改成对视、用下巴一指；s8_st7 老汉改看短靴和布包
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-11
+13
```

- 分镜「动作」改了：

```diff
@@ -2,3 +2,3 @@
 院子里：靠门这头单独一个齐膝高、约一米见方、只容一人站的石砌踩洗小槽，四周是湿石板地面；
-Tertius 站在这个小槽里，在画面左边约四分之一处、Riley 左前方约三米，一下一下踩着浑浊的黄褐色水里的布；
+Tertius 站在这个小槽里，在画面左边约四分之一处、Riley 左前方约两米半，一下一下踩着浑浊的黄褐色水里的布；
 院子后部一排同样的小石槽里，两个工人在踩布（在 Riley 右边、画面中间偏右的远处）；
@@ -7,3 +7,3 @@
 门洞只有左右两根门柱。
-她深吸一口气，肩膀一耸——脸一下皱成一团，猛地扭回头朝门这边（朝着镜头），张大嘴、清清楚楚地大声嚷出那句话（嘴完全露在外面，手垂在身侧）；
+她深吸一口气，肩膀一耸——脸一下皱成一团，整个人猛地转过身来朝门这边（朝着镜头），张大嘴、清清楚楚地大声嚷出那句话（嘴完全露在外面，手垂在身侧）；
 嚷完才用左手两指捏住鼻尖，往门口退半步。
@@ -11,4 +11,4 @@
 接着朝她挥手赶人。
-后面槽里两个工人停下脚，看着捏着鼻子的她，互相咧嘴一笑，一个用胳膊肘碰碰另一个。
-Riley 松开鼻子，举起双手、手心朝着 Tertius（画左），一边往门口慢慢退一边扭头冲他说话，说完转身快步走出门槛。
+后面槽里两个工人一直埋头踩布，这时才抬头看见捏着鼻子的她，停下脚，互相看一眼，咧嘴一笑。
+Riley 松开鼻子，举起双手做投降状（手心朝前），上身往左一拧、从左肩回头瞥一眼 Tertius，再把脸转回镜头这边，一边侧着身子往门口挪一边说那句话，说完快步走出门槛。
 道具：布包一直挂在她左胯；
```

- 分镜「走位」改了：

```diff
@@ -1,6 +1,7 @@
 镜头在门厅里、门洞东边，朝西北斜着拍进院子；
-Riley 站在门厅靠院子那头，在画面中间偏左，先侧背对镜头、面朝院子，嚷之前扭回头朝着镜头；
-Tertius 在院子靠门这头单独的小踩洗槽里，在画面左边约四分之一处、Riley 左前方约三米；
+Riley 站在门厅靠院子那头，在画面中间偏左，先侧背对镜头、面朝院子，嚷之前整个人转过身来朝着镜头；
+Tertius 在院子靠门这头单独的小踩洗槽里，在画面左边约四分之一处、Riley 左前方约两米半；
 两个工人在院子后部那排小石槽里，画面中间偏右的远处；
 柳条笼在画右后方。
-她 6–9.4 秒往门口慢慢退约半米（在画面左半），9.4 秒转身，约第 10 秒从画左出画、走出门槛。
+她 6.4–10.8 秒脸朝镜头、侧着身子往门口慢慢挪约半米（在画面左半），8 秒从左肩回头瞥一眼 Tertius；
+10.8 秒起快步走向门口，约第 11.2 秒从画左出画、走出门槛。
```

- 分镜「节拍」改了：

```diff
@@ -3,9 +3,12 @@
 只有踩水声；
-1.5–2.5秒 她深吸一口气，肩膀一耸，脸一下皱成一团，猛地扭回头朝门这边，嘴还闭着；
-2.5–4.4秒 她张大嘴，清清楚楚地大声嚷出第一句，手还垂在身侧（2.6–4.4 秒）；
-4.4–5.2秒 Tertius 在石槽里扭头看见她，皱眉（单独一拍）；
-5.2–6秒 Riley 用左手两指捏住鼻尖，往门口退半步，嘴闭着；
-6–6.8秒 Tertius 朝她挥手赶人，喊 Apage（6.1–6.6 秒）（单独一拍）；
-6.8–7.6秒 后面槽里两个工人停下脚，看着捏鼻子的她互相咧嘴一笑，一个用胳膊肘碰碰另一个（单独一拍）；
-7.6–9.4秒 Riley 松开鼻子，举起双手、手心朝着 Tertius，一边慢慢往门口退一边扭头冲他说 Okay, okay — I'm going（7.7–9.3 秒），脸朝着镜头这边；
-9.4–11秒 她说完转身，快步从画左走出门槛，工人们接着踩布
+1.5–2.5秒 她深吸一口气，肩膀一耸，脸一下皱成一团，整个人猛地转过身来朝门这边，嘴还闭着；
+2.5–5秒 她张大嘴，清清楚楚地大声嚷出第一句 Oh — oh no. That's pee!
+，手还垂在身侧（2.6–4.9 秒，oh no 之前顿一下）；
+5–5.7秒 Tertius 在石槽里扭头看见她，皱眉（单独一拍）；
+5.7–6.4秒 Riley 用左手两指捏住鼻尖，往门口退半步，嘴闭着；
+6.4–7.2秒 Tertius 朝她挥手赶人，喊 Apage（6.5–7.0 秒）（单独一拍）；
+7.2–8秒 后面槽里两个工人这才抬头，看见捏鼻子的她，停下脚，互相看一眼，咧嘴一笑（单独一拍）；
+8–8.8秒 Riley 松开鼻子，举起双手、手心朝前，上身往左一拧、从左肩回头瞥一眼 Tertius，再把脸转回镜头这边，嘴闭着；
+8.8–10.8秒 她一边侧着身子往门口挪一边说 Okay, okay — I'm going!
+（8.9–10.7 秒）；
+10.8–13秒 她说完快步从画左走出门槛，工人们接着踩布
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
-他拍：中全景，关系镜头：镜头在门厅里、门洞东边朝西北，Riley 头顶到小腿在画面中间偏左，她扭回头时脸朝镜头，看得清她的嘴和皱鼻子的表情；
+他拍：中全景，关系镜头：镜头在门厅里、门洞东边朝西北，Riley 头顶到小腿在画面中间偏左，她转过身来时脸朝镜头，看得清她的嘴和皱鼻子的表情；
 Tertius 在画左约四分之一处的院子里，踩在单人小石槽里；
```


### s4_st2

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st2/planning/st2_first_frame.png`）
- **I1** [严重·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；overhead.toml 里 Riley 的朝向：0
  - 方案：s4_st1 1.5–2.5 s 改为整个人转身朝门；7.6 s 起双手投降状、上身左拧从左肩回头瞥 Tertius，再把脸转回镜头说话，overhead 面朝点全程对机位；v7 台词窗顺延（镜长 11→13 s）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/overhead.toml`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I46** [主要·implemented·待复核] 母语听感·N2 别扭原因：N2 别扭原因 最终 1 分：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词；L36 "His son called it gross — so Dad
  - 方案：v7 重写全部 Riley 台词：s4_st2 改「…held a coin up to his son's nose and went, "Does this smell?"」；s7_st2「…I swear this was in my history textbook…」；s3_st4、s8_st1、s3_st2 一并重写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I61** [待核实·implemented·待复核] 母语听感·N3 笑点：N3 笑点："…Nope." 的典故（金钱不臭）不知典故者接不住（I98 未核）
  - 方案：v7 s4_st2 改成「…held a coin up to his son's nose and went, "Does this smell?"」，s4_st5「…Nope. Just smells like money. Honestly, he had a point.」，不知道典故也接得住
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I69** [记录·implemented·待复核] 世界物理·P7 服装与动作（带盖侧袋，I76 未改）：P7 服装与动作（带盖侧袋，I76 未改）：s4_st1 首帧里右腿侧袋有袋盖，左腿侧袋形制相同。1.4 秒里要单手掀开袋盖、在 7 枚里分出 1 枚红铜小钱、
  - 方案：s4_st2 写明袋盖敞着、取钱时间放宽；v7 掏钱改在说「Apparently his son…」时（13–16 s）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st2/planning/overhead.toml`
- **I84** [记录·implemented·待复核] 人物逻辑·C4（I80 未改）：C4（I80 未改）：Riley 在敞开的门洞前对镜头大声讲 16 秒，spec 只写「街上只有她一个人」，没交代刚赶她出来的 Tertius；首帧门洞里黑着、
  - 方案：s4_st2 加「她身后的门洞里传出哗哗的踩水声，洗衣坊里的人接着干活」（首帧门洞里没人，用声音交代）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st2/planning/overhead.toml`
- **I100** [记录·implemented·待复核] 台词（时长与逻辑）·D4·指代：D4·指代：held a coin up to his nose，his 可指儿子或爸爸（I91）
  - 方案：v7 s4_st2 改「held a coin up to his son's nose」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I102** [记录·implemented·待复核] 台词（时长与逻辑）·D4·his 指代；R I91：D4·his 指代；R I91：Dad held a coin up to his nose 中 his 既可能是儿子也可能是 Dad；下一镜 Riley 自己
  - 方案：同 I100：v7 改成 his son's nose，指代明确
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-16
+25
```

- 分镜「动作」改了：

```diff
@@ -2,8 +2,11 @@
 洗衣坊敞开的门洞在她身后偏画右，窄街从她身后往画左深处延伸。
-街上这会儿只有她一个人。
-她皱着鼻子、又好笑又嫌弃地讲尿税；
-讲儿子那句之前，她的左手垂到画面下缘外，从布包后面伸进裤子左侧的大口袋，掏出一枚红铜小钱，用拇指和食指捏着举到镜头前。
+街上这会儿只有她一个人；
+她身后的门洞里传出哗哗的踩水声，洗衣坊里的人接着干活。
+她皱着鼻子、又好笑又嫌弃地讲尿税（不说皇帝的名字）；
+说到 Apparently his son thought that was disgusting 时，她边说边把左手垂到画面下缘外，从布包后面伸进裤子左侧的大口袋（袋盖敞着），掏出一枚红铜小钱，用拇指和食指捏着抬回胸前；
+说到 "Does this smell?
+" 时把它举到镜头前。
 道具（钱，p2）：进场——全部钱收在她裤子左侧的大口袋里（5 枚红铜小钱＋1 枚小铜币＋1 枚大黄铜币），她左手空着；
 掏出——她只捏出一枚红铜小钱，手里正好 1 枚，捏在拇指和食指之间；
-出场——这一枚还捏在她左手里，举在镜头前（下一镜闻完放回）；
+出场——这一枚还捏在她左手里，举在镜头前；
 裤兜里剩 4 枚小钱＋小铜币＋大黄铜币。
```

- 分镜「节拍」改了：

```diff
@@ -1,5 +1,9 @@
 0–1.2秒 第 0 秒：她面朝镜头站在洗衣坊门外，皱着鼻子，左手在胸前甩一甩，手里空着，嘴还闭着；
-1.2–5.6秒 她朝身后的门一偏头又转回来看镜头，说第一句和第二句，说到 emperor 时挑眉（1.3–5.6 秒）；
-5.6–7秒 她的左手垂到画面下缘外，从布包后面伸进裤子左侧的大口袋，掏出一枚红铜小钱，捏在拇指和食指之间抬回画面，嘴闭着；
-7–13.5秒 她把这枚铜钱举到镜头前，讲儿子嫌恶心、老爸把钱凑到他鼻子底下问 Smell anything（7.1–13.4 秒，引号前停一下）；
-13.5–16秒 她眯眼看着手里的铜钱，眉毛挑着，嘴闭着，铜钱一直捏在手里
+1.2–5.4秒 说 So get this — they wash clothes in pee here.，说到 pee here 时朝身后的门一偏头又转回来看镜头；
+5.4–7秒 说 Like, actual pee.，脸皱起来；
+7–13秒 说 And the emperor — like, the current emperor — puts a tax on the pee.，说到 emperor 时挑眉；
+13–16秒 说 Apparently his son thought that was disgusting,，边说边把左手垂到画面下缘外，从布包后面伸进裤子左侧敞着袋盖的大口袋，掏出一枚红铜小钱，捏在拇指和食指之间抬回画面、停在胸前；
+16–21.3秒 说 so the emperor just held a coin up to his son's nose and went,，铜钱捏在胸前；
+21.3–23秒 引号前停一下，说 "Does this smell?
+" 时把铜钱举到镜头前；
+23–25秒 她眯眼看着手里的铜钱，眉毛挑着，嘴闭着，铜钱一直捏在手里
```

- 分镜「台词」改了：

```diff
@@ -1,3 +1,5 @@
-Riley（又好笑又嫌弃，美式英语）：They wash clothes in pee. And the emperor?
-He taxes it. His son called it gross — so Dad held a coin up to his nose: "Smell anything?
+Riley（又好笑又嫌弃，美式英语；
+不说皇帝的名字；
+引号前停一下，"Does this smell?
+" 学皇帝的口气）：So get this — they wash clothes in pee here. Like, actual pee. And the emperor — like, the current emperor — puts a tax on the pee. Apparently his son thought that was disgusting, so the emperor just held a coin up to his son's nose and went, "Does this smell?
 "
```


### s4_st5

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st5/planning/st5_first_frame.png`）
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I61** [待核实·implemented·待复核] 母语听感·N3 笑点：N3 笑点："…Nope." 的典故（金钱不臭）不知典故者接不住（I98 未核）
  - 方案：v7 s4_st2 改成「…held a coin up to his son's nose and went, "Does this smell?"」，s4_st5「…Nope. Just smells like money. Honestly, he had a point.」，不知道典故也接得住
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I102** [记录·implemented·待复核] 台词（时长与逻辑）·D4·his 指代；R I91：D4·his 指代；R I91：Dad held a coin up to his nose 中 his 既可能是儿子也可能是 Dad；下一镜 Riley 自己
  - 方案：同 I100：v7 改成 his son's nose，指代明确
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-8
+12
```

- 分镜「动作」改了：

```diff
@@ -1,3 +1,4 @@
-同一处、同一条窄街，自拍，镜头和上一镜同一个方向、只是近一点：洗衣坊的门洞在她身后偏画右，窄街往画左深处延伸。
-Riley 右臂伸直持镜，左手捏着那枚红铜小钱，把它凑到自己鼻子底下，夸张地闻两下，停住，一本正经地看着镜头说那个词，接着笑出声；
+洗衣坊门外的窄街，自拍，镜头朝西偏北、离她很近：洗衣坊的门洞在她身后偏画右，窄街往画左深处延伸。
+Riley 右臂伸直持镜，左手捏着那枚红铜小钱，把它凑到自己鼻子底下，夸张地闻两下，停住，一本正经地看着镜头说 …Nope. Just smells like money.，接着憋不住笑出声，笑着补一句 Honestly?
+He's got a point.；
 然后左手垂到画面下缘外，从布包后面把铜钱塞回裤子左侧的大口袋，空手抬回画面，摊开五指给镜头看一下。
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-位置和朝向同上一镜：Riley 背对洗衣坊门口、面对镜头；
-镜头在她伸直的右臂末端，比上一镜稍近，朝西偏北：门洞在她身后偏画右，街往画左深处延伸。
+Riley 背对洗衣坊门口、面对镜头；
+镜头在她伸直的右臂末端、离她很近，朝西偏北：门洞在她身后偏画右，街往画左深处延伸。
```

- 分镜「节拍」改了：

```diff
@@ -3,5 +3,8 @@
 1.5–2.5秒 她停住，一本正经地盯着镜头，铜钱还在鼻子底下（单独一拍，嘴闭着）；
-2.5–3.3秒 她说 Nope（2.6–3.1 秒）；
-3.3–5秒 她笑出声，肩膀抖；
-5–6.5秒 她左手垂到画面下缘外，从布包后面把铜钱塞回裤子左侧的大口袋，嘴闭着；
-6.5–8秒 她空手抬回画面，摊开五指给镜头看一下，笑着，嘴闭着
+2.5–3.3秒 她说 …Nope.（2.6–3.1 秒）；
+3.3–5.3秒 她还一本正经地说 Just smells like money.（3.5–5.2 秒），铜钱还在鼻子底下；
+5.3–6.3秒 她憋不住笑出声，肩膀抖，铜钱从鼻子底下放低；
+6.3–8.8秒 她笑着说 Honestly?
+He's got a point.（6.4–8.6 秒）；
+8.8–10.3秒 她左手垂到画面下缘外，从布包后面把铜钱塞回裤子左侧的大口袋，嘴闭着；
+10.3–12秒 她空手抬回画面，摊开五指给镜头看一下，笑着，嘴闭着
```

- 分镜「镜头」改了：

```diff
@@ -1,4 +1,4 @@
 自拍：她伸直右臂持镜，镜头就在她手里；
-近景，单人，比上一镜更近，她的脸和那枚铜钱在画面上半；
-镜头方向和上一镜相同，门洞在画右；
+近景，单人，镜头离她很近，她的脸和那枚铜钱在画面上半；
+镜头朝西偏北，门洞在画右；
 手持；
```

- 分镜「台词」改了：

```diff
@@ -1 +1,3 @@
-Riley（一本正经，再笑出来，美式英语）：…Nope.
+Riley（先一本正经，憋不住笑出来，美式英语；
+Nope 前先闻钱、停一拍）：…Nope. Just smells like money. Honestly?
+He's got a point.
```


### s4_st4

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st4/planning/st4_first_frame.png`）
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I93** [记录·planned·待复核] 人物逻辑·C2 / C7 · 去浴场的动机没接上：C2 / C7 · 去浴场的动机没接上：s4_st4 收在「I still smell like pee」，s8_st1 去浴场只靠台词「everybody h
  - 方案：s8_st1 结尾加抬手闻袖口、皱鼻、加快脚步（未做；v7 已在 s4_st4「And —」之后加闻袖子）
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-16
+22
```

- 分镜「动作」改了：

```diff
@@ -4,4 +4,5 @@
 镜头在路口南边那条街的路面中间、离路口约两米半，低机位（约腰高）正对北街朝北看：Riley 沿北边那条街从画面深处走过来，刚走进路口，再慢慢走一米多到路口中央停下，左右看看。
-她抬起右臂，偏头把鼻子凑到右肩挽起的短袖袖口上闻一下，立刻皱眉、把头往后一仰、在鼻子前扇扇手。
-然后她转向镜头，小声、慢慢地说那句话，最后无奈地耸耸肩，自己笑了。
+然后她转向镜头小声说起来：先说店都关了、大概是午睡时间，再说自己完全不知道这是哪儿；
+说到 And — 时话停住，抬起右臂，偏头把鼻子凑到右肩挽起的短袖袖口上闻一下，立刻皱眉、把头往后一仰、在鼻子前扇扇手，再转回镜头说完 yep. Still smell like pee. Great.；
+最后无奈地耸耸肩，自己笑了。
 道具：布包一直挂在她左胯，全身入画时看得见；
```

- 分镜「走位」改了：

```diff
@@ -2,3 +2,3 @@
 Riley 第 0 秒已经走进路口北半边（画面正中），0–2.5 秒慢慢走一米多到路口中央停下，左右张望；
-第 6.3 秒起面对镜头。
+第 4.7 秒起面对镜头（14–16 秒偏头闻右肩袖口）。
 镜头从全景慢慢推近，停在离她约一米半处，成腰以上的中景。
```

- 分镜「节拍」改了：

```diff
@@ -3,6 +3,10 @@
 2.5–4秒 她左右看看四条一模一样的街，嘴闭着；
-4–5.3秒 她抬起右臂，偏头把鼻子凑到右肩挽起的袖口上闻一下；
-5.3–6.3秒 她立刻皱眉，头往后一仰，在鼻子前扇扇手，嘴闭着；
-6.3–7秒 她转向镜头，嘴闭着；
-7–13秒 她小声、慢慢地说那句话，每句之间停一下（7.1–12.9 秒）；
-13–16秒 她嘴一直闭着：无奈地耸耸肩、摊开双手，自己笑了，再左右看看四条一模一样的街
+4–4.7秒 她转向镜头，嘴闭着；
+4.7–6.7秒 她小声说 Okay, so… everything's closed.（so… 之后停一下）；
+6.7–10.2秒 说 I think it's, like, nap time or something.；
+10.2–13.6秒 说 And I have no idea where I am.；
+13.6–14秒 说 And —，话停住；
+14–16秒 她抬起右臂，偏头把鼻子凑到右肩挽起的袖口上闻一下，立刻皱眉，头往后一仰，在鼻子前扇扇手，嘴闭着；
+16–18.3秒 她转回镜头，说 yep. Still smell like pee.；
+18.3–19.3秒 平平地说 Great.；
+19.3–22秒 她嘴一直闭着：无奈地耸耸肩、摊开双手，自己笑了，再左右看看四条一模一样的街
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
-他拍：24mm 广角，全景缓推到中景：开头低机位（约腰高）正对北街，她全身在空荡的路口、约占画高三分之一，第 3 秒起镜头慢慢推近、升到胸口高，到第 12 秒停在离她约一米半处，她腰以上占满画面；
+他拍：24mm 广角，全景缓推到中景：开头低机位（约腰高）正对北街，她全身在空荡的路口、约占画高三分之一，第 3 秒起镜头慢慢推近、升到胸口高，到第 15 秒停在离她约一米半处，她腰以上占满画面；
 平视；
```

- 分镜「台词」改了：

```diff
@@ -1 +1,4 @@
-Riley（小声、又累又好笑，说得慢，美式英语）：It's noon. Everything's closed. I'm totally lost… and I still smell like pee.
+Riley（小声、又累又好笑，正常语速，美式英语；
+so… 之后停一下；
+And — 之后话停住、闻完袖子再说 yep；
+Great. 平平地说）：Okay, so… everything's closed. I think it's, like, nap time or something. And I have no idea where I am. And — yep. Still smell like pee. Great.
```


### s4 整场 / 未指明镜头

- **I106** [记录·implemented·待复核] 母语听感·N4 口癖/节奏：N4 口癖/节奏：省略号拖音 8 镜以上；basically 仍有 s8_st1、s5_st5（I97 未改）
  - 方案：v7 全部台词按新听感标准重写，s8_st1 去掉 basically

### s4 整场 / 未指明镜头

- **I112** [记录·planned·待复核] 时代与世界观·E6·出处：E6·出处：卡里把 Petronius Sat. 41 说成「浴场闲聊」；该句出自 Trimalchio 宴会场景
  - 方案：c7 卡与 r05 #21 的出处改成 Petronius Sat. 41（宴席闲谈），台词不动；未做

## s8

### s8_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st1/planning/st1_first_frame.png`）
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I20** [严重·implemented·待复核] 台词（时长与逻辑）·D6 听得清：D6 听得清 最终 1 分：环境声不盖过台词；悄悄话、远处的话能听清；prompt.txt 第 2 行与末行声音模板无「对白压过环境声」；s8_st1 合唱、s
  - 方案：编译器 v14：有台词的镜头声音行加「对白优先：有人说话时环境声和动作声压低到对白下面，每句台词清楚可辨」（ep01 共 82 处）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I46** [主要·implemented·待复核] 母语听感·N2 别扭原因：N2 别扭原因 最终 1 分：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词；L36 "His son called it gross — so Dad
  - 方案：v7 重写全部 Riley 台词：s4_st2 改「…held a coin up to his son's nose and went, "Does this smell?"」；s7_st2「…I swear this was in my history textbook…」；s3_st4、s8_st1、s3_st2 一并重写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I64** [待核实·implemented·待复核] 时代与世界观·E6·推定史实的确定性（上一轮 I108、I67 未改）、R：E6·推定史实的确定性（上一轮 I108、I67 未改）、R：「at two, everybody hits the baths」、「Dinner here i
  - 方案：v7 改成不那么绝对的说法：s5_st1「people eat dinner here at, like, three-thirty」、s8_st1「Apparently they do their afternoon thing right around two」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I93** [记录·planned·待复核] 人物逻辑·C2 / C7 · 去浴场的动机没接上：C2 / C7 · 去浴场的动机没接上：s4_st4 收在「I still smell like pee」，s8_st1 去浴场只靠台词「everybody h
  - 方案：s8_st1 结尾加抬手闻袖口、皱鼻、加快脚步（未做；v7 已在 s4_st4「And —」之后加闻袖子）
- **I108** [记录·implemented·待复核] 时代与世界观·E6 史实一致（R：I108）：E6 史实一致（R：I108）：「basically Pompeii's two o'clock alarm. And at two, everybody hi
  - 方案：同 I64：v7 改成带 like / apparently / right around 的说法，不再是全称断言
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-17
+23
```

- 分镜「动作」改了：

```diff
@@ -4,4 +4,4 @@
 Riley 沿着白墙下的街面，从约七米外用正常步速朝镜头走来，走到离镜头约三米处停住脚，偏头把右耳朝向白墙、右手抬到耳边听，抬头看墙头；
-然后转向镜头压低声音说话；
-说完咧嘴一笑，沿着白墙继续往前走（去浴场的方向），从镜头左侧走出画。
+然后转向镜头，兴奋地对镜头说话，说到 bath time 时咧嘴一笑；
+说完沿着白墙继续往前走（去浴场的方向），从镜头左侧走出画。
 道具：钱都在她裤子左侧的大口袋里，这一镜不拿出来；
```

- 分镜「节拍」改了：

```diff
@@ -7,3 +7,6 @@
 5.5–6秒 她转回来面向镜头，眼睛发亮，还没开口；
-6–14秒 她压低声音、兴奋地对镜头说那三句，句与句之间各停半拍（6.1–13.8 秒）；
-14–17秒 她咧嘴一笑，迈步贴着画左继续往前走，从镜头左侧走出画，没回头，不说话
+6–19秒 她站在原地、不再靠近，兴奋地对镜头说那几句（6.1–18.8 秒）：6.1–7.0 秒 Hear that?
+，7.4–9.4 秒 That's the temple of Isis.，9.8–16.6 秒 Apparently they do their afternoon thing right around two — and two is when the baths open.，17.1–18.8 秒 So… bath time!
+（So 后停半拍，说到 bath time 时咧嘴一笑）；
+19–23秒 她咧嘴笑着迈步，贴着画左继续往前走，约 22 秒从镜头左侧走出画，没回头，不说话；
+最后一秒街上空着，墙后的叉铃声和合唱还在
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1,2 @@
-Riley（压低声音、兴奋，美式英语）：Hear that?
-That's the Temple of Isis — basically Pompeii's two o'clock alarm. And at two, everybody hits the baths.
+Riley（兴奋，美式英语）：Hear that?
+That's the temple of Isis. Apparently they do their afternoon thing right around two — and two is when the baths open. So… bath time!
```


### s8_st2

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/_r3_before/st2_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/st2_first_frame.png`（现行）
- **I2** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；spec 动作行和走位行、prompt「画面」「走位」「动作」三行、over
  - 方案：s4_st3 统一为从她左后方（街南侧、画右）擦过，toml 补南侧墙与菜筐；s8_st7 Riley 走下路缘石停在街边、老汉走街面；s8_st10 出画路线东移、离镜头≥0.9 m；overhead 闸门 0 blocker
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st10/planning/overhead.toml`
- **I22** [严重·implemented·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；首帧左上高窗是木框加竖条、横条的分格窗（z_s8st2
  - 方案：s8_st2 首帧局部修成光秃的方窗洞，ffp 负面词加「窗格、窗框分格、带玻璃的窗」；s3_st8 首帧去掉墙上竖管，负面词加「墙上的竖管、落水管」；s2_st5/st7 文字删掉石块形状描写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/st2_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I47** [主要·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；story.md:75「柳条笼子…底下冒出细细的黄白色烟」、:53「一缕烟从门楣上
  - 方案：story.md 与 story.json 同步（柳条笼冒烟、门楣飘烟都去掉）；c7 卡浴袍改裹身长衣；bg3 光线去掉炉烟；s8 负面词同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p4_刮板/p4_刮板.md`
- **I70** [记录·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒：首帧里 Riley 离门槛约 1 m 以上、正在迈步（脚的位置明显在门框前面）；节拍和 overhead (3,13.6) 写的是「
  - 方案：s8_st2 文字和 overhead 起点改成第 0 秒已进门一步，0–1.5 s 只再走一步（照候选图）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/overhead.toml`
- **I87** [记录·implemented·待复核] 人物逻辑·C6：C6：「胳膊肘碰同伴」出现在 s4_st1 6.8 秒和 s8_st3 4–5.5 秒；「看长发」出现在 s2_st4、s8_st2、s8_st7 三处；当地人
  - 方案：s4_st1 去掉胳膊肘碰同伴（改成互看一眼、咧嘴笑）；s8_st3 改成对视、用下巴一指；s8_st7 老汉改看短靴和布包
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I116** [记录·wontfix·待复核] Prompt 文本·T7·长度与重点：T7·长度与重点：s5_st14 15 秒里 Asellina 8 步以上操作；s8_st2 15 秒数 7 枚钱再付再收；s6_st1/2/3 长达 4471
  - 方案：保留 s5_st14 擦台面、点水两拍和 s8_st2 数钱；固定负面词已去重
- 分镜「动作」改了：

```diff
@@ -2,6 +2,6 @@
 外门开在画右，门外是明亮的午后天光；
-门内靠墙一张矮木凳上坐着中年女门房（不立卡的配角，不说话、不看镜头：四十多岁，深色及踝长 tunica，头发挽起，腰带上挂着一个抽绳扎口的灰褐色小布钱袋）。
+门内靠画左那面墙一张矮木凳上坐着中年女门房（不立卡的配角，不说话、不看镜头：四十多岁，深色及踝长 tunica，头发挽起，腰带上挂着一个抽绳扎口的灰褐色小布钱袋）。
 画面里共两个人：Riley 和门房。
 第 0 秒门房低着头，用手指拨弄腰间钱袋的抽绳，还没注意到来人。
-Riley 从画右的外门跨进来，走两步停在门房面前（伸手够得着）。
+Riley 已经从画右的外门进来一步，再走一步停在门房面前（伸手够得着）。
 门房听见脚步声才抬头，看见一个打扮古怪的外地女人，眉毛一挑，目光从她披散的乌黑长发落到那双系带短靴上，然后伸出右手、掌心朝上。
```

- 分镜「走位」改了：

```diff
@@ -1,4 +1,4 @@
-镜头在门厅里、离外门约三米，斜对着外门：外门在画右，门房的矮凳在画面中间偏左、靠门内东侧的墙；
+镜头在门厅里、离外门约三米，斜对着外门：外门在画右，门房的矮凳在画面中间偏左、靠画左那面墙；
 去厅里的路在镜头身后左侧。
-Riley 从画右的外门进来，走两步停在门房面前、离她不到一米，侧身对镜头、脸朝画左的门房。
+Riley 第 0 秒已经进门一步，再走一步停在门房面前、离她不到一米，侧身对镜头、脸朝画左的门房。
 配角一行：门房——0–1.5 秒低头弄钱袋的抽绳，没看见她；
```

- 分镜「节拍」改了：

```diff
@@ -1,5 +1,5 @@
-0–1.5秒 第 0 秒：Riley 刚从画右明亮的外门跨进门槛，双手空着，布包挂在左胯，脸朝画左的门房；
-门房坐在矮凳上，低着头，用手指拨弄腰间钱袋的抽绳，没看她；
+0–1.5秒 第 0 秒：Riley 已经从画右明亮的外门进来一步，正迈步走向门房，双手空着，布包挂在左胯，脸朝画左的门房；
+门房坐在矮凳上，低着头，用手指拨弄腰间钱袋的抽绳；
 这一拍不说话；
-Riley 走两步，停在门房面前、伸手够得着的地方；
+Riley 再走一步，停在门房面前、伸手够得着的地方；
 1.5–3秒 门房听见脚步声抬起头，看见她，眉毛一挑，目光从她披散的乌黑长发落到那双系带短靴上（门房的反应拍，单独一拍），这一拍不说话；
```

- 分镜「光线」改了：

```diff
@@ -1,3 +1,3 @@
 门外的午后天光从外门照进来，门口一块亮；
-门厅里偏暗，拱顶下一个小高窗洞透进一道天光，空气里有薄薄的水汽；
+门厅里偏暗，墙上高处一个光秃秃的方形窗洞透进一道天光，空气里有薄薄的水汽；
 温暖、潮湿、柔和。
```


### s8_st10

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st10/planning/st10_first_frame.png`）
- **I2** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；spec 动作行和走位行、prompt「画面」「走位」「动作」三行、over
  - 方案：s4_st3 统一为从她左后方（街南侧、画右）擦过，toml 补南侧墙与菜筐；s8_st7 Riley 走下路缘石停在街边、老汉走街面；s8_st10 出画路线东移、离镜头≥0.9 m；overhead 闸门 0 blocker
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st10/planning/overhead.toml`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I64** [待核实·implemented·待复核] 时代与世界观·E6·推定史实的确定性（上一轮 I108、I67 未改）、R：E6·推定史实的确定性（上一轮 I108、I67 未改）、R：「at two, everybody hits the baths」、「Dinner here i
  - 方案：v7 改成不那么绝对的说法：s5_st1「people eat dinner here at, like, three-thirty」、s8_st1「Apparently they do their afternoon thing right around two」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I72** [记录·planned·待复核] 世界物理·流程（审稿后改动未复核）：流程（审稿后改动未复核）：这四镜的 overhead.toml 在审稿后（19:38–19:41）被改过，资料包标了 `_失效.md`；两位审稿人和本裁决看的都
  - 方案：这四镜在 r3/v7 修改后已重出 overhead、v13 重编、shot_pack sync 63/63 ok；新版走位进下一轮审查复核
- **I88** [记录·implemented·待复核] 人物逻辑·C4：C4：首帧里门房已经满面笑意地仰头看 Riley，3.5–5 秒才「摇头失笑」，笑意被提前用掉，反应拍的变化变小
  - 方案：s8_st10 文字改成第 0 秒门房嘴角已带一点笑意，3.5–5 s 摇头笑出声
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-8
+11
```

- 分镜「动作」改了：

```diff
@@ -1,5 +1,5 @@
-接上一镜，同一间窄小的外门门厅（赭黄抹灰墙、深红墙裙，黑白小方块石子地，四壁光秃；
-场景图只借墙面和地面的材质），换一个近一点的机位。
+浴场女区外门里的窄小门厅（赭黄抹灰墙、深红墙裙，黑白小方块石子地，四壁光秃；
+场景图只借墙面和地面的材质），近景机位。
 Riley 站在坐着的门房面前，转过脸对镜头小声说话；
-门房看着她对着空气说话，摇头失笑，右手朝画左（厅里）一挥，像在说「随你吧，进去吧」。
+门房抬头看着她对着空气说话，嘴角本来就带着一点笑意，这下摇头笑出了声，右手朝画左（厅里）一挥，像在说「随你吧，进去吧」。
 Riley 点点头，朝画左走，从镜头左侧走出画，进厅里。
```

- 分镜「节拍」改了：

```diff
@@ -1,8 +1,9 @@
 0–1秒 第 0 秒：Riley 站在门房面前，已经转过脸朝着镜头，两手空着，布包挂在左胯，嘴角压着一点笑；
-门房坐在她身后画左的矮凳上，抬头看着她，右手搭在腰间的钱袋上；
+门房坐在她身后画左的矮凳上，抬头看着她，嘴角带着一点笑意，右手搭在腰间的钱袋上；
 这一拍不说话；
-1–3.5秒 Riley 小声对镜头说那句话（1.1–3.1 秒）；
+1–6.5秒 Riley 小声对镜头说那两句（1.1–6.4 秒）：1.1–5.2 秒 Okay, it was literally one tiny coin to get in.，停半拍，5.6–6.4 秒 That's it!
+（眉毛一扬）；
 门房看着她；
-3.5–5秒 门房摇头失笑，右手朝画左（厅里）一挥（门房的反应拍，单独一拍），这一拍不说话；
-5–6.5秒 Riley 回头看她一眼，点点头，朝画左走，从镜头左侧走出画，不说话；
-6.5–8秒 门房看着她走开的方向，嘴角一撇，转回去看门外（门房的反应拍，单独一拍），这一拍不说话
+6.5–8秒 门房摇头笑出了声，右手朝画左（厅里）一挥（门房的反应拍，单独一拍），这一拍不说话；
+8–9.5秒 Riley 回头看她一眼，点点头，朝画左走，从镜头左侧走出画，不说话；
+9.5–11秒 门房看着她走开的方向，嘴角一撇，转回去看门外（门房的反应拍，单独一拍），这一拍不说话
```

- 分镜「光线」改了：

```diff
@@ -1,3 +1,3 @@
 门外的午后天光从外门照进来，门口一块亮；
-门厅里偏暗，拱顶下一个小高窗洞透进一道天光，空气里有薄薄的水汽；
+门厅里偏暗，墙上高处一个光秃秃的方形窗洞透进一道天光，空气里有薄薄的水汽；
 温暖、潮湿、柔和。
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1 @@
-Riley（小声，美式英语）：Cover charge?
-One tiny coin.
+Riley（小声、又惊又喜，美式英语）：Okay, it was literally one tiny coin to get in. That's it!
```


### s8_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st3/planning/st3_first_frame.png`）
- **I23** [严重·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；牵驴的车夫留着修过的短须（z_s5st8_man.png）
  - 方案：c7 卡、s8 文字和 st3/st4/st5/st6/st8/st9 首帧 prompt 的「浴袍」改成「粗亚麻裹身长衣」，剧级负面词加「翻领浴袍，毛巾布浴袍」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I27** [严重·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数 最终 1 分：动作节拍的秒数排得下（走多远、几秒到），没有挤压；overhead Riley (13.6,20.6) 离镜头 3.4 m、Vib
  - 方案：s2_st4 擦肩提前到 0–1.5 s、老人挪到西人行道；s8_st3 起点前移 0.6 m；s8_st7 老汉路线重排、约 6.5 s 出画右；s3_st1 第 0 秒改为已站定；v7 各镜节拍按新镜长重排，overhead 闸门 63 镜 0 blocker 0 warning
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`
- **I47** [主要·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；story.md:75「柳条笼子…底下冒出细细的黄白色烟」、:53「一缕烟从门楣上
  - 方案：story.md 与 story.json 同步（柳条笼冒烟、门楣飘烟都去掉）；c7 卡浴袍改裹身长衣；bg3 光线去掉炉烟；s8 负面词同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p4_刮板/p4_刮板.md`
- **I81** [记录·implemented·待复核] 人物逻辑·C4 / C6：C4 / C6：首帧里右边石凳里侧两位妇女已经带着笑、脸转向走道，左边第三位也笑着抬头；spec 写 0 秒「在梳头、擦胳膊、闲坐」，4–7 秒才「一个接一个停
  - 方案：s8_st3 第 0 秒照首帧写（几位已笑着看走道）；反应链改为画左中间那位抬头、和同伴对视、用下巴一指，再到画右挽发的年轻妇女回头
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st3/planning/overhead.toml`
- **I83** [记录·implemented·待复核] 人物逻辑·C4（I79 未改）：C4（I79 未改）：Helvia 没有任何目光扫向 Riley 的湿衬衫、工装裤和靴子；厅里的妇女（s8_st3、st8）都看了，邻座人偏偏全程不看
  - 方案：s8_st5 Helvia 先扫一眼 Riley 汗湿的衬衫和工装裤，嘴角一抽，再抬下巴
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I87** [记录·implemented·待复核] 人物逻辑·C6：C6：「胳膊肘碰同伴」出现在 s4_st1 6.8 秒和 s8_st3 4–5.5 秒；「看长发」出现在 s2_st4、s8_st2、s8_st7 三处；当地人
  - 方案：s4_st1 去掉胳膊肘碰同伴（改成互看一眼、咧嘴笑）；s8_st3 改成对视、用下巴一指；s8_st7 老汉改看短靴和布包
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I92** [记录·planned·待复核] 人物逻辑·C2 · 目的与动作脱节：C2 · 目的与动作脱节：st3 spec「动作」写了更衣厅有放衣物的壁龛，七个妇女都裹浴袍；Riley 只「侧过身先看画左、再看画右，有点不知所措」，st8 
  - 方案：s8_st8 扇领口前加半秒：瞄一眼壁龛和妇女的裹身长衣，再低头看自己的衣服、抿嘴，然后转身进门洞（未做）
- **I110** [记录·wontfix·待复核] 时代与世界观·E1 器物：E1 器物：她手里是带长柄的单排宽齿梳（z_s8st3_comb.png），样子偏现代；罗马常见的是骨或木做的双面长方梳
  - 方案：记录，不修图
- 分镜「动作」改了：

```diff
@@ -3,4 +3,5 @@
 七个当地妇女（普通路人，不说话、不看镜头，但会好奇地打量 Riley；
-都裹着米白亚麻浴袍，从肩膀一直裹到小腿，肩头和上臂也盖在浴袍里；
-头发挽起）坐在两侧石凳上：画左石凳三个，画右石凳四个，有的在梳头、有的在擦胳膊、有的靠墙闲坐；
+都裹着米白粗亚麻裹身长衣，从肩膀一直裹到小腿，肩头和上臂也盖在粗亚麻裹身长衣里；
+头发挽起）坐在两侧石凳上：画左石凳三个——靠前那位低头梳头，中间那位双手叠放在膝上、低着头闲坐，靠里那位抬着头、带着笑朝走道看；
+画右石凳四个——里侧两位已经笑着朝走道看，第三位低头闲坐，最靠前那位年轻妇女正抬手挽头发、脸朝自己那边的墙；
 厅的尽头是通往热水室的拱形门洞，白色蒸汽从那里一阵阵漫出来，门洞边的尽头墙角立着一只青铜炭火盆。
@@ -8,3 +9,3 @@
 Riley 穿着全套衣服（衬衫、工装裤、短靴，面包布包挂在左胯），背对镜头从画面下方（镜头身后、入口方向）走进画，沿厅中间的通道往里走，走到厅中段停住，侧过身左右看。
-两侧的妇女一个接一个停下手里的事看她：先是画左石凳中间那位，停下擦胳膊的手，视线从 Riley 的靴子扫到衬衫，用胳膊肘碰碰身边的同伴，两人一起看着她；
+两侧低着头的妇女一个接一个抬头看她：先是画左石凳中间那位，抬起头，视线从 Riley 的靴子扫到衬衫，侧头和身边的同伴对视一眼，用下巴朝 Riley 指了一下，两人一起看着她；
 接着画右石凳靠前一个正在挽头发的年轻妇女停下手，回过头来打量她；
```

- 分镜「走位」改了：

```diff
@@ -5,3 +5,3 @@
 」；
-她的同伴——被碰了才转头，憋着笑；
+她的同伴——对视以后转头看 Riley，憋着笑；
 画右挽头发的年轻妇女——好奇地回头上下打量。
```

- 分镜「节拍」改了：

```diff
@@ -1,6 +1,8 @@
 0–2.5秒 第 0 秒：Riley 的背影刚从画面下方走进画——头、肩和上半身背影在画面下部正中，背对镜头往厅里走，布包挂在左胯；
-两侧石凳上的七个妇女在梳头、擦胳膊、闲坐，蒸汽从深处的门洞漫出来；
+两侧石凳上的七个妇女：画左靠前那位低头梳头、中间那位双手叠放低头闲坐、靠里那位带着笑朝走道看；
+画右里侧两位已经笑着朝走道看，最靠前那位年轻妇女正抬手挽头发；
+蒸汽从深处的门洞漫出来；
 这一拍不说话；
 2.5–4秒 Riley 走到厅中段停住，侧过身先看画左、再看画右，有点不知所措；
-4–5.5秒 画左石凳中间那位妇女停下擦胳膊的手，视线从 Riley 的靴子扫到衬衫，用胳膊肘碰碰身边的同伴，两人一起看着她（妇女的反应拍，单独一拍）；
+4–5.5秒 画左石凳中间那位妇女抬起头，视线从 Riley 的靴子扫到衬衫，侧头和身边的同伴对视一眼，用下巴朝 Riley 指了一下，两人一起看着她（妇女的反应拍，单独一拍）；
 5.5–7秒 画右石凳靠前挽头发的年轻妇女停下手，回过头来打量 Riley（第二个反应拍，单独一拍）；
```


### s8_st8

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st8/planning/st8_first_frame.png`）
- **I23** [严重·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；牵驴的车夫留着修过的短须（z_s5st8_man.png）
  - 方案：c7 卡、s8 文字和 st3/st4/st5/st6/st8/st9 首帧 prompt 的「浴袍」改成「粗亚麻裹身长衣」，剧级负面词加「翻领浴袍，毛巾布浴袍」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I24** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；overhead Vibia 离镜头 3.5 m（在 Ri
  - 方案：s2_st8 文字与 overhead 改成 Vibia 在 Riley 身后约一米（贴首帧）；s2_st4 起点与擦肩提前到 0–1.5 s；s2_st1 机位改为垫脚石南约 2.5 m、离地 0.5 m；s8_st8 两位妇女站位对调贴首帧；s3_st6 机位推到 (5.8,6.0)、标中近景
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st6/planning/overhead.toml`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I47** [主要·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；story.md:75「柳条笼子…底下冒出细细的黄白色烟」、:53「一缕烟从门楣上
  - 方案：story.md 与 story.json 同步（柳条笼冒烟、门楣飘烟都去掉）；c7 卡浴袍改裹身长衣；bg3 光线去掉炉烟；s8 负面词同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p4_刮板/p4_刮板.md`
- **I83** [记录·implemented·待复核] 人物逻辑·C4（I79 未改）：C4（I79 未改）：Helvia 没有任何目光扫向 Riley 的湿衬衫、工装裤和靴子；厅里的妇女（s8_st3、st8）都看了，邻座人偏偏全程不看
  - 方案：s8_st5 Helvia 先扫一眼 Riley 汗湿的衬衫和工装裤，嘴角一抽，再抬下巴
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I92** [记录·planned·待复核] 人物逻辑·C2 · 目的与动作脱节：C2 · 目的与动作脱节：st3 spec「动作」写了更衣厅有放衣物的壁龛，七个妇女都裹浴袍；Riley 只「侧过身先看画左、再看画右，有点不知所措」，st8 
  - 方案：s8_st8 扇领口前加半秒：瞄一眼壁龛和妇女的裹身长衣，再低头看自己的衣服、抿嘴，然后转身进门洞（未做）
- 分镜「动作」改了：

```diff
@@ -1,4 +1,4 @@
-接上一镜：Riley 站在更衣温水厅中间，被几个妇女盯着看。
-画左西墙石凳上坐着两位妇女（普通路人，不说话、不看镜头：一位四十来岁、一位三十来岁，深棕色头发挽成髻，都裹着米白亚麻浴袍，从肩膀一直裹到小腿，肩头和上臂也盖在浴袍里）；
-画右深处、东墙石凳上还远远坐着三个裹浴袍的妇女（在蒸汽里虚化，只是远景）。
+更衣温水厅：Riley 站在厅中间，被几个妇女盯着看。
+画左西墙石凳上坐着两位妇女（普通路人，不说话、不看镜头：一位四十来岁、一位三十来岁，深棕色头发挽成髻，都裹着米白粗亚麻裹身长衣，从肩膀一直裹到小腿，肩头和上臂也盖在粗亚麻裹身长衣里）；
+画右深处、东墙石凳上还远远坐着三个裹粗亚麻裹身长衣的妇女（在蒸汽里虚化，只是远景）。
 画面里共六个人：Riley、画左的两位妇女和画右深处的三个妇女。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
 镜头在厅的西南侧、靠西墙石凳，朝北略偏东斜对 Riley：Riley 站在厅中间通道偏西的地方、离画左两位妇女约一米半，在画面右侧（横向约 64%–84%），侧身朝着画左，四分之三侧脸对镜头；
-画左前景是西墙石凳上那位妇女和她的同伴（离镜头比 Riley 还近），脸朝 Riley、也是四分之三侧脸对镜头；
+画左前景是西墙石凳上那位年长的妇女（最靠画左，离镜头比 Riley 还近）和她的同伴（在她右边，和 Riley 差不多远），脸朝 Riley、也是四分之三侧脸对镜头；
 厅尽头冒蒸汽的门洞在画面深处、正中偏左；
```


### s8_st4

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st4/planning/st4_first_frame.png`）
- **I20** [严重·implemented·待复核] 台词（时长与逻辑）·D6 听得清：D6 听得清 最终 1 分：环境声不盖过台词；悄悄话、远处的话能听清；prompt.txt 第 2 行与末行声音模板无「对白压过环境声」；s8_st1 合唱、s
  - 方案：编译器 v14：有台词的镜头声音行加「对白优先：有人说话时环境声和动作声压低到对白下面，每句台词清楚可辨」（ep01 共 82 处）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I58** [待核实·planned·待复核] 连续性·K3 发梢干湿观感；R·I22：K3 发梢干湿观感；R·I22：st5／st9 FF 头顶仍有体积，但胸前与肩后下半长发较细束、较暗，湿绺感比 st4 大；st6 与出门 st7 又较松。已有
  - 方案：同倍率并排核 s8_st4→st5/st9/st6→st7 的发梢干湿；出片后查 st6→st7
- **I92** [记录·planned·待复核] 人物逻辑·C2 · 目的与动作脱节：C2 · 目的与动作脱节：st3 spec「动作」写了更衣厅有放衣物的壁龛，七个妇女都裹浴袍；Riley 只「侧过身先看画左、再看画右，有点不知所措」，st8 
  - 方案：s8_st8 扇领口前加半秒：瞄一眼壁龛和妇女的裹身长衣，再低头看自己的衣服、抿嘴，然后转身进门洞（未做）
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-10
+18
```

- 分镜「动作」改了：

```diff
@@ -5,3 +5,3 @@
 她的波浪长发是干的、蓬松的，从头顶到发梢都是干的，只有鬓角几缕被汗打湿贴在脸边。
-她深吸一口热气、眯起眼，左手抹一把额头的汗，又热又尴尬地对镜头说话，说到穿着全套衣服时低头扫一眼自己的衬衫；
+她深吸一口热气、眯起眼，左手抹一把额头的汗，又热又尴尬地对镜头说话，说到 all of my clothes 时低头扫一眼自己的衬衫，说到 Why did I keep my clothes on 时无奈地摇摇头；
 最后用左手当扇子在脸边猛扇，自己笑出来。
```

- 分镜「节拍」改了：

```diff
@@ -4,3 +4,4 @@
 1.5–2.5秒 她用左手抹一把额头的汗，看看湿了的手，皱眉，这一拍不说话；
-2.5–7.5秒 她又热又尴尬地对镜头说那三句，说到 fully dressed 时低头扫一眼自己的衬衫（2.6–7.3 秒）；
-7.5–10秒 她用左手当扇子在脸边猛扇几下，自己笑出声，不说话
+2.5–15.2秒 她又热又尴尬地对镜头说那几句（2.6–15.0 秒）：2.6–6.4 秒 Oh my god, it is so hot in here.，6.8–10.4 秒 And I'm wearing, like, all of my clothes.（说到 all of my clothes 时低头扫一眼自己的衬衫，再抬眼看镜头），10.8–13.6 秒 Why did I keep my clothes on?
+（无奈地摇摇头），14.1–15.0 秒 Rookie mistake.；
+15.2–18秒 她用左手当扇子在脸边猛扇几下，自己笑出声，不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1,2 @@
-Riley（又热又尴尬、自嘲，美式英语）：It's SO hot in here. And I'm fully dressed. Rookie mistake.
+Riley（又热又尴尬、自嘲，美式英语）：Oh my god, it is so hot in here. And I'm wearing, like, all of my clothes. Why did I keep my clothes on?
+Rookie mistake.
```


### s8_st5

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st5/planning/st5_first_frame.png`）
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I34** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；人物行「画面里看不到任何相机、手机或自拍杆」，而负面词同时列了相机，手
  - 方案：c1/c6/c7 外观正文改正面写法（脖子、耳垂、手腕光着），相机类只留负面词；p1/p2/p5 卡否定句改正面写法；风格行改「眼前是真实的石头、木头、陶土、布料和活生生的人」；v13 全集重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c6_Vibia/c6_Vibia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p1_陶油灯/p1_陶油灯.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p5_油瓶/p5_油瓶.md`、`ai_videos/chuanyue_yiri/workflow.json`
- **I50** [待核实·planned·待复核] 世界物理·P2 道具尺寸 / 形态守恒：P2 道具尺寸 / 形态守恒：已放大三图。st6 首帧凳面下部 x≈697–826、y≈598–645 的刮板，投影总长约 130 px；旁边油瓶约 100 p
  - 方案：出片后按 p4 实际尺寸和两镜机位核 s8_st6 凳上刮板的投影；透视解释得通就关闭，不然局部修 st6
- **I58** [待核实·planned·待复核] 连续性·K3 发梢干湿观感；R·I22：K3 发梢干湿观感；R·I22：st5／st9 FF 头顶仍有体积，但胸前与肩后下半长发较细束、较暗，湿绺感比 st4 大；st6 与出门 st7 又较松。已有
  - 方案：同倍率并排核 s8_st4→st5/st9/st6→st7 的发梢干湿；出片后查 st6→st7
- **I68** [记录·implemented·待复核] 世界物理·P3 交接三段（递的人怎么握）：P3 交接三段（递的人怎么握）：st9 首帧里 Riley 右手握着木柄。文字写「把木柄那头递向 Helvia」，没写她要先换手去握刚刮过油泥的铜勺。st5 里
  - 方案：s8_st9 写成左手捏铜勺背面、右手松开、Helvia 握木柄接过；s8_st5 写 Helvia 捏铜勺背面拿起，木柄递向 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I71** [记录·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒：放大图 s8st5_helvia_arm.png：刮板的铜勺贴在 Helvia 左上臂靠手肘上方，左小臂垂着、手搭在膝上；spec 
  - 方案：s8_st5 第 0 秒改「正刮到肘弯上方」，贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I83** [记录·implemented·待复核] 人物逻辑·C4（I79 未改）：C4（I79 未改）：Helvia 没有任何目光扫向 Riley 的湿衬衫、工装裤和靴子；厅里的妇女（s8_st3、st8）都看了，邻座人偏偏全程不看
  - 方案：s8_st5 Helvia 先扫一眼 Riley 汗湿的衬衫和工装裤，嘴角一抽，再抬下巴
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I90** [记录·implemented·待复核] 人物逻辑·C4 / R · 反应修订未同步：C4 / R · 反应修订未同步：overhead.toml:52 及 overhead 图右栏已经有“目光先扫过她汗湿的衬衫和工装裤，嘴角一抽”；本单 spe
  - 方案：s8_st5 扫衣服的那一眼同步进分镜和送模 prompt，资料包已 sync
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I116** [记录·wontfix·待复核] Prompt 文本·T7·长度与重点：T7·长度与重点：s5_st14 15 秒里 Asellina 8 步以上操作；s8_st2 15 秒数 7 枚钱再付再收；s6_st1/2/3 长达 4471
  - 方案：保留 s5_st14 擦台面、点水两拍和 s8_st2 数钱；固定负面词已去重
- **I117** [记录·implemented·待复核] Prompt 文本·T7 长度与重点／I35去重尾项：T7 长度与重点／I35去重尾项：最长 s6_st1 P为4471字符，未超过5000字；正文“画面”前有2067字符。P负面词里“画面文字、字幕、水印、log
  - 方案：剧级负面词删掉与编译器 BASE_NEGATIVES 重复的「画面文字、字幕、水印、logo、背景音乐」，v13 重编后每份只出现一次；c5 卡的生产备注删掉
  - 改了：`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-热水室西墙下的石凳上，Riley 和邻座的妇女 Helvia（人物卡 c7，外观照人物卡：深褐夹几缕灰白的头发在头顶后方盘成圆髻、插一根素面骨簪，米白厚亚麻浴袍从双肩裹到小腿中部、半袖垂到肘部、腰间系同色亚麻带，脚上一双深棕色皮带凉鞋）并排坐着，两人这一镜从头坐到尾；
+热水室西墙下的石凳上，Riley 和邻座的妇女 Helvia（人物卡 c7，外观照人物卡：深褐夹几缕灰白的头发在头顶后方盘成圆髻、插一根素面骨簪，米白粗亚麻裹身长衣从双肩裹到小腿中部、半袖垂到肘部、腰间系同色亚麻带，脚上一双深棕色皮带凉鞋）并排坐着，两人这一镜从头坐到尾；
 Helvia 本镜不说话、不看镜头，鬓角几缕汗湿。
@@ -5,6 +5,6 @@
 Riley 脸上带着汗光，头发是干的、蓬松，只有鬓角几缕被汗打湿贴在脸边，衬衫肩头微湿。
-第 0 秒：Helvia 右手握着青铜刮板（p4）的木柄，用勺形的钝头贴着自己左小臂外侧，从靠手的那头往手肘刮，刮下一道油亮的油泥；
+第 0 秒：Helvia 右手握着青铜刮板（p4）的木柄，用勺形的钝头贴着自己左臂，正刮到肘弯上方，刮下一道油亮的油泥；
 小油瓶（p5）瓶口塞着软木塞，立在两人之间的石凳上；
 Riley 双手搁在膝上，侧身好奇地盯着看。
-Helvia 发现她在看，笑了一下，朝她抬抬下巴。
+Helvia 发现她在看，目光先扫过她汗湿的衬衫和工装裤，嘴角一抽，笑了一下，朝她抬抬下巴。
 Riley 把左小臂伸到两人中间（她的衬衫是短袖，小臂本来就露着）；
@@ -12,3 +12,3 @@
 Riley 用右手掌把油在小臂上抹开；
-Helvia 从膝上拿起刮板，把木柄那头递向 Riley，Riley 右手握住木柄接过来。
+Helvia 用手指捏着铜勺的背面从膝上拿起刮板，把木柄那头递向 Riley，Riley 右手握住木柄接过来。
 道具：小油瓶进场、出场都塞着塞子立在两人之间的石凳上，只在 5–10 秒被拿起来拔塞、滴油、塞回；
```

- 分镜「节拍」改了：

```diff
@@ -1,3 +1,3 @@
 0–2.5秒 第 0 秒：两人并排坐在西墙石凳上，Riley 在画左、Helvia 在画右；
-Helvia 右手握着青铜刮板，勺形的钝头贴着自己左小臂外侧，从靠手的那头往手肘刮，刮下一道油泥，在刮板上抖掉；
+Helvia 右手握着青铜刮板，勺形的钝头贴着自己左臂，正刮到肘弯上方，刮下一道油泥，在刮板上抖掉；
 塞着软木塞的小油瓶立在两人之间的石凳上；
@@ -6,3 +6,3 @@
 这一拍不说话；
-2.5–3.5秒 Helvia 发现 Riley 在看，转头看她，笑了一下，朝她抬抬下巴（Helvia 的反应拍，单独一拍）；
+2.5–3.5秒 Helvia 发现 Riley 在看，转头看她，目光先扫过她汗湿的衬衫和工装裤，嘴角一抽，笑了一下，朝她抬抬下巴（Helvia 的反应拍，单独一拍）；
 3.5–5秒 Riley 把左小臂伸到两人中间；
@@ -13,3 +13,3 @@
 10–11.5秒 Riley 用右手掌把油在左小臂上抹开，小臂变得油亮；
-11.5–13秒 Helvia 从膝上拿起刮板，把木柄那头递向 Riley；
+11.5–13秒 Helvia 用手指捏着铜勺的背面从膝上拿起刮板，把木柄那头递向 Riley；
 Riley 右手握住木柄接过来，Helvia 松手；
```


### s8_st9

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st9/planning/st9_first_frame.png`）
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I50** [待核实·planned·待复核] 世界物理·P2 道具尺寸 / 形态守恒：P2 道具尺寸 / 形态守恒：已放大三图。st6 首帧凳面下部 x≈697–826、y≈598–645 的刮板，投影总长约 130 px；旁边油瓶约 100 p
  - 方案：出片后按 p4 实际尺寸和两镜机位核 s8_st6 凳上刮板的投影；透视解释得通就关闭，不然局部修 st6
- **I58** [待核实·planned·待复核] 连续性·K3 发梢干湿观感；R·I22：K3 发梢干湿观感；R·I22：st5／st9 FF 头顶仍有体积，但胸前与肩后下半长发较细束、较暗，湿绺感比 st4 大；st6 与出门 st7 又较松。已有
  - 方案：同倍率并排核 s8_st4→st5/st9/st6→st7 的发梢干湿；出片后查 st6→st7
- **I68** [记录·implemented·待复核] 世界物理·P3 交接三段（递的人怎么握）：P3 交接三段（递的人怎么握）：st9 首帧里 Riley 右手握着木柄。文字写「把木柄那头递向 Helvia」，没写她要先换手去握刚刮过油泥的铜勺。st5 里
  - 方案：s8_st9 写成左手捏铜勺背面、右手松开、Helvia 握木柄接过；s8_st5 写 Helvia 捏铜勺背面拿起，木柄递向 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I98** [记录·planned·待复核] 连续性·连续性·K3：连续性·K3：s6_st2_shirt.jpg：Riley 衬衫前襟、袖子满是凸起的波纹、方格提花图案，看起来像另一件有花纹的衬衫；同场 s6_st5 首帧（s
  - 方案：s6_st2 首帧局部修回素面米白亚麻，ffp 加「素面无花纹亚麻」、负面词加「提花、压纹图案」；s8_st6/st9 视情况处理（未做）
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-13
+21
```

- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-接上一镜，两人仍并排坐在石凳上：邻座的妇女 Helvia（人物卡 c7，外观照人物卡：深褐夹几缕灰白的头发在头顶后方盘成圆髻、插一根素面骨簪，米白厚亚麻浴袍从双肩裹到小腿中部、半袖垂到肘部、腰间系同色亚麻带，脚上一双深棕色皮带凉鞋）在画右边缘，本镜不说话、不看镜头。
+热水室西墙下的石凳上，两人并排坐着：邻座的妇女 Helvia（人物卡 c7，外观照人物卡：深褐夹几缕灰白的头发在头顶后方盘成圆髻、插一根素面骨簪，米白粗亚麻裹身长衣从双肩裹到小腿中部、半袖垂到肘部、腰间系同色亚麻带，脚上一双深棕色皮带凉鞋）在画右边缘，本镜不说话、不看镜头。
 画面里共两个人：Riley 和画右边缘的 Helvia。
@@ -6,5 +6,6 @@
 她抹了油的左小臂油亮，搁在左膝上。
-她把左小臂伸到身前，把刮板勺形的钝头搭在小臂外侧靠手的那头，顺着小臂往手肘慢慢刮了一下，钝头边上挂起一道油泥；
-她瞪大眼睛看看刮板，再看看小臂上刮出的一道干净皮肤，转向镜头说话；
-说完把刮板的木柄那头递向 Helvia，Helvia 右手接住，放回两人之间的石凳上、小油瓶旁边；
+她抬眼转向镜头开始说话：说到 rub oil all over yourself 时把油亮的左小臂抬起来给镜头看，说到 with this thing 时右手把刮板举到脸边晃一晃；
+然后她低头把左小臂伸到身前，把刮板勺形的钝头搭在小臂外侧靠手的那头，顺着小臂往手肘慢慢刮了一下，钝头边上挂起一道油泥；
+说到 look 时她低头看小臂上刮出的一道干净皮肤，把小臂侧过来朝镜头，瞪大眼睛接着说完；
+说完左手捏住铜勺的背面、右手松开木柄，把木柄那头朝 Helvia 递过去，Helvia 右手握住木柄接过，放回两人之间的石凳上、小油瓶旁边；
 Riley 搓了搓油亮的小臂，冲她一笑。
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-同上一镜的座位：Riley 在画面中间偏左，Helvia 在画右边缘、只入画半身；
+两人坐在西墙石凳上、面朝屋子中间：Riley 在画面中间偏左，Helvia 在画右边缘、只入画半身；
 石凳上从画左到画右依次是：Riley、挨着她左胯的面包布包、小油瓶、Helvia；
@@ -4,3 +4,3 @@
 镜头更近，坐姿高度，斜对 Riley；
-Riley 端详刮板、刮小臂时低头看手，说台词时脸转向镜头，还刮板时转向画右。
+Riley 端详刮板（0–1.2 秒）、刮小臂（10.2–12.7 秒）时低头看手，说台词时脸转向镜头，还刮板时转向画右。
 配角一行：Helvia——看着 Riley，心想「刮一下就这么惊奇」，憋着笑。
```

- 分镜「节拍」改了：

```diff
@@ -1,2 +1,2 @@
-0–1秒 第 0 秒：Riley 坐在石凳上，右手握着青铜刮板的木柄，勺形那头朝上，笑着低头端详；
+0–1.5秒 第 0 秒：Riley 坐在石凳上，右手握着青铜刮板的木柄，勺形那头朝上，笑着低头端详；
 油亮的左小臂搁在左膝上；
@@ -4,9 +4,12 @@
 塞着塞子的小油瓶立在两人之间的石凳上，布包挨着 Riley 的左胯；
+1.2 秒她抬眼转向镜头；
 这一拍不说话；
-1–2.5秒 Riley 把左小臂伸到身前，把刮板勺形的钝头搭在小臂外侧靠手的那头；
-2.5–4秒 她顺着小臂往手肘慢慢刮一下，钝头边上挂起一道油泥，这一拍不说话；
-4–5秒 她瞪大眼睛看看刮板，再看看小臂上刮出的一道干净皮肤，转向镜头（Riley 的反应拍，单独一拍）；
-5–9.7秒 她对镜头说那句话，oil up 后面停半拍（5.1–9.6 秒）；
-9.7–11.5秒 她把刮板的木柄那头递向画右的 Helvia；
-Helvia 右手接住，放回两人之间的石凳上、小油瓶旁边；
-11.5–13秒 Riley 搓了搓油亮的小臂，冲 Helvia 一笑，这一拍不说话
+1.5–10.2秒 她对镜头说（1.6–10.0 秒）：1.6–3.6 秒 Okay, so there's no soap.，4.0–10.0 秒 You just rub oil all over yourself and then scrape it off with this thing —（说到 rub oil all over yourself 时把油亮的左小臂抬起来给镜头看，说到 with this thing 时右手把刮板举到脸边晃一晃）；
+10.2–12.7秒 她低头把左小臂伸到身前，把刮板勺形的钝头搭在小臂外侧靠手的那头，顺着小臂往手肘慢慢刮一下，钝头边上挂起一道油泥，这一拍不说话；
+12.7–15.2秒 她说 and look, it actually works!
+（12.8–15.0 秒）——说到 look 时低头看小臂上刮出的一道干净皮肤，把小臂侧过来朝镜头，再瞪大眼睛抬头看镜头；
+15.2–18.2秒 她对镜头说 Gross.（15.4–16.0 秒），先皱一下鼻子，再咧嘴笑着说 Kind of love it, though.（16.4–18.0 秒）；
+18.2–19.8秒 她左手捏住铜勺的背面、右手松开木柄，把木柄那头递向画右的 Helvia；
+Helvia 右手握住木柄接过，放回两人之间的石凳上、小油瓶旁边；
+不说话；
+19.8–21秒 Riley 搓了搓油亮的小臂，冲 Helvia 一笑，这一拍不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1,2 @@
-Riley（惊奇，美式英语）：No soap. You just oil up… and scrape it all off.
+Riley（惊奇，美式英语）：Okay, so there's no soap. You just rub oil all over yourself and then scrape it off with this thing — and look, it actually works!
+Gross. Kind of love it, though.
```


### s8_st6

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st6/planning/st6_first_frame.png`）
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I24** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；overhead Vibia 离镜头 3.5 m（在 Ri
  - 方案：s2_st8 文字与 overhead 改成 Vibia 在 Riley 身后约一米（贴首帧）；s2_st4 起点与擦肩提前到 0–1.5 s；s2_st1 机位改为垫脚石南约 2.5 m、离地 0.5 m；s8_st8 两位妇女站位对调贴首帧；s3_st6 机位推到 (5.8,6.0)、标中近景
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st6/planning/overhead.toml`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I45** [主要·implemented·待复核] 台词（时长与逻辑）·D2 节拍对位：D2 节拍对位 最终 1 分：台词和动作节拍对得上（说到哪句做哪个动作）；总述「她说话时 Felix 抬眼」与节拍「她说完后 13–14.5 s 才抬眼」相抵（
  - 方案：s3_st4 总述改「她说完后 Felix 才抬眼」；s8_st6 拉丁语拆成两句分别落点，说到 versas 时翻手
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I50** [待核实·planned·待复核] 世界物理·P2 道具尺寸 / 形态守恒：P2 道具尺寸 / 形态守恒：已放大三图。st6 首帧凳面下部 x≈697–826、y≈598–645 的刮板，投影总长约 130 px；旁边油瓶约 100 p
  - 方案：出片后按 p4 实际尺寸和两镜机位核 s8_st6 凳上刮板的投影；透视解释得通就关闭，不然局部修 st6
- **I58** [待核实·planned·待复核] 连续性·K3 发梢干湿观感；R·I22：K3 发梢干湿观感；R·I22：st5／st9 FF 头顶仍有体积，但胸前与肩后下半长发较细束、较暗，湿绺感比 st4 大；st6 与出门 st7 又较松。已有
  - 方案：同倍率并排核 s8_st4→st5/st9/st6→st7 的发梢干湿；出片后查 st6→st7
- **I59** [待核实·wontfix·待复核] 台词（时长与逻辑）·D3·出处：D3·出处：「Dies nihil est. Dum versas te, nox fit.」不是已知的庞贝涂鸦，疑似自拟；Riley 译成「get movin
  - 方案：保留台词，出处照 r05 #21 标注
- **I98** [记录·planned·待复核] 连续性·连续性·K3：连续性·K3：s6_st2_shirt.jpg：Riley 衬衫前襟、袖子满是凸起的波纹、方格提花图案，看起来像另一件有花纹的衬衫；同场 s6_st5 首帧（s
  - 方案：s6_st2 首帧局部修回素面米白亚麻，ffp 加「素面无花纹亚麻」、负面词加「提花、压纹图案」；s8_st6/st9 视情况处理（未做）
- **I103** [记录·implemented·待复核] 台词（时长与逻辑）·D3·注音来源未同步；R I46：D3·注音来源未同步；R I46：r05_衣着语言黑名单.md:142 仍写 doom；:148 仍写 EH-oo-geh，未明确 eu 一音节。当前 Helv
  - 方案：r05 #21 改「dum（短 u，不读 doom）」；#27 改 EW-geh，注明 eu 合成一个音节、共两音节、/ˈeu̯.ɡe/
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-15
+19
```

- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-两人仍并排坐在石凳上，这一镜从头坐到尾：邻座的妇女 Helvia（人物卡 c7，外观照人物卡：深褐夹几缕灰白的头发在头顶后方盘成圆髻、插一根素面骨簪，米白厚亚麻浴袍从双肩裹到小腿中部、半袖垂到肘部、腰间系同色亚麻带，脚上一双深棕色皮带凉鞋）在画右，鬓角几缕汗湿；
+两人仍并排坐在石凳上，这一镜从头坐到尾：邻座的妇女 Helvia（人物卡 c7，外观照人物卡：深褐夹几缕灰白的头发在头顶后方盘成圆髻、插一根素面骨簪，米白粗亚麻裹身长衣从双肩裹到小腿中部、半袖垂到肘部、腰间系同色亚麻带，脚上一双深棕色皮带凉鞋）在画右，鬓角几缕汗湿；
 她的声音：中年女声，略低、带笑，语速从容。
@@ -6,3 +6,3 @@
 Riley 往后靠在湿热的墙上，闭着眼舒服地长叹一口气，然后看着妇女懒洋洋地说她能在这儿待一整天；
-Helvia 听不懂英语，但看她往后一靠、闭眼长叹的样子，就明白她是赖着不想走，耸耸肩，笑着用拉丁语回了一句，说到第二句时手在空中一翻（手心朝下翻成朝上），像在说「一转身」。
+Helvia 听不懂英语，但看她往后一靠、闭眼长叹的样子，就明白她是赖着不想走，耸耸肩，笑着用拉丁语回了一句，说到 versas 时手在空中一翻（手心朝下翻成朝上），像在说「一转身」。
 Riley 眨眨眼，想了想，转向镜头说出她的理解，自己先笑了，坐直身子，双手拍一下膝盖。
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-同前两镜的座位，镜头稍远：Riley 在画左、妇女在画右，两人坐着，腰以上；
+两人坐在西墙石凳上、面朝屋子中间，镜头在两人前方斜对、离两人两米多：Riley 在画左、妇女在画右，两人坐着，腰以上；
 石凳上从画左到画右依次是：Riley、挨着她左胯的面包布包、小油瓶、Helvia，刮板平放在小油瓶旁边；
```

- 分镜「节拍」改了：

```diff
@@ -6,5 +6,6 @@
 4.4–5.1秒 Helvia看着她耸耸肩，笑了（Helvia的反应拍，单独一拍），这一拍不说话；
-5.1–9秒 Helvia笑着看着 Riley，用拉丁语说那两句，说到第二句时手在空中一翻（5.1–8.8 秒），只有她张嘴；
+5.1–9秒 Helvia 笑着看着 Riley，用拉丁语说那两句：5.1–6.3 秒说第一句，停半拍，6.8–8.8 秒说第二句，说到 versas 时手在空中一翻（手心朝下翻成朝上）；
+只有她张嘴；
 9–10秒 Riley 眨眨眼，想了想，嘴角慢慢翘起来，转向镜头（Riley 的反应拍，单独一拍），这一拍不说话；
-10–13秒 她对镜头说出她的理解（10.1–12.8 秒）；
-13–15秒 她自己笑出声，坐直身子，双手拍一下膝盖，还坐着，不说话
+10–17秒 她对镜头说出她的理解（10.1–16.9 秒）：10.1–13.4 秒 I have no idea what she just said,（说这半句时朝画右的 Helvia 偏一下头），停半拍，13.8–16.9 秒 but I'm pretty sure it was "get moving."；
+17–19秒 她自己笑出声，坐直身子，双手拍一下膝盖，还坐着，不说话
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1,2 @@
 Riley（放松，美式英语）：I could stay here all day. / Helvia（拉丁语，中年女声、略低、带笑、语速从容，笑着耸肩，古典读法 DEE-es NIH-hil est. dum WER-sahs teh, noks fit；
-dum 的 u 是短元音 /dʊm/，短促一拍）：Dies nihil est. Dum versas te, nox fit. / Riley（对镜头，美式英语）：I'm pretty sure that means "get moving."
+dum 的 u 是短元音 /dʊm/，短促一拍）：Dies nihil est. Dum versas te, nox fit. / Riley（对镜头，美式英语）：I have no idea what she just said, but I'm pretty sure it was "get moving."
```


### s8_st7

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame.png`）
- **I2** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；spec 动作行和走位行、prompt「画面」「走位」「动作」三行、over
  - 方案：s4_st3 统一为从她左后方（街南侧、画右）擦过，toml 补南侧墙与菜筐；s8_st7 Riley 走下路缘石停在街边、老汉走街面；s8_st10 出画路线东移、离镜头≥0.9 m；overhead 闸门 0 blocker
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st10/planning/overhead.toml`
- **I25** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35
  - 方案：s8_st7 overhead 机位改到门洞西北 (5,8) 朝东南 (12,13)，老汉路线和 Riley 出画方向同步，ffp 同步；s2_st1/st4/st8 机位按首帧改
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I26** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；overhead 机位 (5,16)、h 0.9、看 (12,12)、35mm，柱廊
  - 方案：s8_st7、s8_st8、s2_st8 画面位置按首帧同步文字与 overhead；s8_st10 出画路线东移
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I27** [严重·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数 最终 1 分：动作节拍的秒数排得下（走多远、几秒到），没有挤压；overhead Riley (13.6,20.6) 离镜头 3.4 m、Vib
  - 方案：s2_st4 擦肩提前到 0–1.5 s、老人挪到西人行道；s8_st3 起点前移 0.6 m；s8_st7 老汉路线重排、约 6.5 s 出画右；s3_st1 第 0 秒改为已站定；v7 各镜节拍按新镜长重排，overhead 闸门 63 镜 0 blocker 0 warning
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`
- **I58** [待核实·planned·待复核] 连续性·K3 发梢干湿观感；R·I22：K3 发梢干湿观感；R·I22：st5／st9 FF 头顶仍有体积，但胸前与肩后下半长发较细束、较暗，湿绺感比 st4 大；st6 与出门 st7 又较松。已有
  - 方案：同倍率并排核 s8_st4→st5/st9/st6→st7 的发梢干湿；出片后查 st6→st7
- **I72** [记录·planned·待复核] 世界物理·流程（审稿后改动未复核）：流程（审稿后改动未复核）：这四镜的 overhead.toml 在审稿后（19:38–19:41）被改过，资料包标了 `_失效.md`；两位审稿人和本裁决看的都
  - 方案：这四镜在 r3/v7 修改后已重出 overhead、v13 重编、shot_pack sync 63/63 ok；新版走位进下一轮审查复核
- **I87** [记录·implemented·待复核] 人物逻辑·C6：C6：「胳膊肘碰同伴」出现在 s4_st1 6.8 秒和 s8_st3 4–5.5 秒；「看长发」出现在 s2_st4、s8_st2、s8_st7 三处；当地人
  - 方案：s4_st1 去掉胳膊肘碰同伴（改成互看一眼、咧嘴笑）；s8_st3 改成对视、用下巴一指；s8_st7 老汉改看短靴和布包
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I91** [记录·implemented·待复核] 人物逻辑·C3 / C6 / R · 老汉注意对象不一致：C3 / C6 / R · 老汉注意对象不一致：spec「动作」「节拍」「配角一行」及根 prompt 让老汉看蓬松长发、想“头发真多”；overhead.to
  - 方案：s8_st7 老汉统一为看短靴和布包，分镜、ffp、toml 同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/st7_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st7/planning/overhead.toml`
- 分镜「动作」改了：

```diff
@@ -4,6 +4,6 @@
 六十来岁，灰白短发、脸刮得干净，褐色及膝粗布短 tunica，赤褐色皮凉鞋）。
-Riley 从门洞里走出来，走三四步穿过柱廊，站进明亮的午后阳光里，停在柱廊外的路边；
+Riley 从门洞里走出来，走三四步穿过柱廊、走下路缘石，站进明亮的午后阳光里，停在柱廊外的街边；
 她的波浪长发是干的、蓬松，只有鬓角几缕还带着汗湿；
 衬衫被汗贴在背上，她揪着衬衫前襟抖了抖，仰头深深吸了一口气，笑了。
-拎水罐的老汉从画左沿着路沿下的石板街面走来，比 Riley 离镜头近得多，从她和镜头之间走过，目光在她蓬松的乌黑长发上停了一下，接着朝画右赶路。
+拎水罐的老汉从画左边缘沿石板街面走来，比 Riley 离镜头近得多，从她和镜头之间走过，目光在她的系带短靴和腰上的布包上停了一下，接着朝画右远处赶路。
 Riley 朝画右的街望了望，迈步朝画右走出画。
```

- 分镜「走位」改了：

```diff
@@ -1,5 +1,5 @@
-镜头在街对面（西侧人行道）、略低于腰，斜对浴场门口：门洞在画面中间略偏右。
-Riley 从门洞走出来，0–2 秒走三四步（约两米七）穿过柱廊，停在柱廊外的路边，画面正中；
-拎水罐的老汉走在路沿下面的石板街面上（Riley 站在路沿上的人行道边），第 0 秒在画左边缘、离镜头约六米，每秒走不到一米，3–5 秒从 Riley 和镜头之间走过（离镜头约四米，比 Riley 近两米，画面里他的脚比 Riley 的脚低一截），7 秒走出画右；
-最后 Riley 7–10 秒朝画右（往南）走出画。
-配角一行：拎水罐的老汉——赶着回家，路过时看见她头发披散着从女浴场出来，心想「这姑娘头发真多」，看一眼就接着走。
+镜头在街西侧、浴场门口的西北边，略低于腰，朝东南斜对浴场门口：柱廊从画左近处往画右远处去，门洞在画面左半（横向约三成多）。
+Riley 从门洞走出来，0–2 秒走三四步（约两米七）穿过柱廊、走下路缘石，停在柱廊外的街边，画面中间偏右；
+拎水罐的老汉走在石板街面上，第 0 秒在画左边缘、离镜头约三四米，每秒走不到一米，2.5–4.5 秒从 Riley 和镜头之间走过（比 Riley 离镜头近），约 6.5 秒走出画右；
+最后 Riley 7–10 秒朝画右（往南）沿街走远、走出画。
+配角一行：拎水罐的老汉——赶着回家，路过时看见一个穿裤子的外地女人从女浴场出来，目光在她的短靴和布包上停了一下，心想「这是哪来的」，接着走。
```

- 分镜「节拍」改了：

```diff
@@ -1,8 +1,8 @@
 0–2秒 第 0 秒：Riley 刚从柱廊下昏暗的门洞里迈出一步，全身入画，微微眯眼，双手空着，布包挂在左胯；
-画左边缘、离镜头约六米，一个拎着两只小陶水罐的瘦老汉沿着路沿下的街面慢慢走来；
+画左边缘、离镜头约三四米，一个拎着两只小陶水罐的瘦老汉沿着石板街面慢慢走来；
 画面里共两个人；
 这一拍不说话；
-Riley 走三四步穿过柱廊，停在柱廊外路边的阳光里；
+Riley 走三四步穿过柱廊、走下路缘石，停在柱廊外街边的阳光里；
 2–3秒 她揪着衬衫前襟抖了抖，仰头深深吸一口气，笑了；
-3–5秒 拎水罐的老汉在路沿下的街面上从她和镜头之间走过，目光在她蓬松的乌黑长发上停了一下，接着朝画右赶路（路人的反应拍，单独一拍）；
+3–5秒 拎水罐的老汉在街面上从她和镜头之间走过，目光在她的短靴和布包上停了一下，接着朝画右远处赶路，约 6.5 秒走出画右（路人的反应拍，单独一拍）；
 5–7秒 Riley 朝画右的街望了望，舔舔嘴唇，一副饿了的样子，不说话；
```

- 分镜「镜头」改了：

```diff
@@ -1,3 +1,3 @@
 他拍：固定机位旁观拍摄，略低于腰的机位平视；
-全景：她全身入画，和身后柱廊下的门洞同框；
+全景：柱廊从画左近处往画右远处去，她全身入画，和身后柱廊下的门洞同框；
 街道尽头被房屋挡住。
```


### s8 整场 / 未指明镜头

- **I106** [记录·implemented·待复核] 母语听感·N4 口癖/节奏：N4 口癖/节奏：省略号拖音 8 镜以上；basically 仍有 s8_st1、s5_st5（I97 未改）
  - 方案：v7 全部台词按新听感标准重写，s8_st1 去掉 basically

### s8 整场 / 未指明镜头

- **I112** [记录·planned·待复核] 时代与世界观·E6·出处：E6·出处：卡里把 Petronius Sat. 41 说成「浴场闲聊」；该句出自 Trimalchio 宴会场景
  - 方案：c7 卡与 r05 #21 的出处改成 Petronius Sat. 41（宴席闲谈），台词不动；未做

## s5

### s5_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st1/planning/st1_first_frame.png`）
- **I4** [严重·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；`s6st3_cart.png`：驴站在货车左侧，后蹄和车尾轮在同一深
  - 方案：s6_st3 首帧局部修：驴在两根车辕之间、车箱正前方；s5_st13 首帧去掉悬空白汽；s5_st4 文字贴首帧（第 0 秒罐口已淌一缕，一两秒后扶正）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame_prompt.txt`
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I31** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；放大看（`work/framing_B__a/s5_st8_donkey.jpg`）
  - 方案：s5_st8 首帧修成车尾朝镜头、往街深处走；s5_st6、s6_st1 overhead 照首帧改；s7_st5 overhead 机位升到约 6 m、路人放到约 43 m 外，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/overhead.toml`
- **I64** [待核实·implemented·待复核] 时代与世界观·E6·推定史实的确定性（上一轮 I108、I67 未改）、R：E6·推定史实的确定性（上一轮 I108、I67 未改）、R：「at two, everybody hits the baths」、「Dinner here i
  - 方案：v7 改成不那么绝对的说法：s5_st1「people eat dinner here at, like, three-thirty」、s8_st1「Apparently they do their afternoon thing right around two」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I105** [记录·implemented·待复核] 母语听感·N1 语序：N1 语序：L64 "Dinner here is at three-thirty." 偏书面（I96 未改）
  - 方案：v7 s5_st1 改「…people eat dinner here at, like, three-thirty.」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I108** [记录·implemented·待复核] 时代与世界观·E6 史实一致（R：I108）：E6 史实一致（R：I108）：「basically Pompeii's two o'clock alarm. And at two, everybody hi
  - 方案：同 I64：v7 改成带 like / apparently / right around 的说法，不再是全称断言
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-9
+17
```

- 分镜「动作」改了：

```diff
@@ -4,3 +4,3 @@
 衬衫已经不贴身了。
-她用左手把一缕头发拨到肩后，对着镜头又饿又好笑地说话，说到 three-thirty 时挑眉；
+她用左手把一缕头发拨到肩后，对着镜头又饿又好笑地说话，说到 Ish 时左手在脸边晃一晃（「差不多吧」），说到 three-thirty 时挑眉；
 说完放慢脚步，越过镜头朝前方望一眼（前面街角是熟食铺）。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
 Riley 沿街朝东走，面对镜头；
-镜头在她伸直的右臂末端、在她前方一臂远，跟着她一起往前移（每秒不到一米）；
+镜头在她伸直的右臂末端、在她前方一臂远，跟着她一起往前移（边说边慢慢走，每秒约半米）；
 她身后是来时的街（西边）。
```

- 分镜「节拍」改了：

```diff
@@ -3,3 +3,3 @@
 这一拍不说话；
-1.5–6.5秒 她边走边对镜头说那几句，说到 three-thirty 时挑眉（1.6–6.3 秒）；
-6.5–9秒 她放慢脚步，越过镜头朝前方望一眼，舔舔嘴唇，不说话
+1.5–14.6秒 她边走边对镜头说那几句（1.6–14.4 秒）：1.6–2.8 秒 Okay, I'm clean.，3.2–3.6 秒 Ish.（左手在脸边晃一晃），4.0–5.6 秒 And I am starving —，6.0–10.4 秒 which, good news, people eat dinner here at, like, three-thirty.（说到 three-thirty 时挑眉），10.8–12.8 秒 So it's basically dinner time.，13.2–14.4 秒 Which is wild.；
+14.6–17秒 她放慢脚步，越过镜头朝前方望一眼，舔舔嘴唇，不说话
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1 @@
-Riley（又饿又好笑，美式英语）：Clean-ish. And starving. Good news?
-Dinner here is at three-thirty.
+Riley（又饿又好笑，美式英语）：Okay, I'm clean. Ish. And I am starving — which, good news, people eat dinner here at, like, three-thirty. So it's basically dinner time. Which is wild.
```


### s5_st8

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/_r3_before/st8_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame.png`（现行）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I5** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；`work/physics_C__a/s5st8_cart.png`：驴脸正
  - 方案：s5_st8、s6_st3 首帧局部修正驴车结构与朝向；s6_st6 不改图，文字与 overhead 照首帧（楼梯画左、马厩画右），toml note 记下与 bg6 平面图的取舍
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st6/planning/overhead.toml`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I10** [严重·implemented·待复核] 人物逻辑·C1 知道什么：C1 知道什么 最终 1 分：每个人此刻知道什么、不知道什么，行为不越过他的认知；st8 首帧约横向 60% 的驴露正脸、鼻口朝近处，车箱在其右后方更深处；旁边
  - 方案：s5_st8 首帧修成驴、车夫、车都朝街深处走（车尾朝镜头），保留店主，接 st9 右拐的因果；负面词加「驴脸朝镜头、驴朝画面前方走」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`
- **I11** [严重·implemented·待复核] 人物逻辑·C3 视线：C3 视线 最终 1 分：每个时刻每个人看向谁，合理（不无缘无故看镜头、不无视身边的怪事）；首帧放大（work/character_B__a/s5st8_zoo
  - 方案：s5_st8 首帧修后画右铺门口店主在场；s6_st6 文字改为第 0 秒门外一步、看画右柜台（放大核对首帧确认看画右）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I12** [严重·implemented·待复核] 人物逻辑·C4 反应拍：C4 反应拍 最终 1 分：配角的反应单独占拍，不被吞掉；反应和身份、性格相符；首帧放大（work/character_B__a/s5st8_zoom2.png
  - 方案：s5_st8 店主在首帧；Asellina 三镜反应拉开：st12 抱胳膊笑、st14 低头擦台面只抬眼一瞥不笑、st7 摇头笑；s6_st5 改为满意点头、嘴角一抿
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I13** [严重·implemented·待复核] 人物逻辑·C7 动机连贯：C7 动机连贯 最终 1 分：跨镜头的情绪与动机连得上，没有突然的转变；首帧放大（work/character_B__a/s6st6_zoom.png）：Ril
  - 方案：s6_st6 文字照首帧：门外一步、看画右柜台，加触发「门里传出碗勺声和饭香」；s5_st7 远景两个男人按首帧写，不再声称是 st6 那两人；s5_st8 首帧修正
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I16** [严重·implemented·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；z_s5_st8_right.jpg：驴头和赶车人都朝着镜头走过来，spec 写的是车「直直往
  - 方案：s5_st8 首帧修成车尾朝镜头、往画右拐可读；s4_st3 改「左后方」；s6_st1 墙龛改「在她右后方（画面上在她左边）」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I19** [严重·implemented·待复核] 台词（时长与逻辑）·D5 说话人：D5 说话人 最终 1 分：每句的说话人对，画内该张嘴的人张嘴，不说话的人不出声；spec 节拍第 0 秒要求店主站在画右铺子门口，俯视图店主在 (7.8,13
  - 方案：s5_st8 首帧局部修后保留画右铺门口的店主，喊 Dextram 的人在画内；送模 prompt 标明店主说拉丁语
- **I20** [严重·implemented·待复核] 台词（时长与逻辑）·D6 听得清：D6 听得清 最终 1 分：环境声不盖过台词；悄悄话、远处的话能听清；prompt.txt 第 2 行与末行声音模板无「对白压过环境声」；s8_st1 合唱、s
  - 方案：编译器 v14：有台词的镜头声音行加「对白优先：有人说话时环境声和动作声压低到对白下面，每句台词清楚可辨」（ep01 共 82 处）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I23** [严重·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；牵驴的车夫留着修过的短须（z_s5st8_man.png）
  - 方案：c7 卡、s8 文字和 st3/st4/st5/st6/st8/st9 首帧 prompt 的「浴袍」改成「粗亚麻裹身长衣」，剧级负面词加「翻领浴袍，毛巾布浴袍」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I31** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；放大看（`work/framing_B__a/s5_st8_donkey.jpg`）
  - 方案：s5_st8 首帧修成车尾朝镜头、往街深处走；s5_st6、s6_st1 overhead 照首帧改；s7_st5 overhead 机位升到约 6 m、路人放到约 43 m 外，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/overhead.toml`
- **I32** [严重·implemented·待复核] 镜头规格·F5 画内人数：F5 画内人数 最终 1 分：写了几个人就几个人（含 extras），首帧一致；首帧只有 Riley、车夫和驴，画右没有店主，也没有挂大蒜、放藤筐的铺子。修图前
  - 方案：s5_st8 首帧局部修图保留画右铺门口店主（共三人一驴），只改驴车朝向
- **I36** [严重·implemented·待复核] Prompt 文本·T4 图文一致：T4 图文一致 最终 1 分：文字和挂的首帧、站位图、场景图一致；P13写“共三个人和一头驴”，P15第0秒店主已在画右铺门口，车夫牵驴向纵深走、4–8秒右拐。
  - 方案：s5_st8 首帧局部修：驴车朝街深处、车尾朝镜头，保留画右铺门口店主；s5_st4 文字照首帧写第 0 秒已在淌一缕鱼露、一两秒后扶正
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I51** [待核实·implemented·待复核] 世界物理·P5 运动：P5 运动：overhead 驴车 (12,10.2)→(12.9,11.9)→(13.0,13.9)，在约 1–1.5 m 半径内转 90°。驴加车全长约 3
  - 方案：s5_st8 overhead 驴车拐弯起点前移、弧线放宽，时间不变；出片后看车轮是否压墙角
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/overhead.toml`
- **I60** [待核实·planned·待复核] 台词（时长与逻辑）·D3·拉丁语惯用：D3·拉丁语惯用：单说「Dextram, dextram!」是省略式宾格，字面也可理解为「右手」；常见说法是「Ad dextram!」
  - 方案：请拉丁语顾问确认用「Dextram, dextram!」还是「Ad dextram!」；要改就把窗口放宽到 1.6–3.0 s
- 分镜「动作」改了：

```diff
@@ -6,4 +6,4 @@
 她前方几米，一个车夫（普通路人，不说话、不看镜头，但听见喊声会看向店主；
-三十来岁，粗布短 tunica，脸刮得干净）走在驴头左边牵着缰绳，一头小灰驴站在两根车辕中间、整头驴在车箱前面，拉着身后的两轮小车直直往前，眼看要直穿过街口——主街穿过十字街口继续往远处伸，看得到路口对面那一段街。
-画右那排铺面里、离镜头近一些的一家铺子（门口挂着几串大蒜、放着两只藤筐）门口站着一个中年店主（不立卡的配角：粗布 tunica 系着围裙，脸刮得干净；
+三十来岁，粗布短 tunica，脸刮得干净）背对镜头走在驴车左边、手里牵着缰绳，一头小灰驴在两根车辕中间、整头驴在车箱前面、背对镜头，拉着身后的两轮小车直直往前，眼看要直穿过街口——主街穿过十字街口继续往远处伸，看得到路口对面那一段街。
+画右那排铺面里、离镜头近一些的一家铺子（门口挂着几串大蒜、放着一只藤筐）门口站着一个中年店主（不立卡的配角：粗布 tunica 系着围裙，脸刮得干净；
 声音：中年男声，粗嗓，隔着街大喊），他冲车夫大喊「Dextram, dextram!
```

- 分镜「走位」改了：

```diff
@@ -3,3 +3,3 @@
 Riley 在画面中间偏左背对镜头走（0–3 秒慢慢走约两米），停住后头转向画右，侧脸看得到。
-车夫和驴车在画面中间往前走（每秒约一米），4–8 秒在街口往画右拐进横街、消失在墙角后面。
+车夫和驴车在画面中间偏右往前走（每秒约一米），驴和车尾都背对镜头，4–8 秒在街口往画右拐进横街、消失在墙角后面。
 配角一行：店主——看着驴车，心想「这家伙又要走过头」，喊完瞥见 Riley 盯着他，心想「这女人看我干嘛」；
```

- 分镜「节拍」改了：

```diff
@@ -2,6 +2,6 @@
 画左是熟食铺的门脸；
-她前方几米，车夫牵着小灰驴在画面中间直直往前走，驴在两根车辕中间、两轮小车在驴身后，快到十字街口；
+她前方几米，车夫背对镜头走在驴车左边、牵着缰绳，小灰驴背对镜头、在两根车辕中间，两轮小车在驴身后、车尾朝镜头，驴车在画面中间偏右直直往前走，快到十字街口；
 主街穿过路口继续往远处伸；
 画右那排铺面在远处断开，露出往右拐的横街口；
-店主站在画右一家铺子门口，看着驴车；
+店主站在画右一家挂着大蒜的铺子门口（画面横向约八成处），看着驴车；
 这一拍不说话；
```


### s5_st9

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st9/planning/st9_first_frame.png`）
- **I10** [严重·implemented·待复核] 人物逻辑·C1 知道什么：C1 知道什么 最终 1 分：每个人此刻知道什么、不知道什么，行为不越过他的认知；st8 首帧约横向 60% 的驴露正脸、鼻口朝近处，车箱在其右后方更深处；旁边
  - 方案：s5_st8 首帧修成驴、车夫、车都朝街深处走（车尾朝镜头），保留店主，接 st9 右拐的因果；负面词加「驴脸朝镜头、驴朝画面前方走」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`
- **I13** [严重·implemented·待复核] 人物逻辑·C7 动机连贯：C7 动机连贯 最终 1 分：跨镜头的情绪与动机连得上，没有突然的转变；首帧放大（work/character_B__a/s6st6_zoom.png）：Ril
  - 方案：s6_st6 文字照首帧：门外一步、看画右柜台，加触发「门里传出碗勺声和饭香」；s5_st7 远景两个男人按首帧写，不再声称是 st6 那两人；s5_st8 首帧修正
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- **I16** [严重·implemented·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；z_s5_st8_right.jpg：驴头和赶车人都朝着镜头走过来，spec 写的是车「直直往
  - 方案：s5_st8 首帧修成车尾朝镜头、往画右拐可读；s4_st3 改「左后方」；s6_st1 墙龛改「在她右后方（画面上在她左边）」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I31** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；放大看（`work/framing_B__a/s5_st8_donkey.jpg`）
  - 方案：s5_st8 首帧修成车尾朝镜头、往街深处走；s5_st6、s6_st1 overhead 照首帧改；s7_st5 overhead 机位升到约 6 m、路人放到约 43 m 外，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/overhead.toml`
- **I99** [记录·implemented·待复核] 台词（时长与逻辑）·D4：D4：「I went the wrong way all morning」所在镜在下午第九时（I86 未改）
  - 方案：v7 s5_st9 改「I've been going the wrong way all day.」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-10
+12
```

- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-接上一镜，同一条街。
+熟食铺前的东西向石板街。
 Riley 转过身面对镜头自拍，愣着，眼睛睁大、嘴微微张开。
@@ -4,5 +4,5 @@
 她身后：画左是熟食铺的门脸（挂着香肠和火腿）；
-画右远处是刚才那排铺面——店主那家门口挂着几串大蒜、放着藤筐，门里是暗的，门口空着；
-在她左肩后方、画面中间偏右的远处，那排铺面断开，露出驴车拐进去的横街口。
-她慢慢说出这两句，中间停一拍，恍然大悟；
+画右远处是街南侧那排铺面——离得近些的那家门口挂着几串大蒜、放着藤筐，门里是暗的，门口空着；
+在她左肩后方、画面中间偏右的远处，那排铺面断开，露出一个往右（南）拐的横街口。
+她慢慢说出这几句：先问 dextram 是不是「右」，停一拍，恍然大悟；
 说完用左手捂住脸，从指缝里笑出声，笑自己。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
 Riley 站在街上，面朝西对着镜头，在画面中间偏左；
-镜头在她伸直的右臂末端、在她面前一臂远，朝东拍（和 st8 同一个朝向，右还是右）；
+镜头在她伸直的右臂末端、在她面前一臂远，朝东拍；
 她身后是十字街口，横街口在她左肩后方、画面中间偏右的远处。
```

- 分镜「节拍」改了：

```diff
@@ -1,5 +1,6 @@
 0–1.5秒 第 0 秒：Riley 刚转过身面对镜头，愣着，眼睛睁大、嘴微微张开、眉毛扬起；
-她左肩后方（画面中间偏右）的远处是那个横街口，店主的铺子门口空着；
+她左肩后方（画面中间偏右）的远处是那个横街口，挂着大蒜的铺子门口空着；
 这一拍不说话；
-1.5–7.5秒 她慢慢说出那两句，right 前停一拍、重读，两句中间再停一拍，自己恍然大悟（1.6–7.3 秒）；
-7.5–10秒 她用左手捂住脸，从指缝里笑出声，笑自己，不说话
+1.5–9.7秒 她慢慢说出那几句，自己恍然大悟（1.6–9.5 秒）：1.6–2.0 秒 Wait.，2.6–4.0 秒 "Dextram" means right?
+（right 重读、问句上扬），停一拍、眼睛越睁越大，5.0–5.9 秒 …Oh my god.，6.3–9.5 秒 I've been going the wrong way all day.；
+9.7–12秒 她用左手捂住脸，从指缝里笑出声，笑自己，不说话
```

- 分镜「台词」改了：

```diff
@@ -1,3 +1,4 @@
 Riley（愣住，然后恍然大悟、笑自己，美式英语；
-right 重读，前面停一拍）：Wait… "dextram" is right?
-…I went the wrong way all morning.
+Dextram 读 DEK-strahm；
+right 重读、问句上扬，问完停一拍）：Wait. "Dextram" means right?
+…Oh my god. I've been going the wrong way all day.
```


### s5_st2

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st2/planning/st2_first_frame.png`）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -4,5 +4,5 @@
 后墙庞贝红抹灰，上面是赭黄底的壁画：一只倒挂的野鸭和一只公鸡。
-台面上的东西（全场固定）：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
-她左手边是一只收钱的小陶碗，台沿上搭着一块叠起的粗布抹布；
-台面中间那只敞口陶罐的罐口上横搁着一把青铜长柄勺（用完就放回这里）；
+台面上的东西：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
+她左手边是一只收钱的小陶碗；
+她面前、台面前排中间是一只敞口陶罐，青铜长柄勺用完就横搁在它的罐口上；
 两人中间的台面上是一只给 Riley 的赭色粗陶杯（不透光的粗陶）；
@@ -11,3 +11,3 @@
 Riley 从画右的街上走一两步，走到柜台外侧站定，看着陶罐。
-老板娘 Asellina 在柜台里低头用青铜长柄勺搅台面中间那只敞口陶罐，抬头看见她，目光在她披散的乌黑长发和那件古怪的短袖衬衫上转了一圈，挑了下眉；
+老板娘 Asellina 在柜台里低头用青铜长柄勺搅她面前、台面前排中间那只敞口陶罐，抬头看见她，目光在她披散的乌黑长发和那件古怪的短袖衬衫上转了一圈，挑了下眉；
 随即换上做生意的笑，把勺子横搁回那只罐口上，右手举到脸边竖起一根食指（只有一根），竖着这根手指对她说第一句报价。
@@ -16,2 +16,2 @@
 钱在她裤子左侧的大口袋里；
-长柄勺从 Asellina 手里到横搁回台面中间那只敞口陶罐的罐口。
+长柄勺从 Asellina 手里到横搁回台面前排中间那只敞口陶罐的罐口。
```

- 分镜「节拍」改了：

```diff
@@ -1,3 +1,3 @@
 0–2秒 第 0 秒：画右边缘，Riley 刚从街上走进画，正迈步走向柜台，离柜台还有一两步，双手空着，布包挂在左胯，看着冒热气的陶罐；
-画左，Asellina 在柜台里低头用青铜长柄勺搅台面中间那只敞口陶罐；
+画左，Asellina 在柜台里低头用青铜长柄勺搅台面前排中间那只敞口陶罐；
 这一拍不说话；
```


### s5_st10

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st10/planning/_r3_before/st10_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st10/planning/st10_first_frame.png`（现行）
- **I48** [主要·implemented·待复核] 时代与世界观·E4·蒸汽（上一轮 I106 未改好）、R：E4·蒸汽（上一轮 I106 未改好）、R：罐口升起一股灰白热气到画面约 30% 高（z_steam510.jpg），prompt 写「贴在罐口」，违背 bib
  - 方案：s5_st10 首帧局部压低罐口热气，只留贴口一层，ffp 负面词加「升起来的热气柱、蒸汽柱」；s5_st13 首帧去掉悬空白汽
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st10/planning/st10_first_frame_prompt.txt`
- **I107** [记录·implemented·待复核] 时代与世界观·E4 系列禁区（R：I106）：E4 系列禁区（R：I106）：首帧 prompt 第 4 行「旁边一只敞口陶罐冒着热气」；首帧里热气从罐口一股往上升，到画面约一半高（y≈470/941）；同
  - 方案：s5_st10 首帧局部压淡上升的热气；ffp 改「罐口贴着一层很薄的热气」，负面词加热气柱
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st10/planning/st10_first_frame_prompt.txt`
- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
 Asellina 站在柜台后，背靠红色后墙和公鸡壁画，脸朝画右（画外的 Riley）；
-镜头在柜台外、Riley 身边偏左（离 Asellina 约两米三），和双人主机位同一侧，斜对她。
+镜头在柜台外、Riley 身边偏左（离 Asellina 约两米三），斜对她。
 配角一行：Asellina——看着 Riley，心想「给两个子儿，就喝好的」，等着她掏钱。
```


### s5_st11

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st11/planning/st11_first_frame.png`）
- **I15** [严重·implemented·待复核] 连续性·K4 光与时间：K4 光与时间 最终 1 分：光向、时段、天色随时间推进合理，同场一致；z_s2_st1.jpg：画右东侧店面被晒成金色，画左西墙在阴影里，跟同场其他镜（西墙上
  - 方案：s2 八镜光线行改成绝对方位＋本镜画面位置；s2_st1（压暗画右东侧店面）、s2_st3（压暗正对镜头的东侧铺面上半截）首帧局部修图
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st1/planning/st1_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s2/shots/st3/planning/st3_first_frame_prompt.txt`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-9
+14
```

- 分镜「动作」改了：

```diff
@@ -2,3 +2,3 @@
 画面里只有她一个人：她身后的石板街面空空荡荡，对面的房子关着门，阳光铺在路面上。
-她站在柜台外，脸朝画左（画外的 Asellina），眯着眼盯着她那两根手指，眉头微皱，一边慢慢点头一边猜着说出两档价钱；
+她站在柜台外，脸朝画左（画外的 Asellina），眯着眼盯着她那两根手指，眉头微皱，一边慢慢点头一边猜着说出两档价钱，再问一句是不是这个意思；
 说完右手抬到胸前，拇指和食指捏成一个圈、其余三指伸开，比出 OK 手势，伸向画左，挑眉等着回答。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
 Riley 在画面中间偏右，脸朝画左（画外柜台里的 Asellina），视线就在镜头左边一点；
-镜头在柜台里面、Asellina 的西边，隔着柜台朝外（东南）拍，和其他柜台镜头在同一侧；
+镜头在柜台里面、Asellina 的西边，隔着柜台朝外（东南）拍；
 她身后是明亮、空荡荡的石板街。
```

- 分镜「节拍」改了：

```diff
@@ -3,3 +3,5 @@
 这一拍不说话；
-1.5–6.5秒 她看着画左，一边慢慢点头一边猜着说那句（1.6–6.3 秒）；
-6.5–9秒 她右手抬到胸前，拇指和食指捏成一个圈、其余三指伸开，比出 OK 手势，伸向画左，挑眉等着回答，不说话
+1.5–11.6秒 她看着画左，一边慢慢点头一边猜着说（1.6–11.4 秒）：1.6–2.6 秒 Okay, so…，3.0–5.8 秒 one coin gets you the cheap stuff,，6.1–8.9 秒 and two gets you the good stuff?
+，9.4–11.4 秒 Is that what you're saying?
+（眉毛一挑）；
+11.6–14秒 她右手抬到胸前，拇指和食指捏成一个圈、其余三指伸开，比出 OK 手势，伸向画左，挑眉等着回答，不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1,2 @@
-Riley（猜，美式英语）：One coin, cheap stuff… two coins, the good stuff?
+Riley（猜，美式英语）：Okay, so… one coin gets you the cheap stuff, and two gets you the good stuff?
+Is that what you're saying?
```


### s5_st12

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st12/planning/st12_first_frame.png`）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I12** [严重·implemented·待复核] 人物逻辑·C4 反应拍：C4 反应拍 最终 1 分：配角的反应单独占拍，不被吞掉；反应和身份、性格相符；首帧放大（work/character_B__a/s5st8_zoom2.png
  - 方案：s5_st8 店主在首帧；Asellina 三镜反应拉开：st12 抱胳膊笑、st14 低头擦台面只抬眼一瞥不笑、st7 摇头笑；s6_st5 改为满意点头、嘴角一抿
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I97** [记录·implemented·待复核] 连续性·连续性·K2：连续性·K2：st12 道具行写「钱在她裤子左侧的大口袋里」，st3 第 0 s 钱已经攥在右拳里，掏钱、换手在两镜之间的画外完成（上一轮 I8 为了贴首帧有意
  - 方案：s5_st12 末拍补左手从口袋掏钱、换到右手攥拳（v7 在 8.6–11 s），接 st3 第 0 秒的右拳
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st12/planning/overhead.toml`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-8
+11
```

- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-接上一镜，回到双人主机位。
+柜台前。
 画面里只有两个人：Asellina 和 Riley。
@@ -6,6 +6,6 @@
 Asellina 放下手，抱起胳膊看着她对着空气说话，嘴角一扬，不看镜头；
-Riley 说完放下手，笑着转回去看 Asellina。
-台面上的东西（全场固定）：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
-她左手边是一只收钱的小陶碗，台沿上搭着一块叠起的粗布抹布；
-台面中间那只敞口陶罐的罐口上横搁着一把青铜长柄勺（用完就放回这里）；
+Riley 说完放下手，笑着转回去看 Asellina，左手从布包后面伸进裤子左侧的大口袋，掏出钱攥进右手。
+台面上的东西：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
+她左手边是一只收钱的小陶碗；
+她面前、台面前排中间是一只敞口陶罐；
 两人中间的台面上是一只给 Riley 的赭色粗陶杯（不透光的粗陶）；
@@ -13,2 +13,2 @@
 道具：面包布包挂在 Riley 左胯；
-钱在她裤子左侧的大口袋里。
+钱进场在她裤子左侧的大口袋里，8.6–11 秒被她左手掏出来、交到右手攥成拳，出场攥在她右拳里。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
-同 st2 的双人主机位：Asellina 在画左（柜台里），Riley 在画右（柜台外，街在她身后、画右），Riley 四分之三侧脸对镜头；
-砖灶和青铜锅在柜台里、画面中间偏右的后面（和 st2、st7 一致）。
+镜头在街上、柜台长边的西头外侧，斜对柜台朝东，离两人两米半到三米：Asellina 在画左（柜台里），Riley 在画右（柜台外，街在她身后、画右），Riley 四分之三侧脸对镜头；
+砖灶和青铜锅在柜台里、画面中间偏右的后面。
 说台词时 Riley 转脸直视镜头，说完转回画左看 Asellina。
```

- 分镜「节拍」改了：

```diff
@@ -5,5 +5,8 @@
 2.5–3.5秒 Riley 眼睛一亮，惊喜地转脸直视镜头（Riley 的反应拍，单独一拍），不说话；
-3.5–6秒 她对镜头说那句话（3.6–5.8 秒）；
+3.5–8.6秒 她对镜头说那两句（3.6–8.4 秒）：3.6–6.0 秒 Oh my god, the OK sign works!
+，6.4–8.4 秒 She knows the OK sign!
+（说这句时朝画左的 Asellina 偏一下头）；
 Asellina 放下手，抱起胳膊看着她对空气说话，嘴角一扬，不看镜头；
-6–8秒 Riley 放下手，笑着转回去看 Asellina，嘴闭着；
+8.6–11秒 Riley 放下手，笑着转回去看 Asellina，嘴闭着；
+她左手从布包后面伸进裤子左侧的大口袋，掏出钱交到右手，右手攥成拳停在台面边；
 这一拍不说话
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1,2 @@
-Riley（惊喜，美式英语）：Ha!
-The OK sign works here!
+Riley（惊喜，美式英语）：Oh my god, the OK sign works!
+She knows the OK sign!
```


### s5_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st3/planning/st3_first_frame.png`）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I97** [记录·implemented·待复核] 连续性·连续性·K2：连续性·K2：st12 道具行写「钱在她裤子左侧的大口袋里」，st3 第 0 s 钱已经攥在右拳里，掏钱、换手在两镜之间的画外完成（上一轮 I8 为了贴首帧有意
  - 方案：s5_st12 末拍补左手从口袋掏钱、换到右手攥拳（v7 在 8.6–11 s），接 st3 第 0 秒的右拳
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st12/planning/overhead.toml`
- **I98** [记录·planned·待复核] 连续性·连续性·K3：连续性·K3：s6_st2_shirt.jpg：Riley 衬衫前襟、袖子满是凸起的波纹、方格提花图案，看起来像另一件有花纹的衬衫；同场 s6_st5 首帧（s
  - 方案：s6_st2 首帧局部修回素面米白亚麻，ffp 加「素面无花纹亚麻」、负面词加「提花、压纹图案」；s8_st6/st9 视情况处理（未做）
- **I116** [记录·wontfix·待复核] Prompt 文本·T7·长度与重点：T7·长度与重点：s5_st14 15 秒里 Asellina 8 步以上操作；s8_st2 15 秒数 7 枚钱再付再收；s6_st1/2/3 长达 4471
  - 方案：保留 s5_st14 擦台面、点水两拍和 s8_st2 数钱；固定负面词已去重
- 分镜「动作」改了：

```diff
@@ -2,5 +2,5 @@
 画面里只有两个人：Asellina 和 Riley。
-台面上的东西（全场固定）：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
-她左手边是一只收钱的小陶碗，台沿上搭着一块叠起的粗布抹布；
-台面中间那只敞口陶罐的罐口上横搁着一把青铜长柄勺（用完就放回这里）；
+台面上的东西：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
+她左手边是一只收钱的小陶碗；
+她面前、台面前排中间是一只敞口陶罐；
 两人中间的台面上是一只给 Riley 的赭色粗陶杯（不透光的粗陶）；
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-镜头比双人主机位近一点，同一条轴线：Asellina 在画左（柜台里），Riley 在画右（柜台外）；
+镜头在街上、柜台长边的西头外侧，斜对柜台朝东，离两人两米多：Asellina 在画左（柜台里），Riley 在画右（柜台外）；
 钱、陶杯、小陶碗都在两人之间的台面上、画面中下部。
```

- 分镜「镜头」改了：

```diff
@@ -1,3 +1,3 @@
 他拍：固定机位旁观拍摄，眼平略低；
-中景双人，斜对柜台，比双人主机位近一点：Asellina 在画左、Riley 在画右，两人腰以上；
+中景双人，斜对柜台，离两人两米多：Asellina 在画左、Riley 在画右，两人腰以上；
 Riley 的两只手和台面上的钱、陶杯、小陶碗在画面中下部；
```


### s5_st14

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/_r3_before/st14_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame.png`（现行）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I12** [严重·implemented·待复核] 人物逻辑·C4 反应拍：C4 反应拍 最终 1 分：配角的反应单独占拍，不被吞掉；反应和身份、性格相符；首帧放大（work/character_B__a/s5st8_zoom2.png
  - 方案：s5_st8 店主在首帧；Asellina 三镜反应拉开：st12 抱胳膊笑、st14 低头擦台面只抬眼一瞥不笑、st7 摇头笑；s6_st5 改为满意点头、嘴角一抿
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I43** [主要·implemented·待复核] 世界物理·P5 时长：P5 时长：overhead：她原位 (5.85,3.85)，勺 (6.4,4.6) 距 0.79 m，酒罐 (5.3,4.5) 距 0.85 m。1.5 s 
  - 方案：s5_st14 重排：2–4 s 取勺舀酒、5.5–7 s 放勺盖盖；v7 镜长 15→21 s，「Oh, she's putting water in it」和点水同步；toml 同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/overhead.toml`
- **I96** [记录·planned·待复核] 人物逻辑·C5 对当地人有回应：C5 对当地人有回应：0–8 秒 Asellina 倒酒兑水，Riley 只在 0–1 秒「看着她」，8 秒直接指杯转向镜头评论「They water the 
  - 方案：s5_st14 在转向镜头前加 Riley 冲 Asellina 点头笑一下（v7 重排后没加）
- **I115** [记录·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数：快照的节拍写「2–3.5秒 她侧身朝画右探出半步，右手从中间那只陶罐的罐口上拿起长柄勺，退回原位，从酒罐里舀出一勺深红的酒」，1.5 秒里有四个
  - 方案：s5_st14 重排为 2–4 s 取勺舀酒、5.5–7 s 放勺盖盖，v7 镜长 21 s，overhead 同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/overhead.toml`
- **I116** [记录·wontfix·待复核] Prompt 文本·T7·长度与重点：T7·长度与重点：s5_st14 15 秒里 Asellina 8 步以上操作；s8_st2 15 秒数 7 枚钱再付再收；s6_st1/2/3 长达 4471
  - 方案：保留 s5_st14 擦台面、点水两拍和 s8_st2 数钱；固定负面词已去重
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-15
+21
```

- 分镜「动作」改了：

```diff
@@ -1,6 +1,6 @@
-接上一镜，回到双人主机位。
+柜台前。
 画面里只有两个人：Asellina 和 Riley。
-台面上的东西（全场固定）：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
-她左手边是一只收钱的小陶碗，台沿上搭着一块叠起的粗布抹布；
-台面中间那只敞口陶罐的罐口上横搁着一把青铜长柄勺（用完就放回这里）；
+台面上的东西：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
+她左手边是一只收钱的小陶碗，碗旁的台面上叠放着一块灰白粗麻抹布；
+她面前、台面前排中间是一只敞口陶罐，后排靠灶还有一只敞口陶罐，青铜长柄勺此刻横搁在后排那只的罐口上；
 两人中间的台面上是一只给 Riley 的赭色粗陶杯（不透光的粗陶）；
@@ -8,7 +8,7 @@
 Asellina 右手掀开那只酒罐的圆木盖，放在台面上罐口旁边；
-侧身朝画右探出半步，右手从台面中间那只敞口陶罐的罐口上拿起横搁着的青铜长柄勺，退回原位，从酒罐里舀出深红的酒，倒进两人中间那只粗陶杯，到半杯；
-把勺子横搁回台面中间那只陶罐的罐口上，再用右手把圆木盖盖回酒罐；
-再用右手拿起那只带把手的陶水罐，往杯里点了一小股冷水，把水罐放回原处（先酒后水，一次只拿一样）。
-Riley 用右手指着杯子，转脸对镜头说话；
-Asellina 拿起搭在左手边台沿上的抹布擦台面，抬眼看看她对着空气说话，嘴角一撇笑笑，接着擦，不看镜头。
+侧身朝画右探出半步，右手从后排那只陶罐的罐口上拿起青铜长柄勺，退回原位，从酒罐里舀出深红的酒，倒进两人中间那只粗陶杯，到半杯；
+把勺子横搁到她面前前排中间那只陶罐的罐口上，再用右手把圆木盖盖回酒罐；
+再用右手拿起那只带把手的陶水罐，往杯里慢慢点了一小股冷水，把水罐放回原处（先酒后水，一次只拿一样）。
+她拿起水罐时，Riley 用右手指着杯子，转脸对镜头说话：先说她在往酒里兑水，再说这里人人都兑水喝；
+Asellina 放回水罐后拿起小陶碗旁那块抹布，低头擦台面，只抬眼瞥了她一下，不笑，接着擦，不看镜头。
 Riley 说完右手端起陶杯闻了闻，挑挑眉，放回两人中间的台面上。
@@ -16,3 +16,4 @@
 酒罐出场时盖着圆木盖；
-长柄勺出场横搁在台面中间那只陶罐的罐口上；
+长柄勺进场横搁在后排那只陶罐的罐口上，出场横搁在前排中间那只陶罐的罐口上；
+抹布进场叠在小陶碗旁，出场在 Asellina 手边的台面上；
 面包布包挂在 Riley 左胯。
```

- 分镜「走位」改了：

```diff
@@ -1,4 +1,3 @@
-同 st2 的双人主机位：Asellina 在画左（柜台里），Riley 在画右（柜台外），Riley 四分之三侧脸对镜头；
+镜头在街上、柜台长边的西头外侧，斜对柜台朝东，离两人两米半到三米：Asellina 在画左（柜台里），Riley 在画右（柜台外），Riley 四分之三侧脸对镜头；
 陶杯、酒罐、水罐在两人之间的台面上、画面中下部。
-镜头离两人两米半到三米。
 站位：Asellina 在柜台里、紧挨着柜台站（拿勺时朝画右探出半步再退回），Riley 在柜台外、紧挨着柜台站，两人隔着台面面对面，相距一米多，各自伸手都够得到台面中间。
@@ -6,2 +5,2 @@
 配角一行：Asellina——倒酒时专心看杯子；
-Riley 对着空气说话时，她一边擦台面一边抬眼看她，觉得这外地人怪有意思。
+Riley 对着空气说话时，她低头擦台面，只抬眼瞥一下，心想「这外地人又在自言自语」，接着干活。
```

- 分镜「节拍」改了：

```diff
@@ -1,14 +1,18 @@
-0–1秒 第 0 秒：画左，Asellina 在柜台后，右手按在酒罐的圆木盖上；
+0–1秒 第 0 秒：画左，Asellina 在柜台后，右手按在酒罐的圆木盖上，左手搭在小陶碗边；
 画右，Riley 站在柜台外看着她，两手空着垂在身侧，布包挂在左胯；
-两人中间的台面上一只空的粗陶杯，台面中间那只敞口陶罐的罐口上横搁着青铜长柄勺；
+两人中间的台面上一只空的粗陶杯；
+小陶碗旁叠着一块灰白抹布；
+后排靠灶那只敞口陶罐的罐口上横搁着青铜长柄勺；
 这一拍不说话；
 1–2秒 Asellina 右手掀开圆木盖，放在罐口旁边的台面上；
-2–3.5秒 她侧身朝画右探出半步，右手从中间那只陶罐的罐口上拿起长柄勺，退回原位，从酒罐里舀出一勺深红的酒；
-3.5–5秒 她把酒倒进那只陶杯，到半杯；
-5–6.5秒 她把勺子横搁回中间那只陶罐的罐口上，再用右手把圆木盖盖回酒罐；
-6.5–8秒 她右手拿起带把手的陶水罐，往杯里点了一小股冷水，把水罐放回原处；
-8–9秒 Riley 用右手指着杯子，转脸直视镜头，不说话；
-9–12秒 她对镜头说那句话（9.1–11.9 秒）；
-Asellina 拿起左手边台沿上的抹布擦台面，抬眼看看她，嘴角一撇笑笑，不看镜头；
-12–15秒 Riley 右手端起陶杯闻了闻，挑挑眉，把杯子放回两人中间的台面上；
+2–4秒 她侧身朝画右探出半步，右手从后排那只陶罐的罐口上拿起长柄勺，退回原位，从酒罐里舀出一勺深红的酒；
+4–5.5秒 她把酒倒进那只陶杯，到半杯；
+5.5–7秒 她把勺子横搁到面前前排中间那只陶罐的罐口上，再用右手把圆木盖盖回酒罐；
+7–8秒 Asellina 右手拿起带把手的陶水罐；
+Riley 看着，抬起右手指着杯子，转脸直视镜头，不说话；
+8–10.8秒 Asellina 往杯里慢慢点了一小股冷水，把水罐放回原处；
+Riley 指着杯子对镜头说 Oh, she's putting water in it.（8.1–10.7 秒）；
+10.8–18.8秒 她接着对镜头说（10.9–18.6 秒）：10.9–14.5 秒 Yeah — apparently everyone here waters their wine down.，15.0–18.6 秒 Drinking it straight is, like, a barbarian thing.（说到 barbarian 时眉毛一挑）；
+Asellina 拿起小陶碗旁的抹布低头擦台面，只抬眼瞥她一下，不笑，接着擦，不看镜头；
+18.8–21秒 Riley 右手端起陶杯闻了闻，挑挑眉，把杯子放回两人中间的台面上；
 这一拍不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1 @@
-Riley（指着杯子，美式英语）：They water the wine down. Everybody does.
+Riley（指着杯子，美式英语）：Oh, she's putting water in it. Yeah — apparently everyone here waters their wine down. Drinking it straight is, like, a barbarian thing.
```


### s5_st13

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st13/planning/_r3_before/st13_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st13/planning/st13_first_frame.png`（现行）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I4** [严重·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；`s6st3_cart.png`：驴站在货车左侧，后蹄和车尾轮在同一深
  - 方案：s6_st3 首帧局部修：驴在两根车辕之间、车箱正前方；s5_st13 首帧去掉悬空白汽；s5_st4 文字贴首帧（第 0 秒罐口已淌一缕，一两秒后扶正）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame_prompt.txt`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I48** [主要·implemented·待复核] 时代与世界观·E4·蒸汽（上一轮 I106 未改好）、R：E4·蒸汽（上一轮 I106 未改好）、R：罐口升起一股灰白热气到画面约 30% 高（z_steam510.jpg），prompt 写「贴在罐口」，违背 bib
  - 方案：s5_st10 首帧局部压低罐口热气，只留贴口一层，ffp 负面词加「升起来的热气柱、蒸汽柱」；s5_st13 首帧去掉悬空白汽
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st10/planning/st10_first_frame_prompt.txt`
- **I49** [主要·implemented·待复核] 镜头规格·F6 轴线：F6 轴线 最终 1 分：同一场前后镜头的左右关系不跳轴；I116 状态还是 open。st6 机位 (8,9) 在食客 (10.1,3.2) 到 Riley 
  - 方案：s5_st6 删掉「和双人主机位同一侧」的错误说法；overhead [[camera]] 加 axis_ok，写明有意反打、食客朝画左看画外的 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I101** [记录·implemented·待复核] 台词（时长与逻辑）·D3：D3：prompt 写 EW-geh，changes.md 写 YOO-geh，注音不统一
  - 方案：分镜保留 EW-geh（两音节、硬 g）；r05 #27 同步为 EW-geh，补 /ˈeu̯.ɡe/
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`
- **I103** [记录·implemented·待复核] 台词（时长与逻辑）·D3·注音来源未同步；R I46：D3·注音来源未同步；R I46：r05_衣着语言黑名单.md:142 仍写 doom；:148 仍写 EH-oo-geh，未明确 eu 一音节。当前 Helv
  - 方案：r05 #21 改「dum（短 u，不读 doom）」；#27 改 EW-geh，注明 eu 合成一个音节、共两音节、/ˈeu̯.ɡe/
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`
- **I104** [记录·wontfix·待复核] 台词（时长与逻辑）·D3·注音歧义：D3·注音歧义：prompt 第 19 行 Euge 注「EW-geh」，英语读者常把 ew 读成 /juː/，正好回到 changes.md 第 50 行想避
  - 方案：保留 EW-geh，r05 补 IPA /ˈeu̯.ɡe/ 和「eu 合成一个音节」的说明
- 分镜「动作」改了：

```diff
@@ -1,6 +1,6 @@
-接上一镜，柜台前。
+柜台前。
 画面里只有两个人：Asellina 和 Riley。
-台面上的东西（全场固定）：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
-她左手边是一只收钱的小陶碗，台沿上搭着一块叠起的粗布抹布；
-台面中间那只敞口陶罐的罐口上横搁着一把青铜长柄勺（用完就放回这里）；
+台面上的东西：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的小陶罐（装鱼露：约三十厘米高，细颈窄口，浅赭陶色，瓶身光溜溜、不带把，口上塞着一小团布）；
+她左手边是一只收钱的小陶碗，碗旁的台面上叠放着一块灰白粗麻抹布；
+她面前、台面前排中间那只敞口陶罐的罐口上横搁着一把青铜长柄勺；
 两人中间的台面上是Riley 那只盛着兑水酒的赭色粗陶杯（不透光的粗陶）；
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-镜头比双人主机位近一点（同 st3）：Asellina 在画左（柜台里），Riley 在画右（柜台外）；
+镜头在街上、柜台长边的西头外侧，斜对柜台朝东，离两人两米多：Asellina 在画左（柜台里），Riley 在画右（柜台外）；
 布包摊开在 Riley 面前的台面上，画面中下部；
```

- 分镜「节拍」改了：

```diff
@@ -2,3 +2,3 @@
 两人中间的台面上是那只盛了兑水酒的赭色粗陶杯；
-酒罐盖着圆木盖，长柄勺横搁在台面中间那只敞口陶罐的罐口上；
+酒罐盖着圆木盖，长柄勺横搁在台面前排中间那只敞口陶罐的罐口上，小陶碗旁叠着灰白抹布；
 画左，Asellina 在柜台后看着她，细高的小陶罐立在她右手边；
```


### s5_st6

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/st6_first_frame.png`）
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I23** [严重·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；牵驴的车夫留着修过的短须（z_s5st8_man.png）
  - 方案：c7 卡、s8 文字和 st3/st4/st5/st6/st8/st9 首帧 prompt 的「浴袍」改成「粗亚麻裹身长衣」，剧级负面词加「翻领浴袍，毛巾布浴袍」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I30** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；俯视图机位 (6.7,8.7)，离 Riley 1.33 m、离 Fort
  - 方案：s6_st2 照首帧反推 overhead：机位 (5.85,9.0) 看 (5.85,7.2)、aim_h 1.5、约俯 10°，文字写正侧面、离手约 1.8 m；s5_st6 机位贴首帧并加 axis_ok 理由
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I31** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；放大看（`work/framing_B__a/s5_st8_donkey.jpg`）
  - 方案：s5_st8 首帧修成车尾朝镜头、往街深处走；s5_st6、s6_st1 overhead 照首帧改；s7_st5 overhead 机位升到约 6 m、路人放到约 43 m 外，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/overhead.toml`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I49** [主要·implemented·待复核] 镜头规格·F6 轴线：F6 轴线 最终 1 分：同一场前后镜头的左右关系不跳轴；I116 状态还是 open。st6 机位 (8,9) 在食客 (10.1,3.2) 到 Riley 
  - 方案：s5_st6 删掉「和双人主机位同一侧」的错误说法；overhead [[camera]] 加 axis_ok，写明有意反打、食客朝画左看画外的 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -1,7 +1,7 @@
-柜台短边那一头的插入镜：两个刚干完活的男人（普通路人，不说话、不看镜头；
-粗布短 tunica，晒黑的手臂，一个脸刮得干净、一个留着短胡茬）刚走到柜台短边外侧站着吃饭：画左那个用一块面包蘸着红陶碗里的豆子，画右那个仰头喝粗陶杯里的酒；
-柜台角上一个六七岁的小孩踮着脚、扒着台面往一只陶罐里看，他身后一位妇女（深色及踝 tunica，头上搭着披巾）伸手把他拉开，牵着他朝画右走开。
-吃豆子的男人嚼着面包，好奇地朝画左画外（柜台长边那头、Riley 站的地方）看了一眼——看见那个外地女人自己带了一包面包来——嘴里的面包停了一下，又低头接着吃；
+柜台东头那一段的插入镜：两个刚干完活的男人（普通路人，不说话、不看镜头；
+粗布短 tunica，晒黑的手臂，一个脸刮得干净、一个留着短胡茬）站在柜台外侧、东头拐角前的台沿边吃饭：画左那个用一块面包蘸着红陶碗里的豆子，画右那个仰头喝粗陶杯里的酒；
+柜台东头拐角上一个六七岁的小孩踮着脚、扒着台面往一只陶罐里看，他身后一位妇女（深色及踝 tunica，头上搭着披巾）伸手把他拉开，牵着他朝画右走开。
+吃豆子的男人嚼着面包，好奇地朝画左画外（柜台长边西头、Riley 站的地方）看了一眼——看见那个外地女人自己带了一包面包来——嘴里的面包停了一下，又低头接着吃；
 喝酒的那个只顾喝酒，没抬头。
 画面里共四个人：两个男人、小孩和拉孩子的妇女；
-砖灶和青铜锅在柜台里、画面左半的后面。
+砖灶和青铜锅在柜台里、两个男人身后。
```

- 分镜「走位」改了：

```diff
@@ -1,3 +1,4 @@
-镜头在街上、眼平，站在 Riley 身后偏东的街面上斜对柜台短边（朝东北），和双人主机位在 Asellina–Riley 连线的同一侧：两个男人站在柜台短边外侧、画面中间偏右，小孩和妇女在柜台角、画右；
-Asellina 和 Riley 都在画左画外（柜台长边那头）。
+镜头在街上、眼平，站在柜台东头南边约四米的街面上，正对柜台长边的东段朝北拍：两个男人站在柜台外侧的台沿前、画面中间偏左，全身入画；
+小孩和妇女在柜台东头拐角、画右；
+Asellina 和 Riley 都在画左画外（柜台长边西头那段）。
 配角一行：吃豆子的男人——看见那个外地女人自己带了面包来，心想「来铺子里还自带干粮」，看一眼就接着吃；
```

- 分镜「节拍」改了：

```diff
@@ -1,3 +1,3 @@
-0–3秒 第 0 秒：柜台短边外侧站着两个刚干完活的男人：画左那个用一块面包蘸着红陶碗里的豆子吃，画右那个仰头喝粗陶杯里的酒；
-柜台角上一个小孩踮着脚往陶罐里看，一位妇女站在他身后；
+0–3秒 第 0 秒：柜台东段外侧的台沿前站着两个刚干完活的男人：画左那个用一块面包蘸着红陶碗里的豆子吃，画右那个仰头喝粗陶杯里的酒；
+柜台东头拐角上一个小孩踮着脚往陶罐里看，一位妇女站在他身后；
 这一拍不说话；
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
 他拍：固定机位旁观拍摄，眼平；
-全景，环境插入：柜台短边与吃饭的人，砖灶在后面。
+全景，环境插入：柜台东段、台沿前吃饭的人，砖灶在他们身后。
```


### s5_st4

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st4/planning/st4_first_frame.png`）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I4** [严重·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；`s6st3_cart.png`：驴站在货车左侧，后蹄和车尾轮在同一深
  - 方案：s6_st3 首帧局部修：驴在两根车辕之间、车箱正前方；s5_st13 首帧去掉悬空白汽；s5_st4 文字贴首帧（第 0 秒罐口已淌一缕，一两秒后扶正）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame_prompt.txt`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I36** [严重·implemented·待复核] Prompt 文本·T4 图文一致：T4 图文一致 最终 1 分：文字和挂的首帧、站位图、场景图一致；P13写“共三个人和一头驴”，P15第0秒店主已在画右铺门口，车夫牵驴向纵深走、4–8秒右拐。
  - 方案：s5_st8 首帧局部修：驴车朝街深处、车尾朝镜头，保留画右铺门口店主；s5_st4 文字照首帧写第 0 秒已在淌一缕鱼露、一两秒后扶正
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I49** [主要·implemented·待复核] 镜头规格·F6 轴线：F6 轴线 最终 1 分：同一场前后镜头的左右关系不跳轴；I116 状态还是 open。st6 机位 (8,9) 在食客 (10.1,3.2) 到 Riley 
  - 方案：s5_st6 删掉「和双人主机位同一侧」的错误说法；overhead [[camera]] 加 axis_ok，写明有意反打、食客朝画左看画外的 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -3,4 +3,4 @@
 她的右手垂在身侧、在台面以下；
-画左边缘伸进来 Asellina 的右手（她隔着柜台探身过来），握着那只细高的鱼露小陶罐（约三十厘米高，细颈窄口，口上的布塞已经拔掉），罐身已经斜着、罐口朝下，就在面包瓣正上方一两厘米。
-小陶罐再倾斜一点，三滴琥珀色的鱼露一滴一滴落在面包瓣上，然后小陶罐收回画左。
+画左边缘伸进来 Asellina 的右手（她隔着柜台探身过来），握着那只细高的鱼露小陶罐（约三十厘米高，细颈窄口，口上的布塞已经拔掉），罐身已经斜着、罐口朝下，就在面包瓣正上方几厘米，罐口正淌下细细一缕琥珀色的鱼露，落在面包瓣上。
+这一缕只淌一两秒，Asellina 就把罐身扶正，小陶罐收回画左。
 Riley 把面包瓣收回来凑到鼻子前闻，皱了皱鼻子，眉毛扬起；
```

- 分镜「走位」改了：

```diff
@@ -4,3 +4,3 @@
 她把面包瓣伸到台面上方、两人中间，Asellina 探一点身就够得着；
-镜头在柜台外、Riley 左前方，朝东拍，和主机位同一侧：她身后是柜台东头、铺子东侧的墙角（画面中间偏左，虚化）和往东延伸的明亮石板街（画面右半，虚化）。
+镜头在柜台外、Riley 左前方，朝东拍：她身后是柜台东头、铺子东侧的墙角（画面中间偏左，虚化）和往东延伸的明亮石板街（画面右半，虚化）。
 配角一行：Asellina——看着鱼露滴准，等着看外地人的反应。
```

- 分镜「节拍」改了：

```diff
@@ -2,6 +2,6 @@
 右手垂在身侧；
-画左边缘伸进来 Asellina 的右手，握着细高的小陶罐，罐身斜着、罐口朝下，就在面包瓣正上方一两厘米；
+画左边缘伸进来 Asellina 的右手，握着细高的小陶罐，罐身斜着、罐口朝下，就在面包瓣正上方几厘米，罐口正淌下细细一缕琥珀色的鱼露落在面包瓣上；
 画面下沿是摊开的亚麻布和缺了两瓣的面包；
 这一拍不说话；
-1–3秒 小陶罐再倾斜一点，三滴琥珀色的鱼露一滴一滴落在面包瓣上，然后小陶罐收回画左；
+1–3秒 细细一缕鱼露再淌一下就停，Asellina 把罐身扶正，小陶罐收回画左；
 3–5秒 Riley 把面包瓣收回来凑到鼻子前闻，皱了皱鼻子，眉毛扬起（Riley 的反应拍）；
```


### s5_st5

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st5/planning/st5_first_frame.png`）
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I22** [严重·implemented·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；首帧左上高窗是木框加竖条、横条的分格窗（z_s8st2
  - 方案：s8_st2 首帧局部修成光秃的方窗洞，ffp 负面词加「窗格、窗框分格、带玻璃的窗」；s3_st8 首帧去掉墙上竖管，负面词加「墙上的竖管、落水管」；s2_st5/st7 文字删掉石块形状描写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s8/shots/st2/planning/st2_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s3/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I49** [主要·implemented·待复核] 镜头规格·F6 轴线：F6 轴线 最终 1 分：同一场前后镜头的左右关系不跳轴；I116 状态还是 open。st6 机位 (8,9) 在食客 (10.1,3.2) 到 Riley 
  - 方案：s5_st6 删掉「和双人主机位同一侧」的错误说法；overhead [[camera]] 加 axis_ok，写明有意反打、食客朝画左看画外的 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-12
+22
```

- 分镜「动作」改了：

```diff
@@ -4,4 +4,5 @@
 左手捏着那块咬过一口的面包瓣举在下巴边——带硬皮的三角楔形一瓣，尖上缺了一口。
-她咽下去，眉头慢慢松开、眼睛越睁越大，一边回味一边对镜头说出味道；
-最后笑出来，满足地点点头，又看一眼手里的面包。
+她嚼着先「嗯」一声，咽下去，皱着眉一边回味一边对镜头说出味道，说到 funky 时皱一下鼻子；
+说到 Oh wait 时眉头一下松开、眼睛越睁越大，说到 My grandma 时笑起来；
+最后笑出声，满足地点点头，又看一眼手里的面包。
 道具：咬过的面包瓣从头到尾在她左手里；
```

- 分镜「节拍」改了：

```diff
@@ -2,3 +2,5 @@
 这一拍不说话；
-2–9.5秒 她咽下去，眉头慢慢松开、眼睛越睁越大，一边回味一边对镜头说那几句（2.1–9.3 秒）；
-9.5–12秒 她笑出来，满足地点点头，又看一眼手里的面包，不说话
+2–19.1秒 她对镜头说那几句（2.1–18.9 秒）：2.1–2.5 秒 Mm.（还嚼着，接着咽下去），3.0–4.7 秒 Okay, it's really salty,，5.0–6.8 秒 and kind of… funky?
+（皱一下鼻子），7.4–10.2 秒 Oh wait — no, that's actually good.（眉头一下松开、眼睛越睁越大），10.6–13.0 秒 It really is just fish sauce!
+，13.5–16.9 秒 My grandma puts fish sauce on literally everything.（笑起来），17.3–18.9 秒 She would love this.；
+19.1–22秒 她笑出来，满足地点点头，又看一眼手里的面包，不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1,3 @@
-Riley（嚼着，从怀疑到惊喜，美式英语）：Salty… funky… and then — whoa. It's basically fish sauce. My grandma would put this on everything.
+Riley（嚼着，从怀疑到惊喜，美式英语）：Mm. Okay, it's really salty, and kind of… funky?
+Oh wait — no, that's actually good. It really is just fish sauce!
+My grandma puts fish sauce on literally everything. She would love this.
```


### s5_st7

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st7/planning/st7_first_frame.png`）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I12** [严重·implemented·待复核] 人物逻辑·C4 反应拍：C4 反应拍 最终 1 分：配角的反应单独占拍，不被吞掉；反应和身份、性格相符；首帧放大（work/character_B__a/s5st8_zoom2.png
  - 方案：s5_st8 店主在首帧；Asellina 三镜反应拉开：st12 抱胳膊笑、st14 低头擦台面只抬眼一瞥不笑、st7 摇头笑；s6_st5 改为满意点头、嘴角一抿
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I13** [严重·implemented·待复核] 人物逻辑·C7 动机连贯：C7 动机连贯 最终 1 分：跨镜头的情绪与动机连得上，没有突然的转变；首帧放大（work/character_B__a/s6st6_zoom.png）：Ril
  - 方案：s6_st6 文字照首帧：门外一步、看画右柜台，加触发「门里传出碗勺声和饭香」；s5_st7 远景两个男人按首帧写，不再声称是 st6 那两人；s5_st8 首帧修正
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I14** [严重·implemented·待复核] 连续性·K1 道具状态表：K1 道具状态表 最终 1 分：逐镜列出每件道具进、出场状态，前后接得上；z_s5_st14_counter.jpg：台面上看不到抹布，第 9 s 却要她「拿起
  - 方案：s5_st14 首帧局部补叠好的抹布在小陶碗旁；st13、st7 抹布统一在碗旁；st12/st3 文字删掉首帧里没有的勺和抹布；st2/st14/st13 勺的位置照首帧写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I49** [主要·implemented·待复核] 镜头规格·F6 轴线：F6 轴线 最终 1 分：同一场前后镜头的左右关系不跳轴；I116 状态还是 open。st6 机位 (8,9) 在食客 (10.1,3.2) 到 Riley 
  - 方案：s5_st6 删掉「和双人主机位同一侧」的错误说法；overhead [[camera]] 加 axis_ok，写明有意反打、食客朝画左看画外的 Riley
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I62** [待核实·implemented·待复核] 母语听感·N3·开场任务对应；R·I65/I66/I105：N3·开场任务对应；R·I65/I66/I105：B04：lines.md L94 写 “Mission two: done”，L122 回顾 Bed/Garu
  - 方案：v7 开场改成「two goals today: find somewhere to sleep… and try garum」，回收改 s5_st7「garum — check. Now I just have to find a bed」、s7_st1「I found a bed, I tried the garum」，不再靠编号
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-11
+14
```

- 分镜「动作」改了：

```diff
@@ -1,4 +1,4 @@
-回到双人主机位。
+柜台前。
 主要人物是 Asellina 和 Riley；
-画面中间偏右的后面、柜台短边那头，还远远站着上一镜那两个吃饭的男人（虚化的远景，不看镜头）；
+画面中间偏右的后面、灶台那头的店里，远远坐着两个低头吃喝的男人（虚化的远景，粗布短 tunica，不看镜头）；
 Riley 身后的街面空着。
@@ -11,8 +11,8 @@
 Asellina 笑着举起刚从中间罐口拿起的青铜长柄勺回敬。
-Riley 转向镜头，满足地小声说话；
+Riley 转向镜头，满足地小声说话，说到 check 时用左手食指在空中打个勾；
 Asellina 看着她对着空气说话，摇头笑笑，用勺子搅一搅台面中间那只敞口陶罐，不看镜头。
 Riley 然后喝一口酒，长长舒一口气，朝画右街上斜下去的阳光望一眼。
-台面上的东西（全场固定）：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的鱼露小陶罐（约三十厘米高，细颈窄口，浅赭陶色，口上的布塞拔下来放在罐旁）；
-她左手边是一只收钱的小陶碗，台沿上搭着一块叠起的粗布抹布；
-台面中间是那只敞口陶罐；
+台面上的东西：Asellina 右手边（画左一侧）是一只嵌在台面里、盖着圆木盖的酒罐口，旁边立着一只带一个把手的圆肚陶水罐（约二十厘米高）和一只细高的鱼露小陶罐（约三十厘米高，细颈窄口，浅赭陶色，口上的布塞拔下来放在罐旁）；
+她左手边是一只收钱的小陶碗，碗旁的台面上叠放着一块灰白粗麻抹布；
+她面前、台面前排中间是那只敞口陶罐；
 两人中间的台面上是那只盛着兑水酒的赭色粗陶杯（不透光的粗陶）；
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-同 st2 的双人主机位：Asellina 在画左（柜台里），Riley 在画右（柜台外，街在她身后、画右），Riley 四分之三侧脸对镜头；
+镜头在街上、柜台长边的西头外侧，斜对柜台朝东，离两人两米半到三米：Asellina 在画左（柜台里），Riley 在画右（柜台外，街在她身后、画右），Riley 四分之三侧脸对镜头；
 举杯时看着画左的 Asellina，说台词时转脸直视镜头。
```

- 分镜「节拍」改了：

```diff
@@ -3,3 +3,3 @@
 画左，Asellina 在柜台后拿着刚从中间罐口拿起的青铜长柄勺看着她；
-柜台短边那头远远站着两个吃饭的男人；
+灶台那头的店里远远坐着两个低头吃喝的男人；
 这一拍不说话；
@@ -8,4 +8,4 @@
 4–5秒 Riley 转脸直视镜头，不说话；
-5–8秒 她满足地小声对镜头说那句话（5.1–7.8 秒）；
+5–10.9秒 她满足地小声对镜头说那两句（5.1–10.7 秒）：5.1–7.1 秒 Okay, so garum — check.（说到 check 时用左手食指在空中打个勾），7.5–10.7 秒 Now I just have to find a bed.；
 Asellina 看着她摇头笑笑，用勺子搅一搅中间那只敞口陶罐，不看镜头；
-8–11秒 她喝一口酒，长长舒一口气，朝画右街上斜下去的阳光望一眼，不说话
+10.9–14秒 她喝一口酒，长长舒一口气，朝画右街上斜下去的阳光望一眼，不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1,2 @@
-Riley（满足，小声，美式英语）：Mission two: done. Now… a bed.
+Riley（满足，小声，美式英语；
+garum＝GAH-rum，重音在前）：Okay, so garum — check. Now I just have to find a bed.
```


### s5 整场 / 未指明镜头

- **I106** [记录·implemented·待复核] 母语听感·N4 口癖/节奏：N4 口癖/节奏：省略号拖音 8 镜以上；basically 仍有 s8_st1、s5_st5（I97 未改）
  - 方案：v7 全部台词按新听感标准重写，s8_st1 去掉 basically

### s5 整场 / 未指明镜头

- **I112** [记录·planned·待复核] 时代与世界观·E6·出处：E6·出处：卡里把 Petronius Sat. 41 说成「浴场闲聊」；该句出自 Trimalchio 宴会场景
  - 方案：c7 卡与 r05 #21 的出处改成 Petronius Sat. 41（宴席闲谈），台词不动；未做

## s6

### s6_st3

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/_r3_before/st3_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame.png`（现行）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I4** [严重·implemented·待复核] 世界物理·P4 重力与支撑：P4 重力与支撑 最终 1 分：没有悬空的物体；放下的东西有支撑；液体、粉末、蒸汽方向对；`s6st3_cart.png`：驴站在货车左侧，后蹄和车尾轮在同一深
  - 方案：s6_st3 首帧局部修：驴在两根车辕之间、车箱正前方；s5_st13 首帧去掉悬空白汽；s5_st4 文字贴首帧（第 0 秒罐口已淌一缕，一两秒后扶正）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st3/planning/st3_first_frame_prompt.txt`
- **I5** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；`work/physics_C__a/s5st8_cart.png`：驴脸正
  - 方案：s5_st8、s6_st3 首帧局部修正驴车结构与朝向；s6_st6 不改图，文字与 overhead 照首帧（楼梯画左、马厩画右），toml note 记下与 bg6 平面图的取舍
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st6/planning/overhead.toml`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-17
+23
```

- 分镜「动作」改了：

```diff
@@ -9,10 +9,9 @@
 她从铺子主人身边走过时，他抱着门板停了一下，扭头瞥一眼她的裤子和靴子，再转回去插门板。
-她走到离镜头约两米处停下，左手从裤子左侧的大口袋里掏出剩下的钱，倒进右手掌心攥住，对镜头说话；
-说到 This 时把右手往前递到胸前，掌心朝上、手指微微并拢成一个浅窝、朝镜头这边斜约三十度，四枚钱平躺在掌心窝里：正好 3 枚红铜小钱和 1 枚明显大一圈的金黄大黄铜币，互不重叠；
-她先低头看着钱，说到后半句才抬眼看镜头。
-说完收回手攥起来、叹口气。
-接着她像听见画面左边、镜头身后有人吆喝，转头朝画面左边看，听出那个词有点像 hospitality，眼睛一亮，攥着钱朝画面左边走出画。
-本镜只生成 Riley 自己的两句话；
-那声吆喝是 Fortunata 在 s6_st1 喊的，剪辑时贴进来作画外声。
-道具：钱（p2）进场在 Riley 裤子左侧口袋里（看不见）→ 4.5–6.3 秒左手掏出、倒进右手掌心攥住 → 7.9–12.5 秒右手摊在胸前（正好 3 枚小钱＋1 枚大黄铜币）→ 12.5 秒起攥在右手里，出场仍攥在右手。
+她走到离镜头约两米处停下，左手从裤子左侧的大口袋里掏出剩下的钱，倒进右手掌心攥住，看着镜头说话；
+说到 this… 时把右手往前递到胸前，掌心朝上、手指微微并拢成一个浅窝、朝镜头这边斜约三十度，四枚钱平躺在掌心窝里：正好 3 枚红铜小钱和 1 枚明显大一圈的金黄大黄铜币，互不重叠；
+她低头看着钱说完这半句；
+说到 So. 时收回手攥起来、抬眼看镜头，说完最后一句叹口气。
+接着她像被画面左边、镜头身后的什么动静吸引，转头朝画面左边看，眼睛一亮，攥着钱朝画面左边走出画。
+画面里只有 Riley 开口说话。
+道具：钱（p2）进场在 Riley 裤子左侧口袋里（看不见）→ 4.5–6.3 秒左手掏出、倒进右手掌心攥住 → 11.8–16.2 秒右手摊在胸前（正好 3 枚小钱＋1 枚大黄铜币）→ 16.2 秒起攥在右手里，出场仍攥在右手。
 画面里共 3 个人：Riley、插门板的铺子主人、背对镜头的赶车车夫。
```

- 分镜「走位」改了：

```diff
@@ -3,3 +3,3 @@
 Riley 从街的深处沿左边人行道朝镜头走来（每秒一米出头），约 2 秒从铺子主人身边走过，4.5 秒停在人行道边沿、离镜头约两米、画面左边约四分之一处，面朝镜头；
-14.6 秒起转向画面左边，从镜头左侧走出画（去身后的大车店，下一镜从画面右边进来）。
+20.6 秒起转向画面左边，从镜头左侧走出画（去镜头身后的大车店）。
 货车在路的右半边，0 秒车尾在画面右边、离镜头约七米，一直往街的深处越走越远。
```

- 分镜「节拍」改了：

```diff
@@ -7,8 +7,9 @@
 4.5–6.3秒 她左手伸进裤子左侧的大口袋，掏出剩下的钱，倒进右手掌心，右手攥成拳停在胸前，没人说话；
-6.3–7.5秒 她对镜头说 Sun's going down.；
-7.9–12.5秒 她说 This is what's left of the budget… and still no bed.——说到 This 时右手往前递到胸前，掌心朝上并朝镜头斜约三十度，张开成一个浅窝：正好 3 枚红铜小钱和 1 枚大黄铜币平躺在掌心窝里、互不重叠，停住让人数清；
-前半句她低头看着钱，说到 and still no bed 时抬眼看镜头；
-12.5–13.6秒 她把右手收回胸前攥起来，叹一口气，不说话；
-13.6–14.6秒 她像听见画面左边、镜头身后有人吆喝，转头朝画面左边看，眼睛一亮，嘴闭着（吆喝剪辑时从 s6_st1 贴进来）；
-14.6–17秒 她攥着钱朝画面左边走，约 15.8 秒从画面左边走出画；
+6.3–11.7秒 她右拳攥着钱停在胸前，看着镜头，有点累、自嘲地说 Okay, the sun's going down, I still don't have anywhere to sleep,（6.4–11.6 秒）；
+11.7–16.2秒 她说 and this…（11.8–12.4 秒）——说到 this 时右手往前递到胸前，掌心朝上并朝镜头斜约三十度，张开成一个浅窝：正好 3 枚红铜小钱和 1 枚大黄铜币平躺在掌心窝里、互不重叠，停住让人数清；
+她低头看着钱，停半拍，说 is all the money I have left.（13.0–15.8 秒）；
+16.2–18.4秒 她把右手收回胸前攥起来，抬眼看镜头说 Yeah.（16.3–16.6 秒），停半拍，That's — not ideal.（17.0–18.2 秒）；
+18.4–19.6秒 她叹一口气，不说话；
+19.6–20.6秒 她像被画面左边、镜头身后的什么动静吸引，转头朝画面左边看，眼睛一亮，嘴闭着；
+20.6–23秒 她攥着钱朝画面左边走，约 21.8 秒从画面左边走出画；
 街上只剩越走越远的货车和插门板的铺子主人，不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1 @@
-Riley（有点累、自嘲，美式英语，对镜头）：Sun's going down. This is what's left of the budget… and still no bed.
+Riley（有点累、自嘲，美式英语，对镜头）：Okay, the sun's going down, I still don't have anywhere to sleep, and this… is all the money I have left. Yeah. That's — not ideal.
```


### s6_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/st1_first_frame.png`）
- **I16** [严重·implemented·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；z_s5_st8_right.jpg：驴头和赶车人都朝着镜头走过来，spec 写的是车「直直往
  - 方案：s5_st8 首帧修成车尾朝镜头、往画右拐可读；s4_st3 改「左后方」；s6_st1 墙龛改「在她右后方（画面上在她左边）」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I31** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；放大看（`work/framing_B__a/s5_st8_donkey.jpg`）
  - 方案：s5_st8 首帧修成车尾朝镜头、往街深处走；s5_st6、s6_st1 overhead 照首帧改；s7_st5 overhead 机位升到约 6 m、路人放到约 43 m 外，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/overhead.toml`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I34** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；人物行「画面里看不到任何相机、手机或自拍杆」，而负面词同时列了相机，手
  - 方案：c1/c6/c7 外观正文改正面写法（脖子、耳垂、手腕光着），相机类只留负面词；p1/p2/p5 卡否定句改正面写法；风格行改「眼前是真实的石头、木头、陶土、布料和活生生的人」；v13 全集重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c6_Vibia/c6_Vibia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p1_陶油灯/p1_陶油灯.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p5_油瓶/p5_油瓶.md`、`ai_videos/chuanyue_yiri/workflow.json`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I116** [记录·wontfix·待复核] Prompt 文本·T7·长度与重点：T7·长度与重点：s5_st14 15 秒里 Asellina 8 步以上操作；s8_st2 15 秒数 7 枚钱再付再收；s6_st1/2/3 长达 4471
  - 方案：保留 s5_st14 擦台面、点水两拍和 s8_st2 数钱；固定负面词已去重
- **I117** [记录·implemented·待复核] Prompt 文本·T7 长度与重点／I35去重尾项：T7 长度与重点／I35去重尾项：最长 s6_st1 P为4471字符，未超过5000字；正文“画面”前有2067字符。P负面词里“画面文字、字幕、水印、log
  - 方案：剧级负面词删掉与编译器 BASE_NEGATIVES 重复的「画面文字、字幕、水印、logo、背景音乐」，v13 重编后每份只出现一次；c5 卡的生产备注删掉
  - 改了：`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- 分镜「动作」改了：

```diff
@@ -3,4 +3,4 @@
 车门左边门垛西侧的灰泥墙上有一个小拱形墙龛，龛底平放着一盏点着的小陶油灯（p1：赭红素陶，手掌大、长约十二厘米的圆形扁灯身，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个能勾进一根手指的环形把手；
-整盏是一体的陶），就是待会儿交到 Riley 手里的那一盏，整段都在画面里、一直不动。
-女店主 Fortunata（腰带上只挂一个拳头大的小皮钱袋）刚从车门里出来，站在车门左边门垛前的人行道上，墙龛在她左后方（画面上在她左边、离她约一臂远）；
+整盏是一体的陶），整段都在画面里、一直不动。
+女店主 Fortunata（腰带上只挂一个拳头大的小皮钱袋）刚从车门里出来，站在车门左边门垛前的人行道上，墙龛在她右后方（画面上在她左边、离她约一臂远）；
 她眼睛扫着街上过路的人，右手抬到肩边、手心朝着自己往回招两下（招呼人的手势），朝街上吆喝。
```

- 分镜「走位」改了：

```diff
@@ -1,4 +1,4 @@
-Fortunata 站在车门左边门垛前的人行道上，墙龛在她左后方、伸手够得着；
+Fortunata 站在车门左边门垛前的人行道上，墙龛在她右后方（画面上在她左边）、伸手够得着；
 她先面朝街，3.5 秒起转向画面右边的 Riley。
-Riley 0 秒在画面右边画外，约 3.8 秒从画面右边沿人行道走进来，5 秒停在 Fortunata 右边约一米，两人面对面：Fortunata 在画左、Riley 在画右（本场后面的镜头都保持这个左右，墙龛始终在 Fortunata 的画左一侧）。
+Riley 0 秒在画面右边画外，约 3.8 秒从画面右边沿人行道走进来，5 秒停在 Fortunata 右边约一米，两人面对面：Fortunata 在画左、Riley 在画右，墙龛在 Fortunata 的画左一侧。
 两个行人在人行道外沿的街面上从画左走到画右，约 5.5 秒走出画右。
```


### s6_st2

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/_r3_before/st2_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/st2_first_frame.png`（现行）
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I30** [严重·implemented·待复核] 镜头规格·F2 机位与朝向：F2 机位与朝向 最终 1 分：站位图的机位方向、首帧的视角、文字的「镜头」三者一致；俯视图机位 (6.7,8.7)，离 Riley 1.33 m、离 Fort
  - 方案：s6_st2 照首帧反推 overhead：机位 (5.85,9.0) 看 (5.85,7.2)、aim_h 1.5、约俯 10°，文字写正侧面、离手约 1.8 m；s5_st6 机位贴首帧并加 axis_ok 理由
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I34** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；人物行「画面里看不到任何相机、手机或自拍杆」，而负面词同时列了相机，手
  - 方案：c1/c6/c7 外观正文改正面写法（脖子、耳垂、手腕光着），相机类只留负面词；p1/p2/p5 卡否定句改正面写法；风格行改「眼前是真实的石头、木头、陶土、布料和活生生的人」；v13 全集重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c6_Vibia/c6_Vibia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p1_陶油灯/p1_陶油灯.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p5_油瓶/p5_油瓶.md`、`ai_videos/chuanyue_yiri/workflow.json`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I63** [待核实·implemented·待复核] 时代与世界观·E5 文字：E5 文字：大黄铜币上的立像，放大后笔画像汉字「永」（z_s6st2_coin_big.png）；币是亮金色，看着更像金币，不像 p2 参考图里那种发暗的黄铜；
  - 方案：s6_st2 首帧局部重绘大币立像（照 p2 的持杖立像），颜色压成暗黄铜
- **I98** [记录·planned·待复核] 连续性·连续性·K3：连续性·K3：s6_st2_shirt.jpg：Riley 衬衫前襟、袖子满是凸起的波纹、方格提花图案，看起来像另一件有花纹的衬衫；同场 s6_st5 首帧（s
  - 方案：s6_st2 首帧局部修回素面米白亚麻，ffp 加「素面无花纹亚麻」、负面词加「提花、压纹图案」；s8_st6/st9 视情况处理（未做）
- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-车门口，接上一镜：Fortunata 的右手伸在两人中间、掌心朝上。
+车门口：Fortunata 的右手伸在两人中间、掌心朝上。
 Riley 把攥着钱的右手伸过去摊开，掌心朝上：手心里正好 3 枚红铜小钱和 1 枚明显大一圈的金黄大黄铜币。
```

- 分镜「走位」改了：

```diff
@@ -1,5 +1,5 @@
-两人在车门口面对面，相距约一米：Fortunata 在画左、Riley 在画右（接上一镜）；
+两人在车门口面对面，相距约一米：Fortunata 在画左、Riley 在画右；
 两人伸出的手在画面中间。
 墙龛和那盏灯在 Fortunata 身后左上方。
-镜头在两人侧面偏 Riley 一侧，略高往下俯，离两人的手一米半多。
+镜头在两人正侧面、离两人差不多远，略高往下俯，离两人的手一米八左右。
 配角：Fortunata 一直看着 Riley 的手和脸：3.5–5 秒在想「就这些？
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
-他拍：中景双人，两人腰以上，40mm 镜头感，从两人侧面偏 Riley 一侧拍，机位略高往下俯，离两人的手一米半多，固定机位；
+他拍：中景双人，两人腰以上，40mm 镜头感，从两人正侧面拍，机位略高往下俯，离两人的手一米八左右，固定机位；
 两人伸出的手在画面中间，Fortunata 摊开的手掌朝上，手心里的钱清楚可数；
```


### s6_st5

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st5/planning/st5_first_frame.png`）
- **I12** [严重·implemented·待复核] 人物逻辑·C4 反应拍：C4 反应拍 最终 1 分：配角的反应单独占拍，不被吞掉；反应和身份、性格相符；首帧放大（work/character_B__a/s5st8_zoom2.png
  - 方案：s5_st8 店主在首帧；Asellina 三镜反应拉开：st12 抱胳膊笑、st14 低头擦台面只抬眼一瞥不笑、st7 摇头笑；s6_st5 改为满意点头、嘴角一抿
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I16** [严重·implemented·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；z_s5_st8_right.jpg：驴头和赶车人都朝着镜头走过来，spec 写的是车「直直往
  - 方案：s5_st8 首帧修成车尾朝镜头、往画右拐可读；s4_st3 改「左后方」；s6_st1 墙龛改「在她右后方（画面上在她左边）」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I29** [严重·implemented·待复核] 镜头规格·F1 景别与人物大小：F1 景别与人物大小 最终 1 分：按站位图距离与焦距算出的人物画高，和首帧实测相差不超过约 25%；首帧是一段正对镜头的长柜台，两个男人站在柜台靠镜头这一侧（
  - 方案：s5_st6 保留首帧，overhead 食客挪到柜台长边东段外侧、机位改到柜台东头南约 4 m（食客约 0.7 画高，和首帧一致）；s5_st7 远景按首帧写；s6_st2 机位改正侧面 (5.85,9.0)、aim_h 1.5；s6_st1 机位南移贴首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st2/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I31** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；放大看（`work/framing_B__a/s5_st8_donkey.jpg`）
  - 方案：s5_st8 首帧修成车尾朝镜头、往街深处走；s5_st6、s6_st1 overhead 照首帧改；s7_st5 overhead 机位升到约 6 m、路人放到约 43 m 外，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/overhead.toml`
- **I34** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；人物行「画面里看不到任何相机、手机或自拍杆」，而负面词同时列了相机，手
  - 方案：c1/c6/c7 外观正文改正面写法（脖子、耳垂、手腕光着），相机类只留负面词；p1/p2/p5 卡否定句改正面写法；风格行改「眼前是真实的石头、木头、陶土、布料和活生生的人」；v13 全集重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c6_Vibia/c6_Vibia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p1_陶油灯/p1_陶油灯.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p5_油瓶/p5_油瓶.md`、`ai_videos/chuanyue_yiri/workflow.json`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I98** [记录·planned·待复核] 连续性·连续性·K3：连续性·K3：s6_st2_shirt.jpg：Riley 衬衫前襟、袖子满是凸起的波纹、方格提花图案，看起来像另一件有花纹的衬衫；同场 s6_st5 首帧（s
  - 方案：s6_st2 首帧局部修回素面米白亚麻，ffp 加「素面无花纹亚麻」、负面词加「提花、压纹图案」；s8_st6/st9 视情况处理（未做）
- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-车门口，接上一镜：Fortunata 在画左、Riley 在画右，两人面对面，手里都空着；
+车门口：Fortunata 在画左、Riley 在画右，两人面对面，手里都空着；
 车门左边门垛西侧的墙龛里放着那盏点着的小陶油灯（p1：赭红素陶，手掌大、长约十二厘米的圆形扁灯身，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个能勾进一根手指的环形把手；
@@ -8,3 +8,3 @@
 Riley 顺着看过去，点头笑笑，护着火苗从她身边慢慢走进车门，往院子里去。
-Fortunata 一个人掂了掂腰间的钱袋，摇摇头，嘴角一动，转回去看街。
+Fortunata 一个人掂了掂腰间的钱袋，满意地点一下头，嘴角一抿，转回去看街。
 Fortunata 腰带上只挂一个拳头大的小皮钱袋。
```

- 分镜「走位」改了：

```diff
@@ -2,3 +2,3 @@
 车门在两人身后，院子在门里。
-Fortunata 指的方向是车门里的左后方，和后面石楼梯的位置一致（楼梯在院子西侧，从车门往里看在左边）。
+Fortunata 指的方向是车门里的左后方：石楼梯在院子西侧，从车门往里看在左边。
 8.5 秒起 Riley 从画右走进车门、往院子里慢慢走远（护着火苗，每秒不到一米），到 12 秒还在车门里的院子中，背影越来越小。
```

- 分镜「节拍」改了：

```diff
@@ -10,2 +10,2 @@
 8.5–12秒 Riley 护着火苗从 Fortunata 身边慢慢走进车门，背影往院子里去，越走越小，不说话；
-10–12秒 Fortunata 一个人站在门口，右手掂了掂腰间的小皮钱袋，摇摇头，嘴角动了一下，转回身看街，不说话
+10–12秒 Fortunata 一个人站在门口，右手掂了掂腰间的小皮钱袋，满意地点一下头，嘴角一抿，转回身看街，不说话
```

- 分镜「光线」改了：

```diff
@@ -1,2 +1,2 @@
-日落后的傍晚，天光比上一镜又暗一些：西边天空只剩一点橙色、头顶深蓝紫，天空干净；
+日落后的傍晚，天光又暗了一些：西边天空只剩一点橙色、头顶深蓝紫，天空干净；
 那盏小陶油灯的火苗是画面里最亮的暖光，跟着灯移动，照亮递灯的手和两人的脸；
```


### s6_st6

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st6/planning/st6_first_frame.png`）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I5** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；`work/physics_C__a/s5st8_cart.png`：驴脸正
  - 方案：s5_st8、s6_st3 首帧局部修正驴车结构与朝向；s6_st6 不改图，文字与 overhead 照首帧（楼梯画左、马厩画右），toml note 记下与 bg6 平面图的取舍
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st6/planning/overhead.toml`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I11** [严重·implemented·待复核] 人物逻辑·C3 视线：C3 视线 最终 1 分：每个时刻每个人看向谁，合理（不无缘无故看镜头、不无视身边的怪事）；首帧放大（work/character_B__a/s5st8_zoo
  - 方案：s5_st8 首帧修后画右铺门口店主在场；s6_st6 文字改为第 0 秒门外一步、看画右柜台（放大核对首帧确认看画右）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I13** [严重·implemented·待复核] 人物逻辑·C7 动机连贯：C7 动机连贯 最终 1 分：跨镜头的情绪与动机连得上，没有突然的转变；首帧放大（work/character_B__a/s6st6_zoom.png）：Ril
  - 方案：s6_st6 文字照首帧：门外一步、看画右柜台，加触发「门里传出碗勺声和饭香」；s5_st7 远景两个男人按首帧写，不再声称是 st6 那两人；s5_st8 首帧修正
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I16** [严重·implemented·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；z_s5_st8_right.jpg：驴头和赶车人都朝着镜头走过来，spec 写的是车「直直往
  - 方案：s5_st8 首帧修成车尾朝镜头、往画右拐可读；s4_st3 改「左后方」；s6_st1 墙龛改「在她右后方（画面上在她左边）」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I20** [严重·implemented·待复核] 台词（时长与逻辑）·D6 听得清：D6 听得清 最终 1 分：环境声不盖过台词；悄悄话、远处的话能听清；prompt.txt 第 2 行与末行声音模板无「对白压过环境声」；s8_st1 合唱、s
  - 方案：编译器 v14：有台词的镜头声音行加「对白优先：有人说话时环境声和动作声压低到对白下面，每句台词清楚可辨」（ep01 共 82 处）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I23** [严重·implemented·待复核] 时代与世界观·E3 服饰与发型：E3 服饰与发型 最终 1 分：当地人 tunica/palla、男人刮脸；主持人现代旅行装且无首饰；牵驴的车夫留着修过的短须（z_s5st8_man.png）
  - 方案：c7 卡、s8 文字和 st3/st4/st5/st6/st8/st9 首帧 prompt 的「浴袍」改成「粗亚麻裹身长衣」，剧级负面词加「翻领浴袍，毛巾布浴袍」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I94** [记录·implemented·待复核] 人物逻辑·C2：C2：s6_st5 6–7.5 秒 Fortunata 已指了楼梯，Riley 点头；s6_st6 却先停在大堂门口看一圈，spec 只写「好奇」，没有触发点（
  - 方案：s6_st6 加触发「门里传出碗勺声和饭香」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I95** [记录·planned·待复核] 人物逻辑·C6 路人／R·I20：C6 路人／R·I20：故事稿仍为「车夫们停下来看她的裤子」；当前 spec.md:11–12／视频 prompt 改成近者好奇她和灯、远者喝完顺视线看，之后一
  - 方案：story.md / story.json 大堂一句「车夫们停下来看她的裤子」同步成现行分镜（先后注意她和灯、一人点头一人耸肩）；现在故事稿还没改
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-11
+12
```

- 分镜「动作」改了：

```diff
@@ -7,8 +7,9 @@
 地面是夯土。
-敞开的门口外是已经发暗的蓝紫色院子。
-Riley 右手托着那盏小陶油灯（p1：赭红素陶，手掌大、长约十二厘米的圆形扁灯身，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个能勾进一根手指的环形把手；
-整盏是一体的陶）（右手食指勾着环形把手、掌心托底，左手弯成半圈护着火苗），从院子里走到门口，一脚踏上门槛停下，好奇地探头把屋里看了一圈；
+敞开的门口外是已经发暗的蓝紫色院子：院子的石板地往远处伸，门洞里看得见院子左边一道石楼梯贴着墙往上通到二楼的木栏杆走廊，院子右边是马厩的木栏。
+门里传出碗勺声和饭香。
+Riley 双手在胸前捧着那盏点着的小陶油灯（p1：赭红素陶，手掌大、长约十二厘米的圆形扁灯身，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个能勾进一根手指的环形把手；
+整盏是一体的陶），从院子里朝门口走来，一脚踏上门槛停下，换成右手食指勾环、掌心托底，左手弯成半圈护住火苗，好奇地探头把屋里看了一圈；
 两个车夫先后注意到她，反应各不相同；
-她冲他们点点头，转向镜头小声说一句，然后转向她的左手边，跨出门槛，往画面右边（院子西边的楼梯）走出画。
-道具：油灯（p1）进场、出场都在 Riley 右手里点着，火苗只有灯嘴上一朵；
+她冲他们点点头，转向镜头小声说一句，然后转向她的右手边（画面左边），跨出门槛，朝院子左边的石楼梯走，从门洞左边走出画。
+道具：油灯（p1）进场、出场都在 Riley 手里点着，火苗只有灯嘴上一朵；
 屋里柜台和桌上那两盏是另外的双嘴灯（青铜和灰陶）。
```

- 分镜「走位」改了：

```diff
@@ -1,8 +1,9 @@
-大堂在院子北边，门开在大堂南墙上（楼梯和院里货车之间），门口朝着院子；
-镜头在大堂里面靠北墙处，朝南看着门口。
+镜头在大堂里面靠北墙处，朝南看着敞开的门口。
 两个车夫的长桌在画面左边前景、离镜头一两米，在门口的左边，让开门口；
-柜台在画面右边靠西墙；
-双耳陶罐沿南墙排在门的两边。
-Riley 0 秒已经走到门口、正迈步，前脚踏上门槛，1 秒停住，站在门槛上、画面正中，离镜头约五米，全身入画，面朝屋里；
-8.2 秒起转向她的左手边（画面右边），跨出门槛沿门外往院子西边的楼梯走，约 9.6 秒走出门口、走出画。
+柜台在画面右边；
+双耳陶罐沿门那面墙排在门的两边。
+门洞里的院子：石楼梯在画左一侧沿墙往上，马厩木栏在画右一侧。
+Riley 0 秒在门外院子里、离门槛约一步，正朝门口走来，全身入画，在画面正中，眼睛看着画面右边的柜台；
+1.5 秒前脚踏上门槛停住，站在门槛上、离镜头约五米，面朝屋里；
+9.4 秒起转向她的右手边（画面左边），跨出门槛，朝院子左边的石楼梯走，约 10.8 秒从门洞左边走出画。
 配角：近的车夫 3–4 秒先停住手里的面包抬头看她，在想「哪来的外地女人，还端着灯」；
```

- 分镜「节拍」改了：

```diff
@@ -1,4 +1,5 @@
-0–1.5秒 大堂里两个车夫在吃饭，近的掰面包蘸碗里的豆子糊，远的端杯喝酒；
-Riley 端着灯正走到敞开的门口、前脚踏上门槛，眼睛看着画面右边的柜台，停住，站在门槛上，身后是暗下来的院子，没人说话；
-1.5–3秒 她站在门槛上，右手托灯在胸前、左手护着火苗，探头好奇地把屋里看了一圈：先看画面右边的柜台和嵌在台面里的陶罐，再看门边斜靠的一排双耳陶罐和梁上挂的蒜头，没人说话；
+0–1.5秒 第 0 秒：大堂里两个车夫在吃饭，近的掰面包蘸碗里的豆子糊，远的端杯喝酒，都低着头；
+Riley 在门外院子里、离门槛一步，双手在胸前捧着点着的灯，正朝门口走来，被门里的碗勺声和饭香吸引，眼睛看着画面右边的柜台；
+她走一步，前脚踏上门槛停住，换成右手食指勾环、掌心托底，左手弯成半圈护住火苗，没人说话；
+1.5–3秒 她站在门槛上，探头好奇地把屋里看了一圈：先看画面右边的柜台和嵌在台面里的陶罐，再看门边斜靠的一排双耳陶罐和梁上挂的蒜头，没人说话；
 3–4秒 近的车夫停住手，面包停在碗边，抬头看她；
@@ -8,7 +9,7 @@
 近的车夫回她一个小点头，不说话；
-5.4–7.4秒 她转过脸看镜头，压低声音、觉得好笑地说 Ha — it's a truck stop.；
+5.4–8.6秒 她转过脸看镜头，小声、觉得好笑地说 Oh, this is basically a truck stop.（5.5–8.4 秒）；
 大堂里只有很轻的碗勺声；
-7.4–8.2秒 近的车夫低头接着蘸面包吃；
+8.6–9.4秒 近的车夫低头接着蘸面包吃；
 远的车夫又看了她一眼，耸耸肩，端起杯子喝，不说话；
-8.2–9.6秒 Riley 转向她的左手边（画面右边），护着火苗跨出门槛、沿门外往右走，约 9.6 秒走出门口、走出画，不说话；
-9.6–11秒 门口只剩暗下来的院子，车夫们吃喝，不说话
+9.4–10.8秒 Riley 转向她的右手边（画面左边），护着火苗跨出门槛，朝院子左边的石楼梯走，约 10.8 秒从门洞左边走出画，不说话；
+10.8–12秒 门口只剩暗下来的院子和远处的石楼梯，车夫们吃喝，不说话
```

- 分镜「镜头」改了：

```diff
@@ -1,3 +1,3 @@
 他拍：远景，固定机位，眼平，24mm 广角，在大堂里面靠北墙处朝门口看；
-画面里是整间大堂：左边吃饭的车夫和长桌在前景，右边是柜台，门口在画面正中，Riley 站在门槛上全身入画（约占画高四成多）；
-Riley 两只手都在画面里：右手托灯，左手护火苗。
+画面里是整间大堂：左边吃饭的车夫和长桌在前景，右边是柜台，门口在画面正中，Riley 全身入画（约占画高四成多）；
+Riley 两只手都在画面里：第 0 秒双手捧灯，站定后右手托灯、左手护火苗。
```

- 分镜「台词」改了：

```diff
@@ -1 +1 @@
-Riley（压低声音，觉得好笑，美式英语，对镜头）：Ha — it's a truck stop.
+Riley（小声、觉得好笑，美式英语，对镜头）：Oh, this is basically a truck stop.
```


### s6_st4

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st4/planning/st4_first_frame.png`）
- **I3** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；`s5st8_right.png`：画右横向 70% 处只有阴影里的墙和
  - 方案：s5_st8 首帧局部修：驴在车前、车尾朝镜头，保留画右挂蒜铺门口店主；s5_st14 首帧局部补叠好的抹布在小陶碗旁；st2/st12/st3/st13/st7 勺与抹布按各镜首帧重写，st14 勺进出场位置写清
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st8/planning/st8_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st14/planning/st14_first_frame_prompt.txt`
- **I6** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；`work/physics_C__a/s5st8_cart.png`
  - 方案：s5_st8 首帧修成车尾朝镜头、店主在场；s5_st14 首帧补抹布；s6_st6 第 0 秒文字改为门外一步、看画右柜台；s5_st4 第 0 秒照首帧写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I16** [严重·implemented·待复核] 连续性·K5 站位接续：K5 站位接续 最终 1 分：上一镜结束的位置、朝向接下一镜开始；z_s5_st8_right.jpg：驴头和赶车人都朝着镜头走过来，spec 写的是车「直直往
  - 方案：s5_st8 首帧修成车尾朝镜头、往画右拐可读；s4_st3 改「左后方」；s6_st1 墙龛改「在她右后方（画面上在她左边）」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`
- **I17** [严重·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；z_s6_st6_door.jpg：从大堂朝南往门外看，楼梯在画左、马厩
  - 方案：s6_st6 照首帧写门外院子（楼梯画左、马厩画右），toml note 记与 bg6 平面图的取舍；s5_st8 首帧修正且保留铺面店主；s2_st5/st7 路面只写深灰玄武岩、不写形状；s5_st7 远景按首帧写；s3_st5 写一层面包、st1 写摞成一摞
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I52** [待核实·planned·待复核] 世界物理·世界物理·P5 阶数与排时；R I53：世界物理·P5 阶数与排时；R I53：文本与 overhead 已写十二级、0 秒第三级→2.5 秒第五级→9 秒第十二级。首帧从底至平台沿可见阶面边缘逐级数
  - 方案：在 s6_st4 首帧逐阶编号，按实际级数重排 4.5–9 s，或修图到十二级（本轮未做）
- **I111** [记录·planned·待复核] 时代与世界观·E1·灯（p1 顶面封死）：E1·灯（p1 顶面封死）：她手里的灯是敞口浅盆（z_lamp64.jpg），p1 卡写顶面封死、只有注油孔与灯嘴
  - 方案：s6_st4 首帧的灯局部修成封顶灯面（照 p1），未做

### s6 整场 / 未指明镜头

- **I106** [记录·implemented·待复核] 母语听感·N4 口癖/节奏：N4 口癖/节奏：省略号拖音 8 镜以上；basically 仍有 s8_st1、s5_st5（I97 未改）
  - 方案：v7 全部台词按新听感标准重写，s8_st1 去掉 basically

### s6 整场 / 未指明镜头

- **I112** [记录·planned·待复核] 时代与世界观·E6·出处：E6·出处：卡里把 Petronius Sat. 41 说成「浴场闲聊」；该句出自 Trimalchio 宴会场景
  - 方案：c7 卡与 r05 #21 的出处改成 Petronius Sat. 41（宴席闲谈），台词不动；未做

## s7

### s7_st4

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st4/planning/_r3_before/st4_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st4/planning/st4_first_frame.png`（现行）
- **I8** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；六个镜头 prompt.txt 第 11 行仍写「床头边一张空着的三条腿
  - 方案：bg7 卡正文改中性写法（三条腿小木凳、门板内侧两个木闩座），凳上有无灯、闩座状态由 s7 各镜「画面」行写清；bg7 参考图局部去掉门上横闩；v13 重编后 s7 六镜不再有「空着的小木凳 / 门上有一根木闩」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I44** [主要·implemented·待复核] 世界物理·P5 身体可行：P5 身体可行 最终 1 分：转身、迈步、上台阶、坐下是真人做得到的，时长够；没有 180° 扭头、滑步；0.7 s 内要走两步（约 1.0 s）再转身约 16
  - 方案：s7_st4 文字改「0–1.5 s 跨进屋走两步；1.5–2.2 s 站定转身」，和 overhead 一致；首帧局部修，灯离左前臂一拳
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I74** [记录·implemented·待复核] 世界物理·P4 火：P4 火：st4_hands.png：灯嘴火苗尖离她左前臂只有约 2–3 cm（左臂横过灯后方去扶门框）
  - 方案：s7_st4 首帧局部修，灯离左前臂一拳；文字和 ffp 写「灯嘴朝前、离左前臂一拳」，负面词加「火苗贴着手臂」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st4/planning/st4_first_frame_prompt.txt`
- **I78** [记录·wontfix·待复核] 世界物理·P4；R·I78：P4；R·I78：首帧约 x670–1640、y500–900，床垫与毯子褶纹可清楚辨认，床面上缘有连续冷蓝亮边；文字要求灯照到之前只剩很暗剪影，窗洞冷色只在周
  - 方案：按既有处理记录，出片后看床面亮度
- **I79** [记录·implemented·待复核] 世界物理·P6 距离·火与身体：P6 距离·火与身体：st4_lamp_arm.png：灯嘴尖顶在左前臂上，火苗离前臂不到一指宽；首帧 prompt 第 7 行要求「火苗离她的左前臂一拳远」，
  - 方案：s7_st4 首帧局部修，把灯挪离左前臂
- **I113** [记录·implemented·待复核] 镜头规格·F4 节拍秒数：F4 节拍秒数：文字写「1.5–2.2秒 她往屋里走两步站定，转过身面朝门」，0.7 s 里要走两步再转 180°，太挤。俯视图里 0–1.5 s 就已经从 (
  - 方案：s7_st4 文字改「0–1.5 s 跨进屋走两步；1.5–2.2 s 站定转身」，和俯视图一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I114** [记录·implemented·待复核] 镜头规格·F4 节拍秒数；R·I51：F4 节拍秒数；R·I51：镜长已增至10秒，推门本身2.2–3.6秒有1.4秒，确有改善；但文字仍把“往屋里走两步站定，转过身面朝门”挤在0.7秒内。over
  - 方案：同 I113：两步归进 0–1.5 s，1.5–2.2 s 只转身
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -3,3 +3,3 @@
 靠北墙一张木架床，床头朝西，床框是粗加工的木板，床底是绷紧交叉的绳网，上面铺着鼓鼓的草垫（粗麻布套，缝里露出几根草）和一条深褐色粗羊毛毯；
-床头西侧紧挨床头一张三条腿的小木凳，圆凳面直径约三十厘米；
+床头西侧紧挨床头一张三条腿的小木凳，圆凳面直径约三十厘米，凳面空着；
 床下一只带一个把手的素陶夜壶；
@@ -10,7 +10,6 @@
 Riley 右手托着那盏小陶油灯（p1：赭红素陶，圆形扁灯身，长约十二厘米，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个环形把手；
-整盏是一体的陶）（右手食指勾着环形把手、掌心托底），低头从门洞跨进屋，左手扶着门洞北边的门框；
-进屋后往屋里走两步，站到门板转动够不着的地方，转过身面朝门，用左手抓住她左手边那块门板的外缘往门框一推，门板转过去合上，碰在门框上；
+整盏是一体的陶）（右手食指勾着环形把手、掌心托底），灯嘴朝前、离她的左前臂一拳远，她低头从门洞跨进屋，左手扶着门洞北边的门框，往屋里走两步，站到门板转动够不着的地方，转过身面朝门，用左手抓住她左手边那块门板的外缘往门框一推，门板转过去合上，碰在门框上；
 她再转回身面朝屋里。
 她把灯举高，从西墙往北墙慢慢照过去（只转小半圈），灯光扫过墙上满满的划痕，再落到绳底木床上；
-她转向镜头，笑着小声说一个词。
+她转向镜头，笑着小声说两个词。
 道具：油灯（p1）进场、出场都在 Riley 右手里点着，火苗只有灯嘴上一朵。
```

- 分镜「节拍」改了：

```diff
@@ -1,5 +1,6 @@
-0–1.5秒 门开着约九十度，门板在门洞南边（画面左边边上）；
+0–1.5秒 第 0 秒：门开着约九十度，门板在门洞南边（画面左边边上）；
 Riley 站在门洞里，低着头跨进屋，左手扶着门洞北边的门框；
-右手托着点着的油灯，灯光照出门洞和近处一片墙，屋里其余地方很暗，没人说话；
-1.5–2.2秒 她往屋里走两步站定，转过身面朝门，不说话；
+右手托着点着的油灯，灯嘴朝前、离左前臂一拳远，灯光照出门洞和近处一片墙，屋里其余地方很暗；
+她松开门框，往屋里走两步，没人说话；
+1.5–2.2秒 她站定，转过身面朝门，不说话；
 2.2–3.6秒 她用左手抓住左手边那块门板的外缘，往门框推过去，门板转过去合上，碰在门框上，不说话；
@@ -7,3 +8,3 @@
 4.3–6.3秒 她把灯举到肩高，慢慢从西墙照到北墙（只转小半圈）：灯光扫过墙上满满的划痕，再落到绳底木床上，她跟着灯光看，不说话；
-6.3–7.8秒 她转向镜头，笑着小声说 Cozy.（6.6–7.2秒）；
-7.8–10秒 她把灯放低到胸前，笑着又看了一眼屋里，不说话
+6.3–8秒 她转向镜头，笑着小声说 Okay. Cozy.（6.6–7.9 秒：6.6–7.0 秒 Okay.，停半拍，7.4–7.9 秒 Cozy.）；
+8–10秒 她把灯放低到胸前，笑着又看了一眼屋里，不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1 @@
-Riley（小声，笑，美式英语，对镜头）：Cozy.
+Riley（小声，笑，美式英语，对镜头）：Okay. Cozy.
```


### s7_st6

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st6/planning/_r3_before/st6_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st6/planning/st6_first_frame.png`（现行）
- **I7** [严重·implemented·待复核] 世界物理·P1 手数：P1 手数 最终 1 分：自拍镜只剩一只手可用；每个时刻每只手在干什么、有没有多出或少掉的手；st6_three_arms.png、st6_shoulders.
  - 方案：s7_st6 首帧局部修成只有两条手臂（右手掌托灯、左臂垂身侧）；ffp 写明「只有两条手臂」、负面词加「第三条手臂」；文字照新图（床尾东南角外），toml 起点改 (2.85,1.45)
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st6/planning/st6_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st6/planning/overhead.toml`
- **I8** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；六个镜头 prompt.txt 第 11 行仍写「床头边一张空着的三条腿
  - 方案：bg7 卡正文改中性写法（三条腿小木凳、门板内侧两个木闩座），凳上有无灯、闩座状态由 s7 各镜「画面」行写清；bg7 参考图局部去掉门上横闩；v13 重编后 s7 六镜不再有「空着的小木凳 / 门上有一根木闩」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I9** [严重·implemented·待复核] 世界物理·P8 首帧 = 第 0 秒：P8 首帧 = 第 0 秒 最终 1 分：首帧画的正是第 0 秒的状态，和节拍第一拍接得上；st6_three_arms.png、st6_shoulders.p
  - 方案：同 I7：s7_st6 首帧修成两条手臂，第 0 秒持灯写成与首帧一致的掌托
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st6/planning/st6_first_frame_prompt.txt`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I65** [待核实·implemented·待复核] 镜头规格·F4 节拍秒数（审后改动）：F4 节拍秒数（审后改动）：当前 overhead（19:38 审后修改，注明「r3 照候选首帧」）里 Riley 在 4.3→4.5 秒移动 0.35 m（1
  - 方案：v7 s7_st6 镜长 11→15 s，蹲下 6 s、回头 8 s、站起 13 s，toml 时刻同步；overhead 闸门 0 blocker 0 warning
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st6/planning/overhead.toml`
- **I76** [记录·implemented·待复核] 世界物理·P6 距离：P6 距离：首帧她站在床尾柱（x≈950）外侧，按 overhead 算床尾东南角应在 x≈1294、在她身后；4.5 s 蹲到床边照床底时，她得先往西挪
  - 方案：s7_st6 首帧局部修后照新图写：站在床尾旁、床东南角外，之后朝床边挪半步蹲下；overhead 起点改 (2.85,1.45)
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st6/planning/overhead.toml`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-11
+15
```

- 分镜「动作」改了：

```diff
@@ -3,3 +3,3 @@
 靠北墙一张木架床，床头朝西，床框是粗加工的木板，床底是绷紧交叉的绳网，上面铺着鼓鼓的草垫（粗麻布套，缝里露出几根草）和一条深褐色粗羊毛毯；
-床头西侧紧挨床头一张三条腿的小木凳，圆凳面直径约三十厘米；
+床头西侧紧挨床头一张三条腿的小木凳，圆凳面直径约三十厘米，凳面空着；
 床下一只带一个把手的素陶夜壶；
@@ -9,8 +9,8 @@
 门关着。
-Riley 站在屋子中间、床尾南边，右手托着那盏小陶油灯（p1：赭红素陶，圆形扁灯身，长约十二厘米，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个环形把手；
-整盏是一体的陶）（食指勾着环形把手、掌心托底）。
+Riley 站在床尾旁边、床的东南角外，右手掌心朝上托着那盏小陶油灯（p1：赭红素陶，圆形扁灯身，长约十二厘米，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个环形把手；
+整盏是一体的陶）（手掌和手指从下面托住灯底），左手垂在身侧。
 她把灯举高，照向北墙高处的窗洞：墙上挖出的一个方洞，洞边靠着一块素木挡板，洞里直接是深蓝夜空，夜风让火苗轻轻一斜。
-她回头对镜头说一句。
-接着她蹲下，把灯放低、伸到床边，照向床底：床下的夯土地上放着一只带一个把手的素陶夜壶（灰褐色，口沿有个小缺口，空的）。
-她蹲着回头看镜头，又说一句，自己先笑了，再站起来。
+她回头对镜头一本正经地说一句。
+接着她朝床边挪半步蹲下，把灯放低、伸到床沿下面，照向床底：床下的夯土地上放着一只带一个把手的素陶夜壶（灰褐色，口沿有个小缺口，空的）。
+她蹲着回头看镜头，憋着笑又说一句，再一本正经地连说几个 cool，自己先笑了，再站起来。
 道具：油灯（p1）进场、出场都在 Riley 右手里点着，火苗只有灯嘴上一朵；
```

- 分镜「走位」改了：

```diff
@@ -2,8 +2,8 @@
 门在镜头左后方的画外。
-床斜着在画面中间到右边：床头在画左、紧挨床头的小凳在画面左边边上，床尾在画右；
+床斜着在画面中间：床头在画左、紧挨床头的小凳在画面左边边上，床尾在画面中间偏右；
 窗洞在北墙高处、画面横向正中；
 画面右边露出东墙。
-Riley 在床尾南边，先面朝北墙高处的窗洞（背对镜头偏侧），3 秒回头看镜头；
-4.5 秒蹲在床边，脸朝床底，6.5 秒蹲着回头看镜头；
-9 秒站起来。
+Riley 站在床尾旁边、床的东南角外（画面中间偏右），先面朝北墙高处的窗洞（背对镜头偏侧，看得到侧脸轮廓），3 秒回头看镜头；
+6 秒朝床边挪半步、蹲在床尾旁，脸朝床底，8 秒蹲着回头看镜头；
+13 秒站起来。
 夜壶在床底下中间。
```

- 分镜「节拍」改了：

```diff
@@ -1,7 +1,9 @@
-0–1.5秒 Riley 转向北墙，把右手的灯举到头顶高，照向高处的窗洞，抬头看，没人说话；
+0–1.5秒 第 0 秒：Riley 站在床尾旁边，背对镜头偏侧，右手掌心朝上托着点着的灯，举到头侧高，照向北墙高处的窗洞，抬头看；
+左手垂在身侧；
+没人说话；
 1.5–3秒 灯光照出窗洞：墙上一个方洞，洞边靠着一块素木挡板，洞外深蓝的夜空；
 夜风吹进来，火苗轻轻一斜又立直，她看着窗洞，不说话；
-3–4.5秒 她回头看镜头，一本正经地说 Air conditioning.（3.3–4.3秒）；
-4.5–6.5秒 她把灯放低，屈膝蹲到床边，把灯伸到床沿下面照床底：床下夯土地上一只带把手的素陶夜壶，她看着它，不说话；
-6.5–9秒 她蹲着回头看镜头，憋着笑说 And… that's the bathroom.（6.8–8.8秒），说完自己先笑出声；
-9–11秒 她托着灯站起来，摇摇头笑，不说话
+3–6秒 她回头看镜头，一本正经地说 Oh, and we've got air conditioning.（3.2–5.8 秒）；
+6–8秒 她把灯放低，朝床边挪半步，屈膝蹲到床尾旁，把灯伸到床沿下面照床底：床下夯土地上一只带把手的素陶夜壶，她看着它，不说话；
+8–13秒 她蹲着回头看镜头，憋着笑说 And… that's the bathroom.（8.3–10.4 秒），停半拍，再一本正经地点着头说 Cool. Cool cool cool.（10.8–12.6 秒），说完自己先笑出声；
+13–15秒 她托着灯站起来，摇摇头笑，不说话
```

- 分镜「镜头」改了：

```diff
@@ -3,2 +3,2 @@
 4.5–6.5 秒镜头跟着她的灯轻轻往下摇一点，让床底的夜壶入画；
-Riley 两只手都在画面里：右手托灯，左手空着扶膝。
+Riley 两只手都在画面里：右手托灯，左手先垂在身侧、蹲下时扶膝。
```

- 分镜「台词」改了：

```diff
@@ -1 +1 @@
-Riley（一本正经，再憋着笑，美式英语，对镜头）：Air conditioning. / And… that's the bathroom.
+Riley（一本正经，再憋着笑，美式英语，对镜头）：Oh, and we've got air conditioning. / And… that's the bathroom. Cool. Cool cool cool.
```


### s7_st7

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st7/planning/_r3_before/st7_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st7/planning/st7_first_frame.png`（现行）
- **I8** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；六个镜头 prompt.txt 第 11 行仍写「床头边一张空着的三条腿
  - 方案：bg7 卡正文改中性写法（三条腿小木凳、门板内侧两个木闩座），凳上有无灯、闩座状态由 s7 各镜「画面」行写清；bg7 参考图局部去掉门上横闩；v13 重编后 s7 六镜不再有「空着的小木凳 / 门上有一根木闩」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I18** [严重·implemented·待复核] 台词（时长与逻辑）·D1 说得完：D1 说得完 最终 1 分：每句 ≤2.8 词/秒（停顿另算），开口前 ≥1 秒，说完后 ≥1.5 秒（用脚本算，给数字）；19 词，扣句间 1.0 s 停顿后
  - 方案：全部 Riley 台词按母语听感新标准 v7 重写，镜长按正常语速放宽（全集 708→871 s），各镜说话窗 ≤2.5 词/秒、开口前与说完后留白 ≥1 s；s8_st1 改为 26 词 / 12.7 s（2.0 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I37** [严重·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜 最终 1 分：「本场」「场景」行没有把别的镜头的内容带进来；模型只看到一份 prompt，看不懂 st5、st2、「上一镜」。s6_st3 画面
  - 方案：四场分镜和首帧 prompt 删掉「上一镜 / 下一镜 / 同 stN / 剪辑」类跨镜指代，改成自包含描述；s6_st3 删剪辑备注、写明画面里只有 Riley 开口；c5 卡删开发备注与钥匙说明；v13 送模 prompt 检索跨镜指代 0 处
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c5_Fortunata/c5_Fortunata.md`
- **I73** [记录·implemented·待复核] 世界物理·P4 光影·门缝透光（R·I77 理由不成立）：P4 光影·门缝透光（R·I77 理由不成立）：st7_doorgap_stool.png：门底缝一条亮暖光（原图 x60–310,y820–880）。st7 
  - 方案：s7_st7 首帧局部压暗门底缝；光线行加「门底那条缝是暗的」，ffp 负面词带「门缝透光」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st7/planning/st7_first_frame_prompt.txt`
- **I77** [记录·implemented·待复核] 世界物理·P4；R·I77：P4；R·I77：st7 首帧门底 x45–320、y825–884 有明显暖光条，st1 门底也有细亮缝；室内光线只交代油灯和窗洞冷光，没有交代门外暖光源。`
  - 方案：s7_st7 首帧压暗门底缝，文字写门缝是暗的，负面词带「门缝透光」；v13 重编进送模 prompt
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st7/planning/st7_first_frame_prompt.txt`
- **I80** [记录·implemented·待复核] 世界物理·P4 记录·门缝光（I77 更正）：P4 记录·门缝光（I77 更正）：st7_first_frame_prompt.txt:8 写了「门底下是暗的」，:10 负面词有「门缝透光」，首帧仍画出亮缝
  - 方案：s7_st7 首帧压暗门缝，光线行写门底是暗的；v13 重编送模
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-12
+18
```

- 分镜「动作」改了：

```diff
@@ -3,3 +3,3 @@
 靠北墙一张木架床，床头朝西，床框是粗加工的木板，床底是绷紧交叉的绳网，上面铺着鼓鼓的草垫（粗麻布套，缝里露出几根草）和一条深褐色粗羊毛毯；
-床头西侧紧挨床头一张三条腿的小木凳，圆凳面直径约三十厘米；
+床头西侧紧挨床头一张三条腿的小木凳，圆凳面直径约三十厘米，进场时凳面空着；
 床下一只带一个把手的素陶夜壶；
@@ -14,6 +14,6 @@
 又捏起深褐色粗羊毛毯的一角搓了搓（很扎），放下。
-她直起身看镜头说两句。
+她直起身看镜头说三句：草垫就是一袋草搁在绳子上，毯子扎得很，挺「原生态」。
 然后她转身走到床头的小木凳边，弯腰把灯平放在凳面上（灯底平放、火苗朝上，灯身只有手掌大，平放在凳面上，占凳面直径的四成左右），松手；
 转身坐到床边，舒一口气。
-道具：油灯（p1）进场在 Riley 右手里点着 → 8–10 秒放到床头小凳上，松手 → 出场在小凳上点着；
+道具：油灯（p1）进场在 Riley 右手里点着 → 13.8–15.8 秒放到床头小凳上，松手 → 出场在小凳上点着；
 草垫、绳网、毛毯被她摸过后都回到原样。
```

- 分镜「走位」改了：

```diff
@@ -1,4 +1,4 @@
 Riley 先站在床的南边、靠床头那一段，面朝床（背对镜头偏侧，能看到她的右侧脸），4.5 秒转身面朝镜头；
-8 秒朝画面左边走一小步到小凳旁（床头西南角外），弯腰放灯；
-10 秒转身坐到床的南沿，面朝镜头，位置和下一镜 st1 一样。
+13.8 秒朝画面左边走一小步到小凳旁（床头西南角外），弯腰放灯；
+15.8 秒转身坐到床的南沿、靠床头那一段，面朝镜头。
 门在画面左边边上，小凳和灯在画面左边偏中，床在画面中间到右边，窗洞在右上。
```

- 分镜「节拍」改了：

```diff
@@ -3,4 +3,4 @@
 3.5–4.5秒 她用左手捏起粗毛毯的一角搓了搓，皱一下鼻子，放下，不说话；
-4.5–8秒 她直起身转向镜头，说 Straw mattress. Ropes underneath.（4.8–6.3秒），停半拍，挑眉说 Very… rustic.（6.8–7.9秒）；
-8–10秒 她朝画面左边走一小步到床头的小凳旁，弯腰把灯平放在凳面上，灯底平放、火苗朝上，松手，不说话；
-10–12秒 她转身坐到床边，面朝镜头，舒一口气，两手放到膝上，不说话
+4.5–13.8秒 她直起身转向镜头说（4.8–13.4 秒）：4.8–8.8 秒 So it's literally a bag of straw on some ropes.（说到 straw 时左手朝身后的草垫一指），9.2–11.6 秒 And the blanket is so itchy.（左手手指互相搓一搓，皱一下鼻子），12.1–13.4 秒 挑眉说 Very… rustic.；
+13.8–15.8秒 她朝画面左边走一小步到床头的小凳旁，弯腰把灯平放在凳面上，灯底平放、火苗朝上，松手，不说话；
+15.8–18秒 她转身坐到床边，面朝镜头，舒一口气，两手放到膝上，不说话
```

- 分镜「光线」改了：

```diff
@@ -3,2 +3,3 @@
 墙角和天花板沉在深褐暗影里；
-北墙高处的窗洞里透进一点冷蓝夜色。
+北墙高处的窗洞里透进一点冷蓝夜色；
+门底那条缝是暗的。
```

- 分镜「台词」改了：

```diff
@@ -1 +1 @@
-Riley（看着很满意又有点无奈，美式英语，对镜头）：Straw mattress. Ropes underneath. Very… rustic.
+Riley（看着很满意又有点无奈，美式英语，对镜头）：So it's literally a bag of straw on some ropes. And the blanket is so itchy. Very… rustic.
```


### s7_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st1/planning/st1_first_frame.png`）
- **I8** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；六个镜头 prompt.txt 第 11 行仍写「床头边一张空着的三条腿
  - 方案：bg7 卡正文改中性写法（三条腿小木凳、门板内侧两个木闩座），凳上有无灯、闩座状态由 s7 各镜「画面」行写清；bg7 参考图局部去掉门上横闩；v13 重编后 s7 六镜不再有「空着的小木凳 / 门上有一根木闩」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I34** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；人物行「画面里看不到任何相机、手机或自拍杆」，而负面词同时列了相机，手
  - 方案：c1/c6/c7 外观正文改正面写法（脖子、耳垂、手腕光着），相机类只留负面词；p1/p2/p5 卡否定句改正面写法；风格行改「眼前是真实的石头、木头、陶土、布料和活生生的人」；v13 全集重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c6_Vibia/c6_Vibia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/characters/c7_Helvia/c7_Helvia.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p1_陶油灯/p1_陶油灯.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p5_油瓶/p5_油瓶.md`、`ai_videos/chuanyue_yiri/workflow.json`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I62** [待核实·implemented·待复核] 母语听感·N3·开场任务对应；R·I65/I66/I105：N3·开场任务对应；R·I65/I66/I105：B04：lines.md L94 写 “Mission two: done”，L122 回顾 Bed/Garu
  - 方案：v7 开场改成「two goals today: find somewhere to sleep… and try garum」，回收改 s5_st7「garum — check. Now I just have to find a bed」、s7_st1「I found a bed, I tried the garum」，不再靠编号
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I77** [记录·implemented·待复核] 世界物理·P4；R·I77：P4；R·I77：st7 首帧门底 x45–320、y825–884 有明显暖光条，st1 门底也有细亮缝；室内光线只交代油灯和窗洞冷光，没有交代门外暖光源。`
  - 方案：s7_st7 首帧压暗门底缝，文字写门缝是暗的，负面词带「门缝透光」；v13 重编进送模 prompt
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st7/planning/st7_first_frame_prompt.txt`
- **I98** [记录·planned·待复核] 连续性·连续性·K3：连续性·K3：s6_st2_shirt.jpg：Riley 衬衫前襟、袖子满是凸起的波纹、方格提花图案，看起来像另一件有花纹的衬衫；同场 s6_st5 首帧（s
  - 方案：s6_st2 首帧局部修回素面米白亚麻，ffp 加「素面无花纹亚麻」、负面词加「提花、压纹图案」；s8_st6/st9 视情况处理（未做）
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-9
+13
```

- 分镜「动作」改了：

```diff
@@ -6,6 +6,4 @@
 北墙高处的窗洞在画面右上方。
-她舒一口气，压低声音对镜头一项项说：说 Bed?
-Found. 时拍拍身下的床，说 Garum?
-Tasted. 时点一下头，说 Budget?
-…Gone. 时摊开两只空手、耸耸肩。
+她舒一口气，放松地对镜头随口说：说到 bed 时拍拍身下的床，说到 garum 时点一下头，说到 zero money 时摊开两只空手、耸耸肩，停一拍说 Honestly?
+，再笑着说 Worth it.。
 说完转头越过右肩（靠灯那一侧），看身后墙上的划痕，嘴角上扬。
```

- 分镜「走位」改了：

```diff
@@ -3,3 +3,3 @@
 她身后是北墙。
-7.2 秒起她的头转向画左身后（右肩那边、靠灯的墙）。
-镜头在她正前方偏她右手一侧（西南），比下一镜远一些。
+11.6 秒起她的头转向画左身后（右肩那边、靠灯的墙）。
+镜头在她正前方偏她右手一侧（西南），离她两米多。
```

- 分镜「节拍」改了：

```diff
@@ -1,6 +1,4 @@
 0–1.5秒 Riley 坐在床边，两手放在膝盖上，舒一口气，看着镜头，没人说话；
-1.5–7.2秒 她压低声音对镜头一项项说，每个问句后停半拍再答：1.5–2.0秒 Okay.，2.3–3.6秒 Bed?
-Found.（拍拍身下的床），4.0–5.3秒 Garum?
-Tasted.（点一下头），5.7–7.2秒 Budget?
-…Gone.（摊开两只空手、耸耸肩）；
-7.2–9秒 她转头越过右肩，看身后靠灯那边墙上的划痕，嘴角上扬，不说话
+1.5–11.6秒 她放松地对镜头随口说：1.6–2.0 秒 Okay.，2.4–4.4 秒 So I found a bed,（说到 bed 拍拍身下的床），4.7–6.3 秒 I tried the garum…（说到 garum 点一下头），6.8–9.2 秒 and I have zero money left.（说到 zero money 摊开两只空手、耸耸肩），9.7–10.2 秒 Honestly?
+（停一拍），10.7–11.4 秒 Worth it.（笑）；
+11.6–13秒 她转头越过右肩，看身后靠灯那边墙上的划痕，嘴角上扬，不说话
```

- 分镜「台词」改了：

```diff
@@ -1,6 +1,3 @@
-Riley（压低声音，满足，美式英语，对镜头；
-每个问句后停半拍再答；
-Garum＝GAH-rum，重音在前）：Okay. Bed?
-Found. Garum?
-Tasted. Budget?
-…Gone.
+Riley（放松、满足，美式英语，对镜头；
+Garum＝GAH-rum，重音在前）：Okay. So I found a bed, I tried the garum… and I have zero money left. Honestly?
+Worth it.
```


### s7_st2

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st2/planning/st2_first_frame.png`）
- **I8** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；六个镜头 prompt.txt 第 11 行仍写「床头边一张空着的三条腿
  - 方案：bg7 卡正文改中性写法（三条腿小木凳、门板内侧两个木闩座），凳上有无灯、闩座状态由 s7 各镜「画面」行写清；bg7 参考图局部去掉门上横闩；v13 重编后 s7 六镜不再有「空着的小木凳 / 门上有一根木闩」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I46** [主要·implemented·待复核] 母语听感·N2 别扭原因：N2 别扭原因 最终 1 分：直译句式、电报式、时态或视角、讲解腔、指代不清、生僻词；L36 "His son called it gross — so Dad
  - 方案：v7 重写全部 Riley 台词：s4_st2 改「…held a coin up to his son's nose and went, "Does this smell?"」；s7_st2「…I swear this was in my history textbook…」；s3_st4、s8_st1、s3_st2 一并重写
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-19
+23
```

- 分镜「动作」改了：

```diff
@@ -1,6 +1,6 @@
 Riley 坐在床边，一开始头转向画面左边、她身后靠灯的那面墙，看着灯旁墙上的划痕；
-然后把脸转回来正对镜头，转好之后才开口，轻声讲这里的住客什么墙上都写，再说她最喜欢的一句——这句她上学时在历史课上就读过、背了下来，说到 from history class 时眉毛一扬；
-两个人名放慢，讲到 Two thousand years 时微微一笑；
-说完安静地笑着，垂眼看一眼灯苗。
-她的两手放在膝上，只在说 every wall 时用左手朝四周的墙随手一摆。
+然后把脸转回来正对镜头，转好之后才开口，轻声讲这里的住客什么墙上都写，再说其中一句——她发誓这句她在历史课本上读过，说到 history textbook 时眉毛一扬；
+两个人名放慢，念完说一句「挺甜的」，安静地笑着，垂眼看一眼灯苗。
+她的两手放在膝上，只在说 every wall 时用左手朝四周的墙随手一摆，说到 there's one 时用右手拇指越过右肩朝身后靠灯那面墙一指。
+西墙南段那扇厚木板门关着，门板内侧钉着两个空着的木闩座（在画面外）。
 床头小凳上那盏小陶油灯（p1：赭红素陶，圆形扁灯身，长约十二厘米，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个环形把手；
```

- 分镜「走位」改了：

```diff
@@ -1,4 +1,4 @@
-Riley 坐在床边，位置和上一镜一样；
+Riley 坐在床的南沿、靠床头那一段；
 0–1 秒头朝画面左边、往她身后看（她右肩那边、小凳和灯旁边的那面墙），窗洞在画面右上方、她身后另一侧；
 1–2.2 秒转回正对镜头，之后一直看着镜头。
-镜头在她正前方略偏西南，比上一镜近。
+镜头在她正前方略偏西南，离她一米多。
```

- 分镜「节拍」改了：

```diff
@@ -2,6 +2,6 @@
 1–2.2秒 她慢慢把脸转回来正对镜头，嘴还闭着，带一点笑，不说话；
-2.2–4.6秒 她轻声说 People write on every wall here.，说到 every wall 时左手朝四周的墙随手一摆，再放回膝上；
-5.0–6.9秒 My favorite, from history class:（说到 history class 时眉毛一扬）；
-7.3–12.8秒 "Vibius Restitutus slept here alone… missing his Urbana."（两个人名放慢，alone 后停半拍）；
-13.3–17.3秒 Two thousand years from now, people will still read it.，说到 Two thousand years 时微微一笑；
-17.3–19秒 她安静地笑着，垂眼看一眼床头的灯苗，不说话
+2.2–5.5秒 她轻声说 People write on, like, every wall here.（2.3–5.3 秒），说到 every wall 时左手朝四周的墙随手一摆，再放回膝上；
+5.5–10.7秒 And there's one —（5.7–6.9 秒，说到 there's one 时右手拇指越过右肩朝身后靠灯那面墙一指，再放回膝上），I swear this was in my history textbook —（7.2–10.4 秒，说到 history textbook 时眉毛一扬）；
+10.7–18.4秒 that says,（10.9–11.5 秒），停半拍，"Vibius Restitutus slept here alone, and missed his Urbana."（12.0–18.1 秒，两个人名放慢，alone 后停半拍）；
+18.4–20.8秒 Which is kind of sweet.（18.6–20.6 秒），说完嘴角一扬；
+20.8–23秒 念完她安静地笑着，垂眼看一眼床头的灯苗，不说话
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1,2 @@
 Riley（轻声，温柔，美式英语，对镜头；
-两个人名放慢：Vibius Restitutus＝VIB-ee-us res-tih-TOO-tus，Urbana＝ur-BAH-nah）：People write on every wall here. My favorite, from history class: "Vibius Restitutus slept here alone… missing his Urbana." Two thousand years from now, people will still read it.
+两个人名放慢：Vibius Restitutus＝VIB-ee-us res-tih-TOO-tus，Urbana＝ur-BAH-nah）：People write on, like, every wall here. And there's one — I swear this was in my history textbook — that says, "Vibius Restitutus slept here alone, and missed his Urbana." Which is kind of sweet.
```


### s7_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st3/planning/st3_first_frame.png`）
- **I8** [严重·implemented·待复核] 世界物理·P2 道具来源与去向：P2 道具来源与去向 最终 1 分：每件道具进场时在哪、出场时在哪；没有凭空出现或消失；六个镜头 prompt.txt 第 11 行仍写「床头边一张空着的三条腿
  - 方案：bg7 卡正文改中性写法（三条腿小木凳、门板内侧两个木闩座），凳上有无灯、闩座状态由 s7 各镜「画面」行写清；bg7 参考图局部去掉门上横闩；v13 重编后 s7 六镜不再有「空着的小木凳 / 门上有一根木闩」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I33** [严重·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；人物行「下巴和两腮一层几天没刮的短胡茬」，负面词「大胡子，络腮胡」；
  - 方案：bg7 卡改中性写法、s7 六镜重编；剧级负面词去掉与编译器 BASE_NEGATIVES 重复的五个词；「主持人背包」改「主持人背着双肩包」；s4_st1 首帧 prompt 写下巴短胡茬、两腮干净
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/workflow.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s4/shots/st1/planning/st1_first_frame_prompt.txt`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I53** [待核实·implemented·待复核] 世界物理·P6 距离（文字）：P6 距离（文字）：文字写凳在床头正西、紧挨床头。按床头板顶约 0.85 m、灯苗约 0.52 m 算，撑肘时嘴离灯最近约 0.4 m，做不到「二十多厘米」。首
  - 方案：s7_st3 小凳改写成「床头西南角、紧挨床头板前面」，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I54** [待核实·planned·待复核] 世界物理·P4；R·I54/I55：P4；R·I54/I55：本轮 `materials/shots/s7_*` 只有 spec，没有 sheet4.jpg 或本轮视频。各首帧与 p1 参考图未见
  - 方案：出片后逐帧核 s7_st3 吹灯：右肘支撑、嘴到灯的距离、火灭、没有白烟柱、暖光同步退去
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-12
+15
```

- 分镜「动作」改了：

```diff
@@ -3,4 +3,4 @@
 深褐色粗毛毯盖到胸口，上面那一侧的肩膀和上臂露在毯子外。
-床头西侧小凳上的小陶油灯（p1：赭红素陶，圆形扁灯身，长约十二厘米，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个环形把手；
-整盏是一体的陶）（灯身只有手掌大，平放在凳面上，占凳面直径的四成左右）点着，在她头顶那一侧、和她的头离镜头差不多远，看上去和她的脸差不多大或略小。
+床头西南角、紧挨床头板前面的小凳上，平放着那盏小陶油灯（p1：赭红素陶，圆形扁灯身，长约十二厘米，顶面是一整块封死的浅凹圆面、中间一个小注油孔，前端一个短单嘴，尾部一个环形把手；
+整盏是一体的陶）（灯身只有手掌大，平放在凳面上，占凳面直径的四成左右），点着，在她头顶那一侧、和她的头离镜头差不多远，看上去和她的脸差不多大或略小。
 她轻声道晚安；
@@ -9,4 +9,5 @@
 道具：油灯（p1）进场、出场都在床头小凳上原地；
-9.5 秒前点着，9.5 秒后熄灭；
+12.3 秒前点着，12.3 秒后熄灭；
 毯子进场就盖在她身上，左手捏着毯子边，出场仍盖着。
+西墙南段那扇厚木板门关着，门板内侧钉着两个空着的木闩座（在画面外）。
 画面里只有她一个人。
```

- 分镜「走位」改了：

```diff
@@ -1,2 +1,2 @@
-床靠北墙、床头朝西，小凳和灯在床头正西边（画左）、紧挨床头；
+床靠北墙、床头朝西，小凳和灯在床头西南角、紧挨床头板前面（画左）；
 Riley 右侧朝下侧躺，头在画左靠灯那端，脸朝镜头；
```

- 分镜「节拍」改了：

```diff
@@ -1,5 +1,5 @@
 0–1.5秒 她右侧朝下侧躺着，毯子盖到胸口，左手捏着毯子边拉到下巴，看着镜头，嘴闭着，没人说话；
-1.5–8秒 她轻声对镜头说：1.5–2.8秒 Okay. Bedtime.，3.2–6.0秒 Who knows where I'll wake up tomorrow…，6.4–7.8秒 Goodnight from Pompeii.，说完微微一笑；
-8–9.5秒 她用压在下面的右前臂和右肘把上身撑起一点，侧过脸朝床头的灯凑过去，嘴离灯苗二十多厘米，嘟起嘴轻轻吹一口气，左手仍捏着毯子边，不说话；
-9.5–10.5秒 火苗一下灭了，灯嘴一片黑，屋里暗下去，不说话；
-10.5–12秒 屋里只剩窗洞透进的冷蓝微光，勾出她的头发和肩膀轮廓，她躺回草垫上，不说话
+1.5–10.8秒 她轻声对镜头说：1.6–2.0 秒 Okay.，2.4–3.6 秒 I'm gonna sleep.，4.0–7.8 秒 Honestly, no idea where I'm gonna wake up tomorrow…，8.4–8.7 秒 but —，9.1–10.5 秒 goodnight from Pompeii.，说完微微一笑；
+10.8–12.3秒 她用压在下面的右前臂和右肘把上身撑起一点，侧过脸朝床头的灯凑过去，嘴离灯苗二十多厘米，嘟起嘴轻轻吹一口气，左手仍捏着毯子边，不说话；
+12.3–13.3秒 火苗一下灭了，灯嘴一片黑，屋里暗下去，不说话；
+13.3–15秒 屋里只剩窗洞透进的冷蓝微光，勾出她的头发和肩膀轮廓，她躺回草垫上，不说话
```

- 分镜「台词」改了：

```diff
@@ -1 +1 @@
-Riley（轻声，困了，美式英语，对镜头）：Okay. Bedtime. Who knows where I'll wake up tomorrow… Goodnight from Pompeii.
+Riley（轻声，困了，美式英语，对镜头）：Okay. I'm gonna sleep. Honestly, no idea where I'm gonna wake up tomorrow… but — goodnight from Pompeii.
```


### s7_st5

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/st5_first_frame.png`）
- **I31** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；放大看（`work/framing_B__a/s5_st8_donkey.jpg`）
  - 方案：s5_st8 首帧修成车尾朝镜头、往街深处走；s5_st6、s6_st1 overhead 照首帧改；s7_st5 overhead 机位升到约 6 m、路人放到约 43 m 外，和首帧一致
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s5/shots/st6/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s6/shots/st1/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s7/shots/st5/planning/overhead.toml`
- **I35** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；这三镜没有主角，「要求」行缺「人物按真人自然表演：走路有重心起伏和摆臂……」；
  - 方案：编译器 v14：只有路人（extras）的镜头也带「人物按真人自然表演」句（s2_st3、s5_st6、s7_st5 已核）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg7_大车店客房/bg7_大车店客房.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg3_面包房/bg3_面包房.md`、`projects/ai_video_management/libs/common/episode_workflow.py`
- **I75** [记录·planned·待复核] 世界物理·P6 比例：P6 比例：st5_walker.png：路人身高约 42 px，身后墙上的门洞约 28–30 px 高，人比门高出一半，「走过一两扇门」会像巨人走过小门
  - 方案：s7_st5 overhead 已按 43 m 重算路人（约 52 px）；首帧路人缩小约 1/4 或把门洞画高的局部修图还没做
- 分镜「走位」改了：

```diff
@@ -1,3 +1,3 @@
-镜头在城里一处高屋顶边，朝西南（海湾那边）俯瞰屋顶，开场地平线在画面中间偏上（从上往下约 44%），屋顶占下面一半多；
-窄街斜穿画面中部，端灯的路人从画面中间偏右朝画左走，一直在看得见的街上；
+镜头在城里一处高屋顶边、比下面那条窄街高约六米，朝西南（海湾那边）俯瞰屋顶，开场地平线在画面中间偏上（从上往下约 44%），屋顶占下面一半多；
+窄街斜穿画面中部，端灯的路人在约四十米外的街上，从画面中间偏右朝画左走，一直在看得见的街上；
 5 秒起镜头缓缓上摇，9 秒星空占满画面。
```


### s7 整场 / 未指明镜头

- **I106** [记录·implemented·待复核] 母语听感·N4 口癖/节奏：N4 口癖/节奏：省略号拖音 8 镜以上；basically 仍有 s8_st1、s5_st5（I97 未改）
  - 方案：v7 全部台词按新听感标准重写，s8_st1 去掉 basically

### s7 整场 / 未指明镜头

- **I112** [记录·planned·待复核] 时代与世界观·E6·出处：E6·出处：卡里把 Petronius Sat. 41 说成「浴场闲聊」；该句出自 Trimalchio 宴会场景
  - 方案：c7 卡与 r05 #21 的出处改成 Petronius Sat. 41（宴席闲谈），台词不动；未做

