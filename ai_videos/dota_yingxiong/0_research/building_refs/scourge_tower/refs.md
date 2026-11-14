# 天灾防御塔 Spirit Tower 幽魂塔（等级 1–4，共 11 座）· 原版模型与 DotA 1 画面参考

> 暴雪娱乐素材，只作人眼参考：不进成片、不作生成服务的上传参考。2026-10-21 下载（免费公开页面，未调用收费服务）。
> 经典版（Classic）为准；DotA 1 截图里的队伍色只用来认建筑，真人化不照搬。

## 先核实：到底是哪个模型（6.83d 地图解包 `Units\UnitUI.slk`、`Units\UndeadUnitFunc.txt`）

| 单位 | 名称 | 模型文件 | Animprops（决定显示哪种外形） | 图标 |
|---|---|---|---|---|
| `u00M` | Spirit Tower - level 1 | `buildings\undead\Ziggurat\Ziggurat` | `upgrade,first` | BTNZigguratUpgrade |
| `u00D` | Spirit Tower - level 2 | 同上 | `upgrade,first` | 同上 |
| `u00N` | Spirit Tower - level 3 | 同上 | `upgrade,first` | 同上 |
| `u00T` | Spirit Tower - level 4 | 同上 | **`upgrade,second`** | 同上 |
| 对照 `uzig` | 通灵塔 Ziggurat | 同上 | 无 | BTNZiggurat |
| 对照 `uzg1` | WC3 原版幽魂塔 | 同上 | `upgrade,first` | BTNZigguratUpgrade |

- WC3 的通灵塔、幽魂塔、蛛魔塔是**同一个模型文件** `Ziggurat.mdx` 的三种形态，靠 Animprops 切换：无 = 通灵塔，`upgrade,first` = 幽魂塔，`upgrade,second` = 蛛魔塔（Nerubian Tower / 冰塔）。d01 写「模型是通灵塔 Ziggurat」只说对了文件名。
- 所以 **1–3 级塔是幽魂塔外形，4 级（遗迹旁两座四塔）按数据是蛛魔塔外形**。⚠️ 四塔外形只从数据推出，下面截图里只有一张糊图（`../scourge_frozen_throne/yt_7g2x8eoz0l0_hq2_throne_v678c.jpg` 左下角）可能拍到。
- 四个等级的模型缩放、颜色完全一样（scale 4.25、modelScale 1、RGB 255/255/255），1–3 级之间**外观没有区别**。
- 攻击弹道：`Phoenix_Missile_mini.mdl` + `ZigguratMissile.mdl`——游戏里看到的是一团橙红小火球（见 gPLXJIu0nMo 截图），不是冷蓝光束。
- 坐标（脚本 CreateUnit）：一塔 (-4704,5920)(1056,-96)(6240,-2080)；二塔 (32,5920)(2528,1824)(6304,-96)；三塔 (2976,5792)(3936,3488)(6368,2528)；四塔 (4832,4832)(5152,4512)，紧贴遗迹 (5184,4864) 西侧和南侧约 350。

| 文件 | 来源 URL（含所在页面） | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| wowpedia_Spirit_Tower_WC3.gif | https://static.wikia.nocookie.net/wowpedia/images/5/59/Spirit_Tower.gif/revision/latest?format=original（页面 https://wowpedia.fandom.com/wiki/Spirit_Tower_(Warcraft_III)；原图出自 classic.battle.net/war3/undead/buildings/spirittower.shtml） | 9bd8c81a909e | **经典幽魂塔（1–3 级外形）**：矮胖的八角台基，四面斜墙往上收，墙面是紫灰金属板，边上压着一根根青铜 / 金色的骨肋；正面一道楼梯铺着队伍色条纹（这张是紫色）；顶上一圈小骷髅，四根白骨弯牙往上合拢，中间托着一颗**队伍色的水晶 / 光球**，外面绕着蓝白电弧；宽和高差不多，不是细高尖塔 |
| wowpedia_Nerubian_Tower_WC3.gif | https://static.wikia.nocookie.net/wowpedia/images/b/bb/Nerubian_Tower.gif/revision/latest?format=original（页面 https://wowpedia.fandom.com/wiki/Nerubian_Tower_(Warcraft_III)） | 960593b7cf3b | **经典蛛魔塔（按数据 = 4 级塔外形）**：同一个台基但更厚重，正面挡着一张大骷髅脸和竖肋，两侧尖刺外伸；顶上两根弯角夹着一颗**亮冰蓝的冰球**，冰球发强光；侧面同样有紫色（队伍色）条带 |
| wowpedia_BTNZigguratUpgrade.png | https://static.wikia.nocookie.net/wowpedia/images/9/95/BTNZigguratUpgrade.png/revision/latest?format=original（页面同上 Spirit Tower） | fe4627453d2c | 经典图标（DotA 四个等级都用它）：黑底上一座骨肋塔，顶上一根绿色竖晶体，两侧弯角，绿色是图标自带的亡灵绿 |
| yt_eFMfQ7Be088_spirit_tower_L1_closeup.jpg | https://i.ytimg.com/vi/eFMfQ7Be088/maxresdefault.jpg（视频「Ancient Protector vs Spirit Tower - Level 1 \| Who Will Beat?」https://www.youtube.com/watch?v=eFMfQ7Be088 的封面，作者加了 VS 字样） | fcafba201691 | **DotA 1 游戏内 1 级塔特写（经典版）**：俯视下是一朵八瓣「伞」——八片斜墙像帐篷布一样往外摊，每片之间是青铜色骨肋；四面楼梯是**队伍色条纹**（这局测试图里是红色）；顶上一圈白骷髅，四根白牙弯钩托着一块**尖头的红色晶体**（队伍色），一道蓝白电弧绕着它转；塔脚压着黑色荒芜地表的一圈影子 |
| yt_gPLXJIu0nMo_hq2_spirit_tower_L1_label.jpg | https://i.ytimg.com/vi/gPLXJIu0nMo/hq2.jpg（视频「Tower Sentinel vs Tower Scourge \| Who Will Beat?」https://www.youtube.com/watch?v=gPLXJIu0nMo 的自动截帧） | a36dc6ccf689 | 游戏内标准镜头距离：信息栏写「**Spirit Tower - level 1**」，证实名称；塔在画面里只有英雄两三倍大，读得出的是「红条纹 + 顶上红光」；它射出的弹道是一团**橙红火球**，近卫古树射的是蓝白光束 |
| yt_cQB_W_AWtoE_scourge_tower_green_v68AI.jpg | https://i.ytimg.com/vi/cQB_W_AWtoE/maxresdefault.jpg（视频「DotA Allstars 6.88 AI 1v5 \| Legion Commander \| Fountain Destroy + Rampage」https://www.youtube.com/watch?v=cQB_W_AWtoE 的封面，画面右上角写 DotA 6.8 AI） | e754f0944fed | **天灾方真实颜色**：塔的楼梯条纹和顶上晶体都是**亮绿色**（天灾 Player(6) 默认绿），晶体发绿光，正面一颗骷髅；塔周围是暗绿草地和黑灰荒地交界，背后一排灰白扭曲树干的树 |
| yt_Sm2tTC56wqk_scourge_tower_v683.jpg | https://i.ytimg.com/vi/Sm2tTC56wqk/maxresdefault.jpg（视频「DOTA1第一人称大熊，600攻逆风军团！强拆高地」https://www.youtube.com/watch?v=Sm2tTC56wqk 的封面，右上角写 DotA6.83，16 对战平台） | 6da50cb1af56 | 6.83 国服对局：被攻击的天灾塔，绿色条纹、顶上绿光，红圈是敌方选中圈；地面是暗绿苔地夹着灰绿大石板 |

## 结论

DotA 1 里天灾塔长这样：**一座矮胖的八角骨肋「帐篷塔」**，台基宽、往上收得快，八片斜墙之间是青铜骨肋，四面楼梯铺着**绿色**队伍色条纹；顶上一圈白骷髅，四根白骨弯牙托着一块**发绿光的尖头晶体**，外面绕一道蓝白电弧；攻击打出橙红小火球。1–3 级完全一个样，4 级（遗迹旁两座）按数据换成蛛魔塔外形（前脸大骷髅、顶上冰蓝冰球），没拿到清楚截图核对。

和考据、现有卡的出入：

1. **d01 §3.3**：「模型是通灵塔 Ziggurat」→ 文件名对，但显示的是幽魂塔形态（Animprops `upgrade,first`），四塔是蛛魔塔形态（`upgrade,second`），建议 d01 补一句。「顶上有发光的能量球」→ 实为**尖头晶体**，颜色是队伍色（天灾 = 绿），不是固定颜色的球。
2. **bg5 天灾中路一塔**：写的是「约十米高、四层粗凿黑玄武岩逐层收窄的阶梯尖塔，塔顶四根黑铁尖爪托冷蓝光球」。出入：① 原版不是细高的分层石塔，是宽矮的八角斜墙骨肋结构，材质读起来是紫灰金属板 + 青铜骨肋 + 白骨，不是黑玄武岩；② 托晶体的是**白骨弯牙**不是黑铁爪；③ 光是**绿色**（队伍色）加蓝白电弧，不是冷蓝；④ 负面词里的「金字塔、玛雅神庙」正好是原版的阶梯 / 台基感，真人化可以保留八角台基和正面楼梯。冷蓝光可以留给四塔（蛛魔塔冰球）。
3. 队伍色按 world_rules 不进画面：真人化时绿条纹可以改成褪色的绿铜锈或腐绿布幔，保留「四面楼梯有色带」这个轮廓。

没找到：DotA 1 里 4 级塔（蛛魔塔外形）的清楚截图；WC3 经典版高分辨率的幽魂塔多角度图（warcraft.wiki.gg 本次 403 / 502 拒绝访问，只拿到 battle.net 旧站 150 px 渲染图）。
