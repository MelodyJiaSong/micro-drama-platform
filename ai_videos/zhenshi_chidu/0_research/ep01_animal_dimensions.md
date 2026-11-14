# ep01 · 世界最大陆地动物 Top 30 · 尺寸数据（肩高 / 头体长）

> 2026-11-06 代理整理。机读版：同目录 `ep01_animal_dimensions.json`（30 条）。名次、物种、体重照抄 `ai_videos/paihangbang/episodes/ep04_largest_land_animals/data.json`，本文件只补尺寸。
> 调研：三路并行子任务（名次 1–10 / 11–20 / 21–30）逐条打开出处页，主会话汇总复核。没有调用收费服务。所有 `retrieved_at` = 2026-11-06。

## 1. 口径

- **对象**：成年雄性，取典型值或平均值，不取纪录最大值；尺寸要和 ep04 的体重口径对得上（例：非洲草原象 6,000 kg ↔ Larramendi 2016 的平均成年公象肩高 3.20 m）。
- **肩高（shoulder height, SH）**：四足站立时，地面到肩胛最高点（鬐甲）。象类的背部或头顶可能比肩高（HMW 对亚洲象有说明），建模时肩高按本表，背线另按参考图。
- **头体长（head-and-body length, HB）**：吻端到尾根，**不含尾**；取直线长度，用于 3D 包围盒。
  - **象**：已发表的「head-body」都**含象鼻**（例如草原象 6.0–7.5 m），不能直接用。本表的 HB 是「前额到臀部、不含鼻」，从 Larramendi 2016 的比例复原图量出来，标 est.。
  - **长颈鹿**：HB 沿颈部量，从吻到尾根（总长 5.05 m 减尾长），**不是**躯干的水平长度。
  - 一些出处的体长是沿体表曲线量的（例如爪哇犀），会比直线长略长，已在 notes 里注明。
- **取值方式**（`value_kind`）：`mean` = 出处给出的均值；`midpoint` = 范围中点；`typical` = 出处给出的典型单值；`est.` = 换算、推算，或多个来源冲突后的判断值。出处只给范围的，一律取中点。
- **性别**（`sex_basis`）：只有雌雄混合数据的，注明「sexes pooled」。混合范围含雌性和亚成体，雄性真实值可能略高于中点，这类条目在表里标「混合」。
- **来源分级**：沿用 paihangbang bible §3.2。主值优先用同行评审文献（ASM *Mammalian Species* 物种志、Larramendi 2016、Krasińska & Krasiński 2002、Jensen et al. 2013 等）和权威汇编（《Handbook of the Mammals of the World》，简称 HMW，经 Plazi 读原文；San Diego Zoo Wildlife Alliance Library，简称 SDZWA；Animal Diversity Web，简称 ADW；IUCN SSC 亚洲野牛专家组，简称 AWCSG；Britannica；NPS）。维基百科只当线索，凡是经维基转读的都标出来。
- **差异阈值**：主值和交叉核对差异超过 15% 的，在 §3 写明取哪个、为什么（bible 的 10% 规则针对屏上的主值；尺寸只用于建模，按任务约定用 15%）。

## 2. 总表

单位：m。缩写：SH = 肩高，HB = 头体长（不含尾），MS = *Mammalian Species*。

| 名次 | 物种 | 肩高 | 体长 | 主来源 | 交叉核对 | 备注 |
|---|---|---|---|---|---|---|
| 1 | 非洲草原象 *Loxodonta africana* | 3.20 | 4.1 est. | Larramendi 2016（SH 与 6 t 挂钩；HB 从复原图量取）；HMW | SDZWA 公象 SH 2.9–3.7（中点 3.3，+3%） | HB 不含鼻；尾 1.25 |
| 2 | 亚洲象 *Elephas maximus* | 2.75 | 3.3 est. | Larramendi 2016；HMW | SDZWA SH 2.7（−2%）；de Silva 2014 比例法 HB≈3.25 | 背部或头顶可高于肩 |
| 3 | 白犀牛 *Ceratotherium simum* | 1.78 | 3.80 | HMW；Groves 1972 MS 8 | SDZWA 1.78 / 3.9（+3%） | 混合；尾长冲突 |
| 4 | 印度犀牛 *Rhinoceros unicornis* | 1.75 | 3.75 | Laurie 等 MS 211（SH 为雄性实测均值，n=9）；ADW（HB 雄性） | HMW 1.875 / 3.35–3.46 | HB 三个来源差约 19% |
| 5 | 非洲森林象 *Loxodonta cyclotis* | 2.20 | 2.8 est. | Larramendi 2016 | SDZWA 转引 Turkalo & Barnes 2013：2.30 / 2.44 | 没有称重个体；HB 按草原象比例推算 |
| 6 | 河马 *Hippopotamus amphibius* | 1.58 | 4.0 | SDZWA；HMW（范围中点） | ADW 高 1.50–1.65，长 2.09–5.05 | HB 可能偏长，见 §3 |
| 7 | 爪哇犀牛 *Rhinoceros sondaicus* | 1.60 | 3.25 | HMW；Groves & Leslie 2011 MS 43 | ADW SH≈1.7（+6%） | 混合；体长沿体表量 |
| 8 | 长颈鹿 *Giraffa camelopardalis* | 3.31 | 4.1 | SDZWA（转引 Ciofolo & Le Pendu 2013 雄性均值）；HMW | ADW 公 SH 3.3，到角 5.7 | **总高 5.3 est.**（到皮骨角顶）；HB 含颈 |
| 9 | 黑犀牛 *Diceros bicornis* | 1.55 | 2.95 | Hillman-Smith & Groves 1994 MS 455（体重-体长回归）；HMW | SDZWA 1.60 / 3.3（HB +12%） | 混合；尾长冲突 |
| 10 | 印度野牛 *Bos gaurus* | 1.88 | 2.9 | Nowak 1999 雄性均值（经维基转读）；HMW | AWCSG SH 1.5–2.2 / HB 2.5–3.3 | HB 混合中点 |
| 11 | 野牦牛 *Bos mutus* | 1.89 | 3.25 est. | Leslie & Schaller 2009 MS 836（雄性 175–203 cm）；HMW | AWCSG 1.80 / 3.10（混合） | HB 是估计值 |
| 12 | 印度水牛 *Bubalus arnee* | 1.75 | 2.70 | AWCSG；HMW | HMW 1.70 / 2.70 | 混合，雄性可能略大 |
| 13 | 美洲野牛 *Bison bison* | 1.74 | 3.04 | Halloran 1960 雄性均值（经 Krasińska & Krasiński 2002 转引）；Meagher 1986 MS 266 | Meagher SH 1.765 / HB≈2.9 | n=7 |
| 14 | 苏门答腊犀牛 *Dicerorhinus sumatrensis* | 1.25 | 2.77 | HMW | 国际犀牛基金会（IRF）1.25 / 2.50（−10%） | 混合；尾长无数据 |
| 15 | 非洲水牛 *Syncerus caffer* | 1.62 | 2.90 | HMW | Alden 1995（经 Ultimate Ungulate）1.50 / 2.90 | 混合；尾长冲突 |
| 15 | 爪哇野牛 *Bos javanicus* | 1.60 | 2.6 est. | HMW；AWCSG；ADW | Hoogerwerf 1970（经维基转读） | **HB 来源冲突超过 15%** |
| 17 | 德氏大羚羊 *Tragelaphus derbianus* | 1.63 | 2.90 | HMW（HB 雄性） | Kingdon 1997（经 Ultimate Ungulate）1.63 / 2.80 | 尾长冲突 |
| 18 | 欧洲野牛 *Bison bonasus* | 1.72 | 2.57 | Krasińska & Krasiński 2002 Table 3（雄性实测均值，n=39） | HMW 1.75 / 2.80（+9%） | — |
| 19 | 伊兰羚羊 *Tragelaphus oryx* | 1.59 | 2.95 | HMW（雄性） | Kingdon 1997（经维基转读）1.665 / 2.925 | Pappas 2002 原文未见 |
| 20 | 驼鹿 *Alces alces* | 2.00 | 2.75 | HMW（雄性范围中点） | Jensen et al. 2013（*Alces*）实测 ≈1.95 / 2.63 | 含角总高缺 |
| 21 | 北极熊 *Ursus maritimus* | 1.45 | 2.2 est. | DeMaster & Stirling 1981 MS 145 | Britannica 雄性 SH≈1.6 / 长 2.2–2.5 | 站立高 3.0 是上限说法 |
| 22 | 细纹斑马 *Equus grevyi* | 1.50 | 2.63 | HMW | Ultimate Ungulate 1.525 / 2.5–2.75；SDZWA、ADW 的 SH 1.35 | 混合 |
| 23 | 藏野驴 *Equus kiang* | 1.40 | 2.10 | ADW；Ultimate Ungulate | HMW 1.37 / 1.98 | 混合 |
| 24 | 棕熊 *Ursus arctos* | 1.35 | 2.2 est. | Seryodkin et al. 2016（堪察加雄性实测，按体重缩放） | NPS Katmai 雄性长 2.1–3.0（+16%） | 站立高 2.44（ADW，混合） |
| 25 | 加拿大马鹿 *Cervus canadensis* | 1.55 | 2.25 | HMW（雄性） | NPS Yellowstone SH≈1.52（−2%） | HB 没有第二个来源 |
| 26 | 扭角羚 *Budorcas taxicolor* | 1.20 | 2.15 | ADW；SDZWA（雄性） | HMW 1.235 / 1.95（混合） | — |
| 27 | 麝牛 *Ovibos moschatus* | 1.45 est. | 2.25 | ADW（HB 雄性）；ADF&G | ADF&G 公 SH≈1.52；ADW 1.20 | **SH 来源冲突超过 15%** |
| 28 | 紫羚 *Tragelaphus eurycerus* | 1.25 | 2.28 | HMW | Ultimate Ungulate 1.20 / 2.10 | 混合 |
| 29 | 山斑马 *Equus zebra* | 1.44 | 2.35 | ADW（转引 Penzhorn 1988，7 岁以上公马均值）；HMW | krugerpark.co.za 公 SH 1.5 | 298 kg 的公马可能约 1.40 |
| 30 | 平原斑马 *Equus quagga* | 1.30 | 2.52 | SDZWA（雄性范围中点） | HMW 1.335 / 2.315（−8%） | — |

可选列（详见 JSON）：
- **总高**：长颈鹿 5.3（est.）。北极熊站立 3.0、棕熊站立 2.44 只能作参考，不是均值。驼鹿含角高没有找到权威来源，填 null。
- **尾长**：除苏门答腊犀外都有值。

## 3. 差异与取舍记录

超过 15% 的冲突，以及接近阈值、需要人决定的条目：

1. **象类 HB（1、2、5）**：已发表的 HB 全部含鼻，没有不含鼻的实测均值。草原象 4.1 和亚洲象 3.3 是在 Larramendi 2016 复原图上量的比例乘以肩高。亚洲象另有 de Silva 2014 的独立估算（耳孔到尾根≈肩高），两者相差不到 2%。森林象 2.8 按草原象比例推算；Turkalo & Barnes 2013（经 SDZWA 转引）给 2.44，低 13%，量法不明。保留 2.8，以便和体重口径一致。
2. **印度犀 HB（4）**：MS 211 给 4.12（性别未注明，可能沿体表量），ADW 雄性 3.70–3.80，HMW 3.35–3.46，最大差约 19%。取 ADW 的雄性中点 3.75：它是雄性专属值，又居三者中间，也和白犀（2.3 t，3.8 m）相称。缺点是 ADW 这条没有标出处。
3. **河马 HB（6）**：雄性范围 3.00–5.05，中点 4.03，按规则取 4.0。但 5.05 的上限像是纪录个体，均值雄性可能更短；常见资料给 3.3–3.45。如果要保守，取 3.5 也站得住（差 14%）。**建议人工定**。
4. **黑犀 HB（9）**：MS 455 引 Freeman & King 1969 的体重-体长回归，1,150 kg 对应 2.95，并且和白犀、印度犀按等比缩放的结果（约 3.0）一致。HMW 中点 3.40 高 15%，SDZWA 3.3 高 12%。取 2.95，因为它和体重口径挂钩。尾长：HMW 0.25–0.35，SDZWA 0.60–0.70，相差一倍，取 0.65。
5. **爪哇野牛 HB（15）**：Walker's、HMW、ADW 给 1.90–2.25（中点 2.08），AWCSG 给 2.45–3.83（中点 3.14，疑似含尾），Hoogerwerf 1970 给 1.9–3.68。2.08 的 HB/SH 只有 1.3，对 700 kg 的野牛太短（同批其他野牛在 1.5–1.8 之间）；3.14 又可能含尾。取 2.6 est.（HB/SH≈1.6）。
6. **麝牛 SH（27）**：阿拉斯加渔猎局（ADF&G）说公牛约 5 英尺（1.52），ADW 说「通常 120 cm」（混合，低 21%），HMW 混合范围 1.20–1.51。雄性比雌性大约 25%，取 1.45 est.。
7. **尾长冲突**（只影响建模细节）：白犀 0.6 对 0.9（取 HMW 0.6）；非洲水牛 0.80 对 0.65（取 HMW 0.80，可能含尾毛簇）；德氏大羚羊 0.90 对 0.67（取 Kingdon 0.67）。
8. **接近阈值、仍取主来源的**：棕熊（Katmai 的长度高 16%，可能是总长或沿体表量）、细纹斑马 SH（SDZWA、ADW 的「平均 1.35」低 10%，可能是全体均值）、苏门答腊犀 HB（IRF 低 10%）、北极熊（SDZWA 体长高 14%，可能沿体表量）。
9. **推算值**：棕熊没有 340 kg 雄性的实测均值。用 Seryodkin et al. 2016 堪察加 7 岁以上雄性（237 kg：SH 1.25，体长 2.07）按体重立方根缩放，得 1.41 / 2.33；考虑到大个体部分是胖出来的，取中间值 1.35 / 2.2。北极熊 HB 是 MS 145 的雄性鼻到尾尖 2.0–2.5 的中点减去约 0.10 m 尾长。长颈鹿总高取 HMW 混合「到冠顶」4.5–6.0 的上半段，5.3 低于 ADW 给的大公鹿 5.7。

## 4. 未核实项清单

以下数值没有追到原始文献，只读到二手转引，发布前若要上屏须再核：

- **印度野牛 SH 1.88**：Nowak 1999（Walker's）原书未开，只经维基转读；和 HMW、AWCSG 的范围一致（差 3% 以内）。ep04 的体重同样经维基转读。
- **长颈鹿**：SH 3.31 来自 Ciofolo & Le Pendu 2013，只经 SDZWA 转引；总高 5.3 est. 没有雄性均值可依；HB 由总长减尾长推得。
- **象类 HB（1、2、5）**：从复原图量取或推算，不是发表的测量值。
- **美洲野牛**：Halloran 1960 的雄性均值只经 Krasińska & Krasiński 2002 转引（Meagher 1986 已读，一致）。
- **伊兰羚羊**：Pappas 2002（MS 689）的测量值未见；交叉核对 Kingdon 1997 只经维基。
- **爪哇野牛**：HB 是冲突后的判断值；Hoogerwerf 1970 原页未开；公牛 SH 均值 1.6 只在维基上见到。
- **野牦牛**：HB 3.25 est. 和尾长未追到原始测量。
- **山斑马 SH 1.44**：Penzhorn 1988 原文未开，只经 ADW 转引；交叉核对 krugerpark.co.za 是旅游网站，权重低。
- **扭角羚 SH**：经 ADW 转引 Parker 1989 / Nowak 1999，原文未开。
- **斑马、麝牛、熊等 MS 物种志**（Churcher 1993、Penzhorn 1988、Lent 1988、Neas & Hoffmann 1987、Pasitschniak-Arts 1993 等）：需付费或站点无法访问，相关数值依靠 HMW、ADW、SDZWA 等二手汇编。
- **雌雄混合**（雄性值可能偏低）：白犀、河马（SH）、爪哇犀、黑犀、印度水牛、苏门答腊犀、非洲水牛、细纹斑马、藏野驴、紫羚，以及多数条目的尾长。
- **黑犀**：Freeman & King 回归里「body length」的量法 MS 455 没有说明。
- **平原斑马**：SDZWA 的测量表没有逐行注明出处。
- **缺项**：驼鹿含角总高、苏门答腊犀尾长。
- **IUCN 页面**：iucnredlist.org 对抓取返回 403（同 ep04），本期没有引用 IUCN 评估页的尺寸。

## 5. 人体参照取值建议

- **全球均值 1.71 m**：Our World in Data 的「Human Height」页写明，1996 年出生的成年男性全球平均身高 171 cm（女性 159 cm），数据来自 NCD-RisC 2016（eLife 5:e13410，*A century of trends in adult human height*，DOI 10.7554/eLife.13410）。注意：NCD-RisC 论文本身只给各国数值，没有给全球均值（全文已核）；171 cm 是 OWID 基于 NCD-RisC 数据的汇总。出处：https://ourworldindata.org/human-height ；https://pmc.ncbi.nlm.nih.gov/articles/PMC4961475/ （retrieved 2026-11-06）。
- **建议**：旁白或字幕说「an average man」时，用 **1.71 m**，出处写 NCD-RisC / Our World in Data。如果想用整数 **1.75 m（5′9″）**，屏上直接标「1.75 m man」，不要称为平均值：1.75 m 是常用的取整值，高于全球均值，本次没有为它找权威出处（欧美多国男性均值在 1.75–1.83 之间，未逐国核对）。同一期内只用一个值。

## 用户决定与代理取舍（2026-11-06，follow-up 001）

- **排序口径**：用户定「按高度排名」。物种集合沿用排行榜 ep04（体重前 30），排序改为**肩高**——30 条都有、口径一致；总高只有少数物种有，且熊类「总高」是站立高，不可比。肩高相同的并列同名次，名次内按体重从大到小排。
- **人体参照**：用户定 1.75 m，画面标「1.75 m man」，不称「平均」（全球成年男性平均 1.71 m 只作备注，见上文）。
- **分歧取值（用户授权代理定）**：
  - 河马 HB 改为 **3.5 est.**（原 4.0）：范围上限像纪录个体，按「典型值优先」取保守值。
  - 印度犀 HB 3.75、黑犀 HB 2.95、爪哇野牛 HB 2.6 est.、麝牛 SH 1.45 est.：维持上文取值与理由。
  - 体长只作辅助信息与模型比例复核，不影响名次；麝牛 SH 影响名次（与北极熊并列第 22）。
