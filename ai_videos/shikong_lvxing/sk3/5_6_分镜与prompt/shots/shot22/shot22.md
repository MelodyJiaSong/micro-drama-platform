---
segment: 承
section: 四 · 吃
duration: 30s
scene: bg6_Cheapside
view: bg6-1
characters: [c5]
props: [p7]
dialogue: yes
status: 已出prompt
---

# shot22 · 猜价格卡 + ❌ 唯一一次踩坑（茅草顶）

## Shot context

- 景别档: 大特写0.95 → 空镜仰角0.00（机位 `猜价格卡正面大特写` → `对街屋顶仰角空镜`）。**与前一镜的切口**：✅ 比值 2.11 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.transport.004`、`london1666.work.001`、`london1666.myth.008`
- 判断: 全片唯一一次「❌ 我以为」，镜头必须在画面上自证——末段上仰落在**瓦**上，一处茅草都不许有（伦敦城内 1189 年即禁茅草，1212 年后新屋须瓦/木瓦/木板顶）。18 便士是 1662 年马车法令价（T0），16 便士是小工日薪（⚠️ 那是承包商报给账房的价、实际到手低两三成，本镜不展开）。台词拆成三行：「Look up.」之前她在画内对镜，之后镜头已经离开她，改记为画外——嘴唇不动，与上仰的画面对得上

## 视频 prompt

```text
参考: `shot22_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg6-1(场景主体·bg6_Cheapside)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p7-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `先出猜价格卡：雇一小时马车十八便士，比小工干一整天挣的还多；接着她认这一站唯一的一次错——我以为满城是茅草顶；抬头看，是瓦`
场景: `bg6_Cheapside — 全城唯一一条日光能落到街面的街，两侧店面整个敞着`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
道具: `瓦屋顶一段：旧瓦哑光暗赭，一排一排的瓦楞，瓦沟里积着苔、边角有缺口，瓦面有雨痕——**不是**茅草、不是稻草束、不是芦苇`
镜头: `起幅正面大特写，脸几乎占满画面，35mm；0–12 秒机位不动、只有呼吸感；12–22 秒后拉到中景，让街与对街的屋顶进画；22–30 秒顺着她的视线一次连续上仰，她退出画框，落成仰角的瓦屋顶空镜，停在瓦楞与苔痕上。无剪切`
走位: `她正面对着镜头站在街边，视线始终在镜头上；说到「抬头看」时她先把下巴抬起来、视线上移，镜头才跟着上仰（人先动、镜头后动）；后拉时她原地不动，两侧的店面与人流自己进画；末段她完全退出画框，画面只剩对街四层楼的坡屋顶与那条天`
动作: `0–4 秒 她说「猜一下」，伸出一根手指停在胸前；4–8 秒 停住不说话三四秒，让观众自己猜；8–12 秒 报出数字，手指落下；12–16 秒 换了个站姿，肩膀松下来，像要认错的人那样先吸一口气，镜头开始后拉；16–22 秒 摊了一下手说自己以为是茅草，说到最后两个字时下巴抬起、视线上移；22–30 秒 镜头顺着她的视线一次连续上仰，落在对街的坡屋顶上——一排一排的旧瓦，瓦沟里积着苔、边角有缺口，一处茅草都没有`
台词:
  - 妮娅 · 对镜（对口型）: Guess. One hour in a hackney coach. …Eighteen pence. That's more than a labourer earns in a whole day.
  - 妮娅 · 对镜（对口型）: Okay—I owe you a correction. I came in here expecting thatch. Medieval city, wooden houses, straw roofs, right? Look up.
  - 妮娅 · 画外（画外，嘴唇不动）: Tile. London banned thatch in 1189. Nearly five hundred years ago. I was about five centuries out.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `正午的 Cheapside：日光从画面上方偏南打下来，瓦面上一道一道亮暗分明的瓦楞影，苔痕在背光的瓦沟里发暗、瓦脊上的亮边很硬；这条街够宽，所以屋顶和街面一起整个亮着；画面里没有任何火、没有任何暖色人造光源、天没有暗下来`
节奏: 猜价格那 4 秒的停顿是硬的、不许填；认错段一句一顿地慢下来；最后上仰的 8 秒把话交给画面——观众自己看见瓦
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 先卖关子，后坦白 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 0–12s
台词: Guess. One hour in a hackney coach. …Eighteen pence. That's more than a labourer earns in a whole day.
时长目标: 7.9s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 先卖关子，后坦白 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 12–22s
台词: Okay—I owe you a correction. I came in here expecting thatch. Medieval city, wooden houses, straw roofs, right? Look up.
时长目标: 8.3s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 先卖关子，后坦白 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 22–30s
台词: Tile. London banned thatch in 1189. Nearly five hundred years ago. I was about five centuries out.
时长目标: 7.1s
```
