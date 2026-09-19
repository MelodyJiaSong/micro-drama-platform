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

# shot12 · 穿搭检查 · 一件一件往身上套

## Shot context

- 景别档: 中景0.55 → 近景0.85（机位 `回廊栏杆前正面中景` → `她头肩正面近景`）。**与前一镜的切口**：✅ 比值 2.50 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.dress.008`、`london1666.dress.011`
- 判断: 本镜是换装过程：起幅她还是现代装态（`角色:` 锁定串按现代装），落幅时全套 1666 平民装已经穿好、软帽系紧——shot13 起一律 1666 装态

## 视频 prompt

```text
参考: `bg3-1(场景主体·bg3_客栈)=>@`，`c5_妮娅(Seedance 人物 entity·现代装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p11-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `客栈二层回廊的木栏杆上搭着一整套 1666 年平民女装。现代装的妮娅对镜头宣布穿搭检查，然后一件一件往身上套：里面一件亚麻衬裙，外面羊毛紧身上衣、羊毛裙、围裙，最后一顶软帽把头发整个包进去——头得包起来，不然在街上等于在表态，今天她不想表这个态`
场景: `bg3_客栈 — 门洞穿进去是一圈木回廊，院子尽头堆着草`
角色: `妮娅（Seedance 人物 entity · 现代装态）— 深色运动上衣与工装裤、低帮徒步鞋，素色布质胸牌别在左胸；短话筒与麻布采访本随身`
镜头: `一个机位。回廊栏杆前正对她、眼平、35mm；0–20s 固定中景（腰以上），栏杆与其后的院子在景深里软下去；20–30s 极缓推近成近景（头肩），最后落在软帽系带被拉紧的那一下`
走位: `妮娅站在画面中央、正面朝镜头，栏杆在她身前下缘、衣物一件件搭在栏杆上；她说话时看镜头，取衣服时视线才短暂落到栏杆上；院子对面的回廊上有旅客走过，柔焦、不看镜头、不说话；全程她的位置不动，只有身上的层数在增加。**装束时序写死**：0–4s 她还是现代装态（深色运动上衣与工装裤、低帮徒步鞋），4–30s 逐件套上 1666 年平民装，落幅时亚麻衬裙、羊毛紧身上衣、羊毛裙、围裙、软帽全部到位、头发一根不露（`参考:` 行上传的人物 entity 以本行的分段为准）`
动作: `0–4s 她正脸看镜头，双手在栏杆上一拍，宣布穿搭检查；4–9s 抓起亚麻衬裙抖开、套进去，领口整理一下；9–15s 羊毛紧身上衣上身，手指从腰侧一路系到胸口；15–20s 羊毛裙一步跨进去、腰带在身后打好结；20–25s 围裙围上、在腰前系一个平结，低头看了一眼再抬头；25–30s 最后拿起软帽，双手把头发全部拢进帽里、下颌处把系带拉紧，说完看着镜头顿一拍`
台词:
  - 妮娅 · 对镜（对口型）: Right. Outfit check, London, 1666.
  - 妮娅 · 对镜（对口型）: Linen shift underneath, wool bodice, wool skirt, apron, and a coif — head covered, because a woman with her hair out in the street reads as a statement I don't want to be making today.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/1 上午：回廊朝院的一面开敞，日光从院心斜进来打在她的正面与栏杆上，回廊深处是阴影；她脸上是柔和的天光加一点直射侧光，衣料的织纹在侧光里看得见。画面里没有任何火、没有任何暖色人造光源、天没有暗下来；回廊下没有任何路灯、没有任何公共照明装置，吊着的角质提灯是没点的`
节奏: 宣布（拍栏杆）→ 衬裙 → 上衣 → 裙 → 围裙 → 软帽拉紧，顿一拍
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 轻快，像在做示范 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 0–4s
台词: Right. Outfit check, London, 1666.
时长目标: 2.1s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 轻快，像在做示范 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 5–28s
台词: Linen shift underneath, wool bodice, wool skirt, apron, and a coif — head covered, because a woman with her hair out in the street reads as a statement I don't want to be making today.
时长目标: 14.6s
```
