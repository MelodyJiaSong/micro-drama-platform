# c112 寒冬飞龙 · 原版模型参考（WC3 模型 `units\undead\FrostWyrm\FrostWyrm`，亡灵冰霜巨龙；DotA 缩放 0.9、不染色）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式（文件名经 Wowpedia API 查得）；YouTube 只取封面与自动截帧，没下视频。
> **队伍色提醒**：翼膜上的几道亮色条带与身侧的色块是队伍色（PlayDotA 动图里是亮紫、YouTube 封面里是蓝），随玩家变；翼膜底色是暗灰紫。
> PlayDotA 寒冬飞龙页的 `character.gif` 与 Wowpedia `FWWC3.gif`、暴雪官方冰霜巨龙动图是**同一个文件**（sha 相同），只留一份。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero142_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/142/character.gif（PlayDotA 寒冬飞龙页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/winter-wyvern；同文件亦见 https://static.wikia.nocookie.net/wowpedia/images/9/90/FWWC3.gif 与 http://classic.battle.net/war3/images/undead/units/animations/frostwyrm.gif） | e14fbf639ef6 | 冰霜巨龙动图（133×90，14 帧）：**骨白带黑色条纹的骨架龙**；颈背到脊背一排**又密又长的骨刺**；一对大翼，**翼膜是暗灰紫的残破皮膜、满是圆形破洞**，上有亮紫条带（队伍色）；全程悬空 |
| playdota_hero142_icon.gif | 同上 `/hero/142/icon.gif` | 195c49669214 | DotA 头像：骨白龙颅、**眼窝冰蓝发光**、满口尖牙，背景冰蓝 |
| wowpedia_BTNFrostWyrm.png | https://static.wikia.nocookie.net/wowpedia/images/2/22/BTNFrostWyrm.png（页面 https://wowpedia.fandom.com/wiki/Frost_Wyrm_(Warcraft_III)） | 0550ab383fa6 | 经典图标：同 DotA 头像 |
| wowpedia_BTNFrostWyrm-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/d/dd/BTNFrostWyrm-Reforged.png | 2cb9f4ac0506 | 重制版图标（对照）：灰白龙颅、冰蓝发光眼、长獠牙 |
| bnet_frostwyrm_portrait.gif | http://classic.battle.net/war3/images/undead/units/portraits/frostwyrm.gif（暴雪官方页 http://classic.battle.net/war3/undead/units/frostwyrm.shtml） | 5d81537a779f | 官方肖像：**骨白龙颅带黑色纹路**，额后几根向后弯的长角，颅后一圈骨刺；背景暗紫 |
| yt_9-knON4AOGU_maxresdefault.jpg | https://i.ytimg.com/vi/9-knON4AOGU/maxresdefault.jpg（「Chimaera vs Frost Wyrm」https://www.youtube.com/watch?v=9-knON4AOGU） | b8fc8ff368e6 | 模型渲染大图（右侧）：骨白长翼骨展开，**翼膜暗紫灰、边缘破碎带洞**，夹着蓝色（队伍色）条带；背上一片竖起的骨刺 |
| yt_tj9lKIdneQc_hq1.jpg | https://i.ytimg.com/vi/tj9lKIdneQc/hq1.jpg（「DOTA - Auroth the Winter Wyvern」https://www.youtube.com/watch?v=tj9lKIdneQc 自动截帧） | acd02871bf95 | DotA 英雄标题卡：用的就是冰霜巨龙头像（骨白龙颅、冰蓝眼） |

## 结论（据图）

1. **骨架**：骨白色骨架龙，骨头上有**黑色条纹 / 阴影纹**（风化发黑的缝）；龙颅修长、满口尖牙，额后几根后弯长角。与旧卡大体一致。
2. **眼**：眼窝**冰蓝发光**（头像、图标都是）。一致。
3. **翼膜（最大色块）**：**暗灰紫色的残破皮膜，布满大小圆形破洞**，边缘碎裂；不是旧卡「冰蓝色半透明冻膜挂冰凌」。队伍色条带按 world_rules §1.4 不画。
4. **骨刺**：颈背到脊背一排又密又长的骨刺，侧影毛刺刺的；旧卡没写。
5. **发光**：原版只有眼睛冰蓝发光，胸腔里没有光。旧卡「胸腔透冰蓝光」与研究稿「全身冰蓝辉光」都没有图证 ⚠️，改成只保留眼光、骨面挂霜。
6. **四肢数量**：截图都是飞行姿态，看不清是否有前腿 ⚠️（未改）。

## 与当前立绘对比（2026-10-21）

当前立绘 `c112_Winter_Wyvern.png`（2026-10-18，sha `32c98ee0504b`，改名留档为 `c112_Winter_Wyvern_v1.png`）：

- ✅ 骨架巨龙、修长龙颅与后弯长角、冰蓝发光眼、长骨尾、残破骨翼。
- ❌ 翼膜是冰蓝半透明挂冰凌；原版是暗灰紫残破皮膜、满是圆洞（最大色块错）。
- ❌ 胸腔冰蓝发光；原版没有。
- ❌ 脊背只有小骨节；原版颈背到脊背一排密长骨刺。
- ⚠️ 骨面偏黄、没有黑色条纹。

**差异等级：大**（翼膜颜色与质感是最大的色块，拿不准按大处理）→ 改卡，待出图。
