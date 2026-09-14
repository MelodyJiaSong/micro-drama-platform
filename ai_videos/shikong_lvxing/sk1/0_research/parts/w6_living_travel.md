---
worker_id: W6_living_travel
stage: 0
role: researcher
angle: 住行黑名单
status: complete
blockers: []
confidence: medium
---

# W6 · 住与行 + 本站误传黑名单 + 系列来源库 + 器物参考图（sk1 汴京 · 1120 · 清明日）

> 本文件是 `0_research/dossier.md` 第 5 / 6 / 13 节的底稿，由 parent 合并。
> `verified_by` 取值：`ai_read` ＝ 本 worker 本次 **WebFetch 实际打开了含该 quote 的页面**（quote 逐字来自抓取结果）；`ai_draft` ＝ 只来自搜索摘要、未打开原文页。按 playbook，**进 prompt 前仍须人眼看过原文页升为 `human`**。
> 统计：§5 住 12 条（ai_read 11）、§6 行 18 条（ai_read 16）、§13 误传 16 条（本站专属 ≥ 8）。合计 ai_read 27 条（目标 ≥ 15 ✓）。
> 一手底本：维基文库《東京夢華錄》卷一 / 二 / 三 / 四 / 七（逐节抓取原文）、《宋史》卷 175 食货上三、陆游《老学庵笔记》卷四、《梦粱录》四库本卷十三；图像一手：《清明上河图》局部（Commons 公版）、《文会图》（宋徽宗，Commons 公版）、《闸口盘车图》（上海博物馆藏，Commons 公版）、Met 建窑 / 定窑 / 青白瓷碗（CC0）。

---

## §5 住（`kaifeng.house.NNN`）

```yaml
- fact_id: kaifeng.house.001
  claim: 北宋汴京垂足坐已是主流；靠背椅、凳（兀子）、高桌普及于士庶之家，市肆小店陈放高型家具（对照「席地而坐」误传）
  tag: ✅
  source: 陆游《老学庵笔记》卷四（徐敦立言）＋ 澎湃「艺术开卷｜宋代的椅子」(T2) ＋ 《清明上河图》店内陈设 / 《文会图》(T0 图像)
  quote: 「徐敦立言：往时士大夫家，妇女坐椅子兀子，则人皆讥笑其无法度。」（老学庵笔记）；「在宋代，靠背椅是使用数量最多的椅子。无论是高门大户还是寻常百姓，家家都有一把。」（澎湃）
  source_url:
    - https://zh.wikisource.org/wiki/老學庵筆記/卷四
    - https://www.thepaper.cn/newsDetail_forward_24921520
  tier: T0+T2
  verified_by: ai_read
  used_in: []
  prompt_string: "店内摆着木制靠背椅与方凳，客人垂足坐在椅凳上，面前是高脚方桌"
  negative: "席地而坐、跪坐、矮几、榻榻米、蒲团围坐、汉唐式矮案"
  note: 陆游（1125–1210）写「往时」＝北宋；「妇女坐椅被讥」反证男子与市井坐椅已普遍。参考图 p7 ref07/ref08《文会图》（1120 年代）桌椅器皿可直接对照。

- fact_id: kaifeng.house.002
  claim: 北宋时士大夫家妇女坐椅子、兀子会被讥笑「无法度」；市井女性（摊主）坐凳与否史料未直载
  tag: ⚠️
  source: 《老学庵笔记》卷四
  quote: 「往时士大夫家，妇女坐椅子兀子，则人皆讥笑其无法度。梳洗床、火炉床家家有之。」
  source_url: https://zh.wikisource.org/wiki/老學庵筆記/卷四
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "士人家的女眷坐在床榻边沿，不坐椅子；市井女摊主坐一张矮木凳（推测）"
  negative: "士人女眷坐太师椅、圈椅"
  note: 饮子摊女摊主坐凳属推测，记者口播须说「史书没写」。

- fact_id: kaifeng.house.003
  claim: 临汴河大街往东、沿城皆客店，南方官员、商贾、兵级皆在此安泊
  tag: ✅
  source: 《东京梦华录》卷三「大内前州桥东街巷」
  quote: 「東去沿城皆客店，南方官員商賈兵級，皆於此安泊。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "汴河大街东段沿城根一排客店，门口挂布幌，南来的商人与兵士进出"
  negative: "现代旅馆招牌、霓虹灯、玻璃门、前台柜台"

- fact_id: kaifeng.house.004
  claim: 宋代普通客店住一晚约 50 文（T2 转述数字，本次未核到原文页）
  tag: ⚠️
  source: 吴钩（儒家网 / 搜索摘要），原始出处未核
  source_url: https://www.rujiazg.com/article/12883
  tier: T2
  verified_by: ai_draft
  used_in: []
  prompt_string: ""
  negative: ""
  note: 本页实际内容为「约束客店户」（诗板 / 病人义务），不含价格；数字不得进 prompt，物价角（W?）用程民生页码复核。

- fact_id: kaifeng.house.005
  claim: 宋代蜡烛贵、油灯贱——神宗朝官方奠仪「秉烛每条四百文，常料烛每条一百五十文」；哲宗朝定州采购每根约 18–20 文；南宋读书人「每夜提瓶沽油四五文」；通宵点烛 50–90 文＝油灯 10–20 倍。平民夜里用油灯，正店才「灯烛荧煌」
  tag: ✅
  source: 吴钩「宋人用什么照明」（澎湃·私家历史，T2）转引《宋会要辑稿》《续资治通鉴长编》
  quote: 「秉烛每条四百文，常料烛每条一百五十文」；「每根蜡烛约 18 文钱，顶多是 20 文钱左右」；「每夜提瓶沽油四五文，藏于青布褙袖中归，燃灯读书」；「通宵点烛，少说要三至五根蜡烛，即需要支出 50~90 文钱，是油灯成本的 10~20 倍」
  source_url: https://www.thepaper.cn/newsDetail_forward_1452541
  tier: T2（转引 T0）
  verified_by: ai_read
  used_in: []
  prompt_string: "夜里摊位与民居用陶碟油灯，一根灯草，昏黄小火苗；只有正店门首灯烛荧煌"
  negative: "满屋蜡烛、吊灯、电灯、整条街灯笼阵列照亮如白昼"
  note: T0 回查待做（《宋会要辑稿》礼 / 《长编》哲宗卷）。

- fact_id: kaifeng.house.006
  claim: 京中正店七十二户，其余谓「脚店」；门首皆缚彩楼欢门；珠帘绣额、灯烛晃耀；店内两廊小阁子吊窗花竹、各垂帘幕；卖下酒厨子叫「茶饭量酒博士」
  tag: ✅
  source: 《东京梦华录》卷二「酒楼」
  quote: 「在京正店七十二戶，此外不能遍數，其餘皆謂之『腳店』。」「門首皆縛彩樓歡門」「珠簾繡額，燈燭晃耀」「排列小濩子，吊窗花竹，各垂簾幕」「凡店內賣下酒廚子，謂之『茶飯量酒博士』」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "酒楼门口扎着彩楼欢门——木架绑扎彩帛与花枝、彩绸层层垂挂；门内挂珠帘、绣额；店内隔成小阁子，吊窗外见花竹，垂着帘幕；跑堂叫酒博士"
  negative: "红灯笼串、印刷横幅、玻璃橱窗、霓虹灯、现代菜单牌"

- fact_id: kaifeng.house.007
  claim: 民间吉凶筵会，椅桌陈设、器皿合盘、酒担动使之类自有「茶酒司」管赁；厨司、白席人一并可雇（椅桌成套普及的旁证）
  tag: ✅
  source: 《东京梦华录》卷四「筵会假赁」
  quote: 「凡民間吉凶筵會，椅桌陳設，器皿合盤，酒檐動使之類，自有茶酒司管賃。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "筵席一桌数椅，成套租来的椅桌与瓷器摆开"
  negative: "跪坐分食矮案、一人一席"

- fact_id: kaifeng.house.008
  claim: 汴京每年春时官府差人夫监淘在城渠，淘出之泥另开坑盛放谓「泥盆」（✅ 汴京）；「倾脚头」（每日出粪人，各有主顾、侵夺则争讼）是《梦粱录》南宋临安记载（⚠️ 类推汴京）
  tag: ⚠️
  source: 《东京梦华录》卷三「诸色杂卖」＋ 《梦粱录》四库本卷十三「诸色杂货」
  quote: 「每遇春時，宮中差人夫監淘在城渠，別開坑盛淘出者泥，謂之『泥盆』」（东京梦华录）；「毎日自有出糞人瀽去謂之傾脚頭各有主顧不敢侵奪或有侵奪糞主必與之争甚者經府大訟勝而後已」（梦粱录）
  source_url:
    - https://zh.wikisource.org/wiki/東京夢華錄/卷三
    - https://zh.wikisource.org/wiki/夢粱錄_(四庫全書本)/卷13
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "清早巷口有挑木粪桶的粪夫走过（临安记载类推，口播标推测）"
  negative: "现代下水井盖、抽水马桶、塑料桶"
  note: 《东京梦华录》未见「倾脚头」三字，只有淘渠记载；如厕方式（马桶 / 茅厕）本次未查。

- fact_id: kaifeng.house.009
  claim: 汴京夏月有「洗毡淘井者」沿街揽活——井水是民用水主源（✅）；「供人家食用水者各有主顾」（送水夫）为临安记载（⚠️）
  tag: ✅
  source: 《东京梦华录》卷三「诸色杂卖」＋ 《梦粱录》卷十三
  quote: 「夏月則有洗氈淘井者，舉意皆在目前。」；「供人家食用水者各有主顧供之」（梦粱录）
  source_url:
    - https://zh.wikisource.org/wiki/東京夢華錄/卷三
    - https://zh.wikisource.org/wiki/夢粱錄_(四庫全書本)/卷13
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "街边一口砖砌井口，木辘轳，妇人提木桶打水；挑水夫肩挑两只木桶"
  negative: "自来水龙头、压水井、塑料桶、瓶装水"
  note: 参考图 p4 ref08（《清明上河图》井局部）。汴河水直接饮用与否未查。

- fact_id: kaifeng.house.010
  claim: 修整屋宇、泥补墙壁，早晨桥市街巷口皆有木竹匠人；竹木作料有铺席；砖瓦泥匠随手即就——城内民居为木构 + 灰瓦 + 泥抹墙 + 部分砖砌
  tag: ✅
  source: 《东京梦华录》卷四「修整杂货及斋僧请道」
  quote: 「儻欲修整屋宇，泥補墻壁……即早辰橋市街巷口皆有木竹匠人」「竹木作料，亦有鋪席。磚瓦泥匠，隨手即就。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "汴京街巷民居：灰瓦屋顶、木柱木门板、泥抹土墙、砖砌墙脚；城外农舍草顶"
  negative: "白色现代抹灰、玻璃窗、瓷砖、混凝土、金属门"
  note: 「粉墙朱户」（卷一）指护龙河内官宅。窗纸 / 窗纱、床榻形制、炭盆取暖本次未查。

- fact_id: kaifeng.house.011
  claim: 每坊巷三百步许有军巡铺屋一所，铺兵五人，夜间巡警、收领公事；高处砖砌望火楼；失火由马军奔报、三衙与开封府领军扑灭「不劳百姓」
  tag: ✅
  source: 《东京梦华录》卷三「防火」
  quote: 「每坊巷三百步許，有军巡铺屋一所，鋪兵五人，夜间巡警收领公事。又于高处砖砌望火樓」「則有馬軍奔報。軍廂主馬步軍、殿前三衙、開封府各領軍級撲滅，不勞百姓」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "街角一间小铺屋，门口两名铺兵（短衣、裹头巾，倚着水桶与麻搭）；远处砖砌望火楼高台"
  negative: "警察制服、消防栓、警车"
  note: 概念卡「坊市被巡铺兵拦」的史料落点即此。

- fact_id: kaifeng.house.012
  claim: 市井用白瓷 / 青白瓷粗碗与陶缸——卖辣菜小儿「挟白磁缸子」；Met 藏 11–12 世纪定窑 / 青白瓷碗为实物形制
  tag: ✅
  source: 《东京梦华录》卷二「饮食果子」＋ Met 藏品 52589 / 44457 / 50661 / 39577（CC0）
  quote: 「又有小兒子，著白虔布衫，青花手巾，挾白磁缸子，賣辣菜」
  source_url:
    - https://zh.wikisource.org/wiki/東京夢華錄/卷二
    - https://www.metmuseum.org/art/collection/search/52589
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "白瓷或青白瓷粗碗，敞口浅腹，釉色牙白微青，碗口有芒；粗陶大缸"
  negative: "青花瓷（元以后）、粉彩、搪瓷、塑料碗、不锈钢盆"
  note: 「辣菜」是芥菜类，不是辣椒。参考图 p1 ref07–ref11。
```

## §6 行（`kaifeng.travel.NNN`）

```yaml
- fact_id: kaifeng.travel.001
  claim: 景德四年（1007）定汴河岁额六百万石；治平二年（1065）汴河漕粟至京 575.5 万石
  tag: ✅
  source: 《宋史》卷 175 食货上三·漕运
  quote: 「景德四年，定汴河歲額六百萬石。」「治平二年，漕粟至京師，汴河五百七十五萬五千石。」
  source_url: https://zh.wikisource.org/wiki/宋史/卷175
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: 口播数据：「汴河一年往城里运六百万石米」。宣和二年当年数未查，用岁额口径并口播「定额」。

- fact_id: kaifeng.travel.002
  claim: 宋都大梁有汴河、黄河、惠民河、广济河四河通漕，汴河所漕为多
  tag: ✅
  source: 《宋史》卷 175
  quote: 「宋都大梁，有四河以通漕運：曰汴河，曰黃河，曰惠民河，曰廣濟河，而汴河所漕為多。」
  source_url: https://zh.wikisource.org/wiki/宋史/卷175
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""

- fact_id: kaifeng.travel.003
  claim: 汴河自西京洛口分水入京城，东去至泗州入淮；运东南之粮，凡东南方物自此入京，公私仰给
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  quote: 「中曰汴河，自西京洛口分水入京城，東去至泗州，入淮。運東南之糧，凡東南方物，自此入京城，公私仰給焉。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "汴河上满载米袋的纲船首尾相接，船帮吃水很深，岸上纤夫弓身拉纤"
  negative: "蒸汽船、铁壳船、集装箱、现代桥梁、汽艇"

- fact_id: kaifeng.travel.004
  claim: 纲运按「纲」计舟车役人之直，付主纲吏雇募；挽舟卒有终身不还其家、老死河路者
  tag: ✅
  source: 《宋史》卷 175
  quote: 「凡一綱計其舟車役人之直，給付主綱吏雇募。」「挽舟卒有終身不還其家、老死河路者。」
  source_url: https://zh.wikisource.org/wiki/宋史/卷175
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "纤夫赤脚、裤脚挽到膝上、肩搭麻绳纤板，身体前倾四十五度"
  negative: "整齐制服、皮鞋、救生衣"
  note: 长访「汴河脚夫」的史料底色；「一袋米＝几天工钱」由物价角出锚。

- fact_id: kaifeng.travel.005
  claim: 东水门外七里曰虹桥，其桥无柱，皆以巨木虚架，饰以丹雘，宛如飞虹——虹桥在外城之外，不在御街
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  quote: 「自東水門外七里曰虹橋，其橋無柱，皆以巨木虛架，飾以丹雘，宛如飛虹。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "汴河上一座无柱木拱桥，粗大原木交叠成拱，桥身涂朱红，桥面铺木板、两侧木栏，桥上人流摊贩"
  negative: "石拱桥、石柱桥墩、水泥桥、桥上挂灯笼"
  note: 参考图 p6 ref04（《清明上河图》虹桥局部）。一镜到底「虹桥→州桥」实际相距 ≥7 里 + 东水门，须口播或转场说明。

- fact_id: kaifeng.travel.006
  claim: 州桥正名天汉桥，正对大内御街；与相国寺桥皆低平不通舟船；柱皆青石，石梁石笋楯栏
  tag: ✅
  source: 《东京梦华录》卷一「河道」
  quote: 「州橋（正名天漢橋），正對於大內御街，其橋與相國寺橋皆低平不通舟船……其柱皆青石為之，石梁石筍楯欄。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "御街上的州桥：低平青石桥，青石柱、石梁，石笋状栏杆"
  negative: "木拱桥、高拱桥、汉白玉桥"

- fact_id: kaifeng.travel.007
  claim: 叠梁木拱桥（虹桥）起源：《渑水燕谈录》记天禧元年（1017）魏化基在汴河造无脚桥未成，后青州牢城废卒造成南阳桥，陈希亮仿之建于汴水，推广至汴、汾、泗诸河
  tag: ⚠️
  source: 搜索摘要（搜狐 / 新浪转述《渑水燕谈录》）
  source_url: https://www.sohu.com/a/478444274_121117451
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: ""
  negative: ""
  note: 口播可用「这种桥是几十年前一个青州牢城的老兵发明的」，须回查《渑水燕谈录》卷八原文后升 ✅。

- fact_id: kaifeng.travel.008
  claim: 太平车——上有箱无盖，箱如构栏而平，板壁前出两木长二三尺许，可载数十石（前用骡驴二十余头分两行或牛五七头、后拖斜木、夜悬铁铃为 T3 补充）
  tag: ✅
  source: 《东京梦华录》卷三「般载杂卖」
  quote: 「上有箱无盖，箱如构欄而平，板壁前出两木，长二三尺许」「载数十石」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一辆太平车：无盖的木厢大车，厢前伸出两根长木，车夫立在两木之间执长鞭，前面骡驴分两列拉车，车后拖两根斜木"
  negative: "四轮欧式马车、橡胶轮胎、铁辐条轮、汽车"
  note: 参考图 p6 ref05–ref11《清明上河图》车辆局部；ref01/ref02《闸口盘车图》。

- fact_id: kaifeng.travel.009
  claim: 平头车如太平车而小，多为酒正店运酒桶；串车（独轮，前后各一人把驾、两旁扶拐、前有驴拉）载竹木瓦石；浪子车平盘两轮卖糕点用；另有驼骡驴驮子
  tag: ✅
  source: 《东京梦华录》卷三「般载杂卖」（串车 / 浪子车细节为 T3 转述）
  quote: 「平頭車亦如太平車而小」；提及「串车」「浪子车」「驝騾驢馱子」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "街上一辆独轮串车，一人在后把驾、一人在前拉、旁边一人扶拐；驴背驮着两只货筐"
  negative: "自行车、三轮车、板车橡胶轮、手推超市车"

- fact_id: kaifeng.travel.010
  claim: 出街市干事、路远倦行，逐坊巷桥市自有假赁鞍马者，不过百钱
  tag: ✅
  source: 《东京梦华录》卷四「杂赁」
  quote: 「尋常出街市幹事，稍似路遠倦行，逐坊巷橋市，自有假賃鞍馬者，不過百錢。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷四
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "桥头巷口拴着几匹备鞍的马与驴，赁马人蹲在旁边招揽"
  negative: "出租车、马车站牌、拴马桩上挂价目表"
  note: 「不过百钱」是本站可口播的物价锚之一（赁马一趟 ≤ 100 文）。

- fact_id: kaifeng.travel.011
  claim: 马行街夜市直至三更尽，才五更又复开张；耍闹去处通晓不绝——汴京不禁夜
  tag: ✅
  source: 《东京梦华录》卷三「马行街铺席」
  quote: 「夜市直至三更盡，才五更又復開張。如要鬧去處，通曉不絕。」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "深夜街市摊位仍在营业，油灯烛火点点，行人往来"
  negative: "宵禁空街、坊门紧闭、金吾卫巡街驱人、街鼓"

- fact_id: kaifeng.travel.012
  claim: 宋太祖乾德三年（965）诏「令京城夜漏，未及三鼓不得禁止行人」；宋敏求《春明退朝录》（1074 前后）「二纪以来，不闻街鼓之声，金吾之职废矣」——徽宗朝汴京实际已无宵禁
  tag: ✅
  source: 吴钩「为什么说宋代发生了一场城市革命」（澎湃，T2）转引《宋会要辑稿》《春明退朝录》
  quote: 「宋太祖乾德三年（965），诏『令京城夜漏，未及三鼓不得禁止行人』」；「成书于宋神宗熙宁七年（1074）前后的宋敏求《春明退朝录》称，『二纪以来，不闻街鼓之声，金吾之职废矣。』」
  source_url: https://www.thepaper.cn/newsDetail_forward_1387938
  tier: T2（转引 T0）
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "宵禁、坊门、街鼓"
  note: T0 回查待做（《宋会要辑稿·食货》乾德三年四月十三日诏；《春明退朝录》卷上）。

- fact_id: kaifeng.travel.013
  claim: 对照唐长安：唐夜禁从「昼漏尽」击鼓六百下后开始（一入夜即禁行人），至次日「五更三筹」结束
  tag: ✅
  source: 同上（T2 转引《唐律疏议》/《唐六典》）
  quote: 「唐朝的夜禁时间是从『昼漏尽』，击鼓六百下之后开始（即一入夜就开始禁行人），至次日『五更三筹』结束」
  source_url: https://www.thepaper.cn/newsDetail_forward_1387938
  tier: T2（转引 T0）
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: ""
  note: 记者口播用：「六百年前的长安天一黑就赶人，这里三更还在卖夜宵」。

- fact_id: kaifeng.travel.014
  claim: 清明日凡新坟皆用此日拜扫，都城人出郊；士庶阗塞诸门；纸马铺当街用纸叠成楼阁；四野如市，就芳树园囿罗列杯盘互相劝酬；轿子以杨柳杂花装簇顶上、四垂遮映；自此三日皆出城上坟，一百五日最盛；抵暮而归
  tag: ✅
  source: 《东京梦华录》卷七「清明节」
  quote: 「凡新墳皆用此日拜掃。都城人出郊。」「士庶闐塞諸門，紙馬鋪皆於當街用紙袞疊成樓閣之狀。四野如市，往往就芳樹之下，或園囿之間，羅列杯盤，互相勸酬。」「轎子即以楊柳雜花裝族頂上，四垂遮映。自此三日，皆出城上墳，但一百五日最盛。」「緩入都門，斜陽御柳」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "清明日城门口人流拥挤出城，轿顶插满柳枝杂花、四面垂下遮住轿身；郊外树下铺开杯盘野餐；纸马铺门前纸扎楼阁"
  negative: "汽车、柏油路、水泥墓碑、塑料花圈、香烛店霓虹"
  note: 「卯时城门开→出城扫墓」路线：出诸门后郊野；轿为主要载人工具。参考图 p1 ref05（《清明上河图》道路 / 轿局部）。

- fact_id: kaifeng.travel.015
  claim: 清明诸军禁卫各成队伍跨马作乐四出，谓之「摔脚」，旗旄鲜明；节日坊市卖稠饧、麦糕、乳酪、乳饼
  tag: ✅
  source: 《东京梦华录》卷七「清明节」
  quote: 「諸軍禁衛，各成隊伍，跨馬作樂四出，謂之『摔腳』。其旗旄鮮明，軍容雄壯」「節日坊市賣稠餳、麥糕、乳酪、乳餅之類」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "一队禁军骑马结队出城，旗旄鲜明；街摊卖麦糕、乳饼、稠饧（麦芽糖）"
  negative: "青团、艾草团子、粽子"

- fact_id: kaifeng.travel.016
  claim: 东都外城方圆四十余里，城壕「护龙河」阔十余丈，濠内外皆植杨柳；新城南壁三门、东四门、西四门、北四门；旧城方圆约二十里许
  tag: ✅
  source: 《东京梦华录》卷一「东都外城」「旧京城」
  quote: 「東都外城，方圓四十餘里。城壕曰護龍河，闊十餘丈，濠之內外，皆植楊柳，粉牆朱戶，禁人往來。」「舊京城，方圓約二十里許」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: "夯土包砖的高大城墙，城门楼歇山顶（以《清明上河图》城门楼为准）；护城河两岸柳树成行，春日新绿"
  negative: "欧式城堡、明清北京式箭楼、青砖瓮城（待回查）"
  note: 参考图 p7 ref01《清明上河图》城门楼（已人眼核看：单层门楼、歇山顶、夯土墩台、驼队出门）。「瓮城三层屈曲开门」原文本次抓取未含，待回查卷一。

- fact_id: kaifeng.travel.017
  claim: 宋代「过所」制度久已不行（后唐「出入过所事，久不施行」；洪迈称「过所二字，读者多不晓」）；只在出入关禁（如入川陕、经剑门）验「公凭」；走州过县、投宿旅店不需通行证——外地人进汴京不要文书
  tag: ✅
  source: 吴钩文（搜狐「宋人才可以来一场说走就走的旅行」转载，T2）转引《五代会要》《容斋随笔》、天圣六年益州奏
  quote: 「出入过所事，久不施行」「然『过所』二字，读者多不晓」「自来入川陕之人，依法经官司投状，给公凭听行」「西川往来商旅，有公凭者则由剑门经过」「只是在出入关禁时才验看公凭，一般情况下，走州过县是不用通行证的」
  source_url: https://www.sohu.com/a/464108112_99996707
  tier: T2（转引 T0）
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "路引、通关文牒、身份牌、城门查验证件"
  note: 「路引」是明制；记者入城不需文书，本站不做「被盘查证件」桥段（可做「以为要证件」的反向笑点）。

- fact_id: kaifeng.travel.018
  claim: 汴京城门夜间照常关闭，昏晓有街鼓 / 禁鼓提示启闭；上元节城门弛禁通宵；日常具体几更开闭本次未查到 T0 记载
  tag: ⚠️
  source: 搜索摘要（儒家网吴钩 / 网易）
  source_url: https://www.rujiazg.com/article/11523
  tier: T3
  verified_by: ai_draft
  used_in: []
  prompt_string: ""
  negative: ""
  note: 概念卡「卯时城门开」按常例推测，口播须说「按惯例」；回查《宋会要辑稿·方域》。
```

## §13 本站常见误传（`kaifeng.myth.NNN`，全部 tag ❌ 除注明 ⚠️；每条 negative 已同步进 `_series/blacklist.md`）

```yaml
- fact_id: kaifeng.myth.001
  claim: 误传「宋人掏银子 / 银锭付账」；正解：北宋市井主币铜钱（贯 / 陌 / 文），白银非流通货币；纸币交子仅四川等地
  tag: ❌
  source: zh.wikipedia「交子」（ai_read）＋ 上海财大档案馆「白银历程」/ 文汇「古人真的是用银子买东西吗」（F6 C05，本次仅核 URL 200）
  source_url:
    - https://zh.wikipedia.org/wiki/交子
    - https://archives.sufe.edu.cn/bf/ad/c3148a180141/page.htm
    - https://wenhui.whb.cn/zhuzhanapp/tj/20200108/312908.html
  tier: T3/T2
  verified_by: ai_read
  used_in: []
  prompt_string: "一串串用麻绳穿的铜钱，付账时数钱"
  negative: "银锭、元宝、碎银、银两、银票"
  note: 2026-09-14 SYNC_sk1（回应 R7 W07）：仍缺 quote（facts_registry 报 warning）。shot09 画面与口播的正面依据是 money.001 / money.002 / money.006（都带原文 quote），本条只承担「掏银子 ❌」这一误传标签。补 quote 时从 source_url 原文逐字摘；本次网络不通，没有凭记忆补字，id 不变。

- fact_id: kaifeng.myth.002
  claim: 误传「宋人用银票」；正解：「银票」是明清票号产物；宋只有交子——起于四川商人私发，天圣元年（1023）设益州交子务官办；大观元年（1107）改称钱引，四川仍称交子；1120 年的汴京市面不用纸币
  tag: ❌
  source: zh.wikipedia「交子」
  quote: 「天圣元年（1023年）下令交子鋪停止發行交子……改由朝廷設益州交子務」「起初限四川，之後普及」「宋徽宗大觀元年夏（1107年）改交子為钱引」
  source_url: https://zh.wikipedia.org/wiki/交子
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "银票、纸币、钞票、钱庄票号"
  note: 记者「掏银子→只收铜钱」是概念卡既定笑点；口播「纸币只在四川」。

- fact_id: kaifeng.myth.003
  claim: 误传「宋人席地而坐」；正解见 kaifeng.house.001（垂足坐、椅凳桌普及）
  tag: ❌
  source: 《老学庵笔记》卷四 ＋ 澎湃「宋代的椅子」
  source_url: https://zh.wikisource.org/wiki/老學庵筆記/卷四
  tier: T0+T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "席地而坐、跪坐、蒲团、矮几、榻榻米"

- fact_id: kaifeng.myth.004
  claim: 误传「称官员为大人」；正解：唐宋「大人」指父母长辈；官场称「大人」清雍正初起才流行；万历年间仍「很隆重、很罕见」
  tag: ❌
  source: 中新网 2015「古代官员称大人」
  quote: 「到清代，称大人才成为一种很普遍的现象，民初徐珂认为『大人之称，始于雍正初』」；「晚辈对长辈……『父亲大人』『母亲大人』」
  source_url: https://www.chinanews.com.cn/m/cul/2015/04-21/7221935.shtml
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "台词「大人」称官、「老爷」"
  note: 称谓白名单由语言角（W?）出；本条只登记黑名单。

- fact_id: kaifeng.myth.005
  claim: 误传「宋人穿明代立领、盘扣、马褂 / 清代长辫、瓜皮帽」；正解：宋服交领 / 圆领 + 幞头 / 软巾（锁定串由衣角出）
  tag: ❌
  source: 沈从文《中国古代服饰研究》（T1，本次未核页）＋ zh.wikipedia「剃发易服」（F6 C12，本次未核）
  source_url: https://zh.wikipedia.org/wiki/剃发易服
  tier: T1/T3
  verified_by: ai_draft
  used_in: []
  prompt_string: ""
  negative: "立领、盘扣、马褂、长辫、瓜皮帽、旗袍、现代纽扣、拉链"

- fact_id: kaifeng.myth.006
  claim: 误传「汴京夜里宵禁、坊门紧闭」；正解见 kaifeng.travel.011 / 012（夜市三更尽、五更复开；乾德三年诏未及三鼓不禁行人；街鼓早废）
  tag: ❌
  source: 《东京梦华录》卷三 ＋ 澎湃「城市革命」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0+T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "宵禁、坊门、街鼓、金吾卫驱人、空无一人的夜街"
  note: 与长安 742 站形成系列内对照（长安「三百鼓」宵禁）。

- fact_id: kaifeng.myth.007
  claim: 误传「宋代街头有辣椒 / 玉米 / 番茄 / 土豆 / 红薯」；正解：辣椒最早记载为《遵生八笺》「番椒」条且 1591 初刻本无此条（后印补入）、《群芳谱》1614–21；玉米 1560 年（嘉靖三十九年）始有明确记载；番薯 1576 年《云南通志》；马铃薯明末清初；番茄万历（T3 未核）
  tag: ❌
  source: 澎湃「谁人首载辣椒？——高濂《遵生八笺》番椒考」＋ 中新网 2023「玉米番薯马铃薯传入」
  quote: 「11525号善本中并没有记载『番椒』」；「1560年(明嘉靖三十九年)中国始有对玉米最早的明确记载和形态描述」；「明万历四年(1576年)的《云南通志》中就有……『红薯』的记载」
  source_url:
    - https://www.thepaper.cn/newsDetail_forward_27299138
    - https://www.chinanews.com.cn/cj/2023/05-13/10006435.shtml
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "辣椒、红油、干辣椒串、玉米、番茄、土豆、红薯、花生、南瓜、向日葵"
  note: 概念卡「记者问有没有辣的→摊主茫然」纠错单元用此条。

- fact_id: kaifeng.myth.008
  claim: 误传「汴京满街纸币」；正解同 kaifeng.myth.002（交子 / 钱引只在四川等地，汴京用铜钱）
  tag: ❌
  source: zh.wikipedia「交子」
  source_url: https://zh.wikipedia.org/wiki/交子
  tier: T3
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "纸币、钞票"

- fact_id: kaifeng.myth.009
  claim: 误传「宋代女子普遍缠足」；正解：缠足约起于北宋（元丰后在上层开始流行、徽宗朝宫廷推广为 T3 说法）、兴于南宋；北宋末仅限上层少数，劳动妇女不缠足——本站市井女性一律天足
  tag: ⚠️
  source: zh.wikipedia「缠足」＋ 高洪兴《缠足史》（上海文艺 2007，豆瓣页 200，本次未读书）
  quote: 「研究指出，缠足約起源於北宋」「北宋元豐後是开始流行的时期」「部份客家人因婦女有務農、採茶的傳統……所以不纏足」
  source_url:
    - https://zh.wikipedia.org/wiki/缠足
    - https://book.douban.com/subject/2115264/
  tier: T3/T1
  verified_by: ai_read
  used_in: []
  prompt_string: "市井女性天足，穿平头布鞋或麻鞋"
  negative: "三寸金莲、弓鞋、小脚蹒跚（市井女性）"
  note: 上层女性是否已缠足在 1120 年仍 ⚠️——本站不出现上层女性即可回避。

- fact_id: kaifeng.myth.010
  claim: 误传「清明吃青团」；正解：「青团」之名始见明代《杭州府志》「青白圆子」、袁枚《随园食单》（1792）；宋有寒食饼 /「茸母」（鼠曲草）但属江南 / 徽宗被虏后诗；北宋汴京清明坊市卖的是稠饧、麦糕、乳酪、乳饼（卷七）
  tag: ❌
  source: 文汇「隐食记｜清明美食……」＋ 《东京梦华录》卷七
  quote: 「其米食用青白圆子，亦寒食遗意」（明《杭州府志》）；「青糕、青团。捣青草为汁，和粉作糕团」（随园食单）；「青团大体流行于江浙一带」
  source_url:
    - https://wenhui.whb.cn/zhuzhan/xinwen/20200331/337397.html
    - https://zh.wikisource.org/wiki/東京夢華錄/卷七
  tier: T2+T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "青团、艾草团子、绿色糯米团"

- fact_id: kaifeng.myth.011
  claim: 误传「满街红灯笼串、印刷体 / 灯箱招牌、横幅标语」；正解：店门首缚彩楼欢门、珠帘绣额、布幌；画面文字只用核对过的真实店名（《清明上河图》「孙羊正店」「十千脚店」等）或无字纹样，禁止让模型自行「写字」
  tag: ❌
  source: 《东京梦华录》卷二「酒楼」＋ 《清明上河图》（T0 图像，店名题字本次未逐字核）
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷二
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "红灯笼串、印刷字体招牌、灯箱、霓虹、横幅标语、乱码汉字"

- fact_id: kaifeng.myth.012
  claim: 误传「虹桥在城里 / 御街上是木拱桥」；正解：虹桥在东水门外七里（城外汴河上），御街上的州桥是低平青石桥（kaifeng.travel.005 / 006）
  tag: ❌
  source: 《东京梦华录》卷一「河道」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷一
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "御街上的木拱桥、城内虹桥"
  note: 概念卡「一镜到底 虹桥→州桥」须在 previz 里处理跨度（口播「一路往西七里」或分段）。

- fact_id: kaifeng.myth.013
  claim: 误传「街上跑四轮载人马车」；正解：汴京载货用太平车（骡驴牛拉）、平头车、串车，人出行骑马 / 驴（可赁，≤ 百钱）或乘轿；史料不见四轮载人马车
  tag: ⚠️
  source: 《东京梦华录》卷三「般载杂卖」/ 卷四「杂赁」
  source_url: https://zh.wikisource.org/wiki/東京夢華錄/卷三
  tier: T0
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "四轮载人马车、欧式 carriage、车夫戴礼帽"
  note: 「无载人马车」是缺记载推断，故 ⚠️；画面只出太平车 / 轿 / 骑驴即可回避。

- fact_id: kaifeng.myth.014
  claim: 误传「宋代夜里满堂蜡烛」；正解见 kaifeng.house.005（平民油灯，蜡烛 150–400 文一条是贵物；正店才灯烛荧煌）
  tag: ⚠️
  source: 澎湃「宋人用什么照明」
  source_url: https://www.thepaper.cn/newsDetail_forward_1452541
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "满屋蜡烛、烛台阵列、吊灯"

- fact_id: kaifeng.myth.015
  claim: 误传「进城要路引 / 通关文牒 / 身份证」；正解见 kaifeng.travel.017（过所久废，城内与州县间不验证件，只在关禁验公凭；路引是明制）
  tag: ❌
  source: 搜狐转载吴钩文
  source_url: https://www.sohu.com/a/464108112_99996707
  tier: T2
  verified_by: ai_read
  used_in: []
  prompt_string: ""
  negative: "路引、通关文牒、身份牌、城门盘查证件"

- fact_id: kaifeng.myth.016
  claim: 误传「汴京城门是明清式青砖箭楼 / 瓮城」；正解：以《清明上河图》城门楼为形制依据——夯土墩台、单层歇山顶门楼、无箭窗；外城「瓮城三层」记载待回查
  tag: ⚠️
  source: 《清明上河图》城门楼局部（p7 ref01，已人眼核看）＋ 《东京梦华录》卷一
  source_url: https://commons.wikimedia.org/wiki/File:Qingming_shanghe_tu_gate_tower.jpg
  tier: T0（图像）
  verified_by: ai_read
  used_in: []
  prompt_string: "夯土墩台上一座单层歇山顶木构门楼，斗拱、直棂窗；门洞方直，驼队出门"
  negative: "青砖箭楼、箭窗、明清北京式城楼、欧式城堡塔楼"
```

---

## 参考图统计（`python tools/ref_fetch.py pull`，图在各目录 `ref/`，索引在 `refs.md`；媒体走 R2 不进 git）

| 资产目录（`sk1/2_世界观人设/props/`） | 张数 | 来源构成 | 许可 | 备注 / use |
|---|---|---|---|---|
| `p1_旋煎羊白肠与食摊` | **11** | 《清明上河图》Detail 1/2/3/7 + road + 「11」局部（Commons 公版）×6；Commons 磁州窑白地黑花碗 ×1；Met 定窑 / 青白瓷碗 11–12 世纪 CC0 ×4（52589 / 44457 / 50661 / 39577） | 全部可入画 | ref01 已人眼核看：街边食摊、大伞、长桌、挑担、驴——食摊陈设直接依据。evidences: house.012, food.007 |
| `p4_饮子摊` | **11** | Met 建窑黑釉茶盏 11–12 世纪 CC0 ×7（48117 / 42457 / 48105 / 52602 / 48100 / 51074 / 42455）；《清明上河图》井 + Detail 8/9/11 ×4 | 全部可入画 | 建盏是茶盏；饮子摊用的粗碗可与 p1 的定窑 / 青白瓷碗共用。evidences: house.012, house.009 |
| `p6_太平车与独轮车` | **11** | 《闸口盘车图》（上博，五代—北宋初）×2；《清明上河图》纤船 / 虹桥 / Detail 12/14/15/16/17 / 原作局部 / Section 1（CC0）×9 | 全部可入画 | ref05（Detail 12）已人眼核看：驴骡、独轮车轮、挑夫。evidences: travel.008 / 009 / 005 |
| `p7_彩楼欢门与招牌` | **10** | 《清明上河图》城门楼 / 「Festival 2」/ 修复前局部 / Section 2–4（CC0）×6；《文会图》宋徽宗 ×2（桌椅器皿）；清院本局部 ×1（仅对照，不作形制依据）；全卷缩图 ×1 | 全部可入画 | ref01 是**城门楼**而非欢门（作 travel.016 / myth.016 依据）；欢门须在 Section 2–4 中人工圈出「孙羊正店」「十千脚店」。evidences: house.006, myth.011 |

四个目录均 ≥ 8 张（Q4 门槛 ✓）。Met 检索按 `Cizhou` / `Yaozhou` 关键词命中全是无关品（Met 全文检索不认窑口名），改用 `Ding ware bowl` / `Qingbai bowl Song` / `Jian ware tea bowl Song` 才命中——写进 playbook 教训。

## 未能核实 / 待回查

1. `kaifeng.house.004` 客店一晚 50 文——只在搜索摘要出现，儒家网原文页不含该数字；须查程民生《宋代物价研究》「房租 / 旅店」页码。
2. `kaifeng.travel.007` 虹桥起源《渑水燕谈录》——T3 转述，须回查卷八原文。
3. `kaifeng.travel.018` 城门日常启闭时刻——未查到 T0；《宋会要辑稿·方域》待查。卷一「瓮城三层、屈曲开门」一句本次抓取未含，待回看。
4. 如厕（马桶 / 茅厕）、床榻形制、窗纸 / 窗纱、炭盆取暖：本次未查（标「未查」，不删节）。
5. 番茄传入时间只有 F6 C02 的 T3 转述（无 URL），未核。
6. `kaifeng.myth.005` 服饰误传的出处未核页（衣角负责）。
7. `kaifeng.house.005` / `travel.012` / `travel.013` / `travel.017` 四条为 T2 页面转引 T0 原文，tag 记 ✅ 但 T0 原页尚未打开——进 prompt 前须回查《宋会要辑稿》《春明退朝录》《唐律疏议》《容斋随笔》。
8. 《清明上河图》店名题字「孙羊正店」「十千脚店」本次未在图上逐字核。

## 本次实际打开的来源（全部 WebFetch 成功、含逐字 quote）

- 维基文库《東京夢華錄》卷一 / 卷二 / 卷三 / 卷四 / 卷七 — https://zh.wikisource.org/wiki/東京夢華錄/卷一 …/卷七
- 维基文库《宋史》卷 175 — https://zh.wikisource.org/wiki/宋史/卷175
- 维基文库《老學庵筆記》卷四 — https://zh.wikisource.org/wiki/老學庵筆記/卷四
- 维基文库《夢粱錄》（四庫全書本）卷 13 — https://zh.wikisource.org/wiki/夢粱錄_(四庫全書本)/卷13
- ctext《東京夢華錄》索引页（十卷全） — https://ctext.org/wiki.pl?if=gb&res=712358
- 吴钩：澎湃「为什么说宋代发生了一场城市革命」 https://www.thepaper.cn/newsDetail_forward_1387938 ；「宋人用什么照明」 https://www.thepaper.cn/newsDetail_forward_1452541 ；搜狐转载「宋人才可以来一场说走就走的旅行」 https://www.sohu.com/a/464108112_99996707
- 澎湃「艺术开卷｜宋代的椅子」 https://www.thepaper.cn/newsDetail_forward_24921520
- 澎湃「谁人首载辣椒？」 https://www.thepaper.cn/newsDetail_forward_27299138
- 中新网「玉米番薯马铃薯传入」 https://www.chinanews.com.cn/cj/2023/05-13/10006435.shtml ；「大人」 https://www.chinanews.com.cn/m/cul/2015/04-21/7221935.shtml
- 文汇「隐食记｜清明美食」 https://wenhui.whb.cn/zhuzhan/xinwen/20200331/337397.html
- zh.wikipedia「缠足」 https://zh.wikipedia.org/wiki/缠足 ；「交子」 https://zh.wikipedia.org/wiki/交子
- Met Collection API（拉图实测）、Wikimedia Commons API（拉图实测）
- 图像：《清明上河图》Commons 局部（p1 ref01、p6 ref05、p7 ref01 三张已人眼核看）
