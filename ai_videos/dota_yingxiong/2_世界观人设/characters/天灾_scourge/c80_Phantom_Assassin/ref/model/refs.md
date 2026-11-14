# c80 幻影刺客 · 原版模型参考（WC3 暗夜精灵英雄「守望者 Warden」`units\nightelf\herowarden\herowarden`，DotA 原尺寸、不染色）

> 暴雪娱乐 / PlayDotA 版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；warcraft.wiki.gg 原图被拦（502），只取到页面上的缩略图（WebP，本地转 PNG）。YouTube 只取封面，没下视频。`*_frame.png` 是本地把 GIF 抽帧拼成的看图用 PNG。
> **队伍色提醒**：PlayDotA 录像是红方，盔顶长缨末端和脚下的红色随玩家变；墨绿斗篷与羽翼在各来源里一致，是本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero97_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/97/character.gif（PlayDotA 幻影刺客页 http://www.playdota.com/heroes/phantom-assassin 的 Wayback 存档） | f2eb61a87c97 | **DotA 1 里的幻影刺客本体**（120 px，12 帧）：银白板甲金边、墨绿带条纹的斗篷向后飘、盔顶深紫长缨（末端红＝队伍色）、背后墨绿羽翼尖；手里一枚**外缘一圈弯钩尖齿的银白大环刃**，直径约到她腰高 |
| playdota_hero97_character_frame.png | 上图本地抽帧拼图 | ae7fa40d7071 | 看图用 |
| wiki_Warden_WC3_187px.png | https://warcraft.wiki.gg/images/thumb/Warden_WC3.png/187px-Warden_WC3.png?935fdf（页面 https://warcraft.wiki.gg/wiki/Warden_(Warcraft_III) ，缩略图 WebP 转 PNG） | 8e96e085141b | **经典模型正面，最重要的一张**：暗钢色全身板甲、金色描边，宽大尖角肩甲；尖角面甲头盔（金边），面甲下一点紫色脸；盔顶一束高竖的深紫长缨；**背后两片高过头顶的墨绿大羽翼**；长及脚踝的墨绿斗篷；一手垂着武器，脚边一圈白色弯钩刃齿 |
| wiki_Warden_DE_200px.png | https://warcraft.wiki.gg/images/thumb/Warden_DE.png/200px-Warden_DE.png?dc918b（同页 DE 版） | 21ba52c7a039 | DE 版（同一设计更清楚）：同样的暗钢金边甲、墨绿双羽翼、墨绿斗篷、深紫马尾长缨，紫皮下巴露出 |
| wowpedia_WaWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/3/39/WaWC3.gif/revision/latest?format=original（同页「WC3 animation」） | aac230d74cd9 | 经典模型动图：墨绿羽翼与斗篷，挥动大环刃，脚下青绿光圈（选择光效） |
| wowpedia_WaWC3_frame.png | 上图本地抽帧拼图 | fbc9bf5f0864 | 看图用 |
| wowpedia_BTNHeroWarden.png | https://static.wikia.nocookie.net/wowpedia/images/5/58/BTNHeroWarden.png/revision/latest?format=original | 932ff7ccfce2 | 经典图标：灰钢面甲头盔，看不到上半张脸 |
| wowpedia_BTNHeroWarden-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/f/f6/BTNHeroWarden-Reforged.png/revision/latest?format=original | e7f1ca905165 | 重制版图标（对照）：金边面甲头盔、绿光眼 |
| yt_Na7QRpM1l1g_maxresdefault.jpg | https://i.ytimg.com/vi/Na7QRpM1l1g/maxresdefault.jpg（「WC3 Hero Spotlight: The Warden」https://www.youtube.com/watch?v=Na7QRpM1l1g） | 333e5f3ed27e | 重制版模型全身（对照）：墨绿双羽翼、墨绿斗篷、暗甲金边、紫皮下半脸、高竖黑紫长缨，脚边白色钩刃 |
| yt_6nUDjmEsflM_maxresdefault.jpg | https://i.ytimg.com/vi/6nUDjmEsflM/maxresdefault.jpg（「DOTA 1 - Phantom Assassin BEYOND GODLIKE + RAMPAGE!!!」） | b50c29f38d5f | DotA 1 界面，左上角头像是守望者的金边面甲头盔 |
| yt_kdaExo1-QG0_maxresdefault.jpg | https://i.ytimg.com/vi/kdaExo1-QG0/maxresdefault.jpg（「DOTA 1 Phantom Assassin Mortred Beyond GODLIKE #26 + ULTRA KILL」） | 677da0c34daf | DotA 1 6.83 界面，单位名 Mortred |

## 结论（据图，替换旧卡凭记忆写的外观）

1. **不是兜帽刺客**：她穿全身**暗钢色板甲、金色描边**，宽大尖角肩甲。旧卡「兜帽 + 布面罩 + 黑色硬皮轻甲」错。
2. **头**：尖角面甲头盔罩住上半张脸，面甲下露紫色下半脸；盔顶一束高竖的深紫长缨。
3. **背后**：**两片高过头顶的墨绿大羽翼**——正面与侧面的第一识别点，旧卡反而把「翅膀」写进了负向。
4. **斗篷**：长及脚踝的**墨绿**斗篷，不是紫色。
5. **武器**：一枚**外缘一圈弯钩尖齿的银白大环刃**（环内握把），不是小弯镰。
6. **肤色**：暗夜精灵淡紫皮肤（下巴可见）。

## 与当前立绘对比（2026-10-21）

旧图 `c80_Phantom_Assassin_v1.png`（2026-10-18）：
- ❌ 兜帽 + 布面罩 + 黑皮衣 → 原版是面甲头盔 + 金边板甲。
- ❌ 没有墨绿双羽翼；斗篷是深紫 → 原版墨绿。
- ❌ 小号弯镰 → 原版是银白钩齿大环刃。
- ✅ 暗夜精灵女性、淡紫皮肤、尖耳、长斗篷。

**差异等级：大**（头部、服装主色、附加物羽翼、武器形制都错）→ 已按图改卡并重出。

新图 `c80_Phantom_Assassin.png`（gid `goL1YNE6u6jB8JRb8EsG`）核对：暗钢金边板甲、尖角面甲头盔露淡紫下半脸、尖耳、深紫长缨、两片高过头顶的墨绿羽翼、墨绿长斗篷、右手银白钩齿环刃带握把、腰侧三片小飞刃，均与结论一致。
