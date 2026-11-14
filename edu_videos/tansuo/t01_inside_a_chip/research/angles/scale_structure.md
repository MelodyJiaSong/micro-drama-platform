---
worker_id: researcher-01-scale-structure
stage: 3
role: researcher
angle: scale-structure
status: partial
blockers:
  - "TSMC N2 / Samsung SF3 的 CPP、最小金属间距、cell height 没有官方公开值；TechInsights 实测报告在付费墙后"
  - "主流 SoC 各功能区（CPU/GPU/NPU/SLC）的 mm² 占比，公开可核的一手数据很少；本文只有 Snapdragon X Elite 的第三方数字"
  - "NVIDIA Blackwell 单颗 die 的面积没有官方数字"
confidence: medium
---

# 角度：尺度与结构（t01「缩小进芯片」）

- 查证日期：所有链接都在 **2026-11-14** 访问。
- 引文说明：quote 栏是英文原文照抄。来源分三种：
  - WebFetch 抽取的原文：直接标 URL。
  - 搜索结果摘要：标「搜索摘要」，可信度低一级。
  - 本人从 PDF 表格图像读出的数字：标「表格读数」。
- 官方 / 第三方的分法：
  - 官方：厂商或标准组织本身的说法，IRDS 也算官方路线图。
  - 第三方：拆解机构、媒体、Wikipedia、爆料人。
  - 自算：本人计算，写出算式。
- 本次用了 17 次 WebSearch。

---

## 1. 晶圆（wafer）

**要点**
- 主流先进制程用 300 mm 晶圆。一份 300 mm 晶圆商品规格写的是：直径 300±0.20 mm，厚度 775±25 µm，边缘排除 3.0 mm。
- 这份是 SVM 公司的产品规格，不是 SEMI M1 标准原文。SEMI M1 原文本次未查到。Wikipedia 的表也写 775 µm，但那一格没有引注。
- 厚度只有直径的 1/387（300 / 0.775 ≈ 387）。按真实比例，晶圆比一张薄饼还薄得多，画面上应接近一张「硬盘片」。

**一片能切多少颗（自算）**
- 例子用 Apple A20 Pro（TSMC N2）。TechInsights 实测 die 约 8.0 mm × 12.3 mm，估算面积 98.2 mm²。
- 用常用的带边缘修正近似式：DPW ≈ π·d²/(4S) − π·d/√(2S)。
  - Wikipedia 指出这类公式要加「edge correction」，而且不计良率。
  - d = 300 mm，S = 8.0 × 12.3 = 98.4 mm²。
  - 不计边缘：70 686 / 98.4 ≈ 718 颗。
  - 扣边缘修正：718.4 − 942.5 / √196.8 = 718.4 − 67.2 ≈ **651 颗**（毛片数）。
  - 再扣 3 mm 边缘排除（d_eff = 294 mm）：≈ **624 颗**。
  - 再加 0.1 mm 划片道（S = 8.1 × 12.4）：≈ **611 颗**。
- 结论：一片 300 mm 晶圆约切出 **600 多颗** A20 Pro 大小的手机芯片。这是毛片数，**不含良率**。
- Apple 和 TSMC 没有公布实际的每片颗数。
- 对比：AI GPU GH100（814 mm²）用同一公式只有约 **60–64 颗**。Wikipedia 表中「100 mm² die」一栏给的是 640 颗，与本文自算量级一致。

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 300 mm 晶圆直径 | 300±0.20 mm | https://svmi.com/wp-content/uploads/2021/01/SV029.pdf | "Diameter mm 300±0.20" | 厂商规格（SVM 产品 SV029） |
| 300 mm 晶圆厚度 | 775±25 µm | 同上 | "Thickness µm 775±25" | 厂商规格 |
| 边缘排除 | 3.0 mm | 同上 | "Edge exclusion mm 3.0" | 厂商规格 |
| 300 mm 厚度（交叉核对） | 775 µm；100 mm² die 每片 640 颗 | https://en.wikipedia.org/wiki/Wafer_(electronics) | "300 mm (11.8 inch, usually referred to as "12 inch") \| 775 μm \| 1999 \| 125 grams[17] \| 640" | 第三方（该格无引注） |
| DPW 公式要做边缘修正、不计良率 | — | 同上 | "Refinements of this simple formula typically add an edge correction, to account for partial dies on the edge"；"gross DPW calculations do _not_ account for yield loss among those complete dies" | 第三方 |
| A20 Pro die 尺寸 | 约 8.0 × 12.3 mm，约 98.2 mm²，TSMC N2 | https://www.techinsights.com/blog/apple-a20-pro-tsmc-2nm-processor-analysis | "approximately 8.0 mm by 12.3 mm, producing an estimated die area of 98.2 mm²"；"the first Apple application processor manufactured using TSMC's N2 process" | 第三方实测（TechInsights） |
| 每片约 650 / 624 / 611 颗 A20 Pro 大小的 die（毛片） | 见上方算式 | 自算 | — | 自算 |

---

## 2. 一颗芯片（die）

**代表性芯片**

| 芯片 | 工艺 | 面积 | 晶体管数 | 备注 |
|---|---|---|---|---|
| 手机 SoC：Apple A20 Pro | TSMC N2 | ≈98.2 mm²（TechInsights） | 未公开 | 本次未查到晶体管数 |
| 手机 SoC：Apple A19 Pro | N3P（第三方说法） | ≈98.6 mm²（爆料人 die shot 测量） | 未公开 | A18 Pro 约 105 mm² |
| 手机 SoC：Snapdragon 8 Elite Gen 5 | — | ≈126.2 mm² | 未公开 | 第三方 |
| PC 芯片：Apple M4 | Apple 称第二代 3 nm | 未公开（论坛数字 165.9–170 mm²，不采用） | **280 亿（官方）** | |
| PC 芯片：AMD Zen 5 CCD（8 核计算 die） | N4P / N4X 有争议 | **70.6 mm²（AMD 向 Hardwareluxx 确认）** | 8.315 B（非官方） | |
| AI GPU：NVIDIA GH100（H100） | TSMC 4N | **814 mm²（官方）** | **800 亿（官方）** | |
| AI GPU：NVIDIA Blackwell | 定制 TSMC 4NP | 单 die 面积未公开 | **2080 亿（官方）** | 由两颗「reticle-limited」die 组成，片间互联 10 TB/s |

**光罩极限（reticle limit）**
- 低 NA EUV 单次曝光场是 26 × 33 mm = **858 mm²**。High-NA 是半场 26 × 16.5 mm = 429 mm²。
  - 这个数来自日文业界解说（第三方），ASML 官网本次没有读出数值。
- SemiEngineering 2025 文章的写法不同：「26mm square」「up to 676mm2」。这和 26×33 的说法冲突，待用 ASML 或 SEMI 原文定稿。
- 旁证：GH100 是 814 mm²，Blackwell 官方称其 die 为「reticle-limited」。这两点都与「上限约 800 多 mm²」的量级一致。

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| A20 Pro 面积与工艺 | 98.2 mm²，N2 | https://www.techinsights.com/blog/apple-a20-pro-tsmc-2nm-processor-analysis | "producing an estimated die area of 98.2 mm²" | 第三方实测 |
| A20 与 A19 Pro 面积相近 | — | 同上 | "nearly identical in size to the previous-generation A19 Pro" | 第三方 |
| A18 Pro → A19 Pro 面积 | 105 → 98.6 mm² | https://www.notebookcheck.net/Apple-A19-Pro-die-shot-showcases-smaller-profile-chip-with-minimal-design-changes.1164948.0.html （die shot 来自 https://x.com/Kurnalsalts/status/1990191447044391399 ） | "Apple, on the other hand, actually reduced its die area from 105 mm2 to 98.6 mm2." | 第三方（爆料人 die shot，测量者未明示） |
| Snapdragon 8 Elite Gen 5 面积 | ≈126.20 mm² | https://www.notebookcheck.net/Snapdragon-8-Elite-Gen-5-die-shot-highlights-minor-upgrades-and-GPU-improvements.1124373.0.html | "The chip has a die area of ~126.20 mm2, about the same as its last-gen counterpart." | 第三方 |
| Apple M4 晶体管数与工艺 | 280 亿，第二代 3 nm | https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/ （2024-05-07） | "M4 consists of 28 billion transistors built using a second-generation 3-nanometer technology" | 官方 |
| Zen 5 CCD 面积 | 70.6 mm² | 搜索摘要，原文 https://www.tomshardware.com/pc-components/cpus/amds-zen-5-chips-pack-in-8315-billion-transistors-per-compute-die-a-28-increase-in-density | "AMD confirmed to Hardwareluxx that each Zen 5 core complex die (CCD) measures 70.6 mm²"（搜索摘要） | 官方经媒体转述 |
| Zen 5 CCD 晶体管数 | 8.315 B（非官方） | 同上 | "AMD has not publicly talked transistor count but … most believe the figure to be 8.315 billion"（搜索摘要） | 第三方 |
| GH100 | 800 亿晶体管，814 mm²，TSMC 4N | https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/ （2022-03-22） | "The full GH100 GPU that powers the H100 GPU is fabricated using the TSMC 4N process customized for NVIDIA, with 80 billion transistors, a die size of 814 mm2" | 官方 |
| Blackwell 晶体管数 | 2080 亿，4NP | https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/ | "NVIDIA Blackwell-architecture GPUs pack 208 billion transistors and are manufactured using a custom-built TSMC 4NP process." | 官方 |
| Blackwell 由两颗光罩极限 die 组成 | 2 die，10 TB/s | 同上 | "All NVIDIA Blackwell products feature two reticle-limited dies" … "connected by a 10 terabytes per second (TB/s) chip-to-chip interconnect" | 官方 |
| 光罩场 | 26×33 mm = 858 mm²；High-NA 半场 429 mm² | https://semi-connect.net/high-na-euv-complete-guide-na055-intel-tsmc-asml/ （2026-07-18） | "Low-NA EUV：26 × 33 mm（= 858 mm²）のエリアを1回で露光"；"High-NA EUV：26 × 16.5 mm（= 429 mm²）のエリアを1回で露光" | 第三方（日文） |
| 光罩极限（冲突说法） | 26 mm 见方 / 最大 676 mm² | https://semiengineering.com/are-larger-reticle-sizes-on-the-horizon （2025-06-19） | "an area of 26mm square for 193nm immersion and EUV lithography"；"which shrinks to half that size for high-NA due to the anamorphic lens" | 第三方，**与上一行冲突** |
| GH100 面积密度 | 80e9 / 814 ≈ 9.8×10⁷ 个/mm²（约 1 亿/mm²） | 自算 | — | 自算 |

---

## 3. 芯片上的「地图」（floorplan）

**手机 / PC SoC 的典型布局**（从公开 die shot 看）
- **CPU 簇**：大核与小核各自成簇。每簇旁边有一大块规整的 L2 SRAM。
- **GPU**：多个重复的 GPU 核，并排排成阵列。
- **NPU / 神经引擎**：一块独立的规则阵列。
- **系统级缓存（SLC）**：几块大面积、纹理极规整的 SRAM 阵列。
  - SemiAnalysis 指出，A15 上「单一最大的面积贡献者」就是 SLC。
- **IO / 内存 PHY**：贴着 die 的边缘，呈长条状（如 LPDDR PHY）。
- 画面规律：
  - SRAM 区看起来像整齐的「瓷砖」。
  - 逻辑区（标准单元）看起来像细密、随机的「布纹」。
  - PHY 在四周。

**占比（可核数字很少）**
- Snapdragon X Elite（PC 芯片），百度用户标注的 die shot：
  - CPU 域 48.2 mm²，GPU 域 24.3 mm²，整 die 169.6 mm²。
  - 换算：CPU ≈ 28%，GPU ≈ 14%（自算）。
  - 这是第三方爆料数据，NPU 没有标注。
- A15（2021）：SemiAnalysis 只给了各块的增长百分比，没有 mm²。
  - SLC 从 16 MB 翻倍到 32 MB，是最大的面积来源。
- 结论：「CPU/GPU/NPU/SLC 各占多少」不宜在讲稿里给精确百分比。建议用「SLC + 各级缓存占很大一块，CPU 与 GPU 各占约 1/7–1/4」这类定性说法，并注明是示例芯片。

**AI GPU（GH100）**
- 画面应是：大量重复的 SM 阵列，中间是 L2 缓存。HBM 接口 PHY 在长边边缘。
- 这个布局本次未查到 die shot 标注，只能按 NVIDIA 架构框图示意。

**公开 die shot / 标注链接**（只记链接，未下载）
- A19 Pro die shot（@KurnalSalts）：https://x.com/Kurnalsalts/status/1990191447044391399
- Snapdragon 8 Elite Gen 5 die shot（@KurnalSalts）：https://x.com/Kurnalsalts/status/1971234108111192402
- A19 Pro 的 SemiAnalysis 推文（SLC 面积等）：https://twitter.com/SemiAnalysis_/status/1998906955616670207
- Notebookcheck 文章：
  - A19 Pro：https://www.notebookcheck.net/Apple-A19-Pro-die-shot-showcases-smaller-profile-chip-with-minimal-design-changes.1164948.0.html
  - Snapdragon 8 Elite Gen 5：https://www.notebookcheck.net/Snapdragon-8-Elite-Gen-5-die-shot-highlights-minor-upgrades-and-GPU-improvements.1124373.0.html
  - Dimensity 9500：https://www.notebookcheck.net/MediaTek-Dimensity-9500-die-shot-showcases-noticeably-larger-chip-and-incremental-upgrades-to-CPU-and-NPU.1128763.0.html
- Apple A15 die shot 标注（SemiAnalysis，die shot 由 TechInsights 提供）：https://newsletter.semianalysis.com/p/apple-a15-die-shot-and-annotation
- Apple M2 die shot 分析（SemiAnalysis）：https://newsletter.semianalysis.com/p/apple-m2-die-shot-and-architecture
- Snapdragon X Elite 标注：
  - https://www.tomshardware.com/pc-components/cpus/qualcomm-snapdragon-x-die-shot-reveals-massive-cpu-cores-with-huge-caches
  - https://techpowerup.com/327130/qualcomm-snapdragon-x-elite-die-exposed-and-annotated
- Intel Lunar Lake 标注：https://www.tomshardware.com/pc-components/cpus/intel-lunar-lake-cpu-gets-die-annotation-four-skymont-e-cores-slightly-bigger-than-one-lion-cove-p-core
- Intel Panther Lake-H（18A 计算 tile）die shot：https://www.tomshardware.com/pc-components/cpus/intel-panther-lake-h-high-res-die-shot-emerges-image-show-18a-compute-tile-xe3-gpu-tile-in-new-x-series-processors
- AMD Strix Halo 标注：https://www.tomshardware.com/pc-components/gpus/amds-game-changing-strix-halo-apu-formerly-ryzen-ai-max-poses-for-new-die-shots
- AMD Strix Point 标注：https://techpowerup.com/325035/amd-strix-point-silicon-pictured-and-annotated
- Alder Lake die 漫游（Locuza）：https://locuza.substack.com/p/die-walkthrough-alder-lake-sp-and
- TechInsights M5 Pro die 级分析（两颗 die 用 SoIC-X 混合键合，数字在付费墙后）：https://techinsights.com/blog/what-die-level-analysis-reveals-about-apples-m5-pro-gpu-design

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| A15 最大面积块是 SLC | 16→32 MB | https://newsletter.semianalysis.com/p/apple-a15-die-shot-and-annotation （2021-09-30/10-01） | "has doubled from 16MB to 32MB"；"The total die has increased significantly in size to 107.7mm^2" | 第三方 |
| A18→A19 的 4 MB SLC 块面积 | 1.08 → 0.98 mm² | https://wccftech.com/apple-made-a19-pro-10-smaller-than-a18-pro-while-adding-more-features-here-is-how/ （2025-12-11，引 SemiAnalysis） | "For the older SoC, the company utilized 1.08 mm², while the newer silicon has secured 0.98 mm² of space." | 第三方 |
| Snapdragon X Elite CPU 域 / GPU 域 | 48.2 / 24.3 mm²（整 die 169.6 mm²） | 搜索摘要，原文 https://www.tomshardware.com/pc-components/cpus/qualcomm-snapdragon-x-die-shot-reveals-massive-cpu-cores-with-huge-caches | "the CPU domain takes 48.2 mm^2 of space, which is two times larger compared to the Adreno X1 GPU domain, which is 24.3 mm^2"（搜索摘要） | 第三方（爆料） |
| 占比换算 | CPU 48.2/169.6 ≈ 28%；GPU 24.3/169.6 ≈ 14% | 自算 | — | 自算 |
| M5 Pro/Max 用两颗 die 混合键合 | — | https://techinsights.com/blog/what-die-level-analysis-reveals-about-apples-m5-pro-gpu-design （2026-09-02） | "Its new Fusion Architecture combines two silicon dies into a single system-on-chip (SoC)" | 第三方 |

---

## 4. 标准单元与金属互连

### 4.1 关键尺寸（先进节点）

| 节点 | 栅极间距 CPP | 最细金属间距 | 标准单元高度 | 来源 |
|---|---|---|---|---|
| Intel 18A | **50 nm** | M0 **32 nm** | **160 nm（HD）/ 180 nm（HP）** | Intel 官方 2026 VLSI 新闻稿确认 18A 与 18A-P 的 cell height 和 CPP；M0 来自媒体对 VLSI 2025 的整理 |
| TSMC N3 / N3E | N3 **45 nm** | N3E **23 nm** | 未查到官方 | IEDM 2022，经 SemiWiki / Wikipedia 转述 |
| TSMC N2 | 未查到官方 | 未查到官方 | 未查到官方 | TSMC 只公布了 NanoFlex：可选矮单元或高单元。Wikipedia 表格写 48/26 nm，但列对应关系不确定，**不采用** |
| Samsung SF3 / SF2 | 未查到可靠值 | 未查到可靠值 | 未查到 | TechInsights 的 SF3（Exynos W1000）CD 在付费墙后 |
| IRDS 2022 路线图「2nm」（2025，G45M20） | 45 nm | M0 20 / M1 23 / Mx 24 nm | HD 114 nm、HP 138 nm；HD = 4.75 个 Mx 轨道 | 官方路线图，属预测 |

**补充**
- Intel 18A 的 HD 单元：160 / 32 = **5 个 M0 轨道**（自算）。SemiAnalysis 实测也写「five-track logic library」。
- SemiAnalysis 实测还发现：Panther Lake HP 库实际出货用的是 M0 36 nm，而 PDK 写的是 32 nm。
- 一个标准单元的宽度 = 若干个 CPP。最简单的门约 2–3 个 CPP 宽：
  - 以 18A 为例，约 100–150 nm × 160 nm（自算示意）。
  - 「几个 CPP」本次未查到权威数字，画面上**按示意处理**。

### 4.2 金属层数（BEOL）

**Intel 18A**
- 媒体整理的 VLSI 2025 规格表：正面 10ML（低成本 / 高密度）、14–16ML（高性能），背面「3ML+3ML」。
- SemiAnalysis 拆 Panther Lake 实测：正面 **M0–M14（15 层）**信号层，背面 **BM0–BM5（6 层）**供电层。

**IRDS 2022 Table MM-13（2022 和 2025 两列）**
- Mx 层 2 层。
- 中间层（>P40 且 <P720）12 层。
- 720 nm 间距粗厚层 2 层。
- 「布线层 M1+Mx+>P40」共 17 层（表格读数）。

**从上往下看一颗芯片**（倒装封装时，这一面其实朝下）
1. **凸点**：
   - 普通电镀焊料凸点间距 130–250 µm；低于 130 µm 改用铜柱。
   - 微凸点全阵列间距可到 35 µm。
   - TSMC SoIC 混合键合目前 6 µm，2029 年目标 4.5 µm。
2. **最上面的厚金属层**：IRDS 里 720 nm 间距的 2 层，用于电源 / 全局布线。
3. **中间层**：越往下，金属线越细、越密。
4. **最下面的 M0 / M1 / Mx**：几十纳米间距。
5. **接触层（MOL）**。
6. **最底层**：硅表面上的晶体管（FEOL）。

所以从正面「看」芯片，看到的是金属。晶体管被埋在十几层金属下面。

**背面供电（backside power）现状（截至 2026-11）**
- **Intel PowerVia**
  - 已随 18A 量产：Panther Lake 计算 tile 在 Arizona Fab 52 生产，2025 年底出货，2026-01 广泛上市。
  - 这是第一个大规模商用的背面供电。
  - 结构：电源网从正面顶层金属挪到晶圆背面，正面只留给信号。
- **TSMC A16「Super Power Rail」**
  - 用背面接触直接连到源极 / 漏极。SemiEngineering 称这种方式面积微缩最好。
  - 官方页只写「nanosheet + backside power rail」。
  - 原定 2026 下半年量产。2024-11 的 TrendForce 写「by the end of 2026」。
  - 截至 2026-11-14，**本次未查到 TSMC 宣布 A16 已量产的一手公告**。只有 2026-08 一条转述 DigiTimes 的「Q4 量产」搜索摘要，未能打开原文。
- **TSMC N2P**：2023 年曾报道会带背面供电。之后的路线改为由 A16 引入，本次未核实最新说法。

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 18A / 18A-P 单元高度与 CPP | 180 / 160 nm；CPP 50 nm | https://www.intel.com/content/www/us/en/newsroom/news/corporate/intel-foundry-details-process-milestones-future-innovation-at-vlsi-symposium.html （2026-06-16） | "Similar to Intel 18A, Intel 18A-P offers two cell heights (180nm and 160nm), a contacted poly pitch of 50nm." | 官方 |
| 18A 规格表 | HP/HD 180/160；CPP 50；M0 32；正面 10–16ML；背面 3ML+3ML | https://wccftech.com/intel-18a-process-node-25-percent-higher-frequency-36-percent-lower-power-vs-intel-3/ （2025-06-18） | "HP/DR Library Height (nm) \| 180/160"；"Contacted Poly Pitch (nm) \| 50"；"M0 Pitch (nm) \| 32"；"# of Frontside Metal Layers \| 10ML Low cost, 10ML high density, and 14-16ML high performance"；"# of Backside Metal Layers \| 3ML+3ML" | 第三方转述 Intel VLSI 2025 |
| Intel 3 → 18A 单元高度 | 240→180（HP），210→160（HD） | 搜索摘要，原文 https://www.tomshardware.com/tech-industry/semiconductors/intel-details-18a-process-technology-boosts-performance-by-25-percent-or-lowers-power-consumption-by-36-percent | "reduces cell heights from 240CH to 180CH in HP libraries and from 210CH to 160CH in HD libraries"（搜索摘要） | 第三方 |
| Panther Lake 实测金属层 | 正面 15 层 + 背面 6 层 | https://newsletter.semianalysis.com/p/intel-panther-lake-teardown （2026-09-26） | "The frontside comprises the M0-M14 signal stack, while the backside comprises the BM0-BM5 power stack." | 第三方实测 |
| 实际 M0 间距 | PDK 32 nm，HP 库出货 36 nm | 同上 | "Intel 18A PDK provides M0 pitch of 32 nm, but Panther Lake HP libraries shipped at 36 nm" | 第三方实测 |
| 18A 是 5 轨道库 | 5 track | 同上 | "The 18A logic cell dimensions point to a five-track logic library" | 第三方实测 |
| 18A 密度不领先 | — | 同上 | "However, 18A does not lead TSMC N3P, N2 or Samsung SF2 in peak density." | 第三方 |
| TSMC N3 CPP / N3E 最小金属间距 | 45 nm / 23 nm | https://en.wikipedia.org/wiki/3_nm_process （引 SemiWiki「IEDM 2022 – TSMC 3nm」） | "contacted gate pitch of N3 is 45 nm, minimum metal pitch of N3E is 23 nm," | 第三方转述 IEDM 2022 |
| N3 相对 N5 | CPP −6 nm，单鳍 | https://www.techinsights.com/blog/tsmc-reveals-3nm-process-details | "N3 reduces CPP by 6nm compared with N5."；"fins-per-transistor are reduced to a single fin." | 第三方 |
| TSMC N2 量产与结构 | 2025 Q4 量产，第一代纳米片 | https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm | "TSMC's 2nm (N2) technology has started volume production in 4Q25 as planned."；"N2 technology features industry-leading first-generation nanosheet transistor technology." | 官方 |
| N2 密度与 SRAM | 密度 +15%；SRAM 38 Mb/mm² | https://spectrum.ieee.org/tsmc-n2 （2024-12-12） | "while increasing density by 15 percent."；"38 megabits per square millimeter, or an 11 percent boost over the previous technology, N3." | 第三方报道 IEDM 2024 |
| IRDS「2nm」（2025）尺寸 | CPP 45；M0 20 / M1 23 / Mx 24；cell HD 114 / HP 138 | https://irds.ieee.org/images/files/pdf/2022/2022IRDS_MM.pdf Table MM-7、MM-10 | 表格读数：G45M20 列 "Gate pitch (nm) 45"、"M0 pitch (nm) 20"、"Cell height (nm) - HD 114" | 官方路线图（预测） |
| IRDS 金属层数（2025） | Mx 2 + 中间 12 + P720 厚层 2；布线层 17 | 同上 Table MM-13 | 表格读数："Number of wiring layers - M1+Mx+ >P40 17"、"Number of P720 layers 2" | 官方路线图 |
| 凸点间距 | 焊料凸点 130–250 µm；<130 µm 用铜柱；微凸点 35 µm | https://semiengineering.com/challenges-grow-for-creating-smaller-bumps-for-flip-chips （2023-05-18） | "Standard plated solder bumps are generally used on pitches ranging from 130µm to 250µm."；"Copper pillar is generally used below 130µm pitch,"；"Today, a 35µm bump full-array pitch is possible," | 第三方（引 Amkor） |
| SoIC 混合键合间距 | 6 µm → 2029 年 4.5 µm | https://www.eenewseurope.com/en/tsmc-soic-roadmap-2029-chip-stacking （2026-04-29） | "points from 6 µm pitches today towards 4.5 µm by 2029" | 第三方报道 TSMC |
| PowerVia 已量产 | Panther Lake，Fab 52 | https://www.allaboutcircuits.com/news/intel-unwraps-panther-lake-fist-ai-pc-platform-built-on-18a/ （2025-10-20） | "Panther Lake is the first real deployment of Intel's RibbonFET (GAA) and PowerVia (backside power) technologies"；"Intel confirmed that the compute tile is being manufactured on Intel 18A at Fab 52 in Arizona." | 第三方报道 Intel |
| PowerVia 原理 | 电源从顶层金属挪到背面 | 搜索摘要，原文 Tom's Hardware（同上 18A 文） | "relocat[ing] power delivery from the top metal layers to the rear side of the chip"（搜索摘要） | 第三方 |
| A16 结构 | 纳米片 + 背面电源轨 | https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_A16 | "TSMC A16™ technology integrates leading nanosheet transistors with innovative backside power rail solution," | 官方 |
| A16 背面接触源极 / 漏极；2026 下半年 | — | https://semiengineering.com/tsmc-uncorks-a16-with-super-power-rail （2024-04-25） | "uses a backside contact to the source"；"Backside Contact to S/D has the best area scaling of the three methods."；"targeted for the second half of 2026." | 第三方报道 TSMC |
| A16 量产时间（2024 年说法） | 2026 年底 | https://www.trendforce.com/news/?p=19205 （2024-11-26） | "on track to begin mass production of the first chips using its A16" … "by the end of 2026" | 第三方 |

---

## 5. 单个晶体管：FinFET 与 GAA（纳米片）

**结构**
- **FinFET**：硅做成竖立的「鳍」，栅极从三面包住它。
  - TSMC N3 已把每个晶体管减到单鳍。
  - IRDS 2022（「3nm」，2022 年列）给的量级：鳍宽 **5.0 nm**，器件高度 48 nm，栅长 16 nm（HP）/ 18 nm（HD）。
- **GAA 纳米片**：几片水平叠放的硅薄片，栅极四面全包。
  - TSMC N2 叫 nanosheet，Intel 叫 RibbonFET，Samsung 叫 MBCFET。
- IRDS 2022「2nm」（2025 年列）给的量级：
  - 纳米片厚度 **6.0 nm**。
  - 叠 **3 片**，片间竖直节距 18.0 nm。
  - 片宽 HP 30 / HD 15 / SRAM 7 nm。
  - 栅长 **14 nm**，器件高度 52 nm。
- 到 2034 年列：片厚 5.0 nm，叠 4 片。
- **实际片数**：
  - Intel 18A：**4 片**（SemiAnalysis、TechInsights 实测）。
  - Samsung SF2：**3 片**（SemiAnalysis）。
  - TSMC N2：片数本次未查到一手数字。
- 研究级极限：Intel 在 IEDM 2024 展示了栅长 6 nm、纳米片仅 3 nm 厚的器件。

**一个纳米片有多厚，相当于多少个原子（自算）**
- 硅晶格常数 a = 0.5431020511 nm（CODATA 2022）。
- 硅是金刚石结构。沿晶圆法向 [001]，原子层的间距是 a/4。这样数的「原子层」最适合画面：
  - a/4 = 0.5431 / 4 = **0.1358 nm**。
- 最近邻 Si–Si 键长 = a·√3/4 = 0.5431 × 1.732 / 4 = **0.2352 nm**（几何推导，不是实测引用）。
- 不同数法的结果：

| 纳米片厚度 | 晶胞数（÷ a） | 原子层数（÷ a/4） | 「原子挨原子排成一串」粗算（÷ 0.2352） |
|---|---|---|---|
| 6 nm（IRDS 2025） | 6 / 0.5431 ≈ **11.0** | 6 / 0.1358 ≈ **44** | ≈ 26 |
| 5 nm（IRDS 2034） | ≈ 9.2 | ≈ **37** | ≈ 21 |
| 3 nm（Intel 研究器件） | ≈ 5.5 | ≈ **22** | ≈ 13 |

- 讲稿建议：「一片纳米片只有大约 40 层原子厚（约 11 个硅晶胞）」。
- 若说「几十个原子厚」也成立。不要说「只有几个原子厚」：连 3 nm 的研究器件也有约 22 层原子。

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 硅晶格常数 | 0.543 102 0511(89) nm | https://physics.nist.gov/cgi-bin/cuu/Value?asil | "5.431 020 511(89) x 10⁻¹⁰ m"（CODATA 2022） | 官方（NIST） |
| FinFET 鳍宽 / 器件高 / 栅长（2022「3nm」） | 5.0 / 48 / 16–18 nm | https://irds.ieee.org/images/files/pdf/2022/2022IRDS_MM.pdf Table MM-7 | 表格读数："FinFET Fin width (nm) 5.0"、"Device height (nm) 48"、"Lg: Gate Length - HP (nm) 16" | 官方路线图 |
| 纳米片厚 / 片数 / 节距 / 宽 / 栅长（2025「2nm」） | 6.0 / 3 / 18.0 / 30·15·7 / 14 nm | 同上 | 表格读数："Lateral GAA (nanosheet) thickness (nm) 6.0"、"Number of vertically stacked nanosheets on one device 3"、"Lateral GAA vertical pitch (nm) 18.0"、"LGAA width (nm) - HP 30"、"Lg: Gate Length - HP (nm) 14" | 官方路线图（预测） |
| 2034 年纳米片 | 5.0 nm 厚，4 片 | 同上 | 表格读数 | 官方路线图 |
| Intel 18A 4 片、宽度可变 | 4 | https://newsletter.semianalysis.com/p/intel-panther-lake-teardown | "Intel 18A uses stacks of four nanosheets each and varies their widths across logic and SRAM." | 第三方实测 |
| Panther Lake 4 片纳米片 | 4 | 搜索摘要，TechInsights https://techinsights.com/ja/node/61446 | "The compute die employs high-k metal gate (HKMG) GAA transistors comprising four stacked silicon nanosheets."（搜索摘要） | 第三方 |
| Intel 研究器件 | 栅长 6 nm，片厚 3 nm | https://spectrum.ieee.org/tsmc-n2 （2024-12-12） | "a gate length of just 6 nm and a nanosheet just 3 nm thick." | 第三方报道 IEDM |
| 原子层与晶胞换算 | 6 nm ≈ 44 层 ≈ 11 晶胞 | 自算（见上方算式） | — | 自算 |

---

## 6. 「3 纳米」命名为什么和真实尺寸脱钩

**数字对比**
- 「3 nm」N3 的栅极间距是 45 nm，N3E 的最小金属间距是 23 nm。
- 这分别是 15 倍和约 8 倍于「3」。
- 即便看最小的关键尺寸（栅长约 14–16 nm、鳍宽 5 nm），也不等于 3 nm。

**历史**
- IEEE Spectrum（2020）：90 年代中期以前，节点名等于栅长。之后两者脱钩，「约二十年」名不副实。
- IRDS 2022 承认：各家对节点命名没有共识。IRDS 自己改用 **GxxMxx** 记法：G = 接触栅极间距，M = 最紧金属间距。
  - 例：「2nm」= G45M20。
- Wikipedia 转述 IRDS 2021：「3 nm」「has no direct relation to any actual physical feature」。这句本次未直接核对 IRDS 2021 原文，属转述。

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 节点名不反映物理尺寸 | — | https://spectrum.ieee.org/a-better-way-to-measure-progress-in-semiconductors （Samuel K. Moore，2020-07-21） | "The picture the semiconductor technology node system paints is false."；"Most of the critical features of a 7-nm transistor are actually considerably larger than 7 nm," | 第三方（权威媒体） |
| 脱钩已约 20 年；90 年代中期前节点 = 栅长 | 约 20 年 | 同上 | "that disconnect between nomenclature and physical reality has been the case for about two decades."；"Before the mid-1990s, logic technology nodes were synonymous with the gate length of the CMOS transistors they produced." | 第三方 |
| 替代指标 LMC | — | 同上 | "An alternative to the node metric, called LMC," | 第三方 |
| IRDS：节点命名无共识 | — | https://irds.ieee.org/images/files/pdf/2022/2022IRDS_MM.pdf p.6 | "There is not yet a consensus on the node naming across different foundries and integrated device manufacturers (IDMs)" | 官方路线图 |
| IRDS 的 GxxMxx 记法 | 「2nm」= G45M20 | 同上 Table MM-7 注 | "GxxMxx/Tx notation refers to Gxx: contacted gate pitch, Mxx: tightest metal pitch in nm, Tx: number of tiers." | 官方路线图 |
| IRDS 2021 原话（经转述） | — | https://en.wikipedia.org/wiki/3_nm_process （引 IRDS 2021 More Moore p.7） | "has no direct relation to any actual physical feature" | 第三方转述官方 |
| 「2 nm」是营销用语 | — | https://en.wikipedia.org/wiki/2_nm_process | "2 nm is used primarily as a marketing term by the semiconductor industry to refer to a new, improved generation of chips" | 第三方 |
| 倍数换算 | 45 / 3 = 15；23 / 3 ≈ 7.7 | 自算 | — | 自算 |

---

## 7. 尺度类比（全部自算，基于下表来源）

**来源数据**
- 头发直径 17–181 µm（Ley 1999，Wikipedia 引用）。
- 红细胞直径 6.2–8.2 µm。
- SARS-CoV-2 病毒颗粒 60–140 nm（NEJM 2020 电镜）。

**以头发为尺**
- 头发直径 ÷ CPP（48 nm 取整，18A 为 50 nm）：17 000 / 48 ≈ **354**；181 000 / 48 ≈ **3 771**。
  - 讲稿说法：「一根头发的宽度里，能并排放几百到几千根晶体管的栅极」。
- A20 Pro die 宽 8.0 mm ÷ 头发：8 000 / 181 ≈ 44；8 000 / 17 ≈ 471。
  - 讲稿说法：「一颗手机芯片的短边，大约相当于几十到几百根头发并排」。
- 晶圆厚 775 µm ÷ 头发：775 / 181 ≈ 4.3；775 / 17 ≈ 46。
  - 讲稿说法：「晶圆只有几根到几十根头发叠起来那么厚」。
- 18A 标准单元高 160 nm ÷ 头发：17 000 / 160 ≈ 106；181 000 / 160 ≈ 1 131。
  - 讲稿说法：「一根头发宽度上能排一百到一千多行标准单元」。

**以红细胞为尺**
- 红细胞 6.2–8.2 µm ÷ CPP 48 nm ≈ **129–171**：一个红细胞宽度上约排一百多根栅极。

**以病毒为尺**
- 病毒 60–140 nm ÷ CPP 48 nm ≈ **1.25–2.9**：一颗新冠病毒约等于 1–3 个栅极间距。
- 讲稿说法：「病毒放在晶体管旁边差不多一样大」。这是很好的「同尺度」画面点。

**以原子为尺**
- 纳米片 6 nm ≈ 44 层硅原子（见第 5 节）。

**避免**
- 不要用「人类头发 = 100 µm」作精确定值。来源给的是 17–181 µm 范围。
- 讲稿要写单一数字时，用「几十微米」或「大约 0.1 毫米以下」。

| claim | 数字 | 出处 URL | 原文 quote | 官方/第三方 |
|---|---|---|---|---|
| 头发直径 | 17–181 µm | http://hypertextbook.com/facts/1999/BrianLey.shtml （Wikipedia「Hair」的 ref [10]） | "In my research, I have found the diameter of human hair to range from 17 to 181 μm (millionths of a meter)." | 第三方（汇编型） |
| 头发直径（Wikipedia） | 0.017–0.18 mm | https://en.wikipedia.org/wiki/Hair | "The diameter of human hair varies from 0.017 to 0.18 millimeters (0.00067 to 0.00709 in)." | 第三方 |
| 红细胞 | 直径 6.2–8.2 µm，厚 2–2.5 µm | https://en.wikipedia.org/wiki/Red_blood_cell （引 Turgeon, *Clinical Hematology*, 2004, p.100） | "A typical human red blood cell has a disk diameter of approximately 6.2–8.2 μm"；"a maximum thickness of 2–2.5 μm and a minimum thickness in the centre of 0.8–1 μm" | 第三方转述教科书 |
| 新冠病毒颗粒 | 60–140 nm | https://pmc.ncbi.nlm.nih.gov/articles/PMC7092803/ （Zhu et al., NEJM 2020;382:727–733） | "Diameter varied from about 60 to 140 nm." | 一手论文 |
| 各类比倍数 | 见上方算式 | 自算 | — | 自算 |

---

## 8. 给画面的建模尺寸表

建议每级画面右下角的比例尺读数用 1-2-5 序列取整。「应出现的结构」都基于上文可核数字。

| 级别 | 建议比例尺读数 | 画面视野宽度（约） | 该级应出现的结构与真实尺寸 | 真实性 |
|---|---|---|---|---|
| 0 晶圆 | **10 cm** | 40 cm | 300 mm 圆盘，厚 0.775 mm（侧视时薄如纸片，直径/厚度 ≈ 387:1）；边缘有缺口（notch）；表面是约 600+ 个矩形 die 的网格（A20 Pro 级 8.0×12.3 mm），网格之间是划片道；外圈 3 mm 边缘排除区和不完整的边角 die | 可按真实比例建模 |
| 1 一颗芯片 | **2 mm** | 15 mm | 8.0 × 12.3 mm（手机 SoC）或约 29 × 29 mm（814 mm² AI GPU，≈ 光罩极限）；die 表面分块：CPU 簇、GPU 阵列、NPU、SLC（大块规整 SRAM）、边缘的长条内存 PHY 与 IO | 外形与尺寸真实；**分块颜色和边界是示意**（真实正面被金属覆盖，die shot 的彩色是去层后拍摄或伪彩标注；各块占比无权威一手数据） |
| 2 功能区 | **200 µm** | 1 mm | 一个 CPU 簇，或一块 SRAM 阵列（规则瓷砖状）对比逻辑区（随机细纹）；顶部金属的粗电源网 | **示意**：功能区 mm² 精确值未查到 |
| 2.5 封装接口（可选插入） | **100 µm** | 0.5 mm | 焊料凸点间距 130–250 µm；铜柱 <130 µm；微凸点 35 µm；混合键合 6 µm（远小于凸点，像整面贴合） | 尺寸可按来源；形状示意 |
| 3 金属层剖面 | **1 µm** | 3 µm | 从上到下：厚的顶层金属（IRDS 720 nm 间距，2 层）→ 中间层（12 层左右）→ 最细的 M0/M1（20–36 nm 间距）→ 接触 → 晶体管。18A 实测正面 15 层；有 PowerVia 时晶体管下方再加 6 层背面供电层 | 层数和间距按来源；**线宽与层厚比例示意**（各层厚度本次未查） |
| 4 标准单元 | **100 nm** | 500 nm | 一排排等高的单元：高 160 nm（18A HD，5 条 M0 轨道，M0 间距 32 nm）；竖直栅极线等间距 50 nm（18A）或 45 nm（N3）；单元上下边是电源轨（18A 的电源轨在背面）；一个与非门约 2–3 个 CPP 宽 | 节距真实；**门的宽度（几个 CPP）是示意** |
| 5 单个晶体管 | **10 nm** | 60 nm | GAA：3–4 片水平硅纳米片，每片厚 5–6 nm、宽 15–30 nm、竖直节距 16–18 nm，栅长 12–16 nm，栅极四面包住；对照 FinFET：竖鳍宽 5 nm、高 ~48 nm（IRDS 2022） | 取 IRDS 量级，**不是某一家产品的实测**（TSMC N2、Samsung 实测值在付费墙后）；材料分层（高 k 介质、功函数金属、内侧墙）只能示意 |
| 6 原子尺度 | **1 nm** | 5 nm | 金刚石结构硅晶格，晶格常数 0.543 nm，原子层间距 0.136 nm，键长 0.235 nm；6 nm 纳米片 ≈ 44 层原子 / 11 个晶胞 | 晶格几何真实；**原子画成小球是示意**（原子没有清晰边界）；界面、表面粗糙度、栅介质的原子排布只能示意 |

**只能示意的画面与原因**

1. **「从正面一路看下去就能看到晶体管」只能示意**。
   - 晶体管被正面十几层金属盖住（18A 实测 M0–M14），从上方实际看不到。
   - 镜头里应表现为「穿过 / 剥开金属层」。
2. **die 表面的彩色功能区地图只能示意**。
   - 公开 die shot 是爆料人或拆解机构拍的，常经去层和伪彩标注。
   - 区块占比也缺少权威一手数据。
3. **连续变焦是蒙太奇**。
   - 一路缩小的连续镜头把不同来源、不同节点的尺寸拼在了一起：晶圆 / die 用 A20 Pro，单元用 18A，晶体管用 IRDS 路线图量级。
   - 字幕或旁白应避免说「这颗芯片里的晶体管就是这样」，改说「先进芯片里的晶体管大致是这样」。
4. **背面供电只能示意**。
   - PowerVia / A16 的芯片有正反两面金属网。
   - 晶圆如何翻面、减薄、键合，本次未核到一手细节。
5. **原子级画面只能示意**。
   - 晶格常数真实，但原子的「球」、颜色、边界都是示意。
   - 纳米片和栅介质的界面不是理想平面。
6. **光罩极限有两种说法**（26×33 mm = 858 mm²，或 SemiEngineering 的「26 mm square / 676 mm²」）。
   - 画面里如需表示 AI GPU「顶到光罩上限」，用「约 800 多平方毫米、接近上限」，不要标精确值。
   - 精确值等 ASML / SEMI 原文核实。

---

## 未查到 / 待补

- TSMC N2、A16 的官方 CPP、金属间距、cell height、纳米片片数。
- Samsung SF3 / SF2 的 CPP 与金属间距。
- A19 / A20 Pro 晶体管数；Apple M4 / M5 的 die 面积（只有论坛数字，未采用）。
- Blackwell 单 die 面积。
- SEMI M1 标准原文中的 300 mm 晶圆厚度。
- ASML 官方曝光场尺寸。
- 主流手机 SoC 各功能区的 mm² 分解。
- 各 BEOL 层厚度。
- C4 凸点的主流封装实际间距：只有「130–250 µm」区间，没有具体产品值。
- TSMC A16 是否已于 2026 Q4 正式量产（未见 TSMC 一手公告）。
