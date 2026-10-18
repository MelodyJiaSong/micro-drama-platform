# 变更

## 建剧 — 2026-10-18

Source: user_input/raw_prompt.md
Summary: 新建剧 dota_yingxiong；第一项工作为 DotA 1 地图、英雄、物品体系 Research（0_research/）。

未调用收费服务。

## Research 第一轮 — 2026-10-18

Source: user_input/raw_prompt.md
Summary: DotA 1 地图、英雄、物品体系 Research 完成（八路并行 + 合成）。

Auto-updated:
- ai_videos/dota_yingxiong/0_research/parts/d01–d08 — 版本与地图、六格英雄（21/18/20/16/17/20 = 112）、物品 131 件
- ai_videos/dota_yingxiong/0_research/dossier.md — 总览、对账、对 demo 的结论、待用户决定、112 人索引
- ai_videos/dota_yingxiong/README.md — 当前状态

判断：版本锚点由派单预设的「6.88 系列」更正为 6.83d（2015-06-09，IceFrog 最后正式版；6.84+ 为 Dota 2 补丁号，魔兽 6.85k/6.88 为非官方改图）。
未调用收费服务。子任务用 curl 下载了存档地图与网页、pip 安装 mpyq 解包地图（偏离派单「只用 WebSearch/WebFetch」，产物在会话 scratchpad，未入仓库）。

## Follow-up 001 — 2026-10-18 09:40:00

Source: user_input/follow_ups/202610.md - section 001
Summary: 真人电影质感；片种短视频（无连续剧情）；先备齐全部资产。

Auto-updated:
- ai_videos/dota_yingxiong/workflow.json — `format: short`，prompt 风格与负面词（真人奇幻电影）
- ai_videos/dota_yingxiong/2_世界观人设/world_rules.md — 真人化改编准则（新建；含出图不写血腥词）
- ai_videos/dota_yingxiong/2_世界观人设/assets_index.md — 编号总表与出图状态（新建）
- characters/ 173 张卡（英雄 c1–c112、m1–m26、召唤物 m100–m213 中 35 个）、background/ bg1–bg14 + registry、props/ p1–p28 + registry（14 路并行子任务写卡，派单存 `.audit/adhoc_agents/2026-10-18/dota-assets/`）
- 出图 209 张（ElevenLabs：人物与道具 `gpt-image-2`，背景 `gpt-image-2.5-sunburst`），请求日志在 characters / background / props 的 request_log.md；逐张看图，结论写入各卡「生成记录」
- README.md、0_research/dossier.md — 当前状态与已定事项

判断：c19、c27、c37、c93、c105、m200 外观依据不足（地图导入模型或骑乘未定），暂缓出图待截图。c68、m162 被 ElevenLabs moderated（未扣费），改写 prompt 后通过；bg10 目录名去掉专名 Roshan（`bg10_巨兽巢穴`）。
未调用视频服务；建立视频与三视图待用户决定。

No conflicts found in: 0_research/parts/

## Follow-up 002 — 2026-10-18 13:10:00

Source: user_input/follow_ups/202610.md - section 002
Summary: 首个 demo 斧王；两方场地与兵线设计；Vision 起草；收集全部角色原台词。

Auto-updated:
- README.md — Vision 与核心（按用户方向起草措辞，待用户确认）、体验表
- workflow.json — `episode_seconds: [60, 120]`
- 2_世界观人设/battlefield.md（新建）— 两方识别、兵线编成与身高、交战与受击、超级兵、三块场地与推荐、缺的视角图
- background bg1 / bg4 / bg5 `planning/blocks.toml`（新建，含 floorplan 渲染）
- characters/m2 — 长袍改本色亚麻 + 苔绿、光弹改银白带青绿（与 m5 拉开），立绘重出（ElevenLabs，日志 characters/request_log.md）
- 0_research/parts/d09–d14（新建）— 112 名英雄的 WC3 语音组全部台词（英文原句、意译、wiki 音频文件名与链接、出处）；未下载音频
- characters/c1–c112 —「配音参考」改用最出名的原句（含专名），turntable 声音句同步；c46、c68 顺手修正不一致的注释 / 声线描述
- episodes/ep01/story.json、decisions/story.md（新建）— 斧王 demo 故事第一稿；交稿前自检齐全

判断：首个英雄选斧王（四技能都打在小兵身上）；兵线按 6.83d 开局一波 3 近战 + 1 远程；Vision 与 battlefield.md 都是待用户确认的草稿。
台词收集更正 Research：术士用兽人萨满语音组（不是先知）；幽鬼有倒放的人声（不是无台词）。
未调用视频服务。

No conflicts found in: 0_research/parts/d01–d08
- 追记：episodes/ep01 故事经两轮独立冷读（`.audit/adhoc_agents/2026-10-18/dota-ep01-story/`）改到第三稿，待用户确定与打评分卡。

## Follow-up 003 — 2026-10-18 16:20:00

Source: user_input/follow_ups/202610.md - section 003
Summary: 技能做成可复用一致的资产；Vision 简化；EP1 改为无剧情技能展示；下载原声作参考并试做自有声音。

Auto-updated:
- README.md — Vision 改为「宏大绚丽的战场 / 更真实立体的英雄 / 更绚丽的技能」，核心改为「同一个技能在哪一段都是同一个样子」（代理起草，待用户确认）
- 2_世界观人设/skills/（新建）— README（本剧技能资产约定：一技能一卡、键 k{英雄号}{槽}、锁定动作 / 特效 / 作用结果 / 声音、Shot prompt 技能段、峰值图、样片）；斧王 k651–k654 四张卡与峰值图（ElevenLabs，日志 skills/request_log.md；k654 第一张斧头画成双刃，重出后通过）
- characters/c65 —「技能画面」指向技能卡；新增「自有声音（试验）」节
- episodes/ep01/story.json、decisions/story.md — 第四稿：亮相 + 四个可单独复用的技能模块，不再有因果链；交稿前自检齐全
- tools/voice_design.py（新建）— ElevenLabs 声音设计 / 保存 / 台词合成，经 RequestLog；只用文字描述，不上传原声
- .agents/references/project/paid_services.md — 商用表加「ElevenLabs 声音设计：不明确」；ElevenLabs 节登记新入口
- characters/*/ref/audio/original/ — 原版语音组音频下载完成：89 名英雄、1732 个文件、166.5 MB（49 个 404 均为无人声生物音效）；每个英雄目录有 refs.md（含版权说明）与 voice_profile.json 声学测量；本机 pip 安装 librosa 0.11.0（附带 soundfile、scipy）
- characters/c65_Axe/voice/design_01、design_02 — 6 个候选声音（试验），待用户试听

判断：技能资产先在本剧落地（跨剧推广由用户定）；Prompt 编译接入技能卡待做。Voice Design 商用条款不明确，产出只作试验。
未调用视频服务。

## Follow-up 004 — 2026-10-18 18:30:00

Source: user_input/follow_ups/202610.md - section 004
Summary: 其余 111 名英雄批量建技能卡与峰值图。

Auto-updated:
- 2_世界观人设/skills/ — 12 路并行写卡（派单 `.audit/adhoc_agents/2026-10-18/dota-skills/brief_skills.md`），共 449 张新卡（祈求者 4 + 10、大地之灵另有残岩 k21a）；各英雄卡「技能画面」下插入指向技能卡的提示
- 峰值图：并发 8 个进程、每请求内嵌 5 张全尺寸参考图时大量网络失败（curl 55 / 35 / 56、HTTP 100），全部停掉；改为单进程顺序生成，参考图缩到长边 1024 JPEG；已提交未下载的 18 个任务按日志 generation id 收回，不重提（日志 skills/request_log.md）
- 暂缓：施法者立绘未出的 c19、c27、c37、c93、c105 及 k932（需 m200）

判断：技能尺度统一按 1 游戏单位 ≈ 1 cm 换算，多处小于人物卡概要（以技能卡为准，是否整体放大由用户定）；含血字的人物卡概要未回改。
未调用视频服务。

## 2026-10-18 — follow-up 005

- 流浪剑客战吼原句 "Ash nazg gimbatul!" 按用户意见保留（`skills/k83_Warcry` 台词行注明）。
- 导出 EP1 第四稿可读版供用户查看；技能尺度是否整体放大待用户定。

## 2026-10-18 — follow-up 006 / 007

- 斧王声音选定 `design_01/preview_1`，存为 `dota-axe-01`；EP1 三句台词已合成到 `c65_Axe/voice/lines/`（试验）。
- Vision 用户确认。EP1 第四稿待用户 review。
- 技能尺度改为 1 单位 ≈ 2 cm（`skills/README.md`「尺度换算」）；全部技能卡重写尺度，旧尺度峰值图作废待重出。EP1 怒吼热浪改为约六米。
- c5–c9 按用户立绘反馈重研外观，立绘待重出。

## 2026-10-18 — follow-up 007 / 008（立绘反馈）

- c5–c9 按 WC3 原模型重研（参考图在各卡 `ref/model/`，只作人眼参考）：c5 牛头人加壮、方截面红纹图腾；c6 改黑狼头兜帽、赤膊黄褐皮、灰白毛皮护具、银斧；c7 改粗犷海盗船长、后弯弯刀；c8 模型确为蓝色恶魔卫士，外观改为全罩金冠脊头盔、赤膊钴蓝上身、背刺、波浪刃大剑；c9 改直立熊猫人（斗笠、黑长褂、长棍、酒桶、酒坛）。`d02` §5–§9 追加更正。立绘重出中，旧图存 `_v1.png`。
- c14 加壮；c18、c24 加粗上肢，c24 双刃放大。三张已重出、看图通过。
- 技能尺度 ×2 收尾：`skills/README.md` 补位移、弹道直径、贴地雾高度、贴身不放大四条口径；旧尺度峰值图 86 张改名 `*_peak_v1.png`，全部待按新尺度重出。

## 2026-10-18 — follow-up 009 / 010

- m102–m104 熊猫分身按 WC3 原版重研并重出立绘（土：褐袍巨石；风：宝蓝袍斗笠电光；火：红袍火焰纹双火刀）。
- 技能卡从 `2_世界观人设/skills/` 挪到各英雄目录 `characters/{英雄}/skills/`（459 个），全剧路径同步；`skills/` 只留约定与搬家前的请求日志。
- 新增 `tools/skill_pack.py`：技能卡「技能视频 prompt」→ `资料包/`（格式同镜头资料包）→ Dreamina 草稿 / 正式条；`paid_services.md` 入口与 `skills/README.md` 已写。
- 斧王样板：4 张卡加技能视频 prompt（bg5 场景、树人 / 德鲁伊为目标并倒下、食尸鬼为友军、斧王自有声音参考 `voice/c65_Axe_audio.mp3`）；新尺度峰值图 4 张；用户要求出片后提交 4 条 480p 草稿（120 + 120 + 96 + 120 积分），初接成 `episodes/ep01/edit/draft/ep01_draft_v1.mp4`（38.2 秒，`cut_v1.json`）。听写只认出 "Pitiful!"（位置偏早），"In Mannoroth's name!" 未认出，待用户听。
