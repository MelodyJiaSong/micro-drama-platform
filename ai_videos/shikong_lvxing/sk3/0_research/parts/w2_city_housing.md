---
worker_id: researcher-w2-city
stage: 0
role: researcher
angle: city-layout-and-housing
status: complete
blockers: []
confidence: medium
---

# W2 · 城市地图与街区 + 住（sk3 伦敦 · 1666-09-01 · 大火前一夜）

> 本文件是 `sk3/0_research/dossier.md` **第 2 节（城市地图与街区）与第 5 节（住）**的底稿，由 parent 合并。
> 末尾另有 **§2b 给 Blender 整城白模的建模要点**，直接服务两个签名镜（片头航拍长镜 + 20–30 s 一镜到底穿街长镜）。
>
> **`verified_by` 取值**：`ai_read` ＝ 本 worker 本次 **WebFetch 实际打开了含该 `quote` 的页面**，`quote` 逐字来自抓取结果；
> `ai_draft` ＝ 只来自搜索结果摘要、未打开原文页，**不得直接进 prompt**，须人眼复核后升级。
> 按 stage-0 playbook，`ai_read` 进 prompt 前仍应由用户抽查原文页升为 `human`。
>
> **统计**：§2 城市 **26 条**（ai_read 24 / ai_draft 2）· §5 住 **20 条**（ai_read 16 / ai_draft 4）。
> **合计 46 条，其中 ai_read 40 条**（目标 ≥ 14 ✓）。tag 分布：✅ 40 / ⚠️ 6 / ❌ 0。
> **编号说明**：`city.016 / 017 / 028 / 029` 四个号空置——Cheapside（016/017）、Fleet Ditch（028）、
> 用水（029）在成稿时归并进了 §5，分别落为 `housing.010 / 020 / 019`。**空号是有意留白，不是漏条。**
>
> **一手底本（T0）**：
> - John Stow, *A Survey of London* (1603)，British History Online 全文——城墙 / 城门 / 桥 / 各 ward
> - *Statutes of the Realm* vol 5，19 Car. II c. 3《An Act for rebuilding the Citty of London》(1667)——**火后法条反证火前形态**
> - John Evelyn, *Diary*（Project Gutenberg 全文）——1666-08-27 圣保罗勘查 · 1666-09-02/03/04/07 火中与废墟
> - Samuel Pepys, *Diary*（Wikisource）——1666-09-02 / 09-05
> - John Evelyn, *Fumifugium* (1661) 引文（经 T2 转录）
>
> **T1**：Map of Early Modern London (MoEML, U. Victoria)、IHR *People in Place* 项目、Grub Street Project（Stow / Strype / Hatton 转录）、London Museum。
> **T3 交叉核对**：Wikipedia（仅用于核对数字，凡只见于此的一律标 ⚠️）。

---

## 0. 自查对账（rule 4i ③）

### ① 三处「看起来像冲突、其实不是」（先问是不是同一件事）

| # | 表面冲突 | 裁定 | 依据 |
|---|---|---|---|
| 1 | Stow 记伦敦桥拱「in bredth 30. foote」，而现代研究说桥「20 to 24 feet wide」 | **伪冲突，两个都对**。Stow 的 30 ft 是**沿河方向的拱跨（净开口）**，20 ft 是**墩厚**；20–24 ft 是**桥面横向总宽（含两侧房屋占地）**。建模时是两个不同方向的尺寸，不要混用 | `city.006` / `city.007` |
| 2 | Stow 记城墙「8. foote thicke ... 12. foot in height」，现代考古说「6 to 9 feet wide and about 20 feet high」 | **不是同一时点**。Stow 转述的是**罗马初建**规格；考古的 20 ft 高含**中世纪历次加高**。1666 年看到的是加高后的墙，按 **≈6 m 高**建 | `city.001` |
| 3 | 「布丁巷离老天鹅码头很近」（本站任务书的假设） | **任务书方位有误**。**Old Swan 在桥的上游（西侧）**、Swan Lane 底，布丁巷在桥的**下游（东侧）**、Fish Street Hill 以东。两者隔着整座桥头，**不相邻**。与布丁巷真正贴身的是 New Fish Street／Fish Street Hill（西）、Botolph Lane（东）、Little Eastcheap（北）、Thames Street（南） | `city.011` / `city.015`；Pepys 09-02 写火「as far as the Old Swan」是火**向西**烧过去的意思 |

### ② 抽查清单（8 条最吃重的 `ai_read`，请点开 `source_url` 对 `quote`）

| # | fact_id | 断言 | url |
|---|---|---|---|
| 1 | `london1666.city.008` | 旧伦敦桥北端 1633 年烧掉的一段**到 1666 年仍未重建**，只钉着木板挡人落水 | https://stmagnusmartyr.the-axis.com/old-london-bridge/ |
| 2 | `london1666.city.018` | 旧圣保罗尖顶 1561 年雷击焚毁后**从未重建**，1666 年只剩方塔，Hooke 量 204 ft | https://en.wikipedia.org/wiki/Old_St_Paul's_Cathedral |
| 3 | `london1666.city.020` | 1666-08-27 Evelyn / Wren 现场勘查，决定拆塔重做并造 cupola；六天后大火，脚手架助燃 | https://www.gutenberg.org/files/42081/42081-h/42081-h.htm |
| 4 | `london1666.city.011` | 布丁巷南起泰晤士街北至 Little Eastcheap；名字来自屠夫把猪下水顺坡冲到河边粪船 | https://mapoflondon.uvic.ca/PUDD1.htm |
| 5 | `london1666.city.024` | 市政厅 1666 在无焰状态下整体通红发光数小时（Vincent 目击） | https://www.grubstreetproject.net/places/2198/ |
| 6 | `london1666.housing.007` | 1667 法禁 jetty 的原文：`noe Bulks Jettyes Windowes Posts Seates ... beyond the auntient foundation` | https://www.british-history.ac.uk/statutes-realm/vol5/pp603-612 |
| 7 | `london1666.housing.009` | 1667 法要拓宽**所有窄于 14 ft 的通道** → 火前大量小巷 < 14 ft | 同上 |
| 8 | `london1666.housing.013` | 1416 Henry Barton 令只在 **Hallowtide→Candlemas 的冬夜**挂灯 → **9 月 1 日无任何公共照明** | https://www.simoncornwell.com/lighting/timeline/index.htm |

### ③ 未查到确切数值、**禁止编**的清单（⚠️）

| 项 | 状态 |
|---|---|
| Cheapside 的**宽度**（英尺） | **未查到一手数值**。Hatton 1708 的「450 Yds」是**长度**不是宽度；「62 feet wide」只见于搜索摘要转述、未核到原始出处。只能写「城内最宽的街」，**不要写具体英尺数** |
| 布丁巷的**宽度** | **未查到确切数值**。只知它是 Little Eastcheap 与 Thames Street 之间的一条 lane（次级小街）。可用 1667 法「< 14 ft 要拓宽」作**上界推断**（⚠️ 推断，非史料） |
| Thames Street 的**宽度** | **未查到**。只有长度（约 1800 yds）与「much pestered with Carts」的拥堵描述 |
| 旧伦敦桥 1666 年**桥上房屋的确切栋数** | **未查到**。只知 14 世纪末峰值 140 栋、17 世纪多为 4–5 层、1633 年北端烧掉 42 栋 |
| 1666 年城内房屋**总栋数** | 只有火**后**统计（烧毁约 13,200 栋）。火前总数未核 |
| 皇家交易所的**平面尺寸** | 未查到。只有「四层」「中央敞院」「楼上约 100–109 间铺」 |
| 街面铺装的**断面构造** | 「中央 kennel + 两侧 chain stones + 夯土/砾石/卵石」只见于 T2/T3 转述（`housing.011`，ai_draft），未核到一手 |

---

## §2 城市地图与街区（`london1666.city.NNN`）

### 2a 城墙与城门

```yaml
- fact_id: london1666.city.001
  claim: 1666 年伦敦城仍被罗马-中世纪石墙环绕；Stow 实测周长 643 perch ＝ 3536.5 码 ＝ 10608 英尺（两英里又 608 英尺），围出约 330 英亩（1.34 km²）。罗马初建规格 8 ft 厚 × 12 ft 高（Stow），经中世纪加高后考古复原值约 6–9 ft 厚 × 20 ft 高——1666 年看到的是加高后的墙
  tag: ✅
  source: John Stow《A Survey of London》(1603)「The wall about the Citie of London」＋ 现代考古综述（London Wall）
  quote: >-
    "the totall of these perches amounteth to 643. euery perch consisting of 5. yeards and a halfe, which do yeeld 3536. yardes and a halfe, containing 10608. foote, which make vp two English miles and more by 608. foote."；"This Wall they builded 8. foote thicke in breadth, and 12. foot in height"；"The wall is high and great, wel towred on the Northside, with due distances betweene the towres."；（考古）"The wall was 3.2 kilometres (2 miles) long, enclosed an area of about 330 acres (130 ha), and was 6 to 9 feet (2 to 3 m) wide and about 20 feet (6 m) high."
  source_url:
    - https://www.british-history.ac.uk/no-series/survey-of-london-stow/1603/pp5-10
    - https://en.wikipedia.org/wiki/London_Wall
  tier: T0+T3
  verified_by: ai_read
  used_in: []
  prompt_string: "一圈灰石与砖石混砌的旧城墙环住整座城，墙高约六米、顶上有垛口与间隔均匀的方塔，北侧一段还带宽阔的旧护城壕"
  negative: "明清青砖垛口、方正棋盘格城、中式城楼、混凝土墙、笔直的现代城墙、崭新无风化的石面"
  note: 两个厚度/高度数字不是冲突，是不同时点（见 §0 ①-2）。建模用 ≈6 m 高。

- fact_id: london1666.city.002
  claim: 城墙上的门古时只有四座主门（Aldgate 东 / Aldersgate 北 / Ludgate 西 / Bridgegate 南，即桥门），后来为方便通行加开若干门与便门；1666 年墙上常说的七门是 Ludgate / Newgate / Aldersgate / Cripplegate / Moorgate / Bishopsgate / Aldgate，桥门（Bridgegate）算在旧四主门内，另有塔边便门（Postern，1440 年塌后未重建）
  tag: ✅
  source: Stow《Survey of London》(1603)「Gates in the wall of this Citie」
  quote: >-
    "Gates in the wall of this Citie of olde time, were foure: to wit, Aeldgate for the east, Aldersgate for the North, Ludgate for the West, and the Bridgegate ouer the riuer of Thames for the South, but of later times for the ease of Citizens and Passengers, diuers other gates and posterns haue beene made"；（塔边便门）"the same fell downe in the yeare 1440. the xviij. of Henrie the sixt, and was neuer since by the Citizens reedified"
  source_url: https://www.british-history.ac.uk/no-series/survey-of-london-stow/1603/pp27-44
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城墙上每隔一段开一座石砌拱门，门洞上方是带小窗的门楼房间，门前有桥跨过旧城壕"
  negative: "中式牌楼、瓮城、双阙、城门上的琉璃瓦、凯旋门式装饰、现代闸口"

- fact_id: london1666.city.003
  claim: Ludgate（西门，通向 Fleet Street 与 Westminster）1586 年整座拆掉重建，东面立卢德王等雕像、西面立伊丽莎白一世像；门内兼作负债人监狱（自由狱），狱内有一条 38.5 ft 长的放风走道、墙内净宽 29.5 ft
  tag: ✅
  source: Stow《Survey of London》(1603)「Gates in the wall of this Citie」
  quote: >-
    "the same gate being sore decayed, was cleane taken downe... and the same yere the whole gate was newly and beautifully builded, with the Images of Lud, and others, as afore, on the East side, and the picture of her Maiestie, Queene Elizabeth on the West side"；"a large walking place by ground of 38. foot, & halfe in length, besides the thicknesse of the walles... the bredth within the walles is 29. foote and a halfe"
  source_url: https://www.british-history.ac.uk/no-series/survey-of-london-stow/1603/pp27-44
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "Ludgate 是一座相对新的石门楼，门洞两侧的壁龛里立着石雕人像，门楼上层有带铁栅小窗的房间"
  negative: "中世纪残破土门、木栅栏门、门上挂灯笼、现代路牌"

- fact_id: london1666.city.004
  claim: Newgate 是城门也是全城主监狱（1422 年用 Richard Whittington 的遗产重建）；Cripplegate 1491 年重修、同样带监狱功能；Moorgate 1472 年由市长 William Hampton 重建，门外就是沼地 Moorfields（1666 年火后难民就是涌到那里）
  tag: ✅
  source: Stow《Survey of London》(1603)「Gates in the wall of this Citie」；Pepys 1666-09-05
  quote: >-
    "licence was granted to Iohn Couentre, Ienken Carpenter, and William Groue, executors to Richard whittington, to reedifie the Gaile of Newgate, which they did with his goods"；"This Posterne was reedified by William Hampton Fishmonger, Mayor, in the yeare 1472"；（Pepys 09-05）"Walked into Moorefields... find that full of people"
  source_url:
    - https://www.british-history.ac.uk/no-series/survey-of-london-stow/1603/pp27-44
    - https://en.wikisource.org/wiki/Diary_of_Samuel_Pepys/1666/September
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "Newgate 是一座沉重的石门楼，门洞上方几层都是带铁栅的窗，能听见里面囚犯的声音；Moorgate 外是一片平坦的沼草地"
  negative: "现代监狱铁门、探照灯、砖砌牢房、Moorfields 建成公园草坪"

- fact_id: london1666.city.005
  claim: Aldersgate 门本体没有整体重建记录，但历年不断往上加盖木构：南侧（城内一侧）加了一整片木构架、含若干大房间与卧房，东侧又加一栋大木屋、里面铺石地面、还有一口砌石深井——这是「中世纪城门被住人一点点吃掉」的实例
  tag: ✅
  source: Stow《Survey of London》(1603)「Gates in the wall of this Citie」
  quote: >-
    "hath at sundry times beene increased with buildinges, namely on the south or innerside, a great frame of timber hath beene added and set vp, contayning diuers large roomes, and lodgings: also on the East side, is the addition of one great building of Timber, with one large floore paued with stone, or tile, and a Well therein curbed with stone, of a great depth, and rising into the said roome, two stories high from the ground"
  source_url: https://www.british-history.ac.uk/no-series/survey-of-london-stow/1603/pp27-44
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城门两侧和上方被后加的黑木构架房子包住，木屋挂在石门楼上像寄生的巢，门洞旁一堵石墙里嵌着井口"
  negative: "干净规整的纯石门楼、对称古典立面、门楼被清理成纪念碑"
```

### 2b 泰晤士河与旧伦敦桥

```yaml
- fact_id: london1666.city.006
  claim: 旧伦敦桥 1176 年动工、1209 年建成，历时 33 年；Stow 记 20 座方石拱、拱高 60 ft、拱跨 30 ft、墩厚 20 ft；现代研究记全长约 926 ft（282 m）、19 座墩、墩下打木桩（starling 护墩堆）
  tag: ✅
  source: Stow《Survey of London》(1603)「Bridges of this Citie」＋ 现代综述
  quote: >-
    "20. Arches made of squared stone, of height 60. foote, and in bredth 30. foote distant one from another 20. foote"；"this worke to wit, the Arches, Chaple & stone bridge ouer the riuer of Thames at London, hauing beene 33. yeares in building was in the yeare 1209. finished"；（现代）"The bridge was about 926 feet (282 metres) long, and had nineteen piers, supported by timber piles."
  source_url:
    - https://www.british-history.ac.uk/no-series/survey-of-london-stow/1603/pp21-27
    - https://en.wikipedia.org/wiki/London_Bridge
  tier: T0+T3
  verified_by: ai_read
  used_in: []
  prompt_string: "一座约二百八十米长的石拱桥横过泰晤士河，十九座粗壮石墩下堆着船形的木桩护堆，桥孔窄、水从孔间急泻而下形成白色落差"
  negative: "单跨钢桥、现代混凝土桥墩、平缓宽阔的桥孔、桥下水面平静、威尼斯式石栏桥"
  note: 「拱跨 30 ft」与「桥宽 20–24 ft」是两个方向的尺寸，不是冲突（§0 ①-1）。

- fact_id: london1666.city.007
  claim: 桥面连同两侧房屋的总宽只有 20–24 ft（6.1–7.3 m）；桥上房屋 14 世纪末峰值 140 栋，17 世纪时几乎全是四到五层（含阁楼算一层），三栋有六层；大约每隔一栋就有一道「cross building」从一层以上横跨车道把两侧房子连起来——所以桥上是一条**上有顶盖、两侧夹墙**的隧道式街
  tag: ✅
  source: 现代综述（London Bridge），依据 17 世纪逐栋测绘记录
  quote: >-
    "The bridge, including the part occupied by houses, was from 20 to 24 feet (6.1 to 7.3 metres) wide."；"In the seventeenth century, when there are detailed descriptions of them, almost all had four or five storeys (counting the garrets as a storey); three houses had six storeys."；"Approximately every other house shared in a 'cross building' above the roadway, linking the houses either side and extending from the first floor upwards."
  source_url: https://en.wikipedia.org/wiki/London_Bridge
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "桥上是一条被房屋夹死的窄街，两侧四到五层的黑木构架房子直接骑在桥面上，每隔一栋就有一道横跨街道的连廊把两边连住，走在下面像穿过一条时明时暗的木隧道，只在连廊之间的空档露出一线天与河"
  negative: "开阔的桥面、能看见两侧河景的栏杆、单层店铺、砖石排屋、桥上有车道分隔线"
  note: ⚠️「车道净宽」未查到确切数值。总宽 20–24 ft 减去两侧房屋进深，推断车道约 12 ft（**推断，非史料**）。

- fact_id: london1666.city.008
  claim: 【本站最关键的建模事实】1633 年 2 月的大火烧掉了桥**北端**（城这一侧）的全部房屋，从 St Magnus 教堂一直烧到第一处空地，42 栋；这一段到 1666 年**仍未重建**，只在两侧钉了松木板防止行人落水。正是这道 33 年的空档在 1666 年充当防火带，挡住火烧向南岸 Southwark
  tag: ✅
  source: St Magnus the Martyr 教区史（引 Richard Blome）＋ 1633 年火灾同时代记录（thames.me.uk 转录）
  quote: >-
    "A fire in 1633 had destroyed the houses on the northern part of the bridge. Richard Bloome recorded that 'this North end of the Bridge lay unbuilt for many years, only deal boards were set up on both sides, to prevent people's falling into the Thames...'"；（1633 火）"burnt downe all the houses on both sides of the way, from S. Magnes Church to the first open place."；（1666）"The keyed wooden structure known as Nonsuch House... the drawbridge, and the remaining houses towards Southwark were not touched by the fire."
  source_url:
    - https://stmagnusmartyr.the-axis.com/old-london-bridge/
    - https://thames.me.uk/s00049b.htm
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "桥的北段有一大截是空的：房子都没了，只剩光秃的石桥面，两侧临时钉着一排粗糙的松木挡板，板缝里能直接看见下面的河水；空档往南才重新出现密集的桥上房屋"
  negative: "桥上房屋连绵不断毫无缺口、空档处有新房子、整洁的石栏杆、空档被围成观景平台"
  note: >-
    **这一条决定了桥要建成什么样**——不要把桥建成「首尾连贯的房屋长廊」。正确形态是：北端一段光桥面＋木挡板 → 中段密集房屋 → Nonsuch House → 吊桥段 → 南端石门 → Southwark。

- fact_id: london1666.city.009
  claim: 吊桥自 1470 年代起已不再开启；原来的吊桥塔在 1577–1579 年被 Nonsuch House 取代——一对预制木构豪宅，跨在桥面上；南端的 Great Stone Gate（石门）1470 年代最后一次重建，后来接手了**在门顶长杆上示众叛贼头颅**的职能。这三样在 1666 年都在桥的南半段，**都没被烧**
  tag: ✅
  source: 现代综述（London Bridge）＋ thames.me.uk
  quote: >-
    "The drawbridge ceased to be opened in the 1470s and in 1577–1579 the tower was replaced by Nonsuch House—a pair of magnificent houses."；"The stone gate was last rebuilt in the 1470s, and later took over the function of displaying the heads of traitors."
  source_url:
    - https://en.wikipedia.org/wiki/London_Bridge
    - https://thames.me.uk/s00049b.htm
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "桥中段跨着一栋描金彩绘的木构大宅，四角带洋葱顶小塔；再往南是一座厚重的石门楼，门楼顶上一排长铁杆，杆头插着风干发黑的人头"
  negative: "头颅新鲜血腥、头颅插在城墙上、Nonsuch House 是石砌、木宅素面无彩绘"

- fact_id: london1666.city.010
  claim: 桥北端最靠城这一侧的两孔底下装着 Peter Morice（Morris）1578–1582 年建的水车，靠潮汐推动、驱动水泵把泰晤士河水压进城里的木管网（London Bridge Waterworks）；这套水车与机械在 1666 年大火中被毁
  tag: ✅
  source: 现代综述（London Bridge / Peter Morice）
  quote: >-
    "In 1578–1582 a Dutchman, Peter Morris, created a waterworks at the north end of the bridge. Water wheels under the two northernmost arches drove pumps."；"Morice's waterwheels and associated machinery were destroyed in the Great Fire of London of 1666."
  source_url: https://en.wikipedia.org/wiki/London_Bridge
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "桥北端最靠城的两个桥孔里各装着一具巨大的木水车，被急流推着不停转动，旁边木塔里传出水泵的往复撞击声，水花与木架结构在桥孔下形成一团湿黑的机械"
  negative: "金属水车、现代水轮机、水车安静无声、水车装在桥中段"
```

### 2c 布丁巷街区（火起点方圆二百米）

```yaml
- fact_id: london1666.city.011
  claim: >-
    布丁巷（Pudding Lane）南起 Thames Street、北至 Little Eastcheap，西邻 New Fish Street（即 Fish Street Hill）、东邻 Botolph Lane，中间只有 St George's Lane 一条横街。它是次级小街（lane），不是主干道。Stow 记它原名 Rother Lane / Red Rose Lane，改叫「布丁巷」是因为东市（Eastcheap）的屠夫在这里设烫猪房，把猪下水和牲畜秽物顺着这条坡冲到河边的粪船上。Stow 时代主要住着编筐匠、旋木匠和屠夫
  tag: ✅
  source: MoEML「Pudding Lane」引 Stow《Survey of London》
  quote: >-
    "Then haue yee one other lane called Rother Lane, or Red Rose Lane, of such a signe there, now commonly called Pudding Lane, because the Butchers of Eastcheape haue their skalding House for Hogges there, and their puddinges [entrails] with other filth of Beastes, are voided downe that way to theyr dung boates on the Thames."；"Pudding Lane ran south from Little Eastcheap down to Thames Street, with New Fish Street framing it on the west and Botolph Lane on the east."
  source_url: https://mapoflondon.uvic.ca/PUDD1.htm
  tier: T0+T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一条南低北高的窄坡巷，两侧是四五层的黑木构架房屋，上层层层外挑几乎在头顶合拢；地面中央一条明沟，沟里流着屠宰废水与猪血，腥臭；沿街有屠夫的烫猪房、编筐匠和旋木匠的作坊，门口堆着柳条和木屑"
  negative: "宽阔笔直的街、砖石排屋、干净的石板地、鲜花窗台、旅游街区、路牌、Pudding Lane 是平地"
  note: ⚠️ 巷宽未查到确切数值。方位上它**不挨着 Old Swan**（后者在桥西侧），见 §0 ①-3。

- fact_id: london1666.city.012
  claim: 火起于 1666 年 9 月 2 日午夜刚过，Thomas Farriner（国王的面包师）在布丁巷东侧的面包房。后来的纪念碑（The Monument，1671–1677）高 202 ft，立在 Monument Street 与 Fish Street Hill 交口、St Margaret New Fish Street 教堂原址（**大火烧毁的第一座教堂**），碑址**正好在起火点以西 202 ft**——这给了布丁巷面包房一个精确的测绘锚点
  tag: ✅
  source: Monument to the Great Fire of London（现代综述，Wren/Hooke 原始设计意图）＋ MoEML
  quote: >-
    "202 feet (61.6 m) in height and 202 feet west of the spot in Pudding Lane where the Great Fire started on 2 September 1666."；"it stands at the junction of Monument Street and Fish Street Hill"；"it was built on the site of St Margaret, New Fish Street"，"the first church to be destroyed by the Great Fire"；（MoEML）"The Great Fire began on September 2, 1666, around 2 a.m. in the house of Thomas Farriner, the King's baker"
  source_url:
    - https://en.wikipedia.org/wiki/Monument_to_the_Great_Fire_of_London
    - https://mapoflondon.uvic.ca/PUDD1.htm
  tier: T1+T3
  verified_by: ai_read
  used_in: []
  prompt_string: "巷子东侧一栋不起眼的四层木构架房子，底层是面包铺：低矮的门、砖砌烤炉的烟囱、门口堆着柴捆，二楼以上住人，窗户小而歪斜"
  negative: "面包店有玻璃橱窗、招牌写现代字体、门口有纪念牌、店面宽敞明亮、有排队人群"
  note: >-
    **建模用法**：把 Monument 现址当已知坐标，向东量 202 ft（61.6 m）即 Farriner 面包铺；向西下坡即 Fish Street Hill。这是全片最重要的一个位置关系。

- fact_id: london1666.city.013
  claim: St Magnus the Martyr 教堂立在桥的北端桥头、Lower Thames Street 南侧；**桥上的车道直接从它的西门前经过**——七百年间所有从桥进出城的人都贴着它的门走。它的教区小得出奇，只沿桥头两侧各延伸 110 码，包含 Fish Wharf。它距 Farriner 的面包铺约 300 码，是大火最早烧到的建筑之一
  tag: ✅
  source: St Magnus 教区史与现代综述
  quote: >-
    "The northern end of the bridge aligned with Fish Street Hill, so the roadway went directly past the west door of St Magnus the Martyr."；"it extended for 110 yards either side of the bridgehead and included Fish Wharf, where fishmongers had their riverside shops."；"St Magnus-the-Martyr used to stand at the City end of it, about 300 yards away from Thomas Farriner's bakery in Pudding Lane"
  source_url:
    - https://en.wikipedia.org/wiki/St_Magnus_the_Martyr
    - https://www.stmagnusmartyr.org.uk/the-history-of-the-church/great-fire-of-london/
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "刚下桥就是一座中世纪石砌教堂，方形石塔，西门正对着桥面下来的车道，门前人流车马紧贴墙根挤过；教堂南边就是鱼码头，鱼腥味和喧闹声一起涌上来"
  negative: "Wren 的白色石塔与尖顶（那是火后 1671 以后的）、教堂前有开阔广场、哥特大玫瑰窗、教堂独立于街道"
  note: ⚠️ **本条只来自搜索摘要，未打开原文页，进 prompt 前须复核**。尤其：1666 年的 St Magnus 是**中世纪教堂**，绝不能画成今天那座 Wren 白塔。

- fact_id: london1666.city.014
  claim: >-
    Thames Street 是当时伦敦最长的街，东起塔壕、西至 St Andrew's Hill / Puddle Dock，几乎横贯整个墙内城区，穿过七个 ward（Tower Street / Billingsgate / Bridge Within / Dowgate / Vintry / Queenhithe / Castle Baynard）；沿着罗马时代的河岸路走。Strype 记它「长一英里以上」，Hatton 记 1800 码；南侧靠河一面全是染坊、酿酒坊、木料场和一排排码头（key / wharf），因装卸货物而「被车挤得水泄不通」
  tag: ✅
  source: MoEML「Thames Street」；Grub Street Project 转录 Hatton (1708) / Strype (1720) / W. Stow (1722)
  quote: >-
    "was the longest street in early modern London, running east-west from the ditch around the Tower of London in the east to St. Andrew's Hill and Puddle Wharf in the west, almost the complete span of the city within the walls."；"Archaeological finds suggest that it followed an old Roman road beside the river"；（Hatton）"a most extraordinary spacious str. in London... for above a mile betn the Tower dock E. and Puddle dock W. L. 1800 yds"；（Strype）"It is a Street, especially Eastward, of a very good Trade, and inhabited by great Dealers; besides the Diers, Brewers, Woodmongers, and Timber Yards, on the South side, next the Thames."；"by Reason thereof, and of the several Keys and Wharfs, it is much pestered with Carts, for the lading and unlading of Goods."
  source_url:
    - https://mapoflondon.uvic.ca/THAM1.htm
    - https://www.grubstreetproject.net/places/4751/
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "沿河的一条长街，被货车、桶、麻包和搬运工塞满；南侧一排排伸进河里的码头与吊车臂，仓库大门敞着；北侧是仓库与商人住宅的高墙，街上终日车轮碾过石面的噪声"
  negative: "空旷安静的滨江步道、现代吊车、集装箱、河堤护栏、观光船"
  note: Hatton/Strype 是火后（1708/1720）的描述，但街线与用途未变，用作**形态**依据可，用作**1666 年建筑外观**依据不可。

- fact_id: london1666.city.015
  claim: Old Swan（老天鹅）码头台阶在桥的**上游（西侧）**、Upper Thames Street 一端的 Swan Lane（旧名 Ebbgate Lane）底，属 Dowgate Ward。乘船的人在这里上岸、步行绕过伦敦桥、再到桥另一侧重新上船，为的是避开「shooting the bridge」——桥墩护堆之间水道又窄又急，穿桥孔像冲激流。旁边就是 Old Swan 酒馆，1666 年归 Michael Mitchell 一家；Pepys 9 月 2 日正是记「Michell 家、一直到 Old Swan 那一带都烧了」
  tag: ✅
  source: A London Inheritance（引 Walter Thornbury）＋ Pepys 1666-09-02
  quote: >-
    "passengers 'coming by boat used to land to walk to the other side of Old London Bridge when the current was swift and narrow between the starlings.'"；"'shooting the bridge' was 'rather like going down the rapids.'"；（Pepys）"Poor Michell's house, as far as the Old Swan, already burned that way"
  source_url:
    - https://alondoninheritance.com/the-thames/old-swan-stairs/
    - https://en.wikisource.org/wiki/Diary_of_Samuel_Pepys/1666/September
  tier: T0+T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一段从水面斜上来的湿滑石阶，阶上挤着刚下船的人，船夫在下面喊价；石阶顶上是一条窄巷口和一家酒馆的招牌"
  negative: "现代码头浮桥、金属扶手、Old Swan 在桥的东侧、宽阔的登船平台"
  note: >-
    **方位纠错**：Old Swan 在桥**西**、布丁巷在桥**东**，两者不相邻（§0 ①-3）。
```

### 2d 旧圣保罗大教堂（航拍最显眼的地标）

```yaml
- fact_id: london1666.city.018
  claim: 【逐条查证】旧圣保罗的中世纪尖顶在 1561 年 6 月 4 日被雷击引燃、砸穿中殿屋顶；伊丽莎白一世捐了 1000 金镑与王室木料、伦敦主教 Grindal 捐 1200 镑修屋顶，**但尖顶从此再未重建**。该尖顶 1312 年记为 520 ft（158 m）高。到 1666 年，教堂顶上只剩一个**削平的方塔残段**，Robert Hooke 量得「将近两百零四英尺」
  tag: ✅
  source: >-
    Old St Paul's Cathedral（现代综述，含 Penrose 1878 发掘与 Hooke 测量）
  quote: >-
    "On 4 June 1561, the spire caught fire and crashed through the nave roof. According to a newsheet published days after the fire, the cause was a lightning strike."；"This steeple was reputedly measured at 520 feet (158 m) high in 1312."；"Queen Elizabeth I contributed £1,000 in gold towards the cost of repairs as well as timber from the royal estate and the Bishop of London Edmund Grindal gave £1200, although the spire was never rebuilt."；Robert Hooke measured "the height of the tower as 'two hundred and four feet very near.'"
  source_url: https://en.wikipedia.org/wiki/Old_St_Paul%27s_Cathedral
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "巨大的哥特式教堂横卧在城西高地上，**塔顶是平的、没有尖顶**——只有一个方形的石塔残段，像被削掉了头，比周围所有屋顶高出一大截却显得钝而沉"
  negative: "【最高优先级负向】高耸的哥特尖塔、Wren 的圆穹顶（那是 1710 年以后）、任何尖锥形塔顶、十字架尖顶、双塔立面"
  note: >-
    **这是全片最容易画错的一处**。1666 年的圣保罗：无尖顶、无圆顶、方塔残段 204 ft。

- fact_id: london1666.city.019
  claim: Inigo Jones 1620 年代起主持修缮，1630 年代给西端加了一道古典科林斯柱廊（portico）：面阔 10 柱、纵深 4 柱，柱高约 45 ft，由查理一世出资；柱廊上方是狮头与卷叶饰的檐壁，原计划立一排雕像，最后只立了詹姆斯一世与查理一世两尊；西立面两侧还有小塔楼。Jones 同时在整座中世纪外墙外面包了一层石灰岩古典外皮
  tag: ✅
  source: >-
    Exploring London「Lost London – Inigo Jones' Grand Portico on Old St Paul's Cathedral」
  quote: >-
    "10 columns across its breadth and four deep" with "these... stood about 45 feet tall."；"was paid for by King James' son, King Charles I."；"topped by a frieze of lions' heads and foliage with plans for a series of statues which some say were to be saints and others kings to be placed along the top (in the end only statues of King Charles I and King James I were ever placed there)."；"The facade also featured turrets at either side."；Jones added "a layer of limestone masonry over the exterior to give the building a more classical look inspired by the temples of ancient Rome."
  source_url: https://exploring-london.com/2015/07/31/lost-london-inigo-jones-grand-portico-on-old-st-pauls-cathedral/
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂西端贴着一道崭新的古典柱廊，十根巨柱一排、纵深四排，柱子高得压人；柱廊顶上只立着两尊国王石像，其余基座空着；柱廊的干净白石与后面发黑的哥特石墙形成刺眼的新旧对比"
  negative: "柱廊是哥特式、柱廊上立满雕像、柱廊与主体同样发黑、没有柱廊的纯哥特西立面"
  note: >-
    **建模要点**：这道柱廊与后面的哥特主体**材质、颜色、年代都不一样**，是「古典外皮包中世纪骨」的怪东西。航拍与地面镜都要画出这个不协调。

- fact_id: london1666.city.020
  claim: 【逐条查证】1666 年 8 月 27 日——大火前六天——Evelyn、Wren、Pratt、May、Thomas Chicheley、Slingsby，连同伦敦主教、圣保罗座堂主任与多名匠师，在教堂现场勘查整体残破状况并逐项写下要做什么、花多少钱。走到塔下时争论要不要只在旧基础上修（Chicheley 与 Pratt 主张修），Evelyn 与 Wren「完全否决」、坚持必须重做基础，并且「我们想把它建成一座高贵的 cupola（穹顶），这种教堂形式在英格兰还不为人知，却优美得惊人」。**为这次勘修搭起的木脚手架在六天后成了助燃物**
  tag: ✅
  source: >-
    John Evelyn《Diary》1666-08-27（Project Gutenberg 全文）；Old St Paul's 现代综述
  quote: >-
    "I went to St. Paul's church, where, with Dr. Wren, Mr. Pratt, Mr. May, Mr. Thomas Chicheley, Mr. Slingsby, the Bishop of London, the Dean of St. Paul's, and several expert workmen, we went about to survey the general decays of that ancient and venerable church..."；"When we came to the steeple, it was deliberated whether it were not well enough to repair it only on its old foundation, with reservation to the four pillars; this Mr. Chicheley and Mr. Pratt were also for, but we totally rejected it, and persisted that it required a new foundation..."；"we had a mind to build it with a noble cupola, a form of church-building not as yet known in England, but of wonderful grace."；（现代）"The fire, aided by the scaffolding, destroyed the roof and much of the stonework"
  source_url:
    - https://www.gutenberg.org/files/42081/42081-h/42081-h.htm
    - https://en.wikipedia.org/wiki/Old_St_Paul%27s_Cathedral
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂外墙从下到上架满粗木脚手架，绑扎的麻绳和跳板层层交错，地面堆着新采的石料、灰桶和工具；施工现场已经停工，木架空着，在暮色里像一副巨大的木笼罩住整座教堂"
  negative: "脚手架是金属管、有安全网、施工照明、脚手架很小只围一角、教堂完好无施工痕迹"
  note: >-
    **这是本片的戏剧核心之一**：勘修木架 8 月 27 日刚立好，9 月 2 日夜把教堂点着。1666-09-01 的夜景里，这副木架必须在画面里。

- fact_id: london1666.city.021
  claim: 旧圣保罗的体量（Penrose 1878 年发掘实测）：主体长 586 ft（179 m，不含 Jones 后加的门廊）、宽 100 ft（30 m）、横厅与交叉部通宽 290 ft（88 m）。它是中世纪欧洲最长的教堂之一，1666 年仍是伦敦天际线上体量最大的单体
  tag: ✅
  source: >-
    Old St Paul's Cathedral（引 Penrose 1878 发掘）
  quote: >-
    "Excavations in 1878 by Francis Penrose showed the enlarged cathedral was 586 feet (179 m) long (excluding the porch later added by Inigo Jones) and 100 feet (30 m) wide (290 feet (88 m) across the transepts and crossing)."
  source_url: https://en.wikipedia.org/wiki/Old_St_Paul%27s_Cathedral
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂长得离谱，从西端走到东端要走上很久，屋脊像一条灰色的山脊压在城西，周围的民房只到它侧墙的三分之一高"
  negative: "教堂尺度与周围房屋接近、教堂被高楼包围、紧凑的方形平面"

- fact_id: london1666.city.022
  claim: >-
    旧圣保罗的**内部不是安静的教堂**：中殿因其长度被叫作「Paul's walk」，是公共通道与市井社交场；东端地窖里包着圣费思（St Faith's）教区堂——1666 年附近 Paternoster Row 的书商印刷商把全部存书紧紧堆进这个地窖避火，结果全部烧光；教堂墓地本身被王室没收后卖给店主，尤以印刷商与书商为多；墓地东北角是 Paul's Cross 露天布道台
  tag: ✅
  source: >-
    Old St Paul's Cathedral 现代综述；Great Fire of London 现代综述
  quote: >-
    "The length earned it the nickname 'Paul's walk'."；"the east end of the cathedral church was lengthened, enclosing the parish church of St Faith, which was now brought within the cathedral."；"Many of these former religious sites in St Paul's Churchyard, having been seized by the crown, were sold as shops and rental properties, especially to printers and booksellers."；"Crowds were drawn to the northeast corner of the Churchyard, St Paul's Cross, where open-air preaching took place."；（大火）crypt "filled with the tightly packed stocks of the printers and booksellers in adjoining Paternoster Row"
  source_url:
    - https://en.wikipedia.org/wiki/Old_St_Paul%27s_Cathedral
    - https://en.wikipedia.org/wiki/Great_Fire_of_London
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂中殿里人来人往像一条室内街道：有人在谈生意、有人在招揽、有人只是抄近路穿过；四周墓地一圈全是书商与印刷铺的小门面，纸张与油墨味压过香火味"
  negative: "教堂内肃静无人、只有信徒祷告、成排长椅、管风琴演奏、墓地空旷整洁"
```

### 2e 皇家交易所 / 市政厅 / 伦敦塔

```yaml
- fact_id: london1666.city.023
  claim: 皇家交易所（Royal Exchange）由 Thomas Gresham 仿他在安特卫普见到的 bourse 出资建造，1571 年 1 月 23 日由伊丽莎白一世正式开幕；四层；中央是一个敞开的内院，四周是由大理石柱撑起的柱廊（piazza），楼上「pawn」层有约 100–109 间小铺；交易所一周开六天，每天两场各一小时的交易时段，以钟楼敲钟为号；1666 年大火中烧毁，目击者 Thomas Vincent 说火在回廊里奔跑的声音「像有一千辆铁战车在石头上碾过」
  tag: ✅
  source: London Museum「A history of the Royal Exchange」
  quote: >-
    "Influential British merchant Thomas Gresham was based at Antwerp's 'bourse', a purpose-built trading venue, in the mid-1500s. He financed a similar gathering place for international merchants back home."；"London's four-storey bourse was officially opened on 23 January 1571 by Queen Elizabeth I."；"109 shops previously crammed into the upper floor"；"The Exchange was open six days a week. There were two one-hour trading sessions per day, which were marked by ringing the bell in the belltower."；"there had been a thousand iron chariots beating upon the stones"
  source_url: https://www.londonmuseum.org.uk/collections/london-stories/history-royal-exchange/
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座四层的方形商业建筑，中央围出一个敞开的石砌内院，四面是柱廊；院里挤满穿黑色与深色外套、戴宽檐帽的商人，分片站着谈生意，声音嗡嗡回荡；楼上一圈小店铺卖各国货品；一侧立着钟楼"
  negative: "维多利亚式八柱门廊（那是 1844 年的第三代）、玻璃顶、现代交易大厅、屏幕、空旷无人"
  note: ⚠️ 平面尺寸未查到。**绝不能用今天那座 1844 年的皇家交易所**——形制完全不同。

- fact_id: london1666.city.024
  claim: 市政厅（Guildhall）1411 年动工由「又老又小的破屋」改建成一座大宅，1440 年建成；大厅约 152–153 ft 长 × 48–49 ft 宽，到屋脊 89 ft 高（另一说到梁约 53 ft）；1501 年在南面加建了门廊与厨房；西端两角的八角形基座上立着两尊约 15 ft 高、黑须的巨人像（Gog & Magog）。1666 年大火中它烧成空壳，但石墙与 1411 年的地窖幸存。Thomas Vincent 的目击：**「市政厅是一幕可怕的奇景——整座建筑在火烧过之后，整整几个小时不带火焰地立在那里，像一块通亮的炭。」**
  tag: ✅
  source: Grub Street Project「Guildhall」（转录 Fabyan、Stow、Vincent）
  quote: >-
    "In this yere also was ye Guylde hall of London begon to be new edyfied, and of an olde and lytell cottage made into a fayre and goodly house"；"153 feet in length, 48 feet in breadth, and about 53 feet in height"／"152 feet long, 49 feet wide, and 89 feet high to the ridge of the roof."；"a stately porch, entering the great hall was erected to the south front"；giants "about 15 feet in height" with "black and bushy beards"；"the sight of Guildhall was a fearful spectacle, which stood the whole body of it together in view for several hours, after the fire had taken it, without flames... in a bright shining coal."
  source_url: https://www.grubstreetproject.net/places/2198/
  tier: T0+T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座石砌的中世纪大厅，南面一道高耸的门廊，厅内空间开阔、彩绘屋架高悬，西端两角立着两尊十五英尺高的黑须巨人木像"
  negative: "文艺复兴对称立面、圆顶、现代市政厅、大厅里有排椅和讲台"
  note: >-
    **Vincent 那句「不带火焰、通体像一块亮炭」是整部片最值钱的一个画面**——如果本片要拍火（本站设定是「大火前一夜」，理论上不拍），至少可以放进旁白或收尾预告。

- fact_id: london1666.city.025
  claim: 伦敦塔在城墙东南角外，1657 年起 White Tower 除礼拜堂外几乎整栋都当火药库用；1666 年大火最近时距塔约 300 码，塔里的守军把 Tower Street 一带的房屋**炸掉**做防火带，才没让火烧到火药；火后才在火药库外另砌了防护墙
  tag: ⚠️
  source: Historic Royal Palaces / White Tower 现代综述（仅搜索摘要）
  quote: >-
    "The Tower of London held vast stocks of gunpowder, and the fire, advancing fast, was only 300 yards away."；"The garrison at the Tower blew up houses in Tower Street to create firebreaks"；"By 1657, almost the entire White Tower, except for the chapel, was used to store gunpowder."
  source_url:
    - https://www.hrp.org.uk/blog/the-great-fire-of-london-and-the-tower/
    - https://en.wikipedia.org/wiki/White_Tower_(Tower_of_London)
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "城东南角外一组灰白色石堡：中央是一座四角带塔楼的方形主塔（White Tower），外面两圈城墙与一道宽阔的护城壕，塔外紧贴着一片民房，几乎挨到壕边"
  negative: "塔周围是开阔草坪（那是后世清出来的）、乌鸦成为景点符号、现代游客通道、护城壕干涸铺草"
  note: ⚠️ **只来自搜索摘要**。但「民房紧贴到塔外壕边」这一点对航拍很重要——1666 年的塔不是今天那种被草坪包围的孤岛。
```

### 2f 天际线 · 大气 · 人口（航拍的画面依据）

```yaml
- fact_id: london1666.city.026
  claim: 大火前，方圆仅一平方英里的伦敦城里有**约 100 座教堂**（墙内 97 座，另加 liberties 10 座，常合称 107 个教区）；其中 86 座毁于大火，Wren 后来重建了 51 座。**这意味着 1666 年的天际线是一片密集的教堂塔与尖顶的森林**——每隔一两条街就有一座
  tag: ✅
  source: List of churches in the City of London（现代综述）；History Today「The Vanished Churches of the City of London」（搜索摘要交叉核对）
  quote: >-
    "Before the Great Fire of London in 1666, the City of London had around 100 churches in an area of only one square mile (2.6 km2)."；"Of the 86 destroyed by the Fire, 51 were rebuilt along with St Paul's Cathedral."；（交叉核对）"At the Great Fire of 1666, there were 97 churches within the walls and ten in the 'Liberties'"
  source_url: https://en.wikipedia.org/wiki/List_of_churches_in_the_City_of_London
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "从高空俯瞰，褐红色的瓦顶海洋里密密麻麻戳出上百座石塔与铅皮尖顶，每隔一两个街区就有一座，像一片长在屋顶上的森林；最西侧一座巨大的、**顶是平的**灰色教堂压过所有其他建筑"
  negative: "天际线上只有几座教堂、高楼、烟囱林立的工业景观、平坦无起伏的屋顶面、任何现代建筑"
  note: >-
    **航拍第一要务**。若干尖顶 + 一座无尖顶的巨物 = 1666 伦敦天际线的签名。

- fact_id: london1666.city.027
  claim: 1666 年墙内城区住约 8 万人，占全伦敦人口的四分之一；整个大都会（含 Westminster、Southwark、城外各区）约 30–40 万人
  tag: ✅
  source: Great Fire of London（现代综述）
  quote: >-
    "home to about 80,000 people, or one quarter of London's inhabitants"；"estimated at 300,000 to 400,000 inhabitants"
  source_url: https://en.wikipedia.org/wiki/Great_Fire_of_London
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "街上永远挤满人：脚夫、挑水的、赶车的、叫卖的、孩子、狗、猪，人与人之间几乎没有空隙"
  negative: "街上稀稀落落几个人、空旷的广场、有序排队"

- fact_id: london1666.city.030
  claim: 【航拍大气介质的史料依据】John Evelyn 1661 年的《Fumifugium》记：伦敦烧海煤（sea-coal）的烟把全城罩住，「疲惫的旅人在许多英里之外，是先闻到、而不是先看到他要去的这座城」；烟在一切落脚处「附上一层煤烟结成的壳或绒」；他并称几乎一半死在伦敦的人死于肺病
  tag: ✅
  source: John Evelyn《Fumifugium》(1661) 原文引句（经 Histories 转录）
  quote: >-
    "the weary Traveller, at many Miles distance, sooner smells, than sees the City to which he repairs. This is that pernicious Smoke which sullies all her Glory"；"superinducing a sooty Crust or fur upon all that it lights"；"almost one half of them who perish in London, die of Phthisical and Pulmonic distempers"
  source_url: https://www.gethistories.com/p/life-in-the-smoke-1661
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "全城上空压着一层横向铺开的褐灰色煤烟，太阳穿过它变成一枚苍白的圆盘；每一处屋顶、墙面、窗框上都覆着一层洗不掉的黑煤灰"
  negative: "湛蓝通透的天空、清澈的空气、白净的墙面、田园牧歌式的晴日、雾气是浪漫的白色薄纱"
  note: >-
    **这条决定航拍镜的大气层**：不是清澈的航拍，是穿过一层煤烟的航拍。1666 年 9 月初连续两个多月干旱高温，烟不散。
```

### 2g 旅行者一日路线（5 站，每站对应一个 shot 组）

> **距离口径说明**：所有「步行分钟」是**我按已引用的史料锚点推算的估值**（⚠️ 推算，非史料），
> 走速取 **80 m/min**（拥挤街道实际更慢）。锚点：桥长 926 ft（282 m）· Cheapside 长 450 yds（411 m）·
> Thames Street 长约 1800 yds（1646 m）· Monument 距起火点 202 ft（61.6 m）· 城墙周长 10608 ft（约 3.2 km）· 城域约 330 英亩。

| # | 站 | 到站方式 / 距离 | 步行 | 这一站看什么（fact 指针） | shot 组建议 |
|---|---|---|---|---|---|
| **1** | **Southwark 南岸 → 旧伦敦桥 → 桥北端 St Magnus 门前** | 徒步过桥 282 m，但桥上是被房屋夹死的窄街、人车挤 | **8–10 min** | 桥上房屋隧道 + **北端 1633 年留下的空档与松木挡板** + 南段 Nonsuch House + 石门顶上的头颅 + 桥孔下的水车轰鸣 | `city.006–010` `city.013` | 3–4 镜：桥南入口（硬切）→ 桥上连廊隧道（**20–30 s 一镜到底候选 B**）→ 北端空档（视野忽然打开，天光灌入，最好的一个「切口」）→ 落在 St Magnus 西门 |
| **2** | **Fish Street Hill 上坡 → Little Eastcheap → 布丁巷（下坡到 Thames Street）** | 上坡约 150 m + 东折 60 m + 布丁巷南下约 100 m | **5–7 min**（含停） | 屠夫的烫猪房、明沟里的血水、**Farriner 的面包铺**（在 Monument 现址以东 61.6 m）、编筐匠与旋木匠 | `city.011` `city.012` | 4–5 镜：Fish Street Hill 仰坡（远景）→ Eastcheap 市口（中景）→ **布丁巷一镜到底（首选 A，见 §2b）** → 面包铺门前近景（本片的「命运锚点」，留给收尾回扣） |
| **3** | **Thames Street 东段 → Billingsgate 鱼市 → 西行到 Old Swan / Steelyard** | 沿河街东行 200 m 再西行约 600 m | **10–12 min** | 码头、吊车、被车塞死的街、仓库里堆的沥青焦油麻绳树脂亚麻油酒白兰地（`housing.017` 的火药桶）、河阶与船夫、**Old Swan 台阶与「shooting the bridge」** | `city.014` `city.015` `housing.017` | 3–4 镜：码头全景 → 仓库敞门内部（把可燃物一次给足）→ Old Swan 石阶（船夫叫价）→ 河上回望桥与城 |
| **4** | **Gracechurch Street 北上 → Cornhill → 皇家交易所 → Cheapside 西行 → Guildhall** | 北上约 500 m + Cheapside 411 m + 北折约 200 m | **14–16 min** | 交易所内院的商人嗡鸣与钟声、Cheapside 的金匠街与敞开店面、Great Conduit / Standard / Cheapside Cross、Guildhall 门廊与巨人像 | `city.023` `city.024` `city.016`（并入下表） | 4–5 镜：交易所内院（**本片最热闹的一镜**）→ Cheapside 东端起幅（全城最宽的街，给一个「城市尺度」对比）→ 金匠街橱窗 → Guildhall 门廊 |
| **5** | **Cheapside 西端 → 旧圣保罗（Paul's Walk / 书商 / 脚手架 / Jones 柱廊）→ Ludgate 出城看一眼 Fleet Ditch → 折返** | 西行约 200 m + 出城 250 m + 折返 | **10–12 min** | **无尖顶的方塔**、包着白石新皮的哥特怪物、十柱柱廊、满墙脚手架、中殿里的市井、墓地的书商铺、Ludgate 的雕像、Fleet 臭沟 | `city.018–022` `city.003` `city.028` | 4–5 镜：Cheapside 西端望圣保罗（**签名构图**）→ 柱廊仰拍 → Paul's Walk 内景 → 墓地书商 → Ludgate 门洞出城（收） |
| **宿** | **回到 Fish Street Hill 的客栈过夜（Star Inn）** | 从 Ludgate 回 Fish Street Hill 约 1.1 km | **15 min** | 门洞进院、回廊式客栈、后院马厩与干草堆（**次日凌晨火星就落在这堆干草上**）、共睡的床、烛光 | `housing.016` `housing.018` | 3–4 镜：客栈门洞（暮色）→ 院内马厩与干草（**给足，这是明早的引信**）→ 房间烛光 → 窗外全黑的街（`housing.013`：**9 月 1 日没有任何公共照明**）＝ 全片收尾 |

> **纯步行合计约 62–72 min**；含停留、进屋、拍摄，正好撑满 10–15 min 成片的一天。
> **地理上走得通**：路线是「桥头（东南）→ 北上坡 → 沿河东西向 → 北上到城市中轴 → 西端圣保罗 → 折返桥头」，
> 全程在墙内、不折返重走同一段街，只有最后回宿处是长距离直线返程（可用一个转场镜跳过）。

---

## §5 住（`london1666.housing.NNN`）

### 5a 房屋形制与密度

```yaml
- fact_id: london1666.housing.001
  claim: 1666 年前 Cheapside 的临街屋，是十八九世纪伦敦联排屋的**木构架早期版本**：每层两间、四层或更多层、后面带院落与附属建筑；底层是店铺或作坊，主起居间（叫 hall，后来叫 dining room）在**二层（first floor）**，再往上是 chamber（卧室层）与 garret（阁楼）；多建在石砌地窖上
  tag: ✅
  source: >-
    IHR 研究项目《People in Place: houses, families in early modern London (1550-1720)》
  quote: >-
    "Street-front houses in Cheapside before the Fire of 1666 were an early, timber-framed version of the eighteenth- and nineteenth-century London terrace or row house, with two rooms on four or more floors and outbuildings behind."；"A shop or workshop occupied the ground floor, and the main living room, called the hall or later the dining room, was on the first floor, with chambers and garrets above."
  source_url: https://archives.history.ac.uk/people-in-place/pip.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "临街是一栋窄面宽、进深大的四五层黑木构架房子：底层敞着一间店铺，二层是带大窗的起居间，三四层是卧室，最上面是斜顶阁楼，房子后面接着一个小院与附属棚屋"
  negative: "独栋带前院的房子、砖石排屋、平屋顶、宽面宽、玻璃幕墙、门牌号"

- fact_id: london1666.housing.002
  claim: 这一类（富裕商人的）房子有 5–6 个壁炉、**室内厕所**，有的还通了水管；房间墙面做木护壁板（panelling）或挂彩绘布（painted cloth）；窗户大而且装玻璃
  tag: ✅
  source: IHR《People in Place》
  quote: >-
    "Houses like this would have five or six hearths, internal privies, and in some cases piped water; rooms were panelled or hung with painted cloths, and the large windows were glazed."
  source_url: https://archives.history.ac.uk/people-in-place/pip.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "室内四壁是深色木护壁板，或挂着彩绘的粗布幔；窗是分格的小块玻璃嵌在铅条里；屋角一座砖砌壁炉"
  negative: "裸露的土墙、糊纸墙、大片落地玻璃、壁纸、油画满墙、白色石膏墙面"

- fact_id: london1666.housing.003
  claim: 【同城贫富差三倍的量化依据】1660 年代炉灶税：**Cheapside 各教区每户平均 5.4 个壁炉**，**Aldgate 只有 2.5 个**，Clerkenwell 居中 3.3 个。Aldgate 那类地方是把原有房子分隔出租、把花园后院空地全盖上便宜的低层房，形成一张小巷与死胡同的网
  tag: ✅
  source: IHR《People in Place》（据 1666 年 London & Middlesex Hearth Tax）
  quote: >-
    "The mean number of hearths per dwelling was highest in the Cheapside parishes (5.4) and lowest in Aldgate (2.5), with Clerkenwell between the two at 3.3."；"Existing houses were subdivided and gardens, backyards and open spaces were built over with cheap, low-rise housing, forming a network of alleys and closes."
  source_url: https://archives.history.ac.uk/people-in-place/pip.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "主街上是五六层的高大木构架商人宅，转进旁边的小巷，立刻变成两三层、歪斜、挤在一起的破房，院子被后加的棚屋填满，巷子窄到只能一人通过"
  negative: "全城房屋高度一致、贫民区在城外、主街与小巷同样宽敞、房屋整齐划一"
  note: >-
    **建模分级的直接依据**：主街立面高（4–5 层）、背巷立面矮（2–3 层）且更乱。

- fact_id: london1666.housing.004
  claim: 1695 年的人头统计：Cheapside 每个户主名下平均 6.6 人，Aldgate 4.8 人——「一户」通常包含学徒、伙计与仆人，不只是一家人
  tag: ✅
  source: IHR《People in Place》
  quote: >-
    "Each householder answered for an average of 6.6 persons in Cheapside and only 4.8 in Aldgate."
  source_url: https://archives.history.ac.uk/people-in-place/pip.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一栋房子里住着店主一家、两三个学徒和一两个女仆，白天在店里和厨房之间来回，晚上分睡在上面几层"
  negative: "核心家庭独居、空荡的大宅、佣人住独立厢房"

- fact_id: london1666.housing.005
  claim: 【火势蔓延的关键，务必查证——已证实】多层木构屋普遍带 jetty（悬挑）：上层逐层向街面外挑，底层占地窄、越往上越往街上「encroach」；街道本就窄，顶层挑出后两侧几乎相接，当时人已经明确看出这一点的火险——「它既让大火更容易烧起来，也让救火更难施展」
  tag: ✅
  source: >-
    Great Fire of London（现代综述，引同时代评论）；Lichfields「The Great Fire of London: a history of master planning」（搜索摘要交叉核对）
  quote: >-
    "multi-storey timbered London tenement houses had 'jetties' (projecting upper floors)" with "gradually increasing size of their upper storeys"；"as it does facilitate a conflagration, so does it also hinder the remedy"；（交叉核对）"streets were often very narrow with the upper storeys of houses overhanging them"
  source_url: https://en.wikipedia.org/wiki/Great_Fire_of_London
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "街两侧的房子层层向街心外挑，三层比二层更凸出、四层又比三层更凸出；抬头只剩窄窄一条天，两边的屋檐在头顶几乎碰到一起，街面常年见不到直射阳光"
  negative: "上下垂直对齐的立面、开阔的街道天空、阳光洒满街面、房屋向内退让、现代退台式建筑"
  note: ⚠️「对街邻居能隔窗握手」的说法常见于科普转述，**未核到一手出处**，口播时说「几乎相接」即可，不要说「能握手」。

- fact_id: london1666.housing.006
  claim: 木构 + 茅草**被禁了几百年**，但这些便宜材料一直在用
  tag: ✅
  source: Great Fire of London（现代综述）
  quote: >-
    "Building with wood and roofing with thatch had been prohibited for centuries, but these cheap materials continued to be used"
  source_url: https://en.wikipedia.org/wiki/Great_Fire_of_London
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "大部分屋顶铺的是暗红褐色的陶瓦，但穷街背巷里仍能看到成片的茅草顶与木板顶，色泽发灰、边缘毛糙"
  negative: "全城统一陶瓦顶、石板瓦顶、金属屋面、茅草顶崭新金黄"
```

### 5b 建筑法规：存在，且被无视

```yaml
- fact_id: london1666.housing.007
  claim: 【特别查证项——法令存在且被无视】禁止木构与悬挑的法令**确实存在**：1661 年查理二世发布公告禁止悬挑窗与 jetty，**基本被地方当局无视**；1665 年他又发了一份更严厉的，明确警告街道过窄带来的火险，并授权**监禁**不服的建造者、**拆除**危险建筑——**同样几乎没有效果**。往前追，都铎至斯图亚特早期，至少有 3 部议会法案、9 道王室公告，以及数不清的星室法庭令与枢密院往来函件试图禁止或管制伦敦的建造，而市民「几乎不予理会」
  tag: ✅
  source: Great Fire of London（现代综述）；Create Streets「The long history of British Land Use Regulation」（搜索摘要交叉核对）
  quote: >-
    "In 1661, Charles II issued a proclamation forbidding overhanging windows and jetties, but this was largely ignored by the local government. Charles's next, sharper message in 1665 warned of the risk of fire from the narrowness of the streets and authorised both imprisonment of recalcitrant builders and demolition of dangerous buildings. It too had little impact."；（交叉核对）"at least three Acts of Parliament, nine Royal Proclamations and innumerable Orders in Star Chamber and letters to and from the Privy Council attempted to ban construction or regulate what could be built in London"；"the citizens of London took very little notice of the regulations"
  source_url: https://en.wikipedia.org/wiki/Great_Fire_of_London
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播素材，不入画）"
  negative: "把 1666 年的伦敦说成「没有防火法规」、说成「当时人不知道危险」"
  note: >-
    **这是本片一个很好的叙事钩**：法规有、警告有、皇帝亲自发过两次公告，**全城照样我行我素**。⚠️ 1661/1665 两道公告的**原文**本次未核到（只在 T3 转述里），口播前建议再查 *Stuart Royal Proclamations* 卷。

- fact_id: london1666.housing.008
  claim: 【火后法条反证火前形态】1667 年《重建伦敦城法》（19 Car. II c. 3）规定：此后城内及周边一切建筑的**外墙一律用砖或石**（门框窗框除外）；**「任何 Bulks、Jettyes、Windowes、Posts、Seates 或类似之物，都不得在任何街、巷、小巷上营造或竖立，使其伸出房屋原有地基之外」**。房屋分四等：一等（背巷）2 层＋地窖阁楼、层高 9 ft / 9 ft；二等（有名的街巷）3 层、10 / 10 / 9 ft；三等（主街）4 层、10 / 10.5 / 9 / 8.5 ft；四等（大宅）层数自定但不超过 4 层。墙厚以砖长计：一等房前后墙一层高处 2 砖长、往上到阁楼 1.5 砖长，隔墙 1.5 砖长；二三等房隔墙一层高处 2 砖长、往上 1.5 砖长。**法条禁什么，火前就有什么**
  tag: ✅
  source: >-
    《Statutes of the Realm》vol 5，Charles II, 1666: An Act for rebuilding the Citty of London
  quote: >-
    "all the outsides of all Buildings in and about the said Citty be henceforth made of Bricke or Stone or of Bricke and Stone together except Doore cases and Window Frames"；"noe Bulks Jettyes Windowes Posts Seates or any thing of like sort shall be made or erected in any Streets Lanes or By Lanes to extend beyond the auntient foundation of Houses"；（一等）"two Stories high besides Cellers and Garrets... first Story be nine foote high... second Story nine foote high"；（三等）"four Stories high... first Story containe full ten foote... second ten foote and an halfe, the third nine foote, the fourth eight foote and an halfe"
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp603-612
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（建模层高参考，不入画）"
  negative: "把 1667 法规定的砖石排屋当成 1666 年的样子画"
  note: >-
    **建模层高直接照抄**：主街 4 层（10 / 10.5 / 9 / 8.5 ft ≈ 3.05 / 3.20 / 2.74 / 2.59 m，总约 11.6 m ＋ 阁楼）；次街 3 层；背巷 2 层。1666 年木构屋的层高与这接近（法条是在既有实践上做规范），可当**保守下限**用。

- fact_id: london1666.housing.009
  claim: 【街宽的可用量尺】1667 法授权拓宽「城内一切窄于 **14 英尺**的狭窄通道」，并把若干具名街道（如 Water Lane）定为 24 ft 宽。**反推：火前城里大量小巷宽度不足 14 ft（4.3 m），其中有些远不足**
  tag: ✅
  source: 《Statutes of the Realm》vol 5，1667 Rebuilding Act
  quote: >-
    "inlarge any other such strait and narrow passages within the said Citty as are lesse then fowerteene foote in breadth"；Water Lane and others specified as "twenty fower foote in breadth"
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp603-612
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（建模街宽参考，不入画）"
  negative: "把所有街都建成 10 m 以上的宽街、把小巷建成 5 m 以上"
  note: >-
    **建模量尺**：主街（Cheapside / Thames Street / Cornhill / Gracechurch）取 8–12 m；次街（Fish Street Hill / Eastcheap）取 5–7 m；lane（布丁巷 / Botolph Lane）取 **3–4 m**；alley 取 1.5–2.5 m。**上层挑出后，lane 的顶部净空只剩 1.5–2 m**，这就是 jetty 的画面效果。

- fact_id: london1666.housing.010
  claim: >-
    Cheapside 是城内最宽、最气派的街，东起 Old Jewry 口的 Great Conduit、西至圣保罗墓地边的 Little Conduit，Hatton 1708 记长 450 码；两侧是三层、四层甚至五层的高楼，店面朝街敞开、摆着奢侈品；Goldsmiths' Row 在 Bread Street 与 Friday Street 之间，Stow 说那里有 10 栋房子 14 间铺子、是全伦敦最漂亮的一片。街上还立着 Great Conduit、Standard（重罪行刑处）、三层高的 Cheapside Cross、Little Conduit
  tag: ⚠️
  source: MoEML「Cheapside Street」；Grub Street Project「Cheapside」（转录 Hatton 1708 / Strype 1720 / Lockie 1810）
  quote: >-
    "ran east-west between the Great Conduit at the foot of Old Jewry to the Little Conduit by St. Paul's churchyard."；"lined with buildings three, four, and even five stories tall, whose shopfronts were open to the light and set out with attractive displays of luxury commodities."；"there were ten houses and fourteen shops in Goldsmith's Row, and that they were easily the most beautiful in London."；Cheapside Cross "three stories tall"；（Hatton）"Wd. L. 450 Yds"；（Hatton）"one of the most Spacious, Publick, Beautiful and Rich streets, as also of the largest Buildings and greatest Trade in London."
  source_url:
    - https://mapoflondon.uvic.ca/CHEA2.htm
    - https://www.grubstreetproject.net/places/1024/
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一条明显比别处宽的大街，两侧四五层的高楼一字排开，底层店面整排朝街敞开、摆满金银器与布匹；街中央立着一座石砌的水房、一根石柱、一座三层高的哥特式十字碑"
  negative: "Cheapside 与小巷一样窄、店铺有玻璃橱窗、街上跑马车道分隔、十字碑是简单石柱"
  note: ⚠️ **宽度数值缺失**：Hatton 的「450 Yds」是长度。网上流传的「62 feet wide」**未核到一手出处，不要用**。口播只说「城内最宽的街」。
```

### 5c 街面 · 排水 · 照明

```yaml
- fact_id: london1666.housing.011
  claim: 街面做法：中央一条 kennel（明沟），沟两侧铺 chain stones（顺沟的条石）；路基先夯土、再铺砾石夯实、最后铺卵石或方石
  tag: ⚠️
  source: 二手转述（未核到一手）
  quote: >-
    "Streets had a central 'kennel' or gutter of chain stones on either side of which was laid firstly dirt well rammed down, then gravel, rammed again, and finally either pebbles or square pitching."
  source_url: https://www.british-history.ac.uk/vch/oxon/vol4/pp350-364
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: "街面是大小不一的圆卵石铺成，中央一条浅沟顺街往低处流，沟里是黑灰色的污水、菜叶、灰烬和马粪；沟两侧各一排较平整的条石，车轮压出两道亮痕"
  negative: "平整的现代石板、沥青、排水篦子、路缘石、人行道、分道线、路面干净"
  note: ⚠️ 只见转述。但「中央明沟」这一形态在多处独立来源一致出现，画面可用，数值不要写。

- fact_id: london1666.housing.012
  claim: 城市废物处理：马桶直接倒进街上；地下储粪坑（cesspool）在 17 世纪逐渐普及；raker 与 scavenger 负责把街上的垃圾清走，运到城外指定处或河边指定的堆场，再由**粪船（dung-boat）**运出；Sergeant of the Channels 专门巡街检查街巷是否清干净，有罚款权；beadle 与 constable 协助催缴与执行。这套体系的出发点不只是脏，还有当时把「腐败空气」与瘟疫挂钩的瘴气／体液学说（1665 年伦敦刚经历大瘟疫）
  tag: ✅
  source: MoEML「Sewage and Waste Management」
  quote: >-
    "surveyed local streets and lanes to make sure they were kept free of rubbish; he also had the power to fine violators."；"were charged with physically removing rubbish from streets and transporting it to designated areas beyond the city limits or to designated areas on the banks of Thames, whence the rubbish would be removed by dung-boats."；"the use of cesspools—underground vaults for storing privy waste—increased throughout the seventeenth century."；"miasmic and humoral theories"
  source_url: https://mapoflondon.uvic.ca/SEWA1.htm
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "巷子里一个人端着马桶从二楼窗口往街上泼；街角堆着一堆等着装车的垃圾，两个扫街工用宽木铲往马车上铲；河边一条平底船正在装这些东西"
  negative: "垃圾桶、下水道井盖、清洁工制服、街面无异物、消毒喷洒"
  note: 与 `city.011` 呼应：布丁巷的粪船就是这套体系的末端。

- fact_id: london1666.housing.013
  claim: 【夜戏关键——1666 年 9 月 1 日的街上没有任何公共照明】英国最早的公共照明记载是 1405 年令伦敦各区确保沿主街每户门外挂一盏点亮的灯笼，「大致从黄昏到九点、在月黑之夜」；1416 年市长 Henry Barton 令**冬夜**挂灯，时段是 **Hallowtide（11 月 1 日）到 Candlemas（2 月 2 日）**；1657 年市政首次在私人户主无法承担时自行供灯；系统性的「住户每晚挂灯」要到大火**之后**（1666 年起由 Commissioners of Sewers 接管、1668 年规定住户挂灯）；带玻璃灯罩的路灯 1683 年才第一次出现在 Cornhill；1694 年才有第一份照明承包合同（每 8–10 户一盏，一年 120 个黑夜、入夜到午夜）。**所以 9 月 1 日既不在冬季挂灯期、也在正式制度之前——夜里的街只有窗里透出的烛光、提灯的人、打更人的灯笼和月亮**
  tag: ✅
  source: UK 街道照明年表（Simon Cornwell，逐年条目）
  quote: >-
    "1405: First historical reference to public lighting in the UK when Aldermen of the City of London were ordered to see that a lighted lantern was hung outside every house along the highway, generally from dusk to nine o'clock 'when the moon was dark.'"；"1416: Henry Barton, Lord Mayor of London, ordained lanthorns with lights to be hanged out on winter evenings between Hallowtide and Candlemas."；"1657: The Aldermen ordered supplies of lights where private householders couldn't be held responsible"；"1666: Following the Great Fire, the Commissioners of Sewers assumed responsibility for ensuring City streets were lighted."；"1683: The first lanterns with glass sides appeared in Cornhill"
  source_url: https://www.simoncornwell.com/lighting/timeline/index.htm
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "入夜后街上一片漆黑，没有任何街灯；光只来自沿街窗格里透出的昏黄烛火、行人手提的角质灯笼，以及打更人腰间的一盏灯；月光落不进窄巷，只照亮屋顶的一条边"
  negative: "【高优先级负向】街灯、路灯杆、煤气灯、玻璃灯罩路灯、成排照明、街道整体被照亮、暖黄泛光的浪漫夜景、火把插在墙上成排"
  note: >-
    **本片夜戏的硬约束**。1666-09-01 的夜 ＝ 真黑。这也正是次日凌晨火烧起来时「没人第一时间看见」的物理原因。

- fact_id: london1666.housing.014
  claim: 当时的手提灯笼多是**刮薄的兽角**做罩（角质半透明），燃料是动物或植物油脂、或鱼油；1461 年市府规定灯笼用的蜡烛「每磅至少十二支」，1599 年改为「每磅至少八支」（即蜡烛变粗了）
  tag: ✅
  source: UK 街道照明年表；英国照明史科普（搜索交叉核对）
  quote: >-
    "1461: First street lighting specification issued by the Mayor and Aldermen regarding candles for lanterns, specifying 'at least twelve to the pound in weight.'"；"1599: The specification was altered to specify candles of 'at least eight to the pound in weight.'"；（交叉核对）"lanterns were mainly cheap affairs made out of animal horn scraped until they were thin enough for a light to shine through"
  source_url: https://www.simoncornwell.com/lighting/timeline/index.htm
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "手里提的是一只方形木框灯笼，四面嵌着刮到半透明的兽角片，里面一支粗蜡烛，光昏黄、只照亮脚前一小圈地"
  negative: "玻璃灯罩、金属提灯、油灯明亮稳定、电池灯、灯光照亮整条街"
```

### 5d 取暖 · 用水 · 客栈 · 可燃物

```yaml
- fact_id: london1666.housing.015
  claim: 城内取暖与做饭烧的是海运来的煤（sea-coal），这是伦敦烟霾的来源；Evelyn 1661 年点名酿酒、染布、制皂、制盐、烧石灰这些行业是元凶，并主张把它们迁出城；他描述这烟给一切落脚处附上一层煤烟壳
  tag: ✅
  source: John Evelyn《Fumifugium》(1661)；Folger 转录
  quote: >-
    "superinducing a sooty Crust or fur upon all that it lights"；（Evelyn 点名的行业）"Brewers, Dyers, Sope and Salt-boylers, Lime-burners, and the like"
  source_url:
    - https://www.gethistories.com/p/life-in-the-smoke-1661
    - https://www.folger.edu/blogs/shakespeare-and-beyond/air-pollution-london-fumifugium/
  tier: T0+T2
  verified_by: ai_read
  used_in: []
  prompt_string: "屋里壁炉烧的是黑亮的块煤，不是木柴；炉膛铁架上架着煤，火焰偏蓝黄、烟重；屋顶上成千上万根砖烟囱同时冒烟，烟往同一个方向横着铺开"
  negative: "烧木柴的明亮橙火、篝火、木柴堆在炉边、无烟、烟囱稀少、烟垂直上升"
  note: >-
    `city.030` 的地面对应面。烟囱密度是航拍的一个重要纹理。

- fact_id: london1666.housing.016
  claim: 客栈（inn）的住宿形态：绅士可以租单间、通常单独用餐（除非带了朋友），含晚饭、床、早饭约 **5–6 先令一晚**；独行的普通旅客约 **2 先令**，与主人同桌吃 **6 便士**；喂马冬天 18 便士（燕麦＋干草＋垫草）、夏天放牧 3 便士。床多是填豆荚壳、稻草或羽毛的箱式床，**穷客两三人（有时更多）与陌生人同睡一床**以分摊费用兼取暖，讲究的旅客自带便携床铺防虫；客栈后院是马厩与马夫（ostler）的小屋。Fynes Moryson（1617）记「每个仆役都随叫随到，指望一点小赏」、客栈「家什齐备」
  tag: ✅
  source: English Historical Fiction Authors「Bed and Breakfast in Seventeenth Century England」（引 Fynes Moryson 1617、Thomas Brockbank 1695、Evelyn 日记）
  quote: >-
    "Five or six shillings per night for supper, bed, and breakfast. Solo travelers could obtain lodging for two shillings."；"Sixpence when dining communally at the host's table."；"Eighteenth pence in winter for oats, hay, and bedding straw; threepence in summer for pasture."；"each servant being ready at call, in hope of a small reward"；"well furnished with household stuff."；"Poorer guests shared two or three to a bed with strangers to split costs and gain warmth."
  source_url: https://englishhistoryauthors.blogspot.com/2016/08/bed-and-breakfast-in-seventeenth.html
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "从街上一道高大的马车门洞进去，里面是长方形后院，三面是带外挑木回廊的客房，回廊靠木楼梯上去；院子尽头是马厩，地上堆着干草与垫草，马夫在卸鞍；房间里一张挂帐的木框床、一张小桌、一支蜡烛，没有别的"
  negative: "酒店前台、独立卫浴、门牌钥匙、单人床铺整洁、大堂、走廊地毯、客房编号"
  note: ⚠️ 这是**全英格兰**的通例（T2），非伦敦城内某家客栈的实录。本站落到 Fish Street Hill 的 Star Inn（`housing.018`）时，只用形态、不编具体陈设。

- fact_id: london1666.housing.017
  claim: 【火因的物理基础，也是「住」的一部分】泰晤士街南侧临河的仓库与棚屋里堆满可燃物：穷人的油毡棚屋夹在「老纸屋和最易燃的焦油、沥青、麻、松脂、亚麻之类东西」之间；Pepys 9 月 2 日亲眼看到烧的是「油、酒、白兰地和别的东西的仓库」
  tag: ✅
  source: Great Fire of London（现代综述，引同时代文献）；Pepys《Diary》1666-09-02
  quote: >-
    "tar paper shacks of the poor were shoehorned amongst 'old paper buildings and the most combustible matter of tarr, pitch, hemp, rosen, and flax'"；（Pepys）"the warehouses of oyle, and wines, and brandy, and other things"
  source_url:
    - https://en.wikipedia.org/wiki/Great_Fire_of_London
    - https://en.wikisource.org/wiki/Diary_of_Samuel_Pepys/1666/September
  tier: T0+T3
  verified_by: ai_read
  used_in: []
  prompt_string: "河边仓库的大门敞着，里面从地面堆到梁下：沥青桶、焦油桶、成捆的麻绳、松脂块、亚麻包、油罐、酒桶；桶缝渗出的黑油在地上积成一摊，空气里是松脂和酒精混在一起的味道"
  negative: "仓库整齐分区、金属货架、防火门、灭火器、货物有标签、地面干净"
  note: 路线第 3 站的核心画面。**不要只拍码头外观，要进仓库门内给这一层**。

- fact_id: london1666.housing.018
  claim: 火从布丁巷 Farriner 的面包房烧起后，强劲东风把火星吹到 **Fish Street Hill 上 Star Inn 院里的干草与饲料堆**上，把客栈点着，接着引燃 St Margaret 教堂，再烧到泰晤士街的临河仓库与码头
  tag: ⚠️
  source: HISTORY.com / London Fire Brigade 等（仅搜索摘要）
  quote: >-
    "the bakery fire soon spread to other buildings on Pudding Lane before leaping to nearby Fish Street, where it torched the stables of a hotel called the Star Inn."；"the strong wind that blew that night sent sparks that next ignited the Church of St. Margaret, and then spread to Thames Street, with its riverside warehouses and wharves."
  source_url:
    - https://www.history.com/articles/when-london-burned-1666s-great-fire
    - https://www.london-fire.gov.uk/museum/london-fire-brigade-history-and-stories/fires-and-incidents-that-changed-history/the-great-fire-of-london/
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "客栈后院的马厩边堆着一垛齐人高的干草，草垛紧挨着木构的马厩墙，离街只隔一道矮墙"
  negative: "干草堆在远离建筑的空地、院子空旷、干草被苫布盖住"
  note: ⚠️ **只来自搜索摘要**。但它给了收尾镜一个完美的落点：**旅行者睡的那家客栈的干草堆，就是几小时后的引信**。进 prompt 前请复核 Star Inn 的名称与位置。

- fact_id: london1666.housing.019
  claim: 城里的水：到 1666 年城内散布着至少 15 处 conduit / standard（公共取水点）；1582 年起 Morice 的桥头水车把泰晤士河水泵进城；1613 年 New River 从 Lea 河与泉井引水入城；管网是**整段榆木原木钻通做成的木管**，接户用铅制细管（quill）。conduit 的水靠 water carrier（俗称 cob / tankard bearer）挑送到户：有人肩扛一只大木桶沿街叫卖，有人用扁担挑两只三加仑木桶
  tag: ⚠️
  source: Great Conduit / London water supply infrastructure / New River Company（搜索摘要，多源一致）
  quote: >-
    "There were at least 15 conduits or standards scattered about the City by the time of the Great Fire in 1666."；"Some hawked water through the streets, in a large tankard on their shoulders; others would lug two 3-gallon wooden tubs hung from a yoke over their shoulders."；"Miles of wooden pipes – bored from whole elm tree trunks – were laid."
  source_url:
    - https://en.wikipedia.org/wiki/Great_Conduit
    - https://en.wikipedia.org/wiki/London_water_supply_infrastructure
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "街中央一座石砌的小水房，几个女人排队用木桶接水；旁边一个挑夫肩上扛着一只大木桶，另一个用扁担挑两只小桶快步走过"
  negative: "水龙头、水泵手柄、金属水桶、消防栓、自来水管外露"
  note: ⚠️ 只来自搜索摘要。**与火相关的一个反讽**：1666 年 9 月 2 日凌晨，桥头水车就在火场旁边，但它最早被烧毁，救火水源随之断掉。

- fact_id: london1666.housing.020
  claim: Fleet Ditch（Ludgate 外、Fleet Bridge 与 Holborn Bridge 之间那段 Fleet 河）在 1666 年前已经是一条被城市垃圾堵死的臭沟：两岸的码头、磨坊和作坊——尤其屠夫把下水直接扔进水里，加上养猪的与卖牡蛎的的废物——让历次疏浚都很快白费
  tag: ⚠️
  source: Grub Street Project「Fleet Ditch」essay（搜索摘要）
  quote: >-
    "crept slow enough, not so much for age as the injection of the City refuse wherewith it is obstructed."；"notably those of butchers who threw offal into its stream, not to mention the waste left by pig-keepers and oyster sellers"；"Below Fleet Bridge the Fleet itself was labelled 'Fleet Ditch', an apt name by then – it was a stinking mass of refuse."
  source_url: https://www.grubstreetproject.net/essays/fleet-ditch/
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: "出了西门是一条又宽又浅的黑水沟，水面浮着菜叶、内脏、木屑和一层油膜，几乎不流动；两岸挤着磨坊、屠案和堆料棚，气味逼人"
  negative: "清澈的小河、绿树成荫的河岸、石砌整齐的驳岸、河上有游船"
  note: ⚠️ 只来自搜索摘要。用于路线第 5 站出城一眼。
```

---

## §2b 给 Blender 整城白模的建模要点

> **总纲（照 `ai_video.md` rule 4g）**：环境**永远不用 image-to-3D**；
> **几何在 3D、长相在主体（参考图）**；全项目**只有一份 `london1666.blend`**，所有 previz 从它渲；
> **镜头先于几何**——先画两个签名镜的路径，再按「镜头要拍到什么」定精度。
> 建议脚本落在 `tools/build_london1666.py`（确定性生成、不手改 blend）。

### A. 模数（先定这个，构件按它出）

| 项 | 取值 | 依据 |
|---|---|---|
| 街面到二层挑出的净空 | 2.6–3.0 m | `housing.008`（1667 法一层高 9–10 ft） |
| 主街屋总高（4 层＋阁楼） | **13–15 m** | `housing.008` 三等房 10+10.5+9+8.5 ft ≈ 11.6 m ＋阁楼 |
| 次街屋总高（3 层＋阁楼） | 10–12 m | 同上，二等房 |
| 背巷屋总高（2 层＋阁楼） | 7–9 m | 同上，一等房 |
| **单栋临街面宽** | **4.5–6.5 m**（窄面宽、大进深） | `housing.001` 每层两间 |
| 每层 jetty 外挑量 | **0.35–0.55 m / 层**，逐层累加 | `housing.005`；四层屋顶部共挑出 1.4–1.6 m |
| 主街宽（Cheapside / Thames St / Cornhill / Gracechurch） | 8–12 m | `housing.009` 反推 + `housing.010` |
| 次街宽（Fish Street Hill / Eastcheap） | 5–7 m | `housing.009` |
| **lane 宽（布丁巷 / Botolph Lane）** | **3–4 m**（顶部净空剩 1.5–2 m） | `housing.009`「< 14 ft 要拓宽」 |
| alley 宽 | 1.5–2.5 m | 同上 |
| 城墙 | 高 **6 m**、厚 **2.5 m**，间隔设方塔 | `city.001` |
| 城域 | **约 330 英亩 ＝ 1.34 km²**；东西约 1.6 km、南北约 0.9 km；墙周长约 3.2 km | `city.001` |

### B. 按「镜头接近度」分四级

#### ① A 级 — 真立面（旅行者贴身走过，镜头距墙 < 8 m）

**只有这几段，总长控制在 ~400 m 之内**（rule 4g ④：必做的只有镜头真正贴过去的那几米）：

| 段 | 长度 | 必须做到的细节 |
|---|---|---|
| **布丁巷南半段**（Thames Street 口 → Farriner 面包铺门前） | **~40 m** | 逐层 jetty、真木构架（柱／梁／斜撑／填充抹灰）、歪斜不对齐的小窗、烫猪房的低门与外挂铁钩、中央明沟、面包铺的砖烟囱与柴堆 |
| **桥上一段**（桥中段密集房屋区） | ~60 m | 4–5 层桥上屋、**每隔一栋一道跨街 cross building**（这是桥的签名）、房屋悬挑到河面上的后半身、连廊之间漏下的天光 |
| **桥北端空档** | ~50 m | **光桥面 + 两侧钉的松木挡板**（`city.008`）——这一段**不建房子**，是整座桥最重要的负空间 |
| **Fish Street Hill 下段 + St Magnus 西门** | ~50 m | 上坡坡度、中世纪石塔（**不是 Wren 白塔**）、教堂西门紧贴车道 |
| **Thames Street 仓库一段**（Billingsgate 附近） | ~60 m | 敞开的仓库大门＋门内可燃物堆（`housing.017`）、吊车臂、码头伸进水里的木桩 |
| **Cheapside 金匠街一段** | ~50 m | 整排朝街敞开的店面、Goldsmiths' Row 的彩绘木雕立面、街中央的 Standard 与 Cheapside Cross |
| **旧圣保罗西立面** | 单体 | **Jones 的十柱柱廊（柱高 13.7 m）＋ 满墙木脚手架 ＋ 无尖顶的方塔（204 ft ＝ 62 m）** |

#### ② B 级 — 体块 + 屋顶形制（中景／长镜背景，镜头距 8–80 m）

- Cheapside 其余段、Cornhill、Gracechurch Street、Eastcheap、Thames Street 其余段、Lombard Street、Fenchurch Street 的**沿街体块**：只做面宽节奏 + 逐层挑出的轮廓 + 屋顶坡度与山墙朝向（**大量是山墙朝街的陡坡顶**，不是屋脊平行街道），窗洞做凹槽不做窗框。
- **皇家交易所**：四层方块 + 中央挖出内院 + 一圈柱廊 + 一座钟楼（`city.023`）。
- **Guildhall**：46.5 m × 15 m × 脊高 27 m 的大厅体块 + 南面门廊（`city.024`）。
- **旧圣保罗主体**：179 m × 30 m、横厅通宽 88 m、方塔 62 m（`city.021` `city.018`）。**它是全城唯一一个需要 B 级以上精度的远景体量。**
- 航拍能辨认的 **20–30 座教区教堂塔**：做 3–4 种塔型（方石塔 / 方塔＋铅皮小尖 / 带角塔的方塔）随机撒布（`city.026`），**其余 70 座只做屋顶上的小凸起**。

#### ③ C 级 — 纯体块（航拍远景）

- **全城屋海**：按 ward 划区，每区用 2–3 组重复的排屋 proxy（面宽 5 m × 进深 15 m × 高 11 m 或 8 m），沿街线阵列；**只要保证「窄面宽 + 陡坡瓦顶 + 密不透风」三个特征**，单体不建模。
- **城墙 + 七门**：墙做挤出折线，门做体块 + 门楼轮廓（`city.001` `city.002`）。
- **伦敦塔**：White Tower 方塔 + 四角塔楼 + 两圈外墙 + 护城壕；**壕外紧贴民房**（`city.025`）。
- **南岸 Southwark**：只做低矮密集的一片 + Southwark Cathedral 的塔。
- **Fleet Ditch 与 Moorfields**：Fleet 做一条黑水带 + 两岸棚屋带；Moorfields 做一片空旷草地（火后难民地，可作对照）。
- **烟囱**：不逐根建模，用 **displacement / 粒子撒点**在屋顶面上撒砖烟囱 proxy——密度是航拍的关键纹理（`housing.015`）。

#### ④ D 级 — 不建

- 城墙以北 Moorfields 以外、Westminster、Whitehall、城外郊野：只做**天际线剪影**（远山/树带），不建体量。
- **所有室内**：另起 set，不进整城 blend。
- 未出现在两个签名镜路径上的背巷内部（只保留巷口）。
- **任何白模／灰模都不许当出图参考**（rule 4d ①）——它们只服务 previz 机位。

### C. 航拍长镜的推荐飞行路径

> **坐标原点建议**：取 **Monument 现址**（`city.012` 给的精确锚点）为 (0,0,0)，X 轴向东、Y 轴向北。
> 则 Farriner 面包铺 ≈ (+61.6, 0)，Fish Street Hill 向南下坡到 Thames Street，桥头 St Magnus ≈ (−20, −130)。
> 圣保罗西立面 ≈ (−1050, +180)，伦敦塔 White Tower ≈ (+640, −180)，皇家交易所 ≈ (−330, +330)，Guildhall ≈ (−700, +560)。
> （⚠️ 以上相对坐标是我按现代地图与史料距离**推算的起手值**，builder 应以 Ogilby & Morgan 1676 实测图套合后修正。）

| # | 机位（相对 Monument，m） | 离地高 | 看向 | 焦距 | 画面里必须有 |
|---|---|---|---|---|---|
| **WP1 起幅** | (+700, −420) | **8 m** | (−100, −200) | 24 mm | **贴水逆流向西**：右前方是旧伦敦桥的十九座墩与船形护堆、桥孔间白色的落差水花；桥上房屋像一条悬空的街；**北端那一截空档**（光桥面＋松木挡板）在画面正中——这是「1666 年」最不可伪造的一个特征 |
| **WP2 掠桥** | (+120, −300) | 45 m | (−250, +100) | 24 mm | 拔离水面掠过桥面：左侧两孔下的水车在转、木塔里泵声；右侧 St Magnus 石塔与 Fish Street Hill 上坡；Billingsgate 的桅杆林 |
| **WP3 拔高** | (−200, −700) | **280 m** | (−600, +300) | 24 mm | 转西北爬升：褐红瓦顶的海洋铺满画面，**上百座教堂塔从瓦海里戳出来**；海煤烟层横着压在屋顶之上（`city.026` `city.030`） |
| **WP4 全景顶点** | (−400, −2200) | **900 m** | (−500, +250) | 24 mm | **一眼框住整座城**：不规则的城墙圈住 330 英亩、泰晤士河自西向东斜穿、旧伦敦桥是河上唯一一条实线、**西侧压着那座顶是平的巨大灰色教堂**、东南角是伦敦塔的白方塔、南岸 Southwark、西北角外 Moorfields 的空地。太阳被煤烟滤成苍白圆盘 |
| **WP5 俯冲** | (−900, −350) | 130 m | (−1050, +180) | 24 mm | 沿 Cheapside 轴线下降：Little Conduit 与 Cheapside Cross 从镜头下掠过，前方是圣保罗西端的十柱柱廊与满墙脚手架 |
| **WP6 落幅（主选）** | (+45, −15) | **8 m** | (+62, 0) | 35 mm | **落在布丁巷口**，正对 Farriner 面包铺那扇低矮的门；巷子两侧的 jetty 在头顶几乎合拢，街心明沟里的水往镜头脚下流 |

**备选落点**：若剧本让旅行者从桥入城，把 WP6 改为 **(−20, −130)、离地 8 m、看向 St Magnus 西门**，
路径末段改为沿 Fish Street Hill 下坡俯冲。**两个落点二选一，不要两个都做。**

**三条工程约束（必须写进 previz）**：

1. **路径总长约 5.6 km。** 在 30 s 渲染上限内 ＝ 平均 187 m/s（673 km/h），**真实无人机做不到**，
   必须做**速度坡道**：WP1→2 慢（7 s）、WP2→3 快（5 s）、WP3→4 更快（6 s）、WP4 悬停（2 s）、
   WP4→5 极快俯冲（5 s）、WP5→6 减速落幅（4 s），合计 **29 s**。
   **备选**：按 `ai_video.md` 的 30 s 天花板**拆成两镜**——A 镜 WP1–WP4「出河看城」（含 WP4 悬停作镜内切点），
   B 镜 WP4–WP6「俯冲入城」。拆的话两镜之间是**镜内切**不是硬切，共用一条 previz 曲线。
2. **【景别档】WP6 落幅之后的下一镜必须是紧取景。** 航拍落幅是极远景（`人占画高` ≈ 0.02），
   下一镜若仍是全景就是 ❌。建议下一镜直接切到**面包铺门前的近景**（`人占画高` ≈ 0.55），
   比值 0.02 / 0.55 ＝ **0.036 ≤ 0.5 ✅**，且机位标签完全不同。每镜 `## Shot context` 照写
   `景别档: {起幅景别}{人占画高} → {落幅景别}{人占画高}` 与机位标签。
3. **烟层是这一镜的主角之一。** `city.030` 的煤烟不是后期滤镜，要在 blend 里做成**体积雾的分层**
   （地面 0–15 m 一层淡、屋顶 15–40 m 一层浓、40 m 以上渐散），太阳做成被滤过的苍白盘。
   没有这层烟，航拍会像一张干净的现代航测图。

### D. 20–30 s 一镜到底穿街长镜：选段与预算

**算过的硬约束**：跟拍步行速度约 **1.3 m/s**，27 s 只能走 **~35 m**。
所以「一镜穿过 Fish Street Hill 全长再拐进布丁巷」（合计 330 m）**在物理上不可能**——
硬拍就得把人物变成跑的，或者把镜头改成不跟人的飞行镜。

**结论：这一镜的 A 级真立面预算就是「35–40 m 街道 + 两端看得见的部分」。**

| 方案 | 选段 | 长度 | 为什么 |
|---|---|---|---|
| **A（首选）** | **布丁巷：Thames Street 口 → Farriner 面包铺门前** | ~38 m | ① 全片的命运锚点在终点；② 一条**上坡**巷，走起来有天然的运动节奏与视线变化；③ 三种业态在 38 m 里全齐（烫猪房 → 编筐旋木作坊 → 面包铺）；④ 巷窄 3–4 m、jetty 在头顶合拢，**一镜到底的压迫感最强**；⑤ 终点门前可以自然减速落幅成近景 |
| **B（备选）** | **桥上：从密集房屋段走进北端空档** | ~40 m | ① 「被房屋夹死的隧道」忽然打开成「光桥面 + 河 + 天」，**镜内明暗与空间的反转天然成立**；② 这是 1666 年最不可能被误认成别的年代的一段路；③ 缺点是桥上房屋要建两侧＋跨街连廊，几何量比方案 A 大约两倍 |

**两案的共同要求**：
- **一个地点 + 一个状态 ＝ 一镜**（`ai_video.md` 2026-09-08 修订）：镜内可以切，切口不带转场效果、不打断这一镜的单一时间线、氛围与光；`分镜:` 行逐段写起止秒与「连续运镜／切」。
- **hero beat 放在镜尾**：方案 A 的 hero ＝ 面包铺门；方案 B 的 hero ＝ 空档开口那一下。放在尾巴，坏了只重渲一次。
- **A 级几何只建这 38–40 m**，两端各多建 15 m 作为景深收尾，其余一律降到 B 级。

---

## 附：本 worker 未覆盖、需别的 worker 或后续补的

| 项 | 归属 |
|---|---|
| 衣（1660 年代伦敦市民/商人/劳工的服装锁定串） | 另路 |
| 食、物价与货币（先令/便士的购买力锚点） | 另路（本文只给了客栈价 `housing.016`） |
| 语言与称谓（1666 年伦敦口语、如何称呼陌生人） | 另路 |
| 行（河上交通、轿子 sedan chair、hackney coach、渡船） | 另路 —— 本文只给了 Old Swan 与「shooting the bridge」 |
| 1665 年大瘟疫的余波（1666 年 9 月街上还有什么痕迹） | 另路；`housing.012` 的瘴气说是一个接口 |
| **1661 / 1665 两道王室公告的原文** | **需补查** *Stuart Royal Proclamations*（`housing.007` 现为 T3 转述） |
| **Ogilby & Morgan 1676 实测图套合** | **建模前必做**——把本文的推算坐标换成实测坐标（`british-history.ac.uk/no-series/london-map-ogilby-morgan/1676`，比例 100 ft / inch） |
