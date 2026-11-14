# m4 死亡动作研究：参考来源与筛选

2026-10-22 · follow-up 059。第三方素材只作人眼研究，不进成片、不上传生成服务。当前角色造型以 `../../m4_Ghoul.png` 为准；既有原版外观依据见 `../../ref/model/refs.md`。

## 已实际观看的材料

| 参考 | 来源 | 实际所见 | 使用范围 |
|---|---|---|---|
| `identity-contact.png` | 本地拼接当前自有立绘与已有经典模型、侧面缩略图、旧动图；原文件不变 | 现有人物保留了大下巴、黑毛、骨刺和长爪。缩略图带真人主播和文字；游戏图带队伍色 | 造型对账，不是死亡证据；不能整张上传生成 |
| `candidate_ninja_13895_still.webp`、`candidate_ninja_13895_anim.webp` | [模型库13895](https://wc3.ninja/models/13895)，图片直链及 SHA 见 `download_manifest.json` | 外形接近经典食尸鬼；已查看动图第0/5/10/16帧，实际是挥爪攻击的循环，17帧 | 仅作外形和活动肢体轮廓参考；原模型身份未核，不证明 Death |
| `candidate_ninja_8665_still.webp`、对应 anim | [模型库8665](https://wc3.ninja/models/8665) | 静态图灰皮、长直尖爪，明显改模／改色；未逐帧审动图 | **退回**，不作为 m4 的标准形象或死亡样板 |
| `candidate_ninja_100402_still.webp`、对应 anim | [模型库100402](https://wc3.ninja/models/100402) | 静态图是带肩甲和衣甲的改模；未逐帧审动图 | **退回**，不是当前 m4 |
| `classic_battlenet_combat_ss041.jpg` | [暴雪经典站：Creeping](https://classic.battle.net/war3/basics/creeping.shtml) | 800×600战斗场景，小单位太小，没有可跟踪的死亡相位 | 不进死亡动作依据 |
| `classic_battlenet_battle_ss027.jpg` | [暴雪经典站：Night Elf Combos](https://classic.battle.net/war3/nightelf/combos.shtml) | 主要是石像鬼群，不能证明食尸鬼如何死 | **退回此研究用途** |
| `classic_battle_net_ghoul.gif` | [暴雪单位页](https://classic.battle.net/war3/undead/units/ghoul.shtml)中的 `images/undead/headers/units-ghoul.gif` | 实际只有187×71、单帧，是网页页眉，不是角色动作 | **退回误图**，不计作有效角色参考 |

`download-candidates-contact.png` 和 `candidate_ninja_13895_motion-contact.png` 是本地查看拼图，不是新的原典图。

## 实机片段与20张抽帧

- 来源：[Mountain King vs 50 ghouls](https://www.youtube.com/watch?v=JKYKzjkfRrk)。yt-dlp实际返回标题、时长62秒；元数据和15.2 MB研究原片保存在本次审计目录 `.audit/adhoc_agents/2026-10-22/dota-ghoul-death-research-20261022/`。没有把原片当成本剧资产或生成输入。
- `gameplay_35000ms.png`、`gameplay_40000ms.png`、`gameplay_45000ms.png`、`gameplay_50000ms.png`：原片35/40/45/50秒的完整画面。
- `gameplay_sequence_44s/frame_01.png`–`frame_16.png`：原片44.00–47.75秒，每0.25秒一张；裁切源画面矩形 `x=470,y=100,w=420,h=360`。未放大成伪高分辨率，未修改动作。`frame_01`对应44.00秒，`frame_16`对应47.75秒。
- 已实际查看 `gameplay-overview-contact.png`、`gameplay_sequence_44s/contact.png`，并打开45秒完整帧。画面是经典风格WC3界面和食尸鬼群，能看到战斗过程中大量残骸平摊地面；44秒段里镜头会跟着战斗移动，裁切没有跟踪某一只个体。
- **不能从这20帧证明**：某一只食尸鬼从待机到死亡的完整动作、独立 Death 动画时间、翻转或分体相位、片段游戏补丁以及模型是否未经修改；也不能把后期残骸直接当作死亡终帧。它是定位线索与落地状态参考，不是原版动作已完全核验。

## 尚缺的直接证据

### 小兵与英雄的分类复核（follow-up 060）

- 用户明确：m4 食尸鬼是小兵，不能采用英雄死亡方案。项目卡记录 m4 为兵线近战兵 `ugho`、超级兵 `u001`；同模型英雄 c70 不是 m4 的死亡参考替身。
- [暴雪 Ghoul 单位页](https://classic.battle.net/war3/undead/units/ghoul.shtml)将 Ghoul 列为普通单位；[暴雪英雄基础页](https://classic.battle.net/war3/basics/heroes.shtml)的 Hero Revival 节明确英雄死亡不留下普通尸体并可复活。[暴雪亡灵基础页](https://classic.battle.net/war3/undead/basics.shtml)说明墓地可提供 Ghoul 尸体。这些是 WC3 基础分类和尸体机制证据，不是 DotA 6.83d 中 m4 独立 Death 的逐帧证据。
- 因此研究分开看“小兵自身死亡 → 地面遗体”和“英雄自身死亡 → 对应后续处理”。不把英雄消散／灵魂表现套给 m4，也不泛化所有非英雄、所有英雄具有相同动作。死亡后的尸体衰减、消失或复活与死亡动作分别记录。
- 本轮通过网页读取官方资料，未新增媒体下载、未提交收费请求；此前 Art Tools PDF 读取失败仍保留，不把搜索摘要升级为已读模型原始证据。

优先补一条原版经典 `Ghoul` 模型的单体 `Death` 播放：准备姿态 → 失衡／翻转 → 接地 → 末帧，每0.1–0.2秒抽图；同一机位连续，无其他单位遮挡，附模型来源或实机版本。`Decay Flesh`、`Decay Bone` 和英雄 `Dissipate` 必须另外标识，不混进 Death。

社区[2026-09讨论](https://www.reddit.com/r/warcraft3/comments/1wrxd1p/a_few_words_about_the_animations_in_the_new/)提到经典版翻转与分体、新版不同；本轮仅作待核线索，未采用为动作事实或时长依据。

## 请求与失败

免费图片和网页下载、视频元数据查询与研究原片下载均经 `tools/service_request.py` 的 `RequestLog`，落在人物集合 `characters/request_log.md`。网页搜索／浏览工具本身不属于本仓库收费服务入口，不伪造为逐HTTP审计。

- wiki.gg页面、Hive部分模型页和wc3.ninja模型详情页403；Hive定点帖子读取超时；MobyGames候选图403。失败保留审计，不将空文件或失败候选计入可用图片。
- Blizzard《Warcraft III Art Tools Documentation》的镜像下载超时；未完成正文提取，因此本轮不拿搜索摘要证明食尸鬼死亡动作。
- `download_manifest.json`记录8个实际下载成功的候选图／动图和1个失败候选；成功不代表通过用途审查。另有1个页眉误图。已有造型图的本地复用和视频抽帧不冒充新的独立网页来源。
- 每份下载图与每张抽帧的大小、哈希、来源或派生时间记录在 [evidence_manifest.json](evidence_manifest.json)。


## follow-up 067 补充参考

用户 2026-10-22 定方向：往后倒下去，慢慢变成白骨。补查网上资料（免费研究；yt-dlp 调用经 `RequestLog` 记在 `characters/request_log.md`，原片放 `.audit/adhoc_agents/2026-10-22/ghoul-death-backfall-decay-066/`，不进成片、不上传生成）。

| 参考 | 来源 | 所见 | 用途 |
|---|---|---|---|
| `reforged_death_066/reforged_ghoul_death_68-78s_contact.png` | [UNDEAD7 - all units and Death - Warcraft 3 Reforged](https://www.youtube.com/watch?v=ouTuMklBG2U) 68–78 s，每 0.5 s 一格 | **重制版**食尸鬼被打死：往后翻倒落地（重制版身体分成两截），随后皮肉褪去只剩一副骨架摊在地上，最后消失（视频可能有剪辑加速） | 证明「倒地 → 尸体 → 白骨」的相位；重制版造型与分体**不照搬** |
| Hive Workshop [animation problems](https://www.hiveworkshop.com/threads/animation-problems.36353)、[dissipate and decay](https://www.hiveworkshop.com/threads/dissipate-and-decay-question.327756) | 论坛 | WC3 单位模型有 Death / Decay Flesh / Decay Bone：Decay Flesh 时骨架露出、皮肉沉入地下，Decay Bone 时骨头慢慢沉下；整个过程论坛称约 90 秒（未独立核实） | 腐烂两段的依据 |
| [Corpse decomposition](https://en.wikipedia.org/wiki/Corpse_decomposition) | 维基百科 | 晚期分解：皮干缩成皮革状、软组织消失，剩骨、干皮、毛发 | 半腐图的写实质感（只取干腐，不取湿腐） |
| [The Mummy（ILM）](https://history.siggraph.org/?p=44787)、[Army of the Dead 腐烂老虎](https://beforesandafters.com/2021/05/31/oh-my-god-are-they-going-to-show-this-oh-my-god-they-showed-it/) | 特效案例 | 电影里腐尸用「皮贴骨、干裂」而非鲜血表现 | 电影化方向：干腐不血腥 |

退回：`s4d0L93Y6tI`（实为《魔兽世界》）、`I25flZkW4Uw`（实为 Dota 2）；`yxWHNVYiKOM`（经典 vs 重制对比）食尸鬼段 3:45–4:18 只有待机和攻击，没有死亡。
