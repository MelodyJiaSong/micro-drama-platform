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
