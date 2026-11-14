---
worker_id: factcheck-r1
stage: 3
role: validator
level: factcheck
status: complete
blockers: []
confidence: medium
---

# 事实核查 r1：t01「缩小进芯片」研究档案

- 核查对象：`research/dossier.md` §2 F01–F18、§3「蒙太奇声明」，以及 `angles/scale_structure.md`、`angles/seeing_materials.md` 中对应的出处与原文 quote。
- 核查日期：2026-11-14。所有 URL 都在当日用 WebFetch 重新打开。PDF 下载到会话临时目录后用 pdftotext / PyMuPDF 抽字、抽表格图像核对。
- 核查人没有参与原研究。自算条目全部重算（Python）。
- 本轮 WebSearch 用了 5 次，其余全部是 WebFetch。
- 结论分三种：**属实**（数字和原文一致，可以照用）、**需改**（写明改法）、**未能核**（写明原因）。

## 1. 逐条核查

| 编号 | 结论 | 依据（URL + 原文） | 片中稳妥说法 |
|---|---|---|---|
| F01 晶圆直径 / 厚度 | **属实** | SVM 产品规格 SV029（PDF 解压抽字核对）https://svmi.com/wp-content/uploads/2021/01/SV029.pdf ："Diameter mm 300±0.20"；"Thickness µm 775±25"；"Edge exclusion mm 3.0"。Wikipedia 表同为 775 μm：https://en.wikipedia.org/wiki/Wafer_(electronics) "300 mm … \| 775 μm \| 1999 \| 125 grams[17] \| 640"。SEMI M1 原文未读（付费标准），但两处一致。注意：775 µm 是**出厂晶圆**厚度，不是成品芯片的厚度 | 「一片晶圆直径 30 厘米，厚度还不到 1 毫米。」 |
| F02 每片切多少颗手机芯片 | **属实**（自算可复现） | die 尺寸：https://www.techinsights.com/blog/apple-a20-pro-tsmc-2nm-processor-analysis "The A20 Pro compute die measures approximately 8.0 mm by 12.3 mm, producing an estimated die area of 98.2 mm²."（页面未显示发布日期）。公式与「不计良率」：Wikipedia Wafer 页 "gross DPW calculations do _not_ account for yield loss"。重算：S=98.4 mm² 时 651.2 颗；扣 3 mm 边缘 624.1 颗；再加划片道 610.7 颗，与档案一致。Apple / TSMC 没有公布实际颗数 | 「一片晶圆大约能切出六百多颗手机芯片大小的方块，这还没扣掉坏的。」 |
| F03 代表芯片的晶体管数 | **属实**；可补更新的官方数字 | M4：https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/ "M4 consists of 28 billion transistors built using a second-generation 3-nanometer technology"。GH100：https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/ "fabricated using the TSMC 4N process customized for NVIDIA, with 80 billion transistors, a die size of 814 mm2"。Blackwell：https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/ "pack 208 billion transistors and are manufactured using a custom-built TSMC 4NP process."；"All NVIDIA Blackwell products feature two reticle-limited dies"。**更新**：NVIDIA Rubin GPU 官方 3360 亿，同样是两颗光罩极限 die：https://developer.nvidia.com/blog/inside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai/ （2026-07-21）"Its 336 billion transistors, 224 streaming multiprocessors (SMs), and 896 Tensor Cores…"；工艺和是否已出货，该页没写。Apple M5 新闻稿（2025-10-15）没有晶体管数，所以 M4 的 280 亿仍是 Apple 最新的书面官方数字 | 「一颗电脑芯片 M4 有 280 亿个晶体管；一块 AI 芯片 H100 有 800 亿个。」若要说 Blackwell / Rubin，必须说「两块芯片拼成的一个 GPU」 |
| F04 指甲盖放 500 亿个 | **属实**（研究芯片） | https://research.ibm.com/blog/2-nm-chip （2021-05-06）"enables us to fit 50 billion transistors in a space roughly the size of a fingernail."；图注 "2nm test chip"；"we're still several years away from manufacturing of 2 nm node devices." | 「IBM 在 2021 年做出的一块 2 纳米**试验芯片**，指甲盖大小的地方放了大约 500 亿个晶体管。」 |
| F05 晶体管密度 | **属实**（需加限定） | 由 F03 重算：80e9 ÷ 814 = 9.83×10⁷ 个/mm²，约 1 亿。这是 H100 **整颗芯片的平均值**，包含导线、缓存和空白，不是工艺峰值密度。Wikipedia 2 nm 页把 TSMC N2 列为 313 MTr/mm²（二手，非 TSMC 官方） | 「按 H100 平均算，每平方毫米大约放了一亿个晶体管。」 |
| F06 正面金属层数 | **属实**（第三方实测；只适用于 Intel 这颗电脑芯片） | https://newsletter.semianalysis.com/p/intel-panther-lake-teardown （付费文，引文取自公开部分）"The frontside comprises the M0-M14 signal stack, while the backside comprises the BM0-BM5 power stack."。Wikipedia BEOL：https://en.wikipedia.org/wiki/Back_end_of_line "For modern IC processes, more than 10 metal layers can be added in the BEOL." | 「先进芯片的晶体管上面压着十几层金属导线；Intel 一款新芯片拆开数，正面有 15 层。」 |
| F07 越往上越粗 | **需改**：720 nm 是 IRDS 路线图里的「最粗一档」规格，不是实测的顶层间距；M0 区间混了预测值、PDK 值和实测值 | IRDS 2022 More Moore，Table MM-13（PDF 表格图像读数）https://irds.ieee.org/images/files/pdf/2022/2022IRDS_MM.pdf ：2022 和 2025 两列都是 "Number of P720 layers 2"、"Number of wiring layers - M1+Mx+ >P40 17"；Table MM-7 的 2025 列 "M0 pitch (nm) 20"。实测：SemiAnalysis "Intel 18A PDK provides M0 pitch of 32 nm, but Panther Lake HP libraries shipped at 36 nm"。N3E 23 nm 是 "minimum metal pitch"（Wikipedia 3 nm 页转述 IEDM 2022），不一定是 M0。改法：把来源写成「最细一层 20–36 nm（路线图 20、量产 23–36）；最粗一档按 IRDS 路线图约 720 nm」，不要说成某颗芯片的实测顶层 | 「最底下的导线间距只有二三十纳米，越往上越粗，最上面的要粗几十倍。」 |
| F08 栅极间距 | **属实** | 18A 官方：https://www.intel.com/content/www/us/en/newsroom/news/corporate/intel-foundry-details-process-milestones-future-innovation-at-vlsi-symposium.html （2026-06-16）"Similar to Intel 18A, Intel 18A-P offers two cell heights (180nm and 160nm), a contacted poly pitch of 50nm."。N3：https://en.wikipedia.org/wiki/3_nm_process "contacted gate pitch of N3 is 45 nm, minimum metal pitch of N3E is 23 nm"（引 SemiWiki 的 IEDM 2022 报道，第三方） | 「相邻两根栅极之间，只隔大约 50 纳米。」 |
| F09 标准单元高度 | **属实** | 同 F08 的 Intel 官方新闻稿："two cell heights (180nm and 160nm)"。原句的主语是 18A-P，只说「与 18A 相同」；18A 本身的 180 / 160 另有 wccftech 转述的 VLSI 2025 规格表 "HP/DR Library Height (nm) \| 180/160" | 「一排标准单元的高度大约 160 纳米。」 |
| F10 纳米片 | **需改**：「栅长 12–16 nm」里的 16 是 2022 年 FinFET 的数，「5 nm 厚」是 2034 年的预测 | IRDS 2022 Table MM-7（表格图像读数）2025 列："Lateral GAA (nanosheet) thickness (nm) 6.0"、"Number of vertically stacked nanosheets on one device 3"、"Lateral GAA vertical pitch (nm) 18.0"、"Lg: Gate Length - HP (nm) 14"（HD 也是 14）；2022 列是 finFET，Lg 16/18；2034 列片厚 5.0、叠 4 片。IBM 2 nm："we were able to create a 12 nm gate length"。18A 4 片：SemiAnalysis "Intel 18A uses stacks of four nanosheets each"。改法：写成「3–4 片；每片约 6 nm 厚（路线图量级）；栅长约 12–14 nm」 | 「新一代晶体管把三四片只有几纳米厚的硅薄片叠起来，栅极从四面把它们包住。」 |
| F11 6 nm 约多少层原子 | **属实**（自算可复现） | NIST：https://physics.nist.gov/cgi-bin/cuu/Value?asil "5.431 020 511(89) x 10-10 m"（CODATA 2022）。重算：6 ÷ (0.5431/4) = 44.2 层。前提：沿 [001] 方向按 a/4 数原子层；6 nm 本身是 IRDS 预测值 | 「这么一片硅，大约只有四十多层原子厚。」 |
| F12 「3 / 2 纳米」只是代号 | **需改**（措辞和出处） | IEEE Spectrum（Samuel K. Moore，2020-07-21）https://spectrum.ieee.org/a-better-way-to-measure-progress-in-semiconductors "The picture the semiconductor technology node system paints is false."；"Most of the critical features of a 7-nm transistor are actually considerably larger than 7 nm"。IRDS 2022 原文只说命名没有共识："There is not yet a consensus on the node naming across different foundries and integrated device manufacturers (IDMs)"。「不对应物理尺寸」这句来自 IRDS 2021，是 Wikipedia 的转述："has no direct relation to any actual physical feature"（原文未直接核对）。改法：把「不对应任何物理尺寸」改成「不直接对应」；出处改为「IEEE Spectrum 2020 + IRDS 2021（经 Wikipedia 转述）」 | 「『3 纳米』是一代工艺的名字，芯片里并没有哪个关键结构正好是 3 纳米。」 |
| F13 为什么看不见 | **属实** | NASA：https://science.nasa.gov/ems/09_visiblelight/ "Typically, the human eye can detect wavelengths from 380 to 700 nanometers."。Wikipedia：https://en.wikipedia.org/wiki/Diffraction-limited_system "Considering green light around 500 nm and a NA of 1, the Abbe limit is roughly d = λ/2 = 250 nm"；"can reach about 1.4–1.6 in modern optics, hence the Abbe limit is d = λ/2.8"。重算：380/2.8 ≈ 136、700/2.8 = 250；金属间距 20–30 nm 细 4.5–12.5 倍，栅长 12 nm 细 11–21 倍，合起来「5–20 倍」成立。注意：栅长 12 nm 是 IBM 研究芯片的数 | 「普通光学显微镜最多分清两百纳米左右的东西，芯片里的线条还要细好几倍到二十倍，所以用光看不见。」 |
| F14 SEM / TEM 是灰度 | **属实** | https://en.wikipedia.org/wiki/Scanning_electron_microscope "Electron microscopes do not naturally produce color images."；"For each pixel, this single value is represented by a grey level, forming a monochrome image."；"false color imaging"。IBM TEM 图注："Row of 2 nm nanosheet devices as seen using transmission electron microscopy." | 「工程师用电子显微镜看，拍出来是黑白的；彩色是后来加上的。」 |
| F15 真实颜色 | **属实** | IOActive：https://www.ioactive.com/inside-the-ioactive-silicon-lab-interpreting-images/ "This is the same effect responsible for the colors seen in a film of oil floating on a puddle of water"；"most materials used in integrated circuits are either silvery (silicon, polysilicon, aluminum, tungsten) or clear"；"Copper is the lone exception."。FSU：https://micro.magnet.fsu.edu/chipshots/pentium/index.html "using oblique illumination with blue, red, and yellow gels"；"The appearance of busses, registers, and cache units was enhanced by application of oblique auxiliary illumination" | 「芯片照片里的彩色，多半是薄膜反光干涉出来的，就像水面上的油膜；材料本身大多是银灰色或透明的。」 |
| F16 电子慢、信号快 | **需改**：数字对得上，但「50–99% 光速」说的是一般导线 / 传输线，不能直接套到芯片内部的细导线上 | https://en.wikipedia.org/wiki/Speed_of_electricity "For a current density of 1 ampere per square millimeter, the velocity will be about 0.1 cm/s."；"typically at 50%–99% of the speed of light in vacuum"；"the electrons themselves move much more slowly"。https://en.wikipedia.org/wiki/Drift_velocity "the electrons are flowing at the rate of 23 μm/s"。片内导线的信号速度本轮没有找到出处。改法：t01 只说「电子挪得很慢，信号传得很快」，不给芯片内部的光速百分比；t02 另找片上互连出处 | 「电子自己挪得比蜗牛还慢，真正跑得飞快的是电信号。」（t02 再展开） |
| F17 头发宽排多少栅极 | **需改**：48 nm 来自 Wikipedia 表里的 TSMC N2 数，不是官方数，应换成 Intel 18A 官方的 50 nm | 头发宽：https://www.nano.gov/about-nanotechnology/just-how-small-is-nano "A human hair is approximately 80,000–100,000 nanometers wide."。48 nm：Wikipedia 2 nm 页对比表（二手，TSMC 没有公布 N2 的 CPP）。重算：80 000–100 000 ÷ 48 = 1 667–2 083；÷ 50（18A 官方）= 1 600–2 000。头发宽度另有 17–181 µm 的说法（scale_structure §7），片中要固定一个口径并标注 | 「一根头发的宽度上，大约能并排放下两千根晶体管的栅极。」 |
| F18 H100 ≈ 每人 10 个 | **属实**（要说「约」） | 800 亿出处同 F03。人口：https://www.un.org/en/global-issues/population "On 15 November 2022, the world's population reached 8 billion people"；同页预计 2037 年到 90 亿，所以 2026 年已略多于 80 亿。重算：80e9 ÷ 8.0e9 = 10；按 82–83 亿算约 9.6–9.8。「约 10 个」成立 | 「一颗 H100 里的晶体管，够全世界每个人分大约 10 个。」 |

## 2. 特别核查：手机芯片的官方晶体管数

- **A20 Pro（iPhone 18 Pro，2026-09-09 发布）**：Apple 新闻稿没有晶体管数。全文只有 "Built using the latest 2-nanometer process technology, A20 Pro sets a new bar for mobile computing."，没有出现 "transistor"。
  - 来源：https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/
  - TechInsights 的 A20 Pro 分析页也没有给晶体管数。
- **A19 Pro（2025-09-09）**：新闻稿里没有 "transistor"。
  - 来源：https://www.apple.com/newsroom/2025/09/apple-unveils-iphone-17-pro-and-iphone-17-pro-max/
- **A18 Pro（2024-09-09）**：新闻稿只有定性说法 "a new architecture with smaller, faster transistors"，没有数字。
  - 来源：https://www.apple.com/newsroom/2024/09/apple-debuts-iphone-16-pro-and-iphone-16-pro-max/
- **A17 Pro（2023）**：**190 亿**。这是目前能追到 Apple 自己公布的最新手机芯片数字。
  - 但它只出现在 2023-09-12 发布会的口头介绍里，Apple 的书面新闻稿没有写，原文是 "the industry's first 3-nanometer chip"，不含晶体管数。
  - 可核的记录是转录和报道：Wikipedia「Apple A17 Pro」写 "The A17 Pro contains 19 billion transistors."，引用的是 AnandTech 的发布会直播稿（Bonshor & Smith, 2023-09-12）。9to5Mac 当天也写了 "housing a total of 19 billion transistors"。
  - 本轮没能打开 AnandTech 直播稿原页，所以「Apple 官方」这层只能算**经发布会转录的官方数字**，可信度中。
- **结论**：
  - 截至 2026-11，Apple 近三代手机芯片（A18 Pro / A19 Pro / A20 Pro）都**没有公布官方晶体管数**。
  - 最新可追溯的是 A17 Pro 的 190 亿（2023 年发布会口述）。
  - Apple 最新的书面官方数字是 M4 的 280 亿（2024-05-07 新闻稿），但 M4 是 iPad / Mac 芯片，不是手机芯片。M5 新闻稿（2025-10-15）没有晶体管数。
- **片中说法**：「苹果 2023 年的手机芯片 A17 Pro，官方说有 190 亿个晶体管；之后几代苹果没再公布这个数字。」

## 3. 「蒙太奇声明」（dossier §3）核查

**结论：方向正确，需补三处。** 声明与 `scale_structure.md` §8 第 3 条一致。

1. **画面标签和声明打架**
   - §3 表把「栅极与金属间距」列为「真实比例 / 3D 示意 · 比例准确」。可是这些间距来自 18A 和 IRDS，不是镜头里那颗手机芯片（A20 Pro，TSMC N2）的数，而 TSMC 没有公布 N2 的 CPP 和金属间距。
   - 改法：这几级标「3D 示意 · 量级准确（尺寸取自不同芯片 / 路线图）」，不标「比例准确」。
2. **两套结构不能叠在同一颗芯片下**
   - 18A 有背面供电（PowerVia，背面 BM0–BM5 共 6 层），A20 Pro 所用的 N2 没有。如果在手机芯片下面画出背面供电层，就是把两种芯片的结构拼进了一颗。
   - 晶体管一级也有同样问题：IRDS 是 3 片，18A 实测是 4 片。
   - 改法：画面二选一；或者在切换处让字幕 / 旁白说一句「换一颗 Intel 的芯片来看」。
3. **声明只放在研究档案里不够**
   - 声明要进讲稿：在连续缩小进入单元级之前给一句字幕，例如「以下尺寸取自多种先进芯片」。
   - 台词坚持「先进芯片里的晶体管大致是这样」。这条措辞本身没问题，保留。

## 4. 误导风险清单

1. **一句话论点里的「几百亿个开关」配手机芯片画面**
   - 手机芯片近三代没有官方数字，最新可追溯的是 A17 Pro 的 190 亿（一百多亿）。「几百亿」只对 M4（280 亿）和 AI GPU 成立。
   - 改法：die 用手机芯片时说「上百亿」；说「几百亿」时要点名电脑或 AI 芯片。
2. **「铜导线」**
   - IRDS 2022 Table MM-13 写的是 "Metallization - M0: Co, W, Ru"，2025 年起 M1 / Mx 也写 "Cu, Co, Ru"。最细的几层不一定是铜。
   - 改法：说「以铜为主的金属导线」。
3. **研究芯片当产品**
   - F04 的 IBM 500 亿是 2021 年的 "test chip"。F10、F13 里的「栅长 12 nm」也来自这颗 IBM 研究芯片。
   - 片中提到这些数时，都要说明是「试验芯片」。
4. **预测值当实测**
   - F10 的片厚、片数、栅长，F07 的 720 nm 和 M0 20 nm，都来自 IRDS 2022 路线图预测。
   - 表中 2025 列的 M0 / Mx 间距、2028 年以后的栅长等格子标成红色。IRDS 惯例中这表示「尚无已知量产方案」，但本 PDF 没有附图例，**未核**。
   - 讲稿不能说「现在的芯片就是 6 纳米厚、3 片」，要说「大约」「这一代芯片的量级」。
5. **Wikipedia 表格数当「真实尺寸」**
   - `seeing_materials.md` §1.1 把 TSMC N2 的 48 / 26 nm 写成「当代真实尺寸」。这是 Wikipedia 表格数，TSMC 没有官方公布，本轮也无法确认表格的列对应关系。
   - 改法：不进字幕；需要具体数时用 Intel 18A 的官方数字。
6. **平均密度当峰值**
   - F05 的约 1 亿 / mm² 是 H100 的整颗平均值。说成「先进工艺的密度」会低估约 2–3 倍（Wikipedia 列 N2 为 313 MTr/mm²，二手数据）。
7. **「一颗芯片」的口径**
   - Blackwell 的 2080 亿、Rubin 的 3360 亿都是「两颗 die 拼成的一个 GPU」。和 H100（单 die）并排比较时，要说清楚这一点。
8. **晶圆厚度当芯片厚度**
   - 775 µm 是出厂晶圆厚度。成品芯片通常会背面减薄，具体厚度本轮没有核到出处。
   - 片中不要说「芯片厚 0.775 毫米」。
9. **「光学显微镜看不见」的说法过满**
   - 阿贝极限针对常规光学成像。
   - 改法：说「普通光学显微镜」，避免懂行观众用超分辨显微镜来抬杠。
10. **片内信号速度**
    - 见 F16：不要把「50–99% 光速」说成芯片内部导线的信号速度。
11. **头发口径前后不一**
    - `scale_structure.md` 用 17–181 µm，算出 354–3 771 根栅极。`seeing_materials.md` 和 dossier 用 80–100 µm，算出 1 700–2 100 根。
    - 片中只用一个口径（建议 nano.gov 的 80–100 µm），旁边标「普通头发」。
12. **Intel 18A 不是手机芯片**
    - F06、F08、F09 的实测和官方数都来自 Panther Lake（笔记本芯片）。用它们时，台词说「一款先进电脑芯片」，不要套在手机芯片上。

## 5. 角度文件 quote 的小出入

- `seeing_materials.md` §2.4 的 FSU 引文 "oblique illumination with red and blue gels"，原页实际是 "using oblique illumination with blue, red, and yellow gels"。内容不受影响，应改成原句。
- `seeing_materials.md` §2.2 / §2.4 写铜「未拿到原句」。原句是 "Copper is the lone exception."，可以补上。
- `seeing_materials.md` §4.4 的漂移速度「用前复核」一项已核实："the electrons are flowing at the rate of 23 μm/s"（Wikipedia Drift velocity）。
- `scale_structure.md` §1 的 SVM 规格 quote、§2 的 NVIDIA / Apple quote、§4 的 Intel 与 SemiAnalysis quote、IRDS 2022 MM-7 / MM-13 的表格读数（2025 列：栅距 45、M0 20、M1 23、Mx 24、片厚 6.0、3 片、竖直节距 18.0、Lg 14；布线层 17、P720 层 2），都与原文一致。
- 本轮未核：IRDS 单元高度 HD 114 / HP 138（不在 F01–F18 内）。
