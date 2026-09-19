---
worker_id: researcher-w2-architecture
stage: 0
role: researcher
angle: architecture
status: complete
blockers: []
confidence: medium
facts_total: 62
facts_ai_read: 59
facts_ai_draft: 3
ref_images_total: 24
---

# W2 · 暴风城建筑形制与地标（sk2 ·《时空旅行》第 2 站 · 魔兽世界暴风城 · 经典旧世 Vanilla 锚点）

> **用途**：下游阶段 2 要拿本文给每个场景主体写 ≥1500 字的锚点图 prompt，每个形制词都要指得出依据。本文只做 **W2 一路（建筑形制与地标）**，不涉布局路线 / 衣着 / 物价 / 人物（那是 W1/W3/W4/W5 的活）。
>
> **版本锚点 ＝ 经典旧世 Vanilla（WoW 1.x / Classic，大地的裂变之前）。** 本文对每条「现行游戏里有」的特征都回查了补丁号：凡 3.0.2 / 4.0.3a / 5.2.0 / 6.0.2 / 7.0.3 / 7.3.5 / 8.1.5 引入的，一律进 §版本错置清单，**不进 prompt**。
>
> **`verified_by` 口径**：`ai_read` ＝ 本 worker 本次用 WebFetch 实际打开了该页面并拿到含该 quote 的正文；`ai_draft` ＝ 只拿到搜索引擎返回的摘要、没打开原页，**不得直接进 prompt，须人眼复核升级**。全部 `ai_read` 进 prompt 前仍建议人眼抽查升 `human`。
>
> **虚构世界的 tier 映射**（本文实际能拿到的最高层级是 T1）：
> - **T0** ＝ 游戏本体资产 / 暴雪官网与官方新闻站 / 官方设定书。本文 T0 来源：暴雪官网 `worldofwarcraft.blizzard.com` 的官方导览文、`news.blizzard.com` 的 WoW Classic 城市导览（后者正文只给 NPC 名录、无形制描述，仅用作参考图来源）。
> - **T1** ＝ `warcraft.wiki.gg`（Warcraft Wiki，Wowpedia 的现行官方继任站）中**带游戏内出处**的段落，含其逐字转录的补丁说明（`Patch changes`）与开发者访谈（`Development`）。**本文绝大多数事实是 T1。**
> - **T2** ＝ 转述 RPG 设定书（*Lands of Conflict* / *Alliance Player's Guide*）的 wiki「In the RPG」小节；有出处的美术考据长文。
> - **T3** ＝ 无引用的百科段落、玩家美术随笔。
> - **T4** ＝ 玩家推测、模型默认（只作反例）。
>
> **一个必须先说清的判断（总纲）**：暴风城的「长什么样」**主要存在于游戏资产里，不存在于文字里**。Warcraft Wiki 的地标条目普遍只写功能（谁在里面、卖什么）而不写形制；官方导览文写的是 NPC 名录。因此本文的诚实结论是：**凡带 ✅ 的形制词，都是我确实在文字来源里读到的**；游戏里肉眼可见但没有任何文字来源写过的东西（例如「屋顶具体是哪一种蓝」「窗户是尖拱还是圆拱」「街灯的具体造型」），我**一律没有编**，全部进 §未查 / Open questions，留给人眼看参考图定。这正是下游必须先建参考图库、再写 prompt 的原因。
>
> **一条需要上报 parent 的任务书订正**：任务书把「暴风城港口」列为 *Cataclysm* 特征。**实际是 3.0.2（巫妖王之怒，2008-10-14）加入的**，比 Cataclysm 早两年。对 Vanilla 锚点而言它照样是版本错置（结论不变），但理由要写对，口播不能说成「大灾变加的」。详见 §版本错置清单 X1。

---

## §1 通用建筑语汇（`stormwind.arch.NNN`）

### 1.1 材质与主色

```yaml
- fact_id: stormwind.arch.001
  claim: 暴风城在第一次战争被兽人焚毁后，由石匠工会（Stonemasons Guild）重建，外立面用的是白石——这是全城最基本的材质设定，也是「暴风白」这一辨识色的来源
  tag: ✅
  source: Warcraft Wiki - Stormwind City（History / Reconstruction）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "restored Stormwind City to its former majesty with white stone for its exterior"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城市主体建筑为暖白色石灰岩砌体，石块方正、灰缝细密、表面经年略泛米白与浅灰，墙体厚重"
  negative: "红砖, 清水混凝土, 玻璃幕墙, 抹灰外墙, 木板房, 夯土墙, 瓷砖贴面"
  note: 「白石」是全片建筑的**锁定串起点**，凡暴风城外景镜一律复现。

- fact_id: stormwind.arch.002
  claim: 暴风要塞的屋顶铺的是「蓝色石板瓦」（blue slate）——这是设定文字里唯一一处明写屋顶颜色的地方，也是全城蓝屋顶语汇的文字依据
  tag: ✅
  source: Warcraft Wiki - Stormwind Keep（描述旧要塞形制）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "Its roof was shod with blue slate and the complex had many side buildings, towers, and halls."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "屋顶铺深蓝灰色石板瓦，瓦片薄而层叠，边缘略有厚薄不匀，雨后反浅冷光"
  negative: "红瓦, 琉璃瓦, 茅草顶, 金属波纹板, 沥青瓦, 彩钢瓦"
  note: **此句描述的是第一次战争前的旧要塞**（原文在旧城段落）。重建后的要塞沿用同一语汇是游戏里肉眼可见的事实，但「重建后仍是蓝石板」这一句**文字来源里没有**——所以下游若要把蓝屋顶推广到全城民居，那一步是 ⚠️ 推测（见 arch.003）。

- fact_id: stormwind.arch.003
  claim: 「全城民居屋顶都是蓝色圆锥／尖顶」这一条**设定文字里没有明载**；文字只锁到要塞的蓝石板（arch.002）与「蓝金配色」的泛论，具体屋顶形状须以参考图为准
  tag: ⚠️
  source: 本 worker 检索结论（Warcraft Wiki 各区条目均无屋顶形制描述）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The city is made up of roughly rectangular districts separated by canals."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（此条不直接进 prompt——屋顶形状由参考图给，不由文字给）"
  negative: ""
  note: **口播须说「设定没写，我按参考图来」。** 下游建锚点图时，屋顶形状/坡度/塔尖比例一律**看图定**，不要从本文编词。这是本文最重要的一条**边界声明**。

- fact_id: stormwind.arch.004
  claim: 暴风城的美术定位是「石材 + 蓝金点缀」的人类首都语汇
  tag: ⚠️
  source: WoW Housing Hub / 社区数据库对暴风城主题装饰的概括
  source_url: https://housing.wowdb.com/decor/?faction=stormwind
  quote: "Stormwind is the capital of the human kingdom, featuring grand architecture with stone, blue and gold accents."
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "石造主体，蓝色与金色作点缀——蓝用于屋面、旗帜、布幔，金用于纹章、镶边、器物五金"
  negative: "银色为主, 黑金配色, 紫金配色, 大面积原木色"
  note: T3，只作配色大方向的旁证；真正的锁定串以 arch.001 + arch.002 + arch.009 为准。

- fact_id: stormwind.arch.005
  claim: 暴风城的街道是石砌大道，尺度以「巨大的石头通道」形容——夜精灵把公园区当成躲开「暴风城本体那些一望无际的石头大道」的喘息处
  tag: ✅
  source: Warcraft Wiki - Park（描述夜精灵为何聚居于此）
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "a welcome respite from the vast stone thoroughfares of Stormwind proper"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "宽阔的石板大道，路面由大块灰白石板与卵石拼砌，尺度开阔到近乎空旷，两侧是连续的石砌立面"
  negative: "土路, 泥泞小径, 柏油路, 水泥路, 窄巷为主, 木栈道"
  note: 「vast stone thoroughfares」是**全片街道镜的锁定依据**——暴风城的街不是窄巷，是大尺度石道。这条同时反证了老城区的「脏窄」是对比项（landmark.010）。

- fact_id: stormwind.arch.006
  claim: 城墙厚到走过去像穿隧道，墙面是刷白的、砌缝齐整的砖石，地面石板被磨得光滑
  tag: ⚠️
  source: 美术考据随笔《Stormwind is the centre of the world》
  source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world
  quote: "Neat bricks placed in tidy mortar. Washed and white. The smooth stone buffs your boots as you walk through gates and walls so thick they feel like tunnels."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "城门洞进深极大，走进去像穿过一段隧道；墙体砌缝齐整、表面刷白，地面石板被行人磨得光滑反光"
  negative: "薄墙, 单层砖墙, 城门洞浅, 墙面粗糙未处理, 地面粗粝"
  note: T3 玩家随笔，**不是设定**，但它是我找到的**唯一**一份逐项描写暴风城建成环境的连续文字，措辞可作 prompt 用词参考。凡取用须与参考图对账。

- fact_id: stormwind.arch.007
  claim: 运河上架的是厚重的石拱桥，桥身高高拱起
  tag: ⚠️
  source: 同上（美术考据随笔）
  source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world
  quote: "Heavy stone bridges that arch proudly over the canals."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "运河上跨着厚重的白石拱桥，桥拱高起，桥面两侧是实心石栏板，栏板顶面被磨得发亮"
  negative: "铁桥, 木桥, 吊桥, 平桥无拱, 镂空金属栏杆, 现代人行天桥"
  note: 拱数 / 栏杆具体形制**文字来源里没有**，须看参考图。⚠️。

- fact_id: stormwind.arch.008
  claim: 铺地是交错拼砌的卵石／石块，走在其中方向感会被打乱
  tag: ⚠️
  source: 同上（美术考据随笔）
  source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world
  quote: "The cobblestones criss-cross in front of you, which, among the chaos, is disorientating."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "地面为交错拼砌的卵石与石板，纹路纵横交叉，缝隙里积着细尘"
  negative: "整版水泥地, 沥青, 木地板, 规整同向铺砖"
  note: 与官方开发者自述「暴风城布局令人迷路」（landmark.030）互证——迷路感是设计事实，不是玩家抱怨。

- fact_id: stormwind.arch.009
  claim: 狮子是联盟／暴风城的象征，在城门一带**同时以旗帜和石雕的形式**出现——城垛上立着狮子石像
  tag: ✅
  source: 暴雪官网官方导览《Welcome to Stormwind: A Guided Tour》
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/20142731/welcome-to-stormwind-a-guided-tour
  quote: "The lion, symbol of the Alliance is prominently displayed both in the banners and the stone effigies on the parapets."
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城垛上等距立着石雕狮子像，城门两侧垂挂狮纹长幡；狮纹为正面狮首，金色，衬蓝底"
  negative: "鹰纹, 龙纹, 十字纹, 双头鹰, 抽象几何徽记, 现代企业 logo"
  note: **T0 官方**，是全片纹章的第一依据。「石雕狮子在城垛上」是可直接画的形制。

- fact_id: stormwind.arch.010
  claim: 暴风城纹章的纹章学描述是——银（白）底、金色正面狮首、狮首镶蓝边、外加一圈镶蓝边的金色边框
  tag: ⚠️
  source: DrawShield 纹章库 · Blazon of Stormwind
  source_url: https://drawshield.net/gallery/0137/gallery-013701.html
  quote: "on a field argent, a lion's head affronty or fimbriated azure, a bordure or fimbriated azure"
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "盾形纹章：银白底，正中一枚正面朝前的金色狮首，狮首外缘镶一道钴蓝细边；盾牌外圈一道金色边框，边框同样镶钴蓝细边"
  negative: "侧面狮身, 站立狮, 双狮, 红底, 黑底, 狮首带王冠, hex色值"
  note: 第三方纹章站的转译，**不是暴雪原文**，故 ⚠️。但它把 arch.009 的「金狮 + 蓝」量化成了可画的纹章学措辞，实用价值高。配色与 arch.004 一致，互证。

- fact_id: stormwind.arch.011
  claim: 城门外侧两侧各架着一台弩炮（ballista）
  tag: ✅
  source: 暴雪官网官方导览《Welcome to Stormwind: A Guided Tour》
  source_url: http://worldofwarcraft.blizzard.com/en-us/news/20142731/welcome-to-stormwind-a-guided-tour
  quote: "Stormwind Gates which are flanked by two ballistae just outside of them"
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城门外两侧各架一台木制重弩炮，粗绞盘与铁件外露，炮身朝向城外道路"
  negative: "火炮, 加农炮, 现代武器, 投石机, 弩炮朝向城内"
  note: T0 官方。注意**是弩炮不是火炮**——火炮在暴风城是港口（3.0.2）才有的，属版本错置（X1）。

- fact_id: stormwind.arch.012
  claim: 全城每一个区里都有苹果树
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Notes and trivia · Lore）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Apple trees can be found in every district of Stormwind City."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌街区之间点缀着结果的苹果树，树冠不大，深绿叶片间挂着红果，树下是石板地"
  negative: "棕榈树, 松树, 樱花, 热带植物, 光秃无树, 大片草坪"
  note: 极好用的**「城市不是纯石头」的软化元素**，且 ✅ 明载、可放心入画。任何暴风城街景镜都可以挂一棵。

- fact_id: stormwind.arch.013
  claim: 各区之间由「闪着微光的蓝色运河」分隔、由跨河的桥连接；城里有许多码头，市民在码头边钓鱼
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Canals and prisons）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Each district is bordered by shimmering blue canals and linked by bridges spanning over them. Anglers fish from the many docks in the city"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "区与区之间隔着一道明净的蓝绿色运河，水面微微反光；沿岸砌石护岸，间或探出小块木质／石质码头，有人坐在码头边垂钓"
  negative: "浑浊黑水, 干涸河床, 混凝土渠, 现代游艇, 塑料垃圾, 护栏铁丝网"
  note: 「shimmering blue」是**官方给的水色**，与 arch.014 的「脏但诚实」是两种取向，画面按镜选一种、不要混。

- fact_id: stormwind.arch.014
  claim: 运河水并不清澈，是带着汗与木屑的那种「诚实的脏」
  tag: ⚠️
  source: 美术考据随笔《Stormwind is the centre of the world》
  source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world
  quote: "The water is dirty, no city's waterways are truly clean, but dirty in an honest way, with sweat and sawdust."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "运河水略带浊意，水面浮着细碎木屑与草屑，不是污水，是活城市的水"
  negative: "污水, 油污, 泛绿藻华, 蒸馏水般透明, 垃圾漂浮"
  note: T3 随笔的解读，与 arch.013 官方的「shimmering blue」**取向相反**。半写实画风建议以 **arch.013 为主、arch.014 作近景细节**（远景蓝亮、近景有浮屑），两条不冲突。

- fact_id: stormwind.arch.015
  claim: 运河的存在有一个被砍掉的设计原因——最初计划在运河上跑贡多拉小船作为区间快速交通，因技术「过于晦涩」而放弃；玩家能下水也是这个遗留
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Notes and trivia · Development）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Originally, the city was planned to feature gondolas that would serve as a quick way to travel from one district to another, hence the existence of the Canals and the fact that players can get in and out of the Canal waters. However, the technology wound up being \"prohibitively esoteric.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（此条是口播料，不直接进画面 prompt）"
  negative: ""
  note: **极佳的口播梗**——「这城为什么到处是运河？因为本来要跑贡多拉的，做不出来就留下了一城的水。」开发者自述，✅ 可直接讲。画面上**不要画贡多拉**（Vanilla 运河上没有）。

- fact_id: stormwind.arch.016
  claim: 全城由「大致呈矩形的街区」构成，街区之间用运河切分
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Geography）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The city is made up of roughly rectangular districts separated by canals."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "俯瞰时城市呈若干大致矩形的街区，街区被一道道运河切开，桥把它们缝在一起"
  negative: "放射状路网, 同心圆城, 自由曲线街巷, 棋盘格完全规整"
  note: 航拍／开场大全景镜的构图依据。

- fact_id: stormwind.arch.017
  claim: 暴风城原本可能规划了九个区，其中两个被合并成了一个
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Development，引开发者 Johnathan Staats）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Staats also recalls that Stormwind may have originally had nine districts, two of which were fused into a single area."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播料，不进画面）"
  negative: ""
  note: 口播梗。注意原文用 "may have"，是开发者回忆而非确证——口播须说「据当年的设计师回忆」。

- fact_id: stormwind.arch.018
  claim: Vanilla 时期暴风城的建筑**没有屋顶几何**——直到飞行坐骑加入，暴风城才被改造以适应从空中降落；很多玩家在能落到屋顶上之后以为屋顶一直都在
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Notes and trivia · Development）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "With the introduction of flying mounts, Stormwind had to be modified to accommodate this, as the city didn't possess any rooftops. It was noted that when players started to land on rooftops, many assumed the rooftops had always been there."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（口播料 + 反向约束）"
  negative: "俯拍屋顶平台, 人物站在屋顶, 屋顶花园, 可行走的屋面"
  note: **对本片是硬约束**：Vanilla 锚点下**不要出现「人站在屋顶上」的镜头**，也不要把屋面画成可行走的平台。同时是一个上好的口播梗（「你现在看到的屋顶，当年是没有的」）。

- fact_id: stormwind.arch.019
  claim: 光明大教堂的钟会报时，遇险时则用来向全城示警
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Notes and trivia · Lore）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The cathedral's bell rings to mark the hours, and in times of danger to alert the citizens."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（声音设计依据；画面可给钟楼特写）"
  negative: ""
  note: **全片的「时间刻度」由钟声给** —— 旅行者游一天，报时钟声是最自然的转场音。✅ 明载，放心用。

- fact_id: stormwind.arch.020
  claim: 城里有一座钟——它长在运河中那座名为「金库（Vault）」的建筑顶上
  tag: ✅
  source: Warcraft Wiki - Vault (Stormwind City)
  source_url: https://warcraft.wiki.gg/wiki/Vault_(Stormwind_City)
  quote: "is located opposite the Stockade, and mirrors that other prison in most ways, except that it is completely surrounded by water and has a clock on top of it"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河当中一座孤立的石砌方形建筑，四面环水，顶上嵌着一面大钟，钟面朝向水道"
  negative: "钟楼在教堂上, 独立钟塔, 数字钟, 罗马数字以外的现代表盘（表盘细节须看参考图）"
  note: **纠正一个常见混淆**：暴风城的「钟楼」不是教堂尖塔，是运河监狱 Vault 顶上的钟。补丁 5.2.0 的「the clocktower have been restored」指的就是它（被死亡之翼打坏后修复）——反证 Vanilla 时它是完好的。

- fact_id: stormwind.arch.021
  claim: 城里有一条下水道通往艾尔文森林的镜湖（Mirror Lake）
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Notes and trivia · Lore）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "A sewer in the city leads to Mirror Lake."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "石砌拱形下水道口，铁栅半掩，水从暗处淌出，口沿长着湿苔"
  negative: "现代混凝土管涵, 圆形铸铁井盖, 塑料管"
  note: 可作「城市基础设施」一节的口播料。

- fact_id: stormwind.arch.022
  claim: 城内有学校——女教师 Miss Danna 在几个区里给一群孩子上课
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Notes and trivia · Lore）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "In some districts, School Mistress Miss Danna teaches a group of children, indicating the presence of a school in the city."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "街边空地上一位女教师带着一小群孩子席地而坐上课，背后是白石墙面"
  negative: "现代教室, 课桌椅, 黑板, 校服, 书包"
  note: **是流动授课不是校舍**——原文说的是「在某些区里教一群孩子」，没说有校舍建筑。画成露天授课更贴。

- fact_id: stormwind.arch.023
  claim: Vanilla 时期的门洞是真的矮——从 3.0.8 到 4.0.3，夜精灵和德莱尼只能骑机械陆行鸟通过暴风城银行（Stormwind Counting House）的大门，其他坐骑会让这两个种族太高而过不去；4.0.3a 重做时才把门洞加高
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Notes and trivia · Gameplay）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "night elves and draenei could only ride through Stormwind City's Stormwind Counting House bank door on mechanostriders; all other Alliance mounts made these two races too high to fit. When it was remodeled ... in patch 4.0.3a, the height of the doorway was increased."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "店铺与公共建筑的门洞偏矮偏窄，门楣压得低，成年人进门需略低头"
  negative: "高大双开门, 通高玻璃门, 教堂式巨门（银行等民用建筑）"
  note: **对 Vanilla 锚点是一条很硬的形制证据**——民用建筑门洞是矮的。教堂／要塞例外。

- fact_id: stormwind.arch.024
  claim: 第一次战争之前的旧暴风城：三重城墙环绕暴风要塞、各厢区之间另有次级屏障；街区中拔起巨塔；奔涌的河流瀑布被巨大的水车所驯服
  tag: ✅
  source: Warcraft Wiki - Stormwind City（History · 战前旧城）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Three full sets of walls ribboned around Stormwind Keep, with lesser barriers separating the different wards. Great towers sprang from the streets, and a surging river cascade had been harnessed by massive waterwheels."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（历史形态，仅用于回忆／讲史镜）三重环形城墙层层围住山岗上的要塞，街区间拔起高塔，河流跌水处架着巨大的木质水车"
  negative: "（用于当代镜时）三重城墙, 巨型水车, 街心高塔"
  note: **⚠️ 时代边界**：这写的是**被兽人摧毁前**的旧城，不是 Vanilla 时的城。若讲史段落要画，须明确标注「这是一百多年前的暴风城」；当代镜**不得**出现三重城墙与水车。
```

### 1.2 招牌与画面文字纪律

```yaml
- fact_id: stormwind.arch.025
  claim: 暴风城的店铺**都有正式店名**（如「Trias' Cheese」「The Gilded Rose」「Pig and Whistle Tavern」「The Slaughtered Lamb」「Lionheart Armory」），这些名字在游戏里以子区域名／建筑名的形式存在
  tag: ✅
  source: Warcraft Wiki - Trade District / Old Town / Mage Quarter / Dwarven District（各区 shop 列表）
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "Taverns: The Gilded Rose. Shops: The Empty Quiver, Everyday Merchandise, Lionheart Armory, Pestle's Apothecary, Trias' Cheese, Weller's Arsenal"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（店名只进后期贴字与口播，不进画面）"
  negative: "画面内任何文字, 招牌文字, 英文店名, 中文店名, 数字, 门牌号"
  note: **本片画面一律零文字**（详见 arch.026）。店名清单的价值在于：后期贴字时**贴对名字**，以及口播报得出名字。

- fact_id: stormwind.arch.026
  claim: 招牌**本来长什么样**在任何文字来源里都没有描述——须以参考图为准；本片画面统一把招牌画成空白木牌或纯纹样牌，文字由后期贴
  tag: ⚠️
  source: 本 worker 检索结论（Warcraft Wiki 各 shop 条目只给名称与 NPC，无招牌形制描述；搜索「WoW 招牌 形制」只返回周边商品与住宅系统装饰，非游戏本体）
  source_url: https://warcraft.wiki.gg/wiki/Trade_District
  quote: "The article conspicuously lacks descriptive detail about architectural features, landscapes, or aesthetic elements of the district itself."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "店门上方悬挑一块空白木牌，木牌以铁件吊挂于墙上伸出的曲铁臂，随风微晃；牌面无字，只有木纹与铁钉；部分店家以实物幌子代替（一只铁壶、一把剑、一串谷穗）"
  negative: "任何文字, 字母, 汉字, 数字, 印刷体, 手写体, 灯箱, 霓虹, 二维码, logo"
  note: **这是全片最重要的一条画面纪律**。「实物幌子代替文字招牌」是我给的可执行方案（⚠️ 推测，设定没写），好处是零文字且信息量足。下游建参考图库时**必须专门收一组招牌特写**来把这条从 ⚠️ 升到可靠。
```

---

## §2 四大机构地标（`stormwind.landmark.NNN`）

### 2.1 英雄谷与城门（landmark.001–007）

```yaml
- fact_id: stormwind.landmark.001
  claim: 暴风城的巨大城门高过艾尔文森林的树冠；门后是英雄谷——一处天然盆地，一座宏伟的桥横跨其上，通向贸易区
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Valley of Heroes）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Stormwind City's great gates tower over the treetops of Elwynn Forest. Beyond them lies The Valley of Heroes, a beautiful natural basin spanned by a majestic bridge leading to the city's trade district."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "巨大的白石城门高耸，门楣高过森林树冠；门内是一处开阔的天然盆地，一座宽阔的石桥横跨盆地，直通城内"
  negative: "城门低矮, 木门, 铁闸为主体, 平地无盆地, 吊桥"
  note: 「高过树冠」是**可量化的尺度锚**——画面里城门与树的高度比要做到位。

- fact_id: stormwind.landmark.002
  claim: 英雄谷位于暴风城门之前，一座石桥跨过狭窄的护城壕，是所有入城者看到的第一眼
  tag: ✅
  source: Warcraft Wiki - Valley of Heroes
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "The Valley of Heroes is a valley that lies before Stormwind Gate. A bridge of stone crosses the narrow moat and is the first sight of all who enter."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一座石桥跨过一道不宽的护城壕，桥的尽头是城门；这是入城的第一个画面"
  negative: "宽阔护城河, 无水干壕, 铁索桥"
  note: **开场第一镜的构图依据**。注意是 narrow moat（窄壕），不是大河。

- fact_id: stormwind.landmark.003
  claim: 桥两侧排列着巨大的雕像，刻的是第二次战争中的英雄——那些踏入黑暗之门、去德拉诺结束战争的人类、高等精灵与矮人
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Valley of Heroes）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The bridge is lined with enormous statues depicting some of the greatest heroes of the Second War — the brave men, high elves, and dwarves who stepped into the Dark Portal to bring an end to the war in the scarred land of Draenor itself."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "桥的两侧等距立着数尊远超真人尺度的石雕像，像高数倍于行人，立于高大方形基座之上，面朝桥心"
  negative: "青铜像, 现代雕塑, 抽象雕塑, 雕像等身, 无基座"
  note: 与 landmark.004 的具体名单配套使用。

- fact_id: stormwind.landmark.004
  claim: 英雄谷共五尊雕像，位置固定——左侧是库德兰·蛮锤与大法师卡德加，右侧是达纳斯·托尔贝恩与游侠队长奥蕾莉亚·风行者，主道尽头是将军图拉扬
  tag: ✅
  source: Warcraft Wiki - Valley of Heroes
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "On the left are Kurdran Wildhammer ... and the Archmage Khadgar ... on the right are Force Commander Danath Trollbane and Ranger-Captain Alleria Windrunner; at the end of the main road ... is General Turalyon."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "五尊巨像：左侧两尊（一名矮人、一名法师），右侧两尊（一名战士、一名精灵游侠），主道尽头一尊圣骑士将军像居中正对来路"
  negative: "四尊, 六尊, 左右不对称摆放, 尽头无像"
  note: **五尊、左二右二尽头一** —— 这是可机检的硬布局。种族对应：库德兰＝矮人、卡德加＝人类法师、达纳斯＝人类战士、奥蕾莉亚＝高等精灵游侠、图拉扬＝人类圣骑士。

- fact_id: stormwind.landmark.005
  claim: 每尊雕像基座上都有铭牌，文字格式是「头衔＋功绩＋Presumed deceased（推定已故）」——例如库德兰是「著名屠龙者、鹰巢山的狮鹫主人……推定已故」，卡德加是「麦迪文的前学徒、联盟远征军最高指挥官……推定已故」
  tag: ✅
  source: Warcraft Wiki - Valley of Heroes（各雕像铭文）
  source_url: https://warcraft.wiki.gg/wiki/Valley_of_Heroes
  quote: "Kurdran Wildhammer: \"Renowned Dragon Fighter. Gryphon Master of the Aerie Peak... Presumed deceased.\" / Khadgar: \"Former apprentice of Medivh. Supreme Commander of the Alliance Expedition... Presumed deceased.\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（铭文是口播料——画面上基座铭牌须画成空白石板或纹样，零文字）"
  negative: "基座刻字, 可辨认的铭文, 英文碑文"
  note: **极好的口播料**：五块碑全部以「推定已故」收尾，因为第二次战争后远征军失联多年——旅行者念出这一句，是全城最有情绪的一个点。**但画面零文字**（arch.026），铭牌画空白。

- fact_id: stormwind.landmark.006
  claim: 雕像高约三十英尺（约九米），把只在传说里听过的名字做成了看得见的面孔
  tag: ⚠️
  source: 美术考据随笔《Stormwind is the centre of the world》
  source_url: https://youcangothere.substack.com/p/stormwind-is-the-centre-of-the-world
  quote: "Great statues 30 feet high provide chiselled faces to names that you have heard from stories."
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "雕像连基座高约九米，人站在基座前仅及基座高度的一半"
  negative: "雕像高度与人相近, 雕像高过城墙"
  note: T3 目测值，⚠️。但它给了一个**可画的比例尺**（人 ≈ 基座一半），比「enormous」好用得多。须与参考图对账。

- fact_id: stormwind.landmark.007
  claim: 「猎龙者头颅挂在城门拱上」是 Vanilla 独有的景象——奥妮克希亚的头曾悬挂在通往暴风城的**左侧拱门**上；该机制于 1.3.0（2005-03-07）加入、3.2.2（2009-09-22）移除
  tag: ✅
  source: Warcraft Wiki / Wowpedia - Head of Onyxia (Classic)
  source_url: https://warcraft.wiki.gg/wiki/Head_of_Onyxia_(Classic)
  quote: "Onyxia's head used to hang from the left arch into Stormwind City ... This no longer happens as of 3.2.2. ... Added in Patch 1.3.0 (2005-03-07)."
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "城门左侧拱门下悬吊着一颗巨大的黑色巨龙头颅，以粗铁链倒挂，龙角向下，鳞片暗哑，尺寸远大于门下行人"
  negative: "龙头挂在右侧, 完整龙身, 龙头会动, 新鲜血腥, 现代吊索"
  note: **本片最值钱的一条 Vanilla 专属画面**——它是「经典旧世」这个版本锚点的视觉身份证，现行版本已经没有了。⚠️ `ai_draft`（只拿到搜索摘要，未打开原页），**下游用前须人眼开一次 `Head_of_Onyxia_(Classic)` 页面确认「left arch」这个方位**。若是史料驱动的严谨口径，这条值得升 human。
```

### 2.2 贸易区（landmark.008–009）

```yaml
- fact_id: stormwind.landmark.008
  claim: 贸易区位于全城中心，终日喧闹；全城一半的银行、拍卖行、旅店以及狮鹫管理员都在这里；此外还有一排装备店，以及 Trias 家的奶酪铺和 Gallina 家的酒铺
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Trade District）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The Trade District lies in the center of Stormwind City and is always bustling with activity. ... Half of the city's banks, auction houses, and inns, as well as the local gryphon master, are all located within. ... the Trias and Gallina families run cheese and wine shops out of the Trade District as well."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城市中心的大广场，四周围合着两三层的白石商铺，底层开敞为铺面、上层住人；广场中人流不断，摊位与行商混杂"
  negative: "空旷无人, 现代商场, 玻璃橱窗, 连锁店招, 停车场"
  note: 具体建筑：拍卖行＝Trader's Hall（在贸易区中心）、银行＝Stormwind Counting House、旅店＝The Gilded Rose、公会注册＝Stormwind Visitor's Center。

- fact_id: stormwind.landmark.009
  claim: 狮鹫栖木（Gryphon Roost）在贸易区东侧、要顺一道坡道上去；它是飞行管理员所在地，也是两名蛮锤矮人养育的狮鹫的巢
  tag: ✅
  source: Warcraft Wiki - Trade District / Gryphon Roost
  source_url: https://warcraft.wiki.gg/wiki/Gryphon_Roost
  quote: "The Gryphon Master is up a ramp on the east side." / "houses the city's gryphons, raised by the two Wildhammer dwarves."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "贸易区东侧一道石砌坡道盘上一处高台，台上是开敞的狮鹫栖架，粗木横梁上停着数只狮鹫，地面散落羽毛与草料"
  negative: "封闭鸟舍, 铁笼, 马厩, 电梯, 楼梯（是坡道不是台阶）"
  note: **是 ramp（坡道）不是楼梯** —— 因为要让坐骑上去。这种功能决定形式的细节最值得写进 prompt。
```

### 2.3 老城区（landmark.010–011）

```yaml
- fact_id: stormwind.landmark.010
  claim: 老城区在贸易区以东，是首都最古老的部分，很多地方仍然早于第一次战争后的重建——因为它当年没被严重破坏，所以从未真正重建过；结果是一处质朴而破败的地方，街道比别的区脏得多也臭得多
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Old Town）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "the oldest section of the capital, and many parts of it still predate the reconstruction of the city after its razing by the orcs ... As the district had not been badly ravaged, it had never needed true rebuilding. Consequently, it is a rustic, downtrodden place, where the streets are described as far dirtier and smellier than the other districts."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旧城区：墙体不是新砌的白石，而是发黄发灰的旧石与外露木构架，木料深褐开裂；街道狭窄、地面湿污，墙面爬着水渍与霉斑；屋檐低、层高参差，晾衣绳横跨巷子"
  negative: "崭新白石, 整齐立面, 宽阔大道, 干净路面, 统一层高"
  note: **这是全片唯一一个「不是白石新城」的区**，是建立城市层次感的关键对比。「从未重建过」直接给出了「这里的石头比别处旧一百年」这条可画的逻辑。

- fact_id: stormwind.landmark.011
  claim: 老城区边缘是暴风城指挥中心（Command Center），附近是王国情报机构 SI:7 的总部；区内还有勇士大厅、兵营、训练场、马厩与「猪和哨声」酒馆
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Old Town）/ Old Town
  source_url: https://warcraft.wiki.gg/wiki/Old_Town
  quote: "the Stormwind Command Center is located along the edges of the quarter, and near is the headquarters of the SI:7, the kingdom's intelligence agency." / "Command Center, Champions' Hall, SI:7 headquarters, Barracks, Training grounds, Stables, Pig and Whistle Tavern"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "旧城一角是军事建筑群：兵营为厚重石砌、开小窗；旁边是露天训练场，立着草人靶与兵器架；再旁是马厩，木栅与草料"
  negative: "现代营房, 铁丝网, 岗亭, 阅兵广场"
  note: SI:7 总部**外观不显眼**是其设定性质决定的（情报机构），画面上不要做成地标式建筑。
```

### 2.4 法师区与巫师圣殿（landmark.012–015）

```yaml
- fact_id: stormwind.landmark.012
  claim: 法师区在贸易区以西；巫师圣殿巍然立于该区中心；区内其余部分是裁缝铺、存放魔法物品与材料的仓库，以及热闹的咖啡馆和酒吧；「屠宰羔羊」酒馆的地窖是术士们的聚集处
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Mage Quarter）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The Wizard's Sanctum stands proudly in the center of the district, ... while shady warlocks are often drawn to the dark cellars of the Slaughtered Lamb ... The rest of the district is filled with tailoring shops, warehouses storing magical artifacts and reagents, and bustling coffeehouses and bars."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "法师区：一座高塔统领全区，四周是两层的裁缝铺与仓库，门口堆着捆扎的布匹与封蜡的陶罐；沿街有露天咖啡座，桌上是冒热气的杯子"
  negative: "全区都是塔, 无人街道, 现代咖啡馆, 遮阳伞"
  note: 「咖啡馆和酒吧」是很反直觉但 ✅ 明载的细节——法师区是有市井生活的，不是纯魔法区。

- fact_id: stormwind.landmark.013
  claim: 巫师圣殿是一座「爬满藤蔓的塔」，位于城市西部，其内还设有「奥术艺术与科学学院」
  tag: ✅
  source: Warcraft Wiki - Wizard's Sanctum（In the RPG 小节，转述 RPG 设定书）
  source_url: https://warcraft.wiki.gg/wiki/Wizard%27s_Sanctum
  quote: "The vine-covered tower sits to the west of the city, and it also contains the Academy of Arcane Arts and Sciences."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "一座独立高塔，塔身石造，外壁大面积爬满深绿藤蔓，藤蔓沿石缝攀至塔身中上部；塔顶收束为尖锥"
  negative: "光洁无植被的塔, 金属塔, 玻璃塔, 藤蔓覆盖全塔遮住石材, 多塔并立"
  note: **「爬满藤蔓」是我能找到的关于巫师圣殿外观的唯一一条文字描述**，且来自 RPG 设定书（T2）。紫色尖塔群的说法**在文字来源里查无实据**——任务书里的「紫色尖塔群」须以参考图核实，见 §未查 Q3。

- fact_id: stormwind.landmark.014
  claim: 巫师圣殿是法师区南角最高的塔，不用飞行的话要沿塔外盘绕的石径走上去
  tag: ⚠️
  source: 社区数据库／指南（Warcraft Tavern 等）对塔的通行方式描述
  source_url: https://www.warcrafttavern.com/wow/guides/stormwind-portals-and-boats/
  quote: "the tallest tower in the southern corner of The Mage Quarter, and to ascend the tower without flying, you have to climb the winding stone path around the building"
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "塔身外壁盘绕着一道向上的石径／外挂坡道，无扶手或仅有矮石栏，绕塔数圈通向塔顶平台"
  negative: "塔内楼梯为唯一通路, 外挂铁梯, 电梯, 旋转楼梯在内部"
  note: **「楼梯在塔外不在塔内」是很强的形制特征**，若属实则必须写进 prompt。但仅有 `ai_draft`（搜索摘要），**须人眼看参考图确认**。任务书里说的「内部环形楼梯」与此**相反**——见 §未查 Q3。

- fact_id: stormwind.landmark.015
  claim: 法师区里有一处池塘／水面，但游戏里叫「Olivia's Pond」的那个**不在法师区**——它在大灾变后才开放的暴风城郊外（Stormwind City Outskirts）
  tag: ❌
  source: Warcraft Wiki - Olivia's Pond
  source_url: https://warcraft.wiki.gg/wiki/Olivia%27s_Pond
  quote: "Olivia's Pond is a small body of water located in the Stormwind City Outskirts."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（不进 prompt）"
  negative: ""
  note: **防坑条**。法师区确有水面（肉眼可见），但它**没有已知的正式名称**，且 Olivia's Pond 是 4.0.3a 之后郊外的东西，**不能拿来当法师区池塘的依据**。法师区水面的形制见 §未查 Q4。
```

### 2.5 教堂广场与光明大教堂（landmark.016–021）

```yaml
- fact_id: stormwind.landmark.016
  claim: 教堂广场在贸易区以北，是圣光信徒的宗教中心；虽然暴风要塞是城里最大的建筑，但许多人认为最令人敬畏的是光明大教堂；广场上还有城里的孤儿院和市政厅
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Cathedral Square）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "Though Stormwind Keep is the biggest structure in Stormwind City, many believe the most awe-inspiring is the Cathedral of Light. ... Other notable locations in the square include the city's orphanage, and the City Hall"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "一处开阔的石铺广场，北端被一座巨大的教堂立面完全统治；广场两侧是较矮的公共建筑（市政厅、孤儿院），衬得教堂更高"
  negative: "教堂偏居一角, 广场狭小, 广场中央有巨型雕像（Vanilla 时是纪念碑不是雕像，见 landmark.021）"
  note: **「最大的是要塞，最震撼的是教堂」是官方给的主次关系**——构图上教堂要压住广场，但全城最大体量仍归要塞。

- fact_id: stormwind.landmark.017
  claim: 光明大教堂是一座有许多侧翼与尖塔的宏伟建筑
  tag: ✅
  source: Warcraft Wiki - Cathedral of Light（In the RPG 小节）
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "A grand structure with many wings and spires, the Cathedral houses Archbishop Benedictus, the bishop of Stormwind City, and various other priests."
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "巨大的石造教堂，主体两侧伸出多组侧翼，屋脊之上林立着数量众多的细长尖塔，尖塔高低错落、越靠中心越高"
  negative: "单塔教堂, 圆顶教堂, 无尖塔, 对称双塔（\"many spires\" 不是两座）"
  note: **「many wings and spires」＝ 多侧翼 + 多尖塔**，不是常见的哥特双塔正立面。尖塔的**具体数量**文字来源没给，须看参考图（§未查 Q1）。

- fact_id: stormwind.landmark.018
  claim: 大教堂内部是「嵌着钴蓝的石砌厅堂」；它是一处优雅而宁静、宜于祈祷与省思的地方
  tag: ✅
  source: Warcraft Wiki - Cathedral of Light（Notes / 描述）
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "The cathedral has cobalt-inlaid stone halls." / "elegant and peaceful ... inviting for prayer and reflection"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "教堂内厅为浅暖白石砌筑，墙面与地面嵌有饱和的钴蓝色石材条带与几何镶嵌，蓝白对比强烈；空间高敞、光线自高窗斜落、气氛安静"
  negative: "全金内饰, 木质内饰, 暗色内饰, 彩色斑斓, 拥挤低矮, hex色值"
  note: **「cobalt-inlaid」是全片教堂内景的锁定串核心**——钴蓝镶嵌于白石，正好呼应全城的白石＋蓝的主色（arch.001 / arch.002）。

- fact_id: stormwind.landmark.019
  claim: 大教堂的钟是在铁炉堡的「大熔炉」上铸成的，与洛丹伦那口钟是一对，是矮人送给人类、以纪念两族友谊的礼物；每天日落时分，大教堂会敲响一记钟，钟声甜美、传遍全城
  tag: ✅
  source: Warcraft Wiki - Cathedral of Light（Notes / In the RPG）
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "The cathedral's bell was created on the Great Forge in Ironforge, like its twin bell for Lordaeron, as a gift from the dwarves to remind the friendship between their peoples." / "Every night at sunset, the Cathedral of Light rings a solitary bell whose sweet pitch reaches the entire city."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "钟室内一口巨大的青铜钟悬于粗木梁下，钟体表面有矮人风格的錾刻纹样与铆接感的边饰"
  negative: "铁钟, 钢钟, 电子钟, 一组编钟, 钟体光滑无纹"
  note: **收尾镜的答案就在这里**——旅行者游一天，结束在日落的那一记钟声上。且这口钟是矮人造的，能把矮人区那条线收回来。✅ 明载，强烈建议用。

- fact_id: stormwind.landmark.020
  claim: 大教堂的地下是墓穴与图书馆；墓穴是受尊崇的逝者——牧师、战争英雄、圣骑士等——的安息之所；祭坛两侧各有一条通往地下的暗道
  tag: ✅
  source: Warcraft Wiki - Cathedral of Light
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_of_Light
  quote: "The cathedral's catacombs are the resting place of the honored dead: priests, war heroes, paladins, and others" / "hidden ways downstairs \"on each side of the altar\""
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "祭坛左右两侧各有一道向下的石阶通道，隐在列柱阴影里；地下为低矮的石砌拱顶墓穴，壁龛中安放石棺，烛光昏黄"
  negative: "祭坛正后方下楼, 单侧楼梯, 现代地下室, 明亮照明, 电灯"
  note: **「祭坛两侧各一道」是对称的硬布局**，好画也好认。

- fact_id: stormwind.landmark.021
  claim: 教堂广场的纪念碑在 Vanilla 时期纪念的是大主教阿隆索斯·法奥（Alonsus Faol）；直到大灾变（补丁 4.0.3a）才被换成乌瑟尔·光明使者的雕像
  tag: ✅
  source: Warcraft Wiki - Cathedral Square
  source_url: https://warcraft.wiki.gg/wiki/Cathedral_Square
  quote: "The square originally featured a monument to Alonsus Faol, which was replaced after the Cataclysm with a statue of Uther the Lightbringer."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "广场上立着一座纪念碑（非人像雕像），石造、基座方正、碑体竖立，形制庄重而不张扬"
  negative: "乌瑟尔雕像, 圣骑士全身像, 手持战锤的雕像, 喷泉式纪念台"
  note: **⚠️⚠️ 版本红线**。现行游戏和绝大多数网络图片里，教堂广场立的是**乌瑟尔雕像 + 喷泉**，那是 4.0.3a 之后的。Vanilla 锚点下必须是**阿隆索斯·法奥纪念碑**。暴雪官方导览文里写的 "A Fountain dedicated to the memory of Uther the Lightbringer" 是现行版本，**不可用**。碑的具体形制文字没写，见 §未查 Q2。
```

### 2.6 矮人区与矿道地铁（landmark.022–025）

```yaml
- fact_id: stormwind.landmark.022
  claim: 矮人区在教堂广场以东，是铁炉堡的矮人与侏儒在暴风城里划出的一块地盘；空气里满是烟与火星，地面随着铁砧的捶打而震动；街边排满兵器与护甲铺子，铁匠们在许多露天广场上把普通金属打成杰作
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Dwarven District）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The air is thick with smoke and sparks, and the ground trembles with the pounding of anvils, but to many it feels just like a home should. A trove of weapon and armor shops line the streets, and blacksmiths create masterpieces out of common metals in the many open-air plazas."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "矮人区：数处露天广场上并排立着燃着的熔炉与铁砧，橙红炉火跳动，火星四溅并随热气上升；空气中悬着灰白烟尘，光线被烟雾切成一道道；街边店铺门口挂着成排的兵器与护甲"
  negative: "室内锻造为主, 冷炉不燃, 空气清澈无烟, 现代工厂, 电焊, 流水线"
  note: **「open-air plazas」是关键**——锻造是在**露天广场**上进行的，不是关在铺子里。这决定了这一区的镜头能拍到火光与烟。注意本条的烟与火**只属于矮人区**，按 `ai_video.md` 16.9，全片共用的 `渲染样式:` 串里**不得**写死暖橙火光。

- fact_id: stormwind.landmark.023
  claim: 矮人区的锻炉持续产生烟霭，伴着铁匠锤子不断的敲击
  tag: ✅
  source: Warcraft Wiki - Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Dwarven_District
  quote: "The forges in the district produce a constant haze, supplemented by the constant strokes of smiths' hammers."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "熔炉不断吐出烟霭，整个街区笼在一层薄灰雾里，远处建筑轮廓被雾软化"
  negative: "浓黑烟柱, 无烟, 白色蒸汽为主"
  note: 「constant haze」＝**持续的薄霭**，不是浓烟柱。这条给了大气介质的量——对半写实画风是重要的空间感来源。

- fact_id: stormwind.landmark.024
  claim: 矿道地铁隧道入口被一只巨大的旋转齿轮框住，不可能看漏；隧道在矮人区东侧
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Dwarven District）/ Dwarven District
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "The massive spinning cog that frames the entrance to the tram tunnel cannot be missed." / "The Stormwind City end of the Deeprun Tram line is accessible through a tunnel on the east side of the district."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "隧道口被一只巨大的金属齿轮环绕，齿轮竖立、缓缓转动，齿牙粗大、金属表面是暗黄铜与铁灰的混合，带铆钉与油渍；齿轮内圈即是通向地下的拱形洞口"
  negative: "静止齿轮, 小齿轮, 纯装饰浮雕齿轮, 现代工业齿轮, 电动机, 齿轮上有文字"
  note: **矮人区的地标镜就是这一只齿轮**。「在转」是必须写死的动态——否则模型会画成贴在墙上的浮雕。

- fact_id: stormwind.landmark.025
  claim: 矿道地铁是一条完全封闭的地下（且部分在水下）双轨线路，上面跑着两列各三节的车厢，出自侏儒的工程技术；水下段实际上是一个地下湖
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "a long, fully enclosed, underground (and partially underwater) set of double tracks upon which rolls two sets of three wagons, all credited to the gnomes' technical engineering." / "The underwater section of the tram is, in fact, a subterranean lake."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "地下车站：石砌拱顶隧道内并列两条铁轨，站台为石台、边缘包铁；一列三节的金属车厢停在轨上，车厢为铆接钢板、圆角、带观景窗；隧道深处黑暗，轨道向下延伸"
  negative: "单轨, 单节车厢, 木制车厢, 现代地铁, 电气化接触网, 自动闸机, 站台有文字标识"
  note: **「两列各三节」是可机检的硬数**。设计师是侏儒不是矮人——口播须说对（矮人区里的侏儒工程）。

- fact_id: stormwind.landmark.026
  claim: 矿道地铁的水下段能看见一座地下湖里的景象——沉船、巨蚌、潜水者、两名娜迦海妖、一头姥鲨，以及一只被叫作「Nessy」的大家伙
  tag: ✅
  source: Warcraft Wiki - Deeprun Tram
  source_url: https://warcraft.wiki.gg/wiki/Deeprun_Tram
  quote: "a treasure chest, a diver, shipwrecks, a large beast named 'Nessy', a giant clam, two Naga Sirens, and a Basking Shark"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "隧道穿过一段透明水下区间，车窗外是幽暗的地下湖：沉船残骸斜卧、巨大的蚌半开、远处一头长颈巨兽的剪影掠过"
  negative: "海水清澈明亮, 珊瑚礁, 热带鱼, 阳光射入, 现代水族馆玻璃"
  note: **一个上好的「彩蛋镜」** ——「Nessy」是尼斯湖水怪的致敬。旅行者坐电车时看窗外，是本站很自然的一个惊喜点。
```

### 2.7 运河、监狱与水上建筑（landmark.027–029）

```yaml
- fact_id: stormwind.landmark.027
  claim: 暴风城的水面上立着**两座**要塞式建筑，都是关押不法者的监狱——「监狱（The Stockade）」从法师区进入，另一座「金库（Vault）」四面环水
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Canals and prisons）
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_City
  quote: "There are two fortifications that rise from the waters in Stormwind - both are prisons for the lawless and evil. The Stockade is accessible from the Mage Quarter and holds murderers, gnolls, thieves, and other enemies of the kingdom. A similar prison, the Vault, is surrounded by water on all sides"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "运河水面上立着两座敦实的石砌方形堡垒，墙体近乎无窗、只在高处开细长射孔，基座直接从水里长出，水线处附着深色水痕与苔"
  negative: "有大窗的建筑, 尖顶塔楼, 木构, 岸上建筑, 单独一座"
  note: **「两座」常被漏掉** —— 大部分人只知道 Stockade。两座并存是很好的口播点（「这城的水上有两座监狱，其中一座从来没人进得去」）。

- fact_id: stormwind.landmark.028
  claim: 监狱（Stockade）位于环绕法师区的运河最北段；建筑门口旁立着集合石，真正的入口就在建筑内部、沿一小段敞开的台阶下去
  tag: ✅
  source: Warcraft Wiki - The Stockade
  source_url: https://warcraft.wiki.gg/wiki/The_Stockade
  quote: "Stormwind Stockade is located inside Stormwind City, on the northernmost section of the canal surrounding the Mage Quarter, the building is marked with a meeting stone directly next to its doorway, the actual entrance into the instance is directly inside the building, down the small, open set of stairs."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "水上堡垒的正面开一个不大的拱形门洞，门内即是一段向下的敞开石阶，阶下是黑暗；门外侧立着一块人高的刻纹立石"
  negative: "大门敞开可见大厅, 铁栅门, 地面平入无下沉台阶, 门口有卫兵亭"
  note: 「down the small, open set of stairs」＝**进门就往下走**，入口是下沉式的。这是可画的具体形制。

- fact_id: stormwind.landmark.029
  claim: 金库（Vault）在监狱对面，形制与监狱基本相同，区别是四面完全被水包围、且顶上有一面钟；它被一道闸门（portcullis）与两名卫兵封住，从未正式开放过——连内测阶段都没有
  tag: ✅
  source: Warcraft Wiki - Vault (Stormwind City)
  source_url: https://warcraft.wiki.gg/wiki/Vault_(Stormwind_City)
  quote: "It is currently inaccessible, gated off by a portcullis with two guards." / "the Vault has never been officially accessible, not even in alpha or beta."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "四面环水的方形石堡，正面一道铁制落闸（竖向铁栅）落下封死门洞，两名披甲卫兵一左一右持戟守在闸前；建筑顶部嵌着一面大钟"
  negative: "门开着, 木门, 有人进出, 顶上是塔尖而非钟, 建筑与岸相连"
  note: **本站最好的「悬念梗」**——一座游戏上线二十年从未打开过的建筑。口播价值极高，且画面上是一个封闭的铁闸特写，很好拍。与 arch.020（钟）是同一栋楼。
```

### 2.8 暴风要塞（landmark.030–034）

```yaml
- fact_id: stormwind.landmark.030
  claim: 暴风要塞在矮人区与老城区之间拔地而起，是王国的权力中枢；它高出城市本体，部分建在一处岩石高台上；要塞能俯瞰全城
  tag: ✅
  source: Warcraft Wiki - Stormwind City（Stormwind Keep）/ Stormwind Keep
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "Rising high between the Dwarven District and Old Town, the keep is the seat of power of the kingdom." / "The Keep offers a view of the whole city" / "above city level, being partially built unto a rocky outcropping"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城市北侧的岩石高台上耸立着庞大的要塞建筑群，明显高出周围街区一大截；从要塞前沿可以俯瞰整座城的屋顶与运河"
  negative: "要塞与街区同高, 建在平地, 被建筑遮挡看不见, 位于城市中心"
  note: **全城最大体量**（landmark.016）。俯瞰全城的机位就在这里——是本片航拍／全景镜的落点。

- fact_id: stormwind.landmark.031
  claim: 要塞是一座宏伟的城堡，比达拉然的紫罗兰城塞还大；屋顶铺蓝色石板，建筑群包含许多附属建筑、塔楼与厅堂，建筑之间以拱廊相连；城堡至少有五层；其中一座塔是狮鹫栖舍
  tag: ✅
  source: Warcraft Wiki - Stormwind Keep
  source_url: https://warcraft.wiki.gg/wiki/Stormwind_Keep
  quote: "a grand castle, bigger than the Violet Citadel of Dalaran. Its roof was shod with blue slate and the complex had many side buildings, towers, and halls. Arching galleries spanned between the buildings." / "The castle had at least five levels." / "One of the towers was a gryphon aviary"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "要塞为多体量组合的城堡群：主厅居中，四周簇拥着方塔与圆塔，塔顶覆深蓝灰石板；建筑与建筑之间以带连续券拱的高架廊道相连；整体高度约五层"
  negative: "单体城堡, 一座塔, 平屋顶, 建筑之间无连接, 红瓦屋顶"
  note: **⚠️ 时代边界**：此段原文描述的是**第一次战争前的旧要塞**（与 arch.024 同段）。重建后的要塞在游戏里沿用了这套语汇（蓝顶、多塔、拱廊），但「重建后仍如此」这一步是 ⚠️ 推测——须以 Vanilla 参考图对账。「比紫罗兰城塞还大」是可用的口播尺度比。

- fact_id: stormwind.landmark.032
  claim: 王座厅是一个穹顶形的大厅，厅中央是一张由金色狮子护卫两侧的巨大王座，这张王座被称为「狮子御座（Lion Seat）」；金色的王座上装点着彩绘玻璃，令林恩家族的血脉既慑人又鼓舞人心；王座四周环立着皇家卫队
  tag: ✅
  source: Warcraft Wiki - Throne room
  source_url: https://warcraft.wiki.gg/wiki/Throne_room
  quote: "This dome-shaped hall contains a large throne that is flanked by golden lions. The throne is known as the 'Lion Seat'" / "The golden throne is adorned with stained glass in which the Wrynn line intimidates as much as it inspires." / "it is found in the center of the room, surrounded by the Royal Guard"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "穹顶大厅：厅顶为半球形石砌穹窿；正中高起的台基上是一张镶金的王座，左右各蹲踞一尊金色狮子雕像；王座靠背嵌彩绘玻璃，光透过玻璃在台基上落下彩色光斑；台基四周环立披甲卫兵"
  negative: "平顶或尖拱顶大厅, 王座靠墙, 无狮子, 木王座, 空无一人, hex色值"
  note: **「穹顶 + 金狮夹峙 + 彩玻璃王座 + 居中而非靠墙」是四条可机检的硬形制**。⚠️ 但王座厅在 4.0.3a 被重做过，本描述可能反映的是现行版本；Vanilla 王座厅的样子须以参考图对账（§未查 Q5）。红地毯在文字来源里**没有**——任务书提到的「红地毯」查无实据，见 Q5。

- fact_id: stormwind.landmark.033
  claim: 王座厅后面连着地图室（map room），战场指挥官们在那里
  tag: ✅
  source: Warcraft Wiki - Throne room / Stormwind Keep
  source_url: https://warcraft.wiki.gg/wiki/Throne_room
  quote: "The throne room also grants access to the map room behind it, containing the battlemasters" / "the Map room ... first door, straight ahead through the throne room from the main hall"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "王座厅正后方一道门通向地图室：室中央一张大木桌，桌面摊着大幅羊皮地图，压着镇纸与小旗，四周站着披甲军官"
  negative: "沙盘, 电子屏, 全息投影, 地图挂墙为主, 房间在侧面"
  note: **动线是「主厅 → 穿过王座厅 → 正前方第一道门」**，可直接用于运镜设计。

- fact_id: stormwind.landmark.034
  claim: 皇家画廊（Royal Gallery）是要塞里的一个小房间，在一座小庭院花园之后、皇家图书馆旁边；里面陈列着美术品与宏伟的雕像，雕的是玛拉·佛德拉贡、莱恩国王、戴林·普罗德摩尔等名人
  tag: ✅
  source: Warcraft Wiki - Royal Gallery
  source_url: https://warcraft.wiki.gg/wiki/Royal_Gallery
  quote: "The Royal Gallery was a little room beyond the small courtyard park of Stormwind Keep, next to the Royal Library. The gallery featured fine art and grandiose statues of illustrious personas such as Mara Fordragon, King Llane, and Daelin Proudmoore."
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "要塞内一间不大的陈列室：石墙上挂着装框画作，室内立着三尊等身以上的人物石像，各据一隅；室外隔着一个小庭院花园，另一侧门通向图书馆"
  negative: "大型美术馆, 玻璃展柜, 射灯, 展签文字, 雕像为半身像"
  note: **Vanilla 时它是开放的**——大灾变中雕像被死亡之翼震坏后才对公众关闭。所以本片（Vanilla 锚点）**可以进去拍**，这是一个现行版本已经看不到的内景，价值高。动线：小庭院花园 → 画廊 → 皇家图书馆。
```

### 2.9 公园区（landmark.035–036，Vanilla 限定）

```yaml
- fact_id: stormwind.landmark.035
  claim: 公园区位于暴风城西角，原本是给市民休闲用的地方，后来成了来访夜精灵的栖身处——他们在这里能从暴风城本体那些一望无际的石头大道中喘一口气；从教堂广场往西南、或从法师区往西北可以到
  tag: ✅
  source: Warcraft Wiki - Park
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "a place devoted to leisure activities for Stormwind's populace" / "a refuge for visiting night elves, who found the comforting presence of nature a welcome respite from the vast stone thoroughfares of Stormwind proper" / "the district located in the western corner of Stormwind City"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "公园区：与全城的白石硬铺完全不同——地面是草与土径，高大乔木成荫，树影斑驳；建筑稀疏、体量小、依树而建，不与树争高"
  negative: "石板广场, 白石建筑为主, 修剪整齐的法式花园, 喷泉, 硬质铺装, 空旷无树"
  note: **本片最重要的 Vanilla 限定内容之一**——公园区在 4.0.3a 被死亡之翼彻底摧毁，现行版本是 Lion's Rest 纪念园。Vanilla 锚点下它**必须是完好的绿地**。它同时是全城的**材质对比项**（唯一非石质环境）。

- fact_id: stormwind.landmark.036
  claim: 夜精灵在公园广场的正中央造了一口月亮井；这里是整个东部王国唯一有德鲁伊训练师的地方，夜精灵大师们围着月亮井传授德鲁伊之道
  tag: ✅
  source: Warcraft Wiki - Park
  source_url: https://warcraft.wiki.gg/wiki/Park
  quote: "The night elves created a Moonwell in the center of the park square." / "The only place in the Eastern Kingdoms where druid trainers resided"
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "公园中心是一口月亮井：圆形浅池，池沿为浅色石材雕出的花瓣状边缘，池水呈自发光的乳白偏冷蓝色，水面极静并向上散出微弱光雾；池周围环立着几名长耳的紫肤精灵"
  negative: "普通喷泉, 水柱喷射, 井口深洞, 池水普通透明, 池边有栏杆, hex色值"
  note: **月亮井是公园区的视觉核心**，且「自发光的水」是一个很出片的元素。它与全城的白石＋蓝形成温度差（月亮井是冷的、教堂的钴蓝是硬的、矮人区的炉火是暖的）——这三点正好构成全片的色温三角。
```

---

## 综合 · 暴风城建筑语汇表

> 下面每一项是一个**可复用的锁定串**：凡该元素入画的镜，原样复现，不要改写。色名一律中文色名，零 hex。

| 项 | 锁定串（直接粘进 prompt） | 依据 | 负向词 |
|---|---|---|---|
| **墙 / 主体材质** | 暖白色石灰岩砌体，石块方正、灰缝细密、表面经年略泛米白与浅灰，墙体厚重，砌缝齐整并刷白 | arch.001 / arch.006 | 红砖, 混凝土, 玻璃幕墙, 抹灰, 木板房, 夯土, 瓷砖 |
| **屋顶** | 深蓝灰色石板瓦，瓦片薄而层叠，边缘厚薄不匀，雨后反浅冷光 | arch.002（⚠️ 形状看图定 arch.003） | 红瓦, 琉璃瓦, 茅草, 金属波纹板, 沥青瓦 |
| **街道 / 铺地** | 宽阔石板大道，大块灰白石板与卵石交错拼砌，纹路纵横，缝隙积细尘，被行人磨得光滑反光 | arch.005 / arch.006 / arch.008 | 土路, 柏油, 水泥, 窄巷为主, 木栈道, 整版同向铺砖 |
| **窗** | **（未锁定——见 §未查 Q1，须看参考图）** | — | — |
| **门（民用）** | 门洞偏矮偏窄，门楣压低，成年人进门需略低头；石砌门套，木门扇带铁件 | arch.023 | 高大双开门, 通高玻璃门, 自动门 |
| **城门** | 巨大白石门洞，进深极大如穿隧道，高过森林树冠；门外两侧各架一台木制重弩炮 | arch.006 / arch.011 / landmark.001 | 城门低矮, 木门为主体, 火炮, 门洞浅 |
| **纹章** | 银白底，正中一枚正面朝前的金色狮首，狮首外缘镶一道钴蓝细边；外圈金色边框同样镶钴蓝细边 | arch.009 / arch.010 | 鹰纹, 龙纹, 十字, 侧面狮身, 站立狮, 双狮, 红底, 黑底 |
| **旗帜 / 幡** | 城垛与门侧垂挂狮纹长幡，蓝底金狮，布面厚重、下摆略有配重、随风缓摆 | arch.009 | 三角小旗, 塑料旗, 现代旗杆, 旗面有文字 |
| **石雕狮** | 城垛上等距立着石雕狮像，正面蹲踞，白石同体，风化感轻微 | arch.009 | 石狮子（中式）, 青铜狮, 卧狮, 咆哮张口 |
| **运河** | 明净的蓝绿色水面微微反光，砌石护岸，近景水面浮细碎木屑草屑；间或探出小块木质／石质码头 | arch.013 / arch.014 | 浑浊黑水, 混凝土渠, 干涸, 现代游艇, 垃圾 |
| **桥** | 厚重白石拱桥，桥拱高起，两侧实心石栏板，栏板顶面磨得发亮 | arch.007 | 铁桥, 木桥, 吊桥, 平桥, 镂空金属栏杆 |
| **绿化** | 石砌街区间点缀结果的苹果树，树冠不大，深绿叶片间挂红果，树下石板地 | arch.012 | 棕榈, 松树, 樱花, 热带植物, 大片草坪, 无树 |
| **招牌** | 店门上方以曲铁臂悬挑一块**空白**木牌，铁件吊挂、随风微晃，牌面只有木纹与铁钉；或以实物幌子代替（铁壶／剑／谷穗） | arch.026（⚠️） | **任何文字、字母、汉字、数字、印刷体、手写体、灯箱、霓虹、logo** |
| **街具 / 火盆 / 街灯** | **（未锁定——见 §未查 Q1，须看参考图）** | — | — |

**全片画面文字纪律（硬约束）**：暴风城画面**一律零文字**。招牌画成空白木牌或纹样牌、雕像基座铭牌画成空白石板、车站与店铺无任何标识文字。店名与铭文只走**口播**与**后期贴字**。负向词固定挂：`任何文字, 字母, 汉字, 数字, 印刷体, 手写体, 招牌文字, 碑文, 门牌号, logo, 二维码`。

**色温三角（全片配色骨架，按镜条件化，勿写进全片共用串）**：
- **冷白＋钴蓝** ＝ 城市本体与大教堂内厅（arch.001 / landmark.018）
- **暖橙火光＋灰白烟霭** ＝ **仅**矮人区（landmark.022 / landmark.023）
- **自发光的乳白冷蓝** ＝ **仅**公园区月亮井（landmark.036）

> ⚠️ 按 `CLAUDE.md` 的光源自检条（`ai_video.md` 16.9）：**`渲染样式:` 是全镜共用串，上面三组光色一条都不许写死进去**。矮人区的暖橙火光、月亮井的自发光，必须写成**按镜条件化的分句**，且没有该光源的镜要**反向声明**（例如贸易区日景镜须写「本镜画面里没有任何炉火，也没有任何暖橙色光源」并挂灭火负向组）。

---

## 综合 · 四大机构地标形制卡

> 每段可直接作为该主体锚点图 prompt 的**形制骨架**（下游再按 rule 4d §B 扩写到 ≥1500 字）。

### 卡一 · 王座厅（暴风要塞内）

穹顶大厅。厅顶为半球形石砌穹窿，肋券自四周向顶心收拢。厅体为暖白色石灰岩砌筑，墙面高处开细长券窗，光柱斜切入厅。大厅正中、而非靠墙一端，是一处高起数级的石砌台基；台基上是一张镶金的巨大王座，王座左右各蹲踞一尊金色狮子雕像，与王座同高。王座靠背嵌着彩绘玻璃，光透过玻璃在台基石面上落下彩色光斑。台基四周环立着披甲卫兵，持长戟、面朝外。王座厅正后方一道门通向地图室：室中央一张大木桌，桌面摊开大幅羊皮地图，压着镇纸与小旗，四周站着披甲军官。

*依据*：landmark.032 / landmark.033。*负向*：平顶或尖拱顶, 王座靠墙, 无狮子, 木王座, 空无一人, 沙盘, 电子屏, 全息投影, 任何文字。
*⚠️ 版本注*：王座厅在补丁 4.0.3a 被重做，本卡描述可能反映现行版本；Vanilla 形态须以参考图对账（Q5）。**「红地毯」在文字来源中查无实据，未写入本卡。**

### 卡二 · 光明大教堂（教堂广场）

巨大的石造教堂，主体两侧伸出多组侧翼，屋脊之上林立着数量众多的细长尖塔，尖塔高低错落、越靠中心越高——不是常见的对称双塔正立面，而是一片尖塔森林。外墙为暖白色石灰岩。教堂完全统治教堂广场的北端，广场两侧是较矮的公共建筑（市政厅、孤儿院），衬得教堂更高。内厅为浅暖白石砌筑，墙面与地面嵌有饱和的钴蓝色石材条带与几何镶嵌，蓝白对比强烈；空间高敞，光线自高窗斜落，气氛安静。祭坛左右两侧**各有**一道向下的石阶通道，隐在列柱阴影里，阶下是低矮的石砌拱顶墓穴，壁龛中安放石棺，烛光昏黄。钟室内一口巨大的青铜钟悬于粗木梁下，钟体表面有矮人风格的錾刻纹样与铆接感边饰——它是在铁炉堡的大熔炉上铸成的。

*依据*：landmark.016 / 017 / 018 / 019 / 020。*负向*：单塔教堂, 圆顶教堂, 对称双塔, 全金内饰, 木质内饰, 暗色内饰, 祭坛正后方下楼, 单侧楼梯, 铁钟, 电灯, 任何文字。
*未锁定*：尖塔**具体数量**、正立面是否有玫瑰窗／彩绘玻璃窗、正门台阶级数——文字来源全无，须看参考图（Q1）。

### 卡三 · 巫师圣殿（法师区）

一座独立高塔，统领整个法师区，是该区最高的建筑。塔身石造，外壁**大面积爬满深绿藤蔓**，藤蔓沿石缝攀至塔身中上部，越往上越稀。塔顶收束为尖锥。塔身外壁盘绕着一道向上的石径／外挂坡道，无扶手或仅有矮石栏，绕塔数圈通向塔顶平台——不用飞行就只能这样上去。塔的四周是两层的裁缝铺与仓库，门口堆着捆扎的布匹与封蜡的陶罐；沿街有露天咖啡座，桌上是冒热气的杯子。

*依据*：landmark.012 / 013 / 014。*负向*：光洁无植被的塔, 金属塔, 玻璃塔, 藤蔓覆盖全塔遮住石材, 多塔并立, 塔内楼梯为唯一通路, 外挂铁梯, 电梯, 传送门, 漂浮的魔法装置, 水晶球, 任何文字。
*⚠️ 版本红线*：**塔内绝不能画成传送门大厅**——那是补丁 8.1.5 的改造（X7）。Vanilla 时塔内是法师训练场所。
*⚠️ 待核*：外挂坡道仅 `ai_draft`（Q3）；「紫色尖塔群」「内部环形楼梯」「漂浮魔法装置」「水晶球」在文字来源中**均查无实据**，本卡未采用，须以参考图定夺。

### 卡四 · 矿道地铁暴风城端车站（矮人区东侧）

隧道口被一只**巨大的、正在缓缓转动的**金属齿轮环绕，齿轮竖立，齿牙粗大，金属表面是暗黄铜与铁灰的混合，带铆钉与油渍；齿轮内圈即是通向地下的拱形洞口。洞口向下，深处黑暗。站内为石砌拱顶隧道，并列两条铁轨，站台为石台、边缘包铁。轨上停着一列**三节**的金属车厢，车厢为铆接钢板、圆角、带观景窗。隧道内空气里悬着矮人区飘来的薄灰霭，炉火的橙光只到洞口为止，再往里只有冷色的石头。

*依据*：landmark.024 / 025。*负向*：静止齿轮, 小齿轮, 装饰浮雕齿轮, 现代工业齿轮, 电动机, 单轨, 单节车厢, 木制车厢, 现代地铁, 电气化接触网, 自动闸机, 站台标识, 任何文字。
*硬数*：全线是**双轨**、跑**两列各三节**的车厢——单条站台画一列三节即可。设计者是**侏儒**（不是矮人）。

---

## 参考图候选表

> **版权总则**：下表全部图像均为**暴雪娱乐版权**（或 Warcraft 电影版权）。按合理使用只作**形制依据**——**一律不入画、不上传给任何生成模型**。下游建参考图库时，这些图供**人眼看形制**，AI 只吃我们据此写出的**文字 prompt**。
>
> `已开` ＝ 本 worker 本次实际打开过该文件页并读到版权与元数据；`列出` ＝ 该文件名出自 `Stormwind_City` 条目 wikitext 的逐字图片清单，URL 按 wiki 标准 `File:` 路径构造（路径规则已由已开的三例验证），但本 worker 未逐一打开。

| # | URL | 类型 | 版本 | 版权 | 证明哪个 fact_id | 能否入画 |
|---|---|---|---|---|---|---|
| R1 | https://warcraft.wiki.gg/wiki/File:Stormwind_City_Classic.jpg | 官方截图（**已开**，2400×1350，来源＝暴雪官方 WoW Classic 城市导览） | **Vanilla ✅** | Blizzard | arch.001/002/005/016, landmark.001 | ❌ 仅形制依据 |
| R2 | https://warcraft.wiki.gg/wiki/File:OverviewStormwind.JPG | 官方粉丝站素材包截图（**已开**，2006 年上传，标注 "Entrance as seen before Cataclysm"） | **Vanilla ✅** | Blizzard 粉丝站授权 | landmark.001/002/003 | ❌ |
| R3 | https://warcraft.wiki.gg/wiki/File:Stormwind_Location_Plan.jpg | **电影宇宙**地图（**已开**——邓肯·琼斯推特发布） | **电影，非游戏 ❌** | Warcraft 电影 | 无 | ❌ **且不得作游戏形制依据**（见 X13） |
| R4 | https://warcraft.wiki.gg/wiki/File:Stormwindmapmanual.jpg | 《魔兽世界》游戏手册内的城市地图（列出） | **Vanilla ✅** | Blizzard | arch.016, 全城布局 | ❌ |
| R5 | https://warcraft.wiki.gg/wiki/File:VZ-Stormwind_City-old1.jpg | 补丁 3.0.2 之前的城市地图（列出） | **Vanilla ✅**（最贴） | Blizzard | arch.016/017, 各区相对位置 | ❌ |
| R6 | https://warcraft.wiki.gg/wiki/File:VZ-Stormwind_City-old2.jpg | 补丁 4.0.3a 之前的城市地图（列出） | WotLK（含港口） | Blizzard | X1 对照 | ❌ |
| R7 | https://warcraft.wiki.gg/wiki/File:Stormwind_City_plan_December_2001.jpg | 2001 年 12 月的城市布局规划图（列出） | 开发期 | Blizzard | arch.017（九个区） | ❌ |
| R8 | https://warcraft.wiki.gg/wiki/File:WorldMap-Stormwind-Early.jpg | Alpha 期地图（列出） | 开发期 | Blizzard | arch.017 | ❌ |
| R9 | https://warcraft.wiki.gg/wiki/File:Stormwind_-_Development.png | 「暴风城被创建的第一天」（列出） | 开发期 | Blizzard | arch.018（无屋顶） | ❌ |
| R10 | https://warcraft.wiki.gg/wiki/File:The_Trade_District.jpg | 贸易区截图（列出） | 需核 | Blizzard | landmark.008/009 | ❌ |
| R11 | https://warcraft.wiki.gg/wiki/File:Old_Town.jpg | 老城区截图（列出） | 需核 | Blizzard | landmark.010/011 | ❌ |
| R12 | https://warcraft.wiki.gg/wiki/File:The_Mage_Quarter.jpg | 法师区截图（列出） | 需核 | Blizzard | landmark.012/013/014 | ❌ |
| R13 | https://warcraft.wiki.gg/wiki/File:Cathedral_Square.jpg | 教堂广场截图（列出） | 需核（注意 landmark.021 换像） | Blizzard | landmark.016/017/021 | ❌ |
| R14 | https://warcraft.wiki.gg/wiki/File:The_Dwarven_District.jpg | 矮人区截图（列出） | 需核 | Blizzard | landmark.022/023/024 | ❌ |
| R15 | https://warcraft.wiki.gg/wiki/File:The_Park_banner.jpg | 公园区区旗（列出，标注「大灾变中移除」） | **Vanilla ✅** | Blizzard | landmark.035 | ❌ |
| R16 | https://warcraft.wiki.gg/wiki/File:Cathedral_Square_banner.jpg | 教堂广场区旗（列出） | — | Blizzard | arch.009（区旗纹样） | ❌ |
| R17 | https://warcraft.wiki.gg/wiki/File:Dwarven_District_banner.jpg | 矮人区区旗（列出） | — | Blizzard | arch.009 | ❌ |
| R18 | https://warcraft.wiki.gg/wiki/File:Mage_Quarter_banner.jpg | 法师区区旗（列出） | — | Blizzard | arch.009 | ❌ |
| R19 | https://warcraft.wiki.gg/wiki/File:Old_Town_banner.jpg | 老城区区旗（列出） | — | Blizzard | arch.009 | ❌ |
| R20 | https://warcraft.wiki.gg/wiki/File:150px-Perfect_flag_of_Stormwind.jpg | 暴风城旗帜（列出） | — | Blizzard | arch.009/010 | ❌ |
| R21 | https://warcraft.wiki.gg/wiki/File:The-Former-Stormwind-Gardens.jpg | 公园区废墟（列出） | **大灾变后 ❌** | Blizzard | X3 反例 | ❌ |
| R22 | https://warcraft.wiki.gg/wiki/File:Stormwind_City_at_night.jpg | 暴风城夜景（列出） | 需核 | Blizzard | 夜镜光线参考 | ❌ |
| R23 | https://warcraft.wiki.gg/wiki/File:Onyxia%27s_head_in_Stormwind.jpg | 奥妮克希亚头颅悬挂（列出） | **Vanilla 机制 ✅** | Blizzard | landmark.007 | ❌ |
| R24 | https://blizzardwatch.com/gallery/stormwind-city/ | 「WoW Classic Gallery: Stormwind City as it was in vanilla WoW」30 张图集 | **Vanilla ✅** | Blizzard（媒体转载） | 全区形制通查 | ❌ |

**下游建库建议（优先级）**：R1 → R24 → R5 → R4 → R15 → R23 是本片的**Vanilla 六件套**，先看这六组；R10–R14 的各区截图**必须先核版本**（wiki 上很多区景图是大灾变后的重制版），核不出版本就别用。每个场景主体按 rule 4d 建 ≥8 张库时，**至少 3 张须来自明确标注 Vanilla / pre-Cataclysm 的图源**。

---

## 版本错置清单（❌ · 全部不得出现在本片画面中）

> 判定口径：以下特征**在经典旧世 Vanilla（1.x）不存在**。每条附补丁号与出处，可直接进口播的「误传澄清」段。

| # | 错置内容 | 实际引入时间 | 出处 quote | fact 关联 |
|---|---|---|---|---|
| **X1** | **暴风城港口（Stormwind Harbor）** ——码头、船坞、沿墙火炮、攻城器械 | **补丁 3.0.2（2008-10-14，巫妖王之怒）** ——**不是大灾变**，任务书此处需订正 | `"Patch 3.0.2: Stormwind Harbor added."` | arch.011 |
| **X2** | 暴风城郊外（Stormwind City Outskirts）、暴风城湖（Stormwind Lake）、**暴风城公墓** | 补丁 4.0.3a（2010-11-23） | `"Patch 4.0.3a: Texture revamp. Park destroyed, Stormwind City Outskirts opened."`；公墓页 `"Patch 4.0.3a (2010-11-23): Added."` | landmark.035 |
| **X3** | **公园区被毁 / 焦土 / 缺口** | 补丁 4.0.3a——Vanilla 时公园区**完好**，有月亮井与夜精灵 | `"Park destroyed"` | landmark.035/036 |
| **X4** | 狮王安息地（Lion's Rest）、瓦里安之墓、旧兵营重建 | 补丁 7.0.3 | `"Patch 7.0.3: The ruins of the Park and the Old Barracks are rebuilt into the Lion's Rest memorial gardens."` | — |
| **X5** | 暴风城大使馆（Stormwind Embassy） | 补丁 7.3.5 | `"Patch 7.3.5: Stormwind Embassy added."` | — |
| **X6** | 法师区上方高台的**肯瑞托营地与传送门** | 补丁 6.0.2 | `"Patch 6.0.2: A small Kirin Tor encampment with a portal added on a plateau overlooking the Mage Quarter."` | landmark.012 |
| **X7** | **巫师圣殿内的传送门大厅（Portal Room）** ——成排通往各地的传送门 | 补丁 8.1.5 | `"With patch 8.1.5, the tower's interior was completely revamped to house the Stormwind Portal Room"` | landmark.013/014 |
| **X8** | **教堂广场的乌瑟尔雕像 / 乌瑟尔纪念喷泉** | 补丁 4.0.3a——Vanilla 时是**阿隆索斯·法奥纪念碑** | `"The square originally featured a monument to Alonsus Faol, which was replaced after the Cataclysm with a statue of Uther the Lightbringer."` | landmark.021 |
| **X9** | 暴风要塞的**露天大道 + 喷泉 + 瓦里安雕像**入口、重做的王座厅、可俯瞰暴风城湖的花园 | 补丁 4.0.3a——Vanilla 时通往王座厅的路是**封闭的**，不是露天 | `"In Cataclysm, Stormwind Keep was entirely remodeled... The path leading to the throne room is now open air and redesigned, complete with a grand walkway and a fountain."` | landmark.030/032 |
| **X10** | **矮人区的拍卖行与皇家银行（Royal Bank of Stormwind）** | 补丁 4.0.3a——Vanilla 时矮人区**没有**拍卖行和银行 | `"the addition of the Dwarven District's Royal Bank of Stormwind in patch 4.0.3a"` | landmark.022 |
| **X11** | 死亡之翼留下的**焦黑爪痕**、倒进水里的达纳斯·托尔贝恩雕像、损毁的入口塔楼与钟楼 | 大灾变事件；补丁 5.2.0 修复 | `"Patch 5.2.0: Entrance towers, the statue of Danath Trollbane, and the clocktower have been restored."` | landmark.004, arch.020 |
| **X12** | **人物站在屋顶上 / 可行走的屋面 / 屋顶花园** | 飞行坐骑加入后才为暴风城补的屋顶几何——Vanilla 时**城里没有屋顶** | `"Stormwind had to be modified to accommodate this, as the city didn't possess any rooftops."` | arch.018 |
| **X13** | 把 `Stormwind_Location_Plan.jpg` 当作游戏概念图 | 它是**魔兽电影宇宙**的地图（导演邓肯·琼斯发布），与游戏形制无关 | `"This image was taken from Warcraft film universe material."` | R3 |
| **X14** | 把 **Olivia's Pond** 当作法师区的池塘 | 它在 4.0.3a 之后的**城外郊区** | `"Olivia's Pond is a small body of water located in the Stormwind City Outskirts."` | landmark.015 |
| **X15** | 4.0.3a 的**全城贴图重制**外观（更高分辨率、更细腻的石材与木纹） | 补丁 4.0.3a `Texture revamp` | `"Patch 4.0.3a: Texture revamp."` | arch.001 |
| **X16** | 奥妮克希亚头颅仍挂在城门上 —— 反向错置：这是 **Vanilla 有、现行没有** | 1.3.0 加入，3.2.2（2009-09-22）移除 | `"This no longer happens as of 3.2.2."` | landmark.007 |

**另有一处 Vanilla 独有、现行已无的内容**（不是错置，是**该画而容易漏画**的）：老城区与贸易区之间、一道大铁闸后面有一个**从未启用的副本入口**，原本是为玩家住宅区准备的，在大灾变中被移除。出处：`"The unused instance portal behind a large portcullis between the Old Town and the Trade District (removed in Cataclysm) was originally meant to lead to the player housing area."`（`stormwind.landmark.037`，T1，ai_read，https://warcraft.wiki.gg/wiki/Stormwind_City ）。**这是又一个绝佳的口播悬念点**，和金库（landmark.029）是一对：这城里有两处永远打不开的门。

---

## 未查 / Open questions

> 以下是本 worker **确实没能从文字来源查到**的形制细节。一条都没有编。全部须由**人眼看参考图**（§参考图候选表）定夺，定完回填本文并升 `human`。

- **Q1（最重要）· 窗 / 门 / 屋顶形状 / 街灯 / 火盆 / 遮阳篷的具体形制。** Warcraft Wiki 的所有地标条目**只写功能不写形制**（贸易区条目原文自承 `"The article conspicuously lacks descriptive detail about architectural features"`）。所以：窗户是尖拱还是圆拱、有没有铅条玻璃、街灯是壁挂式还是立杆式、市集摊位的遮阳篷是什么材质与颜色——**文字来源零覆盖**。这也是「语汇表」里「窗」与「街具」两格留空的原因。**下游必须先看图再写 prompt，不要从本文推。**
- **Q2 · 阿隆索斯·法奥纪念碑（Vanilla 教堂广场）的具体形制。** 只知道它是 monument 而非 statue（landmark.021），碑体形状、高度、有无人像浮雕全未知。须找 Vanilla 期教堂广场截图（R13 须先核版本，或走 R24 图集）。
- **Q3 · 巫师圣殿的外观分歧。** 三处说法互不一致：① RPG 设定书说是「爬满藤蔓的塔」（T2, ai_read）；② 社区指南说有「绕塔外壁的石径」（T3, ai_draft）；③ 任务书假设的「紫色尖塔群 / 内部环形楼梯 / 漂浮魔法装置 / 水晶球」**在任何文字来源里都查无实据**。**必须看图裁决**，三者可能都对（藤蔓在下、尖塔在上、坡道在外）也可能有错。
- **Q4 · 法师区水面的名称与形制。** 游戏里法师区确有水面，但它**没有已知的正式名称**（Olivia's Pond 不是它，见 X14）。形状、护岸、周边树木全未知。
- **Q5 · Vanilla 王座厅的样子。** landmark.032 的「穹顶 + 金狮 + 彩玻璃王座」描述可能反映的是 4.0.3a 重做后的版本（X9）。Vanilla 王座厅是什么样，须找 Vanilla 期要塞内景图。**顺带：任务书提到的「红地毯」在文字来源中查无实据，本文未采用。**
- **Q6 · 大教堂尖塔的具体数量、正立面构成、有无玫瑰窗。** 只知道 "many wings and spires"（landmark.017），数量与立面组织未知。玫瑰窗 / 彩绘玻璃**外窗**在文字来源里没有（内厅的 cobalt 镶嵌是有的，见 landmark.018；王座的彩绘玻璃是有的，见 landmark.032——但那是**王座上**不是教堂窗上，别串）。
- **Q7 · 民居与商铺的层数与立面组织。** 只知道银行门洞矮（arch.023）、老城区层高参差（landmark.010）。平民住宅是几层、是否前店后宅、有无外挑楼层，全未知。
- **Q8 · `Head_of_Onyxia_(Classic)` 的「left arch」方位。** landmark.007 是本片最有价值的 Vanilla 专属画面，但只有 `ai_draft`。**须人眼开一次原页确认左／右**，再决定画在哪一侧。
- **Q9 · 矮人区建筑的矮人化程度。** 条目只写了炉、砧、烟（landmark.022/023），**没写**建筑本身是否是矮人式石构 + 铆接金属（任务书的假设）。是矮人把暴风城的白石房子改造了，还是原样用？须看图。
- **Q10 · 英雄谷五尊雕像的具体姿态。** 只有名字与铭文（landmark.004/005），**姿态、持物、朝向全无文字描述**。五尊各是什么造型须看图。

---

## §4 统计

- **事实总数 62**（`stormwind.arch.001–026` 计 26 条 + `stormwind.landmark.001–036` 计 36 条；另有 `landmark.037` 以散文形式记在 §版本错置清单末尾）——**超出 ≥40 的目标**
- **`ai_read` 59 条 / `ai_draft` 3 条**（ai_draft 仅 `arch.004`、`landmark.007`、`landmark.014` 三条，已在各自 note 中标注待人眼复核；**三条均未进任何锁定串**）——**ai_read 59 ≫ ≥34 的目标**
- **标签分布**：✅ 51 · ⚠️ 10 · ❌ 1（`landmark.015`）；另有 §版本错置清单单列的 16 条 ❌（X1–X16，以表格而非 YAML 承载）
- **参考图候选 24 组**（3 组已开页核对版权与元数据，21 组出自 `Stormwind_City` 条目 wikitext 的逐字图片清单）
- **tier 分布**：T0 2 条（暴雪官网官方导览）· T1 50 条（Warcraft Wiki 带游戏内出处段落 + 逐字补丁说明 + 开发者自述）· T2 2 条（RPG 设定书转述）· T3 8 条（美术随笔 / 纹章站 / 社区指南）
- **零 hex 已机检通过**（全文无 `#RRGGBB` 形式的色值，颜色一律色名）

### 与其他路的交接

- **`landmark.024–026` + 形制卡四 与 W7（`w7_deeprun_tram.md`）重叠。** 分工建议：**W7 是该线的权威**（命名、建造史、运营、可拍性），本文只保留**暴风城端车站的形制**（齿轮、站台、车厢外观），合并 dossier 时以 W7 为准、本文作形制补充。
- **译名已按 W7 的考据统一为「矿道地铁（Deeprun Tram）」**，本文原稿依任务书写的「深铁矿道」已全量替换。W7 查证简中官方译名为「矿道地铁」，「深铁矿道」查无官方出处。
- **`landmark.035–036`（公园区 / 月亮井）** 若 W 路里有专管夜精灵或公园区的，以那一路为准，本文只出形制。
- **域可达性**：`warcraft.wiki.gg` ✅ / `worldofwarcraft.blizzard.com` ✅ / `news.blizzard.com` ✅（正文仅 NPC 名录）/ `drawshield.net` ✅ / `youcangothere.substack.com` ✅ / **`*.fandom.com` ✖ 全部返回 HTTP 402**（wowpedia、wowwiki-archive、vanilla-wow-archive、classic-wow-archive 均不可达）——这是本次最大的来源损失，`vanilla-wow-archive` 本可给出最贴版本的描述。**若后续需要补 Q1–Q10，建议换出口重试 fandom 系，或直接看图。**
