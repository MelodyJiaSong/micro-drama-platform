---
worker_id: researcher-w4-prices
stage: 0
role: researcher
angle: prices-work-transport
status: complete
blockers: []
confidence: medium
task_id: sk3-20260918-211545
scope: dossier §6 行 / §7 物价与货币 / §8 职业与社会阶层
fact_counts: {ai_read: 77, ai_draft: 5, total: 82}
---

# W4 · 伦敦 1666-09-01 · 物价·货币 / 行 / 职业与阶层

> **口径铁律**：本站一切金额只折算成「**几天工钱**」。**禁止**出现「一先令 ＝ 今天多少元 / 多少镑」。
> 全片统一分母：**非技术劳工 16 便士／天**（见 §7.2 锚 B）。大额物件另附「工匠（30d/天）几天」。
> `verified_by: ai_read` ＝ 本次 WebFetch/WebSearch/curl 真的抓到页面并摘出原句；`ai_draft` ＝ 只见于搜索摘要或无 1660 年代数据，**不得进 prompt、不得进口播数字**。
> 年代差标注：`Δ0` ＝ 1660–1670 年当期；`Δ±N` ＝ 与 1666 年相差 N 年，**一律 ⚠️**。

---

## §7 物价与货币

### 7.1 1666 年伦敦人口袋里到底是什么钱

#### A. 记账单位（这部分零争议）

| 单位 | 换算 | 备注 |
|---|---|---|
| pound £ | 20 shillings | **只是记账单位，市面上没有「一镑」这枚硬币** |
| shilling s. | 12 pence | 银币，日常大额 |
| penny d. | 4 farthings | 日常基本单位 |
| farthing | 1/4 d. | 最小单位 |
| groat | 4 d. | 1662 年后停铸 |
| mark | 13s 4d | 只用于记账／法律文书，非硬币 |

#### B. 真正在流通的硬币（三条会让记者当场尴尬的事实）

1. **金几尼（guinea）是全新的东西。** 第一枚几尼 **1663 年 2 月 6 日**开铸，**1663 年 3 月 27 日**公告成为法定货币（`money.001`）。它**名义上等于 20 先令，但金价上涨使它在市面上溢价交易**——1666 年当年皮普斯的金匠告诉他：他不久前买 2000 枚几尼只贴 **18½ 便士**的兑换费，**现在要 22 便士，而且几乎买不到**（`money.002`，1666-11-29，T0）。12 月 12 日他再买，贴水已到 **22½ 便士**（`money.003`）。→ **旅行者带金币 ＝ 带一件正在涨价的商品，不是带钱。**

2. **铸币正在从「锤打」换成「机制」。** 1662 年 2 月起金币先上机器，银币在随后一年多陆续铺开；机制币有**边齿与边铭**，目的就是防止「剪边」（`money.004`）。但**1666 年市面上仍大量混着旧的锤打银币，边缘被剪过、成色参差**——收钱的人会掂、会看边。

3. **【最重要】小额零钱根本不够用，伦敦靠「商人自铸的代币（token）」找零。**
   - 王室长期不管小面额：「The King took little interest in providing small denomination coinage」，内战后议会同样不管，于是「ordinary tradesmen and even some town authorities start[ed] issuing their own low denomination token coinage (principally farthings, half pennies and pennies)」（`money.005`，T1）。
   - 规模：**1648/9–1672 年间，仅老城墙以内就发行了 4000 种以上的模铸代币**，算上城外「the overall number of token varieties … may well have been double」（`money.007`，T1）。
   - 面额与形制：**farthing 直径 14–16 mm（最早）／halfpenny 17–20 mm（1656 年起，1664 年起成为主力面额）／penny 14–25 mm（1663 年起，咖啡馆尤其大量发行）**；材质是**薄铜片或黄铜片冲压**，极少数锡、皮革（`money.008`，T1）。
   - **致命限制：代币只在发行者自己店里兑现，「not widely circulated beyond the local district in which they were issued」**（`money.009`，T1）。→ **在齐普赛街收的代币，拿到南岸就是废铜。**
   - 咖啡馆代币：1663–1672 年约 **80 种**，其中**至少一半集中在 1669–1671**（`money.010`，T1）。1666 年当天能见到的多数还是 halfpenny 代币。
   - 结局：**1672 年查理二世下令取缔，改发王室铜质 halfpenny 与 farthing**（`money.006`，T1）。

#### C. 旅行者该带什么钱（演绎结论，非史料）

**带银先令与六便士银币 ＋ 一小把当地铜代币**。不要带金几尼（要贴水、找不开、显眼）；不要带任何纸币（英格兰银行 1694 年才成立，1666 年英国没有银行券）。**口播梗：「我兜里这堆铜片，出了这条街就不是钱了。」**

---

### 7.2 两个锚

#### 锚 A · 面包 —— **价格锁死，重量浮动**

这是英国物价制度和中国最不一样的一点，必须在开场讲清：

> **Assize of Bread（面包法定价）不是规定「一条面包卖多少钱」，而是反过来——先钉死「一便士就是一便士」，再按小麦价规定这一便士的面包该有多重。** 「the price of bread was always the same, even though the price of grain fluctuated; instead, when the price of grain increased, the weight of bread was reduced accordingly」（`price.001`，T2）。

- 所以伦敦街上的基本单位就是 **penny loaf（一便士面包）**。皮卡德《Restoration London》（专写 1660 年代伦敦）：**「for a penny you could buy a pound of the cheapest sorts of cheese, or a loaf of bread (price controlled in the city of London)」**（`price.002`，T2，Δ0）。
- **重量到底多少？** 1666 年当年的数字**没查到**。最近的两个官方口径：
  - 伦敦市政记录（Remembrancia 索引）：**1618 年 1 月的「penny wheat loaf」为 13 盎司，此后因小麦价回落四次上调，到 1619 年 1 月为 17 盎司**——「raised four times since January, 1618, as the price of wheat had abated … from thirteen ounces the penny wheat loaf to fourteen, fifteen, sixteen, and finally to seventeen ounces」（`price.003`，T0 转录，**Δ−47 ⚠️**）。同页另记：荒年时「bakers were barely able to maintain eleven ounces weight in the wheaten penny loaf」。
  - 斯特赖普《伦敦志》1720 年版记 Household Bakers 与 Bakers 的差额：**penny white loaf 多 1 盎司、halfpenny wheaten 多 1 盎司、penny wheaten 多 2 盎司、penny household 多 2 盎司、twopenny household 多 4 盎司**（`price.004`，T0，**Δ+54 ⚠️**）。
- **本片采用**：`一便士面包 ＝ 主食基准单位`，重量口播为 **「大约一磅上下」并明示这是区间**（1618–19 年的 13–17 盎司 ≈ 370–480 g，⚠️ 年代差）。**不要在片中报一个精确克数。**

> **锚 A 一句话**：**一便士，一条面包。价格永远是一便士——变的是它有多大。**

#### 锚 B · 日工钱 —— 两档都给

伦敦建筑工地是唯一有连续数字的地方。**1666 年前后最接近的一次点名记账**：

> 王室工务局（Office of the King's Works）**1660 年**的伦敦塔与白厅账目仍逐人记名：「Their day rates ranged from **24d. to 30d.** as Hutchins' found, and the **labourers rate was 16d.**」（Stephenson, LSE 经济史工作论文 231，`work.001`，T1，**Δ−6**）。

| 档位 | 日工钱 | 出处 | 年代差 |
|---|---|---|---|
| **非技术劳工 labourer** | **16 便士（1s 4d）** ← **全片分母** | 王室工务局 1660 年账，`work.001` | Δ−6 |
| **技术工匠 craftsman（石匠／木匠）** | **24–30 便士（2s–2s 6d）**，取 **30d** 作上档 | 同上 `work.001` | Δ−6 |
| 交叉印证（同期手册） | 砌砖工 **36d**、其小工 **20d** | Primatt《The City & Country Purchaser and Builder》**1667 年** → Allen 2017，`work.002` | **Δ+1（最近！）** |
| 交叉印证（同期市价区间） | 工匠 **24–36d**、劳工 **14–24d** | Boulton 的 1670 年挂牌区间 → Stephenson，`work.003` | Δ+4 |
| 后续定盘 | 圣保罗大教堂 1675 年核定木匠／砌砖／石匠 **2s 6d（30d）**，直到 1711 年后才涨 | Stephenson，`work.004` | Δ+9 |
| 更早基线 | 1614 年 工匠 20d／劳工 14d | Boulton 序列 → Stephenson，`work.005` | Δ−52 ⚠️ |

**必须加的一句谨慎**（斯蒂芬森全文的论点）：**这些「day rate」是承包商向业主开的价，不是工人到手的钱；扣掉承包商利润，实际到手比账面低两三成**——「The actual wages paid to London building workers were twenty to thirty per cent below current estimates」（`work.006`，T1）。→ **口播可以说「一个小工一天挣一先令四便士」，但补一句「这还是包工头报给账房的价，真进他口袋的更少」。**

> **锚 B 一句话**：**小工一天 16 便士 ＝ 16 条面包。工匠一天 30 便士 ＝ 30 条面包。**
> 这是本站最好的开场：**「在 1666 年的伦敦，一天工钱，就是一天能买几条面包——小工 16 条，工匠 30 条。记住这两个数，今天所有价格你都能自己算。」**

---

### 7.3 商品与服务价格（≥ 10 件，全部换算「几天工钱」）

说明：`天` 一律 ＝ 价格(便士) ÷ **16**（非技术劳工）。括号内为工匠口径（÷30）。

**价格表（§7 收尾表）**

| # | 商品／服务 | 价格（原币） | ÷ 日工钱 ＝ 几天工钱 | 出处 fact_id | 年代差标注 |
|---|---|---|---|---|---|
| 1 | **一条面包（penny loaf）** | 1d | **0.06 天**（工匠 0.03） | `london1666.price.002` | Δ0 ✅ |
| 2 | 一磅最便宜的奶酪 | 1d | 0.06 天 | `london1666.price.002` | Δ0 ⚠️T2 |
| 3 | 一条比目鱼 | 2d | 0.13 天 | `london1666.price.005` | Δ0 ⚠️T2 |
| 4 | 一磅黄油 / 一品脱奶油 | 4d（a groat） | 0.25 天 | `london1666.price.005` | Δ0 ⚠️T2 |
| 5 | 一磅培根 | 9d | 0.56 天 | `london1666.price.005` | Δ0 ⚠️T2 |
| 6 | 一只鸡 / 一品脱牡蛎 / 半磅胡椒 | 1s（12d） | 0.75 天 | `london1666.price.005` | Δ0 ⚠️T2 |
| 7 | **咖啡馆入场（含一碗咖啡）** | **1d** | **0.06 天** | `london1666.price.006` `.007` | Δ0 ✅ |
| 8 | 一夸脱 ale（酒馆散卖） | 1266 年法定上限 1d／夸脱；18 世纪初实卖 2½d／夸脱 | 0.06–0.16 天 | `london1666.price.008` | **Δ−400 / Δ+40 ⚠️⚠️ 区间推定，不得口播单一数字** |
| 9 | 酒馆一顿「ordinary」（定食） | 1s 6d（18d） | 1.13 天 | `london1666.price.009` | Δ0 ⚠️T3 |
| 10 | **皮普斯在酒馆请客的一笔实账** | **2s 6d（30d）** | **1.88 天** | `london1666.price.010` | Δ0 ✅T0（1666） |
| 11 | 三条鳗鱼（泰晤士河边现买，火灾前） | **3s（36d）** | **2.25 天** | `london1666.price.011` | Δ0 ✅T0（1666-06-13） |
| 12 | **两条鳗鱼（同一条河，火灾第七天）** | **6s（72d）** | **4.50 天** | `london1666.price.012` | Δ0 ✅T0（1666-09-08）**火后涨价实证：单价约 1s → 3s** |
| 13 | **渡河船资 waterman（横渡）** | wherry 整船 1d / sculler ½d | 0.06 / 0.03 天 | `london1666.transport.001` | **Δ−110 ⚠️**（16 世纪费率） |
| 14 | 河上一趟（格林尼治，顺流／逆流） | 8d / 12d | 0.5 / 0.75 天 | `london1666.transport.002` | **Δ−107 ⚠️**（1559 费率） |
| 15 | **雇佣马车 hackney coach（第一小时）** | **18d** | **1.13 天** | `london1666.transport.004` | Δ−4 ✅T0（1662 法令） |
| 16 | 雇佣马车（其后每小时） | 12d | 0.75 天 | `london1666.transport.004` | Δ−4 ✅T0 |
| 17 | **雇佣马车（包一天 ＝ 12 小时）** | **10s（120d）** | **7.50 天** | `london1666.transport.004` | Δ−4 ✅T0 |
| 18 | 马车：律师学院 → 威斯敏斯特／皇家交易所 | 12d | 0.75 天 | `london1666.transport.005` | Δ−4 ✅T0 |
| 19 | 马车：律师学院 → 伦敦塔／主教门／阿尔德门 | 18d | 1.13 天 | `london1666.transport.005` | Δ−4 ✅T0 |
| 20 | 一双长袜（普通） | 5s（60d） | 3.75 天 | `london1666.price.013` | Δ0 ⚠️T2 |
| 21 | 一双丝袜 | 15s（180d） | 11.25 天 | `london1666.price.013` | Δ0 ⚠️T2 |
| 22 | **一双男靴** | **£1 10s（360d）** | **22.5 天**（工匠 12 天） | `london1666.price.014` | Δ0 ⚠️T2 |
| 23 | 皮普斯买的一件骑装外套 | 30s（360d） | 22.5 天 | `london1666.price.015` | Δ0 ✅T0（1666-07-17） |
| 24 | 一顶天鹅绒骑马帽 | 20s（240d） | 15 天 | `london1666.price.016` | Δ0 ✅T0（1666-11-29） |
| 25 | **一本书（皮普斯 1666 年的 Ogilby 大开本）** | **£4 另加装订** | **60 天** | `london1666.price.017` | Δ0 ✅T0（1666-02-19） |
| 26 | 一本带银饰的《圣经》（书 9s6d＋做工 6s6d＋银 7s6d） | £1 3s 6d（282d） | 17.6 天 | `london1666.price.018` | Δ−6 ✅T0（1660） |
| 27 | **剧院正厅（pit）一个座** | **2s 6d（30d）** | **1.88 天** | `london1666.price.019` | Δ+3 ⚠️（1669 记载） |
| 28 | 理发师刮一次脸（上限） | 3d | 0.19 天 | `london1666.price.020` | ⚠️ **ai_draft，年代不明，不得口播** |
| 29 | 一晚客栈住宿 | **未查到 1660 年代数字** | — | `london1666.price.021` | ❌ ai_draft，**待补** |
| 30 | 一张《死亡周报》（Bills of Mortality） | 约 1d | 0.06 天 | `london1666.price.022` | Δ−1 ⚠️T2（1665–66） |
| 31 | **煤（伦敦零售，1655 年）** | **常在 20s 一 chaldron 以上（240d+）** | **15 天以上** | `london1666.price.023` | Δ−11 ⚠️ |
| 32 | 接生＋洗礼整套（接生婆 20s／奶妈 10s／女仆 2s6d／马车 5s） | 近 40s（480d） | 30 天 | `london1666.price.024` | Δ0 ✅T0（1666-11-18） |

**这张表里最该进片子的三条对比：**
1. **咖啡 1 便士 ＝ 面包 1 条 ＝ 小工 1/16 天。**「一便士能读一天报、听一天八卦」——所以咖啡馆叫 penny universities。
2. **雇一小时马车（18d）＞ 小工一整天工钱（16d）。** 一句话说尽阶级：**「他坐一个钟头车，花的比我干一天挣的还多。」**
3. **一双靴子 22.5 天工钱。** 穷人不穿靴，穿破鞋或光脚——这条直接决定服化道。

---

## §6 行（1666-09-01 的伦敦怎么移动）

### 6.1 走路（默认）
城墙内直径约一英里多，**绝大多数人一辈子靠走**。1662 年法令还规定：**每户人家必须在自家门前扫街，「twice every weeke … on every Wednesday and every Saturday」**（`transport.010`，T0）。**9 月 1 日正是周六——街上到处是在自家门口扫地的人**，这是当天最好用的一个环境细节。清道夫（scavengers）的车**除周日外每天来**，来时要出声吆喝。

### 6.2 泰晤士河 —— 真正的主干道
- **伦敦桥是全城唯一的桥**：「Down to about the middle of the seventeenth century … the Thames had formed the great medium of metropolitan conveyance」（`transport.006`，T1）。过河、沿河，全靠船。
- **两种船**：**oars**（两名船夫的 wherry）与 **sculler**（一人一桨，便宜一半）。皮普斯 1666 年亲历：**「by an old poor man, a sculler, having no oares to be got」**（`transport.007`，T0）——**oars 抢手时才退而求其次坐 sculler**，这个鄙视链可以直接演。
- **费率**（⚠️ 都不是 1666 当年）：16 世纪横渡 wherry 整船 1d、sculler ½d（`transport.001`）；1559 年格林尼治顺流 8d、逆流 12d，**逆水加价五成**（`transport.002`）；18 世纪通行口径「the usual fare being **sixpence for a pair of oars and three pence for sculls**；到兰贝斯／沃克斯霍尔 1s，到切尔西／巴特西／万兹沃思 1s 6d」（`transport.003`，⚠️ Δ+50 上下）。**片中口播只说「过一次河，几个便士」，不要报精确数。**
- **「shooting the bridge」**（从伦敦桥的桥洞冲过去）极危险，「a number of people drowned in the attempt」，讲究的人在桥一边下船、走过去、另一边再上船（`transport.008`，T1）。
- **开工时间**：市政 1634 年规定船夫**夏天 5 点、冬天 7 点**必须到自己的码头待客（`transport.009`，T1）。
- **人数：必须辟谣。** 斯托（1598）与「水上诗人」约翰·泰勒都留下「四万」这个数——但那是**连家属和依附行业一起算**的说法；同一批史料里，**斯托另记伦敦、威斯敏斯特与南岸「3,000 人、2,000 条 wherry」，1629 年海军部普查只得 2,426 名船夫**（`transport.011`，T1）。**本片口径：真正摇橹的是数千人量级，是全城最大的单一行业之一；「四万」要说成「当时人自己吹的数」。**
- **1666 年独有的变量——抓壮丁。** 第二次英荷战争打到 1666 年，海军强征（press）大量抓船夫。皮普斯 1666 年：**「thinking to go by water, but could not get watermen; they being now so scarce, by reason of the great presse」**（`transport.012`，T0）。→ **9 月 1 日的码头上，船比往年少、船夫年纪偏大、要价硬。这是本站最好的「当天真实摩擦」。**

### 6.3 雇佣马车 hackney coach —— 1662 年刚被牌照化
**1662 年法令（13 & 14 Car. II c. 2）逐条硬数据（全部 T0）**：
- **发牌上限 400 辆**：「the number to be licensed shall not exceed Foure hundred」（`transport.013`）。
- **年费 £5**：「shall pay … the yearely Rent of five pounds」（`transport.013`）。
- **费率上限**：「above the rate of **ten shillings for a day reckoning twelve houres to the day** and by the houre **not above eighteen pence for the first houre and twelve pence for every houre after**」（`transport.004`）。
- **按段计价**：律师学院一带 → 圣詹姆斯或威斯敏斯特 **12d**；→ 皇家交易所 **12d**；→ 伦敦塔／主教门／阿尔德门一带 **18d**（`transport.005`）。
- **超收罚 10 先令**：「he shall for every such offence forfeit the summ of ten shillings」（`transport.014`）。
- 监管机构是「Commissioners … for the Licensing and Regulating of Hackney Coaches」。
- **1666 年当场可见**：大火期间**「the hackney-coaches now standing at Allgate」**（皮普斯 1666-09-10，`transport.015`，T0）——城里烧了，马车站挪到阿尔德门外。

### 6.4 轿子 sedan chair
**1634 年 Sir Saunders Duncombe 取得 14 年专营，把可雇轿子引入伦敦**；比马车便宜、**能进马车进不去的窄巷**，常常是城里最快的走法（`transport.016`，T2）。皮普斯 1663-02-16 记 Sir W. Wheeler 因痛风被轿子抬下楼。**⚠️ 轿子费率只有 18 世纪数字（1760 年：一英里以内 1s；城内一趟 6d；包一天 4s；午夜后加倍），Δ+94，不得当 1666 年价用。**

### 6.5 货运／搬家 —— 只在灾变日出现的「浮动定价」
大火当天皮普斯亲见：**「the streets and the highways are crowded with people running and riding, and getting of carts at any rate to fetch away things」**（1666-09-03，`transport.017`，T0）。**「at any rate」＝ 要多少给多少**。**这是 9 月 2 日之后才出现的，9 月 1 日当天不能用**——但可以作为片尾「明天会发生什么」的钩子。

---

## §8 职业与社会阶层（8 种人，含 1 官吏 / 1 商贩 / 1 女性劳动者 / 1 底层）

### 8.1 面包师 —— Thomas Farriner（布丁巷）【当天的主角】
- 生卒 **c.1615 – 1670-12-20**；**1637 年入面包师同业公会（Bakers' Company）**，**1649 年起有自己的店**；教区教会执事（churchwarden）（`work.010`，T2）。
- **给海军供面包／干粮**，被称作「the King's baker」——正打第二次英荷战争，是战时订单（`work.011`，T2）。
- **作息**：面包师是夜班工种——傍晚起炉、整夜烤、清晨出炉。**9 月 1 日周六这一天他在正常营业；当夜炉子没有彻底熄。**
- **2 日凌晨约 1 点**起火：「in the early hours of 2 September 1666, in his house on Pudding Lane, Farriner was awakened by smoke billowing under the door of his bedroom」；他和女儿从楼上窗户逃出，**女仆不敢跳，死了**（`work.012`，T2）。
- **给 9 月 1 日的用法**：记者在布丁巷买一条一便士面包 → 报价格锚 → 顺手拍到烤炉 → **观众知道、他不知道**。这是本站的结构性反讽，**但 9 月 1 日当天不要让任何人预告火灾**。

### 8.2 煤炭搬运工 coal heaver 【火的燃料，也是底层重活】
- 伦敦烧的是**纽卡斯尔海运煤（sea-coal）**。**1660 年代进煤量已是 1605–6 年的三倍以上，1700 年超过 46 万吨**（`work.013`，T2）。
- **1655 年伦敦煤价「usually above 20s. a chaldron」，运煤车 420 辆归基督公学管，所有量器要在市政厅打封**（`work.014`／`price.023`，T0 转录，Δ−11）。
- **干活方式**：煤船太大靠不了岸，停在比林斯盖特附近的 Pool，**驳船／lighter 接驳**；承包商（coal undertakers，多半是酒馆老板）**按「帮」雇人，一帮通常 9 人**（4 人在舱内、4 人绞上来、1 人守筐）＋一名量煤官和他的助手，**卸空一船要 5–7 天**；报酬**每二十 chaldron 各得 3 先令**（`work.015`／`work.034`，⚠️ 该描述出自 18 世纪，Δ+100，**数字不得口播**）。领了钱还得回承包商的酒馆里喝贵酒，才保得住明天的活。
- **和火的关系（必须讲）**：**泰晤士街沿河全是煤与可燃货栈**——「riverfront warehouses were packed full with flammable materials such as tallow for candles, lamp oil, spirits, and coal」，当时人描述这一带是「old paper buildings and the most combustible matter of **Tarr, Pitch, Hemp, Rosen, and Flax**」，码头上堆着木材与煤（`work.016`，T2）。
- **给 9 月 1 日的用法**：沿河走一段，镜头交代煤堆、焦油桶、木料垛。**只呈现，不预告。**

### 8.3 船夫 waterman 【全城最庞大的行业之一】
见 §6.2。补充职业层面：
- **同业公会 1555 年成立**；**要先摇两年船才准独自掌一条 wherry**；**师徒制**（`work.017`，T1）。
- 18 世纪末的名册规模：**12,283 人（8,283 名自由人、2,000 名非自由人、2,000 名学徒），每年收学徒 200–300 名**（`work.018`，T0 转录，⚠️ Δ+130，只用于说明「这是一个巨大行业」）。
- **1666 年当年：被海军强征（见 `transport.012`）。** 船夫是被抓壮丁的第一顺位——会划船的人正是海军要的人。**片中船夫可以抱怨「我兄弟上个月被拉上船了」。**
- 着装要点：**自由人船夫有带徽章的臂章／号衣**（公会与主家的标记），普通渡船夫是粗麻布衫、赤脚或简陋皮鞋、手掌厚茧。

### 8.4 酒馆／咖啡馆里的女性从业者 【女性劳动者】
- **数量级**：1577 年普查（不含城内）在米德尔塞克斯记到 **720 家 alehouse ＋ 132 家 inn，约每 76 人一家**；1610 年有人称伦敦近郊「四户里有一户是 alehouse」；**1620 年查令十字到坦普尔栅之间将近 100 家 tavern**；**1641 年，法灵顿外区、波索肯这类穷的城外区每 6 户就有 1 户是卖酒的，富的中心区（阿尔德门、康希尔）是 1/30–1/40**（`work.019`，T1）。
- **女性角色**：女业主、tapster（打酒的）、帮佣；许多 victualling house 是穷寡妇在家里开的营生。
- **咖啡馆则相反**：第一家 1652 年由 Pasqua Rosée 开在康希尔圣米迦勒教堂墙边；**到 1663 年，光是罗马城墙以内就至少开了 82 家**（`work.020`，T1）。但**「No respectable women were seen in coffeehouses as customers」**（`work.021`，T1）——**女人可以在里面端咖啡、可以是老板娘，但不作为顾客坐下**。1674 年还出了《Women's Petition Against Coffee》抱怨丈夫泡咖啡馆。
- **给片子的处理**：记者进咖啡馆，镜头带过柜台后的女性；**口播明说这条性别边界**，这是本站最好的一处社会观察。

### 8.5 学徒 apprentice 【最没有自由的一档】
- **标准 7 年期，14–21 岁入行**，是取得市民资格（freedom of the City）的正路；**约四分之一的人实际服役更久**（`work.022`，T1）。
- **1660 年代伦敦男性有一半不到 25 岁；学徒工时极长、普遍抱怨没有闲暇与人身自由**（`work.023`，T1）。⚠️「早六点到晚八点」这个具体时刻表**没查到 1660 年代出处，不得口播**。
- 学徒住在师傅家里，吃师傅的饭、穿指定的简朴衣服（不许戴假发、不许配剑）；**周六是最长的一天**。
- 街头治安意义：学徒是伦敦街头骚乱的主力人群——**一群十七八岁的男性劳动力聚在一起**。

### 8.6 市政／官吏 —— 教区 constable、ward beadle、更夫【必配的官方视角】
**关键认知：1666 年伦敦没有警察，「官」多数是被轮到的邻居。**
- **1663 年 10 月的市政会法令（以当任市长得名「Robinson's Act」）确认：城内所有户主都要轮值守夜，「to keep the peace and apprehend night-walkers, malefactors and suspected persons」**（`work.024`，T1）。
- **到 1660 年代，花钱雇人代班已是常态**；越来越多是**户主凑钱进一个「守夜基金」，由区里的 beadle 或 constable 雇人**（`work.025`，T1）。
- **更夫在查理二世治下得了个绰号「Charlies」**（`work.026`，T1）。
- **腐败点**：beadle 和 constable 负责收这笔守夜钱，**常被指控尽量少雇人、把差额揣进自己口袋，当作自己那份无薪公职的补偿**（`work.027`，T1）。
- **着装／道具**：beadle 有区里的制服与权杖；更夫提灯、带长棍（bill）、按点报时喊话。
- **给片子的用法**：这是「猜价格」卡之外的第二个反常识点——**「这位大爷不是警察。他是这条街上被轮到值夜的邻居，而且他多半是花钱请来的替班。」**

### 8.7 街头小贩 hawker / crier【商贩】
- 伦敦街头叫卖的货：**「water, coal, matches, singing birds, oysters, fat chickens, strings of onions」**（`work.028`，T1）。
- **女性尤其集中在这一行**；17 世纪伦敦当局受理过「poore woemen selling milke」「pore woman Fruterers」「ancient poore fishwifes」的陈情（`work.029`，T1）。
- **图像依据**：Marcellus Laroon《The Cryes of the City of London drawne after the Life》，Pierce Tempest 出版，**74 幅**，画的是**17 世纪末**的伦敦街头人物与他们的吆喝词（`work.030`，T1，**Δ+21 ⚠️——服装与器物可参考，但要知道晚了 21 年**）。
- **和物价的接口**：小贩是「猜价格卡」最自然的载体——**一条比目鱼 2d、一只鸡 1s**（见价格表）。

### 8.8 清道夫／掏粪工 scavenger, raker, nightman【底层】
- **1662 年法令**（同一部管马车的法）规定：**户主每周三、周六清扫自家门前**；**清道夫的车每天（周日除外）来，来时要出声通知**，负责把污物运走，违者受罚（`work.031`／`transport.010`，T0）。
- 伦敦的粪秽由「nightmen／gold-finders」夜间清掏——**只准夜里干活**，是全城地位最低、气味最重的一档。
- **9 月 1 日是周六**，所以**当天的街道基线是「刚被扫过／正在扫」**——这条直接写进镜头环境。

### 8.9 阶层速查（用于选角与服化道）

| 档 | 代表 | 一天进项 | 穿什么 | 9 月 1 日（周六）在干什么 |
|---|---|---|---|---|
| 底层 | 清道夫、掏粪工、码头散工 | ≤ 16d，且不是天天有活 | 粗麻、破鞋或赤脚、无帽 | 扫街、卸货、等活 |
| 非技术劳工 | 建筑小工、煤炭搬运工 | **16d** | 粗布罩衫、皮围裙、扁帽 | 河边卸煤；建筑工地 |
| 技术工匠 | 石匠、木匠、船夫（自由人）、面包师 | **24–30d** | 好些的毛料、皮鞋、有行会标记 | 面包师在烤；船夫在码头候客 |
| 小铺主／咖啡馆主 | 发代币的那批人 | —（有店面、有信用） | 干净亚麻领、呢外套 | 开门做周六生意、清点自家代币 |
| 学徒 | 各行 14–21 岁 | 0（管吃住） | 师傅指定的简朴服，不许假发佩剑 | 干到天黑 |
| 市政轮值 | constable、beadle、更夫 | 无薪／代班费 | beadle 有制服权杖；更夫提灯带棍 | 白天收守夜钱，夜里上岗 |
| 女性劳动者 | 酒馆 tapster、小贩、女仆 | 低且常为实物 | 围裙、头巾、木屐 | 打酒、沿街叫卖 |
| 上层 | 商人、官员（皮普斯这一档） | 雇一小时马车就花掉小工一天 | 假发、剑、马车 | 皮普斯本人 9 月 1 日：办公、看木偶戏、去伊斯灵顿吃喝 |

**皮普斯 1666 年 9 月 1 日（周六）原文（T0，本站的时间锚）**：
> 「September 1st. Up and at the office all the morning, and then dined at home. Got my new closet made mighty clean against to-morrow. Sir W. Pen and my wife and Mercer and I to "Polichinelly," but were there horribly frighted to see Young Killigrew come in with a great many more young sparks; but we hid ourselves … and so, the play being done, we to Islington, and there eat and drank and mighty merry; and so home singing, and, after a letter or two at the office, to bed.」（`work.032`）

**这段是全片的黄金素材**：**大火前最后一个白天，一个中产官员在看木偶戏、在伊斯灵顿吃喝、唱着歌回家。**

---

## 片子结构件（交给编剧直接用）

### A. 开场「两个物价锚」口播稿（30 秒内讲完）
> 「1666 年 9 月 1 日，伦敦。进城之前先记两个数。
> **第一个：一便士，一条面包。** 这里的面包价格是官方钉死的——永远一便士，涨价的方式是**把面包做小**。
> **第二个：一天工钱。** 一个不会手艺的小工，一天 **16 便士**；一个石匠木匠这样的手艺人，一天 **30 便士**。
> 所以：**小工一天 ＝ 16 条面包。工匠一天 ＝ 30 条面包。**
> 今天我花的每一笔，我都换算成『几天工钱』给你听。」

### B. 「猜价格」停顿卡（≥1 张，这里给 3 张备选）
1. **【推荐】**「雇一辆马车，坐**一个钟头**。你猜多少钱？」→ 停 3 秒 → **「18 便士。比一个小工干一整天挣的（16 便士）还多。」**（T0 法令价，最硬）
2. 「一杯咖啡，外加坐一整天、看报、听八卦。你猜多少？」→ **「1 便士。跟一条面包一样。所以他们管咖啡馆叫『一便士大学』。」**
3. 「一双男人的靴子。你猜要干多少天？」→ **「22 天半。所以你在街上看不到几个人穿靴子。」**

### C. 片尾「今日总账单」模板（数字全部可换，出处已锁）

| 项目 | 花了 | ÷16d ＝ 几天小工工钱 | fact_id |
|---|---|---|---|
| 早市一条面包 | 1d | 0.06 天 | `price.002` |
| 渡河一趟（sculler） | ½d–1d | 0.03–0.06 天 | `transport.001` ⚠️ |
| 咖啡馆坐一上午 | 1d | 0.06 天 | `price.006` |
| 一条比目鱼（给船夫） | 2d | 0.13 天 | `price.005` |
| 酒馆一顿 ordinary | 18d | 1.13 天 | `price.009` ⚠️ |
| 雇马车一小时（回威斯敏斯特） | 18d | 1.13 天 | `transport.004` |
| 一夸脱 ale | 1–2½d | 0.06–0.16 天 | `price.008` ⚠️ |
| **合计** | **约 3 先令 5 便士（41d）** | **约 2.6 天小工工钱／1.4 天工匠工钱** | |

**收尾口播**：「一天当游客，花掉一个小工**两天半**的工钱。而这些钱里最大的一笔，是那一个钟头的马车。」

---

## §13 物价／行／职业 类误传（`tag: ❌`，只进「记者踩坑」与负向词）

| myth_id | 误传 | 正解 | negative（prompt 负向词） |
|---|---|---|---|
| `myth.money.001` | 掏出**纸币／银行券**付账 | 英格兰银行 1694 年才成立；1666 年没有任何纸钞 | 纸币、banknote、钞票、支票 |
| `myth.money.002` | 一把**统一制式的铜便士**随便花 | 王室不铸小钱；靠**商人自铸代币**，且出了本街区就不认 | 统一制式铜币、现代硬币、机制铜分币 |
| `myth.money.003` | **金几尼 ＝ 20 先令，随便花** | 1663 年才有，1666 年在溢价交易且缺货 | 大把金币付小账 |
| `myth.money.004` | 「一先令 ＝ 今天多少元」 | **本片只用「几天工钱」** | —（口播禁语） |
| `myth.price.001` | 面包**涨价**了 | 价格钉死，**变的是重量** | 面包标价牌、写着不同价格的面包 |
| `myth.transport.001` | 泰晤士河上有**好几座桥** | **只有伦敦桥一座**；河上密密麻麻全是小船 | 多座桥、石拱桥群、塔桥 |
| `myth.transport.002` | 出租马车**满街都是** | **全城合法牌照上限 400 辆**，且窄巷进不去 | 成排马车、车水马龙的四轮马车 |
| `myth.transport.003` | 船夫有**四万人** | 那是含家属的老说法；实际摇橹者数千人量级 | —（口播纠偏） |
| `myth.work.001` | 街上有**警察／制服治安队** | 只有轮值户主、雇来的替班更夫与区里的 beadle | 警察、制服警队、警徽、现代警棍 |
| `myth.work.002` | 女人**坐在咖啡馆里喝咖啡** | 体面女性不作为顾客进咖啡馆（可以是老板娘／端咖啡的） | 女顾客围坐咖啡馆、男女混坐喝咖啡 |
| `myth.work.003` | 1666 年的伦敦人**烧木柴** | 伦敦烧的是**纽卡斯尔海运煤 sea-coal**，城市终年煤烟 | 纯木柴炉、无烟洁净空气 |

---

## fact YAML（机检用）

```yaml
- fact_id: london1666.price.001
  claim: 英国面包法定价（Assize of Bread）钉死的是价格不是重量——小麦涨价时，减的是同一便士面包的分量
  tag: ✅
  source: Wikipedia, Assize of Bread and Ale（经济史通说，与 Remembrancia、Strype 原始记载交叉核对）
  source_url: https://en.wikipedia.org/wiki/Assize_of_Bread_and_Ale
  quote: "the price of bread was always the same, even though the price of grain fluctuated; instead, when the price of grain increased, the weight of bread was reduced accordingly"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "面包铺木案上一排大小不一的圆麦面包，价签只写一便士"
  negative: "多种价格的价签、现代烘焙柜、切片吐司、塑料包装"

- fact_id: london1666.price.002
  claim: 1660 年代伦敦，一便士买得到一条面包（城内价格受管制），或一磅最便宜的奶酪
  tag: ✅
  source: Liza Picard《Restoration London》（1660 年代伦敦日常生活专著）经 pepysdiary.com 读者转述
  source_url: https://www.pepysdiary.com/diary/1660/02/04/
  quote: "According to Liza Picard's Restoration London, for a penny you could buy a pound of the cheapest sorts of cheese, or a loaf of bread (price controlled in the city of London)."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "手心里一枚磨旧的铜便士，旁边是一条粗麦圆面包"
  negative: "银币付面包、纸币、现代硬币、找零收银机"

- fact_id: london1666.price.003
  claim: 伦敦「一便士小麦面包」的法定重量按小麦价浮动——1618 年 1 月为 13 盎司，其后四次上调，到 1619 年 1 月为 17 盎司；荒年时曾勉强维持 11 盎司
  tag: ⚠️
  source: Analytical Index to the Remembrancia（伦敦市政记录索引）1579–1664，Provisions, corn etc.
  source_url: https://www.british-history.ac.uk/no-series/index-remembrancia/1579-1664/pp372-391
  quote: "raised four times since January, 1618, as the price of wheat had abated … from thirteen ounces the penny wheat loaf to fourteen, fifteen, sixteen, and finally to seventeen ounces"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "面包师把一条圆面包放上铜盘天平，另一端是砝码"
  negative: "电子秤、克数标签、现代烤盘"

- fact_id: london1666.price.004
  claim: 伦敦「家用面包师」(Household Bakers) 的便士白面包须比普通面包师的重 1 盎司，便士 wheaten 重 2 盎司，两便士 household 重 4 盎司；对照表挂在市政厅长廊
  tag: ⚠️
  source: John Strype, A Survey of the Cities of London and Westminster (1720), Book 5（Strype Online）
  source_url: https://www.dhi.ac.uk/strype/TransformServlet?page=book5_339
  quote: "shall weigh one Ounce more in every Loaf than the Bakers of the same Towns Penny White Loaves do"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "市政厅长廊墙上挂着一张手写的面包重量对照表"
  negative: "印刷海报、现代排版、二维码"

- fact_id: london1666.price.005
  claim: 1660 年代伦敦零售：比目鱼 2d；一磅黄油或一品脱奶油 4d；一磅红糖 5d；一磅培根 9d；一只鸡／一品脱牡蛎／半磅胡椒各 1 先令
  tag: ⚠️
  source: Liza Picard《Restoration London》经 pepysdiary.com 转述
  source_url: https://www.pepysdiary.com/diary/1660/02/04/
  quote: "For tuppence you could buy a flounder. A pound of butter or a pint of cream cost a groat (4 pence). … A chicken cost a shilling, as did a pint of oysters or half a pound of pepper."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "街边摊板上摊着扁鱼、一篮牡蛎、一只拔了毛的鸡"
  negative: "辣椒、番茄、土豆堆成山、塑料筐、冰块保鲜"

- fact_id: london1666.price.006
  claim: 伦敦咖啡馆入场费一便士，这一便士就包含一碗咖啡，故称「一便士大学」
  tag: ✅
  source: The Public Domain Review, "The Lost World of the London Coffeehouse"
  source_url: https://publicdomainreview.org/essay/the-lost-world-of-the-london-coffeehouse/
  quote: "The entry fee was one penny"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "咖啡馆门口的木柜台上放一枚铜币，屋里长桌坐满男人在读报"
  negative: "女顾客坐着喝咖啡、外带纸杯、咖啡机、拉花"

- fact_id: london1666.price.007
  claim: 一便士的入场费换来的是：进得来一间生好火、有家具的屋子，一碗热咖啡和一斗填满的陶烟斗
  tag: ✅
  source: Mr. Pepys' Small Change — London Coffee House Tokens
  source_url: https://c17thlondontokens.com/category/london-coffee-house-tokens/
  quote: "a suitably dressed man could gain access to the well-heated and furnished premises"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "长条木桌上一只无柄陶碗盛深色咖啡，旁边一支白陶长烟斗"
  negative: "马克杯、玻璃杯、拿铁、现代烟具"

- fact_id: london1666.price.008
  claim: ale 的零售价上下界：1266 年法定上限为每夸脱 1 便士；1660 年消费税按每桶 6 先令分档（6 先令以上税 1s3d，6 先令及以下税 3d）；18 世纪初实卖每夸脱 2½ 便士
  tag: ⚠️
  source: Assize of Bread and Ale（Wikipedia）＋ 1660 年消费税法转述
  source_url: https://en.wikipedia.org/wiki/Assize_of_Bread_and_Ale
  quote: "it was forbidden to sell ale or beer at more than a penny a quart (two pints) or halfpenny a pint"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "锡镴大杯里晃着浑浊的淡色麦酒，木桌上一圈湿印"
  negative: "玻璃啤酒杯、气泡丰富的金黄啤酒、瓶装啤酒、品牌标"

- fact_id: london1666.price.009
  claim: 城市酒馆的「ordinary」是定时定价的公共餐，一份 1 先令 6 便士
  tag: ⚠️
  source: The Food Timeline, historic food prices（英式 ordinary 条目）
  source_url: https://www.foodtimeline.org/foodfaq5.html
  quote: "breakfast, dinner, and supper were the same price, one shilling and six pence"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "酒馆长桌上一盘炖肉、一块面包、一杯麦酒，众人同时开饭"
  negative: "单人菜单、分餐摆盘、餐巾折花、账单夹"

- fact_id: london1666.price.010
  claim: 1666 年皮普斯在一家 Taverne 请客，一次花掉 2 先令 6 便士
  tag: ✅
  source: Samuel Pepys, Diary, 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "Taverne, and there spent 2s. 6d. upon them"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "酒馆柜台上摊开几枚银先令，老板用指尖一枚枚推过去"
  negative: "纸币、找零盘、收据"

- fact_id: london1666.price.011
  claim: 1666 年 6 月 13 日，皮普斯在河边渔人处买三条鳗鱼，花三先令
  tag: ✅
  source: Samuel Pepys, Diary, 13 June 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "In my way home I called on a fisherman and bought three eeles, which cost me three shillings."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "河边渔人把三条活鳗鱼从木桶里捞进草篮"
  negative: "冰鲜盒、塑料袋、电子秤"

- fact_id: london1666.price.012
  claim: 1666 年 9 月 8 日（大火后第七天），皮普斯在泰晤士河上买两条鳗鱼就花了六先令——单价约为六月的三倍
  tag: ✅
  source: Samuel Pepys, Diary, 8 September 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "I bought two eeles upon the Thames, cost me six shillings."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "烧毁的河岸边，小船上的人举起两条鳗鱼开价"
  negative: "用于 9 月 1 日当天的镜次；灾后场景不得出现在大火前"

- fact_id: london1666.price.013
  claim: 1660 年代伦敦，一双普通长袜 5 先令，一双丝袜 15 先令
  tag: ⚠️
  source: Liza Picard《Restoration London》经 pepysdiary.com 转述
  source_url: https://www.pepysdiary.com/diary/1660/02/04/
  quote: "a pair of stockings cost 5 shillings, a pair of silk stockings 15 shillings"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "铺子里一排折好的粗毛长袜，旁边单独摆一双有光泽的丝袜"
  negative: "弹力袜、尼龙、包装袋、尺码标"

- fact_id: london1666.price.014
  claim: 1660 年代伦敦，一双男靴约 1 镑 10 先令，相当于非技术劳工约 22 天半的工钱
  tag: ⚠️
  source: Liza Picard《Restoration London》经 pepysdiary.com 转述
  source_url: https://www.pepysdiary.com/diary/1660/02/04/
  quote: "a pair of man's boots cost about 1 pound, 10 shillings"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "一双厚牛皮高筒靴立在鞋匠木凳旁，鞋面有手缝线"
  negative: "橡胶底、机缝、拉链、鞋盒"

- fact_id: london1666.price.015
  claim: 1666 年 7 月 17 日，皮普斯买一件骑装外套，花 30 先令
  tag: ✅
  source: Samuel Pepys, Diary, 17 July 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "riding-cloake for myself, to save my best. It cost me but 30s."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "裁缝铺里一件厚呢骑装外套搭在木架上"
  negative: "成衣吊牌、衣架排、镜面试衣间"

- fact_id: london1666.price.016
  claim: 1666 年 11 月 29 日，皮普斯买一顶天鹅绒骑马帽，花 20 先令
  tag: ✅
  source: Samuel Pepys, Diary, 29 November 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "bought me a velvet riding cap, cost me 20s."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "深色天鹅绒软帽放在木柜台上，绒面反光"
  negative: "棒球帽、机织标、现代帽盒"

- fact_id: london1666.price.017
  claim: 1666 年 2 月 19 日，皮普斯记 Ogilby 的书「另加装订共花我 4 镑」——约等于非技术劳工 60 天工钱
  tag: ✅
  source: Samuel Pepys, Diary, 19 February 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "Cost me L4 besides the binding"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "书桌上一部小牛皮精装大开本书，书口烫金"
  negative: "平装书、条形码、印刷封面设计"

- fact_id: london1666.price.018
  claim: 1660 年 11 月 2 日，皮普斯一部带银饰的《圣经》共 1 镑 3 先令 6 便士：书本身 9s6d、做工 6s6d、银料 7s6d
  tag: ✅
  source: Samuel Pepys, Diary, 2 November 1660，经 pepysdiary.com 读者引录
  source_url: https://www.pepysdiary.com/encyclopedia/317/
  quote: "bible which cost me 6s. 6d. the making, and 7s. 6d. the silver, which, with 9s. 6d. the book, comes in all to 1l. 3s. 6d."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "黑皮圣经封面上钉着银质角饰与搭扣"
  negative: "烫印彩色封面、书腰、塑封"

- fact_id: london1666.price.019
  claim: 复辟时期伦敦剧院正厅（pit）票价 2 先令 6 便士
  tag: ⚠️
  source: 皮普斯 1669 年 1 月 1 日日记所记 Duke of York's playhouse 票价，经二手转述
  source_url: https://www.pepysdiary.com/encyclopedia/475/
  quote: "people paying 2 shillings and 6 pence for pit seating at the Duke of York's playhouse"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "剧场正厅长凳上挤满人，舞台前烛排点着"
  negative: "编号座椅、电灯、票据打印"

- fact_id: london1666.price.023
  claim: 1655 年伦敦煤价通常在每 chaldron 20 先令以上；运煤车 420 辆归基督公学管辖，量器须在市政厅打封
  tag: ⚠️
  source: Old and New London vol.2, Lower Thames Street（British History Online）
  source_url: https://www.british-history.ac.uk/old-new-london/vol2/pp41-60
  quote: "was usually above 20s. a chaldron"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "河岸煤场上黑亮的煤堆与一排木轮运煤车"
  negative: "煤气罐、现代卡车、集装箱"

- fact_id: london1666.price.024
  claim: 1666 年 11 月 18 日，一场洗礼让皮普斯花掉近 40 先令：接生婆 20s、奶妈 10s、女仆 2s6d、马车 5s
  tag: ✅
  source: Samuel Pepys, Diary, 18 November 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "It cost me near 40s. the whole christening: to midwife 20s., nurse 10s., mayde 2s. 6d., and the coach 5s."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "屋里摆着酒与一块大蛋糕，产妇穿着待客的卧床服"
  negative: "气球、蛋糕裱花、相机"

- fact_id: london1666.money.001
  claim: 第一枚金几尼铸于 1663 年 2 月 6 日，1663 年 3 月 27 日公告为法定货币；名义值 20 先令，但金价上涨使其在市面溢价
  tag: ✅
  source: Guinea (coin), Wikipedia（与 Royal Mint Museum 查理二世条目交叉核对）
  source_url: https://en.wikipedia.org/wiki/Guinea_(coin)
  quote: "The first guinea was produced on 6 February 1663, with a proclamation of 27 March 1663 making the coins legal currency."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "掌心一枚小而厚的金币，正面是查理二世侧脸"
  negative: "大块金锭、现代纪念币、金条"

- fact_id: london1666.money.002
  claim: 1666 年 11 月 29 日，皮普斯的金匠说他不久前买 2000 枚几尼只贴 18½ 便士兑换费，现在要 22 便士，而且几乎买不到
  tag: ✅
  source: Samuel Pepys, Diary, 29 November 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "ginnys, which I bought 2,000 of not long ago, and cost me but 18 1/2d. change, will now cost me 22d.; and but very few to be had at any price."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "金匠铺柜台上小天平称几枚金币，旁边摊着银币"
  negative: "汇率牌、计算器、保险柜"

- fact_id: london1666.money.003
  claim: 1666 年 12 月 12 日，皮普斯再买金币，兑换贴水已到 22½ 便士
  tag: ✅
  source: Samuel Pepys, Diary, 12 December 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "of gold more of Mr. Stokes, but cost me 22 1/2d. change; but I am well"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（数据锚，用于口播）"
  negative: "把贴水说成固定汇率"

- fact_id: london1666.money.004
  claim: 查理二世初年铸币从锤打改为机制：1662 年 2 月起金币先上机器，银币随后一年多陆续铺开；机制币的边齿与边铭是为防止剪边
  tag: ✅
  source: Royal Mint Museum, Charles II
  source_url: https://www.royalmintmuseum.org.uk/journal/british-monarchs/charles-ii/
  quote: "The coinage was reformed early in Charles II's reign with the demise of hammered coinage which was replaced by high quality machine made milled coinage."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "手指捏起一枚边缘有细齿的银先令，另一枚边缘被剪得歪斜"
  negative: "全部崭新一致的硬币、塑料币托"

- fact_id: london1666.money.005
  claim: 王室与议会都不肯铸小面额，于是普通商人甚至市镇当局自己发行 farthing / halfpenny / penny 代币来做小额交易
  tag: ✅
  source: Mr. Pepys' Small Change（17 世纪伦敦代币专题站）
  source_url: https://c17thlondontokens.com/
  quote: "ordinary tradesmen and even some town authorities starting to issue their own low denomination token coinage (principally farthings, half pennies and pennies) to facilitate low value financial transactions"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "柜台木盘里一堆大小不一、边缘毛糙的薄铜片代币，面上刻着店名"
  negative: "统一制式硬币、光洁机制币、现代分币"

- fact_id: london1666.money.006
  claim: 私铸代币于 1672 年被查理二世取缔，改由王室发行铜质 halfpenny 与 farthing
  tag: ✅
  source: American Numismatic Association, English Tokens of the 17th and 18th Centuries
  source_url: https://www.money.org/money-museum/virtual-exhibits-moe-case14/
  quote: "Trade tokens were suppressed by Charles II in 1672, and replaced by Royal copper halfpennies and farthings."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（旁白用，不出画面）"
  negative: "1666 年画面中出现王室铜制 halfpenny"

- fact_id: london1666.money.007
  claim: 1648/9–1672 年间，仅伦敦老城墙以内就发行了 4000 种以上模铸代币；算上城外可能还要翻一倍
  tag: ✅
  source: Mr. Pepys' Small Change
  source_url: https://c17thlondontokens.com/
  quote: "During the period 1648/9 to 1672 over 4,000 separate die struck token types were issued within the precincts of the old walled city of London."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一小袋倒出来的代币，每一枚图案都不一样"
  negative: "成卷同款硬币、银行封装"

- fact_id: london1666.money.008
  claim: 代币面额与形制：farthing 直径 14–16mm（最早）、halfpenny 17–20mm（1656 年起，1664 年起成为主力面额）、penny 14–25mm（1663 年起，咖啡馆大量发行）；材质为薄铜片或黄铜片冲压
  tag: ✅
  source: Mr. Pepys' Small Change
  source_url: https://c17thlondontokens.com/
  quote: "struck or pressed on blank flans made of thin sheet copper or brass"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "指尖捏着一枚指甲盖大小的薄铜代币，能看出冲压的凹凸"
  negative: "厚重铸币、银币光泽、滚花边"

- fact_id: london1666.money.009
  claim: 代币只在发行者自己的店里兑现，基本不流通出发行者所在的小片街区
  tag: ✅
  source: Mr. Pepys' Small Change
  source_url: https://c17thlondontokens.com/
  quote: "were redeemable in the shops or premisses of their respective issuers and were not widely circulated beyond the local district in which they were issued"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "店主把一枚别家的代币推回顾客手里，摇头"
  negative: "全城通用的统一货币、找零机"

- fact_id: london1666.money.010
  claim: 1663–1672 年伦敦咖啡馆代币约 80 种，其中至少一半集中在 1669–1671 年；便士面额的代币自 1663 年起出现
  tag: ✅
  source: Mr. Pepys' Small Change — London Coffee House Tokens
  source_url: https://c17thlondontokens.com/category/london-coffee-house-tokens/
  quote: "Approximately 80 different coffee house tokens were issued between 1663-1672"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "咖啡馆柜台边一枚刻着店名与年份的铜代币"
  negative: "会员卡、二维码、积分章"

- fact_id: london1666.transport.001
  claim: 16 世纪横渡泰晤士河：包一条 wherry 1 便士，坐 sculler（单桨）半便士；逆流时费率加五成
  tag: ⚠️
  source: The Thames Watermen, chapter 1（泰晤士船夫专题）
  source_url: https://www.oocities.org/thameswatermen/chapter1.htm
  quote: "1d. for a wherry (whole boat), or ½d. for a sculler"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "河阶下一条窄长木船，船夫伸手接过一枚小铜币"
  negative: "码头闸机、船票、救生衣、发动机"

- fact_id: london1666.transport.002
  claim: 1559 年费率：往返格林尼治顺流 8 便士，逆流 12 便士
  tag: ⚠️
  source: The Thames Watermen, chapter 1
  source_url: https://www.oocities.org/thameswatermen/chapter1.htm
  quote: "8d. with the tide, but 12d. against it (1559 fares)"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "两名船夫并排划桨，逆着浑浊的潮水前进"
  negative: "马达、赛艇式整齐划桨"

- fact_id: london1666.transport.003
  claim: 后世通行的船资口径：一般是一对桨（oars）6 便士、单桨（sculls）3 便士；到兰贝斯与沃克斯霍尔 1 先令，到切尔西、巴特西、万兹沃思 1 先令 6 便士
  tag: ⚠️
  source: Georgian Index / 18 世纪伦敦船夫费率汇总（搜索结果摘录）
  source_url: http://www.georgianindex.net/transportationLondon/Watermen.html
  quote: "the usual fare being sixpence for a pair of oars and three pence for sculls; but to Lambeth and Vauxhall it was one shilling"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（数据参考，⚠️ 18 世纪费率，不得当 1666 年价口播）"
  negative: "作为 1666 年确定船资口播"

- fact_id: london1666.transport.004
  claim: 1662 年法令规定伦敦与威斯敏斯特的雇佣马车费率上限：一天（以 12 小时计）10 先令；第一小时不超过 18 便士，其后每小时 12 便士
  tag: ✅
  source: Statutes of the Realm vol.5, Charles II 1662（13 & 14 Car. II c.2），British History Online
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp351-357
  quote: "above the rate of ten shillings for a day reckoning twelve houres to the day and by the houre not above eighteen pence for the first houre and twelve pence for every houre after"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一辆四轮黑漆马车停在窄街口，车夫坐在前板上等客"
  negative: "计价器、车牌号码、橡胶轮胎、玻璃车窗"

- fact_id: london1666.transport.005
  claim: 1662 年法令的定点费率：律师学院一带到圣詹姆斯或威斯敏斯特 12 便士；到皇家交易所 12 便士；到伦敦塔、主教门或阿尔德门一带 18 便士
  tag: ✅
  source: Statutes of the Realm vol.5, Charles II 1662
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp351-357
  quote: "to the Tower of London or to Bishopsgate street or Algate or thereabouts eighteen pence"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "车夫伸出两根手指比划价钱，乘客掏出银币"
  negative: "价目表贴纸、找零机、手机支付"

- fact_id: london1666.transport.006
  claim: 直到 17 世纪中叶，泰晤士河都是伦敦最主要的交通干道；伦敦桥是当时唯一的桥
  tag: ✅
  source: Old and New London vol.3, The river Thames（British History Online）
  source_url: https://www.british-history.ac.uk/old-new-london/vol3/pp300-311
  quote: "Down to about the middle of the seventeenth century...the Thames had formed the great medium of metropolitan conveyance"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "宽阔浑黄的河面上密布小船，远处是密排屋舍的伦敦桥"
  negative: "多座桥、钢桥、塔桥、游船"

- fact_id: london1666.transport.007
  claim: 1666 年皮普斯因雇不到 oars（双桨船），只好搭一位「又老又穷的单桨船夫」
  tag: ✅
  source: Samuel Pepys, Diary, 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "by an old poor man, a sculler, having no oares to be got"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一名老船夫独自摇桨，船身狭小吃水浅"
  negative: "两名整齐划桨的年轻船夫、制服"

- fact_id: london1666.transport.008
  claim: 从伦敦桥桥洞「冲桥」极危险，淹死过不少人，讲究的人在桥一侧下船、步行过桥、另一侧再上船
  tag: ✅
  source: The Thames Watermen, chapter 1
  source_url: https://www.oocities.org/thameswatermen/chapter1.htm
  quote: "a number of people drowned in the attempt"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "伦敦桥桥墩间湍急的落差水流，小船在上游踌躇"
  negative: "平静水面、宽阔桥拱、现代护栏"

- fact_id: london1666.transport.009
  claim: 1634 年市政规定船夫夏天 5 点、冬天 7 点必须到自己的候客码头
  tag: ⚠️
  source: The Thames Watermen, chapter 1
  source_url: https://www.oocities.org/thameswatermen/chapter1.htm
  quote: "at their plying places by 5 o'clock in summer, 7 in winter"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "天刚亮的河阶上已有船夫坐在船头等客"
  negative: "上班打卡、时钟、排班表"

- fact_id: london1666.transport.010
  claim: 1662 年法令要求户主每周三、周六清扫自家门前街道
  tag: ✅
  source: Statutes of the Realm vol.5, Charles II 1662
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp351-357
  quote: "sweep and cleanse...all the Streets Lanes Allyes and publick places before theire respective Houses...twice every weeke...on every Wednesday and every Saturday"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "周六清早，家家门口有人拿长柄扫帚扫街，污水沿街心明沟流"
  negative: "洒水车、垃圾桶、下水道井盖、清洁工制服"

- fact_id: london1666.transport.011
  claim: 「泰晤士河上四万船夫」是含家属与依附行业的旧说法；斯托另记伦敦、威斯敏斯特与南岸约 3000 人、2000 条 wherry，1629 年海军部普查为 2426 名船夫
  tag: ✅
  source: The Thames Watermen, chapter 1
  source_url: https://www.oocities.org/thameswatermen/chapter1.htm
  quote: "3,000 in London, Westminster and the borough of Southwark, working 2,000 wherries and other small boats"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播纠偏用，无专属画面）"
  negative: "字幕打出「四万船夫」作为事实"

- fact_id: london1666.transport.012
  claim: 1666 年因海军大举强征（press），泰晤士河上雇不到船夫——皮普斯在塔码头「因为大抓丁，船夫太少」而走不成水路
  tag: ✅
  source: Samuel Pepys, Diary, 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "thinking to go by water, but could not get watermen; they being now so scarce, by reason of the great presse"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "空荡荡的河阶，只有两三条船停着，一名老船夫在补绳"
  negative: "河面挤满船只、人声鼎沸的码头"

- fact_id: london1666.transport.013
  claim: 1662 年起伦敦与威斯敏斯特的雇佣马车须领牌，发牌上限 400 辆，每辆年费 5 镑
  tag: ✅
  source: Statutes of the Realm vol.5, Charles II 1662
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp351-357
  quote: "the number to be licensed shall not exceed Foure hundred"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "马车车身侧面钉着一块带编号的金属牌"
  negative: "成排等客的车队、现代出租车顶灯"

- fact_id: london1666.transport.014
  claim: 车夫拒载或超收，每次罚 10 先令
  tag: ✅
  source: Statutes of the Realm vol.5, Charles II 1662
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp351-357
  quote: "If any Coachman shall refuse to go at or exact more for his hire then the severall Rates hereby limited he shall for every such offence forfeit the summ of ten shillings."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "乘客指着车夫理论，路人围观"
  negative: "警察、罚单、对讲机"

- fact_id: london1666.transport.015
  claim: 1666 年 9 月 10 日，因城内烧毁，雇佣马车改在阿尔德门外候客
  tag: ✅
  source: Samuel Pepys, Diary, 10 September 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "Took a hackney-coach myself (the hackney-coaches now standing at Allgate)."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（仅用于灾后镜次）城门外一排马车停在空地上等客"
  negative: "用于 9 月 1 日当天的镜次"

- fact_id: london1666.transport.016
  claim: 1634 年 Sir Saunders Duncombe 取得 14 年专营，把可雇轿子引进伦敦；轿子比马车便宜，能走马车进不去的窄巷
  tag: ⚠️
  source: Historic UK, The Sedan Chair
  source_url: https://www.historic-uk.com/CultureUK/Sedan-Chair/
  quote: "In 1634 Sir Saunders Duncombe introduced the sedan chair for hire in London."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "两名轿夫抬一顶带顶棚的单人轿，侧身挤过窄巷"
  negative: "四人大轿、中式轿子、装饰华丽的礼舆"

- fact_id: london1666.transport.017
  claim: 大火期间街上的人「出多少钱都要雇到车」把东西运走
  tag: ✅
  source: Samuel Pepys, Diary, 3 September 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "the streets and the highways are crowded with people running and riding, and getting of carts at any rate to fetch away things"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（仅用于灾后镜次）挤满人和车的街道，家具堆在车上"
  negative: "用于 9 月 1 日当天的镜次"

- fact_id: london1666.work.001
  claim: 1660 年王室工务局在伦敦塔与白厅的账目里，石匠与木匠日工价 24–30 便士，劳工 16 便士
  tag: ✅
  source: Judy Stephenson, "Real contracts and mistaken wages", LSE Economic History Working Paper 231/2016, p.8（引 TNA WORK 5/1）
  source_url: https://www.lse.ac.uk/asset-library/information/wp231.pdf
  quote: "Their day rates ranged from 24d. to 30d.as Hutchins' found, and the labourers rate was 16d."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "工地木案上，账房用鹅毛笔在账册上逐人记下日数"
  negative: "工资单、打卡机、纸币发薪"

- fact_id: london1666.work.002
  claim: 1667 年的伦敦建筑估价手册 Primatt《The City & Country Purchaser and Builder》按砌砖工 36 便士、其小工 20 便士一天来算成本
  tag: ✅
  source: Robert C. Allen, "Real Wages Once More: A Response to Judy Stephenson", NYUAD Working Paper 0006 (2017)
  source_url: https://nyuad.nyu.edu/content/dam/nyuad/academics/divisions/social-science/working-papers/2017/0006.pdf
  quote: "Primatt's The City & Country Purchaser and Builder (1667) assumed that builders paid bricklayers and their labourers 36d and 20d per day, respectively"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（数据锚，用于口播换算）"
  negative: "把 36d 当成普通劳工的工钱"

- fact_id: london1666.work.003
  claim: Boulton 的伦敦挂牌区间：1670 年工匠 24–36 便士、劳工 14–24 便士；到 1710/1720 年分别升到 30–42 与 21–26 便士
  tag: ✅
  source: Judy Stephenson, LSE WP 231/2016, note 53（引 Boulton, "Wage Labour in Seventeenth-Century London", p.277）
  source_url: https://www.lse.ac.uk/asset-library/information/wp231.pdf
  quote: "the range of rates charged out increased from 24d to 36d per day in 1670 to 30d to 42 d per day in 1710. For labourers the range moved from 14d to 24d in 1670"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（数据锚，用于口播换算）"
  negative: "把区间上限当成典型值"

- fact_id: london1666.work.004
  claim: 圣保罗大教堂 1675 年核定木匠、砌砖工、石匠的日工价为 2 先令 6 便士，直到 1711 年后才上调
  tag: ✅
  source: Judy Stephenson, LSE WP 231/2016
  source_url: https://www.lse.ac.uk/asset-library/information/wp231.pdf
  quote: "St Paul's allowable day rates were set at 2s.6d. for carpenters, bricklayers, masons in 1675."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（数据锚）"
  negative: "用于 1666 年当年的画面字幕"

- fact_id: london1666.work.005
  claim: 更早的基线：1614 年伦敦坦普尔工地的日工价为工匠 20 便士、劳工 14 便士
  tag: ⚠️
  source: Judy Stephenson, LSE WP 231/2016, p.8（引 Boulton 序列，MT2/TOT/3/2）
  source_url: https://www.lse.ac.uk/asset-library/information/wp231.pdf
  quote: "The days rates are as recorded in Boulton's series; 20d. per day for craftsmen, and 14d. per day for labourers."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（数据锚，Δ−52，仅作趋势参照）"
  negative: "作为 1666 年工钱口播"

- fact_id: london1666.work.006
  claim: 账册上的 day rate 是承包商向业主开的价，不是工人到手的工钱；扣掉承包商利润，伦敦建筑工人的实得比现行估算低两到三成
  tag: ✅
  source: Judy Stephenson, LSE WP 231/2016, Abstract
  source_url: https://www.lse.ac.uk/asset-library/information/wp231.pdf
  quote: "The actual wages paid to London building workers were twenty to thirty per cent below current estimates."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播加注用）"
  negative: "把 16d 说成工人一定拿到手的钱"

- fact_id: london1666.work.010
  claim: Thomas Farriner 约生于 1615 年，1637 年加入面包师同业公会，1649 年起自有店面，是布丁巷的面包师兼教区执事
  tag: ✅
  source: Thomas Farriner, Wikipedia
  source_url: https://en.wikipedia.org/wiki/Thomas_Farriner
  quote: "Farriner joined the Baker's Company in 1637, and had his own shop by 1649."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "窄巷里一间前店后坊的面包铺，门口挂着行会招牌"
  negative: "玻璃橱窗、电灯、现代烤箱"

- fact_id: london1666.work.011
  claim: Farriner 在英荷战争期间给皇家海军供面包，被称作「国王的面包师」
  tag: ✅
  source: Thomas Farriner, Wikipedia / The Monument
  source_url: https://en.wikipedia.org/wiki/Thomas_Farriner
  quote: "a well-known baker in the City of London, who provided bread for the Royal Navy during the Anglo-Dutch war"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "作坊里成排的硬面包干（ship's biscuit）摊在木架上晾"
  negative: "松软吐司、蛋糕、包装袋"

- fact_id: london1666.work.012
  claim: 1666 年 9 月 2 日凌晨，Farriner 被卧室门下涌进的烟熏醒，和女儿从楼上窗户逃出，女仆因不敢跳而死
  tag: ✅
  source: Thomas Farriner, Wikipedia
  source_url: https://en.wikipedia.org/wiki/Thomas_Farriner
  quote: "in the early hours of 2 September 1666, in his house on Pudding Lane, Farriner was awakened by smoke billowing under the door of his bedroom"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（仅用于灾后／片尾钩子）窄巷木楼上窗口有人翻出"
  negative: "用于 9 月 1 日白天的镜次"

- fact_id: london1666.work.013
  claim: 到 1660 年代，伦敦的海运煤进口量已是 1605–6 年的三倍以上；1700 年超过 46 万吨运抵码头
  tag: ⚠️
  source: National Coal Mining Museum, The Hidden Lives of the Coal Traders
  source_url: https://www.ncm.org.uk/whats-on/the-hidden-lives-of-the-coal-traders/
  quote: "by the 1660s sea-coal imports to London had more than trebled"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "河上停着一排运煤的柯利尔帆船，天空压着煤烟"
  negative: "蒸汽船、烟囱工厂、现代货轮"

- fact_id: london1666.work.014
  claim: 1655 年伦敦有 420 辆运煤车归基督公学管辖，所有煤的量器必须在市政厅打封
  tag: ⚠️
  source: Old and New London vol.2, Lower Thames Street
  source_url: https://www.british-history.ac.uk/old-new-london/vol2/pp41-60
  quote: "coal-carts numbered 420 and fell under Christ's Hospital governance, with all measures requiring sealing at Guildhall"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "巷口一辆两轮运煤车，车斗满是黑煤，车侧有烙印标记"
  negative: "现代自卸车、集装箱、条形码"

- fact_id: london1666.work.016
  claim: 泰晤士街沿河的货栈塞满可燃物——蜡油、灯油、烈酒和煤；当时人形容那一带是「老纸板房子」和焦油、沥青、麻、松香、亚麻这类最易燃的东西，码头上堆着木材与煤
  tag: ✅
  source: Great Fire of London（Wikipedia，引当时文献）／Gresham College 讲座摘要
  source_url: https://en.wikipedia.org/wiki/Great_Fire_of_London
  quote: "old paper buildings and the most combustible matter of Tarr, Pitch, Hemp, Rosen, and Flax"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "河岸木栈房前堆着焦油桶、麻绳卷、木料垛和黑煤堆"
  negative: "钢构仓库、消防栓、灭火器、安全标识"

- fact_id: london1666.work.017
  claim: 船夫同业公会 1555 年成立，规定须先摇两年船才准独自掌一条 wherry，实行师徒制
  tag: ✅
  source: The Thames Watermen, chapter 1
  source_url: https://www.oocities.org/thameswatermen/chapter1.htm
  quote: "two years' rowing experience before being allowed to take charge of a wherry"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "一个少年学徒在船尾学摇桨，老船夫在旁纠正手势"
  negative: "驾照、教练船、救生衣"

- fact_id: london1666.work.018
  claim: 18 世纪末泰晤士船夫名册规模为 12,283 人（8,283 名自由人、2,000 名非自由人、2,000 名学徒），每年收学徒 200–300 名
  tag: ⚠️
  source: Old and New London vol.2, Lower Thames Street
  source_url: https://www.british-history.ac.uk/old-new-london/vol2/pp41-60
  quote: "records show 12,283 watermen (8,283 freemen, 2,000 non-freemen, and 2,000 apprentices)"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（规模说明用，Δ+130，不得当 1666 年数字口播）"
  negative: "把 12,283 说成 1666 年的船夫数"

- fact_id: london1666.work.019
  claim: 伦敦酒馆密度：1577 年米德尔塞克斯（不含城内）720 家 alehouse、132 家 inn，约每 76 人一家；1620 年查令十字到坦普尔栅之间近 100 家 tavern；1641 年穷的城外区每 6 户就有 1 户卖酒，富的中心区是 1/30–1/40
  tag: ⚠️
  source: Tim Reinke-Williams, "Women, ale and company in early modern London", Brewery History No.135
  source_url: https://www.breweryhistory.com/journal/archive/135/Women.pdf
  quote: "The census taken in 1577 did not include the City, but recorded 720 alehouses and 132 inns in Middlesex, equating to one alehouse for every 76 people."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一条短街上连着三块挑出的酒招牌"
  negative: "霓虹灯招牌、连锁品牌、玻璃门"

- fact_id: london1666.work.020
  claim: 伦敦第一家咖啡馆 1652 年由 Pasqua Rosée 开在康希尔圣米迦勒教堂墙边；到 1663 年，仅罗马城墙以内就至少开了 82 家
  tag: ✅
  source: The Public Domain Review, "The Lost World of the London Coffeehouse"
  source_url: https://publicdomainreview.org/essay/the-lost-world-of-the-london-coffeehouse/
  quote: "By 1663, at least 82 had opened within London's Roman walls."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "挂着招牌的小门脸，门上方一个土耳其人头像，屋里烟雾缭绕"
  negative: "咖啡连锁标识、外卖窗口、菜单板"

- fact_id: london1666.work.021
  claim: 体面女性不会作为顾客出现在咖啡馆里；1674 年还出现过《Women's Petition Against Coffee》抱怨丈夫泡咖啡馆
  tag: ✅
  source: The Public Domain Review, "The Lost World of the London Coffeehouse"
  source_url: https://publicdomainreview.org/essay/the-lost-world-of-the-london-coffeehouse/
  quote: "No respectable women were seen in coffeehouses as customers."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "咖啡馆内清一色男性围坐长桌，唯一的女性站在柜台后倒咖啡"
  negative: "女顾客落座喝咖啡、情侣对坐"

- fact_id: london1666.work.022
  claim: 伦敦同业公会学徒标准期 7 年，多在 14–21 岁之间服役，是取得市民资格的正路；约四分之一的人实际服役更久
  tag: ✅
  source: Records of London's Livery Companies Online（londonroll.org）
  source_url: https://www.londonroll.org/about
  quote: "Seven-year apprenticeships were the standard way to become a freeman of a City of London livery company, typically undertaken between the ages of 14 and 21."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "作坊角落里一个十六七岁的少年在扫地、搬料，穿着素色短袍"
  negative: "校服、课本、工牌"

- fact_id: london1666.work.023
  claim: 1660 年代伦敦男性有一半不到 25 岁；学徒工时极长，普遍抱怨没有闲暇与人身自由
  tag: ⚠️
  source: Gresham College, "Apprenticeship in early modern London"
  source_url: https://www.gresham.ac.uk/watch-now/apprenticeship-early-modern-london-economic-origins-and-destinations
  quote: "In London in the 1660s, half the male population was under the age of 25, and apprentices worked long hours and resented their lack of leisure and personal freedom."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街口聚着一群十七八岁的学徒，戴平顶帽，说笑推搡"
  negative: "中年工人为主的街景、写字楼、背包"

- fact_id: london1666.work.024
  claim: 1663 年 10 月的市政会法令（Robinson's Act）确认伦敦城内所有户主都要轮值守夜，任务是维持治安、拿捕夜行人与可疑人等
  tag: ✅
  source: Journal of ART in SOCIETY, "Watchmen, goldfinders and the plague bearers of the night"（引伦敦市政会法令）
  source_url: https://www.artinsociety.com/watchmen-goldfinders-and-the-plague-bearers-of-the-night.html
  quote: "to keep the peace and apprehend night-walkers, malefactors and suspected persons"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "夜里街角一个提灯的中年男子，手里一根长木棍，没有制服"
  negative: "警察制服、警徽、警棍、警车"

- fact_id: london1666.work.025
  claim: 到 1660 年代，花钱雇人代自己值夜已是常态；越来越多是户主凑钱进一个守夜基金，由区里的 beadle 或 constable 去雇人
  tag: ✅
  source: Journal of ART in SOCIETY, "Watchmen, goldfinders and the plague bearers of the night"
  source_url: https://www.artinsociety.com/watchmen-goldfinders-and-the-plague-bearers-of-the-night.html
  quote: "it was already common practice to avoid night-time service in the watch by paying for a substitute"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "门口一位商人把几枚银币交给拿名册的区吏"
  negative: "缴费单、收据、POS 机"

- fact_id: london1666.work.026
  claim: 更夫在查理二世治下得了个绰号「Charlies」
  tag: ⚠️
  source: Watchman (law enforcement), Wikipedia
  source_url: https://en.wikipedia.org/wiki/Watchman_(law_enforcement)
  quote: "Constables supervised the \"Charlies\", a nickname watchmen acquired during Charles II's reign."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播梗用）"
  negative: "把 Charlies 说成官方职称"

- fact_id: london1666.work.027
  claim: 负责收守夜钱的 beadle 与 constable 常被指控尽量少雇更夫、把差额揣进自己口袋，当作自己无薪公职的补偿
  tag: ✅
  source: Journal of ART in SOCIETY, "Watchmen, goldfinders and the plague bearers of the night"
  source_url: https://www.artinsociety.com/watchmen-goldfinders-and-the-plague-bearers-of-the-night.html
  quote: "often accused to spend as little as possible on hiring watchmen and pocket the difference as a recompense for the unpaid service they had performed"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "区吏在门廊下清点一小堆银币，抬眼看了看四周"
  negative: "账本电脑、监控、制服"

- fact_id: london1666.work.028
  claim: 伦敦街头叫卖的货包括水、煤、火柴、鸣禽、牡蛎、肥鸡、成串的洋葱
  tag: ✅
  source: Theatrum Mundi, "The Cries of London"
  source_url: https://theatrum-mundi.org/library/the-cries-of-london/
  quote: "water, coal, matches, singing birds, oysters, fat chickens, strings of onions"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "挑着扁担的小贩肩上挂着一串洋葱，另一手提柳条鸟笼"
  negative: "香蕉、菠萝、辣椒、塑料袋、推车摊位"

- fact_id: london1666.work.029
  claim: 17 世纪伦敦当局受理过「穷苦卖奶妇人」「穷苦女果贩」「年老的穷鱼妇」的陈情——街头叫卖是女性集中的行业
  tag: ✅
  source: John Gallagher, "Shriek of the Milkman: London Hawking", London Review of Books
  source_url: https://www.lrb.co.uk/the-paper/v45/n21/john-gallagher/shriek-of-the-milkman
  quote: "'poore woemen selling milke', 'pore woman Fruterers' and 'ancient poore fishwifes'"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "戴头巾围裙的妇人头顶木盆，盆里是奶桶，边走边喊"
  negative: "玻璃奶瓶、纸盒牛奶、冷链车"

- fact_id: london1666.work.030
  claim: Marcellus Laroon《The Cryes of the City of London drawne after the Life》由 Pierce Tempest 出版，74 幅铜版画，画的是 17 世纪末伦敦街头小贩、乞丐与市井人物
  tag: ⚠️
  source: University of Chicago Press 书目／Theatrum Mundi 综述
  source_url: https://press.uchicago.edu/ucp/books/book/distributed/H/bo109459036.html
  quote: "The earliest collection of street cries dates from 1688, by the artist Marcellus Laroon."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（视觉参考来源，非画面内容）"
  negative: "把 1688 年的服装细节当作 1666 年的确证"

- fact_id: london1666.work.031
  claim: 1662 年法令规定清道夫（scavengers）的车除周日外每天出动，来时须出声通知，负责把污物运走
  tag: ✅
  source: Statutes of the Realm vol.5, Charles II 1662
  source_url: https://www.british-history.ac.uk/statutes-realm/vol5/pp351-357
  quote: "carry or cause to be carried away"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一辆敞篷粪车停在巷口，车夫摇铃吆喝，邻人把桶端出来"
  negative: "垃圾车、垃圾桶、塑料袋、清洁制服"

- fact_id: london1666.work.032
  claim: 1666 年 9 月 1 日（周六）皮普斯的一天：整个上午在办公室，回家吃饭，把新书房打扫干净「为明天准备」，下午去看木偶戏 Polichinelly，晚上到伊斯灵顿吃喝，唱着歌回家
  tag: ✅
  source: Samuel Pepys, Diary, 1 September 1666（Project Gutenberg #4167, Vol.45）
  source_url: https://www.gutenberg.org/cache/epub/4167/pg4167.html
  quote: "September 1st. Up and at the office all the morning, and then dined at home. Got my new closet made mighty clean against to-morrow."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "傍晚的伊斯灵顿田野酒馆外，几个人边走边唱往城里回"
  negative: "任何预告火灾的画面、烟雾、慌乱人群"

- fact_id: london1666.work.033
  claim: 大火中救火的报酬极低——富商 Alderman Starling 在邻居们救下他的房子后，只拿出 2 先令 6 便士分给三十个人（人均 1 便士），还骂搬瓦砾的人是来偷东西的
  tag: ✅
  source: Samuel Pepys, Diary, 8 September 1666（Project Gutenberg #4171）
  source_url: https://www.gutenberg.org/cache/epub/4171/pg4171.txt
  quote: "the fire at next door to him in our lane, after our men had saved his house, did give 2s. 6d. among thirty of them, and did quarrel with some that would remove the rubbish out of the way of the fire, saying that they come to steal"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（仅用于灾后镜次）满脸烟灰的人们伸手接过几枚铜币"
  negative: "用于 9 月 1 日当天的镜次"
```

### ai_draft（**不得进 prompt、不得进口播数字**，待人工核）

```yaml
- fact_id: london1666.price.020
  claim: 理发师刮一次脸不得超过 3 便士
  tag: ⚠️
  source: 仅见搜索摘要，未找到原始条文与年代
  source_url: https://restaurant-ingthroughhistory.com/restaurant-prices/
  quote: "barbers were not permitted to charge more than 3 pence for a shave"
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "（暂不使用）"
  negative: "作为 1666 年确定价格口播"

- fact_id: london1666.price.021
  claim: 伦敦客栈一晚住宿的价格
  tag: ❌
  source: 未查到 1660 年代数据（找到的最近是 1787 年英格兰某客栈 1s 9d 一晚）
  source_url: https://www.ourcivilisation.com/smartboard/shop/bynpwllr/inns4.htm
  quote: "only one shilling and ninepence a night was charged at an inn"
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "（暂不使用）"
  negative: "拿 1787 年价格当 1666 年价格"

- fact_id: london1666.price.022
  claim: 一张《死亡周报》（Bills of Mortality）售价约一便士
  tag: ⚠️
  source: Gresham College 讲座摘要转述
  source_url: https://www.gresham.ac.uk/watch-now/1665-londons-last-great-plague
  quote: "The bills cost about a penny, and were published in large print runs."
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: "（暂不使用；可作道具，不报价）"
  negative: "作为确证价格口播"

- fact_id: london1666.work.034
  claim: 煤炭搬运工每交付二十 chaldron 得 3 先令；一帮通常 9 人加量煤官与助手，卸空一船 5–7 天
  tag: ⚠️
  source: National Coal Mining Museum（描述出自 18 世纪，Δ+100）
  source_url: https://www.ncm.org.uk/whats-on/the-hidden-lives-of-the-coal-traders/
  quote: "each receiving three shillings for every score of chaldron of coal delivered into the lighter"
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: "（暂不使用数字；「九人一帮」的画面可用）"
  negative: "作为 1666 年工钱口播"

- fact_id: london1666.work.035
  claim: 17 世纪中期伦敦有相当比例的代币由女性商人发行
  tag: ⚠️
  source: Humanities and Social Sciences Communications, "Women's work on small change"（原文被登录墙挡住，仅见标题与摘要）
  source_url: https://www.nature.com/articles/s41599-022-01116-5
  quote: "（未取得原文正句）"
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（暂不使用）"
  negative: "在未核原文前引用任何百分比"
```

---

## 未解决 / 交给人工核的清单

1. **1666 年当年的 penny loaf 重量**——最接近的是 1618–19 年伦敦市政记录（13–17 盎司）与 1720 年斯特赖普。建议查：伦敦市政厅 Journals of the Court of Common Council 1660s 的 assize 条目，或 1666–70 年《London Gazette》的 assize 告示。
2. **1666 年英格兰小麦价（每 quarter 几先令）**——有了它就能反推当年的面包重量。Beveridge / Rogers / Clark 的序列在线版均未取到具体年值（ucdavis 站点证书过期，JSTOR/Wiley 收费）。
3. **1660 年代的船夫官定费率**——只找到 1559 年与 18 世纪两端。建议查：1671 / 1698–9 年 watermen 法令下由 Court of Aldermen 核定的费率表，或 1720 年斯特赖普《伦敦志》里的 "Rates of Watermen"。
4. **1660 年代 ale／small beer 的零售单价**——只有 1266 年上限与 18 世纪初实价两端；1660 年消费税法按每桶 6 先令分档，可反推但需要桶容与零售加成。
5. **1660 年代客栈住宿价**。
6. Nature《Women's work on small change》原文（女性发行代币的比例与行业分布）——被登录墙挡住，建议人工下载 PDF。
7. **Boulton (2000)《Food prices and the standard of living in London … 1580-1700》原文**——两处 PDF 链接分别 404 / 收费；这是唯一能给出 1660 年代伦敦逐项食品价的学术序列，值得人工获取。

## 与其他 worker 的接口

- **§7 与 §8 共用锚 B**：任何 worker 要把金额换成「几天工钱」，一律用 **16d／天（劳工）**，工匠用 **30d／天**。不要各自另设分母。
- **§6 的「周六扫街」（`transport.010`）** 与 **§8.8 清道夫**、**§8.1 面包师夜班** 三条共同决定 9 月 1 日的街道基线，请负责场景／镜头的 worker 直接取用。
- **`transport.012`（船夫被强征）** 是本站唯一一条「1666 年独有」的交通摩擦，建议写进至少一镜。
- **所有 ❌/ai_draft 条目不得进 prompt**；`price.012`、`transport.015`、`transport.017`、`work.012`、`work.033` 是**灾后**素材，**严禁出现在 9 月 1 日当天的镜次**。
