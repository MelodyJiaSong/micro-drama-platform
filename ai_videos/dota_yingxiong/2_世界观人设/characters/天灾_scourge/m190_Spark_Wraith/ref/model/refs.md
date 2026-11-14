# m190 闪光怨灵 · 原版模型参考（DotA 地图导入模型 `war3mapImported\StaticStorm_9`，WC3 原版没有）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。YouTube 只取封面与自动截帧（`hq1/2/3`＝视频约 25% / 50% / 75% 处），没下视频。
> **游戏里的红/蓝等纯色块常是队伍色**（随玩家变），不是角色本色。本模型是地图导入模型，只能靠 DotA 1 技能图标与游戏截图；游戏里它是地上一个小光团，**没找到能确认「这一团就是闪光怨灵」的清楚特写**，结论可信度中等。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero141_skill-2.jpg | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/141/skill-2.jpg（PlayDotA 弧光守望者页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/arc-warden，「闪光怨灵 Spark Wraith」） | b89a29f04459 | **DotA 1 闪光怨灵图标**：一团**深紫 / 紫罗兰色的旋涡状光球**，中心一道白紫色的闪电纹 |
| playdota_hero141_skill-0.jpg | 同上 `/hero/141/skill-0.jpg`（「乱流 Flux」） | 78407b7714f2 | 对照：同一英雄的乱流图标，**紫白色电光**缠着一个人影 |
| playdota_hero141_skill-1.jpg | 同上 `/hero/141/skill-1.jpg`（「磁场 Magnetic Field」） | 63096620d095 | 对照：紫色旋涡。整个英雄的电系颜色语言是**紫 / 紫白** |
| yt_PPH-sWDsPt4_hq3.jpg | https://i.ytimg.com/vi/PPH-sWDsPt4/hq3.jpg（「DOTA 1 Arc Warden Zet Beyond GODLIKE #16」https://www.youtube.com/watch?v=PPH-sWDsPt4） | c065a10da4a7 | DotA 1 游戏内：地上一大团**紫罗兰色发光的电光团**（可能是闪光怨灵，也可能是乱流打在单位上，分不清 ⚠️） |
| yt_PPH-sWDsPt4_hq2.jpg | https://i.ytimg.com/vi/PPH-sWDsPt4/hq2.jpg（同上视频） | f2326ce095cb | DotA 1 游戏内：地面上几个小的紫色光团 |
| yt_mZrO7YowB84_hq3.jpg | https://i.ytimg.com/vi/mZrO7YowB84/hq3.jpg（「Dota zet arc warden gameplay」https://www.youtube.com/watch?v=mZrO7YowB84） | f82b6e95b399 | DotA 1 游戏内：紫色光圈里打出一道青白电光（技能特效整体是紫 + 青白） |

另：已复核的 `c92_Arc_Warden/ref/model/refs.md` 记下 DotA 1 弧光守望者杖头吊着「紫白电光球」，与本卡同一颜色语言。

## 结论（据图）

1. **颜色**：DotA 1 里弧光守望者的电系技能是**紫罗兰 / 紫白色**电光；闪光怨灵图标是一团深紫旋涡状光球、中心白紫闪电。**不是蓝白色**。
2. **形状**：一团旋转的电光球（旋涡状），无脸无手脚——与旧卡一致。
3. 大小、悬停高度：图上看不出，沿用旧卡（创作）。

## 与当前立绘对比（2026-10-21）

对比 `m190_Spark_Wraith_v1.png`（旧图，sha `63d506debe60`）：

- 一致：一团悬空电浆球、球心刺眼、外层缠绕细电弧、向地面打火花、无生物特征。
- 不一致：**主色蓝白**，原版是紫罗兰 / 紫白（旧卡负向还写了「紫色电光」，正好把原版颜色排除了）。
- 小差异：原版图标是旋涡状，旧图更像一团乱电弧。

**差异等级：大**（主色错）→ 改卡、待出图（出图服务额度不足，follow-up 057 暂停出图）。可信度中等：颜色依据是 DotA 1 技能图标与同英雄技能的颜色语言，出图前若能补到游戏特写再核对一次。
