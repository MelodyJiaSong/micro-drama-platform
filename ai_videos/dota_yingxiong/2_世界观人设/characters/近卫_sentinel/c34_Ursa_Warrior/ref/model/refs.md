# c34 熊战士 · 原版模型参考（WC3 中立野怪「熊怪追踪者 Furbolg Tracker」`units\creeps\FurbolgTracker`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面（没下视频）。
> **身上的大红色块是队伍色**（红方），随玩家变，不是本色；界面头像整张发红是「激怒」嗜血术的红光，也不是本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero100_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/100/character.gif（PlayDotA 熊战士页 https://web.archive.org/web/2013/http://www.playdota.com/heroes/ursa-warrior） | 3ab5f02c3b3c | **DotA 1 里的熊战士本体**（120 px，18 帧）：弓背直立的熊怪，**炭黑 / 深灰皮毛**；背上一块大的**橄榄绿皮甲（风筝盾形）、黄褐色包边**，肩、胸、头顶也是绿甲；红色块是队伍色；挥爪攻击 |
| playdota_hero100_character_frame.png | 本地：上图抽 8 帧放大 3 倍 | 300bc046acea | 看图用 |
| playdota_hero100_icon.gif | 同上 `/hero/100/icon.gif` | e4400316fcc0 | DotA 1 头像：黑灰色熊脸侧面，张大嘴满口尖牙、粉红牙龈；**头顶戴绿色兜帽式头盔，黄褐包边**，琥珀色小眼 |
| playdota_hero100_icon_frame.png | 本地：上图放大 3 倍 | 698e8a451ffe | 看图用 |
| wowpedia_BTNFurbolgTracker.png | https://static.wikia.nocookie.net/wowpedia/images/3/31/BTNFurbolgTracker.png（页面 https://wowpedia.fandom.com/wiki/Furbolg） | 7274b7bc9682 | 经典图标，与 DotA 1 头像同 |
| wowpedia_Warcraft_III_-_Furbolg_Tracker.gif | https://static.wikia.nocookie.net/wowpedia/images/8/8d/Warcraft_III_-_Furbolg_Tracker.gif | 612dea7d76fd | 经典模型动图（15 帧）：同 DotA 1——黑灰毛、绿甲黄边、红色队伍色 |
| wowpedia_Warcraft_III_-_Furbolg_Tracker_frame.png | 本地：上图抽 8 帧放大 3 倍 | 8be692da8d45 | 看图用 |
| wowpedia_BTNFurbolgTracker-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/2/20/BTNFurbolgTracker-Reforged.png | 3e21ce3c6cf5 | 重制版图标（看细节）：张嘴咆哮、满口黄白尖牙；**额头到吻部上方罩着一个绿色皮盔、金黄包边**；脸上几道红色战纹（重制版加的） |
| wowpedia_Warcraft_III_creep_Furbolg.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/61/Warcraft_III_creep_Furbolg.jpg（页面 https://wowpedia.fandom.com/wiki/Furbolg_(Warcraft_III)） | 157a8b4cafa6 | 对照：**普通熊怪是棕毛**，追踪者（本卡）是黑灰毛加绿甲——两者别混 |
| wowpedia_Wc3r_furbolg_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/5/5a/Wc3r_furbolg_portrait.png | e406849adbbd | 对照：普通熊怪重制版肖像（棕毛） |
| yt_Pi7vav1TKzE_maxresdefault.jpg | https://i.ytimg.com/vi/Pi7vav1TKzE/maxresdefault.jpg（「Ulfsaar - Ursa Warrior」https://www.youtube.com/watch?v=Pi7vav1TKzE） | 028f5024d4b4 | **熊战士全身（重制版画面，同一设计最清楚）**：灰黑色粗毛（胸腹与四肢偏浅灰）；**头上一个高高的绿色皮盔，顶部尖、黄铜包边，只露出眼睛和吻部**；双肩绿甲黄铜边，胸口绿甲；腰前垂一块白布；粗壮的长臂、黑爪；弓背半蹲 |
| yt_cyd_nQBwMYw_maxresdefault.jpg | https://i.ytimg.com/vi/cyd_nQBwMYw/maxresdefault.jpg（「[Bring Back Memories] Classic Dota 1 Ursa gameplay AI + 6.59 map」） | 7cb8257be6fa | DotA 1（6.59）界面：头像是戴绿盔的黑灰熊脸 |
| yt_brvUWX4imJI_maxresdefault.jpg | https://i.ytimg.com/vi/brvUWX4imJI/maxresdefault.jpg（「DOTA 1 Ursa Warrior Ulfsaar GODLIKE」） | f7bdce1a8bbd | DotA 1 界面：激怒时头像整张变红（嗜血术红光） |
| yt_-ZBGBnw_IxM_maxresdefault.jpg | https://i.ytimg.com/vi/-ZBGBnw_IxM/maxresdefault.jpg（「DOTA 1 Ursa Warrior Ulfsaar Beyond GODLIKE #32」） | 042cac661680 | DotA 1 界面，对照 |
| compare_ingame_crops.png | 本地拼图（动图帧放大、界面头像、全身渲染） | 0aba835f642b | 出图验收对照用 |

## 结论（据图）

1. **毛色（主色）**：**炭黑 / 深灰粗毛**，胸腹与四肢内侧偏浅灰。不是棕熊——棕毛的是普通熊怪。
2. **头（第一识别点）**：头顶戴一个**绿色皮盔**（兜帽形、顶部略尖，黄褐 / 黄铜色包边），罩住额头和耳朵，只露出眼睛与吻部；粗短熊吻、张嘴满口尖牙。
3. **护甲（最显眼的附加物）**：**橄榄绿皮甲片、黄褐 / 黄铜包边**——背上一大块风筝盾形甲、双肩各一块、胸口一块。旧卡「赤身披饰物、没有盔甲护肩」错。
4. **体型**：粗壮的直立熊怪，弓背半蹲，长臂粗、黑爪；无兵器（爪击，与卡一致）。
5. 腰前垂一块浅色布（重制版是白布）；身上红块为队伍色，不进画面。

## 与当前立绘对比（2026-10-21）

- 一致：直立熊形生物、粗壮、空手黑爪、写实毛发。
- 不一致：① **深棕毛，原版是炭黑 / 深灰毛**；② **没有绿色皮盔和绿甲片**（头部与身上最显眼的识别物缺失）；③ 兽牙项串、鹰羽斜挎绳是旧卡创作，原版没有；④ 站得笔直，原版弓背半蹲。
- **差异等级：大**（主色错、头盔与护甲缺失，看起来是普通棕熊）→ 改卡重出。
