# G06 · 洛丹伦北部 + 幽暗城 —— 测绘备注

> 本文件**只放不属于树的东西**。树数据（节点、层级、译名、坐标、邻接）唯一出处是
> `g06_lordaeron_north.yaml`，此处不重复抄写节点清单。
> 版本锚点：**经典旧世 Vanilla / Classic Era（1.12 / 1.15.x 客户端数据）**。

---

## ① 自查对账

### 1.1 最终形态

| 片区 | 节点数 | 说明 |
|---|---|---|
| `tirisfal_glades` 提瑞斯法林地 | 37 | 不含幽暗城子树 |
| `undercity` 幽暗城 | 11 | 挂在 `ruins_of_lordaeron` 之下（物理真实关系） |
| `silverpine_forest` 银松森林 | 28 | |
| `hillsbrad_foothills` 希尔斯布莱德丘陵 | 25 | |
| `alterac_mountains` 奥特兰克山脉 | 23 | 不含奥山谷战场子树 |
| `alterac_valley` 奥特兰克山谷（战场） | 28 | 含入口区 + 战场内 26 个子区域 |
| **合计** | **152** | 全部 `era: vanilla` |

核验强度：`verified_by: ai_read` 137 个 / `ai_draft` 15 个。带地图坐标 65 个。

### 1.2 关键方法（下游要复现就看这里）

**本片区没有靠记忆写任何一个中文地名与坐标**，全部来自可重下载的客户端数据表：

1. **`name_zh` 与层级** —— Classic Era 客户端 `AreaTable`（国服官方简体译名 + `ParentAreaID`）：
   `https://wago.tools/db2/AreaTable/csv?build=1.15.9.69722&locale=zhCN`
   （英文名同表 `locale=enUS`。build 号取自 `https://wago.tools/api/builds` 里 `wow_classic_era` 的最新条目。）
   这一步直接纠正了两处**我原本会写错的译名**：
   - The Sepulcher = **瑟伯切尔**（不是「圣殿」）
   - Pyrewood Village = **焚木村**、The Skittering Dark = **粘丝洞**、Beren's Peril = **博伦的巢穴**、
     Azurelode Mine = **碧玉矿洞**、Cold Hearth Manor = **炉灰庄园**、Purgation Isle = **赎罪岛**、
     Nethander Stead = **奈杉德哨岗**、Dandred's Fold = **达伦德农场**、Terrace of Repose = **休息区**。
2. **`coords`** —— 客户端 `WorldMapOverlay`（每个子区域在分区地图上的高亮贴图矩形）：
   `https://wago.tools/db2/WorldMapOverlay/csv?build=1.15.9.69722&locale=enUS`
   取 `(OffsetX + TextureWidth/2) / 1002 * 100`、`(OffsetY + TextureHeight/2) / 668 * 100`
   （vanilla 分区地图逻辑尺寸 1002×668），即**高亮块中心点**的百分比坐标。
   因此这些坐标是「该子区域的中心」，不是「某个 NPC/门口的精确点」，用于选景足够，用于插旗要再核。
3. **飞行点名称** —— 客户端 `TaxiNodes`（`locale=zhCN`），因此「幽暗城，提瑞斯法林地」这类
   带逗号的官方写法是原样照抄。
4. **散文/剧情/外观** —— `warcraft.wiki.gg` 各条目页，用 `?action=raw` 取原始 wikitext
   （比渲染页更完整，`Maps and subregions` 一节的嵌套列表一条不漏）。

### 1.3 抓取清单

**成功（`?action=raw`，warcraft.wiki.gg）**：
`Tirisfal_Glades` · `Silverpine_Forest` · `Hillsbrad_Foothills` · `Alterac_Mountains` · `Undercity` ·
`Brill` · `Deathknell` · `Bulwark` · `Ruins_of_Lordaeron` · `Scarlet_Monastery` · `Shadowfang_Keep` ·
`Sepulcher` · `Greymane_Wall` · `Tarren_Mill` · `Southshore` · `Durnholde_Keep` · `Purgation_Isle` ·
`Ruins_of_Alterac` · `Strahnbrad` · `Ravenholdt_Manor` · `Dalaran_Crater` · `Alterac_Valley`（22 页）

**成功（数据表，wago.tools）**：`AreaTable`(zhCN/enUS) · `WorldMapOverlay` · `TaxiNodes`(zhCN) · `AreaPOI`(zhCN) · `api/builds`

**抓不到（403 / 重定向循环）**：
- `wow.huijiwiki.com`、`warcraft.huijiwiki.com`（灰机 wiki）—— 全站 403，WebFetch 被挡。
  **中文译名改由客户端 `AreaTable` zhCN 提供，质量更高**（灰机本身也是照抄客户端）。
- `baike.baidu.com` —— 403。
- `www.wowhead.com/classic/cn/zone=85`、`...&xml` —— 重定向循环（该站对无 JS 客户端不友好）。
- `curl` 直连 `warcraft.wiki.gg` —— Cloudflare 拦截（「Blocked - wiki.gg」），只能走 WebFetch。
- `db.nfuwow.com/60/?zone=85` —— 可访问，但只给分区名与等级，无子区域列表（已用于交叉验证
  「提瑞斯法林地 1-10 级 / 部落」）。

**本次会话 WebSearch 配额已用尽（200/200）**，最后几个存疑项无法再用搜索兜底，已如实记在 ③。

---

## ② 版本差异（4.0.3 大地的裂变及之后改了什么）

本树**一律取 vanilla 状态**；下列改动只在这里记录，不进树。

### 2.1 结构级改动（最容易踩的雷）

1. **奥特兰克山脉整个 zone 被取消**。4.0.3 后 `alterac_mountains` 不再是独立地区，整体并入
   **希尔斯布莱德丘陵**，共用一张地图。因此现今 wiki 在 `Hillsbrad Foothills` 页把奥特兰克的
   子区域列在一个二级标题下 —— 看 wiki 时极易把它们错归到希尔斯布莱德。**vanilla 它们是两个 zone、两张地图。**
2. **南海镇被摧毁**。4.0.3 被遗忘者瘟疫攻击后，`Southshore` → `Ruins of Southshore`（南海镇废墟），
   联盟据点后撤。**vanilla 最著名的野外 PK 对峙（南海镇 vs 塔伦米尔）从此不复存在**——
   这是本片区剧情价值最高的一处，也是最不能用现今资料描述的一处。
3. **格雷迈恩之墙被震开**，吉尔尼斯开放为可进入地区（`Ruins of Gilneas`）。vanilla 墙门永久关闭、
   墙后不可进入，且**银松南边没有「吉尔尼斯废墟」这个邻居**。本树 `silverpine_forest.adjacent`
   因此只有提瑞斯法与希尔斯布莱德。
4. **达拉然**：vanilla 是奥特兰克山脉西侧湖边的**紫色魔法穹顶**（罩着废墟，不可进入）；
   WotLK 城市被抬往诺森德，原址成「达拉然巨坑（Dalaran Crater）」。
   本树节点 id 写作 `dalaran_alterac`，`name_zh` 取 vanilla 的「达拉然」。
5. **血色修道院**：vanilla 是一座副本建筑内含**四翼**（墓地/图书馆/军械库/大教堂）；
   MoP(5.0) 重做成「血色大厅 + 血色修道院」两个副本，房间与 Boss 全换。本树取 vanilla 四翼。
6. **幽暗城**：BfA「洛丹伦之战」后全城被瘟疫化、布瑞尔被毁。本树取 vanilla 完好状态。

### 2.2 子区域改名/新增对照（左＝vanilla 本树用名，右＝Cata 之后）

| vanilla（本树） | 4.0.3 之后 | 所在 zone |
|---|---|---|
| 玛尔丁果园 Malden's Orchard | 被遗忘者高级指挥部 Forsaken High Command | 银松森林 |
| 亡者农场 The Dead Field | 被遗忘者后卫营 Forsaken Rear Guard | 银松森林 |
| 破旧渡口 The Decrepit Ferry | 破旧农场 Decrepit Fields | 银松森林 |
| 希尔斯布莱德农场 Hillsbrad Fields | 污泥之地 The Sludge Fields | 希尔斯布莱德 |
| 南点哨塔 Southpoint Tower | 南点大门 Southpoint Gate | 希尔斯布莱德 |
| 南海镇 Southshore | 南海镇废墟 Ruins of Southshore | 希尔斯布莱德 |
| 洛丹米尔收容所 Lordamere Internment Camp | 布雷泽农场 Brazie Farmstead | 奥特兰克山脉 |
| 达拉然 Dalaran | 达拉然巨坑 Dalaran Crater | 奥特兰克山脉 |

**4.0.3 之后才出现、本树不收的地点**（看现今 wiki 时要主动剔除）：
`Calston Estate` 卡斯顿庄园 · `Death's Watch Waystation` · `Rotbrain Encampment` · `Whispering Forest`
（及其 `Tyr's Fall` / `Tomb of Tyr` / `Darkwalk` 等，均为后续版本内容）· `Scarlet Palisade` ·
`Scarlet Watchtower` · `The Battlefront` 与 `7th Legion Base Camp` / `Gilneas Liberation Front Base Camp` ·
`North Tide's Beachhead` · `Eastpoint Tower` · `Sludgeguard Tower` · `Galen's Fall`。
判据：以上名称**均不在 Classic Era 客户端 `AreaTable` 里**（我逐个查过），而本树收录的每一个
带 `area id` 的节点都在表里。

### 2.3 飞行点差异（vanilla 只有这些）

- 提瑞斯法：**只有幽暗城**一个飞行点。（亡灵壁垒 The Bulwark 的飞行点是 **3.3.0 巫妖王之怒**才加的——原文写 4.0.3，核验时改正；4.0.3 只是重修了工事。无论如何 vanilla 不收。）
- 银松：**只有瑟伯切尔**。
- 希尔斯布莱德：**塔伦米尔（部落）+ 南海镇（联盟）**。（斯坦恩布莱德、东点哨塔飞行点都是 Cata 才有。）
- 飞艇：洛丹伦废墟外西侧两座塔，vanilla 两条航线 —— 奥格瑞玛、格罗姆高。（复仇岗是 WotLK。）

---

## ③ 存疑与未查

1. **幽暗城城内分区（贸易区/魔法区/盗贼区/炼金房/军事区/皇家区/运河/下水道）没有客户端区域条目**——
   vanilla 在城里走动时区域名始终是「幽暗城」，分区名只印在地图贴图上。因此这 8 个节点的
   `name_zh` 取自中文社区通用名（与国服地图贴图一致），`verified_by: ai_draft`。
   **若下游要在画面里出现分区名牌，建议再找一张国服幽暗城地图截图人眼确认。**
   其中 `The Apothecarium` 中文社区多写「**炼金房**」（也有写「炼金区」的），本树取前者。
2. **血色修道院四翼中文名**（墓地/图书馆/军械库/大教堂）同理为社区通用名，`ai_draft`。
3. **奥特兰克山谷战场入口的精确坐标未取到**。wiki 只给了 Cata 之后的描述（「南海镇正北 / 塔伦米尔东北」）。
   vanilla 入口区域在客户端里是 `Alterac Valley`(area 2839，父级＝奥特兰克山脉) 与
   `The Foothill Caverns`(area 277)，两者**都没有地图高亮块**，所以 `coords` 留空。
4. **奥山谷等级段**：本树写 `51-60`（vanilla 后期固定分段）。wiki 记载 1.5.0 开放时「45 级可排」，
   两者不矛盾但需下游注意：若剧要还原 1.12，用 51-60。
5. **拉文霍德庄园坐标留空**：它与冰风岗共用同一块地图高亮，中心点不代表庄园本身。
   wiki 给的 `77, 19` 是**现今希尔斯布莱德合并地图**上的坐标，不能直接用于 vanilla 奥特兰克地图。
6. **血色修道院入口坐标**：本树取 `[85, 32]`（vanilla 分区地图上的通用值，与耳语花园高亮块中心 `[85,33]` 一致）。
   现今 wiki 写的 `83.9, 23.4` 是**正式服合并后地图**的值，勿混用。
7. **`Bucklebree Farm` 巴克布雷农场**：在 Classic Era `AreaTable` 里（ID 926，国服名「巴克布雷农场」），
   但没有地图高亮块，wiki 将其列入「Removed locations」。**确实位置存疑**，已如实记在节点 `note_zh`。
8. **`南海镇渡口` 飞行节点**（TaxiNodes ID 46）在客户端里存在，但 vanilla 未开放固定航线。
   本树把它记为 `southshore_docks`（poi），**没有**建成 `transport/boat` 节点。
9. **`North Tide's Run` / `South Tide's Run` / `Thoradin's Wall` / `Faol's Rest` / `The North Coast` /
   `Whispering Shore` 等无坐标**：这些区域在客户端里没有独立高亮块（多为海岸线/长条地形）。
10. **奥山谷内部 26 个子区域**取自 Classic Era（1.15.9）客户端数据。1.13 重建 AV 时沿用 1.12 数据，
    但个别「墓地 / 小径」条目是否在 1.12.1 原版就存在，未逐条对 1.12 客户端核过。
11. **`lordaeron` 这个 parent 我没有定义**（见 ⑤）。
12. 未做：每个 zone 的**任务链**与 NPC 清单（不属于地理树范围）。

---

## ④ 本片区地图图片链接清单（只记 URL 与版权状态，未下载）

> 仓库既有裁定：**暴雪美术资产只进人眼、不入画、不上传给生成模型。**
> 下列全部为暴雪版权素材，**仅供人工比对地形**，不得进入任何 prompt / 参考图槽位 / 训练与生成流程。

| 用途 | 页面 URL | 版权状态 |
|---|---|---|
| 提瑞斯法林地 分区地图（Cata 版，构图与 vanilla 基本一致） | https://warcraft.wiki.gg/wiki/File:VZ-Tirisfal_Glades.jpg | 暴雪版权 · 仅人眼 |
| 提瑞斯法林地 分区地图（BfA 版） | https://warcraft.wiki.gg/wiki/File:VZ-Tirisfal_Glades-t1.jpg | 暴雪版权 · 仅人眼 |
| **银松森林 分区地图（Cata 之前＝vanilla）** | https://warcraft.wiki.gg/wiki/File:WorldMap-Silverpine-old.jpg | 暴雪版权 · 仅人眼 |
| 银松森林 分区地图（Cata 版） | https://warcraft.wiki.gg/wiki/File:VZ-Silverpine_Forest.jpg | 暴雪版权 · 仅人眼 |
| **希尔斯布莱德丘陵 分区地图（Cata 之前＝vanilla）** | https://warcraft.wiki.gg/wiki/File:WorldMap-Hillsbrad.jpg | 暴雪版权 · 仅人眼 |
| 希尔斯布莱德丘陵 分区地图（Cata 版，已并入奥特兰克） | https://warcraft.wiki.gg/wiki/File:WorldMap-HillsbradFoothills.jpg | 暴雪版权 · 仅人眼 |
| **奥特兰克山脉 分区地图（Cata 之前＝vanilla，独立地区）** | https://warcraft.wiki.gg/wiki/File:WorldMap-Alterac-old.jpg | 暴雪版权 · 仅人眼 |
| 幽暗城 城市地图 | https://warcraft.wiki.gg/wiki/File:WorldMap-Undercity.jpg | 暴雪版权 · 仅人眼 |
| 提瑞斯法林地 原画 | https://warcraft.wiki.gg/wiki/File:Tirisfal_Glades_concept.jpg | 暴雪版权 · 仅人眼 |
| 瑟伯切尔 实景（Cata） | https://warcraft.wiki.gg/wiki/File:The_Sepulcher_(Cataclysm).jpg | 暴雪版权 · 仅人眼 |
| 南海镇废墟 实景（Cata，反面参考） | https://warcraft.wiki.gg/wiki/File:Ruins_of_Southshore.jpg | 暴雪版权 · 仅人眼 |

**带 `-old` / `WorldMap-Hillsbrad` / `WorldMap-Alterac-old` 的三张是 vanilla 原版地图**，
人眼比对时优先用它们；其余是改版后的，只能当参考。

---

## ⑤ 给下游的提醒

1. **`lordaeron` 这个 parent 不属于我**。本片区 4 个 zone 的 `parent` 一律写 `lordaeron`
   （洛丹伦，大陆内的 lore 分区），但**我没有定义这个节点**，以免与别的片区重复定义。
   合龙时请确认有人定义了：`azeroth`(world) → `eastern_kingdoms`(continent) → `lordaeron`(region)。
   若最终决定不设 `lordaeron` 这一层，把这 4 个 zone 的 parent 批量改成 `eastern_kingdoms` 即可。
2. **跨片区 `adjacent` 引用**：`western_plaguelands`、`arathi_highlands`、`the_hinterlands`
   属于别的片区，合龙时对账。注意 vanilla 里**银松森林南边没有可进入的邻居**（格雷迈恩之墙封死）。
3. **幽暗城挂在洛丹伦废墟之下**（`undercity.parent = ruins_of_lordaeron`），不是直接挂 zone。
   这是物理真实关系，也是这座城最值得拍的一点：**地表是人类王国的焦黑废墟，地下是亡灵的环形都城，
   中间只靠王座厅后的三部升降梯连接。**
4. **选景优先级（剧情价值从高到低）**：
   洛丹伦王座厅（弑父）> 幽暗城皇家区/炼金房 > 南海镇 ↔ 塔伦米尔（vanilla 野外 PK 圣地）>
   血色修道院大教堂 > 影牙城堡（阿鲁高与狼人）> 敦霍尔德角斗场（萨尔）> 达拉然紫色穹顶 >
   丧钟镇（亡灵出生：从棺材里爬出来）。
5. **同名消歧已按规则加限定**：`lordamere_lake_silverpine` / `lordamere_lake_alterac`
   （客户端确实为同一片湖在两个 zone 各建了一条记录，ID 1338 / 1339），
   `dalaran_alterac`（与达拉然主城区分）。
6. **`The Great Sea` 无尽之海我没有建节点**（提瑞斯法/银松/希尔斯布莱德三区各有一条客户端记录）。
   它必然跨片区重复，建议由合龙者统一在大陆层建一个，各 zone 不再挂。
7. 生成器脚本是一次性的（在 scratchpad 里，用完即弃），**YAML 就是唯一出处**；
   要改译名或坐标，改 YAML，不要回头找脚本。

---

## 核验记录（G06-V）

> 独立核验员复核，默认立场「怀疑每一个地名」。核验日期 2026-09-20。
> 结论：**已修订可用**。原稿 152 节点 → **166 节点**；`ai_read` 136 / `ai_draft` 30。
> 无 id 重复；除作者声明不属于本片区的 `lordaeron` 外无悬空 parent；字段顺序与格式未改。

### V.1 核了哪些 zone，用什么核的

六个片区全核：`tirisfal_glades` · `undercity` · `silverpine_forest` · `hillsbrad_foothills` ·
`alterac_mountains` · `alterac_valley`。

**子区域完整性我没有靠 wiki 的散文列表判定，而是直接拉客户端区域表做集合比对**——
`AreaTable`（Classic Era build 1.15.9.69722，enUS + zhCN），按 `ParentAreaID` 递归展开六个 zone 的全部后代，
与 YAML 逐个对集合。结果：

| zone | AreaTable 子区域数 | 树中缺 | 树中多（表里没有） |
|---|---|---|---|
| 提瑞斯法林地 85 | 27 | 0（仅 The Great Sea 按作者说明留给大陆层） | 0 |
| 银松森林 130 | 23 | 0（同上） | 0 |
| 希尔斯布莱德丘陵 267 | 15 | 0（同上；`UNUSED Alterac Valley` 不收正确） | 0 |
| 奥特兰克山脉 36 | 20 | 0 | 0 |
| 奥特兰克山谷 2597 | 26 | 0 | 0 |
| 幽暗城 1497 | 0（客户端无城内分区条目） | — | — |

**即：分区级（subzone）完整性原稿已经是满分，一个不多一个不少。** 这比对着 wiki 页面数列表可靠得多，
因为现今 wiki 的 `Maps and subregions` 一节把 4.0.3 之后的新地名与 vanilla 地名混在一张表里。
我另行逐个确认了作者 ② 节列出的「不收」名单（`Calston Estate` / `Whispering Forest` / `The Battlefront` /
`Eastpoint Tower` / `Sludge Fields` / `Rotbrain Encampment` / `The Deathknell Graves` / `North Tide's Beachhead` 等）
确实都不在 Classic Era `AreaTable` 里，**一个 Cata 地名都没有漏进树**。**未发现任何编造的地名。**

### V.2 补进去的 14 个节点（都是「建筑级 POI」，不是分区）

分区级没有缺口，缺口在作者自己已经开过的那一层——他给布瑞尔、南海镇、塔伦米尔、敦霍尔德都建了
建筑级 POI，但另外几处同级的建筑没建。按同一粒度补齐：

| 新增 id | parent | 依据 |
|---|---|---|
| `brill_blacksmith` | `brill` | wiki `Brill` 把 vanilla 三建筑并列为 Removed：Town Hall / Gallows' End Tavern / **Blacksmith**，树里只有前两座 |
| `pyrewood_town_hall` · `pyrewood_chapel` · `pyrewood_blacksmith` | `pyrewood_village` | wiki `Pyrewood Village`：「a town hall, a blacksmith, and a chapel」，且 4.0.3 才换成吉尔尼斯建筑，故均属 vanilla。**焚木议会入夜变狼人就发生在议事厅**，选景价值高 |
| `tarren_mill_inn` | `tarren_mill` | wiki `Tarren Mill` 建筑清单含 Inn；部落炉石点，是 vanilla 野外 PK 的部落集结点 |
| `alterac_church` · `alterac_town_hall` | `ruins_of_alterac` | wiki `Ruins of Alterac` 原文把五样并列：palace / **ruined church** / **dilapidated town hall** / gate / two graveyards。树里只收了三样 |
| `dun_baldar_north_bunker` · `dun_baldar_south_bunker` · `stormpike_aid_station` | `dun_baldar` | 奥山联盟侧可占领目标 |
| `iceblood_tower` | `iceblood_garrison` | 部落塔本体（原树只有作为区域的冰血要塞） |
| `east_frostwolf_tower` · `west_frostwolf_tower` · `frostwolf_relief_hut` | `frostwolf_keep` | 奥山部落侧可占领目标 |

**奥山这 7 个是原稿最实质的缺口**：AV 的可占领目标是 4 碉堡（联盟）+ 4 塔（部落）+ 双方各一个指挥官驻地，
它们是 GameObject 不是 AreaTable 区域，所以「按客户端区域表补全」的方法系统性地漏掉了整整一类。
证据来自作者自己——`tower_point.note_zh` 写着「部落四塔之一」，而原树里部落只有两座塔。现已配平。
命名以 wiki 为准：是 **East/West Frostwolf Tower**，不是 Frostwolf East/West Tower。

这 14 个一律 `verified_by: ai_draft`，`note_zh` 明写「国服官方译名未经客户端核实，以 name_en 为准」——
因为它们不在 `AreaTable` 里，拿不到国服官方简体名（见 V.5）。

### V.3 改掉的 12 处（`verified_by` 滥用 / 版本污染）

逐条把 `verified_by: ai_read` 的 quote 拿回原页面做子串比对。**11 个节点的 quote 根本不在它 cite 的那一页上**，
是作者自己总结的话套了引号——这正是「只凭印象写、事后补个 URL」的特征，必须掐掉：

| node_id | 原 quote（页面上没有） | 改成（页面原文） |
|---|---|---|
| `lordaeron_throne_room` | "The Throne Room: Where Arthas murdered his father…" | "To this day, one can hear the moments before King Terenas' death" |
| `deathknell_chapel` | "A church (Forsaken stronghold)" | "the church of Deathknell is one of the main bases of the Forsaken Cult of Forgotten Shadows" |
| `undercity_zeppelin_towers` | 带分号的自造清单 | "Zeppelin towers south of Brill" |
| `southshore_town_hall` | "Town Hall where Marshal Redpath stood" | "An NPC quest giver named Marshal Redpath stood outside the Southshore Town Hall." |
| `southshore_inn` | "Inn with Lieutenant Farren Orinelle" | "Inside the inn, Lieutenant Farren Orinelle mocked Redpath" |
| `southshore_docks` | "Docks where Nat Pagle fished" | "Nat Pagle idly fished off the dock." |
| `alterac_palace` | "The ruined city includes a relatively intact palace" | "The palace, which remains relatively intact." |
| `alterac_gate` | "a substantial gate" | "A mighty gate, not unlike the one at Stormwind City."（原文是 mighty，不是 substantial） |
| `alterac_graveyards` | "two graveyards" | "Two graveyards, one inside the city's limits and the other just outside, near Slaughter Hollow." |
| `the_greymane_wall` | "The Greymane Wall is a colossal defensive structure separating…" | "The Greymane Wall was erected before the Third War by order of King Genn Greymane…" |
| `sm_grand_vestibule` | "Grand Vestibule location: 48.3, 56.3"（页面上是 `{{co}}` 模板，没有这句话） | 换成修道院条目原文，并**降级 `ai_read` → `ai_draft`**（大前厅不在 `AreaTable` 里，中文名也是社区名） |

第 12 处是**版本污染**：`sfk_courtyard` 的 quote 写作 "Courtyard (Baron Ashbury)"，
而**阿什伯里男爵是 4.0.3 才加进影牙城堡的 boss**，拿他给一棵 vanilla 树做证据是错的。已改为 "Courtyard"。

另有一处 notes 自身的版本错误已就地改正：③ 原写「亡灵壁垒的飞行点是 4.0.3 才加的」，
实际是 **3.3.0（巫妖王之怒）**——wiki 补丁记录写得很清楚。结论（vanilla 不收）不变。

### V.4 核过、确认作者是对的，一个字没动

- **`scarlet_monastery.parent = whispering_gardens`** ——我本来怀疑挂错（AreaTable 里耳语花园与休息区都是
  提瑞斯法的直接子区域）。查 wiki 修道院条目信息框，location 字段正是「Whispering Gardens, Tirisfal Glades」。**作者对。**
- **血色修道院入口坐标 `[85, 32]`** ——现今 wiki 写 `83.9, 23.4`。作者在 ③.6 判定那是 Cata 合并地图的值、
  不能用于 vanilla。**判断正确，勿改。**
- **影牙城堡拆成 `shadowfang_keep_grounds`(室外) + `shadowfang_keep`(副本)** ——客户端里确实是两条记录：
  area 236（parent=银松森林）与 area 209（parent=0，副本图）。**建模精确，不是重名错误。**
- **`shadowfang_keep` 等级带 `16-26`** ——wiki 补丁 7.3.5 记录原文「previous instance level: 16 - 26」，**完全吻合**。
- **`ravenholdt_manor` 挂在奥特兰克山脉** ——AreaTable 3486 的 parent 就是 36（奥特兰克）；
  wiki 给的 `77, 19` 是希尔斯布莱德坐标（Cata 合并后），作者留空坐标并在 ③.5 说明，**处理正确**。
- **`the_foothill_caverns`** ——现今 wiki 把它丢进「RPG items」，看起来像不该收；但客户端 area 277 真实存在、
  parent=36，且是 vanilla 部落进奥山的入口。**作者收它是对的，别被 wiki 的分类误导。**
- **四个 zone 的等级带与阵营**（1-10 部落 / 10-20 部落 / 20-30 中立 / 30-40 中立）与奥山 `51-60` 均无误。
- **中文译名全部复核**：凡带 `AreaTable` 出处的节点，其 `name_zh` 我用 zhCN 客户端表重新对了一遍，
  逐字吻合（瑟伯切尔 / 焚木村 / 粘丝洞 / 博伦的巢穴 / 碧玉矿洞 / 炉灰庄园 / 赎罪岛 / 奈杉德哨岗 /
  达伦德农场 / 休息区 / 恐惧之末旅店 …）。**没有一个是作者自己音译的。**

### V.5 我实际抓到的页面清单

**warcraft.wiki.gg（`?action=raw`，逐句做子串比对）**：`Tirisfal_Glades` · `Silverpine_Forest` ·
`Hillsbrad_Foothills` · `Alterac_Mountains` · `Alterac_Valley`（抓两次：子区域清单 + 可占领目标原文）·
`Undercity` · `Brill`（抓两次：开篇 + 建筑原文）· `Deathknell` · `Pyrewood_Village` · `Bulwark` ·
`Ruins_of_Lordaeron` · `Ruins_of_Alterac` · `Scarlet_Monastery` · `Scarlet_Monastery_(Classic)` ·
`Shadowfang_Keep`（raw + 渲染页取等级带）· `Sepulcher` · `Greymane_Wall` · `Tarren_Mill` · `Southshore` ·
`Durnholde_Keep` · `Purgation_Isle` · `Strahnbrad` · `Ravenholdt_Manor` · `Dalaran_Crater`

**wago.tools 数据表（重新独立下载，没有沿用作者的结果）**：
`AreaTable`(enUS) · `AreaTable`(zhCN) · `GameObjects`(enUS/zhCN)

**抓不到**：`wow.huijiwiki.com` 全站 **403**（我复验了，作者所记属实）。
`AreaPOI` 在 1.15.9 build 下取不到（HTTP 55/空）。本次会话 **WebSearch 配额已耗尽（200/200）**，
无法用搜索兜底最后几个中文名。

### V.6 仍然存疑（下游注意）

1. **新增 14 个节点的中文名没有官方出处**。它们都不是客户端区域，拿不到 `AreaTable` 的国服简体名，
   `GameObjects` 表里也只有地图图钉类物件、不含奥山的碉堡与塔。因此
   `丹巴达尔北面碉堡 / 雷矛医疗站 / 冰血塔 / 东霜狼塔 / 霜狼救援站 / 焚木村议事厅 …` 全部是社区通用写法，
   已逐个 `ai_draft` + 在 `note_zh` 里写明「以 name_en 为准」。**若画面里要出现名牌，请人眼对国服截图确认。**
2. **`The Skittering Dark` 的挂法在树内部不自洽**：作者把 `north_tides_hollow` 挂到了 `north_tides_run` 之下
   （跟随 wiki 的嵌套），却把同样被 wiki 嵌在 North Tide's Run 之下的 `the_skittering_dark` 挂在 zone 直下
   （跟随 AreaTable 的扁平结构）。两者客户端里都是银松的直接子区域。**我没有改**——改哪一边都会把作者
   已经定稿的一种取舍推翻，而两种挂法都不算错。合龙时若要统一，建议一律以 `AreaTable` 的 `ParentAreaID` 为准。
3. **斯坦恩布莱德的建筑没有补**。wiki 条目里提到 town hall / blacksmith / town cells / forge，
   但这些描述主要来自**魔兽争霸 III 战役**（阿尔萨斯屠城那一关），不能确证 vanilla 的 WoW 场景里存在同名建筑。
   按「宁缺勿编」放弃——这是本次唯一一处**主动不补**的候选。
4. **血色修道院四翼的等级带**（26-36 / 29-39 / 32-42 / 35-45）在 wiki 上查不到数字（信息框用的是缩放模板，
   `Scarlet_Monastery_(Classic)` 页也只给 7.3.5 之后的值）。作者标 `ai_draft` 是诚实的，但**这四个数字目前无出处**。
5. 作者 ③ 节列的 11 条存疑我逐条看过，**没有一条是我能在本次会话里消解的**，原样保留。
