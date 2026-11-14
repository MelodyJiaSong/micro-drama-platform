# ep11 世界最大船舶 · 交接（代理 2026-11-03/04）

## 做了什么
1. **调研与全量数据**：VesselFinder 高级搜索按 GT 区间自适应切分，抓全部 GT ≥ 160,000 的登记船 1,090 艘（`vf_bands.py` → `vf_fleet_gt160_bands.json`；翻页抓法会漂移漏 52 艘，已弃用 `vf_fleet_gt160.json`）。DNV Vessel Register 公开接口（`dnv.py`，缓存 `dnv/`）核到 13 个船级的一手 GT69，和 VesselFinder 全部一致。维基只作交叉核对（`raw/`）。WebSearch 配额曾用尽一段时间，竞品只用了需求证据文件里的 3 条。
2. **船级归并**：`classes_def.py`（规则）→ `compute_classes.py`（成员、最大 GT、代表船）→ `build.py`（data.json；EXTRA 写备注与徽章）→ `gen_sources.py`（sources.md）→ `gen_content.py`（`content/` 41 份内容文件，找图第一步）。
3. **找图**（follow-up 016/023/用户追加要求 3–5）：
   - `claude_search.py` + `flickr_search.py`：Flickr 搜索页按每艘姊妹船名搜，只收 CC BY / BY-SA / CC0 / PDM（含 4.0），标题/描述须含船名，按拍摄/上传年排除同名旧船（如 1995 年的 Legend of the Seas、旧 Sun Princess），再开照片页取 2048 px 尺寸与页面许可。注意：Flickr 搜索「引号 + 许可过滤」组合会返回 apiFailed，urllib 请求也常被拒，已改为不加引号 + curl。
   - `webimg.py`：WebSearch 找到的新闻 / 官方页，取 og:image 或最大 srcset 原图（许可不明 → 风险图）。
   - `prefetch.py`（curl 预下载，编号与 image_reselect 一致）→ `image_reselect.py download/score` → `sheet.py`（逐项全部候选总览，`sheets/`）→ 人工逐张看 → `picks_manual.json` → `apply_picks.py`（主图 + image_alt + 生成图写 data.json / assets.json）→ `cropsheet.py`（模拟正方形满版裁切 + 底部文字区，逐卡检查船体是否被遮）。
   - Valemax：全网只找到 ≤1,000 px 的真实照片，按追加要求 4/5 用 `tools/codex_image.py` 生成 1 张（`gen/valemax_prompt.txt`，日志由脚本写入 request_log），亲眼看合格（无文字 / logo / 人），账本 licence = "AI-generated (Codex image_gen)"。
4. **渲染**：validate --strict 两版均 OK；timeline 5:53；预览片头 / 洞察 / 前 10 / 冠军 / 计分板 / 来源卡已看；thumb；render 默认母版与风险版；publish（默认版 `publish.md`，风险版 `_build/publish_with-risk-images.md`），`post_publish.py` 修标题、章节、AI 图说明、合成内容声明、标签。

## 关键口径与默认（详见 topic.md / sources.md）
- 指标：登记总吨 GT，屏上写全数（偏离 bible §3.4 的 3 位有效数字，避免前 13 名假并列）。
- 一张卡 = 一个船级（同一船东同一建造计划、同一名义尺寸，分在几家船厂造也算一级；Valemax / Guaibamax 按 Vale 规格算一级）；数值 = 级内最大登记 GT；照片可为任一姊妹船（assets.json `subject_note` 写明是哪艘）。
- 范围：2026-11 在役；不收 FPSO / FLNG / FSO 等永久系泊装置、军舰、在建与已拆船；下限 = 大于仍在营运的最大油轮 170,618 GT → N = 41（集装箱船 29、邮轮 8、矿砂船 3、起重船 1）。
- 国家 = 运营公司总部：OOCL → Hong Kong，ONE → Singapore，Valemax / Guaibamax → Brazil（Vale），Excel 级 → Germany（首制船 AIDAnova 的运营方，也是照片中的船）。计分板 Switzerland 8 > France 6 > Denmark 5 > United States 4。
- 次显示「×Titanic」= GT ÷ 46,328。

## 图片来源分布
- 默认母版：34 张 Flickr 可商用照片 + 2 张可商用替代图（Icon、Disney Adventure 的 image_alt）+ 5 张 AI 生成写实插图（Valemax 主图；OOCL Wisdom、Sphere、Winning Ambition、Guaibamax 的 image_alt，主代理 2026-11-04 决定，`gen/*_prompt.txt`，均一次合格），**无占位卡**。
- 风险版：6 张许可不明网页照片（Icon 皇家加勒比海试航拍、OOCL Wisdom 船厂航拍、Disney Adventure 抵新加坡、Sun Princess、Winning Creation/Devotion 恒力船厂航拍、Sea Zhoushan 旋筒帆）。
- 单独补搜：Valemax（Flickr 二轮 0 张 → 全网 2 轮 → 生成）、Guaibamax、Winning、Sphere、Icon、Oasis、MSC World、Disney、OOCL Wisdom、Berlin Maersk、Ever E、Ane Maersk、MSC London、Meraviglia(-Plus)、Excel 共 15 项做了 WebSearch 全网检索。

## 没解决的问题
1. 章节 #41–#41 问题渲染器已修，publish.md 已重新生成（`post_publish.py` 只补标题、开头句、AI 署名措辞、标签）。
2. 默认版 4 张 AI 替代图是通用船型插图（无涂装 / logo），并非该船级的真实外观（如 OOCL 涂装、Princess 船体波浪画）；风险版用真实照片。Winning 那张船体偏下，部分被文字区遮挡。
3. 默认母版渲染开始后 data.json 又改了不上屏的字段（representative 船名修正），manifest 在渲染结束时取的 sha256 与现文件一致；画面不受影响。渲染期间 10 个代理并发，单部约 80 分钟（4.4 fps）。
4. Pioneering Spirit 冠军卡照片以起重梁为主、船体被文字区遮住一部分（Flickr 全是侧面照，正方形裁切的限制）。
5. YUAN HAI SI LU（2026，180,011 GT 单一来源）未收，若核实应排第 31 名。

## 需要用户决定
见 topic.md「待用户确认」7 条：船级口径、N=41（不凑 50）、海工装置不收、Hong Kong / Singapore 单列、Valemax 归巴西、Yuan Hai Si Lu、GT 全数显示。另：风险版 6 张许可不明图是否签字放行；Valemax 卡用 AI 生成图（上传须勾选合成内容声明）。

## 产物
- 默认母版：`render/ep11_largest_ships_master.mp4`（2026-11-04 加入 4 张 AI 替代图后重渲；5:53，1920×1080，60 fps，静音轨）
- 风险版：`render/ep11_largest_ships_master_with-risk-images.mp4`（5:53，同规格）
- 封面草图 `render/thumbnail.png`；预览帧 `render/preview/`；成片抽帧 `_build/frames/`
- 发布文案：默认版 `publish.md`；选风险版时用 `_build/publish_with-risk-images.md`（含 6 张许可不明图的来源，需补作者 / 授权）
- 风险版未重渲：image_alt 只影响默认版，风险版画面与 2026-11-04 前渲出的一致（其 manifest 里的 data.json / assets.json 哈希是旧值）。

## 第 1 轮独立审片后修改（2026-11-04，主代理决定）
- B1/B2/M1：#30 Berlin Maersk、#13 改名 Hamburg Express class（换 Busan Express 实拍）、#1、#42 Emma、#35 Marco Polo、#24 Barzan（换 Hapag 涂装）、#5 Saadé 均重新取图或预裁切（`picks_by_key.json` 的 precrop，`apply_picks.py` 只裁不改）；冠军默认版用 kees torn 的侧面整船（Allseas 船名 + 生活区），风险版用 Allseas 北海航拍。逐张用 `rank_scroll preview` 实际帧确认看得出船。
- M2：收入远海丝路（Yuan Hai Si Lu）为 #31，计 China；无可商用实拍，用 Codex 生成写实插图（一次合格）。N = 42，洞察卡 1、2 改为 42 / 7 个新船级。
- M3：来源行改「Sources: DNV Vessel Register, VesselFinder · Flag = operator HQ」；scope_note 写明 HK / ONE→Singapore / Valemax→Brazil；Excellence 级改按取值船 Costa Toscana 的运营方 → Italy（卡名改 Excellence class）。计分板：CH 8、FR 6、DK 5、US 4、CN 4、TW/HK/SG 3、DE 2、BR 2、KR 1、IT 1。
- M5：风险版署名补真实来源（Allseas via gCaptain、Royal Caribbean via WPTV、Cruise Hive、Nautical Flock、Vale via gCaptain，许可写 licence unknown）；OOCL Wisdom、Winning 两项风险图质量差，两版都改用 AI 插图；用当前数据与渲染器重渲风险版。
- M6：layout.intro_hold = 2.5（总长 6:03）。minor：Hamburg Express 命名、Star Princess 账本注记、MOL Triumph 加「now ONE」、封面改 #2–#4、checklist 措辞、Excellence class 命名已改；Triple-E HDR 图（m6）与 #1 长度 382 m（m9）未改。
- M4 配乐仍待主代理（Suno）。
