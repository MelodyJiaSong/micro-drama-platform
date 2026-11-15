# 事实核查报告（script 第 2 轮）

结论：**必改 0 · 建议 1 · 记录 2**。C01–C19 已逐项核对；上一轮 factcheck 的 13 项均已解决。未发现新的数字归属、单位换算、因果方向或双语限定语错误。

## 本轮问题

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l43 | 双语 | 建议 | 「这一路你看到的颜色／All the colors」还包括芯片外的米、头发，以及蓝白信号、橙色电子等特效；它们不都是「为了分清材料涂上去的」。材料原图灰度这一结论本身正确，但范围说满了。 | zh：[林] 工程师拍这儿，用的是电子显微镜，原图是灰的。所以进芯片以后，这些材料的颜色都是我们后加的，方便区分。<br>en：[Lin] Engineers use electron microscopes here, and the raw pictures are gray. The material colors inside the chip were added so we can tell them apart. |
| l04 | 双语 | 记录 | C01 的 lines 收了 l04，但 claim 正文只登记晶体管数和人均换算，没有登记「芯片是用大量晶体管工作的薄片」这一定义；事实成立，登记口径不完整。 | 在 C01 的 claim 末尾补：「芯片是用大量晶体管工作的薄片。」 |
| l23 | 双语 | 记录 | 91 句中仅 l23 未出现在任何 claim 的 lines 中；该句只是城市类比和提问，没有新增事实，但破坏台账的句号全覆盖。 | 将 l23 加入 C19 的 lines。 |

## claims.json 逐项复核

| 编号 | 结论 | 核对证据 |
|---|---|---|
| C01 | 通过 | [Tom's Hardware 原文](https://www.tomshardware.com/news/apple-a17-pro-3nm-iphone-15-pro)确为 “The A17 Pro boasts 19 billion transistors…”，不是其他型号或其他部件的数字。按 UN WPP 2024 的 2026 年 7 月 1 日世界人口预测 8,300,678,396 人，190÷83.00678396＝2.289，故「两个多」成立；l04 的登记缺项另记。 |
| C02 | 通过 | 1.7 m ÷ 100 nm＝17,000,000；log10(17,000,000)＝7.230，符合「七格多、每格十倍」。 |
| C03 | 通过 | [nano.gov 原文](https://www.nano.gov/about-nanotechnology/just-how-small-is-nano/)为 “A human hair is approximately 80,000–100,000 nanometers wide.”，即 80–100 µm。 |
| C04 | 通过 | 封装、焊球供电/接地/信号、正面朝下及二氧化硅中的硅元素均表述准确；没有再把焊球多归结为单一通信原因。[TSMC InFO](https://www.tsmc.com/english/dedicatedFoundry/technology/InFO) 与 flip-chip 定义支持该封装语境，翻转被明确说成讲解动作。 |
| C05 | 通过 | 不同功能区都使用晶体管、分区色为后加、器件上方有十几层互连，与研究档案 F06 及 [Hamburg CMOS 教学](https://tams.informatik.uni-hamburg.de/applets/cmos/)一致；没有声称裸眼可从表面可靠读出功能分区。 |
| C06 | 通过 | 15 层正面信号金属支持「十几层」；「大多是铜」给最底层其他金属留了余地。上层粗、下层细密、相邻层换向及通孔选择连接的口径正确，未把方向交替说成导线本身绝缘的原因。 |
| C07 | 通过 | 电子局部漂移与电场/信号传播被分开；弹珠明确标为近似，并补上「不是机械碰撞、传播也需要时间」。[Lessons in Electric Circuits](https://www.ibiblio.org/kuphaldt/electricCircuits/DC/DC_1.html) 的弹珠类比没有被扩大成芯片内精确速度。 |
| C08 | 通过 | [NASA](https://science.nasa.gov/ems/09_visiblelight/) 给 380–700 nm，讲稿约作 400–700 nm合理；比较对象始终是相邻导线**中心间距**与波长，不是线宽或边缘空隙；英文 “struggles” 保留非绝对语气。 |
| C09 | 通过 | [NIGMS](https://nigms.nih.gov/biobeat/2016/12/cool-image-adding-color-to-the-gray-world-of-electron-microscopy) 说明标准 EM 图像为灰度、颜色后加；l44 只说显微图像像老照片，没有再说实物本来就是灰色。l43 的范围问题另记。 |
| C10 | 通过 | [Intel 官方](https://www.intel.com/content/www/us/en/newsroom/news/corporate/intel-foundry-details-process-milestones-future-innovation-at-vlsi-symposium.html)写明 18A 的 contacted poly pitch 为 50 nm；80,000÷50＝1,600，100,000÷50＝2,000。讲稿限定「一种先进工艺」，没有把示例推广成所有芯片。 |
| C11 | 通过 | [IEEE Spectrum](https://spectrum.ieee.org/a-better-way-to-measure-progress-in-semiconductors)支持节点名与物理尺寸脱钩；现稿是「不直接对应哪一条边／一代工艺的名字」，没有过度改成「毫无技术含义」。 |
| C12 | 通过 | IRDS 2022 的 6 nm 属路线图量级，Intel 18A 四纳米片实测支持 3–4 片的示例范围；讲稿明示「一种先进……来示意」，未声称所有手机芯片均为该尺寸。 |
| C13 | 通过 | Z3 等早期计算机确用继电器；通电后电磁铁吸动衔铁、触点接通的描述正确，且只说「有些」早期计算机。 |
| C14 | 通过 | [Toshiba 原文](https://toshiba.semicon-storage.com/us/semiconductor/knowledge/e-learning/discrete/chap3/chap3-7.html)分别施加 VDS、正向 VGS，电子在栅绝缘层下形成反型通道并连接源漏。现稿有增强型、足够正栅压、绝缘层、无机械运动及关态非零漏电等必要边界；磁铁只类比隔空施力。 |
| C15 | 通过 | [Hamburg 原文](https://tams.informatik.uni-hamburg.de/applets/cmos/)明确一个 N 型和一个 P 型晶体管组成 CMOS 反相器，输入 1/0 时输出 0/1；现稿没有说单个反相器能存照片。 |
| C16 | 通过 | [Qualcomm 官方规格](https://www.qualcomm.com/smartphones/products/8-series/snapdragon-8-elite-gen-5)为最高 4.74 GHz，即每秒 47.4 亿周期，支持「几十亿拍」；中英均保留「不是每个开关每拍都翻转」。 |
| C17 | 通过 | [NIST CODATA](https://physics.nist.gov/cgi-bin/cuu/Value?eqasil) 的硅晶格常数为 0.5431020511 nm；沿 [001] 按 a/4 计，6÷(0.5431020511÷4)＝44.19，故「四十几层」成立。现稿没有由厚度推出逐原子层制造方式。 |
| C18 | 通过 | 以 A17 Pro 的 103.8 mm² 示例复算：线性放大 17e6 后面积为 29,998.2 km²，是[北京市 16,410.54 km²](http://tz.mofcom.gov.cn/AboutChina/art/2020/art_7e79b5d83bb14dd6a7812a0990dfbd6a.html)的 1.828 倍；平均每个晶体管为 1.579 m²，边长 1.257 m。即使用台账 114 mm² 上界，也分别为 2.008 倍和 1.317 m。台词只比面积，未再混用长度。 |
| C19 | 基本通过 | 人物反应、缩小、点击路径及城市/弹珠/地铁等修辞可归故事或类比；点击是传到目标开关而非由此发起。l23 漏挂 lines 另记，无新增事实。 |

## 其他必查项

- **夸大与因果**：除 l43 的颜色范围外，未发现把示例说成通用规格、把相关说成因果或把到达说成发起；焊球多因、时钟频率、环绕栅漏电均有恰当限定。
- **引文与双语翻译**：已逐句对照 91 组中英文；未发现改变数字、方向、因果或限定强度的翻译。「part of silicon dioxide」忠实表达组成关系，没有译成单质硅或「一半」。
- **专业概念与类比**：互连中心距、电子漂移与信号传播、增强型 N 沟道反型、CMOS 反相器、纳米片厚度及线性/面积放大均在所述示例和类比边界内成立。
- **未登记事实**：l04 是「已挂句号但 claim 正文漏内容」，l23 是「纯类比句漏挂句号」；除此之外未发现未登记的新增事实性说法。
- **画面文字范围**：所给 lines.md 只有段标题与中英台词，没有独立屏幕文字清单；本报告未声称核过未提供的屏幕标签。

## R：上一轮 factcheck 问题复核

| 句号 | 结论 | 当前证据 |
|---|---|---|
| l03 | 已解决 | 改为 A17 Pro 的 190 亿，人均 2.289 个，不再让「一百亿」也对应「两个多」。 |
| l16 | 已解决 | 供电、接地、数据均列入焊球用途，不再只归因于同时通信。 |
| l19 | 已解决 | 明确「硅元素含在二氧化硅里」；C04 正文也已登记沙子事实。 |
| l42 | 已解决 | 中英均为中心间距；英文 struggles 与中文「很难」强度一致。 |
| l44 | 已解决 | 只说电子显微镜图像灰、像老照片，不再把灰度图当实物真实颜色。 |
| l53 | 已解决 | 英文已限定 “No mechanical parts move”，不再与电子重分布冲突。 |
| l67 | 已解决 | 改为「栅极加够正电压」，不再泛指任意「加电」。 |
| l74 | 已解决 | 中文补齐并非每个开关每拍翻转；时钟拍数不再等同于全部晶体管翻转数。 |
| l75 | 已解决 | 改为点击信号「传到了这儿／make it … here」，方向与 l74 一致。 |
| l77 | 已解决 | 只保留厚度换算及可制造性，删除逐原子层制造推论。 |
| l78 | 已解决 | 删除「每个都是这么一层一层摞出来」，改为准确接入电路。 |
| l84 | 已解决 | 删除长度混用；面积、每管地盘与指甲盖结论均复算成立。 |
| 全片 | 已解决 | C01 引文已换成 Tom's Hardware 的实际原句 “boasts”。 |

上一轮本角色没有「不采纳」项需要另判。

## 最重要的 3 条

1. l43 将「所有颜色」收窄为「进芯片后的材料颜色」，避免把实景和信号特效也说成材料伪彩。
2. l04 的芯片定义补进 C01 的 claim 正文，做到登记内容覆盖句子事实。
3. l23 加入 C19 的 lines；这只是台账完整性修补，不是讲稿事实错误。

## 做得好的、别改掉的

- 190 亿、50 nm、6 nm、4.74 GHz、44 层及一千七百万倍都保留了「谁做到、什么单位、什么示例」的边界。
- 「不是机械碰撞」「传播也需要时间」「不是绝对不漏」「不是每个开关每拍翻转」等限制语中英齐全，建议保留。
- 上一轮涉及信号方向、面积口径、电子显微镜灰度和制造方式的修改均准确，没有为简化而重新说过头。

## 其他

无。
