---
worker_id: researcher-w1-city-layout
stage: 0
role: researcher
angle: city-layout
status: complete
blockers: []
confidence: high
---

# W1 · 暴风城城市地理与分区布局（版本锚点＝经典旧世 Vanilla / WoW 1.x）

## 本路说明（下游必读）

1. **版本锚点**。本文所有 ✅ 条目已按「经典旧世（1.x / Classic，大地的裂变之前）」过滤。
   Warcraft Wiki 的主条目写的是**当前版本**，凡是 Cataclysm 及之后才出现的特征（港口 /
   雄狮之眠 / 城外郊区 / 矮人区第二个拍卖行与银行 / 理发店 / 半淤浅的运河 / 重制过的要塞内部）
   我都单独挑出来放进 § 版本错置清单，正片不得出现。
2. **分区数**。经典旧世的暴风城是 **6 个有正式区名的城区**（贸易区 / 旧城区 / 法师区 /
   矮人区 / 教堂广场 / 花园区）＋ **暴风要塞**（王城本体，独立子区）＋ **英雄谷**（城门内外的
   入城谷地），共 8 个可指认的地名块，中间由 **运河** 串起来。任务书里说的「八区」就是这 8 块。
   **暴风城港口不在其中**——它是 3.0.2 才加的。
3. **坐标的来源与可信度（重要）**。分区相对位置我拿到了两套互相独立的数据：
   一套是 T1 wiki 的**文字方位描述**（「贸易区以东是旧城区」之类），
   一套是玩家整理的 **GM 传送世界坐标表**（map=0 zone=1519，单位＝码）。
   两套**逐条互相印证、无一冲突**（见 § 综合 · 八区关系图 的对账），所以我把坐标条目标 ✅
   但 `tier` 老实写 T3，`source` 写明是玩家整理表。下游建 Blender 用坐标没问题，
   **口播里不要把码数当官方数字念**。
4. **单位换算**。魔兽世界坐标单位＝码（yard），1 码 ＝ 0.9144 m；
   世界坐标系 **+X ＝ 正北，+Y ＝ 正西，+Z ＝ 上**。本文的「东/北/高」米制相对坐标
   已按此换算，原点取城门（英雄谷入口）。
5. **官方简体中文译名**。区名我拿到了中文译名（贸易区 / 旧城区 / 法师区 / 矮人区 /
   教堂广场 / 花园区 / 暴风要塞 / 英雄谷 / 运河 / 暴风城监狱 / 矿道地铁），
   但**中文维基（灰机 wiki）全站对本机 403**，只能从可抓取的中文页与搜索结果取证，
   所以中文译名条目的 tier 我标 T3，并在 § 未查 里列出需要复核的几个。

---

## 事实注册表

### A. 整城骨架

```yaml
- fact_id: stormwind.city.001
  claim: 暴风城由若干个大致呈矩形的城区组成，城区之间由运河分隔。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Districts 开篇
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The city is made up of roughly rectangular districts separated by canals."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌人类王城，若干近似矩形的街区被宽阔石砌运河分隔，街区边缘是整齐的石堤与栏杆"
  negative: "圆形城区, 无水道, 土路村落, 现代街道"

- fact_id: stormwind.city.002
  claim: 每个城区都被运河环绕，城区之间靠跨越运河的桥连接；运河边有许多码头，市民在那里钓鱼。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Canals and the prisons
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Each district is bordered by shimmering blue canals and linked by bridges spanning over them. Anglers fish from the many docks in the city, the freshwater fish within perfect quarry for the beginning fisherman."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "碧蓝运河环绕石砌街区，石拱桥横跨水面，沿岸设木质小码头，市民坐在码头边垂钓"
  negative: "浑浊污水, 无桥, 铁桥, 混凝土护岸"

- fact_id: stormwind.city.003
  claim: 运河是一套贯穿全城、把各城区彼此分开的水道系统，其所在区域本身有个名字叫「运河区」；水道两侧有大理石步道与码头，还开着几间店铺。
  tag: ✅
  source: Warcraft Wiki — Canals (Stormwind City), 开篇
  source_url: https://warcraft.wiki.gg/wiki/Canals_(Stormwind_City)
  quote: "The Canals, located in the Canal District, are a series of waterways that wind their way through Stormwind City, separating each of its various districts. While these canals are mostly used for thoroughfare, they do house a few shops overlooking the marble pathways and docks, and it is a popular area for fishermen to spend time hauling small catches."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河两岸的大理石步道，沿街嵌着一排小店面的门脸与招牌，店门正对水面，水边有系船石桩"
  negative: "泥岸, 无店铺的空旷河堤, 现代商店橱窗"

- fact_id: stormwind.city.004
  claim: 经典旧世的运河是**深水**；运河被淤泥半填成浅水是《大地的裂变》4.0.3a 补丁才改的。
  tag: ✅
  source: Warcraft Wiki — Canals (Stormwind City), §Patch changes / §Trivia
  source_url: https://warcraft.wiki.gg/wiki/Canals_(Stormwind_City)
  quote: "Patch 4.0.3a: Redesign with new thoroughfares, new NPCs, and new shops. Canals now halfway filled in with mud/silt, along with occasional reeds and lost debris."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "深而清澈的碧蓝运河水，水面到石堤顶有明显落差，能看见水下暗色的石砌河床"
  negative: "浅滩, 淤泥, 芦苇丛, 露出水面的杂物, 能涉水走过去的浅水"

- fact_id: stormwind.city.005
  claim: 暴风城之所以有运河，是因为开发时原计划做「贡多拉」作为城区之间的快速交通工具，后来因技术过于复杂而砍掉，运河留了下来。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia（引 John Staats 访谈 + 《World of Warcraft Diary》）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Originally, the city was planned to feature gondolas that would serve as a quick way to travel from one district to another, hence the existence of the Canals and the fact that players can get in and out of the Canal waters."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.006
  claim: 设计师 John Staats 称暴风城「设计起来格外痛苦」，因为布局本身就绕，加上开发期大部分时间没有小地图，很多人进城后会迷路、找不到城门。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia（引 MMO-Champion 的 John Staats 访谈）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Stormwind was \"especially painful\" to design due to its confusing layout and the fact that the minimap functionality didn't exist for the majority of WoW's development, meaning that many who entered Stormwind would get lost and be unable to find the city gates."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.007
  claim: Staats 还回忆暴风城最初可能规划了九个城区，其中两个后来被合并成了一个区域。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Staats also recalls that Stormwind may have originally had nine districts, two of which were fused into a single area."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.008
  claim: 城内每一个城区都长着苹果树。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia（引任务 The King's Cider）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Apple trees can be found in every district of Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌街区的角落里长着结果的苹果树，枝叶探出院墙，树下散落几颗红苹果"
  negative: "棕榈树, 松树, 无果实的行道树, 樱花"

- fact_id: stormwind.city.009
  claim: 全城的指路牌都指向「暴风城大门」。
  tag: ✅
  source: Warcraft Wiki — Stormwind Gate
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Gate
  quote: "Signs can be found throughout the human capital city pointing to Stormwind Gate."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街角立着的木质指路牌，牌面刻着箭头与地名，木色深、包铁角，钉在石柱上"
  negative: "现代路牌, 灯箱, 霓虹, 拉丁字母以外的现代字体"

- fact_id: stormwind.city.010
  claim: 旧城区与贸易区之间有一道大铁闸门，门后是一个从未启用的副本传送门，原本打算通向玩家住宅区；该门在《大地的裂变》中被移除——也就是说**经典旧世时它还在**。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia（引 2004 Blizzard 粉丝站访谈）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The unused instance portal behind a large portcullis between the Old Town and the Trade District (removed in Cataclysm) was originally meant to lead to the player housing area."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一道厚重的铁栅升降闸门嵌在石墙里，门后是黑暗的通道，门前无人、常年紧闭"
  negative: "敞开的门, 木门, 有守卫在放行, 门后有光"
```

### B. 城门与入口

```yaml
- fact_id: stormwind.district.001
  claim: 英雄谷（Valley of Heroes）是「城门内外」那一整块谷地，含城门本身。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Districts 列表
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The Valley of Heroes (area beyond and including the city gate)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.002
  claim: 暴风城的巨大城门高过艾尔文森林的树冠；门后就是英雄谷——一处被一座宏伟石桥跨越的天然盆地，桥直通贸易区。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Valley of Heroes
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Stormwind City's great gates tower over the treetops of Elwynn Forest. Beyond them lies The Valley of Heroes, a beautiful natural basin spanned by a majestic bridge leading to the city's trade district."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "巨型石砌城门高耸于森林树冠之上，门洞深邃，门后是一处开阔的绿色谷地盆地，一座宽阔的石桥横跨谷底直通城内"
  negative: "木栅门, 吊桥, 城门低矮, 门外是荒漠, 现代拱门"

- fact_id: stormwind.district.003
  claim: 英雄谷位于城市**南侧**；一座石桥跨过一道狭窄的护城水面，是所有入城者看到的第一样东西。
  tag: ✅
  source: Warcraft Wiki — Valley of Heroes, 开篇
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "The Valley of Heroes is a valley that lies before Stormwind Gate. A bridge of stone crosses the narrow moat and is the first sight of all who enter. This gloriously lush valley lies south of the city"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座厚重的石桥跨过一道窄护城河，桥面宽阔可容马车并行，桥两端连着绿意盎然的谷地草坡"
  negative: "窄木桥, 宽阔大河, 吊索桥, 无水的桥"

- fact_id: stormwind.district.004
  claim: 桥两侧立着五尊巨大的第二次战争英雄雕像——左侧是库德兰·蛮锤与大法师卡德加，右侧是部队指挥官达纳斯·托尔贝恩与游侠上尉阿莱瑞亚·风行者；主路尽头、正要分岔进城之处立着远征军统帅图拉杨。
  tag: ✅
  source: Warcraft Wiki — Valley of Heroes, §Post-Second War
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "On the left are Kurdran Wildhammer, Thane of Aerie Peak, and the Archmage Khadgar of the Kirin Tor; on the right are Force Commander Danath Trollbane and Ranger-Captain Alleria Windrunner; at the end of the main road, just before it splits to enter Stormwind City proper, is General Turalyon, the expedition's military leader."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "桥两侧各立两尊数层楼高的石质英雄立像，基座刻铭牌；主路尽头正中另立一尊统帅像，路在像前分成左右两岔"
  negative: "金属雕像, 骑马像, 现代纪念碑, 雕像只有一尊, 抽象雕塑"

- fact_id: stormwind.district.005
  claim: 主路在图拉杨像前分岔——左岔与右岔各站着一名军官（圣骑士与元帅），一名骑马的将军在谷中巡视。
  tag: ✅
  source: Warcraft Wiki — Valley of Heroes, 开篇
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "Astride his tall stallion is General Hammond Clay ... Down the left fork of the bridge is the paladin, Major Mattingly, and down to the right stands Field Marshal Stonebridge."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "入城主路在雕像前分成左右两岔，各岔口站着一名披甲军官，谷地中央一名将军骑在高大战马上缓行"
  negative: "路不分岔, 军官骑马站在桥上, 无人守卫"
  note: "tier 应为 T1；将军的名字在经典旧世是 General Marcus Jonathan，Hammond Clay 是后期替换——见版本错置清单。"

- fact_id: stormwind.district.006
  claim: 暴风城大门把城市与艾尔文森林隔开，位置就在艾尔文森林与英雄谷之间；门外（艾尔文森林地界）站两名城卫兵，门内（暴风城地界）也站两名。
  tag: ✅
  source: Warcraft Wiki — Stormwind Gate
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Gate
  quote: "Stormwind Gate is a massive gate that separates Stormwind City from Elwynn Forest. It is located between Elwynn Forest and the Valley of Heroes. ... Two Stormwind City Guards stand just outside the gate (Elwynn Forest zone) and two stand just inside the gate (Stormwind City zone)."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "巨大石门洞两侧各立两名穿蓝金配色板甲、持长戟的人类卫兵，门内门外对称站位"
  negative: "无人值守, 卫兵只有一人, 卫兵着皮甲, 门口有检查站栏杆"

- fact_id: stormwind.district.007
  claim: 暴风城有三个入口：英雄谷（陆路正门）、矿道地铁、暴风城港口——但**港口是 3.0.2 才加的**，所以经典旧世只有前两个。
  tag: ✅
  source: Warcraft Wiki — Valley of Heroes 开篇 ＋ Stormwind Harbor §Patch changes
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "it is one of three entrances to Stormwind (the others are the Deeprun Tram, and the Stormwind Harbor)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.008
  claim: 暴风城港口（Stormwind Harbor）是补丁 3.0.2（《巫妖王之怒》）才加入的，经典旧世**不存在**。
  tag: ❌
  source: Warcraft Wiki — Stormwind Harbor, §Patch changes
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Harbor
  quote: "Patch 3.0.2: Added."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "暴风城港口, 码头栈桥, 大帆船, 船坞, 海岸线, 岸炮, 攻城车"
```

### C. 贸易区（Trade District）

```yaml
- fact_id: stormwind.district.010
  claim: 贸易区位于暴风城正中，永远人声鼎沸，是城里买东西最全的地方；全城**一半**的银行、拍卖行与旅店，以及本地的狮鹫管理员都在这里。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Trade District
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The Trade District lies in the center of Stormwind City and is always bustling with activity. It is the place in the city where people can get most goods. Half of the city's banks, auction houses, and inns, as well as the local gryphon master, are all located within."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "人流拥挤的石砌广场式商业街区，两侧密排店面与摊位，招牌成排，行人叫卖声不断"
  negative: "空旷冷清, 无摊位, 现代商场, 夜市霓虹"

- fact_id: stormwind.district.011
  claim: 贸易区又叫「集市区」（Bazaar District），位置就在从正门进城后的第一块地方。
  tag: ✅
  source: Warcraft Wiki — Trade District, 开篇（引 2003 年 Blizzard 官网城市页存档）
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The Trade District (also referred to as the Bazaar District) is just inside Stormwind City from the main gate."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.011b
  claim: 贸易区内的走法：银行、邮箱、旅店在贸易区的**西南侧**；狮鹫管理员在**东侧一道坡道上去**。
  tag: ✅
  source: Warcraft Wiki — Trade District
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The bank, mailbox, and inn are on the southwest side of the Trade District. The Gryphon Master is up a ramp on the east side."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一道石砌坡道沿建筑外墙盘上二层平台，平台上是露天的狮鹫栖架"
  negative: "电梯, 木梯, 螺旋楼梯, 狮鹫在地面"

- fact_id: stormwind.district.012
  claim: 贸易区正中有一座喷泉，拍卖行在贸易区西部、喷泉正北。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Auction House → Trade District Auction House）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "It is in the western portion Trade District, just north of the fountain."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌圆形喷泉立在街区中央的开阔地上，水柱不高，池沿坐着歇脚的市民，四周被店面环绕"
  negative: "现代音乐喷泉, 大理石天使雕像喷泉, 干涸的喷泉池"

- fact_id: stormwind.district.013
  claim: 贸易区的银行叫「暴风城金库」（Stormwind Counting House），就在贸易区靠正门那一侧。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Bank → Trade District Bank）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "Stormwind Counting House is located by the front gates in the Trade District of Stormwind. And when you get tired of counting your money, be sure to stop by the Gilded Rose for a drink."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座敦实的石砌两层建筑，正门高大厚重、包铁，门楣上挂着钱币图案的招牌"
  negative: "玻璃幕墙, 柜台窗口, 现代银行标志, ATM"

- fact_id: stormwind.district.014
  claim: 贸易区的旅店叫「镀金玫瑰」（The Gilded Rose），在贸易区西侧；卫兵形容它有柔软的鹅绒床和热水澡。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Inn → Trade District Inn）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "Ah, The Gilded Rose... with its soft down beds and warm baths... just thinking about that Inn makes me want to... ::yawn:: Lucky you if you're heading over there... you will find it in the west side of the Trade District."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "两层木石混构的旅店，一层是酒馆大堂、壁炉燃着，二层是客房，窗口透出暖黄灯光，门口挂着雕花的招牌"
  negative: "现代酒店, 前台, 电梯, 冷色灯光, 霓虹招牌"

- fact_id: stormwind.district.015
  claim: 暴风城接待中心（Visitor's Center）在贸易区，正是从英雄谷进城后第一眼看到的建筑之一；公会管理员就在进门左手边。
  tag: ✅
  source: Warcraft Wiki — Trade District ＋ Stormwind City Guard 指路
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The Guild Master is to the left in the Visitor's Center when you come in and can help you make a guild or a guild tabard."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一栋敞开大门的公共厅堂建筑，门厅高阔，两侧设长桌与卷宗架，墙上挂着一排纹章旗帜"
  negative: "售票窗口, 排队栏杆, 现代接待台"

- fact_id: stormwind.district.016
  claim: 贸易区还有崔亚斯家与加利纳家分别经营的奶酪铺与酒庄。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Trade District
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "For those with a taste for the delectable, the Trias and Gallina families run cheese and wine shops out of the Trade District as well."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "临街的奶酪铺，柜台上叠着整轮的黄褐色奶酪，货架挂着腌肉；隔壁酒庄门口堆着木桶与酒瓶架"
  negative: "冷柜, 塑料包装, 现代货架, 价签牌"

- fact_id: stormwind.district.017
  claim: 贸易区售卖的货品包括奶酪、奥术物品与材料、杂货、鲜花、布甲/皮甲/锁甲、弓、枪和衣物。
  tag: ✅
  source: Warcraft Wiki — Trade District
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The goods that are sold in the Trade District are cheese, arcane goods and reagents, general goods, flowers, cloth/leather/mail armor, bows, guns, and clothes."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "沿街摊位分门别类：鲜花摊、布料摊、皮革摊、弓与火枪架、成排陶罐与草药袋"
  negative: "电子产品, 塑料玩具, 现代商品, 统一制式摊位"

- fact_id: stormwind.district.018
  claim: 邮箱不集中在一处，而是散布全城——凡是拍卖行、银行、旅店门口都有一个。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Mailbox）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "Mailboxes are scattered throughout the city. You can find one in front of any auction house, bank or inn."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一个齐腰高的绿铜色金属邮箱立在建筑门前的石阶旁，箱盖是斜的，正面有投信口"
  negative: "现代邮筒, 红色邮箱, 邮局柜台, 快递柜"

- fact_id: stormwind.district.019
  claim: 「拍卖行在贸易区中央」这件事是补丁 1.9.0 才落地的——该补丁给暴风城等地新增了拍卖师，并把铁炉堡/暴风城/达纳苏斯的拍卖行联通成同一个联盟拍卖池。
  tag: ✅
  source: Warcraft Wiki — Auction House, §Patch changes（Patch 1.9.0 原文）
  source_url: https://warcraft.wiki.gg/wiki/Auction_House
  quote: "Auctioneers have been added in Undercity, Thunder Bluff, Stormwind City, Darnassus, Everlook, and Booty Bay."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: "1.9 之后（含 1.12 / Classic 正式服）贸易区确有拍卖行；若剧情锚定 1.9 之前则不应出现。"
```

### D. 旧城区（Old Town）

```yaml
- fact_id: stormwind.district.020
  claim: 旧城区在贸易区**以东**，是全城最老的一块，很多部分早于兽人焚城后的重建；因为当年没被烧毁，所以从未真正重建过。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Old Town
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "To the east of the Trade District is the Old Town, the oldest section of the capital, and many parts of it still predate the reconstruction of the city after its razing by the orcs during the events of the First War. As the district had not been badly ravaged, it had never needed true rebuilding."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "更古旧的半木结构房屋，木梁外露、墙面斑驳，街道狭窄曲折，屋檐低垂、彼此几乎相接"
  negative: "崭新石材, 宽阔笔直大道, 整齐立面, 新粉刷的墙"

- fact_id: stormwind.district.021
  claim: 旧城区破败寒酸，街道比其他区脏得多、气味也重；是城里大多数穷人的居住区，乞丐、窃贼和穷人都在这儿。
  tag: ✅
  source: Warcraft Wiki — Old Town（引小说《Stormrage》第 21 章）
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "It is a rustic, downtrodden place, where the streets are described as far dirtier and smellier than the other districts. It is also the residential area for most of the poor folk of the city, as beggars, thieves, and poor people can be found there."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "湿漉泥泞的窄巷，墙根堆着木桶与破筐，晾衣绳横过巷口，墙角蹲着衣衫褴褛的人，空气里浮着薄雾般的尘"
  negative: "干净整洁, 明亮开阔, 花坛, 鲜艳色彩, 现代脏乱（塑料垃圾）"

- fact_id: stormwind.district.022
  claim: 旧城区的走法：从贸易区往东北，从暴风要塞往南，从矮人区往东南。
  tag: ✅
  source: Warcraft Wiki — Old Town
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "To get to the Old Town, you can head northeast from the Trade District, south from Stormwind Keep, or southeast from the Dwarven District."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.023
  claim: 旧城区里有暴风城军方的指挥中心——包含勇士大厅、军营、露天训练场、马厩，以及情报机构 SI:7 的总部。
  tag: ✅
  source: Warcraft Wiki — Old Town
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "In the district, the Command Center is the base of operations for Stormwind's army officers, which include the Champions' Hall, the army's barracks, open training grounds, stables, and the headquarters of the SI:7"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "围合式的军营院落，院中是露天沙地训练场，立着草人靶与兵器架，一侧是马厩，士兵在列队操练"
  negative: "现代军营, 铁丝网, 车辆, 空无一人的院子"

- fact_id: stormwind.district.024
  claim: 勇士大厅位于旧城区的**东南端**。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Points of Interest → Champions' Hall）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "The Champions' Hall is located in the southeastern end of Old Town."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.025
  claim: 旧城区的酒馆叫「猪和哨声」（Pig and Whistle Tavern），带旅店老板与烹饪训练师；二楼还有卖烹饪配方的人。
  tag: ✅
  source: Warcraft Wiki — Old Town, §Points of interest ＋ §Notes
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "Upstairs in the \"Pig and Whistle\", Kendor Kabonka can be found selling plenty of cooking recipes."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "低矮的两层木构酒馆，一层烟熏的大堂里有长条木桌与炉灶，铁锅挂在墙上，二楼阁楼堆着酒桶与杂货"
  negative: "明亮宽敞, 大理石地面, 现代厨房, 吧台高脚凳"
```

### E. 法师区（Mage Quarter）

```yaml
- fact_id: stormwind.district.030
  claim: 法师区在暴风城的**南角**（官方导览文亦称城市西南部），在贸易区**以西**。
  tag: ✅
  source: Warcraft Wiki — Mage Quarter 开篇 ＋ Stormwind City §Mage Quarter
  source_url: https://warcraft.wiki.gg/wiki/Mage_Quarter
  quote: "The Mage Quarter (also called the Mage District or the Mage's District) lies in the southern corner of Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.031
  claim: 从教堂广场或贸易区去法师区，都要**向西南跨过运河**。
  tag: ✅
  source: Warcraft Wiki — Mage Quarter
  source_url: https://warcraft.wiki.gg/wiki/Mage_Quarter
  quote: "To get to the Mage Quarter, visitors can travel southwest across the Canals from either Cathedral Square, Lion's Rest, or the Trade District."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: "Lion's Rest（雄狮之眠）是军团再临后的产物，经典旧世那个方向是花园区。"

- fact_id: stormwind.district.032
  claim: 巫师圣殿（Wizard's Sanctum）矗立在法师区正中；它是一座螺旋台阶塔，也是通往联盟各主城的传送门房间。
  tag: ✅
  source: Warcraft Wiki — Stormwind City §Mage Quarter ＋ Mage Quarter 开篇 ＋ 中文坐标表条目名「巫师圣殿,入口,法师区的螺旋台阶塔」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The Wizard's Sanctum stands proudly in the center of the district, it is here that mages train to increase their powers"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座细高的石砌魔法塔，外侧盘绕着露天螺旋石阶直上塔顶，塔身开着尖拱窗，顶部有发光的法阵"
  negative: "方形塔楼, 木塔, 内部楼梯看不见, 塔身无窗"

- fact_id: stormwind.district.033
  claim: 法师区里有臭名昭著的酒馆「已宰的羔羊」，术士常被吸引到它的黑暗地窖里，在体面社会的阴影下修习黑暗法术。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Mage Quarter
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "shady warlocks are often drawn to the dark cellars of the Slaughtered Lamb, where they practice their dark arts in the shadows of polite society."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一间门面不起眼的小酒馆，招牌画着被宰的羊，店内地板有一道通往地窖的活板门，地窖里是暗紫色法阵与烛火"
  negative: "明亮店面, 大窗, 热闹人群, 彩色装饰"

- fact_id: stormwind.district.034
  claim: 法师区其余部分是裁缝铺、存放魔法制品与材料的仓库，以及热闹的咖啡馆和酒吧。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Mage Quarter
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The rest of the district is filled with tailoring shops, warehouses storing magical artifacts and reagents, and bustling coffeehouses and bars."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "临街的裁缝铺挂着成匹布料，隔壁是堆满木箱与陶罐的仓库门脸；街角咖啡馆摆着户外木桌，客人围坐"
  negative: "现代咖啡店, 玻璃门, 遮阳伞带商标, 连锁店招牌"

- fact_id: stormwind.district.035
  claim: 法师区靠运河一侧（去监狱的路上）有附魔师的小铺子。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Profession Trainer → Enchanting）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "He runs a shop on the outside of the Magic Quarter on your way to the Stockade."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河边一间窄门面的小铺，橱窗里摆着发微光的符文石与卷轴，店门正对水面步道"
  negative: "大店面, 无水景, 现代橱窗照明"
```

### F. 教堂广场（Cathedral Square）

```yaml
- fact_id: stormwind.district.040
  claim: 教堂广场在贸易区**以北**，是所有圣光信徒的宗教中心；虽然暴风要塞是城里最大的建筑，但很多人认为最令人敬畏的是光明大教堂。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Cathedral Square
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "To the north of the Trade District is Cathedral Square, the religious center for all followers of the Holy Light. Though Stormwind Keep is the biggest structure in Stormwind City, many believe the most awe-inspiring is the Cathedral of Light."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座极高的哥特式石砌大教堂正对开阔广场，双塔耸立、巨大玫瑰窗与尖拱门，广场铺着规整石板"
  negative: "圆顶教堂, 木质礼拜堂, 低矮建筑, 东方庙宇, 现代教堂"

- fact_id: stormwind.district.041
  claim: 教堂广场的走法：从贸易区往西北，从矮人区往东南。
  tag: ✅
  source: Warcraft Wiki — Cathedral Square
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_Square
  quote: "To get to Cathedral Square, one can head northeast from Lion's Rest, northwest from the Trade District, or southeast from the Dwarven District."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: "Lion's Rest 那一岔在经典旧世对应花园区方向。贸易区条目写「从教堂广场往东南到贸易区」，与此互为反向、自洽。"

- fact_id: stormwind.district.042
  claim: 市民常聚在教堂广场上聊天、交换见闻，偶尔顺个苹果。
  tag: ✅
  source: Warcraft Wiki — Cathedral Square（引《Exploring Azeroth: The Eastern Kingdoms》p.17）
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_Square
  quote: "Stormwind citizens often congregate in the Square for conversation, exchange of ideas, and the occasional swiped apple."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂前的开阔石板广场上三三两两站着聊天的市民，孩子在人群间穿行，角落有卖苹果的小摊"
  negative: "空无一人, 集会演讲, 阅兵, 现代人群"

- fact_id: stormwind.district.043
  claim: 广场上还有市政厅（暴风城的建筑师与研究者在此记录人口普查）与孤儿院；大片的暴风城公墓在广场**以北**。
  tag: ✅
  source: Warcraft Wiki — Stormwind City §Cathedral Square ＋ Cathedral Square 条目
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_Square
  quote: "The extensive Stormwind City Cemetery lies to the north of the square."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂后方的墓园，成排的石质墓碑与矮石墙围栏，几株老树，草地被踩出小径"
  negative: "现代公墓, 水泥墓, 骨灰墙, 塑料花"

- fact_id: stormwind.district.044
  claim: 教堂广场内有暴风湖（Stormwind Lake）这一水体。
  tag: ✅
  source: Warcraft Wiki — Cathedral Square, §Points of interest → Cathedral area
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_Square
  quote: "Stormwind Lake"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂区北侧一片开阔的静水湖面，湖岸是天然草坡与石堤混合，倒映着教堂尖塔"
  negative: "人工泳池, 方形水池, 喷泉, 海"

- fact_id: stormwind.district.045
  claim: 教堂广场南侧沿着运河有店铺（例如「三风」/「上好丝线」那个位置）。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路 ＋ Cathedral Square §Canals' shops
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "A trio of ethereal technomancers has set up shop in Stormwind, along the canal south of Cathedral Square."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: "「三风」（虚空仓库/幻化）本身是后期内容；这条只用来确认「教堂广场以南的运河沿岸是有店铺的一段」这个空间事实。"
```

### G. 矮人区（Dwarven District）

```yaml
- fact_id: stormwind.district.050
  claim: 矮人区位于暴风城的**北角**，在教堂广场**以东**；是第二次战争后铁炉堡矮人为安置国王派来的工匠而建的聚居区。
  tag: ✅
  source: Warcraft Wiki — Dwarven District 开篇 ＋ Stormwind City §Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The Dwarven District lies in the northern corner of Stormwind City. Here, the dwarves of Ironforge established an enclave after the Second War to house all the workers sent by King Magni."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "矮胖敦实的石构建筑，门窗比人类区低矮、比例更厚重，铁艺构件与铆钉外露，屋顶是厚石板"
  negative: "高挑纤细的建筑, 尖塔, 轻木结构, 人类比例的门"

- fact_id: stormwind.district.051
  claim: 矮人区空气里满是烟与火星，地面随着铁砧的敲击震动；街上排着武器与护甲铺，铁匠在众多露天广场上打铁。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The air is thick with smoke and sparks, and the ground trembles with the pounding of anvils, but to many it feels just like a home should. A trove of weapon and armor shops line the streets, and blacksmiths create masterpieces out of common metals in the many open-air plazas."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "露天锻造广场上并排立着数座燃着炭火的锻炉与铁砧，橙红火星四溅，空气里浮着灰蓝烟雾，墙上挂满打好的兵器"
  negative: "干净无烟, 现代工厂, 电焊, 室内车间, 冷色调"

- fact_id: stormwind.district.052
  claim: 矮人区的锻炉产生持续不散的烟雾，伴着不停的锤声。
  tag: ✅
  source: Warcraft Wiki — Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The forges in the district produce a constant haze, supplemented by the constant strokes of smiths' hammers."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "整个街区笼在一层不散的灰烟里，远处建筑轮廓被烟雾柔化，光线穿过烟形成可见光柱"
  negative: "通透清澈的空气, 蓝天白云, 无雾"

- fact_id: stormwind.district.053
  claim: 矮人区的走法：从教堂广场往东北，从旧城区往西北，从暴风要塞往西；也可以直接坐矿道地铁到暴风城站下车。
  tag: ✅
  source: Warcraft Wiki — Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "To get to the Dwarven District, you can head northeast from Cathedral Square, northwest from Old Town, west from Stormwind Keep, or get off the Deeprun Tram at the Stormwind City station."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.054
  claim: 矮人区北部有一座喷泉（水井），旅店「金酒桶」就在喷泉旁。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Inn → Dwarven District Inn）＋ 坐标表条目名「矮人区,北部水井」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "The Golden Keg is in the northen part of the Dwarven District, right by the fountain."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌的圆形水井/喷泉立在矮人区街心，井沿粗厚，旁边是一座门口堆着酒桶的矮胖旅店"
  negative: "精致大理石喷泉, 雕像喷泉, 现代水景"

- fact_id: stormwind.district.055
  claim: 割喉小巷（Cut-Throat Alley）在矮人区南部，只能徒步穿过一间叫「暗夜佳丽」的店进去——那店在运河的矮人区一侧，就在从教堂广场过来的那座人行桥南边；小巷不与矮人区其余部分相连，里面只有板条箱和木桶。
  tag: ✅
  source: Warcraft Wiki — Cut-Throat Alley
  source_url: https://warcraft.wiki.gg/wiki/Cut-Throat_Alley
  quote: "Cut-Throat Alley can only be reached on foot by passing through a shop called the Shady Lady, on the Dwarven side of the Canals just south of the footbridge from Cathedral Square; its coordinates are 64, 46. The alley's only features are a number of crates and barrels ... It does not connect to the rest of the Dwarven District."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一条死胡同，两侧是高墙，地上堆着板条箱与木桶，尽头是一栋两层空宅的门，唯一出口是穿过一间店铺"
  negative: "贯通的街道, 开阔, 有行人, 有摊位"
```

### H. 暴风要塞（Stormwind Keep）

```yaml
- fact_id: stormwind.district.060
  claim: 暴风要塞高耸在**矮人区与旧城区之间**，是王国的权力中心与历代国王的居所；要塞能俯瞰全城。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Stormwind Keep（引《Exploring Azeroth: The Eastern Kingdoms》p.12）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Rising high between the Dwarven District and Old Town, the keep is the seat of power of the kingdom and serves as the residence of the Stormwindian kings ... The Keep offers a view of the whole city, so that the king can watch over the masses, and provide a powerful reminder of what deserves to be defended."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座建在全城最高地势上的巨大石砌王城，多重塔楼与城垛层层升高，从城中任何角度抬头都能看见它的轮廓"
  negative: "与周围等高, 藏在建筑后面, 木构, 单座塔楼"

- fact_id: stormwind.district.061
  claim: 去要塞的走法（游戏内卫兵原话）：沿着运河一路往北走，会遇到一座**吊桥**，吊桥通向要塞的内庭院。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Points of Interest → Stormwind Keep）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "The keep is in northren Storwmind. Just follow the canals north and you'll eventually come across a drawbridge... that leads into the keep's courtyard."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座放下的木质吊桥跨过运河，桥两端是石砌门楼与绞盘铁链，桥那头是围合的王城庭院"
  negative: "固定石桥, 无铁链, 平地入口, 无门楼"

- fact_id: stormwind.district.062
  claim: 要塞内有王座厅（在主厅尽头）、皇家图书馆与作战室；王座厅正对主厅的第一道门后就是作战室。
  tag: ✅
  source: Warcraft Wiki — Stormwind Keep, §Layout
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "Throne room - At the end of the main hall. War Room - First door, straight ahead through the throne room from the main hall."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "长而高的石砌主厅，两侧列柱与悬挂的蓝金旗帜，尽头是抬高数级台阶的王座平台"
  negative: "露天走道, 圆形大厅, 现代议事厅, 低矮房间"

- fact_id: stormwind.district.063
  claim: 经典旧世时，王座上坐的不是国王——瓦里安·乌瑞恩失踪后，年幼的安度因被扶上王位，而**高阶领主博瓦尔·弗塔根以摄政王身份代行王权**，王室顾问是卡特拉娜·普瑞斯托女士（实为奥妮克希亚）。
  tag: ✅
  source: Warcraft Wiki — Bolvar Fordragon, §Regent of Stormwind（引《World of Warcraft》游戏手册 p.170）
  source_url: https://warcraft.wiki.gg/wiki/Bolvar_Fordragon
  quote: "After King Varian Wrynn went missing under suspicious circumstances while en route to a diplomatic summit to Theramore Isle, Stormwind was believed to be going through a state of disarray. Young Anduin was given the crown so that order could be preserved within the kingdom of Stormwind, at the behest of the royal councilor, Lady Prestor. Highlord Bolvar Fordragon acted as Regent Lord of Stormwind or the Supreme Commander of Stormwind's forces on behalf of King Anduin."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座厅里，一名披金甲的壮年圣骑士站在王座侧前方代为主事，王座上坐着一个明显年幼的男孩，旁边立着一位深色长裙的贵妇顾问"
  negative: "壮年国王坐在王座上, 独自一人的国王, 满殿朝臣跪拜"

- fact_id: stormwind.district.064
  claim: 暴风要塞在《大地的裂变》中被彻底重制——内外都改了，通往王座厅的路变成了露天，加了宏伟步道与喷泉，王座厅也重新设计，图书馆前的花园能俯瞰暴风湖。**经典旧世的要塞不是这个样子**。
  tag: ❌
  source: Warcraft Wiki — Stormwind Keep, §Notes and trivia
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "In Cataclysm, Stormwind Keep was entirely remodeled, inside, as well as outside. The path leading to the throne room is now open air and redesigned, complete with a grand walkway and a fountain."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "露天步道通往王座厅, 王座厅前的大喷泉, 敞开式庭院走廊, 俯瞰湖景的花园平台"
```

### I. 花园区 / 公园区（The Park）—— 经典旧世独有

```yaml
- fact_id: stormwind.district.070
  claim: 花园区（The Park）曾是位于暴风城**西角**的一个城区，原本是市民的休闲场所，后来成了来访暗夜精灵的聚居地——他们在石城里更愿意待在有自然气息的地方。
  tag: ✅
  source: Warcraft Wiki — Park（条目顶部标 {{Classic only|patch=4.0.3a}}）
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "The Park used to be the district located in the western corner of Stormwind City. It was once a place devoted to leisure activities for Stormwind's populace until it became a refuge for visiting night elves, who found the comforting presence of nature a welcome respite from the vast stone thoroughfares of Stormwind proper."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石城之中一整片绿地城区，高大古树、草坪与自然石径取代了石板路，建筑掩映在树影里，整体色调比其他区更绿更柔"
  negative: "焦土, 废墟, 断墙, 烧黑的地面, 空旷石板广场, 纪念碑"

- fact_id: stormwind.district.071
  claim: 花园区是**整个东部王国唯一有德鲁伊训练师**的地方；暗夜精灵在园区广场正中造了一口月亮井。
  tag: ✅
  source: Warcraft Wiki — Park
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "It was the only place in the Eastern Kingdoms where druid trainers resided. The night elves created a Moonwell in the center of the park square."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "林间空地正中一口暗夜精灵月亮井：环形石台托着一池发着淡青白微光的静水，台边立着藤蔓缠绕的雕花石柱，水面浮着微光"
  negative: "普通水井, 喷泉, 浑浊水, 人类风格石雕, 金色光"

- fact_id: stormwind.district.072
  claim: 去花园区的走法：从教堂广场往西南，或从法师区往西北。
  tag: ✅
  source: Warcraft Wiki — Park
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "To get to the Park, one would have headed southwest from Cathedral Square or northwest from the Mage Quarter."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.district.073
  claim: 花园区是被死亡之翼在《大地的裂变》中摧毁的——他撞上城门、毁掉部分城区，之后把整个花园区掀飞。这发生在本站锚定的版本**之后**。
  tag: ❌
  source: Warcraft Wiki — Stormwind City §History（Cataclysm 段）＋ Park
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "During his short appearance, the Dragon Aspect had crashed down on the city gates, wrecked parts of the city, and blown away the entire Park after."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "花园区废墟, 焦黑土地, 巨龙爪痕, 倒塌的雕像, 雄狮之眠墓园"
```

### J. 监狱、金库与运河中的岛

```yaml
- fact_id: stormwind.city.020
  claim: 运河中央立着**两座**监狱堡垒——暴风城监狱（Stockade）与金库（Vault），两者都是关押不法之徒的地方。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Canals and the prisons
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "There are two fortifications that rise from the waters in Stormwind - both are prisons for the lawless and evil."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河正中拔水而起的两座方形石堡，四面环水，堡身厚重无窗，只在临水面开一道包铁的门"
  negative: "岸上的建筑, 木塔, 有大窗, 塔楼尖顶, 只有一座"

- fact_id: stormwind.city.021
  claim: 暴风城监狱由法师区进入，关押着杀人犯、豺狼人、窃贼和王国的其他敌人。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Canals and the prisons
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The Stockade is accessible from the Mage Quarter and holds murderers, gnolls, thieves, and other enemies of the kingdom."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.022
  claim: 游戏内卫兵对监狱位置的原话：「在城市正中，法师区的东北边」。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Points of Interest → The Stockade）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "It's in the center of the city, just northeast of the Mage Quarter. If you're truly going there, be careful. I've heard news of riots."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.023
  claim: 暴风城监狱是一座高戒备监狱建筑群，**藏在运河区的下方**，由狱长塞尔沃特主管；经典旧世时里面刚发生过囚犯暴动，守卫被赶出，囚犯占据了监狱。
  tag: ✅
  source: Warcraft Wiki — Stormwind Stockade (Classic)（专写大地裂变之前的版本）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Stockade_(Classic)
  quote: "Stormwind Stockade is a high-security prison complex, hidden beneath the canal district of Stormwind city. Presided over by Warden Thelwater, Stormwind Stockade is home to petty crooks, political insurgents, murderers and a score of the most dangerous criminals in the land. Recently, a prisoner-led revolt has resulted in a state of pandemonium within the stockade - where the guards have been driven out and the convicts roam free."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "水中石堡的临水入口：一道包铁的厚门与几级被水浸湿的石阶，门内漆黑向下延伸，门外站着神情紧张的看守"
  negative: "敞开的大门, 明亮的入口, 岸上的入口, 现代铁栅监狱"

- fact_id: stormwind.city.024
  claim: 金库（Vault）位于监狱的**正对面**，除了「四面完全被水包围」和「顶上有一座钟」之外，与监狱大体相同；它被一道铁闸门封着，门口有两名守卫，从来不能进入。
  tag: ✅
  source: Warcraft Wiki — Vault (Stormwind City)
  source_url: https://warcraft.wiki.gg/wiki/Vault_(Stormwind_City)
  quote: "is located opposite the Stockade, and mirrors that other prison in most ways, except that it is completely surrounded by water and has a clock on top of it. It is currently inaccessible, gated off by a portcullis with two guards."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "四面完全被水环绕的方形石堡，堡顶正中嵌着一面大石钟面，临水一侧是放下的铁栅闸门，门前两名卫兵站在窄石台上"
  negative: "与岸相连, 无钟, 门敞开, 有窗有灯"
```

### K. 交通与尺度

```yaml
- fact_id: stormwind.city.030
  claim: 矿道地铁（Deeprun Tram）的暴风城一端在矮人区，通过该区**东侧的一条隧道**进入；隧道口被一个巨大的旋转齿轮框着，绝不会认错。
  tag: ✅
  source: Warcraft Wiki — Dwarven District ＋ Stormwind City §Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The Stormwind City end of the Deeprun Tram line is accessible through a tunnel on the east side of the district."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一个直径数层楼高的巨大金属齿轮嵌在石壁上，框住下方黑洞洞的隧道口，齿轮缓慢旋转，边缘泛着油光与铜锈"
  negative: "静止的齿轮, 小型装饰齿轮, 木门, 无齿轮的普通隧道"

- fact_id: stormwind.city.031
  claim: 矿道地铁是一条全封闭的地下（且部分在水下）双轨线路，两组各三节车厢往返，连接铁炉堡与暴风城，对旅客免费；水下那一段其实是一座地下湖。
  tag: ✅
  source: Warcraft Wiki — Deeprun Tram 开篇（引《Beyond the Dark Portal》第 5 章）
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "The Deeprun Tram (or simply the Tram) is a long, fully enclosed, underground (and partially underwater) set of double tracks upon which rolls two sets of three wagons ... The underwater section of the tram is, in fact, a subterranean lake."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "全封闭的地下隧道双轨，三节连挂的铜黄色侏儒车厢停靠在石台边；某一段隧道顶壁是透明的，外面是幽绿的地下湖水与游鱼"
  negative: "露天轨道, 蒸汽机车, 单节车厢, 现代地铁, 电气化接触网"

- fact_id: stormwind.city.032
  claim: 卫兵指路：矿道地铁「在矮人区靠里面/靠后的位置」。
  tag: ✅
  source: 游戏内 NPC 对话 — Stormwind City Guard 指路（Points of Interest → Deeprun Tram）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "You'll find it in the Dwarven District towards the back. Oh, and be sure to keep your arms and legs inside the tram while the tram is in motion."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.033
  claim: 狮鹫管理员、飞行训练师与坐骑商人都在城墙上。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Points of interest
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The gryphon master, the flying trainer, and the mount vendor are on the walls of the city."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城墙顶端一段加宽的平台被辟成狮鹫栖场，木质栖架上停着数只狮鹫，平台边缘无遮挡、直接临空俯瞰城区"
  negative: "地面的马厩, 室内, 有屋顶的鸟舍, 铁笼"

- fact_id: stormwind.city.034
  claim: 角色的标准跑动速度是每秒 7 码；切换成「走」时地面速度是每秒 2.5 码（约 35%）。（下游排镜与路线计时用。）
  tag: ✅
  source: Warcraft Wiki — Speed
  source_url: https://warcraft.wiki.gg/wiki/Speed
  quote: "The standard running speed is 7 yards per second, or a mile every 4 minutes and 12 seconds (2:37 per kilometer)." ／ "When walking is enabled (vs. run), then all ground speeds are 2.5 yards per second (35%), both mounted and unmounted."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.035
  claim: 钓鱼是暴风城市民的热门消遣，运河与城内湖里有各种水产。
  tag: ✅
  source: Warcraft Wiki — Stormwind City, §Notes and trivia
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Fishing is a favored sport in Stormwind City. The canals and lakes of Stormwind City house a variety of seafood."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河边木码头上坐着几名垂钓者，脚边放着木桶与鱼篓，钓线垂入深水"
  negative: "现代钓具, 遮阳伞, 橡皮艇, 岸边无人"

- fact_id: stormwind.city.036
  claim: 有说法称人们在暴风城中可以步行、骑乘坐骑，也可以乘小船沿着分割城市的几条运河穿行。（**此条出自非正史的 RPG 设定书，作为「水路可通行」的旁证，不作硬设定**。）
  tag: ⚠️
  source: Warcraft Wiki — Stormwind City, §In the RPG（引《Lands of Conflict》p.53）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "one can move about Stormwind on foot, rent one of many mounts or even have a small boat take them through the several canals that bisect the city."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "一条窄木船沿运河缓行，船夫立在船尾撑篙，乘客坐在船中，两岸石堤与桥拱从头顶掠过"
  negative: "机动船, 大型驳船, 帆船, 摩托艇"
```

### L. 世界坐标与米制相对位置（Blender 直接可用）

> 说明：下列坐标出自玩家整理的 GM 传送坐标表（map=0 zone=1519，单位＝码，+X 北 +Y 西 +Z 上），
> 属 T3；但其**相对几何与 T1 wiki 的每一条方位文字逐条吻合**（对账见 § 综合 · 八区关系图），
> 因此可作为建模底稿。口播中不要把具体码数说成官方数据。

```yaml
- fact_id: stormwind.city.040
  claim: 英雄谷/暴风城入口的世界坐标为 (-9040.90, 451.38, 93.06)；贸易区南入口为 (-8886.61, 574.73, 92.76)。
  tag: ✅
  source: 魔兽世界坐标大全（玩家整理的 GM 传送坐标表，CSDN 转载）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "英雄谷,暴风城入口 map=0 zone=1519[1519] location=1617 x,y,z,h=-9040.899414,451.377197,93.055832,0.638096" ／ "贸易区,南入口 ... x,y,z,h=-8886.608398,574.733643,92.759056,0.590161"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.041
  claim: 旧城区中心 (-8720.88, 406.10, 97.74)；暴风要塞入口 (-8524.95, 437.38, 105.57)；皇家画廊（要塞北部）(-8344.79, 514.30, 122.27)。
  tag: ✅
  source: 同上（GM 传送坐标表）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "旧城区,中心 ... x,y,z,h=-8720.882813,406.099609,97.744759,3.471887" ／ "暴风要塞,入口 ... x,y,z,h=-8524.954102,437.384644,105.569412,5.298292" ／ "皇家画廊,暴风要塞北部 ... x,y,z,h=-8344.793945,514.297546,122.274437,0.683697"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.042
  claim: 矮人区北部水井 (-8384.76, 630.87, 94.76)；割喉小巷（矮人区南部）(-8526.17, 595.04, 101.40)。
  tag: ✅
  source: 同上（GM 传送坐标表）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "矮人区,北部水井 ... x,y,z,h=-8384.759766,630.868896,94.762863,3.218431" ／ "割喉小巷,矮人区南部 ... x,y,z,h=-8526.171875,595.036804,101.399025,4.178947"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.043
  claim: 教堂广场入口 (-8623.20, 774.28, 96.65)；光明大教堂入口 (-8556.61, 826.03, 106.53)。
  tag: ✅
  source: 同上（GM 传送坐标表）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "教堂广场,教堂入口 ... x,y,z,h=-8623.195313,774.276550,96.651993,0.730778" ／ "光明大教堂,入口 ... x,y,z,h=-8556.608398,826.026306,106.526123,0.775545"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.044
  claim: 花园区中心 (-8742.26, 1063.29, 89.75)——这是全城**最西**也是**海拔最低**的一块，与「花园区在西角」的 T1 文字吻合。
  tag: ✅
  source: 同上（GM 传送坐标表）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "花园,中心 map=0 zone=1519[1519] location=1519 x,y,z,h=-8742.264648,1063.290649,89.745056,1.915899"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.045
  claim: 法师区水井 (-8929.28, 960.16, 117.31)；已宰的羔羊 (-8960.11, 1007.08, 122.03)；巫师圣殿入口 (-9005.53, 867.86, 129.69)——巫师圣殿是全城**最高**的采样点，比花园区高约 40 码。
  tag: ✅
  source: 同上（GM 传送坐标表）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "法师区,水井 ... x,y,z,h=-8929.279297,960.157776,117.309624,4.079603" ／ "已宰的羔羊,法师区带地下墓地的酒馆 ... x,y,z,h=-8960.111328,1007.083426,122.025322,2.170021" ／ "巫师圣殿,入口,法师区的螺旋台阶塔 ... x,y,z,h=-9005.530273,867.860413,129.692093"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.046
  claim: 监狱入口（坐标表描述为「法师区北部运河边上有地下城的城堡」）(-8822.88, 799.75, 97.68)——与卫兵原话「城市正中、法师区东北」完全吻合。
  tag: ✅
  source: 同上（GM 传送坐标表）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "法师区北部运河边上有地下城的城堡,入口 map=0 zone=1519[1519] location=1519 x,y,z,h=-8822.883789,799.746582,97.678642"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.047
  claim: 由上述坐标算出：含英雄谷在内的全城南北跨度约 **696 码 ≈ 636 m**，东西跨度约 **657 码 ≈ 601 m**，垂直落差约 **40 码 ≈ 37 m**。即暴风城是一座约 **640 × 600 m** 的城，不是想象中的大都会——步行绕一圈是可行的。
  tag: ⚠️
  source: 由 stormwind.city.040–046 的坐标计算（1 码 ＝ 0.9144 m）
  source_url: https://blog.csdn.net/weixin_30439131/article/details/98442978
  quote: "（计算结果，非原文引用）"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.048
  claim: 按标准走路速度 2.5 码/秒算，城门到贸易区约 198 码 ≈ 79 秒；贸易区到教堂广场约 330 码 ≈ 132 秒；全城最长直线（旧城区↔矮人区）约 404 码 ≈ 162 秒。**一个旅行者用走的穿越全城约 4–5 分钟。**
  tag: ⚠️
  source: 坐标计算 ＋ Warcraft Wiki — Speed（2.5 码/秒）
  source_url: https://warcraft.wiki.gg/wiki/Speed
  quote: "When walking is enabled (vs. run), then all ground speeds are 2.5 yards per second (35%)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
```

### M. 官方简体中文译名

```yaml
- fact_id: stormwind.district.090
  claim: 各区的简体中文译名：Trade District＝贸易区，Old Town＝旧城区，Mage Quarter＝法师区，Dwarven District＝矮人区，Cathedral Square＝教堂广场，The Park＝花园区，Stormwind Keep＝暴风要塞，Valley of Heroes＝英雄谷。
  tag: ✅
  source: 中文 GM 传送坐标表条目名（逐条与英文坐标一一对应）＋ 新浪游戏《魔兽建筑考：人类雄城 暴风城》
  source_url: https://games.sina.com.cn/o/z/wow/2017-10-16/fymvuyt1507657.shtml
  quote: "暴风城港口，暴风要塞，教堂广场，法师区，矮人区、贸易区、旧城区与雄狮之眠" ／ "入口的河谷被称为英雄谷"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: "坐标表里 The Park 写作「花园」/「花园区」；灰机 wiki（warcraft.huijiwiki.com）全站对本机 403，未能取到条目原文复核，见 § 未查。"

- fact_id: stormwind.district.091
  claim: 其他关键地名的中文译名：The Canals＝运河（暴风城），Stormwind Stockade＝暴风城监狱，Deeprun Tram＝矿道地铁（亦见「地下城铁」写法），Cut-Throat Alley＝割喉小巷，Wizard's Sanctum＝巫师圣殿，The Slaughtered Lamb＝已宰的羔羊，Cathedral of Light＝光明大教堂。
  tag: ⚠️
  source: 中文 GM 传送坐标表条目名 ＋ 中文检索结果（灰机 wiki 条目标题「运河（暴风城）」可见于检索结果，页面本体 403）
  source_url: https://warcraft.huijiwiki.com/wiki/%E8%BF%90%E6%B2%B3%EF%BC%88%E6%9A%B4%E9%A3%8E%E5%9F%8E%EF%BC%89
  quote: "运河（暴风城） - 魔兽世界中文维基" ／ 坐标表条目名："巫师圣殿,入口,法师区的螺旋台阶塔"、"已宰的羔羊,法师区带地下墓地的酒馆"、"光明大教堂,入口"、"割喉小巷,矮人区南部"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: "「矿道地铁」与「地下城铁」两种译法都在中文社区流通，未能从可抓取的一手页面锁定官方客户端用词，见 § 未查。"
```

### N. 官方导览（Blizzard 官网）

```yaml
- fact_id: stormwind.route.001
  claim: 暴风城官方导览把法师区定位在「城市的西南部」——与坐标算出的「城门西南方约 465 m 西 / 102 m 北」一致。
  tag: ✅
  source: Blizzard 官网 news «Welcome to Stormwind: A Guided Tour»（经 WebFetch 提取正文）
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/20142731
  quote: "Located in the southwest portion of the city, the Mage Quarter houses a variety of mystical services and goods."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: "Blizzard 官网对本机 curl 403，该页正文经 WebFetch 提取；引文措辞以 WebFetch 返回为准，未能二次逐字复核。"

- fact_id: stormwind.route.002
  claim: 官方导览描述的入城顺序是：先穿过暴风城大门（门外两侧各有一架弩炮），进门即英雄谷，两侧高踞着阵亡英雄的雕像，然后才到贸易区的各项服务。
  tag: ✅
  source: Blizzard 官网 news «Welcome to Stormwind: A Guided Tour»（经 WebFetch 提取正文）
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/20142731
  quote: "Arriving at the city, you'll pass through the Stormwind Gates which are flanked by two ballistae just outside of them." ／ "Statues loom above on either side for commemorating the great fallen."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城门外两侧各架着一台木制巨弩（弩炮），弩臂横张、绞盘上弦，弩身漆着蓝金纹样，正对门外道路"
  negative: "火炮, 投石机, 现代武器, 门内的弩炮"

- fact_id: stormwind.route.003
  claim: 官方导览提到运河两岸都有不少店铺，也可以在那儿钓鱼——印证「运河不是单纯的水障，而是一条可逛的商业步道」。
  tag: ✅
  source: Blizzard 官网 news «Welcome to Stormwind: A Guided Tour»（经 WebFetch 提取正文）
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/20142731
  quote: "You'll find quite a few shops along either side of the the canals and if you feel like doing a bit of fishing, you can find that too."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
```

### O. 运河分段（建模用）

```yaml
- fact_id: stormwind.city.050
  claim: 运河按「相邻两区之间的一段」来命名分段，官方条目里可见的至少有：贸易区↔旧城区之间的一段（有南端）、旧城区↔矮人区之间的一段（有东端）。这说明运河不是一个环，而是若干段拼成的网。
  tag: ✅
  source: Warcraft Wiki — Canals (Stormwind City), §Inhabitants 的位置标签
  source_url: https://warcraft.wiki.gg/wiki/Canals_(Stormwind_City)
  quote: "Near southern end of the canal part between Trade District and Old Town" ／ "Near eastern end of the canal part between Old Town and Dwarven District"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: stormwind.city.051
  claim: 教堂广场与矮人区之间有一座**人行桥**（footbridge）；桥南就是运河矮人区一侧的「暗夜佳丽」店。
  tag: ✅
  source: Warcraft Wiki — Cut-Throat Alley
  source_url: https://warcraft.wiki.gg/wiki/Cut-Throat_Alley
  quote: "on the Dwarven side of the Canals just south of the footbridge from Cathedral Square"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座窄而拱的石质人行桥跨过运河，桥面仅容两三人并行，两侧是矮石栏"
  negative: "宽阔车行桥, 吊桥, 木桥, 无栏杆"

- fact_id: stormwind.city.052
  claim: 运河沿岸集中着一批「运河店铺」，分属各区管辖：贸易区一侧有裁缝铺、珠宝匠、花店、加利纳酒庄；法师区一侧有附魔铺与铭文师；教堂广场一侧与矮人区一侧也各有店。
  tag: ✅
  source: Warcraft Wiki — Canals (Stormwind City) §Points of interest ＋ 各区条目的 "Canals' shops" 小节
  source_url: https://warcraft.wiki.gg/wiki/Canals_(Stormwind_City)
  quote: "The Scribe of Stormwind / Cordell's Enchanting / Gallina Winery / Canal Tailor and Fit Shop / Denman Family Jewelers / Fragrant Flowers / Potts' Plates / The Shady Lady / The Three Winds"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河两岸沿石堤一字排开的小店门脸，每间只有一两开间宽，门前挂着各自行业的立体招牌（剪刀、宝石、花束、酒桶）"
  negative: "统一制式店铺, 现代招牌, 大型商场, 空白墙面"
```

---

## 综合 · 八区关系图

### 1. 文字版方位图（原点＝城门，东为右、北为上，单位 m）

```
                                    北 ↑
                                     │
                          ┌──────────┴──────────┐
                          │   矮人区  (-164,600)│  ← 全城最北；东侧隧道 → 矿道地铁
                          │  锻炉/铁砧/金酒桶   │
                          └───────┬─────────────┘
       教堂广场 (-295,382)        │        暴风要塞 (+13,472)→(-58,637)
     ┌──────────────────┐    人行桥│      ┌────────────────────┐
     │ 光明大教堂/市政厅 │◄───运河──┼─────►│ 吊桥入庭院/王座厅  │
     │ 孤儿院/公墓/暴风湖│         │      │ 皇家图书馆         │
     └────────┬─────────┘    割喉小巷(-131,471)└─────────┬──────┘
              │                                          │
  花园区(-560,273)            监狱/金库(-319,199)         │
 ┌────────────────┐         ╔══════════════╗    旧城区 (+41,293)
 │ 月亮井/暗夜精灵│         ║ 运河中的两座 ║   ┌──────────────────┐
 │ 德鲁伊/绿地    │         ║ 水中石堡     ║   │ 猪和哨声/指挥中心│
 └───────┬────────┘         ╚══════════════╝   │ SI:7/勇士大厅    │
         │                                      └────────┬─────────┘
   法师区 (-465,102)                                     │
 ┌────────────────────┐        贸易区 (-113,141)         │
 │ 巫师圣殿(螺旋塔)   │      ┌─────────────────────┐     │
 │ 已宰的羔羊/蓝色隐士│◄─────│ 喷泉/拍卖行/金库银行│◄────┘
 │ (-381,32) 全城最高 │      │ 镀金玫瑰/接待中心   │
 └────────────────────┘      └──────────┬──────────┘
                                         │
西 ←                          英雄谷/城门 (0,0)               → 东
                              五尊雕像 + 石桥 + 护城水面
                                         ↓
                                   艾尔文森林
```

### 2. 相邻关系表（每条都是 T1 wiki 文字 ＋ 坐标双向验证）

| 从 | 到 | T1 文字方向 | 坐标验证（Δ东 m / Δ北 m） | 直线距离 | 走路秒 | 连接方式 |
|---|---|---|---|---|---|---|
| 英雄谷/城门 | 贸易区 | 「northeast from the Valley of Heroes」 | -113 / +141 | 198 码 | 79 s | 英雄谷石桥 → 贸易区南入口 |
| 贸易区 | 旧城区 | 「northeast from the Trade District」 | +154 / +152 | 236 码 | 95 s | 跨运河（贸易区↔旧城区那一段），途中有铁闸门 |
| 旧城区 | 暴风要塞 | 「south from Stormwind Keep」反向 | -29 / +179 | 198 码 | 79 s | 沿运河北上 → 吊桥入要塞庭院 |
| 暴风要塞 | 矮人区 | 「west from Stormwind Keep」 | -177 / +128 | 239 码 | 96 s | 要塞西出口 |
| 矮人区 | 教堂广场 | 「southeast from the Dwarven District」 | -131 / -218 | 278 码 | 111 s | 运河人行桥（割喉小巷在桥南） |
| 教堂广场 | 花园区 | 「southwest from Cathedral Square」 | -264 / -109 | 313 码 | 125 s | 跨运河 |
| 花园区 | 法师区 | 「northwest from the Mage Quarter」反向 | +94 / -171 | 214 码 | 85 s | 跨运河 |
| 法师区 | 贸易区 | 「northeast from the Mage Quarter」 | +352 / +39 | 388 码 | 155 s | 向东北跨运河 |
| 教堂广场 | 贸易区 | 「southeast from the Cathedral Square」 | +182 / -241 | 330 码 | 132 s | 跨运河 |
| 法师区 | 监狱 | 「just northeast of the Mage Quarter」 | +147 / +97 | 192 码 | 77 s | 法师区北缘 → 运河水中石堡 |

**对账结论**：10 条相邻关系里，T1 文字方向与坐标算出的方向 **10/10 一致**（教堂广场↔贸易区那条，
主条目写「北」、分区条目写「西北」，坐标给出的是西北偏北，两说都成立、以「西北」为准）。
所以坐标表可以放心当建模底稿。

### 3. 出入口与水路

- **陆路正门（唯一）**：艾尔文森林 → 暴风城大门 → 英雄谷石桥 → 贸易区南入口。门内外各两名卫兵，门外两侧架弩炮。
- **地下（唯一的第二个入口）**：矮人区东侧隧道（巨型旋转齿轮）→ 矿道地铁 → 铁炉堡。免费、双轨、三节车厢、中段穿过地下湖。
- **水路**：运河系统本身；RPG 设定提到可雇小船穿行（⚠️ 非正史）。**经典旧世没有海港**，所以**没有任何通向海上的出口**。
- **空路**：狮鹫管理员在**城墙上**（贸易区东侧坡道上去），飞往其他联盟据点。
- **通往赤脊山 / 西部荒野 / 暮色森林**：都要先出正门到艾尔文森林，再从森林分路——**城墙上没有第二道城门**。

---

## 综合 · 旅行者路线草案

设定：艾拉清晨从艾尔文森林大道走来，日落后回贸易区住店。全程步行，按 2.5 码/秒算，**纯赶路时间约 22 分钟**，
其余时间都是停下来看。路线按坐标排成一个**逆时针闭环**，不走回头路。

| # | 停靠点 | 所在区 | 为什么停 | 建议镜头类型 |
|---|---|---|---|---|
| 0 | 暴风城大门外（弩炮之间） | 艾尔文森林/城门 | 第一次看见城门高过树冠——建立整城尺度的唯一机会 | 大远景仰拍，人贴画面底部占画高 1/8，无人机自树冠高度推向门洞 |
| 1 | 英雄谷石桥 + 五尊雕像 | 英雄谷 | 「所有入城者都要从英雄脚下走过」——开场的题眼 | 一镜到底步行长镜，低机位贴桥面前推，雕像依次从画框两侧掠过 |
| 2 | 贸易区喷泉与拍卖行 | 贸易区 | 全城最吵最挤的一点；换钱、买城市地图、吃第一顿 | 手持跟随中景，人占画高 1/2，穿过人群与摊位；喷泉作前景层 |
| 3 | 镀金玫瑰旅店（先订房） | 贸易区西侧 | 「先把今晚的床定下来」是旅行节目的标准动作，也埋回程钩子 | 门口中景 → 室内暖光近景，壁炉作光源 |
| 4 | 贸易区↔旧城区之间的运河与铁闸门 | 运河（贸易区段） | 第一次真正看见运河：深水、石堤、钓鱼佬、沿岸小店；顺带拍那道常年关着的铁闸门 | 运河水平面低机位，桥拱作前景；闸门给一个特写 |
| 5 | 旧城区窄巷 + 猪和哨声 | 旧城区 | 全城反差最大的一块：更脏、更旧、更穷，也是最有生活味的午饭点 | 手持窄巷穿行，紧取景（人占画高 2/3），巷口顶光形成明暗对比 |
| 6 | 指挥中心露天训练场 / SI:7 门口 | 旧城区 | 看士兵操练；SI:7 是「城里有个不出声的机构」的钩子 | 中景横摇扫训练场；SI:7 门口只给一个不进去的定镜 |
| 7 | 暴风要塞吊桥 → 王座厅 | 暴风要塞 | 全城制高点＋权力中心；**王座上是个孩子，旁边站着摄政王和那位顾问女士**——这是旧世独有的戏 | 吊桥过桥一镜；王座厅用长焦压缩的大全景，人占画高 1/6 |
| 8 | 要塞外墙俯瞰全城 | 暴风要塞 | 唯一能把「八区＋运河」一次讲完的位置 | 高机位大远景 + 无人机拉升；口播讲分区图 |
| 9 | 矮人区锻造广场 + 金酒桶旁的喷泉 | 矮人区 | 烟、火星、锤声——全城感官最强烈的一块；喝一杯 | 近景特写（火星、通红的铁）+ 中景反打打铁的矮人 |
| 10 | 矿道地铁齿轮隧道口 | 矮人区东侧 | 「这城有第二个入口，在地下」；可以坐一段再回来 | 巨齿轮仰拍定镜 → 车厢内侧跟；地下湖那段给一个透明顶壁的奇观镜 |
| 11 | 教堂广场 + 光明大教堂 | 教堂广场 | 全城最令人敬畏的建筑；黄昏钟声 | 教堂正面大仰角 → 室内彩窗光柱；广场用高机位俯拍人群 |
| 12 | 公墓与市政厅 | 教堂广场北 | 一座城怎么对待它的死者与它的户口本 | 墓园平移长镜，低饱和；市政厅只给门脸 |
| 13 | 花园区月亮井 | 花园区 | **本站最独一份的一站**——石城里唯一的绿地，暗夜精灵与德鲁伊，东部王国唯一的月亮井。日落光 | 林间空地一镜到底环绕月亮井，逆光穿过树叶；水面微光作唯一光源 |
| 14 | 法师区巫师圣殿螺旋塔 + 传送门房间 | 法师区 | 全城最高点，也是「这城通向世界各地」的一站 | 塔外盘旋楼梯的垂直向上摇；传送门房间用广角低机位 |
| 15 | 已宰的羔羊地窖 / 蓝色隐士咖啡馆 | 法师区 | 白天体面、夜里另有一套的反差；夜戏的落点 | 地窖紧取景低照度，紫色单一光源；咖啡馆户外木桌中景 |
| 16 | 运河上看监狱与金库 | 运河中段 | 两座水中石堡：一座刚暴动过，一座顶上有一面钟、门永远关着 | 运河水面低机位，两堡一前一后成纵深；钟面给一个长焦特写 |
| 17 | 回镀金玫瑰住店 | 贸易区 | 收尾；与第 3 站呼应 | 夜景手持回程 → 旅店窗口暖光定镜收 |

**节奏建议**：0–4 早晨，5–8 上午到正午，9–12 下午，13 黄昏（月亮井必须放在日落，这是本站最好的一张画），
14–16 入夜，17 收尾。花园区和矮人区是本站视觉反差最大的两极，别把它们排在一起。

---

## 综合 · Blender 走廊制建议

按 `ai_video.md` rule 4g「几何在 3D、长相在主体」，本站的城市模型应当只建「镜头会拍到的走廊」，不是整城。

### 1. 坐标系与基准

- **原点**：城门（英雄谷入口）世界坐标 `(-9040.90, 451.38, 93.06)`，置于 Blender 原点。
- **换算**：`east = -(y - 451.377) × 0.9144`，`north = (x + 9040.899) × 0.9144`，`up = (z - 93.056) × 0.9144`（结果为米）。
- **建议比例**：按仓库惯例 0.5 比例建模，即上式再 × 0.5。全城包围盒 640 × 600 × 37 m → **320 × 300 × 18.5 m**，单个 `.blend` 完全吃得下。
- **锚点表（米，0.5 比例前的真实米制，东/北/高）**：

| 锚点 | 东 | 北 | 高 |
|---|---|---|---|
| 城门/英雄谷 | 0.0 | 0.0 | 0.0 |
| 贸易区南入口 | -112.8 | 141.1 | -0.3 |
| 旧城区中心 | +41.4 | 292.6 | +4.3 |
| 暴风要塞入口 | +12.8 | 471.8 | +11.4 |
| 要塞北端（皇家画廊） | -57.5 | 636.5 | +26.7 |
| 矮人区北部水井 | -164.1 | 600.0 | +1.6 |
| 割喉小巷 | -131.4 | 470.7 | +7.6 |
| 教堂广场入口 | -295.3 | 381.9 | +3.3 |
| 光明大教堂入口 | -342.6 | 442.8 | +12.3 |
| 花园区中心 | -559.5 | 273.1 | -3.0 |
| 法师区水井 | -465.2 | 102.1 | +22.2 |
| 已宰的羔羊 | -508.1 | 73.9 | +26.5 |
| 巫师圣殿入口 | -380.8 | 32.3 | +33.5 |
| 监狱入口（水中石堡） | -318.5 | 199.4 | +4.2 |

### 2. 无人机航线（一条，开场用）

树冠高度（约 +25 m）自城门正南 120 m 处起飞 → 穿过门洞上方 → 沿英雄谷石桥中轴低飞至贸易区喷泉（-113, 141）
→ 拉升至 +60 m → **逆时针沿运河环绕**：贸易区 → 旧城区 → 要塞（在此升到 +80 m，要塞是全城制高点，
不能从下方穿）→ 矮人区 → 教堂广场 → 花园区 → 法师区 → 回到监狱上方悬停收。
全程约 2.6 km 路径，按 25 s 一段切成 6–7 段（每段 ≤ 30 s 渲染上限）。

### 3. 步行长镜路线（一镜到底，主镜）

**英雄谷石桥 → 贸易区喷泉**：直线 198 码 ≈ 181 m，按走路 2.5 码/秒 ≈ 79 s。
**这超过 30 s 渲染上限，必须切成 3 段**，每段选一个清晰的切口（景别跳档 ≥ 2.0，见 CLAUDE.md 景别档铁律）：

- 段 A（0–26 s）：桥头起幅大远景（人占画高 1/8）→ 落幅中景（人占画高 1/2），走过前两尊雕像。
- 段 B（26–52 s）：**硬切到紧取景**（人占画高 2/3，侧机位跟脸）→ 落幅拉到全景（1/4），走过图拉杨像、路分岔。
- 段 C（52–79 s）：**硬切到贸易区内高机位俯拍**（人占画高 1/10）→ 推进落幅到中近景，喷泉入画收。

三段的机位标签必须互不相同（A＝桥面低机位正跟，B＝侧机位平跟，C＝高机位俯拍），
保证接缝两端不共用机位。

### 4. 走廊两侧需要建的建筑（按镜头接近度分级）

| 走廊段 | 真立面（贴身而过，需真门窗与材质） | 体块+屋顶形制（中景） | 纯体块（远景剪影） | 不建 |
|---|---|---|---|---|
| 城门 → 英雄谷桥 | 城门洞内壁、门楼、五尊雕像与基座、桥栏 | 谷地两侧塔楼、护城石堤 | 城墙延伸段 | 城外森林（用 HDRI/贴片） |
| 英雄谷 → 贸易区 | 贸易区南入口门楼、接待中心门脸、喷泉 | 沿街店面第一排（含招牌） | 第二排屋顶轮廓 | 街区内部 |
| 贸易区 → 旧城区（运河段） | 运河石堤、码头、桥拱内侧、铁闸门、运河店铺门脸 | 两岸第一排建筑 | 要塞轮廓（背景） | 水下 |
| 旧城区窄巷 | 巷子两侧半木结构墙面（木梁+抹灰）、门、木桶木筐、晾衣绳 | 巷口外的建筑 | — | 巷子以外的整个街区 |
| 要塞吊桥 → 庭院 | 吊桥、绞盘铁链、门楼、庭院围墙 | 要塞主体正立面 | 塔楼群 | 要塞内部（另建室内场景） |
| 矮人区锻造广场 | 锻炉、铁砧、兵器架、矮人式门窗（低矮厚重） | 广场四周建筑 | 齿轮隧道口 | 隧道内部（另建） |
| 教堂广场 | 教堂正立面（双塔、玫瑰窗、尖拱门）、广场铺地 | 市政厅、孤儿院 | 公墓、暴风湖岸 | 教堂内部（另建室内） |
| 花园区 | 月亮井（环形石台、雕花石柱）、古树、草地、自然石径 | 林中建筑 | 边缘树线 | — |
| 法师区 | 巫师圣殿塔身与外盘螺旋石阶、已宰的羔羊门脸 | 裁缝铺/仓库/咖啡馆第一排 | 塔顶法阵 | 圣殿内部（另建） |
| 运河中段看监狱 | 监狱与金库两座水中石堡外壳、金库的钟面、临水铁闸门 | 两岸石堤 | 远处桥拱 | 监狱内部（副本，本站不进） |

### 5. 三条模数（rule 4g §B「生成构件，不生成建筑」）

- **人类区模数**：开间 4 m、层高 3.5 m、门洞高 2.4 m。墙/屋顶/街面/桥拱**走脚本**，
  窗/门/招牌/栏杆/瓦当**走生成**。
- **矮人区模数**：开间同 4 m，但**层高压到 2.8 m、门洞高 2.0 m**——这是「矮人区」在画面上唯一可靠的识别特征，
  比任何材质变化都管用。
- **运河模数**：河宽 12 m、堤高 4 m（经典旧世是深水，**堤顶到水面必须有明显落差**，不能做成 Cata 的半淤浅）；
  人行桥宽 2.5 m、车行桥宽 6 m、吊桥宽 6 m。

### 6. 两条硬约束

- **一镜内主体数 ≤ 8**（rule 4g §F）。贸易区人群镜必然超，处理办法是把远处人群做成低模剪影群（算 1 个主体），
  只保留 ≤ 7 个有面部的近景 NPC。
- **要塞是全城最高（+26.7 m），花园区最低（-3.0 m）**，落差 30 m。previz 的相机不能按平地假设排，
  花园区往教堂广场走是**上坡**，法师区往贸易区走是**下坡 22 m**——走位与运镜都要体现。

---

## 版本错置清单（❌，一律不得进正片画面）

| # | 错置项 | 实际引入时间 | 证据 |
|---|---|---|---|
| 1 | **暴风城港口**（码头、船坞、大帆船、岸炮、攻城车） | 补丁 3.0.2（《巫妖王之怒》） | Warcraft Wiki — Stormwind Harbor §Patch changes: "Patch 3.0.2: Added." |
| 2 | **花园区被毁 / 焦土废墟 / 巨龙爪痕** | 《大地的裂变》4.0.3a | Park 条目标 `{{Classic only|patch=4.0.3a}}`；"blown away the entire Park" |
| 3 | **雄狮之眠（Lion's Rest）与瓦里安之墓** | 《军团再临》之后 | Stormwind City §Lion's Rest（在瓦里安于破碎海滩阵亡之后） |
| 4 | **暴风城城外郊区**（大使馆、大地神殿、熊猫人凉亭、湖边农舍） | 《大地的裂变》及之后 | "This area has been built as a replacement for the Stormwind Park, swallowed by Deathwing's assault" |
| 5 | **矮人区的第二个拍卖行与皇家银行** | 补丁 4.0.3a | Stormwind City §Patch：皇家银行随矮人区改版于 4.0.3a 加入；卫兵的「城里有两个银行/两个拍卖行」是改版后台词 |
| 6 | **理发店**（Northshear Abbey / Jelinek） | 补丁 3.0.2 | Warcraft Wiki — Barbershop §Patch changes: "Patch 3.0.2: Added."；且「Cataclysm 之前暴风城的理发师是地精 Sween Neetod」本身也在 3.0.2 之后 |
| 7 | **半淤浅的运河**（淤泥、芦苇、露出水面的杂物、能骑坐骑趟过去） | 补丁 4.0.3a | Canals §Patch changes: "Canals now halfway filled in with mud/silt, along with occasional reeds and lost debris." |
| 8 | **重制后的暴风要塞**（通往王座厅的露天步道、大喷泉、俯瞰暴风湖的花园平台） | 《大地的裂变》 | Stormwind Keep §Notes: "In Cataclysm, Stormwind Keep was entirely remodeled, inside, as well as outside." |
| 9 | **瓦里安·乌瑞恩在位 / 安度因成年在位** | 瓦里安回归在 3.0 前后；安度因在位在《军团再临》之后 | Bolvar Fordragon §Regent of Stormwind：旧世是幼年安度因戴冠、博瓦尔摄政、普瑞斯托女士任顾问 |
| 10 | **英雄谷的 General Hammond Clay** | 后期替换 | Valley of Heroes 条目原文即写他是 "the successor of the late General Marcus Jonathan"——旧世站在那里的是马库斯·乔纳森 |
| 11 | **旧城区训练大厅集中了全部职业训练师** | 第四次战争之后 | Old Town: "Following the Fourth War, the Class Orders sent their trainers to the Training Hall"；旧世是指挥中心（战士/猎人）+ 各区分散的职业训练点 |
| 12 | **「三风」（虚空仓库 / 幻化 / 装备升级）** | 5.x 及之后 | 卫兵台词把它描述为虚空幻化服务点，属后期内容；那个**位置**（教堂广场南侧运河边）旧世有店，但不是这家 |
| 13 | **旧城区↔贸易区之间的铁闸门被移除** | 《大地的裂变》 | "removed in Cataclysm"——**旧世它还在**，反过来说：正片里**应该**出现这道关着的闸门 |
| 14 | **达纳苏斯传送门 / 暗夜精灵与吉尔尼斯难民聚居** | BFA（《争霸艾泽拉斯》） | Stormwind City Outskirts / Stormwind Keep 条目的 War of the Thorns 段 |

---

## 未查 / Open questions

1. **运河上到底有几座桥、各是什么形制**。T1 只说「各区由跨越运河的桥连接」，能确证的具体桥只有两座：
   英雄谷石桥（车行宽桥）、教堂广场↔矮人区的人行桥（footbridge），以及卫兵口述的要塞**吊桥**。
   其余桥的数量与宽窄**没有任何文字来源**。建议下游直接从 Classic 客户端的暴风城地图数一遍，
   或从 1.12 的 WMO/ADT 数据里数。**在数清楚之前，Blender 里桥的数量属于 ⚠️ 自行设定，口播不要报数字。**
2. **运河有没有水闸**。任务书里问了，我在所有 T0/T1 来源里**没有找到任何关于水闸（lock/sluice）的记载**。
   暴风城运河看起来是同一水平面的静水，不存在通航水闸。倾向于「设定没写、且大概率没有」，
   如果正片要拍，必须按 ⚠️ 处理并明说是推的。
3. **运河中央的「岛」**。找到的是**两座水中石堡**（监狱、金库），不是有居民的岛。
   监狱条目写它「藏在运河区的**下方**」，金库写它「四面完全被水包围」——所以更准确的说法是
   「两座从水里立起来的堡垒式建筑」，而不是「运河中央的岛」。下游口播请改用「水中石堡」的说法。
4. **中文官方译名的一手复核**。灰机 wiki（`warcraft.huijiwiki.com` / `wow.huijiwiki.com`）**全站对本机返回 403**
   （Cloudflare 拦截），中文 Wowhead 的经典旧世区域页也 404。目前的中文名来自
   ①中文 GM 传送坐标表条目名 ②可抓取的中文媒体文章 ③搜索结果摘要，都算 T3。
   **需要复核的三个**：The Park 是「花园区」还是「公园区」（坐标表写「花园」，社区两种说法都有）；
   Deeprun Tram 是「矿道地铁」还是「地下城铁」；The Canals 的官方子区名。
   最可靠的办法是直接读 zhCN 客户端的 `AreaTable.dbc`。
5. **各区的相对面积**。中文媒体文章给了一个「面积从大到小」的排序，但那是**大地裂变之后**的城市
   （排序里带着港口和雄狮之眠），对旧世不适用。旧世各区面积没有可引用的数据；
   从坐标只能推出各区中心点的间距，推不出边界。
6. **Blizzard 官网导览页的逐字复核**。`worldofwarcraft.blizzard.com` 对本机 curl 返回 000/403，
   该页正文是经 WebFetch 的提取模型读出来的，引文措辞**未能二次逐字复核**。
   stormwind.route.001/002/003 三条若要进口播，建议先人工开一次网页核对原句。
7. **英雄谷石桥的具体尺寸**（桥长、桥宽、雕像高度）。无任何数据来源。
   坐标只给到「城门到贸易区南入口 198 码」，其中桥占多少未知。建模时按 ⚠️ 自行设定。
8. **旧世贸易区喷泉的确切形制**。只确证了「有一座喷泉，拍卖行在它正北」（卫兵台词），
   形制（几级水池、有无雕像、水柱高度）无来源。
