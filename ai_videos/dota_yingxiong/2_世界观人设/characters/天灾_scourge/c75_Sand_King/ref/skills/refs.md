# c75 沙王 · 技能特效参考（DotA 1 实机 + 地图数据）

> 暴雪娱乐 / DotA Allstars 版权素材，只作人眼参考：不进成片，也不作生成服务的上传参考。2026-10-26 下载（免费公开 YouTube 录像，未调用收费服务）。录像只下 480p 及以下到会话临时目录用于抽帧，未入库；入库的只是本地抽帧拼图（含游戏 UI，只看特效）。抽帧、扫色与拼图脚本在当次会话临时目录（`build_c75.py`、`mk.py`、`scan.py`，未入库）。
> **以 DotA 1（6.83d）为准**。本表只收 k753 腐蚀之终（Caustic Finale）和 k754 地震（Epicenter）；沙王外观以 `ref/model/refs.md` 为准。
> 拼图格内标签如下（每格左上角是「代码 + 录像时间」，每行顶上是英文说明）：
> - `MW`：经典画质，**DotA v6.83d**（画面右上角版本号 `v6.83d`，选中英雄面板 `Crixalis / Level 7 Sand King`）。来源「DotA 6.83d - Sand King, Crixalis Beyond GODLIKE ! #2」https://www.youtube.com/watch?v=MwjhDkAab6o （TheBaltazarTV，2016-01-02），只下视频轨 360p，录像 sha `415739baf1a1`。
> - `TS`：经典画质，**DotA v6.83d**（右上角 `v6.83d`，俄文客户端，面板 `Crixalis / Уровень 19, Sand King`）。来源「Dota 1 Sand King 6.83d」https://www.youtube.com/watch?v=tsTb814EJ9k （A_J_S FRance，2016-11-12），只下视频轨 480p，录像 sha `69bf82ab95f5`。
> - `SG`：经典画质，**版本没读出** ⚠️（画面无版本号；俄文客户端，头顶名牌 `Crixalis / Уровень 25`）。来源「Crixalis skill dota 1 (Санд Кинг скилы)」https://www.youtube.com/watch?v=sGr6qBLy1Tg （zigor ik，2016-11-05，16 秒技能演示，片内字幕标出 Burrowstrike / Epicenter / Sand Storm），480p，录像 sha `d4063cb45c75`。
> - `XH`：Reforged 高清画质，**DotA 6.85k 非官方改图**（不是 6.83d）。来源「Warcraft 3 Reforged: DOTA - All Strength Heros of The Scourge!!!」https://www.youtube.com/watch?v=xH2Fqh8FluQ （DeeTee Gaming，章节「16 CRIXALIS THE SAND KING」28:44–30:44）。本地已下载整片 `0_research/media_refs/videos/xH2Fqh8FluQ/xH2Fqh8FluQ_complete_av.mp4`（640×360），本次直接读本地文件，没有重下。英雄 25 级、像测试模式，只看特效。**Reforged 里沙王是浅青色带晶刺的高清新模型，外观不能拿来对照**。
> - `DM`：`ref/model/yt_dmP-v1StWpA_maxres.jpg`（YouTube 封面，DotA **v6.81d**，经典画质），已在 `ref/model/refs.md` 登记；这里只截入拼图作地震的旁证。
> - 下载、看过但没进拼图的录像：`ylb4-1E914k`（「Sand King Rampage Dota 1」经典，版本未读出，团战太乱）、`W-qLMk6vH78`（「DotA - Crixalis the SandKing」2009 年剪辑合集，加了电影片段与滤镜）、`yxKTkkQbVYU`、`U4V96TWjtpM`、`nzGqxhYiz5Y`（2008–2010 经典短片，看不清技能）；`WlV-FCGPxks`、`feSbysa59-A`、`v5ksTRc_z_k`、`HdesfveEum4`、`AqQ50jT9aJw`（标题含 Caustic Finale / Epicenter，实为 Dota 2）。

| 文件 | 来源 | sha256 前 12 位 | 看到了什么 |
|---|---|---|---|
| dota1_k754_epicenter_frames.jpg | 版本证据：MW 11:27.60、TS 32:23.50 整帧；MW 11:26.00–11:28.75；TS 32:22.17–32:24.81；SG 0:05.80–0:09.00；XH 30:04.50–30:15.00；DM 封面 | 0875d5d2fc10 | **地震（6.83d 经典，MW / TS）**：以沙王为圆心，一圈接一圈地扩出**亮黄偏柠檬绿的粗光环**，环身带向外的放射状条纹、环内是半透明的黄色光雾；新环从他脚下长出时旧环还在外扩，所以常同时看到 2–3 圈同心环（MW 11:27.75–11:28.50、TS 32:23.82–32:24.81）。环扫过的范围很大，几乎占满半个屏幕；脉冲之间沙暴的土黄尘雾也在（他常配合沙暴）。MW 里镜头切过来时他已冲进人群（11:26.0，像是遁地突袭 ⚠️），紧接着开始脉冲（11:27.0），像是先引导、后冲入的常见连招；**本片没拍到 2 秒引导的动作** ⚠️。**SG（版本未读出）**同样是黄色光环，一圈比一圈大。**XH（Reforged 6.85k）**：脉冲前 30:05–30:08 背上冒出几次**绿色尖刺状闪光**（是否为引导特效未核实 ⚠️），随后是**偏金棕色、较暗的光环**一圈圈外扩（30:09–30:15）。**DM（v6.81d 封面）**：沙暴中一道大黄色光环，与 6.83d 一致 |
| dota1_k753_caustic_finale_frames.jpg | XH 29:59.80–30:03.30（整体）；XH 30:00.00–30:00.47、30:01.80–30:03.30（放大） | debc03aa8129 | **只有 Reforged 6.85k 画面，没找到 6.83d 经典画质的清楚画面** ⚠️。**XH**：沙王（浅色蝎子）在野区打一群萨特（Satyr Soulstealer / Hellcaller），被打的萨特身上冒出**亮绿色的点状酸液飞溅**（30:00.13–30:00.47，疑似毒液上身 ⚠️）；萨特接连死亡（头顶金币 +17 / +31 / +85）后，尸体处腾起一团**浑浊的黄绿色毒气云**，翻滚约 1.5 秒（30:01.80–30:03.30），颜色与旁边沙王遁地扬起的土黄尘雾明显不同（更绿、更暗）。没有看到明显的「炸开」火光或冲击环，像是一团毒雾喷出。**由于是 6.85k 改图 + Reforged 高清特效，经典 6.83d 的外观未亲眼看到** |

## 地图数据（DotA 6.83d 官方地图解包）

地图同 `0_research/base_layout_refs/DotA_v6.83d.w3x`（sha `326d7ea8fb2b`），用的是 c60 那次已解出的 `Units\*.slk` 与 `*Func.txt / *Strings.txt`（`.audit/adhoc_agents/2026-10-24/ck-research/map/`）。

- 英雄单位 `U00K`「Sand King」/ Crixalis：模型 `Units\Creeps\ArchnathidGreen\ArchnathidGreen`（绿色蛛形蝎虫），`scale` 1.85、`modelScale` 1，不染色；音效集 `CryptFiend`；武器音效 `WoodHeavyBash`。英雄技能栏 `A06R, A0H0, A06O, A0FA, Aamk`。
- **腐蚀之终 `A0FA`**：被动，图标 `PASBTNPoisonSting`；没有 `Missileart`。地图文本「Each of the Sand King's attacks injects a deadly venom that causes the target to explode violently on death, dealing damage in an area」，1–4 级爆炸伤害 90 / 130 / 170 / 220。英雄说明里写「condemned to violently burst apart in a cloud of noxious fumes」（在一团有毒烟雾中猛然炸开）。
- buff `B03F`（`Bufftip=Caustic Finale`，「This unit will explode on death」）：`Targetart=Abilities\Spells\Other\AcidBomb\BottleImpact.mdl`（WC3 炼金术士酸性炸弹的命中特效，绿色酸液飞溅），`SpecialArt=Abilities\Spells\Undead\PlagueCloud\PlagueCloudCaster.mdl`（WC3 憎恶「疫病云」的施放特效，黄绿色毒雾）。这与 XH 里「被打的萨特冒绿色酸液 → 死后腾起黄绿毒气云」吻合。**脚本里死亡爆炸到底播哪一个特效没有逐行追到** ⚠️（表数据确定，触发路径未核实）。
- **地震 `A06R`**：图标 `BTNEarthquake`；`Effectart=Abilities\Spells\Orc\EarthQuake\EarthQuakeTarget.mdl`（WC3 先知「地震」的地面特效）；`Animnames=spell,looping`（施法时播施法动作并循环，即引导期间一直在做施法动作）。地图说明「Summons up the power of the earth, causing it to shudder violently… 2 second casting time」，1–3 级 6 / 8 / 10 次脉冲、每次 110 伤害，减速 30% 移动 / 30% 攻速 4 秒，冷却 140 / 120 / 100 秒。**画面里那一圈圈的黄色光环用的是哪个模型没有从脚本里查到** ⚠️。

## 结论（据图 + 数据）

1. **地震（k754）**：DotA 1 原版的样子是**以沙王为中心、一圈接一圈向外扩的亮黄（偏柠檬绿）粗光环**，带放射状条纹，环内半透明黄雾，常同时有 2–3 圈同心环，范围很大；两部 6.83d 经典录像（MW、TS）都清楚看到，v6.81d 封面和版本不明的 SG 也一样。引导期 2 秒、施法动作循环（数据），画面里没拍到引导的样子。Reforged 6.85k 的光环偏金棕、较暗，并带背部绿色闪光，不作为原版依据。
2. **腐蚀之终（k753）**：数据确定是「被打的单位中毒 → 死亡时炸成一团有毒烟雾、伤害周围」，表里挂的特效是 WC3 的绿色酸液飞溅和黄绿疫病云。画面只在 Reforged 6.85k 里看到（萨特身上冒绿色酸液、死后腾起黄绿毒气云）；**经典 6.83d 画质没有找到清楚的画面**，经典外观是推断（同一套 WC3 特效文件）⚠️。

## 未核实与限制

- 腐蚀之终：经典画质无原图。看过的经典录像（TS、MW、SG、ylb4 等）远景下小兵只有十几个像素，死时是否有毒雾认不出来；按颜色扫描找到的几处黄绿色亮团经放大核对都是别的东西（天灾 / 近卫建筑特效、其他英雄的投射物），没用。
- 地震：引导动作没拍到；光环所用模型没从脚本里查到；SG 的版本没读出。
- 声音：本次没有逐段听辨录像音轨，两个技能的声音**都没有用耳朵取证** ⚠️。
