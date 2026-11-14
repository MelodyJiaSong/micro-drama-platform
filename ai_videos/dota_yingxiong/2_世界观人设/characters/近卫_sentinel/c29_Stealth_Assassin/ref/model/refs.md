# c29 隐形刺客 · 原版模型参考（WC3 中立野怪「萨特欺诈者」`units\creeps\SatyrTrickster`，地图染色 RGB(130, 100, 255)）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。`*_frame.png` 是本地从 GIF 抽帧放大的拼图，`compare_classic_crops.png` 是本地放大裁切拼图。
> **队伍色**：上臂、手腕的小块红色是队伍色。DotA 地图把整个模型染成蓝紫，所以经典版萨特的本色（褐 / 紫灰）不作准，**以 PlayDotA 动图的蓝紫为准**。同一频道 `4xVEXLAu_ow`、`eGygEZs-2eM` 的头像是粉红换皮，没收。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero64_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/64/character.gif（PlayDotA 隐形刺客页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/stealth-assassin） | d2413cc47290 | **DotA 1 里的本体**（120 px，12 帧，染色后）：全身**浓重的蓝紫色**，肩背、前臂、腰下覆着蓬乱的长毛；**两根又细又长、几乎笔直向后上方斜伸的浅骨色角**；单手握一把**镰刀状的弯钩长刃**；反关节羊腿，腿上毛带黄白色条纹高光；红色队伍色臂环 |
| playdota_hero64_icon.gif | 同上 `/hero/64/icon.gif` | 02ab8fe0c369 | DotA 1 头像：蓝紫色侧脸，**乱蓬蓬的长鬃毛**向后梳，黄眼、白色獠牙 / 下颌，额上浅色角根 |
| wowpedia_BTNSatyrTrickster.png | https://static.wikia.nocookie.net/wowpedia/images/1/10/BTNSatyrTrickster.png（页面 https://wowpedia.fandom.com/wiki/Satyr_Trickster） | f4dfbe574945 | 经典图标，与 DotA 头像相同 |
| wowpedia_BTNSatyrTrickster-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/c/c9/BTNSatyrTrickster-Reforged.png | ebe4770be68c | 重制版图标（看细节）：紫灰长发与浓密胡须，黄色发光眼，宽鼻 |
| wowpedia_Wc3r_satyr_trickster_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/7/78/Wc3r_satyr_trickster_portrait.png | 81e741c92ace | 重制版肖像：长尖耳、紫灰长发、额上长角 |
| wowpedia_Satyr_trickster.gif | https://static.wikia.nocookie.net/wowpedia/images/5/55/Satyr_trickster.gif | c1f23d59721e | 经典模型动图（18 帧，未染色时也是蓝紫）：同上，细长后掠角、镰刀状弯刃、全身长毛 |
| wowpedia_Warcraft_III_creep_Satyr_Trickster.jpg | https://static.wikia.nocookie.net/wowpedia/images/e/e9/Warcraft_III_creep_Satyr_Trickster.jpg | 02873008a23e | 经典游戏截图：萨特营地，欺诈者是蓝紫色、细长后掠角、手里弯刃 |
| wowpedia_Warcraft_III_creep_Satyr.jpg | https://static.wikia.nocookie.net/wowpedia/images/7/72/Warcraft_III_creep_Satyr.jpg（页面 https://wowpedia.fandom.com/wiki/Satyr_(Warcraft_III)） | 7aea7cd872e4 | 同族萨特截图（对照体型） |
| yt_NulKcpJUJhY_maxresdefault.jpg | https://i.ytimg.com/vi/NulKcpJUJhY/maxresdefault.jpg（「DOTA 1 - Rikimaru BEYOND GODLIKE」https://www.youtube.com/watch?v=NulKcpJUJhY） | 168eb827564b | DotA 1 界面（Rikimaru）与放大的蓝紫头像 |
| yt_NulKcpJUJhY_hq2.jpg | 同上 `hq2.jpg` | f941dbd370a7 | DotA 1 界面，俯视远景 |
| compare_classic_crops.png | 本地拼图 | f0189f659ed3 | 出图验收对照用 |

## 结论（据图）

1. **主色**：全身浓重的**蓝紫色**（皮肤与毛都是），比旧卡「冻得发青的灰紫蓝」更饱和；真人化时做成深蓝紫的皮毛，不画成发亮的塑料紫。
2. **角（关键）**：两根**又细又长、几乎笔直、向后上方斜伸**的浅骨色角，比头还长；**不是盘卷的公羊角**。旧卡「向后弯掠的粗羊角」与当前立绘的盘角都错。
3. **毛**：头顶到后颈一大蓬乱蓬蓬的长鬃毛；肩背、前臂、腰下都覆着蓬乱长毛，整体像披着毛的兽，不是光溜溜的人身。
4. **下身**：反关节羊腿、偶蹄，腿上长毛带黄白色条纹高光。
5. **武器（关键）**：**单手一把镰刀状的弯钩长刃**（短柄、刃身大弧度弯回）。旧卡「双手各反握一把匕首」是 Dota 2 的印象，错。
6. 体型：弓背、和小兵差不多高，比旧卡想象的更厚实。

## 与当前立绘对比（2026-10-21）

- 一致：半羊人、反关节羊腿偶蹄、弓背、紫色调、尖耳。
- 不一致：① 角画成盘卷的公羊角，原版是细长笔直后掠的长角；② 双手各一把匕首，原版单手一把镰刀状弯刃；③ 上身光秃秃，原版头上大蓬乱鬃、肩背前臂都是长毛；④ 颜色偏灰淡紫，原版浓重蓝紫。
- **差异等级：大**（角、武器两项识别层错，改卡重出）。
