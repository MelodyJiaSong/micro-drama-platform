# c67 不朽尸王 · 原版模型参考（WC3 模型 `units\creeps\Zombie\Zombie`，中立僵尸；DotA 放大 2 倍。大招形态 `units\other\FleshGolem\FleshGolem`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式（文件名经 Wowpedia API 查得）；YouTube 只取封面与自动截帧，没下视频。
> 僵尸是中立生物模型，没有明显的队伍色区；PlayDotA 动图头顶飘的几颗粉色小点是模型自带的飞散腐屑 / 蝇虫粒子。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero95_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/95/character.gif（PlayDotA 不朽尸王页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/undying） | fc20d5396158 | **DotA 1 里的不朽尸王本体**（120 px，10 帧）：严重驼背、头垂在胸前，**苍白偏淡紫的皮肤**；**肩背上压着一大团土黄色的破布 / 披裹**；前臂、小腿、腰间缠着一圈圈**土黄色布条**；手臂细长垂到膝下；头顶飘几颗粉色小点 |
| playdota_hero95_icon.gif | 同上 `/hero/95/icon.gif` | 05c2372eb2c3 | DotA 1 头像：**淡紫色的秃头长脸**、凹眼一只发白、长鼻、下垂的厚嘴唇、脸上几点暗红斑；尖耳；肩上土黄色布 |
| wowpedia_BTNZombie.png | https://static.wikia.nocookie.net/wowpedia/images/7/7c/BTNZombie.png（页面 https://wowpedia.fandom.com/wiki/Zombie_(Warcraft_III)） | ae2abcfdba9f | 经典版僵尸图标，与 DotA 头像同一张 |
| wowpedia_ZombieWC3.png | https://static.wikia.nocookie.net/wowpedia/images/c/ca/ZombieWC3.png | dddda540b836 | **经典模型正面（最清楚）**：秃头、苍白偏淡紫的脸，深陷的黄绿眼、下垂嘴；脖子上一圈黄布领；**肩背一大块土黄色破布像驼峰一样拱起**；白骨似的细长四肢上缠着一道道**黄色布带**；整体严重驼背 |
| wowpedia_Fleshgolem.JPG | https://static.wikia.nocookie.net/wowpedia/images/7/74/Fleshgolem.JPG（页面 https://wowpedia.fandom.com/wiki/Flesh_Golem_(Warcraft_III)） | daeb73e882c5 | **大招形态血肉傀儡**：巨大魁梧，**头上罩一个带牙的蓝灰金属头罩**、两侧弯角；两肩与前臂是巨大的蓝灰金属护甲、金色纹饰；胸腹是苍白的缝合肉块、缝线带暗红 |
| wowpedia_BTNFleshGolem.png | https://static.wikia.nocookie.net/wowpedia/images/8/81/BTNFleshGolem.png | b5c2021aa855 | 血肉傀儡图标：金边黑面罩、下半张脸是一排缝合的肉色牙齿状褶皱 |
| `yt_1pT6jXLiyLY_maxresdefault.jpg` | 已删：Dota 2 来源，follow-up 316（原视频封面中间是 Dota 2 原画与图标） | — | — |
| yt_3pr63bQAmZo_hq2.jpg | https://i.ytimg.com/vi/3pr63bQAmZo/hq2.jpg（「DOTA 1: Dirge (Undying) WC3 DotA gameplay」https://www.youtube.com/watch?v=3pr63bQAmZo 自动截帧） | 2eb2f99c4ae2 | DotA 1 游戏内：底部肖像是淡紫秃头僵尸，单位名 Dirge |

## 结论（据图）

1. **皮色**：**苍白偏淡紫**（像失血发青的死人皮），不是灰绿。旧卡「灰绿、青紫斑」主色错。
2. **头**：秃头（不是斑秃留灰发）、长脸、凹眼、长鼻、下垂厚唇、尖耳，脸上几点暗红斑。
3. **衣着**：**肩背上一大团土黄色破布裹成驼峰状**，脖子一圈黄布领；四肢上缠一道道土黄色布条（像裹尸布带）。旧卡「褪色发霉的灰褐粗麻衣、破裤」颜色与形制都不对。
4. **体型**：严重驼背、头垂在胸前，四肢细长、手垂到膝下（与旧卡一致）。
5. 头顶飘的粉色小点是腐屑 / 蝇虫粒子（可做成几只苍蝇）。
6. **大招形态 `c67-1`**：血肉傀儡是带牙金属头罩、两肩与前臂巨大蓝灰金属甲（金纹）、胸腹苍白缝合肉块——卡里形态节「皮色斑驳、灰绿瘟疫薄雾」没提金属头罩和蓝灰甲（本次不改形态，待做 `c67-1` 时按本图）。

## 与当前立绘对比（2026-10-21）

当前立绘 `c67_Undying.png`（2026-10-18，sha `f61b331276a5`，改名留档为 `c67_Undying_v1.png`）：

- ✅ 瘦长干瘪、驼背、长臂垂膝、赤脚、徒手。
- ❌ 皮色灰褐偏绿；原版是苍白偏淡紫。
- ❌ 衣着是灰褐破麻衣＋麻绳＋破裤；原版是肩背土黄色破布驼峰＋四肢土黄布条缠裹。
- ❌ 头上留几缕灰发；原版秃头、尖耳。

**差异等级：大**（主色与服装主色都错）→ 改卡，待出图。
