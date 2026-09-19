# Real upstream fixtures

Byte-for-byte copies (`cp -p`) of real repo files taken 2026-09-13 by impl-02-inputs_and_config (spec v2 FR-8/FR-9 parser tests). Never edit a copy; add a new copy when a new variant appears.

**`xianjian__*` 的上游已于 2026-09-19 删除**（`ai_videos/xianjian_yi_mv/` 整个项目被清除，该剧重启为 `xianjian_yi` 系列）。这些拷贝本身仍是有效的 parser 测试输入，只是源路径不再存在；`test_shot_prompt__reader__golden.py` 的 `DELETED_UPSTREAM` 记录了这一点，源若复现会报错提醒。

| fixture | source |
|---|---|
| `real_shots/hy3__shot02.md` | `ai_videos/huangye_shenghuo/hy3/5_6_分镜与prompt/shots/shot02/shot02.md` |
| `real_shots/hy2__shot01.md` | `ai_videos/huangye_shenghuo/hy2/5_6_分镜与prompt/shots/shot01/shot01.md` |
| `real_shots/hy2__shot02.md` | `ai_videos/huangye_shenghuo/hy2/5_6_分镜与prompt/shots/shot02/shot02.md` |
| `real_shots/xianjian__shot01.md` | `ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot01/shot01.md` |
| `real_shots/xianjian__shot02.md` | `ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot02/shot02.md` |
| `real_shots/xianjian__shot03.md` | `ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot03/shot03.md` |
| `real_shots/xianjian__shot14.md` | `ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot14/shot14.md` |
| `real_shots/xianjian__shot17.md` | `ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot17/shot17.md` |
| `real_shots/xianjian__shot23.md` | `ai_videos/xianjian_yi_mv/5_6_分镜与prompt/shots/shot23/shot23.md` |
| `real_shots/wushen__ep01_shot03.md` | `ai_videos/wushen_juexing/5_6_分镜与prompt/episodes/ep01/shots/shot03/shot03.md` |
| `real_shots/wushen__ep03_shot05.md` | `ai_videos/wushen_juexing/5_6_分镜与prompt/episodes/ep03/shots/shot05/shot05.md` |
| `real_shots/wushen__ep06_shot01.md` | `ai_videos/wushen_juexing/5_6_分镜与prompt/episodes/ep06/shots/shot01/shot01.md` |
| `real_shots/rexue__shot01.md` | `ai_videos/rexue_gaoxiao/5_6_分镜与prompt/shots/shot01/shot01.md` |
| `real_shots/rexue__shot21.md` | `ai_videos/rexue_gaoxiao/5_6_分镜与prompt/shots/shot21/shot21.md` |
| `real_shots/duikang__shot01.md` | `ai_videos/duikang_shangzeng/5_6_分镜与prompt/shots/shot01/shot01.md` |
| `real_shots/duikang__shot09.md` | `ai_videos/duikang_shangzeng/5_6_分镜与prompt/shots/shot09/shot09.md` |
| `real_shots/duikang__shot20.md` | `ai_videos/duikang_shangzeng/5_6_分镜与prompt/shots/shot20/shot20.md` |
| `real_shots/xingji__shot02.md` | `ai_videos/xingji_yingjiu/5_6_分镜与prompt/shots/shot02/shot02.md` |
| `real_shots/xingji__shot10.md` | `ai_videos/xingji_yingjiu/5_6_分镜与prompt/shots/shot10/shot10.md` |
| `real_cards/hy3__c1_砌炉的老人.md` | `ai_videos/huangye_shenghuo/hy3/2_世界观人设/characters/c1_砌炉的老人/c1_砌炉的老人.md` |
| `real_cards/hy3__p3_抹泥板与黏土壁炉.md` | `ai_videos/huangye_shenghuo/hy3/2_世界观人设/props/p3_抹泥板与黏土壁炉/p3_抹泥板与黏土壁炉.md` |
| `real_cards/hy3__bg11_崖脚洼地.md` | `ai_videos/huangye_shenghuo/hy3/2_世界观人设/scenes/caoya/bg11_崖脚洼地/bg11_崖脚洼地.md` |
| `real_cards/hy2__c1_造家的人.md` | `ai_videos/huangye_shenghuo/hy2/2_世界观人设/characters/c1_造家的人/c1_造家的人.md` |
| `real_cards/wushen__bg6_空场_无碑.md` | `ai_videos/wushen_juexing/2_世界观人设/scenes/镇演武场/bg6_空场_无碑/bg6_空场_无碑.md` |
| `real_cards/xianjian__p1_木剑.md` | `ai_videos/xianjian_yi_mv/2_世界观人设/props/p1_木剑/p1_木剑.md` |
| `real_shots/hy3__shot02.crlf.md` | derived: `real_shots/hy3__shot02.md` with every LF replaced by CRLF (spec §8 divergence 5 — `core.autocrlf=true`) |
