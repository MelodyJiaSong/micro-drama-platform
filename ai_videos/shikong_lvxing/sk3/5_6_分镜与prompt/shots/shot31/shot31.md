---
segment: 转
section: 六 机构
duration: 30s
scene: bg7_旧圣保罗
view: bg7-1
characters: [c5, c25]
props: []
dialogue: yes
status: 已出prompt
---

# shot31 · 六天前议定的圆顶 · 与一个学徒的盼头

## Shot context

- 景别档: 中景0.40 → 近景0.80（机位 `墓地书商摊前朝西·妮娅中景` → `书商摊后朝东·学徒正面近景`）。**与前一镜的切口**：✅ 比值 2.86 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.city.020`、`london1666.people.013`
- 判断: 字卡（后期叠加，**不进 prompt**）：伊夫林日记 1666-08-27 逐字「a noble cupola, a form of church-building not as yet known in England」（T0，`london1666.city.020`），叠在 10–18s。
剧本原句「The booksellers in the churchyard will carry their entire stock down into the crypt for safekeeping, and it will burn down there too.」因语速闸门未能入镜——30 s 只载得下约 57 词，而本镜还要留住 25 词的 NPC 对话（`people.013` 的盼头是本片最要紧的设计之一）。该句的落差改由段十一 shot48（剧本 shot45）的回扣承担，此处只留「Nine days from now, this burns for a week.」；第一句的两人也压成了一句（原文分三句）。
**镜头拍被问的人的脸**：问的人知道结局、被问的人不知道，妮娅全程不暗示、不剧透，学徒答得轻快、毫无阴影。

## 视频 prompt

```text
参考: `shot31_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg7-1(场景主体·bg7_旧圣保罗)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`c25(人物锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `六天前，约翰·伊夫林和三十三岁的天文学家克里斯托弗·雷恩就站在这儿，一致认为旧塔不值得修了——他们想要的是一座英格兰还没见过的圆顶。九天后这座楼会烧一个星期。镜头最后落在墓地这边一个书商学徒的脸上，他正在码新到的印张。`
场景: `bg7_旧圣保罗 — 包着白石新皮的哥特巨物，中央塔的顶是平的，满墙脚手架`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
镜头: `起幅是墓地一侧书商摊前的中景，妮娅在画面左侧、身后是教堂西墙与满墙脚手架；镜头随她转身走向摊子而横移，最后绕到摊后、停在学徒的正面近景上不动。`
走位: `起幅妮娅在画面左缘、四分之三背向镜头，只见肩线与半张侧脸；书商摊横在画面中段，摊上摞着一叠叠新印张；学徒在摊后站着、身体正对镜头，两手还按在纸上；**他答话时视线落在镜头左侧画外妮娅站的位置（她就在镜头左边一步，画面里看不见她），眼神偏向画左、不直视镜头、不对着观众说话**。镜头绕到摊后之后，妮娅整个退到画框外——最后六秒画面里只有学徒一个人的脸（脸正对镜头、眼神偏向画左的她）。`
动作: `0–10s 妮娅站在摊前朝教堂方向看，抬手朝上方那截方塔指了一下又放下；10–18s 她转身走向书商摊，镜头随之横移，摊上的印张与麻绳捆一叠叠掠过前景；18–24s 她在摊前侧身开口问（只见侧脸，口型可读），学徒抬起头；24–30s 镜头已绕到学徒正面，他停下手里的活、先愣了半秒，随即笑了一下答话，答完低头继续把印张一张张码齐——动作轻快，没有半点犹豫。`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: Six days ago, John Evelyn and Christopher Wren, a thirty-three-year-old astronomer, stood here.
  - 妮娅 · 画外（画外，嘴唇不动）: They agreed the old tower wasn't worth saving. Nine days from now, this burns for a week.
  - 妮娅 · 对话（对口型）: What are you going to do, when you're out of your time?
  - c25 书商学徒 · NPC（对口型）: Have my own shop. Print the one book I actually want to print.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `下午的日在西南，教堂西墙与脚手架把斜影打到墓地这一侧的摊子上，学徒的脸在半影里，受一片从石灰白墙面弹回来的柔和反射光；画面里没有任何火、没有任何暖色人造光源、天没有暗下来；空气里没有烟、没有落灰`
节奏: 前 18 秒稳稳讲完史料，18 秒后把镜头交给学徒的脸，之后不再动
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 前半段克制转述，后半段温的 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 1–8s
台词: Six days ago, John Evelyn and Christopher Wren, a thirty-three-year-old astronomer, stood here.
时长目标: 5.4s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 前半段克制转述，后半段温的 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 9–18s
台词: They agreed the old tower wasn't worth saving. Nine days from now, this burns for a week.
时长目标: 7.1s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 前半段克制转述，后半段温的 ｜ 语速: 中
类型: 对话 ｜ 时间窗: 19–24s
台词: What are you going to do, when you're out of your time?
时长目标: 5.0s
```

```text
角色: c25 书商学徒 ｜ 音色(锁定·全站复用): `en-m-apprentice-01`
情绪: 前半段克制转述，后半段温的 ｜ 语速: 中
类型: NPC ｜ 时间窗: 25–30s
台词: Have my own shop. Print the one book I actually want to print.
时长目标: 5.4s
```

> **非旅行者台词的合法性**：c25 书商学徒 ← 虚构人物·现代英语
