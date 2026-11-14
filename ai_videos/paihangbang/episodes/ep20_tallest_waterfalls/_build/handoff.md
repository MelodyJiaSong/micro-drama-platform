# ep20 交接（handoff）· 世界最高瀑布 Top 35

> 2026-11-03 子代理（follow-up 015 / 016 / 023 / 024 / 用户追加要求 5）。没写 qc.md（主代理另起独立上下文审片），没跑 followup.py，没 commit。

## 做了什么

1. **调研**：抓 World Waterfall Database「Overall Height」榜前 105 条 + 每条瀑布页事实字段（`wwd_crawl.py` → `raw/wwd_top.json`，原始 HTML `raw/wwd/`）；WWD 法律页只限制照片，本期只引事实数值。Guinness（Angel 979 / 807、Tugela 948）、IGN Peru 2007（Yumbilla 895.4）、USGS（Yosemite 739）作权威佐证；Wikipedia 列表 rev 1379783845 只作交叉核对（API 被限流，部分只拿到 REST 导语）。竞品：yt-dlp 搜索（逐条详情被 YouTube 拦，无发布日期）。
2. **数据**：`items_def.py`（入选规则）→ `build.py` → `../data.json`（35 条、5 张洞察卡、scope_note、tally=country、theme=cascade、layout card_w 600）；`gen_sources.py` → `../sources.md`。
3. **内容笔记**：`content/NN_<slug>.md`（WWD 描述摘录 + Wikipedia 导语 + 认图要点 / image_hint），35 份。
4. **找图**：Codex 联网搜索只跑到前 4 批（idx 0–19，follow-up 023 起停用、进程已停）；之后由我自己用 Flickr 公开搜索页（只取 CC BY / BY-SA / CC0 / PDM，`flickr_search.py`）、WebSearch、来源页抓图（`page_imgs.py`）找候选，`contact.py` / `peek.py` 拼图逐张看。定稿在 `final_apply.py`（逐项写明来源与理由）。Codex 只用于生成（`tools/codex_image.py`，先记 `ai_videos/paihangbang/request_log.md`），26 张，逐张看过，全部一次合格。
   - 共用 download 的 c<k> 错位 bug：本期只下载过一次，另外把 12 张取自候选目录的图逐张重新从 image_url 下载比对 SHA，全部一致（未受影响）。
5. **渲染**：validate --strict（默认版、风险版都 OK）、preview 多帧亲眼看（修了 Kjelfossen 裁切、Waihilau 标签重复）、thumb、render 母版 + 风险版、publish。

## 关键口径与默认（详见 `../topic.md`「待用户确认」）

- 主值 = 总落差；WWD 为主源，**有公开测量 / 记录者优先**：Angel 979 m（Guinness，WWD 只算 807 m）、Yumbilla 895.4 m（IGN）。
- 入选：有名字 + WWD Cataloged，或 Confirmed 且写明高度依据，或 Unconfirmed 但有独立权威测量（Tugela、Yumbilla）；排除断流的 Mongefossen、Brufossen，排除只有一个数字的 Confirmed 条目；N = 35（≥ 631 m）。
- 季节性：收，WWD 流量月数 < 12 或明确只在融雪 / 雨季有水的标 SEASONAL（14 条）；Mardalsfossen 标 HYDRO-REGULATED。
- 留尼汪两条计 France。

## 图片来源分布

| 类别 | 数量 | 条目（名次） |
|---|---|---|
| 可商用照片（默认版、风险版都用） | 9 | Angel #1（Imaggeo CC BY-SA 3.0）、Yumbilla #4、Browne #8、Gocta #12、Kjelfossen #13、Yosemite #18（Pexels）、Trou de Fer #21、Mardalsfossen #33（CC0）、Cascade Blanche #34 |
| 风险照片（许可不明 / 保留所有权利，只进 `_with-risk-images` 版；默认版用 AI 生成图 image_alt） | 14 | Tugela #2、Mattenbach #3、Skorga #5、Vinnufossen #6、Kjerrskredfossen #9、Waihilau #10、Colonial Creek #11、Isella #14、Tjøtafossen #16、Døntefossen #17、Tågfossen #24、Seahpo #30、Sulphide #31、Sentinel #35 |
| 只有 AI 生成图（两版都用） | 12 | James Bruce #7、Johannesburg #15、Cloudcap #19、Boulder Glacier #20、Kjeragfossen #22、Yutajé #22、Ølmåfossen #24、Cabin Boy #26、Sprænefossen #27、Lake Unknown #28、Kukenán #29、Ägertenbach #32 |

- 默认母版：9 张真实照片 + 26 张 AI 生成图，无占位卡。风险版：23 张真实照片 + 12 张 AI 生成图。
- 风险照片中 Tågfossen、Sentinel 取自 WWD、Colonial / Seahpo / Sulphide 取自 Northwest Waterfall Survey（与 WWD 同一作者群），两站都写明照片未经书面许可不得使用——要放风险版需先取得许可；分辨率也偏低（533–800 px 宽）。
- 「只有 AI 图」的 12 项已试过：Flickr CC 搜索（每项 2–3 个检索词）、WebSearch 找 Pexels / Unsplash / Pixabay 与来源页、Codex 首轮搜索（只覆盖 idx 0–19）。Bing 图片页对脚本返回无关结果，WebFetch 不允许访问 Bing；world-of-waterfalls 返回 403、europeanwaterfalls 图片由 JS 加载。**建议主代理用浏览器 Google 图片为这 12 项补真实照片（至少风险版）**，优先 Kjeragfossen、Kukenán、James Bruce、Johannesburg（brewbooks 的 CC BY-SA 照片 `flickr.com/photos/brewbooks/5903214152` 可能就是 Johannesburg Falls，但标题写「I think」，未敢用）。

## 没解决的问题

1. 默认版 AI 图比例高（26/35）。publish.md 已写「含 AI 生成图，上传勾选合成内容声明」。卡片署名写「Photo: AI-generated illustration」。
2. 风险版里多张「All rights reserved」图需要逐一取得许可才可发布。
3. Wikipedia API 被限流，部分交叉核对值来自 Wikipedia 列表而非条目；Sulphide Creek Falls、Kjerrskredfossen、Isella、Boulder Glacier、Tjøtafossen、Tågfossen、Cabin Boy、Ägertenbach 只有 WWD 一个来源。
4. 时长约 4:02（N = 35 卡宽 600），低于 bible 建议的 5–8 分钟。

## 需要用户决定

1. 冠军：Angel 979 m（Guinness）vs 按 WWD 只算 807 m（Tugela 第一）。默认前者 + HEIGHT DISPUTED 徽章 + 洞察卡。
2. 是否收 Unconfirmed 估值（Tres Hermanas 914、Olo'upena 878 等）。默认不收。
3. 默认版大量 AI 图是否可接受，或等主代理补真实照片后重渲。
4. 风险版是否发布（需签字 + 许可）。

## 成片

- 默认母版 `render/ep20_tallest_waterfalls_master.mp4`：1920×1080，60 fps，H.264，4:01.6（241.63 s），静音，80 MB。
- 风险版 `render/ep20_tallest_waterfalls_master_with-risk-images.mp4`：同规格，4:01.6，78 MB。
- 两版都从成片抽 3 帧看过（`_build/frames/`）。渲染时机器很忙（10 个代理同时渲），各约 55–65 分钟；Bash 工具会杀掉超长前台 / 后台命令，所以改用 `_build/render_both.cmd` 经 Start-Process 独立运行。
- `publish.md` 由 `rank_scroll publish` 生成，再跑 `_build/finish_publish.py` 补 AI 图署名、合成内容声明（Yes）、标签、置顶说明。

## 第 1 轮审片后的修改（2026-11-04，主代理授权自主）

- **补可商用实拍**：Flickr CC（CC BY / BY-SA / CC0 / PDM / US Gov）补搜 Tugela、Vinnufossen、Kjeragfossen、Kukenán、Sentinel、Mattenbach、Døntefossen、Tjøtafossen、Browne。也试了 Unsplash（下载页有人机验证，拿不到）和 NPS NPGallery（没有 Sentinel Fall）。**只找到 1 张**：Tugela，Mike and Lara Wolfe，CC0，Flickr 39498453682，Royal Natal 谷底仰拍 Amphitheatre，裁成竖幅；作为 `image_alt` 进默认版，风险版保持不动。其余项能找到的只有远景山谷或景区周边，看不到瀑布，或者认不准是哪条（如 mtnscll 的「Sentinel Falls」是一整条大水量直瀑，和 Sentinel Fall 十余级细瀑的形态不符），所以没用。Browne 的 Flickr 原图页没找到，账本仍链到 wondermondo 转载页。
- **洞察卡 5** → 「Angel's 979 m adds rapids below its 807 m drop. Drop those and Tugela (948 m) wins.」（83 字符），置顶评论同步。**洞察卡 2** → 「…; World Waterfall Database estimates ~479 m.」（88 字符）。
- **标签被丢**：subtitle 全面缩短（如 Canaima NP、Eikesdalen、Yosemite NP），去掉和 subtitle 重复的 map-pin 标签；#33、#35 把关键的 calendar 标签放在第一位。预览帧确认 #1「807 m main drop」、#33「Runs Jun 20–Aug 20」、#35「Usually dry by July」都已上屏。
- **其他 minor**：#33 标签改用 WWD 的最长落差 328 m；scope_note 例外里补上 Tugela: Guinness；Yosemite 交叉核对改为 USGS 现有链接；Vinnu 名称说明写进 notes；Kjelfossen 重新裁到主瀑布；Browne 加 image_focus [0.7, 0.5]；topic.md 第 10 名表述修正；publish 章节改为 #35–#31 起（渲染器已修）；sources.md 洞察卡依据同步更新。
- **AI 标注**：渲染器自动加黄色「AI IMAGE」标记和「AI-generated image, not a photo」署名，数据没改。
- **图片分布（新）**：默认版 10 张实拍 + 25 张 AI 生成图；风险版不变（23 张实拍 + 12 张 AI）。
- 两版已按新数据重渲（结果见下）。
- **重渲结果（2026-11-04 03:04 / 03:57）**：默认母版 `render/ep20_tallest_waterfalls_master.mp4` 和风险版 `render/ep20_tallest_waterfalls_master_with-risk-images.mp4`，均为 1920×1080 60 fps，ffprobe 逐帧计数 14,498 帧 = timeline 241.633 s × 60；manifest 里的 data.json sha256 与当前文件一致。两版各抽 2–3 帧看过（`_build/frames/m2_*`、`r2_*`）：#1「807 m main drop」、新洞察卡 5、黄色「AI IMAGE」标记都已上屏；风险版的 Tugela 仍是原风险图（按要求未动）。validate --strict 两版 OK；publish.md 已重新生成并跑过 finish_publish.py。
- **复核小修（2026-11-04）**：重出封面，#2 Tugela 用上 CC0 实拍；#3 Mattenbach 仍是 AI 图，已用 `_build/thumb_ai_label.py` 加黄色「AI IMAGE」角标（原图存 `render/thumbnail_raw.png`）。publish.md 描述首段加「Some images are AI-generated illustrations, marked AI IMAGE on screen.」，清单写明 10 张实拍 + 25 张 AI 图、合成内容声明选 Yes。source_line 加「· AI images marked」后为 78 字符，超过 70 字符上限，所以不改，成片也不需要重渲。
