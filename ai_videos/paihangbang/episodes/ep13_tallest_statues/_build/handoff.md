# ep13 · 世界最高雕像 · 交接（handoff）

> 2026-11-03 子代理（follow-up 015 / 016 / 023 / 追加要求 3–5）。不写 qc.md；审片由主代理另起上下文。

## 做了什么

- 调研：维基 List of tallest statues（rev 1382307847，只作交叉核对与线索）+ 逐条非维基来源（建设方行业刊物、政府 / 旅游主管机构、新闻、百科出版物；个别只有旅游网站）。原料在 `raw/`（维基表 wikitext、Commons 各国 FoP 规则页、维基摘要），每项内容摘要在 `content/`（follow-up 016 第一步）。
- 数据：`items_def.py`（唯一数据源）→ `build.py` → `data.json`；`gen_sources.py` → `sources.md`；`hints.py` 是每项的外观 / 机位 / 易混对象 / 当地名称（喂给找图）。
- 找图：
  1. 第一轮 Codex 联网搜（`image_reselect.py search`，9 批）＋第二轮 Codex 只要可商用（`--licensed`，跑到第 3 批时按 follow-up 023 叫停；`codex_r00–r02` 保留使用；第 4 批起中断，request_log 里可能有一条无结果的请求）。
  2. follow-up 023 起全部由我自己做：Flickr 公开搜索页（CC BY / BY-SA / CC0 / PDM，`tools/flickr_search.py` → `reselect/claude_flickr_a/_b.json`）、Pexels（WebFetch 搜索页 → `claude_web.json`）、全网检索（WebSearch → 页面 og:image / 正文大图，`tools/og_image.py` → `claude_open1–5.json`）。Bing / Google / DuckDuckGo 图片搜索都拿不到结果（Google 拦截、Bing 忽略查询词、DDG 有人机验证）。
  3. `tools/image_reselect_ep13.py` 是共用工具的本地副本：key 去下标、先 codex 后 claude 固定候选编号、Flickr 限流退避 / `SKIP_FLICKR=1`。
  4. 逐张看 `reselect/contact_*.jpg` 挑选，结果写 `selection.json`，`select.py` 落图、写 `assets.json` 与 data.json 的 image / image_alt / image_risk / image_focus。核对过：每张上屏图的像素尺寸与候选元数据一致（来源、作者、许可对应同一张图）。
- 校验与预览：`validate --strict`（两版都 OK）、timeline 4:43、预览帧（片头、洞察卡、前 10、冠军、计分板、来源卡）亲眼看过。
- 渲染：默认母版 `render/ep13_tallest_statues_master.mp4`（4:42.9，1920×1080，60 fps，h264，58.7 MB；10 个代理并发，渲了 71 分钟）+ 风险版 `render/ep13_tallest_statues_master_with-risk-images.mp4`（4:42.9，1080p60，63.5 MB，74 分钟）；ffprobe 核对时长 / 分辨率 / 帧率，两版各抽 3 帧看过。publish.md 已生成并人工补写（默认版描述 + 风险版替换段落）。
- 11-04 补图后两版均已用最新数据重渲（default 4091 s、risk 2113 s），两版 nb_frames = 16974 与 timeline 一致，抽帧看过。

## 关键口径与默认（详见 topic.md、sources.md）

- 只收已建成；主值 = 雕像本体高（含手持物，不含莲花座 / 基座 / 建筑 / 山体），含基座总高放标签。N = 42（能核实的本体 ≥ 49 m 全部），不凑 50。
- **春泉大佛排第 3（108 m）**：按不含莲花座统一口径；常见的 128 m 含 20 m 莲花座，洞察卡 5 解释。拉开坤 115.8 m 第 2。
- 剔除 9 项（数值矛盾 / 只有总高 / 完工未证实）：开元寺阿弥陀佛、Mother of All Asia、清莱观音、太湖西山观音、Lung Por Tuad、Phra Kakusunto、Bodhi Tahtaung 坐佛、Ba Den 山观音、佛光大佛。
- 国家 = 所在地，香港计入中国，台湾单列。计分板：中国 13、日本 9、泰国 5。

## 图片现状

| 类别 | 数量 |
|---|---|
| 风险版有图 | 42 / 42 |
| 主图可商用许可（Unsplash 7、Pexels 7、Flickr CC 6、CC0 / PD 2） | 22 |
| 主图许可不明（标 `licence unknown`，只进风险版） | 20 |
| 有可商用 `image_alt`（默认版显示；FoP 项照片许可干净但雕塑版权仍在） | 13 |
| **默认母版占位卡** | **18**（许可不明且找不到可商用替代；按主代理决定不用 AI 生成替代） |
| AI 生成图 | 0（全网都找到了真实照片，按追加要求 5 不需要生成） |

默认版占位 18 项：Ksitigarbha of Jiuhua、Kyaikhto Seated Buddha、Phra Buddha Chok、Kaga Kannon、Confucius of Mount Ni、Yang'asha Statue、Kurume Jibo Kannon、Jesus of Sibea-bea、Guan Yu of Yuncheng、Mukdahan Great Buddha、God of Red Mountain、Aizu Jibo Kannon、Tokyo Bay Kannon、The Victor、Koxinga Statue、Emperors Yan and Huang、Usami Daikannon、Guerrero Chimalli。

**画质偏低（长边 < 1300 px），建议主代理用浏览器 Google 图片升级**：Kyaikhto 坐佛（847×635）、尼山孔子（640×924）、仰阿莎（820×510）、久留米观音（768×1024）、宇佐美观音（1024×768）、Sibea-bea（1080×720）、The Victor（1280×720 夜景）、炎黄二帝（1200×800，前景有人群）。

**Flickr 限流后重试（11-04 02:10）**：峨眉弥勒换成 Flickr CC BY 2.0 7000 px 照片（主图与默认版都用它）；小豆岛观音默认版加了 Flickr CC BY 2.0 远景作 image_alt；东京湾观音 Flickr 候选都没拍到像、Chimalli 的 Flickr 只拍到基座，未采用；7 项低清图再全网找没有更高清的（The Victor 官方新闻稿图也只有 1280 px）。两版已重渲。

**此前 Flickr 有可商用候选但下载被限流（HTTP 429，多代理并发）**：峨眉弥勒 8、东京湾观音 8、小豆岛观音 3、Chimalli 2、Dordenma 8、African Renaissance 8、慈山寺 4、Wat Paknam 8 张（链接已在 `claude_flickr_*.json`）。限流解除后跑 `python _build/tools/image_reselect_ep13.py download <ep>`（不带 SKIP_FLICKR）→ 看拼图 → 改 `selection.json` 的 alt → `select.py`，峨眉、东京湾、小豆岛、Chimalli 四项就能从占位变成有图（FoP 风险仍在）。

## 需要用户决定

1. **FoP**：21 项所在国对雕塑无商用全景自由（日本 9、台湾 2、缅甸 2、印尼 2、菲律宾 1、越南 1、俄、乌、不丹、塞内加尔）。其中 10 项默认版用了可商用许可照片作 `image_alt`——**照片许可只解决摄影师版权，雕塑作者版权（FoP）仍在**，默认版对这 10 项也有风险。发布哪一版、是否整体改用占位，由用户签字。日本 / 台湾条款只排除「以出售复制品为目的」，用于视频多数解读认为可以，按 brief 从严。
2. 春泉大佛排第 3 的口径（见上）。
3. 默认版 20 张占位卡观感差；可选：①发布风险版（用户签字许可不明图）；②主代理补可商用替代；③对非 FoP 国家（中国 / 泰国 / 墨西哥）的许可不明项按追加要求 4 用 Codex 生成默认版图（本期未做，因为全网有真实照片）。
4. 数据薄弱项（只有旅游网站或单一来源）：赤山明神、宇佐美观音、Kyaikhto 坐佛、南山观音本体 78 m、九华山地藏 84 m（维基 76 m）、Dordenma 54 m（另说 51.5 m）。发布前 7 天复核孟买 Ambedkar 像（若揭幕且本体 ≥ 49 m 需加入）与加贺大观音存废。

## 没解决的问题

- Flickr 下载限流（上）；Unsplash / Pixabay 有反爬，只用了 Codex 已给出的直链与 Pexels。
- `Luang Pho Yai` 用的是 PublicDomainPictures.net 的「Free public domain image」，许可页因 403 未能亲自打开核对，账本记为 Public domain，发布前可再点开确认。

## 2026-11-04 按独立审片（qc.md「必须修」）修改

- 数据：Statue of Belief 改为本体 78.9 m（369 ft 总高 − 110 ft 台座，维基正文 + The Daily Guardian；351 ft 是施工期总高），由第 4 降到第 12；香港慈山寺观音 70 m 含三层莲座、像身高未公开，按口径剔除（N 42→41，标题 Top 41）。春泉大佛备注、NPS 链接、洞察卡位置（Liberty 卡提前到 #37 之后）已改。Son Tra / Guishan / Kaga 只查到总高，无分项资料，按原值保留，sources 已注明。
- 默认版：中国 6、泰国 2、墨西哥 1 共 9 项改用 Codex 生成写实插画（`_build/gen/`，prompt 同目录，均无人物 / 文字 / 横幅，逐张看过；渲染器自动标 AI IMAGE）；占位从 18 降到 9（日本 5、台湾、缅甸、印尼、菲律宾各 1），原因统一写「licence unclear」。
- 风险版：炎黄二帝（真人合影带横幅）、赤山明神（保留权利）主图换成生成图；东京湾观音换 Travel.jp 头像特写（许可不明），The Victor 换 JG Summit 新闻稿夜景（许可不明），不再用写明 All rights reserved 的图；Kyaikhto、会津观音、The Victor、Mukdahan 调 image_focus，预览确认头部完整。
- Mother Ukraine 两版都换成 Pexels（Ev Vekselman）三叉戟盾牌的新照片。
- publish.md 重生成并补人工内容（AI 插画声明、未收录名单、CC BY 链接、版本说明），封面重出。
- 重渲（11-04 05:40）：默认版 / 风险版均 4:37.6、1080p60、nb_frames 16654 = timeline，各抽 3 帧看过；validate --strict 两版 OK。

## 2026-11-04 复核返修

- Chimalli、赤山明神、仰阿莎按实物特征重写 prompt 各重出一次（`_build/gen/*_v2.*`，改为「写实插画」风格，不再用 documentary photograph 措辞），与实拍对照造型已对上（`_build/gen/cmp_v2.jpg`），采用；未退回占位。
- 风险版 Mukdahan 换成 trip.com 全身图（c0），佛脸与全身完整（preview 确认）。
- publish.md 的 AI 图署名改为「AI-generated illustration (Codex)」，去掉评论里的内部路径；sources.md #3 备注改为「would still rank No. 3」，Statue of Belief 备注补 Explore Our India 三叉戟 351 ft 说法。两版重渲。
