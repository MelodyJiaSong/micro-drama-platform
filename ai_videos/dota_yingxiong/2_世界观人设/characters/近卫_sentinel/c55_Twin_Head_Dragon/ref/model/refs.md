# c55 双头龙 · 原版模型参考（WC3 暗夜精灵单位「奇美拉」`units\nightelf\Chimaera`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面，没下视频。GIF 已转成同名 `*_frame.png`。
> **队伍色提醒**：翼膜与背上几块**亮色斑块**是队伍色——PlayDotA 动图（红方）里是红，Wowpedia 动图里是青，YouTube 蓝方截图里是亮蓝。紫色鳞身、骨白角与牙、暗青黑的棘刺、黄眼不随队伍变。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero46_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/46/character.gif（PlayDotA 双头龙页 https://web.archive.org/web/2013/http://www.playdota.com/heroes/twin-head-dragon） | 2a655a81b70c | **DotA 1 里的双头龙本体**（120 px，12 帧，红方）：**通身紫色鳞片**，两条长颈两颗同形龙头并排前伸、黄眼、骨白色角；一对大翼，翼与背上红色斑块（队伍色）；边缘一圈暗青黑棘刺 |
| playdota_hero46_character_frame.png | 上图 6 帧放大拼条（本地转换） | 4b11165657a0 | 同上 |
| playdota_hero46_icon.jpg | 同上 `/hero/46/icon.jpg` | 78e5f55a5680 | DotA 1 头像：两颗紫色龙头，黄眼，**骨白色的角冠与下颌獠牙** |
| wowpedia_BTNChimaera.png | https://static.wikia.nocookie.net/wowpedia/images/5/5c/BTNChimaera.png（页面 https://wowpedia.fandom.com/wiki/Chimaera_(Warcraft_III)） | 75193ae4cd16 | 经典图标：两颗紫色龙头，额后一排骨白色角冠向后掠，**下颌外露一排骨白大牙**，下巴与颈侧一圈暗青色须膜，黄眼 |
| wowpedia_Chimaera.gif | https://static.wikia.nocookie.net/wowpedia/images/7/74/Chimaera.gif（转成 `wowpedia_Chimaera_frame.png` 202ea90f1bbd） | efcd1b2a25d9 | 经典模型旧版动图：紫色鳞身、两头前伸；**身体下面只有两条后腿**，前肢就是一对大翼（翼腕带爪）；翼缘与背脊一圈暗青黑棘刺；青色斑块（队伍色） |
| wowpedia_Wc3r_chimaera_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/a/a2/Wc3r_chimaera_portrait.png | 3178772bfeba | 重制版肖像（对照）：紫色双头、骨白角冠、满口獠牙、颈下暗青须膜 |
| wowpedia_BTNChimaera-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/a/a0/BTNChimaera-Reforged.png | c9b4e790d140 | 重制版图标（对照）：紫鳞、骨白角冠、黄眼、下颌长牙、颈侧青色须膜——与经典同一设计 |
| yt_PR-l1HYZO_4_maxresdefault.jpg | https://i.ytimg.com/vi/PR-l1HYZO_4/maxresdefault.jpg（「DOTA JAKIRO TWIN HEAD DRAGON: Fire + Ice Nuke = 2000 Damage!」https://www.youtube.com/watch?v=PR-l1HYZO_4） | f54895e3bea5 | **DotA 1 游戏内近景（蓝方）**：紫色鳞身、两颗头低头前伸吐火；翼与背上亮蓝斑块是队伍色；翼缘、颈背一排暗青黑棘刺；后腿带爪、长尾尖 |
| yt_6Km6yQlVtEI_maxresdefault.jpg | https://i.ytimg.com/vi/6Km6yQlVtEI/maxresdefault.jpg（「Warcraft 3 Chimaera Quotes」） | 216b019dc8af | 经典模型展示（黑底）：紫鳞、骨白下颌牙、青色斑块（队伍色）；翼像蝙蝠翼一样垂向地面，后腿站立 |

## 结论（据图）

1. **主色**：通身**紫色 / 紫罗兰色鳞片**，腹部偏浅的蓝紫色横纹；不是深青灰。
2. **两头同形同色**：两条长颈、两颗一样的紫色龙头，黄眼；额后一排**骨白色角冠**向后掠；**下颌外露一排骨白大牙**；下巴与颈侧一圈**暗青色须膜**。两头不分冰火色（冰火只在吐息里分）。
3. **体型结构**：**只有两条后腿**，前肢就是一对大翼（翼腕有爪），像双足飞龙；不是「四条腿加一对翼」。
4. **翼**：翼膜暗紫，翼缘与背脊、颈背一排**暗青黑色棘刺**；游戏里翼上和背上的亮色斑块是队伍色，不画。
5. **尾**：长尾，尾尖带棘。
6. 悬浮单位，常悬在离地不高处扇翼。

## 与当前立绘对比（2026-10-21）

- 一身两头、两头同形同色、皮质大翼、长尾、黄眼：一致。
- **鳞色主色：不一致**——旧图是近黑的深炭灰、只有翼膜带一点紫；原版通身鲜明的紫色鳞片。
- **结构：不一致**——旧图是四条腿加一对翼，原版是两条后腿、前肢即翼。
- **头部：不一致**——旧图一对向上弯的黑角，原版额后一排骨白色角冠向后掠、下颌一排外露的骨白大牙、颈下暗青须膜。
- 棘刺：原版翼缘与背脊一排暗青黑棘刺，旧图没有（中）。
- **差异等级：大**（主色、肢体结构、头部识别都不对）→ 改卡，待出图。
