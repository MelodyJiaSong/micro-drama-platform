---
segment: 合
section: 九 · 宵禁与过夜
duration: 30s
scene: bg3_客栈
view: bg3-1
characters: [c5]
props: [p8, p10]
dialogue: yes
status: 已出prompt
---

# shot39 · 九点的钟 —— curfew 就是「盖火」

## Shot context

- 景别档: 全景0.20 → 中景0.55（机位 `客栈院中仰看钟塔方向` → `客栈回廊柱旁平视中景`）。**与前一镜的切口**：✅ 比值 4.25 ≥ 2.0，机位亦不同
- 衔接: 硬切（独立首帧）
- 史实: `london1666.custom.005`、`london1666.custom.006`、`london1666.housing.013`
- 判断: 钟塔本体不入画——bg3 卡里没有钟塔几何，本镜只给钟声与她仰看的方向，避免凭空长出一座塔。「它明天就烧掉了」指 St Mary-le-Bow 本体在大火中焚毁（custom.006）。本镜是笑点清零段的第一镜：同样密度的知识点，但语气必须收住，尾句不许上扬。

## 视频 prompt

```text
参考: `shot39_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg3-1(场景主体·bg3_客栈)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p8-1(物件锚点)=>@`，`p10-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `九点整，Bow Bells 的宵禁钟从城西传过来。妮娅站在客栈院心抬头听。这钟不是「不许上街」的意思——curfew 来自古法语 couvre-feu，字面就是盖火；几百年来它只有一个意思：睡前把炉火压好，免得没人看着的时候城烧起来。镜头下摇，回廊各扇窗里的光一盏盏矮下去、一盏盏灭掉，整座院子照着这道命令在熄火。而敲这钟的那座塔，明天自己就烧掉了。`
场景: `bg3_客栈 — 门洞穿进去是一圈木回廊，院子尽头堆着草`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
道具: `角质提灯：四面刮薄的兽角片嵌在锈黑铁框里，马夫手里那盏点着、回廊下挂着的几盏全程未点；后院敞棚下的干草堆，枯黄、堆到齐胸高，堆在木头墙根下`
镜头: `起幅是院心的仰角广角全景，画面上三分之二是夜空与屋脊的黑剪影，钟声起于画外的西北方向；第一记钟响后镜头极慢下摇并轻微后退，把二层回廊、客房的窗与妮娅一起纳进来，落在她的平视中景。全程手持微呼吸，无变焦、无甩镜。`
走位: `妮娅一人站在院心偏右，面朝院口西北方向仰头；下摇过程中她转身走到回廊的木柱旁停住，侧身朝向镜头左前方，与镜头约三步。二层回廊上另有两名住客在收晾着的布，背对镜头、各做各的，不与她交谈、不看镜头；一名马夫从画右穿过院子走向后院马厩。`
动作: `0–6s 第一记钟响，她仰头静立、不说话，肩随呼吸起伏；6–16s 她讲词源，同时二层第三扇窗里的光被人压矮、第五扇窗的光整个熄掉；16–24s 她走到木柱旁扶住柱子，马夫提着那盏点着的角质提灯从院心横穿出画，院子暗下去一层；24–30s 她说到最后一句时停住不动，第二记钟响，尾音拖长到画面收黑，她始终没有笑、没有耸肩、没有俏皮的收尾动作。`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: Nine o'clock. That's the curfew bell. The word comes from old French — couvre-feu. Cover fire. For centuries that bell has meant one thing: damp down your hearth before you sleep, so the city doesn't burn while nobody's watching. The bell ringing tonight is at St Mary-le-Bow. Bow Bells. It burns tomorrow.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/1 夜 —— 院里没有任何路灯、没有任何公共照明；光只来自回廊各扇窗内的烛光（蜡黄，照不出两米）、马夫手里那盏角质提灯，以及半月的冷白天光。院心只有几块被窗光切出来的浅亮斑，其余全是深褐黑；随着窗里的光一盏盏压下去，院子逐渐更暗。本镜画面里没有任何着火的建筑、天边没有红光、空气里没有烟也没有落灰。`
节奏: 慢。钟声定拍，两记钟之间留白；台词压在钟声的间隙里说，不抢钟、不追钟。
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 30秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 收住的、发凉的平静 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 4–28s
台词: Nine o'clock. That's the curfew bell. The word comes from old French — couvre-feu. Cover fire. For centuries that bell has meant one thing: damp down your hearth before you sleep, so the city doesn't burn while nobody's watching. The bell ringing tonight is at St Mary-le-Bow. Bow Bells. It burns tomorrow.
时长目标: 21.7s
```
