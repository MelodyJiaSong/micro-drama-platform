# m14 巨狼 · 原版模型参考（WC3 中立野怪 Timber Wolf / Giant Wolf，模型 `units\creeps\TimberWolf`）

> 暴雪娱乐 / Wowpedia 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床经其 MediaWiki API 取地址，加 `&format=original` 取原格式。YouTube 只取封面，没下视频。
> DotA 1 的巨狼与头狼都用 WC3 模型 `TimberWolf`（缩放 1.1），**巨狼染紫、头狼不染色**（d01 §5.2）。WC3 里的 Giant Wolf 也是同模型染紫，正好对照；不染色的 Timber Wolf 就是头狼的样子。DotA 1 游戏内能看清巨狼的近景截图没找到。
> **游戏里的红色腿环是队伍色**，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Timberwolf.gif | https://static.wikia.nocookie.net/wowpedia/images/4/46/Timberwolf.gif（页面 https://wowpedia.fandom.com/wiki/Timber_Wolf_(Warcraft_III)） | 82b6e8afc136 | **经典模型动图（不染色本色）**：灰白蓬乱粗毛的大狼，**肩颈一大圈炸开的长鬃**，头大、低压，前身高后身低、弓背；爪子白；腿上红环＝队伍色 |
| wowpedia_BTNTimberWolf.png | https://static.wikia.nocookie.net/wowpedia/images/5/5b/BTNTimberWolf.png（同页） | e8160ce975d4 | 经典图标：灰白狼脸，**上下长獠牙露在嘴外**、一圈蓬毛，眼睛绿光 |
| wowpedia_Warcraft_III_creep_Timber_Wolf.jpg | https://static.wikia.nocookie.net/wowpedia/images/3/35/Warcraft_III_creep_Timber_Wolf.jpg（同页） | 4b63eaef4470 | 经典版游戏内截图：两只紫色（巨狼）+ 一只灰白（本色）同框 |
| wowpedia_Wc3r_timber_wolf_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/d/db/Wc3r_timber_wolf_portrait.png（同页） | 8b3db1e6a07b | 头像（对照）：褐灰狼头，黄眼，长犬齿 |
| yt_DreiHHMlZ5E_maxresdefault.jpg | https://i.ytimg.com/vi/DreiHHMlZ5E/maxresdefault.jpg（「Warcraft 3 Lv04 Creeps 1080p」https://www.youtube.com/watch?v=DreiHHMlZ5E 的封面） | 66c72a4c078c | **经典版游戏内选中 Giant Wolf，最重要的一张**：整只狼是**明显的紫罗兰 / 蓝紫色**长毛，肩颈鬃毛蓬起；头像紫色狼头、黄绿眼、一排外露的白牙 |
| wowpedia_Warcraft_III_creep_Giant_Wolf.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/6c/Warcraft_III_creep_Giant_Wolf.jpg（页面 https://wowpedia.fandom.com/wiki/Giant_Wolf_(Warcraft_III)） | e6cf090f4d28 | 经典版游戏内：一只紫色巨狼走在草地上 |
| wowpedia_BTNGiantWolf.png | https://static.wikia.nocookie.net/wowpedia/images/b/b8/BTNGiantWolf.png（同页） | 1db4761d73ee | 重制版图标（对照）：紫红色毛、黄眼、上颚一对很长的獠牙 |
| wowpedia_Wc3r_giant_wolf_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/1/17/Wc3r_giant_wolf_portrait.png（同页） | f98ae50d8dc7 | 头像（对照）：红紫色狼头、长獠牙 |
| compare_classic_crops.png | 本地拼图（游戏内巨狼与头像放大 + 动图逐帧） | 954d27d56d18 | 出图验收对照用 |

## 结论（据图）

1. **种族 / 体型**：狼，但比真狼粗壮——**肩颈一大圈炸开的蓬乱长鬃**、头大低压、前高后低、弓着背，像披了一件毛斗篷。
2. **主色（巨狼）**：**明显的紫罗兰 / 蓝紫色长毛**，是第一眼的读法（不是「深灰里带一点冷调」）。按 world_rules §1.4 翻成可信的毛色：暗紫灰到紫罗兰灰的粗毛，不是荧光紫。
3. **主色（头狼）**：不染色，灰白蓬毛（旧卡写「灰褐」不对）。
4. **牙**：上下长獠牙露在嘴外，上犬齿特别长。
5. **爪**：浅灰白。

## 与当前立绘对比（2026-10-21）

当前立绘 `m14_Giant_Wolf.png`（sha `424e7310929f`，2026-10-18 出，改名留档为 `m14_Giant_Wolf_v1.png`）：

- ✅ 野狼（不是狗），低头龇牙，琥珀眼，尾低垂。
- ❌ 主色：纯炭灰，看不出一点紫；原版巨狼整只是紫色——主色不对，老玩家会当成头狼或普通狼。
- ❌ 轮廓：真狼的瘦长身材；原版肩颈一大圈蓬鬃、前高后低、更粗壮。
- ⚠️ 獠牙：只露一点牙尖；原版长獠牙外露（小）。

**差异等级：大**（主色缺失 + 体型轮廓偏真狼）→ 改卡，待出图（出图服务额度不足）。
