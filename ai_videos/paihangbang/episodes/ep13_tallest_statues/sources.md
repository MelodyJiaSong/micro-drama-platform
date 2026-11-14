# ep13 · 数据出处、交叉核对、全景自由与图片许可（sources.md）

> 2026-11-03 代理整理（follow-up 015，用户授权自主决策）。本文件由 `_build/gen_sources.py` 从 `data.json` / `assets.json` 生成；改数据请改 `_build/items_def.py` 后重跑 `build.py` → `gen_sources.py`。调研原料：`_build/raw/`（维基表 wikitext、Commons 各国 FoP 规则页、维基摘要），每项内容摘要 `_build/content/`。

## 1. 口径

- **榜单**：世界上已建成的雕像，按**雕像本体高**降序，收录所有能核实到的本体 ≥ 49 m 的雕像，共 41 尊。
- **本体高**：形象从脚底（或坐像底面）到形象最高点，含手持物（伏尔加格勒「祖国母亲在召唤」的剑、自由女神的火炬同理）；不含莲花座 / 宝座 / 基座 / 内含建筑 / 山体。含基座总高另在卡片标签上写「… m with base」，`data.json` 字段 `total_height_m`。
- **为什么不用「含基座」**：基座高度差别极大（统一像 58 m 基座、春泉大佛 100 m 叠台、炎黄二帝 55 m 山体），比较的是「人造台子」而不是雕像；本体口径与维基表的大部分条目、Guinness 的「最高雕像」一致。维基表本身口径不统一：春泉大佛 128 m 含 20 m 莲花座，拉开坤 115.8 m 不含 13.4 m 莲花座。本期统一不含：春泉大佛 108 m，因此排第 3（含莲花座统一算则 128 vs 129.2，拉开坤仍在前）。
- **只收已建成**：在建 / 规划不收（孟买 Ambedkar 像 2026 年 11 月仍在建；柬埔寨 Bokor 108 m 大佛预计 2027；越南广义观音、泰国纳黎萱王像、Maha Sarakham 坐佛等在建）；已拆不收（荆州关公 2021–22 拆除迁移；巴米扬大佛 2001 年被毁）。
- **不收**：按长度计的卧像（江西弋阳卧佛 416 m 长）、浮雕、塔中佛像（室内）。胸像算雕像（炎黄二帝）。
- **同高同名次**（1,1,3 式），同名次内按 data.json 顺序稳定。
- **国家** = 雕像所在地；香港计入中国（同 ep01）；台湾单列。
- **显示**：`value_display` 取 3 位有效数字（≥ 100 m 取整米；带小数的来源值保留 1 位），`secondary_display` = 米 × 3.28084 取整英尺。
- **来源分级**：每条主值至少一个非维基来源（建设方行业刊物、官方 / 政府旅游机构、新闻、百科出版物，个别只有旅游网站——表中照写）；维基表（rev 1382307847，2026-10-27）只作交叉核对。差异 > 10% 写进备注。

## 1b. Statue of Belief 口径修正（2026-11-04，qc #6）

- 揭幕新闻一律写「369 ft」；维基正文：overall statue 369 ft (112 m)、pedestal 110 ft (34 m)；The Daily Guardian：「34 m high pedestal, reaches a height of 112 m」。369 ft 是含台座的总高。
- 施工方行业刊物 NBM&CW 2020 年的「351 ft」是施工期的总高；后来在发髻上加了恒河水流造型，总高变为 369 ft（Zee News / Rajasthan Tour Planner）。
- 按本期口径（不含台座），本体 = 369 − 110 = 259 ft = 78.9 m（推算值，两处来源的分项相减），排第 12；维基表的 106 m / 112 m 隐含台座只有 6 m，与 110 ft 台座和 110 ft 观景层矛盾，不采用。
- 片头卖点「the usual No. 2 drops to No. 3」不受影响（春泉大佛第 3，因为莲花座不计）。

## 2. 名单边界：剔除与未收

| 对象 | 维基表值 | 处理 | 原因 |
|---|---|---|---|
| Chao Mae Kuan Im（清莱 Wat Huay Pla Kang 观音） | 69 m | 剔除 | 来源 69 / 79 / 90 m 三说，均为旅游网站，无官方数 |
| 太湖西山观音（苏州大如意圣境） | 67 m | 剔除 | 唯一中文来源写 88 m（未分本体 / 基座），67 m 无出处 |
| Lung Por Tuad（呵叻 Wat Khao Yai） | 59 m | 剔除 | 泰文报道多写 111 m，并有文章质疑；59 m 无出处 |
| Phra Kakusunto（素攀） | 58 m | 剔除 | 旅游指南写 26 m；58 m 只见维基 |
| Bodhi Tahtaung 坐佛（蒙育瓦） | 74 m | 剔除 | 维基同时列在「已建成 2022」与「在建」，未找到完工证据 |
| Mother of All Asia（菲律宾八打雁） | 98.15 m | 剔除 | 98.15 m 含其下台座 / 建筑（Montemaria），本体高未公开；完工年也有 2021 / 未完两说 |
| 慈山寺观音（香港） | 76 m | 剔除 | 70 m 像高含三层莲花座（慈山寺博物馆导览），另有 6 m 花岗岩基座；不含莲座的像身高未公开（qc #7） |
| 开元寺阿弥陀佛（越南河内山西） | 72 m | 剔除 | 72 m 为坐佛连多层台座建筑（内部 13–16 层）的总高，本体高未公开；另有 70 m 说法 |
| 越南 Ba Den 山观音（西宁） | 未收 | 未收 | 72 m 为含莲花座与五层台基的总高，本体高未公开 |
| 佛光山佛光大佛（高雄） | 未收 | 未收 | 本体 40 / 48 / 50 m 说法不一，含建筑 108 m |
| 江西弋阳卧佛 | 68 m | 不收 | 卧像，68 m 是卧姿的高度、416 m 是长度 |
| Our Lady of Mercy（波兰 Konotopie） | 40.6 m | 不够高 | 本体 40.6 m |
| 巴西 Santa Rita de Cássia | 未收 | 不够高 | 本体 42 m（含座 56 m，Correio Braziliense / Audiala） |
| Statue of Liberty | 未收 | 不够高 | NPS：基座顶到火炬 46.05 m（151 ft 1 in）——洞察卡 1 |
| 荆州关公 | 58 m（已拆） | 不收 | 2021-09 起拆除迁移（SCMP）——洞察卡 2 |
| 孟买 Ambedkar 像 | 在建 | 不收 | 2025-12 州政府称 2026 年内完工，至今未揭幕；发布前复核 |

**可能的遗漏**：维基表只收 ≥ 50 m，49–55 m 段落（泰国、中国地方寺院、东南亚新建佛像）可能还有未被任何英文列表收录的雕像。本期补了维基漏收的不丹 Buddha Dordenma（54 m），并核过巴西、印度、墨西哥、日本常见的 40–50 m 级大像（均 < 49 m）。

## 3. 全景自由（FoP）：所在国是否允许商用复制雕塑的照片

依据：Wikimedia Commons「Copyright rules by territory / 国家」FoP 一节（2026-11-03 取，原文存 `_build/raw/fop/`）及其引用的法条。雕像大多是近几十年的作品，雕塑作者仍享有版权；照片的许可（Pexels / CC 等）只解决摄影师的版权，不解决雕塑本身的版权。

| 国家 | 本期件数 | 雕塑商用 FoP | 法律依据 | 处理 |
|---|---|---|---|---|
| 中国 | 12 | ✅ | 著作权法（2020）第 24 条第 1 款第 10 项：对设置或陈列在公共场所的艺术作品进行临摹、绘画、摄影、录像；香港《版权条例》第 71 条 | 照常 |
| 印度 | 2 | ✅ | Copyright Act 1957 s.52(1)(t)：公共场所永久陈列的雕塑可绘画、摄影并发表 | 照常 |
| 泰国 | 5 | ✅ | Copyright Act B.E. 2537 s.39：公共场所永久陈列的艺术品可绘画、摄影、摄像 | 照常 |
| 墨西哥 | 1 | ✅ | Ley Federal del Derecho de Autor Art. 148(VII)：公共场所可见的作品可摄影、视听复制（须注明出处） | 照常 |
| 日本 | 9 | ⚠️ | 著作权法第 46 条：室外永久设置的美术作品可利用，但第 4 项排除「以出售复制品为目的」的复制；Commons 视为 NoFoP | `image_risk` |
| 台湾 | 2 | ⚠️ | 著作权法第 58 条第 4 款，同日本 | `image_risk` |
| 菲律宾 | 1 | ❌ | IP Code（RA 8293）无 FoP 条款；IPOPHL 2021 表示商用需授权 | `image_risk` |
| 缅甸 | 2 | ❌ | Copyright Law 2019 第 24–33 条无 FoP | `image_risk` |
| 印度尼西亚 | 2 | ❌ | 著作权法 2014 无商用 FoP（CC Indonesia 2018 声明） | `image_risk` |
| 越南 | 1 | ❌ | 知识产权法 2022 修正（2023-01-01 起）：公共场所艺术作品只可非商业摄影 | `image_risk` |
| 俄罗斯 | 1 | ❌ | 民法典第 1276 条：雕塑为主要对象或用于营利时不适用（Vuchetich 1974 年去世，版权至 2044） | `image_risk` |
| 乌克兰 | 1 | ❌ | 著作权法 2022 第 22 条第 10 项：只限「无独立经济价值」的使用 | `image_risk` |
| 不丹 | 1 | ❌ | Copyright Act 2001 无 FoP | `image_risk` |
| 塞内加尔 | 1 | ❌ | 著作权法 2008 第 46 条：作为主要对象并用于商业时不适用 | `image_risk` |
| （古代作品）乐山大佛 | 1 | ✅ | 713–803 年作品，公有领域 | 照常 |

**默认版的处理（follow-up 016）**：用户要求默认母版每张卡都有图。FoP 风险项默认版用一张可商用许可的照片（`image_alt`），风险版（`_with-risk-images`）用最好的那张（可能许可不明）。注意：`image_alt` 仍然是该雕像的照片，**FoP 风险在默认版并未消除**，只是摄影许可干净；是否发布、是否改用远景 / 占位，需用户在发布前决定。

**2026-11-04 主代理决定（qc 必须修）**：雕塑 FoP 安全的国家（中国、泰国、墨西哥）里找不到可商用实拍的项，默认版改用 Codex 生成的写实图（`tools/codex_image.py`，无人物 / 文字 / 横幅，渲染器自动标 AI IMAGE）；其中炎黄二帝、赤山明神两项的风险版原图（真人合影带横幅 / 来源页保留权利）也一并换成生成图。日本、台湾、缅甸、印尼、菲律宾等国许可不明的项默认版维持占位，原因写「licence unclear」；风险版里来源页明写 All rights reserved 的图（东京湾观音、The Victor 原图）已换成许可不明的其他图。

## 4. 逐条出处与交叉核对

差异 = |本期值 − 维基表值| / 本期值。所有条目 retrieved_at = 2026-11-03。FoP 列：ok / risk / pd。

| # | 雕像 | 国家 | 本体 m | 含基座 m | 主值来源 | 维基表 | 差异 % | FoP | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Statue of Unity | India | 182 | 240 | [BBC News, 31 Oct 2018: India unveils world's tallest statue](https://www.bbc.com/news/world-asia-india-46028342) | 182 | 0.0 | ok | Vallabhbhai Patel. 182 m figure on a 58 m base (240 m total). Sculptor Ram V. Sutar. |
| 2 | Laykyun Sekkya | Myanmar | 115.8 | 129.2 | [OrangeSmile: Laykyun Setkyar (116 m on a 13.5 m throne)](https://www.orangesmile.com/extreme/en/largest-monuments/laykyun-setkyar.htm) | 115.8 | 0.0 | risk | Standing Buddha on a 13.41 m lotus throne (129.2 m total). Some sources round to 116 m. |
| 3 | Spring Temple Buddha | China | 108 | 208 | [Zhengzhou Evening News 2013-05-28 B06 (佛身108米, 莲花座20米, 总高208米)](https://zzwb.zynews.cn/page/2/2013-05/28/B06/20130528B06_pdf.PDF) | 128 | 18.5 | ok | Figure 108 m + 20 m copper lotus throne = 128 m (the figure usually quoted, incl. by WPL) + 25 m + 55 m pedestals = 208 m. Our rule excludes thrones, so 108 m. With thrones counted for both it would still rank No. 3 (128 m < 129.2 m Laykyun incl. its 13.4 m throne); only WPL's mixed rule puts it at No. 2. |
| 4 | Ushiku Daibutsu | Japan | 100 | 120 | [Guide to Japan (GLTJP) official info: 120 m incl. 20 m base](https://www.gltjp.com/ja/directory/item/12644/) | 100 | 0.0 | risk | Bronze Amitabha. 100 m figure on 10 m lotus + 10 m base. Guinness: tallest bronze Buddha statue. |
| 5 | Guishan Guanyin | China | 99 | — | [Ctrip attraction page: 千手千眼观音 99.19 m](https://gs.ctrip.com/html5/you/sight/148/52777.html) | 99 | 0.0 | ok | Gilded bronze thousand-armed Guanyin behind Miyin Temple; 99 m (some pages 99.19 m). |
| 6 | Great Buddha of Thailand | Thailand | 92 | — | [Atlas Obscura: Thailand's Biggest Buddha (92 m)](https://www.atlasobscura.com/places/thailands-biggest-buddha) | 93 | 1.1 | ok | Seated concrete Buddha painted gold, 92 m high, 63 m wide. WPL table says 93 m, WP article 92 m, some tourism pages 95 m. |
| 6 | Sendai Daikannon | Japan | 92 | 100 | [Tabi-mag: 仙台大観音 像の身の丈92m, 台座を含め100m](https://tabi-mag.jp/mg0188/) | 92 | 0.0 | risk | White Kannon; 100 m total commemorates Sendai's centenary. Ties with Thailand's Great Buddha at 92 m. |
| 8 | Hokkaido Kannon | Japan | 88 | — | [Onitoge rail travel: 芦別 北海道大観音 高さ88m](https://www.onitoge.org/tetsu/nemuro/05ashibetsu.htm) | 88 | 0.0 | risk | Byakue (white-robed) Kannon at Kita no Miyako park; world's tallest statue 1989–1991. |
| 9 | The Motherland Calls | Russia | 85 | — | [Stalingrad Battle Museum-Reserve (QR guide): 85 m with sword, 52 m without](https://stalingrad-battle.ru/qr/mamaev-kurgan-skulptura-rodina-mat-zovet.php) | 85 | 0.0 | risk | Reinforced concrete, sculptor Yevgeny Vuchetich (d. 1974, so still in copyright). 85 m to the sword tip; the sword is held by the figure, so it counts (same rule as the Statue of Liberty's torch). |
| 10 | Ksitigarbha of Jiuhua | China | 84 | 99 | [Sina News, 31 Aug 2013: 九华山地藏菩萨圣像开光 (像身84米, 加莲花座99米)](https://news.sina.cn/sa/2013-08-31/detail-ikmxzfmk2416114.d.html) | 76 | 9.5 | ok | Bronze Dizang (Ksitigarbha) at Dayuan Cultural Park; consecrated 31 Aug 2013. Body 84 m, 99 m with lotus base (139 m 'viewing height' incl. platform). WPL gives 76 m [citation needed] and completion 2012 — differs >10%; we use the 2013 news figure. |
| 11 | Grand Buddha at Lingshan | China | 79 | 88 | [Maigoo: 灵山大佛 通高88米 (含莲花座)](https://m.maigoo.com/citiao/218459.html) | 79 | 0.0 | ok | Bronze Amitabha; 79 m figure + 9 m lotus = 88 m. |
| 12 | Statue of Belief | India | 78.9 | 112.5 | [The Daily Guardian: 112 m (369 ft) overall incl. a 34 m (110 ft) pedestal; Wikipedia 'Statue of Belief' same split](https://www.magzter.com/nl/stories/newspaper/The-Daily-Guardian/STANDING-TALL-IN-FAITH-THE-STATUE-OF-BELIEF-IN-NATHDWARA) | 106 | 34.3 | ok | Shiva ('Vishwas Swaroopam'), unveiled 29 Oct 2022. Overall 369 ft (112.5 m) incl. a 110 ft (33.5 m) pedestal (Wikipedia article; Daily Guardian: '34 m high pedestal, reaches 112 m'), so the seated figure is 369 - 110 = 259 ft = 78.9 m (derived). The 351 ft (107 m) in the NBM&CW builder report was the overall height during construction, before the Ganga stream was added to the hair (Rajasthan Tour Planner / Zee News). WPL lists 106 m statue / 112 m total, which treats the pedestal as only 6 m; contradicted by the 110 ft pedestal and the 110 ft viewing gallery. Explore Our India gives base 110 ft / shoulders 260 ft / trident tip 351 ft; the topmost point of the figure is the 369 ft hair ornament, so the figure height stays 259 ft. Previously ranked No. 4 in our draft. |
| 13 | Guanyin of Nanshan | China | 78 | 108 | [Sina News, 25 Apr 2005: 南山海上观音 高108米 开光](https://news.sina.cn/sa/2005-04-25/detail-ikkntiam3335350.d.html) | 78 | 0.0 | ok | Three-faced white Guanyin on an artificial island. 108 m includes the 108-petal lotus seat and the Vajra platform that houses a hall; the figure-only 78 m is from WPL (no independent breakdown found) — flagged for review. |
| 14 | Kyaikhto Seated Buddha | Myanmar | 77.9 | — | [Myanmar Digital News (MDN): largest sitting Buddha in Myanmar, Phayathonzu](https://www.mdn.gov.mm/my/node/181825) | 77.9 | 0.0 | risk | Seated Buddha, 255.5 ft (77.9 m); opened 6–7 Apr 2019. Height from WPL; MDN confirms it as Myanmar's largest sitting Buddha. |
| 15 | Garuda Wisnu Kencana | Indonesia | 75 | 121 | [The Jakarta Post, 24 Sep 2018: Jokowi unveils Indonesia's tallest statue](https://www.thejakartapost.com/news/2018/09/24/jokowi-unveils-indonesia-s-tallest-statue.html) | 76 | 1.3 | risk | Vishnu riding Garuda by Nyoman Nuarta; 75 m statue, 65 m wingspan, on a 46 m pedestal (121 m total). |
| 15 | Phra Buddha Chok | Thailand | 75 | — | [Bangkok Biznews (2022): พระพุทธโชค สูง 75 เมตร หน้าตัก 45 เมตร](https://www.bangkokbiznews.com/news/985987) | 75 | 0.0 | ok | Seated Buddha on Khao Wong Phrachan; 75 m high, 45 m lap width; built from 2010 over about 8 years. Sanook gives 78 m. |
| 17 | Kaga Kannon | Japan | 73 | — | [Trafficnews, Apr 2026: 加賀大観音 73m, aviation-light order](https://trafficnews.jp/post/655378) | 73 | 0.0 | risk | Former 'Utopia Kaga no Sato' resort. Apr 2026: aviation authority ordered the owner to fix obstruction lights out since 2022; owner weighing demolition or preservation. |
| 18 | Confucius of Mount Ni | China | 72 | — | [Huanqiu, 2016: 尼山72米铜质孔子像落成](https://m.huanqiu.com/article/9CaKrnK2g6K) | 72 | 0.0 | ok | Bronze Confucius at Nishan Shengjing; 72 m for his 72 leading disciples; built from May 2012, unveiled 2016. |
| 19 | Leshan Giant Buddha | China | 71 | — | [Encyclopaedia Britannica: Leshan Giant Buddha, 71 m (233 ft)](https://www.britannica.com/print/article/883314) | 71 | 0.0 | pd | Seated Maitreya carved into a cliff, 713–803 AD; UNESCO World Heritage (1996, with Mount Emei). Ancient work: public domain. |
| 20 | Wat Paknam Great Buddha | Thailand | 69 | — | [Khaosod English, 17 Aug 2026: the giant Buddha at Wat Paknam (69 m)](https://www.khaosodenglish.com/featured/2026/08/17/discover-the-giant-buddha-at-bangkoks-wat-paknam/) | 69 | 0.0 | ok | Phra Buddha Dhammakaya Thepmongkhon, 69 m (20 storeys), 40 m lap; finished Jun 2021 (Sino Sculpture), royal inauguration 5 Feb 2023. |
| 21 | Lady Buddha of Son Tra | Vietnam | 67 | — | [Vietnam Tourism: Linh Ung Pagoda and the Lady Buddha (67 m)](https://www.vietnamtourism.com/en/linh-ung-pagoda-and-the-lady-buddha-da-nang-history) | 67 | 0.0 | risk | White Quan Am facing the sea on Son Tra peninsula; opened 2010. |
| 22 | Yang'asha Statue | China | 66 | 88 | [People's Daily app / The Paper, Oct 2020: 剑河88米仰阿莎雕塑 (像高66米, 底座22米)](https://www.peopleapp.com/rmharticle/30018156007) | 66 | 0.0 | ok | Stainless-steel Miao goddess of beauty; 66 m figure on a 22 m base. Built Nov 2016–Jul 2017; criticised in 2020 amid China's curbs on giant statues. |
| 23 | Mother Ukraine | Ukraine | 62 | 102 | [Structurae: Mother Ukraine (62 m statue, 102 m with museum base)](https://structurae.net/en/structures/mother-ukraine) | 62 | 0.0 | risk | Stainless steel, opened 9 May 1981 (Vuchetich design, completed by Vasyl Borodai). 62 m incl. sword, on a 40 m museum base. In Aug 2023 the Soviet emblem on the shield was replaced by Ukraine's trident and the statue renamed Mother Ukraine. |
| 23 | Kurume Jibo Kannon | Japan | 62 | — | [Crossroad Fukuoka (official Fukuoka tourism): 高さ62m 慈母大観音](https://www.crossroadfukuoka.jp/spot/12724) | 62 | 0.0 | risk | Reinforced-concrete Kannon holding a child; spiral stairs inside. |
| 25 | Guanyin of Mount Xiqiao | China | 61.9 | — | [Foshan Bendibao: 西樵山观音像 61.9米](https://m.bendibao.com/show633361.html) | 62 | 0.2 | ok | Seated Guanyin, 61.9 m (for Guanyin's day 6/19); on a hall-filled lotus base (WPL: 77 m total). Opened 1998. |
| 26 | Jesus of Sibea-bea | Indonesia | 61 | — | [The Star, 22 Sep 2024: North Sumatra unveils world's tallest Christ statue](https://www.thestar.com.my/aseanplus/aseanplus-news/2024/09/22/north-sumatra-unveils-world039s-tallest-christ-statue) | 61 | 0.0 | risk | Christ the Saviour above Lake Toba, 61 m; unveiled 19–21 Sep 2024 (dates differ by source). WPL total 69 m with an 8 m pedestal ('maybe'). |
| 26 | Guan Yu of Yuncheng | China | 61 | 80 | [CGTN: Guan Yu statue stands 61 m atop a 19 m pedestal](https://news.cgtn.com/news/7841444f32457a6333566d54/index.html) | 61 | 0.0 | ok | Bronze Guan Yu in his home village; 61 m for the 61 years of his life, 19 m pedestal. |
| 28 | Mukdahan Great Buddha | Thailand | 59.99 | — | [Trip.com Mukdahan guide: seated Buddha 59.99 m, lap 39.99 m](https://nz.trip.com/moments/poi-great-buddha-146450991) | 59.9 | 0.2 | ok | Seated Buddha at Wat Roi Phra Phutthabat Phu Manorom; about 84 m with base. |
| 29 | Luang Pho Yai | Thailand | 59.2 | 67.85 | [Thai Holiday Guide: Wat Burapha Phiram, 59.2 m (67.85 m with base)](https://www.thaiholidayguide.com/attraction/wat-burapha-phiram/) | 59.2 | 0.0 | ok | Standing concrete Buddha. Completion year differs (1973 / 1979). |
| 30 | God of Red Mountain | China | 58.8 | — | [Wing On Travel: 赤山明神 58.8 m bronze sea god](https://www.wingontravel.com/discovery/scenic-shidaowan-international-bathing-beach%2C-weihai-51898593) | 58.8 | 0.0 | ok | Forged-copper Chishan Mingshen (local sea god) at Chishan scenic area. Only travel-site sources found; flagged. |
| 31 | Aizu Jibo Kannon | Japan | 57 | — | [Japan Travel (JAL): Aizu Jibo Dai Kannon, 57 m](https://en.jal.japantravel.com/fukushima/aizu-jibo-kannon/4066) | 57 | 0.0 | risk | White Kannon holding a baby at Aizumura park. |
| 32 | Emei Maitreya Buddha | Taiwan | 56.7 | 72 | [Up To Go: 銅像高度56.7公尺, 基座15.3公尺, 總高72公尺](https://uptogo.com.tw/藝術/台灣最大的彌勒佛？/) | 56.7 | 0.0 | risk | Bronze standing Maitreya at Tian En Maitreya Buddhist Temple (Great Nature Culture World); not normally open to visitors. |
| 33 | Tokyo Bay Kannon | Japan | 56 | — | [Tabi-mag: 東京湾観音 高さ56m, 昭和36年完成](https://tabi-mag.jp/ch0046/) | 56 | 0.0 | risk | War-dead memorial on Mt Otsubo overlooking the Uraga Channel. |
| 34 | The Victor | Philippines | 55 | 60 | [Inquirer Business, Aug 2023: 55 m statue + 5 m podium](https://business.inquirer.net/?p=415122) | 55 | 0.0 | risk | Stainless-steel figure by Jefre Manuel-Figueras, unveiled Aug 2023. |
| 35 | Buddha Dordenma | Bhutan | 54 | — | [Thimphu Dzongkhag Administration: Buddha Dordenma, 54 m (177 ft)](https://thimphu.gov.bt/buddha-dordenma/) | 51.5 | 4.6 | risk | Gilded bronze seated Buddha, completed Sep 2015. Not in WPL; some sources give 51.5 m (figure without throne?). Uses the official 54 m. |
| 36 | Koxinga Statue | Taiwan | 52.4 | — | [Focus Taiwan (CNA), 25 Feb 2026: original Koxinga statue in Xikou is 172 ft](https://focustaiwan.tw/culture/202602250019) | 54 | 3.1 | risk | Seated Zheng Chenggong at Xikou Kaiyuan Temple; CNA gives 172 ft (52.4 m); WPL 54 m. |
| 37 | Emperors Yan and Huang | China | 51 | 106 | [Sina News, 18 Apr 2007: 炎黄二帝塑像落成 (高106米)](https://news.sina.cn/sa/2007-04-18/detail-ikftssap2866402.d.html) | 51 | 0.0 | ok | Twin busts carved onto a hill above the Yellow River: busts 51 m on a 55 m hill (106 m). |
| 38 | Usami Daikannon | Japan | 50 | — | [All About Japan: Japan's largest sitting Kannon (Usami)](https://allabout-japan.com/en/article/9518) | 50 | 0.0 | risk | Seated Kannon overlooking Ito; opens only on limited days. |
| 38 | Shodoshima Daikannon | Japan | 50 | — | [japan-guide.com: Great Kannon (Daikannon), 50 m, completed 1993/94](https://www.japan-guide.com/e/e5437.html) | 50 | 0.0 | risk | Standing Kannon with a temple inside; asoview gives ~60 m (likely incl. base). |
| 38 | Guerrero Chimalli | Mexico | 50 | 60 | [Excélsior, 13 Dec 2014: Inauguran escultura Guerrero Chimalli de Sebastián](https://www.excelsior.com.mx/comunidad/2014/12/13/997572) | 50 | 0.0 | ok | Red Aztec warrior by Sebastián; 60 m overall (WPL: 50 m statue on its base). Most Spanish sources quote 60 m overall. |
| 41 | African Renaissance | Senegal | 49 | — | [NBC News / AP, Apr 2010: Senegal unveils 'African Renaissance' statue](https://www.nbcnews.com/id/wbna36158049) | 50 | 2.0 | risk | Bronze family group on a 100 m hill; usually quoted 49 m (some infoboxes 52 m, WPL 50 m). |

## 5. 洞察卡依据

| after | 文字 | 依据 |
|---|---|---|
| 37 | The Statue of Liberty is 46 m from base to torch: too short to make this list. | NPS Statue Statistics：Top of base to torch 151'1" = 46.05 m（https://home.nps.gov/stli/learn/historyculture/statue-statistics.htm）；本榜第 41 名 49 m |
| 28 | China now curbs statues over 30 m. Jingzhou took down its 58 m Guan Yu in 2021-22. | 人民日报客户端 2020-10（剑河仰阿莎争议报道引住建部通知：严格控制高度超过 30 m 或宽度超过 45 m 的大型雕塑）；SCMP 2021：荆州 57.3 / 58 m 关公像违反古城限高，耗资 1.55 亿元迁移，2021-09 起拆除（https://scmp.com/news/china/article/3116103/）；拆除完成于 2022 上半年（多源） |
| 20 | Japan has 9 statues on this list, but the newest of them went up back in 1994. | data.json：日本 9 项建成年 1961–1994，最新为小豆岛大观音 1994 |
| 11 | 4 statues here were unveiled since 2022: in India, Thailand, the Philippines, Indonesia. | Statue of Belief 2022-10-29（ThePrint；本体 78.9 m 由总高 369 ft − 台座 110 ft 推得）；Wat Paknam 大佛 2023-02-05 御临开光（Sino Sculpture / Khaosod）；The Victor 2023-08（Inquirer）；Sibea-bea 耶稣像 2024-09（The Star） |
| 4 | Spring Temple Buddha is often listed at 128 m. That includes its 20 m lotus throne. | 郑州晚报 2013-05-28：佛身 108 m + 莲花座 20 m；维基与多数榜单写 128 m |
| 2 | Next: the Statue of Unity, 66 m taller than any other statue on Earth. | 182 − 115.8 = 66.2 m（BBC；拉开坤见第 2 名出处） |

## 6. 竞品

| 视频 | 频道 | 播放 | 时间 | 口径 |
|---|---|---|---|---|
| ◄ Tallest statue size comparison ► 3d animation | Real Data | 约 5,828 万 | 约 2021（Artribune 2022-01 报道） | 3D 体量对比，数值取维基、本体 / 含基座混用（如自由女神 93 m 含基座） |
| World Tallest Statues size Comparison \| Upcoming Tallest Statues | WorldTV Studio | 约 1,790 万 | 未取到 | 3D 体量对比，含在建 |

需求数据：`ai_videos/paihangbang/0_research/data/yt_demand_2026-11-03.jsonl`（「tallest statues in the world」前 15 条中位数 1,449,466，最高 58,284,039）。

## 7. 图片许可（assets.json 摘要）

| # | 雕像 | 默认版用图 | 许可 | 风险版用图 | 许可 | 说明 |
|---|---|---|---|---|---|---|
| 1 | Statue of Unity | `assets/img/01_statue_of_unity.jpg` | Unsplash License | `同左` |  |  |
| 2 | Laykyun Sekkya | `assets/img/02_laykyun_sekkya.jpg` | CC BY 2.0 | `assets/img/02_laykyun_sekkya.jpg` | CC BY 2.0 | FoP: Myanmar Copyright Law 2019 has no freedom of panorama |
| 3 | Spring Temple Buddha | `assets/img/03_spring_temple_buddha.jpg` | CC0 1.0 | `同左` |  |  |
| 4 | Ushiku Daibutsu | `assets/img/05_ushiku_daibutsu.jpg` | Pexels License | `assets/img/05_ushiku_daibutsu.jpg` | Pexels License | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale |
| 5 | Guishan Guanyin | `assets/img/06_guishan_guanyin.jpg` | Pexels License | `同左` |  |  |
| 6 | Great Buddha of Thailand | `assets/img/08_great_buddha_of_thailand.jpg` | Pexels License | `同左` |  |  |
| 6 | Sendai Daikannon | `assets/img/09_sendai_daikannon.jpg` | Unsplash License | `assets/img/09_sendai_daikannon.jpg` | Unsplash License | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale |
| 8 | Hokkaido Kannon | `assets/img/10_hokkaido_kannon.jpg` | CC BY 2.0 | `assets/img/10_hokkaido_kannon.jpg` | CC BY 2.0 | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale |
| 9 | The Motherland Calls | `assets/img/11_the_motherland_calls.jpg` | Unsplash License | `assets/img/11_the_motherland_calls.jpg` | Unsplash License | FoP: Russia Civil Code Art. 1276 excludes sculpture used as main subject / for profit |
| 10 | Ksitigarbha of Jiuhua | `assets/img/12_ksitigarbha_of_jiuhua_alt.jpg` | AI-generated (Codex image_gen) | `assets/img/12_ksitigarbha_of_jiuhua.jpg` | unknown | licence unknown |
| 11 | Grand Buddha at Lingshan | `assets/img/13_grand_buddha_at_lingshan.jpg` | CC BY 2.0 | `同左` |  |  |
| 12 | Statue of Belief | `assets/img/04_statue_of_belief.jpg` | CC0 | `同左` |  |  |
| 13 | Guanyin of Nanshan | `assets/img/14_guanyin_of_nanshan.jpg` | CC0 1.0 | `同左` |  |  |
| 14 | Kyaikhto Seated Buddha | `（占位）` |  | `assets/img/15_kyaikhto_seated_buddha.jpg` | unknown | FoP: Myanmar Copyright Law 2019 has no freedom of panorama; licence unknown |
| 15 | Garuda Wisnu Kencana | `assets/img/16_garuda_wisnu_kencana.jpg` | Unsplash License | `assets/img/16_garuda_wisnu_kencana.jpg` | Unsplash License | FoP: Indonesia Copyright Law 2014 has no commercial freedom of panorama |
| 15 | Phra Buddha Chok | `assets/img/17_phra_buddha_chok_alt.jpg` | AI-generated (Codex image_gen) | `assets/img/17_phra_buddha_chok.jpg` | unknown | licence unknown |
| 17 | Kaga Kannon | `（占位）` |  | `assets/img/18_kaga_kannon.jpg` | unknown | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale; licence unknown |
| 18 | Confucius of Mount Ni | `assets/img/20_confucius_of_mount_ni_alt.jpg` | AI-generated (Codex image_gen) | `assets/img/20_confucius_of_mount_ni.jpg` | unknown | licence unknown |
| 19 | Leshan Giant Buddha | `assets/img/21_leshan_giant_buddha_alt.jpg` | CC BY 2.0 | `assets/img/21_leshan_giant_buddha.jpg` | unknown | licence unknown |
| 20 | Wat Paknam Great Buddha | `assets/img/23_wat_paknam_great_buddha.jpg` | Unsplash License | `同左` |  |  |
| 21 | Lady Buddha of Son Tra | `assets/img/24_lady_buddha_of_son_tra.jpg` | Pexels License | `assets/img/24_lady_buddha_of_son_tra.jpg` | Pexels License | FoP: Vietnam IP Law (2022 amendment) allows only non-commercial use |
| 22 | Yang'asha Statue | `assets/img/25_yangasha_statue_alt.jpg` | AI-generated (Codex image_gen) | `assets/img/25_yangasha_statue.jpg` | unknown | licence unknown |
| 23 | Mother Ukraine | `assets/img/26_mother_ukraine.jpg` | Pexels License | `assets/img/26_mother_ukraine.jpg` | Pexels License | FoP: Ukraine Copyright Law 2022 Art. 22(10) only without independent economic value |
| 23 | Kurume Jibo Kannon | `（占位）` |  | `assets/img/27_kurume_jibo_kannon.jpg` | unknown | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale; licence unknown |
| 25 | Guanyin of Mount Xiqiao | `assets/img/28_guanyin_of_mount_xiqiao.jpg` | Pexels License | `同左` |  |  |
| 26 | Jesus of Sibea-bea | `（占位）` |  | `assets/img/29_jesus_of_sibea_bea.jpg` | unknown | FoP: Indonesia Copyright Law 2014 has no commercial freedom of panorama; licence unknown |
| 26 | Guan Yu of Yuncheng | `assets/img/30_guan_yu_of_yuncheng_alt.jpg` | AI-generated (Codex image_gen) | `assets/img/30_guan_yu_of_yuncheng.jpg` | unknown | licence unknown |
| 28 | Mukdahan Great Buddha | `assets/img/31_mukdahan_great_buddha_alt.jpg` | AI-generated (Codex image_gen) | `assets/img/31_mukdahan_great_buddha.jpg` | unknown | licence unknown |
| 29 | Luang Pho Yai | `assets/img/32_luang_pho_yai.jpg` | Public domain (PublicDomainPictures.net, 'Free public domain image') | `同左` |  |  |
| 30 | God of Red Mountain | `assets/img/33_god_of_red_mountain.jpg` | AI-generated (Codex image_gen) | `同左` |  |  |
| 31 | Aizu Jibo Kannon | `（占位）` |  | `assets/img/34_aizu_jibo_kannon.jpg` | unknown | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale; licence unknown |
| 32 | Emei Maitreya Buddha | `assets/img/35_emei_maitreya_buddha.jpg` | CC BY 2.0 | `assets/img/35_emei_maitreya_buddha.jpg` | CC BY 2.0 | FoP: Taiwan Copyright Act Art. 58(4) same as Japan |
| 33 | Tokyo Bay Kannon | `（占位）` |  | `assets/img/36_tokyo_bay_kannon.jpg` | unknown | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale; licence unknown |
| 34 | The Victor | `（占位）` |  | `assets/img/37_the_victor.jpg` | unknown | FoP: Philippines IP Code has no freedom of panorama; licence unknown |
| 35 | Buddha Dordenma | `assets/img/38_buddha_dordenma.jpg` | Unsplash License | `assets/img/38_buddha_dordenma.jpg` | Unsplash License | FoP: Bhutan Copyright Act 2001 has no freedom of panorama |
| 36 | Koxinga Statue | `（占位）` |  | `assets/img/39_koxinga_statue.jpg` | unknown | FoP: Taiwan Copyright Act Art. 58(4) same as Japan; licence unknown |
| 37 | Emperors Yan and Huang | `assets/img/40_emperors_yan_and_huang.jpg` | AI-generated (Codex image_gen) | `同左` |  |  |
| 38 | Usami Daikannon | `（占位）` |  | `assets/img/41_usami_daikannon.jpg` | unknown | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale; licence unknown |
| 38 | Shodoshima Daikannon | `assets/img/42_shodoshima_daikannon_alt.jpg` | CC BY 2.0 | `assets/img/42_shodoshima_daikannon.jpg` | unknown | FoP: Japan Copyright Act Art. 46(iv) excludes artistic works reproduced for sale; licence unknown |
| 38 | Guerrero Chimalli | `assets/img/43_guerrero_chimalli_alt.jpg` | AI-generated (Codex image_gen) | `assets/img/43_guerrero_chimalli.jpg` | unknown | licence unknown |
| 41 | African Renaissance | `assets/img/44_african_renaissance.jpg` | Unsplash License | `assets/img/44_african_renaissance.jpg` | Unsplash License | FoP: Senegal Copyright Law 2008 Art. 46 excludes commercial use as main subject |
