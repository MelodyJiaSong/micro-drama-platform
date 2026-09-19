---
segment: 承
section: 穿
duration: 30s
scene: bg3_客栈
view: bg3-1
characters: [c5]
props: [p11]
dialogue: yes
status: 已出prompt
---

# shot13 · 穿搭检查 · 颜色，和不是什么

## Shot context

- 景别档: 全景0.30 → 中景0.45（机位 `回廊下她全身正面全景` → `院心弧线跟移·她四分之三中景`）。**与前一镜的切口**：✅ 比值 2.83 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.myth.001`、`london1666.dress.001`、`london1666.dress.002`
- 判断: 本镜时长 28→30 s，台词按 dialogue.md §2 注③ 减词：script 原文 69 词、需 28.75 s，超 28 s 镜长的 80% 闸门。减掉的是虚词与重复限定（the part / called / whole look / hat buckle 的 hat / was invented in），**sad colour 四个色名、十九世纪帽扣、十月七号、五个星期、中间夹着一件大事全部保留**

## 视频 prompt

```text
参考: `bg3-1(场景主体·bg3_客栈)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p11-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `回廊下，穿好全套 1666 平民装的妮娅站成全身正面：大家最容易弄错的是颜色——这一路叫 sad colour，赤褐、枯叶褐、肝褐、暗茶褐，不是那种一身黑、帽子上一枚大方扣的打扮，那枚帽扣是十九世纪的人想出来的，是同人创作。她再抬手在身前比划一下：没有长外套、没有马甲，那一整套三件式国王十月七号才宣布，离现在五个星期，中间还夹着一件挺大的事`
场景: `bg3_客栈 — 门洞穿进去是一圈木回廊，院子尽头堆着草`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
镜头: `一个机位，连续运动。0–12s 回廊下正对她、眼平、35mm 全景，从软帽到鞋整个人在画面里，身后是回廊的木栏杆与院心；12–22s 机位只极轻地降半米、基本不推，把她转身的半圈完整留在画面里；22–30s 机位沿一道贴地缓弧向画左横移并跟进，随她走出回廊阴影到院心受光处，收成中景（膝以上）——**本镜后段全程在走弧线，与上一镜『锁死不动位＋正面直推』明确分开，两镜的机位行为不撞**`
走位: `0–12s 她站在回廊下画面中央、正面朝镜头，双臂自然垂在身侧让整套衣服看清；12–20s 她转半圈让侧面与背面各过一遍，再转回正面；22–30s 她走到院心站定，身体四分之三侧对机位、脸转正朝镜头，视线落在镜头上；院里马夫与女仆各忙各的，不看镜头、不说话。**画面里不出现任何马甲、任何长外套、任何带方扣的高帽、任何全黑的清教徒装**——她说到这些东西时只是抬手在自己身前比一比又放下，那些东西不入画`
动作: `0–5s 她摊开双手示意整身衣服；5–12s 用手背依次拂过上衣、裙子、围裙的布面，说到色名时手停在每一块颜色上；12–18s 转半圈、再转回来；18–22s 抬手在自己头顶上方虚虚地比了一个帽檐的形状，随即摇头把手放下；22–27s 走到院心，两手在身前上下比一个长外套的轮廓，同样摇头放下；27–30s 说完最后一句，看着镜头挑了一下眉`
台词:
  - 妮娅 · 对镜（对口型）: People get the colour wrong. This is a sad colour — russet, drab, liver, dead-leaf. Not the all-black-with-a-big-buckle-on-the-hat thing. That buckle is nineteenth-century. It's fan fiction.
  - 妮娅 · 对镜（对口型）: Also: no long coat, no waistcoat. That three-piece look — the King announces it on the seventh of October. Five weeks from now. With a rather large event in between.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/1 上午：她从回廊下的阴影走到院心的受光处——前半段是天光反射的冷蓝漫射，衣料的赤褐与枯叶褐显得沉；后半段日光从院子东南斜进来直接照在她身上，同一批色名在直射光下才露出赤褐与肝褐的差别。画面里没有任何火、没有任何暖色人造光源、天没有暗下来；院里没有任何路灯、没有任何公共照明装置，回廊下吊着的角质提灯是没点的`
节奏: 摊手 → 拂过布面（报色名）→ 转一圈 → 比帽檐摇头 → 走到院心 → 比长外套摇头 → 挑眉
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 轻快，带笑 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 0–13s
台词: People get the colour wrong. This is a sad colour — russet, drab, liver, dead-leaf. Not the all-black-with-a-big-buckle-on-the-hat thing. That buckle is nineteenth-century. It's fan fiction.
时长目标: 10.8s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 轻快，带笑 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 14–28s
台词: Also: no long coat, no waistcoat. That three-piece look — the King announces it on the seventh of October. Five weeks from now. With a rather large event in between.
时长目标: 12.5s
```
