# m202 幽冥守卫 · 原版模型参考（WC3「怪物诱饵」`Units\Creeps\MonsterLure`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。
> **游戏里的红/蓝等纯色块常是队伍色**（随玩家变），不是角色本色。
> **原图不足**：只找到 3 张图标，**没有找到 MonsterLure 守卫模型本身的图，也没在 DotA 1 视频截帧里认出幽冥守卫**（Wowpedia / warcraft.wiki.gg 没有该模型的页面图，warcraft.wiki.gg 与 Liquipedia 对本机拒绝访问；查了 9 段 DotA 1 帕格纳视频的封面与自动截帧，守卫太小或不在画面里）。下面的判断只到图标层面。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero13_skill-2.jpg | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/13/skill-2.jpg（PlayDotA 湮灭法师页 https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/oblivion，「幽冥守卫 Nether Ward」） | fd98412a5b9e | **DotA 1 幽冥守卫图标**：一根木棍上顶着一颗白骷髅，骷髅和几根骨头上抹着红色涂痕，背后一圈**绿色辉光** |
| wowpedia_BTNMonsterLure.png | https://static.wikia.nocookie.net/wowpedia/images/3/36/BTNMonsterLure.png（WC3 物品「怪物诱饵」图标） | e3a57c5a20f3 | WC3 原版「怪物诱饵」物品图标：盘子上一大块烤肉 / 火腿 |
| wowpedia_BTNMonsterLure-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/0/03/BTNMonsterLure-Reforged.png | 897ab417d23c | 重制版图标：一大块生肉用麻绳捆在一根木桩 / 木架上，几根木棍横插出来 |

## 结论（据图，可信度低）

1. 模型名「怪物诱饵」与两张物品图标都指向**木桩 / 木架上绑着一大块肉**的诱饵；但图标不等于守卫模型，⚠️ 未核实。
2. DotA 1 的技能图标画的是**木棍顶骷髅、红色涂痕骨头、绿色辉光**——与旧卡「枯木 + 骨片 + 顶端幽绿光」的方向相近。
3. 两种来源互相矛盾，无法据此确定游戏里守卫的识别层。

## 与当前立绘对比（2026-10-21）

对比 `m202_Nether_Ward.png`（sha `4b3ebc15c278`）：

- 与 DotA 1 技能图标相近：木桩、骨头、顶端绿光。
- 与「怪物诱饵」物品图标不符：没有那块用绳子捆在桩上的肉。
- 立绘里骨头上没有红色涂痕，顶上不是骷髅而是一道竖缝里的绿光核。

**差异等级：待定（原图不足，无法判定）**——没有模型图或游戏截图前不改卡。需要一张 DotA 1 游戏里幽冥守卫的清楚截图（或 WC3 模型查看器里 `MonsterLure.mdx` 的渲染）再定。
