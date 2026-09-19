---
segment: 转
section: 六 机构
duration: 20s
scene: bg5_皇家交易所内院
view: bg5-1
characters: [c5]
props: []
dialogue: yes
status: 已出prompt
---

# shot26 · 皇家交易所内院 · 同一座城

## Shot context

- 景别档: 全景0.12 → 中远景0.20（机位 `交易所拱廊下朝院心` → `交易所院心朝东北拱廊`）。**与前一镜的切口**：✅ 比值 5.83 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.city.023`
- 判断: 全片最热闹一镜，也是阶级边界的另一侧；起幅刻意从拱廊的暗里走出来，一步之间从暗跳到亮。
**2026-09-19 跨段复核改**：原台词「Two hours ago I was in an alley where the buildings touched overhead.」在两处重复——① 逐层外挑／头顶合拢这条事实 shot07 与 shot15 已经各讲过一次，本镜是第三次口播；② 「窄→宽 + Same city」这个揭示动作 shot17→18 已经完整做过一遍（那一对还是全片最强的切口）。同时本镜声明的 `city.023` 在原台词里一个字都没用上。现把对比轴从**几何**换成**钱与身份**：街上你不走就挡道，这里一记钟给他们一小时站着说话（`city.023`：交易所一周开六天、每天两场各一小时、以钟楼敲钟为号）。钟楼在 13–20s 随机位升起进画，台词的「a bell」正好落在它上面；这一记钟也替 shot39 的宵禁钟提前埋了一下。

## 视频 prompt

```text
参考: `shot26_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg5-1(场景主体·bg5_皇家交易所内院)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `皇家交易所——同一座城里另一种时间。妮娅从南面拱廊的阴影里走出来，站在露天院心边上，被满院站着谈事的人声罩住；这些人不赶路、不让道，就站在那儿谈，一站一小时。`
场景: `bg5_皇家交易所内院 — 四面拱廊围出的院子里全是站着谈事的人，声音在拱下打转`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
镜头: `起幅在南面拱廊下，前景压一道拱券的暗边，取院心的全景；镜头贴着地面匀速横移穿出拱廊、进入露天院心，同时缓缓升起约半米，落在院心偏东、朝东北回廊的中远景上。全程一个连续运镜，不切。`
走位: `妮娅在画面左三分之一处，背对镜头站在拱券的阴影里，只占画高很小一段，全程不回头、不入面部；院心成团站着三五成群的商人，人群的密度从近到远不减；镜头越过她的右肩推向院心，她随之向前走两步后停住，留在画面左缘。`
动作: `0–6s 拱券的暗框里框着亮处的院心，人群在光里晃动、手势不停；6–13s 镜头贴地横移穿出拱廊，妮娅向院心走两步、停住，慢慢左右环视一圈；13–20s 机位轻轻升起，露出对面两层连续拱券的回廊与壁龛里的国王石雕像，人群向纵深展开，最远处是南面带钟的入口塔楼。`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: On the street you keep moving or you're in the way. In here a bell rings and they get an hour to stand still and talk. This is the Royal Exchange. Same city.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `下午的直射日光把露天院心照得发白，四面两层回廊整个沉在阴影里，明暗分界锐利，人走出拱廊的那一步之间从暗跳到亮；画面里没有任何火、没有任何暖色人造光源、天没有暗下来；空气里没有烟、没有落灰`
节奏: 慢起幅、匀速推进，全程一个连续运镜不切；本段声音密度最高的一镜，画面也最满
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 20秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 好奇、被声音罩住 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 2–17s
台词: On the street you keep moving or you're in the way. In here a bell rings and they get an hour to stand still and talk. This is the Royal Exchange. Same city.
时长目标: 13.8s
```
