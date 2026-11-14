# ep19 调研子任务说明：各国 2024 年国际入境过夜游客数（按 UN Tourism 口径）

背景：排行榜视频「Top 50 Most Visited Countries in the World」，指标 = **UN Tourism（原 UNWTO）口径的 international tourist arrivals（入境过夜游客，overnight visitors），统计年 2024**（2025 法、英、德等仍缺，所以全榜用 2024）。

## 已有资料

- UN Tourism Statistics Database 2025-12 批量下载（一手），参考表在本目录 `ref_<组>.md`（单位：百万）：
  - `TOUR` = inbound overnight visitors (tourists)，即 UN Tourism 的 international tourist arrivals 主序列；
  - `VSTR` = 全部入境访客（含当日往返）；`COMM_GUES` / `HOTL_GUES` = 商业住宿 / 酒店的外国住客到达数。
  - 注意：很多国家的 `TOUR 2019` 实际就等于 `COMM_GUES 2019`（奥地利、荷兰、克罗地亚、丹麦、瑞士、瑞典、挪威、阿联酋、德国……），说明 UN Tourism 对这些国家用「外国人住宿到达数」（TCE）作 arrivals；日本、韩国、台湾、哈萨克斯坦等 TOUR = VSTR（总访客，按 JNTO 等口径）。**这个「2019 指纹」就是判断 UN Tourism 对该国用哪个序列的依据。**
- 数据库里**有 2024 TOUR 的国家**：主值就用数据库值；你只需找**一个本国官方来源**（统计局 / 旅游部 / 央行）的 2024 值做交叉核对，并确认 2019 同口径值。
- 数据库里**没有 2024 TOUR 的国家**：在本国官方来源里找与 UN Tourism 同一序列（看 2019 指纹）的 2024 值作主值，并给 2023、2019 同口径值；再找一个第二来源核对（UN Tourism 新闻稿 / Barometer 摘录、Eurostat、各国另一机构、可靠媒体转引官方数字均可）。

## 每个国家要交的字段（写进 JSON 数组，一国一个对象）

```json
{
  "country": "France", "iso2": "FR",
  "in_un_db_2024": false,
  "series": "TF overnight visitors at frontiers | TCE non-resident arrivals at all commercial accommodation | THS hotels | VF all visitors | 说明",
  "v2024": 102.0, "v2023": 100.0, "v2019": 90.9,          // 百万，尽量保留原始精度
  "v2024_source": {"name": "...", "publisher": "...", "url": "...", "published": "2025-05-..", "quote": "页面原文里含该数字的一句（≤200 字符）"},
  "v2019_source": {"name": "...", "url": "...", "quote": "..."},   // 与 2024 同口径；若来自参考表就写 "UN Tourism DB TOUR 2019"
  "cross_check": {"name": "...", "url": "...", "value_2024": 101.5, "quote": "..."},
  "v2025_prelim": null,                                   // 若有官方 2025 全年值顺手记下（只作备注，不作主值）
  "series_break": "2019 与 2024 是否同口径；不同就说明并给出同口径 2019 值或写 null",
  "notes": "口径坑：是否含本国侨民 / 当日游 / 邮轮 / 过境；与常见榜单数字不同的原因；有争议写清"
}
```

要求：
- **只用 WebSearch / WebFetch**（先用 ToolSearch 加载）；不要调用 Codex、不要调用任何收费服务、不要生成图片。维基百科只能作线索，不能作主值来源；主值与 2019 值要落到官方 / UN Tourism / 统计局页面或 PDF（找不到官方页时，可用引述官方数字的权威媒体或 UN Tourism 新闻，并在 notes 写明）。
- 每个数字都要有 URL 和原文引句；拿不准写 null 并在 notes 说明，**不要编造**。
- 先把 TOUR 2024 已有、明显 < 3.5M 的小国跳过（不可能进 Top 50）；但参考表里没有 2024 的、可能 ≥ 4M 的国家都要查。
- 只写你被指定的那一个输出文件（`_build/research/<组>.json`，UTF-8，合法 JSON）；不改其他文件。
- 完成后回复 ≤150 字：查了几国、哪些找不到、哪些口径有大坑。
