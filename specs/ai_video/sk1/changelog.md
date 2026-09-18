# sk1 · 变更日志

## 阶段 0 启动 — 2026-09-13 19:47
- 六路研究员并行抓原文与参考图；dossier 骨架、README 建立；`verified_by` 增 `ai_read` 三态（playbook / rule 17 / K34 同步）。

## 阶段 0 完成 — 2026-09-13 21:50
- `sk1/0_research/dossier.md` 合并六路（285 条事实：266 ai_read / 19 ai_draft；T0 174）；15 节齐；§0 含冲突裁定 6 条 + 抽查清单 10 条 + 参考图库统计（17 个资产 196 张）。
- `sk1/0_research/qc_stage0.md`：blocker 0 / warning 1（10 条 ✅ 事实 negative 为空，由本站黑名单兜底）。
- 事实注册表 `parts/w1–w6`；重复编号已改（W2 house.001/002 → 013/014；W5 person.001–004 → 007–010）。
- 概念卡校正（proposal.md C §sk1）：路线 虹桥 → 东水门 → 州桥；「十五文」是包子价；州桥是夜市；「桥丁」改军巡铺兵；补迎祥池由头。
- 待用户：抽查 10 条 → 改 human；决定第三受访者（军巡铺兵 vs 酒博士）；是否现在进阶段 1。

## 阶段 1 立项 — 2026-09-13 22:05
- `sk1/1_立项/concept.md`：三件套（主角诉求 / 障碍＝货币·时辰·称谓 / 本站内两条悬念，无跨站伏笔）、正向立意、本站四格、一日时间线（六站 + 可选反向 tag）、密度合同、语言四站、生产提示；每个可截图设定带 `fact_id`。
- `specs/ai_video/sk1/divergence.md`：13 项与全局默认的偏离（16:9 / 10 分钟 / short 扁平 / 20 s 镜 / 双 voice_id / entity 人脸 / 阶段 0 / 参考图进 prompt / 单体建筑 image-to-3D / previz 视频参考 / 画外为主 / 跳过武打特效 QC / 结尾不固定）。
- 用户拍板：先信任 ai_read 直接进阶段 1；第三受访者＝军巡铺兵沈十九。阶段 1 QC＝人工确认，待用户点头后进阶段 2。

## 阶段 2 启动 — 2026-09-13 22:20
- 用户确认阶段 1。五路并行：S2_A 人物（系列基础卡 c1_林问 + sk1 宋装卡 + c2 李十六 / c3 周四娘 / c4 沈十九 + relationships + casting）、S2_B 场景 bg1–bg4（bg1 虹桥＝世界锚点）、S2_C 场景 bg5–bg8 + world + style_guide、S2_D 器物 p1–p7、S2_E 建筑单体 p8–p10 + `_blender/city_plan.md` + `blender_build.md`。
- 共用简报 `.audit/.../stage2_brief.md`（命名 / 模板 / 负向基线 / 参考图挂法）。目录变更：`scenes/bg*` → `scenes/bianjing/`；`c2/c3/c4` 改名为受访者姓名。

## 阶段 3 段落结构 + 阶段 4 剧本 — 2026-09-14 00:55（自主模式，follow-up 006）
- `sk1/3_大纲/outline.md`：四段六站 → 27 镜 ≈ 598 s；每镜 bg / 时长 / beat / 人物 / fact / 景别意图；密度与规则对账；阶段 3 QC 自查（剧情连贯；全剧序列 N/A）。判断：任务结局定「完成」；S26「带你去看一眼」可选实验；S27 考证卡空镜。
- `sk1/4_剧本/script.md` + `dialogue.md`：27 镜画面动作 + 台词三类（记者 ≥ 60% OS）；每句知识点带 fact_id；⚠️ 事实带口播；❌ 只在 S13；白话自检。
- 待办：生成器建表时按「字数 ÷ 时长 ≤ 5」调整 S02 / S05 / S06 / S07 / S08 / S10 / S13 / S24 时长并回写两份剧本；一次性发声角色（大伯 / 摊主 / 小孩 / 闲汉 / 民调三人 / 路人 / 群众）按 K30 建轻量卡。

## Follow-up 001（sk1）+ 系列 007–010 落地（进行中）— 2026-09-14 08:54:27
Source: specs/ai_video/sk1/user_input/follow_ups/202609.md - section 001；specs/ai_video/shikong_lvxing/user_input/follow_ups/202609.md - sections 007–010
Summary: 自主跑完剩余工作；片名改为「汴京清明一日」；节目形态改为外来游客全开放带逛、当地人不开口；开场航拍长镜扫全城；整城 Blender 建模 + 每镜白模动画作 Seedance 参考。

Auto-updated:
- ai_videos/shikong_lvxing/sk1/README.md — 首行改「时空旅行 · 汴京清明一日（sk1）」（剧目管理界面取「汴京清明一日」，已按 tree__reader 的解析规则实测）；形态与阶段状态重写
- ai_videos/shikong_lvxing/sk1/1_立项/concept.md — **整篇重写**为游览形态（逛单 / 形态铁律 / 一日时间线含「序·航拍长镜」）；判断：「反派动机」在游览形态下不适用，由货币 / 时辰 / 脚程承担张力
- ai_videos/shikong_lvxing/sk1/3_大纲/outline.md — **整篇重写**：36 镜 ≈ 842 s（含可选 S35），S01→S02 航拍无缝承接，其余硬切；新地点 fact 标 W7–W11 待回填
- specs/ai_video/sk1/divergence.md — #2 / #4 / #5 / #11 / #13 改写，新增 #14（游览形态）
- tools/shot_logic.py — L1 建造动词检测排除名词里的字（军巡铺 / 纸马铺 / 封面 / 脚手架 / 开封 …，`NOT_BUILD`）；hy1–hy4 扫描结果与改前逐字一致
- tools/facts_registry.py — **新建**：直接读 `0_research/parts/*.md` 的事实注册表（统计 + 重复 id / 非法 tag / ai_read 缺 quote 机检），生成器不再依赖 `.audit` 里的 facts.json 快照
- ai_videos/shikong_lvxing/sk1/0_research/parts/w3_clothing.md、w5_language_people.md — dress.032 / person.008 两条复合 tag 规范为单一 tag，原写法记在 `tag_note`
- ai_videos/shikong_lvxing/_series/glossary.md — 顶部注明当地人不开口，称谓白名单只用于旅行者解说
- .claude/skills/ai_videos__全流程编排/playbooks/ai_videos__stage0_史料调研.md、.claude/agent_refs/project/ai_video.md rule 17.1 / 17.5 — 「可采访人物」「受访者配音」按项目形态二分（采访型 / 旁白型）

In progress（后台 worker，完成后续记）：阶段 2 收尾 + QC（S2_finish）/ 汴京城 builder（B_city）/ 新地点补充调研 W7–W11 / 系列提案重写（P_series）/ 生成器与剧本重写（G_sk1）/ 四站发布页（PUB_sk1）

No conflicts found in: huangye_shenghuo/*（shot_logic 改动已对 hy1–hy4 回归）

## 2026-09-14 进度记录（worker 回稿）— 2026-09-14 09:15:37
Source: 系列 follow-up 007–010；sk1 follow-up 001（续上一条「进行中」）

Auto-updated:
- ai_videos/shikong_lvxing/sk1/2_世界观人设/{relationships.md, casting.md, qc_stage2.md} — **新建**（S2_finish）：人物网按 hy4 体例写「她与这座城 / 与试过的东西 / 与静默的人」；casting 只登记林问一对 voice_id + 39 个参考图文件清单；阶段 2 QC blocker 0 / warning 9
- ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/bg9_今日州桥遗址/ — **新建**卡 + 9 张开放许可照片；一句话锁定按照片更正为「钢棚下发掘坑、北宋浮雕石壁、明代砖拱桥」（无玻璃罩 / 脚手架 / 游客）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/characters/c2–c4 — 改为静默脸（无 voice_id、说话风格模板改为肢体神态锚）；c2 「皂巾包头」→「皂巾裹髻」（「包头」为城市名，K17 审核词）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/{props/p1–p10, scenes/bianjing/bg1–bg8, world.md, style_guide.md} — 7 个锚点补足 1500 字、9 块负向词改裸围栏（rule 4b-A）、37 处采访 / 被拦措辞改写、负向基线「看镜头（林问对镜说话除外）」
- ai_videos/shikong_lvxing/sk1/1_立项/concept.md、3_大纲/outline.md — 「御沟荷花」→「荷叶初生」（清明不开花，bg4 卡为准）；S35 遗址措辞按照片更正；总时长更正为 862 s（含可选 S35）/ 842 s
- ai_videos/shikong_lvxing/sk1/5_6_分镜与prompt/publish.md — **新建**四站发布页（PUB_sk1）：中「时空旅行·第1站｜汴京清明一日」/ 英 *One Day in Kaifeng, 1120*；封面＝S04 桥中回望；片尾评论问题「给你一贯铜钱，在 1120 年的汴京待一天，你第一文钱花在哪？」；YouTube 手动上传中文音轨
- tools/build_bianjing.py + scenes/bianjing/_blender/{bianjing.blend, plan*.png, check_*.png}（B_city）— **新建**确定性建城器：全城体块层（待 W11 布局数据）+ Place A/B/C 细节层；方块号 → 资产 pN，白模到位自动替换；96 物件、两次构建几何哈希一致；§6 验收 11/12 通过（#10 待锚点图）
- tools/render_scene_plan.py — 相机远裁剪面随场景尺度设置（1072 m 宽的汴京平面图原先渲成空白；duikang / xianjian 小尺度场景输出不变）

Pending：W7–W11 补充调研合并与 fact 回填；新地点场景卡 bg0 / bg10–bg13；生成器与剧本重写（G_sk1）；Blender 第二阶段（全城体块 + 航拍路径 + 每镜白模动画）；系列提案重写（P_series）；全维度审查；提交

## 2026-09-14 进度记录（续）— 2026-09-14 09:35:32
Auto-updated:
- ai_videos/shikong_lvxing/sk1/0_research/parts/{w7_medic, w8_gov_palace, w10_inn_daily}.md — **新建**补充调研：医馆 34 条、开封府 24 + 宫城 27 条、客店过夜 42 + 一天作息 20 条（合计 147 条，ai_draft 5 条不进 prompt）；bg10 / bg11 / bg12 参考图库、bg7 追加 10 张室内参考图
- ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/bg7_坊巷民居/bg7_坊巷民居.md — 视图 2（客房）按 W10 修正：木枕 → 白地黑花瓷枕（`inn.026/027`）、床铺新荐席（`inn.010`）、包袱绑床腿（`inn.015`）、不画窗纸（`inn.035` 为 ai_draft）、「客店一晚 ≈ 五十文」口播删除；夜 / 五更态另开主体 `bg14_客店房间夜`（rule 4e ③）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/{characters/c1_林问/c1_林问.md, props/p3_三件不变物/p3_三件不变物.md, qc_stage2.md} — 系列卡已回改，三处「待回改 / 未改」注记更新为已解决

Pending：W9 / W11 补充调研；场景卡 bg10 / bg11 / bg12 / bg14（进行中）与 bg0 / bg13（待调研）；dossier.md 合并 + 阶段 0 补充 QC；生成器与剧本（G_sk1）；Blender 第二阶段；全维度审查；提交

## 2026-09-14 进度记录（续 2）— 2026-09-14 09:57:48
Auto-updated:
- ai_videos/shikong_lvxing/sk1/0_research/parts/w9_fun_literati.md — **新建**（W9，partial）：娱乐 26 条 + 文人 25 条，全部 ai_read；bg6 参考图 11 → 21 张，bg13 新建 13 张（缺宋代寺院建筑图）
- ai_videos/shikong_lvxing/sk1/0_research/dossier.md — §0 新增 ⑤ 补充调研汇总（W7 / W8 / W9 / W10 共 198 条）；§2 / §5 / §8 / §9 / §12 / §13 / §14 / §15 加指针；§5 删去「客店一晚 ≈ 50 文」（ai_draft）；§12 改「可观察的人物（静默）」
- ai_videos/shikong_lvxing/sk1/0_research/qc_stage0.md — 追加补充调研 QC：blocker 0 / warning 2（新地点内景无图、bg11 / bg13 正面参考图偏少）
- ai_videos/shikong_lvxing/_series/blacklist.md — K46–K55（W9 娱乐 / 文人）
- 判断：S22 相国寺开市日有分歧（`literati.005`）→ 以东门书铺为锚、口播存疑；S23 文人不设在茶坊（京城只熟食店挂画 `literati.015`）→ 改为园林雅集远观（《文会图》`literati.018`）；李清照 / 赵明诚 / 米芾 1120 年不在京或已故，不出镜
- ref_fetch 大都会馆 API 403 复现不了（同一 UA 现返回 200）→ 判断为临时限流，工具不改

Pending：W11 全城布局；场景卡 bg10 / bg11 / bg12 / bg14 / bg13 / bg0；生成器与剧本（G_sk1）；Blender 第二阶段；全维度审查；提交

## 2026-09-14 进度记录（续 3）— 2026-09-14 10:03:02
Auto-updated:
- ai_videos/shikong_lvxing/sk1/0_research/parts/w11_city_layout.md — **新建**（W11）：全城布局 50 条（✅ 38 / ⚠️ 11 / ❌ 1，ai_draft 4 条只作 C 级几何）；三重城墙实测尺寸与朝向；§2.8 TOML（3 墙 / 37 门 / 5 河 / 15 街 / 28 地标 + 片区真实锚点 + 航拍 6 航点）；bg0_汴京全城 参考图 13 张
- ai_videos/shikong_lvxing/sk1/0_research/{dossier.md, qc_stage0.md} — 补充调研五路齐（合计 248 条），dossier §2 加全城尺寸与不确定项；阶段 0 补充 QC 追加 W11 行
- ai_videos/shikong_lvxing/_series/blacklist.md — K56「明清城墙＝北宋城墙」（W11）
- 判断：Place A / B / C 由压缩占位偏移改为 W11 真实锚点（航拍长镜需要全城几何连贯）；S01 / S02 航拍按 W11 航点切分（S01＝WP1→WP2、S02＝WP3→WP6，两镜首尾承接），S36 从客店附近屋顶拉远

In progress：Blender 第二阶段 a（全城体块层 + 片区真实锚点 + S01 / S02 / S36 航拍白模动画，B_city）；场景卡 bg0（S2_bg0）/ bg13（S2_bg13）/ bg10 / bg11 / bg12 / bg14（S2_bg11_12）；生成器与剧本（G_sk1）

## 2026-09-14 进度记录（续 4）— 2026-09-14 10:10:14
Auto-updated:
- ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/{bg10_赵太丞家, bg11_开封府, bg12_宣德楼, bg14_客店房间夜}/ — **新建场景卡**（S2_bg11_12），各含锚点 + 第二视图，锚点 1541–1672 中文字；一句话锁定为生成器 BG 权威：bg12「宣德楼五门朱漆金钉，单檐庑殿绿琉璃瓦，朵楼阙亭围成凹字」/ bg11「灰瓦素木府门敞开，望进内门庭院与正厅，不是包公戏里的衙门」/ bg10「赵太丞家浅色木匾，两块立招高过屋檐，门屋斗拱，不是清式药房」/ bg14「客店客房夜里：素木床榻瓷枕、陶油灯、直棂窗，不点蜡烛」
- ai_videos/shikong_lvxing/sk1/2_世界观人设/{style_guide.md, world.md} — 宣德楼例外：绿琉璃瓦与朱漆金钉门为史料确证（`palace.002/004`），只在 S18–S19 放行，负向改「金黄琉璃瓦 / 北京故宫红墙黄瓦 / 重檐」；world.md §4 场景主体清单扩到 bg0–bg14
- ai_videos/shikong_lvxing/sk1/3_大纲/outline.md — S15 医馆内景按 `medic.005` 改为「妇人抱孩、老者俯身、柜台」（删诊脉 / 碾药 / 药柜抽屉）；S34「窗纸发白」→「窗棂间发白」（不画窗纸）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/bg7_坊巷民居/bg7_坊巷民居.md — bg7-2 正文补「新草荐」；瓷枕参考拆为形状 ref14 / 纹样 ref21
- ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/bg11_开封府/refs.md — ref04 条目更正为「殿堂…侧样」
- sk1 各卡 H1 中残留的「《时空旅行》第 1 站」统一改为「时空旅行 · 汴京清明一日」（片名不再用系列名，sk1 follow-up 001）

In progress：场景卡 bg0（S2_bg0）/ bg13（S2_bg13）；生成器与剧本（G_sk1）；Blender 第二阶段 a（B_city）

## 2026-09-14 阶段 4–6 生成 + 全维度审查启动 — 2026-09-14 10:20:10
Auto-updated:
- tools/gen_shots_sk1.py — **按游览形态重写**（G_sk1）：36 镜 / 862 s；只有林问发声（闸门拒绝非林问台词、正常台词镜必须林问入画）；事实直读 `0_research/parts/*.md`（`facts_registry`）；S01→S02 航拍承接（`handoff_from` 豁免切口、S01 `尾帧锁定:`）；每镜 `参考:` 挂 `shotNN_previz.mp4` 白模动画；构建时逐项核对锁定串与卡（人物识别标签 / 道具锁定 / 场景一句话 / 渲染样式串 / 负向块）
- ai_videos/shikong_lvxing/sk1/4_剧本/script.md — **整篇重写**；`dialogue.md`、`5_6_分镜与prompt/{shotlist.md, shots/shot01–36, all_shot_prompts.md}` 由生成器生成
- 关键判断（详见生成器与 `.audit/.../spawns/G_sk1/output.md`）：S21 以开封府放行的清明关扑街摊代替无据的衙门内景；S23 园林雅集设在相国寺侧院池边（为调度安排，非史料）；S03 米价口播「这几年一斗两百五十文上下」；S09 为唯一 ❌ 出场位；S13 租「鞍马」口播为「租头驴，是我猜的」；S26 铺兵只挥臂不开口
- ai_videos/shikong_lvxing/sk1/2_世界观人设/props/p1_旋煎羊白肠与食摊/p1_旋煎羊白肠与食摊.md + 生成器 P1 — 案角牛油烛 → 小陶油灯（style_guide：非正店夜镜只有油灯）
- ai_videos/shikong_lvxing/sk1/2_世界观人设/props/p3_三件不变物/p3_三件不变物.md + 生成器 P3_BADGE — 胸牌「五个墨色手写小字」补「画面上只见淡墨笔画、不要求可读」，与 C1 描述符一致
- ai_videos/shikong_lvxing/sk1/2_世界观人设/scenes/bianjing/bg7_坊巷民居/bg7_坊巷民居.md — bg7-2 删去「包袱绑床腿」（S07–S08 还没绑；绑是 S33 起 bg14 的状态）
- 严格构建 + prompt_light + shot_logic + facts_registry 全过（无 blocker）

Validation started：审查总编排 7 路并行（台词白话 / 站位动作 / 运镜时长 / 光线奇观 / 整集连贯 / 史实核查 / 格式契约），只出 findings，由修改 worker 统一落到生成器
Pending：场景卡 bg0 / bg13 / bg16 州桥夜市；Blender 第二阶段 a（航拍）与 b（其余 31 镜白模动画）；审查修改；提交

## 2026-09-14 进度记录（续 5）— 2026-09-14 10:27:27
Auto-updated:
- scenes/bianjing/bg13_相国寺/bg13_相国寺.md + **bg15_园林雅集/bg15_园林雅集.md** — 新建（S2_bg13）：bg13 锁定「相国寺东门书铺街、殿后资圣门书画摊，灰瓦素木北宋寺」；S23 文人雅集独立为 bg15 主体（锁定「园池边垂柳下黑漆大案藤墩文士雅集，茶床点茶兔毫建盏」，rule 4e：寺里书铺街与柳荫池塘不是同一个地方）；仍缺北宋寺院建筑实物参考图 ⚠️；bg13 追加大都会馆 3 张
- scenes/bianjing/bg0_汴京全城/bg0_汴京全城.md + **bg16_汴京全城五更/bg16_汴京全城五更.md** — 新建（S2_bg0）：bg0-1 斜俯瞰全城（WP3）、bg0-2 汴河低空迎虹桥（WP1）；五更天亮独立为 bg16 主体（rule 4e ③）
- 判断：场景编号撞号——S2_bg0 已占 bg16，州桥夜市改为 **bg17_州桥夜市**（S2_bg16 改名）；`_blender/city_plan.md` 俯视排版底图的路由键 `bg0-1` 与 bg0 主体撞键 → 改为 `plan0-1`（B_city 执行）
- 2_世界观人设/world.md — §2「平原上的一座方城」→ 三重城、城墙不正南北（`city.024`）；§2 路线改为游览顺序；§4 场景清单扩到 bg0–bg17
- 2_世界观人设/style_guide.md — 宣德门绿琉璃瓦例外扩到航拍镜（S01 / S02 / S36 远看宣德门）
- tools/ref_fetch.py — 大都会馆搜索遇到已撤下的藏品（404）跳过，不再整条中断

Pending for the review fixer（审查修改时一并落到生成器）：BG 锁定串 bg13 换卡上版本、新增 bg15 / bg16 / bg17 行；S23 → bg15（去掉寺廊 / 挂画 / 台阶）；S22「一个月开五回」改口播两说；S01 / S02 航拍高度按 W11 航点（WP1 8 m / WP2 150 m / WP3 3800 m），S01 `v`＝bg0-2、S02 `v`＝bg0-1；S36 → bg16；S30 → bg17；删除「bg0-1 被 city_plan 占用」的过期注记

## 2026-09-14 全维度审查回稿（6 / 7）+ 跨审查裁定 — 2026-09-14 10:46:16
Review results（findings 在 `.audit/adhoc_agents/2026-09-14/sk1-20260914-081253/spawns/R*/output.md`）：
- R1 台词白话：47（blocker 3 / warning 19 / nit 25）——对摊主说「给」「两个」、算卦笑话压过 S27；英文 TTS 台词缺失
- R2 站位动作：43（blocker 3 / high 6）——话筒与采访本手位全片锁死、S09 数钱、S33 绳结状态账本；柳枝与出镜台词脸不在画
- R3 运镜时长：40（blocker 3 / major 20）——S01 / S02 航速不可能、S01 交接源字段；S17→S18 同轴跳变、S33 / S34 纯黑段
- R4 光线奇观：37（blocker 1 / major 12）——S09 时辰倒流；参考用法「照搬」锚点光线；宣德楼例外漏删「红柱金匾」
- R5 整集连贯：27（blocker 2 / major 7）——时辰倒流、早饭数钱与总账不符；柳枝消失、开封府没进门、焌糟解释错位、未点名《清明上河图》、S35 / S36 顺序
- R7 格式契约：blocker 5 / warning 17——航拍镜缺 `角色:` 行、21 镜负向含「对口型」、bg13 锁定串过期、两个主体缺 refs.md；锁定串闸门只做子串匹配

Decisions（判断，交给审查修改 worker 统一落地）：
1. S09 改为辰时早市尾声（日出后）；二十文按街市七十五陌付约十五枚，口播标推算 ⚠️
2. 片尾顺序：客店过夜 → **S35 五更航拍收束（bg16）** → **S36 可选实验：今日州桥遗址（bg9）**
3. S21 走进开封府院子（bg11-2，类比口播只在 S20 说一次）→ 镜内切到府门外开封府放行的清明关扑街摊（`gov.013`）
4. 食摊灯形制定为敞口陶灯盏带灯芯（不是纸罩灯），p1 卡 / bg17 卡 / 生成器同步
5. 航拍按 R3 修正航点（S01 止于虹桥后约 600 m 悬停望东水门；S02 镜内一切、删 WP4、航速约 50 m/s，州桥不在飞越路线）
6. 生成器新增：时辰 `tod` 单调闸门、锁定串精确比对、手位 `hands` 与柳枝 / 包袱状态串、台词时间窗与视线、英文旁白台词与英文 TTS 块
7. 早市 / 客店 / 夜里的台词只对镜头说，删掉所有对当地人说的话

Auto-updated（审查期间父级已改）:
- specs/ai_video/sk1/divergence.md — #15 现代装态镜负向豁免、#16 现代物与时间态主体参考图豁免
- scenes/bianjing/{bg14, bg15, bg16, bg17}/refs.md、props/p9_桥尾脚店单元/refs.md — 指针式 refs.md（K34）
- .claude/skills/ai_videos__格式契约/SKILL.md K26 ④ — 交接源镜首次生成豁免（末帧尚不存在，`尾帧锁定:` 写明重生步骤即可）
- 2_世界观人设/casting.md — 场景参考图清单补齐 bg0 / bg10–bg17
- scenes/bianjing/bg4_州桥御街/bg4_州桥御街.md、world.md、style_guide.md — 夜市主体编号统一为 bg17
- tools/ref_fetch.py — 大都会馆搜索跳过已撤下藏品（404）

Pending：R6 史实核查；审查修改 worker；Blender 第二阶段 a 按新航点与 shot35 编号重渲

## 2026-09-14 史实核查回稿（7 / 7）+ 修改启动 — 2026-09-14 10:49:29
- R6 史实核查：知识句 123 条，96 条原样通过、27 条需改；blocker 12（东水门进出城说反、两句无 ai_read 依据的辟谣、遗址镜只靠 ai_draft、线装书、改制前官名、四处招牌要求生成文字）；另发现 `festival.001` 把卷七「一百五日为大寒食…寒食第三节即清明」读成「一百五日为清明」
- 判断：新增调研 W12_factfix 核实五条卡住的史实（今日州桥遗址现状 / 卷七寒食清明读法 / 小额省陌 / 北宋书籍装帧 / 1104 年后开封府官名），直接改 `0_research/parts`；审查修改 FIX_sk1 按七份审查 + 跨审查裁定统一落到生成器与剧本，冲突时优先级：史实 > 格式 > 连贯 > 台词 > 站位 > 运镜 > 光线（物理不可能除外）；另加英文旁白与英文 TTS 块
- 大纲 / 立项书 / 发布页等生成器定稿后由同步 worker 更新

## 2026-09-14 五条卡住的史实核实完毕 — 2026-09-14 11:12:14
Auto-updated（W12_factfix，改 `0_research/parts/{w1,w2,w4,w8,w9,w11}`；注册表 538 条、blocker 0）：
- `kaifeng.zhouqiao.002` 由 ai_draft 升为 ✅ ai_read（五个来源核对后改写 claim）；新增 `zhouqiao.004`（2018–2022 发掘、桥面距地表最浅约 4.3 m、2020-09-28 起公众考古基地开放至今，游客站坑边看）与 `zhouqiao.005`（保护棚 / 博物馆未证实，ai_draft）；`city.024`「仍埋地下」加注：说的是 2018 年发掘前与宋城整体
- `kaifeng.festival.001 / 009` 更正断句：卷七原文是「以冬至後一百五日爲大寒食」「寒食第三節，卽清明日矣」「但一百五日最盛」——人最多的是大寒食那天，不是清明当天
- 新增 `kaifeng.money.009`（⚠️）：二十文付约十五枚只是按七十五陌比例推算，零钱怎么数书上没写
- 新增 `kaifeng.literati.026`（✅）：1120 年书籍是蝴蝶装小册、卷轴、经折装，线装是明代才流行；`literati.001` 的 prompt_string 删去「线装书册」
- 新增 `kaifeng.gov.025`（✅，《宋史》卷 166）：1104 年后开封府设牧、尹、左右少尹、司录与士户仪兵刑工六曹，刑曹户曹最繁；`gov.006` 旧官名加注不适用 1120
- ai_videos/shikong_lvxing/sk1/0_research/dossier.md — §0 抽查清单第 7 条、§1、§9 的清明日期读法同步更正

Sent to FIX_sk1：上述 fact id 与「可以说 / 不能说」清单，用于 S09 / S21 / S22 / S25 / S36

## 2026-09-14 审查修改完成 — 2026-09-14 12:07:38
Auto-updated（FIX_sk1）:
- tools/gen_shots_sk1.py + 生成的 36 镜 / shotlist / all_shot_prompts / dialogue.md、4_剧本/script.md — 七份审查的修改全部落地：**36 镜 898 s**（不含可选 S36 为 874 s）；中文语速 1.17–4.75 字/秒、英文 0.80–2.64 词/秒；出镜说话占中文字数 18%；35 个切口全部强切，只有 S01→S02 承接
- 片序：… S33 绑包袱吹灯 → S34 五更醒来打分 + 签名收尾 → **S35 五更航拍收束（bg16）** → **S36 可选：今日州桥遗址（bg9）**
- 新增构建闸门：时辰 `tod` 单调、锁定串从卡上精确抽取比对、出镜台词必须落在脸在画的段且动作写看镜头、每镜写手位、柳枝 / 驴 / 包袱状态串按镜出现
- 新增英文旁白：每句林问台词一条英文，第二个 TTS 块用 `en-f-reporter-linwen-01`，与中文共用时间窗
- 史实修改：东水门是汴河出城处；删去无据的「明代立领 / 清朝辫子」「青团」两句；丑角不吹哨、杂剧分工口播「南宋书里记的」；书摊是蝴蝶装小册 / 卷轴 / 经折装；开封府只说尹 / 少尹 / 六曹；「一百五日最盛」指大寒食；米价工钱口播「按前后几年推算」；所有招牌提示词不写字（后期加）
- props/p1_旋煎羊白肠与食摊、scenes/bianjing/bg17_州桥夜市 — 食摊灯改为敞口陶灯盏带灯芯，去掉蜡烛残留
- style_guide.md §6 注记 — 林问出镜说话镜删去负向「对口型」；宣德楼绿琉璃瓦例外扩到 S17–S19、S02 尾段、S35
- 判断（节选）：S01 不挂 本镜末帧 handle（K26 ④ 首次生成豁免）；p4 / p7 / p9 卡锁定串仍要求写字，生成器暂以 `SIGN_BLANK` 派生无字版；bg9 卡「钢棚下」未证实，生成器暂以 `BG_PROMPT_FIX` 改写；时空考察队英文暂译 Time Expedition Team

In progress：SYNC_sk1（大纲 / 立项书 / 发布页 / README 同步到终版镜头 + 卡与工具遗留项，完成后删掉两个临时改写表）；B_city 按终版航线渲 S01 / S02 / S35 白模动画

## 2026-09-14 Blender 第二阶段 a 完成（全城层 + 航拍白模动画）— 2026-09-14 12:31:35
Auto-updated（B_city）:
- tools/build_bianjing.py → `scenes/bianjing/_blender/bianjing.blend`（6636 物件）— **全城层**直读 W11 §2.8 TOML：三重城墙（外城基宽 34.2 / 顶 4 / 高 8.7 m）+ 马面、36 门、5 河、护龙河、15 街、28 地标（艮岳工地、繁塔 / 铁塔）、宫殿 11 座、6437 街区（按方块号 → 资产键）、城东汴河沿岸郊区；**Place A / B / C 移到 W11 真实锚点**，§6 验收在新位置全部重跑通过，新增「全城层不侵入片区」检查
- shots/shot01、shot02、shot35 — `previz_config.toml` + `shotNN_previz.py` + `shotNN_previz.mp4`（30 / 30 / 20 s，1920×1080，25 fps）+ `frames_check/`；关键帧按各镜 `动作:` 时间轴；**S01 末帧与 S02 首帧相机状态完全一致、两帧像素差 0**；旧 shot36 航拍文件已删
- 航点按 R3 修正值（记在各镜 TOML 与 `city_plan.md` §9；W11 研究表保留原建议并加注）
- 判断：S02 结尾按提示词（离地 8 m、上仰约 10°、24 mm）而非协调消息里的数字——提示词是镜头真源（rule 4h §B）；S35 从 Place B 附近客店屋顶起、按 R3 相对位移拔高到 600 m
- 遗留：`tools/render_scene_view.py` 远裁剪同 render_scene_plan 的问题（第二阶段 b 顺手修）；city_plan 两处布局冲突（护龙河位置、御街宽度）在第二阶段 b 裁定

In progress：Blender 第二阶段 b（其余 33 镜白模动画）；SYNC_sk1

## 2026-09-14 文档同步 + 招牌无字清理 — 2026-09-14 12:59:39
Auto-updated（SYNC_sk1）:
- 3_大纲/outline.md、1_立项/concept.md、5_6_分镜与prompt/publish.md、README.md — 按终版 36 镜同步：片序 S35 航拍收束 / S36 可选遗址、898 s（不含 S36 为 874 s）、早市在辰时、开封府进院子 + 关扑、园林雅集独立主体、大寒食更正；发布页章节 26 条、封面 S04 01:44–01:48（备选 S02 00:59 / S26 约 10:52）、中英置顶评论与 S34 逐字一致
- props/{p4_饮子摊, p7_彩楼欢门与招牌, p9_桥尾脚店单元}、scenes/bianjing/bg9_今日州桥遗址 — 锁定串与 prompt 改为招牌空白、店名后期加字；bg9 锁定改「很深的考古发掘坑」（钢棚未证实）；生成器删除 `SIGN_BLANK` / `BG_PROMPT_FIX` 两个临时改写表，锁定闸门直读卡片
- style_guide.md（§2 / §3 / §5 / §9）、_series/glossary.md（R33 读音 + 英文专名表）、qc_stage2.md（锁定串副本过期注）、characters/c1–c4（指向生成器描述符、删过期 voice_id）、research parts 若干条 `note:`
- 判断：R2-40 往 shot_logic 加动词会让 hy2 / hy3 各多一条警告 → 撤回不改；R7 W12 切口标签文案在共用 shot_seam.py、改动会影响全部 hy 分镜表 → 不改；笑点计数 14（下限 15）不补，后半程是当天大事与夜里

Auto-updated（父级收尾）:
- tools/gen_shots_sk1.py — S15 英文台词「Maxing Street」→「Mahang Street」（马行读 mǎ háng），glossary 同步
- scenes/bianjing/bg1_虹桥、bg5_正店酒楼 与 world.md 真实性铁律第 1 条 — 「画面文字只有四块店名」改为「画面里不生成任何文字、四块真实店名一律后期加字」；bg1-1 锚点压回 1998 字（硬顶 2000）
- 重建 + 四道闸门全过；终版正向 prompt 里店名只出现在林问台词中（0 处作为招牌文字）

Validation：reviewer 的一次性格式脚本已落后于新格式（中英分块配音、台词行〔类型·时间窗·口型·视线〕注记），原样重跑出 ~1100 条原始告警 → 另起 R8_final_format 做终版格式复核并裁定 K21（台词注记是否有被烧成字幕的风险）

## 2026-09-14 终版格式复核（R8）+ 最后一轮修改启动 — 2026-09-14 13:21:21
Validation（R8_final_format，检查器改到新格式、不降级）：原始 1108 条 → 99 条，其中确认真实 blocker 3、warning 9；R7 的 F01–F05 均未复现；三道仓库闸门全过
- B1（K21）：`台词:` 方括号里夹时间窗与视线——判定违反台词契约 v2（带时间戳的台词行正是字幕形状）；改为方括号只留类型与口型，开口与视线时间表挪进 `走位:`，时间窗只留在配音块 / dialogue.md / script.md
- B2（K29）：shot11 / 12 声音 token 顺序；B3（12.4-H）：shot36 第 4 句情绪为空
- 中英分块配音判定合规（12.4-H / 17.5）

Decisions（判断）：
- 照改：W1 七个多句出镜镜补「全程绝对无字幕」前缀（STYLE_BASE 与 style_guide §7 同步）；W3 人物卡新增「shot 角色行锁定串」逐字字段、生成器闸门比对；W9 胸牌锁定串不再要求模型写「时空考察队」五字（淡墨不可读笔画、店名式后期加字）
- 不改：W2 切口标签文案在共用 `tools/shot_seam.py`，改动会波及全部 hy 分镜表；W4「骨朵」平台未拒审前不换；W7 myth.001 缺原文引句不凭记忆补

Auto-updated（父级）:
- specs/ai_video/sk1/divergence.md — #15 补 S08 换装镜现代装段与 S36 今日遗址；#16 补建筑单体 p9（长相依据在 bg1 参考图）
- 2_世界观人设/casting.md — 林问「出场镜」由占位改为按生成器实填：现代装态 S03–S08、S36；宋装态 S08–S34（S26 不在画）

In progress：FIX2_sk1（B1–B3 + W1 / W3 / W9，重建 + 闸门 + 新检查器复跑）；Blender 第二阶段 b

## 2026-09-14 终版格式修改完成 + 第一次提交 — 2026-09-14 13:34:33
Auto-updated（FIX2_sk1）:
- tools/gen_shots_sk1.py + 36 镜 — `台词:` 方括号只留三种合法写法（类型 + 口型），开口与视线时间表挪进 `走位:`（32 个林问在画的说话镜），新增 `gate_line_tags()`；S11 / S12 声音 token 紧跟林问视觉 token；S36 第 4 句情绪「轻，落定」且 `gate_speech()` 拒绝空情绪；`STYLE_BASE` 加「全程绝对无字幕」前缀（与 style_guide §7 逐字一致）
- characters/c1–c4 与系列 c1 卡 — 新增「shot 角色行锁定串（逐字，生成器闸门比对）」字段；生成器锁定闸门逐字比对
- props/p3_三件不变物 + `P3_BADGE` — 胸牌改为「牌面只见几道淡墨笔画痕、没有可读的字」，任何 prompt 里不再出现「时空考察队」字样（名称只作后期加字）；p3 锚点 1539 字
- 验证：严格构建 + prompt_light + shot_logic + facts_registry 全过；新检查器 blocker 0（R8 为 37）；`动作:` 时间轴未变，渲染中的白模动画不受影响

Commit 1（本条之后）：系列与 sk1 文字产物、规则与工具（只取 ai_video.md 的 rule 17 一段）；**不含** 仍在渲染的白模动画与 `_blender/`、`tools/build_bianjing.py`；本次以 `ASSETS_SYNC_AUTO_PUSH=0` 暂不同步媒体（避免把渲染到一半的 mp4 传上 R2），第二次提交再同步

## 2026-09-14 提交前发现：事实注册表被 .gitignore 忽略 — 2026-09-14 13:36:07
- 根 `.gitignore` 第 19 行的 Python 模板规则 `parts/` 把 `ai_videos/**/0_research/parts/`（538 条事实的唯一出处，生成器直读）整目录忽略了；照原样提交，新克隆的仓库构建不了分镜、研究成果也不进 git
- 判断：不用 `git add -f` 一次性绕过，而是在 `.gitignore` 紧跟 `parts/` 加反向规则 `!ai_videos/**/0_research/parts/`——以后 sk2 / sk3 的研究目录自动入库

## 2026-09-14 第一次提交完成 — 2026-09-14 13:36:30
- 本地提交 `fe26cd2`（152 个文件）：系列与 sk1 的文字产物、规则 / skill、工具、`.gitignore` 事实注册表放行；未推送远端；媒体未同步 R2
- 留给第二次提交：`tools/build_bianjing.py`、`scenes/bianjing/_blender/`、各镜 `previz_config.toml` / `shotNN_previz.py`（Blender 第二阶段 b 完成后）+ 媒体同步 R2
- 不属本系列、两次提交都不带：`tools/gen_scene_prompts_hy4.py`、`tools/gen_shots_hy4.py`、hy4 文件、即梦桥接、index-tts、临时文件

## 2026-09-14 Blender 第二阶段 b 中断后续跑 — 2026-09-14 20:47:02
- B_city 规划完第二阶段 b 后因 API 认证错误（HTTP 403）停止，未渲出任何镜头；核对：无残留 blender.exe、除 shot01 / 02 / 35 外无半截白模动画；`tools/build_sk1_sets.py` 为中断前产出
- 判断：续用同一个建城 worker（保留建城与航拍上下文），按「S 档与城内镜优先、再内景」顺序做，每做完一镜在 `blender_build.md` §9 记进度，便于再次中断后接着做

## Follow-up 002–004（sk1）— 2026-09-14 22:09:42
Source: specs/ai_video/sk1/user_input/follow_ups/202609.md - sections 002, 003, 004
Summary: 参考图进 1:3–3:1 上传窗口；世界锚点由 bg1-1 改为 bg0-1；全片天要蓝、水要绿（晴天航拍效果）。

Auto-updated:
- tools/ref_aspect.py — **新建**：`check` / `fix` 宽高比窗口（≤ 6:1 补中性边到 3:1，更长折行拼版，不裁内容）；37 张 sk1 `ref/` 图已原地处理，复查 0 张越界
- tools/ref_fetch.py — `pull` / `register` 入库即调 `fit()`；pyproject.toml / requirements.txt 加 pillow
- .claude/agent_refs/project/ai_video.md — rule 17.7 上传图宽高比窗口（全局规则）
- 14 个资产的 refs.md — 记下哪几张被补边 / 折行
- scenes/bianjing/bg0_汴京全城 — bg0-1 成为世界锚点（只挂 ref11）、验收 / 出图顺序 / 挂法重写；bg0-1 与 bg0-2 天蓝水绿；字数重算
- scenes/bianjing/bg1_虹桥 — 降为虹桥地点锚点、`参考:` 首项挂 bg0-1；天蓝水绿；字数重算
- scenes/bianjing/bg16_汴京全城五更 — 唯一参考 bg0-1（兼世界锚点），去掉 bg1-1；锁定串「灰蓝天光」→「清冷蓝光」（生成器 BG 同步）；天与水改蓝绿
- scenes/bianjing/bg2–bg15、bg17 — 世界锚点句柄与参考用法换成 bg0-1（只取基调、不取高空视角）；【天】改晴天蓝天、夜镜深蓝；去掉遮远景的薄雾；河水 / 御沟碧绿
- props/p8_虹桥单体 — 世界锚点措辞更正；河面改碧绿（阴天光照不动，image-to-3D 前提）
- _blender/city_plan.md — 排版底图河色改碧绿
- world.md / casting.md — 世界锚点与继承拓扑、出图顺序改为 bg0-1 最先
- style_guide.md — §1 天要蓝水要绿、§2 水与天色锁定、§3 卯时基准与「天与水」条件分句说明、§6 新增天与水负向两行
- tools/gen_shots_sk1.py + 36 镜 + all_shot_prompts.md — `光线:` 按时段追加 SKY_DAY / SKY_DAWN / SKY_NIGHT（航拍镜加晴天无人机航拍比喻）、负向加 NEG_SKY / NEG_SKY_NIGHT；S01 / S02 / S03 / S05 / S17 / S26 / S30 / S31 / S34 / S35 灰霾与浑黄措辞改掉
- 4_剧本/script.md — S26 画面动作「浑黄的浪头」→「泛白的浪头」
- specs/ai_video/sk1/divergence.md — #17 世界锚点在 bg0、#18 天蓝水绿与 `boat.001` 浑黄记载相左

No conflicts found in: 1_立项/concept.md、3_大纲/outline.md（S01「穿出贴水的晨雾」保留——只是贴水一层，不遮蓝天）、characters/*、props/p1–p7、p9、p10（无天空或阴天 image-to-3D）、0_research/*（事实注册表不改）

## 2026-09-14 Blender 第二阶段 b 进行中（中期记录）— 2026-09-14 22:34:23
Auto-updated（B_city，渲染队列仍在跑）:
- 渲染方式：只有 S03 / S05 / S11 / S32 用通用引擎 `tools/previz/build_previz.py`（单机位、无变焦）；其余镜头因引擎做不了镜内切、变焦、跟拍与城景切布景，改用新共用执行器 `tools/previz_sk1.py`（S 档）——生成器里的 `previz 档` 字段待队列结束后按实际更正
- 城市几何：`tools/build_bianjing.py` 新增六个精细片区 D 宣德楼 / E 汴河码头 / F 开封府 / H 相国寺 / I 桑家瓦子 / J 南薰门外；`tools/build_sk1_sets.py` 新建九个简单布景（客店房间、早市摊、医馆门面与铺内、园池、勾栏、正店阁子、遗址坑等）
- 布局裁定（判断）：护龙河按 W11 放在城墙脚外 30 m、宽 38 m（旧表值与城墙重叠 7 m）；御街宽按 W11 320 m，朱杈子移到 ±19.5 m（在御沟外侧，合原文）、黑漆杈子 ±150 m、御廊 ±154…160 m
- `tools/render_scene_view.py` — 远裁剪伸到场景最远角、近裁剪随距离与高度缩放
- 逐镜截帧检查：S03 / S06 / S26 通过；S04（机位穿过人物）、S05（头被切、柜台出画）、S16（人走过机位、头被切）已改走位与机位并重排重渲
- 判断：S01 / S02 / S35 航拍是在护龙河挪位、宣德楼精细片区建成前渲的，排在队尾按终版城市重渲，相机关键帧不变、S01 末帧与 S02 首帧仍须逐像素一致

## Follow-up 005–006 — 2026-09-15 15:05:39
Source: user_input/follow_ups/202609.md - sections 005, 006
Summary: 场景 blend 从灰模升级为写实城市（取色自锚点图、形制 / 禁用项取自场景卡 prompt），shot01 / shot02 blend 从新场景拷贝重建并加人物与动作。

Auto-updated:
- tools/look_bianjing.py — **新建** look pass：锚点图采样取色 + CC0 PBR（pack 进 blend）；G_BLOCKS / 郊外单元盒 → 144 492 个宋式民居 GN 实例（城内零草顶）；p8 虹桥 / p9 / p10 / p10a 细模；柳树球 → 垂柳（截头老干、长柳丝）；御街两侧 → 桃李梨杏花树（bg4）；50 个歇山体块 → 平缓曲面屋顶 + 素木斗拱（仅宣德楼绿琉璃 + 朱漆）；城楼盒 → 木构城楼（直棂窗、平坐栏杆）；物理天空 + 22° 晨光 + 远郊地面外圈；`--stills` / `--frames` 出校验图
- tools/polyhaven_fetch.py — **新建** CC0 纹理拉取；_blender/textures/polyhaven/ 12 套（gitignore、走 R2）
- tools/build_bianjing.py — builder 跑完 QC 默认接 look pass（`--no-look` 关）；QC §6#7 / 走廊三角 / 几何摘要跳过 look 标记（布局摘要 38a7ff… 不变）；航拍 previz 加 `水手`（抱桅后仰 / 撑篙）与 `[["人群"]]`（沿线行走、贴虹桥桥面），场景已写实化时船用平底纲船细模；远裁剪 2000 km
- shots/shot01/previz_config.toml — 放桅纲船 3 名水手；桥上行人 8
- shots/shot02/previz_config.toml — 御街东西两侧行人各 10（御道空无一人）
- shots/shot01|02/shot0N_previz.blend — 从写实化场景重新拷贝重建；shotNN/look/ 下 Cycles 校验帧
- _blender/look_0{1..8}_*.png — 场景写实化校验图（机位表在 look_bianjing.VIEWS）
- _blender/blender_build.md — §4 步 8 look pass；§7 禁止条款改为「布局代码不上材质」
- specs/ai_video/sk1/divergence.md — #19 场景 blend 写实化（偏离 rule 4h §D1 / 4g §K）

未落地（需要改布局 builder，另起任务）：马面 / 瓮城、宣德楼 U 形朵楼廊庑、东水门木框水门洞 + 马道、坊巷排水沟、田埂、彩楼欢门沿主街铺开；shot01 / shot02 的 previz mp4 未重渲（机位与动作时刻未变，灰模 mp4 仍有效）

No conflicts found in: 1_立项/concept.md、3_大纲、4_剧本/script.md、shot01.md / shot02.md prompt 文本（走位与动作时刻未改）

## Follow-up 007 — 2026-09-15 19:32:16
Source: user_input/follow_ups/202609.md - section 007
Summary: 全城与城外均匀铺满房子、建筑与人（对照 bg0-1）。

Auto-updated:
- tools/build_bianjing.py — 街区改逐栋判断 keep-out（KeepIndex）+ 院内背靠背小院，keep-out 收窄到一条路宽；宫城殿宇 72 座铺满；新增 build_gate_suburbs（11 座城门外关厢 13 031 栋 + 外廓散居 + 过壕桥 + 行道柳）与 build_hamlets（226 村 3 030 户）；灰模 previz 隐藏 LOOK_people；布局几何摘要变为 fc7cb2…（布局真的变了）
- tools/look_bianjing.py — 城外房按来源定草顶比例（村落 75% / 关厢 20%）；新增 LOOK_people 约 31 000 静态行人（只进写实渲染）；人物衣色本白 / 皂黑 / 灰青
- tools/previz_sk1.py — 地面探针跳过 look 层；灰模渲染隐藏 LOOK_people
- _blender/city_plan.md §8 — 铺满规则（全部 C 判断）
- bianjing.blend、shot01 / shot02 previz blend + 灰模 mp4 — 重建；房子 144 492 → 262 667

## 系列 follow-up 012 — 2026-09-15 21:21:22
Source: ../shikong_lvxing/user_input/follow_ups/202609.md - section 012
Summary: 旅行者换成可选的 vlogger 候选（默认 c1 林问新形象）；视频直接出声；本站不再放旅行者卡，本地人物改键 c21–c23；宋装形制单列 p11。

Auto-updated:
- 2_世界观人设/characters/ — c1_林问 迁出（系列名册）；c2_李十六 / c3_周四娘 / c4_沈十九 → c21 / c22 / c23（文件、路由键、ref_id、w3_clothing 与 dossier 引用同步）
- 2_世界观人设/props/p11_旅行者宋装/ — 新增
- 2_世界观人设/{casting.md, relationships.md, qc_stage2.md, style_guide.md, props/p4_饮子摊} — 同步
- 5_6_分镜与prompt/{shots/shot01–36, all_shot_prompts.md, shotlist.md, publish.md} + 4_剧本/{dialogue.md, script.md} — 由 tools/gen_shots_sk1.py 重生（声音行、声样参考、c21–c23、新 voice_id）
- specs/ai_video/sk1/divergence.md — #20–#23

No conflicts found in: 1_立项/concept.md、3_大纲/outline.md（旅行者以占位名出现）

## Follow-up 008 — 2026-09-15 22:15:00
Source: user_input/follow_ups/202609.md - section 008
Summary: 城内降密、去整齐网格，房子按面宽 / 层数 / 类型分级，依据史料 w12 城市密度调研。

Auto-updated:
- 0_research/parts/w12_urban_density.md — **新建**：户口、宅院规模、坊巷肌理、城内空地调研（S / S* / J 分级）
- tools/build_bianjing.py — 80 m 网格街区改为 `FABRIC` / `LOT_MIX`：300 m 大街区朝向抖动 ±11°，BSP 切 1 200–9 000 m² 地块、巷宽随机；按里城 / 外城东南 / 西北 / 近城墙分区定占用概率，干道与河边加密；地块类型 = 前店后宅 / 小屋排 / 一至三进院落（院墙 + 门屋 + 正厅 + 厢房）/ 大院 / 草屋 / 军营长屋 / 园圃池塘空地（带树）；层数九成单层、两层集中繁华沿街、三层只偶见正店。城内地块计数：garden 9 344、row 2 060、huts 1 212、courtyard 953、barracks 507、shops 466、compound 109；清掉中途留下的两份重复 `KeepIndex` / `FABRIC` 定义；布局几何摘要 fc7cb2… → 6274e6…
- tools/look_bianjing.py — 民居原型按面宽档（4 / 8 / 12 / 18 m）× 层数（1 / 2 / 3）× 式样（瓦 / 铺面 / 草 / 楼）分，实例只做小幅缩放；18 m 单层宽屋明间高、次间低
- _blender/city_plan.md §8 — 「街区 80 m 网格铺满」划掉，改写城内肌理规则（全部注明依据）
- bianjing.blend — 重建：全城房 262 667 → 71 490（城内 54 555）、树 68 632、静态行人约 31 000 → 11 988；QC 全过（仅表行自身尺寸 WARN，与本次无关）
- _blender/look_01 / 03 / 06 / 07 / 08 — 重渲校验图（02 / 04 / 05 为近景 Place，布局未动，沿用）
- shots/shot01|02/shot0N_previz.blend + shot0N_previz.mp4 — 从新场景拷贝重建、灰模重渲（各 750 帧 / 30 s）；shot01 末机位 = shot02 首机位 (5760, -4470, 152) 仍一致；机位与动作时刻表未改
- shots/shot01|02/look/*.png — Cycles 写实校验帧重渲
- shots/shot01|02/look/shot0N_look.mp4 — 2026-09-16 按新场景 Cycles 重渲写实视频（1280×720、96 采样、各 750 帧 / 30 s，逐帧计数校验后替换）

No conflicts found in: 1_立项/concept.md、3_大纲、4_剧本/script.md、shot01.md / shot02.md prompt 文本、previz_config.toml、divergence.md（#19 已覆盖写实化偏离）

## previz 取景对账 — 2026-09-15 22:50
Source: 自查（非用户 follow-up）——检查新渲的白模时发现取景与 `景别档` 不一致

Summary: `景别档:`（排镜的第一约束）与 S 档白模实际取景第一次逐镜对账：29 个 S 档镜只有 3 个两端都落在 spec 的 ±40% 内。

Auto-updated:
- tools/previz_sk1.py — 渲完落盘 `shotNN_previz_report.txt`（每个机位关键帧的人占画高 / 在不在画内），与产物同寿
- tools/previz_frame_fix.py — 新增：按 `人占画高 ∝ 焦距 / 距离` 反解机位（室内退距 ≤1.8 倍、室外 ≤2.5 倍，焦距夹 20–120 mm）；默认只修「人被裁出画」的关键帧，物件特写档与「人还在画里」的偏差只报不改
- 5_6_分镜与prompt/shots/{shot07,shot08,shot28,shot29,shot31,shot34}/previz_config.toml — 改焦距 + 机位距离；已复核 shot29 4.44→1.23（spec 1.20）、shot31 2.12→0.77（spec 0.75）
- 5_6_分镜与prompt/shots/shot33/previz_config.toml — 20–28 s 切后的机位原来把她挤出画外（`in_frame=0`），看向改到她落座处
- 2_世界观人设/scenes/bianjing/_blender/blender_build.md §9.2 — 对账做法、结果表、事故与处置
- .claude/agent_refs/project/ai_video.md 4h §J / §K — 两条教训（白模取景必须与 `景别档` 对账；批渲进行中不许改运行库）

Open decision（等用户定，未动）:
- **室内镜的 `景别档` 与镜头 / 房间尺寸矛盾**：客店房间宽 4.2 m，「50 mm ＋ 近景 0.80」需要 5.4 m 机距；shot33 落幅写 0.30，房间里退到对角也只能到 ≈0.45。三条路——改 shot md 的景别值（连带重算该对切口比值，可能触发相邻镜连锁改）／改走位让她离镜头更近／认下更广的镜头。涉及 shot04、06、07、08、12、13、14、16、17、18、19、21、22、23、24、25、27、28、31、33、36 的一端或两端（详见 blender_build.md §9.2 与 `python tools/previz_frame_fix.py ai_videos/shikong_lvxing/sk1` 的报告）。

事故: 批渲进行中改运行库（加落盘报告）→ 字符串换行没转义 → 之后 17 镜 3 秒内 SyntaxError 失败；运行库已修并 py_compile，失败镜与改过配置的镜已重渲（queue4，22 镜）。


## Follow-up 009 — 2026-09-16 12:40:30
Source: user_input/follow_ups/202609.md - section 009
Summary: shot01 / shot02 重排为「河上 8 秒 → 穿东水门 → 城里穿梭 → 拉高看大半个城」，两镜无台词。

Auto-updated:
- tools/gen_shots_sk1.py — S01 / S02 镜表条目整条重写（bg / vx 场景参考、cuts 四段、jb·jbcam 接缝、情节 / 镜头 / 走位 / 动作 / 光线 / 节奏 / 判断），`lines=[]`；`gate_shape` 的「S02 末句必须是签名开场」删除、「签名开场只出现一次」放宽为「最多一次」（用户选择本站不要签名开场）；S02 facts 换掉 ⚠️ `ent.015` → ✅ `shop.006`，并加 `route.010`（御沟荷与岸边桃李梨杏）`city.038`（两塔）
- shots/shot01|02/shot0N.md + all_shot_prompts.md + dialogue.md + script.md — 生成器重跑产出（prompt 2217 / 2224 字，≤5000；36 镜 898 s；接缝全 ✅）
- shots/shot01|02/previz_config.toml — 四段机位重写：汴河@A 虹桥段 → 汴河@B 穿水门（水面上 4 m，闸门吊在 z 6–8、门楣在 z 8 以上，previz 实测 z 8.5 会埋进实体渲成全黑）→ Place E 码头 → 汴河@C 州桥东减速；shot02 承接后 Place C 御街 → Place H 相国寺（高位 38 m 斜对中轴）→ Place I 瓦子 → 世界 (2700,-2000,2200) 拉高；新增码头纲船与脚夫、相国寺书市与瓦子门口人群
- tools/look_bianjing.py — 阙楼（`_que` 高盒子）升级为砖台 + 木构楼身 + 曲面瓦顶（原来渲成一块白板，正落在 shot01 末帧里）
- shots/shot01|02/shot0N_previz.blend + shot0N_previz.mp4 + look/shot0N_look.mp4 — 全部重建重渲

No conflicts found in: 3_大纲/outline.md（序段仍是两条航拍长镜）、其余 34 镜（时辰与接缝未变）

## Follow-up 010 — 2026-09-16 14:32:10
Source: user_input/follow_ups/202609.md - section 010
Summary: shot01 / shot02 改成一镜到底，撤掉 follow-up 009 排的镜内硬切。

Auto-updated:
- tools/gen_shots_sk1.py — S01 / S02 的 `cuts=` 全删，新增共用运镜口径常量 `RAMP`（连续运镜、不切、无急转、无折返）；`gate_shape` 放宽（S02 不再强制签名台词行，签名开场最多出现一次）
- shots/shot01/previz_config.toml、shots/shot02/previz_config.toml — 关键帧重排为单条连续航线，零 `"切" = true`
- shots/shot01/shot01.md、shots/shot02/shot02.md — 由生成器重出（`分镜:` 段落取消，`镜头:` / `动作:` 改为一条连续时间轴）

No conflicts found in: 2_世界观人设/、4_剧本/、其余 34 镜

## Follow-up 011 — 2026-09-16 16:05:40
Source: user_input/follow_ups/202609.md - section 011
Summary: 郊区收小、起飞点挪近、全程真无人机速度、航线不作 90° 转弯；结尾按用户选择收在约 320 m。

Auto-updated:
- tools/build_bianjing.py — 关厢出城路 1200 m / 12 m 宽（原 2600 m）、田间村落格 700 m、村落带收到离墙 2600 m 以内
- shots/shot01/previz_config.toml — 起飞点改到东水门外 350 m（虹桥退出航拍），全程 33–50 m/s
- shots/shot02/previz_config.toml — 桑家瓦子与州桥退出航线（它们要求急转 / 折返），结尾爬升收在约 320 m
- tools/gen_shots_sk1.py — S01 / S02 的 `jbcam` / `summary` / `plot` / `cam` / `act` / `spatial` / `judge` 按新航线重写
- ai_videos/.../scenes/bianjing/_blender/bianjing.blend — 按新 builder 重建（布局层几何摘要不变的部分照旧）

用户定调里没有照办的一条（已当面说明）：城内不按比例缩小——城墙、街道、地标的坐标来自 W11 考古实测（外城 x −4132…3904 / y −3625…5699），缩城会让所有史料 fact 与地面镜失效；改的是航线长度与郊区带宽度。

No conflicts found in: 0_research/、4_剧本/、地面 34 镜

## Follow-up 012 — 2026-09-16 19:52:05
Source: user_input/follow_ups/202609.md - section 012
Summary: 码头段压到 8 秒整，省下的时间分给城内汴河段、相国寺与结尾爬升。

Auto-updated:
- shots/shot01/previz_config.toml — 码头 11–19 s（8 秒，约 30 m/s）；城内汴河段 19–30 s（11 秒）；码头入口关键帧从 (2792,−2688,9) 挪到 (2750,−2688,8) 并把看点推远到 (2700,−2566,6)——原位置 ray_cast 实测落在外城东墙墙体里（墙在 x≈2790），出洞后有一秒多画面全是夯土
- shots/shot02/previz_config.toml — 相国寺 12–22 s（6→10 秒）、结尾爬升 22–30 s（6.5→8 秒）；城内汴河平直段压到 12 秒
- tools/gen_shots_sk1.py — S01 / S02 的 `cam` / `act` / `vx` / `moment` / `judge` 同步改时刻表
- shots/shot01/shot01.md、shots/shot02/shot02.md — 生成器重出（prompt 1739 / 2038 字，K10 / K31 / K34 全过）

取舍（已告知用户）：码头给满 8 秒后，shot02 城内汴河段只剩 12 秒，而东水门到州桥实测 2.8 km，这一段要跑约 95 m/s、快于真无人机；选它是因为这段是平直河道、两岸铺面重复，是全镜信息量最低的一段。

No conflicts found in: 其余 34 镜、scene blend 布局层

## Follow-up 013 — 2026-09-16 20:24:30
Source: user_input/follow_ups/202609.md - section 013
Summary: 常规交付＝每镜一个单独 mp4（喂 Seedance 的参考素材口径）；合成 mp4 是一次性需求、不入流程。

Auto-updated:
- （无产物改动；本条改的是交付方式）单镜 mp4 按该镜 md 的 `比例:` / `时长:` 出、用高码率不做重压缩（压缩块影会被生成模型学进画面）；合成版只在用户明确要求时另做

## Follow-up 014 — 2026-09-16 23:08:19
Source: user_input/follow_ups/202609.md - section 014
Summary: 全站画风改《权力的游戏》实拍电影感（先 research 再改，所有 prompt 重出）；汴京 3D 由全城改为航线走廊制、航拍封顶低空取消俯视；旧 png / mp4 / blend 全删。

Auto-updated:
- 2_世界观人设/look_research.md — **新增**。画风调研：现有图为什么像动画（8 条逐条诊断，含「喂宋画出画」这一最大成因）、GoT 实拍感由什么构成（器材 / 只用动机光且不怕黑 / 真材料逐块做旧，附出处）、与既有定调的冲突裁决表（蓝天绿水保留，改的是晴天的画法）、进 prompt 的词表
- 2_世界观人设/style_guide.md — §1 加「画风基准＝GoT 实拍电影感」六条；§3 加「光的四条纪律」（先找逆光 / 写光比 / 暗部不救 / 空气里必须有东西）并改写卯时基准行；§6 加「反 CG 块」（挡成因不挡症状）；§7 `STYLE_BASE` 整串换成可执行的摄影事实并删掉「全景深」；§10 **新增**参考图政策（宋画退出上传）；§11 **新增** `摄影:` 与 `【质感与做旧】` 两条新行
- tools/gen_scene_prompts_sk1.py — **新增**。stage-2 图 prompt 的 look 层唯一出处：37 个 prompt 的 `参考: / 参考用法: / 摄影: / 【天】/ 【光】/ 【质感与做旧】/ 光色: / 样式: / 渲染样式: / 做旧: / 负向块 / 上传行 / 字数行` 逐卡盖章，内容层不碰；`机位:` 里的 `f8，全景深` 由它摘掉；跑两遍结果逐字节相同；`--check` 只校验不写盘
- 2_世界观人设/{scenes,props,characters}/**/*.md — 37 个图 prompt 全部重出（21 个 bg 视图 + 8 个 p 锚点 + 3 张立绘 + bg17-2）。p8 / p9 / p10 三视图与 c* turntable **故意不动**：它们是 image-to-3D 白模输入，按 divergence #18 必须阴天均匀光
- 2_世界观人设/scenes/bianjing/bg16_汴京全城五更/ — 机位由「高空 3800 m 俯瞰全城」改为「屋脊上方 110 m 低角度看屋海」，与降下来的 shot35 对齐
- tools/gen_shots_sk1.py — `STYLE_BASE / NEG_BASE / NEG_ARCH / NEG_CG / SURFACE` 改为从 look 层生成器 import（两边不可能漂）；每镜新增 `摄影:`（光圈按 `jb` 的人占画高分档）与 `做旧:`（按 bg 挑面）两行；`光线:` 末尾统一追加光比与暗部纪律；`SKY_DAY` 的「远景清楚」改为「大气退远」；S02 / S35 的 `cam / act / summary / plot / spatial / contrast / jbcam / judge` 按新航线重写
- 5_6_分镜与prompt/shots/*/shot*.md + all_shot_prompts.md + shotlist.md — 36 镜全部重出（prompt 1817–4675 字，K10 / K31 全过）
- shots/shot02/previz_config.toml — 末段爬升（22–30s 升到 320 m、俯角 38°）整段作废，改为低空续飞 26→42 m、俯角 < 2°
- shots/shot35/previz_config.toml — 悬停高度 602 m → 110 m
- scenes/bianjing/_blender/city_plan.md — §8 精度分级整条重写为走廊制；**新增 §8.2「航线走廊」**（三档线半径 + 三档 Place 半径 + 走廊 leg 表，坐标全部取自 W11 现有的河 / 街折线与 Place 锚点，一个新坐标都不写）
- tools/build_bianjing.py — 新增 `Corridor` 与 `load_corridor()`；`house()` 成为唯一闸门（城内街区 / 城外关厢 / 田间村落三条路都汇进它）并新增 **A 级**建筑（台基 + 墙身 + 出檐悬山 + 正脊 + 临街披檐）；`build_blocks` 加整块街区粗筛；QC 报「走廊内建房 / 走廊外砍掉」
- tools/look_bianjing.py — `sample_palette()` 加闸门：锚点图不在盘上时给出可执行的错误（先 `--no-look` 建灰模，新锚点落盘后再 dress），不再抛裸文件错误
- scenes/bianjing/_blender/bianjing.blend — 按走廊制重建（`--no-look` 布局灰模；走廊内 10 580 栋 / 走廊外砍掉 17 488 栋，A 2 094 / B 3 078 / C 5 408）
- ai_videos/shikong_lvxing/sk1/**/*.{png,mp4,blend,blend1} — **589 个文件、3.44 GB 全部删除**（用户授权）；`ref/` 下 276 张史料参考图保留（它们是形制与验收的依据，只是不再上传）
- specs/ai_video/sk1/divergence.md — #8 收窄（画类参考退出上传）；新增 #24（图 prompt 字数 1200–2800）、#25（全城层走廊制）、#26（航拍封顶低空、全片无俯视）
- .claude/agent_refs/project/ai_video.md — 新增 rule 18（「像动画」的四个成因与修法，可泛化）与 rule 19（环境几何走走廊制）

No conflicts found in: 0_research/、1_立项/、3_大纲/、4_剧本/（台词与剧情未动）

未做 / 待办（已知，明确列出）:
- **36 镜 previz mp4 未重渲**：全部旧 mp4 已删，几何与 shot02 / shot35 的航线都变了，必须整批重渲（rule 4h ⑥：不许重叠跑）。已验证 shot02 的 previz 能正常建场与出帧（首帧 (1794.9, −1064.8, 14.0)、末帧 (305, 580, 42)，末段确无俯视），单帧抽检画面无空洞；整批渲染是数小时的活，留给下一轮
- **look pass 未重跑**：材质色取样自各地点锚点图，而锚点图正等着按新画风重出；新图落盘后跑 `blender -b bianjing.blend --python tools/look_bianjing.py -- --save`
- **照片类参考库只补了 bg1**：本机不通外网，`ref_fetch` 抓不到；清单写在 style_guide §10
- **assets.json 未整理**：`boto3` 未安装、`assets_sync` 跑不起来，manifest 仍指向 R2 里已删的旧媒体（好处是旧图还能找回来）。装好依赖后跑 `python tools/assets_sync.py push --prune-missing` 让索引与盘上一致

## Follow-up 014 修订 — 2026-09-17（用户当面口径：图 prompt < 2000 字、video prompt 5000 字）

Summary: 图 prompt 的上限收回 2000（原 follow-up 014 曾上调到 2800），靠共用串去重挤进去；video 侧 5000 硬线本来就有、已复核。

Auto-updated:
- tools/gen_scene_prompts_sk1.py — `LO, HI = 1200, 1999`，**超上限一律 raise**、偏短只提醒不拦；`STYLE_TAIL` 由 299 字压到 210（反 CG 长清单交给负向块的 `NEG_CG`，正向只留一句）；`【天】/【光】/【质感与做旧】/摄影:/参考用法:` 逐条收紧；做旧由四面改**三面**；**`光色:` 整行取消**（「与世界锚点同一套影调」`参考用法:` 已经说过一遍，两处写就是副本）
- tools/gen_scene_prompts_sk1.py — **焦距改为写死在 `LOOK` 表的 `foc=` 字段**。原来是从卡的 `机位:` 行回读，但那一行的光学尾巴正是本文件要摘掉的，第二遍就读不到、会悄悄退回 35mm 默认值（已发现并修复；36 个焦距从 git HEAD 挖回原值逐条核对，盘上与表零差异）
- 2_世界观人设/**/*.md — 37 个图 prompt 重出，**字数 1128–1988，全部 < 2000**
- 2_世界观人设/scenes/bianjing/bg1_虹桥、bg0_汴京全城 — 内容层去重（做旧词已由 `【质感与做旧】` 接管的部分、重复的解释性叮嘱、`远景清楚`→与大气退远矛盾的说法）
- tools/gen_shots_sk1.py — 随共用串一起变短，**video prompt 1705–4518 字**；`MAX_PROMPT = 5000` 的硬 gate 本来就在（超限 raise），复核通过
- style_guide.md §7 / §11.1 / §11.2 + divergence #24 — 与上面逐条对齐

复核：生成器跑两遍字节相同（幂等）；`prompt_light` / `shot_logic` 在 sk1 范围内 0 blocker

## Follow-up 015 — 2026-09-17
Source: user_input/follow_ups/202609.md - section 015
Summary: Hyper3D 接入并测通（无头），物件优先流水线的骨架落地；自动出图一环因 ElevenLabs 无图像能力而挂起。

Auto-updated:
- .env（gitignored）— 新增 `HYPER3D_API_KEY`、`ELEVENLABS_API_KEY`；两个 key 都不进任何被 git 跟踪的文件
- tools/hyper3d_fetch.py — **新增**。Rodin 的无头 HTTP 适配器（建任务 → 轮询 → 下 GLB），请求体照 `addon.py` 的 `create_rodin_job_main_site`。走 HTTP 而不是 BlenderMCP，是因为 MCP 那条路要开着 GUI、且 `blendermcp_use_hyper3d` 是 per-scene 开关，进不了 pipeline。实测两处与 addon 不符、已修：`texture_mode` 不接受 `"None"`（合法值 legacy…extreme-high，白模用 `minimum`）、`bbox_condition` 只吃整数（内部按最大边归一到 100）
- tools/gen_object_cards.py — **新增**。读物件清单 → 生成 `props/pN_{名}/{名}.md`（锚点 + 正/侧/背四张图的 prompt，正交 + 阴天均匀光，divergence #18）与 `object.toml`（归一化 + 验收规格骨架）。`object.toml` 已存在时不覆盖——阈值是人调过的
- 2_世界观人设/object_inventory.toml — **新增**。第一批 16 个物件（p12–p27），按 rule 4g §B 只收有界物件；环境与整栋建筑不进清单
- 2_世界观人设/props/p12…p27/ — 16 个物件文件夹 + 四图 prompt + 验收规格

验证（实测，不是推断）:
- Hyper3D 打通：Sketch 档 71 s 出「太平车」raw.glb（1.8 MB，23 332 tris），渲四视图人眼验收——板车面、辐条轮、轮毂、铁箍都在
- **同时暴露 text-only 的短板**：prompt 里写了的两根车辕没有生成出来。薄长件正是 image-to-3D 最不稳的地方，**这恰好证明用户提的三视图流程是对的**——多视角参考能把这一类件按住

挂起（需要用户定夺）:
- **自动出图**：ElevenLabs 是语音 API（TTS / 音色 / 音效 / 配音），**没有图像生成接口**，出不了三视图与场景图；且该 key 实测 `401`。仓库里已有的自动出图链路是 `projects/jimeng_web_bridge`（图片走官方 dreamina CLI），但它按自身设计**必须由用户在本地网页点确认**（花积分 + 平台条款风险），Claude 与脚本都不能代点

## Follow-up 015 续 — 2026-09-17（出图自动化：gpt-image-1 / medium）

Auto-updated:
- tools/image_fetch.py — **新增**。OpenAI `gpt-image-1` 适配器，按用户定的次序出图：
  `-1 正面` 走 `images/generations`（纯文字），`-2 侧面` / `-3 背面` 走 `images/edits`、
  把 `-1` 放进参考槽**只换机位**。物件三视图 1024×1024、场景图 1536×1024，`quality=medium`（用户定）。
  `--object all` 跑全清单、`--scene bgN-M` 出场景图、`--dry-run` 不花钱先看 prompt、
  已存在默认跳过（`--force` 覆盖）。429/5xx 退避重试。多部件表单从 `hyper3d_fetch` import，一个出处
- tools/gen_object_cards.py — 出图次序按用户定的改：**`-1` 就是正面（那张参考）**，
  `-2 侧面` / `-3 背面` 挂着它出；四分之三锚点不再默认出（它只对人眼验收有用、对重建没用，省一张）
- props/p12…p27 — 16 张卡按新次序重出

修正一条我先前说错的话:
- **ElevenLabs 那个 key 是有效的**。401 的正文是 `missing the permission voices_read` / `user_read`
  ——是**权限范围受限**，不是 key 失效。我先前写「实测 401 ＝ 过期或撤销」是错的，已改。
  （它仍然不能出图：ElevenLabs 没有图像生成接口。它的用处是台词配音层，需要补 `voices_read` + `text_to_speech` 权限）

修掉一个被实际触发的坑:
- **旧媒体被 git hook 拉回来了**。follow-up 014 删掉的 589 个文件里，有 11 个在我后来几次
  `git checkout -- <路径>` 之后被 `post-checkout` 钩子从 R2 重新下载回来——**因为 `assets.json`
  还列着它们**（这正是 014 changelog 里记的那条风险，现在真的发生了）。危害不止是碍眼：
  `look_bianjing.py` 的调色板取样自 `bg*-1.png`，旧图在盘上就会让重建悄悄捡回旧画风。
  已处理：重新删除 + **直接剪掉 manifest 里 674 条盘上已不存在的 sk1 条目**（索引侧操作，
  等价于 `push --prune-missing`，不需要 boto3、不动 R2 里的对象）。sk1 在 manifest 里
  现在只剩 312 张 `ref/` 史料参考图（它们是有意保留的输入）。

阻塞:
- **缺 `OPENAI_API_KEY`**。`gpt-image-1` 要 OpenAI 的 key（`sk-…` / `sk-proj-…`），
  ElevenLabs 的 `sk_…` 不是同一个东西、也调不了 OpenAI。适配器与卡都已就位、`--dry-run` 走通，
  key 一到就能跑 `python tools/image_fetch.py --object all`

## Follow-up 015 续 2 — 2026-09-17（出图走 ElevenLabs Flows；两处我说错了，已更正）

更正（两条，都是我错）:
1. **ElevenLabs 有图像生成。** 实测 `https://api.elevenlabs.io/openapi.json`：`/v1/flows/image`
   是一个**多厂商**图像入口，`model_id` 判别式支持 `gpt-image-1 / gpt-image-1.5 / gpt-image-2`、
   `gemini-2.5-flash-image / gemini-3-pro-image / gemini-3.1-flash-image / -flash-lite`、
   `bytedance-seedream-5-lite / bytedance-seedream-5-pro`。用户说网页端能选 GPT Image 2 是对的，
   我先前「ElevenLabs 是纯语音 API、没有图像接口」的判断是错的。**一个 key 同时覆盖出图与配音，
   不需要另外的 OpenAI key。**
2. **挡住出图的不是 key 权限，是套餐。** 三次实测把两件事分开了：
   - `POST /v1/flows/image` 空体 → **422 参数错**（说明**有权限**，只是 body 没写对）
   - `POST /v1/flows/image` 合法体 → **402 `paid_plan_required`：requires a Pro plan or above**
   - `GET /v1/voices`、`GET /v1/user` → 401，点名缺 `voices_read` / `user_read`
   所以：**创建图像这一项当前 key 就有权限，缺的是账号套餐（要 Pro 及以上）**；缺权限的是那几个「读」接口。

Auto-updated:
- tools/image_fetch.py — 由「直连 OpenAI」改写为 **ElevenLabs Flows** 适配器：
  `POST /v1/flows/image`（`model_id` 默认 `gpt-image-2`、`quality=medium`（用户定）、
  物件三视图 `1:1 / 1K`、场景图 `16:9 / 2K`）→ 轮询 `GET /v1/flows/image/{id}` → 下 `content_url`。
  侧/背两张按 **`{"type":"generation","generation_id":…}`** 引用正面那次生成（省一次上传，
  且引用的是模型自己的产物、比重传字节更稳），正面若来自上一轮则退回 `inline_base64`。
  401 / 402 分别给出「权限不够」「套餐不够」的可执行提示

Seedance key 验证（用户 2026-09-17 给的 `ak_…` / `sk_…`）:
- **不是可灵**：按可灵的 ak/sk + JWT(HS256, iss=ak) 签名打 `api.klingai.com` 与 `api-singapore.klingai.com`
  → `401 code 1002 access key not found`（签名格式对、账号不存在）
- **不是火山引擎 Ark**：`Bearer` 打 `ark.cn-beijing.volces.com/api/v3/models` → `401 API key format is incorrect`
- **到此为止没有继续试**：搜到的 `seedanceapi.org` / `seedance25free.com` / `seedances.app` 等都是
  第三方聚合站，**把用户的 secret 逐个投给来路不明的域名本身就是泄露**。需要用户说明这对 key 是哪个
  控制台签发的，再对着那一个域名验

## Follow-up 016 — 2026-09-17
Source: user_input/follow_ups/202609.md - section 016
Summary: 物件扩到 33 个并真正进入场景 blend（新增布点层，1658 实例）；Kling 整条退出；即梦 key 验签通过但不能出任意图。

Auto-updated:
- 2_世界观人设/object_inventory.toml — 第二批 17 个物件（p28–p44）：席棚小摊 / 蒸笼灶 / 瓦子看棚 / 黑漆大案与藤墩 /
  茶床与建盏 / 书摊 / 药铺柜台 / 纸扎楼阁 / 青布幌 / 石门枕 / 过壕木桥 / 骨朵 / 空竹筐与芦席卷 / 粮袋堆 /
  拴马石与马槽 / 御沟荷与砖石沿 / 长条木凳。**合计 33 个**，卡与 `object.toml` 由生成器重出
- scenes/bianjing/_blender/city_plan.md — **新增 §12「物件布点（scatter）」**。这是「物件清单」与「场景 blend」
  之间那根一直缺的线：此前卡建好了、白模就算出来也进不了画面，因为没有任何一处告诉 builder 摆在哪。
  按**线**撒（沿 W11 已有的河 / 街折线，给间距 + 横向偏移带 + 抖动），坐标一个都不新写
- tools/build_bianjing.py — 新增 `load_scatter` / `scatter_line` / `place_object` / `build_scatter`，
  接在 `build_global_layer` 末尾。三道剔除：走廊外 → Place 足迹内 → keep-out 内（`in_water` 的反过来只撒在河里）。
  白模缺席时 `resolve_asset` 自动降级成同尺寸替身盒，**所以场景与镜头现在就跑得通**，白模到货逐个替换
- tools/build_bianjing.py — `World` 分出 `keepout_street`：街面 keep-out 挡的是**房子**，
  而行道柳 / 杈子 / 摊子 / 车驴本来就该站在街上。`on_street = true` 的条目摘掉这一层
- bianjing.blend — 重建：**1658 个物件实例**（沿汴河老柳 260 / 御街行道柳 120 / 御街朱漆杈子 713 /
  汴河漕船 40 / 席棚小摊 180 / 市摊大伞 110 / 独轮串车 60 / 驮货毛驴 45 / 沿街竖立招 130）
- CLAUDE.md + .claude/agent_refs/** + tools/** — **Kling 整条退出**：删除 `tools/kling_autopilot/`
  与已完成使命的一次性迁移脚本 `tools/genericize_perf_prompts.py`；「每镜双 prompt（Kling + Seedance）」
  契约改为只出 Seedance；10 s 切分口径、厂商枚举、代码里的 `### Kling 版` 分支共 46+ 处规范性提法清除。
  **dated amendment 块里的历史记录保留**——那是「当时发生了什么」的记录，不是指令
- tools/jimeng_fetch.py — **新增**。即梦 OpenAPI 的签名与调用（`X-Agent-*` + HMAC-SHA256 + Base64URL 无 padding）

实测（不是推断）:
- **即梦 key 验签通过**：用不存在的 run_id 打 `/agent_openapi/v1/novel/query` → `code 20001 task not found`。
  这一条排除了 `10002 AK 不存在` / `10006 签名校验失败` / `10007 权限不足`——**签名算法与账号都是对的**
- **但它出不了三视图**：该 API 只有两个能力——`pippit_novel_agent`（短剧：剧本解析 → 角色 / 场景生成 →
  分镜设计 → 分镜短片 → 成片合成）与 `pippit_avatar_marketing_agent`（营销视频）。`character_generate` /
  `scene_generate` 看着像出图，但它们**绑在一条由 `script_analysis` 上传剧本文件建起的 thread 上**，
  产出什么由 Agent 自己定，**给不了「这个物件的正视图」这种任意 prompt**。且文档写明「目前仅供超级会员限时可用」
- **ElevenLabs 出图仍被套餐挡住**：合法 body 的 `POST /v1/flows/image` → `402 paid_plan_required`

阻塞（两条自动出图的路都不通）:
- ElevenLabs `/v1/flows/image`（gpt-image-2 / seedream-5-pro / gemini-3-pro）：key 有权限，**账号要 Pro 及以上**
- 即梦 OpenAPI：key 有权限，**但没有任意文生图接口**
→ 33 个物件的三视图暂时出不了；`image_fetch.py --object all` 与下游 Hyper3D 链路已就位，解锁即可跑

## Follow-up 015 — 2026-09-17 13:20:00
Source: user_input/follow_ups/202609.md - section 015
Summary: props 全表批量出三视图 + Hyper3D 白模，模型回交用户。

Auto-updated:
- （执行型，产物落在 props/pN_*/ 下：三视图 png + whitemodel/pN_*.blend；进展与失败项在本条下方续记）

## Follow-up 018 — 2026-09-17 14:40:00
Source: user_input/follow_ups/202609.md - section 018
Summary: 三视图 prompt 补上「这一面该看到多大」，33 张物件卡重生成，旧图与旧白模全删重跑。

Auto-updated:
- tools/gen_object_cards.py — `VIEWS` 带上可见轴索引；新增 `_shape()` / `_depth()`；每张 prompt 多一行 `画面尺寸:`
- ai_videos/shikong_lvxing/sk1/2_世界观人设/props/p1[2-9]_*, p[2-4][0-9]_* — 33 张卡重生成（99 段 prompt）
- specs/ai_video/sk1/user_input/revised_prompt.md — 按 raw + follow_ups 重拼

Deleted (regen 前清场，follow-up 018 根因是旧图本身有缺陷):
- props/p12–p44 下 52 张 `pNN-N.png`
- props/p12–p18 下 32 个 `whitemodel/{raw.glb, *.blend}` 派生产物

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/, scenes/, characters/

## Follow-up 018（续）— 2026-09-17 22:50:00
Source: user_input/follow_ups/202609.md - section 018（同一轮实测里连带发现的三件事）
Summary: 三视图指令提到高权重位置；Rodin 对细长物件系统性压方 → 长径比 ≥6 走替身盒；物件布点从 8/33 补到 30/33。

Auto-updated:
- tools/gen_object_cards.py — `视图:` 行提到路由键正下方，按「哪一面正对镜头 / 哪个方向完全看不见 / 外轮廓因此长什么样」写；另外两个视图进负向词
- tools/build_objects.py — 新增 `SKIP_ASPECT = 6.0` 长径比分流；闸门改 `--fit stretch`；`detect_orientation` 加 `SWITCH_MARGIN`（近立方物件不乱转）；白模落盘自动出 peek
- tools/whitemodel_normalize.py — stretch 模式下新增「来源比例漂移」warning + `--aspect-tol`
- tools/mesh_peek.py — 新增：白模三张灰模快照（rule 4h §G 的那一眼）
- tools/hyper3d_fetch.py — HTTP 调用加指数退避重试（4xx/5xx 仍直接判死）
- tools/build_bianjing.py — scatter 新增 `along.kind = "place"` + `in_place`（连同 Place 足迹内的全城层 keep-out 一起摘）；布点落空时记拒绝原因
- ai_videos/.../scenes/bianjing/_blender/city_plan.md — §12 追加 22 条布点；闸门与过壕木桥退出布点（Place B 方块表已建）

实测数据（都进了代码注释，不是口头结论）:
- p12 漕船声明 4:1，三视图正确，Rodin 出 1.25:1；等比缩放偏差 236.9%，逐轴拉伸把斜桅杆抻成长刺
- p14 油纸伞 2.4×2.4×2.6 近立方，包围盒不含朝向信息，旧的 detect_orientation 把伞放倒了
- Place 内布点原为 0–5 个（书市 60→5、瓦子看棚 0），原因是挖洞前建的 keep-out 没跟着撤
- 布点实例 1495 → 2522；30/33 物件有落点

No conflicts found in: 1_立项/, 3_大纲/, 4_剧本/, 5_6_分镜与prompt/

## Follow-up 018（续 2）— 2026-09-17 23:10:00
Source: user_input/follow_ups/202609.md - section 018
Summary: 把「三视图塌成一个轴」做成机检，并挂成 Rodin 调用前的闸门。

Auto-updated:
- tools/view_check.py — 新增。抠主体剪影 + 腐蚀掉细附件后的核心宽高比 + 两张裁切图的相关度，
  三个信号合判「这两张图是不是同一个轴」。阈值 DIFF=1.8 由四个实测例定（见文件抬头）
- tools/build_objects.py — 三视图齐了先过 view_check，塌陷就不送 Rodin（状态 `views-collapsed`），
  省一次调用、也挡住一个注定对不上的网格；另外去掉了 `seen` 里对 "done" 的缓存
  （状态每轮从盘上重推，CLAUDE.md §State surfaces 第 1 条）

为什么需要它（这个缺陷今晚出现三次，全靠人眼）:
- p22 素木床榻 —— 用户报的
- p12 漕船 —— 我改完 prompt 自己抽查才发现
- p27 挑担货筐 —— 机检自己抓到的，确认属实（「正面」是扁担的侧视图）
机检的边界也写明白了：声明宽高比差不到 1.8 倍的两个面，本工具不声称能分辨
（p25 插柳暖轿差 1.6 倍，腐蚀后核心 0.68 vs 0.80 仍分不开——而它其实是对的）。

No conflicts found in: specs 其余部分

## Follow-up 016 — 2026-09-18 09:05:00
Source: user_input/follow_ups/202609.md - section 016
Summary: scene 走物件流水线自下而上装配；先 p46–p60 建筑构件/立面，再以 ≤20 白模原型 + 程序化微调铺满 scene。

Auto-updated:
- （执行中，进展续记于本条下方）

## Follow-up 018（收尾）— 2026-09-18 08:40:00
Source: user_input/follow_ups/202609.md - section 018
Summary: props 全部跑完 —— 25 个白模 / 8 个替身盒；新增俯视与四分之三两档视图集；新增漂移硬闸门。

最终状态（p12–p44 共 33 个物件）:
- 三视图 99/99 出完，机检 `view_check` 33/33 无塌陷
- 白模 25 个，替身盒 8 个（长径比 12.5–36 的平板/线性件 + 漂移超限的 2 个）
- 城市 blend：2110 / 2522 个实例是真网格（10.55M 面），替身盒 412

本轮新增的三条机制（都由实测卡出阈值，不是拍的）:
1. **第三视图可换俯视**（`view3 = "俯视"`）—— 背面与正面同轴、对重建不贡献新方向；
   而「没人会去拍的窄面」模型无论如何不画。实测：p18 4.629/4.8、p27 0.278/0.25、
   p42 2.687/2.8、p22 通过，四个全部奏效。
2. **第二视图可换四分之三**（`view2 = "四分之三"`）—— 又宽又薄的物件换俯视后第三张对了、
   第二张仍塌（p18 杈子窄端 0.5 m）。四分之三一张给全三个轴，是模型最愿意画的角度。
   实测 p18/p27/p42 换后全过（p42 画面相似度掉到 0.60，确实转了）。
3. **漂移硬闸门 `DRIFT_MAX = 2.0`** —— 超了就退回替身盒。阈值由实测卡出：
   p37 石门枕 1.47 形态对、p21 辘轳 1.43 对；p44 长条木凳 2.84 出来是带尖刺的框、
   p22 素木床榻 3.37 是带枕头疙瘩的板且四条腿没了。坏网格连体量轮廓都不保，不如替身盒。

Auto-updated:
- tools/gen_object_cards.py — VIEW3_TOP / VIEW2_ISO 两档；ISO_SCENE / ISO_NEG；逐视图措辞按视角分支
- tools/view_check.py — AXES_TOP（俯视量的轴不同）
- tools/build_objects.py — DRIFT_MAX 闸门
- tools/hyper3d_fetch.py — JSON 调用与下载改走 curl（urllib 反复抛 SSL UNEXPECTED_EOF，p42 连挂两轮；curl 一次过）
- CLAUDE.md — 新增「删除产物不必请示」一节（用户 2026-09-18 定）
- object_inventory.toml — p18/p27/p42 标 view2+view3，p22 标 view3；新增 p45–p60 建筑原型（scene 阶段用，用户改由另一 session 负责，本轮只跑了 p45）

No conflicts found in: scenes/（用户在另一 session 处理，本轮未动）
