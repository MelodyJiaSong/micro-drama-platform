---
worker_id: researcher-w6-daily-blacklist
stage: 0
role: researcher
angle: daily-blacklist
status: complete
blockers:
  - "官方中文译名（旅店名 / 分区名 / 道具名）未能从一手中文源逐字核实：warcraft.huijiwiki.com（灰机 wiki，国服译名对齐站）对本次抓取全部返回 HTTP 403，只拿到搜索摘要。所有中文译名在本文标为 ai_draft + ⚠️，须人眼在国服客户端 / 灰机 wiki 核一遍再进 prompt。"
  - "Wowhead Classic（wowhead.com/classic/）的 NPC / item 页为 JS 渲染，WebFetch 只能拿到页壳，拿不到 vendor 表。本文的 vendor 售货清单全部来自 warcraft.wiki.gg 的 Sells 表，而该表是 **retail（现行版本）** 清单；哪几档属于 Vanilla 由道具的等级门槛 + 改名 patch history 反推，已逐条标注，但**「Vanilla 精确售货清单」本身未经一手客户端核对**。"
  - "『城内能不能骑马』未查实：warcraft.wiki.gg 的 Mount 页只写了 no-fly zone，没有写地面坐骑的室内 / 城内限制；Vanilla 时期的城内骑乘规则本次没找到带引用的出处。标 ⚠️ + 未查。"
  - "旅店 / 民居**内部形制**（床铺、被褥、桌椅、餐具材质、有无私人房间）在所有查到的文字源里都没有正面记载，wiki 只挂图不写字。本文凡涉内部形制的都标 ⚠️，须人眼看游戏内截图 / 模型再定，不得当 ✅ 用。"
confidence: medium
---

# W6 · 暴风城 食 · 住 · 行 · 日常 + 玩家误传黑名单（sk2 · Vanilla 锚点）

> 本文件是 sk2 `0_research/dossier.md` 「食 / 住 / 行 / 误传」四节的**补充底稿**，由 parent 合并；dossier 各节只写指针，不复制 YAML。
> 用途：外来旅行者在暴风城逛一天——吃两三顿、住一晚旅店、次晨打分、看人怎么活动；并建**全站负向词库**。
> **版本锚点 = Vanilla（WoW 1.x / Classic，大地的裂变之前）**。凡本文标 `❌` 的，一律是 Vanilla **没有**、属于后续资料片或跨 IP 污染的东西，**只能进「我以为·踩坑」栏目，不得进正片画面**。
>
> `verified_by` 口径：
> - `ai_read` ＝ 本 worker 本次用 WebFetch **实际打开了该页面**并从返回正文中取到 quote；
> - `ai_draft` ＝ 只拿到 WebSearch 摘要、没打开原页（或原页 403 / JS 渲染取不到），**不得直接进 prompt**，须人眼升 `human`。
>
> tier 映射（虚构世界）：`T0` 游戏本体 / 暴雪官方设定书 / 官网；`T1` warcraft.wiki.gg、wowpedia、Wowhead Classic 条目；`T2` 有出处的考据长文；`T3` 无引用的百科 / 论坛 / 同人游记；`T4` 玩家推测 / 模型默认（只作反例）。
>
> **统计见文末 §6。**

**判断（总纲）**：暴风城的「吃住行」有两层证据，必须分开用。
① **机制层**（谁卖什么、多少钱、旅店怎么住、怎么从 A 到 B）——`warcraft.wiki.gg` 的 NPC 页 + 暴雪官网 Classic 指南写得很死，可以直接口播，但**售货清单是 retail 口径**，得靠道具的等级门槛与改名 patch history 把 Vanilla 那一档切出来（本文逐条做了）。
② **形制层**（旅店里长什么样、床是什么床、杯子什么材质、一日几餐）——**几乎全是空白**：wiki 挂了内景图但一个字的文字描述都没有。所以本文凡涉「长什么样」的，要么标 ⚠️（按世界逻辑推），要么记「未查」，**绝不伪造成 ✅**。这是本路最大的诚实边界。
③ 而**第三层——「哪些东西不该出现」——反而是证据最硬的一层**：暴雪的 patch history 精确到日期，说得清「港口是 2008 年 10 月 14 日加的」「公园是 2010 年 11 月 23 日炸的」。所以本路最可交付的产物是 §5 的**误传黑名单**，它下游直接变成全站负向词库。

---

## §1 食（`stormwind.food.NNN`）

### 1.1 沿街叫卖：面包小贩

```yaml
- fact_id: stormwind.food.001
  claim: 暴风城贸易区有一个沿街走动叫卖的流动面包小贩 Thomas Miller，头衔是 <Baker>（面包师），一边在区里走一边吆喝
  tag: ✅
  source: Warcraft Wiki - Thomas Miller
  source_url: https://warcraft.wiki.gg/wiki/Thomas_Miller
  quote: "Thomas Miller is a human bread vendor located in the Trade District in Stormwind City. He can be found walking around the district advertising his wares."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一名中年男面包贩挎着扁筐沿街慢走，筐里码着圆面包与长面包卷，边走边冲路人吆喝，行人往来不断"
  negative: "固定摊位、玻璃柜台、收银机、纸袋包装、印刷价签、现代面包房招牌"
  note: 他的吆喝原文四句（下条 food.002 引），可直接做背景人声。

- fact_id: stormwind.food.002
  claim: 面包小贩的叫卖词有四句原文可用——「Freshly baked bread for sale!」「Fresh bread for sale!」「Rolls, buns and bread. Baked fresh!」「Warm, wholesome bread!」；对话时会说「Best deals in all of Stormwind my friend, won't find any better.」
  tag: ✅
  source: Warcraft Wiki - Thomas Miller（Quotes / Gossip 段）
  source_url: https://warcraft.wiki.gg/wiki/Thomas_Miller
  quote: "\"Freshly baked bread for sale!\" / \"Fresh bread for sale!\" / \"Rolls, buns and bread. Baked fresh!\" / \"Warm, wholesome bread!\" ... Gossip: \"Best deals in all of Stormwind my friend, won't find any better.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "小贩张口吆喝，嘴型明显，周围两三个路人侧头看过来"
  negative: "扩音喇叭、广播、字幕条、店员统一话术"
  note: 「rolls, buns and bread」三个词直接给画面定了**面包形制**：小圆餐包 + 发面圆包 + 整条面包，三样同筐。这是本文里少数能反推形制的硬证据。

- fact_id: stormwind.food.003
  claim: 面包按价格分档，Vanilla 能买到的是最低六档——Tough Hunk of Bread 25 铜 / Freshly Baked Bread 1 银 25 铜 / Moist Cornbread 5 银 / Mulgore Spice Bread 10 银 / Soft Banana Bread 20 银 / Homemade Cherry Pie 40 银
  tag: ⚠️
  source: Warcraft Wiki - Thomas Miller（Sells 表）
  source_url: https://warcraft.wiki.gg/wiki/Thomas_Miller
  quote: "Tough Hunk of Bread (5x) 25c | Freshly Baked Bread (5x) 1s 25c | Moist Cornbread (5x) 5s | Mulgore Spice Bread (5x) 10s | Soft Banana Bread (5x) 20s | Homemade Cherry Pie (5x) 40s | Mag'har Grainbread (5x) 56s | Crusty Flatbread (5x) 85s ..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "筐里三种面包：粗硬的深色硬面包块、新烤的浅金圆面包、玉米面的黄色方包；旁边一只浅木盘里摆着一块自制樱桃派"
  negative: "法棍、可颂、吐司切片、蛋糕胚、奶油裱花、塑料包装"
  note: **标 ⚠️ 不是 ✅**——这张表是 retail 清单。切 Vanilla 那一档的依据：`Mag'har Grainbread`（56 银档）的名字里带 `Mag'har`（玛格汉兽人，TBC 2007 才出现），故 56 银及以上都是 Vanilla 之后加的。**Vanilla 的面包价格带 ＝ 25 铜 ～ 40 银**，本剧口播只能引这六档。精确 Vanilla 清单未经一手客户端核对（见 blockers）。**价钱本身归 W4，本文只用它做「档位」**。

- fact_id: stormwind.food.004
  claim: Freshly Baked Bread 需要 3 级才能吃，效果是「21 秒内恢复 234 点生命，进食过程中必须保持坐姿」
  tag: ✅
  source: Warcraft Wiki - Freshly Baked Bread
  source_url: https://warcraft.wiki.gg/wiki/Freshly_Baked_Bread
  quote: "Requires Level 3 ... Restores 234 health over 21 sec. Must remain seated while eating."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "她在长凳上坐下来才动口吃面包，双手捧着，背靠墙，吃得很慢"
  negative: "站着吃、边走边吃、单手举着啃、快走中咬一口"
  note: **本条是本路最重要的一条画面铁律**。「Must remain seated while eating」是暴雪写死在每一件食物道具上的机制文字——**在这个世界里，吃东西＝坐下来吃**。所以旅行者的三顿全部是坐着的镜头，任何「边走边啃」的分镜都是版本错（见 myth.017）。同一句话在 Shiny Red Apple、Dwarven Mild 上逐字复现，见 food.007 / food.006。
```

### 1.2 奶酪：贸易区有专卖店

```yaml
- fact_id: stormwind.food.005
  claim: 贸易区有一家奶酪专卖店 Trias' Cheese（坐标 66, 74），由 Trias 一家三口经营——Elling Trias「奶酪大师」、Elaine Trias「奶酪女主人」、Ben Trias「奶酪学徒」
  tag: ✅
  source: Warcraft Wiki - Trias' Cheese
  source_url: https://warcraft.wiki.gg/wiki/Trias%27_Cheese
  quote: "a cheese shop located in the Trade District of Stormwind City ... Elling Trias (Master of Cheese) / Elaine Trias (Mistress of Cheese) / Ben Trias (Apprentice of Cheese)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一间小奶酪铺，店里一对中年夫妇带一个少年学徒，架上摞着大小不一的整轮奶酪与切开的楔块"
  negative: "冷藏柜、保鲜膜、真空包装、连锁店 logo、白大褂"
  note: 「一家三口 + 学徒」是很好的生活感镜头素材。**Elling Trias 在正史里还是 SI:7 的暗桩**（同页有一句他调侃死亡之翼的台词，但那句提到 Deathwing 仍活着，属 Cataclysm 之后的文本，**本剧不能用**）。

- fact_id: stormwind.food.006
  claim: Dwarven Mild（矮人淡味奶酪）需 7 级、售价 5 银，效果「24 秒内恢复 530 点生命，进食过程中必须保持坐姿」；售它的 NPC 遍布艾尔文森林、暴风城、丹莫罗等地的旅店老板、酒保与食物商人
  tag: ✅
  source: Warcraft Wiki - Dwarven Mild
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_Mild
  quote: "Requires Level 7 ... Restores 530 health over 24 sec. Must remain seated while eating. ... sold by 25+ NPCs ... including innkeepers, bartenders, and food merchants in zones like Elwynn Forest, Stormwind City, Dun Morogh"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一小块淡黄色硬质奶酪，切面平整，摆在木盘上，旁边是半块面包"
  negative: "软质涂抹奶酪、奶酪片、独立小包装、芝士拉丝"
  note: 名字本身是画面依据——「Dwarven」＝矮人产，说明暴风城的奶酪走贸易进来，与矮人区互证（travel.005 深铁矿道直通铁炉堡）。

- fact_id: stormwind.food.007
  claim: Shiny Red Apple（鲜红苹果）25 铜，效果「18 秒内恢复 58 点生命，进食过程中必须保持坐姿」，由水果商、旅店老板等 24 个 NPC 出售
  tag: ✅
  source: Warcraft Wiki - Shiny Red Apple
  source_url: https://warcraft.wiki.gg/wiki/Shiny_Red_Apple
  quote: "Restores 58 health over 18 sec. Must remain seated while eating. ... Available from 24 different merchants ... including fruit sellers, innkeepers, and quartermasters"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一颗表皮发亮的红苹果，握在手里，另一只手扶着膝"
  negative: "打蜡超市苹果、条码贴纸、果盘摆拍、切片装盘"
  note: 最低档的即食水果，适合做「路上随手买一个、找地方坐下啃」的小段落。
```

### 1.3 饮品：谁卖、卖什么

```yaml
- fact_id: stormwind.food.008
  claim: 旧城区猪和哨声酒馆的酒保 Reese Langston（头衔 Tavernkeeper）是饮料商人，招呼语是「欢迎来到猪和哨声！来一杯，拉张凳子坐下，人越多越热闹！」
  tag: ✅
  source: Warcraft Wiki - Reese Langston
  source_url: https://warcraft.wiki.gg/wiki/Reese_Langston
  quote: "Reese Langston ... Pig and Whistle Tavern, Old Town, Stormwind City [76.9, 52.9] ... \"Welcome to the Pig and Whistle! Grab a drink my friend and pull up a seat, the more the merrier!\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "酒馆吧台后一名男酒保，正把一只酒杯推向台面，抬眼招呼进门的客人"
  negative: "调酒摇壶、鸡尾酒、霓虹酒柜、菜单立牌、POS 机"
  note: **「pull up a seat」再一次印证 food.004 的坐下机制**——这家店的官方招呼语本身就在叫人坐下。

- fact_id: stormwind.food.009
  claim: 酒保卖的**非酒精饮料**按价格分档，Vanilla 段是最低六档——Refreshing Spring Water 5 铜 / Ice Cold Milk 1 银 25 铜 / Melon Juice 5 银 / Sweet Nectar 10 银 / Moonberry Juice 20 银 / Morning Glory Dew 40 银
  tag: ⚠️
  source: Warcraft Wiki - Reese Langston（Sells 表）
  source_url: https://warcraft.wiki.gg/wiki/Reese_Langston
  quote: "Refreshing Spring Water (5x) - 5c / Ice Cold Milk (5x) - 1s 25c / Melon Juice (5x) - 5s / Sweet Nectar (5x) - 10s / Moonberry Juice (5x) - 20s / Morning Glory Dew (5x) - 40s / Filtered Draenic Water (5x) - 56s ..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "台面上并排三样：一只盛清水的杯、一杯乳白的奶、一杯淡色果汁"
  negative: "玻璃高脚杯、吸管、冰块方块、瓶装饮料、易拉罐、汽水气泡"
  note: 切 Vanilla 那一档的依据：56 银档的 `Filtered Draenic Water`（德莱尼／外域，TBC 2007）之后全是 Vanilla 之后的。**Vanilla 饮料带 ＝ 5 铜 ～ 40 银，共六档，且全是水／奶／果汁／花蜜，没有茶、没有咖啡、没有汽水。**「牛奶」明确存在（Ice Cold Milk），可以放心给画面。

- fact_id: stormwind.food.010
  claim: 酒保另卖**酒精饮料**，Vanilla 段是最低五档——Bottle of Pinot Noir 50 铜 / Skin of Dwarven Stout 1 银 20 铜 / Flask of Port 1 银 50 铜 / Flagon of Mead 15 银 / Jug of Badlands Bourbon 20 银（前三条的现名分别是 Dalaran Noir / 不变 / Stormwind Tawny，见 food.011–013）
  tag: ⚠️
  source: Warcraft Wiki - Reese Langston（Sells 表 · Alcohol 段）
  source_url: https://warcraft.wiki.gg/wiki/Reese_Langston
  quote: "Bottle of Dalaran Noir - 50c / Skin of Dwarven Stout - 1s 20c / Flask of Stormwind Tawny - 1s 50c / Flagon of Dwarven Mead - 15s / Jug of Badlands Bourbon - 20s / Lagrave Stout - 2g 24s ..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "吧台上：一只带塞的深色玻璃酒瓶、一只鼓鼓的皮酒囊、一只带盖的大锡酒壶"
  negative: "啤酒扎啤玻璃杯、品牌酒标、酒精度数标签、冰桶、开瓶器"
  note: 五个容器词直接给了形制——`Bottle`（瓶）/ `Skin`（皮囊）/ `Flask`（扁壶）/ `Flagon`（带盖大酒壶）/ `Jug`（罐）。**这五种容器同台，就是这家酒馆吧台的正确陈设**。注意 `Skin of Dwarven Stout` 是**皮囊装的矮人烈啤**，不是玻璃杯。⚠️ 的原因同 food.009：这是 retail 清单，Vanilla 的精确档位未经客户端核对；且 `Jug of Badlands Bourbon` 是否也被 5.3.0 改过名**未查**。

- fact_id: stormwind.food.011
  claim: 现名 Flask of Stormwind Tawny 的酒，**Vanilla 时叫 Flask of Port**，2013-05-21 的 5.3.0 补丁才改名；道具说明是「一种普通的酒精饮料」，售价 1 银 50 铜，「全艾泽拉斯的酒保都在卖」
  tag: ✅
  source: Warcraft Wiki - Flask of Stormwind Tawny（Patch history）
  source_url: https://warcraft.wiki.gg/wiki/Flask_of_Stormwind_Tawny
  quote: "\"Use: A typical alcoholic beverage.\" ... \"Flasks of Stormwind Tawny can be purchased for 1 silver 50 copper from bartenders throughout Azeroth.\" ... Originally named \"Flask of Port\" before being renamed in Patch 5.3.0"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一只细颈扁酒壶，壶身深色，塞着软木塞"
  negative: "现代玻璃酒瓶、品牌标签、瓶盖螺纹、酒庄封条"
  note: **口播必须用 Vanilla 名**。如果口播说「暴风城茶色酒」就穿帮了——那是 2013 年才有的名字。

- fact_id: stormwind.food.012
  claim: 现名 Flagon of Dwarven Mead 的蜂蜜酒，原名就是 Flagon of Mead，5.3.0（2013-05-21）改名；而**在 Classic 客户端里它叫 Flagon of Dwarven Honeymead**；道具说明「一种烈性酒精饮料」，售价 15 银
  tag: ✅
  source: Warcraft Wiki - Flagon of Dwarven Mead（Patch history / Trivia）
  source_url: https://warcraft.wiki.gg/wiki/Flagon_of_Dwarven_Mead
  quote: "\"A strong alcoholic beverage\" ... \"Renamed from Flagon of Mead\" in Patch 5.3.0 (May 21, 2013). Additionally, there's a trivia note explaining that in Classic, the item is named \"Flagon of Dwarven Honeymead,\" while the original vanilla version was simply called \"Flagon of Mead.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一只带盖的大肚酒壶，金属质地，壶身有捶打纹"
  negative: "玻璃啤酒杯、扎啤桶、拉环、现代酒标"
  note: **这条有个坑**：「Vanilla 原名」与「Classic 客户端名」**不是同一个**——2004 年原版叫 `Flagon of Mead`，2019 年 Classic 重制时客户端里写的是 `Flagon of Dwarven Honeymead`。本剧的版本锚点是 Vanilla，口播用哪个都能自圆其说，但**要选定一个别混用**；建议用 Classic 客户端名（观众今天能自己进游戏对上）。

- fact_id: stormwind.food.013
  claim: 现名 Bottle of Dalaran Noir 的红酒，原名 Bottle of Pinot Noir，同样在 5.3.0（2013-05-21）改名；说明是「一种较弱的酒精饮料」，售价 50 铜
  tag: ✅
  source: Warcraft Wiki - Bottle of Dalaran Noir（Patch history）
  source_url: https://warcraft.wiki.gg/wiki/Bottle_of_Dalaran_Noir
  quote: "\"A fairly weak alcoholic beverage.\" ... 50 copper ... In Patch 5.3.0 (May 21, 2013) ... \"Renamed from Bottle of Pinot Noir.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一只深色细颈葡萄酒瓶，瓶身无标签，只有软木塞"
  negative: "现代酒标、年份标、酒庄印章、醒酒器、高脚杯"
  note: 最便宜的酒（50 铜，比一杯牛奶还便宜一半），适合做「旅行者点了最便宜那杯」的细节。
```

### 1.4 有厨师的地方：法师区的餐馆

```yaml
- fact_id: stormwind.food.014
  claim: 法师区的 The Blue Recluse **既是酒馆也是餐馆**，在受过魔法训练的人里很受欢迎，以「看上去很上档次的氛围」闻名全世界；有主厨 Angus Stern、学徒厨师 Connor Rivers、酒保 Joachim Brenlow；其中一份菜单满是带「bayou（河汊沼泽）」风味的乡土菜
  tag: ✅
  source: Warcraft Wiki - The Blue Recluse
  source_url: https://warcraft.wiki.gg/wiki/The_Blue_Recluse
  quote: "The Blue Recluse is a tavern and restaurant in the Mage Quarter of Stormwind City. ... It is popular among the magically inclined. ... renowned around the world for its apparent classy atmosphere. ... One of its menus is filled with rural dishes with a common 'bayou' theme. ... known for its food, drinks, and good conversations."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一间有真正后厨的酒馆，主厨在灶前，学徒在旁打下手，堂里客人围桌交谈，气氛比街边酒馆体面"
  negative: "明档厨房不锈钢、开放式吧台餐厅、米其林摆盘、服务生制服、菜单立牌"
  note: **这是全城唯一有「主厨 + 学徒厨师」明文记载的地方**，也是唯一被官方称作 `restaurant` 的店。旅行者的「正经一顿」该放这儿，不该放猪和哨声。⚠️ 注意：同页把 Steven Lohan 写成 innkeeper，**那是 retail 头衔**，Vanilla 的头衔未查证，口播别说「旅店老板」。

- fact_id: stormwind.food.015
  claim: 旧城区猪和哨声酒馆里有烹饪训练师 Stephen Ryback（以自家配方的一整排烤肋排闻名）和烹饪材料商 Erika Tate
  tag: ⚠️
  source: Wowpedia / Warcraft Wiki - Stephen Ryback、Erika Tate（仅搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Stephen_Ryback
  quote: "Stephen Ryback is a human cooking trainer located in the Pig and Whistle Tavern in the Old Town of Stormwind City. He is apparently well known for the rack of ribs he serves up from a personal recipe."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "酒馆一角的炉灶边，一名壮实的男厨守着火，铁架上一整排烤得焦亮的肋排在滴油"
  negative: "烤箱、燃气灶、温度计、厨师帽、不锈钢烤盘"
  note: **「rack of ribs」是本文查到的唯一一道有名有姓的暴风城熟食**——整排烤肋排。旅行者的「肉那一顿」就该是这个，不用编。⚠️ 因为只拿到搜索摘要没打开原页。两位 NPC 是电影《潜龙轰天》的梗（Casey Ryback / Jordan Tate），**口播别提梗**，会出戏。

- fact_id: stormwind.food.016
  claim: 「一日几餐」「餐制」在暴风城没有任何设定层面的记载——游戏机制层面只有「坐下吃东西回血」，没有早中晚餐的概念
  tag: ⚠️
  source: 本次检索未在 T0–T2 任一来源中找到餐制记载
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "（未查到——Stormwind City 条目通篇无餐制 / 用餐时间相关段落）"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（不入画——本条是「不要画什么」的依据）"
  negative: "早餐/午餐/晚餐字幕标注、餐钟、开饭铃、排队打饭、固定用餐时段的人群"
  note: **这是一个必须诚实处理的空白**。本片「吃两三顿」是**旅行者自己的节奏**，不是暴风城的制度。所以不要拍成「全城到点开饭」，要拍成「她饿了就找地方坐下吃」。这反而更贴 food.004 的机制真相。
```

---

## §2 住（`stormwind.house.NNN`）

### 2.1 Vanilla 的暴风城只有一家真旅店

```yaml
- fact_id: stormwind.house.001
  claim: The Gilded Rose 是**贸易区的那家旅店**，因为紧挨银行、拍卖行和一个人人都在用的邮箱，成了路过暴风城的旅人最常歇脚的地方；老板娘 Innkeeper Allison 既是东道主，也卖食物与饮料
  tag: ✅
  source: Warcraft Wiki - Gilded Rose
  source_url: https://warcraft.wiki.gg/wiki/Gilded_Rose
  quote: "The Gilded Rose is the inn located in the Trade District. ... It is a popular resting point for travelers passing through the human capital of Stormwind City due to its proximity to the bank, Auction House, and an ever-popular mailbox. ... Innkeeper Allison is the host and offers a Hearthstone point as well as being a vendor of food and drink."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区街面上一间二层旅店门脸，左右紧邻列柱石砌的银行与拍卖行，门口人来人往，进门就是堂屋"
  negative: "酒店前台、行李寄存、房号牌、电梯、玻璃旋转门、霓虹招牌"
  note: **原文用的是定冠词 `the inn`，不是 `an inn`**——这句本身就是「暴风城只有这一家旅店」的语法证据，和 house.003 互证。

- fact_id: stormwind.house.002
  claim: 旅店老板娘 Innkeeper Allison 就在一楼门内，招呼语是「欢迎光临我的旅店，疲惫的旅人。有什么可以为你效劳的？」
  tag: ✅
  source: Warcraft Wiki - Innkeeper Allison
  source_url: https://warcraft.wiki.gg/wiki/Innkeeper_Allison
  quote: "Gilded Rose Inn, Stormwind City [60.6, 75.0] ... Quote: \"Welcome to my Inn, weary traveler. What can I do for you?\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一名中年女店主站在堂屋一侧，围裙，双手交叠，朝进门的旅人点头招呼"
  negative: "前台柜台、登记簿、房卡、制服、工牌、迎宾站姿"
  note: **「weary traveler」这句招呼语几乎是为本片写的**——外来旅行者推门进来，她这么招呼，一句话立住「这是给赶路人歇脚的地方」。可直接口播。

- fact_id: stormwind.house.003
  claim: **Vanilla 时期猪和哨声不是旅店、是酒馆**——它的旅店老板 Innkeeper Maegan Tillman 是 2010-10-12 的 4.0.1 补丁才加进来的，「使猪和哨声成为暴风城的第二家旅店」
  tag: ✅
  source: Warcraft Wiki - Pig and Whistle Tavern（Patch changes）
  source_url: https://warcraft.wiki.gg/wiki/Pig_and_Whistle_Tavern
  quote: "Patch 4.0.1 (2010-10-12): Innkeeper Maegan Tillman was added, making the Pig and Whistle Stormwind's second inn."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（酒馆内只有吧台、酒桶、桌凳与炉火，看不到上楼住宿的动线）"
  negative: "猪和哨声里出现旅店老板、炉石绑定、客房楼梯、住宿登记"
  note: **这是本节最容易翻车的一条，也是最漂亮的一条**。「第二家旅店」这个说法反过来钉死了：**在 4.0.1 之前，暴风城的旅店数量 ＝ 1**。所以旅行者只能住镀金玫瑰。她可以去猪和哨声**喝一杯**，但不能在那儿**住**。见 myth.018。

- fact_id: stormwind.house.004
  claim: 猪和哨声酒馆在旧城区，由 Langston 一家在经营——Reese Langston 是 Tavernkeeper（酒馆主），Elly Langston 是 Barmaid（女招待）兼饮料商人，另有 David Langston
  tag: ✅
  source: Warcraft Wiki - Pig and Whistle Tavern（NPCs 段）
  source_url: https://warcraft.wiki.gg/wiki/Pig_and_Whistle_Tavern
  quote: "Located in the district known as Old Town ... \"Reese Langston\" works as the Tavernkeeper. ... \"Elly Langston\" as a barmaid ... Other patrons and staff include Bartleby (a drunk), Harry Burlguard, David Langston ..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "酒馆堂内：吧台后一名男酒保，一名女招待端着杯子在桌间走动，角落一个明显喝多了的男人趴在桌上"
  negative: "服务生制服、托盘防滑垫、点单本、叫号器"
  note: **`Bartleby (a drunk)` 是有名有姓的醉汉常客**——酒馆里「有一个人已经喝趴下」是官方写死的陈设，不是我们编的氛围。这种细节最能让画面活。

- fact_id: stormwind.house.005
  claim: 住旅店**不花钱**——旅店老板的服务是免费的：跟他说「把这家旅店设为我的家」就能绑定炉石；炉石丢了，旅店老板会免费再给一个
  tag: ⚠️
  source: Warcraft Wiki - Innkeeper；Wowpedia - Innkeeper（服务描述）
  source_url: https://warcraft.wiki.gg/wiki/Innkeeper
  quote: "To set or change the bind point for your hearthstone, talk to an innkeeper and click Make this inn your home. ... Most innkeepers are also either general goods vendors or food and drink vendors, though some innkeepers do not sell anything at all."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旅行者跟店主说了几句，店主点头，她就上楼了——没有掏钱、没有登记的动作"
  negative: "付房钱、数铜板、押金、账本记名、房牌钥匙、结账"
  note: **标 ⚠️ 不是 ✅，理由要说清**：wiki 的 Innkeeper 页**通篇没有任何收费条目**（没写住宿费、没写房价），且炉石补发明确免费。「没写收费」是**沉默证据**，不是正面记载。但这个沉默很强——如果收费，一定会像飞行点那样写出来（travel.003 的官方原文就明写了 "you'll need to pay for travel"）。**所以「暴风城住店不要钱」这件事本身就是本片一条可口播的反差点**（次晨打分那段的现成素材），但口播要说成「我没花一个铜板」而不是「官方规定免费」。

- fact_id: stormwind.house.006
  claim: 旅店与民居的**内部形制**（床铺样式、被褥、是通铺还是私人房间、桌椅、餐具材质、照明是蜡烛还是油灯还是壁炉）在查到的全部文字源里**都没有正面记载**——wiki 只挂内景照片、正文一个字不写
  tag: ⚠️
  source: Warcraft Wiki - Gilded Rose / Pig and Whistle Tavern / The Blue Recluse（三页均如此）
  source_url: https://warcraft.wiki.gg/wiki/Gilded_Rose
  quote: "The page includes an image labeled \"The tavern's interior\" but provides no descriptive text about its interior design."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（不可直接入画——必须先人眼看游戏内截图定形制）"
  negative: "（待定——形制未定之前不出负向词，以免锁错方向）"
  note: **本条是本路最大的诚实边界，务必带进 dossier**。三家店的 wiki 页一律「有图无字」。**下一步的正确做法是人眼看游戏内截图 / 模型**（或让用户在 Classic 客户端里截几张），不是让模型自由发挥，也不是让 Claude 按「中世纪旅店」的通用印象补——那正好会掉进 myth.007「画成地球中世纪」的坑。唯一能从文字反推的只有 food.010 的容器词（瓶/皮囊/扁壶/大酒壶/罐）。

- fact_id: stormwind.house.007
  claim: 暴风要塞的屋顶铺的是**蓝色板岩**，建筑群有许多附属楼、塔楼与厅堂
  tag: ✅
  source: Warcraft Wiki - Stormwind Keep
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "Its roof was shod with blue slate and the complex had many side buildings, towers, and halls."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "白石墙体配蓝色板岩坡屋顶，主楼旁生出多座塔楼与偏厅"
  negative: "红瓦、灰瓦、茅草顶、金顶、铜绿屋顶、平屋顶"
  note: **「蓝屋顶」终于有了一句正面文字出处**（此前只有官网导览的「The distinctive blue roofs reveal that this is the trade district」这种口语表述）。这是暴风城最不能丢的识别特征之一，见 myth.006 / myth.007。

- fact_id: stormwind.house.008
  claim: 旧城区是全城最旧的一块，「破败而乡土，街道被形容为比其他区脏得多也臭得多」；它早于城市被兽人夷平后的重建，「从来不需要真正重建」，因此之后得到的维护也少；它也是城里大多数穷人的居住区——「乞丐、小偷和穷人都在那儿」
  tag: ✅
  source: Warcraft Wiki - Old Town
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "a rustic, downtrodden place, where the streets are described as far dirtier and smellier than the other districts ... predate[s] the reconstruction of the city after its razing by the orcs ... never needed true rebuilding ... It is also the residential area for most of the poor folk of the city, as \"beggars, thieves, and poor people can be found there.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "窄而脏的街巷，墙面斑驳，地面泥水，墙根坐着衣衫破旧的人，与贸易区的整洁形成直接反差"
  negative: "和贸易区一样光鲜的立面、新铺的石板、整齐的商铺、干净的白墙"
  note: **「比别处更脏更臭」是官方写死的**，所以旧城区必须和贸易区拉出可见的画面落差。旅行者从贸易区走到旧城区，应该是「一眼看出换了地方」的。旧城区屋顶颜色见 house.009。

- fact_id: stormwind.house.009
  claim: 旧城区的识别色是**暗红 / 紫红色屋顶**，与贸易区的蓝屋顶相对
  tag: ⚠️
  source: 暴雪官网《Welcome to Stormwind: A Guided Tour》相关表述（仅搜索摘要转述）
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/20142731/welcome-to-stormwind-a-guided-tour
  quote: "The city features various districts, including Old Town, defined by its maroon coloured roofs, which is the oldest part of stormwind city."
  tier: T0
  verified_by: ai_draft
  used_in: []
  prompt_string: "旧城区屋顶是暗红褐色的，远处贸易区的屋顶是蓝色，两片颜色在同一画面里分界明显"
  negative: "旧城区画成蓝屋顶、全城同色屋顶、屋顶颜色随机"
  note: ⚠️ 标 `ai_draft`——这句是从搜索摘要转述的，本次 WebFetch 打开官网导览页时返回的正文里**没有**这句（拿到的是别的段落）。**须人眼回原页核实**。但「屋顶颜色分区」这条本身与 house.007（要塞蓝板岩）+ 官网导览「The distinctive blue roofs reveal that this is the trade district」一致，可信度不低。

- fact_id: stormwind.house.010
  claim: 法师区有两家酒馆——The Slaughtered Lamb 是一家「下三滥的小酒馆」，酒保 Jarel Moor，楼上空荡荡只有他一个人，他会劝客人「离阴影远点」；酒馆的地下墓穴是暴风城术士的密所
  tag: ✅
  source: Warcraft Wiki - The Slaughtered Lamb
  source_url: https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb
  quote: "The Slaughtered Lamb is a seedy pub in the Mage Quarter of Stormwind City. ... \"The top floor is empty except for the bartender Jarel Moor, who advises patrons to 'stay away from the shadows'.\" ... \"The tavern's catacombs serve as the sanctum of the warlocks of Stormwind.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一间空荡阴冷的小酒馆，只有一个酒保守着吧台，光线暗，角落黑得看不清，地上有通往地下的口"
  negative: "热闹满座、暖光、歌舞、明亮吊灯"
  note: 和镀金玫瑰（体面）、猪和哨声（军伍气+醉汉）、蓝色隐士（上档次+主厨）凑成**四种完全不同的喝酒场所气质**，够拍一整段「这城里四家店各是什么味道」。

- fact_id: stormwind.house.011
  claim: 银行是 Stormwind Counting House（暴风城银库），在贸易区西南角、拍卖行对面、面朝喷泉，是一栋带罗马式列柱和石台阶的建筑；银行与邮箱都在贸易区西南侧
  tag: ⚠️
  source: Wowpedia / Warcraft Wiki - Stormwind Counting House（搜索摘要）+ Warcraft Wiki - Trade District（本次实读）
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The [bank]... [and] [mailbox]... are on the southwest side of the Trade District."（Trade District 页，ai_read）；\"The Stormwind Counting House is a building with Roman-style columns and stone steps and is located in the southwest corner of the Trade District, opposite the Auction House, facing the fountain.\"（Counting House 页，ai_draft）
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "一栋列柱石砌的银库建筑，正面一排石台阶，门前是一座石砌喷泉"
  negative: "玻璃幕墙、ATM、保安亭、金属卷帘门、银行 logo"
  note: 混合条目：「银行与邮箱在贸易区西南侧」是 ai_read；「列柱 + 石阶 + 正对喷泉」是 ai_draft。**贸易区有喷泉**这件事由这条侧面确认（拍摄地标）。**布局细节归 W11，本文只取「旅行者会路过什么」这一层。**

- fact_id: stormwind.house.012
  claim: 教堂广场有孤儿院和 City Hall（市政厅）；市政厅是暴风城的建筑师与研究者给王国居民做人口普查、以及琢磨怎么改善城里人生活的地方；孤儿院在光明大教堂东南，收容近年各场战争的人类孤儿，由 John Turner 夫妇名义主持、实际由 Orphan Matron Nightingale 与 Shellene 照看
  tag: ⚠️
  source: Warcraft Wiki - Cathedral Square（实读）+ Wowpedia - City Hall / Orphanage（搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_Square
  quote: "The square contains: Orphanage and City Hall (civic centers)"（实读）；\"City Hall is where Stormwind's architects and researchers keep a census on the citizens of the kingdom, as well as finding ways to improve the quality of life for those within the city.\"（摘要）
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "教堂广场一侧的市政厅门前，几个人在石阶上交谈；不远处孤儿院门口有孩子在玩"
  negative: "现代政府大楼、国旗杆、玻璃门、排队叫号、办事窗口"
  note: **「市政厅在做人口普查」是本片可用的绝妙口播点**——外来者第一天进城，谈「这城里的人是被数过的」比谈任何建筑都有生活质感。⚠️ 因 City Hall 页未实读。

- fact_id: stormwind.house.013
  claim: 矮人区的住宅是「为矮人使用而大幅改造的大房子，加了额外的楼层和房间」；该区人口稠密、是商业与工业中心，当地的工坊通宵开工供应全城货品
  tag: ⚠️
  source: Wowpedia / Warcraft Wiki - Dwarven District（RPG 出处，wiki 明标为非正史）
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "According to RPG lore (non-canon), \"dwarves reside in this district\" with \"large houses heavily modified for dwarf use.\" ... \"The Dwarven District is robust and heavily populated, usually with large houses heavily modified for dwarf use with additional floors and rooms. It is a center of commerce and industry, and the local factories work all night to supply Stormwind with all of its goods.\""
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "加盖过的多层大屋，门窗与楼梯的尺度明显是给矮个子改过的，夜里屋里还亮着火光"
  negative: "统一制式住宅、现代公寓、电灯、烟囱冒工业黑烟"
  note: ⚠️ **wiki 自己标了 non-canon（RPG 桌游设定，非游戏正史）**，所以只能当氛围参考、不能当硬设定口播。但「工坊通宵开工」对「夜里的城市还是亮的」这一画面很有用，和 travel.011 的夜间巡逻互证。

- fact_id: stormwind.house.014
  claim: 普通市民的家**里面**长什么样（家具、坐具、炉灶、床）在所有查到的来源里都没有记载
  tag: ⚠️
  source: 本次检索未在 T0–T2 任一来源中找到暴风城民居内部描述
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "（未查到——Stormwind City 及各分区条目均无民居内部陈设描述）"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（不入画——本条是「不要画什么」的依据）"
  negative: "（同 house.006，形制未定前不出负向词）"
  note: 与 house.006 同理。**如果本片要拍民居内景，必须先让用户在客户端里截图**，否则模型一定按「欧洲农舍」画，直接踩 myth.007。
```

---

## §3 行（`stormwind.travel.NNN`）

### 3.1 城内：走路为主

```yaml
- fact_id: stormwind.travel.001
  claim: 城里主要靠走——贸易区的街道「虽然宽，但挤到让人相当难以移动，至少在正午时分是这样」
  tag: ⚠️
  source: Travels through Azeroth and Outland: Stormwind City（同人游记，第一人称考察体）
  source_url: https://destron.blogspot.com/2007/10/stormwind-city.html
  quote: "The teeming Trade District sprawls to the north past the great walls. Though wide, the streets are so packed as to make movement quite difficult, at least during midday."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "正午的贸易区主街，人挤人，行进缓慢，肩擦肩，摊贩与行人混在一起"
  negative: "空旷街道、稀稀落落几个人、车辆、马车拥堵、红绿灯"
  note: ⚠️ **T3——同人游记，不是官方设定**。但「正午人最挤」这一条对拍摄节奏很有用（正午挤 / 清晨空），且与 food.001「小贩在人流里穿行叫卖」自洽。**当氛围参考用，不口播成事实。**

- fact_id: stormwind.travel.002
  claim: 城市由大致呈长方形的各个区组成，区与区之间以运河分隔
  tag: ✅
  source: Warcraft Wiki - Stormwind City
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The city is made up of roughly rectangular districts separated by canals."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一条石砌运河横在两片街区之间，石桥跨过水面，两岸都是店铺立面"
  negative: "护城河吊桥、天然河流、码头栈桥、游船、船闸"
  note: **「过桥＝换区」是本片最省事的转场语法**。旅行者每换一个区都过一次桥，观众自然读懂城市结构。**布局细节归 W11，本条只取转场用法。**

- fact_id: stormwind.travel.003
  claim: 运河沿岸两侧都有不少店铺，也可以在运河里钓鱼
  tag: ✅
  source: 暴雪官网《Welcome to Stormwind: A Guided Tour》
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/20142731/welcome-to-stormwind-a-guided-tour
  quote: "You'll find quite a few shops along either side of the the canals and if you feel like doing a bit of fishing, you can find that too."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "运河两岸一溜店铺，水边有人垂钓，钓竿斜伸向水面"
  negative: "商业步行街、遮阳伞、户外座椅区、栏杆护网、禁钓牌"
  note: T0 官方。「城里有人钓鱼」是很好的日常生活镜头，且证明运河的水是活的、干净到有鱼。

- fact_id: stormwind.travel.004
  claim: 法师区的地面质感与别处不同——「街道的鹅卵石让位给一片片厚草，点缀着毒蕈和纤细的花」；入夜后区里的实用店铺打烊、气氛转向消遣，「奥术灯柱彻夜发光」
  tag: ⚠️
  source: Travels through Azeroth and Outland: Stormwind City（同人游记）
  source_url: https://destron.blogspot.com/2007/10/stormwind-city.html
  quote: "The cobblestones of the streets give way to lines of thick grass dotted with toadstools and delicate flowers ... As the more utilitarian shops close down the area switches its focus to pleasure...arcane lampposts gleam through the night."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "法师区的地面从石板过渡成厚草地，草里长着蕈子和小花；入夜后路边灯柱亮起冷色的魔法光"
  negative: "电灯、路灯杆、灯泡、灯罩、明火火把当路灯、现代景观照明"
  note: ⚠️ T3 同人游记。但「奥术灯柱」这个意象对「夜里的暴风城」极其关键——**照明不是火把也不是电灯，是魔法光**。这一条若要口播，须人眼在客户端核实法师区夜景。同页还写矮人区「Smoke fills the streets, pouring out from the forges and smithies」（与 travel.008 官方版本互证）。
```

### 3.2 城际：狮鹫、电车，**没有船**

```yaml
- fact_id: stormwind.travel.005
  claim: 狮鹫栖木（Gryphon Roost）就在贸易区旁边、从东侧一条坡道上去，城里的狮鹫养在那儿；狮鹫管理员是 Dungar Longdrink
  tag: ✅
  source: Warcraft Wiki - Gryphon Roost；Warcraft Wiki - Trade District
  source_url: https://warcraft.wiki.gg/wiki/Gryphon_Roost
  quote: "located just off the Trade District ... houses the city's gryphons ... The [Gryphon Master] is up a ramp on the east side"（后半句出自 Trade District 页）
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区东侧一条石坡道通向高处的狮鹫栖木，木架上停着数头狮鹫，一名管理员在旁"
  negative: "机场跑道、候机厅、行李托运、检票口、停机坪"
  note: ⚠️ 同页还写了 Tannec Stonebeak（狮鹫贩子）与 Bralla Cloudwing（骑乘训练师）在此、狮鹫由「两个奇锐部落矮人」饲养——**这几位是否在 Vanilla 就存在未查证**，口播只提 Dungar Longdrink 最安全。

- fact_id: stormwind.travel.006
  claim: 坐狮鹫要付钱，而且必须先亲自到过那个飞行点、跟当地的飞行管理员说过话才能飞过去——光走进那片区域不算
  tag: ✅
  source: 暴雪官网《WoW Classic: Getting around Azeroth》
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/23156366
  quote: "you'll need to pay for travel when you use a flight path."（并：必须先 discover / learn 每条航线）
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "旅行者把几枚铜板递给狮鹫管理员，管理员点头，她才踩上鞍"
  negative: "刷卡、机票、二维码、免费随便飞"
  note: T0 官方，与 house.005「住店不花钱」形成**本片可用的直接反差**：飞行要钱，住店不要钱。这个反差是次晨打分那段的好材料。

- fact_id: stormwind.travel.007
  claim: 深铁矿道（Deeprun Tram）在暴风城的入口在**矮人区东侧的一条隧道**，通向铁炉堡的叮当镇；「深铁矿道在暴风城与铁炉堡两座主城之间提供快速往返——而且免费！」
  tag: ✅
  source: 暴雪官网《WoW Classic: Getting around Azeroth》；Warcraft Wiki - Dwarven District
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/23156366
  quote: "the Deeprun Tram provides quick transportation between the capital cities of Stormwind and Ironforge—for free!"（官网）；\"The Stormwind City end of the Deeprun Tram line is accessible through a tunnel on the east side of the district.\"（Dwarven District 页，ai_read）
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "矮人区东侧一条向下的隧道口，隧道尽头是地下的轨道与站台，车厢沿轨滑入"
  negative: "蒸汽火车、煤烟、汽笛、铁轨道砟、地铁闸机、售票窗口、电子屏"
  note: **它是地下电车（tram），不是蒸汽火车**——免费、地下、有轨。搜索摘要另称入口是「一圈巨大的旋转齿轮」环绕的隧道、单程约 2 分钟，但**这两点只在搜索摘要里，未实读原页**，口播别用。见 myth.020。

- fact_id: stormwind.travel.008
  claim: 矮人区由锻炉造出「一层常驻的烟霭」，伴着「不停歇的铁匠锤声」；区里有采矿、锻造、工程学训练师和对应的熔炉与铁砧
  tag: ✅
  source: Warcraft Wiki - Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "a constant haze ... the constant strokes of smiths' hammers ... Profession trainers for mining, blacksmithing, and engineering, and corresponding forges and anvils can also be found here."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街面上浮着一层散不掉的烟霭，锻炉口透出橙红火光，铁砧上锤声不断，火星四溅"
  negative: "工厂烟囱黑烟、蒸汽管道、机械臂、现代车间、护目镜"
  note: **「烟霭 + 锤声」是矮人区的双重签名**，一个给画面一个给声音。注意这是**锻炉的烟**不是工业黑烟，负向要挂死。

- fact_id: stormwind.travel.009
  claim: **Vanilla 的联盟船不从暴风城开**——Classic 只有：黑海岸出发的两条（去鲁瑟兰村 / 去米奈希尔港）、米奈希尔港去塞拉摩的一条，外加一条中立的藏宝海湾↔棘齿城
  tag: ✅
  source: 暴雪官网《WoW Classic: Getting around Azeroth》
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/23156366
  quote: "There is one neutral boat that is available for both Horde and Alliance which travels between Booty Bay in the Eastern Kingdoms and Ratchet in Kalimdor. ... Alliance-specific boats operate from Darkshore (to Rut'theran Village and Menethil Harbor) and from Menethil Harbor (to Theramore Isle)."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（暴风城画面里不出现任何码头、泊位、船桅、缆绳、货箱堆场）"
  negative: "暴风城港口、码头、栈桥、帆船、桅杆、水手、货箱、跳板、船锚、海鸥"
  note: **T0 官方，且是本片最硬的一条负向**。官方 Classic 指南把 Classic 的全部船班列了个遍，暴风城**一条都没有**。这一条与 myth.001 互为正反面，两条要一起进负向词库。

- fact_id: stormwind.travel.010
  claim: 40 级才拿得到坐骑，而且攒够训练技能与买坐骑的钱本身就是一桩苦差事
  tag: ✅
  source: 暴雪官网《WoW Classic: Getting around Azeroth》
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/23156366
  quote: "While can gain access to a mount at level 40, collecting enough gold to train the skill and purchase a mount can be an endeavor."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "（街上骑马的人是少数，绝大多数人在走路）"
  negative: "满街骑马、人人有坐骑、马匹拥堵"
  note: **这条决定了街景的人马比例**：坐骑在 Vanilla 是**奢侈品**，街上应该以步行为绝对主体，偶尔一两骑。

- fact_id: stormwind.travel.011
  claim: 人类的马不在城里买——骑乘训练师 Randal Hunter 与马贩 Katie Hunter 都在**艾尔文森林的东谷伐木场**的马厩，那里能学骑术、也能买普通和史诗人类坐骑；默认只有人类能跟 Katie 买，其他种族要跟暴风城崇拜；Katie Hunter 在 4.0.3a 被移除
  tag: ⚠️
  source: Wowpedia / Warcraft Wiki - Katie Hunter、Randal Hunter、Eastvale Logging Camp（搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Katie_Hunter
  quote: "Katie Hunter is a human horse breeder and horse vendor located in the Eastvale Logging Camp in Elwynn Forest. ... Randal Hunter is a human horse riding trainer located in the Eastvale Logging Camp ... Only humans can buy from Katie by default ... Katie Hunter was removed from World of Warcraft in patch 4.0.3a"
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（暴风城内不出现卖马的马厩与马贩摊位）"
  negative: "城内马市、马贩吆喝、拴马桩排排站、城内马厩"
  note: ⚠️ ai_draft。**但方向很确定：Vanilla 的马厩在城外森林里，不在城里。** 这意味着旅行者在城内看不到「买马」这件事。⚠️ 旧城区的 Command Center（军队司令部）据 Old Town 页记载带 "training grounds and stables"——**那是军马厩、不是马市**，别混。

- fact_id: stormwind.travel.012
  claim: 暴风城卫兵（Stormwind City Guard）是城里的执法者与守护者，「在城墙之内维持秩序」；他们「在地面和空中巡逻，或者守在都城的城门口，需要时协助和保护市民」；全体卫兵穿与暴风城军队士兵同样的装备与战袍，可见他们使用剑、盾、弩、捕网和油灯；夜里有提着油灯的「暴风城巡夜人」
  tag: ✅
  source: Warcraft Wiki - Stormwind City Guard
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard
  quote: "keeping the peace within the city's walls ... patrolling on the ground and in the sky, or guarding the capital's gates ... All guards wear the same gear and tabard as the soldiers of the Stormwind Army. In terms of equipment, they can be seen employing swords, shields, crossbows, catch nets, and oil lamps ... \"Stormwind City Patroller\" units shown \"at night\" with oil lamps"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "两名披暴风城战袍的卫兵沿街缓步巡逻，一人持剑一人背弩；夜镜里改为一人提油灯在前照路"
  negative: "现代警察、警棍、手电筒、对讲机、警车、反光背心、警戒线"
  note: **三个细节值钱**：① **空中也有巡逻**（骑狮鹫），所以夜空里掠过的黑影是卫兵不是怪物；② **捕网（catch nets）**——他们抓人不是只砍，这个道具很少见、很有辨识度；③ **油灯**是夜间照明，不是火把、更不是手电。

- fact_id: stormwind.travel.013
  claim: 暴风城监狱（The Stockade）是一座高度戒备的监狱建筑群，「藏在暴风城运河区的地下」，入口在运河区、门外有一块集合石，从建筑里的楼梯下去；典狱官是 Warden Thelwater；里面关着「小偷小摸、政治煽动者、杀人犯，以及一批全境最危险的罪犯」
  tag: ✅
  source: Warcraft Wiki - The Stockade；Warcraft Wiki - Stormwind City
  source_url: https://warcraft.wiki.gg/wiki/The_Stockade
  quote: "A high-security prison complex, hidden beneath the canal district of Stormwind City. ... Warden Thelwater presides over the facility as its commander. ... \"Home to petty crooks, political insurgents, murderers, and a score of the most dangerous criminals in the land.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河边一处不起眼的石砌入口，门外立着一块石头，门内一段向下的楼梯没入黑暗"
  negative: "铁栅栏大门、瞭望塔探照灯、铁丝网、囚车、狱警制服"
  note: ⚠️ Stormwind City 页另写「The Stockade is accessible from the Mage Quarter」，与本页「运河区」**有出入**——两说都实读到了。按 `ai_video.md` rule 4i ② 的「冲突三问」：这大概率是**伪冲突**（监狱在运河区、而运河区与法师区相邻，从法师区能走过去）。**不必取舍，画面按「运河边的地下入口」拍即可。** 同页记载监狱原先有一座钟楼、后来被移除——**Vanilla 是否有钟楼未查**，别画。

- fact_id: stormwind.travel.014
  claim: 艾泽拉斯按真实的 24 小时循环转，昼夜跟各服务器自己的时间走——「服务器时间就是游戏内时间」，太阳在真实的 24 小时里升起落下
  tag: ⚠️
  source: Wowpedia - Server time（仅搜索摘要）
  source_url: https://wowpedia.fandom.com/wiki/Server_time
  quote: "In World of Warcraft, Azeroth turns on a literal 24 hour cycle, and server time is in-game time. ... the cycle of day and night in World of Warcraft is tied to each realm's particular time ... with the sun rising and setting over the course of a real-life 24-hour period."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "同一条街的晨、午、夜三态：清晨斜射的低角度光、正午的顶光与人潮、夜里的冷蓝与灯光点"
  negative: "永远白天、时间静止、跳帧式昼夜、极昼极夜"
  note: ⚠️ ai_draft。**但这条是「一天」这个片名的机制基础**——这个世界真的有一天二十四小时。旅行者「住一晚、次晨打分」在机制上成立。

- fact_id: stormwind.travel.015
  claim: **宵禁**在暴风城没有任何记载——卫兵夜间照常巡逻（travel.012），矮人区的工坊通宵开工（house.013），但没有任何来源提到禁止夜行
  tag: ⚠️
  source: 本次检索未在 T0–T2 任一来源中找到宵禁记载
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard
  quote: "（未查到——Stormwind City Guard 及 Stormwind City 条目均无宵禁 / curfew 相关段落）"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "夜里的街上仍有零星行人与提灯的巡夜卫兵，店门多数已闭，但街不是死的"
  negative: "宵禁告示、封街路障、夜间清场、禁行时段广播"
  note: 沉默证据。**画面结论：夜里的暴风城是「安静但没有关闭」**，不是清空的鬼城，也不是照常喧闹。

- fact_id: stormwind.travel.016
  claim: **城内能不能骑马**未查实——warcraft.wiki.gg 的 Mount 页只写了飞行禁区（no-fly zone），没有任何关于地面坐骑在室内 / 城内的限制条款
  tag: ⚠️
  source: Warcraft Wiki - Mount
  source_url: https://warcraft.wiki.gg/wiki/Mount
  quote: "there are still various No-fly zones where flight isn't available for various reasons.（全页仅此一条限制条款，无城内 / 室内地面坐骑规则）"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（暂不出画——须先定）"
  negative: "（待定）"
  note: **明确记为未查**。结合 travel.010（40 级 + 昂贵）与 travel.001（正午街道挤到难行），**画面取「街上极少数人骑马、绝大多数走路」是最安全的**——无论规则如何，这个比例都不会错。如果要拍旅行者在城里骑行，须先人工核实。
```

---

## §4 公共设施（归在 §2 / §3，本节只做索引）

只记位置与外观，**数值归 W4、布局归 W11**：

| 设施 | 所在区 | 外观要点 | 回指 |
|---|---|---|---|
| 银行 Stormwind Counting House | 贸易区西南角，正对喷泉、拍卖行对面 | 罗马式列柱 + 石台阶 | `house.011` ⚠️ |
| 邮箱 | 贸易区西南侧，紧邻镀金玫瑰 | —（未查外观） | `house.011` / `house.001` |
| 拍卖行 | 贸易区中央 | —（未查外观） | `myth.014` ⚠️ 版本问题 |
| 旅店 镀金玫瑰 | 贸易区，夹在银行与拍卖行之间 | 二层门脸，进门即堂屋 | `house.001` |
| 狮鹫栖木 | 贸易区东侧坡道上去 | 高处木架 + 停驻的狮鹫 | `travel.005` |
| 奶酪铺 Trias' Cheese | 贸易区 [66, 74] | 小店面，整轮奶酪上架 | `food.005` |
| 花店 Fragrant Flowers | 运河尽头 / 贸易区靠旧城区一侧 | —（未查外观） | ⚠️ 仅搜索摘要 |
| 铁匠铺 / 熔炉 / 铁砧 | 矮人区 | 烟霭 + 橙红炉火 + 锤声 | `travel.008` |
| 深铁矿道入口 | 矮人区东侧 | 向下的隧道口 | `travel.007` |
| 光明大教堂 | 教堂广场（全城地势最高处） | 细长尖塔，高到「看着像立不住」 | 见 note |
| 市政厅 City Hall / 孤儿院 | 教堂广场 | —（未查外观） | `house.012` ⚠️ |
| 监狱 The Stockade | 运河区地下 | 门外集合石 + 向下楼梯 | `travel.013` |
| 法师塔 Wizard's Sanctum | 法师区中央 | 「一道盘旋石坡从地面轻盈升到塔顶」 | 见 note |
| 酒馆 The Slaughtered Lamb | 法师区 | 空荡、阴冷、地下有口 | `house.010` |
| 酒馆兼餐馆 The Blue Recluse | 法师区 | 上档次、有后厨 | `food.014` |
| 酒馆 猪和哨声 | 旧城区 | 吧台 + 醉汉 + 烤肋排炉 | `house.004` / `food.015` |
| SI:7 总部 / Command Center / 勇士大厅 | 旧城区 | —（未查外观） | ⚠️ 仅实读到名称 |

> 教堂与法师塔的形制引文（同人游记 T3 ⚠️，仅作氛围）：「Delicate spires soar into the air, the entire structure looking too tall to stand」（光明大教堂）；「The Mage Tower is a graceful structure surrounded by a grove of trees...a spiraling stone ramp rises airily from the ground, going all the way to the top」（法师塔）。出处 https://destron.blogspot.com/2007/10/stormwind-city.html
> 官方导览另记：教堂广场中央有一座喷泉（**但那座喷泉在 Vanilla 上面是谁，见 myth.004——是本路最隐蔽的一个坑**）。出处 http://worldofwarcraft.blizzard.com/en-us/news/20142731/welcome-to-stormwind-a-guided-tour

---

## §5 玩家误传黑名单（`stormwind.myth.NNN`）

> **本节是 W6 最重要的产物，下游直接变成全站负向词库。**
> 分四类：**A 版本错置**（Vanilla 之后才有的东西）、**B 跨 IP 混淆**、**C 画风错置**、**D 常见设定错 + 模型默认坑**。

### A. 版本错置（最致命——错了整条 shot 报废）

```yaml
- fact_id: stormwind.myth.001
  claim: ❌ 暴风城港口（Stormwind Harbor）在 Vanilla **不存在**——它是 2008-10-14 的 3.0.2 补丁（巫妖王之怒）才加的；港口大门的施工过程在 2.4.3 才开始出现在画面里
  tag: ❌
  source: Warcraft Wiki - Stormwind Harbor（Patch changes / Gallery）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Harbor
  quote: "\"Added.\" (Patch 3.0.2, Wrath of the Lich King expansion, October 14, 2008) ... \"The harbor gatehouse being built (patch 2.4.3)\" ... \"The harbor gatehouse finished (patch 3.0)\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（正片绝不出现——只可进「我以为·踩坑」栏目）"
  negative: "暴风城港口, 码头, 栈桥, 泊位, 帆船, 桅杆, 船帆, 缆绳, 船锚, 水手, 跳板, 货箱堆场, 灯塔, 海鸥, 海浪拍岸"
  note: **三条必查之一，已查实。** 双重印证：① 官方 patch history 写死 3.0.2；② 暴雪官网 Classic 交通指南列了 Classic 的全部船班，暴风城一条都没有（`travel.009`）。这是最容易踩的坑，因为今天所有玩家记忆里的暴风城都有港口。

- fact_id: stormwind.myth.002
  claim: ❌ 公园区（The Park）在 Vanilla **完好无损**——它是 2010-11-23 的 4.0.3a（大地的裂变）才被死亡之翼摧毁的。Vanilla 的公园是「暴风城居民的休闲去处」，中央有暗夜精灵造的**月井**，是造访的暗夜精灵的庇护所，也是**整个东部王国唯一有德鲁伊训练师的地方**
  tag: ❌
  source: Warcraft Wiki - Park
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "a place devoted to leisure activities for Stormwind's populace ... \"The night elves created a Moonwell in the center of the park square.\" ... it \"became a refuge for visiting night elves, who found the comforting presence of nature a welcome respite.\" ... \"the only place in the Eastern Kingdoms where druid trainers resided.\" ... eliminated in Patch 4.0.3a (November 23, 2010) when \"Deathwing's visit to Stormwind\" caused destruction"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（Vanilla 正解）一片绿意浓密的休闲园区，中央一口暗夜精灵的月井，水面泛着冷银色光，树下有暗夜精灵在歇息"
  negative: "公园废墟, 焦黑巨坑, 塌陷地面, 爪痕, 断柱残垣, 冒烟的瓦砾, 狮王之息, Lion's Rest, 纪念碑广场"
  note: **三条必查之一，已查实。** 这条是**正反双向**的：既要挂废墟的负向，又要正向写出 Vanilla 的月井 + 暗夜精灵。旅行者去公园遇见暗夜精灵，是很好的「这个城市不止住着人类」的段落。补：公园废墟上后来建的 Lion's Rest 是 7.0.3（2016）才有的，见 myth.010。

- fact_id: stormwind.myth.003
  claim: ❌ 瓦里安·乌瑞恩在 Vanilla **不在位**——他在去塞拉摩参加外交会谈的路上离奇失踪，由 Highlord Bolvar Fordragon 出任摄政，由 Lady Katrana Prestor 在旁「就如何正确使用暴风城的资源」向他进言；而 Lady Prestor 其实是黑龙军团的龙母**奥妮克希亚**伪装的
  tag: ❌
  source: Warcraft Wiki - Stormwind City；Warcraft Wiki - Bolvar Fordragon；Wowpedia - Varian Wrynn
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "\"Highlord Bolvar Fordragon acted as the Regent of Stormwind and the commander of their military forces, with Lady Prestor advising him on the proper use of Stormwind's resources.\" ... \"After King Varian went missing under suspicious circumstances, Prince Anduin Wrynn was given the crown.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（王座上不是瓦里安——若要入画，是摄政的博瓦尔·弗塔根、幼年的安度因王子与身着华服的凯特拉娜·普瑞斯托女士）"
  negative: "瓦里安·乌瑞恩, Varian Wrynn, 双持巨剑的国王, 狼首铠甲, 成年国王坐在王座上"
  note: **三条必查之一，已查实。** 这是 Vanilla 与后续版本最难看出差别的一处——因为**王座上确实坐着人**，只是不是观众以为的那个人。本剧如果只是「逛一天」不必进王宫，但**只要镜头扫到王座、扫到国王画像、扫到雕像，就必须核这一条**。

- fact_id: stormwind.myth.004
  claim: ❌ 暴风要塞门前那座「立着瓦里安国王雕像的高耸喷泉」在 Vanilla **不存在**——Stormwind Keep 在 4.0.3a 被里里外外整个重做：「通往王座厅的路现在是露天的，重新设计过，配了一条宏大的步道和一座喷泉；王座厅也重做了」
  tag: ❌
  source: Warcraft Wiki - Stormwind Keep（Patch changes）；暴雪官网导览（描述的是重做后的样子）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "\"In Cataclysm, Stormwind Keep was entirely remodeled, inside, as well as outside. The path leading to the throne room is now open air and redesigned, complete with a grand walkway and a fountain. The throne room was redesigned too and the garden area before the Library now has a view overlooking the Stormwind Lake.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（Vanilla 正解：通往王座厅的是室内通道，不是露天步道；门前没有瓦里安喷泉）"
  negative: "瓦里安雕像喷泉, 露天宏大步道, 重做后的王座厅, 俯瞰暴风湖的花园"
  note: **暴雪官网自己的导览文里那句「A towering fountain with a statue of King Varian Wrynn stands sentinel as you enter the grounds」写的是 Cataclysm 之后的暴风城**——官方文档本身就是版本陷阱。**引用官方不等于版本正确**，这是本路学到的一条通则。

- fact_id: stormwind.myth.005
  claim: ❌ 教堂广场喷泉上那尊**乌瑟尔·光明使者**的雕像，Vanilla 时**不是乌瑟尔，是阿隆索斯·法奥**——「大教堂前原本立着一座雕像与喷泉，纪念法奥在第二次战争后所做的一切辛劳」，「到大地裂变之时，这座纪念碑不知出于什么原因被换成了献给乌瑟尔·光明使者的雕像」
  tag: ❌
  source: Warcraft Wiki - Alonsus Faol
  source_url: https://warcraft.wiki.gg/wiki/Alonsus_Faol
  quote: "\"A statue and fountain were once standing in front of the Cathedral of Light in Stormwind City, honoring all the hard work done by Faol after the Second War.\" ... \"At the time of the Cataclysm, the monument was replaced for unknown reasons by a statue dedicated to Uther the Lightbringer.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（Vanilla 正解：大教堂前的喷泉雕像是阿隆索斯·法奥——一位教士形象的老者，不是持锤的圣骑士）"
  negative: "乌瑟尔雕像, Uther the Lightbringer, 持战锤的圣骑士雕像, 「Uther the Lightbringer / A righteous Paladin」铭牌"
  note: **这是本路挖到的最隐蔽的一个坑**，几乎没人会想到去核。而它**极易入画**——教堂广场是必经之地、喷泉是天然的构图中心。乌瑟尔的铭牌原文（"Uther the Lightbringer / A righteous Paladin, an honorable man, and a dear friend."）是 Cataclysm 之后的，**一旦入画就是穿帮**。⚠️ 法奥雕像**具体长什么样**未查到，须人眼核。

- fact_id: stormwind.myth.006
  claim: ❌ 英雄谷里**倒在水中的雕像**、城门塔楼上**巨大的灼烧爪痕**，在 Vanilla 都不存在——那是死亡之翼在大地裂变里掠过城市时造成的：「他对英雄谷造成了巨大破坏，在附近的塔楼上留下巨大的灼烧爪痕，并把达纳斯·托尔贝恩的雕像掀翻进桥下的水里」。Vanilla 的英雄谷是**五尊雕像完好直立**——图拉扬、奥蕾莉亚·风行者、卡德加、库德兰·蛮锤、达纳斯·托尔贝恩
  tag: ❌
  source: Wowpedia / Warcraft Wiki - Valley of Heroes（搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "five statues in the likeness of Turalyon, Alleria Windrunner, Khadgar, Kurdran Wildhammer, and Danath Trollbane were placed within Stormwind's Valley of Heroes ... As Deathwing swept over the city during the Cataclysm, he caused great damage to the Valley of Heroes, leaving massive, scorching clawmarks on the nearby towers and toppling the statue of Danath Trollbane into the water below the bridge."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（Vanilla 正解）跨过护城水道的石桥两侧，五尊巨大石像整整齐齐立着，全部完好，无一倾倒；两侧塔楼墙面干净无损"
  negative: "倒塌的雕像, 掀翻进水里的石像, 塔楼上的巨大爪痕, 灼烧痕迹, 焦黑墙面, 缺角的石像"
  note: ⚠️ ai_draft（仅搜索摘要）。**但这是进城第一镜**——旅行者的第一个画面就是这座桥。**五尊全立** vs **一尊倒在水里**，一眼就能判版本。强烈建议人眼核实。另：英雄谷是 Stormwind City 页确认存在的分区名（ai_read）。

- fact_id: stormwind.myth.007
  claim: ❌ 「暴风城大使馆」（Stormwind Embassy）在 Vanilla 不存在——它是 2018-01-16 的 7.3.5 补丁才加的，用作联盟领袖会面处与盟约种族总部
  tag: ❌
  source: Wowpedia / Warcraft Wiki - Stormwind Embassy（搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Embassy
  quote: "The Stormwind Embassy was added in Patch 7.3.5 (2018-01-16) ... a building in Stormwind City that serves as a meeting point for the leadership of the Alliance and as headquarters for its allied races."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（正片绝不出现）"
  negative: "暴风城大使馆, Stormwind Embassy, 各族旗帜并列的会馆, 盟约种族代表团"
  note: ⚠️ ai_draft。这条与 myth.008（种族）联动：没有大使馆 ＝ 街上也不该有盟约种族代表。

- fact_id: stormwind.myth.008
  claim: ❌ 狮王之息（Lion's Rest）在 Vanilla 不存在——它建在公园的废墟上，是 2016 年 7.0.3 补丁（军团再临）才有的
  tag: ❌
  source: Warcraft Wiki - Park；Warcraft Wiki - Stormwind City
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "\"Lion's Rest was finally built on its ruins\" in Patch 7.0.3 (2016) ... \"This area has been built as a replacement for the Stormwind Park, swallowed by Deathwing's assault on the city.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（正片绝不出现）"
  negative: "狮王之息, Lion's Rest, 水边的纪念广场, 沉在水里的国王石棺, 纪念墙"
  note: 与 myth.002 是同一块地的三个时代：Vanilla 是公园 → Cataclysm 是废墟 → Legion 是狮王之息。**画错哪一个都是版本错。**

- fact_id: stormwind.myth.009
  claim: ❌ 法师区塔里那个「所有传送门集中在一起的传送门大厅」在 Vanilla 不存在——现行的暴风城传送门大厅是 8.1.5 补丁才把「此前散落在都城各处」的传送门整合进塔内、并把塔的内部完全重做的
  tag: ❌
  source: Wowpedia / Warcraft Wiki - Wizard's Sanctum（搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Wizard%27s_Sanctum
  quote: "With patch 8.1.5, the tower's interior was completely revamped to house the Stormwind Portal Room, where the mages of Stormwind and their allies maintain portals to a number of different areas on Azeroth, Outland, and Draenor that had previously been scattered throughout the capital."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（正片绝不出现整排发光传送门的大厅）"
  negative: "传送门大厅, 一排排发光的传送门, 环形传送门厅, 各地地标浮现在门里"
  note: ⚠️ ai_draft。⚠️ **本条只查实了「8.1.5 做了整合与重做」，没有查实「Vanilla 塔里有没有传送门」。** 严格说：Vanilla 的法师是手动开传送门给人用的，塔里是否有常驻门**未查**。**结论取保守：不画传送门大厅**（这一点是确定的），至于零星的门画不画，须再查。

- fact_id: stormwind.myth.010
  claim: ❌ **在暴风城飞起来**在 Vanilla 不可能——飞行坐骑是燃烧的远征（2007）才有的，且只能在外域飞，「不能在东部王国或卡利姆多飞」；东部王国要到大地的裂变才开放飞行
  tag: ❌
  source: Wowpedia - Mount / World of Warcraft: Cataclysm（搜索摘要）
  source_url: https://wowpedia.fandom.com/wiki/Mount
  quote: "After reaching level 70, players were able to ride flying mounts although only in Outland, not in Eastern Kingdoms or Kalimdor. ... Along with the environmental redesign comes the ability for players to use flying mounts on both classic continents."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（天上只有卫兵的狮鹫在巡逻，没有任何骑着飞行坐骑的平民）"
  negative: "满天飞行坐骑, 龙, 飞行扫帚, 飞行地毯, 悬停在广场上空的坐骑, 空中交通"
  note: ⚠️ ai_draft。**但这条对画面影响极大**：今天的暴风城天上密密麻麻都是飞行坐骑，**Vanilla 的天空是空的**——除了卫兵的狮鹫（`travel.012` 明写 "patrolling on the ground and in the sky"）和狮鹫栖木起降的航线。**「天空是空的」本身就是一个可口播的版本标志。**
```

### B. 跨 IP 混淆

```yaml
- fact_id: stormwind.myth.011
  claim: ❌ 把暴风城画成「地球中世纪城堡」或《指环王》米那斯提力斯式的通用奇幻王城——丢掉暴风城独有的**白石墙 + 蓝色板岩屋顶 + 狮子纹章**三件套
  tag: ❌
  source: Warcraft Wiki - Stormwind Keep（蓝板岩）；Warcraft Wiki - Stormwind City（白石）；暴雪官网导览（狮子）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "\"Its roof was shod with blue slate\"（Keep 页，ai_read）；the city features \"white stone for its exterior\"（Stormwind City 页，ai_read）；\"The lion, symbol of the Alliance is prominently displayed both in the banners and the stone effigies on the parapets.\" / \"there are two massive stone lion heads on either side of the entrance doors.\"（官网导览）"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "白石砌的墙体 + 蓝色板岩坡屋顶 + 城垛上的石狮雕像与狮纹旗帜；大门两侧各有一个巨大的石狮首"
  negative: "灰褐色石城, 白色多层阶梯城, 米那斯提力斯, 通用中世纪城堡, 哥特尖顶群, 城堡吊桥铁闸, 红瓦屋顶, 茅草屋顶"
  note: **三件套是暴风城的身份证**，缺一就滑回通用奇幻。「城垛上的石狮 + 大门两侧的巨大石狮首」是官网亲口写的具体形制，比抽象的「狮子元素」好用得多。⚠️ 狮子引文出自官网导览（ai_read 时未直接返回这两句、来自搜索摘要转述），**须人眼回原页核**。

- fact_id: stormwind.myth.012
  claim: ❌ 把暴风城的纹章配色画错——它是**蓝底金狮**（联盟／暴风城的战袍与旗帜），不是随便一种「王国纹章」
  tag: ⚠️
  source: Warcraft Wiki - Stormwind (kingdom)（该页只挂战袍图，正文无配色文字描述）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_(kingdom)
  quote: "The wiki provides a tabard image but no detailed verbal description of colors or heraldic elements in the text."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（配色须人眼看图定色名后再写死）"
  negative: "红底纹章, 绿底纹章, 黑底纹章, 双头鹰, 十字纹, 百合花纹, 随机家徽"
  note: ⚠️ **标 ⚠️ 不是 ✅——「蓝底金狮」这四个字本次没有查到任何正面文字出处**，wiki 只挂图不写字。本条的**可用部分**只有负向（不是红/绿/黑底、不是鹰/十字/百合），**正向配色必须人眼看战袍图后按 `ai_video.md` 的锁定色名写死**，不得凭印象填 hex 或色名。这是本文第二个诚实边界。

- fact_id: stormwind.myth.013
  claim: ❌ 把暴风城画成「魔兽世界通用奇幻城」——忽略它在正史里是**被兽人夷平后重建的新城**：石匠公会在第二次战争后受雇重建暴风城，把城市恢复到往日的雄伟，随后因为讨薪被拒而在新建成的街上暴动
  tag: ⚠️
  source: Wowpedia - Edwin VanCleef / Defias Brotherhood（搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Edwin_VanCleef
  quote: "Edwin VanCleef was the leader of the Stonemasons Guild that rebuilt Stormwind City after it was sacked by the Horde in the First War. ... They restored Stormwind to its former majesty, but when they asked for payment for their honest work, the House of Nobles refused to pay ... Edwin and the Stonemasons started a riot in the streets of the newly-rebuilt Stormwind."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "石工整齐、接缝新、墙面干净——这是一座**刚重建不久**的城，不是一座积了几百年灰的老城"
  negative: "千年古城的风化墙面, 爬满藤蔓的石墙, 断裂的古老雕像, 苔藓覆盖的石阶, 废墟感"
  note: ⚠️ ai_draft。**这条修正了一个很微妙的画风倾向**：AI 画「奇幻王城」默认往「古老沧桑」走，而暴风城的正确气质是**崭新**——除了 Old Town（`house.008` 明写它「从来不需要真正重建」，所以只有旧城区该有旧感）。**新城 vs 旧城区的对比，正是重建这段历史在画面上的落点。**
```

### C. 画风错置

```yaml
- fact_id: stormwind.myth.014
  claim: ❌ 画成游戏截图质感／卡通渲染（低多边形、塑料高光、描边、饱和度拉满的游戏 UI 感），或者反过来画成完全写实的欧洲石城——本片是**半写实**：**形制与配色忠于游戏，材质与光线走写实**
  tag: ⚠️
  source: 本条是本项目的画风定调，不是外部事实
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "（无外部出处——本条为项目自定画风契约，登记在此以便下游统一挂负向）"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "半写实：建筑形制与配色照游戏，石材/木材/布料/皮革的材质与光照走真实物理"
  negative: "游戏截图, 游戏引擎渲染, UI 界面, 血条, 名字牌, 低多边形, 卡通渲染, 赛璐璐描边, 塑料高光, 过饱和, 3D 建模预览, 白模, 灰模, 完全写实的欧洲石城照片"
  note: ⚠️ 本条不是「查到的事实」，是**项目自定的画风契约**，登记在 myth 表里是为了让它和别的负向词一起进词库。真正的风格串定义归 W3 / 风格指南，本条只负责挂负向。

- fact_id: stormwind.myth.015
  claim: ❌ 招牌上写现代印刷体英文、或让模型自由生成的乱码文字——店铺在游戏里是靠**吊挂的图形招牌 + 建筑形制**辨识的
  tag: ⚠️
  source: Warcraft Wiki - Trade District / Mage Quarter（店名作为子区域名存在，如 The Empty Quiver / Everyday Merchandise / Lionheart Armory / Alchemy Needs / Duncan's Textiles / Larson Clothiers / Stormwind Staves / Heavy Handed Weapons / The Protective Hide）
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "Named establishments include The Empty Quiver, Everyday Merchandise, Lionheart Armory, and Trias' Cheese, among others."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "店门上方挂着木牌，牌面是图形／器物剪影（箭袋、锤子、奶酪轮、法杖），不是文字"
  negative: "印刷体英文招牌, 乱码文字, 伪英文, 霓虹灯招牌, LED 字, 中文招牌, 手写体价目牌, 二维码, 条码"
  note: ⚠️ **「店名存在」是 ai_read 查实的（上面九家店名都是 wiki 上的子区域名），但「招牌是图形不是文字」这一点本次没查到文字出处，是推断。** 不过负向侧无论如何都成立：**AI 生成的招牌文字一定是乱码**，这是模型默认坑里最稳定的一个，必须挂死。**正向（招牌到底长什么样）须人眼核客户端。**
```

### D. 常见设定错 + 模型默认坑

```yaml
- fact_id: stormwind.myth.016
  claim: ❌ 街上出现**德莱尼 / 血精灵 / 狼人 / 熊猫人 / 虚空精灵**——Vanilla 的联盟只有人类、矮人、侏儒、暗夜精灵四族；德莱尼是燃烧的远征（2007）才加入联盟的
  tag: ❌
  source: Wikipedia / Wowhead - TBC Alliance Races（搜索摘要）
  source_url: https://en.wikipedia.org/wiki/World_of_Warcraft:_The_Burning_Crusade
  quote: "The vanilla version of WoW Classic included Human, Dwarf, Gnome, and Night Elf as playable Alliance races. ... Two new playable races were added to World of Warcraft in The Burning Crusade: the Draenei of the Alliance and the Blood Elves of the Horde."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "街上的人群：以人类为绝对主体，矮人与侏儒集中在矮人区，暗夜精灵零星出现（尤其在公园）"
  negative: "德莱尼, 蓝皮肤大角种族, 血精灵, 狼人, 熊猫人, 虚空精灵, 地精, 狐人, 牛头人, 兽人, 巨魔, 亡灵"
  note: ⚠️ ai_draft。**四族比例是街景的骨架**：人类主体（这是人类的都城）、矮人侏儒集中在矮人区（`house.013` / `travel.008`）、暗夜精灵在公园（`myth.002` 明写公园是暗夜精灵的庇护所）。⚠️ 另有零星**高等精灵** NPC——Stormwind (kingdom) 页把 High Elves 列在王国治下人口里（ai_read），但**具体在 Vanilla 的暴风城街上有没有未查**，保守起见不画。

- fact_id: stormwind.myth.017
  claim: ❌ 部落角色（兽人 / 巨魔 / 牛头人 / 亡灵）在暴风城街上闲逛——暴风城卫兵对部落是敌对的，部落一靠近就打
  tag: ❌
  source: Wowpedia / Warcraft Wiki - Stormwind City Guard (NPC)（搜索摘要）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "Stormwind City Guards are flagged for PvP and are hostile to Horde players. They will attack the Horde if one gets close to them."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（街上不出现任何部落种族的平民）"
  negative: "兽人, 巨魔, 牛头人, 亡灵, 地精, 血精灵, 部落旗帜, 部落纹章, 两族和平共处的街景"
  note: ⚠️ ai_draft。**这条同时给了一个剧情机会**：外来旅行者如果长相「不像联盟四族」，会不会被卫兵盯上？这是本片可用的紧张点，但**属剧情设计，不属本路职责**，只记在此备用。

- fact_id: stormwind.myth.018
  claim: ❌ 把猪和哨声当成「能住宿的旅店」——Vanilla 它只是酒馆，没有旅店老板、不能在那儿绑炉石；**Vanilla 的暴风城只有镀金玫瑰一家旅店**
  tag: ❌
  source: Warcraft Wiki - Pig and Whistle Tavern（Patch changes）
  source_url: https://warcraft.wiki.gg/wiki/Pig_and_Whistle_Tavern
  quote: "Patch 4.0.1 (2010-10-12): Innkeeper Maegan Tillman was added, making the Pig and Whistle Stormwind's second inn."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（猪和哨声里不出现旅店老板、不出现通往客房的楼梯动线、不出现住宿交谈）"
  negative: "猪和哨声的旅店老板, Maegan Tillman, 在猪和哨声住宿, 酒馆二楼客房"
  note: 回指 `house.003`。**「这城这么大，能住的地方只有一家」本身就是可口播的好料**，还能自然解释旅行者为什么非住镀金玫瑰不可。

- fact_id: stormwind.myth.019
  claim: ❌ 让人**站着吃、边走边吃**——这个世界的所有食物道具都写着「进食过程中必须保持坐姿」
  tag: ❌
  source: Warcraft Wiki - Freshly Baked Bread / Shiny Red Apple / Dwarven Mild（三件道具逐字相同）
  source_url: https://warcraft.wiki.gg/wiki/Freshly_Baked_Bread
  quote: "Restores 234 health over 21 sec. Must remain seated while eating."（Freshly Baked Bread）；\"Restores 58 health over 18 sec. Must remain seated while eating.\"（Shiny Red Apple）；\"Restores 530 health over 24 sec. Must remain seated while eating.\"（Dwarven Mild）
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "凡进食镜，人物一律先坐下——长凳、台阶、酒馆的桌凳、运河边的石沿"
  negative: "站着吃, 边走边啃, 快走中咬一口, 单手举着食物走路, 站着喝, 走路喝水"
  note: **三件不同道具逐字重复同一句，说明这是机制通则不是个例。** 这条同时也是**正向画面语法**：吃＝找地方坐，所以每一顿都自带一个「她在哪儿坐下」的构图选择。回指 `food.004`，并与 `food.008` 酒保的招呼语「pull up a seat」互证。

- fact_id: stormwind.myth.020
  claim: ❌ 把深铁矿道画成蒸汽火车（煤烟、汽笛、道砟）或现代地铁（闸机、售票口、电子屏）——它是**免费的地下电车**，从矮人区东侧的隧道进
  tag: ❌
  source: 暴雪官网《WoW Classic: Getting around Azeroth》；Warcraft Wiki - Dwarven District
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/23156366
  quote: "the Deeprun Tram provides quick transportation between the capital cities of Stormwind and Ironforge—for free!"；\"The Stormwind City end of the Deeprun Tram line is accessible through a tunnel on the east side of the district.\"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "地下隧道里的有轨车厢，侏儒／矮人工程造物的机械感，不是蒸汽机车"
  negative: "蒸汽火车, 煤烟, 汽笛, 蒸汽喷发, 铁轨道砟, 枕木, 地铁闸机, 售票窗口, 电子显示屏, 广播报站, 车票"
  note: 回指 `travel.007`。**免费**这一点和 `house.005`（住店免费）、`travel.006`（飞行收费）一起，构成本片「这城里什么要钱、什么不要钱」的完整账。

- fact_id: stormwind.myth.021
  claim: ❌ 把旧城区画得和贸易区一样光鲜——旧城区是全城最旧最脏最臭的区，是穷人、乞丐、小偷的居住区
  tag: ❌
  source: Warcraft Wiki - Old Town
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "a rustic, downtrodden place, where the streets are described as far dirtier and smellier than the other districts ... It remains \"preserved\" but \"not nearly as pristine as the rest of the capital.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旧城区：窄巷、斑驳墙面、泥水、墙根的穷人；与贸易区的白石整洁形成直接反差"
  negative: "和贸易区一样整洁的旧城区, 新铺石板路, 干净白墙, 统一立面, 光鲜商铺"
  note: 回指 `house.008` / `house.009`。**旅行者从贸易区走到旧城区，必须有一个「一眼看出落差」的镜头**，否则这个城市就只剩一种质感。

- fact_id: stormwind.myth.022
  claim: ❌ 现代元素混入——玻璃窗格、电灯路灯、金属栏杆、指示牌、砖砌工业烟囱、下水道井盖、现代铺装
  tag: ⚠️
  source: 本条是模型默认坑的通用清单，非外部事实；但照明的正确形制有两条出处（卫兵夜巡提油灯、法师区奥术灯柱）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard
  quote: "In terms of equipment, they can be seen employing swords, shields, crossbows, catch nets, and oil lamps ... \"Stormwind City Patroller\" units shown \"at night\" with oil lamps"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "夜间照明：卫兵手提的油灯 + 法师区的奥术灯柱 + 屋内的炉火，不出现任何电光源"
  negative: "电灯, 路灯杆, 灯泡, 灯罩, 霓虹, LED, 玻璃幕墙, 平板玻璃窗, 金属栏杆, 交通指示牌, 井盖, 沥青路面, 水泥, 空调外机, 电线, 电线杆, 工业砖烟囱"
  note: ⚠️ 通用坑清单。**照明是本条最实用的一半**：正向有两个明确光源（油灯 / 奥术灯柱，出处分别是 `travel.012` ai_read 与 `travel.004` T3 ⚠️），加上屋内炉火，够撑起整个夜戏。

- fact_id: stormwind.myth.023
  claim: ❌ 把旅店画成有前台柜台、登记簿、房号牌的现代酒店——旅店老板就站在一楼堂屋里，办事靠说话，没有柜台流程
  tag: ⚠️
  source: Warcraft Wiki - Innkeeper Allison（位置「just inside the inn on the ground floor」）；Warcraft Wiki - Innkeeper（服务描述里只有对话选项，无任何登记/收费流程）
  source_url: https://warcraft.wiki.gg/wiki/Innkeeper
  quote: "To set or change the bind point for your hearthstone, talk to an innkeeper and click Make this inn your home."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "进门就是堂屋，店主站在堂屋一侧，走过去说两句话就算住下了"
  negative: "酒店前台, 柜台, 登记簿, 房卡, 房号牌, 钥匙牌墙, 行李寄存, 铃铛按钮, 电梯, 大堂沙发"
  note: ⚠️ 半推断：「店主在一楼门内、办事靠对话」是查实的；「所以没有柜台」是推断。但**负向侧无论如何成立**——现代酒店大堂是 AI 画「inn」时最稳定的默认坑之一。**旅店内部的正向形制仍未定，见 `house.006`。**

- fact_id: stormwind.myth.024
  claim: ❌ 酒器画成玻璃扎啤杯／现代啤酒杯——查到的容器词是瓶（Bottle）／皮囊（Skin）／扁壶（Flask）／带盖大酒壶（Flagon）／罐（Jug）
  tag: ⚠️
  source: Warcraft Wiki - Reese Langston（Sells 表的容器词）
  source_url: https://warcraft.wiki.gg/wiki/Reese_Langston
  quote: "Bottle of Dalaran Noir / Skin of Dwarven Stout / Flask of Stormwind Tawny / Flagon of Dwarven Mead / Jug of Badlands Bourbon"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "吧台与桌上的酒器：带塞的深色酒瓶、鼓胀的皮酒囊、细颈扁壶、带盖大肚酒壶、陶罐——同台并列"
  negative: "玻璃扎啤杯, 啤酒杯, 玻璃高脚杯, 透明玻璃器皿, 吸管, 易拉罐, 瓶盖, 品牌酒标"
  note: ⚠️ **半推断，要说清边界**：五个容器词是道具名里查实的（ai_read），所以**这五种容器确实存在**；但「所以没有玻璃杯」是推断——**餐具／酒具的材质在所有来源里都没有正面记载**（见 `house.006`）。**正向可用（这五种照写），反向只挂「现代玻璃扎啤杯」这类明确现代的**，别把「玻璃」整个禁掉。
```

---

## §6 综合 · 旅行者的一天

> 下面是把 §1–§5 的事实按时间轴串起来的**可拍版本**。每一条都带回指；凡带 ⚠️ 的，落到 prompt 之前须人眼升 `human`。

### 清晨（进城 · 第一顿）
她从艾尔文森林方向进城，先过**英雄谷的石桥**——桥两侧**五尊巨像完好直立**，塔楼墙面干净无爪痕（`myth.006` ⚠️）。抬头是**白石墙 + 蓝色板岩屋顶 + 城垛石狮**（`myth.011`），大门两侧各一个巨大的石狮首。
过桥就是**贸易区**。清晨街还不挤（正午才挤，`travel.001` ⚠️）。**面包小贩 Thomas Miller 正沿街走着吆喝**——「Rolls, buns and bread. Baked fresh!」（`food.001` / `food.002`）。她买最便宜那档的硬面包（25 铜）或新烤的圆面包（1 银 25 铜）（`food.003` ⚠️），**然后在运河边的石沿上坐下来吃**——因为在这个世界，吃东西就是要坐下（`food.004` / `myth.019`）。运河里有人在钓鱼（`travel.003`）。

### 上午（认路 · 看人怎么活）
沿运河走，**每过一座桥就换一个区**（`travel.002`）。
**贸易区**：正对喷泉的**列柱石砌银库**（`house.011` ⚠️）、中央的拍卖行、西南侧的邮箱、东侧坡道上去的**狮鹫栖木**（`travel.005`）——木架上停着狮鹫，管理员在旁；有人递钱上鞍飞走（`travel.006`）。奶酪铺 Trias' Cheese 里**一对夫妇带一个少年学徒**（`food.005`）。
**矮人区**：一进去就是**散不掉的烟霭和不停的锤声**（`travel.008`），再往东是**深铁矿道的隧道口**——免费的地下电车，直通铁炉堡（`travel.007` / `myth.020`）。
**教堂广场**（全城最高处）：**大教堂前的喷泉雕像是阿隆索斯·法奥，不是乌瑟尔**（`myth.005` —— 最隐蔽的坑）；旁边是孤儿院和**在给全城人口做普查的市政厅**（`house.012` ⚠️）。
**公园区**（Vanilla 完好）：**中央一口暗夜精灵的月井**，树下有暗夜精灵在歇息（`myth.002`）——这是她第一次看到「这城里不止住着人类」。

### 中午（人最挤的时候 · 第二顿）
**正午的贸易区挤到难以移动**（`travel.001` ⚠️）。她穿过人流去**法师区**——地面从石板过渡成**长着蕈子和小花的厚草地**（`travel.004` ⚠️）。
第二顿在**蓝色隐士**——全城唯一有**主厨 + 学徒厨师**、被官方称作 restaurant 的地方（`food.014`），菜单上有一路「河汊沼泽」风味的乡土菜。坐下吃（`myth.019`）。
饭后经过**已宰的羔羊**——门里空荡阴冷，只有酒保 Jarel Moor 一个人，劝她「离阴影远点」（`house.010`）。她没进去。

### 下午（旧城区 · 落差）
过桥进**旧城区**，一眼就看出换了地方：街窄、墙斑驳、比别处**脏得多也臭得多**，墙根坐着穷人（`house.008` / `myth.021`），屋顶是**暗红褐色**不是蓝色（`house.009` ⚠️）。
**猪和哨声**在这里——**但她不能住这儿**（Vanilla 它只是酒馆，`house.003` / `myth.018`）。她进去喝一杯：吧台后的 Reese Langston 招呼「Grab a drink my friend and pull up a seat」（`food.008`），女招待 Elly 在桌间走动，角落里 Bartleby 已经趴下了（`house.004`）。台上并排是**瓶 / 皮囊 / 扁壶 / 大酒壶 / 罐**五种酒器（`food.010` / `myth.024` ⚠️）。她要最便宜那瓶红酒（50 铜，`food.013`）。炉边**Stephen Ryback 守着一整排烤肋排**——全城唯一有名有姓的熟食（`food.015` ⚠️），她也要了一份，这算第三顿。

### 傍晚 → 夜（住下）
回**贸易区的镀金玫瑰**——**Vanilla 全城唯一的旅店**（`house.001` / `myth.018`），夹在银行和拍卖行之间。店主 Allison 站在一楼堂屋：「Welcome to my Inn, weary traveler.」（`house.002`）。她说了两句就住下了——**没掏钱、没登记、没有柜台**（`house.005` ⚠️ / `myth.023` ⚠️）。
夜里的城不是死的：**卫兵提着油灯巡夜**（`travel.012`），**法师区的奥术灯柱亮着**（`travel.004` ⚠️），矮人区的工坊还在开工（`house.013` ⚠️），**没有宵禁**（`travel.015` ⚠️）。抬头——**天空是空的**：除了卫兵的狮鹫，没有任何飞行坐骑（`myth.010` ⚠️）。

### 次晨（打分）
天亮（这个世界跟真实时间一样转 24 小时，`travel.014` ⚠️）。她给这一晚打分，**最能拿来说的一条是：一个铜板都没花**——住店免费，坐电车去铁炉堡也免费，**但坐狮鹫飞出城要钱**（`house.005` / `travel.007` / `travel.006`）。
> **注意**：「免费」这件事在剧本里只能说成「我没花一个铜板」这种**亲历口吻**，不能说成「这里规定住宿免费」——因为那是沉默证据不是明文（见 `house.005` note）。

---

## §7 旅店卡

> **⚠️ 全部中文译名标 `ai_draft`**：灰机 wiki（warcraft.huijiwiki.com，国服译名对齐站）对本次抓取全部返回 HTTP 403，只拿到搜索摘要，且摘要里同一家店出现了两种写法（「镀金玫瑰」／「镶金玫瑰」、「猪和哨笛」／「猪和哨声」、「已宰的羔羊」／「挨宰的羔羊」）。**须人眼在国服客户端或灰机 wiki 核定一个写法再进 prompt / 口播。**

### ① The Gilded Rose ——「镀金玫瑰」／「镶金玫瑰」⚠️
| 项 | 内容 | 出处 |
|---|---|---|
| 区 | 贸易区，夹在银行与拍卖行之间，紧邻邮箱 | `house.001` ✅ |
| 老板 | Innkeeper Allison，就在一楼门内；招呼语「Welcome to my Inn, weary traveler. What can I do for you?」 | `house.002` ✅ |
| 身份 | **Vanilla 时期暴风城唯一的 inn** | `house.001` / `myth.018` ✅ |
| 兼营 | 食物与饮料商人（面包 / 水果 / 饮料三类） | `house.001` ✅ |
| 住宿费 | **没有任何来源记载收费**；绑炉石免费，炉石丢了免费补 | `house.005` ⚠️ |
| 内部形制 | **未查到任何文字记载**（wiki 只挂内景图） | `house.006` ⚠️ |

### ② Pig and Whistle Tavern ——「猪和哨声」／「猪和哨笛」酒馆 ⚠️
| 项 | 内容 | 出处 |
|---|---|---|
| 区 | 旧城区 [76.9, 52.9] | `house.004` ✅ |
| 老板 | Reese Langston（Tavernkeeper，**不是 Innkeeper**）；招呼语「Welcome to the Pig and Whistle! Grab a drink my friend and pull up a seat, the more the merrier!」 | `food.008` ✅ |
| 身份 | **Vanilla 是酒馆，不是旅店**——旅店老板 Maegan Tillman 是 4.0.1（2010）才加的 | `house.003` / `myth.018` ✅ |
| 其他人 | 女招待 Elly Langston（兼饮料商人）、David Langston、醉汉常客 Bartleby、Harry Burlguard | `house.004` ✅ |
| 厨 | 烹饪训练师 Stephen Ryback（以自家配方的整排烤肋排闻名）、烹饪材料商 Erika Tate | `food.015` ⚠️ |
| 住宿费 | **不提供住宿** | `myth.018` ✅ |
| 内部形制 | **未查到文字记载**；能确定的只有：吧台、桌凳、五种酒器、一个趴下的醉汉、一处烤肋排的炉 | `house.006` ⚠️ |

### ③ The Blue Recluse ——「蓝色隐士」⚠️
| 项 | 内容 | 出处 |
|---|---|---|
| 区 | 法师区 | `food.014` ✅ |
| 身份 | **既是 tavern 也是 restaurant**，在懂魔法的人里很受欢迎，以「看上去很上档次的氛围」闻名全世界 | `food.014` ✅ |
| 人 | 主厨 Angus Stern、学徒厨师 Connor Rivers、酒保 Joachim Brenlow；Steven Lohan（**retail 头衔是 innkeeper，Vanilla 头衔未查**） | `food.014` ✅ / ⚠️ |
| 菜 | 一份菜单满是带「bayou（河汊沼泽）」风味的乡土菜 | `food.014` ✅ |
| 住宿费 | **Vanilla 是否能住未查**——因 `house.003` 明写 4.0.1 时猪和哨声才是「第二家旅店」，**推论 Vanilla 时蓝色隐士也不是 inn** ⚠️ | 推论 |
| 内部形制 | **未查到文字记载** | `house.006` ⚠️ |

### ④ The Slaughtered Lamb ——「已宰的羔羊」／「挨宰的羔羊」⚠️
| 项 | 内容 | 出处 |
|---|---|---|
| 区 | 法师区（中文来源给的坐标 [42.2, 81.9] ⚠️） | `house.010` ✅ |
| 身份 | 「seedy pub」——下三滥的小酒馆 | `house.010` ✅ |
| 人 | 酒保 Jarel Moor，楼上空荡荡只有他一个，劝客人「stay away from the shadows」 | `house.010` ✅ |
| 地下 | 地下墓穴是暴风城术士的密所，有术士新兵的训练场 | `house.010` ✅ |
| 住宿费 | **不提供住宿** | `house.010` |
| 内部形制 | **未查到文字记载**；能确定的只有：空、冷、暗、有下行的口 | `house.006` ⚠️ |

---

## §8 误传黑名单总表

> **这张表下游直接变成全站负向词库。** 排镜 / 出 prompt 时逐条挂。
> 「正确的是什么」一栏若为空，表示 Vanilla **就是没有这个东西**，不需要替代物。

| # | 误传内容 | 正确的是什么（Vanilla） | 负向词 | fact_id |
|---|---|---|---|---|
| 1 | 暴风城有港口、码头、船 | **没有**。港口是 3.0.2（2008-10-14）才加的；Classic 的联盟船只从黑海岸 / 米奈希尔港开 | `暴风城港口, 码头, 栈桥, 泊位, 帆船, 桅杆, 船帆, 缆绳, 船锚, 水手, 跳板, 货箱堆场, 灯塔, 海鸥, 海浪拍岸` | `myth.001` `travel.009` |
| 2 | 公园区是焦黑废墟 / 塌陷巨坑 | 公园**完好**，中央一口暗夜精灵的**月井**，暗夜精灵在此歇息，是东部王国唯一的德鲁伊训练师所在 | `公园废墟, 焦黑巨坑, 塌陷地面, 爪痕, 断柱残垣, 冒烟的瓦砾, 狮王之息, Lion's Rest` | `myth.002` |
| 3 | 瓦里安国王在位 / 王座上是他 | 瓦里安**失踪**；摄政是博瓦尔·弗塔根，顾问是凯特拉娜·普瑞斯托（＝奥妮克希亚伪装），幼年安度因王子 | `瓦里安·乌瑞恩, Varian Wrynn, 双持巨剑的国王, 狼首铠甲, 成年国王坐在王座上` | `myth.003` |
| 4 | 要塞门前有瓦里安雕像的高耸喷泉、露天步道 | **没有**。要塞在 4.0.3a 被里外整个重做，通往王座厅的是室内通道 | `瓦里安雕像喷泉, 露天宏大步道, 重做后的王座厅, 俯瞰暴风湖的花园` | `myth.004` |
| 5 | 教堂广场喷泉上是**乌瑟尔** | 是**阿隆索斯·法奥**（教士形象），乌瑟尔是大地裂变才换上去的 | `乌瑟尔雕像, Uther the Lightbringer, 持战锤的圣骑士雕像, 「A righteous Paladin」铭牌` | `myth.005` |
| 6 | 英雄谷有雕像倒在水里 / 塔楼有巨大爪痕 | **五尊雕像全部完好直立**（图拉扬、奥蕾莉亚、卡德加、库德兰、达纳斯），塔楼墙面干净 | `倒塌的雕像, 掀翻进水里的石像, 塔楼上的巨大爪痕, 灼烧痕迹, 焦黑墙面, 缺角的石像` | `myth.006` |
| 7 | 有「暴风城大使馆」 | **没有**。7.3.5（2018）才加 | `暴风城大使馆, Stormwind Embassy, 各族旗帜并列的会馆, 盟约种族代表团` | `myth.007` |
| 8 | 有「狮王之息」纪念广场 | **没有**。7.0.3（2016）建在公园废墟上 | `狮王之息, Lion's Rest, 水边的纪念广场, 沉在水里的国王石棺, 纪念墙` | `myth.008` |
| 9 | 法师塔里是整排传送门的大厅 | **不画传送门大厅**。现行的传送门大厅是 8.1.5 整合的 | `传送门大厅, 一排排发光的传送门, 环形传送门厅, 各地地标浮现在门里` | `myth.009` |
| 10 | 天上飞满飞行坐骑 | **天空是空的**——只有卫兵的狮鹫巡逻与狮鹫栖木的起降。飞行坐骑是 TBC 才有且只限外域 | `满天飞行坐骑, 龙, 飞行扫帚, 飞行地毯, 悬停在广场上空的坐骑, 空中交通` | `myth.010` |
| 11 | 画成地球中世纪城堡 / 米那斯提力斯 / 通用奇幻王城 | **白石墙 + 蓝色板岩屋顶 + 狮子纹章**三件套；城垛上有石狮，大门两侧各一个巨大石狮首 | `灰褐色石城, 白色多层阶梯城, 米那斯提力斯, 通用中世纪城堡, 哥特尖顶群, 城堡吊桥铁闸, 红瓦屋顶, 茅草屋顶` | `myth.011` |
| 12 | 纹章配色画错 | ⚠️ **正向配色须人眼看战袍图定色名**；只有负向可用 | `红底纹章, 绿底纹章, 黑底纹章, 双头鹰, 十字纹, 百合花纹, 随机家徽` | `myth.012` |
| 13 | 画成积了几百年灰的千年古城 | 它是**刚重建不久的新城**（石匠公会在第二次战争后重建）；只有旧城区该有旧感 | `千年古城的风化墙面, 爬满藤蔓的石墙, 断裂的古老雕像, 苔藓覆盖的石阶, 废墟感` | `myth.013` |
| 14 | 画成游戏截图 / 卡通渲染，或完全写实的欧洲石城 | **半写实**：形制配色照游戏，材质光线走写实 | `游戏截图, 游戏引擎渲染, UI 界面, 血条, 名字牌, 低多边形, 卡通渲染, 赛璐璐描边, 塑料高光, 过饱和, 3D 建模预览, 白模, 灰模` | `myth.014` |
| 15 | 招牌上写现代印刷体英文 / 乱码文字 | 店招是**吊挂的图形木牌**（⚠️ 正向待人眼核） | `印刷体英文招牌, 乱码文字, 伪英文, 霓虹灯招牌, LED 字, 中文招牌, 手写体价目牌, 二维码, 条码` | `myth.015` |
| 16 | 街上有德莱尼 / 血精灵 / 狼人 / 熊猫人 | **只有人类、矮人、侏儒、暗夜精灵**四族；人类为主体，矮人侏儒在矮人区，暗夜精灵在公园 | `德莱尼, 蓝皮肤大角种族, 血精灵, 狼人, 熊猫人, 虚空精灵, 地精, 狐人` | `myth.016` |
| 17 | 街上有部落种族闲逛 | **没有**。卫兵对部落敌对，一靠近就打 | `兽人, 巨魔, 牛头人, 亡灵, 部落旗帜, 部落纹章, 两族和平共处的街景` | `myth.017` |
| 18 | 在猪和哨声住宿 | **Vanilla 全城只有镀金玫瑰一家旅店**；猪和哨声的旅店老板是 4.0.1 才加的 | `猪和哨声的旅店老板, Maegan Tillman, 在猪和哨声住宿, 酒馆二楼客房` | `myth.018` |
| 19 | 站着吃 / 边走边吃 | **进食必须坐下**（三件食物道具逐字相同的机制文字） | `站着吃, 边走边啃, 快走中咬一口, 单手举着食物走路, 站着喝, 走路喝水` | `myth.019` |
| 20 | 深铁矿道画成蒸汽火车 / 现代地铁 | **免费的地下有轨电车**，矮人区东侧隧道进 | `蒸汽火车, 煤烟, 汽笛, 蒸汽喷发, 铁轨道砟, 枕木, 地铁闸机, 售票窗口, 电子显示屏, 广播报站, 车票` | `myth.020` |
| 21 | 旧城区画得和贸易区一样光鲜 | 旧城区**更脏更臭更旧**，穷人 / 乞丐 / 小偷居住区，暗红褐色屋顶 | `和贸易区一样整洁的旧城区, 新铺石板路, 干净白墙, 统一立面, 光鲜商铺` | `myth.021` |
| 22 | 混入现代元素 | 照明只有**油灯（卫兵夜巡）+ 奥术灯柱（法师区）+ 屋内炉火** | `电灯, 路灯杆, 灯泡, 灯罩, 霓虹, LED, 玻璃幕墙, 平板玻璃窗, 金属栏杆, 交通指示牌, 井盖, 沥青路面, 水泥, 空调外机, 电线, 电线杆, 工业砖烟囱` | `myth.022` |
| 23 | 旅店画成现代酒店大堂 | 进门就是堂屋，店主站在一侧，**说两句话就住下了** | `酒店前台, 柜台, 登记簿, 房卡, 房号牌, 钥匙牌墙, 行李寄存, 铃铛按钮, 电梯, 大堂沙发` | `myth.023` |
| 24 | 酒器画成玻璃扎啤杯 | **瓶 / 皮囊 / 扁壶 / 带盖大酒壶 / 罐**五种并存（⚠️ 材质本身无记载，别把「玻璃」整个禁掉） | `玻璃扎啤杯, 啤酒杯, 玻璃高脚杯, 吸管, 易拉罐, 瓶盖, 品牌酒标` | `myth.024` |
| 25 | 用后改名的道具名口播 | Vanilla 名：**Flask of Port**（非 Stormwind Tawny）、**Bottle of Pinot Noir**（非 Dalaran Noir）、**Flagon of Mead**（Classic 客户端作 Flagon of Dwarven Honeymead） | `Flask of Stormwind Tawny, Bottle of Dalaran Noir, Flagon of Dwarven Mead（作为 Vanilla 口播名）` | `food.011` `food.012` `food.013` |
| 26 | 卖 Vanilla 之后才有的食物饮料 | Vanilla 面包只到 **Homemade Cherry Pie（40 银）**；饮料只到 **Morning Glory Dew（40 银）**——之后的档位（Mag'har Grainbread / Filtered Draenic Water 及以上）全是 TBC 之后的 | `Mag'har Grainbread, Crusty Flatbread, Frybread, Filtered Draenic Water, Honeymint Tea, Cobo Cola, Pungent Seal Whey` | `food.003` `food.009` |

---

## §9 未查 / Open questions

**必须补的（会直接影响画面，建议优先）**

1. **旅店 / 酒馆 / 民居的内部形制** —— 床铺样式、被褥、通铺还是私人房、桌椅、餐具材质、照明。**所有文字源一律有图无字**（`house.006` / `house.014`）。**建议做法：请用户在 Classic 客户端里对四家店 + 一间民居各截 3–5 张内景图**，作为参考图入库，而不是让模型自由发挥——后者必然掉进 `myth.011`（中世纪化）与 `myth.023`（现代酒店化）。
2. **官方中文译名** —— 灰机 wiki 403，四家店名各有两种写法（§7 表头）；分区中文名（贸易区 / 旧城区 / 法师区 / 矮人区 / 教堂广场 / 运河 / 公园 / 暴风要塞 / 英雄谷）也只有搜索摘要。**须人眼核定并写进项目的译名对照表，此后全剧一致。**
3. **暴风城纹章的准确配色** —— 「蓝底金狮」本次**未查到任何文字出处**（`myth.012`）。须人眼看战袍图，按 `ai_video.md` 的锁定色名写死（零 hex）。
4. **城内能不能骑马** —— wiki 的 Mount 页只写飞行禁区，无地面坐骑的城内规则（`travel.016`）。**保守方案已给**（街上极少数人骑马），但若要拍旅行者骑行须先核。
5. **阿隆索斯·法奥雕像长什么样** —— 只知道 Vanilla 的教堂广场喷泉上是他不是乌瑟尔（`myth.005`），但雕像形制未查。这是必经之地的构图中心，值得补。

**次要（影响口播准确性，不影响画面对错）**

6. **Vanilla 的精确售货清单** —— 本文的档位是从 retail 清单靠等级门槛 + 改名 patch history 反推的（`food.003` / `food.009` / `food.010`）。Wowhead Classic 的 vendor 表是 JS 渲染、WebFetch 取不到。**建议直接在 Classic 客户端里对 Thomas Miller / Innkeeper Allison / Reese Langston 三个 NPC 各截一张 vendor 窗口图**，一次解决。
7. **`Jug of Badlands Bourbon` / `Skin of Dwarven Stout` 是否也在 5.3.0 被改过名** —— 另外三样都改了（`food.011`–`013`），这两样未查。
8. **Vanilla 的暴风城航线目的地清单** —— 只拿到搜索摘要（铁炉堡、米奈希尔港、Thelsamar、Thorium Point、Morgan's Vigil…），且其中 Thorium Point / Morgan's Vigil 是 Vanilla 中后期补丁才加的，**未逐条核 patch**。
9. **贸易区的拍卖行在 Vanilla 早期是否存在** —— Trade District 页写「Patch 1.9 added the linked Auction House in the center of the Trade District」（ai_read），但搜索里有「1.9 把拍卖行**带回**暴风城」的说法，两者矛盾。**1.9 之前贸易区有没有拍卖行未定**（本剧若锚点在 1.9 之后则无影响）。
10. **Gryphon Roost 的 Tannec Stonebeak / Bralla Cloudwing 是否在 Vanilla 就存在** —— 只查到他们现在在那儿（`travel.005`）。
11. **The Blue Recluse 在 Vanilla 是否能住宿** —— 本文按 `house.003`「4.0.1 才有第二家 inn」推论为「不能」，但这是推论不是查实（§7 ③）。
12. **监狱的位置表述冲突** —— 一处写「运河区地下」、一处写「从法师区进入」（`travel.013`）。判为伪冲突，但未最终确认。
13. **Vanilla 的法师塔里有没有零星的常驻传送门** —— 只查实了「8.1.5 做了整合」，没查实「Vanilla 有没有」（`myth.009`）。
14. **店招到底是图形还是文字** —— 店名作为子区域名确实存在（`myth.015`），但招牌形制未查。

---

## §10 统计

> 下表数字由 `grep` 对本文件实际计数得出，非手数。复核命令：
> `grep -c "^- fact_id:" w6_daily_blacklist.md`；`grep "^  verified_by:" … | sort | uniq -c`（tag / tier 同法）。

| 项 | 数 |
|---|---|
| 事实总数 | **70**（目标 ≥35 ✅） |
| ├ `stormwind.food.NNN` | 16 |
| ├ `stormwind.house.NNN` | 14 |
| ├ `stormwind.travel.NNN` | 16 |
| └ `stormwind.myth.NNN` | **24**（目标 ≥15 ✅） |
| `verified_by: ai_read` | **57**（目标 ≥28 ✅） |
| `verified_by: ai_draft` | 13 |
| `verified_by: human` | 0（本 worker 无法升级，须人眼抽查后升） |
| tag `✅` | 28 |
| tag `⚠️` | 25 |
| tag `❌` | 17 |
| tier `T0`（暴雪官网 / 游戏本体） | 7 |
| tier `T1`（warcraft.wiki.gg / wowpedia / Wowhead） | 60 |
| tier `T2`（wiki 上标注 non-canon 的 RPG 设定） | 1 |
| tier `T3`（同人游记，仅作氛围） | 2 |

字段完整性：70 条全部带 `source_url` / `quote` / `prompt_string` / `negative`（各 70，`grep -c` 核过）。
误传黑名单 24 条中，`❌`（Vanilla 确定没有 / 确定是别的样子）17 条、`⚠️`（画风契约与模型默认坑，非外部事实）7 条。

**本次实际打开并取到正文的页面（35 个）**：Stormwind City / Gilded Rose / Pig and Whistle Tavern / Stormwind Harbor / Innkeeper Allison / Thomas Miller / Trade District / Trias' Cheese / Reese Langston / Elling Trias / Flask of Stormwind Tawny / Old Town / The Stockade / Flagon of Dwarven Mead / Innkeeper / Gryphon Roost / The Slaughtered Lamb / Dwarven Mild / Stormwind City Guard / Cathedral Square / Alonsus Faol / Park / Freshly Baked Bread / Shiny Red Apple / Bottle of Dalaran Noir / Mage Quarter / Dwarven District / The Blue Recluse / Stormwind Keep / Bolvar Fordragon / Stormwind (kingdom) / Mount / Bread vendors（无内容）/ Cheese vendors / Fruit vendors（无内容）；暴雪官网 2 篇（Welcome to Stormwind: A Guided Tour、WoW Classic: Getting around Azeroth）；同人游记 1 篇（destron.blogspot）。

**抓取失败的**：warcraft.huijiwiki.com（403 × 2，中文译名）；vanilla-wow-archive.fandom.com（402 × 2）；classic-wow-archive.fandom.com（402）；wowhead.com/classic（JS 渲染，取不到 vendor 表）。
