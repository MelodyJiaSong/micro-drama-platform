---
segment: 合
section: 九 · 宵禁与过夜
duration: 30s
scene: bg9_客栈房间夜
view: bg9-1
characters: [c5]
props: [p3, p8, p13]
dialogue: yes
status: 已出prompt
---

# shot41 · 今日总账单

## Shot context

- 景别档: 全景0.30 → 近景0.85（机位 `房门内侧略俯看全屋` → `床沿对镜正面近景`）。**与前一镜的切口**：✅ 比值 2.50 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.work.001`、`london1666.work.006`、`london1666.price.001`、`london1666.price.002`、`london1666.housing.013`
- 判断: 折算口径：小工 16 便士一天（work.001）。**只给相对量、不报绝对总数**——work.006 明说账册上的 day rate 是承包商向业主开的价，工人实得低两到三成，报一个精确的便士总额等于把一个有系统偏差的数字钉死。全片唯一的除数仍是 16d。「一便士永远买一条面包、只会越来越小」是 Assize of Bread 价格固定重量浮动的机制（price.001 / price.002）；具体重量本站查无 1666 年 assize 表，全片一个重量数字都不报（见 shot49）。

## 视频 prompt

```text
参考: `shot41_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg9-1(场景主体·bg9_客栈房间夜)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p3-1(物件锚点)=>@`，`p8-1(物件锚点)=>@`，`p13-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `睡前算今天的账：一张床、两顿饭、面包、淡啤酒，还有一趟没雇到的船。全部按小工的日薪折算——大约是别人一天半的活，换她在这儿当一天游客。最后回到那个最有用的数字：一条面包，一便士。永远一便士。只会越来越小。`
场景: `bg9_客栈房间夜 — 一支蜡烛照得到的地方就是全部，窗外是彻底的黑`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
道具: `蜡烛与烛台：白蜡短烛插在锈黑铁烛台上，烛身略歪、蜡泪堆在托盘一侧；角质提灯：四面刮薄的兽角片嵌在锈黑铁框里，挂在门后，全程未点；她的三件不变物——素色布质胸牌、短话筒、麻布封面采访本——放在矮凳上`
镜头: `起幅是从房门内侧略俯看的全屋景，她坐在床沿，烛台在画面右前景、火苗压住构图的一角；镜头贴着地板匀速推进并降到平视，越过烛台把她推成对镜近景，落幅她的视线正对镜头。推进不停顿、不变焦。`
走位: `妮娅坐在床沿，正面略偏左对着镜头，双脚落地；矮凳在她左手边，凳上摊着麻布封面采访本，本子旁分着两小堆硬币——两枚银先令一堆、三枚私铸铜代币一堆。她全程不起身，也不把硬币举到镜头前。`
动作: `0–8s 她把硬币一枚枚推到凳面另一侧，边推边报项目：床、两顿饭、面包、淡啤酒、那趟没雇到的船；8–18s 手停下，抬眼看镜头说折算，说到「一天半」时她的手指在凳面上点了两下；18–26s 说到最后那个数字时，她把最后一枚铜代币按在凳面上不动；26–30s 说完她收回手，低头看烛焰，不说话、不收尾、不看镜头。`
台词:
  - 妮娅 · 对镜（对口型）: Today: a bed, two meals, bread, small beer, and a ferry I never got. All of it, against a labourer's day — call it a day and a half of somebody's work for me to be a tourist here. And the useful number: the loaf. A penny. Always a penny. Only ever smaller.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/1 夜 —— 唯一光源是矮凳旁那支蜡烛，蜡黄，只及一到两米；她的正面被烛光照亮，背后的墙与房间四角落在深褐黑里，推进时烛光在她脸上的亮区逐渐变大。窗是一块纯黑，窗外没有路灯、没有灯笼、没有任何公共照明、没有火光。`
节奏: 中慢；报项目时略快、报折算时慢下来，最后三句一句一停。
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 平、收尾冷；不许有自嘲的收口 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 2–28s
台词: Today: a bed, two meals, bread, small beer, and a ferry I never got. All of it, against a labourer's day — call it a day and a half of somebody's work for me to be a tourist here. And the useful number: the loaf. A penny. Always a penny. Only ever smaller.
时长目标: 22.1s
```
