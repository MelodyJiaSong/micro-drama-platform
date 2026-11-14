# c78 幽鬼 · 原版模型参考（WC3 暗夜精灵「复仇之魂」`units\nightelf\SpiritOfVengeance\SpiritOfVengeance`，DotA 缩放 0.8、不染色）

> 暴雪娱乐 / PlayDotA 版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面与自动截帧（`hq2`＝视频约 50% 处），没下视频。`*_frame.png` 是本地把 GIF 抽帧拼成的看图用 PNG（已提亮）。
> **队伍色提醒**：环刃和眼睛的发光颜色随玩家变——PlayDotA 录像（红方）是红光，WC3 截图和「复仇天神」视频里是青绿光；不以这些光色定本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero50_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/50/character.gif（PlayDotA 幽鬼页 http://www.playdota.com/heroes/spectre 的 Wayback 存档） | a0c87699e7ac | **DotA 1 里的幽鬼本体**（120 px，9 帧，提亮后看）：整个人是半透明的烟黑灰色；头盔两侧各伸出一片又高又尖的鳍状护翼（像拉长的耳朵），眼处一点红光；身后大幅斗篷，挥动时整片甩开；手上一枚**发红光的圆环刃**；看不到脸和头发 |
| playdota_hero50_character_frame.png | 上图本地抽帧拼图（提亮 2.5 倍） | 6277ab5e3314 | 看图用 |
| wowpedia_Spirit_of_Vengeance_W3.jpg | https://static.wikia.nocookie.net/wowpedia/images/a/a2/Spirit_of_Vengeance_W3.jpg/revision/latest?format=original（页面 https://warcraft.wiki.gg/wiki/Spirit_of_Vengeance ，图注「Spirit of Vengeance in Warcraft III: The Frozen Throne」） | 4f829a26ab76 | **经典模型近景，最重要的一张**：黑紫色全身甲，甲缘一圈紫色高光；头盔罩住整张脸，两侧高耸尖翼；肩甲宽大带尖角；一手托着一枚发光的圆环刃；下半身渐隐在黑暗里 |
| wowpedia_BTNSpiritOfVengeance.png | https://static.wikia.nocookie.net/wowpedia/images/9/9c/BTNSpiritOfVengeance.png/revision/latest?format=original | ee881ea9e405 | 经典图标：绿光里一张被尖翼头盔罩住的脸 |
| yt_Y6jgqK6KCNA_maxresdefault.jpg | https://i.ytimg.com/vi/Y6jgqK6KCNA/maxresdefault.jpg（「Warcraft 3 Avatar of Vengeance Quotes」https://www.youtube.com/watch?v=Y6jgqK6KCNA） | a1befad896b0 | 复仇天神（同系模型，放大版）肖像：漆黑甲胄、高耸头盔尖、青绿发光的环刃，紫色甲缘高光 |
| `yt_gaDfeIc7x6w_maxresdefault.jpg` | 已删：Dota 2 来源，follow-up 316（原「Dotaology: History of Spectre」封面，含 Dota 2 形象） | — | — |
| `yt_gaDfeIc7x6w_hq2.jpg` | 已删：Dota 2 来源，follow-up 316（同视频截帧，含 Dota 2 形象） | — | — |
| yt_4IAP9UWiBtE_maxresdefault.jpg | https://i.ytimg.com/vi/4IAP9UWiBtE/maxresdefault.jpg（「DOTA 1 - Spectre BEYOND GODLIKE! (HARD GAME vs. Pro Players)」） | 941a7ed0f814 | DotA 1 界面，左上角头像：黑色头盔、两点亮光 |
| yt_4IAP9UWiBtE_hq2.jpg | 同视频 `hq2.jpg` | 177486d16391 | DotA 1 游戏俯视远景（看界面） |

## 结论（据图，替换旧卡凭记忆写的外观）

1. **不露脸**：头盔罩住整张脸，只在面甲缝里透一点眼光；没有飘散长发。旧卡「脸部轮廓清楚、长发向后飘」错。
2. **头盔**：两侧各向上斜伸一片又高又尖的鳍状护翼，高出头顶，是正面第一识别点。
3. **颜色**：整体烟黑 / 黑紫，半透明，甲缘一圈暗紫高光；不是「发紫蓝光的淡紫色皮肤」。
4. **甲与斗篷**：全身甲，宽大的尖角肩甲；身后一件大幅斗篷，动作时整片甩开。
5. **武器**：**圆环刃**（整圈是刃），不是弯月形长刀。发光颜色是队伍色。
6. **下身**：下半身在暗处渐隐，飘浮感保留（旧卡「腰以下全散成烟、没有腿」偏离，原模型有腿甲）。

## 与当前立绘对比（2026-10-21）

旧图 `c78_Spectre_v1.png`（2026-10-18）：
- ❌ 露出完整精灵女脸 + 飘散长发 → 原版是罩脸的高翼头盔。
- ❌ 发光的淡紫半透明皮肤 → 原版是烟黑甲胄、暗紫甲缘。
- ❌ 弯月形长刀 → 原版是圆环刃。
- ❌ 没有斗篷、没有尖角肩甲。
- ✅ 女性、半透明、飘浮、冷紫色调。

**差异等级：大**（头部最显眼特征、主色、武器类型都错）→ 已按图改卡并重出。

新图 `c78_Spectre.png`（gid `E7dXFCpINvUZI15PscQs`）核对：双鳍尖翼面甲头盔不露脸、烟黑甲胄暗紫甲缘、尖角肩甲、烟状破边斗篷、右手圆环刃带横握把、小腿以下散成黑烟飘浮，均与结论一致。质感偏概念设计图、半透明感偏弱，属小细节。
