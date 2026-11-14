# 边路商店 · 地精实验室 Goblin Laboratory · 原版模型参考（WC3 中立建筑「地精实验室」，模型 / 图标文件名 `AmmoDump`，DotA 里缩放 0.65）

> 暴雪娱乐素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 下载（免费公开页面，未调用收费服务）。
> 和地精商人并排摆在同一处边路商店（见 `../side_shop_goblin_merchant/refs.md`，那边也记了 PlayDotA 2010 年「每处两座：Goblin Merchant 和 Goblin Laboratory」的旁证）。经典版（Classic）是标准；重制版只作对照，**不照它的造型**。warcraft.wiki.gg 当天整站 403 / 502，图改从 wowpedia（fandom）和暴雪旧官网 classic.battle.net 取。

**先说名字**：`AmmoDump`（弹药堆）是 WC3 里「地精实验室」这座建筑的**模型和图标文件名**（图标就叫 `BTNAmmoDump.png`，wowpedia「Goblin Laboratory (Warcraft III)」页用的就是它）。它不是一堆弹药箱，而是一整座房子。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wp_Goblin_Laboratory_classic.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/1f/Goblin_Laboratory.JPG（页面 https://wowpedia.fandom.com/wiki/Goblin_Laboratory_(Warcraft_III)） | 424944be1d56 | **经典模型游戏内截图（对战地图，林间空地上）**：一座**方形、上小下大的碉堡式小楼**。最底下是一圈木板包边、上面钉着一排排**大圆铆钉**的方台，台子边沿堆满**沙袋**；中间是一层**灰蓝色的石 / 铁皮方屋**，正面一个小方窗缝和一扇木门；屋顶又是一圈沙袋。屋顶前沿立着一块**木牌，写着「TEMPLE OF BOOM」**（OF 黄字、BOOM 红字）；门边贴着一块**红底黑字的「WELCUM」小牌**。四角斜插着几根削尖的木桩，右侧伸出一根木杆，杆头是一个**灰铁色的大锤头 / 炮弹头**。脚下是几块浅色石板和碎石。颜色：木头黄褐、沙袋土黄、屋身灰蓝、牌子红黄 |
| cbn_goblin_laboratory.gif | http://classic.battle.net/war3/images/neutral/buildings/laboratory.gif（暴雪旧官网中立建筑页 http://classic.battle.net/war3/neutral/buildings.shtml） | 2cf8a5d502dd | 官网渲染图（黑底），和上图同一个经典模型：铆钉木台、沙袋、灰蓝方屋、顶上木牌（小图里字看不清，只见红黄两色）、四周尖木桩、右上方伸出的灰铁锤头。轮廓是一座矮胖的方金字塔 |
| wp_BTNAmmoDump.png | https://static.wikia.nocookie.net/wowpedia/images/9/9e/BTNAmmoDump.png（页面同上） | d867a6c8f833 | 经典图标（地精实验室）：沙袋顶、铆钉木台和那块红黄木牌，右边灰铁锤头 |
| wp_Goblin_Laboratory_Reforged.jpg | https://static.wikia.nocookie.net/wowpedia/images/3/34/Warcraft_III_Reforged_-_Neutral_Goblin_Laboratory.jpg（页面同上） | fa6b439eb1e2 | **重制版（对照，不照搬）**：同样的铆钉黄铜方台、满圈沙袋、灰铁方屋、四周尖木桩，但屋顶改成一大团**红褐色、带尖刺的皮革 / 帐篷顶**，木牌改写「TEMPLE OF KABOOM」，右侧那根杆头变成一个铆钉木铁大球；门边仍是「WELCUM」红牌，台角多了一扇红色小地窖门。红色尖顶是重制版加的，经典版没有 |
| wp_BTNAmmoDump-Reforged.png | https://static.wikia.nocookie.net/wowpedia/images/0/03/BTNAmmoDump-Reforged.png（页面同上） | d128ce70318e | 重制版图标（对照）：红褐尖刺顶 + 「TEMPLE OF KABOOM」木牌 + 沙袋铆钉台 |

没找到：**DotA 1 游戏内地精实验室 / 边路商店的截图**，所以它在 DotA 里和地精商店怎么摆、朝哪边，没有画面证据。DotA 里的地精实验室只卖物品（d08 §1.1 那 12 件），WC3 原版能雇的地精工兵、飞艇、伐木机在 DotA 里没有。

## 结论

1. **地精实验室在 DotA 1 里也是一座建筑**：一座矮胖的方形碉堡——底下是钉满大圆铆钉的木板方台，台沿和屋顶堆着土黄色沙袋，中间是灰蓝色的石 / 铁皮方屋（小窗缝、木门），屋顶立一块「TEMPLE OF BOOM」木牌，门边一块红色「WELCUM」小牌，四角斜插削尖木桩，侧面伸出一根挑着灰铁大锤头的木杆。缩放 0.65，和旁边的地精商店差不多大。模型里**没有人物**，不像地精商店那样站着一个地精。
2. **和现有描述对照**：
   - d01 §3.5 写「地精实验室用弹药堆 `AmmoDump`」——路径没错，但「弹药堆」是把模型文件名直译了，容易让人以为是一堆箱子。它就是 WC3 的地精实验室建筑，建议以后写成「地精实验室建筑（模型文件名 AmmoDump）」。
   - **bg12 把它画成「一堆码得歪歪扭扭的铁箍木箱与木桶、几卷粗绳、一辆盖油布的推车、桶上有焦痕」，和原版不符**。原版是一座有墙有顶有门的方碉堡，沙袋、铆钉、尖木桩和挑出的锤头是识别点；完全没有推车和木桶堆。
   - bg12「招牌一律无字」是按世界规则做的改动，没问题；但要知道原版这座房子**最显眼的就是那块「TEMPLE OF BOOM」大木牌和红色「WELCUM」牌**。去掉字以后，可以留下木牌本身和红牌的形状、颜色。
   - bg12 的「火药焦痕」在气质上和原版的「BOOM」对得上，但原版是靠招牌和锤头表达的，不是靠烧焦的木桶。
