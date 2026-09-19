---
worker_id: researcher-w4-economy
stage: 0
role: researcher
angle: economy
status: complete
blockers: []
confidence: high
---

# W4 · 暴风城货币 / 物价 / 商业

**版本锚点：经典旧世 Vanilla（WoW 1.x / Classic Era 1.13–1.15）。** 后续资料片（TBC 及之后）与现行正式服的数值一律视为版本错置，见 § 版本错置清单。

## 口径约定（下游必须照抄）

1. **一切换算只用两把尺子：「几顿饭」「几天收入」。全片禁止出现「1 金 ＝ X 元人民币」。**
2. 所有价格先化成**铜**再换算（1 金 ＝ 100 银 ＝ 10000 铜）。
3. **锚 A ＝ 一顿普通饭 ＝ 2 银 50 铜**（面包 1 银 25 铜 ＋ 饮料 1 银 25 铜，旅店／杂货商标价）。
   平民档一餐（粗面包 25 铜 ＋ 清泉水 25 铜）＝ **50 铜**，口播叫「一顿粗饭」。
4. **锚 B ＝ 1 银／天 ＝ 暴风城普通劳工一天的工钱**（⚠️ 推算，推法见 § 两个锚）。
5. 商品价一律取**未打折的商人标价**；声望折扣 5%–20% 另算（`stormwind.trade.011`）。
6. 数据来源优先级：Wowhead Classic 物品条目的 `jsonEquip.buyprice`（＝商人售价，单位铜）＞ 客户端 DB2（狮鹫票价）＞ 维基商人清单 ＞ 攻略站。**`sellprice` 是回收价，永远不要当售价用。**

---

## 事实注册表

### 一、货币形态（stormwind.money.*）

```yaml
- fact_id: stormwind.money.001
  claim: 暴风城（以及全艾泽拉斯）通用三级币制，进制为 100 铜 ＝ 1 银、100 银 ＝ 1 金，即 1 金 ＝ 10000 铜。
  tag: ✅
  source: Warcraft Wiki · Money
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "100 copper pieces = 1 silver piece / 100 silver pieces = 1 gold piece"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "纸币, 银票, 硬币上刻阿拉伯数字面额"

- fact_id: stormwind.money.002
  claim: 铜与银两栏各自封顶 99，满 100 自动进位；金没有上限。
  tag: ✅
  source: Warcraft Wiki · Money
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "There is no conversion rate for gold coins, so you may have more than 99 gold."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.money.003
  claim: 三种硬币在设定里各有本名——铜币叫「便士(copper penny)」、银币叫「格罗特(silver groat)」、金币叫「索维林(gold sovereign)」，是暴风王国的传统币名。
  tag: ✅
  source: Warcraft Wiki · Money（脚注引 Penny Pouch 物品 / 小说《最后的守护者》第 15 章 / 《魔兽争霸：兽人与人类》手册）
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "Stormwind's coinage has traditionally been the copper penny,[12] the silver groat,[13] and the gold sovereign.[14]"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "三种圆形打制硬币：紫铜色小便士、灰白色银格罗特、暖金色金索维林"
  negative: "方孔钱, 元宝, 纸钞, 机制币的规整齿边"

- fact_id: stormwind.money.004
  claim: 设定上早年通货全是金币，经历三次战争之后银币与铜币才进入流通——三级币制本身是战后贫困化的产物。
  tag: ✅
  source: Warcraft Wiki · Money（该句由搜索引擎自该页正文摘出，两次抓取未逐字复现，故降档记 T2）
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "In the past, all coinage was in gold. After three wars, silver and copper have come into use."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.money.005
  claim: 设定里金子必须从金矿挖出来，第二次战争以来矿场常在军队保护下开采——金币的稀缺有物质来源。
  tag: ✅
  source: Warcraft Wiki · Money
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "gold must be dug out from the rock and soil within established gold mines"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.money.006
  claim: 联盟与部落的硬币在美术上是两套（官方图库分 Alliance coins / Horde coins），但面额进制完全一样；任何城市、任何种族的商人都收同一套钱，中立城镇也照收，不存在兑换。
  tag: ✅
  source: Warcraft Wiki · Money（Gallery 分类）
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "Alliance coins / Horde coins"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "联盟版硬币：圆形打制币，边缘略不规整，币面有压印纹章"
  negative: "汇率牌, 兑换柜台, 两种货币不通用"

- fact_id: stormwind.money.007
  claim: 官方图库里有一枚「币面是苦工(peon)脸」的铜币——硬币确实带人像压印，不是素面金属片。
  tag: ✅
  source: Warcraft Wiki · Money（Gallery caption）
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "A copper coin with the face of a peon"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "铜币正面压印一张人脸侧像，压痕浅，边缘磨损发亮"
  negative: "素面无纹的金属圆片"

- fact_id: stormwind.money.008
  claim: 机制层面钱是一个不占背包格、没有重量的数字；银行 NPC 自述的业务是「金融账户 ＋ 贵重物品保险箱」，而不是存现金的金库。
  tag: ⚠️
  source: Warcraft Wiki · Stormwind Counting House（银行 NPC 台词）＋ 机制常识（无逐字条文）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Counting_House
  quote: "Welcome to the Bank of Stormwind. We offer financial accounts and safety deposit boxes for valuable items."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.money.009
  claim: 要让钱在画面上可见，必须自行补一个束口皮钱袋——设定没写死旅人如何携带硬币，也查不到任何纸币、银票、信用票据的记载。
  tag: ⚠️
  source: 本路检索结论（Warcraft Wiki Money 页无纸币/信用条目；专项检索无果）
  source_url: https://warcraft.wiki.gg/wiki/Money
  quote: "（无相关条文）"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "深棕色粗皮束口钱袋，抽绳系在腰带上，袋身被硬币硌出棱角；倒在桌上是三色硬币混作一堆"
  negative: "纸币, 银票, 支票, 钱庄凭条, 现代皮夹, 拉链"

- fact_id: stormwind.money.010
  claim: 「铜币重约 0.5 克 / 银币掺锡debase / 金币重约 8 克 / 迪菲亚把币面砸成"斗鸡眼硬币"」这类硬币物理规格出自玩家 RP 百科，不是官方设定，不得当作事实口播。
  tag: ❌
  source: Moon Guard Wiki · Currency of Stormwind（角色扮演服务器玩家自建百科）
  source_url: https://moon-guard.fandom.com/wiki/Currency_of_Stormwind
  quote: "the sovereign, a gold coin weighing around eight grams on average"
  tier: T4
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "口播硬币克重, 口播含银量, 口播铸币厂"
```

### 二、商品标价（stormwind.price.*）

```yaml
- fact_id: stormwind.price.001
  claim: 粗面包(Tough Hunk of Bread, item 4540) 商人标价 25 铜，1 级可食，回收价 1 铜——暴风城最便宜的主食。
  tag: ✅
  source: Wowhead Classic · item 4540
  source_url: https://www.wowhead.com/classic/item=4540&xml
  quote: '"buyprice":25,"reqlevel":1,"sellprice":1'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一大块粗硬的深色麦面包，表皮开裂，掰得动但要用力"
  negative: "松软白面包, 现代切片吐司"

- fact_id: stormwind.price.002
  claim: 硬肉干(Tough Jerky, item 117) 商人标价 25 铜，1 级可食——最便宜的荤食，与粗面包同价。
  tag: ✅
  source: Wowhead Classic · item 117
  source_url: https://www.wowhead.com/classic/item=117&xml
  quote: '"buyprice":25,"reqlevel":1,"sellprice":1'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一条条暗红褐色的风干肉干，边缘卷曲发硬"
  negative: "新鲜生肉, 真空包装"

- fact_id: stormwind.price.003
  claim: 清泉水(Refreshing Spring Water, item 159) 商人标价 25 铜——最便宜的饮料。
  tag: ✅
  source: Wowhead Classic · item 159
  source_url: https://www.wowhead.com/classic/item=159&xml
  quote: '"buyprice":25,"reqlevel":1,"sellprice":1'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "粗陶水壶装的清水，壶身挂着水珠"
  negative: "塑料瓶, 矿泉水标签"

- fact_id: stormwind.price.004
  claim: 新鲜出炉的面包(Freshly Baked Bread, item 4541) 商人标价 1 银 25 铜（125 铜），5 级可食——比粗面包贵整整 5 倍。
  tag: ✅
  source: Wowhead Classic · item 4541
  source_url: https://www.wowhead.com/classic/item=4541&xml
  quote: '"buyprice":125,"reqlevel":5,"sellprice":6'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "圆鼓鼓的新烤面包，表皮金褐色，掰开冒热气"
  negative: "发霉发硬的陈面包"

- fact_id: stormwind.price.005
  claim: 冰镇牛奶(Ice Cold Milk, item 1179) 商人标价 1 银 25 铜。
  tag: ✅
  source: Wowhead Classic · item 1179
  source_url: https://www.wowhead.com/classic/item=1179&xml
  quote: '"buyprice":125,"reqlevel":5,"sellprice":6'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "粗陶杯盛的白牛奶，杯壁凝着一层冷雾"
  negative: "纸盒牛奶, 玻璃奶瓶"

- fact_id: stormwind.price.006
  claim: 大块烤肉(Haunch of Meat, item 2287) 商人标价 1 银 25 铜。
  tag: ✅
  source: Wowhead Classic · item 2287
  source_url: https://www.wowhead.com/classic/item=2287&xml
  quote: '"buyprice":125,"reqlevel":5,"sellprice":6'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "带骨的大块烤肉，外层焦褐渗油"
  negative: "生肉, 现代摆盘"

- fact_id: stormwind.price.007
  claim: 达拉然浓干酪(Dalaran Sharp, item 414) 商人标价 1 银 25 铜。
  tag: ✅
  source: Wowhead Classic · item 414
  source_url: https://www.wowhead.com/classic/item=414&xml
  quote: '"buyprice":125,"reqlevel":5,"sellprice":6'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "楔形硬质干酪，切面有细孔"
  negative: "塑封奶酪片"

- fact_id: stormwind.price.008
  claim: 15 级档食物统一跳到 5 银：潮湿的玉米面包(4542) 5 银、矮人陈干酪(Dwarven Mild, 422) 5 银、西瓜汁(Melon Juice, 1205) 5 银。
  tag: ✅
  source: Wowhead Classic · item 4542 / 422 / 1205
  source_url: https://www.wowhead.com/classic/item=4542&xml
  quote: '4542 "buyprice":500,"reqlevel":15 ; 422 "buyprice":500,"reqlevel":15 ; 1205 "buyprice":500,"reqlevel":15'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.price.009
  claim: 25 级档食物跳到 10 银：暴风城布里干酪(Stormwind Brie, 1707) 10 银、甜花蜜(Sweet Nectar, 1708) 10 银——是粗面包的 40 倍。
  tag: ✅
  source: Wowhead Classic · item 1707 / 1708
  source_url: https://www.wowhead.com/classic/item=1707&xml
  quote: '1707 "buyprice":1000,"reqlevel":25,"sellprice":62 ; 1708 "buyprice":1000,"reqlevel":25,"sellprice":50'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "奶白色软质布里干酪，外皮起白霜，切开后中心微微塌流"
  negative: "工业奶酪块, 塑封包装"

- fact_id: stormwind.price.010
  claim: 暴风褐啤(Flask of Stormwind Tawny, item 2593) 商人标价 1 银 50 铜，15 级可饮——「在暴风城喝一杯本地酒」的标准价。
  tag: ✅
  source: Wowhead Classic · item 2593
  source_url: https://www.wowhead.com/classic/item=2593&xml
  quote: '"buyprice":150,"sellprice":37'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "陶壶或木杯装的褐色麦酒，表面一层细密酒沫"
  negative: "玻璃啤酒杯配商标, 易拉罐"

- fact_id: stormwind.price.011
  claim: 矮人烈酒皮囊(Skin of Dwarven Stout, 2596) 1 银 20 铜；矮人蜜酒(Flagon of Dwarven Honeymead, 2594) 15 银——同是酒，档次差 12.5 倍。
  tag: ✅
  source: Wowhead Classic · item 2596 / 2594
  source_url: https://www.wowhead.com/classic/item=2596&xml
  quote: '2596 "buyprice":120,"sellprice":30 ; 2594 "buyprice":1500,"sellprice":375'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "鼓胀的皮酒囊配木塞；另一款是带把手的大陶酒壶"
  negative: "现代酒瓶, 印刷标签"

- fact_id: stormwind.price.012
  claim: 背包价格阶梯（商人标价）：6 格棕色小包 5 银(4496) → 8 格棕色皮背包 25 银(4498) → 10 格重型棕色包 2 金(4497) → 12 格巨型棕色麻袋 10 金(4499)。每多两格，价钱跳 4–5 倍。
  tag: ✅
  source: Wowhead Classic · item 4496 / 4498 / 4497 / 4499（与 Warcraft Wiki · Thurman Mullby 商人清单的 2g / 10g 交叉吻合）
  source_url: https://www.wowhead.com/classic/item=4499&xml
  quote: '4496 "buyprice":500 ; 4498 "buyprice":2500 ; 4497 "buyprice":20000 ; 4499 "buyprice":100000'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "粗麻与皮革缝制的束口背包，铜扣，肩带磨白"
  negative: "尼龙登山包, 拉链, 现代 logo"

- fact_id: stormwind.price.013
  claim: 次级治疗药水(Lesser Healing Potion, item 858) 商人标价 1 银。
  tag: ✅
  source: Wowhead Classic · item 858
  source_url: https://www.wowhead.com/classic/item=858&xml
  quote: '"buyprice":100,"reqlevel":3,"sellprice":25'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "小玻璃瓶装的橙红色药水，木塞封口，瓶身缠一圈粗布签"
  negative: "现代药瓶, 印刷说明书"

- fact_id: stormwind.price.014
  claim: 弯刀(Cutlass, item 851) 商人标价 20 银 23 铜，需 10 级；数据库 buyprice=2023 与维基商人清单的「20s 23c」逐字吻合，交叉验证通过。
  tag: ✅
  source: Wowhead Classic · item 851 ＋ Warcraft Wiki · Gunther Weller 商人清单
  source_url: https://www.wowhead.com/classic/item=851&xml
  quote: '"buyprice":2023,"reqlevel":10,"sellprice":404 ／ 维基："Cutlass" - "20s 23c"'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "单刃弯身短剑，半篮状护手，刃面有细磨痕"
  negative: "日式刀, 现代战术刀"

- fact_id: stormwind.price.015
  claim: 贸易区「威勒军械行(Weller's Arsenal)」的武器价带：斧头 24 银 10 铜、锤 17 银 40 铜、弯刀 20 银 23 铜、四分棍 30 银 22 铜、长剑 87 银 45 铜、重矛 2 金 71 银 33 铜——一把像样的武器 ＝ 几十银到数金。
  tag: ✅
  source: Warcraft Wiki · Gunther Weller（商人物品表；店在贸易区拍卖行旁）
  source_url: https://warcraft.wiki.gg/wiki/Gunther_Weller
  quote: '"Hatchet" - "24s 10c" / "Mace" - "17s 40c" / "Quarter Staff" - "30s 22c" / "Longsword" - "87s 45c" / "Heavy Spear" - "2g 71s 33c"'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "军械铺墙面挂满长剑、战斧、长矛与木柄锤，兵器架按长短分排"
  negative: "火枪柜台, 现代货架标价签"

- fact_id: stormwind.price.016
  claim: 【爆点】同区「雄狮之心军械库(Lionheart Armory)」的布甲便宜到离谱：见习长袍 35 铜、织布外衣 46 铜、厚布护甲 79 铜、厚布护腿 1 银 16 铜——一件能穿的衣服比一条新鲜面包(1 银 25 铜)还便宜。
  tag: ✅
  source: Warcraft Wiki · Carla Granger（布甲商人物品表）
  source_url: https://warcraft.wiki.gg/wiki/Carla_Granger
  quote: '"[Acolyte`s Robe]" costs "35c" / "[Knitted Tunic]" costs "46c" / "[Heavy Weave Armor]" costs "79c" / "[Thick Cloth Pants]" costs "1s 16c"'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "军械库内一排排素色布袍与织布外衣挂在木杆上，旁边是皮甲与锁甲架"
  negative: "塑料衣架, 吊牌价签"

- fact_id: stormwind.price.017
  claim: 工具与耗材全在 1 银以内：矿镐 81 铜(2901)、钓鱼竿 23 铜(6256)、空瓶 20 铜(3371)、粗线 10 铜(2320)。
  tag: ✅
  source: Wowhead Classic · item 2901 / 6256 / 3371 / 2320
  source_url: https://www.wowhead.com/classic/item=2901&xml
  quote: '2901 "buyprice":81 ; 6256 "buyprice":23 ; 3371 "buyprice":20 ; 2320 "buyprice":10'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "杂货铺柜台上摊着矿镐、线轴、空玻璃小瓶、钓竿"
  negative: "电动工具, 塑料件"

- fact_id: stormwind.price.018
  claim: 坐骑（棕马缰绳 item 5656）在 Classic Era 数据库里的商人标价是 80 金，需 40 级、需骑术 75；配套「学徒骑术」训练费 20 金——40 级拿到第一匹马的总门槛约 100 金。
  tag: ✅
  source: Wowhead Classic · item 5656 ＋ Icy Veins · WoW Classic Riding Profession Guide
  source_url: https://www.wowhead.com/classic/item=5656&xml
  quote: '"buyprice":800000,"reqlevel":40,"reqskill":148 ／ Icy Veins: "Apprentice Riding costs 20 Gold (before discounts) at Level 40" ; "Rare mounts at Level 40 cost 80 Gold each before discounts."'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "牵着一匹配鞍棕马，皮缰绳与马镫，鬃毛梳过"
  negative: "机械坐骑, 现代马术头盔"

- fact_id: stormwind.price.019
  claim: 60 级史诗坐骑的 Classic 口径是「精通骑术 100 金 ＋ 史诗坐骑 900 金 ≈ 1000 金」，是全游戏最大的金币吸收口。
  tag: ✅
  source: Icy Veins · WoW Classic Riding Profession Guide
  source_url: https://www.icy-veins.com/wow-classic/riding-profession-guide
  quote: '"Journeyman Riding costs 100 Gold (before discounts) at Level 60" ; "Epic mounts at Level 60 cost 900 Gold each before discounts."'
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.price.020
  claim: 坐骑钱在「马价 vs 骑术费」之间的分配被 1.12.1 补丁对调过：此前 马 80 金 ＋ 骑术 20 金，此后 马 20 金 ＋ 骑术 80 金；史诗档从「史诗坐骑 1000 金」改成「坐骑 100 金 ＋ 骑术 1000 金」。总额基本不变，**口播只报总额 100 金 / 1000 金最安全**。
  tag: ✅
  source: Warcraft Wiki · Patch 1.12.1
  source_url: https://warcraft.wiki.gg/wiki/Patch_1.12.1
  quote: '"Instead of paying 80g for a regular mount (undiscounted) and 20g (undiscounted) to learn riding for that mount, you will pay 20g for a regular mount and 80g to learn the riding skill." / "Instead of paying 1000g for an epic mount (undiscounted), you will pay 100g (undiscounted) for the epic mount and 1000g (undiscounted) for the riding skill."'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
```

### 三、服务与商业设施（stormwind.trade.*）

```yaml
- fact_id: stormwind.trade.001
  claim: 【爆点】Vanilla 的旅店**不收住宿费**。旅店老板提供的是「把炉石绑在这儿」＋ 兼卖食物饮料；游戏里根本没有付钱开房这个动作，住店的收益是「充分休息」经验加成（旅店/城市里的休息积累速度是野外的 4 倍）。
  tag: ✅
  source: Warcraft Wiki · Innkeeper ＋ Warcraft Wiki · Rest（两页都不存在任何收费条目，Rest 机制不涉及付费）
  source_url: https://warcraft.wiki.gg/wiki/Innkeeper
  quote: '"To set or change the bind point for your hearthstone, talk to an innkeeper and click Make this inn your home." ／ Rest: "Characters can also earn rest by logging off in other locations, although they will earn rest at a quarter of the speed."'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旅店二楼一排木床，床脚堆着旅人包袱；楼下壁炉与长桌"
  negative: "前台登记簿, 房卡, 收银动作, 墙上挂房价牌"

- fact_id: stormwind.trade.002
  claim: 暴风城的旅店叫「镀金玫瑰(The Gilded Rose)」，在贸易区，老板娘是艾莉森；它紧挨银行、拍卖行与邮箱。
  tag: ✅
  source: Warcraft Wiki · Gilded Rose
  source_url: https://warcraft.wiki.gg/wiki/Gilded_Rose
  quote: '"Innkeeper Allison is the host and offers a [Hearthstone] point as well as being a vendor of food and drink." / "its proximity to the bank, Auction House, and an ever-popular mailbox"'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "挂着镀金玫瑰招牌的两层木石结构旅店，暖黄窗光"
  negative: "霓虹招牌, 门牌号码"

- fact_id: stormwind.trade.003
  claim: 【爆点】暴风城 ↔ 铁炉堡的**深铁矿道（地铁）完全免费**，全程 60 秒、每站停 12 秒；它是侏儒工程学建的全封闭双轨地下铁路，有一段穿过地下湖。
  tag: ✅
  source: Warcraft Wiki · Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The service is provided free of charge to travelers between the Alliance-aligned cities of Ironforge and Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "地下双轨隧道，三节连挂的封闭车厢，一段隧道外是透明的地下湖水体"
  negative: "售票口, 闸机, 车票, 刷卡"

- fact_id: stormwind.trade.004
  claim: 狮鹫是收费的，价钱写死在客户端数据里（TaxiPath.Cost，单位铜），按航段累加。暴风城出发单程价（Classic Era 1.15.5）：→铁炉堡 50 铜、→哨兵岭(西部荒野) 1 银 10 铜、→湖畔镇(赤脊山) 2 银 10 铜、→夜色镇(暮色森林) 3 银 30 铜、→藏宝海湾(荆棘谷) 6 银 30 铜、→守望堡(诅咒之地) 8 银 30 铜、→摩根的岗哨(燃烧平原) 8 银 30 铜。
  tag: ✅
  source: wago.tools · DB2 TaxiPath @ build 1.15.5.57638（Classic Era 客户端数据）；节点名取自同构建 TaxiNodes
  source_url: https://wago.tools/db2/TaxiPath/csv?build=1.15.5.57638
  quote: "ID,FromTaxiNode,ToTaxiNode,Cost / 13,2,6,50 / 6,2,4,110 / 9,2,5,210 / 23,2,12,330 / 40,2,19,630 / 245,2,45,830 / 427,2,71,830"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城墙上的狮鹫栖架，一排狮鹫扑腾整羽，驯鹫人牵着缰绳"
  negative: "机场, 登机牌, 候机厅"

- fact_id: stormwind.trade.005
  claim: 同源数据里铁炉堡出发的单程价：→塞尔萨玛(洛克莫丹) 1 银 10 铜、→米奈希尔港(湿地) 3 银 30 铜、→南海镇(希尔斯布莱德) 3 银 30 铜——「跨一个区」的行情就是 1–3 银。
  tag: ✅
  source: wago.tools · DB2 TaxiPath @ build 1.15.5.57638
  source_url: https://wago.tools/db2/TaxiPath/csv?build=1.15.5.57638
  quote: "16,6,8,110 / 18,6,7,330 / 27,6,14,330"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.006
  claim: 暴风城的驯鹫人叫邓加·长饮(Dungar Longdrink)，狮鹫栖架在城墙上，共 11 条航线（含藏宝海湾、夜色镇、铁炉堡、守望堡等）。
  tag: ✅
  source: Warcraft Wiki · Dungar Longdrink
  source_url: https://warcraft.wiki.gg/wiki/Dungar_Longdrink
  quote: "Dungar Longdrink is a human gryphon flight master located in the Gryphon Roost in Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.007
  claim: 寄信要付邮资 **30 铜**，且按「填了几个附件格」收（一格 30 铜，两格 60 铜），不是按件数；随信寄钱本身不额外收费。
  tag: ✅
  source: Blizzard 官方论坛 · Cost of mail（Classic 玩家实测与互相更正）
  source_url: https://eu.forums.blizzard.com/en/wow/t/cost-of-mail/465466
  quote: '"Each slot you fill is 30 copper" / "30 c per square you put stuff into."'
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌邮箱，铜制投信口，箱顶一面小红旗"
  negative: "邮票, 现代信封, 快递单"

- fact_id: stormwind.trade.008
  claim: 拍卖行成交抽成：本阵营拍卖行抽 5%，中立拍卖行（藏宝海湾／加基森／永望镇）抽 15%。
  tag: ✅
  source: Warcraft Wiki · Auction house ＋ Lifevor · WoW Classic AH Cut Calculator
  source_url: https://warcraft.wiki.gg/wiki/Auction_house
  quote: '"When you successfully sell an item on the auction house, the house will take 5% of the winning bid as its cut." ／ Lifevor（中立行）："Charges a heavy 15% sales cut"'
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.009
  claim: 上架先押一笔押金，按该物品**卖给商人的回收价**计比例：本阵营 12/24/48 小时 ＝ 15%/30%/60%；中立行是 5 倍（75%/150%/300%）。卖出全额退还，流拍或撤单则没收。
  tag: ✅
  source: Lifevor · WoW Classic Auction House Cut Calculator
  source_url: https://lifevor.com/en/tools/wow-classic-auction-house-cut-calculator
  quote: '"12 Hours: 15% (0.15) of Vendor Price" / "48 Hours: 60% (0.60) of Vendor Price" / 中立行 "12 Hours: 75% (0.75) of Vendor Price" / "Refunded in full upon successful sale"'
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.010
  claim: 拍卖行在贸易区正中（1.9 补丁把它装进贸易区中央），1.9 起暴风城／铁炉堡／达纳苏斯三城拍卖行数据互通——在暴风城挂的货，铁炉堡的人也能买。
  tag: ✅
  source: Warcraft Wiki · Trade District ＋ Patch 1.9.0 说明
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "Patch 1.9 added the linked Auction House in the center of the Trade District"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "拍卖行大厅里三名拍卖师各守一张长案，案上摊着羊皮纸与账册，墙边排着货箱"
  negative: "电子屏, 拍卖槌台, 现代竞拍席"

- fact_id: stormwind.trade.011
  claim: 暴风城**没有讨价还价机制**：商人标价固定，唯一能压价的是声望——友善 5%、尊敬 10%、崇敬 15%、崇拜 20%，且该折扣同样作用于**修理费与狮鹫票价**。
  tag: ✅
  source: Warcraft Wiki · Reputation
  source_url: https://warcraft.wiki.gg/wiki/Reputation
  quote: "All vendors, flightmasters, and repairs with an associate faction now give discounts at all levels above neutral: (Friendly: 5%, Honored: 10%, Revered: 15%, Exalted: 20%)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "砍价手势, 摊主让价桥段"

- fact_id: stormwind.trade.012
  claim: 银行叫「暴风城账房(Stormwind Counting House)」，在贸易区，7 名银行职员；NPC 自述业务是「金融账户 ＋ 贵重物品保险箱」，并吹嘘「历史上从没被偷过东西」。
  tag: ✅
  source: Warcraft Wiki · Stormwind Counting House
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Counting_House
  quote: '"We offer financial accounts and safety deposit boxes for valuable items." / "No one''s ever stolen anything out of here. Not in the whole history of... the whole history!"'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌银行大厅，柜台后是铁栅与整墙保险箱柜，职员伏案记账"
  negative: "ATM, 玻璃幕墙, 柜员机"

- fact_id: stormwind.trade.013
  claim: 银行基础存放 24 格，之后可逐格购买「放包的槽位」，价钱阶梯式暴涨：第 1 格 10 银 → 第 2 格 1 金 → 第 3 格 10 金 → 其余每格 25 金（买满合计 111 金 10 银）。**槽位总数在不同来源里是 6 或 7，需按最终版本再核。**
  tag: ⚠️
  source: Warcraft Wiki · Bag slots（历史条目）；槽位数在 Classic 语境下来源冲突
  source_url: https://warcraft.wiki.gg/wiki/Bag_slots
  quote: "starting at 10s, then increasing to 1g, then 10g, then 25g for the rest, for a total of 111g 10s for all seven slots."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.014
  claim: 修理要花钱：装备有耐久，任何卖武器／护甲／铁匠材料的 NPC 都能修；费用随物品等级与品质走（普通品质护甲基准约 需修耐久点数 ×(物品等级−32.5)×0.02 银），所以低级装备修一次只要几十铜到几银。
  tag: ⚠️
  source: Warcraft Wiki · Durability（可修理者范围）＋ Fandom Durability 页公式（经搜索摘取，公式未逐字复核）
  source_url: https://warcraft.wiki.gg/wiki/Durability
  quote: '"Any NPC vendor who sells weapons or armor (or Blacksmithing supplies) can repair durability." ／ 公式："Durability points to be repaired * (ilevel - 32.5) * 0.02 silver"'
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "铁匠铺砧台边，匠人拿着旅人的剑对着炉火看刃口"
  negative: "维修单据, 保修卡"

- fact_id: stormwind.trade.015
  claim: 贸易区卖的品类被官方明文列过：奶酪、奥术材料与试剂、杂货、鲜花、布甲／皮甲／锁甲、弓、枪、成衣；有名号的店铺包括空箭袋(弓箭)、日用百货(杂货)、雄狮之心军械库(护甲)、佩斯特药剂铺(试剂)、崔亚斯奶酪铺、威勒军械行(武器)，运河边还有裁缝铺、丹曼家族珠宝行、鲜花摊与加利纳酒庄。
  tag: ✅
  source: Warcraft Wiki · Trade District
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: '"The goods that are sold in the Trade District are cheese, arcane goods and reagents, general goods, flowers, cloth/leather/mail armor, bows, guns, and clothes." / "The Empty Quiver / Everyday Merchandise / Lionheart Armory / Pestle''s Apothecary / Trias'' Cheese / Weller''s Arsenal"'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌街面两侧一间挨一间的店铺，木招牌悬挑而出：奶酪、军械、药剂、鲜花；门口摆着货筐与酒桶"
  negative: "玻璃橱窗, 印刷海报, 品牌 logo"

- fact_id: stormwind.trade.016
  claim: 【lore】暴风城的国库主要靠**向集市商人收税**填满——城市财政建立在商业税上，而不是采邑地租。
  tag: ✅
  source: Warcraft Wiki · Stormwind City
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "most of the city's coffers are filled with the taxes taken from merchants in the busy market"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "对旅人收入城税, 关卡收费"

- fact_id: stormwind.trade.017
  claim: 旅行者侧**不存在任何税**：进城不收费、买卖不抽税，唯一的抽成是拍卖行的 5%；lore 里的商税是城市向 NPC 商人收的，与外来者无关。
  tag: ⚠️
  source: 本路交叉结论（Trade District / Stormwind City / Auction house 三页均无面向玩家的税项）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "（三页均无玩家税收条目）"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "城门税吏, 入城费, 商品税单"

- fact_id: stormwind.trade.018
  claim: 商人的回收价远低于售价：粗面包卖 25 铜、回收 1 铜（25:1）；弯刀卖 20 银 23 铜、回收 4 银 4 铜（5:1）。**买贵卖贱是这个经济体的底层规则**，也是「今日总账单」最容易出戏的地方。
  tag: ✅
  source: Wowhead Classic · item 4540 / 851
  source_url: https://www.wowhead.com/classic/item=851&xml
  quote: '4540 "buyprice":25,"sellprice":1 ; 851 "buyprice":2023,"sellprice":404'
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.019
  claim: 低级任务现金报酬实测：艾尔文森林 7 级任务《法戈第矿洞》给 1 银 25 铜；赤脊山 20 级任务《豺狼人的哀嚎》给 9（数据库只显示单栏数字，按上下文判为 9 银）。
  tag: ⚠️
  source: classicdb.ch（1.12 数据库）quest 62 / quest 124
  source_url: https://classicdb.ch/?quest=62
  quote: 'quest 62: "You will also receive: 1 25" ; quest 124: "You will also receive: 9"'
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.020
  claim: 玩家实测口径：练到 40 级（买第一匹马的门槛）时身上大约 60–95 金（带采集专业约 95 金，无专业约 62 金）——**攒一匹马 ≈ 一路练到 40 级的全部积蓄**。
  tag: ⚠️
  source: Blizzard 官方论坛玩家统计（非官方数值）
  source_url: https://eu.forums.blizzard.com/en/wow/t/how-big-is-the-quest-gold-bonus-with-60/84849
  quote: "A character with Herbalism/Mining reached level 40 with 95 gold, while a character with no professions had 62 gold"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.trade.021
  claim: 船与飞艇（米奈希尔港↔奥特兰克海、藏宝海湾↔棘齿城等）不收钱，只有狮鹫收钱——「贵的是天上，海上免费」。
  tag: ⚠️
  source: WoW Classic 旅行攻略（多站转述，未找到官方逐字条文）
  source_url: https://www.dexerto.com/world-of-warcraft/where-to-go-in-wow-classic-full-horde-and-alliance-travel-route-guide-996849/
  quote: "ships and zeppelins are free of charge"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "码头售票, 船票"
```

---

## 两个锚

### 锚 A ＝ 一顿普通饭 ＝ **2 银 50 铜**

| 档次 | 组合 | 价钱 | 依据 |
|---|---|---|---|
| 粗饭档（劳工） | 粗面包 25 铜 ＋ 清泉水 25 铜 | **50 铜** | price.001 / price.003 |
| **标准档（锚 A）** | **新鲜面包 1 银 25 铜 ＋ 冰镇牛奶 1 银 25 铜** | **2 银 50 铜** | price.004 / price.005 |
| 有肉有酒档 | 大块烤肉 1 银 25 铜 ＋ 暴风褐啤 1 银 50 铜 | 2 银 75 铜 | price.006 / price.010 |
| 讲究档（旅人挥霍） | 新鲜面包 1 银 25 铜 ＋ 暴风布里干酪 10 银 ＋ 矮人蜜酒 15 银 | 26 银 25 铜 | price.004 / price.009 / price.011 |

**定死：锚 A ＝ 250 铜。** 全片所有「相当于几顿饭」＝ 价格(铜) ÷ 250。
口播时要顺带把「粗饭 50 铜 vs 讲究档 26 银」这个 50 倍落差说出来——**这是暴风城最直观的阶级刻度**。

### 锚 B ＝ 一份日常收入 ＝ **1 银／天**（普通劳工日薪，⚠️ 推算）

游戏里没有「日工钱」这个设定，必须推。推法与依据：

1. **设定定性**：铜便士是「最小额、最常见的钱」，银格罗特才是士兵与商人手里常见的钱（money.003 的币名分层）——这说明**体力劳动者的收入以铜计、不以银计**，量级在几十铜到一百铜／天。
2. **食物反推**：最便宜的一顿（粗面包＋泉水）＝ 50 铜。真实前工业社会里，口粮约占日薪的 1/3 到 1/2。以 1/2 反推 ⇒ **日薪 ≈ 100 铜 ＝ 1 银**。
3. **冒险者对照**：艾尔文森林 7 级任务《法戈第矿洞》的酬劳是 1 银 25 铜（trade.019）——**冒险者跑一趟腿 ≈ 平民干一整天**。这正是「为什么人人都想去当冒险者」的经济学解释，可以直接进口播。
4. **总量校验**：练到 40 级共攒 60–95 金（trade.020）＝ 6000–9500 银 ＝ 6000–9500 个平民日薪。而一匹马 80 金 ＝ 8000 天工钱 ≈ **平民 22 年不吃不喝**。这个数字站得住：马在设定里本来就不是平民买得起的东西。

**定死：锚 B ＝ 100 铜／天。** 全片所有「相当于几天收入」＝ 价格(铜) ÷ 100。

**替代方案（若导演想让平民更宽裕）**：取 锚 B ＝ 2 银／天。那时一顿标准饭 ＝ 1.25 天工钱，一匹马 ＝ 11 年，爽点会削弱一半，**不推荐**。
**冒险者口径（仅用于对比，不作主尺）**：跑腿冒险者日入约 10 银量级（7 级任务 1 银 25 铜、20 级任务约 9 银，一天跑数个任务再卖点杂货）。⚠️ 纯推算。

---

## 物价总表

> 换算：顿 ＝ 价格 ÷ 250 铜；天 ＝ 价格 ÷ 100 铜。**这张表下游直接进口播与「今日总账单」。**

| 商品／服务 | Vanilla 标价 | ＝ 铜 | 几顿饭 | 几天收入 | fact_id | 来源 |
|---|---|---|---|---|---|---|
| 粗面包 | 25 铜 | 25 | 0.1 | 0.25 | price.001 | Wowhead item 4540 |
| 硬肉干 | 25 铜 | 25 | 0.1 | 0.25 | price.002 | Wowhead item 117 |
| 清泉水 | 25 铜 | 25 | 0.1 | 0.25 | price.003 | Wowhead item 159 |
| 新鲜面包 | 1 银 25 铜 | 125 | 0.5 | 1.25 | price.004 | Wowhead item 4541 |
| 冰镇牛奶 | 1 银 25 铜 | 125 | 0.5 | 1.25 | price.005 | Wowhead item 1179 |
| 大块烤肉 | 1 银 25 铜 | 125 | 0.5 | 1.25 | price.006 | Wowhead item 2287 |
| 达拉然浓干酪 | 1 银 25 铜 | 125 | 0.5 | 1.25 | price.007 | Wowhead item 414 |
| 暴风褐啤（一壶酒） | 1 银 50 铜 | 150 | 0.6 | 1.5 | price.010 | Wowhead item 2593 |
| 矮人烈酒皮囊 | 1 银 20 铜 | 120 | 0.48 | 1.2 | price.011 | Wowhead item 2596 |
| 玉米面包／矮人陈干酪／西瓜汁 | 5 银 | 500 | 2 | 5 | price.008 | Wowhead item 4542/422/1205 |
| 暴风布里干酪 | 10 银 | 1000 | 4 | 10 | price.009 | Wowhead item 1707 |
| 甜花蜜 | 10 银 | 1000 | 4 | 10 | price.009 | Wowhead item 1708 |
| 矮人蜜酒 | 15 银 | 1500 | 6 | 15 | price.011 | Wowhead item 2594 |
| **旅店住一晚** | **0（免费）** | 0 | 0 | 0 | trade.001 | Warcraft Wiki Innkeeper/Rest |
| 见习长袍（布甲上衣） | 35 铜 | 35 | 0.14 | 0.35 | price.016 | Wiki · Carla Granger |
| 织布外衣 | 46 铜 | 46 | 0.18 | 0.46 | price.016 | Wiki · Carla Granger |
| 厚布护腿 | 1 银 16 铜 | 116 | 0.46 | 1.16 | price.016 | Wiki · Carla Granger |
| 钓鱼竿 | 23 铜 | 23 | 0.09 | 0.23 | price.017 | Wowhead item 6256 |
| 矿镐 | 81 铜 | 81 | 0.32 | 0.81 | price.017 | Wowhead item 2901 |
| 次级治疗药水 | 1 银 | 100 | 0.4 | 1 | price.013 | Wowhead item 858 |
| 6 格背包 | 5 银 | 500 | 2 | 5 | price.012 | Wowhead item 4496 |
| 8 格背包 | 25 银 | 2500 | 10 | 25 | price.012 | Wowhead item 4498 |
| 10 格背包 | 2 金 | 20000 | 80 | 200 | price.012 | Wowhead item 4497 |
| 12 格大麻袋 | 10 金 | 100000 | 400 | 1000 | price.012 | Wowhead item 4499 |
| 锤（最便宜的像样武器） | 17 银 40 铜 | 1740 | 7 | 17.4 | price.015 | Wiki · Gunther Weller |
| 弯刀 | 20 银 23 铜 | 2023 | 8.1 | 20.2 | price.014 | Wowhead item 851 |
| 长剑 | 87 银 45 铜 | 8745 | 35 | 87.5 | price.015 | Wiki · Gunther Weller |
| 重矛 | 2 金 71 银 33 铜 | 27133 | 108.5 | 271 | price.015 | Wiki · Gunther Weller |
| 狮鹫 暴风城→铁炉堡 | 50 铜 | 50 | 0.2 | 0.5 | trade.004 | DB2 TaxiPath 1.15.5 |
| 狮鹫 暴风城→哨兵岭 | 1 银 10 铜 | 110 | 0.44 | 1.1 | trade.004 | DB2 TaxiPath 1.15.5 |
| 狮鹫 暴风城→湖畔镇 | 2 银 10 铜 | 210 | 0.84 | 2.1 | trade.004 | DB2 TaxiPath 1.15.5 |
| 狮鹫 暴风城→夜色镇 | 3 银 30 铜 | 330 | 1.3 | 3.3 | trade.004 | DB2 TaxiPath 1.15.5 |
| 狮鹫 暴风城→藏宝海湾 | 6 银 30 铜 | 630 | 2.5 | 6.3 | trade.004 | DB2 TaxiPath 1.15.5 |
| 狮鹫 暴风城→守望堡 | 8 银 30 铜 | 830 | 3.3 | 8.3 | trade.004 | DB2 TaxiPath 1.15.5 |
| **深铁矿道（地铁）到铁炉堡** | **0（免费）** | 0 | 0 | 0 | trade.003 | Warcraft Wiki Deeprun Tram |
| 寄一封带附件的信 | 30 铜／格 | 30 | 0.12 | 0.3 | trade.007 | Blizzard 论坛实测 |
| 银行第 1 个包位 | 10 银 | 1000 | 4 | 10 | trade.013 | Wiki · Bag slots |
| 银行第 2 个包位 | 1 金 | 10000 | 40 | 100 | trade.013 | Wiki · Bag slots |
| 银行第 3 个包位 | 10 金 | 100000 | 400 | 1000 | trade.013 | Wiki · Bag slots |
| 修一次低级装备 | 几十铜–几银 ⚠️ | 30–300 | 0.1–1.2 | 0.3–3 | trade.014 | 公式推算 |
| **一匹马（40 级坐骑，含骑术）** | **约 100 金** | 1000000 | **4000** | **10000（≈27 年）** | price.018 / price.020 | Wowhead item 5656 ＋ Icy Veins |
| **史诗坐骑（60 级，含骑术）** | **约 1000 金** | 10000000 | **40000** | **100000（≈274 年）** | price.019 / price.020 | Icy Veins ＋ Patch 1.12.1 |

**口播用的三组对照（建议直接用）**
- 「一件能穿的布袍 35 铜 < 一条新鲜面包 1 银 25 铜」——**在暴风城，穿的比吃的便宜。**
- 「住一晚旅店 0 铜、坐地铁去另一座首都 0 铜、但寄一封信要 30 铜」——**这座城市免你的住宿和交通，却收你的邮费。**
- 「一匹马 ＝ 一个劳工 8000 天的工钱 ＝ 4000 顿饭」——**马不是交通工具，是一栋房子。**

---

## 旅行者预算建议

场景：吃三顿 ＋ 住一晚 ＋ 买两件小东西 ＋ 坐一次狮鹫。

| 项目 | 选择 | 花费 |
|---|---|---|
| 早饭 | 粗面包 ＋ 清泉水（入城先垫一口） | 50 铜 |
| 午饭 | 新鲜面包 ＋ 暴风褐啤 | 2 银 75 铜 |
| 晚饭 | 大块烤肉 ＋ 暴风布里干酪（旅人挥霍一次） | 11 银 25 铜 |
| 住宿 | 镀金玫瑰旅店一晚 | **0 铜** |
| 小东西之一 | 6 格棕色小包（装战利品） | 5 银 |
| 小东西之二 | 次级治疗药水 | 1 银 |
| 狮鹫 | 暴风城 → 夜色镇 单程 | 3 银 30 铜 |
| 邮费 | 寄一封信回去 | 30 铜 |
| **合计** | | **24 银 10 铜** |

**建议进城带 1 金（100 银）。** 理由：
- 24 银 10 铜是「按计划花」的数；**留 4 倍余量**才经得起临时起意（再点一壶 15 银的矮人蜜酒、把 8 格背包 25 银也买了、或者飞一趟 8 银 30 铜的守望堡）。
- 1 金 ＝ 400 顿饭 ＝ 100 天平民工钱，对暴风城市民来说是「一笔明显的巨款」，**够她全天不看价钱地花，却买不起任何一件真正贵的东西**（马 80 金、10 格背包 2 金、银行第二个包位 1 金）。这正是本集想要的戏剧张力。
- 夜里总账：花掉 24 银 10 铜，**剩 75 银 90 铜**。这个余额可以直接做收尾台词——「我带了一金进城，吃了三顿、飞了一趟、睡了一晚，最后发现：我离一匹马，还差 79 个我这样的一天。」

**结账口径提醒**：若她中途把东西卖给商人，务必按回收价算（trade.018，粗面包 25 铜买进、1 铜卖出）。**买贵卖贱这一条如果写反，整本账立刻不成立。**

---

## 版本错置清单（❌）

| 错误说法 | 真相 | 依据 |
|---|---|---|
| 「狮鹫飞一趟只要 5–36 铜」 | 那是**现行正式服**被下调后的 TaxiPath 数值（同一张表 retail 构建里暴风城→哨兵岭 ＝ 5 铜）；Vanilla／Classic Era 是 110 铜。**引 DB2 数据必须带 Classic Era 构建号。** | wago.tools TaxiPath：retail `6,2,4,5` vs 1.15.5 `6,2,4,110` |
| 「40 级坐骑 10 金、骑术 80/90 金」 | 这是 **1.12.1 之后的分配**（或 TBC 之后的口径）。1.12.1 之前是马 80 金 ＋ 骑术 20 金；WoW Classic(1.13+) 用的是**马 80 金 ＋ 骑术 20 金**。总额都约 100 金，**只报总额不会错**。 | Patch 1.12.1 原文；Wowhead Classic item 5656 buyprice=80g；classicdb(1.12) 同一物品 10g |
| 「60 级史诗坐骑 600 金骑术」 | 无此数值。Classic 是 精通骑术 100 金 ＋ 史诗坐骑 900 金；1.12.1 文本里是 100 金 ＋ 1000 金。 | Icy Veins Classic 骑术指南；Patch 1.12.1 |
| 「TBC 之后 30 级就能骑坐骑」 | 那是 2.4.3 的改动（rare 坐骑等级需求由 40 降到 30），**不属于 Vanilla**。 | Warcraft Wiki · Mount |
| 「中立拍卖行抽 30%」 | Vanilla/Classic 是 15%（本阵营 5%）。30% 是个别攻略站的错记。 | Lifevor Classic AH 计算器 ＋ Warcraft Wiki |
| 「银行有 6 个 98 格的标签页」 | 那是现行正式服 11.2.0 之后的银行。Vanilla 是 24 格 ＋ 逐格买的放包槽位。 | Warcraft Wiki · Character Bank |
| 「拍卖行在矮人区／在旅店旁边」 | 矮人区那座是**后来加的**；Cataclysm 才把贸易区的拍卖行挪到旅店附近。Vanilla 定位是「1.9 起在贸易区正中」。 | Warcraft Wiki · Trade District |
| 「WoW 里寄信不要钱」 | 现行版本的维基 Mailbox 页确实没有邮资条目，但 Vanilla/Classic 是 **30 铜／附件格**。 | Blizzard 论坛 Classic 实测帖 |
| 「暴风城金币重 8 克、银币掺锡、有斗鸡眼硬币」 | 出自玩家 RP 百科（Moon Guard / The First Regiment），**不是官方设定**，不得口播。 | money.010 |
| 「Classic 低级任务动辄给几十银」 | 那是 2019 Classic 测试期一个**已修的 bug**（任务奖励按角色等级缩放）引发的论坛热帖，不是 Vanilla 数值。Vanilla 是 7 级任务 1 银 25 铜量级。 | Blizzard 论坛「Quest reward silver too high」帖 ＋ classicdb quest 62 |

---

## 未查 / Open questions

1. **`A Baying of Gnolls`(quest 124) 的 9 是 9 银还是 9 铜**——classicdb 只渲染出单栏数字。建议下游用 Classic 客户端实测，或换一个明确标注单位的数据源复核。**在复核前，口播不要引用 20 级任务的具体报酬。**
2. **银行放包槽位在 Vanilla 到底是 6 个还是 7 个**——维基历史条目写 7 个（合计 111 金 10 银），Classic 语境的攻略写 6 个。价钱阶梯（10 银／1 金／10 金／此后 25 金）两边一致，可以放心用；总数待核。
3. **修理费的具体数字**——只拿到公式，没拿到「某件低级装备修一次 ＝ X 铜」的实测值。若剧情要念修理账单，需补一条实测。
4. **暴风城旅店老板娘艾莉森具体卖哪几样、各卖多少**——Warcraft Wiki 的 Gilded Rose 页没有物品表。若某镜要拍「她在旅店柜台点单」，建议按 price.004/005/006/010（面包／牛奶／烤肉／褐啤）组合，不要新编价格。
5. **硬币的确切纹样**——官方只给了「部落铜币是苦工的脸」和两套硬币图标，**暴风城硬币压什么图案没有任何官方文字**。画面上若要特写币面，属于合理补完，需在 refs 里标 ⚠️（建议：狮首侧像／暴风城狮鹫纹，绝不写具体年号或数字面额）。
6. **是否存在任何信用／借贷／票据**——检索无果，倾向于「没有」，但属于「查不到」而非「查到没有」。
7. **船与飞艇免费**——只有攻略站转述（T3），没找到官方逐字条文。若要口播，建议改成「水路不收钱，只有狮鹫收钱」并弱化断言强度。

---

## 来源清单

- **T0/T1 客户端与官方数据库**
  - Wowhead Classic 物品 XML：`https://www.wowhead.com/classic/item={id}&xml`（本路共读取 item 4540/117/159/4541/1179/2287/414/422/1205/4542/1707/1708/2593/2594/2596/4496/4497/4498/4499/851/858/2901/6256/3371/2320/5656）
  - wago.tools DB2 `TaxiPath` / `TaxiNodes` @ build **1.15.5.57638**（Classic Era）
- **T1 带引用的维基条目**（warcraft.wiki.gg）：Money、Patch 1.12.1、Trade District、Stormwind City、Stormwind Counting House、Gilded Rose、Innkeeper、Rest、Reputation、Durability、Deeprun Tram、Auction house、Dungar Longdrink、Gunther Weller、Carla Granger、Thurman Mullby、Bag slots
- **T2 有出处的攻略／工具**：Icy Veins《WoW Classic Riding Profession Guide》、Lifevor《WoW Classic AH Cut Calculator》、classicdb.ch（1.12 数据库，quest 62/124、item 5656）、PCGamesN Classic AH 指南
- **T3 玩家实测**：Blizzard 官方论坛（Cost of mail、Flight Path Costs、40 级金币存量帖）
- **T4 仅作反例**：Moon Guard Wiki《Currency of Stormwind》等 RP 玩家百科
