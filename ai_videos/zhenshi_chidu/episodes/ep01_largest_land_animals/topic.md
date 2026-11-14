# ep01 · 世界最大陆地动物 Top 30 · 按肩高 · 真实尺度

| 项 | 内容 |
|---|---|
| 题目（英文画面） | The 30 Largest Land Animals, Ranked by Height — True Scale |
| 物种范围 | 与排行榜 ep04 相同：体重前 30 的现存野生陆地动物（`ai_videos/paihangbang/episodes/ep04_largest_land_animals/data.json`） |
| 主口径 | **肩高**（用户定，follow-up 001）：典型成年雄性；只有雌雄混合数据的，卡上写「adults, both sexes」 |
| 并列 | 肩高相同并列同名次（卡上 `=9`），名次内按体重排 |
| N | 30（5 组并列：=9、=15、=19、=22、=28） |
| 人体参照 | 1.75 m（用户定），画面标「1.75 m man」 |
| 数据 | `data.json`（由 `_tools/make_ep01_data.py` 生成）、`sources.md`、调研 `0_research/ep01_animal_dimensions.*` |

## 为什么值得做

- 排行榜 ep04 已经做过「体重」版本；同一批动物换成肩高并放进同一个 3D 画面，排名大洗牌（河马体重第 6，肩高第 18；长颈鹿体重第 8，肩高第 1），有新信息。
- 同类 3D 尺寸对比频道大多手工摆放、尺寸不注出处；本片每只动物由脚本按出处数值缩放并机检（误差 ≤ 2%）。

## 模型可得性（bible §4.1）

- 30 只全部用第 3 档 AI 兜底：Codex 正侧面参考图 + 本地 TripoSR（MIT），卡上标 `AI MODEL`。
- 原计划 16 只走开放库（Sketchfab / Poly Pizza 的 CC0 / CC-BY 候选，见 `0_research/model_sources.md`）。这两个库自动下载都要 API key；用户 2026-11-07 要求「继续做直到成片完成」，代理决定这 16 只也走同一 AI 流程：
  - 全片风格一致；不涉及 CC-BY 署名链；许可全部为自产。
  - 以后要换开放库模型，按 `data.json` 的 `model` 字段逐只替换后重跑即可。
- 不用近缘物种替代（follow-up 002）。
