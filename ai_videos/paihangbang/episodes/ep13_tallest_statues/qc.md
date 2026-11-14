# ep13 · 世界最高雕像 · 审片记录（qc.md）

## 配乐审片 · 2026-11-04（独立上下文）

> 补配乐后由另起上下文的审稿代理测量（未参与制作）；脚本与数据在会话 scratchpad `audio_qc/`。只换音轨，视频流与 `render/_silent/` 原静音版逐流哈希一致（16654 帧）。

**结论：通过**，上面复核 blocker #1「配乐」已解决。
- 配乐：Suno 任务 2f127467，两首（10ae81b2 → 58490eaf），4 s 交叉淡化，fit=end，第二首放到自然结尾。
- 响度 −16.0 LUFS，真峰值 −3.9 dBTP；前十名段中位 −15.2（前段 −18.8），冠军停留与计分板最响（−13.3 / −13.5），最符合 bible「高潮对上前 10 名」；接点 179.9–183.9 s 从 −22 平滑升到 −14；片尾由 −15 淡到 −25，最后 0.5 s 近静音。无削波、断音或拼接爆音。
- `publish.md` 已补 Suno 署名与 Content ID 清单项。

## 复核 · 2026-11-04（返修后，独立上下文）

> 复核人另起上下文，没有参与制作，也没写第 1 轮审片。对照第 1 轮问题清单和 `_build/handoff.md`「按独立审片修改」一节，逐条核对**当前的** data.json、assets.json、sources.md、publish.md 和两版成片。只写本文件和 `_build/qc/recheck/`，没有改数据、图片或渲染。
> 复核产物在 `_build/qc/recheck/`：两版各 31 张全分辨率抽帧（`D_*.png` / `R_*.png`），包括片头、改动过的卡、洞察卡、冠军、计分板、来源卡、片尾，以及 5 个随机点 113.0 / 131.4 / 173.3 / 236.0 / 267.1 s（seed 1304）；拼图 `sheet_d1–5.jpg`、`sheet_r1–2.jpg`；AI 图与实拍对照 `ai_vs_real_1–3.jpg`、`ai_vs_real_phra_buddha_chok.jpg`；裁切细看 `D_181.1_crop.png`、`R_crop_kyaikhto_mukdahan_aizu.jpg`。

### 结论：**必须修**（只差一个 blocker：配乐）。配乐补好、Chimalli 生成图修好以后，可以按**默认版**发布

- 机检全部通过。两版都是 1920×1080、60/1、277.567 s，nb_frames 和逐包计数都是 16654，与 `rank_scroll timeline` 的 16654 帧（4:37.57）一致。两份 manifest 的输入 sha256（34 / 43 个）都与当前文件一致，输出 sha256 也一致。`validate --strict` 两版都 OK。
- 第 1 轮列的 3 个 blocker 里修好了 1 个（#3），1 个部分修好（#2），**#1 配乐没有动**：两版的音频仍是 `anullsrc`，volumedetect 测得 mean / max 都是 −91.0 dB，publish.md 自己也写着「无配乐（静音母版）」。
- 数据方面的两个 major（#6 Statue of Belief、#7 慈山观音）都修了，理由站得住，具体见下文。
- 新发现 1 个 major：有几张 AI 生成图画出来的造型和真实雕像不一样，Chimalli 差得最多。

**推荐发布默认版**，理由：
1. 风险版仍有 18 张许可不明的新闻、博客或旅游站图片。这类摄影师版权更容易被 Content ID 认领或收到下架通知。
2. 默认版现在 41 张卡里 32 张有图，FoP 安全的中、泰、墨三国已经全部有图。
3. 两版的雕塑 FoP 风险项完全相同（俄、乌、塞、印尼、菲、越），选风险版并不能减少这部分风险。

前提：用户按第 1 轮的 FoP 分级逐项签字，上传时「Altered or synthetic content」选 Yes。

### 原问题逐条

| # | 原严重度 | 状态 | 核对证据（当前文件 / 成片） |
|---|---|---|---|
| 1 | blocker | **未修** | 两版音轨 −91.0 dB，manifest 的 ffmpeg 参数仍是 `anullsrc`；publish.md「其他」写「配乐由主代理统一做后重渲」。仍是 blocker |
| 2 | blocker | **部分修 → 降为 major** | 占位从 18 张降到 9 张，FoP 安全国家的 9 项都换成了 AI 图。但日本 5 项、台湾 1 项没有补；第 1 轮建议这 7 项也补图，因为日 / 台用在视频里风险低。占位还是集中在片头：0:16 Usami，0:30–0:57 的 6 张卡里有 4 张占位（Koxinga、Victor、Tokyo Bay、Aizu）（`sheet_d1.jpg`）。之后在 1:28、1:38、2:20、2:36 还各有 1 张 |
| 3 | blocker（风险版） | **已修** | 炎黄二帝两版都换成生成图，画面无人、无横幅（`R_21.2.png`） |
| 4 | major（风险版） | **已修** | 赤山明神改用生成图；Tokyo Bay 换 Travel.jp 特写，The Victor 换 JG Summit 新闻稿图，两张都是许可不明，不再有写明 All rights reserved 的图；publish.md 也改成「18 张许可不明（已剔除…All rights reserved 的图）」 |
| 5 | major（风险版） | **已修（Kyaikhto 部分修）** | Aizu 头部完整；Victor 换了新图，拳头和头都露出来了，没有被国旗挡（`R_41.1.png`）；Kyaikhto 脸能看到了，但肉髻被卡片上沿切掉，国旗紧贴头侧（`R_crop_kyaikhto_mukdahan_aizu.jpg`），可以接受 |
| 6 | major | **已修，推算站得住** | 见下方「Statue of Belief 78.9 m」。description 已不再依赖 #3/#4 先后，只写「Spring Temple Buddha is 108 m here, not the 128 m」 |
| 7 | major | **已修** | 慈山观音已剔除（N 42→41，标题 / kicker 改为 TOP 41，计分板 China 12，合计 41）；置顶评论「Not included」列出了它。官方说法：总高 76 m = 70 m 铜像（含三层铜莲座）+ 6 m 花岗岩基座，剔除理由与 scope_note 一致。遗留：Son Tra 67、Guishan 99、Kaga 73 只查到总高，按原值保留，sources 有注明。实际执行的是「能确认含莲座才剔除」，建议在 sources §2 写成明文规则（minor） |
| 8 | major | **已修** | 两版 Mother Ukraine 都换成 Pexels（Ev Vekselman）的三叉戟盾牌照片，badge 与画面一致（`D_103.7.png`） |
| 9 | major（法律） | **待用户签字**（制作方改不了） | 默认版照样放了 Motherland Calls、Mother Ukraine、African Renaissance、GWK、Son Tra、Dordenma 及日本 4 项（Ushiku / Sendai / Hokkaido / Shodoshima alt）；publish.md 已写明须逐项签字 |
| 10 | minor | **已修** | 9 张占位都写「Photo withheld: licence unclear」 |
| 11 | minor | **未修** | 风险版 Yang'asha 仍是 820×510，Kyaikhto 仍是 847×635 |
| 12 | minor | **未修** | Emei 和 Shodoshima alt 仍是远景（`D_46.4.png`、`D_5.2.png`） |
| 13 | minor | **已修（Luang Pho Yai 仍未核）** | publish 数字改成 18。Luang Pho Yai 的 PD 许可页仍未打开核对，publish.md 列了待办 |
| 14 | minor | **已修** | 置顶评论开头加了 Not included 名单（9 项含慈山观音） |
| 15 | minor | **已修** | 描述框 Image credits 末尾加了 CC BY 2.0 链接 |
| 16 | minor | **部分修** | sources §4 #3 现在写「With the throne it would rank No. 2 (… so Laykyun stays ahead under either consistent rule)」。前半句仍是「No. 2」，与后半句矛盾，改成「it would still rank No. 3」 |
| 17 | minor | **已修** | 洞察 1 链接改成 `home.nps.gov/.../statue-statistics.htm` |
| 18 | minor | 未修（可留到下期） | 文件名 NN 仍不等于名次 |

### Statue of Belief 78.9 m（问题 #6）专项

- 维基条目原文：「The overall statue is 369 feet (112 m) tall; the pedestal is 110 feet (34 m) tall」，观景廊分别在 20 / 110 / 270 ft，其中 110 ft 那层正好在台座顶。The Daily Guardian 也写「34 m high pedestal, reaches 112 m」。Explore Our India 给的是另一组数：「base 110 feet… Shoulder height is 260 feet and Lord Shiva's Trishul reaches 351 feet」。几个来源的台座都是 110 ft，说明 110 ft 台座的说法稳定。
- 351 ft 的含义有两种解释：data.json 采用的是「施工期总高，后来头顶加了恒河水饰」；Explore Our India 则说是三叉戟顶的高度。两种解释都落在 110 ft 台座之上，并不冲突。按本期口径「到形象最高点（含手持物）」，最高点是 369 ft 的头饰，所以本体 = 369 − 110 = 259 ft = 78.9 m。推算**站得住**。
- 余量：78.9 m 是推算值，不是官方直接公布的；369 和 110 都是取整数。#11–#14 四项（79 / 78.9 / 78 / 77.9）相差都不到 1.1 m，所以只要偏差 1–2 m，这四项的先后就会变。但 #12 的显示值有出处，推算方法在 notes 和置顶评论（「its 112 m includes a 34 m pedestal」）里都写了，**可以发**。另外，WPL 列表写的「106 m statue」等于把台座当成 6 m，notes 已解释这和 110 ft 台座矛盾。
- 可选：在 sources notes 里补上 Explore Our India「三叉戟顶 351 ft」这一说法（得 241 ft = 73.5 m，那会排到约 #17）。这样评论区有人质疑时能直接指向。

### 新问题

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| N1 | **major** | 两版 AI 生成图（默认版 9 张，风险版里的赤山明神、炎黄二帝 2 张） | AI 标记**没有缺**：每张都有黄色「AI IMAGE」标签，右下署名写「AI-generated image, not a photo」，描述框写「9 images marked AI-generated are illustrations, not photos」，置顶评论也说明了，上传清单要求勾选合成内容。所以从披露的角度看不算冒充。但 prompt 要求的是「Realistic documentary travel photograph」，出来的是照片质感，卡上又写着真实雕像的名字，观众会默认「这尊像就长这样」。逐张与风险版实拍对照（`ai_vs_real_*.jpg`）：**Guerrero Chimalli 造型完全不对**：实物是 Sebastián 的立体主义红钢抽象人形，胸前是尖角星形盾，举起的手臂是观景台，立在大道中间的高柱上；生成图却是羽冠阿兹特克武士，手持权杖，配圆形放射纹盾牌，站在白色方座上。这等于把一件在世艺术家的作品画成了另一件东西，墨西哥观众一眼就能看出来。**赤山明神**：生成图是高冠、执笏、背景有海；实物是坐像，立在楼阁台基上。**仰阿莎**：生成图是双臂张开、立在城镇的圆形多层台座上；实物身形修长、手在胸前、站在山顶。Phra Buddha Chok（火焰形顶髻对应素可泰样式，实物是清盛样式的短螺髻）、Mukdahan、云城关公只是细节不同；九华地藏、尼山孔子、炎黄二帝与实物接近。另外 bible §主图来源优先级写的是「AI 生成的**风格化**插图」，本期出的是写实照片风格 | Chimalli 发布前必须处理：按实物特征重写 prompt 重新出图（立体主义红钢板块、星形尖角盾、高柱、大道），或者在 Flickr / 官方渠道再找一次可商用实拍。墨西哥属 FoP 安全国家，实拍没有雕塑版权问题；实在不行就改回占位。赤山明神、仰阿莎按实物重写 prompt。之后出图建议按 bible 偏风格化，或至少不要「documentary photograph」措辞 |
| N2 | minor（风险版） | #28 Mukdahan（1:13） | 风险版主图是手部特写，佛脸被卡片右沿切掉（`R_crop_kyaikhto_mukdahan_aizu.jpg`），一眼认不出是整尊大佛 | image_focus 往右上调，或者换图 |
| N3 | minor | publish.md 署名 | AI 图的署名写成「AI-generated (AI-generated (Codex image_gen))」，括号重复 | 改成「AI-generated illustration (Codex)」 |
| N4 | minor | 默认版节奏 | 第 1 轮 #2 的遗留：0:30–0:57 的 6 张卡里有 4 张占位，只隔着 Dordenma、Emei 两张远景 | 优先给日本 4 项、台湾 1 项补图（这两地风险低） |

其余顺带核对，未发现问题：
- 名次 1–41 按标准竞赛排名连续（6/6、15/15、23/23、26/26、38/38/38），与 value 一致。
- 6 张洞察卡的 after_rank 都对。Liberty 卡提前到 #37 之后（0:26）。「4 statues since 2022」在 #11 之后，这时 4 尊都已经出场，作为回顾成立。「Spring Temple」卡在 #3 之前，「Next: Statue of Unity, 66 m」= 182 − 115.8。
- 洞察 3 说日本 9 项，与计分板一致。
- 计分板 China 12 / Japan 9 / Thailand 5 / India、Myanmar、Indonesia、Taiwan 各 2 / 其余 7 国各 1，合计 41。
- 抽帧里没有文字出框，长署名会自动缩小字号。片头、冠军（182 m / 597 ft、光晕）、来源卡、片尾都完整。
- 描述框章节时间 1:02 / 1:59 / 3:01 / 4:09 与 timeline 对得上；「3:58 No. 1」是 #1 卡从右侧进场的时间，champion 段实际从 4:02.6 开始，可以接受。
- request_log 有本期 9 次 Codex 出图的记录。

### 发布前还要做

1. 补配乐后两版重渲，按 §7-6 用 ebur128 查响度和片尾淡出（blocker #1）。
2. 处理 Chimalli 生成图；赤山明神、仰阿莎建议重出（N1）。
3. 用户对 FoP 风险项逐项签字（#9）；Luang Pho Yai 的许可页点开确认（#13）。
4. 可选：日本 / 台湾占位补图（#2 / N4），sources #3 备注改一句（#16），署名格式（N3）。

---

## 第 1 轮独立审片 · 2026-11-04

> 独立审片人（另起上下文，未参与制作）。依据：README Vision、bible §2–§4、§7，data_contract v1.4，本期 topic / data / sources / assets / publish / handoff。只写本文件和 `_build/qc/`，没有改数据、图片或渲染。
> 审片产物：`_build/qc/contact_1–6.jpg`（全部 44 张上屏图，含 alt）、`_build/qc/sweep_{d,r}_01–10.jpg`（两版每 5 s 抽一帧）、`_build/qc/frames/`（全分辨率抽帧）、`_build/qc/decode_check.txt`（逐帧解码与音量）。

### 结论：**必须修**（两个版本现在都不能直接发布）

- 默认版：没有配乐；18 张占位卡（43%），前 12 张卡里有 8 张是占位，片头最容易流失观众的一分钟大半没有照片，也违反 follow-up 020「每张卡都必须有高质量图」。
- 风险版：#38 用的是一张有可辨认真人和活动横幅的合影，另有 3 张来源页明写 All rights reserved 的新闻 / 官方图，还有 2 张图把雕像头部裁掉了。
- 数据整体可信：名次、排序、英尺换算、计分板都对，抽查 15 条主值全部有出处。但 #3/#4 的先后（Statue of Belief 107 m 还是 112.5 m）和慈山观音含不含莲座这两处口径没有落实，会直接影响片头卖点「the usual No. 2 drops to No. 3」。

**发布主版本建议**：两版都不按现状发。以默认版为底，做一个「默认版+」：
1. 补配乐。
2. FoP 安全的国家（中国 6、泰国 2、墨西哥 1 项）先补可商用实拍；找不到就按 bible §4（follow-up 031/032）用 Codex 出图兜底，这几国用照片或插画都没有雕塑版权问题。
3. 日本 6 项、台湾 1 项也按同样办法补图。日 / 台条款只排除「出售复制品」，用在视频里风险低。
4. 剩下的 FoP 高风险项由用户逐项签字（见下方 FoP 分级）。

风险版不要作为主版本：它的主要风险来自摄影师版权（20 张许可不明或明确保留权利），这条路比雕塑 FoP 更容易收到 Content ID 认领或下架通知。

### 问题清单

| # | 严重度 | 位置 | 证据 | 建议修法 |
|---|---|---|---|---|
| 1 | **blocker** | 两版全片 | `decode_check.txt`：音轨是 `anullsrc` 静音，mean/max −91 dB；publish.md 也写了「无配乐（静音母版）」。bible §5、§7-6 要求每期一首配乐，前 10 名进高潮，片尾淡出 | Suno 出曲（`_build/suno_bgm_v2.json` 已有 prompt，先记 request_log），`render --music … --music-fit end` 重渲；之后按 §7-6 用 ebur128 查响度，确认 4:14 后淡出 |
| 2 | **blocker** | 默认版 #42–#11（0:05–3:00） | 18/42 张为「Photo withheld」占位。#42–#31 共 12 张里占位 8 张（Chimalli、Usami、Yan & Huang、Koxinga、Victor、Tokyo Bay、Aizu、Red Mountain），之后 #29–#23 又有 5 张；top 10 全部有图。违反 follow-up 020 / 031：默认版用可商用 `image_alt` 顶替，找不到才由 Codex 出图，不出占位卡 | 见上方「默认版+」。优先补 FoP 安全国家的 9 项和日 / 台 7 项。实在补不齐，至少不能让占位卡集中在片头 |
| 3 | **blocker（仅风险版）** | 风险版 #38 Emperors Yan and Huang（约 0:15–0:25） | `40_emperors_yan_and_huang.jpg` 前景是十余位可辨认的真人举着「2026 中国网络媒体论坛·寻访斯诺足迹·中外大V河南行」横幅，原图右上角还压着活动 logo。雕像只是远处背景。这张图同时涉及肖像、活动品牌和水印类叠字 | 换成只拍雕像的图；没有就改用占位或出图 |
| 4 | **major（仅风险版）** | 风险版 #31 / #34 / #35 | assets.json 里 God of Red Mountain（新浪「我是图文时代」）、Tokyo Bay Kannon（千叶官方旅游站）、The Victor（BusinessWorld）三张的许可**明写 All Rights Reserved**，不是「许可不明」。publish.md 统一写成「许可不明」，低估了风险 | 风险版也不要用明确保留权利的图。如果签字，签字单要按「明确禁止 / 许可不明」分开列 |
| 5 | **major（仅风险版）** | 风险版 #14 Kyaikhto（约 2:40）、#32 Aizu Jibo（约 1:00）、#35 The Victor（约 0:32） | 抽帧 `R_0160.0.png`：Kyaikhto 卡只剩手和袈裟，脸被卡片上沿切掉，国旗又压在头部位置。`R_quad.png`：Aizu 的头部出了卡片上沿；Victor 举起的拳头和头被国旗挡住 | 调 `image_focus`（Kyaikhto 约 [0.4,0.0]，Aizu 约 [0.5,0.0]），或换图；Victor 换竖幅图，或把焦点下移、留出国旗的位置 |
| 6 | **major** | 两版 #3/#4、description 首句 | Statue of Belief 主值 107 m 取自施工方行业刊物 NBM&CW 的「351 ft」，该文没说是不是本体。维基正文写「overall statue 369 ft (112 m)… pedestal 110 ft」，揭幕新闻也一律写 369 ft；另有说法称 351 ft 是到三叉戟顶、369 ft 含头顶恒河水饰。如果 369 ft 是像本身（含头饰），它就是 112.5 m，会排到 #3，春泉大佛退到 #4，片头卖点「the usual No. 2 drops to No. 3」不再成立。topic 待确认 2 已提到这个问题，但没有结论 | 找建设方 / Miraj 集团 / 官方旅游部门的分项数据（像高 vs 台座）。找不到时：要么在 sources 和置顶评论里写明「351 ft 施工方数字，另有 369 ft 说法」，并把 description 改成不依赖 #3/#4 先后的说法（如「Spring Temple Buddha is 108 m here, not 128 m」）；要么两者并列 |
| 7 | **major** | #20 Tsz Shan Guanyin | sources.md 写 70 m「incl. three-tier lotus」，即**含莲座**；春泉大佛、拉开坤、灵山、九华地藏、牛久都按口径去掉了莲座或宝座。scope_note 明写「not its lotus throne」，这一条与口径冲突 | 查慈山寺资料里的像身高。查不到的话：要么在 notes 和 sources 标「本体含莲座，本体高未公开」，要么按同类处理剔除。顺带复核 Son Tra 67 m、Guishan 99 m、Kaga 73 m 是否也含莲座 |
| 8 | **major** | 两版 #24 Mother Ukraine（约 1:40–1:50） | 默认版和风险版共用的 `26_mother_ukraine.jpg`，盾牌上还是**苏联国徽（锤镰）**（`_build/qc/zoom_26_mother_ukraine.jpg`），旁边的 badge 却写「SHIELD CHANGED 2023」，名字也是 Mother Ukraine。Codex 候选备注里已经提示过这张是 historic shield。乌克兰观众会觉得刺眼，画面和 badge 也互相矛盾 | 换 2023-08 以后、三叉戟盾牌的照片（候选里有 haydamak.net 一张，许可不明；Pexels / Unsplash 上应有 2023 年后的照片）。实在没有就去掉 badge |
| 9 | **major（法律）** | 默认版 12 张 FoP 项 | 默认版照样放了 Laykyun、Ushiku、Sendai、Hokkaido、**Motherland Calls（#10）**、GWK、Son Tra、**Mother Ukraine**、Emei、Dordenma、Shodoshima alt、**African Renaissance**。照片许可干净，但雕塑版权仍在（sources §3 自己也这么写）。所以「默认版 = 安全版」的前提不成立 | 发布前由用户逐项签字，分级见下节。签字范围至少包括俄、乌、塞、印尼、越 5 国 |
| 10 | minor | 默认版占位卡文字 | Kaga、Kurume、Aizu、Tokyo Bay、Usami 写「Photo withheld: sculpture copyright」，可同为日本的 Ushiku / Sendai / Hokkaido 却有图。真实原因是图片许可不明，不是雕塑版权（data_contract 要求 image_note 写真实原因） | 如果保留占位，统一改成「licence unclear」 |
| 11 | minor | 风险版画质 | 只有 Yang'asha（820×510，卡上约 1.6× 放大，`R_0107.0.png` 明显发软）和 Kyaikhto（847×635，约 1.3×）在 1080p 满版卡上看得出糊。其余 5 张低清图（Confucius 640×924、Kurume 768×1024、Usami 1024×768、Sibea-bea 1080×720、Victor 1280×720）在 600×800 卡上缩放 ≤1.1×，不明显（`lowres_check.png`）。handoff 担心的「7 张低清」实际只有 2 张需要处理 | Yang'asha 和 Kyaikhto 换更高清的图 |
| 12 | minor | 默认版 #33 Emei、#39 Shodoshima alt | 两张都是远景，雕像只占卡面约 1/6（`D_0053.0.png`、`D_0006.0.png`）。能认出来，但张力不够 | 有更近的可商用图就换 |
| 13 | minor | publish.md「两个版本选哪个」 | 写「21 张许可不明」，按 data.json 实际是 20 张（其中 3 张明确保留权利，见 #4）。Luang Pho Yai 的 PD 许可页 403，没有亲自核对过 | 改数字；Luang Pho Yai 发布前点开许可页确认 |
| 14 | minor | description / 置顶评论 | 维基表里的 Mother of All Asia（98.15 m，会排 #7）、越南开元寺 72 m、清莱观音、太湖观音等 9 项被剔除，屏上和描述都没有提。评论区一定会有人问 | 在置顶评论「How we measured」后加一行「Not included (figure height unconfirmed): Mother of All Asia, …」，指向 sources |
| 15 | minor | description 署名 | CC BY 2.0 的 6 张，许可链接只在置顶评论里。评论可能被折叠或删除，CC BY 要求有许可链接 | 描述框 Image credits 末尾加一行 `CC BY 2.0: https://creativecommons.org/licenses/by/2.0/` |
| 16 | minor | sources.md §4 #3 备注 | 「With the throne it would rank No. 2 (128 m < 129.2 m Laykyun …)」前后矛盾：两者都含座时，春泉大佛仍是 #3 | 改成「With the throne it would still rank No. 3」 |
| 17 | minor | sources.md 洞察 1 链接 | NPS 链接 301 跳转到 `home.nps.gov/stli/learn/historyculture/statue-statistics.htm` | 更新链接 |
| 18 | minor | 文件命名 | `assets/img/NN_*` 的 NN 不等于名次（如 08 是 #7，44 是 #42），与 data_contract「NN = 名次两位」不一致 | 不影响成片；下期按契约命名 |

### 版权 / FoP 分级（发布签字参考）

| 风险 | 国家（本期项） | 理由 |
|---|---|---|
| 最高 | 塞内加尔（African Renaissance） | 无商用 FoP；时任总统 Wade 公开主张该像的知识产权并要求分旅游收入，是少数权利人明确主张过权利的大型雕像 |
| 高 | 俄罗斯（Motherland Calls，#10）、乌克兰（Mother Ukraine） | 民法 / 著作权法明确排除雕塑为主体的营利使用；作者版权有效（Vuchetich 1974 年去世，版权至 2044 年；Borodai 2010 年去世） |
| 高 | 菲律宾（The Victor）、印尼（GWK、Sibea-bea） | 无 FoP；Victor 是 2023 年私人开发商（Robinsons Land）的地标，GWK 雕塑家 Nyoman Nuarta 在世，园区商业化经营，权利人明确、容易找到 |
| 中 | 越南（Lady Buddha） | 2023 年新法明确只允许非商业使用 |
| 低（实务） | 缅甸 2、不丹 1 | 法条上没有 FoP，但执法和主张都极少 |
| 低 | 日本 9、台湾 2 | 条款只排除「以出售复制品为目的」，视频使用多数解读可以 |
| 安全 | 中国 13（含香港）、印度 2、泰国 5、墨西哥 1；乐山大佛为公有领域 | 法定 FoP 覆盖公共场所的雕塑摄影和录像 |

结论：默认版现在的处理正好反了。FoP 最危险的俄、乌、塞、印尼、越 5 项照放，FoP 安全的中国、泰国、墨西哥 9 项却因为照片许可变成占位。优先补后者的图，前者交用户签字。

### 核对过的数据样本（WebSearch / WebFetch，2026-11-04）

| 名次 | 雕像 | 本期值 | 核对结果 | 结论 |
|---|---|---|---|---|
| 1 | Statue of Unity | 182 m / 240 m 含座 | 维基与多源：182 m 像 + 58 m 座 = 240 m | ✅ |
| 2 | Laykyun Sekkya | 115.8（显示 116）/ 129.2 | 维基 116 m / 129.2 m；OrangeSmile 116 m + 13.4 m 座 | ✅ |
| 3 | Spring Temple Buddha | 108 m（含莲座 128） | 郑州晚报 PDF 与景区资料：佛身 108 + 莲花座 20 + 金刚座 25 + 须弥座 55 = 208 | ✅ |
| 4 | Statue of Belief | 107 m（351 ft） | NBM&CW 只给「351 feet tall statue」，没有分项；维基 369 ft overall、pedestal 110 ft；揭幕新闻（Tribune、Deccan Herald）都写 369 ft | ⚠️ 见问题 #6 |
| 5 | Ushiku Daibutsu | 100 / 120 | 多数日文源写像高 100 + 台座 20 = 120（tabi-mag 写 110，为少数） | ✅ |
| 10 | Motherland Calls | 85 m 含剑 | 维基：像 52 m + 剑 33 m = 85 m；一说 85 m 是「剑尖到基座顶面」 | ✅ |
| 11 | Ksitigarbha of Jiuhua | 84 / 99 | 新浪 2013-08-31 与百科：像身 84 m，加莲花座 99 m，2013-08-31 开光 | ✅（维基 76 m 是旧数） |
| 15 | Garuda Wisnu Kencana | 75 / 121 | Jakarta Post：75 m 像 + 台座，共 121 m；2018-09-22 揭幕 | ✅ |
| 21 | Wat Paknam Great Buddha | 69 m，Inaugurated 2023 | 泰媒（Matichon / Thairath）：69 m、膝宽 40 m，2566-02-05（2023）国王主持 สมโภช 典礼；2021 年完工 | ✅ |
| 24 | Mother Ukraine | 62 / 102；SHIELD CHANGED 2023 | AFP 62 m 像，Kyiv Independent 102 m（含馆）；2023-08-06 换三叉戟 | ✅（照片问题见 #8） |
| 27 | Jesus of Sibea-bea | 61 m，2024 | The Star：61 m，2024-09-19 揭幕（另一来源写 9-21） | ✅ |
| 35 | The Victor | 55 / 60 | Inquirer / GMA：55 m + 5 m 台 = 60 m，2023-08 揭幕 | ✅ |
| 36 | Buddha Dordenma | 54 m | 廷布宗政府网站、维基：54 m（177 ft）；旅游站另有 51.5 m（169 ft） | ✅ |
| 42 | African Renaissance | 49 m | 多数来源 49 m（个别 50 / 52 m），2010-04-03 揭幕 | ✅ |
| 洞察 1 | Statue of Liberty 46 m | 46.05 m（151 ft 1 in，基座顶到火炬） | NPS 统计页（链接已 301 跳转） | ✅ |
| 洞察 2 | Jingzhou Guan Yu 2021–22 拆除 | 2021-09 开拆，2022 上半年拆完；迁建到点将台，截至 2023-04 未开工 | ✅（「took down」属实；原像 57.3 m 含约 10 m 底座，像身 < 49 m，重建后也进不了榜） |

其余机检：42 项名次按标准竞赛排名连续、与 value 一致；ft = m × 3.28084 取整，全部正确；计分板 China 13 / Japan 9 / Thailand 5 / India 2 / Myanmar 2 / Indonesia 2 / Taiwan 2 / 其余各 1，与 data.json 一致；国旗逐张对过（台湾用台湾旗、香港计入中国，符合 topic 口径）；scope_note 516 字符（≤ 600）；`validate --strict` 两版都 OK；描述框章节时间码（1:07 #30、2:05 #20、3:06 Top 10、4:03 No. 1、4:14 计分板）与抽帧对得上；标题 44 字符。

### 图片逐张认对象（contact_1–6）

- 认对且构图可用：#1、#2、#3（横幅，竖裁后像居中）、#4、#5、#6（Guishan 只拍到上半身千手部分，不是全身，可以接受）、#7 ×2、#9（Flickr 原页标题「88 meter-tall Dai-Kannon, Ashibetsu」）、#10、#11、#12、#13、#15 GWK、#17 Kaga（金色抱子观音，天空调色重但不是 AI）、#18、#19 主图与 alt、#20、#21、#22、#23（苗族银角头饰）、#24 Kurume、#26（Xiqiao 照片偏棕褐调）、#27 两项、#29、#30（鱼眼畸变加眩光，质量一般）、#31、#33、#34、#36、#37、#39 ×3、#42。
- #4 Statue of Belief：来源页 wordpress.org 本机抓不到。按维基描述核对造型：铜色、盘坐、一膝竖起、三叉戟在左手侧、颈上有蛇，全部吻合，认定为 Nathdwara 像。
- 有问题：#24 Mother Ukraine（旧国徽，#8）、#38 Yan & Huang（合影，#3）、#14 Kyaikhto / #32 Aizu / #35 Victor（裁切，#5）、#23 Yang'asha（糊，#11）。
- AI 痕迹：未发现。账本没有 AI 生成图，publish 里「Altered or synthetic content = No」与之一致。

### 成片核对

| 项 | 默认版 | 风险版 |
|---|---|---|
| 分辨率 / 帧率 | 1920×1080，60/1 | 1920×1080，60/1 |
| 时长 | 282.900 s | 282.900 s |
| 帧数 | 容器 nb_frames 16974；**ffmpeg 逐帧解码 16974**，与 timeline 一致（282.9 × 60），没有截断 | 同左，16974 / 16974 |
| 输入一致性 | manifest 26 个输入的 sha256 全部与当前文件一致；输出 sha256 与 manifest 一致 | 44 个输入全部一致 |
| 编码 | libx264 CRF 16，平均 1.70 Mbps（滚动画面压缩率高，抽帧未见块效应） | 1.80 Mbps |
| 音频 | AAC 静音（−91 dB）→ 问题 #1 | 同左 |

### 抽帧清单（`_build/qc/frames/`，全分辨率亲眼看过）

| 文件 | 时间 | 内容 | 结果 |
|---|---|---|---|
| D_0002.0 | 0:02 | 片头标题 / 口径行 / 来源行 | ✅ |
| D_0006.0 | 0:06 | 第 N 名 #42 African Renaissance、#39 Chimalli 占位、Shodoshima alt | 占位（#2）；Shodoshima 远景（#12） |
| d_t10 / d_t12.5 / d_t15 / d_t20 / d_t25 | 0:10–0:25 | #39 三张并列、#38–#36 | 文字完整；占位集中（#2） |
| D_0038.0 | 0:38 | 洞察卡 1 Statue of Liberty | ✅ 文字在框内，有出处 |
| D_0053.0 | 0:53 | #34–#32（Emei 远景、2 张占位） | #10、#12 |
| D_0075.0 | 1:15 | 洞察卡 2 China / Jingzhou | ✅ |
| D_0097.0、D_0118.0 | 1:37、1:58 | #26–#24、#22–#20 | Mother Ukraine 旧国徽（#8） |
| D_0128.0 | 2:08 | 洞察卡 3 Japan 1994 | ✅ |
| D_0153.0、D_0166.0 | 2:33、2:46 | #17–#13 | 默认版 #11–#18 有 5 张占位 |
| D_0178.0 | 2:58 | 洞察卡 4 since 2022 | ✅ |
| D_0190.0 | 3:10 | 第 10 名附近 Motherland Calls（TALLEST IN EUROPE） | ✅ 放大正常 |
| D_0205.0、D_0214.0 | 3:25、3:34 | #7–#4 | ✅ |
| D_0225.0 | 3:45 | 洞察卡 5 春泉大佛 128 m | ✅ 文字清楚；它出现在 #3 卡之前，解释到位（是否成立取决于 #6） |
| D_0233.0 | 3:53 | #3 / #2 | ✅ |
| D_0243.0 | 4:03 | 洞察卡 6 + #1 进场 | ✅ |
| D_0250.0、D_0252.0 | 4:10、4:12 | 冠军（光晕、No. 1 面板 182 m / 597 ft） | ✅ |
| D_0257.0 | 4:17 | 计分板（11 条 + 「3 more」） | ✅ 与 data 一致 |
| D_0262.0 | 4:22 | 来源卡 | ✅ |
| D_0275.0、D_0282.8 | 4:35、4:42.8 | 片尾 | ✅ 最后一帧完整，18 s 干净 |
| R_0020.0、R_0032.0、R_0060.0、R_0070.0、R_0088.0、R_0107.0、R_0140.0、R_0160.0、R_0243.0 | 风险版 | Yan & Huang 合影、Victor、Aizu、Mukdahan、Sibea-bea、Yang'asha、Confucius / Kaga、Kyaikhto、冠军 | 问题 #3、#5、#11；其余 ✅ |
| sweep_d/r_01–10 | 两版每 5 s | 全片版式巡检（拼图缩小后会出现文字叠影，那是看图缩放造成的；按全分辨率帧 `chk_ghost.png`、`d_t10_crop.png` 复核，成片无叠影） | ✅ |

### 观众视角（全球英文观众）

- **亮点**：这一期有真正反常识的内容：「自由女神进不了榜」「常说的第 2 名其实第 3」「中国开始限高并拆掉了关公」「日本 30 年没再建」；冠军差距「66 m taller than any other」也很有力。卡片解剖清楚，3 秒内能读出名称和数值。
- **会划走的地方**：0:05–1:10 前 12 张卡里 8 张是大国旗加「Photo withheld」，观众会以为片子坏了，或觉得是在凑数。现在第一张洞察卡在 0:38 才出现，最好提前到片头。佛像和观音像连着出现 30 多张，容易审美疲劳，Motherland Calls、The Victor、GWK、Chimalli 这几张异形雕像正好用来调节节奏，至少要保证它们有图。
- **评论区预判**：「春泉大佛明明 128 m」（已有洞察卡和置顶评论应对）、「Mother of All Asia 去哪了」（#14 建议补）、「Statue of Belief 是 369 ft」（#6）、「Mother Ukraine 盾牌早换了」（#8）。
