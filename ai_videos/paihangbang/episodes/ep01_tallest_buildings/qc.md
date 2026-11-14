# 独立审片（fresh-context 子代理，2026-11-03）

> 审片对象：`render/ep01_tallest_buildings_master.mp4`（sha256 `0d4beaef…a166f6`，与 manifest 一致；1920×1080，60 fps，331.0 s，19 860 帧）。
> 输入：`data.json`、`sources.md`、`assets.json`、`topic.md`、`publish.md`、`render/thumbnail.png`、`render/*.manifest.json`、`_build/override_reasons.json`；规则：`../../bible.md` §2/§3/§4/§7、`../../data_contract.md`。
> 审片人没有参与制作。除本文件外没有改动任何文件，也没有调用收费服务。
> 抽帧在会话 scratchpad `qc_ep01/`：全片每 2 s 一帧（166 帧，1280 宽），0–6 s 每 0.5 s 一帧，290–331 s 每 1 s 一帧，章节时间点各 1 帧，另有 640×360 手机尺寸样张。实际看过约 120 帧（6 联拼图加单帧全分辨率），覆盖全部 50 张名次卡、5 张洞察卡、冠军段、计分板、来源卡、片尾和封面。
> 音轨按设计为静音（音乐待做），只记录，不算缺陷。

## 结论：**修后可发布**

数据层面没有发现错误：名次、数值、国旗、计分板、洞察卡都和 CTBUH 现行榜单以及我自己的计算一致，滚动速度恰好每帧 2 px。不能直接发布的原因有三条 major，外加一项必须由人做的版权决定：

1. 冠军卡（#1 Burj Khalifa）的照片是逆光雾霾里的天际线，塔身只是太阳旁边一根细线，看不出是哪座楼。这张图同时用在封面上，还属于 FoP RISK。
2. 封面左格就是这张图，点击率弱，也把 RISK 图片放进了宣传位。
3. 描述框没有写口径说明。`topic.md` 承诺的「per CTBUH status as of 3 Nov 2026」、建筑高度定义，以及为什么不收已开业的重庆陆海国际中心、山东 IFC，都没有写进去；而 Wikipedia 把这两座列在第 18 和第 30 名。

版权决定：5 张标 RISK 的图要逐张定保留、换图还是占位（建议见第 4 节）。`topic.md` 和 `sources.md` 都写了「发布前须人工决定」，目前还没有决定记录。这一项不归审片人判定，但做完之前不应上传。

## 1. bible §7 审片清单

| # | 检查项 | 结果 | 证据 |
|---|---|---|---|
| 1 | 名次连续、无重复，排序和 `data.json` 一致 | **通过** | `data.json` 按 value 降序排列；竞争排名自算结果与 rank 字段完全一致（8/8、20/20、22/22 并列，没有 9、21、23）。画面上按 #50→#1 依次出现（逐张核对拼图 t=4–300 s），没有漏卡或重复卡。第 50 名 388.05 m，第 51 名 30 Hudson Yards 387.1 m，切线处无并列 |
| 2 | 每个数值能在 `sources.md` 追到出处，统计期与片头一致 | **通过** | `sources.md` §2 逐条列出 CTBUH 单楼 URL 和 Wikidata 交叉核对。我另抓了 CTBUH「100 Tallest Completed Buildings」页（2026-11-03），第 1–51 名的名称、高度、层数、竣工年与 `data.json` 全部吻合。片头和角标都写「Completed buildings, Nov 2026」，与来源一致。英尺值与米换算误差都 ≤1 ft |
| 3 | 国旗和国家对得上 | **通过** | 11 个国家的国旗逐一看过（CN、US、AE、MY、KR、SA、TW、RU、VN、KW、EG）。香港计入 China、台北 101 用 Taiwan，按 `topic.md` 定好的口径 |
| 4 | 每张图都在 `assets.json` 里，许可属允许类型 | **通过**（版权决定待人做） | 45 张图都在账本里，sha256 与文件逐一吻合，账本里没有多余条目。许可只有 CC0、CC BY 2.0/3.0/4.0、CC BY-SA 2.0/3.0/4.0，没有 NC、ND 或 GFDL-only。卡上署名与账本作者一致。另 5 座无图（image=null）。FoP 见第 4 节 |
| 5 | 文字不出框、不闪烁；手机全屏 3 秒内看清名称和数值 | **部分不通过**（minor） | 不闪烁：在 t=20、140、250 s 各取连续 11 帧做位移匹配，每帧都恰好 2 px，残差约 0，没有亚像素重采样；匀速段没有冻帧（用 freezedetect 检查）。手机：640×360 下名称和数值清楚，层数和年份标签偏小但能读。出框问题：两个名称被省略号截断（缺陷 #5） |
| 6 | 音乐无爆音，高潮对上前 10 名，片尾 15–20 s 干净 | **未检** | 按设计静音（-91 dB）。音乐做好后要重审。片尾画面 313–331 s 共 18 s，干净 |
| 7 | 描述框的来源与署名完整 | **通过**（口径说明缺失，见缺陷 #3） | 描述 2 961 字符（≤5000），不含 `<` `>`。45 条署名齐全，注明「resized and cropped」。置顶评论 8 427 字符、评论 2 8 203 字符（都 ≤10000），含许可链接和源文件链接 |

### 附加检查

| 项 | 结果 | 证据 |
|---|---|---|
| 计分板 | **通过** | 自算：CN 26、US 8、AE 4、MY 4、KR 2，SA、TW、RU、VN、KW、EG 各 1，合计 50。角落计分板逐张累加（t=4 时 CN 3；t=144 时 CN 15、US 6；t=292 时 CN 26、US 8、AE 4、MY 4、KR 2），揭晓画面与自算一致。只显示前 8 名的问题见缺陷 #7 |
| 洞察卡（5 张） | **通过** | 按 `data.json` 和 CTBUH 竣工年复算：①2025 年竣工 4 座（JPMorganChase、Zijin、Ningbo T1、CMB）✓；②深圳 6 座、纽约 6 座，其他城市最多是迪拜和吉隆坡各 4 座 ✓；③2020 年及以后 15 座 ✓；④美洲 8 座全在美国 ✓；⑤高于 600 m 的已建成建筑 4 座（第 4 名 601 m，第 5 名 599 m）✓。说明：①③依赖 CTBUH 竣工年。Wikipedia 的年份有出入（宁波中心记 2024，Merdeka 记 2024，Iconic 记 2023），但片中只用 CTBUH，口径前后一致 |
| 时间线 vs bible §2.2 | **通过** | 片头 5 s，冠军 296–302 s，计分板 302–309 s（7 s），来源卡 309–313 s（4 s），片尾 313–331 s（18 s）。前 10 名约 232–292 s，每名约 6 s，卡片放大 |
| 章节 | **通过**（有一个小问题） | 0:00 开头，共 7 段，最短间隔 4:52→5:02 正好 10 s，合规。逐点看帧：0:58 洞察卡加 #40、#39 ✓；1:57 洞察卡加 #30、#29 ✓；2:45 #22、#20、#20 ✓；3:54 洞察卡加 #10、#8 ✓；4:52 #2、#1 ✓；5:02.0 画面仍是冠军，计分板约在 5:02.5 才淡入（缺陷 #8） |
| 来源卡和片尾 | **通过** | 来源卡写了数据、口径、照片署名去向、国旗、图标、字体。片尾 18 s，「Thanks for watching!」只占顶部，下方大片空白，可以放 2 个视频元素加订阅按钮 |
| 封面 | **不通过**（major） | 1280×720。左格（#1）是同一张雾霾逆光图，见缺陷 #2 |
| 交付规格 | 通过 | H.264 High，yuv420p，60 fps，faststart；音轨是 AAC 静音占位 |

## 2. 数据抽查（独立来源）

| 名次 | 楼 | data.json | CTBUH 列表页（2026-11-03 抓取） | Wikipedia「List of tallest buildings」 | 结论 |
|---|---|---|---|---|---|
| 1 | Burj Khalifa | 828 m / 163 层 / 2010 | 828 / 163 / 2010 | 828 / 163 / 2010 | ✓ |
| 2 | Merdeka 118 | 678.9 m / 118 / 2023 | 679 / 118 / 2023（名称 Menara Merdeka Maybank） | 678.9 / 118 / 2024 | ✓（年份按 CTBUH） |
| 5 | Ping An Finance Center | 599.05 → 显示 599 m / 115 / 2017 | 599 / 115 / 2017 | 599.1 / 115 / 2017 | ✓ |
| 10 | CITIC Tower | 527.7 → 528 m / 109 / 2018 | 528 / 109 / 2018 | 527.7 / 109 / 2018 | ✓ |
| 20 | Petronas 1 / 2 | 451.9 m / 88 / 1998 | 452 / 88 / 1998（两座并列第 20） | 451.9 / 88 / 1998 | ✓ |
| 30 | 432 Park Avenue | 425.7 → 426 m / 85 / 2015 | 426 / 85 / 2015 | 425.7 / 85 / 2015 | ✓ |
| 40 | LCT The Sharp | 411.6 m / 101 / 2019 | 412 / 101 / 2019 | 411.6 / 101 / 2019 | ✓ |
| 50 | Shum Yip Upperhills T1 | 388.05 → 388.1 m / 80 / 2020 | 单楼页：388.1 m / 1,273 ft / 80 / 2020 / Completed | 388.1 / 80 / 2020 | ✓ |

**漏收与误收**：

- CTBUH 已建成榜的第 1–50 名与 `data.json` 一一对应，第 51 名是 30 Hudson Yards（387 m），所以没有漏收。
- 50 座在 CTBUH 上都是 Completed，没有误收未完工的楼。
- Wikipedia 比 CTBUH 多列两座：International Land-Sea Center（重庆，458 m，2025-09-30 开业，列第 18 名）和 Shandong IFC（428 m，列第 30 名）。CTBUH 单楼页对重庆陆海仍写 *Architecturally Topped Out*、预计 2026 年竣工。本片按 CTBUH 口径不收，口径本身没问题，`topic.md` 和 `sources.md` 也记录了；问题出在描述框没有说明（缺陷 #3）。发布前 7 天内要复核 CTBUH 状态：一旦改成 Completed，第 18 名以后整体顺延，计分板（CN 27）和洞察卡②③都要重算重渲。
- Wikipedia 列出的 2025–2026 年新楼（Ciel Dubai Marina、Hengfeng Guiyang T1、Shanghai ITC T1 等）都低于 388 m，不影响 Top 50。

**机构更名（minor）**：CTBUH 已于 2025-10-06 更名为 **Council on Vertical Urbanism（CVU）**。片头、角标、来源卡和描述框仍写「CTBUH Skyscraper Center」。数据站点 skyscrapercenter.com 还能用，但写法已经过时（缺陷 #6）。

**数据使用条款**：Skyscraper Center FAQ 写「All information provided on the Skyscraper Center is available for public use … if applicable citations referencing CTBUH are made」，图片不在此列。本片只用事实并注明出处，符合 FAQ。商用条款没有找到专门文本，如需稳妥，可发邮件到 skyscrapercenter@ctbuh.org 确认。

## 3. 缺陷清单

| # | 严重度 | 时间点 | 问题 | 建议修法 |
|---|---|---|---|---|
| 1 | **major** | 4:48–5:02（冠军段，约 14 s 停在画面上）；另见封面 | #1 Burj Khalifa 的图（`01_burj_khalifa.jpg`，ECWiki1，CC BY 4.0）是日出或日落逆光拍的雾霾天际线，塔身是阳光眩光旁的细线。卡片尺寸下看不出是哪座楼，手机上更看不清。冠军卡是全片高潮，这张图会被观众当作「没找到图」。同时属 UAE 无 FoP 的 RISK 图：担着风险，却没换来画面效果 | 换图。可选：①换一张塔身清楚的已建成照片（同样是 RISK，须人工书面接受，记进 `sources.md`）；②改用专门设计的冠军剪影卡（不能用通用的「No free-licensed photo」占位）。不建议保留现图。改后重渲冠军段 |
| 2 | **major** | `render/thumbnail.png` 左格 | 封面三格里最显眼的 #1 是同一张雾霾图，第一眼看不出是迪拜塔，点击率弱。封面是宣传素材，放 FoP RISK 图片的风险比片中更高 | 封面 #1 格换成缺陷 #1 的新方案。或者封面只用 FoP 安全的楼（Merdeka 118、Shanghai Tower、Ping An 等），#1 格改成「828 m ?」悬念文字或剪影 |
| 3 | **major** | `publish.md` 描述 | 缺口径说明。`topic.md` 写了描述框要注明「per CTBUH status as of 3 Nov 2026」，实际没写。也没说明高度含尖顶、不含天线，只收已建成的建筑、不收塔类构筑物，以及为什么不收已开业的重庆陆海国际中心和山东 IFC。观众拿 Wikipedia 一对，就会在评论区说「榜单错了」或「漏了」。这和 D1「每个数字有出处」的定位冲突 | 在描述第二段加 2–3 行，例如：「Ranking = architectural height (incl. spires, excl. antennas) of buildings with status *Completed* in the Skyscraper Center database (CVU, formerly CTBUH) as of 3 Nov 2026. Chongqing's International Land-Sea Center and Jinan's Shandong IFC are still listed as 'topped out', so they are not included yet.」置顶评论开头也加同一句 |
| 4 | 待人工决定（发布闸门） | 见第 4 节 | 5 张 RISK 图（Burj Khalifa、23 Marina、Al Hamra、Iconic Tower、Landmark 81）还没有人工决定记录。另外，同为 UAE 的 Marina 101 和 Princess Tower 用了占位，23 Marina 和 Burj 却放了照片，标准不统一（`sources.md` 自己也写了「未加标只说明 Commons 没人处理过」） | 人按第 4 节逐张决定，把结论写进 `sources.md` §3 和 `assets.json` 的 fop_note |
| 5 | minor | 0:28–0:46（#43）、2:08–2:22（#27） | 名称被截断加省略号：「Guiyang International Financial Cente…」「Guangzhou International Finance Cen…」，违反 §7.5「文字不出框」 | 改用通行短名「Guiyang IFC T1」「Guangzhou IFC」，或者让渲染器允许名称折两行 |
| 6 | minor | 全片角标、0:00 片头、5:09 来源卡、描述 | 「CTBUH」已更名为 CVU（2025-10-06） | 写成「Skyscraper Center (CVU, formerly CTBUH)」，或注明「CTBUH (now CVU)」 |
| 7 | minor | 5:02–5:09 计分板揭晓 | 只显示前 8 个国家，合计 47。越南、科威特、埃及（各 1）被省略，而同为 1 座的俄罗斯显示出来了，取舍标准看不出来 | 加一行「+3 others (1 each)」，或者 11 国全显示（版面放得下） |
| 8 | minor | 章节 5:02 | 5:02.0 画面还是冠军卡，计分板约 0.5 s 后才淡入 | 章节改成 5:03（与 4:52 间隔 11 s，仍 ≥10 s） |
| 9 | minor | 0:28–0:46（#43 Guiyang IFC T1） | 占位卡写「No free-licensed photo available」，但这座楼在中国，FoP 没问题；没放图的真实原因是认不准是哪座楼，所以这句话不准确。另外 5 张占位卡里有 1 张在前 10 名（#6 Lotte World Tower，4:15–4:27），通用占位卡显得像没做完 | Guiyang：到 Commons 找 2021 年以后的已建成照片补上。占位卡改成有设计感的剪影卡（楼形剪影或「Photo unavailable for copyright reasons」这类更中性的说法），至少把 #6 做好 |
| 10 | minor | 全片名次卡 | 竖图被缩成卡中间约 40% 宽的一条，两侧是模糊填充，手机上楼显得很小。topic.md 原计划是「按 4:3 或方形裁切，以塔身中上段为焦点」。个别构图问题：#33 JPMorganChase（1:36–1:46）是夜景，旁边 One Vanderbilt 发光的尖顶比主体还抢眼，观众可能认错楼；#45 CMB Global HQ（0:24–0:36）前景有一根带监控探头的灯杆 | 渲染器改成填满裁切、上部对焦（不能截掉塔顶）。#33 和 #45 有更好的已建成照片就换掉 |
| 11 | minor | 0:03.5–0:04.0 | 片头标题淡出后约 0.5 s 几乎全黑，然后卡片才滑入。bible §2.2 要求第一张卡与片头同时进场 | 标题淡出和卡片进场交叠 |
| 12 | minor | 描述 / 置顶评论署名 | #11 写成「User:Sinsyuan」，带了 wiki 前缀。#1 的 Commons 作者字段是 ECWiki1，但文件标题写的摄影者是 Eric Chamchoum | 改成「Sinsyuan」。#1 如果保留，写「ECWiki1 (Eric Chamchoum)」 |

没有 blocker 级缺陷，也就是没有数据错误、错楼、未完工的楼或许可不合格的图。

### 每张图是不是所写的那座楼（目检）

逐张看过 45 张原图和片中卡片：

- 一眼可认，判为正确：Merdeka 118、Shanghai Tower、Makkah Clock Tower、Ping An、1 WTC、Guangzhou CTF、Tianjin CTF、CITIC Tower、Taipei 101、SWFC、ICC、Central Park Tower、Lakhta、Landmark 81、Exchange 106、Petronas（两张都拍到双塔，可以接受）、Suzhou IFS、Zifeng、Willis、KK100、GZIFC、111 W 57th、One Vanderbilt、432 Park、Trump Chicago、Jin Mao、Al Hamra、Two IFC、Iconic Tower、China Resources Tower、CITIC Plaza。
- 外形和 Commons 描述或分类相符，判为大概率正确：Wuhan Greenland、Changsha IFS T1、Wuhan Center、JPMorganChase（Commons 描述明确写 270 Park Ave 位于 432 Park 和 One Vanderbilt 之间）、Minying T2、Zijin、Ningbo T1、Guangxi CR、CMB Global HQ（Commons 分类为 China Merchants Bank Tower Global HQ，2026-03 拍摄，已建成）、23 Marina（Commons 描述是「23 Marina」，分类相符）、Citymark、Upperhills T1。
- 不可辨认：#1 Burj Khalifa（缺陷 #1）。
- 没有发现在建状态的楼（塔吊、未封顶）。The Exchange 106 图下方的塔吊属于周边工地，主塔已完工；111 W 57th 是 2021-05 的照片，当年竣工。

## 4. 版权建议（供人决定，不是法律意见）

前提：频道开收益，风险主要不在 Content ID（建筑不在其中），而在建筑师或开发商发起版权投诉，导致删片或警告。新频道吃一次警告的代价很高。概率很低，但不是零。建议按「画面价值 vs 风险」逐张定，同一国家的楼统一标准。

### 标 RISK、目前放了图的 5 座

| # | 楼（国家） | 现图 | 建议 | 理由 |
|---|---|---|---|---|
| 1 | Burj Khalifa（UAE） | 逆光雾霾天际线 | **换**：换成清楚的照片（人书面接受 RISK），或换成设计过的冠军剪影卡 | 现图风险和清楚的照片一样，画面价值却接近零，最不划算。冠军卡画面价值最高，值得人专门拍板。不论选哪种，**封面都不要用 RISK 图** |
| 47 | 23 Marina（UAE） | 街拍仰视 | **改占位** | 排名靠后，画面价值低。同城、同法律的 Marina 101 和 Princess Tower 已经是占位，统一标准 |
| 38 | Al Hamra Tower（科威特） | 从科威特塔拍的城市远景，Al Hamra 是主体 | **人决定，倾向改占位** | 科威特没有 FoP。照片虽是远景，但主体明确，「附带入镜」的理由站不住 |
| 44 | Iconic Tower（埃及） | 新行政首都 CBD 群楼，Iconic 是主体 | **人决定，倾向改占位** | 埃及法律只允许个人使用。图本身质量好；如果要保留，须人书面接受 |
| 17 | Landmark 81（越南） | 西贡河边远景，Landmark 81 是主体 | **人决定，倾向改占位** | 越南从 2023 年起只允许非商用。照片拍于 2021 年并不能免责，看的是使用时间 |

如果人倾向保留照片：至少把 1 号换掉；其余 4 张统一按「接受风险」处理，并在 `sources.md` 记下理由。不要出现同一国家有的楼放照片、有的楼占位的情况。

### 没有图的 5 座

| # | 楼 | 建议 | 理由 |
|---|---|---|---|
| 6 | Lotte World Tower（韩国） | **保留占位，但重做占位样式** | 韩国 FoP 仅限非商用，Commons 上不打码的图都带 NoFoP 标签。这张在前 10 名，通用占位卡显得像没做完，建议做成楼形剪影 |
| 40 | LCT The Sharp（韩国） | 保留占位 | 同上 |
| 31 | Marina 101（UAE） | 保留占位 | 已建成状态的图都带 NoFoP-UAE |
| 37 | Princess Tower（UAE） | 保留占位 | 同上 |
| 43 | Guiyang IFC T1（中国） | **补真实照片** | 不是版权问题，中国 FoP 允许。找一张认得准的已建成照片；找不到的话，占位文案改成不涉及许可的说法 |

## 5. 观众视角

- **节奏**：5:31。50→11 名每名约 5.3 s，前 10 名约 6 s，同屏 3 张卡，信息密度合适。洞察卡以橙色卡片插在队列里，节奏有变化。少了音乐，整片偏单调，要等配乐后再评。冠军段约 10 s，加一个「No. 1」标注，没有音乐时力度不够，配乐要在 4:48 前后给足。
- **可读性**：640×360 下名称和数值都看得清。长名称会自动缩小字号，仍可读，但有两个被截断（缺陷 #5）。角落计分板的国旗小，但数字能读。
- **滚动平滑度**：t=20、140、250 s 三段各取连续 10 个帧间隔，位移全是 **2 px/帧**，帧差残差 0.00–0.02（0–255 灰度），没有亚像素抖动，匀速段没有冻帧。
- **可能出丑或误导的地方**：①冠军图看不出是迪拜塔（缺陷 #1）；②评论区会有人说「重庆陆海中心呢？」，描述框没有预先回答（缺陷 #3）；③一共 5 张「No free-licensed photo」占位卡，1 张在前 10 名，显得像没做完；④香港计入中国、台湾单列，这是 topic.md 定的口径，可能引来政治争论，属于预期内的风险，不算缺陷。
- **差异化（bible D1–D4）**：D1 有（片头口径行、来源卡、描述加置顶评论），但缺口径说明（缺陷 #3）。D2 只做了 NEW 2025 角标，共 4 个，第一期没有上期可比，可以接受。D3、D4 完整。

## 6. 没能检查的内容

- 音乐和混音（§7.6）：片子静音，要等配乐后重审。高潮是否对上前 10 名、片尾淡出，都没检。
- YouTube 上传后的实际效果（章节识别、片尾元素遮挡、封面在搜索结果里的样子）。
- Commons 元数据只抽查了 9 张（Burj、23 Marina、CMB、111 W 57th、JPMorganChase、Al Hamra、Iconic、Landmark 81、Makkah）。之后接口返回 429 限流，其余 36 张的作者、许可和 FoP 模板以 `assets.json` 为准，没有逐张复核。
- 各国 FoP 的法律结论（尤其 UAE Decree-Law 38/2021 第 22.7 条「broadcasting programs」能否覆盖 YouTube）：需要法律意见，本报告只做风险提示。
- CTBUH/CVU 的数据商用条款：只找到 FAQ 里的「public use with citation」，没有找到正式 ToS 文本。
- 几座中国楼（Zijin、Minying T2、Guangxi CR、Changsha IFS T1、Wuhan Center、Citymark、Upperhills T1）只凭外形加 Commons 描述判断为正确，没有用街景或官方图逐一比对。
- 抽帧间隔是 2 s。每张卡至少看过 2–3 帧，但 2 s 之间如果有单帧闪烁，抽帧可能漏掉。不过 freezedetect 和三段连续帧位移检查都没有发现异常。

参考：CTBUH 已建成榜 https://www.skyscrapercenter.com/buildings ；单楼页 https://www.skyscrapercenter.com/building/shum-yip-upperhills-tower-1/16001 、https://www.skyscrapercenter.com/building/international-land-sea-center/148 ；Wikipedia https://en.wikipedia.org/wiki/List_of_tallest_buildings ；更名 https://elevatorworld.com/news/daily-news/ctbuh-announces-name-change-to-council-on-vertical-urbanism/ ；FAQ https://www.skyscrapercenter.com/faq 。

## 复审（fresh-context 子代理，2026-11-03，第 2 轮）

- 审片对象：
  - 默认母版 `render/ep01_tallest_buildings_master.mp4`：sha256 `40d152e8…8650c9`，与 manifest 一致。1920×1080，60 fps，331.0 s。时间线：intro 0–5，scroll 5–296，champion 296–302，tally 302–309，sources 309–313，end 313–331。
  - 对照版 `render/ep01_tallest_buildings_master_with-risk-images.mp4`：sha256 `75c088f5…40c04`，与 manifest 一致，时间线相同。
- 输入：`data.json`（新增字段 image_risk / image_note / scope_note、短名、source_line）、`publish.md`、`render/thumbnail.png`、`_build/11_post_qc_fixes.py`、`sources.md`。
- 方法：
  - 抽帧：默认母版每 3 s 一帧，拼成 7 张 4×4 接触表，覆盖全片，实际看过约 110 帧。
  - 关键帧（1280 宽）：片头 3.0–5.0 s 每 0.25 s 一帧，并测逐帧亮度；章节点 7 个，含 5:02 / 5:02.5 / 5:03；冠军段、计分板、来源卡、片尾；占位卡 #6、#43、#44；#11 署名局部；回归抽查 21、80、130、190、275、320 s。
  - 对照版：抽查 21、36、69、186、299 s 共 5 帧。
  - 运动：60、140、250 s 各取连续 8 帧，测得位移都是 2 px/帧，残差 ≤0.015。全片跑了 freezedetect：滚动段没有冻帧，冻帧只出现在片头标题停留段、冠军定格之间的短暂静止，以及计分板、来源卡和片尾。
- 帧文件位置：`C:\Users\light\AppData\Local\Temp\claude\C--workspace-micro-drama-platform\ce8ad49c-b9a5-4916-a2cc-04ed64900cb6\scratchpad\qc_r2b\e1\`，对照版在 `e1r\`。
- 审片人没有参与制作。除本节追加的内容外，没有改动任何文件，也没有调用收费服务。

### 上轮缺陷逐条复核

| # | 上轮问题 | 结论 | 证据 |
|---|---|---|---|
| 1 | 冠军卡照片是雾霾逆光图，看不出是迪拜塔（同时是 RISK 图） | **交人决定** | **默认母版**：冠军卡改为 UAE 国旗 + 楼形图标的占位卡，下方写「Photo withheld: architecture copyright」，配有橙色光晕、奖杯和「No. 1 / 828 m / 2,717 ft」（4:56–5:02，帧 299 s）。RISK 图已从成片中去掉，但全片高潮处没有任何楼的画面，原因说明也几乎看不见（见 N1）。<br>**对照版**（299 s）：用的仍是原来那张雾霾逆光图，没有换成塔身清楚的照片。人如果选对照版，上轮的画面问题原样存在。<br>建议人在三条路里选一条：①接受默认版的占位卡（先修 N1）；②换一张清楚的照片，并书面接受 RISK；③做专门的冠军剪影卡。不建议「对照版 + 现图」 |
| 2 | 封面 #1 用了雾霾 RISK 图 | **已修复** | `thumbnail.png` 左格改为深色底、橙色楼形图标加「Burj Khalifa」「#1 828 m」，没有用 RISK 图。中格 Merdeka 118、右格 Shanghai Tower 都是 CC0，封面不需要署名。左格的吸引力仍弱于照片，是否加强（例如「828 m?」悬念字）交人决定，不阻塞发布 |
| 3 | 描述框缺口径说明 | **已修复** | 描述在 Chapters 后面加了「What counts: … completed by the Council on Vertical Urbanism (CVU, formerly CTBUH) Skyscraper Center on 3 Nov 2026, measured to the architectural top (spires count, antennas don't). Chongqing's International Land-Sea Center (458 m) and Shandong IFC (428 m) are topped out but not yet listed as completed … Hong Kong is counted under China.」。`data.json` 有对应的 `scope_note`。上轮建议在置顶评论开头也加一句，这一条没做，属可选 |
| 4 | 5 张 RISK 图没有人工决定，同国标准不统一 | **交人决定** | 默认母版把 5 张 RISK 图（#1、#17、#38、#44、#47）一律改为占位，同国标准统一了：UAE 的 #1、#31、#37、#47 现在全是占位。对照版里 5 张都在（已核对 21、36、69、186、299 s 的帧：23 Marina、Iconic Tower、Al Hamra、Landmark 81、Burj Khalifa）。<br>`sources.md` §3 还没有人工决定的记录。人选定版本后要写进 `sources.md` 和 `assets.json` 的 fop_note。另外，**`publish.md` 只对应默认母版**，见 N2 |
| 5 | 两个名称被省略号截断 | **已修复** | 卡上显示「Guiyang IFC T1」（帧 36 s）和「Guangzhou IFC」（帧 130 s），全称记在 notes。接触表逐卡看过，其余长名（China Merchants Bank Global HQ、Guangxi China Resources Tower、Minying International Trade Center T2、Shanghai World Financial Center、Trump International Hotel & Tower）会自动缩小字号，都没有省略号 |
| 6 | 「CTBUH」已更名 CVU | **已修复（留一处小尾巴）** | 片头、全片角标、来源卡都写「Data: Skyscraper Center (CVU, ex-CTBUH), Wikidata (CC0)」，描述也一样。剩下的问题：评论 2 逐条出处仍是「CTBUH Skyscraper Center, 100 Tallest Completed Buildings…」，共 50 处。属 nit，建议生成器统一写成「Skyscraper Center (CVU, ex-CTBUH)」 |
| 7 | 计分板只显示前 8 国 | **已修复** | 5:05（帧 305 s）列出 11 国：China 26、United States 8、United Arab Emirates 4、Malaysia 4、South Korea 2，Saudi Arabia、Taiwan、Russia、Vietnam、Kuwait、Egypt 各 1，合计 50，与 `data.json` 自算一致。国旗都对 |
| 8 | 章节 5:02 时还是冠军画面 | **已修复** | 章节改为「5:03 Buildings by country」。5:02.0 仍是冠军定格；5:02.5 计分板标题和国家列已经出现；5:03 条形正在生长。其余章节逐点看帧都对：0:58 洞察卡 + #40 + #39；1:57 洞察卡 + #30 + #29；2:45 #22 + #20 + #20；3:54 洞察卡 + #10 + #8；4:52 #2 + #1。最短间隔 4:52→5:03 是 11 s，≥10 s |
| 9 | 占位卡措辞不准，样式像没做完 | **部分修复** | 措辞现在如实：Guiyang 写「No identifiable free-licensed photo」；Lotte、LCT、Marina 101、Princess 写「No usable photo: architecture copyright」；5 张 RISK 图写「Photo withheld: architecture copyright」。样式改成「国旗 + 楼形图标 + 渐变底」，比通用灰卡好。<br>问题是说明文字为白字压在米色渐变底上，实测对比度约 **1.24:1**，1280 宽下勉强能认，手机上看不清（见 N1）。Guiyang 没有补真实照片，改为如实说明，可以接受 |
| 10 | 竖图只占卡中间约 40%，两侧模糊；#33、#45 构图 | **未修复（minor）** | 接触表和抽查帧里，竖图仍是中间一条，两侧模糊填充（例如 #7 One World Trade Center，帧 258 s）。#33 JPMorganChase 仍是夜景，#45 CMB 仍是原图。不阻塞发布，可以留到系列模板统一处理 |
| 11 | 片头标题淡出后约 0.5 s 近乎全黑 | **已修复** | 逐帧亮度：标题在 3.0–3.55 s 淡出，约 3.6 s 卡片开始进场。只有约 0.05–0.1 s 是空背景，而且背景本来就是藏青色，不是黑场。3.0–5.0 s 每 0.25 s 一帧逐张看过，没有任何一帧出现标题和卡片叠加。顶栏和计分板在 3.75–4.25 s 淡入 |
| 12 | 署名带「User:」前缀；#1 作者写法 | **已修复** | `publish.md`、`data.json`、`assets.json` 里都没有「User:」了。#11 卡上署名为「Sinsyuan / CC BY-SA 4.0」（帧 222 s 局部）。对照版 #1 卡上署名为「ECWiki1 (Eric Chamchoum) / CC BY 4.0」 |

### 发布文案核对（默认母版）

- 字数：描述 3,126 字符（≤5,000），置顶评论 1 为 7,541 字符，评论 2 为 8,150 字符（都 ≤10,000）。三段都没有 `<` `>`。
- 署名和画面一一对应：
  - 描述和评论 1 都是 40 条署名，等于 50 座楼减去 5 座本来无图（#6、#31、#37、#40、#43）、再减去 5 座 RISK 占位（#1、#17、#38、#44、#47）。
  - 被撤下的 5 张图在描述和评论 1 里都**没有**署名，这是对的。
  - 片中显示的 40 张照片都有署名（逐条对过名次）。
  - 评论 2 是逐条数据出处，50 座全列，这是对的，因为数据仍在片中。

### 新发现

1. **N1 · major（上传前修）· 全部 10 张占位卡，包括 4:56–5:02 的冠军卡 · 说明文字几乎看不见**
   - 问题：占位卡底部的说明（「Photo withheld: architecture copyright」等）是白字，压在渐变底最浅的米色上（约 RGB 246,225,192），对比度约 1.24:1。在 1280 宽下要凑近才能读，在 640×360 手机尺寸下看不清。
   - 影响：默认母版有 10 张占位卡（占 20%），其中 #1 冠军、#6、#17 在前 20 名。观众读不到原因，只会看到一张「国旗 + 图标」的空卡，容易理解成「没找到图」。上轮第 9 条要「如实说明原因」，这个目的因此没有达到。
   - 建议：说明文字改成深色字，例如卡上正文的深藏青色；或者在文字下面加一条半透明深色底带。字号放大到和城市名相当。ep02 的 #32 占位卡用的是同一个渲染器，同样要改。
2. **N2 · 交人 / 流程 · `publish.md` 只对应默认母版**
   - 问题：`publish.md` 的署名不含 5 张 RISK 图。人如果选择上传对照版，必须先用对应的参数重新生成 `publish.md`，补上 #1 ECWiki1 (Eric Chamchoum)、#17、#38、#44、#47 的署名和许可链接，否则 CC BY / BY-SA 的署名义务不满足。
   - 建议：在 Upload checklist 里加一行说明这一点。
3. **N3 · nit · 评论 2 仍写「CTBUH Skyscraper Center」**（见第 6 条）。
4. **N4 · nit · 计分板版面**：11 国全部显示后，整块内容偏上，下方约 10% 留空。可以接受。

没有发现新的数据错误、错旗、出框、冻帧或闪烁。滚动速度和上轮一样，都是 2 px/帧。

### 回归抽查

- 接触表 7 张（每 3 s 一帧）看过全片约 110 帧，加上关键帧 20 张。
- 50 张名次卡依次出现，没有漏卡或重复。角落计分板逐步累加，没有问题：例如帧 36 s 时 CN 6、EG 1、AE 1；帧 258 s 时 CN 24、US 8、MY 3、AE 3、KR 2；冠军段时 CN 26、US 8、AE 4、MY 4、KR 2。
- 5 张洞察卡的文字和上轮一致。来源卡写「Data: Skyscraper Center (CVU, ex-CTBUH), Wikidata (CC0) / Completed buildings, Nov 2026 / Photo credits: shown on each card and listed in the description / Flags · Icons · Font」。
- 片尾 313–331 s 只有顶部的「Thanks for watching!」，下方空着，可以放片尾元素。

### 未能检查

- 音乐和混音（§7.6）：片子仍是静音，配乐后要再审。
- 对照版只抽了 5 帧，用来确认 RISK 图出现了，没有全片审。对照版没有对应的发布文案。
- 没有重新做外部数据核对。数据值和上轮相比没有改动（`data.json` 只多了展示字段，名次和数值不变，画面逐卡对过）。

## 结论（第 2 轮，默认母版）：**修后可发布**

- 上轮的 major #2、#3 已修复；minor #5、#7、#8、#11、#12 已修复；#6 已修复，评论 2 留一处 nit。
- #1 和 #4 交人决定：默认母版把 RISK 图全部撤下，版权风险已经消除，代价是冠军段没有照片。
- #9 部分修复，#10 未修复（minor，不阻塞）。
- 上传前必须做两件事：
  1. 修 N1：提高占位卡说明文字的对比度，然后重渲。这一条主要影响冠军卡。
  2. 人在 `sources.md` 记下 RISK 图的决定，也就是选默认版还是对照版。选对照版就要重新生成 `publish.md`（N2），并且最好换掉那张冠军图。
- 做完这两件事，静音画面版就可以发布。**音乐仍待制作**，配乐后要再审一次音频。

## 第 3 轮复核（fresh-context 子代理，2026-11-03）

范围：渲染器修复后，只复核 N1 和 N3（CVU 命名），另做小范围回归抽查。被审文件的 sha256 与 manifest 一致：默认母版 `6b045df5…`，对照版 `650e335e…`（都是 10:44–10:48 重渲）。

| 项 | 结论 | 证据 |
|---|---|---|
| N1 占位卡说明文字看不清 | **已修复** | 说明文字下面加了深色圆角底条（约 RGB 28,22,15），字是白色（255,255,254）。用 PIL 在 1920×1080 原帧上逐张取色，按 WCAG 公式算，**10 张占位卡的对比度都是 17.9:1**，上轮是约 1.24:1。底条高 38–42 px（1080p）。底条外的卡面渐变也比上轮深（约 RGB 89,71,50），白字放在上面也有 8.9:1。<br>逐张看过的帧（1280 宽和 640×360 各看一次）：#47 23 Marina（21 s）、#44 Iconic Tower 与 #43 Guiyang IFC T1（36 s）、#40 LCT（60 s）、#38 Al Hamra 与 #37 Princess Tower（69 s）、#31 Marina 101（110 s）、#17 Landmark 81（186 s）、#6 Lotte World Tower（255 s）、#1 Burj Khalifa（299 s）。<br>在 640×360 下，「Photo withheld: architecture copyright」「No usable photo: architecture copyright」「No identifiable free-licensed photo」都能读出来。各卡的措辞和 `data.json` 一致 |
| N3 评论 2 仍写「CTBUH Skyscraper Center」 | **已修复** | `grep -c "CTBUH Skyscraper Center" publish.md` = **0**。评论 2 的 50 条出处都改成「Skyscraper Center (CVU, formerly CTBUH), 100 Tallest Completed Buildings…」，描述里写「Skyscraper Center (CVU, ex-CTBUH)」，两处说法一致 |
| 发布文案字数 | **通过** | 描述 3,126 字符（≤5,000），评论 1 为 7,541 字符，评论 2 为 8,950 字符（都 ≤10,000，评论 2 因为改名多了约 800 字符）。三段都没有 `<` `>` |

### 回归抽查

- **默认母版 6 帧**（2、97、163、231、304、311 s）：片头、#34–#31 滚动段、#22–#20 段、洞察卡加 #10 CITIC、计分板（11 国，合计 50）、来源卡，都正常。没有出框、错旗、重叠或错值。
- **对照版 3 帧**（21、186、299 s）：#47 23 Marina、#17 Landmark 81、#1 Burj Khalifa 显示的是原 RISK 照片，署名分别为 BS2024、Joefrance1995、ECWiki1 (Eric Chamchoum)。冠军卡仍是那张雾霾逆光图，没有变化。

### 新发现

- **nit**：说明文字的字号没有放大，1080p 下字高约 18 px。上轮建议「放大到和城市名相当」，这一条没做。现在对比度已经够，在 640×360 下也能读，所以不阻塞。
- N2（`publish.md` 只对应默认母版）仍然成立。Upload checklist 里还没有写「选对照版要重新生成 publish.md」，这一条交人决定。

### 未能检查

- 音乐和混音：片子仍是静音。
- 对照版只抽了 3 帧，不是全片审。

## 结论（第 3 轮，默认母版）：**可发布（静音画面版）**

- 第 2 轮要求上传前修的 N1 已修复，对比度从约 1.24:1 提高到 17.9:1。N3 已修复。重渲没有引入回归。
- 上传前还剩一件事：人在 `sources.md` 记下 RISK 图的决定，也就是选默认版还是对照版。选对照版要重新生成 `publish.md`（N2），并且最好换掉冠军图。
- **音乐仍待制作**，配乐后要再审一次音频。

## 第 4 轮：版式 v0.2（满版照片卡）独立审片（fresh-context 子代理，2026-11-03，follow-up 004）

背景：用户反馈「图片占比太少」，要求优先级为照片 > 国旗 > 关键数值。渲染器升到 rank_scroll 0.2.0：照片铺满卡片（600×800），裁切默认保留照片顶部，保住塔尖。

**结论：版式本身达成目标，但本期还不能算可发布。** 50 张卡里有 10 张没有照片，其中包括第 1 名。

- **优先级达成**：照片约占画面 60%（含渐变下可见部分），视线顺序是照片 → 国旗 → 数值。
- **运动**：逐帧测量，匀速 2 px/帧，没有跳帧。
- **前 10 名卡**：放大后不碰页头和进度条。

| 级别 | 发现 | 处理 |
|---|---|---|
| 高 | 冠军 #1 Burj Khalifa 是占位卡（因所在国无全景自由，默认不用照片），高潮段没有画面 | **待用户决定**：用 `_with-risk-images` 版本，或另做「无图英雄卡」（例如和 #2、#3 的高度对比图）。本次未改 |
| 高 | 占位卡集中在开头：#47、#44、#43、#40、#38、#37 都在约 10–75 s 之间，开头 14 张里有 6 张，正好落在留存最关键的段 | 同上 |
| 中 | 占位卡说明有三种写法 | 刻意保留：此前审片要求写真实原因 |
| 中 | #3 Shanghai Tower 塔冠被卡片顶边裁掉，#49 Citymark 顶部被裁 | 原照片本身就裁了顶，焦点已设到最上；需换图 |
| 低 | #48、#45 照片发灰、对比度低 | 待换图或调色 |
| 低 | 中日文作者名用的是备用字体，字重偏细 | 不阻塞 |

- **音乐**：同 ep02，Suno 被验证码拦住，没有生成，仍是静音。

## 第 5 轮：全部换图 + Suno 配乐后的独立音画审片（fresh-context 子代理，2026-11-04，follow-up 011 / 021 / 033）

审的是 `render/ep01_tallest_buildings_master_with-risk-images.mp4`（321.6 s）：50 张卡全部换图，加 Suno 两首配乐。
- **画面**：均匀抽帧 127 张，另放大 31 个时间点。
- **音频**：整轨 ebur128（瞬时、短时、真峰值）。

**结论：修后可发布。**

| 级别 | 发现 | 处理（2026-11-04） |
|---|---|---|
| 高 | 本版含 24 张风险图（许可不明 13 张、无全景自由 10 张、保留所有权利 4 张、NC 1 张），署名行能看到 unknown 和 All rights reserved | 不改。按 bible，发布前由用户逐张签字，否则发默认版 |
| 高 | #7 One World Trade Center 尖塔被国旗盖住 | 换成候选 c1（Pexels），尖塔在国旗右侧完整可见 |
| 高 | #3 Shanghai Tower 塔冠藏在国旗后面，整张发灰 | 候选里没有一张同时可商用且塔冠完整，另从 Wikimedia Commons 补图：Melvin Loi，CC BY 4.0，塔居中、塔冠完整 |
| 中 | #15 Central Park Tower、#28、#29、#31、#49 的楼顶被国旗压住，或主体认不出 | 分别换成 c3、c3、c8（One Vanderbilt 与帝国大厦同框）、c3，#49 改用 c3 并把焦点设为 x=0.7 |
| 中 | #8 Guangzhou CTF 塔冠被卡片上沿裁掉 | 换成 c3 夜景，台阶式塔冠完整，焦点 x=0.7 |
| 中 | #19 Changsha IFS 只有立面近景 | 换成 c1：天际线全貌，Pexels 许可 |
| 中 | #45 CMB、#36 Zijin 来源是建筑方宣传图 | 不改。#45 只找到这一张实拍，已在风险清单里，由用户签字 |
| 中 | 接缝 176–180 s 有约 2 s、7.6 LU 的下陷（线性交叉淡化） | 渲染器改用等功率交叉淡化（acrossfade qsin） |
| 中 | 全片最响的一段在 #20 附近，#1 揭晓时反而平 | 两首对调：曲 fd30866d 截 0–160 s 在前；曲 e3d32d23 在后，末尾对齐片尾。它的高潮（原曲 165–176 s）落在视频约 288–300 s，正好是 #1 揭晓之后 |
| 低 | #20、#24、#26、#50、#6 的塔尖贴着国旗或卡片上沿；#18 夜景偏暗 | 不改，能认出 |

**系统性问题（审片员提出）**：国旗固定在左上角，裁切焦点又贴着上沿，所以塔尖常常落在国旗下面。这次逐张选了塔尖避开国旗的图。是否在版式上统一处理，比如检测到塔尖落在国旗区时自动下移，留给后续 follow-up，本次没改渲染器版式。

修后接触表已逐张复核 50 张卡，四个版本重渲中，渲完做第 6 轮复审。

## 第 6 轮：第 5 轮修复后重渲的独立复审（fresh-context 子代理，2026-11-04，follow-up paihangbang 040）

审的是 `render/ep01_tallest_buildings_master_with-risk-images.mp4`（321.6 s），sha256 与 manifest 一致。逐卡抽帧加放大图；用 ebur128、频谱和接缝测量查音频。

**结论：可发布。前提是用户对 24 张风险图逐张签字，否则发默认版。**

第 5 轮修复已生效：
- **画面**：#3、#7、#15、#49 的塔尖都在国旗右侧，#8 的塔冠完整。
- **接缝**：下陷从 7.6 LU 降到约 1.7 LU。
- **高潮**：#1 揭晓前约 2 s 的音乐空拍在 286.5 s 落下重拍，291–300 s 是全片最响的一段（S -13.7 到 -12.7）。

其他核实结果：
- 名次、数值和洞察都与 data.json 一致。
- 滚动没有跳帧。
- 响度 -16.0 LUFS，真峰值 -3.5 dBTP，没有削波。

| 级别 | 发现 | 处理 |
|---|---|---|
| 流程 | 24 张风险图需要用户签字 | 待用户签字 |
| 低 | #33 JPMorganChase 楼顶左侧约 1/4 压在国旗下面 | 不改，留给版式级修复（国旗与上沿的系统性问题） |
| 低 | #50 首卡楼顶贴卡片上沿，左侧碰到国旗 | 同上 |
| 低 | #48 CITIC Plaza 塔尖顶到上沿 | 同上 |
| 低 | #26 KK100 塔冠被上沿切掉（第 5 轮已判不改） | 不改 |
| 低 | #31 Marina 101 是楼群远景，单栋不易认 | 不改（候选里没有更好的可用图） |
