# c103 术士 · 原版模型参考（WC3 兽人「古尔丹」`units\orc\OrcWarlockGuldan\OrcWarlockGuldan`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式。YouTube 只取封面与自动截帧，没下视频。
> **队伍色提醒**：肩上那圈大红披领在 PlayDotA 动图和 Wowpedia 渲染里都是红色（两图都按红方玩家渲染），按惯例判为队伍色 ⚠️；经典图标里同位置是灰白，不是红。

| 文件 | 来源 URL（含所在页面）| sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero58_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/58/character.gif（PlayDotA 英雄页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/warlock） | 557f108fe84c | **DotA 1 本体动图**（小）：驼背；黑袍上大片**金黄色锯齿纹**，白色下摆；肩上一圈红领（队伍色）；**背后竖起两三根木杆，杆顶各插一颗白骷髅**；手里一根红黑相间的长杖 |
| playdota_hero58_character_frame.png | 上图第 0 帧与中间帧放大 3 倍（本地） | c7eb5016d536 | 看图用 |
| playdota_hero58_icon.jpg | 同上 `/hero/58/icon.jpg` | fbf4f0c4d0d3 | DotA 1 头像（`BTNGuldan`）：亮绿皮兽人、白色下獠牙、浓眉；黑兜帽**镶金黄边**，帽沿两侧灰白 |
| wowpedia_BTNGuldan.png | https://static.wikia.nocookie.net/wowpedia/images/f/fa/BTNGuldan.png（页面 https://wowpedia.fandom.com/wiki/Gul'dan_(Warcraft_III)） | 04bfcdfb8ed8 | 同上经典图标 |
| wowpedia_Guldanwiki2.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/12/Guldanwiki2.jpg（同页信息框图） | 2ff497b85164 | **经典模型渲染（最重要）**：亮绿脸、白下獠牙，**灰白长须编成两股垂到胸前**；黑兜帽镶金边；黑长袍前襟和下摆是**金黄色锯齿 / 部落纹**，下身是灰白布裙；一侧肩甲伸出一根长钢刺；**背上三根木杆各顶一颗白骷髅**，高出头顶；右手长杖**红黑螺旋缠绕**，杖头是一颗带角的白骷髅 |
| wowpedia_BTNGuldan-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/7/73/BTNGuldan-Reforged.png | 055a3d8baa66 | 重制版图标（对照，**不照搬**）：老皱绿皮、红眼、獠牙挂环、紫红破兜帽 |
| wowpedia_GuldanReforged.png | https://static.wikia.nocookie.net/wowpedia/images/9/96/GuldanReforged.png | 8cd8311c00b6 | 重制版模型（对照）：背上一排长骨刺 / 枝杈，暗袍红布，骷髅长杖——「背负尖杆」的轮廓与经典版一致 |
| yt_thDp8z2y3Jk_hq2.jpg | https://i.ytimg.com/vi/thDp8z2y3Jk/hq2.jpg（「Dota 1 Warlock (Demnok Lannik)! 1 vs 5 AI」https://www.youtube.com/watch?v=thDp8z2y3Jk） | dd2bc08f46dd | DotA 1 游戏界面：名字 Demnok Lannik / Warlock，头像为亮绿兽人脸，游戏内是小小的黑金身影 |
| compare_classic_crops.png | 本地拼图（经典模型渲染 + 经典图标的放大裁切） | 225c66f3c8de | 出图验收对照用 |

Wowpedia 词条说明：古尔丹单位只在过场出现，音效集借深渊领主；重制版把尖刺改成从身体长出，经典版的尖刺是挂在衣服 / 背架上的（与图一致）。

## 结论（据图）

1. **种族与脸**：亮绿皮老兽人，白色下獠牙，**灰白长须编成两股**垂到胸前；兜帽下露脸。
2. **兜帽与袍（主色）**：黑兜帽**镶金黄边**；黑长袍上大片**金黄锯齿 / 部落纹**；下身是灰白布裙，下摆也有金黄纹。旧卡「深紫黑粗羊毛兜袍、无金饰」错——主色是**黑 + 金黄**。
3. **背上（最显眼附加物）**：背后竖着**三根木杆，每根杆顶插一颗白骷髅**，高出头顶。旧卡写成「肩背一排骨刺」，形制不对。
4. **肩**：一侧肩甲伸出一根长钢刺；肩上一圈大披领（游戏里红色，判为队伍色 ⚠️）。
5. **法杖**：长杖杖身**红黑螺旋缠绕**，杖头是一颗**带角的白骷髅**。
6. **体型**：驼背、肩背宽厚；缩放 1.5，比小兵高大。
7. 绿色邪火：经典图里看不到手上 / 杖头常驻绿火（技能特效另算），本剧作为创作保留在左掌一小团 ⚠️。

## 与当前立绘对比（2026-10-21）

- 一致：绿皮老兽人、獠牙、灰白长须、驼背、兜帽、骷髅头长杖、腰挂骨饰。
- 不一致：① 袍子是**深紫黑破布、无金边**，原版是**黑袍 + 大片金黄锯齿纹 + 灰白下裙**（服装主色错）；② 背上没有**三根顶骷髅的木杆**，只有帽沿、肩上一圈小弯刺（最显眼附加物错）；③ 法杖是自然黑木，原版**红黑螺旋**、杖头带角骷髅；④ 胡须没有编成两股。
- **差异等级：大**（服装主色与背上骷髅杆两项识别层错，远看轮廓不同）。
