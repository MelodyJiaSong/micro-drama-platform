# ep03 · 数据出处、交叉核对与图片许可（sources.md）

> 由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_ab.py` / `items_c.py` 后依次跑 `make_items_def.py` → `build.py` → `gen_sources.py`。调研原始记录在 `_build/research/batch_*.json`（含创始人全名单、员工数、未采用的洽谈中估值等）。

## 1. 口径

30 well-known AI-native companies (language, image, video, voice & music, coding, search, robotics), listed by founding year, not ranked. Value = latest completed private round (post-money), market cap for listed companies (close of Nov 3, 2026 unless dated otherwise), or the acquisition price for companies bought by others. Where no recent valuation exists, the card says what the number is (raised / ARR / share sale / pre-money). Flags show headquarters country. Sources for every number are listed below.

- 顺序：成立年月从老到新；只知道年份的用占位月份排序，屏上只显示年份（见 topic.md）。
- 主值来源分级：公司公告 / 交易所 > 主流财经媒体（Bloomberg、Reuters、CNBC、TechCrunch、Caixin…）> 聚合站；维基百科只作交叉核对（follow-up 009）。
- 调研子代理打不开部分新闻站，只见搜索摘要的条目已在 notes 注明；OpenAI、Anthropic、Cursor、Hugging Face 四条由主代理再次搜索核对（2026-11-03）。

## 2. 逐条

### 1. Google DeepMind（EST. 2010，London, UK）

- 卡上：**Google-owned** since 2014；徽章 PART OF ALPHABET
- 主值来源：[Google DeepMind / Alphabet (acquired by Google 26 Jan 2014)](https://en.wikipedia.org/wiki/Google_DeepMind)（取于 2026-11-03）
- 交叉核对：无第二独立来源（见备注）
- 备注：Subsidiary: no standalone valuation. Merged with Google Brain Apr 2023. Research reports Hassabis moved to chair + Alphabet chief scientist in Aug 2026 (single source) — confirmed by independent QC (several sources): role shown as 'Co-founder & Chair'. [QC 2026-11-04 independent fact-check: qc_data_independent.md]
- 头像：Demis Hassabis（Co-founder & Chair）

### 2. OpenAI（EST. 2015，San Francisco, USA）

- 卡上：**$852B** valuation · Mar 2026；徽章 IPO FILED
- 主值来源：[Bloomberg: OpenAI valued at $852B after completing $122B round (2026-03-31)](https://www.bloomberg.com/news/articles/2026-03-31/openai-valued-at-852-billion-after-completing-122-billion-round)（取于 2026-11-03）
- 交叉核对：[SiliconANGLE](https://siliconangle.com/?p=736979)，852B，差 0.0%
- 备注：Post-money. A new round at ~$1.25T reported open (CNBC 2026-10-31) — not completed, not used. Sora app/API shut down in 2026 (announced 2026-03-24), so it is not listed as a product. Confidential S-1 announced by OpenAI 2026-06-08 → badge IPO FILED. [QC 2026-11-04 independent fact-check: qc_data_independent.md]
- 头像：Sam Altman（Co-founder & CEO）

### 3. Hugging Face（EST. 2016，New York, USA）

- 卡上：**$12.9B** Nvidia deal · Sep 2026；徽章 NVIDIA DEAL PENDING
- 主值来源：[Nvidia agrees to acquire Hugging Face for $12.93B (announced 2026-09-03)](https://forklog.com/en/nvidia-agrees-to-acquire-hugging-face-for-12-93-billion/)（取于 2026-11-03）
- 交叉核对：[La Nación (AP)](https://www.lanacion.com.ar/usa/nvidia-buying-artificial-intelligence-platform-hugging-face-for-13-billion-nid03092026/)，13B，差 0.5%
- 备注：Founded 2016 (month not confirmed; sorted as 2016-01 placeholder before Unitree 2016-08). Last priced round $4.5B (Aug 2023) is >18 months old; acquisition price used. Deal pending regulatory approval, expected H1 2027. The $12.93B includes ~$1B of employee retention equity. [QC 2026-11-04 independent fact-check: qc_data_independent.md]
- 头像：Clément Delangue（Co-founder & CEO）

### 4. Unitree Robotics（EST. 2016，Hangzhou, China）

- 卡上：**$38B** market cap · Nov 2026；徽章 LISTED IN SHANGHAI
- 主值来源：[StockAnalysis 688836.SH, close 2026-11-03: CNY 252.62B](https://stockanalysis.com/quote/sha/688836/)（取于 2026-11-03）
- 交叉核对：[Yahoo Finance 688836.SS](https://finance.yahoo.com/quote/688836.SS/)，37.86B，差 0.4%
- 备注：STAR Market IPO 2026-08-19. CNY→USD at ~6.67. Volatile: re-check within 7 days of publishing.
- 头像：Wang Xingxing（Founder & Chairman）

### 5. Synthesia（EST. 2017，London, UK）

- 卡上：**$4B** valuation · Jan 2026
- 主值来源：[UCL News: Synthesia valued at $4B (Series E, Jan 2026)](https://www.ucl.ac.uk/news/2026/jan/ai-video-startup-co-founded-ucl-professor-valued-4-billion)（取于 2026-11-03）
- 交叉核对：[Built In](https://builtin.com/articles/synthesia-raises-200m-series-e-20260126)，4B，差 0.0%
- 备注：Founded 2017 (month unknown; mid-year placeholder for ordering).
- 头像：Victor Riparbelli（Co-founder & CEO）

### 6. Runway（EST. 2018，New York, USA）

- 卡上：**$5.3B** valuation · Feb 2026
- 主值来源：[Bloomberg: Runway valued at $5.3B (2026-02-10)](https://bloomberg.com/news/articles/2026-02-10/ai-video-startup-runway-valued-at-5-3-billion-with-new-funding)（取于 2026-11-03）
- 交叉核对：[SiliconANGLE](https://siliconangle.com/?p=730553)，5.3B，差 0.0%
- 备注：Founded 2018 (month unknown; mid-year placeholder).
- 头像：Cristóbal Valenzuela（Co-founder & CEO）

### 7. Cohere（EST. 2019，Toronto, Canada）

- 卡上：**C$35.7B** valuation · Oct 2026；徽章 MERGER PENDING
- 主值来源：[Cohere news release (Newswire, 2026-10-29): Series E targeting CAD $7B at a CAD $35.7B valuation](https://www.newswire.ca/news-releases/cohere-announces-series-e-fundraise-targeting-cad-7-billion-to-meet-surging-global-demand-for-secure-sovereign-ai-811489745.html)（取于 2026-11-03）
- 交叉核对：[BetaKit: C$35.7B post-money (~US$25.5B)](https://betakit.com/canada-to-invest-up-to-1-6-billion-in-ai-firm-cohere/)，25.5B，差 0.0%
- 备注：Sources differ >10%: Bloomberg 'over $20B' vs BetaKit C$35.7B post-money (~$25.5B). Independent QC found Cohere's own release (2026-10-29) states C$35.7B post-money (assuming the full C$7B is raised), so the card now shows the company's figure in CAD (≈US$25.5B), as Mistral shows euros; Bloomberg's 'over $20B' likely refers to another basis. Series E only at initial close. Aleph Alpha merger signed 2026-09-16, not yet closed → badge MERGER PENDING. Founded 2019 (month unknown). [QC 2026-11-04 independent fact-check: qc_data_independent.md]
- 头像：Aidan Gomez（Co-founder & CEO）

### 8. Zhipu AI (Z.ai)（EST. 2019，Beijing, China）

- 卡上：**$26B** market cap · Nov 2026；徽章 LISTED IN HONG KONG
- 主值来源：[StockAnalysis 2513.HK, close 2026-11-03: HK$205.81B](https://stockanalysis.com/quote/hkg/2513/)（取于 2026-11-03）
- 交叉核对：无第二独立来源（见备注）
- 备注：HKEX IPO 2026-01-08 — first LLM developer to list. Founders incl. Tang Jie and Li Juanzi (Tsinghua KEG); Zhang Peng is CEO (not a founding professor) — role shown as CEO. HKD→USD 7.845. Volatile.
- 头像：Zhang Peng（CEO）

### 9. Stability AI（EST. 2019，London, UK）

- 卡上：**$76M** raised · Aug 2026
- 主值来源：[Stability AI raised $76M Series B (Aug 2026, valuation undisclosed)](https://stability.ai/news)（取于 2026-11-03）
- 交叉核对：无第二独立来源（见备注）
- 备注：Last disclosed valuation $1B (Oct 2022) is >18 months old, so the latest raise is shown instead (labelled 'raised'). CEO since 2024: Prem Akkaraju. Founded 2019 (month unknown).
- 头像：Emad Mostaque（Founder (left 2024)）

### 10. HeyGen（EST. 2020，Los Angeles, USA）

- 卡上：**$200M** ARR · Jun 2026
- 主值来源：[HeyGen blog: surpasses $200M ARR (2026-06-25)](https://www.heygen.com/blog/heygen-surpasses-200m-arr)（取于 2026-11-03）
- 交叉核对：无第二独立来源（见备注）
- 备注：Last priced round $500M (Jun 2024) is >18 months old; ARR (annual recurring revenue) shown instead, labelled 'ARR'. Founded 2020 (month unknown).
- 头像：Joshua Xu（Co-founder & CEO）

### 11. Anthropic（EST. 2021，San Francisco, USA）

- 卡上：**$965B** valuation · May 2026；徽章 IPO FILED
- 主值来源：[Anthropic newsroom: Series H ($65B at $965B post-money)](https://www.anthropic.com/news/series-h)（取于 2026-11-03）
- 交叉核对：[GV Wire (Reuters)](https://gvwire.com/2026/05/28/anthropic-secures-965-billion-valuation-after-raising-65-billion/)，965B，差 0.0%
- 备注：Public S-1 filed 2026-10-26 (Nasdaq: ANT). If it lists before publishing, switch to market cap. Founded 2021 (month: early 2021).
- 头像：Dario Amodei（Co-founder & CEO）

### 12. Midjourney（EST. 2021，San Francisco, USA）

- 卡上：**Self-funded** no outside investors
- 主值来源：[Reuters via The Star: Meta licenses Midjourney tech; Holz says it stays investor-free (2025-08-25)](https://www.thestar.com.my/tech/tech-news/2025/08/25/meta-partners-with-midjourney-to-license-ai-tech-for-future-products)（取于 2026-11-03）
- 交叉核对：无第二独立来源（见备注）
- 备注：Never raised outside capital; no real valuation exists ($5–10B figures online come from content farms).
- 头像：David Holz（Founder & CEO）

### 13. Luma AI（EST. 2021，Palo Alto, USA）

- 卡上：**$4B** valuation · Nov 2025
- 主值来源：[CNBC: Luma AI raises $900M led by HUMAIN (2025-11-19)](https://www.cnbc.com/2025/11/19/luma-ai-raises-900-million-in-funding-led-by-saudi-ai-firm-humain.html)（取于 2026-11-03）
- 交叉核对：[Bloomberg (BGov)](https://news.bgov.com/artificial-intelligence/saudis-humain-backs-ai-video-startup-luma-at-4-billion-value)，4B，差 0.0%
- 备注：Forbes-reported $9B not confirmed by the company — not used.
- 头像：Amit Jain（Co-founder & CEO）

### 14. MiniMax（EST. 2021，Shanghai, China）

- 卡上：**$7.0B** market cap · Nov 2026；徽章 LISTED IN HONG KONG
- 主值来源：[StockAnalysis 0100.HK price history: close HK$155.70 on 2026-11-03 (~349M shares → ≈HK$54.4B ≈ US$7.0B)](https://stockanalysis.com/quote/hkg/0100/history/)（取于 2026-11-03）
- 交叉核对：[CNBC quote 100-HK](https://www.cnbc.com/quotes/100-HK)，7B，差 0.0%
- 备注：HKEX 00100 since 2026-01-09. Peaked >HK$410B in Mar 2026; very volatile — refresh before publishing. Updated to the 2026-11-03 close (HK$155.70 → ≈US$7.0B) per independent QC; flagship model now M3. [QC 2026-11-04 independent fact-check: qc_data_independent.md]
- 头像：Yan Junjie（Founder & CEO）

### 15. ElevenLabs（EST. 2022，New York / London）

- 卡上：**$22B** share sale · Sep 2026
- 主值来源：[Tech.eu: ElevenLabs doubles valuation to $22B with $300M employee tender (2026-09-30)](https://tech.eu/2026/09/30/elelvenlabs-doubles-valuation-to-22bn-with-300m-employee-tender-offer/)（取于 2026-11-03）
- 交叉核对：[Sifted](https://sifted.eu/articles/elevenlabs-doubles-valuation-to-22bn-with-tender-offer/)，22B，差 0.0%
- 备注：$22B is a secondary (employee tender) price, not a primary round; last primary round Series D $11B (Feb 2026). Card labels it 'share sale' (employee tender) rather than a funding round. Flag = US (legal HQ New York); largest office London; Polish founders. Founded 2022 (month unknown).
- 头像：Mati Staniszewski（Co-founder & CEO）

### 16. Suno（EST. 2022，Cambridge, USA）

- 卡上：**$5.4B** valuation · Jun 2026
- 主值来源：[Suno blog: Series D](https://suno.com/blog/series-d-announcement)（取于 2026-11-03）
- 交叉核对：[TechCrunch (2026-06-03)](https://techcrunch.com/2026/06/03/still-facing-copyright-lawsuits-ai-music-generator-suno-raises-another-400m/)，5.4B，差 0.0%
- 备注：Founded 2022 (month unknown; placeholder). UMG / Sony litigation ongoing.
- 头像：Mikey Shulman（Co-founder & CEO）

### 17. Cursor (Anysphere)（EST. 2022，San Francisco, USA）

- 卡上：**$60B** SpaceX deal · Aug 2026；徽章 PART OF SPACEX
- 主值来源：[CNBC: SpaceX to acquire Cursor for $60B (announced 2026-06-16; closed 2026-08-14 per 8-K)](https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html)（取于 2026-11-03）
- 交叉核对：[TechCrunch](https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo/)，60B，差 0.0%
- 备注：All-stock acquisition announced 2026-06-16; closed 2026-08-14 (8-K, confirmed by independent QC) — card dates it to the close. Founded 2022 (month unknown).
- 头像：Michael Truell（Co-founder & CEO）

### 18. Figure AI（EST. 2022，San Jose, USA）

- 卡上：**$39B** valuation · Sep 2025
- 主值来源：[TechCrunch: Figure reaches $39B valuation (2025-09-16)](https://techcrunch.com/2025/09/16/figure-reaches-39b-valuation-in-latest-funding-round/)（取于 2026-11-03）
- 交叉核对：[Bloomberg Law](https://news.bloomberglaw.com/artificial-intelligence/robotics-startup-figure-ai-valued-at-39-billion-in-new-funding)，39B，差 0.0%
- 备注：Founding month reported as Jan or May 2022. HQ San Jose (some sources Sunnyvale).
- 头像：Brett Adcock（Founder & CEO）

### 19. Perplexity（EST. 2022，San Francisco, USA）

- 卡上：**$20B** valuation · Sep 2025
- 主值来源：[The Information: Perplexity finalizes $20B valuation round](https://www.theinformation.com/briefings/perplexity-finalizes-20-billion-valuation-round)（取于 2026-11-03）
- 交叉核对：[TechCrunch](https://techcrunch.com/2025/09/10/perplexity-reportedly-raised-200m-at-20b-valuation/)，20B，差 0.0%
- 备注：Reported, not officially announced. Aug 2026 talks at $30B+ not completed.
- 头像：Aravind Srinivas（Co-founder & CEO）

### 20. Moonshot AI（EST. 2023，Beijing, China）

- 卡上：**$50B** pre-money · Oct 2026；徽章 HK IPO FILED
- 主值来源：[Bloomberg via The Edge Malaysia: Moonshot closes final private round at $50B (2026-10-06)](https://theedgemalaysia.com/node/820677)（取于 2026-11-03）
- 交叉核对：[AI Weekly](https://aiweekly.co/alerts/moonshot-ai-closes-final-private-round-at-50b-eyes-hong-kong-ipo-up-to-5b-in-q1)，50B，差 0.0%
- 备注：Bloomberg citing people familiar; not confirmed by the company; independent QC: reported as pre-money, so the card says pre-money. Confidential Hong Kong IPO filing (Reuters 2026-09-03), listing targeted Q1 2027 → badge HK IPO FILED. [QC 2026-11-04 independent fact-check: qc_data_independent.md]
- 头像：Yang Zhilin（Founder & CEO）

### 21. xAI（EST. 2023，Palo Alto, USA）

- 卡上：**$250B** SpaceX deal · Feb 2026；徽章 NOW SPACEXAI
- 主值来源：[Entrepreneur: Musk merges SpaceX and xAI (xAI valued at $250B, 2026-02)](https://www.entrepreneur.com/business-news/elon-musk-merges-spacex-and-xai-into-1-trillion-company/502373)（取于 2026-11-03）
- 交叉核对：无第二独立来源（见备注）
- 备注：Acquired by SpaceX 2026-02-02 (all-stock); rebranded SpaceXAI (Jul 2026), Musk said 2026-10-04 it will become SpaceXSI (effective date unknown). Badge NOW SPACEXAI (renamed 2026-07-06; parent SpaceX listed on Nasdaq 2026-06-12, SPCX). HQ: Palo Alto per Wikipedia, some outlets say San Francisco. All 11 other co-founders had left by Mar 2026. Cross-check: CNBC reported a Jan 2026 Series E at ~$230B (8.7% lower; unconfirmed by the company; article URL not recorded by research).
- 头像：Elon Musk（Co-founder）

### 22. Mistral AI（EST. 2023，Paris, France）

- 卡上：**€21B+** valuation · Sep 2026
- 主值来源：[Mistral AI newsroom: Series D (€3B, >€21B post-money)](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/)（取于 2026-11-03）
- 交叉核对：[TechCrunch (2026-09-08)](https://techcrunch.com/2026/09/08/mistral-raises-e3b-as-sovereign-ai-becomes-big-business/)，24.5B，差 0.0%
- 备注：Shown in euros as announced (>€21B post-money ≈ $24.5B).
- 头像：Arthur Mensch（Co-founder & CEO）

### 23. DeepSeek（EST. 2023，Hangzhou, China）

- 卡上：**$52B** valuation · Jul 2026
- 主值来源：[Caixin Global: DeepSeek reaches $52B valuation (2026-07-17)](https://www.caixinglobal.com/2026-07-17/deepseek-reaches-52-billion-valuation-in-round-backed-by-tencent-catl-102465358.html)（取于 2026-11-03）
- 交叉核对：[The Decoder (~$50B)](https://the-decoder.com/deepseek-takes-outside-money-for-the-first-time-at-a-50-billion-valuation/)，50B，差 3.8%
- 备注：First outside money (Series A). A larger round (~CNY 100B at ~$70–74B pre-money) reported in Oct 2026; The Information says it closed but the company has not confirmed — not used (independent QC 2026-11-04 flagged it; agent kept the confirmed figure). Date: Caixin reported the completed round on 2026-07-17, so the card keeps Jul 2026. STAR Market IPO reportedly in preparation.
- 头像：Liang Wenfeng（Founder & CEO）

### 24. Sakana AI（EST. 2023，Tokyo, Japan）

- 卡上：**$2.7B** valuation · Apr 2026
- 主值来源：[Sakana AI Series B page (updated 2026-04-09): ~¥32B raised, post-money ≈¥432B ≈ US$2.7B](https://sakana.ai/series-b/)（取于 2026-11-03）
- 交叉核对：[TechCrunch: Series B at $2.65B (2025-11-17, first close)](https://techcrunch.com/2025/11/17/sakana-ai-raises-135m-series-b-at-a-2-65b-valuation-to-continue-building-ai-models-for-japan)，2.65B，差 1.9%
- 备注：Co-founders David Ha (CEO), Llion Jones (Transformer paper co-author), Ren Ito. Google investment Jan 2026. Company page (updated 2026-04) states post-money ≈¥432B (≈US$2.7B) per independent QC; Series B was $2.65B (Nov 2025). [QC 2026-11-04 independent fact-check: qc_data_independent.md]
- 头像：David Ha（Co-founder & CEO）

### 25. Cognition（EST. 2023，San Francisco, USA）

- 卡上：**$48B** valuation · Sep 2026
- 主值来源：[Cognition blog: Series E](https://cognition.com/blog/series-e)（取于 2026-11-03）
- 交叉核对：[PYMNTS](https://pymnts.com/news/artificial-intelligence/2026/cognition-secures-48-billion-valuation-as-demand-for-ai-coding-surges)，48B，差 0.0%
- 备注：Founded 2023 (Aug or Nov per sources). Acquired Windsurf (Jul 2025), renamed Devin Desktop (Jun 2026).
- 头像：Scott Wu（Co-founder & CEO）

### 26. Lovable（EST. 2023，Stockholm, Sweden）

- 卡上：**$13.3B** valuation · Aug 2026
- 主值来源：[Lovable blog: Series C](https://lovable.dev/blog/series-c)（取于 2026-11-03）
- 交叉核对：[Tech.eu (2026-08-12)](https://tech.eu/2026/08/12/lovables-valuation-doubles-to-13bn-as-raises-400m/)，13.3B，差 0.0%
- 备注：Founded 2023 (month unknown; placeholder); grew out of the open-source GPT Engineer project.
- 头像：Anton Osika（Co-founder & CEO）

### 27. Higgsfield AI（EST. 2023，San Francisco, USA）

- 卡上：**$5.4B** valuation · Aug 2026
- 主值来源：[Bloomberg via BNN Bloomberg: Higgsfield valuation soars to $5.4B (2026-08-17)](https://bnnbloomberg.ca/business/company-news/2026/08/17/higgsfields-valuation-soars-fourfold-to-us54-billion-in-six-months-on-ai-content-demand)（取于 2026-11-03）
- 交叉核对：[The Next Web](https://thenextweb.com/news/higgsfield-series-b-400m-5-4bn-valuation-700m-revenue)，5.4B，差 0.0%
- 备注：Replaces Pika (pivoted to a consumer social app in late 2025; last valuation $470M, Jun 2024). Founded 2023 (month unknown; placeholder).
- 头像：Alex Mashrabov（Co-founder & CEO）

### 28. Black Forest Labs（EST. 2024，Freiburg, Germany）

- 卡上：**$3.25B** valuation · Dec 2025
- 主值来源：[Black Forest Labs Series B press release (via NatLawReview)](https://natlawreview.com/press-releases/update-black-forest-labs-announces-series-b-investment-accelerate-frontier)（取于 2026-11-03）
- 交叉核对：[Tech.eu (2025-12-01)](https://tech.eu/2025/12/01/black-forest-labs-secures-300m-series-b-at-325b-valuation/)，3.25B，差 0.0%
- 备注：Founded 2024 (month unknown; placeholder). Founders built Stable Diffusion's core tech before leaving Stability AI.
- 头像：Robin Rombach（Co-founder & CEO）

### 29. Safe Superintelligence（EST. 2024，Palo Alto / Tel Aviv）

- 卡上：**$32B** valuation · Apr 2025；徽章 NO PRODUCT YET
- 主值来源：[TechCrunch (citing FT): SSI valued at $32B (2025-04-12)](https://techcrunch.com/2025/04/12/openai-co-founder-ilya-sutskevers-safe-superintelligence-reportedly-valued-at-32b)（取于 2026-11-03）
- 交叉核对：[Built In](https://builtin.com/articles/safe-superintelligence-raises-2b-32b-valuation-20250415)，32B，差 0.0%
- 备注：EXCEPTION to bible §3.3: value is 19 months old (no later disclosed valuation; Nvidia invested $5B in Jul 2026 at undisclosed value). Needs user sign-off. Co-founder Daniel Gross left for Meta (Jul 2025).
- 头像：Ilya Sutskever（Co-founder & CEO）

### 30. Thinking Machines Lab（EST. 2025，San Francisco, USA）

- 卡上：**$12B** valuation · Jul 2025
- 主值来源：[TechCrunch: Thinking Machines Lab worth $12B in seed round (2025-07-15)](https://techcrunch.com/2025/07/15/mira-muratis-thinking-machines-lab-is-worth-12b-in-seed-round/)（取于 2026-11-03）
- 交叉核对：[Business Today](https://www.businesstoday.in/technology/news/story/former-openai-cto-mira-muratis-ai-startup-thinking-machines-valued-at-12-billion-in-early-stage-funding-484805-2025-07-16)，12B，差 0.0%
- 备注：$10B vs $12B = pre vs post-money. A $40B+ round reported in talks — not used.
- 头像：Mira Murati（Founder & CEO）

## 3. 洞察卡

- 在 Hugging Face 之后：Hugging Face began as a chatbot app for teenagers before becoming the hub for AI models.
- 在 Runway 之后：Next: Cohere. Its CEO co-wrote 'Attention Is All You Need', the 2017 Transformer paper.
- 在 Midjourney 之后：Midjourney never took outside money. Meta licensed its tech instead (Aug 2025).
- 在 DeepSeek 之后：Fears over DeepSeek-R1 wiped about $589B off Nvidia's value in one day (Jan 27, 2025).
- 在 Black Forest Labs 之后：Google owns DeepMind, SpaceX owns xAI and Cursor, and Nvidia is buying Hugging Face.

依据：Hugging Face 早期为青少年聊天机器人（调研 A fun_fact）；Aidan Gomez 为《Attention Is All You Need》作者之一（arXiv 1706.03762）；Midjourney 未外部融资、Meta 2025-08 授权其技术（Reuters / The Star）；DeepSeek-R1 发布后 Nvidia 单日市值蒸发约 $589B（2025-01，调研 C）；第 5 条由本表 badge 与 status 汇总。

## 4. 图片来源与许可

全部候选与 meta 在 `assets/ref/<公司>/<logo|photo|person>/`（Codex 联网搜，6 轮，见 topic.md）。下表为进卡的图。

| 文件 | 类 | 来源页 | 作者 / 来源 | 许可（照抄来源页） |
|---|---|---|---|---|
| `assets/img/01_google_deepmind.jpg` | photo | https://time.com/7013685/google-ai-deepmind-military-contracts-israel/ | Jose Sarmento Matos—Bloomberg/Getty Images | unknown |
| `assets/img/01_google_deepmind_alt.jpg` | photo | https://www.flickr.com/photos/georgegillams/34802105193/ | George Gillams | CC BY-SA 2.0 |
| `assets/logo/google_deepmind.png` | logo | https://logos-download.com/brands/google-deepmind | Google DeepMind / Google | Trademark of Google DeepMind; identification only (source terms: All logos are the property of their respective owners.) |
| `assets/person/google_deepmind.jpg` | person | https://www.flickr.com/photos/georgegillams/34802105193/ | George Gillams | CC BY-SA 2.0 |
| `assets/img/02_openai.jpg` | photo | https://www.skbarchitects.com/work/openai | Andrew Giammarco / SkB Architects | unknown |
| `assets/img/02_openai_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/openai.png` | logo | https://brandfetch.com/openai.com | OpenAI | Trademark of OpenAI; identification only (source terms: unknown) |
| `assets/person/openai.jpg` | person | https://www.qf.org.qa/education-city-speaker-series/experts/sam-altman | Photographer and image owner unstated; published by Qatar Foundation | Copyright © 2026 Qatar Foundation. All rights reserved. |
| `assets/img/03_hugging_face.jpg` | photo | https://www.latent.space/p/idefics | Latent Space; individual photographer not credited | unknown |
| `assets/img/03_hugging_face_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/hugging_face.png` | logo | https://huggingface.co/brand | Hugging Face | Trademark of Hugging Face; identification only (source terms: unknown) |
| `assets/person/hugging_face.jpg` | person | https://www.amd.com/en/corporate/events/advancing-ai/developer-sessions.html | Photographer and image owner unstated; published by AMD | unknown |
| `assets/img/04_unitree.jpg` | photo | https://newatlas.com/robotics/unitree-g1-humanoid-agent/ | Unitree | unknown |
| `assets/img/04_unitree_alt.jpg` | photo | https://www.pexels.com/photo/futuristic-robotic-dog-at-tech-exhibit-40049039/ | Tori D | Pexels License |
| `assets/logo/unitree.png` | logo | https://www.unitree.com/ | Unitree Robotics / Yushu Technology Co., Ltd. | Trademark of Unitree Robotics; identification only (source terms: Yushu Technology Co., Ltd. All Rights Reserved) |
| `assets/person/unitree.jpg` | person | https://gte-forum.com/en/forum/speakers/speaker/WangXingxing | Photographer and image owner unstated; published by GTEF | Copyright notice ©2026 GTEF. All rights reserved. |
| `assets/img/05_synthesia.jpg` | photo | https://www.maddyness.com/2026/04/07/elevenlabs-synthesia-luminance-ces-scale-up-britanniques-qui-montent-dans-lia/ | unknown | unknown |
| `assets/img/05_synthesia_alt.jpg` | photo | https://www.flickr.com/photos/websummit/49023219346/ | Cody Glenn / Web Summit via Sportsfile | CC BY 2.0 |
| `assets/logo/synthesia.png` | logo | https://brandfetch.com/synthesia.io | Synthesia Limited | Trademark of Synthesia; identification only (source terms: unknown) |
| `assets/person/synthesia.jpg` | person | https://www.flickr.com/photos/websummit/49022697473/ | Cody Glenn / Web Summit via Sportsfile | CC BY 2.0 |
| `assets/img/06_runway.jpg` | photo | https://runwayml.com/careers/ | Runway; photographer not stated | unknown |
| `assets/img/06_runway_alt.jpg` | photo | https://www.flickr.com/photos/websummit/54916364486/ | Lukas Schulze / Web Summit via Sportsfile | CC BY 4.0 |
| `assets/logo/runway.png` | logo | https://brandfetch.com/runwayml.com | Runway | Trademark of Runway; identification only (source terms: unknown) |
| `assets/person/runway.jpg` | person | https://tisch.nyu.edu/giving/the-tisch-gala/tisch-gala-2026/cristobal-valenzuela | unknown; published by NYU Tisch | unknown |
| `assets/img/07_cohere.jpg` | photo | https://www.michaelmuraz.com/office | Michael Muraz | unknown |
| `assets/img/07_cohere_alt.jpg` | photo | https://www.flickr.com/photos/collisionconf/53011923069/ | Piaras Ó Mídheach / Collision via Sportsfile | CC BY 2.0 |
| `assets/logo/cohere.png` | logo | https://webclaw.io/data/startups/company/cohere.com | Cohere | Trademark of Cohere; identification only (source terms: unknown) |
| `assets/person/cohere.jpg` | person | https://www.flickr.com/photos/collisionconf/53012136770/ | Piaras Ó Mídheach / Collision via Sportsfile | CC BY 2.0 |
| `assets/img/08_zhipu.jpg` | photo | https://www.scmp.com/topics/beijing-zhipu-huazhang-technology | Reuters / Laurie Chen | unknown |
| `assets/img/08_zhipu_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/zhipu.png` | logo | https://github.com/zai-org | Z.ai / Zhipu | Trademark of Zhipu AI (Z.ai); identification only (source terms: unknown) |
| `assets/person/zhipu.jpg` | person | https://finance.sina.com.cn/tech/roll/2023-10-19/doc-imzrrxmf1786184.shtml | Article supplied by Shunwei Capital; photographer uncredited | All Rights Reserved 新浪公司 版权所有 |
| `assets/img/09_stability_ai.jpg` | photo | https://aifa.global/news/aifa-x-google-launch-event-pictures | Artificial Intelligence Founders Association; photographer not stated | Copyright © 2023 Artificial Intelligence Founders Association. All rights reserved. |
| `assets/img/09_stability_ai_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/stability_ai.png` | logo | https://stability.ai/ | Stability AI Ltd | Trademark of Stability AI; identification only (source terms: You may not use any Stability name, logos, or trademarks, or imply any affiliation, endorsement, or sponsorship, without Stability’s prior written permission.) |
| `assets/person/stability_ai.jpg` | person | https://stateofopencon.com/2024/01/19/2024-plenary-emad-mostaque/ | unknown; published by OpenUK | unknown |
| `assets/img/10_heygen.jpg` | photo | https://www.forbes.com/sites/kenrickcai/2023/11/29/ai-video-startup-heygen-launches-near-instant-avatar-generator-adds-56-million-in-funding/ | HeyGen | unknown |
| `assets/img/10_heygen_alt.jpg` | photo | https://www.flickr.com/photos/collisionconf/53800887150/ | Piaras Ó Mídheach / Collision via Sportsfile | CC BY 2.0 |
| `assets/logo/heygen.png` | logo | https://www.heygen.com/brand-kit | HeyGen Inc. | Trademark of HeyGen; identification only (source terms: Follow these Guidelines and the HeyGen Terms of Service.) |
| `assets/person/heygen.jpg` | person | https://www.flickr.com/photos/collisionconf/53800786164/ | Piaras Ó Mídheach / Collision via Sportsfile | CC BY 2.0 |
| `assets/img/11_anthropic.jpg` | photo | https://www.wired.com/story/anthropic-benevolent-artificial-intelligence/ | Amber Hakim | All rights reserved. |
| `assets/img/11_anthropic_alt.jpg` | photo | https://www.flickr.com/photos/techcrunch/53201955583/ | Kimberly White/Getty Images for TechCrunch | CC BY 2.0 |
| `assets/logo/anthropic.png` | logo | https://toolweight.com/vendors/anthropic | Anthropic, PBC | Trademark of Anthropic; identification only (source terms: MIT licence) |
| `assets/person/anthropic.jpg` | person | https://www.flickr.com/photos/techcrunch/53201734641/ | Kimberly White/Getty Images for TechCrunch | CC BY 2.0 |
| `assets/img/12_midjourney.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/midjourney.png` | logo | https://ai.sitebard.com/icons/midjourney | Midjourney, Inc.; vector distributed by Lobe Icons | Trademark of Midjourney; identification only (source terms: MIT License) |
| `assets/person/midjourney.jpg` | person | https://www.forbes.com/sites/robsalkowitz/2022/09/16/ai-is-coming-for-commercial-art-jobs-can-it-be-stopped/ | Courtesy of David Holz | unknown |
| `assets/img/13_luma_ai.jpg` | photo | https://www.flickr.com/photos/techcrunch/54105956021/ | Katelyn Tucker / Slava Blazer Photography (TechCrunch) | CC BY 2.0 |
| `assets/logo/luma_ai.png` | logo | https://brandfetch.com/lumalabs.ai | Luma AI | Trademark of Luma AI; identification only (source terms: unknown) |
| `assets/person/luma_ai.jpg` | person | https://www.flickr.com/photos/techcrunch/54105075692/ | Katelyn Tucker / Slava Blazer Photography (TechCrunch) | CC BY 2.0 |
| `assets/img/14_minimax.jpg` | photo | https://x.com/851277048Li/status/2031335492340560381 | RyanLee (@RyanLeeMiniMax); photographer unspecified | unknown |
| `assets/img/14_minimax_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/minimax.png` | logo | https://www.minimax.cn/brand-vi | MiniMax Brand Team and MiniMax Design Team | Trademark of MiniMax; identification only (source terms: Unless otherwise expressly authorized, permission to use these assets is limited, non-exclusive, and non-transferable.) |
| `assets/person/minimax.jpg` | person | https://www.geekpark.net/news/335533 | 极客公园 (publisher); photographer not credited | unknown |
| `assets/img/15_elevenlabs.jpg` | photo | https://elevenlabs.io/press | ElevenLabs; photographer unspecified | unknown |
| `assets/img/15_elevenlabs_alt.jpg` | photo | https://www.flickr.com/photos/mediedager/54505414133/ | Thor Brødreskift / Nordiske Mediedager | CC BY-SA 2.0 |
| `assets/logo/elevenlabs.png` | logo | https://elevenlabs.io/press | ElevenLabs | Trademark of ElevenLabs; identification only (source terms: unknown) |
| `assets/person/elevenlabs.jpg` | person | https://elevenlabs.io/blog/authors/mati-staniszewski | ElevenLabs; photographer not credited | unknown |
| `assets/img/16_suno.jpg` | photo | https://www.clickorlando.com/business/2026/02/26/ai-song-generator-startups-suno-and-udio-angered-the-music-industry-now-theyre-hoping-to-join-it/ | Robert F. Bukaty / Associated Press | Copyright 2026 The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed without permission. |
| `assets/img/16_suno_alt.jpg` | photo | https://www.flickr.com/photos/techcrunch/54105956026/ | Katelyn Tucker / Slava Blazer Photography (TechCrunch) | CC BY 2.0 |
| `assets/logo/suno.png` | logo | https://brandfetch.com/suno.com?collection=logos&library=default&view=library | Suno, Inc. | Trademark of Suno; identification only (source terms: unknown) |
| `assets/person/suno.jpg` | person | https://www.flickr.com/photos/techcrunch/54105087202/ | Katelyn Tucker / Slava Blazer Photography (TechCrunch) | CC BY 2.0 |
| `assets/img/17_cursor.jpg` | photo | https://colossus.com/article/inside-cursor/ | Andria Lo | All rights reserved. |
| `assets/img/17_cursor_alt.jpg` | photo | https://www.flickr.com/photos/vonguard/55339669243/ | vonguard | CC BY-SA 4.0 |
| `assets/logo/cursor.png` | logo | https://cursor.com/brand | Anysphere, Inc. | Trademark of Cursor (Anysphere); identification only (source terms: unknown) |
| `assets/person/cursor.jpg` | person | https://www.humanx.co/us/speakers/michael-truell | Photographer/owner not credited; published by HumanX | unknown |
| `assets/img/18_figure_ai.jpg` | photo | https://newsroom.bmwgroup.com/americas/successful-test-of-humanoid-robots-at-bmw-group-plant-spartanburg | BMW Group | unknown |
| `assets/img/18_figure_ai_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/figure_ai.png` | logo | https://brandfetch.com/figure.ai | Figure AI, Inc. | Trademark of Figure AI; identification only (source terms: unknown) |
| `assets/person/figure_ai.jpg` | person | https://www.abundance360.com/summit | Photographer/owner not credited; published by Abundance360 | unknown |
| `assets/img/19_perplexity.jpg` | photo | https://www.studiodaub.com/perplexityheadquarters | Studio Daub (publisher); photographer uncredited | unknown |
| `assets/img/19_perplexity_alt.jpg` | photo | https://www.flickr.com/photos/techcrunch/54106186974/ | Kimberly White/Getty Images for TechCrunch | CC BY 2.0 |
| `assets/logo/perplexity.png` | logo | https://brandfetch.com/perplexity.ai | Perplexity AI, Inc. | Trademark of Perplexity; identification only (source terms: unknown) |
| `assets/person/perplexity.jpg` | person | https://www.flickr.com/photos/techcrunch/54105846536/ | Kimberly White/Getty Images for TechCrunch | CC BY 2.0 |
| `assets/img/20_moonshot_ai.jpg` | photo | https://news.ifeng.com/c/8f6Kzl1mGiW | The Paper; photographer unspecified | unknown |
| `assets/img/20_moonshot_ai_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/moonshot_ai.png` | logo | https://asvg.app/icons/moonshot | Moonshot AI | Trademark of Moonshot AI; identification only (source terms: Downloading a logo file does not grant trademark, commercial-use, or endorsement permission.) |
| `assets/person/moonshot_ai.jpg` | person | https://www.forbes.com/sites/johnkang/2024/05/15/a-look-at-some-30-under-30-asia-alumni-who-are-reaching-new-heights/ | Moonshot; credited as Courtesy of Moonshot | unknown |
| `assets/img/21_xai.jpg` | photo | https://www.tomshardware.com/desktops/servers/first-in-depth-look-at-elon-musks-100-000-gpu-ai-cluster-xai-colossus-reveals-its-secrets | ServeTheHome | unknown |
| `assets/img/21_xai_alt.jpg` | photo | https://unsplash.com/photos/close-up-of-a-laptop-screen-with-a-logo-bAZ6xZLi_MM | Salvador Rios | Unsplash License |
| `assets/logo/xai.png` | logo | https://github.com/xai-org | SpaceX Super Intelligence LLC | Trademark of xAI; identification only (source terms: unknown) |
| `assets/person/xai.jpg` | person | https://www.flickr.com/photos/gageskidmore/54816836217/ | Gage Skidmore | CC BY-SA 4.0 |
| `assets/img/22_mistral_ai.jpg` | photo | https://stationf.co/news/mistral-ai | STATION F; photographer not stated | All rights reserved |
| `assets/img/22_mistral_ai_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/mistral_ai.png` | logo | https://github.com/mistralai/mistral-common/blob/main/docs/assets/logo.svg | Mistral AI | Trademark of Mistral AI; identification only (source terms: unknown) |
| `assets/person/mistral_ai.jpg` | person | https://www.genaisummitseeurope.com/bio-arthur-mensch | Photographer/owner not credited; published by GenAI Summit | unknown |
| `assets/img/23_deepseek.jpg` | photo | https://www.semafor.com/article/06/15/2025/us-should-prepare-for-possibility-of-losing-ai-race-to-china-experts-say | Florence Lo / Reuters | unknown |
| `assets/img/23_deepseek_alt.jpg` | photo | https://unsplash.com/photos/iPsKQ4kLLkg | Solen Feyissa | Unsplash License |
| `assets/logo/deepseek.png` | logo | https://github.com/deepseek-ai/DeepSeek-LLM/blob/main/images/logo.svg | DeepSeek | Trademark of DeepSeek; identification only (source terms: unknown) |
| `assets/person/deepseek.jpg` | person | https://time.com/collections/100-most-influential-people-2025/7273745/liang-wenfeng/ | VCG/Getty Images | 图注署名 "VCG/Getty Images"；页面未写许可（unknown，版权属 VCG/Getty） |
| `assets/img/24_sakana_ai.jpg` | photo | https://wired.jp/article/sz-sakana-ai-interview/ | SHINTARO YOSHIMATSU | unknown |
| `assets/img/24_sakana_ai_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/sakana_ai.png` | logo | https://github.com/SakanaAI/TinySwallow-ChatUI/blob/main/index.html | Sakana AI | Trademark of Sakana AI; identification only (source terms: unknown) |
| `assets/person/sakana_ai.jpg` | person | https://sakana.ai/company-info/ | Sakana AI; photographer not credited | unknown |
| `assets/img/25_cognition.jpg` | photo | https://sfstandard.com/2026/03/24/grind-sf-startup-racing-build-ai-software-engineer/ | The San Francisco Standard; individual photographer not separately credited for this image | All Rights Reserved. |
| `assets/img/25_cognition_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/cognition.png` | logo | https://www.logo.dev/search/brands/cognition.ai | Cognition | Trademark of Cognition; identification only (source terms: They are displayed here for informational and educational purposes only.) |
| `assets/person/cognition.jpg` | person | https://techcrunch.com/2026/05/29/cognitions-scott-wu-says-ai-coding-agents-shouldnt-replace-humans/ | Cognition | unknown |
| `assets/img/26_lovable.jpg` | photo | https://lovable.dev/blog/hello-from-lovables-new-london-home | Lovable | unknown |
| `assets/img/26_lovable_alt.jpg` | photo | https://www.flickr.com/photos/websummit/54915195963/ | Sam Barnes/Web Summit via Sportsfile | CC BY 4.0 |
| `assets/logo/lovable.png` | logo | https://brandfetch.com/lovable.dev | Lovable | Trademark of Lovable; identification only (source terms: unknown) |
| `assets/person/lovable.jpg` | person | https://www.flickr.com/photos/websummit/54915230069/ | Sam Barnes/Web Summit via Sportsfile | CC BY 4.0 |
| `assets/img/27_higgsfield.jpg` | photo | https://en.oninvest.com/article/kazakhstani-ai-startup-higgsfield-has-raised-400-million-its-valuation-has-risen-to-5-4-billion | Higgsfield AI, via its company LinkedIn account | unknown |
| `assets/img/27_higgsfield_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/higgsfield.png` | logo | https://asvg.app/icons/higgsfield | Higgsfield, Inc. | Trademark of Higgsfield AI; identification only (source terms: All rights reserved.) |
| `assets/person/higgsfield.jpg` | person | https://www.ai-expo.net/northamerica/speaker/alex-mashrabov/ | TechEx Events Ltd; photographer not stated | © 2026 TechEx Events Ltd – All Rights Reserved. |
| `assets/img/28_black_forest_labs.jpg` | photo | https://bfl.ai/careers | Black Forest Labs | All rights reserved. |
| `assets/img/28_black_forest_labs_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/black_forest_labs.png` | logo | https://bfl.ai/brand | Black Forest Labs | Trademark of Black Forest Labs; identification only (source terms: All rights reserved.) |
| `assets/person/black_forest_labs.jpg` | person | https://slush.org/past-speakers/robin-rombach | unknown; published by Slush | unknown |
| `assets/img/29_ssi.jpg` | photo | https://www.aftenposten.no/kultur/nyhetsanalyse/i/Rjx2lJ/ki-utviklingen-kan-stoppe-opp-dette-mangler-maskinene | Kimberly White / Getty Images for SSI | unknown |
| `assets/img/29_ssi_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/person/ssi.jpg` | person | https://events.stanford.edu/event/ilya_sutskever_openai_entrepreneurial_thought_leader_speaker_series_etl | unknown; published by Stanford University | unknown |
| `assets/img/30_thinking_machines.jpg` | photo | https://www.wired.com/story/mira-murati-humans-in-the-loop-ai-models-thinking-machines/ | David Paul Morris / Getty Images | All rights reserved. |
| `assets/img/30_thinking_machines_alt.jpg` | photo | — | AI-generated illustration (Codex image_gen) | AI-generated |
| `assets/logo/thinking_machines.png` | logo | https://thinkingmachines.ai/ | Thinking Machines Lab | Trademark of Thinking Machines Lab; identification only (source terms: unknown) |
| `assets/person/thinking_machines.jpg` | person | https://www.wired.com/story/openai-new-ceo-who-is-mira-murati/ | Jessica Chou / WIRED | All rights reserved. |

风险标记汇总（默认母版扣下，`_with-risk-images` 版放进去，发布前由用户签字）：

- licence unknown：22
- portrait: licence unknown：20
- news-agency photo (Getty/Reuters/AP): highest takedown risk：6

`*_alt.jpg` 是默认母版用的可商用替代图（follow-up 020 / 032）：CC / Pexels / Unsplash 实拍，或 Claude 多轮搜索无可商用实拍时由 Codex 生成的插图（许可记 AI-generated，无真人、无 logo）。logo 按商标指认使用（bible §4），不改色、不变形；Midjourney 卡主图也是 Codex 生成的插图。含 AI 生成图，上传时勾选合成内容声明。
