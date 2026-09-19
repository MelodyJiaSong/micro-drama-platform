---
segment: 承
section: 四 · 吃
duration: 28s
scene: bg6_Cheapside
view: bg6-1
characters: [c5]
props: [p1, p5]
dialogue: yes
status: 已出prompt
---

# shot21 · 试吃打分 + small beer

## Shot context

- 景别档: 近景0.70 → 中景0.45（机位 `街边靠墙对镜近景` → `街边中景带摊位`）。**与前一镜的切口**：✅ 一端无人一端有人，天然跳档
- 衔接: 硬切（独立首帧）
- 史实: `london1666.food.006`、`london1666.food.010`、`london1666.food.011`
- 判断: 台词只砍了一个形容词（slightly），事实未动。杯里是 small beer——浑浊的浅琥珀色、几乎没有泡沫顶；伦敦没有能喝的清水，所以这是日常饮料不是酒。**画面里不出现叉子、不出现茶壶茶具**（1666 年茶还不是日常饮料）

## 视频 prompt

```text
参考: `shot21_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg6-1(场景主体·bg6_Cheapside)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p1-1(物件锚点)=>@`，`p5-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `她当街咬一口 maslin，给七分；再就着一杯 small beer 咽下去——这儿的水会要你的命，所以从大人到小孩整天喝的都是这个`
场景: `bg6_Cheapside — 全城唯一一条日光能落到街面的街，两侧店面整个敞着`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
道具: `maslin 面包：大而扁、灰褐色、气孔粗、外皮硬，掰开要用两只手；small beer 陶杯：粗陶杯，杯里是浑浊的浅琥珀色液体、几乎没有泡沫顶——不是清水、不是现代啤酒那层厚白泡沫`
镜头: `起幅街边靠墙的对镜近景，35mm；镜头几乎不动，只有很轻的手持呼吸感；最后 8 秒缓缓后拉半步，落成中景、把身后的面包摊带进画。无剪切`
走位: `她站在画面中央偏右、正面对着镜头，视线落在镜头上；身后画左约三米是那个面包摊，摊主在摊后侧对她；她右手拿面包、左手端陶杯；说到淡啤酒时把陶杯举到胸口高度让它进画，视线不离镜头`
动作: `0–5 秒 她掰下一块 maslin——外皮硬得要用两只手——咬下去慢慢嚼，不说话；5–9 秒 咽下去，眉毛先挑起来，然后才开口；9–14 秒 报出分数时用拿面包的手比了个七；14–16 秒 举起陶杯喝一口；16–19 秒 先把杯子放稳到胸前，然后才换重心继续说；19–28 秒 说完最后一句，视线始终在镜头上，停半秒`
台词:
  - 妮娅 · 对镜（对口型）: …That's not bad. That's dense and sour and it tastes like it's going to keep me upright until dark. Seven out of ten. And I'm washing it down with small beer, because the water here will end you—this is what everybody drinks, all day, including children. It's not a night out. It's hydration.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `正午的 Cheapside：日光从左前方直落在她脸上，右侧有店面檐口带来的柔和阴影，面包的粗气孔与陶杯里浑浊的浅琥珀色都看得清；画面里没有任何火、没有任何暖色人造光源、天没有暗下来`
节奏: 嚼那 4 秒必须真的空着——这一镜的可信度全在她先吃完再开口；后段一句一顿，最后「这是喝水」落得干脆
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 28秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 轻松、带笑意 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 5–28s
台词: …That's not bad. That's dense and sour and it tastes like it's going to keep me upright until dark. Seven out of ten. And I'm washing it down with small beer, because the water here will end you—this is what everybody drinks, all day, including children. It's not a night out. It's hydration.
时长目标: 22.1s
```
