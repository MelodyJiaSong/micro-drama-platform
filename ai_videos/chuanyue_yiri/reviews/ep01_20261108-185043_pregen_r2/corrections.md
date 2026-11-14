# 修复记录：ep01 · 场一 · 出片前（第 2 次） 第 2 轮 · 11-08 18:50

本轮审查单：`ai_videos/chuanyue_yiri/reviews/ep01_20261108-185043_pregen_r2`；还没开下一轮

问题来源：issues.json

有方案的问题 59 / 59 条；严重 8，主要 3，待核实 12，记录 36；已复核通过 0，复核仍有问题 0，待复核 59；首帧换了 1 镜，分镜文字改了 5 镜。

## s1

### s1_st1

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st1/planning/st1_first_frame.png`）
- **I3** [严重·wontfix·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；st5 资料包 prompt 第 10 行场景（bg2
  - 方案：已改：bg2-2 卡改「两侧略高、中线略低、中线一线积水反光」，st5 文字写中线一线浅浅的流水反光，不再和排水沟矛盾；门楼按文字贴图补进 st5 首帧（见 I9）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I4** [严重·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；bg1 卡第 43 行，种子 prompt 的负面词里有「今天的双峰山，山顶的坑，
  - 方案：bg1–bg13 十三张场景卡种子负面词删掉「今天的双峰山、山顶的坑、冒烟的山」；dossier §5、r05 §5.1、r01 §8/§9 删火山词或注明不进负面词；bg1 山顶改「平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r01_城市与一天.md`
- **I6** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；五镜 prompt 人物段都写「身上没有项链、耳环、手表和任何首饰；画
  - 方案：c1 卡外观改正面写法（脖子、耳垂、手腕都光着），相机、手机、自拍杆只留负面词；bg1-2 写「门口城墙外侧是干净的方石墙面」；bg2-2 写「太阳在镜头身后低低地照过来」；p2 改正面写法；v13 重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`
- **I8** [严重·implemented·待复核] Prompt 文本·T6 参考清单：T6 参考清单 最终 1 分：参考图齐全、顺序与用法说明对得上，没有多余或缺失；第 29 行「画面里它就是这一件，不换成别的样式」，与九枚、三种币的描述相反；有
  - 方案：编译器 v14：道具用法改为「画面里同类道具照它的样子画、不换成别的样式，数量按「画面」写的来」，不再写「画面里它就是这一件」
  - 改了：`projects/ai_video_management/libs/common/episode_workflow.py`
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；st1_gate.png：大拱上方有方形门楼和红瓦两坡顶，st2、st4
  - 方案：选保留门楼：s1_st5 首帧局部修，在门洞正上方补红瓦两坡顶门楼（与 st1/st2/st4 同款），文字和 ffp 写明；bg1 卡补门楼并标 ⚠️ 创作安排；s1_st4 藤筐「两只」改「几只」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/st5_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I18** [待核实·planned·待复核] 台词（时长与逻辑）·D6：D6：previous I39：st1 全景 4.5–5m 低声说话，旧条无台词版转写为空，没有 ASR 验证
  - 方案：出片后对 s1_st1 做无提示转写，逐词核
- **I19** [待核实·planned·待复核] 台词（时长与逻辑）·D6·低声对白实测；R·I39：D6·低声对白实测；R·I39：本轮只提供出片前文字、参考图，没有与当前输入对应的新音轨或 ASR；st1 约 4.5 米全景低声、st3 拱顶蹄声与低声并行。
  - 方案：出片后对 s1_st1/st3/st4 做无提示转写＋人耳核听；v7 已把 s1_st3 改成正常音量
- **I22** [待核实·planned·待复核] 时代与世界观·E5 · 类字母痕（问题 6）：E5 · 类字母痕（问题 6）：st1 神庙三角山墙中部约 x=54%–56%、y=11%–15%，局部放大见近似 S 与 V 的深色钩形/折形痕；st4 与 
  - 方案：核原分辨率山墙纹样；不能确认是装饰，就局部改成清楚的非文字浮雕或素面
- **I23** [待核实·planned·待复核] 时代与世界观·E5 · 神庙山墙类字母刻痕（补强 b 位问题 6）：E5 · 神庙山墙类字母刻痕（补强 b 位问题 6）：原图约 x900–935,y115–135，放大 5 倍后（work/era__judge/st1_ped
  - 方案：同 I22：核山墙「S / V」形刻痕，必要时局部改素面
- **I43** [记录·implemented·待复核] 母语听感·N1 "years back"（对应 I42）：N1 "years back"（对应 I42）：第 8 行 "Almost two thousand years back." 口语里可用，但前面已有 time
  - 方案：v7 s1_st1 重写，不再有 years back
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I48** [记录·wontfix·待复核] 时代与世界观·E1 · 船的形制（上一轮 I45，未改）：E1 · 船的形制（上一轮 I45，未改）：船身是列板上钉成排的铁钉头（work/era__a/st1_boats.png），st4 主船舷边还有一个金属桨架样
  - 方案：记录；以后重出 bg1 时种子 prompt 补平滑拼板、木桨桩
- **I49** [记录·implemented·待复核] 时代与世界观·E4 · 山顶发灰：E4 · 山顶发灰：bg1 底图右侧那座山顶上有一块灰色裸岩（work/era__a/bg1_summit.png），种子 prompt 第 32 行写「山顶平
  - 方案：bg1 卡统一写 Lattari：删「山顶平缓发灰」，改「山顶平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I50** [记录·planned·待复核] 时代与世界观·E5 · 石块上像记号的纹路：E5 · 石块上像记号的纹路：城墙石块面上有一片弯钩、圈形的纹路（work/era__a/st1_wall.png，原图 x560–1000,y250–420）
  - 方案：出片后核城墙石面纹路有没有被画成刻符
- **I51** [记录·wontfix·待复核] 时代与世界观·E1 · 船舷细节（问题 7；I45）：E1 · 船舷细节（问题 7；I45）：st1 右下两船仍有整齐列板与成排钉头；st4 左下船舷小件约 x110、y812，外观近似小金属桨架，但局部只能确认有
  - 方案：保留上轮记录
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-12
+18
```

- 分镜「动作」改了：

```diff
@@ -7,3 +7,3 @@
 衬衫下摆一直塞在裤腰里，海风只吹动她的发梢和短袖的袖口。
-她慢慢转过身来面对镜头，朝镜头迈一步（约半米），停下，眼睛睁得很大，半笑半喘，压低声音说出那句话；
+她慢慢转过身来面对镜头，朝镜头迈一步（约半米），停下，眼睛睁得很大，半笑半喘，小声说出那段话（说到 up there 时眼睛朝画面左上方的城门瞟一下又回到镜头）；
 说完上半身往她的右后方转，右脚跟着往后挪半步，越过右肩回头望一眼画面左上方的城门。
```

- 分镜「走位」改了：

```diff
@@ -4,2 +4,2 @@
 3.5–4.5 秒朝镜头迈一步，停在约四米半处，全身仍在画内、脚离画面下缘还有一点，约占画面高度一半多一点，脸和表情看得清；
-10–12 秒上半身朝她的右后方转，右脚往后挪半步，越过右肩回头望画面左上方的城门。
+15.5–18 秒上半身朝她的右后方转，右脚往后挪半步，越过右肩回头望画面左上方的城门。
```

- 分镜「节拍」改了：

```diff
@@ -4,3 +4,3 @@
 4.5–5.5秒 她站着半笑半喘，还没开口；
-5.5–10秒 她压低声音、半笑半喘地对镜头说那句话（Okay… 之后停半拍）；
-10–12秒 说完她上半身往右后方转、右脚往后挪半步，越过右肩回头望一眼城门，嘴角带着不敢相信的笑，安静
+5.5–15.5秒 她小声、半笑半喘地对镜头说那段话，正常语速：先说 Oh my god. Okay… it worked. It actually worked.（5.6–9.6 秒，Okay… 之后停一下），再说 That's — that's Pompeii up there. Like, real, two-thousand-years-ago Pompeii.（9.8–15.3 秒），说到 up there 时眼睛朝画面左上方的城门瞟一下又回到镜头；
+15.5–18秒 说完她上半身往右后方转、右脚往后挪半步，越过右肩回头望一眼城门，嘴角带着不敢相信的笑，安静
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1,4 @@
-Riley（压低声音、半笑半喘、不敢相信，美式英语；
-吐字清楚，海浪声压在对白下面）：Okay… I just time-traveled. Almost two thousand years back.
+Riley（小声、半笑半喘、不敢相信，美式英语；
+吐字清楚，海浪声压在对白下面；
+Pompeii 读 pom-PAY；
+Okay… 之后、That's — 之后各停一下）：Oh my god. Okay… it worked. It actually worked. That's — that's Pompeii up there. Like, real, two-thousand-years-ago Pompeii.
```


### s1_st2

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st2/planning/st2_first_frame.png`）
- **I3** [严重·wontfix·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；st5 资料包 prompt 第 10 行场景（bg2
  - 方案：已改：bg2-2 卡改「两侧略高、中线略低、中线一线积水反光」，st5 文字写中线一线浅浅的流水反光，不再和排水沟矛盾；门楼按文字贴图补进 st5 首帧（见 I9）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I4** [严重·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；bg1 卡第 43 行，种子 prompt 的负面词里有「今天的双峰山，山顶的坑，
  - 方案：bg1–bg13 十三张场景卡种子负面词删掉「今天的双峰山、山顶的坑、冒烟的山」；dossier §5、r05 §5.1、r01 §8/§9 删火山词或注明不进负面词；bg1 山顶改「平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r01_城市与一天.md`
- **I6** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；五镜 prompt 人物段都写「身上没有项链、耳环、手表和任何首饰；画
  - 方案：c1 卡外观改正面写法（脖子、耳垂、手腕都光着），相机、手机、自拍杆只留负面词；bg1-2 写「门口城墙外侧是干净的方石墙面」；bg2-2 写「太阳在镜头身后低低地照过来」；p2 改正面写法；v13 重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`
- **I7** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；第 57 行「约十几米长」「通道两头都是亮的，……门洞里阴凉、偏暗」；第 58
  - 方案：bg1-2 卡改「约十米长」「进城那头的出口很亮…门洞里阴凉、偏暗」；v13 重编 st3
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`
- **I8** [严重·implemented·待复核] Prompt 文本·T6 参考清单：T6 参考清单 最终 1 分：参考图齐全、顺序与用法说明对得上，没有多余或缺失；第 29 行「画面里它就是这一件，不换成别的样式」，与九枚、三种币的描述相反；有
  - 方案：编译器 v14：道具用法改为「画面里同类道具照它的样子画、不换成别的样式，数量按「画面」写的来」，不再写「画面里它就是这一件」
  - 改了：`projects/ai_video_management/libs/common/episode_workflow.py`
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；st1_gate.png：大拱上方有方形门楼和红瓦两坡顶，st2、st4
  - 方案：选保留门楼：s1_st5 首帧局部修，在门洞正上方补红瓦两坡顶门楼（与 st1/st2/st4 同款），文字和 ffp 写明；bg1 卡补门楼并标 ⚠️ 创作安排；s1_st4 藤筐「两只」改「几只」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/st5_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I10** [主要·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；第 57 行「约十几米长」「通道两头都是亮的，……门洞里阴凉、偏暗」
  - 方案：bg1-2 卡统一为「约十米长」和门洞阴凉；s1_st4 统一「约一米」，绳写「留在他们拉船时站的沙上、绳头仍系在船头」；s1_st3「五六步」改「五六米」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I38** [记录·implemented·待复核] 台词（时长与逻辑）·D1：D1：前两句（9+7 词）合计 16 词放 7s（1.5–8.5）平均 2.29，但各句之间没写停顿；实际句间若各停 0.3s，第一句 4s 内 9 词（含 3
  - 方案：v7 s1_st2 镜长 19→30 s，55 词 / 25.5 s（2.16 词/秒）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st2/planning/overhead.toml`
- **I39** [记录·implemented·待复核] 台词（时长与逻辑）·D1·数字展开与停顿；R·I37：D1·数字展开与停顿；R·I37：Good morning from Pompeii! 为 4 单位，It's May, seventy five A D. 为
  - 方案：同 I38：v7 镜长放宽，停顿有余量
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I40** [记录·planned·待复核] 台词（时长与逻辑）·D6 听得清（st2 漏补对白优先级）：D6 听得清（st2 漏补对白优先级）：s1_st2 prompt:18 台词行无「吐字清楚、浪声压在对白下面」，st1/st3/st4 已补（prompt:1
  - 方案：s1_st2 台词注补「吐字清楚，海浪和风声压在对白下面」，或由编译器对白优先模板统一（v13 还没有）；出片后转写核 seventy-five A-D、garum
- **I42** [记录·implemented·待复核] 母语听感·N1/N2 日期写法与任务编号（对应 I41、I43、I44）：N1/N2 日期写法与任务编号（对应 I41、I43、I44）：第 11 行 "It's May, 75 AD." 英语里 AD 一般写在年份前，"AD 75"
  - 方案：v7 去掉 Mission one / two 编号，改「two goals today」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I45** [记录·implemented·待复核] 母语听感·N2 "this whole town's famous for"：N2 "this whole town's famous for"：第 11 行 "the sauce this whole town's famous for
  - 方案：v7 改「it's this fish sauce everyone here is obsessed with」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I46** [记录·implemented·待复核] 母语听感·N1 / N2 / N4 / R · I43、I44：N1 / N2 / N4 / R · I43、I44：lines.md:11 连续 “Mission one: find a bed before dark.”
  - 方案：v7 去掉编号，改「two goals today: find somewhere to sleep…, and try garum…」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I47** [记录·implemented·待复核] 母语听感·N5 / N3 · I43、I44 的改写会断掉回收：N5 / N3 · I43、I44 的改写会断掉回收：两位审稿人都建议把 lines.md:11 的 "Mission one: … Mission two: 
  - 方案：去掉编号时同步改回收：s5_st7「garum — check」、s7_st1「I found a bed, I tried the garum」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I49** [记录·implemented·待复核] 时代与世界观·E4 · 山顶发灰：E4 · 山顶发灰：bg1 底图右侧那座山顶上有一块灰色裸岩（work/era__a/bg1_summit.png），种子 prompt 第 32 行写「山顶平
  - 方案：bg1 卡统一写 Lattari：删「山顶平缓发灰」，改「山顶平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I56** [记录·implemented·待复核] Prompt 文本·T5 混入别镜：T5 混入别镜：第 35 行「就在上一镜停下的地方」「和上一镜在同一侧」，模型看不到上一镜
  - 方案：s1_st2 删掉两处「上一镜」，直接写站在海边黑沙滩上、城门在她右肩后方
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st2/planning/overhead.toml`
- **I57** [记录·wontfix·待复核] Prompt 文本·T7 长度与重点（R·I50、I55 未改）：T7 长度与重点（R·I50、I55 未改）：st3 画面 967 字、st4 画面 983 字单段，与走位、动作重复；st2 本镜动作到第 1612 字符才出
  - 方案：不动画面行结构
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-19
+30
```

- 分镜「动作」改了：

```diff
@@ -1,2 +1,2 @@
-自拍：Riley 站在同一片沙滩上（就在上一镜停下的地方），面对镜头；
+自拍：Riley 站在海边的黑沙滩上，面对镜头；
 她伸直右臂持镜，镜头就在她手里，在她右前方一臂远。
@@ -4,7 +4,8 @@
 长发披散，海风把几缕吹到脸边。
-身后是陡坡上的城墙、城门和红瓦屋顶：城门在她右肩后方（画面左上），和上一镜在同一侧；
+身后是陡坡上的城墙、城门和红瓦屋顶：城门在她右肩后方（画面左上）；
 神庙脚手架在她头后偏左，城墙和红瓦屋顶从她身后一直延伸到画右。
 她兴奋地报出地点和年份，再报今天的两个目标；
-说到 this whole town 时，用攥着钱的左拳竖起拇指，越过左肩朝身后画右那一片城墙和红瓦屋顶一指，马上收回胸前。
-说 And my budget… 时把攥着钱的左拳举到镜头前，说到 is this 时手心朝上摊开：钱刚摊开时微微叠在一起，接着她用左手拇指把钱拨开两下，红铜色、浅色、金黄三种颜色都看得清，几枚还微微叠着。
+说到 everyone here 时，用攥着钱的左拳竖起拇指，越过左肩朝身后画右那一片城墙和红瓦屋顶一指，马上收回胸前。
+说 And my budget for all of that is… 时把攥着钱的左拳举到镜头前，停半拍，说到 this 时手心朝上摊开：钱刚摊开时微微叠在一起，接着她用左手拇指把钱拨开两下，红铜色、浅色、金黄三种颜色都看得清，几枚还微微叠着；
+她再看着镜头、带点自嘲地说 Yeah. This is it.。
 道具（p2 钱币）：本镜一共 9 枚钱——7 枚红铜色小钱，1 枚明显更小、颜色更浅的小铜币，1 枚金灿灿、比小钱大一圈、更厚更亮的大黄铜币；
```

- 分镜「节拍」改了：

```diff
@@ -1,8 +1,9 @@
 0–1.5秒 她举着右臂对镜头深吸一口气，笑出来，还没开口；
-1.5–5.5秒 说 Good morning from Pompeii!
-It's May, 75 AD.；
-5.5–8.5秒 说 Mission one: find a bed before dark.；
-8.5–13秒 说 Mission two: try garum — the sauce this whole town's famous for.，说到 garum 眼睛一亮，说到 this whole town 时左拳竖起拇指越过左肩朝身后画右的城一指，马上收回胸前；
-13–16秒 说 And my budget… is this.：说 And my budget… 时把攥着钱的左拳举到镜头前，停半拍，说 is this 时手心朝上摊开，钱微微叠在一起；
-16–18秒 她用左手拇指把钱拨开两下，三种颜色都看得清，手心摊着，她看着镜头咧嘴笑，安静；
-18–19秒 她把 9 枚钱重新攥回左拳，手放低出画，海风吹着头发，安静
+1.5–9秒 说 Good morning from Pompeii!
+It's May, 75 AD — which is so weird to say out loud.，说到 so weird to say 时自己笑着轻轻摇一下头；
+9–15秒 说 Okay, so, two goals today: find somewhere to sleep before it gets dark,；
+15–20.5秒 说 and try garum — it's this fish sauce everyone here is obsessed with.，说到 garum 眼睛一亮，说到 everyone here 时左拳竖起拇指越过左肩朝身后画右的城一指，马上收回胸前；
+20.5–25秒 说 And my budget for all of that is… this.：说 And my budget for all of that is… 时把攥着钱的左拳举到镜头前，停半拍，说 this 时手心朝上摊开，钱微微叠在一起；
+25–26.5秒 她用左手拇指把钱拨开两下，三种颜色都看得清，手心摊着，嘴闭着；
+26.5–28.5秒 她看着镜头、带点自嘲地咧嘴笑着说 Yeah. This is it.，手心还摊着；
+28.5–30秒 她把 9 枚钱重新攥回左拳，手放低出画，海风吹着头发，安静
```

- 分镜「台词」改了：

```diff
@@ -3,3 +3,5 @@
 75 AD 读 seventy-five A-D；
-garum 读 GAH-rum，重音在前）：Good morning from Pompeii!
-It's May, 75 AD. Mission one: find a bed before dark. Mission two: try garum — the sauce this whole town's famous for. And my budget… is this.
+garum 读 GAH-rum，重音在前；
+is… 和 this 之间停半拍；
+最后 Yeah. This is it. 带点自嘲）：Good morning from Pompeii!
+It's May, 75 AD — which is so weird to say out loud. Okay, so, two goals today: find somewhere to sleep before it gets dark, and try garum — it's this fish sauce everyone here is obsessed with. And my budget for all of that is… this. Yeah. This is it.
```


### s1_st4

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/st4_first_frame.png`）
- **I1** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；st4_ropes.png：年长渔夫那根绳从船头结斜穿过年轻渔夫胯前、贴着他
  - 方案：s1_st4 年长渔夫挪到靠镜头 0.65 m，绳写成从年轻渔夫腰前斜着绷过去、离身体约一拳；s1_st3 骡子与挑夫按首帧写；s1_st5 驴起点后移到 y 17.5、约 4.5 s 入画
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/st4_first_frame_prompt.txt`
- **I3** [严重·wontfix·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；st5 资料包 prompt 第 10 行场景（bg2
  - 方案：已改：bg2-2 卡改「两侧略高、中线略低、中线一线积水反光」，st5 文字写中线一线浅浅的流水反光，不再和排水沟矛盾；门楼按文字贴图补进 st5 首帧（见 I9）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I4** [严重·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；bg1 卡第 43 行，种子 prompt 的负面词里有「今天的双峰山，山顶的坑，
  - 方案：bg1–bg13 十三张场景卡种子负面词删掉「今天的双峰山、山顶的坑、冒烟的山」；dossier §5、r05 §5.1、r01 §8/§9 删火山词或注明不进负面词；bg1 山顶改「平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r01_城市与一天.md`
- **I5** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；首帧路缘消失线反求（地平线 y≈454，机高约 1.1 m）后量人行道：在约 6.5
  - 方案：s1_st5 用方案①：0–4 s 沿路缘外路面走、绕过斜靠的第二块门板，约 4.4 s 迈上路沿，5 s 停在第一间铺子门口（画面约三成半）；toml 停点 (8.7,8.75)、加门板物件
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/overhead.toml`
- **I8** [严重·implemented·待复核] Prompt 文本·T6 参考清单：T6 参考清单 最终 1 分：参考图齐全、顺序与用法说明对得上，没有多余或缺失；第 29 行「画面里它就是这一件，不换成别的样式」，与九枚、三种币的描述相反；有
  - 方案：编译器 v14：道具用法改为「画面里同类道具照它的样子画、不换成别的样式，数量按「画面」写的来」，不再写「画面里它就是这一件」
  - 改了：`projects/ai_video_management/libs/common/episode_workflow.py`
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；st1_gate.png：大拱上方有方形门楼和红瓦两坡顶，st2、st4
  - 方案：选保留门楼：s1_st5 首帧局部修，在门洞正上方补红瓦两坡顶门楼（与 st1/st2/st4 同款），文字和 ffp 写明；bg1 卡补门楼并标 ⚠️ 创作安排；s1_st4 藤筐「两只」改「几只」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/st5_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I10** [主要·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；第 57 行「约十几米长」「通道两头都是亮的，……门洞里阴凉、偏暗」
  - 方案：bg1-2 卡统一为「约十米长」和门洞阴凉；s1_st4 统一「约一米」，绳写「留在他们拉船时站的沙上、绳头仍系在船头」；s1_st3「五六步」改「五六米」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I15** [待核实·planned·待复核] 人物逻辑·C4 反应拍 / R：C4 反应拍 / R：快照 prompt 第 12 行渔夫离机位约 5.5 米、全身仅占画高约一半；第 13 行以 1 秒“停手、抬眼愣住”起拍。第 15 行补
  - 方案：出片后按正常速度看 s1_st4 「停手→对视→笑着回去干活」是不是一眼看得懂
- **I19** [待核实·planned·待复核] 台词（时长与逻辑）·D6·低声对白实测；R·I39：D6·低声对白实测；R·I39：本轮只提供出片前文字、参考图，没有与当前输入对应的新音轨或 ASR；st1 约 4.5 米全景低声、st3 拱顶蹄声与低声并行。
  - 方案：出片后对 s1_st1/st3/st4 做无提示转写＋人耳核听；v7 已把 s1_st3 改成正常音量
- **I22** [待核实·planned·待复核] 时代与世界观·E5 · 类字母痕（问题 6）：E5 · 类字母痕（问题 6）：st1 神庙三角山墙中部约 x=54%–56%、y=11%–15%，局部放大见近似 S 与 V 的深色钩形/折形痕；st4 与 
  - 方案：核原分辨率山墙纹样；不能确认是装饰，就局部改成清楚的非文字浮雕或素面
- **I23** [待核实·planned·待复核] 时代与世界观·E5 · 神庙山墙类字母刻痕（补强 b 位问题 6）：E5 · 神庙山墙类字母刻痕（补强 b 位问题 6）：原图约 x900–935,y115–135，放大 5 倍后（work/era__judge/st1_ped
  - 方案：同 I22：核山墙「S / V」形刻痕，必要时局部改素面
- **I25** [记录·implemented·待复核] 世界物理·P5 时长：P5 时长：年轻渔夫要走 2.62 m（38.44,54.05→35.9,54.7），年长渔夫 2.23 m，同一拍还要松绳、转身 180°、弯腰；扣掉约 0.
  - 方案：s1_st4 走回船边一拍放宽到 2.5–5.5 s，抬筐 5.5–8 s
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I26** [记录·implemented·待复核] 世界物理·P5 时长 / 动作描述：P5 时长 / 动作描述：两人拉船时面朝船头倒退，走回船边是往前走；prompt「转身走回船边」会诱导模型先转身、再转回来抬筐；2.62 m 加丢绳加弯腰塞在 
  - 方案：同 I25：走回船边一拍放宽到 2.5–5.5 s
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I29** [记录·implemented·待复核] 人物逻辑·C4：C4：年长渔夫目光全程只在鱼上（st4 9–11.7 秒），身边站着穿裤子的高个女人也零反应；挑夫 st3 从头到尾背对。可视为忙，但放在同一场里偏整齐
  - 方案：s1_st4 年长渔夫 9–10 s 斜着瞥她一眼又低头
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I30** [记录·implemented·待复核] 人物逻辑·C6：C6：工人、年轻渔夫都是「愣看脸 → 友善回应 → 低头回去干活」，结构同构，仅点头 / 咧嘴不同
  - 方案：s1_st3 工人改成目光从她的靴子一路抬到她的脸
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- **I31** [记录·planned·待复核] 人物逻辑·C3：C3：st4_overhead.png：Riley (39.1,57.4) 在 0–11.7 秒的朝向线指向北偏西约 20°，几乎背对机位 (38.5,59.5
  - 方案：toml 已把 Riley 回看鱼筐改到 15.5 s；0–11.7 s 朝向和首帧左侧脸是否一致，按 v7 新镜长重出俯视图后再核
- **I36** [记录·implemented·待复核] 台词（时长与逻辑）·D5 说话人（I35 未改）：D5 说话人（I35 未改）：st3、st4 prompt 末行「声音：仅保留本镜指定对白、自然环境声和动作声；不要背景音乐或配乐。」无「除 Riley 外无人
  - 方案：s1_st3、st4 动作行补「挑夫和工人闷声干自己的事 / 两个渔夫闷头干活，只有 Riley 开口说话」，v13 送模已带
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I44** [记录·implemented·待复核] 母语听感·N3 "Future garum" 略隐晦：N3 "Future garum" 略隐晦：第 14 行 观众只在 st2 听过一次 garum，鱼变成 garum 的联系靠画面；不懂的观众可能没接上
  - 方案：v7 改「Those are gonna be garum. That's literally what they make it out of.」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I48** [记录·wontfix·待复核] 时代与世界观·E1 · 船的形制（上一轮 I45，未改）：E1 · 船的形制（上一轮 I45，未改）：船身是列板上钉成排的铁钉头（work/era__a/st1_boats.png），st4 主船舷边还有一个金属桨架样
  - 方案：记录；以后重出 bg1 时种子 prompt 补平滑拼板、木桨桩
- **I49** [记录·implemented·待复核] 时代与世界观·E4 · 山顶发灰：E4 · 山顶发灰：bg1 底图右侧那座山顶上有一块灰色裸岩（work/era__a/bg1_summit.png），种子 prompt 第 32 行写「山顶平
  - 方案：bg1 卡统一写 Lattari：删「山顶平缓发灰」，改「山顶平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I50** [记录·planned·待复核] 时代与世界观·E5 · 石块上像记号的纹路：E5 · 石块上像记号的纹路：城墙石块面上有一片弯钩、圈形的纹路（work/era__a/st1_wall.png，原图 x560–1000,y250–420）
  - 方案：出片后核城墙石面纹路有没有被画成刻符
- **I51** [记录·wontfix·待复核] 时代与世界观·E1 · 船舷细节（问题 7；I45）：E1 · 船舷细节（问题 7；I45）：st1 右下两船仍有整齐列板与成排钉头；st4 左下船舷小件约 x110、y812，外观近似小金属桨架，但局部只能确认有
  - 方案：保留上轮记录
- **I52** [记录·implemented·待复核] 镜头规格·F4 节拍秒数·走回船边偏挤：F4 节拍秒数·走回船边偏挤：年轻渔夫 (38.44,54.05)→(35.9,54.7) 走 2.62 m，年长渔夫走 2.23 m；同一拍还有丢绳、转身、弯
  - 方案：s1_st4 节拍改 2.5–5.5 s，抬筐 5.5–8 s
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I55** [记录·implemented·待复核] Prompt 文本·T4 图文一致：T4 图文一致：overhead_ref 标 Riley「16.5–18s」转回，文字第 15.5 秒起转回看鱼筐
  - 方案：s1_st4 toml 里 Riley 15.5 s 起转回，和文字一致；overhead 重出、shot_pack sync
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I57** [记录·wontfix·待复核] Prompt 文本·T7 长度与重点（R·I50、I55 未改）：T7 长度与重点（R·I50、I55 未改）：st3 画面 967 字、st4 画面 983 字单段，与走位、动作重复；st2 本镜动作到第 1612 字符才出
  - 方案：不动画面行结构
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-18
+23
```

- 分镜「动作」改了：

```diff
@@ -7,6 +7,7 @@
 船头往后一点的船舱里放着一只藤筐，筐沿有两只藤编提耳，筐里装满手指长的银亮小鳀鱼和小沙丁鱼。
-船头的木桩上系着两根绳：年轻的攥一根，年长的攥另一根。
+船头的木桩上系着两根绳：年轻的攥一根，年长的攥另一根；
+年长渔夫那根绳从年轻渔夫的腰前斜着绷过去，离他的身体约一拳。
 两人并排站在船头右边（岸的那一侧）的湿沙上，年轻的在画左、年长的在画右，身子往后仰，咬着牙一把一把往画右拉，边拉边一步步往后倒退约一米，和船头始终隔着一步远，眼睛一直低头看着绳子和船头；
 船往岸上滑了大半米，船底在沙上犁出一道沟。
-接着两人松手，把两根绳子丢在脚边的沙上（绳头仍系在船头，绳子一直留在沙上），转身走回船边，弯下腰：年轻的仍在画左那一边、年长的仍在画右那一边，各用双手抓住藤筐靠自己那一边的提耳，一起把满满一筐小鱼从船里抬起来，越过船舷，抬着往画右横挪两三步，稳稳放到两人中间、比他们靠镜头一点的沙上，筐口朝上，小鱼在筐里蹦跳，鱼鳞反光；
+接着两人松手，把两根绳子丢在他们刚才站的沙上（绳头仍系在船头，绳子一直留在那里），转身走回船边，弯下腰：年轻的仍在画左那一边、年长的仍在画右那一边，各用双手抓住藤筐靠自己那一边的提耳，一起把满满一筐小鱼从船里抬起来，越过船舷，抬着往画右横挪约一米，稳稳放到两人中间、比他们靠镜头一点的沙上，筐口朝上，小鱼在筐里蹦跳，鱼鳞反光；
 两人的左右站位一直保持。
@@ -16,9 +17,11 @@
 他回过神，咧嘴一笑，低头接着和年长的一起拢鱼。
-年长渔夫的目光一直在鱼上：放下筐后蹲在筐边，用手把筐里的鱼拢平。
+年长渔夫放下筐后蹲在筐边，用手把筐里的鱼拢平，只斜着瞥了她一眼，又低头看鱼。
 Riley 站在画面右侧前景，侧身对着镜头、脸朝画左看着他们（镜头看到她的左侧脸）；
-回应完年轻渔夫，她把上半身转向镜头、脚跟着挪半步，把脸凑近镜头，小声说那句话；
+回应完年轻渔夫，她把上半身转向镜头、脚跟着挪半步，把脸凑近镜头，小声说那段话（说 see those little guys?
+时朝身后画左的鱼筐偏一下头）；
 说完回头看那筐鱼，一直看着鱼笑。
 画右、她身后远一点（离镜头约十米）的沙滩上，斜放着两条小木船和一卷麻绳，被她挡住一部分；
-坡上的小路边放着两只空藤筐。
-画面里一共三个人：Riley 和两个渔夫。
+坡上的小路边放着几只空藤筐。
+画面里一共三个人：Riley 和两个渔夫；
+两个渔夫闷头干活，只有 Riley 开口说话。
 Riley 两手空着，钱一直揣在她裤袋里。
```

- 分镜「走位」改了：

```diff
@@ -5,5 +5,5 @@
 Riley 在画面右侧前景，离镜头约两米多，大腿以上，离渔夫约四米。
-5–8 秒两人在船靠镜头的这一侧抬筐，年轻的约在画面一成半、年长的约在三成，抬着往画右横挪约一米；
-鱼筐最后放在两人中间、比他们靠镜头一点的沙上（画面横向约四成、画面下部），两根绳子在他们身后的沙上；
-说 See those tiny fish?
+5.5–8 秒两人在船靠镜头的这一侧抬筐，年轻的约在画面一成半、年长的约在三成，抬着往画右横挪约一米；
+鱼筐最后放在两人中间、比他们靠镜头一点的沙上（画面横向约四成、画面下部），两根绳子留在他们拉船时站的沙上、绳头仍系在船头；
+说 see those little guys?
 时整筐鱼在画内看得见。
@@ -13,3 +13,3 @@
 第 11.7 秒起把上半身转向镜头；
-第 15.5 秒起再转回去看鱼筐。
+第 20.5 秒起再转回去看鱼筐。
 两条小木船在画右、她身后约十米的沙滩上。
```

- 分镜「节拍」改了：

```diff
@@ -1,7 +1,7 @@
 0–2.5秒 两个渔夫各攥一根船头的绳子，边拉边一步步往画右倒退，把小木船往岸上拖了大半米，咬着牙、眼睛一直看着绳子和船，船底在沙上犁出一道沟，浪拍着船尾，Riley 在画右侧身看着；
-2.5–5秒 两人松手把绳子丢在脚边的沙上（绳头仍系在船头），转身走回船边，弯腰；
-5–8秒 年轻的在画左、年长的在画右，各用双手抓住藤筐的提耳，一起把一筐小鱼抬起来越过船舷，往画右横挪两三步，稳稳放到两人中间靠镜头一点的沙上，小鱼在筐里蹦跳；
+2.5–5.5秒 两人松手把绳子丢在他们刚才站的沙上（绳头仍系在船头），转身走回船边，弯腰；
+5.5–8秒 年轻的在画左、年长的在画右，各用双手抓住藤筐的提耳，一起把一筐小鱼抬起来越过船舷，往画右横挪约一米，稳稳放到两人中间靠镜头一点的沙上，小鱼在筐里蹦跳；
 8–9秒 Riley 看见满筐银亮的小鱼，眼睛一亮，微微探身去看，安静；
 9–10秒 年轻渔夫的手停在筐沿上，抬眼愣愣地看了一眼她的脸；
-年长渔夫蹲在筐边低头拢鱼；
+年长渔夫蹲在筐边低头拢鱼，斜着瞥她一眼，又低下头；
 10–10.7秒 Riley 冲年轻渔夫友好地笑一下、轻轻点头；
@@ -9,4 +9,4 @@
 11.7–12.5秒 Riley 把上半身转向镜头、脚跟着挪半步，把脸凑近镜头，还没开口；
-12.5–15.5秒 她小声对镜头说那句话（See those tiny fish?
-之后停半拍，再说 Future garum.）；
-15.5–18秒 她回头看那筐鱼，笑，安静
+12.5–20.5秒 她小声对镜头说那段话，正常语速（12.6–20.3 秒）：说 Okay, see those little guys?
+时朝身后画左的鱼筐偏一下头，再看着镜头说 Those are gonna be garum. That's literally what they make it out of.；
+20.5–23秒 她回头看那筐鱼，笑，安静
```

- 分镜「台词」改了：

```diff
@@ -2,3 +2,3 @@
 吐字清楚，浪声压在对白下面；
-garum 读 GAH-rum，重音在前）：See those tiny fish?
-Future garum.
+garum 读 GAH-rum，重音在前）：Okay, see those little guys?
+Those are gonna be garum. That's literally what they make it out of.
```


### s1_st3

- 首帧没换（`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/st3_first_frame.png`）
- **I1** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；st4_ropes.png：年长渔夫那根绳从船头结斜穿过年轻渔夫胯前、贴着他
  - 方案：s1_st4 年长渔夫挪到靠镜头 0.65 m，绳写成从年轻渔夫腰前斜着绷过去、离身体约一拳；s1_st3 骡子与挑夫按首帧写；s1_st5 驴起点后移到 y 17.5、约 4.5 s 入画
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/st4_first_frame_prompt.txt`
- **I2** [严重·implemented·待复核] 人物逻辑·C7 / 位置：C7 / 位置：st3_first_frame.png：灰浆工人弯腰在大拱右墩与小拱之间的门洞外，不在 spec「大门洞里面、紧贴右侧内壁」；Riley 4–4
  - 方案：s1_st3 工人改成照首帧：大门洞拱口右侧、紧贴右边门墩的墙根下，扛带提梁的小藤筐；toml 同步（工人 (32.6,19.25)）
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- **I3** [严重·wontfix·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；st5 资料包 prompt 第 10 行场景（bg2
  - 方案：已改：bg2-2 卡改「两侧略高、中线略低、中线一线积水反光」，st5 文字写中线一线浅浅的流水反光，不再和排水沟矛盾；门楼按文字贴图补进 st5 首帧（见 I9）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I4** [严重·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；bg1 卡第 43 行，种子 prompt 的负面词里有「今天的双峰山，山顶的坑，
  - 方案：bg1–bg13 十三张场景卡种子负面词删掉「今天的双峰山、山顶的坑、冒烟的山」；dossier §5、r05 §5.1、r01 §8/§9 删火山词或注明不进负面词；bg1 山顶改「平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r01_城市与一天.md`
- **I5** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；首帧路缘消失线反求（地平线 y≈454，机高约 1.1 m）后量人行道：在约 6.5
  - 方案：s1_st5 用方案①：0–4 s 沿路缘外路面走、绕过斜靠的第二块门板，约 4.4 s 迈上路沿，5 s 停在第一间铺子门口（画面约三成半）；toml 停点 (8.7,8.75)、加门板物件
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/overhead.toml`
- **I6** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；五镜 prompt 人物段都写「身上没有项链、耳环、手表和任何首饰；画
  - 方案：c1 卡外观改正面写法（脖子、耳垂、手腕都光着），相机、手机、自拍杆只留负面词；bg1-2 写「门口城墙外侧是干净的方石墙面」；bg2-2 写「太阳在镜头身后低低地照过来」；p2 改正面写法；v13 重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`
- **I7** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；第 57 行「约十几米长」「通道两头都是亮的，……门洞里阴凉、偏暗」；第 58
  - 方案：bg1-2 卡改「约十米长」「进城那头的出口很亮…门洞里阴凉、偏暗」；v13 重编 st3
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`
- **I8** [严重·implemented·待复核] Prompt 文本·T6 参考清单：T6 参考清单 最终 1 分：参考图齐全、顺序与用法说明对得上，没有多余或缺失；第 29 行「画面里它就是这一件，不换成别的样式」，与九枚、三种币的描述相反；有
  - 方案：编译器 v14：道具用法改为「画面里同类道具照它的样子画、不换成别的样式，数量按「画面」写的来」，不再写「画面里它就是这一件」
  - 改了：`projects/ai_video_management/libs/common/episode_workflow.py`
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；st1_gate.png：大拱上方有方形门楼和红瓦两坡顶，st2、st4
  - 方案：选保留门楼：s1_st5 首帧局部修，在门洞正上方补红瓦两坡顶门楼（与 st1/st2/st4 同款），文字和 ffp 写明；bg1 卡补门楼并标 ⚠️ 创作安排；s1_st4 藤筐「两只」改「几只」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/st5_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I10** [主要·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；第 57 行「约十几米长」「通道两头都是亮的，……门洞里阴凉、偏暗」
  - 方案：bg1-2 卡统一为「约十米长」和门洞阴凉；s1_st4 统一「约一米」，绳写「留在他们拉船时站的沙上、绳头仍系在船头」；s1_st3「五六步」改「五六米」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I12** [待核实·implemented·待复核] 世界物理·P4 / P8 灰浆装量与内衬：P4 / P8 灰浆装量与内衬：work/physics__a/st3_basket.png：深灰、平整的灰浆面离筐沿约 1–2 cm（后壁内壁只露一条细带），
  - 方案：s1_st3 文字照首帧写带提梁的小藤筐、大半筐稠灰浆（离筐沿约两指），右手抓提梁、左手托筐底；ffp 负面词改「溢出筐沿的灰浆」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/st3_first_frame_prompt.txt`
- **I13** [待核实·planned·待复核] 世界物理·P2 / P8；R：P2 / P8；R：st3_first_frame.png 原图 1672×941：挑夫右手约 (803,551)，绳下弯后在约 (866,535)、骡子左侧驮
  - 方案：文字已写「牵绳往前通到笼头」；出片后核牵绳是否连续接到笼头，接不上再局部修首帧
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I16** [待核实·planned·待复核] 人物逻辑·其他·连贯：其他·连贯：st3 快照 prompt 第 12 行：挑夫和骡子第 10 秒走出城里那头的出口，「顺着街往前，到第 14 秒还在画里」；Riley 还要走约 9
  - 方案：v7 s1_st3 挑夫骡子路径延到 18 s、全程在画；st5 开场街上只有 Riley，靠剪辑省略时间，出片后用 st3 尾帧和 st5 首秒核实
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- **I17** [待核实·planned·待复核] 连续性·K5 · I18 挑夫与骡子接续：K5 · I18 挑夫与骡子接续：st3 spec:11 规定骡子第 14 秒仍在街上；st5 spec:10 规定开场街上只有 Riley。st3 overh
  - 方案：同 I16：出片后用 st3 尾帧和 st5 首秒核骡子去向，真露在画内才补出画或调剪接
- **I19** [待核实·planned·待复核] 台词（时长与逻辑）·D6·低声对白实测；R·I39：D6·低声对白实测；R·I39：本轮只提供出片前文字、参考图，没有与当前输入对应的新音轨或 ASR；st1 约 4.5 米全景低声、st3 拱顶蹄声与低声并行。
  - 方案：出片后对 s1_st1/st3/st4 做无提示转写＋人耳核听；v7 已把 s1_st3 改成正常音量
- **I24** [记录·implemented·待复核] 世界物理·P2 / P8 牵绳与挑夫位置：P2 / P8 牵绳与挑夫位置：st3_mule.png：挑夫和骡子后半身齐平（脚 y≈667、骡后蹄 y≈683），不在骡子头左侧；牵绳从右手往右前方垂成弧，
  - 方案：s1_st3 文字改「挑夫走在骡子左侧、和后半身差不多齐，牵绳往前通到笼头」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I29** [记录·implemented·待复核] 人物逻辑·C4：C4：年长渔夫目光全程只在鱼上（st4 9–11.7 秒），身边站着穿裤子的高个女人也零反应；挑夫 st3 从头到尾背对。可视为忙，但放在同一场里偏整齐
  - 方案：s1_st4 年长渔夫 9–10 s 斜着瞥她一眼又低头
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I30** [记录·implemented·待复核] 人物逻辑·C6：C6：工人、年轻渔夫都是「愣看脸 → 友善回应 → 低头回去干活」，结构同构，仅点头 / 咧嘴不同
  - 方案：s1_st3 工人改成目光从她的靴子一路抬到她的脸
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- **I36** [记录·implemented·待复核] 台词（时长与逻辑）·D5 说话人（I35 未改）：D5 说话人（I35 未改）：st3、st4 prompt 末行「声音：仅保留本镜指定对白、自然环境声和动作声；不要背景音乐或配乐。」无「除 Riley 外无人
  - 方案：s1_st3、st4 动作行补「挑夫和工人闷声干自己的事 / 两个渔夫闷头干活，只有 Riley 开口说话」，v13 送模已带
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I37** [记录·implemented·待复核] 台词（时长与逻辑）·D1：D1：12 词/5s=2.4 词/秒，两句间未写停顿；说完恰留 1.5s，无余量；悄悄话略慢则压缩到 <1.5s
  - 方案：v7 s1_st3 镜长 14→18 s，20 词 / 9 s（2.2 词/秒），前后留白 1 s / 1.5 s
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- **I41** [记录·implemented·待复核] 母语听感·N2 讲解腔（对应 I40）：N2 讲解腔（对应 I40）：第 17 行 "They had a huge earthquake twelve years ago. They're stil
  - 方案：v7 改「There was this huge earthquake here, like, twelve years ago — and they're still patching it up.」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/story.md`、`ai_videos/chuanyue_yiri/episodes/ep01/story.json`
- **I53** [记录·implemented·待复核] 镜头规格·F4 节拍秒数·工人出画时刻：F4 节拍秒数·工人出画时刻：机位 y=27−1.108t，工人在 (32.3,18.6)；要出 28 mm 半视角 32.7°，需要 cam_y<20.62，
  - 方案：s1_st3 工人挪到 (32.6,19.25)，按 28 mm 算 5.1–5.4 s 出画，文字写约第 5.5 秒从画右边缘出画
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- **I54** [记录·implemented·待复核] 镜头规格·F4 · 工人出画完成点（B04）：F4 · 工人出画完成点（B04）：相机按两路点线性前移，y=27−7.2t/6.5；工人在 (32.3,18.6)。28 mm 横向半视角约 32.7°。工人
  - 方案：同 I53：工人出画时间和文字对齐
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- 分镜「时长」改了：

```diff
@@ -1 +1 @@
-14
+18
```

- 分镜「动作」改了：

```diff
@@ -4,3 +4,3 @@
 两壁几道旧裂缝刚用新灰浆补过，补痕比石头颜色浅。
-一个挑夫牵着一头驮着两只藤筐的骡子走在前面五六步，刚走到大门洞口：挑夫走在骡子头的左侧，右手攥着一根牵绳，牵绳从他手里松松地连到骡子的笼头上；
+一个挑夫牵着一头驮着两只藤筐的骡子走在前面五六米，刚走到大门洞口：挑夫走在骡子的左侧、和骡子的后半身差不多齐，右手攥着一根牵绳，牵绳从他手里往前松松地通到骡子的笼头上；
 他背对镜头往前走，偶尔侧头看一眼骡子（普通路人，只顾赶路；
@@ -8,21 +8,24 @@
 Riley 跟在后面，长发披散在背上。
-一个工人在大门洞里面、紧贴右侧内壁的墙根下（就在拱口里面半步；
-旁边的小门洞空着）：普通路人，忙着手里的活；
+一个工人在大门洞拱口的右侧、紧贴右边门墩的墙根下（就在拱口线上；
+更右边的小门洞空着）：普通路人，忙着手里的活；
 卷发，脸刮得干净，穿沾着灰浆点的短 tunica。
-他脚边是一只小藤筐（筐口约一拃半宽），筐里垫着粗麻布，装着半筐稠稠的灰色灰浆，灰浆面离筐沿还有一掌深。
-他弯腰两手抓住筐沿，把筐提起来扛上右肩，右手扶住肩上的筐沿，左手垂下。
-他扛好筐直起腰，一抬眼看见走近的 Riley，愣住了：高个子、长发披散、一张陌生的外地面孔，他盯着她的脸，站定了；
-他的视线落在走近的她脸上。
-Riley 从他身旁约一米半处走过（他在她右手边），走近时咧嘴一笑，抬起右手两指在眉边轻轻一挥打个招呼；
-他简短地冲她点一下头回礼，目光转回肩上的筐，扛着筐站在原地，随着镜头往前从画右出画。
+他脚边是一只带提梁的小藤筐（筐口约一拃半宽），装着大半筐深灰色的灰浆，灰浆稠得像湿泥，灰浆面离筐沿约两指。
+他弯腰，右手抓住提梁、左手托住筐底，把筐提起来扛上右肩，右手扶住肩上的筐沿，左手垂下；
+稠灰浆稳稳粘在筐里。
+他扛好筐直起腰，一抬眼看见走近的 Riley，愣住了：高个子、长发披散、一张陌生的外地面孔，他的目光从她的靴子一路往上抬到她的脸，像在量这个外地女人有多高，站定了。
+Riley 从他身旁约两米处走过（他在她右手边），走近时咧嘴一笑，抬起右手两指在眉边轻轻一挥打个招呼；
+他简短地冲她点一下头回礼，目光转回肩上的筐，扛着筐站在原地；
+镜头往前走，约第 5.5 秒他从画右边缘出画。
 约第 5 秒 Riley 走到门洞口，走进拱顶下，抬头看了一眼墙上新补的裂缝，放慢脚步，停下；
 门洞里阴凉，骡蹄声在拱顶下回响；
-她像想起什么，转身面对镜头，眉毛一扬，压低声音说悄悄话；
+她像想起什么，转身面对镜头，眉毛一扬，用正常音量对镜头讲（说 See all these cracks?
+时右手朝身旁画左那面拱壁上新补的裂缝一指，马上放下）；
 这时挑夫牵着骡子沿通道一直往前走，走出城里那头的亮处，顺着街越走越小，一直留在画里。
 说完她笑着眨眨眼，转身继续往亮处走。
-画面里一共三个人和一头骡子：Riley、挑夫、扛灰浆筐的工人。
-Riley 两手空着（打招呼时只抬一下右手），钱一直揣在她裤袋里。
+画面里一共三个人和一头骡子：Riley、挑夫、扛灰浆筐的工人；
+挑夫和工人闷声干自己的事，只有 Riley 开口说话。
+Riley 两手空着（打招呼和指裂缝时各抬一下右手），钱一直揣在她裤袋里。
 第 0 秒：Riley 在画面中间偏左背对镜头往大门洞走，离门洞口约五米半；
-骡子在她前面五六步、刚走到大门洞口，挑夫在骡子头左边，背对镜头，右手的牵绳连着骡子的笼头；
-大门洞里面紧贴右侧内壁的墙根下，工人正弯腰两手抓着地上那只小灰浆藤筐的筐沿，低头看着筐；
+骡子在她前面五六米、刚走到大门洞口，挑夫在骡子左侧，背对镜头，右手的牵绳连着骡子的笼头；
+大门洞拱口右侧、紧贴右边门墩的墙根下，工人正弯腰，右手抓着地上那只小灰浆藤筐的提梁、左手扶着筐沿，低头看着筐；
 小门洞空着。
```

- 分镜「走位」改了：

```diff
@@ -1,4 +1,5 @@
 镜头在 Riley 身后约两米半，略低于她的肩、略仰，跟着她往大门洞里走；
-骡子和挑夫在她前方五六步，沿通道中线往前走；
-工人在大门洞拱口里面约半步、紧贴右侧内壁的墙根下，在 Riley 的右手边，她从他身旁约一米半处走过。
+骡子和挑夫在她前方五六米，沿通道中线往前走；
+工人在大门洞拱口右侧、紧贴右边门墩的墙根下，在 Riley 的右手边，她从他身旁约两米处走过；
+镜头往前跟，约第 5.5 秒他从画右边缘出画。
 约第 5 秒 Riley 走到门洞口；
@@ -6,3 +7,3 @@
 6.5–7.5 秒她原地转身面向镜头；
-第 12.5 秒起她转回去，背对镜头朝门洞城里那头的亮处走。
-挑夫和骡子一直沿通道往前走，第 10 秒走出城里那头的出口，继续顺着街往前，到第 14 秒还在画里，越走越小。
+第 16.5 秒起她转回去，背对镜头朝门洞城里那头的亮处走。
+挑夫和骡子一直沿通道往前走，第 10 秒走出城里那头的出口，继续顺着街往前，到第 18 秒还在画里，越走越小。
```

- 分镜「节拍」改了：

```diff
@@ -1,9 +1,10 @@
 0–3秒 Riley 背对镜头，跟着前面的挑夫和骡子走向大门洞，骡蹄声越来越响；
-大门洞里面右侧墙根下，工人弯腰两手提起那只半筐灰浆的小藤筐，扛上右肩，右手扶住筐沿；
-3–4秒 工人扛着筐直起腰，看见走近的 Riley，愣住，盯着她这张陌生的外地面孔；
+拱口右侧的墙根下，工人弯腰，右手抓住提梁、左手托住筐底，提起那只灰浆小藤筐，扛上右肩，右手扶住筐沿；
+3–4秒 工人扛着筐直起腰，看见走近的 Riley，愣住，目光从她的靴子一路抬到她的脸；
 4–4.8秒 Riley 走近他，咧嘴一笑，右手两指在眉边轻轻一挥打招呼；
-4.8–5.6秒 工人简短地点一下头回礼，目光转回肩上的筐，站在原地，随着镜头往前从画右出画；
-5.6–6.5秒 Riley 走进拱顶下，抬头看了一眼墙上新补的裂缝，放慢脚步，停下；
+4.8–5.6秒 工人简短地点一下头回礼，目光转回肩上的筐，站在原地；
+5.6–6.5秒 镜头往前走，工人从画右边缘出画，Riley 走进拱顶下，抬头看了一眼墙上新补的裂缝，放慢脚步，停下；
 6.5–7.5秒 她像想起什么，原地转身面对镜头，眉毛一扬，还没开口；
-7.5–12.5秒 她压低声音对镜头说那句话（这期间她身后的挑夫牵着骡子走出城里那头的亮处，顺着街越走越小）；
-12.5–14秒 说完她笑着眨眨眼，转身背对镜头继续往亮处走，安静
+7.5–16.5秒 她用正常音量对镜头说那段话，正常语速（7.6–16.3 秒）：说 See all these cracks?
+时右手朝身旁画左那面拱壁上新补的裂缝一指，马上放下，再说 There was this huge earthquake here, like, twelve years ago — and they're still patching it up.（这期间她身后的挑夫牵着骡子走出城里那头的亮处，顺着街越走越小）；
+16.5–18秒 说完她笑着眨眨眼，转身背对镜头继续往亮处走，安静
```

- 分镜「镜头」改了：

```diff
@@ -1,2 +1,2 @@
-他拍，跟拍：镜头在她身后约两米半、略低于她的肩、略仰，平稳向前跟，开场是她膝盖以上的背影（中全景），在画面中间偏左，前方看得见骡子、挑夫、大门洞的门框和整条通道（拱顶贴着画面上缘）、门洞里右侧墙根下的工人；
+他拍，跟拍：镜头在她身后约两米半、略低于她的肩、略仰，平稳向前跟，开场是她膝盖以上的背影（中全景），在画面中间偏左，前方看得见骡子、挑夫、大门洞的门框和整条通道（拱顶贴着画面上缘）、拱口右侧墙根下的工人；
 第 6.5 秒她停步转身时镜头也停在门洞口，离她约两米，她成大腿以上的中景；
```

- 分镜「台词」改了：

```diff
@@ -1,2 +1,3 @@
-Riley（压低声音、像说悄悄话，美式英语；
-吐字清楚，骡蹄的回声压在对白下面）：They had a huge earthquake twelve years ago. They're still fixing it.
+Riley（正常音量、像随口讲个冷知识，美式英语；
+吐字清楚，骡蹄的回声压在对白下面）：See all these cracks?
+There was this huge earthquake here, like, twelve years ago — and they're still patching it up.
```


### s1_st5

- 首帧：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/_r3_before/st5_first_frame.png`（_r3_before）→ `ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/st5_first_frame.png`（现行）
- **I1** [严重·implemented·待复核] 世界物理·P6 穿模与距离：P6 穿模与距离 最终 1 分：人、动物、道具之间的距离够，走位路线不穿墙、不撞人；st4_ropes.png：年长渔夫那根绳从船头结斜穿过年轻渔夫胯前、贴着他
  - 方案：s1_st4 年长渔夫挪到靠镜头 0.65 m，绳写成从年轻渔夫腰前斜着绷过去、离身体约一拳；s1_st3 骡子与挑夫按首帧写；s1_st5 驴起点后移到 y 17.5、约 4.5 s 入画
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/overhead.toml`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/st4_first_frame_prompt.txt`
- **I3** [严重·wontfix·待复核] 时代与世界观·E2 建筑与材质：E2 建筑与材质 最终 1 分：抹灰、红瓦、玄武岩石板、凝灰岩；没有城垛、百叶窗、玻璃格窗、托斯卡纳农舍；st5 资料包 prompt 第 10 行场景（bg2
  - 方案：已改：bg2-2 卡改「两侧略高、中线略低、中线一线积水反光」，st5 文字写中线一线浅浅的流水反光，不再和排水沟矛盾；门楼按文字贴图补进 st5 首帧（见 I9）
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I4** [严重·implemented·待复核] 时代与世界观·E7 规则源：E7 规则源 最终 1 分：场景卡、道具卡、考据负面词里没有和以上冲突的写法；bg1 卡第 43 行，种子 prompt 的负面词里有「今天的双峰山，山顶的坑，
  - 方案：bg1–bg13 十三张场景卡种子负面词删掉「今天的双峰山、山顶的坑、冒烟的山」；dossier §5、r05 §5.1、r01 §8/§9 删火山词或注明不进负面词；bg1 山顶改「平缓圆润、长满灌木和草」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/dossier.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r05_衣着语言黑名单.md`、`ai_videos/chuanyue_yiri/episodes/ep01/0_research/parts/r01_城市与一天.md`
- **I5** [严重·implemented·待复核] 镜头规格·F3 画面位置：F3 画面位置 最终 1 分：人和关键道具在画面里的左右上下位置，三处一致；首帧路缘消失线反求（地平线 y≈454，机高约 1.1 m）后量人行道：在约 6.5
  - 方案：s1_st5 用方案①：0–4 s 沿路缘外路面走、绕过斜靠的第二块门板，约 4.4 s 迈上路沿，5 s 停在第一间铺子门口（画面约三成半）；toml 停点 (8.7,8.75)、加门板物件
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/overhead.toml`
- **I6** [严重·implemented·待复核] Prompt 文本·T2 否定句：T2 否定句 最终 1 分：正文里没有「没有 X」「看不到 X」这类会招来 X 的否定句；五镜 prompt 人物段都写「身上没有项链、耳环、手表和任何首饰；画
  - 方案：c1 卡外观改正面写法（脖子、耳垂、手腕都光着），相机、手机、自拍杆只留负面词；bg1-2 写「门口城墙外侧是干净的方石墙面」；bg2-2 写「太阳在镜头身后低低地照过来」；p2 改正面写法；v13 重编
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/characters/c1_Riley/c1_Riley.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg2_石板街/bg2-2_海门内回望/bg2-2_海门内回望.md`、`ai_videos/chuanyue_yiri/2_世界观人设/props/p2_钱币/p2_钱币.md`
- **I7** [严重·implemented·待复核] Prompt 文本·T3 过期描述：T3 过期描述 最终 1 分：人物、场景、道具描述是现行版本（发色、造型、卡片）；第 57 行「约十几米长」「通道两头都是亮的，……门洞里阴凉、偏暗」；第 58
  - 方案：bg1-2 卡改「约十米长」「进城那头的出口很亮…门洞里阴凉、偏暗」；v13 重编 st3
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`
- **I9** [主要·implemented·待复核] 连续性·K6 环境接续：K6 环境接续 最终 1 分：同一地点的建筑、陈设、路人、动物在各镜一致，没有凭空出现；st1_gate.png：大拱上方有方形门楼和红瓦两坡顶，st2、st4
  - 方案：选保留门楼：s1_st5 首帧局部修，在门洞正上方补红瓦两坡顶门楼（与 st1/st2/st4 同款），文字和 ffp 写明；bg1 卡补门楼并标 ⚠️ 创作安排；s1_st4 藤筐「两只」改「几只」
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/st5_first_frame_prompt.txt`、`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1_海门外陡坡.md`
- **I10** [主要·implemented·待复核] Prompt 文本·T1 自相矛盾：T1 自相矛盾 最终 1 分：正文要的东西没有被负面词禁掉；同一 prompt 内前后一致；第 57 行「约十几米长」「通道两头都是亮的，……门洞里阴凉、偏暗」
  - 方案：bg1-2 卡统一为「约十米长」和门洞阴凉；s1_st4 统一「约一米」，绳写「留在他们拉船时站的沙上、绳头仍系在船头」；s1_st3「五六步」改「五六米」
  - 改了：`ai_videos/chuanyue_yiri/2_世界观人设/background/pompeii_75/bg1_海门外陡坡/bg1-2_海门门洞/bg1-2_海门门洞.md`、`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st4/planning/overhead.toml`
- **I11** [主要·implemented·待复核] Prompt 文本·T4 图文一致·明暗相反：T4 图文一致·明暗相反：首帧里 Riley 在门洞口被正面照亮，脸和衣服清楚；画面第 11 行「只看得出暗暗的轮廓」、动作 0–3 秒「从暗轮廓变成被照亮」、
  - 方案：s1_st5 文字照首帧：刚走出门洞，脸和衣服已被镜头身后的晨光照亮；删掉暗轮廓和亮边，ffp 负面词同步
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`、`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st5/planning/st5_first_frame_prompt.txt`
- **I14** [待核实·wontfix·待复核] 人物逻辑·C4 / 世界：C4 / 世界：铺子「刚卸下门板」但街上无任何店主 / 伙计，门洞口只有 Riley 一人，卸板人去哪了没交代；观众可能觉得城空
  - 方案：保留 st5 街上只有 Riley 和赶驴人
- **I16** [待核实·planned·待复核] 人物逻辑·其他·连贯：其他·连贯：st3 快照 prompt 第 12 行：挑夫和骡子第 10 秒走出城里那头的出口，「顺着街往前，到第 14 秒还在画里」；Riley 还要走约 9
  - 方案：v7 s1_st3 挑夫骡子路径延到 18 s、全程在画；st5 开场街上只有 Riley，靠剪辑省略时间，出片后用 st3 尾帧和 st5 首秒核实
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/scenes/s1/shots/st3/planning/overhead.toml`
- **I17** [待核实·planned·待复核] 连续性·K5 · I18 挑夫与骡子接续：K5 · I18 挑夫与骡子接续：st3 spec:11 规定骡子第 14 秒仍在街上；st5 spec:10 规定开场街上只有 Riley。st3 overh
  - 方案：同 I16：出片后用 st3 尾帧和 st5 首秒核骡子去向，真露在画内才补出画或调剪接
- **I28** [记录·planned·待复核] 人物逻辑·C6 / C1：C6 / C1：story.md 场一写「秃头老汉」牵驴、Riley「慢慢转了半圈」；spec 写「满头花白短发的老人」、站定后看驴 / 铺子 / 镜头；st3
  - 方案：story.md / story.json 场一「秃头老汉」改花白短发老人、删「慢慢转了半圈」、工人改扛筐站在墙根（现在 story.md 还没改）
- **I32** [记录·implemented·待复核] 连续性·K4 光（文字与首帧）：K4 光（文字与首帧）：spec 光线一行（第 42 行）写「她刚出门洞时只是一个暗轮廓…亮边」，节拍写「身影从暗轮廓变成被照亮」；首帧里她站在门洞口，被正面照
  - 方案：s1_st5 文字照首帧，删掉暗轮廓
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- **I34** [记录·wontfix·待复核] 连续性·K3 腰带：K3 腰带：st5_riley.png：腰带偏棕，配大号金扣；st1_riley.png 和 st4 首帧都是橄榄色帆布腰带配小金属扣
  - 方案：记录
- **I35** [记录·implemented·待复核] 连续性·K4 光（文字和首帧对不上·画右墙）：K4 光（文字和首帧对不上·画右墙）：spec 光线一行（:14）写「光从镜头身后略偏画右来…画右这一侧的墙面和整个街面在柔和的阴影里」；首帧画右那排铺子的上半
  - 方案：s1_st5 光线行照首帧改写为镜头身后的晨光照亮
  - 改了：`ai_videos/chuanyue_yiri/episodes/ep01/filming.json`
- 分镜「动作」改了：

```diff
@@ -1,7 +1,7 @@
 他拍。
-从城里顺着街朝城门方向拍：街的尽头是城墙，墙头是平的，墙上一个高大的拱形门洞在画面正中略偏右，门洞里是一条昏暗的拱顶通道，另一头出口远远一小块亮光。
-街是深灰色玄武岩石板路，路面中间一道浅浅的排水沟，沟里一线流水反光；
+从城里顺着街朝城门方向拍：街的尽头是城墙，墙上一个高大的拱形门洞在画面正中略偏右，门洞正上方的墙头上立着一座方形门楼，顶上是红瓦两坡顶，门洞里是一条昏暗的拱顶通道，另一头出口远远一小块亮光。
+街是深灰色玄武岩石板路，路面中线上一线浅浅的流水反光；
 两边人行道高出路面约四十厘米；
 两边的铺子是整面敞开的宽门脸，石门槛上有插门板的槽，刚卸下的木门板斜靠在墙边，门口摆着陶罐和藤筐，墙面是庞贝红和赭黄。
-Riley 从门洞的阴影里走出来，长发披散，斜穿过路面的边缘走向画左的人行道，第 3 秒抬脚迈上高出路面的路沿，身体随之一抬，然后沿人行道朝镜头走近。
+Riley 从门洞口往外走，长发披散，沿着画左路缘外侧的路面朝镜头走来，从斜靠在路边的门板旁边走过，约第 4 秒抬脚迈上高出路面的路沿，身体随之一抬，在第一间铺子门口的人行道上停下。
 约第 4.5 秒，一个赶驴人牵着一头灰驴从镜头身后走来，从画右边缘入画（普通路人，只顾赶路；
@@ -11,3 +11,3 @@
 赶驴人从她身旁经过时扭头瞥了一眼她的裤子，随即转回头接着赶路。
-Riley 转头目送驴和两只陶罐朝城门走去；
+Riley 转头目送驴和两只陶罐朝城门走去，顺势低头扫一眼自己的裤子，抿嘴笑一下；
 然后把上半身转向身边的铺子，看门口的陶罐和斜靠的门板；
@@ -18,3 +18,3 @@
 Riley 两手空着，钱一直揣在她裤袋里。
-第 0 秒：Riley 刚从门洞里迈出一步，还在门洞口的阴影里，离镜头约十一米，人很小、只看得出暗暗的轮廓，面朝镜头往外走，两手空着；
+第 0 秒：Riley 刚走出门洞，站在门洞口前，离镜头约十一米，人很小，脸和衣服已经被镜头身后的晨光照亮、看得清，面朝镜头往外走，两手空着；
 街上只有她一个人。
```

- 分镜「走位」改了：

```diff
@@ -2,5 +2,5 @@
 画左的人行道和路缘在画面左下，路面中线在画面右半。
-Riley 第 0 秒在门洞口，离镜头约十一米，约占画面高度四分之一，在画面横向正中略偏右；
-第 3 秒迈上画左的人行道；
-第 5 秒停在人行道上离镜头约六米处，全身入画、约占画面高度一半，在画面横向约三成处，此后站在原处，只转身：5–7.5 秒朝右看驴走近、经过，7.5–9.5 秒朝城门方向目送，9.5–11 秒朝身边的铺子，11 秒起朝镜头。
-驴和赶驴人约第 4.5 秒从画右边缘入画，沿路面靠画右的一半背对镜头朝城门走，第 7 秒前后从她身旁约两米半处经过，第 13 秒走到门洞口。
+Riley 第 0 秒在门洞口前，离镜头约十一米，约占画面高度四分之一，在画面横向正中略偏右；
+0–4 秒沿画左路缘外侧的路面走，约第 4 秒迈上画左的人行道；
+第 5 秒停在第一间铺子门口的人行道上，离镜头约六米，全身入画、约占画面高度一半，在画面横向约三成半处，此后站在原处，只转身：5–7.5 秒朝右看驴走近、经过，7.5–9.5 秒朝城门方向目送，9.5–11 秒朝身边的铺子，11 秒起朝镜头。
+驴和赶驴人约第 4.5 秒从画右边缘入画，沿路面靠画右的一半背对镜头朝城门走，第 7 秒前后从她身旁约两米半处经过（赶驴人走在驴靠画左的一侧，入画前从镜头右边约一米处走过），第 13 秒走到门洞口。
```

- 分镜「节拍」改了：

```diff
@@ -1,4 +1,4 @@
-0–3秒 Riley 从门洞的阴影里走出来，斜穿路面边缘走向画左的人行道，身影从暗轮廓变成被街上的散射光照亮；
-第 3 秒她抬脚迈上高出路面的路沿；
-3–5秒 她沿人行道朝镜头走近；
+0–4秒 Riley 从门洞口往外走，沿着画左路缘外侧的路面朝镜头走来，从斜靠在路边的门板旁边走过，晨光照在她脸上；
+约第 4 秒她抬脚迈上高出路面的路沿；
+4–5秒 她在第一间铺子门口的人行道上停下；
 约第 4.5 秒，赶驴人牵着驮两只陶罐的灰驴从镜头身后走来，从画右边缘入画，沿路面靠画右的一半朝城门走；
@@ -6,3 +6,3 @@
 6.5–7.5秒 赶驴人从她身旁经过，扭头瞥一眼她的裤子，转回头接着赶路；
-7.5–9.5秒 Riley 转头目送驴和两只陶罐朝城门走，嘴角带笑；
+7.5–9.5秒 Riley 转头目送驴和两只陶罐朝城门走，嘴角带笑，顺势低头扫一眼自己的裤子，抿嘴笑一下；
 9.5–11秒 她上半身转向身边的铺子，看门口的陶罐和斜靠的门板，安静；
```

- 分镜「光线」改了：

```diff
@@ -3,4 +3,5 @@
 画右这一侧的墙面和整个街面在柔和的阴影里，排水沟里一线流水反光；
-门洞里面很暗：她刚出门洞时只是一个暗轮廓，门洞远端出口的亮光给她的头发和肩头勾出一圈淡淡的亮边；
-走出几步、进到街上的散射光里才看清脸和衣服，画左亮墙反过来的暖光照在她身上。
+门洞里面很暗；
+她站在门洞口前时，镜头身后低低的晨光已经照到她身上，脸和衣服看得清；
+画左亮墙反过来的暖光也照在她身上。
 只有自然光。
```


### s1 整场 / 未指明镜头

- **I20** [待核实·implemented·待复核] 母语听感·N3 / R · I5 部分未闭合：N3 / R · I5 部分未闭合：lines.md:11 立找床与尝 garum 目标，:14 已改成 Future garum，:17 即结束；没有 dex
  - 方案：v7 母语听感盲审用全集台词（ear_v7/lines.md），结尾和 dextram 回收一起审过

### s1 整场 / 未指明镜头

- **I21** [待核实·implemented·待复核] 母语听感·N3 · 盲审材料与维度范围不一致：N3 · 盲审材料与维度范围不一致：lines.md:1 标题「全集台词」，但只到第 17 行（s1_st3）；N3 维度要求核对结尾和 dextram 的回收
  - 方案：同 I20：v7 盲审材料是全集台词，N3 回收可审

### s1 整场 / 未指明镜头

- **I27** [记录·implemented·待复核] 人物逻辑·C5：C5：上一轮为避免三路人雷同，删去 st5「低头看裤子、耸肩」；s1 五镜再无自嘲 / 敢试拍，唯一被人看裤子的 st5 6.5–7.5 秒里 Riley 在看
  - 方案：s1_st5 7.5–9.5 s 目送驴时低头扫一眼自己的裤子、抿嘴笑一下

### s1 整场 / 未指明镜头

- **I33** [记录·planned·待复核] 连续性·K4 方位（I30 复核）：K4 方位（I30 复核）：五镜 prompt 第 6 行写「上方为北」。st5_overhead.png 上标着 N↑，城门在上，画右写着「东侧店铺墙」，照这
  - 方案：编译器参考用法仍写「上方为北」（v13 63 镜都有）；改成各底图的局部朝向或「↑朝城」

### s1 整场 / 未指明镜头

- **I58** [记录·wontfix·待复核] Prompt 文本·T7·重复信息与本镜动作后置（F06；I50、I55）：T7·重复信息与本镜动作后置（F06；I50、I55）：最长 st4 4150 字符；st2 到第 1614 字符才进入正式画面行。五镜画面、走位、动作重复叙述
  - 方案：负面词已去重；画面 / 动作的重复叙述不大改

### s1 整场 / 未指明镜头

- **I59** [记录·planned·待复核] Prompt 文本·T7·固定句重复：T7·固定句重复：「声音」行在第 2 行和末行重复；「要求」行的字幕、水印、分身与负面词重复；负面词有 5 个词各重复一次
  - 方案：负面词重复已在 workflow.json 去重；声音行首尾两处重复、要求行和负面词的重复还要编译器去重

