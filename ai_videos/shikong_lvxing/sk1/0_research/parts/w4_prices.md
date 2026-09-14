---
worker_id: W4_prices
stage: 0
role: researcher
angle: 物价货币
status: complete
blockers: []
confidence: medium
task_id: sk1-20260913-203500
scope: dossier §7 物价与货币（两锚 + 商品价 + 货币形态 + 今日账单）；§13 货币类误传
fact_counts: {ai_read: 29, ai_draft: 4, total: 33}
tool_calls: 56
---

# W4 · 物价与货币 —— 汴京 · 宣和二年（1120）清明

> 口径：一律「篮子锚定」——每笔钱只换算成「≈ 几斗米 / 几天工钱」，**禁止「一两银子 ＝ X 元」**。
> `verified_by`：`ai_read` ＝ 本次 WebFetch/WebSearch 抓到页面并摘出原句（`quote_kind: 逐字 | 摘要`）；`ai_draft` ＝ 未抓到原页，待人眼核。**`ai_draft` 与「摘要」类不得进 prompt**（playbook §3）。

## 1. 两个锚

### 锚 A · 米价（汴京，1110s–1120s）

| 年份 | 汴京米价 | 出处 | tier |
|---|---|---|---|
| 大中祥符二年 1009 | 粟 每斗 30 文 | 程民生《宋代物价研究》→ 澎湃转述 | T1→T3 |
| 熙宁二年 1069 | 米 每斗 40 文（京师周边） | 同上 | T1→T3 |
| 熙宁七年 1074 | 米 每斗 80–100 文 | 同上 | T1→T3 |
| 大观年间 1107–1110 | 一石米 2 500 文（＝ 每斗 250 文） | 程民生 → 搜狐「食品篇上」转述 | T1→T3 |
| **宣和四年 1122** | **米 每斗 250–300 文** | 程民生 → 澎湃转述 | T1→T3 |

**锚 A 定值：1120 年汴京米 ≈ 每斗 250 文（区间 200–300）**。1120 无当年数据，取大观（250）与宣和四年（250–300）之间内插 → `tag: ⚠️`；两端点本身 `✅`。一斗 ≈ 今 12.5 斤（搜狐转述的换算，T3）。

### 锚 B · 日工钱

| 人群 | 日工钱 | 出处 | tier |
|---|---|---|---|
| 北宋普通劳动者（卖柴 / 淮西雇工 / 渔民）均值 | **≈ 100 文 / 日** | 程民生《宋人生活水平考察》（乌有之乡转载，抓取为摘要） | T1 |
| 「居民人均收入」 | 约每日 100 文 | 程民生 → 澎湃转述 | T1→T3 |
| 一人最低生活费 | ≈ 20 文 / 日；普通家庭日常费 < 100 文 / 日 | 程民生 → 搜狐新书报道（逐字） | T1→T3 |
| 纲运脚夫（嘉祐六年 1061） | 100 文 / 日 | 仅搜索摘要，原页未含此句 | ai_draft |
| 余姚筑堤民夫（庆历七年 1047） | 125 文 / 日 | 仅搜索摘要 | ai_draft |

**锚 B 定值：脚夫 / 力夫 日工钱 ≈ 100 文**（程民生北宋均值；宣和当年无专值 → 本站存疑之一，见 sk1 卡）。

### 换算

- **一天工钱 100 文 ≈ 0.4 斗米（≈ 4 升 ≈ 今 5 斤）**。
- 100 文按「街市通用 75 陌」实付 **75 枚铜钱**；按官陌 77 枚。
- 一贯（名义 1 000 文）≈ **10 天工钱 ≈ 4 斗米**。
- 反向：一斗米 ≈ 2.5 天工钱。→ 宣和末汴京是「一天工钱买不到半斗米」的物价高位（比熙宁七年贵 2.5–3 倍）。

## 2. 商品价格表（≥ 10 件，全换算「≈ 几天工钱」，锚 B ＝ 100 文/日）

| # | fact_id | 商品 | 价格 | ≈ 天工钱 | 出处 / tier | tag |
|---|---|---|---|---|---|---|
| 1 | price.001 | 州桥夜市 鹅鸭鸡兔肚肺鳝鱼**包子**、鸡皮、腰肾、鸡碎 | 每个 ≤ 15 文 | 0.15 天 | 《东京梦华录》卷二「州桥夜市」T0 | ✅ |
| 2 | price.002 | 小酒店**下酒菜**（煎鱼 / 鸭子 / 炒鸡兔 / 煎燠肉 / 梅汁 / 血羹 / 粉羹） | 每分 ≤ 15 钱 | 0.15 天 | 卷二「饮食果子」T0 | ✅ |
| 3 | price.003 | 天晓早市 酒店 **粥饭点心** | 每分 ≤ 20 文 | 0.2 天 | 卷三「天晓诸人入市」T0 | ✅ |
| 4 | price.004 | 食店 精细菜蔬「**造齏**」（碧碗盛） | 每碗 10 文 | 0.1 天 | 卷四「食店」T0 | ✅ |
| 5 | price.005 | 遇仙正店 **银瓶酒 / 羊羔酒** | 72 文 / 81 文 一角 | 0.72 / 0.81 天 | 卷二「宣德楼前省府宫宇」T0 | ✅ |
| 6 | price.006 | 正店 **梢桶酒**（批发，每梢约三斗） | 一贯五百文 → 每升 ≈ 50 文 | 0.5 天 / 升 | 卷三「般载杂卖」T0 | ✅ |
| 7 | price.007 | 冬月黄河客鱼「**车鱼**」 | 每斤 ≤ 100 文 | 1 天 | 卷四「鱼行」T0 | ✅ |
| 8 | price.008 | **租鞍马**（出街市干事、路远倦行） | 不过百钱 | ≤ 1 天 | 卷四「杂赁」T0 | ✅ |
| 9 | price.009 | **笼饼** 一枚 / 蔬菜包子 / 油糍 / 枣 | 7 文 / 3 文 / 1 文 / 1 文 7 颗 | 0.07 / 0.03 / 0.01 天 | 程民生 → 搜狐新书报道（逐字）T1→T3 | ✅ |
| 10 | price.010 | **羹** 一碗（北宋后期洛阳） | 10 文 | 0.1 天 | 同上 | ✅ |
| 11 | price.011 | **猪 / 羊肉**（治平末 1067） | 三四十钱 一斤 | 0.3–0.4 天 | 《长编》→ 搜狐「食品篇上」T0→T3 | ✅ |
| 12 | price.012 | **牛肉**（大观年间） | 每斤 100 文 | 1 天 | 同上 T3 | ⚠️ |
| 13 | price.013 | **羊肉**「每斤六十足」（北宋末） | 60 文足 | 0.6 天 | 同上，页面称出自《清明上河图》题记——存疑 | ⚠️ |
| 14 | price.014 | **绢** 每匹（熙丰间市价） | ≈ 1 贯足 | 10 天 | 《宋会要》→ 知乎熙丰年鉴（搜索摘要，原页 403） | ⚠️ |
| 15 | price.015 | **布** 每匹（元丰元年 成都府路 夏税布估） | 420 文足 | 4.2 天 | 同上 | ⚠️ |
| 16 | price.016 | **蜡烛** 一根 | 150–400 文 | 1.5–4 天 | 程民生 → 吴钩转述（搜索摘要，儒家网 403） | ⚠️ |
| 17 | price.017 | **客店** 一晚 | ≈ 50 文 | 0.5 天 | 仅搜索摘要，无史源 | ai_draft |
| 18 | price.018 | **茶饮子** 一碗 | 未查（估 1–3 文） | ≈ 0.02 天 | 无 | ai_draft |
| 19 | price.019 | **船资 / 过虹桥** | 未查（《梦华录》无桥费记载） | — | 无 | ai_draft |
| 20 | price.020 | **纸马** 一份（清明纸马铺） | 未查 | — | 卷七仅记「纸马铺皆于当街用纸衮叠成楼阁之状」 | ai_draft |
| 21 | price.021 | **柳枝**（清明簪柳 / 轿顶装柳） | 未查（郊野自折，多半不花钱） | 0 | 卷七「轿子即以杨柳杂花装簇顶上」 | ai_draft |

**可直接进 prompt / 口播的（✅ 且逐字）**：#1–#11。**只能进「本站存疑」或旁白加 ⚠️ 的**：#12–#16。**待补**：#17–#21。

## 3. 货币实物形态（1120 年汴京市面）

| fact_id | 要点 | tag |
|---|---|---|
| money.001 | **主币是铜钱**：圆形方孔，面文年号 + 通宝/元宝/重宝。1120 年一串钱里最多的是**熙宁 / 元丰钱**（元丰年铸铜钱 500 万贯，历朝之最）而非最新的宣和钱。 | ✅（铸量）/ ⚠️（「最常见」为推断） |
| money.002 | **徽宗六个年号钱**：崇宁通宝（1102–06，瘦金体，小平 + 当十，Met 样本径 3.5 cm）→ 大观通宝（1107–10，瘦金体，小平 24 mm / 当十 39 mm）→ **政和通宝（1111–18，篆隶对钱，小平 25 mm / 折二 30 mm，铸 8 年，是 1120 年最新且最普遍的新钱）** → 重和通宝（1118，仅三个月，极少）→ **宣和通宝（宣和元年 1119 始铸，篆 / 隶对钱，小平 + 折二；样本外径 3 cm）**。 | ✅ |
| money.003 | **当十大钱贬值**：崇宁当十钱（铜料值 3 文强当 10）私铸泛滥，**政和元年（1111）诏当十改当三**——1120 年市面上崇宁 / 大观大钱按 3 文用。 | ✅《宋史》卷 180 |
| money.004 | **省陌**：「都市钱陌，官用七十七，街市通用七十五，鱼肉菜七十二陌，金银七十四，珠珍、雇婢妮、买虫蚁六十八，文字五十六陌，行市各有长短使用」——**一「百」文实付 75 枚（街市）/ 72 枚（买鱼肉菜）**；官方定制「所在用七十七钱为百」。 | ✅《梦华录》卷三 +《宋史》卷 180 |
| money.005 | **一贯**：名义 1 000 文；按官陌实为 770 枚、街市 750 枚；用麻绳穿成串（钱贯），约 4 kg 级重量（按枚 ≈ 4 g 估算，⚠️）。 | ✅ / ⚠️（重量） |
| money.006 | **铁钱只行川陕**：「蜀平，听仍用铁钱」「川、陕皆行铁钱」；汴京不见铁钱。 | ✅《宋史》卷 180 |
| money.007 | **交子 / 钱引是四川的（铁钱本位）**：崇宁三年（1104）41–43 界交子不再收兑；崇宁四年「令诸路更用钱引，准新样印制，四川如旧法」；大观元年（1107）改四川交子务为钱引务；「大观中，不蓄本钱而增造无艺，至引一缗当钱十数。及张商英秉政，奉诏复循旧法」；「宣和中……引价复平」。**→ 诸路钱引在大观年间崩溃收缩，1120 年汴京市面没有纸币可花。** | ✅（史实链）/ ⚠️（「汴京完全不用」为推论） |
| money.008 | **白银不是日常交易货币**：宋代白银主要作赏赐、军费、边籴、跨地区「轻赍」与大额支付，民间日常买卖用铜钱；《梦华录》里的「银」是**酒器**（会仙酒楼「即银近百两矣」）而非付账的钱。 | ✅（汪圣铎 T1 → 豆瓣笔记摘要）/ T0 银器旁证 |

## 4. §13 货币类误传（`tag: ❌`，只进「记者踩坑」与 prompt 负向词）

| fact_id | 误传 | 正解 | negative（prompt 负向词） |
|---|---|---|---|
| myth.money.001 | 宋人掏**银锭 / 碎银**买早点、结酒账 | 日常只用铜钱（串或散枚）；银是大额 / 官府 / 酒器 | 银锭、元宝、碎银、马蹄银、银子付账 |
| myth.money.002 | 掏**银票 / 交子**在汴京付账 | 交子 / 钱引以铁钱为本位、只在四川；汴京 1120 年无纸币 | 银票、纸钞、交子、钱庄票据 |
| myth.money.003 | 「一两银子 ＝ X 元人民币」 | 篮子锚定：只说「≈ 几天工钱 / 几斗米」 | —（口播禁语） |
| myth.money.004 | 「一贯 ＝ 数出 1 000 枚」 | 省陌：官 77、街市 75、鱼肉菜 72 | — |
| myth.money.005 | 钱面是**乾隆通宝**式清钱 / 背满文 | 北宋年号钱：熙宁 / 元丰 / 政和 / 宣和，篆隶对钱或瘦金体，背多光素 | 乾隆通宝、清代铜钱、满文、现代硬币 |
| myth.money.006 | **元宝形马蹄银锭** | 宋银为束腰**铤**形（ai_draft，待核） | 马蹄银锭、元宝形 |

## 5. 记者「今日账单」样例（锚：脚夫日工钱 100 文；米 250 文/斗）

| 站 | 花销 | 文 | ≈ 天工钱 | ≈ 斗米 | 出处 |
|---|---|---|---|---|---|
| 早市 | 笼饼 1 枚 + 蔬菜包子 1 个 | 10 | 0.10 | 0.04 | price.009 |
| 州桥 | 鹅鸭鸡兔肚肺包子 2 个 | 30 | 0.30 | 0.12 | price.001 |
| 州桥 | 造齏 1 碗 | 10 | 0.10 | 0.04 | price.004 |
| 行 | 租鞍马半日（记者不会骑，退了） | 100 | 1.00 | 0.40 | price.008 |
| 鱼行 | 车鱼 1 斤（送脚夫） | 100 | 1.00 | 0.40 | price.007 |
| 正店 | 银瓶酒 1 角 | 72 | 0.72 | 0.29 | price.005 |
| 正店 | 下酒 2 分 | 30 | 0.30 | 0.12 | price.002 |
| 住 | 客店 1 晚（⚠️ 待核） | 50 | 0.50 | 0.20 | price.017 |
| **合计** | | **402 文** | **≈ 4.0 天工钱** | **≈ 1.6 斗米** | |

口播句式（禁止折人民币）：「这一顿加住店，一共四百文出头——脚夫得扛**四天**。街市按七十五陌算，掏出去的其实是三百来枚钱。」
「我试试」用一贯（≈ 10 天工钱）吃遍早市：按上表，一贯够吃 25 天早点——**「吃遍」不难，「吃穷」难**，笑点在此。

## 6. fact YAML（机检）

```yaml
- fact_id: kaifeng.price.001
  claim: 州桥夜市梅家鹿家的鹅鸭鸡兔肚肺鳝鱼包子、鸡皮、腰肾、鸡碎，每个不过十五文
  tag: ✅
  source: 《东京梦华录》卷二「州桥夜市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  quote: "梅家鹿家鵝鴨雞免肚肺鱔魚包子、雞皮、腰腎、雞碎，每個不過十五文。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 0.15
  used_in: []
  prompt_string: "夜市摊上码着一屉屉肉馅包子、鸡皮、腰肾，摊主收几枚铜钱"
  negative: "银子、纸币、辣椒、玉米、塑料袋"

- fact_id: kaifeng.price.002
  claim: 小酒店下酒菜（煎鱼、鸭子、炒鸡兔、煎燠肉、梅汁、血羹、粉羹）每分不过十五钱
  tag: ✅
  source: 《东京梦华录》卷二「饮食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  quote: "其餘小酒店，亦賣下酒，如煎魚、鴨子、炒雞免、煎燠肉、梅汁、血羹、粉羹之類。每分不過十五錢。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 0.15
  used_in: []
  prompt_string: "小酒店案上一分煎鱼、一碗血羹，粗陶碗"
  negative: "银子付账、辣椒、红油"

- fact_id: kaifeng.price.003
  claim: 天晓早市酒店点灯烛沽卖，每分不过二十文，并粥饭点心
  tag: ✅
  source: 《东京梦华录》卷三「天晓诸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  quote: "酒店多點燈燭沽賣，每分不過二十文，並粥飯點心。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 0.2
  used_in: []
  prompt_string: "天未亮的酒店门口点着灯烛，卖粥饭点心"
  negative: "电灯、玻璃杯、纸币"

- fact_id: kaifeng.price.004
  claim: 食店以琉璃浅棱「碧碗」盛精细菜蔬「造齏」，每碗十文
  tag: ✅
  source: 《东京梦华录》卷四「食店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  quote: "吾輩入店，則用一等琉璃淺棱碗，謂之『碧碗』，亦謂之『造羹』，菜蔬精細，謂之『造齏』，每碗十文。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 0.1
  used_in: []
  prompt_string: "浅棱的碧色琉璃碗盛着切得极细的腌菜"
  negative: "塑料碗、不锈钢"

- fact_id: kaifeng.price.005
  claim: 遇仙正店银瓶酒七十二文一角，羊羔酒八十一文一角
  tag: ✅
  source: 《东京梦华录》卷二「宣德楼前省府宫宇」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  quote: "此一店最是酒店上戶，銀瓶酒七十二文一角，羊羔酒八十一文一角。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 0.72
  note: "「角」为宋代酒量单位，约一升上下（⚠️ 未核）"
  used_in: []
  prompt_string: "正店酒博士提着长嘴酒注，按角打酒"
  negative: "玻璃酒瓶、易拉罐、银子付账"

- fact_id: kaifeng.price.006
  claim: 正店以平头车载酒梢桶，每梢约三斗，一贯五百文（≈ 每升 50 文）
  tag: ✅
  source: 《东京梦华录》卷三「般载杂卖」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  quote: "酒正店多以此載酒梢桶矣。梢桶如長水桶，面安靨口，每梢三斗許，一貫五百文。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 15
  used_in: []
  prompt_string: "独牛平头车上立着几只长水桶样的酒梢桶，桶面安着靨口"
  negative: "塑料桶、玻璃瓶"

- fact_id: kaifeng.price.007
  claim: 冬月黄河远处客鱼「车鱼」每斤不上一百文
  tag: ✅
  source: 《东京梦华录》卷四「鱼行」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  quote: "冬用即黃河諸遠處客魚來，謂之『車魚』，每斤不上一百文。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 1.0
  note: "清明已非冬月，当日鱼价应低于此上限（⚠️）"
  used_in: []
  prompt_string: "鱼行浅木桶里养着活鱼，用秤论斤"
  negative: "电子秤、泡沫箱"

- fact_id: kaifeng.price.008
  claim: 出街市干事路远倦行，逐坊巷桥市有假赁鞍马者，不过百钱
  tag: ✅
  source: 《东京梦华录》卷四「杂赁」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  quote: "尋常出街市幹事，稍似路遠倦行，逐坊巷橋市，自有假賃鞍馬者，不過百錢。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 1.0
  used_in: []
  prompt_string: "桥市边拴着几匹备好鞍的租马，马夫候客"
  negative: "自行车、汽车、马鞍带镫铁现代款式"

- fact_id: kaifeng.price.009
  claim: 北宋开封城内 1 文买 7 颗枣、3 文买 1 个蔬菜包子、7 文买一枚笼饼；北宋中期 1 文买一个油糍
  tag: ✅
  source: 程民生《宋代物价研究》→ 搜狐「新书架」报道
  source_url: https://www.sohu.com/a/472999243_120952561
  quote: "1文可买7颗枣；3文可以买1个蔬菜包子；7文可以买一枚笼饼；1文钱可以买一个油糍"
  quote_kind: 逐字
  tier: T1→T3
  verified_by: ai_read
  days_wage: 0.07
  used_in: []
  prompt_string: "笼屉里的笼饼冒着热气，一枚七文"
  negative: "银子、纸币"

- fact_id: kaifeng.price.010
  claim: 北宋后期洛阳 10 文钱买 1 碗羹
  tag: ✅
  source: 程民生《宋代物价研究》→ 搜狐「新书架」报道
  source_url: https://www.sohu.com/a/472999243_120952561
  quote: "10文钱可以买1碗羹（北宋后期洛阳）"
  quote_kind: 逐字
  tier: T1→T3
  verified_by: ai_read
  days_wage: 0.1
  used_in: []
  prompt_string: "粗陶碗盛的热羹"
  negative: "塑料碗"

- fact_id: kaifeng.price.011
  claim: 宋英宗治平末年猪、羊肉三四十钱一斤
  tag: ✅
  source: 《续资治通鉴长编》→ 搜狐「宋代食品价格（食品篇上）」
  source_url: https://www.sohu.com/a/680938614_121687424
  quote: "猪、羊肉三四十钱一斤（宋英宗治平末年，出处：《续资治通鉴长编》）"
  quote_kind: 摘要
  tier: T0→T3
  verified_by: ai_read
  days_wage: 0.35
  note: "距 1120 年逾 50 年；宣和末应高于此"
  used_in: []
  prompt_string: "肉案上挂着整扇羊肉，屠户论斤切"
  negative: "塑料袋、电子秤"

- fact_id: kaifeng.price.012
  claim: 大观年间牛肉每斤 100 文
  tag: ⚠️
  source: 搜狐「宋代食品价格（食品篇上）」（转述臣僚奏语）
  source_url: https://www.sohu.com/a/680938614_121687424
  quote: "牛肉一斤100文（大观年间）"
  quote_kind: 摘要
  tier: T3
  verified_by: ai_read
  days_wage: 1.0
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.013
  claim: 北宋末羊肉「每斤六十足」
  tag: ⚠️
  source: 搜狐「食品篇上」称出自《清明上河图》题记——来源可疑，待核
  source_url: https://www.sohu.com/a/680938614_121687424
  quote: "「每斤六十足」羊肉（北宋末年）"
  quote_kind: 摘要
  tier: T3
  verified_by: ai_read
  days_wage: 0.6
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.014
  claim: 熙丰间绢每匹市价约 1 贯足
  tag: ⚠️
  source: 《宋会要辑稿》→ 知乎「北宋熙丰经济年鉴」（搜索摘要；原页 403）
  source_url: https://zhuanlan.zhihu.com/p/604559787
  quote: "熙丰间和买岁额当不下于300万匹，每匹市价1贯足"
  quote_kind: 摘要
  tier: T0→T3
  verified_by: ai_read
  days_wage: 10
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.015
  claim: 元丰元年成都府路夏税布每匹估钱 420 文足
  tag: ⚠️
  source: 《宋会要辑稿》→ 知乎「北宋熙丰经济年鉴」（搜索摘要）
  source_url: https://zhuanlan.zhihu.com/p/604559787
  quote: "元丰元年（1078），成都府路夏税布每匹估钱420文足"
  quote_kind: 摘要
  tier: T0→T3
  verified_by: ai_read
  days_wage: 4.2
  note: "蜀地官估，非汴京市价"
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.016
  claim: 宋代蜡烛每根 150–400 文，约合城市下层平民两三天收入
  tag: ⚠️
  source: 程民生《宋代物价研究》→ 吴钩「宋人用什么照明」（搜索摘要；儒家网 403）
  source_url: https://www.rujiazg.com/article/8080
  quote: "宋代每根蜡烛的价格为150至400文不等，相当于一名城市下层平民两三天的收入"
  quote_kind: 摘要
  tier: T1→T2
  verified_by: ai_read
  days_wage: 2.5
  used_in: []
  prompt_string: "客店里只点一盏油灯，蜡烛是奢侈品"
  negative: "电灯、LED"

- fact_id: kaifeng.price.017
  claim: 宋代普通客店住一晚约 50 文
  tag: ⚠️
  source: 搜索摘要（网文），无史源
  source_url: https://m.chuangshi.qq.com/read/50303246/5
  quote: ""
  quote_kind: 无
  tier: T3
  verified_by: ai_draft
  days_wage: 0.5
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.018
  claim: 茶饮子一碗约 1–3 文（估）
  tag: ⚠️
  source: 未查
  source_url: ""
  quote: ""
  quote_kind: 无
  tier: T4
  verified_by: ai_draft
  days_wage: 0.02
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.019
  claim: 汴河渡船船资 / 过虹桥费用
  tag: ⚠️
  source: 未查；《东京梦华录》无桥费记载
  source_url: ""
  quote: ""
  quote_kind: 无
  tier: T4
  verified_by: ai_draft
  days_wage: null
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.020
  claim: 清明纸马铺当街以纸衮叠成楼阁之状（价未载）
  tag: ⚠️
  source: 《东京梦华录》卷七「清明节」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  quote: "士庶闐塞諸門，紙馬鋪皆於當街用紙袞疊成樓閣之狀。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: null
  note: "形制 ✅，价格未查 → 价格为 ai_draft"
  used_in: []
  prompt_string: "纸马铺门口用彩纸叠成小楼阁"
  negative: "塑料花、印刷冥币"

- fact_id: kaifeng.price.021
  claim: 清明轿子以杨柳杂花装簇顶上，四垂遮映（柳枝不计价）
  tag: ✅
  source: 《东京梦华录》卷七「清明节」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  quote: "轎子即以楊柳雜花裝簇頂上，四垂遮映。"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  days_wage: 0
  used_in: []
  prompt_string: "小轿顶上插满新折的杨柳与杂花，柳条四面垂下"
  negative: "塑料花、玻璃窗"

- fact_id: kaifeng.price.022
  claim: 宣和四年（1122）汴京米每斗 250–300 文；熙宁七年 80–100 文；熙宁二年 40 文；大中祥符二年粟 30 文
  tag: ✅
  source: 程民生《宋代物价研究》→ 澎湃「从《梦华录》聊宋代收入和物价」
  source_url: https://m.thepaper.cn/newsDetail_forward_19082518
  quote: "宣和四年（1122年），米价更是高达每斗250文—300文"
  quote_kind: 逐字
  tier: T1→T3
  verified_by: ai_read
  days_wage: 2.75
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.023
  claim: 大观年间一石米值 2 500 文（每斗 250 文）
  tag: ✅
  source: 程民生 → 搜狐「食品篇上」
  source_url: https://www.sohu.com/a/680938614_121687424
  quote: "一石米（相当于现在的125斤米）值2500文，一斤米为20文（大观年间）"
  quote_kind: 逐字
  tier: T1→T3
  verified_by: ai_read
  days_wage: 25
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.024
  claim: 北宋普通劳动者日收入约 100 文；一人最低生活费约 20 文/日；普通家庭日常费低于 100 文/日
  tag: ✅
  source: 程民生《宋人生活水平考察》+《宋代物价研究》
  source_url: https://www.wyzxwk.com/Article/zhonghua/2012/02/288165.html
  quote: "维持一个人生命的最低生活费，折合成铜钱约是20文左右；宋人家庭每天的日常费用，就普通百姓而言，大体低于100文（搜狐 472999243 逐字）；卖柴者日得百钱、淮西雇工日百文、渔民日约百文（乌有之乡页摘要）"
  quote_kind: 逐字+摘要
  tier: T1
  verified_by: ai_read
  days_wage: 1
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.price.025
  claim: 嘉祐六年纲运脚夫日薪 100 文；庆历七年余姚筑堤民夫日 125 文
  tag: ⚠️
  source: 仅搜索摘要；所指页面（中国社会科学网「两宋代役人论析」）不含此句
  source_url: https://cssn.cn/lsx/lsx_zgs/202210/t20221024_5552465.shtml
  quote: ""
  quote_kind: 无
  tier: T3
  verified_by: ai_draft
  days_wage: 1
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.money.001
  claim: 1120 年汴京主币为圆形方孔铜钱；徽宗六个年号钱并行，最新为宣和元年（1119）始铸的宣和通宝（篆/隶对钱，小平+折二，样本外径 3 cm）；崇宁通宝 Met 样本径 3.5 cm、瘦金体
  tag: ✅
  source: 萧山博物馆「北宋钱币（二）」+ 华东师大数字博物馆「宣和通宝」+ Met 75816
  source_url: https://z.hangzhou.com.cn/2022/syjy/content/content_8421398.html
  quote: "崇宁年间著有崇宁通宝小平和当十…除重宝为隶书外，其余为瘦金体；铸大观通宝大小几等，有小平、折二、折三、折五、当十；重和仅有三个月，所以数目很少；宣和通宝有小平和折二两等。（萧博）外径3cm，内径1cm（华东师大 宣和通宝）Diam. 3.5 cm, 1102–06, Copper alloy（Met 2013.43）"
  quote_kind: 逐字
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "一串青褐色圆形方孔铜钱，钱面「政和通宝」「宣和通宝」篆隶两体，钱背光素；不是清代乾隆通宝、不带满文"
  negative: "乾隆通宝、满文、现代硬币、金币、银元、纸币"

- fact_id: kaifeng.money.002
  claim: 省陌——官用 77、街市通用 75、鱼肉菜 72、金银 74、珠珍/雇婢/买虫蚁 68、文字 56 为百；官方定制「所在用七十七钱为百」
  tag: ✅
  source: 《东京梦华录》卷三「都市钱陌」；《宋史》卷 180 食货下二
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  quote: "都市錢陌，官用七十七，街市通用七十五，魚肉菜七十二陌，金銀七十四，珠珍、雇婢妮、買蟲蟻六十八，文字五十六陌，行市各有長短使用。／至是，詔所在用七十七錢為百。（宋史 https://zh.wikisource.org/wiki/宋史/卷180）"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "摊主数钱只数到七十几枚就算「一百」"
  negative: ""

- fact_id: kaifeng.money.003
  claim: 崇宁当十大钱私铸泛滥，政和元年（1111）诏改当十为当三
  tag: ✅
  source: 《宋史》卷 180 食货下二
  source_url: https://zh.wikisource.org/wiki/宋史/卷180
  quote: "政和元年詔：「錢重則物輕，錢輕則物重，其勢然也。今諸路所鑄小平錢，行之久而無弊…往歲圖利之臣鼓鑄當十錢，苟濟目前，不究悠久，公私為害…」"
  quote_kind: 逐字（节引）
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.money.004
  claim: 铁钱只行于四川、陕西；汴京用铜钱
  tag: ✅
  source: 《宋史》卷 180 食货下二
  source_url: https://zh.wikisource.org/wiki/宋史/卷180
  quote: "蜀平，聽仍用鐵錢／陝西行鐵錢／川、陝皆行鐵錢"
  quote_kind: 逐字（片段）
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "铁钱、锈铁色钱"

- fact_id: kaifeng.money.005
  claim: 交子/钱引以铁钱为本位、起初限四川；崇宁四年令诸路更用钱引而四川如旧法；大观中滥发至引一缗当钱十数，张商英复旧法；宣和中引价复平——1120 年汴京市面无纸币
  tag: ✅
  source: 《宋史》卷 181 食货下三「会子」；维基百科「交子」
  source_url: https://zh.wikisource.org/wiki/宋史/卷181
  quote: "四年，令諸路更用錢引，準新樣印製，四川如舊法。／大觀中，不蓄本錢而增造無藝，至引一緡當錢十數。及張商英秉政，奉詔復循舊法。／宣和中，商英錄奏當時所行，以為自舊法之用，至今引價復平。／起初限四川，之后普及…宋廷于崇宁三年（1104年）诏令第四十一至四十三界交子不再收兑…大观元年（1107年）易交子名为钱引（维基 https://zh.wikipedia.org/zh-hans/交子）"
  quote_kind: 逐字
  tier: T0
  verified_by: ai_read
  note: "「1120 汴京无纸币」是从大观崩溃 + 四川本位推出的结论，标 ⚠️ 供口播用「在汴京没人收纸币」"
  used_in: []
  prompt_string: ""
  negative: "银票、纸钞、交子"

- fact_id: kaifeng.money.006
  claim: 宋代白银主要作赏赐、军费、边籴、跨地区轻赍与大额支付，非民间日常市易货币；铜钱为主币与计价标准
  tag: ✅
  source: 汪圣铎《宋代货币与货币流通研究》→ 豆瓣读书笔记（第 2.3 / 3–4 章摘要）
  source_url: https://book.douban.com/annotation/15747489/
  quote: "白银主要作为大额交易与官府开支（赏赐、军费）的「轻赍」手段，而非日常商业媒介；铜钱为价值标准，铁钱与纸币面额均以铜钱计"
  quote_kind: 摘要
  tier: T1→T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "银锭、碎银、元宝、马蹄银"

- fact_id: kaifeng.money.007
  claim: 《梦华录》里的「银」是酒器：会仙酒楼两人对饮也用银器，「即银近百两矣」
  tag: ✅
  source: 《东京梦华录》卷四「会仙酒楼」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  quote: "即銀近百兩矣／雖一人獨飲，碗遂亦用銀盂之類"
  quote_kind: 逐字（片段）
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "正店桌上摆着银注碗、银盂——银子是餐具不是钱"
  negative: ""

- fact_id: kaifeng.money.008
  claim: 元丰年间全国年铸铜钱约 500 万贯（历朝之最），故 1120 年市面钱串中熙宁/元丰钱最多，新钱政和通宝次之
  tag: ⚠️
  source: 《宋会要辑稿·元丰铸钱》→ 雅昌「北宋元丰通宝钱铸巨量揭秘」（搜索摘要）
  source_url: https://m-news.artron.net/20180124/n982892.html
  quote: "铸铜钱17监，铸铁钱9监…年铸钱量达五百九十四万余贯，其中铸铜钱五百零万贯"
  quote_kind: 摘要
  tier: T0→T3
  verified_by: ai_read
  note: "「最常见」为铸量推断；建议 prop 卡以政和通宝 + 元丰通宝 为主样"
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.money.009
  claim: 【推测】省陌怎么用到一百文以下的小额买卖上，没查到史料。卷三只给出每「陌」（一百文）实际付几枚：官用七十七、街市通用七十五、鱼肉菜七十二等。余辉读《清明上河图》孙羊店肉铺的价牌作「□斤六十足」，说「足」字表明店家不收省陌钱贯、60 个铜钱不能少。这说明六十文这一级的零售价上，「足」还是「省」是要标明的，但仍然没说一笔二十文的买卖该数几枚。「二十文按七十五陌数十五枚」只是按比例推算出来的（20×75÷100＝15），不是史料记载
  tag: ⚠️
  source: 《东京梦华录》卷三「都市钱陌」＋ 余辉《如何走进北宋〈清明上河图〉中的世界》（极目新闻 2023-06-17）
  source_url:
    - https://zh.wikisource.org/wiki/東京夢華錄/卷三
    - https://www.ctdsb.net/c1664_202306/1794702.html
  quote: "都市錢陌，官用七十七，街市通用七十五，魚肉菜七十二陌，金銀七十四，珠珍、雇婢妮、買蟲蟻六十八，文字五十六陌，行市各有長短使用"；"屋檐下挂着一副羊肺，还有羊肠、羊肝、羊肚等内脏，上面还有一块价格牌：「□斤六十足」" / "这个『足』字，表明了店家不收『省陌』的钱贯，还真有些背景！60个铜钱不能少"（余辉）
  quote_kind: 逐字（余辉句为网页转录）
  tier: T0＋T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "—"
  note: 2026-09-14 W12_factfix 新增（回应 R6 W05）。检索过「省陌 零钱」「不足百文」「文足 文省」，只找到省陌的定义、各行的陌数，以及南宋价格里「文省」「文足」的标注，没有一条讲百文以下怎么数钱。判断：画面里「数十五枚付二十文」可以作为调度保留，但口播必须带推测口吻，例如「按七十五陌的比例算，二十文大概数十五枚；零钱到底怎么数，书上没写」，不能说成「二十文数十五枚就够」这样的确定句。余辉的「60 个铜钱不能少」和羊下水价属于「崇宁年间初期」，都是他对画面的解读，价牌第一个字看不清（□）⚠️；口播如果引这块牌子，要说「有学者读出来是」。
```

## 7. 参考图库统计 —— `2_世界观人设/props/p2_铜钱与钱串/`

已 `pull` **13 张**（≥ 8 门槛），全部开放许可（CC0 × 7、CC BY 2.0 × 2、CC BY 3.0 × 3、PD × 1）→ **均可入画**。逐张年号标注（Schjøth 编号 + 年代推断，需人眼核面文）：

| ref | 钱 | 许可 | 备注 |
|---|---|---|---|
| ref01 | 崇宁通宝（Met 2013.43，1102–06，径 3.5 cm，当十，瘦金体） | CC0 | 主样 ① |
| ref02 | 崇宁通宝 当十（S-621，1102–07，34 mm） | CC0 | |
| ref03 | 大观通宝 当十（S-630，1107–11，39 mm） | CC0 | 1120 已作当三用 |
| ref04 | 大观通宝 小平（S-629，24 mm） | CC0 | ⚠️ 年号按编号推断 |
| ref05 | **政和通宝 小平（S-634，1111–18，25 mm）** | CC0 | **主样 ②（1120 最普遍新钱）** |
| ref06 | 政和通宝 折二（S-639，1111–18，30 mm） | CC0 | |
| ref07 | 宣和通宝（Hartill 16.486） | CC BY 2.0 | 主样 ③ |
| ref08 | 宣和通宝（NR） | CC BY 2.0 | |
| ref09 | 宣和通宝 隶书 | CC BY 3.0 | 书体参考 |
| ref10 | 宣和通宝 篆书（铁钱，陕） | CC BY 3.0 | 只作书体参考——汴京不用铁钱 |
| ref11 | **北宋 200 文钱串** | CC BY 3.0 | **钱串主样** |
| ref12 | 三种北宋钱合影 | CC BY-SA 4.0 | |
| ref13 | 1899 钱铺穿钱（清末） | PD | 仅穿绳工艺参考，非宋 |

缺：**熙宁元宝 / 元丰通宝**（推断为 1120 年串中最多者）未拉图 → 下一轮 `search "Yuanfeng Tongbao"` 补 2–3 张。

## 8. 未能核实 / 待人眼

1. 1120 当年汴京米价（内插值）；日工钱用北宋均值——两项均进「本站存疑」。
2. 客店一晚 50 文、茶饮子一碗、船资/过桥、纸马价格——无史源，`ai_draft`。
3. 羊肉「每斤六十足」的出处（页面称《清明上河图》）可疑。
4. 绢 / 布 / 蜡烛三条只有搜索摘要（原页 403），需人眼开《宋会要》/ 程民生原书页。
5. 「角」的容量、一贯钱串的实际重量。
6. 宋银铤形制（myth.money.006）未抓到图与文。
7. 程民生《宋人生活水平考察》原文页两次抓取均被工具改写为摘要（乌有之乡 / 豆瓣），日收入三例需人眼核原句。

## 9. 来源（tier 分组）

- **T0**：《东京梦华录》卷二 / 卷三 / 卷四 / 卷七（维基文库 https://zh.wikisource.org/wiki/東京夢華錄/卷二 …/卷三 …/卷四 …/卷七）；《宋史》卷 180 食货下二 https://zh.wikisource.org/wiki/宋史/卷180 ；《宋史》卷 181 食货下三 https://zh.wikisource.org/wiki/宋史/卷181
- **T1**（经转述页抓取）：程民生《宋代物价研究》《宋人生活水平考察》 https://www.wyzxwk.com/Article/zhonghua/2012/02/288165.html ；汪圣铎《宋代货币与货币流通研究》 https://book.douban.com/annotation/15747489/
- **T2**：萧山博物馆「北宋钱币（二）」 https://z.hangzhou.com.cn/2022/syjy/content/content_8421398.html ；华东师大数字博物馆「宣和通宝」 https://digitalmuseum.ecnu.edu.cn/b3/02/c37317a439042/page.htm ；Met 75816 https://www.metmuseum.org/art/collection/search/75816 ；吴钩「宋人用什么照明」 https://www.rujiazg.com/article/8080（403）
- **T3**：澎湃 https://m.thepaper.cn/newsDetail_forward_19082518 ；搜狐 https://www.sohu.com/a/472999243_120952561 、 https://www.sohu.com/a/680938614_121687424 ；维基百科「交子」 https://zh.wikipedia.org/zh-hans/交子 ；知乎熙丰年鉴 https://zhuanlan.zhihu.com/p/604559787（403）；雅昌 https://m-news.artron.net/20180124/n982892.html
- **失败**：sohu 525765973（302→404）、rujiazg 26317 / 14649（403）、zhihu（403）、cssn 代役人页（不含所需句）、airmb post/54（空页）
