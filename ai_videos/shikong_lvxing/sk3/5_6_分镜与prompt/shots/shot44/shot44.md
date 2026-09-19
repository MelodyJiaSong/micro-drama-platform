---
segment: 合
section: 十 · 凌晨
duration: 26s
scene: bg10_伦敦全城燃烧
view: bg10-1
characters: [c5]
props: []
dialogue: yes
status: 已出prompt
---

# shot44 · 起火时刻 —— 两份一手史料对不上

## Shot context

- 景别档: 远景0.08 → 大远景0.00（机位 `街心低位广角远景` → `东南天际火线大远景`）。**与前一镜的切口**：✅ 比值 3.75 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.timeline.004`、`london1666.timeline.011`、`london1666.coord.005`
- 判断: **两说并列、不裁决**：官方通告记凌晨一点（timeline.004），伊夫林日记记 about ten（timeline.011），这是两份一手史料之间的真实分歧，妮娅明说自己没有资格替史料裁决。烟柱向西北倾斜是东风的可视化（coord.005）。合规 D5：火只做远景，本镜最近的火在街尽头之外，街上的人全部静止旁观、没有人奔跑或呼救。
**2026-09-19 跨段复核改**：原首句「It started about one o'clock.」把凌晨一点当作事实断言，紧接着的第二句又把同一个一点降格成「官方口径之一」、第四句再说自己不裁决——一行台词里自相矛盾。现删首句，由「官方通告说……／伊夫林写……」两句平列开场，立场从头到尾一致，也省出 5 个词的语速余量。

## 视频 prompt

```text
参考: `shot44_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg10-1(场景主体·bg10_伦敦全城燃烧)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `她下到街上。街是空的、黑的，两侧木构架房屋只剩剪影；东南方向的天被一条橙红压出一道边，黑烟柱在天上比城还高，被东风推得向西北倾斜。她并列两条一手史料：官方通告写凌晨一点，约翰·伊夫林写大约十点——两份记载对不上。她不替史料裁决，两个都告诉观众。`
场景: `bg10_伦敦全城燃烧 — 一条橙红的火线沿风推过瓦顶之海，烟把整个白天压成褐黄`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
镜头: `起幅是街心低位广角远景，两侧房屋的黑剪影夹出一条窄天，人很小；镜头缓慢抬起并推向街尽头的东南方向，人退出画面下缘，落幅只剩瓦脊剪影、那条橙红火线与向西北倾斜的黑烟柱。火自始至终留在街尽头之外的远处，不进中景、不进前景。`
走位: `妮娅在画面正中偏左的街心，背对镜头朝东南方向站着，很小。街上另有三两个披着衣服出门的住户站在各自门口朝同一方向看，都站着不动、不说话、不互相搭话；没有人奔跑、没有人推挤、没有人被困、没有伤者。`
动作: `0–6s 她从画面下缘走进来停住，抬头看天；6–14s 她报官方口径，这段里火线几乎不变；14–20s 她报伊夫林那条，镜头开始抬起并推远，她走出画面下缘；20–26s 画面只剩火线与烟柱，烟柱被东风推得向西北明显倾斜，火线在最后两秒里向西北挪过一小段瓦脊。`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: The official account says the fire started at one in the morning. John Evelyn writes that it began about ten. Two accounts that do not agree. I don't get to decide which one is right, so I'm telling you both.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/2 凌晨 —— 底子是全黑：街面、屋顶、人全是剪影；街上没有任何路灯、没有任何公共照明。唯一的光是东南方向远处那条橙红的火线，把云底与烟柱的下缘照出暗红，街面只得到极弱的一层橙红反光。画面里没有人被困、没有尸体、没有血，近处没有任何建筑在燃烧，伦敦桥不在画面里也没有着火。`
节奏: 中慢；两条史料各占一段，中间空两秒让烟柱自己走。
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 26秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 冷静的记述，不煽、不加重音 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 4–20s
台词: The official account says the fire started at one in the morning. John Evelyn writes that it began about ten. Two accounts that do not agree. I don't get to decide which one is right, so I'm telling you both.
时长目标: 16.7s
```
