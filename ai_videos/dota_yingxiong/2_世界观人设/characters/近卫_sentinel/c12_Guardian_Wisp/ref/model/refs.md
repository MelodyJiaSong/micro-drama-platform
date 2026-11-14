# c12 守护精灵 · 原版模型参考（WC3 暗夜精灵农民「小精灵」`units\nightelf\Wisp`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式；YouTube 只取自动截帧，没下视频。
> **颜色不是队伍色**：PlayDotA 同一批动图都按红方录（全能骑士、炼金术士身上是红色），这团光却是深蓝，说明 DotA 1 里的守护精灵本身就染成蓝色；WC3 原版小精灵是青白色（Wowpedia 动图）。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero130_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/130/character.gif（PlayDotA 守护精灵页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/guardian-wisp） | 5e622aba0002 | **DotA 1 里的守护精灵本体**（120 px，28 帧）：一颗**针尖般的白亮核心**，四周**放射出一根根细长的深蓝色光芒**（像星芒 / 海胆刺，长短不一、不停旋转伸缩）；外面一圈很淡的蓝色光晕；**三四粒小光点绕着核心转**；**没有拖尾** |
| playdota_hero130_icon.gif | 同上 `/hero/130/icon.gif` | d43803af53db | DotA 1 头像：沿用 WC3 小精灵图标，一团黄绿色光雾（图标配色，不是模型颜色） |
| wowpedia_BTNWisp.png | https://static.wikia.nocookie.net/wowpedia/images/a/a8/BTNWisp.png（页面 https://wowpedia.fandom.com/wiki/Wisp_(Warcraft_III)） | 0803afa1bbd0 | 经典图标，同 DotA 头像 |
| wowpedia_Wisp.gif | https://static.wikia.nocookie.net/wowpedia/images/5/50/Wisp.gif | b3b6f2fdcd87 | WC3 经典小精灵动图（31 帧）：同一形制——白亮核心、放射状细光芒、几粒绕转光点；颜色是青白 / 淡青绿 |
| wowpedia_BTNWisp-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/d/d3/BTNWisp-Reforged.png | 77ebd06d6a9f | 重制版图标（对照，**不照搬**）：画成一张青蓝女精灵脸，与模型无关 |
| wowpedia_WC3R_Wisp_Portrait.png | https://static.wikia.nocookie.net/wowpedia/images/6/63/WC3R_Wisp_Portrait.png | 58509fb3b98e | 重制版肖像（对照，不照搬）：蓝皮精灵头像 |
| yt_S2ZaM3TXenc_hq3.jpg | https://i.ytimg.com/vi/S2ZaM3TXenc/hq3.jpg（「WARCRAFT 3 REFORGED: DOTA 1 GAMEPLAY - IO, THE GUARDIAN WISP」https://www.youtube.com/watch?v=S2ZaM3TXenc） | c0fb98cfead9 | 重制版客户端跑 DotA 1 地图：选中 Io，场上是一团蓝白光，周围技能光圈（只作对照） |

## 结论（据图）

1. **形状**：不是一团云雾球，而是**一颗很小、极亮的白色核心 + 向四面八方放射的细长光芒**（星芒状，长短不一，缓慢旋转、伸缩），外裹一圈很淡的光晕。
2. **主色**：DotA 1 版是**深蓝 / 电光蓝的光芒配白亮核心**；WC3 原版是青白。旧卡「冷白为主、淡蓝为辅」偏淡，改成「白核 + 饱和的冰蓝 / 电光蓝光芒」。
3. **绕转光点**：三四粒米粒大的小光点紧贴核心绕转（模型自带，不是技能「幽魂」的五个大光球）。
4. **没有长拖尾**：两张动图都没有拖尾；旧卡「身后拖 1–2 m 渐隐光尾」是凭记忆加的，去掉（移动时可以有很短的残光，不作识别层）。
5. 无四肢、无五官、浮空（旧卡对）。

## 与当前立绘对比（2026-10-21）

- 无四肢五官、浮空发光、白核：一致。
- **形状：不一致**——旧图是一团翻卷的烟雾状光球；原版是针尖白核放射细长光芒（星芒）。
- **拖尾：多了**——旧图向右拖出一条烟雾光尾，原版没有。
- **主色：不一致（偏差中到大）**——旧图淡冰蓝发白；DotA 1 是饱和的深蓝光芒。
- 绕转光点：缺（中）。
- **差异等级：大**（形状、颜色、多出的拖尾三项都偏，老玩家会认成普通「能量球」；拿不准按大处理）→ 改卡重出。
