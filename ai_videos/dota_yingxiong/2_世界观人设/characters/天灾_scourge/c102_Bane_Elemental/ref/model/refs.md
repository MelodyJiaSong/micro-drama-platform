# c102 祸乱之源 · 原版模型参考（WC3 野怪「虚空行者」`units\creeps\VoidWalker\VoidWalker`）

> 暴雪娱乐 / PlayDotA 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床加 `&format=original` 取原格式。YouTube 只取封面，没下视频。
> **队伍色提醒**：虚空行者模型几乎没有队伍色面积；地面上的彩色光圈是选取圈，不是角色本色。

| 文件 | 来源 URL（含所在页面）| sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| playdota_hero27_character.gif | https://web.archive.org/web/2013id_/http://media.playdota.com/hero/27/character.gif（PlayDotA 英雄页 https://web.archive.org/web/2013id_/http://www.playdota.com/heroes/bane-elemental） | bd529a311c59 | **DotA 1 本体动图**：一团紫罗兰色光晕里的暗紫黑身体，身上是一片片**棱角分明的尖晶片**，头顶、背上向上竖起几根尖刺；下身是一团亮紫雾，没有腿 |
| playdota_hero27_character_frame.png | 上图第 0 帧与中间帧放大 3 倍（本地） | a809b370498f | 看图用 |
| playdota_hero27_icon.jpg | 同上 `/hero/27/icon.jpg` | 172b126003e5 | DotA 1 头像（`BTNVoidWalker`）：紫与粉紫交错的棱面，中间一张尖头的暗脸、两点亮紫眼 |
| wowpedia_BTNVoidWalker.png | https://static.wikia.nocookie.net/wowpedia/images/a/ab/BTNVoidWalker.png（页面 https://wowpedia.fandom.com/wiki/Voidwalker_(Warcraft_III)） | 7dca040d5aac | 同上经典图标 |
| wowpedia_VoidwalkerWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/c/c8/VoidwalkerWC3.gif（同页） | f305e7c9dc0d | WC3 经典模型动图：与 DotA 动图同一造型——紫光包裹的尖晶片身体、长而带尖的爪臂、头顶尖刺 |
| wowpedia_WC3_creep_Voidwalker.jpg | https://static.wikia.nocookie.net/wowpedia/images/0/03/Warcraft_III_creep_Voidwalker.jpg（同页） | bf12eccf3f4f | 游戏内俯视：三只虚空行者是**蓝紫色、刺棱棱的发光团**，远看读得出的是「紫光 + 尖刺」 |
| wowpedia_BTNVoidWalker-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/8/82/BTNVoidWalker-Reforged.png | 5f7118fe404f | 重制版图标（对照，**不照搬**）：圆胖的蓝紫雾体、粉紫眼 |
| wowpedia_Wc3r_voidwalker_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/3/3b/Wc3r_voidwalker_portrait.png | 3202e976a8d0 | 重制版肖像（对照，**不照搬**）：蓝灰色平滑团块脸 |
| yt_4KE6QoCbo08_maxresdefault.jpg | https://i.ytimg.com/vi/4KE6QoCbo08/maxresdefault.jpg（「DOTA 1 HOW TO PLAY BANE LIKE A PRO!」https://www.youtube.com/watch?v=4KE6QoCbo08） | bb5f0515b00e | **经典模型近景（最重要）**：暗紫黑的**尖晶甲片**拼成的身体，片与片之间透出亮紫光；头是一个向上收尖的**铲形尖头**，脸是两道斜吊的亮紫眼光；肩背上几根高高的尖刺；两条长臂末端是**一把把尖晶长爪**；下身收成一根带锯齿的尖尾，悬空 |
| yt_3ysnlysPILY_maxresdefault.jpg | https://i.ytimg.com/vi/3ysnlysPILY/maxresdefault.jpg（「Dota 1 - Atropos (Bane Elemental)! 1 vs 5 AI」） | ae63724e4575 | DotA 1 游戏内：紫色发光的身体、伸出暗色爪臂，下方是紫雾；左下头像是紫团 |
| compare_classic_crops.png | 本地拼图（经典模型近景 + PlayDotA 动图帧的放大裁切） | c256ccbf70f8 | 出图验收对照用 |

## 结论（据图）

1. **形态**：悬浮、没有腿的虚空生物；粗壮上身、两条长臂，下身收成一根尖尾 / 一团紫雾。
2. **质感（识别点）**：身体是**一片片棱角分明的暗紫黑尖晶甲片**拼成的，片缝里透出亮紫罗兰色的光，整体包在一层紫光晕里；不是平滑的雾质肌肉。
3. **轮廓（识别点）**：头是向上收尖的铲形尖头；肩、背向上竖着几根长尖刺；手是尖晶长爪。整体是「刺棱棱」的轮廓。
4. **颜色**：暗紫黑 + 亮紫罗兰光；**没有黄绿色**。d07 的「染色 G 缺省」在游戏画面里看不出偏绿。
5. **眼**：两道斜吊的亮紫 / 粉紫眼光。
6. **没有「漂浮星点」**：原图看不到冷白星点，那是旧卡推测。

## 与当前立绘对比（2026-10-21）

- 一致：悬浮无腿、粗壮上身、两条长臂大手、紫色主体。
- 不一致：① 当前是**平滑的雾质肌肉巨猿**，原版是**尖晶甲片 + 片缝紫光**（材质识别错）；② 没有尖铲形头、没有肩背尖刺（轮廓错）；③ 边缘泛**黄绿光**，原版没有；④ 手是肉质大手，原版是尖晶长爪；⑤ 身周星点原版没有。
- **差异等级：大**（轮廓与材质两项识别层都错，老玩家第一眼不会认成祸乱之源）。
