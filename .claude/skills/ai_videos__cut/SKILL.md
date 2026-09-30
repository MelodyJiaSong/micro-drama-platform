---
name: ai_videos__cut
description: 例：/ai_videos__cut 魔兽世界 ep01 ——AI 短剧后期剪辑师：Claude 读整集观感审稿、实测台词时间（强制对齐）与镜内切点，只从候选切点里挑，给一集的 cut/edl.toml 提类型化补丁（剪头尾 / 删整段 / 闪前冷开场），确定性校验器把关，出代理片交用户逐条批，批了才升版本、finish_ep 出成片、qc 从成片回读。用户说「剪一下」「剪掉空镜」「冷开场」「节奏拖」「按审稿剪」或 /ai_videos__cut <剧名> <ep> 时触发。
argument-hint: "<剧名> <ep> 例: 魔兽世界 ep01 | shengji_zhilu ep01"
---

# AI 剪辑师（/ai_videos__cut）

剪辑决定是文本：每集 `{集}/cut/edl.toml` 是唯一出处（git 跟踪）。ffmpeg（`finish_ep`）只照它出片；任何 GUI 剪辑软件都不是出处。
设计上仍硬切 + 景别跳档（ai_video.md 16.5–16.7）——**零人工剪辑，不是零剪辑**（rule 42 剪辑）。

参数 ＝ `$ARGUMENTS`：剧名（目录名或 `seedance.toml` 的 alias）+ 集号。

## 0. 分工

| 谁 | 做什么 |
|---|---|
| 本 skill（Claude） | 读审稿 + 实测，挑候选切点，写补丁，跑校验，出代理片，交用户批 |
| `tools/post/edl.py` | `init` / `candidates` / `verify`（V1–V10）/ `plan`，全部确定性 |
| `tools/post/align.py` | 强制对齐与 WER（`.venv-post`；edl 缺缓存时自动调） |
| `tools/post/finish_ep.py` | 按 edl 出片（无 edl ＝ 整镜顺接）；`--proxy` 出代理片 |
| `tools/post/qc.py` | 成片回读质检 Q1–Q9 |
| 用户 | 逐条批补丁、锁版 |
| 剧本 / 分镜层（另一流程） | 需要新画面的意见：改剧本再出片——本 skill 只开票，**不改 shot md / 剧本 / prompt** |

## 1. 输入

- 当前审稿：`viewing/review.md`（成片）或 `viewing_animatic/review.md`（animatic）——注意力表、预计划走点、最该改的 3 处。
- `python tools/post/edl.py candidates <剧> <ep>` → `post/cut/candidates.json`：每镜合法切点（离词 ≥ 0.08 s）、镜内切点、死区（> `idle_max_s` 无词无节拍）。**in / out 只许取这里的点或锚点**，不自编时间码。
- 对齐缓存 `post/align/{shot}.{sha12}.json`：每句实测起止、`missing` / `low_conf` 句子（Seedance 漏说、改词、换顺序）。
- 剧本意图（好笑 / 好哭标签）、`goals.toml` 锚点句——剪后必须仍在（V3）。

## 2. 补丁（封闭菜单）

| op | 写法 | 约束（verify 查） |
|---|---|---|
| 剪头 / 剪尾 | 改事件 `in` / `out`：秒数、`line:N.start-0.3`、`cut:K`；用了 `line:` / `cut:` 的事件照抄 candidates 里这条 take 的 `basis` | V2 不切词、删句整句删；V6 场景窗不低于 `post_trim_*`；basis 对不上（md 改过、align 重算）即报错，按新 candidates 重挑 |
| 删整段 | 一镜拆成两个事件，中间不要 | 新接缝过 K31（V4），做不到写 `match_ok = "理由"` |
| 闪前 / 冷开场 | 新增 `kind = "flash"` 事件 | ≤ 4 s，每集 ≤ 2 个，≥ 0.6 s（V5） |
| 留空档 | 剪后仍 > `idle_max_s` 的静场 | 事件写 `quiet_ok = "理由"`（V7） |
| 开票 | `[[note]] status = "ticket"` | 要新画面（近景、补拍、换表演）：交剧本层，不在这里修 |

暂不开放：重排、定格 / 延长（hold）、J/L 音画错位、变速、换 take（换 take 是采用层的事）。
每个非整镜事件写 `why`（审稿条目号或闸门号）；审稿「最该改的 3 处」每条在 `[[note]]` 记 `patched / ticket / waived`（V9）。

## 3. 循环

1. 没有 edl：`python tools/post/edl.py init <剧> <ep> [--shots 1-6,9]` → v1 整镜顺接草稿。
2. 读审稿 + candidates，写 v(N+1) 草稿：`status = "draft"`、`base_version = N`（V10 防并行会话覆盖）。
3. `python tools/post/edl.py verify <剧> <ep> --proxy-ok`：逐条修，最多 3 轮；同一错误连着两轮 → 停下报用户。
4. `python tools/post/finish_ep.py <剧> <ep> --proxy` → `post/proxy/{ep}_v{NNN}_proxy.mp4`（540p、烧时间码与双语字幕）。
5. 新鲜子代理按 `ai_videos__整集观感` 看代理片观片包（`tools/viewing_packet.py <剧> <ep> --video <代理片>` → `viewing_proxy/{代理片名}/`，不碰成片的 `viewing/`），与上一版逐镜比注意力；变差的改动排最前。
6. AskUserQuestion 逐条批（每条：哪一镜、剪掉哪几秒、为什么、比上一版好在哪）；批了的保留，没批的撤回。
7. 用户批完：`status = "approved"`、`approved_by` 写用户 → `finish_ep.py <剧> <ep>` 出成片（草稿直接报错；它先跑不带 `--proxy-ok` 的 verify，每条 take 须有绑 sha 的「通过」审片结论，有一处不过即停；字幕读不完也在出母带前停，开票给剧本层）→ QC 全过才存档 `post/masters/v{NNN}/` → changelog 一行。

## 4. 不做

- 不改 shot md / 剧本 / prompt；不换 take；不变速、不补画；不在 GUI 剪辑软件里点。
- 不为了凑集长注水：集长越界只警告。
- 不跳过审片：`verify` 的 V1 在正式出片时是硬闸门。
