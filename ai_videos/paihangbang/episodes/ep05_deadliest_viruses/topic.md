# ep05 · 历史上致死人数最多的 30 种病毒（Top 30）

> 2026-11-03 代理起草（用户：「历史上杀死人类最多的前30病毒」「开始你的research和制作吧」，follow-up 013 / 016）。**口径与名单待用户点头**。
> 原定 ep04，与同时开工的陆地动物期撞号，按 follow-up 登记顺序改为 ep05（012 动物 = ep04，014 漫画 = ep06）。
> 数据：`data.json`（`_build/build.py` 生成）；出处与推算：`sources.md`、`_build/cumulative.py`；调研原始结果：`_build/research/group_{a,b,c}.json`。

- 英文标题（≤60 字符）：**Deadliest Viruses in History | Top 30 by Death Toll**（51 字符）
  - 屏上：标题「Deadliest Viruses in History」· kicker「TOP 30」· 统计行「Deaths · est. = modelled estimate · years vary by virus · Nov 2026」· 来源行「Sources: WHO, UNAIDS, CDC, GBD (Lancet), peer-reviewed studies」
- 指标与口径（**本期最关键的决定**）：
  - 只收病毒，鼠疫、结核、疟疾、霍乱等细菌 / 寄生虫不收。同一病毒的多次大流行合并（流感 = 1918/1957/1968/2009 四次大流行之和）。
  - 主值 = **有出处的最好死亡数估计**，每张卡写明自己的统计窗口（卡上国家行改成「Deaths · 1900–1977」）：
    1. **已发表的累计估计**（屏上 `est.`）：天花 1900–1977 约 3 亿（Henderson）、流感四次大流行之和、HIV 4,420 万（WHO/UNAIDS 2026-07）——本身是模型估计，按第 1 轮审片 D2 标 est.。
    1b. **计数总和**（屏上不带标）：报告 / 登记的死亡人数之和，如埃博拉历次疫情、MERS、SARS、马尔堡、尼帕，以及单国登记数（徽章 ONLY）。
    2. **推算累计**（est.）：只有年度估计的病毒，取同一来源体系（GBD 或 WHO）≥2 个年度锚点，逐年线性插值求和，窗口为全球估计能支撑的最长区间（多为 1990–2024），屏上标 `est.`，取 2 位有效数字。
    3. **报告数**（reported）：新冠用 WHO 报告死亡 712 万；超额死亡 1,480 万–2,850 万写在洞察卡和描述框。
  - 病毒引起的晚期并发症算进去：乙肝 / 丙肝含肝硬化与肝癌；HPV 只算宫颈癌（因此是下限），EB 病毒、卡波西肉瘤病毒算归因癌症死亡，卡上徽章 `CANCER DEATHS`。
  - 罕见病毒只有单一国家的总数时，照用并在卡上标徽章（`CHINA ONLY` / `US ONLY` / `RUSSIA ONLY` / `TURKEY ONLY`）。
  - **不进榜**：脊灰、风疹、腮腺炎、CMV、单纯疱疹、HTLV-1（只有病例或无全球死亡估计）；人偏肺病毒、副流感、腺病毒（只有单一年份的儿童估计）；丁肝（死亡并入乙肝）；拉沙热（只有「每年约 5,000」的粗估，没有总数）；寨卡、基孔肯雅（全球死亡数零散）。
  - 已知局限（洞察卡和描述框都说明）：窗口不一致，所以这是「有记录的死亡」排名，越古老、越被忽视的病毒越被低估；第 2–4 名（流感 5,240 万、HIV 4,420 万、麻疹约 4,300 万）方法不同、差距在误差内。
- N / 每名秒数 / 预计时长：N = 30，卡宽 720（电镜图多为横幅），每名约 6.3 s，7 张洞察卡；片头 5 s + 滚动约 3:30 + 冠军 10 s + 计分板 7 s + 来源 4 s + 片尾 18 s，**实际 4:18（短于 bible 5–8 分钟目标；Top 30 按用户要求，不加长）**。
- 主源与交叉核对：WHO 情况说明书 / 全球报告、WHO/UNAIDS HIV 统计、CDC、ECDC、GBD 2019/2021（Lancet 系列及以 GBD 为数据的同行评审论文）、GLOBOCAN 2024、各病种文献。维基百科一般只作交叉核对；例外：西尼罗病毒主值 2,330 = CDC 1999–2018 年度死亡数之和，由维基百科表格转引——CDC 页面拒绝脚本访问，标 aggregator）。数值属事实，不搬运文字与表格。
- 国家归属口径：**不挂国旗**。病毒没有国籍，挂「首次发现国」容易被读成甩锅（WHO 2015 命名准则也避免地名），发现地本身也常有争议。卡片左上不放国旗（渲染器 `layout.flags = false`），计分板改按**传播途径**累计（Airborne 7 / Mosquito & tick 6 / Contact 5 / Blood & sex 4 / Food & water 4 / Animals 4，各组有自己的图标）。
- 主题皮肤「virus」：近黑底 `#05080d → #10202a`；强调色生物危害绿 `#7CFF6B`（名次、窗口行）；洞察卡浅绿底深字；占位图标 `virus`；小标签图标 `virus`（病毒科）、`vaccine`（疫苗年份）。
- 主图（follow-up 016 / 024 / 034 / 038）：19 张为可商用实拍电镜图（CDC PHIL 原始 TIFF、NIH / NIAID、Unsplash 上的 NIAID 原图）；11 张为 AI 插画（Codex image_gen）：登革、水痘、乙脑、卡波西、戊肝、手足口、蜱传脑炎、甲肝、EB 病毒、乙肝（这 10 张以 Claude 依 RCSB PDB 原子坐标渲染的结构图为参考），SARS（只有文字 prompt，没有完整病毒粒子结构）。卡上署名「Illustration: AI-generated …」，描述框注明，上传时合成内容声明选 Yes。
  - **代理自主决定（用户夜间授权 follow-up 038）**：第 2 轮审片 N3 认为乙肝（PHIL 10755）、EB 病毒（PHIL 10234）、SARS（PHIL 3466）有可用的 CDC 实拍图，换成 AI 违反「AI 最后手段」。代理判断这三张实拍图不满足用户「每个 tile 都要高质量图」：乙肝主体只占画面角落、大半是空底；EB 病毒是颗粒很重的黑白组织切片；SARS 是黑白负染。按用户「网上找不到合适的高清图才交给 Codex」保留 AI 插画；原图在 `_build/reselect/cand/`（04_05_hbv/h10755、11_12_ebv/p10234、26_27_sars/p3466），用户若更看重「实拍」可直接换回（改 data.json 的 image 与 assets.json 后重渲）。
- 洞察卡（7 条，已写入 `data.json`，均有出处；第 1 条为读法说明，审片 D2 后加）：
  0. after #30：How to read: est. = modelled estimate, no tag = counted deaths. Years differ per card.
  1. after #27：Rare viruses are barely tracked: several counts here cover only one country.
  2. after #22：Ebola, SARS, MERS and Marburg together killed fewer than 18,000 people.（15,514 + 774 + 960 + 561 = 17,809）
  3. after #16：Rabies is almost always fatal once symptoms start, yet a vaccine has existed since 1885.
  4. after #8：COVID-19's reported toll is 7.1M. Excess-death studies put it at 15–28M.
  5. after #4：Measles and HIV are neck and neck, and measles is only counted from 1980.
  6. after #2：Smallpox is the only human disease ever eradicated. Its last natural case was in 1977.
  - 备选：1918 年流感估计 1,740 万–1 亿，差 6 倍；麻疹「150 年 2 亿」流传甚广但找不到原始出处；丙肝 2015 年起可治愈（>95%）；狂犬病按 WHO 口径每年约 5.9 万，是 GBD 的 4–6 倍。
- 竞品同题与差异：YouTube 上「deadliest viruses / pandemics in history」类视频很多，多数把鼠疫、霍乱等细菌混进「病毒」，数字无出处或互相矛盾（天花 3 亿 / 5 亿、麻疹 2 亿）。我们的差异：只收病毒；每个数字带窗口和出处，推算值标 est.；把「有据总数」和「推算」分开；揭示被低估的地方（单国计数、只算宫颈癌）。（竞品播放量未实测，发布前补。）
- 例外（待用户认可）：6 条单国计数（乙脑、汉坦、手足口、西尼罗、蜱传脑炎、克里米亚-刚果）统计窗口早已结束，不符合 bible §3.3「主值超过 18 个月未更新的不用」——这些病毒没有更新的全球或累计数，作为本期例外保留并在卡上标 ONLY 徽章。
- 风险：
  1. **口径争议**：窗口不一致、GBD 与 WHO 差 2 倍（乙肝、丙肝、狂犬病），评论区会有人纠错——sources.md 逐条列了替代值，描述框放口径说明。
  2. **广告友好度**：死亡 / 疾病题材属「敏感事件」边缘；全片无血腥画面，电镜图为主，洞察卡讲疫苗与根除，偏教育。新冠部分按 WHO 数据陈述，不涉阴谋论。
  3. **图片**：HPV、KSHV、丁肝等找不到公开电镜图（调研结论），预计需要 Codex 生成插画，账本标 AI 生成，上传勾合成内容声明。
  4. 发布前 7 天复核：WHO 新冠数据、MERS（ECDC 月报）、HIV（UNAIDS 年中新版会改写全序列）、麻疹（WHO 每年 11 月发布新估计）。
