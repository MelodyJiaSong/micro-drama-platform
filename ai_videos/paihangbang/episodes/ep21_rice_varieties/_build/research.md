> **本期图片约定（用户 2026-11-06，follow-up 056）**：卡片只拍米本身，不用配菜或成品菜（会分散焦点）。主图 = 该品种煮熟的纯米饭或生米粒；小图 = 生米粒特写。大字一栏写粒型（Long grain / Short grain / Glutinous…），不写招牌菜；`items_draft.json` 的 signature dish 只作文字备用。

# ep21 · 30 Kinds of Rice Around the World — 研究稿（列表模式，不排名）

> 2026-11-06 研究草稿。条目数据在 `items_draft.json`，它由 `make_items_draft.py` 生成并校验（共 30 条，`name` ≤ 22 字符，`fact` ≤ 110 字符，名称不重复）。
> 未调用任何收费服务。来源核对只用了网页检索和抓取。
> 本稿还不是 `data.json`：尚未分配 tags、corner、badge 或图片；交叉核对也没有按 bible §3.2 逐条写 `diff_pct`（本期没有数值主值，大多是事实陈述）。

## 1. 路线（地理旅程）

**日本 → 中国东北 → 华南 → 爪哇 → 越南 → 老挝 → 泰国 → 缅甸 → 印度东北（曼尼普尔）→ 孟加拉 → 喀拉拉 → 尼泊尔 → 旁遮普 → 费尔干纳 → 里海岸吉兰 → 安纳托利亚 → 皮埃蒙特 → 卡马格 → 穆尔西亚 → 里巴特茹 → 尼罗河三角洲 → 尼日利亚奥贡 → 马里内尼日尔三角洲 →（横渡大西洋）→ 巴西南大河州 → 墨西哥莫雷洛斯 → 南卡罗来纳低地 → 五大湖（野米收尾）**

为什么这样走：

- **东亚起步**：先讲观众最熟的粳米短粒（寿司米），再讲酿酒米、糯米，然后是中国北方粳米和南方籼米，一南一北形成对比。
- **东南亚先下后上**：从华南直接南下到爪哇（javanica「bulu」型米），再北上经越南、老挝、泰国到缅甸，紧接印度东北的曼尼普尔，陆路连贯。
- **南亚**：从东往西走，中间插一段南下喀拉拉再北上尼泊尔，最后从旁遮普出发，沿丝路进入中亚和西亚。
- **欧洲**：从东往西，经意大利、法国、西班牙到葡萄牙。
- **非洲**：跨地中海到埃及，再往西到西非，最后停在非洲稻的驯化地马里。
- **美洲**：从西非横渡大西洋到美洲，这条线和稻米的历史对得上：非洲稻经奴隶贸易传入巴西和卡罗来纳（来源：Wikipedia *Oryza glaberrima* 引 Carney 2009，只作背景，不上屏）。到美洲后由南往北走，最后以「其实不是稻米」的野米收尾，正好留一个结尾惊喜。

洲际分布（可用于 `tally.by = continent`）：Asia 19（其中东亚 5、东南亚 6、南亚 5、中亚和西亚 3）· Europe 4 · Africa 3 · North America 3 · South America 1。

## 2. 最终 30 条

| # | 名称 | 地区 | 粒型 / 颜色 / 香 / 质地 | 招牌菜 | 类型标签 |
|---|---|---|---|---|---|
| 1 | Koshihikari コシヒカリ | 日本新潟、北陆 | 短粒粳米 / 白 / 无香 / 软糯有光泽 | Sushi | 短粒 |
| 2 | Yamada Nishiki 山田錦 | 日本兵库 | 大粒，心白大 / 白 / 无香 / 磨到只剩心白后酿造 | Sake | 酿酒米（惊喜） |
| 3 | Mochigome もち米 | 日本 | 短粒糯米 / 乳白不透明 / 无香 / 很黏、能拉丝 | Mochi | 糯米 |
| 4 | Wuchang Rice 五常大米 | 黑龙江五常 | 短中粒粳米 / 白 / 有香 / 软、油亮 | Steamed rice | 地理标志（GI），欧盟互认 |
| 5 | Zengcheng Simiao 增城丝苗米 | 广东增城 | 特长细粒籼米 / 白 / 有香 / 松散有弹性 | Claypot rice | 地理标志，长粒 |
| 6 | Pandan Wangi | 印尼西爪哇展玉 | 圆粒 javanica / 白 / 有香 / 软、略黏 | Nasi liwet | 爪哇型米，地理标志 |
| 7 | Broken Rice (tấm) | 越南湄公河、西贡 | 碎粒 / 白 / 无香 / 软、吸汁 | Cơm tấm | 加工等级（惊喜） |
| 8 | Lao Sticky Rice ເຂົ້າໜຽວ | 老挝 | 长或中粒糯米 / 乳白 / 无香 / 黏，用手抓吃 | Larb & sticky rice | 糯米 |
| 9 | Thai Hom Mali ข้าวหอมมะลิ | 泰国东北 Thung Kula Rong-Hai | 长粒 / 白 / 有香 / 软润 | Thai green curry | 香米，欧盟 PGI，「世界最佳大米」 |
| 10 | Riceberry | 泰国农业大学育成 | 长细粒全谷 / 深紫 / 有香 / 有嚼劲 | Purple rice bowl | 紫米，现代育种 |
| 11 | Paw San ပေါ်ဆန်း | 缅甸伊洛瓦底三角洲 | 短圆粒，煮后变长 / 白 / 有香 / 蓬松 | Burmese curry & rice | 香米，「世界最佳大米」2011 |
| 12 | Chak-hao | 印度曼尼普尔 | 中粒糯性 / 黑（煮后紫）/ 有香 / 黏软 | Chak-hao kheer | 黑米，地理标志 2020 |
| 13 | Gobindobhog | 西孟加拉东布德万 | 极短圆粒 / 白 / 有香 / 微黏、奶油感 | Payesh | 小粒香米，地理标志 2017 |
| 14 | Palakkadan Matta | 喀拉拉帕拉卡德 | 粗壮大粒 / 红糠 / 无香 / 硬实 | Kerala sadya | 蒸谷米 + 红米，地理标志 |
| 15 | Jumli Marshi | 尼泊尔久姆拉 | 短中粒 / 红 / 无香 / 硬实带坚果味 | Dal bhat | 高海拔古老品种 |
| 16 | Basmati | 旁遮普（印度 / 巴基斯坦） | 特长细粒 / 白 / 有香 / 干爽粒粒分明 | Biryani | 香米，长粒 |
| 17 | Devzira | 费尔干纳谷地（乌兹别克 / 吉尔吉斯） | 中粒带棱 / 淡红 / 无香 / 硬、不糊 | Plov | 抓饭米，地理标志菜品 2026 |
| 18 | Hashemi برنج هاشمی | 伊朗吉兰 | 长细粒 / 白 / 有香 / 蓬松、粒粒分明 | Tahdig | 香米 |
| 19 | Tosya Rice（Sarıkılçık） | 土耳其卡斯塔莫努 Devrez 谷 | 中粒 / 白 / 有香 / 适合做抓饭 | Pilav | 土耳其原产地名称（PDO）2017 |
| 20 | Carnaroli | 意大利韦尔切利、帕维亚 | 大粒中长 / 珍珠白心 / 无香 / 外糯内弹 | Risotto | 烩饭米 |
| 21 | Camargue Red | 法国罗讷河三角洲 | 短中粒全谷 / 红褐 / 无香 / 有嚼劲 | Camargue rice salad | 红米，Riz de Camargue PGI |
| 22 | Calasparra Bomba | 西班牙穆尔西亚 | 短圆粒 / 珍珠白 / 无香 / 吸汤汁、粒不烂 | Paella | 海鲜饭米，原产地命名（DO）1986 |
| 23 | Carolino | 葡萄牙里巴特茹 | 中长粒粳米 / 白 / 无香 / 绵软吸汤 | Arroz de marisco | 欧盟 PGI 2008 |
| 24 | Egyptian Rice | 尼罗河三角洲 | 短中粒粳米 / 白 / 无香 / 软、微黏 | Mahshi | 非洲的粳米 |
| 25 | Ofada Rice | 尼日利亚奥贡州 | 未抛光 / 褐红或白 / 有香 / 硬、会涨 | Ayamase stew | 未抛光，常混有非洲稻 |
| 26 | African Rice (*O. glaberrima*) | 马里内尼日尔三角洲 | 中粒 / 红糠 / 无香 / 坚果味 | West African rice & stew | 另一个物种（惊喜） |
| 27 | Brazilian Agulhinha | 巴西南大河州 | 长细粒 / 白 / 无香 / 松散 | Arroz e feijão | 日常长粒米 |
| 28 | Morelos Rice | 墨西哥莫雷洛斯州 | 大粒特长，带「白肚」/ 白 / 无香 / 吸汁 | Arroz rojo | 墨西哥原产地命名 2012 |
| 29 | Carolina Gold | 南卡罗来纳低地 | 长粒古老品种 / 白（金色谷壳）/ 无香 / 软、带淀粉感 | Hoppin' John | 古老品种复兴 |
| 30 | Wild Rice (Manoomin) | 美加五大湖 | 针状长粒 / 深褐至黑 / 无香 / 有嚼劲、煮开会裂 | Wild rice soup | **不是稻米（菰属 Zizania）** |

类型覆盖核对：

- 长粒：5、9、16、18、27、29。中粒：4、17、19、20、23。短粒：1、3、13、22、24。
- 香米：4、5、6、9、10、11、12、13、16、18、19。
- 糯米：3、8、12。
- 红米：14、15、21（17 淡红）。黑或紫：10、12。
- 全谷、未抛光或古老品种：10、15、21、25、29。蒸谷米：14。
- 烩饭和海鲜饭用米：20、22。
- 原产地保护（GI / PDO / DO / PGI）：4、5、6、9、12、13、14、19、21、22、23、28（20 被收在 Baraggia PDO 内）。
- 惊喜：2（酿酒米）、7（碎米）、26（非洲稻，另一个物种）、30（野米，不是 Oryza）。

## 3. 判断与取舍（judgement calls）

1. **避免近似重复**。最初候选很多，以下按「同类只留一个」删掉：
   - **黑米**：中国洋县黑米（地理标志的批准年份查不到）、意大利 Venere。最后保留 Chak-hao（黑、糯、有地理标志，有明确的菜 kheer）和 Riceberry（紫、现代育种）。
   - **红米**：不丹红米和 Jumli Marshi 同属喜马拉雅高海拔红米，只留 Marshi，因为它有「世界最高海拔水稻」这个可溯源的事实。不丹红米配 ema datshi 很上镜，可作替补。
   - **茉莉型香米**：越南 ST25、柬埔寨 Phka Rumduol 都多次获得「世界最佳大米」，但和 Thai Hom Mali 太像。东南亚香米只留 Hom Mali，缅甸 Paw San 以「短圆粒、煮后变长」的差异保留。越南改用**碎米**（一个加工类别）。
   - **碎米**：塞内加尔 ceebu jën 也用碎米，和越南重复，所以改放进洞察卡。
   - **巴斯马蒂型**：肯尼亚 Pishori 本身就是 Basmati 370，删掉。
   - **中东长粒香米**：伊拉克 Amber（anbar）和伊朗 Hashemi 重复，留伊朗，因为 tahdig 辨识度更高。伊拉克 Amber 因干旱濒临消失，是个好故事，可作替补。
   - **其他删除**：Calrose 和韩国米（都是短中粒粳米，和日本重复）；Kalanamak（找不到可溯源的招牌菜）；菲律宾 Tinawon（梯田很上镜，但招牌菜没有来源支撑）；马达加斯加（来源弱）。
2. **两个糯米同时保留**：Mochigome（短粒，捣成年糕）和老挝糯米（长粒，蒸熟装竹篮、用手吃），形态和吃法都不同；第三个糯米 Chak-hao 以黑米身份入选。
3. **「招牌菜」不等于品种专属**：许多高档白米本来就是白饭吃，例如五常、Paw San、Riceberry。卡片上的菜是该地区最具代表性的吃法，我已在 `notes` 里写明「pairing, not exclusive」。其中 **African Rice、Riceberry、Camargue Red** 三张没找到有来源支撑的单一招牌菜，大字建议改成别的写法（见各条 notes）。
4. **Basmati 的归属**：印度和巴基斯坦共有这一品种，而且地理标志仍在争议中。草稿 `country_iso2 = IN`（因为卡上的事实是印度 FSSAI 标准），`country_name = "India / Pakistan"`。需要人决定是挂双旗、不挂旗，还是改写成中性事实。
5. **中亚和西亚的洲别**：土耳其（安纳托利亚）计作 Asia。若计分板想单独显示「West Asia」，`continent` 可以改成自定义分组名。
6. **野米与非洲稻**两张卡都已明确标出：野米 `status = "NOT Oryza"`；非洲稻 `status = "Separate species"`。
7. **「首个 / 最大」类说法**：只保留有一手或机构来源的。卡拉斯帕拉「西班牙乃至世界第一个大米原产地命名」、巴西「亚洲以外最大产稻国」两条只有零售或旅游站在说，或者数字太接近，已删除。

## 4. 「Did you know?」洞察（5 条，均 ≤ 90 字符，符合 data_contract）

| after_rank | 文本 | 来源 |
|---|---|---|
| 3 | IRRI's genebank in the Philippines stores over 127,000 rice samples, the largest on Earth. | Genesys / FAO WIEWS PHL001: https://www.genesys-pgr.org/wiews/PHL001 （另有资料称超过 130,000，取保守数） |
| 8 | Glutinous rice is gluten-free: 'glutinous' means glue-like sticky, not gluten. | Beyond Celiac: https://www.beyondceliac.org/gluten-free-diet/is-it-gluten-free/rice/ |
| 16 | Rice is the staple food for nearly half of the world's people. | AfricaRice: https://www.africarice.org/post/birthplace-of-african-rice-domestication-identified-in-mali |
| 25 | Senegal's ceebu jën, UNESCO-listed in 2021, is made with fish and broken rice. | UNESCO ICH 16.COM: https://ich.unesco.org/en/RL/ceebu-jen-a-culinary-art-of-senegal-01748 |
| 26 | 2004 World Food Prize: Yuan Longping (hybrid rice) and Monty Jones (NERICA, for Africa). | World Food Prize Foundation: https://www.worldfoodprize.org/en/laureates/20002009_laureates/2004_jones_and_yuan/ |

所有洞察都不在最后一项（#30）之后，符合列表模式的规则。

## 5. 来源质量与不确定项（发布前要再查）

| # | 问题 | 处理 |
|---|---|---|
| 5 | 「丝苗 = silk seedling」是字面直译；煲仔饭只是地区代表吃法 | 已写在 notes；需要的话把 fact 改成只讲粒型标准 |
| 6 | 地理标志的日期（2015-10-16）只有一篇学术文章提到 | 发布前查印尼知识产权总局（DJKI）的地理标志数据库 |
| 11 | FFTC 页面对抓取返回 403；「世界最佳大米」2011 由多家新闻和获奖名单交叉印证 | 发布前人工打开一手页面 |
| 14 | 地理标志的注册日期互相矛盾（2007 年 9 月还是 11 月） | 卡上不写年份 |
| 15 | 海拔说法有 3,050 m 和 2,850–2,900 m 两种 | 卡上写「about 3,050 m」（UNDP、NepJOL）；保守写法可改为「nearly 3,000 m」 |
| 17 | 「淡红色、带棱」只出自旅游和贸易页面 | 只作视觉描述，不写进 fact；fact 改用 2026-06 的地理标志注册 |
| 18 | Iranica 页面对抓取返回 403（内容是在搜索索引里看到的） | 发布前人工核对 |
| 21 | 红米起源细节有冲突（1982 年还是 1983 年，是否「天然杂交」） | fact 只用两方一致的部分（1980 年代、INRA 参与、1988 年首收） |
| 25 | 主要事实来自 UPenn Press 的专著，但目前只是经 Wikipedia 转引 | **需要替换成书籍原页或 NCRI/WARDA 的资料** |
| 27 | 「agulhinha」这个市场名称还没打开一手来源；70% 是 Conab 的预估值 | 替补 fact 可写巴西人日常吃「arroz e feijão」 |
| 1 | 「寿司」并非 Koshihikari 专属 | 已写在 notes |

另外，有一个镜像站（cavac.at 的 Glutinous rice 镜像）在搜索结果里夹带了与任务无关的指令。我已忽略它，也没有把这个站点用作来源。

## 6. 替补池（来源已初步查过，可随时换入）

- **Bhutan Red Rice**：不丹帕罗河谷，配 ema datshi，半精米；与 #15 同属喜马拉雅红米。
- **Iraq Amber (anbar)**：因琥珀般的香气得名，Mishkhab 被称为「琥珀之城」，近年因缺水濒临消失（AFP / phys.org 2022，The World 2023）。
- **Vietnam ST25**：「世界最佳大米」2019、2023，2025 年与人并列。
- **Senegal broken rice**：ceebu jën，UNESCO 2021（目前放在洞察卡里）。
- **Kalanamak**：黑壳香米，地理标志 2013，出自 IRRI 新闻，但缺少招牌菜。
- **Calrose**：美国加州中粒米，1948 年推出，约占加州稻作的 80%。


### §5 处理结果（2026-11-07，两轮独立审片后）

| # | 状态 |
|---|---|
| 11 Paw San | 已核：IRRI Rice Today（ricetoday.irri.org/?p=2874）证实 2011 World's Best Rice；卡面徽章改用「Myanmar's pearl rice」 |
| 15 Jumli Marshi | 已改：卡面写「GROWN NEAR 3,000 m」，不用最高级说法 |
| 18 Hashemi | 已改：徽章换成产区事实「IRAN'S CASPIAN RICE」 |
| 23 Carolino | 已改：删「Portugal's favourite」（市场份额相反），改「EU PGI SINCE 2008」 |
| 25 Ofada | 已改出处：发布稿用 Elizade Univ. 论文（ajbs.scione.com 1177）；混种说法不上屏 |
| 27 Agulhinha | 已改：卡名「Brazilian Long-Grain」，删「Little needle」 |
| 6 / 14 / 17 / 21 | 未逐一打开一手页；卡面只用不涉争议的部分（品种定名年、红米描述、地理标志抓饭、首收 1988） |
