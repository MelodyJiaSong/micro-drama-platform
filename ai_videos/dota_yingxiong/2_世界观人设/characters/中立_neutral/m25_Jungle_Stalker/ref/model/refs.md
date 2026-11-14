# m25 丛林捕猎者 · 原版模型参考（WC3 中立野怪「丛林捕猎者」`units\creeps\JungleBeast`）

> 暴雪娱乐 / Wowpedia / YouTube 截图等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。
> **肩上 / 身上的小块纯色（经典截图里蓝、DotA 1 对战视频里红）是队伍色**，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_WC3_creep_Jungle_Stalker.jpg | https://static.wikia.nocookie.net/wowpedia/images/f/f4/Warcraft_III_creep_Jungle_Stalker.jpg（页面 https://wowpedia.fandom.com/wiki/Jungle_stalker） | 21c3210c5d5b | **WC3 经典模型游戏截图（正面）**：**两腿站立、弓背的猩猩式巨兽**，不是四足兽；肩背极宽、头低陷在两肩间，一对弯成弧的褐色角（带一节节横纹）从头顶两侧向上翘；暗绿皮上一张浅黄绿的网状纹；两条长臂垂到膝下，每只手三根很长的褐色弯爪；肩上一小块蓝（队伍色） |
| wowpedia_WC3_creep_Elder_Jungle_Stalker.jpg | https://static.wikia.nocookie.net/wowpedia/images/4/44/Warcraft_III_creep_Elder_Jungle_Stalker.jpg | 1274db73ae26 | 经典「年长的丛林捕猎者」（同模型放大）：同样直立弓背、长臂长爪、一对横纹弯角，暗绿身网纹 |
| wowpedia_BTNJungleBeast.png | https://static.wikia.nocookie.net/wowpedia/images/9/99/BTNJungleBeast.png | 49ae57601619 | 经典图标（DotA 1 头像）：正脸——一对黄眼深陷在眉骨下，**嘴的位置垂下一把触须**（像章鱼须的胡子），整张脸暗绿带浅黄纹；两侧角根 |
| wowpedia_BTNJungleBeast-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/e/e7/BTNJungleBeast-Reforged.png | 8e5caf576948 | 重制版图标（对照）：头顶一簇叶片、橙色发光眼、嘴部一把粗触须——与经典同一设计更清楚的版本 |
| wowpedia_Wc3r_jungle_stalker_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/7/71/Wc3r_jungle_stalker_portrait.png | 59d12387dc5f | 重制版肖像（对照）：苔绿皮、触须胡、橙眼 |
| wowpedia_Wc3r_elder_jungle_stalker_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/e/e6/Wc3r_elder_jungle_stalker_portrait.png | df41421815e7 | 重制版年长型肖像（对照）：更黄绿、触须更长 |
| yt_8CfoKZ-oTWE_hq3.jpg | https://i.ytimg.com/vi/8CfoKZ-oTWE/hq3.jpg（「Elder Jungle Stalker vs Black Dragon The Battle of Ancients」https://www.youtube.com/watch?v=8CfoKZ-oTWE ，iCCup DotA 6.8x） | da471db70a60 | **DotA 1 游戏内近景**：年长的丛林捕猎者——巨大的弓背身躯、一对横纹弯角、暗绿身上浅黄网纹、长爪；面板名 Elder Jungle Stalker |
| yt_dWAafhiyzn4_maxresdefault.jpg | https://i.ytimg.com/vi/dWAafhiyzn4/maxresdefault.jpg（「Thunder Lizard vs Elder Jungle Stalker The Battle of Ancients」） | 1dc8dbebbd35 | DotA 1 封面（右）：暗绿网纹弓背巨兽、弯角 |
| yt_1YNI8Hmrm5M_maxresdefault.jpg | https://i.ytimg.com/vi/1YNI8Hmrm5M/maxresdefault.jpg（「Mega Granite Golem VS Elder Jungle Stalker #Dota #iCCup」） | 97151307b7e4 | DotA 1 封面（右）：直立弓背的暗绿网纹身躯，身上几道红（队伍色） |
| yt_fqwVTeJ6rc8_maxresdefault.jpg | https://i.ytimg.com/vi/fqwVTeJ6rc8/maxresdefault.jpg（「Thunder Lizard VS Elder Jungle Stalker #Dota #iCCup」） | 060cd75346f2 | DotA 1 封面（左）：同上，暗绿网纹、红色队伍色块 |
| yt_fqwVTeJ6rc8_hq3.jpg | https://i.ytimg.com/vi/fqwVTeJ6rc8/hq3.jpg（同上） | e84411e3b8ad | DotA 1 游戏内：选中面板名 Jungle Stalker（普通型），头像是同一张触须脸 |
| compare_classic_crops.png | 本地拼图（经典两张截图、经典图标、DotA 1 近景的放大裁切） | 0b8d8fe5ee56 | 出图验收对照用 |

## 结论（据图）

1. **体型轮廓**：**两腿站立、深度弓背的猩猩 / 巨猿式巨兽**——肩背极宽、上身前压、头低陷在两肩之间，两条粗长的前臂垂过膝；不是四足厚皮兽。
2. **头**：一对弯成弧、从头顶两侧向上翘的褐色角，角上一节节横纹；眉骨厚，一对黄眼深陷；**嘴的位置垂着一把触须**（章鱼须似的胡子），第一识别点之一。
3. **皮**：暗绿 / 墨绿的皮，上面一张浅黄绿的网状纹（像叶脉 / 树皮裂纹），是第二识别点。
4. **爪**：每只手三根很长的褐色弯爪，长度接近前臂。
5. **附加物**：重制版头顶一簇叶片（经典版不明显，不作识别层）；身上小块纯色是队伍色，不进画面。

## 与当前立绘对比（2026-10-21）

当前立绘 `m25_Jungle_Stalker.png`（sha `96e195841002`，2026-10-18 出）：

- ❌ 体型轮廓：画成四足的犀牛 / 角龙式厚皮兽；原版是两腿站立、长臂垂膝的弓背巨兽。
- ❌ 头：鼻上一根犀角 + 额头骨冠；原版是头顶一对横纹弯角、嘴部一把触须、黄眼深陷。
- ❌ 皮：苔绿褐、长青苔细藤；原版是暗绿皮上浅黄绿网纹。
- ❌ 武器：没有长爪；原版每手三根长弯爪。
- ❌ 背上一排骨板：原版没有。
- ✅ 绿色调、体量大。

**差异等级：大**（物种轮廓、头部最显眼特征、皮纹、长爪全部不对）→ 改卡、待出图（follow-up 057）。
