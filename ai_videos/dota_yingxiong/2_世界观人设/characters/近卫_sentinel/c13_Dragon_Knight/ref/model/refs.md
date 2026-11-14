# c13 龙骑士 · 原版模型参考（WC3 人类「上尉」`units\human\TheCaptain`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。
> **队伍色**：盾面底色（PlayDotA 红方是红，Wowpedia 截图蓝方是蓝）、胸口与膝甲上的宝石色块、重制版的罩袍前摆，都随玩家变；盾面中间那只白色展翅纹和金盾边是本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero49_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/49/character.gif（PlayDotA 龙骑士页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/dragon-knight） | cad7813bd695 | **DotA 1 里的龙骑士人形**（120 px，8 帧）：**金色全身甲**；**头盔两侧一对高高向后上方扬起的金属翼**；左臂一面**大鸢形盾**，金色盾边、盾面红底（队伍色）正中一只**白色展翅纹**；右手单手长剑，金色剑格 |
| playdota_hero49_icon.gif | 同上 `/hero/49/icon.gif` | d022c74e7b5e | DotA 1 头像：**金色翼盔**几乎包住整张脸，只在横缝里露出一双蓝眼与鼻梁；**下半张脸是一块银白色护颌**，像鸟喙一样向前收尖 |
| wowpedia_BTNTheCaptain.png | https://static.wikia.nocookie.net/wowpedia/images/1/1c/BTNTheCaptain.png（页面 https://wowpedia.fandom.com/wiki/Captain_(Warcraft_III)） | 5d44f3de16fb | 经典图标，同 DotA 头像 |
| wowpedia_Captain.jpg | https://static.wikia.nocookie.net/wowpedia/images/8/81/Captain.jpg | 1b4d80f24ffe | 经典肖像放大（最清楚）：金盔、侧面金翼、眼缝露出蓝眼与浓眉、银白护颌包住口鼻以下 |
| wowpedia_CaptainWC3.png | https://static.wikia.nocookie.net/wowpedia/images/e/ec/CaptainWC3.png | 578ac7f27aa9 | 经典模型全身（蓝方）：**金甲为主、关节处露钢灰**，肩甲大而圆、金色；翼盔；右手高举单手剑（金剑格、宽剑身）；左臂盾；膝与胸的蓝色宝石块＝队伍色 |
| wowpedia_BTNTheCaptain-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/1/10/BTNTheCaptain-Reforged.png | 63cd3b6cc7d9 | 重制版图标（对照）：金色雕纹头盔、深护颊，露出灰白长须的中年男人脸 |
| wowpedia_Human_Captain_REFORGED.png | https://static.wikia.nocookie.net/wowpedia/images/1/15/Human_Captain_REFORGED.png | f2ec749020b1 | 重制版模型（对照）：金色翼盔（盔顶两片金翼）、钢甲配大量金饰、蓝罩袍（队伍色）；鸢形盾蓝底、**金色展翅鹰纹**；单手长剑 |
| yt_Cic6YqQG9HI_hq1.jpg | https://i.ytimg.com/vi/Cic6YqQG9HI/hq1.jpg（「Warcraft 3 [PL] Unit Quotes - Kapitan/Captain」https://www.youtube.com/watch?v=Cic6YqQG9HI） | c25027b1a05e | 经典肖像大图：同 Captain.jpg |
| `yt_dd095BIDmiE_maxresdefault.jpg` | 已删：Dota 2 来源，follow-up 316（原「Dotaology: History of Dragon Knight」封面，DotA 1 与 Dota 2 对照） | — | — |
| yt_vDzs3XF5u4k_maxresdefault.jpg | https://i.ytimg.com/vi/vDzs3XF5u4k/maxresdefault.jpg（「DOTA 1 - Dragon Knight/Davion GODLIKE With Pro Players」） | 8c8008afa34d | DotA 1 游戏截图：Arc Honist 处于 Elder Dragon Form，场上是一条蓝龙、头像换成龙头（对照 `c13-3`） |

## 结论（据图）

1. **主色是金**：金色全身板甲（真人化＝鎏金 / 黄铜色板甲），关节与内衬露钢灰。旧卡「抛光钢银甲 + 宝蓝罩袍」与原版相反。
2. **翼盔（第一识别点）**：金色头盔，两侧各一片高高向后上方扬起的金属翼；横缝露出眼睛与鼻梁；**下半张脸由一块银白色护颌遮住**，向前收尖。旧卡「不戴头盔、露全脸」错。
3. **盾**：大鸢形盾（上宽下尖），金色盾边；盾面底色是队伍色，正中一只白色 / 金色展翅鹰纹。旧卡「宝蓝底、金竖带、不画纹章兽」改为「深蓝底（队伍色取蓝，创作选择）+ 银白展翅鹰纹」。
4. **剑**：单手长剑，金色宽剑格与圆头，剑身宽直。（旧卡对。）
5. **肩甲**：大而圆的金色肩甲。
6. 年龄：重制版图标是灰白长须的中年人；经典版脸被护颌遮住。取四十五岁上下（只露眼与鼻梁，护颌下沿露出一点灰白须）。
7. 变龙后的绿 / 红 / 蓝龙见 `c13-1/2/3`，本次未复核龙形态。

## 与当前立绘对比（2026-10-21）

- 人类骑士、单手长剑、左臂鸢形盾：一致。
- **头盔：不一致**——旧图光头露全脸；原版金色翼盔、银白护颌只露眼。
- **主色：不一致**——旧图钢银甲 + 宝蓝罩袍与披风；原版金甲为主。
- **盾面：不一致**——旧图宝蓝底金竖带；原版队伍色底 + 展翅鹰纹、金边（中）。
- 肩甲：旧图贴身钢肩甲，原版大圆金肩甲（中）。
- **差异等级：大**（头盔与主色两项识别层错，旧图像一个普通的蓝衣骑士）→ 改卡重出。
