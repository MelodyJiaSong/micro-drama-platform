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

## Follow-up 011 — 2026-09-25
Source: user_input/follow_ups/202609.md - section 011
Summary: 每到一个新地方，留足镜头展示场景特点（自然 / 优美 / 宏大），方式灵活。

Auto-updated:
- `1_立项/concept.md` — 新增 G10「新地方先给景」
- `4_剧本/script.toml` — 新增 `[scenery] new_zone_min_s = 12 / new_bg_min_s = 6`
- `tools/script_tools.py` — 新增场景展示闸门（剧级 opt-in）：bg 在全剧第一次出现的那一镜须有 `- 场景展示:` 且窗长达标，跨集按集序算，闪前镜豁免；配置读取合并为 `_config()`
- `4_剧本/episodes/ep01/script.md` — 8 处补场景展示：S02 进谷 12s 升降揭示（新地区）· S03 修道院 6s 仰拍上摇 · S04 主厅 6s 纵深推进 · S05 林缘 8s 跟随 · S08 武器厅 9s 边读边走 · S09 矿洞 6s 坡下仰望 · S18 葡萄园 8s 越栅横移 · S21 小屋 6s 林隙窥视；另给 S17 石桥加 6s（非必需）。S02 18→26s、S03 22→28s、S04 25→28s、S18 22→26s，**全集 631 → 652s**
- `4_剧本/episodes/ep01/dialogue.md` — 重新生成
- `tools/szzl_shot_engine.py` — 从剧本读 `场景展示` 行并进 prompt 的 `镜头:`（数据文件不另写）
- `tools/gen_shots_szzl_ep01.py` + `5_6_分镜与prompt/episodes/ep01/` — S02/S03/S04/S05/S18 镜头、动作时间轴与起幅景别改为先给景；重生成 27 镜，切口审计全过
- `5_6_分镜与prompt/episodes/ep01/publish.md` — 章节时间轴按新镜长重算（10:52，12 章，最短 26s）
- `README.md` — 时长与闸门表

No conflicts found in: `2_世界观人设/`、`3_大纲/`

## Follow-up 012 — 2026-09-25 08:20:25
Source: user_input/follow_ups/202609.md - section 012
Summary: GLB 只装单个物体；每个场景都要出图；场景 blend ＝ 场景图 + prompt + 单物体 GLB 的汇总。

Auto-updated（规则）:
- `CLAUDE.md` — 「每个场景 bg 主体配一份 3D」去掉 `_set.glb`；rule 4h-K 条去掉「单个网格出 .glb」；新增「GLB 只装单个物体；场景 blend ＝ 图 + prompt + 单物体 GLB」三条
- `.claude/agent_refs/project/ai_video.md` — rule 4h-K 2026-09-25 amendment（parts / 场景图分层出图 / 没图不建 blend / W11 W12）

Auto-updated（工具）:
- `tools/build_scene.py` — 删 `export_glb`（旧 `{bg}.glb` 构建时顺手删）；没有场景图直接 raise；新增 `add_refs`（plate 图挂同名机位相机背景、场景卡 / plate 卡 / 资产卡 prompt 进文本块、资产三视图与场景图立成视口图片 empty、机位相机随 blend 保存、图按相对路径引用）；新增 `parts`（一个块里几件单物体资产按各自 size_m 摆）、`layout = "row"`（等距成排）、`build_room`（`interior = true` 的场地四壁 + 顶板，`opening = true` 的块留门洞）；网格最长轴与 size_m 不符时自动立正；不留 `.blend1`
- `tools/gen_bg_images.py` — **新增**：bg 锚点图 + 方位 plate 图，世界锚点 → bg 锚点 → plate 分层出，即梦优先 / 超 1600 字或失败退 ElevenLabs，`.part` 落盘后改名（防半截参考图）
- `tools/gen_bg_assets.py` — 单物体闸门（名字读起来是几样东西即拦，`single = "理由"` 例外）；`_dm_submit` 可传画幅；`--shard` 越界即报错（实测 `1/3..3/3` 漏掉第 0 份）；相对路径打印崩溃修复
- `tools/apply_asset_plan.py` — `[[use]]` 支持 `parts` / `layout`；`check_plan` 校验 parts
- `tools/link_bg_assets.py` — parts 块链接每件资产的文件
- `tools/check_world_scenes_szzl.py` — W11（bg 目录里有 GLB / 资产库 GLB 不在 `{key}_*/mesh/`）blocker、W12（缺场景图）warning
- `tools/build_bg_sets_sk1.py` — 不再导出 `_set.glb`；sk1 已有的 21 个不回溯删除

Auto-updated（本剧）:
- **删除** 228 个场景级 `_blender/bg{N}.glb`；W11 全仓 0 命中
- 艾尔文组合件拆成单物体：a41 长木桌 + a44 长凳、a26 旧木箱 + a45 木桶、a05 石饮马槽 + a46 拴马桩（`plan.toml` 六处 `[[use]]` 改 `parts`）；其余 11 区 11 件组合件交拆分 agent；bg495-a02 树屋声明 `single`
- ep01 九个场景的图：41 张（9 锚点 + 32 plate，含 bg1 世界锚点，全部 16:9 / 即梦）；新增 plate `bg1-6_院北_栎林苔石`（S05）与 `bg1-7_营外_林间矮帐`（S06）——**shot05 / shot06 的 `场景:` 与 `参考:` 仍借 bg1-1，待 ep01 分镜生成器改指**；bg3 卡与 `bg3-4` 补「西侧油灯支巷净宽约一人」（块 b05 宽 2.2 → 0.9 m）
- ep01 九份 blend 重建（`apply_asset_plan --build --only …`）：9 / 9，占位 0；六个外景 bg 的全部 plate 机位挂上背景图，三个室内 bg 的 `c2` 挂场景图；无场景级 GLB、无 `.blend1`
- Rodin：ep01 共出 13 件单物体 GLB（a35–a46 中 ep01 用到的），余额 ≈ 73.5；a05 / a46 只出了三视图（bg4 不在 ep01）；35 张旧 v3 卡按 16:9 重写构图并去黄级专名；bg1 / bg1-1 / bg1-3 去掉方形钟塔（与 bg2 版本铁律对齐）
- bg175 / bg176 / bg177 — 门洞块写 `opening = true`，补与场景卡同机位的 `c2` 相机（`image` 绑场景图）；bg177 两排石柱 `layout = "row"`

## 2026-09-25 — 分层出片：每镜先出镜头平面图（overhead），再做 shot blend（仓库级规则，本剧 ep01 首用）
用户指出：shot 的 `参考:` 挂着 `shotNN_previz.mp4`，却没有任何一步说明它怎么来——阶段 5 的 4b-2（平面图）与 4c（previz）被跳过了。
用户定调的分层：① 场景（scene blend + floor plan）→ ② 每镜 overhead（机位 / 走位 / 建筑与物件位置，不管动作与形状）→ ③ shot blend（真实动作、形状、镜头远近，渲 previz MP4）→ ④ Seedance。

Auto-updated（仓库级）:
- `CLAUDE.md` / `.claude/agent_refs/project/ai_video.md` rule 4j（2026-09-25 修订）/ stage5 playbook 4b-2 — 每一镜都出 overhead；位置只写在 `planning/overhead.toml`；名字统一叫 **overhead（镜头平面图）**（影视工业里画机位与演员走位的俯视图就叫 overhead；floor plan 留给场地，flight plan 是航空用语）
- `tools/shot_overhead.py` — **新增**通用工具：读每镜 `overhead.toml`，底图复用场地平面图画法，出 `shotNN_overhead.png` + 集级 `overheads.md`；闸门：键名白名单、时刻、入画人物与 `角色:` 双向一致、机位扎进实心体块、景别 × 焦距反算距离
- `tools/build_floorplan.py` — 场地画法抽成 `draw_site()` 供两张图共用（场地平面图输出逐字节不变）；越界的边距矩形钳进画布

Auto-updated（本剧 ep01）:
- `5_6_分镜与prompt/episodes/ep01/shots/shot01–27/planning/{overhead.toml, shotNN_overhead.png}` + `overheads.md` — 27 镜全部挂在各自场景的 floor plan 坐标系上，blocker 0 / warning 0
- 闸门首跑拦下的真错误（已修）：S01 / S22 机位埋在柴垛里 · S05 起幅机位在修道院主厅里 · S23 / S24 机位在木屋里 · S06 / S25 / S26 机位距离与景别不符（S25 落幅改中景越肩、S26 起幅改手部特写，切口仍合格）· S08 杜克入画却不在 `角色:`（已补）
- `tools/gen_shots_szzl_ep01.py` — 走位方向按 overhead 同步：主厅正门在西、治安官在东端（S04 / S07 / S25）· 武器厅由西往东、圆盾墙在东端（S08 / S14）· 矿洞洞口朝南、主巷正南北（S09–S12 / S15）· 晒场朝东南指林子（S20）· 出谷的盯梢者在**前方**林缘看着两人走近（S27）；S05 / S06 改用另一 session 新出的 plate bg1-6 / bg1-7
- `4_剧本/episodes/ep01/script.md` — S20 / S27 两处方向同步
- `tools/szzl_shot_engine.py` — 每个 shot md 写明镜头平面图路径与 previz 的来路（overhead → 过目 → shot blend → MP4）

待用户：看 `overheads.md`（27 张图），点头后才进 shot blend。

## Follow-up 013 — 2026-09-25 09:21:32
Source: user_input/follow_ups/202609.md - section 013
Summary: 各区 `_assets/` 物件库并进本剧 `props/p{N}_{名}/`（一套编号）；场景只引用 prop，出图时挂主要物件的正面图、建 blend 时从 props 取 GLB。

Auto-updated（规则）:
- `CLAUDE.md` — 「GLB 只装单个物体」条扩成四条：物件只住 props、一套编号（`props/registry.toml`）、场景出图挂物件图、机检 Z4
- `.claude/agent_refs/project/ai_video.md` — rule 4h-K 2026-09-25 amendment (b)

Auto-updated（工具）:
- `tools/props_lib.py` — **新增**：props 定位 / 登记表读写 / `new` 领号（bpy-free，唯一出处）
- `tools/gen_bg_assets.py` · `apply_asset_plan.py` · `build_scene.py` · `link_bg_assets.py` · `check_world_scenes_szzl.py` — 全部改从 props 取物件；区级规划搬 `_plan/`；W11 改查 props、新增 Z4
- `tools/gen_bg_images.py` — 场景图挂所属 bg 占地最大的前 3 件 prop 正面图 + 一行「物件参考」；世界锚点不挂（守 4e ②）；
  参考图上传前缩成长边 1600 的 JPEG（**实测即梦一次上传 ~20 MB 必败于 upload phase，10 MB 能过**）；上传失败先退避重试、不急着换引擎；即梦等待 4 → 15 分钟
- `tools/gen_props_szzl.py` — 剧情物件的键必须在 registry 登记为 story
- webapp（`ai_video_management` follow-up 174 / 175）— 导入按 `p{N}` 键归位三视图与 GLB；树按数值排序

Auto-updated（本剧）:
- **迁移**：462 件 → 13 件同物合并（两名独立核验员都同意才合并）→ `props/p15–p463` 449 件；`props/registry.toml` 登记 463 条（含剧情物件 p1–p14）；
  309 个文本文件改键（blocks.toml / plan.toml / 卡）；23 个区 `_assets/` → `_plan/`；每个 bg 的 `assets/` 链接重建（4276 条）；286 张平面图重出
- 79 件缺卡的卡里姆多物件补卡（黑海岸 19 / 艾萨拉 18 / 泰达希尔 17 / 灰谷 15 / 达纳苏斯 10）；449 件物件契约 0 不过
- ep01 八张卡压字数，让场景图挂得下物件参考图

未合并（待用户定）: 剧情物件与场景物件的重叠（如 p7 修道院兵器架 ≈ 武器大厅的兵器架）——剧情卡归 ep01 分镜会话的生成器

## Follow-up 014 — 2026-09-25 11:45:05
Source: user_input/follow_ups/202609.md - section 014
Summary: 每个 shot md 末尾加 `## previz prompt`（shot blend 生成指令），由生成器从 overhead.toml + 动作时间轴拼出。

Auto-updated（规则，全仓）:
- `CLAUDE.md` — 分层出片条补「shot md 带齐三层的做法」
- `.claude/agent_refs/project/ai_video.md` — rule 4j 2026-09-25 修订第 5 条
- stage-5 playbook 4b-2 · stage-6 playbook canonical 模板

Auto-updated（工具）:
- `tools/szzl_shot_engine.py` — `previz_prompt()`：`[全局]` 键值、换算好的 Blender 坐标、按 `cut` 分段的机位、角色色块/身高/路点/面朝、道具、姿态词表（按 AST 读 `build_previz.py`，不抄）、验收；缺 overhead 即生成失败；回读查 previz 块
- `tools/previz/build_previz.py` — `场景` 可写 scenes/ 下的嵌套路径，主档名认叶子目录名或 `bg{N}.blend`（原先找不到会静默退回灰模地面；旧剧的平铺写法行为不变）

Auto-updated（本剧）:
- ep01 27 镜重出（回读通过）；previz 块放文件末尾，因为 prompt_light / shot_logic / wow_version_gate 取第一个 text 块当 Seedance prompt

No conflicts found in: script.md, overhead.toml ×27, shotlist.md, all_shot_prompts.md（按标题取块，不受影响）
仍待用户：看 `overheads.md`，点头后才建 shot blend。

## Follow-up 015 — 2026-09-25 17:13:29
Source: user_input/follow_ups/202609.md - section 015
Summary: 24 个角色目录改英文名；补齐立绘（ElevenLabs）

Auto-updated:
- `2_世界观人设/characters/*` — 24 个目录 + md + png 改名为 `c{N}_{EnglishName}`；卡标题英文在前；「路由键不改」「英文名待定」备注更新
- 全剧文本引用（casting / relationships / concept / script / arc_outline / bg17 卡 / ep01 overhead.toml）同步替换
- `tools/szzl_shot_engine.py` · `gen_shots_szzl_ep01.py` · `gen_npc_cards_szzl.py` — 路径同步；ep01 27 镜重出，回读通过
- 缺图的 15 张立绘（c2–c9、c16、m1–m6）走 ElevenLabs 出图

No conflicts found in: shotlist.md, all_shot_prompts.md

## Follow-up 016 — 2026-09-25 17:45:55
Source: user_input/follow_ups/202609.md - section 016
Summary: bg2 六张场景图去动画感，ElevenLabs 覆盖重出

Auto-updated:
- `bg2_北郡修道院.md` + `bg2-1…5` 五张 plate 卡 — 加「真实感」行；风格串改实拍剧照（外景深景深 / 室内自然景深）；老式手工玻璃、暗沉钴蓝、灌木不修剪；负面词补 CG/游戏/微缩/过度干净 ~20 项；锚点加「不继承 bg1 渲染感」
- 6 张 png 由 `tools/gen_bg_images.py run … --engine elevenlabs --force` 覆盖

No conflicts found in: shot 卡（`参考:` 句柄不变）、blocks.toml、_blender
仍待：bg1 世界锚点本身偏游戏渲染，是否也重出由用户定。
- `m6_Spirit_Healer` — 立绘 prompt 原写「上半身无衣物」，被 ElevenLabs 审核拦截两次；改为披一件青白光凝成的高领宽袖长袍（卡内 #3 同步），重出通过
- 结果：24/24 张立绘齐（本批 15 张，走 ElevenLabs gpt-image-2 · 9:16 · 2K）

## Follow-up 017 — 2026-09-25 18:14:56
Source: user_input/follow_ups/202609.md - section 017
Summary: bg3–bg5 八张场景卡去动画感，ElevenLabs 出图（bg3 覆盖，bg4/bg5 首出）

Auto-updated:
- `bg3_回音山矿洞.md` + `bg3-1…5` — 「真实感」行、实拍风格串、锚点参考用法改为不继承 bg1 渲染感、新增负面词行
- `bg4_闪金镇.md` / `bg5_狮王之傲旅店.md` — 同上；负面词补进 `## 负向`；bg4 配色（锁定表 + prompt）「饱和翠绿 / 亮绿草地」→「浓绿 / 草绿」
- png 由 `gen_bg_images.py run … --engine elevenlabs --force` 生成

No conflicts found in: shot 卡、blocks.toml

## Follow-up 016 — 2026-09-25 18:45:37
Source: user_input/follow_ups/202609.md - section 016
Summary: 出图引擎分工（全仓规则 rule 4l）

Auto-updated:
- `CLAUDE.md` — 新增「出图引擎分工」条；场景出图条原「即梦优先」改指向它
- `.claude/agent_refs/project/ai_video.md` — 新增 rule 4l；4h-K 2026-09-25 amendment ② 同步
- `tools/image_engine.py` — 新建，引擎首选的唯一出处
- `tools/gen_bg_images.py` — `--engine auto` 默认：世界 / bg 锚点先 ElevenLabs（失败退即梦），plate 先即梦（失败退 ElevenLabs）
- `tools/gen_char_images.py` — 加即梦通道；人物立绘先 ElevenLabs、剧情物件先即梦，互为退路，超 1600 字只走 ElevenLabs

No conflicts found in: `gen_bg_assets.py`（物件三视图本就即梦优先）

## Follow-up 018 — 2026-09-25 18:46:27
Source: user_input/follow_ups/202609.md - section 018
Summary: previz MP4 只给复杂镜；每镜必有 overhead，另出一张给 Seedance 的版本

Auto-updated:
- `CLAUDE.md` / `ai_video.md` rule 4j 修订第 6 条（4h §A、4k §E、rule 23 表第 1 行同步）/ stage5、stage6 playbook — 新规则
- `tools/shot_overhead.py` — `previz_triggers` / `previz_decision`、Seedance 版 `_overhead_ref.png`、人物颜色按卡号固定、`overheads.md` 加 previz 列
- `tools/szzl_shot_engine.py` — 免 previz 镜挂 overhead_ref、不出 previz 块；Reference uploads 列出盘上路径；`--materials` 素材核对；修「冲画外 / 冲隔壁喊」被误判成画外音（shot01、shot14 的杜克改回对口型）
- `tools/gen_props_szzl.py` — 状态变体移出锚点图 prompt、去 markdown 粗体（p3 / p9 原 prompt 会画出裂盾 / 斧口）；`tools/gen_char_images.py` 加 `--kind props`
- ep01 shot01 `overhead.toml` + 生成器 `走位:` — 杜克面朝镜头旁的亚伦（原图面朝西、prompt 写东，两边都错）
- ep01 shot02 `overhead.toml` — 杜克擦亚伦左肩过（原路线直接穿过亚伦）；`情节:` 去掉与 bg20 卡矛盾的「下坡进谷」
- ep01 shot03 `overhead.toml` + `镜头:` — 阶顶→阶下由连续移动改为 11s 硬切（原路径穿过亚伦头部）；杜克 6–7.5s 冲上石阶绊倒，与 `动作:` 对齐
- ep01 全部 27 个 shot md / shotlist / all_shot_prompts / overheads.md — 重生成（生成器闸门 + 回读通过）
- `props/p3_*/p3_*.png`、`props/p9_*/p9_*.png` — 新出锚点图

No conflicts found in: 其余 24 镜的走位与台词（只换了参考行与 previz 块）
## Follow-up 019 — 2026-09-25 19:11:42
Source: user_input/follow_ups/202609.md - section 019
Summary: 角色参考改挂 Seedance 资产包 entity（长相 + 声音），不入画的说话人注明只用声音

Auto-updated:
- `CLAUDE.md` / `ai_video.md` rule 23 修订 — 新规则
- `tools/szzl_shot_engine.py` — `_handles` 挂 entity、`参考用法:` 改写、Reference uploads 与 `--materials` 把 entity 标为「在 Seedance 里 @」
- ep01 全部 27 个 shot md / all_shot_prompts — 重生成（闸门 + 回读通过）

No conflicts found in: 台词配音块（voice_id 仍从 casting.md 读，供 TTS mux）
## Follow-up 018 — 2026-09-25 19:27:24
Source: user_input/follow_ups/202609.md - section 018
Summary: bg19 六张场景卡去动画感，ElevenLabs 覆盖重出

Auto-updated:
- `bg19_加瑞克的小屋.md` + `bg19-1…5` — 「真实感」行、实拍风格串、锚点参考用法、新增负面词行
- 6 张 png 由 `gen_bg_images.py run … --engine elevenlabs --force` 覆盖

No conflicts found in: shot 卡（ep01 shot01 / 21–24 引用 bg19-2，句柄不变）、blocks.toml、_blender
- 剧情物件 p1–p14 锚点图齐：9 张即梦（各 3 积分）、p10–p12 三张因即梦网络超时退 ElevenLabs；p3 / p9 此前已有
- `tools/gen_bg_assets.py::_dm_submit` — 提交改 `--poll=0`：CLI 自带轮询遇网络超时整条报错且不吐 submit_id（任务其实已成功扣费），改由自有 query 循环取回
- `tools/gen_char_images.py` — 即梦网络错误先退避重试（判据复用 `gen_bg_images.RETRYABLE`），首选引擎失败原因打印出来

## Follow-up 019 — 2026-09-25 19:40:58
Source: user_input/follow_ups/202609.md - section 019
Summary: bg1 / bg18 / bg20 / bg175 / bg177 共 22 张场景卡去动画感，ElevenLabs 覆盖重出；style_guide 上游同步

Auto-updated:
- `style_guide.md` §6 — 场景图不用「轮廓优先的剪影设计 / 手绘感的高饱和色块 / 浅景深」，指向 bg2 卡为范本；C10 — prompt 写「浓绿」不写「饱和」
- `bg1_北郡山谷`（锚点 + 7 plate）、`bg18_北郡葡萄园`（锚点 + 5）、`bg20_南墙隘口`（锚点 + 5）、`bg175_武器大厅`、`bg177_主厅` — 实拍风格串、「真实感」行、「浓绿」、负面词
- `bg2 / bg3 / bg4 / bg5 / bg19` 锚点卡 — 删去「它的画面偏游戏渲染、饱和过高」（bg1 重出后不再成立）
- 22 张 png 覆盖（`gen_bg_images.py … --engine elevenlabs --force`，三段）

No conflicts found in: shot 卡（`参考:` 句柄不变）、blocks.toml
仍待：bg172–186 等其余艾尔文 bg 卡仍含「饱和翠绿 / 手绘感的高饱和色块」，未出图前按 style_guide 新注改即可（不回溯已出图的）。

## Follow-up 020 — 2026-09-25 19:48:19
Source: user_input/follow_ups/202609.md - section 020
Summary: 每张人物卡都有立绘 prompt + 4 秒建立视频 prompt

Auto-updated:
- `tools/gen_turntables_szzl.py` — 新建；从立绘 prompt + casting 生成建立视频块，手写的不覆盖，旧卡手写要点收进 NOTES 表
- `characters/` 20 张卡（c3–c5、c7–c9、c11–c18、m1–m6）— 新增 / 重写 `## turntable 说明`；m1 / m5 / m6「本季不做 turntable」改为指向本节
- `c6_Wren` / `c10_Gryan_Stoutmantle` — 从 git 旧版恢复手写视频 prompt（本次生成器首跑误覆盖过一次），改名、16:9、声样窗 3.5 s
- `c2_Duke` — 视频块首行 `c2_Duke` → `c2_Duke_turntable`（原与立绘撞键）、9:16 → 16:9、声样窗 0–2 s → 0–3.5 s
- `tools/gen_npc_cards_szzl.py` — 去掉自带的 turntable 模板，写完卡调用 gen_turntables；`tools/check_stage2.py` — 缺视频块 warning → blocker、不再豁免群体怪
- `ai_video.md` rule 22.2 修订

No conflicts found in: 立绘 prompt（未改动，出图工具回读正常）
## Follow-up 022 — 2026-09-25 20:35:00
Source: user_input/follow_ups/202609.md - section 022
Summary: p1–p14 改三视图格式；所有 prop 三面图走即梦

Auto-updated:
- `tools/gen_props_szzl.py` — 剧情物件卡改出三视图（`p{N}-1_正面` 块原文不动 + 侧 / 背两块，侧背按现有正面图写），并出 `asset.toml`；14 张卡重生成，`gen_bg_assets check` 14/14 通过
- p1–p14 旧单图改名 `p{N}-1_正面.png`；p10–p12 原为 ElevenLabs 出，删掉用即梦重出
- `tools/szzl_shot_engine.py` + ep01 shot01–27 的 Reference-uploads 行 — 物件图路径改指 `-1_正面.png`
- `tools/gen_bg_assets.py` — 即梦网络错误退避重试；`--engine` 默认 auto（即梦、失败退 ElevenLabs），显式 `dreamina` ＝ 只用即梦
- `tools/image_engine.py` / `gen_char_images.py` — 同一口径：显式引擎只用那一家
- p4 / p6 / p9 名字读作多件，asset.toml 写 `single` 豁免（出 GLB 前要拆）；p8 实为成组摊位，同样待拆

仍待：p375 起 79 件场景物件由另一会话出图（默认 auto，可能有退 ElevenLabs 的，查 gen_log.json）

## Follow-up 023 — 2026-09-25 22:23:21
Source: user_input/follow_ups/202609.md - section 023
Summary: 新手冒险者 c1–c6 人物卡去装备（朴素布衣、两手空空）

Auto-updated:
- `characters/c1_Aaron … c6_Wren` — 立绘 / turntable prompt 去掉兵器、盾、甲，加「手里什么也没拿，身上没有任何武器、盾牌与甲胄」与对应负面词；#4 / #5 / #8 改为只写人与便服，装备指向装备表（rule 4m）；c4 #8 软帽色与 #3 对齐（月白）
- `tools/gen_turntables_szzl.py` — c4 侧面要点去掉「法杖握位」
- c1–c6 立绘用 ElevenLabs 重出（第一张锚点，rule 4l）

未动：ep01 shot（#8 已变，等装备层 `equipment_lib.wearing` 接入后再重出）· c1 旧 turntable mp4 · c3–c6 的法杖 / 匕首 / 皮甲尚无装备卡与装备表
No conflicts found in: NPC c7–c18 · m1–m6
- （022 补记）剧情物件 p1 / p2 / p4–p8 / p11–p13 三面图全部走即梦出齐；p3 / p9 / p10 / p14 已由装备会话迁入 `equipment/`（e1–e5），不再归 props；`gen_bg_assets._dreamina` 等待 4 → 15 分钟

## Follow-up 021 — 2026-09-25 20:24:24
Source: user_input/follow_ups/202609.md - section 021
Summary: 新增「装备」资产类型（槽位 × 品质）；人物卡只管人、起始穿着朴素；到 40 级的真实装备考据（023 扩到 60）

Auto-updated:
- **规则**：`ai_video.md` rule 4m（新）· `CLAUDE.md` 装备条 · 阶段 2 playbook 步骤 3b + QC 条
- **工具（全仓通用）**：`tools/equipment_lib.py`（定位 / e{N} 领号 / 装备表 / 闸门，含 `check_item`、单侧装备 `one_side`）· `tools/gen_equipment.py`（build / check --only / images --shard；物品原名、黄级专名、hex、游戏截图来源、即梦 1600 字在写盘前拦）
- **网页端**（ai_video_management follow-up 177）：树的 `{key} {rest}` 标签 + 下载导入按 e{N} 键落进条目目录
- `2_世界观人设/equipment/`：`equipment.toml`（14 槽位 · 六档做工语法，出自 W21-tiers）· `registry.toml`（99 件）· 99 个条目目录（item.toml + 卡）· `loadouts/c1_Aaron.{toml,md}`（17 阶段）/ `c2_Duke.{toml,md}`（16 阶段）· `equipment_index.md`
- **迁移**：props p3 / p9（拆盾与剑）/ p10 / p14 → e1–e5；props 登记簿与 `tools/gen_props_szzl.py` 删四条；已出的 p3 正 / 侧、p14 正面图改名跟过去，p9 盾剑合照删除
- `characters/c2_Duke/c2_Duke.md` — 起始降为便服 + 旧圆木盾 + 旧短剑（#4 / #5 / #8、来历表、立绘与 turntable 两段生成块、负向）；旧拼凑甲 turntable `c2_Duke.mp4` 移到 `ai_videos/_deleted/`，需按新卡重出
- `characters/c1_Aaron/c1_Aaron.md` — #4 标「便服底层」、#5 与练习锤指向 e1 / e2、装备段指向 1–60 装备表
- `tools/szzl_shot_engine.py` — 镜表认 e{N}（锁定串 / 句柄 / 正面图从装备库取）；有装备表的角色自动追加空槽反向声明；`tools/gen_shots_szzl_ep01.py` 删 27 处手写 `BARE` 串、p 键换 e 键 → ep01 27 镜重写（回读过）+ overhead 重出
- `0_research/parts/w21_装备体系与逐件外观.md`（新，325 条事实）· `dossier.md` 加 W21 行 · W12 的 `wow.gear.030 / 031` 改 ❌（W21-critic 以 1.12 库证伪）
- `1_立项/concept.md` G11（① 40 级首身板甲用真实的重型秘银件 ② 紫装额度 ③ 光铸「金色」口述 ④ B10 ⑤ 两人不撞衫 ⑥ 光铸利刃不排（C5）⑦ D18 照大纲 ⑧ C6 补 40→60 ⑨ C7 查实：1.12 人类圣骑士起手双手锤、不持盾 ⑩ D16 血色护胸是白底红火焰罩衫）· `pending_user.md` #7 🔴 → 可选
- `README.md` — 目录导航加「2c 装备」、闸门表加 `gen_equipment.py build`

No conflicts found in: `4_剧本/episodes/ep01/script.md`（剧本从未写过杜克的甲）、`arc_outline.md`（D18 落点照它）

## Follow-up 022 — 2026-09-25 22:20:00
Source: user_input/follow_ups/202609.md - section 022
Summary: 装备出图沿用 props：正 / 侧 / 背三张，全走即梦 CLI

Auto-updated:
- `tools/gen_equipment.py images` 默认 `--engine dreamina`（只用即梦、失败不退 ElevenLabs）；`tools/image_engine.py` 说明表加一行；`ai_video.md` rule 4l 表 + 4m ⑤；`CLAUDE.md` 装备条
- e1–e5 三视图 15 张齐（e3 首版把盾的背面画成正面，改卡「正面没有把手与臂带」+ 副手槽陈列写死后重出）；其余 94 件分三波、5 个即梦进程在出

## Follow-up 023 — 2026-09-25 22:30:00
Source: user_input/follow_ups/202609.md - section 023
Summary: 装备路线做到 60 级

Auto-updated:
- W21 延伸到 40→60（两路各配对抗核验员 + 逐件看模型）；两人装备表经 W21-reconcile 调和（撞衫、B10、C5、D18 四项，23 条裁定记在 W21 §10）
- 夜间无人值守（用户 2026-09-25 23:30「不要问我，自己 make best effort decision」）：全部裁定以 judgment call 记在 concept G11、W21 §10 与装备表 note 里，可推翻
- 装备库只收剧里用得到的：路线候选池里没进任何装备表、也不是传说 / NPC / 骰点件的 14 件删掉（民兵圆盾、哈加德的战斧 / 战锤、幻影之甲…）；过渡件（弗伦的礼物、民兵短剑）因装备表备注点名而保留

## Follow-up 022 续 — 2026-09-26 出图与验图收尾
Source: user_input/follow_ups/202609.md - section 022（夜间无人值守执行）
Summary: 99 件装备 297 张三视图全部用即梦出齐；六轮验图 + 三次出图上限，56 件全过、19 件正面可用、24 件正面有偏差待人工

Auto-updated:
- 全部 99 件的正 / 侧 / 背三视图（即梦 CLI，5–6 进程分片并发；单件失败只记下、整轮后补跑，`--passes`）
- 验图工作流（每轮 agent 对照卡逐张看图，卡的毛病改 item.toml、随机坏图只删那张）连跑六轮 + 三次终验；**每件最多出 3 次**，第 3 次后仍有偏差的写 `known_issue`（卡上「⚠ 图的已知偏差」、索引图数旁 ⚠）：43 件，其中 19 件正面可用、只侧 / 背有偏差，24 件正面偏差（e12 e30 e33 e34 e35 e38 e39 e41 e45 e46 e52 e55 e58 e59 e70 e71 e81 e83 e90 e107 e110 e111 e117 e129）
- 验图揭出的共性毛病一律收回源头：`equipment.toml` 品质做工串改成只写新旧光洁（不写结构件与附加物）、槽位陈列写死「空手套 / 护肩下面空 / 男式人台 / 没有五官的头模 / 手工皮底」；`tools/gen_equipment.py` 正面加「尺寸 / 年代」行、单侧装备单独陈列、侧背加硬性转角句，新增三道写盘闸门（游戏截图来源、侧背绝对方位 `ABSOLUTE_POS`、正面点名禁物 `NAMED_ABSENCE`）
- `ai_video.md` rule 4m ⑦（八条出图共性坑）· ⑧（出图配验图、3 次上限、known_issue）
- ep01 27 镜再次重写（e3 改灰后句柄更新），回读过；全部闸门过（equipment · ep01 · facts · webapp 24 测试）

No conflicts found in: characters（24 卡零问题；798 个 blocker 均为既有场景卡的 v3 模板缺节）

## Follow-up 020 — 2026-09-26 10:25:54
Source: user_input/follow_ups/202609.md - section 020
Summary: c13–c18 立绘补族裔锚；c14 / c16 重出为欧洲人脸；出图工具加 22.1 闸门

Auto-updated:
- `tools/gen_npc_cards_szzl.py` — PORTRAIT 开篇「西欧白人」+ 骨相行；PORTRAIT_NEG 补东亚兜底；重跑 → c13–c18 卡（立绘块与 turntable 块同步）
- `characters/c14_Brother_Sammuel.png`、`c16_Milly_Osworth.png` — 重出（无 turntable、无成片，下游无返工）
- `characters/c4_Maren.png` — ⚠ 测试闸门时误触 `--force` 被重出；旧图未入 R2，不可取回；新图仍是同一形象（年轻欧洲女性、米白布帽、灰蓝坎肩）
- `tools/gen_char_images.py` — 首句缺人种 / 地域的人物立绘 run 时拒绝、plan 标 ⚠（m 键豁免）
- `.claude/agent_refs/project/ai_video.md` 22.1 — 记机检入口

No conflicts found in: 锁定描述符（未改，shot 不需重出）、casting.md
仍待：c4 / c6 / c7 / c8 / c12 卡首句缺人种，下次重出前须补（闸门会拦）；c6 Wren 黑直发、五官两可，且已出 turntable。

## Follow-up 026 — 2026-09-26 10:34:02
Source: user_input/follow_ups/202609.md - section 026
Summary: 按游戏等级排集，ep01 ＝ 1–5 级

Auto-updated:
- `1_立项/concept.md` — 新增 G13（等级段是排集尺子；ep01 ＝ 1–5；后续路线与职业节点；片里不说等级）

No conflicts found in: `equipment/loadouts/c1_Aaron.toml` / `c2_Duke.toml`（L01 ＝ 1–5 已绑 ep01，与本条一致）· w07 / w21（路线与职业节点一致）
待办：`3_大纲/arc_outline.md` 暂停使用（v3），ep02 起按 G13 重排时再改

## Follow-up 025 — 2026-09-26 12:04:36
Source: user_input/follow_ups/202609.md - section 025（及 026）
Summary: ep01 整集重写——1→5 级、只在北郡、七种野怪、转新手村、装备四渠道、结尾小丑装

Auto-updated:
- `0_research/parts/w23_北郡装备来源.md` — 新调研：任务奖励全表、七种怪掉落、四个商人货架价格、钱的时间线、矿洞「破损的箱子」、推荐表
- `tools/build_blacklist.py` — 黑名单节标题允许带编号；w02 的 26 行首次进库（negatives 861 → 970）
- `4_剧本/episodes/ep01/script.md` — 删除重写（regen 事件见 .audit/adhoc_agents/2026-09-26/shengji_zhilu-20260926-113958/）：24 镜 / 605s，节拍表 v1 经用户确认（去闪前、钢盾走矿洞箱子）；script_tools 闸门全过
- `4_剧本/episodes/ep01/dialogue.md` — 由 script_tools gen 重新生成

未动（待办）：
- ep01 阶段 5/6 的 27 个 shot、overhead、shotlist、all_shot_prompts 已全部过期（对应旧剧本），需按新剧本重出
- 装备表 `loadouts/*.toml` 需支持按镜分段（ep01 一集内换六七次装），归装备会话的 equipment_lib
- 阶段 2 待补：狼的怪物卡、院西商贩一排 plate + 高德瑞克小卡、狗头人三种区分写法、破损的箱子物件卡、新装备卡（2385 / 1366 / 1438 / 11192）
- 人物卡「说话风格」里引用的 ep01 镜号是旧稿的，下次同步卡时改
- ep01 剧本两轮审查已落地（台词：3 major / 9 minor ＋ 中文释义；剧情连贯：1 blocker / 16 major）。要点：尸体全集不入画、加瑞克倒出画外；S20 按「谁出光扑谁」重排——每一声「当」都是冲亚伦去的斧子；狼不再「掉」东西（伊根剥皮送狼皮狼牙）；数量写进台词（十个 / 十二块）；技能名不出口（"CHARGE!" → "Coming through!"）；钢盾改原典外观（冷钢多面椭圆盾）；1366 画成粗皮长裤；装备分层可穿（卸盾套甲、披风时盾靠台阶、腰带扣在外衣外）；S22 杜克听到「闪金镇」一僵；bg20 两名卫兵入画；主厅 / 武器大厅场景展示按场景卡重写；画面文字一律英文、铜币无字。闸门仍全过（24 镜 / 605s）

## Follow-up 027 — 2026-09-26 11:45:00
Source: user_input/follow_ups/202609.md - section 027
Summary: 蓝以上必须有品质色特效光；蓝以上与绿档武器 183 件重做考据与卡；绿以上武器改走 ElevenLabs；受影响的图作废重出
（注：本条起初误编为 025，与 ep01 重写会话的 025 撞号，已改为 027。）

Auto-updated:
- `2_世界观人设/equipment/equipment.toml` — 蓝紫橙 `glow_required` + `glow_grammar`；[meta] `elevenlabs_categories` / `elevenlabs_min_tier = 绿`；修掉三处与发光冲突的设置（蓝紫负向泛禁光晕、紫档 rule「品质不发光」、橙档做工串把「挂毯壁画 / 剪影」送进 prompt）
- `tools/equipment_lib.py` — `Config.engine_for`；闸门：蓝紫橙缺 effect、其余 prompt 字段的光短语带别档颜色、灰白绿写光、蓝紫橙负向泛禁光，一律 blocker
- `tools/gen_equipment.py` — 「光:」一行进正 / 侧 / 背三张；逐件定引擎（`--only-engine`）；prompt 上限随引擎；卡上加「出图引擎」「原典描述与传说」两行
- `equipment/**/item.toml` × 183 — 逐件重做考据（每件 2–18 张图）与卡：真实尺寸、截面与工艺、本档颜色的光、侧背写角度特有结构、`lore`；删 `known_issue`；370 张卡重生
- 旧图 213 张删除（regen 事件见 .audit/adhoc_agents/2026-09-26/shengji_zhilu-20260926-114500/），81 件武器走 ElevenLabs、102 件护甲走即梦重出；另补齐 41 件未受影响但缺图的
- `.claude/agent_refs/project/ai_video.md` rule 4m ① / ⑤、rule 4l 表；`CLAUDE.md` 装备条；`tools/image_engine.py`；stage 2 playbook 3b；`1_立项/concept.md` G14（本想写 G13，与 026 的 G13 撞号，改 G14）；`0_research/parts/w22` §4；README

No conflicts found in: 装备表 loadouts（未改）、ep01 shot（锁定串原样保留，未要求重出）

## Follow-up 028 — 2026-09-26 16:26:42
Source: user_input/follow_ups/202609.md - section 028
Summary: 装备键改层级码 e{分类}{槽位}{序号}，每层目录带号，从号码就能一层层找到件

Auto-updated:
- `2_世界观人设/equipment/equipment.toml` — [[category]] 加 `no`（1 布甲 … 6 法系与远程），[meta] `key_digits = [1, 1, 2]`
- `tools/equipment_lib.py` — `Config.prefix / cat_dir / slot_dir / key`；`allocate` 领本槽下一个号；`item_dir` 按层级目录；闸门拦「键不在自己号段」；`renumber`（搬目录、改图名与 item.toml 首行、registry 记 `was`、装备表同步、清空目录）；入口校验 key_digits / 分类号
- `equipment/` — 375 件（含 ep01 会话新领的 e404–e408）改码搬家：`{C}_{分类}/{C}{S}_{槽位}/e{C}{S}{NN}_{品质}_{名}/`，同槽按品质灰→橙排号；图随键改名；registry 每行 `was = 旧键`
- `equipment/loadouts/c1_Aaron.toml`、`c2_Duke.toml` — 键按映射原地替换（阶段结构不动）
- `tools/gen_equipment.py` — 索引加「号码怎么读」表、分类 / 槽位标题用目录号；卡加「目录」一行（含旧键）
- `characters/c1_Aaron`、`c2_Duke` 卡；`0_research/parts/w21`、`w22`、`w23` — 键按映射替换（区间写法展开）
- `.claude/agent_refs/project/ai_video.md` rule 4m、`CLAUDE.md` 装备条、stage 2 playbook、README、工具注释里的示例键
- 网页端：无代码改动（分类 / 槽位目录本就透明遍历，四位键照常解析），只改 `equipment_key.py` 文档（webapp follow-up 179）

未动（按 ep01 会话要求）：`tools/gen_shots_szzl_ep01.py`、ep01 旧 27 镜与 all_shot_prompts.md——该会话正按新剧本整表重写，将按 `was` 查新键。
历史记录（本 changelog、follow_ups、.audit）里的旧键不改，查 registry 的 `was`。
待办：ep01 会话新领的 5 件（e1603 / e2802 / e3604 / e5121 / e5205）还没有 item.toml，build 在它们补齐前不写卡。

## Follow-up 029 — 2026-09-26 17:20:00
Source: user_input/follow_ups/202609.md - section 029
Summary: ElevenLabs 只给蓝档以上武器（省额度）；绿档武器改即梦并把 prompt 细节写满

Auto-updated:
- `equipment/equipment.toml` — `elevenlabs_min_tier` 绿 → 蓝（卡上「出图引擎」一行随之变）
- `equipment/**/item.toml` × 22 — 未出图的绿档武器补结构 / 截面 / 连接 / 缠握细节，正面 prompt 目标 1450–1590 字（e5123 / e5206 已有 ElevenLabs 三视图，保留不重出）
- `.claude/agent_refs/project/ai_video.md` rule 4m ⑤ 与 4l 表、`CLAUDE.md`、`tools/image_engine.py`、stage 2 playbook、concept G14、README — 绿档 → 蓝档；补「走即梦的件把 1600 字用足」
- `equipment.toml` 六档加 `nonmetal` 材质族；49 件木 / 骨 / 石 / 角主体的武器改挂 nonmetal、5 把火枪 blade → blunt（做工串不再把「刃面 / 钢件」塞给木弓骨杖；rule 4m ⑦ ⑩）
- 本会话 ep01 新写 5 张卡（e1603 / e2802 / e3604 / e5121 / e5205，接 ep01 会话的调研）：check 过，375 张卡重建；e5121 金属件按民兵套装串写素钢（模型是铜色，套装一致优先）

No conflicts found in: 装备表、分镜（锁定串未变）

## Follow-up 030 — 2026-09-26 17:27:50
Source: user_input/follow_ups/202609.md - section 030
Summary: ep01 分镜按新剧本重出（24 镜）；装备表支持按镜分段

Auto-updated:
- `tools/equipment_lib.py` — Stage.shots（一集内按镜分段）、shot_n、stage_for / wearing(…, shot)、同集镜号区间不重叠的闸门
- `tools/szzl_shot_engine.py` — worn_clause 按镜号取装备表；说话人表补 "Kobold"
- `tools/gen_equipment.py` — 装备表 md 显示镜号区间
- `equipment/loadouts/c1_Aaron.toml` L01a–L01g、`c2_Duke.toml` L01a–L01d（按镜分段）；两人 L05 改成 ep01 出谷的一身
- 新装备 5 件（领号 e404–e408，装备会话重编号后为 e3604 / e2802 / e5205 / e1603 / e5121，卡由装备会话写成）
- `tools/gen_shots_szzl_ep01.py` — 镜表按新剧本整表重写（24 镜）；走位方位按场地平面图校正（S09 / S10 / S15 / S17 / S19–S22），S04 去掉尼尔斯，S01 去掉朝谷外的 plate
- `5_6_分镜与prompt/episodes/ep01/` — 删旧 27 镜，重出 24 镜 + shotlist / all_shot_prompts / overheads（24 张平面图，0 blocker / 0 warning；previz 要 7 镜：01 / 06 / 10 / 13 / 15 / 19 / 24，S10 为手动判定）；闸门与回读全过
- `4_剧本/episodes/ep01/script.md` — 装备外观措辞对齐锁定串（皮连指手套 / 十边形冷灰钢盾 / 露指布手套）、「下坡」改中性、S04 去尼尔斯、S17 暴徒不开口（casting：m4 ep01 无配音）

待办：
- 用户过目 24 张镜头平面图 → 7 镜做 shot blend / previz（Blender MCP 本会话未连上）
- Seedance 角色 entity 连服装一起锁（rule 4m ⑥）：亚伦 ep01 有 7 套穿着、杜克 4 套，需按阶段重出 turntable / entity，或另定口径
- `publish.md` 是旧剧本的文案，待按新剧情重写
- 场景层：bg3 岔口与掌子面之间有 1.75 m 空隙（平面图）；院西商贩一排无 plate；狼的怪物卡

## Follow-up 031 — 2026-09-26 17:46:13
Source: user_input/follow_ups/202609.md - section 031
Summary: 换装三面图——亚伦 7 套、杜克 4 套，子目录 c1-1…c1-7 / c2-1…c2-4

Auto-updated:
- `.claude/agent_refs/project/ai_video.md` — rule 4m ⑥ 2026-09-26 修订（换装只出三面图，不重出建立视频）
- `equipment/loadouts/c1_Aaron.toml`（L01a–L01g）、`c2_Duke.toml`（L01a–L01d）— 各阶段加 `view = {key, name, refs, look, carry}`
- `tools/gen_outfit_views.py` — 新工具：读装备表与 item.toml 写子目录卡、出三面图（正面挂锚点正面 + ≤3 件装备正面；侧 / 背挂本套正面 + 锚点侧 / 背）；即梦
- `characters/c1_Aaron/c1-1_便服与父亲的锤` … `c1-7_出谷小丑装`、`characters/c2_Duke/c2-1_便服与祖父木盾` … `c2-4_徽记披风` — 卡已写，图出图中

待办：网页端导入器只认一级键 `c1-1`、落人物卡根目录——手动出这些图再导入会互相覆盖，要先给导入器加子目录路由
- 验图（029 批 C，70 件 + 终验 8 件）：过 35；终验不过的 4 件（e1101 / e1409 / e2204 / e2605，背面照抄正面）写入 `known_issue`
- `equipment.toml` 七个槽位 `display` 去掉点名的缺席物（头模五官 / 人台手臂 / 手套手指 / 护肩衣服人台 / 盾背把手臂带 / 披风下摆散开）；`gen_equipment.py` 加 `DISPLAY_ABSENCE` 闸门、`NAMED_ABSENCE` 补五官 / 手臂 / 手指 / 把手 / 臂带；15 张卡字段里的「没有手臂 / 没有手指」改正面写法；rule 4m ⑦ ⑪
- 验图 029 批 D（57 件 + 终验 10 件）：过 20；终验不过的 6 件（e4601 / e4602 / e4701 / e4801 / e6306 / e6313）写入 `known_issue`
- 新出图方法「三视图设定图」（`gen_equipment.py images --sheet` + `split_sheet`）：侧背照抄正面是即梦挂参考图的通病，护甲改为一张横幅并排三视角再裁三张；试验 e2704 / e3208 有效、e5125（镐）无效，故只用于护甲；rule 4m ⑦ ⑫


## Follow-up 021 — 2026-09-26 19:14:03
Source: user_input/follow_ups/202609.md - section 021
Summary: shot01 shot blend + previz MP4；引擎支持路点机位与逐点地形

Auto-updated:
- `tools/previz/build_previz.py` — `[[机位.路点]]`（t / 位置 / 瞄 / 焦距 / 切，单调插值，与运镜 / 锁定主体 / 位置互斥，默认不切墙）；`[全局].地形`（只认名含片段的场景件、排除 previz 自建物，角色逐帧贴地）
- `tools/szzl_shot_engine.py` — `_plan_xform`（prompt 与 config 共用）、`previz_config()`、`--previz-config`、Shot.previz；previz prompt 里「每段单独渲再拼接」「引擎自动插值成行走」两句改成实际做法
- `tools/gen_shots_szzl_ep01.py` — shot01 previz：14s 低头、20s 回正；卫兵 1.8 m、草丛 0.5 m；ep01 重跑，闸门与回读通过
- `shot01/previz/{previz_config.toml, shot01_previz.blend, shot01_previz.mp4}` — 自检：起幅人占画高 10.2%（档 0.1）、落幅 82.9%（档 0.8）；577 帧 / 24.04 s

No conflicts found in: overhead.toml（未改）
注：重跑时生成器已是另一会话改过的 24 镜版本（原 shot25–27 不再生成），本次按其当前状态输出。
- 终验 029 final3（41 件第 3 次）：过 2（e2208 / e4108），39 件写入 `known_issue`；其中三视图设定图重出的 18 件护甲只过 1 件——成对装备只画一只（设定图 prompt 漏陈列行，已补）、裁图带进分隔线、背面仍照抄；rule 4m ⑫ 改记为「备选、非默认」
- 验图 029 批 E（23 件，第 2 次）：过 5（含 ep01 的 e1603）；18 件改卡后出第 3 次（含 ep01 的 e2802 / e3604 / e5205）
- `equipment.toml` 盾的做工串去掉结构与缺席物（「铆钉规整，没有纹章」让素面钢盾满边长铆钉；「旧板 / 包边」同理）；`gates` 把「不点名缺席物」扩到各档 positive 与材质族串


## Follow-up 032 — 2026-09-26 21:13:02
Source: user_input/follow_ups/202609.md - section 032
Summary: shot01 台词有了听的人（门卫问话）；shot02 家狗 → 半大野狼 + 挪到溪边小径 + 杜克护人格挡逐拍几何；Cascadeur 人体 previz

Auto-updated:
- `4_剧本/episodes/ep01/script.md` — S01 改 29s：门卫问 "Name. Business."，亚伦转身答、看锤改口，最后 12s 揭示山谷；S02 改 28s：下主路到溪边捧水，两只野狼出芦苇，杜克挡在亚伦与狼之间、盾面朝狼，一人只挡、一人只砸；全集 605 → 612s；`dialogue.md` 重生成
- `2_世界观人设/characters/m7_Wolf/`（新）— 野狼图鉴卡（幼狼 / 森林狼两档后缀、狼 vs 狗判别位、负向组 W-A/B/C、立绘已出、turntable prompt）
- `2_世界观人设/characters/m8_Northshire_Guard/`（新）— 北郡门卫群体卡（全覆面圆穹盔 + 金狮罩袍 + 长戟，立绘已出）；`casting.md` 补 `en-m-szzl-guard-01`、狼列入无台词
- `tools/gen_shots_szzl_ep01.py` — S01/S02 重写；S05/S14 挂 m7 卡、状态读卡的档位后缀、负向改 `@卡:m7_Wolf`（S05「肩高及膝」改成年森林狼）
- `tools/szzl_shot_engine.py` — 闸门：正常台词画里没有听的人即 raise；叙事字段点名生物而没挂卡即 raise；`card_tier` / `card_negatives` 从卡读；`[[guard]]` 译成 `走位:` 一句；previz 配置挂 Cascadeur FBX / 四足 / 钩子
- `tools/shot_overhead.py` — `[[guard]]` 护人格挡几何闸门（在中间 / ±40° / 面朝 ≤50°）；previz 判据补「人与怪攻防接触」「护人格挡」；审阅图列出格挡段
- `tools/previz/build_previz.py` — `[[角色]].模型`（Cascadeur FBX，NLA 重定时、逐帧贴地）、`四足` 代理、`[全局].后处理` 每镜钩子
- `tools/cascadeur/{casc_fk.py, choreo.py}`（新）— 关节角 → Cascy 全身 IK 点；动作表 → 逐键 → 驱动 Cascadeur 出 FBX
- `shots/shot01/planning/overhead.toml`、`shots/shot02/planning/overhead.toml` — 重排；S05/S14 狼由 object 改 actor，S05 加 `[[guard]]`、杜克前移半步（闸门拦下的「站在旁边不是前面」）
- `shots/shot02/cascadeur/choreo.toml`、`shot02_body{1,2}.fbx`、`shots/shot02/previz/shot02_previz.py` — 人体动作与盾 / 锤 / 狼扑咬
- `shots/shot01/previz/*`、`shots/shot02/previz/*` — previz 重渲
- `.claude/agent_refs/project/ai_video.md` rule 29（新）+ rule 4j ⑥ 判据补两条；`CLAUDE.md` 分层出片判据同步；`ai_videos__cascadeur动作` 技能补四条实测事实

No conflicts found in: 其余 20 镜台词与切口（ep01 闸门全过，24 镜 612s）
- `tools/previz/build_previz.py` 自检补「人站进场景实体」（射线奇偶 + 包围盒）；负向测试：卫兵放回旧站位 → 报「卫兵（西）站进了门塔西」
- `shots/shot01/planning/overhead.toml` — 卫兵挪到门塔正前方（y 24.4）；问话机位改门内正北朝南 28 mm 侧面（原机位下西侧卫兵被亚伦挡住、东侧在画外）；落幅机位退到门洞北口、升到 3 m
注：S05 / S14 按新判据也要 previz（人与怪攻防），previz 尚未渲。

### 同日追加（用户：六条提速都做）
- `shots/shot05/planning/overhead.toml` — 18–28s 机位从正东挪到东南：原机位下杜克整个躲在亚伦身后，说 "Dad's boots are fine" 时看不见他（新的「说话的人看得见」闸门拦下）
- `tools/gen_shots_szzl_ep01.py` — `vis_legacy = {S11, S12, S14, S16, S18, S22}`：这几镜平面图上说话人被挡 / 在画外，闸门只打印不拦，待逐镜修（只减不增）
- `shots/shot01/previz/shot01_previz_p{1,2}.mp4`、`shots/shot02/previz/shot02_previz_p{1,2}.mp4` — 28–29 s 的 previz 超过 Seedance 单条参考视频 15 s 上限，切成两段；两镜参考行改挂两段
- `shots/shot02/cascadeur/choreo.toml` — 姿势部件改用共享库名（逐键比对零差异，FBX 不重出）
- 收尾（2026-09-26 22:40）：375 件三视图全部齐；终验 029 final4 / final5 共 26 件第 3 次，过 7，19 件写入 `known_issue`。全库 85 件带已知偏差（灰 5 · 白 12 · 绿 27 · 蓝 15 · 紫 25 · 橙 1），按 rule 4m ⑧ 不再循环，交人工挑图——`equipment_index.md` 图数旁标 ⚠、卡上「⚠ 图的已知偏差」一行写明问题
- 最常见的剩余偏差：侧 / 背照抄正面构图（即梦挂参考图的通病，三视图设定图试验未解决）；其次是细部数目与比例（齿数、铆钉数、刃长比）

- （031 补记）11 套 33 张换装三面图全部出齐并逐张验过（即梦，每张 3 积分）；装备会话把 e2802 / e3604 / e5205 出到第三版定稿后，用到它们的 7 套按定稿重出
- `tools/gen_outfit_views.py` 出图中实测修正：① `view.pose` 写握法（只写「横挎在肩上」不写手→锤悬在肩上没人扶）；有握法时兵器不再贴卡上的穿法 ② 正面写明「右手一侧在画面左边」 ③ 侧面写明只露左半边、侧脸只露一只眼 ④ 背面喂本套正面的**镜像**作参考（文字写「左右对调」仍常把盾剑画反）＋ 有盾的阶段写「从背后只露盾背」 ⑤ 下载断线只重下不重交（WinError 10054 / read timeout）
- 仍偶发：左右手随机画反、侧面没转过去——逐张验，错的单张重出（c2-2 侧面、c2-4 背面各出到第 3 次）

## Follow-up 033 — 2026-09-26 23:20:00
Source: user_input/follow_ups/202609.md - section 033
Summary: shot02 / shot05 的攻防按距离 ÷ 速度 ≥ 反应时间重排；平面图加物理与反应机检

Auto-updated:
- `tools/shot_overhead.py` — `physics_errors`：速度上限（人 8 / 四足 14 m/s，跨镜内硬切不算）、真碰过人的怪在 2 m 内 ≤0.8 s、`[[react]]` 反应窗（`REACT_S` 动作时长表）；有 `[[guard]]` / `[[react]]` 的镜为 blocker，其余镜警告
- `shots/shot02/planning/overhead.toml` — 狼 8.2 s 在七八步外出芦苇、潜行 0.8 m/s；11.5 s 咬靴后立即跳开；12.4 s 趁他砸空扑，杜克 9.2 s 起跑、12.6 s 到位挡住；绕后那只 14.4 s 才扑、他 14.0 s 已转身握短；回马 25.5 s 从芦苇窜出 0.8 s 到；三段 `[[react]]`；8.6–12.5 s 机位退成 24 mm 全景让距离看得见
- `4_剧本/episodes/ep01/script.md` S02 画面动作与台词时间窗（Behind me! 12–13 s，其余三句 18–26.5 s）；`dialogue.md` 重生成
- `tools/gen_shots_szzl_ep01.py` — S02 情节 / 镜头 / 分镜 / 镜内状态 / 走位 / 动作 / 节奏同步；S05 动作补「扑—退—再扑」
- `shots/shot05/planning/overhead.toml` — 森林狼：扑盾后退到两步外绕，12.5 s 扑亚伦挨第一锤退开，14.3 s 再扑挨第二锤翻出；`[[guard]]` 收到 10.8 s
- `shots/shot02/cascadeur/choreo.toml`、`shot02_body{1,2}.fbx`、`previz/shot02_previz.py` — 新节拍；`tools/cascadeur/choreo.py` 保持段判定改为「姿势相同、位移 < 0.3 m」（原先位置须完全相同，16 s 的盾被 Bezier 提前转向）
- `tools/szzl_shot_engine.py` — 狼的 previz 色块改紫（灰色与灰模场景混在一起）
- `.claude/agent_refs/project/ai_video.md` rule 29 ④；`CLAUDE.md` 索引补一行

No conflicts found in: 其余 22 镜（ep01 闸门全过）
其余旧镜的物理警告（未改，待逐镜处理）：shot10 / shot15 鼠面矿工在扑咬距离内干等；shot12 / 15 / 17 / 22 / 24 路点速度超限（多为镜内时间跳跃没标硬切）


## Follow-up 034 — 2026-09-27 00:55:08
Source: user_input/follow_ups/202609.md - section 034
Summary: S03 摔倒补上原因；上下文逻辑检测器接进生成器；夜间自主把 ep01 全部 previz 镜过了一遍静帧并修掉查出的错

Auto-updated:
- `4_剧本/episodes/ep01/script.md` — S03 杜克拖着 S02 被咬的右脚一路抢跑、最后一级石阶伤脚一软扑倒；S05 头狼倒下、另两只逃开并补「（过了一会儿）」；S06 九只全打倒；S08 新台词 `Duke: "The Marshal said the mine's worse."`；S10 亚伦被撞倒、裤膝撕开；S11 伤口写成镐尖划开的口子；S14 首句标画外音；S19 / S20 第五斧卡进还绑在左臂的半面木盾里，加瑞克拽斧甩木头那两秒就是杜克换钢盾的时间；S22 麻袋与面罩、信交给杜克；S23 换装前先靠锤、卸包；状态轴补「杜克右脚跟」；`dialogue.md` 重生成
- `4_剧本/episodes/ep01/states.toml`（新）— 跨镜状态账本：杜克右脚跟 S02→S03、亚伦靴尖 S02、杜克左肩 S10→S24、亚伦裤膝 S10→S15、杜克胸口链甲 S14
- `tools/beat_logic.py`（新）— L1 速度词 ↔ 平面图、L2 结果要有原因、L3 状态账本、L3b 伤要登记；生成器 build 时逐镜调，任一条 raise
- `tools/shot_overhead.py` — `[meta] hostile / calm`；持械者按 1.7 m 够得着算；有人挡在扑击线上不算干等；实心块只算 ≥2.5 m、成排块拆开、门洞不算墙；`jump_cuts`；`[[object]] h`
- `tools/szzl_shot_engine.py` — 跳时间的镜内切在 `分镜:` 里照实写；说话人可见性遗留清单清零（S11 / S12 / S14 / S16 / S18 / S22 改站位或机位）；表外角色的 previz 色避开本镜已占色；贴地件名改 `地形 / 地面 / 道路`
- 平面图 S01 S02 S03 S05 S06 S08 S10 S11 S12 S14 S15 S16 S18 S20 S22 — 按物理 / 逻辑 / 可见性闸门逐条改；S14 两只狼拆成两条 actor；S20 开场 0–5.5 s 定住拍第一斧、改 28 mm 退到 5 m 三人同框
- `tools/previz/build_previz.py` — 贴地改成只对地面件的 BVH；场地外 6 m 内按边缘取高；横移开场主体在第一段内入画即可；**画里的人全被场景件挡住即 blocker**（负向测试：shot06 旧机位报出）
- `tools/build_scene.py` — `chamber` 在垂直穿墙的 tunnel 处开洞；散布件高度以平面图 `h_m` 为上限
- `2_世界观人设/scenes/.../bg3_回音山矿洞/planning/blocks.toml` — 补「掌子面过道」b10；狗头人宿营挪到掌子面东南角、只留一顶；bg3 blend 重建
- `shots/shot20/cascadeur/choreo.toml`、`shot20_body{1,2,3}.fbx`、`previz/shot20_previz.py`（新）— 杜克扯盾带 → 越肩卸钢盾 → 扛斧 → 两次横跨截住 → 膝盖一沉 → 盾沿磕下巴；加瑞克拽斧、踩木头拔斧、连砍、两次绕扑、仰倒；亚伦掌心光、扔光；钢盾 / 半面木盾 / 斧 / 锤 / 光柱在钩子里挂
- `tools/cascadeur/poses.toml` — 补 brace_sink / stomp_r / fall_back / twohand_tug / twohand_pull_up / strap_tear / reach_back_r 与单手锤、掌心光几件
- 12 个 previz 镜 — 配置重生成、静帧逐镜审阅后整条重渲（超 15 s 自动切两段）
- `.claude/agent_refs/project/ai_video.md` rule 31（新）+ rule 30 补表；`CLAUDE.md` 索引补一行；新审查 skill `ai_videos__逻辑因果`，接进 `ai_videos__审查总编排` 第 7b 步

No conflicts found in: ep01 其余台词与切口（生成器闸门全过：24 镜 612 s；平面图 24 镜 blocker 0 · warning 0）

留给用户定：
- S21 加瑞克头上套麻袋——剧本硬约束明确允许，未改
- S07 没有补动机台词
- m7 野狼 / m8 门卫的 Seedance entity 还没建（转台视频已出）
- 其余 10 个 previz 镜仍是色块人偶；S05 / S14 的狼扑咬若要真人体，照 shot02 / shot20 做 choreo

### 034 同夜追加（渲整条时查出的引擎问题）
- `tools/previz/build_previz.py` — 描边（Freestyle）门槛从 20 万面降到 6 万面：shot08 七块 2.3 万面的 Rodin 石头让描边一帧 20 s、整条要 3 小时；并给 5.1 粗细着色器读 `FEdgeSmooth.normal_left` 的崩溃包一层（抛错退回居中粗细）
- 12 个 previz 镜全部渲完（每镜约 6 分钟），全部超过 15 s、各切成 `_p1 / _p2` 两段；生成器回读通过

## Follow-up 035 — 2026-09-27 09:05:00
Source: user_input/follow_ups/202609.md - section 035
Summary: S03 删掉杜克门前摔倒；逻辑闸门收紧（摔倒只认外力 / 行动受限的伤，账本加 severity）；新增子代理全集上下文通读并首跑 ep01

Auto-updated:
- `4_剧本/episodes/ep01/script.md` — S03 杜克抢跑冲上最上一级刹住站稳喊 "First!"，维里报数后他挺着的胸塌下去半寸；删掉瘸、扑倒、亚伦拽起；状态轴「杜克右脚跟」改为当场没事；`dialogue.md` 重生成
- `4_剧本/episodes/ep01/states.toml` — 五条都加 `severity`；杜克右脚跟改为 无碍、`to = S02`、`show = []`
- `tools/gen_shots_szzl_ep01.py` S03 — 情节 / 镜头 / 分镜 / 镜内状态 / 走位 / 动作 / 节奏 / 语气同步；负向加 摔倒 / 绊倒 / 趴在地上 / 一瘸一拐
- `shots/shot03/planning/overhead.toml` + 两张 overhead 图 — 杜克停在维里东南侧的最上一级（让开阶下机位看维里的视线与维里朝西下阶的路）；6s 机位改为越过维里右肩俯拍；shot03 免 previz，无 3D 重渲
- `tools/beat_logic.py` — L2 摔倒不再认「跑 / 冲 / 绊 / 踩空」，身上状态当原因须有本镜生效的 行动受限 条目；新增 L3c（severity 分档与后果对账）、L3d（写瘸须有行动受限的伤）；负向测试：旧 S03 被拦下 2 条
- `tools/szzl_shot_engine.py` — build 时调 `check_states`
- `.claude/skills/ai_videos__逻辑因果/SKILL.md` §2b（新）、`agent_refs/project/ai_video.md` rule 31、stage 4 playbook QC、`全流程编排` / `审查总编排` 表、`CLAUDE.md` 索引行
- 生成器全过、回读通过：24 镜 612 s；平面图 blocker 0 · warning 0

§2b 首跑（`.audit/adhoc_agents/2026-09-27/shengji_zhilu-20260927-012843/spawns/logic-review-01/output.md`）：blocker 1 · major 3 · minor 10，均未改，待用户定——
- blocker：S19–S20 暴徒跑后亚伦空着手旁观五斧与加瑞克拔斧的两秒
- major：S15 苦力群 9–19s 去向不明、19s 又「四散」；S16–S17 十一块面罩没有来处；S20–S22 下巴一磕即死、谁割的头没交代、腰挂人头进主厅无人反应（触及剧本硬约束 2）

No conflicts found in: ep01 其余台词与切口

## Follow-up 037 — 2026-09-27 11:51:06
Source: user_input/follow_ups/202609.md - section 037
Summary: Seedance 网页出片资料包——备料自动、生成人点

Auto-updated:
- `tools/seedance_kit.py` — 新工具：open / build / check / sync；资料包是派生缓存 `.seedance_kits/`（已加 .gitignore）
- `ai_videos/shengji_zhilu/seedance.toml` — 本剧设置：别名 魔兽世界 / wow、entity 前缀 wow、Chrome 账号 Work（Jia）
- `.claude/agent_refs/project/ai_video.md` rule 12.4-K；`CLAUDE.md` 一行
- 实测：ep01 shot02 资料包 6 个文件 + prompt + 说明；改指纹后 check 报过期、sync 刷新回最新

No conflicts found in: shot md（正本仍是裸 =>@，只有资料包的 prompt 代填编号）


### 035 续（用户选定：14 条全改、赏金凭证换成斧子、亚伦抡锤被格开）
- `script.md` / 生成器 / `states.toml` / 平面图 S02 S05 S06 S09 S10 S11 S12 S13 S14 S15 S16 S17 S19 S20 S21 S22 S23 — 逐条落地首跑查出的 14 条：S02 握短只留给 S07；S05 护腕软鞋从狼皮卷里抽出；S06 狗头人不咬人；S09 油灯早熄、S15 借撞落的蜡烛点蜡烛头；S10 锤在撞倒那一下脱手；亚伦双掌右膝擦伤登记（皮外，S10→S13）；S13 杜克套链甲时肩伤一顿；S14 亚伦摸空肩、狼咬腰侧链甲下摆；S15 苦力 8s 先逃出矿、皮袋甩在岔口、19s 起在岔口看见长裤；S16–S17 面罩被扯掉刮掉、暴徒三两一伙一垄垄清；S19 亚伦绕到西侧抡锤、被斧柄格开一脚踢出画；S20 三四秒与活结；S21 加瑞克远景里爬起来钻进林子，亚伦捡起他脱手的阔刃斧交杜克；S22 杜克扛斧进厅；S23 斧子与面罩交维里；剧本硬约束 2 改写
- `c13_Deputy_Willem.md` — 「收头颅」改为收赏金凭证（斧子）
- `tools/beat_logic.py` — 一脚踢 / 蹬 / 踹算外力

## Follow-up 036 — 2026-09-27 10:40:00
Source: user_input/follow_ups/202609.md - section 036
Summary: 报问题先提流程改进（写进 CLAUDE.md）；A 说话人朝向闸门 · B 画面相对走位 · C 场景图审图 · D previz 弯腿姿态贴地（用户逐项同意后落地），再用新流程修 shot04 与全集同类

Auto-updated:
- `CLAUDE.md` — 新节「用户报问题：先提流程改进，同意后再修」；索引加 rule 32 / 33 两行
- `tools/shot_overhead.py` — `face_vec` / `screen_view` / `SPEAKER_BACK_DEG`
- `tools/szzl_shot_engine.py` — 说话人背对镜头即 blocker（纯侧脸 warning）；`走位:` 自动接「画面里（按机位换算）」一句；说话镜负向 `NEG_SPEAKER`；剧本行尾「背影：理由」放行并改口型指令；挂场景图前调 `scene_review.gate`；`plate_png` 抽成一处
- `tools/scene_review.py`（新）— 审图清单 S1–S6、`审图` 行读写（绑 sha256）、生成器闸门
- `tools/previz/build_previz.py` — 弯腿姿态每帧按最低点压回地面（坐 / 踏剑除外）；自检加人物离地 > 0.15 m 即 blocker
- 平面图 S04（6–13s 斜侧两人 3/4、13s 起两人之间反拍治安官）S05 S06 S08 S09 S10 S11 S13 S14 S15 S16 S18 S22 S23 S24 — 首扫 36 句说话人背对镜头全部清零：机位绕瞄点转（求解最小转角）、切反打、或改朝向；S02 "Behind me!"、S10 洞口剪影两句、S24 收尾两句标「背影：理由」；S13 机位挪到摊子后面反拍、17–20s 往左带
- 剧本 / 生成器 — S04 S08 S09 S10 S11 S13 S16 S23 的镜头、分镜、镜内状态文字同步；S16 远处红面罩挪进 8–16s；S04 / S13 / S16 景别档与机位标签
- 场景图 — ep01 九个场景 40 张审图并记进各自的 md：38 张通过（5 张带备注），bg177 主厅（石柱半截，S1）与 bg3-4 支巷壁龛（油灯亮着，S6）不过；两张卡改 prompt 后重出——bg177 第二版仍是半截柱，第三版把「柱子一直顶到屋顶、柱头托桁架横梁」写进场景行才对；复审通过
- `.claude/agent_refs/project/ai_video.md` rule 32 / 33（新）；`ai_videos__站位朝向` 机检先行一节；stage 2 playbook 铁律加第 6 条「出图后先审结构再用」
- 生成器全过、回读通过：24 镜 612 s；平面图 blocker 0；纯侧脸 warning 保留（含 shot04 治安官与部分对话镜）

No conflicts found in: 台词与切口（script_tools 全过）
- 037 续（2026-09-27）：资料包挪进每镜目录 `资料包/`（要拖的文件在 `资料包/上传/`），`.gitignore` 改 `ai_videos/**/资料包/`、`tools/assets/scanner.py` 跳过 `资料包/` 不进 R2（assets 测试 22 过）；主体名大小写照卡目录（`wow_c1_Aaron`，在即梦主体页核过）；ep01 全 24 镜资料包已建，check 全部最新
- 037 再续（2026-09-27）：资料包里不要「上传」子目录、且必须与原始文件永远一致——文件直接放 `资料包/`，改为**硬链接**到原始文件（原地改写即同步、不多占盘）；原文件被整个换掉时由 `.claude/settings.json` 新增的 **Stop hook**（每个 Claude 回合结束 `seedance_kit.py sync --all --quiet`，全仓约 1 秒）与 `open` 前的对齐补上；源文件缺失时清空旧素材标「暂不可用」；镜被删资料包跟着删。ep01 全 24 镜已重链，check 全部一致


## Follow-up 037 — 2026-09-27 14:25:00
Source: user_input/follow_ups/202609.md - section 037
Summary: 新增对白通读机制（子代理带全剧上下文 · 母语口语 · 对话接续）＋ 指纹章（台词 / 动作 / 情节任何一处改了，生成器强制重读）；ep01 首跑两名审稿人，采纳全部 major 与多数 minor

Auto-updated:
- `.claude/skills/ai_videos__对白通读/SKILL.md`（新）— 九问 N1–N9（接得上 · 母语口语 · 声口 · 分量 · 称呼 · 信息边界 · 呼应 · 世界口吻 · 念得出来）、修法、盖章
- `tools/dialogue_review.py`（新）＋ `tools/szzl_shot_engine.py` — 指纹 ＝ 剧本每镜正文（去备注）＋ 生成器情节 / 动作；`--dialogue-stamp` 盖章进 `4_剧本/episodes/ep01/dialogue_review.toml`；对不上即 blocker（负向测试：改一个标点即拦下）
- `.claude/agent_refs/project/ai_video.md` rule 34；`CLAUDE.md` 索引；stage 4 playbook QC；`全流程编排` 表；`审查总编排` 1c 步
- `4_剧本/episodes/ep01/script.md`（`dialogue.md` 重生成）— S01 "Aaron, sir." · S03 "closer every week" · S04 "Paladin." / "Trying to be." / "...Warrior." 与 "ten will do" · S05 伊根 "fair's fair. Abbey'll buy the rest." · S07 "Shorten your grip." · S08 "That camp was the easy part."（不再转述没演过的命令）与 "See? They always run!" · S09 "Just for show." · S11 立论那段放宽到 18–23s、维里挪到 23–28s、治伤默数 · S12 "in front of you" 并补「再抬锤、锤头一闪」让「把光叫回来」看得见 · S13 "Marshal paid sixty-five each! Never held this much." · S14 "made something of myself" · S16 "All of them." 与 "Three more days." · S18 杜克拼完 D-U-K-E、米莉 "Their boss — shack up the hill. Sits there all day." · S22 时间窗重排 10–16 / 16–22 / 22–26（动作分段同步）· S23 "I'll keep mine. Thank you." / "Same here." · S24 "Goldshire. You're going home." · Unbreakable 的中文意思改「打不烂」
- 生成器与平面图 S04 S10 S11 S12 S18 S22 同步（S11 切点 22→23s，S22 结尾推镜落到萨缪尔接锤）
- 人物卡与 `relationships.md` 的声口样本同步到现稿（子代理 voice-sample-sync-03，只动样本段）
- 生成器全过、回读通过；平面图 blocker 0；Seedance 资料包已对齐

未采纳（理由）：维里加 "...Watch yourselves."（时间窗会超 3 词/秒）；S19 放宽时间窗（要压缩已调好的打斗节拍并重渲 previz；现 2.63 词/秒）
已知未处理：人物卡里的状态时间线（伤 / 盾 / 锤 / 光环）与出场镜号仍是旧 27 镜稿，与现稿对不上

## Follow-up 038 — 2026-09-27 16:20:00
Source: user_input/follow_ups/202609.md - section 038
Summary: 观众跟不上任务线（S05 不知道去干什么、为什么）→ 冷眼观众（只看屏幕）＋ 目标账本 goals.toml（机检 G1–G6）＋ 写作规则；三轮修改后没看懂的镜 18 → 12 → 5

Auto-updated:
- `.claude/skills/ai_videos__冷眼观众/SKILL.md`（新）· `tools/script_tools.py` `shot_screen` / `screen` 子命令（「观众看得到的」唯一定义：场景展示、画面动作、说出口的台词；不含中文意思、行尾说明、备注、情绪、场景标签）
- `tools/goal_ledger.py`（新）· `tools/dialogue_review.py`（两枚章：对白通读 + 冷眼观众，同一个指纹）· `tools/szzl_shot_engine.py`（build 时跑目标账本、`--viewer-stamp`）；负向测试：删掉 S05 那句接话即报 G1 / G4
- `4_剧本/episodes/ep01/goals.toml`（新）— 10 件事：学当圣骑士 · 狗头人 · 狼肉 · 矿 · 父亲的锤 · 红面罩 · 葡萄 · 头目悬赏 · 闪金镇 · 杜克的谎
- `script.md` / 生成器（`dialogue.md` 重生成）— S04 "Kobolds took the north mine. Start with the woods — ten will do."（窗分界 13→12s，反打切点跟着挪）· S05 杜克接话 "Kobolds first. Then wolves!" · S07 "I keep swinging too big." · S08 "Nine down. The rest live in there." · S10 "Hold still — I can fix that." 与 "Dad's hammer—" · S11 维里丢下两只钱袋 "Nine's close enough. …bring twelve…" · S13 "Sixty-five each!" · S14 "...They think I made the Guard." · S21 账本页眉 *Wages owed* 与 "...Wages." · S22 "...and the mine's quiet." / "I said not today. ...Good. …" / "Goldshire's short of hands."，杜克在第一次听到闪金镇时僵住
- `shots/shot05/planning/overhead.toml` — 0–7s 机位挪到林缘东北侧朝西南，杜克回头答话时脸朝镜头（原机位在两人身后）；previz 重渲
- `.claude/agent_refs/project/ai_video.md` rule 35；`CLAUDE.md` 索引；stage 4 playbook；`全流程编排` / `审查总编排` 1d；`对白通读` 注明共用章；c2 卡声口样本
- 审稿：对白通读复读三 无 blocker / major；冷眼观众复看 v3 前五全修；生成器全过、回读通过；两枚章 4c0b926ad5d4

达到 3 轮上限，剩余交用户定（均为 minor）：
- 对白：S07 加称呼 "Brother, …"；S21 "...Wages." 与数人头拆窗（16–18 / 18–22）；S22 "So much for 'not today.'"（母语里更像自嘲）；S22 10s 分界挪到 9s（四句挤 6 秒）
- 观众：S23 亚伦交斧时对「工钱」毫无反应（一个眼神即可）；S12 祝福看不出效果；S14 前 18 秒不知道去哪；S18「Brother Neals」没介绍过；S24 林边的人与加瑞克分不开

## Follow-up 039 — 2026-09-27 18:35:26
Source: user_input/follow_ups/202609.md - section 039
Summary: 第一件任务交代全（S04 20→30s）；职业本事按升级一样一样解锁、学了要用出来（G7）；生成器写完当场对齐资料包并报出改了哪几镜。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S04 30s（劫过路的人 / 耗子脸顶蜡烛 / 林子里扎营 / 十个 / "Ten? Easy!" + 亚伦点头 / 有工钱；穿门开场、脚步先到）；S05 伊根指路；S07 "The mine's next." + 萨缪尔点掌心教「治伤数三下」+ 隔壁冲刺闷响；S10 数人指人；S11 回声 "Three counts — I never got there."；S12 放低身子盾在前冲进门 "can't stop!"；S17 冲锋实战 "See? I can stop!"；全集 612→622s
- 4_剧本/episodes/ep01/goals.toml — kobolds 接下改 S04；新增 `[[skill]]` 七条本事（学会 → 用出）
- tools/goal_ledger.py — G7：本事学会与用出都得在屏幕上、用在学会之后（反例三种实测能拦）
- tools/seedance_kit.py `after_write` + szzl / xj 两个引擎 — 写完 shot 当场对齐本集全部资料包、报出这次真改了哪几镜
- tools/szzl_shot_engine.py — 注明背影的说话镜提示改说「背对镜头，已注明理由」（原来误标纯侧脸）
- tools/gen_shots_szzl_ep01.py — S04/S05/S07/S10/S12/S17 情节、动作、机位、镜内状态、情绪同步
- shots/shot04 — overhead 五段机位（6 斜侧 / 12 反打 / 20 斜侧 / 26 反打）、正门里侧开场；镜内 5 段触发 previz，已渲 p1/p2
- shots/shot12、shot17 — overhead 节拍文字同步、重画
- 2_世界观人设/characters/c7、c1 — 说话模板同步新台词
- .claude/agent_refs/project/ai_video.md — rule 35 写作规则 6（第一件任务交代最全）、7（本事学了要用出来，G7）；rule 12.4-K ④（生成器写完当场对齐资料包、回复里报改了哪几镜）
- .claude/skills/ai_videos__冷眼观众/SKILL.md — 目标线之外再理本事线
- CLAUDE.md — 资料包一行：生成器当场对齐 + 改了 shot prompt 必须告诉用户

Reviews: 对白通读 dialogue-reread-03 两轮 + 2b PASS；冷眼观众 cold-viewer-03 14/24 → 七镜 2/7 minor（已修）；两枚章 0612d4f544e2。
留账（不在本次范围）: S11 红面罩没人接下（窗口字数满）；S14–S15 回矿取锤没说出口；S24 窥视者易被当成加瑞克；S02 锤光像运气；祝福画面上几乎看不见。

No conflicts found in: 1_立项/concept.md, 3_大纲/arc_outline.md, states.toml

## Follow-up 040 — 2026-09-27 18:55:19
Source: user_input/follow_ups/202609.md - section 040
Summary: 冷眼观众留账五项全修（红面罩有人接、回矿取锤说出口、窥视者与加瑞克分开、锤光不是运气、祝福看得见）。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S11 29s：杜克「Twelve? Easy!」、肩上一抽、亚伦转头看他一眼，情绪收在大话上；S14 亚伦「Back to the mine. Dad's hammer first.」；S24 窥视者瘦高笔直、干净深灰外衣、皮手套、空手；S02 亚伦盯着刚闪过的锤头愣住；S12 杜克低头看手攥拳；S17 一剑把暴徒连棒劈退两步、扔光点名亚伦；S15 往外走时矿巷已空；全集 622→623s
- 4_剧本/episodes/ep01/goals.toml — bandanas / bounty 由 accept_note 改为 accepted「Twelve? Easy!」；hammer 提醒词去掉「肩」
- tools/gen_shots_szzl_ep01.py — S02/S11/S12/S14/S15/S17/S24 同步
- shots/shot11 — overhead 延到 29s、维里 28s 才走；高机位挪到 (48.5, 62.2)——原机位杜克说话时被亚伦挡住（生成器可见性闸门拦下），现杜克 3/4、维里侧脸

Reviews: 对白通读 dialogue-reread-04 PASS（补亚伦那一眼）；冷眼观众 cold-viewer-04 五项全部看懂，1/7 为 S15 旧项已补；两枚章 d3d357aac041。
Shot prompts 改动：shot02、shot11、shot12、shot14、shot15、shot17、shot24；资料包 24/24 一致。previz 动作未变，无需重渲。

No conflicts found in: 1_立项/concept.md, 3_大纲/arc_outline.md, states.toml, c18 卡（加瑞克粗壮，与窥视者分得开）

## Follow-up 042 — 2026-09-27 21:11:10
Source: user_input/follow_ups/202609.md - section 042
Summary: 出片 S04 分身 + 锤悬肩、S05 见狼低头 + 锤变斧 + 没打到狼 → 先改流程（rule 36：持物支撑 / 道具身份锁 / [[hit]] 命中 / 烘焙对账 / 跳切防分身 / 出片审片，用户同意 A–D），再修 S04、S05 与全集同类。

诊断（出片 vs previz vs prompt）:
- S04：仓里只有 15:39 的旧 20s 出片（无分身）；新 30s 版 6s 跳切前新位置已在画、人不在画 → 分身；previz 里根本没有锤、文字「横挎肩上」没写手。
- S05：previz 本身就弯腰低头（亚伦 8–11.8s 编排前倾 6°、烘出来 73°：同姿势挪 0.46 m 被判 Bezier，把后面的大抡提前拉进来）；锤代理是橙柄细棍、prompt 没写「不是斧子」；命中时刻没声明、狼是方块。

流程（工具）:
- tools/szzl_shot_engine.py — carry_gate（扛 / 挎 / 背没手没带即 raise，按句回读产物）；asset_lock 带「不是 X」+ confusable_negatives；hit_clause（prompt `命中:` 行）；hit_coverage（有敌意的镜打击段没 [[hit]] 即 raise）；跳切 prompt 写「每个人只有一个」+ NEG_GHOST；previz_config 写 [[命中]] 与 [[角色.持物]]；平面图闸门 build 时逐镜跑；carry() 读口
- tools/shot_overhead.py — [[hit]] schema + hit_errors（够得着 / 面朝，群体 +1 m，反身 back）、ghost_errors（跳切防分身）、in_view；平面图图例列命中
- tools/previz/build_previz.py — 持物（扛肩R 姿态 + 锤柄锤头挂手与肩）、Cascadeur 烘焙对账（前倾差 > 20° blocker）、命中贴身（≤ 0.35 m；无兵器件按身体 + 兵器长）
- tools/cascadeur/choreo.py — 同姿势段与 ≥ 0.6 s 慢过渡一律 LINEAR（SLOW_S）
- tools/equipment_lib.py — carry() / confusable()；item.toml：e5110 [carry] 扛肩 / 双手握 / 拄地 / 靠腿 + confusable，e5111 挂腰，e5113 扛肩 / 提，e5205 背后
- tools/render_review.py（新）+ .claude/skills/ai_videos__出片审片（新）— 出片落盘出逐秒拼图、命中 / 跳切特写与清单，子代理按 R1–R6 看图判
- tools/previz/review.py — 打印命中结果；shot02/05/20 钩子锤柄改褐色
- .claude/agent_refs/project/ai_video.md rule 36；CLAUDE.md 索引；审查总编排 1e；stage5 4b-1、stage6 出片审片

修（用新流程）:
- S04：0–6s 两人开场就在镜头前四米、广角推进（防分身）；previz 亚伦扛锤、右手握柄；重渲
- S05：Cascadeur 重烘（前倾对上编排）；三下命中声明并 previz 贴身 0.06–0.14 m；锤写清 0–7s 扛肩、8s 起双手握，伊根手里只有剥皮刀；伊根进蕨丛推迟到 17.1s（防分身）；重渲
- S02 / S20：重烘（S02 杜克 4.5s 前倾 44°、S20 加瑞克多处走样）；S20 杜克顶盾挪到 23.0s、加瑞克 23.2s 才倒
- 21 下命中写进 S02 / S05 / S06 / S10 / S14 / S17 / S19 / S20（含故意落空与反身踢）；S06 亚伦 12s 上前半步；S10 镐啄盾 13.2s
- 持物：亚伦扛锤全集引用装备卡；钢盾背后用背带；S17 暴徒单手握棒；S21–S23 杜克的斧写清右手，S22 别进腰带空出两手、亚伦拄锤靠腿；S23 从腰带抽斧
- previz 重渲 S02 / S04 / S05 / S06 / S20；24 镜 prompt 全部改写（装备锁带「不是 X」、负面词加易混物）；平面图 24 镜 blocker 0；资料包 24/24 一致

Reviews: 对白通读 dialogue-reread-04 Round 4 PASS；冷眼观众 cold-viewer-04 Round 4 PASS；两枚章 5713db0fac22。

No conflicts found in: 1_立项/concept.md, 3_大纲/arc_outline.md, goals.toml, states.toml

## Follow-up 041 — 2026-09-27 21:44:46
Source: user_input/follow_ups/202609.md - section 041
Summary: 非人生物的 4 秒建立视频按原典叫声出声——原声不下载不上传（w18 L4），改为文字时间轴 + 许可干净的真实录音作音色参考；七条全部重出。

Auto-updated:
- 0_research/parts/w24_怪物叫声.md（新）— 七种怪 0–3.5 s 叫声时间轴、`声音:` 行、负向、20 条事实、10 行误传黑名单；Q8 已查（音频 2–15 s、≤3 条）
- 0_research/blacklist.md、negatives.txt — build_blacklist 并入 w24（405 行）
- 2_世界观人设/characters/{m1,m2,m3,m5,m6,m7,c12} — 新增 `## 叫声设计`（说话 / 声音 / 负向，唯一出处）；turntable 节重生（叫声模式 + 声音参考）；m6 音量措辞改「比说话声低一截、但听得见」
- characters/{同上}/ref/audio/ — 13 条真实世界录音（PD 4 · CC BY 5 · CC BY-SA 4，许可见各 refs.md；m7-a2 狼嚎不挂）
- characters/{同上}/{卡}_turntable.mp4 + views/ — 即梦全能参考 seedance2.0_vip 出片（8 条 × 56 分）、webapp 抽三视图；旧 m1_Kobold.mp4、c12_Hogger.mp4（念人类天气句）与 m6 首版（约 −75 dB 静音）挪进 ai_videos/_deleted/
- c12_Hogger.md、m2_Gnoll.md、m1_Kobold.md、casting.md — w24 §0③ 1–3 出处更正（两句是豺狼人全族共用文字气泡 / 杂兵不说话是本剧取舍 / 狗头人那句 1.12 无配音）
- tools/gen_turntables_szzl.py — 叫声模式
- tools/gen_turntable_videos_szzl.py（新）— 图 + ≤3 条声音参考出片、账本 / --harvest、--model、成片响度回读闸门（有叫声设计却 < −50 dB 判不通过）
- tools/build_blacklist.py — 章节标题接受编号
- .claude/agent_refs/project/ai_video.md — rule 22.2 2026-09-27 修订（零台词 ≠ 零声音 / 声音参考口径 / 音量只写相对量）；rule 27 ③ 排队可绕开（_vip）
- user_input/follow_ups/202609.md — 撞号：19:20:57 那节改为 042（本节 18:57:04 在先），上一条 changelog 同步改 042

Reviews: 七条逐条回读——三视图拼版 + ElevenLabs 转写（带音效标签）+ 逐 0.2 s 响度。狗头人 "You no take candle." → squeaking → "Eee!"；霍格 "Grr. Fresh meat." 后接笑叫；其余五条零人话（growling / laughs / bubbling / 机械吱嘎 / 800 Hz 稳定长音），平均 −19 至 −41 dB。
留账: m1 转身只到约 3/4 背面（声音全对，保留）；m6 半透明、背面与正面难分；普通通道豺狼人任务 caddd938 仍排在约 3.1 万位（已扣 32 分，CLI 撤不掉，落地后 --harvest 跳过）；w24 §0③-4/5（墓地天使该不该有低语、是否只对鬼魂可见）待用户裁决。

No conflicts found in: 1_立项/concept.md, 3_大纲/arc_outline.md, 4_剧本/episodes/ep01/script.md, 5_6_分镜与prompt（shot 以 entity @ 角色，不引用这些 mp4）

## Follow-up 043 — 2026-09-28 11:26:44
Source: user_input/follow_ups/202609.md - section 043
Summary: S07 教本事观众看不懂、出片效果差（长锤成短锤、低头光变暗没出来、18 s 固定全景）→ rule 37：学会那一刻给特写 + 变化写到秒；装备锁带尺寸；本镜状态写清兵器怎么拿；出片审片 R7。S07 延到 30s 拆三件事，S12 加两处特写。

Auto-updated:
- tools/szzl_shot_engine.py — demo_errors（学会那一刻要有近景 / 特写段、变化写到秒）、hold_errors（兵器写清怎么拿）、asset_lock 带尺寸；previz 瞄高 aim_h
- tools/shot_overhead.py — 机位 aim_h；tools/script_tools.py — snippet_window
- tools/previz/build_previz.py — 持物分时段（起 / 止）、双手低握、靠腿
- tools/render_review.py — R7 关键拍兑现
- item.toml e5110 — [carry] 靠腿、扛左肩
- script.md / 生成器 / overhead — S07 30s：6–13 认毛病 + 握锤手特写、13–17 脚下特写光起、17–23 近景低头变暗抬头稳住 +「It'll keep you standing.」、23–28 掌心特写 + 治伤规矩、28–30 隔壁闷响；S12 14–16 盾面特写、22.5–24.5 杜克握剑手特写、最后半句画外先起；亚伦父亲的锤 11 镜写清拿法
- goals.toml — 祝福的「学会」落到亚伦按住杜克胳膊那一下
- .claude/agent_refs/project/ai_video.md rule 37；CLAUDE.md 索引；ai_videos__出片审片 R7

Reviews: 对白通读 Round 5（只改时刻、预放行）；冷眼观众 Round 5 PASS。

## Follow-up 044 — 2026-09-28 11:26:44
Source: user_input/follow_ups/202609.md - section 044
Summary: 相邻镜连接不自然（S03→S04 两人左右对调）、配乐在镜尾被硬切（S01–S07 七条只有 S03 收住）→ rule 38：跨镜不左右互换（用户同意 A）+ 每镜配乐在本镜内收尾（同意 C，每镜自己收尾）；B 动作承接未采纳。

Auto-updated:
- tools/szzl_shot_engine.py — axis_errors（切点两边同一人不跳左右、两人先后不对调；Shot.axis_ok 写理由放行）、music_line（每条 prompt「音乐:」收尾行）+ NEG_MUSIC、最后一个时间窗台词给镜尾留 0.8 s
- tools/shot_overhead.py — screen_x；tools/render_review.py — R8 实测镜尾响度（最后 0.25 s 比前 2 s 低 ≥ 12 dB）
- 修：S04 亚伦与杜克南北对调（与 S03 结尾左右一致，previz 重渲）；S21 开场越肩机位转向；S23 两人东西对调；axis_ok：S05 / S06 / S11 / S14 / S16 / S19（插入特写收尾、新地点远景开场、剪影换时空）；S11 29→30s、S18 20→21s 给配乐收尾；全集 631s
- 全部 24 镜 prompt 带「音乐:」行
- .claude/agent_refs/project/ai_video.md rule 38；CLAUDE.md 索引；ai_videos__出片审片 R8

No conflicts found in: 1_立项/concept.md, 3_大纲/arc_outline.md, states.toml

## Follow-up 045 — 2026-09-28 13:34:58
Source: user_input/follow_ups/202609.md - section 045
Summary: S07 重新构思——光圈要有铺垫、握锤是常识不教、重点是传授圣光之力；按原典（圣光不是神、人人身上本来就有；虔诚光环加的是身边队友；魔兽三代「圣骑士光是在场就给身边的人勇气」）与亚伦人物灵魂（要「快」、根因「去晚了」）重写；流程 rule 39：学本事的戏要有来路（G7b 机检 + 冷眼观众加问）。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S07：要快 →「圣光不快。它本来就在你身上」→ 使劲落空（隔壁闷响在后）→「不是为你自己，你会为谁站在这儿？」→「My dad. ...His leg. I was too late.」（手搭锤柄）→ 光从脚下漫到萨缪尔靴底 →「...There. It stays where you stand. For them.」；删握锤课与「低头就淡」；S10 亚伦自己说「Three counts.」；S11 亚伦先看一眼带伤的杜克、光才回来（回声 S07）
- tools/goal_ledger.py — G7b（idea / trigger；core 再要 why / fail；offscreen、rule）；goals.toml 五样本事补来路
- tools/gen_shots_szzl_ep01.py / shot07 overhead — 7 段机位（拱门 / 两人中景 / 亚伦近景 / 门洞外全身近景 / 两人脚下特写 / 萨缪尔近景 / 正面）；previz 重渲
- 人物卡 c1（第一次说出父亲的腿）、c14（声口样句）
- .claude/agent_refs/project/ai_video.md rule 39；CLAUDE.md 索引；ai_videos__冷眼观众「他凭什么在这一刻学会？」；stage4 playbook
- 研究：0_research w07 §6.1（圣光三德、圣光非神）、w02 §5.3（神圣信笺）、warcraft.wiki.gg Devotion Aura / Brother Sammuel

Reviews: 对白通读 Round 6 FIX → 6b PASS；冷眼观众 Round 6 PASS。

No conflicts found in: 1_立项/concept.md, 3_大纲/arc_outline.md, states.toml

## Follow-up 046 — 2026-09-28 16:13:26
Source: user_input/follow_ups/202609.md - section 046
Summary: S07 出片成了杜克（画外的人被挂了 entity）、教学敷衍；S10 打斗不举盾、数三下没必要、施法不呼应 S07。先改流程（用户同意 A–D），再修：S07 拆成 S07 / S08（后面各镜编号 +1，共 25 镜 657s），盾墙后施法，「数三下」→ 光从脚下一截一截升上来，Buy me three → Buy me time。

Process (rule 40):
- A 画外不挂 entity：tools/szzl_shot_engine.py 只给入画的人挂 entity、画外台词不进 Seedance（后期配音）、prompt 加「人数:」锁；挂了不入画 / 「只用声音」即 raise
- B 入门课演全：tools/goal_ledger.py G7b 扩展（core 再要 demo / method / effect、fail ≥ 2、先后）；ai_videos__冷眼观众 加三问
- C 施法一处定义：goals.toml [[casting]]（stance / hand / flow 正则、taught、cost）+ G7c（剧本）+ 生成器 cast_errors（prompt 回读）；passive 本事不算施法
- D 持盾挨打要有理由：tools/shot_overhead.py actor.shield / shield_t、hit.open、[[cast]]（exposed）、shield_errors / cast_errors；ep01 八个打斗镜补 shield，S15 狼咬补 open
- .claude/agent_refs/project/ai_video.md rule 40；CLAUDE.md 索引；stage4 / stage5 playbook

Auto-updated:
- 镜号：原 S08–S24 → S09–S25（script / goals / states / generator / 卡 / 装备 loadouts / 平面图 / previz / 目录与文件名；arc_outline、style_guide、bg5 卡不动——多集混排或旧编号）
- 4_剧本/episodes/ep01/script.md — S07（示范：光从萨缪尔脚下升起、亚伦发抖的手稳了；照做两次落空）、S08（为谁 → 成；杜克撞一下光退回地里、代价；再起、杜克站直了＝效果）；S11 盾墙堵过道口、盾后按着杜克的背起光、矿堆上那只从高处啄肩、鼠洞里那只从侧面撞倒亚伦；S12 "They go for the light. And the light isn't fast." / "So somebody buys you time."；S13 / S15 / S16 / S18 / S21 施法呼应起手；S21 不数数、光随三斧升到手；S24 "I'll buy you time."；S09 锤头不再闪
- goals.toml — aura core 补 demo / method / effect / 两次 fail、passive、casts；各样光 casts；[[casting]]
- tools/gen_shots_szzl_ep01.py — S07 / S08 新镜表、S11 重排、JUDGE / PALM / BLESS / PILLAR 按「光从脚下升起」、DEMO_SA / AURA_FIRST / HEAL_CUT
- shot07 / shot08 / shot11 overhead 重写；previz 重渲
- concept G9⑥、world、relationships、c1、c2、style_guide §4、README、publish（时长 10:57、25 镜、章节、封面改到 shot21）

Reviews: 对白通读 Round 7 FIX → 7b PASS（代价台词改 "Get hit, and it's gone. ...And it isn't fast."、S08 开头再试、撞人挪到 20.5s）；冷眼观众 Round 7 FIX → 7b PASS（S09 不闪、S11 先见鼠洞）。

No conflicts found in: 3_大纲/arc_outline.md, states.toml（伤仍在杜克左肩）

## Follow-up 047 — 2026-09-28 18:03:45
Source: user_input/follow_ups/202609.md - section 047
Summary: S10 开箱前干等、两面盾一前一后挂错；S09 数数没交代数的是什么且亚伦脸朝外；S11 打斗不对、脚下光圈走到哪跟到哪；S07/S08 改学能治伤的圣光术并按实机考据外观。先提流程改进（用户选「6 道全上」），再修。

Process (rule 41，六道产物闸门，一律从最终 shot md 回读、build 时 raise)：
- G1 空窗：tools/szzl_shot_engine.py `idle_errors`
- G2 状态对时：tools/shot_logic.py L3（`opt_in`，旧剧不回溯）
- G3 拿法一处定义：`equip_errors` + `_carry_texts`（逐字引 item.toml `[carry]`、盾不写「挎」、同槽新的上手）；equipment_lib `Stage.level_waiver`
- G4 视线目标：tools/shot_overhead.py `[[gaze]]` + `gaze_errors` / `gaze_notes`（写进 `走位:`）
- G5 previz 保真：build_previz 群体 N 个、兵器件缺了即 blocker、命中只认兵器件（planschema `HIT_OBJ` / `BODY_HITS`）、配置过期即报；新持物姿势 臂盾L / 背盾 / 单手握R / 前砸 / 前劈R / 双手前伸 / 举手R / 举手L；poses.toml `arm_up_l`
- G6 外观出处：`look(text, facts, liberty)` + facts_registry（verified_by ∈ human / ai_read）
- 施法按本事分：goal_ledger `casting_for`
- .claude/agent_refs/project/ai_video.md rule 41；CLAUDE.md 索引；格式契约 K35；站位朝向 C13；stage5 playbook 4b-2

Auto-updated:
- 考据：0_research/parts/w25_圣光视觉.md（wow.lightvfx.001–020，1.12 实机）+ refs/圣光视觉/（21 张，只进 prompt 不入画）；w07 §7 常驻光环草稿作废（wow.paladin.097 / 099 ❌、100 加注）
- 4_剧本/episodes/ep01/script.md — 通则 5–7（去光环；圣光术按 w25；代价＝脚下一乱）；S07（萨缪尔治好亚伦磨破的虎口）、S08（学成圣光术、治杜克的鼻血）、S09（保留数数，烛光入画、亚伦脸朝烛光）、S10（进镜就找就撬、旧木盾甩到背上、新钢盾上臂）、S11（重写：盾墙、起光、撞倒、蜡烛撞灭、锤被拖走）、S12 / S13 / S14 / S16、S20–S24（背上的木盾替他挡一斧）；dialogue.md 重生成
- goals.toml — 核心本事改「治伤的光（圣光术）」；两条 `[[casting]]`；bounty 目标；states.toml — 亚伦虎口、杜克鼻子
- tools/gen_shots_szzl_ep01.py — 去 AURA；盾 / 圣光 / previz 持物常量；S07–S25 对应改写；S21 `axis_ok`
- 平面图：shot08 / 09 / 10 / 11 / 13 / 14 / 20 / 21；shot21 钩子与 Cascadeur 编排重烘
- previz 重渲：shot06 / 08 / 09 / 11 / 13 / 14 / 15 / 16 / 20 / 21 / 25
- 装备：item.toml `[carry]`；e5201 / e5205；loadouts/c2_Duke 拆 L01a / L01a2 / L01b；gen_equipment build
- concept C5、style_guide §4、c1 / c2 / c14、relationships、bg3-4 卡、README
- 收尾自查：S13 为让开说话的亚伦挪了杜克，把 22.5s 手特写挪空了——改成杜克停在亚伦西南、手特写与收尾机位重摆（记在 049）

Reviews: 对白通读 Round 8 FIX → 8b PASS（S24 注释「还欠着他们的」、S12 葡萄园、S23 注释、S24 删重复的掂斧）；冷眼观众 Round 8 PASS（S11 两手摊开不碰人、S24 错字与点头）；打斗复审（S11 / S20 / S21）6 blocker / 17 major——另立 follow-up 049 处理。

No conflicts found in: 3_大纲/arc_outline.md

## Follow-up 049 — 2026-09-28 20:52:00
Source: user_input/follow_ups/202609.md - section 049
Summary: 打斗复审（S11 / S20 / S21）6 blocker / 17 major 全落在闸门盲区；用户选四组新闸门全上、blocker + major 全修。22:00 起用户睡了、交代「不确定就自己做决定」，此后全部自主完成，判断列在下面。

Process（rule 41 G7–G10，并补 G6 反面）:
- G6 反面：核错事实在 0_research 用 `banned` 列写法，正文（负面词行外）再出现即 raise（`refuted_errors`；w07 wow.paladin.097 / 099）——扫出 S13「脚下有光环」、S22「脚下光环低亮」
- G7 打击几何：`shot_overhead.strike_errors`（部位对来向、击退顺方向且不超 `KNOCK_MAX_M`；四足豁免）；previz 命中量 part 写的那件道具（`planschema.hit_part_obj` → build_previz `部位`）
- G8 施法因果：`shot_overhead.cast_order_errors`（光不早于放完、不穿己方，hit `over` 豁免从肩上方扔过去；起光前不许冲施法者扑；持械者够得着 > 2 s 不出手即 raise，hit `stuck` 兵器卡住算在拔）
- G9 道具与连续：`[[prop]]`（key / label / path / gone / moved）；`prop_errors`（静态 object 写着会动即 raise）；engine `prop_seam_errors`（同场景接连两镜同 key 首尾 ≤ 0.3 m）；`equip_errors` 动作拿法与本镜状态打架；actor `enter` / `gone`（钻出 / 钻回洞）
- G10 previz 回读：`planschema.render_inputs` + `{shot}_previz.stamp.json` / `{shot}_stills.stamp.json`，对不上即 raise；`POSE_CONTACT` 按该着地的关节贴地与自检；根位置偏 > 0.3 m（Cascadeur 体量两脚中点，切点前 0.2 s 不量）
- 顺带修的引擎问题：`场景:` 行同一场景写三遍；物件卡的易混词（矿工的镐）被压进负面词；命中行同一人同一招同结果并成一条；跌坐 / 跪 / 单膝跪悬空；新姿态 扑跪 / 按左手 / 侧踹R / 外磕R / 垂盾L
- 对白通读 049 提的闸门盲区一并补上：说话人看不看得见脸在台词窗内取 5 个点逐点量（不只量中点；049 前定稿、本轮没动的 S02 / S05 / S06 / S12 / S18 / S19 / S25 进显式遗留清单 `SPEAK_WINDOW_LEGACY`，只减不增）；画外人声从窗的第一秒起配，念的那段不许与画内台词的窗重叠，也不许说话人的脸那时在画里（人占画高 < 0.2 的远景看不清嘴，不算；`shot_overhead.subj_frac`）
- G5 补一条（夜间自查 S20 静帧发现）：色块人偶只贴地形、不贴道具，人在 ≥ 0.3 m 的 `[[object]]` 占地里就嵌进去（加瑞克「坐在劈柴墩上」看着像立在墩顶）——build_previz 加姿态 `坐墩 / 站高`（着地面取身下静态道具顶面，`ON_TOP` / `seat_z`），szzl `_seat_errors`：占地里底姿态不是这两个即 raise；旧的「坐」语义不动（别的剧在用）
- 规则：canon `ai_video.md` rule 41 G6–G10 行、32 行（窗内逐点量）、40 entity 行（画外撞车）；`ai_video_history.md` 沿革一条

Auto-updated（本镜与扫出的同类一并修）:
- S05 伊根扔的狼皮改 [[prop]]；Cascadeur 补 8.5s 键（原先 previz 根位置偏 0.5 m）
- S09 矿工每一镐写成 [[hit]]、面朝杜克；东边那拨在坡半腰不上前；亚伦 11.2s 上前半步短砸；麻袋改成开场就在
- S11 撞腿弯→就地往前扑跪；锤改 [[prop]] 拖进鼠洞；14s 才起光（亚伦挪到杜克右后一步）；一群 / 矿堆上那只每两秒内一镐；17s 杜克往前一顶；守口子两次回头；撞人的那只 calm、enter / gone；结尾单膝跪
- S13 杜克停在亚伦西南（不挡说话的亚伦）、亚伦上前半步用左手按在他握剑的右前臂上；手特写与收尾中景机位重摆；杜克的旧短剑进本镜状态（e5112 补 [carry]）
- S15 扔光前亚伦跨一步让开杜克；S16 每一镐写成 [[hit]]、光从杜克肩上方扔过去、锤与皮袋改 [[prop]]；S18 审判施法窗 14–15s、杜克的剑进本镜状态
- S20 四斧一斧退半步；暴徒一棒被架住、一锤撞回柴垛；亚伦从杜克身后绕到加瑞克右前；踢出顺方向、踉跄三步再坐；杀招 22–23s；杜克跪下时钢盾垂在身侧（e5205 补「垂放」）；落幅机位北移 0.5 m；动作句按剧本重写（去掉 047 前旧稿）
- S21 先有光再扑（11.8s 光、12s 扑）；每一斧 [[hit]] + 全程 [[guard]]；开场斧刃卡在背上圆木盾到 0.8s；亚伦 3.5s 挪到杜克身后；第四斧被顶开；杜克让开那条线；10s 起机位移到西南；两半木盾与斧改 [[prop]]；Cascadeur 重烘；e5110 补「单手拄地」
- S22 开场人与物取 S21 末帧：亚伦走去拎斧、杜克缓一口气再去捡两半木盾
- 新 G5 扫出的同类：S05 伊根改坐墩（原先坐在石头上方半空）；S06 一群矿工逃跑从矮帐篷北边绕过去（原先直穿帐篷）；S11 矿堆上那只改站高（原先只露个头）；S20 加瑞克 0–14s 坐墩、斧子一直在手
- S13 再调：扔出去的光 16.2s 收回，萨缪尔 16.5–18.2s 开口教祝福，杜克画外那句 18.2–19.8s（他进画之前）；24.5s 起萨缪尔身后越肩
- S20 对白挤（对白通读可选项）：林隙揭示缩到新地点下限 6s，对白段 6–15s，五句逐句给窗，加瑞克慢声 2.0–2.5 词/秒
- 冷眼观众 049d：S11 开打头 6 秒亚伦举锤想帮、锤头磕在头顶木撑上抡不开（这才转去用光；previz 补一下扛锤）；S16 蜡烛递给杜克照路、他在缝口举着照，亚伦 9s 把练习锤挂回腰上（本镜状态 0–9s 右手握 → 9s 起挂腰），巷口一抬锤把光叫回再扔；S20 揭示里加瑞克已坐在墩上磨斧、暴徒靠着柴垛；S13 盾面上散开的金点收成一缕倒飞回锤头（「叫回」画出来）；S04 揭示里治安官已站在祭台前；S10 结尾亚伦从巷壁上拿回锤扛上右肩（接 S11 开场）
- 对白通读 049c：S13「Plant your feet.」20.3–21.5s（杜克 19.8s 入画、20s 撞到跟前，生成器走位 / 账本 / 动作同改）；S22 数人 19.5–20.5s、接话 20.5–22s；S11「Dad's hammer—」20–21.4s（杜克 21.4s 听见才转身）；S22 动作写上亚伦肚子那一脚还没缓过来（states.toml 伤写到结束）；S25 三句逐句给窗、S25 移出 `SPEAK_WINDOW_LEGACY`；S20 加瑞克第一句 6.6s 起（先推面罩）；S21「Duke. Buy me time.」喘着说；S19「that shack up the hill」（免得读成 shack up）
- 台词时间窗（对白通读 + 新闸门）：S08 / S09 / S11 / S13 / S15 / S16 / S20 / S21 / S22 的窗挪到起因之后、说话人整窗看得见；S09 杜克停下回头说完再往矿口跑；S13 教审判拆成 8–11s / 11–18s，祝福的光 22.7s 起（手特写里）
- 冷眼观众 049：S11 杜克一离开过道口烛光就涌上来（矿工群平面图与 22.6s 机位同改）、敲手背那只也钻进鼠洞；S20 来不及转身举盾、抡的是父亲的锤；S21 一手拖着父亲的锤；S22 两人看见了没追（亚伦捂肚子、杜克包扎又湿）；S02 坡上一个举盾的少年冲下来
- states.toml：亚伦肚子（S20–S22）、加瑞克下巴（S21–S22）；S17 注释、S15 镜名
- script.md 对应镜的画面动作；dialogue.md 重生成；previz 重渲 S05 / S06 / S09 / S11 / S13 / S15 / S16 / S20 / S21，静帧逐镜重出

判断（夜间自主，理由一并记下）:
- 「起光前不许扑」只算冲着施法者去的（看路点面朝，没写面朝看最近的人）——S16 矿工冲的是堵巷口的杜克，不算
- 一群（count > 1）不查部位来向与击退上限（群心不是某一只）；四足（狼）不查部位与击退上限
- 持械者正跟别人贴身打着，不算在另一人身前干等（旧 DWELL 规则在 S11 的误报）
- S22 用错开走动（同时走动 ≤ 2 人）避开 previz：门内机位在 previz 里被墙挡，是场景 blend 门洞的问题，留给场景层
- S11 结尾「蹲」改「单膝跪」：蹲姿 previz 悬空 0.37 m，改姿态定义牵连面大，只改这一处用法
- S13 / S18 杜克的剑：动作用到、状态从没写过——顺手补上
- minor 只修文字类与顺带的几何（S11 敲手背那只的站位与鼠洞口的够法、S20 逃走的暴徒出画）；S11 一群只挤一侧、S20 15–22s 机位偏杜克背后未改
- S20 对白挤：不删加瑞克那句（人物卡的核心台词），改为把林隙揭示压到新地点下限 6s 腾出 1s
- 画外配音撞脸的豁免线取人占画高 0.2（远景 0.12 与全景 0.3 之间）：S15 横摇远景里杜克只占 4%，照旧画外配
- 坐 / 站在物件顶上不改旧「坐」的定义（duikang / sk1 等剧的配置在用，改了会连带变），另加 `坐墩 / 站高` 两个新姿态
- 冷眼观众 O4 原文写「包扎渗着血」，本剧不见血，改成「包扎又湿了一片」
- 冷眼观众 049d 可选项没改：O4 S11 17–25s 拍子太密（交时长节奏）、O5 S06「Each」、O6 S08 看锤、O8 S13 一次就成——留给下一轮
- 对白通读 049c 可选项没改：S23 10–16s 17 个词四次换人（要挪 10s 切点或删「...Good.」，动到未改镜的机位）——留给下一轮

Reviews: 打斗复审 fight_review_047（blocker / major 全部处理）；对白通读 049 FIX → 049b FIX → 049c FIX（3 个时间窗 + S13 / S22 两处生成器文字）→ 049c 复读 PASS；冷眼观众 049 FIX → 049c PASS → 049d FIX（3 必修）→ 049d 复读 PASS；两枚章同指纹 d0d4abcbbdbf（130 句）。写盘：25 镜全改（本轮 047 + 049 的内容与引擎改动都在这一次落盘），回读通过；资料包 25 镜全部与原始文件一致。

Remaining（下一轮）:
- 时长节奏复核（冷眼观众 049d 复读）：S11 17–20s 抢锤 / 拉锯 / 敲手 / 拖进洞挤在 3 s；S13 11–18s 加了「叫回」更满；S22 19.5–22s 杜克起身、立两半木盾、拍一下、接斧——可把「立好两半木盾、拍一下」挪到 8–16s
- 对白通读 049c 复读可选：S10「...Grandad watches my back.」挪到 19.8–21.2s（拍木盾时说、说完亚伦才拿锤）——盖章要对着审过的那一版，没在审后再改
- c2-2 立绘视图要重出（047 起挂账）

No conflicts found in: 3_大纲/arc_outline.md, goals.toml（本事与施法定义未变）

## 流程改版（common-level，用户批准调研对照第 1 / 2 / 3 / 6 / 7 / 8 条）— 2026-09-29
Source: 主会话对照网上 AI 短剧 / AI 影视做法的调研后，用户批准「帮我优化下 1，2，3，6，7，8」；音频模式由用户选 native。
Summary: 出片前整集 animatic 过审（rule 44）、上传精简 Seedance prompt（12.4-P）、音频模式 native（12.4-H2）、成片后期四环（42）、整集观感 + 观众回路（43）、规则库拆成现行规范 + 沿革。

Auto-updated（本剧）:
- seedance.toml — `audio_mode = "native"`、`legacy_eps = ["ep01"]`（ep01 不查 animatic 闸门、精简稿超长只警告）、`negatives`（精简稿【不要】的画风项）
- 5_6_分镜与prompt/episodes/ep01/shots/shot01–25/shotNN.md — 新增「## Seedance prompt」块（设计稿仍是第一个 text 块）；精简稿中位 2081 字（设计稿 3629），17 镜 > 2000（legacy，只警告）；配音块首行由「01集」改为按集号生成
- ep01/all_shot_prompts.md — 改汇编精简稿；资料包 25 / 25 与原始文件一致（prompt.txt ＝ 精简稿）
- ep01/ep01_animatic.mp4 + animatic/ + viewing_animatic/review.md — 整集 animatic 与观感审：前 38 s 无钩子（狼 00:38 才出）、01:09–02:07 三个 NPC 连发任务、每镜 21–30 s 节奏平
- ep01/viewing/review.md — 已拼 7 镜成片的观感审
- ep01/post/、ep01_final*.mp4、ep01*.srt — finish_ep 试跑产物（native，−14 LUFS）

Process（全局）: tools/{prompt_compact, animatic, viewing_packet, audience, check_canon}.py、tools/post/*、tools/{seedance_kit, indextts_dub, mux_av, szzl_shot_engine}.py；.claude/agent_refs/project/ai_video.md（现行规范）+ ai_video_history.md；CLAUDE.md；ai_videos__全流程编排（SKILL / BLUEPRINT / stage5 / stage6）；ai_videos__格式契约 K10 / K15 / K22；新 skill ai_videos__整集观感；Stop hook 加 check_canon。

- 1_立项/concept.md E1 / E2、2_世界观人设/style_guide.md 声音节 — 改成 audio_mode = native（原「Seedance 自带音全部去掉」与用户选定冲突）

No conflicts found in: 3_大纲/arc_outline.md、4_剧本/episodes/ep01/script.md、states.toml、goals.toml

## Follow-up 050 — 2026-09-29 09:37:05
Source: user_input/follow_ups/202609.md - section 050
Summary: 角色之间时不时加风趣幽默（对话 / 小支线），不离开主线；本轮只出点子给用户挑。

Auto-updated:
- （无）点子已提给用户，选定后再改 ep01 / ep02 剧本与分镜

No conflicts found in: 1_立项/concept.md（基调本就是「喜剧骨 + 正剧心」）、c1 / c2 人物灵魂与声口

## Follow-up 048 — 2026-09-28 18:13:15（阶段 4 剧本稿 + 过审修订，2026-09-30）
Source: user_input/follow_ups/202609.md - section 048
Summary: ep02《Acting》阶段 4 出稿：43 镜 746s（用户批准 690–750s），等级 5→10；五路审稿（台词 / 冷眼 / 对白 / 逻辑 / 剧情连贯）4 致命 18 重要全修，小问题按审稿改法落。

Auto-updated:
- 4_剧本/episodes/ep02/{script.md, dialogue.md（生成）, goals.toml, states.toml} — 新建；过审修订：S32–S36 仇恨规则 / L1 / L2 重排、S35 苏伦娜的火不再悬空、S15 审判照 ep01 定稿、S21 why 改 "is there one for him?"（与 ep01 力量祝福不撞）、S12 便条去处说清、S29 消息来路、S39 项圈上桌、S27 / S38 删复述画面的台词（L3）；749 → 746s
- 4_剧本/script.toml — `[episode_overrides] ep02 = [690, 750]`；tools/script_tools.py 读这张表
- 2_世界观人设/characters/c19–c34 — 16 张新卡（tools/gen_npc_cards_szzl_ep02.py 生成，共用 ep01 的 render）；casting.md 加 17 行 voice
- 2_世界观人设/characters/{c1_Aaron, c2_Duke} — ep02 成长轨迹；c2 前史补「父亲知道」
- 2_世界观人设/characters/c14_Brother_Sammuel — 「Not yet」移给 c19 维尔海姆，萨缪尔不再用
- 2_世界观人设/relationships.md — 新节「闪金镇与南坡（c19–c34 · ep02）」；Aaron—Duke、霍格、亚麻面罩三行续上 ep02
- 2_世界观人设/scenes/registry.toml + bg805–807 最小卡（锚点 prompt 与平面图留到资产阶段）
- divergence.md #20 — 保护祝福出光（用户定）
- tools/check_stage2.py — characters/ 下跳过非目录

待用户：幽默点子 H1–H5（050）挑选；script.md 文末「待确认」6–8（S32 / S40 偏离节拍表 v2、S29 改法）。
No conflicts found in: 1_立项/concept.md（G13 ep02＝艾尔文 6–10 级）、3_大纲/arc_outline.md、ep01 goals.toml 的 [[casting]]

## ep02 阶段 4 复核（follow-up 048 续）— 2026-09-30
Source: `.audit/…/shengji_zhilu-20260928-181315/spawns/qc-verify/output.md`
Summary: 复核审稿：第一轮 blocker 全清；新发现 2 major（S35 亚伦换位、S32 沃尔特干站）+ 8 minor，全按改法落；746s 不变。

Auto-updated:
- 4_剧本/episodes/ep02/script.md — S03 S16 S32 S33 S35 S40 与文件头状态轴；dialogue.md 重生
- 4_剧本/episodes/ep02/goals.toml — 跺地一击 casts 片段「两个强盗」（S32 起强盗数统一为两个）

No conflicts found in: states.toml、relationships.md、c1 / c2 卡

## ep02 剧本对账 w26 技能全表（follow-up 053 调研结果）— 2026-09-30
Source: 技能一致性会话（053）的 `0_research/parts/w26_技能全表.md`
Summary: 定稿后按原典核对改四处，镜长与台词不变：苏伦娜译名、她那句进战句的出处、NPC 火球的起手、圣佑术光壳不贴身。

Auto-updated:
- 4_剧本/episodes/ep02/script.md — S32 备注「凯尔东」；S32 台词注改「迪菲亚施法者通用进战句」；S32 / S33 / S34 / S35 苏伦娜的火先双手端着聚约 3 秒、再单手推出；文件头与 S20 / S25 / S32 圣佑术「贴身」改为比人高约四成的椭圆光壳
- 4_剧本/episodes/ep02/goals.toml — 圣佑术三处片段同步；dialogue.md 重生

待定：审判外观（ep01 脱锤飞出 vs 原典无飞行物）由用户在 053 里定，S15 跟着改。
No conflicts found in: c33_Surena_Caledon（卡里已是凯尔东）

## ep02 按 follow-up 053 用户裁定改技能外观 — 2026-09-30
Source: user_input/follow_ups/202609.md - section 053（裁定经技能一致性会话转达）
Summary: 审判照 1.12 原典（单手一指、无飞行物、胸口黄白光、身子一顿）；战士照原典出光（冲锋红色残影、跺地一击蓝白电火花＋冲击环＋地裂）；施法口令待技能卡原文。

Auto-updated:
- 4_剧本/episodes/ep02/script.md — 文件头第 5 / 8 / 9 条；S15 审判；S16 / S21 冲锋；S22 / S25 / S32 跺地一击；S22 备注删「战士不发光」；文末待确认第 9 条（施法口令）
- 4_剧本/episodes/ep02/goals.toml — 审判 used 片段

No conflicts found in: 镜长 / 台词（746s 不变）、states.toml

## Follow-up 053 — 2026-09-30 10:09:16
Source: user_input/follow_ups/202609.md - section 053
Summary: 技能施放一致性——全角色 / 全职业 / 第一季怪物技能调研（w26 / w27）+ 技能库（rule 45）：每个技能全剧一张卡，镜表只写 casts=，施法的样子 / 手势 / 口令 / 样片 / 音效全从卡来。用户定：口令＝读条技能念固定短句；审判按原典（无飞行物）；战士按原典发光；先建库 + 做圣光术、冲锋两条样片试效果。

Auto-updated:
- 0_research/parts/w26_技能全表.md（新）— 163 个技能（圣骑士 / 牧师 / 战士 / 盗贼 / 法师 / 术士 / 猎人 / 第一季怪物），51 条事实（wow.skill.*）；w27_技能一致性做法.md（新）
- 2_世界观人设/skills/（新）— skills.toml（职业位 / 法系颜色 / 口令政策）、registry.toml、11 张卡：k101 冲锋、k102 雷霆一击、k201 圣光术、k202 审判、k203 正义圣印（请光）、k204 力量祝福、k205 圣佑术、k206 制裁之锤、k207 保护祝福、k208 圣疗术、k401 火球术（含 NPC 变体）；k201 / k101 样片备料（样片/prompt.txt）
- 口令草稿（待用户定稿）：圣光术「Not for me. For them.」；火球术「Burn.」
- 2_世界观人设/style_guide.md §4 — 审判改原典、施法样子改指向技能卡
- 3_大纲/arc_outline.md — 12 级学会的是救赎（不是复活术）；《圣洁之书》
- 0_research/parts/w04、w08；characters/m3、m4、c3、c5 — 原典错误更正（迪菲亚掠取者无冲击波、艾尔文鱼人不投网、造水术 / 造食术 / 魔爆术、偷窃 / 绞喉 / 双武器 / 盾击 / 惩戒痛击 / 血性狂暴 / 祛病术 / 绝望祷言 / 回馈等官方译名）；w26 wow.skill.creature.003 加 banned（冲击波 / 熔岩护甲进 prompt 即拦）

Process（全局）: tools/skills_lib.py（新）；tools/goal_ledger.py（[[casting]] card 引用）；tools/post/finish_ep.py（技能音效按施放时刻贴）；tools/prompt_compact.py（时长不取整修复）；.claude/agent_refs/project/ai_video.md rule 45 + rule 40 行；ai_video_history.md 沿革一条

待做：szzl 引擎接 casts=（等 052 会话让出引擎，补丁已备）；ep01 未出片镜迁到技能卡（审判 S13/S15/S16/S18/S21、力量祝福 S13/S18、冲锋 S18、圣光术各镜 + 口令）；ep02 写 goals card 引用与口令台词（8f 会话）；两条样片由用户在即梦点生成后 adopt

No conflicts found in: 1_立项/concept.md、4_剧本/episodes/ep01/states.toml

## Follow-up 051 — 2026-09-29 10:05:00（并 050 落地）
Source: user_input/follow_ups/202609.md - section 050 / 051
Summary: S11 杜克挡着时亚伦全程在后、伤得假、「它们冲你去」不必喊；改成杜克被打倒起不来、亚伦施光半愈、两人逃出洞。先提流程改进（用户三条全选），再修 S11 与扫出的同类；050 选定的「赶路段斗嘴」同轮落地。

Process（先改流程，再修）:
- G11 打斗里友方不许干站：`shot_overhead.ally_idle_errors`——敌我有来往的第一下到最后一下（两下之间停 > 6 s 算两场）里，参战的具名友方任何 > 3 s 得有自己的出手 / 格挡 / 施法 / 反应、用盾挡下的挨打、挨打后的疼或倒地；真要等写 actor `idle = [[t0, t1, "理由"]]`，理由逐字出现在 `动作:` 里（szzl 引擎产物闸门调用，旧剧的生成器不调、不回溯）
- G12 伤要疼、要影响动作：`shot_overhead.hurt_errors`——打在具名人物身上（不是盾 / 甲 / 兵器）写 `[[hit]].hurt = [秒数 ≥ 1, "怎么疼"]`；疼的这段不出手（0.3 s 内的条件反射除外）、盾臂挨了打不照常挡满、腿挨了打不跑；疼的写法由 `命中:` 行进 prompt，一处定义
- 评审加一问：对白通读 N10「不替画面解释」（九问 → 十问）；冷眼观众加问「有没有台词在把我刚看见的东西再讲一遍」
- 规则位置：本剧 `specs/ai_video/shengji_zhilu/lessons.md`（L1–L3，新建）；canon 只把 row 34 的「九问」改「十问」

全集扫出的同类（G11 8 处 / G12 6 处）与修法:
- S11 重写（用户给的方向）：过道口容两人并肩，亚伦在杜克右肩旁短砸；10s 矿堆上那只一镐啄进杜克左肩（疼 1.4 s：左臂一软、盾垂下），11s 被撞得一屁股坐倒、撑了一下没撑起来；亚伦抡锤一扫把那群逼退、站到他身后起光——光一亮苦力全丢下杜克扑他（演出来，删掉 "They're on you! Why're they on you?!"）；光柱落下一半，15.4s 他右小腿挨一镐跪下、光散了；杜克止住血、爬起来把那一群顶回烛下；拉锯时杜克又要倒，亚伦松开锤去架他，锤被拖进鼠洞（丢锤是他选的），小矿工的蜡烛在这里撞灭（S16 伏笔保留）；两人互相架着退出去
- S12 删掉 "Why'd they go for you?" / "They go for the light. And the light isn't fast."，杜克看着亚伦发抖的手自己想明白 "So somebody buys you time."；c1 卡典型口吻、relationships "Buy me time" 行同步
- G11 同类：S05 杜克盾口对着西边那只（[[guard]]）；S09 8.8s 亚伦抢上一步短砸；S15 另一只狼扑亚伦、他俯身一练习锤砸在鼻子上（练习锤 0–10.6s 挂腰、之后右手握）；S18 杜克回过神追上两步一剑磕飞木棒、随后让开光的弹道；S21 亚伦两段等待写理由（「一手捂着肚子」「大口喘着」）
- G12 同类：S02 杜克脚后跟、S20 亚伦肚子、S21 加瑞克胸口与下巴写疼
- 050 赶路段斗嘴：S10 大圆木盾卡在窄巷两壁之间（"It's fine. ...It's fine."，换盾有了起因）；S14 套好链甲顺手扣上圆铁盔盖住眼睛，"You look like a guard." 落在这一刻（原定 0–6s 横摇远景里人只有一点大、看不清，挪到 16–21s 摊后近景）；S15 链甲一响、蕨丛里狼耳朵转过来；S17 过桥 "Twelve bandanas. Easy." / "Twelve people." / "...Less easy."
- states.toml：杜克 S11 条目写上被撞倒、光只落下一半；亚伦 S11 条目写上右小腿挨一镐
- previz 重渲 S09 / S11 / S14 / S15（S11 的「躺」姿势 previz 里腿朝天，改用「跌坐」）
- 冷眼观众 051（5 必修）：S11 亚伦一扫之后苦力看都不看他、又挤回杜克身上啄，光一亮才一齐盯住那团光转过来（光是唯一的起因）；杜克左臂软了就用右手捂左肩；杜克起身、顶人挪到 17s 切点之后（12–17s 原先挤了九拍）；亚伦小腿挨的是一记镐柄、疼得一抽、出洞时拖着右腿（states.toml 补行动受限一条）；S22 删掉 "Grandad's grip. On the new one."（画面正在缠，N10），缠好拍一拍；S12 杜克先看一眼亚伦撕开的裤膝
- 对白通读 051（8 必修）：S14 放长到 29s（本集 657 → 660s，正好到上限），16–24s 从容卸盾 / 套甲 / 扣盔、24–29s 挽回两面盾，"You look like a guard." 是真心夸不是挖苦；S12 杜克 13s 就侧过脸看、镜头 13–17.5s 推近手和裤膝，维里那句拆成两句（边走边说的背影 + 站定交代）；S05 两句吐槽钉在挨的那两锤之后、伊根先指路再摆东西；S18 / S09 / S10 窗落在起因之后；`SPEAK_WINDOW_LEGACY` 只剩 S02 / S06 / S19

判断（交互中用户已选的以外）:
- S14 头盔戏从 0–6s 挪到 16–21s：远景里看不清，近景才立得住，且让 "You look like a guard." 变成冷幽默
- S11 矿工砍倒地杜克的两下删掉：色块人偶没有往下劈的姿势，previz 贴身量不到；改成亚伦抡锤一扫（故意落空）把那群逼退、它们够不着才发愣，光一亮再扑——也更像「谁出光扑谁」
- S05 / S02 / S21 是 Cascadeur 镜：只加格挡 / 疼 / 理由，不动人的路线，免得重烘
- S18 追上去的落点让开地上爬的暴徒（贴身 < 0.8 m 会让 S18 变成必须做 previz 的镜）
- 对白通读可选项 S15「Ha!」收窄到 10.8–13s 会被挨了一锤后退的那只狼挡住杜克——改用 12.6–14.6s；S10 的 "It's fine." 保留（给 S11 的 "I'm fine" ×3 做铺垫）；S05 "Can't miss the candles." 保留
- S11 矿工啄坐倒的杜克：色块人偶的镐举在半空、够不到坐在地上的人，那两下让领头那只伏低身子（previz「扑跪」）

Reviews: 对白通读 051 FIX（8 必修全落，S15 笑的时刻在 052 落地）；冷眼观众 051 FIX → 复读 PASS。两枚章并入 052 一起盖（9689faa46d42）。

No conflicts found in: 3_大纲/arc_outline.md、goals.toml（本事与施法定义未变）

## Follow-up 052 — 2026-09-30 09:57:18
Source: user_input/follow_ups/202609.md - section 052
Summary: S11 走路像机器人、打斗僵硬；去掉「光把矿工引过来」这条线，只留亚伦施圣光治杜克、两人险险逃出洞，锤在逃跑时丢下。先落用户选的四条流程改进，再用新流程重写 S11、补扫出的同类。

Process（先改流程，再修）:
- ① previz 用法：设计稿与上传的精简稿同一句「只锁站位、走位路线、机位与动作时刻，不取长相，也不照搬白模人偶的姿势——人走路要有重心起伏、摆臂和脚下的分量，打斗要有预备、发力和收势的惯性」（szzl `PREVIZ_POSE_NOTE`，`prompt_compact.compact(doll_note=)`）；每镜负面词加「机器人般僵硬的动作，木偶感，滑步」（`NEG_STIFF`，设计稿与精简稿都带）
- ② G13 攻防镜用 Cascadeur：具名人物出手或挨打的镜，previz 里人体必须是 Cascadeur 烘的真人动作（`previz_fidelity`；已出片的 S06 / S09 进 `CASCADEUR_LEGACY`）
- ③ 白模人偶走路加步态：两腿按走过的距离交替迈步（`build_previz` WALK_*）；引擎版本 `planschema.PREVIZ_ENGINE` 进渲染戳，已出片的 S01–S09 走 `PREVIZ_ENGINE_LEGACY`
- ④ G14 动作写概括：一个机位段里标了时刻的节拍平均间隔 < 1.5 s 即报错（`density_errors`；已出片的 S01–S10 走 `DENSITY_LEGACY`）
- 规则位置：本剧 `lessons.md` L4–L7；canon 不动（单剧教训）

顺手修的工具毛病（做 S11 时撞上的）:
- `choreo.py`：镜内硬切人换位置的那几键一律 LINEAR——Bezier 把 25s 切到洞口的十几米跳变甩出去，骨盆被甩到洞外 16 m
- `build_previz`：Cascadeur 体坐在地上（骨盆离地 < 0.45 m）时站位取骨盆、不取两脚中点
- `review.py`：建场前先删上一轮的静帧，建场失败不再拿旧静帧拼图冒充
- szzl `_act_segs`：`动作:` 按机位段切到下一段开头（原先只取到段里第一个「；」，施法呼应 / 看点 / 空窗三道闸门都只看了半段）
- `prompt_compact._people`：同一张卡的几个人称呼并列（原先最后一个的称呼顶掉前面的）
- S12 负面词去掉「治疗光柱 / 金色光柱」（正文写着白芯金边的光柱，与 S20 / S21 同一处理）

S11 重写:
- 6–12s 不变（过道口并肩挡、矿堆上那只啄进杜克左肩、坐倒起不来）；12–25s 一条手持长镜（岔口南口低机位，后段倒退跟拍）：亚伦一锤扫灭领头两只帽顶的蜡烛、把那群吓回过道口，揪着后领把杜克拖进岔口，右膝砸在碎石上跪稳、按住他 "Hold still — I can fix this."，起光、光柱罩住杜克——他长出一口气、血止住、左臂仍垂着（没治完，S12 再治）；那群挤在过道口重新点火、谁也不敢先上，却被后面的推着一点点挪近；光一散已在两步外，一窝蜂冲过来；两人互相架着站起来，亚伦伸手去捡锤、刚碰到锤柄，一镐擦过后背、杜克往下坠，他缩回手两手架住人逃；那群全扑向那把锤，小矿工抢先抱住、被挤得撞在石壁上蜡烛灭了（"You no take candle!"），拖进掌子面的黑里；亚伦没法回身，偏过头 "Dad's hammer—"；25–30s 洞口剪影不变（亚伦改在杜克西侧，与逃跑时的左右一致）
- 删掉：仇恨线（光一亮矿工全扑亚伦）、亚伦右小腿挨一镐柄（states.toml 那条「行动受限」删掉）、抢锤拉锯
- Cascadeur：两人全程烘焙（`cascadeur/choreo.toml` + `previz/shot11_previz.py` 挂盾 / 锤 / 掌心光 / 光柱）；previz 自检过、整条重渲
- 连带：script.md 文件头三行（圣光术、锤、双掌与右膝）、S12 情绪氛围与备注、relationships.md "Buy me time" 与「互救的对称」两行、c1 / c2 卡的恐惧与成长轨迹、world.md 败北一行、states.toml 杜克左肩与亚伦双掌两条
- S12 人情账翻过来（对白通读 052）："You owe me one." → 杜克小声认账 "...I owe you one."（新 S11 里救人、丢锤的都是亚伦）；ep02 S25 "Now you owe me two." 跟着改成 "Now you owe me one."（这回轮到亚伦欠他）

用新流程扫出的同类:
- G13：S15 / S16 / S20 的人体改 Cascadeur（各写 choreo.toml + 钩子）；S16 镜内硬切的换位挪到切点前 0.1 s；S15 练习锤按卡挂在腰带左侧
- G14：S13 / S15 / S20 / S21 的 `动作:` 写概括（每一下打在哪留给 `命中:` 行）
- G10：S13 / S14 / S15 / S16 / S20 / S21 / S25 静帧与整条按 052 引擎重渲
- 对白通读 051 遗留：S15 大笑挪到第二只狼被砸退、从杜克身边窜过去之后，拍拍被咬的链甲下摆；S12 平面图杜克那条注释（18s → 13s）

判断（交互中用户已选的以外）:
- 锤丢在哪：用户选「逃跑时丢下」；定为跪下起光前撂在手边、逃的时候两手都在杜克身上——丢锤有看得见的原因，也让那群矿工停下来去抢锤，脱身不靠巧合
- 治疗不被打断：用户要「亚伦施圣光治杜克」；起光那几秒没人来打，原因演在画里（那群刚被锤吓退、挤在过道口谁也不敢先上），不写仇恨
- "Hold still — I can fix that." 挪到跪稳之后（原先前半句背对镜头），光顺延到 15.8s
- 12–25s 并成一条长镜：治疗和逃跑在同一处，一条镜头始终看得见那群矿工在背后挪近
- 矿工为什么不趁他施法扑上来：冷眼观众建议写「被光晃得直眯眼、往后缩」，没用——那等于把光与矿工的因果换个方向请回来，也和 S16（它就是想要点光）、S21（谁出光扑谁）反着；改成那一锤扫灭了领头两只的蜡烛，它们挤在过道口重新点火

Reviews: 对白通读 052 FIX（S12 人情账方向反了）→ 复读 PASS；冷眼观众 052 FIX（丢锤不是选择 / 矿工为什么不上前 / 治疗起没起效）→ 复读 PASS；章 9689faa46d42（对白通读、冷眼观众）。
另一会话（follow-up 053 技能库）等本条写盘后再接手 szzl 引擎与 ep01 生成器。

No conflicts found in: 3_大纲/arc_outline.md、goals.toml（圣光术的施法定义未变）、S13 / S16 的借锤与换锤（锤仍丢在矿里、仍在那只小矿工手里）

## ep02 对齐技能卡（follow-up 053 / rule 45）— 2026-09-30
Source: 技能一致性会话交付的 `2_世界观人设/skills/`（11 张卡）与口令草稿（待用户批准，先用）
Summary: ep02 的施法措辞对齐技能卡；两句口令落进台词；goals.toml 的 [[casting]] 改指卡号。

Auto-updated:
- 4_剧本/episodes/ep02/script.md — 口令：S20 修士示范聚光、S32 亚伦两次聚光 "Not for me. For them."（k201）；苏伦娜 S32 / S33 / S34 / S35 聚火 "Burn."（k401），S32 她的进战句挪到 1.2–3.9s；冲锋 S16 / S21 改暗红光带＋起步扬土、被冲者僵住不倒（k101）；跺地一击 S22 / S25 / S32 改双手迸电火花＋黄转紫的尘（k102）；圣佑术 S25 / S32 写出「光壳」（k205）；苏伦娜聚火写「托」（k401）；文件头第 5 / 8 / 9 条
- 4_剧本/episodes/ep02/goals.toml — 五条 [[casting]] 写 card（k201 / k205 / k206 / k207 / k208），删 stance / hand / flow；圣佑术两处片段同步；dialogue.md 重生

检查：script_tools 746s ✔、goal_ledger 0、skills_lib check 0。
No conflicts found in: states.toml、镜长
- 补（同日）：goals.toml 加杜克 k102 / k101、苏伦娜 k401 三条 [[casting]] 与苏伦娜的 [[skill]]；script.md S22 里瑞亚示范写出「推到七八步外就停」（跺地一击的规矩），S32 / S33 / S34 苏伦娜推火那一拍写全「站 / 托 / 火球」。goal_ledger 0、skills_lib 0。

## ep02 资产阶段：屋顶口径、bg808、圣光术吟唱 — 2026-09-30
Source: follow-up 048 用户裁定（钴蓝厚瓦）；follow-up 053 用户改圣光术为吟唱（技能会话转达）
Summary: style_guide 艾尔文行改钴蓝厚瓦（原写赭红瓦，与用户裁定冲突）；五张 bg 卡同步；S11 月夜另立 bg808；圣光术口令改吟唱、S20 加 2s，全集 748s。

Auto-updated:
- 2_世界观人设/style_guide.md — 艾尔文森林行：人类房屋钴蓝厚瓦
- scenes/…/bg4 bg5 bg9 bg174 bg178 — 屋顶措辞；bg4 / bg5 已出的图（09-25，深蓝灰）标待重出
- scenes/registry.toml + bg808_杜克家农场月夜（新，平面图指回 bg805）；bg805 卡月夜行指向 bg808
- scenes/…/bg805 bg806 bg807 — 完整锚点卡与平面图；bg7 洞口补原典暗红瓦木板矿屋
- props p465–p473 + tools/gen_props_szzl_ep02.py；characters/m9_Princess；m1 / m2 / m3 卡补 ep02；casting.md 无台词名单加 m9
- equipment/loadouts/c1_Aaron.toml、c2_Duke.toml — ep02 分段（亚伦 L05a / L05b，杜克 L05a / L05b / L05c）；e5204 长枪兵之盾补 [carry] 与 owner
- 4_剧本/episodes/ep02/script.md — S11 场景 bg808 + 场景展示；S20 24s（修士吟满口令）；S32 两次聚光吟唱、与苏伦娜同时聚火；S33 开头不再重复光壳散；S25 鱼人拿骨矛；dialogue.md 重生

待用户：出图计划；m4 艾尔文强盗造型；views 锚点帧改名；锚点字数量法；gen_bg_images 给变体卡加「不照搬构图」；W6 认平面图指针；其余 bg / 物件卡的屋顶口径。
- 补（同日）：c19–c34 按现稿剧本对账约 140 处（改 tools/gen_npc_cards_szzl_ep02.py 后重生；c33 苏伦娜去掉原典模型的木杖——两手要托火）；S32 亚伦第一次聚光只吟半句 "Not for me. For—"、苏伦娜 "Burn." 错开截断（native 音频不叠声）；S30 收货人「兜帽拉起罩着头」；S22 里瑞亚示范不写盾；剧本中文「麦克鲁尔」统一为「马科伦」（nfu 译名）。748s、goal_ledger 0。

## ep02 资产阶段出图与审图（第一轮）— 2026-09-30
Source: follow-up 048 资产阶段裁定（出图计划全部批准）；053 口令改游戏内语言（技能会话转达）
Summary: 场景 12 张出图，7 张过审（bg6 / bg7 / bg8 / bg805 / bg806 / bg807 / bg808；bg7、bg805 第 2 次过），bg4 / bg5（卡是 ep01 前旧稿）与 bg9 / bg174 / bg178（屋顶发暗、缺剧本要的谷仓 / 筒仓）不过、改卡待重出；立绘 17 张 12 过、5 张（c21 c22 c29 c34 m9）改卡待重出；口令换成德莱尼语 "Pheta vi acahachi." 与萨拉斯语 "Felo'melorn!"。

Auto-updated:
- 2_世界观人设/style_guide.md — 屋顶出图写法「饱和鲜明的钴蓝色厚陶瓦」（只写钴蓝会出成炭灰，实测）
- scenes/…/bg805、bg7 — 锚点 prompt 改屋顶 / 谷仓 / 圆印、暗砖红筒瓦 / 天然岩壁；各图审图行
- 4_剧本/episodes/ep02/script.md — S01 路面照 bg6 卡改黄土大道；S36 面巾对照照 m4 艾尔文档；S20 / S32 圣光术口令、S32–S35 火球口令；S34 杜克那句挪 0.2s 让开口令；dialogue.md 重生
- tools：gen_bg_images（正文 / 送审分开计数、变体照参考构图）、check_world_scenes_szzl（W6 / W7 认平面图指针）、gen_char_images.anchor_frame（views 锚点帧一处定义，兼容 views1–3＝背 / 正 / 侧）、gen_outfit_views / gen_turntable_videos_szzl 改用它；网页端 downloads__writer 不再改名 views 目录

检查：748s ✔、goal_ledger 0、skills_lib 0。对白通读 + 冷眼观众在重读（只读；盖章等分镜生成器）。

## ep02 资产阶段（第二轮）与剧本重读修订 — 2026-09-30
Source: 对白通读 / 冷眼观众重读（spawns/dialogue-reread、viewer-reread）；立绘审图（portrait-review）；场景审图
Summary: 剧本按两道重读改 6 处（S07 二哥在军中说清、S12 奶奶那句、S19 杜汉交代火球口令意思、S20 修士只吟半句被推散＋「Fast ones cost.」挪后、S34 一问一答在口令前、S35 苏伦娜只喊半句），748s；bg4 / bg5 卡按 1.12 调研重写（镇心只有旅店＋铁匠铺＋货车摊、封闭石砌铁匠铺、石墩蓝旗信箱、旅店门廊）；bg9 / bg174 / bg178 卡补谷仓、筒仓、西瓜、屋顶有效写法；c21 c22 c29 c34 m9 卡修（ep02 防现代衣物负面词一处定义）；e2603 狮纹手套改写成半指手套形制。

Auto-updated:
- 4_剧本/episodes/ep02/script.md、dialogue.md；tools/gen_npc_cards_szzl_ep02.py → c19–c34；characters/m9_Princess；equipment/…/e2603 item.toml；scenes/…/bg4 bg5 bg9 bg172 bg173 bg174 bg178 bg180 bg181；style_guide.md 屋顶出图写法
- 审图结论写进各图 md（scene_review）

检查：748s ✔、goal_ledger 0、skills_lib 0、check_stage2 新卡 0。

## Follow-up 056 — 2026-09-30 12:06:48
Source: user_input/follow_ups/202609.md - section 056
Summary: 口令定稿（圣光术德莱尼语 Pheta vi acahachi / 火球术萨拉斯语 Felo'melorn!）+ 圣光术蓄光 3.5s 含吟唱；ep01 全部施法迁到技能卡（053 待做项落地），过对白通读 + 冷眼观众并盖章。

Auto-updated:
- 2_世界观人设/skills/k201_圣光术、k401_火球术 — 口令、念法、liberty（外语口令＝本剧写法）；k201 加「持锤」变体、k202 加「靶」变体（练手打盾）、k101 加「刹不住」变体、冲锋去掉「扬黄土」（室内不对）、[script] flow 认「拢着 / 拢起…光」
- 0_research/parts/w26_技能全表.md — 第 5 部分「口令」：wow.skill.call.001–003（德莱尼语 / 萨拉斯语官方译文、巨魔战争时精灵教人类魔法）
- 4_剧本/episodes/ep01/script.md — S07 萨缪尔示范 + 吟唱 + 翻一句、亚伦念得飞快没出来、删 "...Nothing."；S08 第一次没念自己来、被撞断，第二次慢慢念完才放；S11 / S12 / S21 吟唱（S21 一斧一个词）；S13 审判按原典（"Strike with the light on it." → "...Like at the stream." → "The light goes where you point."）、祝福萨缪尔先示范在亚伦身上、杜克冲锋拖暗红光带；S15 / S16 / S18 / S21 审判一指、胸口炸光，不再扔光 / 叫回；S18 冲锋定住对手不撞翻；剧本头圣光分级改指技能卡；全集仍 660s（S07 28 / S08 30 / S12 28）
- 4_剧本/episodes/ep01/goals.toml — [[casting]] 改为 card 引用（k201 / k202 / k204），审判本事改名「指哪落哪的光」，锚点跟新句
- 4_剧本/episodes/ep01/dialogue_review.toml — 对白通读、冷眼观众复读通过盖章（acbe6b246993；审计 .audit/adhoc_agents/2026-09-30/shengji_zhilu-ep01-skills-20260930-112034/）
- tools/gen_shots_szzl_ep01.py — S07 / S08 / S11 / S12 / S13 / S15 / S16 / S18 / S21 改 casts=，手写圣光常量（JUDGE / BLESS / HL_*）全部退役；S07 / S08 负向去掉「治疗光柱 / 金色光柱」（旧产物自相矛盾：正文要光柱、负向否定光柱）
- 5_6_分镜与prompt/episodes/ep01/shots/shot07、08、11、12、13、15、16、18、21 — overhead 切点 / 路径 / 注记，删 [[hit]] with=光；S11 / S15 / S16 / S21 Cascadeur 编排（审判 point_l）重烘；钩子里的光团改成目标胸口炸光；previz 静帧已看、整条重渲中
- 2_世界观人设/equipment/loadouts/c2_Duke.toml — S10–S13 段等级 [3, 4]（S13 学冲锋要 4 级）
- 2_世界观人设/characters/c1_Aaron、c14_Brother_Sammuel、world.md — 旧「扔光 / 推光 / 不出光」说法改指技能卡

Process（全局）:
- tools/szzl_shot_engine.py — 动作里的〔施法〕占位；施法分句按手写时刻切开、按先后插回；负向词否定施法的光 / 火即 raise（「夸张 / 过曝…」只压强度，放过）；逐拍逻辑从拼好施法分句的动作回读；[[hit]] with=光 即 raise；Cascadeur 体不叠自动手势；S07 / S08 退出 G14 遗留名单
- tools/skills_lib.py — outcome＝空 不画蓄光；previz 手势段起止钉关键帧（不再提前挪）；口令只对 成 / 挡 必念
- tools/cascadeur/poses.toml — point_l（左手往前指）
- .claude/skills/ai_videos__对白通读 / ai_videos__冷眼观众 — 技能口令是锁定咒词：不按母语口语审；外语口令全剧第一次要有人说出意思

待做：previz 七条重渲完 → 生成器写盘 + --verify + 资料包对齐 + animatic 重剪复审；S07 / S08 / 以及改过 prompt 的镜要重出片；k201 / k101 样片由用户在即梦生成后 adopt；口令录音（{键}_口令_{施法者}.wav）可选

No conflicts found in: 1_立项/concept.md、3_大纲/arc_outline.md、4_剧本/episodes/ep01/states.toml

## Follow-up 054 — 2026-09-30 09:57:57
Source: user_input/follow_ups/202609.md - section 054
Summary: 多人同镜施法调研：业内一律「拆」（时间错开、空间绑人、资产锁外观、出错逐人修）；给出推荐做法、闸门提案与待测 MC-A…E，待用户拍板，未改流程与产物。

Auto-updated:
- 0_research/parts/w28_多人同镜施法.md — 新建（结论、业内做法、Seedance 2.5 机制与实测、推荐、待测、38 条出处）

No conflicts found in: w26 / w27（互补，未改）；ep01（5 镜施法均为单人）；ep02 script（S25 已错开；S32–S35 苏伦娜的火与亚伦的圣光同框，留待阶段 5 按方案排，本轮不改）

## Follow-up 055 — 2026-09-30 12:25:00
Source: user_input/follow_ups/202609.md - section 055
Summary: c19–c34、m9 共 17 条人物建立视频由 CLI 以 Seedance 2.5 · 9:16 · 720p 出齐（立绘作 @图片1），并逐个抽三视图。

Auto-updated:
- tools/gen_turntable_videos_szzl.py — 型号加 `seedance2.5`（服务端收、CLI 帮助未列；priority 7 零排队，80 分 / 条）；`--ratio` 覆盖卡里画幅并同步改送审 prompt 的「比例」行
- characters/{c19…c34, m9}/{卡目录}_turntable.mp4 + views/{front,side,back}.png、_audio.mp3、_trim2s.mp4（网页端 CharacterViewExtractor）
- 事故：另一会话同时段用卡里默认（16:9 · seedance2.0_vip）重出 c25–c34，互相把对方的片挪进 `_deleted/`；c27–c32 已换回 9:16 并重抽 views，16:9 版留在 `_deleted/…/{卡目录}_turntable_16x9_other_session.mp4`

待用户：turntable 默认画幅是否改 9:16（改 gen_turntables_szzl.py 源头）；c34 立绘是远景背影、建立视频给了蒙面正身；m9 野猪 9:16 侧面出画；出片脚本加「同卡在途任务」锁。

## Follow-up 055（续）— 2026-09-30 人物资产一条龙做成可复用功能
Summary: 新增 `/ai_videos__人物资产 <剧名>`（`tools/char_assets.py` status / run / sheet），任一部剧补齐 立绘 → 建立视频 → 三视图，已有跳过；未实际出片。

Auto-updated:
- tools/gen_turntable_videos_szzl.py → tools/gen_turntable_videos.py（`--drama`；默认 seedance2.5；`.char_assets.lock` 一剧一进程；账里同卡在途任务等它不重提；`creature_sound` 只在这里定义）
- tools/gen_turntables_szzl.py — 建立视频画幅跟立绘块「比例:」（人物 9:16、m9 16:9），改 `gci.Job` 新签名；重写 turntable 块只改了比例行（c3 / c4 / c5 手改过的块手工只换比例）
- tools/seedance_kit.py — 抽出 `find_drama()`；projects/ai_video_management/apps/cli/extract_views.py + README
- ai_video.md rule 22.2、w24 — 工具名指针

待用户：本剧 concept G9 ⑤ 定成片 16:9，而建立视频按用户要求改 9:16——两者是否并存。
- 补（同日）：skill 改名 `ai_videos__人物资产` → `ai_videos__char_assets`（中文名在 `/` 补全里不出现）；`argument-hint` 带例子；CLAUDE.md 命名规则加「用户手敲 `/` 的 skill 用纯 ASCII 名」一条。

## Follow-up 058 — 2026-09-30（原记为 056，与「口令」056 撞号，改号）
Source: user_input/follow_ups/202609.md - section 058
Summary: 主体自动上传。dreamina CLI 没有主体接口（只有出片 / 查任务 / session），只能走网页（Chrome 自动化）；未动手，等用户定路线。
待用户：新名 `wow_c19_Brother` 与 `seedance_kit.py` 现行 `{entity_prefix}_{卡目录名}`（`wow_c19_Brother_Wilhelm`）冲突，两处须合成一处定义。

## ep02 资产阶段收尾 — 2026-09-30
Source: follow-up 048 资产阶段裁定（出图计划、只出正面、四处工具修正）
Summary: ep02 资产齐：场景 12 张全过审；立绘 17 张过（c34 known_issue）；建立视频 17 条（c26 c28 c32 m9 重出后过；c34 待用户定「不给正脸」卡怎么处理）；换装 c1-8 过、c2-5 / c2-6 手套 known_issue（shot 里另挂 e2603）；物件 9 件只出正面，7 过、p465 p472 known_issue；m9 叫声参考 2 段 CC0。

Auto-updated（本轮新增）:
- tools：gen_char_images（画幅读卡）、gen_bg_assets（负面词进模型、no_text 不挂照片、views 只出声明的面、plan）、gen_props_szzl_ep02（NO_GLYPH 闸门、只出正面）、gen_outfit_views 文件头；lessons L14–L16
- equipment/…/e2603 狮纹手套改写成半指形制（第 3 次过）；loadouts/c2_Duke.toml L05b 记手套 known_issue
- 4_剧本/episodes/ep02/script.md — 文件头第 6 条力量祝福照 k204；口令中文照卡「烈焰风暴」；dialogue.md 重生

与别的会话的协调：建立视频工具已由另一会话改名 tools/gen_turntable_videos.py（char_assets 持锁）；上午两边同时出 c25–c34 互相覆盖，人物按用户要求统一 9:16，m9 按卡 16:9。

## Follow-up 056（续）— 2026-09-30 14:05
Source: user_input/follow_ups/202609.md - section 056
Summary: ep01 迁卡收尾：25 镜写盘 + 回读通过、资料包全部一致；对白通读 / 冷眼观众复读 3 轮后盖章（287cc36eb4d7）；previz 七条（S07 / S08 / S11 / S13 / S15 / S16 / S21）重渲；animatic 重剪、整集观感重审（viewing_animatic/review.md 有效，出片闸门开）。

Auto-updated:
- 5_6_分镜与prompt/episodes/ep01/shots/shot07、08 — 旧成片挪进各自 renders/（shotNN_053前旧版.mp4），待重出
- 5_6_分镜与prompt/episodes/ep01/shots/shot07–21 — 本次写盘改动：S07、S08、S09（仅设计稿切口行，上传 prompt 未变）、S11、S12、S13、S15、S16、S18、S21
- 5_6_分镜与prompt/episodes/ep01/{ep01_animatic.mp4, viewing_animatic/} — 重剪重审；审稿给出 3 处结构建议（开场钩子 / S03–04 站桩交代 / S14–15 空档）待用户定
- tools/szzl_shot_engine.py — G4 视线闸门切分句加「；」（拼进施法分句后主语认错人）
- 2_世界观人设/equipment/loadouts/c2_Duke.toml — 见上一条

No conflicts found in: 4_剧本/episodes/ep01/states.toml

## ep02 阶段 5 分镜（五路并行）+ 059/060 节奏闸门对齐 — 2026-09-30
Source: follow-up 048 分镜阶段裁定；follow-up 059/060（d8 会话告知：G10 场景展示 > 4s 要有事、引擎 G15–G18）
Summary: S02–S43 按剧本镜号分五段并行写镜头数据 + overhead；a / b / c / e 四段写完、闸门全过后又被新节奏闸门拦下 16 处 + S19→S20 跨轴，已发回各段修；d 段（S29–S37）在写。

Auto-updated:
- 4_剧本/episodes/ep02/script.md — 10 个场景展示窗补带时刻节拍（S02 S07 S10 S12 S13 S14 S23 S24 S30 S38，G10）；S01 首句挪到【2–5s】（G16 开场钩子）；分镜回推：S08「门框」→「门廊的木柱」（露脸）、S14 补「接着又是一棒砸在盾上」、S39 补「亚伦拿了另一副」
- tools/szzl_ep02/shots_{a,b,c,e}.py + 5_6_分镜与prompt/episodes/ep02/shots/shot01–28、38–43 — 镜头数据、overhead.toml、俯视图

待定（汇总给用户）：L16 手部装备图与精简稿 ≤2000 字抢预算（S05 S07 S12–S16 S20 为压字没挂）；S16 下层掌子面要补 bg807-1 plate；p467 崩扣状态图；引擎 / 技能卡缺口 15 条待交 d8。

## ep02 打斗拆镜 + 补图 — 2026-09-30
Source: user_input/follow_ups/202609.md - section 048（分镜阶段·打斗拆镜裁定）
Summary: S32–S36 拆成 11 镜，其后 S37–S43 → S43–S49（全集 49 镜）；k401 NPC 变体加「火托在手里」的被打断样子；补图 p474 崩扣项圈（1 次过）、bg807-1 下层掌子面（前 3 次坡道画成楼梯，修工具后第 4 次过）。

Auto-updated:
- 全剧 417 处 S37–S43 引用顺移 +6（剧本 / goals / states / relationships / 人物卡 / 场景卡与 blocks / loadouts / 物件卡 / gen_npc_cards / gen_props / common / shots_d / shots_e）；shot37–43 目录只挪 overhead.toml 到 shot43–49，生成物删了重出
- S32–S36 拆镜（剧本、镜头数据、overhead、旧号引用）由 d 段进行中
- skills/k401_火球术/skill.toml — [variant.npc.look] interrupt：口令咬住、火托在掌心没推出去（skill.md 重生）
- characters/m4、m3 — 画面向负向写成 text 围栏块（`@卡:` 读得到）；m9 — S31 西边低栅
- tools/gen_bg_images.py plan_for — **不再为塞进即梦悄悄删负向词**，塞不进就走 ElevenLabs（流程改进，用户同意；bg807-1 前三次失败的根因）
- scenes/…/bg807-1_下层_掌子面 — 新 plate，过审；shots_b S16 改挂 bg807-1、动作写明坡脚落在东北角地面
- props/p474_公主的黄铜项圈崩扣 — 新状态物件（p467 崩扣）；shots_e S45 挂上
- lessons L16 — 必挂范围收窄到换装图已知画错的那件（杜克 L05b e2603）
- 引擎缺口 17 条已交 d8（#1 G16 子集误报、#2 子集写盘切口已修）

## Follow-up 059（续）— 2026-09-30 ep01 节奏重排落地 + 通读复审 + 七道新闸门
Source: user_input/follow_ups/202609.md - section 059（060 G10「景和事一起给」并入）
Summary: ep01 按 059 四处结构改法重排（628 s），G15–G18 节奏闸门落地；对白通读 / 冷眼观众 r7 盖章（2353c7e4532b）；复审与 `--check` 全跑又逼出七道闸门 / 修正；S02 / S15 Cascadeur 重烘，previz 六条重渲。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S01–S04、S07–S08、S11–S15、S20–S21 重排；S01 世界卡 0–3s → 11–17s 山谷打开时（两位审稿：压在「Name. Business.」上）；S13 杜克画外「Coming through」窗 18.2–19.8 → 18.2–20.3（配音不再 1.41× 加速，20.4s 才进画）；S14 推盔沿挪进 21–24s、24s 起钢盾垂放、台词 25.2–29.2；S21 亚伦脸部近景 16.2–17.7（念完最后一个词 + 放光在近景，光柱落在全景 17.7–18.7）、吟唱窗 12.8–17.4、行尾「16.2s 起近景对口型」；S04 庄稼汉「右手握着草叉扛在肩上」
- tools/gen_shots_szzl_ep01.py — 以上各镜的镜头 / 分镜 / 动作；S14 钢盾 `STEEL_DOWN_P`（e5205 [carry] 垂放）；S02 动作 8–9s + 9–11s 并成 8–11s（G14）
- tools/szzl_shot_engine.py — G15–G18（059）；背影台词可注明「Ns 起近景对口型」，口型指令分两段；**背影窗里说话人脸对镜头 → raise**；命中那一刻打人的与挨打的都不在画里 → 命中行写「画外（只听见）」；**`seg_errors`**：`动作:` 分段不重叠、每一刀落在段界（SEG_LEGACY ep01 S10）；**`--check` 第一层（通读章）没过也跑完产物闸门**（之前章没盖时 G3 / G5 / G10 / G14 一条没跑）；G16 按剧本第一镜判；子集写盘不写「集首镜」；beat_logic / cast_errors 在 `--only` 子集不崩（8f #1–#4）
- tools/beat_logic.py — 状态 to 镜不在镜序里不再 ValueError
- tools/prompt_compact.py — 静默镜【声音】「本镜没有人说话」、相邻人物无状态不留空标签、说话人别名同卡全认（8f #6 / #8 / #9）
- tools/skills_lib.py — outcome＝空 对瞬发卡只写 fizzle（原先悄悄拼成一次成功施放），卡缺 fizzle 明说（8f #14）
- tools/shot_overhead.py — 鞭进够得着 / 击退表；gaze 注不写「他」；硬切换站位不算「同时走动」（8f #5 / #11 / #13）
- 2_世界观人设/skills/k101（变体「半路被定住」）、k102（「敌人」→ {目标}、fizzle）；skill.md 重生
- 5_6_分镜与prompt/episodes/ep01/shots/shot01 / 02 / 04 / 14 / 15 / 21 — overhead、previz_config、静帧与整条 previz 重出；S02 删去 20.5s 过渡路点（后踢时两脚中点被拽开 0.35 m）；S02 / S15 Cascadeur 重烘（桥挂了，在原进程里 `--run-script scripts.mcp.start_server` 拉起，没杀进程）
- 5_6_分镜与prompt/episodes/ep01/publish.md — 世界卡位置
- specs/ai_video/shengji_zhilu/lessons.md — L17（`--check` 不许被第一层挡住）、L18（镜内加一刀要同步三处）

No conflicts found in: 4_剧本/episodes/ep01/{goals.toml, states.toml}
- 写盘：25 镜回读通过；本次改动的 shot：01、02、03、04、06、07、08、09、11、12、13、14、15、16、17、19、20、21、23、24；资料包 25 镜、对齐 20 个，全部与原始文件一致
- 待做：animatic 重剪 + 整集观感重审（出片闸门在此之前关着）

## Follow-up 057 — 2026-09-30 12:26:41（落地进度，会话因用量上限中止）
Source: user_input/follow_ups/202609.md - section 057
Summary: 多人同镜施法四项获批；本会话负责回读 / 修复单 / A/B 协议，引擎与技能卡（E1–E6）归技能库会话。

Auto-updated:
- tools/cast_readback.py — 新建：出片后逐次施法回读（人偶色框 + 同段背景基线、三态结论）；经 41 agent 审查 + 3 轮回归修到 v3
- tools/cast_repair.py — 新建：只修一个人的即梦局部重拍操作单 + 按帧拼回底片
- tools/render_review.py — 抽出 review_dir()，行为不变
- lessons.md — L8–L13；pending_user.md §9 — A/B 协议 MC-A…E；w28 §3 ⑦⑧ 与代码对齐

待办（下一会话接着做）：
- 第三轮回归 g1c 新问题 4 条：随身金饰在没有同位安静帧时被当成亮了；施法者挡住身后静止金饰时区域基线误扣（区域基线应只量人偶轮廓外）；「该空」量到超阈但覆盖不全只记未查；晚入画时「卡是」写成入画时刻。已知限制：蓄光从一点渐亮（3a）、自施且整段站着不动（3b@1.5）。
- 第三轮 g2c / g3c / g4c 结果未读：.claude 会话任务 w01r3vedl 输出；脚本在 scratchpad/regress/。
- 接进 render_review R9、改用 skills_lib 的 casts_in / phases / school_hue / SELF_PHASES / binding_clause：等技能库会话交付。
- bank 插入镜剪入（M3）：等卡的 bank 字段（E6）。

No conflicts found in: ep02 剧本（未改）；S13 待 E1 重排后作试点镜

## Follow-up 057 / 059（续二）— 2026-09-30 E1 排程闸门 + E2 绑定句 + 短锁定串；整集观感 r2；装备缺挂一整类
Source: user_input/follow_ups/202609.md - section 057（多人同镜四项获批，引擎与卡侧归本会话）；section 059（整集观感重审）
Summary: 技能库交付出片回读要的接口；E1 / E2 / 8f #17 落地；animatic 重剪（S01 / S02 / S04 旧片挪进 renders/）、整集观感 r2 有效（出片闸门开）；审稿追出 G3 漏查排第一的人，新闸门扫出 10 镜装备没挂、4 镜人偶空手，已补。

Auto-updated:
- tools/skills_lib.py — `casts_record` / `casts_in`（施放记录一处定义，生成器写、finish_ep 与 cast_readback 读）、`phases`、`SELF_PHASES` / `TARGET_PHASES`、`school_hue` / `card_hue`（法系色相带，卡可覆盖）、`looks`（变体 + [short]）、`restates`（跨硬切重述）、`binding_clause` / `lit_target` / `BINDING_TAIL`；卡新键 hue / short / mark 入白名单与 check
- 2_世界观人设/skills/ — skills.toml 各法系 hue（judgment call，待出片回读校准）；k102 / k207 卡级 hue；11 张卡 [short] 与 mark；k205 / k206 的「他」改 {施法者}；skill.md 重生
- tools/szzl_shot_engine.py — `hard_cuts`、`cast_restates`、`composed_action`（产物与闸门同一函数）、`_with_casts` 接重述；**E1 `cast_schedule_errors`**（②异色同段 ④放段 < 1 s ⑤跨中线 ⑥换技能没散 ⑦跨切没重述 raise；③同段同亮 warning 等 MC-A）；**E2** 精简稿【技能】`binding_text`（闸门从产物回读）；精简稿施法换短串（swaps）；**G3 剥掉「角色: 」**（排第一的人从没查过）；**拿在手上的装备必须在 props**；**`carry_previz_errors`**（要 previz 的镜人偶手上得有）
- tools/prompt_compact.py — `swaps`、`skills`（【技能】）
- tools/post/finish_ep.py — `skill_cues` 按段的源片出入点摆（88：剪掉那段的施放音效串到相邻事件），读 `casts_in`
- tools/gen_shots_szzl_ep01.py — S13 / S15 / S16 / S17 / S18 / S19 / S22 / S23 / S24 / S25 props 补拿在手上的装备；S04 / S08 / S13 / S25 previz 人偶补盾 / 锤 / 剑
- 5_6_分镜与prompt/episodes/ep01/shots/shot01 / 02 / 04 — 旧成片挪进 renders/shotNN_059前旧版.mp4（镜长已改：29 / 28 / 30 s → 17 / 22 / 21 s），animatic 重剪 628.2 s
- 5_6_分镜与prompt/episodes/ep01/viewing_animatic/review.md — 整集观感 r2（有效）：会看下去；最该改的 3 处（开场钩子 / S12–S15 找回锤子那句提前并压短 / 同窗多句台词）待用户定
- specs/ai_video/shengji_zhilu/lessons.md — L19–L21
- 写盘（三次）：本轮改动的 shot 02、07、08、11、12、13、15、16、17、18、19、21、22、23、24、25（S04 / S08 另有 previz 重出）；25 镜回读通过；资料包全部与原始文件一致；animatic 与 r2 审稿仍有效
- 待用户定：整集观感 r2 三处结构建议（冷开场 / S12–S15 提速 / 同窗多句 21 对 12 镜）；88 的 U1–U5

No conflicts found in: 4_剧本/episodes/ep01/{script.md, goals.toml, states.toml}（本轮未改剧本）

## Follow-up 060 — 2026-09-30 15:15:41
Source: user_input/follow_ups/202609.md - section 060
Summary: 后期剪辑层 P0+P1 落地——剪辑决定落成 `cut/edl.toml`（Claude 提补丁、确定性校验器、用户批），字幕按实测对齐、逐事件对白配平 + 线性响度、1080p 母带、AIGC 写回、审片绑 take sha、旧片闸门、画外 TTS 修好；剪映不用、Resolve 先不买。用户 21 点后睡觉并授权自决，之后的判断都标了 judgment call。

Auto-updated:
- tools/post/：新增 `align.py`（stable-ts 强制对齐 + ASR WER / 覆盖率，按 take sha 缓存，VERSION 3 带 CFR 帧数；`.venv-post` 跑）、`edl.py`（init / candidates / verify V1–V10 / plan；锚点带 basis 指纹，md 改了行号就停）、`qc.py`（Q1–Q9 从成片回读）、`aigc.py`、`bodies.py`、`loudness.py`（两遍线性 loudnorm，退到动态 raise）、`segments.py`（v2 时间线）、tests/（test_align 12 项、test_edl 52 组、test_qc 12 组，全过）；改 `finish_ep.py`（按 edl 出片、草稿只出 `--proxy`、正式成片先过 verify、母带存 `post/masters/v{NNN}/`）、`subs.py`（字幕时间取实测、阅读时长下限 CPS 英 20 / 中 9、镜尾句可越切点 ≤ 0.5 s）、`post_common.py`（FPS / AR / MEZZ / DELIVER / DX_TARGET / master_size / check_fps / tts_file / onscreen / take_id / stale_take 等一处定义）
- tools/：`render_review.py`（审片目录与结论绑 take sha，`verdict_ok`；旧片不审）、`indextts_dub.py`（声样读人物卡 views.mp3、首尾切静音 + 归一到 −23 LUFS、回读闸门、摆位 sidecar；atempo 后整句提前 0.76 s 的 bug 已修）、`viewing_packet.py`（实测台词时间；代理片观片包进 `viewing_proxy/`）、`animatic.py`（旧片退回分镜卡）
- .claude/skills/ai_videos__cut/SKILL.md（新）；ai_videos__出片审片/SKILL.md（R8 去掉「rule 38 音乐行」、verdict 首行 + take_sha256）
- .claude/agent_refs/project/ai_video.md：16.5–16.7 加「零人工剪辑，不是零剪辑」；12.4 配音块（声样＝人物卡 views.mp3）；42 改写 + 新增「42 剪辑」「42 标识」；42 字幕（实测时间、CPS）；36 出片审片（绑 sha、旧片）。ai_video_history.md 沿革一行。CLAUDE.md 阶段 7 行、stage6 playbook §9 下游加 `/ai_videos__cut`。*(judgment call — 规则直接进 ai_video.md 而不是先进 lessons.md：用户要的是整条管线的后期策略、批的也是管线级改动，finish_ep 是全仓共享工具，没有 edl 时行为不变)*
- .gitignore：`.venv-post/`、`ai_videos/**/shot*_tts_*.json`（TTS 摆位 sidecar，与旁边已忽略的 wav 同属可再生产物）
- ep01：删过期拼接（webapp `ep01.mp4` 一套、含旧 S07 take 的 `ep01_final` 一套）；S03 / S05 / S06 / S09 / S10 对齐缓存（v3）；S05 / S06 / S09 / S10 出片审片——四镜全「不通过」（锤变斧 / 多出狼 / 两人叠成一人 / 多出的光源 / 命中没打到 / 镜尾没收住），病根多在精简稿（超 2000 字锁串在后、设计稿负面词丢失、命中时刻不齐）→ 提案 U1–U5 交生成层；画外 9 句试听 `post/voice_test/`（WER 0，−23 ±0.7 LUFS）；`cut/edl.toml` v1 草稿（S03 / S05 / S06 整镜）；代理片 `post/proxy/ep01_v001_proxy.mp4`
- git：f48ada0 只提交后期 / 审片工具与三个 skill（它们还依赖别的会话未提交的 seedance_kit / prompt_compact / goal_ledger / script_tools 等，见提交说明）；别的会话暂存的 11 个 blocks.toml 没动
- 与 d8 协调：G10 一处定义在 `4_剧本/script.toml [scenery]`（new_zone_min_s 6 / new_bg_min_s 3 / idle_max_s 4 / post_trim_zone_s 4 / post_trim_bg_s 2，d8 实现，edl 经 `script_tools.scenery_cfg` 读）；`skill_cues` 改按段的源片出入点摆（d8 实现）；`prompt_compact.py` 归 d8（8f 报的 #6–#10、#17）

对别的剧的行为变化（旧剧重跑 finish_ep 时会遇到）：源片须 24p（`pc.check_fps`）；缺对齐缓存会自动跑 `.venv-post`；源片带 AIGC 标签就必须写回（没有标签的旧剧只警告，Q8 记 WARN）；类型带注解的「正常台词（…）」按画内处理（`pc.onscreen` 一处定义），未知类型警告后按画外；legacy 承接镜的 TTS / 音效 / 字幕比改版前早 0.1 s（与画面对齐）。

夜间判断（用户授权自决）：
- U1–U5（生成层提案）决定采纳，实现归 d8；d8 按它自己的授权只做了 U1 的「锁串前置」与 U3，把「重出镜照拦 2000 字」与 U2 / U5 留给用户（见 pending_user）。
- 字幕 CPS 英文上限 17 → 20：*(judgment call — 17 是 Netflix 儿童口径，成人内容通行 20；中文 9 不变)*；读不完的镜尾句允许越过切点 ≤ 0.5 s。当前 take 上读不完的从 6 条降到 3 条（S05 #7 因 Seedance 说反 #7/#8、S05 重出后应自愈；S06 #4 只在 S06 当最后一镜的代理片里撞片尾）。
- R2 推送没做：本机没有 R2 凭据（`R2_ACCESS_KEY_ID` 等都没有）；assets.json 自 09-18 起没同步，待推 5316 个文件 15.3 GB、待拉 545 个。shengji 的片子目前没有任何备份。
- Resolve Studio 没买（用户选「先不买」）。

No conflicts found in: 4_剧本/episodes/ep01/{script.md, goals.toml}（本条未改剧本）；5_6_分镜与prompt 各 shot md（本条未改）

## ep02 第二轮通读修订 + 就寝自主推进 — 2026-09-30 晚
Source: user_input/follow_ups/202609.md - section 048（第二轮通读三处用户裁定；就寝授权：AUTONOMOUS）
Summary: 对白通读 2 major / 冷眼观众 3 major 全部处理；S40 碎镜例外落成 script.toml [fragment_ok]；previz 开工（Cascadeur 与 d8 交接、今晚多子代理共用加排队锁）。

Auto-updated:
- 4_剧本/episodes/ep02/script.md — S37 台词按窗重排；S19 "Elvish — 'strike of flame.'"（技能名不出口）；S21 修士定住母鸡示范；S38 反打 + "Erlan — MOVE!"；S40 5s 攥灭近景、删白塔；S01 "So. The thing is—"；S12 加 "But"；S25 "You owe me one."；S32 窗 0–2.7；S34 "Walt — BEHIND me!" 窗 1.2–2.2（原 1.0 起时杜克背对镜头）；全集 750s；dialogue.md 重生
- tools/script_tools.py + 4_剧本/script.toml — 新增 `[fragment_ok]`（用户批准的 4–6s 碎镜名单；名单里的镜不再是碎镜即报错）
- characters/c22_Nell + gen_npc_cards — S07 样例句同步现稿
- skills/k206 — fizzle（S25）、变体「空手」（S21 修士示范）；k207 fizzle（S27）
- tools/szzl_ep02/shots_{b,c} — 各段按新闸门返修（钢盾 e5205 进 props、E1 施法排程加硬切、S21 三段、S25 光壳提前 1.6s 散、S27 机位换侧）
- scenes/…/bg807/_blender/bg807.blend — 首次建场（S14–S16 previz 用）

判断记录（AUTONOMOUS，醒来请过目）:
- 平面图审阅页已发给用户、尚未点头；按就寝授权先做 previz（只花算力，平面图若改再重渲）。
- S03 杜汉读信、S44 梅贝尔两句保留原典原句（通读建议改短 / 改白话，未采纳：原典引用优先）；梅贝尔卡「关键那句大白话」与此并存，待用户定。
- S31 previz 看出：猪拖人、项圈崩开、猪撞栅三拍都在切到沃尔特反应镜时发生在画外——项圈是 S45 的剧情物，已交 d 段改成在画内。
- Cascadeur 只有一个实例：今晚各子代理一律经 scratchpad/casc_locked.py 排队烘（mkdir 锁），不重启、不杀进程。

## ep02 第三轮通读 + 盖章 — 2026-09-30 深夜
Source: follow-up 048（就寝授权 AUTONOMOUS）
Summary: 对白通读第三轮 1 major（S21 "it" 会被听成母鸡）+ 5 minor、冷眼观众 0/0/17，全部处理后复读通过，两枚章盖在指纹 28b23c220774（171 句）。

Auto-updated:
- script.md — S21 "...wait for the light to come back."；S12 老奶奶删 old 以不跨 19s 硬切；S25 中文照原句；S38 反打 1.5s（4.7–6.2）；S44 杜克攥紧盾背旧握带（替掉蓝布条）；S11 "He saved up for it."（看着锤说）；S33 出手顺序（她先聚满 → 他罩壳 → 她才推）、S37 删「踢」、S40 往东北逃
- goals.toml / relationships.md / 人物卡 c19 c22 c28 c30 c33 + gen_npc_cards — 台词样例与声口同步（c33 加「只在埃尔兰面前破功」那一声）
- dialogue_review.toml — 对白通读 + 冷眼观众两枚章

判断记录（AUTONOMOUS）:
- S11：冷眼观众嫌 "He bought me the hammer." 像新买的，我先改成 "He gave me his hammer."，随后发现这改掉了 c1 卡前史（父亲攒两年钱买的旧锤），定为 "He saved up for it."——前史不动、也不会听成新锤。
- S44：蓝布条在 c2 卡里有来历（选拔那天该交回、他没交），但屏幕文字从未交代；改用观众见过的旧握带（S10 / S46 有呼应），蓝布条留在造型里给以后的集。
- 冷眼观众余下 14 条 minor 未改（S12/S23 接活没人应、S20 光壳没人演示、S38 强盗逃的时机等），清单在 spawns/viewer-reread-3/output.md。

## Follow-up 061 — 2026-09-30 20:10:00（夜间自主推进，用户睡前授权不问、自决）
Source: user_input/follow_ups/202609.md - section 061
Summary: 整集观感 r2 三处全改：S12 加「Dad's hammer first.」（28→30s）、S14 数钱买甲压到 20s、S15 狼 3s 就扑（18→15s），全集 628→617s；12 镜里 21 对共窗台词拆开 + 同窗多句闸门；冷开场闪前交 88（S20 出片后出 edl 补丁）；对白通读 / 冷眼观众 r9 盖章（1015daf9b92c）。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S12 / S14 / S15 按审稿改写（判断：S15 留 3s 横摇而非直接从狼扑开——G10 新机位下限 3s，且链甲一响是招来狼的因）；S11 / S16 / S17 / S19 / S23 / S24 / S25 拆窗；S23 麦克布莱德少一顿；S12 情绪句；文件头 617s；dialogue.md 重生
- 4_剧本/script.toml — [shared_window_ok] ep01 = S03 / S05 / S06 / S09 / S10（已出片，只减不增）
- 4_剧本/episodes/ep01/goals.toml — 锤的目标 pursued 加 S12
- tools/script_tools.py — 同窗多句闸门（同一镜两句台词的窗不许重叠）
- tools/gen_shots_szzl_ep01.py — S12 / S14 / S15 镜块；S14 7s 跳切
- 5_6_分镜与prompt/episodes/ep01/shots/shot12 / 14 / 15 — 平面图（S12 延到 30s、亚伦转向东北 3/4 脸说新台词；S14 重排：4s 布甲摊反打 / 7s 跳切护甲摊 / 13s 近景；S15 删掉前 3s）；S15 Cascadeur 编排与钩子 −3s 后重烘；previz 重出
- 5_6_分镜与prompt/episodes/ep01/shots/shot11 / 16 — 平面图 [meta] proxy：狗头人人偶本镜改粉（057 E3，橙 27° 落在圣光色相带里）；previz 重出
- 2_世界观人设/skills/ — skills.toml 圣光色相带按真片实测校准为 [20, 38, 0.18, 0.6]（55 量 shot07 / shot08 旧片）；k205 / k207 标 `state = true`（光壳余晖不参加排程 ② ③ ⑥，8f ep02 S33 / S37）
- tools/szzl_shot_engine.py — `doll_hue_errors`（057 E3）；`_proxy_of` 认平面图 [meta] proxy；E1 对 state 卡去掉 linger；previz 配置一镜只算一次（三道闸门共用）
- tools/shot_overhead.py — [meta] 允许 proxy
- tools/prompt_compact.py — 命中行只在动作同一秒写了同一件家伙时才省（88 U3：S21 画外那一声当被吞）
- specs/ai_video/shengji_zhilu/pending_user.md — §10：出片清单、冷开场、2000 字是否截断（U1）、负面词进精简稿（U2）、previz 分段避开命中（U3 后半）、技能样片
- specs/ai_video/shengji_zhilu/lessons.md — L22 / L23

判断记录（用户授权夜间自决）：
- 88 的 U1–U5 我只落了 U3 的命中行去重；U1 不压 ep01 到 2000、不改 12.4-P 段序（5000 字旧稿上传从未见截断，2000 是质量线）；U2 与 12.4-P 冲突、U5 属旧片，留给用户（pending_user §10）。
- 狗头人人偶改色只落在有冲突的 S11 / S16（平面图 [meta] proxy），不动 S06 / S09（已出片、无同镜圣光）。
- 写盘：本次改动的 shot 06、09、11、12、14、15、16、17、19、20、21、23、24、25（S06 / S09 只是命中行去重、另有能用的 take）；25 镜回读通过；资料包 25 镜全部与原始文件一致

No conflicts found in: 4_剧本/episodes/ep01/states.toml

## ep02 阶段 5 五路审查（S01–S28、S44–S49；时长节奏整集）— 2026-10-01 凌晨
Source: follow-up 048（就寝授权 AUTONOMOUS）；审查清单 .audit/…/spawns/qc5-{站位朝向,运镜,动作表演,光线色调,时长节奏}/output.md
Summary: 站位 1B/5M/10m · 运镜 6B/16M/15m · 表演 2B/15M/27m · 光线 1B/7M/10m · 时长 2B/11M/7m。先改剧本层（script-rev-qc5），再各段改镜头层与 previz；S29–S43 四路审查排在其后。

Auto-updated（本条目先记已落地的）:
- tools/szzl_ep02/common.py — AFTERNOON 改照场景卡锁定 #5「暖白、西南中高角度」（光线 M2）
- 新 plate 两张在出：bg4 铁匠铺后院 × 清早薄雾（S26–S28、S49）、bg8 芦苇浅滩 × 傍晚（S24–S25）（光线 B1 / M1）

流程改进（AUTONOMOUS：判断都该做，已交 d8 落引擎；理由见各清单末节）:
- 压缩器【参考素材】句按时辰改写（光线 B1）；语速常数一处定义、配音块超窗 raise（时长 ①）；G17 覆盖整镜不切与「定机位」（时长 ③）；G18 hero 钉高潮拍（时长 ④）
- 镜内切也查景别跳档与轴线；无【切】不拆「镜头N」；「画面」行按段起点取样（运镜 1–4）
- 说话人入画余量；画面句按台词窗取样；「对 X」朝向闸门；跨镜世界站位（站位 1–4）
- 慢嗓语速上限（时长 ②）由本会话在 script_tools 落地（待做）

## ep02 剧本层按五路审查修订 + 分段返修开工 — 2026-10-01 凌晨
Source: follow-up 048（就寝授权 AUTONOMOUS）；spawns/script-rev-qc5/output.md
Summary: 剧本 750 → 745s，47 镜动过、23 镜改镜长；台词正文只改 S49 里瑞亚一句（减词，酒馆名留 ep03）；按配音 2.5 词/秒排窗、慢嗓 ≤2.3。五段按「分镜交接表」+ 审查清单返修镜头层与 previz（b 段换新子代理 shots-b2）。

Auto-updated:
- 4_剧本/episodes/ep02/{script.md, goals.toml, states.toml, dialogue.md} — 见 script-rev-qc5 逐镜改动表；文件头待确认第 12 条
- tools/script_tools.py — 慢嗓闸门（casting 语速栏 慢/很慢/极慢 → ≤2.3 词/秒；行尾「语速快」放行；legacy_eps 不查）（时长节奏 proposal ②）
- tools/seedance_kit.py — 使用说明的超长判定按小数读镜长（原把 "3.9" 读成 39）
- characters/c20_Lyria_DuLac + gen_npc_cards — S49 样例句同步
- plates：bg4-1_后院_清早薄雾（S26–S28）、bg8-1_苇滩_傍晚望栈桥（S24–S25）过审；S49 不挂（光向与机位都反），走引擎兜底句

判断记录（AUTONOMOUS）:
- S46 为保住祖父原句与亚伦 "sir"（第 7 条裁定）排到 28.5s，超 27s 软上限、在 30s 硬上限内——保留；备选（祖父那句挪 S47 开头）记在剧本待确认第 12 条，待用户定。
- 审查人估算全改后约 720s，实际 745s：配音块按 2.5 词/秒排窗吃掉了秒数；余量只剩 5s，之后加戏要先减。

## Follow-up 060（续）— 2026-09-30 夜间（用户睡前授权自决）
Source: user_input/follow_ups/202609.md - section 060
Summary: 夜间补完 P0 审片、剪辑层演示、分轨去乐试验、主题曲草稿；字幕跨切点规则收紧；第二次提交。所有判断都标了 judgment call。

Auto-updated:
- S03 出片审片（take 742c7d40e919）：不通过，只挂 R8 镜尾（尾 0.25 s 只比前 2 s 低 3 dB，要 12 dB；切断的是 −42 dB 的环境声与脚步，不是台词）；R1–R7 全过。另记：威廉胸前的狮子是灰的不是金的、杜克的挎包没画、0–4.5 s 两人朝镜头走（剧本是背对）、6–7 s 切口前后爬台阶重复一次、威廉 20 s 往东退场（剧本 18 s 往西）。至此 5 个采用片（S03 / S05 / S06 / S09 / S10）全部「不通过」，edl verify V1 会拦住正式成片。
- 剪辑层演示（`/ai_videos__cut` 走到代理片为止，没批）：`cut/edl.toml` v2 草稿（base_version 0——v1 从没批过），S03 剪掉开头 2.5 s 空走、S06 剪掉开头 2 s 空营地与中段两段静止共 1.5 s，全片 77.1 s → 71.1 s；`post/proxy/ep01_v002_proxy.mp4`；新鲜观众双序盲评（`viewing_proxy/ep01_v002_proxy/compare_v001.md`）两个顺序都判 v002 更好（首句从 00:08.1 提到 00:05.6），并给出下一步三处剪法（S03 背景交代后压尾、伊根出场给脸或 J-cut、S06 包袱后留 0.8–1.2 s 反应）。*(judgment call — 只动已出片的三镜，不加 shot09 / shot10：补丁菜单没有「加镜」，且这三镜要重出的概率高，演示只为验证剪辑层)*
- 字幕：英文 CPS 上限 17 → 20（Netflix 成人口径），中文 9 不变；镜尾句读不完可跨切点，跨就在新镜停满 0.5 s（盲评发现 v002 的「Thank you, Eagan」跨进下一镜后一闪就收）。当前 take 上读不完的从 6 条降到 3 条：S05 #7 中英两条（Seedance 把 #7 / #8 说反了，#8 对不上只能按计划窗、挤住 #7；S05 本来就要重出）、S06 #4 中文（只在 S06 当最后一镜的代理片里撞片尾）。代理片已按新规则重出、观片包重建。
- qc Q8：进片 take 都没有 AIGC 标签（旧剧）时记 WARN 不记 FAIL；有标签的仍须写回、回读。
- 分轨去乐试验（`tools/post/stems_trial.py` + sep_models / stem_metrics / stem_tags；`.venv-post` 装了 audio-separator 0.47.0 与 transformers）：推荐本地路线（BS-RoFormer ep368 + Bandit v2 按 2 s 窗择优的 gated 配方）用于 S03 / S06；**S05 其实没有 Seedance 音乐**（前提有误，只有 S03 片头 0–7 s 与 S06 0–21 s 有）；S06 的镐砸盾声本来就埋在音乐里，任何路线都会一起去掉，0–21 s 要补环境 / 打击声。试听：`post/stems_test/{shot}/preview/{shot}_AB.mp4`（①原片 ②本地最佳 ③去掉了什么 ④只剩人声）。ElevenLabs Voice Isolator 没调用（省额度，且本地已够）。
- 主题曲草稿（`tools/gen_music_szzl.py`，ElevenLabs Music v2.5 composition plan，Pro 档，$0.41）：`2_世界观人设/music/drafts/t01_main_theme/`（85 s）、`t02_skill_motif/`（80 s），各带收据卡与原始响应。机测：两段大概率是 4/4 而不是 7/4、速度 99.5 / 110 BPM（要的是 84）；t02 的三音上行动机是 D–F♯–G（要的是 D–E–A）但确实出现了 ≥ 2 次；无词女声只在计划段落出现。都要你用耳朵确认。
- git：cf27f53（subs / qc 改动、分轨与配乐工具）；render_review.py 里 d8 新加的 R9 施法回读没有带进提交。
- ai_video.md「42 字幕」行按上面两条改了措辞。

更正（续前一条）：d8 最终**没有**做 U1 的「锁串前置」——理由是 12.4-P 之前最长 5000 字的上传即梦照收、没人见过截断，2000 是质量目标不是截断点；它已写进 pending_user 请你在即梦输入框实测。所以我提的「锁串排在 2000 字后被截掉」只是待证假设。U3 它落了一部分（精简稿不再误删不同武器的命中行），previz 分段避开命中时刻留给你定。

No conflicts found in: 4_剧本/*、shot md（本条都没改）

## align v5：找回句重对齐 + edl basis 含起止（align v4 对抗审查 F1–F6）— 2026-10-01 凌晨
Source: 后期工具修复轮（用户睡前授权自决，AUTONOMOUS）
Summary: 找回句（moved）的起止不再取 whisper 的词（常把 take 首词拖回 0 s），改在找到的那段音频上用同一模型重新强制对齐、照 ok 句收首尾；别句的词不许夹进找回段；几句一起找、对上多的先定；让位句只夹出找回句、ASR 漏听的边词不收；edl basis 连句子状态与起止帧一起指纹。

Auto-updated:
- tools/post/align.py — VERSION 5（_retime / MOVE_PAD 0.3 s、_fit 禁插别句的词、relocate 按 rank 全局定、_reclaim 按词序切开只收对上的边）；tools/post/edl.py — basis
- tests：test_align +5 例（shot10 开头、shot06 截断、夹在句中、句子包含、边词漏听），test_edl +1（重算后起止变了按旧 basis 停下）
- ep01 post/align：shot03 / 05 / 06 / 10 重算（台词起止与 speech 同 v4；S05 #8 的词改为强制对齐）；shot09 没有 shot09.mp4，用 `--take renders/shot09_061前旧版.mp4` 重算
- cut/edl.toml — e03 / e05 basis b09c4e601817 → 468ab71e4f87（cut:2 / cut:3 仍 16.50 / 21.25 s，剪辑不变）；post/cut/candidates.json 重出
- 代理片 ep01_v002_proxy 重出（sha 815e5b27f968；旧片用的是 v3 缓存）：S05「Dad's boots are fine.」字幕按实说顺序排到 #7 之前，e02 配平 +0.12 → +0.11 dB；观片包 viewing_proxy/ep01_v002_proxy 重建

判断记录:
- *(judgment call — F3 字幕半边不改：subs 一句 md 一条字幕，被夹住的句子要拆中英两份原文、需逐词映射；这种情况 too_dense 报读不完，finish_ep 出母带前会拦)*
- *(judgment call — viewing_proxy/ep01_v002_proxy/compare_v001.md 绑的是旧代理片 b357c6ff…，没重审：新片只差 S05 两条字幕的先后与 0.01 dB)*

## ep02 分段返修（a b c e 完）+ S29–S43 四路审查 — 2026-10-01
Source: follow-up 048（AUTONOMOUS）
Summary: a（S01–S11）、b（S12–S19，新子代理 shots-b2）、c（S20–S28）、e（S44–S49）按剧本修订与审查清单返修完、写盘、资料包一致，previz S14/S15/S16/S25 过；d 段 14/15 镜写盘后，S29–S43 四路审查：光线 0B/4M、运镜 1B/7M、表演 1B/13M、站位 0B/5M——交新子代理 shots-d2（含 bg178 窄口实为 0.14 m 的场景修正与 8 镜 previz 重做）。

Auto-updated:
- script.md — S31 节拍对齐 d 段时刻（2.9s 抓项圈、3.9s 崩扣、4.7s 起沃尔特）；S33 节拍对齐（4s 光散、5s 罩壳、5.5s 推、6s 炸、10.8s 壳散）；S44 梅贝尔行尾「对杜克」（站位 major：她要看着杜克、杜克避开）
- characters/m1_Kobold — 帽顶烛光改「自上而下」（光线审）
- scenes/…/bg4-1、bg8-1、bg807-1 plate 卡 — 加一句话锁定（挂 plate 的镜 `场景:` 行用它；d8 引擎已支持）
- tools/szzl_ep02/shots_d.py — S29 沃尔特扛草叉写出手；S36 草叉拿法改「双手握着…往下压」

引擎（d8 已落地，本轮 ep02 受益）: 浮点镜尾容差、叉 进 REACH（1.8 m）、G3 ① 不再把物件草叉当装备、plate 锁定句、精简稿时长小数不取整。
待 d8：跳帧测试取中位数（S38 漏检）、axis_ok 理由要写换了什么；站位 proposal 5–9（矮块遮挡、NPC 弹道、路径穿人、打戏两侧不翻、场景卡数字回读）。

## ep01 061 收尾 + 8f ep02 审查的流程改进落引擎（六批）— 2026-09-30 深夜至 10-01 凌晨
Source: follow-up 061（用户睡前授权自决）；8f ep02 阶段 5 五路审查的流程改进（`.audit/adhoc_agents/2026-09-28/shengji_zhilu-20260928-181315/spawns/qc5-*/output.md` 末节，上一条目「已交 d8 落引擎」）
Summary: 8f ep02 审查提的流程改进全部落进引擎（六批）；ep01 按新闸门修画外窗、拆 S09 窗（S09 要重出）、机位与走位共十镜；S21 收尾那一下切近景；animatic 改成 previz 翻页后整集观感 r4 / r5 重审，r5 有效（出片闸门开）；对白通读 / 冷眼观众 r11–r14 盖章（现章 220415f5058d）。

Auto-updated:
- tools/prompt_compact.py — 场景图只锁材质与形制、光与时辰只按【场景与光】（光线 B1）；没【切】不另起「镜头N」、整镜不切不写「镜内硬切」（运镜 3）；【画面】的「时长」不再取整（8f：ep02 S46 28.5 s 被写成 29 秒）
- tools/animatic.py — previz 段每 1.5 s 翻一帧，不再一段一张定格（S02 22 s、S21 18–27 s 高潮段各只有一张图：r3 据此判「仗怎么赢的不在画面上」，其实剧本 22–27 s 有审判 + 盾沿磕下巴 + 倒出画；r4 开头又报 S02 定格 22 s，停掉重拼再审）
- tools/szzl_shot_engine.py —
  - 批 1：画面句按段首 / 段中 / 段尾取样（运镜 4）；G17 认「定机位 / 定点 / 镜头不动」，整镜不切也查（时长 ③）
  - 批 2：`intra_cut_errors`，镜内【切】查跨轴与跳切（运镜 1 / 2）；`speaker_edge_errors`，说话人 |x| ≤ 0.8、近景 ≤ 0.7（站位 1）；`offscreen_window_errors`，画外 / 独白窗按配音语速放够（时长 ①）
  - 批 3：G18 hero 钉在台词窗、动作拍或放光 ±0.5 s（时长 ④）；`face_to_errors`，「对 X」面朝 X（站位 3）；画面句写段内转脸（站位 2）
  - 批 4：`actor_seam_errors`，跨镜世界站位（站位 4）：同场景同 plate 接着演，人不瞬移；说话人按自己的台词窗取样（站位 2 后半）
  - 批 5（8f 运镜复审）：跳切按切点两边都在画里的人的放大倍数中位数判（ep02 S38 只一人 1.68、其余 1.06–1.28，旧的 max 放行了）；axis_ok 理由须写明换了什么（换地点 / 跳过 / 换侧 / 反打 / 推拉 / 人物换位），「重新交代」不算；连续 8 个接缝里超过 5 个靠 axis_ok 报警告
  - 批 6（8f 站位 proposal 5–9）：矮块 2.5D 遮挡（视线在块处低于块高就算挡）与 1–2.5 m 非可走块里不许站人（进块 ≥ 0.1 m 才算）；技能卡 flight 阶段的弹道离施法者自己人 ≥ 0.5 m（[[cast]] over 放行）；路径不许穿人（中心距 < 0.35 m，跳切瞬移除外）；跨镜世界位移阈值 3 → 2 m；同一场打戏里朝向 ≤ 45° 的任意两镜主角 / 敌人、护人 / 被护左右不翻；场景平面图 [[gap]] 回读最小间距
  - 配音语速：慢嗓角色（script_tools.slow_voices）按 SLOW_WPS_MAX，用在配音块、画外窗闸门、画外人声占位（8f 对白通读第四轮；legacy 集不变）
  - 遗留清单（只减不增）：`CUT_GATES_LEGACY` ep01 = S03 / S05 / S06 / S09 / S10；`INTRA_AXIS_LEGACY` ep01 = 10 镜；`FACE_TO_LEGACY` 空
  - `_PROVENANCE`：上传的精简稿里出现审稿 / 流程来历注记（整集观感、follow-up、旧片、rN：…）即 raise，全集适用（S09 状态里的来历注记进了上传稿；ep01 / ep02 扫过，只此一处）
  - `scene_lock`：plate 卡自己有一句话锁定就用它，没有才退回主体卡（8f：ep02 S26–S28 挂后院 plate，【场景与光】却写成主街；ep01 plate 卡都没有锁定行，不变）
  - `--check` 464 s → 25 s（场景树 lru_cache、装备卡按 mtime 缓存）
  - 8f：镜尾静场检查加 1e-6 容差（ep02 S32 3.9 s 镜、末句止于 3.1 s 被浮点误判）；命中行「叉」写「顶在」；_WEAPON / _HELD 认「草叉」（不收单字叉，免得叉腰 / 交叉误中）；G3 ① 逐字引 [carry] 另用 `_EQUIP_WEAPON`（不含草叉：物件没有 [carry] 可引，8f 报 ep02 误报 13 镜）
- .claude/agent_refs/project/ai_video.md — rule 44 的取图说明跟着改（previz 每 1.5 s 一帧）；ai_video_history.md 沿革一行
- .claude/skills/ai_videos__整集观感/SKILL.md — §3 加一句：animatic 的 previz 不渲光，卡上印了闪光就按在画面上算（r4 把 S02 已有的「锤头一闪」判成没有）
- tools/skills_lib.py — 卡加 flight（阶段列表），check 核对阶段名；k401 火球 flight = [effect, blocked]；compose 断的收拢窗末端容浮点误差（55：1.4 + 2.8）
- tools/previz/planschema.py — HIT_OBJ 加「叉」→「叉头」，与 build_previz 持物件名对上
- tools/shot_overhead.py — REACH / KNOCK_MAX_M 加「叉」（1.8 m / 0.8 m，8f：ep02 S35 / S38 沃尔特的草叉被迫写成「棒」）；GEAR_PART 认「草叉 / 叉股」；schema：camera 加 axis_ok / jump_ok，meta 加 skip，actor 加 moved，cast 加 over；path_cross_errors / low_block_errors / 2.5D 遮挡（只由 szzl 引擎调用）；场景树缓存
- tools/equipment_lib.py — 装备卡按 mtime 缓存
- tools/beat_logic.py — INJURY 认「挨了一叉」
- tools/shot_logic.py — NOT_BUILD 加「膝盖」（K33 L1 把「膝盖」的盖当成建造动作，S21 因此被要求逐段状态账本）
- 4_剧本/episodes/ep01/script.md — S04 麦克布莱德第一句画外 0–3.2 s（切前留 0.4 s 气口）；S13 萨缪尔画外 8–10.4 s；S09 两句拆窗
- 4_剧本/script.toml — [shared_window_ok] ep01 删 S09（要重出）
- tools/gen_shots_szzl_ep01.py — S09 矿工状态加「短镐只在矿工手里」（来历写在行尾注释，整集观感 r3：旧片把亚伦的锤画成了镐）；S11 / S21 删非指纹冗字，设计稿回到 5000 字内
- 5_6_分镜与prompt/episodes/ep01/shots/shot13 / 16 / 18 / 20 / 24 / 25 — 平面图机位瞄点 / 焦距微调（站位 1 说话人贴边、运镜 1 镜内跳切；S18 那一刀写 jump_ok）；S13 / S16 / S20 / S25 previz 重渲
- 5_6_分镜与prompt/episodes/ep01/shots/shot09/renders/shot09_061前旧版.mp4 — 旧 take 挪走
- 新闸门扫出的 ep01 修正：S20 15s 那一刀机位挪到方位差 47.5°、撤掉今晚按 max 凑的焦距（中位数判跳切）；S09 亚伦爬坡不再穿过停在半坡的杜克、碎石坡写 walkable；S17 过桥两人起点对调（原来走着走着左右穿过）；S22 亚伦绕到斧子西侧捡斧（原来走进杜克身上）；S06 / S15 的 axis_ok 理由补「换地点」；S09 / S20 previz 重渲
- S21 收尾那一下有了自己的一拍（整集观感 r3 / r4 都点了）：剧本【22–27s】与生成器分镜 / 镜头 / 动作加 23–24.2s 侧面近景（盾沿磕下巴、头往后一仰）→ 24.2s 切回全景倒出画外、静半拍；情节压成一句（原 382 字与动作重复，首句进【概述】的是开场那个动作）；平面图加两台机位（24.2s 那刀写 axis_ok：同方位推近再拉回）；previz 重渲；对白通读 / 冷眼观众 r12 复读 OK（对白通读改一处：情节里「第四斧」其实是第五斧，改「下一斧」）；S04 情节 / 走位里庄稼汉扛草叉补「右手握着」（新认草叉后持物支撑闸门拦下，剧本本来就写了右手）
- specs/ai_video/shengji_zhilu/lessons.md — L26–L29；061 条目写的「L22 / L23」与 057 回读那两条撞号，改为 L24 / L25；表中间一个空行把表断成两截，删了
- specs/ai_video/shengji_zhilu/pending_user.md — §10 a 出片清单改 21 镜（加 S09）；c 精简稿字数更新；i 换成 r5 版（已做 / 不是问题 / 等你定）；k 台词窗太宽（S18 等 14 句）；新增 j：S05 旧片杜克手里多了一把锤、亚伦的双手锤成了短锤（抽帧核过，旧片没挪）
- 写盘（五次）：25 镜全部改动。全集共用的是【参考素材】那句和画面句取样；个别镜另有改动：S04 / S09 / S13 台词窗，S09 状态，S13 / S16 / S18 / S20 / S24 / S25 机位。第三次只动 S21，第四次只动 S04（情节 / 走位措辞），第五次动 S09 / S17 / S20 / S22（走位与机位）。回读通过，资料包 25 镜全部与原始文件一致。保留 take 的 S03 / S05 / S06 / S10 只改措辞，镜长没动，不用重出
- animatic 重拼 617.2 s（S09 旧 take 挪走，改用 previz；previz 段翻页），观片包重出。整集观感 r4 有效：会看下去；最低 S23＝4，S01 / S12 / S15 / S19 / S24＝5。最该改的三处里，S21 收尾已做，开场与 S23–S24 交用户（pending_user §10 i）。r4 另看到 S05 旧片杜克拿锤（§10 j）。S21 改后再拼，整集观感 r5 有效（出片闸门开）：会看下去，高潮已不在最该改的三处；最低 S01 / S22＝4；三处建议（开场、S12–S15、S22–S25 收尾）交用户（pending_user §10 i）；小注里 S18 字幕早于冲锋记 §10 k

判断记录（用户授权夜间自决）:
- 站位 4 只拦「同场景且上一镜末 plate ＝ 下一镜首 plate」的接缝。ep01 的五处同场景大跳都换了子 plate，是真换地方，0 处命中。ep02 全用整场景 plate，22 处命中，清单已交 8f：大跳写 skip，3–6 m 的是真穿帮。
- 镜内跨轴的 10 镜不改机位，进 `INTRA_AXIS_LEGACY`（pending_user §10 g）。
- r4 三处里只做了 S21：它只动一镜的机位，r3 / r4 都点了。开场再压会动 059 定的世界卡，S23–S24 合并是结构大改，都交用户。
- S05 旧片（杜克拿锤）只报不挪：重出要花用户额度；S09 是剧情物件画错，才挪了旧片。
- 已知未修：`shot_logic._SEG_HEAD` 只认整数秒的段头（「10–16.2s」不计数）。K33 L1 的段数对照因此对小数段失灵；修了会回溯别的剧的建造镜，先记下。

No conflicts found in: 4_剧本/episodes/ep01/{goals.toml, states.toml}

## 技能样片 prompt 从卡拼 — 2026-10-01
Source: 用户问「skill.md 里样片 prompt 是空的，怎么生成样片」（只有 k201 / k101 手写过 prompt）
Summary: 样片 prompt 改由卡拼：[sample] scene（地点与机位，一句手写）+ 按 [timing] 默认时长把 [look] 各阶段排成时间轴 + 固定收尾；补 ep01 用到的 k202 审判 / k203 正义圣印 / k204 力量祝福。

Auto-updated:
- tools/skills_lib.py — `sample_prompt_of(card)`：手写 prompt 优先，否则由 scene + [look] 时间轴拼，同时给出峰值秒（最后一个出手 / 生效阶段的中点）；Card 加 sample_scene / sample_target；skill.md、`sample`、`adopt` 都走它（adopt 不给 --peak 时用这个峰值秒）
- 2_世界观人设/skills/k202_审判、k203_正义圣印、k204_力量祝福 — skill.toml [sample] 加 scene / target；样片/prompt.txt 与使用说明.txt 重出；11 张 skill.md 重生
- 判断：光的样子只在卡的 [look] 写一处，样片 prompt 跟着卡走，不再手抄一遍；k201 / k101 已有的手写 prompt 不动。ep02 才用的 k102 / k205–k208 / k401 还没写 scene

## Follow-up 062 — 2026-10-01 08:41:34
Source: user_input/follow_ups/202610.md - section 062
Summary: 技能样片按正片规格做（参考图 + Cascadeur 动作 previz + 完整 prompt，用户手抄手传）；先做圣光术 k201 试点，中性背影人，有 / 无特效代理两版对比（MC-B）。

Auto-updated:
- 2_世界观人设/skills/k201_圣光术/样片/k201_sample/ — 样片的迷你镜头：planning/overhead.toml（借 bg175 武器大厅第二间小室，两人背对镜头、西南角 3/4 背后机位推近）、cascadeur/choreo.toml（施法者 stand → palms_up → arm_up_l → stand；目标 sit_ground，光柱落下时抬头，时刻按卡 [timing] 默认值）→ choreo.py 烘出两具 FBX；previz/ 两份配置 + 特效代理钩子（掌心光 / 举手光团 / 光柱 / 光尘，材质与 ep01 镜头钩子同一个 PREVIZ_光）；prompts.toml＝五段 prompt 的原稿（资料包目录不进 git）
- 2_世界观人设/skills/k201_圣光术/样片/资料包/ — 使用说明、3 段关键帧生图 prompt + 构图参考（previz 第 3 / 4.6 / 5.3 秒）、两版 previz（8 s）、两版视频 prompt（约 1000 字）、游戏录屏对照表（标明不上传）
- 判断：游戏录屏截帧按调研规矩只进 prompt 不入画，所以参考图走「先用即梦生关键帧、再挂进视频」两步；光的写法逐字用卡的 [look]，再补录屏里看得到的细节（手上是光晕不是火、举手掌心一颗小太阳带四角星芒、光柱从上落下柱心白边缘金、脚边星形光尘）；光柱代理是不透明圆柱，正好测它会不会被画成实物
- 上一条「技能样片 prompt 从卡拼」的拼接器留着给没写手稿的卡兜底；k201 试点的视频 prompt 以本资料包为准

No conflicts found in: 4_剧本/、5_6_分镜与prompt/（正片未动）

## Follow-up 063 / 064 — 2026-10-01 09:24:25
Source: user_input/follow_ups/202610.md - sections 063, 064
Summary: 技能样片定无代理版；ep01 用到的五个技能（圣光术 / 审判 / 力量祝福 / 正义圣印 / 冲锋）各出一套样片资料包＝Cascadeur 动作白模 mp4 + 写进技能卡的完整视频 prompt（设计稿规格，1574–2004 字）。

Auto-updated:
- 2_世界观人设/skills/k101 / k201 / k202 / k203 / k204 — skill.toml [sample] prompt 换成完整设计稿（参考 / 参考用法 / 角色 / 人数 / 情节 / 场景 / 镜头 / 镜内状态 / 走位 / 动作 / 技能 / 光线 / 节奏 / 声音 / 渲染样式 / 比例 / 时长 / 负面词），卡的 [look] 锁定串逐字嵌在 `动作:` 里；k202–k204 去掉拼接用的 scene / target；11 张 skill.md 重生
- 2_世界观人设/skills/*/样片/k*_sample/ — 每个技能一个迷你镜头：planning/overhead.toml、cascadeur/choreo.toml（choreo.py 烘 FBX；本样片独有的姿势部件写在自己的 [parts]：reach_touch_l / hammer_up_r / stun_stiff）、previz/ 配置 + 道具钩子（锤 / 短剑 / 圆木盾，不挂光的代理）；场景借 bg175 第二间小室（圣光术、正义圣印）与 bg19 门前空场（审判、力量祝福、冲锋）
- 2_世界观人设/skills/*/样片/资料包/ — 0_使用说明（上传白模 + 粘贴 prompt，出 3–4 条，挑一条告诉我）、2_previz.mp4、3_视频prompt.txt（＝卡里那份）、有游戏录屏的附对照图（标明不上传）
- 圣光术试点：撤掉有代理版与关键帧生图步骤（064：只要白模 + 完整 prompt）；删掉各卡 样片/ 下旧流程留下的 prompt.txt / 使用说明.txt、k201_sample/prompts.toml（prompt 只在卡里一处）
- specs/ai_video/shengji_zhilu/pending_user.md — §9 MC-B：技能样片定不放代理；正片 previz 要不要撤代理待定
- specs/ai_video/shengji_zhilu/lessons.md — L13 补一句：技能样片不放代理

判断记录:
- 样片里的人都是中性人、不露正脸（062 用户定），所以不挂角色主体；被施法的一方按技能来：坐地的伤者（圣光术）、戴兜帽的敌人（审判、冲锋）、握剑的同伴（力量祝福）。
- prompt 里不写点名视觉的否定句（「地面没有光」「光没有飞过去」「不是火焰」都改成正面写法）：模型会把被点名的东西画出来（12.4-P）；负面词只留文字 / 水印 / 音乐与通用画质项。
- 正义圣印按技能卡写（锤头闪一道薄金光）；游戏录屏里是脚下金色符文环沿身体升过头顶，两者不一样——已在资料包使用说明里写明，等用户定要不要改卡。
- 冲锋者刹在对方跟前 1.3 m（原 0.95 m 两人身体叠在一起，读成撞上去；卡禁写撞翻 / 撞倒）。

No conflicts found in: 4_剧本/、5_6_分镜与prompt/（正片未动）


## Follow-up 065 — 2026-10-01 11:25:00
Source: user_input/follow_ups/202610.md - section 065
Summary: 技能按游戏定死——施法时长锁成原典、每镜一样；圣光术两手一高一低、光柱分三层、之后全身泛白；正义圣印改成游戏的符文环 + 金印；ep01 十镜按新时长重排；技能样片剪出「施法片段」挂进各镜参考。

Auto-updated:
- 2_世界观人设/skills/k201_圣光术/skill.toml — [timing] 锁死 2.5 / 0.3 / 0.25 / 1.15 s（w25 .002–.004）；[pose] gather 两步（托光低 → 0.5 s 起托光L高）；[look] / [short] / 持锤变体：两手一高一低、三层光柱（白芯、明黄、金雾、竖直光纹、高出半身、一个半肩宽）、全身泛白 + 头部余辉 + 四角星形光尘；liberty 写明不用挨打回退；样片 prompt 重写（7 s）
- k203_正义圣印 — 改游戏样子：release 0.7 s 脚下金色符文环升过头顶、effect 0.5 s 头顶金印；forbid 加「锤头一闪 / 锤头上闪」；[script] flow 改符文环；样片重做（全身机位、往空里一挥、抬头看金印，4 s）
- k202_审判 1.0 / 0.4 s（w25 .016）；k204_力量祝福 0.8 / 1.9 s、k101_冲锋 1.2 / 1.0 s 锁在原默认值；五张卡 [sample] 加 window / peak / clip
- skills.toml — [timing] unlocked（ep02 才用的六张卡，只减不增）；圣光 colors 加「近乎纯白 / 明黄」
- tools/skills_lib.py — 时长锁死闸门（锁死阶段写 dur 即 raise；check 查没锁的卡）；Cast.legacy；[pose] 分步；施法片段（adopt 按 window 剪 `{key}_施法片段.mp4`，refs 优先挂片段）；window / peak 闸门
- tools/szzl_shot_engine.py — CAST_TIME_LEGACY（ep02 S21 / S33 覆盖了锁死时长，只减不增）；施法样子本身在脚下出一圈时不挂 NEG_RING；previz_config 写 `[[施法]]` 阶段窗；`cast_plan_errors`（平面图 [[cast]] t0 对不上镜表 casts 即 raise）；SKILL_USAGE 进参考用法
- tools/previz/build_previz.py — `[[施法]]` 键白名单、`cast_windows` / `cast_curve` 给钩子；POSES 加「托光低」「托光L高」
- tools/cascadeur/poses.toml — light_waist / light_low_l / light_high_l（正面调试机位核过）
- 4_剧本/episodes/ep01/script.md、goals.toml、tools/gen_shots_szzl_ep01.py —
  - S02 请光改符文环 + 金印，亚伦愣着没听见杜克吹盾、15.5s 才回过神道谢；S05 / S06 去掉请光条件句（保留旧片里本来就没出这道光）
  - S07 萨缪尔 12s 起光（放光仍 14.5s）；15.5s 特写的余辉由跨切重述接上
  - S08 第一道光 15s 起、杜克 16.4s 进门 17.4s 撞散（2.5 s 之内）；萨缪尔那句拆成画外「...There.」与撞散后「Stumble, and it's gone.」「...Again. Give it somewhere to go.」（对白通读 r15 M1）；两手特写收到 85 mm、萨缪尔出画
  - S11 去掉时长覆盖；S12 起光 8.5s；S13 请光改符文环、祝福效果 1.9 s
  - S15 / S16 审判 1.0 + 0.4 s，S16 第二下挪到 7.0s，狼 / 矿工吃了那一下再逃
  - S18 冲锋 1.2 s（原 2.0 s，7.3 m 跑 6 m/s）
  - S21 杜克多扛两斧（12.6 / 13.8s），亚伦喘匀站稳 14.9s 起光，15.1s 加瑞克见光才扑，东挡 15.7s、西挡 16.8s，一斧一词压到最后两斧；审判 21.8s
  - 对白通读 r15 M2 / M3：萨缪尔慢嗓窗放宽（S08 两句、S13 三句，"Light goes where you point."）
- 平面图 / Cascadeur / 钩子：S08 / S11 / S12 / S15 / S16 / S18 / S21 平面图；S11 / S15 / S16 / S21 choreo 重排并重建 FBX；S11 / S15 / S16 / S21 钩子改读 `[[施法]]`；previz 重渲 S02 / S07 / S08 / S11 / S13 / S15 / S16 / S21
- 2_世界观人设/style_guide.md、world.md、relationships.md、c1 / c14 卡 — 请光与圣光术的写法、引句跟上
- 技能样片资料包：k201（7 s）、k202（5 s）、k203（4 s）重出；k204、k101 不变
- specs/ai_video/shengji_zhilu/lessons.md — L30–L32

判断记录：
- S08 用户选「2.5 秒内被撞散、光起得晚一点」：光 15s 起（晚 0.5 s），杜克提前到 17.4s——光再晚，撞散后的两句与第二次施法、结尾那句在 30 s 里放不下（单镜上限 30 s）。
- S21 审判提前到 21.8s，胸口爆光仍在 22.8s、23s 切近景之前。
- ep02 不动：两镜进 CAST_TIME_LEGACY，k202 默认时长变化已回归（ep02 产物闸门全过；S20 精简稿曾超 1 字，靠压短圣光术短串解决）。
- 冷眼观众 r15 minor：S21 从起光到光柱 2.5 秒里放了加瑞克绕两边、两次格挡，偏挤（用户定的统一时长，未改，交用户）；之后各镜的审判前要不要补请光（游戏里审判要先有圣印），交用户。

No conflicts found in: 4_剧本/episodes/ep01/states.toml
- 补（同一 follow-up，用户追问「参考行是不是该有 skill MP4」）：卡写了样片 prompt 与 window 的技能，参考行按固定文件名挂施法片段（放得下）或峰值图（放不下），两者不同挂；文件没收进来前资料包建不起来——先出样片再出镜（ep01 10 镜暂不可用）。圣光术片段 window 改 3.2–5.4 s（S21 才放得下）。
- S08 13–16.4s 两手特写在 previz 里只拍到后背，改成两人中近景，"...There." 改画内说；对白通读 / 冷眼观众 r15 复读通过，盖章 64b0a7e1aa13。
- ep01 写盘回读通过；animatic 重拼、整集观感 r6 有效（高潮段被点名为真高潮；最低 S22＝3、S01 / S12＝4；三处建议是开头、S12–S15、S22–S23 收尾的节奏，交用户；另报 S05 / S10 旧片里看不见父亲的锤）。

## Follow-up 066 — 2026-10-01 12:18:55
Source: user_input/follow_ups/202610.md - section 066
Summary: 先只做 ep01，ep02 暂停（重排与遗留清单都先不动）。

Auto-updated:
- （无产物改动）

No conflicts found in: pending_user.md §12 c（已注明 ep02 搁置）

## Follow-up 067 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 067
Summary: 圣光特效写成真实分层的光；施法者全身协调——choreo.py 加「活人层」与闸门，先在圣光术样片上验证（用户选）。

Auto-updated:
- tools/cascadeur/choreo.py — 活人层（choreo [meta] life = true 时）：全身呼吸、大动作中间键躯干先走肘膝后跟、定住 > 0.6 s 的段落插微动键；闸门：上半身整体不动 > 0.6 s 或关节 > 900°/s 即 raise
- k201 样片 choreo — 全身演：膝微屈站稳、左手由肩带起胸口转向、放光前一沉、放光仰头开胸、手从身前放下吐气；资料包 2_previz.mp4 重渲
- k201 [sample] prompt — 动作写全身协调；光写成真实的光（光核与光晕、羽化边、浮尘、反光与衰减、逆光勾边、白光退潮）；负面词加平面贴图光效 / 光效硬边 / 卡通描边 / 机器人般僵硬；资料包使用说明加两条挑片标准
- 流程改进提案（用户同意，2026-10-01）：动作僵的根因是 choreo 只写关键姿势、中间定死或匀速，且没有闸门。

待用户看过圣光术样片白模后：活人层铺到 S11 / S21 等 Cascadeur 镜与其余技能样片（life = true 后跑闸门、重建、重渲）。

## Follow-up 068 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 068
Summary: 技能样片改策略——每个技能 2–3 张手势参考图（即梦 CLI 自动出）+ 完整视频 prompt，去掉 Blender / Cascadeur；只限技能样片，正片照旧挂白模。

Auto-updated:
- tools/skills_lib.py — [[sample.keyframe]]（name / at / prompt / ref）、keyframe_path、闸门（≤ 1500 字、ref 只能指前面的图、不重名）、skill.md 印出图片 prompt
- tools/skill_keyframes.py（新）— 按卡出图到 样片/资料包/1_{name}.png：第一张文生图，其余以 ref 图生图保人和场景一致；已有跳过
- k201 / k202 / k203 / k204 / k101 skill.toml — 手势参考图 prompt（圣光术 3 张：起手 / 聚光 / 放光；其余各 2 张）；视频 prompt 的参考行与参考用法改挂手势图
- 资料包：删 2_previz.mp4，出 1_*.png 共 11 张（圣光术聚光 / 放光、审判炸开、力量祝福按手 / 光带、冲锋冲 / 定住按看图结果改 prompt 重出），使用说明改为上传手势图
- 删除 样片/k*_sample/（Cascadeur 动作表、FBX、previz 配置与渲染）
- tools/cascadeur/choreo.py 的活人层（067）留着、默认关；正片 S11 / S21 不铺（样片已不用白模，铺不铺正片等用户看正片效果再定）

## Follow-up 069 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 069
Summary: 手势参考图只做动作指导（绿幕棚拍、不带光效与颜色）；技能样片视频的场景改成电影绿幕棚，不管场景细节。

Auto-updated:
- 五张技能卡 [[sample.keyframe]] — prompt 改为绿幕棚拍、低饱和、只写身体动作；11 张图重出（圣光术放光、正义圣印符文环看图后改动作描写再出）
- 五张技能卡 [sample] prompt — 场景＝绿幕棚；情节 / 光线 / 声音 / 动作里的石墙、窗光、林地、黄土、日光换成棚拍光与绿幕；渲染样式「外景午后日光」改「绿幕棚拍光」
- tools/szzl_shot_engine.py SKILL_USAGE —「技能参考只取手势、光与时长」（参考来自绿幕样片，不取背景；S11 / S21 设计稿 5000 字内）
- 资料包：3_视频prompt.txt、使用说明同步；ep01 闸门全过

## Follow-up 070 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 070
Summary: 技能样片做法定型（绿幕 + 手势参考图 + 文字写光）；修好导入，圣光术样片收进技能卡。

Auto-updated:
- tools/skills_lib.py — adopt 修好：认 Git-Bash 路径（/c/…）、即梦下载名带反引号传不全时按前缀找；不给路径就在 ~/Downloads 找名字里带本卡第一张手势图名的最新即梦视频
- k201_圣光术 — 收进 k201_样片.mp4（7.07 s）、k201_峰值.png、k201_施法片段.mp4；按实测光柱 4.0–4.6 s，peak 3.9 → 4.25、window [3.2, 5.4] → [3.3, 5.6]
- 各技能样片资料包里的图被改名成「资料包N.png」（库外改的），按出图时间与文件大小还原成 1_*.png 与 9_对照_游戏画面_不要上传.png（逐张看图核过）
- .claude/agent_refs/project/ai_video.md rule 45 — 「45 资产」改写、新增「45 样片做法」；ai_video_history.md 沿革一行
- ep01 重写：S07 / S08 / S11 / S12 资料包齐了；S02 / S13 / S15 / S16 / S18 / S21 等其余四个技能的样片

## Follow-up 071 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 071
Summary: 圣光术去掉光柱之后的金色星点（连同放光时掌中的四角星芒）。

Auto-updated:
- k201 skill.toml — [look] / [short] linger 改「全身泛白、头部金色余辉，随即慢慢褪去」；forbid 加 光尘 / 星尘 / 星点 / 星芒 / 星形（用到圣光术的镜产物里出现即 raise）；liberty 记偏离原典；样片 prompt 删星点、星芒与叮铃声
- k201 样片：已收的那条在 4.8 s 起有星点——施法片段改剪 2.6–4.75 s（头侧聚光 → 放光 → 光柱），峰值图 4.25 s 不变（两者都看过、没有星星）
- 4_剧本/episodes/ep01/script.md S07 / S08 / S11 / S12 / S21、style_guide.md — 删「几点金色光尘」
- 补（071）：forbid 里的「星形」会误中亚伦护腕「两枚星形小铜钉」，micro-drama-platform-a1 会话收窄为「四角星形」（同意）。ep01 剧本同时有 a1 会话在改台词（台词大师 + 冷眼观众，用户交办）；本会话不盖章、不写盘，等 a1 写完再拼 animatic、跑整集观感。

## Follow-up 072 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 072
Summary: ep01 冷眼观众 + 台词大师通读，改 8 镜 12 句台词。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S03「You're the seventh today.」、S04「Clear out ten.」、S05「Ooh. That barely tickled it.」、S07「Brother, the mine's next…」「What was that?」、S08 父亲的腿说清（A crate crushed his leg…）、S10「Grandad's got my back.」、S12 Duke「Somebody's got to buy you time.」+ Willem「Your pay.」、S17「Not so easy.」
- 4_剧本/episodes/ep01/goals.toml — kobolds.resolved 引文改「Your pay.」
- dialogue.md、shot03/04/05/07/08/10/12/17 重生成；对白通读 + 冷眼观众重盖章 5f565e9ea154
- 试改 S13「Swing it with the light.」、S23「For the time being.」被闸门拦下（画外窗 / 镜尾留白），已退回原句

No conflicts found in: states.toml

## Follow-up 073 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 073
Summary: 圣光光柱一收就没了，去掉余辉 / 泛白 / 残光（071 只去了星点）。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S07 / S08 / S11 / S12 / S21 光柱退去后改「什么也没留下 / 什么也没剩」；S11 两处措辞、S12 红肿「肉眼可见地消下去一圈」（复读建议）
- k201 skill.toml — [look] / [short] linger 改「光柱一收就没了…什么光都不剩」；样片「余辉到 5.2s 散尽」改「一收就没了」；forbid 加 余辉 / 残光
- style_guide.md §4 — 圣光术行改「光柱一收就没了、不留任何残光」
- shot07 / 08 / 11 / 12 / 21 重生成；对白通读 + 冷眼观众重盖章 576f88b87583

No conflicts found in: goals.toml, states.toml
- 补（071 / 073，技能侧）：k201 样片 prompt 去掉泛白 / 余辉 / 白光退潮（情节、动作、光线、节奏），放光后写「光柱一收就没了，什么光都不剩」，与 a1 改过的 linger 锁定串逐字一致；已收的样片光柱后有泛白与星点，施法片段改剪 2.5–4.55 s（2.03 s，末帧光柱还在、没有星点与余光），峰值图 4.25 s 不变。用户：本会话只管技能，不管 shot。

## Follow-up 075 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 075
Summary: S02 亚伦不带任何技能：删符文环与金印，只是普通一锤。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S02 8–9s 去光、11–18s 改看锤看狼；S13「...Like at the stream.」改「...Was that me?」，备注与「愣」措辞同步
- 4_剧本/episodes/ep01/goals.toml — 删 [[skill]] 请光（used S02）
- tools/gen_shots_szzl_ep01.py — S02 删 Cast(k203)、动作同步
- shot02 previz_config 去掉 [[施法]]，previz 重渲；shot02 资料包不再依赖 k203
- 另：script.md 里 6 处「金雾 / 光雾」改「金晕 / 光晕」，跟 k201 锁定串（074 技能侧）一致
- 顺手纠正：此前 S13 的「For the time being.」被我误改成 For now，已还原（S23 的「For now.」本来就是它）

No conflicts found in: states.toml

## Follow-up 074 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 074
Summary: 圣光之后冒烟雾 / 烟尘——根因是 prompt 写了「金色光雾」「浮尘被照亮往上飘」「体积光」；改措辞、禁写词也查样片 prompt；已收样片作废。

Auto-updated:
- k201 skill.toml — [look] effect「金色光雾」→「金色光晕」，[short]「金雾」→「金晕」；样片 prompt 删浮尘、体积光、「金雾边缘融进空气」；forbid 加 光雾 / 金雾 / 浮尘 / 烟雾 / 烟尘 / 体积光
- tools/skills_lib.py check — 样片 prompt 与手势图 prompt 里出现卡的禁写即报错（写了就会被画出来）
- k201 已收样片作废：[sample] video / still / clip 清空，峰值图与施法片段删了；k201_样片.mp4 被别的程序占用删不掉，已不被引用（关掉播放器后可删）；用到圣光术的镜在新样片收进来之前资料包建不起来（用户选「现在就作废」）
- 导入后自动查残留光 / 烟：用户选不做

## Follow-up 077 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 077（原编 075，与 a1 会话撞号；及同轮用户追问：冲锋收尾的撞击与晕眩；导入失败）
Summary: 冲锋去掉红光，改纯物理（扬尘尾、风压、盾撞胸口、尘土炸圈、对方踉跄僵住）；手势图文件名带键、收片按键认；圣光术新样片收进卡。

Auto-updated:
- k101 skill.toml — [look] / [short] / 两个变体改扬尘与撞击写法；mark「冲锋扬起的尘尾」；tier 全力「浓密的」；[script] flow 改 尘尾 / 扬起尘土 / 土尘 / 扬尘；forbid 加 暗红光带 / 红光带 / 暗红的光带 / 红光 / 拖光 / 眩晕圈 / 星圈（a1 报裸「光带」撞力量祝福的锁定串，收窄）；样片 prompt 重写（绿幕棚铺薄黄土；冲 → 盾撞上 → 僵住）；手势图 3 张（冲 / 撞上 / 僵住，僵住一张文生图重出）；peak 2.25
- tools/skills_lib.py — 手势图文件名改为 `{键}_{名}.png`（参考行第一项带键，即梦下载名就带键）；find_video 按键认、兼容改名前的「1_{名}.png」下载；adopt 覆盖时目标文件被占用给出明白的报错
- 资料包里的图又被库外改成「资料包N.png」（16:39，用户下载 / 上传那一刻），按出图时间与文件大小还原成带键的文件名
- k201 新样片收进卡（16:38 下载）：光柱 4.25–5.0 s，之后干净；peak 4.5、window [3.0, 5.25]
- ep01：S13 / S18 冲锋写法由 a1 会话改（剧本与生成器）；产物闸门全过，待 a1 盖章写盘

## Follow-up 076 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 076
Summary: S13 / S18 杜克冲锋由「暗红光带」改「脚下扬尘拖成尘尾、衣角被风压扯起」。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S13（室内写「蹬起的扬尘」）、S18、头注
- tools/gen_shots_szzl_ep01.py — S13 / S18 plot / camera / action 同步；S13 设计稿压回 5000 字内
- shot02 / 07 / 08 / 11 / 12 / 13 / 18 / 21 重写盘；对白通读 + 冷眼观众盖章 e3340e35a939

No conflicts found in: goals.toml
- 补（077，用户：prompt 应该和角色 / 场景一样以键开头）：五张技能卡的样片 prompt 第一行加 `{键}_{名}_样片`（k201_圣光术_样片 …），即梦下载名就以它开头；skills_lib check 加闸门（第一行不是它即报错）；资料包 3_视频prompt.txt 同步；ai_video.md「45 样片做法」补一句。
- 补（077）：五个技能资料包里的手势图在 17:03:37 同一刻又被批量改成「资料包N.png」（16:39 也发生过一次）。查过：本库与 C:\workspace 下所有脚本、今天所有会话的命令记录都没有这样的改名——是库外程序干的，原因待用户确认。对策：手势图正本挪到 `样片/手势图/{键}_{名}.png`（资料包外），资料包里放副本；`skill_keyframes.py --pack` 补回副本并清掉不认识的图；skills_lib check 发现副本缺了即报错。导入（adopt）只拷视频、从不改资料包里的图。

## Follow-up 078 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 078
Summary: S02 狼从十几米外出场、两只逃跑各走各的方向；新增敌人反应时间闸门。

Auto-updated:
- 4_剧本/episodes/ep01/script.md — S02 狼「十几步开外」且先于亚伦被观众看见，9–11s 两狼往两个方向逃
- tools/gen_shots_szzl_ep01.py — S02 plot / camera / action / ledger 同步
- shot02/planning/overhead.toml — 狼起点 y≈199.6（距亚伦 14 m）、绕后那只改往西北逃、增上游芦苇丛、机位抬高并拉宽看见狼；previz_config 重生成、previz 重渲
- tools/szzl_shot_engine.py — 新增 reaction_errors：敌人（m*）从出画到第一次交手 ≥ 4 s（REACT_LEGACY ep01 只有 S15）；已拿 S15 实测会报
- 未动：S15（3.5 s）、ep02 的重复 / 近距清单，按「规则变更不回溯」只列清单

No conflicts found in: goals.toml, states.toml

## Follow-up 079 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 079（078 已被 a1 会话占用）
Summary: 冲锋再快一点、带淡残影（仍纯物理）；被撞的人撞后低头发懵。

Auto-updated:
- k101 skill.toml — release「快得像一道影子……身后跟着两三层半透明的残影、一晃就散」，effect 撞后「头微微低下、眼神发直、身子轻轻晃了晃……像被撞懵了」，short 同步；liberty 记残影＝高速运动残像、不发光；时长锁死 1.2 s 不动，样片里「快」＝同样 1.2 s 冲 12 步（原 9 步）
- k101 样片 prompt：残影写成本人身形的半透明残像、同色、边缘运动模糊、只在全速段；僵住段低头、身子轻晃；手势图「僵住」重出（低头、两臂垂软）

## Follow-up 080 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 080
Summary: 冲锋距离再翻倍、速度再翻倍、残影更明显（仍纯物理）。

Auto-updated:
- k101 skill.toml — release「身后拖着一串四五层半透明的残影、一层比一层淡、转眼就散」，short 同步；时长仍锁 1.2 s，样片里同样 1.2 s 冲 24 步（≈18 m，079 是 12 步）
- k101 样片 prompt：目标「二十四步外」；镜头改「全景转中景」，开场目标在纵深里只有一点大，机位追不上，2.2 s 撞上时急推；残像写成四五个人影沿跑过的路线依次排开
- 手势图「冲」重出：目标在二十多米外、两人之间大片空地，并写死战士只穿锁子甲短背心
- 影响镜头：S13 / S18 引用 k101 release / short，字数变长（S13 近 5000 设计稿上限），已通知 a1 会话

## Follow-up 081 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 081
Summary: S02 芦苇里先闻声后走出；S07 30 s；S07 / S08 资料包挂圣光术视频。

Auto-updated:
- script.md — S02：2s 芦苇窸窣、2.6s 低吼、3.5s 狼才从芦苇走出（七八步外）、5.5s 咬靴尖；S07：28→30 s，开头 0–3.5s、3.5–11s 铺垫（亚伦开口 + 萨缪尔放下书、吸气）、21.9–27s 用力念 + 咬牙无声再试、27–30s 静看空手；本集 617→619 s
- goals.toml — S07 fail 引文改「掌心还是空的」
- tools/szzl_shot_engine.py — Shot.pv_end（白模参考截止，S07 / S08 = 27.5 s，腾出 30 s 参考视频预算给 2.27 s 施法片段）；reaction_errors 改按「察觉时刻 alert_t」≥3.5 s
- tools/shot_overhead.py — actor 合法键加 alert_t；tools/previz/build_previz.py — [全局]「参考截止」
- shot02 / 07 / 08 白模重渲；资料包 S02 / S07 / S08 对齐，S07 / S08 挂 k201_施法片段.mp4

No conflicts found in: states.toml

## Follow-up 082 — 2026-10-01
Source: user_input/follow_ups/202610.md - section 082
Summary: 冲锋距离 ×1.5、速度 ×1.5（36 步 / 1.2 s），残影一闪就没，起步「刷」的破风声。

Auto-updated:
- k101 skill.toml — release「像一阵疾风直冲向{目标}，「刷」的一声破风响，身后甩出一串……一闪就没」，short「像疾风一样「刷」地冲向{目标}，身后一闪而没的残影……」；liberty 记破风声对应原典冲锋的呼啸声
- k101 样片 prompt：三十六步外、大全景开场、残影每个停不到 0.1 s 就散、声音段加蹬地那一下又尖又快的「刷」
- 手势图「冲」重出两次（第二次写死目标只占画面高度十分之一；实际出图约四分之一，距离主要靠视频文字）；资料包 3_视频prompt.txt 同步
- 影响镜头：S13 / S18 引用 k101 release / short，已通知 a1 会话
- user_input/revised_prompt.md 重生成
- （同日追加）k101 样片导入：jimeng-2026-10-01-7846（5.06 s，按 080 版资料包出）；峰值改 2.4 s（盾抵胸口、尘土炸开，2.25 s 处是推镜糊帧），window [0.7, 3.4] 不变

## Follow-up 083 — 2026-10-01（用户睡前交代：自主完成，不再提问）
Source: user_input/follow_ups/202610.md - section 083
Summary: 六镜修改 + 圣光术通则 + 收尾丝滑；流程改进按 best judgment 直接落成闸门。

Auto-updated:
- S02：26 s；先闻声 → 抬头抄锤 → 狼从芦苇走出；杜克打斗动起来（Cascadeur 重烘）；被咬后转头 / 吼 / 回头窘 + "Yeah, run! ...Don't tell anyone." + 收尾拍肩迈步
- S04：治安官对庄稼汉改说 "Good man. Off you go."，不再同句念两遍；新增 `script.toml [repeat_ok]` 与 script_tools 同镜同句闸门
- S07：亚伦念口令改磕绊像新手（"Pheta... vi... uh..." → 萨缪尔画外 "Slower." → 重来），结尾加萨缪尔点头
- S08：删开头画外 "Again?! AGAIN?!"
- S09：数数时画面不见蜡烛 / 矿工，亚伦对着黑洞洞的坑道数；overhead 去 gaze、矿工退到机位后
- S10：钢盾 80×50 → 115×72 cm（e5205 卡、即梦三视图重出、previz 盾 0.72×1.15 m、prompt 描述）
- S11：杜克抬头盯着敌人（Cascadeur 重烘 + 抬头部件）；去掉结尾 "One. Two."；29 s；收尾加亚伦扶他右臂
- S12：删圣光情节，直接包扎，24 s；goals 圣光术 used 改 S21；亚伦「坐」而不是「跪」（避开与 S11 尾重复）
- S15：开头杜克先沉默再跺脚（接 S14 尾的低落）
- 圣光术通则：【技能】句末加快慢照参考 / 光柱罩被救治者（HOLY_PACE）
- 新闸门：同镜同句（script_tools）、敌人反应时间 alert_t（szzl）、打斗抬头（choreo）
- 判断记录（自主模式）：① 做了冷眼观众接缝审计，只改 4 处最便宜的（S02 / S07 / S11 / S15），其余 6 处留作清单；② S15 反应时间 3.5 s 与打斗抬头对 S13 / S18 等已出片镜登记遗留、不回溯；③ S12 删光后保留 "Somebody's got to buy you time."（接 S11 的未治完）

No conflicts found in: states.toml

## Follow-up 084 — 2026-10-02
Source: user_input/follow_ups/202610.md - section 084
Summary: 动作镜改用三张状态图指导视频（S09、S11、S13–S25）；previz MP4 只留给特别复杂的镜；S09 亚伦打小怪不打盾。

Auto-updated:
- tools/szzl_shot_engine.py — Shot.kf（状态图）；有 kf 的镜 previz 免、参考行挂状态图、USAGE_KF、kf_errors（图缺 / 秒数越界 / 重名）
- tools/shot_keyframes.py（新）— 按 Shot.kf 出即梦状态图（场景图 + 角色换装图 + 装备图 + 前一张图作参考；prompt ≤ 1550 字），出到 shots/shotNN/状态图/
- tools/gen_shots_szzl_ep01.py — KF_S09 / KF_S11 / KF_S13…KF_S25 各三张；S09 动作改「亚伦站杜克右侧半步、锤砸在矿工身上、绝不碰杜克的盾」，负面词加「用锤砸杜克的盾」
- 保留 previz 的镜：S02 / S07 / S08 / S10 / S12（已渲）；其余 previz 文件夹留作历史，引擎不再读
- 技能样片视频（k201 施法片段）照旧作参考

No conflicts found in: goals.toml, states.toml

## Follow-up 085 — 2026-10-02
Source: user_input/follow_ups/202610.md - section 085
Summary: S07 / S09 / S11 改回绿幕小人偶 previz（Shot.gs）；S07 retime 30 s、S09 站位重写。

Auto-updated:
- tools/szzl_shot_engine.py / tools/previz/build_previz.py — Shot.gs、绿幕地面 + 穹顶、previz_config 不写场景；参考截止 pv_end
- tools/gen_shots_szzl_ep01.py — S07 / S09 / S11 gs=True、不再用状态图
- script.md — S07 咒语与光效对时、光后停顿、慢讲、30 s；S09 两人始终在洞外坡上面对洞口

No conflicts found in: goals.toml

## Follow-up 086 — 2026-10-02
Source: user_input/follow_ups/202610.md - section 086
Summary: S05–S07 铺伤与求治；S11 战斗中施法、杜克扔木盾、肩伤愈合近景；S12 同步。

Auto-updated:
- script.md — S05 伊根「矿里更糟」；S06 恶战加强（十几只围住、亚伦左上臂被镐划伤）；S07 带伤求学、圣光治好胳膊、特写；S11 重写 12–25 s（偷袭苦力、扔盾、17.4–19 s 肩头近景）；S12 伤口「合上一半」、杜克想起扔盾争时间
- states.toml — 亚伦左上臂（S06–S07）、左袖豁口 + 干血渍（S08–S12）；杜克肩伤措辞
- tools/gen_shots_szzl_ep01.py — S06 / S07 / S11 / S12 同步；SLEEVE 常量进 S08–S12 的亚伦状态
- tools/shot_overhead.py / szzl_shot_engine.py — 新命中类型「投」（扔出去的东西，不查够得着）
- 2026-10-02 提示：S06 为 Cascadeur 旧镜、仍未重渲（只改文字），用户重新生成时需注意；S05–S12 需重新生成
- shot11/planning/overhead.toml — 偷袭的矿工、祖父木盾 prop、近景机位 17.4 s、两个 gaze

No conflicts found in: goals.toml

## Follow-up 087 — 2026-10-02
Source: user_input/follow_ups/202610.md - section 087
Summary: S06 重做打斗（亚伦面朝怪、三波敌人、左小臂被划）改绿幕 previz；S07 小臂 + 不修衣服；全剧左上臂→左小臂。

Auto-updated:
- script.md / states.toml / gen_shots_szzl_ep01.py — 左上臂→左小臂；S06 6–17s 重写；S07 特写补「光只治肉、衣服不复原」
- shot06/planning/overhead.toml — 亚伦朝向、土洞钻出的矿工、偷袭的矿工、13s 挨一镐（疼 1 s）14.1s 单手回砸
- S06 gs=True，previz 重配并重渲

No conflicts found in: goals.toml

## Follow-up 088 — 2026-10-02
Source: user_input/follow_ups/202610.md - section 088
Summary: 加 G19「友方不入挥击线」，并修 S05 / S06 / S09 / S11 / S15 的站位。

Auto-updated:
- tools/shot_overhead.py — friend_actors / friend_line_errors：自己人出手打敌人时，另一个自己人不得在「出手→目标」±55°、够得着的距离内
- tools/previz/build_previz.py — 命中新键「友方」：挥击窗口里锤头离每个自己人（含盾）≥ 0.45 m，否则 blocker（读渲出来的结果）
- tools/szzl_shot_engine.py — previz_config 抄「友方」；命中行自动加「锤只落在敌人身上，不碰同伴及其盾」
- 各镜 overhead.toml — S06 加「南侧的矿工」让亚伦打侧面；S11 加「盾右边的矿工」；S09 亚伦挪到杜克东侧；S05 杜克 / 头狼换位；S15 南狼挪开
- 判断记录：S05 / S15 的 Cascadeur 旧 previz 不重渲（S15 无 previz），只改平面图

No conflicts found in: goals.toml, states.toml
