# m15 泥土傀儡 · 原版模型参考（WC3 中立野怪 Rock Golem / Mud Golem，模型 `units\creeps\RockGolem`）

> 暴雪娱乐 / Wowpedia 等版权素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 follow-up 057 下载（免费公开页面，未调用收费服务）。Wowpedia 图床经其 MediaWiki API 取地址，加 `&format=original` 取原格式。YouTube 只取封面，没下视频。
> DotA 1 的泥土傀儡用 WC3 模型 `RockGolem`（缩放 1.2，**染成褐色 150/110/70**，d01 §5.2）；WC3 里同名野怪 Mud Golem 也是同模型染褐，正好对照。与 `m22` 岩石傀儡、`m7` Roshan 同模型（见 `m22_Rock_Golem/ref/model/refs.md`）。DotA 1 游戏内能看清它的近景截图没找到。
> **游戏里的红色石刺尖端是队伍色**，随玩家变，不是角色本色。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Rockgolem.gif | https://static.wikia.nocookie.net/wowpedia/images/7/77/Rockgolem.gif（页面 https://wowpedia.fandom.com/wiki/Mud_Golem_(Warcraft_III)） | caf7adf0c99a | **经典模型动图（本色）**：大块棱角石头垒成的驼背巨人，两肩是巨大圆石、拳头是两块巨石垂到膝下，小头陷在肩间；**脸上一道发黄光的缝**；肩背几根尖刺（尖端红＝队伍色） |
| wowpedia_Rock_Golem.jpg | https://static.wikia.nocookie.net/wowpedia/images/4/4a/Rock_Golem.jpg（页面 https://wowpedia.fandom.com/wiki/Rock_Golem） | 6ea9714e067b | 经典模型游戏内近景：灰褐石块、巨石拳、小头陷肩、眼嘴一道黄光缝 |
| wowpedia_Warcraft_III_creep_Mud_Golem.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/1d/Warcraft_III_creep_Mud_Golem.jpg（Mud Golem 页） | 502fea42a54c | **经典版游戏内两只 Mud Golem（褐色）**：同骨架，整只褐色石块 |
| yt_kDMrV35PyNM_maxresdefault.jpg | https://i.ytimg.com/vi/kDMrV35PyNM/maxresdefault.jpg（「Warcraft 3 Lv02 Creeps 1080p」https://www.youtube.com/watch?v=kDMrV35PyNM 的封面） | bda01a1307dc | 经典版游戏内选中 Mud Golem：褐色块状驼背巨人；头像是褐色石头脸 |
| wowpedia_Wc3r_mud_golem_portrait.png | https://static.wikia.nocookie.net/wowpedia/images/2/26/Wc3r_mud_golem_portrait.png（Mud Golem 页） | 24233fad213a | 头像：土黄褐色的石头脸，**两眼和嘴里透出黄光**，嘴是一条横缝 |
| wowpedia_BTNMudGolem.png | https://static.wikia.nocookie.net/wowpedia/images/b/b0/BTNMudGolem.png（同页） | f5300b744343 | 重制版图标（对照）：土黄褐石脸，眼与嘴里透出熔炉般的黄橙光 |
| wowpedia_BTNRockGolem.png | https://static.wikia.nocookie.net/wowpedia/images/8/82/BTNRockGolem.png（同页） | bbb3d7cb4e55 | 经典图标：灰褐石头脸，眼缝和嘴缝发橙黄光 |
| wowpedia_Mud_golem_wcr.jpg | https://static.wikia.nocookie.net/wowpedia/images/e/ea/Mud_golem_wcr.jpg（同页） | 6ed676bf0bb4 | 重制版模型（对照）：深褐块状石身、嘴缝发黄光，两肩一排白色晶刺 |
| wowpedia_Warcraft_III_creep_Rock_Golem.jpg | https://static.wikia.nocookie.net/wowpedia/images/8/8c/Warcraft_III_creep_Rock_Golem.jpg（Rock Golem 页） | d0b298bbc58d | 灰色本色版游戏内截图（对照） |
| compare_classic_crops.png | 本地拼图（重制版模型 + 经典动图逐帧放大） | 9b705dc00ba8 | 出图验收对照用 |

## 结论（据图）

1. **材质 / 主色**：**褐色石块**垒成的巨人（原模型灰褐石 × 褐色染色 → 土黄褐 / 赭褐砂岩色），块面棱角分明；不是软塌往下淌的湿泥。按 world_rules §1.4 可以在石缝里加干裂的泥，但主体是石块。
2. **轮廓**：驼背，两肩巨大圆石，两条石臂比腿粗、拳头是两块巨石垂到膝下，小头陷在两肩之间，短粗石柱腿（旧卡这条对）。
3. **脸（第一识别点）**：小石头脑袋上，**眼与嘴的位置是透出橙黄光的缝**；不是空洞眼窝。
4. **肩背**：两肩和背上竖着几根尖锐的石刺（尖端是队伍色，不进画面）。
5. 与 `m22` 岩石傀儡同一副骨架，靠尺寸（本卡最小）与褐色区分。

## 与当前立绘对比（2026-10-21）

当前立绘 `m15_Mud_Golem.png`（sha `cd04eef79f26`，2026-10-18 出，改名留档为 `m15_Mud_Golem_v1.png`）：

- ✅ 驼背、长臂垂拳、小头陷肩——轮廓大体对；褐色对。
- ❌ 材质：整只是往下淌的湿泥团，没有石块；原版是棱角分明的褐色石块。
- ❌ 脸：两个黑洞眼眶；原版是透橙黄光的眼嘴缝——头部第一识别点缺失（旧卡负向写了「发光的眼睛」把它排除了）。
- ❌ 肩背石刺：没有。

**差异等级：大**（材质、发光脸缝、肩刺三项识别层不对）→ 改卡，待出图（出图服务额度不足）。
