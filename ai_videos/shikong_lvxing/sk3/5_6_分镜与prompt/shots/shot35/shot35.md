---
segment: 转
section: 七 河与燃料
duration: 26s
scene: bg4_泰晤士街与码头
view: bg4-1
characters: [c5, c24]
props: []
dialogue: yes
status: 已出prompt
---

# shot35 · 河阶 · 雇不到船 · 船夫的盼头

## Shot context

- 景别档: 中远景0.28 → 近景0.80（机位 `河阶中段朝东·空船位` → `贴水低位略仰·船夫抬眼正面近景`）。**与前一镜的切口**：✅ 比值 2.79 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.transport.012`、`london1666.people.012`
- 判断: 船少、船夫年纪偏大，这就是 `transport.012`（1666 年海军大举强征，皮普斯当年原话「could not get watermen … by reason of the great presse」）的画面表达。**不写他抱怨、不写任何冲突、不写妮娅被拦被赶**（world.md §7）。**镜头拍被问的人的脸**。

## 视频 prompt

```text
参考: `shot35_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg4-1(场景主体·bg4_泰晤士街与码头)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`c24(人物锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `她雇不到船。不是因为忙，是因为根本没有——海军为了打仗一直在强征船夫。河阶上空着一大片船位，最后一条船上有个老船夫正在收工盘绳。`
场景: `bg4_泰晤士街与码头 — 半条街的库门都敞着，里面全是能烧的东西`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
镜头: `起幅在河阶中段朝东，中远景，妮娅背对镜头站在台阶上、身边是一段空着的系船桩；镜头沿台阶向下横移、越过两三条空船，最后沉到船头旁贴近水面的低机位（比他坐着的眼位还低半头），收成**略仰的正面近景**——画面下缘始终压着一线水；本镜是**自下往上看他**，与上一镜的略俯、上上镜的平视各不相同。`
走位: `起幅妮娅背对镜头站在台阶中段，占画高不到三分之一，全程不回头、不入面部，她的两句都在画外；**她自第 8 秒起退出画框、此后不再入画**；老船夫坐在船头上盘绳，落幅时**身体正对镜头，答话时抬眼看向镜头左上方画外——妮娅站在高一级的河阶上、镜头左边，画面里看不见她；他的视线落在画外的她脸上，不直视镜头、不对着观众说话**。`
动作: `0–8s 空着的系船桩一根接一根从画面里过去，水面上只有零星几条船，妮娅抬手朝河面指了一下又放下——一个「没有」的手势；8–16s 镜头沿台阶下移、横过空着的船位，最后一条船上有人；16–21s 老船夫把缆绳一圈圈盘好、扣在桩上，动作很慢、每一下都稳；21–26s 他停下手，抬头朝镜头左上方画外的她答话，说完停了一拍，又把最后半句重了一遍，随即低头继续盘绳。`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: I can't get a boat. Not because they're busy—because there aren't any. The Navy has been pressing watermen for the war, and Pepys complains about exactly this in his diary this year: you simply cannot get one.
  - 妮娅 · 画外（画外，嘴唇不动）: And when it's over?
  - c24 船夫 · NPC（对口型）: Bigger boat. That's all. A bigger boat.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `白天偏晚的斜光从西边来，河面是锡灰反光、台阶的湿处发亮，船夫的脸受一面水反射回来的光、偏冷；画面里没有任何火、没有任何暖色人造光源、天没有暗下来；空气里没有烟、没有落灰`
节奏: 起幅空、慢；老船夫的每一下动作都稳，不催他
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 26秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 扑空之后的平静 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 1–17s
台词: I can't get a boat. Not because they're busy—because there aren't any. The Navy has been pressing watermen for the war, and Pepys complains about exactly this in his diary this year: you simply cannot get one.
时长目标: 15.4s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 扑空之后的平静 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 19–21s
台词: And when it's over?
时长目标: 1.7s
```

```text
角色: c24 船夫 ｜ 音色(锁定·全站复用): `en-m-waterman-01`
情绪: 扑空之后的平静 ｜ 语速: 中
类型: NPC ｜ 时间窗: 21–26s
台词: Bigger boat. That's all. A bigger boat.
时长目标: 2.9s
```

> **非旅行者台词的合法性**：c24 船夫 ← 虚构人物·现代英语
