---
worker_id: W1_menghualu
stage: 0
role: researcher
angle: 城市志
status: complete
blockers: []
confidence: high
---

# W1 · 《东京梦华录》原文抽取 —— sk1 汴京 · 宣和二年（1120）· 清明日

> 抓取记录（2026-09-13）：维基文库《東京夢華錄》卷一 / 卷二 / 卷三 / 卷四 / 卷五 / 卷七 六卷，用 `action=raw` 拉的 wikitext 原文，本地副本存
> `.audit/adhoc_agents/2026-09-13/sk1-20260913-203500/spawns/W1_menghualu/raw_fetch/juan{1,2,3,4,5,7}.txt`；每条 `quote:` 都用 grep 在本地副本里核过存在。
> 维基文库是繁体，`quote:` 照抄繁体不转换（byte-identical 才能机检）；`claim:` / `prompt_string:` 用简体。
> `verified_by: ai_read` ＝ 我本次真的抓到页面并引用了原句；`ai_draft` ＝ 记忆 / 推算，**待核，不得进 prompt**。
> §11 / §12 真实人物的生卒官职来自中文维基百科（T3，只做索引，tag 一律 ⚠️），能用《东京梦华录》原文佐证的另立 T0 条。
> `source_url` 一律给卷的页面：`https://zh.wikisource.org/wiki/東京夢華錄/卷N`。

## 0 · 先说四条对 sk1 概念卡的纠正（都有原文）

1. **「每個不過十五文」不是旋煎羊白肠的价。** 卷二「州橋夜市」原句是「梅家鹿家鵝鴨雞免肚肺鱔魚包子、雞皮、腰腎、雞碎，每個不過十五文」——十五文是**包子 / 鸡皮 / 腰肾 / 鸡碎**的单价；「旋煎羊、白腸、鲊脯、黎凍魚頭」是下一句朱雀门一段的品名，无价。概念卡「一日时间线」那格要改。另：小酒店下酒「每分不過十五錢」（卷二「飲食果子」）可作替代锚。
2. **虹桥在城外**：「從東水門外七里曰虹橋」（卷一「河道」）。记者路线顺序应为 **虹桥（城外）→ 东水门（入城）→ 相国寺桥 / 相国寺 → 州桥 → 御街**，不是「东水门 → 虹桥」。
3. **州桥夜市是夜市**（「直至三更」），概念卡写的「州桥早市」在原文里对应的是：卷三「天曉諸人入市」（五更瓠羹店 / 灌肺炒肺 / 粥饭二十文）+ 卷二「東角樓街巷」潘楼下「每日自五更市合」。早市与夜市分两组镜。
4. **巡铺兵是夜巡**：「鋪兵五人，夜間巡警收領公事」（卷三「防火」）。白天在街上拦人属推测（⚠️），台词须口播「史书只写了夜巡」。

---

## §2 · 城市地图与街区（卷一「東都外城 / 舊京城 / 河道」+ 卷二「御街」+ 卷三）

汴河自西水门入城、东水门出城，城里城外共十三座桥；虹桥在东水门外七里、无柱木拱；州桥（天汉桥）低平青石、正对御街。清明日全城出郊，城南迎祥池「唯每歲清明日放萬姓燒香游觀一日」，城西金明池三月一日至四月八日开池。

```yaml
- fact_id: kaifeng.route.001
  claim: 外城周长四十余里，护城河「护龙河」宽十余丈，两岸种杨柳，粉墙朱门
  tag: ✅
  source: 《东京梦华录》卷一「東都外城」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "東都外城，方圓四十餘里。城壕曰護龍河，闊十餘丈，濠之內外，皆植楊柳，粉牆朱戶"
  used_in: []
  prompt_string: "汴京外城夯土包砖城墙，墙外一道十余丈宽的护城河，河两岸尽是杨柳，白粉墙朱红门"
  negative: "明清式青砖城楼、现代护栏、水泥河堤"

- fact_id: kaifeng.route.002
  claim: 东水门是汴河下游出城的水门，门跨河、铁裹栅门夜里像闸一样垂下，两岸各有旱门供行人
  tag: ✅
  source: 《东京梦华录》卷一「東都外城」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "東南曰東水門，乃汴河下流水門也，其門跨河，有鐵裹窗門，遇夜如閘垂下水面，兩岸各有門通人行路"
  used_in: []
  prompt_string: "横跨汴河的水门城楼，门洞里是铁皮包裹的栅栏门（白天吊起），河两岸各开一道供行人的旱门，门外夹岸百余丈的拐子城"
  negative: "石拱桥式城门、现代闸门机械、汉白玉栏杆"

- fact_id: kaifeng.route.003
  claim: 汴河自洛口分水入京，东至泗州入淮；东南的粮食与货物全由汴河进城，公私仰给
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "中曰汴河，自西京洛口分水入京城，東去至泗州，入淮。運東南之糧，凡東南方物，自此入京城，公私仰給焉"
  used_in: []
  prompt_string: "汴河穿城而过，河面上首尾相接的运粮漕船，船夫撑篙、岸上纤夫拉纤，东南来的货物都从这里进城"
  negative: "机动船、铁壳船、集装箱、现代桥梁"

- fact_id: kaifeng.route.004
  claim: 虹桥在东水门外七里，无桥柱，用巨木凌空叠架，刷朱红色，形如飞虹
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "從東水門外七里曰虹橋，其橋無柱，皆以巨木虛架，飾以丹雘，宛如飛虹"
  used_in: []
  prompt_string: "虹桥：横跨汴河的单孔木拱桥，桥下没有一根桥柱，粗大原木交叠成拱凌空架起，通体刷朱红色，像一道飞虹；桥在东水门外七里的城外"
  negative: "石拱桥、桥墩、石雕栏杆、白石桥、水泥桥"

- fact_id: kaifeng.route.005
  claim: 汴河上的「上土桥」「下土桥」与虹桥同为无柱木拱桥（同型桥共三座）
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "其上下土橋亦如之"
  used_in: []
  prompt_string: "汴河进城后的上土桥、下土桥与虹桥同样是无柱朱红木拱桥"
  negative: "石桥"

- fact_id: kaifeng.route.006
  claim: 自东水门溯汴河向西的桥序：虹桥（城外七里）→顺成仓桥→便桥（入水门）→下土桥→上土桥→相国寺桥→州桥
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "次曰順成倉橋，入水門裏曰便橋，次曰下土橋，次曰上土橋，投西角子門曰相國寺橋。次曰州橋"
  used_in: []
  prompt_string: "（路线用，不入画）记者沿汴河自东向西：虹桥→顺成仓桥→东水门→便桥→下土桥→上土桥→相国寺桥→州桥"
  negative: "—"

- fact_id: kaifeng.route.007
  claim: 州桥正名天汉桥，正对大内御街，桥身低平不通舟船，青石柱、石梁石笋栏杆，两岸石壁雕海马水兽飞云
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "州橋（正名天漢橋），正對於大內御街，其橋與相國寺橋皆低平不通舟船，唯西河平船可過，其柱皆青石為之"
  used_in: []
  prompt_string: "州桥：低平的青石平桥，青石桥柱密排桥下，石梁与石笋形栏杆，桥两岸的石护壁上浮雕海马、水兽、飞云纹，桥面正对北面的御街"
  negative: "高拱桥、木桥、红漆栏杆、汉白玉雕龙"

- fact_id: kaifeng.route.008
  claim: 州桥西侧停两只方浅船、船头架铁枪，岸上三条铁索夜里绞起拦河，防船只走失
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "橋之西有方淺舡二隻，頭置巨杆鐵鎗數條，岸上有鐵索三條，遇夜絞上水面，蓋防遺失舟船矣"
  used_in: []
  prompt_string: "州桥西侧河面上两只方头浅船，船头竖着几根带铁枪头的长杆；岸边绞盘上三条粗铁链垂进水里"
  negative: "现代缆绳、浮标、钢缆"

- fact_id: kaifeng.route.009
  claim: 御街自宣德楼南去，宽约二百余步，两边御廊；黑漆杈子隔行人，路心两行朱漆杈子围出御道，人马不得入
  tag: ✅
  source: 《东京梦华录》卷二「御街」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "各安立黑漆杈子，路心又安朱漆杈子兩行，中心御道，不得人馬行往，行人皆在廊下朱杈子之外"
  used_in: []
  prompt_string: "御街极宽，两边是带廊柱的御廊，廊前一排黑漆木栅栏（杈子），街心两行朱红漆木栅栏围出空无一人的御道，行人车马都挤在廊下栅栏外"
  negative: "行人走在街心、汽车、路灯、柏油路、行道树修剪整齐"

- fact_id: kaifeng.route.010
  claim: 御街杈子内有两道砖石御沟，宣和年间种满荷花，岸边桃李梨杏杂花相间——1120 年正是宣和二年
  tag: ✅
  source: 《东京梦华录》卷二「御街」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "杈子裏有磚石甃砌御溝水兩道，宣和間盡植蓮荷，近岸植桃李梨杏，雜花相間，春夏之間，望之如繡"
  used_in: []
  prompt_string: "御街两侧砖石砌岸的御沟，水里荷叶初生（清明时节荷花未开），岸边桃花李花梨花杏花正盛，杂色相间"
  negative: "荷花盛开、莲蓬、枯荷、樱花、现代花坛"

- fact_id: kaifeng.route.011
  claim: 相国寺在州桥之东临汴河大街，每月五次开放万姓交易；山门上卖飞禽猫犬，二三门内卖日用什物
  tag: ✅
  source: 《东京梦华录》卷三「大內前州橋東街巷」「相國寺內萬姓交易」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "相國寺每月五次開放萬姓交易，大三門上皆是飛禽貓犬之類，珍禽奇獸，無所不有"
  used_in: []
  prompt_string: "大相国寺山门内外的集市：山门下笼子里的飞禽猫狗，二门三门间彩布幕棚下摆着簟席、屏帏、鞍辔、弓剑、时果、腊脯"
  negative: "香客排队上香的现代寺庙、功德箱、电子屏"

- fact_id: kaifeng.route.012
  claim: 相国寺两廊是尼姑卖绣品、领抹、花朵、珠翠头面、销金幞头帽子
  tag: ✅
  source: 《东京梦华录》卷三「相國寺內萬姓交易」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "兩廊，皆諸寺師姑賣繡作、領抹、花朵、珠翠頭面、生色銷金花樣襆頭帽子"
  used_in: []
  prompt_string: "相国寺两侧廊下，尼姑们摆着绣件、领抹、绢花、珠翠头面和销金花样的幞头帽子"
  negative: "现代饰品、塑料花"

- fact_id: kaifeng.route.013
  claim: 州桥以南御街两边皆居民与铺席：车家炭、张家酒店、王楼山洞梅花包子、李家香铺、曹婆婆肉饼、李四分茶
  tag: ✅
  source: 《东京梦华录》卷二「宣德樓前省府宮宇」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "街東車家炭，張家酒店，次則王樓山洞梅花包子、李家香鋪、曹婆婆肉餅、李四分茶"
  used_in: []
  prompt_string: "州桥南御街东侧一溜铺面：炭铺、酒店、包子铺、香铺、肉饼铺、分茶食店，各挂布幌"
  negative: "统一制式招牌、霓虹灯、玻璃橱窗"

- fact_id: kaifeng.route.014
  claim: 城南迎祥池每年只在清明日一天向百姓开放烧香游观
  tag: ✅
  source: 《东京梦华录》卷二「朱雀門外街巷」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "近東即迎祥池，夾岸垂楊，菰蒲蓮荷，鳧雁游泳其間，橋亭臺榭，棋佈相峙，唯每歲清明日放萬姓燒香游觀一日"
  used_in: []
  prompt_string: "迎祥池：两岸垂杨，水里菰蒲初生、野鸭大雁游弋，桥亭台榭错落；清明这一天池门大开，百姓涌进来烧香游玩"
  negative: "荷花盛开、现代公园设施"

- fact_id: kaifeng.route.015
  claim: 金明池在城西顺天门（新郑门）外街北，三月一日开池，至四月八日闭池，风雨无阻有游人
  tag: ✅
  source: 《东京梦华录》卷七「三月一日開金明池瓊林苑」「駕回儀衛」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "三月一日，州西順天門外開金明池瓊林苑"；"自三月一日至四月八日閉池，雖風雨亦有遊人，略無虛日矣"
  used_in: []
  prompt_string: "金明池：周长约九里的方形大池，池中仙桥三拱朱漆栏杆、中央隆起如驼峰，桥尽头五座水殿坐在池心，东岸垂杨夹墙、彩棚幕次连成一片"
  negative: "现代游船、水泥岸、喷泉"

- fact_id: kaifeng.route.016
  claim: 南薰门正对大内，士庶殡葬车舆不许经此门出；但民间所宰猪都从此门入城，每日傍晚每群上万头，只十几人驱赶
  tag: ✅
  source: 《东京梦华录》卷二「朱雀門外街巷」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "唯民間所宰豬，須從此入京，每日至晚，每群萬數，止十數人驅逐，無有亂行者"
  used_in: []
  prompt_string: "傍晚南薰门外，成千上万头黑猪列队进城，只有十几个赶猪人拿着长鞭，猪群不乱"
  negative: "粉白色现代肉猪、卡车运猪"

- fact_id: kaifeng.route.017
  claim: 每坊巷三百步有一军巡铺（铺兵五人），高处砖砌望火楼，楼上有人瞭望
  tag: ✅
  source: 《东京梦华录》卷三「防火」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "每坊巷三百步許，有軍巡鋪屋一所，鋪兵五人，夜間巡警收領公事。又於高處磚砌望火樓，樓上有人卓望"
  used_in: []
  prompt_string: "街角一座小小的军巡铺屋，五个铺兵；坊巷高处一座砖砌的望火楼，楼顶有人瞭望"
  negative: "现代消防站、消防车、警灯"

- fact_id: kaifeng.route.018
  claim: 果子行在朱雀门外与州桥之西，纸画儿也在那里贩卖
  tag: ✅
  source: 《东京梦华录》卷三「天曉諸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "如果木亦集於朱雀門外及州橋之西，謂之果子行。紙畫兒亦在彼處，行販不絕"
  used_in: []
  prompt_string: "州桥西侧的果子行：一筐筐时鲜果子摆在街边，旁边挂着卖纸画儿的摊子"
  negative: "塑料筐、印刷海报"
```

### 清明日记者路线（每个停靠点 → 对应原文 fact）

| # | 时段 | 停靠点 | 原文依据 | 建议 shot 组 |
|---|---|---|---|---|
| 1 | 卯时 | **虹桥**（城外东水门外七里）：纲船过桥、桥上人流、桥头元丰仓 / 顺成仓前「袋家」扛袋 | route.004 / route.005 / job.001 | 一镜到底起点（概念卡「虹桥桥头低角度侧跟」） |
| 2 | 辰时 | **东水门**入城：跨河水门、铁裹栅门吊起、两岸旱门；「卖麦面一宛」的太平车从城外守门入城 | route.002 / job.024 | 进城过关（时辰 / 货币障碍点） |
| 3 | 巳时 | **相国寺桥 → 相国寺**（若逢每月五次开放日）：山门飞禽猫犬、两廊尼姑绣品 | route.011 / route.012 | 「逛街解说」组 |
| 4 | 午时 | **州桥**：青石低桥、海马水兽石壁、西侧防船铁索；桥西果子行 | route.007 / route.008 / route.018 | 一镜到底终点＝州桥街口，画外报物价 |
| 5 | 未时 | **御街**北望宣德楼：黑杈子 / 朱杈子 / 御沟荷叶初生、桃李梨杏；被巡铺兵拦（⚠️ 白天拦人为推测） | route.009 / route.010 / job.012 | 入侵者笑点 |
| 6 | 申时 | **出城踏青**二选一：城南**迎祥池**（清明日唯一开放日）/ 城西顺天门外**金明池**（三月一日至四月八日开池，清明是否在窗口内 ⚠️ 见 festival.017） | route.014 / route.015 / festival.007 | 四野如市、轿顶插柳 |
| 7 | 酉时 | **南薰门**外猪群入城（可作日落转场） | route.016 | 远景转场 |
| 8 | 戌–三更 | **州桥夜市**：自州桥南去到龙津桥，「直至三更」 | food.001–food.005 | 正店晚饭 + 总账单 |

---

## §4 · 食（卷二「州橋夜市」「酒樓」「飲食果子」+ 卷三「天曉諸人入市」「馬行街鋪席」+ 卷四「食店 / 肉行 / 餅店 / 魚行」+ 卷五「民俗」+ 卷七）

有原文的食物 > 30 种；正店七十二户、其余皆脚店；州桥夜市营业「直至三更」，马行街「才五更又復開張」；筷子已取代匙；酒店对坐必用一副注碗两副盘盏。

```yaml
- fact_id: kaifeng.food.001
  claim: 州桥夜市从州桥往南沿街摆：水饭、爊肉、干脯；王楼前獾儿、野狐、肉脯、鸡
  tag: ✅
  source: 《东京梦华录》卷二「州橋夜市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "自州橋南去，當街水飯、爊肉、乾脯。王樓前獾兒、野狐、肉脯、雞"
  used_in: []
  prompt_string: "夜市摊上粗陶盆里的泡饭（水饭）、酱色炖肉、风干肉脯，案板上挂着整只獾、野狐和鸡"
  negative: "辣椒、红油、玉米、番茄、土豆、塑料袋、一次性餐盒"

- fact_id: kaifeng.food.002
  claim: 梅家鹿家的鹅鸭鸡兔肚肺鳝鱼包子、鸡皮、腰肾、鸡碎，每个不过十五文（注：十五文是这些，不是羊白肠）
  tag: ✅
  source: 《东京梦华录》卷二「州橋夜市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "梅家鹿家鵝鴨雞免肚肺鱔魚包子、雞皮、腰腎、雞碎，每個不過十五文"
  used_in: []
  prompt_string: "笼屉里冒着热气的肉包子，摊主用竹签挑给客人，一个十五文（一枚枚铜钱点数）"
  negative: "纸币、银锭、白面馒头式无褶包子"

- fact_id: kaifeng.food.003
  claim: 朱雀门一段卖旋煎羊白肠、鲊脯、冻鱼头、姜豉、抹脏、红丝、批切羊头、辣脚子、姜辣萝卜（维基文库断句「旋煎羊、白腸」，通行本作「旋煎羊白腸」；「黎凍」通行本作「㸇凍」）
  tag: ✅
  source: 《东京梦华录》卷二「州橋夜市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "至朱雀門，旋煎羊、白腸、鲊脯、黎凍魚頭、薑豉類子、抹臟、紅絲、批切羊頭、辣腳子、姜辣蘿蔔"
  used_in: []
  prompt_string: "铁鏊子上现煎的羊白肠切段、腌鱼干、冻成琥珀状的鱼头冻、切成薄片的羊头肉、姜丝拌萝卜，用粗陶碗盛放"
  negative: "辣椒、红油、玉米、番茄、土豆、孜然烤串"

- fact_id: kaifeng.food.004
  claim: 夏月饮子与冷食：麻腐鸡皮、麻饮细粉、素签沙糖、冰雪冷元子、甘草冰雪凉水、荔枝膏（清明时未必上市 ⚠️）
  tag: ✅
  source: 《东京梦华录》卷二「州橋夜市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "夏月麻腐雞皮、麻飲細粉、素簽紗糖、冰雪冷元子、水晶皂兒"；"甘草冰雪涼水、荔枝膏"
  used_in: []
  prompt_string: "（夏季专用）饮子摊：粗陶罐里的甘草凉水、荔枝膏，木勺舀进小陶碗"
  negative: "玻璃杯、吸管、冰块机、塑料杯"

- fact_id: kaifeng.food.005
  claim: 州桥夜市一直摆到龙津桥，叫「杂嚼」，营业直至三更；马行街夜市三更尽、五更又开张
  tag: ✅
  source: 《东京梦华录》卷二「州橋夜市」；卷三「馬行街鋪席」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "直至龍津橋須腦子肉止，謂之雜嚼，直至三更"；"夜市直至三更盡，才五更又復開張。如要鬧去處，通曉不絕"
  used_in: []
  prompt_string: "深夜的州桥夜市，摊上油灯和灯笼连成一线，人流未散"
  negative: "电灯、霓虹、路灯杆"

- fact_id: kaifeng.food.006
  claim: 在京正店七十二户，其余都叫「脚店」
  tag: ✅
  source: 《东京梦华录》卷二「酒樓」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "在京正店七十二戶，此外不能遍數，其餘皆謂之『腳店』"
  used_in: []
  prompt_string: "（旁白用）汴京有七十二家正店（能自己酿酒的大酒楼），其余小酒店都叫脚店"
  negative: "—"

- fact_id: kaifeng.food.007
  claim: 京师酒店门口都扎彩楼欢门；瓠羹店门前用方木和花样扎成山棚，挂着整边猪羊二三十边，门面窗户朱绿装饰
  tag: ✅
  source: 《东京梦华录》卷二「酒樓」；卷四「食店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "凡京師酒店，門首皆縛彩樓歡門"；"門前以枋木及花樣啟結縛如山棚，上掛成邊豬羊，相間三二十邊"
  used_in: []
  prompt_string: "酒店门口用木杆和彩帛扎起的高大彩楼欢门，门面窗棂朱红与绿色相间；食店门前的木棚上挂着一排整边的猪羊"
  negative: "现代招牌、灯箱、卷帘门、玻璃门"
  note: 2026-09-14 SYNC_sk1（回应 R4 F36）：claim 里「门面窗户朱绿装饰」写的是瓠羹店，quote 没收这一句，prompt_string 却把「窗棂朱红与绿色相间」写到了酒店门面上。sk1 的酒店 / 脚店门面按 style_guide §2 色锁取素木灰褐（p7 / p9 卡已改），不据本条画朱绿窗棂。

- fact_id: kaifeng.food.008
  claim: 遇仙正店酒价：银瓶酒七十二文一角，羊羔酒八十一文一角
  tag: ✅
  source: 《东京梦华录》卷二「宣德樓前省府宮宇」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "此一店最是酒店上戶，銀瓶酒七十二文一角，羊羔酒八十一文一角"
  used_in: []
  prompt_string: "（物价用）正店里一角银瓶酒七十二文、羊羔酒八十一文"
  negative: "—"

- fact_id: kaifeng.food.009
  claim: 小酒店下酒菜：煎鱼、鸭子、炒鸡兔、煎燠肉、梅汁、血羹、粉羹，每份不过十五钱
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "其餘小酒店，亦賣下酒，如煎魚、鴨子、炒雞免、煎燠肉、梅汁、血羹、粉羹之類。每分不過十五錢"
  used_in: []
  prompt_string: "脚店桌上的煎鱼、炒鸡、血羹、粉羹几碟小菜，每碟十五文以内"
  negative: "辣椒、红油、玉米、番茄、土豆"

- fact_id: kaifeng.food.010
  claim: 胡饼店卖门油、菊花、宽焦、侧厚、油碢、髓饼、新样、满麻；每案三五人擀剂子按花入炉；五更擀案声远近相闻；大店五十余炉
  tag: ✅
  source: 《东京梦华录》卷四「餅店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "每案用三五人捍劑卓花入爐。自五更卓案之聲遠近相聞"；"每家有五十餘爐"
  used_in: []
  prompt_string: "胡饼铺：几个伙计围着木案擀面剂、按花纹，贴进一排泥炉，出炉的是芝麻满面的圆饼（满麻）与厚边饼（侧厚）"
  negative: "电烤箱、馕坑、披萨"

- fact_id: kaifeng.food.011
  claim: 油饼店卖蒸饼、糖饼、装合、引盘
  tag: ✅
  source: 《东京梦华录》卷四「餅店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "若油餅店，即賣蒸餅、糖餅、裝合、引盤之類"
  used_in: []
  prompt_string: "油饼铺案上摞着白胖的蒸饼（宋人叫蒸饼、即后世馒头）和糖饼"
  negative: "—"

- fact_id: kaifeng.food.012
  claim: 天亮前瓠羹店门口小孩叫卖饶骨头，间有灌肺和炒肺
  tag: ✅
  source: 《东京梦华录》卷三「天曉諸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "如瓠羹店門首坐一小兒，叫饒骨頭，間有灌肺及炒肺"
  used_in: []
  prompt_string: "五更天瓠羹店门口，一个小孩坐着叫卖，案上是灌肺、炒肺"
  negative: "—"

- fact_id: kaifeng.food.013
  claim: 早市酒店点灯卖粥饭点心，每份不过二十文；还有卖洗面水、煎点汤茶药的，直到天明
  tag: ✅
  source: 《东京梦华录》卷三「天曉諸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "酒店多點燈燭沽賣，每分不過二十文，並粥飯點心。亦間或有賣洗面水，煎點湯茶藥者，直至天明"
  used_in: []
  prompt_string: "天没亮的街口，酒店点着油灯卖粥饭点心；旁边摊子上小炉煎着汤茶药，热气冒出来"
  negative: "电灯、保温桶、纸杯"

- fact_id: kaifeng.food.014
  claim: 大食店叫「分茶」，菜单有头羹、石髓羹、白肉、胡饼、软羊、大小骨角、炙腰子、桐皮面、姜泼刀、冷淘；另有川饭店、南食店
  tag: ✅
  source: 《东京梦华录》卷四「食店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "大凡食店，大者謂之『分茶』，則有頭羹、石髓羹、白肉、胡餅、軟羊、大小骨角、炙犒腰子"
  used_in: []
  prompt_string: "分茶食店的堂里，桌上摆着头羹、白肉、软羊、胡饼、桐皮面等碗碟"
  negative: "辣椒、红油、玉米、番茄、土豆"

- fact_id: kaifeng.food.015
  claim: 食店用琉璃浅棱碗（碧碗），每碗十文；从前只用匙，如今都用筷子
  tag: ✅
  source: 《东京梦华录》卷四「食店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "則用一等琉璃淺棱碗，謂之『碧碗』"；"每碗十文"；"舊只用匙，今皆用箸矣"
  used_in: []
  prompt_string: "浅口有棱的青绿色琉璃碗盛着羹面，客人用竹筷子吃，每碗十文"
  negative: "刀叉、勺子为主食具、不锈钢餐具"

- fact_id: kaifeng.food.016
  claim: 客人坐下，一人拿筷子和纸遍问点菜；跑堂「行菜」左手叉三碗、右臂从手到肩摞约二十碗，分毫不错
  tag: ✅
  source: 《东京梦华录》卷四「食店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "客坐，則一人執箸紙，遍問坐客"；"行菜者左手杈三碗、右臂自手至肩馱疊約二十碗"
  used_in: []
  prompt_string: "跑堂伙计左手叉着三只碗、右臂从手腕到肩头摞着二十来只碗穿过堂中，一碗不洒"
  negative: "托盘、餐车"

- fact_id: kaifeng.food.017
  claim: 坊巷桥市到处有肉案，三五人操刀，阔切、片批、细抹、顿刀随客索唤；傍晚有燠爆熟食上市
  tag: ✅
  source: 《东京梦华录》卷四「肉行」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "坊巷橋市，皆有肉案，列三五人操刀，生熟肉從便索喚，闊切、片批、細抹、頓刀之類"
  used_in: []
  prompt_string: "桥头肉案：三五个屠夫各执一把宽刀，生熟肉按客人要的切法当场切"
  negative: "电子秤、冷柜、保鲜膜"

- fact_id: kaifeng.food.018
  claim: 卖生鱼用浅抱桶，柳叶间串浸在清水里沿街卖；每天早上从新郑门、西水门、万胜门进城的生鱼有数千担；冬天黄河远处来的「车鱼」每斤不过一百文
  tag: ✅
  source: 《东京梦华录》卷四「魚行」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "賣生魚則用淺抱桶，以柳葉間串清水中浸，或循街出賣"；"車魚，每斤不上一百文"
  used_in: []
  prompt_string: "鱼贩挑着两只浅木桶，桶里清水中活鱼用柳条穿着，沿街叫卖"
  negative: "泡沫箱、氧气泵、塑料盆"

- fact_id: kaifeng.food.019
  claim: 酒店里外来托卖：炙鸡、燠鸭、羊脚子、点羊头、脆筋巴子、姜虾、酒蟹、獐巴、鹿脯、海鲜时果、旋切莴苣生菜、西京笋
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "又有外來托賣炙雞、燠鴨、羊腳子、點羊頭、脆筋巴子、薑蝦、酒蟹、獐巴、鹿脯、從食蒸作、海鮮時果、旋切萵苣生菜、西京筍"
  used_in: []
  prompt_string: "小贩托着木盘在酒客间穿行，盘里烤鸡、酒蟹、鹿脯、现切的莴苣生菜"
  negative: "—"

- fact_id: kaifeng.food.020
  claim: 卖辣菜的小孩穿白虔布衫、系青花手巾、夹着白瓷缸子
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "又有小兒子，著白虔布衫，青花手巾，挾白磁缸子，賣辣菜"
  used_in: []
  prompt_string: "卖辣菜的小伙计：白色粗布衫、腰间青花布手巾，腋下夹一只白瓷缸子"
  negative: "印花T恤、塑料桶"

- fact_id: kaifeng.food.021
  claim: 干果子托盘卖：旋炒银杏、栗子、河北鹅梨、梨条梨干、胶枣、核桃、榛子、榧子；蜜煎果子都用梅红匣儿盛
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」「州橋夜市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "又有托小盤賣乾果子，乃旋炒銀杏、栗子、河北鵝梨、梨條、梨乾、梨肉、膠棗、棗圈"；"皆用梅紅匣兒盛貯"
  used_in: []
  prompt_string: "小贩托盘里现炒的银杏和栗子、梨干、枣圈，蜜饯装在梅红色的小木匣里"
  negative: "塑料包装、花生、瓜子（花生明以前无）"

- fact_id: kaifeng.food.022
  claim: 后街「院子」里的小民每日卖蒸梨枣、黄糕麋、宿蒸饼、发芽豆
  tag: ✅
  source: 《东京梦华录》卷三「諸色雜賣」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "皆小民居止，每日賣蒸梨棗、黃糕麋、宿蒸餅、發牙豆之類"
  used_in: []
  prompt_string: "后巷小摊上蒸熟的梨和枣、黄米糕、隔夜的蒸饼、发了芽的豆子"
  negative: "—"

- fact_id: kaifeng.food.023
  claim: 清明节坊市卖稠饧、麦糕、乳酪、乳饼；出城人各带枣锢、炊饼、黄胖（泥偶）、掉刀、鸭卵鸡雏，叫「门外土」
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "節日坊市賣稠餳、麥糕、乳酪、乳餅之類"；"各攜棗錮、炊餅，黃胖、掉刀，名花異果，山亭戲具，鴨卵雞芻，謂之『門外土』"
  used_in: []
  prompt_string: "清明街市摊上麦芽糖稀（稠饧）、麦糕、乳酪、乳饼；踏青的人提着枣糕炊饼、泥娃娃、小木刀、鸭蛋和小鸡"
  negative: "青团（吴地后起）、塑料玩具"

- fact_id: kaifeng.food.024
  claim: 金明池池上饮食：水饭、凉水绿豆、螺蛳肉、梅花酒、查片杏片梅子、香药脆梅、旋切鱼脍、青鱼、盐鸭卵、杂和辣菜
  tag: ✅
  source: 《东京梦华录》卷七「池苑內縱人關撲遊戲」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "池上飲食：水飯、涼水菉豆、螺螄肉、饒梅花酒，查片，杏片、梅子、香藥脆梅、旋切魚膾、青魚、鹽鴨卵、雜和辣菜之類"
  used_in: []
  prompt_string: "池边酒摊：现切的生鱼片、螺蛳肉、咸鸭蛋、梅花酒，粗陶碗与竹箸"
  negative: "芥末、酱油碟（日式）、辣椒"

- fact_id: kaifeng.food.025
  claim: 酒店里不论何人，两人对坐也要一副注碗、两副盘盏、五片果菜碟、三五只水菜碗，银器近百两；贫下人家叫酒也用银器送
  tag: ✅
  source: 《东京梦华录》卷四「會仙酒樓」；卷五「民俗」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "止兩人對坐飲酒，亦須用註碗一副，盤盞兩副，果菜碟各五片，水菜碗三五隻，即銀近百兩矣"；"以至貧下人家，就店呼酒，亦用銀器供送"
  used_in: []
  prompt_string: "酒桌上一套银注碗（温酒的注子坐在碗里）、两副银盘盏、五只小碟果菜、几碗水菜，两人对坐"
  negative: "高脚玻璃杯、瓷茶杯当酒杯、塑料托盘"

- fact_id: kaifeng.food.026
  claim: 正店见脚店来打过两三次酒，就敢借三五百两银器；妓馆也只是向店里叫酒
  tag: ✅
  source: 《东京梦华录》卷五「民俗」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "其正酒店戶，見腳店三兩次打酒，便敢借與三五百兩銀器"
  used_in: []
  prompt_string: "（旁白 / 采访用）脚店的酒和银器都是从正店打来借来的"
  negative: "—"

- fact_id: kaifeng.food.027
  claim: 卖饮食的人盘合器皿、车担用具都装得鲜洁精巧，不敢草率
  tag: ✅
  source: 《东京梦华录》卷五「民俗」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "凡百所賣飲食之人，裝鮮凈盤合器皿，車檐動使，奇巧可愛，食味和羹，不敢草略"
  used_in: []
  prompt_string: "小食摊的木盘食盒擦得干净、器皿精巧，摊子收拾得利落"
  negative: "脏乱破旧的摊位、塑料布"

- fact_id: kaifeng.food.028
  claim: 市井经纪人家往往只在市店随时买饭吃，家里不备菜
  tag: ✅
  source: 《东京梦华录》卷三「馬行街鋪席」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "市井經紀之家，往往只於市店旋置飲食，不置家蔬"
  used_in: []
  prompt_string: "（餐制旁白用）汴京做买卖的人家三餐多在外面买，家里不开伙"
  negative: "—"

- fact_id: kaifeng.food.029
  claim: 平头车专给正店运酒梢桶，梢桶像长水桶，每桶三斗许，一贯五百文
  tag: ✅
  source: 《东京梦华录》卷三「般載雜賣」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "酒正店多以此載酒梢桶矣。梢桶如長水桶，面安靨口，每梢三斗許，一貫五百文"
  used_in: []
  prompt_string: "独牛拉的平头车上码着一排长条木酒桶（梢桶），桶面开小口"
  negative: "玻璃酒瓶、铁皮桶"

- fact_id: kaifeng.food.030
  claim: 都市钱陌：官用七十七文作一陌，街市通用七十五，鱼肉菜七十二，金银七十四（短陌制——「一百文」实付不足百）
  tag: ✅
  source: 《东京梦华录》卷三「都市錢陌」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "都市錢陌，官用七十七，街市通用七十五，魚肉菜七十二陌，金銀七十四"
  used_in: []
  prompt_string: "（货币用，交 §7）一贯钱是十陌，街市一陌只数七十五枚铜钱、买鱼肉菜只数七十二枚——记者数钱会被纠正"
  negative: "银锭、银票、纸币"

- fact_id: kaifeng.food.031
  claim: 三更以后才有提瓶卖茶的人上街，因为都人公私忙碌深夜方归
  tag: ✅
  source: 《东京梦华录》卷三「馬行街鋪席」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "至三更方有提瓶賣茶者。蓋都人公私榮幹，夜深方歸也"
  used_in: []
  prompt_string: "深夜提着长嘴茶瓶沿街卖茶的人"
  negative: "保温杯、纸杯"
```

---

## §8 · 职业与社会阶层（卷一「外諸司」+ 卷二「飲食果子」+ 卷三「般載雜賣 / 雇覓人力 / 防火 / 天曉 / 諸色雜賣」+ 卷四「雜賃 / 食店」+ 卷五「民俗」+ 卷七）

记者会碰到的人（含 1 官吏＝军巡铺兵、1 商贩＝饼店/鱼贩、1 女性＝焌糟、1 底层＝袋家脚夫）。各行衣装「各有本色，不敢越外」——这是 §3 衣的 T0 骨架。

```yaml
- fact_id: kaifeng.job.001
  claim: 仓前的「袋家」每人肩扛两石布袋；仓里一有支遣，仓前便成集市；虹桥旁就有元丰仓、顺成仓
  tag: ✅
  source: 《东京梦华录》卷一「外諸司」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  quote: "即有袋家每人肩兩石布袋。遇有支遣，倉前成市"；"自州東虹橋元豐倉、順成倉"
  used_in: []
  prompt_string: "汴河脚夫（袋家）：粗麻短衫敞怀、裤脚扎起、麻鞋，肩上扛一只鼓胀的粗布粮袋，从纲船跳板走到仓前；不是清代长辫、不穿明代立领"
  negative: "长辫、立领、马褂、塑料编织袋、麻袋印字"
  note: 2026-09-14 SYNC_sk1（回应 R6 I02）：quote 只截到虹桥外的元丰仓、顺成仓；卷一「外诸司」原文同段还列有东水门里的广济等仓，shot12 口播「城里汴河边的仓前码头」对应的是城里那几仓。补 quote 要照维基文库卷一原文逐字补齐；本次抓原文网络不通（WebFetch 超时），没有凭记忆补字，id 不变。

- fact_id: kaifeng.job.002
  claim: 太平车：上有箱无盖，驾车人在中间双手执鞭，前面骡驴二十余头分两行或牛五七头拉，中间挂铁铃行则有声，可载数十石
  tag: ✅
  source: 《东京梦华录》卷三「般載雜賣」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "前列騾或驢二十餘，前後作兩行；或牛五七頭拽之"；"中間懸一鐵鈴，行即有聲，使遠來者車相避"
  used_in: []
  prompt_string: "太平车：两轮大板车、木箱无盖、车壁前伸两根长木，赶车人站在中间挥鞭，前面两列骡驴二十余头拉车，车身悬一只铁铃叮当响"
  negative: "四轮马车、橡胶轮胎、马车篷"

- fact_id: kaifeng.job.003
  claim: 独轮「串车」前后两人把驾、两旁两人扶拐、前面驴拉，运竹木瓦石；卖糕的小独轮车只一两人推
  tag: ✅
  source: 《东京梦华录》卷三「般載雜賣」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "又有獨輪車，前後二人把駕，兩旁兩人扶拐，前有驢拽，謂之『串車』"
  used_in: []
  prompt_string: "独轮串车：一只大木轮居中，前后各一人把着车把，两旁两人扶着，前面一头驴拉"
  negative: "自行车、手推铁车"

- fact_id: kaifeng.job.004
  claim: 驼骡驴驮子用皮或竹做成方扁筐搭在背上，粮食用布袋驮
  tag: ✅
  source: 《东京梦华录》卷三「般載雜賣」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "又有駝騾驢馱子，或皮或竹為之，如方匾竹差，兩搭背上，斛禮則用布袋駝之"
  used_in: []
  prompt_string: "骆驼和骡子背上两侧搭着方扁的竹筐或皮囊，驮粮的用布袋"
  negative: "—"

- fact_id: kaifeng.job.005
  claim: 雇人力、干当人、酒食、匠人各有「行老」供雇；找女使有牙人引路
  tag: ✅
  source: 《东京梦华录》卷三「雇覓人力」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "凡雇覓人力，幹當人、酒食、作匠之類，各有行老供雇。覓女使即有引至牙人"
  used_in: []
  prompt_string: "（采访用）雇脚夫要找这一行的行老，不是随便在街上拉人"
  negative: "—"

- fact_id: kaifeng.job.006
  claim: 酒店里卖下酒的厨子叫「茶饭量酒博士」，店里小伙计通称「大伯」
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "凡店內賣下酒廚子，謂之『茶飯量酒博士』。至店中小兒子，皆通謂之『大伯』"
  used_in: []
  prompt_string: "（称谓白名单）酒店掌勺的叫「博士」，跑腿小伙计叫「大伯」"
  negative: "「小二」（后世话本用语，⚠️）、「服务员」"

- fact_id: kaifeng.job.007
  claim: 街坊妇人腰系青花布手巾、绾高髻，在酒店为客人换汤斟酒，俗称「焌糟」——酒楼里的女性服务者
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "更有街坊婦人，腰系青花布手巾，綰危髻，為酒客換湯斟酒，俗謂之『焌糟』"
  used_in: []
  prompt_string: "焌糟（酒楼妇人）：头发绾成高高的髻、腰间系青花布手巾、交领窄袖短衫配长裙，提着汤瓶给酒客斟酒；不是明代立领、不是清代旗装"
  negative: "立领、旗袍、长辫、旗头、现代围裙"

- fact_id: kaifeng.job.008
  claim: 「闲汉」：百姓进酒肆，见年轻子弟饮酒就凑上前伺候、代买东西叫妓、跑腿取送钱物
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "見子弟少年輩飲酒，近前小心供過，使令買物命妓，取送錢物之類，謂之『閑漢』"
  used_in: []
  prompt_string: "闲汉：一个凑到酒桌边点头哈腰、等着替人跑腿的中年男子，青色软巾裹头、粗布短衫"
  negative: "—"

- fact_id: kaifeng.job.009
  claim: 「厮波」上前换汤斟酒唱歌、献果子香药，客散得钱；「撒暂」不问买不买先把果子萝卜散给客人再收钱
  tag: ✅
  source: 《东京梦华录》卷二「飲食果子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  quote: "又有向前換湯斟酒歌唱，或獻果子香藥之類，客散得錢，謂之『廝波』"；"散與坐客，然後得錢，謂之『撒暫』"
  used_in: []
  prompt_string: "酒桌边不请自来的厮波，一边斟酒一边唱曲；撒暂先把一把果子放到每人面前再讨钱"
  negative: "—"

- fact_id: kaifeng.job.010
  claim: 食店点菜流程：跑堂「行菜」记下后到局前唱念报单，掌灶的叫「铛头」；错了一样客人告主人，跑堂挨骂、罚工钱甚至被赶走
  tag: ✅
  source: 《东京梦华录》卷四「食店」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "行菜得之，近局次立，從頭唱念，報與局內。當局者謂之『鐺頭』"；"或罰工價，甚者逐之"
  used_in: []
  prompt_string: "跑堂站在灶局前扯着嗓子唱报菜名，灶上的铛头应声下锅"
  negative: "点菜单、收银机"

- fact_id: kaifeng.job.011
  claim: 军巡铺兵每铺五人、夜间巡警收领公事（官吏形象；白天拦人属推测）
  tag: ✅
  source: 《东京梦华录》卷三「防火」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "每坊巷三百步許，有軍巡鋪屋一所，鋪兵五人，夜間巡警收領公事"
  used_in: []
  prompt_string: "军巡铺兵：五个穿短后衣、裹头巾、束带、执棍杖的兵卒站在铺屋前；不是明清衙役皂隶打扮"
  negative: "「大人」称呼、清代补服、明代锦衣卫飞鱼服、警帽"

- fact_id: kaifeng.job.012
  claim: 每日五更，寺院行者打铁牌或木鱼挨门报晓，各有地段
  tag: ✅
  source: 《东京梦华录》卷三「天曉諸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "每日交五更，諸寺院行者打鐵牌子或木魚循門報曉，亦各分地分，日間求化"
  used_in: []
  prompt_string: "天没亮，一个僧人打扮的行者敲着铁牌沿街挨家报晓"
  negative: "闹钟、钟楼报时（现代）"

- fact_id: kaifeng.job.013
  claim: 士农工商诸行百户衣装各有本色不敢越外：香铺裹香人顶帽披背；质库掌事穿皂衫角带不顶帽——街上一看就知是哪行
  tag: ✅
  source: 《东京梦华录》卷五「民俗」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "其士農工商諸行百戶衣裝，各有本色，不敢越外。謂如香鋪裹香人，即頂帽披背；質庫掌事，即著皂衫角帶不頂帽"
  used_in: []
  prompt_string: "（交 §3 衣）当铺掌事：黑色皂衫、角带、不戴帽；香铺伙计：戴帽、披背子——各行各业穿着一眼可辨"
  negative: "全城穿一样的「古装」"

- fact_id: kaifeng.job.014
  claim: 卖药卖卦的都穿戴冠带；连乞丐也有规格，稍有懈怠众人不容
  tag: ✅
  source: 《东京梦华录》卷五「民俗」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "其賣藥賣卦，皆具冠帶。至於乞丐者，亦有規格。稍似懈怠，眾所不容"
  used_in: []
  prompt_string: "街边卖卦的先生戴冠束带，摊前一块布幡"
  negative: "—"

- fact_id: kaifeng.job.015
  claim: 「提茶瓶之人」每日在邻里间互相送茶、传话问候
  tag: ✅
  source: 《东京梦华录》卷五「民俗」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "更有提茶瓶之人，每日鄰里互相支茶，相問動靜"
  used_in: []
  prompt_string: "提着长嘴茶瓶挨家串门的送茶人"
  negative: "—"

- fact_id: kaifeng.job.016
  claim: 外地人若被都人欺负，众人必出手救护；新搬来的邻居会借家什、送汤茶、指引买卖——记者（外方人）会受到的接待
  tag: ✅
  source: 《东京梦华录》卷五「民俗」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "若見外方人為都人淩欺，眾必救護之"；"獻遣湯茶，指引買賣之類"
  used_in: []
  prompt_string: "（剧情依据）汴京人对外地来客热情、会主动指路"
  negative: "—"

- fact_id: kaifeng.job.017
  claim: 供人家打水者各有地段坊巷；还有使漆、打钗环、荷大斧斫柴、换扇子柄、供香饼子炭团的，夏月有洗毡淘井的
  tag: ✅
  source: 《东京梦华录》卷三「諸色雜賣」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "其供人家打水者，各有地分坊巷，及有使漆、打釵環、荷大斧斫柴、換扇子柄、供香餅子、炭團"
  used_in: []
  prompt_string: "挑水夫挑着两只木桶、扛大斧的劈柴人、走街串巷的修扇柄匠人"
  negative: "塑料桶、自来水"

- fact_id: kaifeng.job.018
  claim: 出街办事嫌路远，坊巷桥市随处可租鞍马，不过一百钱
  tag: ✅
  source: 《东京梦华录》卷四「雜賃」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "逐坊巷橋市，自有假賃鞍馬者，不過百錢"
  used_in: []
  prompt_string: "（交 §6 行 / §7 物价）桥头租马的摊子，一趟不过一百文"
  negative: "—"

- fact_id: kaifeng.job.019
  claim: 早晨桥市街巷口木竹匠人、杂作人夫、僧道罗列等人雇请，叫「罗斋」
  tag: ✅
  source: 《东京梦华录》卷四「修整雜貨及齋僧請道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  quote: "即早辰橋市街巷口皆有木竹匠人，謂之雜貨工匠，以至雜作人夫，道士僧人，羅立會聚，候人請喚，謂之『羅齋』"
  used_in: []
  prompt_string: "清晨桥头，一排扛着锯斧的木匠泥匠和短工蹲坐等活"
  negative: "—"

- fact_id: kaifeng.job.020
  claim: 妓女从前多骑驴，宣和、政和年间只骑马，披凉衫，把盖头反系在冠子上；少年狎客跨马轻衫小帽跟在后面
  tag: ✅
  source: 《东京梦华录》卷七「駕回儀衛」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "妓女舊日多乘驢，宣、政間惟乘馬，披涼衫，將蓋頭背繫冠子上。少年狎客，往往隨後，亦跨馬輕衫小帽"
  used_in: []
  prompt_string: "（1120 年正是宣和）春游路上骑马的歌妓，披薄纱凉衫、盖头翻系在冠子后面；后面跟着骑马的轻衫小帽少年"
  negative: "轿中不露面、缠足小脚特写、清代旗装"

- fact_id: kaifeng.job.021
  claim: 卖麦面每秤装一布袋叫「一宛」，用太平车或驴马驮着从城外守门入城，到天明不绝
  tag: ✅
  source: 《东京梦华录》卷三「天曉諸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "其賣麥麪，每秤作一布袋，謂之『一宛』；或三五秤作一宛，用太平車或驢馬馱之，從城外守門入城貨賣"
  used_in: []
  prompt_string: "天亮前的城门口，驮着面袋的驴队和太平车排队进城"
  negative: "—"

- fact_id: kaifeng.job.022
  claim: 杀猪羊作坊每人担猪羊或用车子上市，动辄上百
  tag: ✅
  source: 《东京梦华录》卷三「天曉諸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "其殺豬羊作坊，每人擔豬羊及車子上市，動即百數"
  used_in: []
  prompt_string: "清晨屠户挑着整片猪羊肉上市"
  negative: "—"

- fact_id: kaifeng.job.023
  claim: 御街从州桥到南内前，趁早朝卖药卖饮食的叫卖声百般
  tag: ✅
  source: 《东京梦华录》卷三「天曉諸人入市」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  quote: "更有御街州橋至南內前趁朝賣藥及飲食者，吟叫百端"
  used_in: []
  prompt_string: "（声音锚）清晨御街上此起彼伏、带调子的叫卖声"
  negative: "扩音喇叭"
```

---

## §9 · 节令与习俗（卷七「清明節」全段 + 「三月一日開金明池瓊林苑」+ 卷二迎祥池）

卷七「清明節」全段已逐字抓到（见 raw_fetch/juan7.txt 首节）。要点：冬至后一百五日为「大寒食」，前一日叫「炊熟」，寒食第三节才是清明日（2026-09-14 更正，见 festival.001）；新坟必于此日（清明日）拜扫，都城人出郊；纸马铺当街用纸叠成楼阁；四野如市，芳树下罗列杯盘；轿顶用杨柳杂花装簇；自此三日皆出城上坟，但一百五日最盛。**注意：「冥器」二字不在「清明节」一节里**（可能在他卷，本次未抓），本节只有「纸马铺」。

```yaml
- fact_id: kaifeng.festival.001
  claim: 京师以冬至后第一百零五天为「大寒食」，它的前一天叫「炊熟」；寒食的第三天（「寒食第三节」）就是清明日。清明不等于冬至后一百五日，而是寒食节期的第三天
  tag: ✅
  source: 《东京梦华录》卷七「清明節」（维基文库原文 ＋ 识典古籍点校本）
  source_url:
    - https://zh.wikisource.org/wiki/東京夢華錄/卷七
    - https://www.shidianguji.com/zh/book/HY0001/chapter/HY0001_60
  tier: T0
  verified_by: ai_read
  quote: "清明節，尋常京師以冬至後一百五日爲大寒食，前一日謂之炊熟"（识典古籍点校本）；"清明節，尋常京師以冬至後一百五日為大。寒食前一日謂之『炊熟』"（维基文库，此处句读有误）；"寒食第三節，即清明日矣"
  used_in: []
  prompt_string: "（旁白用）冬至后第一百零五天是大寒食，寒食的第三天才是清明"
  negative: "—"
  note: 2026-09-14 W12_factfix 更正（回应 R6 W20）。原 claim「以冬至后一百五日为清明」是照着维基文库「為大。寒食前一日」这个断句错误读下来的，「為大」不成句。识典古籍点校本读作「為大寒食，前一日謂之炊熟」，同段后文「寒食第三節，即清明日矣」「但一百五日最盛」也只有按这个读法才前后一致。判断：采用点校本读法。原文没有直接写清明是冬至后第几天：如果以一百五日（大寒食）为寒食第一天，清明是第 107 天；如果从炊熟算起，是第 106 天。口播不报清明是冬至后第几天。人最多的一天见 festival.009（原文是「一百五日」＝大寒食，不是清明日）。

- fact_id: kaifeng.festival.002
  claim: 炊熟日用面做枣糕飞燕，柳条串起插在门楣上，叫「子推燕」
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "用麵造棗旟飛燕，柳條串之，插於門楣，謂之『子推燕』"
  used_in: []
  prompt_string: "家家门楣上插着柳条，柳条上串着面捏的枣糕小燕子"
  negative: "红灯笼、春联（非清明）"

- fact_id: kaifeng.festival.003
  claim: 及笄的女孩多在这一天「上头」（成年梳髻）
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "子女及笄者，多以是日上頭"
  used_in: []
  prompt_string: "院子里母亲给十五岁的女儿第一次梳起发髻、插上簪"
  negative: "—"

- fact_id: kaifeng.festival.004
  claim: 凡新坟都在清明日拜扫，都城人出郊；宫中提前半月发宫人车马朝陵
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "凡新墳皆用此日拜掃。都城人出郊。禁中前半月發宮人車馬朝陵"
  used_in: []
  prompt_string: "清明日城门口涌出上坟的人流，挑担的、抬轿的、赶车的"
  negative: "—"

- fact_id: kaifeng.festival.005
  claim: 朝陵随从人员穿紫衫、白绢三角子、青行缠，都是官给
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "從人皆紫衫白絹三角子青行纏，皆系官給"
  used_in: []
  prompt_string: "（交 §3 衣）朝陵仪仗随从：紫色衫、头戴白绢三角巾、小腿缠青色行缠"
  negative: "—"

- fact_id: kaifeng.festival.006
  claim: 士庶挤满各城门；纸马铺当街用纸叠成楼阁形状
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "士庶闐塞諸門，紙馬鋪皆於當街用紙袞疊成樓閣之狀"
  used_in: []
  prompt_string: "纸马铺门口当街摆着用纸扎叠成的楼阁（祭品），高过人头"
  negative: "纸扎汽车手机、印刷冥币"

- fact_id: kaifeng.festival.007
  claim: 四野如市，人们在芳树下或园囿间罗列杯盘互相劝酒；歌儿舞女遍满园亭，到傍晚才回
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "四野如市，往往就芳樹之下，或園囿之間，羅列杯盤，互相勸酬。都城之歌兒舞女，遍滿園亭，抵暮而歸"
  used_in: []
  prompt_string: "郊外开花的树下，一家家铺开食盒杯盘席地饮酒；远处园亭里有歌女弹唱"
  negative: "野餐垫、烧烤架、帐篷"

- fact_id: kaifeng.festival.008
  claim: 轿子顶上用杨柳和杂花装簇，四面垂下遮映
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "轎子即以楊柳雜花裝族頂上，四垂遮映"
  used_in: []
  prompt_string: "踏青归来的轿子，轿顶插满杨柳枝和杂色鲜花，柳条花枝四面垂下来"
  negative: "红盖头花轿（婚礼式）、彩灯"

- fact_id: kaifeng.festival.009
  claim: 从这时起一连三天，人们都出城上坟，但「一百五日」（冬至后第一百零五天，即大寒食那天）人最多。原文说的最盛之日是大寒食，不是清明日
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url:
    - https://zh.wikisource.org/wiki/東京夢華錄/卷七
    - https://www.shidianguji.com/zh/book/HY0001/chapter/HY0001_60
  tier: T0
  verified_by: ai_read
  quote: "自此三日，皆出城上墳，但一百五日最盛"（维基文库）；"自此三日皆出城上墳，但一百五日最盛"（识典古籍点校本）
  used_in: []
  prompt_string: "（旁白用）一连三天都有人出城上坟，书上说「一百五日」那天人最多"
  negative: "—"
  note: 2026-09-14 W12_factfix 更正（回应 R6 W01 / W20）。删掉了原 claim 和 prompt_string 里的「（清明当日）」「清明当天人最多」：按 festival.001，「一百五日」是大寒食，清明是寒食第三天，两者不是同一天。「自此三日」的「此」指哪一天原文没说清（可能从寒食算，也可能从清明算）⚠️。口播可以说「连着三天出城上坟，书上说一百五日（大寒食那天）人最多」，不能说「清明这一天人最多」。原文拜扫新坟用的「此日」是清明日（「寒食第三節，即清明日矣。凡新墳皆用此日拜掃」），见 festival.004。

- fact_id: kaifeng.festival.010
  claim: 傍晚回城「缓入都门，斜阳御柳；醉归院落，明月梨花」
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "緩入都門，斜陽御柳；醉歸院落，明月梨花"
  used_in: []
  prompt_string: "斜阳下城门内外一排御柳，踏青人陆续回城；夜里院落梨花映月"
  negative: "—"

- fact_id: kaifeng.festival.011
  claim: 诸军禁卫各成队伍骑马奏乐出城，叫「摔脚」，旗帜鲜明军容雄壮
  tag: ✅
  source: 《东京梦华录》卷七「清明節」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "諸軍禁衛，各成隊伍，跨馬作樂四出，謂之『摔腳』。其旗旄鮮明，軍容雄壯"
  used_in: []
  prompt_string: "一队禁军骑兵打着鲜明旗帜、奏着鼓乐从城门出来"
  negative: "—"

- fact_id: kaifeng.festival.012
  claim: 金明池开池期间桥上用瓦盆掷头钱「关扑」赌钱物衣服；池边彩棚可租来看争标；街东皆酒食店、艺人勾肆、质库
  tag: ✅
  source: 《东京梦华录》卷七「三月一日開金明池瓊林苑」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "橋上兩邊用瓦盆，內擲頭錢，關撲錢物、衣服、動使。遊人還往，荷蓋相望"
  used_in: []
  prompt_string: "仙桥上摆着瓦盆，游人往盆里掷铜钱赌东西；桥上人来人往、遮阳的伞盖一个接一个"
  negative: "扑克、骰子桌（现代）"

- fact_id: kaifeng.festival.013
  claim: 金明池龙舟争标：小龙船二十只、虎头船十只、飞鱼船二只、鳅鱼船二只；鳅鱼船是进花石的朱勔所进
  tag: ✅
  source: 《东京梦华录》卷七「駕幸臨水殿觀爭標錫宴」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "有小龍船二十隻，上有緋衣軍士各五十餘人"；"又有鰍魚船二隻，止容一人撐劃，乃獨木為之也。皆進花石朱緬所進"
  used_in: []
  prompt_string: "池面上二十只小龙船列阵，船上军士一色绯红衣，旗鼓铜锣；两只独木鳅鱼船只容一人撑划"
  negative: "现代龙舟赛道浮标、救生衣"

- fact_id: kaifeng.festival.014
  claim: 池上还有「水傀儡」（木偶钓活鱼）、「水秋千」（从秋千上翻筋斗入水）
  tag: ✅
  source: 《东京梦华录》卷七「駕幸臨水殿觀爭標錫宴」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "釣出活小魚一枚，又作樂，小船入棚"；"又一人上蹴秋千，將平架，筋鬥擲身入水，謂之『水秋千』"
  used_in: []
  prompt_string: "画船上架着秋千，一个艺人荡到最高处翻筋斗跳进池里"
  negative: "跳水台"

- fact_id: kaifeng.festival.015
  claim: 季春三月牡丹芍药棣棠木香上市，卖花人用马头竹篮铺排，歌叫之声清奇可听
  tag: ✅
  source: 《东京梦华录》卷七「駕回儀衛」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "是月季春，萬花爛熳，牡丹芍藥，棣棠木香，種種上市，賣花者以馬頭竹藍鋪排，歌叫之聲，清奇可聽"
  used_in: []
  prompt_string: "卖花人挑着马头形竹篮，篮里牡丹芍药棣棠，一路唱着卖"
  negative: "塑料花桶、玫瑰花束（现代花店式）"

- fact_id: kaifeng.festival.016
  claim: 宣和二年清明日的公历/农历具体日期——按「冬至后一百五日」推算约在儒略历 1120 年 3 月末（格里历 4 月上旬），农历约二月末或三月初；是否已过「三月一日开金明池」须查朔闰表
  tag: ⚠️
  source: 推算（陈垣《二十史朔闰表》待查）
  source_url: —
  tier: T3
  verified_by: ai_draft
  quote: "—"
  used_in: []
  prompt_string: "（不得进 prompt）"
  negative: "—"
  note: 2026-09-14 W12_factfix：本条推算的基点错了。「冬至后一百五日」是大寒食，清明是寒食第三天（festival.001），重算要按冬至后第 106 或 107 天。仍为 ai_draft，不得进 prompt。
```

---

## §11 · 当日大事时间线（宣和二年 1120）

**《东京梦华录》里的「宣和间」现状（T0）**：御沟「宣和間盡植蓮荷」（route.010）；东角楼「宣和間展夾城牙道」；白矾楼改丰乐楼「宣和間，更修三層相高。五樓相向」；妓女「宣、政間惟乘馬」（job.020）；金明池「宣、政間亦有假賃大小船子，許士庶遊賞」。这些都可作 1120 年的街景细节，但《梦华录》只说「宣和间」，不能精确到宣和二年以前/以后（⚠️）。

**正史年表（中文维基百科，T3 索引；月份能核到的写月份）**：清明（约公历 4 月初）时，艮岳在建、花石纲在运、方腊**尚未**起义（十月初九才起事）。

```yaml
- fact_id: kaifeng.event.001
  claim: 艮岳于政和七年（1117）十二月开工、宣和四年（1122）落成，位于汴梁里城东北部——1120 年清明时正在营建
  tag: ⚠️
  source: 中文维基百科「艮岳」（需回查《宋史·地理志》/ 徽宗《艮岳记》升 ✅）
  source_url: https://zh.wikipedia.org/wiki/艮岳
  tier: T3
  verified_by: ai_read
  quote: "政和七年（1117年）十二月开工"；"宣和四年（1122年）落成"；"位于京城汴梁（今河南省开封市）里城东北部"
  used_in: []
  prompt_string: "（新闻由头候选 ①）城东北角工地：夯土成山，太湖石一块块从汴河船上卸下运往工地"
  negative: "—"

- fact_id: kaifeng.event.002
  claim: 朱勔自崇宁四年（1105）十一月主持苏州应奉局搜求奇花异石，号称花石纲；靖康元年（1126）正月削官、九月赐死
  tag: ⚠️
  source: 中文维基百科「朱勔」（回查《宋史·朱勔传》升 ✅）
  source_url: https://zh.wikipedia.org/wiki/朱勔
  tier: T3
  verified_by: ai_read
  quote: "崇寧四年（1105年）十一月，朱勔奉迎徽宗，主持蘇州應奉局，專門搜求奇花異石...號稱花石綱"
  used_in: []
  prompt_string: "（旁白用）花石纲已经运了十五年"
  negative: "—"

- fact_id: kaifeng.event.003
  claim: 《东京梦华录》T0 佐证朱勔与花石：金明池的鳅鱼船「皆進花石朱緬所進」——说明宣和年间朱勔的进献已进入汴京日常
  tag: ✅
  source: 《东京梦华录》卷七「駕幸臨水殿觀爭標錫宴」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "皆進花石朱緬所進"
  used_in: []
  prompt_string: "（采访远景用）金明池上朱勔进献的独木鳅鱼船"
  negative: "—"

- fact_id: kaifeng.event.004
  claim: 方腊于宣和二年十月初九（1120 年 11 月 1 日）在歙县七贤村起事，自称年号「永乐」——清明时尚未爆发，相隔约七个月
  tag: ⚠️
  source: 中文维基百科「方腊起义」「宣和 (宋徽宗)」（回查《宋史·童贯传》《续资治通鉴长编拾补》升 ✅）
  source_url: https://zh.wikipedia.org/wiki/方腊起义
  tier: T3
  verified_by: ai_read
  quote: "宣和二年十月初九（1120年11月1日）方臘率眾在歙縣七賢村起事"；"永樂（1120年－1121年）：北宋時期—方臘之年號"
  used_in: []
  prompt_string: "（不入画，只作时间线旁白：半年后东南会因花石纲起大乱）"
  negative: "—"

- fact_id: kaifeng.event.005
  claim: 方腊起事后徽宗下令停运花石纲、任童贯为江浙宣抚使（1120 年末）；宣和三年四月方腊被擒，宣和四年三月全部平定
  tag: ⚠️
  source: 中文维基百科「方腊起义」「1120年」
  source_url: https://zh.wikipedia.org/wiki/1120年
  tier: T3
  verified_by: ai_read
  quote: "宣和二年，宋徽宗下令停運花石綱，又以童贯为江浙宣抚使"；"宣和四年三月全部平亂"
  used_in: []
  prompt_string: "（不入画）"
  negative: "—"

- fact_id: kaifeng.event.006
  claim: 1120 年宋金议定「海上之盟」：金取辽中京、宋取燕京，宋把原给辽的岁币转给金；同年金攻陷辽上京临潢府（月份未核）
  tag: ⚠️
  source: 中文维基百科「海上之盟」「1120年」（月份与赵良嗣出使时间待核《三朝北盟会编》）
  source_url: https://zh.wikipedia.org/wiki/海上之盟
  tier: T3
  verified_by: ai_read
  quote: "宣和二年（1120年），雙方商定...宋答應滅遼後，將原來於澶淵之盟輸給遼的歲幣轉輸給金"；"金國攻陷遼國上京臨潢府"
  used_in: []
  prompt_string: "（新闻由头候选 ④，旁白用）朝廷正派人渡海去跟金人商量联手灭辽"
  negative: "—"

- fact_id: kaifeng.event.007
  claim: 花石纲船队经运河、汴河入京，「舳舻相衔于淮汴之间」——本次未在抓到的页面里核到运输路线原句
  tag: ⚠️
  source: 记忆中《宋史·朱勔传》；维基百科「花石纲」条只说「有的地方甚至为了让船队通过，拆毁桥梁，凿坏城郭」
  source_url: https://zh.wikipedia.org/wiki/花石纲
  tier: T3
  verified_by: ai_draft
  quote: "有的地方甚至为了让船队通过，拆毁桥梁，凿坏城郭"（此句为 ai_read）
  used_in: []
  prompt_string: "（待核后方可用）载着太湖石的纲船从虹桥下穿过"
  negative: "—"
```

### 「新闻由头」候选（给阶段 1 concept 挑）

| # | 由头 | 依据 | 可信度 |
|---|---|---|---|
| ① | **艮岳在建、花石纲的船正经汴河进城**（虹桥下一艘载太湖石的纲船） | event.001 / event.002 / event.003（T0 佐证朱勔进献）/ event.007（汴河路线 ai_draft 待核） | ⚠️ 艮岳 T3 可升 ✅；汴河路线待核 |
| ② | **清明日迎祥池一年一开** + 金明池三月一日开池争标（清明是否在窗口 ⚠️） | route.014（T0 ✅）/ route.015（T0 ✅）/ festival.016 | ✅ / ⚠️ |
| ③ | **御街御沟新栽的荷花与岸边桃李梨杏**（「宣和间」的新工程） | route.010（T0 ✅） | ✅（只到「宣和间」） |
| ④ | 朝廷使者渡海联金灭辽（海上之盟） | event.006 | ⚠️ 月份待核 |
| ⑤ | 反向伏笔：半年后方腊因花石纲起事 | event.004 | ⚠️（只作片尾字幕） |

---

## §12 · 可采访的人物

**真实人物（只引原话 / 远景）**：

```yaml
- fact_id: kaifeng.person.001
  claim: 孟元老——崇宁二年（1103）随父到东京，靖康之难次年南渡，绍兴十七年（1147）撰成《东京梦华录》，自序署「幽兰居士孟元老」；真实姓名学界有孟钺 / 孟揆 / 赵子淔诸说，生平事迹不详
  tag: ⚠️
  source: 中文维基百科「孟元老」（自序原文本次未抓，待补 T0）
  source_url: https://zh.wikipedia.org/wiki/孟元老
  tier: T3
  verified_by: ai_read
  quote: "崇宁二年（1103年）随父到东京。靖康之难次年南下，孟元老避地江左。绍兴十七年（1147年）撰成《东京梦华录》"
  used_in: []
  prompt_string: "（远景）1120 年他在汴京已住了十七年——一个三十来岁、在街市里到处走的士人，交领长衫、幞头"
  negative: "—"

- fact_id: kaifeng.person.002
  claim: 张择端——生卒 1085–1145，密州诸城（东武）人，翰林院待诏；金大定丙午（1186）张著跋：「翰林張擇端，字正道，東武人也。幼讀書，遊學於京師，後習繪事。本工其界畫，尤嗜舟車、市橋郭徑」
  tag: ⚠️
  source: 中文维基百科「张择端」「清明上河圖」（跋文原件在故宫本卷尾，对照名画记高清图后可升 ✅ T0）
  source_url: https://zh.wikipedia.org/wiki/清明上河圖
  tier: T3
  verified_by: ai_read
  quote: "翰林張擇端，字正道，東武人也。幼讀書，遊學於京師，後習繪事。本工其界畫，尤嗜舟車、市橋郭徑，別成家數也"；"大定丙午清明後一日，燕山張著跋"
  used_in: []
  prompt_string: "（远景）虹桥桥头一个三十五岁上下的画院待诏，青衫幞头，拿着炭笔在纸上速写船和桥——只引跋文，不编他的话"
  negative: "—"

- fact_id: kaifeng.person.003
  claim: 朱勔——苏州人，1075–1126，主持苏州应奉局 / 花石纲；《东京梦华录》卷七记金明池鳅鱼船为「進花石朱緬所進」（T0）；宣和五年得「神运昭功石」封盘固侯（1120 时尚未）；靖康元年赐死
  tag: ⚠️
  source: 中文维基百科「朱勔」+《东京梦华录》卷七（T0 佐证见 event.003）
  source_url: https://zh.wikipedia.org/wiki/朱勔
  tier: T3
  verified_by: ai_read
  quote: "朱勔（1075年—1126年）...蘇州（今属江苏）人"；"宣和五年（1123年）取得一巨型太湖石，高達四丈...徽宗賜名曰『神運昭功石』"
  used_in: []
  prompt_string: "（远景 / 不采访）纲船上押运花石的官员，只以「进花石的朱家」被脚夫提起"
  negative: "—"

- fact_id: kaifeng.person.004
  claim: 李师师——《东京梦华录》卷五列为京瓦「小唱」头牌：「小唱：李師師、徐婆惜、封宜奴、孫三四等，誠其角者」（T0；与徽宗的传闻不进正片）
  tag: ✅
  source: 《东京梦华录》卷五「京瓦伎藝」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "小唱：李師師、徐婆惜、封宜奴、孫三四等，誠其角者"
  used_in: []
  prompt_string: "（远景）瓦子勾栏里的小唱名角登台，台下坐满人——不给正脸、不编台词"
  negative: "与徽宗私会的桥段（野史，合规 ❌）"

- fact_id: kaifeng.person.005
  claim: 露台弟子萧住儿、丁都赛、薛子大、薛子小、杨总惜、崔上寿——宝津楼百戏中演杂剧的真实艺人
  tag: ✅
  source: 《东京梦华录》卷七「駕登寶津樓諸軍呈百戲」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  quote: "是時弟子蕭住兒、丁都賽、薛子大、薛子小、楊總惜、崔上壽之輩，後來者不足數"
  used_in: []
  prompt_string: "（远景）金明池边露台上演杂剧的女艺人丁都赛一班"
  negative: "—"

- fact_id: kaifeng.person.006
  claim: 崇宁、大观以来京师瓦肆伎艺由张廷叟、孟子书主持
  tag: ✅
  source: 《东京梦华录》卷五「京瓦伎藝」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷五
  tier: T0
  verified_by: ai_read
  quote: "崇、觀以來，在京瓦肆伎藝，張廷叟、孟子書主張"
  used_in: []
  prompt_string: "（旁白用）瓦子里的班主"
  negative: "—"
```

**典型虚构人物（阶层 / 职业有据；「他会怎么答」是把 T0 原句翻成白话，供阶段 4 台词参考，不是史料）**：

| # | 人物 | 依据 fact | 他会怎么回答记者（白话，据原文改写） | 备注 |
|---|---|---|---|---|
| 1 | **汴河脚夫（袋家）**，长访对象 | job.001（「袋家每人肩兩石布袋」「倉前成市」）/ job.005（行老）/ route.003（汴河运东南之粮） | 「一袋两石，扛上肩走到仓门口算一趟。仓里一开支，仓前头就跟赶集一样。想雇我们？得找行老，街上拉人没人跟你走。」 | 一天工钱 → 交 W-物价（程民生）；两石折合多少公斤 ai_draft 待核 |
| 2 | **卖汤茶药的女摊主**（概念卡「卖饮子的女摊主」） | job.007（焌糟：婦人、青花布手巾、綰危髻）/ food.013（「煎點湯茶藥者，直至天明」）/ food.004（夏月饮子，清明未必有）/ job.016（外方人受救护） | 「天没亮就把炉子生上，洗脸水、汤药、点茶都有。你是外路来的吧？口音不对。在这儿没人欺负外路人，谁欺负你，街坊都得出来说话。」 | 「饮子」一词本次只在夏月条见到；清明时段用「汤茶药」更稳（⚠️ 记者口播「史书写的是夏天卖凉水」） |
| 3 | **虹桥桥头脚店的酒博士 / 大伯** | food.006（正店七十二户，余皆脚店）/ job.006（茶饭量酒博士、大伯）/ food.026（脚店从正店打酒借银器）/ food.025（两人对坐必一副注碗两副盘盏）/ food.009（每分不过十五钱） | 「我们是脚店，酒是从正店打来的，这套银注碗也是人家借的——打过两三回酒人家就敢借。两位坐下，注碗一副、盘盏两副、果菜五碟，这是规矩。下酒菜一份十五文以内。」 | 「桥丁」一职 T0 无载（⚠️），建议改用酒博士 / 大伯 |
| 4 | **军巡铺兵**（在场者 / 官吏） | job.011（铺兵五人，夜间巡警）/ route.009（御道不得人马行往） | 「街心朱杈子里头是御道，人马都不许走，你往回站。我们铺里五个人，三百步一铺，夜里巡街。」 | 白天拦人属推测（⚠️，台词须带「史书只写了夜巡」） |
| 5 | **太平车赶车人**（备用） | job.002（骡驴二十余、铁铃）/ job.021（卖麦面一宛从城外守门入城） | 「二十多头骡子拉一车，能装几十石。车上挂个铁铃，老远听见就让道。天不亮就从城门口排队进城。」 | — |

---

## 未能核实 / 待核（ai_draft，不得进 prompt）

1. **宣和二年清明的确切日期**（公历 / 农历；是否在「三月一日开金明池」之后）——festival.016，查陈垣《二十史朔闰表》。
2. **花石纲经汴河入京的原句**（记忆为《宋史·朱勔传》「舳艫相銜於淮汴之間」）——event.007。
3. **赵良嗣 1120 年出使金国的月份**；**金陷辽上京的月份**（记忆为五月）——event.006。
4. **「冥器」**不在卷七「清明节」一节（可能在卷八中元节），本次未抓其他卷。
5. **两石粮袋折合公斤数**（宋制一石约 5x–6x kg 为记忆值）。
6. **樊楼「宣和间更修三层」是否早于 1120**——T0 只说「宣和间」。
7. **孟元老自序原文**（「幽兰居士」「崇宁癸未到京师」等）本次未抓，person.001 用的是维基转述。
8. **「桥丁」一职**——T0 无载；州桥有防船铁索与浅船（route.008）但未言看守人员。
9. **巡铺兵白天拦人**——T0 只写「夜間巡警」。
10. **张著跋文**——转录自维基百科条目（引余辉 2015 考释），原件须对照故宫名画记高清图。
11. **ctext 备用页**（`https://ctext.org/wiki.pl?if=gb&res=712358`）本次未抓，维基文库六卷已全部抓到，无需备用。

## 来源列表

**T0（本次逐字抓取，本地副本 `raw_fetch/`）**
- 《東京夢華錄》卷一「東都外城 / 舊京城 / 河道 / 大內 / 內諸司 / 外諸司」— https://zh.wikisource.org/wiki/東京夢華錄/卷一
- 卷二「御街 / 宣德樓前省府宮宇 / 朱雀門外街巷 / 州橋夜市 / 東角樓街巷 / 潘樓東街巷 / 酒樓 / 飲食果子」— https://zh.wikisource.org/wiki/東京夢華錄/卷二
- 卷三「馬行街北諸醫鋪 … 相國寺內萬姓交易 / 般載雜賣 / 都市錢陌 / 雇覓人力 / 防火 / 天曉諸人入市 / 諸色雜賣」— https://zh.wikisource.org/wiki/東京夢華錄/卷三
- 卷四「雜賃 / 修整雜貨及齋僧請道 / 筵會假賃 / 會仙酒樓 / 食店 / 肉行 / 餅店 / 魚行」— https://zh.wikisource.org/wiki/東京夢華錄/卷四
- 卷五「民俗 / 京瓦伎藝」— https://zh.wikisource.org/wiki/東京夢華錄/卷五
- 卷七「清明節 / 三月一日開金明池瓊林苑 / 駕幸臨水殿觀爭標錫宴 / 駕登寶津樓諸軍呈百戲 / 池苑內縱人關撲遊戲 / 駕回儀衛」— https://zh.wikisource.org/wiki/東京夢華錄/卷七
- 张著跋（1186，转录）— https://zh.wikipedia.org/wiki/清明上河圖 （原件：故宫博物院藏卷尾）

**T3（中文维基百科，索引级）**
- 宣和 (宋徽宗) https://zh.wikipedia.org/wiki/宣和_(宋徽宗) ；1120年 https://zh.wikipedia.org/wiki/1120年 ；方腊起义 https://zh.wikipedia.org/wiki/方腊起义 ；花石纲 https://zh.wikipedia.org/wiki/花石纲 ；艮岳 https://zh.wikipedia.org/wiki/艮岳 ；海上之盟 https://zh.wikipedia.org/wiki/海上之盟 ；赵良嗣 https://zh.wikipedia.org/wiki/赵良嗣 ；孟元老 https://zh.wikipedia.org/wiki/孟元老 ；张择端 https://zh.wikipedia.org/wiki/张择端 ；朱勔 https://zh.wikipedia.org/wiki/朱勔 ；清明上河圖 https://zh.wikipedia.org/wiki/清明上河圖

**统计**（grep 核过）：fact 共 101 条；`verified_by: ai_read` **99** 条（T0 ✅ 91 条、T3 ⚠️ 8 条）；`ai_draft` 2 条（festival.016、event.007）。分布：route 18 / food 31 / job 23 / festival 16 / event 7 / person 6。
