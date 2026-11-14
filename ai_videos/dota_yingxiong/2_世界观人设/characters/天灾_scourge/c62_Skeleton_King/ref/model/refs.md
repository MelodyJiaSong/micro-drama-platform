# c62 骷髅王 · 原版模型参考（2026-10-25 重新 research）

> 暴雪娱乐 / PlayDotA / YouTube 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。本轮全部来自免费公开页面与地图文件，未调用收费服务。
> 2026-10-25 用户指出：旧 refs 多数是 WC3 通用骷髅小兵（Wowpedia 骷髅战士、巨型骷髅野怪、重制版 / 魔兽世界骷髅），不是 DotA 1 里的这个英雄，按它出的图不对。本轮改以**地图一手数据 + DotA 1 实机截图**为准；旧的通用骷髅图已移到 `_非本英雄_WC3通用骷髅/`，**不得再作立绘依据**。

## 一、地图一手数据（多版本对账）

解包 PlayDotA 官方地图（web.archive.org 存档 `media.playdota.com/maps/eng/…`），读 `Units\UnitUI.slk` 与 `Units\CampaignUnitStrings.txt`。英雄单位 ID 是 **`NC00`**（Name "Skeleton King"，Propernames "King Leoric"）；旧 d05 出处里的 `uske` 是 WC3 召唤用的普通骷髅战士，**不是英雄本身**。

| 版本 | NC00 模型 | 缩放 | 染色 RGB | 语音组 | 头像 portrait 覆盖 |
|---|---|---|---|---|---|
| 6.48b / 6.58b / 6.64 | `units\undead\Skeleton\Skeleton` | 1.8 | 100,125,100 | Skeleton | 无 |
| 6.68c / 6.72f / 6.77c | 同上 | 1.8 | 100,125,100 | 6.72f 起 HeroDemonHunterMorphed | 有：地图自带 `Skeleton_portrait.mdx`（引用 `Textures\Knight.blp` + `Textures\Skeleton.blp`，即加了骑士盔材质的骷髅头） |
| **6.83d（本剧锚点）** | 同上 | **1.8** | **100,125,100** | HeroDemonHunterMorphed | 无（用 WC3 原版骷髅头像） |

- 6.83d 地图里**没有**导入同路径的 `Skeleton.mdx` 或骷髅贴图覆盖，所以英雄本体就是 WC3 骷髅战士的骨架与甲，**整模放大 1.8 倍、整体乘暗绿色（100,125,100）**。
- 选人图标 `Art=BTNSkeletonArcher.blp`：借用的是 **WC3 骷髅弓箭手**的按钮（紫色金边头盔的骷髅头），所以 DotA 头像有「紫冠」，模型上没有。
- 地图里另有 `h05M`（同模型，1.6 倍、同染色，非英雄本体），不作参考。

## 二、DotA 1 实机截图（以此为准）

| 文件 | 来源 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| dota683d_ingame_hero_63s.png / _66s.png | YouTube「DotA 6.83d - Skeleton King, Leoric Guide & Gameplay」https://www.youtube.com/watch?v=XaWmjd-gUQs ，约 63 / 66 秒，1080p 原帧裁切放大 | 0d2dd00f2321 / b76a41669f68 | **6.83d 经典画质里的英雄本体**：整个人从骨到甲到裙**统一是灰白泛病态绿的一个色调**（不是白骨 + 灰钢 + 褐皮的多色）；甲边是发暗的橄榄金；两肩各一根长尖刺的大肩甲；右手一把长而弯的宽弯刀；左臂一面高的上宽下收盾，**盾面正中一个白色骷髅头纹章**，盾面底色发暗（队伍色被绿色压暗）；体型明显比周围单位大 |
| dota683d_ingame_portrait_40s.png | 同上，约 40 秒，界面头像 | 693490bc0548 | 6.83d 头像：**整颗骷髅头偏淡青绿**，眼窝两点黄光，颈下露肋骨；没有王冠、没有头盔 |
| playdota_hero76_character.gif | PlayDotA 骷髅王页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/skeleton-king （`/hero/76/character.gif`） | 27aea7056308 | 官方英雄页动图：形制同上（尖刺肩甲、宽弯刀、高盾、褐裙），但**是未染色的渲染**（盾面红为队伍色），颜色以实机为准 |
| playdota_hero76_icon.gif | 同上 `/hero/76/icon.gif` | ad4998ba6a07 | 选人图标 = WC3 骷髅弓箭手按钮（紫色金边头盔），模型上没有 |
| yt_JZ1Nfq0LjZQ_maxresdefault.jpg | 「DotA Гайд Skeleton King, Leoric」封面 https://www.youtube.com/watch?v=JZ1Nfq0LjZQ | 757dfb9dc768 | 封面正中是未染色的模型渲染，形制清楚：尖刺肩甲 + 金边、胸甲、褐裙、宽弯刀（柄端一点绿光）、木边长盾 |
| yt_XaWmjd-gUQs_maxresdefault.jpg | 上面 6.83d 实机视频封面 | 0d75df19ec0d | 6.83d 界面，单位名 King Leoric |

### 对照（不是 6.83d，不照搬）

| 文件 | 来源 | sha256 前 12 位 | 说明 |
|---|---|---|---|
| unofficial690a8_ingame_hero_crowned.png / _portrait_crowned.png | 「dota 1 Skeleton King, Leoric Good Game」https://www.youtube.com/watch?v=C6RQPNRLmYs ，界面版本号 **v6.90a8（非官方续作图）** | 17ede3d1c82f / 4dbacdcbb8d3 | 非官方图换了导入模型：白骨、**戴金冠**、头像也是戴冠骷髅。玩家若记得「戴冠骷髅王」，多半来自这类非官方图或图标，**不是 6.83d** |
| （未存图）xH2Fqh8FluQ 6.85k Reforged 片段 | 已在 `0_research/media_refs/videos/` | — | 重制版高清皮肤：暗色骷髅、尖刺头冠、圆盾带骷髅头。是 Reforged 换皮，不是 DotA 1 经典模型 |
| `_非本英雄_WC3通用骷髅/` 5 张 | Wowpedia | 见旧版记录 | WC3 普通骷髅战士 / 巨型骷髅野怪 / 重制版 / 魔兽世界骷髅；**不是本英雄**，只留档 |

## 结论（据地图数据 + 6.83d 实机）

1. **骨架与甲的形制**确实沿用 WC3 骷髅战士：两肩尖刺大肩甲、胸甲、尖护膝护胫、腰下皮裙、右手宽背弯刀、左臂高长盾。
2. **但它不是「普通骷髅小兵」的样子**，区别在三处，旧卡和旧立绘全部漏了：
   - **整体染色**：全身乘暗绿（100,125,100），骨、甲、皮裙、刀盾统一成**灰白泛病态青绿的单一色调**；旧立绘的白骨 + 黄铜 + 褐皮 + 黑盾多色搭配不对。
   - **盾面纹章**：高长盾正中有**白色骷髅头纹章**；旧卡写「盾面褪色黑漆」、旧立绘是素面黑盾，不对。
   - **体量**：1.8 倍，是战场上最显眼的大个子，不是小兵比例。
3. 头上**没有王冠、头盔、披风、火焰**（6.83d）；紫冠只在选人图标，金冠只在非官方 6.90 系列。
4. 旧 d05「出处 uske」是把召唤骷髅当成了英雄行；英雄是 NC00，本轮已核实两者模型相同但缩放 / 染色不同。

## 与当前立绘对比（2026-10-25）

当前 `c62_Skeleton_King.png`（follow-up 075 挂武器版，sha `3908c7b97f73`）：

- ✅ 尖刺大肩甲、胸甲、尖护膝、宽背弯刀、高长方盾、无冠无披风。
- ❌ 颜色：白骨 + 黄铜包边 + 褐色皮裙 + 黑盾，多色写实；原版是统一的灰白病态青绿。
- ❌ 盾面：素面黑漆，缺**白色骷髅头纹章**。
- ⚠️ 脚穿钢靴，原模型足部是骨脚加护胫（066 已记偏差）。

**差异等级：中**（形制对、色调与盾徽错）→ 改卡；用户确认后已重出 p75 与立绘（follow-up 212，旧图留档 `_before_212.png`），代理初审通过，待用户看。
