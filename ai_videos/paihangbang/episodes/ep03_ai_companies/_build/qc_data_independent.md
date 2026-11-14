# ep03「30 AI Companies Shaping the Future」数据独立事实审核

- 审核日期：2026-11-04
- 审核对象：`data.json`（30 家公司 + 5 张洞察卡）、`sources.md`
- 审核方式：独立上网核对，每条换用 sources.md 以外的来源。主审核员拆成 5 个并行检索子任务，每个子任务都另起上下文，没有参与制作；关键结论由主审核员再次检索复核，复核项包括 Sora 停服、OpenAI 保密递交 S-1、Hassabis 职位变动、Cohere 官方新闻稿、Sakana 官方 Series B 页、DeepSeek 10 月轮和 4 条洞察卡。
- 未修改任何项目文件，未下载图片，未调用收费服务。

## 总结论：修改后可发布

30 家公司的成立年份、总部国家、主数字的数量级都没有硬错误；Unitree、Zhipu 两家的市值复算后数量级正确。不过下面几处必须先改：

- **2 处 blocker：**
  - ElevenLabs 的 $22B 来自员工股要约收购（tender），卡上却标成「valuation」，和 scope_note 的口径冲突。
  - OpenAI 的代表产品仍写 Sora，而 Sora 已在 2026 年停服。
- **约 11 处 major：** 大多是 2026 年的状态变化没写上，或者口径标错。
  - 状态变化：xAI 已改名 SpaceXAI；OpenAI 已保密递交 IPO 申请；Cohere 与 Aleph Alpha 合并待完成；DeepSeek 10 月新一轮融资。
  - 口径标错：HeyGen 的 ARR 写成了「annual revenue」；MiniMax 的市值日期不一致；Cohere 的「$20B+」低于公司公告；Moonshot 的 $50B 是投前估值。

改完 blocker 和 major，且发布前 7 天内刷新上市公司市值，就可以发布。

## 问题表（按严重程度）

| 序号 | 公司 | 字段 | 现写法 | 应改为 | 依据链接 | 严重程度 |
|---|---|---|---|---|---|---|
| 1 | ElevenLabs (#15) | value_display / secondary_display | $22B · valuation · Sep 2026 | **两种改法二选一：**<br>① 按口径改为「$11B · valuation · Feb 2026」（Series D，$500M，红杉领投，最近一次一级融资）；<br>② 保留 $22B，但标成「employee tender · Sep 2026」，并在 scope_note 写明例外。<br>$22B 是 2026-09-30 完成的 $300M 员工股要约收购（老股转让，钱不进公司），不是「latest completed private round (post-money)」。 | https://tech.eu/2026/02/04/elevenlabs-raises-500m-says-building-towards-ipo/ ・ https://www.musicbusinessworldwide.com/elevenlabs-valuation-doubles-to-22b-four-times-that-of-ai-music-rival-suno/ ・ https://www.eweek.com/news/elevenlabs-500m-funding/ | **blocker** |
| 2 | OpenAI (#2) | tags（产品） | ChatGPT · Sora · Codex | 去掉 Sora，例如改为「ChatGPT · Codex · GPT-5」（具体型号发布前再核）。OpenAI 2026-03-24 宣布停掉 Sora：App 于 2026-04-26 关闭，API 于 2026-09-24 关闭。 | https://www.macrumors.com/2026/03/24/openai-discontinuing-sora-ai-video-app/ ・ https://engadget.com/ai/openai-is-shutting-down-its-sora-video-generation-app-211023358.html ・ https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/ | **blocker** |
| 3 | OpenAI (#2) | badge | 无 | 「IPO FILED (CONFIDENTIAL)」。OpenAI 2026-06-08 自己公告已保密递交 S-1 草案，上市时间未定，截至 11-03 未上市。Anthropic 卡已标 IPO FILED，两张卡应当一致。 | https://www.techrepublic.com/article/news-openai-confidential-sec-ipo-filing/ ・ https://www.eweek.com/news/openai-confidential-ipo-filing-sec/ ・ https://www.digitimes.com/news/a20260609VL208.html | major |
| 4 | xAI (#21) | name / badge | xAI；PART OF SPACEX | 名称改为「SpaceXAI (formerly xAI)」：2026-07-06 正式改名 SpaceXAI，10 月起 X 账号品牌是 SpaceXSI。badge 可写「PART OF SPACEX (NASDAQ: SPCX)」，因为 SpaceX 已于 2026-06-12 在纳斯达克上市。$250B · Feb 2026 正确。 | https://www.engadget.com/2209300/xai-now-officially-spacexai/ ・ https://finance.yahoo.com/technology/ai/articles/xai-makes-rebrand-spacexai-complete-215010760.html ・ https://teslanorth.com/2026/10/10/spacexai-spacexsi-x-rename/ ・ https://news.crunchbase.com/public/spacex-record-breaking-ipo-spcx/ | major |
| 5 | Cohere (#7) | value_display | $20B+ · valuation · Oct 2026 | 「C$35.7B (~US$25.5B) · Series E first close · Oct 2026」。<br>公司 2026-10-29 新闻稿原文是「would represent a CAD $35.7 billion valuation」，前提是 C$7B 目标全部募足；首次交割，投前还是投后没有说明。<br>「$20B+」字面上不算错，但比公司公告低约 20%，而且 FT/NYT 报的「约 $20B」是 Cohere 与 Aleph Alpha 合并后整体的估值，容易混淆。 | https://www.newswire.ca/news-releases/cohere-announces-series-e-fundraise-targeting-cad-7-billion-to-meet-surging-global-demand-for-secure-sovereign-ai-811489745.html ・ https://www.unite.ai/cohere-closes-initial-series-e-targeting-up-to-cad-7b-at-cad-35-7b-valuation/ | major |
| 6 | Cohere (#7) | badge | 无 | 「MERGER PENDING (ALEPH ALPHA)」。2026-09-16 签了最终合并协议，尚待监管批准、未完成交割。Hugging Face 已标「NVIDIA DEAL PENDING」，Cohere 应当一致。 | https://siliconangle.com/2026/09/16/cohere-and-aleph-alpha-agree-to-merge-in-reported-20b-deal/ ・ https://www.techzine.eu/news/infrastructure/144361/cohere-and-aleph-alpha-merge-an-ai-company-with-two-headquarters/ | major |
| 7 | HeyGen (#10) | secondary_display | $200M · annual revenue · 2026 | 「$200M · ARR · Jun 2026」。2026-06-25 公告的是年化经常性收入（ARR），不是已实现的年营收，scope_note 里的「annual revenue」也要同步改。 | https://www.businesswire.com/news/home/20260625305891/en/HeyGen-Doubles-to-%24200M-ARR-in-Eight-Months-on-the-Rise-of-Identity-First-AI-Video ・ https://www.upstartsmedia.com/p/exclusive-heygen-200m-arr-without-burn | major |
| 8 | MiniMax (#14) | value / secondary_display | $7.3B · market cap · Oct 2026（10-22 收盘 HK$160.70） | 「$7.0B · market cap · Nov 2026」。2026-11-03 收盘 HK$155.70，按约 3.49 亿股算，市值约 HK$54.4B ≈ US$7.0B。scope_note 写明市值统一取 11-03 收盘，这一家却用了 10-22。 | https://stockanalysis.com/quote/hkg/0100/history/ ・ https://www.cnbc.com/quotes/100-HK | major |
| 9 | DeepSeek (#23) | value_display | $52B · valuation · Jul 2026 | **需要决定：**<br>• 2026-10-22 Reuters/Bloomberg 报道，新一轮约 ¥100B（约 $15B），由宁德时代和腾讯参与，投前约 ¥500B（约 $70–74B），「数日内完成」。<br>• The Information 10-23 报道已按 ¥106B 交割。<br>• 公司未确认，也没有公开投后估值。<br>建议改为「~$74B pre-money (reported) · Oct 2026」；若坚持只用确认已完成的交易，保留 $52B，并把日期改成「Jun 2026 round」（首轮约 2026 年 6 月中交割，7 月经安徽 Korrun 的公告披露）。 | https://techcrunch.com/2026/10/22/deepseek-reportedly-raises-15b-days-after-us-restrictions/ ・ https://www.chinadaily.com.cn/a/202610/22/WS6ad9b00ee4b06d4aa0564374.html ・ https://www.dealstreetasia.com/stories/deepseek-valuation-489350 | major |
| 10 | Moonshot AI (#20) | secondary_display / badge | $50B · valuation · Oct 2026；无徽章 | 改为「~$50B pre-money (reported)」。Caixin、21 世纪经济报道都写的是「投前估值约 500 亿美元」，募资额未披露，所以投后估值未知，与口径里的 post-money 不一致。<br>badge 可加「HK IPO FILED (REPORTED)」：Reuters 2026-09-03 报道已向港交所保密递表。 | https://www.caixinglobal.com/2026-09-11/in-depth-inside-the-50-billion-rise-of-moonshot-ai-102484028.html ・ https://m.21jingji.com/article/20260806/herald/fef0e6142bf1f168c015ec668e577745.html ・ https://www.dealstreetasia.com/stories/moonshot-hong-kong-ipo-494042/ | major |
| 11 | Stability AI (#9) | person / subtitle | Emad Mostaque — Founder (left 2024)；London, UK | 人物改为现任「Prem Akkaraju — CEO」（2024-06 起任，2026-08 融资稿仍是 CEO），其他卡都是现任负责人。<br>总部：tech.eu 2026-08 报道公司重心已从英国转到美国、关闭伦敦办公室，B 轮新闻稿落款也是 Los Angeles；但没有找到正式宣布迁总部的消息。建议写「Los Angeles / London」或向公司确认。 | https://tech.eu/2026/08/25/stabiityai-raises-76m-with-warner-and-sony-investing/ ・ https://kyodonewsprwire.jp/release/202608264689 ・ https://ca.finance.yahoo.com/news/stability-ai-exits-london-headquarters-182257762.html | major |
| 12 | Google DeepMind (#1) | person.role | Co-founder | 「Co-founder · Chair」或「Co-founder · Alphabet Chief Scientist」。2026-08-05 Hassabis 卸任 CEO，改任 Google DeepMind Chair 兼 Alphabet 首席科学家，日常运营由 Koray Kavukcuoglu（SVP）负责。<br>制作备注说这件事只有「单一来源」，实际已有多家独立来源，可以上卡。「Co-founder」本身没错，但不完整。 | https://engadget.com/2231124/google-deepmind-ceo-demis-hassabis-is-stepping-down-but-will-remain-with-the-company/ ・ https://9to5google.com/2026/08/05/demis-hassabis-deepmind/ ・ https://www.businesstoday.in/technology/news/story/google-deepmind-leadership-changes-547553-2026-08-06 | minor |
| 13 | Sakana AI (#24) | value / secondary_display | $2.65B · valuation · Nov 2025 | 「$2.7B · valuation · Apr 2026」。官方 Series B 页 2026-04-09 更新：总额约 ¥32B（约 $200M），新增 Google、Citi 等投资方，日文版写投后约 ¥4,320 亿（$2.7B）。 | https://sakana.ai/series-b/ ・ https://tech-dictionary.com/japan-ai-startup-talent-2026/（引用日经 2026-07-23） | minor |
| 14 | Luma AI (#13) | value_display（待定） | $4B · Nov 2025 | **单一来源，需要决定：** Forbes 2026-08-25 文中提到 Luma 2026-03 以 $9B 估值融资，但公司未确认，也找不到第二来源。CNBC 2026-05 仍用 $4B。<br>按两源规则可以保留 $4B（制作备注已注明）。产品可考虑写成「Luma Agents · Ray3」：2026-09 起新用户只能注册 Agents。 | https://www.forbes.com/sites/tylerroush/2026/08/25/carl-sagans-estate-sues-ai-startup-over-ad-allegedly-using-his-voice-without-permission/ ・ https://www.cnbc.com/2026/05/19/luma-ai-cnbc-disruptor-50-ranking.html ・ https://en.wikipedia.org/wiki/Luma_AI | minor |
| 15 | Hugging Face (#3) | secondary_display | $12.9B · Nvidia deal · Sep 2026 | 可以保留，但要知道构成：Nvidia 8-K 显示约 $11.9B 付给股东，另有最多约 $1.0B 员工留任股权。可写「$12.9B incl. retention」，或在 sources 里注明。交易待批，预计 2027 上半年交割，「DEAL PENDING」正确。 | https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000078/nvda-20260902.htm ・ https://unite.ai/nvidia-signs-definitive-agreement-to-acquire-hugging-face-for-12-9b | minor |
| 16 | Cursor (#17) | secondary_display | $60B · SpaceX deal · Jun 2026 | 「acquired · Aug 2026」更准确：2026-06-16 行权签约，08-14 交割；$60B 是隐含股权价值。SpaceX 的 8-K 已确认交割，制作备注说的「交割日期未确认」已不成立。 | https://www.sec.gov/Archives/edgar/data/0001181412/000162828026066482/spaceexplorationtechnologi.htm ・ https://www.techzine.eu/news/devops/143619/spacex-completes-acquisition-of-cursor/ | minor |
| 17 | MiniMax (#14) | tags / badge | Hailuo · Talkie · M2；LISTED IN HONG KONG | M2 已过时，2026-06-01 发布了 M3，建议写「Hailuo · Talkie · M3」。2026-05-29 已在上海 STAR 市场 A 股辅导备案，尚未上市，可在 notes 注明。 | https://llm-stats.com/models/minimax-m3 ・ https://m.jiemian.com/article/14511625.html | minor |
| 18 | Zhipu AI (#8) | value / badge | $26B · market cap | 数量级正确：11-03 收盘 HK$442.00，按 4.656 亿股算 ≈ HK$205.8B ≈ $26.2B；部分数据源按约 4.88 亿股，约 $27.7B。2026-06 申请上交所第二上市，尚未完成，可在 notes 注明。 | https://stockanalysis.com/quote/hkg/2513/ ・ https://www.caixinglobal.com/2026-06-02/zhipu-seeks-22-billion-shanghai-listing-to-fuel-ai-expansion-102450244.html | minor |
| 19 | Black Forest Labs (#28) | tags | FLUX.2 · FLUX.3；Image models | 官方写法是「FLUX 3」，不带点（2026-07-23 发布）。FLUX 3 已经涵盖视频，类别可改为「Image & video models」。 | https://bfl.ai/blog ・ https://datanorth.ai/news/black-forest-labs-releases-flux-3 | minor |
| 20 | xAI (#21) | person.role | Founder | 「Co-founder」。xAI 由 Musk 与 11 位研究员共同创立，其余联合创始人到 2026-03 已全部离开。 | https://en.wikipedia.org/wiki/SpaceXAI | minor |
| 21 | Mistral AI (#22) | value_display | €21B | 「€21B+」。官方原文是「more than €21 billion」post-money。 | https://techcrunch.com/2026/09/08/mistral-raises-e3b-as-sovereign-ai-becomes-big-business/ | minor |
| 22 | ElevenLabs (#15) | country flag | 美国旗；New York / London | 可以保留，但存在争议：tech.eu 称其为英国公司，维基百科信息框写 New York。观众可能质疑，建议在 sources 注明理由。 | https://en.wikipedia.org/wiki/ElevenLabs | minor |
| 23 | Unitree (#4) | person.role | Founder & CEO | 招股书写的是董事长、总经理兼 CTO。「Founder & Chairman」更准确，「CEO」可以视为口语化的简写。市值复算：约 4.045 亿股 × 11-03 收盘约 ¥624.58 ≈ ¥252.6B ≈ $37.6B，$38B 正确。 | https://news.10jqka.com.cn/20260807/c678758290.shtml ・ https://finance.yahoo.com/quote/688836.SS/ | minor |
| 24 | Figure AI (#18) | tags | Figure 03 · Helix | 可以写「Helix 02」（2026-01 发布）。其余正确：$39B 是 Series C 投后估值，没有找到 2026 年完成的新一轮；总部 2025-03 已迁到 San Jose。 | https://www.therobotreport.com/figure-ai-raises-1b-in-series-c-funding-toward-humanoid-robot-development/ ・ https://therealdeal.com/san-francisco/2025/03/17/figure-ai-leases-99k-sf-for-new-san-jose-headquarters-plant | minor |
| 25 | 洞察卡 #5（after_rank 28） | text | Google owns DeepMind, SpaceX owns xAI and Cursor, and Nvidia is buying Hugging Face. | 内容属实：Cursor 已于 2026-08-14 交割，Hugging Face 交易待批。但若第 21 张卡改名 SpaceXAI，这里要同步写成「SpaceX owns xAI (now SpaceXAI) and Cursor」。 | 同第 4、15、16 条 | minor |
| 26 | 洞察卡 #4（after_rank 23） | text | DeepSeek-R1's launch wiped about $589B off Nvidia's market value in one day (Jan 2025). | 数字有据：2025-01-27 Nvidia 单日跌约 17%、蒸发约 $589B（Bloomberg 口径，Reuters 口径约 $593B）。但 R1 是 01-20 发布的，下跌发生在一周后。建议改成「Fears over DeepSeek-R1 wiped about $589B off Nvidia's market value in one day (Jan 27, 2025).」，避免把发布写成当天的直接原因。 | https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-loses-usd589-billion-in-market-cap-broad-stock-plunge-triggered-by-deepseek-ai-release ・ https://www.dawn.com/news/1888233 | minor |

### 其他非问题备注（无需改卡）

- **Anthropic：** $965B 是 Series H 投后估值（2026-05）。公开 S-1 于 2026-10-26 递交，纳斯达克代码 ANT，截至 11-03 未定价、未上市。如果发布前已上市，要改用市值。媒体报的 $1.5–2T 是 IPO 预期估值，不要使用。
- **OpenAI：** 10 月新一轮（$1.25T 投前）仍未交割，FT 报道目标已下调，不应采用。发布前再查一次是否已首次交割。
- **Perplexity、Thinking Machines、Cognition：** 2026 年分别有 $30B+、$40B+、$70–80B 的洽谈报道，都没有完成，不使用是正确的。
- **Safe Superintelligence：** Nvidia 2026-07-27 战略投资（媒体称 $5B），金额和估值都未披露，$32B 仍是最近披露的估值，可以在 notes 注明。「NO PRODUCT YET」正确。
- **Suno：** UMG、Sony 的诉讼仍在进行（2026-09-18 又起诉一次）；Warner 2025-11 已和解。网上有「UMG 与 Suno 和解」的说法，是错的，和解的是 Udio。

## 核对无误的公司

下列公司的成立年份、主数字及日期和口径、徽章、总部、产品、人物，都与独立来源一致。部分公司有上表的 minor 措辞建议，但不影响发布。

- **Synthesia (#5)：** $4B，Series E，2026-01。
  - https://tech.eu/2026/01/26/synthesia-doubles-valuation-to-4bn-in-12-months-following-200m-funding-round/
  - https://www.lw.com/en/news/2026/01/latham-watkins-advises-synthesia-on-us200-million-series-e-and-secondary-transaction
- **Runway (#6)：** $5.3B，Series E，2026-02-10。
  - https://techcrunch.com/2026/02/10/ai-video-startup-runway-raises-315m-at-5-3b-valuation-eyes-more-capable-world-models/
- **Anthropic (#11)：** $965B，IPO FILED，代码 ANT。
  - https://www.orrick.com/en/News/2026/05/Anthropic-Raises-65B-Series-H-at-965B-Post-Money-Valuation
  - https://www.iposcoop.com/the-ipo-buzz-anthropic-ant-proposed-files-its-s-1/
- **Midjourney (#12)：** 无外部投资者；V8 已发布（V8.2 为默认）。
  - https://techcrunch.com/2025/08/22/meta-partners-with-midjourney-on-ai-image-and-video-models
  - https://the-decoder.com/midjourney-v8-rolls-out-with-5x-faster-generation-but-charges-4x-more-for-its-best-features/
- **Suno (#16)：** $5.4B 投后，Series D，2026-06-03；v6 与 Studio 都存在。
  - https://siliconangle.com/2026/06/03/generative-ai-music-startup-suno-ai-raises-400m-5-4b-valuation/
  - https://suno.com/blog/introducing-v6
- **Perplexity (#19)：** $20B，2025-09，最近一次完成的融资；2026-08 的 $30B+ 仍在洽谈。
  - https://techfundingnews.com/perplexity-raises-200m-at-20b-valuation-ai-search/
- **Cognition (#25)：** $48B，Series E，2026-09；Windsurf 2026-06 改名 Devin Desktop。
  - https://www.lw.com/en/news/2026/09/latham-watkins-advises-cognition-on-series-e
  - https://www.thestar.com.my/tech/tech-news/2026/09/09/cognition-ai-raises-2-billion-at-48-billion-valuation
- **Lovable (#26)：** $13.3B，$400M Series C，2026-08-12。
  - https://thenextweb.com/news/lovable-400m-series-c-13-3bn-scaleup-europe-fund
  - https://tech.eu/2026/08/12/lovables-valuation-doubles-to-13bn-as-raises-400m/
- **Higgsfield AI (#27)：** $5.4B，Series B，2026-08-17。
  - https://www.thestar.com.my/tech/tech-news/2026/08/17/higgsfield039s-valuation-soars-fourfold-to-54-billion-in-six-months-on-ai-content-demand
  - https://thenextweb.com/news/higgsfield-series-b-400m-5-4bn-valuation-700m-revenue
- **Safe Superintelligence (#29)：** $32B，2025-04，仍是最近披露的估值；无产品。
  - https://builtin.com/articles/safe-superintelligence-raises-2b-32b-valuation-20250415
- **Thinking Machines Lab (#30)：** $12B 投后，种子轮，2025-07；Tinker 与 Inkling 都存在。
  - https://techcrunch.com/2025/07/15/mira-muratis-thinking-machines-lab-is-worth-12b-in-seed-round/
  - https://rits.shanghai.nyu.edu/ai/thinking-machines-releases-inkling-its-first-open-weight-model/

**主值核对无误、仅有 minor 措辞项：** Hugging Face、Unitree、Zhipu、Luma（$9B 单一来源待定）、Cursor、Figure AI、Mistral、Black Forest Labs、Google DeepMind（主值无误，人物身份见第 12 条）。

### 洞察卡核对

| # | 结论 | 依据 |
|---|---|---|
| 1 Hugging Face 起家是青少年聊天机器人 App | 属实 | https://techcrunch.com/2017/03/09/hugging-face-wants-to-become-your-artificial-bff/ |
| 2 Cohere CEO 合著《Attention Is All You Need》 | 属实，Aidan N. Gomez 是 8 位作者之一 | https://arxiv.org/abs/1706.03762 |
| 3 Midjourney 从未拿外部投资；Meta 2025-08 授权其技术 | 属实（2025-08-22 授权「aesthetic technology」；Holz 称公司没有投资者，至今未见外部融资报道） | https://techcrunch.com/2025/08/22/meta-partners-with-midjourney-on-ai-image-and-video-models ・ https://venturebeat.com/ai/meta-is-partnering-with-midjourney-and-will-license-its-technology-for-future-models-and-products |
| 4 DeepSeek-R1 致 Nvidia 单日蒸发约 $589B | 数字属实，因果措辞建议微调（见第 26 条） | 见第 26 条 |
| 5 Google / SpaceX / Nvidia 归属 | 属实；xAI 改名后要同步（见第 25 条） | 见第 4、15、16 条 |

### 未能核实 / 局限

- Bloomberg、Forbes 有付费墙，相关内容只能通过转载或搜索摘要核对。
- DeepSeek 10 月轮是否已交割，公司未确认。
- Luma 的 $9B 只有单一来源。
- SpaceXSI 是法定改名还是只改了品牌，尚不明确。
- Stability AI 是否正式迁了总部，没有找到公告。
- 11-03 的人民币中间价没有查到官方值，Unitree 市值用的是 10-30 汇率 6.7138 估算。
- 上市公司市值（Unitree、Zhipu、MiniMax）波动大，发布前 7 天内必须刷新。
