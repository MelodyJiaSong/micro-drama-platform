---
segment: 起
section: 开场
duration: 30s
scene: bg1_旧伦敦桥
view: bg1-1
characters: [c5]
props: []
dialogue: yes
status: 已出prompt
---

# shot03 · 自报家门 · 今日逛单

## Shot context

- 景别档: 中景0.50 → 近景0.70（机位 `桥南石门外街面正面平视` → `桥南石门外正面平视·推近`）。**与前一镜的切口**：✅ 比值 6.25 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.city.001`、`london1666.city.018`、`london1666.city.026`
- 判断: 本镜时长 28→30 s，台词按 dialogue.md §2 注③ 减词：script 原文 84 词、需 35 s，超 30 s 硬顶两倍有余。减掉的全是形容词与连接语（packed / roughly / You'll notice / Here's the plan / in this city），**三百三十英亩、城墙、一百座教堂塔、顶是平的那座、五条逛单一条不少**

## 视频 prompt

```text
参考: `bg1-1(场景主体·bg1_旧伦敦桥)=>@`，`c5_妮娅(Seedance 人物 entity·现代装态)=>@`，`妮娅声音(c5-2 声样)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `现代装的妮娅站在旧伦敦桥南端石门外的街面上，正对镜头自报家门：这座城墙里三百三十英亩、上百座教堂塔，其中一座顶是平的；接着把今天的逛单一条条数完——过桥、找床、换衣服、吃两顿、进这城里最有钱的两个地方。她身后是南端石门的门洞与一路往桥上走的人流`
场景: `bg1_旧伦敦桥 — 被房屋夹死的桥上隧道走到头，天光从 33 年没补上的缺口灌进来`
角色: `妮娅（Seedance 人物 entity · 现代装态）— 深色运动上衣与工装裤、低帮徒步鞋，素色布质胸牌别在左胸；短话筒与麻布采访本随身`
镜头: `一个机位。石门外街面正对她、眼平、35mm、中等光圈；0–20s 固定中景（腰以上），她身后石门与人流在景深里软下去；20–30s 机位极缓推近成近景（胸口以上），背景进一步压虚`
走位: `妮娅站在画面中央偏左、正面朝镜头，说话时视线始终落在镜头上；画面右侧后方是桥南端石门的门洞与门上的高杆；挑担的、赶驴的、拎篮子的行人从她身后横过画面，柔焦剪影、不看镜头、不说话、不与她互动；12–14s 她抬右手朝身后（画面右后方、城的方向）指一下。**本镜她仍是现代装态**——深色运动上衣与工装裤、低帮徒步鞋，素色布质胸牌别在左胸，短话筒与麻布采访本随身；画面里不出现 1666 年的羊毛紧身上衣、羊毛裙、围裙或软帽（`参考:` 行上传的人物 entity 以本行为准）`
动作: `0–7s 她正脸看镜头开口自报家门，左手把麻布采访本夹在腋下；7–14s 一边说一边用右手在胸前比画城的范围，12–14s 抬手朝身后一指；14–20s 视线回到镜头，说到那座顶是平的塔时顿了半拍；20–30s 机位推近的同时她用左手手指一条一条点数今天的安排，点到第五条时收手、抿嘴一笑`
台词:
  - 妮娅 · 对镜（对口型）: I'm Nia, with the Time Expedition Team. Biggest city in England — three hundred and thirty acres inside a wall, a hundred church towers. One has a flat top.
  - 妮娅 · 对镜（对口型）: Today: cross the bridge, find a bed, change into something that doesn't get me stared at, eat twice, and get into the two places with the money.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/1 上午偏早：日在东南、斜光从画面右后方越过石门照下来，在街面上投出石门与高杆的长影；她脸的右半受光、左半是天空反射的冷蓝柔光；空气里是常年的煤烟霾，远处的桥体与房屋发灰。画面里没有任何火、没有任何暖色人造光源、天没有暗下来；街上没有任何路灯、没有任何公共照明装置`
节奏: 开口（利落）→ 比画城 → 抬手一指 → 掰手指数单 → 推近收，一笑
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 利落，有精神 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 0–14s
台词: I'm Nia, with the Time Expedition Team. Biggest city in England — three hundred and thirty acres inside a wall, a hundred church towers. One has a flat top.
时长目标: 12.1s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 利落，有精神 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 15–29s
台词: Today: cross the bridge, find a bed, change into something that doesn't get me stared at, eat twice, and get into the two places with the money.
时长目标: 11.2s
```
