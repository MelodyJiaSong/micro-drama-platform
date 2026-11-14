# m4 食尸鬼 · 原版模型参考（WC3 食尸鬼 `units\undead\Ghoul\Ghoul`）

> 暴雪娱乐素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-19 follow-up 036 下载（免费公开页面，未调用收费服务）。
> DotA 1 天灾近战兵 `ugho` 直接用这个经典模型（缩放 1.15、不染色，d01 §4），所以经典版（Classic）就是本卡的标准；重制版 / DE 只作对照，**不照它们的造型**。

| 文件 | 来源 URL | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wiki_Ghoul_WC3.png | https://warcraft.wiki.gg/images/Ghoul_WC3.png（页面 https://warcraft.wiki.gg/wiki/Ghoul_(Warcraft_III)） | c55a4085bebf | **经典模型正面**：四肢着地前扑；脸像一颗头骨——粗重眉骨、深眼窝里一对小小的黄绿眼，下巴极大、往前突出，上下两排方而大的白牙整排龇出；头顶一蓬黑里带墨绿的粗乱毛发往后竖；背上、肩上几根白色骨刺；**双手没有任何兵器，每只手是三根又长又弯的淡骨色利爪，爪长接近前臂**；皮肤是干黄的骨色，上面有黑褐色的条纹；上臂、手腕各缠一圈紫布（队伍色） |
| yt_om1qboS0MO4_ghoul_side_ingame.jpg | https://i.ytimg.com/vi/om1qboS0MO4/maxresdefault.jpg（视频「The BEEFIEST Ghouls you'll ever see (Level 3 Vampiric Aura) - WC3 - Grubby」https://www.youtube.com/watch?v=om1qboS0MO4 的封面） | 0c631c4ad54a | **经典模型游戏内侧面（两只）**：深度佝偻，头往前探、低到肩的高度，巨大的下巴与整排白牙在最前面；拱背，肩上白骨刺和一撮黑毛；躯干上黑褐条纹像一根根肋骨；膝盖弯着、大腿粗，脚是带爪的；长爪垂到膝下；肩与手腕的布是队伍色（这里红色）；胯上有一块紫粉色的皮 / 布 |
| yt_JKYKzjkfRrk_ghoul_swarm_ingame.jpg | https://i.ytimg.com/vi/JKYKzjkfRrk/maxresdefault.jpg（「Mountain King vs 50 ghouls」；同图也在 c40 `ref/model/`） | 93b3178c0194 | 游戏俯视距离下的一大群食尸鬼：远看是「骨黄色身体 + 红色队伍色 + 白色长爪」的弓背小怪，读得出的是骨色和爪 |
| wiki_Ghoul.gif | https://warcraft.wiki.gg/images/Ghoul.gif | ad62c27db947 | 经典模型旧版小动图（62 px，40 帧），看动作：前扑、爪挥 |
| wiki_BTNGhoul.png | https://warcraft.wiki.gg/images/BTNGhoul.png | 1694ca07ea05 | 经典图标（DotA 1 头像即此类风格）：张大的血红嘴、一排尖牙，脸偏灰绿 |
| wiki_Ghoul_Reforged.png | https://warcraft.wiki.gg/images/Ghoul_Reforged.png | 96d166c6871b | 重制版（对照，**不照搬**）：灰蓝皮、长舌、黑灰长发、橙红长爪、腿缠布条；同样没有兵器、同样四肢着地、肩有骨刺 |
| wiki_Ghoul_DE.png | https://warcraft.wiki.gg/images/Ghoul_DE.png | 0ec0cfe2846d | DE 版（对照）：骨白皮、墨绿乱发、大下巴满口牙、每手三四根长白爪——与经典版同一设计更清楚的版本 |
| wiki_BTNGhoul-Reforged.png | https://warcraft.wiki.gg/images/BTNGhoul-Reforged.png | df029953cd6f | 重制版图标（对照）：灰蓝脸、白眼、满口獠牙与长舌 |
| compare_classic_crops.png | 本地拼图（经典正面 + 游戏内两只侧面的放大裁切） | 3312621ba06e | 出图验收对照用 |

warcraft.wiki.gg 单位资料：经典版武器一栏写的是 **Claws（爪）**，近战；兵种描述是「吃尸体回血的食人亡灵」。

## 结论（改卡依据）

旧卡（2026-10-18）凭记忆写的「灰绿干皮、光头尖耳、双手各握一把锈弯短刀、腰缠褐布」与原版不符，已改：

1. **没有刀**：武器就是手——每只手三根又长又弯的骨色利爪，爪长接近前臂。
2. **头**：头骨一样的脸，粗眉骨、深眼窝、小黄绿眼；**下巴极大、往前突，上下两排大白牙整排龇出**（没有嘴唇遮挡），这是第一识别点。
3. **毛发**：不是光头——头顶一蓬粗乱的黑毛（带墨绿光泽），往后竖起、披到后颈。
4. **背**：肩胛和脊背上几根白骨刺穿皮而出。
5. **皮**：干黄的骨色 / 赭黄干皮，带黑褐色腐烂条纹，紧贴肋骨与筋（不是灰绿色）。
6. **姿态**：深度佝偻、四肢着地，头往前探、低到肩的高度；长臂撑地，膝盖弯、脚带爪。
7. **布**：上臂、手腕缠的布在游戏里是队伍色；按 world_rules §1.4 队伍色不进画面，改成褪色发黑的脏布条，保留「缠臂缠腕」的轮廓。
