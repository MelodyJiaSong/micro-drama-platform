# m212 死亡守卫 · 原版模型参考（WC3 兽人巫医「静止图腾 / 静止陷阱守卫」`units\orc\StasisTotem\StasisTotem`）

> 暴雪娱乐 / DotA 地图作者等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式；YouTube 只取封面与自动截帧（`hq1/2/3`＝视频约 25% / 50% / 75% 处），没下视频。
> **游戏里纯色块可能是队伍色**（随玩家变）；这根守卫桩的红橙黄是彩绘本色（中立 / 不同玩家截图里都一样），不是队伍色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Stasis_Trap.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/6f/Stasis_Trap.jpg（页面 https://wowpedia.fandom.com/wiki/Stasis_Trap_Ward_(Warcraft_III)） | 07b0d9df0d38 | **经典模型游戏内近景，最重要的一张**：一根比单位略矮的木桩。从上到下：一对向两侧弯起的白色兽角，两角之间一团橙黄白的火焰；一块长方形木牌，红底、黄橙三角折纹、黑描边；一圈黑色羽毛 / 毛束；一张红褐色鬼脸，白底紫瞳的鼓眼、方齿大嘴、嘴角两根向外弯翘的白獠牙；脸下木桩带刻环，往下收成尖桩 |
| wowpedia_Stasis_Trap2.jpg | https://static.wikia.nocookie.net/wowpedia/images/0/00/Stasis_Trap2.jpg（同页） | 896aaa6b9b5e | WC3 对战截图：雪地上一根小木桩，顶端发白光；左下 UI 头像是同一根桩（顶上火、红牌、獠牙脸），名称 Stasis Trap |
| wowpedia_BTNStasisTrap.png | https://static.wikia.nocookie.net/wowpedia/images/3/38/BTNStasisTrap.png（同页） | a38622c53a2c | 经典图标：红橙火焰底上一道折线符号，两边白獠牙，看不出整体造型 |
| wowpedia_BTNStasisTrap-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/4/40/BTNStasisTrap-Reforged.png（同页） | ac867f6b8886 | 重制版图标（对照，**不照搬**）：同一设计更清楚——黄框红底三角纹木牌、红褐木雕脸、白圆眼、方齿、一圈蓝羽毛（重制版加的） |
| yt_G1yjhFSbofc_maxresdefault.jpg | https://i.ytimg.com/vi/G1yjhFSbofc/maxresdefault.jpg（「Vol'jin - Witch Doctor se defiende con el Death Ward - Dota 1」https://www.youtube.com/watch?v=G1yjhFSbofc） | 85daf2291342 | **DotA 1 游戏内**（地图 v7.03b2，DotA 1 社区后续版）：画面中部一根小木桩顶上烧着橙黄火焰，周围一圈白色小石（施法圈）；远距离俯视下读得出的是「顶上一团火的木桩」 |
| yt_4okFAWnONkI_hq2.jpg | https://i.ytimg.com/vi/4okFAWnONkI/hq2.jpg（「Witch Doctor/Vol'Jin \| DOTA/Defense of the Ancients 1 \| Frozen Throne」https://www.youtube.com/watch?v=4okFAWnONkI） | 900181d56551 | DotA 6.83d AI 图：巫医大招时地上一团绿光、向上一道绿色光柱打向敌方英雄（疑为死亡守卫攻击或施法圈；画面太小，守卫本体看不清）⚠️ |

## 结论（据图）

1. **不是骷髅图腾**：没有兽头骨 / 骷髅。是一根**彩绘木雕守卫桩**，约一个单位高（真人化取约 1.8 米，与巫医差不多）。
2. **顶部**：一对向两侧弯起的白色兽角，**两角之间烧着一团橙黄火焰**——DotA 1 远景里认得出的就是这团火。
3. **木牌**：角下一块长方形木牌，红底、黄橙三角折纹、黑描边（部族彩绘）。
4. **羽毛领**：木牌下一圈黑色羽毛 / 毛束。
5. **鬼脸**：红褐色木雕脸，白底紫瞳的鼓眼，咧开的方齿大嘴，嘴角两根**向外弯翘的白獠牙**（巨魔獠牙）。
6. **下端**：脸以下带刻环的木桩，往下收细成尖桩，扎在地里；上宽下尖。
7. **主色**：红、赭橙、黄、黑彩绘 + 白角白牙 + 橙黄火；不是发黑焦木。
8. 攻击投射物外观没截到清楚画面 ⚠️（卡里暗绿鬼火弹仍是创作）。

## 与当前立绘对比（2026-10-21）

当前立绘 `m212_Death_Ward_v1.png`（2026-10-18，sha `a713fac8a371`）：

- ❌ 顶部：一颗巨大兽头骨、眼窝发绿光；原版是一对白角夹着一团火，没有头骨。
- ❌ 主色：通体发黑焦木 + 红黑羽毛；原版是红橙黄黑彩绘（卡里负向还禁了「彩绘」「鲜艳油漆」「红色火焰」，正好与原版相反）。
- ❌ 鬼脸：三张叠着的黑木狰狞脸；原版只有一张红褐鬼脸，嘴角两根外翘白獠牙。
- ❌ 没有彩绘三角纹木牌；轮廓是粗底柱子，原版是上宽下尖的尖桩。
- ✅ 部族巫术木雕、羽毛、獠牙元素、不会动——这些方向对。
- 真人化（真木真骨、褪色颜料）不算差异。

**差异等级：大**（顶部附加物、主色、轮廓三项都错，老玩家认不出是那根「顶上冒火的小木桩」）→ 已改卡，新立绘待出（出图服务额度不足）。
