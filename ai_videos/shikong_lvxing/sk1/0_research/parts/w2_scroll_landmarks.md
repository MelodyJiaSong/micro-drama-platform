---
worker_id: W2_scroll_landmarks
stage: 0
role: researcher
angle: 图像地标
status: complete
blockers: []
confidence: high
facts_total: 48
facts_ai_read: 45
facts_ai_draft: 3
ref_images_total: 94
---

# W2 · 《清明上河图》与汴京城市空间 + 场景参考图库

> 摹本纪律：只有北京故宫藏张择端北宋原本是 T0 图像；明仇英本 / 苏州片、清院本（台北故宫）、Met 11.170 / 47.18.1 均为明清人画，建筑服饰**不作北宋依据**，tag 最高 ⚠️，`use` 注明「摹本，仅作构图/气氛参考」。
> `verified_by` 取值：`ai_read` ＝ 本 worker 打开过原文页 / 原图并逐字核过 quote；`ai_draft` ＝ 只见过检索摘要，**不得进 prompt**，待人眼核原页后改 tag。
> 原文引自维基文库《東京夢華錄》（繁体，逐字），故宫官网藏品页，唐寰澄《〈清明上河图〉上汴水贯木拱虹桥》（凤凰网转载）。

---

## §2 城市地图与街区 · 地标细节

### 2a 虹桥（bg1）

```yaml
- fact_id: kaifeng.bridge.001
  claim: 汴河虹桥无柱，整桥以巨木虚架成拱，饰以丹雘（朱红漆），形如飞虹
  tag: ✅
  source: 《東京夢華錄》卷一「河道」
  quote: "從東水門外七里曰虹橋，其橋無柱，皆以巨木虛架，飾以丹雘，宛如飛虹，其上下土橋亦如之"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一座没有桥墩的单孔木拱桥横跨浑黄的汴河，整座桥由粗大原木交叠架成拱形，木料表面涂着已经褪色的朱红漆，桥身像一道弯弓从两岸土坡拱起"
  negative: "石拱桥、石桥墩、砖券、石栏板、多孔桥、水泥、廊屋顶盖、灯笼串、汉白玉栏杆"

- fact_id: kaifeng.bridge.002
  claim: 虹桥位于东水门外七里的汴河上，是汴河上十三桥中最东的一座；城内上、下土桥同为无柱木拱
  tag: ✅
  source: 《東京夢華錄》卷一「河道」
  quote: "自東水門外七里至西水門外，河上有橋十三：從東水門外七里曰虹橋……次曰順成倉橋，入水門裏曰便橋，次曰下土橋，次曰上土橋"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "桥在城外，两岸是汴河码头与临河店铺，远处看不见城墙，只有柳树、茅棚和货船"
  negative: "桥紧贴城门、桥连着宫墙、御街牌坊"

- fact_id: kaifeng.bridge.003
  claim: 虹桥为贯木拱结构：两套拱骨系统交叠（第一系统 10 组、第二系统 11 组）、其间 5 道横梁；横梁上承纵梁，纵梁上铺木板为桥面
  tag: ✅
  source: 唐寰澄《〈清明上河图〉上汴水贯木拱虹桥》（故宫博物院研究文 / 凤凰网国学转载）
  quote: "汴水虹桥式木拱桥的主拱结构一般由两个系统组成……整座桥的承重结构共由11组第二系统和10组第一系统的拱骨组成……第一和第二系统之间设置有5道横梁……横梁上承纵梁，纵梁上铺木板为桥面"
  source_url: https://iguoxue.ifeng.com/57387951/news.shtml
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "从桥下仰看，桥拱由两层交错的原木拱骨编织而成，每根原木都是整根圆木，拱骨之间用横木穿插锁住，木纹粗糙，接缝处有木楔与藤绳捆扎痕迹"
  negative: "钢索、螺栓、铁架、光滑刨面木板、胶合板、拱下有柱"

- fact_id: kaifeng.bridge.004
  claim: 依画推算虹桥长约 21 m、宽约 7.8 m、拱顶距水面约 5 m
  tag: ⚠️
  source: 唐寰澄（同上，数值系按画中比例推算，非实测）
  quote: "据此可知此桥长约21m……桥宽大约为7.8 m……该桥拱顶距水面约5m"
  source_url: https://iguoxue.ifeng.com/57387951/news.shtml
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "桥跨约二十米、桥面宽约八米，拱顶离水面约五米，一艘带桅杆的货船放倒桅杆后勉强能从桥下通过"
  negative: "巨型跨河大桥、桥高数十米、小溪独木桥"

- fact_id: kaifeng.bridge.005
  claim: 虹桥桥面两侧立木构栏杆，栏柱间距约 1 m
  tag: ✅
  source: 唐寰澄（同上）+ 北宋原本虹桥局部（bg1 ref01 亲眼核）
  quote: "桥面两边立木构栏杆；每两根栏柱间距约1m"
  source_url: https://iguoxue.ifeng.com/57387951/news.shtml
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "桥面两侧是简朴的木栏杆，方形木栏柱每隔一米一根，柱间横穿两道细木栏，没有雕花"
  negative: "石雕栏板、望柱狮子、金属护栏、雕龙栏杆"

- fact_id: kaifeng.bridge.006
  claim: 桥上车马来往如梭、商贩密集、行人熙攘；摊贩带席棚与大伞沿桥两侧排开
  tag: ✅
  source: 故宫博物院藏品页「张择端清明上河图卷」+ 北宋原本虹桥局部（bg1 ref01 亲眼核：桥两侧有席棚摊、圆形大伞、挑担与驴）
  quote: "桥上车马来往如梭，商贩密集，行人熙攘。桥下一艘漕船正放倒桅杆欲穿过桥孔"
  source_url: https://www.dpm.org.cn/collection/paint/228226.html
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "桥面两侧挤满小摊，摊上支着芦席凉棚和竹骨油纸大伞，摊贩蹲在货筐后，中间只留一条窄道，挑担的脚夫、牵驴的、抬轿的在人缝里挤着走"
  negative: "空荡的桥面、现代广告牌、塑料布、电灯、汽车"

- fact_id: kaifeng.bridge.007
  claim: 虹桥两端桥头各立一对高木杆，杆顶有横木与鸟形物（学界多称「表木／华表，顶立仙鹤或风向鸟」）
  tag: ⚠️
  source: 北宋原本虹桥局部（bg1 ref01 亲眼核：桥头左岸可见高木杆、顶端小鸟形，横木呈十字）；「仙鹤／风向标」的功能解释未找到可引原文
  quote: "（图像观察）桥头高木杆顶端立一鸟形物，杆上有横木交叉"
  source_url: https://commons.wikimedia.org/wiki/File:Along_the_River_During_the_Qingming_Festival_(detail_of_original).jpg
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "桥头土坡两边各立着一根比屋檐还高的木杆，杆顶横着一根短木、木上立着一只木雕的鸟，杆身斑驳"
  negative: "石雕华表、龙柱、旗杆挂旗、路灯"

- fact_id: kaifeng.bridge.008
  claim: 画中木拱桥究竟是「虹桥」还是城内「上土桥」有分歧：故宫官网称其正名上土桥，多数研究与《东京梦华录》地望对应称虹桥
  tag: ⚠️
  source: 故宫博物院藏品页 vs 《東京夢華錄》卷一
  quote: "中段以'上土桥'为中心……规模宏敞、状如飞虹的木结构桥梁……正名'上土桥'"
  source_url: https://www.dpm.org.cn/collection/paint/228226.html
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.bridge.009
  claim: 金明池仙桥「骆驼虹」：桥面三段拱起、朱漆栏楯、下排雁柱——北宋汴京木桥通用朱漆栏杆的旁证
  tag: ✅
  source: 《東京夢華錄》卷七「三月一日開金明池瓊林苑」
  quote: "乃仙橋，南北約數百步，橋面三虹，朱漆闌楯，下排雁柱，中央隆起，謂之『駱駝虹』，若飛虹之狀"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "桥栏与拱骨外露木面涂朱红漆，日晒雨淋后颜色发暗发旧，露出木色"
  negative: "全新鲜红油漆、金漆、彩绘图案"
```

### 2b 城门与城墙（bg2）

```yaml
- fact_id: kaifeng.gate.001
  claim: 外城城门皆三层瓮城、屈曲开门；只有南薰、新郑、新宋、封丘四座正门是直门两重（留御路）
  tag: ✅
  source: 《東京夢華錄》卷一「東都外城」
  quote: "城門皆甕城三層，屈曲開門；唯南薰門、新鄭門、新宋門、封丘門皆直門兩重，蓋此係四正門，皆留御路故也"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "外城城门外套着弯折的瓮城，进城要拐两道弯才到正门"
  negative: "一门直通、无瓮城的城门（外城正门除外）、欧洲吊桥、城门口铁栅"

- fact_id: kaifeng.gate.002
  claim: 东水门是汴河下游水门：门跨河而建，有铁裹的闸门夜间垂到水面；两岸各有旱门供行人；门外拐子城夹岸百余丈
  tag: ✅
  source: 《東京夢華錄》卷一「東都外城」
  quote: "東南曰東水門，乃汴河下流水門也，其門跨河，有鐵裹窗門，遇夜如閘垂下水面，兩岸各有門通人行路，出拐子城，夾岸百餘丈"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "水门横跨汴河，门洞上方悬着一扇包铁皮的木栅闸门，白天吊起，河两岸各开一座旱门走人，门外两侧夯土墙夹着河道向东伸出去很远"
  negative: "石拱水关、铁链吊桥、现代水闸、混凝土"

- fact_id: kaifeng.gate.003
  claim: 外城每百步设马面、战棚，密置女头（女墙）；城壕护龙河宽十余丈，壕内外植杨柳，粉墙朱户
  tag: ✅
  source: 《東京夢華錄》卷一「東都外城」
  quote: "城壕曰護龍河，闊十餘丈，濠之內外，皆植楊柳，粉牆朱戶，禁人往來……新城每百步設馬面、戰棚，密置女頭，旦暮修整，望之聳然"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城墙外是宽阔的护城河，河两岸种满垂柳；城墙每隔一段凸出一个马面墩台，墩台上搭着木板战棚，墙头一排齐整的女墙垛口"
  negative: "护城河干涸、无柳、城墙光秃无马面、欧式塔楼、砖砌雉堞过密"

- fact_id: kaifeng.gate.004
  claim: 考古实测外城为夯土版筑：周长约 29180 m（合宋里五十余里），城门 12、水门 6；墙体上窄下宽，现存顶宽约 4 m、底宽约 34 m、高约 8.7 m；瓮城有方形与马蹄形；护城壕宽约 40 m
  tag: ✅
  source: 开封北宋东京城遗址考古（多家转述，数据一致）
  quote: "外城墙系用夯土版筑而成，现存顶部宽4米、底部宽达34.2米、高8.7米……周长计29180米……外城有城门12座、水门6座……瓮城有方形和马蹄形两种。城墙外的护城壕宽约40米"
  source_url: https://baike.baidu.com/item/北宋东京城遗址/7863519
  tier: T1
  verified_by: ai_draft
  used_in: []
  prompt_string: "城墙是夯土筑成，土黄色墙面有一层层水平夯层的横纹，墙体下宽上窄呈梯形，厚得像一道土山"
  negative: "青砖包砌的整面城墙（外城）、灰砖到顶、白色石墙"

- fact_id: kaifeng.gate.005
  claim: 内城景龙门（崇宁年间李诫主持重修）考古为一门三道、通阔约 60 m、门道各宽约 5.6 m、进深约 19.3 m，城门及墩台包砖、逐层错缝内收——北宋晚期官式城门可以包砖
  tag: ✅
  source: 新华网「河南开封首次发现北宋东京城内城城门」2024-07-12
  quote: "景龙门为一门三道式布局，城门主体由墩台、隔墙及门道构成……城门通阔约60米，门道进深约19.3米……三门道宽度相同，均约5.6米……城门及墩台包砖，逐层错缝露龈内收"
  source_url: http://www.news.cn/local/20240712/359b81b8ad3a46e99c49a5bc27346c6b/c.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "城门墩台外表包一层青灰砖，砖缝错开，墩台自下而上微微内收"
  negative: "钢筋、水泥勾缝、红砖、瓷砖"

- fact_id: kaifeng.gate.006
  claim: 画中城门：高大夯土城台（土色、素面）、单个门洞、台顶木构城楼（歇山顶、斗拱、四周平坐栏杆、朱橙色木作）、两侧带栏杆的斜坡马道；楼上只有一人，城头无女墙、无守卫，驼队直接穿门
  tag: ✅
  source: 北宋原本城门局部（bg2 ref01 亲眼核）
  quote: "（图像观察）夯土城台斜壁素面无砖纹；门洞一个；城楼单层带平坐、檐下斗拱、朱橙色柱枋；台顶无垛口；两峰骆驼正出门洞，门内外无兵"
  source_url: https://commons.wikimedia.org/wiki/File:Bianjing_city_gate.JPG
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一座土黄色的夯土城台，斜面素净没有砖，中间一个方形门洞；台顶立着一座木构城楼，歇山灰瓦顶，檐下一排斗拱，四周围着朱橙色木栏杆的平坐，两侧各有一道带木栏杆的斜坡马道通到台顶；城头没有垛口也没有士兵，一队驮货的骆驼正从门洞走出"
  negative: "砖砌雉堞、瓮城箭楼（画中不见）、明清式三重檐城楼、红色宫墙、卫兵列队、灯笼、牌匾大字"

- fact_id: kaifeng.gate.007
  claim: 外城门内外的「牙道」两侧植榆柳成荫；每二百步一座防城库
  tag: ✅
  source: 《東京夢華錄》卷一「東都外城」
  quote: "城裏牙道，各植榆柳成陰。每二百步置一防城庫，貯守禦之器"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城墙内侧的顺城路两旁种着一排排榆树和柳树，树荫遮住土墙根"
  negative: "梧桐、银杏行道树、路灯、柏油路"
```

### 2c 州桥（bg4）

```yaml
- fact_id: kaifeng.zhouqiao.001
  claim: 州桥正名天汉桥，正对大内御街；桥低平不通舟船，唯平底小船可过；桥柱皆青石，石梁、石笋、楯栏；近桥两岸皆石壁，雕海马水兽飞云；桥下密排石柱
  tag: ✅
  source: 《東京夢華錄》卷一「河道」
  quote: "次曰州橋（正名天漢橋），正對於大內御街，其橋與相國寺橋皆低平不通舟船，唯西河平船可過，其柱皆青石為之，石梁石筍楯欄。近橋兩岸，皆石壁，雕鐫海馬水獸飛雲之狀。橋下密排石柱，蓋車駕御路也"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一座低平的青石梁桥横过汴河，桥下密密排着青石方柱，桥面两侧是石栏杆；桥两岸的河堤是整面青石壁，石壁上浮雕着海马、水兽和飞云"
  negative: "高拱石桥、木桥、砖券、汉白玉、现代栏杆、河堤是土坡"

- fact_id: kaifeng.zhouqiao.002
  claim: 2018–2022 年河南省文物考古研究院与开封市文物考古研究所（今开封市文物考古研究院）持续发掘州桥遗址。桥东汴河两岸的宋代堤岸石壁上出土北宋石雕祥瑞壁画：「海马瑞兽」像马又像鹿、偶蹄、头部腿部有鬃毛，昂首嘶鸣、四蹄奔腾；一前一后两只禽鹤引颈飞翔；四周祥云环绕。图案通高约 3.3 m，总长各报道不一（25 m／推测约 30 m），被称为国内已发现体量最大的北宋石刻壁画。现存州桥是明代早期在宋代州桥桥基上建成的单孔砖券石板拱桥：考古队推测宋桥不通大船，所以改建，改建时保留了近桥两岸的宋代石壁。北宋那座低平石桥的桥身已经不在
  tag: ✅
  source: 王三营（开封市文物考古研究院）《考古重现北宋东京州桥》（新华网 2023-02-13）＋ 张野《开封州桥文化旅游开发的构想》（河南省文化和旅游厅网站 2023-04-07）＋ China Daily 2022-09-29 ＋ 河南省人民政府英文网 2022-09-28 ＋ 新华网 2026-04-06
  quote: "一匹海马瑞兽形象逐渐完整清晰。瑞兽像马又像鹿，偶蹄，头部、腿部有鬃毛，独角，身体健硕，呈昂首嘶鸣、四蹄奔腾状，一前一后两只禽鹤引颈飞翔，周围祥云环绕。石刻图案上下通高约3.3米" / "出土的州桥应为明代重建过的州桥" / "因宋代州桥不能通行大型舟船，推测当时对其进行了改建，但保留了近桥两岸宋代石壁"（新华网 2023）；"州桥石壁则是目前国内发现的北宋时期体量最大的石刻壁画" / "现存开封州桥为明代早期所修建，是在宋代州桥桥基基础上建造的单孔砖券石板拱桥。"（河南省文旅厅 2023）；"3.3 meters high and altogether 30 meters long, showing patterns of mythical sea beasts, cranes and clouds" / "the extant bridge was rebuilt on the abutment of the Song bridge in the early Ming Dynasty"（China Daily）；"reliefs of sea horses, auspicious beasts, cranes and auspicious clouds with an average height of 3.3 meters and a total length of 25 meters"（henan.gov.cn）；"2018年至2022年，河南省文物考古研究院联合开封市文物考古研究所（现'开封市文物考古研究院'）对州桥遗址开展持续性考古发掘，并出土北宋时期巨幅石雕祥瑞壁画。"（新华网 2026）
  source_url:
    - http://www.news.cn/culture/20230213/5d258763114b46fa84b6fc98f657c805/c.html
    - https://hct.henan.gov.cn/2023/04-07/2720923.html
    - https://www.chinadaily.com.cn/a/202209/29/WS6334f28fa310fd2b29e7a59e.html
    - https://english.henan.gov.cn/2022/09-28/2614829.html
    - https://www.news.cn/local/20260406/07652a19b0874253869119f03752f1db/c.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（今日遗址镜用）考古坑深处露出一整面青灰色大条石砌成的河岸石壁，石面上是连续的浅浮雕长卷：一匹像马又像鹿、昂首四蹄腾空的瑞兽，前后两只伸长脖子飞翔的鹤，四周布满卷曲的云纹；浮雕整体高过两个成年人；石壁旁是一座青砖拱券的单孔桥体"
  negative: "彩绘浮雕、汉白玉、龙纹凤纹、石狮、完整的北宋平桥桥身、把明代砖券拱桥当北宋州桥、水泥堤岸、可读文字标牌"
  note: 2026-09-14 W12_factfix 更正并升为 ai_read。原 quote 标称出自 news.cn 2022-09-28「城摞城」稿，但在该页上没有逐字找到；该页只写了「宋代堤岸石雕祥瑞壁画保存较好，构成巨幅长卷」「明代州桥结构基本完整，青石铺筑桥面，砖砌拱券」，所以换成上面五个已核来源。「瑞兽」不是另一种动物，指的就是那匹像马又像鹿的「海马瑞兽」。角的形状各报道写法不一（新华网 2023 作「独角」，中新网 2022-10-25 https://www.chinanews.com.cn/cul/2022/10-25/9879460.shtml 作「头上长着鹿角，腿后有翅膀」），画面不要特写角。总长数字各家也不一，口播不报长度，只能说「高三米多」。与 zhouqiao.001（《梦华录》「海馬水獸飛雲」）互证：文献记的是北宋当年所见，本条是今天挖出来的实物。遗址今天的开放状态见 zhouqiao.004 / 005。

- fact_id: kaifeng.zhouqiao.003
  claim: 州桥北岸御路两侧东西两阙楼观对耸；桥西泊两艘方浅船装铁枪，岸上三条铁索夜间绞起拦河
  tag: ✅
  source: 《東京夢華錄》卷一「河道」
  quote: "州橋之北岸御路，東西兩闕，樓觀對聳；橋之西有方淺舡二隻，頭置巨杆鐵鎗數條，岸上有鐵索三條，遇夜絞上水面，蓋防遺失舟船矣"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "桥北岸御路两边各立一座高耸的阙楼；桥西河面停着两艘方头浅船，船头竖着几根装铁枪头的长杆，岸边卧着三条粗铁索"
  negative: "牌坊、石狮、现代路灯"

- fact_id: kaifeng.zhouqiao.004
  claim: 州桥遗址今天是一处边发掘边展示、可以站在探方边参观的考古现场。2018–2022 年持续发掘；桥面距今天地表最浅约 4.3 m。2020 年 9 月 28 日「州桥及汴河遗址公众考古研学示范基地」临展馆对外开放，此后按发掘进度安排市民免费参加公众考古开放日。到 2026 年 4 月，新华网仍报道示范基地「建成开放」，孩子们来到「考古探方边」
  tag: ✅
  source: 中国文化报 陈关超、张莹莹《河南开封：被李自成灌没的州桥正在归来》（中国社会科学网转载）＋ 开封日报·掌上开封《重磅！州桥及汴河遗址对外开放！》（澎湃号 2020-09-30）＋ 新华网 李俊、袁月明（2026-04-06）＋ zh.wikipedia「州桥」
  quote: "今年9月28日，州桥及汴河遗址公众考古研学示范基地就对外开放了，基地根据遗址发掘的进度，安排市民免费参与公众考古开放日活动" / "桥面距地表最浅4.3米"（中国文化报）；"9月28日，州桥及汴河遗址公众考古研学示范基地临展馆正式对外开放！" / "层层叠压的地层剖面清晰可见"（掌上开封 2020-09-30）；"随着州桥及汴河遗址公众考古研学示范基地建成开放，越来越多的孩子们来到考古探方边，感悟千年风雅。"（新华网 2026-04-06）；"开放参观的考古探方"（zh.wikipedia）
  source_url:
    - https://cssn.cn/kgxc/kgxc_kgsb/202207/t20220728_5431534.shtml
    - https://m.thepaper.cn/newsDetail_forward_9418866
    - https://www.news.cn/local/20260406/07652a19b0874253869119f03752f1db/c.html
    - https://zh.wikipedia.org/zh-hans/州桥
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: "（今日遗址镜用）现代城市街区地面下挖开一片很深的方形考古发掘区，坑壁是一层层叠压的土层剖面，坑底露出河岸石壁和砖拱桥体；坑边站着来参观的市民和孩子，低头往下看"
  negative: "游客在坑底行走触摸石壁、仿古复原的州桥楼阁、景区大门牌坊、可读文字标牌"
  note: 2026-09-14 W12_factfix 新增（回应 R6 F04）。发掘起止年用新华网 2026 与 China Daily 的「2018–2022」。州桥本体发掘 2020 年 3 月启动、汴河段 2018 年 10 月启动，这两个日期只见于检索摘要 ⚠️，口播不报月份。报道标题里「被李自成灌没」的决河责任本次没有核史料 ⚠️，口播不要点名是谁决的河。与 city.024（2018-05「仍深埋」）的关系见该条 note。

- fact_id: kaifeng.zhouqiao.005
  claim: 遗址上方有没有保护棚、遗址博物馆有没有建成，本次没有查到确证。2020 年中国文化报只写了远期规划建「汴河州桥遗址博物馆」（地下展厅＋地上仿建州桥）；2023 年河南省文旅厅网站的文章仍是「构想」；2026 年新华网只写示范基地「建成开放」、孩子们来到「考古探方边」
  tag: ⚠️
  source: 本 worker 综合（zhouqiao.004 各来源 ＋ hct.henan.gov.cn 2023-04-07）
  source_url: https://hct.henan.gov.cn/2023/04-07/2720923.html
  tier: T3
  verified_by: ai_draft
  quote: "—"
  used_in: []
  prompt_string: "（不得进 prompt）"
  negative: "—"
  note: 判断：今日遗址镜不写保护棚的形制、博物馆展厅、玻璃地板这类具体设施（有没有都不确定），只拍探方、石壁和坑边参观的人；口播不说「建了博物馆」。People's Daily 2022-09-29 版面页返回 403，newsduan 2024-08-21、人民网 2023-08-14 两篇讲开放参观的稿子也被拦，都没能打开，补查时从这几篇入手。
```

## §5 住 · 沿街建筑形制（bg5 / bg6 / bg7）

```yaml
- fact_id: kaifeng.shop.001
  claim: 京师所有酒店门首都缚扎「彩楼欢门」
  tag: ✅
  source: 《東京夢華錄》卷二「酒樓」+ 北宋原本虹桥左岸脚店（bg1 ref01 亲眼核：门前有木杆缚扎的多层彩楼骨架）
  quote: "凡京師酒店，門首皆縛綵樓歡門"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "酒楼门口用长木杆绑扎出一座三层楼高的镂空彩楼门架，木杆上缠着彩色绸帛和花结，顶上斜插几面小旗，门架比店面本身还高"
  negative: "石牌坊、霓虹灯、气球拱门、红灯笼串、玻璃门"

- fact_id: kaifeng.shop.002
  claim: 在京正店七十二户，其余都叫脚店；正店自酿酒、脚店从正店批酒零卖
  tag: ✅
  source: 《東京夢華錄》卷二「酒樓」
  quote: "在京正店七十二戶，此外不能遍數，其餘皆謂之『腳店』"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "招牌上写着「正店」两字的是有酿酒权的大酒楼，门前叠放着一排排大木箍酒桶；写「脚店」的是小酒铺"
  negative: "「酒吧」「饭店」「客栈」现代招牌字、简体字"
  note: 2026-09-14 SYNC_sk1（回应 R6 I04）：quote 只证明「在京正店七十二户、其余叫脚店」，claim 里「正店自酿酒」这半句不在 quote 里；「脚店从正店打酒」由 food.026 的原文支撑（shot05 同镜引用）。shot05 口播「自己能酿酒的就这七十二家」暂按本条 claim；补上酿酒权的原文 quote（或改由带原文的条目承担）之前，不要再加新的酿酒权说法。本次网络不通，未补 quote，id 不变。

- fact_id: kaifeng.shop.003
  claim: 九桥门街市酒店彩楼相对、绣旆相招、遮蔽天日；豐樂樓三层五楼相向、飞桥栏槛
  tag: ✅
  source: 《東京夢華錄》卷二「酒樓」
  quote: "九橋門街市酒店，彩樓相對，繡旆相招，掩翳天日……更修三層相高。五樓相向，各有飛橋欄檻，明暗相通，珠簾繡額，燈燭晃耀"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "街两边的酒楼彩楼门架对着彩楼门架，绣着字的长条酒旗从楼上垂下来，几乎把街上的天遮住；大酒楼二层临街一排木窗全开着，窗里坐着酒客"
  negative: "单层平房酒馆、玻璃窗、卷帘门、马赛克"

- fact_id: kaifeng.shop.004
  claim: 画中可辨招牌：「孙羊正店」（另有「正店」「香醪」牌）、「十千脚店」、「香饮子」（大伞小摊）、「刘家上色沉檀拣香」（竖招，门前有牌楼）、「赵太丞家」（三进院医铺，立招「大理中丸医肠胃冷」「治酒所伤真方集香丸」，条匾「五劳七伤调理科」）、「杨家应症」
  tag: ✅
  source: 《中国医药报》「《清明上河图》中的医药图像」2019-10-31（医铺与香铺，ai_read）+ 知乎「清明上河图里都有哪些店铺」（孙羊正店/十千脚店/香饮子，仅见摘要）
  quote: "一为'大理中丸医肠胃冷'，一为'治酒所伤真方集香丸'……其后一大立招似乎是'赵太丞家理男妇儿科'，左侧门脸条匾'五劳七伤调理科'……医铺有三进院落……竖立的招牌上写着'刘家上色沉檀樟香'……门前有牌楼"
  source_url: http://bk.cnpharm.com/zgyyb/2019/10/31/app_240318.html
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: "店门口竖着一块高过人头的木立招，招牌是竖写的墨字；门脸横挂一块窄条木匾；小摊只撑一把大伞、伞下挂一块小木牌"
  negative: "画面里让模型自己写字（招牌文字须用核对过的真实字样或留空/无意义纹样）、简体字、印刷体、灯箱、横幅"

- fact_id: kaifeng.shop.005
  claim: 潘楼街「界身」巷为金银彩帛交易之所，屋宇雄壮、门面广阔；潘楼下每日五更开市
  tag: ✅
  source: 《東京夢華錄》卷二「東角樓街巷」
  quote: "南通一巷，謂之「界身」，並是金銀綵帛交易之所。屋宇雄壯，門面廣闊，望之森然。每一交易，動即千萬"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "商业大街两侧是开间宽阔的两层木构铺面，木板门整扇卸下，柜台朝街，屋檐下挂着布幌"
  negative: "石库门、西式拱廊、玻璃橱窗"

- fact_id: kaifeng.shop.006
  claim: 桑家瓦子、中瓦、里瓦有大小勾栏五十余座，莲花棚、牡丹棚、夜叉棚、象棚最大可容数千人；瓦子里还有卖药、卖卦、喝故衣、探搏、饮食、剃剪、纸画、令曲
  tag: ✅
  source: 《東京夢華錄》卷二「東角樓街巷」
  quote: "街南桑家瓦子，近北則中瓦，次裡瓦。其中大小勾欄五十餘座。內中瓦子蓮花棚、牡丹棚；裡瓦子夜叉棚、象棚最大，可容數千人……瓦中多有貨藥、賣卦、喝故衣、探搏、飲食、剃剪、紙畫、令曲之類。終日居此，不覺抵暮"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一片用木栅栏和芦席围起来的露天演艺场，里面用木杆搭着一座座带席顶的看棚，棚口挂着写字的布招子，棚外挤着卖药、算卦、剃头、卖旧衣的小摊，人声嘈杂"
  negative: "砖砌剧院、戏台飞檐彩绘（明清戏台）、红灯笼、观众席座椅、舞台灯光"

- fact_id: kaifeng.shop.007
  claim: 望火楼建在高处、砖砌，楼上有人瞭望，楼下官屋数间驻兵百余并存救火器具；每坊巷三百步一军巡铺，铺兵五人
  tag: ✅
  source: 《東京夢華錄》卷三「防火」
  quote: "每坊巷三百步許，有軍巡鋪屋一所，鋪兵五人……又於高處磚砌望火樓，樓上有人卓望。下有官屋數間，屯駐軍兵百餘人，及有救火家事，謂如大小桶、酒子、麻搭、斧鋸、梯子、火叉、大索、鐵貓兒之類"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "街角一座砖砌的方形高台，台顶一间小木亭，亭里站着一个瞭望的兵；台下几间灰瓦官屋，墙边靠着水桶、长梯、火叉和粗麻绳"
  negative: "钟楼、鼓楼、教堂尖塔、消防车、红色消防栓"

- fact_id: kaifeng.house.013
  claim: 画卷首段郊野「茅檐低伏，阡陌纵横」；后段市区「商店鳞次栉比」；宋人所见建筑从小屋到有宽敞前后院的豪宅不等
  tag: ✅
  source: 故宫博物院藏品页 + 中文维基「清明上河圖」
  quote: "首段……茅檐低伏，阡陌纵横，其间人物往来……后段……市区街道，城内商店鳞次栉比"；"私人住宅和各種風格、宏偉程度不一的官方建築，自小屋到有著寬敞前後院的豪宅不等"
  source_url: https://www.dpm.org.cn/collection/paint/228226.html
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "巷子里的民居是低矮的木架房，屋顶盖灰色板瓦，屋脊平直不起翘，土坯或编竹抹泥的墙刷成白灰色，窗是直棂木窗，门是两扇木板门；城外的农舍则是茅草顶、篱笆院"
  negative: "马头墙、白墙黛瓦徽派、四合院垂花门、琉璃瓦、飞檐翘角过甚、玻璃窗、红砖"

- fact_id: kaifeng.house.014
  claim: 北宋原本城门内外沿街建筑：灰瓦悬山／歇山顶、木柱直棂窗、席棚披檐、部分二层带栏杆；屋脊有简单鸱尾，无彩绘（bg2 ref01、bg1 ref01 亲眼核）
  tag: ✅
  source: 北宋原本局部图像观察
  quote: "（图像观察）临街店铺为单层或两层木构，灰瓦屋面，檐下加席棚披檐遮阳，木柱素色，二层临街有木栏杆"
  source_url: https://commons.wikimedia.org/wiki/File:Bianjing_city_gate.JPG
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "临街铺面木柱不上漆，灰瓦屋面前沿再搭出一截芦席披檐，遮住摊位；二层店铺临街有一圈木栏杆，栏杆里摆着桌凳"
  negative: "红柱金匾、彩画梁枋、琉璃瓦、卷棚顶、太阳伞"
```

## §6 行 · 车船桥（bg1 / bg3 / bg8）

```yaml
- fact_id: kaifeng.boat.001
  claim: 汴河从洛口分水入京、东至泗州入淮，东南漕粮与方物都由此入城，公私仰给
  tag: ✅
  source: 《東京夢華錄》卷一「河道」
  quote: "中曰汴河，自西京洛口分水入京城，東去至泗州，入淮。運東南之糧，凡東南方物，自此入京城，公私仰給焉"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "浑黄的汴河上一艘接一艘的漕船，船舱里堆着麻袋装的粮食，岸边码头上脚夫扛着米袋排队上岸"
  negative: "清澈碧绿的河水、海船、帆船竞赛、游艇"

- fact_id: kaifeng.boat.002
  claim: 画中共 28 艘船；河上有捕鱼船和载客渡船，河岸上有人拉着较大的船（纤夫）；全卷 814 人、60 只动物、30 座建筑、20 辆车、8 顶轿、170 棵树
  tag: ✅
  source: 中文维基「清明上河圖」
  quote: "畫中共有814個人物、28艘船、60隻動物、30座建築、20輛車輛、8輛轎子和170棵樹……河上擠滿了捕魚船和載客渡船，河岸邊的人們正在拉著較大的船隻"
  source_url: https://zh.wikipedia.org/wiki/清明上河圖
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "岸上五六个赤脚纤夫弯着腰，肩上斜挎粗麻纤绳，拉着河里一艘吃水很深的货船逆流缓行"
  negative: "机动船、螺旋桨、救生圈、纤夫穿现代衣服"

- fact_id: kaifeng.boat.003
  claim: 画中漕船：平底、船舷高、中部有带窗的舱棚、船尾有舵楼与长舵、单桅可放倒；过桥时放倒桅杆，水手持长篙撑船（bg1 ref01 亲眼核）
  tag: ✅
  source: 故宫博物院藏品页 + 北宋原本虹桥局部
  quote: "桥下一艘漕船正放倒桅杆欲穿过桥孔"；"（图像观察）船身宽平、舱面有席篷与木窗、船尾高起为舵楼、桅杆已放倒斜卧船上、船头水手持篙"
  source_url: https://www.dpm.org.cn/collection/paint/228226.html
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "一艘宽平的木壳漕船正从桥下穿过，桅杆已经放倒斜卧在舱棚上，船头两个水手撑着长竹篙顶住桥拱，船尾舵工死死扳着一根长木舵，船舷边站着人朝桥上喊"
  negative: "鼓满的风帆从桥下穿过、龙舟、乌篷小船、铁锚链、船体油漆鲜亮"

- fact_id: kaifeng.boat.004
  claim: 泉州湾出土宋代海船与画中内河漕船是两种船型；内河漕船尺度更小、无深龙骨
  tag: ⚠️
  source: 泉州湾宋代海船实物（Commons 图像）；仅作船体板缝、隔舱构造参考
  quote: "（图像）Song Dynasty Ancient Ship of Quanzhou Bay"
  source_url: https://commons.wikimedia.org/wiki/File:Song_Dynasty_Ancient_Ship_of_Quanzhou_Bay_20061229.jpg
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "把海船的多桅与尖底搬进汴河"

- fact_id: kaifeng.cart.001
  claim: 太平车：有箱无盖、箱如栏杆而平，驾车人在中间执鞭，前列骡驴二十余或牛五七头拽；两轮与箱齐高，车后有两斜木脚拖地，中悬铁铃行即有声；可载数十石
  tag: ✅
  source: 《東京夢華錄》卷三「般載雜賣」
  quote: "東京般載車，大者曰『太平』，上有箱無蓋，箱如構欄而平，板壁前出兩木，長二三尺許，駕車人在中間，兩手扶捉鞭裏駕之，前列騾或驢二十餘，前後作兩行；或牛五七頭拽之。車兩輪與箱齊，後有兩斜木腳拖夜；中間懸一鐵鈴，行即有聲……可載數十石"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一辆笨重的两轮大木车，车厢四周是低矮的木栏没有顶盖，两只大木轮和车厢一样高，前面几头黄牛并排拉着，车后拖着两根斜木脚，车下挂着一只铁铃"
  negative: "四轮马车、带篷马车、橡胶轮胎、辐条铁轮、欧式马车"

- fact_id: kaifeng.cart.002
  claim: 平头车：似太平车而小，两轮前出长辕，独牛在辕内项负横木，人牵牛鼻绳；正店多用它载酒梢桶（每梢约三斗，一贯五百文）；宅眷坐车子与平头车相似但棕作盖、前后有栏门垂帘
  tag: ✅
  source: 《東京夢華錄》卷三「般載雜賣」
  quote: "其次有『平頭車』，亦如『太平車』而小，兩輪前出長木作轅木，梢橫一木，以獨牛在轅內，項負橫木，人在一邊，以手牽牛鼻繩駕之，酒正店多以此載酒梢桶矣……又有宅眷坐車子，與『平頭車』大抵相似，但棕作蓋，及前後有構欄門，垂簾"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一头黄牛拉着一辆小两轮车，牛脖子上架着横木，车夫走在牛旁边牵着牛鼻绳，车上码着几只长木桶"
  negative: "马拉车、四轮、车夫坐在车上挥鞭"

- fact_id: kaifeng.cart.003
  claim: 串车：独轮车，前后二人把驾、两旁二人扶拐、前有驴拽，可载竹木瓦石；另有无前辕、一两人推的独轮车，多为卖糕人用；浪子车（平盘两轮人拽）、痴车（无轮拖巨石大木）；驼骡驴驮子用皮或竹匾筐搭于背上
  tag: ✅
  source: 《東京夢華錄》卷三「般載雜賣」
  quote: "又有獨輪車，前後二人把駕，兩旁兩人扶拐，前有驢拽，謂之『串車』，以不用耳子轉輪也。般載竹木瓦石。但無前轅，止一人或兩人推之。此畫往往賣糕及糕麋之類人用……又有駝騾驢馱子，或皮或竹為之，如方匾竹差，兩搭背上"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一辆载满货物的大独轮车，一个人在后面把着车把，前面一个人肩上套着绳拉，车前还拴着一头小毛驴帮着拽，车上货物用草席盖住、麻绳捆紧"
  negative: "自行车、手推购物车、金属独轮车、充气轮胎"

- fact_id: kaifeng.cart.004
  claim: 画中牲畜以驴为主、其次是牛，马很少；马是身份象征，运货载人主要靠驴、牛或人抬的轿
  tag: ✅
  source: 澎湃新闻「《清明上河图》中为什么马少驴多？」
  quote: "《清明上河图》还有200多只动物，大部分是驴，然后是牛，马很少……马是身份的象征。运货载人的交通工具，主要是驴、牛或人抬的轿子"
  source_url: https://www.thepaper.cn/newsDetail_forward_22153456
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: "街上来来往往的是灰褐色的小毛驴，驮着炭筐和布袋，赶驴人拿细棍走在旁边；牛拉车；骑马的只有个别穿长衫戴巾帽的人"
  negative: "满街高头大马、骑兵、马车队、骆驼以外的异域动物、宠物狗牵绳"

- fact_id: kaifeng.cart.005
  claim: 驼队进出城门：画中城门洞有驮货骆驼穿行（bg2 ref01 亲眼核，两峰）
  tag: ✅
  source: 北宋原本城门局部图像观察
  quote: "（图像观察）门洞内一峰双峰驼正出门，门外道上另有两峰驮着货囊"
  source_url: https://commons.wikimedia.org/wiki/File:Bianjing_city_gate.JPG
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "几峰驮着鼓鼓货囊的双峰骆驼排成一列，慢吞吞地穿过城门洞，牵驼人戴毡帽走在最前"
  negative: "单峰骆驼、沙漠背景、阿拉伯服饰"

- fact_id: kaifeng.cart.006
  claim: 清明日轿子顶上用杨柳杂花装簇、四面垂下遮映；都城人出郊上坟，携枣锢炊饼、名花异果，抵暮而归
  tag: ✅
  source: 《東京夢華錄》卷七「清明節」
  quote: "轎子即以楊柳雜花裝族頂上，四垂遮映。自此三日，皆出城上墳，但一百五日最盛"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一顶两人抬的小轿，轿顶上插满新折的柳枝和野花，枝条从四面垂下来把轿子遮住一半，轿后跟着骑驴的、挑食盒的"
  negative: "八抬大轿、红绸花轿、宫廷仪仗、塑料花"

- fact_id: kaifeng.cart.007
  claim: 清明「都城人出郊」「四野如市」，人们在树下园囿间摆杯盘互相劝酒，歌儿舞女遍满园亭；坊市卖稠饧、麦糕、乳酪、乳饼；「缓入都门，斜阳御柳」
  tag: ✅
  source: 《東京夢華錄》卷七「清明節」
  quote: "都城人出郊……士庶闐塞諸門，紙馬鋪皆於當街用紙袞疊成樓閣之狀。四野如市，往往就芳樹之下，或園囿之間，羅列杯盤，互相勸酬……節日坊市賣稠餳、麥糕、乳酪、乳餅之類。緩入都門，斜陽御柳"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "城外柳树刚发嫩芽的土路上，成群结队的人往郊外走，树下有人铺席摆开杯盘吃喝，纸马铺门口用彩纸叠成的楼阁堆在街边；傍晚人流又顺着夕阳下的柳堤慢慢回城"
  negative: "樱花、油菜花海、桃花漫山（可少量）、现代野餐垫、气球、风筝（画中无）"

- fact_id: kaifeng.street.001
  claim: 御街自宣德楼直南，阔二百余步，两侧御廊，黑漆杈子与路心两行朱漆杈子隔出御道，杈子内有砖石砌御沟两道，宣和间植莲荷、岸边桃李梨杏
  tag: ✅
  source: 《東京夢華錄》卷二「御街」（注意：画中不是御街，本条只供 bg4 州桥北望时的远景与「不要把画中街当御街」纠错）
  quote: "坊巷御街，自宣德樓一直南去，約闊二百餘步，兩邊乃御廊……各安立黑漆杈子，路心又安朱漆杈子兩行，中心御道，不得人馬行往，行人皆在廊下朱杈子之外。杈子裏有磚石甃砌御溝水兩道，宣和間盡植蓮荷，近岸植桃李梨杏"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "州桥北面是一条极宽的御街，路中间两排朱红木栅栏围出御道，栅栏外是两道砖砌水沟，沟里种着荷叶，沟岸一排桃树李树正开花，行人都走在两侧长廊下"
  negative: "石板铺的御街、华表、天安门式城楼、御街上摆摊（政和后已禁）"

- fact_id: kaifeng.street.002
  claim: 州桥南去至朱雀门一线夜市：当街水饭、爊肉、乾脯；旋煎羊白肠、鲊脯、冻鱼头、批切羊头、辣脚子、姜辣萝卜；「每个不过十五文」；直至三更
  tag: ✅
  source: 《東京夢華錄》卷二「州橋夜市」
  quote: "出朱雀門，直至龍津橋。自州橋南去，當街水飯、爊肉、乾脯……梅家鹿家鵝鴨雞免肚肺鱔魚包子、雞皮、腰腎、雞碎，每個不過十五文……至朱雀門，旋煎羊、白腸、鲊脯、黎凍魚頭、薑豉類子、抹臟、紅絲、批切羊頭、辣腳子、姜辣蘿蔔……直至三更"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "州桥往南的街心一溜小食摊，炭炉上煎着切段的羊肠，木案上摆着腌鱼干、切好的羊头肉、姜丝萝卜，粗陶碗和竹签，摊主吆喝"
  negative: "辣椒、红油、玉米、番茄、土豆、花生、塑料碗、烧烤铁签架"

- fact_id: kaifeng.street.003
  claim: 五更时市井已开：瓠羹店门口小儿叫卖、酒店点灯烛沽卖；杀猪羊作坊挑担或车子上市动辄百数；果子行在朱雀门外及州桥之西；卖麦面用太平车或驴马驮从城外守门入城
  tag: ✅
  source: 《東京夢華錄》卷三「天曉諸人入市」
  quote: "諸門橋市井已開，如瓠羹店門首坐一小兒，叫饒骨頭……其殺豬羊作坊，每人擔豬羊及車子上市，動即百數。如果木亦集於朱雀門外及州橋之西，謂之果子行……其賣麥麪……用太平車或驢馬馱之，從城外守門入城貨賣，至天明不絕"
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "天刚蒙蒙亮，州桥边的早市已经摆开：挑着整扇猪羊的屠户、堆满果筐的果子行摊位、驮着布袋麦面的驴队刚从城门进来，酒店门口点着灯烛卖粥饭"
  negative: "路灯、电灯、塑料筐、电子秤"

- fact_id: kaifeng.street.004
  claim: 画中街边有水井：井口方形木栏、几人打水（复制品翻拍局部 bg4 ref10；原本对应局部待核）
  tag: ⚠️
  source: Commons「Qingming shanghe tu well」（复制品翻拍）
  quote: "（图像）street well scene"
  source_url: https://commons.wikimedia.org/wiki/File:Qingming_shanghe_tu_well.jpg
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: "巷口一眼水井，井口围着方形木框，两个人用木桶和绳子打水"
  negative: "石雕井圈、辘轳架（画中未见）、水龙头"
```

## §14 未定与推测项（本角度）

```yaml
- fact_id: kaifeng.doubt.001
  claim: 画名「清明」是否指清明节：有「清明节」说、「清明坊」说、「清明之世（颂辞／讽谏）」说、「初秋景」说；中文维基记录邹身城（颂辞）、清明坊说、2013 年《后汉书》「清明之世」讽刺说，并记有研究认为画中场景是初秋
  tag: ⚠️
  source: 中文维基「清明上河圖」
  quote: "並且所描繪的場景是初秋。然而，另一些研究則反駁，認為畫中描繪的城市確實是汴京，但畫作所描繪的是中國農曆清明節的某一天……也有一種觀點認為「清明」指的是「清明坊」……此處的「清明」並非太陽節氣，而是來自《後漢書》中的詞語「清明之世」"
  source_url: https://zh.wikipedia.org/wiki/清明上河圖
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: 本站定调「清明日」来自《东京梦华录》卷七（T0），画作只作视觉参考、不作日期证据；口播时说「学界有争议」。

- fact_id: kaifeng.doubt.002
  claim: 画的地段是城外汴河（虹桥）到一座城门再进城内一段街市，**未画御街与大内**；画中城门究竟是外城东水门、内城旧宋门还是虚构，学界未定；故宫官网把桥定为「上土桥」（城内）与《东京梦华录》地望（虹桥在城外七里）冲突
  tag: ⚠️
  source: 故宫藏品页三段描述 + 《東京夢華錄》卷一
  quote: "首段……郊野……中段以'上土桥'为中心，另画汴河及两岸风光……后段……市区街道"
  source_url: https://www.dpm.org.cn/collection/paint/228226.html
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: 本站路线「虹桥（城外七里）→ 东水门 → 州桥」按《东京梦华录》地望走（合并编辑 2026-09-13 校正：原写「东水门 → 虹桥」与本文件 bridge.002 自相矛盾）；画中城门只借形制（gate.006），不宣称它就是东水门。

- fact_id: kaifeng.doubt.003
  claim: 外城城门墩台是否包砖：内城景龙门（官式）考古证实包砖，外城考古报道只提「夯土版筑」；画中城门为素面土台
  tag: ⚠️
  source: gate.004 / gate.005 / gate.006 交叉
  quote: ""
  source_url: http://www.news.cn/local/20240712/359b81b8ad3a46e99c49a5bc27346c6b/c.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: bg2 默认按画（素面夯土台 + 木楼），口播不谈包砖。

- fact_id: kaifeng.doubt.004
  claim: 虹桥尺寸（21 × 7.8 m，拱高 5 m）为按画推算；1999 年上海青浦金泽复原桥按此建造
  tag: ⚠️
  source: 唐寰澄
  quote: "1999年由美国WGBH电视台NOVA科教片出资……在上海青浦金泽，用当年的施工方法，忠实于原结构，重现了一座汴水虹桥"
  source_url: https://www.dpm.org.cn/study_detail/100191.html
  tier: T1
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.doubt.005
  claim: 桥头木杆顶端鸟形物的功能（风向标 / 仙鹤表木）无可引原文；仅图像可见
  tag: ⚠️
  source: 见 bridge.007
  quote: ""
  source_url: https://commons.wikimedia.org/wiki/File:Along_the_River_During_the_Qingming_Festival_(detail_of_original).jpg
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: 画面可以画（形制有图），口播不解释功能。
```

---

## 参考图库统计表（G §7；门槛 ≥ 8 张）

根目录：`ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/`。图片在各 `bg*/ref/`（媒体走 R2，不进 git），索引 `bg*/refs.md` 进 git。
「许可可入画」按 `ref_fetch.py` 判定（CC0 / Public domain / CC BY / CC BY-SA）；**CC BY-SA 入画须署名**。「北宋依据」＝ T0 原本 / 北宋同期实物或壁画；「⚠️」＝ 摹本 / 后代 / 现代模型 / 复制品翻拍，只作构图、气氛、结构参考。

| bg | 张数 | 许可可入画 | 其中北宋依据 | ⚠️ 参考类 | refs.md |
|---|---|---|---|---|---|
| bg1_虹桥 | 12 | 12 | 5（原本局部 ×1、原本全卷 ×1、原本分段 CC0 ×2、金明池争标图 ×1） | 7（复制品翻拍 1、泰顺贯木拱廊桥实拍 4、清院本 1、Met 11.170 摹本 1） | `scenes/bg1_虹桥/refs.md` |
| bg2_东水门城门 | 11 | 11 | 3（原本城门局部、原本分段 CC0、原本全卷） | 8（复制品 1、今开封明清城墙 1、博物馆模型/示意 4、清院本 2） | `scenes/bg2_东水门城门/refs.md` |
| bg3_汴河码头 | 11 | 11 | 6（原本分段 ×2、原本修复前细部、原本全卷、许道宁渔父图、金明池争标图） | 5（复制品 1、闸口盘车图·五代 2、Cleveland 南宋船 1、泉州宋船实物 1） | `scenes/bg3_汴河码头/refs.md` |
| bg4_州桥早市 | 13 | 13 | 9（州桥遗址实拍 7：北宋石壁浮雕；原本分段、原本全卷） | 4（复制品 3、李嵩货郎图·南宋 1） | `scenes/bg4_州桥早市/refs.md` |
| bg5_正店酒楼 | 11 | 11 | 5（原本分段、原本细部 ×3、原本全卷） | 6（闸口盘车图 2、复制品 1、宋元界画 2、清院本 1） | `scenes/bg5_正店酒楼/refs.md` |
| bg6_瓦子勾栏 | 11 | 11 | 7（白沙北宋墓乐舞砖雕 ×6、原本全卷） | 4（李嵩骷髅幻戏图 ×2、货郎图 ×1 均南宋、复制品 1） | `scenes/bg6_瓦子勾栏/refs.md` |
| bg7_坊巷民居 | 13 | 13 | 8（原本分段 ×2、原本细部 ×2、登封北宋墓壁画 ×4） | 5（复制品 2、铁塔 1、清明上河园模型 2） | `scenes/bg7_坊巷民居/refs.md` |
| bg8_郊外清明踏青路 | 12 | 12 | 5（原本分段、原本细部 ×3、Qingming Festival 2） | 7（复制品 1、马远/马麟南宋春景 3、苏州片 1、清院本 1、Met 47.18.1 摹本 1） | `scenes/bg8_郊外清明踏青路/refs.md` |
| **合计** | **94** | 94 | 48 | 46 | |

注意事项（给阶段 2 写锚点 prompt 的人）：
- 原本「分段 Section 1–4」（CC0）与「Detail 1–17」（华盛顿大学 chinaciv 翻拍）是同一卷的不同裁切；`use` 里写的「看某段」需人眼定位，我未逐张核对每个 Detail 落在哪一段。
- 「Qingming shanghe tu *.jpg」系列（Immanuel Giel）是**复制品翻拍**，构图同原本、色彩偏艳，不能作色彩依据。
- 州桥遗址 8 张中，桥体本身是**明代**砖石拱桥，只有堤岸石壁浮雕是北宋；prompt 依 zhouqiao.001（青石平桥）而非照片桥拱。
- 泰顺廊桥是贯木拱**活态**技艺，拱骨编织可照抄；廊屋、石桥台不要。

## 未能核实 / 缺口

0. **计数**：本文件 48 条 fact（45 `ai_read` / 3 `ai_draft`），其中 7 条 `prompt_string` 留空（bridge.008、boat.004 与 §14 五条——它们是存疑 / 纠错项，不进 prompt）。
1. **外城考古数值**（gate.004：顶宽 4 m / 底宽 34.2 m / 高 8.7 m / 周长 29180 m / 壕宽 40 m）只见检索摘要，原页未打开 → `ai_draft`，请人眼核 baike 或《开封考古发现与研究》后改。
2. **州桥石壁数值**（zhouqiao.002：通高 3.3 m / 长 30 m；明桥 25.4 × 30 m）同上，人民日报页 403、新华网页只见摘要 → `ai_draft`。
3. **孙羊正店彩楼欢门的层数 / 栀子灯 / 红绿叉子**：网易「两个铺面」文只谈商业功能；招牌「正店 / 香醪 / 十千脚店 / 香饮子」只见知乎摘要 → 并入 shop.004 但标 T2/T3，请人眼对原本卷末局部逐字核。
4. **余辉「望火楼无人、兵营改饭铺、城门无防」的画外之意**：cnap.org.cn 原页两次 socket closed，经济观察网文不含此内容 → 未入 fact；gate.006 的「无女墙无守卫」是我按原本局部亲眼观察写的，不引余辉。
5. **故宫名画记（minghuaji.dpm.org.cn）**：未直接抓到条目正文（JS 站），改用故宫官网藏品页 228226 作官方描述来源；Commons 上有一张来自名画记的原本 png（pageid 128234945，未拉取），需要超高清时可 `pull`。
6. **卷中井的原本对应局部**（street.004）未定位，仅复制品翻拍。
7. **Met 检索相关性极差**：4 组关键词 30 条只有 2 条相关（11.170、47.18.1，均为明清摹本）；Met 无北宋汴京题材可入画原作，图库以 Commons 为主。

## 来源列表（本角度）

| tier | 来源 | URL |
|---|---|---|
| T0 | 《東京夢華錄》卷一（外城 / 舊京城 / 河道） | https://zh.wikisource.org/wiki/東京夢華錄/卷一 |
| T0 | 《東京夢華錄》卷二（御街 / 酒樓 / 州橋夜市 / 東角樓街巷） | https://zh.wikisource.org/wiki/東京夢華錄/卷二 |
| T0 | 《東京夢華錄》卷三（般載雜賣 / 防火 / 天曉諸人入市） | https://zh.wikisource.org/wiki/東京夢華錄/卷三 |
| T0 | 《東京夢華錄》卷七（清明節 / 金明池） | https://zh.wikisource.org/wiki/東京夢華錄/卷七 |
| T0 | 张择端《清明上河图》北宋原本（故宫）Commons 高清局部与分段 | https://commons.wikimedia.org/wiki/File:Along_the_River_During_the_Qingming_Festival_(detail_of_original).jpg ；https://commons.wikimedia.org/wiki/File:Bianjing_city_gate.JPG |
| T1 | 唐寰澄《〈清明上河图〉上汴水贯木拱虹桥》 | https://www.dpm.org.cn/study_detail/100191.html ；转载 https://iguoxue.ifeng.com/57387951/news.shtml |
| T1 | 新华网·景龙门遗址（2024） | http://www.news.cn/local/20240712/359b81b8ad3a46e99c49a5bc27346c6b/c.html |
| T1 | 新华网·州桥遗址（2022，仅摘要） | https://www.news.cn/local/2022-09/28/c_1129038021.htm |
| T1 | 北宋东京城遗址外城考古数据（仅摘要） | https://baike.baidu.com/item/北宋东京城遗址/7863519 |
| T2 | 《中国医药报》「《清明上河图》中的医药图像」 | http://bk.cnpharm.com/zgyyb/2019/10/31/app_240318.html |
| T3 | 故宫博物院藏品页「张择端清明上河图卷」 | https://www.dpm.org.cn/collection/paint/228226.html |
| T3 | 中文维基「清明上河圖」 | https://zh.wikipedia.org/wiki/清明上河圖 |
| T3 | 澎湃「《清明上河图》中为什么马少驴多？」 | https://www.thepaper.cn/newsDetail_forward_22153456 |
| T3 | 新浪「串车和江州车的区别」 | https://k.sina.cn/article_1863322885_6f100d0500100gouc.html |
| T3 | 知乎「清明上河图里都有哪些店铺」（仅摘要） | https://zhuanlan.zhihu.com/p/655974204 |
| T4（反例） | 明仇英本 / 苏州片、清院本、Met 11.170 / 47.18.1 | 见各 refs.md ⚠️ 条目 |
