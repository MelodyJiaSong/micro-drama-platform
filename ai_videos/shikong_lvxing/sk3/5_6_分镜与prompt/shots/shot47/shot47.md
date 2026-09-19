---
segment: 合
section: 十一 · 白天
duration: 45s
scene: bg11_坎宁街
view: bg11-1
characters: [c5, c21, c26]
props: []
dialogue: yes
status: 已出prompt
---

# shot47 · 市长 Bludworth —— 全片唯一一句逐字原话

## Shot context

- 景别档: 中景0.55 → 全景0.30（机位 `街心正面平视中景（Bludworth）` → `他背影走进人流的全景`）。**与前一镜的切口**：✅ 比值 2.20 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.people.004`、`london1666.people.005`、`london1666.lang.013`
- 判断: 全片唯一有台词、可对口型的真实历史人物（casting.md §0：同时代人把他**说的话**记成直接引语才可开口）。皮普斯 c26 在画右只留背影、全程不出声、不对口型、不特写（casting.md §2 合规）。那句流传最广的粗话**不在皮普斯日记里**，维基脚注指向 Malcolm《Londinium Redivivum》vol.4（1807，晚 141 年），故不安到他嘴上，只由妮娅点明查无一手出处（people.005 / lang.013）。**妮娅两段画外按 dialogue.md §2 注③「念不完优先砍形容词、不砍事实」压缩**（原 28 + 76 词 → 15 + 38 词），四条事实（国王已下令拆房 / 皮普斯亲自传令 / 那句粗话最早只到 1807 年汇编 / 这句有人当面记下）一条未丢；**Bludworth 那句一个字母未动**。语速账：15 + 30 + 38 = 83 词 ÷ 2.4 = 34.6 s，45 s 里余 10.4 s，其中 4 s 是 8–10 与 24–26 两段硬静默。c21 / c26 的人物锚点卡见 `tools/sk3_data/characters.toml`。

## 视频 prompt

```text
参考: `shot47_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg11-1(场景主体·bg11_坎宁街)=>@`，`妮娅声音(c5-2 声样)=>@`，`c21(人物锚点)=>@`，`c26(人物锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。**本镜没有挂旅行者的人物参考图，因为她不入画**——只挂了她的声样，用于生成画外音。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅的句子全部是画外音，画面里没有她、也没有任何人对这些话做口型；画面里不出现任何文字。
情节: `正午的坎宁街。国王的命令已经下了：拆房，抢在火前面；传令的是皮普斯本人。这就是接到命令的那个人。Bludworth 从人流里被挤出来，脖子上围着一条手帕，气不够、句子断。他停住，对着背对镜头的皮普斯说完那段话，前后各有两秒没有任何人声，然后转身走回人流。接着妮娅画外讲：那句人人会背的话查无一手出处，不在皮普斯日记里，最早只到 1807 年的一本汇编；她不把它安到他嘴上——这句才是他真说过的，而且有人当面站着把它记了下来。`
场景: `bg11_坎宁街 — 一整条街的人都在往外搬东西，连病人带床一起抬走`
角色: `**本镜画面里不出现旅行者妮娅**——她只有画外声。不得依据任何锁定描述符把她画进画面；画面里没有任何现代装或 1666 装的年轻女性主体。`
道具: `Bludworth 脖子上围着一条本白亚麻手帕，打了个松结垂在锁骨前，边角被汗浸出一圈暗痕；他的外衣是炭灰色，前襟沾着灰`
镜头: `起幅是街心正面平视的中景，Bludworth 从画面深处的人流里走出来；他开口时镜头极缓推进到近景（脸的上半部落在褐黄的散光里、没有硬边影子），说完立刻停止推进，随他转身横摇，落幅是他的背影走进人流的全景。镜头不追他、不推特写。`
走位: `妮娅不入画，本镜全程画外；**本镜画面里不出现妮娅本人**——`角色:` 行的锁定串只用于声音与整体风格对齐，不得据此把她画进画面。Bludworth 在画面正中，面朝镜头偏右；他说话的对象皮普斯站在画右前景，只有背影与半个肩膀入画，背对镜头、全程不出声、不转脸、不入特写——**但他不是布景：Bludworth 说话时他的肩背有可读的反应（肩线下沉、抬起的手到胸口又放回），只是从不转脸、不开口、不对口型**。人流从两侧持续穿过他们，没有人停下来看热闹，没有人奔跑、没有人跌倒；画面里没有伤者、没有尸体、没有血、没有人被困。`
动作: `0–8s 他从人流里挤出来、停住，一只手按在膝上喘，另一只手扯了扯脖子上的手帕；8–10s 完全静止，没有任何人声，只有人流的脚步与远处的塌落声；10–24s 他抬起脸说那段话，句子断、气接不上，说到第三句时抬手往拆房的方向指了一下又放下——**画右前景的皮普斯只有背影：他的肩线在第二句上明显往下沉一寸，抬起的右手到胸口就停住、又放回身侧，始终不转脸、不出声、不对口型**；24–26s 说完他闭上嘴，没有人接话，两秒静止——**皮普斯的背影在这两秒里一动不动，只有肩随呼吸极轻地起伏**；26–38s 他转身走回人流，肩背在人群里一点点被淹掉；38–45s 镜头停住，人流继续走过，他站过的位置已经看不出来。`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: The King's order: pull the houses down. Pepys carried it himself. This is the man.
  - c21 Bludworth · NPC（对口型）: Lord! what can I do? I am spent: people will not obey me. I have been pulling down houses; but the fire overtakes us faster than we can do it.
  - 妮娅 · 画外（画外，嘴唇不动）: There's a famous line people put in his mouth. It isn't in Pepys. The earliest source is a compilation from 1807. This is what he actually said, and somebody stood in front of him and wrote it down.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/2 白天 —— 正午的日光被烟滤成褐黄，能见度低，地上没有清晰的投影，人脸上是均匀的散光、没有硬边影子；空气里有细灰在落，落在他的肩上和手帕上。本镜画面里没有明火、没有燃烧的建筑、没有任何火光，火在别处；没有尸体、没有血、没有人被困。`
节奏: 极慢。8–10 与 24–26 这两段两秒静默是本镜的结构，不许填任何人声；**他说话时没有任何画外音压着**。
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 45秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 疲惫、气短、音量偏小（Bludworth）；平述不评判（妮娅画外） ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 0–8s
台词: The King's order: pull the houses down. Pepys carried it himself. This is the man.
时长目标: 6.2s
```

```text
角色: c21 Bludworth ｜ 音色(锁定·全站复用): `en-m-mayor-bludworth-01`
情绪: 疲惫、气短、音量偏小（Bludworth）；平述不评判（妮娅画外） ｜ 语速: 中
类型: NPC ｜ 时间窗: 10–24s
台词: Lord! what can I do? I am spent: people will not obey me. I have been pulling down houses; but the fire overtakes us faster than we can do it.
时长目标: 12.5s
```

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 疲惫、气短、音量偏小（Bludworth）；平述不评判（妮娅画外） ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 26–43s
台词: There's a famous line people put in his mouth. It isn't in Pepys. The earliest source is a compilation from 1807. This is what he actually said, and somebody stood in front of him and wrote it down.
时长目标: 15.8s
```

> **非旅行者台词的合法性**：c21 Bludworth ← london1666.people.004（T0，皮普斯当场目击并记成直接引语）
