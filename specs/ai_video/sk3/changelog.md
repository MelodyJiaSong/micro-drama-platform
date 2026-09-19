# sk3 · changelog

## 2026-09-18 · 阶段 0 调研纠正 001 — Bloodworth 名言查无一手出处
Source: `0_research/parts/w1_timeline_people.md`（`london1666.people.004/005/006/007`）
Summary: 开站时用作「示警失败有史料记载」论据的那句市长原话「Pish! A woman might piss it out」，经全文检索**不在皮普斯日记中**，最早只能追到 Malcolm《Londinium Redivivum》vol.4（1807，事发 141 年后）；剑桥大学图书馆特藏组亦只写 "was said to have remarked"。选站结论**不变**（失败本身另有 T0 依据：《伦敦公报》官方通告认定「本该拆房断火而未办」，以及皮普斯 9/2 正午在坎宁街亲耳所闻的市长崩溃之词），但依据已更换。

Auto-updated:
- `ai_videos/shikong_lvxing/proposal.md` — A §2 的 I-5 分型行：把判据从「有一句名言」改写为「失败本身有记载」，并写明本次踩坑
- `specs/ai_video/sk3/divergence.md` — D1 边界 ③：写死 Bloodworth 不得说该句，给出可用的 T0 替代原话与「间接提及 + 当场点明查无出处」的处理方式
- `ai_videos/shikong_lvxing/_series/format_teardown_chloe.md` — §7 选站四问第 2 问：补一条教训「名言的传播度和史料强度经常反着来，选站时先去查那句话的脚注」

No conflicts found in: `specs/ai_video/sk3/user_input/raw_prompt.md`（未引用该句）

## 2026-09-18 · 阶段 0 决策 002 — 三项结构拍板（用户选定）
Source: 阶段 0 调研 w1/w4/w5 结论 + 用户 2026-09-18 多选题回答
Summary: ① 时间跨度 9/1 清晨 → 9/2 黄昏（Titanic 同构，破 I-1）；② 皮普斯任「跟着的那个人」并可念有记载的原话（破「真实名人只远景静默」）；③ 旅行者的注定失败的任务＝赶在打烊前找到布丁巷那家面包铺、劝他今晚把炉子扒干净。

Auto-updated:
- `specs/ai_video/sk3/divergence.md` — 新增 D5（时间跨度 + 合规与灾后事实分区四条边界）、D6（皮普斯的四条边界，含「火场唯一合法逐字引语只有市长那句」）

待办（进阶段 1 时落 concept.md）：任务的立下点（对标 Titanic 第 39 秒）与失败点（对标第 10 分钟）写进一日时间线。

## 2026-09-18 · 阶段 0 完成 003 — dossier 过 K34，系列公共库接入 sk3
Source: 六路并行调研 w1–w6（`.audit/adhoc_agents/2026-09-18/sk3-20260918-211545/spawns/`）
Summary: dossier 15 节齐 + §0/§0b；253 条事实（242 ai_read / 11 ai_draft 已隔离）、机检 0 blocker；参考图库 9 资产 130 张公版图全部过 ≥8 门槛。

Auto-updated:
- `ai_videos/shikong_lvxing/sk3/0_research/dossier.md` — 新建，15 节 + §0 三条会改变创作的结论 + §0b 六条待人工抽查
- `ai_videos/shikong_lvxing/_series/glossary.md` — 追加 sk3 称谓白/黑名单（量化依据＝Pepys 全日记命中计数）与 TTS 读音表；并给 2026-09-14 那条「当地人不开口」的抬头加了站型分叉范围
- `ai_videos/shikong_lvxing/_series/blacklist.md` — 追加 L01–L18（英语/近代欧洲组）
- `ai_videos/shikong_lvxing/_series/sources.md` — 追加 §3 英格兰·伦敦，含三条抓取避坑与两条未取到的来源
- `.claude/agent_refs/project/ai_video.md` — 新增 rule **18.1b** 适用边界（画类史料：风格参考禁、保留原构图的 img2img 放行、人物一律不放行、铜版线条两步走、年代状态先对账）
- `specs/ai_video/sk3/divergence.md` — 新增 D7（画类史料进上传窗口，仅限地点建筑）
- `tools/ref_fetch.py` — **修真 bug**：`_next_index()` 与 `append_ref()` 并发不安全，同一 asset_dir 并行 pull 会重号并漏索引（本次实测 10 个重号、1 个漏索引）。加按 asset 目录的文件锁，索引分配与 refs.md 改写在锁内、下载在锁外；4 线程 48 次分配复测零重号。不同 asset_dir 仍可并行

No conflicts found in: `raw_prompt.md` · `revised_prompt.md` · `proposal.md`（分型表已于 001 更新）

## 2026-09-18 · 阶段 1 完成 004 — concept.md 落地
Source: 用户选定旅行者 c5 妮娅（Nia Brooks，美国，前高中历史老师）+ 阶段 0 dossier
Summary: 立项策划单按系列概念卡体例（对齐 sk1）落地，Titanic 型三件套写死：任务＝赶在打烊前找到布丁巷那家面包铺并劝他扒炉子（开场 01:00–01:45 立下、傍晚段八失败）；倒计时＝九点宵禁钟→午夜→凌晨一点；脊柱＝远远跟着皮普斯过完这一天一夜。片长 15–16 分钟、44–48 镜。

Auto-updated:
- `ai_videos/shikong_lvxing/sk3/1_立项/concept.md` — 新建
- `ai_videos/shikong_lvxing/sk3/README.md` — 新建（中文，CLAUDE.md 硬要求）

待办（阻塞阶段 2）：
1. **旅行者名册卡与站型分叉不一致**——`_series/characters/c1–c6` 六张卡的「在节目里」段都写着「当地人一律不开口；她不采访、不和任何人交谈」，这在 Titanic 型站上不成立。卡由 `tools/gen_traveller_cards.py` 生成，**改卡＝改生成器重跑**（rule 4i ①），不得手改。进阶段 2 建 c5 的 sk3 装束变体时一并处理。
2. `dossier §0b` 六条待人工抽查，其中 `timeline.003`（Farriner 打烊、女儿午夜巡查）是整集的锚点却 tier 最低。
3. 片名与片长档待用户确认。

## 2026-09-18 · 阶段 2 进行中 005 — 骨干三件 + 一条判据收紧
Source: 阶段 2 生成 casting.md 时对 w5 §10.4 的分类做可执行化
Summary: 落 `world.md` / `style_guide.md` / `casting.md`。过程中把「真实历史人物只念有记载的原话」收紧为**「必须有史料把他『说出』这句话记下来，而不是他自己写下来」**——四档判定表落 casting.md §0。**后果：皮普斯在片中全程不开口**（日记是写的不是说的），他的话走字卡与妮娅画外引述；全片唯一可对口型的真实人物是 Bludworth 一句。

Auto-updated:
- `ai_videos/shikong_lvxing/sk3/2_世界观人设/{world.md, style_guide.md, casting.md}` — 新建
- `specs/ai_video/sk3/divergence.md` — D6 边界①按新判据重写
- `tools/gen_traveller_cards.py` — 名册卡改为**认站型**（三处）：当地人开不开口按游览型 / Titanic 型分叉，不再写成全系列通则；六张卡已重跑

待办：`relationships.md` · 角色卡 c21–c30 · 场景卡 bg0–bg12 · props p1–p13 · 阶段 2b 整城 blend。按 rule 4i ① 走生成器而非手写。

## 2026-09-18 · 阶段 2 进行中 006 — 场景轨 14 张卡 + 生成器
Source: 阶段 2 执行
Summary: 新建 `tools/gen_sk3_assets.py`——**整张卡归生成器**（sk1 是手写卡 + 生成器只盖 look 层；sk3 是新站，按 rule 4i ① 做成一个出处）。14 张场景卡一次生成、`--check` 通过。

Auto-updated:
- `tools/gen_sk3_assets.py` — 新建。内置四道闸门：零 hex（rule 1b）· 裸 `=>@` 占位不得代填槽位号 · 锁定串必带「不是 X」（rule 12.8）· **共用串光源污染交给 `prompt_light.check_drama()` 判**（K32，全仓唯一实现；`legacy` 为空，新站不给豁免）
- `ai_videos/shikong_lvxing/sk3/2_世界观人设/scenes/london/bg0–bg13/` — 14 张主体卡
- `ai_videos/shikong_lvxing/sk3/2_世界观人设/world.md` — §4 补 bg13 行、bg2 改标「白天 · 炉门未亮」

过程中修掉三处自造的错：
1. 我先在生成器里手搓了「`STYLE_BASE` 里不许出现『光』」的检查，**当场被自己的「柔和高光滚降」判死**——高光滚降是感光响应不是光源。改接 `tools/prompt_light.py`（该判据的全仓唯一实现），不另造。
2. `=>@` 的正则写成 `=>@\S`，把结尾反引号当成槽位号。改成只在紧跟数字/字母/汉字时才报。
3. bg2 原本把白天与傍晚两套光塞进同一张卡的反向声明里——**正是 16.9 要防的**。按 rule 4d ③ 拆成 `bg2`（白天）与 `bg13`（傍晚，炉门亮着）两个主体；同时把 bg2 那条标成 ✅ 进上传槽的 ref 改回 ⚠️，它与该主体「不走 img2img」的工艺说明本来是矛盾的。

待办：props p1–p13 · 角色卡 c21–c30 · `relationships.md` · 阶段 2b 整城 blend。

## 2026-09-19 · 阶段 2–5 推进 007 — 骨架全通，出图与几何落地
Source: 自主连续执行（用户 2026-09-18 授权「全程自己决策、不要问」）
Summary: 阶段 3 大纲、阶段 4 剧本与台词、阶段 5/6 生成器与闸门、14 张场景图、伦敦整城 blend 全部落地。

Auto-updated / 新建：
- `3_大纲/outline.md` — 46 镜骨架 + 全片曲线（前 2/3 ≥2 笑点/分钟，**后 1/3 清零**）+ 四位 NPC 盼头落点
- `4_剧本/script.md` — 全片台词（英文成片 + 中文译配双轨），逐镜
- `4_剧本/dialogue.md` — 发声总表 + 语速核算。**核算结果推翻了 46 镜的排法**：三处口播超长（55/58/40 s）必须拆镜 → **46 → 49 镜**
- `tools/gen_shots_sk3.py` — 分镜引擎 + 六道闸门（5000 字硬顶 / 景别跳档 K31 / 光源污染 K32 / 语速 / **非旅行者台词必须带 fact_id 或「虚构人物·现代英语」** / 裸 `=>@`）
- `tools/sk3_data/props.toml` + 13 张物件卡（worker `assets-props`）
- `tools/build_london.py` + `london.blend`（4383 网格）+ `tools/check_london.py`（6 张校验渲图）
- 14 张场景锚点图（ElevenLabs Flows / gpt-image-2，16:9 2K）

**修掉的自造错（都是校验渲图或包围盒查出来的，不是猜的）**：
1. `tools/image_fetch.py` 路径写死在 sk1 → 加 `--drama`，默认值不变、旧命令行为不变。
2. 地形一整块盖住了泰晤士河 → 两岸分建。
3. `jetty_house` 面宽固定沿 x，却拿它建了**南北走向**的布丁巷 → 整排房子转了 90°。加 `axis` 参数。
4. 泰晤士街整排房子盖在布丁巷口上，巷子被堵死 → `street_row` 加 `gaps`，横穿的街留缺口。
5. 校验相机 z=1.7 埋在街面（街面在 z=3.0）以下 → 视平线改 面+1.6 m。
   **教训**：第 3–5 条我靠看渲图猜了两轮才定位，最后是**直接打印包围盒**一次查出来的。几何问题查几何，别看图猜。

**p13 三件不变物的指针没建**：按 rule 4b-B 本应放 `.link.json` 指向 sk1 的那份，但 **sk1 的 `props/p3_三件不变物/` 目录里只有 md、没有任何图**——指向不存在的目标是悬空链接。等 sk1 出了图再建，或本站自己出一次。

几何的已知欠账：坐标是按 dossier 给死的几个距离**推算**的；驱动 hero 镜之前应以 **Ogilby & Morgan 1676 实测图（100 ft/inch）**套合替换。

## 2026-09-19 · 阶段 5/6 完成 008 — 49 镜卡 + 出图 + 出模 + 发布页
Source: 四路并行分镜作者（shots-01-14 / 15-25 / 26-38 / 39-49）+ parent 整合
Summary: 49 镜全部生成、六道闸门零 blocker；27 张物件图、14 张场景图全部落地；4 个 Hyper3D 网格出了原始 GLB；`publish.md` 四站发布页落地。

Auto-updated / 新建：
- `tools/sk3_data/{characters,props,shots_01_14,shots_15_25,shots_26_38,shots_39_49}.toml`
- `5_6_分镜与prompt/{shotlist.md, all_shot_prompts.md, publish.md}` + `shots/shot01..49/shot NN.md`
- `2_世界观人设/{characters/c21..c30, relationships.md, props/p1..p13}`
- `props/p{2,4,8,9}/object.toml` + `raw_p{2,4,8,9}.glb`（Rodin，41–60 s/件）
- `tools/{gen_shots_sk3.py, gen_previz_sk3.py, build_london.py, check_london.py}`
- `tools/image_fetch.py` 加 `--drama`（原先写死 sk1）

**我自己的两个生成器 bug，都是工人查出来的**：
1. `refs_line()` 把旅行者 entity 写死成「1666 装态」，不随 `modern_dress` 切 → shot03–12 的 `参考:` 与 `角色:` 两行自相矛盾。已按 `modern_dress` 二选一。
2. `view` 字段作者各写各的（短 stem vs prompt 首行全名），而盘上只有 `bg2-1.png`。已在生成器里加 `view_key()` 归一——**这种事不该靠约定，靠归一**。

新登记偏离 **D8**（shot38/47 超镜长带）· **D9**（两处台词在语速闸门下无法逐字，砍形容词不砍事实）· **D10**（片长 21 分钟超档，**未擅自砍，给了可执行的压缩顺序，留用户拍板**）。

## 2026-09-19 · 阶段 6 审查 009 — 两路审查落地 + 三处事实/生成器纠错
Source: `spawns/review-story`（剧情连贯·全剧序列）与 `spawns/review-camera`（运镜·站位·动作）
Summary: 两位审查员各通读 49 镜一遍，共改 27 个镜（story 7 / camera 20），全部改在 TOML、重跑生成器，`--check` 与 `shot_logic` / `prompt_light` 全绿。

**审查找到的、机械闸门抓不到的头号问题——情绪转折点提前了 5.4 分钟**：
`outline.md` §0 把转折点定义了两次（按时码 10:40 / 按 beat shot38）。46 镜 15 分钟时两者重合，**49 镜 21 分钟后 shot38 落在 15:54、10:40 落在 shot26**，26–38 的作者跟了时码。实测前 2/3 笑点密度 1.32/分钟（合同 ≥2.0），其中 shot26–38 只有 0.37。**后果是全片最好的三秒静默落在已经安静的地上。** 已补进 D10 与 publish.md §7——**这把「超档 5 分钟」从格式问题升级成结构缺陷，压到 16 分钟能同时解决两件事**。

**三处纠错**：
1. **事实错误（已扩散到成片台词与四站文案）**：「起火时刻两说差十一小时」算不出来——伊夫林「This fatal night, about ten」记在 9/2 条下，对官方凌晨一点，读作当晚 10 点差 21 小时、前一夜 10 点差 3 小时、上午 10 点差 9 小时。**已全仓改为不报数字、只说两份记载对不上**（不替史料裁决）；dossier §0b 第 3 条留了更正说明。
2. **生成器缺陷（第三次同一类）**：`emit()` 无条件写妮娅的锁定串、`refs_line()` 无条件挂她的 entity 图，**她不该入画的镜只能靠作者手写禁令挡住，而四位作者里只有一位写了**。新增 `onscreen` 字段：false 时改写强否定、撤掉 entity 图（声样保留）、并换一套 `参考用法:`（原样板说「她的脸由 entity 承载」，对不入画的镜自相矛盾）。已据作者写下的标记自动标出 **13 个镜**。
3. Farriner（c29）在 shot16/17 缺 `chars` 锚点 → 会被渲成另一个人，整条任务线的回扣就没了（story 审查发现）。

**教训（三次同一类，写下来）**：`view` 键归一、装束态、入不入画——**凡是「四个作者各自要记得」的东西，最后一定有人不记得。能进生成器的判断就别留在约定里。**

待用户定夺的清单见两份审查报告与 `publish.md` §7。

## 2026-09-19 · previz 性能实测与结论 010
Source: 本轮自主执行中对 previz 渲染的反复排查
Summary: previz 管线**是通的**，瓶颈在渲染速度；沿途修掉三个我自己造的问题，并留下可复现的量化结论。

**48 字节 mp4 的根因（订正）**：FFmpeg 开始时写容器头、**结束时才封口**，所以中途被杀的渲染留下的就是 48 字节。**但杀它的不主要是我手动 kill，而是外层 shell 的生命周期**——渲染进程挂在会话的后台 shell 下，shell 被回收时 blender 跟着死，而父进程退出码仍是 0、日志停在最后一帧、连 `Blender quit` 都没有，看上去像「跑完了但没输出」。

决定性实验：把同一配置改成 **2 秒（16 帧）**跑完整流程 → 得到 **15,656 字节**的真 mp4 + 「渲毕」+「Blender quit」。**管线完全正常，纯粹是没跑完。**

**解法**：① 用 PowerShell `Start-Process -NoNewWindow -PassThru` **真正脱离 shell** 启动批量；② fps 降到 6（animatic 标准，运动/遮挡/尺度/时刻表全读得出来），22 s 的镜从 176 帧降到 132 帧。

**教训：判断一个长时间渲染成没成，要看进程有没有自然退出（日志末尾的 `Blender quit`），不能看文件大小、也不能只看退出码。**

**性能实测（同一场景、同一镜）**：
| 配置 | 单帧 |
|---|---|
| 24fps 1920×1080，4383 个独立网格 | **23 s** |
| 12fps 960×540，网格按 collection 合并成 10 个对象 | **5.4 s** |
| 640×360，三盏 sun **开**阴影 | 6.4 s |
| 640×360，三盏 sun **关**阴影 | **1.0 s** |

两个杠杆：**① 对象数**（EEVEE 的逐对象开销，4383 → 10 个对象是 4× 以上）**② 阴影**（三盏 sun 在 1500 m 场景范围上算阴影，6.4×）。分辨率反而不是主因——航拍镜越飞越开阔，后段每帧看到的几何更多，640×360 的后段比 960×540 的前段还慢。

**已落地的三处修正**（都在 `tools/build_london.py`）：
1. `join_per_collection()` —— 合并网格。**这不是洁癖，是 previz 能不能跑完的分水岭。**
2. 场景级 `use_shadows = False` —— 本 blend 只服务 previz，白模体积靠 AO + 三灯主/补/轮廓比读得出来，不靠投影。`build_previz` 会换掉本文件的灯，所以只能在场景级关。
3. `me.validate()` —— 建完就地校验拓扑。不做的话每次打开 blend 现修一遍，一次渲染日志里刷出**十万行** `edge appears twice, correcting`。

**现状**：38 份 previz 配置与 shot previz blend 齐备（配置才是 rule 4h ② 所说的「3D 层唯一真相」）；mp4 需要一次长时间无人值守的批量。命令：`python tools/gen_previz_sk3.py --render`。

## 2026-09-19 · previz 批量的两个自造 bug 011
Source: 批量日志逐镜结果
Summary: previz 渲染本身没问题，两个 bug 都在我写的批量脚本里。

1. **成功被误报成失败**：`subprocess.run(..., text=True)` 在 Windows 上默认用 **cp1252** 解码 blender 的输出，遇到 0x90 字节时读取线程抛 `UnicodeDecodeError`，`returncode` 于是变成 1。**shot02 明明渲出了完整 mp4，日志里却是 ✗。** 已显式传 `encoding="utf-8", errors="replace"`。
2. **报错内容被噪声淹没**：出错时只打印 stderr 末 300 字符，而那 300 字符永远是 `Warning: edge ... appears twice`（一次渲染刷十万行），真正的错误永远看不到。已改成先滤掉网格警告再报最后 6 行。

**这两个加在一起的后果很恶劣**：一个成功的渲染被报成失败、而失败原因显示为无关的网格警告——**排查时会一路往 blender 和几何上找，而 bug 在调用方**。教训：**批量脚本的错误上报本身要先被验证**，否则它会把你引向错误的方向。

另：`shot01/02` 是唯一带 `运镜 = 升降` 与承接对的两镜，也是最慢的（航拍看到全城几何）。断点续跑会在下一轮自动重试未完成的镜（判据是 mp4 > 10 KB）。

## 2026-09-19 · previz 抽帧复核 012 —— 走廊型机位按 bg 钉死
Source: 从 shot06 / shot09 的 previz mp4 抽帧目视
Summary: 抽帧发现两镜拍到的是隔河对岸的一排房子而不是沿桥纵深。**先排除了误判**——查镜表确认 shot06 `jb[0]=0.12`、shot09 `jb[0]=0.10` 都是远景，妮娅本来就该只占一小点，previz 的**取景比例是忠实的**。真正的问题在方位角：我按机位标签关键词猜的 30°，把相机摆到了桥侧面的河上。

**关键词猜方位角对开阔地够用，对走廊不够**——桥上房屋隧道与布丁巷只有沿轴的机位成立，侧向要么被墙挡死、要么把相机放到墙外。已加 `CORRIDOR_BG`，桥与布丁巷的方位角按 bg 直接钉死在 170°（她背后、沿轴，偏 10° 免得与她共线看不见人）。

同时在每份生成的配置抬头写明**「本文件是骨架」**——`占画高` 与时长由镜表算准，但方位角、道具坐标、关键帧时刻仍需按镜手调（这与仓库既有 previz 配置的约定一致，见 `duikang_shangzeng/shot01/previz_config.toml` 的同款抬头）。

**待办**：当前批量跑在旧配置上；跑完后重生成配置并删掉走廊镜（bg1 的 06–09、bg2 的 15–17、bg13 的 36–38）的 mp4，让断点续跑重渲它们。

## 2026-09-19 · previz 位移模型三次迭代 013 —— 已验证并投整批
Source: 逐镜抽帧目视复核
Summary: previz 的相机与位移经三轮修正后验证通过，38 镜整批已投（脱离 shell，pid 记在 `previz_batch.log`）。

**三次迭代，错因各不相同，但现象很像——这是它值得记的原因**：

| 现象 | 第一反应 | 真因 |
|---|---|---|
| mp4 只有 48 字节 | 渲染失败 | **外层 shell 回收进程**，FFmpeg 没封口。2 秒的对照实验出了 15,656 字节的真文件 |
| 主体只占几个像素 | 相机放错 | **没错**——查镜表，shot06 `jb[0]=0.12`、shot09 `=0.10` 本来就是远景 |
| 主体中途消失 | 位移算错 | 位移该由**景别**决定，而我按 bg 给了固定端点 |

**第二行是最险的**：不去翻镜表的 `jb` 值，就会把一个正确的远景当 bug「修」掉。**先查数据源怎么说，再判断产物对不对。**

**最终的位移模型**（`mobility`）：
- `占画高 ≥ 0.70`（近景/特写）→ ×0.05，基本原地。shot19「面包摊三档」是她站着说话的 0.75 近景，第二版却让她走 26.6 m，静止机位当然跟丢
- `0.40–0.70`（中景）→ ×0.30
- `< 0.40`（全景/远景）→ ×1.0，真在穿行
- 航拍与河上镜另给 8× 步速（那是飞行与漂流，不是走路）

**交叉印证**：shot15 一镜到底按此模型走 **35.9 m**，与 w2 调研独立算出的「27 秒跟拍按 80 m/min 只能走约 35 m」吻合——两个来源对上了，比拍脑袋给端点可靠。

**验证证据**：shot19 重渲后第 60 帧（中段）妮娅居中、占画面约 75%，与 `占画高 0.75` 一致，全程在画内。该 mp4 作为参照保留、未随整批清空。

另修：走廊型 bg（桥 / 布丁巷）方位角按 bg 钉死 170°，不再用关键词猜——关键词对开阔地够用，对走廊会把相机摆到墙外（实测摆到了桥侧面的河上）。
