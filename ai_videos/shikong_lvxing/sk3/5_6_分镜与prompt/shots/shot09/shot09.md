---
segment: 起
section: 过桥
duration: 30s
scene: bg1_旧伦敦桥
view: bg1-1
characters: [c5]
props: []
dialogue: yes
status: 已出prompt
---

# shot09 · 北端空档 · 三十三年没补的口子

## Shot context

- 景别档: 远景0.10 → 中景0.50（机位 `隧道尽头逆光纵深远景` → `北端空档松木挡板前她正面中景`）。**与前一镜的切口**：✅ 比值 8.50 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.city.008`、`london1666.city.013`
- 判断: 全片最好的一个切口（style_guide §5 奇观构图①）：明暗与景别同时跳。北端**必须是空的**——1633 年烧掉的四十二栋到 1666 年仍未重建，底本 Visscher 1616 / de Jongh 1632 画的北段是满的，此处以文字写死空档

## 视频 prompt

```text
参考: `shot09_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg1-1(场景主体·bg1_旧伦敦桥)=>@`，`c5_妮娅(Seedance 人物 entity·现代装态)=>@`，`妮娅声音(c5-2 声样)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `隧道尽头的逆光纵深远景：两侧是黑下去的墙，尽头是一个亮口，她是走向亮口的一个小剪影。她走出去，画面忽然整片打开——房子到这儿就断了，北端只有裸露的石桥面和两侧钉着的松木挡板，天光从缺口整片灌进来。她走到挡板边转身对镜头：1633 年这头烧掉四十二栋，三十三年过去没人补；而明天，正是这道口子让火没能烧过河去`
场景: `bg1_旧伦敦桥 — 被房屋夹死的桥上隧道走到头，天光从 33 年没补上的缺口灌进来`
角色: `妮娅（Seedance 人物 entity · 现代装态）— 深色运动上衣与工装裤、低帮徒步鞋，素色布质胸牌别在左胸；短话筒与麻布采访本随身`
镜头: `一个机位，连续运动、不切。0–10s 隧道尽头纵深远景，35mm，曝光压在亮口上，两侧墙面黑成剪影；10–20s 机位跟出隧道，光比在三秒内整片翻过来，北端的空桥面与松木挡板占满画面；20–30s 她走到挡板边转身面向镜头，机位停住收成中景，身后是敞开的河面与北岸的屋顶`
走位: `0–10s 她背对镜头沿中轴走向亮口，画面里没有别人；10–20s 走出隧道后她偏向画面右侧，左侧留出整段空桥面与挡板；20–30s 她站在挡板前、正面朝镜头、视线落在镜头上，身后画面左侧是松木挡板与挡板外的河，右侧远处是隧道口那排断掉的房屋山墙——**那排房屋在她身后戛然而止，断口一目了然**；零星行人从空桥面上走过，不看镜头、不说话。**本镜她仍是现代装态**——深色运动上衣与工装裤、低帮徒步鞋，素色布质胸牌别在左胸，短话筒与麻布采访本随身；画面里不出现 1666 年的羊毛紧身上衣、羊毛裙、围裙或软帽（`参考:` 行上传的人物 entity 以本行为准）`
动作: `0–6s 她的剪影一步步走向亮口，两侧墙面越来越黑；6–10s 亮口在画面里迅速变大；10–14s 她跨出隧道，抬手在眼前挡了一下光，肩膀明显松开；14–20s 她走到挡板边，右手搭在挡板上、低头看了一眼挡板外的河；20–24s 转身面向镜头开口，左手朝身后那排断掉的房屋山墙一指；24–30s 说到明天那道口子挡住火时，她手放下、看着镜头不动`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: And then — nothing. The houses just stop.
  - 妮娅 · 对镜（对口型）: There was a fire at this end in 1633. Forty-two houses burned. Thirty-three years later, nobody has rebuilt them. There's a plank fence so you don't walk off the edge, and that's it. Tomorrow, this gap is the reason the fire doesn't cross the river.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `隧道段是被夹死的暗，北端空档段是天光全开——这是全片最强的一次光比翻转：上午偏东的日光越过缺口直接铺满裸露的石桥面，松木挡板的新木面是浅黄、旧木是灰褐，桥面石材被晒白起毛；她从冷蓝暗部走进明亮天光，三秒之内整个人从剪影变成受光的正面。画面里没有任何火、没有任何暖色人造光源、天没有暗下来；桥上没有任何路灯、没有任何公共照明装置`
节奏: 暗（走向亮口）→ 翻转（整片打开）→ 搭挡板低头 → 转身说 → 定住
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 放开，笃定 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 8–13s
台词: And then — nothing. The houses just stop.
时长目标: 3.3s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 放开，笃定 ｜ 语速: 中
类型: 对镜 ｜ 时间窗: 21–30s
台词: There was a fire at this end in 1633. Forty-two houses burned. Thirty-three years later, nobody has rebuilt them. There's a plank fence so you don't walk off the edge, and that's it. Tomorrow, this gap is the reason the fire doesn't cross the river.
时长目标: 18.8s
```
