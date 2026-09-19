---
worker_id: researcher-w8-event-candidates
stage: 0
role: researcher
angle: event-candidates
status: complete
blockers: []
confidence: high
---

# W8 · 暴风城「当天的大事」候选池 —— sk2 阶段 0 专项

> 版本锚点：**经典旧世 Vanilla / WoW 1.x / Classic Era**（世界内当下 ＝ **Year 25 ADP**）。
> 本路只管「这一天城里在发生什么」。城市布局 / 建筑 / 衣着 / 物价 / 矿道地铁本体不在本路范围。
> **已交付过、本路不重复**：① 监狱暴动 ② 灭鼠日 ③ 奥妮克希亚头颅上城门。

---

## 0. 结论先行（五条，请先读）

### 结论 1 ✅ Vanilla 一共只有 **9 个游戏内节日**，且**逐个有补丁号**

`1.2 冬幕节 / 1.3 复活节 / 1.4 儿童周 / 1.6 收获节 / 1.8 万圣节 / 1.9 元宵节 /
1.9.3 爱情降临节 / 1.11 仲夏火焰节 / 1.12.1 苦工节`。
这 9 个之外的一切节日（啤酒节、朝圣者庆典、亡灵节、海盗日、新年、所有微型节日）
**全部是资料片之后才有的**，写进去就是版本错置。见 `stormwind.event.101`–`.109` 与「不可用清单」。

### 结论 2 ⚠️ 九个节日里，**真正落在暴风城城墙之内的只有五个**

| 节日 | 在暴风城里吗 |
|---|---|
| 元宵节 | ✅ 在。长者站**暴风城公园**（Cata 才挪到城外）+ 全城挂饰 + 入夜后整点烟花 |
| 仲夏火焰节 | ✅ 在。篝火就在**运河**边 |
| 万圣节 | ✅ 在。旅店老板发糖、面具、全城挂饰；**主会场在城门外** |
| 爱情降临节 | ✅ 在。卫兵与市民互赠信物，任务起点在**暴风城银行** |
| 冬幕节 | ✅ 在。哥布林摊贩在**贸易区**；但「冬天爷爷」主场在**铁炉堡** |
| 儿童周 | ✅ 起点在。孤儿院在**教堂广场**；但孤儿指定要去的地方**全在城外** |
| 收获节 | ❌ 联盟会场在**铁炉堡**，献祭对象是**西瘟疫之地的乌瑟尔墓** |
| 复活节 | ❌ Vanilla 只在**闪金镇**等新手村找蛋 |
| 暗月马戏团 | ❌ 在**闪金镇外的艾尔文森林**，不在城里 |

### 结论 3 ❌ 最大的一个坑：**安其拉战争物资募集，联盟收点全部在铁炉堡，暴风城一个都没有**

任务书把它列为必查项，查下来结论是反的：`The Alliance needs to gather in the Military Ward of Ironforge`，
所有联盟缴纳 NPC 都在**铁炉堡军事区**，主持人是 **Field Marshal Snowfall**。
暴风城在这件事上**只能拍「物资往铁炉堡运」**——而运输通道恰好就是矿道地铁。
这是可用的，但必须标成 ⚠️（设定没写「暴风城有募集点」，我们是按世界逻辑推运输）。
见 `stormwind.event.121`–`.126`。

### 结论 4 ✅ 本路挖到的**两个最强候选**都不是节日，而是剧情事件

- **A｜天灾入侵暴风城（补丁 1.11）**——飞行浮空城停在城门外，亡灵**周期性打进贸易区**，
  银行边上支起银色黎明的帐篷。设定原话：`A necropolis has appeared outside Stormwind and Undercity`。
- **B｜假面舞会（The Great Masquerade）**——雷金纳德·温德索尔从城门一路走到**暴风要塞王座厅**，
  当庭揭穿卡特拉娜·普瑞斯托就是黑龙奥妮克希亚，她当场现出真身。
  **这条正好落在四个既定机构里的王座厅**，而且是一条**从城门走到王座**的路线——
  天然就是一条「边走边讲解这座城」的摄影机路径。

### 结论 5 ⚠️ 「一天里的时间刻度」在设定里**几乎是空白**

暴风城没有钟楼、没有报时、没有开市闭市、没有宵禁、没有卫兵换岗的设定文本。
Vanilla 唯一有**明确时间刻度**的城内现象是：**元宵节期间入夜后整点放烟花**（`stormwind.event.113`）。
其余「从早到晚」的节奏只能靠我们自己排，属于 ⚠️ 推演，不能说成设定明载。

---

## 1. 事实注册表

### 1.1 Vanilla 节日全表与补丁号（判定版本错置的硬依据）

```yaml
- fact_id: stormwind.event.101
  claim: WoW Vanilla（1.x）总共只有九个游戏内节日，分别加入于补丁 1.2 / 1.3 / 1.4 / 1.6 / 1.8 / 1.9 / 1.9.3 / 1.11 / 1.12.1。
  tag: ✅
  source: Blizzard Watch《All the in-game holidays that are part of WoW Classic》
  source_url: https://blizzardwatch.com/2019/09/30/wow-classic-holidays/
  quote: "Feast of Winter Veil — Added in patch 1.2; Noblegarden — Added in patch 1.3; Children's Week — Added in patch 1.4; Harvest Festival — Added in patch 1.6; Hallow's End — Added in patch 1.8; Lunar Festival — Added in patch 1.9; Love is in the Air — Added in patch 1.9.3; Midsummer Fire Festival — Added in patch 1.11; Peon Day — Added in patch 1.12.1"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "一年之内九个节庆轮转的城市：雪色挂饰、彩蛋、孤儿的手、丰收谷捆、南瓜面具、红灯笼、玫瑰、篝火、烟花"
  negative: "啤酒节木桶, 万圣节无头骑士, 亡灵节骷髅妆, 朝圣者火鸡宴, 海盗日"

- fact_id: stormwind.event.102
  claim: 冬幕节加入于补丁 1.2.0，是 Vanilla 最早的节日。
  tag: ✅
  source: Warcraft Wiki《Feast of Winter Veil》Patch changes 原始 wikitext
  source_url: https://warcraft.wiki.gg/index.php?title=Feast_of_Winter_Veil&action=raw
  quote: "*{{Patch 1.2.0|note=Added.}}"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石城披雪：门楣挂常青花环与红丝带，货摊顶蒙一层薄雪，铜铃与彩球"
  negative: "圣诞老人红白配色卡通化, 电灯串, 塑料装饰"

- fact_id: stormwind.event.103
  claim: 儿童周加入于补丁 1.4.0。
  tag: ✅
  source: Warcraft Wiki《Children's Week》Patch changes 原始 wikitext
  source_url: https://warcraft.wiki.gg/index.php?title=Children%27s_Week&action=raw
  quote: "*{{Patch 1.4.0|note=Added.}}"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂广场上一排牵着大人衣角的孩子，麻布短褐，赤脚或旧皮鞋"
  negative: "现代校服, 书包, 塑料玩具"

- fact_id: stormwind.event.104
  claim: 万圣节加入于补丁 1.8.0；无头骑士要到补丁 2.2.2（燃烧的远征）才加入，联盟的柴垛人（Wickerman）要到补丁 4.2.0 才加入——两者在 Vanilla 都不存在。
  tag: ✅
  source: Warcraft Wiki《Hallow's End》Patch changes
  source_url: https://warcraft.wiki.gg/index.php?title=Hallow%27s_End&action=raw
  quote: "Patch 4.2.0: Overhauled with new daily quests and an Alliance Wickerman. / Patch 2.2.2: Headless Horseman holiday boss added. / Patch 1.8.0: Added."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "南瓜灯挂在旅店檐下，孩子戴着薄铁皮面具（矮人脸、侏儒脸），糖桶摆在旅店老板脚边"
  negative: "无头骑士, 南瓜头骑马人, 巨型柴垛人偶, 蝙蝠群"

- fact_id: stormwind.event.105
  claim: 元宵节加入于补丁 1.9.0（2006-01-03）。
  tag: ✅
  source: Warcraft Wiki《Lunar Festival》Patch changes
  source_url: https://warcraft.wiki.gg/wiki/Lunar_Festival
  quote: "Patch 1.9.0 (2006-01-03): Added."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "红色纸灯笼成串挂过石桥与拱门，夜空整点炸开彩色烟花"
  negative: "中国现代灯会, 电子灯, LED"

- fact_id: stormwind.event.106
  claim: 爱情降临节加入于补丁 1.9.3；现行版本是补丁 3.3.0 重做过的，Vanilla 玩法与现行完全不同。
  tag: ✅
  source: Warcraft Wiki《Love is in the Air》Patch changes
  source_url: https://warcraft.wiki.gg/index.php?title=Love_is_in_the_Air&action=raw
  quote: "*{{Patch 3.3.0|note=This event has been reworked.}} / *{{Patch 1.9.3|note=Added.}}"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "卫兵头顶飘着一颗心的标记，市民递上小瓶香水与糖果"
  negative: "巧克力工厂, 现代心形气球, 王冠化工公司, 情人节 boss"

- fact_id: stormwind.event.107
  claim: 仲夏火焰节加入于补丁 1.11.0；现行版本的日常任务体系与艾胡恩（Lord Ahune）要到补丁 2.4.0 才有。
  tag: ✅
  source: Warcraft Wiki《Midsummer Fire Festival》Patch changes 原始 wikitext
  source_url: https://warcraft.wiki.gg/index.php?title=Midsummer_Fire_Festival&action=raw
  quote: "*{{Patch 2.4.0|note=Event reworked with daily quests and additional bonfires. [[Lord Ahune]] added.}} / *{{Patch 1.11.0|note=Added.}}"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一堆齐人高的篝火在水边熊熊烧着，火舌卷起火星，看火人守在旁边"
  negative: "冰霜领主艾胡恩, 火把杂耍任务, 现代篝火晚会音响"

- fact_id: stormwind.event.108
  claim: 复活节加入于补丁 1.3；Vanilla 时期它只在新手村（联盟为闪金镇、卡拉诺斯）举办，不在暴风城内，直到补丁 3.1.0 才被彻底重做并扩为一周。
  tag: ✅
  source: Blizzard Watch 节日表 + Warcraft Wiki《Noblegarden》
  source_url: https://warcraft.wiki.gg/index.php?title=Noblegarden&action=raw
  quote: "*{{Patch 3.1.0|note=Noblegarden has been completely revamped, and extended to a week long event.}}"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "村口草丛里散落的彩绘木蛋"
  negative: "暴风城城内找蛋, 兔子坐骑, 现代复活节兔"

- fact_id: stormwind.event.109
  claim: 苦工节加入于补丁 1.12.1，日期为 9 月 30 日、且只在欧服realm生效；当天哥布林商贩会出现在暴风城和奥格瑞玛卖打折烟花。
  tag: ✅
  source: Warcraft Wiki《Peon Day》
  source_url: https://warcraft.wiki.gg/index.php?title=Peon_Day&action=raw
  quote: "Goblin vendors arrive in Stormwind City and Orgrimmar and sell fireworks at discounted prices / September 30 only in European realms"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一个绿皮哥布林蹲在石阶边的小摊后，摊上码着一捆捆纸包烟花"
  negative: "大型烟花汇演, 现代烟花架"
```

### 1.2 节日在暴风城里的**具体落点**

```yaml
- fact_id: stormwind.event.110
  claim: 元宵节期间每座主城都会挂上节日装饰。
  tag: ✅
  source: Warcraft Wiki《Lunar Festival》
  source_url: https://warcraft.wiki.gg/wiki/Lunar_Festival
  quote: "Decorations are placed in every capital as well as in the regions of Nighthaven and Moonglade."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石拱门与桥栏上系满红色纸灯笼，灯笼在夜风里轻轻转"
  negative: "灯笼上有汉字, 电灯泡"

- fact_id: stormwind.event.111
  claim: 元宵节的节日灯笼在设定上是为祖先亡魂点的。
  tag: ✅
  source: Warcraft Wiki《Lunar Festival》
  source_url: https://warcraft.wiki.gg/wiki/Lunar_Festival
  quote: "The light from each Festival Lantern honors the soul of an ancestor spirit."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一盏被托在掌心的纸灯笼，内里一点烛火，映亮持灯人的下巴"
  negative: "孔明灯放飞, 河灯"

- fact_id: stormwind.event.112
  claim: 暴风城的元宵节长者「锤喝长者」在 Vanilla 时期站在**暴风城公园**内，直到补丁 4.0.3a 才被挪到城外的艾尔文森林。
  tag: ✅
  source: Warcraft Wiki《Elder Hammershout》Patch changes
  source_url: https://warcraft.wiki.gg/index.php?title=Elder_Hammershout&action=raw
  quote: "Moved from the Park in Stormwind City to Elwynn Forest"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一位盘腿坐在草地与月亮井边的长者，身披毛皮与骨饰，面前摆着一只矮几"
  negative: "站在城门外, 石板地"

- fact_id: stormwind.event.113
  claim: 元宵节期间，暴风城在入夜后每到整点放一次烟花。
  tag: ✅
  source: Warcraft Wiki《Lunar Festival》
  source_url: https://warcraft.wiki.gg/wiki/Lunar_Festival
  quote: "Hourly displays after sunset in the city"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "夜空中一串串彩色烟花在尖顶与蓝色屋瓦上方炸开，光落在运河水面上"
  negative: "白天放烟花, 现代礼花弹, 无人机表演"

- fact_id: stormwind.event.114
  claim: 暴风城的仲夏篝火设在**运河**边（坐标 49,72）。
  tag: ✅
  source: Warcraft Wiki《Midsummer Fire Festival》篝火位置表
  source_url: https://warcraft.wiki.gg/index.php?title=Midsummer_Fire_Festival&action=raw
  quote: "{{Alliance|sort=}} || Eastern Kingdoms || [[Stormwind]] || The Canals || {{coords|49|72|Stormwind City}}"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河石岸边一堆熊熊燃烧的大篝火，火光在水面拉出一条抖动的橙色倒影"
  negative: "室内壁炉, 火盆, 冷色调"

- fact_id: stormwind.event.115
  claim: 仲夏火焰节的设定说法是：为标记一年中最热的月份，艾泽拉斯各地点起明亮篝火，被选中的守火人负责让火持续烧过整个节庆的日与夜。
  tag: ✅
  source: Warcraft Wiki《Midsummer Fire Festival》
  source_url: https://warcraft.wiki.gg/index.php?title=Midsummer_Fire_Festival&action=raw
  quote: "Across [[Azeroth]], brilliant bonfires have been lit to signify the hottest months of the year. The chosen Flamekeepers are eager to ensure they continue burning long into the days and nights of the celebration - and they seek the aid of able explorers in doing so."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一名守火人拄着长杆站在篝火旁，不断把柴推进火心"
  negative: "消防员, 现代服装"

- fact_id: stormwind.event.116
  claim: Vanilla 万圣节在暴风城的玩法是：旅店老板处的南瓜糖桶、薄铁皮面具、万圣节魔杖变装，暴风城的旅店老板叫 Alison，节庆约在 10 月 18 日至 11 月 1 日。
  tag: ✅
  source: Warcraft Tavern《WoW Classic Hallow's End Guide》
  source_url: https://www.warcrafttavern.com/wow-classic/guides/hallows-end/
  quote: "Alliance players can visit innkeeper Alison in Stormwind ... Event Dates: Typically runs between October 18th and November 1st."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "旅店门口一只南瓜形木桶装满糖果，柜台后的女旅店老板递出一把糖"
  negative: "无头骑士, 现代万圣节服装, 塑料南瓜桶"

- fact_id: stormwind.event.117
  claim: 爱情降临节的设定说法是：主城里的许多卫兵与市民整天都在互赠信物与礼物。
  tag: ✅
  source: Warcraft Wiki《Love is in the Air》
  source_url: https://warcraft.wiki.gg/index.php?title=Love_is_in_the_Air&action=raw
  quote: "Something is in the air in the major cities of Azeroth. Some call it love, and some just call it friendship and admiration. Whichever it is, many guards and townsfolks now spend their days giving and receiving tokens and gifts to other amorous citizens."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "站岗的卫兵低头接过一支玫瑰，头盔下露出一点尴尬的笑"
  negative: "现代玫瑰花束包装纸, 气球"

- fact_id: stormwind.event.118
  claim: Vanilla 爱情降临节的联盟主线「危险的爱情」起点在**暴风城银行**的 Aristan Mottar，主题是调查卫兵们是不是中了「爱情瘟疫」，线索最终指向希尔斯布莱德丘陵的药剂师。
  tag: ✅
  source: Warcraft Wiki《Love is in the Air (Classic)》
  source_url: https://warcraft.wiki.gg/index.php?title=Love_is_in_the_Air_(Classic)&action=raw
  quote: "The Alliance version begins with Aristan Mottar at the Stormwind Bank ... leads to \"Apothecary Staffron Lerent\" ... who is behind the love plague"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "银行大堂里一个穿工匠围裙的男人压低声音说话，背后是柜台与账簿"
  negative: "现代银行柜台, 玻璃幕墙"

- fact_id: stormwind.event.119
  claim: 儿童周的设定说法是：五月初、为期一周，双方阵营的英雄回馈战争的无辜者——孤儿。
  tag: ✅
  source: Warcraft Wiki《Children's Week》
  source_url: https://warcraft.wiki.gg/index.php?title=Children%27s_Week&action=raw
  quote: "At the beginning of May, and lasting for a week, it is a time for heroes of both sides to give back to the innocents of war...the [[Child|orphans]]!"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一个七八岁的孩子仰头看着比自己高两倍的成年人，手里攥着一只木哨"
  negative: "现代儿童节, 气球拱门"

- fact_id: stormwind.event.120
  claim: 冬幕节期间哥布林商贩在暴风城**贸易区**摆摊（Guchie Jinglepocket / Khole Jinglepocket）；而「冬天爷爷」在联盟一侧的主场是铁炉堡。
  tag: ⚠️
  source: Warcraft Tavern / Wowhead Classic 冬幕节指南（搜索摘要）
  source_url: https://www.warcrafttavern.com/wow-classic/guides/winter-veil/
  quote: "In Stormwind, Guchie Jinglepocket is located right in the center of the Trade District as you enter the city proper."
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: "贸易区中央一对绿皮哥布林摆的节庆摊子，摊上堆着彩纸包的礼盒"
  negative: "圣诞老人, 驯鹿, 雪橇"
```

### 1.3 全服事件 / 战争动员

```yaml
- fact_id: stormwind.event.121
  claim: 安其拉之门的开启由补丁 1.9.0 引入，且明确要求玩家先完成一场「规模浩大的世界事件」才能开门。
  tag: ✅
  source: Warcraft Wiki《Patch 1.9.0》（2006-01-03）
  source_url: https://warcraft.wiki.gg/wiki/Patch_1.9.0
  quote: "Players will have to complete a world event of massive proportions before they can open the Gates of Ahn'Qiraj on their realm."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一排排堆到人高的板条箱与麻袋，绳索捆扎，箱面烙着军徽"
  negative: "现代集装箱, 叉车, 托盘"

- fact_id: stormwind.event.122
  claim: 安其拉战争物资募集的联盟缴纳点**全部在铁炉堡军事区**，暴风城没有任何缴纳 NPC。
  tag: ✅
  source: Warcraft Wiki《Gates of Ahn'Qiraj》＋ Warcraft Tavern 战争物资指南
  source_url: https://www.warcrafttavern.com/wow-classic/guides/ahnqiraj-war-effort-guide/
  quote: "All Alliance NPCs can be found in The Military Ward of Ironforge"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例：不要把募集摊位画在暴风城广场上）"
  negative: "暴风城设募集点, 暴风城贸易区收物资"

- fact_id: stormwind.event.123
  claim: 联盟战争物资的品类与总量包括：铜锭 90,000、紫莲花 26,000、厚皮 80,000、斑点黄尾鱼 17,000、符文布绷带 400,000、亚麻绷带 800,000、丝绸绷带 600,000、铁锭 28,000、瑟银锭 24,000、阿尔萨斯之泪 20,000。
  tag: ✅
  source: Warcraft Wiki《Gates of Ahn'Qiraj》
  source_url: https://warcraft.wiki.gg/index.php?title=Gates_of_Ahn%27Qiraj&action=raw
  quote: "90,000 x Copper Bar (1 Signet), 26,000 x Purple Lotus (7 Signets), 80,000 x Thick Leather (7 Signets), 17,000 x Spotted Yellowtail (7 Signets), 400,000 x Runecloth Bandage (10 Signets)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "麻袋里露出成卷的白布绷带，旁边码着一摞摞铜锭与鞣好的厚皮"
  negative: "现代医用纱布, 塑封包装"

- fact_id: stormwind.event.124
  claim: 联盟一侧主持战争物资的是 Field Marshal Snowfall（雪落元帅）。
  tag: ✅
  source: Warcraft Wiki《Gates of Ahn'Qiraj》
  source_url: https://warcraft.wiki.gg/index.php?title=Gates_of_Ahn%27Qiraj&action=raw
  quote: "Field Marshal Snowfall for the Alliance"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一名披斗篷的高阶军官站在物资堆前，手里捏着一卷清单"
  negative: "现代军装, 文件夹"

- fact_id: stormwind.event.125
  claim: 开门后是一场持续十小时的全大陆事件，结束时全服广播「卡利姆多之力获胜」。
  tag: ✅
  source: Warcraft Wiki《Gates of Ahn'Qiraj》
  source_url: https://warcraft.wiki.gg/index.php?title=Gates_of_Ahn%27Qiraj&action=raw
  quote: "The Might of Kalimdor is victorious! The last of the Qiraji forces are defeated."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（声音事件，无画面；可拍市民抬头听见远处传来的消息）"
  negative: "暴风城内出现虫群, 沙漠场景"

- fact_id: stormwind.event.126
  claim: 天灾入侵是补丁 1.11 的世界事件，暴风城与幽暗城外各出现一座浮空城，随后对两座主城发动全面攻势。
  tag: ✅
  source: Warcraft Wiki《Scourge Invasion》
  source_url: https://warcraft.wiki.gg/index.php?title=Scourge_Invasion&action=raw
  quote: "The '''Scourge Invasion''' was a [[Event|world event]] in [[patch 1.11]] ... A necropolis has appeared outside Stormwind and Undercity, and soon the assault on these capitals will launch in full force."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城门外的天空里悬着一座倒金字塔状的黑色浮空石城，底部拖着绿色符文光，投下巨大阴影"
  negative: "飞碟, 科幻飞船, 纳克萨玛斯在城市正上方"

- fact_id: stormwind.event.127
  claim: 天灾入侵期间，银色黎明在被围困的城市内部设营，组织防御。
  tag: ✅
  source: Warcraft Wiki《Scourge Invasion》
  source_url: https://warcraft.wiki.gg/index.php?title=Scourge_Invasion&action=raw
  quote: "The Argent Dawn has already heeded their desperate call for help, setting up camps inside the besieged cities and rallying the defense against the encroaching darkness."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石板广场上支起的白底银纹帆布帐篷，帐前摆着长桌与木箱，三名穿银色黎明制服的人在登记"
  negative: "现代救灾帐篷, 红十字, 塑料折叠桌"

- fact_id: stormwind.event.128
  claim: 天灾入侵在暴风城内的具体表现是：银行旁支起银色黎明帐篷（银色黎明军需官 / 特使 / 征募官三人），亡灵周期性打进贸易区，常见的是 55 级的「炽燃者」，偶尔带 60 级精英「苍白恐魔」或「缝合恐魔」。
  tag: ✅
  source: Warcraft Tavern《Scourge Invasion Event Guide - WoW Classic》
  source_url: https://www.warcrafttavern.com/wow-classic/guides/scourge-invasion-event/
  quote: "These mobs usually spawn in the trade districts ... An Argent Dawn tent appears near Stormwind's bank, staffed by three NPCs: an Argent Quartermaster, Argent Emissary, and Argent Recruiter."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区喷泉边突然裂开的黑绿色地面，爬出一具具骨架与缝合怪，市民四散，卫兵结阵迎上"
  negative: "丧尸病毒, 现代枪械, 血腥内脏特写"

- fact_id: stormwind.event.129
  claim: 天灾在每座主城外扎营，并且在暴风城与幽暗城「格外猖狂」，会周期性打进城内。
  tag: ✅
  source: PC Gamer / Warcraft Tavern 转述的暴雪事件说明
  source_url: https://www.pcgamer.com/world-of-warcraft-classic-now-has-the-scourge-invasion-and-naxxramas-raid/
  quote: "The Scourge have set up camp outside each of your faction's major cities, and they've grown especially bold in Stormwind and Undercity, where they now periodically attack inside the city itself."
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: "城墙外一片插满骨幡的黑色营地，绿色火盆，游荡的食尸鬼"
  negative: "现代军营, 帐篷整齐排列"

- fact_id: stormwind.event.130
  claim: 天灾入侵的野外受袭区域是东瘟疫之地、燃烧平原、诅咒之地、塔纳利斯、艾萨拉、冬泉谷——全部在城外。
  tag: ✅
  source: Warcraft Wiki《Scourge Invasion》
  source_url: https://warcraft.wiki.gg/index.php?title=Scourge_Invasion&action=raw
  quote: "The zones that get attacked are [[Eastern Plaguelands]], [[Burning Steppes]], [[Blasted Lands]], [[Tanaris]], [[Azshara]], and [[Winterspring]]."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（用于口播地图，不入镜）"
  negative: "艾尔文森林被入侵, 暴风城郊农田被烧"

- fact_id: stormwind.event.131
  claim: Vanilla 时期的元素入侵（补丁 1.4.0）只发生在卡利姆多的希利苏斯、安戈洛环形山、艾萨拉、冬泉谷，从未打进任何城市。
  tag: ✅
  source: Vanilla WoW Wiki《Elemental Invasions》（搜索摘要）
  source_url: https://vanilla-wow-archive.fandom.com/wiki/Elemental_Invasions
  quote: "the appearance of groups of various types of elementals throughout Azeroth, although mostly just in Kalimdor: Silithus, Un'Goro Crater, Azshara, and Winterspring"
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "（反例：不要在暴风城画元素裂隙）"
  negative: "暴风城元素入侵, 城内暴雨, 元素领主"
```

### 1.4 城内剧情事件（Year 25 ADP 当下）

```yaml
- fact_id: stormwind.event.132
  claim: 「假面舞会」是 Vanilla 联盟奥妮克希亚钥匙链的城内大事：玩家护送雷金纳德·温德索尔从暴风城入口一路步行约十分钟到要塞，卡特拉娜·普瑞斯托在王座厅当场现出黑龙奥妮克希亚的真身。
  tag: ✅
  source: Warcraft Wiki《The Great Masquerade quest chain》
  source_url: https://warcraft.wiki.gg/wiki/The_Great_Masquerade_quest_chain
  quote: "after about a ten-minute-long walk from the Stormwind entrance to the Castle, Prestor will reveal her true form – the black dragon Onyxia"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一名披铠的老骑士捧着石板缓步穿过石桥与广场，身后跟着一小队人，两侧市民驻足让路"
  negative: "现代游行, 彩车, 横幅标语"

- fact_id: stormwind.event.133
  claim: 行进途中守门的马库斯·乔纳森将军先拦后让，喊出「都退下！你们看不出走在我们中间的是英雄吗？」，街上巡逻的卫兵则低声说「那走着的是位英雄」「一个活着的传奇……」。
  tag: ✅
  source: Warcraft Wiki《The Great Masquerade》
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "Stand down! Can you not see that heroes walk among us? ... There walks a hero ... A living legend..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "骑在高头战马上的将军抬手示意放行，铁甲反光，身后卫兵列队向两侧退开"
  negative: "现代警察, 路障, 警笛"

- fact_id: stormwind.event.134
  claim: 王座厅对质的关键台词是温德索尔的「假面舞会结束了，普瑞斯托女士。还是我该叫你的真名……奥妮克希亚」与普瑞斯托的「你有什么证据？你以为能走进这里，指着王室的鼻子，然后全身而退？」。
  tag: ✅
  source: Warcraft Wiki《The Great Masquerade》
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "The masquerade is over, Lady Prestor. Or should I call you by your true name... Onyxia... / What proof do you have? Did you expect to come in here and point your fingers at royalty and leave unscathed?"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "高拱顶王座厅内，一名贵妇立在王座台阶侧，对面是捧着石板的老骑士，两侧列着卫兵"
  negative: "法庭, 审判席, 现代礼服"

- fact_id: stormwind.event.135
  claim: 对质的结局是温德索尔被奥妮克希亚重伤致死，她随后传送离去；温德索尔的死打碎了博瓦尔身上的控制吊坠。
  tag: ✅
  source: Warcraft Wiki《The Great Masquerade》
  source_url: https://warcraft.wiki.gg/index.php?title=The_Great_Masquerade&action=raw
  quote: "If it was death that you came for, then the prophecy has been fulfilled. ... Bol... Bolvar... the medallion... use..."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座厅地面上一枚碎裂的金属吊坠，旁边倒着一具铠甲身影"
  negative: "血泊特写, 断肢"

- fact_id: stormwind.event.136
  claim: Vanilla 时期暴风城由博瓦尔·弗塔根以摄政的身份代年幼的安度因·乌瑞恩掌权，而卡特拉娜·普瑞斯托以王室顾问身份左右他的军事判断。
  tag: ✅
  source: Warcraft Wiki《Bolvar Fordragon》
  source_url: https://warcraft.wiki.gg/index.php?title=Bolvar_Fordragon&action=raw
  quote: "Highlord Bolvar Fordragon acted as Regent Lord of Stormwind or the Supreme Commander of Stormwind's forces on behalf of King Anduin."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座上坐着一个孩子，台阶下站着一名穿全身板甲的高大男子与一名黑发贵妇"
  negative: "成年国王坐在王座上, 瓦里安在场"

- fact_id: stormwind.event.137
  claim: 安度因是在父亲失踪后以孩童之身登基的，摄政是博瓦尔，进言者是卡特拉娜·普瑞斯托。
  tag: ✅
  source: Warcraft Wiki《Anduin Wrynn》
  source_url: https://warcraft.wiki.gg/index.php?title=Anduin_Wrynn&action=raw
  quote: "Under the regency of [[Bolvar Fordragon]] and the advice of [[Onyxia|Lady Katrana Prestor]], Anduin was only a child when he ascended to the throne following his father's disappearance."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一个十岁上下的金发男孩穿着不合身的王袍坐在过大的王座上"
  negative: "成年安度因, 圣光牧师装束"

- fact_id: stormwind.event.138
  claim: Vanilla 有一条完整的「失踪的外交官」任务链（17 环），揭露失踪者就是暴风城国王瓦里安·乌瑞恩，起点是城里的孩子托马斯把玩家引给要塞的德拉维主教，且以「私下」的名义接头；该链在补丁 4.0.3a 被移除。
  tag: ✅
  source: Warcraft Wiki《The Missing Diplomat》/《The Missing Diplomat quest chain》
  source_url: https://warcraft.wiki.gg/index.php?title=The_Missing_Diplomat&action=raw
  quote: "Thomas asks the player to meet Bishop DeLavey \"discreetly\" regarding \"a matter of some importance\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "要塞回廊拐角处，一名主教压低声音与来人说话，四下无人"
  negative: "公开告示, 通缉令张贴, 大声宣读"

- fact_id: stormwind.event.139
  claim: Vanilla 任务「袭击！」发生在暴风要塞的花园/中庭：格雷戈·列斯科瓦尔勋爵与「沉默之刃」玛尔佐在此密会并双双被杀；该任务同样在补丁 4.0.3a 被移除。
  tag: ✅
  source: Warcraft Wiki《The Attack!》
  source_url: https://warcraft.wiki.gg/index.php?title=The_Attack%21&action=raw
  quote: "There you are. What news from Westfall? ... Lord Gregor Lescovar ... Marzon the Silent Blade"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "要塞内庭花园：修剪过的绿篱、石凳、水池，两个人影贴着墙角低语"
  negative: "现代庭院, 喷泉雕塑, 草坪灯"

- fact_id: stormwind.event.140
  claim: 石匠工会史：工会受暴风城贵族院委托重建被兽人焚毁的暴风城，数年劳作后薪酬被赖账，工会被解散，骚乱中一枚投掷物当场打死了正在劝解的提芬王后。
  tag: ✅
  source: Warcraft Wiki《Stonemasons Guild》
  source_url: https://warcraft.wiki.gg/index.php?title=Stonemasons_Guild&action=raw
  quote: "While the stonemasons spent years toiling to rebuild the glorious city, they were left broke, their fees and salaries left unpaid. ... A projectile killed Queen Tiffin instantly while she tried to calm down the rioting stonemasons"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石墙上还留着未打磨完的凿痕与半截脚手架榫眼"
  negative: "崭新完工的墙面, 现代脚手架"

- fact_id: stormwind.event.141
  claim: Vanilla 当下暴风城的世界地位：自洛丹伦陷落以来，暴风王国已是人类最强的堡垒，也是联盟最强的国家。
  tag: ✅
  source: Warcraft Wiki《Stormwind City》
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_City&action=raw
  quote: "Since the fall of Lordaeron, the kingdom of Stormwind has become the strongest bastion of humanity, as well as the most powerful nation within the Alliance."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城墙外远眺：连绵蓝顶尖塔与高耸石墙，狮鹫在塔尖之间盘旋"
  negative: "废墟, 战后焦土"
```

### 1.5 城市自身的制度性日常

```yaml
- fact_id: stormwind.event.142
  claim: 暴风城的公会注册与公会战袍设计在贸易区的「暴风城游客中心」办理（公会管理员 Aldwin Laughlin、战袍设计师 Rebecca Laughlin）。
  tag: ✅
  source: Warcraft Wiki《Stormwind Visitor's Center》
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_Visitor%27s_Center&action=raw
  quote: "a [[visitor center]] located in the [[Trade District]] in [[Stormwind City]] ... Aldwin Laughlin - Guild Master ... Rebecca Laughlin - Tabard Designer"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一间挂满各色战袍样布的木石办事厅，柜台后摊着羊皮纸与墨水"
  negative: "现代办证大厅, 叫号机, 玻璃窗口"

- fact_id: stormwind.event.143
  claim: 教堂广场同时是暴风城的市政中心，容纳市政厅与孤儿院，银色黎明的驻地就在孤儿院背后、教堂东北、市政厅旁边。
  tag: ⚠️
  source: Warcraft Wiki《Cathedral Square》/《The Argent Dawn (Stormwind)》
  source_url: https://warcraft.wiki.gg/index.php?title=Cathedral_Square&action=raw
  quote: "It is also an important civic center, housing City Hall and the Orphanage (Stormwind City). ... behind the Orphanage (Stormwind City), just to the north-east of the Cathedral of Light, and beside City Hall."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "大教堂前的开阔石砌广场，四周是几栋二层石木公共建筑"
  negative: "乌瑟尔雕像, 墓园, 湖岸, 凉亭"

- fact_id: stormwind.event.144
  claim: 暴风城孤儿院在教堂广场、大教堂东南侧，由孤儿院长夜莺女士与谢琳打理；夜莺女士的原话把孤儿定义为「战争的代价」。
  tag: ✅
  source: Warcraft Wiki《Orphan Matron Nightingale》/《Orphanage (Stormwind City)》
  source_url: https://warcraft.wiki.gg/index.php?title=Orphan_Matron_Nightingale&action=raw
  quote: "There are costs with war, <class>... ones often overlooked. Those costs are the orphans - children who have lost their parents to the far-too-numerous conflicts that rage across Azeroth."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一位系着围裙、头发挽起的中年妇人站在一扇木门外，门内透出孩子的声音"
  negative: "现代福利院, 铁门, 制服"

- fact_id: stormwind.event.145
  claim: Vanilla 儿童周联盟侧的孤儿名叫 Randis，起点是教堂广场的夜莺女士（发人类孤儿哨），节庆约在 5 月 1 日至 7 日；孤儿指定要去的三处（泰达希尔永恒之树枝、洛克莫丹石堡水坝、西部荒野幽灵灯塔）与结尾的塞拉摩全部在暴风城之外。
  tag: ✅
  source: Warcraft Tavern《WoW Classic Children's Week Guide》
  source_url: https://www.warcrafttavern.com/wow-classic/guides/childrens-week/
  quote: "Orphan Name: Randis ... Quest Giver: Orphan Matron Nightingale in Cathedral Square, Stormwind ... The Bough of the Eternals - Teldrassil; The Stonewrought Dam - Loch Modan; Spooky Lighthouse - Westfall coast"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "孩子把一只木哨挂在脖子上，另一只手被牵着"
  negative: "孤儿在暴风城内完成所有行程（设定未写）"

- fact_id: stormwind.event.146
  claim: 荣誉大厅是联盟在暴风城的军官营房，位于旧城区南部，加入于补丁 1.4.0；在 Vanilla 它是一个**有荣誉门槛才进得去**的独立区域，直到补丁 2.0.1 才取消门槛。
  tag: ✅
  source: Warcraft Wiki《Champions' Hall》
  source_url: https://warcraft.wiki.gg/index.php?title=Champions%27_Hall&action=raw
  quote: "The '''Champions' Hall''' is the officer's [[barracks]] for the [[Alliance]] in [[Stormwind City]]. It is located in the south of the [[Old Town]]. ... {{Patch 2.0.1|note=There is no longer an Honor requirement to enter the Champions' Hall."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一扇有卫兵把守的厚重木门，门楣挂着军团徽记，门里透出火光与人声"
  negative: "对所有人开放的大厅, 现代军官俱乐部"

- fact_id: stormwind.event.147
  claim: 战场指挥官（battlemaster）加入于补丁 1.6.0，暴风城的战场指挥官站在**暴风要塞的作战室**。
  tag: ✅
  source: Warcraft Wiki《Battlemaster》
  source_url: https://warcraft.wiki.gg/index.php?title=Battlemaster&action=raw
  quote: "{{Patch 1.6.0|note=Added.}} ... [[War Room]], [[Stormwind Keep]]"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "作战室里一张铺着大幅羊皮地图的长桌，桌上压着小旗与木制标记，四周站着军官"
  negative: "现代沙盘, 电子屏, 指挥中心"

- fact_id: stormwind.event.148
  claim: 奥特兰克山谷与战歌峡谷两个战场加入于补丁 1.5.0（2005 年 6 月 7 日上线），阿拉希盆地加入于补丁 1.7（2005 年 9 月 13 日）。
  tag: ✅
  source: Warcraft Wiki《Battleground》
  source_url: https://warcraft.wiki.gg/index.php?title=Battleground&action=raw
  quote: "The two initial battleground areas, [[Alterac Valley]] and [[Warsong Gulch]], went live June 7th, 2005. ... [[Arathi Basin]] was added to the list in [[patch 1.7]] on September 13th, 2005."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "征募处外排着队的年轻人，肩上挎着自带的包袱与旧剑"
  negative: "现代征兵站, 体检表, 号码牌"

- fact_id: stormwind.event.149
  claim: 大教堂的地下墓室是「受尊敬的逝者」的安息处——牧师、战争英雄、圣骑士等。
  tag: ✅
  source: Warcraft Wiki《Cathedral of Light》
  source_url: https://warcraft.wiki.gg/index.php?title=Cathedral_of_Light&action=raw
  quote: "the cathedral's catacombs are the resting place of the honored dead: priests, war heroes, paladins, and others"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂地下的低矮拱顶石室，两侧石棺与壁龛，烛台一路延伸进黑暗"
  negative: "室外墓园, 墓碑成排, 湖岸"

- fact_id: stormwind.event.150
  claim: 大教堂由本尼迪塔斯大主教主持，是圣光教会最显赫的纪念建筑，被形容为「一处优雅而宁静、适合祈祷与省思的地方」。
  tag: ✅
  source: Warcraft Wiki《Cathedral of Light》
  source_url: https://warcraft.wiki.gg/index.php?title=Cathedral_of_Light&action=raw
  quote: "an elegant and peaceful place, inviting for prayer and reflection"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "高窗投下的成排光柱落在中殿石地上，尽头是圣光徽记与祭坛"
  negative: "哥特式彩绘玻璃基督教图案, 十字架"

- fact_id: stormwind.event.151
  claim: 暴风城卫兵的职能之一是给人指路，问他们时会说「你要去哪儿？」，并会回应挥手、行礼等动作。
  tag: ✅
  source: Warcraft Wiki《Stormwind City Guard (NPC)》
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_City_Guard_(NPC)&action=raw
  quote: "What do you need directions to?"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "戴着全罩头盔、持长戟与鸢形盾的卫兵，抬手往一个方向指"
  negative: "现代警察手势, 交警"

- fact_id: stormwind.event.152
  claim: 贸易区中央的（互联）拍卖行是补丁 1.9 加入的，Cata 时才被挪到靠近旅店的位置。
  tag: ✅
  source: Warcraft Wiki《Trade District》
  source_url: https://warcraft.wiki.gg/index.php?title=Trade_District&action=raw
  quote: "Patch 1.9 added the linked Auction House in the center of the Trade District"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "广场中央一栋开放式拍卖行，柜台前挤满举着货品与钱袋的人"
  negative: "现代拍卖槌, 举牌号, 电子屏报价"

- fact_id: stormwind.event.153
  claim: 英雄谷是暴风城门前的谷地，一座石桥横跨护城河，是所有进城者看到的第一景；路两侧立着五尊第二次战争远征德拉诺的联盟英雄雕像——正中图拉扬，一侧库德兰·蛮锤与卡德加，另一侧达纳斯·托尔贝恩与奥蕾莉亚·风行者。
  tag: ✅
  source: Warcraft Wiki《Valley of Heroes》
  source_url: https://warcraft.wiki.gg/index.php?title=Valley_of_Heroes&action=raw
  quote: "The Valley of Heroes is a valley that lies before Stormwind Gate. A bridge of stone crosses the narrow moat and is the first sight of all who enter."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石桥两侧五尊两倍真人高的石像，持武器俯视行人，桥下是护城河水"
  negative: "哈蒙德·克雷将军（Cata 后才接任）, 现代纪念碑"

- fact_id: stormwind.event.154
  claim: Vanilla 时期暴风城防务的统帅是马库斯·乔纳森将军（62 级精英），骑马立在英雄谷；他在补丁 4.0.3a 被移除、由哈蒙德·克雷接任，所以「克雷将军」属于版本错置。
  tag: ✅
  source: Warcraft Wiki《General Marcus Jonathan》（搜索摘要）＋《Valley of Heroes》
  source_url: https://warcraft.wiki.gg/wiki/General_Marcus_Jonathan
  quote: "General Marcus Jonathan is a level 62 Elite NPC that can be found in Stormwind City ... removed from World of Warcraft in patch 4.0.3a but is present in Classic"
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "骑在披甲战马上的银发将军，一手握缰一手按剑，停在桥头不动"
  negative: "哈蒙德·克雷, 步行的将军"

- fact_id: stormwind.event.155
  claim: 矮人区是矮人在第二次战争后按麦格尼国王派工的名义建的飞地；区内的锻炉整日冒出常驻的烟霾，伴着不停的锤声；设定称有近三万名矮人住在这个区，比他们自己的首都铁炉堡还多。
  tag: ✅
  source: Warcraft Wiki《Dwarven District》
  source_url: https://warcraft.wiki.gg/index.php?title=Dwarven_District&action=raw
  quote: "The forges in the district produce a constant haze, supplemented by the constant strokes of smiths' hammers. ... almost 30,000 dwarves reside in this district, more than in their capital city of Ironforge"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "锻炉口喷出的橙红火光与终日不散的青灰烟霾，铁砧上飞溅的火星"
  negative: "矮人区有拍卖行与银行（Cata 才加）, 现代工厂烟囱"

- fact_id: stormwind.event.156
  claim: 暴风城的狮鹫管理员是杜加·长饮，在暴风城的狮鹫栖木（坐标 71.0, 72.6）；他的原话是「这些大家伙认得你走不到的路，能把你送得比最快的马还快」。
  tag: ✅
  source: Warcraft Wiki《Dungar Longdrink》
  source_url: https://warcraft.wiki.gg/index.php?title=Dungar_Longdrink&action=raw
  quote: "Where is it ye would like to go <lad/lass>? For just a few coin my Gryphons can get ye there faster than even the swiftest horse."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "高台栖木上一排系着鞍具的狮鹫，抖翅、蹬爪，飞起时压出一阵风把人的斗篷吹开"
  negative: "飞机跑道, 现代航站楼, 机场广播"

- fact_id: stormwind.event.157
  claim: 法师区的「屠宰羔羊」是一间破旧酒馆，其地窖是暴风城术士的密所与教学处。
  tag: ✅
  source: Warcraft Wiki《Slaughtered Lamb》
  source_url: https://warcraft.wiki.gg/index.php?title=Slaughtered_Lamb&action=raw
  quote: "The Slaughtered Lamb is a seedy pub in the Mage Quarter of Stormwind City. ... The tavern's catacombs serve as the sanctum of the warlocks of Stormwind."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "酒馆地板下的石阶通向一间点着绿色蜡烛的地窖，地上刻着一圈符文召唤阵"
  negative: "血祭, 裸露献祭, 现代邪教符号"

- fact_id: stormwind.event.158
  claim: 旧城区是暴风城最老的区，风格「粗陋、破败」，街道「比其它区都更脏更臭」，住的是城里的穷人，同时也是军事与情报中枢（指挥中心、SI:7）。
  tag: ✅
  source: Warcraft Wiki《Old Town》
  source_url: https://warcraft.wiki.gg/index.php?title=Old_Town&action=raw
  quote: "rustic, downtrodden ... far dirtier and smellier than the other districts"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "窄巷、木构外露的旧楼、泥泞石板、晾衣绳，尽头是营房与练兵场"
  negative: "整洁石板路, 贵族宅邸, 现代贫民窟铁皮房"

- fact_id: stormwind.event.159
  claim: 暴风城运河里能钓到鲶鱼和螃蟹，钓鱼是城中居民喜爱的消遣。
  tag: ✅
  source: Warcraft Wiki《Stormwind City》
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_City&action=raw
  quote: "fishing is a favored sport"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河石阶上坐着几个垂钓的人，浮标在水面上下点头"
  negative: "现代钓具, 碳素竿, 折叠椅"

- fact_id: stormwind.event.160
  claim: Vanilla 时期的暴风城公园是市民的休闲地，也是来访暗夜精灵的避居处，广场中心有一口暗夜精灵立的月亮井，还是东部王国唯一有德鲁伊训练师的地方。
  tag: ✅
  source: Warcraft Wiki《Park》
  source_url: https://warcraft.wiki.gg/index.php?title=Park&action=raw
  quote: "a place devoted to leisure activities for Stormwind's populace ... a refuge for visiting night elves, who found the comforting presence of nature a welcome respite from the vast stone thoroughfares of Stormwind proper ... the only place in the Eastern Kingdoms where druid trainers resided"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石城之内一片绿地：高树、草坡、中心一口泛着幽蓝光的月亮井，紫皮长耳的暗夜精灵在树下"
  negative: "公园被毁, 巨坑, 海水倒灌"
```

### 1.6 版本错置警戒（画面上极易踩的坑）

```yaml
- fact_id: stormwind.event.161
  claim: 暴风城港口加入于补丁 3.0.2（巫妖王之怒），Vanilla 的暴风城**没有港口**。
  tag: ❌
  source: Warcraft Wiki《Stormwind Harbor》Patch changes
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_Harbor&action=raw
  quote: "{{Patch 3.0.2|note=Added.}}"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例，不得入镜）"
  negative: "暴风城港口, 码头, 大帆船靠泊, 海鸥, 船坞"

- fact_id: stormwind.event.162
  claim: 暴风城墓园加入于补丁 4.0.3a（大地的裂变），Vanilla 城内**没有室外墓园**，也没有教堂广场北边的湖与凉亭。
  tag: ❌
  source: Warcraft Wiki《Stormwind City Cemetery》/《Cathedral Square》
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_City_Cemetery&action=raw
  quote: "Added ... 4.0.3a"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例，不得入镜）"
  negative: "暴风城墓园, 成排墓碑, 提芬王后墓, 教堂广场旁的湖, 凉亭"

- fact_id: stormwind.event.163
  claim: 教堂广场上的雕像在 Vanilla 是阿隆索斯·法奥，直到补丁 4.0.3a 才换成乌瑟尔·光明使者。
  tag: ❌
  source: Warcraft Wiki《Cathedral Square》Patch changes
  source_url: https://warcraft.wiki.gg/index.php?title=Cathedral_Square&action=raw
  quote: "Alonsus Faol monument replaced with one of Uther the Lightbringer"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（Vanilla 正解：广场立的是阿隆索斯·法奥像）"
  negative: "乌瑟尔雕像, 光明使者纪念碑"

- fact_id: stormwind.event.164
  claim: 巫师圣殿的「暴风城传送门大厅」是补丁 8.1.5 才把塔内彻底重做出来的；Vanilla 的巫师圣殿只有法师训练师与传送门训练师（拉里曼·普尔杜），**没有常驻传送门阵列**。
  tag: ❌
  source: Warcraft Wiki《Wizard's Sanctum》
  source_url: https://warcraft.wiki.gg/index.php?title=Wizard%27s_Sanctum&action=raw
  quote: "Its interior was completely revamped in patch 8.1.5 to house the Stormwind Portal Room"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（Vanilla 正解：塔内是书架、星象仪、法师训练师，没有一圈发光传送门）"
  negative: "一圈常驻传送门, 达拉然传送门, 奥格瑞玛传送门, 传送门大厅"

- fact_id: stormwind.event.165
  claim: 矮人区的拍卖行与皇家银行是大地的裂变才加的，Vanilla 暴风城只有贸易区一处拍卖行。
  tag: ❌
  source: Warcraft Wiki《Dwarven District》
  source_url: https://warcraft.wiki.gg/index.php?title=Dwarven_District&action=raw
  quote: "Auction House and Royal Bank (added in the Cataclysm expansion)"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例，不得入镜）"
  negative: "矮人区拍卖行, 矮人区银行"

- fact_id: stormwind.event.166
  claim: 「元素动荡」（元素攻打暴风城、暴风城被暴雨与气/水元素淹没）是大地的裂变 4.0.3a 的前夕事件，**与 Vanilla 无关**。
  tag: ❌
  source: Warcraft Wiki《Elemental Unrest》
  source_url: https://warcraft.wiki.gg/index.php?title=Elemental_Unrest&action=raw
  quote: "The event culminated in elementals attacking [[Stormwind]], [[Orgrimmar]], [[Ironforge]], and [[Thunder Bluff]]. ... During the invasion, Stormwind and Thunder Bluff are hit by powerful rainstorms as they are invaded by Air and Water elementals."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例，不得入镜）"
  negative: "元素入侵暴风城, 城内暴雨, 水元素, 气元素, 元素裂隙"

- fact_id: stormwind.event.167
  claim: 暗月马戏团加入于补丁 1.6.0；在补丁 4.3.0 之前它只在三处摆摊，联盟侧是**艾尔文森林的闪金镇外**，从不在暴风城内；达克索尔加农炮是 1.9.0 才加的，蒸汽坦克是 1.10.0 才加的。
  tag: ⚠️
  source: Warcraft Wiki《Darkmoon Faire》
  source_url: https://warcraft.wiki.gg/index.php?title=Darkmoon_Faire&action=raw
  quote: "Prior to [[patch 4.3.0]], the Darkmoon Faire was located solely in three locations: Outside [[Goldshire]] in [[Elwynn Forest]], outside [[Thunder Bluff]] in [[Mulgore]], and on the outskirts of [[Shattrath City]] in [[Outland]]'s [[Terokkar Forest]]."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "森林空地上的紫色条纹帐篷群、旗幡与木制游艺架"
  negative: "暗月岛, 旋转木马, 暗月马戏团开在暴风城内, 宠物对战"

- fact_id: stormwind.event.168
  claim: 收获节的设定是向为我们牺牲的英雄致谢；联盟侧的会场在铁炉堡，献祭的对象是西瘟疫之地的乌瑟尔之墓——都不在暴风城。
  tag: ⚠️
  source: Warcraft Wiki《Harvest Festival》
  source_url: https://warcraft.wiki.gg/index.php?title=Harvest_Festival&action=raw
  quote: "During the Harvest Festival of Azeroth, the Horde and the Alliance give thanks to heroes for the sacrifices - in some cases ultimate sacrifices - they have given on our behalf."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "堆着谷捆、南瓜与果篮的祭桌"
  negative: "暴风城办收获节主会场, 感恩节火鸡"
```

**注册表统计：共 68 条事实，`fact_id` ＝ `stormwind.event.101`–`.168`（连续、无空号，与 W7 已用的 `.001`–`.011` 不重叠）。
其中 ai_read 64 条（抓到原文页）、ai_draft 4 条（`.120` / `.129` / `.131` / `.154`，只拿到搜索摘要）。
目标 ≥40 条、ai_read ≥32 —— **均达标**。**

---

## 2. 候选池总表

> 覆盖八块代号：**貌**＝城市面貌 / **吃** / **住** / **穿** / **活**＝人们怎么活动 / **构**＝机构 / **娱**＝娱乐 / **事**＝当天大事

| # | 候选名 | 版本可用性 | 所在区 | 覆盖八块 | 分量 | 风险 | fact_id |
|---|---|---|---|---|---|---|---|
| 1 | **天灾入侵暴风城**（浮空城 + 贸易区尸潮 + 银色黎明帐篷） | ✅ 1.11 | 城门外 + 贸易区 + 银行边 | 貌·活·构·事 | ★★★★★ 能独撑 | 基调从「逛街」变「战时」，会吃掉吃住穿的篇幅 | 126–130 |
| 2 | **假面舞会：温德索尔的最后一程** | ✅ Vanilla | 英雄谷→贸易区→要塞王座厅 | 貌·活·构·事 | ★★★★★ 能独撑 | 与已交付候选③同属奥妮克希亚线；结局死人，偏沉 | 132–137 |
| 3 | **元宵节：白天挂灯、入夜整点烟花** | ✅ 1.9.0 | 暴风城公园 + 全城 | 貌·娱·活·事 | ★★★★☆ 能独撑 | 几乎零冲突；需注意长者在公园不在城外 | 105·110–113 |
| 4 | **儿童周：借一个孤儿当向导** | ✅ 1.4.0 | 教堂广场孤儿院 | 全八块 | ★★★★★ 能独撑（**结构最贴节目形态**） | 孤儿的法定行程全在城外，「在城里逛」属 ⚠️ 推演 | 103·119·144·145 |
| 5 | **仲夏火焰节：运河边的大篝火** | ✅ 1.11 | 运河（49,72） | 貌·娱·吃·事 | ★★★☆☆ 需搭配 | 与 1 同为 1.11，同一天并存要解释 | 107·114·115 |
| 6 | **爱情降临节 +「危险的爱情」：卫兵是不是被下药了** | ✅ 1.9.3 | 银行 + 全城岗哨 | 活·构·事·娱 | ★★★★☆ 能独撑 | 悬疑线收尾在城外（希尔斯布莱德），要改成城内闭环 | 106·117·118 |
| 7 | **万圣节：面具、糖桶与变装魔杖** | ✅ 1.8.0 | 旅店 + 城门外主会场 | 娱·吃·活·貌 | ★★★☆☆ 需搭配 | 无头骑士 / 柴垛人**严禁出现** | 104·116 |
| 8 | **冬幕节：石城披雪与哥布林礼盒摊** | ✅ 1.2.0 | 贸易区 | 貌·娱·吃 | ★★☆☆☆ 只能当片段 | 「冬天爷爷」主场在铁炉堡，不能安在暴风城 | 102·120 |
| 9 | **贵族遇刺：列斯科瓦尔之死** | ✅ Vanilla（4.0.3a 移除） | 暴风要塞花园 | 构·事·活 | ★★★☆☆ 需搭配 | 密谋戏，画面信息少；与 2 抢要塞篇幅 | 139 |
| 10 | **战场征召：作战室里的奥山动员** | ✅ 1.5.0/1.6.0 | 暴风要塞作战室 + 旧城区练兵场 | 构·活·事 | ★★★☆☆ 需搭配 | 战场是游戏机制，世界内说法要谨慎包装 | 147·148·158 |
| 11 | **荣誉大厅：凭军衔才进得去的军官营房** | ✅ 1.4.0 | 旧城区南部 | 构·活·穿 | ★★☆☆☆ 只能当片段 | 「进不去」本身是戏；不要画成对外开放 | 146 |
| 12 | **安其拉战争物资：往铁炉堡运的那一列车** | ⚠️ 1.9.0（收点不在城内） | 矮人区→矿道地铁 | 活·事·构 | ★★★★☆ 能独撑（需明标推演） | **必须标 ⚠️**：设定只写铁炉堡收点，「暴风城起运」是我们推的 | 121–125 |
| 13 | **公会特许状：在贸易区街头凑签名** | ✅ Vanilla | 贸易区游客中心 | 构·活·娱 | ★★☆☆☆ 只能当片段 | 是玩家机制的世界内翻译，要写成「结社登记」 | 142 |
| 14 | **苦工节：哥布林的打折烟花摊** | ⚠️ 1.12.1（仅欧服 / 9 月 30 日） | 贸易区 | 娱·吃·事 | ★★☆☆☆ 只能当片段 | 「只在欧服」是现实世界的运营口径，世界内没法解释，需处理 | 109 |
| 15 | **暗月马戏团进艾尔文森林**（城外一日游） | ⚠️ 1.6.0（不在城内） | 闪金镇外 | 娱·吃·事 | ★★★☆☆ 需搭配 | 出城即破「一城一天」的框；只能当「城门口望见旗幡」 | 167 |
| 16 | **收获节 / 复活节** | ⚠️（会场不在暴风城） | 铁炉堡 / 闪金镇 | — | ★☆☆☆☆ | 不建议作为主事件 | 108·168 |
| 17 | **狮鹫栖木的早班起降** | ✅ Vanilla | 贸易区高台 | 貌·活·构 | ★★☆☆☆ 只能当片段 | 无「事件」性，只是景观；适合做开场或转场 | 156 |
| 18 | **矮人区终日不散的锻炉烟霾** | ✅ Vanilla | 矮人区 | 貌·活·穿 | ★★☆☆☆ 只能当片段 | 同上；但「三万矮人比铁炉堡还多」是好口播 | 155 |
| 19 | **屠宰羔羊地窖：城里公开存在的术士团** | ✅ Vanilla | 法师区 | 构·貌·活 | ★★☆☆☆ 只能当片段 | 平台合规：不要血祭/邪教视觉 | 157 |

**新候选计 19 个**（不含已交付的 ①②③），其中「✅ 版本可用且落在城内」的 11 个。

---

## 3. 前五名详述

---

### 第 1 名｜天灾入侵暴风城（Scourge Invasion，补丁 1.11）

| 项 | 内容 |
|---|---|
| **候选名** | 城门外悬着一座亡灵浮空城，而城里的人还在照常做买卖——直到尸潮打进贸易区。 |
| **是什么** | 补丁 1.11 的全服世界事件，为纳克萨玛斯开放做铺垫。设定原话：`A necropolis has appeared outside Stormwind and Undercity, and soon the assault on these capitals will launch in full force.`（`source_url` https://warcraft.wiki.gg/index.php?title=Scourge_Invasion&action=raw ）银色黎明随即进城设营：`The Argent Dawn has already heeded their desperate call for help, setting up camps inside the besieged cities`。城内实际表现见 Warcraft Tavern Classic 指南：`These mobs usually spawn in the trade districts`，银行旁支起三人编制的银色黎明帐篷。 |
| **版本** | ✅ 补丁 1.11.0（2006-06-19），Vanilla 晚期。**不是全程存在**——它是限时世界事件，只在纳克萨玛斯开放前后跑。若要用它当「今天」，需接受这一天是 Vanilla 末段的某一天。 |
| **在哪** | ① 城门外／英雄谷上空：浮空城 ② 贸易区：尸潮爆发点 ③ 贸易区银行旁：银色黎明帐篷 ④ 全城：卫兵进入戒备 |
| **画面** | 1）逆光仰拍，一座倒金字塔状的黑色石城悬在城墙外的天上，底部拖绿色符文光，在护城河水面投下缓慢移动的巨大阴影；2）贸易区喷泉边地面裂开黑绿色口子，骨架与缝合怪爬出，卖花的推车被撞翻；3）银行台阶旁支起白底银纹的帆布帐篷，长桌上摊着名册，三名穿银色黎明制服的人边写边发放护符；4）卫兵在拱门下横戟结成一道线，把市民往教堂广场方向赶；5）打斗结束后石板上留下的一摊黑色灼痕与一枚裂开的水晶。 |
| **与逛单八块的关系** | **貌**（浮空城彻底改写城市天际线）**活**（市民的一天被打断，看得见他们平时在干什么）**构**（银色黎明＝临时进城的第五个机构；大教堂成为避难点）**事**（满分）。**吃／住／穿／娱** 会被挤压——这是它最大的代价。 |
| **风险** | ① 基调风险最大：一旦开打，「从早逛到晚」的散步感会断。② 与四个既定机构抢时长：矮人区地铁与法师区圣殿在尸潮日很难安排「悠闲参观」。③ 平台合规：亡灵题材要控制血腥度（用骨架/腐甲而非内脏）。④ 与候选 5（仲夏节）同为 1.11，若两者同日需要一句解释。 |

**作为「当天大事」时这一天怎么排（5 个时间点）：**
1. **清晨**｜旅行者从英雄谷进城，抬头才发现天上多了一座东西——但城里人已经看了三天，照常开摊。（对比：奇观 vs 日常麻木）
2. **上午**｜贸易区拍卖行、狮鹫栖木、游客中心照常运转；镜头带出银行旁刚支起的银色黎明帐篷，排队的人在登记自愿守夜。
3. **午后**｜进矮人区与矿道地铁，讲运输与通勤；地铁站台上多了往铁炉堡疏散的家眷。
4. **黄昏**｜第一波尸潮从贸易区地面钻出，卫兵结阵，市民退向教堂广场；旅行者被挤进大教堂，顺势讲这座机构。
5. **入夜**｜打退之后，广场上收拾残局、点起火盆；旅行者站在城墙上对镜收束：这座城最强的不是墙，是明天早上还会照常开摊。

---

### 第 2 名｜假面舞会：温德索尔的最后一程（The Great Masquerade）

| 项 | 内容 |
|---|---|
| **候选名** | 一个老骑士捧着石板，从城门一路走到王座前，当庭指认王室顾问是一条黑龙。 |
| **是什么** | Vanilla 联盟奥妮克希亚钥匙链的城内高潮。设定原话：`after about a ten-minute-long walk from the Stormwind entrance to the Castle, Prestor will reveal her true form – the black dragon Onyxia`（ https://warcraft.wiki.gg/wiki/The_Great_Masquerade_quest_chain ）。沿途守门的马库斯·乔纳森将军从拦到让：`Stand down! Can you not see that heroes walk among us?`；街上卫兵低声传话：`There walks a hero` / `A living legend...`。王座厅对质：`The masquerade is over, Lady Prestor. Or should I call you by your true name... Onyxia...` |
| **版本** | ✅ Vanilla 原生（奥妮克希亚之巢是 1.0 内容，该链在整个 1.x 全程可跑）。⚠️ 需注意：温德索尔本人在补丁 4.0.3a 后的正史里已不在此位置，但在 Classic 里在。 |
| **在哪** | 英雄谷（城门）→ 贸易区 → 要塞前庭 → **暴风要塞王座厅**（四个既定机构之一） |
| **画面** | 1）城门石桥上，骑马的将军抬手，铁甲反光，两列卫兵向两侧退开让出一条路；2）捧着石板的银发骑士缓步穿过贸易区，摊主停下手里的活，孩子跟着走了几步被大人拉回去；3）王座厅高拱顶下，一名黑发贵妇立在王座台阶侧，对面是老骑士，两侧是列队卫兵，光柱从高窗斜切下来；4）贵妇的轮廓在一瞬间拉长、鳞片浮起——黑龙真身撑满整个厅堂，卫兵被气浪掀翻；5）空荡的厅内地面上，一枚碎成两半的金属吊坠躺在石缝里。 |
| **与逛单八块的关系** | **构**（整条路线正好串起 城门→贸易区→要塞王座厅，是「参观机构」的天然路径）**貌**（一条贯穿全城的移动长镜）**活**（市民的反应就是最好的市井素材）**事**（满分）。**吃／住／穿** 需要在护送途中顺带交代——这反而比静态讲解更自然。 |
| **风险** | ① **与已交付候选③（奥妮克希亚头颅）同属一条线**——若两者都用，观众会觉得这一季全在讲同一条龙；建议二选一（本路认为本候选比头颅更强，因为它是「发生」而不是「已经发生」）。② 结局死人且有巨龙现形，制作量级高（一条龙的分镜成本≈整集三分之一）。③ 王座厅被大事件占满，就很难再平静讲解王座厅这个机构本身。 |

**作为「当天大事」时这一天怎么排（5 个时间点）：**
1. **清晨**｜旅行者在城门排队进城，听见前头骚动——一个浑身尘土的老骑士被将军拦下。
2. **上午**｜将军放行。旅行者跟着这支小队走，用它作为动线把贸易区（拍卖行、狮鹫、游客中心）一路讲过去。
3. **正午**｜队伍拐进要塞前庭，旅行者被拦在门外，趁机去矮人区与矿道地铁、法师区圣殿（把两个机构塞进这段空档）。
4. **午后**｜回到要塞，混进王座厅旁听：对质、现真身、老骑士倒下。
5. **入夜**｜城里各处议论纷纷；旅行者在旅店吃饭、住下，对镜收束：这座城今天才知道，它的顾问是一条龙。

---

### 第 3 名｜儿童周：借一个孤儿当向导（Children's Week，补丁 1.4.0）

| 项 | 内容 |
|---|---|
| **候选名** | 城里的规矩是：这一周，你可以领一个孤儿出门，带他看看这座城。 |
| **是什么** | 补丁 1.4.0 加入的节日。设定原话：`At the beginning of May, and lasting for a week, it is a time for heroes of both sides to give back to the innocents of war...the orphans!`。起点是教堂广场的孤儿院长夜莺女士，她对孤儿的定义是：`Those costs are the orphans - children who have lost their parents to the far-too-numerous conflicts that rage across Azeroth.` Classic 联盟侧的孤儿名叫 **Randis**。 |
| **版本** | ✅ 补丁 1.4.0（2005 年），Vanilla 全程存在，每年五月初一周。**在九个节日里版本最"早"、最安全**。 |
| **在哪** | 教堂广场孤儿院（大教堂东南侧，坐标约 56.3, 54.0） |
| **画面** | 1）大教堂东南一扇不起眼的木门，门口站着系围裙的妇人，门内传出孩子的声音；2）一个七八岁、穿麻布短褐的孩子被交到旅行者手里，脖子上挂一只木哨；3）孩子在狮鹫栖木前仰头看狮鹫起飞，被翅风吹得眯眼；4）孩子第一次坐进矿道地铁的矿车，两手死死抓住把手；5）傍晚把孩子送回那扇木门，孩子回头挥手——门在身后合上。 |
| **与逛单八块的关系** | **全部八块**。这是本路唯一一个**能把「逛」本身变成剧情**的候选：孩子＝观众的代入体，旅行者对孩子讲解就不再是对镜头讲解，「为什么带你看这个」自动产生动机。吃（给孩子买冰淇淋，设定里确有 `Tigule and Foror's Strawberry Ice Cream`）、住（旅店）、穿（给孩子添件衣服）都有天然由头。 |
| **风险** | ① **最大风险是 ⚠️ 推演**：设定里 Randis 指定要去的三个地方（泰达希尔、洛克莫丹、西部荒野）**全在城外**，「在暴风城里逛」是我们改的。必须在文档里显式标 ⚠️，不能说成设定明载。② 「当天的大事」分量偏软——它不是一件"大事"，是一项制度；若系列不变量 I-1 要求的是"事件"，需要再叠一个小事件（例如当天正好是孤儿院缺粮 / 有人来认领孩子）。③ 情绪基调偏暖，与"科普"的距离要把握好，别滑成煽情短剧。 |

**作为「当天大事」时这一天怎么排（5 个时间点）：**
1. **清晨**｜教堂广场，孤儿院开门；旅行者登记领走 Randis，夜莺女士交代规矩（顺势讲大教堂与教会这个机构）。
2. **上午**｜贸易区：拍卖行、游客中心、狮鹫栖木。孩子问"狮鹫吃什么"，引出物价与日常。
3. **正午**｜矮人区：烟霾、锻炉、三万矮人；吃一顿（街边食摊）。
4. **午后**｜矿道地铁往返一趟（孩子的第一次）＋ 法师区巫师圣殿（孩子不许进，旅行者单独进）。
5. **黄昏→入夜**｜回要塞王座厅外围远远看一眼"王座上坐的也是个孩子"（呼应），送孩子回院，旅行者住进旅店收束。

---

### 第 4 名｜元宵节：白天挂灯，入夜整点烟花（Lunar Festival，补丁 1.9.0）

| 项 | 内容 |
|---|---|
| **候选名** | 这一天，石头城从早到晚都在为死去的人点灯——到了夜里，每个整点炸一次烟花。 |
| **是什么** | 补丁 1.9.0（2006-01-03）加入。设定原话：`Every year the druids of Moonglade hold a celebration of their city's great triumph over an ancient evil.`；装饰覆盖每座主城 `Decorations are placed in every capital`；灯笼的含义是 `The light from each Festival Lantern honors the soul of an ancestor spirit.`；暴风城入夜后 `Hourly displays after sunset in the city`。暴风城的长者「锤喝长者」**在 Vanilla 时站在暴风城公园内**（4.0.3a 才挪到城外）。 |
| **版本** | ✅ 补丁 1.9.0，Vanilla 后半程全程存在，每年冬末一段时间。 |
| **在哪** | 暴风城公园（长者 + 月亮井 + 暗夜精灵）＋ 全城挂饰 ＋ 夜空烟花 |
| **画面** | 1）清晨的石桥拱门上，人正把一串串红纸灯笼系上去，灯笼还没点；2）公园中心的月亮井泛着幽蓝，盘腿的长者坐在草地上，暗夜精灵在树下；3）一盏被托在掌心的灯笼，烛火映亮持灯人的下巴；4）入夜，整点一到，烟花在蓝色尖顶与运河水面上同时炸开两层光；5）烟花散尽，运河上漂着倒影与几盏没人收的灯笼。 |
| **与逛单八块的关系** | **貌**（白天与夜晚两套城市外观，一集之内拿到两个视觉版本）**娱**（满分）**活**（挂灯、买灯、放烟花都是具体劳作）**事**（有明确的"今天是什么日子"）。**吃** 可搭节庆食摊（⚠️ 设定未写暴风城元宵食摊，需标）；**住／穿／构** 需另找由头。 |
| **风险** | ① 冲突几乎为零，是**最安全**的候选。② 代价也正是"安全"：它没有戏剧转折，全靠观察与讲解撑 15 分钟，对文本密度要求高。③ 视觉上要防"中国现代灯会"味——负向词必须挂 `灯笼上有汉字 / 电灯 / LED / 灯会牌楼`。④ 长者的位置是**本路发现的一个易错点**：很多攻略写他在城外，那是 Cata 之后的事。 |

**作为「当天大事」时这一天怎么排（5 个时间点）：**
1. **清晨**｜城门口，工人正把灯笼串挂上拱门；旅行者进城，问"今天什么日子"。
2. **上午**｜贸易区买一盏灯笼（讲物价）＋ 游客中心 ＋ 狮鹫栖木。
3. **正午**｜矮人区吃饭、看锻炉；矿道地铁往返。
4. **午后**｜暴风城公园：月亮井、长者、暗夜精灵；讲这个节日到底在纪念什么（古代之战）。
5. **入夜**｜要塞外与法师区各一段，最后登上城墙／桥头看整点烟花，对镜收束。

---

### 第 5 名｜爱情降临节 +「危险的爱情」：城里的卫兵是不是被下药了（补丁 1.9.3）

| 项 | 内容 |
|---|---|
| **候选名** | 满城的卫兵头顶都飘着一颗心——银行里有个工匠觉得这事不对劲。 |
| **是什么** | 补丁 1.9.3 加入的节日。设定原话：`many guards and townsfolks now spend their days giving and receiving tokens and gifts to other amorous citizens`。联盟主线「危险的爱情」起点在**暴风城银行**的 Aristan Mottar，主题是调查这场"爱情瘟疫"（`who is behind the love plague`）到底是谁下的手。 |
| **版本** | ✅ 补丁 1.9.3（2006-02-07）。⚠️ 注意：现行版本是补丁 3.3.0 重做过的，**王冠化工公司、情人节首领、礼物大会（Gala of Gifts）全部是后续版本**，不得出现。 |
| **在哪** | 暴风城银行（起点）＋ 全城各处岗哨（卫兵）＋ 旅店（买香水/古龙水） |
| **画面** | 1）站岗的卫兵头顶飘着一颗心的标记，低头接过一支玫瑰，头盔下露出一点尴尬；2）旅店柜台上摆着成排的小玻璃香水瓶与糖果盒；3）银行大堂里，一个系工匠围裙的男人压低声音，背后是柜台与账簿；4）一名市民把信物递给另一名市民，旁边有人起哄；5）傍晚，被送出去的花瓣与空瓶子散在运河石阶上。 |
| **与逛单八块的关系** | **活**（满分——这是整个候选池里"人在干什么"最密集的一个）**构**（银行是没被四个既定机构覆盖的第五个公共设施）**娱**（互赠信物）**吃**（糖果、巧克力）**事**（悬疑线提供推进力）。**貌／住／穿** 需另配。 |
| **风险** | ① 悬疑线的收尾在城外（希尔斯布莱德丘陵的药剂师），要在城内闭环就得改写——必须标 ⚠️。② "下药"题材的平台合规要留意，建议把"爱情瘟疫"处理成滑稽而非投毒犯罪。③ 分量中等：若不叠悬疑线，只剩"满城送花"，撑不满 15 分钟。 |

**作为「当天大事」时这一天怎么排（5 个时间点）：**
1. **清晨**｜进城就看见卫兵头顶飘心，旅行者以为是自己眼花。
2. **上午**｜贸易区与旅店：买香水、看市民互赠；顺势讲物价、旅店与住宿。
3. **正午**｜银行：工匠拉住旅行者，说"卫兵们不对劲"，悬疑线起。
4. **午后**｜借调查之名走完矮人区 / 矿道地铁 / 法师区圣殿（问遍每个机构的人"你今天有没有觉得怪"）。
5. **入夜**｜在王座厅外揭盅（改写为城内闭环），对镜收束这座城平常的样子与今天的样子。

---

## 4. 不可用清单（版本错置 / 与 Vanilla 冲突）

| 条目 | 为什么不可用 | 依据 |
|---|---|---|
| **啤酒节（Brewfest）** | 补丁 2.2.2 加入，燃烧的远征内容 | `stormwind.event.101` 反表 |
| **朝圣者的丰收（Pilgrim's Bounty）** | 补丁 3.2 加入，巫妖王之怒 | 同上 |
| **亡灵节（Day of the Dead）** | 补丁 3.2 加入 | 同上 |
| **海盗日（Pirates' Day）** | 补丁 2.4.3 加入 | 同上 |
| **新年（New Year）** | 补丁 2.0.1 加入 | 同上 |
| **一切微型节日（Micro-Holidays）** | 补丁 7.1.5 / 7.2.5 加入，军团 | 同上 |
| **无头骑士** | 补丁 2.2.2 才加入万圣节 | `.104` |
| **联盟柴垛人（Wickerman）** | 补丁 4.2.0 才加入 | `.104` |
| **仲夏节的日常任务体系与艾胡恩** | 补丁 2.4.0 才加入 | `.107` |
| **爱情降临节的王冠化工公司 / 礼物大会** | 补丁 3.3.0 重做后才有 | `.106` |
| **复活节在暴风城城内找蛋** | Vanilla 只在新手村；3.1.0 才重做 | `.108` |
| **暗月马戏团在暴风城城内 / 暗月岛 / 旋转木马 / 宠物对战** | 4.3.0 才移到暗月岛并重做；Vanilla 在闪金镇外 | `.167` |
| **暴风城港口、码头、大帆船** | 补丁 3.0.2 加入，Vanilla 无港口 | `.161` |
| **暴风城墓园、提芬王后墓、教堂广场旁的湖与凉亭** | 补丁 4.0.3a 加入 | `.162` |
| **教堂广场的乌瑟尔雕像** | 4.0.3a 才替换阿隆索斯·法奥像 | `.163` |
| **巫师圣殿里的一圈常驻传送门（传送门大厅）** | 补丁 8.1.5 才建成 | `.164` |
| **矮人区的拍卖行与银行** | 大地的裂变才加 | `.165` |
| **元素攻打暴风城 / 城内暴雨 / 元素裂隙** | 大地的裂变 4.0.3a 前夕事件 | `.166` |
| **Vanilla 元素入侵打进城市** | 1.4.0 的元素入侵只在卡利姆多四个野外区域 | `.131` |
| **哈蒙德·克雷将军** | Cata 后才接任；Vanilla 是马库斯·乔纳森 | `.154` |
| **暴风城设有安其拉战争物资缴纳点** | 联盟缴纳 NPC 全在铁炉堡军事区 | `.122` |
| **瓦里安·乌瑞恩在城里 / 坐在王座上** | Year 25 ADP 时国王失踪，摄政是博瓦尔，王座上是孩童安度因 | `.136` `.137` `.138` |
| **暴风城在天灾入侵里由瓦里安与博瓦尔共同指挥、冰霜巨龙掠城** | 那是补丁 3.0.2（巫妖王之怒）版本的暴风城攻防，不是 1.11 | Warcraft Wiki《Scourge Invasion (Stormwind)》——该页描述的是 WotLK 版本 |

---

## 5. 未查 / Open questions

1. **暴风城有没有"钟声/报时/开市闭市/宵禁/卫兵换岗"的任何设定文本？** 穷尽查了 `Stormwind City` / `Stormwind City Guard` / `Trade District` / `Old Town` 四页，**没有任何一条**。本路结论：除元宵节整点烟花外，Vanilla 暴风城**没有任何设定明载的时间刻度**。若节目需要"一天的节奏感"，只能自己造并标 ⚠️。

2. **Vanilla 暴风城有没有处决 / 公开审判 / 押送囚犯的设定？** 未查到。监狱（暴风城监狱）本身归已交付候选 ①，但"押送/审判/处决"这条线在 warcraft.wiki.gg 上没有可引用的 Vanilla 文本。建议：要用就当 ⚠️ 推演，或并入候选 ①。

3. **教堂广场的"市政厅（City Hall）"与贸易区的"游客中心"是同一个还是两个机构？** 两页说法并存（`Cathedral Square` 说市政厅在教堂广场；`Stormwind Visitor's Center` 说公会业务在贸易区）。本路未能判定 Vanilla 时"市政厅"这栋楼里到底办什么，**已标 ⚠️（`.143`）**。建议由 W1（城市布局）路交叉核对。

4. **教堂广场的"银色黎明"驻地在 Vanilla 就存在吗？** 该页没有 Patch changes 段，唯一的出处是 RPG 设定书《Dark Factions》。本路标 ⚠️，未定论。若要在片中出现银色黎明的常设据点，风险自负；但**天灾入侵期间的临时帐篷是 ✅ 有据的**。

5. **Vanilla 暴风城的节庆食摊 / 节日限定食物** 只查到万圣节的糖果贩（Bellara's Nutterbar、Styleen's Sour Suckerpop）与冬幕节哥布林礼盒摊。元宵节、仲夏节在暴风城有没有食摊，**未查到**。

6. **来源损失记录**：`*.fandom.com` 在本环境可访问但内容与 `warcraft.wiki.gg` 重复，故未深挖；`warcraft.huijiwiki.com`（中文）**全程未尝试**，所有中文译名均为本路按通行简中译法给出，**未经官方简中客户端核对**——`锤喝长者` / `杜加·长饮` / `雪落元帅` / `苍白恐魔` / `缝合恐魔` / `炽燃者` 六个译名建议由后续路核对官方简中。Wowhead Classic 的 `wow-classic-childrens-week-holiday` 与 `wow-classic-hallows-end-holiday-event` 两页为 JS 渲染，正文抓不到，已改用 Warcraft Tavern 的 Classic 指南替代（T2）。

7. **本路未覆盖**：矿道地铁本体（归 W7）、物价与经济（归 W4）、衣着（归 W3）、人物与称谓（归 W5）、日常禁忌黑名单（归 W6）。候选表中凡涉及这些的格子只给指向，不给结论。
