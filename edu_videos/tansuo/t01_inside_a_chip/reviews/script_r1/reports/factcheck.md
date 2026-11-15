# 独立事实核查报告（script 第 1 轮）

结论：8 条必改、2 条建议、3 条记录。最严重的是把纳米片说成逐原子层摞出、把到达的点击信号说成从这里发出，以及「一两百亿」与「每人两个多」的范围不成立。

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l03 | 双语 | 必改 | 「一两百亿」包含一百亿；按约八十三亿人，一百亿只能每人约 1.2 个，并非「两个多」。台账的 2.29 来自一百九十亿，不是整个范围。[Tom's Hardware](https://www.tomshardware.com/news/apple-a17-pro-3nm-iphone-15-pro) 记录的也是 A17 Pro 一百九十亿。 | zh：[凯] 就这么一小片，里头有一百九十亿个开关？摊给地球上每个人，都有两个多。可我眼睛都快贴上去了，一个也没看见啊。<br>en：[Kai] This tiny thing has nineteen billion switches? That's more than two for every person on Earth. But I've got my eye practically touching it, and I can't see a single one. |
| l16 | 双语 | 必改 | 焊球多不能只用「同时跟内存、屏幕、摄像头说话」解释；大量焊球还用于供电和接地，高速并行信号也需要许多连接。现句把多因一果说成了单因。 | zh：[林] 门这么多，是因为送电、接地、传数据都要占门，不只是为了同时说话。<br>en：[Lin] So many doorways are needed for power, ground, and data—not just for talking to several parts at once. |
| l19 | 双语 | 记录 | C04 的 lines 包含 l19，但 claim 正文没有登记「硅／二氧化硅／沙子」这一独立事实；事实本身成立，宜明确是化合态的硅元素，避免听成沙子里已有单质硅。 | zh：[林] 对，这片薄硅才是真正的芯片。硅元素，就含在沙子的主要成分——二氧化硅里。<br>en：[Lin] Right. This thin slice of silicon is the real chip. The element silicon is part of silicon dioxide, the main ingredient in sand. |
| l42 | 双语 | 必改 | 台账所据 M0 metal pitch 是相邻导线中心距；英文 spaces between wires 通常指边缘间的空隙，口径变了。中文「间距」也应点明中心距，避免与线宽、空隙混用。 | zh：[林] 可见光波长约四百到七百纳米。最底层相邻导线的中心间距只有几十纳米，比波长小得多，普通光学成像很难分清。就像拿拖把描头发丝。<br>en：[Lin] Visible light has wavelengths of about 400 to 700 nanometers. Neighboring wire centers in the bottom layers are only tens of nanometers apart, so ordinary optical imaging can't resolve them. It's like trying to draw a strand of hair with a mop. |
| l44 | 双语 | 必改 | 电子显微镜原图是灰度，不等于实物「真的」就是灰的；这是成像信号没有可见光颜色信息。研究档案 F15 还明确提到芯片照片可有薄膜干涉色。 | zh：[凯] ……哇，全灰了。原来电子显微镜拍出来是这样，跟老照片似的。<br>en：[Kai] ...Whoa, it's all gray. So that's an electron-microscope image. Like an old photograph. |
| l53 | en | 记录 | Nothing moves at all 比中文「一个零件都不动」更满，字面上连电子也不动，与 l60–l63 的电子重分布相抵触；上下文虽能救回，宜限定机械零件。 | en：[Kai] No mechanical parts move at all... Does it still count as a switch? |
| l67 | 双语 | 建议 | 「加电」容易被理解为接通整机电源；东芝原文分别施加 VDS 与正向 VGS，增强型 N 沟道器件需要足够正的栅源电压才形成沟道，不是任意「有电」就通。 | zh：[林] 就这样。栅极加够正电压，通；撤掉，断。<br>en：[Lin] That's it. Enough positive gate voltage, on. Remove it, off. |
| l74 | zh | 建议 | 英文有「不是每个晶体管每拍都翻转」的必要限定，中文漏掉了；只保留「时钟一秒几十亿拍」，容易延续「每个开关每拍都动」的误解。 | zh：[林] 你看，你那一下到了：栅极亮了，通道通了，信号传给下一个开关。手机芯片的时钟一秒几十亿拍，但不是每个开关每拍都翻。 |
| l75 | 双语 | 必改 | l74 刚说点击信号「到了」，l75 却说它「从这儿亮起来／started right here」，把到达说成发出，信号方向相反。这不是纯人物反应，C19 的 analogy 不能覆盖这个因果说法。 | zh：[凯] 所以我刚才点那一下，真的传到了这儿。……找到你了。<br>en：[Kai] So my tap really did make it all the way here... Found you. |
| l77 | 双语 | 必改 | 「四十几层原子厚」的计算成立，但不能推出器件是「一层一层地」按原子层造出。纳米片工艺先外延 Si/SiGe 叠层，再图形化并选择性去除 SiGe 释放沟道；C17 只登记了厚度，没有登记制造方式。[Semiconductor Engineering](https://semiengineering.com/whats-different-about-next-gen-transistors/) | zh：[林] 按这个六纳米的示意模型算，一片只有四十几层原子那么厚。这么薄的硅片，工程师真的能造出来。<br>en：[Lin] In this six-nanometer illustrative model, each sheet is only forty-something atomic layers thick. Engineers really can make silicon sheets this thin. |
| l78 | 双语 | 必改 | 「每个都是这么一层一层摞出来」把上句的错误制造印象扩展到一两百亿个晶体管，且把六纳米示意模型泛化成所有手机晶体管；C17 不支持这两层推论。 | zh：[凯] ……一两百亿个开关。每一个，都要准确地连进电路。<br>en：[Kai] ...Ten or twenty billion switches. Every one has to be wired into the circuit precisely. |
| l84 | 双语 | 必改 | C18 复算得到的是面积约 3.00–3.29 万 km²，即北京市面积的 1.83–2.01 倍；「两个北京」是面积比较。现句紧接「一两百公里长」，把长度与面积口径混在一起。 | zh：[林] 对，平均每个开关能分到一米多见方。整颗芯片摊开，面积差不多两个北京。这就是指甲盖那么一小片，放得下一两百亿个开关的答案。<br>en：[Lin] Yes. Each switch would get an average patch a little over a meter square. The whole chip would cover about twice the area of Beijing. That's how a fingernail-sized slice can hold ten or twenty billion switches. |
| 全片（C01） | en | 记录 | 数字无误，但台账 quote 的 “The A17 Pro contains 19 billion transistors.” 不是所引页面的逐字原句：Tom's Hardware 用 “boasts”，AnandTech 直播记录为 “19 billion transistors”。原话栏应换成实际原文。 | en：The A17 Pro boasts 19 billion transistors and a 6-core CPU. |

## 核查证据与范围

- **数字与单位**：逐项复算 C01、C02、C03、C10、C17、C18。19×10⁹÷8,300,678,396＝2.28897；1.7 m÷100 nm＝17,000,000，log₁₀＝7.23045；80–100 µm÷50 nm＝1600–2000；6 nm÷(0.5431020511 nm÷4)＝44.1906；放大后平均地盘边长 1.2565–1.3168 m，面积比 1.8280–2.0076。原值见 [nano.gov](https://www.nano.gov/about-nanotechnology/just-how-small-is-nano/)、[Intel 18A](https://www.intel.com/content/www/us/en/newsroom/news/corporate/intel-foundry-details-process-milestones-future-innovation-at-vlsi-symposium.html)、[NIST](https://physics.nist.gov/cgi-bin/cuu/Value?asil)、[北京市政府](https://english.beijing.gov.cn/beijinginfo/facts/demographicgeography/)。这些计算本身无误，问题只在 l03、l42、l84 的表达口径。
- **概念与原文**：C04–C16 已对照 [TSMC InFO](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/InFO.htm)、[IRDS 2022 More Moore](https://irds.ieee.org/images/files/pdf/2022/2022IRDS_MM.pdf)、[IEEE Spectrum 节点命名](https://spectrum.ieee.org/a-better-way-to-measure-progress-in-semiconductors)、[东芝 MOSFET](https://toshiba.semicon-storage.com/us/semiconductor/knowledge/e-learning/discrete/chap3/chap3-7.html)、[汉堡大学 CMOS](https://tams.informatik.uni-hamburg.de/applets/cmos/)、[All About Circuits](https://www.allaboutcircuits.com/textbook/direct-current/chpt-1/conductors-insulators-electron-flow/) 等。除表列项外，未发现把相关说成因果、把预测值说成某手机实测或把弹珠类比当严格模型；可见光 400–700 nm 是 NASA 380–700 nm 的合理约写。
- **翻译与漏登记**：已逐句对照中英文；未发现 part…part 一类份额误译。l53、l74 的语义差异已列出。l16 的单因解释、l75 的信号起点、l77–l78 的制造方式，以及 l19 的化学事实，均不能被对应 claim 正文完整覆盖；其余事实性说法已能在 C01–C19 找到登记或属于明确的故事／类比。
- **画面文字**：所给 lines.md 只有口播对照，没有独立的屏幕文字清单；因此未宣称审查未提供的画面文字。

## 最重要的 3 条

1. **l77–l78**：厚度计算不能证明制造方法；删掉「每个都按原子层一层层摞出来」。
2. **l75**：点击信号是传到这里，不是从这里开始，方向必须改正。
3. **l03**：只有约一百九十亿这个口径才能得到每人 2.29 个，不能让下限一百亿也共享「两个多」。

## 做得好的、别改掉的

1. **l46–l47**：50 nm 明确限定为一种先进工艺的栅极中心间距，1600–2000 的换算正确；「3 纳米是工艺代号，不直接对应某条边」忠实于原文。
2. **l54–l69**：增强型 N 沟道、绝缘栅、电场形成反型沟道、关态仍有漏电都讲对了；磁铁只类比隔空施力且明确电场不是磁场，这个边界要保留。
3. **l35–l39**：把电子局部漂移与信号快速传播分开，没有用「电子逐个碰撞把信号撞过去」的错误说法；弹珠、地铁只承担近似类比的功能。
