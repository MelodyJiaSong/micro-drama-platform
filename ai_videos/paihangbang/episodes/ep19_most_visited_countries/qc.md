# ep19 · 第 1 轮独立审片 · 2026-11-04

> 审片人：独立上下文（没有参与制作），按 `bible.md` §7 与 QC brief 逐项审。只写本文件和 `_build/qc/`，没有改数据、图片和渲染。
> 审的对象：`render/ep19_most_visited_countries_master.mp4`（sha256 b518b918…，与 manifest 一致；52 个输入文件的哈希与当前 data.json / assets.json / assets/img 全部一致，说明渲染对应当前数据）。本期没有 `image_risk` 条目，也就没有 `_with-risk-images` 版。没有配乐版。

## 结论：小修后发布

数据主体可靠：冠军和前 5 名、英国，以及制作方标为「未核到」的 15 项里抽到的 11 项，都由我联网核过，主值都对得上（见数据样本表）。名次连续、排序与 value 一致；▲▼% 和 5 张洞察卡的结论都已逐条重算，全部成立。50 张图都在账本里，许可都是 Unsplash / Pexels，主体都认对了，没有水印，也没有 AI 图。成片 1920×1080、60 fps，共 22,526 帧（375.433 s），与 manifest 时间线一致，没有截断，抽帧中没有文字出框，国旗都对。

需要修的有 2 条 major，没有 blocker：
1. **哈萨克斯坦卡片口径标签写错**（屏上事实错误，要改数据并重渲）。
2. **母版是静音的**，配乐版还没做，不能直接上传（§5、§7-6）。

其余为 minor。

## 问题清单

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| 1 | **major** | #33 Kazakhstan（约 1:50–2:00） | 卡上标签写「Incl. same-day visits」，scope / topic.md 也把哈萨克斯坦归为 VF（含当日往返）。但 UN Tourism 批量表里哈萨克斯坦 2024 的 VSTR 10,381.566 带 flag D，注明 "Value represents overnight visitors (tourists) only"。哈萨克斯坦旅游部的 2024 公布也是：15.3M 外国访客中，**10.4M 停留超过一天**（[Caspian Post](https://caspianpost.com/kazakhstan/kazakhstan-welcomes-15-3-million-foreign-visitors-in-2024)）。所以 10.4M 正是过夜游客。另外，D2 的基数 2019 = 8.515M 是 UN 的 VSTR（2019 年外国人入境总数约 8.5M，[Forbes.kz](https://forbes.kz/life/travels/v_2023_godu_kazahstan_posetilo_svyishe_9_millionov_inostrantsev/)），拿 2024 过夜数和它比不是同口径，「▲22% vs 2019」不成立。 | 删掉「Incl. same-day visits」标签（如需要，可换成 "Stays of 1+ night"）。D2 改为与同序列 2023 比（UN DB 9,871 → ▲5% vs 2023），或者不显示变化。同步改 topic.md / sources.md 的 VF 名单（只剩越南、罗马尼亚，乌兹别克斯坦见 #6）。然后重渲。 |
| 2 | **major** | 全片 | 音轨是 anullsrc 静音（volumedetect：mean / max 都是 −91 dB）。bible §5 要求每期一首配乐，§7-6 要求查爆音和片尾淡出。 | 配乐版做出来以后补审：用 ebur128 查响度、片尾 15–20 s 淡出，抽 3 段试听。在这之前不上传。 |
| 3 | minor | #4 Türkiye 60.6M | 60.6M 只见于 Invest in Türkiye 转引的 UN Barometer。旅游部 2025-06 引用 2025-05 版 Barometer 的数字是 **56.7M**（[Hürriyet](https://hurriyetdailynews.com/turkiye-moves-to-fourth-place-in-most-visited-countries-list-210664)），部里自己的边境数是 52.63M 外国人 + 9.64M 海外侨民 = 62.27M。另有媒体把 60.6M 标成 2025 年数据。如果取 56.7M，土耳其会低于意大利的 57.7M，名次互换，洞察卡 5 也就不成立。不过 UN Tourism 自己公布的 2024 排名是土耳其第 4、意大利第 5，与本片一致。 | 主值暂时保留，在 sources.md 写明这三个数和取舍理由。发布前 7 天复核时，以 UN DB 或 Barometer 原表的土耳其 2024 TOUR 为准，如果低于 57.7M，就交换 #4 / #5 并改洞察卡 5。 |
| 4 | minor | #47 Argentina 6.60M | INDEC 的 2024 头条是 **6.2M** 国际游客、−8.4%（[Bloomberg Línea](https://www.bloomberglinea.com/latinoamerica/argentina/turismo-internacional-a-la-argentina-cayo-84-en-2024-ante-apreciacion-del-super-peso/)），比 UN DB 的 6.604M（Subsecretaría 基于 INDEC 的全国估计）低 6%。如果改用 6.2M，阿根廷会掉到 #49 附近，只在榜尾小幅换位，不会出榜。 | 保留 UN DB 值，在 sources.md 的交叉核对一栏补上 INDEC 6.2M 和口径说明（ETI 头条与全国总估计的区别）。 |
| 5 | minor | #41 Uzbekistan | 统计局公布的 2024 全年数是 8.2M（[Daryo](https://daryo.uz/en/2025/02/03/tourist-arrivals-in-uzbekistan-hit-8-2mn-in-2024-1209283/)），UN DB 是 7.957M，差 3%。UN 把该值标为过夜，卡上却写「Incl. same-day visits」，没有找到出处证明它含当日游。 | 核实统计局的口径。证明不了就删掉这个标签，sources.md 注明 8.2M。 |
| 6 | minor | #19 Poland 署名行（约 3:26–3:32） | 署名「Photo: Annashoots 📷 / Pexels License」里的相机 emoji 在 Inter 字体里渲染成方框（tofu），抽帧 t=206、212 都能看到。 | 账本 author 改成 "Annashoots"（去掉 emoji），重渲时一起改。publish.md 里同步改。 |
| 7 | minor | 封面 `render/thumbnail.png` | 封面直接写出 #1 France 100M、#2、#3，和 Vision「看到最后才知道冠军」相冲突。 | 封面改为前三名打问号，或只放 #2–#4，把冠军留成悬念。属于人工改版项，不影响母版。 |
| 8 | minor | #21 Morocco / #22 Croatia | 屏上都显示 17.4M。摩洛哥的 17.4 是官方四舍五入后的数，克罗地亚是 17.379。如果摩洛哥的精确值 < 17.379，两者名次会互换。 | 找摩洛哥部里的精确数（17,4xx,xxx）；找不到就在 notes 注明「官方只公布 17.4M」。 |
| 9 | minor | #42 Taiwan 图 | Unsplash 页面有反爬，取不到地点字段。候选记录里只写了 "Alt: Taroko Gorge"，没有地点佐证。画面（大理石峡谷、碧绿溪流）和太鲁阁相符，但没有证实。#46 Bahrain 这张已经核实是作者在巴林拍的堡垒（同一作者另有 Karbabad 的 Bahrain Fort 系列），卡上写 "Bahrain Fort, Manama" 可以接受（实际在 Karbabad，属首都省）。 | 人工打开 Unsplash 页面，确认太鲁阁这张的地点字段；对不上就从候选里换一张。 |
| 10 | minor | publish.md 描述 | 「Per-item data sources … see the pinned comment」：置顶的 Comment 1 其实是图片署名，数据出处在 Comment 2 / 3。 | 改成 "see the pinned comment and its replies"。 |
| 11 | minor | 标题年份 | 「(2026)」写的是发布年，bible §3.3 要求写统计期，topic.md 待确认 1 还没定。 | 交用户定。屏上和描述框已写清「Data: 2024 full year」，不会误导。 |

## 英国口径：建议屏上保留 38.2M（UN Tourism）

- ONS《Travel trends: 2024》（2025-08-26，[原文](https://www.ons.gov.uk/peoplepopulationandcommunity/leisureandtourism/articles/traveltrends/2024)）给出的是海外居民访英 **42.6M visits**。原文说明了三点：① 2024 上半年用旧 IPS 设计、下半年用新设计，两半拼成全年，"there may be differences between these two halves"；② **首次并入北爱尔兰（NISRA）数据**，只有世界合计做到 UK 层级；③ 整体标为 "official statistics in development"。
- UN DB 里 2024 的 38.23M（TOUR）/ 39.03M（VSTR）标注来源为 IPS，与 2019 的 39.42M 是同一条序列。42.6M 和它之间的 4.4M 差距，很可能来自北爱尔兰并入、设计切换和当日访问。
- 理由：① 全片的规则是「UN DB 有值就用 UN DB」，统一口径；② D2「▼3% vs 2019」要求同一序列，改成 42.6M 就成了 +8%，而这个增幅主要来自统计口径变化，会误导观众；③ 无论用哪个数，英国都在第 7（低于墨西哥 45.0M，高于德国 37.4M），不影响名次和计分板。
- 做法：屏上不动，在 sources.md 和置顶评论（数据出处那条）里加一行："ONS Travel trends 2024 reports 42.6M visits (first year including Northern Ireland; survey redesigned mid-2024; official statistics in development). We use UN Tourism's 38.2M overnight figure for comparability with 2019." 评论区有人问时可以直接引用。

## 核对过的数据样本（亲自联网 + UN 原表）

UN DB 一列由我直接读 `_build/raw/UN_Tourism_inbound_arrivals_12_2025.xlsx` 得到（单位：千人次）。

| # | 国家 | 屏上 | 我核到的值与出处 | UN DB 原表 | 统计期 | 结论 |
|---|---|---|---|---|---|---|
| 1 | France（冠军） | 100M，Official estimate | 经济部 / Atout France：2024 年 "plus de 100 millions"，是 Atout France 的预估（[economie.gouv.fr](https://www.economie.gouv.fr/node/3232816)、Atout France 2025-01 简报） | 2024 无值；2019 TOUR 90,914 | 2024 | 通过（卡上已标 estimate） |
| 2 | Spain | 93.8M | INE FRONTUR 2025-02-03：93.8M，+10.1%（[INE](https://ine.es/dyngs/Prensa/es/FRONTUR1224.htm)） | 93,759.297 | 2024 | 通过 |
| 3 | United States | 72.4M | NTTO：72,390,321，相当于 2019 的 91%（[IITA](https://www.inboundtravel.org/news/ntto-2024-international-inbound-numbers)、trade.gov 2025 Forecast） | 72,390.321 | 2024 | 通过 |
| 4 | Türkiye | 60.6M | Invest in Türkiye 引 Barometer 为 60.6M；部长引 2025-05 Barometer 为 56.7M；部里边境数 62.27M | 2024 无值 | 2024 | 存疑，见问题 #3 |
| 5 | Italy | 57.7M | UN 原表 57,725 = Banca d'Italia 边境调查（制作方另附 BdI 表 2 的 57.8M） | 57,725 | 2024 | 通过 |
| 7 | United Kingdom | 38.2M | ONS 42.6M（含北爱尔兰、设计切换），见上节 | 38,229.568 | 2024 | 保留 38.2M |
| 8 | Germany | 37.4M | 聚合站引 Destatis：37.4M，+7.5%（[BusinessTats](https://businesstats.com/accommodation-industry-in-germany-statistics-facts/)）；Destatis 原表没有取到 | 37,420（Supply-side） | 2024 | 通过（二手佐证） |
| 9 | Japan | 36.9M | JNTO：36,869,900（后来修订为 36,870,148），2019 = 31,882,049（[JNTO PDF](https://asset.japan.travel/image/upload/v1737079137/pdf/Number_of_visitor_arrivals_to_Japan_in_December_2024.pdf)） | 36,870 | 2024 | 通过 |
| 10 | Greece | 36.0M ▲15% | BoG 初值 35,951.4 千，不含邮轮（abnase 转引）；2019 初值同口径 31.3M（[GTP](https://news.gtp.gr/2020/02/21/greece-welcomes-rise-travel-receipts-2019/)），所以 +15% 是同口径 | 2019 TOUR 31,348 | 2024 | 通过 |
| 12 | Austria | 32.2M | Statistik Austria：外国客人到达 32.20M（[Advantage Austria](https://www.advantageaustria.org/ch/zentral/branchen/tourismus-nach-oesterreich/zahlen-und-fakten/Zahlen_und_Fakten.de.html)） | — | 2024 | 通过 |
| 17 | Netherlands | 21.3M | CBS：外国客人 21.31M，后修订为 21.28M（[CBS](https://www.cbs.nl/en-gb/news/2025/10/over-50-million-holiday-guests-in-2024)） | — | 2024 | 通过 |
| 18 | Canada | 19.9M | StatCan：非居民赴加 29.8M trips，含当日（[StatCan](https://www150.statcan.gc.ca/n1/daily-quotidien/250825/dq250825b-eng.htm) 等），等于 UN VSTR 29,818；TOUR 是其中的过夜部分 | 19,913 / VSTR 29,818 | 2024 | 通过（同一序列） |
| 27 | Indonesia | 13.6M | BPS：2024 外国游客 13,902,420，等于 UN VSTR 13,902；TOUR 是其中的过夜部分 | 13,603 / 13,902 | 2024 | 通过 |
| 33 | Kazakhstan | 10.4M ▲22% | 旅游部：15.3M 访客中 10.4M 停留超过一天 | 10,381.566（D：只含过夜） | 2024 | 主值对；标签和 D2 错，见问题 #1 |
| 41 | Uzbekistan | 7.96M | 统计局 8.2M | 7,957.213 | 2024 | 小差，见问题 #5 |
| 44 | Cambodia | 6.70M ▲1% | 旅游部 6,700,125；2019 年 6.6M（[The Star](https://www.thestar.com.my/aseanplus/aseanplus-news/2025/02/02/thai-vietnamese-and-chinese-tourists-account-for-two-thirds-of-cambodia039s-international-guests-in-2024)） | — | 2024 | 通过 |
| 46 | Bahrain | 6.62M ▲21% vs 2023 | 开放数据：过夜 6.6M（+20.7%），总访客 14.9M，其中当日 8.3M（[GDN](https://www.gdnonline.com/Details/1288850/Inbound-tourism-increases-by-51pc) 等） | 6,618 / VSTR 14,882 | 2024 | 通过 |
| 47 | Argentina | 6.60M | INDEC 6.2M，−8.4% | 6,603.877 | 2024 | 存疑，见问题 #4 |
| 50 | Philippines | 5.95M | DOT：5,949,350，其中海外菲律宾人 510,383（[Manila Times](https://manilatimes.net/2025/01/09/news/national/dot-2024-tourist-arrivals-surpass-previous-records/2033489)、MB） | 2019 TOUR 8,261 | 2024 | 通过 |
| 15 | Malaysia（图） | — | Unsplash 页面地点 "Kampung Kiau, Ranau, Sabah"，标签 mount kinabalu | — | — | 图认对 |

共 19 国：数值或口径通过 14 项；存疑 4 项（土耳其、阿根廷、乌兹别克斯坦，以及主值对但标签和 D2 错的哈萨克斯坦）；英国单列（见上节）。制作方标「未核到」的项里，抽到德、日、希、奥、荷、加、印尼、哈、乌、柬、巴林、阿根廷、菲共 13 项，其中只有 UN 一个来源的 11 项全部抽了。

脚本复核：
- 50 项的 ▲▼% 都和 `change_base` 重算一致；`value_display` 取 3 位有效数字（突尼斯 10.25 → 10.3M，按四舍五入）。
- 洞察卡 1–5：台湾 −33.8% 是 2019 基准里跌幅最大（其次菲 −28.0%、匈 −22.3%）；阿尔巴尼亚 +87.4% 最大；沙特 +69.6% 是前 15 名最大；土 +18.4% / 意 −10.5%。都成立。
- 大洲计分 20 / 18 / 4 / 4 / 3 / 1，合计 50，与屏上一致。

## 图片（50 / 50）

- 账本：50 张都在 `assets.json` 里，sha256 与文件一致，卡上署名的作者 = 账本 author。许可只有 Unsplash License（45）和 Pexels License（5），都在白名单内。FoP 备注合理：香港、新加坡、伦敦都可以拍公共场所建筑；阿联酋、卡塔尔等没有商用 FoP 的国家都没上榜，也没有用现代地标。
- 逐张看过（`_build/qc/img_sheets/imgs_00–05.jpg`）：
  - 主体都认对了：圣米歇尔山、阿尔罕布拉、大峡谷、卡帕多奇亚、斗兽场、奇琴伊察、威斯敏斯特、新天鹅堡、富士山 + 忠灵塔、雅典卫城、郑王庙、哈尔施塔特、Hegra（孤独城堡）、佩纳宫、京那巴鲁山、维港、小孩堤防、梦莲湖、克拉科夫中央广场、下龙湾、舍夫沙万、杜布罗夫尼克、景福宫、大三巴、吉萨、查理大桥、婆罗浮屠、佩莱什城堡、匈牙利国会、滨海湾金沙、马特洪峰、Ksamil、恰伦峡谷、西迪布赛义德、泰姬陵、布鲁塞尔大广场、桌山、绍纳岛、斯德哥尔摩老城、十二使徒岩、雷吉斯坦、太鲁阁、糖面包山、吴哥窟、盖朗厄尔峡湾、巴林堡、莫雷诺冰川、莫赫悬崖、卡塔赫纳、爱妮岛。
  - 短边都 ≥ 1,580 px，构图适合 720×800 满版卡，没有水印，看不出 AI 痕迹，也没有生成图。
- 唯一没能证实的是台湾这张的拍摄地点（见问题 #9）。
- 成片里的裁切都保住了主体：塔尖、富士山、斗兽场、圣米歇尔山尖顶都完整。

## 成片技术核对

- ffprobe：h264 1920×1080，r_frame_rate 60/1，nb_frames 22,526，时长 375.433 s，等于 manifest 的 range_s；AAC 静音轨。编码参数 libx264 crf16（码率只有约 2.2 Mbps，是因为画面变化少，看帧没有压缩块）。
- 时间线：intro 0–5，scroll 5–340.43，champion 340.43–346.43，tally 346.43–353.43，sources 353.43–357.43，end 357.43–375.43。publish.md 的章节时间（1:08 #40、2:16 #30、3:24 #20、4:32 Top 10、5:36 No. 1、5:47 计分板）和抽帧一致。
- 亲眼看过的内容：
  - 片头标题、口径行、来源行完整。
  - 5 张洞察卡全文完整、没有出框，都有 sources.md §5 支持。
  - 冠军面板（No. 1 / 100M / ▲10% vs 2019）、角落计分板逐步累加、结尾大洲条形图（Europe 20 高亮）都正确。
  - 来源卡和片尾干净。
  - 没有占位卡；▲▼ 字形正常；国旗与国家逐一对应，含 HK / MO 区旗与 SAR OF CHINA 徽章、台湾、沙特、哈萨克、乌兹别克、柬埔寨。
  - 唯一的字形问题是问题 #6 的 emoji 方框。

## 观众视角（全球英文观众）

- 好看的地方：照片质量整体很高，满版卡在手机上 3 秒内能读出国名和数值。▲▼ vs 2019 让「谁恢复了、谁没恢复」一目了然。洞察卡「China isn't ranked」和「Türkiye overtook Italy」都是评论区能吵起来的点；希腊 36M 不含邮轮、香港只算过夜这类小标签，让整份榜单显得可信。
- 可能划走的地方：#50–#31 约 2 分钟都是中小国家，节奏平，现在又没有配乐，最容易流失。等配乐做好后，前段可以考虑减到每名约 6 s。冠军被封面剧透（问题 #7），会削弱看到最后的动机。
- 评论区风险：「中国 / 阿联酋去哪了」已经由洞察卡 3 和 scope_note 回应，但阿联酋只在描述框里提到。只算迪拜就有 18.7M，按这个数它会排在第 20 名左右，阿联酋观众很可能会追问。建议在置顶评论里加一句说明。

## 抽帧清单（`_build/qc/frames/`，拼图在 `_build/qc/sheets/sheet_00–11.jpg`）

- 片头 t=0.5 / 2.5 / 4.5 s。
- 滚动段从 t=8 s 起每 6 s 一帧，到 338 s 为止（共 56 帧）：覆盖 #50 → #1 全部 50 张卡，以及 5 张洞察卡（after 41：约 56–68 s；after 31：约 122–140 s；after 21：约 194–206 s；after 11：约 260–266 s；after 4：约 314–326 s）。第 10 名附近 t=266–278 s，冠军入场 t=332–338 s。
- 冠军 t=341 / 343 / 345.5 s，计分板 t=348 / 350 / 352.5 s，来源卡 t=355 s，片尾 t=358 / 365 / 374.5 s。
- 局部放大检查：`_build/qc/crop_header_t50.png`、`crop_header_t4.5.png`（顶栏标题完整，拼图上看起来被截是标签框遮挡造成的）。
- 脚本：`_build/qc/extract_frames.py`、`sheets.py`、`img_sheets.py`。

## 未审 / 留待下轮

- 配乐版（不存在）：响度、高潮是否对上前 10 名、片尾淡出。
- 竖版 Shorts（未产出）。
- 台湾图的拍摄地点（Unsplash 反爬）。
- 德国 Destatis 原表，以及土耳其 UN 原表（Barometer 附表）。
