# 事实核查（script 第 3 轮）

| 句号 | 语言 | 级别 | 问题 | 建议改法 |
|---|---|---|---|---|
| l70 | zh | 必改 | 「栅极……变成竖起的鳍」主体错误：竖起成鳍的是半导体沟道，栅极改为三面围住鳍；英文以 design 为主语，没有此错。[Semiconductor Engineering](https://semiengineering.com/how-to-get-the-most-out-of-gate-all-around-designs/) 与 [IRDS 2022 §4.2.7](https://irds.ieee.org/images/files/pdf/2022/2022IRDS_MM.pdf) 均明确 FinFET 是栅极三面控制沟道、GAA 是各面控制。 | [林] 所以器件从平面结构，变成竖起的鳍式沟道，再变成栅极四面全包。英文保留原文。 |
| l59 | 双语 | 建议 | 「电流却不会／current can't flow」把栅极漏电说成绝对零。绝缘层确实挡住常规导电，但先进 MOS 的薄栅介质仍可能有量子隧穿漏电；[IEEE 对 gate leakage 的定义](https://technav.ieee.org/topic/gate-leakage/)就是经过栅绝缘层的不期望电流。此处说「极小」即可，不影响后文反型通道机制。 | zh：[林] 栅极和硅片间，隔着一层极薄的绝缘层。电场能透过去；栅极漏进硅的电流，正常工作时也极小。<br>en：[Lin] A very thin insulator separates the gate from the silicon. The field acts through it; any gate leakage into the silicon is normally tiny. |
| l19 | 双语 | 建议 | 「沙子的主要成分／the main ingredient in sand」略呈全称；sand 是粒径类别，也有碳酸盐砂等，并非所有沙都以二氧化硅为主。改成「常见沙子／most sand」即可，硅是二氧化硅的组成元素这一核心说法正确。 | zh：[林] 对，这片薄硅才是真正的芯片。硅元素，就含在常见沙子的主要成分——二氧化硅里。<br>en：[Lin] Right. This thin slice of silicon is the real chip. Silicon is part of silicon dioxide, the main ingredient in most sand. |
| l04 | 双语 | 记录 | R：已解决。上一轮指出 C01 未登记「芯片是用大量晶体管工作的薄片」；现 C01 的 claim 已补入该定义，l04 也在 lines 中。 | 保留现文与登记。 |
| l23 | 双语 | 记录 | R：已解决。上一轮指出 l23 未进入任何 claim；现 C19 已收 l23，城市类比与 CPU 提问作为故事内容登记合理。 | 保留现文与登记。 |
| l43 | 双语 | 记录 | R：已解决。上一轮指出「这一路所有颜色」会误包芯片外景物和信号特效；现中英均限定为「进芯片以后这些材料的颜色／material colors inside the chip」，范围准确。 | 保留现文。 |
| 全片 | 双语 | 记录 | 存疑但不影响台词结论：C18 用 A17 Pro die 面积 103.8–114 mm²；dossier F02 却写同来源实测尺寸 8.0×12.3 mm（98.4 mm²），且 [TechInsights 公开页](https://www.techinsights.com/blog/apple-apl1v02-a17-pro-processor-tsmc-3-nm-finfet-process-digital-floorplan-analysis)未列这些数值。按 98.4 mm² 复算仍为约 1.73 个北京、平均边长约 1.22 m，「一米多／差不多两个北京」仍成立。 | 台词不改；C18 补清实测报告编号、原始尺寸及 103.8–114 mm² 区间的各自来源，消除与 F02 的口径差异。 |
| 全片 | 双语 | 记录 | 数字核查证据：已逐条核对 C01–C19（编号无 C16）的主体、原话、单位和口径。[Tom's Hardware](https://www.tomshardware.com/news/apple-a17-pro-3nm-iphone-15-pro) 报道的是 2023 年 A17 Pro 的 190 亿个晶体管；按 UN WPP 2024 的 2026 年世界人口 83.00678396 亿，人均 2.289 个。[nano.gov](https://www.nano.gov/about-nanotechnology/just-how-small-is-nano) 原文为头发约 80,000–100,000 nm；[Intel](https://www.intel.com/content/www/us/en/newsroom/news/corporate/intel-foundry-details-process-milestones-future-innovation-at-vlsi-symposium.html) 原文为 contacted poly pitch 50 nm，故 1,600–2,000 个周期正确。1.7 m÷100 nm＝1700 万，log10＝7.230；按 [NIST 晶格常数](https://physics.nist.gov/cgi-bin/cuu/Value?asil) 6÷(0.5431020511÷4)＝44.19 层；C18 所给面积区间复算为北京面积的 1.828–2.008 倍、平均地盘边长 1.257–1.317 m。未发现把相关说成因果或把路线图值说成某产品实测值。 | 保留这些数字、限定语与计算口径。 |
| 全片 | 双语 | 记录 | 概念、翻译与登记核查证据：MOS 反型通道与 [Toshiba 原文](https://toshiba.semicon-storage.com/us/semiconductor/knowledge/e-learning/discrete/chap3/chap3-7.html)一致；可见光范围与 [NASA](https://science.nasa.gov/ems/09_visiblelight/) 的约数差异属于常见取整，l42 始终比较中心间距而非线宽；弹珠类比保留「近似、非碰撞、非瞬时」边界。91 句均进入 claims 的 lines，除上述边界问题外未发现未登记的新事实。逐句比对中英，除 l70 中文主体错误外，数量、单位、限定语和因果方向一致；本稿没有直接引语翻译，工艺名、反型通道等转述忠实原意。 | 除表内建议外无需改动。 |

## 最重要的 3 条

1. **l70 必改**：中文说「栅极变成鳍」是器件结构主体错误；应改成鳍式沟道，英文不动。
2. **l59 建议收紧**：栅极电流不是绝对零，改成正常工作时的栅极漏电极小，中英同步。
3. **C18 溯源存疑**：die 面积输入与 F02 不一致且公开原页未列数值；结论仍成立，但应补齐实测出处和口径。

## 做得好的、别改掉的

1. l42 明确比较「相邻导线中心间距」与可见光波长，没有偷换成线宽，也保留「很难」而非绝对不可见。
2. l46、l77、l81、l84 的示例范围、单位和换算都清楚；190 亿没有冒充 2026 年新款芯片官方数字。
3. l38 主动说明弹珠类比不是电子碰撞且传播非瞬时，l69 保留关态仍可能漏电，l43 已把后加颜色限定到芯片内材料；这些边界应保留。
