# c94 巫妖 · 原版模型参考（WC3 亡灵英雄「巫妖」`units\undead\HeroLich\HeroLich_V1`）

> 暴雪娱乐 / PlayDotA / 83dota 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取封面与自动截帧，没下视频。GIF 抽帧另存 `*_frame.png`。
> **游戏里的红/蓝/紫等纯色块常是队伍色**（随玩家变），不是角色本色：巫妖下摆布条末端的菱形片、Wowpedia 动图里的紫色都属此类。PlayDotA 动图里那团白蓝强光是霜冻护甲特效，不是身体颜色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero92_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/92/character.gif（PlayDotA 巫妖页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/lich） | 0c3d040dd0b8 | DotA 1 里的巫妖（120 px，13 帧，正面）：瘦长骨架悬空，**头后竖起一个高高的尖三角兜帽 / 硬领**；下身是一束长条下摆；周身裹着白蓝冰甲光效（技能特效） |
| playdota_hero92_character_frame.png | 上图 6 帧放大 | 7b307be3004f | 同上 |
| playdota_hero92_icon.jpg | 同上 `/hero/92/icon.jpg` | 41ffe702a78d | DotA 1 头像（= WC3 `BTNLichVersion2`）：灰白骷髅脸，**上颌一排长獠牙、两颗特别长**，眼窝发蓝紫光；头被黑色兜帽 / 高领包住，领口有金色细边 |
| dota83_hero30_portrait.jpg | https://83dota.com/assets/heroes/30/1.jpg（页面 https://83dota.com/database/heroes/30/） | 4f4130e34132 | 6.83 资料站头像，同上 |
| wowpedia_BTNLichVersion2.png | https://static.wikia.nocookie.net/wowpedia/images/4/45/BTNLichVersion2.png（页面 https://wowpedia.fandom.com/wiki/Lich_(Warcraft_III)） | d8977ee58ae0 | 同 DotA 头像 |
| wowpedia_BTNHeroLich.png | https://static.wikia.nocookie.net/wowpedia/images/b/b8/BTNHeroLich.png（同页） | 0cedc9dcc565 | WC3 巫妖英雄图标：同一张獠牙骷髅脸，黑兜帽、金边，背景蓝 |
| wowpedia_BTNHeroLich-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/c/c7/BTNHeroLich-Reforged.png（同页） | aed2efb2dd73 | 重制版图标（看细节）：旧骨色头骨，獠牙结霜、眼窝冰蓝光，头后金边高冠 / 兜帽 |
| wowpedia_Lichii.gif | https://static.wikia.nocookie.net/wowpedia/images/e/e6/Lichii.gif（同页） | 8ab254c85c2d | **WC3 巫妖模型动图，轮廓最清楚**：瘦长骨架，**头后一个向后上方伸出的高尖兜帽 / 硬领**；上身是外露骨架（肋骨、骨臂），腰下是一圈 7–8 条黑色长布条像触手一样摊在地上，末端各一块菱形片（紫＝队伍色）；没有腿 |
| wowpedia_Lichii_frame.png | 上图 4 帧放大 | 8696c4e5b7ec | 同上 |
| wowpedia_KelThuzad_Lich_Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/b/b4/Kel%27Thuzad_Lich_Reforged.png（页面 https://wowpedia.fandom.com/wiki/Kel%27Thuzad_(Warcraft_III)） | 282b2aeac48c | 重制版克尔苏加德巫妖（不同模型，只对照骨架）：外露肋骨与骨臂、腰下多条长布条散开拖地、金边 |
| yt_6GxWtZ9nAEw_maxresdefault.jpg | https://i.ytimg.com/vi/6GxWtZ9nAEw/maxresdefault.jpg（Warcraft 3 Lich 语音视频 https://www.youtube.com/watch?v=6GxWtZ9nAEw） | 231898d6de31 | 同 Lichii 动图的模型画面 + 经典图标 |
| yt_PpgezpjkfEU_maxresdefault.jpg | https://i.ytimg.com/vi/PpgezpjkfEU/maxresdefault.jpg（「DoTa 6.83d - Lich, Kel'Thuzad ★ Beyond GODLIKE! #1」https://www.youtube.com/watch?v=PpgezpjkfEU） | ffcff4329ae2 | DotA 6.83d 界面：左上角 DotA 头像是獠牙骷髅 + 黑兜帽，名字 Kel'Thuzad |
| yt_PpgezpjkfEU_hq3.jpg | https://i.ytimg.com/vi/PpgezpjkfEU/hq3.jpg（同上视频） | 3d4ffb38ad8f | DotA 1 游戏内俯视：巫妖身体偏蓝黑，带冰蓝光 |

## 结论（据图，替换旧卡凭记忆写的外观）

1. **头**：骷髅头，上颌一排尖长獠牙、两颗特别长；眼窝发冰蓝 / 蓝紫光。
2. **头饰（最显眼）**：**头后与两肩竖起一个高高的黑色尖顶兜帽 / 硬领**，像向后上方伸出的尖三角，边缘镶金色细边，把骷髅脸框在前面。不是骨角冠。
3. **上身**：外露的骨架——肋骨、脊椎、细长骨臂与骨爪都看得见；不是整件长袍裹住。
4. **下身**：腰下是一圈 7–8 条黑色长布条，像触手一样垂下并摊开拖地，末端有菱形片（游戏里紫色＝队伍色）；没有腿，悬空。
5. **主色**：黑（兜帽与布条）+ 骨白 + 金色细边；冰蓝只在眼窝与冰霜技能特效里。旧卡「深靛蓝长袍 + 灰白宽边」不对。
6. 没有武器、没有法杖。

## 与当前立绘对比（2026-10-21）

- 一致：骷髅脸、悬空无腿、下摆接寒雾、眼窝冷蓝光、无法杖。
- 不一致：头上是「黑铁冠箍 + 几根骨角」，原图是高高的黑色尖顶兜帽 / 硬领（金边）。
- 不一致：整件深靛蓝厚羊毛长袍 + 灰白宽边包住全身，原图上身是外露骨架、腰下才是黑色长布条。
- 不一致：没有獠牙（原图獠牙是头像最显眼的特征）。
- 不一致：主色深蓝，原图黑 + 骨白 + 金边。

**差异等级：大**（头饰、体型轮廓、主色都不对）→ 改卡重出。
