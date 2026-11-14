# c35 圣堂刺客 · 原版模型参考（WC3 中立「刺客 Assassin」`units\creeps\assassin`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面与自动截帧（没下视频）。
> **肩头那片大红色翻领是队伍色**（红方），随玩家变，不是本色。
> Wowpedia「Assassin (Warcraft III)」页面上的截图与重制版肖像是人类男性强盗刺客（重制版重做），与 DotA 1 用的这个女性刺客模型不是一回事，没有采用。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero57_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/57/character.gif（PlayDotA 圣堂刺客页 https://web.archive.org/web/2013/http://www.playdota.com/heroes/templar-assassin） | fb3dfd7c7c4f | **DotA 1 里的圣堂刺客本体**（120 px，45 帧）：瘦高女性，**淡紫色皮肤**；深色兜帽 / 头发；**肩头一圈向外张开的硬翻领（红＝队伍色）**；**黑色长斗篷拖到地**；胸口与腰腹露出淡紫皮肤、深色短上衣；**腿上是橄榄黄与黑相间的缠绕绑腿**；背后斜插一根细长柄（橙色端头） |
| playdota_hero57_character_frame.png | 本地：上图抽 8 帧放大 3 倍 | d4dc94d02d11 | 看图用 |
| playdota_hero57_icon.gif | 同上 `/hero/57/icon.gif` | 34adbb215037 | DotA 1 头像：**淡紫色女性脸，眼部横着一道深蓝紫色的眼罩状面纹，眼睛发黄光，深紫色嘴唇**，头部罩在黑色里 |
| playdota_hero57_icon_frame.png | 本地：上图放大 3 倍 | d8f9a007907d | 看图用 |
| wowpedia_BTNAssassin.png | https://static.wikia.nocookie.net/wowpedia/images/f/fc/BTNAssassin.png（页面 https://wowpedia.fandom.com/wiki/Assassin_(Warcraft_III)） | b1e02300e7f0 | WC3 经典「刺客」图标，与 DotA 1 头像同 |
| yt_kMUmFQ8rWdQ_maxresdefault.jpg | https://i.ytimg.com/vi/kMUmFQ8rWdQ/maxresdefault.jpg（「Let's Play DotA Match: Lanaya, Templar Assassin」https://www.youtube.com/watch?v=kMUmFQ8rWdQ） | 35fe66fe71d5 | DotA 1（6.72）界面头像：淡紫脸、深蓝紫眼部面纹、黄绿发光的眼、深紫唇，黑兜帽 |
| yt_9jA45xCIWao_maxresdefault.jpg | https://i.ytimg.com/vi/9jA45xCIWao/maxresdefault.jpg（「DOTA 1 Templar Assassin Lanaya Beyond GODLIKE #33」） | 01b2460101c3 | DotA 1 界面头像（最清楚）：**黑色兜帽边缘尖而硬挺，框住淡紫色的瘦长脸**；深蓝紫面纹横过双眼并向两颊延伸成细线；眼睛黄绿发光；深紫唇 |
| yt_dosuK9xvVV4_maxresdefault.jpg | https://i.ytimg.com/vi/dosuK9xvVV4/maxresdefault.jpg（「★DoTa Lanaya, Templar Assassin - GamePlay」） | ac973efadfc7 | DotA 1（6.83d 界面）：左侧大头像同上 |
| compare_ingame_crops.png | 本地拼图（动图帧放大、界面头像裁切） | 610c53943acc | 出图验收对照用 |

## 结论（据图）

1. **种族（第一识别点）**：不是人类。**淡紫色皮肤的精灵女性**（暗夜精灵系），瘦高修长；脸全部露出，不戴面罩。
2. **脸**：双眼处横着一道**深蓝紫色的眼罩状面纹**，向两颊延伸出细线；**眼睛发淡黄绿光**；深紫色嘴唇。
3. **头**：黑色兜帽，兜帽边缘硬挺带尖角，框住脸。
4. **服装**：**黑色长斗篷拖到地**；肩头一圈向外张开的硬翻领（游戏里是队伍色）；深色短上衣，**露出一截淡紫色腰腹**；**腿上橄榄黄与黑相间的缠绕绑腿**。
5. **武器**：模型看不清（背后斜插一根细长柄）；普攻投射物是守望者的飞刃（d03）。卡里「腕下弯刃」属创作选择，不破坏识别层，可保留。

## 与当前立绘对比（2026-10-21）

- 一致：瘦高女性、兜帽、深色主调、腕下弯刃（创作）。
- 不一致：① **人类南欧白人，原版是淡紫皮肤的精灵**；② **面罩遮住下半脸，原版整张脸露出、眼部是深蓝紫面纹、眼睛发光**；③ **没有披风（卡里还把长披风列为负向），原版黑色长斗篷拖地**；④ 全身包裹的紧身皮甲与黑裤，原版露腰腹、橄榄黄黑相间的绑腿；⑤ 没有肩头张开的硬翻领。
- **差异等级：大**（种族与脸、斗篷都错，老玩家认不出）→ 改卡重出。
