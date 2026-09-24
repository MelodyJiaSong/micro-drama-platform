---
worker_id: g13-northshire-goldshire-detail
stage: 0
role: researcher
angle: map-g13-northshire-goldshire
status: complete
blockers: []
confidence: medium
---

# G13 备注 · 北郡山谷 + 闪金镇（建筑级）

本文件**只放不属于树的东西**。凡是节点字段能装下的信息（名字 / 父子 / 坐标 / 长相 / 备注 / 出处），
一律只写在 `g13_northshire_goldshire_detail.yaml` 里，这里不复述（仓库规则「一份东西只有一个出处，副本必漂」）。

---

## 0. 先读这条：`verified_by` 认证的是**位置**，不是**长相**

这是本片区最容易被下游误读的一点，写在最前面。

- YAML 里 55 个节点标了 `ai_read`。它们认证的是：**这个地方存在、叫这个名字、在那个相对位置**——
  每一条都附了我真的抓到的那一页的英文原句。
- **`look_zh` 几乎全部是 `ai_draft`**，与该节点的 `verified_by` 无关。
  原因见 §3：wiki 的文字里**基本没有「长什么样」**。`look_zh` 是我按
  「人类·暴风城建筑族系 + 艾尔文森林金秋色调」这两条已知风格前提推的，
  用途是**给分镜一个可以直接生成的起点**，不是考据结论。
- 因此：**凡要把 `look_zh` 当成锁定串写进 prompt 之前，必须先按 §6 的清单过一遍参考图。**
  这和 sk2 在暴风城上踩过的是同一堵墙（`ai_videos/shikong_lvxing/sk2/0_research/parts/w1_city_layout.md`
  § 本路说明第 3 条：城市的「长什么样」主要存在于游戏资产里、不在文字里）。

---

## 1. 自查对账

### 1.1 真的抓到并读了的页（52 页，全部来自 `warcraft.wiki.gg`）

**地点页（17 次抓取，覆盖 14 个条目，部分页按不同追问抓了 2–3 次）**

`Northshire_Valley`（×3）· `Northshire_Abbey`（×2）· `Northshire`（重定向到 Northshire Valley）·
`Main_Hall_(Northshire)` · `Hall_of_Arms_(Northshire)` · `Library_Wing_(Northshire)` ·
`Northshire_River` · `Northshire_Vineyards` · `Echo_Ridge_Mine` · `Northshire_Guard` ·
`Goldshire`（×3）· `Lion's_Pride_Inn` · `Crystal_Lake` · `Elwynn_Forest` ·
`Fargodeep_Mine` · `Jasperlode_Mine` · `Stormwind_Gate`

**NPC 页（35 个，抓它们是为了拿信息框坐标 + 「他站在哪栋房子里」那一句）**

闪金镇侧：`Smith_Argus` `Marshal_Dughan` `Innkeeper_Farley` `Erma` `Tharynn_Bouden`
`Corina_Steele` `Kurran_Steele` `Brother_Wilhelm` `Helene_Peltskinner` `Lee_Brown`
`Adele_Fielder` `Jason_Mathers` `Priestess_Josetta` `Michelle_Belle` `Zaldimar_Wefhellt`
`Keryn_Sylvius` `Maximillian_Crowe` `Remen_Marcot` `Tomas` `Toddrick` `Brog_Hamfist`
`Barkeep_Dobbins` `William_Pestle`

北郡侧：`Marshal_McBride` `Deputy_Willem` `Brother_Paxton` `Milly_Osworth` `Khelden_Bremen`
`Brother_Sammuel` `Llane_Beshere` `Priestess_Anetta` `Jorik_Kerridan` `Drusilla_La_Salle`
`Eagan_Peltskinner` `Garrick_Padfoot`

**关键方法**：wiki 的**地点页几乎不写长相**，但**NPC 页写「他在哪一间屋子」并在信息框给坐标**。
本片区的建筑级精度几乎全部是从 NPC 页反推出来的——
狮王之傲旅店的一楼 / 后厨 / 地窖 / 二楼三间房，
修道院的武器大厅右起第二三间 / 图书馆一层与二层 / 楼梯间，
全是这么拿到的。**下游做别的片区时请直接复用这个套路。**

### 1.2 抓不到的源（逐条记，供下游别再白撞一次）

| 源 | 结果 | 说明 |
|---|---|---|
| `www.wowhead.com/classic/zone=9` | **HTTP 403** | 任务书给的 `&xml` 绕法在本机同样 403，整站不可达 |
| `warcraft.huijiwiki.com` / `wow.huijiwiki.com` | **HTTP 403** | 与 sk2 的既有结论一致（灰机 wiki 全站对本机 403）。中文译名只能靠搜索结果摘要 |
| `wowwiki-archive.fandom.com`（旧 WoWWiki，旧世时期文本） | **HTTP 402** | Fandom 整站对本机 402。这是最可惜的一个——它保存着 Vanilla 时期的原始描述 |
| `classic-wow-archive.fandom.com` / `turtle-wow.fandom.com` | 同上 402 | 未单独重试 |
| `database.turtle-wow.org` | **DNS ENOTFOUND** | 域名解析不到 |
| `classicdb.ch/?zone=9` | 返回空壳页 | 页面只有导航框架，NPC / 对象表靠 JS 拉取，抓不到数据 |
| `web.archive.org` | **Claude Code 拒绝抓取** | 时光机路线整条不可用 |
| `curl` 直连 `warcraft.wiki.gg?action=raw` | wiki.gg 的 **Blocked 拦截页** | 拿不到原始 wikitext。**warcraft.wiki.gg 只能走 WebFetch**，且 WebFetch 会过一道小模型摘要——逐字 wikitext 取不到，所以本片区的 `quote` 都是摘要里回传的整句引文，不是我亲手从 wikitext 里裁的 |
| `Category:Northshire_Valley` | **HTTP 404** | 该分类不存在 |
| `Category:Goldshire` | **HTTP 429** | 限流，未重试（分类页对本片区价值不大，地点页的 Subzones 节已覆盖） |

### 1.3 完整性自评

- **北郡山谷**：wiki 的正式子区域全表只有 4 项（修道院含三段 / 葡萄园 / 回音山矿洞 / 北郡河），
  一个没漏。任务书要的「每一栋房子」靠往下再挂两层地标补到 **30 个节点**。
- **闪金镇**：wiki 没有闪金镇的建筑清单，**24 个节点全部是从 NPC 页一间一间反推出来的**。
  确证的建筑只有三栋（旅店 / 铁匠铺 / 马厩）＋ 一个露天货车摊。
  **镇上其余民居我一栋都没能确证，故一栋都没写进树**——宁缺毋造。见 §4 未查。
- **水晶湖**：5 个节点。湖的**形状与东南半边完全没有文字源**，只锚住了西北岸。

---

## 2. 版本差异（4.0.3a 大地的裂变改了什么）

**本树是旧世树，以下每一条都已经被排除在 YAML 之外。** 逐条列出，因为它们是本片区的头号雷区
——艾尔文森林与北郡正是 4.0.3a 改得最狠的一块地。

| # | 4.0.3a 之后的状态（**不得入镜**） | 旧世应该是什么样 | 出处 |
|---|---|---|---|
| 1 | **北郡葡萄园在烧**，被黑石兽人点着 | 完好的农庄葡萄园，占据者是迪菲亚的爪牙（一伙人，不是兽人） | `Northshire_Valley`：「Northshire Vineyards is now burning」；「invaded by Blackrock orcs and Goblin Assassins during the Cataclysm」 |
| 2 | **回音山矿洞被一道门封死**，正常手段进不去 | 洞口敞开，可以一路走到尽头大厅 | `Echo_Ridge_Mine`：「A gate was added which closed off the mine」（Patch 4.0.3a）；「can't be accessed by normal means」 |
| 3 | **麦克布莱德元帅站在修道院外面** | **他在修道院里面**（主厅） | `Northshire_Valley`：「In vanilla World of Warcraft, Marshal McBride was inside the Abbey.」 |
| 4 | 谷里摆着**新的训练假人** | 旧世没有这批新假人 | `Northshire_Valley`：「new training dummies implemented」。⚠️ 旧世修道院内**是否原本就有假人**未确证，见 §4 |
| 5 | **闪金镇有飞行点**（狮鹫管理员巴特莱特） | **旧世闪金镇没有飞行点**，艾尔文森林的联盟飞行点只在暴风城 | `Goldshire`：「In Cataclysm, a flight path has been added to the town.」 |
| 6 | 闪金镇有**专业训练师**与**猎人训练师** | 旧世两者都没有 | 同上：「A Profession Trainer and a Hunter Trainer have also been added.」 |
| 7 | 水晶湖**南岸有一栋人类宅邸** | 旧世南岸没有这栋房子 | `Crystal_Lake`：南岸 homestead「added in patch 9.0.5」（是暗影国度，比 4.0.3a 还晚） |
| 8 | 北郡山谷**有自己的独立地图** | 旧世没有，玩家在谷里看到的就是艾尔文森林地图 | 见 §5 坐标帧 |
| 9 | 闪金镇北边房子里的**六个小孩**（Cameron / Jose / John / Aaron / Lisa / Dana）、
「Remy 两次」、旅店助理梅利卡、战斗宠物训练师马库斯·詹森 | 旧世均无。⚠️ 其中**部分 NPC 的加入版本我没拿到白纸黑字**，见 §4 | `Goldshire` NPC 表（wiki 写的是当前版本，未标版本） |

**给分镜的一句话结论**：任何一个带火、带焦黑、带「矿洞铁门」、带「狮鹫停在闪金镇」的画面，
都是大地的裂变之后的魔兽，**旧世观众一眼看出来**。第 1–5 集一个都不能出现。

---

## 3. 为什么 `look_zh` 只能是 `ai_draft`：文字源的天花板

我把本片区能找到的每一个地点页都读完了，**关于「长什么样」的文字总共只有这么多**：

- 北郡山谷：「被不可穿越的群山环绕，唯一缺口在南边，有厚石墙与设卫的入口」——**只有地形拓扑，没有颜色、材质、光线**。
- 北郡修道院：「由主厅、武器大厅、图书馆侧厅三段组成」「墓地在正门以东」「马厩在后面」「主厅通向钟塔」
  ——**只有房间清单与相对方位，没有一句描述石头、屋顶、窗户**。
- 狮王之傲旅店：wiki 在「Physical Appearance」一节下**明说自己没有文字描述**，只有三张图。
- 回音山矿洞：「一条路绕到深处、开出一个大房间」——**只有拓扑**。
- 水晶湖：**形状与尺寸整条没有描述**。

所以本片区的交付重心（任务书 ③「`look_zh` 必须写到能直接生成画面」）**在文字源上是不可能完成的**，
我按任务书 ④ 的指示走了：**写出可生成的一句话、如实标 `ai_draft`、并把该找哪些参考图列成清单（§6）**。

`look_zh` 的推导前提有两条，下游若要推翻请先推翻这两条：

1. **建筑族系**＝暴风城人类建筑的乡村变体。沿用 sk2 已有的锁定结论：
   屋顶是**深蓝灰色石板瓦**，负向词含「红瓦, 琉璃瓦, 茅草顶, 金属波纹板, 沥青瓦」
   （`w2_architecture.md` 的屋顶锁定行）。因此本片区所有民居我都写了「深蓝灰瓦顶」、
   **没有写茅草顶**。⚠️ 这条是从**主城**外推到**村镇**的，是本片区最大的单点风险，见 §4。
   同样沿用的还有旧城区那条「白灰泥墙 + 外露深褐木构架（half-timbering）」的描述。
2. **色调与光**＝艾尔文森林的金秋午后。全片区统一为
   「金黄栎树林 + 亮绿草坡 + 午后三四点的暖金斜光」，
   洞窟内部与地窖是唯二的例外（火把橙红 / 烛光加大面积纯黑）。

---

## 4. 存疑与未查

**必须由用户或下游用参考图/游戏内截图裁决的，按风险从高到低：**

1. **【高】闪金镇与北郡民居的屋顶到底是瓦还是木瓦/茅草。**
   我按 sk2 的暴风城结论统一写了「深蓝灰石板瓦」，但那是**主城**的锁定结论；
   乡村建筑完全可能是木瓦（shingle）甚至更粗糙的做法。**错了就是全片区所有房子一起错。**
2. **【高】狮王之傲旅店二楼到底有没有外挑木廊 / 阳台。**
   我在树里挂了 `inn_upper_gallery` 并标 `ai_draft`——**文字源零记载**。
   它是「俯拍门口决斗」的唯一现成机位，所以值得单独核；**如果没有，这个节点要删**。
3. **【中】图书馆侧厅到底在修道院北侧还是南侧。**
   wiki 的 `Hall_of_Arms_(Northshire)` 与 `Library_Wing_(Northshire)` **两页都说自己在主厅以南**，
   互相矛盾（其中一页显然是复制粘贴时没改）。我按 NPC 坐标判定：
   武器大厅的两位训练师在 Y≈42.0–42.2（南），图书馆的两位在 Y≈39.5–39.6（北），
   **故取「武器大厅在南、图书馆在北」**。但这是我的推断，不是 wiki 的原话。
4. **【中】旧世修道院里本来有没有训练假人。**
   4.0.3a 的改动写的是「new training dummies implemented」——`new` 这个词既可以读成
   「新加了假人」也可以读成「换了一批假人」。我在 `abbey_hall_of_arms` 的 `look_zh` 里写了稻草假人，
   **若要保险应删掉**。
5. **【中】水晶湖湖心小岛上的墓碑是不是旧世就有。**
   小岛与墓碑 wiki 都确认存在，但**没写加入版本**，而该页另一处的南岸宅邸明确是 9.0.5 加的
   ——说明这个湖被后期改过。建议只拍岛、不拍碑。
6. **【中】闪金镇除三栋确证建筑外还有几栋房子、分别是什么。**
   实机里镇上肯定不止三栋，但**文字源一栋都没写**，我一栋都没编进树。
   这是本片区**已知的最大缺口**——第 4–5 集要拍镇子全景必须补。
7. **【中】这几位 NPC 是不是旧世就有**（wiki 只列当前版本、不标版本）：
   酒保多宾斯、屠夫托德里克、鱼贩杰森·马瑟斯、面包师琪拉·松歌、护甲商安德鲁·克莱顿。
   我在树里只用了「他们站在哪」来定位房间，**没有把任何一位写成旧世居民**；
   若第 4–5 集要让他们上戏，得先单独核版本。
8. **【低】中文官方译名。** 灰机 wiki 全站 403，以下译名来自**搜索结果摘要**（＝`ai_draft` 级），
   不是我打开页面读到的：北郡山谷 / 闪金镇 / 狮王之傲旅店 / 北郡修道院 / 回音山矿洞 /
   北郡葡萄园 / 水晶湖 / 法戈第矿洞 / 明镜湖。
   其中两条要特别提醒：
   - **Northshire Valley 的官方译名是「北郡山谷」，不是「北郡谷地」**（灰机 wiki 的条目名就是北郡山谷）。
   - **Crystal Lake 的官方译名是「水晶湖」。任务书里写的「黄金鱼塘」不是官方译名**，
     疑似把玩家俗称或别的地名记串了；本树按官方走。
   房间级名称（主厅两侧耳房 / 二楼阅览室 / 铁匠铺后院 / 湖畔大宅 …）**本来就没有官方中文名**，
   它们在 YAML 的 `note_zh` 里都写了「非官方地名（描述性标签）」。
9. **【低】北郡山谷该算 `zone` 还是 `subzone`。** 我按 wiki 信息框有独立等级带（1-10）判为 `zone`，
   但旧世它在地图上是艾尔文森林的子区域。**合龙时若 G-艾尔文 那一路也把它写成 subzone，以这条为准做取舍。**

**没查（超出本片区、留给邻路）**：法戈第矿洞 / 玉石矿洞 / 马科伦农场 / 斯通菲尔德农场 /
明镜湖 / 布莱克威尔南瓜田 / 东谷伐木场 / 阿祖拉之塔 / 暴风城大门本体 / 石堆湖 —— 这些都是
艾尔文森林片区的节点，我只在路的 `note_zh` 里提到方向，**没有给它们建节点**。

---

## 5. 坐标帧（合龙时必读）

**本片区所有 `coords` 都是【艾尔文森林地图帧】。**

原因：旧世**没有独立的北郡地图**（北郡自己的地图是 4.0.3a 才加的），旧世玩家在谷里打开地图
看到的就是艾尔文森林。所以采用艾尔文帧 ＝ 采用旧世玩家的视角。

**坑在这里**：`warcraft.wiki.gg` 的北郡 NPC 信息框**同时给两套坐标**。
实测萨穆尔修士那一页写的是「[50.4, 42.0] for Elwynn Forest, or alternatively [41.2, 53.0] for Northshire」。
**两套数字差得很远，混用会把修道院内部的方位判反。** 本树一律取前者。
已知被这条坑到的两个数据点（**我没有采用，在此记录以免下游重蹈**）：
副官威廉的 `[35.6, 40.0]` 与米利·奥斯沃斯的 `[33.6, 55.0]`——这两个是北郡帧，不是艾尔文帧。

**换算**：坐标单位是地图百分比。艾尔文森林地图约 3470 × 2313 码，
故 **X 方向 1% ≈ 34.7 码 ≈ 31.7 m，Y 方向 1% ≈ 23.1 码 ≈ 21.1 m**。
X 增大 ＝ 向东，Y 增大 ＝ 向南。
（码→米沿用 sk2 的换算口径：1 码 ＝ 0.9144 m。）
用这把尺子可以读出：狮王之傲旅店到铁匠铺约 2.2% X ≈ 70 m，一条街的宽度；
旅店本身横跨约 1.3% X ≈ 41 m ——**WoW 的建筑比真实建筑大一号，不要按现实民宅的尺度建模。**

**标了 coords 但不是 wiki 直给、而是我推出来的节点**（合龙时降权处理）：
`northshire_abbey`（建筑中心）· `abbey_main_doors` · `abbey_main_hall` · `inn_upper_floor` ·
`inn_cellar` · `goldshire_forge` · `goldshire`（取镇中心 NPC 站位）。
其余带 coords 的节点都是某个 NPC 信息框的原始数字。

---

## 6. 必须靠参考图定的清单（下游按 sk2 #108 办法处理）

**仓库既有裁定：暴雪美术资产只进人眼、不入画、不上传给生成模型。**
所以下面每一项的正确做法是：**人去看图 → 写成中文锁定串 → 把串写进卡片/prompt → 图本身不进仓库、不喂模型。**

按优先级：

| 优先 | 要定的事 | 看什么 | 要产出的锁定串 |
|---|---|---|---|
| P0 | 北郡修道院外观 | 修道院正面、侧面、钟塔 | 墙体石材色与砌法 / 屋顶材质与颜色 / 窗形（尖拱？有无彩窗）/ 钟塔顶形 / 有无扶壁 / 旗帜图案与挂法 |
| P0 | 狮王之傲旅店外观 | 正面（含招牌）、侧面、屋顶 | 一层二层是否异材质 / 木构架走向 / **有没有二楼外廊** / 招牌造型与图案 / 烟囱位置 / 门廊形制 |
| P0 | 闪金镇整镇俯视 | 从北路进镇的视角 + 高处俯视 | **到底有几栋房子、分别在十字路口的哪一角** —— 这是 §4 第 6 条那个已知缺口 |
| P1 | 修道院内部三厅 | 主厅 / 武器大厅 / 图书馆一层二层 | 柱式与屋架 / 地面材质 / 采光位置 / 墙面挂什么 / **旧世有没有假人** |
| P1 | 旅店内部 | 一楼大厅、吧台、后厨、地窖、二楼三间房 | 壁炉位置与形制 / 吧台朝向 / 楼梯位置 / 地窖净高与拱顶 / 客房陈设 |
| P1 | 铁匠铺 | 正面与内部 | 是全敞、半敞还是封闭 / 锻炉形制 / 屋顶覆什么 |
| P1 | 北郡山谷全景 | 从谷口往北看 + 从修道院往南看 | 谷的实际开阔度 / 树种与密度 / 草色 / **太阳方位**（决定全片区打光方向） |
| P2 | 回音山矿洞 | 洞口 + 内部 | 洞口支护形制 / 坑道断面 / 尽头大厅有无天光 |
| P2 | 北郡葡萄园（旧世未烧版） | 葡萄架与农舍 | 藤架高度与行距 / 农舍形制 / 有无酒窖或压榨设备 |
| P2 | 水晶湖 | 俯视全貌 | **湖的实际形状与相对尺寸** / 岸线 / 小岛位置与大小 / 芦苇分布 |
| P2 | 谷口关卡 | 石墙与门洞 | 墙高与厚 / 有无塔楼 / 门是敞口还是有门扇 / 旗帜 |

**图在哪里找（只记 URL 与版权状态，按任务书要求不下载）：**

| 页面（图廊在页内） | URL | 版权 |
|---|---|---|
| Northshire Valley（含东/北/西/南四向全景图） | `https://warcraft.wiki.gg/wiki/Northshire_Valley` | © Blizzard Entertainment，游戏截图。**只进人眼** |
| Northshire Abbey（含主厅、武器大厅图） | `https://warcraft.wiki.gg/wiki/Northshire_Abbey` | 同上 |
| Hall of Arms (Northshire) | `https://warcraft.wiki.gg/wiki/Hall_of_Arms_(Northshire)` | 同上 |
| Library Wing (Northshire)（含 Lower / Upper floor room 两张） | `https://warcraft.wiki.gg/wiki/Library_Wing_(Northshire)` | 同上 |
| Main Hall (Northshire) | `https://warcraft.wiki.gg/wiki/Main_Hall_(Northshire)` | 同上 |
| Northshire River（含修道院旁瀑布图） | `https://warcraft.wiki.gg/wiki/Northshire_River` | 同上 |
| Northshire Vineyards（含「原始葡萄园」旧世图 + 燃烧后图，**注意区分**） | `https://warcraft.wiki.gg/wiki/Northshire_Vineyards` | 同上 |
| Echo Ridge Mine（含区域地图缩略图） | `https://warcraft.wiki.gg/wiki/Echo_Ridge_Mine` | 同上 |
| Goldshire | `https://warcraft.wiki.gg/wiki/Goldshire` | 同上 |
| Lion's Pride Inn（**三张不同时期的旅店图**，是 P0 的主力素材） | `https://warcraft.wiki.gg/wiki/Lion%27s_Pride_Inn` | 同上 |
| Crystal Lake | `https://warcraft.wiki.gg/wiki/Crystal_Lake` | 同上 |
| Fargodeep Mine / Jasperlode Mine（区域地图缩略图，可看南路走向） | `https://warcraft.wiki.gg/wiki/Fargodeep_Mine`｜`https://warcraft.wiki.gg/wiki/Jasperlode_Mine` | 同上 |

⚠️ **我没有取到任何一张图的直链**（WebFetch 回传的是摘要文本，不含图片 file URL）。
上表给的是**图所在的页面**，人去页面上看即可。
⚠️ **看图时必须先分辨版本**：`Northshire_Vineyards` 与 `Lion's_Pride_Inn` 两页都同时挂着
旧世与后期的图，拿错一张整套锁定串就全歪了。

---

## 7. 给下游的提醒

1. **两个主场之间只有一条路。** 北郡山谷是封闭谷地，出入口只有南端一个；闪金镇是四岔路口。
   所以第 3→4 集的转场**只可能是「出谷口 → 走东北路下坡 → 进闪金镇十字路口」**，
   没有第二条走法。这条约束很硬，但同时也是个礼物：转场序列是现成的。
2. **「铁匠铺正对旅店」是本片区最好的机位。** wiki 两次用 *opposite the Lion's Pride Inn* 定位铁匠铺
   ——两栋主建筑隔街对望，天然成立的正反打，而且两边色温完全相反
   （锻炉的橙红 vs 旅店窗口的暖黄 + 户外的金绿）。第 4–5 集的对话戏优先考虑这条轴线。
3. **旅店是本片区唯一的多层立体空间**：地窖 / 一楼 / 二楼 / 二楼各房间，垂直四层。
   全剧唯一能做「楼上楼下同时发生」「从地窖走到二楼」这类调度的地方。地窖尤其值钱
   ——**全镇最暗的空间**，是唯一不靠夜戏就能压暗的场景。
4. **狗头人不是主动攻击的。** wiki 明写旧世回音山的狗头人被打才还手。
   这直接决定第 1 集的动机写法：**是主角先动的手**（奉命清剿），
   不能写成「狗头人扑上来主角自卫」——那是在改设定，而且观众里的老玩家知道。
5. **修道院里躺着受伤的学员。** 这是 wiki 白纸黑字的（主厅两侧耳房、图书馆侧厅都有）。
   第 1 集不必额外编一个「这里很危险」的交代，走过去拍一眼就够了。
6. **闪金镇的杂货不在铺子里，是个路边货车摊。** 别按「进店买东西」写。
7. **旧世闪金镇没有飞行点。** 主角离开新手区**只能靠走**（或回暴风城坐狮鹫）。
   这条对第 5 集的收尾与整剧的「练级 → 换地区」节奏有实际影响，别顺手安排他在闪金镇起飞。
8. **旅店门口是决斗场。** wiki 明写这里以频繁决斗出名。
   这是把「这是个游戏世界」这件事拍出来的最便宜的一个镜头，建议第 4 集一定用。
9. **暴风城相关的一切直接复用 sk2，不要重查。**
   `ai_videos/shikong_lvxing/sk2/0_research/parts/w1_city_layout.md` 里有整城布局与 GM 世界坐标 14 锚点。
   本树的 `goldshire_north_road` 只负责把路指过去，城门以内的事归 sk2。
10. **合龙对账**：本片区唯一引用的外部 parent 是 `elwynn_forest`。
    另外三个 id 可能与别的片区**撞车**，合龙时请先对：
    `northshire_valley`（我建成 `zone`，别人可能建成 `subzone`）、
    `goldshire`、`crystal_lake`——尤其水晶湖，任务书把它划进了本片区，
    但它在地理上属于艾尔文森林的公共区域，G-艾尔文 那一路很可能也建了同名节点。
    我这一份是**建筑级**的（5 个节点，含码头与湖畔大宅），若对方那份只有 1 个节点，**以本份为准并合并**。
11. **类型约定（本片区自定，生成器合龙时若有全局约定请以全局为准）**：
    `settlement` 只给聚落（闪金镇 = town、狮王之傲旅店 = inn）；
    **聚落内部的单体建筑、房间、路、地标一律 `poi`**（因为 `subtype` 枚举里没有「房子」「房间」「路」）；
    `subzone` 只给会让游戏内小地图换名的正式子区域。

---

## 核验记录（G13-V）

独立核验员复核，日期 2026-09-20。默认立场：怀疑每一个地名。**所有判据都来自本次实际抓取的
`warcraft.wiki.gg` 页面**，不采用记忆。总体结论：**已修订可用**——原稿地名零编造、坐标零编造，
但有 3 处版本错置、3 处层级/类型挂错、4 处 `verified_by: ai_read` 却引文对不上页面，已全部就地修好。

### V-1 方法上的一个突破（下游务必复用）

原稿 §1.2 记「`curl` 直连 `?action=raw` 被 wiki.gg 拦截、WebFetch 只回摘要、逐字 wikitext 取不到」。
**这条结论只对了一半**：`curl` 确实被拦，但 **WebFetch 抓 `https://warcraft.wiki.gg/wiki/<Page>?action=raw`
是通的，且回传的就是原始 wikitext**——信息框每个字段、`{{coords|x|y|帧}}` 模板的第三参数、
`<gallery>` 的图注、Patch changes 的补丁号，全都能逐字读到。本次的三条硬发现
（等级字段是空的 / 北郡自有地图是 5.0.4 / 湖心墓碑是 10.1.5）**只有走 raw 才拿得到**。

唯一限制：WebFetch 的小模型有**单条引文 ≤125 字符**的硬限制，所以要拿长句得分段问，
或改问「某个短语是否出现在该页 → 是/否 + 120 字以内引一句」。原稿里那几条长引文经本次逐条复查
**确认都真实存在于页面上**（见 V-3），并非编造。

### V-2 完整性核验：三个 zone 的官方子区域一个不缺

以 `Elwynn_Forest?action=raw` 的 `Maps and subregions` 表为准（它是全艾尔文子区域的权威清单），
落在 G13 范围内的官方子区域共 **10 条**：

```
*[[Goldshire]]
**[[Lion's Pride Inn]]
*[[Crystal Lake]]
----
;[[Northshire Valley]]
*[[Echo Ridge Mine]]
*[[Northshire Abbey]]
**[[Hall of Arms (Northshire)|Hall of Arms]]
**[[Library Wing (Northshire)|Library Wing]]
**[[Main Hall (Northshire)|Main Hall]]
*[[Northshire Vineyards]]
----
;[[Undisplayed location]]s
*[[Northshire River]]            ← 落在 G13 内
```

**逐条对账结果：10 / 10 全部已在原稿树中，无一遗漏；树里也没有任何 wiki 上不存在的地名。
故补充子区域数为 0——这是核验结论，不是偷懒。**

`Northshire_Valley?action=raw` 自己的 `Maps and subregions` 节与上表完全一致（4 条 + 河），
`Goldshire` 名下只有狮王之傲旅店一条，`Crystal_Lake` 页无任何子区域。

顺带排除的三个「看着像漏了」的候选：

| 候选 | 判定 | 依据 |
|---|---|---|
| `Thieves Camp` | **不收**。WoW beta 阶段的 planned subzone，从未上线 | `Thieves_Camp` 页顶 `Removedfrombeta` 模板，艾尔文表里挂在 "Removed locations" 下 |
| `Nazferiti river` | **不收**。它是暮色森林与艾尔文的天然分界，在艾尔文最南，不在 G13 | 「flows west, bordering Duskwood and Elwynn Forest」 |
| `Darkmoon Faire Staging Area` | **不收进本文件**。它是 `elwynn_forest` 的直属 undisplayed 子区域、不是闪金镇的子区域；4.3.0 随暗月马戏团迁往暗月岛而废 | 艾尔文表 Undisplayed 节；`Darkmoon_Faire_Staging_Area` 页 |

> 留给 G-艾尔文 那一路：暗月马戏团集结地在旧世是真实存在的，且就在闪金镇近旁，
> 若第 4–5 集要用，它该建在 `elwynn_forest` 名下，不该挂进本文件。

### V-3 本次实际抓到并读过的页（全部 `warcraft.wiki.gg`）

**地点 / 物件页（17 个条目）**：`Elwynn_Forest`（含 raw）· `Northshire_Valley`（raw ×3）·
`Northshire_Abbey`（×2）· `Main_Hall_(Northshire)` raw · `Hall_of_Arms_(Northshire)` raw ·
`Library_Wing_(Northshire)` raw · `Northshire_River` raw · `Northshire_Vineyards` raw ·
`Echo_Ridge_Mine` raw ×2 · `Northshire_Guard` raw · `Goldshire`（×3，含 raw）·
`Lion's_Pride_Inn`（含 raw）· `Crystal_Lake` raw · `Deeply_missed,_never_forgotten` raw ·
`Thieves_Camp` raw · `Nazferiti_river` raw · `Darkmoon_Faire_Staging_Area` raw

**NPC 页（24 个，全部取 raw，为的是读 `coords` 模板的第三参数＝地图帧）**：
`Willem`（`Deputy_Willem` 是重定向）· `Marshal_McBride` · `Brother_Sammuel` · `Llane_Beshere` ·
`Priestess_Anetta` · `Khelden_Bremen` · `Drusilla_La_Salle` · `Jorik_Kerridan` · `Milly_Osworth` ·
`Garrick_Padfoot` · `Adele_Fielder` · `Helene_Peltskinner` · `Lee_Brown` · `Corina_Steele` ·
`Brother_Wilhelm` · `Erma` · `Tharynn_Bouden` · `Brog_Hamfist` · `Tomas` · `Maximillian_Crowe` ·
`Zaldimar_Wefhellt` · `Priestess_Josetta` · `Michelle_Belle` · `Keryn_Sylvius`

**坐标逐条对账：原稿所有取自 NPC 信息框的坐标，本次全部复核，无一错**——
萨穆尔 50.4/42.0、莱恩·贝希尔 50.2/42.2、安妮塔 49.8/39.6、凯尔顿 49.6/39.5、
德鲁希拉 49.9/42.7、尤里克 51/40、加里克 57.4/48.2、麦克布莱德 48.9/41.6、
艾尔玛 42.8/65.9、威廉修士 41.1/66.0、萨林 41.9/67.1、科琳娜 41.6/65.8、
布罗格 43.9/66.0、托马斯 44.3/66.0、克罗 44.4/66.2、扎尔迪马尔 43.3/66.2、
约瑟塔 43.3/65.7、米歇尔 43.4/65.6、凯琳 43.8/65.9、阿德勒 46.4/62.1、
海伦妮 46.3/62.2、李·布朗 47.5/62.3 —— 全部与 YAML 一致，且模板第三参数都是 `Elwynn Forest`。

原稿 §5 关于「两套坐标帧」的判断也**全部复核正确**：威廉的 35.6/40.0、米利的 33.6/55.0
确实是北郡帧，wiki 模板自己就标了 `Northshire`，原稿不采用是对的。
**补一条可机检的规则：照 coords 模板第三参数取即可，不必靠数值大小猜帧。**

### V-4 改了什么（12 条）

| # | 节点 | 问题 | 修法 |
|---|---|---|---|
| 1 | 文件头注释 | **版本错置**。「北郡自己的地图是 4.0.3a 才加的」错 | 改为 **5.0.4 熊猫人之谜**。`Northshire_Valley` 的 Patch changes 原文是「Northshire Valley receives its own world map」挂在 5.0.4 下。结论（旧世用艾尔文帧）不变 |
| 2 | `northshire_valley` | **等级带错误**。填了 `level: "1-10"`，但 `Infobox zone` 里 `level =` 是**空字段**，全页也无任何等级表述 | `level` 改空，note 写明原委。"1-10" 是大地的裂变后艾尔文整区的带宽，不是本谷的 |
| 3 | `crystal_lake_islet` | **版本错置（本次最重）**。原稿把湖心墓碑记为「加入版本没写明、存疑」 | 墓碑有独立条目 `Deeply missed, never forgotten`，Patch changes 只有一行「Patch 10.1.5｜Added.」——**巨龙时代 2023 年**才加的 Mats "Ibelin" Steen 纪念碑（连提灯与狐狸雕刻）。存疑消解为**硬排除**：`look_zh` 删掉「旧石碑」，note 写死「湖心岛必须是空岛」 |
| 4 | `echo_ridge_mine_entrance` | **版本错置**。引文「Gug Fatcandle can occasionally be found at the entrance」在页面上是写在 "Following the Cataclysm, the mine has been closed off, and…" 这一句里的 | 换成 4.0.3a 补丁条目「A gate was added which closed off the mine」——用「那次才加门封死」反证旧世洞口敞开，版本方向正确 |
| 5 | `lions_pride_inn` | **层级挂错**。`type: settlement / subtype: inn`。一栋旅店不是聚落 | 改 `type: subzone`。`Elwynn_Forest` 子区域表里它就是挂在 Goldshire 下的正式子区域，也正符合本树自订的「subzone = 会让小地图换名的正式子区域」 |
| 6 | `inn_main_room` `inn_back_room` `inn_cellar` `inn_upper_floor` | **层级挂错**。四间屋子标成 `subzone`，但它们都不是 wiki 子区域（艾尔文表里旅店之下再无一层） | 四个一律改 `poi`，与树里其余「房间」保持同一口径 |
| 7 | `crystal_lake_lakehouse` | **层级挂错**。挂在 `crystal_lake` 下 | 改挂 `goldshire`。阿德勒·菲尔德与海伦妮·佩尔特斯金纳两页信息框都写 `location = [[Goldshire]]`，海伦妮页明写「on the outskirts north-east of Goldshire」。对照：李·布朗的信息框 `location` 只写 `[[Elwynn Forest]]`，故码头仍挂水晶湖 |
| 8 | `vineyard_farmhouse` | **无出处 / `verified_by` 滥用**。标 `ai_read`，但所挂引文（葡萄园被迪菲亚占据）完全不能证明这里有一栋农舍 | 降级 `ai_draft`，清空 source/quote。复核过：`Northshire_Vineyards` 全页零建筑字样，`Milly_Osworth` 页也没有，只写她是葡萄园主人 |
| 9 | `goldshire_mailbox` | **无出处**。引文「Inn … Mailbox … Stables … Anvil & Forge … No Bank or Auctions」是把设施表复述成了一句页面上并不存在的话 | 换成信息框原始 wikitext。顺带记下：信息框**根本没有 bank / auction 键**，而其中的 `flightpath = yes` 是大地的裂变后才有的 |
| 10 | `goldshire_stable` | **无出处**。引文是信息框渲染出的坐标串，不是页面句子 | 换成 `Erma` 页正文句 |
| 11 | `crystal_lake_reed_shallows`、`crystal_lake_islet`、`northshire_abbey`、`abbey_stable`、`abbey_library_wing` | 引文是**转述**而非逐字（意思对，字不对） | 五条一律换成页面逐字原文 |
| 12 | `northshire_abbey_road` | **命名不一致**。id 说「修道院路」，`name_en` 写 `Northshire Valley Road` | id 改 `northshire_valley_road`。无任何 `adjacent` 引用它，改名安全 |

**顺带补进去的（补全侧）**：`crystal_lake` 原 coords 留空，现填 `[49.0, 65.7]`
——取自 `Deeply missed, never forgotten` 的 `Co|49|65.7|Elwynn Forest` 模板，该物件在湖心小岛上，
故可当湖心锚点；`crystal_lake_islet` 同步填上。**墓碑本身不能拍，但它的坐标是干净的地理数据。**
另把 `abbey_forecourt` 的坐标出处写实（麦克布莱德信息框 48.9/41.6），并记下威廉现坐标 48.8/38.4
是「修道院后方西北」的 4.0.3a 后站位、不可当前庭锚点。

### V-5 复核后确认「原稿是对的、一个字没动」

- 59 个节点**无 id 重复、无孤儿 parent、字段结构 59 条完全一致**（脚本校验通过）。
- 原稿那几条长引文**逐条命中页面**，包括最容易被怀疑的两条：
  `Northshire_Valley` 的「surrounded by impenetrable mountains, with the exception of a pass to the south
  which is protected by thick stone walls and a guarded entryway」（确在页上）、
  `Northshire_Guard` 的「A number of them can be found at the entrance to the valley, and more will
  arrive if Horde interlopers attack any members of the Alliance who dwell within the valley」（确在页上）。
- **副官威廉那条是原稿最漂亮的一处考据**：`Deputy_Willem` 是重定向到 `Willem`，而「He originally
  stood straight in front of the garrison」确实写在该页 History·World of Warcraft 节（＝大地的裂变之前）里
  ——原稿既找对了句子，也用对了版本。核验只把 `source_url` 从重定向改成了实际条目。
- **图书馆侧厅南北之争，原稿的裁决成立**：`Hall_of_Arms_(Northshire)` 与 `Library_Wing_(Northshire)`
  两页确实都写「It is situated south of the Main Hall」——是复制粘贴漏改，wiki 自身矛盾。
  原稿按 NPC 纵坐标判「武器大厅在南（Y≈42.0–42.2）、图书馆在北（Y≈39.5–39.6）」，坐标本次已复核无误，
  判法成立。**保留原判，并保留它「这是推断不是原话」的声明。**
- 原稿 §2 的版本差异表其余各条（葡萄园在烧 / 矿洞加门 / 麦克布莱德移到室外 / 闪金镇飞行点 /
  水晶湖南岸宅邸 9.0.5）**逐条复核全部属实**。`Goldshire` 信息框里 `flightpath = yes` 确实在，
  正是原稿要排除的那条。

### V-6 对本 notes 自身两处表述的更正

1. **§3 说「狮王之傲旅店 wiki 在『Physical Appearance』一节下明说自己没有文字描述，只有三张图」
   ——查无此节。** 实情更糟：`Lion's_Pride_Inn` 全页只有 NPCs / Players' activity / Film universe /
   References / External links 五节，**连一节建筑描述都没有**。§3 的整体结论（文字源给不出长相）不变，
   但这条具体说法要改掉，免得下游去找一节不存在的内容。
2. **§1.2 说 `?action=raw` 取不到** —— 见 V-1，`curl` 取不到，**WebFetch 取得到**。

### V-7 仍存疑（核验后未能消解的）

1. **【高】`inn_upper_gallery`（旅店二楼外挑木廊）零文字源，既不能证实也不能证伪。**
   旅店页全页无建筑描述，唯一与高处有关的一句是「Players sometimes can be found climbing up to the
   top of the roof and lighting a campfire for fun.」——说的是屋顶、不是外廊。**保留但挂了硬警告**：
   出图前先看参考图，没有就删，俯拍广场改用屋顶或对街铁匠铺机位。
2. **【高】屋顶材质（深蓝灰石板瓦）仍是从 sk2 的暴风城主城结论外推到乡村的**，本次核验无法触及
   （文字源里根本没有材质）。原稿 §4.1 的风险评级维持不变。
3. **【中】中文官方译名整块仍未能核。** `wow.huijiwiki.com` 与 `warcraft.huijiwiki.com` 本次重试
   **仍是 HTTP 403**，与原稿结论一致；且本 session 的 WebSearch 配额已用尽（200/200），
   连搜索摘要这条退路也断了。**故本次一个中文名都没动**——它们维持原稿 §4.8 的 `ai_draft` 级别。
   逐一目视过一遍，没有发现「自己音译」的痕迹：北郡山谷 / 闪金镇 / 狮王之傲旅店 / 北郡修道院 /
   回音山矿洞 / 北郡葡萄园 / 水晶湖 / 主厅 / 武器大厅 / 图书馆侧厅，以及全部 NPC 名，
   都是国服长期沿用的通行译法。**但「没发现问题」≠「已核实」，下游仍应在灰机 wiki 可达时补核一遍。**
4. **【中】北郡山谷的等级带现在是空的。** 见 V-4 第 2 条：wiki 信息框不给，就不要编。
   若第 1–5 集需要一个数字，请另找出处（任务等级表 / 怪物等级），不要沿用被删掉的 "1-10"。
5. **【中】闪金镇实际有几栋房子**——原稿 §4.6 的缺口本次**未能补上**。
   `Goldshire` 页的 NPC 节只分 Vendors / Trainers / Guards 三档，**不按建筑分组**，
   全页也没有任何建筑清单。确证的建筑仍是三栋（旅店 / 铁匠铺 / 马厩）＋ 一个露天货车摊 ＋
   镇东北外围那栋湖畔大宅。**这仍是本片区最大的已知缺口，只能靠参考图（§6 的 P0 第三项）补。**
6. **【中】北郡山谷该算 `zone` 还是 `subzone`。** 维持原稿判法（它有自己的 `Infobox zone`），
   但补一条新证据供合龙时取舍：在 `Elwynn_Forest` 的子区域表里，北郡山谷是被单独拉出来当
   **小标题**（`;[[Northshire Valley]]`）领着 4 条子区域的，不是平级的一个 `*` 条目
   ——这支持把它当 zone 处理。
7. **【低】原稿 §4.7 那几位 NPC 的版本归属**（多宾斯 / 托德里克 / 杰森·马瑟斯 / 琪拉·松歌 /
   安德鲁·克莱顿）本次未逐个核。树里仍只用他们「站在哪」来定位房间，没有把任何一位写成旧世居民，
   这个处理是安全的；要让他们上戏才需要单独核版本。
