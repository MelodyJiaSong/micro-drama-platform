# t02 Seedance 模拟镜头（v1，2026-11-14）

规则：生成永远人点——用户在对话里同意后才提交；先经 `tools/service_call.py` 写本期 `request_log.md` 再调用 Dreamina CLI。
统一参数：`dreamina text2video --model_version=seedance2.5 --video_resolution=720p --ratio=16:9`；成片里静音使用（只取画面），画面角标「AI 模拟画面」。
**不生成任何可识别的真人**（黄仁勋、两位女性当事人、议员、官员一律不出现；见 dossier §6.1）；不出英伟达 logo 与产品外观。
落盘：`seedance/<镜头id>/`（视频 + generation.json + prompt.txt + review.md），媒体不进 git。

| id | 用在哪 | 时长 | prompt |
|---|---|---|---|
| sd1_empty_stage | s0 l01–l02（公告：立即辞职） | 6 秒 | A large empty keynote stage in a dark arena after the show. A single spotlight shines on an empty spot at center stage, a giant blank screen behind it glowing faintly. The spotlight slowly dims and goes out. Rows of empty seats in the foreground, slow push-in, quiet, melancholic, realistic documentary look. No people, no text, no logos. |
| sd2_datacenter | s2 l10（芯片是科技战主战场） | 6 秒 | Inside a vast modern AI data center: long aisles of black server racks with dense blinking status lights and thick bundles of cables, cool blue light, faint haze. Slow dolly forward down the aisle. Realistic, cinematic, no people, no readable text, no logos or brand markings. |
| sd3_port | s2 l11（芯片绕道东南亚） | 6 秒 | Dusk at a busy Southeast Asian container port. A crane lowers a shipping container onto a cargo ship; in the foreground, a forklift carries wooden-crated server boxes wrapped in plastic toward a container. Humid air, orange sky, wide shot slowly panning. Realistic documentary footage, workers small and unrecognizable in the distance. No readable text, no logos. |
| sd4_hearing_room | s3 l18 / s6 l29（国会作证还在谈） | 6 秒 | An empty congressional hearing room: a raised curved dais with rows of leather chairs and microphones, a single empty witness table with one microphone facing it. Soft overhead light, dust in the air, slow push-in toward the empty witness chair. Realistic, quiet, tense. No people, no flags with readable text, no nameplates, no logos. |

合计 24 秒，预计约 480 积分（参考 t01：6 秒一条回执 120 积分）。积分以 Dreamina 回执为准。
