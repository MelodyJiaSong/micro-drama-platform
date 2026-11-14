---
worker_id: researcher-02-seeing-materials
stage: 3
role: researcher
angle: seeing-materials
status: complete
blockers: []
confidence: medium
---

# t01「缩小进芯片」研究角度：看见什么 / 什么材料 / 怎么工作

- 研究员：researcher-02（角度 seeing-materials）
- 所有网页查看日期：**2026-11-14**（下文表格「看到日期」一栏统一为此日，不再逐行重复）
- 原文 quote 为英文原文摘录。抓取工具每段引文限 125 字符，长句只摘到关键部分，用 `…` 表示省略。
- 「算式」都是本文自己用出处数字算出来的，出处中没有这些结果。
- 没查到或出处不可靠的内容一律标「未查到」或「不可靠」。

---

## 1. 为什么在这个尺度「看不见」

### 1.1 光的波长比晶体管大得多

- 人眼能看到的光，波长约 380–700 nm（NASA）。
- 光学显微镜的分辨率有物理上限，叫阿贝衍射极限：d = λ / (2·NA)。NA 是物镜的数值孔径，用油浸物镜最高约 1.4–1.6，此时 d ≈ λ/2.8。
  - 算式：380 nm / 2.8 ≈ 136 nm；700 nm / 2.8 ≈ 250 nm。用绿光（500 nm）、NA = 1 时，d ≈ 250 nm（Wikipedia 自带的例子）。
  - 结论：再好的光学显微镜也只能分清相距约 **140–250 nm** 的两个点。
- 当代「2 nm 级」工艺的真实尺寸（Wikipedia 2 nm process 页表格）：
  - TSMC N2：栅极间距（gate pitch）48 nm，最密金属线间距（metal pitch）26 nm。
  - Intel 18A：栅极间距 50 nm，金属线间距 32 nm。
  - IBM 2021 年的 2 nm 演示芯片：栅长 12 nm。
  - 对比（算式）：250 / 26 ≈ 10、136 / 26 ≈ 5，金属线间距比光学极限细 **5–10 倍**；136 / 12 ≈ 11、250 / 12 ≈ 21，栅长细 **11–20 倍**。
- 「2 nm」只是工艺代号，芯片里没有哪个结构真的是 2 nm。Wikipedia 原文说这个名字「has no relation to any actual physical feature」。
- 工厂「印」这些图案用的光比可见光短得多：DUV 248 nm 和 193 nm，EUV 13.5 nm（ASML）。可以给观众一句：连「印图案的光」都得换成看不见的极紫外光。

### 1.2 工程师怎么「看」：SEM、TEM、截面、FIB

- **SEM（扫描电镜）**
  - 有的 SEM 分辨率好于 1 nm。
  - 成像原理：每个像素只记录一个探测器读数，显示成一级灰度，所以原图是**单色灰度图**。
  - 原文：「Electron microscopes do not naturally produce color images.」图上的彩色是后期上的伪彩色（false color）。
- **TEM（透射电镜）**
  - 分辨率远高于光学显微镜，能看到「a single column of atoms」（单列原子）。
  - 动能只有 1 eV 的电子，波长已经短到 1.18 nm，可见光是 400–700 nm。
  - 样品必须薄于 100 nm，电子才能穿过去。
- **FIB（聚焦离子束）**
  - 用来从芯片指定位置切出很薄的切片（lamella），再送进 TEM 拍截面（cross-section）。
  - 原文提到可以从「a semiconductor」的感兴趣区域铣出薄膜。
  - TESCAN 用 FIB-SEM 从 FinFET 上制出了厚度小于 10 nm 的切片，TEM 下能看到清晰的界面、多晶硅和 high-k 栅叠层、鳍的间距和氧化层边界。
- **截面图长什么样**
  - 灰度图，层层叠叠：底部是硅里的晶体管（FEOL），中间是接触层（MOL），上面是很多层金属导线（BEOL）。
  - 现代工艺的 BEOL 可以有 10 层以上金属。2018 年最复杂的芯片超过 15 层。
  - 元素成分图（EDS）能分出 Co、Cu、Si、W、Hf 等元素，这类图的颜色是人为指定的。
  - 用一句话概括画面：灰白相间的层状「千层糕」，每层看起来都是一样的灰。
    - 灰度含义的推断（未查到直接出处）：一般重元素偏亮、轻元素偏暗，具体取决于成像模式。

### 1.3 公开的真实截面 / 电镜图出处（只给链接，没有下载）

| 内容 | 链接 | 说明 |
|---|---|---|
| IBM 2 nm 纳米片晶体管 TEM 图 | https://research.ibm.com/blog/2-nm-chip | 图注：「Row of 2 nm nanosheet devices as seen using transmission electron microscopy.」发布于 2021-05-06 |
| TESCAN：FinFET 小于 10 nm 的 TEM 切片 | https://tescan.com/applications/semiconductors/tem-lamella-preparation/10nm-finfet-lamella | 只有文字描述，页面上不一定有显微图 |
| Bruker：7 nm FinFET 互连层 SEM-EDS 元素图 | https://www.bruker.com/en/products-and-solutions/elemental-analyzers/eds-wds-ebsd-SEM-Micro-XRF/quantax-eds-for-sem/sem-eds-analysis-of-interconnecting-layers-process-finfet.html | SE 灰度图加上各元素的着色图，从下到上依次是 FEOL、MOL、BEOL |
| TechInsights：Samsung SF3（3 nm GAA）SEM 截面 | https://techinsights.com/ja/node/58215 | 大部分内容付费，只能看摘要 |
| Wikimedia Commons：80486 DX2 上层互连的光学显微照片（200×） | https://commons.wikimedia.org/wiki/File:Layers_on_Intel_80486_DX2.png | 是光学照片，不是截面。文件页写明编辑时**提高了饱和度和对比度**。许可 CC BY-SA 2.5 |

### 1.4 本节候选事实表

| claim | 数字 | 出处 URL | 原文 quote |
|---|---|---|---|
| 人眼可见光波长范围 | 380–700 nm | https://science.nasa.gov/ems/09_visiblelight/ | "Typically, the human eye can detect wavelengths from 380 to 700 nanometers." |
| 阿贝极限公式 | d = λ/2NA | https://en.wikipedia.org/wiki/Diffraction-limited_system | "d = λ/2n sin 𝜃 = λ/2NA′" |
| 绿光、NA = 1 时的阿贝极限 | 约 250 nm | 同上 | "the Abbe limit is roughly d = λ/2 = 250 nm (0.25 μm)" |
| 高 NA（1.4–1.6）时的极限 | λ/2.8 | 同上 | "the Abbe limit is d = λ/2.8" |
| 「2 nm」不对应任何物理尺寸 | — | https://en.wikipedia.org/wiki/2_nm_process | "has no relation to any actual physical feature (such as gate length, metal pitch or gate pitch)" |
| TSMC N2 栅极间距 / 金属线间距 | 48 / 26 nm | 同上（表格） | 表格行：TSMC N2 \| 48 \| 26 |
| Intel 18A 栅极间距 / 金属线间距 | 50 / 32 nm | 同上（表格） | 表格行：Intel 18A \| 50 \| 32 |
| IBM 2021 纳米片的栅长 | 12 nm | 同上 | "using three silicon layer nanosheets with a gate length of 12 nm" |
| 光刻光源波长 | 248 / 193 / 13.5 nm | https://www.asml.com/en/technology/lithography-principles/light-and-lasers | "produce light with a wavelength of 193 nm"；EUV "uses light with a wavelength of 13.5 nanometers" |
| SEM 分辨率 | 好于 1 nm | https://en.wikipedia.org/wiki/Scanning_electron_microscope | "Some SEMs can achieve resolutions better than 1 nanometer." |
| SEM 原图是灰度图 | — | 同上 | "Electron microscopes do not naturally produce color images." / "represented by a grey level, forming a monochrome image" |
| 电镜彩图是伪彩色 | — | 同上 | "This method is known as false color imaging." |
| TEM 能看到原子列 | — | https://en.wikipedia.org/wiki/Transmission_electron_microscopy | "even as small as a single column of atoms" |
| 1 eV 电子的波长 | 1.18 nm | 同上 | "Even for electrons with a kinetic energy of just 1 electronvolt the wavelength is already as short as 1.18 nm." |
| TEM 样品厚度 | 小于 100 nm | 同上 | "TEM specimens should be less than 100 nanometres thick for a conventional TEM." |
| FIB 制备 TEM 薄样 | — | 同上 | "FIB is a relatively new technique to prepare thin samples for TEM examination from larger specimens." |
| FinFET 的 TEM 切片厚度 | 小于 10 nm | https://tescan.com/applications/semiconductors/tem-lamella-preparation/10nm-finfet-lamella | "ensured sub-10 nm lamella thickness" / "TEM imaging revealed crisp interfaces and minimal amorphous damage" |
| BEOL 金属层数 | 10 层以上 | https://en.wikipedia.org/wiki/Back_end_of_line | "For modern IC processes, more than 10 metal layers can be added in the BEOL." |
| 最复杂芯片的金属层数（2018） | 15 层以上 | https://en.wikipedia.org/wiki/Interconnect_(integrated_circuits) | 抓取工具只给了转述，没有原句（转述：2018 年最复杂的 IC 可超过 15 层）。**用前需复核原句** |
| IBM 纳米片 TEM 图 | — | https://research.ibm.com/blog/2-nm-chip | "Row of 2 nm nanosheet devices as seen using transmission electron microscopy." |
| EDS 分层元素图（从 BEOL 到 FEOL） | — | Bruker（见 1.3 链接） | "Elemental distribution of different layers of an IC chip from BEOL (top) to FEOL (bottom) identified by SEM EDS." |

---

## 2. 真实颜色

### 2.1 显微镜下芯片的彩色是怎么来的

- 主要原因是**薄膜干涉**，和水面油膜的彩色是同一个原理。
  - 芯片上盖着透明的介质薄膜，主要是二氧化硅和氮化硅这类「玻璃」。
  - 光在薄膜的上表面和下表面各反射一次，两束光互相干涉，有的颜色加强、有的抵消。
  - 膜厚不同，颜色就不同。
- 实际用途：BYU 洁净室的计算器可以从硅片上 SiO₂ / 氮化硅薄膜的颜色反推膜厚。颜色还会随观察角度明显变化。
- 典型的「彩色 die shot」大多是**刻意用彩色光拍的**：
  - FSU 的芯片照片用了斜射照明，加红、蓝、黄色明胶滤光片，并且说这样是为了让结构「enhanced」（更醒目）。
  - Wikimedia 上 80486 那张图在编辑时提高了饱和度。
- 次要原因：周期很密的阵列（比如存储阵列）可能像光栅一样衍射出彩虹色。这一点只有论坛来源（EEVblog），**不可靠，不建议上台词**。

### 2.2 裸 die 本身是什么颜色

- 芯片里的常用材料要么是**银灰色金属光泽**（硅、多晶硅、铝、钨），要么是**透明的**（各种介质玻璃）。
- 铜是唯一明显带颜色的例外，偏红铜色。这一点来自 IOActive 页面，抓取工具转述为「Copper is the exception」，未拿到原句。
- 所以肉眼看裸 die：像一片有金属光泽的灰色小镜子，换个角度会泛出干涉色。
- 很多人以为芯片是绿色的，其实绿色是电路板表面的阻焊层（solder mask），见第 7 节。

### 2.3 「在纳米尺度谈颜色没有意义」有没有权威出处

- 有，但要说得**准确一点**。
- 物理学教授 Christopher S. Baird（West Texas A&M University）的科普问答：
  - 平时看到的物体颜色（反射、折射、吸收）来自很多原子怎样结合、怎样排列，不是单个原子的「颜色」。
  - 可见光波长比原子大约大一千倍。
  - 如果把「颜色」定义得很窄，单个原子「too small to have a color」。
  - 如果把瑞利散射、气体放电发光也算进来，原子「do have a color」。
- 给台词的建议：不要说「纳米世界没有颜色」，绝对化了。可以说：
  - 「这么小的东西，可见光根本分辨不出来，所以你没法『看到』它的颜色。我们画上的颜色，是为了让你分清是哪种材料。」
- 这个说法同时有 1.1 的阿贝极限和 Baird 的文章支撑。

### 2.4 本节候选事实表

| claim | 数字 | 出处 URL | 原文 quote |
|---|---|---|---|
| 芯片彩色和油膜彩色同理（干涉） | — | https://www.ioactive.com/inside-the-ioactive-silicon-lab-interpreting-images/ | "This is the same effect responsible for the colors seen in a film of oil floating on a puddle of water" |
| 两束反射光干涉 | — | 同上 | "The two beams interfere with each other, producing constructive and destructive interference" |
| 芯片材料多为银色或透明 | — | 同上 | "most materials used in integrated circuits are either silvery (silicon, polysilicon, aluminum, tungsten) or clear" |
| 薄膜颜色取决于膜厚 | — | https://en.wikipedia.org/wiki/Thin-film_interference | "Different regions of the film appear in different colors depending on the local film thickness." |
| SiO₂ / 氮化硅膜在硅上的颜色可以计算 | — | https://cleanroom.byu.edu/color_chart | "This calculator displays the color generated by thin films of silicon nitride or silicon dioxide on a silicon substrate." |
| 晶圆检测中用颜色估氧化层厚度 | — | https://journals.spiedigitallibrary.org/conference-proceedings-of-spie/1250/0000/Use-of-color-in-integrated-circuit-inspection/10.1117/12.19708.full | 只看到搜索摘要，没有打开原文，**未取得原句** |
| die 照片用彩色滤光片增强 | — | https://micro.magnet.fsu.edu/chipshots/pentium/index.html | "oblique illumination with red and blue gels" / "enhanced by application of oblique auxiliary illumination with red, green, and blue gelatin filters" |
| 光学 die 照片经过加饱和度处理 | — | https://commons.wikimedia.org/wiki/File:Layers_on_Intel_80486_DX2.png | "Photograph of the upper interconnect layers on an Intel 80486 DX2 taken with an optical microscope at 200x magnification."（加饱和度、对比度一事是文件页转述） |
| 物体颜色来自原子的排列，不是单个原子的颜色 | — | https://wtamu.edu/~cbaird/sq/2014/01/17/does-an-atom-have-a-color/ | "…is therefore a result of how several atoms are bound together and arranged, and not a result of the actual color of individual atoms." |
| 可见光波长约是原子的一千倍 | 约 1000× | 同上 | "visible light has a wavelength that is about a thousand times bigger than atoms" |
| 窄定义下单个原子太小，谈不上颜色 | — | 同上 | "a single atom is too small to have a color" |
| 广定义下原子有颜色 | — | 同上 | "In the sense of Rayleigh scattering and gas discharge atoms do have a color." |

---

## 3. 材料：芯片由什么构成，各在什么位置

自下而上的结构（示意用）：

| 位置 | 材料 | 作用 / 要点 |
|---|---|---|
| 衬底和沟道（FEOL 最底层） | 单晶**硅**。GAA 晶体管把沟道做成几层叠起来的硅纳米片 | 电子在这里流动，栅压控制它通还是断。IBM 2 nm 用了「three silicon layer nanosheets」 |
| 栅介质（包在沟道外面，只有几纳米厚） | **高 k 介质**，以铪基氧化物（HfO₂）为代表，取代了 SiO₂ | SiO₂ 减薄到 2 nm 以下时，隧穿漏电会急剧增加。HfO₂ 的介电常数是 SiO₂（3.9）的 4–6 倍，同样的电容效果下可以做得更厚、漏电更少。Intel 2007 年起采用 |
| 栅电极（包在介质外面） | **金属栅**，取代了多晶硅 | 45 nm 节点起与 high-k 一起回归，由 Intel 带头。Wikipedia 列出的候选金属有 Ta、TaN、Nb（NMOS）和 WN/RuO₂（PMOS）。实际量产的具体配方**未查到**（常见说法是 TiN、TiAl 等，未核实） |
| 接触和局部互连（MOL，把晶体管接到导线） | **钨**（用了二十多年）→ 部分换成**钴**（2018 年起，10 nm 之后）→ **钼**（2025 年开始量产导入） | 钨长期用于填充接触孔和导线。Applied Materials 称钴是 20 年来接触和互连的首次换金属，因为钨、铜在 10 nm 之后「no longer scalable」。Lam 称钼的电阻比钨改善 50% 以上，而且**不需要阻挡层** |
| 多层互连（BEOL，10–15 层以上） | **铜**导线，铜外面包一层阻挡层（Ta、TaN 等） | IBM 1997 年引入铜（Motorola 协助）。铜导电好、更抗电迁移。铜会扩散进硅，在硅里形成深能级陷阱，所以要包阻挡层。铜只能用镶嵌（damascene）工艺制作：先刻沟槽，填满铜，再磨平 |
| 导线之间的绝缘 | **低 k 介质**，例如掺碳氧化物（k 约 3.0）、多孔材料（k 可低于 2.0）；还有空气隙 | 减小导线之间的寄生电容，让信号切换更快 |
| 最细的几层导线（研发中） | **钌**（Ru，用减法刻蚀），加空气隙 | Intel 2024 年 IEDM 发表：在间距 ≤25 nm 处取代铜镶嵌，线间电容最多降 25%。目前**仍是研发**，没有产品时间表 |

> 给台词的提醒：芯片里不是「只有硅」。光是一个晶体管周围，就有硅、铪的氧化物、多种金属、钨 / 钴 / 钼和铜等；并且每代工艺在换材料。

### 3.1 本节候选事实表

| claim | 数字 | 出处 URL | 原文 quote |
|---|---|---|---|
| SiO₂ 太薄会隧穿漏电 | 2 nm 以下 | https://en.wikipedia.org/wiki/High-%CE%BA_dielectric | "leakage currents due to tunneling increase drastically" |
| SiO₂ 的介电常数 | 3.9 | 同上 | "3.9 for silicon dioxide" |
| Intel 用铪基 high-k 配金属栅（45 nm） | 2007 | 同上 | "in conjunction with a metallic gate" |
| HfO₂ 介电常数是 SiO₂ 的 4–6 倍 | 4–6× | https://en.wikipedia.org/wiki/Hafnium(IV)_oxide | "the dielectric constant of HfO2 is 4–6 times higher than that of SiO2, which is 3.9" |
| Intel 2007 年用铪基氧化物替代氧化硅 | 2007 | 同上 | "Hafnium-based oxides were introduced by Intel in 2007 as a replacement for silicon oxide." |
| 45 nm 起金属栅随 high-k 回归 | 45 nm | https://en.wikipedia.org/wiki/Metal_gate | "From the 45 nm node onward, the metal gate technology returns, together with the use of high-dielectric (high-κ) materials" |
| 用钴取代钨和铜（接触和局部互连） | 最多 +15% 性能 | https://www.eejournal.com/industry_news/applied-materials-breakthrough-accelerates-chip-performance-in-the-big-data-and-ai-era/ | "replace tungsten and copper with cobalt to increase performance by up to 15%" |
| 20 年来首次换金属 | 20 年 | 同上 | "First metal change to transistor contact and interconnect in 20 years" |
| 钨、铜在 10 nm 后不再好缩 | 10 nm | 同上 | "no longer scalable beyond the 10nm foundry node" |
| 钨用于接触和导线二十多年 | 20 多年 | https://newsroom.lamresearch.com/2025-02-19-Lam-Research-Ushers-in-New-Era-of-Semiconductor-Metallization-with-ALTUS-R-Halo-for-Molybdenum-Atomic-Layer-Deposition | "void-free fill of contacts and lines for over two decades" |
| 行业正从钨转向钼 | 2025-02-19 | 同上 | "transition from tungsten to molybdenum" |
| 钼比钨的电阻改善 | 50% 以上 | 同上 | "better than 50% improvement in resistance over conventional tungsten metallization" |
| 钼不需要阻挡层 | — | 同上 | "doesn't need an adhesion or barrier layer" |
| 铜互连的引入 | 1997 | https://en.wikipedia.org/wiki/Copper_interconnects | "first introduced by IBM, with assistance from Motorola, in 1997" |
| 铜扩散会损害周围材料 | — | 同上 | "diffusion of copper into surrounding materials would degrade their properties" / "deep-level traps when doped with copper" |
| 阻挡层材料 | Ta、TaN、SiN、SiC | 同上 | 抓取工具转述为「Ta, TaN, SiN, or SiC」作为防扩散层，**未取得完整原句** |
| 低 k 介质减小寄生电容 | — | https://en.wikipedia.org/wiki/Low-%CE%BA_dielectric | "reduces parasitic capacitance, enabling faster switching speeds" |
| 掺碳氧化物的 k | 3.0 | 同上 | "lower the relative dielectric constant to 3.0" |
| 多孔介质的 k | 低于 2.0 | 同上 | "Relative dielectric constants lower than 2.0 have been reported." |
| 钌是替代金属 | — | https://www.intel.com/content/www/us/en/newsroom/news/intel-foundry-unveils-technology-advancements-iedm-2024.html | "subtractive ruthenium, a new key alternative metallization material" |
| 钌用于取代最密几层的铜镶嵌 | — | 同上 | "to replace copper damascene in tight pitch layers" |
| 钌加空气隙降低线间电容（2024-12-07） | 最多 25%，间距 ≤25 nm | 同上 | "up to 25% of line-to-line capacitance reduction at pitches less than or equal to 25 nanometers (nm)" |
| 纳米片宽度（IBM 2 nm） | 15–70 nm | https://research.ibm.com/blog/2-nm-chip | "nanosheet devices ranging from 15 to 70 nm in width" |

---

## 4. 晶体管怎么当开关

### 4.1 一句大白话 + 准确解释

- **大白话**：晶体管像一个「电控水闸」，但没有任何会动的零件。栅极上加电压，硅里就出现一条能导电的通道（开）；撤掉电压，通道消失（关）。
- **准确解释**：
  - 栅极和硅之间隔着一层极薄的绝缘层（现在是 high-k 介质）。
  - 栅极电压在硅表面感应出一层载流子（反型层），在源极和漏极之间形成导电沟道。
  - 栅压超过阈值电压时导通，低于阈值时关断。
  - 电压通过电场控制电导，所以叫「场效应」晶体管（MOSFET）。

### 4.2 速度量级

- **开关速度**：业内常用 FO4（一个反相器带 4 个同样反相器的延迟）衡量门的速度。从约 30 ps（65 nm）降到 10 ps 以下（7 nm FinFET）。更新节点的公开 ps 数值**未查到**。
- **时钟频率**：量产处理器最高加速频率为 i9-14900KS 的 6.2 GHz，也就是每秒 62 亿个时钟周期。
  - 每个周期（算式）：1 / 6.2×10⁹ ≈ 161 ps。
  - 这段时间里，真空中的光走了（算式）：299,792,458 m/s × 1.613×10⁻¹⁰ s ≈ 4.8 cm。
  - 可以用的画面：「芯片一拍的时间里，连光都只跑得过半个手掌。」芯片内导线里的信号比真空光速慢得多，所以这只是上限对比。
- **超频纪录**：2025 年 i9-14900KF 达到 9.12 GHz（Wikipedia Clock rate）。

### 4.3 电子漂移速度 vs 信号传播速度（常见误解）

- 电子本身「挪」得非常慢：
  - 1 A 电流、直径 2 mm 的铜线中，漂移速度约 2.3×10⁻⁵ m/s，即每秒约 23 μm。
  - 电流密度为 1 A/mm² 时约 0.1 cm/s。
- 信号（电磁场）传得快：典型为真空光速的 50%–99%。1850 年测得铜线中约为光速的 2/3。
- 芯片导线里的实际漂移速度、片上信号速度的权威数值：**未查到**。片上细导线受电阻和电容限制，信号速度远低于光速，这是推断，没有找到出处。
- 结论：**不要画「一个电子从晶体管 A 飞到晶体管 B」来表示信号**。信号是一路传过去的「推挤」或电场，电子本身几乎原地慢慢挪。

### 4.4 本节候选事实表

| claim | 数字 | 出处 URL | 原文 quote |
|---|---|---|---|
| 栅压决定导电性 | — | https://en.wikipedia.org/wiki/MOSFET | "the voltage of which determines the conductivity of the device" |
| 反型层形成源漏之间的沟道 | — | 同上 | "The inversion layer provides a channel through which current can pass between source and drain terminals." |
| MOSFET 是数字电路最常用的晶体管 | — | 同上 | "The MOSFET is by far the most common transistor in digital circuits." |
| FO4 门延迟量级 | 30 ps → 小于 10 ps | https://arxiv.org/html/2606.21454 | "from approximately 30ps at 65nm to sub-10ps in 7nm FinFET" |
| 量产 CPU 最高加速频率 | 6.2 GHz | https://en.wikipedia.org/wiki/Clock_rate | "The highest boost clock rate on a production processor is the i9-14900KS, clocked at 6.2 GHz." |
| 超频纪录 | 9.12 GHz（2025） | 同上 | "These records were broken in 2025 when an Intel Core i9-14900KF was overclocked to 9.12 GHz." |
| 频率越高发热越多 | — | 同上 | "the higher the clock rate the more heat produced" |
| 真空光速 | 299,792,458 m/s | https://physics.nist.gov/cgi-bin/cuu/Value?c | "299 792 458 m s-1" |
| 铜线中的电子漂移速度 | 约 23 μm/s（1 A，2 mm 线） | https://en.wikipedia.org/wiki/Drift_velocity | "Assume a current I = 1 ampere, and a wire of 2 mm diameter (radius = 0.001 m)."（结果约 2.3×10⁻⁵ m/s，抓取工具转述，**用前复核原式**） |
| 1 A/mm² 时的漂移速度 | 约 0.1 cm/s | https://en.wikipedia.org/wiki/Speed_of_electricity | "For a current density of 1 ampere per square millimeter, the velocity will be about 0.1 cm/s." |
| 信号传播速度 | 光速的 50%–99% | 同上 | "typically at 50%–99% of the speed of light in vacuum" / "the electrons themselves move much more slowly" |
| 铜线中的信号速度（1850 年测） | 约 2/3 光速 | 同上 | "2/3 the speed of light for copper wire" |

---

## 5. 芯片里的热与电流

### 5.1 功耗与功率密度

- NVIDIA H100（GH100）：800 亿个晶体管，die 面积 814 mm²，TSMC 4N 工艺，SXM5 版本功耗 700 W。
- 平均功率密度（算式）：700 W ÷ 8.14 cm² ≈ **86 W/cm²**。
  - 注意 1：700 W 是整个模块的功耗，包含 HBM 显存等，不全是 GPU die 发出的热。所以 86 W/cm² 是**偏高的粗估上限**。
  - 注意 2：局部热点会高于平均值，但热点的具体数值**未查到**。
- Blackwell（B200 等）：2080 亿个晶体管，两颗光罩极限尺寸的 die，TSMC 4NP。
  - 官方页面上的单卡功耗和 die 面积**未查到**，所以没有算它的功率密度。
- 一个有出处的对比：大气层顶、正对太阳处的阳光强度约 1,360 W/m² = 0.136 W/cm²（NASA）。
  - 算式：86 ÷ 0.136 ≈ **630 倍**。
  - 可用的说法：「指甲盖大小的地方，每平方厘米发出的热，约是太空中正对太阳那一面所受阳光的六百多倍。」以 H100 的平均值估算，说成「几百倍」最稳妥。

### 5.2 「比电炉还热、接近核反应堆」类比的可靠性

- 出处：Intel 的 Fred Pollack 1999 年在 MICRO-32 主题演讲里有一张图，按功率密度把处理器画在 hot plate（电热板）之上，把核反应堆、火箭喷口作为**未来趋势的外推目标**。
- 2026 年一篇资深 CPU 架构师的文章（36Kr 转载）复述了这个说法，并写道核反应堆的类比「often controversial」（常有争议）。
- 原始幻灯片：两个链接都打不开（UCSB 课程 PDF 证书错误，CERN 镜像域名解析失败）。**图上的具体 W/cm² 数值未核实。**
- 结论：
  - 「芯片功率密度超过电热板」：有 1999 年 Intel 演讲作出处，但数字没有核实，可以弱化成「比家里电炉炉面还集中」。说的时候注明这是工程界的经典类比，不要报具体数字。
  - 「接近核反应堆、火箭喷口、太阳表面」：**不可靠**。原图是外推，后人也有争议，而且量纲不同：反应堆功率密度常按体积算（W/cm³），芯片按面积算（W/cm²）。**不建议使用。**
  - 电炉的 W/cm² 数值：**未查到可靠出处**，所以没有自行计算。

### 5.3 本节候选事实表

| claim | 数字 | 出处 URL | 原文 quote |
|---|---|---|---|
| H100 晶体管数 | 800 亿 | https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/ | "with 80 billion transistors" |
| H100 die 面积 | 814 mm² | 同上 | "a die size of 814 mm2" |
| H100 工艺 | TSMC 4N | 同上 | "TSMC 4N process customized for NVIDIA" |
| H100 SXM5 功耗 | 700 W | 同上 | 表格："700 Watts" |
| Blackwell 晶体管数 | 2080 亿 | https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/ | "208 billion transistors" |
| Blackwell 由两颗 die 组成 | 2 | 同上 | "two reticle-limited dies" |
| 大气层顶正对太阳的阳光强度 | 约 1,360 W/m² | https://science.nasa.gov/earth/earth-observatory/climate-and-earths-energy-budget | "the average intensity of solar energy reaching the top of the atmosphere directly facing the Sun" … "is about 1,360 watts per square meter" |
| Pollack 1999：功率密度已超过电热板，预计达到核反应堆水平 | 1999 | https://eu.36kr.com/en/p/3625874431001606 | "that the power density had exceeded that of hot plates and was expected to reach the level of nuclear reactors." |
| 核反应堆类比有争议 | — | 同上 | "the statement about the power density of nuclear reactors is often controversial" |
| H100 平均功率密度（自算） | 约 86 W/cm² | 自算：700 / 8.14 | — |

---

## 6. 一个晶体管多大、一颗芯片有多少个（类比自算）

### 6.1 用到的数字

| 数字 | 出处 |
|---|---|
| H100：800 亿个晶体管，814 mm² | NVIDIA 开发者博客（见 5.3） |
| TSMC N2：栅极间距 48 nm；晶体管密度 313 MTr/mm²（Wikipedia 表格，非 TSMC 官方） | https://en.wikipedia.org/wiki/2_nm_process |
| 人的头发宽 80,000–100,000 nm；一张纸厚约 100,000 nm | https://www.nano.gov/about-nanotechnology/just-how-small-is-nano |
| 世界人口在 2022-11-15 达到 80 亿 | https://www.un.org/en/global-issues/population |
| IBM：指甲盖大小放下 500 亿个晶体管 | https://research.ibm.com/blog/2-nm-chip |

### 6.2 算式

**A. 每个晶体管平均占多大地方（H100）**

- 814 mm² ÷ 8.0×10¹⁰ = 1.0175×10⁻⁸ mm² = 10,175 nm²（因为 1 mm² = 10¹² nm²）
- 开平方：√10,175 ≈ **101 nm**。也就是说，平均每个晶体管占一块约 100 nm × 100 nm 的地盘。
- 这块地盘包含它头顶的导线、缓存、空白区，**不是晶体管本体的大小**。

**B. 「如果晶体管放大成 1 cm 的小方块」**

- 放大倍数：1 cm ÷ 100 nm = 10⁷ nm ÷ 10² nm = 10⁵ 倍。
- die 边长：√814 mm² ≈ 28.5 mm，放大后 28.5 mm × 10⁵ = 2,850 m ≈ **2.85 km**。
- 结论：芯片会变成一块约 **2.9 km × 2.9 km** 的广场，面积约 8.1 km²，地上铺满 800 亿块 1 cm 的方块，而且这只是最底下那一层。

**C. 一根头发的宽度上能并排放多少个栅极（TSMC N2）**

- 80,000 nm ÷ 48 nm ≈ 1,667
- 100,000 nm ÷ 48 nm ≈ 2,083
- 结论：一根头发宽度上能并排放约 **1,700–2,100 个**晶体管栅极。

**D. 一颗芯片里的晶体管和地球人数比**

- H100：8.0×10¹⁰ ÷ 8.0×10⁹ = **10**，相当于地球上每人分到约 10 个。
- Blackwell：2.08×10¹¹ ÷ 8.0×10⁹ = **26**，每人约 26 个。

**E. 一秒数一个，要数多久（H100）**

- 一年的秒数：365.25 × 86,400 = 31,557,600 s。
- 8.0×10¹⁰ ÷ 31,557,600 ≈ **2,535 年**。

**F. 顺带：TSMC N2 每平方毫米有多少晶体管**

- 3.13 亿个/mm²。
- 换算成平均地盘：10¹² nm² ÷ 3.13×10⁸ ≈ 3,195 nm²，约 57 nm × 57 nm。

### 6.3 推荐最直观的两个

1. **C：一根头发宽度上能排约 2,000 个晶体管的「门」。** 观众熟悉头发，也直接回应「为什么看不见」。
2. **D：一颗 AI 芯片里的晶体管，地球上每人能分到 10 个。** 好记，也不需要空间想象。

备选：B（2.9 km 的广场，适合「缩小」的镜头运动）；E（数 2,500 年）。

### 6.4 本节候选事实表

| claim | 数字 | 出处 URL | 原文 quote |
|---|---|---|---|
| 头发宽度 | 80,000–100,000 nm | https://www.nano.gov/about-nanotechnology/just-how-small-is-nano | "A human hair is approximately 80,000–100,000 nanometers wide." |
| 纸张厚度 | 约 100,000 nm | 同上 | "A sheet of paper is about 100,000 nanometers thick." |
| DNA 直径 | 2.5 nm | 同上 | "A strand of human DNA is 2.5 nanometers in diameter." |
| 世界人口 | 80 亿（2022-11-15） | https://www.un.org/en/global-issues/population | "the world's population reached 8 billion people" |
| 指甲盖大小放下 500 亿个晶体管（IBM 2 nm 演示） | 500 亿 | https://research.ibm.com/blog/2-nm-chip | "fit 50 billion transistors in a space roughly the size of a fingernail" |
| N2 晶体管密度 | 313 MTr/mm² | https://en.wikipedia.org/wiki/2_nm_process | 表格值 313（N2 列）。**Wikipedia 二手值，非官方** |
| Apple M3 Max 晶体管数 | 920 亿（2023，3 nm，面积未公开） | https://en.wikipedia.org/wiki/Transistor_count | "92,000,000,000 \| 2023 \| Apple \| 3 nm \| ? \| ?" |
| Intel 4004 | 2,250 个，12 mm²（1971） | 同上 | "2,250 \| 1971 \| Intel \| 10,000 nm \| 12 mm2 \| 188" |
| 平均每个晶体管的地盘（自算） | 约 100 nm × 100 nm | 自算：814 mm² / 8×10¹⁰ | — |
| 头发宽度上的栅极数（自算） | 约 1,700–2,100 | 自算：(80,000–100,000) / 48 | — |

---

## 7. 常见误解清单

| # | 误解 | 纠正 | 出处 URL | 原文 quote |
|---|---|---|---|---|
| 1 | 用够强的光学显微镜就能看见晶体管 | 光学分辨率极限约 140–250 nm，现在的金属线间距 26 nm、栅长 12 nm 级，比它细一个数量级。工程师要用电子显微镜 | https://en.wikipedia.org/wiki/Diffraction-limited_system ；https://en.wikipedia.org/wiki/2_nm_process | "the Abbe limit is roughly d = λ/2 = 250 nm (0.25 μm)" |
| 2 | 「2 nm 芯片」里的晶体管就是 2 nm 大 | 2 nm 只是代号，不对应任何物理尺寸。栅极间距约 48–50 nm | https://en.wikipedia.org/wiki/2_nm_process | "has no relation to any actual physical feature (such as gate length, metal pitch or gate pitch)" |
| 3 | 芯片照片里的彩色就是材料本来的颜色 | 彩色主要来自透明薄膜的干涉。材料本身多为银灰或透明。很多 die 照片还加了彩色滤光片或饱和度 | https://www.ioactive.com/inside-the-ioactive-silicon-lab-interpreting-images/ ；https://micro.magnet.fsu.edu/chipshots/pentium/index.html | "most materials used in integrated circuits are either silvery (silicon, polysilicon, aluminum, tungsten) or clear" |
| 4 | 电镜照片本来就是彩色的 | SEM / TEM 原图是灰度图，彩色是后加的伪彩色 | https://en.wikipedia.org/wiki/Scanning_electron_microscope | "Electron microscopes do not naturally produce color images." |
| 5 | 电信号是电子以光速从一头飞到另一头 | 电子漂移速度只有每秒微米到毫米级；以接近光速传播的是电磁信号 | https://en.wikipedia.org/wiki/Speed_of_electricity | "typically at 50%–99% of the speed of light in vacuum" / "the electrons themselves move much more slowly" |
| 6 | 芯片就是一块硅 | 包含硅、铪基 high-k、金属栅、钨 / 钴 / 钼接触、铜加阻挡层、低 k 介质，最细几层还在研究用钌；上面叠着 10 层以上金属导线 | https://en.wikipedia.org/wiki/Back_end_of_line ；第 3 节各出处 | "For modern IC processes, more than 10 metal layers can be added in the BEOL." |
| 7 | 芯片是绿色的 | 绿色是电路板的阻焊层，裸 die 是金属灰 | https://en.wikipedia.org/wiki/Solder_mask | "Solder mask is traditionally green, but is also available in many other colors." |
| 8 | 芯片热得像核反应堆 | 来自 1999 年的外推图，后人认为有争议，量纲也不同。高端芯片平均约每平方厘米几十瓦（H100 粗估 ≤86 W/cm²） | https://eu.36kr.com/en/p/3625874431001606 | "the statement about the power density of nuclear reactors is often controversial" |

---

## 8. 给画面的建议（示意怎样画才不误导）

1. **开头先「打预防针」**
   - 进入芯片前给一个镜头：光的波浪比晶体管大得多，「光挤不进去」。
   - 向导台词示意：「接下来你看到的颜色和光，都是我们为了讲清楚加上的。真实世界在这个尺度没法用眼睛看。」
   - 画面右下角可以常驻小标签「示意 / Illustration」。
2. **颜色按「材料编码」来画，不当真实颜色**
   - 每种材料固定一种颜色，全片一致，并在出现时说明「这是编码色」。
   - 建议：硅为冷灰蓝；high-k 为薄的半透明层；金属栅、钨 / 钴为银灰；铜可以用铜色（铜本身就偏红，是少数「接近真实」的颜色）；介质画成半透明玻璃，略带干涉彩虹边，正好呼应真实原因。
   - 不要做成霓虹发光的科幻风，那会让观众以为芯片里在发光。
3. **穿插一次「真实感」对照**
   - 引用公开灰度 TEM 截面（如 IBM 2 nm 纳米片的 TEM 图，用前需确认授权），或用灰度风格重画。
   - 告诉观众：工程师真正看到的是这种灰色的「千层糕」。
   - 从灰度图过渡到我们的彩色编码示意，让观众明白两者的关系。
4. **结构比例和层次**
   - 晶体管在最底层，上面是 10–15 层以上越来越粗的铜导线，像立交桥一样一层层往上。
   - 不要把导线画成和晶体管一样大的平面迷宫。
   - GAA 纳米片画成几层叠起来的扁「硅片」，被栅极整圈包住。
5. **材料的质感**
   - 金属是有光泽的实心晶体，介质是玻璃般的非晶质。
   - 要放大到原子级时，再出现规则的硅晶格球点，并提示「这是更放大一千倍的视角」。原子尺度约为可见光波长的千分之一。
6. **电子怎么表现**
   - 不要画单个电子像子弹一样从 A 晶体管飞到 B 晶体管。
   - 推荐做法：导线里挤满缓慢漂移的电子小点，信号用沿导线快速传过去的「波纹 / 推挤」表示，好比水管里一推，出口立刻出水。
   - 晶体管开关：栅极加电时，沟道里「浮现」出一层电子通路（由暗变亮的薄层）；关断时消散。不要画成机械闸门上下移动。
   - 电子不要画成有颜色的小球「本来就是蓝色」，配一句「电子没有颜色，这只是标记」。
7. **时间感**
   - 一个时钟周期（约 160–200 ps）光只走约 5–6 cm，可以用慢动作表现「一拍」。
   - 不要暗示观众能看到开关动作。真实开关是皮秒级，画面一定是极度慢放，加字幕「放慢约 10¹⁰ 倍以上」（数量级为推断：1 秒画面对应约 100 ps 的真实时间）。
8. **热**
   - 用「每平方厘米几十瓦、约为太空中阳光强度的几百倍」这类有出处的对比。
   - 不用「核反应堆」类比。
   - 画面上可以用热浪或红外伪彩色，但标注「温度伪彩色」。

---

### 未查到 / 待复核清单

- 量产金属栅的具体功函数金属（TiN、TiAl 等）：未查到权威出处。
- 最新节点（3 nm / 2 nm）的 FO4 门延迟 ps 值：未查到。
- 芯片热点的功率密度、B200 的官方 TDP 与 die 面积：未查到（没有检索到 NVIDIA 官方页面中的这些数值）。
- 电炉的 W/cm²、Pollack 原图的具体数值：未查到（原 PDF 打不开）。
- 片上导线中的信号速度和漂移速度：未查到专门出处。
- 以下几条在表中已标「复核」，用前需打开原页面核对原句：Drift velocity 的 23 μm/s、Interconnect 页 2018 年「超过 15 层」、Copper interconnects 页的阻挡层材料、铜呈红色的原句。
