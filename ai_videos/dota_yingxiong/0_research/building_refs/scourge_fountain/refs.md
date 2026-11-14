# 天灾泉水 Defiled Fountain of Life 被污染的生命之泉（`ndfl`）· 原版模型与 DotA 1 画面参考

> 暴雪娱乐素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 下载（免费公开页面，未调用收费服务）。
> 地图数据（6.83d `Units\UnitUI.slk`）：模型 `buildings\other\FountainOfLifeDefiled\FountainOfLifeDefiled`，选择圈 scale 5、不染色；坐标 (6784,6368)，地图东北角。出生点能量圈和商店不在本目录范围。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| yt_7VSCu4XkbLU_hq2_defiled_fountain_circles.jpg | https://i.ytimg.com/vi/7VSCu4XkbLU/hq2.jpg（视频「Bot Bash - Warcraft 3: Dota Allstars」https://www.youtube.com/watch?v=7VSCu4XkbLU 的自动截帧） | 247b19124476 | **最清楚的一张游戏内泉水**（没被技能挡住）：一堆**灰绿色竖立的尖岩**围成一圈，中间一池**刺眼的亮绿色**液体发光，绿光把岩石内侧染绿；泉水右侧一道弧排着彩色出生圈（粉、灰、浅蓝……）；左边是骨头 / 木桩围栏；周围暗绿草地和灰白扭曲树干的树 |
| yt_GRX57T2XAc0_hq1_defiled_fountain_selected_v649b.jpg | https://i.ytimg.com/vi/GRX57T2XAc0/hq1.jpg（视频「Dota - Rjdagreat3 - No to Scourge!」https://www.youtube.com/watch?v=GRX57T2XAc0 的自动截帧，v6.49b） | 43b5e9d232a7 | 信息栏写「**Defiled Fountain of Life**」，头像是绿光岩堆，证实名称和外观对应；画面右上就是它：绿光岩堆，旁边是两座商店建筑（不在本目录范围）；屏幕中间是「The Sentinel has won!」字样 |
| yt_0j0c8tjU2eY_fountain_attacked_v667c.jpg | https://i.ytimg.com/vi/0j0c8tjU2eY/maxresdefault.jpg（视频「Destroying Scourge Base In 1 Min」https://www.youtube.com/watch?v=0j0c8tjU2eY 的封面，v6.67c） | 15680276df44 | 1280×720：泉水正被打，绿色液光从英雄身后透出来，几根灰色尖岩伸出；尺度上泉水比英雄宽四五倍；右侧四个出生圈（粉、黑灰、浅蓝、暗绿）；地面是暗绿苔草，左上有骨头堆和木桩栅栏 |
| wowpedia_BTNFountainOfLifeDefiled.png | https://static.wikia.nocookie.net/wowpedia/images/7/7f/BTNFountainOfLifeDefiled.png/revision/latest?format=original（页面 https://wowpedia.fandom.com/wiki/Fountain_of_Health） | 91e688d3c8c5 | 经典图标：黑灰尖岩中间一池青绿色水，岩缝里淌下荧光绿的黏液，像被毒污染 |
| wowpedia_Fountain_of_health_WC3_未污染对照.jpg | https://static.wikia.nocookie.net/wowpedia/images/1/11/Fountain_of_health.jpg/revision/latest?format=original（页面同上） | da2e16e003e3 | **对照：未污染的经典生命之泉**（同一套岩石布局）：几块灰色尖岩围着一池发蓝光的水，岩缝里一道小瀑布，前面两盏矮石灯笼；被污染版就是这一套换成绿光 |
| wowpedia_Reforged_Fountain_of_Chaos_对照.jpg | https://static.wikia.nocookie.net/wowpedia/images/6/66/Warcraft_III_Reforged_-_Fountain_of_Chaos.jpg/revision/latest?format=original（页面同上，wiki 图注：重制版的被污染生命之泉） | 4b553b32945f | **重制版对照（不照搬）**：一圈深灰尖岩，后方两座岩峰之间一道亮绿瀑布泻进绿池；前面两盏圆顶石灯笼，灯窗透绿光；岩石上长着绿苔——形制和经典版一致，看得更清楚 |

多建筑截图另见 `../_scourge_base_overview/yt_kgMRy9SOLv4_fountain_shops_v669b.jpg`（泉水被打，旁边出生圈和商店）。

## 结论

DotA 1 的天灾泉水是**一堆天然尖岩围出的发绿光毒池**：几块灰（偏灰绿）色竖立尖岩围成一圈，后面有一道小瀑布，池里是刺眼的荧光绿液体，绿光往外溢，染亮岩石内侧；前面两盏小石灯笼（经典未污染版和重制版都有，DotA 截图分辨率下看不清）。它和近卫泉水是同一个岩堆模型，只是水从蓝光换成了绿光。泉水旁边一道弧排开彩色出生圈，左侧是骨头和木桩栅栏，地面是暗绿苔草，不是纯黑荒地。

和考据、现有卡的出入：

1. **d01 §3.4** 只写了模型路径，没写外观，可以补「尖岩毒池、亮绿光」。
2. **bg14 天灾泉水与商店**：写「直径约六米的**圆形石砌泉池**、齐膝池壁、**中央刻藤蔓纹的石柱托两层浅石盘**、池水浑浊发暗、暗绿偏紫的病态微光」。出入：① 原版没有人工砌的圆池、石柱和石盘，是**天然尖岩堆 + 小瀑布**，这是最大的形制错误；② 光不是「微光」，是整池**很亮的荧光绿**，是天灾基地最亮的光源；③ 灯笼是原版就有的（两盏矮石灯笼，重制版灯窗透绿光），卡里把灯笼挂到了墓穴门口，可以挪回泉边；④ 卡里「与 bg13 同一形制」这条思路是对的——近卫泉和天灾泉原版就是同一模型，前提是 bg13 也改成岩堆形制。
3. 出生圈按原版是五个彩色光圈（玩家色），bg14 写的「冷绿刻纹石板」是真人化处理，由能量圈那边的 refs 定。

没找到：经典版（非重制版）被污染泉水的 wiki 模型渲染图（warcraft.wiki.gg 本次 403 / 502；wowpedia 只存了重制版的图）。
