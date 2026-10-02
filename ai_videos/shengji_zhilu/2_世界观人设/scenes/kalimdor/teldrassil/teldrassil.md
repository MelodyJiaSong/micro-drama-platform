# 泰达希尔（Teldrassil）

> **本文件由 `tools/gen_world_scenes_szzl.py` 生成，不要手改**——区一级的索引卡。区的画面与空间结构写在 `bg692_泰达希尔全境/`（区级主体，拥有区级 floor plan）。
> 层级：`scenes/kalimdor/teldrassil/`（卡利姆多 → 泰达希尔），与游戏内地图「大陆 → 区 → 子区」一致（follow-up 006）。

| 项 | 值 |
|---|---|
| 类型 | 地区 · 1-12 级 · alliance |
| 相邻 | 黑海岸 |
| 世界地图尺寸 | 4655.8 × 3103.2 m（坐标表：WorldMapArea：5091.7 × 3393.8 码 × 0.9144（https://github.com/TheGrayDot/wow-vanilla-world-coords/blob/master/worldmaparea.csv）） |
| 世界树画面 | 世界树冠顶上的浅紫靛蓝夜林，青蓝发光的巨树枝干、紫白花草与垂落的藤萝，木质吊桥与树屋盘绕而上 |
| 备注 | 暗夜精灵新手区，整座地区长在世界树的树冠上；对外唯一通路是南端鲁瑟兰村的船与传送门。等级带以 wiki 旧世专页「Teldrassil (Classic)」信息框 `level=1-12` 为准（G08-V 核验改；任务线实际集中在 1-10，两个数字都可用，取景按 1-12 算更稳） |
| 出处 | https://warcraft.wiki.gg/wiki/Teldrassil |

## 原版参考地图（只进人眼，不进模型）

- `ref/WorldMap-Teldrassil_c60.jpg.link.json` → `ai_videos/shengji_zhilu/0_research/map/refs/kalimdor/northern_kalimdor/teldrassil/WorldMap-Teldrassil_c60.jpg`
- `ref/WorldMap-MicroDungeon-Teldrassil-BanethilBarrowDen.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-Teldrassil-BanethilBarrowDen1.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-Teldrassil-FelRock.jpg.link.json` → 微型地下城图
- `ref/WorldMap-MicroDungeon-Teldrassil-ShadowthreadCave.jpg.link.json` → 微型地下城图

## 区级场地平面图

`bg692_泰达希尔全境/planning/bg692_floorplan.png`（块 ＝ 下表有坐标的 bg；山脊 / 水系 / 道路来自 `terrain.toml`）。

## bg 清单（15 个 · 每个一份主体卡 + 场地平面图）

| bg | 主体 | 类型 | 坐标 | 世界树画面 |
|---|---|---|---|---|
| **bg692** | [泰达希尔全境](bg692_泰达希尔全境/bg692_泰达希尔全境.md) | 自造 | — |  |
| **bg693** | [奥达希尔](bg693_奥达希尔/bg693_奥达希尔.md) | 聚居点 · village | — | 幽影谷正中的巨树，树身裹着螺旋木梯与平台，枝上挂满淡金光球 |
| **bg694** | [多兰纳尔](bg694_多兰纳尔/bg694_多兰纳尔.md) | 聚居点 · village | — | 林间十字路口的暗夜精灵村落，紫顶弧形木屋与藤蔓廊桥，路边立着发光的月亮石灯柱 |
| **bg695** | [鲁瑟兰村](bg695_鲁瑟兰村/bg695_鲁瑟兰村.md) | 聚居点 · port | — | 世界树根部海面上的小码头村，贝壳形白顶木屋立在水中木桩上，长栈桥伸进灰蓝海雾 |
| **bg696** | [星风村](bg696_星风村/bg696_星风村.md) | 聚居点 · village | [65, 49.6] | 东侧林中的废弃小村，几栋紫顶木屋空无一人，屋内外结满灰白蛛丝 |
| **bg697** | [班尼希尔山谷](bg697_班尼希尔山谷/bg697_班尼希尔山谷.md) | 子区域 | — | 多兰纳尔到达纳苏斯大道以南的下凹峡谷，两壁树根裸露，谷底堆着熊怪的粗木图腾 |
| **bg698** | [地狱石](bg698_地狱石/bg698_地狱石.md) | 子区域 | — | 幽影谷西侧的岩壁洞口，洞内岩石泛暗绿磷光，蝙蝠与蛛类在顶壁倒挂 |
| **bg699** | [脊骨堡](bg699_脊骨堡/bg699_脊骨堡.md) | 子区域 | [43, 65.2] | 树冠西南尽头的熊怪营地，粗木尖桩围栏、兽皮帐篷与中央大篝火，地面踩成泥 |
| **bg700** | [奥拉密斯湖](bg700_奥拉密斯湖/bg700_奥拉密斯湖.md) | 子区域 | — | 多兰纳尔以南的静水湖，湖面映出紫色树冠，岸边芦苇与倒伏的白木 |
| **bg701** | [阿里斯瑞恩之池](bg701_阿里斯瑞恩之池/bg701_阿里斯瑞恩之池.md) | 子区域 | [40, 65] | 一串阶梯状的小水潭，水色青碧，潭间有细瀑跌落，周围铺满湿润的苔石 |
| **bg702** | [幽影谷](bg702_幽影谷/bg702_幽影谷.md) | 子区域 | [58.4, 34.4] | 树冠东北的浅碗状林间谷地，紫蓝薄雾贴地，中央一株巨大发光金树，四周是新绿草坡与小木台 |
| **bg703** | [大断崖](bg703_大断崖/bg703_大断崖.md) | 子区域 | — | 多兰纳尔西北的树身裂口，断面粗糙发黑，裂缝深处是熊怪的窝棚与骨堆 |
| **bg704** | [神谕林地](bg704_神谕林地/bg704_神谕林地.md) | 子区域 | — | 西北端的圆形圣林，中央一口冷蓝月亮井，周围立着风化的精灵石柱与白色花海 |
| **bg705** | [涌泉湖](bg705_涌泉湖/bg705_涌泉湖.md) | 子区域 | — | 达纳苏斯东北的小湖，水面极静如镜，映着树冠的紫光，岸边是平铺的白石滩 |
| **bg706** | [涌泉河](bg706_涌泉河/bg706_涌泉河.md) | 子区域 | — | 从树心涌出的细河，水流清亮带微光，沿林间石槽蜿蜒，两岸铺满蕨类 |

## 未立 bg 的节点（地标 / 交通 / 副本 / 主体内部）

- 班奈希尔兽穴（`ban_ethil_barrow_den` · 子区域） → 属 班尼希尔山谷
- 鲁瑟兰村·奥伯丁航线码头（`dock_rutheran_to_auberdine` · transport · boat） → 属 鲁瑟兰村
- 鲁瑟兰村飞行点（`fp_rutheran_village` · transport · flightpath） → 属 鲁瑟兰村
- 鲁瑟兰村→达纳苏斯传送门（`portal_rutheran_to_darnassus` · transport · portal） → 属 鲁瑟兰村
- 鲁瑟兰村码头（`rut_theran_docks` · transport · boat） → 属 鲁瑟兰村
- 鲁瑟兰村飞行点（`rut_theran_flightpath` · transport · flightpath） → 属 鲁瑟兰村
- 鲁瑟兰村传送门（通达纳苏斯）（`rut_theran_portal` · transport · portal） → 属 鲁瑟兰村
- 黑丝洞（`shadowthread_cave` · 子区域） → 属 幽影谷
