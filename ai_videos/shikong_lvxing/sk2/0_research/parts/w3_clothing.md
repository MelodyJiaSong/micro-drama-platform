---
worker_id: researcher-w3-clothing
stage: 0
role: researcher
angle: clothing
status: complete
blockers: []
confidence: medium
facts_total: 97
facts_ai_read: 81
facts_ai_draft: 16
facts_tag_ok: 75
facts_tag_warn: 19
facts_tag_bad: 3
version_anchor: Vanilla / WoW Classic 1.x（大地的裂变之前）
run: sk2-20260918-130201
---

# W3 · 衣：暴风城各阶层装束（Vanilla 锚点 · 半写实画风）

> 供 `0_research/dossier.md` §「衣」合并。
> **版本锚点＝经典旧世（WoW 1.x / Classic）**，后续资料片才有的装束一律进 §版本错置清单。
> **画风＝半写实**：形制与配色忠于游戏，材质与皮肤走写实电影级。
> **当地人零台词** → 长相与装束就是全部表演，下面 §锁定串总表 是本路最重要的产物。
> 色名一律零 hex。锁定串模板：`{形制名词}（{材质}，{色名}，{2–3 处关键结构}），{穿着方式}；不是 {最常见误画法}`。

## 本路的 tier 诚实声明（必读）

- 本轮**没有 T0**：我无法运行 Classic 客户端、无法打开 Wowhead Modelviewer 的 3D 视图（页面靠 JS 渲染，抓取只拿到文字壳）。
- 因此**「形制骨架」有据（T1 wiki 带游戏内/小说引用），「针脚级细节」多为 ⚠️ 推定**——尤其是
  **卫兵头盔有没有面甲、平民上衣的领口与系法、贵族华服的裁剪**这三处，文字来源全网都没写。
- 这三处已进 §未查 / Open questions，并在 §参考图候选表 里给出**人眼必须去开的 Modelviewer / 截图 URL**。
- 标 `ai_draft` 的条目**不得直接进 shot prompt**，须人眼核过模型后改 `human`。

---

## 0. 总纲：城中都有谁 · 纹章 · 材质分档（贯穿全部 9 套）

```yaml
- fact_id: stormwind.dress.001
  claim: 暴风城同时住着人类、大量矮人、侏儒、高等精灵与暗夜精灵等多个种族——街上装束必须同时出现 4–5 种体型，不能全是人类
  tag: ✅
  source: Warcraft Wiki「Stormwind City」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "humans, many dwarves, gnomes, high elves, and night elves and other races"
  tier: T1
  verified_by: ai_read
  used_in: [街景群像]
  prompt_string: "街上同框出现四种体型：人类成年人、约及人类胸口的矮人、约及人类腰际的侏儒、高出人类一头半的暗夜精灵；比例差一眼可辨"
  negative: "全部同一身高, 只有人类, 体型统一, 缩小版人类当矮人"

- fact_id: stormwind.dress.002
  claim: 城里绝大多数人是平民——农人、店主、酒馆老板、普通工匠；打马蹄铁与铁锅的乡村铁匠也算平民
  tag: ✅
  source: Warcraft Wiki「Commoner」（RPG 段）
  source_url: https://warcraft.wiki.gg/wiki/Commoner
  quote: "Most citizens are commoners. They are farmers, shopkeepers, tavern owners, and simple craftsmen."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_m, commoner_f]
  prompt_string: "平民衣着以劳动功能为先：耐磨、可卷袖、腰上挂得住工具，没有一处装饰性垂坠"
  negative: "华服, 珠宝, 拖地长摆, 宫廷礼服, 一尘不染"

- fact_id: stormwind.dress.003
  claim: 暴风城的纹章是「蓝底金狮」——一面巨大的蓝色旗帜上绣着金色狮子即代表暴风王国
  tag: ✅
  source: Warcraft Wiki「Hall of Justice」
  source_url: https://warcraft.wiki.gg/wiki/Hall_of_Justice
  quote: "A large blue banner embroidered with a golden lion signified the kingdom of Stormwind. Another banner, black with a red-gauntleted fist, represented the kingdom of Stromgarde."
  tier: T1
  verified_by: ai_read
  used_in: [guard, royal_guard, 街景]
  prompt_string: "暴风城纹章＝群青蓝底上一头金黄色狮子；凡罩袍、盾面、旗帜出现纹章，一律这一组配色"
  negative: "红底, 黑底, 银狮, 双头鹰, 十字, 红底金狮, 白底蓝狮"

- fact_id: stormwind.dress.004
  claim: 金色狮首象征人类的勇气与坚韧，代表暴风王国；暴风城地图图标用的就是这颗狮首
  tag: ✅
  source: Warcraft Wiki「Icon of Courage」
  source_url: https://warcraft.wiki.gg/wiki/Icon_of_Courage
  quote: "a shield emblazoned with the symbol of the fallen Kingdom of Lordaeron over a pair of crossed swords and a warhammer accented with a golden lion's head."
  tier: T1
  verified_by: ai_read
  used_in: [guard, royal_guard]
  prompt_string: "纹章主体是一颗正面狮首（金黄，鬃毛呈放射状分瓣，双耳外张），不是全身狮、不是行走狮"
  negative: "全身狮子, 侧面行走狮, 站立狮, 狮子抱盾, 卡通狮"

- fact_id: stormwind.dress.005
  claim: 旧城区是穷人住区，街道比其他区「更脏更臭」，乞丐、窃贼与贫民聚集
  tag: ✅
  source: Warcraft Wiki「Old Town」
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "It is a rustic, downtrodden place, where the streets are described as far dirtier and smellier than the other districts."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_m, commoner_f, si7]
  prompt_string: "旧城区的人衣服更旧：下摆与袖口磨白起毛、有补丁、鞋面沾泥、颜色被洗到发灰"
  negative: "崭新衣料, 鲜亮颜色, 熨平褶线, 干净白鞋"

- fact_id: stormwind.dress.006
  claim: 贸易区紧挨城门，是城中买卖枢纽，沿街与运河边有面包铺、军械铺、药剂铺、奶酪铺、花铺、酒庄、裁缝铺与珠宝匠
  tag: ✅
  source: Warcraft Wiki「Trade District」
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "It is the place in the city where you can get most goods."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_m, commoner_f]
  prompt_string: "贸易区商贩衣着比旧城区整洁一档：同样是劳动装，但料子完好、围裙干净、袖口卷得齐整"
  negative: "破烂乞丐装, 贵族华服, 制服化统一店服"

- fact_id: stormwind.dress.007
  claim: 拍卖行是 1.9 补丁才加进贸易区中心的——Vanilla 早期贸易区中心没有拍卖行建筑
  tag: ✅
  source: Warcraft Wiki「Trade District」
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "Patch 1.9 added the linked Auction House in the center of the Trade District."
  tier: T1
  verified_by: ai_read
  used_in: [街景]
  prompt_string: "（时序提示）本站若设定在 1.x 中后期，贸易区中心可有拍卖行人群；设定在开服初期则没有"
  negative: ""

- fact_id: stormwind.dress.008
  claim: 装甲分四档（布 / 皮 / 锁 / 板）是暴雪的职业体系设定，可直接当街上的阶层可视化分档
  tag: ⚠️
  source: 由 Warcraft Wiki 各职业页 "Armor type" 字段归纳（法师=Cloth、潜行者=Leather、德鲁伊=Cloth+Leather、战士=Plate）
  source_url: https://warcraft.wiki.gg/wiki/Mage
  quote: "Armor type: Cloth"
  tier: T1
  verified_by: ai_draft
  used_in: [全部]
  prompt_string: "镜头里一眼分档：布（法师/牧师/平民）→ 皮（潜行者/德鲁伊/工匠围裙）→ 板（卫兵/皇家卫队/圣骑士）；三档反光完全不同——布不反光、皮半哑光、板有清晰高光带"
  negative: "所有人材质一样, 布衣有金属高光, 板甲像塑料"
```

---

## 1. 暴风城卫兵 Stormwind City Guard（城市卫兵档）

```yaml
- fact_id: stormwind.dress.010
  claim: 所有卫兵穿的装备与罩袍，与暴风城军队的士兵完全相同——卫兵不是独立制服，是军服
  tag: ✅
  source: Warcraft Wiki「Stormwind City Guard」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_City_Guard&action=raw
  quote: "All guards wear the same gear and tabard as the soldiers of the [[Stormwind Army]]."
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "卫兵＝军人装束：板甲外罩军用纹章罩袍，不是另设一套「警察制服」"
  negative: "警服, 治安员皮马甲, 便装配袖章, 巡逻背心"

- fact_id: stormwind.dress.011
  claim: 卫兵可见的装备包括：剑、盾、弩、捕网，以及夜间提的油灯
  tag: ✅
  source: Warcraft Wiki「Stormwind City Guard」（原始 wikitext，引 Stormwind City Patroller#Abilities）
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_City_Guard&action=raw
  quote: "In terms of equipment, they can be seen employing swords, shields, crossbows, catch nets, and oil lamps at night."
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "白天：右手单手直剑、左手鸢形盾；夜间：一手提铜壳油灯（灯焰暖橙、只照亮身前一小片）、另一手扶剑柄；抓贼分队另配木柄弩与折叠捕网"
  negative: "长戟, 火把, 电筒, 现代手铐, 火枪, 纸灯笼"

- fact_id: stormwind.dress.012
  claim: 部分卫兵受过狮鹫骑手训练，以小队形式骑白色狮鹫在空中执勤
  tag: ✅
  source: Warcraft Wiki「Stormwind City Guard」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Stormwind_City_Guard&action=raw
  quote: "some guards are expertly trained as [[gryphon rider]]s and can be seen working in squads on their white [[gryphon]]s."
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "空中巡逻的卫兵骑白色狮鹫（白羽头颈、狮身后躯），成小队掠过屋顶线；地面卫兵抬头时视线跟着它们走"
  negative: "黑色狮鹫, 龙, 飞马, 单骑独行, 天上骑马"

- fact_id: stormwind.dress.013
  claim: 卫兵在地面与空中巡逻、或守在首都城门，并在需要时协助与保护市民
  tag: ✅
  source: Warcraft Wiki「Stormwind City Guard」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard
  quote: "They are patrolling on the ground and in the sky, or guarding the capital's gates, while assisting and protecting the citizens when needed."
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "站姿两种：城门口双人对称立定（双手叠按剑柄或盾沿、重心平均）／街上两人并行慢巡（步幅一致、头随人流转）"
  negative: "东倒西歪, 靠墙抽烟, 交头接耳嬉闹, 追着人跑"

- fact_id: stormwind.dress.014
  claim: Vanilla 时期暴风城卫兵是 55 级人类战士（2.0.1 才提到 65 级）
  tag: ✅
  source: Warcraft Wiki「Stormwind City Guard (NPC)」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
  quote: "Classic/Vanilla level: 55 (raised to 65 in Patch 2.0.1)"
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "卫兵是职业军人体格：肩宽、上臂与颈部有厚度，不是瘦削少年"
  negative: "少年兵, 瘦弱体型, 大肚子滑稽卫兵"

- fact_id: stormwind.dress.015
  claim: 卫兵制服自 Vanilla 起就是「经典钢制板甲＋蓝色点缀＋绘有暴风城狮子的盾＋标志性板盔」
  tag: ✅
  source: Engadget《Transmogrifying your way into the Stormwind Guard》（2012-01-05，美术考据栏目）
  source_url: https://www.engadget.com/2012-01-05-transmogrifying-your-way-into-the-stormwind-guard.html
  quote: "The uniform of the Stormwind guard is an iconic look that's been around since vanilla — classic steel plate armor with blue accents, a shield emblazoned with the Stormwind lion, and the iconic plate helm all make up the look of the Stormwind guard."
  tier: T2
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "全身锻钢板甲（抛光钢灰，胸甲一整片弧面带中脊、肩甲双层叠片、护臂与护胫分段铆接），关节缝处露深灰锁环；蓝色只作点缀，不是整身蓝"
  negative: "整身涂蓝, 镀金浮雕重甲, 银白发光铠甲, 锁子甲为主, 皮甲, 布衣"

- fact_id: stormwind.dress.016
  claim: 暴雪官方出的 Stormwind Set 明载「是暴风城卫兵所穿铠甲的复制品」，套装含 Stormwind Shield 与 Stormwind Tabard
  tag: ✅
  source: Warcraft Wiki「Stormwind Set」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Set
  quote: "It is a replica of the armor worn by Stormwind Guards."
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "卫兵一身＝头盔＋肩甲＋胸甲＋手甲＋腰带＋腿甲＋战靴 七件板甲，外加盾与罩袍两件纹章件"
  negative: "缺件露布衣, 只有胸甲没有腿甲, 裸露小腿"

- fact_id: stormwind.dress.017
  claim: 暴风城罩袍由贸易区的 Captain Lancy Revshon〈暴风城军需官〉出售
  tag: ✅
  source: Warcraft Wiki「Stormwind Tabard」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Tabard
  quote: "The tabard can be purchased from Captain Lancy Revshon, the Stormwind Quartermaster, located in the Trade District of Stormwind City for 10 silver at friendly reputation status with Stormwind."
  tier: T1
  verified_by: ai_read
  used_in: [guard, 街景]
  prompt_string: "（可入镜细节）贸易区有一名披同款罩袍的军需官坐在摊后，面前摞着叠好的罩袍"
  negative: ""

- fact_id: stormwind.dress.018
  claim: 卫兵罩袍＝群青蓝底、正中金黄狮首，穿在板甲之外
  tag: ⚠️
  source: 由 003「纹章＝蓝底金狮」＋ 010「卫兵穿军队罩袍」＋ 015「盾上绘暴风城狮子」三条交叉推得；无单一原文页直接描述罩袍配色
  source_url: https://warcraft.wiki.gg/wiki/Hall_of_Justice
  quote: "A large blue banner embroidered with a golden lion signified the kingdom of Stormwind."
  tier: T1
  verified_by: ai_draft
  used_in: [guard, royal_guard]
  prompt_string: "过膝罩袍（厚织呢，群青蓝底，正中一颗金黄狮首，两侧开衩至腰、下摆平直），套头穿在板甲外、腰间用皮带束住；不是围裙式只挡前身"
  negative: "红色罩袍, 白底红十字, 素色无纹章罩袍, 披风代替罩袍, 罩袍穿在甲内"

- fact_id: stormwind.dress.019
  claim: 卫兵头盔的具体形制（是否全覆面、有无面甲/观察缝、有无羽饰）——全网文字来源均无描述
  tag: ⚠️
  source: 未查到原文；Engadget 仅称 "the iconic plate helm"，Warcraft Wiki 卫兵页无头盔描述
  source_url: https://www.engadget.com/2012-01-05-transmogrifying-your-way-into-the-stormwind-guard.html
  quote: "the iconic plate helm"
  tier: T2
  verified_by: ai_draft
  used_in: [guard]
  prompt_string: "（待人眼核模型后定稿）钢灰色全覆式板盔，盔顶一道纵向脊，前脸只留一条横向观察缝与数排呼吸孔，无羽饰无角"
  negative: "羽毛顶饰, 牛角盔, 敞开式头巾, 现代警帽, 十字形面甲, 龙翼装饰"
  note: 本条是本路第一优先待核项；进 shot prompt 前必须开 Modelviewer 核过并改 human

- fact_id: stormwind.dress.020
  claim: 部分卫兵不戴头盔巡逻（露脸）
  tag: ✅
  source: Warcraft Wiki「Stormwind Guard collection」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Guard_collection
  quote: "Some guards patrol without helmets."
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "同一队里允许一名卫兵不戴盔、露出短发与短须的人类男性面孔——给镜头一张可读的脸"
  negative: "全队一律戴盔面目全无, 摘盔夹在腋下走路"

- fact_id: stormwind.dress.021
  claim: 卫兵不披斗篷——官方复刻指南明确要求关掉披风，因为卫兵不穿
  tag: ✅
  source: Warcraft Wiki「Stormwind Guard collection」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Guard_collection
  quote: "instructs players to disable capes since guards don't wear them"
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "卫兵背后是空的：无披风、无斗篷、无背旗"
  negative: "红披风, 长斗篷, 背后插旗, 飘带"

- fact_id: stormwind.dress.022
  claim: 卫兵 NPC 实际佩戴的肩甲是玩家拿不到的专属模型——肩甲造型不同于任何一件玩家装备
  tag: ✅
  source: Warcraft Wiki「Stormwind Guard collection」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Guard_collection
  quote: "the exact shoulders worn by NPCs are not available to players"
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "肩甲是专属造型：双层弧形叠片，外沿略微上翘，表面素净无浮雕兽首"
  negative: "尖刺肩甲, 兽首浮雕肩甲, 巨型夸张肩铠, 翼形肩甲"
  note: 反过来说——拿玩家装备（Imperial Plate Shoulders）反推 NPC 肩甲是错的

- fact_id: stormwind.dress.023
  claim: 人类步兵的标准形象是「一身硬化钢铠，手持阔剑与盾牌」；各人类王国的步兵铠甲按本国颜色配色
  tag: ✅
  source: Warcraft Wiki「Footman」
  source_url: https://warcraft.wiki.gg/wiki/Footman
  quote: "Clad in armor of hardened steel, they wield broadsword and shield in pitched hand-to-hand combat."
  tier: T1
  verified_by: ai_read
  used_in: [guard]
  prompt_string: "剑是宽刃直身阔剑（钢灰刃、十字护手、圆盘柄首），盾是鸢形盾（上缘平、下收尖，群青蓝底金黄狮首）"
  negative: "细剑, 弯刀, 武士刀, 圆盾, 方盾, 双手巨剑"

- fact_id: stormwind.dress.024
  claim: RPG 资料书称「城卫兵通常只穿轻甲，用以应付偶发的窃贼与匪徒」——与游戏内板甲模型直接冲突
  tag: ❌
  source: Warcraft Wiki「Stormwind City」引 RPG 段
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The city guard usually wears only light armor to handle the occasional thief or bandit."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "轻甲卫兵, 皮甲卫兵, 布面巡逻服"
  note: >
    冲突判定（按 ai_video.md rule 4i ②「先问是不是同一个东西」）：这是真冲突，不是伪冲突——RPG 线（T2 纸面设定）
    与游戏本体（T0 模型）说的是同一批人。判据＝本项目锚点是游戏本体（半写实复刻游戏形象，不是复刻 RPG 书），
    故游戏内板甲胜。RPG 这句只作反面词来源，不进任何 prompt。
```

---

## 1b. 皇家卫队 Stormwind Royal Guard（王宫档，与城市卫兵分列）

```yaml
- fact_id: stormwind.dress.025
  claim: 皇家卫队是与「暴风城城市卫兵」并列的独立编制，隶属暴风城军队，专责守卫王室与要塞
  tag: ✅
  source: Warcraft Wiki「Stormwind City Guard」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard
  quote: "The article distinguishes the Stormwind City Guard from the Stormwind Royal Guard, which is listed as a separate military organization under the Stormwind Army."
  tier: T1
  verified_by: ai_read
  used_in: [royal_guard]
  prompt_string: "皇家卫队与街头卫兵是两档：同源纹章、同为板甲，但皇家卫队只出现在要塞台阶与王座厅内外，从不在市集游走"
  negative: "皇家卫队在菜市场巡逻, 与街头卫兵混编"

- fact_id: stormwind.dress.026
  claim: 皇家卫队 NPC 在 1.4.0 补丁（2005-04-19）加入，是人类战士，Vanilla 为 60 级精英，位于暴风要塞内外
  tag: ✅
  source: Warcraft Wiki「Stormwind Royal Guard (NPC)」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Royal_Guard_(NPC)
  quote: "Added in Patch 1.4.0 (2005-04-19)"
  tier: T1
  verified_by: ai_read
  used_in: [royal_guard]
  prompt_string: "皇家卫队站位永远成对、面朝门道中线、纹丝不动；体格比街头卫兵更壮一档"
  negative: "走动巡逻, 随意站姿, 闲聊"

- fact_id: stormwind.dress.027
  claim: 皇家卫队的女性模型是 4.0.3a（2010-11-23，大灾变前夕）才加入的、同时改了铠甲——Vanilla 的皇家卫队清一色男性
  tag: ✅
  source: Warcraft Wiki「Stormwind Royal Guard (NPC)」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Royal_Guard_(NPC)
  quote: "a female model was added in Patch 4.0.3a with armor changes"
  tier: T1
  verified_by: ai_read
  used_in: [royal_guard, guard]
  prompt_string: "（版本闸门）Vanilla 镜头里的卫兵与皇家卫队全为男性；要表现女性从军只能放在冒险者/民兵而非卫兵岗"
  negative: "女性卫兵, 女性皇家卫队"
  note: 4.0.3a 同时改了铠甲——所以任何「大灾变之后的皇家卫队铠甲」图都不能当 Vanilla 参考

- fact_id: stormwind.dress.028
  claim: 暴风要塞内除皇家卫队外，还有相当数量的 SI:7 特工，假扮成小贵族或王室仆从
  tag: ✅
  source: Warcraft Wiki「Stormwind Keep」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "a considerable number of agents from SI:7 intelligence who posing as lesser noblemen or servants to the crown"
  tier: T1
  verified_by: ai_read
  used_in: [royal_guard, noble, si7]
  prompt_string: "（可入镜细节）王宫厅内的「小贵族」里混着眼神过分警觉的一两位——衣服是贵族的，站位是哨兵的"
  negative: "明着穿潜行者皮甲站在王宫大厅"

- fact_id: stormwind.dress.029
  claim: 皇家卫队装束＝城市卫兵同源板甲的加强档，但**具体差异点未查到任何原文**
  tag: ⚠️
  source: 无原文页；Wowhead 上的 "Stormwind Royal Guard" outfit（TBC/正式服）均为玩家自建 transmog 复刻，非游戏数据
  source_url: https://www.wowhead.com/tbc/outfit=221485/stormwind-royal-guard
  quote: "Head: Savage Gladiator Helm / Shoulder: Imperial Plate Shoulders / Chest: Imperial Plate Chest / Tabard: Knight's Colors"
  tier: T4
  verified_by: ai_draft
  used_in: [royal_guard]
  prompt_string: "（待核）与城市卫兵同一套群青蓝金狮罩袍与钢灰板甲，差别在：甲面更少战损、罩袍更长至小腿、一律戴盔不露脸"
  negative: "金甲, 红罩袍, 华丽羽饰, 与街头卫兵完全同款无差别"
  note: 玩家 transmog 只作构图旁证，不得当形制依据（T4）
```

---

## 2. 平民男性（商贩 / 工匠 / 搬运工 / 农人）

```yaml
- fact_id: stormwind.dress.030
  claim: 人类男性平均身高约 6 英尺 1 英寸（部分可达 6 英尺 6 英寸）；男性常蓄短须
  tag: ✅
  source: Warcraft Wiki「Human」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Human&action=raw
  quote: "Female humans are on average 5'8\" tall while males usually reach a height of about 6'1\", however, some males do reach heights of 6'6\"." / "Men often grow short beards and women commonly wear their hair long."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_m]
  prompt_string: "人类成年男性：身高约一米八五，蓄修剪过的短须（不是大胡子也不是净面）、短发"
  negative: "及胸长须, 光头, 长发飘飘, 现代寸头渐变, 童颜"

- fact_id: stormwind.dress.031
  claim: 人类的瞳色为蓝 / 棕 / 绿 / 灰 / 榛，发色为棕 / 黑 / 金 / 红，肤色从浅粉到晒褐到深褐
  tag: ✅
  source: Warcraft Wiki「Human」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Human&action=raw
  quote: "Their eyes are blue, brown, green, gray, or hazel." / "Human hair is brown, black, blond, or red." / "The color and hue of human skin vary, ranging from a fair pink, to tanned, to a very dark brown."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_m, commoner_f, noble]
  prompt_string: "群像肤色要拉开：浅粉、晒成小麦色、深褐三档同框；瞳色限蓝棕绿灰榛，发色限棕黑金红"
  negative: "紫色头发, 荧光发色, 蓝皮肤, 全员同一肤色, 动漫色瞳"

- fact_id: stormwind.dress.032
  claim: 平民男性装束的形制细节（上衣领口、系带方式、裤型、围裙裁剪）——各来源均无文字描述
  tag: ⚠️
  source: 未查到；Warcraft Wiki「Human」页只描述军装（板甲步兵、重甲骑士），无平民服饰段；「Commoner」页只写职业不写形制
  source_url: https://warcraft.wiki.gg/index.php?title=Human&action=raw
  quote: "Well-trained footmen march to battle in plate armor with kite shields and broadswords, while courageous knights covered in heavy plate mail ride headlong into battle"
  tier: T1
  verified_by: ai_draft
  used_in: [commoner_m]
  prompt_string: "（待人眼核模型后定稿）中世纪欧式平民男装：粗纺束腰长衫（麻褐或本白，开襟到胸口用两三根系带、袖口可卷到小臂），下配深褐粗布长裤，小腿缠布带，脚穿翻口皮靴"
  negative: "中式盘扣, 和服, 现代衬衫领, 牛仔裤, 拉链, 印花图案, 露腹肌背心"
  note: 本条是本路第二优先待核项

- fact_id: stormwind.dress.033
  claim: 铁匠 / 工匠一档以皮围裙作职业标记（由「乡村铁匠打马蹄铁与铁锅也算平民」＋矮人区的露天锻造场景推得）
  tag: ⚠️
  source: Warcraft Wiki「Commoner」＋「Stormwind City」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "blacksmiths create masterpieces out of common metals in many open-air plazas"
  tier: T1
  verified_by: ai_draft
  used_in: [commoner_m, dwarf_smith]
  prompt_string: "铁匠：厚牛皮围裙（深棕，胸口一道横向加厚带、两条肩带在背后交叉、下摆过膝），围裙面上有暗色火星灼痕与锤击压光；袖子卷到肘上、小臂裸露带汗光"
  negative: "布围裙, 厨师白围裙, 塑料围裙, 干净无痕围裙, 长袖不卷"

- fact_id: stormwind.dress.034
  claim: 「码头工」在 Vanilla 不成立——暴风城海港是 3.0.2（2008-10-14，巫妖王之怒前夕）才加的
  tag: ❌
  source: Warcraft Wiki「Stormwind Harbor」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Harbor
  quote: "Patch 3.0.2 (2008-10-14): Added."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_m]
  prompt_string: "（改写）Vanilla 没有海港，「搬运工」一档改设在贸易区运河边的驳船与货栈：肩扛麻袋、腰缠护腰布带、赤裸上臂"
  negative: "海港, 远洋帆船, 栈桥, 水手, 船坞, 灯塔"
```

---

## 3. 平民女性（女摊主 / 女侍 / 织工）

```yaml
- fact_id: stormwind.dress.035
  claim: 人类女性平均身高约 5 英尺 8 英寸；女性通常留长发
  tag: ✅
  source: Warcraft Wiki「Human」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Human&action=raw
  quote: "Female humans are on average 5'8\" tall" / "women commonly wear their hair long."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_f]
  prompt_string: "人类成年女性：身高约一米七三，长发（干活时在脑后挽成一个低髻或编成一条粗辫搭在肩前）"
  negative: "短发波波头, 现代高马尾, 披散长发下厨, 精致盘发配发簪"

- fact_id: stormwind.dress.036
  claim: 贸易区当街有花铺、奶酪铺、酒庄、裁缝铺——女摊主一档有明确职业落点
  tag: ✅
  source: Warcraft Wiki「Trade District」
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "Along the canals are additional shops: the Canal Tailor and Fit Shop, Denman Family Jewelers, Fragrant Flowers, and Gallina Winery."
  tier: T1
  verified_by: ai_read
  used_in: [commoner_f]
  prompt_string: "女摊主站在自己的摊后（花摊／奶酪摊／酒摊），双手在摊面上整理货物，不是空手站着"
  negative: "两手空空干站, 靠墙玩手部动作, 摊面空无一物"

- fact_id: stormwind.dress.037
  claim: 贸易区的面包师 Thomas Miller 是具名平民 NPC——「面点／作坊」一档可直接落地
  tag: ✅
  source: Warcraft Wiki「Trade District」
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The district bustles with various NPCs including Thomas Miller (baker), Officer Brady, Officer Jaxon, Captain Lancy Revshon, and Melris Malagan (Captain of the Guard)"
  tier: T1
  verified_by: ai_read
  used_in: [commoner_m, commoner_f]
  prompt_string: "（可入镜细节）面包铺门口的木案上摊着面粉，手上与前襟沾着白粉"
  negative: "现代烘焙托盘, 纸包装, 玻璃橱窗"

- fact_id: stormwind.dress.038
  claim: 平民女性装束的形制细节（裙型、腰线高低、围裙系法、头巾有无）——各来源均无文字描述
  tag: ⚠️
  source: 未查到；Warcraft Wiki 无人类女性平民服饰段
  source_url: https://warcraft.wiki.gg/wiki/Commoner
  quote: "commoners will usually be dressed in traditional attire for whichever event is going on."
  tier: T3
  verified_by: ai_draft
  used_in: [commoner_f]
  prompt_string: "（待人眼核模型后定稿）中世纪欧式平民女装：长袖束腰连身长裙（粗纺，暗酒红或苔绿或麻褐，圆领、腰间一条编绳束带、裙摆及踝），外系本白粗麻围裙（腰后打结、两侧无褶）；头上系一方素色头巾包住发际"
  negative: "中式襦裙, 和服, 束胸紧身胸衣, 露肩, 蕾丝, 蓬蓬裙, 短裙, 高跟鞋, 印花布"
  note: 本条与 032 同属第二优先待核项

- fact_id: stormwind.dress.039
  claim: 旧城区的女性平民与贸易区的应有可见差别（衣旧、料糙、颜色被洗灰）
  tag: ⚠️
  source: 由 005「旧城区更脏更臭、贫民聚集」推得
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "It is a rustic, downtrodden place, where the streets are described as far dirtier and smellier than the other districts."
  tier: T1
  verified_by: ai_draft
  used_in: [commoner_f]
  prompt_string: "旧城区女性：同款长裙但布面起球、肘部与裙摆有补丁（补丁色与底色不同，一眼看得出是后补的）、围裙边缘磨成毛边、赤脚或穿开裂的布鞋"
  negative: "崭新裙装, 鲜艳色, 干净围裙, 皮鞋"
```

---

## 4. 贵族 / 廷臣

```yaml
- fact_id: stormwind.dress.040
  claim: 暴风城贵族是王国的统治阶级；其中最有影响力的组成「贵族院」，是王室顾问，因为自己拥有大量土地而对商业与劳工有重大影响力
  tag: ✅
  source: Warcraft Wiki「Nobles of Stormwind」
  source_url: https://warcraft.wiki.gg/wiki/Nobles_of_Stormwind
  quote: "The nobles of Stormwind are the aristocratic ruling class of the kingdom of Stormwind." / "Members of the House of Nobles" have "major leverage over business and labor, due to the fact that they own much of the land themselves."
  tier: T1
  verified_by: ai_read
  used_in: [noble]
  prompt_string: "贵族的身体语言是「拥有」：下巴微抬、肩线放平、手背在身后或一手搭在腰带扣上，走路慢半拍"
  negative: "点头哈腰, 小跑, 东张西望, 扛东西"

- fact_id: stormwind.dress.041
  claim: 具名贵族头衔包括伯爵（Count / Countess）、领主（Lord）、男爵（Baron）——是欧式封建头衔体系，不是东方爵位
  tag: ✅
  source: Warcraft Wiki「Nobles of Stormwind」
  source_url: https://warcraft.wiki.gg/wiki/Nobles_of_Stormwind
  quote: "Count Clessington / Countess Cecilia Clessington, Count Erlgadin, Count Remington Ridgewell, Lord Joran Tremaind, Lord Ello Ebonlocke, Lord Bolvar Fordragon, Baron Freeman"
  tier: T1
  verified_by: ai_read
  used_in: [noble]
  prompt_string: "贵族配饰走欧式封建路线：宽皮腰带配方形金属带扣、手指一枚印章戒、胸前一枚固定披肩的圆形胸针"
  negative: "玉佩, 朝珠, 乌纱帽, 官袍补子, 权杖, 皇冠"

- fact_id: stormwind.dress.042
  claim: 暴风要塞内部有王座厅、战情室、带王室图书馆的花园、请愿厅、宴会厅与箭术训练室——廷臣的活动场所有明确落点
  tag: ✅
  source: Warcraft Wiki「Stormwind Keep」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "The keep contains several key areas including a throne room, war room, garden with royal library, petitioner's chamber, dining hall, archery training room, and dirigible mooring."
  tier: T1
  verified_by: ai_read
  used_in: [noble]
  prompt_string: "廷臣出现在王座厅两侧与请愿厅：三两成组站着低声交谈，手上拿卷轴或酒杯，不与镜头对视"
  negative: "跪拜, 列队站军姿, 大声喧哗, 打斗"

- fact_id: stormwind.dress.043
  claim: Vanilla 时期瓦里安·乌瑞恩失踪，博瓦尔·弗塔根摄政，安度因还是孩子——王宫群像的构成与后期资料片完全不同
  tag: ✅
  source: Warcraft Wiki「Stormwind Keep」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "With Varian Wrynn absent, Bolvar Fordragon served as regent." / "young Anduin Wrynn, who was still a child at that time"
  tier: T1
  verified_by: ai_read
  used_in: [noble, royal_guard]
  prompt_string: "（版本闸门）王座上没有蓄须的成年国王；台前是一位穿板甲的摄政领主与一个孩子"
  negative: "瓦里安坐在王座上, 成年安度因, 白袍国王"

- fact_id: stormwind.dress.044
  claim: 贵族华服的具体形制（外袍长度、内衬、袖型、配色）——各来源均无文字描述
  tag: ⚠️
  source: Warcraft Wiki「Nobles of Stormwind」明确没有服饰段
  source_url: https://warcraft.wiki.gg/wiki/Nobles_of_Stormwind
  quote: "The wiki contains no specific descriptions of noble clothing, finery, or physical appearance."
  tier: T1
  verified_by: ai_draft
  used_in: [noble]
  prompt_string: "（待人眼核模型后定稿）齐膝开襟外袍（厚天鹅绒，深群青或暗酒红，前襟与袖口一道金黄织锦滚边、下摆分前后两片），内穿本白细麻高领内衫，腰束宽皮带配方形金属带扣，下配深色贴腿裤与及踝软皮短靴"
  negative: "中式长袍马褂, 和服, 燕尾服, 现代西装, 王冠, 全身金甲, 拖地斗篷, 蕾丝领巾"
  note: 本条是本路第三优先待核项
```

---

## 5. 圣光教会神职（大教堂的牧师 / 主教 / 大主教）

```yaml
- fact_id: stormwind.dress.045
  claim: 光明大教堂是圣光教会最醒目的丰碑，位于大教堂广场，内部是「镶嵌着钴蓝的石厅」，优雅安宁、宜于祈祷与省思
  tag: ✅
  source: Warcraft Wiki「Cathedral of Light」
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "an elegant and peaceful place, inviting for prayer and reflection" / "cobalt-inlaid stone halls"
  tier: T1
  verified_by: ai_read
  used_in: [priest, bishop]
  prompt_string: "教堂内景基调：米白石材＋钴蓝镶嵌线条；神职的白金法衣在这个底色上要压得住、不能糊成一片白"
  negative: "哥特黑石, 金碧辉煌满堂金, 彩色霓虹, 现代教堂长椅"

- fact_id: stormwind.dress.046
  claim: 人类牧师多穿「符文布长袍」外加一顶配套的帽子
  tag: ✅
  source: Warcraft Wiki「Church of the Holy Light」（Notes 段）
  source_url: https://warcraft.wiki.gg/wiki/Church_of_the_Holy_Light
  quote: "Many human priests are wearing a Runecloth Robe and a matching hat."
  tier: T1
  verified_by: ai_read
  used_in: [priest]
  prompt_string: "牧师是「长袍＋配套软帽」成套出现的，不是光头长袍、也不是单戴兜帽"
  negative: "光头无帽, 单独兜帽不配袍, 盔甲, 现代神父黑袍白领"

- fact_id: stormwind.dress.047
  claim: 圣光教会的徽记戴在大主教的帽子上
  tag: ✅
  source: Warcraft Wiki「Church of the Holy Light」（图注）
  source_url: https://warcraft.wiki.gg/wiki/Church_of_the_Holy_Light
  quote: "The Church's symbol as seen on Archbishop Benedictus' hat"
  tier: T1
  verified_by: ai_read
  used_in: [bishop]
  prompt_string: "圣光徽记的佩戴位置在**帽子正面**，不是挂在胸前的项链"
  negative: "胸前挂十字架, 项链吊坠, 手持权杖顶端, 背后刺绣"
  note: 徽记的具体形状未查到文字描述——见 §未查

- fact_id: stormwind.dress.048
  claim: 圣光的念珠（prayer beads / rosaries of the Light）常用于祈祷
  tag: ✅
  source: Warcraft Wiki「Church of the Holy Light」
  source_url: https://warcraft.wiki.gg/wiki/Church_of_the_Holy_Light
  quote: "Prayer beads and rosaries of the Light are often used in prayer."
  tier: T1
  verified_by: ai_read
  used_in: [priest, bishop]
  prompt_string: "（可入镜细节）祈祷中的信众与低阶神职手里绕着一串素色念珠，拇指一颗一颗推过去"
  negative: "佛珠手串, 十字架念珠, 转经筒"

- fact_id: stormwind.dress.049
  claim: 大主教班尼迪塔斯穿的是「华美的白金法衣」，而且他穿着它时总显得有点不自在
  tag: ✅
  source: Warcraft Wiki「Archbishop Benedictus」（引小说）
  source_url: https://warcraft.wiki.gg/wiki/Archbishop_Benedictus
  quote: "ill at ease in his splendid white and gold robes"
  tier: T1
  verified_by: ai_read
  used_in: [bishop]
  prompt_string: "大主教法衣＝**白底配金**（象牙白厚织缎面，前襟与袖缘一道宽金黄织锦，肩上一条过颈垂到膝的金边披带），层数多、垂坠重"
  negative: "紫袍, 红衣主教红袍, 黑袍, 素麻衣, 金光特效, 发光法衣"

- fact_id: stormwind.dress.050
  claim: 班尼迪塔斯是中年男性，中等身高、结实敦厚，「看上去更像个农夫而不是圣职者」
  tag: ✅
  source: Warcraft Wiki「Archbishop Benedictus」
  source_url: https://warcraft.wiki.gg/wiki/Archbishop_Benedictus
  quote: "a middle-aged man" with "average height and solid, stocky build. Looking more like a farmer than a holy man."
  tier: T1
  verified_by: ai_read
  used_in: [bishop]
  prompt_string: "大主教的脸与身形要反差：一身华美白金法衣，里面是个肩厚手粗、面盘方正、像庄稼人的中年男人"
  negative: "清瘦仙风道骨, 白胡子老者, 苍白病弱, 年轻俊美"

- fact_id: stormwind.dress.051
  claim: 班尼迪塔斯在大灾变之前的造型是「戴兜帽的修士」，改成「长袍＋主教冠」是大灾变才发生的
  tag: ✅
  source: Warcraft Wiki（经 Villains Wiki / Wowpedia 同源段落转述）
  source_url: https://warcraft.wiki.gg/wiki/Archbishop_Benedictus
  quote: "In the Cataclysm expansion, his appearance changed from the appearance of a monk wearing a hood to one wearing a robe and wearing a bishop's crown."
  tier: T1
  verified_by: ai_read
  used_in: [bishop]
  prompt_string: "（版本闸门）Vanilla 的大主教**戴兜帽**（帽沿垂下在眼窝处投一道阴影），**没有主教冠**"
  negative: "主教冠, 教皇三重冕, 高筒法帽, 光头露顶"
  note: >
    这与 046「牧师戴配套帽子」、047「徽记在帽子上」并不冲突——047 的图注取自大灾变之后的大主教造型。
    Vanilla 镜头里：牧师戴软帽、大主教戴兜帽；徽记在兜帽正面还是别处，未查。

- fact_id: stormwind.dress.052
  claim: 大教堂内的神职名录：大主教班尼迪塔斯、High Priestess Laurena（首席牧师训练师）、Lord Grayson Shadowbreaker（首席圣骑士训练师）、Bishop Arthur、Bishop Farthing、Brother Joshua、Brother Benjamin、Katherine the Pure
  tag: ✅
  source: Warcraft Wiki「Cathedral of Light」
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "Archbishop Benedictus (Church leader), High Priestess Laurena (chief priest trainer), Lord Grayson Shadowbreaker (foremost human paladin, chief paladin trainer)... Bishop Arthur, Bishop Farthing (bishops)"
  tier: T1
  verified_by: ai_read
  used_in: [priest, bishop]
  prompt_string: "教堂内至少三档同框：白金法衣的高阶（大主教/女祭司长）、素色长袍的牧师（Brother 一档）、穿胸甲的圣骑士训练师"
  negative: "全场一律白袍, 只有一个人, 全员戴冠"

- fact_id: stormwind.dress.053
  claim: 圣骑士在城里日常只穿胸甲，全套板甲只在仪式时穿；和平时期有人把武器与铠甲换成朴素长袍
  tag: ✅
  source: Warcraft Wiki「Stormwind City」＋「Church of the Holy Light」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Paladins don their full plate during ceremonies but wear only breastplates around the city." / "in times of peace, some exchange their weapons and armor for simple robes"
  tier: T2
  verified_by: ai_read
  used_in: [priest, bishop]
  prompt_string: "大教堂里的圣骑士：钢灰胸甲直接罩在本白布袍外（下半身是布袍不是腿甲），腰挂锤或剑，不戴头盔"
  negative: "全身板甲站教堂, 头盔不摘, 全套仪仗甲"
  note: 这条与 024 同属 RPG 线（T2）；但它描述的是「同一个人在不同场合的穿法」，与游戏内模型不构成冲突，故保留

- fact_id: stormwind.dress.054
  claim: 牧师法衣的配色与形制细节（是否白金、袖型、腰带）——除大主教一人外无文字描述
  tag: ⚠️
  source: 由 045「钴蓝镶嵌石厅」＋ 049「大主教白金法衣」＋ 046「符文布长袍」推得
  source_url: https://warcraft.wiki.gg/wiki/Church_of_the_Holy_Light
  quote: "Many human priests are wearing a Runecloth Robe and a matching hat."
  tier: T1
  verified_by: ai_draft
  used_in: [priest]
  prompt_string: "（待核）普通牧师：及踝直筒长袍（细织布，象牙白底、领口与下摆一道窄金黄织带），腰束一条同色布带打结垂下两条带尾，头戴同布料的圆顶软帽；袖口宽大能盖住手背"
  negative: "紫袍, 黑袍, 露肩, 开衩到腿, 紧身, 发光"
```

---

## 6. 法师区的法师（＋屠宰羔羊酒馆地下的术士）

```yaml
- fact_id: stormwind.dress.058
  claim: 法师只穿布甲——为了不干扰施法
  tag: ✅
  source: Warcraft Wiki「Mage」
  source_url: https://warcraft.wiki.gg/wiki/Mage
  quote: "To avoid interference with their spellcasting, magi wear only cloth armor, but arcane shields and enchantments give them additional protection."
  tier: T1
  verified_by: ai_read
  used_in: [mage]
  prompt_string: "法师全身零金属：布袍、布帽、布腰带、软底布鞋；身上任何一处都不能有铠甲片或金属护肩"
  negative: "锁甲, 金属护肩, 板甲靴, 胸甲, 金属护腕"

- fact_id: stormwind.dress.059
  claim: 法师可用的武器是法杖、魔杖、匕首与单手剑；副手可持非盾牌的手持物
  tag: ✅
  source: Warcraft Wiki「Mage」
  source_url: https://warcraft.wiki.gg/wiki/Mage
  quote: "Weapon skills: Staves, Wands, Daggers, One-handed Swords and held in off-hand items excluding shields and weapons"
  tier: T1
  verified_by: ai_read
  used_in: [mage]
  prompt_string: "法师手里是长法杖（及眉高，木杆、顶端嵌一块不发光的宝石）或短魔杖；绝不持盾"
  negative: "盾牌, 双手巨剑, 长矛, 弓, 法杖发光发电特效"

- fact_id: stormwind.dress.060
  claim: 法师区位于暴风城南角，中偏南是巫师圣殿（法师塔与传送门厅），王国的法师在其中研习奥术
  tag: ✅
  source: Warcraft Wiki「Mage Quarter」＋「Wizard's Sanctum」
  source_url: https://warcraft.wiki.gg/wiki/Mage_Quarter
  quote: "The Mage Quarter lies in the southern corner of Stormwind City." / "the kingdom's mages study the arts of arcane magic"
  tier: T1
  verified_by: ai_read
  used_in: [mage]
  prompt_string: "法师出现在塔内环形厅与区内草药/炼金/裁缝铺门口，不在市集叫卖"
  negative: "法师在菜摊讨价还价, 法师站城门口值勤"

- fact_id: stormwind.dress.061
  claim: 法师区的具名训练师有 Archmage Malin（人类）、Archmage Nakada（人类，法术大师）、Tannysa（暗夜精灵，草药学训练师）；还有一批见习法师 Daniel、Elizabeth、Jenna、Jeremy、Naomi、Sammy
  tag: ✅
  source: Warcraft Wiki「Mage Quarter」
  source_url: https://warcraft.wiki.gg/wiki/Mage_Quarter
  quote: "Archmage Malin (Human, Mage trainer), Archmage Nakada (Human, Master of Spells), Tannysa (Night Elf, Herbalism Trainer)... Junior mages in training include Daniel, Elizabeth, Jenna, Jeremy, Naomi, and Sammy."
  tier: T1
  verified_by: ai_read
  used_in: [mage]
  prompt_string: "法师有两档：大法师（年长、袍更重更长、独自站在塔心）与见习法师（年轻、袍更短更素、三两成组围着一张桌子）"
  negative: "全员同款同龄, 全员大法师"

- fact_id: stormwind.dress.062
  claim: 法师区的「屠宰羔羊」是一家阴暗小酒馆，地下墓室是暴风城术士的秘密训练所；三名人类术士训练师 Demisette Cloyce、Sandahl、Ursula Deline，外加侏儒恶魔训练师 Spackle Thornberry 与小鬼 Zggi
  tag: ✅
  source: Warcraft Wiki「The Slaughtered Lamb」
  source_url: https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb
  quote: "a seedy pub in the Mage Quarter of Stormwind City" / 酒保 Jarel Moor 劝客人 "stay away from the shadows"
  tier: T1
  verified_by: ai_read
  used_in: [warlock]
  prompt_string: "术士与法师同穿布袍但反着来：法师袍浅、术士袍深；术士在地下室烛光里，脚边有一只齐膝高的小鬼"
  negative: "术士穿铠甲, 术士在街上公开施法, 地上层就有术士"

- fact_id: stormwind.dress.063
  claim: 法师袍的配色与形制细节（兜帽有无、腰带样式、肩部结构）——无文字描述
  tag: ⚠️
  source: 由 058「只穿布甲」＋ 060「巫师圣殿」＋ 「Mage Quarter 有裁缝铺 Duncan's Textiles」推得
  source_url: https://warcraft.wiki.gg/wiki/Mage
  quote: "Armor type: Cloth"
  tier: T1
  verified_by: ai_draft
  used_in: [mage]
  prompt_string: "（待核）法师：连兜帽拖地长袍（细织布，靛蓝或紫罗兰为主、袖口与下摆一道银灰几何纹滚边，两侧开衩便于迈步），兜帽戴起时只露下半张脸，腰束一条系了布结的软腰带、上面挂一只小皮袋"
  negative: "尖顶巫师帽, 星月图案袍, 现代学院袍, 金属扣, 露肩, 短袍, 袍上发光符文"

- fact_id: stormwind.dress.064
  claim: 术士袍的配色与形制细节——无文字描述
  tag: ⚠️
  source: 由 062「地下墓室、阴暗小酒馆、恶魔训练师」推得
  source_url: https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb
  quote: "The catacombs beneath the pub serve as the secret training sanctuary for Stormwind's warlocks."
  tier: T1
  verified_by: ai_draft
  used_in: [warlock]
  prompt_string: "（待核）术士：深兜帽长袍（粗织布，炭黑与暗紫为主、边缘一道暗红缝线，肩上搭一条厚料短披肩），兜帽压得比法师更低、脸只剩下颌与嘴；手上无杖时持一本厚皮面书"
  negative: "绿色火焰特效, 骷髅头饰, 荧光紫瞳, 恶魔角, 露胸紧身装"
```

---

## 7. 矮人与侏儒工匠（矮人区）

```yaml
- fact_id: stormwind.dress.066
  claim: 矮人女性平均身高 4 英尺 6 英寸、男性约 4 英尺 8 英寸（少数男性略过 5 英尺）；矮人体格矮壮有力
  tag: ✅
  source: Warcraft Wiki「Dwarf」
  source_url: https://warcraft.wiki.gg/wiki/Dwarf
  quote: "On average, women reach a height of 4'6\" while men generally stand around 4'8\" tall" / "Dwarves are squat and powerfully built."
  tier: T1
  verified_by: ai_read
  used_in: [dwarf_smith]
  prompt_string: "矮人身高约一米四二，头顶约到人类胸口；肩宽几乎等于身高的一半，四肢短粗、手掌厚大"
  negative: "缩小版人类比例, 头身比正常的小个子, 瘦长矮人, 儿童体型"

- fact_id: stormwind.dress.067
  claim: 矮人男性**必定**有胡子，通常是又长又野的大胡子，有时头发也一样野
  tag: ✅
  source: Warcraft Wiki「Dwarf」
  source_url: https://warcraft.wiki.gg/wiki/Dwarf
  quote: "The males always have beards, typically a long wild beard sometimes with hair to match."
  tier: T1
  verified_by: ai_read
  used_in: [dwarf_smith]
  prompt_string: "矮人男性一律大胡子：垂到胸口、发丝粗硬带卷、常编成一两股用铜环箍住；干活时把胡子塞进围裙里或甩到肩后"
  negative: "净面矮人, 山羊胡, 修剪整齐的短须, 光头无须"

- fact_id: stormwind.dress.068
  claim: 部分矮人女性也留浓密的胡须，在族内被视为美的象征
  tag: ✅
  source: Warcraft Wiki「Dwarf」
  source_url: https://warcraft.wiki.gg/wiki/Dwarf
  quote: "Some females sport strong beards as well, which is considered a sign of beauty among members of the race."
  tier: T1
  verified_by: ai_read
  used_in: [dwarf_smith]
  prompt_string: "群像里可安排一位有胡须的矮人女性（编成两股辫、缀铜环），面部结构仍是女性"
  negative: "把有胡子的女矮人画成男性, 全员女矮人都有胡子"

- fact_id: stormwind.dress.069
  claim: 侏儒女性平均身高 3 英尺 4 英寸、男性约 3 英尺 6 英寸；少数只有 2 英尺 6 英寸
  tag: ✅
  source: Warcraft Wiki「Gnome」
  source_url: https://warcraft.wiki.gg/wiki/Gnome
  quote: "On average, female gnomes are 3'4\" tall while males aren't much larger, typically standing at close to 3'6\" in height."
  tier: T1
  verified_by: ai_read
  used_in: [gnome_tinker]
  prompt_string: "侏儒身高约一米零七，头顶约到人类腰际、到矮人胸口；三种体型同框时高度差要清清楚楚"
  negative: "和矮人一样高, 儿童比例, 娃娃脸无年龄感"

- fact_id: stormwind.dress.070
  claim: 侏儒每只手四指（三指加一拇指）、脚五趾；游戏模型中耳朵相对头部又大又圆
  tag: ✅
  source: Warcraft Wiki「Gnome」
  source_url: https://warcraft.wiki.gg/wiki/Gnome
  quote: "They have four fingers (three fingers, one thumb) on each hand, and five-toed feet." / "in World of Warcraft, the gnome model is noted to have large, rounded ears in proportion to their head."
  tier: T1
  verified_by: ai_read
  used_in: [gnome_tinker]
  prompt_string: "侏儒手部特写必须是四指（三指＋拇指）；耳朵大而圆、贴头侧，不是尖耳"
  negative: "五指的手, 精灵尖耳, 小圆耳, 兽耳"
  note: 这是最容易被生成模型画错的一处——手部入画的镜要显式写四指

- fact_id: stormwind.dress.071
  claim: 侏儒常带着护目镜、工具腰带等与其技术倾向相关的物件
  tag: ✅
  source: Warcraft Wiki「Gnome」
  source_url: https://warcraft.wiki.gg/wiki/Gnome
  quote: "are often seen with goggles, tool belts, and other items related to their technological inclinations"
  tier: T1
  verified_by: ai_read
  used_in: [gnome_tinker]
  prompt_string: "侏儒工匠标配：黄铜边护目镜（不戴时推到额头上，镜片是茶色玻璃、边上有一圈调节旋钮），腰上一条插满钳锉的宽皮工具带，皮手套的指端被烧短一截"
  negative: "太阳镜, 现代焊接面罩, 空手无工具, 干净手套"

- fact_id: stormwind.dress.072
  claim: 侏儒发色变化极大，甚至有粉色或绿色的头发
  tag: ✅
  source: Warcraft Wiki「Gnome」（RPG 段）
  source_url: https://warcraft.wiki.gg/wiki/Gnome
  quote: "Their hair color varies wildly, some even having pink or green hair."
  tier: T1
  verified_by: ai_read
  used_in: [gnome_tinker]
  prompt_string: "侏儒是全城唯一允许出现粉色 / 绿色头发的族群——半写实画风下处理成染过的哑光色，不是荧光"
  negative: "荧光发色, 渐变挑染, 人类也染彩发"

- fact_id: stormwind.dress.073
  claim: 矮人区的锻炉终日产生烟霾，锤声不断；区内是从人类原有大宅改造加层而成的矮人住宅
  tag: ✅
  source: Warcraft Wiki「Dwarven District」
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The forges in the district produce a constant haze, supplemented by the constant strokes of smiths' hammers." / "large houses heavily modified for dwarf use with additional floors and rooms dividing the original, overly large and wasteful, human designs"
  tier: T1
  verified_by: ai_read
  used_in: [dwarf_smith, gnome_tinker]
  prompt_string: "矮人区的人脸上有一层薄煤灰（尤其鼻侧与颈后），衣服上有细小火星灼孔；空气里有可见的烟霾使远处轮廓变淡"
  negative: "干净脸, 无烟清爽, 白色工作服, 无尘车间"

- fact_id: stormwind.dress.074
  claim: 矮人区的具名训练师：Therum Deepforge（锻造）、Lilliam Sparkspindle（工程学，侏儒）；另有采矿补给与猎人公会、拍卖行
  tag: ✅
  source: Warcraft Wiki「Dwarven District」
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "Blacksmithing: Therum Deepforge (trainer) and supporting smiths. Engineering: Lilliam Sparkspindle (trainer) and gnome engineers."
  tier: T1
  verified_by: ai_read
  used_in: [dwarf_smith, gnome_tinker]
  prompt_string: "分工可视化：矮人在露天砧前抡锤（大件、热活），侏儒在工作台前低头装配（小件、精细活）"
  negative: "矮人做精细活, 侏儒抡大锤, 两族分工混同"

- fact_id: stormwind.dress.075
  claim: 矮人区东侧有隧道通往深铁矿车（Deeprun Tram）——Vanilla 已有
  tag: ✅
  source: Warcraft Wiki「Dwarven District」
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The Stormwind City end of the Deeprun Tram line is accessible through a tunnel on the east side of the district."
  tier: T1
  verified_by: ai_read
  used_in: [dwarf_smith]
  prompt_string: "（可入镜细节）矮人区东侧有一个向下的隧道口，有矮人与侏儒拎着行李进出"
  negative: "地铁闸机, 现代车站, 电梯"

- fact_id: stormwind.dress.076
  claim: 矮人工匠的具体工作服形制（上衣、裤、靴、围裙裁剪）——无文字描述
  tag: ⚠️
  source: 由 066「矮壮」＋ 073「锻炉烟霾锤声」＋ 033「皮围裙」推得
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "blacksmiths create masterpieces out of common metals in many open-air plazas"
  tier: T1
  verified_by: ai_draft
  used_in: [dwarf_smith]
  prompt_string: "（待核）矮人铁匠：无袖粗布衬衣（本白或麻褐，前襟敞开）外罩厚牛皮围裙（深棕，胸口一道加厚横带、肩带在背后交叉、下摆及小腿），围裙面布满灼痕；腰上宽皮带挂锤与钳，小臂裸露布满旧烫疤，脚穿厚底铁头短靴"
  negative: "长袖工装, 布围裙, 全身板甲打铁, 赤膊无围裙, 现代工装裤"

- fact_id: stormwind.dress.077
  claim: 侏儒工匠的具体工作服形制——无文字描述
  tag: ⚠️
  source: 由 071「护目镜、工具腰带」＋ 074「侏儒工程师」推得
  source_url: https://warcraft.wiki.gg/wiki/Gnome
  quote: "are often seen with goggles, tool belts, and other items related to their technological inclinations"
  tier: T1
  verified_by: ai_read
  used_in: [gnome_tinker]
  prompt_string: "（待核）侏儒技师：连体工作服（厚帆布，橄榄褐或铁灰，胸前两只带盖口袋、膝部与肘部有补强皮片、袖口用铜扣收紧），外系短皮工具围裙只到大腿；额头推着黄铜边护目镜，脚穿厚底短靴"
  negative: "长袍, 中世纪束腰衫, 现代连帽卫衣, 白大褂, 赤脚"

- fact_id: stormwind.dress.078
  claim: 矮人肤色与瞳色——Warcraft Wiki 的矮人外观段没有写
  tag: ⚠️
  source: Warcraft Wiki「Dwarf」明确缺失
  source_url: https://warcraft.wiki.gg/wiki/Dwarf
  quote: "The wiki does not provide specific descriptions of typical dwarf clothing or skin color in the physical appearance sections provided."
  tier: T1
  verified_by: ai_read
  used_in: [dwarf_smith]
  prompt_string: "（待核）矮人肤色走人类同一区间（浅粉到晒褐），但面部皮肤更粗厚、毛孔更明显、颧骨与眉骨更突"
  negative: "灰皮肤, 石头质感皮肤, 绿皮, 蓝皮"
```

---

## 8. SI:7 / 潜行者（旧城区）

```yaml
- fact_id: stormwind.dress.080
  claim: 潜行者穿皮甲；皮甲比其他近战职业的锁甲与板甲更弱
  tag: ✅
  source: Warcraft Wiki「Rogue」
  source_url: https://warcraft.wiki.gg/wiki/Rogue
  quote: "Rogues wear leather armor. Leather is weaker than the mail and plate worn by other melee classes"
  tier: T1
  verified_by: ai_read
  used_in: [si7]
  prompt_string: "潜行者全身皮质：半哑光的鞣制皮，肩、胸、前臂有缝线分片，动起来无金属撞击声、无反光带"
  negative: "板甲, 锁甲, 金属护肩, 布袍, 亮面漆皮, 铆钉朋克装"

- fact_id: stormwind.dress.081
  claim: 潜行者被形容为「夜里不被看见的影子」「越过暗野的兜帽身影」，偏好匕首与单手武器，常双持并给武器淬毒
  tag: ✅
  source: Warcraft Wiki「Rogue」
  source_url: https://warcraft.wiki.gg/wiki/Rogue
  quote: "the shadows in the night that remain unseen" / "hooded figures crossing dark fields"
  tier: T1
  verified_by: ai_read
  used_in: [si7]
  prompt_string: "潜行者一律戴兜帽（帽沿压到眉线，脸只剩下颌与嘴），腰后交叉挂两把短匕；站姿重心低、肩收、手不离刀柄"
  negative: "露脸无兜帽, 长剑, 双手斧, 盾牌, 大摇大摆走路"

- fact_id: stormwind.dress.082
  claim: SI:7 是暴风城君主的秘密军事力量，总部在旧城区同名建筑内
  tag: ✅
  source: Warcraft Wiki「SI:7」
  source_url: https://warcraft.wiki.gg/wiki/SI:7
  quote: "a secretive military force of Stormwind's sovereign monarch" / "its headquarters located in the building with the same name, in the Old Town quarter of Stormwind City"
  tier: T1
  verified_by: ai_read
  used_in: [si7]
  prompt_string: "SI:7 的人出现在旧城区窄巷与那栋挂着招牌的建筑门口，不在主街中央"
  negative: "SI:7 在贸易区摆摊, 在王座厅公开亮相"

- fact_id: stormwind.dress.083
  claim: SI:7 成员的识别物是「一件白色衣物上仔细缝进一根红线，看起来像根没摘掉的线头」；组织徽记是一只拳头
  tag: ✅
  source: Warcraft Wiki「SI:7」
  source_url: https://warcraft.wiki.gg/wiki/SI:7
  quote: "one piece of white clothing with a single red thread carefully sewn in, looking like a stray piece of lint" / "The organization's symbol is a fist."
  tier: T1
  verified_by: ai_read
  used_in: [si7]
  prompt_string: "（可入镜细节）SI:7 的人身上有且仅有一件白色衣物（内衬领口或袖口露出的一角），上面一根红线，短得像根线头——特写才看得见，中景看不出"
  negative: "大红标记, 显眼臂章, 全身白衣, 胸前挂徽章, 红丝带蝴蝶结"

- fact_id: stormwind.dress.084
  claim: SI:7 首领是 Master Mathias Shaw（人类），是潜行与渗透的大师；旧城区的 SI:7 也是潜行者职业训练点
  tag: ✅
  source: Warcraft Wiki「SI:7」＋「Old Town」
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "The secretive intelligence agency operates from Old Town under the command of Spymaster Mathias Shaw" / "SI:7 serves as the primary location for Rogue class instruction."
  tier: T1
  verified_by: ai_read
  used_in: [si7]
  prompt_string: "SI:7 内有两档：一位不戴兜帽、露脸、腰佩双匕的红发首领，与一群戴兜帽的匿名特工"
  negative: "首领也戴兜帽遮脸, 全员露脸, 制服化统一"

- fact_id: stormwind.dress.085
  claim: SI:7 普通特工「常配武士刀与胁差、穿卡其色渗透制服」——这句的版本归属存疑，卡其色与日式双刀不属 Vanilla 视觉
  tag: ❌
  source: Warcraft Wiki「SI:7」
  source_url: https://warcraft.wiki.gg/wiki/SI:7
  quote: "Generic agents are often armed with katana and wakizashi swords while wearing khaki infiltration uniforms."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "武士刀, 胁差, 卡其色制服, 忍者装, 日式配色"
  note: >
    版本判定：这条描述对应的是后期资料片（BfA 之后）的 SI:7 模型。Vanilla 锚点下一律不画。
    Vanilla 的 SI:7 走 080/081 的「深色皮甲＋兜帽＋双匕」。

- fact_id: stormwind.dress.086
  claim: 旧城区还设有指挥中心（Command Center），内有勇士大厅、兵营、训练场与马厩，驻猎人与战士训练师
  tag: ✅
  source: Warcraft Wiki「Old Town」
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "This military installation houses the Stormwind army's operations, including the Champions' Hall, barracks, training grounds, and stables. Hunter and Warrior trainers are stationed here."
  tier: T1
  verified_by: ai_read
  used_in: [si7, guard]
  prompt_string: "旧城区同框两种人：巷子里的兜帽皮甲身影，与训练场上穿板甲对练的士兵——一暗一明"
  negative: "旧城区只有贼, 只有兵"
  note: 该区在大灾变后经过重新设计（加了林地训练区、扩了马厩）——Vanilla 用旧布局

- fact_id: stormwind.dress.087
  claim: SI:7 特工皮甲的具体形制（分片、兜帽形状、披风有无、色名）——无 Vanilla 文字描述
  tag: ⚠️
  source: 由 080「皮甲」＋ 081「兜帽身影」＋ 083「唯一一件白衣＋红线」推得
  source_url: https://warcraft.wiki.gg/wiki/Rogue
  quote: "Rogues wear leather armor."
  tier: T1
  verified_by: ai_draft
  used_in: [si7]
  prompt_string: "（待核）SI:7 特工：连兜帽皮质紧身上衣（哑光鞣革，炭黑与深烟灰拼色，胸前一道斜向缝合线、肩部一层加厚覆片、腰间宽皮带加两只小扣袋），内衬露出一角本白布领（上有一根红线），下配深色紧腿裤与无声软底皮靴，腰后交叉两把短匕"
  negative: "金属护肩, 亮面皮衣, 披风, 铆钉, 露脸, 鲜艳配色, 现代战术背心"
```

---

## 9. 公园区的暗夜精灵（Vanilla 时公园区完好）

```yaml
- fact_id: stormwind.dress.090
  claim: 公园区位于暴风城西角，原本是市民休闲地，后来成了来访暗夜精灵的居所——他们觉得这里的自然气息是石砌大道之外的安慰
  tag: ✅
  source: Warcraft Wiki「Park」
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "The Park used to be the district located in the western corner of Stormwind City. It was once a place devoted to leisure activities for Stormwind's populace until it became a refuge for visiting night elves, who found the comforting presence of nature a welcome respite from the vast stone thoroughfares of Stormwind proper."
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "公园区是全城唯一以绿为主的区：暗夜精灵在树影与草地上活动，衣料颜色跟着环境走（森绿、苔色、暗紫），与外面白石街道形成整片色差"
  negative: "石板广场, 城市灰调, 鲜艳撞色, 暗夜精灵穿人类平民装"

- fact_id: stormwind.dress.091
  claim: 暗夜精灵在公园中央造了一口月亮井；这里是东部王国唯一有德鲁伊训练师的地方
  tag: ✅
  source: Warcraft Wiki「Park」
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "The night elves created a Moonwell in the center of the park square." / "It was the only place in the Eastern Kingdoms where druid trainers resided."
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "（可入镜细节）园心一口环形石砌月亮井，水面泛冷银色微光（是水本身的反光，不是发光特效）；德鲁伊在井边盘腿或站立"
  negative: "喷泉, 许愿池, 荧光蓝水, 水柱特效, 水中发光符文"

- fact_id: stormwind.dress.092
  claim: 公园区是在大灾变中被死亡之翼摧毁的——Vanilla 时它完好无损（后来原址建成了镀金玫瑰陵园）
  tag: ✅
  source: Warcraft Wiki「Park」
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "The Park was destroyed by Deathwing's visit to Stormwind, during the Cataclysm." / "Lion's Rest has been built on the site of the former Park."
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "（版本闸门）Vanilla 镜头里公园区完整、绿意盎然、有月亮井"
  negative: "废墟, 焦土, 镀金玫瑰陵园, 纪念碑, 墓园"

- fact_id: stormwind.dress.093
  claim: 公园区的具名 NPC 全是暗夜精灵：Sheldras Moontree / Maldryn / Theridran（德鲁伊训练师）、Nara Meideros（牧师训练师）、Shylamiir（草药学训练师）、Sylista（驯兽师）
  tag: ✅
  source: Warcraft Wiki「Park」
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "Sheldras Moontree (Night Elf, Druid Trainer), Maldryn (Night Elf, Druid Trainer), Theridran (Night Elf, Druid Trainer), Nara Meideros (Night Elf, Priest Trainer), Shylamiir (Night Elf, Herbalism Trainer), Sylista (Night Elf, Stable Master)"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "公园区两档暗夜精灵：德鲁伊（皮甲＋自然元素）与月神牧师（长袍）；男女都有"
  negative: "全员女性, 全员德鲁伊, 混入人类训练师"

- fact_id: stormwind.dress.094
  claim: 暗夜精灵平均身高 7–8 英尺（213–244 厘米）
  tag: ✅
  source: Warcraft Wiki「Night elf」
  source_url: https://warcraft.wiki.gg/wiki/Night_elf
  quote: "Average height 7–8 feet (213 - 244 cm)"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "暗夜精灵比人类高一头半（约两米二），四肢修长、肩窄腰长；与人类同框时人类要仰头看"
  negative: "和人类一样高, 矮小精灵, 圆润体型"

- fact_id: stormwind.dress.095
  claim: 暗夜精灵肤色落在紫色谱系的宽区间，从最深的兰紫到最浅的淡粉；部分个体呈各种蔚蓝色调或带一种苍白乳色的珠光白
  tag: ✅
  source: Warcraft Wiki「Night elf」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Night_elf&action=raw
  quote: "fall into a broad range of the purple spectrum. Colors may vary from the darkest orchid to the faintest pink. Some individuals may even appear various hues of cerulean or bear a pale milky, opalescent shade of white."
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "暗夜精灵皮肤：紫色谱系（深兰紫 / 淡粉紫 / 蔚蓝 / 珠光乳白 任选一档并锁死），半写实处理成有真实毛孔与皮下血色的皮肤，不是涂色塑料"
  negative: "绿皮, 灰皮, 纯白无血色, 涂料感平色, 荧光紫, 蓝人特效妆"

- fact_id: stormwind.dress.096
  claim: 暗夜精灵的眼睛因远古与永恒之井的联系而常年发光，呈银色或金色光辉；游戏模型中女性是发光银眼、男性是琥珀色，但两种眼色并不按性别排他
  tag: ✅
  source: Warcraft Wiki「Night elf」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Night_elf&action=raw
  quote: "in-game models show female night elves with glowing silver eyes, while the male's eyes have an amber glow to them, the two eye colors are not exclusive to gender"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "暗夜精灵瞳孔发光：女性冷银、男性暖琥珀；发光是**眼球自身的内透光**，不向外投射光束、不在脸上打光斑、不拖尾"
  negative: "眼睛射光束, 眼周发光特效, 红瞳, 眼睛冒火, 荧光贴片, 发光拖尾"
  note: >
    与 CLAUDE.md 光线自查条呼应——「眼睛发光」极易被生成模型渲成外放特效。
    正确写法是把它写成材质属性（虹膜自发光、亮度低于环境光），不是灯光。

- fact_id: stormwind.dress.097
  claim: 暗夜精灵的发色以蔚蓝与紫罗兰为主，其次是各种绿，以及接近白的银；少数（多在上层精灵中）有红、琥珀、金、棕等秋色
  tag: ✅
  source: Warcraft Wiki「Night elf」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Night_elf&action=raw
  quote: "a panorama of azures and violet, followed closely by greens and even silver" / "autumnal tinctures such as red, amber, blonde, and brown"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "暗夜精灵发色限：蔚蓝 / 紫罗兰 / 森绿 / 近白银 四档；半写实下是有层次的真实发丝，不是一整块色"
  negative: "黑发, 金发（除非上层精灵）, 粉发, 荧光发, 塑料整块发色"

- fact_id: stormwind.dress.098
  claim: 与其他精灵族不同，暗夜精灵男性常有浓密精致的胡须与浓眉
  tag: ✅
  source: Warcraft Wiki「Night elf」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Night_elf&action=raw
  quote: "Unlike most of their elven cousins, Kaldorei men often have thick, elaborate beards and bushy eyebrows."
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "暗夜精灵男性：浓密长须（与发色同系，常编成股）＋浓重外扬的眉；不是净面美少年"
  negative: "净面无须, 细眉, 中性少年脸, 光滑下巴"
  note: 这是最容易画错的一处——大众印象里的精灵男性都是净面的

- fact_id: stormwind.dress.099
  claim: 暗夜精灵女性在成年之后选定面部刺青，可标记更早的一次成年礼；这些刺青代表她们与自然的紧密联系，典型式样是风格化的爪痕
  tag: ✅
  source: Warcraft Wiki「Night elf」（原始 wikitext）
  source_url: https://warcraft.wiki.gg/index.php?title=Night_elf&action=raw
  quote: "facial markings sometime after adulthood, and they can mark an earlier rite of passage" / "represent their close ties with nature" / "stylized claw marks"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "暗夜精灵女性面部刺青：左右对称的风格化爪痕（三道一组，从眉骨扫过颧骨），颜色比肤色深一到两档、哑光、像染进皮肤而非画上去"
  negative: "不对称涂鸦, 发光刺青, 部落图腾, 汉字, 符文, 亮色颜料感"

- fact_id: stormwind.dress.100
  claim: 德鲁伊只能穿布甲与皮甲；可用武器是长杖、匕首、单手或双手锤、拳套与长柄武器
  tag: ✅
  source: Warcraft Wiki「Druid」
  source_url: https://warcraft.wiki.gg/wiki/Druid
  quote: "Druids are able to wear cloth and leather armor only" / "Druids can equip staves, daggers, one-handed or two-handed maces, fist weapons, and polearms"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "德鲁伊：皮甲为主、布为辅，手持一根粗木长杖（树皮未剥净、顶端分叉处夹一块原石）；全身零金属片"
  negative: "板甲, 锁甲, 金属护肩, 长剑, 盾牌, 弓"

- fact_id: stormwind.dress.101
  claim: 德鲁伊的两大流派在设定源头就用披挂作区分：利爪德鲁伊背上披熊皮、鸦爪德鲁伊披羽氅
  tag: ✅
  source: Warcraft Wiki「Druid」（Warcraft III 段）
  source_url: https://warcraft.wiki.gg/wiki/Druid
  quote: "Druids of the Claw wear bear pelts on their back" / "Druids of the Talon wear feathered cloaks"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "德鲁伊背上二选一：整张熊皮（带头骨盖在肩上，毛色深棕，前爪在胸前交叉系住）／羽氅（层叠的深灰与墨绿长羽，从肩铺到腰）"
  negative: "披风, 斗篷, 布料外套, 塑料羽毛, 天使翅膀"

- fact_id: stormwind.dress.102
  claim: 德鲁伊袍/皮甲的具体分片与色名——无 Vanilla 文字描述
  tag: ⚠️
  source: 由 100「布＋皮」＋ 101「熊皮/羽氅」＋ 090「公园区自然基调」推得
  source_url: https://warcraft.wiki.gg/wiki/Druid
  quote: "Druids are able to wear cloth and leather armor only"
  tier: T1
  verified_by: ai_draft
  used_in: [nightelf]
  prompt_string: "（待核）暗夜精灵德鲁伊：无袖皮质长身外衣（哑光鞣革，森绿与树皮褐拼色，肩头一块弧形加厚皮片、腰间宽皮带上缠一圈藤条、下摆前短后长开衩到膝），内衬本色粗麻长袖；小臂缠皮绳，赤足或穿软底皮履"
  negative: "金属甲片, 华丽刺绣, 亮面皮, 高跟靴, 布制长袍拖地, 荧光纹样"

- fact_id: stormwind.dress.103
  claim: 月神牧师（如 Nara Meideros）的法衣形制与色名——无 Vanilla 文字描述
  tag: ⚠️
  source: 由 093「Nara Meideros 是暗夜精灵牧师训练师」＋ 091「月亮井」推得
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "Nara Meideros (Night Elf, Priest Trainer)"
  tier: T1
  verified_by: ai_draft
  used_in: [nightelf]
  prompt_string: "（待核）暗夜精灵女祭司：及地长袍（细织布，午夜蓝底、领口与袖缘一道冷银织纹，两肩各一片薄纱垂到肘），腰束银灰软带；长发在脑后挽起、额前一道弧形银饰"
  negative: "白金圣光法衣, 人类牧师软帽, 露肩紧身, 太阳纹样, 金色为主"

- fact_id: stormwind.dress.104
  claim: 暴风城在 Vanilla 已住有高等精灵（high elves）——公园区之外还有第二种精灵体型
  tag: ✅
  source: Warcraft Wiki「Stormwind City」
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "humans, many dwarves, gnomes, high elves, and night elves and other races"
  tier: T1
  verified_by: ai_read
  used_in: [街景群像]
  prompt_string: "高等精灵与暗夜精灵要分清：高等精灵身高接近人类、肤色浅、眼睛发蓝光；暗夜精灵高一头半、紫皮、银/琥珀眼"
  negative: "把高等精灵画成暗夜精灵, 血精灵绿眼（血精灵是燃烧的远征才有）"

- fact_id: stormwind.dress.105
  claim: 暗夜精灵的「鹿角」与「金眼」在 wiki 中是独立小节，说明它们是**特例而非通例**
  tag: ⚠️
  source: Warcraft Wiki「Night elf」目录结构（Appearance and biology 下设 Golden eyes / Antlers / Facial tattoos 三个子节）
  source_url: https://warcraft.wiki.gg/wiki/Night_elf
  quote: "subsections for: Golden eyes, Antlers, Facial tattoos, Aging and lifespan"
  tier: T1
  verified_by: ai_read
  used_in: [nightelf]
  prompt_string: "公园区的普通暗夜精灵**不长鹿角**；鹿角只属于极个别与自然深度结合的个体，本片不画"
  negative: "人人头顶鹿角, 树枝状头饰, 藤蔓长在头上"
```

---

## 锁定串总表

> **这张表是本路最重要的产物**，下游直接进人物卡与 shot prompt。
> 「定稿状态」列：`可用` ＝ 形制有 T1/T2 依据，可直接进 prompt；`待核` ＝ 骨架有据但细节为推定，进 prompt 前须人眼核 Modelviewer 并改 `human`。

| # | 身份 | 锁定串 | 负向词 | 回指 fact_id | 定稿状态 |
|---|---|---|---|---|---|
| 1 | **暴风城卫兵**（城市卫兵） | 全身锻钢板甲（抛光钢灰，胸甲一整片弧面带中脊、肩甲双层弧形叠片外沿上翘且素净无浮雕、护臂与护胫分段铆接，关节缝露深灰锁环），外罩过膝罩袍（厚织呢，群青蓝底，正中一颗金黄狮首，两侧开衩至腰）用皮带束在腰间；头戴钢灰全覆式板盔（盔顶一道纵向脊、前脸横向观察缝，无羽饰无角），右手宽刃直身阔剑、左手鸢形盾（群青蓝底金黄狮首），背后空无披风；夜间改提铜壳油灯。**不是**后期资料片的镀金浮雕重甲，也**不是**地球中世纪的白底红十字十字军罩袍 | 镀金浮雕重甲, 银白发光铠甲, 锁子甲, 白底红十字罩袍, 红色罩袍, 羽饰头盔, 尖刺肩甲, 披风, 长戟, 圆盾, 现代警服, 皮甲, 整身涂蓝, 女性卫兵, 火把 | 010–024, 003, 004 | 待核（头盔面甲形状） |
| 2 | **皇家卫队**（王宫） | 与卫兵同源：群青蓝金狮罩袍＋钢灰板甲，但罩袍更长至小腿、甲面无战损、一律戴盔不露脸；成对立于王座厅门道两侧、面朝中线纹丝不动；清一色男性。**不是**镀金礼仪甲，也**不是**街头卫兵的原样复制 | 金甲, 红罩袍, 华丽羽饰, 女性皇家卫队, 走动巡逻, 与街头卫兵完全同款 | 025–029 | 待核（与卫兵的差异点） |
| 3 | **平民男性**（商贩/工匠/搬运） | 粗纺束腰长衫（粗麻，麻褐或本白，开襟到胸口用两三根系带、袖口卷到小臂），下配深褐粗布长裤，小腿缠布带，脚穿翻口皮靴；腰间宽皮带挂得住工具；蓄修剪过的短须、短发。**不是**中式盘扣长衫，也**不是**现代衬衫牛仔裤 | 中式盘扣, 和服, 现代衬衫领, 牛仔裤, 拉链, 印花图案, 露腹肌背心, 华服, 珠宝 | 002, 030–034 | 待核（领口与系法） |
| 4 | **平民女性**（女摊主/女侍/织工） | 长袖束腰连身长裙（粗纺，暗酒红或苔绿或麻褐，圆领、腰间编绳束带、裙摆及踝），外系本白粗麻围裙（腰后打结、两侧无褶），头上系一方素色头巾包住发际；长发在脑后挽低髻或编一条粗辫搭肩前。**不是**中式襦裙，也**不是**束胸紧身胸衣的西幻女仆装 | 中式襦裙, 和服, 束胸紧身胸衣, 露肩, 蕾丝, 蓬蓬裙, 短裙, 高跟鞋, 印花布, 披散长发 | 002, 035–039 | 待核（裙型与围裙系法） |
| 5 | **铁匠/工匠**（人类，通用） | 厚牛皮围裙（深棕，胸口一道横向加厚带、两条肩带背后交叉、下摆过膝，面上布满暗色火星灼痕与锤击压光），袖子卷到肘上、小臂裸露带汗光与旧烫疤。**不是**厨师白围裙，也**不是**无尘车间的干净工装 | 布围裙, 厨师白围裙, 塑料围裙, 干净无痕围裙, 长袖不卷, 现代工装裤 | 033, 073 | 可用 |
| 6 | **贵族/廷臣** | 齐膝开襟外袍（厚天鹅绒，深群青或暗酒红，前襟与袖口一道金黄织锦滚边、下摆分前后两片），内穿本白细麻高领内衫，腰束宽皮带配方形金属带扣，下配深色贴腿裤与及踝软皮短靴；配饰限印章戒与圆形披肩胸针；下巴微抬、手背身后。**不是**中式长袍马褂，也**不是**现代西装或燕尾服 | 中式长袍马褂, 和服, 燕尾服, 现代西装, 王冠, 全身金甲, 拖地斗篷, 蕾丝领巾, 玉佩, 朝珠, 乌纱帽 | 040–044, 031 | 待核（外袍裁剪） |
| 7 | **圣光牧师**（大教堂，Brother 一档） | 及踝直筒长袍（细织布，象牙白底、领口与下摆一道窄金黄织带，袖口宽大盖住手背），腰束同色布带打结垂两条带尾，头戴同布料圆顶软帽；手里绕一串素色念珠。**不是**红衣主教的红袍，也**不是**现代神父的黑袍白领 | 紫袍, 黑袍, 红衣主教红袍, 素麻衣, 露肩, 开衩到腿, 紧身, 发光法衣, 佛珠, 十字架 | 045–048, 053, 054 | 待核（牧师袍配色） |
| 8 | **大主教**（Vanilla 档） | 华美白金法衣（象牙白厚织缎面，前襟与袖缘一道宽金黄织锦，肩上一条过颈垂到膝的金边披带，层数多、垂坠重）＋**兜帽**（帽沿在眼窝投一道阴影）；里面是个肩厚手粗、面盘方正、像庄稼人的中年男人，穿着这身总显得不自在。**不是**大灾变之后的主教冠造型，也**不是**清瘦仙风道骨的白胡子老者 | 主教冠, 教皇三重冕, 高筒法帽, 紫袍, 红袍, 黑袍, 清瘦仙风道骨, 白胡子老者, 年轻俊美, 金光特效 | 049–052 | 可用（兜帽已确证） |
| 9 | **法师**（法师区） | 连兜帽拖地长袍（细织布，靛蓝或紫罗兰为主、袖口与下摆一道银灰几何纹滚边，两侧开衩），兜帽戴起只露下半张脸，腰束系了布结的软腰带挂一只小皮袋；手持及眉高长法杖（木杆、顶端嵌一块**不发光**的宝石）；全身零金属。**不是**尖顶巫师帽配星月图案的童话巫师，也**不是**现代学院袍 | 尖顶巫师帽, 星月图案袍, 现代学院袍, 金属扣, 护肩, 锁甲, 盾牌, 露肩, 短袍, 袍上发光符文, 法杖发光 | 058–063 | 待核（袍配色） |
| 10 | **术士**（屠宰羔羊地下） | 深兜帽长袍（粗织布，炭黑与暗紫为主、边缘一道暗红缝线，肩上搭厚料短披肩），兜帽压得比法师更低、脸只剩下颌与嘴；无杖时持一本厚皮面书；脚边可有一只齐膝高小鬼。**不是**绿火骷髅的恶魔法师刻板形象 | 绿色火焰特效, 骷髅头饰, 荧光紫瞳, 恶魔角, 露胸紧身装, 铠甲 | 062, 064 | 待核 |
| 11 | **矮人铁匠**（矮人区） | 身高约一米四二、肩宽近身高一半、四肢短粗手掌厚大；无袖粗布衬衣（本白或麻褐，前襟敞开）外罩厚牛皮围裙（深棕，胸口加厚横带、肩带背后交叉、下摆及小腿，布满灼痕）；**必有大胡子**（垂到胸口、粗硬带卷、编一两股用铜环箍住，干活时塞进围裙）；腰上宽皮带挂锤与钳，厚底铁头短靴，脸上薄煤灰。**不是**缩小版的人类比例，也**不是**净面的小个子 | 缩小版人类比例, 净面矮人, 山羊胡, 瘦长矮人, 儿童体型, 全身板甲打铁, 布围裙, 灰皮肤 | 066–068, 073, 076, 078 | 待核（工作服） |
| 12 | **侏儒技师**（矮人区） | 身高约一米零七（头顶到人类腰际）；连体工作服（厚帆布，橄榄褐或铁灰，胸前两只带盖口袋、膝肘有补强皮片、袖口铜扣收紧）外系只到大腿的短皮工具围裙；额头推着黄铜边护目镜（茶色镜片、边缘一圈调节旋钮），腰上宽皮工具带插满钳锉，皮手套指端被烧短；**每只手四指（三指＋拇指）**，耳朵大而圆；发色可为粉或绿（哑光，非荧光）。**不是**戴尖帽的园艺小矮人，也**不是**五指的小个子人类 | 五指的手, 精灵尖耳, 园艺小矮人尖帽, 荧光发色, 长袍, 白大褂, 现代焊接面罩, 太阳镜, 和矮人一样高 | 069–072, 074, 077 | 待核（工作服） |
| 13 | **SI:7 特工**（旧城区） | 连兜帽皮质紧身上衣（哑光鞣革，炭黑与深烟灰拼色，胸前一道斜向缝合线、肩部加厚覆片、腰间宽皮带加两只小扣袋），兜帽压到眉线、脸只剩下颌与嘴；内衬露出一角本白布领，**上面一根短得像线头的红线**；下配深色紧腿裤与无声软底皮靴，腰后交叉两把短匕；重心低、肩收、手不离刀柄。**不是**日式武士刀卡其制服的后期造型，也**不是**铆钉亮面的朋克皮衣 | 武士刀, 胁差, 卡其色制服, 忍者装, 亮面皮衣, 铆钉, 金属护肩, 披风, 露脸, 鲜艳配色, 现代战术背心 | 080–087 | 待核（皮甲分片） |
| 14 | **暗夜精灵德鲁伊**（公园区） | 身高约两米二（比人类高一头半）、四肢修长；紫色谱系皮肤（深兰紫/淡粉紫/蔚蓝/珠光乳白 任选一档锁死）；发色限蔚蓝/紫罗兰/森绿/近白银；**男性有浓密长须与浓眉**，女性有左右对称的风格化爪痕刺青（三道一组，眉骨扫过颧骨，比肤色深一两档、哑光）；瞳孔内透光（女冷银、男暖琥珀，**不外放不投射**）；无袖皮质长身外衣（哑光鞣革，森绿与树皮褐拼色，肩头弧形加厚皮片、腰带缠藤条、下摆前短后长开衩到膝），内衬本色粗麻长袖，小臂缠皮绳，赤足或软底皮履；背上二选一：整张深棕熊皮（带头骨盖肩、前爪胸前交叉系住）／层叠深灰墨绿长羽氅；手持粗木长杖（树皮未剥净、顶端分叉夹一块原石）。**不是**净面的美少年精灵，也**不是**头顶鹿角的树人 | 净面无须, 细眉, 中性少年脸, 头顶鹿角, 藤蔓长在头上, 眼睛射光束, 眼周发光特效, 红瞳, 绿皮, 灰皮, 黑发, 金发, 板甲, 金属护肩, 长剑, 盾牌, 和人类一样高 | 090–102, 105 | 待核（皮甲分片） |
| 15 | **暗夜精灵女祭司**（公园区） | 体型/肤色/发色/眼睛/刺青同上；及地长袍（细织布，午夜蓝底、领口与袖缘一道冷银织纹，两肩各一片薄纱垂到肘），腰束银灰软带，长发脑后挽起、额前一道弧形银饰。**不是**人类教会的白金圣光法衣，也**不是**露肩紧身的西幻女法师装 | 白金圣光法衣, 人类牧师软帽, 露肩紧身, 太阳纹样, 金色为主, 露腿高开衩 | 093, 095–099, 103 | 待核 |

---

## 参考图候选表

> **全部为暴雪版权素材**（游戏截图、模型、官方原画）。
> 用途：**只作形制依据，供人眼核对；一律不入画、不上传给生成模型**（ai_video.md rule 4d ①「图先行、零参考图自由生成」＋版权）。
> 「优先级」列标 ★ 的是本路**必须人眼打开**的三处待核项。

| # | URL | 类型 | 版权 | 证明哪个 fact_id | 能否入画 | 优先级 |
|---|---|---|---|---|---|---|
| 1 | https://www.wowhead.com/classic/npc=68/stormwind-city-guard | Wowhead Classic NPC 页（含 3D Modelviewer） | 暴雪 | 010, 015, **019（头盔面甲）**, 022（肩甲） | ❌ | ★★★ |
| 2 | https://www.wowhead.com/classic/npc=1756/stormwind-royal-guard | Wowhead Classic NPC 页（含 Modelviewer） | 暴雪 | 026, **029（与卫兵差异）**, 027 | ❌ | ★★ |
| 3 | https://warcraft.wiki.gg/wiki/Stormwind_Guard_collection | wiki 图文（含卫兵 vs 复刻套装对比图） | 暴雪 | 020, 021, 022 | ❌ | ★★ |
| 4 | https://warcraft.wiki.gg/wiki/Stormwind_Set | wiki 图库（官方复刻套装 vs 真卫兵并排图） | 暴雪 | 016, 018 | ❌ | ★★ |
| 5 | https://www.wowhead.com/classic/npc=1723/stormwind-citizen | Wowhead Classic NPC 页（含 Modelviewer） | 暴雪 | **032（平民男装）**, **038（平民女装）** | ❌ | ★★★ |
| 6 | https://www.wowhead.com/classic/items/armor/shirts | Wowhead Classic 衬衣列表（含全部平民上衣模型） | 暴雪 | 032, 038 | ❌ | ★★ |
| 7 | https://warcraft.wiki.gg/wiki/Archbishop_Benedictus | wiki 图文（含大灾变前后两张造型对比） | 暴雪 | 049, 050, **051（兜帽 vs 主教冠）** | ❌ | ★★★ |
| 8 | https://warcraft.wiki.gg/wiki/Church_of_the_Holy_Light | wiki 图注（教会徽记在帽子上的那张图） | 暴雪 | 046, **047（徽记形状）** | ❌ | ★★ |
| 9 | https://warcraft.wiki.gg/wiki/Cathedral_of_Light | wiki 图文（教堂内景、钴蓝镶嵌石厅） | 暴雪 | 045, 052 | ❌ | ★ |
| 10 | https://warcraft.wiki.gg/wiki/Mage_Quarter | wiki 图文（法师区与巫师圣殿截图） | 暴雪 | 060, 061, **063（法师袍配色）** | ❌ | ★★ |
| 11 | https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb | wiki 图文（酒馆与地下室截图） | 暴雪 | 062, 064 | ❌ | ★ |
| 12 | https://warcraft.wiki.gg/wiki/Dwarven_District | wiki 图文（矮人区截图、露天锻造场） | 暴雪 | 073, 074, 075, **076（矮人工作服）** | ❌ | ★★ |
| 13 | https://warcraft.wiki.gg/wiki/Dwarf | wiki 图库（矮人模型与原画） | 暴雪 | 066, 067, 068, 078 | ❌ | ★ |
| 14 | https://warcraft.wiki.gg/wiki/Gnome | wiki 图库（侏儒模型与原画） | 暴雪 | 069, **070（四指）**, 071, 072 | ❌ | ★★ |
| 15 | https://warcraft.wiki.gg/wiki/SI:7 | wiki 图文（SI:7 建筑与成员图） | 暴雪 | 082, 083, 084, **087（皮甲分片）** | ❌ | ★★ |
| 16 | https://warcraft.wiki.gg/wiki/Old_Town | wiki 图文（旧城区截图） | 暴雪 | 005, 086 | ❌ | ★ |
| 17 | https://warcraft.wiki.gg/wiki/Park | wiki 图文（Vanilla 公园区与月亮井截图） | 暴雪 | 090, 091, **092（Vanilla 完好状态）**, 093 | ❌ | ★★★ |
| 18 | https://warcraft.wiki.gg/wiki/Night_elf | wiki 图库（肤色/发色/眼色/刺青示例） | 暴雪 | 094–099, 105 | ❌ | ★★ |
| 19 | https://warcraft.wiki.gg/wiki/Nobles_of_Stormwind | wiki 图文（具名贵族立绘） | 暴雪 | 040, 041, **044（贵族华服）** | ❌ | ★★★ |
| 20 | https://warcraft.wiki.gg/wiki/Stormwind_Keep | wiki 图文（王座厅内景与廷臣） | 暴雪 | 028, 042, 043 | ❌ | ★★ |
| 21 | https://warcraft.wiki.gg/wiki/Trade_District | wiki 图文（贸易区街景与商贩） | 暴雪 | 006, 007, 017, 036, 037 | ❌ | ★ |
| 22 | https://www.wowhead.com/classic/item=12427/imperial-plate-helm | Wowhead Classic 装备页（含 Modelviewer） | 暴雪 | 019（**近似**参考，非 NPC 原件） | ❌ | ★ |

**入画替代方案**（按 ai_video.md rule 4d ①）：本片所有参考图资产走**纯文字自由生成**——
用上表 §锁定串总表 的串直接出锚点图，**绝不把暴雪素材喂给生成模型**。
上表只供人眼核对「我写的串对不对」。

---

## 版本错置清单（所有 ❌）

| # | 误画法 | 为什么错 | 正确做法 | 回指 fact_id |
|---|---|---|---|---|
| 1 | **轻甲 / 皮甲卫兵** | RPG 资料书（T2 纸面）说城卫兵「只穿轻甲」，与游戏本体的板甲模型冲突；本项目锚点是游戏本体 | 全身钢灰板甲＋蓝金罩袍 | 024 |
| 2 | **女性卫兵 / 女性皇家卫队** | 女性模型是 4.0.3a（大灾变前夕）才加的，Vanilla 清一色男性 | Vanilla 卫兵岗全为男性；要拍女性从军放冒险者/民兵 | 027 |
| 3 | **大灾变之后的皇家卫队铠甲** | 4.0.3a 加女模型的同时改了铠甲 | 用 1.x 的卫兵同源甲 | 027 |
| 4 | **暴风城海港 / 码头工 / 帆船 / 栈桥** | 海港是 3.0.2（巫妖王之怒前夕）才加的 | 「搬运工」改设在贸易区运河边的驳船与货栈 | 034 |
| 5 | **镀金玫瑰陵园 / 公园区废墟** | 公园区在大灾变才被死亡之翼摧毁，原址后来才建陵园 | Vanilla 公园区完整、绿意盎然、有月亮井 | 092 |
| 6 | **大主教戴主教冠** | 「长袍＋主教冠」是大灾变才换的造型；Vanilla 是戴兜帽的修士形象 | Vanilla 大主教戴兜帽，无冠 | 051 |
| 7 | **SI:7 配武士刀 / 胁差 / 卡其色制服** | 该描述对应 BfA 之后的 SI:7 模型 | Vanilla SI:7 走深色皮甲＋兜帽＋双匕 | 085 |
| 8 | **德莱尼 / 血精灵 / 狼人 / 熊猫人出现在街上** | 德莱尼与血精灵是燃烧的远征（2.x）、狼人是大灾变（4.x）、熊猫人是 5.x | Vanilla 街上只有人类、矮人、侏儒、高等精灵、暗夜精灵 | 001, 104 |
| 9 | **血精灵绿眼** | 血精灵是 2.x 才有的种族 | 高等精灵是蓝光眼 | 104 |
| 10 | **成年瓦里安坐在王座上** | Vanilla 期间瓦里安失踪，博瓦尔摄政、安度因还是孩子 | 王座前是穿板甲的摄政领主与一个孩子 | 043 |
| 11 | **拿玩家装备（Imperial Plate Shoulders）当卫兵肩甲原件** | NPC 肩甲是玩家拿不到的专属模型 | 素净的双层弧形叠片，外沿上翘，无浮雕 | 022 |
| 12 | **贸易区中心的拍卖行**（若设定在开服初期） | 拍卖行是 1.9 才加进贸易区中心的 | 按本站选定的 1.x 时点决定有无 | 007 |
| 13 | **卫兵披红披风** | 复刻指南明确「卫兵不穿披风」 | 背后空无一物 | 021 |
| 14 | **暗夜精灵头顶鹿角** | 鹿角在 wiki 里是独立的特例小节，不是通例 | 公园区的普通暗夜精灵不长鹿角 | 105 |
| 15 | **暗夜精灵男性净面** | 与其他精灵族不同，暗夜精灵男性常有浓密胡须与浓眉 | 浓密长须＋浓眉 | 098 |
| 16 | **暗夜精灵眼睛向外射光 / 眼周光斑** | 设定是眼球「发出银或金的光辉」，是内透光不是灯 | 虹膜自发光、亮度低于环境光、不投射不拖尾 | 096 |
| 17 | **侏儒画五根手指** | 侏儒每只手四指（三指＋拇指） | 手部入画的镜显式写四指 | 070 |
| 18 | **净面矮人 / 山羊胡矮人** | 矮人男性「always have beards」，且通常又长又野 | 垂到胸口的粗硬大胡子 | 067 |
| 19 | **把矮人画成缩小版人类** | 矮人是 squat and powerfully built，肩宽近身高一半 | 四肢短粗、手掌厚大、头身比明显不同于人类 | 066 |
| 20 | **红底 / 黑底 / 银狮纹章** | 暴风城纹章是蓝底金狮；黑底红拳是斯托颂（Stromgarde） | 群青蓝底＋金黄狮首 | 003 |
| 21 | **白底红十字的十字军罩袍** | 那是地球中世纪的形象，不是暴风城 | 蓝底金狮罩袍 | 003, 018 |
| 22 | **神职穿紫袍 / 红衣主教红袍** | 圣光教会的高阶法衣是白金 | 象牙白＋金黄织锦 | 049 |

---

## 未查 / Open questions

> 按优先级排序。前三项是本路的**主要缺口**，均因「全网文字来源都没写视觉细节」而非「没找」。

1. **★★★ 卫兵头盔的确切形制**（fact 019）——是否全覆面？观察缝是横条还是 T 形？有无羽饰？
   文字来源只有 "the iconic plate helm" 一句。**必须开参考图 #1 的 Modelviewer 人眼核**。
2. **★★★ 平民男装与女装的确切形制**（fact 032 / 038）——领口、系法、裙型、围裙、头巾。
   Warcraft Wiki 的「Human」页只写军装，「Commoner」页只写职业。**必须开参考图 #5 / #6 人眼核**。
3. **★★★ 贵族华服的确切形制**（fact 044）——wiki 明说「contains no specific descriptions of noble clothing」。
   **必须开参考图 #19 / #20 人眼核**。
4. **★★ 圣光徽记的确切形状**（fact 047）——只知道「戴在大主教的帽子上」，形状本身无描述。
   开参考图 #8 的那张图注截图。
5. **★★ Vanilla 大主教兜帽上有没有徽记**——047 的图注取自大灾变之后的造型，
   Vanilla 的兜帽版是否也有徽记、在什么位置，未查。
6. **★★ 皇家卫队与城市卫兵的具体差异**（fact 029）——除「更精英、守要塞」外无任何形制描述；
   Wowhead 上的相关 outfit 全是玩家 transmog（T4），不能当依据。
7. **★★ 法师袍与术士袍的配色**（fact 063 / 064）——只知道「只能穿布甲」。
   法师区具名训练师（Archmage Malin / Nakada）各自穿什么，未查。
8. **★ 矮人的肤色与瞳色**（fact 078）——Warcraft Wiki 的矮人外观段明确缺失。
9. **★ 矮人与侏儒工匠的工作服**（fact 076 / 077）——只有「护目镜、工具腰带」一句有据，其余为推定。
10. **★ SI:7 特工皮甲的 Vanilla 形制**（fact 087）——wiki 唯一具体的一句（武士刀＋卡其制服）是后期版本。
11. **★ Vanilla 公园区的暗夜精灵训练师各自穿什么**（fact 102 / 103）——只有名字与职业，无外观。
12. **★ 高等精灵在 Vanilla 暴风城的具体出现位置与装束**（fact 104）——只知道「住在城里」。
13. **技术限制说明**：Wowhead 的 3D Modelviewer 与 NPC 装备列表是 JS 渲染的，
    抓取只能拿到文字壳（对白、地点），拿不到模型与装备槽。
    **本轮所有「T0 游戏本体」级别的核验都必须由人在浏览器里完成**，无法由本路补齐。

---

## 来源（分级）

**T1 — warcraft.wiki.gg 带游戏内 / 小说引用的段落**
- Stormwind City Guard（组织） https://warcraft.wiki.gg/wiki/Stormwind_City_Guard ／原始 wikitext https://warcraft.wiki.gg/index.php?title=Stormwind_City_Guard&action=raw
- Stormwind City Guard (NPC) https://warcraft.wiki.gg/wiki/Stormwind_City_Guard_(NPC)
- Stormwind Royal Guard (NPC) https://warcraft.wiki.gg/wiki/Stormwind_Royal_Guard_(NPC)
- Stormwind Guard collection https://warcraft.wiki.gg/wiki/Stormwind_Guard_collection
- Stormwind Set https://warcraft.wiki.gg/wiki/Stormwind_Set
- Stormwind Tabard https://warcraft.wiki.gg/wiki/Stormwind_Tabard
- Hall of Justice（蓝底金狮旗原文） https://warcraft.wiki.gg/wiki/Hall_of_Justice
- Icon of Courage https://warcraft.wiki.gg/wiki/Icon_of_Courage
- Footman https://warcraft.wiki.gg/wiki/Footman
- Stormwind Keep https://warcraft.wiki.gg/wiki/Stormwind_Keep
- Nobles of Stormwind https://warcraft.wiki.gg/wiki/Nobles_of_Stormwind
- Cathedral of Light https://warcraft.wiki.gg/wiki/Cathedral_of_Light
- Church of the Holy Light https://warcraft.wiki.gg/wiki/Church_of_the_Holy_Light
- Archbishop Benedictus https://warcraft.wiki.gg/wiki/Archbishop_Benedictus
- Mage https://warcraft.wiki.gg/wiki/Mage ／ Mage Quarter https://warcraft.wiki.gg/wiki/Mage_Quarter
- The Slaughtered Lamb https://warcraft.wiki.gg/wiki/The_Slaughtered_Lamb
- Rogue https://warcraft.wiki.gg/wiki/Rogue ／ SI:7 https://warcraft.wiki.gg/wiki/SI:7 ／ Old Town https://warcraft.wiki.gg/wiki/Old_Town
- Dwarf https://warcraft.wiki.gg/wiki/Dwarf ／ Gnome https://warcraft.wiki.gg/wiki/Gnome ／ Dwarven District https://warcraft.wiki.gg/wiki/Dwarven_District
- Night elf https://warcraft.wiki.gg/wiki/Night_elf ／原始 wikitext https://warcraft.wiki.gg/index.php?title=Night_elf&action=raw
- The Warcraft Encyclopedia/Night Elves https://warcraft.wiki.gg/wiki/The_Warcraft_Encyclopedia/Night_Elves
- Druid https://warcraft.wiki.gg/wiki/Druid ／ Park https://warcraft.wiki.gg/wiki/Park
- Human https://warcraft.wiki.gg/wiki/Human ／原始 wikitext https://warcraft.wiki.gg/index.php?title=Human&action=raw
- Commoner https://warcraft.wiki.gg/wiki/Commoner
- Trade District https://warcraft.wiki.gg/wiki/Trade_District ／ Stormwind Harbor https://warcraft.wiki.gg/wiki/Stormwind_Harbor
- Stormwind City https://warcraft.wiki.gg/wiki/Stormwind_City
- Wowhead Classic 装备页：Imperial Plate Helm https://www.wowhead.com/classic/item=12427/imperial-plate-helm

**T2 — 有出处的美术考据**
- Engadget《Transmogrifying your way into the Stormwind Guard》（2012-01-05） https://www.engadget.com/2012-01-05-transmogrifying-your-way-into-the-stormwind-guard.html
- Warcraft RPG 线（经 wiki 转述）：Stormwind City 的「城卫兵只穿轻甲」「圣骑士城内只穿胸甲」两句

**T4 — 玩家 transmog 复刻（只作反例 / 构图旁证，不得当形制依据）**
- Wowhead Classic「Stormwind guard」outfit https://www.wowhead.com/classic/outfit=207747/stormwind-guard
- Wowhead TBC「Stormwind Royal guard」outfit https://www.wowhead.com/tbc/outfit=221485/stormwind-royal-guard
- Wowhead Classic「Footman of Stormwind」outfit https://www.wowhead.com/classic/outfit=263014/footman-of-stormwind
- Wowhead Classic「Stormwind Citizen」outfit https://www.wowhead.com/classic/outfit=16842/stormwind-citizen
- Wowhead Classic「Stormwind Noble」outfit https://www.wowhead.com/classic/outfit=202135/stormwind-noble
- Wowhead「Human Kingdoms - Stormwind - commoner/peasant/noble/royalty」系列（作者 Nicholac） https://www.wowhead.com/cata/outfit=185916/human-kingdoms-stormwind-commoner

**抓取失败 / 付费墙（下轮补）**
- vanilla-wow-archive.fandom.com「Stormwind City」（HTTP 402）
- wowpedia.fandom.com「Stormwind (kingdom)」（HTTP 402）
- Wowhead 3D Modelviewer 与 NPC 装备槽（JS 渲染，抓取只得文字壳）——**须人眼在浏览器完成**
