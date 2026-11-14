---
worker_id: researcher-03-fab-process
stage: 3
role: researcher
angle: fab-process
status: complete
blockers: []
confidence: medium
---

# 角度：制造流程与晶圆厂（fab-process）

- 查阅日期：所有条目均为 **2026-11-14** 查看。
- 引文怎么来的：网页经 WebFetch 抽取原句（工具会做摘要，引号内是它返回的原文句子）。Intel 两份 PDF（Sand-to-Silicon 2012、Manufacturing 101 2023/2024、What does it take to build a fab 2022）由本人直接读 PDF 页面核对；ASML 2025 年报 PDF 用 pypdf 抽取原文核对。凡标「仅搜索摘要」的，说明原页没打开（403 或配额不够），只能当线索，**不能直接写进片子**。
- 「官方」指公司或标准机构自己的页面、PDF。Wikipedia、行业媒体、分析机构都算「第三方」。
- 画面禁用规则提醒：下面出现的 Intel / ASML / TSMC / Samsung / Muratec 等名字只是事实出处，不能出现在画面里，也不能出现在角色台词的品牌露出中。

---

## 1. 从沙子到芯片：主线流程

| # | 步骤 | 在干什么（一句话） | 关键数字（有出处的才写） |
|---|---|---|---|
| 1 | 石英砂 | 硅是地壳里含量第二多的元素，普通砂子含硅比例很高。 | 未查到工业「砂→冶金级硅」的官方工艺数字。Intel Tech101 写的是「砂加镁粉加热」，这更像教学或实验室方法。工业上用碳热还原电弧炉，但本次**未查到出处**，片中不要写「镁粉」，也不要写电弧炉的细节。 |
| 2 | 多晶硅（电子级） | 冶金硅先用 HCl 变成三氯氢硅，蒸馏提纯后在约 1000 °C 的反应器里沉积到硅芯棒上，这就是西门子法。 | 杂质在 ppt（万亿分之一）量级（Wacker）。Intel 的说法是「少于十亿分之一的外来原子」。纯度「11N」是第三方给的现实上限（Bernreuter），「12N」被指为营销说法。 |
| 3 | 单晶硅锭（直拉法 Cz） | 把籽晶浸入石英坩埚里的熔融硅，边转边往上拉，长成一整根连续无断裂的单晶圆柱。 | Intel（2012）：直径 300 mm，约 100 kg。Wikipedia：最长约 2 m，重「数百公斤」。两者口径不同，**片中建议说「约一个人那么高、比人重好几倍」这种量级，或者干脆不报重量**。 |
| 4 | 切片、抛光 | 硅锭切成薄圆片，再抛光到镜面般无瑕。 | 直径 300 mm。厚度：Intel 写「约 1 mm」，Wikipedia 写「约 0.75 mm」。两个出处不一致，建议说「不到 1 毫米」。300 mm 晶圆在 2000 年开始引入。 |
| 5 | 前道 FEOL | 在硅里直接做出晶体管。循环做这几步：氧化/沉积（含 ALD 原子层沉积）→ 涂胶 → 光刻曝光 → 显影 → 刻蚀 → 离子注入 → 去胶 → CMP 平坦化。 | 一片晶圆最多要经过约 50 次光刻循环（Wikipedia）。工序总数：「300 道以上」（Wikipedia）、「600～1000 道以上」（SemiEngineering 2017）、「数百道」（Intel）。**建议说「几百到上千道工序」**。 |
| 6 | 后道互连 BEOL | 在晶体管上方一层层做金属导线（铜电镀加 CMP 磨平），层与层之间用介质隔开。 | 金属层：「11 层或更多」（Wikipedia）；Intel（2012）说芯片「可能有 30 多层」，这是含所有层的总数。 |
| 7 | 晶圆测试（wafer sort） | 探针台一颗颗扎针，喂测试图形，比对「正确答案」。 | 无数字。 |
| 8 | 切割（singulation/dicing） | 把晶圆切成一颗颗裸片（die）。先减薄（背面研磨）再切。 | 无数字。 |
| 9 | 封装与终测 | 裸片装到基板上，加散热盖，再做功能、性能、功耗终测，然后分档（binning）。 | 无数字。 |
| 10 | 先进封装 | CoWoS 用中介层把计算芯片和 HBM 拼在一起。HBM 是多层 DRAM 用 TSV 加微凸点垂直叠起来。Chiplet 指把一颗大芯片拆成多颗小芯片再拼装。 | TSMC 2026-04：已在量产 5.5 倍光罩尺寸的 CoWoS；14 倍光罩尺寸版本（约 10 颗大计算芯片加 20 个 HBM 堆栈）计划 2028 年量产。HBM：每堆 4/8/12/16 层 DRAM 叠在 1 颗基底逻辑芯片上（Wikipedia）。 |

**周期（投片到出厂）**：
- 第三方数字：每层 1–1.5 天。28nm 约 40–50 层光罩、40 天；14/10nm 约 60 层、60 天；7nm 预计 80–85 层、80–85 天（SemiEngineering 2017，引 KLA-Tencor）。另一个说法是晶圆制造「最长 15 周，业界平均 11–13 周」（Wikipedia）。
- **2nm/18A 这一代的光罩层数与周期：未查到出处**，片中只能说「几个月」「几十层光罩」。
- 官方给出的周期数字：未查到。

**FEOL / BEOL 定义**（Wikipedia）：FEOL 在硅里做晶体管，BEOL 做被介质隔开的金属互连线。

### 候选事实表（第 1 节）

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 硅是地壳第二丰富元素 | 第 2 | https://download.intel.com/newsroom/kits/chipmaking/pdfs/Sand-to-Silicon_22nm-Version.pdf （p3，2012-01） | "Silicon is the second most abundant element in the earth's crust. Common sand has a high percentage of silicon." | 官方 |
| 芯片用硅纯度 | <1/10⁹ 外来原子 | 同上 p3 | "silicon must be purified so there is less than one alien atom per billion." | 官方 |
| 多晶硅杂质量级 | ppt | https://reports.wacker.com/2022/annual-report/sustainable-solutions/purity-is-our-recipe-for-success.html | "We're talking about concentrations of critical impurities in the parts-per-trillion range" | 官方（Wacker 年报） |
| ppt 的比喻 | 10 g 糖 / 100 亿升水 | 同上 | "One ppt corresponds to a concentration of 10 grams of sugar in ten billion liters of water." | 官方 |
| 西门子法温度 | ≈1000 °C | 同上 | "feeding trichlorosilane into reactors at a temperature of about 1,000 degrees Celsius" | 官方 |
| 冶金硅→三氯氢硅 | — | 同上 | "is converted to liquid trichlorosilane using hydrogen chloride" | 官方 |
| 纯度现实值 11N，12N 不存在 | 11N | https://www.bernreuter.com/newsroom/polysilicon-news/article/a-silicon-purity-of-12n-only-exists-in-the-world-of-marketers/ （2025-10-01） | "one might talk of a purity of 11.5N in the best case; more realistic is a level of 11N." / "Such a silicon purity simply does not exist." | 第三方（分析机构） |
| 9N 的说法 | 9N–11N | 仅搜索摘要（市场报告页，未打开） | — | 第三方·未核验，不建议使用 |
| 硅锭尺寸与重量 | 300 mm / ≈100 kg | Intel Sand-to-Silicon p3 | "The ingot has a diameter of 300mm and weighs about 100 kg." | 官方（2012，较旧） |
| 硅锭最大长度与重量 | ≤2 m / 数百 kg | https://en.wikipedia.org/wiki/Monocrystalline_silicon | "a monocrystalline cylindrical ingot up to 2 meters in length and weighing several hundred kilograms" | 第三方 |
| 直拉法动作 | — | 同上 | "dips a precisely oriented rod-mounted seed crystal into the molten silicon" | 第三方 |
| 晶圆厚度（Intel） | ≈1 mm | Intel Sand-to-Silicon p4 | "Each wafer has a diameter of 300mm and is about 1 mm thick." | 官方（2012） |
| 晶圆厚度（Wiki） | ≈0.75 mm | Wikipedia Monocrystalline silicon | "sliced into wafers about 0.75 mm thick" | 第三方 |
| 抛光 | 镜面 | Intel Sand-to-Silicon p4 | "The wafers are polished until they have flawless, mirror-smooth surfaces." | 官方 |
| 300 mm 晶圆引入年份 | 2000 | https://en.wikipedia.org/wiki/Semiconductor_device_fabrication | "the introduction of 300 mm diameter wafers in 2000" | 第三方 |
| 工序为数百步 | 数百 | Intel Sand-to-Silicon p5 | "Fabrication of chips on a wafer consists of hundreds of precisely controlled steps" | 官方 |
| 工序数（Wiki） | 300+ | Wikipedia Semiconductor device fabrication | "Modern chips have up to eleven or more metal levels produced in over 300 or more sequenced processing steps." | 第三方 |
| 工序数（先进逻辑） | 600–1000+ | https://semiengineering.com/battling-fab-cycle-times （2017-02-16） | "An advanced logic process could have from 600 to 1,000 steps or more." | 第三方 |
| 光刻循环次数 | ≤50 | https://en.wikipedia.org/wiki/Photolithography | "In complex integrated circuits, a wafer may go through the photolithographic cycle as many as 50 times." | 第三方 |
| 光罩层数 | 28nm 40–50；14/10nm 60；7nm 80–85 | SemiEngineering 2017 | "A 28nm device has 40 to 50 mask layers." / "a 14nm/10nm device has 60 layers, with 7nm expected to jump to 80 to 85." | 第三方（2017 预测） |
| 每层处理时间 | 1–1.5 天/层 | 同上 | "On average, a fab takes 1 to 1.5 days to process a layer." | 第三方 |
| 周期 | 40→60→80–85 天 | 同上 | "the cycle times are increasing from roughly 40 days at 28nm, to 60 days at 14nm/10nm, to 80 to 85 days at 7nm." | 第三方 |
| 周期（Wiki） | 平均 11–13 周，最长 15 周 | Wikipedia Semiconductor device fabrication | "fabrication can take up to 15 weeks, with 11–13 weeks being the industry average." | 第三方 |
| 离子注入 | — | Intel Sand-to-Silicon p7 | "The wafer with patterned photoresist is bombarded with a beam of ions" | 官方 |
| ALD | — | 同上 p11 | "Individual molecular layers are applied to the surface of the wafer in a process called "atomic layer deposition"." | 官方 |
| 铜电镀 | — | 同上 p12 | "The wafers are put into a copper sulphate solution at this stage." | 官方 |
| CMP 抛掉多余铜 | — | 同上 p13 | "The excess material is mechanically polished away to reveal a specific pattern of copper." | 官方 |
| CMP 用途 | — | Wikipedia Semiconductor device fabrication | "is the primary processing method to achieve such planarization." | 第三方 |
| 层数 | 30+ 层 | Intel Sand-to-Silicon p13 | "they may actually have over 30 layers to form complex circuitry." | 官方（2012） |
| FEOL 定义 | — | Wikipedia Semiconductor device fabrication | "FEOL processing refers to the formation of the transistors directly in the silicon." | 第三方 |
| BEOL 定义 | — | 同上 | "BEOL processing involves creating metal interconnecting wires that are isolated by dielectric layers." | 第三方 |
| 测试→切割→封装 | — | Intel Sand-to-Silicon p14 | "the individual die are tested while still on the wafer, then separated, and the ones that pass are packaged." | 官方 |
| 晶圆测试做法 | — | 同上 p15 | "A tester steps across the wafer; leads from its head make contact on specific points on the top of the wafer and an electrical test is performed." | 官方 |
| 终测内容 | — | 同上 p17 | "During this final test the processor is thoroughly tested for functionality, performance and power." | 官方 |
| CoWoS 当前尺寸 | 5.5 倍光罩 | https://pr.tsmc.com/english/news/3302 （2026-04-23） | "The Company is now producing 5.5-reticle size CoWoS and planning for even larger versions." | 官方 |
| CoWoS 2028 计划 | 14 倍光罩；约 10 颗计算芯片 + 20 个 HBM | 同上 | "A 14-reticle size CoWoS, capable of integrating approximately 10 large compute dies and 20 HBM stacks" | 官方 |
| CoWoS 描述（产品页，较旧） | >2 倍光罩 ≈1700 mm² | https://www.tsmc.com/english/dedicatedFoundry/technology/cowos | "It can enable larger than 2X-reticle size (or ~1,700mm2) interposer integrating leading SoC chips with more than four HBM2/HBM2E cubes." | 官方（旧） |
| SoIC 3D 堆叠 | A14-to-A14 2029 | pr.tsmc.com/english/news/3302 | "A14-to-A14 SoIC set to be available for production in 2029" | 官方 |
| HBM 堆叠结构 | 4/8/12/16 层 + 1 基底 | https://en.wikipedia.org/wiki/High_Bandwidth_Memory | "4, 8, 12, or 16 DRAM core dies stacked over 1 base logic die" | 第三方 |
| HBM 层间连接 | TSV + 微凸点 | 同上 | "Within the stack the dies are vertically interconnected by through-silicon vias (TSVs) and microbumps." | 第三方 |
| HBM4 标准 | 2025-04 | 同上 | "In April 2025, JEDEC released the official HBM4 specification." | 第三方 |
| HBM 厂商官方 12/16 层量产细节 | — | 未查到（SK hynix 官方搜索无结果） | — | — |
| Chiplet 定义 | — | 未查到官方原句 | — | — |

---

## 2. 光刻：DUV 与 EUV

**DUV 浸没式**：193 nm ArF 光，镜头和晶圆之间夹一层超纯水，水的折射率 1.44。NA 1.35 时分辨率极限约 36 nm。再往下（sub-20nm）要靠多重曝光，比如把相邻图形分配到不同的光罩上（双重图形 pitch splitting）。

**EUV**：
- 13.5 nm 光，ASML 原话「almost x-ray range」。
- 光源：液态锡滴流每秒 50,000 滴。每滴先被弱的预脉冲压成「薄饼」状，再被高能主脉冲打成等离子体，等离子体放出 EUV 光。
- 光路：EUV 会被一切物质吸收，所以从光源到晶圆全程高真空，不能用透镜，只能用多层膜反射镜。光罩本身也是反射式的。
- 反射率：Mo/Si 多层膜理论反射率上限约 75%（第三方）。
- 反射镜数量：Wikipedia（2002–2009 年的系统）是「至少 2 面聚光镜 + 6 面投影镜」。当前机型的面数没有官方数字，ASML 只写「several」。

**High-NA EUV（EXE 系列）**：
- NA 从 0.33 提高到 0.55，分辨率从 13 nm 到 8 nm。
- 首台 EXE:5200B 于 2025 年 4 月初出货，标称 175 片/小时，比 EXE:5000 高 60%。
- 2025 年确认销售 4 台 EXE（2024 年 2 台）。截至 2025 年底，客户累计用 High-NA 跑了 40 万片以上晶圆。
- ASML 官方预计 EXE 平台 2027 年开始支持大规模量产（HVM）。
- 第三方（Bits&Chips 2026-09-02）：10 台在 4 家客户处运行，另有 3 台在运输或安装中；目标 Q4 机群可用率 90%，2026 年底达到 HVM 所需的可用率；验收测试实测 135 片/小时。
- 价格：**官方未公开**。第三方报道约 3.8 亿美元/台（约 3.5 亿欧元，2024 年报道），属于量级参考。

**多重曝光**：ASML 年报说 EUV 让芯片厂「从多重图形走向单次图形」，减少工序。

### 候选事实表（第 2 节）

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| EUV 波长 | 13.5 nm | https://www.asml.com/en/products/euv-lithography-systems | "prints microchips using light with a wavelength of just 13.5 nm – almost x-ray range" | 官方 |
| 两次激光打击 | 2 次脉冲 | 同上 | "a CO2 laser fires two separate laser pulses at a fast-moving drop of tin." | 官方 |
| 每秒次数 | 50,000 次/秒 | 同上 | "This vaporizes the tin and creates EUV light. It does this up to 50,000 times per second." | 官方 |
| 锡滴发生器 | 50,000 滴/秒 | https://www.asml.com/en/company/about-asml/locations/san-diego | "delivering a steady stream of 50,000 liquid tin droplets per second" | 官方 |
| 双脉冲生成等离子体 | — | 同上 | "targeted by two high-powered CO2 laser pulses, generating a plasma that emits EUV light." | 官方 |
| 收集镜 | — | 同上 | "A highly polished, multilayered mirror collects and reflects the 13.5-nanometer EUV light" | 官方 |
| 锡污染光学件 | — | 同上 | "it can contaminate the optics." | 官方 |
| 预脉冲压扁锡滴 | — | https://en.wikipedia.org/wiki/Extreme_ultraviolet_lithography | "A low-energy "pre-pulse" strikes the droplet first, expanding it into a low-density pancake-like cloud of tin vapor." | 第三方 |
| 主脉冲打成等离子体 | — | 同上 | "A high-energy "main pulse" then strikes this vapor, ionizing it into a high-temperature plasma" | 第三方 |
| 等离子体温度 | 电子温度 20–50 eV | 同上 | "electron temperatures of 20–50 eV and electron densities of 10²⁰–10²¹ cm⁻³" | 第三方（「比太阳表面热 X 倍」类说法：未查到官方出处） |
| 多层反射镜代替透镜 | — | ASML EUV 页 | "EUV systems use several multilayer mirrors instead of lenses to guide the EUV light to the wafer" | 官方 |
| 光罩也是反射式 | — | 同上 | "reticles are multilayer reflectors that use interference to reflect light from the pattern" | 官方 |
| 全程高真空 | — | 同上 | "So the whole light path and everything the light interacts with – from source to wafer – must be in high vacuum." | 官方 |
| 真空的原因 | — | Wikipedia EUV | "All matter absorbs EUV radiation. Hence, EUV lithography requires vacuum." | 第三方 |
| 多层膜反射率上限 | ≈75% | 同上 | "which have a theoretical reflectivity limit at 13.5 nm of ~75%." | 第三方 |
| 镜子数量（旧系统） | ≥2+6 | 同上 | "EUVL systems, as of 2002–2009, contain at least two condenser multilayer mirrors, six projection multilayer mirrors" | 第三方（旧） |
| NXE 的 NA 与分辨率 | 0.33 / 13 nm | ASML EUV 页 | "they have a numerical aperture (NA) of 0.33" / "These systems print microchip features with a resolution of 13 nm" | 官方 |
| EXE 的 NA 与分辨率 | 0.55 / 8 nm | 同上 | "With an (NA) of 0.55, their innovative new optics use our novel 13.5 nm EUV light source" / "print with a resolution of just 8 nm" | 官方 |
| EXE:5200B 定位 | sub-2nm | https://www.asml.com/en/products/euv-lithography-systems/twinscan-exe-5200b | "designed to support volume production of sub-2 nm Logic nodes and leading-edge DRAM nodes." | 官方 |
| 首台 EXE:5200B 出货 | 2025-04 初；175 wph；+60% | https://ourbrand.asml.com/m/8ab959d4926657b/original/asml-2025-annual-report-strategic-report-section.pdf （p16） | "In early April 2025, we shipped our first TWINSCAN EXE:5200B system" / "At 175 wafers per hour, it offers 60% higher productivity compared to the TWINSCAN EXE:5000" | 官方 |
| HVM 时间 | 2027 | 同上 p16 | "We expect our TWINSCAN EXE platform to start supporting high-volume manufacturing in 2027." | 官方 |
| High-NA 累计片数 | >400,000 片 | 同上 p8 | "By the end of the year, our customers had run more than 400,000 wafers on High NA EUV systems." | 官方 |
| EXE 确认销售台数 | 2025：4 台；2024：2 台 | 同上 p54 | "We recognized four EXE and 44 NXE systems in sales in 2025 compared to two EXE and 42 NXE systems in 2024." | 官方 |
| 2026-09 部署情况 | 10 台 / 4 家客户 + 3 台 | https://bits-chips.com/article/asml-expects-high-na-euv-to-reach-production-grade-availability-by-year-end/ （2026-09-02） | "Ten systems are now running at four customers, with another three being shipped or installed." | 第三方 |
| 可用率目标 | Q4 90%（7 月 84%） | 同上 | "The lithography giant is targeting 90 percent fleet availability in the fourth quarter, up from 84 percent in July." | 第三方 |
| 实测产能 | 135 wph | 同上 | "135 wafers per hour in acceptance testing." | 第三方 |
| 价格 | ≈3.8 亿美元 | https://www.tomshardware.com/tech-industry/manufacturing/asmls-high-na-chipmaking-tool-will-cost-dollar380-million-the-company-already-has-orders-for-10-to-20-machines-and-is-ramping-up-production | 标题："ASML's High-NA chipmaking tool will cost $380 million…"（正文未抓到；「€350 million」仅见于搜索摘要） | 第三方 |
| 从多重图形到单次图形 | — | ASML 2025 年报 p38 | "ASML supports chipmakers in simplifying the manufacturing process, moving from multi-patterning to single patterning." | 官方 |
| 193 nm 浸没的水折射率 | 1.44 | https://en.wikipedia.org/wiki/Immersion_lithography | "for water immersion using ultraviolet light at 193 nm wavelength, the index of refraction is 1.44." | 第三方 |
| NA 1.35 分辨率极限 | 36 nm | 同上 | "The resolution limit for a 1.35 NA immersion tool operating at 193 nm wavelength is 36 nm." | 第三方 |
| 需多重曝光 | sub-20nm | 同上 | "Going beyond this limit to sub-20nm nodes requires multiple patterning." | 第三方 |
| 双重图形做法 | — | 同上 | "Double patterning by pitch splitting involves assigning adjacent features to different masks" | 第三方 |
| 水层（ASML 图注） | — | https://www.asml.com/en/products/duv-lithography-systems | "A close-up picture of a layer of water between our lithography system's optics and a silicon wafer." | 官方 |
| DUV 产能 | >300 wph | 同上 | "The industry's most productive lithography platform yet is the first to go beyond 300 wafers per hour." | 官方 |
| 曝光是步进重复 | — | Intel Sand-to-Silicon p6 | "it is optically reduced by a lens, and the exposure tool steps and repeats across the wafer to form the same image a large number of times." | 官方 |
| 机器尺寸/重量 | — | 未查到（ASML 页面未列） | — | — |

---

## 3. 洁净室

**洁净等级（ISO 14644-1，每立方米最多颗粒数）**，按 Wikipedia 的表重构：

| 等级 | ≥0.1 µm | ≥0.5 µm |
|---|---|---|
| ISO 1 | 10 | 不适用 |
| ISO 2 | 100 | 不适用 |
| ISO 3 | 1,000 | 35 |
| ISO 4 | 10,000 | 352 |
| ISO 5 | 100,000 | 3,520 |
| ISO 9（≈普通室内或城市室外空气） | — | 35,200,000 |

注：ISO 14644 标准原文要付费，本次未读，上表来自 Wikipedia（第三方）。

- **对比**：城市室外空气每立方米约 3500 万颗 ≥0.5 µm 的颗粒，相当于 ISO 9。也就是说，ISO 5 比普通空气干净约 1 万倍（35,200,000 ÷ 3,520），ISO 3 约 100 万倍，这两个倍数是本人按表计算的。
- 晶圆盒（FOUP）和设备内部的 mini-environment 可以做到 ISO 1。
- **医院手术室的等级对比：未查到可靠出处**，不要在片中写「比手术室干净 X 倍」。
- **黄光区**：光刻胶对短波光（UV 和蓝光）敏感，所以照明要滤掉这些波段，房间就成了黄色。Intel 官方原话可用。业内经验阈值是「避开 500 nm 以下」，出处是 MIT 实验室网络邮件列表里的设备商工程师，属于第三方。
- **AMHS / OHT / FOUP**：
  - 晶圆装在密封的塑料盒 FOUP 里，由自动物料搬运系统（AMHS）在机台之间运送。
  - OHT 是天花板轨道上的小车，用皮带吊升抓起 FOUP，靠非接触感应供电以避免产尘。
  - 很多厂的 FOUP 内充氮气，防止铜氧化。
  - 一个 FOUP 装 25 片：**未查到出处**，不写。
- **工人服装**：穿兔子装（bunny suit），挡住纤维、头发和皮屑。洁净室下面的 subfab 层不穿兔子装，改为安全帽、护目镜、手套和鞋套；最底层公用设施层穿便服、戴安全帽。进洁净室前约 50 个步骤：仅搜索摘要（Intel 教育讲义），未核验。
- **厂房结构（Intel 的四层模型，适合直接做建模参考）**：
  1. 顶层 interstitial 与风机层：保持空气无颗粒、恒温恒湿，是最高的一层。
  2. 洁净室层：1200 多台机台。
  3. 洁净 subfab：数千台泵、变压器和电柜，大管道（laterals）把气体、液体、废料和废气送到机台或从机台运走。
  4. 公用设施层：电气盘柜、主管道、冷水机。
  - 厂房高约 70 英尺（约 21 m，本人换算）。洁净室能放下 4 个美式橄榄球场。每座厂至少 25 万平方英尺。
- **造价量级**：
  - Intel 官方：约 120 亿美元、约 3 年、约 6000 名建筑工人（2023/2024 版）；2022 版为「超过 100 亿美元、3–4 年、7000 人」。
  - TSMC 美国总投资 1650 亿美元，是多座厂加封装厂和研发中心的合计，不是单厂造价（第三方转述）。
  - 「一座先进厂 200 亿美元以上」这类说法：本次**未查到出处**。片中建议用「上百亿美元」。

### 候选事实表（第 3 节）

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| ISO 1–5 颗粒上限 | 见上表 | https://en.wikipedia.org/wiki/Cleanroom | （表格数值，例如 ISO 5：≥0.1 µm 100,000、≥0.5 µm 3,520） | 第三方 |
| 城市室外空气 | 3500 万/m³（≥0.5 µm）≈ISO 9 | 同上 | "The ambient outdoor air in a typical urban area contains 35,000,000 particles for each cubic meter" | 第三方 |
| 普通室内空气 | ≈ISO 9 | 同上 | "Ordinary room air is around class 1,000,000 or ISO 9." | 第三方 |
| 层流送风 | 约 80% 天花板 | 同上 | "Laminar airflow systems are typically employed across 80% of a cleanroom ceiling to maintain constant air processing." | 第三方 |
| mini-environment | ISO 1 | https://en.wikipedia.org/wiki/Semiconductor_device_fabrication | FOUPs and equipment "may have a mini environment with ISO class 1 level of dust." | 第三方 |
| FOUP 充氮 | — | 同上 | "FOUPs in many fabs contain an internal nitrogen atmosphere which helps prevent copper from oxidizing on the wafers." | 第三方 |
| FOUP 定义 | — | https://semiengineering.com/battling-fab-cycle-times | "wafers are processed and transported in an enclosed container called a front opening unified pod (FOUP)." | 第三方 |
| AMHS | — | 同上 | "Fabs are automated plants that make use of an automated material handling system (AMHS)." | 第三方 |
| OHT 吊运 FOUP | — | https://www.muratec-usa.com/product-lines/cleanroom-transport-systems | "It utilizes a belt-driven hoisting mechanism to carry FOUPs (Front Opening Unified Pods)." | 官方（设备商） |
| OHT 非接触供电 | — | 同上 | "Both G series and SRC series OHTs are powered through non-contact and clean induction coupling" | 官方（设备商） |
| OHT 轨道旁缓存 | — | 同上 | "Overhead side buffers along the OHT's route eliminate the need for traditional stockers" | 官方（设备商） |
| 黄光原因 | — | https://download.intel.com/newsroom/2022/manufacturing/fab-final-static.pdf | "Clean rooms are usually lit with yellow lights, necessary in photolithography to prevent unwanted exposure of photoresist to light of shorter wavelengths." | 官方 |
| 黄光光谱 | 无 UV 和蓝光 | https://en.wikipedia.org/wiki/Photolithography | "contains no ultraviolet or blue light in order to avoid exposing photoresists." | 第三方 |
| 500 nm 阈值 | <500 nm 要避开 | https://mtl.mit.edu/pipermail/labnetwork/2023-February/005959.html （2023-02-14） | "we learned that wavelengths below 500 nm must be avoided." | 第三方（业内邮件列表） |
| 兔子装 | — | Intel fab-final-static.pdf (2022) | "Clean room workers wear bunny suits to keep lint, hair and skin flakes off the wafers." | 官方 |
| subfab 着装 | — | 同上 | "Workers don't wear bunny suits here, but they do wear hard hats, safety glasses, gloves and shoe covers." | 官方 |
| 机台数 | 1200+ | 同上 | "A clean room is made up of more than 1,200 factory tools that take pizza-size silicon wafers and eventually turn them into hundreds of computer chips." | 官方 |
| 厂房高度与层数 | 70 英尺，4 层 | 同上 | "the 70-foot-tall structure produces millions of computer chips" / "Three of the fab's four levels support the clean room level" | 官方 |
| 洁净室面积 | 4 个橄榄球场；≥25 万平方英尺 | 同上 | "Each fab is at least 250k square feet. Four American football fields could fit inside each fab's clean room." | 官方 |
| 造价（2022 版） | >100 亿美元，3–4 年，7000 工人 | 同上 | "takes about three to four years, over $10 billion and 7,000 construction workers to complete." | 官方 |
| 造价（2023/24 版） | ≈120 亿美元，≈3 年，6000 工人 | https://download.intel.com/newsroom/2023/tech101/manufacturing-101-semicon/how-a-semiconductor-factory-works.pdf | "It costs about $12 billion and takes about three years and 6,000 construction workers to complete." | 官方 |
| 风机层功能 | — | 同上 | "The fan deck houses systems that keep the air in the clean room particle-free and precisely maintained at the right temperature and humidity for production." | 官方 |
| 一对先进厂的建材 | 50 万 m³ 混凝土；5.8 万吨结构钢 | fab-final-static.pdf (2022) | "500K cubic meters of concrete will be poured" / "58K tons of structural steel will be erected." | 官方 |
| TSMC 美国总投资 | 1650 亿美元（多厂合计） | https://www.theengineer.co.uk/content/news/tsmc-to-invest-100bn-into-expansion-in-arizona | （仅搜索摘要）"TSMC's total investment in the US is expected to reach $165bn." | 第三方·未打开原页 |
| 手术室对比 | — | 未查到 | — | — |
| FOUP 25 片 | — | 未查到 | — | — |
| 进洁净室约 50 步 | ≈50 | 仅搜索摘要：https://www.intel.com/content/dam/www/program/education/us/en/documents/the-journery-inside/microprocessor/tji-microprocessors-handout9.pdf | （摘要）"Each worker completes approximately 50 steps before entering." | 官方·未打开原页 |

---

## 4. 良率与检测

- **为什么一粒灰就能毁芯片**：
  - 经验规则：颗粒只要有特征尺寸的约 1/5，就足以造成致命缺陷（killer defect），这是 Wikipedia 的说法，属于第三方。
  - 设计尺寸越小，良率对缺陷的大小和密度越敏感（KLA 年报，仅搜索摘要）。
  - 光罩上的缺陷会在每颗芯片上重复印出来，一个缺陷就可能造成灾难性良率损失（KLA 产品页，仅搜索摘要；页面是 JS 渲染，抓不到原文）。
- **良率定义**：晶圆上能正常工作的芯片所占的比例。
- **检测/量测怎么做**：
  - 工序之间插入量测，用椭偏或反射法测薄膜厚度，并用量测数据预测良率。
  - 缺陷检测用光学（明场、宽带等离子体光源）扫描晶圆找异常，再用复查设备（如电子束复查）做分类。这部分只有 KLA 产品页的搜索摘要，**未拿到原句**。
  - 最终测试是探针扎在晶圆上做电测，封装后再终测。
- 先进节点的良率数字：仅见 Samsung SF2 的第三方传闻（约 50%），**不建议入片**。

### 候选事实表（第 4 节）

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 致命颗粒尺寸 | ≈特征尺寸的 1/5 | https://en.wikipedia.org/wiki/Semiconductor_device_fabrication | "A particle needs to be 1/5 the size of a feature to cause a killer defect." | 第三方 |
| 良率定义 | — | 同上 | "The percent of devices on the wafer found to perform properly is referred to as the yield." | 第三方 |
| 工序间量测需求 | — | 同上 | "The highly serialized nature of wafer processing has increased the demand for metrology in between the various processing steps." | 第三方 |
| 薄膜量测方法 | 椭偏/反射 | 同上 | "thin film metrology based on ellipsometry or reflectometry" | 第三方 |
| 量测预测良率 | — | 同上 | "Metrology tools are used to inspect the wafers during the production process and predict yield." | 第三方 |
| 晶圆电测 | — | Intel Sand-to-Silicon p15 | "Test patterns are fed into every single chip and the response from the chip is monitored and compared to "the right answer"." | 官方 |
| 线宽越小越敏感 | — | 仅搜索摘要：https://ir.kla.com/sec-filings/all-sec-filings/content/0000319201-25-000024/0000319201-25-000024.pdf | （摘要）"as design rules decrease, yields become more sensitive to the size and density of defects" | 官方·未打开原页 |
| 光罩缺陷重复 | — | 仅搜索摘要：https://www.kla.com/products/reticle-qualification | （摘要）"even a single defect can cause catastrophic yield loss" | 官方·页面抓取为空 |
| 光学检测原理细节 | — | 未查到原句 | — | — |

---

## 5. 产业分工（背景，一句话级）

- **分工**：设计公司（无晶圆厂）负责设计；代工厂负责制造；IDM 自己设计也自己制造（ASML 年报把逻辑芯片制造商分成 IDM 和代工两类）；设备商提供光刻、刻蚀、量测等设备；EDA 提供设计软件。EDA 和设备商的定义原句：**未查到**，只作常识背景，不引数字。
- **ASML 光学独家供应商**是 Carl Zeiss SMT（ASML 年报）。仅背景，不入画面。
- **2026 年先进制程状态（只写到有出处为止）**：
  - TSMC N2：2025 年第 4 季度按计划开始量产，是第一代纳米片（nanosheet）晶体管。N2U 计划 2028 年量产，A13 计划 2029 年量产。**A16 的量产日期在官方页上未查到**。
  - Intel 18A：官方页写「In high-volume production in the United States」（查看日 2026-11-14），采用 RibbonFET（GAA）和 PowerVia 背面供电。Fab 52（亚利桑那）2025-10 已全面运转；Panther Lake 2026 年 1 月起广泛供货。
  - Samsung SF2：官方 Logic Node 页写「Started mass production in 2025」，首款产品 Exynos 2600 自称业界首个 2nm GAA。良率只有第三方传闻，不写。
  - TSMC 是否在 A14 跳过 High-NA：仅第三方传闻，不写。

### 候选事实表（第 5 节）

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 逻辑芯片制造商的两类 | IDM / 代工 | ASML 2025 年报 p24 | "They are produced by two groups of manufacturers: integrated device manufacturers (IDMs), which design and manufacture Logic chips; and contract manufac[turers]…" | 官方 |
| ASML 光学独家供应 | — | 同上 p68 | "Carl Zeiss SMT, our sole supplier of lenses, mirrors, illuminators, collectors and other critical optical components" | 官方 |
| TSMC N2 量产 | 4Q25 | https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm | "TSMC's 2nm (N2) technology has started volume production in 4Q25 as planned." | 官方 |
| N2 纳米片 | 第一代 | 同上 | "N2 technology features industry-leading first-generation nanosheet transistor technology" | 官方 |
| N2U / A13 时间 | 2028 / 2029 | https://pr.tsmc.com/english/news/3302 （2026-04-23） | "N2U is scheduled for production in 2028." / A13 "is scheduled to enter production in 2029, one year after A14." | 官方 |
| A16 量产时间 | — | 未查到（官方页无日期） | — | — |
| Intel 18A 量产 | HVM（美国） | https://www.intel.com/content/www/us/en/foundry/process/18a.html | "In high-volume production in the United States." | 官方 |
| RibbonFET | GAA | 同上 | "RibbonFET is Intel Foundry's gate-all-around transistor architecture" | 官方 |
| PowerVia | 背面供电 | 同上 | "Intel Foundry's industry-first PowerVia technology relocates course pitch metals and bumps to the back side of the die" | 官方（原文就写作 "course"） |
| Fab 52 | 2025-10 全面运转 | https://www.intel.com/content/www/us/en/newsroom/news/client-computing/intel-unveils-panther-lake-architecture-first-ai-pc-platform-built-on-18a.html （2025-10-09） | "Arizona's Fab 52 is fully operational and set to reach high-volume production using Intel 18A later this year" | 官方 |
| Panther Lake 供货 | 2026-01 | 同上 | "broad market availability starting January 2026" | 官方 |
| Intel 18A 2025 年底在 AZ 和 OR 达到 HVM | — | 仅搜索摘要：Intel CSR 2025-26 https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2026-08/csr-2025-26-full-report.pdf | （摘要）"by the end of 2025, Intel reached high-volume manufacturing on Intel 18A at both its Arizona and Oregon fabs" | 官方·未打开原页 |
| Samsung SF2 量产 | 2025 | https://semiconductor.samsung.com/foundry/process-technology/logic-node/ | "Started mass production in 2025" | 官方 |
| Exynos 2600 = 业界首个 2nm GAA | — | 仅搜索摘要：https://semiconductor.samsung.com/processor/mobile-processor/exynos-2600/ | — | 官方·未打开原页 |

---

## 6. 画面参考渠道（只作建模参考，不放进片子）

| 渠道 | 内容 | 版权/使用条款（本次所见） |
|---|---|---|
| Intel「Making of a Chip」新闻素材包：www.intel.com/pressroom/kits/chipmaking（PDF 里给出的地址）；PDF：https://download.intel.com/newsroom/kits/chipmaking/pdfs/Sand-to-Silicon_22nm-Version.pdf | 从砂、硅锭、切片、光刻、离子注入、刻蚀、电镀、CMP、测试、切割到封装的 3D 插画，**非常适合做分镜和建模参考** | PDF 页脚写「Copyright © 2012, Intel Corporation. All rights reserved.」。PDF p2 写「For publishing purposes there are high resolution JPEG files posted to the Intel website」，意思是给媒体发布用，属于新闻素材。是否允许商业视频再使用：**未查到**。画面里带 Intel 商标。 |
| Intel fab 结构信息图：https://download.intel.com/newsroom/2022/manufacturing/fab-final-static.pdf ；https://download.intel.com/newsroom/2023/tech101/manufacturing-101-semicon/how-a-semiconductor-factory-works.pdf | 四层厂房剖面（风机层、洁净室、subfab、公用设施），**是重建通用洁净室剖面的最佳参考** | © Intel，页脚写有商标声明。使用条款：**未查到** |
| ASML 媒体库：https://www.asml.com/en/news/media-library （会 301 到 investor.asml.com，抓取返回 403） | EUV/DUV 系统、装配洁净环境（"ultraclean environment where we assemble our lithography systems"）的照片和动画 | 仅搜索摘要：只限编辑用途，必须标「©ASML」，不得用于推广或商业（"may only be used for editorial purposes and must be labeled "©ASML"" / 不允许 "promotional or commercial purposes"）。**原页未直接核验** |
| ASML 产品页：https://www.asml.com/en/products/euv-lithography-systems 、/duv-lithography-systems 、/euv-lithography-systems/twinscan-exe-5200b | 设备外观图、光路示意动画 | 网站条款：https://www.asml.com/terms-of-use （未打开）。默认 All Rights Reserved（页脚「Copyright © 2019-2026 (ASML) All Rights Reserved」） |
| TSMC CoWoS 页：https://www.tsmc.com/english/dedicatedFoundry/technology/cowos | 先进封装结构示意 | 条款：**未查到** |
| Muratec 洁净室搬运：https://www.muratec-usa.com/product-lines/cleanroom-transport-systems | OHT 小车、轨道、FOUP 的产品照片，可作天车建模参考 | 设备商产品图，条款：**未查到** |
| Wikipedia / Wikimedia Commons（Cleanroom、Photolithography、Semiconductor device fabrication 等条目的配图） | 洁净室、兔子装、FOUP、晶圆照片 | 每张图的许可不同（常见 CC BY/CC BY-SA 或公有领域）。**本次未逐张核对**，用前查文件页 |

建模注意：重建时去掉所有 logo、设备外壳上的品牌造型和配色。EUV 机台不要照抄 ASML 的外壳轮廓，做成通用的「巨型白色模块化机台 + 真空腔 + 光路」。

---

## 7. 知识点地图建议（按真实流程拆期）

| 期 | 主题 | 一个核心画面 |
|---|---|---|
| A | 从沙子到超纯硅 | 一粒沙放大成晶格。对比镜头：10 克糖溶进 100 亿升水，表示 ppt 级纯度 |
| B | 拉出一根单晶 | 籽晶点进发光的熔硅，旋转着往上拉出一根比人还高的银色单晶柱 |
| C | 切片与镜面晶圆 | 线锯切出一摞薄片，主角在镜面晶圆上照见自己的倒影 |
| D | 走进洁净室（t01 预告用） | 黄光走廊，兔子装工人，头顶 OHT 吊着 FOUP 呼啸而过；空气颗粒计数从 3500 万降到个位数 |
| E | 光刻（DUV） | 光穿过光罩、透镜和一层水，把电路图「印」到胶上，在晶圆上步进重复 |
| F | EUV 光源 | 锡滴雨每秒 5 万滴，每滴先被压扁再被击碎成等离子体，发出看不见的光，经一串镜子反射（全程真空） |
| G | 刻蚀、注入、沉积循环 | 同一片晶圆一圈圈回到不同机台，叠层像在盖楼。镜头上挂一个层数计数器，最多 50 次光刻 |
| H | 后道互连 | 铜电镀灌进沟槽，CMP 磨平，十几层铜「立交桥」在晶体管上方生长 |
| I | 一粒灰的灾难与检测 | 一颗只有线宽 1/5 大的颗粒落在电路上，导致短路；检测光束扫过晶圆，异常点亮红 |
| J | 测试、切割、封装 | 探针阵列扎下去，好片亮绿灯，晶圆切成芯片，加盖封装 |
| K | 先进封装 | 计算芯片和一摞摞 HBM 并排坐在中介层上，HBM 是 12 层薄片用竖直通孔串起来 |

t01 结尾预告建议用 D：黄光加天车加兔子装，辨识度最高，而且全部有官方出处支撑。

---

## 缺口汇总（未查到 / 未核验）

- 工业上「石英砂→冶金硅」的工艺与数字：未查到。
- 2nm 级节点的光罩层数和投片到出厂周期：未查到，现有数字截至 2017 年的 7nm 预测。
- High-NA 官方价格：未查到，只有第三方的约 3.8 亿美元。
- 洁净室和手术室的对比：未查到。
- 一个 FOUP 装几片：未查到。
- ASML 媒体库条款、KLA 检测原句、Intel CSR 18A HVM：只有搜索摘要，原页 403、JS 渲染或未打开。
- TSMC A16 量产日期：未查到。
- HBM 厂商官方的堆叠和减薄细节：未查到。
- Chiplet、EDA、设备商的定义原句：未查到。
