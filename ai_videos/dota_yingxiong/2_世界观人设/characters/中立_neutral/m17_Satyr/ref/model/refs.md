# m17 萨特窃魂者 · 原版模型参考（WC3 中立野怪 Satyr，模型 `Satyr`；变体 `SatyrTrickster`、`satyrhellcaller`）

> 暴雪娱乐 / Wowpedia 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床经其 MediaWiki API 取地址，加 `&format=original` 取原格式。YouTube 只取封面，没下视频。
> DotA 1 的窃魂者用 WC3 基础模型 `Satyr`，诡计师用 `SatyrTrickster`，地狱召唤者用 `satyrhellcaller`（缩放 1–1.8，粉、黄等染色，分卷没有逐个变体列出，d01 §5.2），所以 WC3 经典版就是本卡标准；重制版只作对照。DotA 1 游戏内能看清萨特的近景截图没找到。
> **游戏里的红 / 蓝色带是队伍色**（角上、肩上的色带随玩家变），不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_SatyrWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/a/a6/SatyrWC3.gif（页面 https://wowpedia.fandom.com/wiki/Satyr_Soulstealer） | 34f74dd404b8 | **经典 `Satyr` 模型动图**：瘦长、佝偻前倾；**全身覆着金黄底深褐虎纹的毛**（上身也是）；头上一对**细长的角向后上方斜伸**（几乎笔直，带色带＝队伍色）；手里一把**长长的骨白色月牙形弯刃**；反关节羊腿、偶蹄；身后一条细尾 |
| wowpedia_Warcraft_III_creep_Satyr_Soulstealer.jpg | https://static.wikia.nocookie.net/wowpedia/images/b/be/Warcraft_III_creep_Satyr_Soulstealer.jpg（同页） | c3d403ca9003 | 经典版游戏内截图：右侧选中的窃魂者是同模型染**赤褐色**，同样一身深色条纹毛、细长后掠的角、手里月牙弯刃；左边紫色的是诡计师 |
| wowpedia_Warcraft_III_creep_Satyr.jpg | https://static.wikia.nocookie.net/wowpedia/images/7/72/Warcraft_III_creep_Satyr.jpg（页面 https://wowpedia.fandom.com/wiki/Satyr_(Warcraft_III)） | 7aea7cd872e4 | 经典版游戏内：金黄条纹的基础萨特（选中）+ 紫色诡计师 + 赤褐窃魂者同框 |
| wowpedia_BTNSatyr.png | https://static.wikia.nocookie.net/wowpedia/images/a/a8/BTNSatyr.png（同页） | e26d06bcb3f2 | 经典图标：金黄底黑条纹的长鬃脸，黄眼发亮，獠牙 |
| wowpedia_Wc3r_satyr_soulstealer_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/1/1f/Wc3r_satyr_soulstealer_portrait.png（同页） | 80aebcf75f0c | 窃魂者头像：赤红褐皮肤、**两只长尖耳向两侧伸出**、橙褐长发、长胡须、黄眼；头顶后掠的角 |
| wowpedia_BTNSatyrSoulStealer.png | https://static.wikia.nocookie.net/wowpedia/images/c/c6/BTNSatyrSoulStealer.png（同页） | e01edb3ec07f | 重制版图标（对照）：红皮、橙长发、发光黄眼 |
| wowpedia_BTNSatyrTrickster.png | https://static.wikia.nocookie.net/wowpedia/images/1/10/BTNSatyrTrickster.png（页面 https://wowpedia.fandom.com/wiki/Satyr_Trickster） | f4dfbe574945 | 诡计师经典图标：紫蓝底黄白条纹 |
| wowpedia_Satyr_trickster.gif | https://static.wikia.nocookie.net/wowpedia/images/5/55/Satyr_trickster.gif（同页） | c1f23d59721e | 诡计师动图：紫色条纹毛、细长后掠角、手持月牙弯刃 |
| wowpedia_Warcraft_III_creep_Satyr_Trickster.jpg | https://static.wikia.nocookie.net/wowpedia/images/e/e9/Warcraft_III_creep_Satyr_Trickster.jpg（同页） | 02873008a23e | 诡计师游戏内截图 |
| wowpedia_BTNSatyrHellCaller.png | https://static.wikia.nocookie.net/wowpedia/images/c/c9/BTNSatyrHellCaller.png（页面 https://wowpedia.fandom.com/wiki/Satyr_Hellcaller） | c6d48126838c | 重制版图标（对照）：灰紫皮、白长鬃、发光眼 |
| wowpedia_Warcraft_III_creep_Satyr_Hellcaller.jpg | https://static.wikia.nocookie.net/wowpedia/images/7/7e/Warcraft_III_creep_Satyr_Hellcaller.jpg（同页） | 1733df6a8246 | 地狱召唤者游戏内截图：金黄条纹、体型更大 |
| yt_l2BeLWPBUPY_maxresdefault.jpg | https://i.ytimg.com/vi/l2BeLWPBUPY/maxresdefault.jpg（「Satyr HellCaller vs Centaur Khan The Battle of Forest」https://www.youtube.com/watch?v=l2BeLWPBUPY 的封面） | 0afff1d2eaee | **经典模型大图（左，地狱召唤者）**：金黄底深褐虎纹毛、一大蓬披到背上的长鬃；**两根细长的角从额头笔直向后伸出、长过头部两倍**（蓝色带＝队伍色）；反关节腿 |
| yt_Xr3ZIuBwnYY_maxresdefault.jpg | https://i.ytimg.com/vi/Xr3ZIuBwnYY/maxresdefault.jpg（「Satyr Hellcaller vs Elder Wildkin Full items Who Will WIN?」https://www.youtube.com/watch?v=Xr3ZIuBwnYY 的封面） | 49f36eab62c6 | 同上，另一角度 |
| compare_classic_crops.png | 本地拼图（游戏内三种萨特放大 + 地狱召唤者放大 + 动图逐帧） | f01a49ed5056 | 出图验收对照用 |

## 结论（据图）

1. **种族 / 体型**：半羊人，瘦长、佝偻前倾，反关节山羊腿、偶蹄，身后一条细尾（旧卡「羊腿偶蹄」对）。
2. **毛色（主色）**：**全身（连上身）覆着短密的毛，底色上一道道深褐虎纹般的横条纹**；基础模型金黄底，窃魂者在 WC3 里染赤褐，诡计师紫色，地狱召唤者金黄。DotA 各变体的具体染色分卷未载 ⚠️；本卡窃魂者取赭黄偏赤褐。不是光滑的人类上身。
3. **角（第一识别点）**：一对**细长、几乎笔直的角从额头向后上方斜伸**，长过头部两倍，像羚羊角；不是盘卷的公羊角。
4. **头**：长尖耳向两侧伸出；一大蓬长鬃发从头顶披到背上；长须；黄眼。
5. **武器**：手里一把**长长的月牙形弯刃**（刃长约一臂，骨白 / 钢灰），不是短镰。
6. **装束**：几乎没有衣物，只有腰间一小块兽皮。

## 与当前立绘对比（2026-10-21）

当前立绘 `m17_Satyr.png`（sha `c0b477d6219f`，2026-10-18 出，改名留档为 `m17_Satyr_v1.png`）：

- ✅ 半羊人、反关节羊腿偶蹄、尖耳、山羊胡、黄眼、手持弯刃。
- ❌ 角：一对盘卷的公羊角；原版是细长笔直、向后斜伸的长角——头部第一识别点不对。
- ❌ 毛色：光滑的人类上身 + 下身褐毛；原版全身金黄 / 赤褐底深色虎纹毛。
- ⚠️ 武器：短镰；原版是一臂长的月牙弯刃（同类，形制偏小）。
- ⚠️ 骨珠串、皮护腕、腰挂皮囊：原版没有（小）。

**差异等级：大**（角形与全身条纹毛两项识别层不对）→ 改卡，待出图（出图服务额度不足）。
