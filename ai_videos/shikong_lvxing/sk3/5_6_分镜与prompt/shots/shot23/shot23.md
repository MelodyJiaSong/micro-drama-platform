---
segment: 承
section: 五 · 跟着皮普斯
duration: 25s
scene: bg8_Moorfields木偶戏棚
view: bg8-1
characters: [c5, c26]
props: []
dialogue: yes
status: 已出prompt
---

# shot23 · 远远跟着皮普斯

## Shot context

- 景别档: 全景0.12 → 中远景0.30（机位 `Moorfields 草地远景` → `人群后方中远景跟移`）。**与前一镜的切口**：✅ 一端无人一端有人，天然跳档
- 衔接: 硬切（独立首帧）
- 史实: `london1666.people.003`、`london1666.timeline.002`
- 判断: c26 皮普斯全程不开口、不对口型、不给特写（casting §0／§2：他的话是**写的**不是说的，走字卡与妮娅的画外引述）；本镜他最近也只到中远景 0.30，侧脸说话听不见内容、不算台词。9 月 1 日下午他确实带着妻子与 Mercer 来看木偶戏（日记 T0）

## 视频 prompt

```text
参考: `shot23_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg8-1(场景主体·bg8_Moorfields木偶戏棚)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`c26(人物锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `城墙外北侧的 Moorfields 空地。她远远指给你看一个人：海军署的塞缪尔·皮普斯——他什么都记，所以我们才知道今天长什么样`
场景: `bg8_Moorfields木偶戏棚 — 城外草地上一座布幔木偶棚，三面围站的人在笑`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
镜头: `起幅观众人群后方的草地远景（皮普斯只是人群里的一个小人影），35mm 手持；全程一次缓慢的跟移前推，最后 8 秒落成人群后方的中远景；镜头始终隔着两三层人看他，不越过人群、不给正面特写`
走位: `戏棚在画面纵深的正中，观众三面围站；皮普斯在人群靠右的位置、背对镜头面朝戏棚，身边跟着一位女眷与另一名男子；妮娅在画面最前景的左下角，只入半个背影与肩线、面朝皮普斯的方向、不看镜头；镜头在她身后跟着她走`
动作: `0–6 秒 人群里一阵笑，皮普斯抬手把帽子往上推了一下；6–13 秒 妮娅从画左的前景横过、停在一棵树边，镜头跟着她移；13–19 秒 她微微侧头示意皮普斯的方向——手抬到腰高就停住，不伸直、不指人脸；19–25 秒 皮普斯侧过半张脸对身边的人说了句什么（听不见内容），随即转回去看戏，镜头停在中远景上`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: I want to show you someone. I'm not going to talk to him—he wouldn't know what to do with me. That man works for the Navy Board. His name is Samuel Pepys, and he writes everything down. Everything. Which is why we know what today looked like.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `城外空地的下午：开阔地，日光平均，没有窄巷那种压迫感，人影在草地上拖出不长的斜影；远处城墙与塔林的轮廓罩在一层煤烟灰里；画面里没有任何火、没有任何暖色人造光源、天没有暗下来`
节奏: 整镜都是「远远地看」的节奏——不追、不推脸；最后停在中远景上不动，把距离本身留在画面里
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 25秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 压低的兴奋 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 2–23s
台词: I want to show you someone. I'm not going to talk to him—he wouldn't know what to do with me. That man works for the Navy Board. His name is Samuel Pepys, and he writes everything down. Everything. Which is why we know what today looked like.
时长目标: 19.6s
```
