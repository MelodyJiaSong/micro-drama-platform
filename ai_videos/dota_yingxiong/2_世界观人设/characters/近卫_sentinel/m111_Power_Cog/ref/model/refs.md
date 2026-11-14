# m111 能量齿轮 · 原版模型参考（WC3 建筑「能量发生器」`PowerGenerator`，缩放 0.75）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式（页面本身被 Cloudflare 拦，用 Wowpedia API 查到图片地址）。YouTube 只取封面与自动截帧（`hq1/hq2/hq3`＝视频约 25% / 50% / 75% 处），没下视频。
> **游戏里的红 / 蓝等纯色块常是队伍色**（随玩家变）；能量齿轮的粉红光在不同玩家的对局里都一样，不是队伍色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero65_skill-1.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/65/skill-1.gif（PlayDotA 发条地精页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/clockwerk-goblin） | 601fad3bcfba | DotA 1 技能图标「Power Cogs」：与 WC3 能量发生器图标同一张——圆形铜色底座、右侧一只齿轮、中央升起粉红光柱与粉色纹样 |
| wowpedia_BTNPowerGenerator.png | https://static.wikia.nocookie.net/wowpedia/images/9/98/BTNPowerGenerator.png（Wowpedia「Lord of Outland (WC3 Blood Elf)」「Mana crystal」页使用） | 57f49875329a | WC3 经典图标：矮圆的铜色圆盘底座，顶面中央辐条状圆口，一侧竖着齿轮，圆口里冒出粉红光柱 |
| wowpedia_BTNPowerGenerator-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/f/f3/BTNPowerGenerator-Reforged.png | 254cea5e68fb | 重制版图标（对照，**不照搬**）：圆桶底座顶着一块红色大水晶 |
| wowpedia_Warcraft_III_Reforged_-_Power_Generator.jpg | https://static.wikia.nocookie.net/wowpedia/images/2/24/Warcraft_III_Reforged_-_Power_Generator.jpg（「Mana crystal」页） | b54712b9cb04 | 重制版模型全貌（对照，不照搬）：铁箍木桶式矮圆底座、铆钉、橙色发光栅口，顶面圆形铁栅，一侧机械臂与齿轮，顶上红水晶；重制版加了部落旗和兽角，经典版没有 |
| yt_R-9-0EEl5Nw_maxresdefault.jpg | https://i.ytimg.com/vi/R-9-0EEl5Nw/maxresdefault.jpg（「Clockwerk double luck/skill :D Power cog abuse」https://www.youtube.com/watch?v=R-9-0EEl5Nw） | 611a610ffb9e | **DotA 1 游戏内，最清楚的一张**：8 个齿轮排成 **3×3 方阵、中间空一格**，发条（Rattletrap）在正中；每个齿轮是一团粉红 / 洋红的光，底下暗色圆座 |
| yt_R-9-0EEl5Nw_hq1.jpg | https://i.ytimg.com/vi/R-9-0EEl5Nw/hq1.jpg（同上） | 1e8c81d44508 | 近处放大：圆形铜褐底座、底座边一圈花纹，顶上粉红光团 |
| yt_R-9-0EEl5Nw_hq2.jpg | https://i.ytimg.com/vi/R-9-0EEl5Nw/hq2.jpg（同上） | 4100e0b47c21 | 同一方阵另一时刻：底排三个能看出矮圆的铜褐底座，顶上粉红光，桩高大约到英雄胸口 |
| yt_S2yO3ISRUpY_hq1.jpg | https://i.ytimg.com/vi/S2yO3ISRUpY/hq1.jpg（「DOTA CLOCKWERK FIRST BLOOD! – THE TRAP MASTER, NO ONE ESCAPES!」https://www.youtube.com/watch?v=S2yO3ISRUpY） | f1958df3a9a4 | 刚落地：3×3 方阵，每个齿轮冒出一大团洋红光，并向上射出细长的粉红光柱 |
| yt_S2yO3ISRUpY_hq2.jpg | https://i.ytimg.com/vi/S2yO3ISRUpY/hq2.jpg（同上） | 75b187e84e22 | 同上，困住一个敌人；光柱粉红偏红 |
| yt_93Y9DqJYMb8_hq2.jpg | https://i.ytimg.com/vi/93Y9DqJYMb8/hq2.jpg（「Power cog autoattack」https://www.youtube.com/watch?v=93Y9DqJYMb8） | 3bfdc8bcbfed | 又一局：方阵、洋红光团、向上的红色光柱 |
| yt_gGRcJXaIpQQ_hq3.jpg | https://i.ytimg.com/vi/gGRcJXaIpQQ/hq3.jpg（「DOTA ENCHANTRESS RAMPAGEEEE! (625 ATTACK DAMAGE)」https://www.youtube.com/watch?v=gGRcJXaIpQQ） | b7bf62e8df3b | 选中一个齿轮，界面名字 **Power Cog**，头像是粉红光的圆座；场上 3×3 方阵，粉红 |

## 结论（据图）

1. **模型**：WC3「能量发生器」经典模型——**矮胖的圆形发生器**（宽度接近高度），圆鼓 / 圆盘形金属底座，一侧竖着一只齿轮，顶面中央一个辐条状圆口。不是高瘦的齿轮塔，也不是方箱。
2. **主色**：底座暗铜褐 / 铁灰；**能量光是粉红偏洋红**，落地时每个向上射出一道粉红光柱。**不是蓝白电光**。
3. **数量与排布**：**8 个排成 3×3 方阵、中间空一格**，发条站在正中。不是一圈圆。
4. 大小：大约到英雄胸口（缩放 0.75 的建筑）。
5. 重制版的红水晶、部落旗、兽角是重制版重画，经典版没有，不采用。

## 与当前立绘对比（2026-10-21）

旧图 `m111_Power_Cog_v1.png`（sha `51658fb8e408`，2026-10-18）：

- 材质语言（铆钉、铜、铁锈、油污）：一致。
- **形制：不一致**——旧图是高瘦的「方铁箱底座 + 竖立大齿轮 + 顶上铜针」的齿轮塔；原版是矮胖圆鼓发生器，齿轮装在侧面，顶面是辐条圆口。
- **主色：不一致**——旧图是蓝白电火花；原版是粉红 / 洋红的能量光柱。
- **排布：不一致**——旧卡「一圈约 8 个围成圆」；原版是 3×3 方阵（研究文档 d02 §15 也写成「一圈」）。

**差异等级：大**（轮廓、主色两项识别层错）→ 改卡，新立绘待出（出图服务额度不足）。
