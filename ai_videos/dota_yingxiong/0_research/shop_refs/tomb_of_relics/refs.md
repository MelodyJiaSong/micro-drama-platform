# 天灾独有商店 · 崩碎之穴 Tomb of Relics（WC3「遗物陵墓」，模型 `buildings\undead\TombOfRelics`）

> 暴雪娱乐素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 下载（免费公开页面，未调用收费服务）。
> DotA 1 里这家店卖消耗品和信使，对应近卫的奇迹古树（d01 §3.5、d08 §1.1）。经典版（Classic）是标准；本轮 warcraft.wiki.gg 图床整站 502，Reforged / DE 版没能下到，所以这里没有重制版对照图。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| bnet_TombOfRelics_WC3.gif | https://classic.battle.net/war3/images/undead/buildings/tombofrelics.gif（暴雪旧官网亡灵建筑页 https://classic.battle.net/war3/undead/tombofrelics.shtml）；wowpedia 存档里的 `Tomb_of_Relics.gif` 与此逐字节相同 | 788b7efaf4e0 | **经典模型官方渲染（190×211）**，左前方俯视。长方形的石砌陵墓：主体是一口「大石棺」，顶上盖紫色压边的深灰石板坡顶，石板上是蛛网 / 鳞片状的浮雕纹；后半截是一道很高的**筒形拱顶**（像半截水管横躺着），拱面一圈圈铜色箍边、中间深紫灰；屋脊和拱顶交接处排着**一串白骷髅**（四五个）。四个角各立一根**方尖碑式石柱**，柱身是一层层黑石夹铜色横带，柱顶是铜色金字塔尖。底座四周是暗绿石板，边缘冒**亡灵绿光**（荒芜地表的光）。没有招牌、没有文字、没有商人站位——就是一栋建筑 |
| wp_BTNTombOfRelics.png | https://web.archive.org/web/20220627203329im_/https://static.wikia.nocookie.net/wowpedia/images/9/93/BTNTombOfRelics.png/revision/latest?cb=20090112041756（页面 https://web.archive.org/web/20220627203329/https://wowpedia.fandom.com/wiki/Tomb_of_Relics_(Warcraft_III)） | e242ab801896 | 经典图标 64×64：同一栋建筑的近景，左边两根铜尖方尖碑，中间斜着一道**红色**压边的坡顶（图标里压边是红不是紫），右上是铜箍筒形拱。整体黑灰 + 铜色 |
| ytcap_fPeCaVMCx1g_669s_683d_tomb.jpg | YouTube「DOTA 1 - HOW TO DESTROY FOUNTAIN」（TheBaltazarTV）https://www.youtube.com/watch?v=fPeCaVMCx1g 第 669 秒，1080p 画面在浏览器里暂停后整页截屏（1536×735，两侧黑边是截屏留白）；画面右上角版本号 **v6.83d** | 14b4e4cb8aa0 | **DotA 1 6.83d 游戏内，天灾基地，白天**。崩碎之穴就是上面那个经典模型，没换皮、看不出染色：四根铜尖方尖碑、紫压边黑石坡顶朝**西南**（朝镜头），铜箍筒形拱在**东北**侧，屋脊一排 4 个白骷髅。它在泉水区**最南端**：正北是恶魔遗物那栋石塔，东边紧挨着竖排的 5 个红色英雄出生圈（Spawning Artifact），南边紧贴一道**铁钉木栅栏**，栅栏外就是一道往下的崖壁。体量比恶魔遗物大一圈。建筑周围**没有站人**，商人单位都在西边（见 `_scourge_base_area`） |
| yt_xUzkEwR4848_667c_tomb_magetower.jpg | https://i.ytimg.com/vi/xUzkEwR4848/hqdefault.jpg（视频「DotA - Destroying the Scourge Fountain on a PUB Game (garena) 6.67c」https://www.youtube.com/watch?v=xUzkEwR4848 的封面，480×360） | b6a75e71b4c9 | **6.67c 游戏内，夜里**，糊。右侧从上到下：被打的泉水 → 恶魔遗物石塔（尖碑 + 顶上一圈环）→ 最下面一栋**铜尖方尖碑 + 紫顶**的建筑，就是崩碎之穴；旁边一列 5 个玩家色出生圈。说明 6.67c 起位置和模型就跟 6.83d 一样 |

## 补充观察（没收图的）

- 更老的版本不一样：`_scourge_base_area` 里 6.59（q2HATr2uGlY）和另一段 6.57b 录像（https://www.youtube.com/watch?v=CWIu9sSneUk 封面）在同一个位置放的是**另一栋建筑**——八角形石台、深色板岩坡顶、正面一排骷髅、带铁栅门和台阶，不是遗物陵墓。我没认出它是哪个 WC3 模型，只记一笔：**6.6x 以前的天灾消耗品店长相可能不同**，本剧以 6.83d 为准，不受影响。
- 6.83d 同一段视频第 112 秒附近选中泉水时，鼠标悬停弹出的是泉水的攻击说明（190–199 混乱攻击、射程 1050），说明泉水和这两家店挨得很近，镜头一屏就能装下。

## 结论

**崩碎之穴在 DotA 1（6.67c–6.83d）画面里就是 WC3 原版的遗物陵墓，原样摆放**：一口巨大的黑石「石棺」，紫压边坡顶 + 后半截铜箍筒形拱顶，屋脊一排白骷髅，四角四根铜尖方尖碑；没有招牌、没有文字、门口不站商人。位置在天灾泉水区的最南端，北边是恶魔遗物，东边是 5 个出生圈，南边是栅栏和崖壁。

和 d01 §3.5 / d08 §1.1 对照：
- d01 写「模型 `buildings\undead\TombOfRelics` ✅」——**画面证实，没有出入**。
- d08 把位置标成「天灾基地 ⚠️（不死族阵营单位）」——现在有 6.83d 截图，可以去掉 ⚠️：就在天灾泉水旁、出生圈西侧。
- 中文名「崩碎之穴」是地图中文版的叫法，WC3 中文版里这栋建筑叫「遗物陵墓」，画面上看不到任何名字，两个名字指的是同一栋楼。
- 出图时注意：画面里的光是亡灵荒芜地表的冷绿色，白天截图里建筑本身是黑灰石 + 铜 + 紫，夜里截图会整体偏青。
