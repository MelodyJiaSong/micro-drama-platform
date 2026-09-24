# changelog · shengji_zhilu（升级之路）

本文件**只追加**（CLAUDE.md § Follow-up prompt handling 第 6 条 + 全流程编排「每次 update 复核」机制）。
每一条记：来源 · 一句话摘要 · 自动更新了哪些文件 · 哪些文件查过但无冲突。

---

## 开工 — 2026-09-19 23:39:07
Source: user_input/raw_prompt.md + follow_ups/202609.md 段 001–002
Summary: 立项一部模拟魔兽世界玩家练级的中文竖屏短剧长系列；阶段 0 设定考据与地理测绘同时开跑。

任务 ID: `shengji_zhilu-20260919-233907` · 审计: `.audit/adhoc_agents/2026-09-19/shengji_zhilu-20260919-233907/`

新建:
- `ai_videos/shengji_zhilu/` — 阶段编号目录骨架（0_research … 5_6_分镜与prompt）
- `specs/ai_video/shengji_zhilu/user_input/{raw_prompt.md, revised_prompt.md, follow_ups/202609.md}`
- `tools/build_world_tree.py` — 地理树渲染器兼闸门
- `ai_videos/_research/wow/parts/w01–w20_*.md` — 20 路设定考据（每路配独立对抗核验员）
- `ai_videos/_research/wow/map/g01–g13_*.{yaml,_notes.md}` — 13 路地理测绘

无冲突: 仓库既有各剧（shikong_lvxing / wushen_juexing / huangye_shenghuo / xianjian_yi / … ）均未被触碰。

## 阶段 0 收口 — 2026-09-20 08:20
Source: 阶段 0 设定考据 + 地理测绘
Summary: 1857 条事实交付（ai_read 1744 / ai_draft 112 / human 1），地理 12/13 片区，两处复发性机制故障已闸门化。

新建:
- `0_research/dossier.md` — 15 节按游戏原典做等价映射（城市志→地理树 / 物价→金币体系 / 节令→玩家文化）
- `0_research/blacklist.md` + `negatives.txt` — 329 行误传黑名单 / 827 条负向词，由 `tools/build_blacklist.py` 生成
- `0_research/map/_dedup_log.md` — 56 个跨片区重复节点的归属裁定
- `tools/build_blacklist.py` — 黑名单合并器

修改:
- `tools/facts_registry.py` — 枚举字段行尾注释剥离。**这是复发性故障的闸门化**：核验员习惯把
  `# 核验修正（…）` 写进 `tag:` / `verified_by:` 的值里，sk2 2026-09-18 踩过并靠手改 10 条收场；
  手改会复发，剥注释不会。blocker 15 → 0，sk1/sk2/sk3 回归干净。

无冲突: sk1 / sk2 / sk3 的事实注册表机检结果与改动前一致。

## 阶段 1 立项 — 2026-09-20 08:40
Source: 0_research/dossier.md + revised_prompt.md
Summary: 剧名《圣光刚好够用》，59 条创作裁定全部拍板（AUTONOMOUS 模式，判断内联留痕）。

新建:
- `1_立项/concept.md` — 立项策划单 + 59 条裁定表 + 第一季 20 集骨架
- `specs/ai_video/shengji_zhilu/divergence.md` — 15 条相对仓库默认的偏离
- `specs/ai_video/shengji_zhilu/pending_user.md` — 6 件需人操作的事 + 6 条最值得复核的裁定

QC: 三件套（主角诉求 / 反派动机 / 长线伏笔）+ 正向立意四项齐全，blocker 0。

## 阶段 2 世界观人设（进行中） — 2026-09-20 09:00
Source: 1_立项/concept.md
Summary: 地基两份已立；18 张角色/图鉴卡与 4 个场景档并行生成中。

新建:
- `2_世界观人设/style_guide.md` — 渲染三档滑杆 / 分区色板 / 情绪运镜映射 / 圣光分级 / 负向锁定基线 22 项 + 7 组条件负向
- `2_世界观人设/world.md` — 双层规则（艾泽拉斯 lore + 这是一款游戏）/ 玩家三件套 / 17 个 bg 代号 / 杜撰边界

判断: 本剧走「自身立绘供脸」而非 `_actors/` 选角库——选角库 205 张全是东亚面孔，
而西方面孔是「一眼认出这是魔兽」的组成部分。已登记 divergence。

## 阶段 2 收口 + 世界树合龙 — 2026-09-20 21:10
Source: 阶段 2 资产工作流（22 agent）+ 阶段 0 补跑工作流（8 agent）
Summary: 18 张卡 + 4 个场景档（20 个 plate）全部过闸门；世界树 1768 节点合龙出树。

新建:
- `2_世界观人设/characters/` — 12 张人物卡（含人物灵魂 12 维）+ 6 张非人形图鉴
- `2_世界观人设/scenes/` — bg1 北郡山谷（世界锚点）/ bg2 修道院 / bg3 回音山矿洞 / bg17 墓地，各含步骤一底图 + 步骤二 walk-through + 5 个 plate
- `2_世界观人设/{casting.md, relationships.md}` — voice_id 总表 + 人物网
- `0_research/map/{world_overview.md, world_tree.md, zones/*.md, world_tree.json}` — 生成物
- `0_research/map/g10_kalimdor_south.{yaml,_notes.md}` — parent 补写（两轮 agent 均失败），全 `ai_draft`
- `0_research/sk2_reuse.md` — 跨系列资产复用审计
- `tools/{check_stage2.py, wow_version_gate.py}` — 阶段 2 契约闸门 + 版本红线闸门

修改（**核验驱动的三处实质修正**）:
- **「北郡河谷」→「北郡山谷」80 处** —— 核验查出这是自造译名，国服 1.12 官方作「北郡山谷」。
  目录 `scenes/bg1_北郡河谷/` 一并改名。
- **艾尔文 `look_zh`：暖金秋色 → 饱和翠绿 + 午后暖斜光** —— 与 C10 裁定冲突。
  **叶子是绿的，「暖」来自光**——色是场景属性、光是分镜属性（16.9），两件事要分开写。
- **`style_guide.md` §2 色板整节重写** —— 核验确认**六区里只有西部荒野的颜色有原文依据**（「草是黄的」），
  其余全是推定；另纠正「赤脊山的赤 ＝ 红岩」查无出处、暮色森林黑雾只有一层。
- **voice_id 统一命名** —— 18 个 agent 并行写出**五套命名法**，已统一为 `zh-{m|f|x}-szzl-{角色}-{NN}`（13 个文件）。
- `tools/build_world_tree.py` — 总览表改为按**直接拥有 zone 的分区**分组；
  初版只看直接子节点，把「暴风王国」连同本剧四个主战场区一起漏掉了。

QC: `check_stage2.py` 18 张卡 blocker 0 / warning 0；`build_world_tree.py` blocker 0；
`facts_registry.py` blocker 0；`wow_version_gate.py` 在 sk2 的 44 镜上零误报。

## 阶段 3 大纲 v1 → v2（双审回修） — 2026-09-20 22:10
Source: 阶段 3 QC 双审（`ai_videos__剧情连贯` + `ai_videos__全剧序列`），26 条 blocker
Summary: 大纲整份重出；三份上游文件同步回写。**大半 blocker 是真原典错误，不是风格分歧。**

最要紧的六条（不改会一路流到 prompt 与成片）:
- **霍格线整条落错地方** —— 通缉告示在**西泉要塞外**不在闪金镇墙上；霍格在**霍格山**不在法戈第矿洞
  （那是狗头人的废弃金矿，归 ep09 罗朱支线）；治安官杜汉是**交付人不是发布者**。
  地点错了，ep05–07 三集的场景资产、动线、previz 全建在错误地基上。
- **ep06 的 hero beat 是个 20 级技能** —— 「三人脚下同时亮起贴地光环」＝**奉献＝20 级**，
  正是本剧自己黑名单点名的画面，而当时主角 7 级。祝福的真实视觉是**目标身上金光一闪**（单体）；
  贴地光环是**虔诚光环**，1 级自带、**只在主角自己脚下**、全剧常驻。
- **ep02 的死亡代价写错原典** —— `"Resurrection sickness limited to ten minutes"` 的 `limited to` 是**封顶不是定额**，
  **10 级及以下完全不吃复活疾病**。改成跑尸 + 10% 耐久，并让他**绕过墓地天使不复活**（省 25% 耐久）——
  这个选择本身就是人物。
- **三个原典 NPC 专名写错，且三条都已躺在本剧自己的误传黑名单里** ——
  治安官玛克布莱德 / 萨缪尔修士 / 治安官杜汉。「费舍尔」在 1857 条事实里**零出处**，
  属于给原典 NPC 凭空安姓。**目录名 `c7_` `c8_` 不动**（导入路由契约）。
- **ep03 三件活的任务归属全错** —— 河东三件活原典里**全是维里副队长发的、全交回维里**；
  大纲让主角没人派活就自己过了桥。补上维里那句原典原话，顺手办了迪菲亚的第一次点名。
- **ep06 两个队友没有入队动机** —— `relationships.md` 自己把这一格列成待办，大纲交上来时仍是空的。
  按两张卡写死的 needs 补：不灭战魂＝**那个前排位置空着而且没人抢**；知无不言＝**终于有人不知道怎么打了**。

其余二十条: ep05 输→ep07 赢的变量不够（补「有人替他挨打，他就念得完」）· ep05 死亡无代价（补断锤 + 全部铜币）·
ep02 豺狼人越界（改成一根不属于狗头人尺寸的粗木棒，反而成了 ep05 的呼应）· L4 落在不可能的角色上
（Vanilla 好友列表按角色存，新号是空的 → 改成冷开场老号）· 尼尔斯修士身份错（他是食物管事，改成**分面包**——
一个 50 级的人在这条谷里干的活是发面包，比整理书架更毒）· ep08 的 9 级接 12 级任务（「慈悲」挪到 ep13）·
F 编号三套并存（长线伏笔整体改号 **L1–L7**）· L3/L4 中段断档 9 集（各补三个零成本触点）·
ep16 与 ep14/15 自相矛盾 · L1 埋点「待定」（钉死在 ep04 S04）· 季度命题没有兑现点（ep19 补不灭战魂那一句）·
**钩尾自检假通过**（只算了 ep01–06 却给全表打勾 → 重排全 20 集，零连续同类）。

同步回写:
- `1_立项/concept.md` — F7 条改写 · B3 的 L2 白名单补第四档「好友列表」· 第一季骨架表 20 行重写 · 新增 F12/F13
- `2_世界观人设/world.md` — bg 台账出现集重排 + **补 bg18–bg22 五个主体**（ep03/ep05–07 实际要拍的地方此前一个都没有）
- `2_世界观人设/relationships.md` — 出谷 ep10→ep03 · 踏雪无痕首次照面口径 · 长线暗桩改 L 号 · 拉尔 ep08→ep13
- `specs/.../divergence.md` — #3 / #10 的 `叠层:` 枚举补「好友列表」

QC: 回修后复审见下一条。`check_stage2.py` 仍 blocker 0 / warning 0。

## 阶段 3 大纲 v2 → v3（复审回修） — 2026-09-20 23:05
Source: 阶段 3 复审（两名核验员独立验收 v2），**5 条未改对 + 15 条回修新引入**
Summary: 首审 26 条改对 21 条；**复审的价值全在第二类——「回修引入的新问题」是首审那一轮看不见的**。

### 回修自己造的三起事故

- **盲的全文替换把「错名」那一侧也替换了**。`c7` 卡的译名负向行变成 `治安官玛克布莱德，中士，…`
  ——**等于在告诉下游把正确的名字挂进每个 shot 的负面词**；`arc_outline` §7 的审计行变成
  「玛克布莱德 → 玛克布莱德」，读不出原来错在哪。
  **已闸门化**：`check_stage2.py` 新增「自负向」检查——卡片自己的正名出现在负向词声明行里即 blocker。
  已回归验证：放回毒行能逮住、还原后零误报。教训是**对必须同时写正名与错名的文件不能跑全局 replace**。
- **「虔诚光环 1 级自带」写错**——原典是 **1 级向训练师学**，而主角 ep01 S07 才第一次见训练师，
  **前六个镜（88 秒）他脚下不可能有光环**；而 divergence #2 把这圈光环定成全片仅有的两个常驻圣骑士记号之一。
  改对之后白捡一拍：**萨缪尔说完「我暂时负责你的训练」，光环第一次亮起来**。
- **跑尸方向写反**——原典里灵魂**在墓地醒**（天使「saving you a trip to your corpse」，
  省掉的正是墓地→尸体那一趟）。写成「在尸体旁站起来再走去墓地」是凭空多一趟往返。

### 改漏的一整个目录

**`characters/` 没跟**：v2 的回写清单只列了 concept / world / relationships，
而 rule 12.11-C 规定写剧本前必读人物卡——**卡里的旧口径会被原样读回去，等于回修白做**。
已补 c1 / c6 / c9 / c12 四张。

### 专名又错了一次

为补 L5 新写的那句把 **达芙妮·斯迪威尔**（西部荒野匕首岭）写成了 **达芙妮·斯通菲尔德**——
而斯通菲尔德是**艾尔文森林那对世仇农庄**的姓，正是本剧 ep09 罗朱支线用的那家。
**一份文件里把两个区、两户人家的姓混成了一个人**，且是在声称修完「凭空安姓」的同一稿里。

### 自检表第二次假通过

v2 的钩尾轮换是**改标签达标**的——四集的类型被换掉，内容一个字没动。
`ep19` 被标成「信息」，而它的最后一拍是全季情感落点。**下游是按钩尾类型配音乐、配镜尾节奏的**。
v3 改结尾不改标签，并给 §6 加了一列「钩尾的最后一拍到底是什么」让标签与内容当场对账；
其余各行改成「已核范围 + 待核范围」两段，未覆盖的打 ⏳ 不打 ✅。

其余: ep05 承段 34s÷3 镜跌破 12s 下限（并回 2 镜）· ep03 后半段压爆（摊成 8 镜 / 120s）+
**南墙隘口回头看见主厅室内的人**这一处几何不成立 · ep13 超载（《神圣之书》是跨四点的 9 步链，
读懂迪菲亚与 L3 擦肩移到 ep12）· F 编号声明当场过期（F1–F11 → F1–F13，三个命名空间分开，
引用 concept 的 F 号必须带表名）· L5 埋点补到别处（达芙妮独立成 L8）· world.md 的「尚未建」已非事实。

同步回写: `concept.md`（裁定 F8 拍法 / B3 白名单三次→五次 / 骨架表 7 行）·
`characters/{c1,c6,c9,c12}` · `world.md` · `tools/check_stage2.py`（自负向闸门 + 场景档 v3 契约 + 方位 token 撞车）。

QC: `check_stage2` 18 卡 + 9 场景 blocker 0 · `facts_registry` blocker 0 ·
`build_world_tree` 1768 节点 blocker 0 · `wow_version_gate` 无版本错置。

## Follow-up 004 — 2026-09-21
Source: user_input/follow_ups/202609.md - section 004
Summary: 四项拍板（并行推进 / 3D 只上北郡+闪金 / 纯爱好者不变现 / 剧名占位），随后按新规则给 9 个 bg 全部建出 3D 产物。

Auto-updated:
- `pending_user.md` — #8 结案（3D 范围表取代原 (a)/(b) 两档）；E6 标为用户确认；剧名降级为占位名且不得进对外文案
- `0_research/map/PIPELINE_3D.md` — ② 的「前置未决」改为已决；④ 的地点表改成本次定的四行范围；①②③④ 状态位更新
- `user_input/revised_prompt.md` — 按 raw + follow_ups 重建

Auto-updated（3D 层，由「每个 bg 一个 glb/blend」新规则触发）:
- `tools/build_scene.py` — **新建**：场景层通用建模引擎，读 `<scene>/planning/blocks.toml`，
  出 `{bg}.blend` + `{bg}.glb` + 校验 PNG。32 个 `kind`；`kind` 未登记直接 raise
- `tools/build_northshire.py` — **已删**：抽成通用引擎后它就是一份副本（rule 4i ① / 4h ③）
- 9 个 `scenes/bg*/planning/blocks.toml` — bg1 定点修正，其余 8 个新建
- 9 个 `scenes/bg*/_blender/` — 每个 `.blend` + `.glb` + `check_plan.png` + 5 张锚点透视
- 9 个 `scenes/bg*/planning/{bg}_floorplan.png` + `{bg}_blocks.md` — 由新 toml 重出

修正的实质错误（全部由生成时闸门抓出，不是人眼）:
- **商贩区有 12 m 陷在西侧山脊里**；加瑞克的小屋此前也犯过同一类错
- **修道院两翼由「南北」改判「东西」**（rule 4i ② 裁定，见 divergence #16）
- **修道院建了钟塔** —— `abbey.012` 的 negative 明排钟楼，属 4.0.3a 版本错置，已删
- **石拱桥桥心没对准河道中线** —— 按「过河桥道 × 北郡河」真交点重算为 (140, 144)
- **河的南段与出谷大道几乎重合**（路和河走同一条缝），河南段东移
- **前庭草坪与墓地平面重叠 1×9 m**
- **南墙必须让河过去** —— 原典写河自南出谷，而南墙是唯一出口，故加水门拱（位置从河道折线算）
- bg17/18/19/20/22/3 共 14 处块压块与扎进山体
- **4 个校验机位埋在体块内部**（bg22-1 在树丛里、bg3-1 在碎石堆里……），渲出来是一幅灰
- **bg22-1 的 `target_h` 被当成绝对高度写成 26** —— 丘顶地形本已 31 m，机位仰到 51° 去看天

新增的生成时闸门（左移，不留给出片前 reviewer）:
- 未登记的 `kind` / 块扎进山脊（`into_ridge` 显式豁免）/ 块压块（`may_overlap`）/
  块坐在河道上（`over_water`）/ 没有 `[[anchor]]` / **机位埋在块内部**（`inside`）
- `footprint()` 吃 `rot` —— 不吃 rot 的版本会把旋转过的墙全部算错

No conflicts found in: `1_立项/concept.md`, `3_大纲/arc_outline.md`, `0_research/`（事实层未动）

## 阶段 4 — 2026-09-22 — ep01–ep03 文学剧本
Source: follow-up 004「两条并行」的第二条（3D 与剧本同时推进）
Summary: 补齐 6 张北郡 NPC 卡（阶段 2 欠账）后，写出 ep01–ep03 剧本，22 镜 326s，台词闸门全过。

先补的阶段 2 欠账（**台词先于人物是倒序，rule 12.11 不允许**）:
- `tools/gen_npc_cards_szzl.py` — **新建**：六张北郡 NPC 卡的生成器（look 层同构走生成器，内容层逐人手写）
- `characters/c13_维里副队长` · `c14_萨缪尔修士` · `c15_伊根` · `c16_米莉` · `c17_尼尔斯修士` · `c18_加瑞克`
  —— 每张含 `## 人物灵魂` 12 维 + 锁定描述符 8 行 + 声口模板 + Seedream 立绘 prompt + turntable
- `casting.md` — 6 个 voice_id 登记（`zh-{m|f}-szzl-{短名}-01`）
- `relationships.md` — 补「北郡六人」10 组关系对
- `characters/c1_小满` — 补 **⓪ 旧号 · 19 级战士**变化态（ep01 冷开场专用，只一镜，故挂在主角卡而非另立卡）

阶段 4 产物:
- `4_剧本/episodes/ep01/script.md` — S01–S07 · 106s · 钩尾＝情感（萨缪尔那句「暂时」）
- `4_剧本/episodes/ep02/script.md` — S01–S07 · 100s · 钩尾＝危机（死 + 跑尸 + 墓地天使）
- `4_剧本/episodes/ep03/script.md` — S01–S08 · 120s · 钩尾＝实力（走出南墙隘口）
- 三份 `dialogue.md` — **生成物**，不手写（见下）
- `tools/script_tools.py` — **新建**：剧本解析器 + 台词闸门 + `dialogue.md` 生成器

为什么 `dialogue.md` 改成生成（rule 4i ①）:
playbook 要求每集两份文件，而同一句台词写两遍必漂——改了 script 忘了改 dialogue，
**两边都不报错，只会让配音那一侧拿到旧词**。现在 `script.md` 是台词唯一出处。

新增的生成时台词闸门（`python tools/script_tools.py check <范围>`）:
- 单镜台词字数 ÷ 时长 ≤ 5（实测 ep01 S03 是最紧的一镜，4.7）
- 每镜 3–30s；**4–6s 碎镜直接报错**（先问能不能与邻镜合并）
- 各镜时长合计 ＝ 文件头声明值，且落在 90–120s
- 每行台词必须带 `[对白]/[OS]/[系统]/[叠层]`
- **白话铁律**：24 个古语/公文唱礼腔词命中即 blocker；只有行尾自己声明「不走白话闸门」的
  声音彩蛋通道（`You no take candle!`）豁免

修正的实质错误:
- **解析器的 `\s*` 把换行吃掉**，于是行尾注释跑去捕获下一行台词，**那一行从结果里静默消失**
  （ep01 S01 三行只解析出两行，而生成的 dialogue.md 看上去完全正常）。已改成 `[ \t]*`

judgment call（已内联在产物里，带理由）:
- ep01 S01 的地点选 `bg21` 西泉要塞（大纲只写「两年前下线的那个地方」）
- 19 级战士不另立卡，登记为 `c1_小满` 的 ⓪ 变化态

全剧序列自检（三集作为一个序列读）:
- 钩尾轮换 情感 → 危机 → 实力，**无重复**
- 三个开场互不同构（冷开场 / 洞口 / 院门口），**没有「重新开始」式的开场**
- 状态轴连续：光环（ep01 S07 起常驻 → ep02 S06 熄灭 → ep03 复现）·
  装备裂口（ep02 S07 出现 → ep03 S01 之前修好）· L4/L5/L6/L7 埋点与呼应位置与大纲逐条对齐
- **L7 的呼应从 S08 挪回 S07**（几何：南墙隘口看不见主厅里的人），与大纲 v3 的裁定一致

No conflicts found in: `1_立项/concept.md`, `3_大纲/arc_outline.md`, `0_research/`, `5_6_分镜与prompt/`（未开始）

## Follow-up 005 — 2026-09-22
Source: user_input/follow_ups/202609.md - section 005
Summary: floor plan 升为每个 bg 的必备上游产物；标准落成 rule 4k + `tools/previz/planschema.py`；本剧 9 张图按新标准重出。

设计过程（5 路并行 + 完整性批判，agent 6 个 / 89.8 万 token）:
按**四个下游消费者各自的视角**分别设计——航线图 / Blender previz / Seedance prompt /
人眼五秒审批 / 既有规则约束——再由一路批判者找矛盾、缺口与过度。
批判者的三条裁定被原样采纳：① 图挂在**坐标系**上不挂在目录上；② 必填压到最少；
③ 「必备」靠**消费者跑不起来**咬人，不靠全仓盘点。

Auto-updated（通用规则）:
- `.claude/agent_refs/project/ai_video.md` — **新增 rule 4k**（含「明确不要做的」一节）
- `CLAUDE.md` — 加 rule 4k 指针
- `tools/previz/planschema.py` — **新建**：图的 schema + 解析 + 校验，**不 import bpy**，
  平面图生成器与 Blender 场景引擎共用同一份判据
- `tools/build_floorplan.py` — 改用 planschema；高度做成填充深浅（h0 画斜线）；
  索引栏印 `id`；尺度推定挂 ⚠；页脚印 `blocks.toml@sha8`；`--audit` 覆盖率
- `tools/build_scene.py` — 建 blend 前先过同一份 schema（消费者侧闸门）
- `tools/plan_stormwind.py` — 补 `id` / `scale_src`，**`h_m` 从 blend 包围盒量**（不手填）

Auto-updated（本剧）:
- 9 份 `scenes/bg*/planning/blocks.toml` — 补 `id`（88 块）/ `scale_src` / `absent`（6 个 bg）
- 9 张 `{bg}_floorplan.png` + `{bg}_blocks.md` — 按新标准重出

修正的实质错误:
- **`blocks.toml` 全仓一份都没进 git**（不是被忽略，是从没提交过），
  而**派生的 PNG 反倒被 gitignore + 同步 R2**——派生物有备份、唯一真相在工作区一个 `rm` 就没了，
  直接把 rule 4h-K ⑥ 反了过来。11 份已全部 `git add`
- **旋转过的块只测中心点**：`rot = 90` 的长墙有一半在场地外也判合格，而图上看就是贴着边
- **详图上每一块都印「无专属 bg」**：bg2 的 13 块本来就是 bg2 卡的组成部分，
  逼作者把 `bg = "bg2"` 抄 13 遍只会制造副本 → 改成默认继承本图主体
- **⚠ 在 msyh 里没有字形**，渲成方块 → 改画真三角
- `[meta] scale_src` 枚举漏了「坐标表」，把暴风城那份图判成不合格（会弄坏别的剧）

已登记、未执行（写进 rule 4k §G，动的是别人正在做的东西）:
- shot 层 `planning/blocks.toml` 是几何副本；方向应是 shot 只写
  `["全局"] 场景 = [{dir, t0, t1}]` 指向场地平面图。**全仓今天只有 1 份，趁早改还来得及**
- builder 拥有的世界（bianjing）应由 builder 生成 `blocks.toml` 落进 scene 目录，不留两类格式
- 系列共用地点的图跟着资产进 `_series/`，分集差异是 `states` 而不是分集子图

全仓覆盖率（`--audit`，只报告不判错）: 173 个 bg 目录 —— 自有图 9 · 未解析 164。
按 CLAUDE.md 2026-09-06「不回溯旧剧」，**不做全仓 sweep**；旧剧在真的动到某个 bg 时才补图。

No conflicts found in: `3_大纲/`, `4_剧本/`, `0_research/`（事实层未动）

## Follow-up 006 — 2026-09-22 22:44:53（执行跨 2026-09-23 夜）
Source: user_input/follow_ups/202609.md - section 006
Summary: 两片大陆全图入 scene——区目录 + 每个聚居点/子区域一个 bg + 原版地图 ref + 全部 floor plan；3D 不扩。

四项拍板（用户全部选推荐项）：区 = scene、聚居点 + 野外子区域 = bg；`scenes/{大陆}/{区}/bg{N}_{主体}/` 三层；旧 9 个 bg 迁入；每个 bg 主体卡 + 原版地图 ref + floor plan、不建 blend。

设计与执行（三个工作流）：
1. **完整性调研**（49 区各一名核验员 + 区图尺寸 + 缺图定位 + 完整性批判者 + 二轮补核，53 agent / 895 万 token）：
   逐区对照 warcraft.wiki.gg 经典旧世子区域表；补入 140 个 1.12 节点（含暗炉城 15 个城区、希利苏斯 21、千针石林 16、安戈洛 8），
   补坐标 100（348 → 448），判非 1.12 若干；49 区里 46 区的 WorldMapArea 尺寸取到一手出处；补抓银松 / 黑石山 / 荆棘谷 c60 / 石爪山 c60 原版图。
   结论：**1.12 玩家可达的区一个不缺，没有「明显该有却没有」的聚居点**。报告 `0_research/map/completeness.md`。
2. **结构生成**：`tools/gen_world_scenes_szzl.py` 从世界树铺出 49 区 / 804 bg（含 49 个区级「全境 / 全城」主体），每区 `ref/` 指向原版区图（`.link.json`），
   有坐标的 bg 附点位裁切图；bg 编号唯一出处 `scenes/registry.toml`（bg1–bg22 手工登记，其余顺序追加）。
3. **分区写卡**（49 个区级 agent + 146 个 bg 批次 agent）：terrain.toml（山脊 / 水系 / 道路，从原版区图量取）、≥1500 字锚点 prompt、blocks.toml、floor plan PNG，逐目录过 `tools/check_world_scenes_szzl.py`。
   之后分区对抗审核 + 修正（见本条末尾的结果补记）。

Auto-updated（通用规则）:
- `.claude/agent_refs/project/ai_video.md` — rule 4e 新增 2026-09-22 amendment（scenes 可按世界层级嵌套 / 锚点级档 / bg 登记簿）
- `CLAUDE.md` — AI video rules 加指针
- `.claude/skills/ai_videos__全流程编排/playbooks/ai_videos__stage2_世界观人设.md` — §3b 命名表加两行
- `tools/check_stage2.py` — 递归找主体目录；锚点级档跳过 K23 五 plate 与「步骤二」
- `tools/build_floorplan.py` — `[meta] grid_m`（整区级图用 200 m 网格）
- `projects/ai_video_management` — `series_shared.scene_subject_dirs`（递归找主体）、下载导入按它路由、左树 / 主体 md 中文标签对任意深度生效；新增测试 `test_subject_is_found_under_world_hierarchy_layout`
- 新工具：`tools/gen_world_scenes_szzl.py`（结构生成器）、`tools/check_world_scenes_szzl.py`（闸门 W1–W8 / Z1–Z3）

Auto-updated（本剧）:
- `2_世界观人设/scenes/` — 9 个旧 bg `git mv` 进 `eastern_kingdoms/elwynn_forest/`（相对路径 `../../../` → `../../../../../` 已改，floor plan 校验通过）；新建 49 区目录 + 795 个 bg 目录 + `registry.toml` + `scenes_index.md`
- `0_research/map/` — 新片区 `g14_completeness_20260923.yaml`；`zone_extents.toml`；`completeness.md`；世界树 1768 → 1908 节点；refs 补 8 张图并重建 `INDEX.md`；暗影裂口城 → 官方名「暗炉城」
- `2_世界观人设/world.md` §5 — 指向登记簿；bg8「黄金鱼塘」→ 水晶湖、bg9「石牧场」→ 斯通菲尔德农场、bg10 / bg14–16 名称规范化
- `0_research/map/PIPELINE_3D.md`、`specs/.../pending_user.md`、`tools/build_floorplan.py` 示例路径 — 改指新布局

未做 / 留给用户：
- 每个新 bg 不建 blend / glb（follow-up 004 维持：3D 只上北郡 + 闪金镇）
- `completeness.md` 末尾 159 条「留审」（核验员提出但脚本没自动采纳的改名 / parent 修正 / 存疑项）
- 本次改动未提交 git；`blocks.toml` / `terrain.toml` / `.link.json` / 卡片都是文本，`git add` 即可；PNG 裁切图与 floor plan 走 `assets_sync.py push`

No conflicts found in: `1_立项/concept.md`, `3_大纲/arc_outline.md`, `4_剧本/`（ep01–03 只引用 bg1–bg3 / bg17–bg22，目录名未变）

### Follow-up 006 续跑补记 — 2026-09-23（新会话接手）

上一会话的写卡工作流随会话一起终止：49 个区级 agent 里 26 个写完，bg 批次 agent 一个都没开始（排在区级 agent 之后）。
磁盘核对：769 张卡仍是骨架（每张 10 处占位，toml 未动），没有写了一半的目录。

开工前先修的：
- **bg 目录名走客户端官方简中**：从 wago.tools 取 Classic Era 1.15.9 客户端 `AreaTable` + `WMOAreaTable`（zhCN / enUS 按 ID 对齐），
  世界树里 `name_zh` 为空或英文占位的 151 个节点中 108 个有唯一官方译名，写回片区 YAML（note_zh 挂出处）并重建世界树；
  另按同一出处改 `wyrmbog` 蛮沼泽地 → 巨龙沼泽、`feralas` 费拉斯 → 菲拉斯、`ortells_hideout` 取 AreaTable 形「奥泰尔藏身处」、
  `tabethas_farm` 取 2.3 起的官方名「塔贝萨的农场」、`freewind_post` → 乱风岗（留审提议的「自由之风岗哨」与客户端不符）、6 个飞行点改成父节点官方名 + 飞行点。
  33 个 bg 目录随之改名（`bg97_Slither-Rock` → `bg97_滑石` 等；同区两座 Crusader's Outpost → `十字军前哨（南）/（西）`），全是未写的骨架，删后由生成器按新名重建。
  客户端两张表都没有条目的 7 个（Newman's Landing 等）按生成器「绝不自己音译」保留英文目录名。
- **`gen_world_scenes_szzl.py`**：区级平面图的块名改取登记簿目录名（提瑞斯法有三座同名「十字军前哨」，块名撞车）。
- **`check_world_scenes_szzl.py` 新闸门**：
  - **W9（blocker）**：锚点 prompt 正文与「一句话锁定」不许出现黄级专名（concept C3：text-only 实测放行前不进生成块）。
    词表 ＝ 世界树 大陆 / 分区 / 地区 / 主城 / 聚居点 名（≥3 字）+ 子区域名（≥4 字）+ 魔兽特有种族 / 职业译名；城区名与泛奇幻词不收（会天天误报）。
    一句话锁定也管：它 byte-identical 进每个 shot 的 `场景:` 行。已写好的 16 张区级卡锁定串去掉了开头的地名。旧卡（bg1–3 / 17–22）只报 warning。
  - **W10（warning）**：同区两张卡的 prompt 正文共用 ≥2 句 ≥24 字原句（风格 / 比例 / 负向 / 反向声明除外）。
  - `--json` 输出，给编排脚本读。
- 留审补处理：寂静河岸（Hushed Bank）的位置 / 描述 / 出处按专页改正（bg137 骨架同步）。

写卡工作流：`wf_c4bc80f6-13c`（审计目录 `.audit/adhoc_agents/2026-09-23/shengji_zhilu-20260923-212518/`）——
23 张区级卡 + 146 个 bg 批次（746 张卡）；每批写完立即由**独立审稿 agent** 逐张核事实 / 版本 / 专名 / 光源 / 平面图并当场改；
每区写完再做整区审（区级平面图对原版区图、跨卡雷同、锁定串互异）；最后按闸门 JSON 把仍不干净的目录重写一轮。结果见下一条补记。

## Follow-up 007 — 2026-09-24 12:40:00（执行跨 2026-09-24 / 25 夜，进行中补记）
Source: user_input/follow_ups/202609.md - section 007
Summary: 平面图每个编号块都要有资产卡与三视图，出 Rodin GLB，再拼成 bg 的 blend。

新工具 / 引擎改动（通用）:
- `tools/gen_bg_assets.py` —— 区级资产库流水线：`check` / `refs`（Wikimedia Commons 真实照片，逐张记许可；429 退避、串行节流）/
  `images`（即梦优先，失败退 ElevenLabs；**按 prompt 全文找回任务，多进程并发安全**）/ `mesh`（Rodin Sketch，余额保底 10）/ `--shard k/n`；
  任何一步卡住就记账跳过、接着做下一件（用户 2026-09-24「太久没反应就跳过」）。
- `tools/apply_asset_plan.py` —— 区级 `_assets/plan.toml` → 各 bg 的 blocks.toml（kind / asset / face / count + 默认校验机位），
  `--check-plan` / `--dirs-only` / `--build`（布局闸门以 build_scene 为唯一判据，自动声明逐条记账；区级主体跳过，它由生成器重写）。
- `tools/build_scene.py` —— 新 kind `asset`（导入资产 GLB：合并、剥材质、底面中心落原点、正面朝南；单件逐轴撑满块占地与 h_m，
  成片块按 `count` 确定性散布；没出模的方盒占位 `…·待出模`）与 `proxy`；线性 kind（palisade / low_wall / tunnel / arch_bridge）按占地长轴定走向。
- `tools/build_floorplan.py` —— 山 / 水 / 路裁到场地框内（原先湖面会伸出左边框）。
- `tools/check_world_scenes_szzl.py` —— （见 006 续跑补记）W9 / W10 / `--json`。
- `.claude/agent_refs/project/ai_video.md` rule 4h-K —— 2026-09-24 amendment（区级资产库、真实照片参考、线性 kind 走向、额度现实）。

实测单价（2026-09-24）：即梦三视图 9 积分 / 件（约 90 s / 张）；Rodin Sketch 0.5 credit / 件（约 2.5 min）。
Rodin 余额 155 → 瓶颈，约 300 件；先给第一季路线的五个区出模。

试点（闪金镇 bg4）：10 件资产（旅店 / 铁匠铺 / 马厩 / 路牌 / 马槽 / 信箱 / 井 / 民居 ×3 共用 / 大宅 / 货车摊）全部出图出模，
`_blender/bg4.blend` 建成，正反打轴线（旅店正门朝西）在锚点透视里对得上。教训：Rodin 把 41×17 m 旅店出成瘦高楼 → 改逐轴撑满占地；
即梦把「烧黑的火把架」画成点燃的火 → 写卡时明写「未点燃、无火焰、无光」。

第一季五区（夜里进度）：规划 + 资产卡全部完成（艾尔文 34 件含试点 10 · 西部荒野 35 · 暴风城 30 · 赤脊山 25 · 暮色森林 25），
西部荒野 / 暴风城 / 赤脊山 / 暮色森林的 blocks.toml 已写入并建出 blend（资产未出模者占位）；三视图与 GLB 在生成中。
第二梯队 18 区的规划 + 资产卡在跑（`wf_e042cba8-340`）。结果与剩余项见本条后续补记。

## Follow-up 008 / 009 / 010 — 2026-09-24 22:48 → 2026-09-25（夜间 AUTONOMOUS）
Source: user_input/follow_ups/202609.md - sections 008, 009, 010
Summary: 剧集化转向（零玩家概念、单集约 10 分钟）+ 面向英语观众（英文台词）+ 夜间全自主推进。第一集＝北郡全程，重写。

Auto-updated（本剧）:
- `1_立项/concept.md` — 新增「⚠ G 组 · 剧集化转向」G1–G9：零游戏/玩家概念、败北收费制（无死亡）、等级不出口、主角 Aaron / 同伴 Duke、单集 540–660s、ep01＝北郡全程、英文台词、G9 回填（升级零画面、片头字卡世界内英文、成片 16:9、签名句 "Buy me three."）
- `divergence.md` — #12 单集时长改 540–660s；新增 #19 台词英文（每句附中文意思），偏离「文件内容一律中文」
- `3_大纲/arc_outline.md` — 顶部标注暂停使用：旧 ep01–03 已合并进新 ep01，ep04+ 按第一集反馈重排
- `4_剧本/script.toml` — 新增，`[episode] min_s=540 max_s=660`
- `4_剧本/episodes/ep01/{script.md, dialogue.md}` — 整份重写：*Buy Me Three*（撑三下），27 镜 / 606s，英文台词 + 中文意思；工作流 `shengji-ep01-script-en`（三路草案与评审因断网失败，由合成稿兜底，见 script.md 文末 judgment call 20）+ `shengji-ep01-review-fix`（五维审查 + 修订 + 对抗复核）
- `4_剧本/episodes/ep02/`、`ep03/` — **删除**（旧中文玩家版，未进 git；内容已并入新 ep01；用户授权）
- `2_世界观人设/characters/c1_小满` → Aaron、`c2_不灭战魂` → Duke：按 G 组整卡重写（目录名与路由契约不动）
- `2_世界观人设/casting.md` + 全部人物卡配音段 — voice_id 统一 `en-…`（c1 `en-m-szzl-aaron-01`、c2 `en-m-szzl-duke-01`），声线改英文配音口径
- `2_世界观人设/{relationships, world, style_guide}.md` — 按 G 组 surgical 更新，作废段落标 ⚠（不删，防下游断链）
- `2_世界观人设/props/p1_金色感叹号 … p5_技能图标框`（UI 物件卡 5 张）+ `tools/gen_ui_props_szzl.py` — **删除**（G1 零 UI；且与正式物件卡 p1–p5 重号；未进 git）

Auto-updated（工具）:
- `tools/script_tools.py` — 单集区间改读剧级 `4_剧本/script.toml`（未知键报错）；英文台词按 ≤3 词/秒折算、中英可混排；拦伪古英语；台词下一行的中文意思带进 dialogue.md；**逐时间窗核念白**（台词行尾 `【a–bs】`）；`main()` 改为 import 安全
- `tools/check_stage2.py` — divergence #9 的 `[玩家]/[NPC]` 闸门换成 G1 闸门（卡里正面出现玩家三件套 / 玩家标记即 blocker）；voice_id 必须 `en-` 开头
- `tools/gen_npc_cards_szzl.py` — 生成器里写死的 `zh-` 前缀改 `en-`

未做 / 留给用户:
- 场景卡 797 条旧 blocker（锚点级卡缺「背景图系统 index」、bg5/bg7「待建」）属另一个 session 的范围，未动
- 名字、升级零画面、败北三笔账、16:9、片头字卡等都是夜间自主裁定（concept G9），可推翻

No conflicts found in: `0_research/`（事实层未动）

### 夜间进度补记 — 2026-09-25（子 agent 触发每周用量上限，Sep 30 8am 重置）

**已完成**：ep01 剧本 v1（27 镜 / 606s，`check` 通过）· 阶段 2 同步第一轮（c1/c2 重写、全员 en- 配音、人物网 / 世界观 / 风格指南按 G 组更新、人设闸门 G1）· UI 物件卡删除。

**第二轮五维审查已跑完、修订未跑**（fix / verify 因用量上限失败）：
审查结果全文 `.audit/adhoc_agents/2026-09-25/shengji_zhilu-20260924-224832/ep01_review_round2.json`（98 条：blocker 10 / major 42 / minor 46），
另有复核员上一轮留下的 3 条 major（时间窗、S22「第一次」、S15 审判冷却）与 7 条 minor，已并入该文件的处理范围。
主要问题归类：
1. **时间窗念不完**（B×7，S03 S04 S13 S14 S16 S18 S26）：整镜平均合格、局部窗 3.5–5 词/秒；S13 S14 S16 S26 连整镜都装不下 → 要加镜长（总时长可到 660s）并给**每句台词行尾标 `【a–bs】`**，让 `script_tools.py` 的逐窗闸门生效。
2. **原典**：S09–S10 劳工（Kobold Worker）在矿洞外营地纵深、洞里只有苦力；S05 应为森林狼；S16 赏金任务的前置是先交 12 块面罩；S15 审判冷却 / bg3 没有「只容一人的窄口」；c18 靴筒是短刀不是短剑。
3. **世界内逻辑**：S24 加瑞克之死读起来像处决倒地的人（blocker）；S12 苦力停在洞口不追＝游戏脱战；S07/S09/S11 两趟下矿没人派活。
4. **剧情**：S27 杜克坦白后亚伦无回应、情感落点空；"They think I made the Guard" 无铺垫；「光会把敌人引过来」触发条件前后不一；S23 杜克「站起来」与前拍矛盾。
5. **可拍性**：掉落物未写真实重力；S22 / S24 镜内切未分段；力量祝福写成肩背闪金（超分级）；刀刃入肉等写法过审风险。

**阶段 2 清理未跑**（同因）：`tools/gen_npc_cards_szzl.py` 未回写卡上现行内容（重跑会冲掉英文配音段！**用量恢复前不要跑它**）· `[NPC]` 标记未清 · turntable 统一生成器未写 · `props/p3_旧锤与木盾` 仍是单手锤 + 木盾旧设定 · style_guide 缺「审判」档与画面文字口径 · Llane Beshere（S08 / S14 有台词）缺卡与 voice_id。

**下一步（按序）**：① 按审查 JSON 修 ep01 剧本并对抗复核 → ② 阶段 2 清理（上一行）→ ③ 阶段 5/6：写 `tools/szzl_shot_engine.py` + `tools/gen_shots_szzl_ep01.py`（台词从 script.md 读、锁定串从卡读、闸门：shot_seam K31 / prompt_light K32 / shot_logic K33 / wow_version_gate / 参考行 rule 23）→ ④ previz 等另一 session 的北郡 blend 定稿后再做。

### Follow-up 006 / 007 补记 — 2026-09-25 06:00（周额度耗尽，交接）

**Claude 周额度 2026-09-25 凌晨耗尽，重置于 2026-09-30 08:00**——此后所有 agent 调用立即失败；不需要 agent 的脚本步骤（即梦 / ElevenLabs / Rodin 出图出模、`apply_asset_plan.py`、Blender 建 blend）照常跑完。

006（全图 scene 卡 + 平面图）：804 个 bg 里 **732 张卡已写完并过闸门**，还剩 **72 张**（塔纳利斯 18、千针石林 15、辛特兰 13、莫高雷 8、奥格瑞玛 5、希利苏斯 4、荆棘谷 3、菲拉斯 / 希尔斯布莱德 / 艾尔文 各 2、东瘟疫 / 费伍德 / 石爪 / 贫瘠 各 1）。
区审：第一季五区 + 奥特兰克 / 阿拉希 / 黑石山 / 诅咒之地 / 逆风小径 / 暗炉城 / 藏宝海湾 已审；其余区的区审因网络中断与额度耗尽没跑。

007（资产 → GLB → blend）：
- 第一季五区 **149 件资产全部出齐三视图 + GLB**；blend 按资产规划重建中（艾尔文在区审前直接落地——区审要等额度）。
- 第二梯队 13 区（奥特兰克 / 阿拉希 / 黑石山 / 诅咒之地 / 燃烧平原 / 逆风小径 / 铁炉堡 / 洛克莫丹 / 灼热峡谷 / 暗炉城 / 银松 / 悲伤沼泽 / 月光林地）**198 件资产卡已写**，出图出模在跑；Rodin 余额 80，保底 10，约够 140 件，按「铁炉堡 → 洛克莫丹 → 银松 → 悲伤沼泽 → 其余」的顺序花。
- 灰谷 / 艾萨拉 / 黑海岸 / 达纳苏斯 / 泰达希尔：规划与 asset.toml 已有，**资产卡没写**（写卡 agent 被额度挡住）。
- 其余 26 区：还没做资产规划（要等 006 的卡写完）。

额度恢复后按这个顺序续（每一步都从磁盘状态续跑，不重做已完成的）：
1. 72 张缺卡：`wf_v3.js` 的写卡 prompt 重跑到闸门 0 blocker。
2. 缺卡五区的资产卡；其余 26 区的资产规划 + 资产卡（`azeroth-zone-asset-cards` 工作流）。
3. 各区 `python tools/apply_asset_plan.py <区> --build`；出图出模 `python tools/gen_bg_assets.py all <区>/_assets --shard k/4`（Rodin 额度要充值才能出完）。
4. 没跑的区审。
5. 收尾：全量重出平面图（裁框修复）、`gen_world_scenes_szzl.py` 全量刷新索引、README 状态、本 changelog 终稿。

### ep01 第二轮审查落地 — 2026-09-25（主 session 手做）
- 先把被中断的修订 agent 留下的半截状态回退：它把 S21–S27 顺延成 S22–S28 准备插新镜、没插就断了；回退到它的备份（内容未变，镜号连续）。
- `4_剧本/episodes/ep01/script.md` — 按 `.audit/.../ep01_review_round2.json` 的 10 条 blocker + 42 条 major 逐镜修订（裁定见 script.md 文末 judgment call 8 / 21）；**27 镜 / 631s**；每句台词标【a–bs】，逐窗念白闸门全过。minor 46 条未逐条处理。
- `4_剧本/episodes/ep01/dialogue.md` — 重新生成。
- 阶段 2 清理的部分成果核实可用：`tools/gen_npc_cards_szzl.py` 已回写 c13–c18 现行内容（重跑与卡片零差异，**可以安全重跑**）；c8–c12 已去 `[NPC]` 与玩家口径。
- 仍待办：m1–m6 的 `[NPC]` 标记；`props/p3_旧锤与木盾` 旧设定；style_guide §4 审判档 / §8 画面文字口径；Llane Beshere 卡与 voice_id；bg3 卡补「西侧油灯支巷净宽约一人」（场景归另一 session）；对抗复核（等子 agent 用量恢复）。

### 阶段 2 清理 + ep01 阶段 5/6 — 2026-09-25（主 session 手做）
Auto-updated（本剧）:
- `2_世界观人设/casting.md` — 登记 Llane Beshere `en-m-szzl-llane-01`（ep01 只以隔壁画外声出现，无卡）
- `2_世界观人设/style_guide.md` — §4 补「审判」中档 + ep01 六种圣光表现落档表（祝福不出光、锤子从不持续发光、全量光柱只在 S23）；§8 定案「prompt 永不渲染可读文字」，作废「书写道具镜摘掉画面文字」的待确认项
- `2_世界观人设/characters/m1–m6` — 去掉 `[NPC]` 标记与「区分玩家与 NPC」措辞，改成世界内的「行为底线（G1）」
- `2_世界观人设/props/` — 物件卡按新 ep01 重生：p3 改为**亚伦父亲的旧双手锤**（含斧口变体 p3-2），新增 p9 杜克的旧木盾与短剑（完整 / 裂缝 / 半面三态）· p10 练习锤 · p11 圣信 · p12 葡萄清单 · p13 封好的文件 · p14 加瑞克的阔刃斧；旧 `p3_旧锤与木盾/` **删除**
- `5_6_分镜与prompt/episodes/ep01/` — **新建**：27 个 `shots/shotNN/shotNN.md`（五层 Seedance prompt + 英文台词配音块，16:9，全部硬切 + 景别跳档）+ `shotlist.md`（含 26 个接缝的切口审计）+ `all_shot_prompts.md`
- `README.md` — 头部与状态表按剧集化转向更新；闸门表补分镜生成器

Auto-updated（工具）:
- `tools/szzl_shot_engine.py` — **新增**本剧分镜引擎：台词从 script.md 读、锁定串从卡读、voice_id 从 casting 读、渲染串与负向从 style_guide 读；闸门 = shot_seam(K31) + prompt_light(K32) + shot_logic(K33) + wow_version_gate + 5000 字 + 零 hex + 裸 `=>@` + IP 红 / 黄级 + rule 23 参考行 + 时间轴铺满；写盘后回读
- `tools/gen_shots_szzl_ep01.py` — **新增** ep01 镜表（改分镜 ＝ 改它重跑）
- `tools/gen_props_szzl.py` — STYLE / NEG_BASE 改为运行时从 style_guide 围栏读（原为两份手抄副本）；物件表按 ep01 重排
- `tools/check_stage2.py` — G1 闸门扩到 `[NPC]` 标记

未做 / 留给用户:
- **previz 全部未做**（rule 4h 要求每镜必配）：北郡 blend 由另一 session 在做，按 rule 4h ⑥ 等 blend 定稿后再跑；各 shot 的 `参考:` 已占好 `shotNN_previz.mp4` 位
- 阶段 5 五道审查（站位朝向 / 运镜 / 动作表演 / 光线色调 / 时长节奏）与阶段 6 格式契约**未跑**（子 agent 用量上限，Sep 30 8am 重置）；机检闸门已全过
- bg3 卡须补「西侧油灯支巷净宽约一人」（S15 地形解依赖它）；bg1 缺院北林缘与狗头人营地两张 plate（S05 / S06 暂借 bg1-1）——场景归另一 session
- 图与立绘一张都没出；人物 turntable 统一生成器未写（rule 22.2）
