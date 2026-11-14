# ep13 · 世界最高雕像 Top 41（只收已建成，按雕像本体高）

> 2026-11-03 代理起草（follow-up 015，用户授权自主决策，**待用户点头**）。数据见 `data.json`、出处与判断见 `sources.md`、图片账本 `assets.json`；生成脚本在 `_build/`（`items_def.py` → `build.py` → `gen_sources.py`）。

- 英文标题（≤60 字符）：**Tallest Statues in the World | Top 41 (2026)**（44 字符）
  - 屏上：标题 Tallest Statues in the World · kicker「TOP 41」· 统计行「Statue height · Completed statues, Nov 2026」· 来源行「Sources: builders, governments & news; Wikipedia cross-check」
- 指标与口径：
  - **雕像本体高**：人物 / 神像 / 动物形象从脚底（或坐姿底面）到形象最高点，**含手持物**（剑、火炬、锡杖）；**不含**莲花座、宝座、基座、内含建筑、山体。含基座总高放卡上标签（「240 m with base」）。
  - **只收已建成**：在建 / 规划（孟买 Ambedkar、柬埔寨 Bokor 108 m 大佛、越南广义观音、泰国纳黎萱王等）不收；已拆（荆州关公、巴米扬大佛）不收，荆州关公做洞察卡。
  - 卧像按长度计的不收（江西弋阳卧佛 416 m 长）；浮雕不收；胸像算雕像（炎黄二帝）。
  - 同高同名次（标准竞赛排名 1,1,3）。
  - **N = 41**：所有能核实到的本体 ≥ 49 m 的已建成雕像。名单底子是维基百科 List of tallest statues（收 ≥ 50 m，只作交叉核对与线索），逐条另找官方 / 建设方 / 新闻 / 旅游主管部门来源；维基漏收的不丹 Buddha Dordenma 补入；数值打架、只有含基座总高、建成状态不明的 9 项剔除（见 `sources.md` §2），不凑满 50。
- N / 每名秒数 / 预计时长：41 张卡 + 6 张洞察卡；卡宽 600，每名约 5.3 s，前 10 名约 5.7 s；片头 5 s + 冠军 10 s + 计分板 7 s + 来源 4 s + 片尾 18 s，**约 4:43**（`timeline` 实测）。
- 主源与交叉核对源（许可已核？）：每条主值有一个非维基来源（建设方 / 官方 / 政府旅游机构 / 新闻 / 百科性出版物），维基列表 revid 1382307847 作交叉核对；事实数据不受版权限制，只引数字不搬文字。主图全部 Codex 联网找，不用维基共享资源（follow-up 009）。
- 国家归属口径：**所在地**。香港计入中国（同 ep01）；台湾单列 Taiwan（同 ep02）。计分板按 country。
- 主题皮肤「monument」（渲染器已有）：深褐黑底 `#14110d`，青铜金强调色 `#d4a24c`；主图 = 雕像实景竖幅照片，焦点偏上 `[0.5, 0.2]` 保住头部；国旗角标。
- 洞察卡（6 张，已写入 `data.json`，依据见 `sources.md` §5）：
  1. after 37：The Statue of Liberty is 46 m from base to torch: too short to make this list.
  2. after 28：China now curbs statues over 30 m. Jingzhou took down its 58 m Guan Yu in 2021-22.
  3. after 20：Japan has 9 statues on this list, but the newest of them went up back in 1994.
  4. after 11：4 statues here were unveiled since 2022: in India, Thailand, the Philippines, Indonesia.
  5. after 4：Spring Temple Buddha is often listed at 128 m. That includes its 20 m lotus throne.
  6. after 2：Next: the Statue of Unity, 66 m taller than any other statue on Earth.
  - 备选：Motherland Calls 不带剑只有 52 m；Mother Ukraine 2023 年把盾上的锤镰换成三叉戟；加贺大观音 2026 年 4 月因航空障碍灯长期不亮被行政处分，存废未定；Christ the Redeemer 只有 30 m（含基座 38 m）。
- D2 变化信息：本题没有官方「上一期名次」，改用 badge：NEW 2022（Statue of Belief）、NEW 2023（The Victor、Wat Paknam）、NEW 2024（Sibea-bea 耶稣像）、SHIELD CHANGED 2023（Mother Ukraine）；洞察卡 2、3、4 讲「谁在新建、谁在停、谁被拆」。
- 竞品同题（需求证据：「tallest statues in the world」搜索前 15 条播放中位数 145 万、最高 5,828 万）：
  - Real Data《◄ Tallest statue size comparison ► 3d animation》约 5,828 万播放（3D 体量对比，2021 年前后，Nerdist / Artribune 2022-01 报道过）。
  - WorldTV Studio《World Tallest Statues size Comparison | Upcoming Tallest Statues》约 1,790 万播放（发布时间未取到）。
  - 我们的差异：D1 统一口径（本体高 vs 含基座总高分开显示；维基表里春泉大佛 128 m 含莲花座、拉开坤 115.8 m 不含，口径不一致——我们统一后冠亚军之后的名次会变），每个数字有出处；D2 新上榜与变化 badge；D3 国家计分板（中国 13、日本 9、泰国 5）；D4 洞察卡讲「自由女神进不了榜」「中国限高令与拆像」「日本 1994 年后没再建」。竞品都是 3D 体量动画，我们是真实照片 + 数据卡，形式不同。
- 待用户确认（代理已按默认处理）：
  1. **春泉大佛（中原大佛）排第 3 而非常见的第 2**：按「不含莲花座」统一口径，佛身 108 m < 拉开坤 115.8 m；若改为「含莲花座」，两者 128 m vs 129.2 m，拉开坤仍在前。默认保留，洞察卡 5 主动解释。评论区会有人纠正，sources.md 可直接指向。
  2. **Statue of Belief 改为本体 78.9 m（第 12），2026-11-04 依独立审片 qc #6 修正**：369 ft 是含 110 ft 台座的总高（维基正文、The Daily Guardian），351 ft 是施工期总高；本体 = 369 − 110 = 259 ft（推算）。原稿取 351 ft = 107 m 排第 4，已撤销。
  3. **南山海上观音 78 m 只有维基一个来源**（108 m 含莲花座与金刚台，各方一致）；九华山地藏取 2013 新闻的像身 84 m（维基 76 m，差 >10%）；Buddha Dordenma 取廷布宗政府 54 m（另有 51.5 m 说法）；Koxinga 取中央社 172 ft（52.4 m，维基 54 m）。
  4. 剔除 10 项（数值互相矛盾、只有总高或含莲座、建成未证实）：香港慈山寺观音（70 m 含三层莲座，像身高未公开，qc #7）、越南开元寺阿弥陀佛（72 m 含多层台座建筑，本体未公开）、菲律宾 Mother of All Asia（98.15 m 含其下建筑 / 台座，本体未公开，完工也有争议）、清莱观音（69/79/90 m）、太湖西山观音（67/88 m）、呵叻 Lung Por Tuad（59/111 m）、素攀 Phra Kakusunto（58/26 m）、Bodhi Tahtaung 坐佛（未证实完工）、越南 Ba Den 山观音（72 m 含基座，本体未知）、佛光山佛光大佛（40/48/50 m）。
  5. **全景自由（FoP）**：21 项所在国对雕塑无商用 FoP（中国现 12 项、全部 FoP 安全）（日本 9、台湾 2、菲律宾 1、缅甸 2、印尼 2、越南 1、俄、乌、不丹、塞内加尔），按 bible 标 `image_risk`。其中 10 项找到了可商用许可的照片，默认版用它作 `image_alt`（其余 11 项与另 9 项许可不明的图，默认版为占位卡，风险版有图；图片现状见 `_build/handoff.md`）——**但照片许可只解决摄影师的版权，雕塑作者的版权（FoP 问题）并不因此消失**，默认版仍带 FoP 风险，需用户发布前签字或改用占位。
  6. 日本、台湾的 FoP 条款只排除「以出售复制品为目的」，用于 YouTube 视频多数解读认为可以；按 brief 从严当风险处理。
- 风险：
  1. 数据层：维基表下半部分（50–60 m）原始出处薄弱，本期 7 项剔除、若干项只有旅游网站来源（赤山明神、宇佐美观音等），sources.md 逐项标明。可能还有维基与本期都漏收的 49–55 m 级雕像（泰国、中国地方寺院尤其多）。
  2. 版权层：见待确认 5。
  3. 发布前 7 天复核：孟买 Ambedkar 像（目标 2026 年内完工，若揭幕且本体 > 49 m 需加入）、加贺大观音存废。

- 2026-11-04 独立审片（qc.md「必须修」）后的修改：Statue of Belief 改值、慈山寺观音剔除（N 42→41）；默认版中、泰、墨 9 项占位改用 Codex 写实生成图（AI IMAGE 标记）；风险版炎黄二帝（真人合影）、赤山明神（保留权利）换生成图，东京湾观音、The Victor 换掉保留权利的图；Mother Ukraine 换成 2023 年后三叉戟盾牌的照片；Kyaikhto、会津观音、The Victor 调焦点；占位原因统一写真实原因。
