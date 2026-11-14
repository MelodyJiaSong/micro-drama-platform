# ep06 · 史上最畅销日本漫画 Top 30（累计发行量，截至 2026-11）

> 2026-11-03 代理起草（用户「开始你的 research 和制作吧」，未提问直接开工，**待用户点头**）。follow-up 014（立项）、019（两步走找图）。
> 原定 ep04，与同时开工的动物（ep04）、病毒（ep05）按 follow-up 顺序协调后改为 ep06。
> 数据 `data.json`，出处与取舍 `sources.md`，图片账本 `assets.json`，脚本 `_build/`（01 数据 → 02 出处 → search_covers 找图）。

- 英文标题（≤60 字符）：**Best-Selling Manga of All Time | Top 30 (2026)**（46 字符）
  - 屏上：标题 Best-Selling Manga of All Time · kicker「TOP 30」· 统计行「Copies in circulation · Latest announced figure · year on each card」
- 指标与口径：
  - 用户说的「日本动漫销量」取**漫画系列累计发行量**（copies in circulation）。动画没有统一可比的「销量」口径（票房、播放、碟片各不相同），不混进来。
  - 主值 = 出版社公布（或主流媒体转述其公告）的**最新**累计数字，含海外与电子版与否按公告原文；Wikipedia 只作基线与交叉核对。
  - 剔除含非漫画书籍的数字（Crayon Shin-chan 1.48 亿 → 漫画约 5800 万；Astro Boy 1 亿为 1981 年「相关书籍」）；Major 6666 万无出处，出榜。
  - 旧公告照收（累计只增不减，旧值是下限），每张卡在数值旁标「as of 年份」，年份 = 该数字**首次公布**的年份（审片后统一）——这是对 bible §3.3「18 个月」规则的本期例外，理由见 `sources.md` §2-4。
- N / 每名秒数 / 预计时长：30 张卡（同值同名次：2、14、16×7、23、28 并列）；卡宽 600，每名约 5.3 s，前 10 名约 5.7 s；洞察卡 5 张；**实际 3:37**（`layout.intro_hold = 2.5`：片头后整排静止 2.5 s，让 #30 也能读满 3 s）。
- 主源与交叉核对源：集英社 / 讲谈社 / 小学馆 / 秋田书店 / Square Enix 公告与官方 X、Oricon、Natalie、Mantan Web、ANN 等（逐条见 `sources.md` §1）；数字是事实，不搬文字。
- 国家归属口径：作品全部来自日本。**不显示国旗**（`layout.flags = false`，渲染器 2026-11-03 新增）：30 面相同的日本国旗不提供信息，又压住封面标题字（预览实测）；标题已写明是日本漫画。**计分板改按单行本出版社**（复用 `continent` 字段），卡上国家行显示出版社名。结尾揭晓：Shueisha 16 > Kodansha 5 > Shogakukan 4 > 其余各 1。
- 主题皮肤「manga」：墨黑 → 深红渐变底，印章红强调色 `#FF3B4E`；主图 = 第 1 卷日文原版封面（或官方漫画主视觉），卡宽 600（封面约 0.70 宽高比，裁切极少），焦点 `[0.5, 0.2]` 保住标题字。标签：作者（users）、连载年份（calendar）；徽章写变化与看点（NEW: 100M IN JUNE 2026、+50M IN ONE YEAR、ON HIATUS SINCE 2014 等）。
- 洞察卡（5 张，`sources.md` §3 有依据；第 1 轮独立审片后改写 3 条）：
  1. after 28：Crayon Shin-chan's 148M is left out: it also counts ~20M non-manga books.
  2. after 23：Next: seven series tied at the 100-million mark.
  3. after 11：Jujutsu Kaisen added 50 million copies in the 15 months after its 2024 finale.
  4. after 8：Demon Slayer has just 23 volumes: about 9.6M copies each, the most per volume here.
  5. after 2：One Piece has sold about twice as many copies as any other manga.
  - 备选：Golgo 13 holds the record for most volumes of a single manga series（220+）；One Piece 6 亿里海外 1.5 亿；Demon Slayer 海外 5600 万；Berserk 70M 里 30M 是海外版；Blue Lock 3 个月 +5M，下一个最可能进榜。
- 竞品同题：搜索未取到可靠的 YouTube 播放数据（只找到文字榜单：comicbook.com、Statista、Beebom 等）；差异仍按 D1–D4：每个数字带出处和年份，纠正常见错值（Crayon Shin-chan、Major），出版社计分板，洞察卡讲「谁在涨」。
- 主图（follow-up 019 两步走、026 改由 Claude 找图）：先定内容（data.json），再按日文名 / 作者 / 出版社找封面——两轮 Codex 联网搜（follow-up 026 之前已完成）＋一轮 Claude 子代理补搜（Google Play Books 官方电子版封面大图、Amazon 原图），每部 4–13 张候选，全部下载、打分、拼图人工逐张核对作品。选定 30 张：28 张日文版（25 张第 1 卷），Baki、Fist of the North Star 用英文版第 1 卷（日文版无足够清晰的图）；Kingdom 用官方 X 发布的第 71 卷封面，KochiKame 用第 200 卷，Slam Dunk 用新装再编版 #1，Captain Tsubasa 用电子版小学生編 1。长边全部 ≥1725 px（Doraemon 切白边后 1831），Google Books 的部分大图疑为放大，实际细节约 1200–1600 px。候选与拼图在 `_build/reselect/`、`_build/contact/`。卡上署名「Illustration: © 作者 / 出版社」。
- 风险：
  1. **封面版权**：所有主图都是版权作品。按 follow-up 014 统一标 `image_risk = "copyrighted artwork"`：默认母版扣下（占位卡），`_with-risk-images` 版放入，**以带图版为主片**（follow-up 019：每张卡都要高质量图），由用户发布前决定。不生成原作角色图。
  2. **数字口径与时效**：口径不统一、部分数字很旧，评论区会有人纠错——片头口径行 + 描述框 scope_note + 卡上「as of 年份」。发布前 7 天复核（Blue Lock、Gintama、Kingdom、One Piece 最可能变化）。
  3. **YPP 原创性**：同前几期，靠 D1、D4 区分；旁白仍不加。
