# 好老师独立审稿（script 第 1 轮）

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l07 | 双语 | 必改 | “那个开关 / the switch”把一次点击说成只拨动唯一开关，容易形成错误心智模型。 | 中：那咱们就跟着这一下进去，找到被它拨动的一个开关。<br>EN: Let's follow that tap inside and find one of the switches it flips. |
| l24 | 双语 | 必改 | 一句塞入 CPU、GPU、缓存，普通观众无法同时吸收；“缓存像小区”只像外形，没映射缓存的作用。删去后两个名字和小区类比。 | 中：这块是 CPU。其他区域先不记名字，后面只看它们共同的东西：最底下的开关。<br>EN: This is the CPU. Let's skip the other names and focus on what these regions share: the switches at the bottom. |
| s10 | 双语 | 必改 | 高速公路、小巷、织布分别对应“远路／近处、粗稀／细密、分层交叉”，但只讲“像什么、做什么”，没讲清为什么这样分层；O2 因此只有部分支撑。 | l33 中：上层要送电、跑远路，所以像高速公路，又粗又宽；靠近开关的连接短而多，所以下层像小巷，又细又密。<br>EN: The upper layers carry power and signals over long distances, so they're thick highways. Connections near the switches are short and numerous, so the lower layers are thin, crowded alleys.<br>l34 中：一层南北、一层东西，交叉的线路才不会碰上；要上下接通，就走这些短柱。<br>EN: Alternating directions let routes cross on separate layers without touching; these short posts connect selected points vertically. |
| s11 | 双语 | 必改 | 弹珠和地铁都对应“个体只挪一点、变化向前传”，但没比较两个例子，也没说电子并非机械碰撞；“马上掉出来”还可能让人以为传递不需要时间。 | l38 中：像一管弹珠：这头一推，那头很快有反应，不是一颗弹珠跑完全程。<br>EN: Picture a packed tube of marbles: push one end and the other responds quickly; no marble travels the whole way.<br>l39 中：地铁也一样：每个人都只挪一点。可电子不是靠碰撞传劲，是电场在传，而且也需要时间。<br>EN: The train is the same: everyone moves only a little. But electrons don't pass on a mechanical shove; the field carries the change, and that takes time. |
| l44 | 双语 | 必改 | “真东西长这样”把灰度电子显微镜图像说成物体的真实外观，会制造“纳米器件本来就是灰色、可被直接看见”的新误解。 | 中：……哇，全灰了。原来电子显微镜拍出来是这样，像老照片；可这不是肉眼看到的颜色。<br>EN: ...Whoa, it's all gray. So that's what an electron-microscope image looks like—like an old photo, not what our eyes would see. |
| l48 | 双语 | 建议 | “就是个名字 / basically just a name”容易从“不是物理尺寸”过度纠正成“没有技术含义”。车型类比本身可由 l47 保留。 | 中：原来三纳米不是晶体管的尺寸，而是一代工艺的名字。<br>EN: So “three nanometers” isn't a transistor measurement; it names a generation of manufacturing technology. |
| l54 | 双语 | 必改 | 英文突然堆出 enhancement-mode、N-channel、MOSFET，中文又漏掉“增强型”这一通断前提；两种叫法都没有照顾新手。 | 中：先看一种增强型 N 型晶体管：栅极没加电压时，它为什么是断的？<br>EN: Let's take one enhancement-mode N-type transistor: with no gate voltage, why is it off? |
| s15 | 双语 | 必改 | 桥与路对应“硅片／电子通道”，但“中间还没有路、把路变出来”没说明类比边界，容易让人以为断开时中间真的缺材料、通电时新建实体道路。 | l57 中：所以硅片一直都在；断的是里面的电子通道，不是中间少了材料？<br>EN: So the silicon stays; it's the electron path that's missing, not material?<br>l58 中：对。没有新路出现，看栅极怎么让电子连成通道。<br>EN: Right. No road appears. Watch the gate gather electrons into a path. |
| l59 | 双语 | 必改 | 绝缘层只被说成“没贴在一起”，没有讲它同时挡住栅极电流；因此 Q4 所考“拿掉绝缘层会怎样”在讲稿里没有支撑，磁铁类比也不能补这一点。 | 中：栅极和硅片隔着极薄的绝缘层：电场能作用过去，正常时栅极电流却不会直接灌进硅里。<br>EN: A very thin insulator separates the gate and silicon: the field acts through it, but in normal operation gate current can't simply flow into the silicon. |
| l69 | zh | 建议 | 前文一直叫“通道”，这里突然改叫“沟道”，又新增“关态漏电”术语；同一概念应保持一致。 | 栅极包得越完整，对通道的控制通常越好，断开时也更容易减少漏电。但断开不等于绝对不漏，仍可能有少量电流通过。 |
| l73 | 双语 | 必改 | P 型、CMOS、反相器一次涌入；又从单个反相器直接跳到“存照片”，容易误以为反相器本身能存储。只保留一个有用的“反相”心智模型。 | 中：把两个不同的开关配合起来，能做成反相器：输入一，输出零；输入零，输出一。它自己不能存照片，要和其他不同电路组合，才能判断、存照片、放视频。<br>EN: Two different switches can work together as an inverter: one becomes zero, and zero becomes one. It can't store photos by itself; that takes other circuits. Different circuits together let a chip make decisions, store photos, and play videos. |
| l74 | 双语 | 必改 | 本段已有反相器，又新增“时钟”；更关键的是英文说“并非每个晶体管每拍都翻转”，中文漏掉这层限定，容易让人以为所有开关每秒都通断几十亿次。 | 中：你看，你那一下到了：栅极有电压，通道形成，信号接着传给下一个开关。这样的变化一秒能发生几十亿次，但不是每个开关每次都变。<br>EN: Look, here's your tap. Voltage on the gate forms the channel, and the signal passes to the next switch. Changes like this can happen billions of times a second, but not every switch changes each time. |
| l75 | 双语 | 必改 | l74 刚说点击信号“到了”，l75 又说“从这儿亮起来 / started right here”，把经过此开关误说成由此开关发起，与信号路径矛盾。 | 中：所以我刚才点那一下，信号也传到了这儿。……找到你了。<br>EN: So the signal from my tap reached this switch too... Found you. |
| l78 | 双语 | 建议 | “每个都是这么一层一层摞出来”可能让人以为一两百亿个开关被逐个组装；这里适合点破并行制造，而不是只留惊叹。 | 中：……一两百亿个，都是在整片硅上一起做出来的。<br>EN: ...Ten or twenty billion of them, all made together across the silicon. |

## 必查项核查证据

- **例子与类比总账**：改 l24 城市／小区、s10 公路／小巷／织布、s11 弹珠／地铁、l44 老照片、l48 车型余韵、s15 桥／路；其中 l24 的“缓存＋小区”应删。留 l03“每人两个多”、l10 米山／发崖、l14–17 停车场／门、l31 立交桥、l42 拖把描头发、l47 车型、l51 继电器、l65 隔桌磁铁、l77 原子层、l79–85 先猜再反向放大。留项中，城市颜色由 l25 点破是后加，织布由分层和短柱限定，拖把由波长解释限定，车型由“不对应哪条边”限定，磁铁已点破电场不是磁场；其余未见实质误导。
- **两个不同例子并比较**：已满足。l51–52、l63 把继电器的机械接点与晶体管的电场控制 explicitly 对比，不只是连续堆两个例子；弹珠与地铁的比较不足已单列为 s11。
- **认知提升**：芯片“封装—薄硅—导线—开关”的层级、电场聚成电子通道、反向放大的尺度感都是可复用心智模型，不只是定义；开关的“为什么”由 l56–63 讲清，导线分层的“为什么”需按 s10 补足。
- **误解**：已明确点名并驳斥多个常见误解，包括 l12–13“黑块就是芯片”、l35–37“电子跑得和信号一样快”、l45–47“3 纳米是某条边”、l49–63“开关一定要有活动零件”、l69“关态绝对零漏电”；新制造的风险见 l44、l48、l57–58、l75、l78。
- **启发**：l83–85 把缩小反转为芯片放大，提供可继续想的尺度视角；l90“只会通断，怎么算一加一”是自然追问。全片没有使用“学习即压缩”，不存在该视角的过度引申。
- **术语**：封装、焊球、导线、栅极均有先看物或先提问再命名；“3 纳米”这个误导性名字由 l47 直接点破。集中越界的是 l24、l54、l73–74，叫法漂移见 l69。
- **学习目标**：O1 有 l13、l15、l20、l30、l88 清楚支撑；O2 有 l32–34 对应但缺原因，需补；O3 的零栅压断、加栅压聚电子成通道、撤压断、无机械运动、关态漏电分别有 l54–67、l69 支撑，但 Q4 还缺 l59 的阻流作用；O4 有 l42–43 支撑，l44 需避免反向误导；O5 有 l46–47、l50、l77、l81、l84 清楚支撑。

## 最重要的 3 条

1. **l59**：补上绝缘层“让电场作用、阻止栅极电流直接进硅”的作用，否则通关题 Q4 无讲稿依据。
2. **l73–74**：删掉术语堆叠，区分反相与存储，并补齐中文的“并非每个开关每次都变”。
3. **l07、l75**：统一成“点击信号经过许多开关，此处是其中之一”，不要说成唯一开关或信号起点。

## 做得好的、别改掉的

1. l49–67 用继电器作对照，再以“无栅压断—加栅压聚电子成通道—撤压断”完整回答为什么，是全片最强的机制讲解。
2. l79–85 先让观众猜缩小倍数，再反向放大芯片，把抽象密度变成米与城市尺度，惊叹服务于概念。
3. l88–91 先由凯讲回来，再留下“通断怎样变成加法”的问题，既回收全片又自然保留下一期动力。
