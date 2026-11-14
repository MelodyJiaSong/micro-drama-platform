# ep04 调研任务说明（给调研子代理）

今天是 2026-11-03。系列：YouTube 英文数据视频「排行榜」第 4 期 —— **Deadliest Viruses in History: Top 30（历史上致死人数最多的 30 种病毒）**，按死亡人数倒数到第 1 名。每张卡：病毒电镜图满版 + 病毒名 + 大号主数值（累计死亡估计）+ 统计窗口 + 1–2 个小标签。画面语言英文。

## 只收病毒

鼠疫、结核、疟疾、霍乱、斑疹伤寒等**细菌 / 寄生虫一律不收**。同一种病毒的不同大流行（1918、1957、1968、2009 流感）合并在「Influenza」名下，分项数值记在 `components` 里。

## 指标口径（最关键，宁缺毋滥）

主指标 = **有出处的累计死亡人数估计**（病毒直接致死 + 公认由该病毒引起的晚期并发症，如乙肝/丙肝导致的肝硬化与肝癌、HPV 导致的宫颈癌等——但要分开记，`includes_cancer: true/false`）。

每种病毒按下面三层找，能找到的都记下来：

1. `historical_totals`：文献 / 权威机构给出的**历史累计**数字（如「天花 20 世纪致死约 3 亿」「HIV 自流行开始 4,410 万」「埃博拉历次疫情合计约 1.5 万」）。每条记 `{"value", "low", "high", "period": "1900–1977"（统计窗口）, "source_name", "source_url", "quote"（原文一句，≤ 200 字符）, "tier": "primary"|"peer-reviewed"|"aggregator"|"media"}`。
2. `annual_estimates`：近年**每年死亡**估计，至少两个时间点（如 WHO 2000 年与 2022 年；GBD 1990 与 2021），用于推算 1990 年以来的累计。每条 `{"year", "value", "low", "high", "source_name", "source_url", "quote"}`。
3. `cumulative_since_1990`：如果有论文或数据直接给出 1990（或某年）以来的累计数，记下；没有就写 null（不要自己算，代理会统一算）。

来源优先级：WHO 情况说明书 / 全球报告、UNAIDS、CDC、ECDC、国家卫生部门、Lancet / NEJM / Nature 等同行评审论文（含 GBD 研究）、Our World in Data → 维基百科只作交叉核对与找原始出处（**不能作为唯一来源**）。不要用内容农场、AI 生成站点、医疗营销站。每个 URL 必须是你真的打开过或在搜索结果里看到的页面；quote 要是原文。

## 每种病毒还要查

- `name_display`：屏上英文名（≤ 24 字符，如 "Smallpox (variola)"、"Hepatitis B virus"、"SARS-CoV-2 (COVID-19)"）
- `family`：病毒科（如 Poxviridae）
- `transmission`：从 `Airborne / droplets`、`Blood & sexual`、`Mosquito & tick`、`Food & water (fecal-oral)`、`Animal bite / contact`、`Body fluids (contact)` 里选 1 个主要的
- `discovered`：首次分离或鉴定的年份（及谁 / 在哪，带出处）；`earliest_evidence`：最早的人类感染证据（如木乃伊、古 DNA），带出处
- `vaccine`：有无获批疫苗、首个疫苗年份；`status_2026`：已根除 / 仍在流行 / 有新近疫情（2025–2026 的新数据要查）
- `fun_fact`：1–2 条观众可能不知道、有出处的事实（英文，≤ 90 字符），附 `fun_fact_source`
- `image_hint`：CDC PHIL（phil.cdc.gov）的图片 ID、NIAID Flickr 相册页、或其他公有领域 / CC BY 的**电镜图页面链接**（只给页面链接，不下载；没有就 null）
- `notes`：口径疑点、来源冲突（不同来源差异 > 2 倍必写）、是否容易和别的病毒重复计数

## 输出

把结果写成 JSON 文件（UTF-8、缩进 1）：`{"viruses": [ ... ]}`，路径见你的任务。最后回复里只给：写了哪个文件、每种病毒一行（name / 最可信的历史累计数字 + 窗口 + 来源名 / 最新年死亡数 + 年份），以及所有查不到或有冲突的项。
