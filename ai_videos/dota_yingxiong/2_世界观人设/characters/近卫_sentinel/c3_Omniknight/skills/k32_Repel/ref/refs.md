# k32 驱逐 Repel · 参考研究（follow-up 087）

> 暴雪娱乐 / Valve / IceFrog / 各 YouTube 作者的版权素材，**只作人眼研究**：不进成片、不上传任何生成服务、不挂进「视频参考」。2026-10-23 下载，全部经留痕脚本（图片 `RequestLog.download`，视频 `yt-dlp` 经 `RequestLog.invoke`），日志在 `characters/request_log.md`（provider `web_reference` / `youtube`）。免费公开页面，未调用收费服务。
> 整段视频只在本机临时用来截帧，截完挪出资产目录（不入库）；入库的是 `research_087/` 下的拼图与单帧。sha256 取前 12 位。
> 另：PlayDotA 6.x 全能骑士页（`https://web.archive.org/web/2014id_/http://www.playdota.com/heroes/omniknight`）只抓文字读数值，未存档进仓库。

## 一、原典数值（6.83 前后的 DotA 1，PlayDotA 存档页）

- 说明原文："Creates a powerful divine ward that blocks most magic from affecting a target unit."
- 1–4 级：耗魔 50、冷却 14 s、施法距离 500、持续 **6 / 8 / 10 / 12 s**，效果 **Grants Spell Immunity**（魔法免疫）。施法动作 0.5 s。
- Notes：**"Repel removes most effects from the target when cast, including Guardian Angel."**——施放瞬间**驱散**目标身上大部分效果。"Magic Immunity doesn't prevent side effects of most ultimates."
- 英雄介绍："make a target ally immune to most spells for an extended period of time"。目标栏写 "Any unit" ⚠️（介绍说给友军；对敌施放用来驱散增益在 Dota 2 旧版有教学视频 `Sg92urKtymk`，DotA 1 是否可对敌未实机取证）。
- 换算（按 1 单位 ≈ 2 cm 放大换算）：施法距离 500 → 约 10 m。本卡 demo 取约 7 m，在射程内。

## 二、逐份参考

| 文件（`research_087/`） | 来源 URL | sha256 | 看到了什么 |
|---|---|---|---|
| `dota1_wEM2tnIkVBc_repel_on_creep_15.8-18s.png`（6 帧特写；同行原有 `dota1_wEM2tnIkVBc_omni_skills_11.5-20.5s.png`（36 帧），follow-up 316 用户定「一切以 dota1 为准」已整张删除：第一格右缘露出对照片另半屏的灰边，且源片本身是 DotA 1 / Dota 2 同屏对照片；本地纯 DotA 1 全能片 `vhARz5CpDbA` 里只认出洗礼与守护天使，没找到驱逐，只删不补） | YouTube「Dota 2 VS Dota 1 Hero Skills Showcase Part 1」https://www.youtube.com/watch?v=wEM2tnIkVBc 章节 OmniKnight 1:14–1:33（只下这一段，源 sha `dfba3c539cbe`） | `1c563caa9b64`（`98b4704b2bda` 已删） | **DotA 1 实机（WC3 引擎）**：右半屏 Purist 先对一处放洗礼（竖直光柱），随后约 16–18 s 一个近卫小兵（红色队伍色的树人群中）身上出现**驱逐的 WC3「神圣护盾」特效**：一团**黄金色、半透明、球状**的光团把整只单位包住，直径约单位身高的 1.3–1.5 倍，球面上是旋转流动的细碎金丝与亮点，持续数秒不灭、跟着单位走；单位本身颜色不变。只裁了 WC3 半屏（follow-up 316 看图核对：6 格都是经典 WC3 画面；但源片是同屏对照片，⚠️ 按同一原则是否也要删待用户定）。分辨率低（640 宽、远景），只能读出「金色、球形、半透明、表面流动、持续」，读不出边缘细节。**驱逐在 DotA 1 里本来就常给兵线树人放**——支持本卡 demo 选「给被围的树人施放」。 |
| `yt_wEM2tnIkVBc_omni_sheet.png` | 已删：Dota 2 来源，follow-up 316（同屏对照总览，含 Dota 2 半屏与 Dota 2 头像） | | |
| `yt_gkHfDa7zRDk_sheet.png` | YouTube「Dota - Omniknight pro Repel」https://www.youtube.com/watch?v=gkHfDa7zRDk（源 `a72e15baf81b`） | `8a1874a2e314` | DotA 1 团战录像（640×480，fraps 水印）：画面乱、单位极小；只能看到一处单位身上的黄色球状光团与洗礼光柱，佐证上条，不单独作依据。 |
| `dota2_repel_sheet.png`、`dota2_repel_zoom.png` | 已删：Dota 2 来源，follow-up 316 | | |
| `dota2_martyr_sheet.png` | 已删：Dota 2 来源，follow-up 316 | | |
| `dota2_heavenly_grace_sheet.png` | 已删：Dota 2 来源，follow-up 316 | | |
| `yt__ci1gYw5An0_zoom.png`、`yt__ci1gYw5An0_sheet.png` | 已删：Dota 2 来源，follow-up 316 | | |
| `yt_4B0U8hgXhRY_sheet.png` | 已删：Dota 2 来源，follow-up 316 | | |
| `yt_aZfoxXrtWgg_immune_32-42s.png`、`yt_aZfoxXrtWgg_sheet.png` | 已删：Dota 2 来源，follow-up 316 | | |
| `yt_Sg92urKtymk_sheet.png` | 已删：Dota 2 来源，follow-up 316 | | |
| `yt_9e9FH0jurG8_sheet.png`、`yt_9e9FH0jurG8_bubble_3.6s.png` | YouTube「Paladin, Divine Shield - 2020 08 05」https://www.youtube.com/watch?v=9e9FH0jurG8（12.5 s，同源「神圣护盾」的同人重制特效，源 `49a217fb35f8`） | `adccaa4e0724` / `ca58635258a1` | 圣骑士**把锤举向天** → 头顶一颗星点闪亮、一束极淡的光尘落下 → 身周凝成一个**透明泡泡**：**里面完全透明、只有边缘一圈亮金色的细边（菲涅尔反光）**，泡壁上几粒金色光尘，脚边扬起一圈金色尘雾。这是「真实的光罩」最可信的样子：**看得见的只有边缘与光尘，人物本身不发光**。 |
| `yt_Q_U3DrCV_C4_sheet.png`、`yt_Q_U3DrCV_C4_4.8s.png` | YouTube「Paladin - Divine Shield」https://www.youtube.com/watch?v=Q_U3DrCV_C4（11.6 s，魔兽世界，源 `1b7ca6347079`） | `3badc53ecc2d` / `29f5cd202dec` | 魔兽世界的同名护盾：施放时一团橙金光爆开，之后是一圈带放射状光芒的橙金泡泡，持续约 8 s 后一下消失。比 WC3 版更「游戏特效」，**只取：施放先爆一下、之后是包住全身的泡、人在里面清楚可见**。 |
| `wowpedia_Divine_Shield_WoW.jpg` | https://static.wikia.nocookie.net/wowpedia/images/4/42/Divine_Shield_WoW.jpg（页面 https://wowpedia.fandom.com/wiki/Divine_Shield） | `f2889a504e06` | 魔兽世界护盾静帧：人物外一圈约 1.6 倍身高的椭圆泡，边缘亮、放射状金粉光芒，里面透明。泡面有明显亮边与内侧暗。 |
| `wowpedia_BTNDivineIntervention.png` | https://static.wikia.nocookie.net/wowpedia/images/e/ec/BTNDivineIntervention.png | `56e22233f951` | WC3「神圣护盾」按钮图标：一只铁手套**把战锤举向天**，锤头放出白金光。施法姿势参考：举锤 / 竖锤。 |
| `dota2wiki_Repel_icon.png`、`dota2wiki_Heavenly_Grace_icon.png` | 已删：Dota 2 来源，follow-up 316 | | |
| （既有）`../icon/k32_icon_dota1.png` | PlayDotA 存档（见 `icon/refs.md`） | `ed3a3e8e4ee3` | DotA 1 图标：一面圆形金盾、红十字、四周放射金光——「一道神圣的屏障」。 |

**下载了但退回**（只记日志，不留截图）：`RTonUPynngw`（标题「Divine Shield」，实为《风暴英雄》对局）、`zV2cGPEYwVA`（魔兽世界玩笑剪辑）、`d3_TB9pZE3s`（WC3 对战录像，单位太小看不清护盾）。

## 三、结论 → 怎么影响 prompt

1. **机制是「驱散 + 魔法免疫」，最好读的是驱散**：Dota 2 三版演示都是「目标身上先有一个看得见的负面效果（减速绿圈 / 绿毒 / 缴械）→ 施法白金光一闪 → 负面效果消失」。DotA 1 原文也写明施放即驱散。→ demo 先交代负面效果，再一闪驱散，这是「施法 → 效果 → 结果」的主轴；免疫再用一次「同样的东西又打上来、这回沾不上」作对照（`aZfoxXrtWgg` 那段）。
2. **光罩的真实样子是透明泡、只看得见边与光尘，人不发光**：DotA 1 是半透明金球；同源重制版与魔兽世界都是「里面透明、边缘一圈亮边、几粒光尘」。旧片的毛病正相反（人整个镀金描边、像贴纸）。→ 本卡锁定：一层顺着身形、离身约 30 cm 的**长卵形透明光膜**，正面几乎看不见，只有轮廓边缘一线细金反光与少量光尘；被碰到的那一点才亮出一小圈涟漪。被罩的人/树本身颜色不变、不描边。贴身（不做 DotA 1 那种大球）是本剧取舍：大球在真人画面里像游戏 UI，且会挡住打斗。
3. **施法动作**：WC3 图标与 Dota 2 旧版都是「举锤 / 竖锤」起手。→ 保留「战锤竖在胸前、低头」，加一个**左手伸向目标**的指向动作（友军施放要读得出是给谁的），0.5 s 内完成（原典施法动作 0.5 s）。
4. **一闪是真实光源**：所有版本施放瞬间都有一团比环境亮得多的白金光（Dota 2 甚至从天上落一束）。→ 一闪从**目标自己身体里**透出（像树干里点亮一盏灯，从树皮裂缝漏光），照亮旁边的食尸鬼脸、地面和骑士侧面；不加天上光柱（与 k31 洗礼的天降光柱区分开）。
5. **持续与收尾**：原典 6–12 s；Dota 2 演示里常驻效果很淡。→ 镜头内一直在但很淡，结尾 2 s 内从下往上淡去。

## 四、为什么选「给被围的树人施放」，以及怎么在只有树人、食尸鬼时演清楚

- 用户新规则：小兵只能是树人或食尸鬼；食尸鬼没有法术，场上没有「魔法弹」可挡。旧片靠亡灵法师打暗影弹，必须拿掉。
- 能演的只剩**驱散**（施放瞬间把负面效果赶出去）和**免疫**（之后同类负面效果沾不上）。食尸鬼的爪子是腐尸爪，爪上带乌黑的腐泥；抓进树皮的伤口里，腐斑像墨一样往外爬、叶子卷黑——这是看得见的「负面效果」（创作设定：原版食尸鬼爪无毒，这里只当作视觉化的负面状态，不写成新技能）。
- 演法：① 树人被两只食尸鬼抓得单膝跪地、伤口腐斑扩散；② 骑士竖锤、伸手指向树人，说台词；③ 暖金光从树人体内透出一闪，腐斑冒黑烟、碎成黑灰被逼出来，叶子回绿，树人站起，身外留一层透明光膜；④ 一只食尸鬼再扑，沾着腐泥的骨爪碰到光膜，那一点亮一圈金涟漪、腐泥嘶地烧成一缕黑烟——**腐斑不再沾上**（免疫），但爪尖照样在树皮上刮下木屑（只挡魔法、不挡物理，符合原典）；⑤ 骑士冲上去一锤、树人一臂，两只食尸鬼都往后仰面倒下，按 `m4` 死亡参考倒地即烂成白骨。
- 不选「骑士对自己施放后冲进食尸鬼群」：骑士钢甲上演不出「腐斑被逼出来」，只剩冲锋砍杀，看不出技能做了什么；而且 DotA 1 实机正是给树人小兵放（第一条参考）。代价：k31 洗礼也用「被围的树人」，两条靠「天降光柱 + 愈合」与「体内透光 + 腐斑被逼出 + 透明光膜」区分。

## follow-up 093 补充（主代理看图）

- 用户：驱逐是魔法免疫罩子，给自己加就行，不需要食尸鬼。
- 重看 `research_087/dota1_wEM2tnIkVBc_repel_on_creep_15.8-18s.png`：DotA 1 里被驱逐罩住的单位外面是一团**金黄色、半透明、球形、表面有旋纹流动**的光罩，持续数秒，看得很清楚。
- 重看 `research_087/yt_9e9FH0jurG8_bubble_3.6s.png`（神圣护盾重制风格）：**透明大泡、边缘一圈清楚的金色亮边、四周飘金色火星**，里面的人看得清。
- 结论：087 版写的「几乎看不见、贴身 30 cm 的薄膜」太弱，改为一眼看得见的透明金边大泡；只对自己施放，画面只有骑士一人。

## follow-up 098 补充（主代理看图）

- 用户：施法也是举锤、快一点、不用台词；罩子再厚、再圆，是圆形的罩子，多看 ref。
- 已删：Dota 2 来源，follow-up 316（原 `dota2_repel_zoom.png`）
- 重看 `research_087/dota1_wEM2tnIkVBc_repel_on_creep_15.8-18s.png`（DotA 1）：金黄色球形光罩，表面旋纹流动。
- 结论：093 版的竖长薄泡改为**正圆、厚壁（半透明金色琉璃感）、粗亮金边、表面光纹流动、外绕三道旋转光带**的球罩；施法压到 1 秒内，天光落下即成罩。

## follow-up 316 补充（2026-11-01，严格 DotA 1）

- 用户：不要任何 Dota 2 参考，借鉴过 Dota 2 的删掉重出。本文件第三节结论 1、3、4、5 中以 Dota 2 演示为依据的部分（天降金光、驱散的「绿圈 / 绿毒」演示、「Dota 2 甚至从天上落一束」）与「follow-up 098 补充」的 Dota 2 球罩 + 陀螺仪光带，**作废**。
- 现行依据只剩：DotA 1 实机 `dota1_wEM2tnIkVBc_repel_on_creep_15.8-18s.png`（金黄、半透明、球状、球面细碎金丝旋转流动、直径约单位身高 1.3–1.5 倍、单位颜色不变、跟着走）、`yt_gkHfDa7zRDk_sheet.png`（佐证）、WC3 按钮图标 `wowpedia_BTNDivineIntervention.png`（举锤向天起手）。
- 卡已改：去掉天光落下、琉璃罩粗金边、罩外光带与符文环（符文环是用户 103 / 109 选的，按 316 去掉，待用户确认）。
- 另：`yt_9e9FH0jurG8_*`（同人重制）与 `yt_Q_U3DrCV_C4_*`、`wowpedia_Divine_Shield_WoW.jpg`（魔兽世界）不是 Dota 2，按本次范围未删，但也不是 DotA 1 / WC3 原版，现行卡不以它们为依据。
