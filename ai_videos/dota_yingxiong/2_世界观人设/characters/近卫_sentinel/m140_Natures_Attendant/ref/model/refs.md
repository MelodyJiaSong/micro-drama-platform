# m140 小精灵（自然之助）· 原版模型参考（WC3 暗夜精灵「小精灵」`units\nightelf\Wisp`，缩放 0.3）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面与自动截帧（`hq1/hq2/hq3`），没下视频。
> **游戏里的红 / 蓝等纯色块常是队伍色**（随玩家变）。同一模型（缩放 1.3）是 `c12` 守护精灵本体，形状结论与 `c12_Guardian_Wisp/ref/model/refs.md` 一致。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Wisp.gif | https://static.wikia.nocookie.net/wowpedia/images/5/50/Wisp.gif?format=original（页面 Wisp (Warcraft III)） | b3b6f2fdcd87 | WC3 经典小精灵模型动图（31 帧）：**针尖般的白亮核心，四面放射细长光芒**（星芒状），外裹淡光晕，颜色青白；**没有拖尾** |
| wowpedia_Wisp_frame.png | 由上一个 GIF 抽 3 帧、放大 4 倍拼成 PNG（本地） | 8cb31453a5ab | 同上，便于看图 |
| wowpedia_BTNWisp.png | https://static.wikia.nocookie.net/wowpedia/images/a/a8/BTNWisp.png?format=original | 0803afa1bbd0 | WC3 经典图标（图标配色，对照） |
| playdota_hero21_skill-2.jpg | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/21/skill-2.jpg（PlayDotA 魅惑魔女页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/enchantress） | 129286eaff81 | DotA 1 技能图标「Nature's Attendants」：几颗**绿色**发光光球，带放射光芒（图标配色） |
| yt__wMNubjeDRo_hq3.jpg | https://i.ytimg.com/vi/_wMNubjeDRo/hq3.jpg（「Enchantress ruled in Dota 1」https://www.youtube.com/watch?v=_wMNubjeDRo） | df4e91518947 | **DotA 1 游戏内**：魅惑魔女四周散着七八个**蓝白色的小星点**（自然之助的小精灵），每个是一点亮核加几根短光芒，没有长尾；其中一个飞动时带一小段白色弧形残光 |
| yt_VfKzk08b2ts_maxresdefault.jpg | https://i.ytimg.com/vi/VfKzk08b2ts/maxresdefault.jpg（「DOTA 1 Enchantress Aiushtha Beyond GODLIKE #5」https://www.youtube.com/watch?v=VfKzk08b2ts） | 8f21a49c4003 | 较新地图 **7.03R10**（左下版本号）：魅惑魔女身边几颗**绿色**小光点，各拖一小段弧形残光——版本较新，颜色只作对照 |
| yt_2j3JtlUoR3I_hq2.jpg | https://i.ytimg.com/vi/2j3JtlUoR3I/hq2.jpg（「DOTA 1 Enchantress Aiushtha Beyond GODLIKE #6」https://www.youtube.com/watch?v=2j3JtlUoR3I） | 3cee430c0a4f | 同一频道较新地图：一群绿色小光点带短弧尾绕在单位间（对照） |

## 结论（据图）

1. **形状**：一颗很小、极亮的白色核心，四面放射细长光芒（星芒状），外裹很淡的光晕；**没有长拖尾**，飞动时只有一小段很短的弧形残光。
2. **大小**：缩放 0.3，比英雄小得多，一群散在她身边。
3. **颜色**：WC3 模型青白；一局 DotA 1 画面里是蓝白小星点；较新的 7.0x 地图里是绿色、DotA 图标也是绿色——6.83d 是否已染绿未核实 ⚠️。卡里按模型本色青白处理，治疗光点用淡绿白。
4. 无脸、无四肢、无翅膀。

## 与当前立绘对比（2026-10-21）

旧图 `m140_Natures_Attendant_v1.png`（sha `9f0a04c6d939`，2026-10-18）：

- 拳头大小、淡蓝白、无脸无四肢、亮度柔和：一致。
- **形状：不一致**——旧图是一颗薄纱包着的圆光球；原版是针尖白核放射细长光芒（星芒）。
- **拖尾：多了**——旧图身后一条比光核长两三倍的薄纱光尾；原版没有长尾（与 `c12` 同一问题）。

**差异等级：大**（形状与多出的长尾两项偏，和 `c12` 守护精灵同模型、同结论）→ 改卡，新立绘待出（出图服务额度不足）。
