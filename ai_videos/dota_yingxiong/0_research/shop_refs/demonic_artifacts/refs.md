# 天灾独有商店 · 恶魔遗物 Demonic Artifacts（地图数据模型 `buildings\other\MageTower`）

> 暴雪娱乐素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 下载（免费公开页面，未调用收费服务）。
> 对应近卫的奎尔瑟兰的密室（同货，d08 §2.3）。d01 §3.5 把模型标了 ⚠️，本卡重点就是核这个。warcraft.wiki.gg 图床本轮整站 502，经典模型图改从 wowpedia 的 archive.org 存档拿。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wp_High_Elven_Barracks_WC3.png | https://web.archive.org/web/20240205180402im_/https://static.wikia.nocookie.net/wowpedia/images/f/fa/High_Elven_Barracks.jpg/revision/latest?cb=20181114201641（页面 https://web.archive.org/web/20240205180402/https://wowpedia.fandom.com/wiki/High_Elven_Barracks，信息框「Classic」页签）。服务器实际回的是 webp，本地转成 PNG 存，像素未改 | 2df7787422b3 | **经典模型「高等精灵兵营」游戏内截图（419×420）**，草地上俯视。**两层退台的灰白石块建筑**：下层是带台阶的平台，正面台阶中间嵌一颗**发黄光的圆球**；上层再缩进一级，每层顶面各有一块**金边圆形徽章**（里面是螺旋 / 花纹浮雕）；上层正面一道铜色拱形小门。三根**石质方尖碑**立在左、右前、右后三个角，碑身上开着黑色的眼形小孔，右后那根最高。上层后方斜挂一道**铜色圆环、环上镶绿宝石**（像一个倾斜的星盘环）。地面铺灰色石砖，四周碎石。整体是人类 / 高等精灵的石头建筑，**没有任何恶魔、亡灵元素**，没有招牌和文字 |
| wp_BTNMageTower.png | https://web.archive.org/web/20240205180402im_/https://static.wikia.nocookie.net/wowpedia/images/f/f2/BTNMageTower.png/revision/latest?cb=20090112013855（同上页面，高等精灵兵营用的图标） | b870ed69221c | 经典图标 64×64「BTNMageTower」：同一座石塔的近景，上方一道**蓝色**弧环 + 铜色光晕（图标里环是蓝的，模型里是铜 + 绿），下面是石门和圆徽章 |
| wp_High_Elven_Barracks_Reforged.jpg | https://web.archive.org/web/20240205180402im_/https://static.wikia.nocookie.net/wowpedia/images/8/83/Warcraft_III_Reforged_-_High_Elven_Barracks.jpg/revision/latest?cb=20191019101131（同上页面「Reforged」页签） | e17df0cf1bcb | **重制版，只作对照，不照它**：完全换了设计——蓝色穹顶 + 金色月牙尖饰的圆殿，三座细高的蓝顶小塔，一道带金扶手的大台阶。和 DotA 1 画面里的东西**完全不像** |
| yt_fPeCaVMCx1g_maxres2_683d_magetower.jpg | https://i.ytimg.com/vi/fPeCaVMCx1g/maxres2.jpg（YouTube 自动截帧，视频「DOTA 1 - HOW TO DESTROY FOUNTAIN」https://www.youtube.com/watch?v=fPeCaVMCx1g ，1280×720；左上的计时器是作者加的） | 2568f66032bb | **DotA 1 v6.83d 游戏内，白天**。泉水在画面中上方（被一圈红色攻击范围框住，Sven 在砍）；泉水**正南**就是这栋楼：两层退台灰白石块、两块金边圆徽章、正面台阶上发黄光的圆球、三根带眼孔的石尖碑、后上方铜环绿宝石——**和上面经典「高等精灵兵营」一模一样**，看不出染色或缩放异常。楼东边是竖排 4 个（第 5 个在画面外）红色出生圈，画面下沿露出崩碎之穴的一角。楼周围不站人 |
| yt_6QEcSWqs9ek_fountain_magetower.jpg | https://i.ytimg.com/vi/6QEcSWqs9ek/maxresdefault.jpg（视频「DOTA URSA DESTROYING FOUNTAIN - DIVINE RAPIER (BEYOND GODLIKE)」https://www.youtube.com/watch?v=6QEcSWqs9ek 的封面，作者加了大字和箭头；同一视频自动截帧 HUD 写的是 v6.83s r64，即 6.83 的 AI 版地图） | ed675b8729a1 | 夜里近景。上方是「The Scourge」泉水（灰石堆 + 冰晶 + 绿水）；右下角就是这栋石塔的俯视：退台石块、圆徽章、底层台阶和绿 / 黄光点；右边是红色出生圈。封面加了字，只看右下角 |

## 补充观察

- 6.59（`_scourge_base_area/yt_q2HATr2uGlY_…`）和 6.72f（`_scourge_base_area/yt_4zh6dGIuICc_…`）的夜景里也是同一栋楼、同一个位置（泉水南、出生圈西），夜里被荒芜地表的光照成偏青绿。
- wowpedia「High Elven Barracks」页的 Notes 说这栋兵营 "uses the original model for the Mage Tower"，并说明法师塔在发售前被奥秘圣殿（Arcane Sanctum）取代——也就是说 `buildings\other\MageTower` 是 WC3 开发期**人族法师塔的旧模型**，正式版人族改用奥秘圣殿，旧模型留给战役里的高等精灵兵营用。
- 网页搜索结果里 Liquipedia 的商店页（托管于 Dota 2 wiki，内容为 DotA 1）也提到：天灾一方的杂货店叫 Demonic Artifacts，用的是高等精灵兵营的模型。Liquipedia 页面本身被人机验证挡住，我没打开原页，只当旁证；主据是 6.83d 地图数据里的模型路径 `buildings\other\MageTower`（见 d01 §3.5）。

## 结论

**恶魔遗物在 DotA 1 画面里是一座灰白石头的退台小石塔**——就是 WC3 经典版的「高等精灵兵营」，也就是 `buildings\other\MageTower`（人族法师塔的旧版模型）：两层石台、金边圆徽章、台阶上一颗发黄光的球、三根带眼孔的石尖碑、后上方一道镶绿宝石的铜环。**一点恶魔味都没有**，名字叫「恶魔遗物」，样子是高等精灵 / 人类的法师建筑。

和 d01 / d08 对照：
- d01 §3.5「地图数据指向 `buildings\other\MageTower` ⚠️」——**画面证实指向没错，⚠️ 可以去掉**。要补一句：这个模型在 WC3 里的名字是「高等精灵兵营 High Elven Barracks」（法师塔旧模型），不是一座「法师塔」单位，也不是奥秘圣殿。
- 有个容易弄混的点：近卫的奎尔瑟兰的密室用的是**正式版**奥秘圣殿 `ArcaneSanctum`（缩放 0.8），天灾的恶魔遗物用的是它的**前身**。两家同货的店，长得是「一新一旧两版人族法师建筑」，并不是一边精灵一边恶魔。
- d08 §1.1 的位置「天灾基地 ⚠️」：6.83d 截图里就在天灾泉水正南、崩碎之穴北边、出生圈西边，可以去掉 ⚠️。
- 出图时：要么照原样做成「混在亡灵基地里的一座人类石塔」（这正是 DotA 1 的真实画面），要么按 world_rules 另行设计；**不能照重制版**（蓝穹顶圆殿，跟 DotA 1 毫无关系），也不要凭名字脑补成恶魔祭坛。
