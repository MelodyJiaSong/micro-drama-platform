# m151 地雷 · 原版模型参考（WC3 地精地雷 Goblin Land Mine，`GoblinLandMine`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-22 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面，没下视频。
> **队伍色提醒**：DotA 1 近卫英雄玩家色是蓝 / 青 / 紫 / 黄 / 橙，没有红；两段实机截图里的地雷都是暗红色，图标也是红色，所以**红色是地雷本色**，不是队伍色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_BTNGoblinLandMine.png | https://static.wikia.nocookie.net/wowpedia/images/1/19/BTNGoblinLandMine.png（文件页 https://wowpedia.fandom.com/wiki/File:BTNGoblinLandMine.png） | 03a62d149d82 | 经典图标：**一枚扁圆盘**，像倒扣的小圆盾：顶面**暗红色**、分成一瓣瓣扇形板、每瓣一颗金色铆钉；外缘一圈银灰钢边；**正中一圈金环托着一根银灰色钢锥尖朝上**；盘边向外伸出几根**金黄色三角尖刺** |
| wowpedia_BTNGoblinLandMine-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/6/69/BTNGoblinLandMine-Reforged.png | 929bdfd12648 | 重制版图标：同一设计更清楚——红漆扇形瓣、金铆钉、银钢外圈、正中金环加钢锥、盘边外伸金色尖刺 |
| playdota_hero107_skill0.jpg | https://web.archive.org/web/2014id_/http://media.playdota.com/hero/107/skill-0.JPG（PlayDotA 地精工程师页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/goblin-techies） | db67a83ec955 | **DotA 1「埋布地雷」技能图标** = 地精地雷图标 |
| yt_u3IcL8R5ZuQ_maxresdefault.jpg | https://i.ytimg.com/vi/u3IcL8R5ZuQ/maxresdefault.jpg（「DOTA TECHIES PRO LAND MINES: FIRST BLOOD! (EPIC BAIT)」https://www.youtube.com/watch?v=u3IcL8R5ZuQ） | 690788f08478 | **DotA 1 实机**：神符旁边埋着的一颗地雷（红箭头所指）——**暗红色圆盘，一圈浅色尖刺向外张开**；左下角放大的地雷图标 |
| yt_DSzMXv11HbM_maxresdefault.jpg | https://i.ytimg.com/vi/DSzMXv11HbM/maxresdefault.jpg（「DOTA TECHIES PRO MINES – INSTANT DEATH」https://www.youtube.com/watch?v=DSzMXv11HbM） | eebb967ab936 | DotA 1 实机：石板路上一颗地雷（红箭头所指），同样是红盘加一圈尖刺，旁边一群小兵正踩上去爆开 |
| yt_QVsZ4nieQm4_maxresdefault.jpg | https://i.ytimg.com/vi/QVsZ4nieQm4/maxresdefault.jpg（「DOTA GOBLIN TECHIES: Everyone Stepping on Mines!」https://www.youtube.com/watch?v=QVsZ4nieQm4） | f03e410e6856 | DotA 1 实机：地雷图标 + 地雷炸开的一大团白黄火光 |
| compare_classic_crops.png | 本地拼图（两张图标 + 两段实机的放大裁切） | f5523e058b93 | 出图验收对照用 |

## 结论（据图）

1. **形制**：一枚扁圆盘地雷，像倒扣的小圆盾——顶面微微隆起，分成一瓣瓣扇形铁板。
2. **主色**：**暗红色**的盘面（红漆），配**金黄色铆钉**与**银灰钢外圈**；不是黑铸铁。
3. **顶部**：正中一圈金色（黄铜）环托着一根**朝上的银灰钢锥尖**——这是触发针，也是第一识别点。
4. **尖刺**：盘的外缘一周向外伸出几根（图标约 4–6 根）**金黄色三角尖刺**，实机远看就是「红盘外一圈尖刺」。
5. **没有引信**：图标与实机都看不到麻绳引信。
6. 爆炸：一大团白黄火光（地图导入 `NewGroundEX.mdx`，d04 §14）。

## 与当前立绘对比（2026-10-22）

当前立绘：`m151_Land_Mine.png`（sha `be4ca20a6050`，2026-10-18）。

- ❌ **主色**：通体黑铸铁锈色；原版暗红盘面、金铆钉、银钢边。
- ❌ **顶部识别点**：一块平的黄铜压板；原版正中一根朝上的钢锥尖。
- ❌ **附加物**：没有外缘一圈金色三角尖刺；多了一截麻绳引信。
- ✅ 扁圆盘形、一圈铆钉、尺度（盘子大小）。

**差异等级：大**（主色、顶部钢锥、外圈尖刺三项识别层错）→ 改卡；出图暂停，待出图。
