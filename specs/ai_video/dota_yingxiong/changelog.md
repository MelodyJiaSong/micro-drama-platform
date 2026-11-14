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

## 2026-10-18 — follow-up 011

- 斧王建立视频 `characters/c65_Axe/c65_Axe_turntable.mp4`（4 s，720×1280，Dreamina 48551e26），正→侧→背转身，与立绘一致。
- DotA 1 技能图标：PlayDotA 2013 存档的 4 个 64×64 原版图标存进各技能目录 `icon/`（`refs.md` 记来源，版权素材只在剪辑时叠加）。
- 初接 v2 `episodes/ep01/edit/draft/ep01_draft_v2.mp4`（38.2 s，`cut_v2.json`）：施法时段在左上角叠技能图标，时段按草稿逐 0.5 s 看定。技能视频正式条（720p）待用户看过草稿后出。

## 2026-10-18 — follow-up 012–014

- 斧王 4 张技能卡按用户样片意见改锁定的动作 / 特效 / 作用结果 / Shot prompt / 峰值图 / 视频 prompt：k651 暗红霸气 + 红色魔法束缚拖拽（只要树人）；k652 头顶燃烧火焰鬼脸（原版 `SoulBurnbuff` ⚠️）、逃 6–8 秒才倒；k653 随机瞬发、每秒三四圈、残影；k654 助跑蓄力起跳、空中反弓、力劈华山、目标原地火焰爆炸。英雄卡「技能画面」同步。
- 峰值图重出（旧版存 `_peak_v2.png`）；4 条 480p 草稿重出（120 + 144 + 120 + 120 积分）。
- 人物视频本剧特殊安排（README）：16:9、8 s、口型同步、挂自有声音 `ref/audio/c65_Axe_own_voice.mp3`；c65 已重出（Dreamina 949c340b），嘴有张合、台词识别为 "Tremble before me"；画面裁到大腿、斧横端，未全身入画。
- 初接 v3 `episodes/ep01/edit/draft/ep01_draft_v3.mp4`（50.3 s，1280×720，`cut_v3.json`）：开场人物视频 + 4 技能 + 左上角图标；k651 草稿未吼出原句，剪辑时叠自有声音 "In Mannoroth's name!" 并压低原片人声。

## 2026-10-18 — follow-up 015–019

- k653：光尾调暗、由亮到透明渐变、不闭合；一秒五六圈；残影写成同一人五六个由实到淡的叠影（峰值图第四版通过）；三个树人各自独立出手（018）。草稿：光已不染红、有运动模糊、树人错开，但光尾仍闭合成整圈、每次约 1 秒。
- k651：开头树人四散外逃，吼后被束缚拖回（017）。草稿：拖回与收尾对，外逃不明显；原句仍未吼出，剪辑叠自有声音。
- 技能视频统一留约 1 秒干净收尾（017，`skills/README.md`）。
- k654：只要树人、起跳劈下一气呵成不停留（019）。草稿：只有树人，跳劈比上一版快，空中仍有约 1 秒；"Pitiful!" 约 8 s。
- 人物视频改全景全身入画（016）：c65 重出，全身、斧拄地、嘴型明显。
- 初接 v4 `episodes/ep01/edit/draft/ep01_draft_v4.mp4`（50.3 s，`cut_v4.json`）。

## 2026-10-18 — follow-up 020–024

- 020 重新生成；021 k653 改为混战中被动随机触发（斧王主动对砍）；022 k654 因果先后（劈开与爆炸只在斧刃接触时，峰值图改画接触瞬间）；023 5 个视频收尾 ≥2 s（技能各 +1 s，人物视频 10 s）；024 k654 爆炸加大（约 6 m 蘑菇火团、贴地冲击波、持续 1.5 s）。
- 本轮草稿：k651 132、k652 156、k653 132、k654 132 积分；人物视频 c65 重出（10 s，全身，末 2 s 定住）。中间三条按旧 prompt 的重出（f1632dab / 2b5a30cb / f3ddc0dd，360 积分）被新意见覆盖、未用。
- 初接 v5 `episodes/ep01/edit/draft/ep01_draft_v5.mp4`（56.3 s，`cut_v5.json`），各条整段接入保留收尾；k651 原句仍未吼出（识别为 "And BOOM!"），剪辑叠自有声音。
- 全英雄峰值图批量续跑因网络（curl 55/35）大量失败，已停（成功 85 张），待目录调整（follow-up 025）后续跑。

## 2026-10-18 — follow-up 025 搬迁结果

- 代码先支持一层分组目录（ai_video_management follow-up 284），测试通过后搬迁。
- 人物 173 张：近卫_sentinel 83、天灾_scourge 70、中立_neutral 20（英雄按首行阵营；m1–m3 近卫、m4–m6 天灾；召唤物 / 变形产物跟召唤者；野怪与 Roshan 中立；无拿不准的卡）。背景 14 个：近卫 4、天灾 4、中立 6（river 四个 + bg11、bg12 公共商店），去掉 `dota_map/` 层，`background/registry.toml` 的 `zone` 改为阵营目录、删 `continent`。道具 28 个全进 `props/中立_neutral/`，无阵营专属物件。
- 全剧 521 个 md/json/toml/txt 路径重写（技能卡参考行、人物卡、`assets_index.md`、`battlefield.md`、`world_rules.md`、EP1 story / decisions、`cut_v1–v5.json`（note 注明搬迁）、技能 `drafts/*/generation.json`、资料包 manifest；bg 平面图里指向 `battlefield.md` 的相对路径少一层）。`request_log.md` 与本 changelog 的旧路径保留。`assets_index.md` 顶部新增「目录结构」。
- 核对：旧路径残留 0；技能卡 459、人物卡 173 全部找得到；`skill_pack sync` 4 个资料包均 ok；`gen_char_images plan` 172 张（c65 没有立绘块，与 `char_assets status` 一致）、`--kind props` 28；`gen_turntable_videos --only c65 --dry-run` 正常；`shot_pack check --all`、`workflow_catalog --check` 通过。

## 2026-10-18 — follow-up 026

- 斧王 4 条技能 720p 正式条（`--stage final`，以 v5 草稿为运动参考 `@视频1`）：k651 286、k652 338、k653 286、k654 286 积分，存各技能 `renders/`。`tools/skill_pack.py` 加正式条：追加最新草稿（1280×720、24fps、去音轨）作参考视频，prompt 用 `shot_take.final_prompt` 的草稿用法句。
- k651 正式条吼出了原句（识别 "IN MADOR AXE NAAAARGH!"），不再叠配音；k654 "Pitiful!" 约 9 s。
- 正式版初接 `episodes/ep01/edit/final/ep01_final_v1.mp4`（56.3 s，720p，`cut_v1.json`）：开场人物视频 + 4 技能（保留收尾）+ 左上角技能图标。
- 管理应用 follow-up 285：图片扩展名测试与读取器对齐；工作流目录登记 `skill_pack.py`、`voice_design.py`、`asset_group.py`；后端 397 通过。

## 2026-10-18 — follow-up 027 / 028

- k651 改：树人朝左 / 右 / 深处三向逃；斧王全程双手握斧吼、不拄地。峰值图重出（gid FOb09ovFX8h54VsKPYaf，两次下载截断后按 gid 重下）；正式条直接出、不带草稿（`skill_pack.py --no-draft`，198 积分）；未吼出可辨原句，剪辑叠自有声音。
- 正式版 v2 `episodes/ep01/edit/final/ep01_final_v2.mp4`（`cut_v2.json`）。
- `tools/image_fetch.download` 先写 `.part`、能完整解码再改名（网络中断时 curl 会回 200 带半截图）。
- 管理应用 follow-up 286：人物详情页「样片与正片」review 区（正片 / 样片 / 剪辑拼接三个标签）；后端 406、前端 100 测试通过。

## 2026-10-18 — follow-up 029

- k651 改：树人以斧王为圆心向前 / 左后 / 右后辐射逃散；半径 6 m 红色爆圈（地面清楚边缘）；瞬发无前摇（删蓄力拍）；高俯拍。峰值图重出（gid iozy8tHB1UqiODr84xFT，通过）；正式条直接出（220 积分），吼出可辨的 "...his name!"，不叠配音。
- 正式版 v3 `episodes/ep01/edit/final/ep01_final_v3.mp4`（`cut_v3.json`）。

## 2026-10-18 — follow-up 030

- 斧王 EP1 正式版粗剪 `episodes/ep01/edit/final/ep01_final_v4.mp4`（53.1 s，720p，`cut_v4.json`）：人物视频 + 4 技能正式条，段间 0.8 s 压暗转场（落在上一段 2 s 收尾里）；每个技能入场中央标题卡（DotA 1 图标金框 + 中英文名 + 快捷键 Q / W / E·被动 / R·大招，PNG 存同目录 `title_card_k65N.png`）；施法时段左上角小图标；片尾 1 s 淡出。剪辑脚本在 scratchpad `axe_edit.py`（一次性，未进 tools/）。

## 2026-10-18 — follow-up 031

- 人物详情页剪辑拼接：正片剪辑排在草稿剪辑前（管理应用 follow-up 287）。
- c65 人物视频转身段（2.3–7.35 s）脚步声静音，台词与低笑保留；turntable prompt 加「原地转身无脚步声」与负面词。
- 正式版 v5 `episodes/ep01/edit/final/ep01_final_v5.mp4`（53.1 s，`cut_v5.json`）：标题卡改纯英文（Georgia 字体：技能英文名 + Active / Passive / Ultimate + 快捷键），用静音后的人物视频；英文卡 PNG `title_card_k65N_en.png`。

## 2026-10-18 — follow-up 032

- 宙斯 c40 立绘重出：下载 DotA 1 原版图（PlayDotA hero 18 动图、WC3 BTNAvatar 经典 / 重制版、普通形态山丘之王对照）到 `c40_Lord_of_Olympus/ref/model/`（`refs.md`）。原版是天神下凡形态：全身银灰石像 / 白银质感、冰蓝眼光、尖脊双弯角头盔、方头大锤；旧卡的「鎏金青铜皮肤、金色双辫长须、护鼻圆顶盔、单手战锤」是凭记忆套了普通形态的金胡子，全改。新立绘 sha `e87553d96fd9`（ElevenLabs gpt-image-2，gid vl9YT7Wl8A2IUlvl8EsS），通过；旧图删。
- 同步改：4 张技能卡的人物描述、`0_research/parts/d04` §1 外观。`k402_Lightning_Bolt_peak_v1.png` 是旧金色形象，待重出。
- 流程：`ai-videos-pipeline/resources/assets.md` 人物节加「改编自已有作品的人物先看原版图」。规模：112 张英雄卡只有 6 张有 `ref/model/`（c5–c9、c40），其余外观未经看图核对。

## 2026-10-18 — follow-up 033

- 宙斯 c40 再查原版：补下载天神下凡模型渲染图（YouTube 封面）、游戏内天神下凡与 DotA 1 宙斯画面、DotA 1 界面头像、WC3 穆拉丁截图等 8 张到 `ref/model/`（refs.md 记来源 / sha / 所见；`compare_avatar_crops.png` 为验收对照拼图）。
- 卡改：方墩体型（约 1.4 m、连肩甲宽约 1.1 m）；头盔粗短竖角 + 顶部尖脊 + 额箍菱形宝石；右手方块头大锤、左手月牙刃大斧（Battle.net 资料：战锤 + 手斧）；锤斧与脚下常驻蓝电光；倒三角尖楔胡须。battlefield.md 宙斯行同步。技能卡动作随武器改：弧形闪电从左手斧刃尖射出，大招锤斧齐砸。
- 立绘两轮：第一张（gid y0kgECYEF8tkGZcjbC2n）比例仍偏高、编辫、牛角，不过；加死比例 / 胡须 / 角形后第二张（gid Gu2oETNOFFZ8f2Dq5VqZ，sha ffbb8aa74d15）通过。`k402_Lightning_Bolt_peak_v1.png` 仍是旧金色形象，待重出。

## 2026-10-18 — follow-up 035（demo-under-character，搬迁结果）

- 本剧现阶段没有分集；斧王 demo 从 `episodes/ep01/` 整体搬到 `ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c65_Axe/demo/`，空的 `episodes/` 已删。
- 搬 30 个文件：`story.json`、`decisions/story.md`、`edit/draft/`（`cut_v1–v5.json`、`ep01_draft_v1–v5.mp4`）、`edit/final/`（`cut_v1–v4.json`、`ep01_final_v1–v6.mp4`、`title_card_k651–k654{,_en}.png`）；文件名与内容不变（cut 的 `clip` 原本就指向人物目录，核对全部存在；`output.file` 同目录）。ep01 下没有 `request_log.md`；之后 `demo/` 下的收费请求按 `tools/service_request.py` 归 `2_世界观人设/characters/request_log.md`
- `ai_videos/dota_yingxiong/README.md`：「当前」段的斧王 demo 位置改为人物目录 `demo/`；目录表 `episodes/` 行改为「每个英雄的 demo 在该英雄目录 `demo/`，现阶段没有分集、不建 `episodes/`」
- `ai_videos/dota_yingxiong/2_世界观人设/skills/README.md`：状态表成片路径与「拼成 demo 短片」一条改为英雄目录 `demo/edit/{draft,final}/`
- 管理应用 follow-up 288：人物详情页「样片与正片」的剪辑拼接改读人物目录 `demo/`

Validation: `skill_pack.py sync dota_yingxiong` 正常；`workflow_catalog.py --check` 通过；剧目录内 `episodes/ep01` 无残留（request_log 除外）；运行中后端斧王 review 接口列出草稿 v1–v5、正片 v1/v2/v3/v6。

## 2026-10-18 — 编号与剪辑记录修正

- follow_ups 撞号：另一会话的宙斯立绘占了 032 / 033；本会话的快捷键改为 **034**、demo 搬迁改为 **035**（节移到其后），本会话写过的引用已改。
- 剪辑脚本把正式版 v4–v6 的记录都写进了 `cut_v4.json`：拆成 `cut_v6.json`（原内容）与补建的 `cut_v4.json`、`cut_v5.json`（标「已被取代」）；脚本改为按版本号写 `cut_v{N}.json`。

## 2026-10-18 — follow-up 034 结果

- `0_research/parts/d15_技能名与快捷键.md` + `d15_abilities.json`：6.83d 地图（主据）+ PlayDotA 2013-12 / 2014-01 存档（旁证与图标）；459 张技能卡全部对上地图，455 张对上 PlayDotA（k772 / k272 / k273 / k362 存档是旧技能）。技能卡首行改「快捷键 X」，人物卡「技能画面」小标题改快捷键字母，另 89 处正文；451 个原版图标（PNG）下到各技能 `icon/`。主会话抽查 c5 / c24 / c72 / c110 与地图一致。
- 清理：峰值图取回时按旧（分阵营前）路径写出的 `characters/c100_*`、`c101_*`、`c14_*` 三个散目录——2 张与现有重复、4 张截断——已删；k1002、k1003、k1011、k141 峰值图待重出；脚本取回改为按技能目录名在新结构里找。

## 2026-10-18 — follow-up 034

- 宙斯 c40 五条 720p 正式条（直接出，无草稿，共 996 积分）：人物视频 `c40_Lord_of_Olympus_turntable.mp4`（16:9 · 10 s，200；首次下载 SSL 断开，`--harvest` 补收未重提）；k401 180、k402 180、k403 220、k404 216，存各技能 `renders/`。
- 提交前补：4 张峰值图按新立绘出（ElevenLabs gpt-image-2，gid 见各技能卡）；4 条「技能视频 prompt」（目标天灾食尸鬼、场地 bg4、大招替身骷髅王 c62）；人物视频块改 16:9 / 10 s；k404 台词改 "Spears, blood, booze and thunder!"。宙斯无自有声音参考（Voice Design 商用不明确，未用），声音由 prompt 描述。
- 验收：人物视频、k401、k402、k403 通过；k404 举起时左手大斧变成第二把锤、机位转到正面、台词漏 "blood"，待用户定是否重出。

## 2026-10-19 — follow-up 036

- `m4` 食尸鬼按 WC3 经典模型截图重写外观（`ref/model/refs.md`）；立绘重出：`m4_Ghoul.png`（gid `mkTwBvovwoF4KLdjARfE`，代理初审通过、待用户看图），备选 `m4_Ghoul_v2a.png`、旧图 `m4_Ghoul_v1.png` 待用户定后删。
- 同步改 `0_research/parts/d01` §4 食尸鬼外观、`battlefield.md` 超级兵 `m4-1` 描述。
- **未改**：约 70 张技能卡（多为近卫英雄）的技能视频 prompt 里内嵌了旧食尸鬼描述（「双手锈短刀」「短刀脱手」等），c40 四个技能资料包里的 `m4_Ghoul.png` 也是旧图；等用户确认新造型后再批量改、重跑 `skill_pack.py sync`。同模型的噬魂鬼 `c70` 卡写「无发」，也与原版不符，待核。

## 2026-10-19 — follow-up 037

- `m4_Ghoul_turntable.mp4`（9:16 · 4 s · 720p，72 积分，submit `ffc344c3`）：代理初审通过、待用户看片；侧面时爪尖出画左边缘（小偏差）。

## 2026-10-19 — follow-up 038

- 食尸鬼声音：原声 7 个入 `ref/audio/original/`（refs.md 记来源、sha、音高）；Voice Design 两组 6 版 preview（`voice/design_01` 说话、`design_02` 无词），待用户选。首条建立视频 `m4_Ghoul_turntable.mp4` 声音被退回（画面保留），待挂选定声音后重出。

## 2026-10-19 — follow-up 039

- 食尸鬼声音再加一组：本地 Stable Audio 3（`tools/local_audio.py`，不收费）出 6 类 × 2 种子 = 12 条 5 秒无词叫声，清单 `m4_Ghoul/voice/sa3_01/gen_v1.json`，每条旁有 `.json`（prompt、种子、sha、逐秒响度）。全部无静音、无削波；pyin 测音高多数 58–80 Hz（原版 55–60 Hz），`ghoul_attack_s421` 音高与质心（57.6 Hz / 1452 Hz）最接近原版。待用户在 038 的 6 版与这 12 条里挑。

## 2026-10-19 — follow-up 040

- Stable Audio 3 不用：039 的 12 条与 `voice/sa3_01/` 已删；模型与工具删除见 ai_video_management follow-up 291；`paid_services.md` 定本地模型只用完全开源的。食尸鬼声音候选只剩 038 的 6 版。

## 2026-10-20 — follow-up 041

- 食尸鬼叫声：本地 MOSS-SoundEffect-v2.0 出 12 条（`m4_Ghoul/voice/sfx_01/`，清单 `gen_v1.json`，每条旁有 `.json`）。无静音、无削波；中文提示词那组音高约 53 Hz，最接近原版 55–60 Hz；`ghoul_attack` 两条偏弱（一条整体约 −45 dB，一条第 1 秒几乎无声），`ghoul_feed` 是咀嚼声、无嗓音。待用户挑。

## 2026-10-20 — follow-up 042

- `m4_Ghoul_turntable.mp4` 重出（挂 MOSS 声音参考，submit `26f19dad`，旧条挪进 `_deleted/`）；用户说声音不对。
- 原声拼 4 秒 → 本地换音轨的内部样片 `m4_Ghoul/samples/m4_Ghoul_turntable_原声样片_不进成片.mp4`。
- 待处理：Windows Defender 2026-10-20 09:49 隔离了 `~/bin/dreamina.exe`（1.4.20），所有会话无法提交即梦任务，需用户在 Windows 安全中心还原并加排除。

## 2026-10-21 — follow-up 043

- 新工具 `tools/local_voice.py`（MOSS-VoiceGenerator 本地配音），登记 `paid_services.md` 商用用途表。
- `m4_Ghoul_turntable.mp4` 换成自有声音音轨（"Must feed!" + 啃食，全部本地 Apache-2.0 模型），可对外用；上一条挪进 `_deleted/`。
- Seedance submit `e2814ecd` 生成失败（回执 80 积分，退分未知）。`~/bin/dreamina.exe` 仍在 Defender 隔离区，待用户管理员还原。
- 已解决（2026-10-21 12:18）：用户经 UAC 授权，Defender 加单文件排除 `~/bin/dreamina.exe` 后从隔离区还原；`dreamina version` = 1.4.20（commit `ac44792a`），SHA256 `50E0E684…2F943774`，未签名；`multimodal2video -h` 确认 seedance2.5 收 480p。

- 编号更正：本会话的 039 / 040 与另一会话撞号（039 stable-audio、040 只用开源），改为 **042**（ghoul-voice-moss-then-original）、**043**（ghoul-own-voice-must-feed），卡与生成清单里的引用已改。

## 2026-10-21 — follow-up 044

- 用户决定：`m4` 台词声音可用原版语音作参考本地克隆、对外使用，用户自担风险；只限本地模型、只限 `m4`。`m4_Ghoul/ref/audio/original/refs.md` 改写对应规则；等用户下载 MOSS-TTS-Local-Transformer-v1.5 权重（清单 `.cache/models/moss_tts_local_v15_download_list.md`）。
- 2026-10-21：用户已在 Defender 还原 `~/bin/dreamina.exe`（1.4.20，`version` 能跑）；临时 1.4.5 副本已删。
- 2026-10-21：按用户要求删除 `~/bin/dreamina_1.4.5_backup.exe`，本机只留 1.4.20；`paid_services.md` 同步。
- 2026-10-21 follow-up 044 克隆：用户下载权重 sha256 核对通过；`tools/local_voice_clone.py` 改为自己读参考再编码（模型代码的 torchaudio.load 要 torchcodec，Windows 缺 FFmpeg 动态库）。`voice/clone_01` 共 21 条（参考 GhoulWhat4 18 条、参考另 3 句 3 条），语音识别加与 GhoulWhat4 的频谱比对，选 A `clone_what4_s808`、B `clone_what4_s802`、C `clone_what4_slow_s821`，各接 MOSS 啃食成 4 秒（`voice/final/clone3/`），发用户选。原版本身识别为 "MUST BE!"，克隆版识别成 "Must be it" 属同一含糊口音。
- 2026-10-21 follow-up 044：用户选 A。`m4_Ghoul_turntable.mp4` 换成克隆音轨（sha `1077be232693`），上一条挪进 `_deleted/`。食尸鬼 `m4` 资产：立绘、建立视频、声音齐；三视图未抽、技能卡里旧描述未改（见 follow-up 036 遗留）。

## 2026-10-21 — follow-up 045

- `k401_Arc_Lightning`：卡的施法动作、特效、作用结果、声音、Shot prompt、峰值图 prompt、技能视频 prompt 改为「斧刃只放一次电，之后电弧自己逐个跳」；目标换新造型 `m4` 食尸鬼。
- 峰值图重出 `k401_Arc_Lightning_peak.png`（sha `e5557c47d3d9`，gid `q7qLh1FTiQP5O7L6rxqf`）；旧图与落选候选在 `k401_Arc_Lightning/_deleted/`。`skill_pack.py sync dota_yingxiong k401` 已更新资料包。
- 旧技能视频 `renders/20261018-233512_4b22a9b0/` 标为用户退回，新视频待用户点。

## 2026-10-21 — follow-up 045

- 敌法师 `c24`：下载 20 张 DotA 1 / WC3 恶魔猎手原版图到 `ref/model/`（`refs.md` 记来源与看图结论）；按图重写人物卡外观（双刃握正中、重型体格、黑色纹身、后梳束发、护胫与靴）；立绘重出 `c24_Anti_Mage.png`（sha `ea4d4dcac4ca`），旧版改名 `c24_Anti_Mage_v2.png`。待用户确认。
- 未做：技能卡 k241–k244 外观描述与峰值图仍是旧形象，等新立绘确认后同步；建立视频未出（视频由用户点）。

## 2026-10-21 — follow-up 050（原记 047，与另一会话撞号改号）

- `m1` 树人按 WC3 经典模型（暴雪旧官网 classic.battle.net 动图 + 头像，`m1_Treant/ref/model/refs.md`）重写外观：瘦长木头脸（有嘴、琥珀黄眼）、鹿角状尖枝挂鲜绿叶团、暖棕光滑木身、三四根白木长爪、胯后短枝、腕踝老藤（队伍色改材质）。立绘重出：推荐 `m1_Treant.png`（gid `XM9wLNOMQ9vP8dxOGlPI`，代理初审通过、待用户看图），备选 `m1_Treant_v2a.png`、`m1_Treant_v2b.png`（后者是代理脚本失误多出的一张，同 v2a prompt），旧图 `m1_Treant_v1.png`，均待用户定后删。ElevenLabs 3 次出图，请求见 `characters/request_log.md`。
- 同步改 `battlefield.md`（超级树人 `m1-1`、与 `c1` 的区分、交战「近卫扫」）、`0_research/parts/d01` §4 树人外观。
- **未改**：5 张近卫技能卡（k121、k123、k124、k173、k192）的技能视频 prompt 内嵌了旧树人描述；约 230 张技能卡提到树人、资料包里的 `m1_Treant.png` 仍是旧图；斧王 demo 已出的片也是旧树人。等用户确认新造型后再批量改、重跑 `skill_pack.py sync`。建立视频（9:16 · 4 s，约 72 积分）与叫声未做，视频由用户点。
- 2026-10-21 用户点出片：`renders/20261021-204944_8a130d4d/k401_Arc_Lightning_clip.mp4`（720p · 10.05 s，submit `8a130d4d`，180 积分，sha `9019b47aa292`）。代理初审：新造型食尸鬼、依次电倒、收尾都对；**电弧仍每次从斧头重新射出，不是从目标自己跳**，开头 2 秒机位贴着铠甲。待用户看片定是否改 prompt 再出。
- 2026-10-21 k401 按用户同意改 prompt 再出（食尸鬼横排散开、离他 12–15 m，打中第一只后斧头收回，开场全景）：`renders/20261021-210359_3e26b624/`（submit `3e26b624`，180 积分）。代理初审仍不通过：约 3.9 s 又从斧头拉出一整条电弧穿过整排，距离看着五到八米。
- 2026-10-21 用户追加：技能二也重出，施法距离要远，小怪换成食尸鬼。`k402_Lightning_Bolt` 卡改为目标离他约 25 m、新造型 `m4`（骨爪无刀、低沉喉音），机位改背侧 24mm 纵深；峰值图重出（sha `337b1d8caedb`，gid `25XDgBhClr3pyGo95ZUn`，旧图与落选在 `_deleted/`）；720p 正式条 `renders/20261021-211330_1bc315a3/`（submit `1bc315a3`，180 积分），代理初审画面通过，距离看着约 15 m。

## 2026-10-21 — follow-up 046

- 新道具 `p29` 敌法师月刃（`props/近卫_sentinel/p29_Anti_Mage_Glaive/`），锚点图 sha `9f05506f68f0`。
- `c24` 立绘带参考重出（v3 定人 + p29 定武器）：当前 `c24_Anti_Mage.png` sha `8e8bf4d8dd7e`；第一条 `c24_Anti_Mage_v4.png`（弧太浅）、上一版 `c24_Anti_Mage_v3.png` 留档。待用户确认。
- 未做：技能卡 k241–k244 外观与峰值图仍是旧形象。
- 第二轮（用户退回：「是树人小兵不是英雄，相对接近的是 v1」，选「以 v1 为底微调」）：直译版 `v2a` / `v2b` / `v3` 作废待删；卡改回 v1 造型，只借原版叶色（鲜绿）、白木长爪、腕踝老藤三处；挂 v1 作参考图重出 `m1_Treant.png`（ElevenLabs，gid `6oOxfg4acYM8BHfK8wNa`），代理初审通过、待用户看图。本条共 4 次 ElevenLabs 出图。上面「未改」一段的技能卡同步照旧等新立绘确认。

## 2026-10-21 — follow-up 047

- `p29` 敌法师月刃按用户定的形制重写（外弧开锋、外弧正中断开装握把、轮廓完美月牙）；锚点图改 16:9 一对，当前 sha `1234c5d1c67f`，`_v1`（046 版）、`_v2`（外弧没断）留档。待用户确认；`c24` 立绘的武器描述还是 046 版，武器定了再改卡、出全身。
- 2026-10-21 用户：技能一四只食尸鬼不要并排，要前后有距离，闪电链在他们之间跳。k401 视频 prompt 改为四只前后错开、左右交替（约 12/17/22/27 m），电弧往纵深折跳；第三条 `renders/20261021-212535_f6297965/`（submit `f6297965`，180 积分）。代理初审：斧头只放一次、之后目标间逐个跳，基本做到；前后错开不明显、食尸鬼越凑越近，一瞬三只连成一串。待用户看片。

## 2026-10-21 — follow-up 048

- `p29` 敌法师月刃改半月牙并加细节（大马士革纹、回火色、嵌银新月盈亏、狼首咬握把、鲨鱼皮银丝握把），锚点图 sha `f1a84c4c2b83`；047 版留作 `_v3.png`。待用户确认后改 `c24` 卡、出全身。
- 第三轮（用户「还是 v1 更好，就用它出视频」）：`m1_Treant.png` 恢复为 v1，卡与 `battlefield.md`、`d01` 改回 v1 造型；`v2a`、`v2b`、`v3`、`v4` 作废待删。建立视频 `m1_Treant_turntable.mp4`（9:16 · 4 s · 720p，submit `241a807f`，72 积分）代理初审画面通过、声音待用户听。技能卡与资料包本来就是 v1，不用同步。

## 2026-10-21 — follow-up 049 / 050

- 049：p29 握把挪内侧、外弧连续，出 `_v5.png`。
- 050：用户回到 046 版 `_v1` 方向，只把刃口挪到外面；以 `_v1` 作参考重出 `p29_Anti_Mage_Glaive.png`（sha `afaa98c7eae0`），一次审核拦截未扣费。待用户确认后改 `c24` 卡、出全身。
- 2026-10-21 用户：跳得太慢，要 4 只、能多跳 → 第四条 `renders/20261021-215938_ee807d33/`（来回弹 8 次，submit `ee807d33`，180 积分）；用户随即改口「不要来回弹，4 只就弹 4 次」，该条作废。卡锁定「每个目标只打一次、跳到最后一只结束、整串约 0.3 s」，第五条 `renders/20261021-220603_0388c4a1/`（submit `0388c4a1`，180 积分）。代理初审：一次出斧、各打一次、顺序倒地都对，但后三次命中像从上方竖劈、目标之间不见连线，速度约 1 s。k401 本轮共出 5 条（900 积分）。

## 2026-10-21 — follow-up 051

- p29 加细节（护手与轮廓不变）：`p29_Anti_Mage_Glaive.png` sha `ed4162733102`，050 版留作 `_v6.png`。待用户确认后改 `c24` 卡、出全身。
- 2026-10-21 用户：A 跳到 B 时要有闪电链连着两只；两条路都做。① 后期版 `k401_Arc_Lightning/post/20261021-后期电弧_0388c4a1/k401_Arc_Lightning_clip_post.mp4`（8.58 s，本地合成、不扣积分）：底片 `0388c4a1` 重排成 斧→B→A→C→D，每跳画连线电弧，整串约 0.6 s。② 后期版去音轨作参考视频再出 `renders/20261021-222156_6fb90177/`（submit `6fb90177`，216 积分）：有了连线电弧，但跳了约 1.4 s、超过四次。k401 本轮 Seedance 共 6 条，1116 积分。

## 2026-10-21 — follow-up 052

- p29 以 `_v6` 为基础把外缘改圆滑、去尖刺：`p29_Anti_Mage_Glaive.png` sha `3b3446537424`；051 版留 `_v7.png`。待用户确认后改 `c24` 卡、出全身。

## 2026-10-21 — follow-up 051

- 兵线 m1–m6 建立视频补齐：新出 `m2_Druid_of_the_Talon_turntable.mp4`、`m3_Glaive_Thrower_turntable.mp4`、`m5_Necromancer_turntable.mp4`、`m6_Meat_Wagon_turntable.mp4`（Seedance 2.5 · 720p · 4 s，各 72 积分，共 288；请求见 `characters/request_log.md`）。代理初审画面通过，声音待用户听；m6 首次下载 SSL 断开后按 submit 号补收。

## 2026-10-21 — follow-up 053

- p29 外缘改一整条顺滑刃弧（无波浪尖刺），护手收进弧内：`p29_Anti_Mage_Glaive.png` sha `f57a99acb83e`；052 版留 `_v8.png`。待用户确认后改 `c24` 卡、出全身。
- 2026-10-21 用户：后期版还行，电弧速度慢一倍。后期版 v2 `k401_Arc_Lightning/post/20261021-后期电弧v2_0388c4a1/k401_Arc_Lightning_clip_post.mp4`（8.92 s，本地）：每跳停留 4 帧，三跳约 0.63 s。
- 2026-10-21 用户：再慢一倍。后期版 v3 `k401_Arc_Lightning/post/20261021-后期电弧v3_0388c4a1/k401_Arc_Lightning_clip_post.mp4`（9.17 s，本地）：每跳停留 8 帧，三跳约 1.0 s。

## 2026-10-21 — follow-up 054

- p29 刃口定稿（053），弧度放平放宽：`p29_Anti_Mage_Glaive.png` sha `7f8a853a85c1`；053 版留 `_v9.png`。待用户确认后改 `c24` 卡、出全身。
- 2026-10-21 用户定：k401 正式样片用后期版 v3 `k401_Arc_Lightning/post/20261021-后期电弧v3_0388c4a1/k401_Arc_Lightning_clip_post.mp4`。技能卡、`skills/README.md`、人物卡 c40「技能画面」概要同步（旧描述里的短刀、5 只一排改掉）。
- 2026-10-21 用户：技能三小怪换成食尸鬼。`k403_Static_Field` 卡、峰值图 prompt、技能视频 prompt 换成新造型 `m4`（骨爪无刀、低沉喉音）；峰值图重出（gid `Dd5V7kMe5mrdAZ2XEJj4`，旧图与落选在 `_deleted/`），资料包已同步；技能视频未重出。

## 2026-10-21 — follow-up 055

- p29 敌法师月刃定稿（sha `7f8a853a85c1`）。之后只做敌法师。
- `c24` 卡武器描述换成定稿；立绘带参考重出 `c24_Anti_Mage.png` sha `efe42bd85ed0`（`_v5` 旧武器版、`_v6` 月刃偏小留档）。待用户确认。

## 2026-10-21 — follow-up 056

- `c24` 立绘改横提月刃、画幅 16:9，月刃与 p29 锚点图同形同大：`c24_Anti_Mage.png` sha `350874fa88ff`；竖拿版留 `_v7.png`。待用户确认。

## 2026-10-21 — follow-up 057

- `c24` 立绘改三步合成（无武器底图 → 本地贴 p29 定稿锚点图、拳心对准握把正中 → 模型只修手与光影）：`c24_Anti_Mage.png` sha `00c2ff389c69`；056 版留 `_v8.png`；中间文件与脚本 `c24_Anti_Mage/_work/`。月刃在立绘里约 1.05 米（受两手间距限制）。待用户确认。
- 2026-10-21 用户：k403 改成只放技能二。视频 prompt 改为连放两次闪电击触发静电场，峰值图按落雷重出（gid `aEUvTFfwGKjYhG8Qogqh`，斧头版与七只落选版在 `_deleted/`）；720p 正式条 `renders/20261021-230106_fa495356/`（submit `fa495356`，198 积分）。代理初审：两次落雷各引一次全场同帧叉形电光、无连线；偏差：电光晚落雷约 0.2 s，结尾五只全倒（应留三只）。

## 2026-10-21 — follow-up 058

- `c24` 立绘改竖握合成（p29 旋转 90°、护手转正，约 1.4 米，拳握正中）：`c24_Anti_Mage.png` sha `4b3fb7fce398`；057 横提版留 `_v9.png`。待用户确认。
- 2026-10-21 用户：k403 施法要快、食尸鬼走得更快、镜头拉远。prompt 改为 10 s、食尸鬼从约 30 m 外飞快窜来、举锤即落雷、20 m 高 16mm 超广角俯拍；新条 `renders/20261021-231640_f19a0efd/`（submit `f19a0efd`，180 积分）。代理初审画面通过；偏差：电光晚落雷约 0.2 s，结尾五只全倒。

## 2026-10-21 — follow-up 053（地图建筑与商店，用户睡觉、自主模式）

Source: user_input/follow_ups/202610.md § 053
Summary:
- Research：两方遗迹、泉水、出生圈、塔、兵营、附属建筑（17 项）与全部商店（15 家）下载 WC3 经典模型图与 DotA 1 截图，每目录 `refs.md`（`0_research/building_refs/`、`shop_refs/`，免费公开页面，未调用收费服务；暴雪素材只作人眼参考）。汇总与对 d01 / d08 的更正写成 `0_research/parts/d16_地图建筑与商店.md`，dossier 与 d01 §3.3–3.5 加指向。
- 资产：新立背景卡 bg15–bg36（单体建筑、商店建筑、两方商人营地、天灾侧秘密商店、地精实验室），商人人物卡 m300–m309（号段 m300–m319 留给商店与地图 NPC）；按原版重写 bg2、bg3、bg11、bg12、bg13、bg14（旧图改名 `_v1.png` 留档）。registry.toml（next = 37）、assets_index.md 同步。
- 出图：28 张背景锚点图（`tools/gen_bg_images.py`）+ 10 张商人立绘（`tools/gen_char_images.py`），全部 ElevenLabs `gpt-image-2.5-sunburst`、先写请求日志（`background/request_log.md`、`characters/request_log.md`）；bg23 首次轮询网络中断，按 gid 补收、未重提。代理逐张看图初审通过（小偏差写在各卡「生成记录」），待用户看图。视频未出（「生成视频永远人点」）。
- 工具：`tools/gen_bg_images.py` 的 `Job.send` 不再把 text 块首行路由键（目录名，常带原名）发给模型，与 `gen_char_images.py` 一致；加测试 `test_routing_key_line_not_sent`。此前各剧 bg 图的送审稿都带了首行目录名。
- 判断依据（自主）：bg4 / bg5 塔形与原版不符但已被技能卡与斧王 demo 大量引用，不改、记入 `battlefield.md` §6 第 7 条待用户定；bg2 / bg3 / bg11–bg14 下游无引用（bg3 只在 c110 技能卡文字里提到），直接重写重出。队伍色（近卫红、天灾绿）按 world_rules 一律改材质色；出生圈原版玩家色改成统一淡光。天灾 4 级塔（蛛魔塔形态）没截图，未立卡。
- 事故：一个 research 子代理清理坏下载时误删 9 份他人写的 refs.md（未跟踪文件），已由原作者代理按原内容重写，sha 复核一致。

## Follow-up 057 — 2026-10-22 — 全部人物按 DotA 1 原图复核
Source: user_input/follow_ups/202610.md - section 057
Summary: 161 张人物卡下载原图、写 refs.md、评差异；差异大的改卡重出（出图服务中途停用，大部分待出）。

- 执行：20 个子代理各 8 张卡并行（prompt 与回复存档 `.audit/adhoc_agents/2026-10-21/dota-char-ref-review-20261021-225500/spawns/`）。原图来自 PlayDotA 存档、Wowpedia、YouTube 封面 / 截帧等免费公开页面，只作人眼参考，不上传生成服务。
- 结果（161）：重出并代理看图通过 22（c31–c33、c69、c77、c78、c80、c81、c84–c90、c93 首次、c94–c98、c100）；改卡待出图 119；差异小保留 13（c17、c79、c82、c106、c107、m9、m10、m11、m19、m24、m112、m201、m210）；有建立视频只评估 5（c65、m2、m3、m5、m6，均差异大，改动清单在 refs.md 末节，由用户定）；原图不足未定 2（m130、m202）。不在范围：c5–c9、c24、c40、m1、m4、m102–m104（此前已按原图做过或用户定稿）、m300–m309（另一会话 053 新建的商人）。
- 出图服务（2026-10-21 晚）：ElevenLabs quota_exceeded（剩 93 credits，一张约 267，未扣费）；api.openai.com DNS 解析失败，Codex 回退每次约 900 s 超时、无图落盘（结果按规矩记未知，未重提；request_id 见各 worker 存档与 `characters/request_log.md`）。之后暂停出图，其余卡只改卡、旧图改名 `_vN.png`、卡头标「新立绘待出」。恢复后 `python tools/gen_char_images.py run --drama dota_yingxiong` 只补缺图的卡（`plan` 已核 119 张全部能解析、无 rule 22.1 警告）。
- 重要更正：c58 天怒法师模型是血精灵龙鹰骑士，不是风蛇（dossier、d01、d04、d11 原句加注）；复仇之魂无翅膀；干扰者骑狼；风暴之灵是熊猫人；m24「黑蜉蝣」为误译（assets_index 已改，卡内形态目录 `m24-1_黑蜉蝣` 未改名）。
- 待同步：受影响技能卡（峰值图、技能视频 prompt、人物卡内「技能画面」概要）等新立绘经用户确认后同步；个别卡配音表与新外观不符（c26 声线、c72「长鼻号鸣」、m15「湿泥咕嘟声」、m121「骨片木珠」）。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/**（161 卡的 `ref/model/`；140 卡外观相关节；22 张新立绘）
- ai_videos/dota_yingxiong/0_research/parts/d01–d07 — 末尾加「外观更正（follow-up 057）」节；dossier.md、d01、d04、d11 风蛇句加注
- ai_videos/dota_yingxiong/2_世界观人设/assets_index.md — 「原图复核」状态节、m24 译名
- ai_videos/dota_yingxiong/README.md — 当前状态

No conflicts found in: battlefield.md、world_rules.md（准则不变，本次按其 §1 执行）

## Follow-up 059 — 2026-10-22 — 全角色死亡动作需求，先做食尸鬼研究
Source: user_input/follow_ups/202610.md - section 059
Summary: 按参考研究 → 关键图 → 视频分阶段筹划；本轮完成资料整理与计划，未调用收费生成服务。

- 清点183张主体卡（112英雄、71其他人物），写 `characters/death_assets.json`：m4研究筹划中，其他角色仅登记。当前64张主体立绘文件存在、119张缺当前别名；存在不表示外观已选定，变体尚未逐卡核对。
- 下载8个模型／战斗图候选（另1个失败），保留误下的页眉图并明确退回；从 `Mountain King vs 50 ghouls` 研究片段抽取20张参考帧。逐项用途、哈希与失败记录见 m4 `death/ref/`。第三方素材不上传生成、不进成片。
- 群战片段只能作残骸和战斗状态参考；经典单体 Death 的翻转／分体相位仍未核实，未把社区说法当事实。镜像 Art Tools 文档下载超时，未引用正文结论。
- m4筹划稿提出8秒非血腥完整身体侧倒、首尾两张关键图、固定机位、末段静止与声音验收；只是电影化提案，尚未选定。重新打开立绘发现每手4–5爪，与卡要求3爪不符，关键图需校正并核对既有视频衔接。
- 公开下载与元数据查询经 `RequestLog` 留痕；现有立绘、建立视频、声音未改。未出死亡图、死亡视频或死亡声样；没有独立成片 QC，也没有用户选条。
- 更新项目 README、资产索引和 m4 卡的阶段入口；从原始输入与月度 follow-up 重建 revised_prompt。未改全局工作流、生成默认值或共享 skill。
- 该剧当前无分集目录；本次不改 c65 demo／技能镜头。资料包工具的实际适用性与本地验证结果见 `.audit/adhoc_agents/2026-10-22/dota-ghoul-death-research-20261022/validation.json`，不把空范围检查写成全剧资料包通过。

## Follow-up 060 — 2026-10-22 09:00:40 — 小兵与英雄死亡分开
Source: user_input/follow_ups/202610.md - section 060
Summary: 食尸鬼 m4 明确按兵线小兵研究；撤回8秒通用侧倒的默认方案。

- m4死亡筹划增加当前小兵路线，区分死亡与后续尸体处理；原侧倒时间轴与提示词标为暂停草稿，不能直接提交。原版单体动作、时长和终态仍待证，不把此次分类修订当成动作取证已完成。
- 官方 WC3 单位页、英雄基础页及亡灵基础页支持普通单位／英雄和尸体机制的区别；已在参考说明写明不替代 DotA 6.83d 具体模型取证。没有新媒体下载或收费调用。
- 同步 m4卡、项目README、资产索引、死亡待办分类和 revised_prompt；c70 英雄另行研究，未将其他非英雄卡一律标成小兵。现有立绘、视频、参考帧未变。
- 仅修订本剧文档与待办，无编译镜头或参考媒体变更，不重复运行已因缺分集 prompts.json 失败的资料包检查；不声称既有资料包已验证。060本地核对结果另存本次审计目录 `validation_060.json`，059检查保留原状。


## Follow-up 061 — 2026-10-22 — 月刃刀身收窄一半
Source: user_input/follow_ups/202610.md - section 061
Summary: 保存径向刀身带宽减半的要求，维持整体长度、外弧与握把护手。内置图像编辑请求经RequestLog预先审计，输入审核以moderation_blocked/violence拒绝；没有新图，不宣称编辑完成。原p29图与卡指纹未变，无新资料包产物。证据：.audit/adhoc_agents/2026-10-22/antimage-glaive-halfwidth/。

## Follow-up 062 — 2026-10-22 — 建筑正侧背三视图
Source: user_input/follow_ups/202610.md - section 062
Summary: 刚发送的建筑图片需要正面、侧面、背面；登记需求并试生成，未把失败候选标为完成。

- 28 项背景卡和剧 README 登记三视图要求及计划路径。6 项生成 7 张候选，0 项通过；正侧背角度、灯数量及附属布局存在问题。候选保留，原锚点图 SHA256 全部不变。
- 泉水多灯问题连续两轮未解决，按 CONVENTIONS.md 的 Iteration bounds 停止此批量方法，未继续消耗生成；22 项待生成。建议先分离复合画面的单体建筑，再逐面生成或从统一三维模型渲染，待用户决定。
- 全部生成先经 RequestLog 写入 background/request_log.md，内置工具未返回费用。没有生成视频、修改镜头或参考绑定，无新增或改变的 shot_pack 范围。审计见 `.audit/adhoc_agents/2026-10-22/dota-building-three-views/`。

## Follow-up 063 — 2026-10-22 — 推进食尸鬼首帧并纠正进度报告
Source: user_input/follow_ups/202610.md - section 063
Summary: 实际尝试首帧生成，接口返回中间响应后中断，提交结果未知，无对应图片和视频；未复投。

- 此前只做研究与方案，没有后台生成；本轮说明此前进度表达不准确，继续既定制作范围。
- 起始候选只表现小兵战斗待机，不套用已暂停的侧倒末态或英雄消散。默认 ElevenLabs gpt-image-2.5-sunburst，16:9、2K、high，参考本剧现有立绘；经 image_fetch / RequestLog 先记请求。
- 实际POST只返回 HTTP 100、没有终态和任务号，结果未知、费用未知，未重提。随后经同一审计入口查询最近任务、查询并下载首个候选；看图为其他角色，已排除并移至 .audit 下 recovery_rejected，不作为 m4 产物。列表和回执均脱敏保存。
- 当前没有首帧图片、死亡末帧或死亡视频，也没有后台任务。默认出图规则不允许以这类中断当成额度不足而换服务。状态及本地检查见本次审计目录 validation_063.json；旧媒体指纹未变。原版单体 Death 证据缺口仍保留。


## Follow-up 065 — 2026-10-22 — 按用户指定用 Codex 生成食尸鬼姿态候选
Source: user_input/follow_ups/202610.md - section 065
Summary: 经 codex-imagegen 共用入口出首帧v1、修手部v2及小兵倒地末姿概念；图片已落盘，视频未做。

- 原 ElevenLabs 请求仍为结果未知，未重提；本轮是用户显式指定 Codex，不改全局默认值。登录使用 ChatGPT，先 RequestLog 后调用 tools/codex_image.py；实际图像型号与费用未暴露。
- 起始v1已看，手爪偏多退回；v2只修手部，清晰可见每手三根主要长骨爪，保留为候选。末姿只提出普通小兵倒地留体的电影化构图，不加英雄消散；具体看图结论在审计目录 codex_end_v1_qc.md。
- 原版特有翻转／分体与相位仍未核实。新末姿是本剧创作候选，不恢复旧8秒通用侧倒默认值，不表示死亡动作已经定稿。
- 版本、输入prompt、元数据和SHA见m4 death/frames；未覆盖原立绘、建立视频或旧候选，未生成死亡视频。主代理看图不冒充独立成片QC或用户选定。

## Follow-up 067 — 2026-10-22 — 食尸鬼死亡改为仰倒、腐烂成白骨
Source: user_input/follow_ups/202610.md - section 067

- 用户：死亡状态太差，应往后倒下去、慢慢变成白骨；每个角色和技能效果以后都要有死亡 demo（大场面战争可用）。
- 补参考：重制版实机 68–78 s 证明「往后翻倒 → 尸体 → 只剩骨架」（`m4_Ghoul/death/ref/reforged_death_066/`）；Hive 论坛关于 Decay Flesh / Decay Bone 的说明；写实干腐与电影特效案例。两条搜到的视频实为《魔兽世界》和 Dota 2，已退回。详见 `death/ref/refs.md`。
- Codex 出同机位 4 张：后仰摔倒 / 仰躺尸体 / 半腐露骨 / 白骨（`death/frames/*_067_*`），代理看图通过，偏差：摔倒图身体已近落地、左手只见 2 爪；白骨图黑毛偏多。065 趴倒末姿作废；人物卡「倒地 / 死亡」同步。未出视频。

## Follow-up 068 — 2026-10-22 — 食尸鬼死亡图转正式、出死亡视频；k403 用死亡参考重出
Source: user_input/follow_ups/202610.md - section 068

- 用户认可 067 四张死亡关键图，转正式（`m4_Ghoul/death/m4_Ghoul_death_*.png`），并出死亡视频（Seedance 2.5 · 720p · 14 s）。
- k403 卡视频参考加食尸鬼死亡摔倒 / 仰躺两张；动作改为被劈死的往后仰面摔倒、仰躺；负面词加「往前扑倒、趴着」。资料包已 sync，重出 720p 正式条。

## Follow-up 064 — 2026-10-22 — 单体建筑逐面三视图完成
Source: user_input/follow_ups/202610.md - section 064
Summary: 22 类建筑／固定设施，66 张单图和 22 张合图；已通过 ccconnect 发给用户，待确认。

- 用户批准拆单体、逐面生成后合图。28 张来源图去重为 22 类；组合场景复用单体，无实体商店的空地不新增建筑。每卡保存正面、右侧面、背面、合图及完整指纹清单；README 和资产索引同步。
- 内置 image_gen 经 RequestLog 先记请求再生成，75 次请求及结果可追溯，9 张退回候选保留；正交方向、台阶分布、完整入画等问题经针对性修正。费用及实际型号未知。主代理初审不等于独立终审或用户确认；未知背面明确为本剧设计补全。
- 28 张原锚点指纹不变，66 张单图与 22 张合图可解码，逐栏验证合图像素无裁切／缩放／重绘；22 张合图有 ccconnect 成功回执。无剧集、镜头、overhead 或参考绑定改动，不涉及 shot_pack 同步。完整审计见 `.audit/adhoc_agents/2026-10-22/dota-building-single-views/validation.json`。
- 结果：死亡视频 `m4_Ghoul/death/renders/20261022-203838_568d98d0/m4_Ghoul_death.mp4`（252 积分）——仰倒、仰躺、腐烂成白骨、定格都做到；0–2.2 s 是另一机位、2.2 s 硬切。k403 `renders/20261022-203721_a90d1233/`（180 积分）——第一只被劈死的照参考仰面倒下，第二只和其余三只仍往前趴倒、结尾全倒。两条待用户看。

## Follow-up 069 — 2026-10-22 — k403 五只死法统一并腐烂成白骨；死亡视频 4 秒版
Source: user_input/follow_ups/202610.md - section 069

- 用户：五只食尸鬼死法要一致，要有变成白骨的效果，参考死亡渐进图；先出一个。→ 先出 k403 结尾关键图候选 `_candidates/k403_end_bones_069a.png`（五副仰躺白骨围着矮人），待用户看。
- 死亡视频 4 秒版 `m4_Ghoul_death_4s.mp4`：本地变速剪辑，去掉开头 2.2 s 另一机位，摔倒 1.2 s + 腐烂 2.0 s + 白骨定格 0.8 s。
- 用户认可结尾图后出 k403 14 s 正式条 `renders/20261022-212206_fa26e737/`（252 积分）：五只全部往后仰面倒下、一起腐烂成白骨、定格在结尾关键图；第二次落雷偏晚约 1.3 s。

## Follow-up 071 — 2026-10-22 — 斧王巨斧立道具卡，斧头描述统一
Source: user_input/follow_ups/202610.md - section 071

- 用户：斧王各技能视频的斧头不统一，问挂带武器的立绘够不够，还是单独做武器图。→ 采纳代理建议：单独立道具卡并每次一起挂。
- 新建 `props/天灾_scourge/p30_Axe_Great_Axe/`（registry 领号 p30），参考现立绘 `c65_Axe.png` 出锚点图；ElevenLabs 额度为 0（401 quota_exceeded），按出图顺序换 Codex（第一次网络发送失败、未出图，重试一次成功）。
- `c65_Axe.md`、k651–k654 斧头句子统一成 p30 外观一句（补上四根内弧尖刺与锤背，删掉「比人还长」，全长以立绘为准约 1.5 m）；建立视频与四个技能视频的参考都加挂 p30；峰值图加图五 p30 重出：k652、k654 已换上，k651、k653 Codex 超时结果未知、未重提。`tools/gen_turntable_videos.py` 支持参考行里的道具项（加测试）。
- 现有建立视频（10-22 13:11）斧头与立绘不同，待用户挂 p30 重出；视频仍由用户出。

## Follow-up 070 — 2026-10-22 — 食尸鬼比宙斯小；k404 改五只食尸鬼五雷同落
Source: user_input/follow_ups/202610.md - section 070

- k403：食尸鬼写成比矮人小一圈，结尾关键图重出（070a）；重出 14 s 正式条 `renders/20261022-223024_7de3312d/`（252 积分）。
- k404：目标从骷髅王换成五只食尸鬼（原典不打小兵，按用户改编），五道雷同一帧劈下、全部仰倒并腐烂成白骨；峰值图 Codex 三版选 070c；14 s 正式条 `renders/20261022-222939_157b0cc5/`（252 积分），左手斧不再变锤。
- 全剧 m4 基准身高（battlefield.md）未改，待用户定是否全局缩小。

## Follow-up 074 — 2026-10-22 — k403 挥锤一道雷、白骨更快
Source: user_input/follow_ups/202610.md - section 074

- k403 prompt：两次挥锤从上往下、每次只落一道雷；倒地即烂约 1.5 s 成白骨；加死亡 4 秒版运动参考；10 s。出片 `renders/20261022-225159_a0698071/`（168 积分；首提 2036 失败不扣分）。一道雷与快速白骨做到；挥锤方向仍是往上举。


## Follow-up 075–076 — 固定武器先行与自主制作

Source: user_input/follow_ups/202610.md - sections 075–076

**武器一致性（follow-up 075）**：93 名角色、92 套固定武器；新增武器初审通过 77 套，挂武器重出人物初审通过 78 张。[对照总览](2_世界观人设/weapon_reference_gallery.html) · [武器清单](2_世界观人设/characters/weapon_assets.json)。未来人物图、建立视频、技能峰值图／视频及镜头均同时带独立武器图。待审、失败与既有修改未完成项均未算通过；未新增视频提交。

Auto-updated:

- 人物卡、武器道具卡、registry、world_rules、资产索引与 README：先武器初审，再挂武器重出人物；原图备份，未通过候选保留。
- 342 张技能卡补固定武器的峰值图参考；已有峰值图未冒充重生。
- tools/props_lib.py、gen_char_images.py、gen_outfit_views.py、gen_turntable_videos.py、skill_pack.py、shot_pack.py 与镜头资料读取：人物声明自动携带武器，缺图阻止生成／编译，漏挂的旧包失效。
- 共用资产指南、人物资产 skill、Prompt 参考规则同步；未改 skill 名称／描述。

验证：工具测试 168 passed；管理应用镜头／工作流测试 66 passed、1 skipped；工作流目录 223 源编号连续，Claude 薄入口 6/12 check 通过。覆盖页 219/223 可读，4 项为未配置的可选本机／用户规则文件，没有漏登记的现存文档引用。图像初审与 SHA 见各卡和 `.audit/adhoc_agents/2026-10-22/dota-weapons/`；不冒充独立终审、用户定稿或视频完成。未启动软件全阶段重跑。

收尾：8 个现有技能视频资料包已 sync，当前状态全部 ok；目标剧尚无分集，episode shot_pack sync 不适用。对照总览与四张拼图已生成。final_audit.json 检查正式图 SHA、旧图备份、93 人物绑定、请求链与参考来源、HTML 本地链接及在途状态；通过的 156 张正式图可追溯。13 套新增武器失败／未知，加 p29 先前窄刃修改未完成，合计 15 名人物没有冒充重出；详细清单见该审计文件。所有失败候选保留。

续跑：该审计目录 `generate.py` 跳过已有状态，不会自动重提失败／未知请求；`portraits.py --only <人物键>` 只用已通过且 SHA 未变的武器；`refresh.py` 从实际文件与审图记录刷新清单。

## Follow-up 072–073 — 2026-10-22 — 斧王挂 p30 重出视频，demo v8
Source: user_input/follow_ups/202610.md - sections 072, 073

- 072：用户认可 p30 与 k652/k654 峰值图；k651 峰值图重出换上，k653 两次 Codex 超时未重提。
- 073：用户授权出视频。建立视频与 k651–k654 都挂 p30 重出（k651 一次版权误判 2053 后原样重提成功），代理看片斧头全片一致；views 按卡内时间重抽；剪出 `demo/edit/final/ep01_final_v8.mp4`（结构同 v7）。


## Follow-up 066 — 2026-10-22 12:50 → 2026-10-23
Source: user_input/follow_ups/202610.md - section 066
Summary: 出图改走 Codex、ElevenLabs 有 blocker 直接换不问；补齐 057 待出的立绘、5 张有视频的卡按原图改并重出视频、斧王 demo 正片重出；技能卡与峰值图同步到新外观。

- **全局规则**：`tools/image_engine.fallback_ok` 改为 ElevenLabs 任何失败都换 Codex（取代 ai_video_management follow-up 275 的只看额度）；CONVENTIONS「图片的生成服务」「出图与出片的授权」、`paid_services.md`、pipeline `resources/assets.md`、`codex-imagegen` SKILL、`ai_video_workflow.md`、`prompts-references.md`、出图器帮助文字同步；`tools/tests` 160 passed。codex-imagegen SKILL 记卡住 / 被拒的常见措辞原因与「一次最多 5 张参考图」；paid_services 记即梦 `OutputVideoCopyright` 原样重提一次即过、建立视频下载断线用 `--force --harvest` 补收。
- **工具**：`tools/gen_turntable_videos.py --harvest` 支持 `--only` 与 `--force`，同卡多次提交只收最新一条，`--force` 时旧片占着文件名也照收（m2、m3、m5、m6 下载 SSL 断线后均按 submit_id 补收、未重提）。
- **立绘**：119 张待出 + c65/m2/m3/m5/m6 共 124 张用 `gen_char_images.py --engine codex` 出图；10 个验收子代理逐张对照 refs.md，c20/c23/c26/c58/c101/c111/m20 各重出 1 轮、c37 与 c109 由主代理复核后改措辞重出；c49 被 Codex 审核拒（熊猫人联想）、m13/c28/m181/m25 连续卡住无图，改措辞后出成（确认无图后才重提）。c26 首图背旗出现游戏阵营标志，改为素旗重出。合计 146 张差异大的卡已有新立绘。
- **视频**（用户本条点）：c65（16:9 · 10 s）与 m2、m3、m5、m6 建立视频 Seedance 2.5 · 720p 重出并抽三视图、合图（c65 的 10 s 片按卡抽 0.3 / 3.5 / 5.0 s 手工补抽）；斧王 k651–k654 按用户选择直出 720p 正式条（k651 一次 `OutputVideoCopyright` 后原样重提成功），剪成 `ep01_final_v7.mp4`（沿用 v6 结构，scratchpad 脚本 `axe_cut_v7.py`，`cut_v7.json`）。即梦积分：建立视频约 180 + 4×72，技能 198+234+198+198+198（重提），以回执为准。
- **技能卡**：9 个子代理把 106 位英雄（除 c24、c40、c65）技能卡里的施法者与小兵 / 召唤物外观改成新卡；与新外观矛盾的动作道具顺改（如 c19 长剑→钉锤盾、c58 风蛇→龙鹰骑士、c60/c51 骑乘施法、c100 空手施法）；已有峰值图 107 张（含斧王 4 张）Codex 重出、逐张看图。与另一会话 follow-up 075 同时改技能卡：保留其武器参考行，出图时缺盘的武器图跳过并记录。
- **清理**：c72、m15、m121、m5、c26 配音描述与 c25「形态」按新外观改；23 张卡头「立绘未出」、12 张「技能卡待同步」改正；skills/README「暂缓」行解除。

Auto-updated:
- tools/image_engine.py、tools/gen_turntable_videos.py、tools/tests/test_scene_image_policy.py、各出图器帮助文字
- CONVENTIONS.md、.agents/references/project/{paid_services,ai_video_workflow}.md、.agents/skills/{codex-imagegen/SKILL.md, ai-videos-pipeline/resources/assets.md, ai-videos-pipeline/modules/prompts-references.md}
- ai_videos/dota_yingxiong/2_世界观人设/{characters/**, skills/README.md, assets_index.md, world_rules.md}、README.md

待用户：看新立绘（146 张，各卡「生成记录」）、斧王 v7/v8、5 条建立视频；技能卡里改了锁定节的取舍（各子代理存档 `.audit/adhoc_agents/2026-10-21/dota-char-ref-review-20261021-225500/spawns/skillsync-*/output.md`）。

## Follow-up 077 — 2026-10-23 — 宙斯 demo v1

- 用户接受宙斯 5 条视频（人物视频、k401 后期版 v3、k402 `1bc315a3`、k403 `a0698071`、k404 `157b0cc5`）。
- 照斧王 demo 结构剪 `characters/近卫_sentinel/c40_Lord_of_Olympus/demo/edit/final/ep01_final_v1.mp4`（50.2 s，720p，`cut_v1.json`）：0.8 s 压暗转场、英文标题卡（DotA 1 快捷键 C / G / F / W，PNG `title_card_k40N_en.png`）、施法时段左上角图标、人物视频转身段静音、片尾 1 s 淡出。本地剪辑，无收费请求。脚本 `.audit/adhoc_agents/2026-10-23/zeus-demo-077/zeus_cut_v1.py`。
- follow-up 074 的执行结果先前被并发写到 076 段下，已挪回 074。

## Follow-up 078 — 2026-10-23T07:59:45+08:00 — Luna 五条视频
Source: user_input/follow_ups/202610.md - section 078
Summary: 明确授权按 Axe 当前规格生成并发送亮相与四技能；开始制作，未宣称完成。

- c23 亮相从通用 4 秒改为本剧 10 秒、末 2 秒收尾；不改人物身份或技能锁定内容。补四技能视频 prompt 与参考包后提交，所有外部请求先留痕。


### 执行结果

生成 7 条（亮相 1、四技能首版 4、月光／月蚀各修正 1），选取 5 条 720p 原片，经 ccconnect 以 5 个 ZIP 成功发给用户（包内 SHA256 与原 MP4 一致；直发 MP4 报飞书 230055 文件类型错误）。服务回执积分共 1332，逐次请求先记日志、ID 落盘，未重提结果未知的任务；亮相 Python 下载阻塞后经审计 CLI 补收，只停止本次 PID 30840，不影响其他会话。

主代理抽帧看图、全片解码与参考指纹检查；月光首版横向武器光束、月蚀首版结尾蹲伏均保留并修正。各卡记当前结论与偏差；当前环境不支持音频输入，未作台词／背景音乐试听，不能据音轨存在宣称通过。五条待用户看与试听，未作独立终审。四技能资料包同步且指纹有效；无集／镜头／overhead／镜头绑定变更，未运行无范围的 shot_pack 全仓同步。审计 `.audit/adhoc_agents/2026-10-23/luna-five-videos-20261023-075830/validation.json`。

## Follow-up 079 — 2026-10-23T08:01:41+08:00
Source: user_input/follow_ups/202610.md - section 079
Summary: 全能骑士照片与人物视频，沿用最新照片，更新10秒亮相提示词并按用户授权出片。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c3_Omniknight/c3_Omniknight.md — 旧4秒竖幅改为10秒横幅，固定p31武器，原台词口型同步、末2秒站定。
- user_input/revised_prompt.md — 汇总本次指令。

No conflicts found in: 既有人物与武器外观；本次不改其他会话产物。

## Follow-up 080 — 2026-10-23 — 斧王、宙斯 demo 发布文案
Source: user_input/follow_ups/202610.md - section 080

- 新建 `c65_Axe/demo/publish.md`（对应 `ep01_final_v8.mp4`）与 `c40_Lord_of_Olympus/demo/publish.md`（对应 `ep01_final_v1.mp4`）：YouTube / TikTok / Instagram 全英文，抖音 / 哔哩哔哩 / 小红书 全中文；标题、简介、标签各一个代码块，按平台字数上限写，附 AI 生成标注与非官方声明。

### Follow-up 079 执行结果 — 2026-10-23T08:09:58+08:00

全能骑士照片和10秒人物视频已通过cc-connect发送（ZIP，MP4直传被飞书拒绝）。生成回执180积分；源片保留，本地节奏修正与三视图/合图/声样已落盘。当前产物SHA与QC、音频未核听范围及发送回执见`.audit/adhoc_agents/2026-10-23/omniknight-assets/state.json`。视频待用户看片确认；四个技能未提交。无本剧episodes/shot pack，未改共用源。

## Follow-up 081 — 2026-10-23T08:14:37+08:00
Source: user_input/follow_ups/202610.md - section 081
Summary: 明确授权全能骑士四技能，补新峰值图并按Axe规格出片及cc-connect交付。

Auto-updated:
- user_input/revised_prompt.md — 汇总本次指令。
- c3_Omniknight/skills/k31–k34 — 本轮制作范围，具体产物状态与QC逐项落盘。

## Follow-up 083 — 2026-10-23 — 宙斯建立视频重出（不踏步），demo v2

- 用户否定 demo v1 的转身段静音。宙斯卡建立视频 prompt：转身双脚不抬、不踏步，转身段声音只有电弧噼啪与电流嗡鸣，负面词加踏步 / 靴子踩地声 / 盔甲碰撞声。
- 重出 `c40_Lord_of_Olympus_turntable.mp4`（submit `5e101443`，180 积分；前一次 `74a07b29` 上传失败未生成；首次下载损坏后只重下）。
- demo v2 `c40_Lord_of_Olympus/demo/edit/final/ep01_final_v2.mp4`（50.2 s，`cut_v2.json`），原声不静音。


### Follow-up 081 执行结果 — 2026-10-23T08:54:21+08:00

四技能首轮720p视频和新版峰值图已通过cc-connect三包ZIP发送成功，生成回执共828积分，图片5次费用未知。原片保留、播放副本及ZIP校验完成；四份技能资料包state=ok。逐条当前SHA、ASR、观察到的偏差与未核听范围见`.audit/adhoc_agents/2026-10-23/omniknight-skills/state.json`。候选待用户观看，退化光环速度对比/白霜停留和洗礼持续时间等尚有偏差；未宣称完整媒体验收或独立终审通过。


## Follow-up 082 执行结果 — 2026-10-23T09:03:46+08:00

参照Axe补CM人物与四技能首轮素材，三包ZIP经cc-connect全部发送成功。Codex图片6次，Seedance2.5视频5次，视频回执1104积分；未知或失败下载未重提。原片保留，本地修新星尾跳切及冰封持续，69秒顺序预览未锁片。数量/光效等偏差和声音未人工核听范围明确记录在c41/README.md及assets_manifest.json；未宣称独立终审通过。四技能资料包限定同步检查，不适用episodes集级shot_pack。没有改共用源或工具。


## Follow-up 084 — 2026-10-23T10:50:28+08:00

CM技能1纠偏：旧轻点地面/不倒地及漏死亡参考使动作与用户预期冲突，本轮改主动伸杖瞄准、主目标先中再范围波及，挂入m4专属4秒仰倒/留骨视频，任务`9f920d2f-0948-4570-ac47-440176f34ea7`，240积分，单包ZIP发送成功。具体表现与未核听范围绑定当前SHA，见技能take/review.md和本轮.audit/.../cm-skill1-rework/state.json；旧合剪标记过期，不假称锁片。共用assets技能流程与生成入口/目录同步，相关12测试通过、1跳过，入口/目录/资料包检查通过。其他角色/技能不批量重生。


## Follow-up 085 — 2026-10-23T11:25:30+08:00

CM技能1纠正为远程、无弹道、目标胸肩高度空中原位霜爆；撤回地面冰环假设，换Codex峰值图，再挂m4专属死亡视频出16秒720p。任务`38c5010b-2cec-42a5-84c4-95e729631726`，240积分，新图与视频经cc-connect成功发送，原片保留。观察、偏差及未核听范围绑定当前SHA，见技能take/review.md及.audit/adhoc_agents/2026-10-23/cm-skill1-airburst/。共用资产规则补射程与来源分别锁定，目录/入口/全局工作流测试通过（12通过1跳过）。旧合剪不更新；其余技能未重生，未锁片。


## Follow-up 086 — 2026-10-23T13:32:04+08:00

CM技能1重做快速起手与水平径向渐变冰雾，任务`f9973d8e-0806-4549-9b0b-4b9a5a077bda`，8秒720p源片、144积分，当前7.050秒候选单包ZIP经cc-connect发送。新图连接中断、结果未知，未重提，不上传旧纵向图；只用六份实存自有参考。实际表现/偏差、本地处理与SHA见take/review.md及.audit/adhoc_agents/2026-10-23/cm-skill1-gradient/。资料包限定同步检查，不重生其他技能、不改共用默认值，声音待试听、未锁片。


## Follow-up 088 — 2026-10-23T16:47:12+08:00

CM技能1统一爆心/雾心为主目标胸腹，同帧全范围峰值；新增效果源`7bcf643f-9f9d-42bf-aa0f-f41b0fa962fd`、120积分，与旧干净起手拼成6.350秒预览并经cc-connect发送。旧局部变速候选不采用，原片保留；实际观察、偏差及SHA见take/review与本轮.audit。流程补空间gradient和时间演化区别，目录/入口检查通过，相关测试12通过1跳过；两段086错位执行说明归回原条目，087正文保留。声音待试听、未独立终审或锁片。


### 088 v6逐帧复核更正

逐帧复核更正：先前2fps抽帧漏掉了原片开头0–0.333333秒的右侧射入光束，所谓“源片第一帧即全范围峰值”不成立。已查看最终剪接点及0–1.5秒细帧，v6剪去这段后直接从胸腹亮核与范围雾峰值开始；新文件已发送替代v5，无新生成或费用。雾的水平形态仍不达标，保留偏差，不作为完全通过。


## Follow-up 089 — 2026-10-23T19:06:05+08:00

CM技能1改为一镜到底、约0.5秒爆炸展开。更新技能卡、角色卡与当前选择；任务`396214ec-857e-4df5-99f3-e7a9faf6b659`回执144积分，单包发送成功。原片约0.9–1.8秒仍有杖头至目标的发射亮线，未实现完全无弹道的凭空起爆；冰雾偏球形且上下溢散，不是指定的水平薄层，空间gradient不足。死亡姿态部分前倾/侧倒，没有完整遵守仰面收爪参考。半秒时长为抽帧近似观察，不冒称精确0.500秒。音频未人工核听，开头ASR有极短疑似误识别，待试听；无独立终审，未锁片。第二条加入运动示意后亮线更长、仍未纠正机制，不采用；delogo和干净底板局部修补都露痕，均不采用，没有把修补版冒充完整原片。


## Follow-up 090 — 2026-10-23T19:55:47+08:00

无发射/无弹道作为CM技能1硬要求：废弃089带连接线条的验收资格，Codex新图锁被动材质法杖与目标原位霜核，新8秒条经97个原生帧空域裁图和全片检查未见发射/弹道/连接线，已cc-connect发送。1条144积分、1图型号/费用未知；其他表演、雾形、声音待审，未锁片。

## Follow-up 087 / 091 — 2026-10-23 — 全能骑士四技能参考研究、重写与重出

- 用户：Omniknight prompt 质量不高，每个技能先下载多张参考研究再改 prompt、再出片；小兵只用树人或食尸鬼，食尸鬼死亡照对应图片。
- k31–k34 各建 `ref/research_087/` 与 `ref/refs.md`（下载经 RequestLog 留痕，原版素材不上传）；四张卡锁定段与视频 prompt 重写，挂 `m4_Ghoul/death/` 四张渐进图与 4 秒运动参考；k31–k33 峰值图用 Codex 重出，k34 因 Codex 连接失败未出。
- 出片（720p 正式条）：k31 `23da3230`（180）、k32 `faae877c`（216）、k33 `a5d65629`（204）→ 091 重出 `66dd7563`（204）、k34 `d6494afb`（216），合计 1020 积分。
- 091：退化光环只慢移动（靠近、逃跑都慢），攻击速度不变，不是慢镜头。


## Follow-up 092 — 2026-10-23

树人小兵 m1 死亡动作：`m1_Treant/death/`。Codex 出关键图今晚反复失败——仰躺树尸 `m1_Treant_death_2corpse.png` 出成（第 3 次）；「往后倒」「枯萎一半」两张各有一次 15 分钟超时、结果未知，按规则不重提，「枯木」未提交。用户定直接出 4 秒，视频挂立绘 + 树尸两张参考，seedance2.5 720p，submit `87c00ade`，72 积分，`renders/20261023_87c00ade/m1_Treant_death.mp4`。代理看片：倒下与枯萎成银灰枯木都读得清，但 1.92 s 有一刀硬切（远景 → 树尸机位，切点叶冠跳色），不是要求的一镜到底；末态叶堆灰叶、根脚未变灰。音轨未核听，待用户看片。


## Follow-up 096 — 2026-10-23 21:36:48
Source: user_input/follow_ups/202610.md - section 096
Summary: 两方基地原版坐标、已有建筑资产映射与参考素材总览。

Auto-updated:
- user_input/revised_prompt.md — 汇总本次项目指令。
- ai_videos/dota_yingxiong/0_research/base_layout_refs/ — 重新下载原地图；6 张坐标图、86 点坐标清单、参考清单与 HTML 总览。
- ai_videos/dota_yingxiong/0_research/parts/d16_地图建筑与商店.md — 四级塔截图补证与本次范围。
- ai_videos/dota_yingxiong/2_世界观人设/assets_index.md、README.md — 追加总览入口及缺口。

核对：60 座建筑中 58 座映射现有 20 类基地资产；两座天灾四级塔未假配；86 点回查原脚本行、素材路径和 HTML 本地链接通过。4 张资产号/放大图已看图，数字版同源输出。未重新审定旧图质量、未提交生成、未改镜头绑定资产。剧规格没有 interview/findings/final_specs/validation 文件；按当前资产路径接续，其他会话改动保留。
审计：.audit/adhoc_agents/2026-10-23/dota-base-layout/verification.json。

## Follow-up 093 — 2026-10-23 — 全能骑士四技能第二轮

- 用户：洗礼改给自己加、周围食尸鬼死，食尸鬼攻击别像挠痒（看原版）；驱逐是魔法免疫罩、只给自己加、不要食尸鬼；退化光环里逃跑的也逃不掉；守护天使施法快一点、释放后所有友军身上有无敌标记。
- 食尸鬼攻击动作按 WC3 原版动画研究后写进 `m4_Ghoul.md`；四张技能卡重写（旧卡存 `_history/` 或 `ref/`）。
- 出片：k31 `6fbdbec3`（180）、k32 `bacf244c`（180）、k33 `8f0f64d5`（204）、k34 `a910176e`（192），合计 756 积分。


## Follow-up 097 — 2026-10-23

树人死亡改成先下肢后上身、两臂撞地折断感、不弹起（人物卡受击反应同步）。只挂立绘、机位写进 prompt，4 秒 720p，submit `c9802af1`，72 积分，`renders/20261023_c9802af1/m1_Treant_death.mp4`。代理看片：一镜到底无切镜；腿先折、身子塌成跪坐再整体倒地，未见回弹；枯成银灰枯木。偏差：上身往下塌而非明确往后倒、两臂看不出折断角度与断口、叶冠倒地途中提前变橙。音轨未核听，待用户看片。

## Follow-up 098 — 2026-10-23 — 全能骑士四技能第三轮

- 用户：洗礼无台词、单手举锤朝天、圣光给自己恢复、周围食尸鬼死；驱逐举锤、更快、无台词、罩子更厚更圆；退化光环对骑士自己无影响；守护天使树人要有手并反击、无敌后树人也有标记。
- 四张卡改写（093 版卡存 `_history/*_card_093.md`）；驱逐按 Dota 2 / DotA 1 原版改为正圆球罩 + 旋转光带。
- 出片：k31 `fce1e1f5`（168）、k32 `02f14328`（144）、k33 `af885474`（204）、k34 `b84c2c53`（192），合计 708 积分。


## Follow-up 100 — 2026-10-23

树人死亡改为侧身倒地、不跪倒（人物卡同步）。submit `c7a0a625`（首次上传失败未提交后重试一次），72 积分，`renders/20261023_c7a0a625/m1_Treant_death.mp4`。代理看片：一镜到底；腿先折歪、整个侧倒侧躺、没跪、落地不弹；枯成银灰枯木。偏差：站立时叶冠出画顶、倒地时出左边；叶子站着就开始变橙；前 1.6 s 受击反应弱；手臂折断仍不明显。音轨未核听，待用户看片。

## Follow-up 094 — 2026-10-23 — Luna 四技能按网上参考重做
Source: user_input/follow_ups/202610.md - section 094
Summary: 补 DotA 1 / Dota 2 技能参考，四张技能卡改为月夜并重写特效与 prompt；4 条 720p 重出（756 积分），峰值图因 Codex 断流与 ElevenLabs 无额度未出。


## Follow-up 099 — 2026-10-23 — 补缺塔并接入管理站
Source: user_input/follow_ups/202610.md - section 099

新增 bg37 天灾四级蛛魔塔，原版 u00T 的两处实例替换为 bg37#01/#02，不混用绿色尖晶的 bg26。主图、正面图已出并由主代理看图；侧面/背面各三次 Codex 请求均网络失败，无新文件，按上限停止。另一次 ElevenLabs HTTP 100 未给任务ID，结果未知不重提。没有伪造三视图合图。请求审计见 background/request_log.md。

60座建筑全部映射21类资产，另列16位商人和10个出生圈。数字图、真实资产编号图、商店放大图与10张游戏参考接入现有 http://127.0.0.1:8766/base-layout 页面；剧导航/首页有入口，临时8765服务已停止，旧HTML移入审计归档。用户醒后可在同页放大、搜索、预览和下载。原版游戏素材仅供人眼，未上传生成服务。

UI代码与验证见管理项目 follow-up 297：前端相关14项、后端相关25项通过；构建通过；Chrome实际页面交互与桌面/窄屏截图检查通过。当前图片仍为候选，未做用户或独立终审。

## Follow-up 106 — 2026-10-23 — 两基地自主搭景准备
Source: user_input/follow_ups/202610.md - section 106

新增 bg38近卫基地全景、bg39天灾基地全景。每座保存30个带真实资产/实例号的建筑体块、43行CSV/JSON摆放表、米制平面图、Blender文件和俯视/总览/遗迹/泉水四张检查图。原版XY逐项回查通过；12游戏单位/米、建筑占地/高度为工作候选，模型视觉正面未确认。三组机位按所需主体包围盒和取景余量计算，主遗迹及两塔、泉水及两商店均完整入画。

原地图 W3E 的129×129顶点高度场已提取，泉水商店区比主基地高128游戏单位（工作比例约10.67米）；技术场景和摆放表已带高程。悬崖/坡道专用模型、接地边缘、精细建筑、树和装饰未重建。原版点位、渲染所用blocks散列、Blender实例集、四张QC图散列一致；bg37/38/39平面图schema检查通过。坐标文件和新资产未绑定任何Dota episodes镜头，shot_pack本次同步范围为空，未宣称其他剧镜头资料包全部同步。

天灾电影概念候选已出并看图：冰封王座与两座蓝球塔成立，未严格匹配30个实例和地形；远处城堡仅生成细节，不登记原版资产。原版截图、技术图均未上传生成，参考使用本剧自有建筑正面图/主图联系表与bg1世界图。近卫概念图第三轮成功：世界之树、两座树人塔、泉水和森林暖光成立；泛化背景建筑不登记新资产，数量/三路/高差未严格对齐。两张均已在管理页展示，作为未获用户批准的美术候选。

审计：.audit/adhoc_agents/2026-10-23/dota-base-layout/，包括 native_verification.json、browser_verification.json、assembly_consistency.json 及截图。workflow_catalog --check：11组223源连续；未改共用skill名称或描述，不需生成入口。未提交新视频，未动其他会话制作内容。

## Follow-up 103 — 2026-10-23 — 全能骑士声音研究与第四轮

- 研究全能骑士说话声音与技能音效（`c3_Omniknight/ref/audio/research_103/`）；人物卡声线改为低沉温厚男中音（原声约 100 Hz）。
- k31、k32、k34 声音锁定段与视频 prompt 按研究重写；k32 加一圈绕球罩旋转的圆形符文环；k34 每个友军各落光柱与光天使虚影、身边飘发光羽毛、树人持续反击。旧卡存 `_history/*_card_098.md`。
- 出片：k31 `9f30c5b5`（168）、k32 `601b7b13`（144）、k34 `d590c869`（192），合计 504 积分。



## Follow-up 102 — 2026-10-23 23:22:17
Source: user_input/follow_ups/202610.md - section 102；自主接续授权见105。
Summary: 全英雄原声与技能音视频参考库；保留真实缺口与版本差异。

Auto-updated:
- ai_videos/dota_yingxiong/0_research/media_refs/ — 112位逐英雄索引、原声／叫声、技能画面、来源及离线包。
- ai_videos/dota_yingxiong/README.md、0_research/dossier.md — 当前音视频资料入口与覆盖边界。
- user_input/revised_prompt.md — 合并本月已落盘追加指令。

Validation:
- 1,732个已有WAV逐文件SHA256一致；232个生成试听／短片及13份实机／游戏录音完整解码无错。
- JS语法、本地媒体路径、112位编号覆盖通过；ZIP CRC与文件清单核对通过（2954个条目）。
- 浏览器无可用实例，未做页面浏览器视觉／交互实测；新增公共音频未逐条听辨，未做独立审稿。

Incomplete:
- 原版四技能声画未齐，实机画面19位；其余媒体流403／超时，保存112位待补队列，不用波形MP4冒充实机。
- 关键地图版本已逐片读画面标注；未修改其他会话正在制作的卡片／prompt，未生成付费媒体。

## Follow-up 095 — 2026-10-24 00:05:00

Source: user_input/follow_ups/202610.md - section 095
Summary: CM 四技能按 DotA 1 原版参考研究后重写卡片并重出 720p；新星回到地面冰晶环。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c41_Crystal_Maiden/ref/skills/ — 新增原版抽帧拼图与 refs.md
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c41_Crystal_Maiden/skills/k411–k414 — 锁定段、prompt 重写；新渲染与 review.md；k413 新峰值图
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c41_Crystal_Maiden/README.md、ai_videos/dota_yingxiong/README.md — 当前选择与状态

No conflicts found in: 共用 skills / CONVENTIONS（未改）

## Follow-up 108 — 2026-10-24

树人死亡往侧后方倒、树干可稍微折断（人物卡同步），机位拉远保证整棵在画内。submit `cd21c82e`，72 积分，`renders/20261024_cd21c82e/m1_Treant_death.mp4`。代理看片：一镜到底、整棵全程在画内；腰部裂口、往左后斜倒侧躺、不弹、枯成枯木。偏差：受击后叶冠立刻变紫红；腰部裂口站立时就出现且横平；中段张臂停顿约 1 秒；远景下树人偏小。音轨未核听，待用户看片。

## Follow-up 110 — 2026-10-24

树人死亡只做倒地（不枯萎、叶子不变色）、机位推近、裂口改为斜裂。submit `4df2cf8b`，72 积分，`renders/20261024_4df2cf8b/m1_Treant_death.mp4`。代理看片：一镜到底、整棵在画内、叶冠全程暗绿；腿先折、往左后斜倒侧躺、不跪不弹、约 2 s 定格。偏差：斜裂口受击后站着就出现；受击后张臂略停；树人约占画高五成多；手臂折角不明显。音轨未核听，待用户看片。

## Follow-up 109 — 2026-10-24 — 驱逐符文环转轴、守护天使改符文标记

- k32 符文环改为沿 x 轴转（`renders/20261024-080051_b263709d/`，144 积分；出来是水平环，待确认）。
- k34 去掉天降光柱与降落天使，改为柔和暖光直接照下、每个友军背后浮现淡金线条符文印记，树人全程攻击；两次提交均 `1151 TranscodeFail`，未出片。
- 核对另一会话参考库的全能骑士音效：没有可用的干净技能音效（WC3 文件为空、实机有解说）。


## Follow-up 111 — 2026-10-24

树人折断改为多处崩裂、不像刀砍（人物卡同步）。submit `aa156cf7`，72 积分，`renders/20261024_aa156cf7/m1_Treant_death.mp4`。代理看片：动作、方向、不变色、不弹都保持；但折断仍是一道窄斜裂线加几根细木刺，未见多处参差崩裂，且受击后站着就裂开。音轨未核听，待用户看片。


## Follow-up 107 — media download continuation
Time: 2026-10-24T08:18:22.864493+08:00
Source: user_input/follow_ups/202610.md — section 107

- 补齐12份完整公开音视频，合计4.27小时；本地实机参考19 → 112位，有音轨112位。
- 新增21个WC3音频候选；逐技能入口15条／实际不同短片12条。
- 修复自动章节错配与8位补充检索中的不可读版本说明；依据原始会话恢复105节损坏文字，未扩大授权。
- 核验1,732个已有WAV哈希；16份实机／录音及236份试听／短片完整解码、JS语法和本地路径检查通过。更新ZIP的CRC核对通过，共3267个条目。
- 仍缺逐技能原版声画验收、干净技能音轨及112位原版说话口型录像；新增网络音频未逐条听辨，无独立审稿／浏览器视觉实测。
- 独立Research库，未绑镜头参考；不改其他会话卡片、prompt和付费生成，不宣称全仓shot pack已检查。


## Follow-up 101 / 104 — 2026-10-24 — Tiny研究、五条720p与独立预审

新增16份公开图/动图，保留URL、SHA与版本边界；修复动画/头像同名下载冲突，16文件逐一核验。6.83d原地图Tiny实际技能列表核验后改人物/四技能卡，三轮prompt验证与独立复核；生成10秒亮相并抽正侧背及2.1秒声样，修正m4侧背抽帧，四技能资料包当前一致。

五条1280×720原片已落盘并打包，服务回执credit_count合计936。独立冷看认为前四条可带瑕疵review；长大首版约1.2–1.25倍、双目标被拳击带倒，两个blocker未清。第二版加自有构图参考、纯被动长大，通过prompt专项复核，但POST返回网络超时；ID7b88f90d-bdb7-4c16-8933-4710f96f2b15查询及list_task未给媒体/费用，费用未知，停止重提。Codex构图图费用未知。未删除原片、未对外发送或发布。

全部五条完整解码无错、源与交付SHA一致、ZIP CRC通过；三视图合图指纹及四技能资料包一致。每0.5秒及关键事件加密抽帧、独立冷看均有冻结证据；声音实际试听和正常速度完整播放未审，不宣称锁片或全质检通过。本剧没有episodes，本次shot_pack集镜头范围为空，只核四技能包；共用workflow/skill未改，不运行跨剧修复。审计 .audit/adhoc_agents/2026-10-23/tiny-five-videos/；交付 c2_Stone_Giant/demo/review_20261024/。

## Follow-up 096 — 2026-10-24 08:35:00

Source: user_input/follow_ups/202610.md - section 096
Summary: CM 四技能第二轮纠偏重出；k412–k414 初查通过，k411 杖头光束不通过待用户决定。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c41_Crystal_Maiden/skills/k411–k414 — 锁定段与 prompt 重写、死亡参考入包、新渲染与 review.md
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c41_Crystal_Maiden/README.md — 当前选择

No conflicts found in: 共用 skills / CONVENTIONS（未改）

## follow-up 113 — 2026-10-24

Summary: 自建 Suno API（127.0.0.1:8770）写进声音流程为默认入口，含 MCP 优先、服务没启动代理自启；全能骑士五条技能音效入队，等验证码解除。

Auto-updated:
- .agents/skills/ai-videos-pipeline/modules/sound.md、.agents/skills/suno-music/SKILL.md

## follow-up 114 — 2026-10-24

Summary: 树人死亡改成「生命力流失、苍老自裂」：全身多处参差龟裂、树皮翘起剥落，不是外力打断、不是一道线。先出 Codex 关键图 `frames/m1_Treant_death_5agedcrack_v1.png`（一次成功）：龟裂做到了，树皮偏灰、叶冠偏小；用户看图「可以」后出片 `renders/20261024_612206cb/`（72 积分）：龟裂、剥落做到了、一镜到底；站立时叶冠出画顶、倒下偏快。待用户看片。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/m1_Treant/death/ — 关键图 5、prompt、m1_Treant_death.md（111 版 prompt 存 `renders/20261024_aa156cf7/prompt.txt`）
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/m1_Treant/m1_Treant.md — 受击反应「倒地 / 死亡」


## Follow-up 116 — shared media references
Source: user_input/follow_ups/202610.md — section 116
Summary: 共享参考库前置到Claude/Codex入口，112位英雄新增本地ref索引。

Auto-updated:
- 本剧README、Research总览和六卷台词：加入当前参考库入口，纠正旧未下载／19位状态说明。
- shared_handoff.json、112位英雄ref/shared_media_refs.json：指向权威媒体清单、英雄定位、试听、声音可用性与待补项。
- 声音采样复核：374个网络候选中370个有有效采样，4个空或不足10毫秒；页面与清单已标不可用。全能索引的HolyBolt和PaladinDivineShieldDeath1有采样，DivineShield和ResurrectTarget仅有WAV头；均未作为具体DotA技能原版音轨验收。
- 更新音频可用性清单、播放器标记与离线包；保留原文件作为下载证据。

Validation: 112位英雄索引、900个目标路径通过；4个全能相关声音文件SHA256匹配，实际只有2个有声音采样；新版ZIP内9份核心清单与现文件一致。2761份音视频SHA256与此前完整解码时一致，媒体内容未变；JS语法通过。无生成卡片变更或新增镜头参考绑定，shot-pack同步范围为空。现有会话仍需重新读取共享入口，未声称已经自动刷新所有会话。

## 2026-10-24 — follow-up 117 冰霜新星开场图首帧重出 + CM 技能音效研究与排队

- k411：Codex 开场图 `planning/k411_seed_v9.png` 作首帧参考，卡片视频 prompt 改为从指向状态开始；新原片 `5e8f44b3`（168 积分）无光束，起爆晚且近；review.md、卡片「117 结果」、c41 README。
- 声音：`c41_Crystal_Maiden/ref/audio/research_117/`（盘点、测量、频谱图、结论）；四条 Suno Sounds 入队，服务验证码暂停未执行。

## follow-up 118 — 2026-10-24

Summary: Tiny 五条视频质量差，诊断（背对镜头、参考糊、山崩成圆球、结果太小）后按实机参考重写亮相与四技能 prompt，先出四张 Codex 开场构图图，五条 720p 重出。

Auto-updated:
- c2_Stone_Giant.md turntable 说明；skills/k21–k24 卡（Shot prompt 技能、峰值图状态、技能视频 prompt，k21/k23 锁定描述）与资料包；planning/k21/k22/k23_keyframe_v3.png、k24_keyframe_v3(b).png；ref/model/refs.md 实机复看节
- c2 README、本剧 README、demo/review_118_20261024/（六条副本与说明）、各条 renders/*/review.md、c2_Stone_Giant_turntable_review.md

Validation: skill_pack sync k21–k24 已更新；每秒抽帧看图；未试听、未独立冷看。


## 115 — 2026-10-24 — 地图分区与多机位资产

- 原管理站新增「地图资产」：8个大区、16个区域、64个机位；新增采用51张，复用13张远景。区域→bg主体→建筑/商人引用→机位层级保留既有编号与物理目录；新增bg40、bg41。
- 两方泉水区各3座固定建筑（含泉水）、8商人站位、5出生点；多余商店与出生圈经定点修正。全部86处基地实例通过编号引用原版布局唯一源，不另维护坐标副本。
- 主体/角度/数量代理初审绑定当前SHA；独立审稿未审。生成图为电影候选，分区边界、米制尺度与部分侧前机位属推定，不能当原版精确几何。
- 浏览器实际切换并解码64张、逐张点击下载64次且SHA一致；标记地图与两方坐标图下载一致。217个资料链接HTTP/内容检查通过；新增泉水卡图片点击7次通过；移动端无横向溢出、无JS错误。
- 前端相关9测试、导航20测试、生产构建通过。该剧无episodes，未改任何已用镜头的引用，shot_pack同步无适用目标。
- 审计：`.audit/adhoc_agents/2026-10-24/dota-map-regions/`；请求仍在剧background/request_log.md，未绕过审计入口。

## follow-up 119 — 2026-10-24

Summary: 树人死亡「始终保持全身」：关键图拉远出 `frames/m1_Treant_death_5agedcrack_v2.png`，改挂它再出 `renders/20261024_4d0ab372/`（72 积分）。远景全身基本做到（叶冠顶贴画面上边），龟裂同 114；倒下仍偏快。待用户看片。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/m1_Treant/death/ — 关键图 5b、prompt（机位远景全身、倒下放慢）、m1_Treant_death.md

## follow-up 120 — 2026-10-24

Summary: 用户定 `renders/20261024_4d0ab372/` 为树人死亡正式视频，复制为 `death/m1_Treant_death.mp4`（sha `0974cec8a073`）。截四格 `m1_Treant_death_sequence.png`；人物卡登记「死亡参考资产」，今后 demo 树人致死都挂；斧王已出版不改（k653 改后已恢复）。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/m1_Treant/death/m1_Treant_death.mp4、m1_Treant_death.md（正式版说明）
- ai_videos/dota_yingxiong/2_世界观人设/characters/death_assets.json — m1 stage / selected_video_file_exists / reference_assets
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/m1_Treant/m1_Treant.md — 死亡参考资产

- 2026-10-24 follow-up 121：地图页顶部加入完整原版地图红线分区与原图对照、代号图例、放大/下载；保留8大区16拍摄区层级。

## follow-up 159 — 2026-10-24

Summary: Tiny 四技能按用户新设计重做：全部致死（m4 死亡样板）、Tiny 与食尸鬼一般大、山崩胸口沙石洪流加眩晕标记、投掷竖直上抛砸地地裂、崎岖外表天降落石加巴掌、长大后一击致死；四条 720p 重出 696 积分。

Auto-updated:
- c2_Stone_Giant.md（体量、外观句、形态、技能画面概要、turntable 体量）；skills/k21–k24（159 当前设计节、Shot prompt、峰值图状态、技能视频 prompt、资料包、planning/*_keyframe_v4.png、renders 审阅）；c2 README；demo/review_159_20261024/；本剧 README

Validation: skill_pack sync k21–k24 已更新；每秒抽帧与关键段加密看图、ffmpeg 场景检测无硬切；未试听、未独立冷看。

- 2026-10-24 follow-up 163：泉水区生成俯视/原版截图以相同bg编号并排标注；展示当前布局差异，支持放大和资产卡跳转。

## 2026-10-24 — follow-up 122 / 124 CM 新星同步起爆、光环全屏、冰柱更猛

- k411：开场图 + 峰值图（Codex）挂参考，新原片 `80e66cfc`：指出与起爆同步、无光束，出手晚。
- k413 `92eb08bc`：光场铺满全屏；k414 `3f21599e`：冰柱更快更猛。卡片「122 / 124 结果」、review.md、c41 README。

## 2026-10-24 — follow-up 128 CM 新星开场即出杖、三层递进；大招冰柱不间断（待充值）

- k411 新开场图 / 三层峰值图（Codex），卡片改为 0.3 秒起爆、冰雹核 / 冰风刃 / 冰雾范围与持续递进；k414 改为 0.5 秒起冰柱与冰爆不间断、更密。
- 两条提交因即梦余额不足（136）被拒，未生成未扣费。

- 2026-10-24 follow-up 127：泉水俯视补齐7人形NPC＋1光团，生成6候选选择2张；32对象标注、原版坐标重绘与目标叠加已验。精确布局仍未通过，其他旧机位待布局更新。
- 补：新即梦账号出片 k411 `b6edbbe2`（同步起爆、三层递进）、k414 `6a69a0c7`（冰柱更密但晚到 4.8 秒）。

## follow-up 160 — 2026-10-24

Summary: 用户「全部」重出：Tiny 四技能按 159 审阅问题修 prompt，亮相按新体型重出；876 积分。山崩、长大修好，投掷小偏差，崎岖外表单块落石与巴掌连续两条未达成。

Auto-updated:
- skills/k21–k24（技能视频 prompt、Shot prompt、资料包、renders 审阅）；c2_Stone_Giant_turntable_review.md；c2 README；demo/review_160_20261024/；本剧 README

Validation: skill_pack sync 已更新；每秒抽帧与关键段加密看图、场景检测无硬切；未试听、未独立冷看。

## 2026-10-24 — follow-up 129 CM 新星一镜到底；大招开场即满屏冰柱冰雹

- k411 同机位峰值图 peak_v12 → `303a72f9` 一镜到底；k414 开场图 start_v12 → `84291627` 冰柱冰雹 0 秒起不停。review.md、卡片「129 结果」、c41 README。


## 2026-10-24 · follow-up 130 · 泉水通道与机位连续性

- 共生成14张版本候选，采用8张接入原management站点：两方俯视v1、远景v1、正面v2；近卫侧面选v1侧前方（5圈正确），天灾侧面v3标布局待核准（6圈，应5）。新图不覆盖历史文件。
- 两张俯视主代理检查：每方3建筑、7人形商人＋1光团、5圈，S1东/东北通路和D1西南大道贯通；高台/外围景观加强。所有派生视角的第一参考是各自新俯视，实际路径/SHA入清单。
- **未完成项**：天灾侧面出生圈多1个；近卫侧前方转角较浅；天灾正面远天光略暖。三轮侧面修订后按codex-imagegen规定停止，不把候选写成通过；独立审稿未审，未声称三维投影精确一致。
- UI保留原图并排与分类标注，32个新图标点重新定位；记录机位参考母图并显示过期提示。原版坐标图保留研究用途，当前美术图未作透视配准。
- 验证：12项相关前端测试、生产构建通过；实际浏览器两方8张机位解码/下载SHA一致、6个参考母图下载SHA一致，32对象分类与2组原图对照解码通过；手机无横向溢出，无JS错误。构建只有既有大chunk提醒。
- 本剧无episodes（已检查），shot_pack无适用同步目标。请求经审计入口，14个输出均在background/request_log.md中可追溯。本轮没有修改共用工作流/skill源，无目录同步目标。

## follow-up 161 — 2026-10-24

Summary: Tiny 四技能按用户看 160 后意见重出：山崩胸前凭空碎石墙、原版螺旋眩晕；投掷竖直出画再砸回；崎岖外表一块石头瞬间砸头；长大后快拳。696 积分，主要要求均做到。

Auto-updated:
- skills/k21–k24（prompt、资料包、planning 新图、renders 审阅）；ref/skills/（原版眩晕证据）；c2 README；demo/review_161_20261024/；本剧 README

Validation: skill_pack sync 已更新；抽帧看图；list_task 核对 k22 首次失败无任务后重提；未试听、未独立冷看。

## follow-up 125 — 2026-10-24

Summary: 沙王 c75 出全套：亮相 10 s 视频、三视图与声样；四技能按原版研究重写卡、Codex 峰值图、720p 技能视频（k751 重出一次）。共 1044 积分，待用户看片。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c75_Sand_King/c75_Sand_King.md — turntable 改 10 秒规格、技能概要、亮相制作记录
- ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c75_Sand_King/{c75_Sand_King_turntable.mp4,views/,source/}
- ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c75_Sand_King/skills/k751–k754 — 卡重写（旧卡 `_history/`）、`ref/refs.md` 与 `ref/research_125/`、峰值图、资料包、renders

## 2026-10-24 — follow-up 131 CM 新星冰雾加快；大招晴天无冰开场

- k411 `91a0a7d3`（冰雾仍到约 4 秒）；k414 晴天无冰开场图 + 同机位峰值图 → `d9ac1bfd`，另存剪头预览 `post/v131_trim/`。

## 2026-10-24 — follow-up 133 CM 大招只有食尸鬼变慢

- k414 卡片写明只有怪物前进变慢、禁止慢动作 → `bf28769a`；开场仍空等，剪头预览 `post/v133_trim/`。

## follow-up 134 — 2026-10-24

Summary: 沙王 k751 改为头朝一个方向笔直扎入、尖刺同向一排；k754 改为以他为中心 6 道间隔 0.5 秒、天崩地裂的大规模震荡波。两卡重写、两张峰值图重出（旧图 `_125` 退役）、两条视频重出（348 积分）。待用户看片。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c75_Sand_King/skills/k751_Burrowstrike/、k754_Epicenter/ — 卡、`_history/`、峰值图、资料包、renders

## follow-up 162 — 2026-10-24

Summary: Tiny 四技能按用户看 161 后意见重出：碎石直接瀑布奔涌、浅蓝白眩晕、投掷快上快下原地致死、崎岖外表拳头、长大快拳；投掷重出一次；共 1088 积分。

Auto-updated:
- skills/k21–k24（prompt、资料包、stun_swirl_v2_blue.png、renders 审阅）；c2 README；demo/review_162_20261024/；本剧 README

Validation: skill_pack sync 已更新；抽帧看图、场景检测（投掷首条检出 4.8 秒硬切）；未试听、未独立冷看。

## 2026-10-24 — follow-up 135 CM 大招法杖 45 度、开场不张臂

- k414 开场图 / 峰值图 v14 → `af73e947`：45 度对了，开场仍拖 2.4 秒；剪头预览 `post/v135_trim/`。

## follow-up 163 — 2026-10-24

Summary: Tiny 山崩/投掷/崎岖外表按用户看 162 后意见重出（高速碎石遮脚、淡透明眩晕、快抛快砸地裂）；504 积分；投掷原片空等改用本地剪辑版；长大 162 版通过。

Auto-updated:
- skills/k21–k23（prompt、资料包、stun_swirl_v3_pale.png、renders 审阅、k22 剪辑版）；c2 README；demo/review_163_20261024/；本剧 README

Validation: skill_pack sync 已更新；抽帧看图、场景检测（k22 2.75 秒、k23 3.67 秒硬切）；未试听、未独立冷看。


## 2026-10-24 · follow-up 136 · 泉水直通大本营

已按完整原版地图、全基地脚本坐标及地形高程重做：S1泉水向东北直接连接世界之树内庭，D1泉水向西南直接连接冰封王座广场。两张俯视母图同时呈现泉水角落、整段连接和古迹；六张其他机位都记录并使用相应母图作为第一参考。共生成14个版本候选，选用8张，旧山崖/长桥版本留档并标为历史。

原management站增加泉水→大本营说明、可展开的全基地坐标图、S2/D2邻区导航；保留原版截图并排，重新定位32个对象标注。S2/D2早期全景未重生成，标为旧布局待更新，避免冒充本轮对齐结果。

已核验：15项相关前端测试与生产构建通过；实际Chrome打开两方8张机位、逐张下载SHA一致，6个母图引用下载SHA一致；2张全基地坐标图解码及邻区导航成功；32对象筛选、原图对照、移动端无横向溢出，无JS错误。逐图主代理检查，所有选用图的出生圈为5个；天灾远景末圈间距偏宽，前/侧机位仍属斜俯，局部距离与附属装饰未达严格三维配准。独立审稿未审。

14个生成输出均通过审计入口写入background/request_log.md。本剧无episodes，shot_pack无适用同步目标；未改共用工作流或skill，无目录/入口同步目标。审计：`.audit/adhoc_agents/2026-10-24/dota-fountain-base-connection/`。

最终复核更正：D1俯视v2实际4圈，早先计数错误；最终采用v3补齐5圈。天灾三个派生机位实际参考仍是v2，保留真实路径/SHA；已逐图对照v3复核连接关系，复核记录同时绑定当前母图与机位SHA，任一更新即失效。近卫三个派生机位仍直接参考当前v1。出生圈标签边距及天灾北排商人标签已调整。最终截图、下载与机位复核显示均再次通过。

## follow-up 164 — 2026-10-24

Summary: Tiny 山崩（湍急碎石洪水、洪流中死亡）、投掷（一镜到底）、崎岖外表（去慢动作）重出；片长压到 8/6/7 秒逼节奏；396 积分，均无硬切。

Auto-updated:
- skills/k21–k23（prompt、片长、资料包、renders 审阅）；c2 README；demo/review_164_20261024/；本剧 README

Validation: skill_pack sync 已更新；抽帧看图、场景检测无硬切；未试听、未独立冷看。

## follow-up 137 / 138 — 2026-10-24

Summary: 沙王 k751 改为头正对敌人、尖刺约 0.1 s 冲顶、眩晕改浅蓝白旋涡圈（照魔兽 3 经典版截帧）；提交一次服务端 GenerateTimeoutFail，重提被新「出片前先审时间轴」必要流程拦下，时间轴表待用户认可。k754 改为砸地后不动、波自己发出 5 道约 0.5 s 间隔，重出 `541a3697`（168 积分）。四张卡视频 prompt 动作段改为逐行分秒格式。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c75_Sand_King/skills/k751–k754 — 卡、`_history/`、资料包、k754 renders

## follow-up 139 — 2026-10-24

Summary: 全能骑士技能音效试听后去掉 Suno 这一步；k31 改全景锁机位重出（a364e83c，用户接受）；k32 去背景音版；k34 109 版重试成功（cffb04a0）；全能骑士 demo v1 出片。

Auto-updated:
- c3_Omniknight/skills/k31_Purification、k32_Repel 卡（旧卡入 `_history/`）与资料包；k34 制作记录
- c3_Omniknight/demo/edit/final/ep01_final_v1.mp4、cut_v1.json

## 2026-10-24 — follow-up 140 CM 大招站姿起手、空中随机冰雾爆

- k414 开场图 / 峰值图 v15 → `871b0c7f`：站姿起手、冰柱更多、空中随机冰雾爆；冰柱约 3 秒才落、杖偏陡。

## follow-up 165 — 2026-10-24

Summary: Tiny 山崩（对准食尸鬼、贴地翻滚）、投掷（明显范围伤害与地裂）、崎岖外表（落石不规则、稍小）改 prompt；参考图网络失败未取得；提交被「时间轴先审」流程拦截，时间轴表待用户审阅，未扣费。

Auto-updated:
- skills/k21–k23（Shot prompt、技能视频 prompt、资料包）

Validation: skill_pack sync 已更新；skill_pack timeline 已出表；未提交。

## follow-up 144 — 2026-10-24

Summary: 沙王 k751 掘地穿刺：头扎进去到钻出来压到 1 秒内（1–1.9 秒），后续拍提前；时间轴指纹 338665ce99f5 待用户认可，未提交。

Auto-updated:
- c75_Sand_King/skills/k751_Burrowstrike/k751_Burrowstrike.md（旧卡 `_history/k751_Burrowstrike_card_137.md`）、资料包

## 2026-10-24 — follow-up 143 CM 大招冰柱必须落地、冰爆瞬间即散

- k414 卡：冰柱根根一口气砸进地里、空中不留冰柱；空中冰爆一闪炸开约 1 秒散成薄雾；画面只四只怪物。峰值图换同机位 `planning/k414_peak_v16.png`。时间轴指纹 `9cdcee542e79` 经用户认可 → `a99b12dc`（228 积分）：冰柱落地、冰爆瞬散达标；起手仍约 3 秒、杖偏陡、前排怪物冲近。用户「重出」→ 峰值图 v17 → `1730faf1`（228 积分）：杖约 45 度、怪物始终远离；怪物仍多于四只、死得偏晚。

## follow-up 146 — 2026-10-24

Summary: 用户认可沙王 k754 地震 138 版为现行版本；k751 时间轴仍待用户认可。

Auto-updated:
- c75_Sand_King/skills/k754_Epicenter/k754_Epicenter.md（状态、生成记录）
- 补：用户认可时间轴后提交三条，396 积分；renders 审阅、demo/review_125_20261024/、c2 README 已更新。

## follow-up 142 — 2026-10-24

Summary: 全能骑士 k34 无敌标记改为三个友军背后的大天使金色大翅膀，时间轴经用户认可后出片（ecce859a）；demo v2 换回 k32 完整原声、换上新 k34。

Auto-updated:
- c3_Omniknight/skills/k34_Guardian_Angel 卡（旧卡入 `_history/k34_Guardian_Angel_card_109.md`）、资料包、时间轴审阅与制作记录
- c3_Omniknight/demo/edit/final/ep01_final_v2.mp4、cut_v2.json

Validation: skill_pack timeline / approve（583147cbb8e9）后 submit；抽帧初审；demo v2 响度与静音检测。

## follow-up 147 / 148 — 2026-10-24

Summary: 全能骑士 k34 翅膀改为金光半透明光影翼、友军周身加金色符文光带；k33 减速光圈改为以骑士为中心向外荡开。两条时间轴待用户审阅，未提交。

Auto-updated:
- c3_Omniknight/skills/k34_Guardian_Angel 卡、ref/refs.md、资料包（旧卡 `_history/k34_Guardian_Angel_card_142.md`）
- c3_Omniknight/skills/k33_Degen_Aura 卡、资料包（旧卡 `_history/k33_Degen_Aura_card_098.md`）

Validation: skill_pack sync 两条均已更新；timeline 指纹 k33 `76383788362e`、k34 `36d6fc8e145e`。


## 2026-10-24 · follow-up 145 · 泉水五英雄活动空间

已扩大S1/D1泉水本地前庭，商人站位外移、中心留空、商店与泉水前沿留出通行空间；保持建筑/商人顺序和阵营内方位，出口仍直通世界之树/冰封王座。11张版本候选中采用8张：S1俯视/远景/侧前v1、正面v2；D1俯视v2、远景/正面v1、侧前v2。六个派生机位均以本轮最终俯视为第一参考，路径和SHA可追溯。

原management页面加入“五英雄活动空间”开关，H1–H5占位与选定连续净空叠加于当前俯视，原图对照保留；标注绑定当前母图SHA，换图后旧标注隐藏。32对象重新标点。五个活动占位均在空地内，互不重叠，并留有通过余量。30×24m前庭、18×14m净空、8m出口为提示词中的设计目标，未当作实测尺寸。

验收：逐图查看8张当前图，5出生圈、7人形商人＋光团和3建筑均保留；近卫正面商人误位已修正，天灾侧前图额外远城已去除。17项相关前端测试、生产构建通过；Chrome实际8张切换/解码/下载SHA核对，6母图引用、2组五英雄叠加/关闭、32对象筛选、全基地图与邻区导航、移动端无横向溢出均通过，无JS错误。构建仍有既有大chunk提醒。

限制：几何为电影化概念；正面/侧面仍有明显俯角，侧前转角较浅，未做精确3D碰撞或动态行走模拟，独立审稿未审。S2/D2旧全基地机位继续标为旧布局待更新。本剧无episodes，shot_pack无适用同步目标；未改共用工作流或skill源。11个生成输出全部通过审计入口，审计`.audit/adhoc_agents/2026-10-24/dota-fountain-capacity/`。

## follow-up 166 — 2026-10-24

Summary: 投掷 165 版用户选定；山崩（碎石密集无空隙贴地滚动）、崎岖外表（石头正中脑袋）经时间轴审阅后重出，276 积分。

Auto-updated:
- skills/k21、k23（prompt、资料包、时间轴审阅行、renders 审阅）；k22 165 版 review 标选定；c2 README；demo/review_166_20261024/；本剧 README

Validation: skill_pack sync / timeline / approve；抽帧看图、场景检测无硬切；未试听、未独立冷看。

## follow-up 149 — 2026-10-24

Summary: 用户认可沙王 k752 沙尘暴、k753 腐尸毒 125 版为现行版本。

Auto-updated:
- c75_Sand_King/skills/k752_Sand_Storm、k753_Caustic_Finale 卡（状态、生成记录）
- 补：用户认可时间轴后两条出片（k33 3eebdc41、k34 bbbdedb3）；demo v3 `ep01_final_v3.mp4`、`cut_v3.json`。

## 2026-10-24 — follow-up 150 水晶室女 demo v2

- 用户接受 k414 `1730faf1`。`c41_Crystal_Maiden/demo/edit/final/ep01_final_v2.mp4`（53.07 s）+ `cut_v2.json`：人物 turntable + k411 `91a0a7d3` / k412 `403f1ed4` / k413 `92eb08bc` / k414 `1730faf1`，结构同全能骑士 demo。待用户看。

## 2026-10-24 — follow-up 153 水晶室女 demo 定版与发布文案

- `ep01_final_v2.mp4` 定版（cut_v2.json）；新增 `c41_Crystal_Maiden/demo/publish.md`（六平台中英文案，格式同宙斯 / 斧王）。

## follow-up 167 — 2026-10-24

Summary: 崎岖外表 166 版选定；山崩碎石路径改为腹部→15度斜线→贴地滚动，经时间轴审阅后出片 144 积分，开头仍被开场图带成胸前悬飞，待重出开场图。

Auto-updated:
- skills/k21（prompt、资料包、时间轴审阅行、renders 审阅）；k23 166 版 review 标选定；c2 README；demo/review_167_20261024/

Validation: skill_pack sync / timeline / approve；抽帧看图、场景检测无硬切；未试听。

## follow-up 155 — 2026-10-24

Summary: 沙王 k751 掘地穿刺改为 4 根骨节弯钩尖刺、钻出时尖刺与半空树人仍在；时间轴指纹 97df416d47bb 待用户认可，未提交。

Auto-updated:
- c75_Sand_King/skills/k751_Burrowstrike/k751_Burrowstrike.md（旧卡 `_history/k751_Burrowstrike_card_144.md`）、资料包

## follow-up 168 — 2026-10-24

Summary: 山崩改用新开场图 v7（贴地高速石流），时间轴提速；用户授权免确认直接出，144 积分；贴地滚动达成，速度中等。

Auto-updated:
- skills/k21（prompt、开场图 v7、资料包、时间轴审阅行、renders 审阅）；c2 README；demo/review_168_20261024/

Validation: skill_pack sync / timeline / approve；抽帧看图、场景检测无硬切；未试听。


## Follow-up 152 — 2026-10-24 — 天灾NPC多轮冷看

Source: user_input/follow_ups/202610.md section 152

天灾D1四图更新为NPC动线v2：7人形商人＋1光团沿西北边缘，中央五英雄前庭和西南王座通路开放。共8张候选，选4张；三个派生角度真实引用最终俯视母图。三名独立审查者分别检查站姿、连续性与通行，发现并修复多出生圈、多光团、侧面楼梯朝向；主代理另修外围悬崖/海洋/桥。两组最终复审均无blocker，结论绑定四图SHA。保留正面第五圈间距偏大、局部箱桶差异、固定商店站姿和入口未细化等限制。

原management站Chrome核验通过：两区域8张图片切换/解码/下载SHA、6个真实母图引用、32对象分类、原图并排、两组五英雄叠加、全基地图及邻区跳转；移动端无横向溢出，无JS错误。已实际查看D1对照及五英雄叠加截图。S1及其余15区manifest内容保持不变；本轮未改UI代码。8张生成均在background/request_log.md可追溯。本剧无episodes，shot_pack无适用目标；未改共用工作流/skill。

Auto-updated: D1区域manifest、8商人标点、母图容量指纹、四机位卡与父卡、planning/npc_flow_review.json、本剧README。既有spec/validation中的地图分区功能无冲突，未触发完整阶段重跑。审计：`.audit/adhoc_agents/2026-10-24/dota-scourge-npc-review/`。

## follow-up 157 — 2026-10-24

Summary: 沙王 k751 加 Codex 同机位关键帧参考，尖刺改笔直骨节，树人不翻滚快速落地；时间轴 8f5b439737f7 待用户认可，未提交。

Auto-updated:
- c75_Sand_King/skills/k751_Burrowstrike/（keyframe 图、卡，旧卡 `_history/k751_Burrowstrike_card_155.md`、资料包）

## follow-up 151 / 156 — 2026-10-24

Summary: 全能骑士 k33 回到 098 版效果、涟漪从骑士脚下发出、最后一只转身逃、骑士盯敌人（7b24755a）；k34 骑士与树人都缠满金色符文带（借 Codex 收尾定格图作参考，d388c634）；demo v4。用户授权本轮不逐条确认时间轴。

Auto-updated:
- c3_Omniknight/skills/k33_Degen_Aura、k34_Guardian_Angel 卡、资料包、制作记录；k34_Guardian_Angel_peak_151.png
- c3_Omniknight/demo/edit/final/ep01_final_v4.mp4、cut_v4.json

## 2026-10-24 — follow-up 154 影魔 research（影压三连为重点）

- 新增 `c86_Shadow_Fiend/ref/skills/refs.md` 与抽帧拼图：DotA 1 影压是淡黄绿细光柱 + 根部黑影（非黑红火柱），三连压由远到近、间隔约 0.65 s；k861 卡已按用户所选「原版加强、远→中→近」重写，开场图 v3 / 峰值图 v2，时间轴 `237ade7062b2` 经用户认可 → `ac24b292`（168 积分，顺序反了、开场拖 4 秒）；c86 建立视频与三视图、声样已出。

## follow-up 158 — 2026-10-24

Summary: 全能骑士 demo v4 定版，写发布文案 `c3_Omniknight/demo/publish.md`。

## follow-up 169 — 2026-10-24

Summary: 山崩 168 版选定；按斧王 / CM 结构剪 Tiny demo 正片 v1（40 秒，亮相 160 + 山崩 168 + 投掷 165 + 崎岖外表 166 + 长大 162）。Tiny 线原 follow-up 119–128 与其他会话重号，重编为 159–168。

Auto-updated:
- c2_Stone_Giant/demo/edit/final/（ep01_final_v1.mp4、cut_v1.json、标题卡）；c2 README；k21 168 版 review 标选定；c2 下 49 个 md、审阅包目录 review_119…128 → review_159…168、本剧 README Tiny 段、follow_ups / revised_prompt / changelog 的 Tiny 条目编号（改前备份在 `.audit/adhoc_agents/2026-10-24/tiny-demo-169/`）

Validation: 抽帧看图、FFmpeg 完整解码、音量检测；编号重排后 follow_ups 无重复编号。未试听、未锁片。

## follow-up 172 — 2026-10-24

Summary: Tiny demo v2 转场放缓（段尾停 0.6 s、压暗转场 1.2 s、技能开头定格 0.5 s 先出标题卡），43.5 秒；只剪辑、不重出。

Auto-updated:
- c2_Stone_Giant/demo/edit/final/（ep01_final_v2.mp4、cut_v2.json）；c2 README；本剧 README

Validation: 抽帧看转场、FFmpeg 完整解码。未试听、未锁片。

## follow-up 173 — 2026-10-24

Summary: 沙王 k751 变速版减速：另出 2.6 倍、2 倍两档（本地，不收费），待用户选。

Auto-updated:
- c75_Sand_King/skills/k751_Burrowstrike/k751_Burrowstrike.md（生成记录）

## follow-up 174 — 2026-10-24

Summary: Tiny demo v3：正片原速完整、不叠化，只在段尾加末帧停留、段前加首帧定格（渐黑/渐亮与标题卡都在加出来的时间里），50.95 秒。

Auto-updated:
- c2_Stone_Giant/demo/edit/final/（ep01_final_v3.mp4、cut_v3.json）；c2 README；本剧 README

Validation: 抽帧看转场、各段正片时长对照原片、FFmpeg 完整解码。未试听、未锁片。

## follow-up 175 — 2026-10-24

Summary: 沙王 k751 树人改为被弹飞到空中再落地、尖刺快出快收；关键帧 v3；按用户授权免确认重出。

Auto-updated:
- c75_Sand_King/skills/k751_Burrowstrike/（keyframe 图、卡，旧卡 `_history/k751_Burrowstrike_card_157.md`、资料包）


## Follow-up 171 — 2026-10-24 — 默认俯视与全区原图

已将区域默认机位与区域切换重置为俯视；大区标题可直达首个区域。全部16区新增原图tab，远景/俯视/正面/侧面默认并排显示本区原图，支持关闭并排、单看原图、来源与下载、完整6.83d地图定位。9区用游戏截图（7张独立来源；M1/M2/R2共用中路坡道参考），7区用2009年6.60之后旧版地貌局部；旧版、非同机位、一塔全景未覆盖等限制均显式标明，不能冒充16区6.83d高清实机齐全。原版源全部本地保存，来源与SHA记在map_regions/original_references.json。

Auto-updated: MapRegionsPage、RegionOriginalPanel、mapRegions解析、页面CSS和测试；map_regions.json及来源清单；README、项目spec/验收。独立interview/findings无本次冲突，未重跑完整阶段。验证详情见 `.audit/adhoc_agents/2026-10-24/dota-region-originals/verification.json`。

## follow-up 179 — 2026-10-24

Summary: Tiny demo v3 用户定版锁片，写发布文案 publish.md。

Auto-updated:
- c2_Stone_Giant/demo/publish.md（新）；demo/edit/final/cut_v3.json status；c2 README；本剧 README

Validation: 时间点按 cut_v3.json 段起点核对；封面帧看图确认。声音未人工试听（publish.md 已提示）。


验证：19项相关前端测试、TypeScript与生产构建通过（仅既有大chunk提醒）；Chrome逐区验证16区默认俯视、64机位解码、16原图链接及SHA、来源文档、原图tab、并排切换、完整地图定位、浏览器后退与大区标题选择；无JS错误，390px移动端无横向溢出。实际查看上路/中路对照与移动端截图。现有生成图、标注与五英雄空间数据未变。本剧无episodes，shot_pack无适用目标；未改共用工作流/skill。

## follow-up 180 — 2026-10-24

Summary: 5 个 demo publish.md 的 YouTube 标题统一为「DotA X in Live Action – 另一名」格式；今后新 demo 沿用。

Auto-updated:
- c65_Axe、c2_Stone_Giant、c3_Omniknight、c40_Lord_of_Olympus、c41_Crystal_Maiden 的 demo/publish.md（YouTube Title）

Validation: 名称对照研究表；每个文件旧标题恰好一处被替换。

## follow-up 181 — 2026-10-24

Summary: 用户认可沙王 k751 175 版；沙王 demo v1（47 s，照宙斯 v2 结构）与 publish.md 已出，待用户看。

Auto-updated:
- c75_Sand_King/skills/k751_Burrowstrike/k751_Burrowstrike.md（状态、生成记录）
- c75_Sand_King/demo/edit/final/（ep01_final_v1.mp4、cut_v1.json、title_card_k751–k754_en.png）、c75_Sand_King/demo/publish.md

## follow-up 182 — 2026-10-24

Summary: 用户指出沙王尾巴没有针；Codex 出带毒针的立绘候选，待用户看图后再整套重出。

Auto-updated:
- c75_Sand_King/c75_Sand_King_stinger_v1.png（候选）

## follow-up 184 — 2026-10-24

Summary: 沙王毒针改为向内蜷的钩，立绘候选 stinger_v2，待用户看。

Auto-updated:
- c75_Sand_King/c75_Sand_King_stinger_v2.png（候选）

## follow-up 185 — 2026-10-24

Summary: 开始混沌骑士 c60：技能原版 research（进行中）；建立视频按 16:9 / 10 秒样板重写并出片（即梦 7d91193b，180 积分），抽三视图与声样。

Auto-updated:
- c60_Chaos_Knight/c60_Chaos_Knight.md（turntable 节；旧卡备份 `.audit/adhoc_agents/2026-10-24/ck-research/c60_Chaos_Knight_before.md`）
- c60_Chaos_Knight/c60_Chaos_Knight_turntable.mp4、views/（front/side/back/views/audio/source.json）

Validation: 0.5 s 接触表与候选帧看图；未试听、未锁片。

## follow-up 187 — 2026-10-24

Summary: 沙王换内蜷毒针立绘，五张卡改尾巴写法，亮相视频重出已提交，四张技能参考图改尾巴，四条时间轴待用户认可。

Auto-updated:
- c75_Sand_King/（立绘、人物卡、source/turntable_prompt_184、skills/k751–k754 卡与参考图、资料包）

## 2026-10-24 — follow-up 183 影压三连跟着敌群推进、影魔更高大、影压音效

- k861 卡：三发改为敌群推进中远 → 中 → 近依次打死三波；光柱改细高椭圆光环；开场图 v5 / 峰值图 v3；时间轴 `1c1e12933044` 待审。
- 影压音效：原片只作测量；Suno Sounds 2 条、MOSS 24 条、本地合成 3 条，频谱对比后都未达到「很像」，试听页待用户定。

## follow-up 189 — 2026-10-24

Summary: 沙王 demo v2：新亮相 + 四条旧技能条，待用户看。

Auto-updated:
- c75_Sand_King/demo/edit/final/（ep01_final_v2.mp4、cut_v2.json）

## follow-up 190 — 2026-10-24

Summary: 沙王旧技能条作参考视频换内蜷毒针造型，k753 先试一条。

Auto-updated:
- c75_Sand_King/skills/k753_Caustic_Finale/renders/（试条，待出）
- follow-up 183 续：影压音效改为 DotA 1 版（wc3.ninja shadowraze 候选），按用户书面决定本地克隆 `sfx/clone_v1/`，试听页 `listen_v2.html` 待检查。
- follow-up 183 续：用户确认 E（TM 0:34 实机三连压）为影压原声，本地克隆单发 / 三连 `sfx/clone_v2/`，待检查。
- follow-up 183 续：k861 `5c36b9cf`（168 积分）光柱与体型达标、只出两发；带克隆音效版 `post/sfx_183/`。

## follow-up 185（续）— 2026-10-24

Summary: c60 技能原版 research 完成；用户选四技能方向；k601–k604 技能卡重写；k601 开场图出成，其余图因 Codex 网络失败待补。

Auto-updated:
- c60_Chaos_Knight/ref/skills/（refs.md、4 张拼图）；skills/k601–k604/*.md；k601_Chaos_Bolt/planning/k601_start_v1.png

Validation: 拼图与开场图看图核对；时间轴未跑（缺参考图）；未出片。

## follow-up 191 — 2026-10-24

Summary: 沙王 demo v3 定版锁片，publish.md 按 v3 更新（毒针尾、封面 0:30）。

Auto-updated:
- c75_Sand_King/demo/edit/final/cut_v3.json（锁片）、c75_Sand_King/demo/publish.md、人物卡与 k751–k754 卡状态行
- follow-up 183 续：k861 `683b936b`（168 积分）三发齐（1.7 / 4.0 / 5.3 s），带克隆音效版 `post/sfx_183b/`。

## follow-up 192 — 2026-10-24

Summary: 狼人 c61 补下载 DotA 1 / 魔兽 3 原图，外观按 2002 原模型 × 品红染色重写，Codex 重出立绘，待用户看。

Auto-updated:
- c61_Lycanthrope/ref/model/（20 张新原图、refs.md、compare_202610_c61.jpg）、c61_Lycanthrope.md、c61_Lycanthrope.png（旧版 _066）

## follow-up 185（出片）— 2026-10-25

Summary: c60 开场 / 峰值图 8 张出齐；四技能时间轴按用户认可提交，720p 四条出片；建立视频 + 四技能共 780 积分；审阅包与 c60 README。

Auto-updated:
- c60_Chaos_Knight/skills/k601–k604/（planning/、资料包、renders/、卡内时间轴审阅行）；demo/review_185_20261025/；c60 README；本剧 README

Validation: 每条抽帧看图初审（review.md）；未试听、未独立冷看、未锁片。


## 2026-10-25 · follow-up 186 · 原版通行研究

完成6.83d静态地图研究、16区左右标注/约束与现有站点导航检查；24项测试、构建和16区浏览器验证通过。20张地形出图均未获路线母图批准，返工对照可看，电影配准/实机碰撞仍未完成。见本条follow-up及navigation/research.md。

## 2026-10-25 — follow-up 194 影压改黑色暗影柱、三发远中近各打死一波

- k861 卡：黑色暗影柱（无发光轮廓），三发 14 / 9 / 4 m 各打死一波，声音去爆炸；参考三张事件图 far / mid / near v2；新时间轴待审。原生为主的混音 `post/sfx_194/`。


## 2026-10-25 · follow-up 195 · 最新布局直接参考修订

按当前项目最新6.83d静态导航研究，生成16区自绘布局参考，直接输入S1/D1/T1/R2重出v3四张（审计入口留痕）。四张及其四份参考均已独立冷看并绑定SHA；累计24张导航候选审查，路线母图批准仍为0。S1宽坡道仍被桥式通道及树台挤占；D1把南端bg30埋骨地画成王座式建筑；两基地7人形NPC＋1精灵均未验明；T1/R2仅可供有限美术参考。五出生圈各可数到5个，但五英雄净空未验证。

原management站已展示v3候选、原版标注对照、实际输入布局图和独立拒绝原因；新增“蓝色仅为低地，不等于水域”说明。其他12区候选、地图几何与64个正式角度没有被替换；其余12区布局图已准备，尚未直接参考重出。现有多角度图未按新布局完成空间配准。

本轮实际prompt错误（低层误等同水、D1裁切外Ancient未清楚限定）已在research.md如实记录，不事后改写已提交prompt。关键四区累计三轮仍不合格，按codex-imagegen skill停止同类重抽；遵用户不提问授权，自主保留待返工状态，后续应优先统一地形、建筑和NPC的三维坐标再出机位。没有将审查失败的图晋升正式路线母图。

验证：24项相关前端测试、TypeScript和生产构建通过（仅既有bundle尺寸提醒）。浏览器实际核验结果见本次audit/browser_verification.json。本剧无episodes，shot_pack无适用目标；未改共用工作流/skills，无对应目录同步。审计目录：.audit/adhoc_agents/2026-10-25/dota-latest-layout-revision/。整体状态为已复审、未全部修妥，水位/实机碰撞与镜头配准仍未完成。

补充显示修复：实际截图发现候选图超出左右对照列，已限制图片列宽，手机端保持完整缩放；重新构建并用图片/figure实际边界验证，见本次audit/visual_bounds_verification.json。

## follow-up 193 — 2026-10-25

Summary: 狼人 c61 10 秒亮相 02476c76（180 积分）装为 `c61_Lycanthrope_turntable.mp4`，三视图与声样已截；四技能 DotA 1 原版研究完成（召狼身前烟球、嗥叫脚下品红旋涡 + 头顶鬼脸、野性驱使无特效、变狼品红闪光 + 梅紫狼），技能卡待改。

Auto-updated:
- c61_Lycanthrope.md（turntable 段、人物亮相制作记录）、c61_Lycanthrope_turntable.mp4、source/、views/、skills/k611–k614/ref/

## follow-up 196 — 2026-10-25

Summary: 狼人 c61 去掉头后翼尖：Codex 以现行立绘为参考只删翼，出候选 `c61_Lycanthrope_nowing_196.png` 与对比图 `compare_wings_196.jpg`，待用户定；未换立绘、未改卡。
- follow-up 194 续：k861 `3fc3fc23`（168 积分）黑色影压远中近三发各打死一波；带音效版 `post/sfx_194b/`。

## follow-up 185 续 — 2026-10-25（看首版后改卡）

Summary: 混沌骑士四技能按用户反馈改卡：k601 暗红不规则碎刃直线强命中、射程约 18 m；k602 起始约 20 m、神秘力量把两人硬拖到一起；k603 暴击砸中时暗红光壳包裹树人；k604 四个分身从本体同时分出、分出瞬间暗红幻影重影。尸体描述改按尸体图。新开场/峰值图 6 张（Codex）；新时间轴待审，未出片。

Auto-updated:
- c60_Chaos_Knight/skills/k601–k604 卡（首版卡备份 `.audit/adhoc_agents/2026-10-25/ck-revise/before/`）、planning/*_v2.png


## follow-up 197 — 2026-10-25 14:07:56

Source: user_input/follow_ups/202610.md — section 197

Summary: Treant c1 按经典原版动图、头像与暴雪官方模型图重研；三轮Codex新图，v5换为当前候选，待用户看。

Auto-updated:
- `c1_Treant_Protector/ref/model/refs.md`、D02 §1 — 区分据图事实和电影化设计，纠正仅看绿色占比漏查轮廓的旧判断。
- c1人物卡 — 宽厚前弓树体、宽木脸、大片木质前臂、簇状鲜绿叶片、粗根腿；立绘4:5；保留原图 `c1_Treant_Protector_v2_pre197.png` 与三轮候选。
- 4张技能卡 — 旧峰值图造型已过期，标待更新，本轮未重出技能图或视频。
- 当前立绘SHA `bd3f76599db96262aa66c2a88444c6f778765eef6ae213a16ea55b8d5620752c`；代理看图记录 `.audit/adhoc_agents/2026-10-25/treant-research/review_v5.json`；未获用户确认、未作独立终审。图像型号与费用未知，未上传原版版权图。

验证：PNG读取／SHA／请求前日志与结果关联、卡片代码围栏和4项下游待更新标记已检查。本剧没有episodes，shot_pack无适用目标；共用工作流与skills未修改，无目录或薄入口同步任务。其他会话原有改动保留。

197验证补充：管理页面实际图片接口 `/api/media` 返回PNG，SHA与当前v5一致；`/file/`返回HTML是正常前端路由。v5眼球小瞳孔、鼻部拟人细节和钝木指仍存在，三轮后交用户看，未宣称完全复原。

## follow-up 199 — 2026-10-25

Summary: 狼人 c61 用户指出头后尖片是披风上的突起而非翅膀；Codex 出候选 C `c61_Lycanthrope_capepeaks_199.png`，三图对比 `compare_wings_199.jpg`，待用户定；未换立绘、未改卡。

## 2026-10-25 — follow-up 201 影压施法双手从正下方抬起、只有被击中的倒下

- k861 卡：施法改双手从正下方抬起；只有被黑烟罩住的树人倒下，倒下不爬起；时间轴 `a3a6117dad4f` 待审。

## follow-up 202 — 2026-10-25

Summary: 狼人 c61 披风上沿折角尖片改紫色，候选 D `c61_Lycanthrope_capepeaks_purple_202.png`，四图对比 `compare_wings_202.jpg`，待用户定；未换立绘、未改卡。
- follow-up 201 续：k861 `f4c5e91e`（168 积分）死亡规则达标，但三发成近→中→中。
- 续：第二版四条出片 k601 `6a189a7b`、k602 `d76eda16`、k603 `cc96914b`、k604 `fd06df9a`（共 600 积分；k604 首提 `28a89e25` 生成阶段明确失败后重提）。k604 分身特效按用户改为不发光的原色残影加颤动（峰值图 v4）。审阅包加 02b–05b。
- follow-up 201 续：k861 `329802f3`（168 积分）只出两发、仍握拳。

## Follow-up 203 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 203
Summary: 地图区域复核：S1 按原版高一层台地＋东北坡道在 Blender 搭技术布局并重出四机位（两轮独立冷看：正面通过、侧面有条件、俯视仅作布局地图、远景未通过）；T1/J2/K2/R1/R3 按脚本地标坐标重定位；管理站坐标俯视改真实比例并加布局底图。

Auto-updated:
- ai_videos/dota_yingxiong/0_research/map_regions/map_regions.json — S1 四机位、对照标注、布局底图、五英雄空间；T1/J2/K2/R1/R3 位置与窗口
- ai_videos/dota_yingxiong/0_research/map_regions/navigation/ — T1/J2/K2 约束、裁图、导出、布局参考与 navigation.json 条目
- ai_videos/dota_yingxiong/0_research/map_regions/blender/ — region_blockout.py、annotate_layout.py、S1.json（新增）
- ai_videos/dota_yingxiong/0_research/map_regions/regions_overview_red.{svg,png} — 按新位置重渲
- ai_videos/dota_yingxiong/2_世界观人设/background/近卫_sentinel/bg13_近卫泉水与商店/ — 新卡节、_blender/、新机位图与 prompt
- projects/ai_video_management/apps/ui — RegionObjectDiagram 真实比例与底图、机位布局渲染链接、新状态标签、测试

No conflicts found in: shared skills / workflow catalog（未改共用源）
- 续：看第二版——k603 用户认可定版（cc96914b）；k601 弹道改为带弧度、随机拐弯；k602 改为一瞬间扯到一起；k604 残影加颤动缩到 0.5–1 秒，分身音效写清楚。k601、k602 峰值图重出；新时间轴待审。

## 2026-10-25 — follow-up 204 影压三发 4 秒内打完、用确认的原声

- 开场图 v6（树人更近）；时间轴 `28d6043ce8b9` 待审；声音试听 `post/sfx_204/`（克隆原声清楚、原生让位）。

## follow-up 205 — 2026-10-25

Summary: 狼人 c61 头侧紫色尖片改为肩胛后方从肩板后缘立起的紫甲片，候选 E `c61_Lycanthrope_shoulderpeaks_205.png`，五图对比 `compare_wings_205.jpg`，待用户定；未换立绘、未改卡。

## follow-up 206 — 2026-10-25

Summary: 狼人 c61 用户选 E：立绘换为肩板后缘紫甲尖片、无翅膀版（sha 53055d08514c，旧版 `_192.png`），人物卡翼相关描述与负向全部改写，亮相 prompt 206 待用户点后重出。

Auto-updated:
- c61_Lycanthrope.md（193 版存 `_history/`）、c61_Lycanthrope.png、source/*_prompt_{196,199,202,205,206}.txt


## follow-up 207 — 2026-10-25 15:28:01

Summary: 用户否定197版Treant造型，撤下v5，恢复066旧图仅作占位；撤回197版卡内结构改写，候选及审计保留。原版直传生成参考的授权正在询问中，未生成新图。

Auto-updated: c1人物卡、ref/model/refs.md、D02 §1、当前PNG、follow-up与revised_prompt。4张技能图继续待更新。本剧无episodes及shot_pack适用目标。
- follow-up 204 续：k861 `a2c31f19`（168 积分）只出两发、近→中。

## Follow-up 208 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 208
Summary: 野区拆成12个营地点位区（标清组合与建议默认），肉山、神符、商店、中路一塔等点题区域对准点位并收窄到一屏，28区各出一张原版数据三维布局图。

Auto-updated:
- ai_videos/dota_yingxiong/0_research/map_regions/map_features.json（新增，build_map_features.py 生成）
- ai_videos/dota_yingxiong/0_research/map_regions/map_regions.json — 28区（新增 J3–J8、K3–K8；R1/R2/R3/R4/J2/K2/T1/B1/M1/M2/J1/K1 窗口与位置；全区「布局图」机位）
- ai_videos/dota_yingxiong/0_research/map_regions/navigation/ — 24区约束、裁图、导出与 navigation.json
- ai_videos/dota_yingxiong/0_research/map_regions/blender/ — regions_layout.json、region_blockout.py（区域相机、点位标注）、annotate_layout.py
- ai_videos/dota_yingxiong/0_research/map_regions/layout/ — 28张布局图及标注、projection
- ai_videos/dota_yingxiong/0_research/map_regions/regions_overview_red.{svg,png}
- ai_videos/dota_yingxiong/0_research/parts/d01_版本与地图.md §5.1 — 营地归属与池子已核实

No conflicts found in: shared skills / workflow catalog（未改共用源）
- 续：第三版 k601 `3a48b819`、k602 `d781f1c2`、k604 `604539fb`（456 积分）；k603 第二版定版；审阅包加 02c、03c、05c。
- 续：看第三版——k601 碎刃一瞬间飞到、前端钝；k602 加响亮「嗖」声；k604 分身弹射加快。k601 峰值图 v4；新时间轴待审。

## 2026-10-25 — follow-up 210 影压三连 Blender 白模预演

- `k861_Shadowraze/previz/k861_previz_v1.mp4`（远中近 1.0 / 2.0 / 3.2 s）作为参考视频挂进卡；时间轴未变。
- 续：第四版 k601 `127c4582`、k602 `e1a8ee04`、k604 `c5bf34b9`（456 积分）；审阅包加 02d、03d、05d。
- follow-up 210 续：k861 `56f9a53b`（240 积分）挂白模后仍只两发。

## Follow-up 212 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 212
Summary: 骷髅王重新 research：地图七个官方版本 NC00 数据 + 6.83d 实机截图，确认借骷髅战士模型但整模 1.8 倍、灰白青绿单色调、盾面骷髅纹章；旧通用骷髅 refs 移出；卡与武器描述改写，未出新图。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c62_Skeleton_King/c62_Skeleton_King.md、ref/model/refs.md 及新增 6.83d / v6.90a8 实机裁图
- ai_videos/dota_yingxiong/2_世界观人设/props/天灾_scourge/p75_c62_Skeleton_King_Weapons/p75_c62_Skeleton_King_Weapons.md
- ai_videos/dota_yingxiong/0_research/parts/d05_天灾力量英雄.md §外观更正

No conflicts found in: shared skills / workflow catalog（未改共用源）


## 2026-10-25 — 影压三连改关键帧分段出片

- 五张关键帧（开场 v6 / 远 / 中 / 近 / 收尾 end_v1）+ multiframe2video；过渡表待审。
- 续：看第四版——k601 改为一串跳跃的暗红弹珠；k602 加吸力段，贴上后直接砸锤；k604 改为一共 4 骑，先原地分身再分头冲锋，树人 4 个。新开场图/峰值图出图中；新时间轴待审。
- follow-up 212 续：用户确认 6.83d 造型；Codex 重出 p75 与 c62 立绘（各 1 次，费用未知），初审通过；k621–k624 外观句同步；视频未提交。

## Follow-up 217 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 217
Summary: demo 出片标准：新出亮相 12 秒；技能条按需定长，出片时开头、结尾各留 1–2 秒起势 / 收势；成片能过 1 分钟最好、不强求；剪辑不定格、不加钩子 / 速览。

Auto-updated:
- ai_videos/dota_yingxiong/demo_standard.md — 新建
- ai_videos/dota_yingxiong/README.md — 标准入口，取代亮相 10 秒旧规格
- c41_Crystal_Maiden/demo/edit/final/cut_v3.json、cut_v4.json — 样片作废（v2 仍定版）
- 续 2–4：成片目标改为超过 60 秒；转场改为不重叠压暗（渐黑 0.4 s + 渐亮 0.4 s）；已定版 demo 按用户要求逐个重做。冰女亮相重出 12 秒（用户认可）；k411_Crystal_Nova.md 改 13 秒（起势 / 收势），新开场图 `planning/k411_start_v13.png`，时间轴 `88d377c1e036` 用户认可后提交
- 续 6：k411 新条 `3aecf4db`（13.06 s）+ review.md；冰女 demo `cut_v5.json` / `ep01_final_v5.mp4` 65.4 s，用户「可以」定版（续 7），取代 v2；c41 卡「demo 时长预算」
- 续 5：四个技能条合计 ≥ 53 s 为硬要求（成片 ≥ 65 s），代理分配时长、预算写进英雄卡；原片不够时每条首尾各加 0.5 s 停顿补足，再不够加长重出（demo_standard.md §1 / §3、README 入口）

No conflicts found in: shared skills / workflow catalog（未改共用源）


## 2026-10-25 — follow-ups 198 / 200 / 209 / 218 — Luna 技能重出（k232 / k233 / k234）

- k234_Eclipse.md — 第六轮锁片作废；第七轮关键帧（猫头鹰全程在头顶、光柱带月光鸟）与四段 Seedance 成片、独立审稿不通过；2 倍速版
- k232_Moon_Glaive.md、k233_Lunar_Blessing.md — 改回纯 Seedance（第十 / 十一、十一 / 十二轮），独立审稿均不通过（挨打后直立）
- follow_ups/202610.md — 198、200、209、218；218 记录对齐 217 新 demo 标准（起势 / 收势各 1–2 秒、活的预备动作、不在剪辑里凑）

No conflicts found in: demo_standard.md（Luna 尚未进剪辑）、shared skills / workflow catalog（未改共用源）

## follow-up 220 — 2026-10-25

Summary: 狼人 c61 亮相 prompt 按 demo_standard 改 12 秒（1.5 s 起势 / 2.5 s 收势），待用户点后出片。

## follow-up 185 续 — 2026-10-25（对齐 217 demo 标准）

- c60_Chaos_Knight/skills/k601_Chaos_Bolt、k602_Reality_Rift、k604_Phantasm 卡：动作分秒加起势 / 收势，时长 10 / 10 / 12 秒，峰值图时刻后移；状态行注明待时间轴审阅
- follow_ups/202610.md、revised_prompt.md — 185 下加「对齐 demo 新标准」一节

No conflicts found in: demo_standard.md（CK 尚未进剪辑）、k603 定版与亮相（不重出）

## 2026-10-25 — follow-up 211／214／215 树精卫士重研、加壮、定稿与亮相

- 211：取得暴雪 2000 年 WC3 远古守护者原版概念图，经用户许可上传原版参考出图（v6–v9）；`c1/ref/model/refs.md` 加新证据节。
- 214：用户要「再壮一点」，v10／v11。
- 215：定稿 v10 为主立绘，卡片外观各段重写；亮相 submit `16b6bf7f`（10 s，旧规格）已补收待看；卡里亮相 prompt 已按 217 改为 12 秒，未重提。技能卡与峰值图仍为旧外观。
- follow-up 219：k861 multiframe2video `76ba2bf1`（18 积分）三发远中近 4 秒内首次达标，有火团 / 变形 / 第四根柱等缺陷。共用规则 assets.md §技能加「首尾留白」。

## Follow-up 216 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 216
Summary: 地狱领主 c63 validate＋出片：补 p76 武器并挂武器重出立绘；亮相 12 s 出片（`383f1f3d`，216 积分）并抽三视图与声样；四技能原版 research，按用户选方向重写 k631–k634 卡、出开场 / 峰值图；技能时间轴待审，未提交技能视频。

Auto-updated:
- c63_Lord_of_Avernus/（人物卡 turntable 段与制作记录、立绘、turntable.mp4、views/、README.md、ref/skills/、skills/k631–k634 卡与 planning/、资料包）；旧卡备份 `.audit/adhoc_agents/2026-10-25/c63-avernus/`
- props/天灾_scourge/p76_c63_Lord_of_Avernus_Weapons/（锚点图）；characters/weapon_assets.json（c63 行）

Validation: 武器、立绘、开场 / 峰值图与亮相接触表主代理看图初审；亮相声音未试听、未独立冷看；本剧无 episodes，shot_pack 无适用目标；未改共用 skills / workflow catalog。
- 215 续：用户选 12 秒，亮相重出 submit `3e7236f8`（216 积分），旧 10 秒版（180 积分）移入 `_deleted/`。

## Follow-up 223 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 223
Summary: 骷髅王致死打击加「被暴击目标全身披暗红」；重生减速改为骨堆震开的暗红地面震波，扫到的周围敌人全部减速。

Auto-updated:
- c62 skills k623_Mortal_Strike.md、k624_Reincarnation.md 及资料包

No conflicts found in: shared skills / workflow catalog（未改共用源）
- follow-up 219 续：三条 multiframe 变体（60 积分）三发都对，收势段黑柱重现。

## 2026-10-25 — follow-up 226 影压回到 Seedance、加起势收势

- k861 卡 11 秒（起势 1.5 s / 三发 / 收势 2 s），时间轴 `2490d7a080db` 待审。

## follow-up 185 续 — 2026-10-25（第五版出片）

- k601 / k602 / k604 第五版 approve + submit（528 积分），各 renders 目录 review.md；审阅包 02e / 03e / 05e 与 README；三张卡状态行
- follow-up 216 续：时间轴经用户认可，c63 四技能 720p 出片 k631 `8315dfdd`、k632 `c62a4d79`、k633 `bfb7c230`、k634 `87030d39`（共 690 积分）；每条抽帧初审写 renders/*/review.md；未试听、未锁片。

## Follow-up 228 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 228
Summary: 骷髅王四技能合计 53 秒（13 / 13 / 13 / 14），每条首尾各 0.5 s 停顿；时间轴待用户审。

Auto-updated:
- c62 skills k621–k624 卡「技能视频 prompt」时长与动作分秒及资料包

No conflicts found in: shared skills / workflow catalog（未改共用源）

## follow-up 185 续 — 2026-10-25（看第五版后改，四技能合计 53 秒）

- k601 改笔直暗红飞弹 12 秒、k602 改瞬间传送 13 秒、k604 锁四骑 20 秒（加结尾参考图），k603 定版 8 秒；剪辑首尾 0.5 秒停顿为本英雄用户特许后备
- follow_ups/202610.md、revised_prompt.md — 185 下加「看第五版反馈」

No conflicts found in: demo_standard.md（未改共用标准，53 秒与 0.5 秒停顿仅记于混沌骑士）

## 2026-10-25 — follow-up 230 luna-skills-53s
- Luna 四技能按合计 53 s 重分：k231 11 s / k232 12 s / k233 14 s / k234 16 s，各一段 Seedance 2.5 frames2video；k231 加台词 "Plead your innocence!"；k234 光柱间隔约 2.3 s
- 卡片「技能视频 prompt」更新；脚本 `.audit/adhoc_agents/2026-10-25/luna-sfx/make_53s_round.py`
- follow_ups/202610.md、revised_prompt.md — 加 230
- 0.5 秒首尾停顿仅为本英雄后备，未改 demo_standard.md

Source: user_input/follow_ups/202610.md - section 229
Summary: 影魔四技能合计 53 秒（k861 11 / k862 14 / k863 13 / k864 15）；k861 时间轴认可后出片 11d4fb4f，只有两发，未达标。

Auto-updated:
- c86 人物卡新增「demo 时长预算」
- k861 卡 229 结果节、renders/20261025-194529_11d4fb4f/review.md

No conflicts found in: shared skills / workflow catalog（未改共用源）

## 2026-10-25 — follow-up 231 lycan-turntable-12s-render
- c61 狼人 12 秒亮相出片 `f321b4fd`（216 积分；首提 `12174c59` 取上传令牌失败、未生成）→ `c61_Lycanthrope/source/turntable_f321b4fd/`
- 未替换正式 turntable，待用户确认
- follow_ups/202610.md、revised_prompt.md — 加 231
- follow-up 228 续：时间轴经用户认可，c62 四技能 720p 出片 k621 `3b398158`、k622 `c9a67949`、k623 `991a69c6`、k624 `8bb702ca`（共 954 积分）；每条抽帧初审写 renders/*/review.md；未试听、未锁片。

Source: user_input/follow_ups/202610.md - section 232
Summary: k864 魂之挽歌烟魂改为黑色但不浓、由黑渐淡、半透明有虚空感。

Auto-updated:
- k864 卡特效 / Shot prompt / 峰值图 prompt

No conflicts found in: shared skills / workflow catalog（未改共用源）

Source: user_input/follow_ups/202610.md - section 233
Summary: k861 重抽；k862–k864 写技能视频 prompt（14 / 13 / 15 s）、认可时间轴并出片。

Auto-updated:
- k862 / k863 / k864 卡「技能视频 prompt」与资料包

No conflicts found in: shared skills / workflow catalog（未改共用源）

## Follow-up 227 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 227
Summary: 地狱领主四技能按用户看首版的意见改卡：合计 53 s（11 / 14 / 14 / 14）；k631 剑指＋缠绕，k632 多向能量环护盾＋剑指＋树人更快，k633 暗蓝霜寒包裹后逃跑被砍，k634 不流血、绿光全程缠绕、一刀一个。新图 5 张，时间轴待审，未出片。

Auto-updated:
- c63_Lord_of_Avernus/skills/k631–k634 卡、planning/（新图）、资料包；首版卡备份 `.audit/adhoc_agents/2026-10-25/c63-avernus/before_cards_227/`

## 2026-10-25 — follow-up 225 树精卫士四技能按新造型重做

- k11–k14 新开场图／峰值图、技能卡与视频 prompt 重写（12/14/13/14 s＝53 s，首尾 0.5 s 停顿）；720p 正式条四条共 828 积分，待用户看。

## follow-up 185 续 — 2026-10-25（第六版出片）

- k601 / k602 / k604 第六版 approve + submit（684 积分），review.md、审阅包 02f / 03f / 05f 与 README、三张卡状态行

## 2026-10-25 — follow-up 234 lycan-install-turntable-skills-53s
- c61 12 秒亮相 `f321b4fd` 装为正式版；三视图、声样重切；带翼旧版留档（`_turntable_wings_193.mp4`、`views/_wings_193/`）
- c61 人物卡加「demo 时长预算」（13 / 12 / 12 / 16 = 53 s），狼形态改深梅紫，新立绘 `c61_Lycanthrope_wolf_form.png`
- k611–k614 技能卡按原版 research 与 E 立绘重写，旧卡存各自 `_history/`；开场图 `planning/k61x_start_v*.png`；资料包 sync
- follow_ups/202610.md、revised_prompt.md — 加 234

## Follow-up 235 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 235
Summary: 骷髅王技能第二版：k621 快节奏抛物线火球与明显眩晕、k622 每刀回血两树人各三刀、k624 先对砍再死 + 十字墓碑 + 金橙光柱 + 反杀；k623 接受。时间轴待审。

Auto-updated:
- c62 skills k621、k622、k624 卡（施法动作、特效、作用结果、声音、Shot prompt、不要、技能视频 prompt）及资料包
- c62 skills k624_Reincarnation/ref/（DotA 1 实机重生截图 3 张与 refs.md）
- c62_Skeleton_King.md 重生「真人化画面」

No conflicts found in: shared skills / workflow catalog（未改共用源）


## follow-up 185 续 — 2026-10-25（看第六版后）

- k602、k604 卡状态改第六版定版；k601 卡改不规则折线轨迹（第七版，待审）
- follow_ups/202610.md、revised_prompt.md — 185 下加「看第六版反馈」

## Follow-up 221 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 221
Summary: 全部28区按尺度B（20单位/米、建筑按卡）更新：自动机位、同机位布局渲染，出远景/正面/侧面84张，三轮独立冷看后通过25、有条件35、未通过24。

Auto-updated:
- ai_videos/dota_yingxiong/0_research/map_regions/blender/ — common.json（新增，公共尺度/材质/体块）、plan_cameras.py、region_cameras.json（新增）、region_blockout.py（extends、区域相机）、S1.json/regions_layout.json（继承公共配置）
- ai_videos/dota_yingxiong/0_research/map_regions/layout/ — 109张布局渲染与标注
- ai_videos/dota_yingxiong/0_research/map_regions/map_regions.json — 28区机位指向最终图与审稿状态
- ai_videos/dota_yingxiong/2_世界观人设/background/*/spots/ — 各区机位图与提示词；bg13 远景 v4/v5、侧面 v4/v5
- projects/ai_video_management/apps/ui — 新状态标签（独立冷看通过／冷看有条件通过／冷看未通过／仅作布局地图）

No conflicts found in: shared skills / workflow catalog（未改共用源）

Source: user_input/follow_ups/202610.md - section 237
Summary: k861 ca92388b 认可并混入克隆原声；k862/k863 改远程攻击、k863 光环不伤人、k864 改贴地灵魂柱瞬杀，新时间轴待审。

Auto-updated:
- k861 post/sfx_234；k862–k864 卡锁定节、技能视频 prompt 与资料包

No conflicts found in: shared skills / workflow catalog（未改共用源）

## 2026-10-25 — follow-up 238 luna-53s-feedback
- k231 / k233 Codex 重出首尾帧；k232 月刃早掷、形状保持、先命中再弹；k233 减员、Luna 亲自攻击；k234 光柱快、柱顶鸟一致、撤掉克隆光柱声
- follow_ups/202610.md、revised_prompt.md — 加 238
- follow-up 227 续：时间轴经用户认可，第二版四条 720p 出片 k631 `41e22b04`、k632 `d81320ad`、k633 `f35c3149`、k634 `28720f1e`（共 828 积分，合计约 53.3 s）；每条初审写 renders/*/review.md；未试听、未锁片。

## 2026-10-25 — follow-up 217 续 8 zeus-65s-demo
- c40 亮相 12 秒 `469b068f`；k402 `bc4bda59`、k403 `2f7a475d` 13 秒重出（408 积分）；demo v3 `ep01_final_v3.mp4` 65.4 s，用户定版（取代 v2）

## follow-up 185 续 — 2026-10-25（k601 第七版出片）

- k601 approve + submit（192 积分），review.md、审阅包 02g 与 README、卡状态行

## 2026-10-25 — follow-up 239 lycan-skills-render
- c61 k611–k614 时间轴用户认可后出正式条：7fe418b4 / 928863c4 / 0c4d73dd / f1651fee，合计 954 积分、53.2 s
- 各条 renders/*/review.md 初审；技能卡生成记录、人物卡时长预算状态更新
- follow_ups/202610.md、revised_prompt.md — 加 239
- follow-up 235 续：时间轴经用户认可，k621 `6a50f1c9`、k622 `7c3a5f7d`、k624 `2448a9d5` 出片（共 720 积分）；初审写 renders/*/review.md；未锁片。

## follow-up 185 续 — 2026-10-25（混沌骑士 demo v1）

- c60 demo/edit/final/ep01_final_v1.mp4（63.833 s）、cut_v1.json、四张 title_card_k60x_en.png；c60 README 加 Demo 节；k601 卡状态改定版
- .audit/adhoc_agents/2026-10-25/ck-demo/ 剪辑脚本入库
- follow_ups/202610.md、revised_prompt.md — 185 下加「剪 demo」

No conflicts found in: demo_standard.md（照 §3；k603 首帧定格 0.5 s 为挡标题卡的例外，已在 cut_v1.json note 说明）

## 2026-10-25 — follow-up 241 luna-self-validate-pacing
- Luna 四技能出片后自检流畅度与慢动作嫌疑；填时长用小兵多攻击几下、攻击频率不变
- follow_ups/202610.md、revised_prompt.md — 加 241

## follow-up 185 续 — 2026-10-25（自我验证、12 秒亮相、k602 重出）

- c60 人物卡 turntable 改 12 秒并重出；旧 10 秒版备份 source/
- k602 第七版（伤势不复原、固定出锤节奏）、k601 第八版（眩晕中追击三锤）、k604 第七版（凝实即冲锋）卡与峰值图；待时间轴审阅
- follow_ups/202610.md、revised_prompt.md — 185 下加对应一节

## Follow-up 243 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 243
Summary: c62 四条流畅自检（k621 不合格）；k621 不着火只眩晕 + 连砍填时间，k622 回血光由低往上涌 + 你来我往节奏，k624 两米高十字墓碑 + 跪地停 1 秒；时间轴待审。

Auto-updated:
- c62 skills k621、k622、k624 卡与资料包；四条 renders/*/review.md 补「流畅自检」节；k624 ref/ 新增大小对比图

No conflicts found in: shared skills / workflow catalog（未改共用源）

Source: user_input/follow_ups/202610.md - section 242
Summary: 影魔 k862–k864 按流畅度 / 慢动作自检：k863、k864 改卡重出，k864 剪掉 1.2 s 定格；四条合计 53.11 s（含 k864 首尾停顿）。

Auto-updated:
- k863 / k864 卡技能视频 prompt 与资料包；c86 demo 时长预算；各 render review.md；k864 post/cut_242

No conflicts found in: shared skills / workflow catalog（未改共用源）

## 2026-10-25 — follow-up 236 树精卫士四技能第二版

- 去小树人、掩护／护甲对自己、种子改缠绕绿光、疯狂生长改带刺绿藤；四条 720p 共 828 积分，流畅自检无慢动作；k14 伤害节拍未到每 0.5 s 一次，待用户定。

## Follow-up 240 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 240
Summary: 地狱领主 k631、k634 第二版定版；k632（一镜到底、两层护盾）、k633（不能有慢动作）改卡后出第三版共 432 积分，流畅自检不通过（跳切、星爆拖、树人原地扭动），未交用户；按动作节奏规则改时间轴并重出 k632 开场 / 峰值图，新时间轴待审。

Auto-updated:
- c63_Lord_of_Avernus/skills/k631、k634 卡头定版；k632、k633 卡、planning/（k632_shield_v2、k632_start_v2、k632_peak_v2）、资料包；各条 review.md 的流畅自检

## 2026-10-25 — follow-up 245 lycan-scale-research-self-validate
- demo_standard.md §2「动作节奏」、§4「流畅自检（必做）」；新工具 tools/motion_check.py；README 同步
- c61 体型加大 1.5 倍（人物卡、m160、狼形态）；四张开场图重出；k611–k614 视频 prompt 重写；k612 / k613 补充研究写入 ref/refs.md
- follow_ups/202610.md、revised_prompt.md — 加 245

## 2026-10-25 — follow-up 217 续 9 axe-66s-demo
- c65 亮相 12 秒 `63e28477`；k654 15 秒重出 `2b384b33`（follow-up 240 动作节奏，流畅自检通过）；demo v9 `ep01_final_v9.mp4` 66.4 s，用户定版（取代 v8）

## 2026-10-25 — follow-up 248 luna-r3-feedback-ranged-instant
- Luna 四技能第四轮：柱顶只留鸟；k232 一掷六跳；k233 Luna 只远程掷刃；倒地即死不再起；k234 首道光柱落在 Luna 身上、0.8 s 一道一击必杀、10 s
- follow_ups/202610.md、revised_prompt.md — 加 248

Source: user_input/follow_ups/202610.md - section 247
Summary: 影魔 k861 / k862 认可；k863 体型加倍、盯敌连发（11 s）重出通过自检；k864 体型加倍重出并剪掉 1.1 s 定格；合计 53.22 s（含停顿）。

Auto-updated:
- k863 / k864 卡技能视频 prompt 与资料包；c86 demo 时长预算；render review.md；k864 post/cut_247

No conflicts found in: shared skills / workflow catalog（未改共用源）
- follow-up 243 续：c62 第三版 k621 `a111b229`、k622 `f43d92a6`、k624 `b1f8d804` 出片（720 积分），流畅自检通过，review.md 已写；未锁片。

## follow-up 185 续 — 2026-10-25（自我验证后重出 + demo v2）

- k601 / k602 / k604 新片 review.md、卡状态、审阅包 02h / 03g / 05g
- c60 demo/edit/final/ep01_final_v2.mp4（65.841 s）、cut_v2.json；c60 README

## 2026-10-25 — follow-up 249 lycan-skills-selfcheck-rounds
- c61 四条按 245 时间轴出片并两轮流畅自检；k611 f486b06e、k613 a8bda832 通过；k614 ee66392a 剪辑修正 post/cut_245；k612 两次未做出友方头顶标记，待用户定
- follow_ups/202610.md、revised_prompt.md — 加 249
- follow-up 240 续：第四版 k633 `d55e850e` 自检通过；k632 `1384e717` 自检不通过（举剑停顿、星爆挂约 1.75 s），改时间轴待审。

## Follow-up 250 — 2026-10-25
Source: user_input/follow_ups/202610.md - section 250
Summary: c62 三条技能视频里骷髅王放大到树人的两倍（约 3.6 m）；k621 眩晕加强。时间轴待审。

Auto-updated:
- c62 skills k621、k622、k624 卡「Shot prompt」「技能视频 prompt」及资料包

No conflicts found in: shared skills / workflow catalog（未改共用源）


## follow-up 185 续 — 2026-10-25（demo v3）

- c60 demo/edit/final/ep01_final_v3.mp4（65.841 s）、cut_v3.json；c60 README

## follow-up 185 续 — 2026-10-25（demo v3 定版 + 发布文案）

- c60 cut_v3.json 定版；demo/publish.md 新建；c60 README；k601 / k602 / k604 卡状态行
- follow-up 240 续：k633 第四版 `d55e850e` 定版；k632 第五版 `ced13fbf` 自检通过，待用户看。

## 2026-10-25 — follow-up 217 续 10 omniknight-66s-demo
- c3 亮相 12 秒；k31 14 秒、k34 15 秒各重出两版（第一版骑士站着被用户否，第二版 `dbdd26d2` / `1f9a49b2` 骑士参战、最后单手举锤施法）；demo v5 `ep01_final_v5.mp4` 66.4 s，用户定版（取代 v4）

## 2026-10-25 — follow-up 252 lycan-howl-chest-marks-no-splice
- k612 标记改回胸口 / 肩背，fdb76412；k614 连续原片 8612586c（不用 cut_245 剪辑版）；四条合计 53.12 s
- follow_ups/202610.md、revised_prompt.md — 加 252

## 2026-10-25 — follow-up 254 luna-r4-verdict
- k232 / k234 用户通过；k231 镜头拉远重出首尾帧；k233 缩到 11 s、每只两下死
- follow_ups/202610.md、revised_prompt.md — 加 254
- follow-up 250 续：c62 第四版 k621 `6bb63424`、k622 `161ccc22`、k624 `6b1d9485`（720 积分）流畅自检通过，体型两倍未达到；review.md 已写。

Source: user_input/follow_ups/202610.md - section 251
Summary: k863 三树人错开、只打三下，开场图版 d725f43d 候选；k864 竖直灵魂柱事件图 + 开场图，三次重出仍未做到「从中心一瞬间扩散、所到即死」，待用户定。

Auto-updated:
- k863 / k864 卡技能视频 prompt、planning 开场图与事件图、资料包、render review.md

No conflicts found in: shared skills / workflow catalog（未改共用源）

## Follow-up 253 — 2026-10-26
Source: user_input/follow_ups/202610.md - section 253
Summary: 地狱领主 demo v1 剪出（65.4 s）；用户要 k632 盾里接着砍、受击与爆炸改冷蓝。改卡；两张新参考图 Codex 三轮、ElevenLabs 一次都失败，改只挂开场图 / 护盾图；新时间轴待审，未出片。

Auto-updated:
- c63_Lord_of_Avernus/demo/edit/final/（cut_v1.json、ep01_final_v1.mp4、title_card_k63*_en.png）；skills/k632 卡与资料包
- c63 skills/k632 卡与资料包（第六至八版；参考改为开场图 v2 + 第七版 6.3 s 截帧）、renders/*/review.md；demo/edit/final/cut_v2.json、ep01_final_v2.mp4（65.4 s，k632 换第八版 25fb5a64）

验证: k632 第六、七版流畅自检不通过（举剑定住 1.5–2 s），未交用户；第八版 25fb5a64 motion_check 无嫌疑、无剪切，拼图确认盾里连砍与冰蓝星爆；demo v2 1 fps 抽帧确认标题卡、角标、转场、片尾
费用: k632 第六、七、八版各 216 积分，共 648；Codex 出图五次、ElevenLabs 一次均未出图（费用未知）

No conflicts found in: 共用 skills / workflow catalog 未改

## Follow-up 255 — 2026-10-26 08:55:22
Source: user_input/follow_ups/202610.md - section 255
Summary: 7 天日志复盘（225 条 follow-up）：漏记 25、撞号 7、条目串写、独立审稿多为未审；新增 tools/followup.py 作 follow-up/changelog 唯一写入口并接入 Stop hook。

Auto-updated:
- tools/followup.py — 新增：new 加锁分配编号并一次写好 follow-up 与 changelog、done 写回本条目、check 机检漏记/撞号/格式/待补超 6 小时
- tools/tests/test_followup.py — 新增 6 条测试（漏记、撞号、串写、待补时效、历史不回溯）
- .claude/settings.json — Stop hook 增加 followup.py check --all --hook
- CONVENTIONS.md — Follow-up 第 2、6 步改为经工具写入，规定记录粒度
- AGENTS.md — 工具与收尾增加 check（Codex 无 hook，需显式执行）
- .agents/references/project/workflow_catalog.json — 登记 tools/followup.py
- .gitignore — 忽略 .followup.lock

验证: pytest 6/6 通过；check --all 对 25 个项目通过（2026-10-26 起生效，历史不回溯）；hook 模式与 stop_hook_active 防循环实测；workflow_catalog --check 通过

No conflicts found in: 共用 skills 正文未改；各剧产物未改


## Follow-up 256 — 2026-10-26 09:46:52
Source: user_input/follow_ups/202610.md - section 256
Summary: c42 火女只按 DotA 1 定造型（剔除重制版 / Dota 2 依据），高挑清秀性感；先出 3 张候选立绘

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/ref/model/refs.md — 新增「依据分级」：DotA 1 本体 / 所用经典模型（只看轮廓）/ 不作依据（重制版高等精灵、混乱之治贴图、Dota 2）
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer_v3{a,b,c}.png — 3 张候选立绘（纯文字出图，未上传原版图），未覆盖 c42_Slayer.png；卡与锁定描述符待用户选定后再改

验证: 代理逐张看图：三张都不戴兜帽、红铜蓬卷发、金额冠竖尖饰、尖角垫肩、短尖角裙片（非重制版长裙）、两手各一大团火、无杖、高挑长腿。v3b 首版（无袖+心形领口+开衩）被 OpenAI 输出审核以 sexual 拦下，改为长袖、回眸、收紧腰线、过膝长靴后通过。用户尚未看图（cc-connect 发送接口拒绝连接，图未送达）
费用: ElevenLabs 3 次 quota_exceeded（0 积分余额，未扣）；Codex 订阅额度 4 次出图（含 v3b 被拒 1 次），费用未知；k421 峰值图重试中断 cancelled，费用未知

No conflicts found in: c42_Slayer.md 卡与技能卡未改（待选定）；其他英雄未动

## Follow-up 257 — 2026-10-26 11:45:26
Source: user_input/follow_ups/202610.md - section 257
Summary: 建自检地基：全仓共用检查登记表 + tools/qc.py（record/gate/defect/escapes/stats），审稿类检查须独立审稿，缺陷记录驱动检查进化。

Auto-updated:
- .agents/references/project/qc_checks.toml — 新增全仓共用自检登记表：16 条检查（参考图/原声/规格/prompt/关键帧/视频/成片），每条带来源 follow-up
- tools/qc.py — 新增 record（qc.json 绑 sha）/ gate（审稿项须独立审稿、未审计入统计、旧产物豁免）/ defect / escapes（四种逃逸原因→进化动作）/ stats（逃逸率）
- tools/tests/test_qc.py — 新增 9 条测试
- specs/ai_video/dota_yingxiong/defects.jsonl — 记入本周用户抓到的 10 条缺陷作基线（逃逸率 100%）
- CONVENTIONS.md — 「用户报问题」节增「自检与自我进化」；参考 best effort 且参考本身受检；声音 原声→克隆→使用 各步受检
- AGENTS.md — 工具与收尾增 qc.py record / gate / defect
- .agents/references/project/workflow_catalog.json — 登记 tools/qc.py 与 qc_checks.toml

验证: pytest 16/16 通过（qc 9 + followup 7）；真实数据上 stats / escapes 跑通；followup check --all、workflow_catalog --check 通过。未完成：每周复盘定时任务没挂上——cc-connect 本地 API socket 在 08:45 被另一进程覆盖，需用户重启 cc-connect 后再加；闸门目前还没有接进任何交付路径（剪辑靠各会话拷贝的临时脚本，第二步建共用剪辑工具时接入）

No conflicts found in: 各剧产物未改；正在进行的出片（目录早于 CUTOFF 20261026-120000）不受闸门影响


## Follow-up 258 — 2026-10-26 12:23:21
Source: user_input/follow_ups/202610.md - section 258
Summary: 自检登记按两层拆分（仓库级只留 4 条有共用依据的检查，其余 12 条降到 dota 剧级）；CONVENTIONS 增「仓库级与剧级」原则；管理站新增流程与自检页（仓库级 /workflow/qc、剧级 /qc）。

Auto-updated:
- .agents/references/project/qc_checks.toml — 仓库级只留 4 条有共用依据的检查（video.subject_count / video.onetake_cuts / video.no_text / keyframe.locked_traits），每条写 basis
- ai_videos/dota_yingxiong/qc_checks.toml — 新建剧级登记表：其余 12 条（慢动作、体型、53/65 秒、起势收势、参考图、原声克隆、技能规格、审核避词、时间轴、6.83d 版本）；本剧参考 best effort 与声音 原声→克隆→使用 原则写在抬头
- tools/qc.py — 按产物所在剧合并仓库级 + 剧级登记表，同一 id 两层重复即报错；逃逸报告标注层级
- tools/tests/test_qc.py — 增两层合并与重复 id 测试（11 条全过）
- CONVENTIONS.md — 增「仓库级与剧级」原则（拿不准一律剧级，升仓库级须用户明确同意）；自检节改为只约束有剧级登记表的剧，移出 dota 专属内容
- AGENTS.md — 收尾清单同步两层原则
- .agents/references/project/workflow_catalog.json — qc_checks.toml 移到 1.0 总览组（编号 1.0.4）
- 管理站 UI 见 specs/development/ai_video_management follow-up 310

验证: tools 测试 18/18；qc.py escapes 在真实数据上按层级标注；workflow_catalog --check 通过

No conflicts found in: 各剧产物未改；正在进行的出片不受影响


## Follow-up 259 — 2026-10-26 12:57:02
Source: user_input/follow_ups/202610.md - section 259
Summary: c42 火女衣服形制按 WC3 经典女巫模型重读（大尖角披肩领、喇叭尖袖、菱形前摆加燕尾摆、深 V、大披风、过膝靴），出修正版 v4

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer_v4.png — 修正版候选：宽大尖角披肩领、V 领胸衣、背后大披风带金纹章、喇叭袖长尖角下垂米白袖口、金腰带正中菱形前摆加两侧长尖角燕尾摆、过膝长靴米白尖角靴口；未覆盖 c42_Slayer.png，卡待用户确认后再改

验证: 代理看图：上述六处形制都在，两手各一大团火、无杖、不戴兜帽、金额冠尖饰在。第一次（深 V、露胸口上方）Codex 超时且 generated_images 为空，判为审核静默拦截；领口改为「V 字形开到锁骨下方」后出图。用户尚未确认读法
费用: Codex 订阅额度 2 次（1 次超时无图、1 次成功），费用未知；ElevenLabs 未调用（余额 0）

No conflicts found in: c42_Slayer.md 与技能卡未改


## Follow-up 260 — 2026-10-26 14:34:44
Source: user_input/follow_ups/202610.md - section 260
Summary: 接 246：自检加全局速度审核（motion_check --xt 时空切片＋红蓝参考线，代理看图读速，写进 demo_standard §4 2b）；k14 第四版写死冲刺速度；k12／k13 第三版按大远景开场图实距改时间轴出片并逐条做流畅＋速度审核

Auto-updated:
- tools/motion_check.py — 新增 --xt/--band/--scale/--expect：时空切片图加红线（要求速度）蓝线（走路 1.5 m/s）参考，打印换算值，不自动判定（自动测速三种算法在 AI 视频上不可靠，已放弃）
- ai_videos/dota_yingxiong/demo_standard.md — §4 新增 2b 全局速度审核（必做）：代理看切片图比对斜线读速，写进 review.md；参考食尸鬼冲刺约 6 m/s
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c1_Treant_Protector/skills/k14_Overgrowth/renders/20261026-090223_8e1d566c/ — 第四版（192 积分）：冲刺 2.0–3.6 s 约 5 m/s，速度通过；伤害闪光只有两下，建议剪辑后期叠加 4.2–6.7 s 每 0.5 s 一次
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c1_Treant_Protector/skills/k12_Leech_Seed/ — 开场图／峰值图 planning/k12_*_v3b.png（大远景，树精约占画面六成）；时间轴按实距改写；首条 renders/20261026-130150_3d334b98（228）自检不合格（空蹲、冲出又跑回、绿光晚 3 s）；第二条 renders/20261026-130954_1ded6657（228）通过，剪头 3 s 版 post/cut_246/k12_Leech_Seed_cut.mp4（12.07 s）
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c1_Treant_Protector/skills/k13_Living_Armor/ — 开场图 planning/k13_start_v3b.png；峰值图 v3b 推近停用、v3c 网络 6 次失败未出，本条不挂峰值图；renders/20261026-143223_e98ef8e8（204）：冲刺约 6.5 m/s 通过、无慢动作；偏差：藤甲像条纹绿壳、食尸鬼被打飞时像人形
- 卡片 k12/k13 时间轴、镜头、负面词按 skill_patch_v3 重写并追加视频记录；每条 render 写 review.md、motion_sheet.jpg、xt.png

验证: 每条都跑了 motion_check（拼图＋时空切片），代理看图读速：k14v4 约 5 m/s、k12 扑击约 7 m/s、k13 冲刺约 6.5 m/s；k12 首条自检不合格后自行重出；声音未试听；未做独立冷看；k12/k13/k14 待用户看
费用: Dreamina 积分 192（k14 v4）+228+228（k12 两条）+204（k13）= 852（k14 v3 的 192 记在 246）；Codex 订阅出图约 30 次（多数网络失败无图），费用未知

No conflicts found in: k11 第二版（用户已通过）未动；亮相视频未动；follow-up 256（c42 莉娜，另一会话）未动


## Follow-up 261 — 2026-10-26 14:44:36
Source: user_input/follow_ups/202610.md - section 261
Summary: c42 火女：按原版队伍色位置加蓝（披肩领、披风、前摆、燕尾摆深宝蓝），出 v5 与全红 v4 对照

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer_v5.png — 红配蓝候选：宽大尖角披肩领、大披风（金纹章）、菱形前摆、两条燕尾摆为深宝蓝金边，胸衣、喇叭袖、长裤、过膝靴深红；与 v4 全红并列待用户选；未覆盖 c42_Slayer.png

验证: 代理看图：蓝色落在原版队伍色的四个部位，出成偏深的藏蓝（与红色染色后的效果一致）；其余形制同 v4 全在。PlayDotA 官方动图人物区域偏蓝像素实测 0%，已向用户说明两种依据。用户尚未选定
费用: Codex 订阅额度 1 次，费用未知

No conflicts found in: c42_Slayer.md 与技能卡未改


## Follow-up 262 — 2026-10-26 14:48:10
Source: user_input/follow_ups/202610.md - section 262
Summary: c42 火女：脸改秀美，以 v5 为参考只换脸，出 v6a 清丽端庄 / v6b 甜美秀气

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer_v7a.png — 清丽端庄版：以 v5 遮脸参考（.audit/adhoc_agents/2026-10-26/c42_slayer_v3/c42_Slayer_v5_faceless_ref.png）只换脸，衣服与 v5 一致；鼻更小巧、下颌更柔、眼更清亮、淡妆
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer_v6a.png — 未遮脸参考的作废稿：整张 v5 作参考会把脸一起锁死，脸与 v5 几乎相同（留作教训）

验证: 代理并排裁脸对比 v5 / v6a / v7a：v6a 脸未变，v7a 明显更秀美；v7a 全身服装与 v5 一致、无灰块残留。甜美秀气版（v6b 1 次、v7b 3 次）全部 image_gen「network error: error sending request」且 generated_images 为空，同批 v7a 成功，疑似审核以网络错误形式拦截（年轻化描述＋V 领），第三轮改为二十四岁成年描述仍失败，按三轮上限搁置，交用户决定
费用: Codex 订阅额度：v6a 成功 1、v6b 失败 1（另 1 次重试中断记 cancelled）、v7a 成功 1、v7b 失败 3，费用未知；ElevenLabs 未调用

No conflicts found in: c42_Slayer.md 与技能卡未改，c42_Slayer.png 未覆盖

## Follow-up 263 — 2026-10-26 14:58:46
Source: user_input/follow_ups/202610.md - section 263
Summary: 独立审稿改为脚本另起 CLI 进程（tools/qc_review.py，默认换另一个模型、临时空目录只读、失败换审稿人、都失败记未审）；拦截从 Claude 钩子挪进两边共用的工具（skill_pack 提交前查日志）；新增共用 skill ai-videos-self-check；补 qc.py override 记误报。

Auto-updated:
- tools/qc_review.py — 新增：独立审稿另起 codex exec / claude -p 进程，默认换另一个模型；临时空目录只读、只给拼图与规格；失败换审稿人，都失败记未审；提示词与原始回复存 .audit/…/qc_review/
- tools/qc.py — Check 增 how 字段；新增 override（用户放行＝误报，计入统计、闸门转软项）；stats 单列误报
- tools/skill_pack.py — submit 前自查本剧日志（漏记/撞号/格式/待补超时不提交，Claude 与 Codex 同一道关）；poll 落地后对已启用自检的剧打印自检三步
- .agents/skills/ai-videos-self-check/SKILL.md — 新增共用 skill（两代理同一套），同步 Claude 入口；.agents/skill-aliases.json 加 ai_videos__自检
- CONVENTIONS.md — 能力对照表加「出片独立审稿」「收尾与出片前拦截」两行；follow-up 规则加「先分配编号再引用」
- AGENTS.md — 自检收尾清单改为按 skill 走，审稿一律 qc_review.py
- projects/ai_video_management — 误报不计入缺陷与逃逸率，UI 单列误报（后端 4/4、前端 140/140）
- tools/tests/test_qc_review.py — 新增 6 条；test_qc.py 增 override 测试
- .agents/references/project/workflow_catalog.json — 登记 tools/qc_review.py（新 skill 自动发现）

验证: 工具测试 27/27；管理站后端 4/4、前端 140/140；sync_agent_skills --check、workflow_catalog --check 通过；真实端到端：Codex 审 k601 一条片的临时副本，四项结论均附逐秒依据（人数 pass，时间轴/体型/起势收势 fail），副本已删；两个 CLI 都实测可非交互运行（提示词须经 stdin 传入，-i / --add-dir 会吞掉位置参数）

No conflicts found in: 各剧产物未改；dota、shengji_zhilu 日志闸门实测放行


## Follow-up 264 — 2026-10-26 15:01:51
Source: user_input/follow_ups/202610.md - section 264
Summary: 盘点技能视频的出片前与出片后检查；修正 qc_review 只审审稿类、导致「画面无文字」无人判、闸门永远卡住的问题（无工具的机检项改由审稿兜底）。

Auto-updated:
- tools/qc_review.py — 还没有机检工具的检查（auto = false，如 video.no_text）也交独立审稿兜底，证据标「审稿兜底，待机检工具」；工具做好后改 auto = true 自动退出审稿
- tools/tests/test_qc_review.py — 增兜底项断言

验证: 工具测试 18/18。盘点结论：出片前工具强制的只有时间轴指纹、资料包新鲜度、固定武器参考、参考数量上限、日志健康与付费请求日志；规格必答项、时长预算、参考图身份、关键帧锁定特征、审核敏感词登记了但出片前无人拦（最大缺口）

No conflicts found in: 各剧产物未改


## Follow-up 265 — 2026-10-26 15:18:15
Source: user_input/follow_ups/202610.md - section 265
Summary: c42 火女甜美秀气版按用户要求再试（最多 3 种写法，成功即停）

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer_v7b.png — 未生成（6 次全部失败）

验证: 立即重试 3 次（try1 以 v7a 为参考只改表情 / try2 遮脸＋中性甜美描述 / try3 遮脸＋柔和五官）＋ 后台间隔 5 分钟重试 3 次（15:37、15:45、15:55），全部 image_gen「network error: error sending request」，各会话 generated_images 为空。同时段其他会话 k13_peak_v3c 同样报错，自 15:01 v7a 之后全仓无一张 Codex 出图成功；chatgpt.com / api.openai.com 基本连通（403/401）。据此更正 262 的推断：失败原因判为 Codex 出图线路不通，非审核。后台重试任务在第 3 次后因后台时限被停，无残留进程。
费用: Codex 订阅额度 6 次请求均失败、无图，费用未知

No conflicts found in: c42_Slayer.md、技能卡、c42_Slayer.png 均未改

## Follow-up 266 — 2026-10-26 15:31:22
Source: user_input/follow_ups/202610.md - section 266
Summary: 出片前闸门＋多视角独立审稿（每个角色各一个立场审稿人、导演、观众、原版还原，轮换模型）；体型对照从人物卡派生。

Auto-updated:
- tools/qc_pre.py — 新增出片前闸门：机检（出场角色身高、四条合计 ≥53 s、审核敏感词）、结论写 qc_pre.json 并绑定资料包 prompt 与参考 sha，改了即作废；原版参考与身份立绘的取图
- tools/qc_review.py — 改为多视角：每个出场角色各一个审稿人（立场与视线）、导演、观众（不给规格）、原版还原（附原版截帧与峰值图）；各视角看不同的图；轮流分给 Claude / Codex 并行；任一视角不过即不过；新增 --pre 出片前模式
- tools/scale_table.py — 新增：从人物卡派生体型对照（167/183 张读出身高，16 张待补卡）→ ai_videos/dota_yingxiong/scale_table.{md,png}
- tools/skill_pack.py — submit 先过出片前闸门（一条不过整批不提交，并提示要跑的两条命令）
- tools/qc.py — 抽出 record_into / verdict_problems 供出片前后共用；Check 增 perspective、words
- ai_videos/dota_yingxiong/qc_checks.toml — 剧级新增 8 条：spec.scale_table、keyframe.scale、spec.agency、spec.gaze、video.agency、video.gaze、video.readability、video.fidelity；已有项标视角；时长预算与审核敏感词改为已自动化
- .agents/skills/ai-videos-self-check/SKILL.md — 加出片前步骤与多视角说明，同步 Claude 入口
- projects/ai_video_management — 流程与自检页显示每条检查的审稿视角（后端 4/4、前端 140/140、已构建）
- tools/tests/test_qc_review.py — 重写为 14 条（按角色拆分、任一不过即不过、观众不看规格、模型轮换、出片前结论随规格作废、缺身高拦截、身高解析）
- .agents/references/project/workflow_catalog.json — 登记 qc_pre.py、scale_table.py

验证: 工具测试 35/35（qc_review 14、qc 12、followup 7、skill_pack 时间轴 2）；sync_agent_skills 与 workflow_catalog 检查通过。真实端到端（k601 规格与资料包的临时副本，跑完已删）：4 个视角并行、模型轮换；立场两角色均通过并逐拍说理；抓到真问题——视线只写了 0–2 秒、规格写树人十八米外而开场图折算仅 5–6 米、规格「只到马肩高」无战马身高可核；研究参考里混入 Reforged 重制图（非 6.83d）。端到端暴露并已修的实现缺陷：导演缺身份立绘、版本检查误审我方设计稿

No conflicts found in: k601 卡、资料包与研究参考未改（审出的问题待用户决定）；其他英雄进行中的提交从此需先过出片前闸门


## Follow-up 267 — 2026-10-26 16:22:50
Source: user_input/follow_ups/202610.md - section 267
Summary: c42 火女定稿 v7a（服装沿用 v5 红配蓝）；本会话接手 Lina：定稿改卡 → 补 DotA 1 原版技能参考 → 按新标准重写四条技能 → 开场图 / 峰值图 → 出片前闸门 → 出片 → 出片后多视角审稿 → 剪 demo。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer.md — 文件最后修改 10-26 20:33（由沙王会话按文件时间记录，内容未核）
- c42_Slayer/c42_Slayer_turntable.mp4 — 10-26 17:18 生成（由沙王会话按文件时间记录）
- c42_Slayer/ref/skills/ — 已有 dota1_k421 / k422 / k424 原版截帧与 refs.md（k423 无截帧）
- c42_Slayer/skills/k421–k424/planning/ — 10-26 20:32–21:12 有更新；四条技能均无 qc_pre.json、无新出片

验证: 未完成：Lina 由另一会话按新流程继续（定稿改卡 → 原版参考 → 四条技能 → 开场 / 峰值图 → 出片前闸门 → 出片 → 审稿 → demo）。本条由沙王会话因 Stop hook 超时拦截、只按文件现状记交接进度，没有替 Lina 会话下结论；该会话收尾时应再调用 done 覆盖

No conflicts found in: 未单独核查（非本会话任务）

## Follow-up 268 — 2026-10-26 19:42:54
Source: user_input/follow_ups/202610.md - section 268
Summary: 沙王 demo 按 demo_standard.md 做到 ≥ 65 s：亮相 12 秒已采用（「亮相可以了」）；k753 Caustic Finale 改 14 秒、k754 Epicenter 改 15 秒（六道震荡波）重出，按新自检流程走出片前闸门（qc_pre machine + qc_review --pre）与出片后机检、多视角审稿、qc.py gate；接 follow-up 217 续 11。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/天灾_scourge/c75_Sand_King/c75_Sand_King.md — 12 秒亮相 70242dc2d6d5 采用（用户「亮相可以了」）；demo 时长预算表
- c75_Sand_King/skills/k753_Caustic_Finale/k753_Caustic_Finale.md — 14 秒时间轴 d337ccc28371（用户认可：反击、酸液斑挂到倒下）、视线 / 角色反应行、开场图 planning/k753_start_v268.png 挂入视频参考
- c75_Sand_King/skills/k754_Epicenter/k754_Epicenter.md — 15 秒时间轴 9b774ff43f0e（用户认可：六道地浪＋前沿亮黄偏青柠发光环）、视线 / 角色反应行、开场图 planning/k754_start_v268c.png；峰值图重出 k754_Epicenter_peak.png（旧图存 _134 / _268a）
- c75_Sand_King/ref/skills/（新）与 ref/model/dota1_* — DotA 6.83d / Reforged 原版截帧与 refs.md（子代理）
- tools/qc_pre.py — spec.duration_budget 计入每条首尾 0.5 s 停顿（用户选「工具改成算停顿」）；original_refs 优先 ref/model/dota1_*
- ai_videos/dota_yingxiong/qc_checks.toml — spec.duration_budget 的 desc / how 写明可计停顿，sources 加 #268

验证: 进行中，未出片：qc_pre machine 两条通过；qc_review --pre 第 1 轮（缺开场图、参考是 WC3 野怪等 6 项不过）、第 2 轮（identity 过；locked_traits / scale / agency / gaze / status_visual 不过）已按证据改；k754 峰值图加发光环与 k753 开场图重出因 Codex 429 未成，25 分钟后重试，随后第 3 轮审稿，过了才提交
费用: 即梦 0 积分（未提交）；Codex 出图为订阅额度

No conflicts found in: demo_standard.md §1 停顿条款与 qc_pre 已对齐

## Follow-up 269 — 2026-10-26 19:45:52
Source: user_input/follow_ups/202610.md - section 269
Summary: c63 k632 第八版、k633 第四版不通过：k632 开场就要攻击树人、剑要真正砍到树人身上、盾灭后冷蓝爆炸收小不要大花；k633 开场被打要立刻反击。按新出片与自检流程（scale_table、qc_pre 机检与多视角审稿、出片后 qc_review 与 qc.py gate）重出，用户抓到的问题记 qc.py defect。

Auto-updated:
- c63_Lord_of_Avernus/skills/k632_Aphotic_Shield/ — 卡最后修改 10-26 22:14；qc_pre.json 10-26 22:16（locked_traits / identity / version / scale / gaze 仍 fail）；新出片目录 renders/20261026-215316_f6464754、20261026-222341_480abbc1（由沙王会话按文件现状记录，未看片）
- c63_Lord_of_Avernus/skills/k633_Frostmourne/ — 卡最后修改 10-26 22:01；qc_pre.json 10-26 22:13（locked_traits / identity / version / scale / status_visual 仍 fail）；新出片目录 renders/20261026-215523_10e750c8、20261026-222241_7ad6ea6a（未看片）
- c63 skills/k632、k633 卡与资料包（开场图 k632_start_v4 / k633_start_v3、两轮规格修订）；qc_pre.json（用户放行记录）；renders 下第 1、2 轮出片与 review.md；剧级 qc_checks.toml 新增 video.attack_contact、video.stun_visible 补 when=眩晕；c63 人物卡体型行与 demo 时长预算

验证: 出片前：qc_pre machine 通过；多视角审稿三轮，体型 / 锁定特征 / 原版参考类不过由用户选「1」放行；出片后：第 1、2 轮两条均 motion_check 无慢动作，k632 第 1 轮 3.88 s 硬切，多视角审稿与 qc.py gate 均不通过，未交用户；后续在 follow-up 279 继续
费用: k632 / k633 第 1、2 轮各 216 积分，共 864；Codex 开场图若干次（费用未知），ElevenLabs 一次发送失败

No conflicts found in: 共用 skills / workflow catalog 未改

## Follow-up 270 — 2026-10-26 19:50:02
Source: user_input/follow_ups/202610.md - section 270
Summary: 按 251 方案 1 给 k864 出加速 demo：e7a6f07a（唯一一次灵魂柱从脚边向外扩散）7.75–10.0 s 加速 2.5 倍 → post/speed_demo/k864_Requiem_of_Souls_speed.mp4（13.75 s），扩散到树人全倒约 1 s；不花积分。已读新版 ai-videos-self-check 流程，后续出片走 qc_pre / qc_review / qc gate 与 followup.py。

Auto-updated:
- k864 post/speed_demo（edit.json、sheet_4fps.jpg）

验证: motion_check：动作段 1.5–11.5 s 未见慢动作或定格；拼图确认 7.75 s 出柱、约 8.75 s 扩散到外圈、9 s 前树人全倒
费用: 0 积分

No conflicts found in: （未单独核查）


## Follow-up 271 — 2026-10-26 19:50:37
Source: user_input/follow_ups/202610.md - section 271
Summary: 骷髅王第四版（k621 6bb63424 / k622 161ccc22 / k624 6b1d9485）不通过：k621 眩晕仍看不出；开场他没看敌人；体型不是树人两倍。按新流程：人物卡改身高（改体型＝改卡）、出开场图锁比例与视线、每拍写视线、k621 眩晕改用原版头顶旋涡圈并重出峰值图，过 qc_pre 闸门后交时间轴审。

Auto-updated:
- c62_Skeleton_King.md（身高 3.8 m）；scale_table.{md,png}；k621/k622/k624 技能卡（开场图、逐拍视线与树人反应、k621 眩晕旋涡圈与时间轴按六米重排、新峰值图）；planning/ 开场图与峰值图；ref/skills/ 原版截帧与 refs.md；qc_checks.toml（新增 spec.status_visual、video.stun_visible）；三条旧 render 的 review.md

验证: 缺陷已记 7 条（video.gaze×3、video.scale×3、new:stun_visible）；qc_pre machine 三条通过；出片前多视角审稿跑满 3 轮仍有开场图项不过，带证据交用户，用户选 A（见 follow-up 275）
费用: Codex 出图 13 次成功（ChatGPT 订阅额度），5 次网络 / 限流失败核对无产出；无视频积分

No conflicts found in: （未单独核查）

## Follow-up 272 — 2026-10-26 19:54:04
Source: user_input/follow_ups/202610.md - section 272
Summary: 影魔身高统一为树人四倍：人物卡「体型 / 年龄 / 种族」改为约 7.6 m（连火尾），真人化与 Shot prompt 外观句同步；scale_table 重生成（4.22×）。已认可的 k861 / k862 里他约为树人两倍，是否重出由用户定。

Auto-updated:
- c86 人物卡体型行、真人化、Shot prompt 外观；scale_table.{md,png}

验证: scale_table 显示 c86 7.6 m（4.22×）
费用: 0 积分

No conflicts found in: （未单独核查）


## Follow-up 273 — 2026-10-26 20:07:29
Source: user_input/follow_ups/202610.md - section 273
Summary: 按 272 新身高（树人四倍、约 7.6 m）重出 k861 / k862 / k863：k862、k863 文字改体型；k861 开场图与远中近事件图里他只有两倍高，先用 Codex 按四倍重画再出。每条先过 qc_pre（机检 + 多视角独立审稿）闸门，出片后跑 motion_check、qc_review、qc gate。

Auto-updated:
- k861/k862/k863 卡技能视频 prompt（体型四倍、树人动机与逐拍视线、k863 常驻光环去热浪）；k861 planning start_v7/v8、far/mid/near_v3；k862 planning start_v1；k863 planning start_v2/v3/v4；资料包 sync

验证: qc_pre 三轮均不通过（keyframe.scale 透视下量不出四倍、原版参考版本/原版无此效果、首帧朝向）；用户同意放行「原版无此设计」与「参考版本」两类，体型选择继续重画开场图；Codex 网络错误与 429 限流共 11 张未出图（会话目录无图，确认未生成），未提交出片
费用: Seedance 0 积分（未提交）；Codex 订阅额度

No conflicts found in: （未单独核查）

## Follow-up 274 — 2026-10-26 20:20:56
Source: user_input/follow_ups/202610.md - section 274
Summary: Luna k231–k234 按新出片与自检流程重做：预算 9+11+13+16=49 s+停顿 4 s=53 s；峰值图按已认可长相重出；每条过 qc_pre 再出片，出片后过 qc gate。

Auto-updated:
- c23_Moon_Rider.md「demo 时长预算」（9+11+13+16=49 s+停顿 4 s=53 s）；k231–k234 技能卡「技能视频 prompt」改为 multimodal 新格式（视线 / 角色反应 / 镜头 / 光线 / 台词 / 声音）；四张峰值图按已认可长相重出；开场图 k231_v18_start、k232_v3_start、k233_v16_start、k234_v2_start；ref/model 与 ref/skills 剔除 Reforged 与单源截帧（refs.md 记录）；脚本 .audit/adhoc_agents/2026-10-26/luna-newflow/

验证: qc_pre machine 四条 pass；qc_review --pre 第 1 轮四条不过（pre_fails_r1.md）、第 2 轮仍不过（pre_fails_r2.md，k234 只剩 2 项）；第 3 轮改图因 Codex 429 限流仍在补出（k232 / k233 峰值图），第 3 轮审稿与出片尚未进行
费用: Codex 出图约 16 次（含限流失败）；Dreamina 0 积分（尚未提交）

No conflicts found in: demo_standard.md、qc_checks.toml 未改

## Follow-up 275 — 2026-10-26 21:34:44
Source: user_input/follow_ups/202610.md - section 275
Summary: 按 A：k621/k622/k624 时间轴（cd05dbd338ac / d2051321dc37 / 392e7e302126）随选项认可后 approve；出片前审稿重跑一轮，用户接受的开场图项与 k624 减速标记记为用户放行（误报）；过闸门后出片，下载后走出片后机检、多视角审稿与 qc.py gate。人物卡改 3.8 m 后 k623 与亮相是否重出，用户未答，不动。

Auto-updated:
- k621/k622/k624 技能卡（逐拍视线与树人反应、措辞修正、第二轮镜头/要求/负面词）；开场图 k622_start_v6、k624_start_v7；tools/qc.py override 支持出片前 qc_pre.json；三条第一轮 renders 的 review.md / qc.json；c62 ref/skills 原版截帧

验证: 出片前闸门按用户 A 放行开场图项后通过并出片；第一轮 k621 c4ccc5fc / k622 65455a48 / k624 4e6c1b3e：motion_check 无慢动作（k624 8.5–10 s 为规格跪地停顿），出片后多视角审稿闸门三条均不通过，理由写入 review.md；tools/tests/test_qc*.py 26 passed
费用: 视频：k621 216、k622 234、k624（见 request_log）约 720 积分；Codex 出图（订阅额度）若干次；k624 首次提交在取账户信息时超时，list_task 核对无任务后重提

No conflicts found in: （未单独核查）

## Follow-up 276 — 2026-10-27 08:19:49
Source: user_input/follow_ups/202610.md - section 276
Summary: 骷髅王第二轮：267 由本会话代为结项（写明 Lina 工作仍在进行）；k622 无原图项按用户放行；k621/k622/k624 第二轮 prompt（不推近、火球不包住他、旋涡 4.6 s 散、红光不铺地、十字无圆环、收尾看倒地树人）过出片前闸门后提交，出片后机检、多视角审稿与闸门。

Auto-updated:
- k621/k622/k624 技能卡第二轮镜头 / 要求 / 负面词与措辞（指纹 k621 06d4755c57eb、k622 5e6359dedf1a、k624 666229878696，秒数未变）
- 第二轮 renders：k621 20261027-085059_52beb960、k622 20261027-085142_f48ed895、k624 20261027-085230_7241138e（review.md / qc.json）

验证: 出片前闸门按用户放行项通过后提交；motion_check 三条无真慢动作（k624 两段对应规格墓碑静立与跪地停顿）；出片后多视角审稿三条闸门均不通过，停在第 2 轮带证据交用户
费用: 第二轮视频约 720 积分（k621 216 / k622 234 / k624 270 级别，以 request_log 为准）

No conflicts found in: （未单独核查）

## Follow-up 277 — 2026-10-27 08:20:35
Source: user_input/follow_ups/202610.md - section 277
Summary: 接 273：Codex 限流恢复后用长焦侧拍写法重画 k861/k862/k863 开场图（四倍体型），量比例合格后换进卡，跑第四轮 qc_pre；按用户同意登记「原版无此设计」「参考版本」两类放行，过闸门后提交出片，出片后 motion_check + qc_review + qc gate。

Auto-updated:
- k861/k862/k863 开场图（Codex start_v7–v10、k862 v1–v5、k863 v2–v4）、事件图 v3；卡与资料包

验证: 见 285 与 decisions.md
费用: Codex 订阅额度

No conflicts found in: （未单独核查）

## Follow-up 278 — 2026-10-27 08:21:34
Source: user_input/follow_ups/202610.md - section 278
Summary: Luna 出片前闸门：修三张图；用户放行 scale / locked_traits / identity 三类审稿 fail（qc.py override 记误报）；图改后工具强制重审一次；随后 skill_pack submit 四条 final。

Auto-updated:
- k232 qc_pre.json 两项 override（keyframe.locked_traits / keyframe.scale，记误报 defects.jsonl）；k233_v17_start、k231 峰值图、k234_v3_start 修图中（.audit/adhoc_agents/2026-10-26/luna-newflow/fix4_*）

验证: k232 出片前闸门通过（用户放行 2 项）并已 skill_pack submit final；k231 / k233 / k234 待修图后工具强制重审，再按用户放行范围 override 后提交
费用: k232 约 198 积分（11 s）；Codex 出图 3 张进行中

No conflicts found in: qc_checks.toml、demo_standard.md 未改


## Follow-up 279 — 2026-10-27 08:40:14
Source: user_input/follow_ups/202610.md - section 279
Summary: 看 k632 / k633 第 2 轮（480abbc1 / 7ad6ea6a）：k632 开场出剑要快；外层能量环分布在 x / y / z 三个不同轴上旋转，不能都是同一方向。k633 霜寒裹住后逃跑要明显变慢（霜之哀伤减速），仍是正常实时画面。只改技能描述、特效与负面词，不动时间轴分秒行；按新流程过出片前与出片后闸门。

Auto-updated:
- k632 / k633 卡（出手节奏、三轴环、减速可见）与资料包；剧级 qc_checks.toml 新增 video.attack_tempo、video.slow_visible；第 3 轮出片 894e8252 / c446ae86 与 review.md

验证: 出片前闸门（代理沿用用户放行）通过；第 3 轮两条 motion_check 无慢动作、多视角审稿与 qc.py gate 不通过，未交付；后续并入 follow-up 284
费用: 2 × 216 = 432 积分

No conflicts found in: 共用 skills / workflow catalog 未改

## Follow-up 280 — 2026-10-27 08:43:02
Source: user_input/follow_ups/202610.md - section 280
Summary: follow-up 改为各会话先各自记（_inbox 每条一文件、记归属会话），done 只改自己的条目；merge 周期性汇聚进月度文件与 changelog（Stop 钩子与 done 后自动跑）；钩子与 skill_pack 日志闸门只拦本会话自己超时未收尾的条目，其他会话的问题只提示。

Auto-updated:
- tools/followup.py — new 写进本会话 _inbox 条目（记归属会话）、done 只改自己的条目并汇聚、新增 merge、check/钩子先汇聚且只拦本会话自己的问题
- tools/skill_pack.py — log_gate 只按本会话查日志
- tools/tests/test_followup.py — 按新语义重写（各自记、汇聚顺序、只拦自己、旧条目只提示、钩子按 stdin 会话）
- CONVENTIONS.md §Follow-up prompt handling 与工具对照表；.agents/skills/ai-videos-self-check/SKILL.md 日志行

验证: pytest tools/tests/test_followup.py test_qc.py test_qc_review.py test_skill_pack_timeline.py 38 passed；实库 followup.py check --all 通过（其他会话与旧条目只提示）；skill_pack.log_gate('dota_yingxiong') 为 True；sync_agent_skills --check、workflow_catalog --check 通过

No conflicts found in: 管理站 process_qc__reader 只读月度文件，_inbox 条目汇聚前不显示（汇聚后正常）


## Follow-up 282 — 2026-10-27 13:01:50
Source: user_input/follow_ups/202610.md - section 282
Summary: 根因：代理把出图→资料包→机检→审稿→闸门→提交→收片→出片后自检十来步手动一段段接，每段跑完要被唤醒才接下一段，四条串行、会话一断全停；画面无法验证类的审稿项拖到第 3 轮才问用户。修：新增 tools/skill_run.py 总控（可续跑、几条并行、出图网络失败且确认没出图才重试、出片前不过时把画面无法验证类当场列给用户、--allow 沿用用户已明确的整类放行、出片后自动 motion_check 记 slowmo + qc_review + gate、run_state.json 与 cc-connect 推送）；qc_review 提示里注明拼图时间码是审片工具加的（k422 被误判 video.no_text）；先放剧级（dota skills/README），用法未升仓库级。另记：同一张 k424 峰值图两轮审稿对后排食尸鬼姿态判法相反，审稿稳定性待观察。

Auto-updated:
- tools/skill_run.py — 新增技能视频总控（关键帧自动出图含网络重试、资料包、出片前审稿与闸门、--allow 沿用用户整类放行、时间轴留痕、720p 正式条、出片后 motion_check/qc_review/gate、run_state.json、cc-connect 推送；几条并行、可续跑）
- tools/qc_review.py — 出片后审稿提示注明拼图时间码是审片工具加的（修 video.no_text 误判）
- tools/tests/test_skill_run.py — 动作段与 --when 推断 3 个测试
- ai_videos/dota_yingxiong/2_世界观人设/skills/README.md — 剧级记一条龙跑用法；.agents/references/project/workflow_catalog.json — 登记 tools/skill_run.py（2.3.116）

验证: pytest test_skill_run / test_qc_review / test_qc 29 passed；workflow_catalog --fix/--check 通过；实跑：k422 第 2 轮、k424 第 2 轮由总控提交并自动出片后审稿与闸门，k422 r2 审稿 no_text 已 pass（误判已修）

No conflicts found in: 未改仓库级登记表与共用 skill 正文（仅剧级 README）


## Follow-up 281 — 2026-10-27 09:20:20
Source: user_input/follow_ups/202610.md - section 281
Summary: 接 267（已由他会话结项）：Lina 四个技能按新流程续做——开场图 v3、峰值图 v1 已出；按新检查 spec.status_visual 把 k422 眩晕改成原版头顶浅蓝白旋涡（去掉负面词里的晕眩标记）；sync 资料包 → qc_pre machine → qc_review --pre → 时间轴表 approve（用户 2026-10-24 授权免等）→ 出片前闸门 → submit final → 出片后 motion_check + qc_review + qc gate；之后剪 demo。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/skills/k421–k424 技能卡 — 技能视频 prompt 多轮修订（k422 眩晕改原版浅蓝白旋涡、补刀；k423 炽魂改两手裹火去击退；k424 只打领头、闪电半秒、画面大小卡出手；k421 去控制、补凤凰模型依据）；k423 卡锁定段同步
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/skills/*/planning — 开场图 v3、峰值图 k421 v3 / k422 v2 / k423 v3 / k424 v2 及 prompt / refs
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/ref/model — 原拼图与重制版图移入 _excluded/，新 compare_dota1_classic_only.png，refs.md 记调整；ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/ref/skills — DotA1 原版技能截帧与 refs.md
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/c42_Slayer.md — demo 时长预算（53 s）、亮相转盘生成记录（7e44338ec39b，独立审稿 pass）
- qc_pre.json / qc.json / review.md — 各条出片前与出片后结论；用户放行（「这几项先放行」）按 qc.py override 记：k421/k422/k424 keyframe.scale、keyframe.locked_traits、spec.gaze（远景俯身体型、骨爪看不清、远处脸朝镜头）

验证: 亮相转盘：拼图+听写+独立审稿通过，已经 cc-connect 发用户（zip）。出片：k422 r1 313be2e0 / r2 2d72a605、k424 r1 e2fef651 / r2 45b3c4be 均出片后闸门不通过（review.md 写明）；k422 r2 代理判可用、已发用户待定放行与时间轴容差；k421 已过出片前闸门在出片、k423 重审中、k424 第 3 轮重审中——工作未完，后续另开条目
费用: 视频：k422 204×2、k424 r1/r2 约 270×2（以 request_log 为准）；亮相 12 s 一条；Codex 出图（订阅额度）约 20 次（含网络失败重试）

No conflicts found in: （未单独核查）


## Follow-up 285 — 2026-10-27 18:10:24
Source: user_input/follow_ups/202610.md - section 285
Summary: 影魔四技能改为代理自主推进到成片：闸门不过时由代理按「最优解」决定改 prompt / 放行 / 剪辑补救，不再逐项问用户；每个问题与决定写进决策日志 .audit/adhoc_agents/2026-10-24/sf-research-154/decisions.md，事后与用户复盘。

Auto-updated:
- c86 demo/edit/final/ep01_final_v1.mp4 + cut_v1.json + title cards；人物卡 demo 时长预算；k861/k862/k863/k864 卡与 qc_pre（含放行记录）；defects.jsonl；decisions.md D1–D7

验证: demo 64.05 s、技能条合计 53.94 s（cut_v1.json）；1 fps 拼图确认亮相、四段标题卡、角标、压暗转场、片尾淡出；k862/k863 出片后 motion_check 通过、qc_review 闸门未过（qc.json）；k861/k864 因即梦积分 84 不足未提交
费用: Seedance 450 积分（k862 252 + k863 198）；k861 提交被拒未扣费

No conflicts found in: （未单独核查）


## Follow-up 284 — 2026-10-27 18:04:10
Source: user_input/follow_ups/202610.md - section 284
Summary: 自主授权（Iteration bounds）：范围＝c63 地狱领主 k632 / k633 重出到可用 + 重剪 demo MP4；时间轴审阅、参考图确认、闸门放行由代理按最优判断自行决定，不再中途询问。付费：即梦视频按需（预算上限约 6 条 × 216 ≈ 1,300 积分），图片 Codex。轮次：每技能最多再 3 轮出片；退出条件：过出片后闸门，或 3 轮后选审稿不过项最少的一条交付并写明未过项。请求前日志、独立审稿、结果未知不重提照常。问题与决策逐条记 .audit/adhoc_agents/2026-10-25/c63-avernus/decision_log.md，事后与用户复盘。

Auto-updated:
- 编辑式开场图 k632_start_v5 / k633_start_v4、参考图 k632_shield_v5 / k633_peak_v4、两张卡与资料包；选中条 480abbc1 / 7ad6ea6a 的 qc.json（代理放行）；demo cut_v3.json 与 ep01_final_v3.mp4（65.4 s）；decision_log.md

验证: 第 4 轮提交被即梦拒（CreditPreDeductNotEnough，未扣费，余 84）；选中条补跑独立审稿后代理放行，qc.py gate 通过（放行计入统计）；demo v3 ffprobe 65.43 s、1 fps 抽帧核对；未试听、未独立冷看、未锁片
费用: 本轮新出图若干（Codex，费用未知）；视频 0 积分（提交未成功）

No conflicts found in: 共用 skills / workflow catalog 未改


## Follow-up 288 — 2026-10-27 21:19:15
Source: user_input/follow_ups/202610.md - section 288
Summary: 确认287建模范围、静态交付与DINOv3任务级例外。

Auto-updated:
- 2_世界观人设/background/map_3d/asset_manifest.json：锁定地图与常驻 NPC、英雄另做、静态精模与摆放优先、后续再绑定动画；记录本次 DINOv3 例外，禁止 Hyper3D。bg23/model_3d/r03/workflow_api.json 使用本地 TRELLIS.2、BiRefNet、CuMesh 和 DRTK。

验证: 用户三个异步答复已落实；资产清单含 23 建筑与 36 NPC；未调用 Hyper3D 或收费服务；精模生成仍在进行，未宣称模型验收通过。
费用: 本地推理，无按次生成费；0 次 Hyper3D 请求

No conflicts found in: （未单独核查）


## Follow-up 287 — 2026-10-27 21:17:07
Source: user_input/follow_ups/202610.md - section 287
Summary: 本地三维资产制作与完整DotA地图搭建；先验证建筑样例，再批量资产及组装。

Auto-updated:
- 本轮阶段性结果，任务未完成：0_research/map_regions/blender/ 新增 prepare_production_assets.py、local_mesh.py、local_attention_compat.py、build_production_map.py、refine_map_environment.py、render_map_check.py、inspect_model.py；2_世界观人设/background/map_3d/ 保存资产与环境清单、foundation_v001/v002.blend、两版俯瞰及河道检查图、production_state.json。bg23_奎尔瑟兰的密室/model_3d/r01-r03 保存三个本地请求与失败历史，r03 已导出 849729648 字节原始 GLB，PBR 烘焙在运行。运行审计及单项超时 pipeline.halted 事件见 .audit/adhoc_agents/2026-10-27/dota-local-3d-287/。
- 阶段性产物，完整任务未完成：0_research/map_regions/blender/ 新增 prepare_production_assets.py、local_mesh.py、local_attention_compat.py、build_production_map.py、refine_map_environment.py、render_map_check.py、inspect_model.py。2_世界观人设/background/map_3d/ 保存资产/环境清单、foundation_v001/v002.blend、两版俯瞰与河道图、production_state.json。2_世界观人设/background/近卫_sentinel/bg23_奎尔瑟兰的密室/model_3d/r01-r03/ 保存请求/历史；r03 最终成功，原始 GLB 849729648字节（SHA db10a83456c5fdcd4435ef299c264031278054ef48343a221d28ca072af9ff99）、PBR GLB 31292480字节（SHA c57cc0fedba8bd8ea0450c0adfdc10f0dac68fc4a24eed654c51c9161178d008）；inspection/ 保存可编辑 bg23_r03.blend、五视角渲染、inspection.json、quality_review.json。审计与 pipeline.halted 事件见 .audit/adhoc_agents/2026-10-27/dota-local-3d-287/。

验证: 23建筑、36 NPC；地图1050625顶点、3676树实例；另有1522个地图对象，其中195为逻辑阻挡物。地图保存/重载/渲染及看图通过，但仍是底稿。SageAttention崩溃通过仅本任务运行时 PyTorch SDPA 兼容层解决，数值对照通过，7脚本语法通过。r03历时20分43秒，PBR导出并在Blender成功导入；场景候选262379顶点、233941三角面、高5米。五视角检查发现球体缺失、支架断裂、屋檐墙面碎片变形，作者QC失败，零个精模通过交付；未做独立审稿，未启动批量。原始3949万面高模导入过慢，已停止该自有检查进程，最终检查改用PBR模型。先前30分钟单项超时已升级用户，当前等待是否继续修复；后台生成已结束并请求释放模型内存。原图自定义装饰物表的MPQ读取受已装读取器不支持加密限制，未继续重试；未误建逻辑阻挡物。其他会话改动保留。
费用: 本地推理；Hyper3D 0 次，收费服务 0 次

No conflicts found in: （未单独核查）


## Follow-up 289 — 2026-10-28 04:45:01
Source: user_input/follow_ups/202610.md - section 289
Summary: 解除本次本地三维制作的单项时限，继续首件结构修复、全部建筑与NPC建模及地图组装

Auto-updated:
- 已完成地图环境 v013、工作组装 v003、11 类模型候选及多轮独立检查；本条记录本阶段实际进展，总任务尚未完成，后续接续基础建模与返工。

验证: 11/59 类有完整候选，0/59 类通过；bg12 单视图和官方参数对照、m300 官方参数对照均未消除质量缺陷；m306 r16 坐标迁移检查通过，外观检查仍失败。
费用: 本地生成；未调用 Hyper3D 或收费生成服务。

No conflicts found in: 只处理本任务脚本、资产版本和状态；保留其他会话改动。


## Follow-up 290 — 2026-10-28 19:23:13
Source: user_input/follow_ups/202610.md - section 290
Summary: 接续本地三维制作：保留全部候选，恢复剩余资产队列，按实际检查结果返工，不把文件生成当成完成。

Auto-updated:
- 本阶段部分完成：候选增至42/59，通过仍为1/59；验证512重建导致细节损失，保留3M面流程接入后续批次；m5/m8接地修复；树人r12、塔r12仍失败；环境v016远近草地衔接已接入工作图v012。后续高分辨率树人、扫描叶与食人魔精修继续，不代表整图交付。

验证: m1 r01/r08原始GLB哈希相同；r08独立审稿fail5；r12独立审稿fail8；环境v016总览和近景作者目检；批量任务与审稿、地图刷新进程已核对；最终资产和整图QC未通过。
费用: 本阶段无Hyper3D及收费生成请求；本地GPU运行，槭叶扫描来自ambientCG CC0。

No conflicts found in: 仅修改本剧建模脚本、候选版本与制作状态，原始图和历史版本保留，其他会话改动保留。


## Follow-up 291 — 2026-10-29 01:10:07
Source: user_input/follow_ups/202610.md - section 291
Summary: 接续290：完成剩余模型候选、树人1536与扫描叶对照、食人魔材质獠牙修复及地图质量检查。严格区分候选与独立验收，不以批量生成代替精细完成。

Auto-updated:
- 阶段检查点：59类候选已齐备，仅Wisp通过；v018地图包含59类、95个布置与30个线兵实例。v030环境和bg23 r33、m26 r04仍为作者修订候选，总任务继续。

验证: v018环境独立检查fail9；bg23 r32 fail3，r33几何间隙0.07255米且作者预览已查看；m26校正5米体长，局部封孔仍有76182条边界边。v028水域回退拒绝，v030实际水面核对正在执行。
费用: 未调用Hyper3D或付费生成；本地Blender修订、渲染及独立QC。

No conflicts found in: 保留原始资产、历次候选及其他会话改动；此条仅记录阶段工作，不表示总任务交付。


## Follow-up 292 — 2026-10-29 06:53:02
Source: user_input/follow_ups/202610.md - section 292
Summary: 接续291：核对v030水域与环境、bg23 r33完整检查、雷霆蜥蜴线状残片修复，继续剩余资产精修与整图验收。

Auto-updated:
- 阶段接续：保存 v022 总装；v039–v041 局部岩层试验；bg23 r45 完整审稿 fail 5；NPC 补面仍未通过。整体制作未完成，转下一条继续。

验证: 59/59 候选，1/59 独立通过；v022 全景因系统提交额度不足失败，恢复等待已超时；保留日志与 manual_work_r21.json。m26 r12 UV 转移运行一夜无产物，核验任务进程后终止。

No conflicts found in: 保留现有 1149 项工作区改动和其他会话条目；未关闭 openweb。


## Follow-up 283 — 2026-10-27 15:20:59
Source: user_input/follow_ups/202610.md - section 283
Summary: 接 281：总控 skill_run 继续跑 k421（出片中）、k423（重审）、k424 第 3 轮（画面大小卡出手时机）；出片后结论与预览经 cc-connect 发用户（飞书 mp4 需打 zip）；k422 r2 待用户定放行与时间轴 0.75 s 容差；四条过闸门后剪 demo（≥65 s）交用户批准。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/skills/k421_Dragon_Slave — 出片前放行 locked_traits / spec.gaze（用户「这几项先放行」范围：远处脸朝镜头、骨爪看不清），规格去掉原版没有的击退 / 眩晕、补凤凰模型依据、后三只改急刹护脸；第 1 轮出片 renders/20261027-153415_b3a9b37f（qc.json）
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/skills/k423_Fiery_Soul — 规格按峰值图 v3 对齐（背景以开场图为准、两手火大小、尸体可被画框裁）
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/skills/k424_Laguna_Blade — 第 2 轮出片 renders/20261027-145013_45b3c4be + review.md；第 3 轮规格（画面大小卡出手时机，指纹 eedb19bee73b）
- cc-connect 发用户：k422 第 2 版预览（zip）与拼图、亮相转盘预览（zip）；飞书不收直接发的 mp4、需打 zip

验证: k421 r1 b3a9b37f：motion_check 通过，出片后闸门不通过（3.0–3.25 s 敌人到跟前才出手、火浪持续喷约 3 s）；k423 出片前不过（规格「对称」与「一大一小」自相矛盾）；k424 第 3 轮后台重审未跑成（& 启动的进程未留结果）。工作停在待用户定：k422 r2 放行、时间轴 0.75 s 容差、是否给 Lina 开自主授权（同 284/285）——续做另开条目
费用: k421 r1 192 积分；本条其余为重审（订阅额度）

No conflicts found in: （未单独核查）


## Follow-up 294 — 2026-10-30 12:35:34
Source: user_input/follow_ups/202610.md - section 294
Summary: 继续 Lina（接 283）：把现有全部视频（亮相转盘、k421 r1、k422 r1/r2、k424 r1/r2）压缩打 zip 经 cc-connect 发用户看，附每条状态；之后按用户反馈续做 k421/k423/k424 与 demo。

Auto-updated:
- （无仓库文件改动）经 cc-connect 发用户 6 条预览：亮相转盘、k421 v1（b3a9b37f）、k422 v1（313be2e0）/ v2（2d72a605）、k424 v1（e2fef651）/ v2（45b3c4be）；960 宽 crf30 压缩、打 zip（飞书不收直接发的 mp4）

验证: 6 条 cc-connect send 均返回 Message sent successfully

No conflicts found in: （未单独核查）


## Follow-up 295 — 2026-10-30 12:54:34
Source: user_input/follow_ups/202610.md - section 295
Summary: k421 龙破斩重出：一镜到底（v1 3.50 s 有剪切）、双手一起推出（v1 单手持续喷）、一次掠过不持续喷、敌人在远处就出手。流程（剧级）：自主权下出片后有问题不得自动再提交，必须等用户反馈——skill_pack submit / skill_run 强制：上一条出片没有用户反馈记录就拒绝提交，新增 feedback 记录命令。另补机检漏洞：motion_check 原无剪切检测（登记表却写已自动化），新增边缘重合剪切检测并接进总控记 video.onetake_cuts；剪切根源是峰值图与开场图取景不一致，出片前加开场图 / 峰值图取景一致机检。

Auto-updated:
- tools/skill_pack.py — 剧级策略 wait_user_feedback_after_render：上一条出片没有 user_feedback.md 就拒绝提交；新增 feedback 命令
- tools/skill_run.py — 提交前过反馈闸门；出片后记 video.onetake_cuts；出片后自动压缩打 zip 经 cc-connect 发预览与拼图（不论闸门过没过）；whens 按剧级策略强制一镜到底
- tools/motion_check.py — 新增边缘重合剪切检测（< 0.6 报疑似剪切），6 条 Lina 片子实测 4 处真剪切全中、无误报
- tools/qc_pre.py — keyframe.framing_match（开场图 / 峰值图边缘重合 ≥ 0.62）、spec.onetake 机检；tools/qc.py — forced_when：剧级 skill_video_onetake 时 skills/ 下出片一律按一镜到底查
- ai_videos/dota_yingxiong/qc_checks.toml — [policy] wait_user_feedback_after_render / skill_video_onetake；新检查 keyframe.framing_match、spec.onetake；2_世界观人设/skills/README.md — 剧级记两条新规则
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/skills/k421_Dragon_Slave — 规格改双手推出、一次掠过、火鸟一发射就直线朝食尸鬼飞、正侧面平拍；开场图 v4、峰值图 v4–v7（以开场图为底图）；v1 / v2 user_feedback.md；v2 renders/20261030-165659_8a983f1d + review.md
- tools/tests/test_skill_run.py — 反馈闸门、剪切检测、强制一镜到底等 6 个新测试

验证: pytest test_skill_run/test_qc/test_qc_review/test_skill_pack_timeline/test_followup 45 passed；k421 v2 8a983f1d 一镜到底机检通过（无剪切）、已发用户并收到反馈；k421 v3 已过出片前闸门（取景重合 0.67，locked_traits 按用户「这几项先放行」记）并提交，出片后自检与发预览由总控自动完成——续做与用户反馈另开条目
费用: k421 v2 192 积分、v3 约 192 积分；Codex 出图 5 张（订阅额度）

No conflicts found in: 未改仓库级登记表与共用 skill 正文；一镜到底 / 等反馈两条只放剧级


## Follow-up 293 — 2026-10-30 07:35:56
Source: user_input/follow_ups/202610.md - section 293
Summary: 接续 292：修复 UV 转移计算路径，继续密室与岩壁质量检查；v022 全景等待系统提交额度，openweb 关闭许可仍未获得。

Auto-updated:
- ai_videos/dota_yingxiong/0_research/map_regions/blender 与 map_3d — 分段续跑记录：r49 独立审稿 fail 4；59 个 LOD 候选库已完成，已看部分对照并拒用退化版；总装 remap 失败待续修。

验证: 部分完成，未交付。manual_work_r25.json 记录 1/59 验收；batch_state 显示 59 库候选，地图保存报 Library remap incomplete。未把候选或队列完成计为资产验收。

No conflicts found in: （未单独核查）


## Follow-up 297 — 2026-10-31 10:38:12
Source: user_input/follow_ups/202610.md - section 297
Summary: 接续 293：限时任务、检查 LOD 候选与修复地图外部库映射。

Auto-updated:
- ai_videos/dota_yingxiong/0_research/map_regions/blender/build_map_lod_batch.py、finish_map_lod_preview.py — 单项 20 分钟、内存等待 2 分钟；超时停止本任务子进程并记录跳过，镜头失败继续下一镜头。
- ai_videos/dota_yingxiong/0_research/map_regions/blender/save_map_with_lod_libraries.py — 仅允许覆盖审计中未使用的 7 类野怪库缺席，未审或拒用 LOD 保留原库。
- ai_videos/dota_yingxiong/2_世界观人设/background/map_3d — 59 类候选均有决策：35 类可作远景、20 类拒用、4 类未改几何；assembly_working_v022_lod_v004.blend 已保存。manual_work_r26.json 与 checkpoint 记录真实进度。

验证: 分段完成，未交付。3 个脚本 AST 通过；地图保存实跑成功，959776742 字节；新进程重开/资源检查运行中，后台 PID 36936，当前子进程 19780。尚无优化版整图预览或独立验收；精细资产验收仍 1/59。

No conflicts found in: （未单独核查）


## Follow-up 298 — 2026-10-31 19:24:03
Source: user_input/follow_ups/202610.md - section 298
Summary: Claude 接手 3D 地图：先修总装管线，再按区域精修

Auto-updated:
- ai_videos/dota_yingxiong/0_research/map_regions/blender/ — 新增 render_region_eye.py（区域贴地机位只读出图、按机位临时设太阳）、patch_lane_surface.py、recolor_asset_library.py、remap_asset_libraries.py、stage_demo_wave.py；2_世界观人设/background/map_3d/ — assembly_working_v022_lod_v004_m1_v001–v005.blend（源 v022_lod_v004 未改）、lod_libraries/m1_recolor_v001/{bg16,m2}、m1_recolor_v002/m3（原库不改）、regions/M1/ 检查图与 README、demo 站位 json

验证: 按用户定的标准 A（3D 作出片参考）：Codex 上午已修通 LOD 版保存与全景（未记 changelog），本条接续。M1 贴地机位逐张看图：兵道由白砂岩改夯土；树人黑柱查明为逆光（贴图齐、高 1.92 m）；7 个 M1 模型实测高度与 scale_table 一致；bg16/m2/m3 重着色单体与地图内看图通过作者目检；demo 常规波（4 食尸鬼+2 亡灵法师+英雄占位）首版英雄被塔挡已弃，v005 侧拍整组入画、朝向正确。未做独立审稿；58/59 类精模验收状态不变。
费用: 本地 Blender CPU 渲染；无收费服务、无 Hyper3D、无 Codex 出图

No conflicts found in: 只新增脚本与新版本文件；Codex 产物与 current_status.json 未改；其他会话改动保留


## Follow-up 299 — 2026-11-01 10:47:28
Source: user_input/follow_ups/202611.md - section 299
Summary: 给 M1 总装做轻量查看版：外部库与本地重网格减面、贴图降到 1024，另存 light_v001 库与 _light 总装；原文件不动

Auto-updated:
- 0_research/map_regions/blender/make_light_map.py；map_3d/lod_libraries/light_v001/（52 库）；map_3d/assembly_working_v022_lod_v004_m1_v005_light.blend；regions/M1/README.md

验证: 后台打开 51.6 s→16.4 s；面数 7220 万→675 万；轻量版 demo_side 渲染与完整版构图一致，近景树叶略稀偏暗
费用: 本地 Blender，无收费服务

No conflicts found in: （未单独核查）


## Follow-up 302 — 2026-11-01 12:08:07
Source: user_input/follow_ups/202611.md - section 302
Summary: 剧级流程：任何英雄的改动（出片、改图、改卡后出新条、剪 demo）收尾后，直接给用户该英雄预览页链接并说明看哪几条；写进 README 预览页条、demo_standard §4 验收、skills/README 出片后反馈节。

Auto-updated:
- ai_videos/dota_yingxiong/README.md — 英雄预览页条加英雄级流程：任何英雄改动做完即给预览链接、写明新出哪几条与状态
- ai_videos/dota_yingxiong/demo_standard.md §4 — 交片给预览页链接
- ai_videos/dota_yingxiong/2_世界观人设/skills/README.md — 出片后反馈节改为先给预览链接、cc-connect zip 为补充

验证: 三处文字已写入并核对；只放剧级，未改仓库级规则与管理应用代码（预览页由另一会话管理应用 follow-up 312 实现）

No conflicts found in: README 第 30 行原预览页约定（管理应用 follow-up 312）只扩展不改义


## Follow-up 303 — 2026-11-01 12:09:14
Source: user_input/follow_ups/202611.md - section 303
Summary: 仓库级（用户明确要求以后都这样）：CONVENTIONS 新增「给用户的文件路径一律写完整绝对路径」

Auto-updated:
- CONVENTIONS.md 新增「给用户的文件路径一律写完整绝对路径（2026-11-01，用户定）」节

验证: 条文已写入，Claude/Codex 共用入口经 AGENTS.md 路由读取
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 300 — 2026-11-01 11:34:14
Source: user_input/follow_ups/202611.md - section 300
Summary: Tiny demo 按 demo_standard.md 重做到 ≥ 65 s：亮相重出 12 秒；四技能现合计 33.2 s，加长重出到合计 ≥ 53 s；时长预算写进人物卡，按新出片与自检流程（qc_pre、一镜到底、出片后等用户反馈）走。

Auto-updated:
- c2_Stone_Giant.md — turntable 改 12 秒（起势/收势）、新增 demo 时长预算（13+13+12+12=50 s，加停顿 54 s）、12 秒亮相验收记录；旧 10 秒版留 source/
- skills/k21–k23 — 技能视频 prompt 加长重写（起势 1.5 s、多挨几下、收势 2 s、逐拍视线、一镜到底）；planning/ 新开场图 k21/k22/k23_start_v1、峰值图 k21_peak_v2、k22_peak_v2、k23_peak_v2（Codex）；旧条 user_feedback.md 记用户 179 定版原话
- ref/skills — 补 6.85k 山崩实机截帧 dota1_k21_*；ref/model Reforged 图标移入 _excluded_reforged/
- renders：k21 23ddf8e9、k22 0de2e33c、k23 bb06e1ce + review.md；亮相 b3d69c87

验证: 亮相 12.06 s 代理看图通过（motion_check 1.5–3.5 s 判误报）；出片前闸门三轮，用户放行 keyframe.scale / ref_image.identity / ref_image.version / keyframe.locked_traits 后提交；三条出片后一镜到底与流畅机检通过，但出片后多视角审稿闸门均不通过（k21 洪流翻滚弱、k22 B/C 离地与抓举停顿、k23 开场背对与头发发蓝）；按剧级策略停在等用户反馈，已给预览链接；cc-connect 未运行，zip 预览未发；demo 未剪
费用: 亮相约 216 积分；三条技能 720p（13/13/12 s）以 request_log 回执为准；Codex 出图 7 张（订阅额度）

No conflicts found in: k24 162 版不动；未改仓库级规则


## Follow-up 304 — 2026-11-01 13:38:44
Source: user_input/follow_ups/202611.md - section 304
Summary: Tiny demo v4：12 秒亮相 + k21 23ddf8e9 / k22 0de2e33c / k23 bb06e1ce（出片后闸门未过、待用户定）+ k24 575b74f9，按 demo_standard §3 拼成成片（不重叠压暗、首尾 0.5 s 停顿、英文标题卡与角标、片尾淡出），给预览链接供用户看整体。

Auto-updated:
- c2_Stone_Giant/demo/edit/final/ep01_final_v4.mp4 + cut_v4.json + title_card_k2x_en.png（重生成）；c2 README demo v4 节；剪辑脚本 .audit/adhoc_agents/2026-11-01/tiny-demo-300/tiny_cut_v4.py

验证: ffprobe 66.327 s；四条技能含停顿 54.24 s（≥ 53）；1 fps 拼图核对亮相、四张英文标题卡、角标、压暗转场、片尾淡出；k21–k23 出片后闸门未过照实标注；未试听、未独立冷看、未锁片
费用: 无收费服务（本地 ffmpeg）

No conflicts found in: v3 旧定版与 publish.md 不动


## Follow-up 301 — 2026-11-01 12:02:53
Source: user_input/follow_ups/202611.md - section 301
Summary: 沙王重出 k751 与 k754：k751 按 demo_standard 加起势收势、钻地与尖刺更清楚、眩晕标记缩到原版约 1.65 秒，新时间轴先交审；k754 用 10-27 已认可的修订时间轴 e69a94451773，过出片前独立审稿后提交。

Auto-updated:
- c75_Sand_King/skills/k751_Burrowstrike/k751_Burrowstrike.md — 新 10 秒时间轴 4854d151aff2（用户认可）：中景、起势铲刃护身、四根粗骨节刺、右侧钻出、眩晕只在头顶 1.65 s、对打、收势；开场图 planning/k751_start_v301f.png、同机位眩晕峰值图 planning/k751_peak_v301.png；旧卡 _history/k751_Burrowstrike_card_301.md
- c75_Sand_King/skills/k754_Epicenter/k754_Epicenter.md — 开场图 planning/k754_start_v301b.png、同机位峰值图 planning/k754_peak_v301b.png；光环改宽的半透明发光脉冲带、去掉负面词能量波（用户选，重记认可 18d52db2b07f）；要求行补一镜到底；减速画法；旧卡 _history/k754_Epicenter_card_301.md
- c75_Sand_King/c75_Sand_King.md — 时长预算 k751 行改 10 s 重出
- renders：k751 20261101-132227_86911e41、20261101-134345_4ee1757b；k754 20261101-134440_b6dd0b30（各含 sheet_4fps、qc.json、review.md）
- c75_Sand_King/skills/k751_Burrowstrike/k751_Burrowstrike.md — 时间轴 771b7acfd788（用户「好的」）：先对打、不规则倒钩骨刺、瞬出瞬收、树人落地即死（去掉眩晕）；峰值图 planning/k751_peak_v301b.png；旧卡 _history/k751_Burrowstrike_card_301.md、_301b.md
- c75_Sand_King/skills/k754_Epicenter/k754_Epicenter.md — 开场图 v301b、同机位峰值图 v301b、宽发光脉冲带（时间轴 18d52db2b07f）
- renders：k751 86911e41、4ee1757b、5358b638；k754 b6dd0b30（各含 sheet_4fps、qc.json、review.md、user_feedback）
- c75_Sand_King/demo/edit/final/ep01_final_v4.mp4、v5.mp4 + cut_v4/v5.json（65.37 s，技能含停顿 53.28 s）；脚本 .audit/adhoc_agents/2026-11-01/sandking-demo-301/sk_cut_v4.py、sk_cut_v5.py

验证: 出片前闸门余项均为用户放行；出片后 motion_check 无真慢动作；qc_review + qc.py gate：k751 三条、k754 一条均不通过（见各 review.md），交用户看；demo v5 用 1 fps 拼图核对 v4 结构；声音未核听；未锁片
费用: 即梦 k751 180+180+168（ac48ba61 TranscodeFail 无产出，扣费情况未核）＋k754 228；Codex 出图十余张为订阅额度；demo 剪辑本地 ffmpeg 不收费

No conflicts found in: 共用 skills / CONVENTIONS 未改；落地即死只写在本剧 k751 卡

## Follow-up 307 — 2026-11-01 13:48:28
Source: user_input/follow_ups/202611.md - section 307
Summary: Tiny demo v4 用户定版：k21–k23 新条记用户接受反馈；cut_v4.json 状态定版；README 与 publish.md 改为 v4（66 s，时间点 0:12/0:26/0:40/0:53）；转 Lina。

Auto-updated:
- c2 skills k21–k23 新条 user_feedback.md 记用户接受；demo/edit/final/cut_v4.json 状态定版；c2 README 定版节；demo/publish.md 改 v4（66 s、时间点 0:12/0:26/0:40/0:53、封面 0:57）

验证: publish.md 无残留 51 秒 / v3 时间点；声音未人工试听（发布前需听）
费用: 无

No conflicts found in: v3 及旧审阅包保留


## Follow-up 306 — 2026-11-01 13:44:38
Source: user_input/follow_ups/202611.md - section 306
Summary: 写 vlog 系列构思稿 v0：人设、拍法、8 集路线、第 1 集节拍，待用户定

Auto-updated:
- ai_videos/dota_yingxiong/vlog/concept.md（构思稿 v0）

验证: 构思稿已写，含人设依据（原台词、英雄卡）、8 集路线与 3D 地图准备度、第 1 集节拍、4 个待定项；待用户定
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 309 — 2026-11-01 15:05:37
Source: user_input/follow_ups/202611.md - section 309
Summary: 沙王 demo v5 定版（65.37 s：12 秒亮相 + k751 5358b638 / k752 3e5f25c9 / k753 42462616 / k754 b6dd0b30），出片后闸门未过项由用户放行；发布文案按 v5 更新。

Auto-updated:
- c75_Sand_King/demo/edit/final/cut_v5.json status 定版；cut_v4.json 标被取代
- c75_Sand_King/demo/publish.md — 视频改 v5、65 秒、时间点 0:00/0:12/0:23/0:34/0:49、封面建议；v3 版存 c75_Sand_King/_history/publish_v3.md
- c75_Sand_King/c75_Sand_King.md — 状态行 v5 定版、预算表实测值
- k751 5358b638、k753 42462616、k754 b6dd0b30 qc.json：未过项 qc.py override（用户原话），k753 补记 onetake_cuts 机检

验证: 三条 qc.py gate --when 一镜到底 均通过（用户放行）；demo v5 ffprobe 65.37 s、技能含停顿 53.28 s；声音与台词未核听，发布前需人工试听
费用: 0（本地操作）

No conflicts found in: v3 文件保留不删


## Follow-up 308 — 2026-11-01 14:13:13
Source: user_input/follow_ups/202611.md - section 308
Summary: Lina 四技能按用户意见改卡重出：k421 前后食尸鬼数量一致；k422 双手向前推出火焰、落点地面瞬间起火；k423 出清楚的片；k424 只一只远处食尸鬼、强力瞬间电击原地秒杀。出片后给预览链接，再剪 demo。

Auto-updated:
- c42 skills k421–k424 卡按用户意见改（k421 24mm 远景、三只一致；k422 双手推出地面瞬间起火；k423 两手同大小火、删对称；k424 一只远处、粗闪电一击秒杀，15→12 s）；c42 卡 demo 时长预算（50 s + 停顿 = 54 s）
- planning：k421_start_v6 / peak_v9–v11、k422_peak_v3、k423_peak_v4–v5、k424_start_v4 / peak_v3（Codex）
- renders：k421 4ed76ef9、k422 97e33479（b3518d16 服务端失败归档 _failed/）、k423 4cf5129a、k424 fe921876，各写 review.md；旧条 user_feedback.md 记用户意见
- demo/edit/final/ep01_final_v1.mp4 + cut_v1.json（66.3 s，四条含停顿 54.24 s）；剪辑脚本 .audit/adhoc_agents/2026-11-01/lina-demo-308/lina_cut_v1.py

验证: 出片前闸门按用户放行（体型、原版参考、静态细节、远景视线）后提交；四条出片后多视角审稿闸门均未过（偏差见各 review.md），按剧级策略等用户反馈；demo 1 fps 拼图核对结构；未试听、未锁片；cc-connect 未运行，只给预览链接
费用: k421 192、k422 204、k423 约 204、k424 192 积分（以 request_log 回执为准）；k424 首次与 k421/k422 首次提交为上传/网络失败不扣费；k422 b3518d16 服务端失败扣费情况未知

No conflicts found in: 未改仓库级规则


## Follow-up 310 — 2026-11-01 15:09:32
Source: user_input/follow_ups/202611.md - section 310
Summary: 6.83d 全部商店物品立卡出锚点图，建立商店/NPC→道具货单

Auto-updated:
- ai_videos/dota_yingxiong/0_research/item_refs/ — 新建：132 件物品各一目录，DotA1 PlayDotA 存档图标 128 张、Dota2 CDN 图标 132 张、refs.md 132 份、README、_fetch_results.json
- ai_videos/dota_yingxiong/2_世界观人设/props/registry.toml — props_lib.allocate 领号 p122–p232（111 件，story）
- ai_videos/dota_yingxiong/2_世界观人设/props/中立_neutral/p122…p232_*/ — 111 张新卡 + asset.toml + 锚点图 png（Codex 内置出图，零参考），卡末生成记录含 sha/codex_thread/审图结论；p128/p154/p155/p159/p185/p230 旧候选留 _v1
- ai_videos/dota_yingxiong/2_世界观人设/props/shop_items.json, shop_items.md — 新建：16 个出售方→道具货单与道具→出售方反查（d08 §1.1/§2）
- characters/中立_neutral/m300–m309、m7；background bg22/bg23/bg32/bg33/bg36 卡 — 末尾追加「售卖道具 / 掉落道具（follow-up 310）」节
- ai_videos/dota_yingxiong/2_世界观人设/assets_index.md — 道具计数改 231/中立 152；取消「被动属性装不立卡」；新增「商店物品」小节 p122–p232
- ai_videos/dota_yingxiong/README.md — 新增商店物品与货单状态段

验证: 111 张新图全部经 fresh-context 独立看图审（对照卡 Shot 外观/验收 + DotA1 图标）：首轮 p128 裁切、p159 裁切、p185 铁箍、p230 獠牙数、p154 护腕短不过，p155 左右脚改进；改 prompt 重出后复审通过，p154 第二次重出只主代理复核。Codex 网络断开 16 次失败均查 generated_images 无产物后重跑。shot_pack sync --all、workflow_catalog --check rc=0；test_asset_groups 18 passed。未经用户看图；旧 21 张卡未按新参考复核。
费用: Codex 订阅额度内置出图约 135 次调用，费用字段未返回（未知）

No conflicts found in: （未单独核查）


## Follow-up 305 — 2026-11-01 13:44:38
Source: user_input/follow_ups/202611.md - section 305
Summary: c41 冰女改高挑长腿、更有女性魅力的合身剪裁：改卡与比例表，Codex 重出立绘（先给用户看），认可后重出 12 秒亮相；评估四技能条是否需重出

Auto-updated:
- c41 卡（真人化/外观/锁定描述/立绘与亮相 prompt 改高挑长腿、收腰低领、古典脸）；scale_table.md c41 1.68→1.75 m；立绘 v305e 定稿替换 c41_Crystal_Maiden.png（旧图 _before_305.png）；12 秒全身亮相 568fb2f9 替换 turntable，半身版与原片留 source/；三视图重截并重建合图（旧图 views/before_305/）；k411 开场/峰值图 v14/v13；k412/k413 时间轴审阅记录；三条上版用户反馈；k411 framing_match 用户放行

验证: 立绘经用户三轮看图定稿；全身亮相 1/5 fps 抽帧初审全身入画，台词口型未人工核听、未独立审稿；技能三条出片前独立审稿未过（视线、参考版本、关键帧缺失等，k411 另有一审稿人调用失败），未出片，待用户选「放行」或「补齐」；demo v6 未剪
费用: Codex 出图 5 次成功 2 次 sexual 拦截（订阅额度）；即梦亮相：b1 半身 1 条成功、3 次上传阶段失败未生成、568fb2f9 全身 1 条成功，积分以账户为准（约 2×180）；技能条未提交

No conflicts found in: （未单独核查）


## Follow-up 311 — 2026-11-01 15:27:11
Source: user_input/follow_ups/202611.md - section 311
Summary: Lina：k422 97e33479、k424 fe921876 用户接受；k421 重出——死前可着火乱转，死后完全不动；k423 重出——一开场就放法术触发炽魂，多几只食尸鬼连打体现攻速快；出片后重剪 demo v2 给预览链接。

Auto-updated:
- c42 k421 卡：死后像石头一样定住（规则 + 负面词）；k423 卡：1.3 s 放法术、六只、每只两下、两近两远依次倒下；planning k423_start_v4–v5 / peak_v6–v7
- renders：k421 43012aeb、k423 1414c4ad + review.md；k422 97e33479 / k424 fe921876 记用户接受
- demo/edit/final/ep01_final_v2.mp4 + cut_v2.json（66.3 s，四条含停顿 54.24 s）；脚本 .audit/adhoc_agents/2026-11-01/lina-demo-308/lina_cut_v2.py

验证: k423 1414c4ad 出片后闸门通过、代理看图确认；k421 43012aeb 出片后闸门未过（火鸟竖起），拼图未见死后转向；demo 结构同 v1；未试听、未锁片
费用: k421 192、k423 约 204 积分（以 request_log 为准）

No conflicts found in: k422 / k424 不重出


## Follow-up 313 — 2026-11-01 15:48:52
Source: user_input/follow_ups/202611.md - section 313
Summary: 斧王 v9、全能骑士 v5、宙斯 v3、冰女 v5 的 publish.md 按当前定版成片更新时长、时间点与文案；旧版存 _history

Auto-updated:
- c65_Axe、c3_Omniknight、c40_Lord_of_Olympus、c41_Crystal_Maiden 的 demo/publish.md；旧版存各自 _history/publish_v{8,4,1,2}.md

验证: C:/Program Files/Git/api/demo-status 7 位定版英雄 publish_state 全部 ok；四份文案的时间点按 cut 的 events.start 取整核对，CK/沙王/小小三份原已对上也逐条核过；新亮相台词未人工核听，文案里已注明

No conflicts found in: （未单独核查）


## Follow-up 315 — 2026-11-01 20:02:54
Source: user_input/follow_ups/202611.md - section 315
Summary: Lina k423 炽魂：法术在 1.0 s 食尸鬼还在约二十米外时就放（火柱炸在远处），后续燃火与连发整体提前；重出后重剪 demo v3 给预览链接。

Auto-updated:
- c42 k423 卡：去掉开头停顿，1.0 s 远处放火柱，燃火与连发提前约 0.4 s；负面词补「冲到跟前才施法」
- renders：k423 f54a250e + review.md（前一次审稿进程因 Windows 临时目录占用崩溃，重跑）
- demo/edit/final/ep01_final_v3.mp4 + cut_v3.json（66.3 s）；脚本 .audit/adhoc_agents/2026-11-01/lina-demo-308/lina_cut_v3.py

验证: 拼图确认约 1.5 s 远处火柱、最前两只未冲近；出片后闸门未过（燃火后约 2 s 空档、手部火形）；demo v3 输入四条核对；未试听、未锁片
费用: k423 约 204 积分（以 request_log 为准）

No conflicts found in: 其余三条不动


## Follow-up 312 — 2026-11-01 15:29:32
Source: user_input/follow_ups/202611.md - section 312
Summary: 影魔 k861 / k863 / k864：体型按卡（树人 4 倍）放大、开场图锁比例；树人冲刺与技能释放提速（写死距离与到达秒数）；改时间轴先交审，再过出片前闸门后重出。

Auto-updated:
- c86_Shadow_Fiend/skills/k861_Shadowraze — 12 秒三轮九发时间轴 de7b494441a3（用户认可；去掉旧事件图标注后重记）；开场图 planning/k861_start_v312b.png（拼图草图锁四倍）；视线 / 角色反应行；旧卡 _history/k861_Shadowraze_card_312.md
- c86_Shadow_Fiend/skills/k863_Presence_of_the_Dark_Lord — 11 秒全速冲、每 0.7 秒一发时间轴 9e0eba129485；开场图 planning/k863_start_v312b.png；视线行；旧卡 _history/k863_card_312.md
- c86_Shadow_Fiend/skills/k864_Requiem_of_Souls — 12 秒边挨打边蓄力时间轴 f7e850f52ffc；开场图 planning/k864_start_v312.png、事件图 planning/k864_pillars_v312.png；视线行；旧卡 _history/k864_card_312.md
- c86_Shadow_Fiend.md — 时长预算 53.05 s、demo v2 记录
- renders：k861 ee7c785c、k863 82636f37、k864 a3adb4a8（sheet、qc.json、review.md）；demo/edit/final/ep01_final_v2.mp4 + cut_v2.json（63.35 s，技能含停顿 53.25 s）；剪辑脚本 .audit/adhoc_agents/2026-10-24/sf-research-154/sf_cut_v2.py
- ai_videos/dota_yingxiong/2_世界观人设/characters/request_log.md — 补记一次未先写日志的 dreamina user_credit 查询（事后补记，如实注明）

验证: 出片前：qc_pre machine 通过，qc_review --pre 余项用户放行；出片后：motion_check k864 4–5 s 慢动作嫌疑（蓄力段），k861 / k863 无；qc_review + qc.py gate 三条均不通过（见 review.md）；demo v2 合成；声音未核听；未锁片
费用: 即梦：k861 ee7c785c、k864 216、k863 82636f37（积分见各 generation.json）；k863 首次提交网络超时未扣费；Codex 出图约十张为订阅额度

No conflicts found in: 共用 skills / CONVENTIONS 未改


## Follow-up 316 — 2026-11-01 20:14:16
Source: user_input/follow_ups/202611.md - section 316
Summary: 删除全剧 Dota 2 图标与参考；物品卡改为只依据 DotA 1 / War3 图标，借鉴过 Dota 2 的重写重出；补缺的 DotA 1 图标；复核 p7–p28 旧卡；商店指针与货单 UI；剧级流程写入严格 DotA 1 规则

Auto-updated:
- （待补：执行后用 `python tools/followup.py done` 写入）

验证: （待补）

No conflicts found in: （待补）


## Follow-up 317 — 2026-11-01 20:26:32
Source: user_input/follow_ups/202611.md - section 317
Summary: Lina demo v3 用户定版：k421 43012aeb、k423 f54a250e 记用户接受；cut_v3.json 状态定版；新建 demo/publish.md（v3 时间点 0:12/0:25/0:39/0:53）；人物卡记 demo 定版。

Auto-updated:
- c42 skills k421 43012aeb / k423 f54a250e user_feedback.md 记用户接受；demo/edit/final/cut_v3.json 状态定版；demo/publish.md 新建；c42 卡 demo v3 定版节
- specs changelog：本会话误对他会话的 follow-up 316 执行 done（followup.py done 在 _inbox 按编号取条目、不核对归属），已把 316 恢复为待补骨架，原指令 / 摘要未动

验证: publish.md 时间点按 cut_v3.json 段起点（12.064/25.128/39.184/53.24 s）；声音未人工试听（发布前需听）；316 已复原为待补
费用: 无

No conflicts found in: v1 / v2 保留


## Follow-up 319 — 2026-11-01 20:34:58
Source: user_input/follow_ups/202611.md - section 319
Summary: 剧级流程：每个英雄 demo 定版时必须同时新建或更新 demo/publish.md（视频版本、时长、时间点按 cut_vN.json 段起点、封面建议、台词，各平台文案与 AI 标注），换定版版本就同步改；写进 demo_standard §4 与 README 英雄级流程。

Auto-updated:
- ai_videos/dota_yingxiong/demo_standard.md §4 — 定版必写 / 同步更新 demo/publish.md（格式照 Tiny / Lina）
- ai_videos/dota_yingxiong/README.md 英雄级流程 — 定版同一轮写好 publish.md，交片链接一并提到

验证: 核对全部英雄 demo：已定版的 c2 / c3 / c40 / c41 / c42 / c60 / c65 / c75 的 publish.md 都指向最新 cut 版本；c63、c86 未定版、尚无 publish.md（定版时按新规则写）
费用: 无

No conflicts found in: 只放剧级，未改仓库级


## Follow-up 318 — 2026-11-01 20:31:30
Source: user_input/follow_ups/202611.md - section 318
Summary: 影魔身高改树人 2 倍（人物卡 3.8 m，改体型＝改卡）；k861 每发双手明显抬起、树人更快；k863 只来 3 个树人、进光环防御降低、挥手一下一个；k864 魂柱冲天高。开场图按 2 倍重出，时间轴交审后重出。

Auto-updated:
- c86_Shadow_Fiend.md — 身高改 3.8 m（树人两倍，撤 272 的四倍）；亮相改 12 秒并重出 19ea274e（旧 10 s 存 source/c86_Shadow_Fiend_turntable_10s.mp4）；demo v3 记录；旧卡 _history/c86_Shadow_Fiend_card_318.md；scale_table 重生成
- k861：每发双臂高举、树人每秒约五步狂奔，开场图回 planning/k861_start_v10.png（时间轴 c062db83c4db）
- k863：只来三个树人、进光环树皮开裂（防御降低）、挥手一下一个；开场图回 planning/k863_start_v4.png；光环半径 8 m、收势 1.5 s（时间轴 384f570a97ec）
- k864：灵魂柱冲天约三十米（含锁定特效段）；开场图 planning/k864_start_v318.png、事件图 planning/k864_pillars_v318.png（时间轴 4a5f7e9f29a7）
- renders k861 33234d24、k863 384508f4、k864 163095fa（sheet、qc.json、review.md）；demo/edit/final/ep01_final_v3.mp4 + cut_v3.json（65.34 s）；脚本 .audit/adhoc_agents/2026-10-24/sf-research-154/sf_cut_v3.py

验证: 时间轴用户认可（「可以」）；出片前闸门余项按用户放行口径放行（规格自相矛盾项先改）；motion_check：k864 蓄力段慢动作嫌疑，余无；qc_review + gate 后台运行；亮相 motion_check 无慢动作、无剪切；声音未核听；未锁片
费用: 即梦：亮相 19ea274e（积分见 request_log）＋k861 216＋k863 198＋k864 216；Codex 出图三张为订阅额度

No conflicts found in: 共用 skills / CONVENTIONS 未改


## Follow-up 321 — 2026-11-01 21:35:22
Source: user_input/follow_ups/202611.md - section 321
Summary: 影魔 k861 树人更快、影压落点整体远推（树人远处就打）；k863 光环范围加大、树人不停顿冲上来就攻击影魔；k864 魂柱从脚下中心瞬间向四周炸开扩散；改时间轴交审后重出。

Auto-updated:
- k861：落点远推 20/15/10 m、树人每秒约六步（时间轴 e459c79c7b35）；旧卡 _history/k861_card_321.md
- k863：光环半径约 15 m、树人不停顿冲上来就抽、近身挥爪一扫一个，去掉远程飞弹（时间轴 cf041b82bd4f）；旧卡 _history/k863_card_321.md
- k864：释放拍改为中心一束冲天后半秒内向四周炸开；事件图 planning/k864_burst_v321.png（时间轴 cfa42cda3126）；旧卡 _history/k864_card_321.md
- renders k861 18b42792、k863 1d6f4cd4、k864 2131385c（sheet、qc.json、review.md）；demo/edit/final/ep01_final_v4.mp4 + cut_v4.json（65.34 s）；脚本 .audit/adhoc_agents/2026-10-24/sf-research-154/sf_cut_v4.py

验证: 用户「重出视频」授权直接出片（时间轴按此登记）；出片前闸门余项按用户放行口径放行；motion_check 三条无慢动作、无剪切；出片后 qc_review + gate 后台运行；demo v4 合成；声音未核听；未锁片
费用: 即梦三条（积分见各 generation.json 与 request_log）；k863 下载失败只重下未重提；Codex 出图一张为订阅额度

No conflicts found in: 共用 skills / CONVENTIONS 未改


## Follow-up 320 — 2026-11-01 20:37:14
Source: user_input/follow_ups/202611.md - section 320
Summary: 树精卫士 k12/k13/k14 按用户意见改卡与时间轴，交审后再出片

Auto-updated:
- k12/k13/k14 技能卡、资料包、qc_pre.json、各条 review.md / qc.json / user_feedback.md

验证: 按用户意见改 k12/k13/k14 卡与时间轴，出片前审稿多轮修正；出片 k12 aac714b5（228）、k13 08de8f0c（204）、k14 2fb03cf8（192），代理自检与出片后审稿均不合格，交用户看后转 follow-up 322；k12 另用 Codex 出新开场图 k12_start_v4.png
费用: Dreamina 624 积分；Codex 出图 1 张（订阅额度）

No conflicts found in: （未单独核查）


## Follow-up 322 — 2026-11-01 22:21:05
Source: user_input/follow_ups/202611.md - section 322
Summary: 树精卫士 k12 跟拍追逐、六波脉冲吸取（查原版 6.83：6 次脉冲、4.5 秒、减速 28%）；k13 两只全程在画且攻击统一；k14 第一帧起匀速冲杀、0.5 s 起手、勒紧每秒一下；改卡后重出

Auto-updated:
- k12/k13/k14 技能卡、资料包、qc_pre.json、各条 review.md / qc.json

验证: 按用户意见改卡（k12 跟拍追逐+六波脉冲，原版查证 iCCup 6 次/4.5 s/减速 28% ⚠️单源；k13 两只全程、攻击统一；k14 匀速冲杀、0.5 s 起手、1 秒一勒）后重出：k12 cc0530bc（228）、k13 f3e9468a（204）、k14 feffe154（192）；motion_check k12/k13 通过、k14 慢动作嫌疑；出片后独立审稿三条闸门均不通过，偏差写入各条 review.md，交用户定；k14 出片前 agency 放行误套 k13 理由，已在 qc_pre.json 与 defects.jsonl 更正
费用: Dreamina 624 积分

No conflicts found in: （未单独核查）


## Follow-up 323 — 2026-11-01 22:26:40
Source: user_input/follow_ups/202611.md - section 323
Summary: 影魔 k861 树人冲刺写死速度与到达秒数；k863 光环半径远推、影魔远处就远程攻击冲来的树人；k864 魂柱始终竖直 90 度、整根水平从中心快速平移扩散；事件图重出。

Auto-updated:
- k861：冲刺写死每秒约八步、一秒冲过约八米（时间轴 7d72f70af3c1）；k863：光环半径约 25 m、恢复远程飞弹、约 20 m 外打碎（325727600c8e）；k864：魂柱始终竖直、整圈水平平移扩散，事件图 planning/k864_vertical_v323.png（9757553061a4）；旧卡 _history/*_card_323.md
- renders k861 b1d0a443、k863 7073f249、k864 8172a952（sheet、xt_charge、qc.json、review.md）；demo/edit/final/ep01_final_v5.mp4 + cut_v5.json（65.34 s）；脚本 sf_cut_v5.py

验证: 用户「改好后重出视频」授权直接出片；出片前闸门余项按用户放行口径放行；motion_check：k861 时空切片树人约 2–3 m/s 仍全局偏慢、k864 蓄力段慢动作嫌疑；qc_review + gate 三条均不通过；声音未核听；未锁片
费用: 即梦 216＋198＋216＝630 积分；Codex 出图一张为订阅额度

No conflicts found in: 共用 skills / CONVENTIONS 未改


## Follow-up 314 — 2026-11-01 19:55:05
Source: user_input/follow_ups/202611.md - section 314
Summary: vlog 定 16:9、全英文无字幕、可多位客串；第 1 集从近卫基地开始：构思稿记决定，3D 总装近卫基地区域按 M1 办法出检查图并精修

Auto-updated:
- vlog/：concept.md（v1 决定、人设）、series.md（寻盾线降为里程碑）、synopsis.md、synopsis_ladder.md（全剧短中长对照）、season01_synopsis.md、lore_war.md（灵脉资源战争）、lore_home.md（法器+传承书）、world_globe.md（星球、两端、三条大道、赤道河）、base_world.md（近卫城扩展、NPC）、research_kaldorei.md（暗夜精灵设计参考，未联网核对）、01_crossing/story.md（穿越故事稿 v1）、01_crossing/refs/（现代造型 v3、冰洞、法器与书、泉水 v3 等 Codex 参考图）；0_research/map_regions/blender/render_region_eye.py 加 B1 近卫基地五机位与 look_z；regions/B1 检查图 5 张

验证: 设定与概要逐轮按用户意见改；参考图逐张看图，现代造型 v3、冰洞、道具、泉水 v3 用户认可（法器两图形制不一致、泉水岩峰偏中式，均已记录）；B1 检查图已渲染未逐张审；故事稿待用户 review
费用: Codex 出图 10 张（订阅额度）；无即梦/收费调用

No conflicts found in: （未单独核查）


## Follow-up 325 — 2026-11-02 00:03:11
Source: user_input/follow_ups/202611.md - section 325
Summary: vlog 穿越段补资产：德鲁伊医者人物卡与立绘、小树屋外观图（Codex 出图）；灵脉改为有限不必变弱、去掉摄像机电量设定、造型 v4 去相机

Auto-updated:
- ep01 资产登记（c113 旅行者卡、m310 德鲁伊医者、bg42/43/44、p233/p234）；filming 13 镜与 overhead、prompts 编译、资料包；c113 立绘换 v6（用户认可，旧版在 views/before_v6/）并由 Codex 重出三视图、重建 _views；s2 st2 按用户反馈改分镜（开场即湖、坐水边、居民远望、不回头）与人群种族（魔兽式精灵族 + 人族，不能有外星人感；规则写入 vlog/base_world.md §3）；同样人群描述加到 s3 st1/st2、s4 st1；decisions/filming.md 记录反馈

验证: 看图核对 c113 v6 立绘与正/侧/背三视图同一张脸、背面单人；shot_overhead --all 0 blocker 0 warning；prompts 编译通过（draft）；shot_pack sync updated 13；s2 st2 编译后 prompt 含精灵族/人族描述。重出的 s1 st1、s2 st2 草稿已提交，待看片
费用: Seedance 草稿：旧稿 s1 st1 84 + s2 st2 96 积分；m310 转台约 80 积分；本轮两条草稿约 180 积分（已提交）；Codex 出图走订阅额度

No conflicts found in: （未单独核查）


## Follow-up 326 — 2026-11-02 08:44:28
Source: user_input/follow_ups/202611.md - section 326
Summary: ep01 人群按近卫英雄种族写（暗夜精灵为主，夹人族、矮人、兽人；可扩牛头人、熊猫人、地精等），s2 st2 居民拉近到二三十米、岸上不下水；规则写入 vlog/base_world.md §3

Auto-updated:
- vlog/base_world.md §3 种族规则改为参考近卫英雄种族（精灵为主，人族、矮人、兽人，可扩牛头人、熊猫人、地精、巨魔、半人马、树人）并写明各族外观；episodes/ep01/filming.json：s2 st2 居民拉近到二三十米、各族可辨、站岸上不下水，s3 st1/st2、s4 st1 人群描述同步；overhead 视线目标改到 (374,566)；prompts 重新编译、资料包同步

验证: 种族名单对照 0_research/parts d02–d04 近卫英雄表；shot_overhead --all 0 blocker；prompts 编译通过；shot_pack check ok 13；4 个人群镜头的 prompt 含兽人/矮人描述。s2 st2 尚未按新描述重出（需用户点）
费用: 无（未调用收费服务）

No conflicts found in: （未单独核查）


## Follow-up 296 — 2026-10-30 19:00:08
Source: user_input/follow_ups/202610.md - section 296
Summary: k421 v3（正侧面平拍、峰值图 v7）出片后由总控自动自检并发预览，按剧级策略等用户反馈；k422 v2 / k424 v2 仍待用户反馈；k423 规格修好后出片；四条通过后剪 demo。

Auto-updated:
- ai_videos/dota_yingxiong/2_世界观人设/characters/近卫_sentinel/c42_Slayer/skills/k421_Dragon_Slave — 第 3 版 13355f57 出片并发用户；按用户反馈「火焰前后食尸鬼数量不一致」改为恰好三只、原地倒下、尸体数一致、掌心与火浪不相连；开场图 v5、峰值图 v8（取景重合 0.69）；review.md / user_feedback.md
- tools/qc_review.py — parse 取第一个合法 JSON 数组（尾巴文字曾让整次审稿崩）；tools/skill_run.py — 审稿记录缺失时即使 sha 未变也重审；tests 加解析回归

验证: test_qc_review / test_skill_run 22 passed；k421 v4 规格出片前闸门停在 keyframe.locked_traits（峰值图领头食尸鬼造型、掌心火流相连）与 spec.gaze（中间那只脸朝镜头）——未提交，待新会话接续
费用: k421 v3 192 积分；Codex 出图 2 张（订阅额度）

No conflicts found in: （未单独核查）


## Follow-up 327 — 2026-11-02 08:46:28
Source: user_input/follow_ups/202611.md - section 327
Summary: s1 st1 改为开场不见洞口、后揭示并转为好奇惊讶；剧级 qc 加 spec/video.reaction_matches_seen；重出 s1 st1、s2 st2 草稿；链接改为直达视频文件

Auto-updated:
- s1 st1 改为开场不见洞口、说完后视线越过镜头、镜头右转揭示洞口、表情转好奇惊讶（filming.json、overhead、episodes/ep01/story.md、vlog/01_crossing/story.md）；s2 st2 补写震惊与对各族居民的紧张好奇；剧级 qc_checks.toml 新增 spec.reaction_matches_seen / video.reaction_matches_seen，qc defect 已记；重出 s1 st1（683c107b）与 s2 st2（7755be8f）草稿

验证: shot_overhead --all 0 blocker；prompts 编译、shot_pack sync 对齐；抽帧看片：s1 st1 前 4 秒无洞口、结尾揭示洞口且表情惊讶，合格；s2 st2 有问题：开场露出靴子，5.75 秒处硬切到正面构图（她面朝镜头、人群在身后），精灵像白色石膏雕像（灰白皮肤），矮人、兽人、地精可辨
费用: Seedance 草稿 84 + 96 = 180 积分

No conflicts found in: （未单独核查）


## Follow-up 328 — 2026-11-02 10:41:44
Source: user_input/follow_ups/202611.md - section 328
Summary: 冰女 vlog ep01 s1：洞口不能一转头就看到（太快、太容易发现不合理）；改为多走几步→发现冰里微弱的光→走近用手使劲扒→冰面断裂→跌进山洞；开头用最短的方式交代「Day X of 某旅程」。改故事 / 分镜 / prompt，按剧级流程出草稿、自检、发用户等反馈。

Auto-updated:
- episodes/ep01/story.json（+ story.md、vlog/01_crossing/story.md 同步）— 场一改为 Day six of my Svalbard crossing 开场、走几步发现冰崖深处微光、扒冰、冰面塌陷摔进冰洞
- episodes/ep01/filming.json — s1 由 5 镜改为 7 镜（新 st1–st3，原 st2–st5 顺延为 st4–st7）；st1–st3 场景参考改为新建 bg42-1；scenes/s1/shots 目录顺延、新 st1–st4 overhead.toml；prompts 全集重编译，资料包 15 镜对齐
- 2_世界观人设/background/中立_neutral/bg42_北极冰洞/bg42-1_北极冰崖外/ — 冰崖外场景图（Codex 出图）与卡

验证: shot_overhead --all 0 blocker；shot_pack sync / check ok；草稿 st1 b56e324f、st2 06e55cbe、st3 b585b107、st4 11107437 已出并经 cc-connect 发用户；motion_check：st1 3.42/5.55 s 疑似切镜且背景冒出石柱与发光洞口（根因：崖外镜头挂了冰洞内部场景图），st2/st3 无切镜，st4 3.05 s 待确认；已换 bg42-1 重编译，按用户规则等反馈再重出
费用: Seedance 草稿 4 条约 360 积分；Codex 出图 1 张（订阅额度）

No conflicts found in: （未单独核查）


## Follow-up 329 — 2026-11-02 11:52:40
Source: user_input/follow_ups/202611.md - section 329
Summary: s1 st1–st3 摔下去之前画面里只能有冰雪后一点微弱的光，不能有洞口、石柱、碑文；场景参考已换 bg42-1，规格再写死并加负面词，重出 st1–st3 草稿，看片后发用户等反馈。

Auto-updated:
- episodes/ep01/filming.json — s1 st1–st2 写死摔下去之前无洞口 / 石柱 / 碑文，只有冰雪后一点弱光；st3 破口改为身体大小、边缘参差；全集重编译、资料包对齐；st1 旧草稿记 user_feedback.md

验证: 新草稿 st1 bcb37c36、st2 4996f63e 无洞口无石柱、motion_check 无切镜；st3 8743544a 冰面蛛网裂开后栽进去，破口仍偏大露出蓝色冰洞，3.25–3.8 s 剪切检测连续报警为塌陷时的快速运动（非单帧切镜，检测器待改：真切镜是孤立单帧）；三条已发用户等反馈
费用: Seedance 草稿 3 条约 270 积分

No conflicts found in: （未单独核查）


## Follow-up 330 — 2026-11-02 13:00:54
Source: user_input/follow_ups/202611.md - section 330
Summary: 用户认可 s1 st1 bcb37c36、st2 4996f63e、st3 8743544a 三条草稿：各条 review.md 记「状态：通过」与用户原话，供之后出正式条。

Auto-updated:
- s1 st1 bcb37c36 / st2 4996f63e / st3 8743544a 的 review.md 改为「状态：通过」、user_feedback.md 记用户原话

验证: shot_take.py approved 列出这三镜为草稿已通过

No conflicts found in: （未单独核查）


## Follow-up 331 — 2026-11-02 21:05:13
Source: user_input/follow_ups/202611.md - section 331
Summary: 新增镜组层：filming.json 场级 groups，编译器出镜组 prompt（镜组板＋各镜俯视图＋分镜头段落），shot_pack / shot_take 支持镜组 key，管理 UI 新增 /group-preview 页面；术语表加镜组；s1 g2（st4–st7）出镜组板

Auto-updated:
- 管理应用：production_key 加镜组 key；episode_workflow 常量（GROUP_*）；编译器 entity 校验 filming 场级 groups（≥2 镜、连续、不重叠、≤30 秒）并为每个镜组多出一条 prompt（镜组板→各镜俯视图→人物/道具/场景/声音，按镜头分段、镜头间切换），成员镜头 prompt 不变、编译器版本仍 12；shot_materials reader 找镜组板；UI 新增 /group-preview 页面（镜组板、出片、镜头分解、prompt、参考）。tools/shot_pack.py 与 shot_take.py 支持 ep1_s1_g2（目录 scenes/s1/groups/g2，成员镜头有问题镜组包也失效）。术语表加「镜组」并改镜头/条定义；prompts-generate.md、filming.md 加镜组说明。dota_yingxiong ep01 s1 写入 g2（st4–st7，27 秒），Codex 出镜组板 board.png，编译与资料包已建（10 个参考，4060 字）

验证: 后端 pytest 467 passed（test_global_workflow 的引用闭包一条因其他会话的 xianxia qc/deep_review.md 与 tools/motion_check.py 未登记而失败，与本改动无关）；新增编译器测试 7 条、shot_pack 测试 1 条、UI vitest 4 条通过；tsc -b 通过；workflow_catalog --check、sync_agent_skills --check 通过；浏览器打开 /group-preview 页面核对镜组板、镜头分解、prompt 与参考清单都显示。镜组草稿未提交（等用户看镜组板）
费用: 无收费服务（Codex 出图走订阅额度）

No conflicts found in: （未单独核查）


## Follow-up 332 — 2026-11-02 21:36:06
Source: user_input/follow_ups/202611.md - section 332
Summary: 管理 UI 左侧导航：影视改编与 Prompt 模块下的场改为 场→镜组→镜头；没写镜组的镜头显示为单镜组；镜组节点链到 /group-preview 并列出镜组目录

Auto-updated:
- tree__reader._workflow_scenes：每场下先列镜组再列镜头；filming.json 的 groups 成为「镜组 ep1_s1_g2 · st4–st7 · 27 秒」节点（链到 /group-preview，子项是成员镜头和镜组目录文件），其余镜头各自包一层「单镜 stN · N 秒」；镜头节点 path 不变。测试 test_a_shot_group_compiles… 补了导航断言

验证: pytest tests/test_episode_workflow.py + test_tree*：105 passed；实时 /api/tree 里 ep01 s1 显示 单镜 st1/st2/st3 与 镜组 ep1_s1_g2（含 st4–st7、drafts、资料包）
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 333 — 2026-11-02 21:42:46
Source: user_input/follow_ups/202611.md - section 333
Summary: s1 g1（st1–st3，镜组板取自已通过草稿帧）；g1、g2 出正式条（g1 用成员镜头通过草稿接起来作参考）；s2–s4 整理成镜组并出镜组板

Auto-updated:
- s1 新增 g1（st1–st3，22 秒），镜组板由三条已通过单镜草稿各取一帧拼成；tools/shot_take.py：镜组出正式条时若镜组无通过草稿而成员镜头都有，就把成员草稿按顺序接成参考视频（member_drafts / joined_reference，含测试）；编译器镜组板用法补「空格不对应镜头」；g2 草稿按用户「真是出片两个镜组」标通过；g1、g2 出 720p 正式条；s2–s4 各整理成一个镜组 g1（21 / 23 / 14 秒），Codex 出三张镜组板，编译与资料包已建

验证: tools 测试 11 passed；编译 5 个镜组（3523–4162 字）、shot_pack sync ok；g1 正式条 22.08 秒、切点 8.0/15.9 秒，与已通过草稿一致，但第 1 镜她戴了灰色围脖遮住嘴（人物卡没有）；g2 正式条 27.07 秒、切点 8.0/15.9/21.7 秒，与通过草稿一致。三张镜组板看图：种族、人物、道具对；s3/s4 医者肤色是自然肤色，与 m310 卡的淡灰紫不同
费用: Seedance 正式条：g1 528 + g2 648 = 1176 积分；Codex 出图走订阅额度

No conflicts found in: （未单独核查）


## Follow-up 334 — 2026-11-02 22:14:10
Source: user_input/follow_ups/202611.md - section 334
Summary: 记缺陷；剧级 qc 加 spec.pacing / spec.world_logic / video.pacing；提出 s1 前段改写方案待用户确认

Auto-updated:
- qc_checks.toml 剧级新增 spec.pacing、spec.world_logic、video.pacing（视角 viewer，闸门）；qc defect 记两条（spec.pacing、spec.world_logic，artifact = s1 g1 正式条）；s1 前段改写方案交用户确认，未改分镜、未出片

验证: qc.py defect 两条写入成功；qc_checks.toml 新条目按既有格式
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 335 — 2026-11-02 22:14:57
Source: user_input/follow_ups/202611.md - section 335
Summary: 剧 workflow.json prompt.skip_draft 记用户理由；shot_take 不给 --stage 时按此直接出正式条（--no-draft 理由自动带上）；prompts-generate.md 记一句

Auto-updated:
- ai_videos/dota_yingxiong/workflow.json prompt.skip_draft；tools/shot_take.py --stage 默认按剧设置（有 skip_draft 就 final + no_draft 理由）；prompts-generate.md 两步出片一行补说明

验证: tools/tests/test_shot_take_stages.py 11 passed；shot_take --help 正常
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 336 — 2026-11-02 22:35:24
Source: user_input/follow_ups/202611.md - section 336
Summary: tools/scene_board.py 生成场故事板（每镜一格＋文字＋起止秒，从左到右）；shot_pack sync 自动更新；UI /scene-preview 页面与左侧导航「场故事板」

Auto-updated:
- 新增 tools/scene_board.py（切镜组板、scene_board.json、整场长图 scene_board.png，来源指纹变了才重画）；tools/shot_pack.py sync 顺带更新、check 报过期；管理 UI 新增 SceneBoardPage（/scene-preview）与 lib/sceneBoard.ts，tree__reader 每场第一项「场故事板」；prompts-generate.md 补说明；ep01 s1–s4 场故事板已生成

验证: tools/tests/test_scene_board.py 等 5 passed；vitest scene-board/group-preview 6 passed；tsc -b 通过；shot_pack sync/check ok 20；浏览器打开 /scene-preview?…s1 显示 7 格、镜组分段、时间范围，左侧导航出现「场故事板」
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 337 — 2026-11-02 22:38:00
Source: user_input/follow_ups/202611.md - section 337
Summary: 场故事板页面与整场图改为从左到右、自动换行，不再横向滚动

Auto-updated:
- SceneBoardPage.css 镜组与格子 flex-wrap 换行、卡片 300px；tools/scene_board.py 整场图每行 4 格往下排（VERSION 2），ep01 四场重画

验证: 浏览器打开 s1 场故事板：卡片按窗口宽度换行，无横向滚动条；test_scene_board 通过
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 324 — 2026-11-01 23:13:44
Source: user_input/follow_ups/202611.md - section 324
Summary: 影魔 k861 只放三发影压（远中近），其余时间用普通远程攻击（火焰飞弹）逐个打死后续树人；k864 魂柱从地面自下而上冲天、保持竖直的同时从中心快速水平向远处扩散。

Auto-updated:
- c86 影魔 k861 技能卡改为只放 3 发影压（1.8/2.4/3.0 s，落点 20/15/10 米），3.3–9 s 用火焰飞弹普攻逐个打死 6 个树人（指纹 283c77da6578）；k864 释放拍改为魂柱自下而上垂直冲天、整圈水平外扩到 20 米（指纹 4d7a08646b8e）；旧卡备份 _history/k861_card_324.md、_history/k864_card_324.md。重出视频待用户认可新时间轴后再提交（约 430 积分），出片后另开 follow-up。

验证: 两张卡已按用户原话逐条核对并给用户看了时间轴表；没有出片、没有调用即梦，本条未消耗积分。
费用: 0

No conflicts found in: 只改 k861/k864 技能卡，k862/k863 和其他英雄没动


## Follow-up 338 — 2026-11-02 22:50:55
Source: user_input/follow_ups/202611.md - section 338
Summary: s1 前段改为 52 秒 st8–st14（镜组 g3、g4），蓝光改为时隐时现；镜组板、故事稿、决策记录、episode_seconds 上限 300

Auto-updated:
- filming.json：旧 st1–st3 与旧 g1 退出分镜（目录留档），新增 st8–st14（8+7+7+8+8+7+7=52 秒）与俯视图，镜组 g3=st8–st11、g4=st12–st14、g2 不变；Codex 出 g3、g4 镜组板；episodes/ep01/story.md 与 vlog/01_crossing/story.md 场一改写；decisions/filming.md 记改写理由；workflow.json episode_seconds [60,300]；重新编译、资料包与 s1 场故事板已更新

验证: shot_overhead --all 19 镜 0 blocker；编译 g3 4225 字 / g4 3396 字；shot_pack sync ok 25；看图：g3/g4 镜组板蓝光微弱、无围脖、无洞口、种族与人物一致
费用: 无（Codex 订阅额度）；未出片

No conflicts found in: （未单独核查）


## Follow-up 339 — 2026-11-02 22:50:55
Source: user_input/follow_ups/202611.md - section 339
Summary: 导航镜组节点只放成员镜头（去掉镜组目录杂项）；场故事板抽成 SceneBoardView，嵌进影视改编的场页面

Auto-updated:
- tree__reader 镜组节点 children 只剩成员镜头；新增 SceneBoardView.tsx（SceneBoardPage 复用），EpisodeWorkflowPage 影视改编的场视图在走位图前显示场故事板

验证: 浏览器打开用户给的 /drama?…scene=s1：导航展开、选镜头正常（未能复现错乱，推测是保存新分镜时树中途刷新）；场页面显示场故事板 11 镜 79 秒；pytest 105 passed；vitest 10 passed；tsc 通过
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 340 — 2026-11-02 23:07:54
Source: user_input/follow_ups/202611.md - section 340
Summary: s1 镜头重编 st1–st11、镜组 g1–g3，目录/文件名/生成记录/审核/overhead/缺陷记录一起改，旧 st1–st3 与旧 g1 存档；场页面不再列每镜全文

Auto-updated:
- 改号：st8–st14→st1–st7、st4–st7→st8–st11、g3/g4/g2→g1/g2/g3；旧 st1–st3、旧 g1 移到 scenes/s1/_archive_20261102/（过期俯视图也挪进 stale_planning）；generation.json / review.md / prompt.txt / overhead.toml 内的 key 与路径、视频文件名、specs/ai_video/dota_yingxiong/defects.jsonl 路径同步；request_log.md 不改（审计），对照表 scenes/s1/renumber_20261102.md；decisions/filming.md 更新；EpisodeWorkflowPage 有镜组的场只显示场故事板，选中镜头才显示分镜全文

验证: shot_overhead --all 0 blocker；编译后 s1 镜头 st1–st11、镜组 g1(st1–st4)/g2(st5–st7)/g3(st8–st11)；shot_pack sync ok；g3 的草稿与正式条记录 key=ep1_s1_g3、src 路径指向新目录；浏览器：导航与场页面显示新编号，场页面只有场故事板；tsc、vitest 通过
费用: 无

No conflicts found in: （未单独核查）


## Follow-up 341 — 2026-11-02 23:21:09
Source: user_input/follow_ups/202611.md - section 341
Summary: s1 冰洞段 66 秒（g3–g5）与 s2–s4 按节奏/世界逻辑/反应复查重写，出 9 张镜组板，故事稿与决策记录同步

Auto-updated:
- filming.json：s1 冰洞段改为 st8–st17（66 秒，g3/g4/g5），s2 改为 st1–st6（42 秒，g1/g2），s3 改为 st1–st7（48 秒，g1/g2，一句台词一镜），s4 改为 st1–st5（36 秒，g1/g2，加活木小路与精灵学徒）；旧镜头与镜组目录存档在各场 _archive_20261102b/；35 镜俯视图；9 张新镜组板（Codex，s1 g4/g5 两轮、s2 g1 一轮因道具与画面逻辑重出，退稿在 episodes/ep01/scenes/_board_rejects/）；故事稿两份与 decisions/filming.md 全集节奏复查表同步；11 个镜组编译、资料包与四场场故事板更新

验证: shot_overhead --all 35 镜 0 blocker；编译 11 个镜组 3161–4223 字；shot_pack sync updated 46；逐张看镜组板：一本书、无围脖、种族对、她看不见人群时画面里没有人群
费用: 无 Seedance；Codex 订阅额度（9 张 + 重出 5 张，3 张撞 429 未出图后补出）。作废：s1 旧 g3（原 st8–st11 冰洞段）正式条 648 积分与草稿 324 积分

No conflicts found in: （未单独核查）


## Follow-up 342 — 2026-11-03 09:48:59
Source: user_input/follow_ups/202611.md - section 342
Summary: s1 g1：她发现蓝光时头和视线必须先转向蓝光方向、蓝光在她视线里；g2：掉进去必须有物理原因（身体重量压在冰上 / 脚下冰层塌陷 / 她主动钻），不能敲了两下就掉进去。改分镜重出 g1、g2；加剧级检查（发现＝视线指向、因果＝物理原因）防再犯；记用户缺陷。

Auto-updated:
- episodes/ep01/filming.json — s1 st2/st3 视线按画面左右写死（先转头盯住蓝光再反应），st6/st7 写清掉落的物理原因（重量压在冰上、脚下积雪坡塌）；st8–st11 改为真实天然冰川冰洞、风化灰石柱简单刻痕、st10 不拍脸部特写（g3 两次被判 OutputVideoCopyright）；全集重编译、资料包对齐
- scenes/s1/groups/g3/board.png — 按新写法重画（旧图存 board_v1_copyright_fail.png、board_prompt_v1.txt）
- ai_videos/dota_yingxiong/qc_checks.toml — 新增 spec/video.notice_gaze、spec/video.physical_cause；defects.jsonl 记两条用户缺陷；g1/g2 旧条 user_feedback.md

验证: 重出 g1 e6999b56（蓝光在画左、她先转头盯住）、g2 50e1d384（前倾压冰、积雪滑塌扑倒）抽帧确认改对；g3 803c4b84 / 3723d3b0 均出片、未再被判版权；s1 g1–g5 与 s2 g1–g2 全部经 cc-connect 发用户等反馈
费用: g1 600、g2 440、g3 520×2（第二次为代理重复提交：后台 & 启动的提交实际已成功、未确认又提交一次）；Codex 镜组板 1 张

No conflicts found in: （未单独核查）


## Follow-up 343 — 2026-11-03 12:04:50
Source: user_input/follow_ups/202611.md - section 343
Summary: s1 g1 发现蓝光两镜改为过肩 / 视线同轴的机位（她的脸朝向与蓝光在同一条视线上，必要时切过肩镜头）；收紧 spec.notice_gaze 判法（要求机位方案）；重出 g1；之后按场剪辑 s1（g1–g5）与 s2（g1–g2）完整视频经 cc-connect 发用户。

Auto-updated:
- episodes/ep01/filming.json — s1 st2 改过肩镜头（蓝光在她头朝向正前方）、st3 改反打（光源在镜头方向、淡蓝光照在她脸上）；st2/st3 overhead.toml 机位改写并重画；g1 镜组板重画（旧图 board_v1_gaze_fail.png）
- ai_videos/dota_yingxiong/qc_checks.toml — spec.notice_gaze 判法加：必须写出让人和物同一视线的机位方案（过肩 / 主观 / 反打），单机位人前物后判不过
- scenes/s1/edit/final/s1_assembly_v1.{mp4,json}（118.34 s）、scenes/s2/edit/final/s2_assembly_v1.{mp4,json}（42.14 s）— 按镜组顺序原样拼接，清单记每段来源与 sha

验证: g1 96a27470 抽帧：过肩段蓝光在她头朝向正前方、她盯着再揉眼；反打段她看镜头旁边；小瑕疵：反打开头约 1 s 虚焦背景左下闪过蓝光。s1 / s2 完整版经 cc-connect 发用户（zip）。scene_cut.py 暂不支持镜组，本次用拼接脚本
费用: g1 600 积分；Codex 镜组板 1 张

No conflicts found in: （未单独核查）


## Follow-up 344 — 2026-11-03 12:55:18
Source: user_input/follow_ups/202611.md - section 344
Summary: s1 g3 结尾她望向远处蓝光、朝它走去；g4 开头直接蹲着摸地板，中间缺了「走过去、进入圆厅、脚下踩到纹路才蹲下」的过渡。改 g4 首镜补上走近与发现的动作，重出 g4、重剪场一；加剧级检查：相邻镜组首尾动作 / 位置 / 视线要接得上。

Auto-updated:
- episodes/ep01/filming.json — st12 改为接上 g3 结尾（过右肩跟拍朝蓝光走进圆形大厅→绊到刻纹→蹲下→抬头看石台，7→9 s）；st12–st14 冰洞写法与 g3 一致；st12 overhead 重写；g4 镜组板重画（v1/v2 旧图留档）
- ai_videos/dota_yingxiong/qc_checks.toml — 新增 spec/video.group_continuity

验证: g4 ccaa0b96 与 efa91bad 抽帧：开头她背对镜头朝蓝光走进大厅、蹲下摸刻纹，衔接已接上；已发用户
费用: g4 ccaa0b96 480 积分；Codex 镜组板 2 张

No conflicts found in: （未单独核查）


## Follow-up 345 — 2026-11-03 13:04:46
Source: user_input/follow_ups/202611.md - section 345
Summary: 冰霜法典第一次出现（s1 g4 石台脚下）画得太大，不像能单手拿的书；在道具卡、分镜与镜组板写死尺寸（普通精装书大小，约 25×18 cm、4 cm 厚，能单手拿、夹在胳膊下），重出 g4；加剧级检查：道具首次出现的尺寸与人体比例。

Auto-updated:
- props/近卫_sentinel/p234_冰霜法典/p234_冰霜法典.md — 尺寸写死（约 25×18 cm、4 cm 厚、单手可拿）；filming st13/st14 加尺寸句；g4 镜组板重画
- ai_videos/dota_yingxiong/qc_checks.toml — 新增 spec/video.prop_scale

验证: g4 efa91bad 抽帧：石台脚下的书约靴子大小、拿在手里比例合理；已发用户
费用: g4 efa91bad 480 积分；Codex 镜组板 1 张

No conflicts found in: （未单独核查）


## Follow-up 346 — 2026-11-03 13:13:05
Source: user_input/follow_ups/202611.md - section 346
Summary: s1 传送（g5）改为专门设计的传送法阵与符文：先立法阵资产卡与设计图锁定形制（多层同心符文环、逐圈点亮、反向旋转、符文浮起螺旋上升、冰晶与光柱），st12 休眠刻纹与之一致，st15–st17 写清激活过程；重画 g5 镜组板并重出 g5，之后重剪场一。

Auto-updated:
- props/近卫_sentinel/p235_传送法阵/（新）— 卡、设计图、启动过程锁定（props_lib 领号 p235）
- episodes/ep01/filming.json — st12 休眠外环与 p235 一致；st15–st17 挂 p235，st16 改为三环逐圈点亮 + 反向旋转（6→7 s）、st17 符文浮起螺旋上升 + 光柱（5→6 s）；st16/st17 overhead 时间改写；g5 镜组板重画并局部擦掉多出的书
- scenes/s1/edit/final/s1_assembly_v2.{mp4,json}（122.34 s）

验证: g5 ff6ea0dd 抽帧：三层符文环与放射刻槽点亮、符文绕她螺旋上升、光柱吞没至全白；场一 v2 与 g4/g5 已经 cc-connect 发用户
费用: g5 400 积分；Codex 出图 4 张（设计图 + 镜组板 3 次）

No conflicts found in: （未单独核查）


## Follow-up 347 — 2026-11-03 15:27:03
Source: user_input/follow_ups/202611.md - section 347
Summary: s1 g1 过肩（st2）切反打（st3）时蓝光出现在她脑后，越轴。st3 改为与 st2 同侧（不越轴）的侧面双人构图：她在画左侧脸朝右、冰崖与蓝光在画右，两镜屏幕方向一致；重画 g1 板、重出 g1、重剪场一（含审片版）；加剧级检查：切镜不越轴、关键物屏幕方位前后一致。

Auto-updated:
- episodes/ep01/filming.json — s1 st3 由反打改为与 st2 同侧的侧面双人构图（她在画左朝右、冰崖与光点在画右同框），st2/st3 写死屏幕方向；st2/st3 overhead 机位改到轴线同侧；g1 镜组板重画（旧图 board_v2_axis_fail.png）
- ai_videos/dota_yingxiong/qc_checks.toml — 新增 spec/video.screen_axis；defects.jsonl 记 new:screen_axis
- scenes/s1/edit/final/s1_assembly_v3.{mp4,json} 与 _review.mp4（左下角标镜组 / 条号）；label 脚本给场剪辑出审片版（用户要求）

验证: g1 c5b206dd 抽帧：过肩与侧面两镜她都在画左朝右、蓝光都在画右，切镜前后不越轴；场一 v3 干净版与审片版已经 cc-connect 发用户
费用: g1 600 积分；Codex 镜组板 1 张

No conflicts found in: （未单独核查）


## Follow-up 348 — 2026-11-03 18:16:08
Source: user_input/follow_ups/202611.md - section 348
Summary: s1 g1：冰崖里的光很微弱，不该映到她脸上 / 眼里（去掉『蓝光映在脸上』、加负面词）；g1 四镜冰崖距离统一（小路离崖脚固定距离、每镜写明冰崖在画面里的大小），overhead 位置对齐；重画 g1 板、重出 g1、重剪场一；加剧级检查：光源强弱与照明效果一致、同一场地多镜的空间距离一致。

Auto-updated:
- episodes/ep01/filming.json — s1 st1–st4 写死小路离崖脚约 8 m、冰崖近在身旁；st2/st3 蓝光写成极弱小点、照不到她、脸 / 眼无蓝色反光（删『映在侧脸上』）；重复长句压缩以过 5000 字上限；st1–st4 overhead 位置改到 8 m；g1 镜组板重画（旧图 board_v3_distance_fail.png）
- ai_videos/dota_yingxiong/qc_checks.toml — 新增 spec.light_strength、spec/video.space_consistency；defects.jsonl 记两条
- scenes/s1/edit/final/s1_assembly_v4.{mp4,json} 与 _review.mp4

验证: g1 432f7f34 抽帧：四镜冰崖都近在身旁、距离一致；蓝光是冰崖上小亮点，她脸上无蓝光；场一 v4 审片版与干净版已经 cc-connect 发用户
费用: g1 600 积分；Codex 镜组板 1 张

No conflicts found in: （未单独核查）


## Follow-up 349 — 2026-11-03 20:21:23
Source: user_input/follow_ups/202611.md - section 349
Summary: g1 st1→st2 跳切（相邻两镜景别角度太近、光线整体突变）：相邻镜头拉开景别 / 角度，光变化写局部；g4 去掉手摸地板（改为看见冰下刻纹）；g5 帽子全程戴着；法器（大光球）留在冰洞不带走，s2 她被传送到生命之泉，那里有一个一样的光球，静默不亮——重启需要机缘（以后再提）；改 s2 st6 及故事稿；重出 g1、g4、g5、s2 g2；加剧级检查：剪切点跳切、道具去向连续。

Auto-updated:
- episodes/ep01/filming.json：s1 st1–st4 剪切点动作接动作、全组天光不变；st12 站着看冰下刻纹不碰地；st15–17 帽子全程在、法器留在石台；s2 st6 改为生命之泉浅水里同款大法器（晶石暗）；s3 st1 只抱书
- 故事稿两份、vlog/lore_home.md（法器成对、重启需机缘）、vlog/base_world.md 同步
- s2 st6 / s1 st12 / s3 st1 overhead 重画；s1 g5、s2 g2、s3 g1 镜组板重画（旧板留 board_v*）
- qc_checks.toml 加 spec.cut_contrast、video.jump_cut、spec.prop_whereabouts；qc.py defect 记 3 条用户缺陷
- tools/shot_take.py：poll / record 遇到已收过的 submit_id 不再重复建条（之前会误记成草稿）；加测试
- 重出 s1 g1（600）、g4（480）、g5（400）、s2 g2（440），共 1920 积分

验证: 1 秒 1 帧拼图逐组看过：g1 剪切点动作接上、光线一致；g4 不碰地板；g5 帽子全程在、法器留在石台；s2 g2 她蹚水去按浅水里的大法器、手里只有书；语音识别核对台词位置；pytest tools/tests/test_shot_take_stages.py 12 passed；shot_pack check ok 46；shot_overhead --check 0 blocker
费用: 1920 积分

No conflicts found in: 另一会话（follow-up 342–348）已由用户停掉；只改了它留下的最新分镜，未动其渲染记录


## Follow-up 350 — 2026-11-03 22:20:37
Source: user_input/follow_ups/202611.md - section 350
Summary: s1 g4 书改小、翻书放慢后重出；s2 改成她落在生命之泉浅水里同样的法阵上、法器就在旁边，改分镜/overhead/镜组板/场故事板并重出 s2；每次改完出整场剪辑视频与预览链接（剧级约定）

Auto-updated:
- ai_videos/dota_yingxiong/episodes/ep01/filming.json; story.md; vlog/01_crossing/story.md; vlog/lore_home.md; vlog/base_world.md; README.md（剧集交片整场剪辑约定）; s1 st13/st14、s2 st1/st6 overhead; s1 g4、s2 g1、s2 g2 镜组板; s1_assembly_v5、s2_assembly_v2

验证: 1fps 抽帧 + 语音识别看过三条新条：g4 书小、只翻两页；s2 g1 落在水底法阵上、法器在右边；s2 g2 法器在法阵中央；s2 g1 开头 1 秒帽子不在，整场剪辑入点设 1.25 s；shot_pack check ok 46；场故事板最新
费用: Dreamina 1320 积分（480+400+440）；codex_image 3 张

No conflicts found in: （未单独核查）


## Follow-up 351 — 2026-11-03 23:04:37
Source: user_input/follow_ups/202611.md - section 351
Summary: s1 g4 书不在远景里出现，改成特写里在她靴尖旁露出小书角；s1 g1 st3 改成从冰崖光点旁反拍她，她正对光点说台词；两组重出并给整场剪辑

Auto-updated:
- filming.json（s1 st2/st3/st13/st14）; st3/st13/st14 overhead; s1 g1、g4 镜组板; s1_assembly_v6

验证: 1fps 抽帧 + 语音识别：g1 第 15–21 秒反打，她正对前景冰里的光点说 did you see that；g4 远景里不再出现书，第 16–18 秒特写里从靴边霜里抽出小书；shot_pack check ok 46
费用: Dreamina 1080 积分（600+480）；codex_image 2 张

No conflicts found in: （未单独核查）


## Follow-up 352 — 2026-11-04 23:19:18
Source: user_input/follow_ups/202611.md - section 352
Summary: 10 个英雄 demo：补 c63 / c86 的 publish.md（未定版先行），每个英雄做中文封面 4:3 横、3:4 竖各三张

Auto-updated:
- c63_Lord_of_Avernus/demo/publish.md、c86_Shadow_Fiend/demo/publish.md（新，标明未定版）；10 个英雄 demo/publish.md 加中文封面候选一行；_tools/demo_covers.py（新）；各英雄 demo/covers/cover_{1,2,3}_{4x3,3x4}.png（60 张）与 covers/frames/；demo_covers.html 挑选页

验证: 8 个已有 publish.md 头部版本与 edit/final 最新成片一致（CK v3、斧王 v9、沙王 v5、小小 v4、全能 v5、宙斯 v3、冰女 v5、火女 v3），未改正文；c63 v3 / c86 v5 按成片逐段抽帧核对技能描述后照 Lina 格式写；封面逐英雄看拼图，换掉人物被裁或被字挡住的帧，英雄名改到底部，左上角 DotA 原版技能图标改为裁掉最左一条（模糊遮盖可见，已弃）；Chrome 打开 demo_covers.html 正常；workflow_catalog --check 通过

No conflicts found in: 只新增文件与 publish.md 头部一行，未动成片、剪辑决定与技能卡


## Follow-up 353 — 2026-11-04 23:43:51
Source: user_input/follow_ups/202611.md - section 353
Summary: 抖音合集「DotA英雄真人化」名称、简介与三张 3:4 封面候选（群像九宫格 / 斧王大片 / 近卫 VS 天灾）

Auto-updated:
- _tools/collection_cover.py（新，复用 demo_covers 选帧）、_assets/collection_cover/cover_{A_grid,B_hero,C_versus}.png 与 contact_sheet.jpg

验证: 看对比图：B 款标题首版挡住斧王的脸，改到下方后重出；画面全部取自成片，技能段已裁掉原版技能图标

No conflicts found in: 只新增文件


## Follow-up 354 — 2026-11-14 12:37:57
Source: user_input/follow_ups/202611.md - section 354
Summary: 自检闸门改两层（通用质量 / 对照规格＋容差）、三种结论、放行分类并绑定检查定义、取消 CUTOFF 豁免

Auto-updated:
- tools/qc.py — 登记表 layer（quality 通用 / spec 对照规格）与 tolerance、SPEC_TOLERANCE；结论加「审不了」（--reason 材料缺|看不清）；取消 CUTOFF 豁免；旧审稿规则（无 rule 字段）的审稿 fail 要求重审；override 必填 --kind accept|false_positive、绑定 check_sha、一句原话只管一类（--mention）；stats 分误报与接受瑕疵、计审不了；闸门提示改为每镜最多重出两次
- tools/qc_review.py — 提示词去掉「拿不准就判 fail」，加三种结论与两层说明（观众视角只给三种结论）、每项标【通用】/【对照规格】与容差；parse/aggregate 支持审不了与原因；出片后对照该条提交时的 prompt.txt，不用卡上现行规格
- tools/skill_run.py — --allow 放行改记 --kind accept，fail 与审不了都可按用户原话放行
- .agents/references/project/qc_checks.toml — 6 条标 layer；keyframe.locked_traits 改为「认得出是卡上那个」，细节出入只记录；字段说明补 layer / tolerance
- ai_videos/dota_yingxiong/qc_checks.toml — 49 条标 layer（14 条 spec）；video.timeline 改「时刻大致对、大范围偏差才算错」并写容差；video.scale、keyframe.scale、video.head_tail、video.fidelity 写容差；video.gaze 看不清记审不了
- CONVENTIONS.md — 自检与自我进化：record 四种结论、闸门不过按每镜最多重出两次（原写 3 轮，与 Iteration bounds 矛盾）、新增「审查不随流程版本变」一条
- .agents/skills/ai-videos-self-check/SKILL.md — 新增「两层、三种结论」表；override 改为两种 kind 与一句原话一类
- .agents/skills/ai-videos-pipeline/modules/prompts-generate.md — 审完记进闸门：补「审不了」与 --reason
- tools/tests/test_qc.py、tools/tests/test_qc_review.py — CUTOFF 用例改为旧条不豁免；新增审不了分层、旧规则重审、accept 不算误报、检查改了放行作废、一句原话一类、提示词三种结论与对照提交时 prompt 共 7 个用例

验证: python -m pytest tools/tests：282 passed；管理站 tests/test_process_qc.py 4 passed；qc_review.py --dry-run 对 chuanyue s3 st4 实条核对提示词（每项带层级与容差、无「拿不准就判 fail」）；qc.py gate 实条可用；sync_agent_skills --check、workflow_catalog --check 通过；tests/test_global_workflow.py 引用闭包仍失败（25 条未登记引用均为既有，不是本次引入）。未做独立审稿：本次是工具与规则改动，没有新产物

No conflicts found in: review_run.py 双审查单体系未改；qc_pre.py 只经 verdict_problems 受影响；管理站 process_qc 读取 verdict 原样显示

