# m16 食人魔拳手 · 原版模型参考（WC3 中立野怪 Ogre Mauler，模型 `Ogre`；法师变体 `OgreMagi`）

> 暴雪娱乐 / Wowpedia 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床经其 MediaWiki API 取地址，加 `&format=original` 取原格式。YouTube 只取封面，没下视频。
> DotA 1 的拳手用 WC3 模型 `Ogre`（缩放 1.6，偏红）、法师用 `OgreMagi`（缩放 1.55，d01 §5.2），所以 WC3 经典版就是本卡标准；重制版只作对照。DotA 1 游戏内能看清拳手的近景截图没找到。
> **游戏里的红色护肩、腰前垂布是队伍色**，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_OgreWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/d/de/OgreWC3.gif（页面 https://wowpedia.fandom.com/wiki/Ogre_Mauler_(Warcraft_III)） | 2b633203f07a | **经典 `Ogre` 模型动图**：土黄皮肤的胖壮食人魔，**两颗头并排长在肩上**；胸腹一排黑色三角纹；双肩红护肩、腰前红垂布（队伍色）；单手拖一根粗木棒 |
| yt_5w51lKbzGYc_maxresdefault.jpg | https://i.ytimg.com/vi/5w51lKbzGYc/maxresdefault.jpg（「Warcraft 3 Ogre Mauler Quotes」https://www.youtube.com/watch?v=5w51lKbzGYc 的封面） | f7f48222ad91 | **经典模型正面大图，最清楚的一张**：两颗秃头并排、头顶一根短尖角；大肚腩、短粗腿；胸口与肚子上一圈黑色锯齿三角纹；右手握一根头粗尾细的木棒；右下角经典双头图标 |
| wowpedia_Ogre_Mauler_Warcraft_III.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/17/Ogre_Mauler_%28Warcraft_III%29.jpg（同页） | c5b17e77e390 | 经典模型近景：**两颗头，每颗头顶中央一根短尖角**，粗眉小眼、下颚獠牙；粉褐皮肤，胸腹大块黑色三角纹，腰前垂布印骷髅；手拿粗木棒 |
| wowpedia_Ogre_Mauler_portrait.jpg | https://static.wikia.nocookie.net/wowpedia/images/d/d2/Ogre_Mauler_portrait.jpg（同页） | 3b1762b5a519 | 经典头像：两颗头并排，左头顶一根尖角、右头侧脸獠牙 |
| wowpedia_BTNOgre.png | https://static.wikia.nocookie.net/wowpedia/images/5/57/BTNOgre.png（同页） | 0ea6853fa8ec | 经典图标：两颗土黄色的头挤在一起，獠牙外露 |
| wowpedia_Warcraft_III_creep_Ogre_Mauler.jpg | https://static.wikia.nocookie.net/wowpedia/images/0/0c/Warcraft_III_creep_Ogre_Mauler.jpg（同页） | 99e259b74ea3 | 经典版游戏内截图：雪地里一只橙褐色双头拳手 |
| wowpedia_BTNOgreMauler.png | https://static.wikia.nocookie.net/wowpedia/images/2/2c/BTNOgreMauler.png（同页） | a0354b1d886d | 重制版图标（对照）：同样两颗头，一颗戴铁盔 |
| wowpedia_Ogre_mauler_wcr.png | https://static.wikia.nocookie.net/wowpedia/images/3/3e/Ogre_mauler_wcr.png（同页） | a63ec7db090d | 重制版模型（对照，不照搬）：双头、红护肩、铁锤 |
| wowpedia_OgreMageWC3.gif | https://static.wikia.nocookie.net/wowpedia/images/b/b1/OgreMageWC3.gif（页面 https://wowpedia.fandom.com/wiki/Ogre_Magi_(Warcraft_III)） | 30da63cf2a4c | **法师变体 `OgreMagi` 动图**：同样双头，**皮肤是灰蓝 / 冰蓝色**，手持带尖头的法杖 |
| wowpedia_BTNOgreMagi.png | https://static.wikia.nocookie.net/wowpedia/images/e/e6/BTNOgreMagi.png（同页） | d5eac31bb4bd | 法师图标：两颗蓝皮头 |
| wowpedia_Warcraft_III_creep_Ogre_Magi.jpg | https://static.wikia.nocookie.net/wowpedia/images/a/ae/Warcraft_III_creep_Ogre_Magi.jpg（同页） | 423e5c4b6e59 | 法师游戏内截图：蓝皮双头 |
| compare_classic_crops.png | 本地拼图（封面经典模型放大 + 经典近景） | 005b18c7a828 | 出图验收对照用 |

## 结论（据图）

1. **双头（第一识别点）**：拳手本身就是**两颗头并排长在肩上**，不只是法师。分卷「法师是双头」的说法不全（见报告）。
2. **头**：两颗都是大秃头，**头顶中央各一根短而尖的角**；粗眉、小眼、宽鼻，下颚两根上翘獠牙。没有辫子。
3. **体型**：胖壮、大肚腩、厚肩、短粗腿（旧卡对）。
4. **皮肤主色**：原模型土黄 / 粉褐，DotA 染「偏红」→ 红褐 / 赭红褐。
5. **纹饰**：胸口和肚子上一圈**黑色锯齿三角纹**（像一排三角旗）。
6. **装束**：双肩护肩、腰前一块垂布（游戏里是队伍色），按 world_rules §1.4 翻成暗色兽皮。没有铁环腰带。
7. **武器**：一根头粗尾细的粗木棒，单手拖着。
8. **法师（`OgreMagi`）**：同样双头，**灰蓝 / 冰蓝皮肤**，手持带尖头的法杖。

## 与当前立绘对比（2026-10-21）

当前立绘 `m16_Ogre.png`（sha `c56dfbd1d85e`，2026-10-18 出，改名留档为 `m16_Ogre_v1.png`）：

- ✅ 胖壮大肚腩、红褐皮、秃头、獠牙、兽皮腰裙、赤足、带钉大木棒（木棒类型对）。
- ❌ **只有一颗头**；原版两颗头——最显眼的识别特征缺失，旧卡验收还写了「只有一颗头」。
- ❌ 头顶没有短尖角；后脑多了一根粗辫（原版没有）。
- ❌ 胸腹没有黑色三角纹。
- ⚠️ 单边铁护肩 + 斜挎皮带 + 铁环腰带：原版是双肩护肩、腰前垂布（小）。

**差异等级：大**（双头这一识别层缺失）→ 改卡，待出图（出图服务额度不足）。
