# c3 全能骑士 · 声音研究（follow-up 103）

> 用户 2026-10-23：「请上网research omni knight平时说话的声音，还有释放技能时候的声音以及视频，技能1，2 的声音不对」。
> 下载经 `reflog.py`（`tools/service_request.py::RequestLog`）留痕，记在 `characters/request_log.md`；整段视频放 scratchpad、不入库，这里只留频谱图与截帧拼图。所有原版素材只作研究，**不上传生成、不挂进视频参考**。
> 局限：代理不能用耳朵听，声音结论来自**语音识别 + 基频测量 + 频谱图**，以及画面对照；音色的细腻描述（像钟、像合唱）是从频谱结构推断的，待用户试听确认。

## 1. 平时说话的声音

DotA 1 的全能骑士借用 WC3 战役英雄**阿尔萨斯（圣骑士时期）**的语音组（人物卡「原典」✅；WC3 中由 Justin Gross 配音，[Wikipedia](https://en.wikipedia.org/wiki/Arthas_Menethil)）。本地 23 条原声（`../original/`，2026-10-18 下载）重新测量：

| 测量 | 结果 |
|---|---|
| 基频中位数 | 约 **100 Hz**（各句 84–122 Hz；战吼 "For Lordaeron!" 145 Hz、"You are past redemption." 148 Hz） |
| 语速 | 每句 0.7–2.5 s，字字清楚、不急 |
| 句子 | "The Light is my strength." / "I stand for the Light." / "Justice shall be done." / "I'm here to help." / "For Lordaeron!" 等 |

对照：WC3 通用圣骑士语音（YouTube `ifm-mTPPFts`）约 139 Hz、更高更亮；Dota 2 全能骑士（`m-oBmTTH_D8` 等）每放技能都会喊技能名（如 "Purification!"），DotA 1 不喊。

**本剧生成片的问题**：087 版 k31 "I'm here to help." 约 168 Hz、k32 "The Light is my strength." 约 142 Hz、098 版 k34 战吼约 327 Hz（夹杂特效）——都明显比原声高、薄、像年轻人在喊。

**结论（写进人物卡）**：低沉温厚的男中音、接近男低音（说话时音高约在 100 Hz 一带），胸腔共鸣厚，沉稳、端正、虔诚，像在宣誓；咬字干净、不急不躁；带一点石砌大厅般的短混响。战吼时更响、更有力，但仍低沉，不尖、不破音。

## 2. 技能释放的声音

| 文件 | 来源 | 看到 / 测到 |
|---|---|---|
| `m-oBmTTH_D8_frames.jpg / _spectrogram.png` | 已删：Dota 2 来源，follow-up 316 | |
| `4B0U8hgXhRY_frames.jpg / _spectrogram.png` | 已删：Dota 2 来源，follow-up 316 | |
| `LAgsYrdh5zc_frames.jpg / _spectrogram.png` | 已删：Dota 2 来源，follow-up 316 | |
| `TSZhHLkIfkc_*` | YouTube「Warcraft 3 Resurrection」（WC3 原版圣骑士复活术，守护天使借用的特效） | 先三段高频（2–5 kHz）短促闪烁像施法吟唱的光点声；5.6 s 起一段约 2.5 s 的**饱满和声膨胀**：300–700 Hz 密集谐波 + 1–1.5 kHz 明亮泛音 + 深低频，正是「天使降临」的合唱式和弦 |
| `kqlt5JgmoY8_*` | YouTube「Divine Shield」（魔兽世界圣骑士神圣护盾，驱逐的同源特效） | 3.6 s 施放：一下**清脆的闪亮爆音**（高频沙沙的光尘声从 10 kHz 往下落，约 1 s 衰减）+ 一下**低沉闷击**，之后护盾持续时一层低沉平稳的嗡鸣（约 300 Hz）；画面是金色发光球罩、四射光芒 |

**结论（写进技能卡）**

- **洗礼（k31）**：光柱落地那一下＝**沉重的低频轰击**（像大钟被重锤撞响、从地面滚过的闷雷）＋同时迸开的**明亮钟声和声**（一个像教堂合唱「啊——」的和弦，带细碎闪亮的高音），约 1 秒后高音散去，低沉余响再拖一会儿；热浪贴地的「呼」与食尸鬼干皮被灼烧的嘶嘶声。不说话、不喊技能名。
- **驱逐（k32）**：举锤天光落下＝一声**清脆闪亮的光爆**（高音沙沙的光尘从上往下落）＋一下低沉闷击；球罩张开＝一声**往上滑的共鸣「嗡——」**（像巨大的水晶碗被敲响后音调升高）；之后球罩持续一层**低沉平稳的嗡鸣**，符文环旋转时带一点很轻的、有节奏的低声嗡转。不说话。
- **守护天使（k34）**：降光＝深沉的低频轰鸣，紧接着一段约 2–3 秒**宏大的合唱式和弦膨胀**（像管风琴加天使合唱，缓缓升起再渐弱），夹细碎明亮的光尘声；翅膀展开时一阵柔和的羽毛掠风声；爪子打在无敌友军身上是清脆的「叮」。台词保留 "For Lordaeron!"，用第 1 节的低沉嗓音。

## 3. 技能视频里看到的画面（补充）

- Dota 2 守护天使（`LAgsYrdh5zc`、`BHOH1o-s5xM`）：一道白蓝光柱从天落在单位身上、脚下一圈亮环，随后单位背后长出一对白色翅膀、头顶浮一圈光环，持续到结束。
- WC3 复活术（`TSZhHLkIfkc`，见 `k34_Guardian_Angel/ref/research_087/` 截帧）：光柱里一个带大翅膀的长袍天使虚影浮现、悬在上方后散去。
- 驱逐（Dota 2 `4B0U8hgXhRY`）：亮光一闪后单位外有一圈旋转的光环 / 光带绕身转动。

## 4. 另一会话下载的参考库（follow-up 102 / 107，`0_research/media_refs/`）核对（2026-10-24，follow-up 109）

用户：「我感觉技能特效音乐还没加上，我让另一个 session download 了，你看有没有」。逐项核对：

| 项 | 路径 | 能不能用 |
|---|---|---|
| 全能骑士原台词合集 | `media_refs/heroes/c3_Omniknight/c3_Omniknight_voice_listen.mp3`（38 s，23 句） | 能听；就是本目录 `../original/` 的阿尔萨斯原声拼接，没有新内容 |
| WC3 神圣护盾音效 | `media_refs/audio_sources/wc3_ninja/1116274/divineshield.wav` | **不能**：文件只有 58 字节，没有音频内容（下载不完整） |
| WC3 复活术目标音效 | `media_refs/audio_sources/wc3_ninja/891422/resurrecttarget.wav` | **不能**：只有 44 字节，没有音频内容 |
| WC3 圣光术音效 | `native_spell_candidates/holybolt.wav.json` | 只有候选链接，**没下载** |
| 圣骑士神圣护盾结束音 | `wc3_ninja/1831409/paladindivineshielddeath1.wav`（2.9 s） | 有内容，但只是护盾消失时的声音，不是施放音；且只按路径匹配，未证明是 DotA 1 用的 |
| 6.83d 技能实机 | `media_refs/videos/vhARz5CpDbA/vhARz5CpDbA.mp4`（14 min，WC3 重制版跑 6.83d AI 图） | 有游戏声，但**全程有解说人说话**盖在上面（语音识别整段都是解说与英雄应答），分不出干净的技能音效；画面上这一版驱逐是**绿色**旋纹球、洗礼 / 守护天使是金色光柱 + 金环，与经典画质不同 |

结论：参考库里**没有可直接用的干净全能骑士技能音效**。而且按本剧规定，暴雪原版音频只作人耳参考，**不能混进成片**。成片里的技能声音现在来自视频模型按 prompt 生成；如果要在后期另外加一层专门的技能音效，需要用本仓库的音频入口（Suno）新做，属于收费服务，等用户决定。

## follow-up 316 补充（2026-11-01，严格 DotA 1）

- 第 2 节「技能释放的声音」里 k31 的「大钟 + 教堂合唱和声」、k32 的「往上滑的共鸣『嗡——』+ 符文环嗡转」、k34 的「宏大合唱式和弦 / 管风琴」，依据含已删的 Dota 2 视频（`m-oBmTTH_D8`、`4B0U8hgXhRY`、`LAgsYrdh5zc`），**作废**；第 3 节前两条 Dota 2 画面描述同样不再作依据。
- 现行写法见各技能卡「声音（锁定）」：k31 / k34 只按 WC3 复活术实录 `TSZhHLkIfkc`（短促高频闪烁 + 饱满谐波膨胀与深低频，按 follow-up 139 压到约 1 秒、不成合唱）；k32 原版神圣护盾施放音未取到可听文件，写「原版无此细节 ⚠️」后创作一声短促光爆 + 低沉闷击。
- `kqlt5JgmoY8` 是魔兽世界的神圣护盾，不是 DotA 1 / WC3，不再作 k32 声音依据。
