# ep19 handoff（子代理 → 主代理，2026-11-03）

## 做了什么

1. **调研**：主源 = UN Tourism Statistics Database 批量下载（2025-12 版；2026-05 版的入境表逐字节相同），`raw/UN_Tourism_inbound_arrivals_12_2025.xlsx`。数据库 2024 年只有约 67 个国家有 TOUR 值，法、土、希、泰、奥等缺，所以起了 3 个调研子代理按「2019 指纹」找本国官方同一序列（`research/brief_research.md`、`research/{europe,asia,africa_americas,extra}.json`，逐国来源 + 原文引句 + 口径坑）。中途 10 个代理共用的 WebSearch 额度用尽，部分交叉核对是额度恢复后主线补的（`items_def.py` 的 `CROSS`）。
2. **数据**：`items_def.py`（人工定稿表）→ `build.py` → `../data.json`；`gen_sources.py` → `../sources.md`；`topic.md` 手写。N = 50，冠军法国 100M（官方估计），第 50 名菲律宾 5.95M。D2 = 与 2019 同一序列的 ▲▼%（`secondary_display`）；巴林、爱尔兰序列断档改与 2023 比。大洲计分 Europe 20 / Asia 18 / North America 4 / Africa 4 / South America 3 / Oceania 1。洞察卡 5 张。
3. **找图第一步**：`landmarks.py`（每国一个标志性景点，优先自然 / 古迹，避开无 FoP 国家的现代建筑）→ `fetch_content.py`（维基纯文字摘要）→ `gen_content.py` 写 `content/NN_<slug>.md`；要点并入 data.json 的 `image_hint`。
4. **找图第二步**：follow-up 016 时先跑了共用 `image_reselect.py search`（Codex，b00–b07 完成，每项仅 2–3 个候选）；收到 follow-up 023 后立即停掉（b08/b09 未完成，未再调 Codex，`research_images.py` 写好但从未运行）。随后 3 个子代理用 WebFetch 在 Unsplash（少量 Pexels / Pixabay）补到每项 8–13 个候选（`reselect/claude_{a,b,c}.json`，直链均 curl 验证过）。download → score → 自制全候选拼图 `contact_sheet.py` → `reselect/sheet_01..10.jpg` **逐张看过**，人工选定 `picks_manual.json` → apply。
5. **图片结果**：50/50 可商用（Unsplash License 45、Pexels License 5），**无风险图、无 AI 生成图、无占位卡、无需补搜第三轮**。台湾改用太鲁阁（日月潭候选都灰蒙蒙）。香港天际线、新加坡滨海湾金沙为现代建筑，但两地版权法都允许拍摄公共场所建筑（assets.json `fop_note`）。
5b. **候选编号错位 bug 核查**（主代理通知）：本期只在 codex + claude 结果都到齐后跑过一次 download，没有旧文件残留；逐项核对 50 张上屏图 = assets.json source_url 对应候选（缩略图差异 < 1）、作者 / 许可一致，并抽 6 张重新从 source_url 下载比对（差异 ≤ 0.19 / 255），全部对应，无需重跑 download / apply。
6. **校验与预览**：`validate --strict` 通过；29 帧预览（`render/preview/`，`_grid*.jpg` 是我拼的 2×2 总览，拼缝处的重影是拼图造成的，不是渲染问题）亲眼看过：▲▼ 字形正常、文字不出框、国旗正确、裁切都保住了主体。
7. **渲染与包装**：见文末「产出」。

## 关键口径与默认（详见 topic.md / sources.md）

- 指标：UN Tourism international tourist arrivals（入境过夜游客），2024 全年；UN Tourism 本身混合口径（边境 / 住宿登记 / 含当日 / 含侨民），照搬并在卡上加小标签注明。
- 未入榜（缺 2024 同口径值）：中国、阿联酋、丹麦、保加利亚、俄罗斯（+ 卡塔尔、伊朗、老挝未核到）；波多黎各不列入（美国属地）。香港、澳门单列，badge SAR OF CHINA。
- 大洲按 UN M49（土耳其算 Asia）。
- 维基「World Tourism rankings」的中国 2024 = 64.9M 是移民局「外国人出入境合计人次」误用——洞察卡 3 就讲中国为什么不在榜。

## 没解决的问题

1. 交叉核对仍缺：加拿大（StatCan 只给含当日的 29.8M）、阿根廷、印尼、哈萨克斯坦、乌兹别克斯坦、巴林、约旦等只有 UN Tourism 数据库一个来源；希腊、奥地利、荷兰、挪威、柬埔寨的第二来源只做了部分核对。`sources.md` 标「未核到」，发布前 7 天复核时补。
2. 英国：UN DB 38.2M vs ONS Travel trends 2024 的 42.6M（2024 年中途换调查设计），未解决；不影响名次。
3. 法国 100M 是官方估计（Atout France），UN Tourism 正式值未见；有媒体称 2024 = 102M。
4. 菲律宾 5.95M（DOT，经 Manila Times 转引）vs 维基表 6.44M（引 DOT 年报 PDF，403 未核）；任一值都在第 50 名。
5. 竞品视频发布日期没取到（YouTube 要求登录）。
6. 静音母版，配乐由主代理做。

## 需要用户决定

见 `topic.md`「待用户确认」：标题年份 (2026) vs (2024)；中国等是否用估算补；波多黎各；大洲口径；英国用哪个数。

## 产出

- 默认母版：`render/ep19_most_visited_countries_master.mp4`，1920×1080，60 fps，H.264，**6:15（375.4 s）**，静音（含静音 AAC 轨），约 104 MB；manifest 同目录。第一次渲染在 23:42 被异常中断（exit 255，原因不明，可能是机器负载 / 外部结束进程），00:22–01:05 重渲成功（4.6 fps，10 个代理并发）。抽 40 s / 200 s / 340 s 三帧看过。
- **无风险版**：本期没有 image_risk 条目，不需要 `_with-risk-images` 版。
- 封面草图：`render/thumbnail.png`；预览帧：`render/preview/`；抽帧：`render/frames/`。
- `publish.md`：`rank_scroll publish --strict` 生成后经 `_build/fix_publish.py` 补标题（Most Visited Countries in the World | Top 50 (2026)，51 字符）、描述开头、话题标签、Tags；描述 4,7xx / 5000 字符；本片无 AI 生成图，合成内容声明选 No。
- 用户追加要求 5（质量优先、先全网找）到达时 50 张已选定：都是 ≥ 2,000 px 的高清实拍、经典机位、色彩好且可商用，按新标准逐张复看后认为无需升级，未再做全网检索；如主代理 / 用户认为某张一般，可指定再换。
