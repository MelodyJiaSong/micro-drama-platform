# c91 闪电幽魂 · 原版模型参考（WC3 野怪「亡魂」系 `units\creeps\Revenant\Revenant`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `?format=original` 取原格式。YouTube 只取封面与自动截帧，没下视频。
> **游戏里的红色披风 / 布块是队伍色**（随玩家变），不是角色本色；脚下的蓝白光团是模型自带的。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero86_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/86/character.gif（PlayDotA 闪电幽魂页 https://web.archive.org/web/2012id_/http://www.playdota.com/heroes/lightning-revenant） | ee84d32e6c46 | **DotA 1 里的闪电幽魂本体**（120 px 动图）：高瘦的悬浮铠甲身影；头顶一顶尖高的骨金色头盔；左臂一面几乎和身体一样长的黑色鸢形大盾，骨金色边框；右手举一根长杖头的锤 / 权杖；身后红披风（队伍色）；**下身没有腿，末端是一团蓝白色光** |
| playdota_hero86_icon.gif | 同上 `/hero/86/icon.gif` | ae9636c193d3 | DotA 1 头像：骨金色尖顶头盔正面，面罩黑洞里两团发亮的蓝色眼光 |
| wowpedia_BTNRevenant.png | https://static.wikia.nocookie.net/wowpedia/images/7/7b/BTNRevenant.png（页面 https://wowpedia.fandom.com/wiki/Lightning_Revenant_(Warcraft_III)） | caa75188c987 | 经典图标，与 DotA 头像同一张 |
| wowpedia_Revenant.gif | https://static.wikia.nocookie.net/wowpedia/images/d/d5/Revenant.gif | e6bada47f339 | **经典模型动图，最重要的一张**：同上——尖顶头盔两侧横伸一对角翼；骨金色的甲架；左臂黑色鸢形大盾（盾面有骨金色十字形肋）；右手长柄权杖锤高举；红布（队伍色）从肩后垂下；下身是一团蓝光，悬浮不着地 |
| wowpedia_Wc3r_lightning_revenant_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/e/ee/Wc3r_lightning_revenant_portrait.png | 1bd11204fc4e | 重制版肖像（对照，不照搬）：金色尖顶盔 |
| wowpedia_BTNLightningRevenant.png | https://static.wikia.nocookie.net/wowpedia/images/3/31/BTNLightningRevenant.png | 9551d6b60746 | 重制版图标（对照）：金色尖盔、黄色电光 |
| wowpedia_BTNDeathRevenant.png | https://static.wikia.nocookie.net/wowpedia/images/c/ce/BTNDeathRevenant.png | 15e553b1df07 | 同系「死亡亡魂」重制版图标（对照：同一顶尖盔） |
| yt_elS5SLToVR4_maxresdefault.jpg | https://i.ytimg.com/vi/elS5SLToVR4/maxresdefault.jpg（「Razor - Lightning Revenant」https://www.youtube.com/watch?v=elS5SLToVR4） | 64da0647d2f4 | 重制版（Reforged HD）渲染的同一模型（对照结构，**不照它的材质**）：尖盔、肩上骷髅、巨大的鸢形盾、长柄权杖、下身破布条 |
| yt_WJXvaM6OQzU_maxresdefault.jpg | https://i.ytimg.com/vi/WJXvaM6OQzU/maxresdefault.jpg（「(BEYOND GODLIKE) Razor - Lightning Revenant」） | 7ca92997d34a | 同上重制版渲染（对照） |
| yt_6LFues8lg0s_hq2.jpg | https://i.ytimg.com/vi/6LFues8lg0s/hq2.jpg（「Dota Allstars Razor - The Lightning Revenant」） | a730b78856e7 | DotA 1 游戏远景：放电链 |
| compare_classic_crops.png | 本地拼图（经典动图 4 帧 + PlayDotA 4 帧 + 经典图标） | 132780a176d3 | 出图验收对照用 |

## 结论（据图）

1. **形体**：高瘦的悬浮铠甲身影，**没有腿**——腰以下的甲裙收窄，末端是一团冷蓝白色的光，离地漂着。
2. **头盔（第一识别点）**：一顶尖高的骨金色头盔，盔顶一道竖脊，两侧横伸一对角翼；面罩是黑洞，里面两团发亮的冰蓝色眼光。看不到脸。
3. **甲**：骨金 / 旧金色的甲架包着深色甲片，整体是金＋黑；不是锈灰色铁甲，也不是半透明。
4. **盾（左臂）**：一面几乎和身体一样长的黑色鸢形大盾，骨金色边框和十字形肋。
5. **武器（右手）**：一根长柄权杖锤，杖头是尖头的金属锤冠，常态高举。不是剑。
6. **披风**：肩后垂下的布在游戏里是红色（队伍色）。
7. 电光是技能特效，不是常态。

## 与当前立绘对比（2026-10-21）

当前图：`c91_Lightning_Revenant.png`（sha `0b723d5b47ea`，2026-10-18 出）。

- ✅ 悬浮、下身虚化不着地、头盔面罩里两团冰蓝鬼火。
- ❌ **武器错**：一柄长剑；原版是长柄权杖锤。
- ❌ **缺大盾**：原版左臂那面和身体一样长的黑色鸢形盾是正面轮廓里最大的一块。
- ❌ 头盔是圆顶骑士盔；原版是尖高带竖脊、两侧角翼的尖盔。
- ❌ 甲是锈灰色铁甲、半透明；原版骨金＋黑、实体。
- ❌ 全身缠绕常驻电弧；原版常态没有。

**差异等级：大**（武器类型错、最显眼附加物（大盾）缺、主色错）→ 改卡重出。

## 重出结果（2026-10-21）

卡已按上面结论改好，旧图改名 `c91_Lightning_Revenant_v1.png`；`tools/gen_char_images.py run --only c91` 时 ElevenLabs 回 quota_exceeded（剩 93 credits），自动换 Codex 后断网（DNS 解析 api.openai.com 失败）超时，request_id `3b65802423ee4f5aa7ab8434d4bc6e83` 结果未知、未拿到图，按规定未重提。**新立绘待出、待验收。**
