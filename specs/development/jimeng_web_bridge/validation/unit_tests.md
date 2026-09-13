---
worker_id: level-specialist-03-unit_tests
stage: 5
role: level-specialist
level: unit_tests
status: complete
blockers: []
confidence: medium
---

# Validation · unit_tests — jimeng_web_bridge

Run `jimeng_web_bridge-20260913-093603` · 输入 `final_specs/spec.md`（FR-1..FR-56, §7, §8）。
本文件只描述单元测试（名称、位置、输入、期望、边界），不含实现代码。
confidence = medium：测试面完整，但 §11 列出的若干 spec 歧义未定之前，部分期望值无法写成确定断言。

---

## 0. 约定

### 0.1 目录、命名、运行

- 测试根 `projects/jimeng_web_bridge/tests/`，镜像源码树（development.md §6）：`tests/libs/{common,domain,application,infrastructure}/{role}/…`、`tests/api/{routes,mcp_tools}/…`。
- 文件名 `test_{源文件 stem}.py`。例：`libs/domain/entities/generation_job__entity.py` → `tests/libs/domain/entities/test_generation_job__entity.py`。
- 测试 ID `UT-{层}-{聚合}-{NN}`。层码：`C` common · `D` domain · `R` infra readers · `W` infra writers/clients · `MW` middleware · `A` application · `MCP` MCP tools · `S` 静态/架构。stage-6 validator 按 ID 回报。
- `make test` 在 `.venv` 中执行 `python -m pytest`，依赖用 pip 安装，Makefile 里不得出现 `uv`（validation/development.md §6）。
- 共享 fake 放在 `tests/fakes/`（不镜像源码，只供测试）：
  - `ManualClock`；
  - `FakeGenerationBackend`：实现 `GenerationBackend` 端口，记录有序调用，结果可脚本化（ok / parallel_limit / moderation_reject / captcha / raise_after_click）；
  - `FakeBrowserActor`：断言 UI 动作从不重叠；
  - `FakeSessionProbe`、`FakeToastClient`、`FakeEntitySnapshotStore`。

### 0.2 分层纪律

- **domain**：无 I/O、无框架。时钟、HMAC key、文件事实（exists / sha256）全部作为参数注入。
- **application**：用 `container.{provider}.override(...)` 注入 fake，不 monkeypatch import。FR-19 这类以持久化顺序为核心的用例改用 `tmp_path` 下的真 SQLite。
- **infrastructure**：碰真实边界，不 mock 边界本身：
  - 真文件系统（`tmp_path` 或只读真实仓库树）；
  - 真 SQLite；
  - 真子进程（fake `dreamina`）；
  - Playwright 打开本地 fake 站点 HTML。

### 0.3 pytest markers（在 `pyproject.toml` 注册，开 `--strict-markers`）

| marker | 运行条件 | skip reason |
|---|---|---|
| `real_repo` | 仓库根存在 `ai_videos/` md 树 | `ai_videos tree absent` |
| `real_media` | 用例需要的 png / mp4 已从 R2 拉到本地（media 被 gitignore） | `media not pulled: python tools/assets_sync.py pull` |
| `probe_fixture` | stage-6 只读探针捕获的 fixture 已存在 | `awaiting stage-6 probe capture` |
| `win_only` / `posix_only` | 按 `sys.platform` | 见 §10 |
| `needs_symlink` | 运行时探测到 `os.symlink` 可用（Windows 需 Developer Mode） | `symlink creation not permitted` |
| `needs_ffprobe` | `ffprobe` 在 PATH 上 | `ffprobe not on PATH` |
| `browser` | Playwright chromium 已安装 | `playwright browsers not installed` |

**skip 不得变成静默通过**（general.md 原则 3）。stage-6 sign-off 时设置 `JWB_REQUIRE_PROBE=1`、`JWB_REQUIRE_FFPROBE=1`、`JWB_REQUIRE_REAL_REPO=1`，对应 marker 从 skip 改为 fail。conftest 自身要有一条测试验证这个开关确实生效（`UT-S-MARK-01`）。

---

## 1. 真实上游样本基线（2026-09-13 全仓实测，排除 `_deleted/`）

reader 测试的边界用例全部取自这张表，**不另写手工 fixture 模拟这些变体**（validation/development.md §10）。

| # | 实测事实 | 数量 / 位置 | 对测试的含义 |
|---|---|---|---|
| F1 | shot md 共 271 个，每个恰有 1 行 `参考:` | 全仓 | 与 spec「271 条」一致；可作为 sweep 的不变量 |
| F2 | 视频 prompt 首个 fence 里，`=>@` 从不出现在 `参考:` 行以外 | 271/271 | 不变量：`=>@` 个数 = ReferenceItem 个数 |
| F3 | 参考项分隔有两种：整行一个反引号 span、内部用 `, `；每项各自带反引号、项间用全角 `，` | 358 / 200 处 | 两种都要解析 |
| F4 | 旧写法 `=>@N`（已填槽位号） | wushen_juexing 11 个、rexue_gaoxiao 20 个（如 `学校泳池_bg2_水面_俯拍=>@1`，同时无括号） | 预检错误 |
| F5 | 旧写法 `名字=>`（无 `@`，也无括号） | wushen_juexing 60 个（`裴昭=>, 裴知秋=>`） | spec 未列出这种形态，见 A-13 |
| F6 | 无括号的 `名字=>@` | wushen（`c15_青衣女天骄=>@`、`c11_围观武者甲声音=>@3`） | 预检错误 |
| F7 | label 形如 `(…声音)` | **0 处** | 默认规则 `*声音` 在真实数据中零命中 |
| F8 | 默认规则覆盖不到的 label | `道具参考图`（xianjian 5、xingji 3）、`道家手印参考图`、`大地裂痕参考图` | 预检错误：label 未命中任何 rule |
| F9 | 带段落后缀的 label，含嵌套全角括号 | `场景参考图·第四段：根盘与坑全景（N1 机位）` 等约 35 处（hy1–hy3） | 名与 label 按 ASCII 括号切分，全角括号属于 label 内容 |
| F10 | `本镜首帧(上一镜末帧)` | xingji 17、rexue 3、duikang 2；上一镜 `_lastframe.png` 目前只存在于 wushen（而 wushen 不用这个 label） | xingji shot02 解析结果必为「找不到文件」 |
| F11 | `stem_in_shot` 的目标文件不在镜目录顶层 | xianjian `shot02_previz` 在 `shots/shot02/previz/shot02_previz.mp4` | 需要递归查找，见 A-11 |
| F12 | 参考项名与文件 stem 对不上 | duikang 写 `previz_shot01(previz灰模视频)`，实际文件是 `shot01_previz.mp4` | 默认规则 miss → 错误信息里提示 override 键 |
| F13 | `时长:` 的写法 | `N秒`（多数）；`Ns`（xianjian shot14–16）；反引号小数 `` `1.5s` ``（rexue 21 个）；`比例: 9:16 ｜ 时长: 9秒` 两字段同一行（wushen ep03 shot05 / shot07） | 全部要能解析 |
| F14 | `比例:` 的写法 | `16:9`、`9:16`、`` `9:16` ``（rexue）、`16:9（项目 divergence·style_guide 画幅节）`（尾注）、`2.35:1`（duikang 21 个） | `2.35:1` 在预检报「模型不支持的比例」 |
| F15 | prompt 标题 | `## 视频 prompt`；`## 视频 prompt — 复制下方代码块到视频生成模型`（rexue 21 个） | 标题按前缀匹配 |
| F16 | 反向提示词标题有 4 种形态，其中一种与 fence 之间隔着空行；另有 128 个文件没有负向 fence（`负面词:` 写在 prompt 内：wushen 102、rexue 21、xianjian 5） | 见 §3.1 | 无负向 fence → `negative_prompt=None`；prompt 内的 `负面词:` 逐字保留 |
| F17 | prompt 正文里出现不属于 `=>@` 的裸 `@` | wushen 60（`参考分配: @图1…`）、xianjian 19（`@图片1`）、duikang 15（`@f80_ferrari`） | 影响 FR-31 填写与校验，见 A-14 |
| F18 | 行尾与编码 | CRLF 0 个、BOM 0 个；但 `core.autocrlf=true` 且仓库没有 `.gitattributes` | 新 clone 可能引入 CRLF，见 A-07 |
| F19 | 资产卡 ```text fence 的首行 | 291 个卡 md：路由键形态 `x{N}-{M}_` 158 个；旧形态 `x{N}_` 95 个；其他（负面词清单、中文场景名）224 个 | 只取路由键形态 |
| F20 | hy3 `c1_砌炉的老人.md` | `c1-1_…立绘`（图）+ `c1-2_…turntable`（4 s 视频块，块内带 `参考:` 行）+ 2 个裸 fence | 见 A-15 |
| F21 | `.link.json` | hy2 `c1_造家的人` 同时有 `.png.link.json` 和 `.mp4.link.json`（stem 相同、种类不同），target 在 hy1 | 图片 resolver 只认 png 那条 |
| F22 | 同一剧内的重复图片 stem | wushen 21 个（`shot10_lastframe` 跨集 ×3）、xianjian 4 个（`views1` ×10）；hy1–hy4、duikang、rexue、xingji 为 0 | 多重匹配错误可以用真实树测试 |
| F23 | `series.json` | 只有 `huangye_shenghuo` 有；`ai_videos/notes/`（只含 note.txt）是非 `_` 目录且无标记 | 按参考语义会被当成平铺剧，见 A-23 |
| F24 | `dreamina` 可执行文件 | 实际为 `~/bin/dreamina.exe`（原生 exe，31 MB）；spec 默认值写的是 `~/bin/dreamina` | 见 A-22 |

---

## 2. Domain（`tests/libs/domain/`）

### 2.1 `JobEntity` 状态机 — `entities/test_generation_job__entity.py`

**黄金转移表。** 9 个状态两两组合共 81 对，全部参数化。断言「允许集合」与下表**逐项相等**：多出或缺少一条边都算失败。

| 边 | from → to | 前置条件 / 负载 | 依据 |
|---|---|---|---|
| E1 | queued → preparing | — | FR-17 |
| E2 | preparing → awaiting_submit_slot | 子步骤 `preview` 已完成 | FR-17, FR-32 |
| E3 | awaiting_submit_slot → submitting | 必须带 `ConfirmedBatchProof`（batch_id + confirmed_at） | FR-16, FR-33 |
| E4 | submitting → generating | 必须带 `platform_task_id` | FR-33 |
| E5 | generating → downloading | — | FR-17 |
| E6 | downloading → done | 必须带 `output{sha256,size}` | FR-35 |
| E7 | submitting → awaiting_submit_slot | 原因 `parallel_limit`；不计失败，重试计数不变 | FR-18 |
| E8 | queued / preparing / awaiting_submit_slot → cancelled | `credits_spent=false` | FR-22 |
| E9 | generating / downloading → cancelled | `credits_spent=true`（「积分不会退还」）——**终态名待定 A-03** | FR-22 |
| E10 | preparing / awaiting_submit_slot / submitting / generating / downloading → paused_needs_human | 必须带 `PauseReason` | FR-21 |
| E11 | preparing / generating → failed | 必须带失败原因 | FR-20, FR-21 |
| E12 | paused_needs_human → {按暂停来源决定} | **待定 A-03**，只断言下面的禁止项 | FR-23 |

**无论 A-03 怎么定，都必须成立的确定性断言：**

| ID | 测试名 | 输入 | 期望 |
|---|---|---|---|
| UT-D-JOB-01 | `test_transition_matrix_matches_golden_table` | 81 对 (from, to) | 允许集合 = 黄金表 |
| UT-D-JOB-02 | `test_submitting_only_from_awaiting_submit_slot` | 除 awaiting_submit_slot 外的每个状态调用 `begin_submit` | 抛 `JobTransitionError`（具名领域错误，不是 ValueError），状态与转移日志都不变 |
| UT-D-JOB-03 | `test_begin_submit_requires_confirmation_proof` | 在 awaiting_submit_slot 上调用 `begin_submit(proof=None)` | 抛 `UnconfirmedBatchError` |
| UT-D-JOB-04 | `test_restart_during_submit_never_reaches_submitting` | paused(restart_during_submit) 后依次尝试 resume → begin_submit | 永不进入 submitting / awaiting_submit_slot |
| UT-D-JOB-05 | `test_terminal_states_have_no_outgoing_edges` | done / failed / cancelled → 任意状态 | 抛错 |
| UT-D-JOB-06 | `test_transition_log_appends_from_to_at_reason` | 走完 E1–E6 全链；时钟用 ManualClock | 日志 6 条，`{from,to,at,reason?}`，`at` 单调不减，reason 可为 None |
| UT-D-JOB-07 | `test_illegal_transition_does_not_append_log` | 任一非法边 | 日志长度不变 |
| UT-D-JOB-08 | `test_pause_requires_pause_reason_and_fail_requires_reason` | `pause(None)`、`fail(None)` | 抛错 |
| UT-D-JOB-09 | `test_self_transition_rejected` | x → x | 抛错（子步骤进度更新不算转移） |
| UT-D-JOB-10 | `test_preparing_substeps_in_order` | 按 set_params → upload → fill → preview 推进；跳过 upload 直接 fill；preview 未完成就走 E2 | 顺序推进通过；其余两种抛 `SubstepOrderError` |
| UT-D-JOB-11 | `test_substep_progress_bounds` | 进度 -1、0、100、101 | 0 与 100 合法，-1 与 101 抛错 |
| UT-D-JOB-12 | `test_retry_budget_per_substep_is_three` | `set_params` / `upload` / `fill` / `download` 各失败 1..4 次 | 第 1–3 次允许重试，第 4 次返回 `RetryBudgetExhausted`（之后进 paused 还是 failed 见 A-03） |
| UT-D-JOB-13 | `test_submit_has_zero_retry_budget` | 提交失败后请求重试 | 抛 `SubmitRetryForbiddenError` |
| UT-D-JOB-14 | `test_parallel_limit_is_not_failure` | 走 E7 | `failure_count` 不变；重试计数不变；日志 reason=`parallel_limit` |
| UT-D-JOB-15 | `test_reroll_creates_new_attempt_not_transition` | 对 done 的 job 发起 reroll | 原 job 不变；新 job 的 `attempt = 原 attempt + 1`，指纹相同 |
| UT-D-JOB-16 | `test_cancel_pre_submit_marks_no_credit_spent` | 分别在 E8 的三个起点取消 | `credits_spent=false` |
| UT-D-JOB-17 | `test_cancel_post_submit_flags_non_refundable` | 从 generating 取消 | `credits_spent=true`，DTO 必然带「积分不会退还」标记 |
| UT-D-JOB-18 | `test_cancel_during_submitting_is_deferred` | 在 submitting 上取消 | 记为 `cancel_requested`；到达 generating 后按 E9 执行（**待定 A-03**） |

### 2.2 `BatchEntity` — `entities/test_batch__entity.py`

| ID | 测试名 | 输入 | 期望 / 边界 |
|---|---|---|---|
| UT-D-BAT-01 | `test_new_batch_is_awaiting_confirm` | precheck 结果 | `awaiting_confirm`；`content_digest` 与内容是确定性对应 |
| UT-D-BAT-02 | `test_confirm_rejected_when_any_item_has_error` | 含 1 条 error 的 batch | 抛 `BatchHasErrorsError` |
| UT-D-BAT-03 | `test_items_are_immutable_after_precheck` | 尝试删除 error 条目 | 没有这种变更方法；只能重新预检（FR-13） |
| UT-D-BAT-04 | `test_confirm_records_confirmer_and_time` | 以 `ui_human` / `mcp` / `http_auto` 各确认一次 | 三者都入实体；非法值（如 `admin`）抛错 |
| UT-D-BAT-05 | `test_confirm_twice_rejected` | 同一 batch 第二次 confirm | 抛 `BatchAlreadyConfirmedError`（实体侧单次；存储侧 CAS 见 UT-W-DB-05） |
| UT-D-BAT-06 | `test_digest_changes_with_any_item_field` | 分别改 prompt 1 个字节、改 1 个参考 sha、改一个 params 字段、调换两条 item 的顺序 | digest 每次都变 |
| UT-D-BAT-07 | `test_balance_start_end_recorded_once` | 两次写入 start 余额 | 第二次抛错（FR-46） |

### 2.3 `Fingerprint` — `value_objects/test_fingerprint__valueobject.py`

规范化编码未定（A-06）。以下断言不依赖它的具体形式：

| ID | 输入 | 期望 |
|---|---|---|
| UT-D-FP-01 | 两个字段完全相同的请求 | 指纹相等（跨进程稳定：同一输入的十六进制值写死在测试里作为 golden） |
| UT-D-FP-02 | prompt 只差 1 个尾随空格 / 全角 `，` 换成半角 `,` / 一个 U+3000 | 各自与原请求指纹不同（prompt 逐字节，**不做空白规范化**） |
| UT-D-FP-03 | 两个参考项调换顺序 | 不同（mention 顺序有意义） |
| UT-D-FP-04 | 同一字符串分别作为「文件项 sha256」和「主体名」 | 不同（类型需要带标签） |
| UT-D-FP-05 | 边界注入：prompt=`"a"` + 参考=`"bc"`，对比 prompt=`"ab"` + 参考=`"c"` | 不同（编码必须结构化或带长度前缀） |
| UT-D-FP-06 | params 字典的键顺序不同，值相同 | 相等 |
| UT-D-FP-07 | `negative_prompt=None` 与 `""` | 断言二者一致（待 A-06 确认，建议把 `""` 规范化为 None） |
| UT-D-FP-08 | 同内容文件、不同路径 | 相等（spec 只签入 sha256） |
| UT-D-FP-09 | 同一个镜、不同时间戳落盘 | 相等——前提是 `output_target` 取目录粒度（A-06） |
| UT-D-FP-10 | 大小 1 MB 的 prompt | 不抛错，耗时 < 50 ms（只做 smoke，不作性能断言） |

### 2.4 `ConfirmationToken` — `value_objects/test_confirmation_token__valueobject.py`

key 由参数注入，固定测试 key，时钟用 ManualClock。

| ID | 测试名 | 输入 | 期望 |
|---|---|---|---|
| UT-D-TOK-01 | `test_sign_verify_roundtrip` | digest D、credits C、exp = now + 30min | 验证通过 |
| UT-D-TOK-02 | `test_tamper_each_segment_rejected` | 分别翻转 payload、签名、分隔符中的 1 个字符 | 全部拒绝，错误码 `TOKEN_INVALID` |
| UT-D-TOK-03 | `test_digest_mismatch_rejected` | 用 D 签发，拿 D' 验证 | `TOKEN_DIGEST_MISMATCH` |
| UT-D-TOK-04 | `test_credits_mismatch_rejected` | 用 C 签发，拿 C+1 验证 | 拒绝 |
| UT-D-TOK-05 | `test_expiry_boundary` | now = exp−1s、exp、exp+1s | 通过、**待定（A-21 建议 exp 当刻即拒绝）**、拒绝 |
| UT-D-TOK-06 | `test_wrong_key_rejected` | 用 key K 签发，拿 K' 验证 | 拒绝 |
| UT-D-TOK-07 | `test_token_has_no_secret_material` | 解析出 token 文本 | 不含 key、不含 `JIMENG_BRIDGE_TOKEN` 的值 |
| UT-D-TOK-08 | `test_ttl_comes_from_injected_value` | ttl 分别为 1 min / 30 min | exp 随之变化（与 FR-5 / A-08 联动） |
| UT-D-TOK-09 | `test_single_use_is_not_a_token_property` | 同一个 token 验证两次 | 两次都通过——单次有效由服务端存储强制，见 UT-W-DB-05 / UT-A-BAT-12 |

### 2.5 静态预检纯函数 — `value_objects/test_precheck__valueobject.py`

输入是 `GenerationRequest` + 注入的「事实」（参考文件是否存在 / 可读 / sha256、输出目录是否可写 / 目标是否存在、主体快照及其同步时间、指纹命中情况、平台负向框能力、ModelLimits、DramaConfig）。函数本身不做 I/O（A-16）。每个 check 至少覆盖 ok / warning / error 各一，并断言 error 带 `config_key` 或 `hint`。

| ID | FR-11 检查 | 用例 → 期望 |
|---|---|---|
| UT-D-PRE-01 | ① 参考文件 | 存在 → ok；不存在 → error `REF_FILE_NOT_FOUND` 且 `config_key=references.overrides."{name}"`；不可读 → error |
| UT-D-PRE-02 | ② 种类 / 数量 | seedance2.5：图片 30 张 ok、31 张 error；视频 10 ok / 11 error；音频 10 ok / 11 error。`first_frame` 与主体是否计入图片上限待定（A-13） |
| UT-D-PRE-03 | ③ 时长 | seedance2.5：3 error、4 ok、30 ok、31 error；seedance2.0：15 ok、16 error；真实值 `1.5s`（rexue）→ error |
| UT-D-PRE-04 | ③ 分辨率 | seedance2.5 + `1080p` → error；seedance2.0_vip + `1080p` → ok；seedream5.0 + `1k` → error；seedream3.x + `1k` → ok |
| UT-D-PRE-05 | ③ 比例 | `16:9`、`9:16` → ok；`2.35:1`（duikang 真实值）→ error |
| UT-D-PRE-06 | ④ backend 能力 | `routing.video=cli` 时：带主体 → error；模型为 2.5 → error；时长 16 s → error；seedance2.0 + 15 s + 无主体 → ok。断言 error 结果里的 `params` **与输入完全相同**（不降级） |
| UT-D-PRE-07 | ⑤ prompt 字数 | 5000 ok、5001 error；计数单位待定（A-17），测试用例同时包含 CJK 字符与 emoji（代理对） |
| UT-D-PRE-08 | ⑥ 主体 | 名称 20 字 ok、21 字 error；不在快照里 → error，hint 指向主体对账页；快照 23h59m → ok、24h01m → warning；从未同步 → error（A-27） |
| UT-D-PRE-09 | ⑦ 输出 | 目录不可写 → error；目标已存在 → error；目录在沙箱外 → error |
| UT-D-PRE-10 | ⑧ 指纹命中 | 命中非终态或 done 的 job → 结果带 `existing_job_id`，严重度 warning（A-27）；请求带 `reroll=true` → 不标注 |
| UT-D-PRE-11 | ⑨ 负向策略 | `fail` + 平台无负向框 → error；`platform_field_or_omit` + 无负向框 → warning；`omit` → ok 且 `negative_prompt` 不下发 |
| UT-D-PRE-12 | 缩写 | 独立剧 `drama.abbrev=""` + 请求里有主体 → error，`config_key=drama.abbrev` |
| UT-D-PRE-13 | 聚合 | 任一 error → 条目为 error、不可确认；只有 warning → warning；全部 ok → ok |
| UT-D-PRE-14 | 纯函数性质 | 同一输入调用两次 | 结果相等；函数模块不 import `os` / `pathlib` / `sqlite3`（静态断言） |

### 2.6 `ModelLimits` — `value_objects/test_model_limits__valueobject.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-D-ML-01 | 解析 FR-1 表中的全部模型键 | 能力矩阵逐格等于 spec 表；`as_of=2026-09-13` |
| UT-D-ML-02 | `seedance2.0_vip` 的主体能力 | web 支持、cli 不支持 |
| UT-D-ML-03 | seedream `image2image` 参考张数 | 0 张 → error；1 与 10 张 → ok；11 张 → error。text2image 必须 0 张 |
| UT-D-ML-04 | 查询未知模型键 | 抛 `UnknownModelError` |
| UT-D-ML-05 | min > max、缺 `as_of`、backend 取值非 web/cli | 构造时抛错 |

### 2.7 配置 schema 校验 = FR-5 契约表 — `value_objects/test_global_config__valueobject.py`、`test_drama_config__valueobject.py`

**每一行都是一条参数化测试**：合法样例通过；每个非法样例都被拒绝，并且错误里带**精确字段路径**。两个 meta 测试把这张表与 schema 绑定：

- `UT-D-CFG-META-01`：schema 内省出的叶子键集合 = 本表键集合（双向）。
- `UT-D-CFG-META-02`：未知键（如 `server.token`）→ 拒绝，并给出路径。严格模式是建议值，见 A-08。

**GlobalConfig（FR-1）**

| 键 | FR | 合法 | 非法 → 错误路径 |
|---|---|---|---|
| `server.host` | FR-1、NFR 安全 | `127.0.0.1`、`localhost` | `0.0.0.0`、`::1`、`192.168.1.5` → `server.host` |
| `server.port` | FR-1 | `8790` | `0`、`70000`、`"8790"` → `server.port` |
| `routing.video` | FR-1、FR-11④ | `web`、`cli` | `api` |
| `routing.image` | FR-1、§2 | `cli` | `api`；`web` 待定（A-10） |
| `concurrency.max_remote_rendering` | FR-18 | `1`、`3` | `0`、`-1`、`1.5` |
| `pacing.min_submit_interval_s` | FR-18 | `0`、`15` | `-1`、`"15s"` |
| `wait.timeout_h` | FR-1、FR-17 | `12` | `0`、`-1` |
| `confirm.allow_http_auto` | FR-15 | `false`、`true` | `"false"`、`0` |
| `budget.auto_confirm_daily_credits` | FR-15 | `0`、`2000` | `-1`、`1.5` |
| `browser.channel` | FR-25 | `chrome`、`chromium` | `msedge`、`firefox` |
| `browser.profile_dir` | FR-25、NFR 沙箱 | `projects/jimeng_web_bridge/.data/chrome_profile` | 指向 `ai_videos/…`、含 `..`。`.env` 里的 `JIMENG_BRIDGE_PROFILE_DIR` 允许写绝对路径 |
| `browser.start_url` | FR-1 | `https://jimeng.jianying.com/ai-tool/generate?type=video&workspace=…` | `http://…`、`https://evil.com/…` |
| `canary.interval_min` | FR-27 | `30` | `0`、`-5` |
| `cli.path` | FR-38 | `~/bin/dreamina` | `""`；`.cmd` / `.bat` 待定（A-22） |
| `cli.min_version` | FR-41 | `1.4.5` | `1.4`、`v1.4.5`、`latest` |
| `notifications.toast` | FR-56 | `true` | `"yes"` |
| `model_limits.{model}.*` + `as_of` | FR-1、FR-11 | spec 表 | 见 UT-D-ML-05 |
| `price_table.*` + `as_of` | FR-12 | **结构未定（A-09）** | 负价格、缺 `as_of` |
| `.env`：`JIMENG_BRIDGE_TOKEN` | NFR 安全 | 非空 | 未设置时的行为待定（A-01）；出现在 `global.toml` 里 → 按未知键拒绝 |

**DramaConfig（FR-2）**

| 键 | FR | 合法 | 非法 → 错误路径 |
|---|---|---|---|
| `drama.abbrev` | FR-2、FR-3 | `hy3`；`""`（schema 合法，由预检报错） | 字符集与长度约束未定，建议 `[A-Za-z0-9_]{1,10}` |
| `entities.name_template` | FR-2、FR-48 | `{abbrev}_{character_name}` | `{abbrev}_{unknown}` → 未知占位符；`""` |
| `entities.overrides` | FR-2 | `{"c1_砌炉的老人"="hy3_主角"}` | 值为空；值超过 `precheck.entity_name_max_chars`（跨字段校验）；键不是 `c{N}_…` 形式 |
| `entities.source_images` | FR-49 | `["{card_dir}/*-1.png"]` | `[]`、含 `..`、绝对路径 |
| `entities.description_from` | FR-49 | 默认值（锁定描述符） | 枚举未定（A-08） |
| `references.rules[]` | FR-8 | spec 默认 5 条 | `kind=gif`；`resolver=unknown`；kind 与 resolver 不兼容（`entity` + `stem_in_shot`）；`label_glob=""` |
| `references.overrides` | FR-8 | `"x"="ai_videos/…/f.png"`、`"砌炉的老人"="entity:hy3_主角"` | 沙箱外路径、`..`、`C:\…`、`entity:` 后为空 |
| `references.search_exclude` | FR-2 | spec 默认列表 | 非列表；元素含 `..` |
| `video.model` | FR-2、FR-11 | `seedance2.5` | `seedance3`；填了图片模型 |
| `video.resolution` | FR-2 | `720p` | `8k`（未知取值）。已知但不被模型支持的组合由预检报错 |
| `video.count` | FR-2、FR-42 | `1`、`3` | `0`、`-1`、`1.5`（上限未定） |
| `video.reference_mode` | FR-2、§2 | `全能参考` | `首尾帧`、`智能多帧` |
| `video.ratio_source` / `duration_source` | FR-2 | `shot` | 其余取值未定（A-08） |
| `video.negative_prompt` | FR-2、FR-31 | `platform_field_or_omit`、`omit`、`fail` | `merge`、`append` |
| `image.model` | FR-2 | `5.0` | 与 `model_limits` 键名 `seedream5.0` 不一致（A-10） |
| `image.resolution` | FR-2 | `2k`、`4k` | `8k` |
| `image.command` | FR-2、FR-9 | `auto`、`text2image`、`image2image` | `img2img` |
| `image.ratio.{characters,scenes,props}` 及逐块覆盖 | FR-2 | `3:4`、`16:9`、`1:1` | `3x4`、`0:1` |
| `outputs.video_name` | FR-2、FR-42 | `{shot}_{ts}{_i}.mp4` | 缺 `{ts}`；含路径分隔符或 `..`；扩展名不是 `.mp4` |
| `outputs.image_candidates_dir` | FR-2、FR-43 | `_candidates/{key}` | 缺 `{key}`、`../x`、绝对路径 |
| `outputs.image_on_existing` | FR-2、FR-43 | `archive`、`fail` | `overwrite` |
| `precheck.prompt_max_chars` | FR-2、FR-11⑤ | `5000` | `0`、`-1` |
| `precheck.entity_name_max_chars` | FR-2、FR-11⑥、FR-49 | `20` | `0` |
| `precheck.estimate_deviation_warn_pct` | FR-2、FR-12 | `20` | `-1`、`"20%"` |

### 2.8 暂停原因分类 — `tests/libs/common/test_enums.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-C-ENUM-01 | 队列级 7 个原因：`login_expired`、`captcha_or_risk_popup`、`insufficient_credit`、`page_contract_broken`、`browser_lost`、`cli_login_required`、`compliance_confirmation_required` | `scope(reason)=queue` |
| UT-C-ENUM-02 | 作业级 6 个原因：`moderation_reject`、`real_face_rejected`、`upload_rejected`、`fill_mismatch`、`wait_timeout`、`restart_during_submit` | `scope(reason)=job` |
| UT-C-ENUM-03 | 穷尽性 | 枚举每个成员被分类恰好一次；新增成员而不分类 → 测试失败 |
| UT-C-ENUM-04 | 目标状态（failed 还是 paused） | spec 已明确的：`moderation_reject → failed`（FR-20）；`wait_timeout`、`restart_during_submit → paused_needs_human`（FR-1、FR-19）。`real_face_rejected`、`upload_rejected`、`fill_mismatch` **待定 A-03** |
| UT-C-ENUM-05 | backend 归属 | `cli_login_required`、`compliance_confirmation_required` 只暂停 cli 队列；另外 5 个队列级原因只暂停 web 队列 |

### 2.9 命名模板 — `value_objects/test_drama_config__valueobject.py`（命名段）

| ID | 输入 | 期望 |
|---|---|---|
| UT-D-NAME-01 | 卡目录 `c1_砌炉的老人`、abbrev `hy3` | `hy3_砌炉的老人` |
| UT-D-NAME-02 | 卡目录 `c12_围观武者乙` | 去掉多位数前缀 → `围观武者乙` |
| UT-D-NAME-03 | 目录名没有 `c{N}_` 前缀（`裴知秋`） | 抛 `CharacterDirNameError` |
| UT-D-NAME-04 | 同时存在 override `c1_砌炉的老人=hy3_主角` | override 优先 → `hy3_主角` |
| UT-D-NAME-05 | 跨集来源：hy2 的卡通过 `.link.json` 指向 hy1 | `hy1_造家的人`（来源缩写取法见 A-05） |
| UT-D-NAME-06 | 生成后的名字 21 字 | 预检 error（UT-D-PRE-08） |
| UT-D-NAME-07 | `video_name`：count=1、ts=`20260913-181500`、shot=`shot02` | `shot02_20260913-181500.mp4` |
| UT-D-NAME-08 | count=3 | `…_1.mp4`、`…_2.mp4`、`…_3.mp4` |
| UT-D-NAME-09 | 候选图 `{ts}_{i}.png` | i 从 1 开始（待定 A-19） |
| UT-D-NAME-10 | 归档路径 | `ai_videos/_deleted/{原相对路径}.{ts}.png` 的精确形态待定（A-19） |
| UT-D-NAME-11 | ts 格式与时区 | 由注入的 Clock + 时区决定（A-18） |

---

## 3. Infrastructure readers（`tests/libs/infrastructure/readers/`）

### 3.1 `ShotPromptReader` — `test_shot_prompt__reader.py`

**Golden 机制。** 每个真实副本配一个 `{name}.expected.json`，内容是：

- `prompt_sha256`、`prompt_first_line`、`prompt_codepoints`；
- `references[{name,label}]` 或 `errors[{code,config_key}]`；
- `ratio`、`duration_s`、`negative_prompt_sha256 | null`。

golden 由 stage-6 实施者**逐字段对照 md 人工核对**后提交，不允许「让被测 parser 生成然后直接接受」。错误码名称是建议值，定名后同步。

**真实副本（`tests/fixtures/real_shots/`，文件名 `{drama}__{path_flat}.md`）**

| # | 源文件（`ai_videos/` 下） | 覆盖的变体 |
|---|---|---|
| S1 | `huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md` | 标准形态；每项独立反引号 + `，`；`(Seedance 人物 entity)`；`22秒`；huangye 式反向标题；验收 #1 |
| S2 | `huangye_shenghuo/hy2/…/shots/shot01/shot01.md` | label `场景参考图·第二、三段：步道纵深全景`；`p1_砍刀(砍刀锚点)` 经 `.link.json` 解析；主体 `造家的人` |
| S3 | `huangye_shenghuo/hy2/…/shots/shot02/shot02.md` | label 内嵌全角括号 `（N1 机位）` |
| S4 | `xianjian_yi_mv/…/shots/shot02/shot02.md` | 整行一个反引号 span + `, `；`3D预演视频` 在 `previz/` 子目录；比例带尾注；反向标题与 fence 之间有空行 |
| S5 | `xianjian_yi_mv/…/shots/shot01/shot01.md` | 正文裸 `@图片1` |
| S6 | `xianjian_yi_mv/…/shots/shot03/shot03.md` | `道具参考图` 未命中规则 |
| S7 | `xianjian_yi_mv/…/shots/shot14/shot14.md` | `时长: Ns` |
| S8 | `xianjian_yi_mv/…/shots/shot17/shot17.md` | 反向标题 `反向提示词（粘平台「…` |
| S9 | `xianjian_yi_mv/…/shots/shot23/shot23.md` | 无负向 fence（`负面词:` 在 prompt 内） |
| S10 | `wushen_juexing/…/episodes/ep01/shots/shot03/shot03.md` | `裴昭=>`（无 @、无括号）；`参考分配: @图1`；首行 `01集03镜视`；`9:16`；`15秒` |
| S11 | `wushen_juexing/…/episodes/ep06/shots/shot01/shot01.md` | `=>@1..N`；`c11_围观武者甲声音=>@3` |
| S12 | `wushen_juexing/…/episodes/ep03/shots/shot05/shot05.md` | `比例: 9:16 ｜ 时长: 9秒` 同一行；`> ⚠ 合规改写` 引用块 |
| S13 | `rexue_gaoxiao/…/shots/shot01/shot01.md` | 标题 `## 视频 prompt — 复制…`；`学校泳池_bg2_水面_俯拍=>@1`；`` `9:16` ``；`` `1.5s` `` |
| S14 | `duikang_shangzeng/…/shots/shot01/shot01.md` | `场景主体` / `物件主体` / `previz灰模视频`（名 `previz_shot01` ≠ 文件 `shot01_previz.mp4`）；`2.35:1`；`@f80_ferrari` |
| S15 | `duikang_shangzeng/…/shots/shot09/shot09.md` | `(人物主体)` 出现在独立剧（abbrev 为空） |
| S16 | `duikang_shangzeng/…/shots/shot20/shot20.md` | `本镜首帧(上一镜末帧)` |
| S17 | `xingji_yingjiu/…/shots/shot02/shot02.md` | `本镜首帧(上一镜末帧)` + `单位参考图` / `角色参考图`；反向标题 `> **反向提示词**：`；shot01 没有 lastframe |
| S18 | `xingji_yingjiu/…/shots/shot10/shot10.md` | `道具参考图` |

**测试**

| ID | 测试名 | 输入 | 期望 / 边界 |
|---|---|---|---|
| UT-R-SHOT-01 | `test_prompt_is_first_text_fence_bytes_verbatim` | S1–S18 | 等于 golden `prompt_sha256`；包含首行 `shotNN` 与 `参考:` 行本身；不含 fence 标记行；末尾换行的处理与 golden 一致 |
| UT-R-SHOT-02 | `test_heading_prefix_variants` | S1、S13 | 两种标题都能定位到 fence |
| UT-R-SHOT-03 | `test_negative_fence_heading_variants` | S1、S4、S8、S17 | 4 种标题都能取到负向 fence；S4 中间隔的空行被容忍 |
| UT-R-SHOT-04 | `test_no_negative_fence_yields_none_and_keeps_inline_negative` | S9、S10、S13 | `negative_prompt=None`；`负面词:` 行仍在 prompt 字节里 |
| UT-R-SHOT-05 | `test_negative_never_merged_into_prompt` | S1 | prompt 不含负向 fence 的任何一行 |
| UT-R-SHOT-06 | `test_reference_items_order_and_split` | S1、S2、S3、S4 | 名称、label、顺序等于 golden；按 ASCII `(` 与 `)=>@` 切分，全角括号保留在 label 内（S3） |
| UT-R-SHOT-07 | `test_both_separator_styles` | S1（`，`）、S4（`, `） | 结果都正确 |
| UT-R-SHOT-08 | `test_ratio_forms` | S1、S4（尾注）、S12（同一行 `｜`）、S13（反引号）、S14（`2.35:1` 原样解析，由预检报错） | 值等于 golden |
| UT-R-SHOT-09 | `test_duration_forms` | S1 `22秒`、S7 `Ns`、S12 同一行、S13 `` `1.5s` `` | 等于 golden；小数原样保留，交给预检判断 |
| UT-R-SHOT-10 | `test_legacy_slot_number_is_error` | S11、S13 | `REF_LEGACY_SLOT_NUMBER`，带 `config_key` 提示 |
| UT-R-SHOT-11 | `test_legacy_no_label_is_error` | S11（`c11_…声音=>@3`）、wushen 的 `c15_青衣女天骄=>@` | `REF_LEGACY_NO_LABEL` |
| UT-R-SHOT-12 | `test_arrow_without_at_is_error_not_empty` | S10 | 结构化错误（建议 `REF_LEGACY_NO_AT`，A-13）；**绝不能返回空参考列表然后判为 ok** |
| UT-R-SHOT-13 | `test_mention_count_equals_reference_count` | S1–S18 | prompt 中 `=>@` 的个数 = 解析出的参考项个数（F2） |
| UT-R-SHOT-14 | `test_literal_at_in_text_is_reported` | S5、S10、S14 | 结果带 `literal_at_positions`，形成 warning（A-14） |
| UT-R-SHOT-15 | `test_missing_ratio_or_duration_is_structured_error` | 基于 S1 在 tmp 中删去 `比例:` 行（合成变体，只用于缺字段的负面测试） | `RATIO_MISSING` / `DURATION_MISSING` |
| UT-R-SHOT-16 | `test_crlf_input_normalised` | S1 转成 CRLF 后的 tmp 副本 | 结果与 LF 版本相同（前提是 A-07 采纳 LF 规范化） |
| UT-R-SHOT-17 | `test_repo_sweep_never_raises` `@real_repo` | 枚举仓库内全部 `shot\d+\.md`（排除 `_deleted`，**实时枚举，不写死 271**） | 每个文件都返回结果或结构化错误，不抛异常；每个文件恰找到 1 个视频 prompt fence；F2 不变量成立；按错误码汇总的报告写到 pytest 日志，**只作信息，不作 golden**（仓库持续演进） |
| UT-R-SHOT-18 | `test_fixture_provenance` `@real_repo` | 每个副本旁的 `{name}.source.json`（`repo_path`、`sha256_at_copy`） | 源文件变了 → 发 warning（不失败）；源文件被删 → info |

### 3.2 参考项 resolver — `test_drama_tree__reader.py`（resolve 段）

对真实仓库树只读，标记 `@real_repo @real_media`。

| ID | 输入 | 期望 |
|---|---|---|
| UT-R-RES-01 | S1 + override `c1_砌炉的老人=hy3_主角` | 4 项：`bg11-1` → `hy3/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11-1.png`（image）；`砌炉的老人` → entity `hy3_主角`；`p2-1`、`p3-1` → 各自卡目录下的 png；每项都有 sha256 |
| UT-R-RES-02 | S2 的 `p1_砍刀` | 通过 `p1_砍刀.png.link.json` 解析到 hy1 的 png；`resolved_path` 是**目标路径** |
| UT-R-RES-03 | stem `c1_造家的人`（hy2 同时有 png 和 mp4 两条 link） | image 规则只匹配 png 那条，不报多重匹配 |
| UT-R-RES-04 | S4 的 `shot02_previz(3D预演视频)` | 找到 `previz/shot02_previz.mp4`（递归，A-11）；`renders/` 下的文件不参与 |
| UT-R-RES-05 | S14 的 `previz_shot01` | `REF_FILE_NOT_FOUND`，`config_key=references.overrides."previz_shot01"` |
| UT-R-RES-06 | S17 的 `本镜首帧(上一镜末帧)` | 查 `shots/shot01/shot01_lastframe.png` → 不存在 → error |
| UT-R-RES-07 | 某剧 shot01 的 `上一镜末帧` | 不去找 `shot00`，直接给出明确错误 |
| UT-R-RES-08 | 在 wushen 中查 stem `shot10_lastframe`（raw override 场景） | `REF_MULTIPLE_MATCHES`，候选列表含 3 个路径 |
| UT-R-RES-09 | 在 xianjian 中查 stem `views1` | `REF_MULTIPLE_MATCHES`，10 个候选 |
| UT-R-RES-10 | S6 / S18 的 `道具参考图` | `REF_LABEL_NO_RULE`，hint「新增一条 rule」 |
| UT-R-RES-11 | tmp 树：`_candidates/bg11-1.png`、`renders/…`、`previz/frames/…` 中放同 stem 文件 | 全部被排除 |
| UT-R-RES-12 | tmp config：两条 glob 规则都能匹配同一 label | 取**第一条** |
| UT-R-RES-13 | 系列剧成员 | 同时搜剧根与 `{series}/_series/`；平铺剧不搜 `_series` |
| UT-R-RES-14 | override 值 `entity:hy3_主角` 与路径形态 | 分别产出 entity 项与 image 项；override 优先于 rule |

### 3.3 `AssetCardReader` — `test_asset_card__reader.py`

真实副本放在 `tests/fixtures/real_cards/`（同样带 `.source.json`）。

| ID | 输入 | 期望 |
|---|---|---|
| UT-R-CARD-01 | hy3 `p3_抹泥板与黏土壁炉.md` | 2 个块：`p3-1`、`p3-2`；prompt 从路由键首行开始逐字节保留；3 个裸 fence（锁定描述符）被忽略 |
| UT-R-CARD-02 | hy3 `bg11_崖脚洼地.md` | 取 `bg11-1_崖脚洼地全景`；首行是负面词清单的 ```text fence 被忽略 |
| UT-R-CARD-03 | hy3 `c1_砌炉的老人.md` | `c1-1` 为图片块；`c1-2_…turntable` 的处理**待定 A-15**（建议：识别为非图片块，给出 skip warning） |
| UT-R-CARD-04 | hy2 `c1_造家的人.md`（复用卡） | 0 个块 |
| UT-R-CARD-05 | wushen 场景卡中首行为 `bg6_空场_无碑`（旧形态，无 `-M`）的块 | 忽略，0 个块 |
| UT-R-CARD-06 | xianjian 卡中首行为 `人脸变形、…` 的 text fence | 忽略 |
| UT-R-CARD-07 | tmp 合成：`p3_…` 目录里出现首行 `p2-1_…` 的块 | 与目录路由键不符 → 忽略并 warning（与 `asset_key.folder_key` 语义一致；A-15） |
| UT-R-CARD-08 | 输出目标 | `output_target` = 主体目录；`block_key` = 路由键；`source.type=asset` |
| UT-R-CARD-09 | 未配置参考图 | `image.command=auto` → text2image；配置了逐块参考 → image2image |
| UT-R-CARD-10 | 比例 | characters 3:4、scenes 16:9、props 1:1；逐块覆盖优先；与 prompt 正文里写的「画幅 16:9」冲突的处理见 A-15 |
| UT-R-CARD-11 `@real_repo` | 全仓 sweep：`characters/`、`props/`、`scenes/` 下所有主体 md | 从不抛异常；取到的块数 = 首行匹配 `^(bg\|c\|p)\d+-\d+_` 的 fence 数（实时计算，不写死 158） |

### 3.4 `drama_ref` 契约（§8 divergence 2）— `tests/libs/common/test_drama_ref.py`

测试**不 import** `ai_video_management`，只按同一条 `series.json` 规则断言。

| ID | 输入 | 期望 |
|---|---|---|
| UT-C-DR-01 `@real_repo` | `ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md` | 深度 3，剧根 `ai_videos/huangye_shenghuo/hy3` |
| UT-C-DR-02 `@real_repo` | `ai_videos/wushen_juexing/…` | 深度 2 |
| UT-C-DR-03 `@real_repo` | `ai_videos/huangye_shenghuo/_series/series_bible.md` | None |
| UT-C-DR-04 `@real_repo` | `ai_videos/_deleted/…` | None |
| UT-C-DR-05 `@real_repo` | 只有 `ai_videos/huangye_shenghuo` 这一段 | None |
| UT-C-DR-06 `@real_repo` | `list_dramas()` | 包含 hy1–hy4 与 5 个平铺剧；不含 `huangye_shenghuo`、`_series`、`_actors` 等；`notes` 是否包含见 A-23 |
| UT-C-DR-07 | tmp：平铺剧里有一个子目录叫 `hy1` | 仍为深度 2（**不按路径深度或目录名推断**） |
| UT-C-DR-08 | tmp：系列目录下有 `_x/` | 不算剧 |
| UT-C-DR-09 `@needs_symlink` | tmp：指向剧目录的 symlink | 跳过 |
| UT-C-DR-10 | 首段不是 `ai_videos`、parts 为空、段为空字符串 | None |

### 3.5 `.link.json` 解析 — `test_drama_tree__reader.py`（link 段）

| ID | 输入 | 期望 |
|---|---|---|
| UT-R-LINK-01 `@real_repo @real_media` | hy2 `p1_砍刀.png.link.json` | 目标 = hy1 png 且存在；`note` 被读出 |
| UT-R-LINK-02 | JSON 格式错误 / 不是对象 / `target` 不是字符串 / `target` 为空 | 结构化拒绝，不抛未捕获异常 |
| UT-R-LINK-03 | `target` 含 `..`、以 `projects/` 开头、为 `C:\…` 绝对路径、UNC `\\host\…` | 拒绝（安全级 critical） |
| UT-R-LINK-04 | `target` 使用反斜杠 `ai_videos\…` | 规范化后接受 |
| UT-R-LINK-05 | `target` 不存在 / 是目录 | 拒绝 |
| UT-R-LINK-06 `@needs_symlink` | `target` 本身是 symlink | 拒绝 |
| UT-R-LINK-07 | `target` 指向另一个 `.link.json` | 拒绝链式 link（A-28） |
| UT-R-LINK-08 | `target` 大小写与盘上不同（`AI_VIDEOS/…`） | 拒绝（段比较大小写敏感，与参考实现一致） |

### 3.6 `jimeng_response__reader` 版本化解析器 — `test_jimeng_response__reader.py`

fixture：`tests/fixtures/jimeng_responses/{web_version}/{endpoint}/{case}.json`，全部来自 stage-6 只读探针，**全部标记 `@probe_fixture`**。

| ID | 用例 | 期望 |
|---|---|---|
| UT-R-RESP-01 | `get_history_queue_info` 排队中 / 生成中 | 解析出排队位置、进度百分比（0..100） |
| UT-R-RESP-02 | `get_history_by_ids` 完成 / 失败 / 审核拒绝 / 写实人脸拒绝 | 状态与失败原因映射到 `PauseReason` / failed 原因；完成时带结果标识 |
| UT-R-RESP-03 | 提交响应 | 取出平台任务标识（字段名由 open question 3 决定） |
| UT-R-RESP-04 | `dreamina_subject/get` | 主体快照 DAO：名称、缩略图 URL、修改时间 |
| UT-R-RESP-05 | commerce 余额 | 取出数值（与网页上「1.1万」这种文本的对账口径见 open question 7） |
| UT-R-RESP-06 | **schema 漂移**：删掉一个必需字段 / 字段类型改变 / 出现未知状态值 | 返回 `ParseFailure{endpoint, web_version, reason}`，**不抛异常**；未知状态值返回 `unknown_status`，而不是随便映射到某个已知状态 |
| UT-R-RESP-07 | body 不是 JSON / 为空 | `ParseFailure`，计数 +1 |
| UT-R-RESP-08 | 按 `web_version` 选择解析器；未知版本 | 回退到最新解析器并 warning |
| UT-R-RESP-09 | 纯函数性质 | 同一输入两次调用结果相等，不读时钟 |
| UT-R-RESP-10 | fixture 脱敏扫描（这一条**不**标 `probe_fixture`，fixture 目录为空时也运行） | 全部 fixture 不含 `sessionid`、`sid_tt`、`msToken`、`a_bogus`、`X-Bogus`、`uid=`、手机号模式 |
| UT-R-RESP-11 | 连续失败计数（计数器所在类见 UT-W-WEB-03） | 解析器只返回失败，不自行决定暂停 |

### 3.7 CLI 输出解析 — `tests/libs/infrastructure/clients/test_dreamina_cli__client.py`（解析段）

fixture 来源：

- `tests/fixtures/fake_dreamina/outputs/*.json`：合成，形态照真实 CLI 抄；
- `tests/fixtures/dreamina_real/`：stage 6 用真实 CLI 只读捕获 `version`、`user_credit`、`list_task` 的输出，标记 `@probe_fixture`。

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-CLI-P01 | `text2image` 成功 | 取出 `submit_id` |
| UT-W-CLI-P02 | `query_result` 为 pending / success（含文件列表）/ fail | 对应的 DAO 状态 |
| UT-W-CLI-P03 | 退出码非零 + stderr | `DreaminaCliError(exit_code, stderr_tail)` |
| UT-W-CLI-P04 | 未登录输出 | 映射到 `cli_login_required` |
| UT-W-CLI-P05 | `AigcComplianceConfirmationRequired` | 映射到 `compliance_confirmation_required` |
| UT-W-CLI-P06 | stdout 里先有横幅文字再有 JSON / 完全不是 JSON | 前者的处理待定（建议取最后一个完整 JSON 对象）；后者 → 结构化错误 |
| UT-W-CLI-P07 | stdout 含中文 | 按 UTF-8 解码；**不依赖 Windows 控制台 cp936** |
| UT-W-CLI-P08 | 版本比较 | `1.4.18 > 1.4.5` 为真（数值比较，不是字符串比较）；`1.4.4 < 1.4.5` → warning |
| UT-W-CLI-P09 | `user_credit` | 解析出整数余额 |

---

## 4. Infrastructure writers / clients（`tests/libs/infrastructure/{writers,clients}/`）

### 4.1 `OutputWriter` — `writers/test_output__writer.py`

媒体 fixture 放在 `tests/fixtures/media/`，每个 < 100 KB：

- `tiny_16x9_22s.mp4`、`tiny_9x16_4s.mp4`；
- `corrupt.mp4`（截断的文件）；
- `tiny.png`（2048×2048）。

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-OUT-01 `@needs_ffprobe` | 正常流程 | 临时文件校验通过 → 目标出现 → 目标字节 sha 与源流相同（FR-45，不改字节）→ sidecar 在 rename **之后**写入 |
| UT-W-OUT-02 | 声明的 sha256 与实际不符 | 目标不出现；临时文件被删；错误 `DOWNLOAD_SHA_MISMATCH` |
| UT-W-OUT-03 | size 不符 | 同上，错误码 `DOWNLOAD_SIZE_MISMATCH` |
| UT-W-OUT-04 `@needs_ffprobe` | `corrupt.mp4` | `FFPROBE_FAILED`；目标不出现 |
| UT-W-OUT-05 `@needs_ffprobe` | 期望 22 s 16:9，实际 4 s 9:16 | `MEDIA_MISMATCH`（容差待定 A-20） |
| UT-W-OUT-06 | ffprobe 不在 PATH | 错误 `FFPROBE_UNAVAILABLE`，与「校验失败」区分；**不跳过校验直接落盘** |
| UT-W-OUT-07 | 目标文件已存在 | 抛 `OutputExistsError`；已存在文件的字节不变（两个平台都要断言结果） |
| UT-W-OUT-08 | 竞态：在 verify 与 rename 之间由测试钩子创建目标 | 仍然不覆盖（机制按平台不同，见 §10） |
| UT-W-OUT-09 | count=3 | 依次落 `_1`、`_2`、`_3`；中途 `_2` 已被占用时的行为待定（A-19） |
| UT-W-OUT-10 | 临时文件位置 | 与目标在同一卷（Windows 上 rename 不能跨卷原子完成） |
| UT-W-OUT-11 | 目标目录不在沙箱内 / 路径含 `..` / 目标是 symlink | 拒绝 |
| UT-W-OUT-12 | 目录名含中文（`bg11_崖脚洼地`） | 正常 |
| UT-W-OUT-13 `@win_only` | 目标所在目录里另一个句柄独占打开了同名临时文件 | 得到可诊断的错误，不留下半成品 |

### 4.2 Sidecar — `writers/test_output__writer.py`（sidecar 段）

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-SC-01 | web 视频 sidecar | FR-44 全部字段存在：`job_id`、`batch_id`、`backend`、`source{type,path,block_key}`、`prompt_sha256`、`negative_prompt_sha256`、`references[{name,kind,path/entity,sha256}]`、`params`、`platform_task_id`、`credits_estimated{static,page}`、`credits_charged`、`submitted_at`、`finished_at`、`confirmer`、`web_version`、`browser_version`、`output{sha256,size,duration_s,width,height}` |
| UT-W-SC-02 | cli 图片 sidecar | 有 `cli_version`，没有 `web_version`；没有 `output.duration_s`；`credits_estimated.page` 为 null |
| UT-W-SC-03 | 文件名 | `{产物文件名}.jimeng.json` |
| UT-W-SC-04 | 编码 | UTF-8、中文不转义、键顺序固定（便于 git diff） |
| UT-W-SC-05 | 不含机密 | 用已知 token 值扫描全文 → 不出现；不出现 `Authorization`、cookie |
| UT-W-SC-06 | `prompt_sha256` | 等于 GenerationRequest.prompt 字节的 sha256（与 S1 golden 交叉校验） |
| UT-W-SC-07 | sidecar 写入失败（目录只读） | 产物保留，job 记录 `sidecar_missing` 并报错；**不删除已校验通过的产物**（A-19） |

### 4.3 `TomlConfigStore` — `writers/test_drama_config__writer.py`、`readers/test_drama_config__reader.py`、`test_global_config__*`

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-TOML-01 | 读入带注释、中文键 inline table（`"c1_砌炉的老人" = "hy3_主角"`）的 fixture，不改任何值直接保存 | 字节完全相同 |
| UT-W-TOML-02 | 只改 `video.count` | 与原文件的 diff 恰好一行；注释与键顺序保留 |
| UT-W-TOML-03 | 追加一条 `references.overrides` | 追加到该表内部，其余内容不变 |
| UT-W-TOML-04 | 读取得到 hash H；外部改写文件；再用 H 保存 | 抛 `ConfigConflictError`（路由映射 409）；文件保持外部改写后的内容 |
| UT-W-TOML-05 | 用匹配的 hash 保存 | 临时文件 → rename 覆盖原文件；返回新 hash |
| UT-W-TOML-06 | 非法值（`video.negative_prompt="merge"`） | 写入前被拒；文件字节不变；错误路径 `video.negative_prompt` |
| UT-W-TOML-07 | hash 的计算对象 | 原始字节（只改空白也会得到不同 hash） |
| UT-W-TOML-08 | 文件是 CRLF | 保存后仍为 CRLF（或按 A-07 统一），测试断言与决定一致 |
| UT-W-TOML-09 | 写入路径 | 只能是 `ai_videos/{drama_root}/jimeng_config.toml` 与 `projects/jimeng_web_bridge/config/global.toml`；其他路径拒绝 |

### 4.4 SQLite `JobStore` — `writers/test_job_store__writer.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-DB-01 | 打开数据库 | `PRAGMA journal_mode` = `wal` |
| UT-W-DB-02 | 实体往返 | JobEntity（含转移日志、子步骤进度、重试计数、PauseReason）存入再读出，两者相等 |
| UT-W-DB-03 | **点击前持久化**：`FakeGenerationBackend.click_generate` 回调中，**另开一个连接**读这条 job | 读到 `submitting` + 指纹（已提交，不是仍在事务里）；并断言 `click_generate` 之前恰好有一次 commit |
| UT-W-DB-04 | 启动扫描 | 返回 `{submitting: […], generating: […], downloading: […]}` 三个列表 |
| UT-W-DB-05 | token 单次使用 CAS | `consume_token(batch_id, token_hash)`：第 1 次影响 1 行、第 2 次影响 0 行；两个线程并发调用 → 恰好一个成功 |
| UT-W-DB-06 | 幂等 key 保留期 | 23h59m 仍可命中；24h01m 被清理（ManualClock） |
| UT-W-DB-07 | 状态转移与日志原子写入 | 在写日志时注入异常 → 状态也回滚 |
| UT-W-DB-08 | 当日 auto_confirm 预算合计查询 | 只统计 `confirmer=http_auto`；按日切分（时区见 A-18） |
| UT-W-DB-09 | 数据库路径 | 只能在 `.data/` 下 |

### 4.5 `DreaminaCliClient` 调用 — `clients/test_dreamina_cli__client.py`（调用段）

fake `dreamina`：`tests/fixtures/fake_dreamina/fake_dreamina.py`。在 echo 模式下，它把收到的 `sys.argv[1:]` 以 JSON 写到 stdout。Windows 上 Python 脚本不能直接作为 argv[0] 执行，测试通过 DI 覆盖「启动器 argv 前缀」为 `[sys.executable, fake_dreamina.py]`——这需要 A-22 的决定。

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-CLI-01 | prompt 含 `"`、`\`、结尾 `\`、`\n`、`%PATH%`、`^&\|<>`、中文、emoji、U+3000 | fake 回显的 argv 与发送值逐字节相等 |
| UT-W-CLI-02 | argv 形态 | 以列表形式传给子进程；静态断言代码库里没有 `shell=True`（UT-S-ARCH-04） |
| UT-W-CLI-03 | 只允许文档化命令 | `text2image`、`image2image`、`query_result --submit_id --download_dir`、`list_task`、`user_credit`、`version`；其他子命令在客户端内部即被拒绝 |
| UT-W-CLI-04 | `cli.path` 含 `~` | 被展开 |
| UT-W-CLI-05 `@win_only` | `cli.path=~/bin/dreamina`（无扩展名） | 解析到 `dreamina.exe`（F24） |
| UT-W-CLI-06 `@win_only` | `cli.path` 指向 `.cmd` / `.bat` | 拒绝（cmd.exe 会重新解析参数；A-22） |
| UT-W-CLI-07 | fake 进程 sleep 超过超时 | 进程被杀，返回结构化超时错误，不留下僵尸进程 |
| UT-W-CLI-08 | 子进程环境变量 | 不含 `JIMENG_BRIDGE_TOKEN` |
| UT-W-CLI-09 | `query_result --download_dir` | 下载到 `.data/tmp/` 下的临时目录，不直接写进 `ai_videos/` |

### 4.6 PageMap — `clients/test_jimeng_page__map.py`（`@browser`）

fake 站点：`tests/fixtures/fake_jimeng_site/index.html` 及其变体。stage-6 探针另外捕获真实 DOM 快照 `tests/fixtures/jimeng_dom/{web_version}/*.html`（脱敏、只读），标记 `@probe_fixture`。

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-PM-01 | **注册表完整性**：必需步骤 id 清单（写死在测试里）⊆ 注册表的键 | 清单：`login_marker`；`creation_type`、`model`、`reference_mode`、`ratio`、`resolution`、`count`、`duration` 各自的 `set` 与 `readback`（FR-29）；`upload_input`、`upload_done_signal`、`upload_rejected`（FR-30）；`editor`、`mention_trigger`、`mention_popup`、`mention_option_by_name`、`mention_node`、`editor_clear`、`negative_field`（可选，FR-31）；`composer_region`、`estimated_credits_text`（FR-32）；`generate_button`、`parallel_limit_notice`、`history_record_by_prompt_prefix`（FR-33）；`history_response_patterns`（FR-34）；`record_download_control`、`record_details_credits`（FR-35）；`captcha_or_risk_popup`、`login_expired_notice`（FR-21）；`entity_page`、`entity_new_form_*`（FR-47、FR-49） |
| UT-W-PM-02 | 每个条目 | 带 `web_version_verified`；定位策略只能是 role / text / label / testid，不能是 `nth` 或坐标 |
| UT-W-PM-03 | 在 fake 站点默认页上逐个 resolve | 每个 selector 在 strict 模式下恰好匹配 1 个元素（可选项允许 0 个） |
| UT-W-PM-04 | 记录内定位 | fake 页面列表里有 3 条记录，selector 只在目标记录容器内命中 |
| UT-W-PM-05 | 注入变体（验证码 / 登录失效 / 并发上限 / 审核拒绝） | 对应探测器命中；默认页上这些探测器不命中 |
| UT-W-PM-06 `@probe_fixture` | 对真实 DOM 快照逐个 resolve | 与 UT-W-PM-03 同样的断言（证明 fake 站点的保真度） |
| UT-W-PM-07 | canary 检查项清单（FR-27） | 每一项都能映射到注册表中的条目；canary 流程引用的条目里不含 `generate_button` 的 click 动作 |

### 4.7 填写校验器（纯函数）— `clients/test_jimeng_browser__client.py`（verifier 段）

纯函数：输入「期望（文本段序列 + mention 名序列）」与「编辑器快照（纯文本 + mention 节点列表）」。

| ID | 用例 | 期望 |
|---|---|---|
| UT-W-FILL-01 | 完全一致 | 通过 |
| UT-W-FILL-02 | 编辑器在末尾多了一个段落换行 / NBSP / `\r\n` | 规范化后通过（规范化规则的细节待定 A-14） |
| UT-W-FILL-03 | 少了一个文本段 | `fill_mismatch`，diff 指出位置 |
| UT-W-FILL-04 | 纯文本相等，但 mention 顺序对调 | `fill_mismatch`（两项校验独立进行） |
| UT-W-FILL-05 | mention 个数少 1 | `fill_mismatch` |
| UT-W-FILL-06 | mention 名显示为 `bg11-1.png`，期望 `bg11-1` | `fill_mismatch`（显示名是否等于 stem 由 open question 2 决定） |
| UT-W-FILL-07 | 文本段里的字面 `@图1`（S10） | 算作文本，不算 mention |
| UT-W-FILL-08 | U+3000 全角空格与连续空格 | 不折叠成单个空格（prompt 逐字节语义），测试断言与决定一致 |
| UT-W-FILL-09 | 按 `=>@` 切段 | S1 切成 5 段文本 + 4 个 mention；S10（`=>` 无 @）在预检阶段就被拦下，不会进入填写 |
| UT-W-FILL-10（fake 站点，`@browser`） | 注入一次填写不一致 | 清空重填 1 次；再次不一致 → `fill_mismatch`，fake 站点的 generate 点击计数为 0 |

### 4.8 其他 clients / writers

| ID | 文件 | 用例 | 期望 |
|---|---|---|---|
| UT-W-TOAST-01 | `clients/test_toast__client.py` | 发送时抛异常 | 只记录日志，不向外抛；作业状态不受影响 |
| UT-W-TOAST-02 | 同上 | payload | 深链到 UI 对应页面；不含 token |
| UT-W-ART-01 | `writers/test_artifact__writer.py` | 截图写入位置 | `.data/artifacts/{job_id}/`；name 中含 `..`、`/`、`\`、`%2e%2e` → 拒绝 |
| UT-W-ART-02 | 同上 | 缩略图 | 长边 ≤ 768 px，保持宽高比 |
| UT-W-ART-03 | 同上 | 成功的 job | 只保留预演截图；失败或暂停的 job 保留截图 + DOM 快照 + trace 片段（FR-36） |
| UT-W-WEB-01 | `writers/test_web_ui_backend__writer.py`（fake 站点，`@browser`） | 参数设置后读回不一致 | 重试 1 次；仍不一致 → `page_contract_broken` |
| UT-W-WEB-02 | 同上 | 上传时文件名与参考项名不同 | 复制到 `.data/tmp/`，改名为 `{name}{ext}` 后上传；原文件不动 |
| UT-W-WEB-03 | 同上 | 连续 N 次 `ParseFailure` | 达到阈值 → `page_contract_broken`；N 的来源待定（A-08） |
| UT-W-WEB-04 | 同上 | canary 运行一遍 | fake 站点 generate 点击计数 = 0 |
| UT-W-WEB-05 | 同上 | 监听方式 | 只用 context 级 `on("response")` 被动读取；不调用 `route()`、`fetch()`，也不伪造请求（静态 + 运行时双重断言） |

---

## 5. Middleware（`tests/libs/infrastructure/middleware/`）

### 5.1 §11 适用性判定

spec §6 规定单一运行模式：UI 构建到 `apps/api/static/`，由同一进程提供；不提供 Vite dev server 模式。因此**不存在改写 header 的代理层**，validation/development.md §11 的「pre-rewrite / post-rewrite / 真实代理」三行**不构成 blocker**。

为防止将来悄悄引入代理，增加两条守卫测试：

| ID | 测试名 | 期望 |
|---|---|---|
| UT-MW-GUARD-01 | `test_no_dev_proxy_configured` | `apps/ui/vite.config.ts` 中不存在 `server.proxy`；README 与 Makefile 不宣传 dev server。**一旦失败**，§11 的三行立即变为必测 blocker |
| UT-MW-GUARD-02 | `test_forwarded_headers_not_trusted` | uvicorn 未开启 proxy headers；请求带 `X-Forwarded-Host: 127.0.0.1:8790`、实际 `Host: evil.com` → 403 |

### 5.2 Host allowlist — `test_host_origin__middleware.py`

| ID | Host | 期望 |
|---|---|---|
| UT-MW-HOST-01 | `127.0.0.1:8790`、`localhost:8790` | 放行 |
| UT-MW-HOST-02 | `LOCALHOST:8790` | 放行（大小写不敏感） |
| UT-MW-HOST-03 | `evil.com`、`127.0.0.1.nip.io:8790`、`[::1]:8790`、`0.0.0.0:8790` | 403 |
| UT-MW-HOST-04 | 缺少 Host header | 403 |
| UT-MW-HOST-05 | `127.0.0.1:9999`（端口不对）、`127.0.0.1`（不带端口） | 待定（建议端口不一致 → 403，不带端口 → 放行） |
| UT-MW-HOST-06 | 分别对 `/api/health`、`/mcp`、`/`、`/assets/x.js` | 同一规则全部生效（`/mcp` 挂载必须在中间件栈内部） |

### 5.3 Origin + Bearer — `test_host_origin__middleware.py`、`test_bearer_token__middleware.py`

| ID | 请求形态 | 期望 |
|---|---|---|
| UT-MW-AUTH-01 | POST `/api/batches`，`Origin: http://127.0.0.1:8790`，无 token | 放行（同源 UI） |
| UT-MW-AUTH-02 | 同上，`Origin: http://localhost:8790` | 放行 |
| UT-MW-AUTH-03 | `Origin: https://127.0.0.1:8790`（scheme 不对） | 403 |
| UT-MW-AUTH-04 | `Origin: http://127.0.0.1:5173`（dev server 源，也是「原始浏览器形态」） | 403 |
| UT-MW-AUTH-05 | `Origin: null` | 403 |
| UT-MW-AUTH-06 | `Origin: https://evil.com` + **正确的** Bearer | 403（Origin 存在且非法时一律拒绝，Streamable HTTP 规范 MUST） |
| UT-MW-AUTH-07 | 无 Origin，`Authorization: Bearer {正确}`，分别打 `/mcp` 与 `/api/*` | 放行 |
| UT-MW-AUTH-08 | 无 Origin，无 token | 403 |
| UT-MW-AUTH-09 | Bearer 错误 / `Bearer` 后为空 / `Basic xxx` / 同时带两个 Authorization header | 403 |
| UT-MW-AUTH-10 | scheme 写成小写 `bearer {正确}` | 放行（RFC 7235 规定 scheme 大小写不敏感） |
| UT-MW-AUTH-11 | **同源 GET 不带 Origin**（浏览器对同源 GET 通常不发 Origin）：GET `/api/jobs` + `Sec-Fetch-Site: same-origin`，无 token | **待定 A-01**（建议放行） |
| UT-MW-AUTH-12 | GET `/api/jobs`，无 Origin，`Sec-Fetch-Site: cross-site`，无 token | 403 |
| UT-MW-AUTH-13 | 浏览器导航 GET `/`、`/assets/*`，无 Origin、无 token | 放行（仍校验 Host） |
| UT-MW-AUTH-14 | 403 响应体 | `{error_code, message, hint}`；不回显 token，也不回显 Authorization |
| UT-MW-AUTH-15 | 日志 | 带 token 的请求被记录后，`.data/logs/*.jsonl` 中不含 token 值 |
| UT-MW-AUTH-16 | `JIMENG_BRIDGE_TOKEN` 未设置 | 待定（建议启动失败，或所有非同源请求一律 403）；**不得出现「未设置 = 不校验」** |
| UT-MW-AUTH-17 | 同源 Origin 访问 `/mcp` 但不带 token | 待定（建议仍要求 Bearer；A-01） |

---

## 6. Application（`tests/libs/application/`，DI override）

公共装配：`ManualClock`、固定 HMAC key、`FakeGenerationBackend`（web 与 cli 各一个实例）、`FakeSessionProbe`、`FakeToastClient`、tmp SQLite `JobStore`、tmp 仓库根（拷入 S1 + hy3 的卡 md，media 用小占位图，其 sha 写死）。

### 6.1 `BatchCommand.precheck` — `commands/test_batch__command.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-BAT-01 | S1 + hy3 config（override `c1_砌炉的老人=hy3_主角`） | 1 条 ok；参数 `seedance2.5` / `16:9` / 22 / `720p` / 1 / `全能参考`；4 个参考项，其中主体为 `hy3_主角`（验收 #1 的应用层部分） |
| UT-A-BAT-02 | 混合 items：shot 路径、`{card_path,key}`、raw 请求 | 同属一个 batch；`source.type` 分别为 shot / asset / raw |
| UT-A-BAT-03 | raw 请求的文件路径在 `ai_videos/` 外 | 条目 error `PATH_OUTSIDE_SANDBOX` |
| UT-A-BAT-04 | 返回值 | `batch_id`、逐条结果、合计积分（error 条目是否计入待定 A-09）、`confirmation_token`、UI URL（形如 `http://127.0.0.1:8790/batches/{id}`）；batch 状态为 `awaiting_confirm` |
| UT-A-BAT-05 | 同一 `idempotency_key`、同内容，调用两次 | 返回同一个 `batch_id`，不新建 batch |
| UT-A-BAT-06 | 同一 key、不同内容 | 错误 `IDEMPOTENCY_KEY_REUSED`（HTTP 409 / MCP isError） |
| UT-A-BAT-07 | 同一 key，时间过去 24h01m | 按新请求处理 |
| UT-A-BAT-08 | 指纹命中一个 done 的 job | 条目标注 `existing_job_id`；确认后不新建 job，直接返回已有 job（验收 #6） |
| UT-A-BAT-09 | 同样的请求带 `reroll=true` | 新建 attempt（序号 +1） |
| UT-A-BAT-10 | 解析错误可操作（验收 #8） | S11 → `REF_LEGACY_SLOT_NUMBER`；多重匹配（tmp 树放两份同 stem 图）→ `REF_MULTIPLE_MATCHES`；S6 → `REF_LABEL_NO_RULE`；三者都带 `config_key` |

### 6.2 `BatchCommand.confirm` — `commands/test_batch__command.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-BAT-11 | 有效 token，confirmer=`ui_human` | batch 进入 confirmed；`confirmer` 与 `confirmed_at`（取 ManualClock）入库；job 进入 queued |
| UT-A-BAT-12 | 重放同一 token | `TOKEN_ALREADY_USED`；job 不重复创建 |
| UT-A-BAT-13 | now = 签发 + 30min + 1s | `TOKEN_EXPIRED` |
| UT-A-BAT-14 | token 被篡改 / 属于另一个 batch | 拒绝 |
| UT-A-BAT-15 | batch 含 error 条目 | 拒绝 |
| UT-A-BAT-16 | confirmer=`http_auto`，但 `allow_http_auto=false` | 拒绝，`config_key=confirm.allow_http_auto` |
| UT-A-BAT-17 | `http_auto` 预算：当日已用 1500，本批 500 / 501 | 500 放行（≤ 2000）；501 拒绝 |
| UT-A-BAT-18 | 预算只统计 `http_auto` | 当日已有 5000 的 `mcp` 确认，不影响 `http_auto` 的判定 |
| UT-A-BAT-19 | 跨日 | ManualClock 越过日界线后预算清零（日界线所用时区见 A-18） |
| UT-A-BAT-20 | 两个线程同时 confirm | 恰好一个成功 |
| UT-A-BAT-21 | confirmer 来源 | confirmer 由调用入口决定，**调用方传入的值不被信任**（A-02）；MCP 入口恒为 `mcp` |

### 6.3 FR-16 硬不变量扫描 — `commands/test_job__command.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-INV-01 | batch 未确认；分别触发调度器 tick、`JobCommand.resume`、`JobCommand.resume_queue`、`BrowserStepCommand.run(op=submit)`、`EntityCommand.create` 的执行段 | `FakeGenerationBackend.click_generate` / `submit` 调用次数 = 0；没有任何 job 的转移日志里出现 `submitting` |
| UT-A-INV-02 | batch 已确认、token 已消费，然后某条 job 被外部改回 awaiting_confirm 等价状态（直接改库） | 调度器仍然不提交（每次提交前从存储重新读取确认证明） |

### 6.4 `JobCommand.cancel / resume / pause_queue / resume_queue` — `commands/test_job__command.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-JOB-01 | 取消 queued / preparing / awaiting_submit_slot 的 job | cancelled；backend 从未被调用 submit；响应里 `credits_spent=false` |
| UT-A-JOB-02 | 取消 generating 的 job | 停止轮询与下载（fake backend 之后不再收到 `poll`）；响应含「积分不会退还」 |
| UT-A-JOB-03 | 取消终态 job | `JOB_ALREADY_TERMINAL` |
| UT-A-JOB-04 | 在 preparing/upload 进行中取消 | upload 做完才生效；fill 从未开始（检查点语义，spec §4 架构） |
| UT-A-JOB-05 | resume（web），canary 通过 | 恢复（目标状态见 A-03） |
| UT-A-JOB-06 | resume（web），canary 失败 | 保持暂停；返回失败项 |
| UT-A-JOB-07 | resume（cli） | 调用 `user_credit` 自检，而不是 canary |
| UT-A-JOB-08 | resume 一个 paused(restart_during_submit) 的 job | `submit` 调用次数 = 0 |
| UT-A-JOB-09 | `pause_queue(web)` | web 队列停止准备与提交；cli 队列照常 tick |
| UT-A-JOB-10 | `resume_queue(cli)`，`user_credit` 报未登录 | 保持暂停，原因 `cli_login_required` |

### 6.5 调度器 tick（位置待定 A-25）— `commands/test_job__command.py`（scheduler 段）

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-SCH-01 | 已有 3 个 generating；另有 1 个 awaiting_submit_slot | 本 tick 不提交 |
| UT-A-SCH-02 | 已有 2 个 generating | 本 tick 提交 1 个，且只提交 1 个 |
| UT-A-SCH-03 | 上次提交在 t0；分别在 t0+14.999s、t0+15s tick | 前者不提交；后者提交（≥） |
| UT-A-SCH-04 | backend 返回并发已达上限 | job 回到 awaiting_submit_slot；不计失败；`last_submit_at` 更新，下一次提交仍受间隔约束 |
| UT-A-SCH-05 | UI 动作串行 | 两个 job 同时处于准备阶段时，`FakeBrowserActor` 从未检测到重叠调用 |
| UT-A-SCH-06 | 选取顺序 | 按 `confirmed_at`、再按条目序号 FIFO（spec 未写，建议值） |
| UT-A-SCH-07 | canary 触发 | batch 开始前跑恰好 1 次；之后每 `canary.interval_min` 分钟 1 次；canary 失败 → 该 batch 不开始 |
| UT-A-SCH-08 | generating 超过 `wait.timeout_h` | paused(wait_timeout)；队列不暂停 |
| UT-A-SCH-09 | 启动恢复（FR-19）：库中已有 submitting / generating / downloading 各 1 条 | 依次得到 paused(restart_during_submit) / 恢复轮询 / 恢复下载；`submit` 调用次数 = 0 |
| UT-A-SCH-10 | 提交对账（FR-33）：点击后没有截获到响应，但历史里有「提交时刻之后、prompt 前缀一致」的一条 | generating，并带该记录的 id；找不到 → paused(restart_during_submit)；找到多条 → 取最新一条（spec 原文） |
| UT-A-SCH-11 | 注入验证码弹窗（验收 #4 的应用层部分） | web 队列暂停；toast 1 次（带截图路径）；cli 队列不受影响 |
| UT-A-SCH-12 | 注入审核拒绝 | 只有该 job 进入 failed(moderation_reject)；其余 job 继续；prompt 未被改写 |
| UT-A-SCH-13 | `max_remote_rendering` 是否把 cli 的 generating 也计入 | 待定 A-25 |
| UT-A-SCH-14 | 浏览器丢失（FR-37） | 暂停 web 队列 → 重建 context → 检查登录 → 对所有 generating 做对账；以上顺序由 fake 记录的调用序列断言 |

### 6.6 `DramaConfigCommand.propose` — `commands/test_drama_config__command.py`

propose 不写文件，所以可以对真实仓库只读运行（`@real_repo @real_media`）。每条用例都断言目标 `jimeng_config.toml` 的字节与 mtime 不变。

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-CFG-01 | hy3，无 config（验收 #7） | `abbrev=hy3`；entities 提议 `c1_砌炉的老人 → hy3_砌炉的老人`、`c2_獾 → hy3_獾`；参考项预览覆盖 hy3 的全部 shot；不写入文件 |
| UT-A-CFG-02 | hy3 + 主体快照 fixture（含 `hy3_主角`） | 「主体名冲突」`needs_confirmation=true` 并带原因——**判定规则待定 A-05**，未定之前这条断言无法写成确定形式 |
| UT-A-CFG-03 | wushen_juexing（独立剧） | `abbrev=""`，`needs_confirmation`，原因「独立剧缺缩写」 |
| UT-A-CFG-04 | hy2 | `c1_造家的人` 经 link 指向 hy1 → 提议 `hy1_造家的人` |
| UT-A-CFG-05 | xianjian | S4 与 S6 所在的镜：`views1` 多重匹配或 `道具参考图` 未命中规则，带 `needs_confirmation`，原因分别为「参考项多重匹配」与「label 无规则」 |
| UT-A-CFG-06 | tmp 剧目录里已有 config | 返回逐键 diff 建议；文件不变 |
| UT-A-CFG-07 | `DramaConfigCommand.save`：合法 / 非法 / hash 冲突 | 分别写入 / 拒绝并给出字段路径 / 409（与 UT-W-TOML 联动） |

### 6.7 `EntityQuery.reconcile` 与 `EntityCommand` — `queries/test_entity__query.py`、`commands/test_entity__command.py`

fixture：快照 `{hy3_主角, hy1_造家的人, 旧主体X}`；hy3 config（override → `hy3_主角`，`c2_獾 → hy3_獾`）；hy2、hy1 都期望 `hy1_造家的人`。

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-ENT-01 | 不带过滤条件 | `mapped`：`hy3_主角`，以及 `hy1_造家的人`（一行，列出 hy1、hy2 两个剧）；`missing_on_platform`：`hy3_獾`；`unmapped_on_platform`：`旧主体X` |
| UT-A-ENT-02 | `drama=hy3` | mapped / missing 只列 hy3 的；unmapped 的计算范围待定 A-24 |
| UT-A-ENT-03 | 快照同步于 25h 前 | DTO 带 `snapshot_stale=true` |
| UT-A-ENT-04 | 名称比较 | 精确字符串相等，不做全半角或大小写归一（建议值） |
| UT-A-ENT-05 | create：名称 21 字 | 预检 error |
| UT-A-ENT-06 | create：`source_images` glob 对 hy3 c1 | 命中 `c1-1.png`；glob 无命中 → error |
| UT-A-ENT-07 | create：同名主体已存在于快照 | 复用；`FakeGenerationBackend.create_entity` 调用次数 = 0 |
| UT-A-ENT-08 | create 未经确认 | 拒绝（沿用 FR-16 的思路） |
| UT-A-ENT-09 | create 成功 | 之后自动 sync 一次，并验证新主体在快照里 |
| UT-A-ENT-10 | FR-50 | backend 端口上根本不存在 rename / delete / overwrite 主体的方法（静态断言） |
| UT-A-ENT-11 | sync | 快照整体替换；`synced_at` 取 ManualClock |

### 6.8 `CandidateCommand.promote` — `commands/test_candidate__command.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-CAN-01 | `_candidates/p3-1/20260913-181500_1.png` → promote（目标不存在） | 复制为 `p3-1.png`；两者 sha 相同；候选文件保留 |
| UT-A-CAN-02 | 目标 `p3-1.png` 已存在，`image_on_existing=archive` | 旧文件**先**被移入 `ai_videos/_deleted/…`（命名见 A-19），**然后**才复制；archive 失败 → 不复制 |
| UT-A-CAN-03 | `image_on_existing=fail` | 报错；两处文件都不动 |
| UT-A-CAN-04 | 候选路径不在 `_candidates/` 内 / 含 `..` / 是 symlink | 拒绝 |
| UT-A-CAN-05 | 归档目标同名已存在 | 不覆盖 |
| UT-A-CAN-06 | 候选的 sidecar | promote 后，`{key}.png.jimeng.json` 与产物同步存在（复制还是重写待定 A-19） |

### 6.9 `HistoryQuery`、`SessionQuery`、`GlobalConfigQuery`

| ID | 文件 | 用例 | 期望 |
|---|---|---|---|
| UT-A-HIS-01 | `queries/test_history__query.py` | 按剧 / 镜 / 资产主体 / 日期过滤 | 结果集正确（fixture 含 20 条 job） |
| UT-A-HIS-02 | 同上 | 每日合计 | 预估与实扣分开求和；提交前就失败的 job 实扣为 0 |
| UT-A-HIS-03 | 同上 | batch 余额 | 带 `balance_start`、`balance_end` |
| UT-A-HIS-04 | 同上 | 按日切分边界 | 23:59:59 与 00:00:00 分属两天（时区见 A-18） |
| UT-A-SES-01 | `queries/test_session__query.py` | `status` | web 部分（登录、canary 逐项、浏览器版本、web_version）与 cli 部分（登录、版本、余额）都在；某一侧取不到时字段为 null 并带原因，不整体失败 |
| UT-A-GC-01 | `queries/test_global_config__query.py` | `get` | 不含 `JIMENG_BRIDGE_TOKEN` 等 `.env` 机密字段 |

### 6.10 Mappers — `mappers/test_*__mapper.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-MAP-01 | Job：Entity → Dao → Entity | 相等（含转移日志、枚举、时间） |
| UT-A-MAP-02 | Batch、EntitySnapshot、DreaminaResult | 同样的往返测试 |
| UT-A-MAP-03 | DTO 序列化 | 枚举序列化为字符串；时间为 ISO 8601 UTC（带 `Z`）；中文不转义 |
| UT-A-MAP-04 | DTO 字段集 ↔ `tests/fixtures/api_schemas/{dto}.json` 快照 | 相等。该快照同时被 UI 的 `types.ts` 契约检查使用（validation/development.md §3，由 system_tests 引用） |
| UT-A-MAP-05 | 映射逻辑的位置 | 只存在于 mapper 文件（静态：DAO / Entity / DTO 类上没有 `to_*` / `from_*` 方法） |

### 6.11 `BrowserStepCommand.run` — `commands/test_browser_step__command.py`

| ID | 用例 | 期望 |
|---|---|---|
| UT-A-STEP-01 | 顺序执行 set_params → upload → fill → preview | 每步都经过 BrowserActor；job 子步骤进度更新 |
| UT-A-STEP-02 | 跳过 upload 直接 `op=fill` | `STEP_ORDER` 错误 |
| UT-A-STEP-03 | `op=submit`，batch 未确认 | 拒绝（FR-16） |
| UT-A-STEP-04 | `op=submit`，batch 已确认，但并发已满 / 间隔未到 | 不点击；返回「等待提交位」 |
| UT-A-STEP-05 | `op` 不在枚举内 | 400 / isError |

---

## 7. MCP tool 包装层（`tests/api/mcp_tools/`）

每个测试用 strict spy 覆盖**全部** Query / Command provider。

| ID | 用例 | 期望 |
|---|---|---|
| UT-MCP-01 | 注册表 | 工具名集合恰好等于 FR-51 的 10 个 |
| UT-MCP-02 | 逐个工具调用一次 | 恰好一个 provider 的恰好一个方法被调用；工具模块没有 import `libs.infrastructure` 或 `libs.domain`（静态） |
| UT-MCP-03 | `resume`：`scope=job` / `scope=queue` | 分别只调用 `JobCommand.resume` / `resume_queue` |
| UT-MCP-04 | `entities`：`op=reconcile` / `op=sync` | 分别只调用 `EntityQuery.reconcile` / `EntityCommand.sync` |
| UT-MCP-05 | 返回形态 | `structuredContent` 等于 DTO 的 JSON；`content[0].text` 解析后等于同一个对象 |
| UT-MCP-06 | 业务错误（如 token 过期） | `isError: true`；带 `error_code`、`message`、`hint`（hint 含确认页 URL 或 `references.overrides."砌炉的老人"` 这类 config 键）；**不是** JSON-RPC 协议错误 |
| UT-MCP-07 | 未预期异常 | `isError: true`，错误码为通用码；不含堆栈、路径外信息与 token |
| UT-MCP-08 | `wait_jobs` 请求 timeout 为 300 | 90 s 内返回（ManualClock / anyio 虚拟时间）；返回当前快照 + 建议的下一步 |
| UT-MCP-09 | `wait_jobs` 进度通知 | 等待期间在 ≤30 s、≤60 s 各发 1 次 `notifications/progress`；job 全部完成则提前返回 |
| UT-MCP-10 | `get_screenshot` | 返回路径 + 长边 ≤ 768 px 的缩略图；不含原图 base64 |
| UT-MCP-11 | `confirm_batch` 传入 `confirmer: "ui_human"` | 入库的 confirmer 仍为 `mcp`（A-02） |
| UT-MCP-12 | 静态 | 代码里不使用 elicitation，也不使用 MCP tasks 扩展 |
| UT-MCP-13 | `precheck_batch` 的三种 item 形态 | 各自正确转成 `BatchCommand.precheck` 的输入 |

HTTP routes 用同样的「一个入口 = 一个方法」spy 测试：`tests/api/routes/test_{aggregate}__route.py`，逐项覆盖 §5.10 表中的 25 行。`serve_static=True` 下的状态变更端点测试属于 system_tests（validation/development.md §1），这里不重复。

---

## 8. 静态 / 架构测试（`tests/test_architecture.py`，AST 扫描）

| ID | 断言 |
|---|---|
| UT-S-ARCH-01 | 层间依赖方向符合 development.md §1（infra → common；domain → common；application → 三者；apps → application + common），违反即 blocker |
| UT-S-ARCH-02 | 文件名后缀与类名一致（`__entity` → `…Entity` 等）；commands / queries 每个文件恰好一个类 |
| UT-S-ARCH-03 | `container.py` 中每个 route / tool 引用的 provider 都存在（防止 wire 时启动崩溃，development.md §5） |
| UT-S-ARCH-04 | 代码中无 `shell=True`、`os.system`、`subprocess.getoutput` |
| UT-S-ARCH-05 | 代码中无坐标点击（`mouse.click(`、`position=`）；无 stealth / 指纹伪装库（`playwright_stealth`、`undetected`）；无 `add_init_script` 修改 `navigator.webdriver` |
| UT-S-ARCH-06 | FR-5 写死值扫描：`8790`、`"hy3"`、`"_candidates"`、`"renders"`、`5000`、`"全能参考"`、`"seedance2.5"` 只允许出现在默认值模块与 `config/global.toml` 中（默认值模块的位置待定 A-08） |
| UT-S-ARCH-07 | Makefile 不含 `uv`；`make test` 使用 `.venv` |
| UT-S-ARCH-08 | 测试目录镜像源码树：每个 `libs/**/*.py` 都有对应的测试文件，或列入白名单并说明原因 |
| UT-S-MARK-01 | 设置 `JWB_REQUIRE_*=1` 时，对应 marker 的用例变为 fail 而不是 skip |

---

## 9. Fixtures inventory

| 路径（`tests/fixtures/` 下） | 来源 | 覆盖 | 刷新策略 |
|---|---|---|---|
| `real_shots/*.md` + `.expected.json` + `.source.json` | 真实仓库副本 S1–S18 | §3.1 全部变体 | 冻结；源文件漂移只发 warning；新增变体时追加副本，不改旧副本 |
| `real_cards/*.md` + 同上 | 真实仓库副本：hy3 p3 / c1 / bg11、hy2 c1、wushen 旧形态场景卡、xianjian 负面词 fence 卡 | §3.3 | 同上 |
| （无副本）真实 `ai_videos/` 树只读 | 仓库本身 | sweep、resolver、drama_ref、link、propose | `@real_repo` / `@real_media` |
| `jimeng_responses/{web_version}/{endpoint}/*.json` | stage-6 只读探针捕获，脱敏 | §3.6 | 每次 `web_version` 变化时追加一个版本目录 |
| `jimeng_dom/{web_version}/*.html` | stage-6 探针保存的 DOM 快照，脱敏 | UT-W-PM-06 | 同上 |
| `fake_jimeng_site/` | 合成（按探针结果写） | §4.6、§4.7、§4.8 | 探针结论变化时更新 |
| `fake_dreamina/fake_dreamina.py` + `outputs/*.json` | 合成 | §3.7、§4.5 | CLI 版本升级时对照 `dreamina_real/` 核对 |
| `dreamina_real/{version,user_credit,list_task}.txt` | 真实 CLI 只读捕获 | UT-W-CLI-P08/P09 | `@probe_fixture` |
| `configs/hy3_commented.toml` 与 `configs/invalid/*.toml` | 合成（含注释、中文键、全部非法样例） | §2.7、§4.3 | 随 schema 变化 |
| `configs/model_limits_2026-09-13.toml`、`configs/price_table_sample.toml` | 按 spec 表抄写；price 结构待 A-09 | §2.5、§2.6 | 探针后更新 `as_of` |
| `entity_snapshots/*.json` | 合成（按 UT-R-RESP-04 的 DAO 形态） | §6.7 | — |
| `media/tiny_16x9_22s.mp4`、`tiny_9x16_4s.mp4`、`corrupt.mp4`、`tiny.png` | 合成，每个 < 100 KB，放在 `projects/` 下（不属于 `ai_videos/` 的 R2 管辖） | §4.1 | — |
| `api_schemas/*.json` | 由 DTO 导出后人工核对 | UT-A-MAP-04 与 UI 契约 | DTO 改动时同步提交 |

---

## 10. Windows / POSIX skip markers

canonical 宿主是 Windows（validation/development.md §5）。以下测试**必须**带 marker，缺 marker 属于 blocker。

| 测试 | marker | 原因 |
|---|---|---|
| UT-C-DR-09、UT-R-LINK-06、UT-A-CAN-04（symlink 分支）、UT-W-OUT-11（symlink 分支） | `needs_symlink`（运行时能力探测，不按平台判断） | Windows 创建 symlink 需要 Developer Mode |
| UT-W-OUT-08 的「POSIX 下 rename 会覆盖，必须用 link/O_EXCL 保证不覆盖」分支 | `posix_only` | POSIX 的 `rename` 会静默覆盖目标 |
| UT-W-OUT-08 的「Windows 下 rename 抛 FileExistsError」分支 | `win_only` | NTFS 语义 |
| 断电情况下 `os.replace` 的原子性 | 不测试，写明 skip 原因 | 在 NTFS 上只是 best-effort |
| UT-W-OUT-13（共享冲突 / 句柄独占） | `win_only` | Windows 独有 |
| UT-W-CLI-05、UT-W-CLI-06（`.exe` 解析、`.cmd` 拒绝）、UT-W-CLI-01 的 CreateProcess 引号分支 | `win_only` | `list2cmdline` / PATHEXT |
| UT-W-CLI-01 的 execve 分支 | `posix_only` | — |
| UT-W-CLI-07 用信号杀进程的分支 | `posix_only`；Windows 走 `TerminateProcess` 分支，标 `win_only` | 不使用 `os.fork` |
| 路径大小写（`BG11-1.png` 与 stem `bg11-1`） | resolver 自己做大小写敏感的比较，**不依赖文件系统**；验证文件系统行为的测试标 `posix_only` | NTFS 默认大小写不敏感 |
| 目标路径超过 260 字符 | `win_only` | MAX_PATH；hy3 下的深层中文路径有风险 |
| UT-W-TOAST-* 真实弹出 | `win_only`，并作为 `requires_manual_walkthrough` | 需要交互桌面 |
| UT-W-PM-*、UT-W-FILL-10、UT-W-WEB-* | `browser` | Playwright 浏览器需要单独安装 |
| 需要 media 的真实树测试 | `real_media` | media 在 R2，新 clone 默认没有 |
| UT-W-OUT-01/04/05 | `needs_ffprobe`；sign-off 时由 `JWB_REQUIRE_FFPROBE=1` 强制 | — |
| 中文路径与 UTF-8 解码 | 两个平台都运行，不设 skip | Windows 控制台默认 cp936 |

---

## 11. 阻碍确定性单测的 spec 歧义

严重度含义：`blocker` = 不定就写不出确定断言，并且涉及 FR-16、安全或验收条目；`warning` = 有可行的建议默认值，需要确认。

| ID | FR | 问题 | 建议默认 | 受阻测试 | 严重度 |
|---|---|---|---|---|---|
| A-01 | NFR 安全、FR-53 | 浏览器对同源 GET 通常**不发 Origin**，按「同源 UI 靠 Origin 放行」的写法，UI 的所有 GET 都会被 403。另外：未设置 token 时怎么办？`/mcp` 在带同源 Origin 时是否仍要求 Bearer？ | 无 Origin 但 `Sec-Fetch-Site: same-origin` 视为 UI；`/mcp` 一律要求 Bearer；token 未设置则拒绝启动 | UT-MW-AUTH-11/16/17 | blocker |
| A-02 | FR-14、FR-15 | HTTP 如何区分 `ui_human` 与 `http_auto`？如果 confirmer 由调用方自报，脚本可以冒充人工。带 Bearer 但不带 `auto_confirm` 的 HTTP confirm 算什么？ | confirmer 由认证形态推导（同源 → ui_human；Bearer 调 `/api` → 必须显式 `auto_confirm` 且满足预算；MCP → mcp） | UT-A-BAT-21、UT-MCP-11 | blocker |
| A-03 | FR-17、FR-20–23 | 状态机缺边：提交后取消的终态名；各类暂停恢复后回到哪个状态；`upload_rejected` / `real_face_rejected` / `fill_mismatch` / 重试耗尽 / 提交异常属于 failed 还是 paused；submitting 期间取消怎么处理 | preparing 阶段来源的暂停恢复到 queued（页面状态已丢，重做准备）；generating 来源的恢复到 generating；restart_during_submit 只允许人工在对账后标为 generating / failed / cancelled | UT-D-JOB-01/12/18、UT-C-ENUM-04、UT-A-JOB-05 | blocker |
| A-04 | FR-21 | 队列级暂停是只设一个队列标志，还是把相关 job 都置为 paused？同队列里其他 job 显示什么？ | 触发暂停的那条 job → paused(reason)，队列打标志，其余 job 保持原状态 | UT-A-SCH-11 | blocker |
| A-05 | FR-3、验收 #7 | 「期望主体名与即梦现有主体不一致」怎么判定？快照里没有「主体 ↔ 角色」的对应信息。跨集来源缩写取来源剧 config 里的 abbrev，还是来源剧目录名？ | 规则示例：快照中存在同 abbrev 前缀、但不在任何剧期望集合里的主体 → 标为冲突候选；来源缩写优先取来源剧 config，没有再用目录名 | UT-A-CFG-02、UT-D-NAME-05 | blocker |
| A-06 | FR-24 | 指纹的规范化编码没有定义：分隔方式、`None` 与 `""`、params 序列化、`output_target` 的粒度（落到文件名时 ts 每次不同，永远去不了重） | 用带类型标签的 canonical JSON；`""` 视为 None；`output_target` 取目录 | UT-D-FP-*、UT-A-BAT-08、验收 #6 | blocker |
| A-07 | FR-8 | `core.autocrlf=true` 且没有 `.gitattributes`：新 clone 的 shot md 可能带 CRLF，从而改变 prompt 字节、指纹与字数 | reader 统一转成 LF；另议是否在仓库加 `*.md text eol=lf`（会影响仓库文件，需用户决定） | UT-R-SHOT-16、UT-D-FP-01 | blocker |
| A-08 | FR-5 | 多个阈值写在 FR 正文里却没有 config 键：token TTL 30 min、快照过期 24h、幂等保留 24h、重试 3 次、FR-34「解析连续失败超过阈值」（**连数值都没有**）、90 s / 30 s / 768 px。另外：未知键是否拒绝、默认值放在哪个模块、`description_from` / `ratio_source` 的枚举值 | 要么补充 config 键，要么在 spec 中明确列为「非 FR-5 范围的协议常量」；FR-34 阈值补一个数（建议 5）；未知键拒绝 | UT-D-CFG-META-01、UT-W-WEB-03、UT-S-ARCH-06 | blocker |
| A-09 | FR-12、FR-13 | `price_table` 结构未定义（按模型 × 分辨率 × 秒？图片按张？）；合计积分是否包含 error 条目 | `price_table.{model}.{resolution}.per_second` / `per_image`；合计只算非 error 条目 | UT-A-BAT-04、预估积分相关测试 | blocker |
| A-10 | FR-1、FR-2、§2 | `image.model="5.0"` 与 `model_limits` 的键 `seedream5.0` 名字对不上；FR-1 允许 `routing.image=web`，但 §2 把网页端出图列为 out of scope | 统一用 `seedream5.0`；v1 schema 只接受 `routing.image=cli` | §2.7 对应行 | warning |
| A-11 | FR-8 | `stem_in_shot` 是否递归？真实数据中 previz 视频放在 `previz/` 子目录（F11） | 递归查找，排除 `search_exclude` | UT-R-RES-04 | warning |
| A-12 | FR-8 | `prev_shot_lastframe` 依赖上一镜的成片：同一 batch 里放入连续承接的两镜时，下一镜必然预检失败；一集第一镜怎么办；跨集怎么办 | v1 报预检错误并提示「先完成上一镜」；不支持跨集 | UT-R-RES-06/07 | warning |
| A-13 | FR-8、FR-11② | 旧写法 `名字=>`（无 `@`，wushen 60 个文件）不在 spec 列出的错误类型里；`*声音` 规则真实零命中（F7）；`first_frame` 与主体是否计入参考数量上限 | 新增错误码 `REF_LEGACY_NO_AT`；`first_frame` 计入图片上限，主体不计入 | UT-R-SHOT-12、UT-D-PRE-02 | warning |
| A-14 | FR-31 | 94 个真实文件的正文里有字面 `@`（F17），逐字输入会弹出 mention 浮层；「规范化空白」的具体规则（NBSP、U+3000、段落换行）没有定义 | 文本段一律用不触发浮层的插入策略；预检给 warning `literal_at_in_prompt`；只规范化 `\r\n` / NBSP / 段落边界，不折叠 U+3000 | UT-R-SHOT-14、UT-W-FILL-02/07/08 | warning |
| A-15 | FR-9 | 角色卡里的 `c1-2_…turntable` 是视频块，而 FR-9 把所有路由键块都当作出图请求；块内 `负面词:` 行怎么处理（CLI 是否有负向参数）；prompt 正文写「画幅 16:9」而 config 默认 characters 3:4；块首路由键与目录路由键不一致 | 块内出现 `参考:` / `=>@` 或路由键对应落盘为 `.mp4` → 跳过并 warning；以 config 比例为准，冲突时预检 warning；路由键不一致 → 忽略并 warning | UT-R-CARD-03/07/10 | blocker（决定 hy3 c1 的期望块数） |
| A-16 | FR-11 | 预检被称为「纯函数」，但检查 ① 与 ⑦ 需要 I/O | application 先收集「事实」，再交给 domain 纯函数判定（本文已按此写） | §2.5 | warning |
| A-17 | FR-11⑤ | 字数的计数单位：Unicode 码点、仓库 K10 的「中文字符」，还是浏览器 maxlength 用的 UTF-16 码元？ | 整个 fence 的 Unicode 码点数 | UT-D-PRE-07 | warning |
| A-18 | FR-15、FR-42、FR-46 | 「当日」预算、每日合计、文件名 `{ts}` 各自用哪个时区？ | 统一用本机本地时区，经 Clock 注入；sidecar 内的时间用 UTC | UT-A-BAT-19、UT-A-HIS-04、UT-D-NAME-11 | warning |
| A-19 | FR-42–FR-44 | 同一镜、同一秒内的两个 job 会得到同名文件；候选序号 `i` 从 0 还是 1 开始；归档名 `{原相对路径}.{ts}.png` 会出现双扩展名；sidecar 写入失败时产物怎么处理；promote 时 sidecar 是复制还是重写 | 同名时追加 `-2`；`i` 从 1 开始；归档名为 `{原路径去扩展名}.{ts}{ext}`；sidecar 失败时保留产物并标记 | UT-W-OUT-09、UT-A-CAN-02/06、UT-W-SC-07 | warning |
| A-20 | FR-35 | ffprobe 的时长容差、比例判定方式；ffprobe 缺失时怎么办 | 时长 ±0.5 s；宽高比按约分后精确比较；缺 ffprobe → 拒绝落盘 | UT-W-OUT-05/06 | warning |
| A-21 | FR-13、FR-14 | HMAC key 从哪来（每次进程随机生成则重启后 token 失效；从 Bearer token 派生则两种机密耦合）；到期时刻当秒是否有效 | 独立的 key 文件放在 `.data/`，首次启动生成；到期时刻当秒即拒绝 | UT-D-TOK-05 | warning |
| A-22 | FR-38、NFR 可测性 | `cli.path` 默认值不带 `.exe`；路径指向 `.cmd` 包装脚本时参数会被 cmd.exe 重新解析；Windows 上 fake dreamina（Python 脚本）无法直接作为 argv[0] 执行 | 增加 `cli.launcher_argv` 覆盖项（仅测试或高级用途），`.cmd` / `.bat` 拒绝 | UT-W-CLI-01/05/06 | warning |
| A-23 | FR-10 | `ai_videos/notes/` 按 series 标记规则会被认成平铺剧；`list_dramas` 要不要额外过滤（例如要求存在 `2_世界观人设` 或 `5_6_分镜与prompt`）？ | `drama_ref` 保持与参考实现一致；`list_dramas` 在展示层过滤 | UT-C-DR-06 | warning |
| A-24 | FR-48 | `reconcile(drama=…)` 时，`unmapped_on_platform` 是对全部剧计算还是只对该剧计算 | 始终对全部剧计算 | UT-A-ENT-02 | warning |
| A-25 | §4、§7、FR-18 | 调度器没有出现在 §7 布局里（是 application command 还是 apps 的后台任务）；`max_remote_rendering` 是否把 cli 的 generating 也算进去（取决于两边是否共用积分池，见 open question 7） | 放在 `JobCommand.tick`，由 apps 的后台任务调用；上限按 backend 分别计算 | §6.5 | warning |
| A-26 | FR-30–35 | 响应字段、上传完成信号、mention 的 DOM 结构与显示名全部依赖 stage-6 探针 | 相关测试标 `probe_fixture`，sign-off 时强制 | §3.6、UT-W-PM-06、UT-W-FILL-06 | warning（依赖，不是歧义） |
| A-27 | FR-11⑥⑧ | 从未同步过主体快照时报 error 还是 warning；指纹命中的严重度 | 从未同步 → error；指纹命中 → warning | UT-D-PRE-08/10 | warning |
| A-28 | FR-10 | `.link.json` 的 target 本身又是一个 `.link.json`：参考实现会把它当作普通文件接受 | 拒绝链式 link | UT-R-LINK-07 | warning |

---

## 12. FR → 单测覆盖速查

| FR | 章节 | 备注 |
|---|---|---|
| FR-1, FR-2, FR-5 | §2.7、UT-S-ARCH-06 | 契约表 |
| FR-3, FR-4 | §6.6、§4.3 | |
| FR-6, FR-7 | §6.1、UT-D-FP | |
| FR-8 | §1、§3.1、§3.2 | 真实产物 |
| FR-9 | §3.3 | |
| FR-10 | §3.4、§3.5 | |
| FR-11, FR-12 | §2.5、§2.6 | FR-12 中的页面预估属于 system 层 |
| FR-13–FR-16 | §2.4、§2.2、§6.2、§6.3、§5 | |
| FR-17–FR-24 | §2.1、§2.8、§4.4、§6.4、§6.5 | |
| FR-25–FR-37 | §4.6、§4.7、§4.8、UT-A-SCH-10/14 | 真实浏览器会话、登录、下载属于 system_tests / 手工 canary |
| FR-38–FR-41 | §3.7、§4.5 | |
| FR-42–FR-45 | §4.1、§4.2、§2.9 | |
| FR-46 | §6.9 | |
| FR-47–FR-50 | §6.7、UT-R-RESP-04 | |
| FR-51–FR-53 | §7 | FR-53 的 README 片段由 acceptance 检查 |
| FR-54, FR-55 | — | UI 属于 e2e / system_tests，另加手工 walkthrough |
| FR-56 | §4.8 | 真实弹出靠手工 walkthrough |
