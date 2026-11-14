# c51 干扰者 · 原版模型参考（WC3 战役英雄「萨尔」`units\orc\Thrall`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面，没下视频。GIF 已转成同名 `*_frame.png`。
> **队伍色提醒**：胸前垂下的前摆布、狼身上的布、辫子上的缠绳是队伍色——PlayDotA 动图（红方）里是红，YouTube 蓝方截图里是蓝。黑色板甲、金边、银灰色锤头、黑灰狼不随队伍变。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero131_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/131/character.gif（PlayDotA 干扰者页 https://web.archive.org/web/2013/http://www.playdota.com/heroes/disruptor） | 6ab3fc474542 | **DotA 1 里的干扰者本体**（120 px，8 帧，红方）：**骑在一头黑灰色巨狼背上**；绿皮兽人，黑色板甲、**方形黑色大肩甲镶金边与金铆钉**；手持一柄**银灰色方块锤头**的大锤；胸前红色前摆（队伍色）；狼头前伸、龇牙 |
| playdota_hero131_character_frame.png | 上图 6 帧放大拼条（本地转换） | 82b7c40bfcc3 | 同上，看骑乘与挥锤 |
| playdota_hero131_icon.gif | 同上 `/hero/131/icon.gif`（转成 `playdota_hero131_icon_frame.png` 808886cd36c8） | f3c59791a028 | DotA 1 头像：亮绿脸、蓝眼、下颌两颗白獠牙；**黑色长直发**披在脑后，**没有头盔**；发辫缠绳是蓝色（队伍色） |
| wowpedia_BTNThrall.png | https://static.wikia.nocookie.net/wowpedia/images/6/6d/BTNThrall.png（页面 https://wowpedia.fandom.com/wiki/Thrall_(Warcraft_III)） | 6aa6013547fb | 经典图标，同 DotA 头像 |
| wowpedia_Thrall2war3.JPG | https://static.wikia.nocookie.net/wowpedia/images/b/be/Thrall2war3.JPG | 475752960534 | **经典模型游戏内近景（红方）**：骑狼；黑色长发、发辫缠红绳；**方形大黑肩甲金边、金铆钉**，黑胸甲上金色涡纹；**锤头是一块银灰色的方钢块**、锤顶四棱锥；狼身披黑色金边甲片和红布 |
| wowpedia_Thrall_Reforged_Umounted.png | https://static.wikia.nocookie.net/wowpedia/images/c/c9/Thrall_Reforged_Umounted.png | 420a14dd3b1f | 重制版下马（对照，**不照搬**造型）：头顶束发、两条长辫、黑胡子；黑甲金边；银灰色方块锤头带铆钉箍——锤的形制和经典版一致 |
| wowpedia_BTNThrall-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/e/e5/BTNThrall-Reforged.png | a1875ac0976c | 重制版图标（对照）：黄绿皮、蓝眼、大獠牙、黑长发 |
| yt_A-TzOxfuJMo_maxresdefault.jpg | https://i.ytimg.com/vi/A-TzOxfuJMo/maxresdefault.jpg（「DOTA THRALL The Disruptor - HOW TO SUPPORT HIGH SKILLED GAME」https://www.youtube.com/watch?v=A-TzOxfuJMo） | b4e810b2951a | **DotA 1 游戏内近景（蓝方）**：骑狼、黑甲金边方肩甲、黑发无盔；银灰方锤；蓝色前摆与狼身甲布是队伍色 |
| yt_iQiLfIUj0nk_maxresdefault.jpg | https://i.ytimg.com/vi/iQiLfIUj0nk/maxresdefault.jpg（「DOTA THRALL - DISRUPTOR: KILLING EVERYONE! (DELETED IN SECONDS)」） | 084a0264c7e6 | DotA 1 游戏内俯视：骑狼的萨尔与银灰方锤，身边是动能力场的蓝色圆环；飞出的普攻是一柄旋转的小锤 |

## 结论（据图）

1. **坐骑（最大的识别层）**：DotA 1 的干扰者**骑着一头黑灰色巨狼**，狼身披黑色金边甲片与布。地图模型 `units\orc\Thrall` 就是骑狼的萨尔，不是步行。d04 §12 写「坐骑：无」是错的（见报告）。
2. **种族**：绿皮兽人（游戏里偏亮的黄绿，真人化取可信的橄榄绿），下颌两颗白獠牙，蓝眼。
3. **头**：**不戴头盔**；黑色长直发披到背后，耳侧几缕编成辫、缠绳（缠绳是队伍色）。
4. **铠甲**：黑色板甲，**方形大黑肩甲镶金边、钉一排金铆钉**，胸甲上金色涡纹；胸前垂一片前摆布（队伍色）。
5. **锤**：**银灰色方钢块锤头**，锤顶四棱锥、锤身几道铆钉箍；中长柄。不是黑铁锤。
6. 主色：黑甲 + 金边 + 绿皮 + 银灰锤 + 黑灰狼。

## 与当前立绘对比（2026-10-21）

- 绿皮兽人、黑色板甲、黑色长发、大锤：一致。
- **坐骑：缺**——旧图步行，原版骑黑灰巨狼（卡里写「不骑坐骑」是错的）。
- **头盔：多了**——旧图戴开面角盔，原版不戴头盔、黑长发露在外面。
- **锤头：不一致**——旧图黑铁锤头，原版银灰色方钢块锤头。
- 肩甲：旧图是层叠甲片，原版是方形大肩甲镶金边金铆钉（中）。
- **差异等级：大**（坐骑缺失、头盔多余、锤头主色不对）→ 改卡，待出图。
