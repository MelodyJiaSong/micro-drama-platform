# 调研 B · 数据、版权、国旗图标、渲染与音乐

> 2026-11-02 调研（只读，未调用收费服务）。「证据」带编号来源；「推断」为判断。非法律意见，发布前对关键许可书面复核。

## 0. 最大风险：YouTube 收益政策

YouTube「非原创内容」政策（原 repetitious content，2025-07 改名）明确不予收益：**"image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value"**，以及看似模板批量、期间差异很小的视频 [1]。同页 reused content：只读他人网站文本 / 新闻源不符合收益资格 [1]。

「无旁白 + 模板滚动卡片」正落在打击范围。推断的对策：每期独立选题与数据研究、屏上解读（同比、升降箭头、方法与来源卡）、每期设计随主题变化；上线先 1–2 期试水观察 YPP 审核。

## 1. 数据来源

| 主题 | 一手 / 权威 | 许可与限制 |
|---|---|---|
| 国家宏观 | World Bank WDI / API | 自产数据默认 **CC BY 4.0**，可商用，须署名、注明改动；部分数据集为 ODbL / 第三方，逐个看元数据 [2] |
| 国家宏观 | IMF WEO | 引用格式 "Source: International Monetary Fund, 库名, 链接"；**商业再利用须先邮件 copyright@imf.org 申请**；批量下载也要许可 [3] |
| 通用结构化 | Wikidata SPARQL | **CC0** [4]；用于实体 QID、国家、成立年份、官网、Commons 图；统计值时效参差（推断） |
| 汽车销量 | OICA（国家级 PDF）[5]；Focus2Move 品牌榜（159 市场上牌）[6]；JATO / MarkLines（付费） | OICA 口径为乘用＋商用，与只算乘用差很大，标题必须写口径 [5][7] |
| 企业 | Forbes Global 2000、Fortune Global 500、companiesmarketcap、年报 / 10-K | Forbes 无明确商用授权（二手资料称需许可）[8]；推断：只作交叉核对与引用，主值回年报 / 交易所 |
| 足球 | Transfermarkt | 二手资料：条款禁爬虫、禁商业转售，并保留 TDM 权利 [9]（原文抓取被拒，未核）。**不爬取** |

推断：事实不受版权保护，但商业榜单编排、欧盟数据库权、站点条款可能构成限制。安全做法：一手数据当主值，商业榜单只作交叉核对，并写「据 X 整理」。

## 2. 图片版权

- Wikimedia Commons：署名含作者、标题（若有）、链接、许可名，格式「适合媒介」，署作者不署上传者 [10][11]；CC 推荐视频内＋描述框都署名，最好另有署名网页 [12]。
- CC BY-SA：纯格式 / 媒介转换不构成改编，进合集不改变合集许可 [13]；推断：原样缩放裁切放进卡片大概率不触发 SA，重绘 / 深改会触发。**音乐与画面同步一律算改编** [13] → 不用 CC BY-SA 音乐。
- 人物照片：商用可能还需被摄者同意，摄影师许可不够 [10]；OpenAI 出图不得未经同意生成真人肖像（仓库商用表）。
- 品牌 logo：受商标法保护，复杂 logo 还可能有版权；YouTube 禁商标侵权，由权利人投诉 [14]。推断：只用于指认（指示性使用）、不暗示合作、不改色不变形是业界做法，YouTube 无成文豁免 [15]。
- AI 图：逼真内容须勾选合成内容声明 [16]；不要 AI 生成真实品牌的产品与 logo（推断：假冒与误导）。

## 3. 国旗与图标

| 资源 | 许可 | 署名 |
|---|---|---|
| lipis/flag-icons（SVG 4:3 / 1:1） | MIT [17] | 保留许可声明 |
| flagcdn / flagpedia | 国旗图属公有领域 [18] | 不要求 |
| Twemoji（jdecked） | 代码 MIT，图形 **CC BY 4.0** [19] | 必须 |
| Lucide | ISC（Feather 部分 MIT）[20] | 保留声明 |
| Tabler Icons | MIT [21] | 保留声明 |
| Phosphor | MIT [22] | 保留声明 |
| Material Symbols | Apache 2.0 [23] | 不强制 |
| Font Awesome Free | 图标 CC BY 4.0；品牌图标另受商标约束 [24] | 必须 |

## 4. 渲染方案（10–20 min × 60fps ≈ 3.6–7.2 万帧）

| 方案 | 许可 | 评价（推断为主） |
|---|---|---|
| Remotion | 个人 / ≤3 人营利组织免费；超过须 Company License（Creators $25/人/月；Automators $0.01/次、月底 $100）[25][26]；源码可见非 OSI | CSS 能力最强、CJK 质量好、有 CameraMotionBlur [27]；阴影 / 模糊 / 渐变慢 [28]；4K 长片本地数小时 |
| Python：skia-python / Pillow + ffmpeg 管道 | skia-python BSD，144.1（2026-10-20），有 Win / 3.11 轮子 [29] | 与仓库技术栈一致、开源、可复现；浮点坐标、高质量抗锯齿 |
| MoviePy 2 | MIT，2.2.1（2025-05）[30] | 适合拼接混音，不当主渲染 |
| Manim | MIT [31] | 数学动画，不合适 |
| Motion Canvas | MIT [32] | 编辑器手工向，批量弱 |
| HTML + Playwright | — | 等于自制简化 Remotion |
| Blender | 开源，本机 5.1 / 5.2 | 适合 3D 片头，主体滚动过重 |
| After Effects 模板 | 订阅＋模板许可 | 难代码化复现 |

## 5. 音乐

- Suno（条款 2026-08-10 修订、2026-09-03 生效）[33]：Pro / Premier 档权利转让给用户，但仅限本档月度额度内、官方渠道下载的产出；免费档仅个人非商用；**Remix 任何档都不能商用**；不保证可获版权；禁止去水印 / 元数据。条款未提 Content ID；二手资料：Content ID 只做指纹比对不识别 AI，有分发商拒送 AI 曲目进 Content ID，也有误认领案例 [34][35]。
- YouTube 音频库：YPP 可变现，「版权安全」曲目不会被 Content ID 认领；CC 曲目须描述框署名 [36]。风险最低，但撞曲多。
- Epidemic Sound：订阅后频道进 Content ID 白名单；Creator 1 个频道 / 平台，Pro 3 个 [37]（价格以官网为准）。
- Artlist：接入 Content ID 白名单；订阅期发布的作品停订后仍有效；禁止把音乐登记进 Content ID [38][39]。
- 合成内容声明：只有以生成音乐为主体的内容才需声明 [16]；背景乐大概率不需要（推断）。
- 仓库本机 Suno 服务（`specs/development/suno_browser_service`）：FastAPI `POST /v1/jobs`（必带幂等键）、SQLite、CLI、stdio MCP、`suno-music` skill；advanced / simple / sounds；验证码即整队暂停，未知提交不重提。**2026-10-22 实测 Pro 账号，但验证码导致队列持久暂停，实际下载未验收**（paid_services.md）。
- `specs/development/bgm_library` 已于 2026-10-05 停用（实现已删）。

## 6. paid_services.md 相关约束

- 收费调用前读 paid_services.md、定归属，经 `tools/service_request.py::RequestLog` 先写 request 事件再调用；查询 / 下载 / 重试 / 失败都留痕；不可直连绕过；超时或结果未知先按任务 ID 查询，不重提。
- 图片只用 ElevenLabs（`gpt-image-2.5-sunburst`）或 Codex 内置 image_gen；禁止即梦出图；不生成未经同意的真人肖像。
- 音乐：Suno 有条件可用（Pro / Premier、额度内官方下载、Remix 不商用、不去水印）；Eleven Music、Udio、Stable Audio 禁用；ACE-Step 1.5 本地（MIT）允许。用户只授权本机 Suno 服务自动点 Create 与下载。
- 条款不明确的工具不进成品，由用户决定。
- 本系列请求日志归属：`ai_videos/paihangbang/request_log.md`（见 README）。

## 7. 本机工具现状（2026-11-02 实测）

| 项 | 结果 |
|---|---|
| Node / npm | v25.2.1（Current 非 LTS）/ 11.6.2 |
| ffmpeg | N-125365（2026-06-30），libx264 / libx265 / libsvtav1 / h264_nvenc / hevc_nvenc / av1_nvenc |
| GPU | NVIDIA RTX 5000 Ada Laptop，驱动 596.58 |
| Python | 3.11.9；Pillow 12.3.0（FreeType 有，**raqm 无**）；numpy 2.4.6 |
| 未安装 | moviepy、playwright、skia-python、fontTools |
| 字体 | NotoSansSC-VF、NotoSerifSC-VF、微软雅黑、黑体、Arial、Bahnschrift、Segoe |
| Blender | 5.1、5.2 |

字体（推断）：缺完整 Noto Sans CJK、Inter；微软雅黑用于商业视频有授权疑问。建议把 Noto Sans / Inter（SIL OFL，待复核 [40]）字体文件放进项目并锁版本。

## 未能核实

Transfermarkt / Forbes 条款原文；Epidemic / Artlist 现价。

## 来源

1. https://support.google.com/youtube/answer/1311392
2. https://datacatalog.worldbank.org/public-licenses
3. https://www.imf.org/en/About/copyright-and-terms
4. https://www.wikidata.org/wiki/Wikidata:Licensing
5. https://oica.net/wp-content/uploads/2026/04/sales-2025.pdf
6. https://www.focus2move.com/world-cars-brand-ranking
7. https://www.theglobaleconomy.com/rankings/passenger_cars_sales/
8. https://someka.net/excel-template/forbes-global-2000-list ；https://statista.com/page/forbes-global2000
9. https://inquisitiveminds.bristows.com/post/102hhpm/web-crawling-and-scraping-data-what-is-prohibited-commercial-use ；https://stat.ethz.ch/pipermail/r-package-devel/2018q1/002405.html
10. https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia
11. https://commons.wikimedia.org/wiki/Commons:Credit_line
12. https://wiki.creativecommons.org/wiki/Recommended_practices_for_attribution
13. https://creativecommons.org/faq/
14. https://support.google.com/youtube/answer/6154218
15. https://forum.openwrt.org/t/use-of-openwrt-logo-on-youtube-videos/135507 ；https://digiday.com/media/youtubes-hands-off-enforcement-branded-content
16. https://support.google.com/youtube/answer/14328491
17. https://github.com/lipis/flag-icons
18. https://flagpedia.net/terms ；https://flagpedia.net/download/api
19. https://github.com/jdecked/twemoji
20. https://lucide.dev/license
21. https://github.com/tabler/tabler-icons
22. https://github.com/phosphor-icons/core
23. https://github.com/google/material-design-icons
24. https://fontawesome.com/license/free
25. https://github.com/remotion-dev/remotion/blob/main/LICENSE.md
26. https://www.remotion.dev/docs/license/faq
27. https://www.remotion.dev/docs/motion-blur
28. https://www.remotion.dev/docs/performance
29. https://pypi.org/project/skia-python/
30. https://pypi.org/project/moviepy/
31. https://manim.community
32. https://github.com/motion-canvas/motion-canvas
33. https://suno.com/terms
34. https://www.creativeainews.com/articles/ai-music-youtube-content-id-claims-2026/
35. https://sunowatermark.com/youtube-content-id-ai-music/ ；https://www.musicbusinessworldwide.com/suno-upgrades-ai-song-editor-as-labels-reportedly-push-for-content-id-style-fingerprinting-in-licensing-talks-with-ai-music-platforms
36. https://support.google.com/youtube/answer/3376882
37. https://www.epidemicsound.com/our-plans/personal-subscription/ ；https://help.epidemicsound.com/hc/en-us/articles/26247405706386
38. https://help.artlist.io/hc/en-us/articles/29648622402333
39. https://help-center.artlist.io/media/w5mglb2w/pro-license-19112023.pdf
40. https://github.com/notofonts/noto-cjk
