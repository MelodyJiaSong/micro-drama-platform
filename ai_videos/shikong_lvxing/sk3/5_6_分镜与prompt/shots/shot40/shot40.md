---
segment: 合
section: 九 · 宵禁与过夜
duration: 24s
scene: bg9_客栈房间夜
view: bg9-1
characters: [c5]
props: [p8, p13]
dialogue: yes
status: 已出prompt
---

# shot40 · 这座城没有路灯

## Shot context

- 景别档: 空镜特写0.00 → 近景0.75（机位 `桌上烛焰微距空镜` → `窗边侧脸近景（烛光擦边）`）。**与前一镜的切口**：✅ 一端无人一端有人，天然跳档
- 衔接: 硬切（独立首帧）
- 史实: `london1666.housing.013`
- 判断: 1666-09-01 不在冬季挂灯期、也在正式制度之前：住户每晚挂灯是大火之后 1668 年的规定，带玻璃罩的路灯 1683 年才第一次装在 Cornhill（housing.013）。所以窗外不是「暗」，是**没有东西可看**——这一条是本站最容易画错的光，窗外出现任何一个光点即为返工。

## 视频 prompt

```text
参考: `shot40_previz.mp4(白模动画·运动与几何参考，不取长相)=>@`，`bg9-1(场景主体·bg9_客栈房间夜)=>@`，`c5_妮娅(Seedance 人物 entity·1666 装态)=>@`，`妮娅声音(c5-2 声样)=>@`，`p8-1(物件锚点)=>@`，`p13-1(物件锚点)=>@`
参考用法: 白模动画决定运动与几何：机位路径、走位、到位时刻以它为准；它是灰色方块，长相、材质、颜色一律不从它取。场景主体给这个地点的形制、布局与材质，照搬；它是在别的时辰出的图，光的方向与明暗一律不从它取，以本镜 `光线:` 为准。妮娅的脸、体型与装束由 Seedance 人物 entity 承载，本 prompt 不写五官。物件锚点锁形制，入画时照搬。台词由视频直接出声：妮娅说英语，对镜的句子对口型、画外的句子嘴唇不动；画面里不出现任何文字。
情节: `她回到房间。桌上一支蜡烛是屋里唯一的光，照不出两米。她走到窗前往外看：外面不是暗，是彻底的黑。住户每晚挂灯要到 1668 年才被规定，带玻璃罩的路灯要到 1683 年才第一次装在 Cornhill。今晚的窗外，一盏灯都没有。`
场景: `bg9_客栈房间夜 — 一支蜡烛照得到的地方就是全部，窗外是彻底的黑`
角色: `妮娅（Seedance 人物 entity · 1666 装态）— 亚麻衬裙外羊毛紧身上衣与羊毛裙，系围裙、戴软帽包住头发，色系是赤褐与枯叶褐一路的 sad colour；胸牌、短话筒、麻布采访本随身；不是全黑清教徒装、帽上没有方形金属扣`
道具: `蜡烛与烛台：白蜡短烛插在锈黑铁烛台上，烛身略歪、蜡泪堆在托盘一侧；角质提灯：四面刮薄的兽角片嵌在锈黑铁框里，挂在门后，全程未点；她的三件不变物——素色布质胸牌、短话筒、麻布封面采访本——放在矮凳上`
镜头: `起幅是桌上烛焰的微距空镜，人不入画，火苗被开门的气流带歪又立住；镜头随她入画向画左横移并轻微后拉，越过烛台，落在她贴着窗的侧脸近景。手持，无变焦。`
走位: `妮娅从画右的门进来，先在桌边停一下（不碰蜡烛、不挡火苗），再走到画左的小窗前，侧身贴窗、面朝窗外；镜头始终在她右后方约四十五度，她的脸只有靠烛光那一侧被擦出一道边，另一侧完全埋在黑里。房里没有别人。`
动作: `0–5s 烛焰被开门的风带歪又立住，门轴响一声；5–12s 她走过来，两手撑住窗台俯身往外看，窗玻璃上映出屋里那一点蜡黄；12–19s 她讲挂灯令与玻璃罩路灯的年份，报年份时语速放慢一拍；19–24s 她不再说话，把额头往窗边又凑近一点停住，窗外自始至终没有出现任何光点。`
台词:
  - 妮娅 · 画外（画外，嘴唇不动）: There is no street lighting in this city. None. Householders won't be ordered to hang out lanterns until 1668, and the first glass lamps don't go up on Cornhill until 1683. Out there it is simply black.
声音: `妮娅的声音：三十岁美国女声，说英语；清亮中音、咬字干净，短跑运动员的呼吸感，语速中偏快、报数字时放慢一拍；笑点自带干脆的收尾；不甜不嗲、不播音腔`；本镜人声由视频直接生成
摄影: `35mm 球面镜头，中等光圈，自然景深；主体清楚，背景软下去——不是全景深；边缘略松、很淡的暗角`
做旧: `木：向阳晒白起毛刺、背阴长霉斑，手握处磨出油亮包浆；瓦：旧瓦哑光、瓦楞积苔与缺角；砖：烟熏与雨痕；布：起毛见织纹、领口袖口发亮、补丁颜色对不上。所有痕迹都是早已结束的冷状态——不冒烟、不发光、不发烫`
光线: `9/1 夜 —— 唯一光源是桌上那支蜡烛，蜡黄，只及一到两米，衰减极快，房间四角是深褐黑。窗外是彻底的黑：没有路灯、没有灯笼、没有任何公共照明、没有火光、没有邻家透出的灯，只有半月的冷白天光在对面瓦脊上留一道极淡的边。窗玻璃上只映得出屋里这一点蜡黄。`
节奏: 慢；台词分两段，中间让窗外那片黑自己占几秒。
渲染样式: 写实纪录片影像，35mm 胶片质感，细腻颗粒，自然肤色，柔和高光滚降，轻微暗角，手持纪录片式轻微呼吸感，景深真实不糊，材质可读（木纹、砖缝、亚麻织纹、瓦面苔痕），无字幕无水印无logo，16:9
比例: 16:9
时长: 24秒
负面词: thatched roof, thatch, straw roof, long vest, waistcoat, Persian vest, three-piece suit, Monument column, Wren dome, baroque dome, tall gothic spire, pilgrim hat, buckled hat, all-black puritan dress, square hat buckle, capotain, potato, tomato, maize, corn on the cob, chilli, fork in commoner hand, teapot, tea service, plague cart, plague doctor beak mask, large glass windows, wide paved boulevard, street lamps, burning London Bridge, 画面文字, 可读招牌, 印刷体, 乱码字母, 字幕, 水印, logo, 人脸变形, 五官漂移, 磨皮, 美颜, 网红脸, 现代服饰, 手表, 眼镜, 墨镜, 塑料, 畸形肢体, 多余手指, 版画线条感, 铜版雕刻纹理, 线描感照片
```

## 台词配音 prompt

```text
角色: 妮娅 ｜ 音色(锁定·全站复用): `c5 视频原声（补录 en-f-vlogger-nia-01）`
情绪: 低、静，被黑压住的紧 ｜ 语速: 中
类型: 画外（画外，嘴唇不动） ｜ 时间窗: 5–19s
台词: There is no street lighting in this city. None. Householders won't be ordered to hang out lanterns until 1668, and the first glass lamps don't go up on Cornhill until 1683. Out there it is simply black.
时长目标: 15.4s
```
