---
worker_id: researcher-w9-player-memory
stage: 0
role: researcher
angle: player-memory
status: complete
blockers: []
confidence: high
---

# W9 · 玩家共同记忆的场景与仪式（版本锚点＝经典旧世 Vanilla / WoW 1.x；世界内当下＝ Year 25 ADP）

## 本路说明（下游必读）

1. **本路问的不是「设定对不对」，而是「老玩家站过没有」。** W8 查的是「那天发生了什么」，
   W1 查的是「城长什么样」。本路查的是**一个玩过 Vanilla 联盟角色的人，在暴风城必然做过的动作
   与必然站过的地方**——它决定这一站的情感钩子，也决定哪些镜是「观众会在弹幕里刷"我站过"」的镜。

2. **两类证据严格分开。**
   - **机制/设定类**（炉石怎么绑、地铁跑多久、监狱在哪、铭文写什么）走 T0/T1，可标 `✅`。
   - **玩家主观怀念**（「铁炉堡才是首都」「公园区最安静」「贸易区最吵」）一律 `⚠️` + `tier: T3` +
     `source` 写明**玩家社区**。**本文没有一条把玩家怀旧说法写成设定明载。**

3. **版本闸门比别的路更紧。** 玩家记忆是跨 20 年累积的，里面**混了大量后续资料片的东西**
   （港口 / 传送门大厅 / 贸易区骑术训练师 / 猪和哨声的旅店老板 / 雄狮之眠 / 集合石当召唤石用）。
   凡不是 Vanilla 的，我一律挑进 § 不可用清单，正片不得出现。**尤其注意三条高频误植**：
   ① 巫师圣殿的**传送门大厅是 8.1.5 才有的**，旧世那座塔里只有法师训练师；
   ② **猪和哨声在旧世没有旅店老板**，全城**只有镀金玫瑰一家能绑炉石**；
   ③ **集合石在旧世不是召唤石**，它是「自动帮你凑队」的东西，2.0.1 才变成召唤。

4. **一个对本项目特别有利的巧合**：Warcraft Wiki 的矿道地铁条目写的是
   「**By the Year 25 ADP, the rat problem remained and was handled by Monty.**」——
   **Year 25 ADP 正是本片的世界内当下**。地铁里的老鼠与灭鼠工 Monty 是**当下时态**的设定明载，
   艾拉可以直接对镜讲「现在这条隧道里还在闹老鼠，那边那位就是灭鼠的」。

5. **当地人零台词（系列铁律）。** 下面每条「艾拉能讲什么」都是**艾拉自己对镜说**的方向，
   NPC 一律不出声。老鼠、灭鼠工、旅店老板、卫兵都只出画面与环境音。

6. **来源损失**：`*.fandom.com` 全站对本机返回 **HTTP 402**（Wowpedia / Vanilla WoW Wiki /
   WoWWiki 三个镜像都进不去）；Wowhead Classic 的 NPC / zone 页是 JS 渲染，抓回来是空壳
   （Nessy 的 `npc=10942` 只拿到 "The location of this NPC is unknown."）；
   `massivelyop.com` 403、`rpgamer.com` 403、`dvorakgaming.com` DNS 解析失败；
   `blizzardwatch.com` 的图集页正文是懒加载抓不到。所有需要它们的条目我都改用
   `warcraft.wiki.gg` 的 `?action=raw` 原始 wikitext 取证（这条路最稳，建议下游沿用）。

---

## 事实注册表

### A. 玩家仪式——每个联盟玩家都做过的事

```yaml
- fact_id: stormwind.lore.001
  claim: 炉石（Hearthstone）是 2004 年 4 月 13 日的 0.6 版就加进游戏的元老级物品，旧世每个角色都随身带着它。
  tag: ✅
  source: Warcraft Wiki — Hearthstone, §Patch history
  source_url: https://warcraft.wiki.gg/wiki/Hearthstone
  quote: "Patch 0.6 (2004-04-13): Added."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一枚掌心大小的灰白石片，表面刻着一圈同心的符文凹槽，边缘被摩挲得发亮，用麻绳穿孔挂在腰带上"
  negative: "发光宝石, 水晶球, 金属护符, 现代钥匙扣, 卡牌"

- fact_id: stormwind.lore.002
  claim: 绑炉石的动作是走到旅店老板面前，在对话里点那句「把这家旅店设为你的家」——这是全体联盟玩家最强的共同肌肉记忆。
  tag: ✅
  source: Warcraft Wiki — Hearthstone（旧措辞，2025-12-02 的 11.2.7 才改成现在这句）
  source_url: https://warcraft.wiki.gg/wiki/Hearthstone
  quote: "Make this inn your home."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旅行者站在旅店柜台前与老板交谈，柜台后是酒桶与挂排的铜壶，壁炉暖光从侧面打来"
  negative: "现代前台, 电脑, 登记簿签字, 钥匙卡"

- fact_id: stormwind.lore.003
  claim: 炉石的说明文字写的是「把你送回家所在地；到别处跟旅店老板说话可以改绑」。
  tag: ✅
  source: Warcraft Wiki — Hearthstone, §Item usage
  source_url: https://warcraft.wiki.gg/wiki/Hearthstone
  quote: "Use: Returns you to <home location>. Speak to an Innkeeper in a different place to change your home location."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "手掌摊开托着一枚刻符文的石片，石片凹槽里浮出极淡的暖光，人物周身起一圈缓慢上升的光屑"
  negative: "强烈光柱, 爆炸特效, 传送门漩涡, 蓝色科技光"

- fact_id: stormwind.lore.004
  claim: 用炉石要站着念满 10 秒，中途挨打就断——所以旧世玩家的记忆里总有「差一秒被打断」这件事。
  tag: ✅
  source: Warcraft Wiki — Hearthstone, §Item usage details
  source_url: https://warcraft.wiki.gg/wiki/Hearthstone
  quote: "The casting process requires 10 seconds and will be interrupted if you take damage."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "人物原地站定不动，双手在身前合握，脚下地面浮出一圈缓慢旋转的符文环，环随读条逐格点亮"
  negative: "奔跑中使用, 骑马中使用, 瞬间消失"

- fact_id: stormwind.lore.005
  claim: 炉石的冷却时间到 2009 年 4 月 14 日的 3.1.0 才被砍到 30 分钟——也就是说**经典旧世是一小时一次**，这是旧世「回城很贵」的核心体感。
  tag: ✅
  source: Warcraft Wiki — Hearthstone, §Patch history（3.1.0 明写「reduced to 30 minutes」，故此前为更长；玩家社区一致记为 1 小时）
  source_url: https://warcraft.wiki.gg/wiki/Hearthstone
  quote: "Patch 3.1.0 (2009-04-14): The cooldown reduced to 30 minutes."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石片表面的符文凹槽全部黯淡无光，像烧尽的炭，握在手里只是一块凉石头"
  negative: "发光, 裂纹, 碎裂, 计时器数字"

- fact_id: stormwind.lore.006
  claim: 绑炉石的那位是镀金玫瑰旅店的老板娘 Innkeeper Allison，位置在贸易区 [60.6, 75.0]，正好夹在银行和拍卖行中间。
  tag: ✅
  source: Warcraft Wiki — Innkeeper Allison
  source_url: https://warcraft.wiki.gg/wiki/Innkeeper_Allison
  quote: "Innkeeper Allison operates from the Gilded Rose Inn in Stormwind City's Trade District, situated between the bank and auction house at coordinates [60.6, 75.0]."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旅店一层柜台后站着一位人类中年女性店主，深色长裙配围裙，身后木架摆满面包、苹果与陶罐饮料"
  negative: "年轻少女形象, 华服, 武器, 酒吧女郎打扮"

- fact_id: stormwind.lore.007
  claim: 她的招呼语是「欢迎光临小店，风尘仆仆的旅人。有什么能为你效劳的？」——老玩家听到这句就知道自己到家了。
  tag: ✅
  source: Warcraft Wiki — Innkeeper Allison, §Quotes
  source_url: https://warcraft.wiki.gg/wiki/Innkeeper_Allison
  quote: "Welcome to my Inn, weary traveler. What can I do for you?"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "店主抬头对进门的人微笑并微微欠身，门口逆光把旅人剪成暗影，室内是壁炉的暖橙光"
  negative: "冷光, 空无一人的店堂, 顾客背对镜头"

- fact_id: stormwind.lore.008
  claim: 镀金玫瑰之所以成为全服默认绑点，是因为它离银行、拍卖行和一个邮箱都只有几步——这四样东西挤在贸易区西南角一小块地方。
  tag: ✅
  source: Warcraft Wiki — Gilded Rose
  source_url: https://warcraft.wiki.gg/wiki/Gilded_Rose
  quote: "a popular resting point for travelers passing through the human capital of Stormwind City due to its proximity to the bank, Auction House, and an ever-popular mailbox."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一小片街区里并排立着三栋石砌建筑：挂着玫瑰招牌的旅店、厚重铁门的银行、门口人来人往的拍卖行，街心一根石柱上嵌着投信口"
  negative: "分散在城市各处, 空旷广场, 现代邮筒"

- fact_id: stormwind.lore.009
  claim: 旧城区「猪和哨声」在经典旧世**没有旅店老板**——它的老板娘 Maegan Tillman 是 4.0.1 才加的，加的时候被称作「暴风城的第二家旅店」。因此旧世全城只有镀金玫瑰一家能绑炉石。
  tag: ✅
  source: Warcraft Wiki — Pig and Whistle Tavern
  source_url: https://warcraft.wiki.gg/wiki/Pig_and_Whistle_Tavern
  quote: "Maegan Tillman ... was added in Patch 4.0.1, making this Stormwind's second inn."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旧城区窄巷里一间挂木招牌的酒馆，门口堆着空酒桶，里面只有酒保和厨子，没有柜台登记处"
  negative: "旅店老板, 楼上客房编号, 炉石绑定"

- fact_id: stormwind.lore.010
  claim: 连城里的卫兵都不把猪和哨声当「旅店」指路——问路时他们只会把你指去镀金玫瑰。
  tag: ✅
  source: Warcraft Wiki — Pig and Whistle Tavern
  source_url: https://warcraft.wiki.gg/wiki/Pig_and_Whistle_Tavern
  quote: "Stormwind's guards do not guide players to the Pig and Whistle as a usable inn"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "披蓝色狮徽罩袍的卫兵持长戟立在街角，抬手朝一个方向指，手臂延长线指向远处的旅店招牌"
  negative: "卫兵坐着, 卫兵无视路人, 现代警察手势"

- fact_id: stormwind.lore.011
  claim: 矿道地铁是侏儒工程造的、全封闭、部分在水下的双轨地下铁，两列各三节车厢往返跑，**免费乘坐**。
  tag: ✅
  source: Warcraft Wiki — Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The Deeprun Tram (or simply the Tram) is a long, fully enclosed, underground (and partially underwater) set of double tracks upon which rolls two sets of three wagons, all credited to the gnomes' technical engineering."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "铆接钢板与铜管构成的地下隧道，双轨并行，三节连挂的开放式车厢停在月台边，车头是黄铜与齿轮"
  negative: "现代地铁, 玻璃幕门, 电子屏, 蒸汽机车烟囱, 单轨"

- fact_id: stormwind.lore.012
  claim: 单程 60 秒，到站停 12 秒——这一分钟是旧世玩家挂机、喝水、聊天的固定一分钟。
  tag: ✅
  source: Warcraft Wiki — Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The transit time between each end is 60 seconds and remains at each stop for 12 seconds."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "车厢内侧跟机位，乘客抓着立柱随车身轻晃，隧道壁灯以固定节奏一盏盏向后掠过"
  negative: "车厢空无一人, 高速模糊, 车窗外是地面风景"

- fact_id: stormwind.lore.013
  claim: 这条地铁是暴风城与铁炉堡之间**唯一一条永久直连**——从暴风城没有任何传送门能去铁炉堡。
  tag: ✅
  source: Warcraft Wiki — Ironforge
  source_url: https://warcraft.wiki.gg/wiki/Ironforge
  quote: "it represents the only direct permanent connection between these two major Alliance cities, as Ironforge cannot be reached via portal from Stormwind itself."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "矮人区东侧一个巨大的齿轮形隧道口，轨道从口中延伸进黑暗，口沿刻着侏儒工程铭牌"
  negative: "魔法传送门, 飞艇, 船坞, 自然洞穴口"

- fact_id: stormwind.lore.014
  claim: 经典旧世的拍卖行**按城市各自独立**，三座联盟拍卖行（铁炉堡 / 暴风城 / 达纳苏斯）挂的是三池不同的货；直到 2006 年 1 月 3 日的 1.9.0 才把它们并成同一池。
  tag: ✅
  source: Warcraft Wiki — Auction house, §Patch 1.9.0 原文
  source_url: https://warcraft.wiki.gg/wiki/Auction_house
  quote: "Auction Houses in Orgrimmar, Undercity, and Thunder Bluff will now share the same pool of Horde player-created auctions, and Alliance players will find the same to be true when visiting Ironforge, Stormwind City, and Darnassus Auction Houses."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "大厅内一排高脚木台后站着拍卖师，台面堆着卷轴与账本，台前围着挤挤挨挨的顾客，墙上挂着一块块木质告示板"
  negative: "电子屏幕, 竞价槌台, 现代交易所, 空荡大厅"

- fact_id: stormwind.lore.015
  claim: 挂拍要先交押金（按 12/24/48 小时分别是商店售价的 15%/30%/60%），卖出后拍卖行再抽走成交价的 5%。
  tag: ✅
  source: Warcraft Wiki — Auction house, §Deposit and fees
  source_url: https://warcraft.wiki.gg/wiki/Auction_house
  quote: "House cut on successful sales: 5% of the winning bid"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "顾客把一小堆铜币推过柜台，拍卖师用铜秤称过后记入账本，铜币在台面上散开"
  negative: "刷卡, 纸币, 收据打印, 保险柜"

- fact_id: stormwind.lore.016
  claim: 暴风城的拍卖行建筑今天叫「Trader's Hall」，但这个名字是 4.0.3a 改的——**旧世时它不叫这个名字**。
  tag: ✅
  source: Warcraft Wiki — Trader's Hall
  source_url: https://warcraft.wiki.gg/wiki/Trader%27s_Hall
  quote: "renamed to Trader's Hall"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区街心一栋敞开式石砌大厅，正面是三道连拱门洞，门内可见木质柜台与人群"
  negative: "刻着 Trader's Hall 字样的招牌, 现代店招, 玻璃门"

- fact_id: stormwind.lore.017
  claim: 贸易区的银行叫 Stormwind Counting House，1.1.0 就在了，业务是「开户 + 贵重物品保险箱」。
  tag: ✅
  source: Warcraft Wiki — Stormwind Counting House
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Counting_House
  quote: "We offer financial accounts and safety deposit boxes for valuable items."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌方正建筑，正门是包铁厚木门，门内一排柜台与身后成列的铁柜格，柜格上刻编号"
  negative: "现代银行大堂, 防弹玻璃, ATM, 金库转盘门"

- fact_id: stormwind.lore.018
  claim: 银行、邮箱、旅店三样挤在贸易区的西南一侧——这解释了为什么玩家一进城就直奔那个角落。
  tag: ✅
  source: Warcraft Wiki — Trade District
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The bank, mailbox, and inn are on the southwest side of the Trade District."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "俯拍一小块街区：三栋建筑围成一个小广场，街心立着一根嵌投信口的石柱，人流在三点之间来回穿梭"
  negative: "分散布局, 空旷广场, 现代邮局"

- fact_id: stormwind.lore.019
  claim: 旧世寄件只要挂了物品或金币就要**整整一小时**才送到——「寄给小号」是一件要提前一小时计划的事。
  tag: ✅
  source: Warcraft Wiki — Mailbox, §Patch history / delivery times
  source_url: https://warcraft.wiki.gg/wiki/Mailbox
  quote: "Mail from another account if items or money are attached takes one hour."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街心一根石柱，柱身中部开一道铜边投信口，口下方挂一只小铜铃，柱顶是尖锥形铜盖"
  negative: "现代邮筒, 红色信箱, 木质邮箱, 快递柜"

- fact_id: stormwind.lore.020
  claim: 旧世**每两级**就得回城找职业训练师学新技能、还要花钱——这才是「必须回城」的真正原因，也是旅店与训练师之间那条路被走烂的原因。
  tag: ✅
  source: Warcraft Wiki — Class trainer
  source_url: https://warcraft.wiki.gg/wiki/Class_trainer
  quote: "New abilities and ranks become available from class trainers every other level (at even-numbered levels)."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "室内一位身着职业特征长袍的导师站在书案旁，案上摊开写满字的羊皮卷，来者站在案前低头听讲"
  negative: "教室黑板, 学生排队叫号, 现代培训机构"

- fact_id: stormwind.lore.021
  claim: 暴风城是**唯一一座职业训练师配齐的联盟城市**（连德鲁伊和萨满都有）——这是它作为「万事屋」的结构性优势。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Gameplay)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "It is the only Alliance city with all class trainers present (including druid and shaman)."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "俯拍全城，若干处屋顶下透出不同色调的光——祭坛的白、法术的蓝紫、锻炉的橙、林地的绿"
  negative: "单一色调, 空城, 现代写字楼"

- fact_id: stormwind.lore.022
  claim: 狮鹫管理员在贸易区东侧、要**顺一条坡道上去**——不是在地面，这是老玩家找飞行点时的固定动作。
  tag: ✅
  source: Warcraft Wiki — Trade District
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The Gryphon Master is up a ramp on the east side."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一道石砌宽坡道沿建筑外侧盘上平台，平台上立着栖木，两三只巨鹫收翅站立，羽毛被风掀起"
  negative: "电梯, 楼梯间, 平地栖木, 鸟笼"

- fact_id: stormwind.lore.023
  claim: 战场管理员是 2005 年 7 月 12 日的 1.6.0 才加进城里的；在那之前玩家得亲自跑到战场门口排队。
  tag: ✅
  source: Warcraft Wiki — Battlemaster, §Patch history
  source_url: https://warcraft.wiki.gg/wiki/Battlemaster
  quote: "Patch 1.6.0 (2005-07-12): Added."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "要塞内一间挂满旗帜的厅室，中央长桌上铺着战场地图，几名披甲军官围桌而立"
  negative: "电子排队机, 大屏幕, 报名处窗口"
```

### B. 玩家熟悉的地标与「梗」地点

```yaml
- fact_id: stormwind.lore.024
  claim: 入城必经的英雄谷里立着五尊雕像，纪念远征德拉诺的联盟远征军成员——所有人进城都得从他们脚下走过。
  tag: ✅
  source: Warcraft Wiki — Valley of Heroes
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "Five statues commemorate Alliance Expedition members."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "宽阔石桥两侧各立两尊、桥尽头正中一尊，共五尊三倍真人高的石雕，基座嵌铜牌，雕像背光成剪影"
  negative: "金色雕像, 现代纪念碑, 大理石抛光, 雕像手持现代武器"

- fact_id: stormwind.lore.025
  claim: 五块铜牌里有四块以「推定已故」四个字收尾（库德兰 / 卡德加 / 图拉杨 / 达纳斯），只有奥蕾莉亚那块没有这句。
  tag: ✅
  source: Warcraft Wiki — Valley of Heroes, §Statues（原始 wikitext 逐字取回）
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "Former Lieutenant to Lord Anduin Lothar. Knight of the Silver Hand. High General of the Alliance Expedition that marched into the orc homeworld of Draenor. Presumed deceased."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "长焦贴近雕像基座的铜牌，铜面氧化发暗、字口积着一层灰绿铜锈，末行字迹清晰可读"
  negative: "崭新铜牌, 抛光金牌, 现代刻字机字体, 中文碑文"

- fact_id: stormwind.lore.026
  claim: 只要最近有人杀掉奥妮克希亚，**她的头就会挂在暴风城入城拱门的左侧**；这条机制到 3.2.2 为止。
  tag: ✅
  source: Warcraft Wiki — Onyxia
  source_url: https://warcraft.wiki.gg/wiki/Onyxia
  quote: "Onyxia's head used to hang from the left arch into Stormwind City or be mounted on a large pillar near the front of Orgrimmar if she had recently been killed. This no longer happens as of 3.2.2."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "巨大黑龙头颅悬吊在石砌拱门左侧，鳞片是暗黑带虹彩的硬甲，獠牙外露、双目已浊，粗铁链穿颅骨固定，头颅尺寸比门下行人大出数倍"
  negative: "新鲜血迹喷溅, 卡通化龙头, 头颅发光, 头颅在摆动, 完整龙身"

- fact_id: stormwind.lore.027
  claim: 头一挂上去，**城里所有 60 级及以下的角色**同时吃到「屠龙者的战吼」增益——这是旧世最有「全服共同时刻」味道的一件事。
  tag: ✅
  source: Warcraft Wiki — Head of Onyxia (Classic)
  source_url: https://warcraft.wiki.gg/wiki/Head_of_Onyxia_(Classic)
  quote: "Completing [60] Victory for the Alliance grants the [Rallying Cry of the Dragonslayer] buff to all level 60 or lower characters in Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "广场上密密麻麻的人群同时被一层极淡的暖金色薄光扫过，光自拱门方向掠向人群，人群纷纷抬头"
  negative: "强烈金光爆炸, 光柱, 人物发光, 粒子雨, 现代灯光秀"

- fact_id: stormwind.lore.028
  claim: 这个增益持续 120 分钟——所以「头挂上了，快进城」是旧世公会频道里最常见的一句话。
  tag: ✅
  source: Warcraft Wiki — Rallying Cry of the Dragonslayer
  source_url: https://warcraft.wiki.gg/wiki/Rallying_Cry_of_the_Dragonslayer
  quote: "Duration: 120 minutes."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "拱门下人流骤然变密，来的方向单一，所有人都朝同一个方向奔跑"
  negative: "人群四散, 恐慌逃跑, 空街"

- fact_id: stormwind.lore.029
  claim: 交头的流程是把龙头交给暴风要塞里的博瓦尔·弗塔根；任务原文写的是「你完成了不可能之事。黑龙军团的育母倒在你脚下。取下她的头，呈给至高统帅。」
  tag: ✅
  source: Wowhead Classic — Quest 7495 "Victory for the Alliance"
  source_url: https://www.wowhead.com/classic/quest=7495/victory-for-the-alliance
  quote: "You have accomplished the impossible. The brood mother of the Black Dragonflight lies dead at your feet. Take her head and present it to the Highlord."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座厅内，一名披重甲的人类将领立于阶前，厅内两侧立柱高耸，光自高窗斜射入厅"
  negative: "国王坐在王座上, 现代法庭, 红毯颁奖"

- fact_id: stormwind.lore.030
  claim: 这套「挂头 + 全城 buff」机制是 2005 年 3 月 7 日的 1.3.0 加进来的——**经典旧世正是它存在的年代**。
  tag: ✅
  source: Warcraft Wiki — Head of Onyxia (Classic), §Patch history
  source_url: https://warcraft.wiki.gg/wiki/Head_of_Onyxia_(Classic)
  quote: "Added in Patch 1.3.0 (2005-03-07)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "拱门左侧空着一副粗铁链与铁环，链条垂下随风微摆，说明这里经常挂东西"
  negative: "拱门完全光秃, 现代吊钩, 装饰彩带"

- fact_id: stormwind.lore.031
  claim: 矿道地铁水下段里游着一只叫 Nessy 的巨型索德鲁怪，玩家永远碰不到它——它是对尼斯湖水怪的致敬。
  tag: ✅
  source: Warcraft Wiki — Nessy
  source_url: https://warcraft.wiki.gg/wiki/Nessy
  quote: "Nessy is a threshadon boss sometimes seen by travelers on the Deeprun Tram." / "Nessy is a reference to the Loch Ness Monster."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "隧道透明顶壁外的深绿色水体中，一头长颈巨兽的暗色轮廓缓慢横穿而过，只看得清颈、背脊与尾的剪影，细节隐没在浑水里"
  negative: "清晰全身特写, 卡通长颈龙, 发光眼睛, 张嘴攻击, 跃出水面"

- fact_id: stormwind.lore.032
  claim: 那段水下其实是一整座**地下湖**，里面除了 Nessy 还有巨蚌、两只娜迦海妖、一条姥鲨、若干沉船和一口宝箱。
  tag: ✅
  source: Warcraft Wiki — Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The underwater section of the tram is, in fact, a subterranean lake." / "a large beast named 'Nessy,'" / "a giant clam, two Naga Sirens, and a Basking Shark"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "隧道中段钢板让位给整段透明拱形顶壁，壁外是深绿水体，水中散落倾覆的木船骸骨与一口包铁木箱，光线自上方极弱地漏下"
  negative: "清澈蓝色海水, 珊瑚礁, 热带鱼, 阳光光柱, 玻璃反光过强"

- fact_id: stormwind.lore.033
  claim: 地铁修建时闹过鼠患，而且**到 Year 25 ADP 老鼠问题还在**，由一位叫 Monty 的「灭鼠专员」负责——这正是本片的当下时间点。
  tag: ✅
  source: Warcraft Wiki — Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "By the Year 25 ADP, the rat problem remained and was handled by Monty."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "月台角落堆着捕鼠笼与麻袋，一名穿工装、腰挂工具的男子蹲在轨道边查看，几只灰褐色大鼠贴着墙根窜过"
  negative: "卡通老鼠, 成群鼠潮, 现代灭鼠设备, 防护服"

- fact_id: stormwind.lore.034
  claim: 月台上还有个小贩 Nipsy——他卖的是「矿道鼠肉串」，拿地铁的鼠患当生意做。
  tag: ✅
  source: Warcraft Wiki — Deeprun Tram, §NPCs
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "Nipsy (Deeprun Rat kabob merchant)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "月台边一个小摊，炭火上架着穿好的肉串，摊主身后挂着一串串风干的小兽，摊前立着手写木牌"
  negative: "现代烧烤摊, 不锈钢推车, 招牌灯箱, 一次性餐具"

- fact_id: stormwind.lore.035
  claim: 暴风城监狱（Stockade）是一座**藏在运河区水下**的高警戒监狱，关的是小贼、政治犯、杀人犯和全境最危险的一批人。
  tag: ✅
  source: Warcraft Wiki — The Stockade
  source_url: https://warcraft.wiki.gg/wiki/The_Stockade
  quote: "Stormwind Stockade, aka the Stormwind Stockades and The Stockade, is a high-security prison complex, hidden beneath the canal district of Stormwind City." / "Presided over by Warden Thelwater, the Stockade is home to petty crooks, political insurgents, murderers, and a score of the most dangerous criminals in the land."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河水面上一座四面环水的方形石堡，墙体厚重、开窗极小且都装铁栅，唯一的入口是一道朝向岸边的包铁木门"
  negative: "现代监狱铁丝网, 探照灯, 岗楼, 高墙大院"

- fact_id: stormwind.lore.036
  claim: 它的入口在**环绕法师区那段运河的最北端**，进门后顺一小段敞开式台阶直接下去就是副本。
  tag: ✅
  source: Warcraft Wiki — Stormwind Stockade
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Stockade
  quote: "located inside Stormwind City, on the northernmost section of the canal surrounding the Mage Quarter" / "directly inside the building, down the small, open set of stairs"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石堡内一间小门厅，正中一段无扶手的敞开石阶直通地下，阶下是更暗的通道，墙上挂着油灯"
  negative: "电梯, 安检门, 长走廊, 铁门轰响"

- fact_id: stormwind.lore.037
  claim: 监狱门口**紧挨着**一块集合石——这块石头是 2005 年 3 月 7 日的 1.3.0 加的，旧世时它的作用是「自动帮等级合适的人凑队」，**不是召唤**。
  tag: ✅
  source: Warcraft Wiki — Meeting stone
  source_url: https://warcraft.wiki.gg/wiki/Meeting_stone
  quote: "Patch 1.3.0 (2005-03-07): Added." / "be used to fill in partially-formed parties whose members met the required level range by auto-inviting suitable candidates."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一块半人高的粗凿石碑立在门侧，碑面刻着一圈同心符文，符文缝隙里有极微弱的稳定辉光"
  negative: "强烈发光, 悬浮石块, 传送门, 现代指示牌, 全息投影"

- fact_id: stormwind.lore.038
  claim: 监狱在旧世是 22–30 级的低级副本——几乎每个联盟角色在二十几级时都被拉进去打过一次。
  tag: ✅
  source: Warcraft Wiki — The Stockade, §Patch history
  source_url: https://warcraft.wiki.gg/wiki/The_Stockade
  quote: "previous instance level: 22 - 30"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "门厅外的石阶上坐着三四个等人的旅人，装备粗糙、武器搁在膝上，有人在啃干粮"
  negative: "全副重甲, 精英装束, 排队叫号, 现代候车"

- fact_id: stormwind.lore.039
  claim: **旧世的监狱楼顶是有钟楼的**（后来被拆了），而它对岸那座「姊妹建筑」金库至今还留着钟楼——所以旧世的运河中段是**两座带钟的水中石堡对望**。
  tag: ✅
  source: Warcraft Wiki — Stormwind Stockade, §Notes and trivia
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Stockade
  quote: "used to have a clock tower, which has now been removed" / "A sister building called the Vault still retains its clock tower"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河纵深构图，近处一座方形石堡顶上立着带圆钟面的方塔，远处对岸另一座同形制石堡也顶着一座钟塔，两钟隔水相望"
  negative: "只有一座钟塔, 大本钟造型, 教堂尖顶钟楼, 电子钟"

- fact_id: stormwind.lore.040
  claim: 金库（Vault）就在监狱对面、四面环水，门口是一道落闸铁栅加两名守卫——而这扇门**从内测到现在就没开过一次**。
  tag: ✅
  source: Warcraft Wiki — Stormwind Vault
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Vault
  quote: "The Vault has never been officially accessible, not even in alpha or beta." / "gated off by a portcullis with two guards"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "水中石堡正面一道粗铁条焊成的落闸栅门，栅后是纯黑的门洞，两名披罩袍的守卫分立两侧一动不动"
  negative: "门开着, 门内有光, 栅门生锈断裂, 现代铁门, 守卫走动"

- fact_id: stormwind.lore.041
  claim: 旧城区与贸易区之间还有**另一扇永远打不开的门**——一道落闸铁栅后面藏着一个从未启用的副本传送门，它原本是给「玩家住宅区」准备的，直到《大地的裂变》才被移除。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Development)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The unused instance portal behind a large portcullis between the Old Town and the Trade District (removed in World of Warcraft: Cataclysm) was originally meant to lead to the player housing area."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "两街区之间一条无出口的短石廊，尽头是一道落闸铁栅，栅后一团幽蓝色的门户光在黑暗里缓慢旋转，廊内无人无灯"
  negative: "门户是紫色, 门户外溢强光, 有人进出, 廊内有摊贩, 门是打开的"

- fact_id: stormwind.lore.042
  claim: 运河本身就是一件**没做成的功能留下的疤**——设计之初打算在里面跑贡多拉让玩家在区间快速通勤，后来这套技术被判定「过于晦涩不值当」而砍掉，运河与「玩家可以下水再爬上来」的设定就这么留了下来。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Development)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Originally, the city was planned to feature gondolas that would serve as a quick way to travel from one district to another, hence the existence of the Canals and the fact that players can get in and out of the Canal waters. However, the technology wound up being \"prohibitively esoteric.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "宽阔石砌运河水面空无一船，两岸石堤整齐、每隔一段有一道下水石阶，阶面被水浸出深色水线"
  negative: "运河里有船, 贡多拉, 码头系船柱有缆绳, 划桨人"

- fact_id: stormwind.lore.043
  claim: 花园区正中那口月亮井是暗夜精灵自己凿的——石砌水池里盛着会发银光的水。
  tag: ✅
  source: Warcraft Wiki — Park / Moonwell
  source_url: https://warcraft.wiki.gg/wiki/Moonwell
  quote: "The night elves created a Moonwell in the center of the park square." / "stone pools filled with silvery glowing water"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "林间空地中央一口圆形石砌浅池，池水泛着冷银色自发光，池沿雕着藤蔓纹，四周是高大树木与草地"
  negative: "蓝色泳池, 喷泉水柱, 金色光, 水面沸腾, 人造灯带"

- fact_id: stormwind.lore.044
  claim: 花园区是**整个东部王国唯一有德鲁伊训练师的地方**——所有东部王国的德鲁伊玩家，每两级都必须回到这片小树林。
  tag: ✅
  source: Warcraft Wiki — Park
  source_url: https://warcraft.wiki.gg/wiki/The_Park
  quote: "It was the only place in the Eastern Kingdoms where druid trainers resided."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "树下三位暗夜精灵长者分立，身着树叶与皮革缀成的长袍，各自面前站着前来求教的人"
  negative: "人类训练师, 室内教室, 法师长袍, 石砌讲堂"

- fact_id: stormwind.lore.045
  claim: 花园区是暗夜精灵在这座石头城里的避难所——他们觉得这点自然气息是对城里无边石路的一种慰藉。
  tag: ✅
  source: Warcraft Wiki — Park
  source_url: https://warcraft.wiki.gg/wiki/The_Park
  quote: "a refuge for visiting night elves, who found the comforting presence of nature a welcome respite from the vast stone thoroughfares of Stormwind proper."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌街道尽头忽然转为草地与林荫，界线清晰得像被刀切开，几名高挑的暗夜精灵坐在树根上"
  negative: "过渡渐变, 花圃花坛, 修剪整齐的绿篱, 人造草坪"

- fact_id: stormwind.lore.046
  claim: 法师区那家「已宰的羔羊」明面上只是间破酒馆，柜台后的酒保会劝客人「离阴影远点」。
  tag: ✅
  source: Warcraft Wiki — The Slaughtered Lamb
  source_url: https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb
  quote: "The Slaughtered Lamb is a seedy pub in the Mage Quarter of Stormwind City." / "advises patrons to 'stay away from the shadows'."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "低矮昏暗的酒馆一层，只有一名酒保和两三张空桌，招牌是一只被吊起的羊，墙角堆着杂物，光源只有柜台后一盏油灯"
  negative: "热闹酒吧, 乐师, 满座客人, 明亮吊灯, 彩色酒瓶"

- fact_id: stormwind.lore.047
  claim: 但它的地窖与地下墓穴是**暴风城术士的圣所与训练场**——新人在这里入门，从卡兹莫丹转来的学徒也在这里受训。
  tag: ✅
  source: Warcraft Wiki — The Slaughtered Lamb
  source_url: https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb
  quote: "The tavern's catacombs serve as the sanctum of the warlocks of Stormwind." / "training grounds for new recruits in the kingdom, and for transferred students from Khaz Modan."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "地窖石室，地面刻着一圈直径两米的召唤法阵，阵线里嵌着暗紫色余烬般的微光，四壁是粗石与壁龛，壁龛里点着数支蜡烛"
  negative: "明亮法阵, 强紫色光柱, 血迹, 骷髅堆, 现代地下室"

- fact_id: stormwind.lore.048
  claim: 「已宰的羔羊」这个名字是致敬电影《美国狼人在伦敦》里那家同名酒馆。
  tag: ✅
  source: Warcraft Wiki — The Slaughtered Lamb, §Trivia
  source_url: https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb
  quote: "The Slaughtered Lamb is named after a pub of the same name that appears in the film An American Werewolf in London."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "酒馆门外挂着一块褪色木招牌，画着一只被后腿倒吊的剥皮羊，招牌铁环锈蚀、随风轻晃"
  negative: "霓虹招牌, 可爱卡通羊, 崭新油漆, 英文店名特写"

- fact_id: stormwind.lore.049
  claim: 经典旧世的术士新人任务原文就是「到暴风城法师区找加金·黑暗之缚……你会在已宰的羔羊的地下室找到他」。
  tag: ✅
  source: Wowhead Classic — Quest 1715 "The Slaughtered Lamb"
  source_url: https://www.wowhead.com/classic/quest=1715/the-slaughtered-lamb
  quote: "you'll find Gakin in the basement of the Slaughtered Lamb in Stormwind."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "地窖深处一名披深色兜帽长袍的人类立于阴影中，只有下半张脸被烛光照亮"
  negative: "全身发光, 恶魔外形, 面部完全遮蔽, 红色眼睛"
```

### C. 玩家会讲的「城市冷知识」

```yaml
- fact_id: stormwind.lore.050
  claim: 狮鹫管理员 Dungar Longdrink 是个人类，**却带着一口矮人腔**，连名字都像矮人名——这被认为是开发期本来打算把他做成矮人留下的痕迹。
  tag: ✅
  source: Warcraft Wiki — Dungar Longdrink, §Trivia
  source_url: https://warcraft.wiki.gg/wiki/Dungar_Longdrink
  quote: "Although Dungar is a human, his name sounds more appropriate for a dwarf and he speaks with a dwarven accent in his original dialogue lines, implying he was originally intended to be a dwarf during development."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "栖木平台上一名络腮胡人类男子，穿皮护腕与厚外套，正伸手拍一只巨鹫的颈羽"
  negative: "矮人身材, 精致贵族装, 无胡须青年, 现代制服"

- fact_id: stormwind.lore.051
  claim: 贸易区 [66.1, 74.2] 那家奶酪铺的老板 Elling Trias 明面上只卖奶酪、和妻子 Elaine 与儿子 Ben 一起看店，暗地里手握一张**从 SI:7 一直铺到希尔斯布莱德北边赫斯格拉德的情报网**。
  tag: ✅
  source: Warcraft Wiki — Elling Trias
  source_url: https://warcraft.wiki.gg/wiki/Elling_Trias
  quote: "an extensive web of contacts, stretching from SI:7 to agents as far off as Hearthglen."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "临街一间窄铺面，柜台上摞着大小奶酪轮，蜡封面朝外，梁上悬挂纱布包裹的干酪，一家三口在店内各做各事"
  negative: "冷柜, 保鲜膜, 价签, 连锁店装潢, 试吃台"

- fact_id: stormwind.lore.052
  claim: 城里有个绰号叫「奶酪之都」——这个称呼多半就是冲着这家奶酪铺来的。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Lore)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Doctor Weavil refers to Stormwind City as the \"capital of cheese\", likely because of the shop Trias Cheese."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "奶酪轮的特写：外壳是蜡封的深红与土黄，切口处质地紧实带气孔，旁边搁着一把宽刃奶酪刀"
  negative: "切片包装奶酪, 塑料盒, 现代超市货架"

- fact_id: stormwind.lore.053
  claim: 情报机构 SI:7 在**几乎每一个城区**都安着「朋友」——卖货的、听闲话的、替他们盯梢的。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Lore)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "SI:7 have \"friends\" in nearly every quarter of Stormwind City, selling goods, listening to strangers chat, and keeping an eye out on their behalf."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街边一个不起眼的摊主在称货，视线却越过顾客肩膀落向街对面，眼神停留时间比正常长半拍"
  negative: "夸张的窥探动作, 躲在柱子后, 望远镜, 黑衣特工"

- fact_id: stormwind.lore.054
  claim: 光明大教堂那口钟是**在铁炉堡的大熔炉上铸的**，是矮人送的礼；它还有一口孪生钟给了洛丹伦。
  tag: ✅
  source: Warcraft Wiki — Cathedral of Light
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "created on the Great Forge in Ironforge" / "a gift from the dwarves"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "钟楼内部仰拍，一口青铜大钟悬于粗梁之下，钟体外壁有铸造流纹与一圈浮雕铭带，钟口边缘被撞槌磨出亮痕"
  negative: "金色钟, 现代电动钟, 钟表机芯, 小手摇铃"

- fact_id: stormwind.lore.055
  claim: 这口钟**按点报时**，遇险时则用来示警；它每天日落敲一次，音色清甜，全城都听得见。
  tag: ✅
  source: Warcraft Wiki — Cathedral of Light / Stormwind City §Notes and trivia
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The cathedral's bell rings to mark the hours, and in times of danger to alert the citizens."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "黄昏时分的教堂广场，长焦压缩的钟楼剪影贴在橙红天幕上，广场上行人同时停步抬头"
  negative: "正午强光, 夜景, 钟楼灯光照明, 鸽群特效"

- fact_id: stormwind.lore.056
  claim: 这座城**连设计它的人都承认难走**——设计师 Johnathan Staats 回忆暴风城「做起来格外痛苦」，因为布局绕，而且开发期的绝大部分时间里**根本没有小地图**，很多人一进城就迷路、连城门都找不回去；他举的例子是「你要一直走到看见出城的大门，才知道自己原来在贸易区」。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Development)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Johnathan Staats recalls that Stormwind was \"especially painful\" to design due to its confusing layout and the fact that the minimap functionality didn't exist for the majority of WoW's development, meaning that many who entered Stormwind would get lost and be unable to find the city gates."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一条石砌拱廊通道内的主观视角，左右各有岔口，尽头又是一道拱门，看不到任何地标或天际线"
  negative: "开阔广场, 清晰地标, 指路牌, 俯瞰全景, 现代路标"

- fact_id: stormwind.lore.057
  claim: 同一位设计师还记得，暴风城**本来可能有九个城区**，后来其中两个被并成了一个。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Development)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Staats also recalls that Stormwind may have originally had nine districts, two of which were fused into a single area."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "俯拍全城，运河把街区切成若干近似矩形的块，其中一块明显比邻块大出一倍、内部还残留一道旧分界线"
  negative: "均匀网格, 现代规划图, 标注数字"

- fact_id: stormwind.lore.058
  claim: 2002 年初有几个星期，暴风城的区域背景音乐被换成了一首杰斐逊星船乐队的歌——纯粹是恶作剧，因为那首歌太招人烦。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Development)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "For a few weeks in early 2002, Stormwind's zone music was a Jefferson Starship song. It was set up that way as a practical joke, since the song was so reviled."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（无画面；本条是纯口播梗，配城市空镜即可）"
  negative: "出现现代乐队, 唱片, 音响设备, 乐谱"

- fact_id: stormwind.lore.059
  claim: **每一个城区都能找到苹果树**——这是全城最容易被忽略、却最适合当前景层的细节。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Lore)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Apple trees can be found in every district of Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌街角一棵不高的苹果树，枝上挂着零星红果，树根处围着一圈矮石砌花池，落果散在石板上"
  negative: "果园成排, 观赏樱花, 热带植物, 盆栽, 塑料树"

- fact_id: stormwind.lore.060
  claim: 旧世的暴风城里散着**一堆装牛奶的木桶，而且是取之不尽的**——低级法系玩家靠它省下大把买水钱。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Gameplay)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "There was once an endless supply of Ice Cold Milk scattered around Stormwind City in barrels, which was useful if you were a low-level mana user and wanted to save gold."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "墙根下并排三只矮胖木桶，桶盖半掀，里面是乳白色液体，桶箍是黑铁，桶身有溢出后干涸的白渍"
  negative: "玻璃瓶装牛奶, 现代奶箱, 纸盒, 冷藏柜, 奶牛"

- fact_id: stormwind.lore.061
  claim: 在运河里钓鱼是市民的正经消遣，钓上来的是巨型鲶鱼和运河蟹。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Lore)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Fishing is a favored sport in Stormwind City. ... Fishermen fish Gigantic Catfish and Canal Crabs in the Canals."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河石阶上坐着两三个垂钓者，简陋木竿斜出水面，脚边放着湿麻袋与木桶，水面浮标静止"
  negative: "现代钓具, 遮阳伞, 折叠椅, 渔船, 海钓"

- fact_id: stormwind.lore.062
  claim: 城里有学校——女教师 Miss Danna 在好几个城区都带着一群孩子上课。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Lore)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "In some districts, School Mistress Miss Danna teaches a group of children, indicating the presence of a school in the city."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街边石阶上七八个孩子席地坐成半圈，正中一名穿素色长裙的女教师举着一块小木板讲解"
  negative: "教室课桌, 黑板, 校服, 书包, 现代课本"
```

### D. 副本入口、远方战事在城里的体现

```yaml
- fact_id: stormwind.lore.063
  claim: 暴风城是**唯一一座城内就有副本的联盟首都**——打完出来就能就地修装备、卖东西。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Gameplay)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "It is the only Alliance capital that has an instance within the city borders. This is convenient for repairing and selling afterwards."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "监狱石堡门外几步就是沿河店铺，铁匠炉火与货摊紧挨着监狱大门"
  negative: "荒僻郊外, 隔离带, 空无一人的门口"

- fact_id: stormwind.lore.064
  claim: 这座城曾经是部落玩家最爱的作案现场——他们把团本 BOSS 克萨维厄斯一路拉进城里放开。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Gameplay)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The capital used to be a big target for Horde players to kite the end-game boss Lord Kazzak and then set him loose within the city."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城门内广场上尸横遍地，幸存者朝四个方向奔逃，画面中央地面有一个巨大的凹陷脚印"
  negative: "出现怪物全身, 火焰爆炸, 血浆, 卡通化, 现代灾难片"

- fact_id: stormwind.lore.065
  claim: 有据可查的第一次发生在 **2005 年 3 月 6 日**——一个（显然闲得发慌的）玩家把它从诅咒之地一路拉到暴风城，把那个服务器搅得天翻地覆。
  tag: ⚠️
  source: DKPminus — "Awesome Events that Happened in Vanilla World of Warcraft"（媒体整理，非官方补丁说明）
  source_url: https://www.dkpminus.com/wow/news/awesome-events-that-happened-in-vanilla-world-of-wacraft/
  quote: "On March 6th of 2005 an industrious (and obviously bored) player kited Kazzak from his then home in the Blasted Lands to Stormwind, wrecking havoc on players on that server."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（同上条；本条只提供日期，画面沿用 064）"
  negative: "同上"

- fact_id: stormwind.lore.066
  claim: 2005 年 9 月 13 日的 1.7.0 之后爆发过一场「堕落之血」瘟疫——本该只存在于祖尔格拉布副本里的传染性 debuff 被带进了人口密集的首都，几小时内成片秒杀低级玩家。
  tag: ✅
  source: Warcraft Wiki — Corrupted Blood incident
  source_url: https://warcraft.wiki.gg/wiki/Corrupted_Blood_incident
  quote: "When infected pets were re-summoned the debuff immediately spread to nearby players and NPCs."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城市广场地面上散落着尚未消失的尸体轮廓，周围的人群拉开一个空圈站着不敢靠近"
  negative: "血迹喷溅, 绿色毒雾特效, 丧尸, 医疗队, 现代防疫装备"

- fact_id: stormwind.lore.067
  claim: 1.11.0 的天灾入侵事件里，**一座天灾浮空城直接停在了暴风城外**，城里还会零星刷出天灾生物，白银之手黎明军团在各处扎营应对。
  tag: ✅
  source: Warcraft Wiki — Scourge Invasion
  source_url: https://warcraft.wiki.gg/wiki/Scourge_Invasion
  quote: "A necropolis has appeared outside Stormwind and Undercity." / "Scourge mobs will occasionally appear in Stormwind and Undercity"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城外天际线上悬着一块倒金字塔形的巨大黑石构造，底部尖端朝下，表面有苍绿色微光的裂缝，云层在它周围被压成环状"
  negative: "飞船, 陨石, 龙, 现代 UFO, 强烈绿光照亮全城"

- fact_id: stormwind.lore.068
  claim: 暴风要塞的王座厅里发生过旧世最著名的一场当众揭穿——玩家护送雷金纳德·温德索尔进厅，当场戳穿王室顾问卡特拉娜·普瑞斯托的真身是黑龙奥妮克希亚。
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade
  source_url: https://warcraft.wiki.gg/wiki/The_Great_Masquerade
  quote: "Reginald Windsor escorts players to confront Lady Katrana Prestor, who is revealed to be the dragon Onyxia in disguise."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "高大石柱夹道的王座厅，尽头王座与阶台，两侧站满披甲卫兵，高窗斜射的光柱把厅内切成明暗相间的条带"
  negative: "龙出现在厅内, 打斗场面, 火焰, 现代法庭, 红毯"

- fact_id: stormwind.lore.069
  claim: 安其拉之门的战争物资收集**不在暴风城**——联盟的集结点是铁炉堡的军事区。
  tag: ✅
  source: Warcraft Wiki — Ahn'Qiraj War Effort
  source_url: https://warcraft.wiki.gg/wiki/Ahn%27Qiraj_War_Effort
  quote: "The Alliance needs to gather in the Military Ward of Ironforge"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（本条是反例，用于排除误植；无需画面）"
  negative: "暴风城内出现战争物资收集台, 铜锭堆, 绷带堆"
```

### E. 环境质感与机位（玩家反复截图的地方）

```yaml
- fact_id: stormwind.lore.070
  claim: 矮人区的锻炉**常年在冒一层烟霾**，配着不间断的铁锤声——这是全城感官最强烈的一块。
  tag: ✅
  source: Warcraft Wiki — Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The forges in the district produce a constant haze, supplemented by the constant strokes of smiths' hammers."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "半开放的锻造棚下炉膛通红，空气里悬着一层灰白烟霾把光打散成可见光柱，砧上铁件通红、锤落处溅起橙色火星"
  negative: "清澈空气, 冷色调, 现代车间, 电焊弧光, 无烟"

- fact_id: stormwind.lore.071
  claim: 旧城区是全城反差最大的一块——街道明显更脏更臭，住的多是穷人，乞丐和小偷都在这儿。
  tag: ✅
  source: Warcraft Wiki — Old Town
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "the streets are described as far dirtier and smellier than the other districts. It is also the residential area for most of the poor folk of the city, as beggars, thieves, and poor people can be found there."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "窄巷两侧是木构上层外挑的旧屋，巷面石板缝里积着污水，墙根堆着破筐与草料，巷口顶光形成强明暗对比"
  negative: "整洁街道, 鲜花窗台, 明亮均匀光, 观光步行街"

- fact_id: stormwind.lore.072
  claim: 法师区有家叫「蓝色隐士」的小馆子，以吃食、饮品和好谈话出名，来的多是懂点魔法的人，气氛比已宰的羔羊体面得多。
  tag: ✅
  source: Warcraft Wiki — Blue Recluse
  source_url: https://warcraft.wiki.gg/wiki/Blue_Recluse
  quote: "known for its food, drinks, and good conversations"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "临水一栋两层小馆，一层户外摆着几张厚木桌，桌上有陶杯与烛台，窗内透出暖光，水面映着窗影"
  negative: "露天咖啡遮阳伞, 现代餐厅, 霓虹, 塑料椅"

- fact_id: stormwind.lore.073
  claim: 教堂广场除了大教堂，还挤着公墓、市政厅和孤儿院——一座城怎么对待它的死者、它的户口本和它的孤儿，全在这一块地上。
  tag: ✅
  source: Warcraft Wiki — Cathedral Square
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_Square
  quote: "Stormwind City Cemetery (north of the square)" / "City Hall" / "Orphanage"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "广场一侧是大教堂正立面，北侧铁栅围出一片墓园、立着成排素色石碑，另一侧是两栋较矮的石砌公署建筑"
  negative: "商业街, 游乐设施, 现代市政厅玻璃幕墙, 十字架墓碑"

- fact_id: stormwind.lore.074
  claim: 孤儿院的院长 Orphan Matron Nightingale 就在教堂广场 [56.3, 54.0]；儿童周是 2005 年 4 月 19 日的 1.4.0 加的，玩家要领一个孤儿出来带他看世界。
  tag: ✅
  source: Warcraft Wiki — Children's Week
  source_url: https://warcraft.wiki.gg/wiki/Children%27s_Week
  quote: "Orphan Matron Nightingale at [56.3, 54.0] in Cathedral Square of Stormwind City" / "Patch 1.4.0 (2005-04-19): Added."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一栋朴素石砌小楼，门前台阶上坐着几个衣着旧但干净的孩子，门口立着一名穿灰裙的中年女性"
  negative: "现代孤儿院, 铁门, 玩具, 校服, 福利院招牌"

- fact_id: stormwind.lore.075
  claim: 城门永远开着；门外站两名卫兵、门内也站两名，另有两名在英雄谷两头来回巡逻。
  tag: ✅
  source: Warcraft Wiki — Stormwind Gate
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Gate
  quote: "Two Stormwind City Guards stand just outside the gate (Elwynn Forest zone) and two stand just inside the gate (Stormwind City zone)." / "always open to allow players to travel in and out of the city"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "巨大石砌门洞两侧各立一名披蓝狮徽罩袍、持长戟的卫兵，门扇完全敞开且看不出有关闭的痕迹"
  negative: "城门关闭, 吊桥升起, 安检, 收费亭, 拒马"

- fact_id: stormwind.lore.076
  claim: 卫兵会给人指路——在主城里跟他们搭话，他们会把你要找的地方标到地图上。
  tag: ✅
  source: Warcraft Wiki — Guard
  source_url: https://warcraft.wiki.gg/wiki/Guard
  quote: "Most will answer questions about the capitals they protect if interacted with, guiding adventurers to various useful locations."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "卫兵侧身抬起持戟的另一只手，指向街道延伸的方向，指尖所指处远景里正是目标建筑的屋顶"
  negative: "卫兵掏出地图, 纸质指示牌, 电子屏, 导游举旗"
```

### F. Classic 怀旧服重新激活的记忆（含玩家社区说法）

```yaml
- fact_id: stormwind.lore.077
  claim: 在经典旧世的大部分时间里，**联盟的实际首都是铁炉堡而不是暴风城**——各城拍卖行还没并池之前，铁炉堡才是联盟活动的中心。
  tag: ✅
  source: Warcraft Wiki — Ironforge
  source_url: https://warcraft.wiki.gg/wiki/Ironforge
  quote: "Before the addition of auction houses in all capital cities, Ironforge was *the* central hub of Alliance activity."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（对照用；暴风城这边的画面是街上人流稀疏、店铺开着却没什么顾客）"
  negative: "暴风城人山人海, 拥堵, 排队"

- fact_id: stormwind.lore.078
  claim: 因为人太挤，铁炉堡在玩家嘴里的外号是「卡炉堡」——延迟高、帧数低。
  tag: ⚠️
  source: Warcraft Wiki — Ironforge（记录的是玩家社区的叫法，非设定）
  source_url: https://warcraft.wiki.gg/wiki/Ironforge
  quote: "the city was often referred to as \"Lagforge\" because of the increase in latency and decrease in framerates."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（对照用；无暴风城画面）"
  negative: "同上"

- fact_id: stormwind.lore.079
  claim: 暴风城作为高级玩家聚集地的地位是**一路起伏的**，直到 1.10 之后才相对铁炉堡涨了起来（还因服务器而异）。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia (Gameplay)
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Stormwind City's role as a hangout for high-level players has fluctuated over the years. Since patch 1.10, it has risen in popularity compared to Ironforge (though this may vary by server)."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区街道上人流中等——不空也不挤，几个人围着拍卖行门口，其余街段只有零散行人"
  negative: "极度拥挤, 完全空城"

- fact_id: stormwind.lore.080
  claim: 玩家社区里，「第一次进大城被震住」是最高频的旧世回忆之一——有人回忆自己进城后开口问路，一堆人回应，还有个人专门带他绕了一圈指出银行和拍卖行在哪。
  tag: ⚠️
  source: 玩家社区 — 暴雪官方论坛 WoW Classic 版 "What are your earliest memories from vanilla?"
  source_url: https://us.forums.blizzard.com/en/wow/t/what-are-your-earliest-memories-from-vanilla/160565
  quote: "I remember asking for a little direction and a bunch of people responded and one guy even gave me a little tour to show me the bank, auction house"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "街心一个显然是新来的人站着左右张望，两三个路人停下来朝不同方向比划"
  negative: "所有人低头赶路, 无人互动, 现代问路 App"

- fact_id: stormwind.lore.081
  claim: 玩家社区里，「不知道炉石是什么、卡在荒野回不去城」也是旧世的集体记忆之一。
  tag: ⚠️
  source: 玩家社区 — 暴雪官方论坛同帖
  source_url: https://us.forums.blizzard.com/en/wow/t/what-are-your-earliest-memories-from-vanilla/160565
  quote: "i remember i got lost in badlands at lvl 17 or something, didnt know what hearthstone was"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播梗；配一个人站在城门口回望城外荒野的背影镜）"
  negative: "地图 UI, 导航箭头, 现代手机"

- fact_id: stormwind.lore.082
  claim: 老花园区在玩家社区里被怀念的是它的「留白」——玩家说老公园「有一种活着的城市的感觉」，还有人说「不是每个角落都得塞满东西，塞满了就没沉浸感了」。
  tag: ⚠️
  source: 玩家社区 — MMO-Champion 帖 "I miss the old Stormwind park"
  source_url: https://www.mmo-champion.com/threads/2387193-I-miss-the-old-Stormwind-park
  quote: "the old park had a 'living city' feel to it" / "not every nook and cranny needs to be filled with stuff. It kills immersion."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "林间空地留出大片什么都没有的草地与空白，只有几棵树、一口井和两三个坐着的人"
  negative: "摆满摊位, 密集 NPC, 装饰物堆砌, 活动舞台"

- fact_id: stormwind.lore.083
  claim: 有玩家把自己在老花园区的时间说成「2006 年在那儿和别人一起玩得很开心，或者就是一个人待着歇口气」——「歇口气的地方」是这一区最准确的定位。
  tag: ⚠️
  source: 玩家社区 — 同帖
  source_url: https://www.mmo-champion.com/threads/2387193-I-miss-the-old-Stormwind-park
  quote: "I had so much fun there back in 2006 with other players or just relaxing on my own taking a break from questing in Elwynn Forest."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "一个人独自坐在月亮井边的石沿上，面朝水面，背对镜头，四周没有别人"
  negative: "人群, 活动, 表演, 拍照打卡"

- fact_id: stormwind.lore.084
  claim: 一篇玩家长文把暴风城总结为「你是这台大机器里的一个齿轮，但你也是这座伟大城市里重要的一部分」——「归属感」是这座城对玩家的核心作用。
  tag: ⚠️
  source: 玩家社区 — 个人长文 "Stormwind is the centre of the world"
  source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world
  quote: "you're a cog in a bigger machine, but you're an important part of this great city too."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "高机位俯拍，主角贴画面底部占画高 1/10，前方是层层叠叠的屋顶与运河，人流从画面各处穿过"
  negative: "主角占画面中心, 特写, 英雄光, 逆光剪影站在高处"

- fact_id: stormwind.lore.085
  claim: 同一篇长文把矿道地铁的观感写成「每天运送成千上万人，方式近乎魔法」——地铁在玩家心里的分量不在快，而在「奇观」。
  tag: ⚠️
  source: 玩家社区 — 同文
  source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world
  quote: "The tram that runs from here to Ironforge, taking thousands of people a day in a manner that seems magical."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "月台仰拍，巨大齿轮与铜管构成的机械结构占据画面上半，车厢从隧道口驶出，蒸汽自轨侧喷出"
  negative: "现代地铁, 电子报站, 闸机, 广告灯箱"

- fact_id: stormwind.lore.086
  claim: 2019 年怀旧服开服时，暴风城与铁炉堡「重新变得生机勃勃、挤满了找人组队的玩家」——这是怀旧服最被反复提起的画面。
  tag: ⚠️
  source: Kotaku — "World Of Warcraft Classic: Maybe You Can't Go Home Again"（媒体报道玩家体验）
  source_url: https://kotaku.com/world-of-warcraft-classic-maybe-you-cant-go-home-again-1844611355
  quote: "Stormwind and Ironforge, the two most important hubs of the Alliance, were vibrant and flush with players looking to group up."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区街心挤满了人，人群密到看不见地面，所有人都朝同一块区域移动"
  negative: "空城, 稀疏行人, 现代人群"

- fact_id: stormwind.lore.087
  claim: 旧世玩家怀念的不是「升到 60」，而是过程本身——有作者总结「60 级就在地平线上，但那从来不是目标」。
  tag: ⚠️
  source: Kotaku — 同文
  source_url: https://kotaku.com/world-of-warcraft-classic-maybe-you-cant-go-home-again-1844611355
  quote: "Level 60 loomed on the horizon, but that was never the goal."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（纯口播；配城市黄昏空镜）"
  negative: "等级数字, UI, 进度条"

- fact_id: stormwind.lore.088
  claim: 主城交易频道后来接手了「贫瘠之地闲聊」那套刷屏文化——爱找茬的玩家「整天泡在主城的交易频道里」。
  tag: ✅
  source: Warcraft Wiki — Barrens chat
  source_url: https://warcraft.wiki.gg/wiki/Barrens_chat
  quote: "most \"trolls\", or players that enjoy provoking others into confrontations, spend their days in Trade chat in the main cities."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播梗；配拍卖行门口人群嘈杂的中景，人物都在原地站着或坐着，没人在动）"
  negative: "聊天气泡, 文字 UI, 表情符号"

- fact_id: stormwind.lore.089
  claim: 暴风城的主题曲由 Jason Hayes 为 2004 年初版《魔兽世界》所作，是联盟玩家公认的记忆锚点。
  tag: ⚠️
  source: 玩家社区 / 音乐平台条目（VI-Control 论坛与 Spotify 均标注 Jason Hayes 为 "Stormwind" 作曲）
  source_url: https://vi-control.net/community/threads/world-of-warcraft-stormwind-city-theme-mockup-composed-by-jason-hayes.110266/
  quote: "World of Warcraft: Stormwind City Theme ... composed by Jason Hayes"
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "（纯声音层；画面用城市大远景 + 缓慢推进）"
  negative: "出现乐器, 乐团, 唱片封面"
```

### G. 版本错置（❌，机器可读的排除项；完整清单见 § 不可用清单）

```yaml
- fact_id: stormwind.lore.090
  claim: 巫师圣殿塔内有一间通往各大城市的传送门大厅。
  tag: ❌
  source: Warcraft Wiki — Wizard's Sanctum（该大厅是 8.1.5 才建的，旧世没有）
  source_url: https://warcraft.wiki.gg/wiki/Wizard%27s_Sanctum
  quote: "With patch 8.1.5, the tower's interior was completely revamped to house the Stormwind Portal Room"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止出现的画面：塔内一圈站立的传送门阵列）"
  negative: "传送门大厅, 一圈传送门, 门户阵列, 传送门管理员, 各城传送门标牌"

- fact_id: stormwind.lore.091
  claim: 猪和哨声酒馆有旅店老板，可以在旧城区绑炉石。
  tag: ❌
  source: Warcraft Wiki — Pig and Whistle Tavern（老板娘是 4.0.1 才加的）
  source_url: https://warcraft.wiki.gg/wiki/Pig_and_Whistle_Tavern
  quote: "Maegan Tillman ... was added in Patch 4.0.1, making this Stormwind's second inn."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止出现的画面：猪和哨声里的旅店老板柜台）"
  negative: "旧城区旅店老板, 第二家旅店, 猪和哨声绑炉石"

- fact_id: stormwind.lore.092
  claim: 集合石是用来把队友召唤到副本门口的。
  tag: ❌
  source: Warcraft Wiki — Meeting stone（这是 2.0.1 之后的功能；旧世是自动凑队）
  source_url: https://warcraft.wiki.gg/wiki/Meeting_stone
  quote: "Patch 2.0.1 (2006-12-05): Meeting Stones now function similar to a Warlock Summon spell."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止出现的画面：集合石上方浮现传送门、人从中走出）"
  negative: "集合石开门, 人从石中传送出现, 召唤光柱"

- fact_id: stormwind.lore.093
  claim: 暴风城有一座港口。
  tag: ❌
  source: Warcraft Wiki — Stormwind Harbor（3.0.2 才加）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Harbor
  quote: "Patch 3.0.2 (2008-10-14): Added."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止出现的画面：城西北的大型港口、栈桥与远洋帆船）"
  negative: "港口, 栈桥, 远洋帆船, 灯塔, 码头吊臂, 船坞"

- fact_id: stormwind.lore.094
  claim: 金库顶上的钟停在 8 点 15 分。
  tag: ❌
  source: Warcraft Wiki — Stormwind Vault（钟停在死亡之翼袭城那一刻，是大灾变之后的设定）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Vault
  quote: "The clock at the top of the vault which was stopped at the time of Deathwing's attack on Stormwind City"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止出现的画面：钟面指针停在 8:15）"
  negative: "停摆的钟, 指针停在八点一刻, 钟面裂纹, 焦痕"

- fact_id: stormwind.lore.095
  claim: 运河是半淤浅的，长着芦苇、沉着杂物。
  tag: ❌
  source: Warcraft Wiki — Canals (Stormwind City)（4.0.3a 才改成这样；旧世是深水）
  source_url: https://warcraft.wiki.gg/wiki/Canals_(Stormwind_City)
  quote: "canals became halfway filled in with mud/silt, along with occasional reeds and lost debris."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（禁止出现的画面：浅水淤泥运河、芦苇丛、露出水面的杂物）"
  negative: "浅水, 淤泥, 芦苇, 露出水面的木桩与杂物, 可涉水而过"
```

---

## 讲解点总表

> 「玩家记忆强度」判据：**强**＝旧世每个联盟角色几乎必然做过/见过（机制强制或位于必经之路）；
> **中**＝多数玩家做过但可绕过（职业限定、需要主动找）；**弱**＝要特意去找或运气成分大。

| # | 讲解点 | 所在区 | Vanilla 可用 | 记忆强度 | 镜头类型建议 | 回指 fact_id |
|---|---|---|---|---|---|---|
| 1 | **把炉石绑在镀金玫瑰**（全城唯一旅店） | 贸易区 | ✅ | **强**——机制强制，全服唯一绑点，一小时一次的回城键 | 门口中景 → 柜台近景（壁炉侧光）→ 手中石片特写 | 001–010 |
| 2 | **矿道地铁：从暴风城坐到铁炉堡** | 矮人区东侧 | ✅ | **强**——唯一直连，几乎人人坐过，60 秒挂机时间 | 齿轮隧道口仰拍定镜 → 车厢内侧跟 → 水下段透壁奇观镜 | 011–013, 085 |
| 3 | **水下段的 Nessy** | 地铁水下段 | ✅ | **中**——要恰好抬头看向水里；但「有没有看见过」本身就是玩家话题 | 车窗内主观视角，长焦透过水体拍暗色剪影横穿 | 031, 032 |
| 4 | **地铁的老鼠与灭鼠工 Monty**（Year 25 ADP 当下时态） | 地铁月台 | ✅ | 中 | 月台角落低机位近景（捕鼠笼 + 窜过的鼠）→ 中景反打 Monty | 033, 034 |
| 5 | **英雄谷五尊雕像与「推定已故」铭文** | 英雄谷 | ✅ | **强**——入城必经，第一眼 | 步行长镜贴桥面前推 → 长焦贴铜牌特写 | 024, 025 |
| 6 | **城门拱左侧挂着的奥妮克希亚头颅 + 全城 buff** | 城门/英雄谷 | ✅（1.3.0 起，3.2.2 止） | **强**——全服共同时刻，「头挂上了快进城」 | 大仰角拍头颅 → 硬切到广场人群被暖光扫过的中景 | 026–030 |
| 7 | **贸易区的银行 / 拍卖行 / 邮箱三件套** | 贸易区西南 | ✅ | **强**——每次回城的固定三连 | 手持跟随中景穿过三点，喷泉作前景层 | 014–019 |
| 8 | **「旧世拍卖行不通池」** | 贸易区 | ✅（1.9.0 前） | 中——老玩家知道，新玩家会惊讶 | 拍卖行大厅内广角低机位，拍木质告示板 | 014, 077 |
| 9 | **回城找职业训练师（每两级一次）** | 各区 | ✅ | **强**——这是「必须回城」的真实原因 | 室内近景：导师 + 摊开的羊皮卷 | 020, 021 |
| 10 | **运河里的监狱与金库：两座水中石堡** | 运河中段 | ✅ | **强**——所有人都从桥上看见过 | 运河水面低机位，两堡一前一后成纵深；钟塔长焦特写 | 035–040 |
| 11 | **金库那扇从未开过的门** | 运河 | ✅ | 中 | 落闸栅门正面定镜，栅后纯黑 | 040 |
| 12 | **旧城区↔贸易区之间那扇同样打不开的副本门**（原定玩家住宅区） | 旧城区西侧 | ✅ | 中——见过的人多，知道内情的人少 | 短石廊主观推进 → 栅门后幽蓝门户定镜 | 041 |
| 13 | **监狱门口的集合石**（旧世＝自动凑队，非召唤） | 运河/法师区北 | ✅（1.3.0 起） | **强**——22–30 级必打 | 门侧石碑近景 + 石阶上等人的旅人中景 | 037, 038 |
| 14 | **花园区的月亮井与东部王国唯一的德鲁伊训练师** | 花园区 | ✅ | **强**（对德鲁伊玩家是 100% 强制）| 一镜到底环绕月亮井，逆光穿叶，水面自发光为唯一光源 | 043–045, 082, 083 |
| 15 | **已宰的羔羊地窖：术士的召唤法阵** | 法师区 | ✅ | **强**（对术士玩家 100% 强制）| 一层昏暗酒馆定镜 → 下楼梯手持 → 地窖法阵俯拍 | 046–049 |
| 16 | **狮鹫管理员 Dungar：人类，一口矮人腔** | 贸易区东侧坡道上 | ✅ | 中——梗强于记忆 | 坡道仰拍 → 平台上人与鹫的中景 | 022, 050 |
| 17 | **奶酪商 Elling Trias：明面卖酪、暗里是情报节点** | 贸易区 | ✅ | 中 | 铺面中景（奶酪轮堆叠）→ 老板越过顾客肩膀的视线特写 | 051–053 |
| 18 | **运河为什么存在：没做成的贡多拉** | 运河 | ✅（遗迹永久存在） | 中——最好用的「冷知识」之一 | 空无一船的运河水平面低机位长镜 | 042 |
| 19 | **大教堂的钟铸自铁炉堡的大熔炉** | 教堂广场 | ✅ | 中 | 钟楼内部仰拍 → 黄昏钟楼剪影长焦 | 054, 055 |
| 20 | **「连设计师都说这城难走」** | 任意拱廊 | ✅ | 中——老玩家一听就笑 | 拱廊主观视角，左右岔口、无地标 | 056, 057 |
| 21 | **免费牛奶桶** | 各区墙根 | ✅ | 中——法系玩家的集体记忆 | 墙根木桶近景，手伸进画面取走一瓶 | 060 |
| 22 | **运河边钓鱼的人** | 运河 | ✅ | 中 | 石阶垂钓者中景，浮标水面特写 | 061 |
| 23 | **每个区都有苹果树** | 全城 | ✅ | 弱——但是最好的前景层素材 | 街角苹果树作前景，主体在景深后 | 059 |
| 24 | **克萨维厄斯被拉进城的那一天**（2005-03-06） | 城门/贸易区 | ✅ | **强**——旧世最著名的「城市灾难」 | 城门内广场空镜 + 口播；不出现怪物本体 | 064, 065 |
| 25 | **堕落之血瘟疫**（1.7.0 之后） | 全城 | ✅ | 中 | 广场地面尸体轮廓 + 人群空圈中景 | 066 |
| 26 | **城外的天灾浮空城**（1.11.0） | 城外天际线 | ✅ | 中 | 城墙上远眺，浮空城占画面上三分之一 | 067 |
| 27 | **王座厅当众揭穿顾问的那场戏** | 暴风要塞 | ✅ | **强**——旧世最著名的剧情高光之一 | 长焦压缩王座厅大全景，人占画高 1/6 | 068 |
| 28 | **暴风城是唯一城内有副本的联盟首都** | 运河 | ✅ | 中 | 监狱门 + 紧邻商铺的同框中景 | 063 |
| 29 | **卫兵会给你指路** | 各区 | ✅ | 中 | 卫兵指路的手臂延长线接远处目标建筑 | 076 |
| 30 | **「其实旧世大家都泡在铁炉堡」** | 贸易区（对照）| ✅ | **强**——最能戳中老玩家的反差 | 贸易区人流稀疏的中景 + 口播 | 077–079 |
| 31 | **战场管理员（1.6.0 起）** | 暴风要塞 | ✅（1.6.0 后） | 中 | 挂满旗帜的厅室 + 铺着战场地图的长桌 | 023 |
| 32 | **儿童周：领一个孤儿出门** | 教堂广场 | ✅（1.4.0 起） | 中 | 孤儿院门前台阶中景 | 074 |
| 33 | **2002 年的音乐恶作剧** | —— | ✅（开发期轶事） | 弱——纯梗 | 城市空镜 + 口播 | 058 |

（合计 33 个讲解点，其中 Vanilla 可用 33 / 33；不可用的另见 § 不可用清单。）

---

## 前十名详述

排序依据：**记忆强度（机制是否强制 + 是否位于必经之路）× 画面可拍性 × 是否只有旧世才有**。

### 1. 把炉石绑在镀金玫瑰

| 项 | 内容 |
|---|---|
| **讲解点名** | 全联盟最强的一块肌肉记忆：走进贸易区那家旅店，把「家」定在这里。 |
| **在哪** | 贸易区西南角，镀金玫瑰旅店一层，老板娘 Innkeeper Allison 站在柜台后，坐标 [60.6, 75.0]，左边银行、右边拍卖行。 |
| **玩家记忆是什么** | 炉石是 0.6 版（2004-04-13）就在的元老物品（`source_url: https://warcraft.wiki.gg/wiki/Hearthstone`，quote: "Patch 0.6 (2004-04-13): Added."）；绑定的动作是在旅店老板的对话里点那句 "Make this inn your home."；旧世冷却是**一小时**一次（3.1.0 才砍到 30 分钟，quote: "Patch 3.1.0 (2009-04-14): The cooldown reduced to 30 minutes."），要站着念满 10 秒、挨打就断（quote: "The casting process requires 10 seconds and will be interrupted if you take damage."）。而镀金玫瑰之所以成为全服默认绑点，是因为银行、拍卖行、邮箱全在几步之内（`source_url: https://warcraft.wiki.gg/wiki/Gilded_Rose`，quote: "due to its proximity to the bank, Auction House, and an ever-popular mailbox."）。 |
| **版本** | ✅ Vanilla 完整存在。**关键补充**：旧世**全城只有这一家旅店**——猪和哨声的旅店老板 Maegan Tillman 是 4.0.1 才加的，加的时候被明确称作「暴风城的第二家旅店」。 |
| **镜头看到什么** | ① 挂玫瑰招牌的木门与门楣，门内溢出壁炉暖橙光；② 柜台后的老板娘抬头欠身，身后木架摆满面包、苹果、陶罐；③ 柜台木面的划痕与酒渍特写；④ 掌心那枚刻同心符文的灰白石片，凹槽被摩挲得发亮；⑤ 楼上一排简陋客房的木门，门缝透光。 |
| **艾拉能讲什么** | ✅ 设定明载。她可以对镜讲：**这家店的名字，在一整个时代里等于「回家」两个字**——不是因为这里的床好，是因为全城只有这一家能做这件事，而且做完之后，一小时只能用一次。**给她一个「她自己也在柜台前完成了这个动作」的落点**，作为本片的情感锚。 |

### 2. 矿道地铁：坐一趟去铁炉堡

| 项 | 内容 |
|---|---|
| **讲解点名** | 这座城有第二个入口，它在地下、在水下，而且免费。 |
| **在哪** | 矮人区东侧，一条隧道通向月台（`source_url: https://warcraft.wiki.gg/wiki/Dwarven_District`，quote: "The Stormwind City end of the Deeprun Tram line is accessible through a tunnel on the east side of the district."）。 |
| **玩家记忆是什么** | 它是侏儒工程造的全封闭双轨地下铁，两列各三节车厢（quote: "all credited to the gnomes' technical engineering."）；单程 60 秒、到站停 12 秒（quote: "The transit time between each end is 60 seconds and remains at each stop for 12 seconds."）；它是暴风城与铁炉堡之间**唯一一条永久直连**，从暴风城没有任何传送门能去铁炉堡（`source_url: https://warcraft.wiki.gg/wiki/Ironforge`）。玩家社区把它的观感总结为「每天运送成千上万人，方式近乎魔法」（T3，`source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world`）。 |
| **版本** | ✅ Vanilla 完整存在，是旧世联盟通勤的主干道（且因为那时人都在铁炉堡，这条线的客流比现在大得多）。 |
| **镜头看到什么** | ① 隧道口巨大的齿轮形结构仰拍，轨道没入黑暗；② 月台上铆接钢板与铜管构成的壁面，壁灯成串；③ 车厢内侧跟机位，乘客抓立柱随车身轻晃；④ 隧道壁灯以固定节奏一盏盏向后掠过；⑤ 中段钢板让位给整段透明拱形顶壁，壁外是深绿水体。 |
| **艾拉能讲什么** | ✅ 设定明载（车程、造它的是谁、免费、唯一直连均有出处）。她可以讲：**这一分钟，是这座城送给每个人的一分钟**——你什么也做不了，只能看着灯一盏盏往后退。⚠️ 推测部分（须明确标出）：「所以大家都在这一分钟里发呆/聊天」是**玩家社区的普遍说法**，不是设定。 |

### 3. 水下段的 Nessy

| 项 | 内容 |
|---|---|
| **讲解点名** | 隧道中段那面透明壁外面，偶尔会游过一头没人碰得到的巨兽。 |
| **在哪** | 矿道地铁中段——那里其实是一整座**地下湖**（quote: "The underwater section of the tram is, in fact, a subterranean lake."）。 |
| **玩家记忆是什么** | Nessy 是一头索德鲁怪，玩家永远接触不到它（quote: "Nessy is a threshadon boss sometimes seen by travelers on the Deeprun Tram." / "inaccessible to players."），它是对尼斯湖水怪的致敬（quote: "Nessy is a reference to the Loch Ness Monster."）。同一片水里还有巨蚌、两只娜迦海妖、一条姥鲨、沉船和一口宝箱。 |
| **版本** | ✅ Vanilla 存在（Warcraft Wiki 的补丁历史里只有 8.0.1 的「模型更新」，没有「新增」条目，说明它是原生内容）。⚠️ **注意**：Wowhead Classic 的 NPC 页是 JS 渲染，本机抓回来只有 "The location of this NPC is unknown."，所以「它在 Classic 里具体多久刷一次」我没拿到硬数据，正片不要报频率。 |
| **镜头看到什么** | ① 钢板隧道忽然让位给整段透明拱形顶壁；② 壁外深绿浑水，光从上方极弱地漏下；③ 水中倾覆的木船骸骨与一口包铁木箱；④ 一头长颈巨兽的暗色轮廓缓慢横穿，只看得清颈、背脊、尾的剪影；⑤ 车厢内乘客贴着壁面仰头看的背影。 |
| **艾拉能讲什么** | ✅ 设定明载（生物存在、够不着、致敬尼斯湖）。她可以讲：**它就在那儿，而且它永远只是「在那儿」——没人能靠近它、打它、研究它。这座城把一个谜留在了自己的地基底下。** ⚠️ 推测：「很多人坐了好几年都没看见过」属玩家说法，要标明。 |

### 4. 英雄谷五尊雕像与「推定已故」

| 项 | 内容 |
|---|---|
| **讲解点名** | 所有入城者都要从五个「已经死了的人」脚下走过——而他们其实一个都没死。 |
| **在哪** | 城门内的英雄谷，石桥两侧各两尊、桥尽头正中一尊（图拉杨）。 |
| **玩家记忆是什么** | 五尊雕像纪念远征德拉诺的联盟远征军成员（quote: "Five statues commemorate Alliance Expedition members."）。**铭文逐字取回**：图拉杨那块写的是 "Former Lieutenant to Lord Anduin Lothar. Knight of the Silver Hand. High General of the Alliance Expedition that marched into the orc homeworld of Draenor. Presumed deceased."；库德兰 / 卡德加 / 达纳斯三块同样以 "Presumed deceased." 收尾；**只有奥蕾莉亚那块没有这句**。 |
| **版本** | ✅ Vanilla 完整存在，且**旧世正是「他们仍被认为已死」的年代**——这是旧世独有的戏剧性，后续资料片里他们陆续回来了。 |
| **镜头看到什么** | ① 宽石桥两侧的雕像依次从画框两侧掠过（低机位贴桥面前推）；② 三倍真人高的石雕逆光成剪影，看不清脸；③ 基座铜牌的长焦特写，铜面氧化发暗、字口积着灰绿铜锈；④ 末行 "Presumed deceased." 字迹清晰；⑤ 行人从雕像脚下走过，人只占画高 1/6。 |
| **艾拉能讲什么** | ✅ 设定明载（雕像数、身份、铭文原文均有出处）。她可以讲：**这五块牌子写的是同一句话的四遍——「推定已故」。这不是墓碑，是一座城在承认「我们不知道他们怎么了」。** 再指出第五块没写这句，留一个钩子。**不要展开讲他们后来回来了**——那是我们的未来、不是这座城的当下。 |

### 5. 城门拱上的龙头与全城同时亮起的那一下

| 项 | 内容 |
|---|---|
| **讲解点名** | 只要最近有人杀了那条黑龙，她的头就挂在你进城时的左手边——而且全城的人会同时变强两个小时。 |
| **在哪** | 暴风城入城拱门**左侧**（quote: "Onyxia's head used to hang from the left arch into Stormwind City"）。交头的地点在暴风要塞，交给博瓦尔·弗塔根。 |
| **玩家记忆是什么** | 这套机制是 2005-03-07 的 1.3.0 加的、3.2.2 取消；头一挂上，**城里所有 60 级及以下的角色**同时获得「屠龙者的战吼」（quote: "grants the [Rallying Cry of the Dragonslayer] buff to all level 60 or lower characters in Stormwind City."），持续 **120 分钟**。交任务的原文是 "You have accomplished the impossible. The brood mother of the Black Dragonflight lies dead at your feet. Take her head and present it to the Highlord."（`source_url: https://www.wowhead.com/classic/quest=7495/victory-for-the-alliance`）。 |
| **版本** | ✅ Vanilla 完整存在（1.3.0–3.2.2 正好覆盖整个旧世）。 |
| **镜头看到什么** | ① 大仰角：巨大黑龙头颅悬在石拱左侧，粗铁链穿颅骨固定，头比门下行人大出数倍；② 鳞片是暗黑带虹彩的硬甲，獠牙外露、双目已浊；③ **硬切**到广场：密密麻麻的人群同时被一层极淡的暖金薄光自拱门方向扫过；④ 人群纷纷抬头；⑤ 拱门下人流骤然变密，来的方向单一。 |
| **艾拉能讲什么** | ✅ 设定明载。她可以讲：**这是这座城最接近「全民节日」的东西——不是历法上的节日，是一群人在很远的地方赢了，然后整座城在同一秒钟里知道了。** 时长两小时这个数字要念出来（它把「赶紧进城」的紧迫感讲清楚了）。 |

### 6. 运河里的两座水中石堡

| 项 | 内容 |
|---|---|
| **讲解点名** | 运河中段漂着两座石头堡：一座是监狱，一座的门从开服到现在没开过。 |
| **在哪** | 监狱入口在**环绕法师区那段运河的最北端**；金库就在监狱对面，四面环水。 |
| **玩家记忆是什么** | 监狱是「藏在运河区水下的高警戒监狱」，关着小贼、政治犯、杀人犯和全境最危险的一批人（quote 见 fact 035）；进门后顺一小段敞开式石阶直接下去（quote: "directly inside the building, down the small, open set of stairs."）；旧世等级区间 22–30，门口紧挨一块集合石。金库那边则是 "The Vault has never been officially accessible, not even in alpha or beta."，门口是落闸铁栅加两名守卫。**最关键的旧世画面差异**：监狱**旧世是有钟楼的**（后来拆了），金库的钟楼至今还在——所以旧世的运河中段是**两座带钟的石堡隔水相望**。 |
| **版本** | ✅ Vanilla 完整存在，且「两座钟塔」是旧世独有构图。❌ **不要用**金库钟面「停在 8:15」那条——那是死亡之翼袭城之后才有的设定。 |
| **镜头看到什么** | ① 运河水面低机位，两座方形石堡一前一后成纵深，各顶一座方塔圆钟面；② 墙体厚重、开窗极小且装铁栅；③ 落闸铁栅门正面，栅后纯黑门洞，两名守卫一动不动；④ 门厅内一段无扶手石阶直通更暗的地下；⑤ 石阶上坐着三四个等人的旅人，装备粗糙、武器搁在膝上。 |
| **艾拉能讲什么** | ✅ 设定明载。她可以讲：**这座城把两样东西放进了水里——它关起来的人，和它藏起来的东西。一座门天天开，一座门从来没开过。** 「从没开过」这句要落到 "not even in alpha or beta" 这个事实上（口播里换成「从这座城建成起就没开过」）。 |

### 7. 花园区的月亮井

| 项 | 内容 |
|---|---|
| **讲解点名** | 满城石头里唯一一块绿地，它不是给人类准备的。 |
| **在哪** | 城市西角的花园区，从教堂广场往西南、或从法师区往西北走。井在园区中心。 |
| **玩家记忆是什么** | 月亮井是暗夜精灵自己凿的（quote: "The night elves created a Moonwell in the center of the park square."），外形是「石砌水池里盛着会发银光的水」；这里是**整个东部王国唯一有德鲁伊训练师的地方**（quote: "It was the only place in the Eastern Kingdoms where druid trainers resided."）——所以每个东部王国的德鲁伊玩家每两级都得回到这片小树林。它同时是暗夜精灵在这座石城里的避难所（quote: "a refuge for visiting night elves..."）。玩家社区怀念的是它的留白：「老公园有一种活着的城市的感觉」「不是每个角落都得塞满东西，塞满了就没沉浸感了」（T3）。 |
| **版本** | ✅ Vanilla 完整存在。❌ 它在《大地的裂变》被死亡之翼摧毁、后来原址建了雄狮之眠——**正片绝不能出现废墟或雄狮之眠**。 |
| **镜头看到什么** | ① 石砌街道尽头忽然转为草地与林荫，界线清晰得像被刀切开；② 林间空地正中一口圆形石砌浅池，池水冷银色自发光；③ 池沿雕着藤蔓纹；④ 树下三位暗夜精灵长者分立，长袍由树叶与皮革缀成；⑤ 一个人独自坐在井沿上、背对镜头，四周留出大片什么都没有的草地。 |
| **艾拉能讲什么** | ✅ 设定明载（井是谁凿的、这里是唯一的德鲁伊训练地、是暗夜精灵的避难所）。她可以讲：**一整座石头城里，有一小块地是别人借来的——他们在这儿凿了一口井，因为这里让他们想起家。** ⚠️ 推测：「这是全城最安静的地方」是玩家共识而非设定，要标明。**这一站必须放在日落**（W1 已如此排，与本路一致）。 |

### 8. 已宰的羔羊地窖

| 项 | 内容 |
|---|---|
| **讲解点名** | 法师区一间破酒馆，楼上卖酒，楼下是这座城正式承认的术士学校。 |
| **在哪** | 法师区，「已宰的羔羊」酒馆，下楼进地窖与地下墓穴。 |
| **玩家记忆是什么** | 一层只有一个酒保，他劝客人 "stay away from the shadows"；地窖与地下墓穴是**暴风城术士的圣所与训练场**，新人和从卡兹莫丹转来的学徒都在这里受训（quote 见 fact 047）。旧世术士的入门任务原文就是 "you'll find Gakin in the basement of the Slaughtered Lamb in Stormwind."（`source_url: https://www.wowhead.com/classic/quest=1715/the-slaughtered-lamb`）。店名致敬电影《美国狼人在伦敦》。 |
| **版本** | ✅ Vanilla 完整存在，且**对术士玩家是 100% 强制**——旧世每个联盟术士都在这个地窖里站过。 |
| **镜头看到什么** | ① 门外褪色木招牌：一只被后腿倒吊的剥皮羊，铁环锈蚀随风轻晃；② 一层低矮昏暗，只有酒保和两三张空桌，光源只有柜台后一盏油灯；③ 一段窄石阶向下；④ 地窖地面一圈直径两米的召唤法阵，阵线里是暗紫色余烬般的微光；⑤ 壁龛里的蜡烛与粗石墙面。 |
| **艾拉能讲什么** | ✅ 设定明载。她可以讲：**这座城不禁止这门手艺——它只是把它放在楼下。上面照常卖酒，下面照常上课，中间隔着一段楼梯和一句「离阴影远点」。** 讲到店名时可以顺手把《美国狼人在伦敦》的致敬点出来（有出处，✅）。 |

### 9. 没做成的贡多拉

| 项 | 内容 |
|---|---|
| **讲解点名** | 这座城为什么有运河？因为本来要在里面划船，后来放弃了。 |
| **在哪** | 全城的运河，任意一段；最好选一段完全没有船的宽水面。 |
| **玩家记忆是什么** | Warcraft Wiki 的开发笔记逐字写着：**"Originally, the city was planned to feature gondolas that would serve as a quick way to travel from one district to another, hence the existence of the Canals and the fact that players can get in and out of the Canal waters. However, the technology wound up being 'prohibitively esoteric.'"** 换句话说，运河**是一个被砍掉的功能留下来的疤**，连「玩家能下水再爬上岸」这个设定都是当年为贡多拉准备的。 |
| **版本** | ✅ 运河本身 Vanilla 就在；这条开发轶事是永久有效的「城市冷知识」。 |
| **镜头看到什么** | ① 宽阔石砌运河水面，**一条船都没有**；② 两岸整齐石堤，每隔一段有一道下水石阶，阶面被水浸出深色水线；③ 桥拱作前景的低机位纵深；④ 水面倒影里的两岸建筑被涟漪拉长；⑤ 岸边系船用的石桩空着、上面没有缆绳。 |
| **艾拉能讲什么** | ✅ 设定明载（开发者说法有逐字出处）。她可以讲：**这条水道是为了船挖的，可是船一直没来。于是它变成了别的东西——分区的界、钓鱼的地方、监狱的护城河。一个没做成的计划，反而成了这座城的骨架。** 这是全片最适合当「城市哲学小结」的一条。 |

### 10. 「其实旧世大家都泡在铁炉堡」

| 项 | 内容 |
|---|---|
| **讲解点名** | 这座城是联盟的首都——但在很长一段时间里，它不是联盟玩家真正待的地方。 |
| **在哪** | 贸易区街道（用「人流中等、不空也不挤」的画面作对照）。 |
| **玩家记忆是什么** | Warcraft Wiki 明写：各城拍卖行并池之前，**铁炉堡才是联盟活动的中心**（quote: "Before the addition of auction houses in all capital cities, Ironforge was *the* central hub of Alliance activity."）；人挤到玩家给它起了外号「卡炉堡」（quote: "the city was often referred to as 'Lagforge'..."）。暴风城作为高级玩家聚集地的地位一路起伏，**直到 1.10 之后才相对涨起来**（quote: "Since patch 1.10, it has risen in popularity compared to Ironforge (though this may vary by server).")。机制上的原因是：旧世三座联盟拍卖行**各挂各的货**，1.9.0 才并池（quote 见 fact 014）。 |
| **版本** | ✅ Vanilla；且这条**只有旧世成立**——今天的暴风城是毫无争议的联盟中心。 |
| **镜头看到什么** | ① 贸易区街道人流中等：拍卖行门口围着几个人，其余街段只有零散行人；② 空着的摊位与合上的店板；③ 从地铁隧道口方向拍：人流是**朝隧道口去**的，不是从那儿来的；④ 拍卖行大厅内广角，木质告示板前只站着两三个人；⑤ 硬切到英雄谷石桥上，桥面宽而人少。 |
| **艾拉能讲什么** | ✅ 设定明载（wiki 逐字记录了这段社群史）。她可以讲：**一座城最热闹的地方，不一定由建它的人决定。这里有王座、有大教堂、有五尊雕像——可大家都在山那头，因为那头的集市能卖得出东西。** 结尾接第 2 条（地铁）：**那条地铁不是观光线，它是通勤线。** ⚠️ 推测：「所以暴风城当年很冷清」——冷清到什么程度没有硬数据，口播里不要给量化描述。 |

---

## 一条「玩家记忆」路线建议

设计原则：**不另起一条路线，而是把 W9 的讲解点挂到 W1 那条 17 站逆时针闭环上**，
让每一站在「看这座城」之外再多一层「你站过这儿」。下表左列是 W1 的站号，
右列是本路要在那一站加的东西。W1 没有的站我只加了两个（★ 标出），都在原路线的顺路位置上。

| W1 站号 | 站点 | W9 在此站叠加的玩家记忆层 | 回指讲解点 |
|---|---|---|---|
| 0 | 城门外 | —— | —— |
| 1 | 英雄谷石桥 + 五尊雕像 | **五块铭文的「推定已故」**；**城门拱左侧的龙头 + 全城 buff**（若按「刚有人交了头」的设定拍，这是全片最强开场之一） | 5 / 6 |
| 2 | 贸易区喷泉与拍卖行 | **银行/拍卖行/邮箱三件套**；**旧世拍卖行不通池**；**交易频道的刷屏文化**（口播） | 7 / 8 / 33 |
| 3 | 镀金玫瑰旅店（先订房） | **★核心：绑炉石**——把 W1 原本的「订房」升格成本片的情感锚；顺带点明「全城只有这一家」 | 1 |
| ★3b | 旅店门外街口（贸易区东侧坡道下） | **狮鹫管理员 Dungar：人类却一口矮人腔**；**奶酪商 Elling Trias**（两家都在贸易区，顺路，不额外绕） | 16 / 17 |
| 4 | 贸易区↔旧城区的运河与铁闸门 | **那扇从未启用的副本门（原定玩家住宅区）**——W1 已经在这站拍了铁闸门，本路给它一个身份 | 12 |
| 5 | 旧城区窄巷 + 猪和哨声 | **「这家酒馆在这个年代还没有旅店老板」**——反向点题，呼应第 3 站 | 1（反面） |
| 6 | 指挥中心 / SI:7 门口 | **SI:7 在几乎每个城区都有「朋友」**（回扣第 3b 站的奶酪铺） | 17 |
| 7 | 暴风要塞吊桥 → 王座厅 | **王座厅当众揭穿顾问的那场戏**；**战场管理员** | 27 / 31 |
| 8 | 要塞外墙俯瞰全城 | **「连设计师都说这城难走」**（从唯一能看清全局的位置讲「在下面根本看不清」，反差最大）；**每个区都有苹果树**（俯拍时点出） | 20 / 23 |
| 9 | 矮人区锻造广场 | **免费牛奶桶**（墙根木桶，顺手取一瓶） | 21 |
| 10 | 矿道地铁隧道口 | **★核心：坐一段地铁**——**水下段的 Nessy**、**老鼠与灭鼠工 Monty**、**唯一直连**、**60 秒车程**；回程时口播 **「其实旧世大家都泡在铁炉堡」** | 2 / 3 / 4 / 30 |
| 11 | 教堂广场 + 光明大教堂 | **钟铸自铁炉堡的大熔炉**（黄昏钟声正好对上「每天日落敲一次」） | 19 |
| 12 | 公墓与市政厅 | **孤儿院与儿童周**（就在同一广场） | 32 |
| 13 | 花园区月亮井（日落） | **东部王国唯一的德鲁伊训练师**；**暗夜精灵的避难所**；玩家社区对「留白」的怀念 | 14 |
| 14 | 法师区巫师圣殿 | ⚠️ **此站必须改**——W1 原案写了「传送门房间」，那是 8.1.5 才有的。旧世这座塔里只有法师训练师，**改拍塔外盘旋楼梯的垂直上摇 + 塔内螺旋梯**，不拍传送门 | 见 § 不可用清单 |
| 15 | 已宰的羔羊地窖 | **★核心：术士的召唤法阵**；店名致敬《美国狼人在伦敦》 | 15 |
| 16 | 运河上看监狱与金库 | **两座带钟的水中石堡**（旧世独有构图）；**金库那扇从没开过的门**；**监狱门口的集合石**（旧世＝自动凑队）；**城内副本是联盟独一份** | 10 / 11 / 13 / 28 |
| ★16b | 运河石阶（顺路，就在 16 与 17 之间） | **运河边钓鱼的人**（巨型鲶鱼、运河蟹）；**没做成的贡多拉**——这是全片最好的「城市哲学小结」落点，放在倒数第二站 | 22 / 18 |
| 17 | 回镀金玫瑰住店 | **收尾呼应第 3 站**：她自己用掉了那块石头 / 或者只是走回来睡觉。**「一小时一次」这个数字在这里再念一遍**，把一天收住 | 1 |

**三条「远方战事」口播（克萨维厄斯 / 堕落之血 / 天灾浮空城）的安排建议**：
它们都是**城市尺度的灾难回忆**，不属于任何一个具体站点。建议**不新设站**，
而是挂在 8（俯瞰全城）与 16（运河纵深）两个大景别镜上做口播——大景别 + 灾难口播
是最省镜次也最有压迫感的组合。天灾浮空城那条要放在**能看见城外天际线**的位置（站 8）。

---

## 不可用清单（❌，一律不得进正片）

| # | 东西 | 为什么不能用 | 出处 |
|---|---|---|---|
| 1 | **巫师圣殿的传送门大厅** | **8.1.5（2019）才建的**。旧世那座塔里只有法师训练师，没有通往各城的传送门阵列。W1 路线草案第 14 站写了「传送门房间用广角低机位」——**必须改掉** | "With patch 8.1.5, the tower's interior was completely revamped to house the Stormwind Portal Room" · https://warcraft.wiki.gg/wiki/Wizard%27s_Sanctum |
| 2 | **猪和哨声的旅店老板 / 在那儿绑炉石** | 老板娘 Maegan Tillman 是 **4.0.1** 才加的，加时被称作「暴风城的第二家旅店」——旧世只有镀金玫瑰 | https://warcraft.wiki.gg/wiki/Pig_and_Whistle_Tavern |
| 3 | **把集合石当「召唤石」用** | 旧世集合石是**自动帮等级合适的人凑队**；变成类似术士召唤是 **2.0.1（2006-12-05）** 的事 | "Patch 2.0.1 (2006-12-05): Meeting Stones now function similar to a Warlock Summon spell." · https://warcraft.wiki.gg/wiki/Meeting_stone |
| 4 | **集合石「15 级即可使用、无上限」** | 那是 **3.3.0** 的规则；旧世有等级区间限制（监狱段是 21–29） | https://warcraft.wiki.gg/wiki/Meeting_stone |
| 5 | **暴风城港口** | **3.0.2（2008-10-14）** 才加 | "Patch 3.0.2 (2008-10-14): Added." · https://warcraft.wiki.gg/wiki/Stormwind_Harbor |
| 6 | **金库钟面「停在 8:15」** | 那是死亡之翼袭城之后的设定（并且是对广岛的致敬）；旧世的钟是正常走的 | https://warcraft.wiki.gg/wiki/Stormwind_Vault |
| 7 | **监狱没有钟楼** | 反了——**旧世的监狱是有钟楼的**，后来才拆。正片必须把它画出来 | "used to have a clock tower, which has now been removed" · https://warcraft.wiki.gg/wiki/Stormwind_Stockade |
| 8 | **监狱里的霍格 / 兰多夫·莫洛克 / 监狱暴动剧情** | 霍格进监狱、暴动、Rifle Commander Coe 平乱都是 **4.0.3a 重制版**的内容 | "Completely revamped in Patch 4.0.3a (November 23, 2010)" · https://warcraft.wiki.gg/wiki/The_Stockade |
| 9 | **矮人区的第二座拍卖行与皇家银行** | **4.0.3a** 才加（W1 已列，本路复述以防误植） | https://warcraft.wiki.gg/wiki/Stormwind_Counting_House |
| 10 | **贸易区的骑术训练师 / 飞行坐骑商人** | 《大地的裂变》才加；**旧世人类的骑术训练师与马匹商人在艾尔文森林的东谷伐木场**（Randal Hunter / Katie Hunter），不在城里 | "In Cataclysm... a flight trainer and flying mount vendor have been added." · https://warcraft.wiki.gg/wiki/Trade_District |
| 11 | **拍卖行叫「Trader's Hall」这个名字** | 建筑旧世就在，但**这个名字是 4.0.3a 改的** | "renamed to Trader's Hall" · https://warcraft.wiki.gg/wiki/Trader%27s_Hall |
| 12 | **半淤浅、长着芦苇的运河** | **4.0.3a** 把运河改成半填淤泥＋芦苇＋杂物；旧世是深水 | "canals became halfway filled in with mud/silt, along with occasional reeds and lost debris." · https://warcraft.wiki.gg/wiki/Canals_(Stormwind_City) |
| 13 | **运河里的下水道巨兽（Sewer Beast）稀有怪** | 这条出现在当前版本的说明里；旧世没有这个稀有怪 | https://warcraft.wiki.gg/wiki/Stormwind_City |
| 14 | **教堂广场的婚礼凉亭** | **4.0.3a** 加的 | "A gazebo perfect for weddings was added during the Cataclysm redesign (Patch 4.0.3a)." · https://warcraft.wiki.gg/wiki/Cathedral_Square |
| 15 | **教堂广场的乌瑟尔雕像** | 《大地的裂变》之后才替换掉阿隆索斯·法奥的那尊 | https://warcraft.wiki.gg/wiki/Cathedral_Square |
| 16 | **冠军大厅 / 东部地祇之座 / 雄狮之眠 / 理发店** | 全是 TBC 及之后的建筑 | https://warcraft.wiki.gg/wiki/Stormwind_City |
| 17 | **炉石 30 分钟冷却** | 旧世是一小时；30 分钟是 **3.1.0（2009-04-14）** | https://warcraft.wiki.gg/wiki/Hearthstone |
| 18 | **炉石绑定用语「Bind your hearthstone to this inn.」** | 那是 **11.2.7（2025-12-02）** 改的措辞；旧世是 "Make this inn your home." | https://warcraft.wiki.gg/wiki/Hearthstone |
| 19 | **安其拉战争物资在暴风城收集** | 联盟的收集点是**铁炉堡的军事区**，不在暴风城 | "The Alliance needs to gather in the Military Ward of Ironforge" · https://warcraft.wiki.gg/wiki/Ahn%27Qiraj_War_Effort |
| 20 | **冬幕节的大圣诞树在暴风城** | 旧世联盟那棵树和冬天爷爷在**铁炉堡** | "gifts are available underneath the trees near Greatfather Winter in Ironforge, and Great-father Winter in Orgrimmar." · https://warcraft.wiki.gg/wiki/Feast_of_Winter_Veil |
| 21 | **「屠龙者的战吼」来自奈法利安之首** | 旧世的来源是**奥妮克希亚之首**；换成奈法利安是 **3.2.2** 之后的事 | https://warcraft.wiki.gg/wiki/Rallying_Cry_of_the_Dragonslayer |
| 22 | **屠龙者战吼「10% 暴击 + 10% 主属性」这套数值** | 那是 **8.0.1 重做后**的效果，不是旧世数值 | "Patch 8.0.1 (2018-07-17): Effect redesigned" · https://warcraft.wiki.gg/wiki/Rallying_Cry_of_the_Dragonslayer |
| 23 | **2008 年那场有阵营领袖对白、每半小时一波精英的天灾入侵** | 那是 **3.0.2** 版；旧世（1.11.0）那次只有城外的浮空城与零星刷怪 | https://warcraft.wiki.gg/wiki/Scourge_Invasion |
| 24 | **花园区的废墟 / 大灾变后的雄狮之眠** | 花园区在旧世是完好的 | https://warcraft.wiki.gg/wiki/The_Park |
| 25 | **给当地人写台词**（旅店老板、灭鼠工、卫兵、术士导师……） | 系列铁律：当地人零台词。上面引用的所有 NPC 台词**只作为设定证据**，不得进入成片音轨 | 本项目规则 |

---

## 未查 / Open questions

1. **旧世炉石冷却的官方数字**。我拿到的硬证据只有「3.1.0 把它降到 30 分钟」这一条，
   由此**推出**此前更长；「一小时」这个数字目前只有玩家社区一致说法支撑（Vanilla WoW Wiki 全站 402）。
   **建议**：正片里说「在那个年代，这块石头一小时只能用一次」时，把它当 ⚠️ 处理，
   或改成有硬证据的说法「后来它才被缩短到半小时」。

2. **Nessy 在 Classic 的出现频率 / 触发条件**。Wowhead Classic 的 `npc=10942` 页是 JS 渲染，
   本机只抓到 "The location of this NPC is unknown."。**正片不要报任何频率**（「几百次才见一次」之类）。

3. **旧世贸易区喷泉的确切形制**。W1 也列了这条未决项（只确证「有一座喷泉，拍卖行在它正北」）。
   本路同样没能补上——建拍卖行门口那一组镜时按 W1 的 `prompt_string` 走。

4. **贸易区那个「众所周知的邮箱」的确切位置**。只确证「银行、邮箱、旅店在贸易区西南侧」，
   没拿到坐标。建模时按「三点围成一个小广场、邮箱在街心」处理，并在 previz 里标为待核。

5. **旧世卫兵指路能指到哪几个点位的完整清单**。`warcraft.wiki.gg` 的 Guard 条目只有一句总述；
   细节在 Vanilla WoW Wiki（402）。**正片只讲「卫兵会指路」，不要列清单。**

6. **战场管理员在旧世暴风城的确切位置**。Battlemaster 条目给的「War Room / Stormwind Keep」
   可能是当前版本的位置。要用这一站的话需要再核一次 1.x 的位置。

7. **旧世暴风城到底有多冷清**。有「铁炉堡才是中心」「1.10 之后暴风城才涨起来」两条硬证据，
   但没有任何量化数据。**口播里不要说「空城」「没人」这类量化描述。**

8. **「运河里可以游泳/爬上岸」这条是否在旧世成立**。开发笔记把它和贡多拉绑在一起讲
   （"the fact that players can get in and out of the Canal waters"），语气是「一直如此」，
   但没有明确的版本标注。若要拍艾拉下水或看人下水，**先标 ⚠️**。

9. **暴风城主题曲的曲目编号与官方曲名**。作曲者 Jason Hayes 有多个来源印证，
   但我没能抓到 `warcraft.wiki.gg` 上的官方原声带条目（两个候选 URL 都 404）。
   **音乐层若要写进 shot，先按「城市主题曲」泛指处理。**

10. **「贸易区喷泉边等队友 / AFK」这个玩家习惯**。这是任务书点名要查的一条，
    但我在 T0–T2 层**没有找到任何可引用的出处**，只有零散的论坛观感。
    **本路不把它写成事实**。若要用，必须在口播里明说是「玩家自己的习惯」，
    并且最好改成有硬证据的等价物——**监狱门口石阶上等人**（集合石在那儿，fact 037/038 支撑）。

---

## 来源损失记录

| 站点 | 症状 | 替代方案 |
|---|---|---|
| `*.fandom.com`（Wowpedia / Vanilla WoW Wiki / WoWWiki） | **全站 HTTP 402** | 改用 `warcraft.wiki.gg`（同源内容，且可用 `?action=raw` 取原始 wikitext——**这条路取回的逐字引文质量最高，强烈建议下游沿用**） |
| Wowhead Classic 的 `npc=` / `zone=` 页 | JS 渲染，抓回空壳 | `quest=` 页可用（本文两条术士/龙头任务原文就是从那儿取的）；NPC/zone 数据改走 wiki |
| `rpgamer.com` | HTTP 403 | 改用 Kotaku 同题报道 |
| `massivelyop.com` | HTTP 403 | 未替代（该条目标记为未取） |
| `www.dvorakgaming.com` | DNS 解析失败（EAI_AGAIN） | 地铁史料改由 `Deeprun_Tram?action=raw` 取全 |
| `blizzardwatch.com/gallery/stormwind-city/` | 图集正文懒加载，抓不到 caption | 未替代；该图集本可作为「旧世暴风城长什么样」的视觉对照，**建议人工打开核对一次** |
| `techradar.com` | 正文被会员墙截断 | 改用 Kotaku |
| `warcraft.huijiwiki.com`（中文） | W1 报告记录为全站 403，本路未再尝试 | 中文译名沿用 W1 的 T3 标注 |
