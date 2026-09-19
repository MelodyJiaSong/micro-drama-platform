---
worker_id: researcher-w5-people-glossary
stage: 0
role: researcher
angle: people-glossary
status: complete
blockers: []
confidence: medium
---

# W5 · 暴风城可观察人物 / 称谓 / 中英译名表

**版本锚点：经典旧世 Vanilla（WoW 1.x / Classic Era，大地的裂变之前）。**
**形态铁律：当地人零台词。** 本文只回答「镜头能看到他在做什么」，不写任何当地人的话。

## 本路最重要的三条结论（先读）

1. **Vanilla 的王座上坐的是 10 岁的男孩王 安杜因·乌瑞恩**，**瓦里安·乌瑞恩当时失踪在外、不在暴风城**。
   实际掌权的是摄政 **大领主伯瓦尔·弗塔根**，王座右侧站着 **卡特拉娜·普瑞斯托女士**（真身是黑龙奥妮克希亚）。
   把瓦里安放上王座 = 版本错置（那是 3.0.2 之后的事）。
2. **Vanilla 的暴风城没有港口。** 「暴风城港口」是补丁 3.0.2（2008-10-14，巫妖王之怒）才加的。
   本站脚本里**不能有码头、货船、栈桥、仓库工**。要拍「水边劳作」只能拍**运河**与运河边的商铺、钓鱼人。
3. **Deeprun Tram 的官方中文是「矿道地铁」，不是「深铁矿道」。** 立项 brief 里的写法需要改。

---

## 事实注册表

```yaml
# ============ 王座与宫廷 ============
- fact_id: stormwind.person.001
  claim: Vanilla 时期暴风城王座上的是 10 岁的男孩王安杜因·乌瑞恩，他在父亲失踪期间被加冕看守王国。
  tag: ✅
  source: Warcraft Wiki — Throne room
  source_url: https://warcraft.wiki.gg/wiki/Throne_room
  quote: "his ten-year-old son Anduin watched over the city, aided in his rule by Lady Katrana Prestor and Highlord Bolvar Fordragon"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "暴风要塞圆顶王座厅中轴线尽头，两侧金狮环抱的石质王座（Lion Seat）上，端坐一名约十岁的金发男孩，蓝白两色带金边的小号王室长袍，肩上披短斗篷，双手放在扶手上，身形小得撑不满椅背，脚够不到地面；他不说话，只是坐着，偶尔转头看向站在旁边的两个大人"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 成年国王, 络腮胡国王, 空王座, 王座上坐着壮年男子"

- fact_id: stormwind.person.002
  claim: 安杜因·乌瑞恩在 1.12 简体中文客户端里的官方译名是「安杜因·乌瑞恩」，NPC 等级 5 级；现行零售版官方译名已改为「安度因·乌瑞恩」。
  tag: ✅
  source: NFU 1.12 中文数据库 NPC 1747 / Wowhead Classic npc=1747
  source_url: https://db.nfuwow.com/60/?npc=1747
  quote: "中文名：安杜因·乌瑞恩 / 英文名：Anduin Wrynn / 等级：5"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（译名字幕用）口播写「安杜因」，字面与 Vanilla 客户端一致；若统一到现行官方版本则写「安度因」，二选一后全剧锁死不得混用"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 同一集里两种译名混用"

- fact_id: stormwind.person.003
  claim: 大领主伯瓦尔·弗塔根是 Vanilla 暴风城的实际摄政与军队统帅，代男孩王安杜因行使权力，位置在暴风要塞中央王座厅、男孩王身侧。
  tag: ✅
  source: Warcraft Wiki — Bolvar Fordragon
  source_url: https://warcraft.wiki.gg/wiki/Bolvar_Fordragon
  quote: "Regent Lord of Stormwind or the Supreme Commander of Stormwind's forces on behalf of King Anduin"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座台阶下方偏左，一名高大壮年男性人类立定，全身抛光板甲，胸甲正中一枚狮首浮雕，外披深蓝底金狮纹罩袍（tabard），金褐色短发与修剪过的短须，左手扣在腰侧剑柄上，右手垂在身侧，身体正面朝厅门方向——他是全厅唯一直视来客的人，站姿不动如钉"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 亡灵化, 巫妖王形象, 焦黑铠甲, 头盔冒火"

- fact_id: stormwind.person.004
  claim: 伯瓦尔·弗塔根的 1.12 简体中文官方译名为「大领主伯瓦尔·弗塔根」（注意是「伯」不是「博」）。
  tag: ✅
  source: NFU 1.12 中文数据库 NPC 1748
  source_url: https://db.nfuwow.com/60/?npc=1748
  quote: "中文名：大领主伯瓦尔·弗塔根 / 英文名：Highlord Bolvar Fordragon"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（译名字幕用）「大领主伯瓦尔·弗塔根」，Highlord 官方译作「大领主」"
  negative: "博瓦尔, 弗塔跟, 弗坦根, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.person.005
  claim: 卡特拉娜·普瑞斯托女士是王室顾问，站位紧贴男孩王右侧；其真身是死亡之翼之女、黑龙奥妮克希亚。
  tag: ✅
  source: Warcraft Wiki — Katrana Prestor
  source_url: https://warcraft.wiki.gg/wiki/Katrana_Prestor
  quote: "stood immediately to the right of the boy king"; "a form that would quicken their heartbeats"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座右侧半步处，一名身形高挑的成年女性人类贵族，深色长发盘束，一袭深紫近黑的曳地长裙、袖口与领缘金线绣纹，双手在身前交叠，下颌微抬、眼神向下扫视厅内，整个人比宫廷里任何人都更放松——她不看男孩，只看进厅的人"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 变身龙形, 龙翼, 龙角, 鳞片, 发光眼睛"

- fact_id: stormwind.person.006
  claim: 卡特拉娜·普瑞斯托的 1.12 简体中文官方译名为「卡特拉娜·普瑞斯托女士」。
  tag: ✅
  source: NFU 1.12 中文数据库 NPC 1749
  source_url: https://db.nfuwow.com/60/?npc=1749
  quote: "中文名：卡特拉娜·普瑞斯托女士 / 英文名：Lady Katrana Prestor"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（译名字幕用）「卡特拉娜·普瑞斯托女士」——Lady 在官方译名里直接后缀为「女士」，不译作「夫人」"
  negative: "普雷斯托夫人, 卡崔娜, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.person.007
  claim: 瓦里安·乌瑞恩国王在 Vanilla 期间失踪、不在暴风城——他是在前往塞拉摩外交会晤途中「在可疑情况下失踪」的。
  tag: ✅
  source: Warcraft Wiki — Varian Wrynn
  source_url: https://warcraft.wiki.gg/wiki/Varian_Wrynn
  quote: "After King Varian Wrynn went missing under suspicious circumstances while en route to a diplomatic summit to Theramore Isle, Stormwind was believed to be going through a state of disarray."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例锁定）本站任何镜头里都不得出现瓦里安：不得出现壮年长发国王、不得出现双持巨剑的王者、王座上不得坐成年人"
  negative: "瓦里安, 成年国王坐在王座上, 长发披肩的壮年国王, 双持巨剑, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.person.008
  claim: 补丁 3.0.2 把伯瓦尔与卡特拉娜从暴风要塞移除、换上瓦里安国王——这条补丁记录反证了二人在 Vanilla 期间确实站在要塞里。
  tag: ✅
  source: Warcraft Wiki — Patch 3.0.2 (undocumented changes)
  source_url: https://warcraft.wiki.gg/wiki/Patch_3.0.2_(undocumented_changes)
  quote: "Bolvar Fordragon and Katrana Prestor have been removed from Stormwind Keep, and King Varian Wrynn has been added in their place."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（版本闸门）王座厅三人组＝男孩王 + 伯瓦尔 + 普瑞斯托；这是 Vanilla 的唯一正确组合"
  negative: "瓦里安在王座厅, 图拉扬摄政, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.person.009
  claim: 同一补丁 3.0.2 才给安杜因挂上「Prince of Stormwind（暴风城王子）」头衔——在 Vanilla 他的身份是被加冕的国王，不是王子。
  tag: ✅
  source: Warcraft Wiki — Patch 3.0.2 (undocumented changes)
  source_url: https://warcraft.wiki.gg/wiki/Patch_3.0.2_(undocumented_changes)
  quote: "Anduin Wrynn now bears the title 'Prince of Stormwind'."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（称谓闸门）本站口播称安杜因为「男孩王 / the boy king」或「安杜因国王」，绝不称「王子」"
  negative: "安杜因王子, Prince Anduin, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.person.010
  claim: 德拉维主教代表教会常驻暴风要塞的「请愿厅（Petitioner's Chamber）」，坐标 [80.6, 34.8]，处理宫廷事务。
  tag: ✅
  source: Warcraft Wiki — Bishop DeLavey
  source_url: https://warcraft.wiki.gg/wiki/Bishop_DeLavey
  quote: "Bishop DeLavey is a human of the Church of the Holy Light found in the Petitioner's Chamber of Stormwind Keep."; "[80.6, 34.8]"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "暴风要塞进门后的请愿厅一侧，一名中年男性人类立于石柱旁，白底金边的教会长袍、胸前一枚圣光徽记，双手交握于腹前，脚下是抛光石地与蓝金地毯，身后有排队等候的请愿平民背影"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 主教手持武器, 主教在户外"

# ============ 教堂广场 ============
- fact_id: stormwind.person.011
  claim: 大主教本尼迪塔斯在 Vanilla 位于教堂广场的大教堂内，是圣光教会最高神职，训练联盟年轻牧师。
  tag: ✅
  source: Warcraft Wiki — Archbishop Benedictus
  source_url: https://warcraft.wiki.gg/wiki/Archbishop_Benedictus
  quote: "trained young priests of the Alliance in the way of the Holy Light"; "a soft-spoken man of average height and stocky build who looks more like a farmer than a religious leader"; "slightly ill at ease in his splendid white and gold robes"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "大教堂中殿尽头的高坛前，一名中等身高、体格敦实的中年男性人类，白底大面积金线刺绣的华贵主教长袍，头戴无沿白金主教冠，肩上垂长披带，双手扶在讲经台边缘；面相朴实近似农夫，整个人被彩窗透下的斜光罩住，站在那里不动"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 暮光之锤装束, 黑袍, 兜帽遮脸, 反派化"

- fact_id: stormwind.person.012
  claim: 大主教本尼迪塔斯的 1.12 简体中文官方译名为「大主教本尼迪塔斯」。
  tag: ✅
  source: NFU 1.12 中文数据库 NPC 1284
  source_url: https://db.nfuwow.com/60/?npc=1284
  quote: "中文名：大主教本尼迪塔斯 / 英文名：Archbishop Benedictus"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（译名字幕用）「大主教本尼迪塔斯」，Archbishop 官方译作「大主教」"
  negative: "贝内迪克图斯, 本尼迪克特, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.person.013
  claim: 高阶牧师劳瑞娜是暴风城最高阶的牧师训练师（60 级），常驻光明大教堂。
  tag: ✅
  source: Warcraft Wiki — Cathedral of Light；NFU 1.12 中文数据库 NPC 376
  source_url: https://db.nfuwow.com/60/?npc=376
  quote: "中文名：高阶牧师劳瑞娜 / 英文名：High Priestess Laurena"；wiki: "the highest-ranking priest trainer in Stormwind City"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "大教堂侧翼回廊，一名成年女性人类身着白金牧师长袍、肩披白色圣带，站在一排跪坐祈祷的年轻牧师学徒前方，一手抬起做引导手势，一手托着一本翻开的厚书，身后是高窄彩窗与烛台"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 施放攻击法术, 战斗姿态"

- fact_id: stormwind.person.014
  claim: 格雷森·破影者领主是暴风城首席圣骑士、60 级圣骑士训练师，位于教堂广场的大教堂。
  tag: ✅
  source: Warcraft Wiki — Cathedral of Light；NFU 1.12 中文数据库 NPC 928
  source_url: https://db.nfuwow.com/60/?npc=928
  quote: "中文名：格雷森·破影者领主 / 英文名：Lord Grayson Shadowbreaker / 圣骑士训练师"；wiki: "one of the foremost human paladins of the Alliance and the chief paladin in Stormwind"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "大教堂另一侧翼，一名壮年男性人类穿整套白银板甲、肩甲高耸带金饰，无头盔，短发，一柄战锤靠在他身旁的立架上，他双臂抱胸站在一面圣光旗帜下，面朝几名穿链甲的年轻见习骑士"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 骑马进教堂, 挥舞武器"

- fact_id: stormwind.job.001
  claim: 光明大教堂位于教堂广场，是圣光教会最醒目的纪念建筑，钴蓝镶嵌石厅、多翼多尖塔、地下有墓室与地窟，也是全城疗伤中心。
  tag: ✅
  source: Warcraft Wiki — Cathedral of Light
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "the most striking monument of the Church of the Holy Light"; "cobalt-inlaid stone halls"; "the center of all healing practices in the city"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "广场仰角：巨大的白石教堂正立面，中央高拱门、两侧对称尖塔，墙面嵌钴蓝色石饰，正门前宽石阶上零星站着白袍神职与受伤的平民，鸽群从塔尖起飞"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 哥特式滴水兽, 地球教堂十字架, 现代玻璃幕墙"

# ============ 英雄谷 / 城门 ============
- fact_id: stormwind.person.015
  claim: 马库斯·乔纳森将军是 Vanilla 的「暴风城防务最高指挥官」，站在英雄谷，坐标 [69, 83]，对玩家的固定招呼是「Greetings, citizen」。
  tag: ✅
  source: Warcraft Wiki — Marcus Jonathan
  source_url: https://warcraft.wiki.gg/wiki/Marcus_Jonathan
  quote: "High Commander of Stormwind Defense"; "Valley of Heroes within Stormwind City at coordinates [69, 83]"; "Greetings, citizen"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "英雄谷石桥中段，一名壮年男性人类骑在一匹披蓝金马衣的白色战马上，全身银亮板甲、外罩狮纹罩袍，无头盔或头盔夹在臂弯，缰绳握在左手，马原地小幅踏步；他两侧是高耸的第二次战争英雄石像与长条形水面"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 步行的将军, 现代马术装备, 马镫反光过曝"

- fact_id: stormwind.person.016
  claim: 马库斯·乔纳森将军的简体中文官方译名为「马库斯·乔纳森将军」。
  tag: ⚠️
  source: WowDB 中文数据库 暴风城区域 NPC 列表（区域 1519）
  source_url: http://www.wowdb.cn/zone-1519.html
  quote: "马库斯·乔纳森将军"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（译名字幕用）「马库斯·乔纳森将军」"
  negative: "马库斯·约翰逊, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.job.002
  claim: 英雄谷是暴风城唯一的入城通路，谷中立有第二次战争英雄的纪念石像，每一个来访者都必须穿过它。
  tag: ✅
  source: Warcraft Wiki — Stormwind City；中文来源：百度百科 暴风城
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Valley of Heroes - Entry area beyond city gates; memorial statues of Second War heroes"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "入城长镜：两侧各三尊数层楼高的石制人类英雄立像夹出一条笔直大道，中间是狭长水道与石桥，尽头是高耸的白石城门与两座塔楼，人流与马匹在桥面上双向通过"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 现代雕塑, 抽象雕塑, 空无一人的城门"

# ============ 贸易区 ============
- fact_id: stormwind.person.017
  claim: 杜加尔·朗德瑞克是暴风城的狮鹫兽管理员（55 级），位于贸易区东侧的狮鹫栖木，坐标 [71.0, 72.6]；他是人类，却说一口矮人腔。
  tag: ✅
  source: Warcraft Wiki — Dungar Longdrink；NFU 1.12 中文数据库 NPC 352
  source_url: https://warcraft.wiki.gg/wiki/Dungar_Longdrink
  quote: "Gryphon Roost at coordinates [71.0, 72.6]"; "despite being human, he speaks with a dwarven accent"；NFU: "杜加尔·朗德瑞克 <狮鹫兽管理员>"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区东侧一座半开放的石砌高台栖木，一名中年男性人类穿厚皮飞行服与护目镜（护目镜推在额头上），腰挂皮质飞行绳具，一手托着一副缰辔，一手抚在一只伏地收翅的巨型狮鹫颈羽上；台上并排停着两三只狮鹫，羽毛被风吹动"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 狮鹫起飞喷火, 现代滑翔装备, 狮鹫是纯狮子或纯鹰"

- fact_id: stormwind.person.018
  claim: 旅店老板奥里森（Innkeeper Allison）经营贸易区的「镀金玫瑰」旅店，位置夹在银行与拍卖行之间，坐标 [60.6, 75.0]，30 级。
  tag: ✅
  source: Warcraft Wiki — Innkeeper Allison；NFU 1.12 中文数据库 NPC 6740
  source_url: https://warcraft.wiki.gg/wiki/Innkeeper_Allison
  quote: "operates the Gilded Rose inn in Stormwind City's Trade District, positioned between the bank and auction house at coordinates [60.6, 75.0]"；NFU: "旅店老板奥里森 <旅馆老板>"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旅店一层柜台后，一名成年女性人类穿米白束腰长裙加深色围裙，头发在脑后挽起，双手正把一排陶质酒杯从托盘摆到木柜台上；她身后是酒桶架与挂着铜壶的墙，柜台一侧堆着面包与水果，壁炉在画面深处发暖光"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 现代吧台, 玻璃酒瓶, 霓虹招牌"

- fact_id: stormwind.person.019
  claim: 贸易区中央的「商人大厅（Trader's Hall）」内是拍卖行；Vanilla 的拍卖师包括拍卖师希尔顿（50 级）、拍卖师费奇、拍卖师亚克森。
  tag: ✅
  source: Warcraft Wiki — Trade District；NFU 1.12 中文数据库 NPC 8670；WowDB 中文 区域 1519
  source_url: https://db.nfuwow.com/60/?npc=8670
  quote: "中文名：拍卖师希尔顿 / 英文名：Auctioneer Chilton"；wiki: "Trader's Hall houses the Auction House in the district's center"；WowDB: "拍卖师费奇""拍卖师亚克森""拍卖师希尔顿"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "拍卖行厅内，一排三名穿深色马甲配白衬衫的成年人类站在一条长木台后，每人面前一本摊开的厚账簿与一枚铜铃，手里捏着羽毛笔在纸上划记；台前挤着背包鼓胀的各族来客，墙上钉满写满字的羊皮纸告示"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 拍卖槌敲击声画, 现代柜台, 电子屏"

- fact_id: stormwind.person.020
  claim: 伊林·提亚斯（30 级）在贸易区开「提亚斯的奶酪店」，坐标 [66.1, 74.2]，表面是乳酪商，实为情报网节点、与军情七处有联系。
  tag: ✅
  source: Warcraft Wiki — Elling Trias；NFU 1.12 中文数据库 NPC 482
  source_url: https://warcraft.wiki.gg/wiki/Elling_Trias
  quote: "Elling Trias is a Human Rogue who owns Trias' Cheese shop in Stormwind City's Trade District"; "[66.1, 74.2]"; "an extensive web of contacts, stretching from SI:7 to agents"；NFU: "伊林·提亚斯 <乳酪商>"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河边一间窄门面奶酪铺，一名中年男性人类穿深绿罩衫配皮围裙，正把一只车轮状的大奶酪抱上柜台、另一只手握一把宽刃奶酪刀；铺内货架上层层码着不同大小的奶酪轮，门口挂着成串洋葱与麻绳"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 匕首出鞘, 潜行动作, 现代冷柜"

- fact_id: stormwind.job.003
  claim: 贸易区就在暴风城正门内侧，包含银行「暴风城银号（Stormwind Counting House）」、拍卖行、镀金玫瑰旅店、狮鹫栖木、接待中心与一长串专门店铺（军械、药剂、裁缝、珠宝、花店、酒庄等）。
  tag: ✅
  source: Warcraft Wiki — Trade District
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The Stormwind Counting House serves as the bank"; "The Gilded Rose functions as the inn"; "The Gryphon Roost on the east side"; "Canal-side shops include the Canal Tailor and Fit Shop, Denman Family Jewelers, Fragrant Flowers, and Gallina Winery"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区全景：石板广场中央一圈围着运河的半月形街面，两三层高的白墙蓝顶木筋建筑连成一排，每间门口挂铁艺行业招牌（剪刀、酒杯、宝石、面包），人流密集、各族混杂，马车与推车沿石板路穿行"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 现代店招, 玻璃橱窗, 电线, 柏油路"

# ============ 旧城区 / 军情七处 ============
- fact_id: stormwind.person.021
  claim: 马迪亚斯·肖尔（62 级）是暴风城情报机构军情七处（SI:7）的首脑，以旧城区兵营为据点。
  tag: ✅
  source: Warcraft Wiki — Mathias Shaw；NFU 1.12 中文数据库 NPC 332
  source_url: https://warcraft.wiki.gg/wiki/Mathias_Shaw
  quote: "Shaw is based in the SI:7 barracks located in Old Town, Stormwind City"; "from his base of operations in the barracks of Old Town"；NFU: "中文名：马迪亚斯·肖尔 / 英文名：Master Mathias Shaw / 等级：62"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旧城区一间无窗石屋内，一名中年男性人类穿深褐色贴身皮甲、外披暗色短披风，红褐短发与修剪短须，背对门口俯身在一张摊满地图与信件的方桌上，双手撑在桌沿，腰后交叉别着两把匕首；桌上一盏油灯是全屋唯一光源"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 明亮室内, 隐身特效, 拔刀攻击"

- fact_id: stormwind.job.004
  claim: 旧城区是暴风城最老的一片，街道比别处更脏更臭，是穷人、乞丐与窃贼聚集的居住区；其中有军情七处、指挥中心（军官据点）与「猪和哨声酒馆」。
  tag: ✅
  source: Warcraft Wiki — Old Town
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "the streets are described as far dirtier and smellier than the other districts"; "the residential area for most of the poor folk of the city, as beggars, thieves, and poor people can be found there"; "Pig and Whistle Tavern"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旧城区窄巷：两侧木筋老屋向内倾斜几乎遮住天空，墙面木料发黑、抹灰剥落，地面石板不平且有积水，晾衣绳横跨巷子，墙根坐着裹旧毯的乞丐，酒馆木门上方挂一块画着猪的铁皮招牌"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 干净整洁的街道, 明亮宽阔广场, 现代垃圾桶"

- fact_id: stormwind.person.022
  claim: 典狱官塞尔沃特（30 级）是暴风城监狱（Stockade）方面的典狱官 NPC。
  tag: ✅
  source: NFU 1.12 中文数据库 NPC 1719；Wowhead Classic npc=1719
  source_url: https://db.nfuwow.com/60/?npc=1719
  quote: "中文名：典狱官塞尔沃特 / 英文名：Warden Thelwater / 等级：30"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河下方一处圆形石井口旁，一名中年男性人类穿暗色链甲配皮护腕，腰间挂一大串铁钥匙，一手提着铁栅门把手，一手举油灯照向井下的下行阶梯；他脚边是铁链与一只空锁具"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 现代制服, 手铐, 电筒"

# ============ 矮人区 / 矿道地铁 ============
- fact_id: stormwind.person.023
  claim: 瑟鲁姆·深炉（33 级）是矮人区的锻造训练师，坐标 [63.6, 37.7]。
  tag: ✅
  source: Warcraft Wiki — Dwarven District；NFU 1.12 中文数据库 NPC 5511
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "Therum Deepforge (Blacksmithing trainer) at coordinates [63.6, 37.7]"；NFU: "中文名：瑟鲁姆·深炉 / 英文名：Therum Deepforge / 锻造训练师 / 等级：33"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "矮人区露天锻炉旁，一名矮人男性（身高约到人类腰胸之间、体宽、络腮大胡编成辫）穿厚皮围裙与护臂，赤裸的前臂沾着黑灰，右手抡一把短柄铁锤砸在铁砧上的红热坯料上，左手用长柄铁钳夹住坯料；火星从砧面弹起后加速下坠、落地即灭"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 火星慢动作, 火星匀速飘浮, 火星滞空, 人类身高的矮人, 无胡须矮人"

- fact_id: stormwind.person.024
  claim: 矮人区另有工程学训练师莉莲·闪轴（Lilliam Sparkspindle，工程学手推车旁 [63.0, 31.6]）与猎人训练师乌尔菲尔·铁须（Ulfir Ironbeard，[67.3, 36.9]）。
  tag: ✅
  source: Warcraft Wiki — Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "Lilliam Sparkspindle (Engineering trainer) at the engineering cart [63.0, 31.6]"; "Ulfir Ironbeard (Hunter trainer) at [67.3, 36.9]"
  tier: ⚠️T1（中文译名未查到官方对应，暂留英文）
  verified_by: ai_read
  used_in: []
  prompt_string: "工程学手推车：一辆两轮木车上堆满黄铜齿轮、发条盒、铜管与螺栓，车旁站一名侏儒（身高仅到人类大腿、大鼻子、鲜艳发色），戴护目镜，正拧一只冒白气的小型装置；不远处一名蓄长灰须的矮人扶着一把长弓，脚边卧着一只巨熊"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 装置爆炸, 现代电子元件, 人类身高的侏儒"

- fact_id: stormwind.job.005
  claim: 矮人区的锻炉「持续冒出烟霾」，并且「持续响着铁匠锤击」；这里集中了采矿、锻造、工程学训练与猎人公会。
  tag: ✅
  source: Warcraft Wiki — Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The forges in the district produce a constant haze, supplemented by the constant strokes of smiths' hammers."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "矮人区街景：低矮厚重的石砌建筑、圆拱门与铜皮屋顶，街面上并排三四座露天锻炉，每座上方一股稳定上升的灰白烟柱把天光滤成暖褐色；矮人与侏儒在炉间往来搬运铁料，空气里有悬浮的细尘颗粒"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 无烟的锻炉, 冷蓝色调, 现代工厂烟囱"

- fact_id: stormwind.job.006
  claim: 矮人们是在第二次战争后由麦格尼·铜须国王派工匠来暴风城重建城市而留下的，矮人区就是为安置这些工人而建；侏儒因工程学专长随之聚居。
  tag: ✅
  source: Warcraft Wiki — Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "King Magni [sent] workers...to house all the workers sent by King Magni"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播支撑事实，无需专门镜头；可配矮人区人群镜）"
  negative: "开口说话, 清晰可辨的对白, 路人对口型"

- fact_id: stormwind.job.007
  claim: Deeprun Tram 是连接铁炉堡与暴风城的全封闭地下双轨铁路，跑两组三节车厢，暴风城这一端的入口在矮人区；单程 60 秒，每站停 12 秒，免费。
  tag: ✅
  source: Warcraft Wiki — Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "a long, fully enclosed, underground (and partially underwater) set of double tracks upon which rolls two sets of three wagons"; "transit time between each end is 60 seconds and remains at each stop for 12 seconds"; "the entrance is located in the Dwarven District"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "地下车站：一条笔直没入黑暗的双轨隧道，月台是铆接铁板与黄铜栏杆，墙上嵌着发光的圆形仪表盘；一列三节的封闭铁皮车厢停靠在轨上，车门开着，车身满是铆钉与锈迹；隧道中段可见一段透明穹顶外是深色湖水"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 现代地铁, LED屏, 自动闸机, 蒸汽机车烟囱"

- fact_id: stormwind.job.008
  claim: Deeprun Tram 的官方简体中文译名是「矿道地铁」；它由大工匠格尔宾·梅卡托克受麦格尼·铜须国王之托设计，每天有侏儒在上面维护。
  tag: ✅
  source: 魔兽世界中文维基（灰机）— 矿道地铁
  source_url: https://warcraft.huijiwiki.com/wiki/%E7%9F%BF%E9%81%93%E5%9C%B0%E9%93%81
  quote: "矿道地铁是一组长而全封闭的地下双轨铁路，运行着两组三节车厢，免费提供给穿行于联盟城市铁炉堡和暴风城之间的旅者"；"大工匠格尔宾·梅卡托克受麦格尼·铜须国王的委托，设计了这个连接暴风城和铁炉堡的宏伟地下铁路系统"
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: "（译名字幕用）「矿道地铁 / Deeprun Tram」——立项 brief 里的「深铁矿道」是错的，须改"
  negative: "深铁矿道, 深铁地铁, 开口说话, 清晰可辨的对白"

# ============ 法师区 / 公园 ============
- fact_id: stormwind.job.009
  claim: 巫师圣殿是位于法师区中南部的法师塔与传送厅，坐标约 [49.1, 92.0]；2019 年改建前外墙爬满藤蔓。
  tag: ✅
  source: Warcraft Wiki — Wizard's Sanctum
  source_url: https://warcraft.wiki.gg/wiki/Wizard%27s_Sanctum
  quote: "a mage tower and a portal room located in the central-southern part of the Mage Quarter, in Stormwind City"; "[49.1, 92.0]"; "Before 2019's redesign, the tower had a 'vine-covered' exterior"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "法师区仰角：一座细高的圆柱形石塔，塔身自下而上爬满深绿藤蔓，顶部一圈开放拱窗透出冷蓝色光；塔底一道拱门两侧立着紫袍法师学徒，门内隐约可见几面竖立的圆形传送门光幕"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 塔身干净无藤蔓, 现代玻璃塔, 霓虹紫光过曝"

- fact_id: stormwind.person.025
  claim: 法师区/巫师圣殿一带的具名法师包括大法师马林（Archmage Malin）、高阶巫师安多玛斯（High Sorcerer Andromath）、法师训练师 Jennea Cannon、传送门训练师 Larimaine Purdue、高等精灵法师训练师 Elsharin。
  tag: ⚠️
  source: Warcraft Wiki — Wizard's Sanctum / Mage Quarter；中文译名来自 WowDB 中文 区域 1519
  source_url: https://warcraft.wiki.gg/wiki/Mage_Quarter
  quote: "key inhabitants mentioned include: Elsharin (High Elf Mage Trainer), High Sorcerer Andromath, Jennea Cannon (Mage Trainer), Larimaine Purdue (Portal Trainer)"；WowDB: "大法师马林""高阶巫师安多玛斯"
  tier: T1/T2 混
  verified_by: ai_read
  used_in: []
  prompt_string: "塔内环形厅，一名长须老年男性人类穿深紫镶银长袍、头戴尖顶宽檐法师帽，双手举在胸前掌心相对、两掌之间悬着一个缓慢旋转的符文球；他身后墙面立着三四道圆形传送门，门中各显一处远方景色"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 施放攻击法术, 爆炸特效, 现代激光"

- fact_id: stormwind.job.010
  claim: Vanilla 的暴风城有「公园（The Park）」区，位于城市西角，因主要住暗夜精灵而被叫作「暗夜精灵区」，广场中心有一口月亮井；这里有德鲁伊训练师、牧师训练师、草药学训练师与马厩管理员。
  tag: ✅
  source: Warcraft Wiki — The Park
  source_url: https://warcraft.wiki.gg/wiki/The_Park
  quote: "The Park used to be the district located in the western corner of Stormwind City."; "Due to the park being mostly inhabited by night elves, this area had also been called the 'night elf district'."; "The night elves created a Moonwell in the center of the park square."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "绿意最浓的一区：草地、成年乔木与藤架取代石板，中心一座圆形白石水池（月亮井），池水泛淡青色微光；池边站着两三名暗夜精灵——身形比人类更高更瘦、蓝紫肤色、长耳、深色长发，穿麻质与皮质混合的自然色系衣物，安静地看着水面"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 废墟, 焦土, 巨坑, 雄狮之眠, 纪念碑"

- fact_id: stormwind.job.011
  claim: 「公园」是在《大地的裂变》中被死亡之翼摧毁的（补丁 4.0.3a，2010-11-23），其废墟上到 2016 年（补丁 7.0.3）才建成「雄狮之眠」。两者在 Vanilla 都不存在。（若出现即版本错置）
  tag: ❌
  source: Warcraft Wiki — The Park
  source_url: https://warcraft.wiki.gg/wiki/The_Park
  quote: "The Park was destroyed by Deathwing's visit to Stormwind, during the Cataclysm."; "Lion's Rest was finally built on its ruins"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例锁定）本站西角必须是完好的绿地公园与月亮井，不得出现任何废墟、焦痕、断墙或纪念性墓园"
  negative: "废墟, 焦土, 断墙, 雄狮之眠, 瓦里安之墓, 死亡之翼破坏痕迹, 开口说话, 清晰可辨的对白"

# ============ 典型（非具名）人物 ============
- fact_id: stormwind.job.012
  claim: 暴风城卫兵（Vanilla 为 55 级）穿与暴风城军队相同的装备与狮纹罩袍，武器含剑、盾、弩、捕网，夜间巡逻时提油灯；他们巡街巡墙、守城门，并把被捕者押往暴风城监狱。
  tag: ✅
  source: Warcraft Wiki — Stormwind City Guard；NFU 1.12 中文数据库 NPC 68
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City_Guard
  quote: "the same gear and tabard as the soldiers of the Stormwind Army"; "swords, shields, crossbows, catch nets, and oil lamps for nighttime patrols"; "transport arrested criminals to the Stormwind Stockade"；NFU: "中文名：暴风城卫兵 / 英文名：Stormwind City Guard / 等级：55"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "两名卫兵并肩沿石板街缓步巡行：银灰板甲外罩蓝底金狮纹罩袍，带面颊护片的钢盔，左臂挂长方形狮纹盾，右手持长剑垂在体侧，腰后别一副折叠捕网；夜镜则一人换成左手提铜壳油灯、灯光在甲面上滑动"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 现代警察装备, 火枪, 90级版本外观, 港口背景"

- fact_id: stormwind.job.013
  claim: 卫兵对地位高的来访者会用「sir」与敬语，例句包括「Light be with you, sir.」「We are but dirt beneath your feet, sir.」「There walks a hero.」「Make way!」；将军对普通人的固定招呼是「Greetings, citizen」。
  tag: ✅
  source: Warcraft Wiki — Stormwind City Guard (NPC) quotes；Wowhead Classic npc=68；Warcraft Wiki — Marcus Jonathan
  source_url: https://www.wowhead.com/classic/npc=68/stormwind-city-guard
  quote: "Light be with you, sir."; "We are but dirt beneath your feet, sir."; "There walks a hero."; "Make way!"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（称谓依据，不出镜；卫兵仍零台词——只拍敬礼动作：右拳捶左胸后侧身让路）"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 卫兵嘴部开合"

- fact_id: stormwind.job.014
  claim: 玩家向卫兵挥手/敬礼时卫兵会挥手/回礼；马库斯·乔纳森将军亦如此（敬礼回敬礼、挥手回招呼）——即当地人的反应是**动作**，不是话。
  tag: ✅
  source: Warcraft Wiki — Stormwind City Guard (NPC) / Marcus Jonathan
  source_url: https://warcraft.wiki.gg/wiki/Marcus_Jonathan
  quote: "If players saluted him, he would salute back. If they waved, he would greet them with his standard phrase."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旅行者对卫兵挥手，卫兵抬手回挥并微微点头；旅行者敬礼，卫兵右拳捶胸回礼——全程无人张嘴"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 当地人回答旅行者, 当地人看镜头说话"

- fact_id: stormwind.job.015
  claim: Vanilla 暴风城的卫兵类 NPC 至少分三种：暴风城卫兵、暴风城巡逻兵、暴风城皇家卫兵；此外城中常驻的普通人 NPC 类型包括「人类平民」「暴风城孤儿」「老艾玛」等。
  tag: ⚠️
  source: WowDB 中文数据库 暴风城区域 NPC 列表（区域 1519）
  source_url: http://www.wowdb.cn/zone-1519.html
  quote: "暴风城卫兵""暴风城巡逻兵""暴风城皇家卫兵""人类平民""暴风城孤儿""老艾玛"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "皇家卫兵与街面卫兵的分工：皇家卫兵只出现在暴风要塞内，甲更亮、罩袍更新、持长柄戟立定不动；街面卫兵按固定路线来回走；巡逻兵在城门与桥头之间往返"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 皇家卫兵出现在街市, 卫兵坐着"

- fact_id: stormwind.job.016
  claim: 城中「暴风城孤儿」是可见的街头儿童 NPC 类型；孤儿院相关内容在 Vanilla 的教堂广场一带。
  tag: ⚠️
  source: WowDB 中文数据库 区域 1519；Warcraft Wiki — Stormwind City（Cathedral Square 含 Orphanage）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Cathedral Square - Northern religious center ... Orphanage"；WowDB: "暴风城孤儿"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂广场石阶下，三四个七八岁的孩子穿打补丁的粗布短衫与光脚或旧皮鞋，围着一块空地蹲着玩石子；一个孩子抱着布娃娃靠在石栏上看过路的人"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 孩子向镜头挥手喊话, 现代童装, 玩具"

- fact_id: stormwind.job.017
  claim: 贸易区街面上有具名的日常手艺人，例如面包师托马斯·米勒（Thomas Miller），以及卫兵军官 Officer Brady、Officer Jaxon、Captain Lancy Revshon、卫队长 Melris Malagan。
  tag: ⚠️
  source: Warcraft Wiki — Trade District
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "Street inhabitants include Thomas Miller (baker), Officer Brady and Jaxon (guards), Captain Lancy Revshon, and Melris Malagan (Captain of the Guard)."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街边面包摊：一名中年男性人类穿沾面粉的浅色罩衫，正用长柄木铲从砖砌拱形烤炉里把一排圆面包铲到木架上，热气从面包表面升起；摊前木板上已码了两层面包"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 现代烤箱, 包装袋, 价签"

# ============ 语言与称谓 ============
- fact_id: stormwind.lang.001
  claim: 通用语（Common）是人类的母语，也是联盟成员通用的交流语；矮人与侏儒为与人类通商而学会它。
  tag: ✅
  source: Warcraft Wiki — Common (language)；NFU 1.12 中文数据库 spell 668
  source_url: https://warcraft.wiki.gg/wiki/Common_(language)
  quote: "the native language of the humans"; "mostly spoken by the members of the Alliance"; "Dwarves and Gnomes learned it 'for trade purposes with the humans'"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播支撑）暴风城街面上人人都听得懂通用语，所以旅行者在城里不需要翻译"
  negative: "开口说话, 清晰可辨的对白, 路人对口型, 字幕翻译器, 现代同传设备"

- fact_id: stormwind.lang.002
  claim: 「通用语」是 Language Common 的官方简体中文译名（法术 ID 668）。
  tag: ✅
  source: NFU 1.12 中文数据库 spell 668
  source_url: https://db.nfuwow.com/60/?spell=668
  quote: "通用语 ID: 668 Language Common"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（译名字幕用）Common = 通用语"
  negative: "普通话, 通用语言, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.lang.003
  claim: 「矮人语」是 Language Dwarven 的官方简体中文译名（法术 ID 672）；矮人区是城里最可能听到矮人语的地方。
  tag: ✅
  source: NFU 1.12 中文数据库 spell 672
  source_url: https://db.nfuwow.com/60/?spell=672
  quote: "中文名：矮人语 / 英文名：Language Dwarven"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播支撑）矮人区的锻炉之间是矮人语的主场；狮鹫管理员杜加尔虽是人类却带一口矮人腔，是城内语言混杂的活标本"
  negative: "开口说话, 清晰可辨的对白, 路人对口型"

- fact_id: stormwind.lang.004
  claim: 「达纳苏斯语」是 Language Darnassian（暗夜精灵语）的官方简体中文译名（法术 ID 671）；在暴风城主要出现在「公园」区。
  tag: ✅
  source: NFU 1.12 中文数据库 spell 671
  source_url: https://db.nfuwow.com/60/?spell=671
  quote: "中文名：达纳苏斯语 / 英文名：Language Darnassian"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播支撑）公园区的月亮井边是达纳苏斯语的出现场景"
  negative: "暗夜精灵语（非官方）, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.lang.005
  claim: 「侏儒语」是 Language Gnomish 的官方简体中文译名（法术 ID 7340）；侏儒在矮人区与矿道地铁维护岗位上最常见。
  tag: ✅
  source: NFU 1.12 中文数据库 spell 7340
  source_url: https://db.nfuwow.com/60/?spell=7340
  quote: "中文名：侏儒语 / 英文名：Language Gnomish"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播支撑）矿道地铁月台上的技师是侏儒，侏儒语在这里出现"
  negative: "地精语, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.lang.006
  claim: 「牛头人语」（Language Taurahe，法术 ID 670）属部落阵营语言，不应出现在暴风城场景中。（若出现即错）
  tag: ❌
  source: NFU 1.12 中文数据库 spell 670
  source_url: https://db.nfuwow.com/60/?spell=670
  quote: "中文名：牛头人语 / 英文名：Language Taurahe"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（反例锁定）暴风城里不得出现兽人语/牛头人语/亡灵语的提法与其对应种族路人"
  negative: "兽人, 牛头人, 亡灵, 巨魔, 部落旗帜, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.lang.007
  claim: 暴风城军队采用正式军衔阶梯（自高向低）：General / Grand Marshal / Field Marshal / Marshal / Colonel / Commander / Lieutenant Commander / Major / Captain / Lieutenant / Knight-Champion / Knight-Captain / Knight-Lieutenant / Knight / Sergeant Major / Master Sergeant / Sergeant / Corporal / Private；军官以「军衔 + 姓名」称呼。
  tag: ✅
  source: Warcraft Wiki — Stormwind Army
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Army
  quote: "General - currently the highest conventional military rank"; "they are addressed by their rank and name: 'General Hammond Clay', 'Marshal Gryan Stoutmantle', and 'Commander Sharp'"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（称谓依据）口播称呼军官一律「军衔 + 姓名」：General Marcus Jonathan / 马库斯·乔纳森将军"
  negative: "长官大人, 警官, 队长同志, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.lang.008
  claim: 《伪装者的假面舞会》（The Great Masquerade）这段暴风要塞王座厅剧情里，宫廷成员互相以「Lady + 姓氏」称呼，伯瓦尔被称「Highlord」；这可作为宫廷称谓的游戏内佐证。
  tag: ✅
  source: Warcraft Wiki — The Great Masquerade
  source_url: https://warcraft.wiki.gg/wiki/The_Great_Masquerade
  quote: "The masquerade is over, Lady Prestor. Or should I call you by your true name... Onyxia..."; "Present in the throne room: Reginald Windsor, Highlord Bolvar Fordragon, Lady Katrana Prestor ... and King Anduin Wrynn"
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "（称谓依据，不出镜）"
  negative: "开口说话, 清晰可辨的对白, 路人对口型"

- fact_id: stormwind.lang.009
  claim: 暴雪方面表示 Wrynn 的读音是「Rin」，W 不发音（如 wrist 的 w）。（蓝贴标题与转述可见，正文原文未读到，按 ai_draft 处理）
  tag: ⚠️
  source: Wowhead Blue Tracker — "How do you pronounce 'Wrynn'?"
  source_url: https://www.wowhead.com/blue-tracker/topic/how-do-you-pronounce-wrynn-927076234
  quote: "a Blizzard developer indicated it should be pronounced 'Rin' with a silent 'W' like in 'wrist'"（搜索摘要转述，非蓝贴原文）
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "（TTS 用）Wrynn = /rɪn/「RIN」，W 不发音"
  negative: "WRIN, 弯-林, 开口说话, 清晰可辨的对白"

- fact_id: stormwind.lang.010
  claim: 魔兽世界的货币为金币/银币/铜币三级，100 铜 = 1 银，100 银 = 1 金。
  tag: ⚠️
  source: 中文社区通行说明（多来源一致）；英文侧 Wowhead/Wiki 价格以 g/s/c 表示（如 "2g 50s"）
  source_url: https://warcraft.wiki.gg/wiki/Elling_Trias
  quote: "Moist Azsunian Feta (2g 50s)"
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播支撑）街市交易的钱币特写：一小堆暗黄铜币与几枚白银币摊在木柜台上，硬币边缘磨损、正面有狮首压印"
  negative: "纸币, 现代硬币, 塑料代币, 开口说话, 清晰可辨的对白"
```

**统计：** 共 **52 条**事实（`stormwind.person` 25 / `stormwind.job` 17 / `stormwind.lang` 10，无重号）。
按核验方式：`ai_read` **50 条** / `ai_search_snippet` 1 条（`job.008` 矿道地铁官方译名）/ `ai_draft` 1 条（`lang.009` Wrynn 读音）。
按标签：✅ 43 / ⚠️ 7 / ❌ 2（另有 12 条版本错置整理在文末《版本错置清单》，那一节是**反例表**，不重复计入注册表）。

---

## 具名人物卡

> 全部只写「镜头能看到什么」。**他们一句话都不说。**

### 1. Highlord Bolvar Fordragon ｜ 大领主伯瓦尔·弗塔根
- **位置**：暴风要塞（Stormwind Keep）中央王座厅，王座台阶下偏左、男孩王身侧。
- **身份**：摄政（Regent Lord of Stormwind）兼暴风城军队最高统帅，代 10 岁的安杜因国王行权。**这是本站最重要的一条设定：Vanilla 的暴风城真正说了算的人是他。**
- **镜头看到**：高大壮年人类男性，全身抛光板甲，胸甲中央狮首浮雕，外披深蓝底金狮纹罩袍；金褐短发短须；左手扣在腰侧剑柄，右手垂落；正面朝厅门，站姿不动如钉——全厅唯一直视来客的人。
- **fact_id**：`stormwind.person.003` `.004` `.008`
- **务必避开**：任何巫妖王/亡灵化形象（那是 WotLK 结局之后的事）。

### 2. Anduin Wrynn ｜ 安杜因·乌瑞恩（1.12 客户端译名；现行官方作「安度因」）
- **位置**：暴风要塞王座厅，金狮环抱的「狮座（Lion Seat）」上。
- **身份**：**被加冕的男孩王，十岁**。不是王子（「暴风城王子」头衔是 3.0.2 才挂上的）。NPC 等级 5 级。
- **镜头看到**：约十岁的金发男孩，蓝白带金边的小号王室长袍，肩披短斗篷，双手放扶手，身形撑不满椅背、脚够不到地；偶尔转头看身旁两个大人。
- **fact_id**：`stormwind.person.001` `.002` `.009`

### 3. Lady Katrana Prestor ｜ 卡特拉娜·普瑞斯托女士
- **位置**：王座右侧半步处（**紧贴男孩王右手边**）。
- **身份**：王室顾问。真身是死亡之翼之女、黑龙奥妮克希亚——**镜头上不揭穿**，只让她比谁都放松。
- **镜头看到**：高挑成年女性人类贵族，深色长发盘束，深紫近黑曳地长裙、袖口领缘金线绣纹，双手身前交叠，下颌微抬、目光向下扫视厅内；不看男孩，只看进厅的人。
- **fact_id**：`stormwind.person.005` `.006`

### 4. Bishop DeLavey ｜ 德拉维主教
- **位置**：暴风要塞请愿厅（Petitioner's Chamber），坐标 [80.6, 34.8]。
- **身份**：教会派驻宫廷的代表，处理要塞内的事务。
- **镜头看到**：中年男性人类立于石柱旁，白底金边教会长袍、胸前圣光徽记，双手腹前交握；身后是排队等候的请愿平民背影。
- **fact_id**：`stormwind.person.010`

### 5. Archbishop Benedictus ｜ 大主教本尼迪塔斯
- **位置**：教堂广场 · 光明大教堂，中殿尽头高坛前。
- **身份**：圣光教会最高神职，训练联盟年轻牧师。
- **镜头看到**：中等身高、体格敦实的中年人类，白底大面积金绣的主教长袍、无沿白金主教冠、长披带，双手扶讲经台；**面相朴实近似农夫**（设定原话），穿着华服略显不自在；彩窗斜光罩身。
- **fact_id**：`stormwind.person.011` `.012`
- **务必避开**：暮光之锤的黑袍反派造型（那是 4.3 的事）。

### 6. Master Mathias Shaw ｜ 马迪亚斯·肖尔
- **位置**：旧城区 · 军情七处（SI:7）兵营内。62 级。
- **身份**：暴风城情报机构首脑、刺客之王。
- **镜头看到**：中年人类，深褐贴身皮甲外披暗色短披风，红褐短发短须；背对门口俯身撑在一张摊满地图与信件的方桌上，腰后交叉别双匕首；桌上一盏油灯是全屋唯一光源。
- **fact_id**：`stormwind.person.021`

### 7. General Marcus Jonathan ｜ 马库斯·乔纳森将军
- **位置**：英雄谷（Valley of Heroes）石桥中段，坐标 [69, 83]。
- **身份**：暴风城防务最高指挥官（High Commander of Stormwind Defense）。**Vanilla 的守城第一人就是他**——不是 Hammond Clay（那是他阵亡之后的继任者）。
- **镜头看到**：壮年人类骑在披蓝金马衣的白色战马上，全身银亮板甲外罩狮纹罩袍，缰绳握左手，马原地小幅踏步；两侧是数层楼高的第二次战争英雄石像。
- **fact_id**：`stormwind.person.015` `.016`
- **互动可拍**：旅行者敬礼 → 他回礼；挥手 → 他点头回挥。**只有动作，没有话。**

### 8. Dungar Longdrink ｜ 杜加尔·朗德瑞克（狮鹫兽管理员）
- **位置**：贸易区东侧狮鹫栖木（Gryphon Roost），坐标 [71.0, 72.6]。55 级。
- **身份**：飞行管理员，掌管全城的狮鹫航线。
- **镜头看到**：中年人类，厚皮飞行服、护目镜推在额头，腰挂飞行绳具；一手托缰辔、一手抚在伏地收翅的巨型狮鹫颈羽上；台上并排停着两三只狮鹫，羽毛被风吹动。
- **趣点（可口播）**：他是人类，却一口矮人腔。
- **fact_id**：`stormwind.person.017`

### 9. Innkeeper Allison ｜ 旅店老板奥里森
- **位置**：贸易区「镀金玫瑰（The Gilded Rose）」旅店，夹在银行与拍卖行之间，坐标 [60.6, 75.0]。30 级。
- **镜头看到**：成年女性人类，米白束腰长裙加深色围裙，头发脑后挽起，正把一排陶杯从托盘摆上木柜台；身后酒桶架与挂铜壶的墙，柜台一侧堆面包与水果，壁炉在深处发暖光。
- **fact_id**：`stormwind.person.018`

### 10. Auctioneer Chilton / Fitch / Jaxon ｜ 拍卖师希尔顿 / 拍卖师费奇 / 拍卖师亚克森
- **位置**：贸易区中央「商人大厅（Trader's Hall）」内的拍卖行。50 级。
- **镜头看到**：一排三人站在长木台后，深色马甲配白衬衫，人各一本摊开的厚账簿与一枚铜铃，手捏羽毛笔划记；台前挤着背包鼓胀的各族来客，墙上钉满羊皮纸告示。
- **fact_id**：`stormwind.person.019`

### 11. Elling Trias ｜ 伊林·提亚斯（乳酪商）
- **位置**：贸易区「提亚斯的奶酪店（Trias' Cheese）」，坐标 [66.1, 74.2]。30 级。
- **身份**：明面乳酪商，暗地情报网节点（与军情七处有线）。**镜头不揭穿，只当成街边奶酪铺拍。**
- **镜头看到**：中年人类，深绿罩衫配皮围裙，正把车轮状大奶酪抱上柜台、另一手握宽刃奶酪刀；货架层层码着不同大小的奶酪轮，门口挂成串洋葱与麻绳。
- **fact_id**：`stormwind.person.020`

### 12. Therum Deepforge ｜ 瑟鲁姆·深炉（锻造训练师）
- **位置**：矮人区，坐标 [63.6, 37.7]。33 级。
- **镜头看到**：矮人男性（身高到人类腰胸之间、体宽、络腮大胡编辫），厚皮围裙与护臂，赤裸前臂沾黑灰；右手抡短柄铁锤砸铁砧上的红热坯料，左手用长柄铁钳夹住；火星弹起后**加速下坠、落地即灭**（不得慢放/滞空）。
- **fact_id**：`stormwind.person.023`

### 13. High Priestess Laurena ｜ 高阶牧师劳瑞娜 / Lord Grayson Shadowbreaker ｜ 格雷森·破影者领主
- **位置**：教堂广场 · 光明大教堂两侧翼。均 60 级。
- **镜头看到**：劳瑞娜——白金牧师长袍加白色圣带，站在一排跪坐的年轻学徒前，一手抬起引导、一手托摊开厚书；格雷森——整套白银板甲、高耸肩甲带金饰、无头盔，战锤靠在身旁立架，双臂抱胸站在圣光旗帜下，面朝几名链甲见习骑士。
- **fact_id**：`stormwind.person.013` `.014`

### 14. Warden Thelwater ｜ 典狱官塞尔沃特
- **位置**：运河下方的暴风城监狱（Stockade）入口。30 级。
- **镜头看到**：中年人类，暗色链甲配皮护腕，腰挂一大串铁钥匙；一手提铁栅门把手，一手举油灯照向井下的下行阶梯；脚边是铁链与一只空锁具。
- **fact_id**：`stormwind.person.022`

### 15.（法师区）Archmage Malin ｜ 大法师马林 · High Sorcerer Andromath ｜ 高阶巫师安多玛斯
- **位置**：法师区 · 巫师圣殿（约 [49.1, 92.0]）。
- **镜头看到**：长须老年人类，深紫镶银长袍、尖顶宽檐法师帽，双手举胸前掌心相对、两掌之间悬一枚缓慢旋转的符文球；身后墙面立着三四道圆形传送门，门中各显一处远方景色。
- **fact_id**：`stormwind.person.025`（⚠️ 中文译名来自 T2 中文数据库，非游戏内截图确认）

---

## 典型人物卡（非具名 · 「他的一天」）

### A. 暴风城卫兵（Stormwind City Guard，55 级）
**一天**：晨间在城门与英雄谷石桥换岗（新岗上前、旧岗右拳捶胸后离开）→ 白天沿固定路线巡街，遇人流拥堵时抬手示意让路 → 午后押送一名被缚双手的人穿过运河桥往监狱方向 → 黄昏换上提油灯的夜巡组，两人一组沿城墙与运河边缓行，灯光在甲面上滑动。
**装束**：银灰板甲 + 蓝底金狮纹罩袍 + 面颊护片钢盔 + 长方形狮纹盾 + 长剑，腰后折叠捕网。
`stormwind.job.012` `.013` `.014` `.015`

### B. 市集摊贩与街面手艺人
**一天**：天没亮支摊、卸货、把货码成塔（面包师从砖砌拱炉里铲面包上木架；花贩把成捆花插进水桶；奶酪商把车轮奶酪抱上柜台）→ 上午客流高峰，收铜币银币、找零、用麻绳捆好递出 → 午后趁淡时补货、擦柜台、赶苍蝇 → 日落收摊，把没卖完的塞回筐里、拉油布盖上。
`stormwind.job.003` `.017` `.010`

### C. 矮人工匠与侏儒技师（矮人区 / 矿道地铁）
**一天**：矮人在露天锻炉前抡锤——夹坯、入炉、出炉、锤打、淬火（白汽腾起），一整天循环；炉上一股稳定的灰白烟柱把天光滤成暖褐 → 侏儒在工程学手推车旁拧发条盒、调铜管，护目镜拉下又推上 → 另一拨侏儒下到矿道地铁月台，趴在轨道边拧螺栓、给转轴上油，三节铁皮车厢停站 12 秒又开走。
`stormwind.job.005` `.006` `.007` `.008` `stormwind.person.024`

### D. 神职人员与受助者（教堂广场）
**一天**：清晨白袍神职在大教堂石阶上清扫、点燃两侧烛台 → 上午高阶牧师带一排跪坐学徒诵读（**只有口型以外的动作：抬手引导、翻书、低头**——本系列不给他们台词，改用手势与体态叙事）→ 白天陆续有受伤平民被搀进侧厅救治（这里是全城疗伤中心）→ 傍晚孤儿们在石阶下蹲着玩石子，一名神职把一篮面包放到石栏上。
`stormwind.job.001` `.016` `stormwind.person.011` `.013`

### E. 法师学徒（法师区）
**一天**：清晨在巫师圣殿塔底门口两侧立定值守 → 日间抱着卷轴与书册在塔内旋梯上下奔走 → 反复练习同一个手势：双掌相对、掌间凝出一点光又散掉（练不成，再来）→ 傍晚站在传送门光幕前记录进出人数。
`stormwind.job.009` `stormwind.person.025`

### F. 街头孩子（暴风城孤儿）
**一天**：教堂广场石阶下蹲着玩石子 → 追着过路的马车跑一小段 → 趴在运河石栏上看水里的鱼 → 傍晚三四个人挤在一级石阶上分一块面包。
**装束**：打补丁的粗布短衫、光脚或旧皮鞋，一个孩子抱布娃娃。
`stormwind.job.016`

### G. 暗夜精灵访客（公园区 · Vanilla 限定）
**一天**：整天几乎不移动——站在月亮井边看水面、在乔木下打坐、给马厩的坐骑刷毛。身形比人类更高更瘦、蓝紫肤色、长耳、深色长发，麻质与皮质混合的自然色系衣物。
`stormwind.job.010`

---

## 称谓白名单 / 黑名单

> 说明：**旅行者说英语**，中文只出现在字幕。所以白名单给「英文原文 + 中文译法 + 读音」。
> **当地人不回话**，所以白名单只管旅行者**提到/指认**他们时怎么称呼。

### ✅ 白名单

| 对象 | 英文称呼（旅行者口播） | 中文字幕 | 读音（TTS） | 依据 |
|---|---|---|---|---|
| 男孩王 | **the boy king** / **King Anduin** | 男孩王／安杜因国王 | KING AN-doo-in RIN | `person.001` `.009` |
| 摄政 | **Highlord Fordragon** / **the Highlord** / **Lord Regent** | 大领主弗塔根／大领主／摄政 | HIGH-lord FOR-dra-gon | `person.003` `lang.008` |
| 王室顾问 | **Lady Prestor** / **Lady Katrana** | 普瑞斯托女士 | LAY-dee PRESS-tor | `person.005` `lang.008` |
| 大主教 | **Archbishop Benedictus** / **Your Grace**（书面尊称） | 大主教本尼迪塔斯 | ARCH-bish-op ben-eh-DIK-tus | `person.011` |
| 主教 | **Bishop DeLavey** | 德拉维主教 | BISH-op duh-LAY-vee | `person.010` |
| 高阶牧师 | **High Priestess Laurena** | 高阶牧师劳瑞娜 | HYE PREE-stess lor-EE-nah | `person.013` |
| 圣骑士首席 | **Lord Grayson Shadowbreaker** | 格雷森·破影者领主 | GRAY-son SHAD-ow-bray-ker | `person.014` |
| 将军 / 军官 | **军衔 + 姓名**：General Marcus Jonathan、Captain …、Marshal … | 马库斯·乔纳森将军 | JEN-er-al MAR-cus JON-a-than | `lang.007` `person.015` |
| 普通卫兵 | **guardsman** / **the guard** | 卫兵 | GARD-z-man | `job.012` |
| 情报头子 | **Master Shaw** / **Spymaster Shaw** | 肖尔大师／间谍大师肖尔 | MAS-ter SHAW | `person.021` |
| 店主 / 旅店老板 | **Innkeeper Allison** / **the innkeeper** | 旅店老板奥里森 | IN-kee-per AL-i-son | `person.018` |
| 陌生市民（泛称） | **citizen** / **good folk** / **friend** | 市民／各位／朋友 | SIT-i-zen | `job.013`（游戏内卫兵与将军对人的固定用词就是 citizen） |
| 对高阶者的敬语 | **sir** / **my lord** / **my lady** | 阁下／大人／夫人 | — | `job.013`（卫兵原话 "Light be with you, sir."） |
| 祝祷式招呼 | **Light be with you.** | 愿圣光与你同在 | — | `job.013` |

### ❌ 黑名单（禁止出现）

| 禁用 | 为什么 |
|---|---|
| **Prince Anduin / 安杜因王子** | 「暴风城王子」头衔是补丁 3.0.2 才有的；Vanilla 他是被加冕的**国王**。`person.009` |
| **King Varian / 瓦里安陛下** | Vanilla 期间他失踪在外，不在城里。`person.007` |
| **Lord Regent Turalyon / 图拉扬摄政** | 摄政是伯瓦尔；图拉扬摄政是 BfA 之后的事。`person.008` |
| **General Hammond Clay** | 他是马库斯·乔纳森阵亡后的继任者，Vanilla 没有他。`person.015` |
| **Anduin 作「安度因」与「安杜因」混用** | 两种都是官方（1.12 客户端 vs 现行零售），但**一集内只能用一种**。`person.002` |
| **博瓦尔·弗塔根** | 官方是「**伯**瓦尔」。`person.004` |
| **深铁矿道** | 官方是「**矿道地铁**」。`job.008` |
| 「陛下」以外的地球式敬称：**殿下（对国王）/ 皇上 / 圣上 / 万岁 / 主公 / 大人（对平民）** | 中式与日式宫廷敬语，与设定不符 |
| 现代称呼：**先生 / 女士（泛用）/ 警官 / 老板 / 同志 / 市长** | 出戏 |
| 其他 IP 的称谓：**陛下万岁 / Your Highness 对国王 / Khaleesi / Jarl / 领主大人（泛用）** | 串 IP |
| **Milord / M'lady 的滥用** | 这是对贵族的称呼，不能拿去叫卫兵、摊贩、矮人工匠 |
| **兽人语 / 牛头人语 / 亡灵语** 的提法及对应种族路人 | 部落阵营，不属于暴风城。`lang.006` |
| 给任何当地人配台词 | 系列铁律：**当地人零台词**，只拍动作 |

---

## 专名译名表（glossary 草案 → `_series/glossary.md`）

> 三列：英文 / 官方简体中文 / 英语读音标注（TTS 用；读音标注为本路撰写的近似音，标 ⚠️）

### 城市与八大区

| English | 官方简体中文 | 读音（TTS） |
|---|---|---|
| Stormwind City | 暴风城 | STORM-wind SIT-ee |
| Kingdom of Stormwind | 暴风王国 | KING-dom of STORM-wind |
| Valley of Heroes | 英雄谷 | VAL-ee of HEE-rohz |
| Trade District | 贸易区 | TRAYD DIS-trikt |
| Old Town | 旧城区 | OHLD TOWN |
| Mage Quarter | 法师区 | MAYJ KWOR-ter |
| Dwarven District | 矮人区 | DWOR-ven DIS-trikt |
| Cathedral Square | 教堂广场 | kuh-THEE-dral SKWAIR |
| The Park | 公园（俗称「暗夜精灵区」） | thuh PARK |
| Stormwind Keep | 暴风要塞 | STORM-wind KEEP |
| The Canals | 运河 | thuh kuh-NALZ |

### 地标建筑

| English | 官方简体中文 | 读音（TTS） |
|---|---|---|
| Cathedral of Light | 光明大教堂（部分中文来源作「圣光大教堂」⚠️） | kuh-THEE-dral of LYTE |
| Throne Room / Lion Seat | 王座厅 / 狮座 | THROHN ROOM |
| Petitioner's Chamber | 请愿厅 | puh-TISH-un-erz CHAYM-ber |
| The Gilded Rose | 镀金玫瑰（旅店） | thuh GIL-did ROHZ |
| Trader's Hall | 商人大厅（拍卖行所在） | TRAY-derz HAWL |
| Stormwind Counting House | 暴风城银号（银行） | STORM-wind KOWN-ting HOWS |
| Gryphon Roost | 狮鹫栖木 | GRIF-on ROOST |
| Trias' Cheese | 提亚斯的奶酪店 | TRY-us CHEEZ |
| The Pig and Whistle Tavern | 猪和哨声酒馆 | thuh PIG and WIS-ul TAV-ern |
| Wizard's Sanctum | 巫师圣殿 | WIZ-erdz SANK-tum |
| The Slaughtered Lamb | 被屠宰的羔羊（酒馆） | thuh SLAW-terd LAM |
| The Stockade | 暴风城监狱 | thuh STOK-ayd |
| Deeprun Tram | **矿道地铁** | DEEP-run TRAM |
| Moonwell | 月亮井 | MOON-wel |
| Stormwind Visitor's Center | 暴风城接待中心 | STORM-wind VIZ-i-terz SEN-ter |

### 机构与阵营

| English | 官方简体中文 | 读音（TTS） |
|---|---|---|
| The Alliance | 联盟 | thuh uh-LY-ans |
| SI:7 (Stormwind Intelligence) | 军情七处 | ES-EYE SEV-en |
| Church of the Holy Light | 圣光教会 | CHURCH of thuh HOH-lee LYTE |
| Stormwind Army | 暴风城军队 | STORM-wind AR-mee |
| Stormwind City Guard | 暴风城卫兵 | STORM-wind SIT-ee GARD |

### 人名

| English | 官方简体中文 | 读音（TTS） |
|---|---|---|
| Anduin Wrynn | 安杜因·乌瑞恩（1.12 客户端）／安度因·乌瑞恩（现行） | AN-doo-in RIN（W 不发音） |
| Varian Wrynn | 瓦里安·乌瑞恩 | VAIR-ee-an RIN |
| Highlord Bolvar Fordragon | 大领主伯瓦尔·弗塔根 | BOHL-var for-DRAG-on |
| Lady Katrana Prestor | 卡特拉娜·普瑞斯托女士 | kuh-TRAH-nuh PRESS-tor |
| Onyxia | 奥妮克希亚 | oh-NIK-see-uh |
| Archbishop Benedictus | 大主教本尼迪塔斯 | ben-eh-DIK-tus |
| Bishop DeLavey | 德拉维主教 | duh-LAY-vee |
| High Priestess Laurena | 高阶牧师劳瑞娜 | lor-EE-nuh |
| Lord Grayson Shadowbreaker | 格雷森·破影者领主 | GRAY-son SHAD-oh-bray-ker |
| Master Mathias Shaw | 马迪亚斯·肖尔 | muh-THY-us SHAW |
| General Marcus Jonathan | 马库斯·乔纳森将军 | MAR-kus JON-uh-thun |
| Dungar Longdrink | 杜加尔·朗德瑞克 | DUN-gar LONG-drink |
| Innkeeper Allison | 旅店老板奥里森 | AL-i-son |
| Auctioneer Chilton / Fitch / Jaxon | 拍卖师希尔顿 / 费奇 / 亚克森 | awk-shun-EER CHIL-tun |
| Elling Trias | 伊林·提亚斯 | EL-ing TRY-us |
| Therum Deepforge | 瑟鲁姆·深炉 | THEER-um DEEP-forj |
| Warden Thelwater | 典狱官塞尔沃特 | THEL-waw-ter |
| Archmage Malin | 大法师马林 | MAL-in |
| High Sorcerer Andromath | 高阶巫师安多玛斯 | AN-droh-math |
| Gelbin Mekkatorque | 格尔宾·梅卡托克 | GEL-bin MEK-uh-tork |
| Magni Bronzebeard | 麦格尼·铜须 | MAG-nee BRONZ-beerd |
| Ironforge | 铁炉堡 | EYE-ern-forj |
| Elwynn Forest | 艾尔文森林 | EL-win FOR-est |

### 种族

| English | 官方简体中文 | 读音（TTS） |
|---|---|---|
| Human | 人类 | HYOO-man |
| Dwarf / Dwarves | 矮人 | DWORF / DWORVZ |
| Gnome | 侏儒 | NOHM（G 不发音） |
| Night Elf | 暗夜精灵 | NYTE ELF |
| High Elf | 高等精灵 | HYE ELF |

### 语言

| English | 官方简体中文 | 读音（TTS） |
|---|---|---|
| Common | 通用语 | KOM-un |
| Dwarvish / Dwarven | 矮人语 | DWOR-vish |
| Darnassian | 达纳苏斯语 | dar-NAY-shun |
| Gnomish | 侏儒语 | NOH-mish |

### 货币

| English | 官方简体中文 | 读音（TTS） |
|---|---|---|
| gold (piece) | 金币 | GOHLD |
| silver (piece) | 银币 | SIL-ver |
| copper (piece) | 铜币 | KOP-er |

> 换算：100 铜 = 1 银，100 银 = 1 金。⚠️（T2）

---

## 版本错置清单（所有 ❌）

| # | 错误 | 正确（Vanilla） | 依据 |
|---|---|---|---|
| 1 | 瓦里安·乌瑞恩坐在暴风城王座上 | 他在 Vanilla 期间**失踪在外、不在城里**；王座上是 10 岁的安杜因 | `person.007` `.008` |
| 2 | 称安杜因为「王子 / Prince」 | Vanilla 他是**被加冕的国王**；「暴风城王子」头衔是补丁 3.0.2 才挂上的 | `person.009` |
| 3 | **拍暴风城港口 / 码头 / 货船 / 栈桥 / 仓库工** | Vanilla **没有港口**（补丁 3.0.2，2008-10-14 才加）。水边戏只能拍**运河** | `stormwind.job` 版本锚 + Warcraft Wiki — Stormwind Harbor："Patch 3.0.2 (2008-10-14): Added." |
| 4 | 西角是废墟 / 雄狮之眠 / 瓦里安之墓 | Vanilla 西角是完好的**公园**，中心有月亮井，住暗夜精灵 | `job.010` `.011` |
| 5 | 出现「暴风城外城区 / 暴风城大使馆 / 东部地契之台」 | 均为后续资料片添加，Vanilla 无 | Warcraft Wiki — Stormwind City（列为 post-Cataclysm 增补） |
| 6 | 图拉扬任摄政 | 摄政是**伯瓦尔·弗塔根** | `person.003` `.008` |
| 7 | Hammond Clay 将军守城 | Vanilla 守城第一人是**马库斯·乔纳森将军**；Clay 是其阵亡后的继任者 | `person.015` |
| 8 | 伯瓦尔以巫妖王 / 亡灵形态出现 | 那是 WotLK 结局之后；Vanilla 是活人、板甲、狮纹罩袍 | `person.003` |
| 9 | 本尼迪塔斯以暮光之锤黑袍反派形象出现 | 那是 4.3；Vanilla 是白金主教袍的圣光教会最高神职 | `person.011` |
| 10 | 写「深铁矿道」 | 官方中文是「**矿道地铁**」 | `job.008` |
| 11 | 写「博瓦尔·弗塔根」 | 官方中文是「**伯**瓦尔·弗塔根」 | `person.004` |
| 12 | 卫兵用 90 级零售版外观 | Vanilla 暴风城卫兵是 55 级、板甲＋狮纹罩袍＋长剑盾牌，夜巡提油灯 | `job.012` |
| 13 | 城里出现兽人 / 牛头人 / 亡灵 / 巨魔路人或部落旗帜 | 暴风城是联盟主城，Vanilla 城内只有人类 / 矮人 / 侏儒 / 暗夜精灵 / 少量高等精灵 | `lang.006` `job.010` |
| 14 | 给任何当地人配台词 / 让路人对口型 | 系列铁律：当地人零台词，反应全部用动作（敬礼、让路、点头） | `job.013` `.014` |

---

## 未查 / Open questions

1. **伯瓦尔与卡特拉娜在 Vanilla 的精确坐标未查到。** 已确认「暴风要塞中央王座厅，男孩王身侧 / 王座右侧半步」，但拿不到 [x, y] 数字。Wowhead Classic 的坐标由 JS 渲染，WebFetch 读不到；`vanilla-wow-archive.fandom.com` 返回 402。**建议**：由人工在 Classic Era 客户端内截图对账，或换用可渲染 JS 的抓取方式。
2. **`warcraft.huijiwiki.com`（魔兽世界中文维基）全站对 WebFetch 返回 403**，`baike.baidu.com` 同样 403。本文的中文官方译名主要来自 **NFU 1.12 中文数据库（`db.nfuwow.com/60/`）**（T1，1.12 客户端数据）与 **WowDB 中文（`wowdb.cn`）**（T2）。`矿道地铁` 一条只拿到搜索摘要（T2，`ai_search_snippet`），**建议人工用中文客户端复核一次**。
3. **「光明大教堂」vs「圣光大教堂」未定。** 灰机中文维基条目名为「光明大教堂」，但中文社区大量使用「圣光大教堂」。两者都在流通，**需人工在中文客户端确认区域名后锁死**。
4. **Wrynn 读音的蓝贴原文未读到**（Wowhead Blue Tracker 正文 JS 渲染）。目前只有搜索摘要转述「'Rin'，W 不发音」。已标 `ai_draft` / T3。**其余人名读音标注全部是本路撰写的近似音，非官方**——若要严格，需人工对照暴雪官方语音（过场动画配音）逐个确认。
5. **莉莲·闪轴（Lilliam Sparkspindle）、乌尔菲尔·铁须（Ulfir Ironbeard）、Jennea Cannon、Larimaine Purdue、Elsharin 的官方简体中文译名未查到**，本文暂留英文＋⚠️ 标注，未自行音译。
6. **「老艾玛（Old Emma）」的英文原名与身份未核实**，只在 WowDB 中文 NPC 列表里见到中文名。
7. **暴风城孤儿院的具体位置与院长 NPC 未查到**（`warcraft.wiki.gg/wiki/Stormwind_Orphanage` 返回 404）。只确认「教堂广场含孤儿院」。
8. **未查：Vanilla 暴风城的具名银行职员**（Wiki 未列 Vanilla 名单）。若脚本要拍银行柜台，需补查。
9. **越界未做**（属别路）：城市布局与建筑形制（W1/W2）、衣着形制细节（W3）、物价与经济（W4）。本文的 `prompt_string` 里对衣着/建筑的描述只到「够分镜用」的粒度，**以对应路的研究为准**。
