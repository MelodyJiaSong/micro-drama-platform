# ep01 · 世界最高建筑 Top 50（已建成，2026 年 11 月）

> 2026-11-03 代理起草（用户授权自主决策，**待用户点头**）。数据与图片见同目录 `data.json`、`sources.md`、`assets.json`；构建脚本在 `_build/`。

- 英文标题（≤60 字符）：**World's 50 Tallest Buildings (2026)**（36 字符）
  - 屏上：kicker `TOP 50`，标题 `World's Tallest Buildings`，口径行 `Completed buildings, Nov 2026`，来源行 `Data: CTBUH Skyscraper Center, Wikidata (CC0)`。
- 指标与口径：**建筑高度（CTBUH architectural height）**，即从最低的重要露天步行入口量到建筑的建筑顶端，**含尖顶（spire），不含天线、旗杆、信号设备**。只收 CTBUH 状态为 **Completed** 的**建筑**（须有可连续使用的楼层；东京晴空塔、CN Tower 这类塔不算建筑）。
  - **CTBUH 标为 Architecturally Topped Out 的不收**，即便当地已经开业：重庆陆海国际中心（458.2 m，2025-09 开业，CTBUH 仍是 topped out）和山东国际金融中心（428 m，CTBUH 预计 2026 年竣工）。Wikipedia 已把这两座列进榜单，见「风险」。
  - 吉达塔、Burj Binghatti、Marina 106、成都熊猫塔（天府中心）等都**未完工**，不在 CTBUH 已建成榜内，不收。
  - 同高同名次（CTBUH 竞争排名 1,2,2,4）：第 8（广州周大福 / 天津周大福 530 m）、第 20（双子塔 1/2 451.9 m）、第 22（苏州国际金融中心 / 紫峰大厦 450 m）。同名次内按名称字母序。第 50 名深业上城 T1 388.05 m，第 51 名 30 Hudson Yards 387.07 m，切线处没有并列。
  - 显示值取整到米（3 位有效数字）。如果两座**不同名次**的楼取整后数字相同（如 Willis 442.14 / KK100 441.8），这几座改显示 1 位小数，避免观众以为数据出错。英尺用 CTBUH 公布的英尺值。
  - 「NEW 2025 / NEW 2026」角标（D2）给 CTBUH 竣工年为 2025 或 2026 的楼：JPMorganChase Tower、紫金金融大厦（南京金融城二期）、宁波中心 T1、招商银行全球总部，共 4 座；Top 50 里没有 2026 年竣工的楼。
  - 本期没有上一期可比，所以不标 ▲▼。D2 只用 NEW 角标和洞察卡来做。
- N / 每名秒数 / 预计时长：N = 50；第 50→11 名每名约 5 s（40 × 5 = 200 s），前 10 名每名约 7 s（70 s），冠军另停约 6 s，5 张洞察卡各约 3.5 s（≈18 s），片头 5 s，国家计分板 7 s，来源卡 4 s，片尾 18 s。**合计约 5:28**，落在 bible 要求的 5–8 分钟里。
- 主源与交叉核对源（许可已核？）：
  - 主源：**CTBUH Skyscraper Center**「The 100 Tallest Completed Buildings in the World in 2026」，2026-11-03 抓取。只引用事实（名称、城市、高度、层数、竣工年），注明出处，不整表搬运网页的版式和文字。CTBUH 的使用条款（ToS）没有细看，作为 **待核** 留给用户。事实本身不受版权保护，但 CTBUH 数据库可能受合同条款约束。
  - 交叉核对：**Wikidata**（CC0）P2048 / P1101 / P1619 / P17；Wikidata 缺高度的 4 座用 Wikipedia「List of tallest buildings」核对。Wikipedia 本身引 CTBUH，**不算独立来源**，sources.md 已标明。
  - 50 座里 47 座差异 ≤0.5%。3 座超过 0.5%（麦加皇家钟塔 +1.0%、武汉中心 −1.2%、民盈国贸 T2 +1.0%），都是 Wikidata 用了另一种高度口径或设计高度，sources.md 有逐条说明。
- 国家归属口径：**建筑所在地**的主权国家。香港 → `CN` China，副标题写「Hong Kong」；台北 101 → `TW` Taiwan（和 ep02 的「名单含台湾」口径一致）。计分板按 country_iso2 计数，所以香港的 2 座算进中国。洲：俄罗斯（圣彼得堡）→ Europe，埃及 → Africa，美国 → North America，其余 → Asia。
- 主题皮肤（`theme: skyline`）：
  - 背景：深夜空蓝黑渐变（#0B1020 → #141B33），底部加一条很淡的城市天际线剪影。
  - 卡片：深石板色（#1C2340），1 px 冷灰描边。
  - 强调色：暖琥珀色（#FFB547），用于数值、名次和冠军光效；NEW 角标用青绿色（#3DDC97）。
  - 主图：Commons 实拍外观照片，竖图居多，卡片按 4:3 或方形裁切，以塔身中上段为焦点。
  - 主题图标：`building`（数值左侧），小图标行用 `stairs`（层数）和 `calendar`（竣工年）。
  - 国旗：固定位置的国旗条（默认样式）。
- 洞察卡候选（≥5 条；已入 data.json 的打 ✔，均对照 data.json 核过）：
  1. ✔ after 41：「4 of the world's 50 tallest buildings were completed in 2025 alone.」
  2. ✔ after 31：「Shenzhen and New York City tie for the most towers in the top 50: 6 each.」
  3. ✔ after 19：「15 of the top 50 were completed in 2020 or later.」
  4. ✔ after 11：「Only 8 of the top 50 stand in the Americas, all of them in the United States.」
  5. ✔ after 4：「Only 4 completed buildings on Earth rise higher than 600 m.」
  6. 备选：「The oldest tower in the top 50 is Chicago's Willis Tower, completed in 1974.」
  7. 备选：「Only 11 completed buildings reach 500 m or more.」
  8. 不用：「China has 26 of the top 50」。这个数会提前剧透结尾的国家计分板（D3），留给计分板揭晓。
- 竞品同题（播放为 2026-11-03 yt-dlp 检索快照，见 `0_research/data/yt_search_mountains_buildings_2026-11-03.jsonl`）：

  | 视频 | 频道 | 播放 | 时长 | 链接 |
  |---|---|---|---|---|
  | Top 50 Tallest Buildings in the World 2023 | Gravity | 6,842,963 | 4:23 | https://www.youtube.com/watch?v=unmQoX5a_20 |
  | Top 50 Tallest Buildings in the World 2026 | GLOBAL TARGET | 255,255 | 4:27 | https://www.youtube.com/watch?v=efzQCwCG5OY |
  | Tallest Buildings by Country Ranking | OnTheWeb | 9,398,983 | 10:47 | https://www.youtube.com/watch?v=eOAmOrzKVJg |

  （发布时间未在检索快照里抓到，待补。）

  我们的差异：
  - 口径写明，每个数字可追到 CTBUH（D1）。
  - 2025 年新上榜的 4 座标 NEW（D2），这是 2023 年版的竞品里没有的信息。
  - 结尾国家计分板揭晓（D3）。
  - 5 张洞察卡（D4）。
  - 竞品常把晴空塔、CN Tower 这类塔混进来，或者收录未完工的楼；我们严格只收 CTBUH 已建成的建筑，并在描述框说明口径。
- 风险：
  1. **全景自由（FoP）**：50 座里有 9 座位于商业用途没有 FoP 的国家：阿联酋 4、韩国 2、科威特 1、埃及 1、越南 1。这些建筑的照片用于有收益的视频，理论上要建筑师授权。Commons 上标了 {{NoFoP-…}} 的文件一律跳过；没有这个标、也没有删除请求的文件，仍在 `fop_note` 里标「RISK」。**发布前须人工决定**：保留、换成更远的天际线图、还是改用剪影。详见 sources.md「FoP」。
     - 选图结果：50 座中 45 座有图，5 座 image=null，渲染器需要准备剪影或占位卡：乐天世界塔、LCT The Sharp（韩国，Commons 上可用的图只有打码版或带 NoFoP 标的）；Marina 101、Princess Tower（阿联酋，没有完工后的无标照片）；贵阳国际金融中心 T1（候选图塔顶都有塔吊，认不准是哪座楼）。
     - 有图但标 RISK 的 5 座：Burj Khalifa、23 Marina（阿联酋）、Al Hamra（科威特）、Iconic Tower（埃及）、Landmark 81（越南）。冠军卡 Burj Khalifa 的图是逆光远景，塔身偏小，构图偏弱，需人工复核。
  2. **竣工口径争议**：重庆陆海国际中心已开业，但 CTBUH 未改成 Completed。观众可能在评论区指出。描述框写「per CTBUH status as of 3 Nov 2026」，发布前 7 天内复核 CTBUH，若它改为 Completed 就排在第 18 名，后面名次整体顺延，并重渲染。山东 IFC 同理，会排在第 30 名附近。
  3. **名称**：吉隆坡第 2 名采用通行英文名「Merdeka 118」；CTBUH 官方名为 Menara Merdeka Maybank（Wikipedia 现标题 Merdeka Maybank Tower）。如果用户想用官方名，改 `_build/entities.json` 一处后重跑即可。其他按 CTBUH 名、改用通行名的见 sources.md。
  4. **CTBUH 条款**：数据库使用条款待核，见上文。
  5. **图片构图**：竖图裁成横卡后可能截掉塔顶。渲染器需要以塔身中上部为焦点，审片时逐张查看。
