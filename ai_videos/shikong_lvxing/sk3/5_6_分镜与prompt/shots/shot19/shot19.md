---
segment: 承
section: 四 · 吃
duration: 20s
scene: bg6_Cheapside
view: bg6-1
characters: [c5]
props: [p1]
dialogue: yes
status: 已出prompt
---

# shot19 · 面包摊三档（都是一便士）

## Shot context

- 景别档: 近景0.75 → 中景0.55（机位 `面包摊侧前方近景` → `面包摊正面中景`）。**与前一镜的切口**：✅ 比值 2.14 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.food.006`、`london1666.price.001`、`london1666.price.002`
- 判断: 三档都卖一便士、区别在大小——Assize of Bread 钉死的是价、浮动的是重量。**1666 年一便士面包的确切重量查不到，画面与台词都不报盎司数**（dossier §14）。画面里不出现叉子、不出现土豆番茄玉米辣椒

## 视频 prompt

```text
参考: `shot19_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg6-1(场景主体·bg6_Cheapside)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p1-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `街边面包摊前，三档面包并排摆着：白的 manchet、中间的 cheat、黑麦掺小麦的 maslin——三种都是一便士，区别只是你能拿到多少`
场景: `bg6_Cheapside — 全城唯一一条日光能落到街面的街，两侧店面整个敞着`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
道具: `面包三档同框：最贵的 manchet 小而圆、表皮浅金、内里近白；中档 cheat 中等个头、米黄带细麸点；最便宜的 maslin 大而扁、灰褐色、气孔粗、外皮硬——三条并排摆在同一块摊布上，个头一眼分得出大小`
镜头: `起幅摊位侧前方的近景（她半身入画，摊面在画左下），35mm 中等光圈；一次轻微的左弧摇加后拉，落成摊位正面的中景，三档面包在画面中央并排，摊主与她同框。无剪切`
走位: `摊子在画左，摊主站在摊后面朝街、面朝她；她在摊前画右，四分之三侧对镜头、面朝摊主；她的视线在三档面包之间从左到右移；镜头起幅在她右后方，弧摇到摊位正面，全程与两人在同一侧、不越轴`
动作: `0–5 秒 她伸手挨个指过三档面包，指到第三种时手停在上方不碰；5–10 秒 摊主把最小的那条白面包立起来给她看，又拍了一下最大的那条灰褐色的——两条的个头差一眼可见；10–15 秒 她用两只手比了一下这两条的长度差，眉毛挑起来；15–20 秒 摊主把大的那条递过来，她双手接住，先接稳、然后才抬头看摊主`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: Three sizes on the stall. White manchet for people with money, cheat in the middle, and maslin—rye and wheat together—for everyone else. All of them cost a penny. The difference is how much bread you get.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `正午的 Cheapside：日光直接落到街面与摊布上，面包的表皮反光与切面的粗气孔都看得清；摊棚布在摊面上投下一道边界清楚的硬影，影子外面是亮的、里面是暗的；画面里没有任何火、没有任何暖色人造光源、天没有暗下来`
节奏: 三档面包一档一拍，节奏跟着台词的三段走；最后接过面包那一下慢半拍，为下一镜的付钱留口
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 20秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 轻快、好奇 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 1–17s
台词: Three sizes on the stall. White manchet for people with money, cheat in the middle, and maslin—rye and wheat together—for everyone else. All of them cost a penny. The difference is how much bread you get.
时长目标: 15.0s
```
