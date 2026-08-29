# ai_video_eval — AI 短剧分镜 prompt 评测系统

独立运行的分镜 prompt 质量评测框架：用**冻结的分层 rubric**（v3：6 维度 → 15 核心字段，全量 v1 存于 `rubric/archive_v1/` 供逐步加回）对 `ai_videos/` 各剧的 `shotNN.md` 逐镜打分——主观字段由 LLM 评审（Anthropic API 直连，逐字段 1–5 分 + 置信度 + 证据引文 + 修改建议），机械字段由确定性规则代码判定，全部结果经**非 LLM、完全确定性的聚合层**汇成 镜/集/全剧 三级判定与可机读的发现清单，供后续修订 agent 消费。

**100% 独立**：运行时不读 `.claude/`、`CLAUDE.md` 或任何仓库级配置；只读 `config/eval_config.yaml`、本目录 `.env` 与被评的 `ai_videos/{project}/` 产物；绝不写入 `ai_videos/`。

## 快速开始

两种评审引擎（`config/eval_config.yaml` 的 `judge.engine`）：

- **`claude_code`（当前默认）**——headless `claude -p` 子进程跑在你的 Claude 订阅上，**无需 API key**。独立性照旧：子进程工作目录在系统临时目录（不加载本仓库 CLAUDE.md/skills/MCP）、禁用全部工具、纯 prompt 评审。
- **`api`**——Anthropic API 直连（schema 强制输出、effort 可控）。需要 `cp .env.example .env` 并填入 key（platform.claude.com → API Keys，需 API 账户与充值）。

```bash
cd projects/ai_video_eval

PY=../../.venv/Scripts/python
$PY -m apps.cli.main rubric validate
$PY -m apps.cli.main estimate --project wushen_juexing --ep 8
$PY -m apps.cli.main run --project wushen_juexing --ep 8 --budget 50
$PY -m apps.cli.main report --project wushen_juexing
```

注：成本估算/预算按 API 价格口径；`claude_code` 引擎下实际花费的是订阅用量（报告成本≈$0），预算门只在 api 引擎下有实际意义。

常用参数：`--shot shot03`（选镜）、`--dimension renderability`（选维度）、`--samples 1`（降本筛查）、`--dry-run`（只跑规则字段、零 API 调用）、`--full`（忽略增量、全部重评）。

## 命令

| 命令 | 作用 |
|---|---|
| `run` | 评测并产出 `runs/{run_id}/`：manifest、原始评审输出、逐镜结果、verdicts.json、findings.json、中文 report.md，并更新 `runs/latest/{project}.json` |
| `estimate` | 零调用成本估算（含提示缓存折扣口径） |
| `report` | 打印最近（或指定）运行的中文报告 |
| `trends` | 跨运行维度分数走势 + 高频失分字段 |
| `dispute` | 对某个 finding 提出异议，写入 `disputes/` 并累积 `golden/golden.jsonl`（金标集） |
| `rubric validate` | 校验 rubric 可加载、规则可执行 |

## 机制要点

- **判定层级**：pass / conditional_pass / fail / needs_canon_fix（canon 自相矛盾导致无法判定时）。加权平均 + 存疑占比阈值 + **gate 一票否决直达顶层**——gate 字段（如 ≤2000 字符、语速上限、比喻词禁令等硬契约）是二元 通过/不通过，任何一镜 gate 未过，该镜、该集、整个项目判定全部 FAIL（rollup 带 `gate_failed_units` 列明肇事镜）。
- **每次评测都是全新开始（2026-07-29）**：无增量、无沿用、无判分缓存——每次 `run` 对选中范围全量重新评审，结果只取决于当下的 产物 + rubric + 配置，语义最清晰；每次运行仍留全量可复算记录（manifest 含输入哈希与 rubric 版本）。
- **每字段 3 样本**取中位数、样本分歧压低置信度；canon 矛盾多数票 → 字段记 inconclusive。
- **预算**：跑前估算拦截 + 跑中硬停（已完成部分照常落盘）。

## 结构

DDD 分层（apps/cli + libs/{domain,infrastructure,application,common}），rubric 数据在 `rubric/`，运行产物在 `runs/`（gitignored）。详细需求见 `docs/spec.md`；下游消费契约见 `docs/handoff_contract.md`；访谈记录见 `docs/interview.md`。

## 门户 UI

`ai_video_management` 门户（侧栏「🧪 评测」）提供本系统的 Web 视图：结果只读浏览（判定/明细/发现/报告）+ Rubric 与 `eval_config.yaml` 在线编辑（保存即跑 `rubric validate`、失败回滚）。门户只消费本项目的文件面；本项目对门户无感知，评测触发仍只在 CLI。

## Rubric 演进

`rubric/` 当前为 `3.0.0`（2026-07-29 按用户方向精简：去掉 忠实剧本/戏剧效果/立足原文 三维（并非所有短剧都有原文）、去掉确定性 <95% 与复杂的 check，每维保留 2–3 个核心 check，共 15 字段）。全量 v1（9 维 / 133 字段，2026-07-28 从各审查 skill 提炼）快照在 `rubric/archive_v1/`——加回某个 check＝把它从 archive 复制回对应维度文件 → `rubric validate` → 升版本号。每份判定都盖 rubric 版本+内容哈希，跨版本对比会被标记。争议（dispute）是 rubric 校准的主要输入。
