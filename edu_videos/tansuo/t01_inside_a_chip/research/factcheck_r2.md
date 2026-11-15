---
worker_id: factcheck-r2
stage: 3
role: validator
level: factcheck
status: complete
blockers: []
confidence: high
---

# 事实核查 r2：t01 故事大纲 v2.1「新增待核」7 条 + 开关原理措辞

- 核查日期：2026-11-15。
- 核查对象：`story_v2.md`「事实与待核」新增 1–7 条，以及第 8c 场开关原理措辞。
- 核查人没有参与写稿。所有自算用 Python 重算。网页当日用 WebSearch / WebFetch 打开；引文为原文短引（每条不超过 25 个词）。
- 结论三种：**属实**（照用）、**需改**（写明改法）、**不能核**（写明原因）。

## 1. 手机芯片晶体管数 ÷ 世界人口

- **结论：属实（措辞要加「约」，并注明 190 亿是 2023 年的数）**。A17 Pro 190 亿出自 2023 年发布会口播，但 Apple 新闻稿本身没有写这个数；A18 Pro、A19 Pro、A20 Pro 苹果都没公布晶体管数，所以 190 亿仍是苹果手机芯片最新的「官方口径」数字。其他厂商：联发科天玑 9400 为 291 亿（设计方口径，经媒体转述）；天玑 9500 约 300 亿（媒体报道，未见官方原文）；高通骁龙 8 Elite / 8 Elite Gen 5 未公布。
- **依据**：
  - Apple 新闻稿（2023-09-12）https://www.apple.com/newsroom/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/ ："powered by A17 Pro, the industry's first 3-nanometer chip"（全文没有晶体管数）。
  - 190 亿：https://en.wikipedia.org/wiki/Apple_A17_Pro "The A17 Pro contains 19 billion transistors, a 19% increase from the A16's transistor count of 16 billion."（脚注引 AnandTech 发布会直播记录，原页已下线，未能打开）。Tom's Hardware、9to5Mac 同为 190 亿。
  - A20 Pro 新闻稿（2026-09-09）https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/ ："Built using the latest 2-nanometer process technology"（没有晶体管数，也没有主频）。A18 Pro 发布时也没给晶体管数（wccftech 等报道 "the company did not reveal the transistor count"）。
  - 天玑 9400：https://www.theregister.com/2024/10/09/mediatek_dimensity_9400/ "sports 29.1 billion transistors, according to the designers."
  - 天玑 9500：https://heise.de/-10665861 （2025-09-22）"The processor now has around 30 billion transistors."（未标出处）
  - 人口：UN WPP 2024 中方案，2026-07-01 世界人口 8,300,678,396（转引自 https://www.populationpyramids.org/methodology "world, 1 July 2026: 8,300,678,396"；UN 原数据门户未直接打开）。UN https://www.un.org/en/global-issues/population "On 15 November 2022, the world's population reached 8 billion people"；"until 2037— for it to reach 9 billion"。下一版 WPP 推迟到 2027 年，2026 年用的是 WPP 2024 预测值。
- **自算**（Python）：190 亿 ÷ 83.0 亿 = 2.29；291 亿 ÷ 83.0 亿 = 3.51；300 亿 ÷ 83.0 亿 = 3.61。大纲写的「约 81 亿」偏低，2026 年应写「约 83 亿」（结论「每人两个多」不变）。
- **安全措辞**：「一颗手机芯片里有一两百亿个开关——2023 年那颗 A17 Pro 就有 190 亿个，全世界八十多亿人，每人能分到两个多。」
  - 不点名版：「一颗手机芯片里有上百亿个开关，够地球上每个人分两三个。」
- **备注**：
  - 片中若不提芯片名，「一两百亿」与「两三个」都安全；若画面是新款手机，别把 190 亿说成「现在的手机芯片」。
  - 大纲第 1 场台词「这一小片里有一两百亿个开关」：A17 Pro 190 亿、天玑 9400 291 亿，「一两百亿」对苹果成立，对安卓旗舰偏低。若想覆盖两者，说「一两百亿到三百亿」或「上百亿」。
  - 「开关」= 晶体管，片中已定义，可用。

## 2. 倒扣封装：「它干活的那一面朝下」

- **结论：主句属实；「朝下才能直接接到小凸点上」和剖面画法需改**。
  - 属实：手机 SoC 做有晶体管和导线的那一面（正面）朝向主板，这一点对常见的两种手机封装都成立。
  - 需改 1：苹果 A 系列从 A10（2016）起用台积电 InFO 扇出封装，**没有有机基板、也没有传统 C4 凸点**；芯片正面直接做一层很薄的重布线层（RDL），再由焊球接主板。所以「一排小铜凸点 + 带铜层的基板」只对传统倒装叠封（FC-PoP）准确，对苹果芯片不准确。
  - 需改 2：手机常见叠封（PoP）里，**主板上能看到的那块黑色方块往往是叠在上面的内存**，SoC 压在它下面。第 3 场「这块黑的就是芯片吧？」→「黑的是外壳」的说法要考虑这一点。2026 年的 A20 Pro 改成芯片和内存并排，芯片背面直接贴散热均热板（同样是正面朝下）。
- **依据**：
  - 倒装定义：https://en.wikipedia.org/wiki/Flip_chip "it is flipped over so that its top side faces down"；"Chips are flipped and positioned so that the solder balls are facing the connectors"。
  - InFO 没有基板和 C4 凸点：https://www.tsmc.com/english/dedicatedFoundry/technology/InFO "because of no organic substrate and C4 bump."；"high density RDL and TIV to integrate mobile AP w/ DRAM package stacking"。
  - 苹果 A10 起用 InFO-PoP：https://semiconductorx.com/packaging-info.html "Apple A-series iPhone processors from the A10 in 2016 to the A19 in 2025"；"a separate DRAM package stacked on top of a fan-out package"；"NO SUBSTRATE SITS UNDER THE REDISTRIBUTION LAYER"（第三方科普站）。
  - 处理器在下、内存在上：https://sst.semiconductor-digest.com/insights-from-leading-edge/2017/01/iftle-318-2016-imaps-3d-asip-the-expanding-world-of-fan-out-packaging "This is a PoP package with memory on the top … and the processor below."；同文 "TSMC has still not published process flow or cross section"。
  - A20 Pro 并排：https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/ "places the silicon die side by side with the memory"；"allowing A20 Pro to attach directly to a next-generation vapor chamber."
- **推断（未找到台积电原文直接写明）**：InFO 的 RDL 做在芯片正面、焊球从 RDL 一侧接主板、内存经 TIV 从上方接下来，所以芯片正面朝向主板。台积电没有公开工艺流程（见上引），这条是由结构推出来的，第三方资料对「贴片时正面朝上还是朝下」说法不一，但不影响成品里正面朝主板。
- **安全措辞**：「真正的芯片是里面那片薄薄的硅，它是倒扣着装的：做满开关和导线的那一面朝下，对着主板，电和信号从这一面进出。」
- **备注**：
  - 不要说「朝下才能接到凸点上」，改说「朝下，离焊球最近」或「朝下，直接通到下面那层布线和焊球」。
  - 第 4 场爆炸图：若画通用手机芯片，建议画「硅片 → 一层很薄的布线层 → 焊球」，不要画厚基板；或者标「示意」。若要画叠封，顶上应是一块内存，不是空的塑封盖。
  - 第 3 场「黑壳不是芯片」：仍可说「黑色的是外壳」，但别暗示黑壳下面只有一片硅——叠封时上面还压着内存。最简单的做法是画面里的「黑壳」不画成某款真机的样子，只当示意。
  - 「倒扣」对电脑 CPU / GPU 同样成立（倒装是高性能芯片主流），所以片中说「芯片是倒扣着装的」不会错。

## 3. 自算：「每个开关放大到一个人那么大，芯片有多宽」

- **结论：需改**。大纲的「一百七十公里、两个北京」是拿 A20 Pro 的 die 尺寸（8.0×12.3 mm）配 H100 的平均密度（1 亿 / mm²）算的，两组数不属于同一颗芯片；手机芯片实际平均密度约 1.7–1.8 亿 / mm²，比 H100 高。巧的是密度取 1 亿时，「晶体管地盘 100 nm」恰好等于「人缩到 100 nm」，两种算法重合；换成真实手机芯片后两种算法就分开了（见下）。推荐用算法 B，结果仍是「差不多两个北京」，但理由要改。
- **依据（输入数字）**：
  - 晶体管数：A17 Pro 190 亿（见第 1 条）。A20 Pro 没有官方晶体管数，所以不能用 A20 Pro 的面积。
  - A17 Pro die 面积，两个第三方实测不一致：
    - 103.8 mm²：https://wccftech.com/a18-pro-die-size-bigger-than-the-a17-pro-slc-cache-bigger-than-a18/ （2024-10-02）"as it measures 103.8mm²"（文中没写谁量的；同文 A18 Pro 105 mm² 出自 High Yield）。
    - 13.27 × 8.59 mm = 114.0 mm²：https://iphone-mania.jp/?p=606151 （2026-09-19）表格，数据来自 X 用户 Kurnal 的 die 照片测量（可能含划片边，所以偏大）。
    - TechInsights 的 A17 Pro 报告付费，没读到面积。
  - 北京面积：https://english.beijing.gov.cn/beijinginfo/facts/demographicgeography/ "Beijing Municipality covers an area of 16410.54 square kilometres"。
  - 海南岛面积（备选比喻）：海南省概况（商务部转载，注明来源海南省政府网）https://fdi.mofcom.gov.cn/resource/pdf/2020/10/21/500426a68f8a4346a2bf69f16298aa9f.pdf "面积 3.39 万平方公里，是国内仅次于台湾岛的第二大岛"（指海南岛本岛；全省陆地 3.54 万）。
- **自算**（Python）：
  - 每个晶体管平均地盘：103.8 mm² ÷ 190 亿 = 5.46×10³ nm² → 约 **74 nm 见方**（114 mm² 时约 77 nm）。平均密度 1.67–1.83 亿 / mm²。
  - **算法 A：放大到「每个晶体管地盘边长 = 1.7 m」**：倍数 1.7 m ÷ 74 nm ≈ 2,300 万倍（114 mm² 时 2,200 万倍）。放大后面积 = 190 亿 × 1.7² m² = **54,910 km²**（与 die 面积无关），约 **3.3 个北京**；按正方形算边长约 **234 km**（按 Kurnal 长宽比约 190 × 290 km）。
  - **算法 B：按故事里的缩小倍数反推（人 1.7 m → 约 100 nm，即 1,700 万倍）**：die 边长 √103.8 ≈ 10.2 mm → **约 173 km**；按 Kurnal 尺寸为 **146 × 226 km**。面积 30,000–32,900 km²，约 **1.8–2.0 个北京**，或约等于**一个海南岛**（3.39 万 km²）。这时每个晶体管的地盘放大成约 **1.26–1.32 m 见方**——比一个人略矮。
  - 差别：A 比 B 面积大约 1.8 倍（因为手机芯片每个晶体管地盘 74 nm，比故事里人的身高 100 nm 还小）。
- **推荐（前后自洽）**：用**算法 B**。第 10 场前一句刚说「我们缩小了一千七百万倍」，后一句直接「把芯片也放大一千七百万倍」，观众只需记一个倍数；结果说「一两百公里、差不多两个北京」都对。再补一句「到那时每个开关的地盘一米多见方，跟我们差不多大」，回应凯的「要是每个开关都有我这么大」。
- **安全措辞**：「我们缩小了大约一千七百万倍。反过来，把这颗手机芯片也放大一千七百万倍，它会有一两百公里长，差不多两个北京那么大——那时候每个开关的地盘也就一米多见方，跟我们差不多。」
  - 若坚持凯的原问法（算法 A）：「要是每个开关连同它的地盘都放大到一人高，这颗芯片能铺满三个多北京。」
- **备注**：
  - 「地盘」是平均值，包含导线、缓存和空白，不是晶体管本体大小（同 seeing_materials §6.2 A 的限定）。片中说「每个开关的地盘」或「平均每个开关占的地方」，不要说「每个开关有一米多大」。
  - 「一千七百万倍」只在人高 1.7 m、缩到 100 nm 时成立；如果画面里角色缩到别的高度，倍数要跟着改。
  - 「一百七十公里宽」不要再用：芯片是长方形，按 B 算是约 150 × 230 km，说「一两百公里」最稳。
  - 不要把 A20 Pro 的面积和 A17 Pro 的晶体管数混在一起用（A20 Pro 无官方晶体管数）。

## 4. 「电子在导线里挪得比蜗牛还慢」＋弹珠管类比

- **结论：需改**。
  - 对**普通电线**（台灯线、充电线）属实：电子漂移每秒几十微米到零点几毫米，蜗牛每秒约 1 毫米到 1 厘米，电子确实比蜗牛慢几十到上百倍。
  - 对**芯片内部的细导线**不能这么说：芯片导线截面极小，电流密度比家用电线高一万倍以上，按同一公式算，电子漂移可到每秒厘米—米级，可能比蜗牛快。没有找到「芯片内电子漂移速度」的直接权威数值，下面是按公式的自算，但量级足以说明「比蜗牛慢」在芯片里不安全。
  - 弹珠管类比：属实，教科书常用，可以用；需加一条限定（见备注）。
- **依据**：
  - 蜗牛速度：Lauga & Hosoi（2006，腹足类爬行力学）https://ar5iv.labs.arxiv.org/html/cond-mat/0608363 "crawling velocities typically between 1 mm/s and 1 cm/s."（说的是腹足类总体）。另查 Pembury Smith & Ruxton 2021（花园蜗牛实测，J. Zool.）全文只给图，没有可引的数字。
  - 电子漂移（普通铜线）：https://en.wikipedia.org/wiki/Drift_velocity "the electrons are flowing at the rate of 23 μm/s"（1 A、直径 2 mm 铜线；本轮用 n = 8.49×10²⁸ /m³ 重算得 23.4 μm/s，一致）。
  - https://en.wikipedia.org/wiki/Speed_of_electricity "For a current density of 1 ampere per square millimeter, the velocity will be about 0.1 cm/s." **此句数字可疑**：按同一公式重算 1 A/mm² 得 7.4×10⁻⁵ m/s ≈ 0.07 mm/s（约 0.1 **毫米**/秒），比原句小约 14 倍，疑为单位笔误。r1 与 dossier F16 引过此句，建议不要再引这个数，改引 Drift velocity 页的 23 μm/s。同页 "The electrons travel back and forth with the alternating electric potential."
  - 芯片导线电流密度：https://en.wikipedia.org/wiki/Electromigration "The typical current density at which electromigration occurs in Cu or Al interconnects is 10⁶ to 10⁷ A/cm²."；ITRS 2015 Interconnect（https://www.semiconductors.org/wp-content/uploads/2018/06/6_2015-ITRS-2.0_Interconnect.pdf ）"The accelerated scaling of MPU pitch has aggravated the copper electromigration problem."（说明芯片导线电流密度已逼近电迁移极限）。
  - 弹珠类比：Lessons in Electric Circuits https://www.allaboutcircuits.com/textbook/direct-current/chpt-1/conductors-insulators-electron-flow/ "The tube is full of marbles, just as a conductor is full of free electrons"；"An approximate analogy."；"Each individual electron, though, travels through the conductor at a much slower pace."。FHSST 高中物理教材（Wikibooks）同一类比：https://en.wikibooks.org/wiki/FHSST_Physics/Electricity/Flow_of_Charge 。
- **自算**（v = J / (n·e)，铜 n = 8.49×10²⁸ /m³）：
  - 家用线常见 1–10 A/mm²（10²–10³ A/cm²）：0.07–0.7 mm/s → **比蜗牛慢**。
  - 10⁴ A/cm²：7 mm/s（≈ 蜗牛）；10⁶ A/cm²（电迁移开始出现的量级）：0.7 m/s；10⁷ A/cm²：7 m/s。
  - 粗估一根最细导线（截面 12×24 nm）流过 20 µA：约 7×10⁶ A/cm²，漂移约 5 m/s。这是量级估算，截面和电流都是假设值，不是实测。
  - 另外，芯片信号线上的电流是来回充放电，电子大多在原地来回晃，净位移很小——所以「电子没有从这头跑到那头」这个**意思**仍然对，只是不能用「比蜗牛慢」来量化。
- **安全措辞**：「信号一眨眼就传过去了，可电子自己并没有一路跑过去——它们只是在原地挤一挤、挪一小步，就像一管装满的弹珠，这头推进去一颗，那头马上掉出来一颗。」
  - 若一定要用蜗牛：「在家里的电线里，电子自己挪得比蜗牛还慢。」（限定「家里的电线」，不说芯片里。）
- **备注**：
  - 第 6 场画面「导线里琥珀色电子小点慢慢挪」可以保留，表达「电子不是信号」；但不要配「比蜗牛还慢」的字幕或台词。
  - 弹珠类比的限定：弹珠是靠一颗碰一颗把推力传过去的；电线里传得快的是电场（电磁信号），不是电子一个撞一个。片中说到「这头一推那头就出来」即可，不要加「电子一个推一个」。教材原文也自称是「近似类比」。
  - 「那头**立刻**出来」：对家用线可以；芯片里的细导线电阻大，信号要一点时间才传到（RC 延迟），所以用「马上」比「立刻 / 同时」稳。
  - r1 / dossier F16 的「1 A/mm² 约 0.1 cm/s」建议在下一版档案里改成「约 0.1 mm/s」或换用 23 μm/s（本文件不改其他文件，只提示）。

## 5. 继电器：「早年的计算机用继电器——通电时电磁铁把一块铁片吸过去，咔哒一声接通」

- **结论：属实，加一个限定**。继电器原理描述准确（线圈通电 → 电磁铁 → 吸动可动铁片（衔铁）→ 触点接通）。限定：不是所有早年计算机都用继电器——同一时期的 ENIAC 等已用电子管；应说「有些早年的计算机」或直接举楚泽 Z3。举例时首选 **Z3**（逻辑和寄存器都是继电器）；Harvard Mark I 也用了几千个继电器，但它的数字主要存在机械计数轮里、由电机带长轴驱动，不算「纯继电器计算机」；纯继电器的例子还有 Harvard Mark II、Zuse Z2。
- **依据**：
  - 原理：https://en.wikipedia.org/wiki/Relay "A simple electromagnetic relay consists of a coil of wire wrapped around a soft iron core"；"a movable iron armature, and one or more sets of contacts"；衔铁 "makes or breaks … a connection with a fixed contact"。
  - 早期计算机：同页 "the ARRA, Harvard Mark II, Zuse Z2, and Zuse Z3 … used relays for logic and working registers."
  - Z3：https://en.wikipedia.org/wiki/Z3_(computer) "The Z3 was completed in Berlin in 1941."；"built with 2,600 relays … operated at a clock frequency of about 5–10 Hz."（同页规格表另写 "Around 2,000 relays"，数字不一，片中只说「两千多个」）。
  - Harvard Mark I：https://en.wikipedia.org/wiki/Harvard_Mark_I "3,500 multipole relays with 35,000 contacts"；"2,225 counters"；"a 50-foot (15 m) drive shaft coupled to a 5 horsepower (3.7 kW) electric motor"；1944-08-07 交付哈佛。
- **安全措辞**：「有些早年的计算机用的是继电器：线圈一通电变成电磁铁，把一小块铁片吸过去，咔哒一声，两个触点就碰上了——1941 年德国的 Z3 就用了两千多个这样的开关，一秒钟只能走几拍。」
  - 简短版：「早年有的计算机用继电器当开关：一通电，电磁铁把一块铁片吸过去，咔哒一声接通。」
- **备注**：
  - 「一秒钟只能走几拍」对应 Z3 的 5–10 Hz，可以和第 8d 场的「几十亿拍」做对比，效果好且有出处。
  - 继电器也有「通电断开」的接法（常闭触点）；片中只讲「通电接通」不算错，属于简化。
  - 画面：继电器示意画「线圈 + 铁芯 + 可动铁片 + 一对触点」即可；不要画成真空管（那是另一种早期开关）。
  - 片中别提 Mark I 是「继电器计算机」；若要提 Mark I，说「哈佛 Mark I 里也装了三千多个继电器」。


## 6. 手机芯片「一秒几十亿拍」

> 第 6–8 条由主代理在独立核查进程中断后续核（parent-direct）；网页于 2026-11-15 重新打开，不把本段冒充独立审稿。

- **结论：属实，但必须说「时钟走多少拍」，不能说「每个晶体管都开关这么多次」。** 时钟频率是芯片的节拍，不代表所有晶体管每拍都翻转。
- **依据**：Qualcomm Snapdragon 8 Elite Gen 5 官方规格页 https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-elite-gen-5 ："Clocking in at 4.74GHz"；2024 年 Snapdragon 8 Elite 官方产品简介 https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Platform-Product-Brief.pdf ："4.32 GHz peak CPU speeds"。
- **自算**：4.74 GHz = 每秒 47.4 亿个时钟周期；4.32 GHz = 每秒 43.2 亿个时钟周期。
- **安全措辞**：「有些手机芯片的时钟，一秒能走四十多亿拍。」不点名版：「手机芯片的时钟，一秒能走几十亿拍。」
- **不用**：「这个晶体管最快一秒开关几十亿次」——把时钟频率误当成单个器件的保证开关频率。

## 7. 两个晶体管组成一个反相器

- **结论：属实，但反相器是「把输入反过来」，不能泛指任何判断。**
- **依据**：汉堡大学计算机科学系 CMOS 教学演示 https://tams.informatik.uni-hamburg.de/applets/cmos/ ："It consists of only two transistors, a pair of one N-type and one P-type transistor." 同页给出输入 1 输出 0、输入 0 输出 1。
- **安全措辞**：「两个这样的开关就能搭一个反相器：输入一，输出零；输入零，输出一。再把这样的电路一层层连起来，才能做判断、存照片、放视频。」
- **限定**：这里说的是常见 CMOS 反相器，不暗示芯片只含 N 型晶体管，也不在本期展开逻辑门；详细「怎么算一加一」留 t02。

## 8. 开关原理与类比措辞

- **结论：主原理属实；原稿「电子被吸进硅片」「动的只有电场」需改。**
- **依据**：Toshiba MOSFET 教学页 https://toshiba.semicon-storage.com/us/semiconductor/knowledge/e-learning/discrete/chap3/chap3-7.html ：栅源加正电压后，"electrons are attracted to the p-type layer just under the gate insulator film"，形成反型层；反型层构成源漏之间的 N 型通路。既有档案 `seeing_materials.md` §4.1 亦给出绝缘栅、反型层与场效应原文。
- **改法**：
  1. 电子不是从栅极或硅片外被「吸进硅片」，而是**硅里的电子被吸到绝缘层附近**，聚成连续通道。
  2. 关态不要笼统说「硅里没有电子、硅不导电」；说「还没有一条连续的电子通道把两头接通」更准确。
  3. 电场本身不是机械零件在「动」；说「没有机械零件在动，变化的是电场和电子的分布」。
  4. 磁铁隔桌吸铁屑只解释「不接触也能施力」；必须同时说「这里起作用的是电场，不是磁场」，不能用它解释反型层。
  5. Toshiba 图是平面 MOSFET；本片纳米片是栅极四面包围，几何不同，但「栅压经绝缘层控制沟道」的原理相同。
- **安全措辞**：「没加栅压时，还没有一条连续的电子通道把两头接通。栅极隔着极薄的绝缘层加上电压，电场把硅里的电子吸到绝缘层附近，聚成一条通道，两头就通了；撤掉电压，通道消失，又断了。」

## 独立复核与关闭（2026-11-15）

- 第 1–5 条由独立核查员完成；第 6–8 条因原进程中断由主代理续核，再由独立 Kimi 进程复核（`factcheck_r2_review.md`）。
- 第一轮复核要求修改 l28、l42、l46、l50、l54、l69、l72、l73、l77，已全部落实到 `script.md`、`claims.json`、`beats.md`、`story_v2.md`、`learning.json`。
- 第二轮独立复核 `factcheck_r2_review2.md` 判定九项全部解决，无遗留 blocker，同意关闭 r2。
- 第 7 条原先「两个这样的开关」的推荐措辞作废：常见 CMOS 反相器必须明确一个 N 型和一个 P 型晶体管。l73 的分号仅作口语清理，不改事实含义。
