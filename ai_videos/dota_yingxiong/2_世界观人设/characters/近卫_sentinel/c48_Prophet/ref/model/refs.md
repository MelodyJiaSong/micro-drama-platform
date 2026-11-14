# c48 先知 · 原版模型参考（WC3 暗夜精灵战役英雄「玛法里奥」不骑鹿版 `units\nightelf\MalFurion\MalFurionNoStag`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面，没下视频。GIF 已转成同名 `*_frame.png` 方便看。
> **游戏里的红 / 蓝纯色块是队伍色**（PlayDotA 动图是红方，Furion_WC3 与 YouTube 截图是蓝方）：小腿护甲、杖身的一段、斗篷局部随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero103_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/103/character.gif（PlayDotA 先知页 https://web.archive.org/web/20131222151131/http://www.playdota.com/heroes/prophet） | 56ca572f651e | **DotA 1 里的先知本体**（120 px，52 帧）：紫皮、宽肩；一对暗蓝灰色的粗大弯角（分叉少）；**深蓝色长须垂到腰**；土黄 / 金褐色长袍下摆与大斗篷，腰间一道绿色布带；两肩宽大的金褐色叶形肩甲；左手一根比人高的长杖，杖头金色叉饰；小腿护甲是红色（队伍色） |
| playdota_hero103_character_frame.png | 上图 6 帧放大拼条（本地转换） | c08d22a6b548 | 同上，看施法与挥杖动作 |
| playdota_hero103_icon.jpg | 同上 `/hero/103/icon.jpg` | 239b00a6bed3 | DotA 1 头像：紫脸、黄眼、粗眉，**蓝色长发长须**，额角露出暗色角根 |
| wowpedia_BTNFurion.png | https://static.wikia.nocookie.net/wowpedia/images/c/c2/BTNFurion.png（页面 https://wowpedia.fandom.com/wiki/Malfurion_(Warcraft_III)） | a61f88796c98 | 经典图标，同 DotA 头像：紫皮、深蓝发须、白色纹面 |
| wowpedia_Malfurion_face_TFT.jpg | https://static.wikia.nocookie.net/wowpedia/images/d/d7/Malfurion_face_TFT.jpg | 3caf7d8fedcb | 经典肖像特写：紫脸、黄眼、两颊几道浅色纹面；**发与须都是蓝紫色**，须极浓密；头顶两侧暗色角 |
| wowpedia_Furion_WC3.jpg | https://static.wikia.nocookie.net/wowpedia/images/c/c9/Furion_WC3.jpg | 89c0b09e2588 | **经典模型游戏内近景（蓝方）**：两只**灰色粗角先向两侧平伸再向上弯**，像一对宽弯角、几乎没有细分叉；深蓝长须垂到腹部；黑色短斗篷镶灰白毛边；紫色裸臂；长杖杖头金黑相间的弯钩叉饰；小腿护甲蓝色（队伍色） |
| wowpedia_FurionTFT.jpg | https://static.wikia.nocookie.net/wowpedia/images/9/9f/FurionTFT.jpg | 0ba6fcdce10c | 骑鹿版（对照，本卡不骑鹿）：**金色大肩甲**镶蓝边、暗色弯角、深蓝长须 |
| wowpedia_BTNFurion-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/1/1e/BTNFurion-Reforged.png | 440c9ee3305d | 重制版图标（对照，**不照搬**）：绿发绿须——重制版改的色，经典版是蓝 |
| wowpedia_FurionReforged.png | https://static.wikia.nocookie.net/wowpedia/images/5/5d/FurionReforged.png | 5c3c705abd15 | 重制版骑鹿（对照）：多叉鹿角、绿发 |
| yt_LSTWm50Sa9k_maxresdefault.jpg | https://i.ytimg.com/vi/LSTWm50Sa9k/maxresdefault.jpg（「DOTA FURION FAST DIVINE RAPIER: 2 HITS = 1 KILL (FUNNY GAME)」https://www.youtube.com/watch?v=LSTWm50Sa9k） | 11d9c686afca | **DotA 1 游戏内（蓝方）**：先知金褐袍、暗色角，蓝色是队伍色；**普攻是一团绿色能量弹拖着绿烟**，弹心像一块暗色石子 |
| yt_mN9r35a4D8w_maxresdefault.jpg | https://i.ytimg.com/vi/mN9r35a4D8w/maxresdefault.jpg（「DOTA 1 Furion Nature Prophet Beyond GODLIKE #11 + ULTRA KILL」） | b1b9fc56a033 | DotA 界面「Furion / Level 8 Prophet」，确认名字与模型 |

## 结论（据图）

1. **种族与体型**：紫皮暗夜精灵，高大、**宽肩**有力（不是瘦削老人）；两颊有几道浅色纹面；眼睛金黄。
2. **发与须（主色）**：**深蓝 / 靛蓝色**长发披背，**深蓝长须极浓密、垂到腰腹**。绿发绿须是重制版的造型，不是 DotA 1。
3. **角**：一对**暗灰色粗大弯角**，从额顶先向两侧平伸再向上弯，弧度宽、分叉很少（只有角尖附近一两个短叉）；不是细密多叉的马鹿角。
4. **衣着**：两肩**宽大的金褐色叶形肩甲**（层叠的大叶片形）；背后一袭深色短斗篷，边缘镶灰白毛皮；**土黄 / 金褐色长袍下摆**及踝，腰间一道**绿色布带**；手臂裸露（紫皮）。
5. **腿**：小腿有护甲（游戏里是队伍色，不用纯红 / 纯蓝）。
6. **法杖**：比他还高的长杖，深色杖身缠金色饰箍，**杖头是金色的弯钩叉饰**（张开的爪 / 弯月形）。
7. **普攻**：绿色能量弹，带绿色烟尾。

## 与当前立绘对比（2026-10-21）

- 紫皮尖耳精灵、长须、长袍、木杖、不骑鹿：一致。
- **发须颜色：不一致**——旧图墨绿，原版深蓝（老玩家对先知的第一印象就是「紫脸蓝胡子」）。
- **角：不一致**——旧图浅骨色多叉马鹿角，原版暗灰色宽弯角、分叉很少。
- **衣着：不一致**——旧图是苔藓粗麻破布袍、树皮肩，原版是金褐色叶形大肩甲 + 毛边深色短斗篷 + 土黄长袍 + 绿腰带，整体主色偏金褐而非苔绿。
- **法杖：不一致**——旧图盘曲树枝杖，原版长杖带金色弯钩杖头。
- 体型：旧图偏瘦，原版宽肩（中）。
- **差异等级：大**（发须主色、角形、服装主色与杖都不对）→ 改卡，待出图。
