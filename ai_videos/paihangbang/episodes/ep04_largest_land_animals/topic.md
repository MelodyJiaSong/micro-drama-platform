# ep04 · 世界最大陆地动物 Top 30

> 2026-11-03 代理起草（follow-up 012 / 018），**待用户点头**。数据见 `data.json`，出处与判断依据见 `sources.md`；生成脚本 `_build/build.py` → `_build/gen_sources.py`。
> 按 follow-up 018 分两步：**① 内容先定稿**（本文件、`data.json`、`sources.md`，每张卡的找图辨认要点写在 `items[].image_hint`）→ **② 再按内容找图**（Codex 联网搜多张候选、逐张看图核对物种与画质；找不到合格真实照片的卡用 Codex 以真实照片为参考生成，标 AI 生成）。

- 英文标题（≤60 字符）：**Largest Land Animals in the World | Top 30 (2026)**（49 字符）
  - 屏上：标题 Largest Land Animals in the World · kicker「TOP 30」· 统计行「Typical adult male weight · wild species only · Data as of Nov 2026」· 来源行「Sources: IUCN Red List, peer-reviewed studies, zoo & reference works」（独立审片 M5 / m10 后改）
- 指标与口径：成年雄性典型体重，kg（副显示 lb）。**出处只给雄性范围的一律取该范围中点**（独立审片 M2 后统一：棕熊 130–550 → 340 入榜，加拉帕戈斯象龟 295 落到第 31）；非洲水牛改用 HMW（700，与班腾牛并列第 15；M1）；gaur 两性合并的 HMW 825 低估雄性（复审 N2），改回 Walker's 雄性 588–1,500 中点 1,044，卡上首位标「Estimates: 650–1,500 kg」（第 3 轮 R3-M1）。野生双峰驼因查不到野生雄性体重不排，口径说明写明（M4）。按 IUCN Red List 现行分类的**现存野生物种**；不收家畜 / 家养型、海兽、鳄类；收河马、北极熊；亚种不单列（Kodiak 熊归棕熊）。
- N / 每名秒数 / 预计时长：N = 30；卡宽 720（动物照片多为横幅），每名约 6.3 s；6 张洞察卡；预计约 4 分钟（`python -m rank_scroll timeline` 为准）。比 bible 建议的 5–8 分钟短，Top 30 是用户定的。
- 主源与交叉核对：象类 Larramendi 2016（同行评审）、犀牛 / 河马 / 长颈鹿 Owen-Smith 2024（百科全书章节）、牛科 IUCN SSC 专家组与 ASM《Mammalian Species》、ADW、圣地亚哥动物园资料库；维基百科只作交叉核对。逐条见 `sources.md` §2。
- 国家归属口径：**国旗 = 该物种野外个体数最多的国家**，卡上写「Most in Botswana」；大洲按国旗国家的 UN M49 分区。可信度 low 的：长颈鹿（KE / ZA / TZ 数据年份不一）、巨羚（CF）、邦戈（GA，无分国数据）、普通大羚羊（ZA 含私人猎场）、欧洲野牛（PL / RU / BY 相差不到 5%）。
- 主题皮肤「savanna」：深褐夜色渐变 `#1a1208 → #4a3214`，强调色琥珀 `#ffb02e`；主图 = 野外实拍满版；国旗左上飘动；计分板按大洲（结果：Africa 13、Asia 10、North America 4、Europe 3）。爪哇犀、苏门答腊犀卡写「Only in Indonesia」。
- 洞察卡（6 张，已写入 `data.json`，出处见 `sources.md` §4；独立审片后改写）：
  1. after 30：国旗规则说明
  2. after 26：第 31 名加拉帕戈斯象龟（约 295 kg）差一点入榜
  3. after 22：湾鳄（约 460 kg）本可排在这里，但本片把鳄类算作水生
  4. after 15：高棉牛（约 750 kg）本可排在这附近，但几十年来没有确认存活
  5. after 12：从这里起每一种的典型雄性都在 1 吨及以上（a tonne or more）
  6. after 8：长颈鹿专家已认定 4 种，红色名录仍按 1 种
  - 备选：只剩约 50 头爪哇犀，全在一个国家公园；非洲草原象的腿骨要到约 40 岁才长合，所以一直在长；北极熊在美国法律上算海洋哺乳动物。
- 竞品同题（`0_research/data/yt_search_land_animals_2026-11-03.jsonl`，4 个检索词 × 20 条）：搜索结果以纪录片和探访类为主，**没有搜到同格式（卡片滚动 + 国旗 + 数值）的「最大陆地动物 Top N」**；相近的有 Doctor NOS《The Largest Animals You Wont Believe Actually Exist!》162 万、Axtro Explainer《Elephants Species and Monsters Sizes Ranked》90 万、SR. RAVI《Top 10 Biggest Land Animals in History》57 万（含灭绝物种）。差异：① 只收现存野生物种、统一用雄性平均体重，逐条出处；② 每张卡带 IUCN 等级与野外数量（D2 的变体：谁在减少）；③ 国旗 = 野外最多的国家 + 大洲计分板；④ 洞察卡讲「为什么它不在榜上」。
- **非洲森林象 2,000 kg 的取值（独立审片 M8，代理 2026-11-04 夜间自主决定）**：沿用 Larramendi 2016（同行评审、按肩高与体积推算的雄性均值），不取 Owen-Smith 2024 表中 4,500 kg（百科章节、未说明方法）或网上 4–7 t（无出处）。理由：只有前者给出方法；没有任何实测称重，所以卡上加「Estimate: none weighed」标签，口径与描述框照写。若用户要取更大的值，它会升到第 3–4 名。
- 风险：
  1. **数值争议**：体重随种群差异大（驼鹿、棕熊、野牛），很多物种只有范围；第 27–31 名相差不到 5%。口径行写明「相差约 5% 以内视为并列」，评论区纠错可指向 sources。
  2. **出处偏弱**：IUCN 网站对脚本 403，部分 IUCN 类别 / 年份取自转载；gaur、African buffalo、giant eland、kiang、bongo 的雄性体重只有二手或百科级来源。发布前 7 天复核。
  3. **口径争议**：河马、北极熊收而鳄类不收，长颈鹿按 1 种——片头口径与洞察卡主动说明。
  4. **找图**（已按 follow-up 018 / 022 / 030 完成，见 `assets.json` 的 `selected_by`）：28 张为可商用实拍（Pexels / Unsplash / iNaturalist CC / 美国政府公有领域；#25 麋鹿第 3 轮审片后换成 iNaturalist 科罗拉多大公鹿，原图动物太小被文字盖住）；邦戈为美国动物园圈养个体（找不到可商用野外照）；爪哇犀、野牦牛默认版用维基共享资源博物馆标本图（用户特许），带风险图版用野外实拍（许可未知，发布前签字）。原计划：爪哇犀、苏门答腊犀、高原野牦牛、野水牛、班腾牛野外照片稀少，容易拿到家养型或圈养个体；第二步逐张核对，不合格的用 Codex 生成并标 AI 生成（上传时勾选 YouTube 合成内容声明）。
