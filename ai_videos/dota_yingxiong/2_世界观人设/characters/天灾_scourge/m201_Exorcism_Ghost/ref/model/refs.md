# m201 恶灵 · 原版模型参考（WC3「附身」飞行物 `PossessionMissile`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面与自动截帧（`hq1/2/3`＝视频约 25% / 50% / 75% 处），没下视频。GIF 抽帧另存 `*_frame.png`。
> **游戏里的红/蓝等纯色块常是队伍色**（随玩家变），不是角色本色。恶灵是飞弹模型，游戏里只有拳头大、飞得快，看不到脸；**没找到 `PossessionMissile` 本身的模型图**，以 DotA 1 游戏截图为主，可信度中等。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| yt_wXAvXo8j2xw_hq1.jpg | https://i.ytimg.com/vi/wXAvXo8j2xw/hq1.jpg（「krobelus death prophet (DoTA)」https://www.youtube.com/watch?v=wXAvXo8j2xw；同视频 `hq2` 已在 `c95_Death_Prophet/ref/model/`） | e48056965309 | **DotA 1 游戏内放驱使恶灵**：死亡先知周围一大群**鲜绿色、自带辉光的团状灵体**，边缘像火焰一样毛糙、一团团飘 |
| yt_XGMsqrKHgDo_hq3.jpg | https://i.ytimg.com/vi/XGMsqrKHgDo/hq3.jpg（「DOTA 1 Krobelus Death Prophet Beyond GODLIKE #6」https://www.youtube.com/watch?v=XGMsqrKHgDo） | c03b70cd441a | DotA 1（6.83 界面）：死亡先知身边一团绿色光团，另有几道**白中带淡紫的长条拖尾**在飞（可能是恶灵冲刺时的尾迹，也可能是她的普攻，分不清 ⚠️） |
| yt_i4_EXKwHTck_hq3.jpg | https://i.ytimg.com/vi/i4_EXKwHTck/hq3.jpg（「DOTA 1 Krobelus Death Prophet Beyond GODLIKE #5」） | 26752027901f | DotA 1 游戏内：几团小的绿色发光灵体在小兵上方飘 |
| playdota_hero109_skill-3.jpg | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/109/skill-3.jpg（PlayDotA 死亡先知页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/death-prophet，「驱使恶灵 Exorcism」） | b1acfbd54f70 | DotA 1 驱使恶灵图标：一个黑色人影，周围一圈青绿色的灵体旋涡 |
| wowpedia_BTNPossession.png | https://static.wikia.nocookie.net/wowpedia/images/0/06/BTNPossession.png（页面 https://wowpedia.fandom.com/wiki/Banshee_(Warcraft_III)） | c4d3746d2999 | WC3「附身」图标（对照）：灰白女鬼脸、紫色发光眼带 |
| wowpedia_BTNPossession-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/c/cd/BTNPossession-Reforged.png | 5bc312181c43 | 重制版附身图标（对照）：灰蓝女鬼脸、紫色发光眼 |
| wowpedia_BansheeWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/a/ae/BansheeWC3.gif | 16fd8aa4f565 | 放「附身」的 WC3 女妖（对照）：紫黑烟雾袍、灰蓝乱发 |
| wowpedia_BansheeWC3_frame.png | 上图 5 帧放大（本地抽帧） | bac5285282cd | 同上 |

## 结论（据图）

1. **颜色**：DotA 1 游戏里恶灵读作**鲜绿色、自带辉光的灵体团**（几段视频都一样）；图标是青绿旋涡。WC3 附身图标的紫色是女妖本身，不是恶灵的颜色。
2. **形状**：一团团边缘毛糙、像绿火 / 绿雾的灵体，成群绕着死亡先知飘，再扑向目标；游戏里看不到脸。
3. 冲刺时可能拖出白中带淡紫的长尾迹（⚠️ 分不清是否恶灵）。

## 与当前立绘对比（2026-10-21）

对比 `m201_Exorcism_Ghost.png`（sha `d95a7d4b8d7c`）：

- 一致：淡绿白、半透明、发光的雾状灵体，没有手脚，成群使用；颜色家族（绿）对。
- 小差异：游戏里的绿更**饱和鲜亮**，立绘偏淡、接近灰白薄荷色。
- 小差异：立绘前端有一张张嘴的骷髅人脸，游戏里看不到脸（旧卡写明是创作，不破坏识别层）。

**差异等级：小**（识别层——绿色发光灵体、成群、无实体——对）→ 不重出，只记录。以后若重出，建议把绿色调得更饱和（鲜绿辉光），脸做得更模糊。
