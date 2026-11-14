# m4 食尸鬼：死亡动作样板筹划

2026-10-22 · follow-up 059–065。**研究与姿态候选图阶段；已出起始候选与倒地末姿概念，未提交死亡视频、未获用户选定。**

**068 当前**：用户认可 067 四张图，转正式 `m4_Ghoul_death_{1fall,2corpse,3decay,4bones}.png`（拼图 `m4_Ghoul_death_sequence.png`）。死亡视频 `renders/20261022-203838_568d98d0/m4_Ghoul_death.mp4` sha `727732580cd2`（720p · 14.08 s · Seedance 2.5 · 参考四张正式图 · prompt `m4_Ghoul_death_video_prompt.txt` · submit `568d98d0`，252 积分；请求见 `characters/request_log.md`）。代理看片：2.2 s 起往后仰面摔倒、扬尘、仰躺，长爪蜷到胸前，4–10 s 皮肉干裂剥落露骨，约 11 s 成白骨，最后约 3 s 定格，机位不动，和四张图一致；不血腥。偏差：**0–2.2 s 是另一个机位**（中景、天空地平线、食尸鬼半直立后仰），2.2 s 处硬切到正式机位（prompt 要一个连续镜头）；开头那只姿态偏直立、不够佝偻。有音轨（均值 −28 dB），未逐声核听。待用户看片。

**069 4 秒版**（用户：死亡视频压缩成 4 秒）：`renders/20261022-203838_568d98d0/m4_Ghoul_death_4s.mp4` sha `26195d7bed5f`（4.02 s · 720p · 24fps）。本地 ffmpeg 变速剪辑，不调服务：去掉 0–2.22 s 另一机位的开头（硬切那段）；2.22–3.82 s 摔倒落地 ×1.33 → 1.2 s，3.82–11.52 s 腐烂 ×3.85 → 2.0 s，11.52–14.08 s 白骨定格 ×3.2 → 0.8 s；音轨同比 atempo，末尾 0.3 s 淡出。代理看片：一个机位到底，摔倒 → 仰躺 → 露骨 → 白骨连贯。

**067（用户 2026-10-22 定方向）**：死亡改为**受击后仰面往后倒 → 仰躺尸体 → 皮肉干缩剥落、露出骨头 → 只剩一副白骨**（对应 WC3 单位 Death → Decay Flesh → Decay Bone；重制版实机 `ref/reforged_death_066/` 也是往后翻倒、皮肉褪尽剩骨架，见 [ref/refs.md](ref/refs.md#follow-up-067-补充参考)）。065 的趴倒末姿概念作废。Codex 出了一组同机位 4 张关键图（干土地面、低机位三分之四侧、16:9），代理看图通过，待用户看：

| 序 | 文件 | 画面 | 代理看图 |
|---|---|---|---|
| 1 | `frames/m4_Ghoul_death_067_1fall_v1.png` | 往后摔：头甩后、下巴大张，两臂甩上天，脚下扬尘 | 读得出后仰倒；身体已接近落地（不是 45° 半空），左手只看得见 2 根爪 |
| 2 | `frames/m4_Ghoul_death_067_2corpse_v1.png` | 仰躺尸体：头后仰、下巴朝天张着，长爪蜷扣在胸前，腿软倒一侧 | 通过 |
| 3 | `frames/m4_Ghoul_death_067_3decay_v1.png` | 半腐：皮干裂剥落成碎屑，露肋骨、膝骨、腿骨，黑毛变稀 | 通过，与 2 同机位同姿势 |
| 4 | `frames/m4_Ghoul_death_067_4bones_v1.png` | 白骨：完整骨架仰躺，大下巴整排牙、背骨刺、三根爪骨，腕上残布 | 通过；头部黑毛仍偏多，脚爪骨多于 3 |

四张拼图 `frames/m4_Ghoul_death_067_sequence_contact.png`；prompt 在同目录 `*_067_*_prompt.txt`；SHA 见 `frames/codex_frames_manifest.json`。视频未出（用户点）。

**065（已作废方向）**：用户指定 Codex imagegen，已经共用入口实际出图。起始v1手爪偏多退回，v2只修手部，每手三根主要长骨爪；另出一张小兵趴倒留体的末姿构图候选，供用户看姿态。完整俯卧是本剧电影化创作选择，不宣称原版翻转／分体的准确终态，也不恢复旧8秒侧倒时间轴。末姿一侧后脚被遮挡、背部轮廓需在最终动作核对，暂不称定稿。文件与SHA见 [图片清单](frames/codex_frames_manifest.json)，实际prompt在同目录；图像型号和费用工具未暴露。原立绘与建立视频未覆盖。

**follow-up 060 修订：食尸鬼 m4 是兵线小兵，英雄与小兵死亡分开研究和制作。此前“8秒电影化通用侧倒”已撤回默认方案，相关时间轴和提示词仅保留为未采用草稿，不得作为当前生成输入。**

**063 实际制作状态**：已尝试提交小兵待机起始候选帧（不沿用旧侧倒末态）。ElevenLabs只返回 HTTP 100 中间响应，无终态或任务号，提交结果未知；查询最近任务后下载核对的候选是其他角色，已排除并移至审计目录。没有本次图片、视频或后台任务，不重复付费请求。完整提示词和状态见 `frames/m4_Ghoul_death_start_v1_prompt.txt`、`frames/m4_Ghoul_death_start_v1_status.json`；请求留痕在 `characters/request_log.md`。原版单体 Death 取证仍未完成。

## 目的与范围

对照全剧 Vision：沿用当前真人电影化食尸鬼的身份与材质，处理已知爪数偏差；动作有重量，长爪、骨刺和大下巴保持辨识，死亡结果能在战斗镜头中读清。先做 m4 兵线小兵自身的死亡动作，验证参考→出图→出视频的方法，再分别研究其他单位；不把 m4 动作推广为英雄死亡模板。

死亡动作独立于已有建立视频，不覆盖人物立绘、声音或技能素材。既有卡说的“不做 demo”指不做英雄四技能展示，不妨碍制作本动作资产。

## 研究结论与证据边界

| 判断 | 状态与依据 |
|---|---|
| m4 是天灾近战兵 `ugho`，用 WC3 经典 `units\\undead\\Ghoul\\Ghoul` 模型 | 既有地图取证，见人物卡与 `0_research/parts/d01_版本与地图.md` §4；不是 Dota 2 兵，也不是英雄 c70 |
| 自有造型参考已经存在，仍有已知偏差 | 当前 `../m4_Ghoul.png`；干黄皮、黑毛、大下巴、背骨刺、无兵器。卡要求每手三爪，但现图4–5爪，需在首帧校正并验收；不称完全定稿。生成只挂本剧自有图，不挂游戏图 |
| 已取得经典画面风格的实机参考 | 视频 `Mountain King vs 50 ghouls`，YouTube `JKYKzjkfRrk`，62 秒；研究原片放本次 `.audit/`。保存 35/40/45/50 秒四张完整帧，44.00–47.75 秒每 0.25 秒抽一张，共 20 张；来源、限制与哈希见 [ref/refs.md](ref/refs.md) |
| 实机中可见死亡后的平摊残骸 | 已看战斗概览、44 秒段拼图和45秒完整帧。群战遮挡、分辨率与后期阶段混杂，只支持“会倒下并留下残骸”的粗粒度观察 |
| 经典死亡是否包含翻转、分体，顺序和时长是什么 | **未完成直接取证**。社区讨论有此说法，但当前片段不足以跟踪同一只单位的完整相位；不能将其写成已核实的 m4 动作。需要经典模型 Death 独立播放或清晰单体实机片段 |
| 三个模型库候选是否可用 | 13895 外观接近经典，但身份及动画未核实，预览实际为挥爪攻击；8665 改色改爪、100402 带甲，退回。不能因文件名叫 Ghoul 就采用 |

逐条来源和退回原因在 [ref/refs.md](ref/refs.md)。网上普通站姿图不是死亡动作证据；20 张抽帧来自同一片段，不是20个不同动作或机位。

## 全角色如何扩展

**先按单位身份分流，再按身体结构研究。** 英雄、小兵、野怪、召唤物和其他 NPC 分别登记；“非英雄”不等于“小兵”，相同模型也不代表相同死亡机制。m4 小兵与同模型的 c70 噬魂鬼英雄尤其不能混用。其余非英雄类别待逐卡核对。

全剧当前183张人物主体卡（112英雄、71小兵／野怪／召唤物／商人）登记在 [死亡资产待办](../../../death_assets.json)。这只是本轮清点，不改变资产编号。换形态、坐骑与合体单位后续逐卡核对，不拿183当最终视频总数。

| 动作族 | 筹划时必须另看什么 |
|---|---|
| 有机地面角色 | 重心失去支撑、接地顺序、武器落点、倒地后的身体空间 |
| 飞行、游动、骑乘与多人组合 | 落点和载具／坐骑／成员分别如何结束，不能一律套人形侧倒 |
| 机械、构装、元素、幽灵与召唤物 | 按角色取证破坏、散落或消散；不自动加爆炸或光效 |

每个角色先锁当前造型，再做参考 → 关键图 → 视频 → 看图／试听／用户选定。119张仍待重出立绘的角色先不做死亡图，避免刚出完动作又因外观重做。

## 当前方向：m4 兵线小兵死亡

1. 参考锁定 DotA 1 / 6.83d 的天灾近战兵 `ugho`；超级兵 `u001` 单独检查缩放与动作复用条件。排除 c70 英雄、Dota 2 兵和重制模型。
2. 找同一只小兵的连续受击／死亡／落地参考，分别记录 `Death` 与之后的尸体状态。后续尸体衰减、清理或技能作用另记，不把它们当成死亡动作的最后一拍。
3. m4 以小兵死亡后留下地面遗体的方向筹划，不添加英雄消散、灵魂离体或复活演出；尸体具体轮廓、是否翻转或分体、实际时间仍待本模型直接证据。不能因有残骸就假定完整侧卧是原版终帧。
4. 先按原版小兵动作确定起止姿态，再编首尾关键图；动作时长从参考量取。此前8秒只是样片设想，已不作为动作时长或片长默认值。静止尾段可为剪辑保留，不能把死亡本体拖长成角色告别表演。
5. 英雄单开研究：查各自模型死亡与死亡后的处理。暴雪 WC3 基础规则明确英雄不留下普通尸体；这只能证明分类有别，不能替代 DotA 6.83d 对具体英雄的核实，更不能反推 m4 应有英雄消散。

来源见 [本轮分类复核](ref/refs.md#小兵与英雄的分类复核follow-up-060)。本轮未获得新的单体死亡视频，也未修改已下载参考帧。

## 已撤回默认方案：电影化通用侧倒（仅留草稿）

**未采用草稿，不用于当前出图／视频。** 以下保留 follow-up 059 的电影化设想供追溯；060 之后先按小兵原版 Death 证据重写，不能将本草稿称为已选动作。

- 画幅：16:9，拟8秒；固定机位，略高于腰部的三分之四侧前视角，全身与全部长爪始终入画，四周留足倒地空间。
- 场地：与现有立绘相容的中性灰摄影棚和可辨的灰色地面，有接触阴影；不先绑定 bg5 等战场。它是动作母版，不声称灰底可以自动抠出透明通道。
- 开始：已处于战斗后的濒死失衡阶段，身体伏低。动作资产不自带攻击者；用进战斗镜头前，必须在上游补可见命中和方向衔接。
- 结束：右侧卧，头、躯干和腿都有真实支点，长爪松开落地；最后2秒完全静止，不再抬头、撑起或循环回站姿。

| 拟定时间 | 可见动作 | 关注点 |
|---|---|---|
| 0.0–0.8秒 | 低伏姿势短暂支撑，重心不稳 | 首帧能接现有人物，不能先躺好 |
| 0.8–1.5秒 | 右前臂屈曲，肩线和头一起下沉，后腿收软 | 先失去支撑，再发生位移；不跳、不飞 |
| 1.5–3.0秒 | 重心向右落，右侧躯干接地，长爪沿地面滑出少量距离，双腿屈曲跟落 | 有落地重量；爪、骨刺不穿身或穿地 |
| 3.0–5.5秒 | 头与四肢有一次小幅惯性落定，布条回落 | 余动来自刚才落地，不反复抽动或继续呼吸表演 |
| 5.5–8.0秒 | 身体保持原位静止 | 提供可剪的落地静止段；终帧不换脸换体型 |

不是被雷劈、烧毁、冻结、斧劈或吞噬的通用替代：那些在对应技能镜头里另做。普通死亡、残骸腐化、游戏清理消失也分开，不在这8秒中捆成一套。

## 下一阶段：先出两张关键图

**当前只保留“先图后视频”的顺序。下方侧倒终帧和英文提示词随旧方案暂停，需用小兵动作证据重写后才可提交。**

造型衔接有一个已知问题：现有立绘的生成记录承认每手4–5爪，原卡要求3爪；本轮重新打开立绘也能看到多爪。因此它是身份与材质参考，不能把“原图已经三爪且完全定稿”当成事实。下一阶段首帧需单独校正为每手三根长骨爪并看图验收；已有建立视频也应核对是否需同步。这是计划中的外观修正，尚未改原立绘或既有视频。

| 文件（拟） | 内容 | 生成输入 |
|---|---|---|
| `frames/m4_Ghoul_death_start.png` | 原角色、16:9、单体全身、低伏支撑、三分之四侧前视角 | 当前自有 `../m4_Ghoul.png` |
| `frames/m4_Ghoul_death_end.png` | 同机位、同体型、同光线，完整身体右侧卧且完全入画 | 已选 start 图加当前自有立绘 |

不先做每0.5秒一张的独立生成图：独立生成会漂造型，运动也不能靠静图张数证明。先验收开始和结束姿势，确有需要再加一张中间失衡图。

关键图验收：仍是当前 m4；每手三爪；头骨脸、毛发和骨刺不变；没有刀和新增服装；没有分身、多肢、缺肢、悬空或穿地；起终帧机位和光线一致；终态一眼读成动作结束，不像睡觉、撑地或准备爬起。

### 首帧图提示词草案

只上传本剧自有立绘。原名、游戏名与网页参考不进入生成请求。以下待参考缺口与方向确认后使用，不是已提交请求。

```text
Create a single full-body film creature reference frame, using the supplied production character image as the identity and material reference. Keep one emaciated, deeply hunched practical-effects fantasy creature: dry ochre skin, dark rib-like markings, rough black hair, a broad projecting jaw with exposed large teeth and pale bony back spines. Correct the source image's extra hand claws: each hand must have exactly three long curved bone claws, no additional claw-bearing digits. No handheld weapons. A fixed three-quarter front-side camera, neutral gray studio backdrop and a visible matte gray floor, soft cinematic light and grounded contact shadows. The creature is low on all fours, struggling to support its weight, with the complete body, both feet and every claw visible. Reserve generous empty floor space for a fall toward its right side. Photoreal materials and film-quality creature effects. One image, no grid, labels, text, UI, logos, extra creatures or added body parts.
```

### 终帧图提示词草案

```text
Use the supplied production creature and approved start frame. Keep the exact same single creature, body proportions, three long claws per hand, back spines, skin, hair, framing, floor and lighting. Show the end of a non-graphic death-action performance: the complete intact body is motionless on its right side, the torso fully resting on the floor, legs folded naturally, head supported by the floor, forearms and long claws relaxed in front. The pose has no active arm support and no intention to stand. Maintain believable weight and floor contact, with all extremities inside the frame. No blood, open wounds, detached parts, magical effects, smoke, extra subjects, text, UI or camera change. This is one final full-body frame, not a sequence or collage.
```

## 再出视频

**此节的8秒、侧倒和声音节奏属于暂停草稿；提交前依小兵原版 Death 重编，不能直接沿用。**

预定成品选择路径 `m4_Ghoul_death.mp4`；原始条保存在 `renders/<时间与任务号>/`，不覆盖旧条。拟16:9、8秒、先720p样片，参数在提交时按实际服务能力和费用核对。

使用已选自有 start/end 图；是否走首尾帧模式、或全能参考模式，在图片定稿后按实际接口确定。两张图表达同一角色两个时刻，不表达两只角色。第三方游戏图和本次原视频不上传。

视频提示词采用上表时间轴：只发生一次失去支撑与侧倒，固定机位、保持单体身份，最后2秒完全静止。不把建立视频 "Must feed!" 或啃食声接到死亡上；无台词、无旁白、无背景音乐，只留本剧自有的短促低沉断气声、身体接地闷响和布料／爪擦地声，终段归静。

验收看实际逐帧与试听：全程仅一只；没有新武器、换造型、翻面变另一角色、抖动变形、穿地或爪数漂移；重心与接地合理，死亡终态不复活；无多余台词和音乐。失败保留版本和原因，修参考／动作描述，不盲重提。

## 当前交接

- 已做：登记全角色需求；下载和筛选参考；从实机片段抽帧；写制作筹划；按用户指定用Codex生成起始候选v1、修手v2与小兵倒地末姿概念，主代理逐图看过，候选待用户看图。
- 待证：经典模型单体 Death 完整相位、是否采用翻转／分体，以及最后姿势。
- 当前路线：按 m4 兵线小兵补原版单体动作证据，再做真人电影化改编；英雄另行筹划，旧通用侧倒方案已撤回默认。
- 未做：关键图选定与死亡动作定稿、视频提交、死亡声音生成、独立成片审核与用户选条。现有建立视频不受影响。
