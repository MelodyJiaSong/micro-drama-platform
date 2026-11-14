# c87 地卜师 · 原版模型参考（WC3 野怪「狗头人地卜师」`units\creeps\KoboldGeomancer\KoboldGeomancer`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面与自动截帧，没下视频。
> **游戏里的红 / 蓝色布块与光圈是队伍色或选中光效**（随玩家变），不是角色本色；地卜师的**紫色是模型本色**（图标、肖像、野怪截图、DotA 1 头像都是紫，与队伍无关）。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero74_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/74/character.gif（PlayDotA 英雄列表 https://web.archive.org/web/2011id_/http://www.playdota.com/heroes 里 geomancer ＝ 74） | 7e887acc19c9 | **DotA 1 里的地卜师本体**（120 px 动图）：通体紫色的矮个狗头人，头顶一点白（蜡烛），双手横抡一把长柄大铲，铲面灰白 |
| playdota_hero74_icon.gif | 同上 `/hero/74/icon.gif` | 5fc125321f4a | DotA 1 头像：紫色鼠脸，蓝色发亮的眼睛，一排白色大板牙，头顶一圈金色 |
| wowpedia_BTNKoboldGeomancer.png | https://static.wikia.nocookie.net/wowpedia/images/4/42/BTNKoboldGeomancer.png（页面 https://wowpedia.fandom.com/wiki/Kobold_Geomancer_(Warcraft_III)） | 0ead14745982 | 经典图标，与 DotA 头像同一张 |
| wowpedia_Koboldgeomancer.gif | https://static.wikia.nocookie.net/wowpedia/images/a/a9/Koboldgeomancer.gif | 39d5dc4e0c66 | 经典模型小动图：通体紫色，拿长柄铲 |
| wowpedia_WC3_creep_Kobold_Geomancer.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/6d/Warcraft_III_creep_Kobold_Geomancer.jpg | 8e8c2dbff29e | 经典版野怪截图：选中的地卜师是**紫色**的，旁边普通狗头人是棕色——紫色是地卜师这一种的本色 |
| wowpedia_BTNKoboldGeomancer-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/a/a3/BTNKoboldGeomancer-Reforged.png | b20ba4b32f71 | 重制版图标（对照，不照搬）：粉灰鼠脸、大板牙、长须、头顶白蜡烛 |
| wowpedia_Wc3r_kobold_geomancer_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/b/b1/Wc3r_kobold_geomancer_portrait.png | b8e4cdfe1f24 | 重制版肖像（对照）：头顶一截白蜡烛、蜡泪流下，紫灰毛 |
| yt_CW-I7HSdIYI_maxresdefault.jpg | https://i.ytimg.com/vi/CW-I7HSdIYI/maxresdefault.jpg（「DOTA 1 - Pro GEOMANCER FAST HAND POFF (MEEPO) BEYOND GODLIKE」） | 5a681df96118 | **DotA 1 模型放大**：紫色鼠脸、亮蓝眼、白牙，头顶一截白蜡烛，一对很大的紫色圆耳带深蓝条纹，肩上扛一把长柄铲（铲面灰白宽大） |
| yt_Y46fLnsXQ5Y_maxresdefault.jpg | https://i.ytimg.com/vi/Y46fLnsXQ5Y/maxresdefault.jpg（「DotA 1 Geomancer Meepo Beyond GODLIKE-DotA 6.83d Style8x」） | 6931e26ba2e1 | DotA 6.83d 界面：头像是紫色狗头人 |
| yt_55YItsnPpxY_hq2.jpg | https://i.ytimg.com/vi/55YItsnPpxY/hq2.jpg（「DotA 1 Geomancer LoL Combo Imba Meepo-DotA 6.83d Style8x」） | 6e651c81ee32 | DotA 6.83d 游戏远景 |
| compare_classic_crops.png | 本地拼图（经典图标 / 动图 / 重制肖像 + PlayDotA 4 帧 + DotA 1 模型放大与野怪截图） | 1720d46b2020 | 出图验收对照用 |

## 结论（据图）

1. **主色（第一识别点）**：通体**紫色**——毛、皮都是紫罗兰色，耳朵与身上带深靛蓝条纹。不是灰褐色老鼠。
2. **头**：长鼠脸、圆钝的大鼻头，一排露在外面的白色大板牙；一对很大的圆耳；眼睛是亮蓝色。
3. **头顶**：一截白蜡烛（重制版肖像看得清蜡泪），这一点旧卡写对了。
4. **武器**：一把长柄大铲，铲面灰白宽大，平时扛在肩上，打人时横抡——旧卡的「长柄铁锹」对了，原「短杖或工具」的猜测可以去掉。
5. **体型**：矮小驼背的狗头人；DotA 放大 1.4 后和小兵差不多高。
6. 衣着在小模型上看不清，只知道整体是紫色调。

## 与当前立绘对比（2026-10-21）

当前图：`c87_Geomancer.png`（sha `b555b7f243c4`，2026-10-18 出）。

- ✅ 鼠脸矮个、驼背、头顶点燃的白蜡烛、长柄铁锹、长须。
- ❌ **主色错**：灰褐色毛、土黄粗麻袍；原版通体紫色带靛蓝条纹。
- ❌ 眼睛是黑色小眼；原版是亮蓝色眼。
- ❌ 耳朵偏小、没有那排露在外面的白色大板牙。

**差异等级：大**（皮毛主色错，老玩家记得的就是「紫色小地精拿铲子」）→ 改卡重出。

## 重出结果（2026-10-21）

新图 `c87_Geomancer.png` sha `6c48bd58a0e9`（`tools/gen_char_images.py` · ElevenLabs `gpt-image-2` · 零参考，gid `CJTMhdTFqetWj1YlgT33`），1 轮。看图核对：暗紫罗兰毛带靛蓝条纹、外露大板牙、冰蓝眼、大圆耳、头顶点燃白蜡烛、长柄大铲——与结论 1–5 一致（铲是竖持在肩侧，不是横扛，属小差异）。旧图 `c87_Geomancer_v1.png` 留档。
