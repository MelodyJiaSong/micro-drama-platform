# ep03 调研任务说明（给调研子代理）

今天是 2026-11-03。系列：YouTube 英文数据视频「排行榜」第 3 期 —— **30 家知名 AI 原生公司，按成立年份从老到新逐个介绍（不排名）**。每张卡：公司照片满版 + logo + 创始人圆形头像；大号主数字 = 最新估值（或上市公司的市值），小字 = 成立年、总部、代表产品。画面语言英文。

## 每家要查清的事实（只收有出处的；查不到写 null，不要猜）

- `name`：屏上用的通用名（如 "Anthropic"、"Cursor (Anysphere)"）；`legal_name`
- `founded`：成立日期（至少到年，尽量到月），`founded_source`（URL）。公司官网 / 公司注册 / 权威媒体优先；Wikipedia 只作交叉核对
- `hq_city`、`country_iso2`、`country_name`（总部所在国；如 ElevenLabs 这种多地的，写法律总部并在 notes 说明）
- `founders`：全部联合创始人 `[{"name","role_now"}]`；`headshot_founder`：卡上放哪一位（通常现任 CEO 或最有代表性的创始人），并说明理由
- `category`：从 LLM / Image / Video / Voice & Music / Coding / Search / Robotics / Platform / Avatar video / Research 里选 1–2 个
- `products`：代表产品 1–3 个（≤ 24 字符一个，如 "ChatGPT"、"Claude"、"Gen-4"）
- `valuation`：最新一轮私募的投后估值，或上市公司最近市值；`{"usd": 数字, "display": "$183B", "kind": "post-money"|"market cap"|"reported talks"|"n/a", "date": "YYYY-MM", "round": "Series F" 等, "source_name", "source_url", "tier": "primary"|"aggregator"}`。只收**已完成**的融资或官方公告；「洽谈中」的报道单独放 `valuation_talks`，不当主值。子公司（如 Google DeepMind）写 kind="n/a" 并说明母公司。
- `valuation_cross_check`：第二个独立来源（不同媒体），`{"source_name","source_url","usd"}`
- `employees`（可选，带出处）、`total_funding`（可选，带出处）
- `status`：截至 2026-11 是否独立运营；被收购、核心团队被挖走、改名、上市等都写清楚并带出处
- `fun_fact`：一条观众可能不知道、有出处的事实（英文，≤ 90 字符），可作洞察卡候选，附 `fun_fact_source`
- `brand_hints`：官方品牌素材 / press kit 页面 URL、官网创始人介绍页 URL、官网 newsroom 图片页（只给页面链接，**不下载、不找图片文件**；图片由另一路 Codex 搜）
- `notes`：口径疑点、来源冲突（差异 > 10% 必写）

来源优先级：公司官方公告 / 博客 / 交易所文件 → Reuters、Bloomberg、FT、WSJ、CNBC、TechCrunch、The Information、财新、36氪 等 → Wikipedia（只交叉核对）。不要用内容农场。每个 URL 都要是你真的打开或在搜索结果里看到的页面。

## 替补

如果某家已被收购、基本停摆，或你判断它在 2026 年已明显不算「知名」，在 `replace_suggestion` 写一句理由并给一个同领域的替补候选（替补也按上面字段查好）。

## 输出

把结果写成 JSON 文件（UTF-8、缩进 1）：`{"companies": [ ... ]}`，路径见你的任务。最后回复里只给：写了哪个文件、每家一行（name / founded / valuation display+date / status 是否有异常），以及所有查不到或有冲突的项。
