# ep04 · 独立审片记录（qc.md）

> 2026-11-03 独立审片（fresh context，未参与制作）。审的是 `data.json` / `sources.md` / `assets.json` / `assets/img/` 的当前版本，以及 `projects/rank_scroll` 按当前数据出的预览单帧（`render/preview/t*.png`，风险版在 `render/preview/risk/`）。`render/` 里旧的 mp4 没有审，音乐（§7-6）也没审，因为配乐还没做。
> 抽查数字用了 WebSearch 和 iNaturalist API，没有调用收费服务。

**总结论：小修后可发布。** 要先清掉 1 个 blocker（第 22 名的图不是 Grévy's 斑马），再处理下面全部 major。改完要重出受影响的帧，再复审一次。这些问题都是数据口径、文案和换图层面的修改，不用重做结构。

---

## Blocker

### B1 第 22 名 Grévy's Zebra 的主图是杂交斑马，不是 Grévy's 斑马
- 证据：`assets/img/gr_vy_s_zebra.jpg`，来源 iNaturalist 观测 226374165。通过 API 查到，这条观测的物种是 **Equus grevyi × quagga（Grévy's × Plains Zebra 杂交）**，研究级，7 个鉴定全部一致，拍摄地 Ol Pejeta（肯尼亚），时间 2024-05-19。看图也对得上：体侧条纹宽，臀部条纹横向弯曲，没有 Grévy's 那种两侧镶白边的宽背线。预览帧 t=58 s、t=66 s 里，这张图配的字幕是「Grévy's Zebra」。
- 影响：卡片写的物种和画面里的动物不一致，懂行的观众一眼就能看出来。
- 改法：换成研究级、`captive=false`、物种为 *Equus grevyi* 的图。iNaturalist 上 Samburu、Laikipia 的 CC BY / CC0 观测很多，也可以去 Unsplash、Pexels 找，先核对鉴定再选。找图脚本要加一条硬性检查：iNat 来源的图，`taxon.name` 必须和卡片物种完全一致（不接受杂交种、近缘种）。

---

## Major

### M1 Gaur（第 10 名）和 African Buffalo（第 15 名）的主值出处是维基百科
- 证据：`sources.md` §2 第 10、15 行写的是「Wikipedia: Gaur (citing Nowak 1999)」和「Wikipedia: African buffalo (citing Melletti & Burton 2014)」，等级 secondary。这违反 bible §3.2 和 BRIEF「维基只作交叉核对」的规定。
- Gaur 的问题最大：1,044 kg 是维基上 588–1,500 kg 的中点，而交叉核对 AWCSG 给的是 440–1,000 kg（−31%）。抽查结果也很分散，各来源的平均值从 650 到 1,300 kg 都有。第 11 名之后那张洞察卡「From here on, every typical adult male weighs more than a tonne」正好压在这个最弱的数字上；第 11 名野牦牛的 1,000 kg 来自 Leslie & Schaller 2009，原文是「>800 kg…as high as 1,000 kg」，更接近上限估计，也不是典型值。
- 改法：Gaur 改用原书（Nowak 1999 Walker's、Melletti & Burton 2014 *Ecology, Evolution and Behaviour of Wild Cattle* 的 gaur 章）或 ASM *Mammalian Species* 里的雄性数值；拿不到原书，就在卡上标 `est.` 并降低措辞。African buffalo 直接引 Melletti & Burton 2014 原书页码（pp. 340–341）。洞察卡建议改成「From here on, a typical adult male weighs about a tonne or more」，或者把 gaur、wild yak 两个数字核实后再保留「more than a tonne」。

### M2 「典型雄性」口径不一致：棕熊按全物种平均，其他多亚种物种按最大或最常见的种群
- 证据：棕熊按物种整体约 200 kg 落选（洞察卡 after 26）。同一份榜里：African Buffalo 775 kg 用的是最大的开普亚种（森林水牛只有 265–320 kg，见 `sources.md` 备注 #15）；Mountain Zebra 298 kg 用的是 Hartmann's 亚种（Cape 亚种 250–260 kg）；Moose 545 kg 用 Toronto Zoo 的北美数值，旗子却插在俄罗斯；Elk 用的是落基山种群。批次 C 原本给棕熊的值是 Katmai 雄性 272–408 kg（中点 340），按「最大种群」的标准，棕熊应排在第 23 名左右。
- 影响：Kodiak 熊、灰熊是「最大陆地食肉动物」争论的固定话题，评论区一定会有人质疑。洞察卡给的理由（物种整体约 200 kg）和其他卡的取值方法不一致，站不住。
- 改法：只选一种规则，全榜照它执行。(a) 全部用「全物种代表值 / 分布最广的种群」，buffalo、moose 等要相应下调并复核名次；或者 (b) 全部用「最大的主要种群」，棕熊用阿拉斯加沿海或 Katmai 的雄性数值进榜。选定后把规则写进 `scope_note`，洞察卡同步改。

### M3 湾鳄洞察卡的理由和收录规则自相矛盾
- 证据：洞察卡 after 22 写「Not ranked: saltwater crocodiles… but they hunt in the water」，t=66 s 的帧里它紧挨着第 21 名北极熊。北极熊在海冰上捕猎海豹，美国法律把它算作海洋哺乳动物；河马白天主要泡在水里。这期还收了一只爬行动物（第 30 名象龟）。说「在水里捕猎所以不算陆地动物」，套到北极熊、河马身上都说不通，观众很容易指出来。
- 改法：两个选择。(a) 承认这是编辑口径，例如「We left out crocodilians: semi-aquatic reptiles that spend most of their lives in water」，同时在 `scope_note` 解释河马、北极熊为什么收（陆上繁殖、休息、行走）；或者 (b) 把湾鳄收进榜（约 460 kg，大约排第 22 名），把这张洞察卡换掉。不管选哪种，都不要再用「hunt in the water」作理由。

### M4 漏了野生双峰驼，屏上和描述框都没有解释
- 证据：*Camelus ferus* 是 IUCN 认可的现存野生物种（批次 B 记的类别是 EN 2025 或 CR，约 950 头，分布在中国和蒙古）。`sources.md` §3 以「查不到野生个体的雄性体重」为由没排它。抽查结果：所有来源都没有区分野驼和家驼的雄性体重，但常见范围是 450–690 kg（ADW 300–690 kg，SDZ 450–500 kg，DesertUSA 约 450–680 kg）。取其中任何一个值，它都能进前 30，大约在第 19–22 名之间，远超门槛。`scope_note` 和洞察卡都没有提到它。
- 改法：要么用 SDZ 的 450–500 kg 标 `est.` 收进来（卡上写明「wild & domestic data pooled」）；要么在 `scope_note` 加一句「Wild Bactrian camels are left out: no reliable weights exist for wild males」，最好再配一张「Missed the cut」洞察卡。

### M5 片头口径行没写收录和排除规则
- 证据：t=3 s 的片头只有「Average adult male weight · Data as of Nov 2026」，没有说明只收现存野生物种、排除家畜、海兽和鳄类、国旗代表野外数量最多的国家、相差 5% 以内可视为并列。bible §3.4 要求口径差异大的必须在片头口径行写明，但这些内容只出现在 `scope_note`，也就是描述框里。
- 改法：在片头口径行或第二行加一句短的，例如「Living wild species · no domestic, marine or crocodilian species」。同时把「Average」改成「Typical」，见 m1。

### M6 多个「Record ~X kg」标签写的其实不是记录
- 证据：`sources.md`「野外数量与最大记录」表和卡片标签（t=75 s 的北极熊卡能直接看到）：
  - Moose「Record ~725 kg」：是 ADF&G 给的范围上限，原文注明「not a single weighed record」。
  - Elk「Record ~500 kg」：Britannica 原话是「exceptional bulls exceed 500 kg」，原文注明「No individual weighed record found」。
  - Common Eland「Record ~942 kg」：是 Estes 1991 的雄性范围上限，「非单一称重事件」。
  - Muskox「Record ~650 kg」：是圈养个体，原文扫描件未核对。
  - Polar Bear「Record ~800 kg」：PBI 写的是「estimated」，不是称重。
  - 象类的 10,400 kg 和 7,000 kg 是按肩高推算的。现在卡片上因为放不下没显示，但数据里还在。
- 改法：只有真正称过重的个体记录才用「Record」。其余改成「Up to ~X kg」，圈养个体写「captive」，推算值写「est.」。

### M7 「Galápagos Giant Tortoise」的名字、数值和数量口径会误导观众
- 证据：第 30 名的学名是 *Chelonoidis porteri*（西圣克鲁斯象龟）。IUCN 现在把加拉帕戈斯象龟拆成约 13 个物种，卡上却用了泛称。标签「~3,400 in the wild」只是 porteri 一个物种的数量，观众会以为整个加拉帕戈斯只剩 3,400 只（实际合计约 2.5–2.7 万）。295 kg 取自 SF Zoo 272–318 kg 的中点，来源是动物园页面（secondary）。`sources.md` 备注 #30 也写了「no source definitively names the single largest species」，选 porteri 有点随意。
- 改法：卡名改成「Western Santa Cruz Giant Tortoise」（或「Santa Cruz Giant Tortoise」），副标题写「Galápagos」。数量标签写成「~3,400 (this species)」。另外在 `sources.md` 说明为什么选它（和 *C. vandenburghi* 等候选物种比较）。

### M8 非洲森林象排在两种犀牛后面，差异 +125% 还没有人拍板
- 证据：第 5 名 2,000 kg 来自 Larramendi 2016（同行评审，按肩高推算），交叉核对 Owen-Smith 2024 给的是 4,500 kg（+125%），Grubb et al. 2000（经维基转引）给的是公牛 4–7 t。按 bible §3.4，差异超过 10% 的「由人决定」，但 `topic.md` 至今是「待用户点头」，屏上（t=190 s）也没有任何说明。很多观众记得的是维基的「2.7–6 t」，看到森林象比印度犀、白犀还轻，会认为数据错了。
- 改法：请用户确认继续用 Larramendi。然后二选一：把备选洞察换成一张讲这件事的卡，例如「No forest elephant has ever been weighed; estimates range from 2 to 4.5 tonnes」；或者至少在描述框里写明。

### M9 第 7 名爪哇犀的默认版替代图裁切差，画面里还有人的影子（默认母版就会发布这张）
- 证据：t=172 s 的默认版。`06_javan_rhinoceros_alt.jpg` 是隔着玻璃拍的博物馆标本，卡上只露出头顶和耳朵，眼睛和吻部被文字遮住，看不到角。右侧玻璃上有一个半透明的人形反光，能看清是拍照的人。
- 改法：把 `image_focus` 调到头部和角能完整露出来，例如 `[0.6, 0.75]`，并确认人影被裁掉。裁不掉就换一张标本照片，或换成 USFWS、IRF 等机构的公有领域图。实在没有，按 follow-up 032 交 Codex 生成，并标 AI。

### M10 爪哇犀风险版主图是带水印和机构 logo 的新闻图
- 证据：`assets/img/javan_rhinoceros.jpg` 的原图左下角有「© Robin Moore/GWC」，右下角有国家公园、林业部、WWF 等 4 个 logo（见 `_build` 拼图和原图）。风险版 t=172 s 的帧里，水印被裁掉了，但 logo 条的边缘还露在「2,900 lb」右侧。署名行显示的是「… / unknown」。bible §4 规定带水印的候选图直接排除。另外这张图实际上是版权所有（©），不只是「许可不明」。
- 改法：风险版不要用这张图，或者裁切时完全避开 logo 条，并把 `assets.json` 的 licence 改成「© all rights reserved (press image)」，交给用户签字。屏上署名不要出现「unknown」这个词。

---

## Minor

- m1 指标名写的是「Average adult male weight」，但有 13 个值是范围中点（`kind = range midpoint`）。建议改成「Typical adult male weight」，`scope_note` 已经这样写了。
- m2 Kiang 345 kg 用的是 ADW 雌雄合并范围 250–440 kg 的中点。雄性专属数据是 350–400 kg（维基、吉尼斯），中点 375。名次不变，但按「雄性」口径应该用 375，或者在卡上标明是合并数据。
- m3 第 27–31 名边界很软：Bongo 300（Britannica）、Mountain Zebra 298、Plains Zebra 297（SDZ 220–373 的中点；维基是 220–322，中点 271，按它会掉出榜）、象龟 295、马来貘 285（只有维基来源，而且雌性更大）。「相差 5% 以内视为并列」现在只写在描述框里，建议在第 30 名之后那张洞察卡或片头也提一句。
- m4 国旗可信度低的几项：European Bison 旗子是波兰，但按自由放养数量，白俄罗斯可能更多（EBPB 总数三国相差不到 5%，而且含圈养个体）；Giraffe 旗子是肯尼亚（KE 2021、ZA 2025、TZ 年份不明，数据年份不统一）；Bongo 旗子是加蓬（完全没有分国数据）。建议在描述框列出「flag confidence: low」的物种，避免这几个国家的观众来纠正。
- m5 爪哇犀卡上写「Most in Indonesia」，但它只分布在印度尼西亚（全部在 Ujung Kulon）。建议改成「Only in Indonesia」。苏门答腊犀同理，可以写「Almost all in Indonesia」。
- m6 Mountain Zebra 的图是 Cape 亚种（橘色吻部，南非特有），而数值 298 kg 和国旗（纳米比亚）对应的是 Hartmann's 亚种。可以换一张 Hartmann's 的图，或者至少在 `sources.md` 写清楚。
- m7 Bongo 的图来自 iNat 观测 218180159，标注 `captive=True`，拍摄地在美国，是动物园里的山地邦戈（树干上有人工管道），与 `layout.image_prefer`「wild animal」要求不符。Takin 的图只有 1152 px 宽，满版卡上是放大显示（t=40 s 看得出发软），而且动物是卧姿、占画面比例小。建议有余力时换掉这两张。
- m8 Wild Yak 默认版的替代图是博物馆布景（t=140 s，署名注明了 museum diorama），已有用户特许（follow-up 030），可以保留。但「野生动物排行榜」里出现两张标本图会显得廉价，建议后续继续找野外实拍图。
- m9 高棉牛洞察卡：「~750 kg」是雌雄合并范围的中点（ADW 681–910 kg），按雄性口径会更高，可能排在第 15 名之前。「confirmed alive since 1969」和 AWCSG 的说法冲突（AWCSG 写的是「no confirmed sightings since 1983」，IUCN 原文写最后正式记录是 1963/64）。建议改成「would rank around here」和「not confirmed alive in decades」。
- m10 来源卡和片头的来源行只写了「IUCN Red List, peer-reviewed studies, zoo & park data」，没有反映实际也用了百科和汇编站点（Britannica、EOL、animalinfo.org、Ultimate Ungulate、维基转引）。建议改成「…zoo, park & reference works」，或在来源卡点出 2–3 个主要来源（Larramendi 2016、Owen-Smith 2024、IUCN SSC 专家组）。
- m11 数量标签有几个比较旧：Wild Water Buffalo ~3,400 是 2010 年 WTI 的数据；Asian Elephant ~50,000 用的是印度 2017 年数据，印度 2025 年 DNA 普查只有 22,446 头。建议注明年份，或改成「<4,000」「~40,000–50,000」。
- m12 文件命名不符合数据契约「NN_<slug>.jpg」：主图都没有名次前缀；两张替代图的前缀 `06_`、`10_` 是旧名次，现在实际是第 7、11 名。建议统一重命名（同步改 data.json 和 assets.json 的 sha 与路径）。
- m13 Banteng 的许可只写了「CC BY」，没有版本号（licence_url 默认填了 4.0）。iNat 照片页对脚本返回 403，没能核实，建议到原页确认版本。
- m14 giraffe 洞察卡「IUCN Red List still lists just one」目前成立：抽查确认专家组 2025-08 认定 4 种，红色名录按 4 种重新评估计划在 2026 年完成，但还没查到已经发布。发布前 7 天要复核；一旦红色名录改成 4 种，按本片「按 IUCN 现行分类」的口径，长颈鹿这张卡本身也要改。
- m15 片长约 4:13（timeline 253.43 s），短于 bible 建议的 5–8 分钟。`topic.md` 已说明 Top 30 是用户定的，这里只记录，不作为问题。

---

## 核过且通过的项

- **名次与排序**：30 条 rank 1–30 连续、无重复，按 `value` 降序，与 data.json 一致；6 张洞察卡的 `after_rank` 位置与倒数顺序相符（例如高棉牛卡在第 16 名 700 kg 和第 15 名 775 kg 之间，t=110 s）。
- **取整与换算**：30 条 kg 显示值（1,000 kg 以上取整到 50 kg）和 lb 副显示（×2.20462，2,000 lb 以上取整到 100 lb，以下取整到 10 lb）逐条复算，全部正确。
- **差异超过 10% 的交叉核对**：森林象、爪哇犀、gaur、野牦牛、野牛、欧洲野牛、普通大羚羊、驼鹿、扭角羚、麝牛都已在 `sources.md` 备注写明。处理是否恰当见 M1、M8。
- **抽查的关键数字**：Bongo 300 kg 与 Britannica「males weigh on average 300 kg」一致；Grévy's 430 kg 与 animalinfo「avg 430 kg」一致，ADW 是 349–451 kg；Kiang 见 m2；Gaur 见 M1；野双峰驼见 M4；冠军 6,000 kg 与 Larramendi 2016 的公牛均值一致（交叉核对 +8%）；长颈鹿 1,192 kg 是 Skinner 系列的经典雄性均值。
- **IUCN 徽章**：banteng CR 已确认（2024-10-28 由 EN 升级）；giant eland VU 与 MDD 和维基一致；American bison 目前仍是 NT，没有查到已发布的重新评估。LC 物种不显示徽章，全榜执行一致。
- **大洲计分板**：Africa 13 / Asia 10 / North America 4 / Europe 2 / South America 1，与逐条 M49 映射一致；滚动中间的累计数在 t=40、75、110、140、172、190、222 s 逐帧核对，全部正确；揭晓帧（t=228 s）正确。
- **国旗与国家**：30 张卡的国旗图案和「MOST IN …」国名一致（印度、中国、印尼、南非、坦桑尼亚、加拿大等都核对过），飘动正常。
- **物种辨认**（除 B1 外）：家牦牛和野牦牛（风险版是青海野牛沟的野牦牛，灰吻、全身深色、没有白斑）；家水牛和野水牛（iNat 研究级，阿萨姆，`captive=false`）；印度犀和爪哇犀（第 4 名有明显的铠甲状皮褶，是 Kaziranga 一带的印度犀；第 7 名单角、鳞状纹皮，是爪哇犀）；平原斑马、山斑马、细纹斑马（第 29 名有影纹，背景是角马群，是平原斑马；第 28 名有喉垂和橘色吻，是山斑马）；普通大羚羊和巨羚（第 17 名黑颈白纹，iNat 鉴定为西部巨羚，塞内加尔；第 19 名是普通大羚羊）；白犀和黑犀（第 3 名方唇、头低垂；第 9 名尖唇、在灌丛里）；森林象和草原象（第 5 名是 iNat 研究级 *L. cyclotis*，加蓬，椭圆耳、直向下的牙；第 1 名扇形大耳，在草原上）。
- **许可**：32 个账本条目的 sha256 与文件全部吻合；许可都在可接受名单内（Pexels、Unsplash、CC BY、CC BY-SA、CC0、PD）。两张「unknown」都已标 `image_risk`，并配了可接受许可的 `image_alt`；没有出现不在账本里的图。
- **画面**：t=3、12、20、40、58、66、75、110、140、150、172、190、222、228、232、240 s 共 16 帧，没有文字出框或重叠；手机全屏下名称（约 44 px）和数值（约 80 px）醒目，3 秒内看得清；徽章、名次药丸、署名行位置正确；前 10 名放大、冠军光晕和右侧 No. 1 面板正常；来源卡和片尾干净。

## 审片中出的帧

- 默认版：`render/preview/t0003.00.png` … `t0240.00.png`（16 帧）
- 风险版（`--allow-risk-images`）：`render/preview/risk/t0140.00.png`、`t0172.00.png`

## 抽查用到的外部页面

- iNaturalist API：observations 226374165（Grévy's × Plains）、218180159（bongo, captive）、92834495、332731789、136413128、207907600、357148953
- Britannica bongo：https://www.britannica.com/print/article/73016
- ADW Equus grevyi：https://animaldiversity.org/accounts/Equus_grevyi
- Wikipedia Kiang / Gaur / Wild Bactrian camel（只作交叉核对）
- 长颈鹿 4 种：https://www.the-star.co.ke/news/2025-08-26-giraffes-are-four-species-landmark-study-redefines-worlds-tallest-mammal 、CMS COP15 Doc.31.2.5
- Banteng CR：https://www.asianwildcattle.org/news.html 、https://thestar.com.my/aseanplus/aseanplus-news/2024/12/10/cambodia-houses-largest-population-of-critically-endangered-forest-giants
- 双峰驼体重：https://ielc.libguides.com/sdzg/factsheets/extantcamels/summary 、https://www.desertusa.com/animals/bactrian-camel.html

---

## 复审（第 2 轮，2026-11-04）

> 独立复审（fresh context，没有参与制作）。审的是当前版本的 `data.json`、`sources.md`、`topic.md`、`assets.json`、`assets/img/`、`publish.md`，以及按当前数据出的预览帧。
> 默认版预览帧在 `render/preview/r2/`，共 44 帧：t = 3、4.4、5.4、6、11.33、17.67、24、30.33、35.83、41.33、47.67、54、60.33、65.83、71.33、77.67、84、90.33、96.67、103、106.2、109.33、114.83、120.33、126.67、133、139.33、144.83、150.57、157.37、164.17、169.9、175.63、182.43、189.23、196.03、202.83、209.63、216.43、221、228、233、240、250 s。取点用 `rank_scroll.timeline` 算出的每张卡居中时刻，30 张卡、6 张洞察卡、冠军段、计分板、来源卡、片尾都覆盖到了。风险版在 `render/preview/r2_risk/`（t = 150.57、175.63、233 s）。
> `render/` 下的 mp4 和配乐没审（mp4 可能正在重渲，配乐 §7-6 不在本轮范围）。外部只查了 iNaturalist API 和 Plazi（HMW 原文），没有调用收费服务。

**总结论：小修后可发布。** B1 已解决：新 Grévy's 斑马经 API 核实是纯种，物种正确。30 张主图逐张看过，物种都对。数值、名次、洞察卡位置、计分板都正确。

发布前还要处理 6 个 major：
- R-M9：默认版爪哇犀的替代图问题没解决。
- N1：`publish.md` 过期。
- N2：gaur 用的是两性合并值。
- N3：森林象「none weighed」标签在屏上看不到。
- N4：河马卡切头。
- N5：第 30 名可读时间不足。

这些都是改数据、改焦点、重新生成，不用改结构。改完重出受影响的帧，抽查即可，不用第 3 轮全审。

### 逐条核对

| 编号 | 结论 | 证据 |
|---|---|---|
| **B1** Grévy's 图是杂交种 | **已解决** | 新图来自 iNat 观测 390638213：`taxon = Equus grevyi`（种级），研究级，6/6 鉴定一致，`captive = false`，肯尼亚，2026-08-07，照片许可 cc-by。看图也对：窄而密的条纹、白腹、圆大耳。t = 54、60.33 s 的卡上头部完整，署名「Daniel Benák / CC BY 4.0」。 |
| **M1** gaur 和非洲水牛的主值出自维基 | **部分解决** | 两条都改引 HMW vol. 2（Plazi），我核对了原文。非洲水牛写的是「500–900 kg (males)」，中点 700，没问题。**gaur 原文是「weight 650–1000 kg」，没有分性别**（`build.py` 自己也注明了「sexes not separated」），中点 825 是两性混合值，却放在「typical adult male」的榜里，和其他物种用的雄性值不可比，见 N2。洞察卡已改成「a tonne or more」，和第 10 名野牦牛 1,000 kg 起的数据一致，措辞成立；野牦牛 1,000 kg 仍是 Leslie & Schaller「as high as」的上限值，却标成 `typical`，这条残留降为 minor。 |
| **M2** 「典型雄性」口径不一致 | **部分解决** | 棕熊已按 SDZ 的雄性全分布范围 130–550 kg 取中点 340，排第 24 名。原问题的核心（棕熊被不公平排除）已消除。但 Moose 仍用 Toronto Zoo「American Moose」的北美值 545，旗子却插在俄罗斯；gaur 和 kiang 用两性合并值。规则没有全榜执行。另外 `sources.md` §1 写的「凡出处只给雄性体重范围的，一律取全物种范围中点」读不通，建议改成「取该物种雄性全分布范围（非最大种群）的中点」。名次影响小，残留为 minor。 |
| **M3** 湾鳄的理由自相矛盾 | **部分解决（可接受）** | t = 65.83 s 的洞察卡现在是「…but we count crocodiles as aquatic.」，明确说是本片口径，不再拿「hunt in the water」当理由。约 460 kg 夹在第 22 名 430 和第 21 名 475 之间，位置正确。`scope_note` 写了「Hippos and polar bears are included」，但没说为什么收。建议补半句「(they breed and rest on land)」，作为 minor 处理。 |
| **M4** 漏了野生双峰驼 | **已解决** | `scope_note` 和 `sources.md` §3 都写明了不排的原因。屏上没有专门的卡，按原建议这一条可选，不强求。 |
| **M5** 片头口径行 | **部分解决（可接受）** | 片头和顶栏写的是「Typical adult male weight · wild species only · Data as of Nov 2026」，t = 3 s 一行放得下，t = 6 s 起的顶栏也不溢出。海兽和鳄类的排除没写进片头，但湾鳄卡说明了鳄类，海兽本来就不属于陆地动物，可以接受。 |
| **M6** 「Record」标签 | **已解决（附一处残留）** | 所有标签都改成了「Up to ~X kg」，`sources.md` §1 说明了含义。残留：棕熊的「Up to ~751 kg」只出自维基和二手页面（1894 年射杀个体，未核实），违反维基只作交叉核对的规定。这个标签目前因宽度不够没有上屏，见 N3，但数据和描述里还在。建议改成 ADF&G 的 Kodiak 雄性上限「up to ~680 kg (1,500 lb)」，或者删掉。 |
| **M7** 象龟的名称和数量口径 | **已失效 / 转为 minor** | 按新口径，象龟 295 kg 掉到第 31 名，不再有卡。after 26 的洞察卡写「the Galápagos giant tortoise, at about 295 kg」，仍是泛称，但只是一句话，可以接受。建议写成「a Galápagos giant tortoise species」，或者用「Santa Cruz giant tortoise」。 |
| **M8** 森林象 +125% 差异 | **未解决** | ① `topic.md` 仍是「待用户点头」，没有用户确认，也没有按 AUTONOMOUS 授权写下判断记录。② 新加的「Estimate: none weighed」标签**在屏上看不到**：t = 189.23 s 的卡只显示「~136,000 in the wild」，原因见 N3。③ 描述框里也没写（`publish.md` 过期，见 N1）。 |
| **M9** 默认版爪哇犀替代图 | **未解决** | 图没换，焦点改成了 `[0.4, 0.5]`。t = 175.63 s 默认版的卡上，**右侧玻璃里拿相机的拍摄者人影仍然清楚**（局部放大见本轮截图）；眼睛被「ONLY IN INDONESIA」压住；这个标本没有角，观众很难认出是犀牛的哪一种。默认母版会发布这一版。 |
| **M10** 风险版爪哇犀带水印和 logo | **大部分解决** | 新图换成 WWF 的 Stephen Belcher 野外照。我看了原图全幅，没有水印，也没有 logo。风险版 t = 175.63 s 画面干净，单角、皮肤鳞纹，物种正确。残留：① 屏上署名还是「Stephen Belcher Photography / WWF / unknown」，原意见要求不出现「unknown」；② 源文件名带「©」，`assets.json` 的 licence 应写「© Stephen Belcher / WWF, all rights reserved」，而不是「unknown」，签字时要按版权所有的图对待。这两点是 minor。 |
| m1 Average → Typical | 已解决 | 片头、顶栏和 `scope_note` 都已改。 |
| m2 Kiang 用两性合并值 | 未处理 | 仍是 ADW 250–440 的中点 345，名次不受影响。 |
| m3 5% 并列规则只在描述框 | 未处理 | 屏上没有提。第 28–31 名 300 / 298 / 297 / 295 kg 差距不到 2%，建议在 after 26 的象龟卡加一句「(within 2% of #28–30)」。 |
| m4 低可信度国旗 | 部分处理 | `topic.md` 列出了 5 个，但描述框（`publish.md`）没有。 |
| m5 Only in Indonesia | 已解决 | 爪哇犀和苏门答腊犀都写「Only in Indonesia」。马来西亚的苏门答腊犀已野外灭绝，「Only」站得住。 |
| m6 山斑马的图和亚种 | 已解决 | 新图 iNat 70213082 是 *E. zebra hartmannae*，研究级，野外，纳米比亚，与 298 kg 和纳米比亚国旗一致。焦点 `[0.0, 0.5]` 下头和颈完整，t = 11.33 s。 |
| m7 Bongo 圈养 / Takin 发软 | 未处理 | 和上轮一样。 |
| m9 高棉牛措辞 | 已解决 | t = 114.83 s 的卡是「…would rank near here, but none has been confirmed alive in decades.」，约 750 kg 夹在第 15 名 700 和第 14 名 800 之间，位置正确。 |
| m10 来源行 | 已解决 | 改成「…zoo & reference works」，t = 3 s 片头和 t = 233 s 来源卡一致。 |
| m11 旧的数量数据 | 已解决 | 野水牛「<4,000」，亚洲象「<50,000」。 |
| m12 文件命名 | 已解决 | 32 个文件都是 `NN_slug.jpg`，并列的两张都是 `15_`，替代图和名次一致。32 个账本条目的 sha256 全部吻合，没有账本外的图。（`22_gr_vy_s_zebra.jpg` 这个 slug 不好看，不影响使用。） |
| m13 Banteng 许可版本 | 未核实 | 账本已写「CC BY 4.0」，但没有注明怎么核实的。我用 iNat API 按 photo_id 查不到对应观测，发布前请在原页确认。 |
| m14 长颈鹿 4 种 | 待发布前复核 | 洞察卡文字没变，t = 169.9 s，after 8 紧跟第 8 名长颈鹿，位置正确。 |
| m15 片长 | 记录 | 253.43 s。 |

**本轮重新核过、通过的项**
- 名次：1–14、15、15、17–30。并列按标准竞赛排名处理，跳过 16，`data_contract` 允许同值同名次。t = 106.2 s 两张卡都显示「#15」，前一张是 #17、后一张是 #14，读得懂。
- 30 条 kg 和 lb 的显示值按规则逐条复算，全部正确；`value` 严格降序。
- 6 张洞察卡的 `after_rank` 位置（倒数顺序里在该名次之后）：after 30（国旗规则）、after 26（象龟，第 31 名）、after 22（湾鳄约 460，在 430 和 475 之间）、after 15（高棉牛约 750，在 700 和 800 之间，排在两张 #15 都出现之后）、after 11（之后的第 10–1 名都 ≥ 1,000 kg，第 11 名是 950）、after 8（长颈鹿），数值上全部正确。6 条都 ≤ 90 字符。
- 计分板：滚动中各帧累计都和已入画的卡一致。揭晓帧 t = 228 s 是 Africa 13 / Asia 10 / North America 4 / Europe 3，与逐条 M49 一致（俄罗斯算 Europe，所以棕熊和驼鹿记 Europe）。South America 随象龟出榜而消失，正确。
- 30 张主图物种逐张核对（拼图 `assets/img` 全量）：新棕熊（iNat 223421173，*U. a. beringianus*，堪察加，野外，研究级，照片 cc-by）、新山斑马、新 Grévy's 都对，其余 27 张和上轮一致。
- 文字：44 帧里没有文字出框或重叠。最长的名称「African Forest Elephant」「Sumatran Rhinoceros」「Wild Water Buffalo」「MOST IN CENTRAL AFRICAN REP.」都在卡内。前 10 名的放大卡下沿高于进度条。冠军光晕和 No. 1 面板正常。来源卡和片尾干净。

### 新问题

**Blocker：无。**

**Major**

- **N1 `publish.md` 过期，按它上传会署错名、写错数据**（bible §7-7）
  - 证据：`publish.md` 修改时间是 11-03 23:28，早于 `data.json`（11-04 00:02）。内容还是旧榜：#10 Gaur、#16 Banteng、#30 Galápagos Giant Tortoise；#22 Grévy's 署名「ecovore」，链接是**杂交种观测 226374165**；#28 山斑马署名「George Brits」；#7 写「Most in Indonesia」；gaur 和非洲水牛的来源仍是 Wikipedia；第一行是「ranked by average adult male weight」，来源行是「zoo & park data」；章节时间戳和「4.2 分钟」也是旧的。新棕熊、新山斑马、新 Grévy's、新爪哇犀风险图的署名都没有。
  - 建议：重跑 `python -m rank_scroll publish <ep>`，然后补上：M8 的森林象说明、m4 的低可信度国旗、风险版爪哇犀署名（签字后才用）。

- **N2 gaur 825 kg 是两性合并值，在「典型雄性」榜里被低估**
  - 证据：HMW 原文（Plazi 03F507139949FFF2037DFDC2F79AF289）写的是「weight 650–1000 kg」，紧接着说「Males are considerably larger than females」，没有给雄性范围。同一份 HMW 给非洲水牛的是雄性 500–900 kg。gaur 因此从第 10 名掉到第 12 名，排在野水牛（950）之后，而 gaur 常被称为「最大的野牛」（HMW 自己也这么说）。这是评论区最容易挑的一处。
  - 建议：找一个给雄性体重的原始来源（例如 Ahrestani 2018, *Mammalian Species* 50(959) *Bos gaurus*，或 Melletti & Burton 2014 的 gaur 章），按雄性范围中点重排。拿不到的话，至少在卡上或 sources 里标「sexes combined (males larger)」，并承认名次可能偏低。

- **N3 卡片标签宽度放不下时会被静默丢掉：M8 的「Estimate: none weighed」和大部分「Up to」都没上屏**
  - 证据：`projects/rank_scroll/rank_scroll/cards.py` 的 `_info_line` 会从后往前丢掉放不下的部分，不报错。逐帧核对：#1、#2、#5、#6、#13、#19、#20、#24、#27 的第二个标签都没显示，只有 #21 北极熊的「Up to ~800 kg」上了屏（t = 65.83 s）。所以 M8 的屏上说明实际不存在。
  - 建议：森林象把「Estimate: none weighed」放到地点行（例如 subtitle 改成「Central & West Africa · est.」），或者缩短数量标签，或者用一张洞察卡讲这件事（原意见的首选）。另外，渲染器应该在 timeline 或 validate 阶段对被丢掉的标签给警告，这条记到 rank_scroll 的 follow-up。

- **N4 第 6 名河马卡把头切掉了**
  - 证据：t = 182.43 s，河马头在原图横向 86–95% 的位置。按全局焦点 `[0.5, 0.45]` 和 720×800 的卡，横向只能露出 20–80%，所以画面里只剩耳朵，口鼻被裁掉。这是前 10 名的放大卡（上轮漏看了）。
  - 建议：给 #6 加 `image_focus: [1.0, 0.5]`，重出 t ≈ 182 s 的帧确认。

- **N5 第 30 名卡只能看清约 1.5 秒，不满足 §7-5**
  - 证据：第 30 名卡在 t ≈ 4.2 s 滑入到位，5 s 起开始滚动，t = 6 s 时名称已被切成「ains Zebra」（见 `r2/t0004.40`、`t0005.40`、`t0006.00`）。`layout.intro_hold` 现在是 0；`data_contract.md` 规定这个参数就是为了「让倒数第一张卡也能读满 3 秒（bible §7-5）」，建议值 2.5。
  - 建议：`data.json` 的 `layout.intro_hold` 设成 2.5，片长会增加 2.5 s。

- **R-M9（沿用 M9）** 默认版爪哇犀替代图要换。
  - 建议：首选换一张能露出角、没有反光的公有领域或 CC 图；或者把焦点推到 `[0.0, 0.3]` 看能不能完全裁掉人影（这张标本无角的问题仍在）；或者按原意见交给 Codex 生成并标 AI。

**Minor**

- n1 after 26 的象龟卡讲的是「#31」，却放在第 26 和第 25 名之间，观众刚看完 #30–#26。放在 after 30 更顺；也可以把国旗规则卡挪到 after 26，两张对调。
- n2 并列只靠两个「#15」表示。可以考虑在第二张卡的名次药丸旁加「TIE」，或者在高棉牛卡前加一句说明。可选。
- n3 风险版爪哇犀屏上署名还显示「unknown」，licence 字段应写成「© … all rights reserved」，见 M10 残留。
- n4 #25 Elk 的动物在画面里偏小，头部紧贴「MOST IN UNITED STATES」上方（t = 41.33 s）；#12 gaur 的口鼻被名称和数值压住（t = 133 s）。可以通过调焦点改善，不调也能接受。
- n5 `topic.md` 有几处没同步：洞察卡第 5 条还写「在 1 吨以上」（data 是「a tonne or more」）；开头仍是「待用户点头」，没有记下 M8 的判断。
- n6 `sources.md` §1 那句口径规则读不通，见 M2 行。棕熊「Up to ~751 kg」只出自维基，见 M6 行。

### 本轮出的帧
- 默认版：`render/preview/r2/t*.png`（44 帧）
- 风险版：`render/preview/r2_risk/t0150.57.png`、`t0175.63.png`、`t0233.00.png`


## 作者处理记录（第 2 轮复审后，2026-11-04，夜间 AUTONOMOUS，follow-up 039）

| 项 | 处理 |
|---|---|
| M9 爪哇犀默认替代图 | 换成维也纳自然史博物馆标本（Commons「Javanashorn NHM-Wien.jpg」，0Lucky Luke，CC BY-SA 4.0）：正面、角可见、背景为雨林布景，无人影反光；文件 `assets/img/07_javan_rhinoceros_alt.jpg`。仍是标本图，署名注 museum specimen |
| M8 森林象 | 取值依据写进 `topic.md`（Larramendi 2016 唯一给出方法的来源）；「Estimate: none weighed」标签挪到第一位，已上屏（t≈186 s 预览帧核对） |
| N1 publish.md 过期 | 配乐重渲后用 `python -m rank_scroll publish` 重新生成（收尾步骤） |
| N2 gaur 两性合并值 | 改回雄性专属范围 Walker's 588–1500（中点 1,044，经维基读取，tier=secondary），HMW 650–1000 作交叉核对（-21%，已记 notes）；gaur 回到第 10，野牦牛 11、野水牛 12；「一吨」洞察卡改 after #12 |
| N3 第二标签被丢 | 已知限制（渲染器按宽度从后往前丢标签）；关键标签（森林象估计值）已提前；其余被丢的是「Up to ~X kg」，作次要信息接受 |
| N4 河马切头 | `image_focus: [1.0, 0.5]`，预览核对头部完整 |
| N5 第 30 名停留短 | `layout.intro_hold: 2.5` |
| 文件名 | 名次变化后重新按 `NN_<slug>.jpg` 同步（10_gaur、11_wild_yak、12_wild_water_buffalo 等），assets.json 同步 |

## 配乐记录（2026-11-04 夜间 AUTONOMOUS）

- 原任务 `51842da5…`（键 `paihangbang-ep04-savanna-bgm`）提交时 TimeoutError → uncertain；按 skill 用原 job `resume` + `recollect: true` 到库里按带 job 号的标题认领，排队约 1.5 小时后结果仍为 `generation_timeout`「尚未确认两首属于本任务的歌曲」。
- 判断：带唯一 job 号的标题在库里找不到歌曲，视为**确认没生成**，按 skill「确认没生成才另建新键重提」另建 `paihangbang-ep04-savanna-bgm-v2`（job `101bce70…`），prompt 不变。同批 ep11 / ep13 / ep14 会话遇到同样情况也是这么处理的。若日后在 Suno 库里发现原任务的两首歌，属于多花一次积分，不影响成片。

---

## 第 3 轮独立审片（2026-11-04，fresh context）

> 独立复审（fresh context，没有参与制作）。这一轮只看**当前渲染出的成片**，不以作者处理记录为准：`render/ep04_largest_land_animals_master.mp4`（默认母版）、`…_master_with-risk-images.mp4`（风险版）、`…_draft_temp-music.mp4`（临时配乐审片版），以及 `data.json`、`assets.json`、`sources.md`、`publish.md`、`topic.md` 和 `render/thumbnail.png`。
> 一致性：三个 manifest 记录的输入 sha256 与当前 `data.json`、`assets.json` 及全部图片逐一吻合，成片对应的就是当前数据。`python -m rank_scroll validate` 结果为 OK。时间线总长 255.93 s：intro 0–5，scroll 5–220.93（含 `intro_hold` 2.5 s），champion 至 226.93，tally 至 233.93，sources 至 237.93，end 至 255.93。
> 出帧：默认版共 58 张，放在 `render/preview/r3/`。其中 50 张是按 `rank_scroll.timeline` 算出的每张卡居中时刻，加上片头、冠军段、计分板、来源卡和片尾的单帧（960 px 宽）；`grid4s_01–04.png` 是每 4 s 一格的拼图，覆盖全片；另有 Javan、河马、gaur、Elk 4 张原分辨率局部图。风险版出了 6 张，放在 `render/preview/r3_risk/`（t = 50.17、146.5、178.13、222 s，外加 #11、#7 的原分辨率局部图）。
> 外部只查了一次 WebSearch 和一次 WebFetch（Ahrestani 2018 原文，BioOne 没有返回正文），没有调用收费服务。

### 第 2 轮各项核对（按当前文件）

| 项 | 结论 | 证据 |
|---|---|---|
| **M8** 森林象取值 | **基本解决，仍差用户签字** | t = 191.73 s 的 #5 卡上能看到「Estimate: none weighed」，排在第一个标签位，代价是数量标签被挤掉，可以接受。`topic.md` 记下了按 AUTONOMOUS 授权取 Larramendi 的理由。残留：① `topic.md` 开头仍写「待用户点头」，+125% 的差异按 bible §3.4 需要人拍板，至今没有用户确认；② `topic.md` 写「口径与描述框照写」，但 `publish.md` 的描述框里**没有**森林象的说明（见 R3-m1）。 |
| **M9** 默认版爪哇犀替代图 | **已解决** | 新图是 NHM Wien 的标本照（Commons，0Lucky Luke，CC BY-SA 4.0）。t = 178.13 s 原分辨率局部图：正面，眼、吻、角完整，玻璃上只有木柜反光，**没有人影**；署名「(museum specimen)」完整上屏。小残留见 R3-m4。 |
| **N1** publish.md 过期 | **已解决（内容待补）** | `publish.md` 在 02:32 重新生成，晚于数据。30 条署名与 `assets.json` 中默认版用到的 30 张图逐条对应，作者和源页都对；没有过期署名（旧 ecovore / 杂交斑马链接已经没有了）。名次、并列 #15、「typical」口径、来源行、片长 4.3 分钟都是当前数据。章节 0:00 / 1:20 / 2:33 / 3:36 / 3:47 与时间线对得上（#20 卡居中在 80.2 s，#10 在 153.1 s，计分板从 226.9 s 开始），每段都在 10 s 以上。缺的内容见 R3-m1 和 R3-M3。 |
| **N2** gaur 用两性合并值 | **没有按要求解决，主值退回了维基** | 当前 #10 Gaur 1,044 kg 的 `source` 写的是「Nowak 1999, Walker's… (male range, **via Wikipedia**)」，tier = secondary，链接就是 `en.wikipedia.org/wiki/Gaur`，这一行原样出现在 `publish.md` Comment 2。这正是第 1 轮 M1 指出的问题（维基只作交叉核对），见 R3-M1。名次本身：gaur #10 1,050 kg、野牦牛 #11 1,000 kg、野水牛 #12 950 kg，排序和显示值复算都正确。 |
| **N3** 第二标签被静默丢掉 | **按已知限制接受** | 森林象的关键标签已经上屏。逐帧看，#1、#2、#6、#13、#19、#20、#24、#27 的「Up to ~X kg」仍然没有上屏，只有 #21、#25 的显示出来。渲染器对被丢掉的标签仍然不报警告，`validate` 输出 OK，见 R3-m6。 |
| **N4** 河马切头 | **已解决** | t = 184.93 s 原分辨率局部图：`image_focus [1.0, 0.5]` 下头、眼、耳、吻全在卡内，吻部在「kg」右侧，没有被文字压住。 |
| **N5** #30 可读时间 | **已解决** | `intro_hold` = 2.5。#30 平原斑马卡约 4.2 s 滑入到位，静止到 7.5 s，8.3 s 左右才开始出左边，完整可读约 3.5–4 s，满足 §7-5（t = 4.4、5.5、7.5 s）。 |
| gaur / 野牛 / 棕熊的数据改动 | **数值正确，说明文字没同步** | 非洲水牛 700 kg = HMW「500–900 kg (males)」的中点，交叉核对用维基 775（+11%，已记）。与 Banteng 同为 700，按竞赛排名并列 #15，下一名是 #17。t = 105.5、111.83 s 两张卡都显示「#15」，Banteng 在前、Buffalo 在后，紧接着是高棉牛卡，再往后是 #14 苏门答腊犀。棕熊 340 kg = SDZ 雄性 130–550 的中点，交叉核对 NPS Katmai 340，排 #24，t = 50.17 s 卡面正常。但这几条的 `notes`、`sources.md` §1 和 `topic.md` 里还留着旧说法，见 R3-m2。 |
| 洞察卡 | **位置和数值都正确** | after 30（国旗规则，t = 8.3 s）。after 26（象龟 #31，t = 38.33 s）。after 22（湾鳄约 460，在 430 和 475 之间，t = 68.33 s）。after 15（高棉牛约 750，在 700 和 800 之间，t = 117.33 s）。after 12（「a tonne or more」，后面 #11–#1 都 ≥ 1,000 kg，#12 是 950，t = 141 s）。after 8（长颈鹿 4 种，t = 172.4 s）。文字都没有出框。 |
| 显示值 / 名次 | **正确** | 30 条 kg 和 lb 显示值按规则重新算了一遍，全部吻合，`value` 严格降序，名次是 1–15、15、17–30。 |
| 计分板 | **正确** | 揭晓帧 t = 230 s 是 Africa 13 / Asia 10 / North America 4 / Europe 3，与逐条大洲统计一致；滚动途中各帧的累计数都和已入画的卡一致。 |
| 缩略图 | **通过** | `render/thumbnail.png` 1280×720，1.09 MB。#1 6,000 kg / #2 4,000 kg / #3 2,300 kg，国旗为博茨瓦纳、印度、南非，与数据一致，物种也对。 |
| 物种辨认 | **通过** | 30 张默认图逐张看过，物种都对：#7 是标本馆展柜里标注 *Rhinoceros sondaicus* 的标本；#11 是博物馆布景里的野牦牛；#22 是纯种 Grévy's；#29 是 Hartmann's 山斑马。风险版 #7 是 Ujung Kulon 泡水的爪哇犀，单角、鳞纹皮；#11 是灰吻、全身深色的野牦牛。两张都对。 |

### Blocker

无。

### Major

- **R3-M1 gaur（#10）主值出处是维基，违反「维基只作交叉核对」**（`data.json` items[9].source、`sources.md` §2 第 10 行、`publish.md` Comment 2 #10）
  - 证据：1,044 kg 是维基转述 Walker's 雄性 588–1,500 kg 的中点。作者自己在 notes 里写了「未能打开 Walker's 原书核对，建议按 ~1,000 kg 量级谨慎使用」。HMW 交叉核对是 −21%。排序上 gaur 比 #11 野牦牛只多 44 kg，比 #12 野水牛多 94 kg：主值不可靠，它与 #11、#12 的先后、after 12 那张「一吨」洞察卡的成立，都直接受影响。描述框还会公开写出「via Wikipedia」。
  - 改法（任选一种）：
    - (a) 取得 Ahrestani 2018, *Mammalian Species* 50(959):34–50（doi:10.1093/mspecies/sey004）原文，或 Melletti & Burton 2014 的 gaur 章，用里面的雄性数值重算名次。BioOne 本轮没返回正文，可以经机构访问或请用户代取。
    - (b) 拿不到原文就保留 1,044，但改 source 的写法：source 写 Walker's 原书条目（并注明「male range as quoted by Wikipedia; original not seen」）。卡上 gaur 加「est.」标签，并放在第一个标签位（参考森林象的做法，否则会被丢掉）。描述框补一句「Gaur weights vary widely by source (650–1,500 kg)」。
  - 同类问题：#15 Banteng 的「bulls 600–800 kg」也只出自维基（ADW 不分性别），见 R3-m3。

- **R3-M2 #25 Elk 卡看不到动物：鹿身和鹿头全被文字压住**（t ≈ 38.8–48.8 s，居中帧 t = 43.83 s，局部图 `r3/t0043.83_elk_crop_fullres.png`）
  - 证据：原图 2400×1600，鹿位于横向 24–50%、纵向 48–95%。卡片按高度铺满，纵向没有余量，所以 `image_focus` 的 y 值不起作用。上屏后画面主体是雪山和松林，只有鹿角露在「MOST IN UNITED STATES」上方，头和身体都在名称和数值下面。手机上观众看不出这张卡讲的是什么动物。第 2 轮把它记为 minor（n4），本轮按「动物主体被文字遮住」上调为 major。
  - 改法：渲染器不支持缩放，所以要预裁一张衍生图。例如从原图截取 x ≈ 540–1300、y ≈ 700–1550 的区域，让鹿头落在卡片上半部，存为 `25_elk_wapiti.jpg`，同步更新 `assets.json` 的 sha256 和 modified 说明。Unsplash 许可允许裁切。也可以换一张鹿占画面中上部的图。改完重出 t ≈ 44 s 的帧确认。
  - 同类较轻：#10 Gaur（t = 153.07 s，局部图 `r3/t0153.07_gaur_crop_fullres.png`）的眼和吻被「Gaur / 1,050 kg」压住，只有角和头顶清楚。也建议预裁，把头部上移约 20% 画面高度。

- **R3-M3 风险版现在不能按现有文件发布**（风险版 t = 146.5、178.13 s；`publish.md`）
  - 证据：① 风险版屏上署名仍是「Photo: Coke Smith / unknown」「Photo: Stephen Belcher Photography / WWF / unknown」（第 2 轮 n3 没处理）；`assets.json` 里这两张的 licence 仍是「unknown」，`licence_url` 为空。② `publish.md` 只有默认版的署名，#7 写 0Lucky Luke，#11 写 Jim, the Photographer，和风险版画面不符。如果用户签字选风险版，按现在的 `publish.md` 上传会署错名。
  - 改法：默认母版发布时不受影响。若要发布风险版：先取得书面授权，把 licence 改成实际授权条款（例如「© Stephen Belcher / WWF, used with permission」），屏上署名去掉「unknown」，重渲风险版，再单独生成一份风险版的 publish（或在 `publish.md` 里加一节风险版署名）。

### Minor

- **R3-m1 描述框缺两段说明**：森林象「no forest elephant has ever been weighed; estimates range from ~2 to 4.5 t」，以及低可信度国旗清单（长颈鹿、巨羚、邦戈、普通大羚羊、欧洲野牛，第 2 轮 m4）。`topic.md` 说描述框已照写，实际没有。建议在 `publish.md` 描述的口径段之后补 2 行，再跑 `publish` 或手工补进去。
- **R3-m2 说明文字没同步**：
  - `sources.md` §1 末句仍写「gaur 与非洲水牛主值改用 HMW」，gaur 已不是 HMW；「凡出处只给雄性体重范围的，一律取全物种范围中点」读不通（第 2 轮 n6）。
  - `topic.md` 口径行仍写「gaur（825）」，洞察卡第 5 条仍写「after 11 … 1 吨以上」（实际是 after 12、「a tonne or more」），开头仍是「待用户点头」。
  - #15 African Buffalo 的 notes 仍写「按最大、最常见的开普水牛口径」「唯一性别分开来源经 Wikipedia 转引」，与现在的 HMW 取值矛盾；#24 Brown Bear 的 notes 仍写「Chosen value (Katmai mid-summer)… consider a lower figure」。
  - 改法：在 `_build/build.py` 改 notes 和 §1 文案，重跑 gen_sources，并改 `topic.md`。
- **R3-m3 Banteng（并列 #15）的雄性值同样只出自维基**：source 写「ADW (600–800 kg, sexes not separated) ; Wikipedia: bulls 600–800 kg (citing Mason's… Livestock Breeds)」，tier 却标 primary，而《Livestock Breeds》是家畜资料。与 R3-M1 同类，影响的是并列 #15 是否成立。建议找 AWCSG 或 HMW 的 banteng 雄性数值；找不到就把 tier 改为 secondary，并在描述框里承认并列只是近似。Banteng 图的许可版本（第 2 轮 m13）仍没有注明核实方式。
- **R3-m4 #7 默认版标本图的小瑕疵**（t = 178.13 s）：左侧露出半只别的犀牛标本（疑似印度犀），底部信用行下面隐约能看到展柜标签字。标本的角很小、体态偏幼，观众会觉得比 #4、#9 的野外犀牛小很多。可以接受，有余力时把 `image_focus` x 调到约 0.6，减少左侧那只标本。
- **R3-m5 国旗或徽章压住角**：#19 Common Eland（t = 86.5 s）的角被南非国旗挡住；#18 European Bison（t = 92.83 s）的角被国旗和「NEAR THREATENED」压住；#17 Giant Eland（t = 99.17 s）的角尖贴着徽章。不影响辨认，可选择把焦点或图下移。
- **R3-m6 「Up to」标签被丢掉，渲染器仍不报警告**：棕熊「Up to ~751 kg」只出自维基（第 2 轮 M6 残留），目前没上屏，但还留在 `data.json` 里。建议删掉，或改成 ADF&G Kodiak 的「up to ~680 kg」；同时给 rank_scroll 记 follow-up，在 timeline / validate 阶段对被丢掉的标签给警告。
- **R3-m7 第 2 轮仍未处理的项**（都不影响发布）：n1 象龟卡放在 after 26（建议改为 after 30，与国旗卡对调）；n2 并列只靠两个「#15」；m2 Kiang 用两性合并值；m3 并列规则只写在描述框；m7 Bongo 是圈养个体、Takin 偏软；m14 长颈鹿 4 种在发布前 7 天复核。

### 音频（临时配乐审片版）

- `…_draft_temp-music.mp4`：AAC 48 kHz 立体声，时长 255.933 s，与视频等长。音轨借用 ep12 的配乐，只供审片，不发布。
- ebur128：Integrated −16.0 LUFS，LRA 5.8 LU，True Peak −4.0 dBFS。对 YouTube 来说响度合适，峰值余量足够。
- 每 0.5 s 的 RMS 曲线：
  - 淡入：0 s −48 dB，约 2.5 s 升到正常电平（−22 至 −25 dB）。
  - 淡出：251 s 起逐步下降，255.5 s 降到 −70 dB，约 4.5 s。
  - 冠军段：222 s 附近有一次抬升，与 #1 揭晓对得上。
  - 片尾：249.5–250.5 s 有一个峰（−13 dB RMS），落在片尾画面上，是借来的曲子自身结构，正式配乐要重看。
- silencedetect（−50 dB、0.5 s）只检出 255.28–255.93 s 的淡出尾，**片中没有断档**。
- 默认母版和风险版的音轨实测 −91 dB，是按设计的静音轨（anullsrc）。**正式 Suno 配乐还没下载（账号下载额度暂停），两个母版目前都不能上传。**配乐到位重混后，要按同样方法重测：ebur128、首尾淡入淡出、silencedetect，以及冠军段的节拍。

### 本轮出的帧

- 默认版：`render/preview/r3/t*.png`（50 张单帧，另有 4 张 `*_crop_fullres.png` 原分辨率局部图）、`render/preview/r3/grid4s_01–04.png`（每 4 s 拼图）。
- 风险版：`render/preview/r3_risk/`（t = 50.17、146.5、178.13、222 s，以及 #7、#11 的原分辨率局部图）。

结论：小修后可发布（默认母版）。数据、名次、并列、洞察卡、计分板、缩略图和署名都已核对正确，第 2 轮的 M9、N1、N4、N5 已解决，没有 blocker。上传前还要处理以下几项：R3-M1，gaur 主值出处是维基；R3-M2，Elk 卡看不到动物；R3-m1，补齐描述框；M8，取得用户签字。另外，正式 Suno 配乐仍待下载，两个母版目前是静音轨，配乐重混并复核音频之前不能上传。风险版在授权签字并修正署名、单独出 publish 之前不可发布。

## 作者处理记录（第 3 轮复审后，2026-11-04 夜间 AUTONOMOUS）

| 项 | 处理 |
|---|---|
| R3-M1 gaur 主值出处是维基 | 再查一轮仍找不到雄性体重的一手出处（ADW 抓取被拦，Ahrestani 2018 取不到原文；网上数字 650–1,000 / 588–1,500 / 840 / 1,300 各说各话）。保留中点 1,044（名次不变），卡上**首位**标「Estimates: 650–1,500 kg」，描述框口径说明加「Forest elephant (2–4.5 t) and gaur (0.65–1.5 t) weights are estimates」。同步进 `_build/build.py`（重跑 build 与现 data.json 逐字段一致） |
| R3-M2 #25 Elk 看不到动物 | 换图：iNaturalist 野外研究级观测 326726395（*C. c. canadensis*，Colorado，ayden，CC BY 4.0），大公鹿占满画面、头和角在上半部，预览帧 `render/preview/r3fix/t0044.00.png` 核对。没选更好看的 n9 / n14，因为是体型小得多的 tule elk 亚种。旧图移到 `_build/old_img/` |
| R3-M3 风险版署名「unknown」 | 屏上署名改为「© Stephen Belcher / WWF, all rights reserved」「© Coke Smith, all rights reserved」（`r3fix_risk/t0178.00.png`）；另出 `publish_with-risk-images.md`（文首注明只在取得授权后使用、授权后改署名） |
| R3-m1 描述框缺说明 | scope_note 补森林象 / gaur 估计值与低可信度国旗清单（581 / 600 字符） |
| sources / topic 旧说法 | `gen_sources.py` 重生成；`topic.md` gaur 口径、洞察卡 after 12 与换图说明已改 |
| gaur 眼口被文字压住 | 图是横幅、渲染器不缩放，焦点调整无效；作为 minor 接受 |
| Banteng 只出自维基 | 主源实为 ADW（600–800 kg），维基只作同值交叉，不改 |
| 母版 | 两个母版按新数据重渲；临时配乐审片版随后从新默认母版重建 |

---

## 第 4 轮独立复核（2026-11-04，fresh context）

> 独立复核（fresh context，没有参与制作）。不以作者处理记录为准，只看当前文件和成片。
> **一致性**：三个 mp4 的 sha256 与各自 manifest 的 `output_sha256` 一致：默认版 `dc523f84…`，风险版 `99d22034…`，临时配乐版 `75ebbb7e…`。两个母版 manifest 记录的 32 项输入（`data.json`、`assets.json`、30 张图）与当前文件逐一吻合。临时配乐版的视频流 MD5 与默认母版相同（`eb798965…`），只换了音轨，manifest 里的 `video_sha256_before` 也是默认母版的哈希。`python -m rank_scroll validate` 结果为 OK，带和不带 `--allow-risk-images` 都一样。时间线总长 255.93 s，与第 3 轮相同。
> **出帧**：默认版放在 `render/preview/r4/`，t = 1.5、3、5.5、7.5、43.83（另有原分辨率图）、146.5、153.07（另有原分辨率图）、178.13、191.73、223、230、235.5、240、250 s。风险版放在 `render/preview/r4_risk/`，t = 146.5、153.07、178.13、230、235.5、245 s。取点用 `rank_scroll.timeline` 算出的每张卡居中时刻：#25 在 43.83 s，#11 在 146.5 s，#10 在 153.07 s，#7 在 178.13 s。
> **外部查询**：只用 iNaturalist API 查了观测 326726395，并用 curl 把照片原图 591794212 下载到 scratchpad 做比对。没有调用收费服务，也没有渲染。

### 逐条核实

| 项目 | 作者声称 | 我看到的证据 | 是否通过 |
|---|---|---|---|
| **R3-M1** gaur 主值出处是维基 | 找不到雄性体重的一手出处，保留 1,044；卡上首位标「Estimates: 650–1,500 kg」；描述框加 gaur 估计值说明 | `data.json` 中 #10 的第一个标签是「Estimates: 650–1,500 kg」。t = 153.07 s 原分辨率帧上，这个标签完整显示在第二个位置（地点行之后），数量标签被挤掉，属于可接受的取舍。`scope_note` 和 `publish.md` 描述框里都有「gaur (0.65–1.5 t) weights are estimates」。source 写的是「Nowak 1999, Walker's… (male range, via Wikipedia)」，tier = secondary，如实写明经维基转引，即第 3 轮方案 (b)。主值仍然只能靠维基读到，但已在屏上和描述框里公开标为估计值。名次 #10 1,050 > #11 1,000 > #12 950，显示值复算正确。 | **通过**（按方案 b 接受；残留：一手出处仍缺） |
| **R3-M2** #25 Elk 看不到动物 | 换成 iNat 326726395 的科罗拉多大公鹿 | API 核实：`taxon = Cervus canadensis canadensis`，研究级，4/4 鉴定一致，`captive = false`，地点 Colorado, US，日期 2025-11-15；照片 591794212 为 cc-by，署名「(c) ayden」，原图 2048×1536。我下载了原图，sha256 是 `598650fd…`，**与 `assets/img/25_elk_wapiti.jpg` 和 `assets.json` 逐字节相同**。来源页、作者、许可三处一致：`assets.json`（source_page = observations/326726395，author = ayden，CC BY 4.0）、`data.json` 的 `image_credit`（「ayden / CC BY 4.0」）、`publish.md` 描述框和 Comment 1（含许可链接和源页）。t = 43.83 s 的卡上，鹿头、眼、吻和整副鹿角都在名称上方的空白区，一眼能认出是公鹿；身体后半部压在文字下面，不影响辨认。屏上署名「Photo: ayden / CC BY 4.0」完整显示。 | **通过** |
| R3-M2 同类：gaur 眼口被压住 | 横幅图，渲染器不缩放，作为 minor 接受 | t = 153.07 s：角、头顶和耳都清楚，脸部偏暗，吻部被「Gaur」压住，物种仍能认出。 | 接受（minor，维持） |
| **R3-M3** 风险版署名「unknown」 | 屏上署名改成「© … all rights reserved」，另出 `publish_with-risk-images.md` | 风险版 t = 178.13 s 显示「Photo: © Stephen Belcher / WWF, all rights reserved」，t = 146.5 s 显示「Photo: © Coke Smith, all rights reserved」，屏上没有「unknown」。默认版同两个时刻显示「0Lucky Luke / CC BY-SA 4.0 (museum specimen)」和「Jim, the Photographer / CC BY 2.0 (museum diorama)」，与 `publish.md` 一致。`publish_with-risk-images.md` 已经生成，与 `publish.md` 只差 #7、#11 两行署名和文首警示（「只在取得授权后使用」）。但它的描述框和 Comment 1 里这两条仍写「(unknown)」，与屏上的「all rights reserved」不一致，见 R4-m3。`assets.json` 里这两张的 licence 仍是「unknown」，在未授权时如实。 | **通过**（作为「授权前不可用」的草稿合理，残留见 R4-m3） |
| **R3-m1** 描述框缺两段说明 | `scope_note` 补上森林象、gaur 估计值和低可信度国旗清单（581 字符） | `scope_note` 实测 581 字符，原样出现在两份 publish 的描述框里，包含「Forest elephant (2–4.5 t) and gaur (0.65–1.5 t) weights are estimates」和「Low-confidence flags: giraffe, giant eland, bongo, common eland, European bison」。描述框实测：默认版 3,306 字符，风险版 3,310 字符，都 ≤ 5,000，也都没有 YouTube 禁用的 `<`、`>`。署名覆盖：描述框和 Comment 1 各有 30 条，与默认版屏上 30 张图逐条对应（#7、#11 用的是替代图作者），没有漏项，也没有多出的条目。 | **通过** |
| **R3-m2** sources / topic 旧说法 | 重跑 `gen_sources.py` 重新生成；`topic.md` 的 gaur 口径、洞察卡 after 12、换图说明已改 | `topic.md` 第 8 行的 gaur 口径、第 18 行「after 12 … a tonne or more」、第 27 行 #25 换图说明都已更新。**但以下几处仍是旧的**：`sources.md` §1 第 13 行仍写「gaur 与非洲水牛主值改用《HMW》」（gaur 现在不是 HMW），「一律取全物种范围中点」这句仍然读不通（`topic.md` 第 8 行同样）；#15 African Buffalo 的备注仍写「按最大、最常见的开普水牛口径」「唯一性别分开来源经 Wikipedia 转引」；#24 Brown Bear 的备注仍写「Chosen value (Katmai mid-summer)… consider a lower figure」。 | **部分通过**（见 R4-m2） |
| Banteng 只出自维基 | 主源是 ADW，维基只是同值交叉核对，不改 | source 链接是 ADW，原文写「sexes not separated」，雄性口径仍有疑问，tier 仍标 primary。属于第 3 轮 R3-m3 的范围，不影响画面。 | 维持 minor（未改） |
| 母版重渲 | 两个母版按新数据重渲；临时配乐版从新默认母版重建 | 哈希、输入、视频流比对的结果见上方「一致性」。 | **通过** |

**本轮重新核对、通过的画面**：
- 片头：t = 3 s 片头三行（标题、口径行、来源行）都完整。
- #30：t = 5.5、7.5 s 的 #30 平原斑马卡在 `intro_hold` 期间完整可读。
- #5 森林象：t = 191.73 s 的卡上「Estimate: none weighed」在屏上。
- 冠军段：t = 223 s 冠军光晕、No. 1 面板、6,000 kg / 13,200 lb 都正常。
- 计分板：t = 230 s 显示 Africa 13 / Asia 10 / North America 4 / Europe 3，合计 30。滚动途中 t = 43.83、146.5、153.07、178.13 s 各帧的累计数，我按已入画的卡逐个数过，都对得上。
- 来源卡（t = 235.5 s）和片尾（t = 240、250 s）干净，两个版本相同。
- 没有发现文字出框或重叠。

### 新发现的问题

**Blocker：无。**

**Major：无。**

**Minor**
- **R4-m1 `assets.json` 中 #25 的 `modified` 写的是「resized and cropped」，但文件与 iNat 原图逐字节相同**，sha 都是 `598650fd…`，尺寸都是 2048×1536。实际裁切发生在渲染阶段，描述框里的「resized and cropped」是对成片的总说明，不影响许可合规。建议账本这一项改成「unmodified (renderer crops)」。
- **R4-m2 R3-m2 只改了一部分**（明细见上表）。这些说明文字和备注不上屏，也不进 publish，但仍和当前取值矛盾：`sources.md` §1 第 13 行、#15 和 #24 的备注、`topic.md` 第 8 行的口径句。建议在 `_build/build.py` 和 `gen_sources.py` 里改掉，再重新生成。
- **R4-m3 风险版发布稿的署名写的是「(unknown)」，屏上写的是「© … all rights reserved」**，两者不一致。文首警示已经要求授权后再改。另外要注意：授权后如果条款要求写「used with permission」之类，屏上文字也要改，风险版就得重渲；不能只改 publish 稿。
- **残留（不阻挡发布）**：
  - R3-m4：#7 默认版标本图左侧仍露出半只别的犀牛标本。
  - R3-m5：#17 至 #19 的角被国旗或徽章压住。
  - R3-m6：棕熊「Up to ~751 kg」只出自维基，仍留在数据里，因宽度不够没有上屏；渲染器对被丢掉的标签仍不报警告。
  - R3-m7 各项仍未处理。

**待用户办理（不是画面缺陷，但上传前必须完成）**：
- M8 森林象取值：`topic.md` 开头仍是「待用户点头」，还没有用户签字。
- m14 长颈鹿 4 种：发布前 7 天要复核。

### 配乐现状

正式 Suno 配乐还没到位（下载额度暂停，属于已知外部阻塞）。实测 volumedetect：默认母版和风险版的音轨 mean 和 max 都是 −91.0 dB，确认是静音轨；临时配乐审片版是 mean −18.7 dB、max −4.1 dB，借用 ep12 的曲子，只供审片，不发布。正式配乐重混后，要按第 3 轮的方法重测：ebur128、首尾淡入淡出、silencedetect，以及冠军段的节拍。

结论：可发布（默认母版静音画面版）。第 3 轮的 R3-M1、R3-M2、R3-M3、R3-m1 已在当前产物中生效，没有新的 blocker 或 major。正式配乐重混并复测之前不能上传。上传前还需要用户对 M8（森林象取值）签字。风险版要先取得两张图的授权，并按授权条款改署名（必要时重渲），之后才可使用。

## 作者处理记录（第 4 轮复核后，2026-11-04）

| 项 | 处理 |
|---|---|
| R4-m1 #25 账本 `modified` | `assets.json` 改为「unmodified original (2048x1536); the renderer resizes and crops at render time」。渲染器不读该字段，画面不变，不重渲；三个 manifest 的 `inputs.assets.json` 换成新 sha，并在 `post_render_edits` 记前后 sha 与原因。`validate` OK |
| R4-m2 说明文字残留 | `sources.md` §1 口径句改为逐条说明（棕熊 / 非洲水牛 / gaur 各自取值）；#15、#24 备注末尾加「第 4 轮复核更正」（`gen_sources.py` 的 ERRATA，不改 data.json，免得母版输入 sha 失配）；`topic.md` 口径句「全物种范围中点」改为「该范围中点」 |
| R4-m3 风险版发布稿署名 | `publish_with-risk-images.md` 两条署名改为与屏上一致的「© … all rights reserved, used with permission」，文首警示写明若授权方要求别的写法，发布稿和屏上署名都要改、风险版须重渲 |
| 沿用 minor（R3-m4/m5/m6/m7、gaur 脸部） | 不改：不挡辨认，换图或改版式的收益小于重渲 1 小时的成本 |
| M8 森林象取值、m14 长颈鹿复核 | 留给用户（`_build/handoff.md`「发布前要你定」） |

## 配乐独立审片（2026-11-04，fresh context）

> 独立审片（fresh context，没有参与配乐制作）。只读检查，不重渲，没有调用收费服务。工具：ffprobe / ffmpeg（ebur128、astats、silencedetect、showspectrumpic）+ numpy 自算每秒频谱、互相关和节拍网格。中间产物在 `render/preview/audio_r1/`：`loudness_energy.png`（全片 M/S 曲线、>4 kHz 能量与段落标记）、`spec_full.png`、`spec_140-200.png`、`spec_236-256.png`、`spec_108-122_lin4k.png`、`spec_196-210_lin4k.png`、`wave_*.png`、`per_second_table.txt`、`ebur128_log.txt`。为节省空间，解码出的 wav 已删除，可用 ffmpeg 重新导出。
> 卡片时刻是用 `rank_scroll.timeline.build` 按 card_w=720 算出的：#10 Gaur 141.9 s 入画，148.3 s 全入，153.1 s 居中；#9 Black Rhino 159.9 s 居中；#8 Giraffe 166.7 s 居中；#8 后洞察卡 172.4 s；#7 Javan 178.1 s 居中；#6 Hippo 184.9 s 居中；#2 212.1 s 居中；冠军段 220.93 s 起。

### 测量表

| 项 | 实测 | 判定 |
|---|---|---|
| 帧数 / 时长（默认版、风险版） | 都是 15356 帧（count_frames 实数），60 fps，255.933 s；AAC 48 kHz 立体声 256k，音轨 start 0、时长 255.933 s，共 12,284,784 个采样点，与视频等长 | 通过 |
| sha256 vs manifest | 默认版 `5e94b8e8…dee9`、风险版 `2b4c92a7…27f4`，都与各自的 `output_sha256` 一致；两首原曲 sha 与 `inputs.music` 一致 | 通过 |
| 两版音轨是否相同 | AAC 包级 MD5 都是 `ea5bf770…b229`，解码后 PCM 的 sha 也相同 | 逐位一致 |
| 音乐床拼法是否与 manifest 相符 | 成片与原曲做互相关：0–178 s 对 A 同一时刻，滞后 0、相关 0.9997–1.0000；182–255.9 s 对 B 的 `t − 178 + 94.387`，滞后 0、相关约 0.9995。A 0–182 全曲，B 从 94.387 s 切入到 172.32 s，接点在成片 **178–182 s**（2:58–3:02），与 fit=end 的计算一致（链长 350.32 − 255.933 = 94.387） | 与 manifest 一致 |
| 积分响度 / LRA | −16.0 LUFS；LRA 5.8 LU（low −19.5，high −13.7） | 通过 |
| 真峰值 / 样本峰值 | TP −3.9 dBFS；样本峰值 −3.96 dBFS（出现在 7 s 首个鼓点）；Flat factor 0；DC 0.0002 | 无削波 |
| 静音段 | silencedetect −50 dB/0.3 s 和 −40 dB/0.5 s 都只检出 255.35–255.93 s 的淡出尾，片中没有断档 | 通过 |
| 淡入 | 0–50 ms 峰值 −71 dBFS，0.05–0.5 s 峰值 −27 dBFS，1 s 后进入正常电平，没有起始爆音。7.2–7.6 s 首个重拍（M 从 −20 升到 −14） | 通过 |
| 淡出 / 收尾 | B 曲的尾声从成片约 235.6 s 开始（来源卡至片尾），250 s 有一记低音重拍和长和弦。3 s 淡出 252.93–255.93 s；最后 133 ms 峰值 −62.7 dBFS，干净落到静音，与片尾画面同时结束 | 通过 |
| 短时响度跳变（S 每 1 s 变化 ≥ 2.5 LU） | 只有 7→8 s（首鼓进入）和 250→251 s（片尾重拍）。M 在 0.4 s 内变化 ≥ 5 LU 的点：145.1–146.1 s（进前 10 前的 break）、220.1–221.5 s（冠军段起点的短停顿）、167.7 s，都是曲子自身的编曲 | 无异常跳变 |
| 分段平均响度 | #30–#21 −17.4；#20–#11 −14.7；#10 入画到 #9（147–163 s）−14.2；**163–180 s −18.3（>4 kHz 能量 22 dB，前后约 48–49 dB）**；B 段 #7–#2（180–220.9 s）−15.4；冠军 −17.3；计分板 −15.8；来源 −15.8；片尾淡出前 −19.3（单位 LUFS，按 M 能量平均） | 见 AU-M1 |
| 速度（onset 自相关粗估） | A 主体约 132 bpm（66 和 99 的峰也强，节拍歧义）；B 约 100 bpm（prompt 要求 96）。B 切入点 94.387 s 落在 B 节拍网格某拍之前约 0.12 s；处于小节第几拍，算法定不了 | 见 AU-m1 |
| 人声 | Suno 请求 `instrumental: true`，prompt 写明「no vocals」。0–4 kHz 线性频谱（108–122 s、196–210 s）只有阶梯状的平直谐波，没看到独唱人声的滑音、颤音或共振峰走向。无词合唱垫（aah）不能排除 | 代理判断：未见人声，需人耳确认 |
| publish 署名与清单 | `publish.md:60`、`publish_with-risk-images.md:62` 都有 Music 署名行（job 101bce70，clips 11cce2f0 + b2fcbabf），与 `data.json.music_credit` 一致；两份 Upload checklist 都有配乐项（不登记 Content ID，被认领时用 request_log 申诉）。`paihangbang/request_log.md` 里有该 job 和两首 clip 的完整 ID | 通过 |

### 问题

**Blocker**：无。

**Major**

- **AU-M1 A 曲的结尾段落落在前 10 名中段，听起来像曲子先结束、再换一首。** 按 fit=end 的拼法，A 整首（0–182 s）原样保留，没有裁掉结尾。A 自身 163 s 起进入尾声：>4 kHz 能量从约 51 dB 掉到 5–30 dB，RMS 降 6–10 dB，178–182 s 自然淡出到 −37.5 dB。这一段落在成片 **2:43–3:00**，正是 #8 Giraffe 居中（2:46.7）、#8 后洞察卡（2:52.4）、#7 Javan 入画到居中（2:47–2:58.1）的位置。随后 B 从中段以 4 s qsin 渐强切入，约 3:01 恢复满编（M 从 −22.0 升到 −14.9）。结果是前 10 名段（147–220.9 s）平均 −15.6 LUFS，反而不如 #20–#11 段（−14.7）响；全曲能量最高的地方在 #15–#11（约 110–145 s，S −13.5 至 −14），不在前 10。这与 bible §5「前 10 名处进入高潮段」相反。补充：进前 10 的 145–148 s 有一个 break 加低音落点，与 Gaur 全入画（148.3 s）对得上，这一点是好的。问题在其后约 17 s 的能量洞。
  - 修法（只需重做音轨 remux，视频流照旧复制，不用重渲）：把 A 的出点设在尾声开始前，大约 162.5–163 s（162 s 有一记重拍，163 s 起转入尾声），例如 `a.mp3@0:163`，fit=end 仍然生效。重算后，B 的切入点会前移到约 75.4 s（链长 331.32 − 255.933），接点移到成片约 159–163 s，也就是 #9 Black Rhino 居中附近。B 的切入点最好对齐 B 自身的乐句起点（人耳选，或在 75 s 附近找下拍）。改完要按本节的方法复测接点。

**Minor**

- **AU-m1 两首曲子的速度感不同（A 约 132/66 bpm，B 约 100 bpm），接点是硬换节奏。** 本版重叠的 4 s 内，A 已经在自身尾声（−22 → −37 dB），节拍冲突被掩盖，实测接点没有响度突增或瞬态（M 在 178–182 s 没有 ≥ 5 LU/0.4 s 的跳变）。按 AU-M1 改出点后，A 在接点处是满编，两套节拍会在 4 s 内叠在一起，冲突会更明显。届时建议缩短交叉淡化，或把接点放在 A 的 break（如 145 s）上，并请人耳确认。

### 无法由代理判断、需要人耳试听的点

1. **2:43–3:02（163–182 s）**：A 尾声加 B 渐入，听起来是否像「歌结束了」；B 的切入（成片 2:58，B 曲 94.4 s）是否落在乐句中间、是否突兀。
2. **2:25–2:28（145–148 s）**：进前 10 的 break 和落点与 Gaur 入画是否合拍（代理判断：大致对上）。
3. **3:40.5–3:41.3（220.5–221.3 s）**：冠军段起点有约 0.5 s 的停顿（M 降到 −29 LUFS）后再进，可能起到「揭晓前的停顿」作用，也可能显得像掉音。冠军段整体比前一段低约 2 LU，有没有揭晓感要人耳判断。
4. **4:10–4:16（250–255.9 s）**：片尾的低音重拍、长和弦和 3 s 淡出是否自然收住。
5. **人声**：全片，重点听 1:48–2:02 和 3:16–3:30，是否有无词合唱或人声采样。
6. 整体曲风（非洲鼓、马林巴、弦乐）与草原动物题材是否相称，是否吵到影响读卡；这些只能靠人耳。

结论：需修改：AU-M1（A 曲尾声落在前 10 名中段 2:43–3:00，形成约 17 s 的能量洞，随后换曲，与 bible §5「前 10 名进入高潮」相反）。修法是把 A 的出点提前到约 163 s，重做 remux，不用重渲。技术指标全部通过：帧数和 sha 一致，两版音轨逐位相同，−16.0 LUFS，TP −3.9 dBFS，无削波，无片中静音，首尾淡入淡出干净，署名齐全。改后请复测接点，并请人耳试听新接点和 3:40.9 冠军停顿。

## 配乐独立复核第 2 轮（2026-11-04，fresh context）

> 本轮由没有参与配乐制作的独立审片人复核（fresh context），作者自述只当待验证的说法。只读检查，没有重渲，也没有调用收费服务。工具：ffprobe / ffmpeg（ebur128 帧日志、astats、silencedetect、showspectrumpic）、numpy / scipy（逐段互相关、分频带能量）、librosa（节拍跟踪）。中间产物在 `render/preview/audio_r2/`：`loudness_energy.png`（全片 M/S 曲线、>4 kHz 能量、段落和接点标记）、`spec_full.png`、`spec_junction_138-160.png`、`spec_champion_214-227.png`、`spec_end_234-256.png`、`spec_185-199_lin4k.png`、`per_second_table.txt`（分段表、逐秒表、跳变表）、`ebur128_log.txt`。解码出的 wav 已删除，需要时可用 ffmpeg 重新导出。
> 卡片时刻用 `rank_scroll.timeline.build` 算出（card_w=720）。下文的「入画」「居中」都指这个结果，例如 #11 Wild Yak 居中 146.5 s；#10 Gaur 141.89 s 入画、148.25 s 全入、153.07 s 居中；#5 居中 191.7 s；#1 207.75 s 入画、220.93 s 居中，冠军段从 220.93 s 起。

### 逐条核实

| 项 | 实测 | 判定 |
|---|---|---|
| 帧数 / 时长 | 两版都是 15356 帧（count_frames 实数），60 fps，时长 255.933 s。音轨为 AAC 48 kHz 立体声，start 0，时长 255.933 s，共 12,284,784 个采样点 | 通过 |
| sha 与 manifest | 默认版 `6cc00ab2…5853`、风险版 `1aa6abc9…a8f7` 都与各自 manifest 的 `output_sha256` 一致。两首原曲 A `9b522096…274d`、B `f2b09cd1…1507` 与 `inputs.music` 一致。`video_sha256_before` 是上一轮带配乐母版的 sha（`5e94b8e8…`）。默认版视频流的包级 MD5 是 `eb798965…`，与第 4 轮复核记录的默认母版视频流相同，说明画面没动 | 通过 |
| 两版音轨是否逐位相同 | AAC 包级 MD5 都是 `903dab43…2f01a`，解码后 PCM 的 sha256 也一样（都是 `9f93f652…77f7`） | 逐位一致 |
| 拼接是否如作者所述 | 用 2 s 窗把成片与原曲做互相关。0–144 s 对 B 的同一时刻，滞后 0，NCC 0.9989–1.0000。150–252 s 对 A 的 `t − 73.933`（即 71.797 + (t − 145.73)），滞后 0，NCC 0.9994–1.0000。145–149 s 是过渡：B 的 NCC 从 0.97 降到 0.05，A 的 NCC 从 0.20 升到 0.99。增益恒为 −1.3 dB，与 loudnorm pass1 的 −14.71 → −16 一致（第二遍是 linear）。拼链长度 149.73 + 110.203 − 4 = 255.933，与片长相等，A 播到自身 182.0 s 的末尾，与画面终点对齐 | 与作者所述和 manifest 一致 |
| 积分响度 / LRA | −16.0 LUFS；LRA 6.7 LU（low −20.4，high −13.7） | 通过 |
| 真峰值 / 削波 | TP −5.1 dBFS，样本峰值 −5.10 dBFS，Flat factor 0，DC 0.0002 | 无削波 |
| 片中静音 | silencedetect：−50 dB / 0.3 s 一处都没有；−40 dB / 0.25 s 只有 0–0.28 s（淡入）和 255.03–255.93 s（片尾淡出）。片中最低的地方是 136.9–137.3 s（B 的 stop-time，0.1 s 窗 RMS 降到 −38 dB，持续 < 0.3 s）和 219.4–219.5 s（A 的 break，−36 dB，约 0.2 s） | 无断档（两处短停顿列入人耳项） |
| 分段响度（M 能量平均，LUFS） | 片头 −25.0；#30–#21（5–77 s）−18.8；#20–#11（77–141.9 s）−15.7；#11→#10 过渡（141.9–149.8 s）−16.1；**前 10 名 #10–#2（149.8–216.5 s）−14.7**，其中 #10–#6 为 −15.4、#5–#2 为 −13.9；冠军逼近（216.5–220.93 s）−13.8；**冠军段 −14.5**；计分板 −13.9；来源卡 −14.0；片尾（237.93–252.93 s）−18.6；最后 3 s 淡出 −28.5 | 见 AU-M1 |
| AU-M1 是否消除 | 已消除。以 10 s 为一块，S 的最大值：前 10 名以前最高 −14.3（130–140 s）；180–240 s 每块都在 −12.8 到 −13.5 之间。全片 S 最大值 −12.8 出现在 191.7 s（#5 居中）和 218.8 s（冠军揭晓前）。>4 kHz 能量在 150–236 s 一直保持在 44–53 dB，没有出现上一轮那种降到 22 dB 的尾声。A 的尾声（自身 163 s 起）现在落在成片 236.9 s，即来源卡末尾，片尾画面 237.93 s 起，正好用作收尾。前 10 名、冠军和计分板一段（约 180–236 s）是全片能量最高的地方 | 通过 |
| 新接点（145.73–149.73 s，4 s qsin） | 逐秒 M：−17.1 / −15.8 / −15.4 / −15.2 / −15.2 / −15.8（145–150 s），过渡平滑，没有凹陷或鼓包，0.4 s 内变化 ≥ 5 LU 的点一个都没有。频谱上，B 约 700–1000 Hz 的旋律型与 A 1–3 kHz 的和声层在约 146.7–149 s 共存，随后 A 接管。A 切入点附近：A 自身 70.5–71.1 s RMS 下降约 3–4 dB，属于小停顿；71.8 s 有一个起音（−15.7 dB），作者的描述属实。不过入点处 qsin 的增益接近 0，入点本身听不出来 | 响度通过；节拍见 AU-m1 |
| 节拍（AU-m1） | librosa 节拍跟踪：A 为 129.2 bpm（拍距 0.464 s），B 为 99.4 bpm（拍距 0.604 s），两者之比 1.30，不成整数比。过渡期 B 的拍点在 146.73 / 147.33 / 147.91 / 148.52 / 149.10 s，A 的拍点在 146.54 / 147.01 / 147.47 / 147.91 / 148.38 / 148.84 s。两组在 147.91 s 恰好重合，这一刻也接近交叉淡化的中点 147.73 s；但相邻拍子各错开约 140 ms，再往外错得更多。两首电平相差不到约 8 dB 的时段大约是 146.7–148.7 s，即约 2 s 的两套速度叠加 | 残留 minor（R2-m1） |
| 片尾 | A 尾声从 236.9 s 开始：鼓组停止，>4 kHz 能量降到 5–30 dB，只剩长和弦和低音，241.6 s、246 s 各有一处轻重拍。A 自身最后 1 s 为 −36 至 −39 dB，没有自己落到全静音；3 s 淡出（252.93 s 起）叠加后，最后 100 ms 峰值 −60.8 dBFS，最后 10 ms 峰值 −84 dBFS，末样本为 0。片尾画面 18 s（237.93–255.93 s）全程是安静的尾声 | 通过，干净落到静音 |
| 冠军揭晓附近 | 218.8 s 为全片 S 峰值（−12.8）。219.0–219.5 s 音乐快速收住，219.4–219.55 s 约 0.2 s 降到 −30 至 −36 dB；219.6 s 中频乐器重新进入，低频（<200 Hz）一直到约 221.4 s 才回来；**约 221.5 s 低音和鼓全部回归**，比冠军居中（220.93 s）晚约 0.6 s。这是典型的 stop、break、drop 结构，不是掉音或拼接造成的；整个冠军段（220.93–226.93 s）是 −14.5 LUFS，后面的计分板是 −13.9 | 判为编曲本身的设计；揭晓感需人耳确认 |
| 人声 | 0–4 kHz 线性频谱（185–199 s，A 段）只有阶梯状的平直长音谐波，没看到独唱人声那种滑音、颤音或共振峰走向。B 段与上一轮看过的同一首曲子相同。无词合唱垫（aah）不能排除 | 代理判断未见人声，需人耳确认 |
| 署名 | `publish.md:60` 的 Music 行列了两个 clip（11cce2f0 + b2fcbabf），顺序调换不影响署名；`publish.md:145` 的 Content ID 清单项还在 | 通过 |

### 问题

**Blocker**：无。

**Major**：无。上一轮的 AU-M1 已消除，前 10 名、冠军和计分板一段（约 180–236 s）是全片能量最高处。

**Minor**

- **R2-m1（即 AU-m1，风险降低但没有消除）：接点 2:26.7–2:28.7（146.7–148.7 s）有约 2 s 两套速度（99.4 / 129.2 bpm）以相近电平叠加。** 中点附近两组拍子在 147.91 s 重合，响度过渡平滑，所以是否听起来发糊、像抢拍，只能靠人耳判断。人耳若觉得乱，可以把交叉淡化缩短到约 1.5–2 s，并以 147.91 s 这个重合拍为中心。`build_music_bed` 的 `MUSIC_XFADE` 是固定的 4 s，改它要动工具代码，或者在 `add_music.py` 里单独处理。这项只需重做 remux，不用重渲。人耳不觉得有问题就不用改。

**观察（不计入问题）**

- 前 10 名内部是逐步升高的：#10–#6（149.8–188.3 s）为 −15.4，与 #20–#11 的 −15.7 基本持平，157–170 s 有几次 1 s 左右的低频抽空（A 自身的编曲）；明显抬升从 #5（约 3:08）开始。进入前 10 名时的「换段」主要靠音色和曲子的更替，不是靠响度。这符合 bible §5「前 10 名处进入高潮段」的大意，但想要 #10 一入画就更燃，只能换选段。
- 开头 0:00–0:30 是 B 的前奏，比上一版轻（片头 −25，#30–#21 为 −18.8，上一版是 −17.4），属于渐进铺垫。是否太薄、影响开头抓人，需人耳判断。

### 需要人耳试听的具体时刻

1. **2:25.7–2:29.7（145.7–149.7 s）新接点**，重点听 2:26.7–2:28.7：两套速度叠在一起是否发糊或抢拍，换曲是否与 #10 Gaur 入画（2:21.9 入、2:28.3 全入）对得上，像不像「进入前 10 名换了一段」。
2. **3:39.0–3:41.6（219.0–221.6 s）冠军揭晓**：219.4 s 约 0.2 s 近静音，然后约 1.8 s 没有低音，221.5 s 低音和鼓回归（冠军 220.93 s 居中后约 0.6 s）。要判断这听起来是「揭晓前的停顿」还是像掉音，以及低音回归是否最好正好落在居中那一刻。
3. **2:16.5–2:17.4（136.5–137.4 s）**：B 的 stop-time，约 0.8 s 衰减到 −38 dB 后重拍进入，画面上是 #11 Wild Yak 正在入画。要判断听起来像不像断档。
4. **3:57–4:16（237–255.9 s）片尾**：A 尾声的长和弦、241.6 s 和 246 s 的轻重拍，加上最后 3 s 淡出，是否自然收住。注意 A 自身最后的余音被淡出压掉了约 1–2 s。
5. **0:00–0:30 开头**：B 前奏偏轻，是否撑得住片头和前几张卡。
6. **人声**：全片都要听，重点是 1:48–2:02（B）和 3:05–3:19（A），听是否有无词合唱或人声采样。
7. 整体曲风（非洲鼓、马林巴、弦乐）是否贴合草原动物题材，是否吵到影响读卡。

结论：默认母版（带配乐）可以发布（有条件）。AU-M1 已消除，前 10 名、冠军和计分板是全片能量最高处，A 的自然尾声落在片尾画面上，干净收到静音。拼接与作者所述和 manifest 一致，两版音轨逐位相同，帧数和 sha 都对得上；−16.0 LUFS，TP −5.1 dBFS，无削波，片中无静音断档。没有 blocker 或 major，只剩 R2-m1（2:26.7–2:28.7 两套速度短暂叠加）这一条 minor。发布前请人耳听一遍 2:25–2:30 接点和 3:39–3:42 冠军揭晓；两处都没有异议即可发布，否则按 R2-m1 的方法缩短交叉淡化后重做 remux。
