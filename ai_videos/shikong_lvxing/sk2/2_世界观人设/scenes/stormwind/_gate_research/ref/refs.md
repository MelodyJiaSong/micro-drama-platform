# sk2 · 暴风城入城段（城门 + 英雄谷）参考图库

> **版本锚**：经典旧世 Vanilla（1.x / WoW Classic），**大灾变 4.0.3a 之前**。
> **用途**：`../gate_spec.md` 的唯一图证来源。
> **纪律（`0_research/look_from_images.md` §3 + 2026-09-20 补记）**：
> ① 所有结论都在**放大 2–6 倍**后判读，远景/缩略图上看到的形制一律不写进规格书；
> ② **单图结论标 ⚠️**，两张及以上互相印证才标 ✅；
> ③ 全部图片**只进人眼（含 Claude 读图）**，**一张都不上传给生成模型、不入画**。

## 版本判定的三条依据（本库统一口径）

1. **文件上传时间不能用作版本依据。** 本站全部图片的 `imageinfo.timestamp` 都是
   `2023-10-05`（Fandom→warcraft.wiki.gg 整站迁移日），与拍摄版本无关。
2. **可用的依据只有三种**：
   a. **图源自述**（Blizzard 官方 WoW Classic 城市导览配图 / wiki 图注明写「before Cataclysm」）；
   b. **画面内的版本判据**（大灾变损毁与脚手架、乌瑟尔喷泉、港口、雄狮之眠、肯瑞托营地…）；
   c. **与 a 类图逐项比对**——几何逐件一致即判「该处形制未随版本改动」。
3. **英雄谷唯一一次几何变动**是 4.0.3a：屏墙被死亡之翼烧毁 + 脚手架、Danath 雕像倒塌；
   5.2.0 全部修复。因此**「屏墙完好 + 五尊雕像全部站立」的图，形制等同 Vanilla**；
   带火光/脚手架/倒塌雕像的图一律 ❌。

## 图库

| ref_id | 文件 | source_url | 版本判定与依据 | 证明了什么 | 能否入画 |
|---|---|---|---|---|---|
| r01 | `r01_classic_valley_ground.jpg` | https://warcraft.wiki.gg/images/Stormwind_City_Classic.jpg （图源页自述：news.blizzard.com《WoW Classic City Tour: Stormwind》） | **✅ Vanilla（最高可信）**。暴雪官方 WoW Classic 城市导览配图，图源栏直指 Blizzard 新闻稿。本库的**版本基准图**。 | 英雄谷地面平视北望全景：五尊雕像的排布与姿态、街灯形制、主路/人行道铺装、北端三拱屏墙、屏墙后蓝瓦半木建筑、天际线尽头的光明大教堂尖塔群 | ❌ 暴雪版权·只作形制依据·不入画·不上传生成模型 |
| r02 | `r02_valley_ground_north.jpg` | https://warcraft.wiki.gg/images/The_Valley_of_Heroes.jpg | **✅ 形制等同 Vanilla**。图注只写「in *World of Warcraft*」未标版本，但屏墙完好、五像全立、无脚手架；与 r01 逐项比对（雕像位序/姿态/持物、街灯、铺装、屏墙拱数）**10/10 一致** → 判为版本无关几何 | 比 r01 更靠北的机位；**画面内有多名卫兵 NPC 站在灯柱旁 → 本库的主比例尺图**；主路/人字砖步道/路缘石三层剖面 | ❌ 同上 |
| r03 | `r03_gate_aerial_intact.jpg` | https://warcraft.wiki.gg/images/Stormwind_Gate.jpg | **⚠️→✅ 形制可用**。现行版本俯视截图（分辨率 2560×1440、无 UI），版本未标注；但与 r04（wiki 明标 pre-Cata）**逐件比对一致**：四塔配置、蓝锥顶、外堡木甲板、狮首石雕、蓝底金狮旗、木门扇、护城水面、木栏杆、三拱屏墙。判为「城门几何未随版本改动」 | 城门段的**唯一高分辨率俯视**：门扇开启角度与比例、门洞净宽、四塔平面关系、引道弓形收放、护城水面位置、灯柱沿线间距 | ❌ 同上 |
| r04 | `r04_gate_precata.jpg` | https://warcraft.wiki.gg/images/Gates.jpg （用在 Stormwind Gate 条目 Gallery，图注原文「The Stormwind Gate before *Cataclysm*」） | **✅ 明标 pre-Cataclysm**。wiki 图注直接写明。分辨率仅 700×525，**只用于版本对账，不单独判形制** | 与 r03 的 A/B 对账：确认大灾变前后城门段几何**无差异**；另证实屏墙之后的大教堂尖塔剪影 | ❌ 同上 |
| r05 | `r05_gate_cataclysm_NEGATIVE.jpg` | https://warcraft.wiki.gg/images/Stormwind_Gate_Cataclysm.jpg （图注「After *Cataclysm*」） | **❌ Cataclysm**。画面内有版本判据：远端屏墙顶部橙红灼烧发光 + 木脚手架 | **反向样本**：这就是「不能画成这样」——本片禁止出现烧灼屏墙/脚手架。同时它的俯视角度补证了 r03 的门扇、狮首、旗帜、木栏杆细节（这些构件本身未损毁） | ❌ 同上（且形制上只作反向词来源） |
| r06 | `r06_statue_kurdran.jpg` | https://warcraft.wiki.gg/images/Kurdran.jpg | **✅ 形制等同 Vanilla**。雕像本体自建成起未重做；画面内屏墙完好、无脚手架 | 库德兰·蛮锤像：姿态/持物/基座形制/基座上的铭牌凹槽/基座紧贴水面 | ❌ 同上 |
| r07 | `r07_statue_khadgar.jpg` | https://warcraft.wiki.gg/images/Archmage_Khadgar_of_the_Kirin_Tor.jpg | 同 r06 | 卡德加像：长袍/长杖角度/杖头形制/八角低基座/身后拱桥 | ❌ 同上 |
| r08 | `r08_statue_turalyon.jpg` | https://warcraft.wiki.gg/images/Turalyon.JPG | 同 r06 | 图拉扬像：双手持剑于胸前、剑尖向下；位于中轴屏墙前的方台 | ❌ 同上 |
| r09 | `r09_statue_danath.jpg` | https://warcraft.wiki.gg/images/Danath.jpg | 同 r06（**注**：此像在 4.0.3a–5.2.0 期间是倒塌状态，本图中站立 → 非该窗口期） | 丹娜斯·托尔贝恩像：光头/肩扛长柄武器/八角基座；**画面左下角有卫兵 NPC → 本库雕像高度的主测量图** | ❌ 同上 |
| r10 | `r10_statue_alleria.jpg` | https://warcraft.wiki.gg/images/Alleria.jpg | 同 r06 | 奥蕾莉亚像：弓/箭袋/左臂托鹰、八角基座与铺地纹样 | ❌ 同上 |
| r11 | `r11_causeway_eyelevel_scale.jpg` | https://warcraft.wiki.gg/images/The_Unseen_Blade_-_Valley_of_Heroes.jpg | **⚠️ 版本未定（Legion 任务场景）**，但画面内屏墙完好、五像全立；**只用作比例尺与铺装质感**，不用于判任何「有无某构件」 | 引道地面平视 + 十余名卫兵 NPC 同深度站位 → 主路净宽的第二组独立测量 | ❌ 同上 |
| r12 | `r12_worldmap_precata.jpg` | https://warcraft.wiki.gg/images/WorldMap-StormwindCity-old4.jpg | **✅ pre-Cata 世界地图**（文件名 `-old4` 即旧版地图序列；图中**无暴风城港口、无雄狮之眠**，公园区完好 → 3.0.2 之前） | 英雄谷在全城平面中的位置与朝向（城南、轴线指向西北偏北、尽头分叉进贸易区） | ❌ 同上 |
| r13 | `r13_concept_art_NOTBUILT.jpg` | https://warcraft.wiki.gg/images/Stormwind_Gates_concept_art.jpg （作者 Thomas Jung，出自官方 wow-classic 艺术画廊） | **✅ Vanilla 期概念图，但 ❌ 不作形制依据**——实拍判读：画面是**陡尖多层塔楼 + 垂幔 + 长阶梯**的早期方案，与最终实装的「圆塔＋蓝锥顶＋木门扇」**完全不同** | **反向样本**：证明「拿概念图当形制依据」会直接建错。列出来是为了防止下一个人去用它 | ❌ 同上 |
| r14 | `r14_wwi2006_banner.jpg` | https://warcraft.wiki.gg/images/WWI2006_Stormwind_Zone.jpg | **✅ 2006 年实物照片**（暴雪嘉年华 WWI 2006 展台，时间点在 Vanilla 期内） | 联盟旗帜的**实物配色与纹章**：深宝蓝底 + 暗金狮首纹 + 金边 + 下摆双尖角 —— 与 r03/r05 游戏内旗帜互证 | ❌ 同上 |

## 本次没有采用的图（和原因）

- `Valleyofheroes.JPG` —— **不是游戏截图**，是 RPG 桌游书《Shadows & Light》的插画（James Stowe）。RPG 线与游戏几何不同源，**不作形制依据**。
- `Stormwind_City_TCG.jpg` / `Exploring_Azeroth_-_Stormwind.jpg` / `Chronicle2_Statue_of_Alleria.jpg` / `The_Comic_-_Valley_of_Heroes.jpg` —— 集换式卡牌 / 画册 / 漫画插画，**均为再创作**，比例与构件自由发挥，不作形制依据。
- `Stormwind_Gates_Hearthstone_styleguide.jpg` —— 炉石风格指南插画，风格化幅度大。
- `Cataclysm_Login_No_text.jpg` / `Valley_of_Heroes_-_Cataclysm_Danath's_statue.jpg` —— ❌ 大灾变损毁状态。
- `Classic_-_Stormwind_City_and_Paladin.jpg` —— 已亲眼看过：**画面是法师区/公园区街景，不含城门与英雄谷**，与本任务无关。
- `Great_Gnomeregan_Run_-_Stormwind_Gate.jpg` —— 已亲眼看过：**画面全是艾尔文森林草地与玩家，城门根本不在画内**（文件名有误导性）。
