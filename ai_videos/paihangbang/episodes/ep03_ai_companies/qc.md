# ep03「30 AI Companies Shaping the Future」独立审片（静音画面版）

- 审片人：独立上下文 Claude 子代理（没有参与制作）
- 日期：2026-11-04
- 审核文件（sha256 前 12 位）：

  | 文件 | sha256 前 12 位 |
  |---|---|
  | `render/ep03_ai_companies_master_with-risk-images.mp4`（签字版） | `32a85a488421` |
  | `render/ep03_ai_companies_master.mp4`（默认版） | `28506e7b202d` |
  | `render/thumbnail.png` | `7e7af2db656c` |

- 对照材料：`bible.md`（§2、§4、§7）、`data_contract.md`、`topic.md`、`data.json`、`assets.json`、`sources.md`、`publish.md`、`_build/qc_data_independent.md`。两份 manifest 记录的 `data.json` 与 `assets.json` 哈希都和当前文件一致，所以两版成片对应的就是当前数据。
- 审片方法：
  - 用 ffprobe 核对规格。
  - 每 3 秒抽一帧做联系表。
  - 在每张卡和洞察卡居中的时刻抽全分辨率裁图，两版各 35 张。
  - 片头按 0.17–0.5 秒间隔细看；片尾每段抽全帧。
  - 用 signalstats 逐帧算 YDIF，查闪烁和跳帧。
  - 看了全部 30 张头像源图、21 张 AI 插图和对应 prompt。
  - 用脚本逐条核对 `assets.json` 的覆盖情况、许可和 sha256。
- 未做：
  - 配乐（本版静音，§7-6 不适用）。
  - 全量事实复核：只抽查了 `qc_data_independent.md` 的修正有没有落实。
  - 人脸比对：头像身份只按来源页署名和外观判断。

## 总结论：小修后可发布（静音画面版）

**现在不能直接上传。** 先清掉下面 2 个 blocker，再处理 major：

- 2 个 blocker 都在包装层面（封面、发布文案），改起来不费事。
- major 里有两项需要改参数或换图，然后**重渲一次**：第一张卡停留太短；Lovable 插图接近品牌 logo。

画面本体总体质量不错：

- **规格**：1920×1080，60 fps（60/1），H.264 High，yuv420p，14540 帧。时长 242.333 s，两版都和 manifest 一致。
- **顺序与图片**：30 张卡的顺序和 `data.json` 一致，无重复无遗漏，每张卡都有图，默认版没有占位卡。
- **数字与计分**：卡上数字和 `data.json` 一致；计分板累计正确（US 17 / CN 5 / UK 3 / CA、FR、JP、SE、DE 各 1，共 30）。
- **洞察卡**：5 张的位置和文字都正确。
- **转场**：没有闪烁或跳帧。
- **事实核查修正**：已落实到卡面。

签字版另有许可风险，由用户决定，详见文末「签字版专项」。

## 问题表

### Blocker

| # | 位置 | 现象 | 建议改法 |
|---|---|---|---|
| B1 | `render/thumbnail.png` | 封面三张图用的都是**风险图**，不是默认版的图：<br>• OpenAI 办公室照（许可未知）；<br>• Anthropic 办公室照（Amber Hakim，All rights reserved）；<br>• DeepSeek 照（Florence Lo / Reuters，通讯社照片，下架风险最高）。<br>默认版上传时用这张封面，等于把扣下的图放在最显眼的位置。 | 封面渲染时同样走 `image_alt`，默认版另出一张封面，例如 `thumbnail.png` 用替代图、`thumbnail_with-risk-images.png` 用风险图。<br>上传哪一版视频，就配哪一版封面。 |
| B2 | `publish.md` 描述与章节 | 文案还是按「排名模式」生成的，和本期「列表、不排名」相矛盾：<br>• 首句写「30 ai companies **ranked by** latest valuation」；<br>• 章节写「0:00 Intro & #21–#30 / 1:13 #11–#20 / 3:25 No. 1」。实际 0:00 起是第 1–10 家（DeepMind 起）；3:25 是 Thinking Machines Lab 停留，不是「No. 1」；<br>• 标签有 `#Ranking`。 | 首句改为「listed by founding year, not ranked」。<br>章节按实际时间线重写，例如：<br>0:00 Intro<br>0:04 2010–2018 (DeepMind → Runway)<br>0:47 2019–2021 (Cohere → MiniMax)<br>1:42 2022 (ElevenLabs → Perplexity)<br>2:14 2023 (Moonshot → Higgsfield)<br>3:09 2024–2025<br>3:33 Companies by country<br>3:40 Sources & credits<br>去掉 `#Ranking`。<br>根因在 `rank_scroll publish` 没有处理 `mode: list`，建议修模板，避免下一期再出现。 |

### Major

| # | 位置 | 现象 | 建议改法 |
|---|---|---|---|
| M1 | 第 1 张卡 Google DeepMind（两版都有，约 3.5–6 s） | 卡片约 3.6 s 开始滑入，约 4.4 s 才完整进画，约 5.2 s 起左缘就被裁掉，「Google DeepMind」名称和「Google-owned」在约 5.6 s 后被截成「oogle DeepMind」。<br>完整可读约 1–1.4 s，不满足 §7-5「3 秒内看得清」，而开场第一张卡正是钩子。<br>原因：`data.json.layout` 没有设 `intro_hold`，数据契约建议 2.5。 | 在 `layout` 里加 `"intro_hold": 2.5`（或 3），然后重渲两版。 |
| M2 | 默认版第 26 张 Lovable 插图（`26_lovable_alt.jpg`） | prompt 写的是「a glowing heart-shaped gradient of orange, pink and blue」，成图中央是一颗橙粉紫渐变的发光爱心。这几乎就是 Lovable 的 logo 图形。<br>违反 bible §4「不生成 logo / 品牌标识」，而且卡上同时还放着真 logo 牌，看起来像二次改色的 logo。 | 改写 prompt，去掉心形和品牌色渐变，改成中性意象（例如浮起的 app 界面卡片加斯德哥尔摩窗景），重新生成并记录日志，再重渲。 |
| M3 | `publish.md` 署名 + 卡面署名行 | 描述和置顶评论只列了主图署名，**完全没有头像署名**。进片的 CC 头像有 5 张：<br>• Amodei、Srinivas：Kimberly White / Getty for TechCrunch，CC BY 2.0；<br>• Jain、Shulman：Katelyn Tucker / Slava Blazer，CC BY 2.0；<br>• Musk：Gage Skidmore，CC BY-SA 4.0。<br>来源卡写的是「Image credits: … listed in the description」，和实际不符。<br>另外，Luma（13）和 Suno（16）卡底署名行被截成「Portrait: Katelyn Tucker / Slava Blazer Photography (TechCr…」，许可名看不到。根因是 `data.json` 里 `person.credit` 本身在 60 字符处被截断（「…(TechCrunch) / CC 」）。CC BY 要求标明许可。 | 在描述或置顶评论里补「Portraits」一节，逐条写作者、许可和链接。<br>`person.credit` 改成短写法（如「K. Tucker/TechCrunch · CC BY 2.0」），保证许可名完整显示。 |
| M4 | `sources.md` 与 `publish.md` Comment 2 · MiniMax（14）、Sakana（24） | 卡面已按事实核查改成「$7.0B · market cap · Nov 2026」和「$2.7B · valuation · Apr 2026」，但「主值来源」链接还是旧值：<br>• MiniMax 仍是「close HK$160.70 on 2026-10-22」，交叉核对值 7.29B，「差 0.1%」与 7.0 对不上；<br>• Sakana 仍是 TechCrunch「$2.65B (2025-11-17)」。<br>观众点链接看不到卡上的数字，不满足 §7-2「每个数值能追到出处」。 | MiniMax 主值来源换成 11-03 收盘行情页（如 stockanalysis 0100.HK 或核查报告用的链接）。<br>Sakana 主值来源换成 https://sakana.ai/series-b/（2026-04 更新页）。<br>重跑 `gen_sources.py` 与 publish。 |
| M5 | `publish.md` 标题 | 「30 AI Companies Shaping the Future \| 30 Ai Companies (2026)」：<br>• 和 `topic.md` 定稿「30 AI Companies Shaping the Future (2026)」不一致；<br>• 后半句重复；<br>• 「Ai」大小写错误。<br>标签 `#30Aicompanies` 同样有误。 | 标题改为「30 AI Companies Shaping the Future (2026)」，标签同步修正。 |
| M6 | `publish.md`（签字版） | 只有一套按**默认版**生成的署名。如果用户签字上传签字版：<br>• 描述里写的是「AI-generated illustration」，画面上却是真实照片；<br>• Getty / Reuters / AP / WIRED 等实际署名一条都没有。 | 生成 `publish_with-risk-images.md`（或在同一文件里分两节），按 `image` 和风险头像逐条列署名，并在上传清单里写明两版的对应关系。 |

### Minor

| # | 位置 | 现象 | 建议改法 |
|---|---|---|---|
| m1 | 默认版 21 张 AI 插图卡 | 署名行写「**Photo:** AI-generated illustration」。前缀「Photo」和「不是照片」自相矛盾。 | AI 图的前缀改成「Image:」或「Illustration:」。 |
| m2 | 默认版 Anthropic（11）、Luma（13）、Suno（16）、Perplexity（19） | 主图和圆形头像出自同一张舞台照，同一张脸在卡上出现两次，画面重复。 | 可以接受。有余力时，主图换成同许可的另一张（如舞台全景或活动现场）。 |
| m3 | 默认版 Figure AI（18）插图 | prompt 写的是 generic、no markings，但成图（黑色面罩头、银黑分段机身、工厂搬箱）和 Figure 02 外观、BMW 工厂场景很接近，有「可辨认品牌产品」之嫌。**存疑**。 | 人工比对一下。若认为太像，改成明显不同的造型（如白色圆润机身），或改成工厂场景加机械臂。 |
| m4 | 默认版 OpenAI（2）、Sakana（24）插图 | OpenAI 图中央「发光的扭结」容易让人联想到 OpenAI 的花结 logo；Sakana「鱼群组成大鱼」接近其 logo 意象。都不是 logo 本身，风险低。 | 记录在案即可。如要更稳妥，OpenAI 改成别的中心物。 |
| m5 | 默认版 Unitree（4）Pexels 图 | 来源页标题只写了「futuristic robotic dog at tech exhibit」，没写型号。外观像宇树四足机器人，但是否 Unitree 产品**存疑**。 | 查原图页的说明或展会信息。确认不了就在 notes 注明，或另找明确标注 Unitree 的 CC 图。 |
| m6 | 默认版 ElevenLabs（15）、xAI（21）主图 | ElevenLabs 是暗场舞台照，人物很小，无法确认台上是否为公司人员。xAI 是 Grok 网页特写，灰白、低对比，海报感弱。 | 有更好的 CC 或 Unsplash 图时再替换；不阻塞发布。 |
| m7 | Thinking Machines（30）logo 牌；Sakana（24）logo 牌 | TML 是浅灰字放在白底上，对比度低；Sakana 的 logo 在牌内很小，手机上难认。 | 白色或浅色字标的 logo 按契约用深色 `logo_bg`；Sakana 可放大或裁掉留白。 |
| m8 | SSI（29）名称行 | 「Safe Superintelligence」和右侧「Ilya Sutskever」之间只有约 20 px 间隙，几乎相碰。 | 渲染器在名称与人物块之间留最小间距，不够时缩小字号，或允许名称换行。 |
| m9 | 角落计分板 | 只显示前 5 国（US / CN / UK / CA / FR），日本、瑞典、德国出场时角落不会出现。结尾揭晓页 8 国完整，数字正确。 | 可接受；可以考虑显示 6–8 个小旗。 |
| m10 | DeepSeek（23）次行 | 事实核查建议：如果保留 $52B，日期改为「Jun 2026 round」（6 月中交割，7 月披露）。卡上仍写 Jul 2026，制作方没写理由。 | 改成 Jun 2026，或在 notes 写明为何用披露月。 |
| m11 | `publish.md` 描述 | 写「per-item links in the pinned comment」，但逐条数据来源在 Comment 2（回复），置顶的是图片署名。署名里还暴露了内部路径「prompt in assets/gen/…」，观众看不懂。 | 改成「in the pinned comment thread」。删掉内部路径，只写「AI-generated illustration (Codex image_gen)」。 |
| m12 | `publish.md` Comment 2 · Moonshot（20）、Cursor（17） | Moonshot 来源标题写「closes final private round at $50B」，卡上写 pre-money。Cursor 来源是 06-16 宣布收购，卡上日期是 Aug 2026（交割）。 | 来源标题后补一句口径说明（pre-money / closed Aug 14），或补第二个链接。 |
| m13 | 风险头像 Yan Junjie（14） | 源图 426×460，低于 topic 定的「头像短边 ≥ 600 px」质量闸门。只影响签字版。 | 有更大图时替换。 |
| m14 | 封面草图 | 标题完整、没被截断，三张卡的数字清晰。但胶囊「30 AI COMPANIES」和大标题「30 AI COMPANIES SHAPING THE FUTURE」重复，标题里也没有年份。 | 胶囊改成「2026」或「EST. 2010 → 2025」，或者去掉。 |

## 签字版专项（供用户签字时参考，不计入上面的结论）

- 签字版换回的风险图：主图 28 张、头像 25 张，许可都是 unknown 或 All rights reserved。
- 其中**通讯社或图库照片**，被下架和索赔的风险最高：
  - 主图 6 张：DeepMind（Bloomberg / Getty）、Zhipu（Reuters）、Suno（AP）、DeepSeek（Reuters）、SSI（Getty for SSI）、Thinking Machines（Getty）。
  - 头像 2 张：DeepSeek 梁文锋（VCG / Getty）、Mira Murati（WIRED，All rights reserved）。
  - 建议即使签字，也至少把这 8 张换回 `image_alt` 或首字母章。
- 签字版卡底署名行大多带「/ unknown」，而且多处被截断（如「published by Qatar Fo」「GTEF / C」）。这不构成授权，只是照实标注。
- Luma（13）风险主图是两人的宣传照，站立男子看起来不是 Amit Jain，是否为创始人**存疑**。其余风险图主体都和公司相关。
- 头像身份：30 张都与标注的人外观一致，没发现张冠李戴。
  - Emad Mostaque（红色棒球帽，来源 OpenUK）和 Yan Junjie（光头）两张没有第二来源可对照，标记为**存疑，未做人脸比对**。
  - 裁切都把脸放在圆内。

## 事实核查修正抽查（`_build/qc_data_independent.md`）

| 核查项 | 卡面现状 | 结论 |
|---|---|---|
| 1 ElevenLabs 口径 | $22B · share sale · Sep 2026 | 已落实 |
| 2 OpenAI 去掉 Sora | ChatGPT · Codex · LLMs | 已落实 |
| 3 OpenAI 徽章 | IPO FILED | 已落实 |
| 4 xAI 改名 | 名称仍为 xAI，徽章 NOW SPACEXAI | 已落实（取徽章方案） |
| 5–6 Cohere | C$35.7B · valuation · Oct 2026，MERGER PENDING | 已落实（未写「~US$25.5B」，可接受） |
| 7 HeyGen | $200M · ARR · Jun 2026 | 已落实 |
| 8 MiniMax | $7.0B · market cap · Nov 2026 | 卡面已落实，**来源链接未更新（M4）** |
| 9 DeepSeek | $52B · Jul 2026 | 保留确认值，理由已记录；日期见 m10 |
| 10 Moonshot | pre-money · Oct 2026，HK IPO FILED | 已落实 |
| 11 Stability 人物 | Emad Mostaque · Founder (left 2024) | 按用户意图保留，已标注 |
| 12 Hassabis | Co-founder & Chair | 已落实 |
| 13 Sakana | $2.7B · Apr 2026 | 卡面已落实，**来源链接未更新（M4）** |
| 16 Cursor | SpaceX deal · Aug 2026 | 已落实 |
| 17 MiniMax 产品 | Hailuo · Talkie · M3 | 已落实 |
| 19 BFL | FLUX 3 · Kontext | 已落实 |
| 20 Musk | Co-founder | 已落实 |
| 21 Mistral | €21B+ | 已落实 |
| 23 Unitree | Founder & Chairman | 已落实 |
| 24 Figure | Figure 03 · Helix 02 | 已落实 |
| 26 洞察卡 4 | 「Fears over DeepSeek-R1 … (Jan 27, 2025)」 | 已落实 |

## 专项检查结果（任务清单 1–11）

1. **顺序**：30 张卡按成立年份 2010 → 2025 排列，和 `data.json` 一致，无重复无遗漏。两版每张卡都有图，默认版没有空白或占位卡。✔
2. **卡上文字**：名称、主数字和次行、EST. 年份、徽章、信息行、人物姓名与身份都和 `data.json` 一致，没有拼写错误，也没有出框；放不下的类别标签按设计从后往前丢（如 Cohere、BFL、SSI）。手机全屏下名称和数值都清楚。<br>例外：第 1 张卡完整可读时间太短（M1）；SSI 名称和人物块几乎相碰（m8）；部分署名行被截断（M3）。△
3. **logo**：都是当前 logo，没有变形或改色。<br>TML 对比度低、Sakana 太小（m7）。Midjourney 用的是 Lobe Icons 的等宽字标，不是官方矢量，**存疑**但可辨认。xAI 已改名 SpaceXAI，仍用 xAI 的「X」图形，和徽章一起看能对上。△
4. **头像**：外观都和标注的人一致，裁切都把脸放在圆内。Emad Mostaque、Yan Junjie 存疑（未比对）。默认版里许可未知的 25 人都显示首字母章，只放了 5 张 CC 头像。✔（附存疑）
5. **照片与插图**：主体都和公司相关。AI 插图没有真人脸、可读文字或水印；Synthesia、HeyGen 里是无五官的剪影或图形，可以接受。<br>Lovable 插图近似 logo（M2）；Figure 插图接近 Figure 02 外观（m3，存疑）。△
6. **国旗与计分板**：国旗和总部国家对得上（ElevenLabs 用美国旗、SSI 用美国旗，口径见 `sources.md`）。角落计分板逐张累计正确，结尾揭晓 US 17 / CN 5 / UK 3 / CA / FR / JP / SE / DE 各 1，和 `data.json` 一致。✔
7. **洞察卡**：5 张分别出现在 Hugging Face、Runway、Midjourney、DeepSeek、Black Forest Labs 之后，文字和 `data.json` 逐字一致，完整可读，在屏上停留约 10 s 以上。✔
8. **片头片尾与转场**：
   - 片头 0–3.5 s，标题、口径行、来源行都完整；
   - 最后一张卡 209.3–213.3 s 停留 4 s，居中；
   - 计分板揭晓 213.3–220.3 s；
   - 来源卡 220.3–224.3 s；
   - 片尾「Thanks for watching!」224.3–242.3 s，共 18 s，留了片尾元素空间。
   - YDIF 逐帧检查：只有片头滑入时的预期运动；静止段每约 4.17 s 有一次关键帧编码微变（平均像素差 0.08，肉眼不可见），没有闪烁或跳帧。
   - 第 1 张卡停留问题见 M1。△
9. **版权账本**：两版进片的全部图片都在 `assets.json` 里，共 118 条，sha256 全部匹配。默认版用到的主图许可都在白名单内：AI-generated 21 张；CC BY 2.0 4 张；CC BY-SA 2.0 / 4.0 各 1 张；Pexels 1 张；Unsplash 2 张。默认版头像只有 CC BY 2.0 ×4 和 CC BY-SA 4.0 ×1，其余显示首字母章。logo 按商标指认使用。卡上有署名行（字号很小，部分被截断，见 M3）。Codex 生图在 `request_log.md` 有记录。△
10. **publish.md**：「ranked」措辞和章节错误（B2），标题错误（M5），缺头像署名（M3），来源链接过时（M4），没有签字版文案（M6）。合成内容声明已在上传清单里提示（选 Yes），描述里也写了「21 images marked AI-generated are illustrations, not photos」。✘
11. **封面草图**：1280×720，标题完整未截断，但用了风险图（B1），胶囊和标题重复（m14）。✘

## bible §7 审片清单勾选

| # | 清单项 | 结果 | 说明 |
|---|---|---|---|
| 1 | 名次连续、无重复，排序与 `data.json` 一致 | ☑ 通过 | 列表模式不显示名次，出场位置 1–30 连续，和 `data.json` 一致 |
| 2 | 每个数值能在 `sources.md` 追到出处，统计期与片头一致 | ☐ 未通过（小修） | 片头写「Data as of Nov 3, 2026」，和口径一致；MiniMax、Sakana 的来源链接对不上卡面数字（M4） |
| 3 | 国旗与国家对得上，口径在 `topic.md` 定好 | ☑ 通过 | 口径是总部所在国（scope_note「Flags show headquarters country」） |
| 4 | 每张图都在 `assets.json`，许可是允许的类型 | ☑ 通过（默认版）／ ☐ 签字版待用户签字 | 默认版全在白名单内；签字版 28 张主图和 25 张头像许可未知，其中 8 张是通讯社或图库照片 |
| 5 | 文字不出框、不闪烁；手机全屏 3 秒内看清名称与数值 | ☐ 未通过（小修） | 第 1 张卡完整可读约 1–1.4 s（M1）；其余卡完整可见约 10 s，没有闪烁 |
| 6 | 音乐无爆音，高潮对上前 10 名，片尾 15–20 s 干净 | — 不适用 | 本版静音，配乐另行处理；片尾画面 18 s 干净 |
| 7 | 描述框的来源与署名完整 | ☐ 未通过 | 缺头像署名（M3）、缺签字版署名（M6），「ranked」措辞和章节有误（B2），标题有误（M5） |

## 复审建议

修完 B1、B2 和 M1–M6 后：

1. 重渲两版，同时出各自的封面；
2. 复审只需看：片头第 1 张卡、Lovable 卡、署名行、两版封面、`publish.md`（两版）、`sources.md` 的 MiniMax 和 Sakana 两条。

---

## 作者处理记录（2026-11-04 夜间，制作代理；不是独立审片结论）

以下为制作代理按本报告逐条处理的结果，处理后两版重渲（`_build/finalize.py --render`，配乐见文末）。是否通过以用户看片与下一轮独立审片为准。

| 项 | 处理 |
|---|---|
| B1 封面用风险图 | `finalize.py` 分别出 `render/thumbnail.png`（默认版，只用可商用图）与 `render/thumbnail_with-risk-images.png`（签字版）；封面加 logo 牌、标题两行不截断（rank_scroll follow-up 012） |
| B2 publish 排名口径 | 渲染器 publish 加列表模式：首句 "one by one in order (not a ranking)"，章节按出场公司分段，去掉 #Ranking 与名次（rank_scroll follow-up 013） |
| M1 首卡停留太短 | `layout.intro_hold = 2.5` |
| M2 Lovable 插图像 logo | 改 prompt 重生成（`assets/gen/lovable_prompt_v2.txt`，无爱心）；后 Flickr 限流解除，默认版改用 Web Summit CC BY 4.0 实拍；Figure 插图也改为机械手特写（`figure_ai_v2`），避免像 Figure 02 |
| M3 头像署名 | publish 两版都列出进片头像的署名（简版 + 完整版）；`person.credit` 不再截到 60 字；来源卡文案沿用渲染器默认 |
| M4 来源链接未跟改 | MiniMax 改为 11-03 收盘的 StockAnalysis 历史页、Sakana 改为官方 Series B 页 |
| M5 标题 | `youtube_title` = "30 AI Companies Shaping the Future (2026)" |
| M6 签字版发布文案 | 另出 `publish_with-risk-images.md`（按签字版画面列署名，含 Getty / Reuters / AP 等） |
| minor：AI 图署名写 Photo | 卡上改为 "Illustration: AI-generated, not a photo"（另一会话同时加了 AI IMAGE 角标） |
| minor：内部 prompt 路径外露 | 账本 author 只写 "AI-generated illustration (Codex image_gen)"，prompt 路径移到 `prompt_file` 字段 |
| minor：SSI 名称贴着人名 | 名称与创始人说明之间留 40 px |
| minor：DeepSeek 日期 | 保留 Jul 2026（财新 2026-07-17 报道完成），理由写入 notes |
| minor：Cursor 来源标题 | 写明 announced 2026-06-16 / closed 2026-08-14 |
| minor：Luma 签字版站着的男子未必是 Amit Jain | 主图改用 TechCrunch CC BY 2.0 舞台照，两版一致、无风险 |
| 新增：更多 CC 实拍 | Flickr 限流解除后：DeepMind、Synthesia、Runway、Cohere、HeyGen、Lovable 默认版改用 CC 实拍；Hassabis、Riparbelli、Gomez、Joshua Xu、Osika 的头像改用 CC 舞台照裁脸（两版无风险） |
| 未处理 | 同一张脸出现两次（主图与头像同一人，Anthropic 等）——默认版可接受；ElevenLabs / xAI 主图偏弱；角落计分板只显示前 5 国（渲染器既有设计）；Yan Junjie 头像 426 px（仅签字版）；OpenAI、Hugging Face、Sakana 的 CC 实拍因 Flickr 限流没下下来，默认版仍为 AI 插图 |
| 签字版通讯社图 | 未替换：签字版仍含 DeepMind、智谱、Suno、DeepSeek、SSI、Thinking Machines 的通讯社 / 图库主图（默认版这几张都已是 CC 实拍或 AI 插图），由用户签字时决定是否换成默认版的图 |

配乐：Suno 本期生成 2 首（job 84113957），起初只下载到 1 首（57 s），第二首因下载额度用完未取回。2026-11-04 用户要求重试，第二首（72 s，`assets/music/f0c149fc-….mp3`）已取回；两版母版用两首重渲（renderer 交叉淡化接成 125.3 s 链，循环铺满 244.8 s，整体 −16 LUFS，无静音段）。机检：两首接点（约 0:55）短暂降到约 −26 dB；链循环点（约 2:03–2:06）有约 2 s 降到约 −33 dB 的「换气」（第二首收尾接第一首前奏），不是断音，待人耳试听确认是否要手工修接点（参照 ep06）。
