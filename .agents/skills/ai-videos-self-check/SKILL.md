---
name: ai-videos-self-check
description: 技能出片前后的自检与自我进化（Claude / Codex 通用）：出片前先过闸门（规格、参考、体型、每个角色的立场与视线），出片后机检＋多视角独立审稿（每个角色各一个审稿人、导演、观众、原版还原，轮换模型）再过闸门；用户抓到问题记缺陷、放行记误报，让检查越用越准。仓库级与剧级分开。
metadata:
  claude:
    argument-hint: '<出片目录> [--when 一镜到底]'
---

> Claude / Codex 共用正文。执行前按根目录 `AGENTS.md` 路由，工具、提问、委派、参数与收尾遵 `CONVENTIONS.md` § Tool scoping and team coordination 与「用户报问题」节的「仓库级与剧级」「自检与自我进化」。路径相对仓库根。

# 出片自检与自我进化

**只对剧目录里有 `qc_checks.toml`（剧级登记表）的剧生效**；没有的剧照原流程。查什么＝仓库级 `.agents/references/project/qc_checks.toml` ＋ 剧级 `ai_videos/{剧}/qc_checks.toml`，`tools/qc.py` 自动合并。

## 两个代理一样做

| 能力 | 做法（Claude 与 Codex 相同） |
|---|---|
| 机检 | 跑 `tools/motion_check.py` 等工具，结论用 `qc.py record --by machine` 记 |
| 独立审稿 | `python tools/qc_review.py <出片目录>`：另起 `codex exec` / `claude -p` 进程，在临时空目录、只读下只看拼图与规格；默认交给**另一个**模型（Claude 调用 → Codex 审，反之亦然），失败自动换另一个，都失败记「未审」。不用代理自带的子代理，也不由作者自判 |
| 日志 | 只用 `tools/followup.py new / done`：各会话先记在自己的 `_inbox` 条目，`merge` 周期性汇聚（Stop 钩子每次先跑）；`skill_pack.py submit` 提交前只查**本会话**的条目（撞号、格式、待补超时），别的会话的只提示、不拦 |
| 收尾 | Claude 由 Stop hook 拦；Codex 没有 hook，收尾显式跑 `python tools/followup.py check --all` |

## 两层、三种结论（2026-11-14，用户定，dota_yingxiong follow-up 354）

审查不随流程版本变：登记表每条标 `layer`，提示词里每项带【通用】或【对照规格】。

| | 通用质量 `quality` | 对照规格 `spec` |
|---|---|---|
| 判什么 | 产物本身有没有观众看得出的错，不拿规格里的秒数、措辞、身高数字当判据 | 和这一条**提交时**的规格比，只有大偏差判不过（不要求精确到秒；`tolerance`，默认 `qc.py` `SPEC_TOLERANCE`） |
| 审不了·材料缺 | 挡：补材料或修工具再审 | 只记录（旧产物缺新版材料不算片子差） |
| 审不了·看不清 | 放行、列为待人看 | 放行、记录 |

不按出片日期豁免；「拿不准就判 fail」已取消，旧规则下审稿给的 fail 闸门会要求重审。

## 出片前（`skill_pack.py submit` 会自动拦，不过不提交）

1. **体型**：身高只写在人物卡「体型 / 年龄 / 种族」一行，`python tools/scale_table.py <剧>` 派生对照表与图（`ai_videos/{剧}/scale_table.{md,png}`）；缺身高先补卡，**改体型＝改卡**。
2. **机检**：`python tools/qc_pre.py machine <技能目录>`——出场角色卡里有身高、该英雄四条合计 ≥ 53 s、审核敏感词。
3. **多视角独立审稿**：`python tools/qc_review.py <技能目录> --pre`——每个出场角色各开一个审稿人代入自己的立场审动作逻辑与视线，导演审规格必答项 / 开场图比例 / 锁定特征（附身份立绘），原版还原对照 DotA 1 原版截帧与模型图审参考（我们的设计稿本就是真人质感，不拿来判版本）。
4. 结论在技能目录 `qc_pre.json`，绑定资料包的 prompt 与参考 sha；规格或参考一改就作废、重审。

## 片子落地后（`skill_pack.py poll` 会打印这几条）

1. **机检**：`python tools/motion_check.py <片> --action <起势结束>-<收势开始> --sheet <出片目录>/sheet_4fps.jpg`，看拼图判定，`python tools/qc.py record <出片目录> --check video.slowmo=pass|fail --by machine --evidence "…"`；规格要求一镜到底时同记 `video.onetake_cuts`。
2. **多视角独立审稿**：`python tools/qc_review.py <出片目录> [--when 一镜到底]`——每个角色各一个审稿人看拼图判立场与眼神，导演判时间轴 / 人数 / 体型 / 起势收势，观众**不看规格**只看画面说出发生了什么，原版还原对照峰值图与原版截帧；视角轮流分给两个模型并行，任一视角不过即不过，结论自动写进 `qc.json`。
3. **闸门**：`python tools/qc.py gate <出片目录> [--when 一镜到底]`。不过就改 prompt 重出，**每镜最多重出两次**（用户 2026-11-09），第二次重出仍不过就停，带审稿证据找用户（见出片「重试与搁置」）。
4. 理由照写进 `review.md`（给人看）；`qc.json` 给闸门与统计读。

## 用户的反馈怎么变成进化

- **用户抓到问题**（检查漏了）：`python tools/qc.py defect <剧> --category <检查id|new:短名> --artifact <片> --caught-by user --followup NNN --note "…"`，再跑 `python tools/qc.py escapes <剧>` 看「为什么没抓到」，按动作补检查或收紧。**新检查默认加在剧级**。
- **用户放行闸门拦下的结果**：`python tools/qc.py override <出片目录> --check <id> --kind accept|false_positive --note "用户原话" --followup NNN`。`accept`＝检查判对了、用户接受这次的瑕疵；`false_positive`＝检查判错了，多次误报才放松或改写那条检查。放行绑定产物与检查定义，检查一改即作废、不沿用；一句用户原话只管一类检查（同一句放行另一类要 `--mention` 原话里点到这一类的字），泛化的授权（如「你自己按 best effort」）不能拿来逐项放行。
- **升仓库级**：同类问题在两部以上的剧反复出现，先列证据交用户；用户明确同意才改仓库级登记表（写 `basis`），并记 follow-up。
- 改任何登记表都用 `followup.py` 记 changelog；进度看管理站「工作流 › 1.0.4 自检与进化」（仓库级）与剧页「🔍 流程与自检」（剧级）。
