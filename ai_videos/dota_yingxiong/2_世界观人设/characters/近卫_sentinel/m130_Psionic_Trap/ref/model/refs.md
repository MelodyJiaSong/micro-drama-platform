# m130 灵能陷阱 · 原版模型参考（DotA 地图单位，模型未取证）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。YouTube 只取封面与自动截帧，没下视频。
> **游戏里的红 / 蓝等纯色块常是队伍色**（随玩家变）。
> **原图不足**：查了 PlayDotA 存档、DotA Fandom（DotA 1 页只有技能图标）、十几个 DotA 1 对局 / 技能视频的封面与截帧，**没有一张看得清陷阱本体**（陷阱对敌方隐形，俯视距离下很小）。搜到的清楚画面都是 Dota 2（粉紫色地面法阵，造型不同，不算）。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero57_skill-3.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/57/skill-3.gif（PlayDotA 圣堂刺客页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/templar-assassin） | 8a1b4b60b7d9 | DotA 1 技能图标「Psionic Trap」：深色底上一道**青蓝色发光的新月 / 螺旋光纹**，外圈一圈带尖齿的光环；图标风格，不一定是模型 |
| playdota_hero57_character.gif | 同上 `/hero/57/character.gif` | fb3dfd7c7c4f | DotA 1 圣堂刺客本体动图（对照她的配色：黑斗篷、紫皮、橄榄黄黑绑腿，肩头红色硬领是队伍色） |
| playdota_hero57_character_frame.png | 由上一个 GIF 第 1 帧放大 3 倍转成 PNG（本地） | 7d0b2dd5a979 | 同上，便于看图 |
| yt_LbO7vKef28o_sddefault.jpg | https://i.ytimg.com/vi/LbO7vKef28o/sddefault.jpg（「W3 DotA Lanaya (Templar Assassin) Indefinite Trap Detonate Range」https://www.youtube.com/watch?v=LbO7vKef28o） | 29bcd86a762d | 专讲陷阱的 DotA 1 视频封面：草地上一团**青白色强光爆开**、几道光线向上射出——推测是陷阱触发 / 引爆的特效，**未确认** ⚠️ |
| yt_LbO7vKef28o_hq1.jpg | https://i.ytimg.com/vi/LbO7vKef28o/hq1.jpg（同上） | 96eacdd94568 | 同一视频游戏画面：远景，看不清陷阱本体 |
| yt_Rlk6_C4mQos_hq3.jpg | https://i.ytimg.com/vi/Rlk6_C4mQos/hq3.jpg（「Warcraft 3 Reforged: DOTA - Lanaya (the Templar Assassin) Skills !!!」https://www.youtube.com/watch?v=Rlk6_C4mQos） | e52eab728d61 | 重制版客户端跑 DotA 地图，技能说明「Trap」（引爆最近的陷阱）时的一道青蓝色光流；重制版画面，只作对照 |

## 结论（据图）

1. **陷阱本体的模型、大小、颜色：仍未核实** ⚠️。
2. DotA 1 里能看到的颜色线索是**青蓝 / 青白**（技能图标、疑似触发特效），不是紫色；但这只是图标和特效，不能当成本体外观。
3. Dota 2 的粉紫地面法阵是另一套造型，不采用。

## 与当前立绘对比（2026-10-21）

当前立绘 `m130_Psionic_Trap.png`（sha `cc4927723712`，2026-10-18）：悬浮的拳头大六棱紫水晶。

- 无法和陷阱本体比对（没有原图）。
- 能比的只有颜色线索：DotA 1 图标与疑似触发特效偏**青蓝**，旧图是**紫色**——可能不符，但证据只有图标级。

**差异等级：未定（原图不足）**。不改外观，只在卡里注明补图结果。需要人工在 DotA 1 6.83d 里实际放一个陷阱截图（或从地图文件查 `Psionic Trap` 单位的模型路径）后再定；如果确认是青蓝色地面光纹，再改卡重出。
