# k34 守护天使 · 参考研究（follow-up 087）

> 只作人眼研究，不上传生成、不挂进视频参考。下载经 `reflog.py`（`tools/service_request.py::RequestLog`）留痕，记在 `characters/request_log.md`；整段源视频不入库，只留截帧拼图（`research_087/`）。研究由子代理下载截帧，子代理中途因接口认证错误终止，结论由主代理看图补写。

## 参考清单

| 文件 | 来源 | 看到了什么 |
|---|---|---|
| `yt_wEM2tnIkVBc_dota1_guardian_angel_closeup.jpg` | YouTube `wEM2tnIkVBc`（DotA 1 实机，团战放守护天使） | 放下的一瞬间一团金白光在骑士周围炸开；之后**范围内每个友军头顶各浮起一个金白色、张着大翅膀的天使人形光影**（WC3 复活术施法者的天使模型），翅膀很大、亮，罩在友军上方，持续数秒；地上没有圆环线条 |
| `yt_vhARz5CpDbA_reforged_683d_selfcast_column.jpg` | YouTube `vhARz5CpDbA`（WC3 重制版跑 6.83d，对自己放） | 一道暖金光柱从天上笔直落在骑士身上，几圈金色光环像螺旋一样绕着他往上升，四周飘金色光点 |
| `yt_TSZhHLkIfkc_wc3_resurrect_caster_angel_3fps.jpg` | YouTube `TSZhHLkIfkc`（WC3 原版圣骑士复活术） | 守护天使借用的 `ResurrectCaster` 特效本体：先是一道斜落的光柱，随后**一个带大翅膀、披长袍的天使人形光影**从光里浮现、悬在施法者上方，翅膀张开，最后散去 |
| `yt_acA2A0iFAIA_dota2_spotlight_team_4fps.jpg`、`yt_acA2A0iFAIA_dota2_spotlight_single_4fps.jpg` | 已删：Dota 2 来源，follow-up 316 | |
| `yt_07IoV90YOoQ_dota2_selfcast_4fps.jpg` | 已删：Dota 2 来源，follow-up 316 | |
| `d2_official_video_frames.jpg` | 已删：Dota 2 来源，follow-up 316 | |
| `d2_icon_guardian_angel.png` | 已删：Dota 2 来源，follow-up 316 | |
| `playdota_hero47_skill3_guardian_angel.gif` | PlayDotA 存档图标 | 图标是张开双翼的天使 |
| `render_081_548d71cb_2fps_sheet.jpg` | 本剧 081 版成片抽帧 | 见下「旧视频的问题」 |

## 结论

1. **天使是这个技能的识别点**：DotA 1 与 WC3 的样子都是「每个友军头上浮起一个金色带翼天使光影」。旧卡把「天使人形」「羽毛翅膀」列为禁止，方向反了；改为：每个友军身后升起一个半透明、由光和金尘构成的长袍天使虚影，张开光羽大翼护住它。
2. **施放感**：重制版是一道金光落在骑士身上、几圈光环螺旋上升；DotA 1 是一团金白光在骑士周围炸开。取「光从云隙落在高举战锤的骑士身上 + 螺旋光环 + 一圈贴地光浪推开到范围边缘就散」，地上不留圆环线条。
3. **效果的兑现**：物理攻击打在被护住的友军身上无效。用食尸鬼的骨爪（全速）抓在树人身上只迸金色火星、树皮完好来表现，并让旧爪痕愈合（大量回血）。
4. **持续与结束**：天使光影持续数秒，结束时散成金尘。

## 旧视频的问题（081 版 `renders/20261023-084935_548d71cb/`，2 fps 抽帧）

1. 施法（举锤）约 3 s 才开始，光翼约 8 s 才出现，比时间轴晚很多。
2. 光翼只是贴在树人身上的半透明轮廓，不像天使，也不够亮、不够大。
3. 食尸鬼有的近乎直立、像人，开场蹲着的几只个头与树人腰部齐平，偏大。
4. 「打不动」没有清楚兑现：看不出爪子打上去被挡住、树人毫发无伤。
5. 没有结果：食尸鬼只是退开，结尾仍围在旁边；用户要求小兵死亡照对应图片，这一版改为反击打死、照死亡图腐烂成白骨。
6. 骑士全程站在中间不动，最后 4 s 只有站姿。

## 峰值图

Codex 出图两次都在连接阶段失败（`workspace routing discovery failed`，未生成），这一版视频不挂峰值图，动作与特效全靠 prompt 文字；旧峰值图 `k34_Guardian_Angel_peak.png`（081）不再作参考。峰值图 prompt 已写好在 `_candidates/k34_peak_087_prompt.txt`，Codex 恢复后可再出。

## follow-up 093 补充（主代理看图）

- 用户：施法快一点；释放之后所有友军都处于无敌状态，身上有无敌标记；多参考游戏 ref 图。
- 已删：Dota 2 来源，follow-up 316（原 `yt_07IoV90YOoQ_dota2_selfcast_4fps.jpg`）
- 已删：Dota 2 来源，follow-up 316（原 `yt_acA2A0iFAIA_dota2_spotlight_team_4fps.jpg`）
- 重看 `research_087/yt_wEM2tnIkVBc_dota1_guardian_angel_closeup.jpg`（DotA 1）：每个友军头上各浮起一个金色带翼天使光影，持续数秒。
- 结论：087 版只出了一个罩住全体的大天使，不对；改为每个友军（含骑士）各一套「背后光羽翅膀 + 头顶细光环 + 脚下光环 + 淡白金光晕」，持续到片尾。施法压到 1 秒内（原典施法动作很短）。
- 食尸鬼攻击照原版动画改为人立重劈，见 `k31_Purification/ref/research_093/` 与 `m4_Ghoul.md`。

## follow-up 147 补充（主代理重看原版图）

- 用户：天使的翅膀不要那么实，要有光影的感觉；所有友军周身也缠绕着金光符文，预示无敌；多参考游戏原图。
- 重看 `research_087/yt_wEM2tnIkVBc_dota1_guardian_angel_closeup.jpg`（DotA 1）：每个友军身上浮起的天使是**金黄色、像火焰一样摇曳的半透明光影**，翅膀由一片片亮黄光块组成、边缘发散，看得见下面的地面，没有一根实体羽毛。
- 已删：Dota 2 来源，follow-up 316（原 `yt_acA2A0iFAIA_dota2_spotlight_single_4fps.jpg`、`yt_07IoV90YOoQ_dota2_selfcast_4fps.jpg`）
- 结论：142 版写实羽毛翅膀方向偏「实」；改为由流动金光构成的半透明光翼（DotA 1 的金黄火焰感），把 Dota 2 的符文环改成用户要的「周身缠绕的金色符文光带」（从脚踝盘旋到肩头、紧贴身体），二者都持续到片尾。

## follow-up 316 补充（2026-11-01，严格 DotA 1）

- 「follow-up 093 补充」结论里照 Dota 2 加的「背后光羽翅膀 + 头顶光环 + 脚下光环」，与「follow-up 147 补充」里由 Dota 2 符文环改来的「周身缠绕金色符文带」，**作废**。
- 现行依据：DotA 1 实机 `yt_wEM2tnIkVBc_dota1_guardian_angel_closeup.jpg`（放下时一团金白光在骑士周围炸开；之后每个友军头顶各浮一个金黄色、火焰感、半透明的带翼天使光影，翅膀由亮黄光块组成、边缘发散；地上没有圆环线条）、WC3 复活术 `yt_TSZhHLkIfkc_wc3_resurrect_caster_angel_3fps.jpg`（`ResurrectCaster` 天使本体）、PlayDotA 图标。
- 卡已改：无敌标记改为每个友军头顶各浮一个金色火焰感天使光影；符文带（用户 147 / 151 选的）按 316 去掉，待用户确认。
- `yt_vhARz5CpDbA_reforged_683d_selfcast_column.jpg` 是 WC3 重制版跑 6.83d，不是经典画质，仅作旁证。
