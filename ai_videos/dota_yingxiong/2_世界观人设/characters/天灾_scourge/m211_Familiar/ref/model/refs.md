# m211 佣兽 · 原版模型参考（WC3 亡灵族「石像鬼」`units\undead\Gargoyle\Gargoyle`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面与自动截帧（`hq1/2/3`＝视频约 25% / 50% / 75% 处），没下视频。GIF 抽帧另存 `*_frame.png`。
> **游戏里的红/蓝/紫等纯色块常是队伍色**（随玩家变），不是角色本色。石像鬼翼骨、翼缘和四肢上的那几道**亮紫色是队伍色**（下面几张都是紫色玩家），不是本色。DotA 1 佣兽直接用这个经典模型（d07 §15），缩放、染色分卷未记。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_GargoyleWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/8/81/GargoyleWC3.gif（页面 https://wowpedia.fandom.com/wiki/Gargoyle_(Warcraft_III)） | 0b542ddc825c | **经典模型动图**（118 px，13 帧）：身体是带金属光泽的**银灰偏冷蓝**色，细瘦骨感、四肢细长；一对很大的蝙蝠翼，翼膜深灰、带一道道肋纹，翼骨末端是钩爪；翼骨与四肢上的亮紫色是队伍色 |
| wowpedia_GargoyleWC3_frame.png | 上图 5 帧放大（本地抽帧） | 9d1ce500e892 | 同上，看翼形与身体颜色 |
| wowpedia_BTNGargoyle.png | https://static.wikia.nocookie.net/wowpedia/images/8/8e/BTNGargoyle.png | 9ce15c5b8778 | 经典图标（DotA 1 召唤佣兽也用这张）：**惨白发蓝、像骷髅的脸**，眼窝里发白紫的光；嘴大张，**下颚两颗粗大的白獠牙向上翘**，满口尖牙；**脑后与颈后一大蓬深蓝黑色的长鬃毛**；头侧一只高耸的大尖耳 |
| playdota_hero113_skill-3.jpg | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/113/skill-3.jpg（PlayDotA 死灵飞龙页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/necrolic） | 4cb7efffb713 | **DotA 1「召唤佣兽」技能图标**：就是上面的石像鬼图标 |
| wowpedia_BTNGargoyle-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/8/80/BTNGargoyle-Reforged.png | 9ee4ec7fd843 | 重制版图标（对照，看细节）：蝙蝠一样的脸、上翻的鼻孔、橙黄眼；**一对粗长的下獠牙**；头颈一圈蓬乱的深色长毛；大尖耳 |
| wowpedia_Gargoyle_WC3.jpg | https://static.wikia.nocookie.net/wowpedia/images/a/aa/Gargoyle_WC3.jpg | dcef6abb1a2b | WC3 石像鬼原画（线稿）：蹲在岩上，巨大的蝙蝠翼高举、翼骨顶端钩爪；**蝙蝠脸、巨大的蝙蝠耳**、满口獠牙、颈背一蓬乱毛；一条长尾；**没有角** |
| wowpedia_BTNStoneForm.png | https://static.wikia.nocookie.net/wowpedia/images/0/08/BTNStoneForm.png | e94a14c97391 | 「石像形态」图标：灰褐石质的收拢翼与钩爪 |
| yt_Sj0TdUg0rhA_maxresdefault.jpg | https://i.ytimg.com/vi/Sj0TdUg0rhA/maxresdefault.jpg（「24 Gargoyles vs 24 Hippogryphs - Same Food - WarCraft III Retro Battles」https://www.youtube.com/watch?v=Sj0TdUg0rhA） | 2cd84ca4ae5e | **经典模型游戏内一群**（俯视）：整体读作**冷蓝银灰**的大翼小恶魔，翼膜深灰，翼缘一圈紫（队伍色） |
| yt_6ZiWIOS2F74_maxresdefault.jpg | https://i.ytimg.com/vi/6ZiWIOS2F74/maxresdefault.jpg（「24 Flying Machines vs 12 Gargoyles - Same Food - WarCraft III Retro Battles」） | 5a616781ac16 | 同上另一群，同样银灰偏蓝身体 + 深灰大翼 |
| yt_Sj0TdUg0rhA_hq2.jpg | https://i.ytimg.com/vi/Sj0TdUg0rhA/hq2.jpg（同上视频，画面有「Stone Form Timer」） | 8a59a1c46fdc | 石像形态时：缩成一团灰白的石块状 |

## 结论（据图）

1. **体型**：细瘦骨感的有翼小恶魔，四肢细长，翼极大（翼展远超身长），一条长尾。与旧卡一致。
2. **主色**：身体是**冷蓝银灰 / 石青灰**，有一点湿冷的光泽（像打磨过的青灰石），**不是灰紫**；翼膜深灰。紫色是队伍色，不进画面。
3. **头（第一识别点）**：**蝙蝠一样的脸 + 一对高耸的大蝙蝠耳**；**脑后、颈背一大蓬深蓝黑长鬃毛**；嘴大、满口尖牙，**下颚两颗粗大的上翘獠牙**；眼窝发白光。**原版没有角**。
4. **翼**：蝙蝠式膜翼，翼骨顶端带钩爪，翼膜有一道道肋纹。
5. **石像形态**：收翼缩成一团，变成灰白石块。
6. 尾巴：长尾；尾尖是否箭头形看不清（原画里是细长尾）。

## 与当前立绘对比（2026-10-21）

对比 `m211_Familiar_v1.png`（旧图，sha `0c3bf0555226`）：

- 一致：细瘦弓背的有翼小恶魔、蹲伏、大蝙蝠翼带翼爪、长尾、满口獠牙、尖耳。
- 不一致：额头一对**后弯尖角**（原版没有角，最显眼的是一对大蝙蝠耳）。
- 不一致：**没有鬃毛**（原版脑后颈背一大蓬深蓝黑长毛，是图标里最显眼的东西）。
- 不一致：缺下颚两颗粗大上翘的**獠牙**，脸偏蜥蜴 / 龙，不是蝙蝠脸。
- 不一致：皮色**灰紫**，原版是冷蓝银灰（紫色是队伍色）。
- 小差异：箭头形尾尖（原版看不清，可以留）。

**差异等级：大**（头部最显眼特征——角 vs 蝙蝠耳 + 鬃毛 + 獠牙——和主色都不对）→ 改卡、待出图（出图服务额度不足，follow-up 057 暂停出图）。
