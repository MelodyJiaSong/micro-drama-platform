---
worker_id: level-specialist-02-bdd_scenarios
stage: 5
role: level-specialist
level: bdd_scenarios
status: complete
blockers: []
confidence: medium
---

# BDD scenarios — jimeng_web_bridge

Run: jimeng_web_bridge-20260913-093603 · 契约来源：`final_specs/spec.md`（FR-1..FR-56）

本文件为规则密集的部分写出**特性级行为**，采用 Scenario Outline + Examples 表的形式。断言只针对**消费方能看到的东西**：
- 预检 JSON `{error_code, message, hint, config_key?}`；
- SQLite 中 job / batch 的状态与转移记录；
- 盘上文件与 sidecar；
- Fake 即梦站点记录的操作时间线（点击次数、上传文件名、编辑器 mention 序列）；
- fake `dreamina` 的调用记录。

不断言内部实现。

**约定**
- `HY` = `ai_videos/huangye_shenghuo`。「real」行的 shot md 取自仓库原件，按 development.md §10 要求复制到 `tests/fixtures/real_shots/`；参考媒体按原相对路径放入 fixture 树。媒体字节存在 R2、本机未必 pull，所以测试不得依赖本机 `ai_videos/` 里是否真有该文件。
- `error_code` 名称（`REF_NOT_FOUND` 等）只是占位名，spec 没有定义枚举。**契约断言以错误类别 + `config_key` / hint 为准**：FR-8 要求错误指出应填的 config 键。
- 带 `AMB-nn` 的行：spec 没有决定其期望结果，见文末「Ambiguities found」。在 stage-5 汇总定调之前，这些行不作为阻断用例。
- 执行层：纯函数与实体（预检、解析、状态机、指纹、命名）→ unit；调度 / 暂停 / 填写 / 落盘 → system（Fake 站点 + fake dreamina）。
- 失败严重度（general.md + development.md）：
  - 黄金路径 BDD 失败 = `blocker`；
  - FR-16（未确认花积分）、FR-19（重复提交）、沙箱逃逸 = `critical`（爆炸半径为积分与账号）。

**真实数据基线**（2026-09-13 在本机按 FR-8 默认规则扫描全仓 `参考:` 行，共 271 行，与 spec 统计一致）

| 形态 | 条数 | 默认规则下的结果 |
|---|---|---|
| image 项（`场景参考图*`/`*锚点`/`角色参考图`/`单位参考图`/`场景主体`/`物件主体`） | 382 | 204 唯一命中；178 找不到（原因见「覆盖观察」） |
| entity 项 | 57 | 55 命中角色卡；2 条是 duikang `driver`（卡目录无 `c{N}_` 前缀） |
| video 项（previz） | 30 | 1 命中；29 找不到（duikang 盘上是 `shot01_previz.mp4`，与 name `previz_shot01` 不一致） |
| first_frame 项 | 19 | 19 找不到（`shot{NN-1}_lastframe.png` 要等上一镜出片后才会有） |
| 旧写法 已填槽位 `=>@N` | 107 | 预检错误 |
| 旧写法 无括号 | 163 | 预检错误 |
| 未命中任何 label | 10 | `道具参考图` ×8、`大地裂痕参考图`、`道家手印参考图` |

---

## Feature 1: 参考项解析

绑定 FR-6、FR-8、FR-10、FR-11.1、FR-30（上传名）、FR-31（mention 序列）

作为 Claude，我把一个 `shotNN.md` 交给 `precheck_batch`，期望 service 把 `参考:` 行的每一项确定地解析成盘上文件或主体名。解析不了时，给出我能照做的 config 键，而不是猜测。

Background:
- Given 全局 config 与各剧 `jimeng_config.toml` 均为 FR-2 提议默认值；
- And `references.search_exclude = ["_deleted", "_candidates", "renders", "previz/frames"]`；
- And `HY/hy3/jimeng_config.toml` 含 `entities.overrides = { "c1_砌炉的老人" = "hy3_主角" }`；
- And 主体快照（24 h 内同步）含 `hy3_主角`、`hy1_主角`、`hy1_造家的人`。

### Scenario Outline 1.1: `参考:` 行切分出有序条目

- Given 某 shot 的 `## 视频 prompt` 首个 text 围栏里 `参考:` 行为 `<line>`
- When `ShotPromptReader` 解析
- Then 得到按出现顺序排列的 `(name, label)` 列表 `<items>`

| ID | 来源 | line（节选） | items |
|---|---|---|---|
| P01 | real HY/hy3 shot02 | `` `bg11-1(场景参考图)=>@`，`砌炉的老人(Seedance 人物 entity)=>@`，`p2-1(随身装备锚点)=>@`，`p3-1(抹泥板锚点)=>@` `` | (bg11-1, 场景参考图), (砌炉的老人, Seedance 人物 entity), (p2-1, 随身装备锚点), (p3-1, 抹泥板锚点) |
| P02 | real HY/hy2 shot10 | `` `bg11-1(场景参考图·第四段：坑口全景（根盘背面冒烟）)=>@` `` | (bg11-1, `场景参考图·第四段：坑口全景（根盘背面冒烟）`)——label 内的全角括号保持完整 |
| P03 | real duikang_shangzeng shot01 | `` `entropy_city_bg1_广场(场景主体)=>@, f80_ferrari(物件主体)=>@, previz_shot01(previz灰模视频)=>@` ``（一个反引号内含多项，ASCII 逗号分隔） | 3 项，顺序同原文（AMB-01） |
| P04 | real xingji_yingjiu shot03 | `` `本镜首帧(上一镜末帧)=>@, c4_幽灵特工(单位参考图)=>@, bg1_菌毯岩脊(场景参考图)=>@` `` | 3 项（AMB-01） |

### Scenario Outline 1.2: 单项 → ReferenceItem 或可操作的预检错误

- Given 剧 `<drama>` 的 shot `<shot>` 含参考项 `<item>`，fixture 树状态为 `<disk>`
- When 执行静态预检
- Then 该项按 `references.rules` 自上而下命中第一条规则 `<rule>`
- And 结果为 `<expected>`
- And 若为错误，该条目状态为 `error`、hint 含 `<config_key>`，且批次不可确认

| ID | drama / shot | item | disk（fixture） | rule → kind / resolver | expected | config_key |
|---|---|---|---|---|---|---|
| R01 | HY/hy3 shot02 | `bg11-1(场景参考图)` | hy1、hy2、hy3、hy4 各有一个 `bg11-1.png`（real） | 场景参考图* → image / stem_in_drama | `resolved_path = HY/hy3/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11-1.png`，sha256 = 文件字节哈希。**只在 hy3 剧根内搜索，兄弟集不算多重匹配** | — |
| R02 | HY/hy3 shot02 | `p2-1(随身装备锚点)` | `props/p2_随身装备/p2-1.png` | *锚点 → image | `resolved_path = …/hy3/2_世界观人设/props/p2_随身装备/p2-1.png` | — |
| R03 | HY/hy3 shot02 | `砌炉的老人(Seedance 人物 entity)` | 卡目录 `characters/c1_砌炉的老人/` | Seedance 人物 entity → entity | `kind=entity, entity_name=hy3_主角`（override 生效，模板值 `hy3_砌炉的老人` 被取代） | — |
| R04 | HY/hy1 shot12 | `bg7-4(场景参考图·第四段：林中四十米外的远景)` | `scenes/yulin/bg7_棚屋雨歇夜/bg7-4.png` | 场景参考图* → image | 命中；`label` 保存完整原文 | — |
| R05 | HY/hy2 shot12 | `p2_随身装备(随身装备锚点)` | 本集只有 `p2_随身装备.png.link.json`，target 指向 hy1（real） | *锚点 → image | `resolved_path = HY/hy1/2_世界观人设/props/p2_随身装备/p2_随身装备.png`（取 link 的 target），sha256 = target 字节哈希（AMB-08） | — |
| R06 | HY/hy1 shot09 | `c2_犀鸟(犀鸟锚点)` | `characters/c2_犀鸟/c2_犀鸟.png` | *锚点 → image | **按 image 处理**，不因为它是角色卡就当主体 | — |
| R07 | HY/hy2 shot12 | `造家的人(Seedance 人物 entity)` | `hy2/…/c1_造家的人/` 只含指向 hy1 的 `.link.json` | entity | `entity_name = hy1_造家的人`（跨集沿用来源集缩写，FR-3；另见 AMB-09） | — |
| R08 | xianjian_yi_mv shot12 | `shot12_previz(3D预演视频)` | `shots/shot12/shot12_previz.mp4`（real） | 3D预演视频 → video / stem_in_shot | `kind=video`，在本镜目录内命中 | — |
| R09 | duikang_shangzeng shot01 | `previz_shot01(previz灰模视频)` | 盘上是 `shot01_previz.mp4`（real，name ≠ stem） | previz灰模视频 → video / stem_in_shot | `REF_NOT_FOUND` | `references.overrides."previz_shot01"` |
| R10 | xingji_yingjiu shot03 | `本镜首帧(上一镜末帧)` | fixture 放入 `shots/shot02/shot02_lastframe.png` | 上一镜末帧 → first_frame / prev_shot_lastframe | `kind=first_frame, name=本镜首帧`，路径为上一镜末帧 | — |
| R11 | xingji_yingjiu shot03 | 同上 | 上一镜末帧不存在（real 现状） | 同上 | `REF_NOT_FOUND`（AMB-07：同批承接链） | `references.overrides."本镜首帧"` |
| R12 | 任一剧 shot01 | `本镜首帧(上一镜末帧)` | 不存在 shot00 | 同上 | AMB-07 | — |
| R13 | duikang_shangzeng shot09 | `driver(人物主体)` | 卡目录 `characters/driver/`，无 `c{N}_` 前缀（real） | 人物主体 → entity | AMB-05；即便能解析，abbrev 为空仍报 `drama.abbrev` 错误（见 E07） | `drama.abbrev` |
| R14 | rexue_gaoxiao shot02 | `学校泳池_bg3_水下_幽蓝=>@2` | — | 不进入规则匹配 | `REF_LEGACY_FILLED_SLOT`（AMB-04） | `references.overrides."学校泳池_bg3_水下_幽蓝"` |
| R15 | rexue_gaoxiao shot01 | `学校泳池_bg2_水面_俯拍=>@1` | — | 不进入规则匹配 | 预检错误；既无括号又已填槽位，报哪个错误码未定（AMB-04） | 同上形态 |
| R16 | wushen_juexing shot12 | `c4_裴昭=>@` | — | 不进入规则匹配 | `REF_LEGACY_NO_LABEL`（AMB-04） | `references.overrides."c4_裴昭"` |
| R17 | xianjian_yi_mv shot03 | `p1_木剑(道具参考图)` | — | 无规则命中 | `REF_LABEL_UNMATCHED` | `references.rules`（或 `references.overrides."p1_木剑"`） |
| R18 | xianjian_yi_mv shot12 | `dilie(大地裂痕参考图)` | — | 无规则命中 | `REF_LABEL_UNMATCHED` | `references.rules` |
| R19 | HY/hy1 shot01 | `bg9-1(场景参考图)` | hy1 只有 `bg9_林冠光柱/bg9-1.mp4`；hy2、hy3、hy4 各有 `bg9-1.png`（real） | 场景参考图* → image | `REF_NOT_FOUND`：image 解析器不收视频扩展名（AMB-06），兄弟集的同名文件不在搜索范围 | `references.overrides."bg9-1"` |
| R20 | HY/hy2 shot07 | `p3-1(树皮门板锚点)` | 盘上是 `p3-1_树皮门板锚点.png`（real，stem ≠ name） | *锚点 → image | `REF_NOT_FOUND`（stem 必须全等，不做前缀匹配） | `references.overrides."p3-1"` |
| R21 | xingji_yingjiu shot01 | `bg1_菌毯岩脊(场景参考图)` | name 对应主体目录 `scenes/bg1_菌毯岩脊/`，目录里只有 md（real） | 场景参考图* → image | `REF_NOT_FOUND`（目录名不等于图片） | `references.overrides."bg1_菌毯岩脊"` |
| R22 | fixture drama | `bg3-1(场景参考图)` | `scenes/x/bg3_a/bg3-1.png` 与 `props/p9_b/bg3-1.png` 同时存在 | 场景参考图* → image | `REF_MULTI_MATCH`，message 列出两个路径 | `references.overrides."bg3-1"` |
| R23 | fixture 系列集 | `bg3-1(场景参考图)` | 剧根和 `{series}/_series/` 各有一个 | 同上 | `REF_MULTI_MATCH`（两处都在搜索范围） | 同上 |
| R24 | fixture drama | `bg3-1(场景参考图)` | 另有 `_candidates/bg3-1/…`、`renders/bg3-1.png`、`previz/frames/bg3-1.png` 各一 | 同上 | 唯一命中正式文件，排除目录不计 | — |
| R25 | fixture drama | `bg3-1(场景参考图)` | `references.overrides."bg3-1" = "ai_videos/…/bg3-1_远景.png"` | override 优先于 rules | `resolved_path` = override 路径 | — |
| R26 | fixture drama | `造家的人(Seedance 人物 entity)` | `references.overrides."造家的人" = "entity:hy1_主角"` | override | `kind=entity, entity_name=hy1_主角` | — |
| R27 | fixture drama | 任意 image 项 | override 值为 `ai_videos/../projects/x.png` 或绝对路径 `C:/Windows/x.png` | override | 拒绝，沙箱错误（`critical`） | `references.overrides."{name}"` |
| R28 | fixture drama | 任意 image 项 | `.link.json` 的 target 逃出 `ai_videos/`，或 target 是 symlink | stem_in_drama | 拒绝（FR-10，`critical`）；symlink 用例在 Windows 上带 skip 标记（development.md §5） | — |
| R29 | fixture drama | `老人(砌炉的老人声音)` | `characters/c1_x/老人.mp3` | *声音 → audio / stem_in_drama | `kind=audio`（仓库目前 0 条真实样本，只能用 fixture 覆盖） | — |

### Scenario Outline 1.3: 围栏字段解析

- Given shot md 的 `## 视频 prompt` 段为 `<fence_shape>`
- When 解析
- Then `<field>` = `<expected>`

| ID | 来源 | fence_shape | field | expected |
|---|---|---|---|---|
| F01 | real HY/hy3 shot02 | 首个 text 围栏（首行 `shot02`，含 `参考:` 行），CRLF 或 LF | `prompt` | 与围栏内容逐字节相等，包括首行、`参考:` 行和原换行符 |
| F02 | real 409 条 | `时长: 22秒` | `duration_s` | 22 |
| F03 | real 3 条 | `时长: 22s` | `duration_s` | 22 |
| F04 | real 21 条 | `` 时长: `12s` ``（反引号包裹） | `duration_s` | AMB-03 |
| F05 | real 196 条 | `比例: 16:9` | `ratio` | `16:9` |
| F06 | real 195 条 | `比例: 16:9（项目 divergence·style_guide 画幅节）` | `ratio` | AMB-03 |
| F07 | real 2 条 | `比例: 9:16 ｜ 时长: 9秒`（同一行） | ratio、duration_s | AMB-03 |
| F08 | real 21 条 | `比例: 2.35:1` | 预检 | AMB-03（`model_limits` 无比例列） |
| F09 | real 12 条 | 围栏后 `## 反向提示词` + text 围栏 | `negative_prompt` | 该围栏全文 |
| F10 | real 295 条（含 hy3 shot02） | 围栏后 `> **反向提示词**（粘进平台负向框…）：` + text 围栏 | `negative_prompt` | AMB-02（按 development.md §10 应接受，但 FR-8 写的是「标题」） |
| F11 | real 旧剧 | 正向围栏内含 `负面词: …` 行，其后无反向围栏 | `negative_prompt` / `prompt` | `negative_prompt = None`；`负面词:` 行留在 prompt 原文里，不抽出 |

### Scenario 1.4: hy3 shot02 的上传名与 mention 序列（黄金路径，FR-30/31）

- Given R01–R03 与 `p3-1` 均已解析，并已确认
- When WebUiBackend 执行 upload 与 fill
- Then Fake 站点依次收到的上传文件名为 `bg11-1.png`、`p2-1.png`、`p3-1.png`（主体项不上传；AMB-28）
- And 编辑器的 mention 节点序列为 `[bg11-1, hy3_主角, p2-1, p3-1]`，与 `=>@` 的出现顺序一致
- And 规范化空白后的编辑器纯文本（mention 按名称计）等于期望文本
- And 若 R05 这类 link 项的文件名与 name 不同，service 先复制到临时目录并改名为 `{name}{ext}` 再上传

---

## Feature 2: 主体命名与对账

绑定 FR-2 `[drama]`/`[entities]`、FR-3、FR-11.6、FR-48、FR-49、FR-50

作为用户，我希望每部剧的期望主体名都能由 config 算出来并可以覆盖。命名不确定时要让我确认，不能静默建出名字错误的主体。

### Scenario Outline 2.1: 期望主体名推导

- Given 剧 `<drama>` 的 config `<config>`，角色卡 `<card>`
- When 执行 `DramaConfigCommand.propose`，并对引用该角色的 shot 做预检
- Then 期望主体名为 `<name>`，propose 标记为 `<flag>`，预检结果为 `<precheck>`

| ID | drama | card | config | name | flag | precheck |
|---|---|---|---|---|---|---|
| E01 | HY/hy3 | `c1_砌炉的老人` | abbrev=hy3（系列成员默认），无 override | `hy3_砌炉的老人` | 快照有 `hy3_主角`、没有 `hy3_砌炉的老人` 时标「期望主体名与即梦现有主体不一致」（判定规则见 AMB-10） | error：快照中不存在，hint 指向主体对账页 |
| E02 | HY/hy3 | `c1_砌炉的老人` | `overrides."c1_砌炉的老人" = "hy3_主角"` | `hy3_主角` | 无 | ok |
| E03 | HY/hy3 | `c2_獾` | 默认 | `hy3_獾` | 无 | 被引用时按快照判断 |
| E04 | HY/hy2 | `c1_造家的人`（图片为 `.png.link.json` → hy1） | 默认 | `hy1_造家的人` | 无 | 快照含 `hy1_造家的人` → ok |
| E05 | HY/hy2 | 同 E04 | hy1 config 有 `overrides."c1_造家的人" = "hy1_主角"` | AMB-09 | — | — |
| E06 | HY/hy3 | 已有 `jimeng_config.toml` | 再次 propose | 不覆盖文件，返回逐键 diff 建议 | — | — |
| E07 | wushen_juexing（无 `series.json`） | `c4_裴昭` | abbrev 为空 | 无法生成 | `needs_confirmation: true`，原因「独立剧缺缩写」 | error，`config_key = drama.abbrev` |
| E08 | duikang_shangzeng | `driver`（无 `c{N}_` 前缀） | abbrev=`dk` | AMB-05 | — | — |
| E09 | fixture 系列集 hy3 | `c3_在草崖下砌了一辈子炉子的沉默老人` | 默认 | `hy3_在草崖下砌了一辈子炉子的沉默老人`（正好 20 字） | 无 | ok（字数计法见 AMB-11） |
| E10 | fixture 系列集 hy3 | `c3_在草崖下砌了一辈子炉子的沉默的老人` | 默认 | 21 字 | `needs_confirmation`（名称超长） | error，`config_key = entities.overrides."c3_…"` |
| E11 | HY/hy3 | 任一被引用角色 | 快照 25 h 前同步，含期望名 | — | — | warning（快照过期），不阻断确认 |
| E12 | HY/hy3 | 任一被引用角色 | 从未同步过主体 | — | — | error，hint 指向主体对账页 |

### Scenario Outline 2.2: 对账三态（FR-48）

- Given 主体快照为 `{hy3_主角, hy1_主角, xj_游侠}`
- And hy3 config 含 E02 的 override；hy1 config 无 override
- When 执行 `EntityQuery.reconcile()`
- Then 名称 `<name>` 的状态为 `<state>`

| name | state |
|---|---|
| `hy3_主角` | `mapped` |
| `hy1_造家的人`（hy1 的期望名，hy2 跨集沿用） | `missing_on_platform` |
| `hy1_主角` | `unmapped_on_platform` |
| `xj_游侠` | `unmapped_on_platform` |

### Scenario 2.3: 创建只增不改（FR-49/50）

- Given `hy3_獾` 为 `missing_on_platform`，并已在 UI 确认页确认创建
- When 执行 `EntityCommand.create`
- Then Fake 站点「新建主体」表单只提交一次，随后再同步一次，快照中出现 `hy3_獾`
- And 若确认前快照里已有同名主体，则直接复用：表单提交 0 次、改名 0 次、删除 0 次
- And 若 `source_images` 的 glob `{card_dir}/*-1.png` 无命中 → 预检 error，`config_key = entities.source_images`

---

## Feature 3: 能力矩阵预检

绑定 FR-1 `routing`/`model_limits`、FR-2 `[precheck]`、FR-11.2–11.5

作为用户，我不希望请求在花积分之后才因为模型档位不支持而失败。所有能力判断都在静态预检里完成，运行时不降级。

### Scenario Outline 3.1

- Given 全局 `routing.video = <rv>`、`routing.image = <ri>`，`model_limits` 为提议默认值
- And 一条 `<kind>` 请求：model `<model>`、时长 `<dur>`、分辨率 `<res>`、参考数（图/视频/音频）`<refs>`、主体 `<ent>`、prompt 字数 `<chars>`
- When 静态预检（不开浏览器、不调 CLI）
- Then 结果为 `<result>`，错误的 `config_key` 为 `<key>`
- And 结果与 backend 可用性无关（Fake 站点、fake dreamina 均未被调用）

| ID | kind | rv/ri | model | dur | res | refs | ent | chars | result | key |
|---|---|---|---|---|---|---|---|---|---|---|
| C01 | video | web/cli | seedance2.5 | 30 | 720p | 3/0/0 | 1 | 1200 | ok | — |
| C02 | video | web/cli | seedance2.5 | 31 | 720p | 3/0/0 | 1 | 1200 | error 时长越界 | `model_limits.seedance2.5` / `video.duration_source` |
| C03 | video | web/cli | seedance2.5 | 3 | 720p | 1/0/0 | 0 | 800 | error 时长低于 4 | 同上 |
| C04 | video | web/cli | seedance2.5 | 4 | 480p | 1/0/0 | 0 | 800 | ok | — |
| C05 | video | web/cli | seedance2.5 | 22 | 1080p | 3/0/0 | 1 | 1200 | error 分辨率不支持（以 config 为准，探针结果回写 config） | `video.resolution` |
| C06 | video | web/cli | seedance2.0_vip | 15 | 1080p | 9/3/3 | 1 | 1200 | ok（web 支持主体） | — |
| C07 | video | web/cli | seedance2.0_vip | 16 | 720p | 1/0/0 | 0 | 800 | error 时长越界 | `model_limits.seedance2.0_vip` |
| C08 | video | web/cli | seedance2.0 | 10 | 1080p | 1/0/0 | 0 | 800 | error 分辨率不支持 | `video.resolution` |
| C09 | video | web/cli | seedance2.0fast | 10 | 720p | 1/0/0 | 0 | 800 | ok | — |
| C10 | video | web/cli | seedance2.5 | 22 | 720p | 30/10/10 | 1 | 1200 | ok（主体是否计入上限见 AMB-12） | — |
| C11 | video | web/cli | seedance2.5 | 22 | 720p | 31/0/0 | 0 | 1200 | error 图片超限 | `model_limits.seedance2.5` |
| C12 | video | web/cli | seedance2.5 | 22 | 720p | 0/11/0 | 0 | 1200 | error 视频超限 | 同上 |
| C13 | video | web/cli | seedance2.0_vip | 10 | 720p | 10/0/0 | 0 | 800 | error 图片超限 | `model_limits.seedance2.0_vip` |
| C14 | video | web/cli | seedance2.5 | 22 | 720p | 30/0/0 + 1 first_frame | 0 | 1200 | AMB-12 | — |
| C15 | video | **cli**/cli | seedance2.5 | 22 | 720p | 3/0/0 | 0 | 1200 | error backend 不具备该能力，**不降级到 2.0** | `routing.video` |
| C16 | video | **cli**/cli | seedance2.0_vip | 15 | 720p | 9/3/3 | 0 | 1200 | ok | — |
| C17 | video | **cli**/cli | seedance2.0_vip | 12 | 720p | 2/0/0 | 1 | 1200 | error cli 不支持主体 | `routing.video` |
| C18 | image | web/cli | seedream5.0 | — | 2k | 0/0/0 | 0 | 900 | ok，command=text2image | — |
| C19 | image | web/cli | seedream5.0 | — | 4k | 10/0/0 | 0 | 900 | ok，command=image2image | — |
| C20 | image | web/cli | seedream5.0 | — | 2k | 11/0/0 | 0 | 900 | error 超出 image2image 1–10 张 | `image.model` |
| C21 | image | web/cli | seedream5.0 | — | 1k | 0/0/0 | 0 | 900 | error 分辨率不支持 | `image.resolution` |
| C22 | image | web/cli | seedream3.0 | — | 4k | 0/0/0 | 0 | 900 | error（3.x 只支持 1k/2k） | `image.resolution` |
| C23 | image | web/cli | seedream5.0 | — | 2k | 1/0/0 | 1 | 900 | error cli 图片请求不能带主体 | `routing.image` |
| C24 | image | web/**web** | seedream5.0 | — | 2k | 0/0/0 | 0 | 900 | error 网页端出图不在 v1 范围、矩阵无此能力 | `routing.image` |
| C25 | video | web/cli | seedance2.5 | 22 | 720p | 1/0/0 | 0 | 5000 汉字 | ok | — |
| C26 | video | web/cli | seedance2.5 | 22 | 720p | 1/0/0 | 0 | 5001 汉字 | error prompt 超长 | `precheck.prompt_max_chars` |
| C27 | video | web/cli | seedance2.5 | 22 | 720p | 1/0/0 | 0 | 4990 汉字 + 15 个换行或 ASCII 字符 | AMB-11 | — |
| C28 | video | web/cli | seedance3.0（矩阵中不存在） | 22 | 720p | 1/0/0 | 0 | 800 | error 未知模型 | `video.model` |

---

## Feature 4: 作业状态机

绑定 FR-16、FR-17、FR-19、FR-20、FR-22、FR-23、FR-29、FR-31、FR-33

作为用户，我要求任何一次积分支出都能追溯到一次确认和一次点击。重启、取消、失败都不能导致重复提交。每次转移记录 `{from, to, at, reason?}`。

### Scenario Outline 4.1: 合法转移

- Given job 处于 `<from>`（其 batch 已确认）
- When 发生 `<trigger>`
- Then job 进入 `<to>`，转移记录的 reason = `<reason>`
- And `<assert>`

| ID | from | trigger | to | reason | assert |
|---|---|---|---|---|---|
| T01 | queued | 调度器选中（web 队列未暂停） | preparing | — | 子步骤从 `set_params` 开始 |
| T02 | preparing | `set_params → upload → fill → preview` 全部完成 | awaiting_submit_slot | — | artifacts 有全页与 composer 两张截图、页面预计积分 |
| T03 | awaiting_submit_slot | 名额与间隔都满足（Feature 9） | submitting | — | `submitting` 行与指纹**先于** Fake 站点收到点击落库 |
| T04 | submitting | 截获提交响应，拿到平台任务标识 | generating | — | `platform_task_id` 非空 |
| T05 | submitting | 未截获响应，但历史里有「提交时刻之后、prompt 前缀一致」的最新一条 | generating | — | 用对账到的记录作为任务标识；点击次数 = 1 |
| T06 | submitting | 未截获响应，历史对账也失败 | paused_needs_human | `restart_during_submit` | 点击次数 = 1，之后不再点击 |
| T07 | generating | 状态响应为完成 | downloading | — | 进度写入 job |
| T08 | downloading | 临时文件通过 size + sha256 + ffprobe 校验 → rename → sidecar | done | — | 目标文件与 sidecar 同时存在；实扣积分入库 |
| T09 | generating | 状态响应为审核拒绝 | failed | `moderation_reject` | prompt 未改写，没有新提交 |
| T10 | generating | 距提交超过 `wait.timeout_h`（时钟快进 12 h 01 min） | paused_needs_human | `wait_timeout` | 队列其余 job 继续 |
| T11 | submitting | 页面提示「并行任务已达上限」 | awaiting_submit_slot | 背压，不算失败 | AMB-18 |
| T12 | submitting（cli） | fake dreamina 返回 `submit_id` | generating | — | `submit_id` 在轮询前已落库 |
| T13 | paused_needs_human | `resume_job`，自检（canary 或 `user_credit`）通过 | AMB-15 | — | — |
| T14 | paused_needs_human | `resume_job`，自检失败 | paused_needs_human（不变） | 原 reason 保留 | 响应带自检失败原因 |

### Scenario Outline 4.2: 非法转移（抛领域错误，状态与点击次数不变）

- Given job 处于 `<from>`
- When 尝试 `<attempt>`
- Then 抛领域错误，job 仍是 `<from>`，Fake 站点点击次数不变

| ID | from | attempt | 严重度 |
|---|---|---|---|
| I01 | queued | → submitting | blocker |
| I02 | queued | → generating | blocker |
| I03 | preparing | → submitting（跳过 awaiting_submit_slot） | blocker |
| I04 | awaiting_submit_slot，batch 为 `awaiting_confirm` | → submitting（调度器 / HTTP step / MCP browser_step） | critical（FR-16） |
| I05 | generating | → submitting | critical（重复提交） |
| I06 | paused_needs_human(`restart_during_submit`) | 调度器自动 → submitting | critical（FR-19） |
| I07 | done | cancel / resume / → preparing | blocker |
| I08 | failed | `resume_job`（应改用 `reroll`，见 D09） | blocker |
| I09 | cancelled | → preparing | blocker |
| I10 | downloading | → submitting | critical |

### Scenario Outline 4.3: 取消（FR-22）

- Given job 处于 `<state>`
- When 调用 `cancel_job`
- Then 结果为 `<result>`，响应与 UI 文案 `<msg>`，Fake 站点累计点击 `<clicks>`

| ID | state | result | msg | clicks |
|---|---|---|---|---|
| X01 | queued | cancelled | 不花积分 | 0 |
| X02 | preparing（upload 进行中） | 当前 UI 动作结束后的检查点 → cancelled；不再执行 fill | 不花积分 | 0 |
| X03 | awaiting_submit_slot | cancelled | 不花积分 | 0 |
| X04 | submitting | AMB-16 | — | — |
| X05 | generating | 停止轮询；终态名称见 AMB-16 | 明确写「积分不会退还」 | 1 |
| X06 | downloading | 停止下载，目标路径下没有半写文件 | 明确写「积分不会退还」 | 1 |

### Scenario Outline 4.4: 重启恢复（FR-19）

- Given job 处于 `<state>` 时 service 进程被杀
- When service 重启
- Then job 状态为 `<after>`，Fake 站点在重启后收到的点击数 = `<clicks_after>`

| ID | state | after | clicks_after |
|---|---|---|---|
| B01 | submitting（点击前后各测一次） | paused_needs_human(`restart_during_submit`) | 0 |
| B02 | generating | generating，轮询恢复 | 0 |
| B03 | downloading | downloading，重新下载到临时文件 | 0 |
| B04 | preparing / awaiting_submit_slot | AMB-15 | 0 |

### Scenario Outline 4.5: 重试边界（FR-20/29/31）

- Given 在 `<step>` 注入 `<fault>`，连续 `<n>` 次
- Then 结果为 `<result>`，提交点击次数为 `<clicks>`

| ID | step | fault | n | result | clicks |
|---|---|---|---|---|---|
| Y01 | set_params | 读回显示值不一致 | 1 | 重试后继续，重试计数 = 1 | 按后续流程 |
| Y02 | set_params | 读回显示值不一致 | 4 | `page_contract_broken`（队列级） | 0 |
| Y03 | upload | 瞬时失败 | 3 | 第 4 次成功，继续 | 按后续流程 |
| Y04 | upload | 瞬时失败 | 4 | AMB-17 | 0 |
| Y05 | fill | 校验不一致（编辑器失焦追加文本） | 1 | 清空重填一次后通过 | 按后续流程 |
| Y06 | fill | 校验不一致 | 2 | `fill_mismatch`，**绝不提交**（与 FR-20「fill 最多 3 次」的关系见 AMB-17） | 0 |
| Y07 | submit | 点击后 Playwright 抛异常 | 1 | 零重试 → 按 T05 / T06 走对账 | 1 |
| Y08 | download | 瞬时失败 | 4 | AMB-17 | 1 |

---

## Feature 5: 暂停分级

绑定 FR-18（backend 隔离）、FR-21、FR-23、FR-36、FR-37、FR-38、FR-40、FR-56

作为用户，只有需要我到浏览器里处理的情况才停整条队列并弹 toast；单条 job 的问题不应拖住其余 job。

### Scenario Outline 5.1

- Given web 队列有 4 个已确认 job（1 个 generating、1 个 awaiting_submit_slot、2 个 queued），cli 队列有 2 个已确认出图 job
- When 在 job J1 上注入 `<fault>`
- Then 暂停级别为 `<level>`，被暂停的队列为 `<paused>`
- And J1 的状态为 `<j1>`
- And 其余 web job 的行为为 `<others_web>`，cli job 的行为为 `<cli>`
- And toast = `<toast>`，失败现场（截图 + DOM + trace）= `<forensics>`

| ID | fault（注入方式） | level | paused | j1 | others_web | cli | toast | forensics |
|---|---|---|---|---|---|---|---|---|
| Q01 | `login_expired`：Fake 站点登录失效 | 队列 | web | 停在检查点，不前进（AMB-14） | 不再推进 | 继续 | 是 | 是 |
| Q02 | `captcha_or_risk_popup`：注入验证码弹窗 | 队列 | web | 同上 | 不再推进 | 继续 | 是，附截图 | 是 |
| Q03 | `insufficient_credit`：页面提示积分不足 | 队列 | web（是否连带 cli 见 AMB-27） | 同上 | 不再推进 | 继续 | 是 | 是 |
| Q04 | `page_contract_broken`：删掉「生成」按钮 / canary 某项失败 / 解析连续失败超过阈值 | 队列 | web | 同上 | 不再推进 | 继续 | 是 | 是 |
| Q05 | `browser_lost`：关闭 context | 队列 | web | 重建 context → 检查登录 → 对账全部 generating job | 不再推进 | 继续 | 是 | 是 |
| Q06 | `cli_login_required`：fake dreamina 返回未登录 | 队列 | cli | 停在检查点 | 继续 | 不再推进；UI 提示自行运行 `dreamina login` | 是 | 是 |
| Q07 | `compliance_confirmation_required`：fake dreamina 返回 `AigcComplianceConfirmationRequired` | 队列 | cli | 同上 | 继续 | 不再推进 | 是 | 是 |
| Q08 | `moderation_reject` | 作业 | 无 | failed | 继续 | 继续 | 否 | 是 |
| Q09 | `real_face_rejected` | 作业 | 无 | AMB-13 | 继续 | 继续 | 否 | 是 |
| Q10 | `upload_rejected` | 作业 | 无 | AMB-13 | 继续 | 继续 | 否 | 是 |
| Q11 | `fill_mismatch` | 作业 | 无 | AMB-13，点击 0 | 继续 | 继续 | 否 | 是 |
| Q12 | `wait_timeout` | 作业 | 无 | paused_needs_human | 继续 | 继续 | 否 | 是 |
| Q13 | `restart_during_submit` | 作业 | 无 | paused_needs_human | 继续（重启后） | 继续 | 否 | 是 |
| Q14 | fake dreamina 非零退出码，且不属于未登录或合规确认 | AMB-27 | — | — | — | — | — | — |

### Scenario Outline 5.2: 恢复队列（FR-23）

- Given web 队列因 `<reason>` 暂停
- When 调用 `resume_queue(web)`，canary 结果为 `<canary>`
- Then 队列状态为 `<queue>`，响应为 `<resp>`

| reason | canary | queue | resp |
|---|---|---|---|
| captcha_or_risk_popup（用户已手动处理） | 通过 | 运行，queued job 继续 | ok |
| captcha_or_risk_popup（弹窗仍在） | 失败 | 保持暂停 | 返回失败项 |
| login_expired（用户未登录） | 失败 | 保持暂停 | 原因 = 登录标志缺失 |

### Scenario 5.3: toast 只是尽力而为（FR-56）

- Given toast 发送会抛异常
- When 发生 Q02
- Then 日志记录发送失败，web 队列照常进入暂停，暂停原因和截图可以通过 `/api/jobs` 查到

---

## Feature 6: 确认闸门与每日预算

绑定 FR-13、FR-14、FR-15、FR-16、FR-55

作为用户，没有我（或我明确授权的预算内自动化）的确认，任何一分积分都不应被花出去。

### Scenario Outline 6.1: token 有效性

- Given batch B 预检完成，状态为 `awaiting_confirm`，签发了 token T（30 min 过期）
- When 在 `<when>` 用 `<token>` 调用 confirm
- Then 结果为 `<result>`，batch 状态为 `<batch>`

| ID | when | token | result | batch |
|---|---|---|---|---|
| V01 | 签发后 29 min 59 s，首次使用 | T | accepted | confirmed，job 进入队列 |
| V02 | V01 之后再用一次 | T | rejected（单次有效） | 保持 confirmed，没有重复入队 |
| V03 | 签发后 30 min 01 s | T | rejected（已过期） | awaiting_confirm |
| V04 | 同时发起两个并发 confirm | T | 恰好一个 accepted | confirmed，job 只入队一份 |
| V05 | 任意 | 改过合计积分字段的 T′ | rejected（HMAC 不符） | awaiting_confirm |
| V06 | 任意 | batch A 的 token 用在 batch B 上 | rejected（内容摘要不一致） | awaiting_confirm |
| V07 | B 中有 error 条目 | T | rejected（AMB-23） | awaiting_confirm |

### Scenario Outline 6.2: confirmer × `allow_http_auto` × 预算

- Given `confirm.allow_http_auto = <allow>`，`budget.auto_confirm_daily_credits = 2000`
- And 当日已计入 auto_confirm 的预计积分为 `<spent>`，本批静态预计积分为 `<est>`
- When 通过 `<entry>` 确认
- Then 结果为 `<result>`；accepted 时入库的 `confirmer` 为 `<confirmer>`；rejected 时 `config_key` 为 `<key>`

| ID | entry | allow | spent | est | result | confirmer | key |
|---|---|---|---|---|---|---|---|
| K01 | UI 确认页（同源） | false | 0 | 900 | accepted | `ui_human` | — |
| K02 | MCP `confirm_batch(token)` | false | 0 | 900 | accepted | `mcp` | — |
| K03 | HTTP `auto_confirm=true` | false | 0 | 100 | rejected | — | `confirm.allow_http_auto` |
| K04 | HTTP `auto_confirm=true` | true | 0 | 2000 | accepted（等于上限） | `http_auto` | — |
| K05 | HTTP `auto_confirm=true` | true | 1500 | 500 | accepted | `http_auto` | — |
| K06 | HTTP `auto_confirm=true` | true | 1500 | 501 | rejected | — | `budget.auto_confirm_daily_credits` |
| K07 | HTTP `auto_confirm=true`（当日另有 8000 积分由 ui_human 确认） | true | 0 | 1000 | accepted（人工确认不计入预算） | `http_auto` | — |
| K08 | UI 确认页 | true | 2000 | 5000 | accepted（预算只约束 auto） | `ui_human` | — |
| K09 | MCP `precheck_batch` 携带 `auto_confirm: true` | true | 0 | 100 | AMB-22（至少 batch 不能被确认） | — | — |
| K10 | 非同源 bearer 客户端直接 `POST /api/batches/{id}/confirm`，携带 token，自报 `confirmer=ui_human` | false | — | 100 | AMB-21 | — | — |
| K11 | HTTP `auto_confirm=true`，K06 的次日 | true | 次日重新计 0 | 501 | accepted（「当日」怎么界定见 AMB-22） | `http_auto` | — |

### Scenario Outline 6.3: FR-16 硬不变量覆盖所有入口

- Given batch 状态为 `<batch>`
- When 通过 `<entry>` 执行 `<op>`
- Then 结果为 `<result>`，Fake 站点「生成」点击次数为 `<clicks>`

| entry | batch | op | result | clicks |
|---|---|---|---|---|
| HTTP `POST /api/jobs/{id}/steps/submit` | awaiting_confirm | submit | 业务错误，hint 含 UI 确认页 URL | 0 |
| MCP `browser_step` | awaiting_confirm | submit | `isError: true` + 确认建议 | 0 |
| HTTP `steps/preview` | awaiting_confirm | set_params → upload → fill → preview | 允许（F7），产出截图 | 0 |
| 调度器 | awaiting_confirm（token 已过期） | 自动推进 | 永不进入 submitting（是否会先跑 preparing 见 AMB-29） | 0 |
| HTTP `steps/submit` | confirmed | submit | 允许，仍受 FR-18 名额与间隔约束 | 1 |
| UI 主体页「创建」 | 未确认 | 新建主体 | 不提交表单（FR-49/55） | 0（表单提交） |

所有 `serve_static=True` 的 state-changing route 至少各有一个集成用例（development.md §1）。

---

## Feature 7: 幂等与指纹去重

绑定 FR-11.8、FR-13、FR-24、FR-44（attempt）

作为 Claude，我可能因为超时重试同一个调用。我希望重复调用不会变成重复出片；真想重抽时，我显式传 `reroll`。

### Scenario Outline 7.1

- Given 前序状态 `<prior>`
- When 发起 `<request>`
- Then 结果为 `<expected>`，新建 job 数为 `<new_jobs>`

| ID | prior | request | expected | new_jobs |
|---|---|---|---|---|
| D01 | 1 h 前 `idempotency_key=K1`、body B | K1 + B | 返回首次结果（同 `batch_id`、同逐条结果） | 0 |
| D02 | 1 h 前 K1 + B | K1 + B′（改了一个参数） | HTTP 409 / MCP `isError`，不做任何处理 | 0 |
| D03 | 25 h 前 K1 + B | K1 + B′ | key 已过期，当作新请求 | 按内容 |
| D04 | 同指纹 job 处于 generating | 无 key，同内容预检 → 确认 | 预检条目标注已有 job id；确认后返回该 job，不提交 | 0 |
| D05 | 同指纹 job 处于 paused_needs_human | 同 D04 | 返回该 job | 0 |
| D06 | 同指纹 job 为 done | 同 D04 | 返回 done job（计积分口径见 AMB-22） | 0 |
| D07 | 同指纹 job 为 failed | 同 D04 | 新 job | 1 |
| D08 | 同指纹 job 为 cancelled | 同 D04 | 新 job | 1 |
| D09 | 同指纹 job 为 done（attempt 1） | `reroll: true` | 新 job，attempt = 2 | 1 |
| D10 | attempt 2 为 done | `reroll: true` | 新 job，attempt = 3 | 1 |
| D11 | 同 prompt，但 `bg11-1.png` 被重新导出（sha256 改变） | 同 D04 | 指纹不同 → 新 job | 1 |
| D12 | 只有 `output_target` 不同 | 同 D04 | 新 job | 1 |
| D13 | 只有 `negative_prompt` 不同 | 同 D04 | 新 job | 1 |
| D14 | 同 shot，override 从 `hy3_砌炉的老人` 改为 `hy3_主角` | 同 D04 | 主体名不同 → 新 job | 1 |
| D15 | 同一镜，一次写 `时长: 22秒`、另一次写 `时长: 22s`，其余逐字节相同 | 同 D04 | prompt 字节不同 → 指纹不同 → 新 job（指纹包含 prompt 原文） | 1 |
| D16 | acceptance #6：同内容先预检确认，再预检确认一次 | 同 D04 | 返回同一个 job | 0 |

---

## Feature 8: 产物命名与候选图升格

绑定 FR-2 `[outputs]`、FR-5、FR-11.7、FR-35、FR-42、FR-43、FR-44、FR-45、NFR 沙箱

作为用户，我希望产物落在 `ai_video_management` 约定的位置，永远不覆盖已有文件；图片升格时旧图可以找回。

### Scenario Outline 8.1: 视频落点

- Given HY/hy3 shot02 的 job 完成，时间戳 ts = `20260913-181500`，`outputs.video_name = <tpl>`
- And `renders/` 目录现状为 `<existing>`
- When 下载并落盘，`count = <count>`
- Then 产物为 `<files>`，每个产物旁都有 `{产物文件名}.jimeng.json`

| ID | tpl | count | existing | files |
|---|---|---|---|---|
| O01 | 默认 `{shot}_{ts}{_i}.mp4` | 1 | 目录不存在 | 创建 `shots/shot02/renders/`，写 `shot02_20260913-181500.mp4` + `shot02_20260913-181500.mp4.jimeng.json` |
| O02 | 默认 | 3 | 空 | `shot02_20260913-181500_1.mp4`、`_2.mp4`、`_3.mp4`，各带 sidecar |
| O03 | 默认 | 1 | 已有同名 `shot02_20260913-181500.mp4` | 原文件字节不变；新产物处理方式见 AMB-25 |
| O04 | 默认 | 1 | 空；ffprobe 读出 20 s（期望 22 s） | 目标文件不存在；job 不进入 done（失败归类见 AMB-17）；下载的字节未被修改 |
| O05 | `{shot}_{ts}_jm{_i}.mp4`（config 覆盖） | 1 | 空 | `shot02_20260913-181500_jm.mp4`（FR-5：命名来自 config） |
| O06 | 默认 | 1 | 空 | sidecar 字段齐全（FR-44 全部键）；不含 `JIMENG_BRIDGE_TOKEN`；产物 sha256 等于下载字节的哈希 |

### Scenario Outline 8.2: 图片候选与升格

- Given 资产块 `c1-1`，主体目录为 `HY/hy3/2_世界观人设/characters/c1_砌炉的老人/`，`image_on_existing = <mode>`
- And fake dreamina 返回 `<n>` 张图；目标文件 `c1-1.png` 的现状为 `<existing>`
- When 候选落盘后执行 `promote(<pick>)`
- Then 结果为 `<result>`

| ID | mode | n | existing | pick | result |
|---|---|---|---|---|---|
| G01 | archive | 4 | 已存在（real：hy3 有 `c1-1.png`） | `_candidates/c1-1/20260913-181500_2.png` | 候选文件为 `_candidates/c1-1/20260913-181500_1.png` … `_4.png`；旧 `c1-1.png` 先移到 `ai_videos/_deleted/huangye_shenghuo/hy3/2_世界观人设/characters/c1_砌炉的老人/c1-1.png.{ts}.png`（按 FR-43 字面拼接，见 AMB-25），然后把 `_2` 复制为 `c1-1.png`，候选仍保留 |
| G02 | archive | 1 | 不存在（新键 `p4-1`） | `_candidates/p4-1/{ts}_1.png` | 直接复制为 `p4-1.png`，`_deleted` 下没有新增 |
| G03 | fail | 1 | 已存在 | 任一候选 | 业务错误，`config_key = outputs.image_on_existing`；没有移动或复制任何文件 |
| G04 | archive | 1 | 已存在 | `../../c2_獾/c2-1.png`，或 `_candidates` 之外的路径 | 拒绝（沙箱，`critical`） |
| G05 | — | — | 主体卡是跨集复用卡（hy2 `p2_随身装备`，只有 `.link.json`，没有路由键 prompt 块） | 对该卡做预检 | 产生 0 个请求（FR-9 + 规则 4b-B），不写 `_candidates` |

---

## Feature 9: 调度器

绑定 FR-18、FR-5、FR-27（批前 canary）、FR-33

作为用户，我希望 service 模仿我手动出片的节奏：远端同时渲染不超过 3 条，两次提交至少隔 15 s。遇到平台背压就等待，不报错；一个 backend 暂停时，另一个照常工作。

### Scenario Outline 9.1: 单次调度判定

- Given `concurrency.max_remote_rendering = <cap>`，`pacing.min_submit_interval_s = 15`
- And 当前 generating 数为 `<gen>`，距上次提交已过 `<since>`，web 队列状态为 `<queue>`
- When 一个处于 awaiting_submit_slot 的 web job 等待调度
- Then 结果为 `<result>`

| ID | cap | gen | since | queue | result |
|---|---|---|---|---|---|
| S01 | 3 | 2 | 20 s | 运行 | 立即提交 |
| S02 | 3 | 3 | 60 s | 运行 | 保持 awaiting_submit_slot |
| S03 | 3 | 2 | 14.9 s | 运行 | 等到满 15 s 才点击 |
| S04 | 3 | 2 | 15.0 s | 运行 | 提交（≥ 为合法） |
| S05 | 1 | 1 | 60 s | 运行 | 保持等待（上限来自 config） |
| S06 | 3 | 1 | 30 s，点击后页面提示「并行任务已达上限」 | 运行 | 回到 awaiting_submit_slot，不算失败（何时再次提交见 AMB-18） |
| S07 | 3 | 0 | — | 暂停（captcha） | web 不提交；cli job 照常提交与轮询 |
| S08 | 3 | 0 | — | cli 暂停（`cli_login_required`） | web job 照常提交 |

### Scenario 9.2: 时间线不变量（system，Fake 站点 + 可控时钟）

- Given 7 个已确认 web job，Fake 站点把每条渲染时长随机设在 40–200 s
- When 队列跑完
- Then 在 Fake 站点记录的时间线上，任一时刻 generating 数 ≤ 3
- And 任意相邻两次「生成」点击间隔 ≥ 15 s，且间隔里没有随机抖动成分（固定值，FR-1）
- And UI 动作时间段两两不重叠（单 BrowserActor）
- And 该 batch 第一次点击之前恰好跑过一次 canary，且 canary 期间「生成」点击数为 0
- And 名额或间隔的 scope 是全局还是按 backend，以 AMB-20 的定调为准
- And 当 awaiting_submit_slot job 已填好 composer 时，其他 job 能否进入 preparing，以 AMB-19 的定调为准

---

## Feature 10: 负向提示词策略

绑定 FR-2 `video.negative_prompt`、FR-4（schema 校验）、FR-8、FR-11.9、FR-24、FR-31、FR-44

作为用户，我要求反向提示词**永远不会**并入正向 prompt；平台有负向框就填进去，没有的话按我在 config 里选的策略处理。

### Scenario Outline 10.1

- Given `video.negative_prompt = <strategy>`，Fake 站点 `<field>` 负向输入框
- And shot `<neg>` 反向提示词围栏
- When 预检、确认并执行到 preview
- Then 预检结果为 `<precheck>`，负向框为 `<neg_box>`
- And 编辑器正向纯文本等于 prompt 原文，不含任何负向词
- And job 的 warning 为 `<warn>`，sidecar 的 `negative_prompt_sha256` 为 `<sidecar>`

| ID | strategy | field | neg | precheck | neg_box | warn | sidecar |
|---|---|---|---|---|---|---|---|
| N01 | platform_field_or_omit | 有 | 有 | ok | 填入负向文本 | 无 | sha256(负向文本) |
| N02 | platform_field_or_omit | 无 | 有 | ok | 省略 | 有：「平台无负向框，已省略」 | AMB-26 |
| N03 | omit | 有 | 有 | ok | 不填 | AMB-26 | AMB-26 |
| N04 | omit | 无 | 有 | ok | 不填 | 无 | AMB-26 |
| N05 | fail | 无 | 有 | error，`config_key = video.negative_prompt` | —（不进入确认） | — | — |
| N06 | fail | 有 | 有 | ok | 填入负向文本 | 无 | sha256(负向文本) |
| N07 | fail | 无 | 无 | AMB-26 | — | — | — |
| N08 | 任一 | 有 | 无 | ok | 留空 | 无 | null |
| N09 | platform_field_or_omit | 有 | 有；负向文本含 `字幕, 水印, 人声`（real hy3 shot02） | ok | 填入 | 无 | 正向编辑器的 mention 与文本序列不变 |
| N10 | `merge`（非法值） | — | — | config 保存被拒，错误指出字段路径 `video.negative_prompt` | — | — | — |

「平台有无负向框」在静态预检阶段从哪里得知（PageMap 探针结论，还是最近一次 canary）见 AMB-26。

---

## Traceability

| Feature | FR | 执行层 | 黄金路径行（失败 = blocker） | critical 行 |
|---|---|---|---|---|
| 1 参考项解析 | 6, 8, 10, 11.1, 30, 31 | unit（real fixture）+ system（1.4） | P01, R01–R03, F01–F03, 1.4 | R27, R28 |
| 2 主体命名 | 2, 3, 11.6, 48–50 | unit + system（2.3） | E02, E04, 2.2 | 2.3（改名或删除次数必须为 0） |
| 3 能力矩阵 | 1, 2, 11.2–11.5 | unit | C01, C15, C26 | — |
| 4 状态机 | 16, 17, 19, 20, 22, 23, 33 | unit + system | T01–T08, B01 | I04, I05, I06, I10, B01 |
| 5 暂停分级 | 18, 21, 23, 36–38, 40, 56 | system | Q02, Q08 | — |
| 6 确认闸门 | 13–16, 55 | unit + system（serve_static=True） | V01, K01, K02 | V02, V04, 6.3 全表 |
| 7 幂等 | 11.8, 13, 24 | unit + system | D01, D04, D09, D16 | D04（不得重复提交） |
| 8 产物 | 2, 5, 11.7, 35, 42–45 | system | O01, O02, G01 | G04 |
| 9 调度 | 18, 5, 27, 33 | system（可控时钟） | 9.2 | — |
| 10 负向 | 2, 4, 8, 11.9, 24, 31, 44 | unit + system | N01, N05 | — |

---

## 覆盖观察

以下各项的结果已由 spec 确定，但建议 stage-5 汇总时告知用户。

1. **默认 image 规则在真实数据上命中率低。** 仓库 382 条非旧写法的 image 项里，本机磁盘上 178 条按 FR-8 默认规则找不到文件。原因分三类：
   - **name 是主体目录，不是文件 stem**：xingji_yingjiu 共 111 条（`bg1_菌毯岩脊`、`c4_幽灵特工`），另有 duikang 的 `f80_ferrari`（目录里是 `f80_ferrari1..4.png`）、xianjian 的 `s1_bg6_…`；
   - **旧式 `{key}_{视图名}` 文件名**：hy2 的 `p3-1_树皮门板锚点.png`、`c2-1_香蕉蛞蝓锚点.png`；
   - **剧根内完全没有该文件**：xianjian 的 20 条 `角色参考图`、duikang 的 `entropy_city_*`。

   spec 说默认规则「依据全仓 271 条统计」，但照现行规则，这些剧只能靠逐项 override 才能出片。
2. **`references.overrides` 只能按 name 精确映射。** duikang 的 29 条 previz（`previz_shotNN` → 盘上 `shotNN_previz.mp4`）需要写 29 条 override，没有「模式 → 路径模板」式的 resolver 可用。
3. **`上一镜末帧` 的 19 条样本在本机都不存在。** 承接镜在上一镜出片并抽帧之前一律预检报错，见 AMB-07。

---

## Ambiguities found

下表中每一项 spec 都没有决定期望结果。「建议默认」仅供 stage-5 汇总定调参考，不是本 worker 替用户做的决定。

| ID | FR | 未决问题 | 证据 | 建议默认 / 严重度提示 |
|---|---|---|---|---|
| AMB-01 | FR-8 | FR-8 写的是「每个 `` `{name}({label})=>@` ``」（每项一对反引号）。一对反引号内含多项、用 ASCII 逗号分隔的写法算不算合法？ | duikang、xianjian、xingji 大量采用这种写法（P03/P04） | 两种写法都接受，否则这三部剧全部报错；`blocker` 级决策 |
| AMB-02 | FR-8 | 「以『反向提示词』为标题」是否包含 `> **反向提示词**（…）：` 这种引用块加粗标签？ | 295 个 shot（含验收用例 hy3 shot02）用引用块，只有 12 个用 `##` 标题 | 接受两种形态；否则验收 #1 的 negative 会被静默丢弃 |
| AMB-03 | FR-8、FR-11.3 | `时长` / `比例` 的变体怎么解析：反引号包裹、尾随全角注释、`比例: 9:16 ｜ 时长: 9秒` 同一行；`2.35:1` 是否合法？`model_limits` 没有比例列，「ratio 属于该模型支持的范围」拿什么来判断？ | F04、F06、F07、F08，均为真实数据 | 在 `model_limits` 中补 `ratios`；解析时剥掉反引号和尾随注释；无法识别 → 预检错误并指向 config 键 |
| AMB-04 | FR-8 vs §2 | FR-8 说旧写法「一律」预检错误；§2 又说「旧写法通过每剧 config 的 override 解决」。在 override 已存在时，`c4_裴昭=>@` / `=>@1` 能否解析？两种旧写法同时出现时报哪个错误码？ | 旧写法共 270 条（rexue、wushen） | 以 override 为准：有 override 就放行、无 override 就报错；这决定旧剧能否使用本服务，`blocker` 级决策 |
| AMB-05 | FR-2、FR-8 | 没有 `c{N}_` 前缀的卡目录（`characters/driver/`）算不算角色卡？`character_name` 取整个目录名吗？ | duikang shot09、shot11 | 算角色卡，`character_name` 取整个目录名，并在 propose 中标 `needs_confirmation` |
| AMB-06 | FR-8、FR-11.2 | resolver 里的「图片 / 视频 / 音频」按哪些扩展名判定（png/jpg/webp？mp4/mov？）？label 为 image 类但盘上只有同 stem 视频时（hy1 `bg9-1.mp4` 是视频版场景参考），是报 not found，还是按实际媒体类型改判 kind？ | R19 | 在 config 里加 `references.extensions.{image,video,audio}`；kind 以 label 规则为准，不改判，并在 hint 中提示「盘上有同 stem 的视频文件」 |
| AMB-07 | FR-8、FR-11.1、FR-13 | shot01 的 `上一镜末帧`（不存在 shot00）怎么处理？同一 batch 里的承接链（shot03 依赖 shot02 本批才出的末帧）是直接报错，还是延迟到上一镜 done 后再解析？末帧由谁抽取？ | 19 条 first_frame 样本在本机都不存在 | v1 静态报错，提示先完成上一镜并抽帧；同批承接链显式列为已知限制 |
| AMB-08 | FR-8、FR-10 | 带 `.link.json` 的文件，stem 取 link 文件名（`p2_随身装备.png.link.json` → `p2_随身装备`）还是 target 文件名？两者不同时以谁为准？ | hy2 的 link 目前两者恰好相同 | 以 link 文件名为准（它才是本集的「位置」），sha256 取 target 字节 |
| AMB-09 | FR-3、FR-48 | 跨集复用角色（hy2 → hy1）的期望主体名只用来源集缩写套模板（`hy1_造家的人`），还是沿用来源集 config 的 override（`hy1_主角`）？ | E05 | 沿用来源集最终解析出的名字（含 override），避免同一人得到两个名字 |
| AMB-10 | FR-3 | 「期望主体名与即梦现有主体不一致」按什么规则判定？（同缩写前缀下存在其他主体？不在快照里就算？）验收 #7 要求 hy3 必须标出冲突 | E01 | 期望名不在快照、而快照中有同 `{abbrev}_` 前缀的主体 → 标记 |
| AMB-11 | FR-2、FR-11.5、FR-11.6、FR-49 | 「≤ 20 字」「prompt_max_chars」按什么计：Unicode 码点、按字节，还是只数中文字符？空白和换行算不算？ | 仓库 K10 口径是「中文字符」 | 两者都按 Unicode 码点、含空白换行，并在 README 写明 |
| AMB-12 | FR-1、FR-11.2 | first_frame 项计不计入图片上限？主体计不计入参考上限？页面「最多 50 个参考素材」这个总上限是否要单独检查？ | C10、C14 | first_frame 计入图片；主体不计入；总上限作为 `model_limits` 的可选键 |
| AMB-13 | FR-20、FR-21 | 作业级原因的落点不统一：`moderation_reject` → failed（FR-20），`restart_during_submit` / `wait_timeout` → paused_needs_human（FR-19 / FR-1）；`real_face_rejected`、`upload_rejected`、`fill_mismatch` 进入 failed 还是 paused_needs_human？ | Q09–Q11 | 平台明确拒绝 → failed；本地校验不一致（fill_mismatch）→ paused_needs_human |
| AMB-14 | FR-18、FR-21 | 队列级暂停是队列标志，还是把每个 job 改成 paused_needs_human？暂停期间 generating job 是否继续被动轮询或对账？ | Q01–Q07 | 队列标志 + 触发 job 记 reason；generating 继续被动监听（不点击），login 失效时除外 |
| AMB-15 | FR-19、FR-23 | `resume_job` 把 paused_needs_human 恢复到哪个状态？特别是 `restart_during_submit`：人工核对历史后如何声明「已提交（给平台 id）」或「未提交」？重启时处于 preparing / awaiting_submit_slot 的 job 怎么办？ | T13、B04 | resume 必须带人工结论参数；「未提交」回 awaiting_submit_slot，并需要一次新的确认或显式标注；preparing 从 set_params 重做 |
| AMB-16 | FR-22 | 提交后取消的终态叫什么（仍是 `cancelled`？是否记录「已扣费」）？在 `submitting` 期间到达的取消怎么处理？ | X04、X05 | 终态为 `cancelled` + `credits_charged_expected: true`；submitting 期间的取消延迟到点击之后，按提交后取消处理 |
| AMB-17 | FR-20、FR-29、FR-31、FR-35 | upload / download 重试耗尽后进入什么状态？平台明确拒绝上传是否也要重试？FR-20 的「fill 最多重试 3 次」与 FR-31 的「清空重填一次」冲突；下载校验失败归为什么原因？ | Y04、Y06、Y08、O04 | fill：操作异常重试 3 次、校验不一致只重填 1 次；upload 耗尽 → `upload_rejected`；download 耗尽或校验失败 → paused_needs_human（新原因 `download_failed`） |
| AMB-18 | FR-18 vs FR-20、§2 | 点击后页面提示「并行已达上限」，job 回到 awaiting_submit_slot 后再次点击，是否违反「提交零自动重试 / 任何形式的自动重复提交」？背压是在点击前从页面状态检测，还是点击后才得知？ | T11、S06 | 只有能证明平台未建任务（有背压提示 + 无提交响应 + 历史对账无记录）时才允许再次提交；并写进 FR-20 的例外条款。`critical` 级决策 |
| AMB-19 | FR-17、FR-18、FR-31、FR-33 | 处于 awaiting_submit_slot 的 job 占着已填好的 composer，可能要等几个小时。期间其他 job 能否进入 preparing（会覆盖 composer）？点击前是否重新校验填写？ | 状态顺序 preparing → awaiting_submit_slot → submitting | 单 composer 模型下，名额可用前不进入 preparing；点击前必须重跑 FR-31 校验，不一致按 fill_mismatch 处理 |
| AMB-20 | FR-18 | `max_remote_rendering` 与 `min_submit_interval_s` 是全局生效还是按 backend 生效？CLI 出图的 generating 计不计入 3？ | S07、S08、9.2 | 两者都按 backend 生效（web 3 条、cli 单独配置），与「暂停按 backend 隔离」一致 |
| AMB-21 | FR-13、FR-14、FR-15 | precheck 会把 token 返回给调用方，非同源的 bearer 脚本可以直接调 `POST /api/batches/{id}/confirm`。这样就等于在 `allow_http_auto=false`、不受预算约束的情况下完成了自确认。`confirmer` 是调用方自报，还是服务端按入口推导？ | K10 | 服务端推导：同源 UI → `ui_human`；`/mcp` → `mcp`；其余 HTTP → 视同 `http_auto`，受开关与预算约束。建议 `critical`（确认闸门可被绕过） |
| AMB-22 | FR-12、FR-15、FR-24 | `auto_confirm` 挂在 precheck 调用上还是 confirm 调用上？MCP 传 `auto_confirm` 是拒绝还是忽略？「当日」按哪个时区？预算累计用静态估算还是页面估算？命中去重的条目（D04–D06）计不计入合计积分与预算？ | K09、K11、D06 | 挂在 `POST /api/batches` 上；MCP 拒绝并 `isError`；按本机时区；用静态估算；去重命中的条目计 0 |
| AMB-23 | FR-11、FR-13、FR-54 | batch 里只要有 error 条目，整批就不能确认，还是可以只确认 ok 条目？（「剔除 error 条目需要重新预检」暗示前者） | V07 | 整批拒绝，UI 提供「剔除错误项并重新预检」按钮 |
| AMB-24 | FR-24 | 「同 key 同内容」按 body 字节比较还是按规范化 JSON 比较？key 的作用域（按调用方或按端点）？指纹拼接的规范化（分隔符、params 键序）？ | D01、D02 | 规范化 JSON 比较；key 全局唯一；指纹用带长度前缀或 JSON 规范化序列化 |
| AMB-25 | FR-42、FR-43、FR-11.7 | `{ts}` 取预检、提交还是下载时刻？落盘时发现同名文件是报错还是追加后缀？图片 `{ts}_{i}` 在 n = 1 时是否保留 `_1`、i 从几开始？升格出的 `{key}.png` 是否也写 sidecar？归档名 `{原相对路径}.{ts}.png` 按字面会得到 `c1-1.png.{ts}.png` 这种双扩展名，是否本意？旧 sidecar 要不要一起归档？ | O03、G01 | ts 取下载完成时刻；同名追加 `_dupN` 并记 warning；i 从 1 开始且始终保留；升格文件复制 sidecar 并加 `promoted_from`；归档名去掉原扩展名；旧 sidecar 一并归档 |
| AMB-26 | FR-11.9、FR-31、FR-44 | `fail` + 平台无负向框 + 请求本身没有负向时，是否算错误？静态预检怎么知道平台有没有负向框？`omit` 策略下平台有框时，要不要记 warning？被省略的负向是否仍写 `negative_prompt_sha256`？CLI 视频（2.0）是否适用该策略？ | N02–N04、N07 | 仅当请求带负向时才报错；负向框是否存在作为 PageMap 的已验证能力位（`web_version` 绑定）；sidecar 增加 `negative_prompt_sent: bool` |
| AMB-27 | FR-21、FR-38 | CLI 的一般性非零退出码映射到哪个暂停原因（队列级还是作业级）？`insufficient_credit` 若 web 与 CLI 共用积分池（open question 7），是否要同时暂停两条队列？ | Q03、Q14 | 未知的非零退出码 → 作业级 failed（新原因 `cli_error`，保留 stderr）；积分池确认共用后，两条队列一起暂停 |
| AMB-28 | §9 验收 #1、FR-30 | 验收 #1 写「4 个参考项按 stem 上传」，但 hy3 shot02 实际是 3 个上传项 + 1 个主体 | P01、1.4 | 改写验收为「3 个上传项 + 1 个主体 mention」 |
| AMB-29 | FR-13、FR-16、F3、F7 | job 在 batch 确认之前就存在（F7 允许分步调试）。调度器是否会对未确认 batch 的 job 自动执行 preparing？ | 6.3 | 调度器只选 confirmed 的 batch；未确认的 job 只能通过手动 `browser_step` 走到 preview |
